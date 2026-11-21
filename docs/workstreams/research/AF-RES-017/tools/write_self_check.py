"""Write an explicit, non-passing substantive acceptance record.

Artifact integrity is checked separately by validate.py. Missing cases are not
converted to a pass merely because the files are complete and reproducible.
"""
import json
from pathlib import Path

P = Path(__file__).resolve().parents[1]
qrows = json.loads((P / 'evidence/q-evidence.json').read_text())
sources = {s['id']: s for s in json.loads((P / 'sources.json').read_text())['sources']}

conditions = [
    {
        'condition': '사례 40개 이상, 출처 계열 4개 이상, 한 계열 40% 이하, 한 조직 3개 이하다.',
        'met': False,
        'evidence': 'RESULT.md#q2-사례-집합의-수량과-반례; evidence/statistics.json#minimum_dated_episode_ids; SAMPLING.md#실행-뒤-추가한-관측-기록--사전-계획-변경-아님',
        'note': '40은 관측 원장이다. 공개 날짜 대리값을 허용한 사건18은 a1/c16/e1의 3계열이며 PR16/18(88.9%)이다. 40관측의 a16/b3/c16/e5, 최대40%, 조직최대2를 적격18의 다양성으로 옮길 수 없다. 확보한 공개 원문에 최초 결정월·실제 발견월·변경 결과가 없거나 계획만 있는22건은 적격으로 세지 않았다. 기존18의 최초 선택일을 재확인하고 최소 새 적격22개를 추가하되, 완성 집합에서 4계열·계열당40% 이하를 다시 맞춰야 한다. 추가 검색 입력과 필요 자료는 SELF_CHECK.md §3, RESULT.md §4.1에 있다.'
    },
    {
        'condition': '정당한 자체 구현 5개 이상, 되돌림 3개 이상이 포함됐다.',
        'met': False,
        'evidence': 'RESULT.md#q2-사례-집합의-수량과-반례; evidence/counterexamples.json; cases/CASES.json',
        'note': '정당화 기록9개 중8개는 처음부터 알고 거절한 대안이다. 구현 뒤 발견한 B01은 실험용·미테스트이며 결정월과 생산 결과가 없다. 세부 요구인 늦게 알았지만 자체 구현이 옳았던 적격5건은 충족하지 않았다. 실제 외부 채택 후 철회는 PR11/PR15/PM04의3건을 확보했으나 초기 미인지의 인과까지 확인된 것은 아니다. 후기 발견 진술·월별 최초 선택·실제 유지 결과를 모두 갖춘5건을 추가 확보해야 한다.'
    },
    {
        'condition': '모든 사례에 결정 시점 존재 판정과 그 근거 주소가 있다(판정 불가는 이유와 함께).',
        'met': True,
        'evidence': 'cases/CASES.json#existed_at_decision; evidence/validation.json; evidence/EXISTENCE_AND_SEARCH.md',
        'note': '관측40건 모두 yes/no/unknown, 근거 URL, 판정 불가 사유를 보존했다. yes25/no3/unknown12. 실제 최초 결정일 자체가 대리값인 경우가 있으며 당시 유명함과 역사적 검색 가능성을 확인한 것은 아니다.'
    },
    {
        'condition': '모든 사례가 내부 별도 검토로 이중 코딩됐고, coder-a 동결 커밋이 coder-b 원 응답 커밋보다 앞선다.',
        'met': True,
        'evidence': '70fa1b691601a0cc9fb751db518fd4c5cad06bf8 -> d137422f1ff322f28bc09434cf50a7f31e31a591; coding/REVIEW_PROTOCOL.md; coding/coder-b.json; coding/agreement.json; evidence/remote-coding-verification.json',
        'note': '40개 모두 새 문맥 gpt-6.2-sol의 내부 별도 검토를 받았다. A·B 원응답 및 packet hash, 원격 커밋 선후를 검증했다. B는 코드북과 라벨 없는 공통 추출 요약을 읽었으며 원문 재추출 독립 검증이나 사람 검토는 아니다.'
    },
    {
        'condition': '표 1~4가 지정한 열로 채워져 있다.',
        'met': True,
        'evidence': 'RESULT.md#1-필수-결과-표; evidence/validation.json',
        'note': '열 이름·순서와 비어 있는 칸 유무를 검사했다. 표1의40행은 관측이며 미확인과 확인할 추가 자료를 명시했다. 빈칸 대신 미확인을 썼다는 이유로 적격 사건 수를 늘리지 않는다.'
    },
    {
        'condition': 'Q1–Q8 각각에 서로 다른 종류의 출처가 2개 이상 있다.',
        'met': True,
        'evidence': 'SELF_CHECK.md#1-세부-질문별-자기-점검; evidence/q-evidence.json; sources.json',
        'note': '각 질문의 source ID와 source_type을 실제 원장에 대조했다. 종류 수는 Q1=5,Q2=5,Q3=4,Q4=7,Q5=6,Q6=5,Q7=7,Q8=8이다. 같은 사이트 개수나 문서 개수를 종류 수로 바꾸지 않았다.'
    },
    {
        'condition': '다른 분야 4개 이상이 원문으로 대조됐다.',
        'met': True,
        'evidence': 'CROSSFIELD.md#1-q7--다른-분야는-무엇을-실제로-세는가; evidence/methods/counts.json; evidence/methods/sources.json',
        'note': '의학·특허·과학의 다중 발견·사후 판단 심리학을 원문으로 대조했고 운영연구를 추가했다. 원문이 차단된 Lau1992/Fischhoff1975/Katz-Allen은 최소 수에 넣지 않았다.'
    },
    {
        'condition': '반례 다섯 가지 각각을 찾은 기록(질의와 결과)이 있다.',
        'met': True,
        'evidence': 'evidence/counterexamples.json; SEARCH_LOG.json; CROSSFIELD.md',
        'note': '알고 거절·채택 철회·당시 부재·현재 쉬운 검색·이름과 구조의 구분을 각각 검색하고 결과를 남겼다. 다섯째는 M27의 동일 최종 결과 반례와 M28의 다의성까지 확인했으며, 모든 용례가 장식적이라거나 순수 장식의 변경 전후를 확정한 것은 아니다. 실패·미확인도 결과에 포함한다.'
    },
    {
        'condition': 'RESULT.md §4에 불일치·약점 3건과 다음 조사 제안이 있다.',
        'met': True,
        'evidence': 'RESULT.md#4-가장-중요한-불일치약점-3건과-다음-조사-제안; evidence/validation.json',
        'note': '정확히3건: 적격 수와 분모, 비용·발견 가능성의 사후 귀속, 분류 경계·타 분야0의 해석. 각각 근거 위치·바뀔 결론·질문·필요 자료·최소 규모를 명시했다.'
    },
    {
        'condition': 'SELF_CHECK.md 점검을 통과한 뒤에만 HANDOFF.md를 쓴다.',
        'met': False,
        'evidence': 'SELF_CHECK.md#2-끝내도-되는-조건; evidence/acceptance-evidence.json; evidence/validation.json',
        'note': '이 점검을 먼저 작성·커밋한 뒤에만 HANDOFF를 작성한다. 형식·참조·산술 검증은 통과했으나 첫 두 실질 조건이 미충족이므로 전체 점검 통과라고 하지 않는다. 요청에 명시된 자료 부재 예외에 따라 REVIEW_READY_WITH_GAPS로 인계한다. 필요한 공개 기록이 현재 확보 자료에 없다는 뜻이며 세상에 없음을 입증한 것이 아니다. 완전 수락은 §3의 보강 후 다시 점검해야 한다.'
    },
]

