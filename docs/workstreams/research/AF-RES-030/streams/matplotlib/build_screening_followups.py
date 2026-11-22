"""Post-selection audit of all nonselected B screening attempts.

These cases are never promoted into the fixed A or B denominators.
"""
from pathlib import Path
import datetime as dt
import hashlib
import json
import re

P=Path(__file__).resolve().parent
NOW=dt.datetime.now(dt.timezone.utc).isoformat()
SEAL='9de54923257d613359348c8ccee2ff8225c8a0d8'
NOTES={
'MB01':('작성자는 본인설정법을 몰라서가 아니라 타인의기본값 개선을 원했다고 공개. scatter경계반례를 보고0.01보다0.02 또는symbol크기기반 margin을 새로 선호. 새실행보고는 없음.','goal_clarification_without_question; preference_revision',1495047091),
'MB02':('원작성자 답 없음.75일째 다른사용자가 pandas신고여부를 묻고77일째 관련upstream이슈를 찾아옴. 이를 원작성자왕복/실행으로 합치지 않음.','third_party_followup_root90_only',1596668154),
'MB03':('지원자가 이미있는3.7.1수리PR를 찾아업데이트안내, 원작성자 실행없음. 닫힘은 성공아님.','provider_existing_fix_no_author_execution',1494647893),
'MB04':('원작성자가 Astropy ticket요청에 동의했으나 ticket주소/실행결과 없음.','acceptance_only',1493691643),
'MB05':('ndarray.values우회안 뒤 원작성자가 숫자에소수점을 붙였으나 실패. 다른지원자가 float/int가 아니라 ndarray/Series객체변환 문제였다고 정정. 사용자값 변경과 지원자가 뜻한변수의 불일치.','reported_failure_wrong_interpretation',1494819417),
'MB06':('조건부 backend_qt5agg→backend_qtagg안내 뒤 원작성자가 import를바꾸자 정상이라고 구체적으로 보고. 질문없이 실제실행성공.','conditional_action_success',1494359913),
'MB07':('첫답은tight금지. 후발질문은수동layout을figure안에둘수없는이유; 작성자가 사용자추가axes가canvas밖에생기는tool목적을직접답. 여러지원자설명과작성자코드초안뒤 같은jklymak이_tight_bbox소스를안내, 작성자가resize_fig코드및범위밖항목영상출력을성공보고. 여러단계가매개되어한변수질문의단독효과는미확인.','later_goal_question_answer_action_and_execution',1498346144),
'MB08':('작성자가 원문의label.set_text우회안을수용하되colorbar위치reset문제를추가. jklymak이목적/이유를묻지만원작성자답은없고기여자설계토론으로이어짐.','later_clarification_no_author_answer',1511602045),
'MB10':('공급자원인분석및수리PR25681/3.7.2안내. 다른사용자임시margin보고는있지만원작성자사용확인은없음.','provider_fix_third_party_results',1516410147),
'MB11':('root30/90에댓글없음.2026봇댓글은창밖이며실질응답아님.','no_response_window',None),
'MB12':('root30/90에댓글없음.2026봇댓글은창밖. 유지관리자요청이라는역할은별도보존.','no_response_window',None),
'MB13':('전체공개댓글0. root30/90 무응답.','no_response_window',None),
'MB14':('root30/90에댓글없음.최초기술답은2025-02-02라시작2023-04-07의90일창밖.','first_response_after_root90',None),
'MB15':('개발기여자의test수용범위질문에원작성자가경량시험으로충분하다고답. 새기능설계수용질문이라B환경/목표/입력범위에서제외한판정을유지. PR의존성및61일째설계논의는실사용실행아님.','new_design_acceptance_question',1581564271),
'MB16':('torch없는새입력을요구하자작성자는Image.open외부파일로바꿈. 같은지원자는파일없이여전히재현불가라며RGB/RGBA/greyscale을좁혀묻는다. 작성자는다른이슈와같으며RGB일지모른다고추정;실제배열/형식확인은없음.','partial_answer_target_mismatch',1503479266),
'MB17':('타인답없이원작성자자기소스분석1댓글. 독립왕복아님.','self_followup_only',1504548366),
'MB18':('두지원자가Agg stroke와연관가능성을논의. 원작성자답/실행없음.','provider_hypotheses_only',1510183621),
'MB19':('useblit=False우회안뒤작성자는설명과우회책에감사했으나새실행한결과를말하지않음. 감사만으로성공을세지않음.','thanks_not_execution',1517528849),
'MB20':('원작성자의PyQt비교시험방법질문에답없음.30일밖다른기여자가실험했다가처음TkAgg를쓴사실을정정;Qt ALT동작이기능이라는결정으로종료. 이를원작성자값이나성공으로합치지않음.','no_author_answer_third_party_wrong_environment',1564530920),
'MB21':('원작성자가같은shell PySide6.5.0을직접답. 지원자가많은실험과이미받은판을다시묻고작성자는실패/작동backend를세분응답.12일째QtCore먼저import우회성공및디버깅으로Qt5강제발견,13일째IPython qt매핑을확인. 다른지원자의qt6최종안내뒤원작성자실행은없음.','direct_answer_repeated_version_many_trials',1523690871),
'MB22':('관리댓글2건뒤Agg/Cairo지원범위질문은있으나원작성자답없음. 다른관리요청을질문왕복으로세지않음.','question_no_author_answer',1522852395),
'MB23':('공급자들transform/data-limit수정방식논의와새기여자의PR제안. 원작성자조건회수/실행없음.','provider_design_only',1512288302),
'MB24':('underscore필터의문서계약과strip/공백우회안. 원작성자답이나실행없음.','directive_no_author_followup',1509208000),
'MB25':('sphinx-gallery/devguide링크후원작성자후속없음. 종료를해결로보지않음.','conditional_link_no_author_followup',1509044915),
'MB26':('PySide6.5다중상속변경설명과composition권고뒤원작성자가delegation으로해결됐다고구체적으로확인. 첫정보질문없이실행성공.','directive_success',1509885968),
'MB27':('GTK4/GLib복합질문에GTK4.8.3와잘못된GLib1.2.10을답한뒤GLib2.76.1로정정. 지원자는버전들을인용하여GTK4.10을권고. 자체빌드4.10.3실패후배포판4.10설치가29.7일째성공. 첫질문전후보제안은없어초기권고는변경보다새제안이며새패키지공급이매개.','version_answer_corrected_package_new_proposal_failure_then_success',1546936936),
}
rows=[];sources=[]
for r in map(json.loads,(P/'initial.jsonl').read_text().splitlines()):
    c=r['case_id']
    if c not in NOTES:continue
    s=(P/'cache'/f'{c}-root-page.html').read_text()
    d=[json.loads(z) for z in re.findall(r'<script[^>]*type="application/json"[^>]*>(.*?)</script>',s,re.S) if 'issueViewerRoute' in z][0]['payload']['issueViewerRoute']['data']['repository']['issue']
    ns={n['databaseId']:n for e in d['timelineItems']['edges']+d['backTimelineItems']['edges'] if (n:=e['node']).get('__typename')=='IssueComment'}
    root=dt.datetime.fromisoformat(r['created_at'].replace('Z','+00:00'));cut30=root+dt.timedelta(days=30);cut90=root+dt.timedelta(days=90)
    window=[n for n in sorted(ns.values(),key=lambda n:n['createdAt']) if dt.datetime.fromisoformat(n['createdAt'].replace('Z','+00:00'))<=cut90]
    met=[{'comment_id':n['databaseId'],'url':n['url'],'utc':n['createdAt'],'author':n['author']['login'],'root_author':n['author']['login']==r['author'],'last_edited_utc':n.get('lastEditedAt'),'within_root30':dt.datetime.fromisoformat(n['createdAt'].replace('Z','+00:00'))<=cut30,'sha256':hashlib.sha256(n['body'].encode()).hexdigest()} for n in window]
    complete=len(ns)==d['totalCommentsCount']
    summary,classification,last=NOTES[c]
    lasturl=f"{r['root_url']}#issuecomment-{last}" if last else r['root_url']
    exclude='첫실질답은B목표/환경/입력직접질문아님' if not r['b_question_eligible'] else '질문적격이나고정전역interleave에서첫8양성뒤; 결과로대체하지않음'
    row={'case_id':c,'sample':'B_screen_not_selected','root_url':r['root_url'],'root_created_at':r['created_at'],'root_author':r['author'],'original_goal':r['original_goal'],'first_response_url':r['first_response_url'],'first_response_utc':r['first_response_utc'],'first_strategy':r['first_strategy'],'request_type':r['request_type'],'information_score':r['information_score'],'original_grade':r['original_grade'],'exposure':r['exposure'],'T0_sha':SEAL,'selection_exclusion':exclude,'count_in_A_or_B':False,'root30_end':cut30.isoformat(),'root90_end':cut90.isoformat(),'root30_status':'complete_public_snapshot' if complete else 'unobservable_pagination_gap','root90_status':'complete_public_snapshot' if complete else 'unobservable_pagination_gap','html_total_comments':d['totalCommentsCount'],'html_union_comments':len(ns),'root30_comment_count':sum(x['within_root30'] for x in met),'root90_comment_count':len(met),'root90_original_author_comments':sum(x['root_author'] for x in met),'front_page_info':d['timelineItems']['pageInfo'],'back_page_info':d['backTimelineItems']['pageInfo'],'messages':met,'classification':classification,'followup_summary':summary,'last_confirmed_location':lasturl,'checked_utc':NOW,'unknown':'공개현재댓글/수정시각만확인. 삭제된미표시자료의존재및현장실행로그는미확인;외부PR본문/첨부이미지전부를읽은것은아님.','next_material':'표시된핵심당사자댓글의편집이력 또는 연결된당시공급자PR/공식문서'}
    rows.append(row)
    sources.append({'source_id':'M-SCREEN-'+c,'type':'public_GitHub_issue_thread','publisher':'matplotlib/matplotlib; requester '+r['author'],'url':r['root_url'],'version':'created '+r['created_at']+'; root SHA256 '+r['current_body_sha256'],'checked_utc':NOW,'sections':'root/first응답은T0에서읽음; 봉인후 root+90일 public comment IDs '+','.join(str(n['databaseId']) for n in window),'observed':summary,'limitations':row['unknown']+' B선정밖의사후audit이며확증분모에산입하지않음.','linked_Q_cases':['Q4','Q5','Q6','Q7','Q8',c],'duplicate_group':r['root_url'],'count_minimum':False,'direct_read':True,'last_confirmed_location':lasturl,'next_material':row['next_material']})
(P/'screening-followups.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
(P/'screening-sources.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in sources))
print('wrote',len(rows),'nonselected screening followups and sources; all root90 comment bytes read; A/B denominators unchanged')
