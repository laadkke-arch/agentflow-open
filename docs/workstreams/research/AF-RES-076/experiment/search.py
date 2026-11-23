"""Run L/S/E ranking with only a whitelisted input packet and a transport."""
import argparse
import csv
import hashlib
import html
import json
import re
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

ARMS = "LSE"
MODES = ("cold", "repeat")
PACKET = {"L.jsonl", "S.jsonl", "E.jsonl", "documents.jsonl", "requests.jsonl"}
MAX_CALLS = 3
MAX_BODY = 1024 * 1024
MAX_DISPLAY_WORDS = 750
WINDOW_LINES = 14
WINDOW_WORDS = 108
STOP_WORDS = frozenset(
    "a an and are as at be both by for from has have how in into is it its of on or our "
    "so store than that the then this to use using was were what when which with within".split()
)


def words(text):
    return len(text.split())


def tokens(text):
    split = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text)
    parts = re.findall(r"[a-z][a-z0-9]*", split.casefold())
    return set(parts) - STOP_WORDS


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            print(json.dumps(row, ensure_ascii=False, separators=(",", ":")), file=stream)


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def clean_lines(body, url):
    lines = body.decode("utf-8").splitlines()
    markdown = url.endswith(".md")
    web_source = url.endswith((".html", ".bs"))
    front_matter = markdown and bool(lines) and lines[0] == "---"
    out = []
    for number, line in enumerate(lines, 1):
        if front_matter:
            if number > 1 and line == "---":
                front_matter = False
            continue
        if markdown:
            line = re.sub(r"\[([^\]]+)\]\((?:\{%.*?%\}|[^)]+)\)", r"\1", line)
            line = re.sub(r"\{%.*?%\}", "", line)
        if web_source:
            line = re.sub(r"<(?!<)[!/a-zA-Z][^>]*>", "", line)
            line = html.unescape(line)
        if url.endswith(".rst"):
            line = re.sub(r":py:\w+:`~?([^`]+)`", r"\1", line)
        if url.endswith(".json") and '"doc":' in line:
            match = re.search(r'"doc":\s*(".*")(?:,)?\s*$', line)
            if match:
                line = json.loads(match[1]).replace("\n", " ")
        line = " ".join(line.strip(" `#\t").split())
        if line and any(char.isalnum() for char in line):
            out.append((number, line))
    return out


def select_window(body, url, query):
    cleaned = clean_lines(body, url)
    scanned = sum(words(line) for _, line in cleaned)
    best_score = -1
    best = None
    for pos, (first, _) in enumerate(cleaned):
        selection = []
        remaining = WINDOW_WORDS
        for end, line in cleaned[pos:pos + WINDOW_LINES]:
            if end - first >= WINDOW_LINES:
                break
            line_words = line.split()
            chosen = line_words[:remaining]
            selection.append((end, " ".join(chosen)))
            remaining -= len(chosen)
            if remaining == 0:
                break
        text = "\n".join(line for _, line in selection)
        score = len(query & tokens(text))
        if score > best_score:
            best_score = score
            best = {"start": first, "end": selection[-1][0], "text": text,
                    "source_lines": [number for number, _ in selection]}
    return best, scanned


def load_packet(directory):
    allowed = {x.name for x in directory.iterdir()}
    if allowed != PACKET or any((directory / f).is_symlink() for f in PACKET):
        raise ValueError(f"Unexpected input packet paths: {sorted(allowed ^ PACKET)}")
    data = {name: read_jsonl(directory / name) for name in sorted(PACKET)}
    docs = data["documents.jsonl"]
    assert len(docs) == 20 and len(data["requests.jsonl"]) == 12
    assert len({x["candidate_id"] for x in docs}) == len(docs)
    assert len({x["url"] for x in docs}) == len(docs)
    paths = {}
    for arm in ARMS:
        material = data[arm + ".jsonl"]
        assert len(material) == len(docs)
        assert [x if arm == "L" else x["url"] for x in material] == [d["url"] for d in docs]
        if arm != "L":
            assert all(words(x["name"] + " " + x["text"]) <= 40 for x in material)
        paths[arm] = {d["candidate_id"]: {"url": x} if arm == "L" else x
                      for d, x in zip(docs, material)}
    return data["requests.jsonl"], docs, paths