(P / 'evidence/acceptance-evidence.json').write_text(json.dumps(conditions, ensure_ascii=False, indent=2) + '\n')

def cell(x):
    return str(x).replace('|', '\\|').replace('\n', ' ')

lines = [
    '# AF-RES-017 — 자기 점검',
    '',
    '**전체 수락: 미통과.** 40개 관측과 27개 산입 방법·비교 저작, 이중 코딩 및 지정 보고서는 확보했지만 적격40개와 후기 발견 뒤 정당한 자체 구현5개를 충족하지 못했다. 형식·참조·산술 검증의 통과와 연구 수락의 통과를 분리한다. 이 파일과 acceptance-evidence를 먼저 커밋한 뒤 자료 부재 예외에 따른 인계를 작성한다.',
    '',
    '## §1 세부 질문별 자기 점검',
    '',
    '출처 ID는 sources.json에 해소되며, 종류 수는 해당 원장의 source_type 고유값이다. 판단자는 작업자이고 B의 코딩만 새 문맥의 내부 별도 검토다. 아래 반증 기록은 전부 실행한 질의·자료이며 향후 계획과 분리했다.',
    '',
    '| 세부 질문 | 답 한 줄 | 붙은 출처 ID(종류 수) | 반증 시도(쓴 질의·자료와 결과) | 남은 불확실성 |',
    '| --- | --- | --- | --- | --- |',
]
for row in qrows:
    types = {sources[s]['source_type'] for s in row['source_ids']}
    assert len(types) >= 2 and row['disconfirmation']
    lines.append('| ' + ' | '.join(map(cell, [row['question'], row['answer'], ', '.join(row['source_ids']) + f' ({len(types)}종류)', row['disconfirmation'], row['uncertainty']])) + ' |')

