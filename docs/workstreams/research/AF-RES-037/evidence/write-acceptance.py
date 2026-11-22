#!/usr/bin/env python3
"""Write a transparent pre-handoff acceptance record, including unmet items."""
import csv
import datetime
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
recount = json.loads((ROOT / "evidence/recount.json").read_text())
locations = json.loads((ROOT / "evidence/source-locations.json").read_text())
cases = json.loads((ROOT / "evidence/case-decisions.json").read_text())
result_lines = (ROOT / "RESULT.md").read_text().splitlines()


def locate(path, text):
    lines = (ROOT / path).read_text().splitlines()
    return {"file":path, "line":next(i for i,l in enumerate(lines,1) if text in l), "marker":text}


def source_evidence(ids):
    return [{"source_id":s, "file":"sources.jsonl", "line":locations[s]["sources_jsonl_line"], "original_url":locations[s]["url"], "locator":locations[s]["locator"]} for s in ids]


questions = [
    {"id":"Q1", "status":"partial", "judgment":"CSS/GDAL 각4 최초 실질 제안을 복원하고 선택·제외·중복·노출을 고정. 완전 결말 비노출은7/8.", "numerator":8,"denominator":8,"evidence_ids":["CSS-001","CSS-002","CSS-003","CSS-004","GDAL-001","GDAL-002","GDAL-003","GDAL-004"],"counter_ids":["CSS-007","CSS-020"],"unknowns":"A-C03의 우발 결의 스니펫 노출; 명칭 변경의 포함 경계. 최초판8은 복원됐으나 전체 설계자의 지식은 미확인.","files":["SCOPE.md","frame.csv","streams/csswg/method.md","streams/gdal/boundary-reconciliation.json"]},
    {"id":"Q2", "status":"partial", "judgment":"고정3분야 쿼리·각 최초10 결과에서 round-robin 4후보 추적. A/B 동일 사건0. B04 원 발행자 본문 미확보.", "numerator":4,"denominator":4,"evidence_ids":["B-S06","B-S07","B-S11"],"counter_ids":["B-S13","B-S35","B-S40"],"unknowns":"B04 발행자/기관 본문; B01 핵심 hz와 B03 악보 판은 확인되지 않음. 미러를 최소수에 산입하지 않음.","files":["streams/b/frame.json","streams/b/initial.json","streams/b/attempts.jsonl","frame.csv"]},
    {"id":"Q3", "status":"partial", "judgment":"12사건의 P/V/I/A와 최초안·연결·변경·반영을 분리. 시간 공백과 날짜 종류를 보존.", "numerator":12,"denominator":12,"evidence_ids":["ROOT-P01","ROOT-P08","ROOT-P10","GDAL-M049665","B-S15","B-S20","B-S32"],"counter_ids":["ROOT-P02","CSS-021","B-S13"],"unknowns":"역사 검색색인·저자 첫 독서일12건 미확인. B03 mtime는 공개일 증명 아님. 원문 접근 실패를 서지로 메우지 않음.","files":["chains.csv","sources.jsonl","streams/b/followup.json"]},
    {"id":"Q4", "status":"met_with_recorded_unknowns", "judgment":"입력·동일 객체·권한·상태 전후·출력 제약을 사건별로 대응. B02의 원안 기준과 코드 기준을 분리.", "numerator":12,"denominator":12,"evidence_ids":["GDAL-003","GDAL-C73SRS","B-S20","B-S21","B-S32","ROOT-P06","ROOT-P10"],"counter_ids":["CSS-007","ROOT-C02","ROOT-C01","GDAL-M049649"],"unknowns":"정확한 타 분야 원전과 같은 기준선의 인과 변경을 결합한 strict 사슬은0. B04 mapping은 미러의 제한된 근거.","files":["chains.csv","judgments.csv","evidence/case-decisions.json"]},
    {"id":"Q5", "status":"met_with_recorded_unknowns", "judgment":"같은 목적의 고정 명세·코드·시험·공지와 미반영 범위를 추적. A후속반영7/8, B정적반영3/4; 역사 실행0.", "numerator":12,"denominator":12,"evidence_ids":["CSS-010","CSS-011","CSS-013","GDAL-M048296","GDAL-C72INI","GDAL-C73CTTEST","GDAL-C74CONF","B-S16","B-S21","B-S22","B-S32"],"counter_ids":["CSS-016","GDAL-M049658","B-S26","B-S44"],"unknowns":"C01의 실제 페이지 변경, B04의 특정 구현, 모든 역사 런타임. 서로 다른 하위기능·버전의 인과를 합치지 않음.","files":["chains.csv","RESULT.md","streams/gdal/case-analysis.md","streams/b/followup.json"]},
    {"id":"Q6", "status":"partial", "judgment":"네 반례 목표 모두 추적. 객체 혼동·시간 역전은 직접 관측, 독립 원리 발명과 확정 채택 전 공급자 포기는 미확인.", "numerator":4,"denominator":4,"evidence_ids":["CSS-007","CSS-021","GDAL-M049649","B-S06","ROOT-C01","ROOT-C02","ROOT-C03","ROOT-C04","ROOT-C05"],"counter_ids":["ROOT-P10","C4-RFC72-V1","C4-RFC72-V11"],"unknowns":"알고리즘 독립 구현을 원리 독립 발명으로 바꾸지 않음. RFC72 최초 CI 코드가 이미 sugar-off여서 활성→철회 사슬 미확인.","files":["judgments.csv","streams/review-counts/countertype4.json","streams/review-csswg/review.md"]},
    {"id":"Q7", "status":"met", "judgment":"12카드·세 묶음·카드당 최대2링크. strict 적격 A0/B0이면 조건부 회수율 해당 없음. 코드 기준 감도 B02는 별도.", "numerator":12,"denominator":12,"evidence_ids":["GDAL-003","B-S18","B-S20","B-S21","ROOT-P10"],"counter_ids":["B-S26","B-S40"],"unknowns":"검색 실험은 하지 않아 회수율·새 원리 발견 성능 미측정. 조건부 B02 준수 대조를 strict 새 학습 양성으로 사용하지 않음.","files":["cards.md","judgments.csv","evidence/recount.json","RESULT.md"]},
]
for q in questions:
    q["evidence"] = source_evidence(q.pop("evidence_ids"))
    q["counterevidence"] = source_evidence(q.pop("counter_ids"))
    q["result_location"] = locate("RESULT.md", "## " + ("Q1·Q2" if q["id"] in ("Q1","Q2") else "Q4·Q5" if q["id"] in ("Q4","Q5") else q["id"]))

