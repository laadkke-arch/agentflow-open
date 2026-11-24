"""Pinned inputs and source section capture for the two display-depth comparisons."""
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import UTC, datetime
from hashlib import sha256
import io
import json
from pathlib import Path
import re
import subprocess
from time import perf_counter_ns, process_time_ns
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent.parent
PIN142 = "6c379fe049e8e8416c4a42df8dcb9f76de36b684"
PIN138 = "198e74358fe2d124c31e16f8bbb93dbbf7ee561d"
PATH142 = "docs/workstreams/research/AF-RES-142/"
PATH138 = "docs/workstreams/research/AF-RES-138/"
LEGACY_FILES = ("cards.csv", "rank_scores.csv", "slots.csv", "judgments.csv", "requests.jsonl", "role_spans.jsonl")
GITHUB_CLAUSE = re.compile(r"https://github\.com/([^/]+/[^/]+)/blob/([0-9a-f]{40})/(.+)#L(\d+)-L(\d+)")


def digest(data):
    return sha256(data).hexdigest()


def git_bytes(sha, path):
    return subprocess.check_output(["git", "show", f"{sha}:{path}"])


def read_csv(raw):
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))


def read_jsonl(raw):
    return [json.loads(line) for line in raw.splitlines()]


def legacy_inputs():
    material = {f"{PATH142}{name}": git_bytes(PIN142, PATH142 + name) for name in LEGACY_FILES}
    material[PATH138 + "requests.jsonl"] = git_bytes(PIN138, PATH138 + "requests.jsonl")
    cards, rows, slots, truth = (read_csv(material[PATH142 + name]) for name in LEGACY_FILES[:4])
    cases = {row["request_id"]: row["layer"] for row in rows}
    requirements = {
        **{r["request_id"]: r for r in read_jsonl(material[PATH142 + "requests.jsonl"])},
        **{"C-" + r["request_id"]: r for r in read_jsonl(material[PATH138 + "requests.jsonl"])},
    }
    authority = {(row["request_id"], row["card_id"]): row for row in truth}
    assert len(cards) == 22 and len(cases) == 11 and len(rows) == 836 and len(slots) == 484
    assert len(authority) == 242 and set(requirements) == set(cases)
    assert Counter(row["grade"] for row in truth) == {"direct": 2, "partial": 6, "conflict": 3, "unconfirmed": 231}
    assert all(row["alternative_grade"] == "partial" for row in truth if row["grade"] == "direct")
    passes = [(r["request_id"], r["card_id"]) for r in slots if r["stage"] == "display" and r["card_id"]]
    assert passes == [("C-P1-07", "S04")]
    assert sum(r["stage"] == "display" and not r["card_id"] for r in slots) == 131
    assert sum(r["stage"] == "investigate" and r["logical_inspection"] == "1" for r in slots) == 89

    by_policy = defaultdict(list)
    for row in rows:
        by_policy[(row["pool"], row["mode"], row["request_id"])].append(row)
    orders = {row["feature_id"]: idx for idx, row in enumerate(cards)}
    slotted = {(r["pool"], r["mode"], r["request_id"], r["card_id"]): r
               for r in slots if r["stage"] == "investigate" and r["card_id"]}
    ranks = {}
    for (pool, mode, event), rows in by_policy.items():
        ordered = sorted(rows, key=lambda r: (-int(r["score"]), orders[r["id"]]))
        ranks[(f"{pool}/{mode}", event)] = []
        for rank, row in enumerate(ordered, 1):
            score = int(row["score"])
            if score:
                assert int(row["positive_rank"]) == rank
            assert (row["investigate"] == "yes") == (score > 0 and rank <= 8)
            assert ((pool, mode, event, row["id"]) in slotted) == (row["investigate"] == "yes")
            ranks[(f"{pool}/{mode}", event)].append({"card_id": row["id"], "score": score, "rank": rank,
                                                    "hits": row["english"]})
    return {"material": material, "cards": {row["feature_id"]: row for row in cards},
            "ranks": ranks, "slots": slotted, "truth": authority, "cases": cases, "requests": requirements}


def tokens(text):
    return re.findall(r"[^\W_]+", text.casefold(), flags=re.UNICODE)


