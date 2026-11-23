"""Run L, I, H and the purpose projection inside the public corpus boundary."""

import argparse
import csv
import gzip
import json
import math
import re
import time
import unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urldefrag, urlsplit

from capture import jsonl, lines
from passages import reading_windows
from source_io import DISPLAY, MAX_BODY, MAX_OPENS, WINDOW, retrieve, sha, utc

ROOT = Path(__file__).resolve().parent
ARMS = ("L", "I", "H", "P")
CARD = ("name", "purpose", "inputs", "action", "constraints")
STOP = set(("a an and are as at be by for from has have how i in into is it its of on or "
            "our should that the their then there these this those to was what when where which "
            "will with would you your").split())
URL_STOP = set("src site xdoc index publishing snapshot snapshots overview note rec md xml html nara preservation action plan".split())
BOUNDARY_MARKERS = set(("not no without error except unless incompatible cannot fail invalid skip "
                        "ignore omit suppress instead only never unsupported required").split())


def words(text):
    text = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", text)
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    text = unicodedata.normalize("NFKC", text).casefold()
    result = []
    for word in re.findall(r"[^\W_]+", text):
        if len(word) < 2 or word.isdigit() or word in STOP:
            continue
        if word.isascii() and len(word) > 4 and word.endswith("ies"):
            word = word[:-3] + "y"
        elif word.isascii() and len(word) > 3 and word.endswith("s") and not word.endswith(("ss", "us", "is")):
            word = word[:-1]
        result.append(word)
    return result


def url_terms(url):
    path = unquote(urlsplit(url).path)
    path = re.sub(r"/[0-9a-f]{40}(?=/)", "", path)
    return [token for token in words(path) if token not in URL_STOP]


class BM25:
    def __init__(self, token_lists):
        self.documents = {key: Counter(tokens) for key, tokens in token_lists.items()}
        self.lengths = {key: sum(counts.values()) for key, counts in self.documents.items()}
        self.average = sum(self.lengths.values()) / max(1, len(self.lengths)) or 1
        self.df = Counter(token for document in self.documents.values() for token in document)

    def idf(self, token):
        hits = self.df[token]
        size = len(self.documents)
        return math.log1p((size - hits + 0.5) / (hits + 0.5))

    def scores(self, terms):
        query = sorted(set(terms))
        values = {}
        for key, counts in self.documents.items():
            norm = 1.2 * (0.25 + 0.75 * self.lengths[key] / self.average)
            values[key] = sum(self.idf(term) * counts[term] * 2.2 / (counts[term] + norm)
                              for term in query if counts[term])
        return values

    def coverage(self, query, tokens):
        query = sorted(set(query))
        tokens = set(tokens)
        available = sum(self.idf(x) for x in query)
        matched = sum(self.idf(x) for x in query if x in tokens)
        return matched / available if available else 0.0


def stable(work):
    return sha(f"AF-RES-072-tie:{work}".encode())


def ordering(scores, exclude=()):
    return sorted((key for key in scores if key not in exclude), key=lambda k: (-round(scores[k], 12), stable(k)))


def comparable(scores):
    peak = max(scores.values(), default=0) or 1
    return {key: value / peak for key, value in scores.items()}


def first_window(raw, url, query, boundary, index, arm):
    windows, scanned = reading_windows(raw, url)
    highest = None
    best = -1
    for window in windows:
        text = words(window.text)
        score = index.coverage(query, text)
        if arm == "H":
            score += 0.20 * index.coverage(boundary, text)
            score += 0.05 * bool(set(text) & BOUNDARY_MARKERS)
        if score > best + 1e-12:
            highest, best = window, score
    return highest, scanned


