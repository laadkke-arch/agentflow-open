"""Read exactly one view and request only the declared old/current routes."""
import json
import sys

from registry import (CLAIMS, ENTRYPOINTS, VIEWS, check_rule, encode, inventory,
                      matched_key, parse, receipt, sha, summarize)

REQUEST_KEYS = {"domain", "query", "claim", "view", "record", "entrypoint"}
BASE_KEYS = {"edition", "source_url", "witness", "display"}
EXTRA_KEYS = {
    "A": set(),
    "B": {"rule", "keys", "coverage"},
    "C": {"rule", "source_raw", "source_sha256", "population_rows"},
}
WITNESS_KEYS = {"id", "line", "clause_sha256", "url", "clause", "matched_key", "reason"}
RECOVERABLE = (KeyError, ValueError, SyntaxError, TypeError, AttributeError)


def reject_extra(request):
    if set(request) != REQUEST_KEYS:
        raise ValueError("unexpected request field")
    domain, claim, view = request["domain"], request["claim"], request["view"]
    if claim not in CLAIMS or view not in VIEWS or request["entrypoint"] != ENTRYPOINTS.get(domain):
        raise ValueError("unexpected claim, view or entrypoint")
    record = request["record"]
    if not BASE_KEYS <= set(record) <= BASE_KEYS | EXTRA_KEYS[view]:
        raise ValueError("unexpected projection field")
    if set(record["display"]) != set(CLAIMS):
        raise ValueError("unexpected display field")
    witness = record["witness"]
    if witness is not None and set(witness) != WITNESS_KEYS:
        raise ValueError("unexpected witness field")


def verified_witness(domain, query, present):
    if present is None:
        return None
    clause = present["clause"]
    if sha(clause.encode()) != present["clause_sha256"]:
        raise ValueError("witness digest mismatch")
    if domain == "PG":
        clause = "LEXERS = {\n" + clause + "\n}\n"
    rows = parse(domain, clause.encode())
    row, = rows
    if row != present["id"] or present["matched_key"] not in matched_key(domain, query, rows[row]["key"]):
        raise ValueError("recorded clause no longer establishes eligibility")
    return {
        "id": row, "line": present["line"], "clause_sha256": present["clause_sha256"],
    }


def projected_keys(domain, query, record):
    rule = record.get("rule")
    check_rule(domain, rule)
    keys = record["keys"]
    names = [row_id for row_id, key in keys if isinstance(key, list)]
    if names != sorted(set(names)) or len(names) != len(keys):
        raise ValueError("invalid or duplicated per-candidate key")
    computed = summarize(domain, query, keys, rule)
    claim = record["coverage"]
    if (claim["scope"] != {"domain": domain, "query": query, "edition": record["edition"]}
            or claim["key_sha256"] != sha(encode(keys))
            or claim["rule_sha256"] != sha(encode(rule))
            or claim["boundary"] != computed["boundary"]):
        raise ValueError("coverage receipt does not match the stored keys or scope")
    support = {"asset_sha256": claim["source_sha256"], "key_sha256": claim["key_sha256"],
               "boundary": computed["boundary"], "witness": verified_witness(domain, query, record["witness"])}
    if support["witness"] and support["witness"]["id"] not in dict(computed["eligible"]):
        raise ValueError("witness absent from eligible key set")
    return computed, support


def whole_registry(domain, query, raw, wanted_sha, wanted_rows, rule):
    check_rule(domain, rule)
    data = raw.encode()
    if sha(data) != wanted_sha:
        raise ValueError("full registry digest mismatch")
    rows = parse(domain, data)
    if len(rows) != wanted_rows:
        raise ValueError("full registry row count mismatch")
    computed = summarize(domain, query, inventory(rows), rule)
    top = computed["top"]
    support = {
        "asset_sha256": wanted_sha, "boundary": computed["boundary"],
        "witness": receipt(rows, top[0]) if top else None,
    }
    return computed, support


def resolve(request, send, slot, phase):
    response = send({"entrypoint": request["entrypoint"], "slot": slot, "phase": phase,
                     "revision": request["record"]["edition"] if slot == "historical" else None})
    if response["status"] != "available":
        raise ValueError(response["status"])
    if slot == "historical" and response["edition"] != request["record"]["edition"]:
        raise ValueError("archive returned a different edition")
    return whole_registry(request["domain"], request["query"], response["raw"], response["sha256"],
                          response["rows"], response["rule"])


def resolved(value, method, evidence, notes):
    return {"status": "resolved", "value": value, "method": method,
            "evidence": evidence, "notes": notes}


def deferred(notes):
    return {"status": "deferred", "value": None, "method": None, "evidence": None, "notes": notes}


def historical(request, send):
    domain, query = request["domain"], request["query"]
    record, view, claim = request["record"], request["view"], request["claim"]
    notes = []
    try:
        if view == "A" and claim == "exists":
            witness = verified_witness(domain, query, record["witness"])
            if witness:
                return resolved(True, "one_verified_clause", {"witness": witness}, notes)
        if view == "B":
            calculated, support = projected_keys(domain, query, record)
            return resolved(calculated[claim], "inventory_keys", support, notes)
        if view == "C":
            calculated, support = whole_registry(domain, query, record["source_raw"],
                                                  record["source_sha256"], record["population_rows"],
                                                  record.get("rule"))
            return resolved(calculated[claim], "local_full_registry", support, notes)
        notes.append("view lacks evidence for this quantified claim")
    except RECOVERABLE as error:
        notes.append(str(error))
    for phase in ("initial", "post_defer"):
        try:
            value, support = resolve(request, send, "historical", phase)
            return resolved(value[claim], "historical_archive", support, notes)
        except RECOVERABLE as error:
            notes.append(f"{phase}: {error}")
    return deferred(notes)


def evaluate(request, send):
    reject_extra(request)
    claim = request["claim"]
    # Display the opaque stored text in its own field. The two solvers do not consume it.
    shown = request["record"]["display"][claim]
    old = historical(request, send)
    try:
        value, support = resolve(request, send, "current", "initial")
        current = resolved(value[claim], "current_route", support, [])
    except RECOVERABLE as error:
        current = deferred([str(error)])
    return {"display": shown, "historical": old, "current": current}


def publish(key, value):
    print(encode({key: value}).decode(), flush=True)


def send(event):
    publish("read", event)
    return json.loads(sys.stdin.readline())


if __name__ == "__main__":
    try:
        publish("decision", evaluate(json.loads(sys.stdin.readline()), send))
    except RECOVERABLE as exc:
        publish("error", str(exc))
        sys.exit(2)