class LiveTransport:
    def __init__(self, cache_dir):
        self.cache_dir = cache_dir
        self.captures = []

    def fetch(self, query, document, key, remaining):
        cache_file = self.cache_dir / key["request"] / key["arm"] / document["candidate_id"]
        started = time.monotonic()
        result = dict(key, fetch_url=document["fetch_url"], arrival_url=None, http_status=None,
                      received_body_b=0, body_sha256=None, cache_write_b=0, content_length=None,
                      storage="cache" if cache_file.exists() else "http", status="ok",
                      wall_ms=None, error=None, window=None, scanned_words=0,
                      observed_utc=datetime.now(timezone.utc).isoformat(), retry_count=0)
        data = None
        try:
            if cache_file.exists():
                data = cache_file.read_bytes()
                result["arrival_url"] = document["fetch_url"]
            else:
                request = urllib.request.Request(
                    document["fetch_url"],
                    headers={"User-Agent": "AF-RES-076 reproducibility", "Accept-Encoding": "identity"},
                )
                with urllib.request.urlopen(request, timeout=15) as response:
                    result["arrival_url"] = response.url
                    result["http_status"] = response.status
                    length = response.headers.get("Content-Length")
                    result["content_length"] = int(length) if length and length.isdecimal() else None
                    if result["content_length"] is not None and result["content_length"] > remaining:
                        result["status"] = "budget_skip_body"
                    else:
                        data = response.read(remaining)
                        result["received_body_b"] = len(data)
                        if len(data) == remaining and result["content_length"] != remaining:
                            result["status"] = "budget_truncated"
                            data = None
        except urllib.error.HTTPError as error:
            result.update(status="http_error", http_status=error.code,
                          arrival_url=error.geturl(), error=str(error))
            error.close()
        except OSError as error:
            result.update(status="failed", error=str(error))

        if data is not None:
            result["body_sha256"] = sha(data)
            if result["body_sha256"] != document["document_sha256"]:
                result["status"] = "edition_mismatch"
            else:
                result["window"], result["scanned_words"] = select_window(
                    data, document["fetch_url"], query
                )
                if result["window"] is None:
                    result["status"] = "no_window"
                if result["storage"] == "http":
                    cache_file.parent.mkdir(parents=True, exist_ok=True)
                    cache_file.write_bytes(data)
                    result["cache_write_b"] = cache_file.stat().st_size
        result["wall_ms"] = round((time.monotonic() - started) * 1000)
        self.captures.append(result)
        return result


class FrozenTransport:
    def __init__(self, captures):
        self.events = iter(captures)

    def fetch(self, query, document, key, remaining):
        event = next(self.events)
        assert {name: event[name] for name in key} == key, (event, key)
        assert event["fetch_url"] == document["fetch_url"]
        assert event["received_body_b"] <= remaining
        if event["status"] in {"ok", "no_window"}:
            assert event["body_sha256"] == document["document_sha256"]
        return event

    def finish(self):
        assert next(self.events, None) is None, "Unused replay event"


def ordered(scores):
    return sorted(scores, key=lambda candidate: (-scores[candidate], candidate))


def terms_request(request):
    return tokens(" ".join(request[name] for name in ("part", "purpose", "c1", "c2", "environment")))


def render(document, representation, view):
    header = [document["url"], document["edition"]]
    card = None
    if "name" in representation:
        card = representation["name"] + " " + representation["text"]
        header.append(card)
    text = "\n".join(header + ([view["text"]] if view else []))
    return {
        "kind": "original" if view else "card_only" if card else "none",
        "candidate_url": document["url"], "edition": document["edition"], "card": card,
        "view": view, "display_words": words(text), "display_b": len(text.encode()),
        "display_sha256": sha(text.encode()),
    }