class Route:
    def __init__(self, input_dir, arm):
        self.path = input_dir
        self.arm = arm
        self.addresses = {row["work_id"]: row["url"] for row in lines(input_dir/"urls.jsonl")}
        self.card_text = {}
        if arm == "L":
            token_lists = {work: url_terms(url) for work, url in self.addresses.items()}
        else:
            fields = CARD if arm in {"I", "H"} else CARD[:2]
            file = "cards.jsonl" if arm in {"I", "H"} else "purpose.jsonl"
            self.card_text = {row["work_id"]: " ".join(row[key] for key in fields)
                              for row in lines(input_dir/file)}
            token_lists = {work: words(text) for work, text in self.card_text.items()}
            assert set(self.card_text) == set(self.addresses)
            assert all(len(value.split()) <= 80 for value in self.card_text.values())
        self.terms = {work: set(tokens) for work, tokens in token_lists.items()}
        self.index = BM25(token_lists)

    def choose(self, base, query, seen, links, tried, current):
        avail = set(base) - set(tried)
        if not tried:
            return ordering(base)[0], "first-url" if self.arm == "L" else "first-card"
        if self.arm == "L":
            context = Counter(token for window in seen.values() for token in set(words(window.text)))
            gains = {work: sum(self.index.idf(t) for t in sorted(self.terms[work] & context.keys()))
                     for work in avail}
            gains = comparable(gains)
            scores = {work: base[work] + 0.35*gains[work] + 0.65*(self.addresses[work] in links)
                      for work in avail}
            winner = ordering(scores)[0]
            why = ("follow-observed-link" if self.addresses[winner] in links else
                   "observed-terms+url" if gains[winner] else "remaining-url")
            return winner, why
        covered = set(token for window in seen.values() for token in words(window.text))
        fresh = set(query) - covered
        leader = max(current.values(), default=0)
        scores = {}
        for work in avail:
            distance = max(0.0, 1 - abs(leader - base[work]))
            scores[work] = (0.50*base[work] + 0.25*distance +
                            0.25*self.index.coverage(fresh, self.terms[work]))
        return ordering(scores)[0], "card-margin+uncovered-actions"

    def combined(self, base, query, seen, rejected):
        weight = 1.0 if self.arm == "L" else 0.65
        scores = {work: weight*score for work, score in base.items() if work not in rejected}
        for work, window in seen.items():
            coverage = self.index.coverage(query, words(window.text))
            scores[work] += (1.0 if self.arm == "L" else 0.35) * coverage
        return scores

    def run(self, case, network, cache, injected_failure=None):
        start = time.perf_counter_ns()
        requested = case["request_id"]
        query, boundary = words(case["query"]), words(case["boundary"])
        base = comparable(self.index.scores(query))
        current = base
        prior = ordering(current)[:3]
        seen = {}
        tried = []
        failures = set()
        links = set()
        attempt_rows = []
        used_bytes = shown = scan_words = local_bytes = 0
        card_count = len(self.card_text)
        cache_start_bytes = sum(map(len, cache.values()))
        maximum = MAX_OPENS if self.arm in {"L", "H"} else 0
        for attempt in range(1, maximum + 1):
            if used_bytes >= MAX_BODY or len(tried) >= len(base):
                break
            work, reason = self.choose(base, query, seen, links, tried, current)
            tried.append(work)
            url = self.addresses[work]
            row = dict(fetch_id=f"F-{requested}-{self.arm}-{attempt}", request_id=requested, path=self.arm,
                       attempt=attempt, work_id=work, selection_reason=reason, remaining_before_bytes=MAX_BODY-used_bytes,
                       url=url, top3_before=prior)
            local_fetch = dict(utc=None, final_url=url, http_status=None, error=None, headers={},
                               redirects=[], http_attempts=0, retries=0, read_bytes=0, body_sha256=None, complete=False)
            if injected_failure == (requested, work):
                raw = None
                row.update(local_fetch, transport="injected-offline", error="synthetic-unavailable")
            elif network and work in cache:
                raw = cache[work]
                row.update(local_fetch, transport="memory-hit", body_sha256=sha(raw), complete=True)
                local_bytes += len(raw)
            elif network:
                raw, receipt = retrieve(url, MAX_BODY-used_bytes)
                row.update(receipt, transport="http")
                used_bytes += receipt["read_bytes"]
                if raw is not None:
                    cache[work] = raw
            else:
                at = self.path/"frozen"/"body"/f"{work}.gz"
                raw = gzip.decompress(at.read_bytes()) if at.is_file() else None
                row.update(local_fetch, transport="offline", body_sha256=sha(raw) if raw else None,
                           complete=raw is not None, error=None if raw else "missing-frozen-body")
                local_bytes += len(raw) if raw else 0
            window = None
            if row["complete"]:
                try:
                    window, scans = first_window(raw, url, query, boundary, self.index, self.arm)
                    scan_words += scans
                except (ValueError, OSError, SyntaxError) as exc:
                    row["error"] = f"parse-{type(exc).__name__}"
                if window is None and row["error"] is None:
                    row["error"] = "no-readable-window"
            if window is None:
                failures.add(work)
                row.update(section=None, origin_lines=None, display_words=0, passage_sha256=None,
                           passage=None, boundary_signals=[], observed_member_links=[])
            else:
                seen[work] = window
                member_links = sorted({urldefrag(link).url for link in window.links
                                       if urldefrag(link).url in self.addresses.values()})
                links.update(member_links)
                shown += len(window.text.split())
                row.update(section=window.section, origin_lines=[window.start, window.end],
                           display_words=len(window.text.split()), passage_sha256=sha(window.text.encode()),
                           passage=window.text,
                           boundary_signals=sorted(set(words(window.text)) & BOUNDARY_MARKERS),
                           observed_member_links=member_links)
            current = self.combined(base, query, seen, failures)
            prior = ordering(current)[:3]
            row["top3_after"] = prior
            row["local_body_bytes"] = len(raw) if raw is not None and row["transport"] in {"offline","memory-hit"} else 0
            attempt_rows.append(row)

        final = ordering(current)[:3]
        ranks = []
        for slot in range(1, 4):
            work = final[slot-1] if slot <= len(final) else None
            text = self.card_text.get(work, "")
            shown += len(text.split())
            shown_words = len(text.split())
            ranks.append(dict(rank_id=f"R-{requested}-{self.arm}-{slot}", request_id=requested, path=self.arm,
                              rank=slot, work_id=work, url=self.addresses.get(work),
                              score=round(current[work], 9) if work else None,
                              baseline_rank=ordering(base).index(work)+1 if work else None,
                              opened=work in seen, failed=work in failures, displayed_card_words=shown_words))
        assert len(attempt_rows) <= MAX_OPENS and shown <= DISPLAY and used_bytes <= MAX_BODY
        cost = dict(request_id=requested, path=self.arm, logical_opens=len(attempt_rows),
                    http_requests=sum(row["http_attempts"]+len(row["redirects"]) for row in attempt_rows),
                    retries=sum(row["retries"] for row in attempt_rows), failures=len(failures),
                    cache_hits=sum(row["transport"] == "memory-hit" for row in attempt_rows),
                    http_body_bytes=used_bytes, local_body_bytes=local_bytes,
                    displayed_words=shown, scanned_card_rows=card_count,
                    scanned_url_rows=len(base) if self.arm == "L" else 0, scanned_body_words=scan_words,
                    unused_opens=MAX_OPENS-len(attempt_rows), unused_display_words=DISPLAY-shown,
                    unused_http_bytes=MAX_BODY-used_bytes, cache_start_bytes=cache_start_bytes,
                    cache_end_bytes=sum(map(len,cache.values())),
                    elapsed_ns=time.perf_counter_ns()-start,
                    http_elapsed_ns=sum(row.get("elapsed_ns",0) for row in attempt_rows))
        return ranks, attempt_rows, cost


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--input", default=ROOT, type=Path)
    parser.add_argument("--split", choices=("pilot", "holdout"), default="holdout")
    parser.add_argument("--mode", choices=("offline", "live", "translated", "failure"), default="offline")
    parser.add_argument("--arms", nargs="+", choices=ARMS, default=ARMS)
    parser.add_argument("--drop", nargs=2, metavar=("REQUEST", "WORK"))
    args = parser.parse_args()
    if (args.mode == "failure") != (args.drop is not None):
        parser.error("the failure replay requires --drop REQUEST WORK, which is reserved for this mode")
    args.output.mkdir(parents=True, exist_ok=False)
    cases = [row for row in lines(args.input/"requests.jsonl") if row["split"] == args.split]
    if args.mode == "translated":
        translations = {row["request_id"]:row for row in lines(args.input/"translated.jsonl")}
        cases = [case | {key: translations[case["request_id"]][key] for key in ("query","boundary")}
                 for case in cases if case["request_id"] in translations]
    network = args.mode == "live"
    schedule = ("cold", "repeat") if network else (args.mode,)
    ranks, attempts, costs, builds = [], [], [], []
    started = utc()
    for arm in args.arms:
        start = time.perf_counter_ns()
        route = Route(args.input, arm)
        builds.append(dict(path=arm, elapsed_ns=time.perf_counter_ns()-start,
                           index_rows=len(route.index.documents)))
        for case in cases:
            cache = {}
            for phase in schedule:
                r, a, c = route.run(case, network, cache, tuple(args.drop) if args.drop else None)
                ranks.extend(dict(phase=phase,**row) for row in r)
                attempts.extend(dict(phase=phase,**row) for row in a)
                costs.append(dict(phase=phase,**c))
    write_csv(args.output/"ranks.csv", ranks)
    jsonl(args.output/"fetches.jsonl", attempts)
    write_csv(args.output/"costs.csv", costs)
    (args.output/"build.json").write_text(json.dumps(dict(start_utc=started, end_utc=utc(), build=builds),indent=2)+"\n")
    print(json.dumps(dict(ranks=len(ranks), attempts=len(attempts), paths=len(costs), started=started, completed=utc())))


if __name__ == "__main__":
    main()
