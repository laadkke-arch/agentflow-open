"""Build explicit item-level acceptance evidence from recorded ledgers."""
import pathlib,json,csv,collections,datetime,hashlib
P=pathlib.Path(__file__).resolve().parents[1]
def csvread(name):return list(csv.DictReader((P/name).open()))
sources=[json.loads(x) for x in (P/"sources.jsonl").read_text().splitlines()]
counted=[r for r in sources if r["minimum_count"]]
req=csvread("requests.csv");pred=csvread("predictions.csv");out=csvread("outcomes.csv");frame=csvread("frame.csv")
alloc=collections.Counter(r["allocation"] for r in counted)
items=[]
def add(i,title,met,n,d,unit,evidence,reason="",next_check="추가 확인 없음; 고정판 보존"):
 items.append({"id":i,"criterion":title,"status":"충족" if met else "미충족","numerator":n,"denominator":d,"unit":unit,"evidence":evidence,"unmet_reason":None if met else reason,"qualification":reason if met else None,"minimum_next_check":next_check})
ref=lambda f,rows:{"file":f,"rows_or_locator":rows}
add("A01","원래6요구와저장소별30노출보존",len(frame)==60 and len(req)==6,6,6,"requirement_slots",[ref("frame.csv","60 data rows;3selected perrepository"),ref("requests.csv","M01,M02,M03,AUD01,AUD02,AUD03")],"현재제목으로과거생성이슈표집;역사적제목검색복원아님.")
add("A02","12후보와요구별2행봉인",len(pred)==12 and all(v==2 for v in collections.Counter(r["request_id"] for r in pred).values()),12,12,"prediction_rows",[ref("predictions.csv","12data rows"),ref("evidence/prediction-seal.json","files")])
add("A03","후속첫열람전원격봉인확인",True,3,3,"readers",[ref("evidence/reveal-receipt.json","seal22:19:23Z;remoteverify22:19:27Z;root22:20:09.248Z"),ref("evidence/audacity-outcomes.json","first_outcome_opened_utc22:20:00.421Z"),ref("evidence/matplotlib12-outcomes.json","first_outcome_opened_utc22:20:03Z")],"편집된요구본문E01및교차API노출E02는별도감도;완전무노출보장아님.")
add("A04","4개고정입력해시불변",True,4,4,"files",[ref("evidence/verification.json","protected_hashes: SCOPE,frame,requests,predictions")])
add("A05","고유직접열람1차원문24개이상",len(counted)>=24,len(counted),24,"unique_primary_works",[ref("sources.jsonl","minimum_count=true;unique work_id"),ref("evidence/verification.json","sources")],"분모는최소목표수이며성공확률의분모가아님.")
add("A06","최초요구원문6",alloc["consumer_requests"]>=6,alloc["consumer_requests"],6,"unique_works",[ref("sources.jsonl","MPL-R13430,MPL-R13522,MPL-R13600,AUD-R407,AUD-R511,AUD-R644")])
donors=sum(alloc[k] for k in ["donor_spatial","donor_temporal","donor_other"])
add("A07","제공원전8이상",donors>=8,donors,8,"unique_works",[ref("sources.jsonl","SD01,SD02,SD04,SD06,TD01,TD02,TD03,TD04,WD01")],"같은수신소프트웨어매뉴얼은제공원전산입안함.")
add("A08","공간제공원전3이상",alloc["donor_spatial"]>=3,alloc["donor_spatial"],3,"unique_works",[ref("sources.jsonl","SD01,SD02,SD04,SD06")])
add("A09","영화방송제공원전3이상및시간경계3",alloc["donor_temporal"]>=3,alloc["donor_temporal"],3,"unique_works",[ref("sources.jsonl","TD01,TD02,TD03,TD04")],"시간경계자체는TD01/02/03=3;TD04는색상마스크.현대판역사가용성은별도.")
add("A10","수신후속원문6이상",alloc["receiver_followup"]>=6,alloc["receiver_followup"],6,"unique_works",[ref("sources.jsonl","MO04,MO05,MO06,MO08,RMO02,AUD-O6165,AUD-O6347,AUD-O2713,AUD-O6201")],"별도후속저작수.같은입력시험수아님;releaseAUD-O360중복제외.")
comp=alloc["comparison"]+alloc["independent_comparison"]
add("A11","독립비교원문4이상",comp>=4,comp,4,"unique_works",[ref("sources.jsonl","SD03,SC01,TC01,TC02,MC01,AUD-C5653")],"독립주제/작업의비교원문이지외부독립연구자검증을뜻하지않음.")
add("A12","정확한생성시점요구본문판확인",False,0,6,"requirements",[ref("requests.csv","first_body_status/body_revision"),ref("sources.jsonl","SELF-Q1-TITLE,SELF-Q1-BODY")],"모두현재첫게시본문;M03제목만최초제출,AUD02사후본문및제목변경.","해결조언전불변snapshot/편집이력한건부터복원.")
add("A13","사전노출기록과제외감도",True,3,3,"exposure_events",[ref("amendments.md","E01,E02,E03"),ref("RESULT.md","노출·판 필터 감도")],"E03은정원후다른본문노출이며E01/E02와같은결말노출로묶지않음.")
add("A14","모든후보의제공판을과거가용으로확정",False,4,9,"donor_works_with_dated_edition_evidence",[ref("sources.jsonl","SD02,TD01,TD02,WD01 dated editions;SD01,SD04,SD06,TD03,TD04 limits"),ref("RESULT.md","제공계열표")],"날짜고정판증거가있는4개와나머지를구분.이4개도역사적저자독서를뜻하지않음;현행Netflix/Apple및정확공개일미상원전잔존.","당시공개판·보관snapshot을필요절까지확인.")
add("A15","결정/명세/코드/시험정의/공개실행범위분리",True,6,6,"requirements",[ref("outcomes.csv","all12rows;evidence_levels;local_receiver_run"),ref("RESULT.md","Q4·Q5증거층위표")])
add("A16","봉인두입력과조작의동일조건후속시험",False,0,6,"requirements",[ref("outcomes.csv","matched_normal=false,matched_boundary=false allrows"),ref("RESULT.md","표1·표2")],"정성적수락,제3안,다른fixture,비활성API를완전한같은입력검증으로올리지않음.","M03고정3.0.2에A/B와factor.01/.001의actuallimits/anchor;역사적판정에는당시공개동일입력로그추가.")
add("A17","사전분류와0/1/2분모재집계",True,6,6,"requirements",[ref("evidence/verification.json","sealed_pair_classification,outcomes,sensitivity_populations"),ref("amendments.md","분모해석")],"넓은3/2/1유지.사후완결0=해당없음;원문관대해석M01분모1/유일지지0/판정불가1;조작수락M01+M03분모2/유일지지0/판정불가2.사후강화명시.")
add("A18","타분야원리의유일판별성공확인",False,0,1,"original_wording_lenient_eligible_requirements",[ref("outcomes.csv","strict_pair_denominator_member=false;unique_support=false"),ref("RESULT.md","Q4·Q5")],"사후완결분모0은해당없음;원문관대해석분모1과조작수락분모2에서도유일지지0.불가능증명아님.","같은조작/입력/목적의분기출력근거를최소한사례에서확보.")
add("A19","근접후보의그럴듯함과깨짐을기록",True,12,12,"prediction_rows",[ref("predictions.csv","initial_plausibility,receiver_mapping,breaks,domain_relation"),ref("cards.md","6cards")],"문장기록충족이둘다실제API에서가능하다는검증은아님. M01차이의약점명시.")
add("A20","사전수신API판독의정확성",False,0,1,"critical_preseal_API_check",[ref("amendments.md","AUD03localundefcorrection"),ref("sources.jsonl","AUD-BASE-CORRECTION,REV-AUD-NR242")],"NoiseReduction.cpp의local#undef누락이라는연구자오류를봉인후발견.","기존예측을고치지말고실제활성API/빌드경로부터새검사.")
add("A21","요청한네종류의반례를실제출력까지확인",False,3,4,"counterexample_types",[ref("RESULT.md","Q6"),ref("cards.md","M02,AUD01,AUD03")],"공간표시/위치,frame/sample단위,수신API제약은원문확인.양쪽후보가봉인두입력의출력을모두맞힌실제사례는미확인;M02공유조작수락만있음.","M02고정10/30입력의A/B실행과동일예측을관측.")
add("A22","입력·판·단위·비용민감도재계산/명시",True,4,4,"sensitivity_families",[ref("evidence/verification.json","arithmetic"),ref("RESULT.md","Q6민감도표")],"산술모델실행및정적코드/명세비교.수신프로그램실행이아님.")
add("A23","반환수준·새선택·동률·채택구분",True,6,6,"cards",[ref("cards.md","6cases"),ref("RESULT.md","Q7")],"완전사슬0/6,조건부참고와모양유사수준명시;historicalinspiration/retrieval/laborsaving주장없음.")
add("A24","필수표12/6와RESULT말미약점3행",True,2,2,"mandatory_tables",[ref("evidence/deliverable-validation.json","result_tables,ending_weakness_rows"),ref("RESULT.md","first2tables;lasttable")])
add("A25","Q1–Q7재판독·반증·최소반전자료",True,7,7,"questions",[ref("SELF_CHECK.md","Q1...Q7"),ref("evidence/final-method-review.md","same-modelreview"),ref("evidence/final-spatial-review.md","same-modelreview"),ref("evidence/final-audacity-review.md","same-modelreview")],"외부독립판독은수행하지않았다고구분.")
add("A26","고정결과와수용원장원격재열람",False,0,2,"files",[ref("evidence/result-verification.json","pendingafterbatch4commit")],"이원장초안은원격커밋전이다.커밋후실제응답과해시를기록하고상태갱신.","RESULT.md와acceptance-evidence.json을같은고정SHA에서fetch_file로다시읽음.")
add("A27","종료session check실제출력보존",False,0,1,"command",[ref("evidence/session-check.json","pending")],"최종고정결과커밋뒤check --fetch를실행할예정;아직완료로표시하지않음.","python -B -m workbench.session check docs/workstreams/research/AF-RES-045/manifest.json --fetch")
add("A28","사후판정기준강화와원규칙집계보존",True,1,1,"rule_change",[ref("amendments.md","최종방법반론"),ref("RESULT.md","세분모표"),ref("outcomes.csv","explicitmembershipfields")],"원SCOPE에없는두입력·경쟁조작완결조건을사후강화로공개;원문관대1과조작수락2함께보존.")
result={"schema_version":1,"task_id":"AF-RES-045","status":"partial_handoff","overall_claim":"자료수·봉인·조사산출물은충족;동일입력후속검증과유일판별성공미충족.","generated_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"repository":"laadkke-arch/agentflow-open","branch":"work/research-af-res-045","owned_path":"docs/workstreams/research/AF-RES-045/","planning_base_sha":"1f722bfb7360ff9c8d221284d7b1b6484c6fa692","actual_integration_sha":"4492dd8e9978087b32897ec2685110d24f510473","prediction_seal_sha":"0d998cb3503e8a7f0faf2bf2f8e62dd046a662b1","counts":{"frame":len(frame),"requests":len(req),"predictions":len(pred),"outcome_rows":len(out),"source_records":len(sources),"unique_counted_works":len(counted),"allocation_raw":dict(alloc),"quota_normalized":{"consumer_requests":alloc["consumer_requests"],"donors":donors,"donor_spatial":alloc["donor_spatial"],"donor_temporal":alloc["donor_temporal"],"donor_other":alloc["donor_other"],"receiver_followup":alloc["receiver_followup"],"independent_comparison":comp},"empty_requirement_slots":0,"empty_prediction_slots":0,"verifiable_creation_body_editions":0,"same_two_input_followup_cases":0,"judgments":dict(collections.Counter(r["judgment"] for r in out))},"original_preseal_relations":{"different":3,"same":2,"underdetermined":1},"strict_discrimination":{"numerator_unique_support":0,"denominator_same_input_followup":0,"both_rejected":0,"indeterminate_within_eligible_denominator":0,"conditional_ratio":"해당 없음","full_six_slot_disposition":{"different_but_insufficient_matching_outcome":3,"same_predictions":2,"underdetermined":1}},"review":{"self_reread":True,"same_model_separate_context":True,"external_independent_reader":False,"historical_receiver_execution":False,"arithmetic_and_structural_verification_executed":True},"acceptance":items,"input_hashes":{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ["SCOPE.md","frame.csv","requests.csv","predictions.csv","outcomes.csv","sources.jsonl"]},"postseal_corrections_preserved_in":"amendments.md","note":"미충족은증거상태다.자료수충족이나검사통과만으로원리가설계선택을가른다는성공을선언하지않는다."}
result["strict_discrimination"]["rule_status"]="post-reveal strengthened complete-comparison criterion, not identical to prespecified wording"
result["denominator_policies"]={
 "complete_comparison_post_reveal":{"case_ids":[],"denominator":0,"unique_support":0,"both_rejected":0,"indeterminate":0,"ratio":"해당 없음"},
 "original_wording_lenient":{"case_ids":["M01"],"denominator":1,"unique_support":0,"both_rejected":0,"indeterminate":1,"qualification":"qualitative original-input A report admitted; B unknown and P2 already predicts failure"},
 "operator_only_sensitivity":{"case_ids":["M01","M03"],"denominator":2,"unique_support":0,"both_rejected":0,"indeterminate":2,"qualification":"input identity relaxed; M03 factor-specific output absent"}}
# Preserve real, already-observed workflow receipts when regenerating this ledger.
receipt_path=P/"evidence/result-verification.json"
check_path=P/"evidence/session-check.json"
if receipt_path.exists():
 receipt=json.loads(receipt_path.read_text())
 if receipt.get("status")=="passed" and len(receipt.get("files",[]))==2 and all(r.get("equal_to_committed_input") for r in receipt["files"]):
  item=next(r for r in items if r["id"]=="A26")
  item.update(status="충족",numerator=2,unmet_reason=None,qualification="Fixed batch4 files directly reopened aftercommit; final verification-commit reread is additionally recorded in HANDOFF.",minimum_next_check="추가 확인 없음; 고정판·재열람 영수증 보존",evidence=[ref("evidence/result-verification.json",receipt["fixed_result_commit"]+";files")])
if check_path.exists():
 session=json.loads(check_path.read_text())
 if session.get("exit_code")==0 and json.loads(session["stdout"]).get("status")=="passed":
  item=next(r for r in items if r["id"]=="A27")
  item.update(status="충족",numerator=1,unmet_reason=None,qualification="Actualcheck --fetch passed; Git ownership/contract gate only, not product verification.",minimum_next_check="다음 재개 때 같은 명령 재실행",evidence=[ref("evidence/session-check.json",session["head_at_check"]+";stdout,started_utc,finished_utc")])
(P/"evidence/acceptance-evidence.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"records":len(sources),"counted":len(counted),"items":len(items),"met":sum(i["status"]=="충족" for i in items),"unmet":sum(i["status"]=="미충족" for i in items)},ensure_ascii=False))
