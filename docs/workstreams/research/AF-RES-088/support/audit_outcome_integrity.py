"""Independent metadata audit for AF-RES-088 outcomes; no judgment/semantic edits."""
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict, Counter
from html.parser import HTMLParser
import csv, gzip, hashlib, json, re

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'support'
R1_SEAL='f048885abfbfcca1ffd8840899bf2911cd35da60'
inputs={}
def read(name):
    data=(ROOT/name).read_bytes();inputs[name]=hashlib.sha256(data).hexdigest();return data
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def utc(t):return datetime.fromtimestamp(t,timezone.utc).isoformat().replace('+00:00','Z')
def key(r):return (r['creation_date'],r.get('revision_number',-1),r.get('revision_guid',''))
def role(user,owner_id):
    uid=user.get('user_id')
    if uid==-1:return 'community_bot'
    if uid is None or owner_id is None:return 'unverified_deleted_or_missing_account_id'
    return 'question_author' if uid==owner_id else 'other_editor'

class Representation(HTMLParser):
    def __init__(self,s):
        super().__init__(convert_charrefs=True);self.text=[];self.links=[];self.code=[];self.code_depth=0;self.feed(s)
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        for a in ('href','src'):
            if a in d:self.links.append([tag,a,d[a]])
        if tag=='code':self.code_depth+=1;self.code.append('')
    def handle_endtag(self,tag):
        if tag=='code':self.code_depth=max(0,self.code_depth-1)
    def handle_data(self,data):
        self.text.append(data)
        if self.code_depth:self.code[-1]+=data
    def normalized(self):return re.sub(r'\s+',' ',' '.join(self.text)).strip()

def compare_representations(a,b):
    pa,pb=Representation(a),Representation(b)
    pre_class=lambda s:re.sub(r'<pre\s+class="lang-md prettyprint-override">','<pre>',s)
    return {'raw_equal':a==b,'visible_text_equal':pa.normalized()==pb.normalized(),'link_targets_equal':pa.links==pb.links,'code_texts_equal':pa.code==pb.code,'equal_after_removing_only_lang_md_pre_class':pre_class(a)==pre_class(b)}

packet=json.loads(read('outcome_packet.json'))
frame=list(csv.DictReader(read('frame.csv').decode().splitlines()))
selected=[r for r in frame if r['case_id']]
case_by_qid={int(r['question_id']):r['case_id'] for r in selected}
frame_meta={q['question_id']:q for q in json.loads(read('frame_metadata.json'))}
errors=[];checks=[]
for name,pkey in [('questions','questions'),('answers','answers'),('answer_revisions','answer_revisions'),('comments','comments')]:
    path=f'raw/outcomes/{name}_1.json'
    raw=json.loads(read(path))
    matches=raw['items']==packet[pkey]
    checks.append({'path':path,'items':len(raw['items']),'has_more':raw.get('has_more'),'packet_items_exactly_match':matches})
    if raw.get('has_more') is not False or not matches:errors.append({'kind':'page_end_or_packet_mismatch','path':path})
questions={q['question_id']:q for q in packet['questions']}
answers={a['answer_id']:a for a in packet['answers']}
if set(questions)!=set(case_by_qid):errors.append({'kind':'question_ids_differ_from_selected_frame'})
for qid,q in questions.items():
    if q['creation_date']!=frame_meta[qid]['creation_date']:errors.append({'kind':'question_creation_date_differs_from_frozen_frame','question_id':qid})
answer_ids_by_qid=defaultdict(list)
for a in answers.values():
    answer_ids_by_qid[a['question_id']].append(a['answer_id'])
    if a['question_id'] not in questions:errors.append({'kind':'answer_mapped_to_unselected_question','answer_id':a['answer_id']})
for qid,q in questions.items():
    if q['answer_count']!=len(answer_ids_by_qid[qid]):errors.append({'kind':'current_answer_count_mismatch','question_id':qid})
arevs=defaultdict(list)
for r in packet['answer_revisions']:
    arevs[r['post_id']].append(r)
    if r['post_type']!='answer' or r['post_id'] not in answers:errors.append({'kind':'answer_revision_mapping_error','guid':r['revision_guid']})