criteria = []
def criterion(id, name, met, numerator, denominator, files, evidence_ids=None, shortfall="없음"):
    criteria.append({"id":id,"condition":name,"met":met,"numerator":numerator,"denominator":denominator,"files":files,"evidence":source_evidence(evidence_ids or []),"shortfall_reason":shortfall})

criterion("AC01","계획/배정 SHA·환경·독립 경로·선행 입력 고정",True,1,1,[locate("manifest.json",'"task_id"') if '"task_id"' in (ROOT/'manifest.json').read_text() else {"file":"manifest.json","line":1},locate("SCOPE.md","고정 시각"),{"file":"evidence/prior-exclusions.json","line":1}])
criterion("AC02","A 각 원장 최대40 내 결정 우선8선정·최초판복원",True,8,8,[{"file":"frame.csv","line":1},{"file":"streams/gdal/boundary-reconciliation.json","line":1}], ["CSS-001","CSS-002","CSS-003","CSS-004","GDAL-001","GDAL-002","GDAL-003","GDAL-004"])
criterion("AC03","A 최초판 동결 전 완전한 후속 결말 비노출",False,7,8,[locate("streams/csswg/method.md","노출 편차"),{"file":"evidence/protocol-amendments.jsonl","line":1}], ["CSS-003"],"A-C03 선정 뒤 최초판 복원 검색에서 후속 결의 스니펫이 보임. 사례 교체 없이0/7감도를 추가.")
criterion("AC04","B 최소2분야·고정쿼리별 최초10·4후보 추적",True,4,4,[{"file":"streams/b/frame.json","line":1},{"file":"frame.csv","line":1}], ["B-S06","B-S07","B-S11","B-S12"])
criterion("AC05","B 네 후보 모두 원 발행자/기관 초기 수신 본문 직접 열람",False,3,4,[{"file":"streams/b/attempts.jsonl","line":1}], ["B-S13","B-S35","B-S40"],"B04 AMS403·Stanford503. Typekit 미러는 읽었으나 최소수/원 발행본 조건에 산입하지 않음.")
criterion("AC06","B 인과의 핵심 제공 원전 접점을 모두 직접 복원",False,1,4,[{"file":"chains.csv","line":10}], ["ROOT-P10","ROOT-P08","B-S06","B-S32","B-S13"],"B02 기술 준수 원전만 좁게 연결. B01 hz1993, B03 정확한 악보 판, B04 Goudy/Zapf 원전과 원 수신본 미확인. Wild·MPA·MOLA로 대체하지 않음.")
minimums = [("AC07","외부 고유1차 원문 최소24",49,24,None),("AC08","A 최초 수신 원문8",8,8,"A_initial"),("AC09","날짜·판 있는 제공 분야 운영규칙/설계서6",10,6,"donor_rule_or_design"),("AC10","수신 후속 결정·반영6",15,6,"recipient_followup"),("AC11","독립 반대·제약 기록4",10,4,"independent_counterrecord")]
for id,name,n,minimum,cat in minimums:
    actual = recount["distinct_counted_primary_works"] if cat is None else recount["count_categories"][cat]
    assert actual == n
    criterion(id,name,actual>=minimum,actual,minimum,[{"file":"evidence/recount.json","line":1}],recount["source_ids_by_category"].get(cat,[]),"총량은 충족. 제공 규칙10은 실제 인과 donor10이 아니며 사건별 원전 공백은 별도." if cat=="donor_rule_or_design" else "없음")
