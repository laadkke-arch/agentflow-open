"""Materialize the source-exposed root's manual assessments, six cases per commit.

This is not an automated correctness oracle. Verdicts and reasons below were
written after reading preserved answers and the fixed, separately stored key.
"""
from pathlib import Path
from datetime import datetime,timezone
import csv,json,hashlib,argparse,collections
P=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--batch',type=int,choices=[1,2,3],required=True);args=ap.parse_args()
CORE=['MB01','MB02','MB03','MB04','MB05','MB06','ROR01','ROR02','ROR05','ROR06','ROR07','ROR08','SW01','SW02','SW03','SW05','SW06','WD01']
key={k['event_id']:k for k in json.loads((P/'reconstruction/key/answer-key.json').read_text())['cases']}
events={e['event_id']:e for e in (json.loads(z) for z in (P/'events.jsonl').read_text().splitlines() if z.strip())}
# Each entry: target verdict, function/version/reason verdict, concise target reason,
# concise function reason. PASS is restricted to the provided key's stated scope.
G={
'MB01':[
 ('PARTIAL','PARTIAL','유럽 소장판 의도만; retained와의 일치 미확인','지역 요구는 알지만 matrix·구체 판 부족'),
 ('PARTIAL','PARTIAL','Worldwide 근거판과 유럽 의도의 간극을 보류','DiscID/트랙수로 지역판을 확정하지 않음'),
 ('PARTIAL','PARTIAL','Europe 새 후보와 retained US/Canada를 구분','실물 matrix 없어서 소장판 완전 일치는 보류')],
'MB02':[
 ('PARTIAL','PARTIAL','곡명 불일치를 탐지; 정정 recording 미정','CD3 첫 곡 의도는 복원,5:27/역사범위 부족'),
 ('PARTIAL','PASS','당시 Les Princes 표기를 복원; 올바른 ID 미정','medium3 track1/5:27과 현재 다른 이름을 구별'),
 ('PASS','PASS','La Groupie 원ID와 Les Princes 새ID 구분','CD2/4:39와 CD3/5:27 및 참조복구 범위 복원')],
'MB03':[
 ('PARTIAL','PARTIAL','B4 의도는 읽었지만 retained2:32를 선택','당시 B4판/길이 미확인; 제목 일치로 선택'),
 ('PARTIAL','PARTIAL','B4와recording 길이 차이를 탐지','2:38/2:32 구분, 오케스트라 차이·정정대상 미정'),
 ('PASS','PASS','B4를 새aa574fa3으로 잇는 정정 복원','비오케스트라2:38을 저자진술 범위에서 구분')],
'MB04':[
 ('PASS','PASS','같은URL의 Reamonn Back Again 녹음 식별','7:34 녹음 목적; 특정CD를 추가 요구하지 않음'),
 ('PASS','PASS','과거고정판/현재 recording을 같은목적범위로 복원','ISRC값·7:34와 release공유를 구별'),
 ('PASS','PASS','허용병합 target의 좁은 녹음목적 일치','적용승인과 음원 동일성 검증을 구별')],
'MB05':[
 ('PARTIAL','PARTIAL','Neththara와 oldrelease 의도만 복원','보완 선호는 알지만 누락항목·판 미정'),
 ('PARTIAL','PASS','oldrelease와 다른후보는 알지만 동일판 미정','트랙3·8 및 축약 artist, 보완목적 복원'),
 ('PASS','PASS','명시된source→633a31aa 생존target을 복원','누락보완 후release/medium 병합 범위 구별')],
'MB06':[
 ('PARTIAL','PARTIAL','oldMBID와 현재target만,2024중간판 없음','지문조회목적은 알지만 당시 연결/replica범위 없음'),
 ('PASS','PASS','2024인용ID/target과2026target을 구별','지문조회와 당시target범위 복원; 원인판정 보류'),
 ('PASS','PASS','2024/2026 ID역할 복원;2022즉시target 보류','live/replica와 문제보고/현재관측을 구별')],
'ROR01':[
 ('PARTIAL','PASS','회사 의도만; 당시record상태/중복관계 미정','회사등록·연락 목적을 복원'),
 ('PASS','PASS','v1.55 active/nonprofit 표기와 회사인용을 구별','회사Contacts 사용과 분류의 정확성승인을 분리'),
 ('PASS','PASS','동일회사 중복withdrawn→successor 복원','현실합병 아닌catalog정리라는 목적범위 구별')],
'ROR02':[
 ('PASS','PASS','Pacific Islands Division 단위를 보존','본부로 대체할 근거가 없다고 보류'),
 ('PASS','PASS','본부04x와division01db를 구분','논문소속단위에 맞는division 의도 복원'),
 ('PASS','PASS','기각결정 범위에서division ID유지','적용병합/rollback으로 오인하지 않음')],
'ROR05':[
 ('PARTIAL','PARTIAL','옛 ZFH와 현재문의 목적을 분리','평가시기/후계자료 부족,현재선택 보류'),
 ('PASS','PASS','umbrella기관과EQAR역사기록 식별','2009–2021 평가목적은선택,현재문의는별도보류'),
 ('PASS','PASS','inactive역사기관과네후계를 구별','옛평가기록 유지; 프로그램없는현재문의 보류')],
'ROR06':[
 ('PARTIAL','PARTIAL','SLP캠퍼스 의도만;oldID정합성 미정','캠퍼스단위는 보존하나시점/판 부족'),
 ('PARTIAL','PASS','v1.66의SLP표기 복원;원Puebla경계 미정','당시판의소속주장을재현;정정후적합성 미정'),
 ('PASS','PASS','Puebla parent와SLP child02qmmxm27 구별','본교externalIDs를child로복사하지 않음')],
'ROR07':[
 ('PARTIAL','PARTIAL','스페인Biofisika 의도만;정확한기관ID 미정','기관정보 목적은알지만시점/대상정합성 부족'),
 ('PARTIAL','PASS','v1.38스페인표기는복원;원Italian ID경계 미정','위치/사이트/외부ID의역사기재와정확성을구별'),
 ('PARTIAL','PASS','원Italian ID오염을탐지;Spanish정답ID 보류','과거스페인주장과v1.60잔여location충돌 구별')],
'ROR08':[
 ('PARTIAL','PARTIAL','Netrokona 의도만;oldID정합성 미정','소속기능은알지만시점/판 부족'),
 ('PARTIAL','PASS','당시Netrokona표기와두ID차이복원','외부ID차이를동일/비동일성 확정으로쓰지않음'),
 ('PASS','PASS','Gazipur01fva와Netrokona05ktf를 구별','wrong-ID정정과정상개명alias를 구별')],
'SW01':[
 ('PASS','PASS','TinyFugue tf-50b8라는명시대상 복원','exact패치 재현을불필요하게요구하지않음'),
 ('PASS','PASS','두recipe의같은배포물URL을 확인범위로선택','recipe차이와배포물탐색 대체성을구별'),
 ('PASS','PASS','중복recipe와surviving alias대상 복원','같은배포물목적과설치/bytes미검증 구별')],
'SW02':[
 ('PASS','PASS','libxml++ major3라는좁은대상 복원','major3요구;404를배포물소실로오판하지않음'),
 ('PASS','PASS','고정parent3.2.4를추가로 복원','major3탐색과exactrecipe/현재경로를 구별'),
 ('PASS','PASS','libxml++3→@3 정상rename 구분','같은3.2.4 archive와바뀐recipe필드 구별')],
'SW03':[
 ('PASS','PASS','명시된GNUreadline6.2.4설치대상 복원','주장의재현과recipe실제내용승인 구별'),
 ('PASS','PASS','parent고정gnu-readline recipe 식별','6.2.4역사참조만조건부선택,현재설치는보류'),
 ('PASS','PASS','정정commit의canonicalreadline 식별','정정후에도6.2.4,설치성공과현재latest는별도')],
'SW05':[
 ('PARTIAL','PARTIAL','PostgreSQL이지만당시latest의판 미정','시점없는latest를현재와같다고추정하지않음'),
 ('PASS','PARTIAL','2022recipe14.5와2024oldBrewfile을구별','후속최신판선택/사유를보류'),
 ('PASS','PASS','canonical@14와2024목적@16을구별','libpq동반조건과2024최신판범위 보존')],
'SW06':[
 ('PARTIAL','PARTIAL','CLI목적과현재library불일치탐지','당시0.25.8은미확인;200을기능보존으로보지않음'),
 ('PASS','PASS','oldcombined0.25.8과현재library 구별','generate기능및역사판복원;후계ID는보류'),
 ('PASS','PASS','library/CLI분리와CLI후계 식별','역사0.25.8과consumer개별판요구 구별')],
'WD01':[
 ('PARTIAL','PASS','category 의도만;당시실제statement판 미정','건물그자체가아닌P910역할 구별'),
 ('PASS','PASS','revision936463156의category/기관/건물구별','P910와외부ID가서로다른대상이라는범위 복원'),
 ('PASS','PASS','복구판P910의Q55296215 선택','본체undo와consumerundo의별도범위 구별')]
}
KEY_LIMIT={
'MB01':'SOURCE_MAPPING_INFERENCE;MATRIX_MISSING;EXTRACTION_NOT_RUN',
'MB02':'AUDIO_NOT_TESTED;EXTERNAL_ID_ABSENCE_AUTHOR_STATEMENT',
'MB03':'SOURCE_IDS_NOT_EXPOSED;EXTRACTION_NOT_RUN;AUDIO_AUTHOR_STATEMENT',
'MB04':'SOURCE_ID_NOT_EXPOSED;NO_POST_CORRECTION_KEY;AUDIO_NOT_TESTED',
'MB05':'INDIVIDUAL_EDIT_ACCESS_UNAVAILABLE;NO_INDEPENDENT_PHYSICAL_RELEASE_KEY',
'MB06':'2022_TARGET_NOT_EXPOSED;INTERMEDIATE_CHAIN_INCOMPLETE;REPLICA_COMPLETION_UNVERIFIED',
'ROR01':'FULL_DUMP_NOT_CHECKED;HTTP_UNVERIFIED;CONSUMER_DATES_UNVERIFIED',
'ROR02':'NO_BEFORE_AFTER_DUMP;AFFILIATION_PAPER_NOT_READ',
'ROR05':'PURPOSE_NOT_SPECIFIED;FULL_DUMP_NOT_CHECKED;CONSUMER_DATES_UNVERIFIED',
'ROR06':'PRE_ERROR_SNAPSHOT_MISSING;FULL_DUMP_NOT_CHECKED',
'ROR07':'ATTRIBUTE_CONFLICT_OBSERVED;SPANISH_TARGET_ID_UNVERIFIED;PRE_ERROR_SNAPSHOT_MISSING',
'ROR08':'ISSUER_NOTICE_NOT_READ;FULL_DUMP_NOT_CHECKED',
'SW01':'ARCHIVE_BYTES_NOT_COMPARED;RUNTIME_NOT_RUN',
'SW02':'RUNTIME_NOT_RUN;LIVE_ALIAS_NOT_TESTED',
'SW03':'ORIGINAL_RENAME_ACCESS_UNAVAILABLE;RUNTIME_NOT_RUN',
'SW05':'RUNTIME_NOT_RUN;LATEST_IS_TIME_SCOPED',
'SW06':'RUNTIME_NOT_RUN;CONSUMER_VERSION_CONSTRAINT',
'WD01':'CATEGORY_RESTORE_REVISION_MISSING;INCOMING_GRAPH_NOT_AUDITED'
}
def decision(eid,level,a):
    d=a['destination_decision']
    if eid=='MB03' and level==1:return 'WRONG_FOR_REQUEST','오연결: B4대신retained2:32를선택; B4미검증단서가요청충족을보장하지않음','retained recording for wrong release context'
    if eid=='ROR06' and level==2:return 'HISTORICAL_ONLY','역사v1.66판만선택; 정정후SLP목적지로쓰면부적합. 현재정답단정은아님','historical version restricted; unsafe if reused as corrected ID'
    if eid=='ROR05' and level==2:return 'HISTORICAL_ONLY','EQAR역사평가기록만SELECT;현재문의처는별도보류','none within expressly limited historical scope'
    if eid=='MB01' and level==3:return 'SUPPORTED_CONDITIONAL','Europe후보조건부;실물matrix추가확인필요','no exact physical edition claim'
    if eid=='ROR07' and level==3:return 'SUPPORTED_HOLD','적절한보류:Spanish정답ID미확인','key gap, not proof of loss'
    if eid=='ROR05' and level==3:return 'SUPPORTED_HOLD','적절한보류:후계4개,문의프로그램없음','purpose absent; history alone cannot choose'
    if eid=='SW03' and level==2:return 'HISTORICAL_ONLY','고정된과거recipe만조건부선택;현재/정정설치목적은보류','none within historical recipe scope'
    if d=='HOLD':return 'SUPPORTED_HOLD','보류:표시정보만으로후계/현재적합성확정불가','information withheld by representation; not source loss'
    if d=='CONDITIONAL':return 'SUPPORTED_CONDITIONAL','명시한조건범위에서만후보선택','no unconditional current guarantee'
    return 'SUPPORTED_RECORD_SCOPE','기록의확인범위에서선택;실행·전수복원은미확인','none within the limited record scope'

