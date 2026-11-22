"""Assemble manually reviewed, unchanged C3/C4 atom evidence.

The URL/section rules below encode the review of definitions and relevant
contexts. They are not a keyword classifier and do not compute A/B/C groups.
"""
import collections
import datetime
import hashlib
import json
from pathlib import Path
import urllib.parse

P = Path(__file__).parent
def load(name):
    return json.loads((P / ('control-second-hop-' + name)).read_text())
def write(name, data):
    (P / ('control-second-hop-' + name)).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

arrivals = load('arrivals.json')
access = {x['document_url']: x for x in load('access.json')}
temporary = {x['document_url']: x for x in load('windows.tmp.json')}
targets = load('targets.json')
required = {
    'C3.A1': ['availability_3_11', 'exceptiongroup_constructor_boundary', 'baseexceptiongroup_constructor_boundary'],
    'C3.A2': ['subgroup_matching', 'nonmatch_propagation', 'ordinary_except_distinction'],
    'C4.A1': ['noncancel_first_failure', 'cancel_siblings', 'wait_all', 'gather_default_distinction'],
    'C4.A2': ['await_aenter', 'await_aexit', 'exception_forwarding'],
}
atom_text = {}
for case in ['C3', 'C4']:
    for a in json.loads((P.parent / 'control' / ('freeze-' + case + '.json')).read_text())['atoms']:
        atom_text[a['id']] = a['text']

PURPOSES = {
    'https://peps.python.org/pep-0001/': 'PEP 작성·심사 절차의 첫800 단어. 예외그룹 또는 TaskGroup 호출 계약이 아님.',
    'https://peps.python.org/pep-3134/': 'Python3.0의 예외 chaining·traceback 제안. 독립 예외그룹의 constructor/except* 계약과 다름.',
    'https://docs.python.org/3.11/reference/simple_stmts.html': 'break/continue/return의 제어 흐름 계약. 예외그룹 constructor나 subgroup 처리 전체를 입증하지 않음.',
    'https://docs.python.org/3.11/glossary.html': 'ABC·async context manager 등 용어 정의. 정의·해당 용어 문맥을 읽었으며8천 단어 전체 정독을 주장하지 않음.',
    'https://docs.python.org/3.11/library/sys.html': 'sys.exception()/exc_info()는 현재 처리 중인 예외 조회를 규정. subgroup 매칭·미처리 그룹 자동 전파 계약과 다름.',
    'https://docs.python.org/3.11/library/asyncio-runner.html': 'Runner/run은 event loop의 생명주기와 최상위 coroutine 실행. TaskGroup 형제 실패 정책과 다름.',
    'https://docs.python.org/3.11/library/asyncio-sync.html': 'Barrier의 참여자 동기화·대기 해제. 첫 자식 실패에 따른 TaskGroup 취소 정책이나 두 await 호출 명세가 아님.',
    'https://docs.python.org/3.11/library/asyncio-eventloop.html': '네트워크 연결·socket·event loop 구현 및 조회의 정의를 읽음. TaskGroup의 첫 실패 정책과 다른 호출.',
    'https://docs.python.org/3.11/library/asyncio-stream.html': 'StreamWriter와 TLS 전환 정의. 같은 asyncio 프로젝트지만 TaskGroup/async-with 명세가 아님.',
    'https://docs.python.org/3.11/library/constants.html': 'NotImplemented 등 내장 상수 정의. 예외그룹/TaskGroup 요구의 지원 문서가 아님.',
    'https://docs.python.org/3.11/library/contextvars.html': 'Context 복사·값 보관·run의 문맥. async-with의 두 await 호출 프로토콜과 다름.',
    'https://github.com/python/cpython/tree/3.11/Lib/asyncio/tasks.py': '첫800 단어는 파일 UI·행번호 중심이다. 같은 HTML의 코드에서 gather가 별도로 구현됨을 W 진단으로 확인했으나 TaskGroup 클래스와 전체 async-with 프로토콜은 없음.',
    'https://github.com/python/cpython/issues/75453': '실제 목적지는2017년 itertools.zip_longest 문서 이슈(BPO31270). 출발 댓글의 TaskGroup 문맥과 불일치.',
    'https://github.com/python/cpython/issues/75494': '실제 목적지는2017년 Linux os.chflags 기능 이슈. 출발 댓글의 취소 API 문맥과 불일치.',
    'https://github.com/python/cpython/pull/31398': 'TaskGroup constructor의 name 제거와 create_task name 추가의 유지보수 결정. 전체 실패/await 계약은 없음.',
    'https://github.com/python/cpython/pull/31409': 'TaskGroup repr 표시 통일 변경. 본 요구의 실행 계약을 입증하지 않음.',
    'https://github.com/python/cpython/pull/31411': 'TaskGroup test13 불안정성 감소의 유지보수 변경. 전체 계약을 시험했다는 뜻으로 확대하지 않음.',
    'https://github.com/python/cpython/pull/31513': 'task.cancel 요청과 반복 취소 의미의 유지보수 논의. TaskGroup 첫 실패 정책 및 두 await 프로토콜 전체는 없음.',
    'https://github.com/python/cpython/pull/31559': 'uncancel 결과·CancelledError 전달·abort 중복의 수정. 현재 요구의 모든 조건을 별도로 입증하지 않음.',
}

