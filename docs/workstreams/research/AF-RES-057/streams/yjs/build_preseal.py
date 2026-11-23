from pathlib import Path
import json,csv,hashlib,datetime,re
P=Path(__file__).resolve().parent; ROOT=P.parents[1]; C=ROOT/'.cache/yjs';now=datetime.datetime.now(datetime.timezone.utc).isoformat()
rows=json.loads((C/'frame-full-hidden.json').read_text())
notes={
156:('excluded','두 type의 공유 undo/redo stack 요구지만 남길 구체 내용 없음. separate observers와 afterTransaction의 두 시도 모두 redo가 2 stack items로 갈라진다고 이미 보고.','같은 stack으로 두 type 변경 묶기; 두 시도 결과 노출'),
157:('selected','보존할 정확 문구와 startSkipping/stopSkipping 사건 경계가 함께 있음. 제안 메서드는 실제 API로 취급하지 않음.','보호 문자열 this text can not be undone을 되돌리기에서 제외'),
162:('excluded','추가 a→삭제→undo→undo 실패와 !struct.deleted 조건 제거 뒤 작동/시험 통과라는 두 조작 답이 본문 노출.','두 번째 undo 뒤 a가 남는 오류; 소스 조건 제거 수정 제안'),
165:('excluded','width20→30→34 묶음의 기본 undo30와 연결한 fix가 작동한다는 진술 모두 노출. 수정 diff는 아직 열지 않음.','변경 묶음 이전20 보존 목표; 원판13.0.0-96 명시'),
192:('excluded','변경 직렬화 질문만 있고 구분할 사건열/남길 구체 내용 없음.','개별 변경을 저장했다 나중에 되돌리고 싶음'),
203:('excluded','복원 stack 오류 dump와 doc bytes는 있으나 보존할 사용자 내용/성공 기준 미명시.','직렬화 undoStack 복원 뒤 Unexpected case'),
204:('selected','삭제한 Hello 복원과 복사 뒤 별도로 삽입한123 보존, 명시판13.0.8. 본문 기대·대조는 노출됐지만 여기 고정 gc A/B의 답 둘은 미제시.','Hello World 앞5글자 삭제, 문서복사,123 추가, 원stack 이식undo; 삭제/추가 대조'),
236:('eligible_not_selected','앞선2자리 충원 후 후보. A/B 주체와 map value 보존 목표 명시; 원작동 결과 노출.','A가 설정/갱신한map을 Bundo하면 key전체삭제'),
240:('eligible_not_selected','앞선2자리 충원 후 후보; 본문 실패 출력 노출. #241과 같은 사건 계보로 합침.','1221→123321 두번undo 뒤3재삽입이31221'),
241:('eligible_not_selected','앞선2자리 충원 후 후보. #240 재게시/동일 재현 계보.','13.3.2에서 기대12321/관측31221'),
273:('excluded','captureTimeout 기본과0 각각의 출력, 다른 원점끼임,redo 모두 본문에 공개.','ME abc/OTHER def/ME ghi 묶음이 타인def도 지움;0이면abcdef'),
290:('eligible_not_selected','앞선2자리 충원 후 후보; 내용은 위치속성 일반형이며 실제좌표 없음.','drag pause 중에도 한 이벤트로합치기'),
304:('eligible_not_selected','앞선2자리 충원 후 후보; 같은판 실패XML/전체출력 사전노출.','세번undo/redo 뒤a속성소실;b는보존'),
315:('excluded','여러Y.Doc scope API문의; 사건/보존내용미제시.','복수문서를하나UndoManager에연결문의'),
317:('eligible_not_selected','앞선2자리 충원 후 후보; 입력은 외부sandbox로만연결, 본문결과노출.','nested blocks Something Else 소실'),
328:('excluded','복사type에history이식문의지만 본문에 편집사건열/남길내용 없음.','JupyterLab의 이전시각history 보존문의'),
343:('eligible_not_selected','앞선2자리 충원후후보; #317후속변형으로 계보연결.','2변경수정뒤3개이상변경중첩데이터오류지속'),
350:('eligible_not_selected','앞선2자리 충원후후보; 구체입력은외부sandbox, 기대foo.hello=world 노출.','snapshot돌리기에서데이터손실'),
353:('excluded','event순서/API알림 보존요구이며 문서내용보존과 사건열미제시.','added가popped보다먼저라cursor metadata접근문제'),
355:('eligible_not_selected','앞선2자리충원후후보; #317/343관련이나 새 독립수정경로예정. 원장에는 같은중첩복구실패군으로 보수계보.','x/y0→100→200→300 redo끝속성소실,deleteFilter우회노출'),
358:('excluded','observeDeep알림호출결함; 남길문서내용/두편집사건 없음.','undo때observeDeep이호출되지않음'),
365:('excluded','canUndo/canRedo 버튼상태 API질문만.','빈stack에서undo/redo버튼비활성'),
390:('excluded','두정책의A/B주체동작·undo/redo결과모두본문노출.','다른주체가덮어쓴map을undo할지두정책비교'),
392:('eligible_not_selected','앞선2자리충원후후보; 텍스트/format의 기대·실패 모두본문노출.','같은text지만원격bold범위가다름;13.5.27'),
400:('eligible_not_selected','앞선2자리충원후후보; 실제20actionpayload없음.','undoStack뒤10개만남기면map손상'),
402:('eligible_not_selected','앞선2자리충원후후보; 실제배열/주체/기대및실패본문노출.','A추가→B삭제→Aundo추가→Bundo삭제때bbbb부활'),
414:('excluded','applyDelta와직접delete/insert대체의두결과본문노출.','XML속성복구에서실제로존재하지않은상태'),
433:('excluded','core/timeout구조분리제안; 남길내용/편집열 없음.','BaseUndoManager와withCaptureTimeout제안'),
443:('excluded','samegroup실패와다른undoblock성공두답본문노출.','map속성변경+map삭제undo시bar손실'),
447:('eligible_not_selected','앞선2자리충원후후보; 실패/기대XML본문노출.','속성b변경+요소삭제undo후b소실')}
frame=[];sources=[]
for rank,x in enumerate(rows,1):
 num=x['number'];status,reason,finding=notes[num];body=x['body'] or '';sid=f'Y-I{num}';work=f'yjs-issue-{num}'
 if num==241:work='yjs-issue-240-241'
 if num==240:work='yjs-issue-240-241'
 if num in [317,343,355]:work='yjs-nested-undo-317-343-355'
 slot={157:'YN1',204:'YN2'}.get(num,'')
 frame.append({'recruitment_order':rank,'layer':'natural','repository':'yjs/yjs','issue_number':num,'created_UTC':x['created_at'],'title':x['title'],'url':x['html_url'],'case_id':slot,'decision':status,'reason':reason,'earliest_body_status':'현재 API 복원 본문; 최초 생성 revision 미복원','updated_UTC':x['updated_at'],'body_sha256':hashlib.sha256(body.encode()).hexdigest(),'exposure':finding,'body_read':True})
 sources.append({'source_id':sid,'work_id':work,'kind_lineage':'requester issue; current body. comments/diff withheld until stage2','questions_cases':['Q1','Q2','Q6',slot or 'frame-exclusion'],'original_url':x['html_url'],'fixed_url':x['html_url'],'version_date_hash':{'created_UTC':x['created_at'],'updated_UTC':x['updated_at'],'body_sha256':hashlib.sha256(body.encode()).hexdigest()},'opened_UTC':{'from':'2026-11-23T03:19:42Z','through':now,'precision':'three body-display batches within interval; ledger recorded afterward'},'location':'issue body only, source code and author expected/observed blocks where supplied; migration footer excluded','findings':finding,'limits':'Earliest submitted revision not recovered; current body may have later edits. Claimed output is author statement, not this session execution. No comments or linked fixes read before seal. '+reason,'evidence_type':'author_statement','contrary_source_ids':[],'access_status':'direct_read','count_external_primary':True,'source_group':'request_body','selected_request':bool(slot)})
