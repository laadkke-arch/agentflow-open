"""Merge and validate raw card observations without consulting the answer key."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READ_FIELDS = "read_id judgment_id card_id case_id task ordinal mode requested_url resolved_url parent_read_id href_raw href_evidence outcome observed_edition locator observed_fact checked_utc tool_ref budget_counted diagnostic_only".split()
JUDGMENT_FIELDS = "judgment_id card_id case_id task reader_id order_index key_exposure prior_card_exposure visible_cues read_ids publisher_opens local_x_displayed action historical_level observed_edition observed_locator observed_claim consumer_edition_confirmed support_state hold_reason rationale confidence diagnostic_only".split()


def jl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def scalar(value):
    if isinstance(value, (dict, list, bool)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    if value is None or value == "":
        return "미확인"
    return value


def dump_csv(path, rows, core):
    keys = core + sorted(set().union(*(set(row) for row in rows)) - set(core))
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=keys, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: scalar(row.get(k, "미확인")) for k in keys})


def main():
    cards = {r["card_id"]: r for r in jl(ROOT / "cards.jsonl")}
    readings, judgments, file_hashes = [], [], {}
    for reader in ("reader_a", "reader_b", "reader_c"):
        folder = ROOT / "readers" / reader
        for name, dest in (("reads.jsonl", readings), ("judgments.jsonl", judgments)):
            path = folder / name
            file_hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
            dest.extend(jl(path))
    issues, notes = [], []

    def require(condition, msg):
        if not condition:
            issues.append(msg)

    require(len(cards) == 32, "card_count_not_32")
    require(len(judgments) == 64, "judgment_count_not_64")
    require(len({r["judgment_id"] for r in judgments}) == len(judgments), "duplicate_judgment_id")
    require(len({r["read_id"] for r in readings}) == len(readings), "duplicate_read_id")
    require(Counter((r["card_id"], r["task"]) for r in judgments) == Counter((c, t) for c in cards for t in ("C", "H")), "card_task_linkage_mismatch")
    by_read = {r["read_id"]: r for r in readings}
    by_judgment = {r["judgment_id"]: r for r in judgments}
    for r in readings:
        require(not (set(READ_FIELDS) - set(r)), f"read_missing_fields:{r['read_id']}:{sorted(set(READ_FIELDS)-set(r))}")
        require(r["judgment_id"] in by_judgment, f"read_orphan:{r['read_id']}")
        require(r["mode"] in ("publisher_open", "local_X", "same_document_find"), f"read_bad_mode:{r['read_id']}")
        require(bool(r["budget_counted"]) == (r["mode"] == "publisher_open"), f"budget_flag:{r['read_id']}")
    for j in judgments:
        jid = j["judgment_id"]
        require(not (set(JUDGMENT_FIELDS) - set(j)), f"judgment_missing_fields:{jid}:{sorted(set(JUDGMENT_FIELDS)-set(j))}")
        c = cards[j["card_id"]]
        require(j["case_id"] == c["case_id"], f"case_link:{jid}")
        require(j["key_exposure"] == "none", f"key_exposure:{jid}")
        rs = [r for r in readings if r["judgment_id"] == jid]
        require(set(j["read_ids"]) == {r["read_id"] for r in rs}, f"read_ids_link:{jid}")
        opens = [r for r in rs if r["mode"] == "publisher_open"]
        require(len(opens) <= 2, f"open_budget_exceeded:{jid}")
        require(j["publisher_opens"] == len(opens), f"open_count_mismatch:{jid}")
        if opens:
            first = opens[0]
            visible = re.findall(r"https?://\S+", c["body"])
            require(first["requested_url"] in visible, f"first_not_card_visible:{jid}:{first['requested_url']}")
            if len(opens) == 2:
                second = opens[1]
                require(second["parent_read_id"] == first["read_id"], f"second_parent_mismatch:{jid}")
                require(second["href_raw"] not in ("미확인", "", None), f"second_href_missing:{jid}")
                require(second["href_evidence"] not in ("미확인", "", None, "card-visible"), f"second_href_evidence_missing:{jid}")
        if j["local_x_displayed"]:
            require("X" in c["elements"], f"x_not_in_card:{jid}")
            require(any(r["mode"] == "local_X" for r in rs), f"x_display_not_logged:{jid}")
    for case_id in sorted({c["case_id"] for c in cards.values()}):
        expected = [(c["card_id"], t) for c in sorted(cards.values(), key=lambda x:x["presentation_index"]) if c["case_id"] == case_id for t in c["task_order"]]
        actual = [(j["card_id"],j["task"]) for j in judgments if j["case_id"] == case_id]
        require(actual == expected, f"case_order_mismatch:{case_id}")
    # The global presentation_index is a protocol order, not a claim of serial wall-clock execution.
    judgments.sort(key=lambda j:(cards[j["card_id"]]["presentation_index"], cards[j["card_id"]]["task_order"].index(j["task"])))
    jindex = {j["judgment_id"]:i for i,j in enumerate(judgments)}
    readings.sort(key=lambda r:(jindex.get(r["judgment_id"],999),r["ordinal"]))
    dump_csv(ROOT / "reads.csv", readings, READ_FIELDS)
    dump_csv(ROOT / "judgments.csv", judgments, JUDGMENT_FIELDS)
    for name in ("reads.csv", "judgments.csv", "cards.jsonl"):
        file_hashes[name] = hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    record = {
        "phase":3,"created_utc":datetime.now(timezone.utc).isoformat(),
        "answer_key_consulted_by_this_script":False,
        "cards":len(cards),"judgments":len(judgments),"read_events":len(readings),
        "publisher_opens":sum(r["mode"] == "publisher_open" for r in readings),
        "local_x_events":sum(r["mode"] == "local_X" for r in readings),
        "by_reader":dict(Counter(j["reader_id"] for j in judgments)),
        "issues":issues,"structural_checks_met":not issues,"file_sha256":file_hashes,
        "manual_followup":"Actual second-href text, substantive evidence and time order require review; this structural audit does not assert substantive correctness.",
        "notes":notes,
    }
    (ROOT / "evidence/read-seal.json").write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:record[k] for k in ("cards","judgments","read_events","publisher_opens","local_x_events","by_reader","issues","structural_checks_met")},ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
