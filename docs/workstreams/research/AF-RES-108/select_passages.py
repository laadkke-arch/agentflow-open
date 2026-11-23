#!/usr/bin/env python3
"""Extract one source stream and apply two equal-budget W2 selectors."""
from argparse import ArgumentParser
from bisect import bisect_left
from hashlib import sha256
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from time import perf_counter_ns
import unicodedata

ROOT = Path(__file__).resolve().parent
TOKEN = re.compile(r"[a-z0-9_]+")
MARKER = re.compile(r"(?<![a-z0-9_])(?:except|unless|only\s+if|otherwise|must\s+not|does\s+not)(?![a-z0-9_])", re.I | re.ASCII)
SENTENCE_BREAK = re.compile(r"(?<=[.!?])(?=\s|$)")
LINK = re.compile(r"【\d+†([^】]+)】")


def digest(data):
    return sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()


def serialized(value):
    return json.dumps(value, separators=(",", ":"), sort_keys=True, ensure_ascii=False)


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def write_jsonl(path, values):
    path.write_text("".join(serialized(row) + "\n" for row in values))


# Unicode span projection and candidate generation inherited from AF-RES-104 W2.
def normalized(text):
    return unicodedata.normalize("NFKC", text).casefold()


def tokens(text):
    return set(TOKEN.findall(normalized(text)))


def normalized_with_origins(text):
    """Carry original codepoint spans through NFKD, canonical composition and folding."""
    if text.isascii():
        return text.casefold(), None
    ordered = []
    nonstarters = []
    for index, char in enumerate(text):
        for part in unicodedata.normalize("NFKD", char):
            record = (part, index, index + 1)
            if unicodedata.combining(part):
                nonstarters.append(record)
            else:
                ordered.extend(sorted(nonstarters, key=lambda item: unicodedata.combining(item[0])))
                nonstarters.clear()
                ordered.append(record)
    ordered.extend(sorted(nonstarters, key=lambda item: unicodedata.combining(item[0])))

    composed = []
    starter = None
    last_class = 0
    for char, start, end in ordered:
        mark_class = unicodedata.combining(char)
        if starter is not None and (last_class == 0 or last_class < mark_class):
            base, base_start, base_end = composed[starter]
            merged = unicodedata.normalize("NFC", base + char)
            if len(merged) == 1:
                composed[starter] = (merged, min(base_start, start), max(base_end, end))
                continue
        if not mark_class:
            starter = len(composed)
        composed.append((char, start, end))
        last_class = mark_class

    pieces, origins = [], []
    for char, start, end in composed:
        folded = char.casefold()
        pieces.append(folded)
        origins.extend([(start, end)] * len(folded))
    value = "".join(pieces)
    if value != normalized(text):
        raise ValueError("NFKC/casefold provenance decomposition disagrees with Python")
    return value, origins


def occurrences(text, wanted):
    value, origins = normalized_with_origins(text)
    hits = []
    for match in TOKEN.finditer(value):
        token = match.group()
        if token in wanted:
            start, end = match.span()
            if origins is not None:
                provenance = origins[start:end]
                start = min(item[0] for item in provenance)
                end = max(item[1] for item in provenance)
            hits.append((start, end, token))
    return sorted(hits)


def start_candidates(size, width, hits):
    last = size - width
    return {0, last, *(min(last, max(0, start - 100)) for start, _, _ in hits)}


def clamp(start, last):
    return max(0, min(last, start))


def candidate_pairs(size, first, second, hits):
    left_base = start_candidates(size, first, hits)
    right_base = start_candidates(size, second, hits)
    # One symmetric expansion from base starts adds adjacent boundaries.
    left = left_base | {clamp(start - first, size - first) for start in right_base}
    right = right_base | {clamp(start + first, size - second) for start in left_base}
    return sorted(left), sorted(right)


def unique_token_masks(starts, width, hits, bits):
    offsets = [start for start, _, _ in hits]
    masks = {}
    for start in starts:
        end = start + width
        mask = 0
        for index in range(bisect_left(offsets, start), bisect_left(offsets, end)):
            _, token_end, token = hits[index]
            if token_end <= end:
                mask |= bits[token]
        masks[start] = mask
    return masks


BLOCK = {"p", "div", "section", "article", "figure", "figcaption", "dd", "dt", "li",
         "blockquote", "br", "hr", "h1", "h2", "h3", "h4", "h5", "h6", "td", "th", "tr", "pre"}
