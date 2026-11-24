"""Run AF-RES-146 from pinned inputs in one new directory. No grading is done by the replay."""
import argparse
from collections import Counter
import csv
from datetime import UTC, datetime
import json
from pathlib import Path
import platform
import sqlite3
from time import perf_counter_ns, process_time_ns

from inputs import ROOT, collect_sources, digest, legacy_inputs, rank_new, read_csv, read_jsonl, snapshot_specs
from prototype import run as run_prototype

ELIGIBLE = {"direct", "partial"}
POLICIES = {
    "cap3": (3, False, False), "cap8": (8, False, False),
    "sequential8": (8, True, False), "zero_fill8": (8, False, True),
}
SCHEMA = """
CREATE TABLE rank_before_cut (
  cohort TEXT, policy_group TEXT, event_id TEXT, card_id TEXT, rank INT, score INT, matched TEXT,
  PRIMARY KEY(cohort, policy_group, event_id,card_id)
);
CREATE TABLE shortlisted (
  cohort TEXT, policy_group TEXT, event_id TEXT, policy TEXT, card_id TEXT, rank INT,
  PRIMARY KEY(cohort, policy_group, event_id,policy,card_id)
);
CREATE TABLE reviewed (
  cohort TEXT, policy_group TEXT, event_id TEXT, policy TEXT, card_id TEXT, rank INT,
  verdict TEXT, section_sha256 TEXT, section_kind TEXT, evidence_source TEXT,
  PRIMARY KEY(cohort, policy_group, event_id,policy,card_id)
);
CREATE TABLE displayed (
  cohort TEXT, policy_group TEXT, event_id TEXT, policy TEXT, slot INT, card_id TEXT, reason TEXT,
  PRIMARY KEY(cohort, policy_group, event_id,policy,slot)
);
"""
STAGE_FIELDS = (
    "cohort","layer","policy_group","event_id","policy","stage","card_id","rank","score","matched",
    "cut_rank","review_rank","review_grade","source_kind","source_id","source_url","section_sha256",
    "display_slot","state","reason","condition",
)
COST_FIELDS = (
    "run","cohort","policy_group","event_id","policy","pass_kind","stop_reason","shortlisted","compared",
    "actual_file_opens","source_text_opens","reading_note_opens","bytes_read","source_text_bytes","reading_note_bytes",
    "cache_hits","hits_source_text","hits_reading_note","process_cpu_ns","wall_ns","direct","partial","conflict_reviewed",
    "unconfirmed_reviewed","conflict_displayed","vacancies","basis",
)
JOIN_FIELDS = (
    "cohort","policy_group","event_id","card_id","initial_rank","score","inspected_3","inspected_8",
    "display_3","display_8","entered_link","displaced_link","effect","new_grade","source_id","source_url","condition",
    "vacancies_3","vacancies_8",
)


class SectionStore:
    def __init__(self, path, sections):
        self.path = path
        self.sections = sections
        self.cache = {}

    def read(self, card_id, expected_sha, operations):
        info = self.sections[card_id]
        key, kind = info["sha256"], info["kind"]
        assert key == expected_sha, (card_id, key, expected_sha)
        if key in self.cache:
            operations["cache_hits"] += 1
            operations["hits_source_text" if kind == "git_source_lines" else "hits_reading_note"] += 1
            return info
        data = (self.path / info["file"]).read_bytes()
        assert len(data) == info["bytes"] and digest(data) == key
        self.cache[key] = data
        operations["actual_file_opens"] += 1
        operations["bytes_read"] += len(data)
        if kind == "git_source_lines":
            operations["source_text_opens"] += 1
            operations["source_text_bytes"] += len(data)
        else:
            operations["reading_note_opens"] += 1
            operations["reading_note_bytes"] += len(data)
        return info