def classify(row, case):
    url = row['url']
    doc, frag = urllib.parse.urldefrag(url)
    frag = urllib.parse.unquote(frag)
    loc = row.get('locator', '')
    facts = {case + '.A1': set(), case + '.A2': set()}
    wfacts = {case + '.A1': set(), case + '.A2': set()}
    reason = PURPOSES.get(doc, '실제 도착 창의 제목·정의와 관련 계약 문맥을 확인했으나 해당 복합 원자를 완전히 입증하는 범위를 확인하지 못함.')
    w_reason = '이 원문 전체의 계약을 판독했다고 주장하지 않음; W 전체 적격은 미확인.'
    w_status = '미확인'
    alignment = '3.11 pinned URL' if '/3.11/' in doc else '미확인'
    conflict = []
    a1, a2 = case + '.A1', case + '.A2'
    if row['read_status'] in ('failed', 'missing_fragment'):
        return facts, wfacts, '접속 실패 또는 실제 fragment 부재로 해당 도착 창 의미판독은 미확인.', w_reason, '미확인', alignment, conflict
    if doc in ('https://peps.python.org/pep-0654/', 'https://peps.python.org/654'):
        alignment = 'PEP Final/Python-Version3.11 metadata is in entry window; section-local availability separated'
        if case == 'C3':
            wfacts[a1].update(required[a1]); wfacts[a2].update(required[a2])
            w_status = 'confirmed_selected_sections'
            w_reason = '같은 PEP의 표제3.11·constructor 명세·except* 및 Unmatched Exceptions를 직접 대조. W는 한 원문에서 두 역할을 제공한다.'
            if not frag:
                facts[a1].add('availability_3_11')
                reason = '첫800 단어에서 Final/Python-Version3.11과 목차 확인. constructor와 자동 전파 명세는 이 창 밖.'
            elif frag in ('specification', 'exceptiongroup-and-baseexceptiongroup', 'rejected-ideas', 'make-it-impossible-to-wrap-baseexceptions-in-an-exception-group'):
                facts[a1].update(['exceptiongroup_constructor_boundary', 'baseexceptiongroup_constructor_boundary'])
                reason = '해당 절의 ExceptionGroup/BaseExceptionGroup 포장 경계를 읽음. 3.11 availability는 첫 화면의 별도 메타데이터 사실이며 이 절에 자동 합산하지 않음.'
            if frag in ('specification', 'except'):
                facts[a2].update(required[a2])
                reason += ' 같은 절에 subgroup 매칭·미처리 예외 전파·ordinary except와의 차이가 명시된다.'
            elif frag in ('unmatched-exceptions', 'chaining', 'reference-implementation'):
                facts[a2].update(['subgroup_matching', 'nonmatch_propagation'])
                reason = '부분 처리와 남은 예외의 전달 예제/구현 설명 확인. ordinary except 대비까지 이 작은 절에서 모두 입증한 것으로 세지 않음.'
            elif frag in ('recursive-matching', 'applying-an-except-clause-on-one-exception-at-a-time'):
                facts[a2].add('subgroup_matching')
                reason = '매칭 예외를 한 subgroup으로 처리하는 설명/예제. 미처리 그룹 자동 전파 전체 명세는 이 절 밖.'
            elif frag in ('forbidden-combinations', 'backwards-compatibility', 'make-exceptiongroup-extend-baseexception', 'extend-except-to-handle-exception-groups', 'a-new-except-alternative', 'allow-mixing-except-and-except-in-the-same-try'):
                facts[a2].add('ordinary_except_distinction')
                reason = 'ordinary except와 새 except*의 호환성·금지 조합·설계 차이를 확인. constructor+전파 전체를 대신하지 않음.'
            elif frag in ('programming-without-except', 'raising-exceptions-in-an-except-block', 'raising-new-exceptions', 'naked-exceptions', 'caught-exception-objects'):
                reason = '개별 처리·재발생·새 예외·naked exception의 해당 예제만 확인. 다른 절의 핵심 원자 전체를 이 작은 창으로 가져오지 않음.'
            elif frag in ('abstract', 'motivation', 'rationale', 'subclassing-exception-groups', 'the-traceback-of-an-exception-group', 'handling-exception-groups', 'how-to-teach-this'):
                reason = '해당 절의 소개·설계·분할/상속·traceback 문맥을 확인. subgroup/split 자체를 except* 자동 전파 전체와 동일시하지 않음.'
            elif frag and not any(facts.values()):
                reason = '실제 목차/주석/참고·감사·채택·저작권 구조 블록. 핵심 계약이 있는 다른 절은 기본 창에 포함하지 않음.'
        else:
            reason = 'PEP654는 exception-group 언어 기능의 문서. TaskGroup 동기 언급이나 예제만으로 C4의 실패 정책·두 await 프로토콜 전체를 입증하지 않음.'
    elif doc == 'https://docs.python.org/3.11/library/exceptions.html':
        w_status = 'confirmed_selected_sections'
        if case == 'C3':
            wfacts[a1].update(required[a1]);wfacts[a2].add('subgroup_matching')
            w_reason = '전체 동일 원문 중 Exception groups 절은 A1을 제공. split의 rest 반환은 except* 자동 재발생 명세가 아니다.'
            if loc == 'section#exception-groups':
                facts[a1].update(required[a1]); facts[a2].add('subgroup_matching')
                reason = '3.11 도입 표시와 두 constructor 경계를 직접 확인. except*의 subgroup 매칭은 있으나 split 반환값만으로 미처리 예외 자동 전파를 입증하지 않음.'
            else:
                reason = '기본 예외형·구체 예외·chaining 문맥. constructor 계약의 Exception groups 절은 이 기본 창 밖.'
        else:
            w_reason = '예외형과 그룹 constructor 문서는 C4의 TaskGroup 정책·async-with 호출을 명세하지 않는다.'
            reason = 'ExceptionGroup·KeyboardInterrupt·SystemExit 정의의 실제 도착 확인. TaskGroup 실행 계약과 다른 역할.'
    elif doc == 'https://docs.python.org/3.11/reference/compound_stmts.html':
        wfacts[a2].update(required[a2]);w_status='confirmed_selected_sections'
        w_reason = '같은 원문의 except* 또는 async-with 명세를 직접 대조; 해당 요구 A2는 W에서 제공됨. 다른 원자까지 제공하지 않음.'
        if case == 'C3' and loc in ('section#except-star','section#the-try-statement'):
            facts[a2].update(required[a2]);reason='except*의 부분 매칭·미처리 예외 재발생·ordinary except 차이를 실제 도착 절에서 확인.'
        elif case == 'C3' and loc == 'section#except-clause':
            facts[a2].add('ordinary_except_distinction');reason='ordinary except는 예외 객체 타입을 처리. 다음 except* 절의 subgroup/전파를 기본 창에 포함하지 않음.'
        elif case == 'C4' and loc == 'section#the-async-with-statement':
            facts[a2].update(required[a2]);reason='실제 async-with 확장에서 enter await, 예외 정보로 exit await, 정상 None 인수 exit await를 모두 확인.'
        else:
            reason='도착한 각주/다른 statement 절만 확인. 상위 chapter 전체로 넓혀 다른 절의 원자를 무료 제공하지 않음.'
    elif doc in ('https://docs.python.org/3/builtins/exceptions.html','https://docs.python.org/3/reference/compound_stmts.html','https://docs.python.org/3/tutorial/errors.html'):
        alignment='observed Python3.15.2, requested Python3.11; retrospective contract validation 미확인'
        conflict.append('version_not_pinned_to_requested_3_11')
        reason='실제 /3 링크는 Python3.15.2로 도착. 유사한 constructor/except* 설명은 읽었으나3.11 계약 검증으로 대체하지 않음.'
        if case=='C3':
            if 'exceptions.html' in doc:facts[a1].update(['exceptiongroup_constructor_boundary','baseexceptiongroup_constructor_boundary'])
            else:facts[a2].update(['subgroup_matching','nonmatch_propagation'])
        w_reason='W가 문서의 판을3.11로 바꾸지 않는다. 현재판 내용을 과거판 계약으로 소급 판정하지 않음.'
    elif doc == 'https://docs.python.org/3.11/reference/datamodel.html':
        w_status='confirmed_selected_sections'
        w_reason='W로 동기 exit의 예외 인수 의미를 함께 읽음. 두 async 메서드의 caller await를 풀어 쓴 별도 compound 원문은 무료 포함하지 않음.'
        if case=='C4':
            wfacts[a2].add('exception_forwarding')
            if loc=='section#asynchronous-context-managers':
                reason='두 async 메서드가 awaitable을 반환하고 동기 메서드와 의미가 유사하다는 명세. 두 결과를 caller가 await하는 절차는 직접 명시하지 않음.'
            elif loc=='section#with-statement-context-managers':
                facts[a2].add('exception_forwarding')
                reason='동기 exit의 예외 인수/None·억제 계약을 확인. 두 async 메서드 await의 전체 조건은 부족.'
            else:reason='객체 생성·특수메서드·수치/컨테이너·각주 도착. 해당 창은 async-with 두 await 프로토콜 전체를 제공하지 않음.'
        else:
            reason='object.__new__/__init__ 등 일반 생성 메서드 문서. ExceptionGroup-specific constructor 경계가 아님.'
    elif doc == 'https://docs.python.org/3.11/library/asyncio-task.html':
        w_status='confirmed_selected_sections'
        if case=='C4':
            wfacts[a1].update(required[a1]); wfacts[a2].add('exception_forwarding')
            w_reason='동일 원문의 Task Groups와 gather의 실제 정책 문단을 W에서 함께 읽으면 C4.A1 전체를 제공. 전체 문서도 __aenter__/__aexit__ 두 await 호출 명세는 부족.'
            if loc=='section#task-groups':
                facts[a1].update(['noncancel_first_failure','cancel_siblings','wait_all']);facts[a2].add('exception_forwarding')
                reason='TaskGroup 첫 비취소 실패·형제 취소·전체 대기·예외를 받은 exit를 확인. frozen A1의 gather 대비는 별도 절에 있으므로 전체 A1로 승격하지 않음.'
            elif loc=='section#running-tasks-concurrently':
                facts[a1].add('gather_default_distinction')
                conflict.append('gather_default_does_not_cancel_remaining_on_first_error')
                reason='gather 기본 첫 오류 전파는 다른 awaitable을 취소하지 않음. gather 자체 취소는 별개로 남은 작업도 취소한다. TaskGroup 정책의 양성 명세는 별도 절.'
            elif loc in ('section#coroutines','section#creating-tasks'):
                reason='coroutine/create_task 문맥의 TaskGroup 사용·이름 지원과 예제 종료 대기만 확인. 예제/추천을 일반 wait_all 조건으로 승격하지 않음.'
            elif loc=='section#timeouts':reason='timeout/wait_for는 시간 제한·대상 취소 계약. TaskGroup 형제 실패 정책의 대안으로 세지 않음.'
            elif loc=='section#task-object':reason='Task 취소·uncancel 상태 문맥. TaskGroup의 언급만으로 첫 실패 정책 및 async-with 프로토콜을 입증하지 않음.'
            elif loc.startswith('structural '):reason='실제 목차 backlink 블록의 링크 라벨뿐. 이 링크를 전체 chapter로 확대하지 않음.'
            else:reason='awaitable 정의 창. await 가능성과 특정 async-with 언어 프로토콜의 입증은 구별.'
    elif doc == 'https://docs.python.org/3.11/library/asyncio-exceptions.html':
        reason='CancelledError의 취소 신호·BaseException 상속을 확인. TaskGroup의 첫 비취소 실패 정책 전체와 별개인 예외형 근거.'
    elif 'discuss.python.org/t/accepting-pep-654' in doc:
        if case=='C3':facts[a1].add('availability_3_11')
        alignment='accepted PEP targeted3.11, technical contract not restated'
        reason='Steering Council의 PEP654 채택 및3.11 대상의 실제 결정문. constructor 경계와 subgroup 자동 전파 전체를 이 글에 대입하지 않음.'
    elif 'mail.python.org/archives/list/python-dev' in doc:
        alignment='pre-release proposal/discussion; final3.11 contract mapping 미확인'
        if 'MQ2UCSQ2ZC4FIGT7KSVI6BJA4FCXSOCL' in doc and case=='C3':
            facts[a1].update(['exceptiongroup_constructor_boundary','baseexceptiongroup_constructor_boundary'])
            reason='2021-03-20 저자의 두 그룹 타입·constructor 선택 변경 제안. 발표 당시 제안을 최종3.11 계약으로 자동 승격하지 않음.'
        else:reason='PEP 피드백 요청 또는 except* 표기 논의의 첫800 단어. 초안 토론과 최종판의 전체 호출 계약을 구별.'
        w_reason='장문의 전체 메일 스레드는 정독하지 않았다. W 전체 증거는 미확인.'
    elif doc=='https://docs.python.org/3.11/whatsnew/3.11.html':
        if case=='C3':
            facts[a1].add('availability_3_11');facts[a2].add('subgroup_matching')
            reason='도입판과 subgroup 기능 개요. constructor 경계·자동 미처리 전파는 요약 절 밖.'
        else:
            facts[a1].add('wait_all');reason='TaskGroup 종료 대기·추천 개요. gather 기본 오류 동작과 두 async 메서드 await는 없음.'
        w_status='confirmed_selected_sections';wfacts={k:set(v) for k,v in facts.items()}
        w_reason='release의 관련 기능 절을 확인. 전체 변경 목록의 다른 기능을 해당 계약 증거로 합치지 않음.'
    elif doc.endswith('/commit/602630ac1855e38ef06361c68f6e216375a06180'):
        reason='커밋 첫800 단어는 설계 설명과 __aenter__ 정의 시작까지. 뒤의 취소/대기 코드 전체는 기본 창 밖.'
        alignment='fixed initial implementation commit; final3.11 release contract equivalence not assumed'
        w_status='confirmed_selected_code_regions'
        w_reason='동일 커밋 HTML의 taskgroups.py __aexit__(70–153), _abort(174–179), _on_task_done(181–232)를 읽음. 자식 실패·취소·대기는 있으나 gather 대비와 언어가 두 메서드를 await하는 expansion은 없음.'
        if case=='C4':
            wfacts[a1].update(['noncancel_first_failure','cancel_siblings','wait_all'])
            wfacts[a2].add('exception_forwarding')
    elif ('issues/90908' in doc or 'issue46752' in doc or 'bpo=46752' in doc or 'pull/31270' in doc):
        wait_statement_source=(doc in ('https://github.com/python/cpython/issues/90908','https://bugs.python.org/issue46752','https://bugs.python.org/issue?@action=redirect&bpo=46752') and frag in ('','issuecomment-1093944756'))
        if case=='C4' and wait_statement_source:facts[a1].add('wait_all')
        reason='유지보수자의 TaskGroup 종료 대기·새 작업 허용·취소 상태 논의. 명세 전체를 증명하는 대신 실제 이 창의 하위사실만 보존.'
        if frag=='issuecomment-1093944757':reason='TaskGroup 추가 changeset 링크를 알린 댓글. 링크된 코드 내용을 이 도착 댓글에 합치지 않음.'
        if frag=='issuecomment-1093944758':reason='uncancel 필요성 시험·C/Python 구현·문서 보완의 TODO 댓글. 완료된 전체 계약 증명으로 세지 않음.'
    elif doc.startswith('https://github.com/login') or ('github.com/' in doc and '/python/' not in doc and '/edgedb/' not in doc) or 'issues?q=' in doc:
        reason='실제 로그인·개인 프로필·이슈 목록 탐색 화면. 원문 기능 계약으로 인정하지 않으며 별도 개인 정보는 연구 결과에 전재하지 않음.'
        w_status='navigation_only';w_reason='기능 명세가 아닌 탐색 화면.'
    return facts,wfacts,reason,w_reason,w_status,alignment,conflict

