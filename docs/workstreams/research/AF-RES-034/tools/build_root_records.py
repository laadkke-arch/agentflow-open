"""Materialize root's human-reviewed extraction. Does not fetch or execute study code."""
import json, hashlib, csv
from pathlib import Path
R=Path(__file__).resolve().parents[1]/'streams/root'
G='https://github.com/ronxin/codemend/blob/445d5d822174aa7cdfd7ceb16ce5db18f4e2b69d/'
U='https://lxieyang.github.io/assets/files/pubs/unakite-uist-2019/unakite-uist-2019.pdf'
C='https://cond.org/codemend.pdf'
checked='2026-11-22T15:56:17Z'
sources=[]
def source(id,type,title,url,fixed,year,loc,content,limits,family,cat,file=None,**kw):
 x=dict(source_id=id,type=type,publisher='원 저자 공개본/저자 GitHub',title=title,original_url=url,fixed_url=fixed,published=year,version='출판 저자본' if type=='primary_human_study' else 'Git commit 445d5d822174aa7cdfd7ceb16ce5db18f4e2b69d (2016-10-17)',checked_utc=checked,read_locator=loc,verified_content=content,questions=['Q2','Q3','Q4','Q5','Q6','Q8'],claim_ids=[],limitations=limits,study_family=family,count_category=cat,count_minimum=True,access_level='D1' if type=='primary_human_study' else 'D2',aliases=[],reader='root',**kw)
 if file:
  b=(R/'tmp'/file).read_bytes();x['download_sha256']=hashlib.sha256(b).hexdigest();x['download_bytes']=len(b)
 sources.append(x)
source('Rt-S01','primary_human_study','Unakite: Scaffolding Developers’ Decision-Making Using the Web','https://doi.org/10.1145/3332165.3347908',U,'2019','Evaluation pp.8–9, Table1/Figure6, Discussion p.10; system overview와references; p.9 렌더 재확인',
 '연구1 20명은 근거 수집·정리 도구 조작시간 비중을 비교했다. 연구2의 별도16명은 같은 웹 자료 또는 사전 구조화표를 사용해 정답설명3개를 제시했고 전원 완료했다. 평균시간114.63초 대332.56초. 연구1 P3의1주 인터뷰는 채택 후 사용 확인이며 비교된 재작업 시간이 아니다.',
 '구조·요약·인터페이스·훈련이 함께 바뀐다. 시간비중을 전체 노동시간으로 바꾸지 않는다. 연구2 paired 원자료·공분산 없어서 CI 미계산. 연구1 표 작성의 독립 품질 점수와 군별 n은 본문에서 미확인. 장기 필드 연구는 미래 계획.',
 'ROOT-UNAKITE-2019','software_primary','unakite.pdf',read_evidence_refs=['turn129164723view1'],claim_ids_override=['Cr-01','Cr-02','Cr-03'])
source('Rt-S02','primary_human_study','CodeMend: Assisting Interactive Programming with Bimodal Embedding','https://doi.org/10.1145/2984511.2984544',C,'2016','Evaluation pp.8–9, Table5, Lab User Study p.9, Limitations/Discussion p.10; system overview와 References pp.11–12',
 '20학생이 두 UI를 번갈아 사용해 막대/원 그래프를 각3단계 수정했다. 두 조건 모두 Google 허용. 완료 subtask46 대41, 평균108.70 대134.12초, 저자는 통계적 유의 차이 없다고 보고했다. 별도 IR 평가에 쓰인361선별 질의는 lab 참여자 시간이 아니다.',
 '반복 측정, 완수한 subtask 평균의 정확한 분석 분모·미완료 처리·SD 미공개. 자동 제안/미리보기/삽입·모델이 함께 바뀌며 링크 단독 개입 아님. 사후 모델 튜닝을 최초 결과와 섞지 않는다. 재작업 추적 없음.',
 'ROOT-CODEMEND-2016','software_primary','codemend.pdf',read_evidence_refs=['turn939796939view0'],claim_ids_override=['Cr-04','Cr-05'])
source('Rt-A01','original_artifact','CodeMend lab study preparation notebook',G+'codemend/models/user-study-prepare-0405.ipynb',G+'codemend/models/user-study-prepare-0405.ipynb','2016','notebook cells0–15 전체 source; Practice Task, Task1, Task2',
 '연습은 선 굵기·색·marker 변경, 본 과제는 bar grid·x-label 회전·hatch와 pie title bbox크기·색·90도 회전의 누적 목표 코드를 포함한다. 자극을 여러 번 반복해서 세지 않고 notebook1개로 센다.',
 '논문은 bar 마지막변경을 shadow라고 부르지만 공개 준비본은 hatch이다. 정확한 실험 제공판 동일성 미확인. 사람별 시간/완료 기록은 없다. 읽기만 했고 Python2 시각화 코드를 실행하지 않았다.',
 'ROOT-CODEMEND-2016','original_artifact','cm-user-study-prepare-0405.ipynb',artifact_scope='lab task preparation',study_version_verified=False)
