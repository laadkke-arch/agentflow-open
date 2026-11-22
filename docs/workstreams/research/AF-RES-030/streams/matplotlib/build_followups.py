"""Post-seal Matplotlib observation ledger, not an execution experiment."""
from pathlib import Path
import csv
import datetime as dt
import hashlib
import json
import re

P = Path(__file__).resolve().parent
NOW = dt.datetime.now(dt.timezone.utc).isoformat()
SEAL = '9de54923257d613359348c8ccee2ff8225c8a0d8'
INITIAL = {r['case_id']: r for r in map(json.loads, (P/'initial.jsonl').read_text().splitlines())}
Q = list(csv.DictReader((P/'questions.csv').open()))
def date(s): return dt.datetime.fromisoformat(s.replace('Z', '+00:00'))
def iso(d): return d.isoformat().replace('+00:00', 'Z')
def issue_html(c):
    text=(P/'cache'/f'{c}-root-page.html').read_text()
    return [json.loads(z) for z in re.findall(r'<script[^>]*type="application/json"[^>]*>(.*?)</script>',text,re.S) if 'issueViewerRoute' in z][0]['payload']['issueViewerRoute']['data']['repository']['issue']
def load_comments(c):
    d=issue_html(c)
    nodes={n['databaseId']:n for e in d['timelineItems']['edges']+d['backTimelineItems']['edges'] if (n:=e['node']).get('__typename')=='IssueComment'}
    api=P/'cache'/f'{c}-comments.json'
    if api.exists(): a=json.loads(api.read_text())
    else: a=[{'id':n['databaseId'],'html_url':n['url'],'created_at':n['createdAt'],'user':n['author'],'author_association':n['authorAssociation'],'body':n['body']} for n in nodes.values()]
    return sorted(a,key=lambda r:r['created_at']),nodes,d

# A human read every below-window message before writing these summaries.
SUMMARY={
1368541658:'NumPy 판을 묻고 지원자는 재현하지 못했다고 말함.',
1368542341:'작성자는 경고 활성화 옵션과 pytest에서의 경고를 자발적으로 보충하고 NumPy1.24.0 출력으로 판을 답함.',
1368556640:'같은 지원자가 이제 재현된다고 확인. 사용자 사용권고나 사용자 실행성공은 아님.',
1376897781:'다른 유지관리자가 colormap 특수값3개와 uint8 범위 문제를 설명하고 modulo 대안을 논의함.',
1379254494:'다른 유지관리자가 실제버그라며 입력을 더 큰 정수형으로 승격해야 한다고 설명.',
1381324519:'출시 전 의존성 deprecation 경고 수리를 희망하는 공급자 일정 의견.',
1369116325:'상태문자 전체 제거를 제안. 사용자에게 묻는 환경/입력 질문 없음.',
1369957180:'관련 addfont 문서/작업이 원목적에 맞는지 평가를 요청.',
1370065191:'작성자가 addfont 시도는 세션 한정이라 영속 목표에 맞지 않는다고 답하고 필요하면 기능요청하겠다고 함. 시도시점 자체는 불명.',
1370331856:'다른 지원자가 fontlist-v330.json 및 검색경로 소스를 설명하며 사용자의 경로는 작동해야 한다고 답함.',
1370332943:'원작성자가 cache 파일 위치와 재생성 방법을 역으로 묻는다.',
1370830375:'다른 지원자가 cache 예상 위치와 MPLCONFIGDIR 영향을 설명. 댓글은53초 뒤 수정됨.',
1370892263:'작성자가 ~/.cache/matplotlib/의 cache를 삭제하니 작동했다고 보고. MPLCONFIGDIR은 비어 있었음. 문서개선 요구는 유지.',
1371139050:'지원자가 공개 cache재생성 API의 필요성을 제안. 작성자 실행과 별개 공급자 설계.',
1371193584:'다른 지원자가 cache위치 문서 또는 공개조회함수를 제안.',
1374892272:'제3자가 get_cachedir와 FAQ를 추가. 최초 작성자의 회수값/실행이 아님.',
1464945971:'67일째 제3자가 별도 custom-font 사례와 접근성 문서제안을 제시. 원작성자 사건 실행으로 합치지 않음.',
1466488174:'첫 지원자가 새 제3자의 문서예시 제안을 지지. 원작성자 목표 후속과 분리.',
1370025244:'pyplot.figure 대신 Figure를 직접 생성하는 공식Tk 예제 링크를 즉시 제시.',
1370981028:'작성자가 Figure로 교체하니 종료문제가 해결되었고 GUI 모양도 달라졌다고 구체적으로 보고.',
1371094215:'지원자 종료선언. 성공근거는 앞 작성자 실행보고이며 종료 자체가 아님.',
2206991348:'pandas timeseries의 ax.clear 고정소스를 제시하고 upstream 쪽에 논의를 돌림. 비시계열은 미검사라 명시.',
2206992828:'작성자가 원문을 더 큰 grid로 수정했다고 밝히고 pandas에 신고할 계획을 말함. 실제 신고/성공 실행은 아직 아님.',
2211377162:'Seaborn legend구현을 설명하고 이전 Seaborn 신고 여부를 묻는 혼합답.',
2245186842:'18일째 제3자인 Seaborn 공급자가 현재 구현이 의도된 선택이라 설명하고 move_legend를 소개. 원작성자 답 아님.',
2245451004:'다른 공급자가 기존Legend의 setter를 설명하고 제3자에게 API 우려를 묻는 논의.',
2245466345:'제3자가 기존Legend에 ncols=3 설정하는 제안을 제시. 실행결과 없음.',
2245467600:'제3자가 pyplot 사용자의 혼란이 남는다는 의견.',
2245475799:'제3자가 Legend.set이 constructor 모든 매개변수를 바꿀 수는 없다고 한계를 추가.',
2245980286:'최초지원자가 artist/legend 자동탐색의 제약과 API개편을 논의. 원작성자 값 회수로 인한 변경 아님.',
2211418254:'draw_idle 즉시시도와 한 GUI toolkit만 쓰는 재현입력 요청을 함께 제시.',
2211433918:'작성자가 loop/close_event를 제거한 새 코드도 약절반 crash라고 보고. Tk와 macosx 혼합은 유지하며 추천 GUI 방식도 역으로 질문.',
2214055492:'같은 지원자가 toolkit 하나로 통일하라는 일반원칙과 event-loop/검출소스를 설명. 실제 혼합충돌 원인은 파고들지 않았다고 제한.',
1496053940:'현재 실행환경이 선언한 패키지판과 같은지 묻고 새conda 환경시험·실패시Cartopy 신고를 동시에 제시.',
1496211688:'작성자가 새 환경을 만들자 정상이라고 보고. 이전환경의 실제 package판은 답하지 않음.',
}