def score_new(card, query):
    text = " " + " ".join(tokens(query)) + " "
    operations = set(card["operation_aliases"])
    terms = set(card["terms"]) - operations

    def matches(aliases):
        return sorted(alias for alias in aliases if f" {' '.join(tokens(alias))} " in text)

    op_hits, term_hits = matches(operations), matches(terms)
    return 2*len(op_hits) + len(term_hits), op_hits + term_hits


def rank_new(cards, requests):
    ranks = {}
    for row in requests:
        query = " ".join(row["query_fields"])
        scored = []
        for card in cards:
            points, hits = score_new(card, query)
            scored.append({"card_id": card["card_id"], "score": points, "hits": " | ".join(hits)})
        ordered = sorted(scored, key=lambda r: (-r["score"], r["card_id"]))
        ranks[row["event_id"]] = [dict(result, rank=index) for index, result in enumerate(ordered, 1)]
    return ranks


def legacy_capture_spec(card):
    match = GITHUB_CLAUSE.fullmatch(card["clause_url"])
    repo, sha, file, start, end = match.groups()
    return {"kind": "git_source_lines", "raw_url": f"https://raw.githubusercontent.com/{repo}/{sha}/{file}",
            "start": int(start), "end": int(end)}


def fetch(url):
    t0, c0 = perf_counter_ns(), process_time_ns()
    with urlopen(url, timeout=30) as response:
        raw = response.read()
        assert response.status == 200
        receipt = {"url": url, "final_url": response.url, "http_status": response.status,
                   "sha256": digest(raw), "bytes": len(raw),
                   "opened_utc": datetime.now(UTC).isoformat(timespec="milliseconds"),
                   "wall_ns": perf_counter_ns()-t0, "process_cpu_ns_concurrent": process_time_ns()-c0}
    return raw, receipt


def collect_sources(output, specs):
    """Pin padded bytes to exact upstream line ranges or the already-verified reading note."""
    output.mkdir(parents=True)
    urls = sorted({s["raw_url"] for s in specs.values() if s["kind"] == "git_source_lines"})
    t0, c0 = perf_counter_ns(), process_time_ns()
    with ThreadPoolExecutor(max_workers=6) as pool:
        fetched = dict(zip(urls, pool.map(fetch, urls), strict=True))
    sections = {}
    for key, spec in specs.items():
        if spec["kind"] == "git_source_lines":
            raw, receipt = fetched[spec["raw_url"]]
            lines = raw.splitlines(keepends=True)
            start, end = spec["start"], spec["end"]
            assert 1 <= start <= end <= len(lines), key
            if spec.get("source_file_sha256"):
                assert receipt["sha256"] == spec["source_file_sha256"], key
            data = b"".join(lines[start-1:end])
        else:
            assert spec["kind"] == "verified_reading_note"
            data = spec["text"].encode()
        hashed = digest(data)
        if spec.get("sha256"):
            assert hashed == spec["sha256"], key
        filename = hashed + ".txt"
        file = output / filename
        if not file.exists():
            file.write_bytes(data)
        sections[key] = {"sha256": hashed, "bytes": len(data), "file": filename, "kind": spec["kind"]}
    return {"sections": sections, "upstream_fetches": [receipt for _,receipt in fetched.values()],
            "setup_process_cpu_ns": process_time_ns()-c0, "setup_wall_ns": perf_counter_ns()-t0}


def snapshot_specs(cards, legacy):
    return {**{r["card_id"]: r["capture"] for r in cards},
            **{cid: legacy_capture_spec(card) for cid, card in legacy["cards"].items()}}


def main():
    cards = read_jsonl((ROOT/"inventory.jsonl").read_bytes())
    requests = read_jsonl((ROOT/"requests.jsonl").read_bytes())
    for event, rows in rank_new(cards, requests).items():
        print(event, [(r["card_id"],r["score"],r["hits"]) for r in rows])
    if len(__import__("sys").argv) == 2:
        folder = Path(__import__("sys").argv[1])
        folder.mkdir(parents=True)
        data = collect_sources(folder/"sections", snapshot_specs(cards, legacy_inputs()))
        (folder/"capture.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")


if __name__ == "__main__":
    main()
