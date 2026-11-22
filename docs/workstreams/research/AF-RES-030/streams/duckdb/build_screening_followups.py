"""Post-seal audit of every DuckDB B root actually screened, outside B8 rates."""
from pathlib import Path
import csv,json,datetime as dt,hashlib
P=Path(__file__).resolve().parent; C=P/'evidence/unread_cache'
NOW=dt.datetime.now(dt.timezone.utc).isoformat(); parse=lambda s:dt.datetime.fromisoformat(s.replace('Z','+00:00'))
initial={r['case_id']:r for r in map(json.loads,(P/'initial.jsonl').read_text().splitlines())}
pages={r['case_id']:r for r in json.loads((P/'evidence/B-followup-pagination.json').read_text())}
summaries={
'DB01':('즉답/옵션 제시 뒤 빠르다는 보고가 나왔으나 같은 코드의 행 수 누락이 드러남. 공급자 추가 패치 후4/26 원 작성자가212363079행과 실행시간을 보고.4/21에 입력/단계 정보를 묻는 후발 요청도 있음. 파일 공유는 공개 댓글에 감사만 보이므로 전달내용 미확인.',[1493408625,1493410931,1517370177,1523795642]),
'DB02':('개인 연락 요청만 있고30/90일 안 기술적 답 없음. 연락이 실제 일어났는지/그 내용은 미확인.',[1493790487]),
'DB03':('fork tag 조언에 작성자가 원 저장소 clone에서도 발생한다고 반박. 다른 지원자가 본인 재현과 문서 저장소로 이동을 제안. 새 해결 실행 보고 없음.',[1493261935,1493264879]),
'DB04':('선정 B. 실제 CSV의 인용된 null을 직접 답함. 이후 권고 댓글/작성자 실행 없음.90일 안 공급자 회귀시험은 chains와 DP03에 별도.',[1493302942]),
'DB05':('30/90일 댓글 없음. 이후 봇 댓글은 창 밖으로 분리. 공개 창의 무응답이며 현재 댓글 원문은 관측 가능.',[]),
'DB06':('지원자가 수정 R 호출을 제시하고 작성자가 상수 offset을 사용한 재현 코드/출력을 남김. 첫답의 PR 언급은 실제 기존정보 질문으로 선정하지 않았음.',[1494360429,1500899374]),
'DB07':('선정 B. 기존 행순서 목표 재진술, index/row-number 방법 논의, client 구현 의향. 마지막 배치 질문에는 답과 실행결과 없음.',[1493849083,1494446827,1494488354]),
'DB08':('후발 OS 요청에 작성자가 Windows10과 업그레이드 후 동일 오류를 답함. 다른 발신자의 path separator 조언 후5/2 script 작동을 보고. exact build 요청은 미답. 최초 질문 적격은 아니므로 B8 편입 안 함.',[1494639701,1494708175,1531770729]),
'DB09':('작성자 스스로 자신의 오류를 찾았다고만 말함. 구체적 수정/출력/새 실행 성공은 미확인.',[1496375065]),
'DB10':('작성자가 Discord 논의를 가리킨 한 댓글. 해당 외부 내용은 직접 읽지 않았으므로 결정/실행 미확인.',[1496436059]),
'DB11':('지원자가 master 수정과 자체 출력을 제시. 원 작성자 후속 없음. 공급자 출력만으로 사용자 실행 성공이라 하지 않음.',[1496567795]),
'DB12':('공급자가 Parquet 구조 위반과 defensive repair를 논의. 작성자는 생성 라이브러리에서 읽혔다고 말하고 형식 오기를 추적했다고 답함. 그 라이브러리 사용은 과거 사실이며 수정판 실행은 미확인.',[1499218520,1499287099,1499322241]),
'DB13':('첫 패치 시험 여부 확인에 작성자는 아직 빌드할 시간이 없다고 답함. 사전 규칙상 순수 patch verification이므로 B 질문 적격에서 제외.',[1499431288]),
'DB14':('지원자의 Windows 경로 구분자 설명 후30/90일 작성자 답 없음. 수정/작동 미확인.',[1500674065]),
'DB15':('연도가52주와 같지 않다는 설명을 작성자가 수락하고 자신의 시험이 잘못됐다고 말함. 새 실행 결과는 없음.',[1500756253]),
'DB16':('implicit cast 문서 링크 설명을 수락하며 문서에서 다른 절을 찾았었다고 말함. 새 실행 없음.',[1501679127]),
'DB17':('첫 PostgreSQL 오류 질문에 작성자가 dialect 오류를 구분해 답함. 후속 native 함수/driver 수정과 시행착오 뒤5/9 nightly JDBC로 timestamp truncation 문제가 해결됐다고 보고.6/8 제3자의 다른 월 단위 문제는 원 작성자 성공을 대체하지 않음. 전역 첫8 B에서 탈락, 주분모 제외.',[1501901972,1503962799,1540506256,1582455602]),
'DB18':('자동 JSON 읽기 자체는 작동했지만 nested field/행 펼침 목적은 아직 미달이라고 작성자가 명시. 나중 unnest 안내에4/20 작동 보고와 notebook 링크. notebook 원문은 미열람이라 독립 실행 산출물 검증 없음.',[1511490541,1516478886,1516794995]),
'DB19':('첫답은 patch trial 요청. 작성자는 빌드하겠다고 하고 다음날 확인했다고 답함. 공급자 자체 출력은 있지만 작성자의 별도 출력/세부 실행은 없음. 시험 요청을 환경정보 질문으로 바꾸어 B8에 넣지 않음.',[1502343418,1503592540]),
'DB20':('공급자의 primary-key 저장공간 설명과 제3자의 압축실험. 원 작성자는 설명을 수락하고 VARCHAR 새 이슈를 열겠다고 말함. 원 목표의 새 실행은 없음.',[1503809266,1503832680]),
'DB21':('30/90일 공개 댓글 없음. root 및 timeline 접근 가능. 종료만으로 재실행을 인정하지 않음.',[]),
'DB22':('catalog 질의 안내 뒤 감사와 새 release 일정 질문. 실제 query 실행/원 출력 검증 보고 없음.',[1542846640,1542847948]),
'DB23':('다른 기여자의 가벼운 댓글만 존재하고30/90일에 실질 지원답 없음. 원 작성자는 maintainer라는 별도 역할 정보 보존.',[1503603703]),
'DB24':('공급자 reference-count 수정 설명 후4/21 작성자가 특정 Python 호출과 수정판0.7.2.dev2366에서 메모리가 안정적이었다고 명시. 질문 없이 공급자 수정 후 실행 보고된 후보이며 A/B8 양성률에 넣지 않음.',[1518086893]),
'DB25':('제3자가 SMALLINT/VARCHAR 비교의 더 작은 반례를 만들었으나 마지막 차이 이유는 모른다고 함. 원 작성자 후속/수정 성공 없음.',[1505801320]),
'DB26':('작성자가 스스로 상수를 DOUBLE로 지정하면 같은 결과가 나온다고 말하고 종료. 타인 실질 답 없음. T0 도구 탐색 때 이 결말을 본 노출은 이미 기록됨.',[1504907075])}