ANALYSIS={
'M01': dict(strict_question=True, broad_question=True, same_variable=True, answer_id=1368542341, answer_class='direct_answer_overlap_current_root_timing_unconfirmed', answer_value='NumPy1.24.0; 조사시 current root1.24와중복하며patch정밀도추가', answer_note='current root는1.24를포함하지만최초본문/제목이력미복원이므로질문전에이미공개됐는지는미확인. 추가 -W always/pytest설정은다른변수의자발적공개. 두정보를한답에받아재현확인을version질문의단독효과로분리할수없음.', change='no_prior_proposal', change_summary='dstansby의 재현불가→재현가능은 명시적 진단상태 변화. 답 전 후보/사용/다음행동 제안이 없고 실제후속 코드수리는 다른 공급자.', support_after=1368556640, execution_success=False, execution_failure=False, full_goal_success=False, acceptance='없음', unknown='원작성자가 공급자PR를 설치해 원래경고가 사라졌는지 미확인', next_material='원작성자의 PR24970 적용후 경고 재실행 로그 또는 같은사건의 공개후속'),
'M02': dict(strict_question=False,broad_question=False,same_variable=False,answer_id=None,answer_class='not_applicable',answer_value=None,answer_note='질문 없음; 원작성자의 뒤댓글도 없음.',change='not_applicable',change_summary='최초 공급자 제안을 PR24869로 구현; 작성자의 정보회수·선택변화 아님.',support_after=None,execution_success=False,execution_failure=False,full_goal_success=False,acceptance='없음',unknown='원작성자가 새toolbar를 실제로 사용했는지 미확인',next_material='원작성자의 PR24869 포함판 사용보고'),
'M03': dict(strict_question=False,broad_question=True,same_variable=False,broad_same_variable=True,answer_id=1370065191,answer_class='candidate_evaluation_direct',answer_value='세션한정 addfont는 매import 영속목표에 부합하지 않음',answer_note='broad 평가질문에는 직접답. 기존환경/입력값 질문 분모에서는 제외. 영속목표는 T0 current root에 이미 있음; 뒤에 만든새선호라고 단정할 수 없음.',change='candidate_switch_other_supporter',change_summary='첫 story645 후보fit질문→작성자거절→다른 tacaswell/oscargus의 cache 경로설명→작성자cache삭제. 같은 지원자 명시연결 기준은 실패.',support_after=1370331856,execution_success=True,execution_failure=False,full_goal_success=False,acceptance='작성자가 해결되었다고 말함; 문서개선 요구 유지',unknown='새 프로세스마다 font발견이 지속되는지 미확인. addfont실패 시도는 질문 전후 시점 미확인.',next_material='원작성자의 새 Python프로세스 재시작 뒤 font발견 확인자료'),
'M04': dict(strict_question=False,broad_question=False,same_variable=False,answer_id=None,answer_class='not_applicable',answer_value=None,answer_note='직접안내 뒤 원작성자가 API교체 성공을 보고. 정보요청은 없음.',change='not_applicable',change_summary='Figure 직접생성이라는 최초안내가 그대로 실행됨.',support_after=None,execution_success=True,execution_failure=False,full_goal_success=True,acceptance='작성자 해결보고',unknown='실제 머신 로그/반복시험은 미확인; 원작성자 보고 수준의 전체 원목표 해결',next_material='원작성자의 Figure교체 후 GUI종료/터미널종료 재현로그'),
'M05': dict(strict_question=False,broad_question=False,same_variable=False,answer_id=None,answer_class='not_applicable',answer_value=None,answer_note='공개댓글0. 무응답이며 접근불능이 아님.',change='not_applicable',change_summary='실질 권고 없음.',support_after=None,execution_success=False,execution_failure=False,full_goal_success=False,acceptance='없음',unknown='원작성자의 후속시도와 hatch문제 해결 미확인',next_material='원작성자의 동일입력으로 pgf판/TeX판을 고정한 후속출력'),
'M06': dict(strict_question=False,broad_question=False,same_variable=False,answer_id=None,answer_class='not_applicable',answer_value=None,answer_note='원작성자는 감사·원문개정·upstream 신고계획을 밝힘. 실제 외부신고 URL/새 성공실행은 없음.',change='not_applicable',change_summary='pandas.clear를 근거로 논의위치를 안내. 이후 권고변경 없음.',support_after=None,execution_success=False,execution_failure=False,full_goal_success=False,acceptance='진단에 말로 동의; 신고계획',unknown='최초원문의 grid/조건과 실제pandas후속신고 미확인',next_material='2024-07-03T18:56:41Z 전 root revision 또는 작성자의 pandas후속 issue URL'),
'M07': dict(strict_question=True,broad_question=True,same_variable=False,answer_id=None,answer_class='no_author_answer',answer_value=None,answer_note='원작성자 GrunCrow 댓글0. 뒤의 mwaskom은 다른 공급자이며 신고여부에 대한 작성자답으로 대체하지 않음.',change='unconfirmed',change_summary='같은 tacaswell의 뒤 API설계논의는 존재하나 회수한 작성자값이 없음. 다른 공급자 move_legend/set(ncols) 제안도 실행 미확인.',support_after=2245980286,execution_success=False,execution_failure=False,full_goal_success=False,acceptance='없음',unknown='Seaborn신고 여부, 제안한 API실제판, 원작성자 다열범례 실행 모두 미확인',next_material='원작성자의 Seaborn 이슈 permalink 또는 histplot 다열범례 실행출력'),
'M08': dict(strict_question=True,broad_question=True,same_variable=False,answer_id=2211433918,answer_class='partial_requested_input_not_matching_toolkit',answer_value='hot-loop/close_event 제거 후에도 Tk+macosx 혼합으로 crash 약절반',answer_note='새 재현입력은 주었지만 요구한 single-toolkit조건을 만족하지 않음. draw_idle를 실제로 시도했는지도 미확인.',change='next_action_change_partial_input',change_summary='같은 지원자가 draw_idle 가설에서 toolkit통일 설명으로 이동. 직접답이 아닌 부분입력/역질문 뒤의 변화이며 strict연결변경으로 세지 않음.',support_after=2214055492,execution_success=False,execution_failure=True,full_goal_success=False,acceptance='없음',unknown='single-toolkit 재현 및 retina목표와 양립하는 GUI선택의 실제 실행 미확인',next_material='Tk를 완전히 제거한 macosx-only 최소코드와 crash결과'),
'MB09': dict(strict_question=True,broad_question=True,same_variable=False,answer_id=1496211688,answer_class='action_response_not_same_variable',answer_value='새 conda 환경은 정상',answer_note='새 환경에서의 성공은 이전 실행환경/실제 package판을 확인하지 않는다. 질문과 함께 이미 제공한 행동을 실행한 결과임.',change='no_change',change_summary='권고는 새환경 생성으로 동일. 지원자의 뒤메시지가 없으며 답을 받아 수정한 권고 없음.',support_after=None,execution_success=True,execution_failure=False,full_goal_success=True,acceptance='원작성자 정상작동 보고',unknown='이전환경이 잘못된판을 불러왔는지, 어떤패키지가 원인인지 미확인',next_material='이전·새환경의 sys.executable, matplotlib/cartopy __version__/__file__ 비교 출력'),
}
EXECUTIONS={
'M01': [(1368542341,'diagnostic_version_query','version확인 출력은 존재하나 원래colormap경고 해결의 새실행 아님',False,'diagnostic_only')],
'M03': [(1370065191,'earlier_trial_timing_unknown','addfont를 시도했으나 세션한정이라는 보고; 질문후 새실행으로 세지 않음',False,'unconfirmed_timing'),(1370892263,'success','cache파일 삭제 후 작동; 같은font발견 목표 진전',True,'partial_goal_persistence_unverified')],
'M04': [(1370981028,'success','Figure 직접생성으로 종료문제 해결; GUI모양 변화도 관찰',True,'full_goal_author_report')],
'M06': [(2206992828,'author_edited_example','큰grid로 root개정 및 pandas신고계획; 새실행 성공/실패 분자에서 제외',False,'unconfirmed_execution')],
'M08': [(2211433918,'failure','loop/close_event 제거한 코드도 약절반 segfault; 혼합toolkit 유지',True,'same_goal_partial_test')],
'MB09': [(1496211688,'success','새환경을 실제로 생성한 뒤 정상작동 보고',True,'full_minimal_goal_author_report')],
}

