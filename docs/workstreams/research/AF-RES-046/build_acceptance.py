#!/usr/bin/env python3
"""Build an explicit acceptance ledger without turning missing observations into successes."""
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def read(name):
    return json.loads((ROOT/name).read_text())

def main():
    assembly=read("evidence/assembly.json")
    stats=read("evidence/statistics.json")
    cases=read("cases.json")
    sources=[json.loads(l) for l in (ROOT/"sources.jsonl").read_text().splitlines() if l.strip()]
    counted=[r for r in sources if r["count_in_minimum"]]
    alloc=Counter(r["allocation"] for r in counted)
    criteria=[]
    def add(id,question,requirement,status,num,den,unit,file,rows,reason,next_check,reversal,source_ids=None):
        criteria.append({"id":id,"question":question,"requirement":requirement,"status":status,"numerator":num,"denominator":den,"unit":unit,"evidence":[{"file":file,"rows":rows,"source_ids":source_ids or []}],"reason":reason,"minimum_followup":next_check,"condition_to_change_judgment":reversal})
    add("governance_and_dependencies","Q1","지정 governance와 pinned 의존 HANDOFF 읽기","충족",10,10,"입력 저작/판","streams/root/sources.jsonl","I01–I10","GitHub와 고정 git 객체에서 필수 입력을 확인; planned1f722/actual4492를 분리","새 계약/의존 변경이 생길 때에만 정확 SHA로 재검토","시작시 실제 읽은 판과 manifest가 다르면 재핀/영향분석")
    add("frame_enumeration","Q1","저장소×기간별40개·생성일/번호 순서","충족",160,160,"PR frame 행","frame.csv","data records1–160","4 queries each40; result status/merge로 슬롯을 바꾸지 않음","독립 코더가 동일 query를 재실행","누락/순서 오류가 확인되면 원frame 유지한 대안집계")
    add("twelve_slots","Q1","자연8+링크우선4 고정","충족",12,12,"고정 PR 슬롯","frame.csv","slot_id N-P1..N-S4,L-P1..L-S2","빈 슬롯0, PR 중복0. 미병합·무링크·무응답·선행착수도 유지","첫4/첫2의 별도 가림 재판독","선행 적격 탈락행 발견 시 선정 재검토")
    add("preoutcome_selection_freeze","Q1","선정은 작성자 응답/후속patch 판독 전에 원격 고정","부분 충족",12,12,"봉인 슬롯; 완전 가림은 별도","evidence/selection-freeze.json","freeze_commit994e21aaea7c5da0c4322db9d1ce2c4f52fa6a2f","원격 봉인 뒤 본격 결과 판독. 그러나 reviewer 필터의 후속 상태 단서 일부 노출 및 R01 선별중수정","결과를 가린 독립 코더가 frozen frame/당시판만 판독","완전가림을 소급주장하지 않음; 새로운 독립재현으로만 보완")
    add("full_outcome_blinding","Q1","선정 전 결말 단서도 완전히 가림","미충족",0,1,"전체 선정 절차","streams/crossdomain/selection-audit.md","L-P2,L-S1 및 비선정 노출 기록","후속 reviewer 문장이 URL filter에 함께 노출. 저자 반응을 읽지 않았다는 사실과 완전가림은 다름","별도 가림 코더와 당시자료로 같은선정 재현","해당 재현만 새로운 가림 분석으로 인정; 기존 오염 삭제불가")
    add("opening_snapshot_recovery","Q2","최초 공개 head/base/body와 실제 diff 연결","충족(공개 미러 기준)",stats["exact_first_public_heads_verified"],12,"선정 PR 최초판","initial-public-heads.csv","data records1–12","문서화된 opened-event mirror와 immutable GitHub diff 연결. 이전0/12 및 changed head2건 보존","각 raw hour JSON.gz에서 event ID/head/base/body hash 독립대조","mirror와 raw가 다르면 복원판정을 낮추고 재해석")
    add("raw_event_corroboration","Q2","정규화 미러와 원 이벤트 독립 확인","미충족",0,12,"선정 PR 원형 opened 이벤트","streams/pandas/initial-public-head-recovery.json;streams/sklearn/initial-public-head-recovery.json","raw_attempts/failed_attempts/remaining_limits","raw gzip403, mirror에 원 event ID 없음. 최초판 복원과 raw 독립 확인을 분리","기록된 시간별URL에서 정상공개 raw event 한 줄 확보","동일 event의 head/base/bodyhash 일치 시 각 슬롯 보완")
    add("first_link_classification","Q3","첫 적격 링크·제공자·위치·시간·URL종류 기록","충족",4,4,"링크 우선층 첫 사건","events.csv;cases.json","L-P1,L-P2,L-S1,L-S2","same-project2/external workflow1/external issue+notes1. 같은 발언의 두 URL은 한사건; 현재PR/봇/절차 링크 제외","누락된 더 이른 적격 human reviewer 발언 확인","더 이른 링크가 나오면 원판정과 새기준 모두 보존")
    add("reading_and_prior_awareness_coding","Q3","게시·감사·내용관여·명시열람·첫발견 구분","충족",12,12,"PR 사례 코드","cases.json","reading_status/target_content_engagement_confirmed/review_acknowledgement_confirmed","명시열람확인0/4, 내용관여2/4, 제안응답3/4; L-P2 target prior authorship 별도","자료별 당사자의 명시 읽음/사전인지 진술","새 진술이 같은 URL/판을 특정하면 해당 상태만 변경")
    add("explicit_first_discovery","Q3","첫 링크의 신규 발견을 당사자 근거로 확인","미충족",0,4,"첫 링크 사건","cases.json","explicit_first_discovery_observed","확인0은 미인지/무효과0이라는뜻이아님. L-P2는 target을 이미 작성","언제 처음 알았는지와 그 자료를 명시한 당사자 기록","첫 발견 근거가 직접 확보될 때만 분자 증가")
    same=sum(c["same_author_same_purpose_change"] is True for c in cases)
    unknown=[c["slot_id"] for c in cases if c["first_qualifying_link_observed"] and c["same_author_same_purpose_change"] is None]
    add("same_author_same_purpose_observed","Q4","첫 링크 뒤 주창의 동일인·동일목적 실제patch","부분 충족",same,4,"링크 우선층 사건","changes.csv;cases.json;streams/pandas/final-risk-review.json","same_author_same_purpose_change; L-P2-7 and S-C09",f"확정{same}/4; 미확인슬롯{unknown}. 확정 중 L-P2는사전작성로직의사후통합1건이며그유형제외시1/슬롯4. f951의주창공개미확인은유지. 부모생성에서통합하한을추론하고review로공개상한확인","미복구 원branch/공개event/review head 및 실제diff;19e exactpush 기록","같은행위자의 같은요구 patch가 창내 공개됐다는 고정판이 확보되거나통합부모의시점/행위자근거가반증될때")
    add("strict_first_link_chain","Q4","첫 링크→작성자 이유연결→동일인patch→시험/반영","미충족",0,4,"첫 링크 사건","RESULT.md","필수표1 L-P1..L-S2; Q3–Q4","링크의 명시 기여 연결없음/선행착수/다른작성자/후속판손실. 나중5243사건을첫5230대신넣지않음","첫자료와변경이유를 연결한 당사자발언과 대응시험/반영","모든 사슬고리가 같은첫사건으로 연결될 때만 확정")
    add("window_and_tail_separation","Q5","모든 PR 같은 first-terminal/90일 창과 후기 분리","충족",12,12,"PR 관측창","labor.csv;events.csv;sensitivity.csv","12 windows;36 sensitivity rows;post_closure_tail","무링크/무응답도같은창. git date와platform공개관측분리","누락된 최초종결/reopen event 또는창경계publicSHA 확인","창경계가바뀌면원집계/새집계함께보존")
    add("labor_unit_separation","Q5","직접로그·자기보고·경과·기계시간·산출물 분리","충족",12,12,"PR 노동 원장","labor.csv","data records1–12","benchmark초/CI초/commit수/LOC를 사람 시간으로 환산하지 않음. 소비자비용은별도","활동시작/중지와행위자·범위·중단기록","직접측정또는명시자기보고가있을때만값추가")
    add("direct_human_work_time","Q5","주창 표본 작성자의 직접 작업 로그 확보","미충족",0,12,"PR 작성자의 측정가능 능동시간","labor.csv","direct_work_log/direct_work_seconds","모든값미확인;0초아님. CI·주말대기분리불가","행위자·과제·시작/중지·대기구간 기록","같은기능수정의 실제노동시간이직접기록될때")
    add("author_duration_selfreport","Q5","주창 표본 작성자의 소요시간 자기보고","미충족",0,12,"PR 작성자 소요시간 보고","labor.csv","selfreport fields","소비자25261 manyhours는 다른사람·개설전·비수치라합산하지않음","표본작성자의시작/끝범위를명시한소요시간발언","단위·범위·행위자가명확할때자기보고열에만추가")
    add("quality_matched_savings","Q5/Q7","동등 품질 무링크 인간시간 비교쌍","미충족",0,12,"PR에 연결된 비교 가능한 시간·품질 쌍","labor.csv;RESULT.md","comparison_scope; Q7 최소기록1–5","비교쌍0; 절감량미확인, 조건부비율해당없음. 자연8은난이도/요구/작성자다름","동일요구·품질 기준과 인간시간을 양조건에 기록한 사전비교 설계","품질동등성과시간쌍이확보될때만절감량계산")
    add("competing_explanations_and_sensitivity","Q6/Q7","선행수정·실패·타인구현·유지·후기와감도","충족",12,12,"PR 사례의 경쟁 설명 코드","counterexamples.md;evidence/statistics.json","각사례;time_boundary_sensitivity;actor_and_prework_sensitivity","동일인/타인선행착수구분. 넓은사전작업조건은분모0으로명시. 강한뒤사건을첫사건으로대체하지않음","원source의순서/행위자/목적을반증하는새고정판","경쟁설명이틀렸다는직접자료가있으면해당사례와감도만수정")
    add("primary_source_total","자료수","고유1차저작 최소26개 직접판독","충족",len(counted),26,"한저작·한배당","sources.jsonl","count_in_minimum=true records","PR+ordinarycomments1/reviewID1/commit1; mirrors/revisits/failures0","counted source의고유성·직접읽은위치를재검토","중복/미열람이확인되면분자를줄임")
    for key,target,label in (("pr_origin",8,"원제안/초기구현"),("review_decision",5,"별도발행review"),("commit_test",6,"고정commit/시험"),("linked_original",3,"실제review가리킨원문")):
        source_ids=[s["source_id"] for s in counted if s["allocation"]==key]
        add("allocation_"+key,"자료수",label+" 최소배당","충족" if alloc[key]>=target else "미충족",alloc[key],target,"고유저작","sources.jsonl",f"allocation={key}; count_in_minimum=true","한원문은최소배당한곳에만산입","자료별저작/판/발행자/위치재열람","고유성/판독근거가무너지면산입제외",source_ids)
    add("music_edit_ledger","Q6/자료수","MusicBrainz 개별편집·노트·실제적용 전후","미충족",0,1,"음악 개별 원장 사례/필수저작","streams/crossdomain/sources.jsonl;streams/crossdomain/sources-supplement-recovery.jsonl","X-MB-BLOCK*;X-MB-REC-*","production403;공식beta/test 접근불가/timeout. 포럼취소/대체보고와운영규칙만으로실제적용승격불가","production또는공식beta edit49854105의상태/entity/old/new 확보→대체편집적용이력연결","개별노트·수정자·적용판이원문ID로연결될때")
    add("music_operating_rule","Q6/자료수","음악 운영규칙 원문","충족",alloc["music_rule"],1,"고유공식규칙","sources.jsonl","X-MB01","근거URL와설명/취소규칙을읽음;개별편집실행증거와구분","개별적용원장확보","규칙내용과현장기록을연결할때사례사슬보완",["X-MB01"])
    add("map_ledger_and_versions","Q6/자료수","지도 토론/수정 전후판 대조","충족",alloc["map_ledger"]+alloc["map_versions"],2,"고유원장/객체판","streams/crossdomain/counterexamples.md","X-OS;changeset192056303,node11329057532 v3/v4","타인수정01:03:05→출처댓글01:03:31;링크후원작성자수정아님","원작성자응답·작업로그가나오면별도추가","시간순서/행위자를뒤집는원형버전증거가있을때만변경")
    add("cross_domain_allocation","자료수","음악2+지도2 필수배당4","부분 충족",3,4,"필수배당저작","sources.jsonl","music_rule1/music_ledger0/map_ledger1/map_versions1","전체54가많아도음악ledger0을대체할수없음","음악개별원장1개추가","해당개별원장직접판독때4/4")
    add("required_tables_and_selfcheck","Q7/형식","12슬롯첫표·층별둘째표·Q1~Q7·끝3행","충족",7,7,"질문별점검","RESULT.md;SELF_CHECK.md","필수표1/2;Q1–Q7;마지막약점표","원문URL/위치·반증·최소뒤집기자료를각행에연결;validator구조검사별도","최종고정SHA두파일재열람","행수/출처/분모불일치가없을때")
    check_path=ROOT/"evidence/session-check.json"
    checked=read("evidence/session-check.json") if check_path.exists() else None
    ok=bool(checked and checked.get("exit_code")==0 and checked.get("parsed_stdout",{}).get("status")=="passed")
    add("session_check_fetch","운영","지정workbench.session check --fetch 실제실행","충족" if ok else "후속 검증 대기",1 if ok else 0,1,"명령실행","evidence/session-check.json","command/start/end/stdout/stderr/exit_code","Git계약·의존·허용경로검사이며연구인과/pytest검증아님","지정 check 명령을실행하고실제출력보존","exit0/statuspassed및outside_paths=[]일때")
    reread_path=ROOT/"evidence/fixed-result-recheck.json"
    reread=read("evidence/fixed-result-recheck.json") if reread_path.exists() else None
    rr_ok=bool(reread and reread.get("status")=="passed")
    add("fixed_result_reread","운영","커밋한RESULT와수용원장을SHA로재열람","충족" if rr_ok else "후속 검증 대기",2 if rr_ok else 0,2,"고정파일","evidence/fixed-result-recheck.json","files RESULT.md/evidence/acceptance-evidence.json","이항목은결과커밋뒤확인;계획문구를완료로세지않음","원격SHA로두파일열고blob/내용/표확인후영수증커밋","정확한커밋의두내용일치와표검산이확인될때")
    result={"task_id":"AF-RES-046","generated_utc":datetime.now(timezone.utc).isoformat(),"overall_status":"부분 인계 — 조사·원장·반증은 보존, 필수 음악 원장 및 엄격/노동의 긍정 증거 미충족","interpretation":"Unmet positive evidence is not evidence of no effect; missing labor remains unknown. Conditional denominators of zero are not applicable.","ledger_counts":{**assembly["counts"],"slots":12,"natural_slots":8,"link_priority_slots":4,"empty_slots":0,"opened_recoveries":stats["exact_first_public_heads_verified"],"source_allocation_required":{"pr_origin":8,"review_decision":5,"commit_test":6,"linked_original":3,"music_rule":1,"music_ledger":1,"map_ledger":1,"map_versions":1}},"primary_observations":{"first_qualifying_links":4,"explicit_reading":0,"target_content_engagement":2,"first_review_acknowledgement":3,"explicit_first_discovery":0,"same_author_change_confirmed":same,"same_author_change_unknown_slots":unknown,"any_author_change_confirmed":sum(c["any_author_same_purpose_change"] is True for c in cases),"strict_first_link_chain":0,"direct_active_human_time":0,"in_window_author_duration_selfreport":0,"quality_matched_time_pairs":0,"saved_human_seconds":None},"review_scope":{"self_reread":True,"separate_AI_crosscheck":True,"external_independent_human_coding":False,"fully_blinded_selection":False,"upstream_historical_tests_executed":False},"criteria":criteria}
    (ROOT/"evidence/acceptance-evidence.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"criteria":len(criteria),"status_counts":dict(Counter(c["status"] for c in criteria)),"ledger_counts":result["ledger_counts"],"primary_observations":result["primary_observations"]},ensure_ascii=False))

if __name__=="__main__":
    main()
