"""Project one complete historical capture into A, B and C."""
from registry import encode, inventory, matched_key, parse, receipt, sha, summarize


def display_text(claim, value):
    if claim == "top":
        return "공동 1위 " + (", ".join(value) if value else "없음")
    label = {"exists": "적격 후보 있음", "unique": "적격 후보 정확히 하나"}[claim]
    return label + (" · 참" if value else " · 거짓")


def coverage(keys, result, asset, domain, query, rule):
    return {
        "scope": {"domain": domain, "query": query, "edition": asset["edition"]},
        "source_sha256": asset["sha256"],
        "key_sha256": sha(encode(keys)),
        "rule_sha256": sha(encode(rule)),
        "boundary": result["boundary"],
    }


def project(domain, query, asset, raw, rule):
    if sha(raw) != asset["sha256"]:
        raise ValueError("Capture hash differs from the frozen source")
    rows = parse(domain, raw)
    if len(rows) != asset["row_count"]:
        raise ValueError("Capture did not read the full frozen source")
    keys = inventory(rows)
    result = summarize(domain, query, keys, rule)
    witness = None
    if result["top"]:
        chosen = result["top"][0]
        row = rows[chosen]
        witness = receipt(rows, chosen) | {
            "url": f"{asset['url']}#L{row['line']}", "clause": row["clause"],
            "matched_key": matched_key(domain, query, row["key"])[0],
            "reason": "Primary filename matches the requested basename" if domain == "PG"
                      else "Requested country code appears in this row",
        }
    a = {
        "edition": asset["edition"], "source_url": asset["url"], "witness": witness,
        "display": {claim: display_text(claim, result[claim]) for claim in ("exists", "unique", "top")},
    }
    b = a | {"rule": rule, "keys": keys, "coverage": coverage(keys, result, asset, domain, query, rule)}
    c = a | {"rule": rule, "source_raw": raw.decode("utf8"), "source_sha256": asset["sha256"],
             "population_rows": len(rows)}
    return {"A": a, "B": b, "C": c}


def logical_records(view, record):
    # The base including snapshot is one record. B adds rule, receipt and each key.
    # C adds its rule and one full file record with its hash and count.
    return 3 + len(record["keys"]) if view == "B" else {"A": 1, "C": 3}[view]