out=[];receipts=[]
for c,a in ANALYSIS.items():
    init=INITIAL[c];comments,nodes,d=load_comments(c);byid={r['id']:r for r in comments};root=date(init['created_at']);root30=root+dt.timedelta(days=30);root90=root+dt.timedelta(days=90)
    def event(id):
        z=byid[id];t=date(z['created_at']);n=nodes.get(id,{})
        return {'comment_id':id,'url':z['html_url'],'utc':z['created_at'],'author':z['user']['login'],'role':z['author_association'],'root_author':z['user']['login']==init['author'],'body_sha256':hashlib.sha256(z['body'].encode()).hexdigest(),'last_edited_utc':n.get('lastEditedAt'),'within_root30':t<=root30,'within_root90':t<=root90,'summary':SUMMARY.get(id,'outside-window metadata only')}
    msgs=[event(z['id']) for z in comments if date(z['created_at'])<=root90]
    qrows=[];answers=[]
    for q in [r for r in Q if r['case_id']==c]:
        qt=date(q['question_utc']);ans=event(a['answer_id']) if a['answer_id'] else None
        entry={'question_id':q['question_id'],'comment_id':int(q['question_comment_id']),'utc':q['question_utc'],'url':q['question_url'],'author':q['question_author'],'variable':q['variable'],'already_in_current_root':q['already_in_root'],'already_in_pre_first_root_confirmed':False,'prior_disclosure_status':'unconfirmed_root_history','strict_information_question':a['strict_question'],'broad_question':a['broad_question'],'predictions_source':'questions.csv@'+SEAL,'question30_end':iso(qt+dt.timedelta(days=30)),'answer_class':a['answer_class'],'same_variable_direct':a['same_variable'],'broad_same_variable_direct':a.get('broad_same_variable',a['same_variable']),'answer_comment_id':a['answer_id'],'answer_within_root30':ans['within_root30'] if ans else None,'answer_within_root90':ans['within_root90'] if ans else None,'answer_within_question30':date(ans['utc'])<=qt+dt.timedelta(days=30) if ans else None,'answer_wait_hours':round((date(ans['utc'])-qt).total_seconds()/3600,6) if ans else None,'answer_content_latest_wait_hours':round((date(ans['last_edited_utc'] or ans['utc'])-qt).total_seconds()/3600,6) if ans else None,'same_variable_wait_hours':round((date(ans['utc'])-qt).total_seconds()/3600,6) if ans and a['same_variable'] else None,'root30_no_same_variable_answer_censor_hours':round(max(0,(root30-qt).total_seconds())/3600,6) if not a['same_variable'] else None,'question30_no_same_variable_answer_censor_hours':720 if not a['same_variable'] else None,'reply_roundtrip_key':f"{c}:{q['question_comment_id']}:{a['answer_id']}" if ans else None,'strict_roundtrip_key':f"{c}:{q['question_comment_id']}:{a['answer_id']}" if ans and a['same_variable'] else None}
        qrows.append(entry)
        if ans:
            answers.append({**ans,'question_id':q['question_id'],'classification':a['answer_class'],'reported_value':a['answer_value'],'same_subject_version_target':a['same_variable'],'reason':a['answer_note'],'reply_to_evidence':'root author follows the question in same issue; lexical version/candidate/code/environment response; REST issue comments do not provide in_reply_to_id'})
    change={'classification':a['change'],'strict_linked_change':False,'same_supporter':c in ['M01','M07','M08'],'pre_answer_proposal_exists':c not in ['M01','M04','M05','M06'],'explicit_link':c=='M01','link_type':'explicit_reproduction_acknowledgment_not_recommendation' if c=='M01' else 'different_supporter_sequence' if c=='M03' else 'analyst_inference_from_partial_input' if c=='M08' else 'not_established','summary':a['change_summary'],'before_url':init['first_response_url'],'after':event(a['support_after']) if a['support_after'] else None}
    execs=[{**event(i),'classification':kind,'summary':desc,'new_execution_for_original_goal':new,'goal_scope':scope} for i,kind,desc,new,scope in EXECUTIONS.get(c,[])]
    provider=[]
    if c in ['M01','M02']:
        pn=24970 if c=='M01' else 24869;pr=json.loads((P/'cache'/f'PR{pn}.json').read_text())['pull_request']
        provider.append({'url':pr['url'],'created_at':pr['created_at'],'merged_at':pr['merged_at'],'merge_commit_sha':pr['merge_commit_sha'],'within_root30':date(pr['merged_at'])<=root30,'within_root90':date(pr['merged_at'])<=root90,'summary':'공급자가 uint8승격 및회귀test를 추가함; 원작성자 재실행 아님' if c=='M01' else '공급자가 toolbar pan/zoom 상태문자 제거를 구현함; 원작성자 사용확인 아님','user_execution':False})
    completeness='complete_public_snapshot' if len(comments)==d['totalCommentsCount'] else 'unobservable_pagination_gap'
    receipt={'case_id':c,'checked_utc':NOW,'t0_seal_sha':SEAL,'original_fetch_receipt':f'evidence/{c}-comments-receipt.json' if (P/'cache'/f'{c}-comments.json').exists() else f'evidence/{c}-html-receipt.json','api_comment_count':len(comments) if (P/'cache'/f'{c}-comments.json').exists() else None,'html_total_comments':d['totalCommentsCount'],'html_union_comments':len(nodes),'front_page_info':d['timelineItems']['pageInfo'],'back_page_info':d['backTimelineItems']['pageInfo'],'public_snapshot_complete':completeness=='complete_public_snapshot','visible_deleted_message_marker':False,'limit':'일치하는공개댓글수/페이지완료는 과거에 삭제된미표시자료의 부재까지 증명하지 않음. 수정댓글은현재본문과최종수정시각만 확인.','last_confirmed_location':comments[-1]['html_url'] if comments else init['root_url'],'last_in_window_location':msgs[-1]['url'] if msgs else init['root_url']}
    receipts.append(receipt)
    out.append({'case_id':c,'sample':'A' if c.startswith('M0') else 'B','root_url':init['root_url'],'root_created_at':init['created_at'],'root_author':init['author'],'request_type':init['request_type'],'first_strategy':init['first_strategy'],'information_score':init['information_score'],'original_grade':init['original_grade'],'exposure':init['exposure'],'t0_seal_sha':SEAL,'direct_read_utc':NOW,'root30_end':iso(root30),'root90_end':iso(root90),'root30_status':completeness,'root90_status':completeness,'strict_first_question':a['strict_question'],'broad_first_question':a['broad_question'],'any_question_root30':a['strict_question'],'later_first_clarification':None,'messages':msgs,'questions':qrows,'answers':answers,'recommendation_changes':[change],'executions':execs,'provider_implementations':provider,'same_variable_answer_case':a['same_variable'],'broad_same_variable_answer_case':a.get('broad_same_variable',a['same_variable']),'linked_recommendation_change_case':False,'new_execution_success_case':a['execution_success'],'new_execution_failure_case':a['execution_failure'],'full_goal_success_case':a['full_goal_success'],'chain_success_case':False,'author_acceptance':a['acceptance'],'author_response_after_first':any(z['user']['login']==init['author'] and (not init['first_response_utc'] or z['created_at']>init['first_response_utc']) and date(z['created_at'])<=root30 for z in comments),'no_substantive_response':init['first_strategy']=='no_substantive_response','observation_unavailable':completeness!='complete_public_snapshot','unknown':a['unknown'],'last_confirmed_location':receipt['last_in_window_location'],'next_material':a['next_material'],'observed_cost':{'strict_roundtrip_keys':sorted({q['strict_roundtrip_key'] for q in qrows if q['strict_roundtrip_key']}),'reply_roundtrip_keys':sorted({q['reply_roundtrip_key'] for q in qrows if q['reply_roundtrip_key']}),'first_response_hours':round((date(init['first_response_utc'])-root).total_seconds()/3600,6) if init['first_response_utc'] else None,'clicks_reading_labor_saved':'미확인; 공개댓글에는 독립 측정없음'}})