results=[]; ledger=[]
for idx,row in enumerate(arrivals,1):
    url=row['url'];doc,frag=urllib.parse.urldefrag(url)
    cases=sorted({x['case_id'] for x in row['source_occurrences']})
    sid=f'C-H2-{idx:03d}'
    confirmed=row['read_status'] not in ('failed','missing_fragment')
    record=dict(source_id=sid,url=url,document_url=doc,source_cases=cases,
                source_candidate_ids=sorted({x['candidate_id'] for x in row['source_occurrences']}),
                http_status=row['http_status'],connectivity_success=row.get('access_success',False),
                destination_section_confirmed=confirmed,fragment_exists=row.get('fragment_exists'),
                semantic_review_status='definition_and_relevant_contract_contexts_read' if confirmed else '미확인',
                locator=row.get('locator'),html_sha256=row.get('html_sha256'),
                actual_user_response='미확인',pool_membership_changed=False,
                reading_method='Declared destination window: opening/definition and exact relevant contract contexts; no exhaustive reading claim for unrelated long content.',
                per_case=[])
    reasons=[]
    for case in cases:
        f,wf,reason,wreason,wstatus,alignment,conflicts=classify(row,case)
        reasons.append(reason)
        supported=[a for a,v in f.items() if set(required[a])<=v and confirmed]
        partial=[a for a,v in f.items() if v and a not in supported]
        wsupported=[a for a,v in wf.items() if set(required[a])<=v and wstatus.startswith('confirmed')]
        verdicts=[]
        for a in f:
            verdict='예' if a in supported else ('조건부' if f[a] else ('미확인' if not confirmed else '아니오'))
            verdicts.append(dict(atom_id=a,atom_text=atom_text[a],verdict=verdict,
                                 counts_as_proven=a in supported,
                                 proven_subconditions=sorted(f[a]),
                                 missing_subconditions=sorted(set(required[a])-f[a]),reason=reason))
        record['per_case'].append(dict(case_id=case,required_version='3.11',version_alignment=alignment,
                                      supports=supported,partial=partial,unknown=[a for a in f if not confirmed],
                                      atom_verdicts=verdicts,subcondition_facts={a:sorted(v) for a,v in f.items()},
                                      full_document_supports=wsupported,
                                      full_document_partial=[a for a,v in wf.items() if v and a not in wsupported],
                                      full_document_subcondition_facts={a:sorted(v) for a,v in wf.items()},
                                      full_document_review_status=wstatus,full_document_reason=wreason,
                                      conflicts=conflicts,complete_alternative_ids=[],
                                      limitation='Do not add this destination to the frozen six-slot pool or combine separate trials. Composite atom partials remain partial.'))
    record['verified_fact']=' / '.join(dict.fromkeys(reasons))
    results.append(record)
    rec=access.get(doc,{})
    final=rec.get('final_url',doc)
    duplicate=urllib.parse.urldefrag(final)[0]
    if doc=='https://peps.python.org/654':duplicate='https://peps.python.org/pep-0654/'
    if '/accepting-pep-654-exception-groups-and-except/10813' in doc:duplicate='https://discuss.python.org/t/accepting-pep-654-exception-groups-and-except/10813'
    if 'issues/90908' in final or 'bpo=46752' in doc or doc.endswith('/issue46752'):duplicate='https://github.com/python/cpython/issues/90908'
    ledger.append(dict(source_id=sid,original_url=url,
                       pinned_url_or_version=(rec.get('published_version_display','미확인')+'; HTML SHA256 '+str(row.get('html_sha256',rec.get('sha256','미확인')))),
                       publisher=urllib.parse.urlparse(final).hostname or '미확인',
                       event_or_publication_date='미확인',checked_utc=row['checked_utc'],locator=row.get('locator'),
                       source_kind='second_hop_primary_or_navigation_direct_read' if confirmed else 'second_hop_access_or_fragment_failure',
                       verified_fact=record['verified_fact'],
                       limitation='Supplemental route audit, not asserted as a newly counted independent original. Only the stated window and selected relevant contexts were read; user response 미확인. Missing fragments and failures do not prove semantic absence.',
                       question_ids=['Q3','Q4','Q5','Q6'],case_ids=cases,duplicate_group=duplicate,counted=False))