def calculate(ranks, policy, gate, store):
    t0, c0 = perf_counter_ns(), process_time_ns()
    depth, stop_when_full, fill_zero = POLICIES[policy]
    shortlist = [row for row in ranks if row["score"] or fill_zero][:depth]
    operations = Counter()
    reviews, shown = {}, []
    stop = "positive_exhausted" if len(shortlist) < depth else "depth_cap_reached"
    for row in shortlist:
        cid = row["card_id"]
        entry = gate[cid]
        info = store.read(cid, entry["sha256"], operations)
        reviews[cid] = {**entry, "kind": info["kind"]}
        if entry["grade"] in ELIGIBLE and len(shown) < 3:
            shown.append(cid)
        if stop_when_full and len(shown) == 3:
            stop = "three_eligible_slots_filled"
            break
    measures = {name: operations[name] for name in COST_FIELDS[9:18]}
    grade_counts = Counter(row["grade"] for row in reviews.values())
    display_counts = Counter(reviews[c]["grade"] for c in shown)
    measures.update(stop_reason=stop, shortlisted=len(shortlist), compared=len(reviews),
                    process_cpu_ns=process_time_ns()-c0, wall_ns=perf_counter_ns()-t0,
                    direct=display_counts["direct"], partial=display_counts["partial"],
                    conflict_reviewed=grade_counts["conflict"], unconfirmed_reviewed=grade_counts["unconfirmed"],
                    conflict_displayed=display_counts["conflict"], vacancies=3-len(shown),
                    basis="local source section or preserved reading note, plus frozen gate lookup")
    assert measures["compared"] == measures["actual_file_opens"] + measures["cache_hits"]
    assert measures["direct"] + measures["partial"] + measures["vacancies"] == 3
    return [row["card_id"] for row in shortlist], reviews, shown, measures


def record(db, stages, cohort, group, layer, event, policy, ranks, result, references):
    base = {"cohort":cohort,"policy_group":group,"event_id":event,"policy":policy,"layer":layer}
    key = (cohort,group,event)
    cut, reviews, shown, cost = result
    db.executemany("INSERT INTO shortlisted VALUES (?,?,?,?,?,?)",
                   [(*key,policy,cid,i) for i,cid in enumerate(cut,1)])
    for row in ranks:
        cid = row["card_id"]
        reference = references[cid]
        verdict = reviews.get(cid)
        state = ("reviewed" if verdict else "stopped_at_three" if cid in cut else
                 "zero_score" if row["score"] == 0 else "depth_excluded")
        stage_row = {**base, "card_id":cid, "rank":row["rank"], "score":row["score"], "matched":row["hits"], "stage":"candidate", "state":state, "source_id":reference["source_id"],
                     "source_url":reference["url"], "cut_rank":cut.index(cid)+1 if cid in cut else "",
                     "display_slot":shown.index(cid)+1 if cid in shown else ""}
        if verdict:
            db.execute("INSERT INTO reviewed VALUES (?,?,?,?,?,?,?,?,?,?)",
                       (*key,policy,cid,row["rank"],verdict["grade"],verdict["sha256"],verdict["kind"],verdict["source_id"]))
            stage_row.update(review_rank=row["rank"], review_grade=verdict["grade"], source_kind=verdict["kind"],
                             section_sha256=verdict["sha256"], reason=verdict["reason"], condition=verdict["condition"])
        stages.append(stage_row)
    for i in range(1,4):
        card = shown[i-1] if i <= len(shown) else None
        reason = reviews[card]["grade"] if card else cost["stop_reason"] + ": insufficient eligible candidates"
        db.execute("INSERT INTO displayed VALUES (?,?,?,?,?,?,?)", (*key,policy,i,card,reason))
        stages.append({**base,"stage":"display_slot","card_id":card or "","display_slot":i,
                       "state":"displayed" if card else "vacant","reason":reason})


