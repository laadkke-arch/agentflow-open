"""Produce a reader packet from shown originals and cards, with no qrel input."""
import argparse
import csv
from pathlib import Path

from search import read_jsonl, write_jsonl


def display_rows(root):
    requests = {r["id"]: r for r in read_jsonl(root / "experiment/inputs/requests.jsonl")}
    events = {r["fetch_id"]: r for r in read_jsonl(root / "fetches.jsonl") if r["cache"] == "cold"}
    docs = {r["candidate_id"]: r for r in read_jsonl(root / "experiment/inputs/documents.jsonl")}
    indexes = {arm: dict(zip(docs, read_jsonl(root / "experiment/inputs" / (arm + ".jsonl"))))
               for arm in "SE"}
    with (root / "ranks.csv").open() as stream:
        ranks = [r for r in csv.DictReader(stream) if r["cache"] == "cold" and r["final_slot"]]
    ranks.sort(key=lambda r: (list(requests).index(r["request_id"]), "LSE".index(r["arm"]),
                              int(r["final_slot"])))
    for r in ranks:
        rid, cid, arm = (r[k] for k in ("request_id", "candidate_id", "arm"))
        doc = docs[cid]
        event = events.get(r["fetch_id"])
        card = indexes.get(arm, {}).get(cid)
        card_text = card["name"] + " " + card["text"] if card else None
        yield {
            "slot_id": f"V-{rid}-{arm}-{r['final_slot']}", "request": requests[rid],
            "rank_id": r["rank_id"], "request_id": rid, "arm": arm, "slot": int(r["final_slot"]),
            "candidate_id": cid, "edition": doc["edition"], "url": doc["url"],
            "source_http_url": event["arrival_url"] if event else None,
            "fetch_id": r["fetch_id"], "opening_step": int(r["opened_step"]) if r["opened_step"] else None,
            "exposure": event["kind"] if event else "card_only" if card_text else "none",
            "card_text": card_text, "view": event["view"] if event else None,
            "display_sha256": event["display_sha256"] if event else None,
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    write_jsonl(args.output, display_rows(args.root))