allrows=[]
for eid in CORE:
 for level in [1,2,3]:
  repaired=eid in ['MB05','SW03']
  rel=f'reconstruction/answers/v4-repair-reader-{level}.json' if repaired else f'reconstruction/answers/v3-reader-{level}.json'
  reader=json.loads((P/rel).read_text());a=next(z for z in reader['answers'] if z['event_id']==eid)
  full=json.loads((P/f'reconstruction/views/v4-view-{level}.json').read_text());card=next(z for z in full['cards'] if z['event_id']==eid)
  t,f,tn,fn=G[eid][level-1];dv,dn,err=decision(eid,level,a)
  row=dict(event_id=eid,representation=level,input_version='v4-repair' if repaired else 'v3-carried-to-v4-identical',reader=reader['reader'],answer_file=rel,answer_input_sha256=reader['read_sha256'],visible_card_sha256=hashlib.sha256(json.dumps(card,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),visible_information=json.dumps(card,ensure_ascii=False),target_answer=a['target_answer'],function_version_reason_answer=a['function_version_reason_answer'],destination_decision=a['destination_decision'],destination_ids=json.dumps(a['destination_ids'],ensure_ascii=False),post_edit_key=key[eid]['post_edit_key'],target_verdict=t,target_assessment=tn,function_version_verdict=f,function_assessment=fn,destination_verdict=dv,destination_assessment=dn,error_or_hold=err,needed_evidence=a['needed_evidence'],reader_uncertainty=a['uncertainty'],key_completeness_limit=KEY_LIMIT[eid],source_ids=';'.join(events[eid]['source_ids']),scorer='/root; source-exposed self-check',scoring_rubric='evidence/scoring-rubric.md',actual_user_misrecommendation='미확인',loss_or_access_rule='missing/withheld/access failure != demonstrated data loss')
  allrows.append(row)

end=args.batch*6;chosen=set(CORE[:end]);subset=[r for r in allrows if r['event_id'] in chosen]
def write(path,rs):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
write(P/'reconstruction.csv',subset)
batchids=set(CORE[(args.batch-1)*6:end]);batch=[r for r in allrows if r['event_id'] in batchids]
write(P/f'comparisons/B0{args.batch}.csv',batch)
citations=list(csv.DictReader((P/'citations.csv').open()));bcs=[c for c in citations if c['event_id'] in batchids]
if bcs:write(P/f'comparisons/B0{args.batch}-citations.csv',bcs)
counts={str(i):dict(collections.Counter(r['destination_decision'] for r in subset if r['representation']==i)) for i in [1,2,3]}
report={'at_utc':datetime.now(timezone.utc).isoformat(),'cumulative_cases':end,'cumulative_rows':len(subset),'batch_cases':sorted(batchids),'batch_rows':len(batch),'reader_decision_counts':counts,'wrong_for_request_rows':[(r['event_id'],r['representation']) for r in subset if r['destination_verdict']=='WRONG_FOR_REQUEST'],'historical_only_rows':[(r['event_id'],r['representation']) for r in subset if r['destination_verdict']=='HISTORICAL_ONLY'],'key_gaps_retained':True,'rates_are_not_operational_estimates':True}
(P/f'comparisons/B0{args.batch}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if args.batch==3:
 (P/'evidence/reconstruction-summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 with (P/'evidence/exposure-log.jsonl').open('a') as f:f.write(json.dumps({'at_utc':report['at_utc'],'actor':'/root','action':'source-exposed self-check after frozen answers; all54 rows compared with key','key_file':'reconstruction/key/answer-key.json','answer_batches':['v3 sixteen cases','v4 repair two cases'],'note':'no external blind scoring; no original file edits'},ensure_ascii=False)+'\n')
print(json.dumps(report,ensure_ascii=False))
