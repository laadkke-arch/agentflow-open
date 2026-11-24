"""Compare current first-author body fingerprints against the frozen 138/142 evidence."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import unicodedata

from capture_frame import get_payload

PIN138 = "198e74358fe2d124c31e16f8bbb93dbbf7ee561d"
PIN142 = "6c379fe049e8e8416c4a42df8dcb9f76de36b684"


def from_git(sha, task, file):
    path = f"docs/workstreams/research/{task}/{file}"
    content = subprocess.check_output(["git", "show", f"{sha}:{path}"])
    return [json.loads(line) for line in content.splitlines()]


def inspect(args):
    row, spans, prior = args
    identifier = row["request_id"] if not prior else "C-" + row["request_id"]
    result = {"event_id": identifier, "url": row["url"], "prior_nfc_sha256": row.get("nfc_sha256")}
    try:
        access, payload = get_payload(row["url"])
        issue = payload["issueViewerRoute"]["data"]["repository"]["issue"]
    except Exception as error:
        return {**result, "access": "failed", "error": str(error), "verified_original": False}
    raw = issue["body"]
    nfc = unicodedata.normalize("NFC", raw)
    lf = nfc.replace("\r\n", "\n").replace("\r", "\n")
    shas = {name: sha256(value.encode()).hexdigest() for name, value in (("raw", raw), ("nfc", nfc), ("nfc_lf", lf))}
    result.update(access="opened", current_sha256=shas, checked_utc=access["checked_utc"],
                  body_version=issue.get("bodyVersion"), source_updated_utc=issue["updatedAt"])
    if prior:
        matches = [mode for mode, digest in shas.items() if digest == row["nfc_sha256"]]
        result.update(matched_modes=matches, verified_original=bool(matches),
                      expected_nfc_codepoints=row["normalized_codepoints"], actual_nfc_codepoints=len(nfc))
        return result
    matches = {}
    for name, body in (("nfc", nfc), ("nfc_lf", lf)):
        units = body.encode("utf-16-le")
        matches[name] = sum(
            units[s["start"]*2:s["end"]*2].decode("utf-16-le", errors="replace") == s["excerpt"] for s in spans
        )
    return {**result, "span_matches": matches, "expected_spans": len(spans), "verified_original": False,
            "limit": "142 does not pin a full body hash in requests.jsonl; span correspondence only"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    corrections = from_git(PIN138, "AF-RES-138", "requests.jsonl")
    requests = from_git(PIN142, "AF-RES-142", "requests.jsonl")
    role_spans = from_git(PIN142, "AF-RES-142", "role_spans.jsonl")
    cases = [(r, [], True) for r in corrections]
    for r in requests:
        spans = [s for s in role_spans if s["request_id"] == r["request_id"] and {"start","end","excerpt"} <= s.keys()]
        cases.append((r, spans, False))
    with ThreadPoolExecutor(max_workers=5) as concurrency:
        result = list(concurrency.map(inspect, cases))
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    for r in result:
        print(r["event_id"], r["access"], r.get("matched_modes", r.get("span_matches")), r.get("expected_spans"))


if __name__ == "__main__":
    main()