lines += [
    '',
    '## §2 끝내도 되는 조건',
    '',
    '| 조건(요청 원문) | 충족 여부 | 근거 위치 | 판정 범위·미충족 이유 |',
    '| --- | --- | --- | --- |',
]
for item in conditions:
    lines.append('| ' + ' | '.join(map(cell, [item['condition'], '예' if item['met'] else '아니오', item['evidence'], item['note']])) + ' |')

lines += [
    '',
    '### 추가 수량·절차 점검',
    '',
    '| 점검 | 결과 | 근거 |',
    '| --- | --- | --- |',
    '| 본문을 직접 읽은 실제 자료 최소20 | 예. 방법·비교 저작만28개 원문, 그중27개 산입. 사례와 방법 문헌을 중복 산입하지 않음 | evidence/methods/counts.json; sources.json |',
    '| 방법·비교 문헌25, 동일 사이트 최대3 | 예.27저작/24사이트; 최대3. 소프트웨어 실증5/의학3/특허3/다중발견2/사후편향2 | evidence/methods/counts.json |',
    '| 원리 도입의 일차 경로5 | 예. 구조 대응이 있는7경로. 최초 발명자·역사상 최초라는 주장은 별도 | CROSSFIELD.md; M06/M07/M17/M20/M21/M22/M23 |',
    '| 비용 공백을0으로 채우지 않음 | 예. 수치가 있는 관련 변경·사고 지표31/40, 비용 미확인9/40. B16의 변경 규모는 비용에서 제외 | evidence/statistics.json; RESULT.md Q5 |',
    '| 실제 필요 문장과 짧은 공식 설명 | 예.40개 모두25단어 이하. 필요 문장은 회고 자료에서 작업자가 만든 요약이며 동시기 질의 원문으로 부르지 않음 | cases/INPUTS.json; cases/CASES.json; evidence/lexical-protocol.json |',
    '| 라벨 집중과 변별력 | A/B의 주요 코딩 축은 단일 값80% 미만. 당시 인기 unknown40/40은 별도 경계 진단 D04/D07/D08로 점검. 부정7·긍정3 합성 진단10/10은 실제 사례 분모 밖 | coding/agreement.json; coding/REVIEW_PROTOCOL.md |',
    '| 모든 필요 호스트를 첫 커밋 전에 익명 점검 | 아니오. 계획한11호스트는 먼저 점검했으나 수집 중 새로 만난 호스트는 실제 이후 시각에 한 번씩 점검. 사전 절차를 소급한 것으로 기록하지 않음 | PROGRESS.md; evidence/network-followup.json; evidence/methods/NETWORK.json |',
    '| 차단·초록·검색 snippet을 본문 근거로 세지 않음 | 예. 제외96개를 별도로 유지. 통합243기록에는 D1 156/D2 44/D3-fetch 43과 고정 선행 입력이 포함되므로243개 모두를 외부 본문이라고 부르지 않음 | sources.json; evidence/validation.json |',
    '| 소유 경로와 원응답 보존 | 예. 기준 SHA 이후 커밋 경로는 모두 owned_path. SCOPE와 A hash, B 원응답 보존. dot-control 수정 없음 | evidence/validation.json; git diff --name-only source_commit HEAD |',
    '',
    '## §3 보강할 수 없었던 행과 최소 재개 입력',
    '',
    '자료 부재는 **이번에 확보한 공개 기록에 요구된 문장·월·실제 변경이 없음**을 뜻한다. 모든 공개 자료가 소진됐거나 앞으로도 확인 불가능하다는 뜻이 아니다. 원문이 공개하지 않은 사적 최초 선택일, 인지 상태, 노동시간을 현재 작성자가 만들어 채울 수 없다. 일반 이행 글·현재 인기도·문서상 계획을 대신 넣어 수량을 맞추지 않았다.',
    '',
    '| 보강 대상 | 이미 확인한 장애 | 답을 바꿀 최소 추가 자료 | 재개 입력 |',
    '| --- | --- | --- | --- |',
    '| Q1·Q2: 적격40·계열 균형 | 22관측에서 최초월·실제 인지월·변경 결과 일부가 없음. AD01은 미구현안, AD02는 알고 거절한 대안 | 기존18의 원 결정 확인 + 최소 새 적격22; 완성 집합에서 계열4·계열당40% 이하 | 먼저 evidence/statistics.json의 minimum_dated_episode_ids와 CASES 날짜 필드를 대조. 공개 검색: `"after implementing" "discovered" "library"`; `"did not know" "replaced" "custom"`; `"ADR" "superseded" "migration"` |',
    '| Q2: 후기 발견 뒤 자체 구현5 | B01은 후기 발견을 밝히지만 미테스트 실험이고 결정월 미상. 알고 거절8건은 요구와 다름 | 당사자의 후기 발견 진술·양쪽 월·실제 유지 결과가 연결된5건 | 공개 검색: `"after writing" "found" "still" "library"`; `"reinvented" "existing" "requirements"`; B01의 공개 저장소 도입 커밋과 이후 검증 기록 탐색 |',
    '| Q4·Q5: 발견 가능성과 회피 비용 | 회고 need와 현행 문서·색인을 썼으며 노동시간/금액 직접 기록 없음 | 결정 전 need20개와 당시 버전 후보; 직접 시간·일정 근거10개 | cases/INPUTS.json을 누설 검토하고 동일 입력·동일20분 제한의 기존 검색/제품 조건 비교. 운영 중인 제품은 이번에 구현·실행하지 않았음 |',
    '| Q3·Q8: 관계 경계와 다른 분야0 | shared extraction과 제한된 표집. M27은 이름/적합성 재인식의 직접 반례지만 모든 용례의 장식성 증거는 아님 | 불일치11개+명시적 구조 도입5+동일 구조2의 독립18검증 세트 | coding/agreement.json의 disagreements와 CROSSFIELD의 원리·전제·대응을 입력으로 새 세트 작성. 현재 B 원응답은 수정하지 않음 |',
    '| 지정 원저 일부 | Lau1992 NEJM403, Fischhoff1975 원문 미확보, Katz/Allen MIT429·CORE403. 최소 수는 대체 원문으로 충족 | 정상적으로 열린 원저 본문 한 부와 발행판 확인 | evidence/methods/sources.json의 excluded URL과 실패 상태를 그대로 사용하여 정상 공개 열람이 가능한 다음 세션에서 확인. 차단된 경로를 프록시 변경 등으로 우회하지 않음 |',
    '',
    '다음 작업이 자료를 추가하면 사례 판정과 분모를 다시 고정하고 새 A 동결 커밋 후 그 추가/변경 사례의 B 검토를 새 문맥에서 실행해야 한다. 현재40개의 원응답을 결과에 맞춰 재작성하지 않는다.',
    '',
    '## §4 재현과 검증 명령',
    '',
    '저장소 루트에서 실행한다. 아래 검증은 기존 산출물의 일관성만 검사하며 미확인 연구값을 만들어 내지 않는다.',
    '',
    '```bash',
    'python docs/workstreams/research/AF-RES-017/tools/validate.py --no-write',
    'git merge-base --is-ancestor 70fa1b691601a0cc9fb751db518fd4c5cad06bf8 d137422f1ff322f28bc09434cf50a7f31e31a591',
    'git diff --name-only 0209117d8ec00af39bd25844d52a18edc7323207 HEAD',
    '```',
    '',
    '필요시 `tools/analyze.py`, `tools/agreement.py`, `tools/write_result.py`, `tools/write_self_check.py` 순서로 재생성할 수 있다. `tools/freeze.py`와 `tools/check_hosts.py`는 동결·한 번의 접속 관측을 다시 쓰는 도구이므로 재실행하지 않는다. 마지막 인계 커밋 뒤에는 `validate.py --no-write --check-handoff`로 파일을 바꾸지 않고 확인한다.',
    '',
    '## 한계',
    '',
    '모든 비율은 목적표집의40관측 또는 명시한 하위 집합과 탐색 창1990-01-01~2026-11-21에 한정한다. 월별 대리 사건18의 실제 연도는2006~2025이며 현재 검색 관측일은2026-11-21이다. 자료 수·코딩 일치율·파일 검증이 대표성, 인과성, 역사적 발견 가능성 또는 제품 효과를 보장하지 않는다. 이 한계 때문에 최종 상태는 REVIEW_READY가 아닌 REVIEW_READY_WITH_GAPS다.',
    '',
]
(P / 'SELF_CHECK.md').write_text('\n'.join(lines))
print(json.dumps({'conditions': len(conditions), 'met': sum(c['met'] for c in conditions), 'not_met': sum(not c['met'] for c in conditions), 'questions': len(qrows)}, ensure_ascii=False))