criterion("AC12","원문별 필수키·URL·판/위치·한계·실패·고유작품 처리",True,recount["source_record_count"],recount["source_record_count"],[{"file":"sources.jsonl","line":1},{"file":"evidence/source-locations.json","line":1},{"file":"streams/review-counts/report.json","line":1}])
criterion("AC13","A/B 모든 추적·탈락·미심사 및 중복 처리 복원",True,219,219,[{"file":"frame.csv","line":1},{"file":"evidence/prior-exclusions.json","line":1}],shortfall="A/B 중복0. B 첫10 30행과 상한밖73행, GDAL 경계71행은 선정 분모와 구별.")
criterion("AC14","12사건 사슬 접점에 직접 근거 또는 미확인/실패 영수증",True,12,12,[{"file":"chains.csv","line":1},{"file":"judgments.csv","line":1}])
criterion("AC15","출판·당시공개·역사색인·저자읽기 및 신규대상/신규인지 분리",True,12,12,[{"file":"chains.csv","line":1},locate("RESULT.md","## Q3")],shortfall="역사 검색색인·첫 독서의 미확인을 보존했다는 조건의 충족이며 값 자체가 확인됐다는 뜻이 아님.")
criterion("AC16","객체·권한·전후·범위·세 관점 및 반영/미반영 표시",True,12,12,[{"file":"chains.csv","line":1},{"file":"judgments.csv","line":1},locate("RESULT.md","### 누가")])
criterion("AC17","네 반례 목표의 반대 기록 탐색·조건 기록",True,4,4,[locate("RESULT.md","## Q6"),{"file":"streams/review-counts/countertype4.json","line":1}])
criterion("AC18","다른 분야 원리 자체의 독립 발명 반례를 직접 확정",False,0,1,[locate("RESULT.md","② 유사하지만 독립 발명")],["B-S06","B-S40"],"알고리즘 독립 구현은 확인했으나 원리의 독립 발명으로 확대할 수 없음. 새 사례로 표집을 교체하지 않음.")
criterion("AC19","확정된 타 분야 채택을 공급자 제약으로 반영 전 새로 포기한 사슬",False,0,1,[{"file":"streams/review-counts/countertype4.json","line":1}],["C4-RFC72-V1","C4-RFC72-V11","B-S26"],"조건부 CI 제외·기존 포맷 호환성 제한은 확인. sugar-enabled 이전 상태와 공급자 실패→철회 사슬 미확인.")
criterion("AC20","엄격/회고 기준·동일 사건 코드 감도·적격0 처리 분리",True,25,25,[{"file":"judgments.csv","line":1},{"file":"evidence/recount.json","line":1}])
criterion("AC21","사건별 선택/절/금지조건과 최대2링크의 카드",True,12,12,[{"file":"cards.md","line":1}])
criterion("AC22","RESULT 제목 직후 필수표1·표2 및 전체 사건",True,2,2,[locate("RESULT.md","| 층 |"),locate("RESULT.md","| 층·조건 |")])
criterion("AC23","마지막 동순위 약점3개와 각각 다음 첫 자료·전복조건",True,3,3,[locate("RESULT.md","| 중요한 불일치·약점 |"),{"file":"evidence/weaknesses.json","line":1}])
criterion("AC24","재계산·CSV 독립 파싱·추적키 결합 검사",True,3,3,[{"file":"evidence/csv-verification.json","line":1},{"file":"evidence/rebuild.py","line":1}])