def transitions(cohort, group, event, ranks, result3, result8, references):
    cut3, reviews3, shown3, _ = result3
    cut8, reviews8, shown8, _ = result8
    assert cut8[:len(cut3)] == cut3
    assert list(reviews8)[:len(reviews3)] == list(reviews3)
    assert shown8[:len(shown3)] == shown3
    prefix_held = {r["card_id"]:r for r in ranks}
    changed = [c for c in reviews8 if c not in reviews3]
    rows = []
    for cid in changed or [""]:
        verdict = reviews8.get(cid,{})
        reference = references.get(cid,{})
        rows.append(dict(cohort=cohort,policy_group=group,event_id=event,card_id=cid,
                         initial_rank=prefix_held.get(cid,{}).get("rank"),score=prefix_held.get(cid,{}).get("score"),
                         inspected_3=int(cid in reviews3),inspected_8=int(cid in reviews8),display_3=int(cid in shown3),
                         display_8=int(cid in shown8),entered_link=reference.get("url","") if cid in shown8 else "",
                         displaced_link="",effect="fills_vacancy" if cid in shown8 else "new_review_held" if cid else "no_new_review",
                         new_grade=verdict.get("grade",""),source_id=reference.get("source_id",""),
                         source_url=reference.get("url",""),condition=verdict.get("condition",""),
                         vacancies_3=3-len(shown3),vacancies_8=3-len(shown8)))
    return rows


def prototype_stages(payload):
    for case in payload["cases"]:
        answer = case["answer"]
        cut = [row["item_id"] for row in answer["catalog_shortlist"]]
        contextual = {r["id"]:r for r in case["trace"] if r["stage"]=="fixture_inspection"}
        shown = {row["catalog_item"]:row for row in answer["answers"]}
        base = dict(cohort="prototype",layer="synthetic_calibration" if case["synthetic_only"] else "calibration",
                    policy_group="unmodified",event_id=case["case"],policy=f"budget{case['display_budget']}")
        for rank, row in enumerate(case["matching_catalog"],1):
            cid = row["item_id"]
            item = contextual.get(cid)
            status = shown[cid]["status"] if cid in shown else ""
            yield {**base,"stage":"candidate","card_id":cid,"rank":rank,
                   "score":f"{len(row['matched_operations'])} op / {len(row['matched_terms'])} terms",
                   "cut_rank":cut.index(cid)+1 if cid in cut else "","review_rank":rank if item and item["context"] else "",
                   "review_grade":status,"source_kind":"prototype curated note" if status else "",
                   "source_url":row["url"],"display_slot":list(shown).index(cid)+1 if cid in shown else "",
                   "state":"reviewed" if status else "no_fixture_handler" if item else "depth_excluded"}
        for slot in range(1,case["display_budget"]+1):
            item = list(shown)[slot-1] if slot <= len(shown) else ""
            yield {**base,"stage":"display_slot","card_id":item,"display_slot":slot,"state":"displayed" if item else "vacant"}


def put_csv(path, fields, rows):
    with path.open("w",encoding="utf-8",newline="") as file:
        writer = csv.DictWriter(file,fieldnames=fields,lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def put_json(path, data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2) + "\n",encoding="utf-8")