def run_route(request, arm, mode, documents, records, transport):
    query = terms_request(request)
    def index_words(cid):
        record = records[cid]
        path = urlsplit(record["url"]).path.split("/", 5)[-1]
        return tokens(path + " " + record.get("name", "") + " " + record.get("text", ""))

    initial = {cid: len(query & index_words(cid)) for cid in documents}
    scores = initial.copy()
    stages = [dict(scores)]
    history = {}
    received = 0
    for step in range(1, MAX_CALLS + 1):
        before = ordered(scores)
        cid = next(c for c in before if c not in history)
        key = {"request": request["id"], "arm": arm, "cache": mode, "step": step, "candidate": cid}
        event = transport.fetch(query, documents[cid], key, MAX_BODY - received)
        received += event["received_body_b"]
        view = event["window"]
        rank_gain = len(query & tokens(view["text"])) if view else -1
        scores[cid] += rank_gain
        stages.append(dict(scores))
        display = render(documents[cid], records[cid], view)
        history[cid] = {
            "fetch_id": f"F-{request['id']}-{arm}-{mode}-{step}",
            **event, "remaining_body_b": MAX_BODY - received,
            "before_top3": before[:3], "after_top3": ordered(scores)[:3],
            "rank_delta_score": rank_gain, **display,
        }

    order_by_stage = [{cid: p for p, cid in enumerate(ordered(stage), 1)} for stage in stages]
    final = ordered(scores)[:3]
    ranks = []
    for cid in ordered(initial):
        start = initial[cid]
        record = {
            "rank_id": f"R-{request['id']}-{arm}-{mode}-{cid}", "request_id": request["id"],
            "arm": arm, "cache": mode, "candidate_id": cid, "initial_score": start,
            "initial_rank": order_by_stage[0][cid],
            "initial_tie_n": list(initial.values()).count(start),
        }
        for n in range(1, 4):
            record[f"score_after_{n}"] = stages[n][cid]
            record[f"rank_after_{n}"] = order_by_stage[n][cid]
        record["final_slot"] = final.index(cid) + 1 if cid in final else ""
        record["opened_step"] = history[cid]["step"] if cid in history else ""
        record["fetch_id"] = history[cid]["fetch_id"] if cid in history else ""
        ranks.append(record)

    entries = list(history.values())
    opened_display = sum(x["display_words"] for x in entries)
    opened_b = sum(x["display_b"] for x in entries)
    unseen = [render(documents[cid], records[cid], None) for cid in final if cid not in history]
    words_display = opened_display + sum(x["display_words"] for x in unseen)
    bytes_display = opened_b + sum(x["display_b"] for x in unseen)
    assert received <= MAX_BODY and words_display <= MAX_DISPLAY_WORDS
    cost = {
        "request_id": request["id"], "arm": arm, "cache": mode,
        "attempts": len(entries), "http_calls": sum(e["storage"] == "http" for e in entries),
        "cache_reads": sum(e["storage"] == "cache" for e in entries),
        "network_body_b": received, "display_b": bytes_display, "display_words": words_display,
        "card_words": sum(words(e["card"]) for e in entries + unseen if e.get("card")),
        "machine_scan_words": sum(e["scanned_words"] for e in entries),
        "machine_index_records": len(records),
        "new_cache_b": sum(e["cache_write_b"] for e in entries),
        "wall_transport_and_extraction_ms": sum(e["wall_ms"] for e in entries),
        "failures": sum(e["status"] != "ok" for e in entries),
        "retry_count": sum(e["retry_count"] for e in entries),
    }
    return ranks, entries, cost


def run(directory, transport, output):
    requests, docs, indexes = load_packet(directory)
    documents = {doc["candidate_id"]: doc for doc in docs}
    ranks, fetches, costs = [], [], []
    for request in requests:
        for arm in ARMS:
            for mode in MODES:
                ranking, attempts, cost = run_route(request, arm, mode, documents, indexes[arm], transport)
                ranks.extend(ranking)
                fetches.extend(attempts)
                costs.append(cost)
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / "ranks.csv", ranks)
    write_jsonl(output / "fetches.jsonl", fetches)
    write_csv(output / "route-costs.csv", costs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("output", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--live", action="store_true")
    mode.add_argument("--replay", type=Path)
    args = parser.parse_args()
    if args.live:
        with tempfile.TemporaryDirectory(prefix="af076-body-cache-") as raw:
            transport = LiveTransport(Path(raw))
            run(args.packet, transport, args.output)
            write_jsonl(args.output / "captures.jsonl", transport.captures)
    else:
        transport = FrozenTransport(read_jsonl(args.replay))
        run(args.packet, transport, args.output)
        transport.finish()
    for path in sorted(args.output.iterdir()):
        print(sha(path.read_bytes()), path.name, path.stat().st_size)


if __name__ == "__main__":
    main()