(P/'chains.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in out))
(P/'evidence/followup-read-receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
later=[
dict(case_id='M03',comment_id=1370332943,direction='root_author_to_supporter',variable='cache_location_and_rebuild',classification='not_supporter_clarification',reason='원작성자의 새질문이며 작성자에게 추가조건을 묻는 표본분모 아님'),
dict(case_id='M07',comment_id=2245451004,direction='supporter_to_third_party',variable='legend_api_concern',classification='third_party_design_discussion',reason='mwaskom의 API의견을 되묻는 것으로 원작성자 GrunCrow의 값 요청 아님'),
dict(case_id='M07',comment_id=2245466345,direction='third_party_to_supporters',variable='proposed_ncols_setter',classification='proposal_in_question_form',reason='해법제안의 의문형이며 원작성자가 가진 기존값 요청 아님'),
dict(case_id='M08',comment_id=2211433918,direction='root_author_to_supporter',variable='recommended_gui_arrangement',classification='new_request_from_author',reason='원작성자의 추천방식 질문이며 single-toolkit 입력의 직접답과 구별'),
]
for x in later:
    init=INITIAL[x['case_id']];z=next(r for r in load_comments(x['case_id'])[0] if r['id']==x['comment_id'])
    x.update(url=z['html_url'],utc=z['created_at'],strict_information_question=False,within_root30=True,pre_outcome_prediction=False)
with (P/'later-questions.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(later[0]));w.writeheader();w.writerows(later)
cor=[{'case_id':'M06','correction_type':'root_revision_timing_corrobation','frozen_initial_changed':False,'evidence_url':'https://github.com/matplotlib/matplotlib/issues/28505#issuecomment-2206992828','created_at':'2024-07-03T18:57:46Z','last_edited_at':'2024-07-03T18:58:17Z','finding':'작성자가 최초답 뒤 더큰grid로 원문을 방금개정했다고 밝힘. T0 exposure=true를 보강하며 최초원문 전체복원은 안됨.','affected_field':'initial.information_score/current-body field_map is not proven pre-response','next_material':'첫실질답2024-07-03T18:56:41Z보다앞선 description revision'}]
cor.append({'case_id':'M01','correction_type':'temporal_overlap_qualification','frozen_initial_changed':False,'evidence_url':'https://github.com/matplotlib/matplotlib/issues/24865#issuecomment-1368542341','finding':'current-root NumPy1.24와답1.24.0은내용중복이지만최초공개시점은미확인. 공개timeline12개에rename이벤트는보이지않으나absence만으로원판확정하지않음. same-variable직접답은유지하고restatement확정은보류.','affected_field':'post-seal answer_class; original_grade U retained','next_material':'first-response전title/body를보존한메일또는원판revision'})
(P/'corrections.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in cor))
print('wrote',len(out),'case chains;',len(later),'later question-like exclusions; 2 corrections')