write('coding.json',dict(protocol='Unchanged frozen C3/C4 atoms; supports means every literal subcondition is proven inside this scoped destination. No A/B/C calculation.',
                          subcondition_decomposition=required,atom_text=atom_text,url_count=len(results),
                          case_destination_rows=sum(len(x['per_case']) for x in results),
                          complete_alternative_ids=[],destinations=results))
(P/'control-second-hop-sources.jsonl').write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in ledger)+'\n')

trials=load('independent-trials.json')
for t in trials:
    if t['case_id']=='C3':
        t.update(semantic_review_status='confirmed both unchanged atoms in this independent pair',
                 first_window_facts={'C3.A1':['availability_3_11']},
                 second_window_facts={'C3.A1':['exceptiongroup_constructor_boundary','baseexceptiongroup_constructor_boundary'],
                                      'C3.A2':required['C3.A2']},
                 supports=['C3.A1','C3.A2'],complete_requirement_confirmed=True,
                 evidence_locators=['PEP entry Python-Version3.11 within first800',
                                    'section#specification / ExceptionGroup and BaseExceptionGroup constructor paragraphs',
                                    'section#specification / except* introductory comparison and Unmatched Exceptions'])
    else:
        t.update(semantic_review_status='A2 confirmed; A1 absent in this independent pair',
                 first_window_facts={'C4.A2':['awaitable-return requirement only; not counted as await execution']},
                 second_window_facts={'C4.A2':required['C4.A2']},
                 supports=['C4.A2'],complete_requirement_confirmed=False,
                 evidence_locators=['section#the-async-with-statement / equivalent expansion: awaited aenter; awaited aexit with sys.exc_info or None triplet'],
                 missing_atoms=['C4.A1'])