SKIP = {"script", "style", "nav", "template", "svg"}


class Stream:
    def __init__(self):
        self.pieces = []
        self.map = []
        self.blocks = []
        self.size = 0
        self.block_start = 0
        self.kind = "prose"

    def append(self, text, origin, tag="text"):
        if not text:
            return
        end = self.size + len(text)
        self.pieces.append(text)
        self.map.append([self.size, end, origin, tag])
        self.size = end

    def break_block(self, origin, kind="prose"):
        if self.size > self.block_start:
            self.blocks.append([self.block_start, self.size, self.kind])
            self.append("\n\n", origin, "inserted-block-break")
        self.block_start = self.size
        self.kind = kind

    def finish(self):
        if self.size > self.block_start:
            self.blocks.append([self.block_start, self.size, self.kind])
        return "".join(self.pieces), self.blocks, self.map


class HTMLBody(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.stream = Stream()
        self.offsets = [0] + [m.end() for m in re.finditer("\n", source)]
        self.body = False
        self.skip = []
        self.pre = 0
        self.table = 0
        self.feed(source)
        self.close()

    def raw_offset(self):
        line, column = self.getpos()
        return self.offsets[line - 1] + column

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.body = True
        if not self.body:
            return
        if self.skip or tag in SKIP:
            if tag in SKIP:
                self.skip.append(tag)
            return
        self.pre += tag == "pre"
        self.table += tag == "table"
        if tag in BLOCK:
            self.stream.break_block(self.raw_offset(), self.kind())

    def kind(self):
        return "code" if self.pre else ("table" if self.table else "prose")

    def handle_endtag(self, tag):
        if self.skip:
            if tag == self.skip[-1]:
                self.skip.pop()
            return
        if tag == "body":
            self.body = False
        if tag in BLOCK:
            self.stream.break_block(self.raw_offset(), self.kind())
        if tag == "pre":
            self.pre = max(0, self.pre - 1)
        if tag == "table":
            self.table = max(0, self.table - 1)
        self.stream.kind = self.kind()

    def handle_data(self, data):
        if self.body and not self.skip:
            offset = self.raw_offset()
            self.stream.append(data, [offset, offset + len(data)])

    def handle_entityref(self, name):
        self.entity("&" + name + ";")

    def handle_charref(self, name):
        self.entity("&#" + name + ";")

    def entity(self, raw):
        if self.body and not self.skip:
            offset = self.raw_offset()
            self.stream.append(unescape(raw), [offset, offset + len(raw)], "entity")


def extract_web(source, key):
    """Convert numbered publisher-page web view into prose and code blocks."""
    out = Stream()
    minimum = 21 if key in {"lang_expr", "lang_aggfunc", "lang_select", "windowfunctions"} else 0
    fenced = False
    headings = re.compile(r"^\s*(?:#{1,6}\s+|[*+-]\s+|\d+\.\s+)")
    rules = re.compile(r"^\s*[-|: ]{3,}\s*$")
    for index, raw in enumerate(source.split("\n")):
        if index < minimum:
            continue
        if raw.strip().startswith("```"):
            fenced = not fenced
            out.break_block([index, 0], "code" if fenced else "prose")
            continue
        if not raw.strip() or rules.fullmatch(raw):
            out.break_block([index, 0])
            continue
        indented = raw.startswith("    ") and not headings.match(raw)
        kind = "code" if fenced or indented else ("table" if " | " in raw else "prose")
        lead = headings.match(raw) if not fenced else None
        if kind != out.kind or lead:
            out.break_block([index, 0], kind)
        elif out.size > out.block_start:
            out.append("\n", [index, 0], "inserted-line-break")
        start = lead.end() if lead else 0
        for match in LINK.finditer(raw, start):
            out.append(raw[start:match.start()], [index, start, match.start()])
            out.append(match[1], [index, match.start(1), match.end(1)], "web-link-label")
            start = match.end()
        out.append(raw[start:], [index, start, len(raw)])
    return out.finish()


def exception_spans(text, blocks, hits):
    offsets = [start for start, _, _ in hits]
    for a, b, kind in blocks:
        if kind != "prose":
            continue
        boundaries = [a, *(m.end() for m in SENTENCE_BREAK.finditer(text, a, b)), b]
        for left, right in zip(boundaries, boundaries[1:]):
            while left < right and text[left].isspace():
                left += 1
            while left < right and text[right - 1].isspace():
                right -= 1
            marker = MARKER.search(text, left, right)
            if marker is None:
                continue
            head = bisect_left(offsets, left)
            tail = bisect_left(offsets, right)
            if any(end <= right for _, end, _ in hits[head:tail]):
                yield [left, right, marker.group().lower()]


def positions_with_exception(starts, width, exceptions):
    a = [span[0] for span in exceptions]
    return {start for start in starts if any(
        right <= start + width for _, right, _ in exceptions[
            bisect_left(a, start):bisect_left(a, start + width)
        ])}


def choose(text, blocks, query_tokens):
    size = len(text)
    n = min(1200, size)
    if n < 2:
        ranges = [(0, 0), (0, n)]
        return {"K": ranges, "E": ranges}, {"n": n, "candidate_count": 1, "orientations": [],
                                              "fallback": True, "exceptions": [], "scores": [[0, 0], [0, 0]]}
    queries = [set(group) for group in query_tokens]
    wanted = set().union(*queries)
    bits = {name: 1 << index for index, name in enumerate(sorted(wanted))}
    q1, q2 = [sum(bits[token] for token in query) for query in queries]
    hits = occurrences(text, wanted)
    exceptions = list(exception_spans(text, blocks, hits))
    orientations = []
    best_k = best_e = None
    for w1, w2 in sorted({(n // 2, (n + 1) // 2), ((n + 1) // 2, n // 2)}):
        left, right = candidate_pairs(size, w1, w2, hits)
        left_mask = unique_token_masks(left, w1, hits, bits)
        right_mask = unique_token_masks(right, w2, hits, bits)
        left_e = positions_with_exception(left, w1, exceptions)
        right_e = positions_with_exception(right, w2, exceptions)
        pairs = e_pairs = 0
        for a in left:
            other = right[bisect_left(right, a + w1):]
            pairs += len(other)
            for b in other:
                union = left_mask[a] | right_mask[b]
                c1, c2 = (union & q1).bit_count(), (union & q2).bit_count()
                score = (-min(c1, c2), -c1-c2, a, b, w1, w2)
                if best_k is None or score < best_k:
                    best_k = score
                if a in left_e or b in right_e:
                    e_pairs += 1
                    if best_e is None or score < best_e:
                        best_e = score
        orientations.append({"widths":[w1,w2],"starts":[len(left),len(right)],
           "sha256":digest(serialized([left,right])),"pairs":pairs,"exception_qualified_pairs":e_pairs})
    if best_k is None:
        raise RuntimeError("No disjoint candidate at the registered width")

    def ranges(key):
        a,b,w1,w2=key[2:]
        return [(a,a+w1),(b,b+w2)]

    fallback = best_e is None
    chosen = best_e or best_k
    return {"K":ranges(best_k),"E":ranges(chosen)}, {
        "n":n, "fallback":fallback, "orientations":orientations,
        "candidate_count":sum(o["pairs"] for o in orientations),
        "occurrences":len(hits),"occurrence_sha256":digest(serialized(hits)),
        "exceptions":exceptions,"scores":[[-k[0],-k[1]] for k in [best_k,chosen]]
    }


def measure_segment(source, span, origin_map):
    a, b = span
    words = source[a:b]
    covered = [item for item in origin_map if item[0] < b and a < item[1]]
    return {
       "codepoints":list(span),"utf8":[len(source[:a].encode()),len(source[:b].encode())],
       "chars":len(words),"bytes":len(words.encode()),"sha256":digest(words),
       "upstream": [covered[0][2],covered[-1][2]] if covered else [],
    }


def build(cache, root):
    cases = json.loads((root / "inputs" / "selection.json").read_text())
    all_packets, docs, timings = [], {}, {}
    for case in cases:
        key = case["doc_key"]
        if key not in docs:
            path = cache / (key + ".html")
            method = "HTMLBody-v1"
            if not path.exists():
                path = cache / (key + ".view")
                method = "publisher-page-numbered-web-view-v1"
            raw = path.read_bytes()
            born = perf_counter_ns()
            text = raw.decode()
            source, blocks, origin_map = (
                HTMLBody(text).stream.finish() if path.suffix == ".html" else extract_web(text, key))
            (cache / (key + ".txt")).write_bytes(source.encode())
            (cache / (key + ".map.json")).write_text(serialized(origin_map))
            timings[key] = {"extraction_ns":perf_counter_ns()-born,
                            "source_codepoints":len(source),"map_entries":len(origin_map)}
            access = cache / (key + ".access.json")
            receipt = json.loads(access.read_text()) if access.exists() else {}
            docs[key] = (source, blocks, origin_map, {"url":case["doc_url"],"method":method,
                "publisher_page_sha256":digest(raw),"normalized_sha256":digest(source),
                "position_map_sha256":digest(serialized(origin_map)),"blocks_sha256":digest(serialized(blocks)),
                "raw_bytes":len(raw),"codepoints":len(source),"utf8_bytes":len(source.encode()),
                "line_views":receipt,
                "release_match":"2025-10-14 W3C CRD" if key == "flexbox" else "미확인 when publisher is rolling"})
        source, blocks, origin, info = docs[key]
        born = perf_counter_ns()
        selected, search = choose(source,blocks,case["query_tokens"])
        timings[case["case"]] = {"joint_selector_ns":perf_counter_ns()-born,
           "normalization_occurrences":search.get("occurrences",0),"candidate_pairs":search["candidate_count"],
           "marked_sentence_candidates":len(search["exceptions"])}
        header = {"document":info["url"],"snapshot_sha256":info["normalized_sha256"],
                  "task":case["unit"]}
        for item in case["inputs"]:
            for arm in ("K","E"):
                packet_id=digest(f'AF-RES-108/pre-answer/v1/{case["case"]}/{item["form"]}/{arm}')[:16]
                segments=[measure_segment(source,p,origin) for p in selected[arm]]
                meta=serialized(header)
                screen={
                    "opaque_id":packet_id, "metadata":header,"input":(root/item["path"]).read_text(),
                    "intervals":[{"start":a,"end":b,"text":source[a:b]} for a,b in selected[arm]],
                }
                all_packets.append({
                    "packet_id":packet_id, "case":case["case"],"input":item["form"],"arm":arm,
                    "input_file":item["path"],"input_sha256":item["sha256"],"doc":key,"metadata":header,
                    "metadata_sha256":digest(meta),"metadata_codepoints":len(meta),"metadata_utf8":len(meta.encode()),
                    "segments":segments,"cp":sum(s["chars"] for s in segments),
                    "utf8":sum(s["bytes"] for s in segments),"union_cp":sum(s["chars"] for s in segments),
                    "union_utf8":sum(s["bytes"] for s in segments),"boundaries":len(segments),"incremental_moves":0,
                    "screen_sha256":digest(serialized(screen)),
                    "candidate_profile":{k:v for k,v in search.items() if k not in {"exceptions","scores"}},
                    "exception_candidates":len(search["exceptions"]),
                    "included_marked_sentences":[s for s in search["exceptions"]
                        if any(a <= s[0] < s[1] <= b for a,b in selected[arm])],
                    "objective":search["scores"][arm=="E"],"mode_fallback":arm=="E" and search["fallback"],
                })
                out=cache/"reader"
                out.mkdir(exist_ok=True)
                (out / (packet_id+".json")).write_text(serialized(screen))
    all_packets.sort(key=lambda row: row["packet_id"])
    write_jsonl(root / "packets.jsonl", all_packets)
    (cache / "schedule.json").write_text(serialized([x["packet_id"] for x in all_packets]))
    (root / "evidence" / "documents.json").write_text(json.dumps(
        {k:v[3] for k,v in docs.items()}, ensure_ascii=False, indent=2)+"\n")
    (root / "evidence" / "preprocess-cost.json").write_text(json.dumps(timings,indent=2)+"\n")


def view(cache, low, high):
    ids=json.loads((cache / "schedule.json").read_text())
    for i,pid in enumerate(ids[low-1:high],low):
        screen=json.loads((cache/"reader"/(pid+".json")).read_text())
        print(f'\n{i}. {pid}', screen["metadata"]["document"], screen["metadata"]["task"])
        print(screen["input"].strip())
        for s in screen["intervals"]:
            print(f'[{s["start"]},{s["end"]})\n{s["text"]}')


def main():
    parser = ArgumentParser()
    parser.add_argument("cache", type=Path)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--view", type=int, nargs=2)
    args = parser.parse_args()
    if args.view is not None:
        view(args.cache, *args.view)
    else:
        build(args.cache, args.root)


if __name__ == "__main__":
    main()
