"""Render the committed case records into the requested four-table report.

This is a presentation script, not a new adjudicator. Frozen messages and
original records are never rewritten. Narrative judgments are explicitly
postseal and their evidence is linked in the output.
"""
import csv
import json
from pathlib import Path

P = Path(__file__).resolve().parent
S = {r['id']: r for r in json.loads((P / 'sources.json').read_text())}
M = json.loads((P / 'report-case-matrix.json').read_text())['cases']
A = {r['case_id']: r for r in M}
MET = json.loads((P / 'evidence/metrics.json').read_text())
CLAIMS = json.loads((P / 'report-claims.json').read_text())


def safe(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def link(label, url):
    return f'[{label}]({url})'


def source(sid, loc=True):
    r = S[sid]
    x = link(sid, r['url'])
    where = r['read_locations']
    if isinstance(where, list):
        where = '; '.join(where)
    return x + (' — ' + where if loc else '')


def table(headers, rows):
    out = ['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |']
    out += ['| ' + ' | '.join(safe(cell) for cell in row) + ' |' for row in rows]
    return '\n'.join(out) + '\n\n'


VALUE_NOTES = {
 'S01': '작성자 T0에 생성 의도 명시; 1월1일10:16:22.660Z 자가 앱 해결 보고. 후속은 CREATE 기술 설명이지 봉인Q 새 값이 아님.',
 'S02': '작성자 T0에 -o mysql / ./ex1.db 명시. 30일 내 작성자 재응답·실행 결과 미확인.',
 'S03': 'OFF 유지가 필수인지 30일 내 작성자 답 없음. 이미 교체할 view의 순서 변경 A는 이 값 없이 유지.',
 'S04': '작성자 1월6일04:57:01.939Z committed 주장. 11:38:19.078Z 재현 편집판에는 COMMIT 없는 코드·실패 로그. 성공 반환 값은 미확인.',
 'S05': '제3자가 serialized 조건을 설명. 작성자의 실효 mode 값·호출 순서는 30일 내 미확인.',
 'S06': '작성자 1월5일21:21:13.731Z 가능성에 관심 표명. 소스 형태·판의 답이나 적용 성공은 아님.',
 'S07': 'T0에 PG autovacuum daemon 명시. 작성자 1월7일02:39:32.391Z 문서 비교·독서 보고; 이후 UPDATE/DELETE 목적은 추가 범위.',
 'S08': 'T0 JS req.body 값 명시. 작성자 1월6일08:43:36.044Z 다른 실제 조언 뒤 같은 오류·두 열로 바꾼 스키마 보고.',
 'P01': 'T0에 부모 행 명시. 1월2일19:41:56Z 작성자의 data-entry 목적은 최초 조회 설명 뒤 공개; 실제 목적 질문은 그보다 뒤.',
 'P02': '첫 답이 실제 SELECT 반환을 물었지만 작성자 답 없음. 계획 출력은 실제 전체 값 조회 성공이 아님.',
 'P03': '재게시의 같은 작성자 1월6일10:20:49Z local 발화. 실제 ID 테이블인지 예제 결과집합인지 미확인; 엄격0/넓은 해석1.',
 'P04': '30일 내 작성자 추가 답 없음. 기존 dump 파일의 데이터·시점 경계는 T0 재독으로 확인한 조건.',
 'P05': 'T0부터 ONE 목적 명시. 다른 갱신을 절대 금지하는 강도·실제 설치판은 미확인; 구문 판정에는 강도 질문 불필요.',
 'P06': 'SQL/동일 geography·출력 값 답 없음. 연결된 재현을 90일 원장까지 찾았으나 미관측.',
 'P07': '작성자 후속에서 DO와 Oracle 전체 이식 목적을 추가 표현. 봉인 Q의 loop 값과 새 실행은 미확인.',
 'P08': '작성자 1월8일·11일 순서/pop·사전/loop·hstore를 논의. 숫자 text 변환 허용이라는 봉인 값은 미확인.',
 'C01': 'T0부터 브라우저 요청의 cookies. 작성자 1월2일 빈 cookiejar 시도 보고는 다른 시도의 결과이며 새 목적값 아님.',
 'C02': 'NAT는 제3자 설명. 작성자 1월22일 감사 두 답에 값·실행 결과 없음.',
 'C03': 'T0부터 전체 요청 구간과 byte 전송 구간을 대비. 30일 내 작성자 추가 결과 없음.',
 'C04': '실제 답변자는 추가 문자 od 출력을 요청했으나 작성자 답 없음. 봉인 Q는 다른 변수인 CR/LF 보존 여부.',
 'C05': '작성자 1월9일17:40:14Z 빈 임시 디렉터리·move/rename 기존 workflow를 자발 고지. basename 필수성은 부분값.',
 'C06': '공급자이자 질문자: 1월21일 PR, 2월1일 새 --json 구현, 2월5일 이후 범위 설명. T0 기존 필수사실의 직접 답 아님.',
 'C07': 'T0부터 새 CLI 문법 제안. 1월21일21:26:18Z 실제 대상 사용자 질문에 답했으나 봉인 Q와 다른 변수.',
 'C08': '원 요청에 30일 내 첫 답·작성자 값 없음. 우측 검열이며 거절/실패가 아님.'
}

CHANGE_NOTES = {
 'S01':'선택 유지; 작성자 새 자가 실행 성공. 사전 답 문구 노출로 엄격23에서 제외.',
 'S02':'실행파일명 정정은 즉시 가능; 프로그램 전체 DB 조회는 여전히 미확인.',
 'S03':'A 유지. C의 분기 선택·참조 의미 미확정으로 전체 승인 보류; 넓은 A 가능성 해석은 별도.',
 'S04':'주장·재현 불일치 미해소; 성공 COMMIT 조건을 채웠다고 볼 수 없음.',
 'S05':'두 API mode 조건 설명은 가능; 원래 statement 작업 순서·성능 승인 보류.',
 'S06':'후보 관심만 관측; 소스형태 한 값으로 버전까지 해결되지 않음.',
 'S07':'원래 비교 설명 유지; 문서 독서 보고. 추가 UPDATE/DELETE 물리 동작은 별도 요구.',
 'S08':'바인딩 제안 유지. 실제 다른 조언 실패를 I/C 결과로 세지 않음; C의 NOT NULL 누락.',
 'P01':'부모 조회 설명 유지. 새 data-entry 표현을 T0 전체 목적에 소급하지 않음.',
 'P02':'진단 보류 유지; EXPLAIN과 실제 값 접근 구별.',
 'P03':'실제 ID 원천 미확인 유지. 넓은 local 해석만 B 적합성 변화1; 원 예제 B는 T0부터 부적합.',
 'P04':'원판 재독으로 C 근거부족1 확인. 재접속 가능성과 기존 dump 대체 가능성은 다름.',
 'P05':'14.1의 음성 구문 답 유지. 실제판 미상은 별도.',
 'P06':'동일값 질문만으로 원인 판정 불가. SQL·측정·환경 보류.',
 'P07':'SQL 함수 존재 설명 유지; 전체 Oracle 호환 미확인.',
 'P08':'표현 후보 유지; 추가 순서/pop와 전체 collection 요구는 별도 미확인.',
 'C01':'원판 재독 교정; 브라우저 지원 목표를 curl 옵션 설명으로 승인하지 않음.',
 'C02':'관측주체별 주소 설명 가능; 실제 공인 주소·NAT 값은 미확인.',
 'C03':'속도 지표 설명 유지; 사용 결과 미확인.',
 'C04':'-d/--data-binary 조건부 안내 가능; 실제 추가 byte 원인 미확인.',
 'C05':'선택 유지; 질문 없는 설명 수용·기존 workflow 보고. 신규 실행 미확인.',
 'C06':'새 기능 개발 관측. 새 commit은 T0 제안판의 사용 성공이 아님.',
 'C07':'설계 대상 논의, 구현 미확인. 신규 문법을 현행 기능으로 승인하지 않음.',
 'C08':'후보0·원인 보류 유지; 미연결 2월 새 질문을 후속 성공으로 붙이지 않음.'
}


def action_ref(row):
    refs = row['user_action']['exact_action_evidence']
    return '; '.join(link('발화 ' + x.get('occurred_utc', ''), x['url']) + ' ' + x.get('locator', '') for x in refs[:1])


def coverage_text(row):
    # Citation audits are postseal checks, separate from the frozen input.
    extra = P / f"streams/{'sqlite' if row['family']=='S' else 'curl'}/citation-coverage.json"
    base = []
    for st in ('I','C'):
        b = row['strategy_evidence'][st]['all_needed_technical_sources_cited']
        base.append(st + ':' + ('예(제한 주장)' if b is True else '아니요(조건 누락)' if b is False else '미확인'))
    if row['family'] in ('S','C') and extra.exists():
        audit=json.loads(extra.read_text())
        if row['family']=='S':
            records={x['strategy']:x for x in audit['records'] if x['case_id']==row['case_id']}
            values={st:records[st]['all_necessary_provider_evidence_cited_for_limited_message'] for st in ('I','C')}
            axis='봉인 메시지 안 제공자 링크의 완결'
        else:
            rec=next(x for x in audit['cases'] if x['case_id']==row['case_id'])
            values={st:rec['strategies'][st]['all_message_claims_supported'] for st in ('I','C')}
            axis='연구기록 인용의 제한 명제 지지'
        flags='; '.join(st+'='+('예' if values[st] is True else '아니요' if values[st] is False else '해당 없음(후보 없음)') for st in ('I','C'))
        return axis+': '+flags+f"; [명제별 점검]({extra.relative_to(P).as_posix()}) {row['case_id']}. " + ', '.join(st + ' 전체승인=' + ('예' if row['strategy_evidence'][st]['whole_original_goal_use_approval'] else '보류/해당 없음') for st in ('I','C'))
    return '; '.join(base) + '; 근거 위치와 미확인 조건은 이 행·행렬에 명시'


def first_tables():
    out = '# AF-RES-026 · 부분 설계에서 먼저 물을 조건\n\n'
    rows=[]
    for r in M:
        cid=r['case_id']; f=r['first_request']; q=r['frozen_question']
        places='; '.join(x['locator'] for x in f['goal_exact_locations'])
        req='; '.join(x['text']+' ('+x['locator']+')' for x in f['required_conditions'])
        rows.append([cid+' · '+f['submitted_utc'], link(f['initial_goal'],f['url'])+' — '+places+'; 필수: '+req,
          ('OFF 유지가 필수인지(봉인 변수 요약의 방향 오류를 사후 보정)' if cid=='S03' else q['variable'])+' / **미전송 Q:** '+q['message'], VALUE_NOTES[cid]+(' '+action_ref(r) if action_ref(r) else ''),
          CHANGE_NOTES[cid], '미확인: '+r['remaining_unknowns']['minimal_next_evidence']])
    out += table(['질문 ID·원판 시각','최초 목적·필수 조건의 원문 URL·위치','빠진 변수와 봉인한 질문','실제 응답 주체·값·시점','사용 또는 판정 변화','미확인'],rows)
    rows=[]
    groups=[('all_24','전체/원판24'),('strict_unexposed','답 미노출23'),('extra_original_corroboration','추가 원판보강18'),('non_supplier_requesters','비공급자22')]
    for key,label in groups:
        g=MET['subsets'][key]; n=g['denominator']
        for st in ('I','C','Q'):
            ds=g['strategy_dispositions'][st]
            if st=='Q':
                verdict=f"승인 해당 없음; 기존값 {g['counts']['q_value_already_T0']}/{n}, 새값0/{n}, 변수 미확정 {g['counts']['q_still_unconfirmed_after_window']}/{n}"
            else:
                verdict=f"제한 근거응답 {ds.get('supported_limited',0)}/{n}; 그중 전체사용승인 {g['grounded_full_use_approvals_by_strategy'][st]}/{n}; 확인된 기술오승인0; 근거부족 {ds.get('unsupported_approval',0)}; 보류 {ds.get('hold',0)}"
            progress=f"공통 실제 관측 진전 {g['counts']['reported_progress_broad']}/{n}; 외부사용자 신규성공 {g['counts']['external_user_new_successful_execution']}/{n}. 주30일/별도구현90일; 전략에 귀속하지 않음"
            cost=f"공통 주왕복 {g['actual_primary_roundtrip_pairs']}쌍; 구현열은 C06 포함시1. 가상 {('답을 받으면 최소1' if st=='Q' else '문구 발송에0')}회; 실제 전략 효과 아님"
            example={'I':'C01 목표 재독; S02 한정 수정≠전체 조회','C':'P04 근거부족; S08 조건누락; S03 미확정 분기','Q':'기존8 재질문; P03/S04/C05 약한값; C08 후보없음'}[st]
            rows.append([st+' · '+label,f"이 행 {n}; 전체24/최초판24/같은변수 직접답0(비율 해당 없음)",verdict,progress,cost,example])
    out += table(['전략 I·C·Q','전체·최초판 확정·직접 답 분모','근거 있는 승인·오승인·보류','실제 진전 보고·관측 창','실제 왕복·대리 비용','반례'],rows)
    rows=[]
    for r in M:
        cid=r['case_id']; cs=r['frozen_candidates']
        uses='; '.join(link(c['candidate_id']+': '+c['use'],c['source_snapshot_url'] or c['frozen_candidate_url']) for c in cs) if cs else '후보 없음; 원 요청 유지'
        ids=list(dict.fromkeys(c['source_id'] for c in cs if c['source_id']))
        extra={'S05':['S-D01'],'S08':['S-TD02'],'P08':['P-D11','P-D12'],'C06':['C-IM01']}.get(cid,[])
        ids=list(dict.fromkeys(ids+extra))
        refs='; '.join(source(sid) for sid in ids) if ids else '해당 없음(후보 부재); 원문 입력의 불충분성이 보류 근거'
        if cid in ('S08','C06'): refs+='; S-TD02/C-IM01 중 해당 자료는 사후 검증·새 구현이며 T0 후보 추가 아님'
        action = action_ref(r) or '30일 내 새 실행 성공 보고 미확인'
        rows.append([cid,uses,CHANGE_NOTES[cid],refs,coverage_text(r),action+'; '+r['remaining_unknowns']['canonical_limit']])
    out += table(['사례 ID','최초판의 사용과 후보 URL','추가 사실로 유지·변경된 제안','당시 공식 근거 절','필요한 근거 전부 인용 여부','사용자 행동·대체 설명'],rows)
    rows=[]
    for q in CLAIMS:
        refs='; '.join(source(sid) for sid in q['source_ids'])
        refs+='; '+ '; '.join(link(x,x) for x in q['local_evidence'])
        rows.append([q['q']+' · '+q['claim']+' 적용: '+q['scope'],refs,q['counts'],q['counterexample_search'],q['unknown_and_minimum']])
    out += table(['Q 번호·주장·적용 범위','근거 원문 URL·정확한 절 또는 실행 영수증','확인한 내용·분자·분모','반례를 찾은 곳과 결과','미확인·판단을 바꿀 최소 자료'],rows)
    return out


def narrative():
    return f'''## 결과를 읽는 기준

이 조사에서 설계자에게 넘길 수 있는 규칙은 **사용자가 원하는 다음 행동을 먼저 좁히고, 그 행동의 판정을 바꾸는 미상 변수만 요청하라**는 것이다. 최초 글의 주체·입력·판을 다시 읽어 해결되는 문제를 추가 질문의 성과로 세면 안 된다. 조건별로 근거가 완결된 설명은 사용자가 스스로 분기를 고르게 할 수 있지만, 그것이 전체 구현의 안전성이나 실제 사용 성공을 보증하지는 않는다.

24건의 봉인 Q 가운데 값이 원래 있던 것은 **8건**이다. 후속 작성자의 명확한 기존 사실로 새로 채운 값은 엄격한 기준에서 **0건**, 같은 변수를 실제로 물어 작성자가 직접 답한 완결 쌍의 분모도 **0건**이다. 이는 질문이 무효라는 결과가 아니다. 실제로 보내지 않은 Q와 실제 응답자의 다른 질문을 구별했을 때 남는 공개 기록의 결과다. 모호한 P03, 상충하는 S04, 부분값인 C05를 모두 넓게 인정하면 값은0–3건, 후보 변화는 P03에 한해0–1건이다. 이 범위는 통계적 신뢰구간이 아니라 코딩 선택의 민감도다. [정본 집계](evidence/metrics.json), [판정 교정](adjudication-overrides.json), [24건 행렬](report-case-matrix.json).

I의13건과 C의14건은 **한정된 설명·부적합 답·조건부 경로가 근거를 갖춘 수**다. 원래 목표의 필수조건을 포함하고 T0로 사용이 정해진 전체 승인만 세면 I4건, C2건이다. 미노출23건에서는 I3/C1이다. 교차검토에서 S08 C의 NOT NULL 누락과 S03 C의 미확정 분기를 발견해 전체 승인을 줄였으며, 원래 문구나 계열 태그를 지우지 않았다. S03의 가능한 A 경로만으로 C의 전체 승인까지 인정하는 넓은 정의라면 C3이라는 민감도는 남긴다. [집계 정의](ANALYSIS_RULES.md), [교차검토](evidence/integration-review.json).

표와 파일의 **0건**은 정한 관측·분류에서 해당 사건을 확인하지 못했다는 수다. **해당 없음**은 직접 답 분모0, 후보 없는 기술인용처럼 계산할 대상이 없는 경우다. **관측 실패**는 raw 원문·미러 차단이나 삭제 때문에 읽지 못한 상태다. **미확인**은 필요한 사실·동일성·결과가 공개 근거로 정해지지 않은 상태다. 30일 무응답은 우측 검열이며 거절·실패·무능력과 동일하지 않다.

## Q1 · 무엇을 최초 요청이라고 고정했는가

사전 원장은 SQLite 공식 Forum, PostgreSQL pgsql-general, curl-users다. 2022–2024 기간과 프로젝트당8건, 최초 제출 시각 오름차순을 먼저 정했으며 세 계열 모두 2022년1월에 상한에 도달했다. 따라서 이 결과가 뒤의3년 전체를 대표한다는 주장은 하지 않는다. 원장149행은 독립 질문149개가 아니다. root심사40건 중24건을 포함하고16건을 제외했으며, 답장 metadata87행과 상한 뒤 미심사22행을 따로 남겼다. curl 제외 root3건은 제목·원장상 공지/전체 로드맵이라는 판단이며 전문 판독으로 부풀리지 않았다. 답·수락·명확화·성공은 선정 기준에 쓰지 않았다. [사전 SCOPE](https://github.com/laadkke-arch/agentflow-open/blob/cecbfb981b9a7ccfd59f7bc40a23445a19d020fa/docs/workstreams/research/AF-RES-026/SCOPE.md), [원장](frame.csv).

SQLite는 artifact의 본문·D시각과 개정 predecessor 및 첫 답의 연결을 읽고 raw SHA3를 확인했다. curl은 완전한 최초 본문과 Message-ID, Date, Hypermail isoreceived를 분리했다. C02의 제출과 수신은 수 시간 차이가 나므로 Date를 서버시각으로 바꾸지 않았다. PostgreSQL은 Message-ID로 식별되는 보존 전문과 응답 순서를 연결했으나 raw RFC822/Received를8건 모두 확보하지 못했다. 공식 raw는 인증/리다이렉트, 공개 대체 미러는403 등의 한계가 있었고 그 실패를 기록했다. P04/P05는 첫 답에 인용된 질문을 해시로 추가 대조했지만, P04의 인사·감사·서명까지 같았다고 쓰지 않는다. {source('C-R02')}; [PG 대체 시도](streams/postgres/initial-mirror-attempts.json), [인용 대조](streams/postgres/initial-quote-crosschecks.json).

따라서 **공개 보존 전문·식별·응답순서 연결24**, **추가 교차근거18**, **답 미노출23**은 별개의 수다. 보강18과 미노출23의 교집합은17이다. raw 서버 원형이 없다는 불확실성을 “원판 미확인0”이라는 아카이브 식별 집계로 없애지 않는다. S01은 검색 중 답변 한 문장이 노출됐고 이 사건은 교체하지 않았다. 전체24와 미노출23의 결과를 함께 보존하는 것이 사후에 유리한 사례만 남기지 않는 방법이었다. [T0 노출 기록](evidence/T0-review.md), [봉인 영수증](evidence/t0-seal.json).

## Q2 · 처음부터 알 수 있던 조건과 잘못 읽은 조건

원판 전문과 그때 연결된 첨부·공식 비교판으로 목표, 입력·출력, 판, 플랫폼, 호출 주체를 따로 적었다. 동기/비동기는 코드의 순서에서 해석한 것과 글에 직접 쓴 것을 구별했고, 없으면 미상으로 남겼다. “브라우저 요청 cookies”인 C01을 curl이 새 요청을 보내는 문제로 바꾸거나, S08의 JS 값을 다시 묻는 것은 정보를 얻는 질문이 아니다. P01의 부모 행 저장과 S07의 autovacuum daemon도 원판에 있었다.8건은 S01/S02/S07/S08/P01/C01/C03/C07이며, 나머지16건을 모두 실제 무응답 사례라고 부르지는 않는다. [필드별 위치](field-locations.jsonl), {source('C-R01')}, {source('S-S08',False)}.

최초 목표의 판정에 필요한 사실이 충분했던 사례는 S01/S03/S07/S08/P01/C03의6건이다. 이 값은 각 사례의 선언된 답 범위와 당시 비교판에 대한 연구자 판정이며, 설치 환경의 모든 사실이 명시된6건이라는 뜻은 아니다. P05의 14.1 비교판 구문 답을 포함하면7건이지만, 이 판을 질문자의 실제 설치판으로 바꾸면 안 된다. P05는 이미 publication 하나만 원한다고 명시했고, 금지의 강도를 더 알아도 14.1 REFRESH 구문이 이름 하나를 받는지의 답은 바뀌지 않는다. {source('P-S05')}; {source('P-D07')}.

필수·선호·불필요·금지는 서로 대체할 수 없다. S03의 legacy OFF는 예제의 설정이며 반드시 유지해야 한다고 명시돼 있지 않아 필수 여부는 미확인이다. P05의 단일 publication 목적을 단순 선호로만 축소하면 원 요청의 경계를 잃는다. C06의 wiki에서 JSON 응답 특별 처리를 제안하지 않은 것은 금지가 아니다. 이후 제3자가 제안한 응답처리를 T0 작성자의 숨은 필수조건으로 넣지 않았다. S06는 여러 빌드 시스템을 쓰는 이유를 묻지 말라고 했지만, 소스형태·판까지 질문하지 말라는 말은 아니었다. {source('S-S03',False)}, {source('S-S06',False)}, {source('C-W01')}.

원판을 재독해 이 사실을 알아낸 것은 **연구자의 판독 교정**이다. 작성자가 새 정보를 알려줘 판정이 좋아졌다는 것으로 집계하지 않았다. 이는 고정 입력021의 발췌/전문 및 동기·비동기 혼동,022 A01/A19의 이미 알던 기술에 대한 조건 교정과 이어지는 구분이다. 이번 조사에서는 앞선12질문을 다시 채점하거나 발견률·경제효과로 환산하지 않았다. [고정 입력·manifest](SCOPE.md), [조건 교정](adjudication-overrides.json).

## Q3 · 즉답·조건부 답·한 문장 질문의 실제 모양

후속을 의도적으로 읽기 전 세 계열8건씩 I/C/Q를 커밋하고 원격에서 읽었으며, 전체24건·72문구를68fc97f에 봉인한 뒤 후속 전문을 열었다. 문구당 URL·공백 포함300자 상한과 사례당 후보최대2를 지켰다. 실제 후보는45개이며 C08처럼 후보가 없어도 원 질문을 유지했다. 원 문구와 입력 해시는 지금도 같고, 나중의 더 좋은 문구로 교체하지 않았다. [봉인본](https://github.com/laadkke-arch/agentflow-open/blob/68fc97fadceb46f9945a71fcc53730e29f6c62bf/docs/workstreams/research/AF-RES-026/frozen-responses.jsonl), [문구 예시](examples.md).

즉답의 좋은 범위는 C03처럼 특정 판의 속도 지표를 설명하거나 S02처럼 실제 실행파일명을 바로잡는 것이다. 뒤에 필요한 모든 구현을 보증할 필요 없이, 질문에서 이미 정해진 작은 동작에 근거 링크를 줄 수 있다. 반대로 S02 프로그램에는 SELECT가 없어 파일명 수정만으로 “DB 읽기 전체 성공”을 승인하지 않았다. {source('C-D09')}; {source('C-D10')}; {source('S-S02',False)}.

C04에서는 CR/LF 보존이 필요하면 --data-binary, 줄바꿈을 제거하는 입력 처리라면 -d라는 조건을 두 공식 절로 안내할 수 있다. 그러나 실제 추가 byte가 무엇인지는 이 조건만으로 진단되지 않는다. S05에서는 같은 sqlite.h.in의 mutex 계약 한 링크로 두 mode의 차이를 설명할 수 있다. 그 링크가 statement 결과수명과 여러 호출의 논리적 순서까지 알아서 보증하는 것은 아니다. 따라서 **조건부 링크 하나로 제한된 판정을 설명할 수 있음**과 **링크 하나를 보고 사용자가 전체 문제를 해결했음**을 분리했다. {source('C-D04')}; {source('C-D05')}; {source('S-D01')}.

표3의 인용 점검에서는 연구기록이 기술 명제를 지지하는지와 봉인 메시지 안에 필요한 제공자 링크가 모두 들어 있는지를 구별했다. SQLite 메시지16개 중6개(S01/I, S02/I·C, S06/C, S08/I·C)는 후자의 인용이 빠졌다. S08 I의 NOT NULL은 같은 역사판 테스트를 T1에 읽어 보강했으므로 이 근거를 T0에 이미 인용했다고 쓰지 않는다. curl C01/C는 JS 미실행에서 요청 대체의 일반 불가능으로, C02/I·C는 local_ip 정의에서 외부 서비스/비교의 필수성으로 문구를 넓혔다. 세 문구는 원래 보류여서 승인 수를 늘리거나 실제 오승인으로 바꾸지 않았지만 문장 수준의 근거 결손으로 남겼다. 인용 축이 다른 계열 값을 하나의 완결률로 합산하지 않는다. [SQLite 인용 점검](streams/sqlite/citation-coverage.json), [curl 명제 점검](streams/curl/citation-coverage.json).

Q가 한 문장이라는 이유만으로 좋은 질문이 되는 것도 아니다. P04의 원 서버 재접속 가능성은 새 pg_dump 가능성을 가르지만, 기존 pg_dumpall 파일의 시점·데이터를 새 덤프로 대체해도 되는지는 묻지 않는다. I/C/Q 모두 같은 후보를 유지했기 때문에 이 결함을 사후 후보 추가로 덮지 않았다. C의 이1건은 근거 부족 승인이다. 실제 실행의 필수조건 충돌과 피해를 확인한 기술적 오승인으로는 확정하지 않았다. {source('P-S04')}; {source('P-D05')}; {source('P-D06')}.

## Q4 · 작성자가 실제로 알려준 것의 시간과 주체

후속137행은 공개 발화114개, 개정4개, 검열 요약11개, 원 사례와 연결되지 않은 인접 기록8개다. 이를 작성자 메시지137개로 세지 않았다. 주창은 최초 요청부터30일이며90일 구현은 별도 열이다. 공개 동일 발신자와 Message-ID/답장 연결·내용을 계보 근거로 쓰고 실명 신원을 증명했다고 하지 않는다. [후속 정본](followups.csv), [창 경계 점검](evidence/window-audit.json).

P03은 초기 예제의 상수 UNION과 실제 비공개 ID 질의를 구별해야 한다. 다른 목록에 재게시한 작성자가 작은 쪽을 local이라고 말했지만 같은 예제를 반복했으므로, 이 말이 실제 테이블의 foreign-server 소속을 특정하는지는 불명이다. 엄격 판정에서는 실제 원천이 T0/T1 모두 미확인이고 예제의 로컬 실행은 이미 T0 사실이다. local을 실제 원천까지 가리킨다고 넓게 읽는 경우에만 후보B가 부적합으로 바뀌는1건을 둔다. 이 해석 이견은 원판만 먼저 읽는 표적 재검토로 점검했지만, 재검토자는 이 사례가 중요한 이유를 알았으므로 완전 맹검이 아니다. {source('P-S03')}; [작성자 local 발화](https://www.postgresql.org/message-id/DB9PR07MB718015C40BC021957A7165F5CB4C9%40DB9PR07MB7180.eurprd07.prod.outlook.com) 본문 local 및 상수 UNION; [검토 이견](streams/curl/p03-cross-review.json).

S04의 작성자는 committed라고 주장했지만 성공 반환을 보여주지 않았고, 같은 후속의 재현에는 BEGIN 뒤 COMMIT이 없으며 로그에 commit 실패가 있었다. FMDB 원앱과 직접 C API 재현이 같은 실행인지도 확정되지 않는다. 이 상충은 작성자의 진술을 거짓이라고 판정할 근거가 아니라, 봉인 Q의 “성공 COMMIT”을 채우지 못했다는 이유다. C05의 기존 move/rename은 basename 보존을 반드시 요구하는지의 부분 단서일 뿐 완전한 답이 아니다. [S04 주장](https://sqlite.org/forum/artifact/2070eae6fd0fa53a44a8ac87b946dd31facab9d181d29f4a304c74c5846246a4) W L1–2, [S04 재현 편집](https://sqlite.org/forum/artifact/8a24d27a64786c26fcee69222d94ce3e0d88c58126bec7aedcd22bff513139d6) W L7–23·28–35; [C05 작성자](https://curl.se/mail/archive-2022-01/0037.html) empty temp directory/move·rename 문단.

늦게 나온 말은 새 요구가 실제로 태어난 시점을 증명하지 않는다. P01의 data-entry, P07의 Oracle 전체 호환, P08의 순서·pop, S07의 UPDATE/DELETE는 그때 처음 공개된 범위일 수 있지만 원래도 필요했는지는 모른다. C06의 후속 --json 개발은 설계 선택이 새로 정해진 기록이며 숨은 T0 필수조건의 발견으로 소급하지 않는다. **지연과 함께 요구의 발생 자체가 확인된 사례는 미확인**으로 남겼다. [24건 소급 민감도](retrofit.csv).

## Q5 · 기술 조건의 변화와 사용자 행동의 변화

판정294행은 같은 후보·판·조건에 대한 T0/T1을 맞췄고, 공식 문서/테스트와 작성자 행동이라는 두 판정원을 나눴다. 엄격한 새Q사실에 의한 후보 변화는0/24, 그런 변화와 작성자 진전 보고가 동반된 것도0/24다. 수락/감사나 문서판 하나로 기술과 사용을 동시에 채점하지 않았다. 확인된 기술 오승인0은 모든 제안이 옳다는 뜻이 아니다. P04 C의 근거부족1, 다수 보류와 원판 재독 오류를 함께 공개했다. [조건 대조](judgments.csv), [사례별 집계](analysis.csv).

실제 진전은 서로 다른 세 사건이다. S01은 CREATE 플래그의 켜기/끄기 대조와 자기 테스트 앱 해결을 작성자가 보고했다. 그러나 사전 답 문구에 노출된 사례여서 미노출23에서는 외부 사용자의 새 실행 성공이0건이다. C05는 기존 workflow에 맞는다는 결정 수용이며 새로운 실행 로그가 없다. C06는 공급자가 PR과 새 commit을 만들었고 테스트를 붙인 개발이다. 외부 사용자 채택이나 같은 T0 제안판의 실행으로 바꾸지 않았다. [S01 자가 실행](https://sqlite.org/forum/artifact/76963f0026b6b12a2ccec60eff052ad870a1fe4e597334cf19d287ffcc2f18cb) W L3·16–18·35–59; [C05 수용](https://curl.se/mail/archive-2022-01/0037.html); {source('C-IM01')}.

반례는 실제 실패와 문서의 적용 경계 양쪽에서 찾았다. S04/S08에는 다른 실제 개입 뒤 실패 보고2건이 있지만 미전송 I/C가 실패했다고 쓰지 않는다. S05는 serialized mode여도 step으로 얻은 row를 다른 reset이 무효화할 수 있어 API mutex와 논리적 다중호출 순서가 다르다. 이 순서는 제공자 계약에서 만든 연구자의 정적 반례이고 작성자의 실행 trace가 아니다. S07의 PostgreSQL 일반 VACUUM에 대한 단정은 끝부분의 빈 page 반환 가능 예외를 놓쳤고, S08 실제 답변의 작은따옴표 열 이름 불가 주장은 당시 parser 허용과 충돌한다. 실제 답변의 명제 충돌2건을 봉인 응답의 오승인0과 섞지 않았다. {source('S-D01')}; {source('S-D11')}; {source('S-TD01')}.

소급표는24건 모두를 남긴다.14건은 실제 후발 요구 관측이 없어 해당 없음이며, 나머지10건에는 늦은 선호·새 증상·다른 연산·스키마 변경·제3자 제안·미연결 새 root가 섞여 있다. 예를 들어 S08의 뒤늦게 줄인 두 열 스키마로 T0의 여섯 NOT NULL을 지우면 C의 누락을 놓친다. P03의 뒤 DELETE 성능을 원래 SELECT 성과로 붙이는 것도 잘못이다. 요구의 발생 시점을 모르면 T0 필수조건의 주 판정에는 넣지 않는다. [소급표](retrofit.csv), [SQLite 보조 반사실](streams/sqlite/counterfactual-audit.csv).

## Q6 · 질문 비용이 더 커지는 조건

실제 추가 사실 요청→작성자 답은 주 대화7쌍이다. S01 세 쌍, S04 세 쌍, C07의 대상 사용자/목적 한 쌍이며, 기술 입력 질문만 세면6쌍이다. 별도 구현 열의 C06 한 쌍을 합치면 중복 없는8쌍이다. C06 쌍도 최초 요청 후30일 안이므로 “90일 구현 열”을31–90일에 새로 나타난 비용으로 오독하면 안 된다. PostgreSQL의 일반 답장9쌍을 다시 읽어 정보 요청이 아닌 설명에 대한 응답을 추가 질문 왕복에서 제외했다. [실제 쌍](evidence/actual-roundtrips.json), [PG 재판독](streams/postgres/clarification-cost-audit.json).

주 대화 쌍별 대기는0.076522–16.222305시간이다. 겹치는 S04 구간이 있어 이를 더한 값을 전체 달력 지연이나 절약 가능한 시간으로 쓰지 않았다. 최초 답까지 시간, 질문 뒤 답까지 시간, 전체 스레드 기간도 구별했다. 가상 I/C는 문구를 발송하기 위해 추가 왕복0, Q는 답이 온다면 최소1이라는 문구 구조만 알 수 있다. 어느 전략이 실제로 더 빨랐는지는 이 자료에서 미확인이다.

링크의 대리 비용도 제한적이다. 봉인 I24개에는 링크23개, C24개에는35개, Q에는0개다. 이는 문구 속 링크 수이지 사용자가 클릭한 수가 아니다. 직접 연 고유 원문61저작은 연구 작업의 출처 수이며 모든 HTTP 재시도나 독자의 읽기 시간을 뜻하지 않는다. 원문/후속 페이지를 다시 여는 비용이 존재해도 그 대리량을 질문의 금전 효과로 바꾸지 않았다. [전략행](strategy.csv), [출처 집계](evidence/source-counts.json).

C05는 비용 주장의 중요한 한계다. 실제 첫 답은 header가 없으면 URL 이름을 쓰는 조건부 설명이었고, 추가 질문 없이 작성자가 수용했다. 그러나 첫 답에 기술 문서 링크는 없었다. 공급자의 문서 정정과 링크는 수용 뒤에 나왔다. 따라서 이 사건은 “질문 없이 설명이 충분할 수 있음”의 사례이며, “조건부 링크 하나만으로 새 구현 성공”의 관측은 아니다. 후자는24건에서 확인하지 못했다. [첫 답](https://curl.se/mail/archive-2022-01/0033.html), [수용](https://curl.se/mail/archive-2022-01/0037.html), [나중 문서 링크](https://curl.se/mail/archive-2022-01/0038.html).

더 물어도 이미 정해진 사용이 바뀌지 않는 S01의 permissions/버퍼 등 실제 확인이나, S03의 안전한 view 순서 경로는 질문 비용의 반대 사례다. 하지만 후보가 같다는 이유만으로 질문의 전체 가치가0은 아니다. 도서관 Mexico 사례는 자료형식 후보를 좁히지 못했어도 검색 숙련도 정보를 얻었다. 소프트웨어에서도 설명 수준·검증 방법·다음 행동이 달라질 수 있다. 다만 이 표본에서는 그 편익을 채택효과로 측정하지 않았다. {source('X-L2')}.

## Q7 · 도서관 상담과 설문 인지면접의 전이 경계

도서관의 RUSA2023 지침은 이용자의 말을 듣고 재진술해 확인하며, 열린 질문과 닫힌 질문을 조합하고, 이전 검색·기한·결과의 적절성을 확인하도록 한다. 이는 모든 질문 앞에서 주변 목적을 전부 수집하라는 규칙은 아니다. 실제 공개 사례로 읽은 Pellegrino2004는 NCSU 채팅70건 중56건을 분석한 연구이며 본문에 익명 대화 발췌가 있다. 2023 지침을2004 상담자가 따랐다는 효과 시험으로 연결하지 않았다. {source('X-L1')}; {source('X-L2')}.

그 발췌에서 기한 필드의 의미는 즉답이 가능했고, Ingenta 질문은 일반 검색법처럼 시작했지만 특정 논문 접근 목적을 확인하며 좁혀졌다. 이는 원래 있던 목적을 명확히 한 사례다. Mexico에서는 자료형식 질문이 형식별 후보를 좁히지 못했지만 이용자의 검색 이해를 알아냈다. Long Island 상담의 약50분·연결 끊김·스트레스는 전체 상담의 관측이며 한 질문 때문에50분을 잃었다는 인과값이 아니다. 감사 표시 뒤에도 다음 행동이 미해결인 예는 “고맙다=해결” 코딩을 반박한다. 이 전이는 질문자의 접근·이해와 답변자의 설명 조절에 적용되며 도구 공급자의 버전 보증을 대신하지 않는다. {source('X-L2')}.

Census의 인지면접 지침·훈련 자료와 실제 프로토콜/관측 보고서는 응답자가 문장을 어떻게 해석하고 기간·기억·판단을 구성했는지 탐색한다. RSM2025-03은2025년3월7일 발행, 내부 최종보고서 표지는2024년10월이며 관측은2023–2024다. 2차 모집기간4월8일–5월11일과 실제 면접기간4월15일–5월14일을 구별했다. 보고서와 부록을 여러 독립 원문으로 세지 않았다. 날짜 불명 현재A2 지침을 최소수에서 빼도 두 분야4저작이 남는다. {source('X-S1')}; {source('X-S2')}; {source('X-S3')}.

관측 보고서 §3.3.2, 인쇄3-18쪽에서는 구직기간 답이 의미를 이해한 뒤1개월에서2개월로 바뀌었다. 반대로 §3.2.4,3-5쪽의 회상 probe 자체가 여러 기간을 혼동시켜2차에서 문구를 바꿨다. 그때 기준기간이 면접에 더 가까워지는 변화도 있어 하나의 문구 변경만으로 차이를 설명할 수 없다. P636은 가정형 취업 가능성을 실제 제안의 부재로 읽어 후속 분기가 어긋났다. 이것들은 해석·계산·회상·주의가 질문으로 바뀔 수 있음을 보여주며, 소프트웨어 요구가 새로 생겼다는 증거는 아니다. {source('X-S2')}.

두 영역에서 **질문이 이용자의 목적 자체를 새로 만들었다는 직접 관측은 미확인**이다. 설계자에게 넘기는 별도 제안은, 질문 문구가 새 목적·금지·선호를 먼저 제시하고 작성자가 이를 채택했다면 그 시점의 공동 설계/후발 요구로 기록하라는 것이다. 이를 원래 숨겨져 있던 T0 필수조건 발견으로 넣지 않는다. 이 규칙을 뒷받침할 최소 후속 자료는 질문 전후 목적 표현과 채택시점이 모두 공개된 전체 대화다. 만족도·응답률·인지면접 응답 수정률을 소프트웨어 채택효과로 환산하지 않았다. [타 분야 반증 기록](streams/cross/notes.md), [날짜·절 교정](streams/cross/corrections.json).

## Q8 · 설계자에게 넘길 입력 규칙과 적용 조건

다음은 관측에서 도출한 **연구자 설계 제안**이다. 질문 수를 일률로 늘리거나 줄이는 정책 효과가 검증됐다는 뜻은 아니다.

| 입력에서 확인한 상태 | 가능한 반환 | 적용 경계·사례 |
| --- | --- | --- |
| 원문 전체로 주체·입력·대상 판과 작은 동작이 정해짐 | 그 동작의 즉답과 직접 근거 링크 | C03 지표 설명, P01 조회 방향. 실제 실행 성공은 별도. 이미 있는 사실은 다시 묻지 않음 |
| 하나의 변수에 따라 각 가지의 주장과 근거가 완결되고 사용자가 자기 조건을 알 수 있음 | 한 갈림 조건과 양쪽 사용/보류·필요한 링크 | C04 바이트 보존 두 절. S05 API mode는 한 문서로 설명 가능하지만 전체 작업안전성은 보류 |
| 원문에 없고, 답에 따라 후보의 적합성 또는 다음 행동이 달라지며, 작성자가 확인 가능한 한 변수 | 한 문장 질문. 답 뒤에도 남는 필수조건을 표시 | P03 실제 원천·S04 성공 COMMIT은 판정에 중요하나 공개 후속은 모호/상충. 한 질문이 충분하다고 보장하지 않음 |
| 후보가 없거나 둘 이상의 필수조건이 남음, 원판·동일성이 불명 | 보류 이유와 다음에 필요한 최소 자료 | C08 원 요청 보존; P02 실제 SELECT·P06 재현. P04는 잘못 고른 변수부터 교정 |
| 나중에 처음 나온 목적·선호·금지 | 해당 시점의 별도 요구와 T0 소급 민감도 | P08 순서/pop, C06 이후 설계선택. 발생시점 미확인이면 기존 사실로 확정하지 않음 |

질문자 관점에서는 원하는 결과와 다음 행동을 바꾸는지를 본다. 답변자 관점에서는 원판이 말한 사실과 기술 검증에 필요한 조건을 구분한다. 공급자 관점에서는 정확히 어떤 공개판이 무엇을 보증하는지 확인한다. 공급자의 새 기능 개발이나 문서 정정을 질문자의 기존 버전 사용 성공으로 바꾸지 않는 이유도 이 세 관점의 차이다. [실제 문구와 한계](examples.md), [조건·행동 행렬](report-case-matrix.json).

전체24, 원판확정24, 미노출23, 직접답0, 비공급자22, 추가 원판보강18의 여섯 분모를 보존했다. 원판 미확인 사례는 아카이브 식별 기준상0이므로 전부 성립/불성립으로 놓은 양끝이 같다. 이것을 PG raw 수신시각 불확실성까지0이라는 의미로 읽으면 안 된다. 직접답만의 비율은 해당 없음이다. 공급자2건을 빼면 넓은 진전은2건이지만 이 역시 사용자 채택2회라는 뜻이 아니다. [분모별 전략](strategy-summary.csv).

표본24는 공개 발신자 표기19개이고 동일인이 다른 문제를 묻거나 다른 목록에 재게시했다. P07/P08은 Oracle 이동 맥락이 유사하지만 같은 사업/실행이라고 확정하지 않았고, C01/C08도 같은 작성자의 브라우저 맥락만으로 성공 계보를 만들지 않았다. 독립 사건은 서로 다른 최초 요청24건이라는 기록 단위이며 독립 사람24명·독립 채택24회가 아니다. 단일월·세 프로젝트·한 작성자의 T0/T1 판독이라는 제한 아래에서 정책의 인과효과·시간 절감은 미확인이다.

## 추가 분석과 재현 경로

원문 최소수는61저작=24대화+당시 제공자 문서/테스트32+타 분야5다. 재독·미러·댓글·개정·재게시·같은 파일의 여러 판은 새 저작으로 세지 않았다. 날짜 불명 X-S1을 빼면60이다. sources159행의 각 ID에는 직접 읽은 위치·확인 UTC·판·생산자·계보·한계를 붙였고, 차단·탐색/초록·내부 입력은 최소수 밖에 뒀다. 구현 소스 C-D09/C-D13과 설계 주석 S-D07/S-D08 및 T0 후 C-IM01도 보수적 최소수에서는 제외했지만 기술·행동 대조 근거로 유지했다. [출처](sources.json), [산입 검산](evidence/source-counts.json).

수치 재현은 이 디렉터리의 `assemble_results.py` → `summarize.py` → `verify.py --require-report` 순서다. 원판과 봉인 문구를 다시 만드는 T0 수집기를 이 순서에 넣지 않는다. 외부 사이트 재접근 없이 커밋된 판독 기록으로 분모·해시·참조·쌍판정·표 형식을 검산할 수 있다. 이 검사가 원문 판독의 정확성이나 인과 효과를 자동 증명하는 것은 아니다. 역사판 SQLite/PostgreSQL/curl 테스트는 원문을 직접 읽었지만 이 실행에서 빌드·실행하지 않았다. 필요한 후속 실행의 고정 입력·명령은 인계에 분리한다.

```bash
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-026/assemble_results.py
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-026/summarize.py
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-026/verify.py --require-report
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-026/manifest-cli.json --fetch
```

고정 입력021/022, 계획 기준과 실제 통합 SHA, 환경·모델 표기, 조사 창은 [SCOPE](SCOPE.md)에 있다. 각 묶음의 커밋과 원격 확인은 [PROGRESS](PROGRESS.md)·[commit 기록](evidence/bundle-commits.json), 기계 검산은 [verification](evidence/verification.json), Q별 자기 점검은 [SELF_CHECK](SELF_CHECK.md), 조건별 수용 상태는 [acceptance evidence](evidence/acceptance-evidence.json)를 본다. 이 보고서의 커밋 뒤 수행한 검사/인계는 그때의 SHA와 시간을 따로 기록하며, 후속 문서 커밋을 이전 실행에 포함됐다고 쓰지 않는다.

## 남은 불일치·약점 — 영향순 세 건

'''


def weaknesses():
    return table(['중요한 불일치·약점','근거 ID·URL','영향을 받는 결정','다음 조사 질문·찾을 자료·최소 확인'],[
      ['P03 local 지시대상이 모호해 새 정보에 따른 후보변화0/1이 갈림',source('P-S03',False)+'; [작성자 local 발화](https://www.postgresql.org/message-id/DB9PR07MB718015C40BC021957A7165F5CB4C9%40DB9PR07MB7180.eurprd07.prod.outlook.com); [표적 검토](streams/curl/p03-cross-review.json)','Q값 회수·후보 변경의 엄격0을 넓은1로 바꿀 수 있음. 구현 성공은 여전히 별도','실제 ID 질의의 물리 원천은 어느 서버였나? 같은 사건의 공개 SQL FROM 관계·foreign server 정의/EXPLAIN VERBOSE 한 묶음에서 실제 질의임을 확인'],
      ['S01 사전노출과 PG raw 수신원본 부재; 순차 자기 판독',source('S-S01',False)+'; [T0 노출](evidence/T0-review.md); [PG raw 시도](streams/postgres/initial-raw-attempts.json)','전24건 미노출 비교 불가; 유일 외부사용자 새 성공은 미노출집합에서 제외. 원판24를 동급 암호학적 원본으로 부를 수 없음','남은 고정24를 답을 가린 판독자가 어떻게 코딩하는가? T0봉인 SHA만 제공한 독립 재판독1회에서 변수·승인/보류·원판증거 등급 일치를 확인; 원본 부재는 그대로 표기'],
      ['직접답 분모0·단일월/반복발신자·가상전략으로 인과효과와 목적생성을 알 수 없음',source('X-L2',False)+'; '+source('X-S2',False)+'; [여섯 분모](strategy-summary.csv)','질문을 줄이는 일반 정책, 조건부 링크 단독 해결, 시간절감·새 목적 발생을 확정할 수 없음','다음 사전고정 원장에서 같은 변수 질문→작성자의 기존사실 답→동일판 행동이 연결되는가? 응답 결과와 무관하게 정한 다음 월의 공개 전체 대화1계열을 읽고 실제 계보와 요구 발생시점 표현을 확인']
    ])


if __name__ == '__main__':
    result = first_tables() + narrative() + weaknesses()
    (P / 'RESULT.md').write_text(result, encoding='utf-8')
    print(json.dumps({'file':'RESULT.md','case_rows':len(M),'claim_rows':len(CLAIMS),'characters':len(result)},ensure_ascii=False))