def comments(s):
 n=s['issue_number'];f=C/f'comments-{n}.json'
 if f.exists(): return json.loads(f.read_text())
 return [dict(id=x['databaseId'],html_url=x['url'],created_at=x['createdAt'],updated_at=x.get('lastEditedAt') or x['createdAt'],user={'login':x['author']['login']},body=x['body']) for x in json.loads((C/f'html-comments-{n}.json').read_text())]
rows=[];updates=[]
for case,s in initial.items():
 if not case.startswith('DB'):continue
 r=parse(s['root_created_utc']);a=comments(s);a30=[x for x in a if parse(x['created_at'])<=r+dt.timedelta(days=30)];a90=[x for x in a if parse(x['created_at'])<=r+dt.timedelta(days=90)]
 summary,ids=summaries[case]; selection=case in ['DB04','DB07'];receiptfile=P/f"evidence/first-{s['issue_number']}.json";receipt=json.loads(receiptfile.read_text())
 api_complete=receipt.get('has_next_page') is False
 html_complete=all(not(pages[case].get('page_info',{}).get(k) or {}).get('hasNextPage') and not(pages[case].get('page_info',{}).get(k) or {}).get('hasPreviousPage') for k in ['timelineItems','backTimelineItems'])
 complete=api_complete or html_complete
 z={'case_id':case,'sample':'B_selected' if selection else 'B_screen_only','root_url':s['root_url'],'root_created_utc':s['root_created_utc'],'root_author':s['root_author'],
  'first_strategy':s['first_strategy'],'request_type':s['request_type'],'information_score':s['information_score'],'original_grade':s['original_grade'],
  'exposure_effective':s['exposure'] or case=='DB04','first_purpose':s['goal'],'first_response_url':s['first_response_url'],
  'first_response_created_utc':s['first_response_created_utc'],'eligible_root':True,'b_first_question_eligible':s['b_question_eligible'],
  'selected_global_B':selection,'included_in_A_rate':False,'included_in_B8_rate':selection,
  'exclusion_reason':None if selection else ('global interleave first8 already filled; later eligible question candidate' if s['b_question_eligible'] else s['b_eligibility_note']),
  'root30_end':(r+dt.timedelta(days=30)).isoformat(),'root90_end':(r+dt.timedelta(days=90)).isoformat(),
  'root30_status':'observed_comments' if a30 else 'observed_no_public_comments','root90_status':'observed_comments' if a90 else 'observed_no_public_comments',
  'root30_comment_count':len(a30),'root90_comment_count':len(a90),'current_all_comment_count':len(a),'public_conversation_complete':complete,
  'pagination':{'api_no_next':api_complete,'html_page_info':pages[case].get('page_info'),'timeline_references_complete':html_complete},
  'deleted_or_hidden_records':'no deleted placeholder observed; historical undetectable deletions cannot be ruled out',
  'followup_summary':summary,'key_urls':[s['root_url']+'#issuecomment-'+str(i) for i in ids],
  'observed_comment_records':[{'id':x['id'],'utc':x['created_at'],'updated_utc':x['updated_at'],'actor':x['user']['login'],'url':x['html_url'],'body_sha256':hashlib.sha256(x['body'].encode()).hexdigest()} for x in a90],
  'last_confirmed_url':a90[-1]['html_url'] if a90 else s['root_url'],'last_endpoint':s['root_url'],'checked_utc':NOW,
  'limitations':'current edited text; no private/off-platform conversations; linked notebooks/attachments not counted as read unless separately logged',
  'next_source_if_changed':s['root_url']+'의 댓글 편집 이력 또는 공개 cross-reference 후속'}
 if not complete:z.update(root30_status='unobservable_incomplete_pagination',root90_status='unobservable_incomplete_pagination')
 rows.append(z)
 updates.append({'source_id':'D-READ-UPDATE-'+case,'type':'public GitHub thread followup reading update','publisher':'duckdb/duckdb public participants','url':s['root_url'],
  'version':s['root_created_utc']+' root; post-seal current public comments','checked_utc':NOW,'sections':'all comments created within root+90 days; root+30 separately marked; quoted prior text omitted only when already read',
  'observed':summary,'limitations':z['limitations'],'linked_Q_cases':['Q4','Q5','Q6','Q7',case],'duplicate_group':f"duckdb-issue-{s['issue_number']}",'count_minimum':False,
  'read_after_seal':'9de54923257d613359348c8ccee2ff8225c8a0d8','evidence_file':'screening-followups.jsonl#'+case})

