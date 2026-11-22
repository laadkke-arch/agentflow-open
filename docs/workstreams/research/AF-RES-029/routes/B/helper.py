"""B-route receipt and one-shot serialization helper. No network or cross-route reads."""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

OWNED = Path(__file__).resolve().parent
ROOT = OWNED.parent.parent
sys.path.insert(0, str(ROOT))
from protocol import write_return

def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"

def main():
    q = sys.argv[1]
    if len(q) != 3 or q[0] != "Q" or not q[1:].isdigit():
        raise ValueError("question id")
    dest = OWNED / q
    bundle = json.loads((dest / "bundle.json").read_text())
    packet, route = bundle["packet"], bundle["route"]
    if packet["question_id"] != q or packet["route"] != "B":
        raise ValueError("identity")
    receipts = []
    for name in route.get("request_receipts", []):
        p = (dest / name).resolve()
        if not p.is_relative_to(dest.resolve()):
            raise ValueError("receipt outside question")
        receipts.append(json.loads(p.read_text()))
    nav = sum(r["budget_debit"]["navigation"] for r in receipts)
    body = sum(r["budget_debit"]["body_opens"] for r in receipts)
    if (nav, body) != (packet["budget"]["navigation"], packet["budget"]["body_opens"]):
        raise ValueError("receipt budget mismatch")
    for filename in ("route.json", "sources.jsonl", "exposures.jsonl", "return.json"):
        if (dest / filename).exists():
            raise ValueError("sealed artifact already exists: " + filename)
    try:
        digest = write_return(dest / "return.json", packet)
    except Exception as err:
        with (dest / "gate-rejections.jsonl").open("a") as f:
            f.write(json.dumps({"checked_utc": datetime.now(timezone.utc).isoformat(), "error": repr(err), "original_attempt": "bundle.json"}, ensure_ascii=False)+"\n")
        raise
    route["return_sha256"] = digest
    route["validated_budget"] = {"navigation": nav, "body_opens": body}
    route["serialization_gate"] = packet["serialization_gate"]
    route["finalized_utc"] = datetime.now(timezone.utc).isoformat()
    (dest / "route.json").write_text(dump(route))
    for key, filename in (("sources", "sources.jsonl"), ("exposures", "exposures.jsonl")):
        (dest / filename).write_text("".join(json.dumps(v, ensure_ascii=False)+"\n" for v in bundle[key]))
    print(json.dumps({"question_id": q, "route": "B", "navigation": nav, "body_opens": body, "candidates": len(packet["candidates"]), "document_urls": packet["serialization_gate"]["url_count"], "return_sha256": digest, "path": str(dest), "started_utc": packet["started_utc"], "ended_utc": packet["ended_utc"]}))

if __name__ == "__main__":
    main()