with (P/'frame.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(frame[0]));w.writeheader();w.writerows(frame)
(P/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
(P/'recruitment-review.md').write_text('''# Yjs 모집 검토\n\n모든 첫 30개 복원 본문을 직접 읽었다. query-word 결과27개를 모집틀로 쓰지 않았다. 본문 전에 performed title-only audit의381개 기간 issue 중 첫300개 metadata로 substring 첫30개가 확정됐다. 처음 token검색에서 빠진16개가 `title-audit.json`에 있다. PR과 cutoff 밖은 제외했다.\n\n첫 적격 두 자리는 **#157→YN1, #204→YN2**다. #156은 구체 보존내용이 없고 두 그룹화 시도의 실패도 이미 노출했다. #162와#165는 실패 출력만이 아니라 소스 수정 후 작동/통과 진술도 본문에 있어 두조작 답 노출로 제외했다. 본문에 baseline 결과가 있다는 이유만으로 모든 bug를 제외한 것은 아니다. #204는 복사 후123 보존 목표와 사건열이 명시돼 있고, 선정 A/B의gc설정 차이는 본문에 답이 없다. 다만 본문 기대값과 삭제/추가 대조를 이미 읽었으므로 새 exact-text적중의 근거로 쓸 수 없다.\n\n#157의 `this text can not be undone`은 원문 정확 보호 문자열이다. 초기문서와 앞뒤 ordinary edit는 원문에 없다. 원문에서 제안한startSkipping/stopSkipping을 현재제품의 실제 API로 바꾸어 부르지 않는다. 당시 코드를 확인하여 사용가능한origin집합차이로 별도연구입력을 만든다. 당시정식판12.3.3과 contemporaneous prerelease13.0.0-94는 분리한다.\n\n#204의원문은 `// expect ~"Hello 123 World"`라는 근사기대다. 삽입앞공백을연구자가정정해원래정답으로만들지않는다. primitive문자열,새123보존,삭제한Hello복원,redo범위를각각확인한다.\n\n자연층은 API에서현재복원가능한body를읽은것이지,2019/2020년최초bodyrevision을복원한것이아니다. 공개이슈에2024년붙은migration footer는관련없고저장/추적하지않았다. 원bodyhash만남겼다.\n\n진단층초기기계후보testUndoText는push변경을못센heuristic결함이었다. root교차검토에서결과를열기전에수정하여2push+undo의**testInfiniteCaptureTimeout**을선택했다. 원시험에redo는없으므로추가redo는연구자변형이다. 이전후보의input전체를읽은노출은그대로보존한다.\n''')
print('frame rows',len(frame),'direct request works conservative',len({x['work_id'] for x in sources}),'selected',[x['case_id'] for x in frame if x['case_id']])