# The four root-ineligible candidates were also opened after seal; they do not consume the eligible cap.
frame=list(csv.DictReader((P/'frame.csv').open()))
exsumm={6954:'공급자의 이미 수정한 현상을 알리는 공지.30/90일 댓글 없음.',6964:'빌드 오류 후 다른 빌드 오류, compiler 질문에 gcc판을 답했으나 실제 필요값은 cmake 설정임을 지원자가 다시 명시. 설정 답 후 원 작성자가 더 이상 재현되지 않는다고 보고. 순수 build 범위이므로 선정 제외 유지.',7002:'30일 댓글 없음.90일 안 타 사용자들의 Alpine/다른 언어 binding 오류와 우회안. 원 요청자 동일목적 성공으로 합치지 않음.',7009:'90일 안 댓글 없음. 최초 댓글은 root90 밖 봇. API 전체9개를 확인해 HTML 중간 pagination과 구별.'}
exgoal={6954:'Pandas2 시간대 자료 소비 문제의 수정 공지',6964:'DuckDB 컴파일 오류 수정',7002:'Alpine musl에서 httpfs 확장 로드',7009:'32비트 libatomic 링크 오류 해결'}
for n in [6954,6964,7002,7009]:
 s=next(x for x in frame if x['issue_number']==str(n));raw=json.loads((C/f'excluded-followup-{n}.json').read_text());r=parse(s['created_utc']); a=raw['comments']; a30=[x for x in a if parse(x['createdAt'])<=r+dt.timedelta(days=30)];a90=[x for x in a if parse(x['createdAt'])<=r+dt.timedelta(days=90)]
 z={'case_id':'DBX-'+str(n),'frame_id':s['frame_id'],'sample':'B_root_excluded','root_url':s['root_url'],'root_created_utc':s['created_utc'],'first_purpose':exgoal[n],
  'first_response_url':a[0]['url'] if a else None,'first_response_created_utc':a[0]['createdAt'] if a else None,'eligible_root':False,'selected_global_B':False,'included_in_A_rate':False,'included_in_B8_rate':False,
  'exclusion_reason':s['reason'],'root30_end':(r+dt.timedelta(days=30)).isoformat(),'root90_end':(r+dt.timedelta(days=90)).isoformat(),
  'root30_status':'observed_comments' if a30 else 'observed_no_public_comments','root90_status':'observed_comments' if a90 else 'observed_no_public_comments',
  'root30_comment_count':len(a30),'root90_comment_count':len(a90),'public_conversation_complete':True,'pagination':raw['pages'],
  'followup_summary':exsumm[n],'last_confirmed_url':a90[-1]['url'] if a90 else s['root_url'],'last_endpoint':s['root_url'],'checked_utc':NOW,
  'limitations':'out-of-scope root; no use/design intent added from later outcome; same-thread timeline only; 7009 REST comments9 complete',
  'observed_comment_records':[{'utc':x['createdAt'],'url':x['url'],'body_sha256':hashlib.sha256(x['body'].encode()).hexdigest()} for x in a90]}
 rows.append(z)
 updates.append({'source_id':'D-READ-UPDATE-DBX-'+str(n),'type':'excluded public GitHub thread followup','publisher':'duckdb/duckdb public participants','url':s['root_url'],'version':s['created_utc']+' root','checked_utc':NOW,'sections':'root-level exclusion at T0; after seal public comments through90d','observed':exsumm[n],'limitations':z['limitations'],'linked_Q_cases':['Q1','Q4','Q7','DBX-'+str(n)],'duplicate_group':f'duckdb-issue-{n}','count_minimum':False})