def run(output):
    started = datetime.now(UTC).isoformat(timespec="milliseconds")
    output.mkdir(parents=True)
    local_files = ("inventory.jsonl","requests.jsonl","replay/gate-new.csv","replay/gate-legacy.csv",
                   "replay/inputs.py","replay/prototype.py","replay/run.py")
    data = {f:(ROOT/f).read_bytes() for f in local_files}
    cards = read_jsonl(data["inventory.jsonl"])
    requests = read_jsonl(data["requests.jsonl"])
    t0,c0=perf_counter_ns(),process_time_ns()
    legacy = legacy_inputs()
    legacy_arithmetic = {"wall_ns":perf_counter_ns()-t0,"process_cpu_ns":process_time_ns()-c0,
                         "input_bytes":sum(map(len,legacy["material"].values())),"source_document_opens":0,
                         "input_files":len(legacy["material"]),"display_slots":132,"vacancies":131,
                         "judgment_pairs":242,"prior_investigations_logical":89}
    t0,c0=perf_counter_ns(),process_time_ns()
    new = rank_new(cards,requests)
    rank_cost = {"wall_ns":perf_counter_ns()-t0,"process_cpu_ns":process_time_ns()-c0,"candidates":48}
    sections_path = output/"sections"
    captured = collect_sources(sections_path,snapshot_specs(cards,legacy))
    sealed_sections = json.loads((ROOT/"evidence/gate-capture.json").read_bytes())["sections"]
    assert captured["sections"] == sealed_sections
    provider_refs = {c["card_id"]:c for c in cards}
    old_refs = {k:dict(url=v["clause_url"],source_id=v["source_id"]) for k,v in legacy["cards"].items()}
    sources = {"new":provider_refs,"legacy142":old_refs}
    gates = {}
    for cohort,name in (("new","replay/gate-new.csv"),("legacy142","replay/gate-legacy.csv")):
        for row in read_csv(data[name]):
            gates.setdefault((cohort,row["event_id"]),{})[row["card_id"]] = row
    work = {"new": {
        "fixed12": {e:("new_public",r) for e,r in new.items()}},
        "legacy142": {g:{e:(legacy["cases"][e],r) for (k,e),r in legacy["ranks"].items() if k==g}
                      for g in ("K22/L","K16/L","K22/R","K16/R")}}
    stages, costs, changes, cut_results = [], [], [], {}
    with sqlite3.connect(output/"stages.sqlite") as db:
        db.executescript(SCHEMA)
        for cohort, policy_groups in work.items():
            for group, events in policy_groups.items():
                for event, (_, ranks) in events.items():
                    db.executemany("INSERT INTO rank_before_cut VALUES (?,?,?,?,?,?,?)",
                                   [(cohort,group,event,r["card_id"],r["rank"],r["score"],r["hits"]) for r in ranks])
                test_policies = ["cap3","cap8"]
                if group in ("K22/L","fixed12"):
                    test_policies.append("sequential8")
                if cohort == "new":
                    test_policies.append("zero_fill8")
                for policy in test_policies:
                    store = SectionStore(sections_path,captured["sections"])
                    for pass_kind in ("cache_empty_at_policy_start","same_order_repeat"):
                        for event, (layer, ranks) in events.items():
                            gate = gates.get((cohort,event),{})
                            result = calculate(ranks,policy,gate,store)
                            address = (cohort,group,event,policy)
                            costs.append(dict(run=output.name,cohort=cohort,policy_group=group,event_id=event,policy=policy,
                                              pass_kind=pass_kind,**result[3]))
                            if pass_kind=="cache_empty_at_policy_start":
                                cut_results[address] = result
                                record(db,stages,cohort,group,layer,event,policy,ranks,result,sources[cohort])
                            else:
                                assert result[:3] == cut_results[address][:3]
                                assert result[3]["actual_file_opens"] == 0
                for event, (_, ranks) in events.items():
                    addr = (cohort,group,event)
                    short, deep = (cut_results[(*addr,policy)] for policy in ("cap3","cap8"))
                    changes.extend(transitions(*addr,ranks,short,deep,sources[cohort]))
                    if "sequential8" in test_policies:
                        sequential = cut_results[(*addr,"sequential8")]
                        assert deep[2] == sequential[2]
        assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        counts = {table: db.execute("SELECT COUNT(*) FROM "+table).fetchone()[0]
                  for table in ("rank_before_cut","shortlisted","reviewed","displayed")}

    prior_grades = Counter(row["grade"] for row in legacy["truth"].values())
    gate_sensitivity = {"grade_counts":dict(prior_grades),"demote_two_direct_grade_counts":{
        **prior_grades,"direct":0,"partial":prior_grades["partial"]+prior_grades["direct"]}}
    for policy in ("cap3","cap8"):
        ascertained = [(event, cid) for event in legacy["cases"]
                       for cid in cut_results[("legacy142","K22/L",event,policy)][2]]
        gate_sensitivity[policy] = {
            "labels":dict(Counter(legacy["truth"][pair]["grade"] for pair in ascertained)),
            "demote_two_direct":dict(Counter("partial" if legacy["truth"][pair]["grade"]=="direct"
                                             else legacy["truth"][pair]["grade"] for pair in ascertained)),
            "whole_request_gate_vacancies":33,
        }
    prototype = run_prototype(output)
    stages.extend(prototype_stages(prototype))
    for case in prototype["cases"]:
        answer = case["answer"]
        reviewed = sum(row["stage"]=="fixture_inspection" and row["context"] is not None for row in case["trace"])
        costs.append(dict(run=output.name,cohort="prototype",policy_group="unmodified",
                          event_id=case["case"],policy=f"budget{case['display_budget']}",pass_kind="offline_fixture",
                          shortlisted=len(answer["catalog_shortlist"]),compared=reviewed,
                          stop_reason="returned_by_fixture",actual_file_opens=0,
                          vacancies=case["display_budget"]-len(answer["answers"]),
                          basis=f"source captures already authored in code; {case['persisted_source_note_bytes']} bytes in SQLite"))
    data_table_row = dict(run=output.name,cohort="legacy142",policy_group="pinned_tables",event_id="all",
                          policy="table_recount",pass_kind="table_only",actual_file_opens=0,compared=0,
                          bytes_read=legacy_arithmetic["input_bytes"],process_cpu_ns=legacy_arithmetic["process_cpu_ns"],
                          wall_ns=legacy_arithmetic["wall_ns"],vacancies=131,basis="7 tabular inputs, zero provider document opens")
    costs.append(data_table_row)
    put_csv(output/"stages.csv",STAGE_FIELDS,stages)
    put_csv(output/"costs.csv",COST_FIELDS,costs)
    put_csv(output/"transitions.csv",JOIN_FIELDS,changes)
    put_json(output/"prototype.json",prototype)
    put_json(output/"source-capture.json",captured)
    fingerprints = {"local:"+name:digest(body) for name,body in data.items()}
    fingerprints.update({"git:"+name:digest(body) for name,body in legacy["material"].items()})
    fingerprints.update({"section:"+name:r["sha256"] for name,r in captured["sections"].items()})
    fingerprints.update({"prototype:"+name:sha for name,sha in prototype["source_file_sha256"].items()})
    result_files = {f:digest((output/f).read_bytes()) for f in ("stages.csv","transitions.csv","prototype.json")}
    payload = {"environment":{"python":platform.python_version(),"sqlite":sqlite3.sqlite_version,
                              "platform":platform.platform()},"started_utc":started,
               "completed_utc":datetime.now(UTC).isoformat(timespec="milliseconds"),
               "input_fingerprints":fingerprints,"input_sha256":digest(json.dumps(fingerprints,sort_keys=True).encode()),
               "result_sha256":result_files,"counts":counts,"stage_rows":len(stages),"cost_rows":len(costs),
               "legacy":legacy_arithmetic,"legacy_alternative":gate_sensitivity,"new_ranking_cost":rank_cost,
               "assertions":{"prefix_within_each_cut":True,"display_prefix_preserved":True,
                             "sequential_equals_fixed_display":True,"cache_repeat_zero_opens":True,
                             "three_slots_per_research_event_policy":True,"sqlite_integrity":"ok"},
               "timing_limit":"Process CPU, wall and local file opens; excludes human reading and case recruitment. "
                              "Policy cache at start is empty, operating-system cache is not cleared."}
    put_json(output/"run-receipt.json",payload)
    print(json.dumps({k:payload[k] for k in ("input_sha256","result_sha256","counts","stage_rows","cost_rows")},indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    options = parser.parse_args()
    run(options.output.resolve())


if __name__ == "__main__":
    main()