md = ["# AF-RES-037 · 자체 점검", "", "**정해진 표집의 조사·기록을 마쳤지만 수용 조건 일부는 미충족이다.** 엄격 사슬0은 허용되는 관측 결과이며 실패 조건으로 만들지 않았다. 원전 열람 공백·완전 비노출 실패·엄격 반례의 미확인은 별도로 남긴다.", "", "## Q1–Q7 대조", "", "| 질문 | 판단·확인 범위 | 직접 근거·위치 | 반대 근거 | 남은 미확인 |", "| --- | --- | --- | --- | --- |"]
for q in questions:
    link = lambda e:f"[{e['source_id']}]({e['original_url']}) {e['locator']} (`sources.jsonl` L{e['line']})"
    md.append("| " + " | ".join([q["id"]+" · "+q["status"],q["judgment"],"; ".join(link(e) for e in q["evidence"][:3]),"; ".join(link(e) for e in q["counterevidence"][:2]),q["unknowns"]]) + " |")
md += ["", "JSON 수용 원장은 각 질문의 전체 source ID·직접 URL·locator·정확한 원장 행을 포함한다. 위 표는 주요 근거만 표시한다.", "", "## 수용 조건", "", "| 조건 | met | 분자/분모 | 부족한 이유 또는 범위 |", "| --- | --- | --- | --- |"]
for c in criteria:md.append(f"| {c['id']} · {c['condition']} | {str(c['met']).lower()} | {c['numerator']}/{c['denominator']} | {c['shortfall_reason']} |")
md += ["", "## 실제로 수행한 점검", "", "- `python -B docs/workstreams/research/AF-RES-037/evidence/rebuild.py --check`: 원 stream·정정·해석 플래그에서 산출 CSV/JSON의 내용 일치를 점검한다. 사슬 완결과 분모를 상수로 고정하지 않는다.", "- `evidence/verify-csv.mjs`: 기본 runtime의 Artifact Tool로 CSV3개를 독립 import, 219/12/25행과 ID 결합·해석별 행을 검사했다. JSON 영수증의 파일 해시와 실제 파일이 일치해야 한다.", "- `evidence/validate.py`: 원문 고유성·범주 수·source 참조·두 표의 순서/행·마지막3행·카드 링크 수·허용 경로를 검사한다. 결과 영수증은 `evidence/validation.json`이다.", "", "## 실행하지 않은 검사와 경계", "", "역사적 GDAL·pdfTeX·LilyPond·browser 실행은 하지 않았다. 정적 코드/시험·당대 작성자 보고를 연구자의 실행 성공으로 바꾸지 않았다. 확인한 현재 환경과 버전 차이, 고정 입력·재개 명령은 `streams/b/followup.json`, `streams/gdal/case-analysis.md`에 있으며 최종 HANDOFF에 다시 모은다. 미확정 의존성 SHA는 미확인으로 둔다.", "", "## 커밋 뒤에 수행할 종료 순서", "", "RESULT와 수용 파일을 원격에 커밋한 뒤 그 고정 SHA에서 두 파일을 다시 열고 `python -B -m workbench.session check docs/workstreams/research/AF-RES-037/manifest.json --fetch`를 실행한다. 이 시점의 결과를 아직 실행한 것으로 표시하지 않는다. 실제 명령 출력·고정 SHA·파일 해시·마지막 HANDOFF 별도 커밋은 HANDOFF에 기록한다.", "", "## 첫 결론에 반하는 자료까지 읽었는가", "", "그렇다. 기존 규칙 설명이라는 해석 뒤 B02의 실제 패치·시험과 B03의1998 초기 변경 진술을 찾아 긍정 범위를 보강했다. 반대로 GML 규칙 부재라는 설명은 원 규범을 회수해 수정했고, CI 공급자 제약의 포기 사례는 최초 코드가 이미 off여서 엄격한 철회로 셀 수 없음을 확인했다. 원값·새 근거·분모 영향은 protocol-amendments와 review 파일에 보존했다. 엄격 양성0을 맞추기 위해 실제 변화를 삭제하지 않았다.", ""]
(ROOT / "SELF_CHECK.md").write_text("\n".join(md))
file_names = ["manifest.json","SCOPE.md","sources.jsonl","frame.csv","chains.csv","judgments.csv","cards.md","RESULT.md","SELF_CHECK.md"]
acceptance = {
    "work_id":"AF-RES-037", "checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "status":"recorded_with_unmet_conditions", "all_acceptance_conditions_met":all(c["met"] for c in criteria),
    "scope_commit":"b6ba3ccb7631ef1d219300ce28844e444f99baaa", "initial_freeze_commit":"7a33c17be2d25b2c1936038205187e8108bf4482", "observations_commit":"d3643808010c5d465aea05e0efea46f625e8b9c9",
    "final_result_commit":"recorded in HANDOFF after fixed-SHA re-open; no self-referential SHA invented",
    "criteria":criteria,"questions":questions,
    "recount":recount,
    "unmet_ids":[c["id"] for c in criteria if not c["met"]],
    "runtime_execution":{"historical_program_tests_run":0,"status":"미실행","current_environment_only":"GDAL3.10.3/pdfTeX1.40.26; Python2/LilyPond absent; JP2KAK unrecognized; B attempts receipt"},
    "postcommit_checks":{"fixed_sha_result_and_acceptance_reopen":"pending by required ordering; actual receipt belongs in final HANDOFF","workbench_session_check_fetch":"pending by required ordering; actual command/result belongs in final HANDOFF","handoff_only_last_commit":"pending after preceding checks"},
    "artifact_sha256":{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in file_names},
    "not_performed":["BM25 ranking rerun","200-token window experiment","017 origin7 rerun","search recall measurement","new candidate replacement after failure"],
}
(ROOT / "evidence/acceptance-evidence.json").write_text(json.dumps(acceptance,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"criteria":len(criteria),"unmet":acceptance["unmet_ids"],"questions":len(questions),"strict_complete":recount["strict_eligible"]},ensure_ascii=False))