if set(arevs)!=set(answers):errors.append({'kind':'missing_or_extra_answer_revision_post_ids'})
guid_counts=Counter(r['revision_guid'] for r in packet['answer_revisions'])
if any(n>1 for n in guid_counts.values()):errors.append({'kind':'duplicate_answer_revision_guid'})
comments=packet['comments'];cids=[c['comment_id'] for c in comments]
if len(cids)!=len(set(cids)):errors.append({'kind':'duplicate_comment_id'})
comment_map=[]
for c in comments:
    if c['post_id'] in questions:qid=c['post_id'];target='question'
    elif c['post_id'] in answers:qid=answers[c['post_id']]['question_id'];target='answer'
    else:
        errors.append({'kind':'orphan_comment','comment_id':c['comment_id'],'post_id':c['post_id']});continue
    comment_map.append({'comment_id':c['comment_id'],'post_id':c['post_id'],'target_type':target,'question_id':qid,'case_id':case_by_qid[qid],'created_utc':utc(c['creation_date']),'within_question_30d':questions[qid]['creation_date']<=c['creation_date']<=questions[qid]['creation_date']+2592000,'owner_user_id':c.get('owner',{}).get('user_id'),'actor_role':role(c.get('owner',{}),questions[qid].get('owner',{}).get('user_id')),'edited_flag':c.get('edited'),'body_sha256':sha(c['body']),'url':f"https://stackoverflow.com/posts/comments/{c['comment_id']}",'wording_temporal_limit':'API supplies current comment text plus original creation time; edited comments do not preserve the initial wording in this packet.'})

answer_audits=[];body_chain_links=0;body_chain_matches=0
for aid,a in sorted(answers.items(),key=lambda pair:(pair[1]['question_id'],pair[1]['creation_date'],pair[0])):
    rr=sorted(arevs[aid],key=key);bodies=[r for r in rr if 'body'in r]
    nums=sorted(r['revision_number']for r in rr if 'revision_number'in r)
    if nums!=list(range(1,max(nums,default=0)+1)):errors.append({'kind':'answer_revision_number_gap','answer_id':aid,'numbers':nums})
    if not bodies:
        errors.append({'kind':'answer_has_no_body_revision','answer_id':aid});continue
    first,last=bodies[0],bodies[-1]
    if first['creation_date']!=a['creation_date']:errors.append({'kind':'answer_initial_revision_creation_mismatch','answer_id':aid})
    previous=None;revrows=[]
    for r in bodies:
        match=None
        if previous is not None:
            body_chain_links+=1;match=r.get('last_body')==previous['body'];body_chain_matches+=int(match)
            if not match:errors.append({'kind':'answer_last_body_chain_mismatch','answer_id':aid,'guid':r['revision_guid']})
        revrows.append({'guid':r['revision_guid'],'revision_number':r.get('revision_number'),'utc':utc(r['creation_date']),'user_id':r.get('user',{}).get('user_id'),'display_name':r.get('user',{}).get('display_name'),'is_rollback':r.get('is_rollback'),'body_sha256':sha(r['body']),'last_body_matches_preceding_body':match,'body_differs_from_preceding':None if previous is None else r['body']!=previous['body']})
        previous=r
    first_diff=compare_representations(first['body'],a['body'])
    latest_diff=compare_representations(last['body'],a['body'])
    if first_diff['raw_equal']:classification='current_equals_first_preserved_body'
    elif len(bodies)>1 and latest_diff['raw_equal']:classification='explicit_later_body_revision_current_matches_latest'
    elif first_diff['equal_after_removing_only_lang_md_pre_class'] and first_diff['visible_text_equal'] and first_diff['link_targets_equal'] and first_diff['code_texts_equal']:classification='pre_class_attribute_only_difference_no_explicit_later_revision'
    else:classification='unexplained_current_vs_history_difference'
    if classification=='unexplained_current_vs_history_difference':errors.append({'kind':classification,'answer_id':aid})
    answer_audits.append({'answer_id':aid,'question_id':a['question_id'],'case_id':case_by_qid[a['question_id']],'created_utc':utc(a['creation_date']),'answer_owner_id':a.get('owner',{}).get('user_id'),'current_is_accepted':a.get('is_accepted'),'accepted_time':'unverified_not_supplied_by_packet','first_guid':first['revision_guid'],'first_revision_number':first.get('revision_number'),'first_revision_utc':utc(first['creation_date']),'first_revision_url':f"https://stackoverflow.com/revisions/{aid}/{first['revision_number']}",'first_revision_sha256':sha(first['body']),'current_body_sha256':sha(a['body']),'latest_guid':last['revision_guid'],'current_matches_first':first_diff['raw_equal'],'current_matches_latest':latest_diff['raw_equal'],'first_current_representation_checks':first_diff,'difference_classification':classification,'difference_cause':'pre.class-only discrepancy is observed; rendering/caching/sanitization cause is not established'if classification.startswith('pre_class')else'not_inferred','revision_count':len(rr),'body_revision_count':len(bodies),'revisions':revrows})

