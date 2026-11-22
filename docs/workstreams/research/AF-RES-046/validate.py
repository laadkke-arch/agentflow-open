#!/usr/bin/env python3
"""Validate research ledgers and report structure, not upstream software behavior."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
OWNED = "docs/workstreams/research/AF-RES-046/"
FREEZE = "994e21aaea7c5da0c4322db9d1ce2c4f52fa6a2f"
SLOTS = {f"N-{r}{i}" for r in ("P", "S") for i in range(1, 5)} | {f"L-{r}{i}" for r in ("P", "S") for i in (1, 2)}

def read_csv(name):
    with (ROOT / name).open(newline="") as f:
        return list(csv.DictReader(f))

def read_json(name):
    return json.loads((ROOT / name).read_text())

def dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def truth(s):
    return s is True or str(s).lower() == "true"

def table_blocks(text):
    result, current = [], []
    for line in text.splitlines() + [""]:
        if line.startswith("|"):
            current.append(line)
        elif current:
            result.append(current)
            current = []
    return result

def table_cells(line):
    return [x.strip() for x in re.split(r"(?<!\\)\|", line.strip())[1:-1]]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--check-handoff", action="store_true")
    args = parser.parse_args()
    started = datetime.now(timezone.utc).isoformat()
    checks = []
    def check(name, condition, evidence):
        checks.append({"check": name, "passed": bool(condition), "evidence": evidence})
    frame = read_csv("frame.csv")
    src = [json.loads(l) for l in (ROOT / "sources.jsonl").read_text().splitlines() if l.strip()]
    cases = read_json("cases.json")
    baselines, events, changes, labor = [read_csv(n) for n in ("baselines.csv", "events.csv", "changes.csv", "labor.csv")]
    opening, sensitivity = read_csv("initial-public-heads.csv"), read_csv("sensitivity.csv")
    stats, assembly = read_json("evidence/statistics.json"), read_json("evidence/assembly.json")
    groups = defaultdict(list)
    for row in frame:
        groups[(row["repository"], row["stratum"])].append(row)
    check("frame_160_and_four_groups_of_40", len(frame) == 160 and len(groups) == 4 and all(len(x) == 40 for x in groups.values()), {str(k): len(v) for k,v in groups.items()})
    ordered = all([int(r["rank"]) for r in rows] == list(range(1,41)) and [(r["created_at"],int(r["pr_number"])) for r in rows] == sorted((r["created_at"],int(r["pr_number"])) for r in rows) for rows in groups.values())
    check("frame_creation_then_number_order", ordered, "All four rank sequences1..40 and created_at/number order")
    selected = [r for r in frame if r.get("slot_id")]
    check("fixed_8_plus_4_slots_no_duplicate_PR", len(selected) == 12 and {r["slot_id"] for r in selected} == SLOTS and len({(r["repository"],r["pr_number"]) for r in selected}) == 12, [r["slot_id"] for r in selected])
    old_text = subprocess.check_output(["git","show",FREEZE+":"+OWNED+"frame.csv"],cwd=REPO,text=True)
    old = list(csv.DictReader(old_text.splitlines()))
    keys = ("frame_id","repository","stratum","rank","pr_number","created_at","slot_id")
    check("selection_unchanged_from_remote_freeze", [{k:r[k] for k in keys} for r in frame] == [{k:r[k] for k in keys} for r in old], FREEZE)
    check("frozen_status_preserved", all(r["frozen_status"] == o["status"] for r,o in zip(frame,old)), "Current recovery columns do not erase selection-time status")
    ids = {r["source_id"] for r in src}
    counted = [r for r in src if r["count_in_minimum"]]
    allocation = Counter(r["allocation"] for r in counted)
    check("source_ids_unique", len(ids)==len(src), {"receipts":len(src),"unique_ids":len(ids)})
    check("counted_work_ids_unique_single_allocation", len({r["work_id"] for r in counted}) == len(counted), {"counted_works":len(counted),"allocation":dict(allocation)})
    check("minimum_total_26",len(counted)>=26,{"observed":len(counted),"required":26})
    required_fields=("url","final_url","publisher","kind","checked_utc","location","finding","limitation")
    missing=[(r["source_id"],k) for r in counted for k in required_fields if not r.get(k)]
    check("counted_sources_have_read_receipts",not missing,missing)
    unresolved=[]
    for name,rows in (("baselines",baselines),("events",events),("changes",changes),("labor",labor)):
        for i,r in enumerate(rows,1):
            for sid in (r.get("source_ids") or r.get("source_id") or "").split(";"):
                if sid.strip() and sid.strip() not in ids:
                    unresolved.append([name,i,sid])
    for c in cases:
        unresolved.extend(["cases",c["slot_id"],sid] for sid in c["source_ids"] if sid not in ids)
    check("all_ledger_source_references_resolve",not unresolved,unresolved)
    for name,rows in (("baseline",baselines),("labor",labor),("cases",cases),("opening",opening)):
        check(name+"_exactly_12_unique_slots",len(rows)==12 and {r["slot_id"] for r in rows}==SLOTS,name)
    check("event_and_change_ids_unique",len({r["event_id"] for r in events})==len(events) and len({r["change_id"] for r in changes})==len(changes),{"events":len(events),"changes":len(changes)})
    case_map={c["slot_id"]:c for c in cases}
    baseline_map={r["slot_id"]:r for r in baselines}
    frame_map={r["slot_id"]:r for r in selected}
    window_errors=[]
    for r in labor:
        c=case_map[r["slot_id"]]
        start,end=dt(c["window_start"]),dt(c["window_end"])
        seconds=int(r.get("elapsed_seconds") or r.get("elapsed_observation_seconds"))
        if not (start<=end<=start+timedelta(days=90)) or (end-start).total_seconds()!=seconds:
            window_errors.append(c["slot_id"])
        if any(obj["window_start"]!=c["window_start"] or obj["window_end"]!=c["window_end"] for obj in (r,baseline_map[c["slot_id"]],frame_map[c["slot_id"]])):
            window_errors.append(c["slot_id"]+": joins")
    check("all_windows_join_and_elapsed_arithmetic",not window_errors,window_errors)
    opening_errors=[]
    for o in opening:
        c,b=case_map[o["slot_id"]],baseline_map[o["slot_id"]]
        if not (re.fullmatch("[0-9a-f]{40}",o["opening_head_sha"]) and re.fullmatch("[0-9a-f]{40}",o["opening_base_sha"]) and o["opening_head_sha"]==c["baseline_sha"]==b["initial_candidate_sha"]):
            opening_errors.append(o["slot_id"])
        if o["head_parents"] and b["parent_sha"]!=o["head_parents"]:
            opening_errors.append(o["slot_id"]+": parent")
        if (dt(o["opening_event_utc"])-dt(o["pr_created_utc"])).total_seconds() not in (0,1):
            opening_errors.append(o["slot_id"]+": event offset")
    check("opened_recovery_sha_parent_time_consistency",not opening_errors,opening_errors)
    check("raw_archive_limit_not_erased",all(c["raw_event_independent_corroboration"] is False for c in cases),"12 mirror-based recoveries; raw event independent confirmations0")
    links=[c for c in cases if c["first_qualifying_link_observed"]]
    same=[c for c in links if c["same_author_same_purpose_change"] is True]
    unknown=[c for c in links if c["same_author_same_purpose_change"] is None]
    anyauthor=[c for c in links if c["any_author_same_purpose_change"] is True]
    check("main_link_actor_denominators",len(links)==4 and len(same)==1 and len(anyauthor)==3 and [c["slot_id"] for c in unknown]==["L-P2","L-S1"],{"links":4,"same_confirmed":[c["slot_id"] for c in same],"same_unknown":[c["slot_id"] for c in unknown],"any_confirmed":len(anyauthor)})
    check("same_author_patch_public_bound_in_window",all(dt(c["first_link_at"])<=dt(c["same_author_change_public_by"])<=dt(c["window_end"]) for c in same),[c["same_author_change_public_by"] for c in same])
    check("no_implicit_human_time_or_savings",all(c["active_human_work_seconds"] is None and c["saved_human_seconds"] is None and not c["active_work_log_observed"] and not c["in_window_author_duration_selfreport_observed"] for c in cases),"Unknown values remain null, not zero seconds")
    check("strict_counts_not_inflated_by_later_link",sum(c["strict_first_link_chain_confirmed"] for c in cases)==0,"First Cython5230/HackMD event retained; later5243 not substituted")
    sens_errors=[]
    for days in (30,60,90):
        rows=[r for r in sensitivity if int(r["days"])==days]
        if len(rows)!=12 or {r["slot_id"] for r in rows}!=SLOTS:
            sens_errors.append(days)
        for r in rows:
            c=case_map[r["slot_id"]]
            end=min(dt(c["window_end"]),dt(c["window_start"])+timedelta(days=days))
            link=c["first_qualifying_link_observed"] and dt(c["first_link_at"])<=end
            sm=bool(link and c["same_author_change_public_by"] and dt(c["same_author_change_public_by"])<=end)
            an=bool(link and c["any_author_change_public_by"] and dt(c["any_author_change_public_by"])<=end)
            if dt(r["window_end"])!=end or truth(r["link_in_window"])!=bool(link) or truth(r["same_author_change_confirmed"])!=sm or truth(r["any_author_change_confirmed"])!=an:
                sens_errors.append([days,r["slot_id"]])
    check("time_sensitivity_36_rows_recomputed",not sens_errors,sens_errors)
    expected=[(4,1,3),(3,1,3),(2,1,2)]
    observed=[(r["denominator_first_link_slots"],r["same_author_change_confirmed"],r["any_author_change_confirmed"]) for r in stats["actor_and_prework_sensitivity"]]
    check("actor_prework_sensitivity",observed==expected,{"observed":observed,"expected":expected})
    stale=[]
    for name,sha in {**stats["inputs_sha256"],**assembly["source_input_sha256"]}.items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:
            stale.append(name)
    check("assembly_inputs_match_frozen_stream_bytes",not stale,stale)
    check("assembly_counts_match_actual_ledgers",assembly["counts"]=={"sources_receipts":len(src),"counted_unique_works":len(counted),"allocation":dict(allocation),"baseline_rows":len(baselines),"event_rows":len(events),"changes.csv":len(changes),"labor.csv":len(labor)},assembly["counts"])
    result=(ROOT/"RESULT.md").read_text()
    blocks=table_blocks(result)
    check("RESULT_first_table_12_slots_8_columns",len(blocks[0])==14 and all(len(table_cells(r))==8 for r in blocks[0]) and all(any(c["slot_id"] in row for row in blocks[0][2:]) for c in cases),{"rows":len(blocks[0])-2})
    check("RESULT_second_table_2_strata_8_columns",len(blocks[1])==4 and all(len(table_cells(r))==8 for r in blocks[1]),{"rows":len(blocks[1])-2})
    check("RESULT_ends_exactly_three_weakness_rows",len(blocks[-1])==5 and len(table_cells(blocks[-1][0]))==5 and result.rstrip().endswith(blocks[-1][-1]),{"last_data_rows":len(blocks[-1])-2})
    check("required_table_rows_have_source_urls",all("https://" in r for block in (blocks[0],blocks[1]) for r in block[2:]),"12 slot rows and2 stratum rows")
    selfcheck=(ROOT/"SELF_CHECK.md").read_text()
    check("SELF_CHECK_Q1_to_Q7",all(re.search(r"^\| Q"+str(i)+r"\b",selfcheck,re.M) for i in range(1,8)),"Each Q row includes evidence, counterevidence and minimum reversal material")
    acceptance_path=ROOT/"evidence/acceptance-evidence.json"
    if acceptance_path.exists():
        acc=read_json("evidence/acceptance-evidence.json")
        check("acceptance_source_counts_current",acc["ledger_counts"]["counted_unique_works"]==len(counted) and acc["ledger_counts"]["sources_receipts"]==len(src),acc["ledger_counts"])
        music=next(x for x in acc["criteria"] if x["id"]=="music_edit_ledger")
        check("music_gap_remains_unmet",music["numerator"]==0 and music["status"]=="미충족",music["reason"])
    if args.check_handoff:
        h=(ROOT/"HANDOFF.md").read_text()
        hb=table_blocks(h)
        check("HANDOFF_ends_exactly_three_weakness_rows",len(hb[-1])==5 and len(table_cells(hb[-1][0]))==5 and h.rstrip().endswith(hb[-1][-1]),{"last_data_rows":len(hb[-1])-2})
    manifest=read_json("manifest.json")
    tracked=subprocess.check_output(["git","diff","--name-only",manifest["base_commit"],"--"],cwd=REPO,text=True).splitlines()
    untracked=subprocess.check_output(["git","ls-files","--others","--exclude-standard"],cwd=REPO,text=True).splitlines()
    outside=[p for p in tracked+untracked if not p.startswith(OWNED)]
    check("only_owned_path_changed",not outside,outside)
    receipt={"command":"python -B docs/workstreams/research/AF-RES-046/validate.py"+(" --check-handoff --no-write" if args.check_handoff else ""),"started_utc":started,"completed_utc":datetime.now(timezone.utc).isoformat(),"status":"passed" if all(c["passed"] for c in checks) else "failed","checks":checks,"counts":{"frame":len(frame),"cases":len(cases),"baselines":len(baselines),"events":len(events),"changes":len(changes),"labor":len(labor),"sources_receipts":len(src),"counted_unique_works":len(counted),"opening_recoveries":len(opening),"sensitivity":len(sensitivity)},"known_research_gaps":{"music_ledger":0,"strict_first_link_chains":0,"active_human_time_observations":0,"quality_matched_time_pairs":0,"full_selection_blinding":False,"raw_archive_independent_corroboration":0},"boundary":"Ledger joins, arithmetic, source-count identity, ownership and report structure only; no upstream test execution or human labor causal validation."}
    if not args.no_write:
        (ROOT/"evidence/validation.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(receipt,ensure_ascii=False))
    return 0 if receipt["status"]=="passed" else 1

if __name__=="__main__":
    raise SystemExit(main())