write('independent-trials.json',trials)

summary=dict(href_occurrences=targets['strict_outgoing_occurrences'],unique_urls=len(results),document_requests=len(access),
             http200_documents=sum(x['http_status']==200 for x in access.values()),
             http_failure_documents=sum(not x['access_success'] for x in access.values()),
             resolved_destinations=sum(x['destination_section_confirmed'] for x in results),
             missing_fragments=sum(x.get('fragment_exists') is False for x in results),
             failed_url_access=sum(not x['connectivity_success'] for x in results),
             independently_checked_two_step_trials=len(trials),
             independent_complete_trials=[x['trial_id'] for x in trials if x['complete_requirement_confirmed']],
             source_ledger_rows=len(ledger),new_independent_primary_sources_claimed=0,
             actual_user_response='미확인',full_document_unreviewed_destinations_are_unknown=True,
             by_case={})
for case in ['C3','C4']:
    relevant=[(r,p) for r in results for p in r['per_case'] if p['case_id']==case]
    summary['by_case'][case]=dict(unique_destination_urls=len(relevant),
                                  destination_atom_proofs=sum(len(p['supports']) for r,p in relevant),
                                  fully_proven_atoms={a:sum(a in p['supports'] for r,p in relevant) for a in required if a.startswith(case)},
                                  partial_atom_rows=sum(bool(p['partial']) for r,p in relevant),
                                  unknown_destination_rows=sum(not r['destination_section_confirmed'] for r,p in relevant))
write('summary.json',summary)
print(json.dumps(summary,ensure_ascii=False))