qrevs=defaultdict(list)
for tag in ('jq','pandoc'):
    data=json.loads(gzip.decompress(read(f'sealed/revisions_{tag}_page1.json.gz')))
    for r in data['items']:
        if r['post_id']in questions:qrevs[r['post_id']].append(r)
q_audits=[];edit_events=[]
for f in selected:
    qid=int(f['question_id']);q=questions[qid];created=q['creation_date'];end=created+2592000
    aa=sorted([answers[aid]for aid in answer_ids_by_qid[qid]],key=lambda a:(a['creation_date'],a['answer_id']))
    first=aa[0]if aa else None
    body=sorted([r for r in qrevs[qid]if'body'in r],key=key)
    for r in body[1:]:
        when='no_observed_answer'if first is None else('before'if r['creation_date']<first['creation_date']else('after'if r['creation_date']>first['creation_date']else'same_timestamp'))
        uid=r.get('user',{}).get('user_id');first_uid=None if first is None else first.get('owner',{}).get('user_id')
        edit_events.append({'case_id':f['case_id'],'question_id':qid,'guid':r['revision_guid'],'revision_number':r.get('revision_number'),'utc':utc(r['creation_date']),'within_question_30d':created<=r['creation_date']<=end,'relative_to_first_observed_answer':when,'first_answer_id':None if first is None else first['answer_id'],'seconds_from_first_answer':None if first is None else r['creation_date']-first['creation_date'],'editor_user_id':uid,'editor_display_name':r.get('user',{}).get('display_name'),'editor_role':role(r.get('user',{}),q.get('owner',{}).get('user_id')),'editor_is_first_answer_author':None if uid is None or first_uid is None else uid==first_uid,'is_rollback':bool(r.get('is_rollback')),'causal_claim':'temporal ordering only; no inference that viewing an answer caused the edit'})
    accepted=q.get('accepted_answer_id')
    flagged=[a['answer_id']for a in aa if a.get('is_accepted')]
    if flagged!=([]if accepted is None else[accepted]):errors.append({'kind':'question_accepted_id_vs_answer_flag_mismatch','question_id':qid,'question_accepted_id':accepted,'answer_accepted_flags':flagged})
    cs=[c for c in comment_map if c['question_id']==qid]
    cm30=[c for c in cs if c['within_question_30d']]
    edits=[e for e in edit_events if e['question_id']==qid and e['within_question_30d']]
    q_audits.append({'case_id':f['case_id'],'question_id':qid,'created_utc':utc(created),'window_end_utc_inclusive':utc(end),'current_answer_count':len(aa),'answers_within_30d':sum(created<=a['creation_date']<=end for a in aa),'first_observed_answer_id':None if first is None else first['answer_id'],'first_observed_answer_utc':None if first is None else utc(first['creation_date']),'first_answer_delay_seconds':None if first is None else first['creation_date']-created,'current_accepted_answer_id':accepted,'acceptance_time':'unverified_not_supplied_by_packet','current_comment_count':len(cs),'question_comments_within_30d':sum(c['target_type']=='question'for c in cm30),'answer_comments_within_30d':sum(c['target_type']=='answer'for c in cm30),'all_observed_answers_and_comments_within_30d_count':sum(created<=a['creation_date']<=end for a in aa)+len(cm30),'question_body_edits_within_30d':len(edits),'question_body_edits_before_first_answer':sum(e['relative_to_first_observed_answer']=='before'for e in edits),'question_body_edits_after_first_answer':sum(e['relative_to_first_observed_answer']=='after'for e in edits),'limitations':'Accessible currently returned answers/comments only; deleted responses and comment-edit history are outside this packet. No runtime version or actual execution inferred.'})

