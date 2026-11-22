#!/usr/bin/env python3
"""Acceptance structure and independent ledger reconciliation; no external runs."""
import collections
import csv
import datetime
import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
OWNED = "docs/workstreams/research/AF-RES-037/"


def load(path):
    return json.loads((ROOT/path).read_text())


def rows(path):
    with (ROOT/path).open(newline="") as f:
        return list(csv.DictReader(f))


checks = []
def check(name, condition, actual):
    checks.append({"name":name,"passed":bool(condition),"actual":actual})
    if not condition:
        raise AssertionError((name,actual))


required = ["manifest.json","SCOPE.md","sources.jsonl","frame.csv","chains.csv","judgments.csv","cards.md","RESULT.md","SELF_CHECK.md","evidence/acceptance-evidence.json"]
check("pre_handoff_required_files",all((ROOT/f).is_file() and (ROOT/f).stat().st_size for f in required),required)
sources = [json.loads(l) for l in (ROOT/"sources.jsonl").read_text().splitlines()]
source_ids = {r["source_id"] for r in sources}
required_keys = set("source_id original_url pinned_url_or_version publisher published_or_event_date checked_utc locator source_kind verified_fact limitation question_ids case_ids duplicate_group counted".split())
check("all_source_keys",all(required_keys <= r.keys() for r in sources),len(sources))
check("unique_source_ids",len(source_ids)==len(sources),len(source_ids))
counted = [r for r in sources if r["counted"]]
groups = collections.Counter(r["duplicate_group"].casefold() for r in counted)
check("one_counted_representative_per_work",max(groups.values())==1,dict(groups))
cats = collections.Counter(r["count_category"] for r in counted)
minimums = {"A_initial":8,"donor_rule_or_design":6,"recipient_followup":6,"independent_counterrecord":4}
check("category_minimums",all(cats[k]>=n for k,n in minimums.items()) and len(counted)>=24,{"observed":dict(cats),"required":minimums,"total":len(counted)})
recount = load("evidence/recount.json")
check("source_recount_matches",len(sources)==recount["source_record_count"] and len(counted)==recount["distinct_counted_primary_works"] and dict(cats)==recount["count_categories"],{"records":len(sources),"works":len(counted)})
frame,chains,judgments = rows("frame.csv"),rows("chains.csv"),rows("judgments.csv")
selected = [r for r in frame if r["selected"]=="true"]
case_ids = {r["case_id"] for r in chains}
check("sampling_targets_and_case_joins",len(case_ids)==12 and len(selected)==12 and case_ids=={r["case_id"] for r in selected}, {"A":sum(r["stratum"]=="A" for r in chains),"B":sum(r["stratum"]=="B" for r in chains),"frame":len(frame)})
check("source_references_resolve",all(set(json.loads(r["source_ids"]))<=source_ids for r in chains),len(chains))
check("no_unknown_authority_when_observed",all(r["decision_authority"] != "미확인" for r in judgments if r["case_id"] in ("B02","B03","B04")),"authority fallback preserved; B04 mirror provenance remains explicit")
csv_locations = {}
for path,data in [("frame.csv",frame),("chains.csv",chains),("judgments.csv",judgments)]:
    # Returned search titles contain real newlines. Preserve valid quoted CSV,
    # and record physical line spans rather than pretending one row is one line.
    mapped = []
    with (ROOT/path).open(newline="") as f:
        reader = csv.DictReader(f)
        _ = reader.fieldnames
        previous = reader.line_num
        for index,row in enumerate(reader,1):
            mapped.append({"data_row":index,"first_line":previous+1,"last_line":reader.line_num,"frame_id":row.get("frame_id"),"case_id":row.get("case_id"),"interpretation":row.get("interpretation")})
            previous = reader.line_num
    check("csv_physical_line_locator:"+path,len(mapped)==len(data) and previous==(ROOT/path).read_text().count("\n"),{"logical_rows":len(data),"physical_lines":previous})
    csv_locations[path] = mapped
(ROOT/"evidence/csv-row-locations.json").write_text(json.dumps(csv_locations,ensure_ascii=False,indent=2)+"\n")
for interpretation in ("strict_initial_proposal","retrospective_analogy_same_baseline"):
    rr = [r for r in judgments if r["interpretation"]==interpretation]
    check("interpretation_cases:"+interpretation,len(rr)==len(case_ids) and {r["case_id"] for r in rr}==case_ids,len(rr))
    for r in rr:
        expected = all(r[k]=="true" for k in ("contemporary_source_confirmed","author_citation_primary_confirmed","exact_donor_mechanism_confirmed","changed_same_baseline_confirmed","actual_reflection_confirmed"))
        check("conjunction:"+interpretation+":"+r["case_id"],(r["complete_chain"]=="true")==expected,r["complete_chain"])
    for s in ("A","B"):
        subset=[r for r in rr if r["stratum"]==s]
        recorded=next(r for r in recount["table2_rows"] if r["stratum"]==s and r["interpretation"]==interpretation)
        actual=sum(r["complete_chain"]=="true" for r in subset)
        check("chain_recount:"+interpretation+":"+s,actual==recorded["complete_chain"] and len(subset)==recorded["unique_cases"],{"complete":actual,"cases":len(subset)})
sens=[r for r in judgments if r["interpretation"]=="sensitivity_standards_inclusive_preexisting_code"]
check("sensitivity_same_case_only",[r["case_id"] for r in sens]==["B02"] and recount["sensitivity"]["denominator"]==sum(r["stratum"]=="B" for r in chains),recount["sensitivity"])