(P/'screening-followups.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))

# Same source identities as the eight A roots: this is an updated reading record, never an additional original.
chains=[json.loads(x) for x in (P/'chains.jsonl').read_text().splitlines()]
for x in chains:
 if x['sample']!='A':continue
 updates.append({'source_id':'D-READ-UPDATE-'+x['case_id'],'type':'public GitHub thread followup reading update','publisher':'duckdb/duckdb public participants','url':x['root_url'],
 'version':x['root_created_utc']+' root; current public comments read after seal','checked_utc':NOW,'sections':'all root+90 comments, root+30 primary separately coded; same-event references opened only if providers ledger says so',
 'observed':{'first_question':x['first_question'],'same_variable_answer':x['same_variable_answer'],'bundle_linked_change':x['bundle_linked_change'],'new_execution_success':x['new_execution_success']},
 'limitations':'current comment versions; root first version unrecovered; no unpublished execution; exact source links in chains','linked_Q_cases':['Q5','Q6','Q7','Q8',x['case_id']],
 'duplicate_group':'duckdb-issue-'+str(initial[x['case_id']]['issue_number']),'count_minimum':False,'evidence_file':'chains.jsonl#'+x['case_id']})
(P/'reading-updates.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in updates))
print(json.dumps({'eligible_B_screened':26,'selected_B':2,'root_excluded_audited':4,'read_update_rows':len(updates),'unobservable_conversation_cases':[x['case_id'] for x in rows if not x['public_conversation_complete']]}))