within=[e for e in edit_events if e['within_question_30d']]
summary={'question_count':len(questions),'answer_count':len(answers),'answer_revision_count':len(packet['answer_revisions']),'comment_count':len(comments),'all_four_api_pages_complete':all(c['has_more']is False for c in checks),'all_packet_arrays_match_raw_pages':all(c['packet_items_exactly_match']for c in checks),'current_accepted_question_count':sum(q.get('accepted_answer_id')is not None for q in questions.values()),'current_accepted_answer_flags':sum(bool(a.get('is_accepted'))for a in answers.values()),'answer_first_revision_creation_matches':sum(a['created_utc']==a['first_revision_utc']for a in answer_audits),'answer_last_body_links_checked':body_chain_links,'answer_last_body_links_matched':body_chain_matches,'current_not_equal_first_answer_bodies':sum(not a['current_matches_first']for a in answer_audits),'explicitly_revised_answers':sum(a['body_revision_count']>1 for a in answer_audits),'current_not_equal_latest_answer_bodies':sum(not a['current_matches_latest']for a in answer_audits),'pre_class_only_mismatch_count':sum(a['difference_classification'].startswith('pre_class')for a in answer_audits),'edited_comment_flag_count':sum(bool(c.get('edited'))for c in comments),'question_body_edit_events_within_30d':len(within),'question_body_edits_before_first_answer':sum(e['relative_to_first_observed_answer']=='before'for e in within),'question_body_edits_after_first_answer':sum(e['relative_to_first_observed_answer']=='after'for e in within),'question_body_edit_actor_counts':dict(Counter(e['editor_role']for e in within)),'question_body_after_answer_actor_counts':dict(Counter(e['editor_role']for e in within if e['relative_to_first_observed_answer']=='after')),'error_count':len(errors)}
report={'audit_id':'AF-RES-088-OUTCOME-INTEGRITY','performed_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'provided_r1_remote_commit':R1_SEAL,'packet_exposure_after_commit':packet.get('answer_exposure_after_commit'),'audit_scope':'Independent metadata/representation recalculation from frozen local API packets. No independent reacquisition, semantic scoring, acceptance-time reconstruction, or runtime evidence inference.','input_sha256':inputs,'status':'PASS'if not errors else'FAIL','summary':summary,'page_checks':checks,'question_audits':q_audits,'answer_audits':answer_audits,'comment_mapping':comment_map,'question_body_edit_timeline':edit_events,'errors':errors,'limits':['Current acceptance is a snapshot, not an acceptance timestamp.','Current answer count and currently visible comments do not reconstruct deleted responses.','A comment creation date cannot date the currently returned wording when that comment is edited.','PE2 has zero answers within30days but one question comment; do not describe it as no response of any kind.','PN1 answer78260959 has a pre.class-only current-vs-history discrepancy; actual rendering mechanism is unverified.','User runtime version and execution remain unverified unless a separate attributed text/trace establishes them.']}
(OUT/'outcome_integrity_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['# AF-RES-088 사후 응답 메타데이터·표현 무결성 감사','',f"판정 **{report['status']}**, 검사 UTC `{report['performed_utc']}`. 기준으로 전달받은 R1 커밋 `{R1_SEAL}`.",'','원본 공개 API의 저장 응답을 별도로 계산했다. 질문 의미·후보 판정은 평가하지 않았고 주파일·Git을 변경하지 않았다. 새로운 원격 API 재취득이나 독립 이중 코딩이 아니다.','', '## 분모와 무결성','', '| 항목 | 수/판정 |','| --- | --- |']
for label,value in [('질문',len(questions)),('답변',len(answers)),('답변 리비전',len(packet['answer_revisions'])),('댓글',len(comments)),('페이지 종료', '4/4 has_more=false'),('현재 채택',summary['current_accepted_question_count']),('최초답판 시각=답생성시각',str(summary['answer_first_revision_creation_matches'])+'/11'),('답 last_body 연결',str(body_chain_matches)+'/'+str(body_chain_links)),('확인된 오류',len(errors))]:lines.append(f'| {label} | {value} |')
lines+=['','## 질문별 관측 창','', '| 사례 | 현재 답수 | 30일 답수 | 30일 질문댓글/답댓글 | 최초 답 UTC | 현재 채택 답ID | 30일 질문본문수정: 답전/답후 |','| --- | --- | --- | --- | --- | --- | --- |']
for q in q_audits:lines.append(f"| {q['case_id']} | {q['current_answer_count']} | {q['answers_within_30d']} | {q['question_comments_within_30d']}/{q['answer_comments_within_30d']} | {q['first_observed_answer_utc']} | {q['current_accepted_answer_id']} | {q['question_body_edits_before_first_answer']}/{q['question_body_edits_after_first_answer']} |")
lines+=['','PE2는30일 내 **답변0·질문댓글1**이다. 질문댓글138328053은2024-05-11T04:50:59Z에 존재한다. 따라서 댓글을 포함한 무응답으로 보고할 수 없다. 현재는 답변3개가 보이고 첫답78854242가2024-08-09T18:49:42Z에 생성됐다. 삭제된 응답까지 없는 것으로 증명하지 않는다.','', '## 답 최초판 식별','', '| 사례·답ID | 첫 GUID | 첫 UTC | 본문판수 | 현재채택 | 현재본문 비교 |','| --- | --- | --- | --- | --- | --- |']
for a in answer_audits:lines.append(f"| {a['case_id']} / {a['answer_id']} | {a['first_guid']} | {a['first_revision_utc']} | {a['body_revision_count']} | {a['current_is_accepted']} | {a['difference_classification']} |")
lines+=['','## 현재본문과 최초판이 다른 세 건','', '- PN1 답78260959: 보존 리비전은1개뿐이다. 차이는 `<pre class="lang-md prettyprint-override">`와 `<pre>`의class 속성이다. 그 속성만 제거하면 HTML이 같고, 표시텍스트·링크 대상·code텍스트도 같다. 명시 후속본문개정으로 세지 않는다. 렌더링/캐시/정제 중 어떤 원인인지는 이 패킷으로 확인하지 못했다.', '- PE2 답78854242: 실제 판2 GUID B3C475B4-F9D3-48D0-AEC5-B93EE659BE33이 존재하며 현재본문이 판2와 같다. 최초판의 외부 이미지 링크를 설명과 코드 예제로 바꾼 기록이다. 최초답 시각에 현재의 상세 예제가 있었다고 소급하면 안 된다.', '- PE2 답79918498: 실제 판2 GUID E2520566-9CCE-4271-A258-0C580688F2BA가 존재하며 현재본문이 판2와 같다. 최초판 뒤에 다른 extension 링크를 추가했다.','', '## 질문본문수정과 답 선후관계','', f"30일 내 별도 질문본문수정{len(within)}건 중 답전{summary['question_body_edits_before_first_answer']}건, 답후{summary['question_body_edits_after_first_answer']}건이다. 작성 주체 집계는 `{json.dumps(summary['question_body_edit_actor_counts'],ensure_ascii=False)}`다.",'', '| 사례 | 판/GUID | 질문편집 UTC | 첫답 이후 초 | 편집자 | 첫답 작성자와 동일ID |','| --- | --- | --- | --- | --- | --- |']
for e in within:
    if e['relative_to_first_observed_answer']=='after':lines.append(f"| {e['case_id']} | {e['revision_number']} / {e['guid']} | {e['utc']} | {e['seconds_from_first_answer']} | {e['editor_display_name']} / {e['editor_user_id']} / {e['editor_role']} | {e['editor_is_first_answer_author']} |")
lines+=['','두 답후 편집은 모두 질문자 이외의 안정user_id다. 질문자가 답을 본 뒤 해법명을 본문에 추가한 사건으로 바꿔 부르면 안 된다. 선후관계만으로 답이 편집을 유발했다고 주장하지 않는다. JN1의 삭제계정 편집자는stableID가 없어 작성자/타인 확정을 보류했다.','', f"댓글 edited=true 표지는 {summary['edited_comment_flag_count']}/17이다. 현재 댓글문구를 생성시각의 최초 문구로 소급하지 않는다. 채택시각과 실제 실행 프로그램판은 이 API 메타데이터에 없으며 만들지 않았다.",'', '## 재실행','', '```sh','python docs/workstreams/research/AF-RES-088/support/audit_outcome_integrity.py','```','', 'JSON의 input_sha256에 실제 검사 입력을 고정했다. 오류 발견시 종료1, 없으면 종료0. 답11개의 GUID·시각·revision chain과댓글17개의 질문/답 부모 매핑은 JSON에 모두 들어 있다.','', '## 검출 오류','', '```json',json.dumps(errors,ensure_ascii=False,indent=2),'```','']
(OUT/'outcome_integrity_audit.md').write_text('\n'.join(lines))
print(json.dumps({'status':report['status'],'summary':summary,'after_answer_edits':[e for e in within if e['relative_to_first_observed_answer']=='after'],'pe2':next(q for q in q_audits if q['case_id']=='PE2')},ensure_ascii=False,indent=2))
raise SystemExit(0 if not errors else 1)