source('Rt-A02','original_artifact','CodeMend crowd query stimulus preparation notebook',G+'codemend/models/mturk_data_prepare_0302.ipynb',G+'codemend/models/mturk_data_prepare_0302.ipynb','2016','notebook cells0–44 source 전체, Before/After labels and task headings',
 '5종류 그래프와 각2개 변경수준을 만들어10before-after 자극으로 제시하는 코드와 별도 boxplot 예시 지시용 자극이 있다. 논문 IR 절의 질의 수집 자극에 대응하며 lab과 다른 입력이다.',
 '사람이 만든 검색 질의의 원자극이며20명 lab의 근무시간 측정자료가 아니다. 배포 당시 개별 화면·질문지·workerID는 없다. 파생 이미지마다 별자료로 세지 않는다. 논문은 five pairs로 보고하지만 준비본은10후보쌍이므로 실제 배포 After판은 미확인이다.',
 'ROOT-CODEMEND-2016','original_artifact','cm-mturk_data_prepare_0302.ipynb',artifact_scope='crowdsourced IR query stimuli, not lab labor outcome',study_version_verified='family/content match; exact deployed version unknown')
source('Rt-A03','original_artifact','CodeMend filtered query and answer corpus',G+'codemend/models/eval-gt-2.csv',G+'codemend/models/eval-gt-2.csv','2016','CSV header 및 전체362records 기계검사; rows2–12, 마지막3행과 각5case 데이터 내용을 열람',
 'header case_study_no/answer/query/query_source와361질의 행이 있다. 이 수는 논문 선별361질의와 맞는다. 정답은 함수/매개변수 식별자 목록이다. 개인 식별자·소요시간·미완료 필드는 없다.',
 '883개 수집 중 선별된361개만 공개되어 제외522개를 감사할 수 없다.361질의를361사람으로 세지 않는다. 실험시간 효과의 raw data가 아니다. 모든행을 사람이 수동 이중코딩한 것은 아니다.',
 'ROOT-CODEMEND-2016','original_artifact','cm-eval-gt-2.csv',artifact_scope='filtered crowd query ground truth',study_version_verified='361 count +5 cases match paper; exact run unknown')
source('Rt-A04','original_artifact','CodeMend original benchmark scoring procedure',G+'codemend/models/eval2.py',G+'codemend/models/eval2.py','2016','lines1–74,105–168,170–235: input parse, ranking/miss rule, denominator and log fields',
 'eval-gt-2.csvを読み、正答候補集合に一致する最上位順位を採る。見つからない場合0、MRR・top-k命中を全query数で割る。result logにquery/answer/rankを出力する。独立の採点手順としてデータ表と分ける。',
 'IRスコア用のコードであり人の完了時間・再作業を採点しない。原著Table5のR@kに対しコード名はP@kだが実装は1queryあたりhit。モデル・backupファイルを取得して実行したわけではない。',
 'ROOT-CODEMEND-2016','original_artifact','cm-eval2.py',artifact_scope='original IR scoring codebook, not human time record',study_version_verified='public code semantics checked; exact paper run not reproduced')
# Keep source prose Korean; above source code note translated explicitly.
sources[-1]['verified_content']='eval-gt-2.csv를 읽어 정답 후보 집합과 일치하는 최상위 순위를 사용한다. 없으면0, MRR·top-k hit를 전체 질의 수로 나눈다. query/answer/rank 로그 필드를 정의한다. 데이터 자체와 독립인 원 채점 절차다.'
sources[-1]['limitations']='IR 점수 코드이며 사람 완료시간·재작업 채점표가 아니다. 원문 Table5의 R@k와 달리 코드 변수는 P@k지만 구현은 질의당 hit이다. 모델·backup 의존 파일을 확보해 실행한 것은 아니다.'
for x in sources:
 x['claim_ids']=x.pop('claim_ids_override', ['Cr-06'] if x['type']=='original_artifact' else [])