report=(ROOT/"RESULT.md").read_text().splitlines()
tables=[]
for i,line in enumerate(report):
    if line.startswith("| ") and (i==0 or not report[i-1].startswith("| ")):
        j=i
        while j<len(report) and report[j].startswith("| "):j+=1
        tables.append((i+1,j,report[i:j]))
check("title_then_table1",report[0].startswith("# ") and tables[0][0]==3,tables[0][:2])
h1="| 층 | 사건 ID | 원래 목적·기존 선택 | 타 분야 원리·행위자 | 당시 원문 URL·절 | 연결 발언 URL·날짜 | 달라진 선택 | 같은 목적 반영 URL·범위 | 판정 | 미확인 |"
h2="| 층·조건 | 고유 사건 | 당대 가용 | 작성자 인용 | 명시적 선택 변경 | 실제 반영 | 사슬 완결 | 반증 시 뒤집힌 수 |"
check("mandatory_headers_and_order",tables[0][2][0]==h1 and tables[1][2][0]==h2 and tables[1][0]==tables[0][1]+2,[tables[0][0],tables[1][0]])
table1ids=[re.search(r"\b(?:A-[CG]\d{2}|B\d{2})\b",line).group() for line in tables[0][2][2:]]
check("table1_all_unique_cases",len(table1ids)==12 and set(table1ids)==case_ids,table1ids)
check("table2_five_conditions",len(tables[1][2])-2==5,len(tables[1][2])-2)
for line,recorded in zip(tables[1][2][2:6],recount["table2_rows"]):
    cells=[c.strip() for c in line.split("|")[1:-1]]
    expected=[recorded[k] for k in ("unique_cases","contemporary_source_confirmed","author_citation_primary_confirmed","explicit_change_confirmed","actual_reflection_confirmed","complete_chain","positive_grade_reversed_by_counterevidence")]
    actual=[int(re.match(r"\d+",c).group()) for c in cells[1:]]
    check("table2_values:"+recorded["stratum"]+":"+recorded["interpretation"],actual==expected,actual)
check("final_table_exact_three",len(tables[-1][2])-2==3 and tables[-1][2][0].startswith("| 중요한 불일치·약점 |") and tables[-1][1]==len(report),tables[-1][:2])
card_lines=[l for l in (ROOT/"cards.md").read_text().splitlines() if re.match(r"\| (A-[CG]\d{2}|B\d{2}) \|",l)]
check("twelve_cards_two_links",len(card_lines)==12 and all(len(re.findall(r"\]\(https?://",l))<=2 for l in card_lines),len(card_lines))
accept=load("evidence/acceptance-evidence.json")
check("unmet_preserved",accept["all_acceptance_conditions_met"] is False and set(accept["unmet_ids"])=={"AC03","AC05","AC06","AC18","AC19"},accept["unmet_ids"])
check("all_Q1_Q7",{q["id"] for q in accept["questions"]}=={f"Q{i}" for i in range(1,8)},len(accept["questions"]))
for q in accept["questions"]:
    for e in q["evidence"]+q["counterevidence"]:
        check("acceptance_source_locator:"+q["id"]+":"+e["source_id"],sources[e["line"]-1]["source_id"]==e["source_id"],e["line"])
check("saved_artifact_hashes",all(hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h for f,h in accept["artifact_sha256"].items()),list(accept["artifact_sha256"]))
csv_receipt=load("evidence/csv-verification.json")
check("csv_tool_receipt_current",all(hashlib.sha256((ROOT/r["file"]).read_bytes()).hexdigest()==r["sha256"] and r["checks_passed"] for r in csv_receipt["results"]),[r["file"] for r in csv_receipt["results"]])
changed=subprocess.check_output(["git","diff","--name-only","de544231bc72fa6f2ddb3e91f9c0e8d16a0d1f62"],cwd=REPO,text=True).splitlines()
untracked=subprocess.check_output(["git","ls-files","--others","--exclude-standard"],cwd=REPO,text=True).splitlines()
check("owned_path_only",all(p.startswith(OWNED) for p in changed+untracked),{"changed":len(changed),"untracked":len(untracked)})
rebuild=subprocess.run([sys.executable,"-B",str(ROOT/"evidence/rebuild.py"),"--check"],cwd=REPO,capture_output=True,text=True)
check("rebuild_check_exit",rebuild.returncode==0,{"exit_code":rebuild.returncode,"stdout":rebuild.stdout.strip(),"stderr":rebuild.stderr.strip()})
receipt={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"all_passed":all(c["passed"] for c in checks),"checks":checks,"structural_check_count":len(checks),"substantive_acceptance_all_met":False,"note":"Structural consistency does not erase AC03/05/06/18/19 or run historical programs. Postcommit remote re-open and session --fetch check belong in HANDOFF.","report_locations":{"table1":{"first_line":tables[0][0],"last_line":tables[0][1]},"table2":{"first_line":tables[1][0],"last_line":tables[1][1]},"weakness3":{"first_line":tables[-1][0],"last_line":tables[-1][1]}}}
(ROOT/"evidence/validation.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"all_passed":receipt["all_passed"],"checks":len(checks),"sources":len(sources),"works":len(counted),"cases":len(case_ids),"report_locations":receipt["report_locations"]},ensure_ascii=False))
