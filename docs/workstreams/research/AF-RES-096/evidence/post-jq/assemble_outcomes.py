import collections,datetime,hashlib,json,pathlib
P=pathlib.Path(__file__).resolve().parents[2];O=P/'evidence/post-jq'
raw=[x for x in json.loads((P/'evidence/outcomes/public-records.json').read_text()) if x['case_id'].startswith('J')]
reads=[json.loads(x) for x in (O/'public-read-log.jsonl').read_text().splitlines()]
revtimes=json.loads((O/'answer-revision-times.json').read_text());runtime=json.loads((O/'runtime-results.json').read_text())
def utc(e):return datetime.datetime.fromtimestamp(e,datetime.timezone.utc).isoformat() if e is not None else None
M='https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml'
G='https://git.savannah.gnu.org/cgit/grep.git/tree/doc/grep.in.1?h=v3.11'
details={
'J1':{
 'first_answer_summary':'채택 첫답은 부모 startTime 배열과 각 자식 one/two 배열을 더한 뒤 join하는 jq filter를 제안한다. 사전 변수-binding 해법과 코드는 다르지만 같은 부모 문맥을 유지한다. 답에는 독립 실행판·완전 입력·출력 기록이 없다.',
 'answer_revision_summary':'본문 revision 1 하나; 마지막 수정 시각 없음.',
 'execution_fields':{'input':'질문 R0는 JSON 닫힘이 누락된 조각','command':'답변자가 .data[] → [.startTime] + child tuple → join 조합을 제안','version':'질문자·답변자 jq판 미확인','output':'질문에는 실패 출력; 채택 답 자체에는 성공 stdout 없음','attribution':'답변자 코드 제안과 현재 채택표시; 질문자 성공실행 로그 아님'},
 'agreement_with_frozen':'A/B 완결 판정과 기능상 일치. 공개 답의 join 조합과 사전 binding 조합은 서로 다른 주 도구 내부 경로이다. 현재 채택은 완전 입력 실행 검증을 대신하지 않는다.',
 'post_links':[{'url':M,'purpose':'배열/변수 binding 및 string interpolation 명세','perspective':'maintainer'},{'url':'https://stackoverflow.com/a/79322532','purpose':'짧은 join 기반 대안','perspective':'asker'}],
 'keep_or_change_reason':'기본 공식 manual 링크를 유지하고, 긴 원 시험 링크 대신 짧은 공개 대안 링크를 두 번째에 제시할 수 있다. 사후 링크이며 사전 근거를 대체하지 않는다.',
 'ask_one':'잘린 JSON의 닫힘을 포함한 최소 완전 입력을 줄 수 있는가?',
 'limitations':['현재 채택 시점은 알 수 없다.','작성자 댓글·생성 이후 본문수정이 관측되지 않아 실제 사용 성공은 미확인.','로컬 최소 문법수리 입력의 성공은 원 게시자 실행 증거가 아니다.']},
'J2':{
 'first_answer_summary':'현재 채택 첫답은 .modules.data 전체를 유지하고 title/tracks 내부에서 각각 순회하도록 바꾼다. title/artist는 원 시도와 같은 primary/secondary 순서이고 .offset.start/end를 그대로 참조한다. 다른 첫답은 INDEX(.id)로 분기 자료를 매핑하며 실제 제시 출력에 start/end=null이 남는다.',
 'answer_revision_summary':'채택 답 revision 2는 두 부분 객체에 empty가 생기면 전체 출력이 없어진다는 설명을 추가했다. 새 offset 입력이나 성공 출력은 추가하지 않았다. INDEX 답 revision 1 하나.',
 'execution_fields':{'input':'원 질문의 유효 JSON에는 offset 객체가 없다; 제목은 기대표기와도 다르다','command':'채택 답의 object 내부 iteration, 비채택 답의 INDEX(.id)','version':'INDEX 답은 함수가 v1.6부터 있다고 설명하나 질문자 사용판은 미확인','output':'비채택 답이 null offset을 가진 출력 제공; 채택 답에는 exact stdout 없음','attribution':'질문자는 채택 답에 수정되는 듯하다고 긍정했지만 데이터·판·출력 동반 실행보고는 아님'},
 'agreement_with_frozen':'사전 A/B 부분 판정을 유지한다. 공개 긍정과 채택은 핵심 객체결합 문제의 해결 지표이지만 모든 명시 출력값의 완결 증거와 불일치한다. null 출력은 입력결손 판정을 지지한다.',
 'post_links':[{'url':M,'purpose':'객체 생성 시 input 문맥과 missing key=null 명세','perspective':'maintainer'},{'url':'https://stackoverflow.com/a/79389173','purpose':'INDEX 대안과 null offset을 숨기지 않은 구체 출력','perspective':'asker'}],
 'keep_or_change_reason':'cat 링크는 완결값을 보충하지 못하므로 사용자용 두 링크에서는 공식 jq 설명+INDEX 출력 대안으로 바꾼다. 채택답/질문자 반응은 outcomes 근거로 보존하되 제품 카드는 offset 결손을 설명한다.',
 'ask_one':'offset 수치와 title/artist 정규화 규칙을 포함한 완전 입력을 줄 수 있는가?',
 'limitations':['질문자 긍정의 대상이 객체결합만인지 누락된 실제 데이터까지인지 미확인.','채택 시각이 알려져 있지 않다.','공개 댓글의 설명과 INDEX 출력을 로컬 직접 실행한 것으로 기록하지 않는다.']},
'J3':{
 'first_answer_summary':'채택 첫답은 undocumented _nwise(2)로 두 항목씩 묶고 add하는 jq 내부 기능을 제시하며 단순 배열 기대출력을 제공한다. 이후 while(length > 0; .[2:])[:2]와 add를 쓰는 문서화된 연산 조합을 추가했다.',
 'answer_revision_summary':'revision 2가 undocumented 함수에 의존하지 않는 while/slicing 대안을 추가했고 revision 3은 jq 명령·설명 형태를 다듬었다. 세 revision 모두 질문 생성 후 30일 안이다.',
 'execution_fields':{'input':'질문/답의 단순 배열 [a,b,c,d]; 실제 Overpass JSON 전체·전처리는 없음','command':'답변자의 _nwise+add; 수정판의 while/slice+add','version':'질문자 사용 jq판은 미확인; _nwise 안정 API 보장은 답도 주장하지 않음','output':'답변자가 [ab,cd]를 제시','attribution':'질문자는 실제 사례가 더 복잡하고 merge 전 변형이 필요하지만 같은 접근이 작동한다고 보고. 정확 명령/입력/판/출력 묶음은 없음'},
 'agreement_with_frozen':'A/B 완결과 jq-only 해결 방향은 일치한다. 그러나 공개 선택은 사전 range/index 조합과 다른 함수·절이다. 인접 Overpass가 필요했다는 증거는 없다.',
 'post_links':[{'url':M,'purpose':'공식 range/index/+ 및 while/slice 명세','perspective':'maintainer'},{'url':'https://stackoverflow.com/revisions/8B5D568A-8370-4DA2-8612-FF08869D3144/view-source','purpose':'짧은 _nwise 대안과 문서화된 while 대안이 함께 있는 고정 수정판','perspective':'asker'}],
 'keep_or_change_reason':'공식 manual 유지; 두 번째 링크는 수정판 답으로 교체하면 유지관리자가 private 함수 의존과 documented 대안의 차이를 판단할 수 있다. _nwise가 안정 API인 것처럼 단독 추천하지 않는다.',
 'ask_one':'실제 객체의 merge 전 변형과 중복 key 충돌 규칙을 보여줄 수 있는가?',
 'limitations':['질문자 실제 입력·명령·판·출력은 공개되지 않았다.','현재 채택을 테스트 결과와 동일시하지 않는다.','사후 while/_nwise 발견은 사전 경로에 소급 추가하지 않는다.']},
'J4':{
 'first_answer_summary':'비채택 답은 PCRE 지원 grep을 전제로 재귀 capture group을 사용하는 grep -Po 해법을 제시했다. 쉼표·중첩 대괄호·빈값·반복을 포함한 답변자 입력 및 3개 기대출력이 있다.',
 'answer_revision_summary':'답 revision 1 하나. 질문자는 30일 내 두 차례 본문을 수정하여 실제처럼 보이는 쉼표 포함 입력을 추가했고 마지막 수정에서 일부 중첩 예시를 삭제했다. 평가 요구는 계속 R0에 고정한다.',
 'execution_fields':{'input':'R0 line+empty; 수정 질문은 실제처럼 보이는 SpecificWord 필드를 추가; 답변자는 별도 합성 test.txt 제공','command':'답변자 grep -Po recursive PCRE; 질문자는 기존 adb|grep 파이프라인만 제시','version':'질문자 grep판/PCRE 지원 미확인; 답은 -P 필요를 명시','output':'답변자가 3줄 결과 제공, 질문자의 성공 stdout 없음','attribution':'답변자 재현 주장과 연구자 jq 1.7.1 로컬 실행을 별도 기록; 질문자 실행 확인 아님'},
 'agreement_with_frozen':'사전 A/B 완결은 고정된 literal-balanced 괄호 범위의 합성 jq 해법으로 남는다. 사후 공개 답은 인접 grep의 짧은 대안을 보여주지만 B의 노출·반환 원문에서 발견된 완성 해법은 아니며 B 승리로 재분류할 수 없다.',
 'post_links':[{'url':G,'purpose':'grep의 -P/-o 지원 조건과 출력 경계','perspective':'maintainer'},{'url':'https://stackoverflow.com/a/79426171','purpose':'재귀 PCRE의 짧은 명령과 별도 시험 입력/출력','perspective':'asker'}],
 'keep_or_change_reason':'PCRE 지원 및 bracket 문법을 확인할 수 있으면 사용자 카드에는 훨씬 짧은 grep 대안을 제시할 수 있다. 미확인 환경에는 검증된 jq 합성 filter와 공식 manual을 대안으로 남긴다. 사전 B 문서가 재귀 구문 자체를 입증했다고 주장하지 않는다.',
 'ask_one':'모든 대괄호가 균형을 이루고 escape/quoted bracket이 없다는 점과 grep -P 지원을 확인할 수 있는가?',
 'limitations':['질문자는 괄호가 맞고 escape되지 않는다고 추정했을 뿐 확정 명세를 제공하지 않았다.','현재 채택답 없음, 30일 내 해결 성공후속 없음.','30일 뒤의 댓글 한 건은 제3자 잡담으로 실행 성과가 아니다.','원 질문은 반복을 허용하지만 marker가 payload 안에 있는 문법은 지정하지 않아 합성 filter의 그 경우는 미검증이다.','실제 범위밖 경계시험 specificword=["]"] status=ok에서는 quoted ]를 구조괄호로 처리하여 조기절단했다. JSON quoting semantics는 R0에 없는 추가 전제이다; escaping은 실행하지 않았고 미확인으로 남긴다.']}
}
comment_summaries={
140003033:'질문자가 URI select 두 개는 작동하는데 다른 branch를 함께 추출하지 못하는 이유를 질문했다.',
140003480:'질문자가 채택 답의 변경으로 수정되는 듯하다고 긍정하고 동작 원리 설명을 요청했다; 판/출력/전체입력은 없다.',
140003860:'제3자가 외부 iteration과 object 내부별 iteration의 차이를 설명했다.',
140003878:'제3자가 INDEX로 참조를 수집하는 대안을 소개했다.',
140003837:'제3자가 title/tracks는 각각 동일 .modules.data 전체를 입력으로 받는다고 설명했다.',
140005591:'질문자가 실제 사례는 merge 전 변형이 더 필요하지만 같은 접근이 작동한다고 보고했다; 구체 재현은 없다.',
140045222:'제3자가 쉼표 전까지의 단순 grep 패턴을 제안했다.',
140048144:'제3자가 내부 쉼표·unmatched/escaped ] 여부를 물으며 실제 문법에 따라 답이 달라진다고 지적했다.',
140049230:'질문자가 기존 제안은 빈값에 실패한다고 주장하고, 괄호는 맞고 escape되지 않는 것으로 생각한다고 했다.',
140049294:'질문자가 쉼표 포함 SpecificWord와 빈값을 본문에 추가했다고 알렸다.',
140050229:'제3자가 adb의 실제 입력과 원하는 출력을 요청했다.',
140053637:'제3자가 빈값 실패 주장에 반박하고 내부 쉼표 때문에 제안패턴이 충분하지 않다고 설명했다; 괄호문법 확정을 요구했다.',
140053687:'제3자가 중첩 대괄호를 포함한 복사 가능한 최소 재현 입력과 기대출력을 요청했다.',
140331693:'30일 이후 제3자의 사교적 댓글. 요청 해결/실행에 관한 근거가 아니다.'}
result=[]
for x in raw:
 d={'case_id':x['case_id'],'question_id':x['question_id'],'question_creation_utc':utc(x['question_creation_epoch']),'deadline_30d_utc':utc(x['deadline_30d_epoch']),'answer_ids':[a['answer_id'] for a in x['answers']],'accepted_now':x['current_accepted_answer_id'],'acceptance_timestamp':'미확인; API current marker only',**details[x['case_id']]}
 d['answer_dates']=[{'answer_id':a['answer_id'],'created_utc':utc(a['creation_epoch']),'first_body_utc':utc(a['first_revision_epoch']),'last_edit_utc':utc(a['last_edit_epoch']),'accepted_now':a['current_is_accepted'],'within_30d':a['within_30_days'],'revision_times':[{'number':r['revision_number'],'utc':utc(r['creation_date']),'url':r['url']} for r in revtimes if r['post_id']==a['answer_id']]} for a in x['answers']]
 acts=[]
 for c in x['comments']:
  if c['by_asker'] and c['within_30_days']:acts.append({'type':'asker_comment','id':c['comment_id'],'utc':utc(c['creation_epoch']),'url':c['url'],'summary':comment_summaries[c['comment_id']]})
 for v in x['question_body_revisions']:
  if v['by_asker'] and v['within_30_days'] and v['revision_number']>1:acts.append({'type':'asker_question_revision','revision_number':v['revision_number'],'utc':utc(v['creation_epoch']),'url':v['url'],'summary':('쉼표를 포함한 SpecificWord 입력 및 기대 예시 추가' if v['revision_number']==2 else '일부 중첩/일반 텍스트 기대 예시 삭제와 오타 정정')})
 d['asker_actions_30d']=sorted(acts,key=lambda a:a['utc']);d['asker_followup_observed_30d']=bool(acts);d['asker_self_report_success_30d']=x['case_id'] in ['J2','J3'];d['exact_asker_execution_verified']=False
 d['after_30d_followup']=[{'type':'comment','id':c['comment_id'],'by_asker':c['by_asker'],'utc':utc(c['creation_epoch']),'url':c['url'],'summary':comment_summaries[c['comment_id']]} for c in x['comments'] if not c['within_30_days']]
 d['researcher_runtime_after_seal']={'file':'evidence/post-jq/runtime-results.json','attempts':len([r for r in runtime if r['case_id']==x['case_id']]),'description':{'J1':'原 JSON 조각은 닫힘누락으로 exit5; 연구자가 문법만 닫은 입력에서는 봉인 filter의 3줄 출력 일치.','J2':'미실시; offset 입력결손을 추가 실행으로 고칠 수 없어 불필요한 실행을 하지 않았다.','J3':'봉인 .elements filter는 연구자 envelope 입력에서 성공; 원 단순배열에는 .elements만 제거한 별도 사후 변형으로 성공.','J4':'A/B 봉인 filter 바이트 일치 확인 후 원R0+범위내4벡터 각4 총8실행은 모두 exit0·기대출력일치. 별도 범위밖 quoted-bracket 1개는 exit0이지만 첫 quoted ]에서 조기절단하여 추가 JSON-quoting 기대출력 불일치. 사전승패는 변경하지 않음.'}[x['case_id']]}
 d['frozen_judgments']={r:json.loads((P/f"evidence/routes/{x['case_id']}-{r}/judgment.json").read_text())['judgment'] for r in 'AB'}
 d['frozen_verdict_changed']=False;d['post_budget']='All public outcome reading and runtime are auxiliary after remote seal2; excluded from each 2-search/4-open route budget.';d['review_completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();d['seal2_remote_sha']='d03ca37daf0c43688c68bc39417d84a9b84803e9'
 assert len(d['post_links'])<=2;result.append(d)
(O/'outcomes.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
# A source ledger row for each actually read original work; repeated revisions retain event identity.
source_rows=[]
for r in reads:
 m=r['metadata'];case=r['case_id'];kind=r['kind'];sid=f"POST-{case}-"+({'first_answer':f"A{m.get('answer_id')}",'comment':f"C{m.get('comment_id')}",'question_revision':f"Q{m.get('revision_number')}"}[kind])
 if kind=='comment':content=comment_summaries[m['comment_id']]
 elif kind=='first_answer':content={79322532:'부모 startTime 배열과 각 자식 tuple 배열을 더하고 join하는 filter. 실행판/독립 성공 stdout 없음.',79388975:'modules.data 전체에서 객체를 만들고 각 title/tracks 값 내부에서 별도 순회한다. offset은 여전히 존재하지 않는 경로를 읽고 title/artist 순서는 원 시도와 같다. 첫판에는 별도 출력/해설 없음.',79389173:'INDEX(.id)로 id별 참조를 만든다. 답의 출력은 title/artist를 원 시도대로 매핑하고 start/end가 null이다.',79389420:'최초답은 undocumented _nwise(2)와 add 조합 및 ab/cd 기대출력만 제시한다. while 대안은 이후 수정에서 추가된다.',79426171:'PCRE를 지원하는 grep -Po와 재귀 capture group 패턴을 제시한다. 쉼표·중첩·빈값·반복을 포함한 답변자 test.txt와 3줄 출력이 있다.'}[m['answer_id']]
 else:content=('원 최초 질문 재확인; 기존 R0 자료와 동일 원문이므로 독립 하한에 다시 세지 않음.' if m['revision_number']==1 else ('J3: 제3자 문장·JSON 표기 수정; 조건 추가 없음.' if case=='J3' else ('J4 revision2: 쉼표 포함 SpecificWord 입력과 기대예시 추가. 기존 중첩/빈값 예시도 보존.' if m['revision_number']==2 else 'J4 revision3: 중첩/일반텍스트 기대예시 두 개 삭제와 오타 정정. R0 요구의 사전평가는 바꾸지 않음.')))
 qid=next(x['question_id'] for x in raw if x['case_id']==case)
 source_rows.append({'source_id':sid,'original_url':r['url'],'reread_url':r['url'],'published_utc':utc(m['created']),'checked_utc':r['checked_utc'],'version_revision':m.get('first_guid',m.get('guid',m.get('comment_id'))),'body_sha256':r['sha256'],'directly_verified':content,'supports_or_refutes':'Q6: 사후 공개 자료와 사전 문서완결을 구별한다.','limitations':'현재 보존 API 본문; 삭제된 댓글/답이나 grace-period 수정은 확인할 수 없다. 채택표시는 실행로그가 아니다.','authorship_lineage':f"Stack Overflow question {qid} discussion",'event_lineage':f'SO-question-{qid}','minimum_count_eligible':False,'minimum_count_reason':'후속 답/댓글은 별도 추적; R0 재열람은 중복.','outside_frozen_route_budget':True,'access_method':'루트가 공개 Stack Exchange API에서 수집한 원문 캐시를 직접 읽음; body hash와 최초열람시각 보존.'})
for r in revtimes:
 if r['revision_number']<=1:continue
 case='J2' if r['post_id']==79388975 else 'J3';qid=next(x['question_id'] for x in raw if x['case_id']==case)
 source_rows.append({'source_id':f"POST-{case}-A{r['post_id']}-R{r['revision_number']}",'original_url':r['url'],'reread_url':r['url'],'published_utc':utc(r['creation_date']),'checked_utc':r['read_utc'],'version_revision':r['revision_guid'],'body_sha256':r['body_sha256'],'directly_verified':('J2 revision2는 empty가 포함된 객체 생성이 전체 empty가 되는 이유를 추가설명한다. 입력 offset 추가나 실제 stdout은 없다.' if case=='J2' else ('J3 revision2는 undocumented _nwise 대신 while/slicing/add 대안을 추가한다.' if r['revision_number']==2 else 'J3 revision3은 jq 호출과 here-string 입력을 명시하고 while/slicing 설명을 다듬는다.')),'supports_or_refutes':'Q6: 최초답과 수정 후 추가근거의 시간 구분.','limitations':'같은 답의 수정은 새로운 독립 사건 또는 최소자료로 세지 않음.','authorship_lineage':f"SO answer {r['post_id']}",'event_lineage':f'SO-question-{qid}','minimum_count_eligible':False,'outside_frozen_route_budget':True})
release=json.loads((O/'release-metadata.json').read_text());down=json.loads((O/'download-record.json').read_text());env=json.loads((O/'runtime-environment.json').read_text())
source_rows.append({'source_id':'POST-JQ171-RELEASE','original_url':release['source_url'],'reread_url':release['html_url'],'published_utc':release['published_at'],'checked_utc':release['retrieved_utc'],'version_revision':'jq-1.7.1; source commit 71c2ab509a8628dbbad4bc7b3f98a64aa90d3297','directly_verified':'공식 릴리스의 published 시각과 Linux amd64 자산·checksum 파일의 URL/크기/생성시각을 확인했다. API asset digest는 null이다.','supports_or_refutes':'사후 exact-version 연구자 실행의 출처 검증.','limitations':'사용자 당시 설치판을 밝히지 않음. 서명검증이 아닌 동일 공식 릴리스 checksum 확인.','authorship_lineage':'jqlang/jq maintainers','event_lineage':'jqlang/jq@jq-1.7.1','minimum_count_eligible':False,'minimum_count_reason':'판·실행 보조 메타자료; 앞선 같은 릴리스 구현과 독립 사건으로 늘리지 않음.','outside_frozen_route_budget':True})
for a in down:
 source_rows.append({'source_id':'POST-JQ171-'+('CHECKSUM' if a['asset']=='sha256sum.txt' else 'BINARY'),'original_url':a['url'],'reread_url':a['url'],'published_utc':next(z['created_at'] for z in release['assets'] if z['name']==a['asset']),'checked_utc':a['checked_utc'],'version_revision':'jq-1.7.1 Linux amd64','body_sha256':a['sha256'],'directly_verified':('checksum 문서의 jq-linux-amd64 행은 '+env['official_checksum_line'] if a['asset']=='sha256sum.txt' else '실행파일의 계산 sha256이 공식 checksum과 일치하고 --version은 jq-1.7.1, --build-configuration은 builtin Oniguruma를 보고했다.'),'supports_or_refutes':'사후 exact-version 연구자 실행 재현.','limitations':'실행산출물은 외부 원 시험 또는 원 작성자 실행이 아니다.','authorship_lineage':'jqlang/jq release assets','event_lineage':'jqlang/jq@jq-1.7.1','minimum_count_eligible':False,'outside_frozen_route_budget':True})
(O/'source-note.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in source_rows))
print(json.dumps({'outcomes':len(result),'source_rows':len(source_rows),'public_read_rows':len(reads),'exact_asker_execution_verified':sum(x['exact_asker_execution_verified'] for x in result),'asker_positive_reports':sum(x['asker_self_report_success_30d'] for x in result),'runtime_runs':len(runtime)},ensure_ascii=False))