(R/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
rows=[]
def study(id,fam,src,exp,arm,n,**kw):
 rows.append(dict(study_row_id=id,study_family=fam,source_id=src,experiment_id=exp,arm=arm,participants_arm=n,**kw))
common=dict(locator='PDF p.8–9, Table1',comparison_grade='R',directness='B',participants_total=20,allocation_unit='사람 간 무작위',trials_total=40,recruitment='local pool;18세이상 영어유창 프로그래밍경험;20명,탈락기재없음',expertise='평균8.8년;13명 직업경험/7명 대학경험',prior_solution_knowledge='과제해법 친숙도 미측정',task='JS 호출방식/REST 생성갱신 trade-off 근거 수집·표작성 각1회;이후 자유문제 task3는 무대조',timing='과제 전 도구훈련 뒤 정해진 웹 원문 수집',cointerventions='표·snippet 캡처/링크/요약UI, GoogleDocs와 다른 도구;실험군먼저15분훈련',time_method='화면기록;도구 직접조작 시간/전체 과제시간 비중',time_stop_rule='스스로 완료/더 진전없음 판단',quality_rule='완료 여부, feature사용 통계;표 내용 독립품질 점수 없음',followup_rework='제3무대조 과제 P3 1주 사용 인터뷰만;수정량·대조 없음',link_display_open_adopt='snippet URL/timestamp 보존;처음2과제 채택/구현 관측안함;3명자유과제 선택전환 보고',shared_caveat='보고45% overhead감소와 반올림평균25/44 재산식43.18%는 다름;총시간 절감 아님',participants_assigned_total=20,participants_completed_total=20)
for id,arm,mean,sd in [('Tr-01','Unakite',.25,.07),('Tr-02','Google Docs',.44,.12)]:
 study(id,'ROOT-UNAKITE-2019','Rt-S01','UNAKITE1',arm,None,results={'overhead_fraction_mean':mean,'overhead_fraction_sd':sd,'all_complete':True},**common)
common=dict(locator='PDF p.9, Figure6',comparison_grade='R',directness='B',participants_total=16,allocation_unit='동일인2과제/조건교차,순서균형',trials_total=32,recruitment='별도16명,연구1중복없음;분석탈락없음',expertise='평균7.8년;주제/Unakite모두비친숙',prior_solution_knowledge='두 주제와 도구 모두 비친숙하다고 보고',task='numpy array vs matrix/Python2.7;vs Python list/array 선택의 정당한 설명3개',timing='과제 전에10분훈련,한조건에 미리 만든표 제공',cointerventions='동일 원문집합의 사전 선별·구조화·요약·snippet repository와UI',time_method='전 연구와 동일 화면기록 setup;과제에서 정당한 설명3개까지초',time_stop_rule='두 연구자가 합의한 gold standard 설명3개',quality_rule='동일3개정당설명 종점,16명전원 두조건달성;일반설계품질 동등성시험아님',followup_rework='후속재작업 비교 없음',link_display_open_adopt='표/원문조건 제공,개별링크열람이나실제개발채택은 별도관측안함',shared_caveat='paired covariance/raw없음. 보고ANOVA df1,26;16명에서의 분석세부 재현불가',participants_assigned_total=16,participants_completed_total=16)
for id,arm,mean,sd in [('Tr-03','Unakite prebuilt table',114.63,38.91),('Tr-04','same source webpages',332.56,56.26)]:
 study(id,'ROOT-UNAKITE-2019','Rt-S01','UNAKITE2',arm,16,trials_arm=16,results={'time_mean_s':mean,'time_sd_s':sd,'completion_n':16},**common)
common=dict(locator='PDF p.9 Lab User Study',comparison_grade='R',directness='B',participants_total=20,allocation_unit='동일인2조건교차,과제/순서균형',trials_total=40,subtasks_total=120,recruitment='CS/IS등19대학원1학부,숙련도로제외안함',expertise='Python6expert/9intermediate/5beginner;matplotlib2/7/7/4never,자가보고',prior_solution_knowledge='Python/API숙련도와는 별개;해법사전인지 미측정',task='bar/pie각3누적변경;최초그림을 목표그림처럼 수정',timing='공통데모+interactive tutorial 후 요청시 검색/제안',cointerventions='NL+코드모델·추천·삽입·하이라이트·preview와Google;baseline은Google만',time_method='모든상호작용 로그;subtask 완료초 평균;정확 시작과실패시간 포함 미기재',time_stop_rule='목표그림완료,시간한도/중단상세 미기재',quality_rule='목표그림완성;맹검독립채점·일반품질동등성 없음',followup_rework='3단계변경은초기과제;첫설계채택후의재작업추적없음',link_display_open_adopt='Google쿼리평균1.5대5.5;예제채택/URL열람 전체로그공개 미확인',shared_caveat='미완료분모/SD/paired raw없음;분석시간은완료subtask조건부일가능성',participants_assigned_total=20,participants_completed_total='사람별전체완료 미확인')
for id,arm,mean,complete in [('Tr-05','CodeMend + Google',108.70,46),('Tr-06','Google only',134.12,41)]:
 study(id,'ROOT-CODEMEND-2016','Rt-S02','CODEMEND-LAB',arm,20,trials_arm=20,subtasks_assigned_arm=60,subtasks_denominator_basis='20participants×3protocolsubtasks;derived',results={'time_mean_s':mean,'completed_subtasks':complete,'time_significance':'not significant;no exact p/SD'},**common)
(R/'studies.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
effects=[]
def effect(id,fam,src,url,loc,outcome,orig,inputs,formula,result,unc,noncomp,reversal,claim,**kw):
 effects.append(dict(comparison_id=id,study_family=fam,source_id=src,source_url=url,locator=loc,outcome=outcome,original=orig,input=inputs,formula=formula,result=result,uncertainty=unc,noncompletion=noncomp,reversal_condition=reversal,calculation_status='descriptive_recalculation',claim_id=claim,**kw))
effect('Er-01','ROOT-UNAKITE-2019','Rt-S01',U,'p.9 Fig6','3 gold-standard explanationsまでの秒','mean114.63 SD38.91 vs332.56 SD56.26;F(1,26)=25.59,p<.001',{'intervention':114.63,'control':332.56,'n_people':16,'n_trials':32,'unit':'s'},'delta=I-C;ratio=I/C;change_pct=100*(I-C)/C',{'delta':114.63-332.56,'ratio':114.63/332.56,'change_pct':100*(114.63-332.56)/332.56},'paired raw/covarianceなし;CI未計算;報告Fのみ','16/16各条件達成','新設計/完全実装/長期更新で必要品質や構築費が異なれば適用不可','Cr-01')
effects[-1].update(outcome='gold-standard 설명3개까지초',uncertainty='paired raw/공분산 없어 CI미계산;보고F만 보존',noncompletion='16/16 각조건달성',reversal_condition='새설계/전체구현/장기갱신에서 필요품질·표작성비가 다르면 적용불가')
effect('Er-02','ROOT-UNAKITE-2019','Rt-S01',U,'pp.8–9','overhead fraction','25% SD.07 vs44% SD.12;reported45% reduction;model coef−.22',{'intervention':.25,'control':.44,'n_people_total':20,'unit':'fraction'},'delta_pp=100*(I-C);relative_pct=100*(I-C)/C',{'delta_pp':-19.0,'relative_pct':100*(.25-.44)/.44},'반올림평균기반;보고45%의원자료/가중법 미확인','20/20두과제완료;군별n미기재','정리시간비중감소에도총과제시간증가가능','Cr-02')
effect('Er-03','ROOT-CODEMEND-2016','Rt-S02',C,'p.9','subtask time','108.70 vs134.12 seconds;46 vs41subtasks completed;not significant',{'intervention':108.70,'control':134.12,'n_people':20,'assigned_subtasks_each':60,'completed_I':46,'completed_C':41,'unit':'s'},'delta=I-C;relative_pct=100*(I-C)/C',{'delta':108.7-134.12,'relative_pct':100*(108.7-134.12)/134.12,'completion_delta_pp':100*(46-41)/60},'SD/pairedraw없고완료subtask시간분모미기재;CI불가.비유의=동등아님','60각조건은프로토콜유도.46/41완료,시간평균에미완료포함미확인','완료자선택,학습,도구훈련/실패시간포함시시간차변경가능','Cr-04')
(R/'effects.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in effects))
sc=[]
for s in sources:
 sc.append(dict(screening_id='SCR-'+s['source_id'],source_id=s['source_id'],study_family=s['study_family'],title=s['title'],url=s['fixed_url'],discovery_path='supplemental primary/artifact search',decision='include',reason='primary human tool study' if s['type']=='primary_human_study' else 'paper-linked original independent repository artifact; scope limits retained',full_text_read=True,category=s['count_category']))
# Public eval1..5 are read but belong to stimulus variants; not five additional originals.
sc.append(dict(screening_id='SCR-RT-CM-EVALS',source_id='',study_family='ROOT-CODEMEND-2016',title='CodeMend eval1.py..eval5.py demo code samples',url=G+'codemend/demo/code-samples/',decision='exclude_from_minimum',reason='same chart-family stimulus variants; final lab mapping uncertain;not count each source file as independent experiment artifact',full_text_read=True,category='related_code'))
(R/'screening.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sc))
# Record exactly what was counted/reproduced in the public CSV; no model execution.
p=R/'tmp/cm-eval-gt-2.csv'; data=list(csv.DictReader(p.open()))
from collections import Counter
receipt={'input_url':G+'codemend/models/eval-gt-2.csv','input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'rows':len(data),'columns':list(data[0]),'case_counts':dict(Counter(x['case_study_no'] for x in data)),'query_source_counts':dict(Counter(x['query_source'] for x in data)),'missing_time_columns':True,'labor_outcome_reproduced':False,'method':'csv.DictReader structural count only; no model or human experiment executed'}
(R/'artifact-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print({'sources':len(sources),'study_rows':len(rows),'effects':len(effects),'artifact_corpus_rows':len(data)})
