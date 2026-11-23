"""Render the audit report from preserved ledgers; no retrieval or scoring."""
from pathlib import Path
import csv
import json
from collections import Counter

P = Path(__file__).resolve().parent.parent


def jsonl(name):
    return [json.loads(line) for line in (P / name).read_text().splitlines() if line.strip()]


def cell(value):
    return str(value).replace("|", "&#124;").replace("\n", " ")


def table(headers, rows):
    return "\n".join(["| " + " | ".join(map(cell, headers)) + " |", "| " + " | ".join("---" for _ in headers) + " |"] + ["| " + " | ".join(map(cell, row)) + " |" for row in rows]) + "\n"


proposals = jsonl("proposals.jsonl")
sources = jsonl("sources.jsonl")
src = {r["source_id"]: r for r in sources}
judgments = list(csv.DictReader((P / "judgments.csv").open()))
counts = json.loads((P / "evidence/normalized-counts.json").read_text())
original_sources = [s for s in sources if s["phase"] == "original_experiment"]
work_count = counts["independent_original_works"]
source_count = len(sources)

origin_notes = {
    "P1": "첫 PR와 입력 Git판 일치. 본문이 언급한 2024년 3월 Google 초안의 당시 판 미확보. 창설판으로 단정 불가.",
    "P2": "이 주소는 첫 main판. 사후 확보한 6ddd0d85(2024-06-05) PR 초안이 앞섬. C1/C2는 동일하나 대안·참조가 다름. 전체 PR-first 모집순위 미확정.",
    "P3": "이 주소는 첫 main판. 사후 확보한 0f451026(2023-03-08)에는 불변 문서·버전쌍 일대일 C2가 없음. 3월14일 추가됨. 입력은 창설판 비교를 충족하지 못함.",
}
first_rows = []
for p in proposals:
    alternatives = "; ".join(p["choices_before_search"]) + ". 이미 알려진 참조: " + ", ".join(p["known_names"])
    if p["id"] == "P2":
        alternatives = "원문 모델 대안: BDFL, meritocracy/do-ocracy, self-appointing council, electoral, foundation-backed, liberal/C4. 연구자가 검색 전 비교용으로 구체화한 선택: " + "; ".join(p["choices_before_search"]) + ". 원문 참조: OSSWatch, CommunityRule, The Open Source Way."
    first_rows.append([p["id"] + " · " + p["proposal_id"], f'{p["raw_rank"]} / [실제 검색 입력 blob]({p["first_blob_url"]})', p["part"] + "; " + p["purpose"], "C1: " + p["conditions"]["C1"] + " C2: " + p["conditions"]["C2"], alternatives, origin_notes[p["id"]]])

second_rows = []
for j in judgments:
    source = src.get(j["source_id"], {})
    location = j["read_sections"] or "원문 절 미확인"
    address = j["landed_url"] or j["original_url"]
    provenance = f'[{j["source_id"] or "반환 URL·미열람"}]({address}) / {location}'
    role = j["candidate_role"] or "미판정"
    if j["direct_original_read"].lower() != "true":
        role += " · 원저작 판독 근거 없음/별도 상태"
    mapping = j["donor_to_recipient_choice"] or "원문 근거로 대응시키지 않음"
    novelty = (j["novelty_assessment"] or "미확인") + "; " + j["read_status"]
    if j["remaining_unknowns"]:
        novelty += "; " + j["remaining_unknowns"]
    falsifier = j["minimal_falsifier"] or "미열람/미확인: 입력을 검증한 것으로 세지 않음"
    if j["control_input"]:
        falsifier += " / 대조: " + j["control_input"]
    readcost = j["reading_cumulative_cost"] or "미열람(산출 안 함)"
    costs = f'검색반환 {j["search_cumulative_cost"]}; 해당 판독 {readcost}; 보기총 {j["arm_total_cost"]}; 공통상한 {j["common_prefix"]}'
    condition = "C1=" + j["C1"] + "; C2=" + j["C2"] + "; 목표 적용 미실행"
    if "contradict" in j["C1"] + j["C2"]:
        condition += "; contradict는 공여 규칙을 그대로 복사할 때의 조건 충돌, 목표 시스템 실행 반증이 아님"
    second_rows.append([j["rank_id"], j["actual_query"], role + "; " + provenance, mapping, condition, falsifier, novelty, costs])

third_rows = [
    ["P1 · JEP122", "7", "A만 0 / B만 0 / C만 0 / 공통 0", "저장소 접근권 이전·수신 주체의 책임 수락·우산조직 범위를 다른 상태로 적고, 제외 저장소가 분쟁 당사자인 최소 입력으로 C2를 확인한다.", "[2024-06-27 승인 댓글](https://github.com/jupyter/enhancement-proposals/pull/123#issuecomment-2195794991), [governance PR229](https://github.com/jupyter/governance/pull/229); 2021 외부 incubation은 당시 존재, 작성자의 해당 옵션 인지는 미확인", "C1의 표준·프로토콜 부합 증거와 개별 저장소의 실제 권한 경계 미확인. C의 비용8 판독은 같은 비용 표에서 제외."],
    ["P2 · SPEC9", "7", "A만 0 / B만 0 / C만 0 / 공통 0", "공개 결정·요약과 비공개 인선/민감정보 예외를 구분한다. C2를 예외 없는 조건으로 유지할지 제안자의 선택으로 되돌린다.", "[PR323](https://github.com/scientific-python/specs/pull/323); 6월5일 Matplotlib 사례를 이미 전달받음. [최후 확인판](https://github.com/scientific-python/specs/blob/00fa7c15c3ada4a1f3ae80559b628c31ce17658f/spec-0009/index.md)은 draft·endorsement 공란", "SPEC9 실제 채택·운영 성과 미확인. 비용8 Wikimedia 원문은 공통비용에서 제외. 첫 PR 기준 전체 모집 미확정."],
    ["P3 · JEP97", "8", "A만 0 / B만 0 / C만 0 / 공통 0", "구형 reader 읽기, 독립 strict validator, 미래 minor 허용을 분리한 입력을 실행한다. 동일 URI의 바이트 고정·정규 표기·버전쌍 대응을 각각 확인한다.", "[2023-03-16 제안자 댓글](https://github.com/jupyter/enhancement-proposals/pull/97#issuecomment-1471548986), [2023-07-11 표결](https://github.com/jupyter/enhancement-proposals/pull/97#issuecomment-1630425438); strict/permissive 차이는 이미 인지", "제안 승인과 구현 출시는 별개. 실행0, 당시 CI 결과 확보 못함. 최초 PR에는 실험 C2 없음."],
]

text = "# AF-RES-073 결과 — PARTIAL\n\n## 표 1. 모집과 실제 고정 입력\n\n"
text += table(["제안 ID", "원순번·최초 blob 주소", "부분·목적", "C1·C2", "기존 대안", "미확인"], first_rows)
text += "\n## 표 2. 모든 반환 자리와 판독·판정·비용\n\n"
text += table(["제안·보기·원순위", "실제 질의", "후보 역할·도착 원문 주소/절", "공여 동작→수신 선택", "같은 구성의 C1/C2", "뒤집을 입력", "신규성·미확인", "누적 비용"], second_rows)
text += "\n## 표 3. 동일 누적 연산에서의 적격과 다음 행동\n\n"
text += table(["제안", "같은 연산 수", "A만/B만/C만/공통 적격", "다음 설계 행동", "제안자 인지·채택 근거 주소", "미확인"], third_rows)

text += f"""
## 판정과 읽는 방법

이 기록의 상태는 **PARTIAL**이다. 3개 고정 입력에 대한 9개 보기·18질의·90순위 관측과 읽기 비용 기록은 끝냈다. 그러나 엄격한 ‘최초 제안 3건’ 완료 조건은 충족하지 못했다. 모집에서 검증한 첫 main 추가판과, 사후에 확보한 첫 PR 초안이 달랐다. P3에서는 C2 자체가 후대에 추가되었다. 사후 발견으로 원질의나 점수를 덮어쓰지 않았다. 기존 관측은 **main-first 고정 입력을 사용한 탐색 기록**으로 남기며, 창설 당시 개발자의 최초 설계 대안 탐색 실험으로 승격하지 않는다.

고정 C1·C2를 같은 구성에서 함께 지지한 조건부 설계 적격은 **관측된 0건**이다. ‘대상 종류를 복원해도 도움이 없다’거나 ‘후보가 어디에도 없다’는 뜻이 아니다. 원문의 한쪽 조건만 지지한 부분 원리, 원래 알려진 기능, 범위가 다른 후보를 구분한 결과다. 미열람과 실패는 0점짜리 반례가 아니다. 목표 시스템 실행·실제 조직 변경은 0회이므로 적용 성공률은 **분모가 없어 산출 불가**다. 최초 적격까지의 비용도 0회가 아니라 **정해진 예산 안에서 관측 없음(null)**이다.

출처 원장은 현재 **{source_count}행**, 보수적 계보 병합 후 직접 읽은 독립 원저작은 **{work_count}개**다. 같은 제안·PR의 댓글과 후속판, 같은 구현의 문서·코드·시험·출시, 번역·미러·재열람은 추가 저작으로 세지 않았다. 접근 실패와 메타데이터만 읽은 행은 최소량에서 제외했다. 원 검색에서 직접 읽은 독립 원저작은 {len(counts['original_direct_read_work_ids'])}계보이며, 원저작 판독이 연결된 순위는 46자리다. 중복 재사용 3자리가 포함되므로 46을 읽기 횟수로 쓰지 않는다. 직접 원저작 읽기 작업은 43회, 전체 문서 작업은 52회다. 원 검색 분자에 사후 자료를 넣은 수는 0이다. 구체 필드와 산입 근거는 [sources.jsonl](sources.jsonl), [정규화 수치](evidence/normalized-counts.json), [검토 기록](review/ledger-review.md)에 남겼다.

모든 시각·확인 기록은 UTC다. 오늘의 순위는 오늘 관측이며 2023~2024년의 순위를 재구성하지 않는다. 검색은 동일 도구 system1, 영어, 기간·도메인 제한 없음, 첫5자리로 고정했다. 두 질의의 검색2회 뒤 Q1R1→Q2R1 순으로 읽었다. 같은 보기의 완전히 같은 URL만 비용 없이 연결했고, 다른 URL이나 다른 보기의 재등장은 새 읽기였다. 원문 열기·실패에 각각1회를 부과했다. [SCOPE.md](SCOPE.md), [queries.jsonl](queries.jsonl), [runs.jsonl](runs.jsonl)이 실제 규칙과 시행을 보존한다.

## Q1. 최초 제안의 선택과 버전 경계

### 모집틀

MEP는 기간 안에 추가된 공통 README 1행만 발견되어 제외했고 번호가 있는 제안은 이미 2017년 트리에 있었다. 공석을 숫자로 채우지 않았다. JEP와 SPEC는 기본 브랜치에서 도달 가능한 제안 파일의 최초 추가를 날짜 내림차순·경로순으로 첫8개씩 보존했다. 따라서 [frame.csv](frame.csv)는 17행이며 그중 MEP 1행은 제외 영수증이다. JEP의 원순위는 122, 118, 97, handshaking, optional-features, schema-subdomain, connectionfile, kernelspec 순이다. SPEC는 9, 7, 8, 6, 5, 4, 3, API Dispatch인2 순이다. 작성시각과 커밋시각을 각각 남겼고 두 시각 정렬로 첫 선택이 바뀌지는 않았다. 다만 이는 main-first 범위의 민감도 점검이며 PR 전체 이력의 검증은 아니다.

JEP122와 SPEC9가 조직 운영 제안이라는 이유로 건너뛰지 않았다. JEP118은 최초 main판에서 새 메시지 대안이 이미 기각되고 정확한 설명 문구만 미정이어서, 다른 관측을 내는 설계 선택을 남긴 첫 문서라는 사전 기준에서 제외했다. MEP 공석은 봉인한 JEP→SPEC 순서에 따라 JEP97로 채웠다. 이 때문에 결과는 두 프로젝트·두 조직 운영 문제와 한 형식 이행 문제에 제한된다. 일반적인 소프트웨어 모듈 검색 효율을 대표하지 않는다. 각 제외·선정의 직접 원문과 이력 명령은 [recruitment/](recruitment/) 아래에 있다.

### 요구와 실제 인용

P1의 고정 입력 [JEP122](https://github.com/jupyter/enhancement-proposals/blob/2b194a3c090fd375321871c47a3de503a0758206/122-jupyter-book-incorporation/jupyter-book-incorporation.md)는 일부 저장소를 편입하고 나머지는 독립 관리를 유지하는 선택이다. Guide-level L43의 **“integrate and interoperate cleanly”**, L45의 **“will not have any responsibility or oversight”**가 두 조건의 핵심이다. FAQ L124–126의 **“Not right now.”**는 같은 웹 기술을 쓴다는 이유만으로 범위 밖 Papyri를 이번 편입에 포함하지 않는 경계다. 표준·프로토콜과의 부합은 선정 기준이며 조직 이동이 기술적 호환성을 완성한다는 말은 아니다. 독립 후원기관과 현상 유지가 이미 명시되어 있었다. source REC-JEP-01, [selection.json](recruitment/jep/selection.json).

P2 [SPEC9 고정판](https://github.com/scientific-python/specs/blob/846579d4b8d5ca90ba6a9792c263574c73b9f48d/spec-0009/index.md)의 선택은 특정 모델 하나를 정답으로 정하는 것이 아니라 변화 가능성과 공개 운영을 어떤 절차로 결합할지다. C1 L138–140은 **“Choose a model that allows for future adjustments as the project evolves”**, C2 L173–175는 **“making all governance-related documentation, meeting minutes, and decisions publicly available”**다. 이 권고를 실험의 고정 조건으로 삼았으므로 모든 배포 현장의 의무라고 확대하지 않는다. 원문의 성장·다양성·피드백 문맥을 ‘권한을 바꾸는 개정과 일반 기여자의 기록 열람’이라는 최소 입력으로 구체화했으며 투표정족수·마감일은 만들어 넣지 않았다. source REC-SPEC-09, [selection.json](recruitment/spec/selection.json).

P3 [JEP97 고정판](https://github.com/jupyter/enhancement-proposals/blob/b9ab810ae0fc50ac7494fdf9d345738e1cf6751d/97-add-schema/add-schema-to-notebook-format.md)은 숫자 버전 필드와 직접 스키마 참조의 과도기를 어떻게 운영할지 남겨 두었다. L595 **“ensure old clients can still work”**, L30 **“refer to an immutable document”**, 미해결 절의 **“Major version update?”**를 근거로 두 조건과 열린 이행 선택을 정했다. 정규 URI와 /../ 별칭의 경계는 원문 예시다. JSON Schema, 임시 숫자 필드 유지, extraSchemas, 기존 탐색 gist는 이미 알려짐이다. diff의 required에는 $schema가 있으나 전체 예시에는 빠진 내부 불일치도 기록했다. source REC-JEP-03, [reserve-selection.json](recruitment/jep/reserve-selection.json).

### 사후 발견이 최초판 주장을 무너뜨린 부분

P1의 첫 PR 커밋은 실제 고정 입력과 같았다. 그러나 본문이 언급한 3월 Google 초안과 5월 초 사전 논의의 당시 문서판은 확보하지 못했다. P2의 [첫 PR blob](https://github.com/scientific-python/specs/blob/6ddd0d85a8acf184e2e7e35899c0d80af639dc94/spec-0009/index.md)은 2024-06-05이며 main 최초 추가 9월10일보다 이르다. C1/C2는 같지만 단일판매자 대안이 아직 있었고 The Open Source Way Notes 인용은 나중에 추가되었다. OSSWatch 템플릿은 첫 PR부터 존재하므로 모든 OSSWatch 지식이 나중이라는 주장도 기각했다. P3 [첫 PR blob](https://github.com/jupyter/enhancement-proposals/blob/0f4510266ead738e62f1d9e412d6bb9e7eb7a97d/97-add-schema/add-schema-to-notebook-format.md)은 2023-03-08이고 불변성·일대일 C2가 없다. 그것은 [3월14일 판](https://github.com/jupyter/enhancement-proposals/blob/e2651761a98f673d9c1e05d02e33ac4b3668c736/97-add-schema/add-schema-to-notebook-format.md)에 들어왔다. 후기 조건을 초기 요구처럼 쓰는 오류가 실제로 확인되었다. [P1 기원 점검](postseal/P1/origin-correction.json), [P2 정정](postseal/P2/provenance-audit.json), [P3 증거](postseal/P3/evidence.json).

이름 변경에서도 같은 경계를 적용했다. SPEC7의 생존 `nep7-prng` 브랜치 [b2332422](https://github.com/scientific-python/specs/blob/b233242257195a62e118ca3881eb69e86a4fb796/spec-0007/index.md)는 rng=None에 전역 시드를 따르는 반면 나중 main판은 그 동작을 피하도록 바뀌었다. SPEC2의 옛 같은 파일명은 최소 지원 버전 정책이었고, 현 API Dispatch는 삭제 후 새로 추가된 다른 문서다. 파일명이 같다는 이유로 문서의 탄생이나 문구를 앞당기지 않았다. 이 점검으로도 PR-first 전체 순위가 완성된 것은 아니다. 원 frame과 질의를 바꾸면 사전 봉인이 사라지므로 정정은 별도 사후 층으로 남겼다.

## Q2. B에서 지워진 뜻과 C에서 복원된 뜻

각 질의의 원문→연산·대상·행위자·관찰자 대응은 18행 [query-mapping.csv](evidence/query-mapping.csv)에 있다. P1에서 ‘일부를 집단 사이로 옮김’은 저장소의 감독 책임인지 기하 부품의 그룹 소속인지 구별하지 않는다. B의 Netfabb와 Tekla는 이동·복사라는 동작에는 맞지만 지켜야 할 사람 사이의 권한 경계는 없다. C는 repositories, maintainers, governing bodies, contributors를 복원하여 FINOS와 CNCF의 편입·위임 절차로 가까워졌다. 그러나 우산조직 안에서 자율적인 하위 프로젝트와 우산조직 밖에 남는 저장소는 다르다. 후자의 C2를 전자로 대신하지 않았다. rows P1-B-Q1-R1/R2/R3, P1-C-Q1-R2/R3.

P2에서 규칙 변경과 공개를 추상화하면 권한 있는 승인자, 의견을 제시하는 사람, 결과를 읽는 사람의 구별이 사라진다. B는 제품의 승인 절차와 행정 규칙 제정을 반환했고, C는 오픈소스 유지보수자·공동체·회의록을 회복해 실제 개정 절차를 반환했다. 그렇더라도 공개 열람권은 승인권이 아니다. C의 Feast와 Matplotlib도 공개 결정과 비공개 인선·민감정보를 구분한다. ‘구성원 모두가 읽는다’를 ‘구성원 모두가 결정권을 가진다’로 확대하지 않았다. rows P2-B-Q1-R1/R2/R3, P2-B-Q2-R1/R2, P2-C-Q1-R2/R3.

P3의 old readers는 B에서 사람 독자나 문서 판독기로 넓어졌다. C의 JSON document, schema URI, validator, notebook client는 판정 대상과 관찰자를 다시 특정했다. 그 결과 스키마 식별·버전 고정·이행 규칙이 돌아왔다. 다만 canonical이라는 문자열 규칙은 HTTP 응답의 불변성이나 구형 클라이언트 성공을 보장하지 않는다. 작성자는 무엇을 출력하고 검증기는 어떤 스키마를 사용하며 구형 독자는 어떤 내용을 보존하는지 각각 확인해야 한다. B의 VTML처럼 다른 어휘를 쓰는 원리도 구형 독자용 투영이라는 선택을 제시했으므로 B의 자료를 일괄 무가치로 기각하지 않았다. rows P3-B-Q1-R2, P3-C-Q1-R3/R4, P3-C-Q2-R1/R2/R4.

이 비교는 순수한 명사 복원 효과의 인과 추정이 아니다. A/B/C 질의의 총 단어 수는 각각68/85/89이며 문장 길이와 동사 구성도 다르다. 원문 역할의 정확한 명칭이 언제나 있는 것도 아니어서 일부 관찰자는 연구자의 명시적 대응이다. 모든 작업자는 원문과 사용자 브리프를 알고 있었고 다른 보기 결과가 있는 같은 연구 작업에 참여했다. [query-audit.json](evidence/query-audit.json), [researcher-roles.json](evidence/researcher-roles.json).

## Q3. 반환된 대상과 실제로 읽은 원문

82개의 서로 다른 URL이 90자리에 나타났다. URL 수는 독립 구현 수가 아니다. Netfabb 2021/2025 문서는 같은 그룹 기능 계보, ONES의 여러 글은 같은 공급자 업무절차 계보, OMI의 언어별 버전 정책은 하나, nbformat의 문서·validator 코드·스키마는 같은 구현으로 묶었다. 표2와 [judgments.csv](judgments.csv)는 원순위마다 실제 도착 URL·절·source ID와 읽기 비용을 연결한다. P2 A의 중복2자리와 P3 A의 중복1자리는 같은 보기의 앞선 open을 재사용한다. 별도 구현인지, 같은 원리의 다른 설명인지는 [semantic-overlap.csv](evidence/semantic-overlap.csv)와 원래 target ID를 함께 본다.

P1 B의 Netfabb·Tekla는 완성된 제품의 기능 매뉴얼이고 ONES는 서비스 제공자가 쓴 절차 설명이다. 판매자 글의 절차가 실제 구성에서 실행됐다는 시험은 없다. P1 C는 재사용 코드 부품보다 재단의 편입 정책을 가져왔다. P2는 대부분 조직 운영 규칙이며 이를 소프트웨어 구현으로 세지 않는다. P3 A는 바로 원 프로젝트의 재사용 구현·스키마 레지스트리, C는 포맷 규격·버전 정책·저장 모델 설계, B는 하이퍼텍스트 원논문·식별자 절차를 돌려줬다. ‘22개 자료’와 ‘9개 재사용 부품’을 동의어로 취급하지 않았다.

직접 원문이 아닌 접근도 그대로 남겼다. P1 A의 두 redirect 공지는 목적 문서를 읽은 것이 아니고, P1 C의 미러·재수록·해설4회는 원저작 최소량에 넣지 않았다. P2 C의 scikit-learn 반환 URL은 실제로 Kobo 로그인에 도착하여 실패1회다. P3 B의 COPIM 결과는 도구가 재작성 요약으로 반환했고 eduKate 글은 가상의 교육 사례를 재설명하므로 독립 원설계 근거로 세지 않았다. 미열람은 예산 제한으로 총22자리다. 다음 후보가 더 좋을 가능성을 잃지 않도록 그 주소와 순위를 보존했다.

## Q4. 링크가 제안하는 실제 선택과 반례

**P1: 이동 완료와 책임 수락을 구분한다.** ONES의 업무 인계는 접근권을 넘긴 상태와 수신자가 책임을 받아들인 상태를 분리할 수 있다는 부분 원리다. 수신 프로젝트의 선택은 ‘저장소를 옮기면 자동 편입’과 ‘범위·적합성 검토 후 책임 수락을 별도 확정’이다. 구별 입력은 저장소 접근권은 넘겼으나 수신 관리기구가 책임을 수락하지 않은 경우다. 대조는 접근권과 책임 수락이 모두 확인된 단일 저장소다. 그러나 해당 글은 Jupyter 표준 부합을 검사하지 않는다. 기존 동종 절차인 Jupyter newsubprojects의 integration criteria와 incubation outside Jupyter가 더 직접적이다. 그것도 특정 프로토콜 전략의 확인이나 모든 제외 저장소의 권한 경계를 대신하지 않는다. 이 반례 때문에 A의 잠정 적격1건을 철회했다. [self-review.json](experiment/P1/self-review.json), P1-A-S05, P1-B-S02/S04/S06.

**P2: 개정권과 공개 범위를 별도 선택으로 만든다.** Feast·Matplotlib·Scientific Python의 원 규칙은 누가 개정·인선에 관여하는지, 어떤 정보는 공개되고 어떤 정보는 비공개인지 구체화한다. 수신 선택은 기존 역할을 유지하며 공개 기록만 보강하거나, 명시적 권한 개정 절차와 공개 기록을 결합하는 것이다. 구별 입력은 한 유지보수자 인선이 비공개로 결정되어 일반 기여자가 전체 회의록을 볼 수 없는 경우다. 대조는 역할을 바꾸지 않는 민감하지 않은 결정을 공개 기록에 남기는 경우다. 후자는 양 선택이 같은 관측을 낼 수 있다. 전자에서는 C1이 가능해도 예외 없는 C2와 충돌한다. 연구자가 C2를 ‘요약만 공개’로 완화하면 후보가 좋아 보이지만 그것은 원 조건을 바꾸는 새로운 결정이다. P2-A-S01/S02/S04/S05, P2-C-S03/S05.

**P3: 식별자를 유지하는 것과 구형 표현을 생성하는 것을 구분한다.** VTML의 태그 처리·삭제 내용 보존·선택 버전 출력 규칙에서, 버전 태그를 모르는 독자가 태그를 무시하는 것만으로는 선택 버전의 의미를 보존하지 못할 수 있다는 최소 입력을 추론했다. 원 응답 L95–101의 삭제 문단은 같은 작성자의 캐시 재판독으로 다시 대조했다(review/result-review.json RR-04). 이는 목표 노트북 실행 결과가 아니다. 이를 노트북 이행에 옮기면 ‘새 필드와 옛 버전 라벨을 함께 둠’과 ‘구형 클라이언트용 내용을 실제로 변환·검증함’을 비교한다. 구별 입력은 구형 표현으로 나타낼 수 없는 새 기능을 담은 파일이고, 대조는 옛 표현만 쓰는 빈 노트북이다. OMI의 버전 차원 분리와 검증된 이행 규칙도 비슷한 경계다. 원리의 대응일 뿐 notebook 변환기의 구현이나 무손실 변환이 확인된 것은 아니다. P3-B-O3, P3-C-O1/O2/O4.

기존 동종 기능은 더 가까운 반례를 준다. nbformat의 raw v4.5 스키마는 추가 최상위 필드를 거부하지만 reader 함수는 validation 예외를 기록하고 파일을 반환할 수 있다. 그 둘을 ‘구형 클라이언트 실패’ 하나로 묶으면 잘못된 설계 선택을 한다. canonical URI의 네트워크 조회와 local registry 조회도 별개이며 JSON Schema 원문은 식별자와 locator를 구분한다. exact-version/digest로 거부하는 Modeller의 규칙은 불변성 요구에 가깝지만 알 수 없는 미래 버전을 받아야 하는 C1에는 역방향이다. P3-A-O2, P3-C-O3/O6; 사후 원코드 PS-P3-S12/S13.

## Q5. 확인된 동작과 적용 가설의 경계

원 검색에서 ‘두 조건이 같은 구성에서 확인됨’이라고 판정한 후보는 없다. 여러 문서의 편리한 문장을 합쳐 하나의 작동 환경으로 만들지 않았다. 환경·버전·권한·예외가 빠진 설명은 부분 지지로 남겼다. 현재 운영 정책의 개정 절차가 있다는 사실은 그 절차를 SPEC9 수신 프로젝트가 이미 적용했다는 뜻도 아니고, 공급자 절차 설명은 그 서비스의 특정 계정 설정에서 시험한 결과도 아니다.

가장 구체적으로 고정한 구현은 사후 판독한 nbformat v5.7.3, commit `bbd0f83b67a126cd04c48a03ad053c52e6597d96`이다. `nbformat/__init__.py`의 reads 예외 처리, `validator.py`의 미래 minor 완화와 explicit relax_add_props, `tests/test_api.py::test_capture_validation_error`, `tests/test_validator.py::test_future`를 읽었다. 첫 시험은 잘못된 노트북을 반환하면서 오류를 별도로 얻는 관찰을, 둘째는 강제 구형 검증과 future minor 문맥을 구분하는 입력을 준다. 시험 소스를 읽었으며 실행하지 않았다. 조회한 check-runs가 빈 목록이라는 사실만 확인했고 과거 CI가 실패했다거나 없었다고 단정하지 않는다. [P3 사후 증거](postseal/P3/evidence.json), PS-P3-S11~S17.

재개 시에는 JSON payload, 숫자 버전, schema URL, schema 바이트, reader/validator 버전과 출력 관찰자를 모두 고정해야 한다. 제안 내부의 required 불일치도 먼저 결정해야 한다. [reproduce.md](reproduce.md)와 P3의 사후 재현 지침은 실행 명령과 최소 입력을 남긴다. 이 보고서에 적힌 기대 관측은 적용 가설이다. 실행 로그·공개 성공 결과가 없는 칸을 자연어 추정으로 채우지 않았다.

## Q6. 새로운 URL, 새로운 원리, 다른 대상

A/B/C의 교집합을 URL로만 계산하면 C의 신규성이 과대평가된다. P1의 Jupyter 하위 프로젝트 위임(A)과 CNCF 연합 구조(C)는 다른 운영 주체이지만 부분적 감독 위임이라는 원리 P1-M01에 맞춘다. Jupyter admission gate(A)와 FINOS contribution gate(C)는 P1-M02다. 두 조건을 만족하는 공통 적격은 아니며, C의 다른 URL을 새 선택 하나로 자동 계산하지 않았다. Netfabb의 group/part와 저장소 집단은 같은 단어의 다른 대상이므로 governance 적격에서는 기각했다.

P2의 role-separated approval은 A·B·C 모두에서 발견되는 부분 원리다. ONES 승인 절차, 오픈소스 인선, 행정 규칙 제정은 승인자와 의견 제공자·독자를 나누지만 승인 대상·공개 예외·권한 변경 범위가 다르다. 같은 원리군을 같은 구현으로 합치지도, 서로 다른 URL을 모두 독립 선택으로 세지도 않는다. The Open Source Way의 여러 장은 한 원저작이며 이미 고정 입력에 알려진 참조였다. Matplotlib이라는 사례 자체도 사후 작성자 댓글에서 선행 인지가 확인되었다.

P3의 exact version / moving alias는 원 프로젝트 레지스트리(A), 다른 문서의 latest 규칙(B), 형식 버전 정책(C)에 다른 어휘로 나타난다. VTML의 투영은 notebook 변환과 구체 구현이 다르지만 ‘옛 표식 유지’만으로 의미가 보존되지 않는다는 부분 원리로 채택했다. B의 일반 개념 label/identifier 글은 사람이 읽는 용어 의미를 다루므로 parser 보존을 직접 증명하는 후보에서는 기각했다. 같은 단어의 대상이 다른 사례와 다른 단어의 원리가 같은 사례를 모두 남겼다. [semantic-overlap.csv](evidence/semantic-overlap.csv)는 원리군, 보기, 원순위, source ID와 대상 ID를 나란히 둔다.

### 경로 봉인 뒤 읽은 두 비소프트웨어 분야

공공 기록관리와 공연 진행은 사용자 브리프에 미리 노출된 분야다. 경로 봉인 뒤 자료4개를 직접 읽고 NARA 두 페이지는 하나의 업무절차 계보로 묶어 독립3저작으로 셌다. 이 자료는 원 검색 적중0건이며 오늘의 추가 비용은 별도 [postseal-costs.json](evidence/postseal-costs.json)에 있다.

[NARA accession](https://www.archives.gov/records-mgmt/accessioning)의 정의는 물리 보관과 법적 관리권을 구분한다. [Annual Move](https://www.archives.gov/records-mgmt/accessioning/annual-move)는 목록 대조·물리 인수와 별도 법적 인수 절차를 명시한다. 이로부터 얻는 검사 질문은 ‘어디로 이동했는가’와 ‘어느 주체가 어떤 범위의 책임을 받아들였는가’를 나누라는 것이다. 최소 반례는 저장소 주소나 자료의 물리 위치는 바뀌었으나 권한 이전이 아직 승인되지 않은 경우, 대조는 승인·인수가 모두 끝난 경우다. 법적 custody를 오픈소스 관리 권한과 동일한 제도로 취급하지 않는다. POST-X-01/02.

[UAF 무대감독 지침](https://www.uaf.edu/theatrefilm/stage-managers-handbook.php) §8.5–8.6은 대기·이해 응답과 긴 cue의 완료 보고를 구분한다. 신호 발신자, 실행자, 완료 보고를 받는 관찰자를 남겨야 요청 접수와 동작 완료가 뒤섞이지 않는다. 긴 cue가 아직 진행 중이지만 준비 응답은 온 경우가 구별 입력이며 즉시 끝나고 보고된 cue가 대조다. 보고는 독립 센서에 의한 실제 효과 검증이 아니다. [Kent의 2014 무대감독 handbook](https://www-s3-live.kent.edu/s3fs-root/s3fs-public/file/SM%20Handbook.pdf?VersionId=CZOkpiRCPICm8bJQIvjcJCT8lsTaplsO) pp39–40은 신호 수신 응답을 명시하지만 같은 완료 규약까지 확인하지 못했다. 같은 분야의 두 문서를 합쳐 공통 규칙을 만들어내지 않았다. POST-X-03/04.

## Q7. 제안자에게 새로웠는지와 당시 가용성

후행 토론과 출시 자료는 원 검색 봉인 `fbc05801af45f21e60d6901f3293f9af9969ef8d` 뒤에만 열었다. 원 검색에서 후속 문서 제목·미리보기 및 목적 원문에 들어 있는 가용성·후행 정보가 자동 노출된 경우는 exposure 파일에 남겼다. VTML 원문의 minimal-parser 가용성 문장도 이 노출에 포함된다. 사용자 Q7을 적용하여 일반 유지보수자 토론도 사후로 유보한다는 시행 명확화가 P2 A 단계에서 이루어졌으며, 완벽한 무노출 사전등록이라고 표현하지 않는다. 사후 결정 원장의 날짜·작성자 인지·채택·결과는 별개 열이다. [decisions.csv](decisions.csv), [protocol-clarifications.json](evidence/protocol-clarifications.json).

P1은 2021년의 외부 incubation 절차가 2024년보다 먼저 존재했다. 작성자가 그 파일의 서론을 수정한 이력은 있어도 해당 옵션을 이번 제안에서 읽고 기각했다는 증거는 아니다. 반면 2024년 6월26일 댓글은 일반 의사결정 규칙을 직접 인용한다. 6월27일 양 위원회 승인과 governance PR229의 공식 하위 프로젝트 추가는 조직적 편입의 결정 증거다. 개별 저장소 이전·제외 범위 권한·기술적 호환성 성과는 확인하지 못했다. 5월 논의에서는 별도 조직의 권한 경계와 중앙 Enterprise 정책 관리가 함께 등장한다. 이는 실제 대안 인지의 기록이며 보안 감사나 성능 시험 결과로 확대하지 않는다. [P1 사후 분석](postseal/P1/ANALYSIS.md).

P2의 6월5일 댓글은 Matplotlib·PSF의 거버넌스 전환을 제안자에게 전달했고 주저자가 답했다. 따라서 9월 main판 입력으로 C가 반환한 Matplotlib 사례를 저자에게 새로운 발견이라고 할 수 없다. 정확한 현행 charter의 모든 규칙을 그때 알았는지는 미확인이다. 6월19일에는 Jupyter의 옛 거버넌스를 읽었다는 발언과 single-vendor 대안 삭제 patch가 대응한다. 9월 승인은 초안 형태 승인이고 마지막 확인판도 draft·endorsement 공란이다. Jupyter의 2023년 전환 발표는 별도 실제 적용 사례지만 SPEC9 채택이나 효과의 증거는 아니다. [P2 사후 판독](postseal/P2/FINDINGS.md).

P3의 2023년 3월16일 제안자 댓글은 추가 필드를 거부하는 strict schema와 permissive reader를 이미 구분했다. 따라서 A의 해당 반례는 연구자의 검증에는 유용하지만 당사자에게 새로웠다고 할 수 없다. 7월11일의 날짜가 붙은 표결은 찬성8·반대0·기권0·미투표3으로 기록되어 있고, 나중 수정 가능한 PR 본문의 체크박스 수와 혼동하지 않았다. 제안 병합은 확인했으나 새 schema 동작의 출시까지 확인하지 못했다. v5.7.3의 relaxed validation 복원 PR343과 출시 기록은 원 제안보다 앞선 기능 가용성을 지지한다. VTML은 공식 WWW4 프로그램의 1995년12월12일 세션에 등재된 논문으로 제안 이전 존재가 확인되지만(정확한 최초 업로드일은 미확인), 저자의 선행 인지는 미확인이다. 날짜가 2026년인 현재 정책 문서에 대해서는 그 날짜만으로 2023년에 없었다고 판단하지 않는다. [P3 사후 원장](postseal/P3/sources.jsonl).

## Q8. 비용을 맞췄을 때 남는 결과와 역할별 행동

사후 조사62회는 본문·코드·패치·당사자 기록40, 메타데이터·서지 확인13, 검색4, 접근 실패4, 재작성 요약1로 별도 계수했다. 이62를 원 검색의 성적이나 비용에 섞지 않았다. 모집의 Git 지원 작업, 내부 HTTP 요청 수, 로컬 캐시 재판독·검토 노동시간은 같은 척도로 측정하지 않았으므로70+62를 전체 연구 노동비용이라고 부르지 않는다.

원 검색 비용은 A22·B24·C24, 총70회다. 각 보기 검색2회는 공통이고 문서 작업은52회다. 검색 결과90자리 자체를90번의 읽기로 세지 않았다. 실패·redirect·요약·미러도 작업 비용에서 빼지 않았다. 같은 보기의 중복 URL3자리는 원순위에 남기되 추가 open 비용을 부과하지 않았다. 각 제안의 실제 최솟값7·7·8까지 비교하여 긴 보기만 마지막 원문을 읽은 이득을 제거했다.

"""

cost_rows = []
for pr in ["P1", "P2", "P3"]:
    for arm in "ABC":
        r = counts["arms"][pr][arm]
        cost_rows.append([pr, arm, r["search"], r["document_operations"], r["cost"], r["common_prefix"], r["direct_original_document_operations"], r["direct_original_document_operations_at_prefix"], r["qualified"], "예산 내 없음(null)"])
text += table(["제안", "보기", "검색", "문서 작업", "실제 총비용", "동일 비용", "직접 원저작 작업", "동일 비용의 직접 작업", "적격", "첫 적격 비용"], cost_rows)

text += """

P1 C의 마지막 ORC 해설, P2 C의 마지막 Wikimedia 절차는 비용7 비교에서 빠진다. P2에서 C가 비용8에 추가로 읽은 절차는 공개 기록의 일부 규칙을 주지만 그 비용을 A의7회와 같은 것으로 취급할 수 없다. 어느 보기에도 조건부 적격이 없어서 동일 비용 적격 교집합은 모두0이다. 부분 원리의 종류가 다르다는 관찰은 남지만 분모·표본·질의 길이 차이를 제어한 효율 우위로 바뀌지는 않는다. 상세 누적 지출은 [runs.jsonl](runs.jsonl), [원 봉인](evidence/original-seal.json), [정규화 수치](evidence/normalized-counts.json)에 있다.

원문 확인자에게 남는 행동은 링크의 출처·판·대상·예외를 먼저 확인하고 후보가 같은 두 조건을 지지하는지 다시 묻는 것이다. 특히 첫 main판과 첫 PR판의 차이를 읽기 전에 해결해야 후대의 지식을 초기에 투입하지 않는다. 부품을 붙일 개발자에게는 ‘호환’이라는 말 대신 구형 reader의 반환값, validation 예외, 출력의 손실, URI 바이트 변화를 따로 측정할 최소 입력이 남는다. 제안을 승인할 관리자에게는 새 URL의 수가 아니라 기존에 인지한 대안, 제외 범위, 공개 정보의 예외, 권한 수락 주체와 검증 책임을 결정할 일이 남는다. 세 역할에 모두 유용한 것은 한 문장의 추상 원리보다 **입력·규칙·관찰자·적용 조건을 포함한 원리 링크**다. 이 마지막 문장은 관측에서 도출한 설계 권고이며 성능을 실험적으로 입증한 결과가 아니다.

## 자료 최소량·검산·재개 범위

[sources.jsonl](sources.jsonl)은 모집·원실험·사후 반례를 구분한다. 직접 읽은 저작 수는 `independent_work_id`의 중복을 제거해 계산하며, 읽은 원본과 최소량에 한 번 산입하는 행을 구분한다. 자료 최소량은 넘었지만 ‘최초 제안3건’의 증명이 부족하여 전체 완료로 올리지 않는다. 원순위에서 읽은 구현·정책·기능 자료의 혼합도 보존했다. 거버넌스 정책을 실행된 소프트웨어 부품으로 이름만 바꾸어 9개 구현 목표를 채우지 않았다. 직접 원자료가 없는 성공·채택·과거 검색 순위는 미확인이다.

검사기는 JSONL/CSV 키·열·행,18질의·90순위·52문서 작업 연결, 보기별 상한, 27개 원 파일의 SHA256 봉인, 사전 입력 불변, 같은 비용의 분자·분모, 허용 경로를 점검한다. 검사는 연구 진실성이나 외부 구현 성공을 자동으로 증명하지 않는다. 실제 실행 주체·SHA·명령·종료값은 [acceptance-evidence.json](evidence/acceptance-evidence.json), [SELF_CHECK.md](SELF_CHECK.md), 마지막 [HANDOFF.md](HANDOFF.md)에 기록한다. 같은 모델의 협업 검토와 작성자 재판독은 있었으며 독립 인간 검토자는 없었다.

재개 첫 행동은 SPEC와 JEP 후보 전체에서 PR의 최초 added blob을 수집해 모집틀을 다시 봉인하는 것이다. P1의 3월 원고, SPEC9의 summit 이전 작성판, JEP97의 3월1일 원고를 확보하지 못하면 창설판 층은 계속 미확인으로 둔다. 결과를 이미 본 작업자가 옛 기록을 다시 써서 무힌트 최초 탐색으로 만들 수는 없다. 새 모집·질의는 새 실행 층으로 분리해야 한다. 당장 실행 가능한 명령과 입력은 [reproduce.md](reproduce.md)에 남겼다. 중앙 상태 변경은 이 연구 결과와 별개이며 수행하지 않았다.

## 가장 중요한 불일치·약점 — 정확히 3건

| ID | 불일치·약점 | 다음 조사 | 판단이 바뀔 관측 |
| --- | --- | --- | --- |
| W1 | 첫 main 추가판을 최초 Git판으로 표현한 모집 오류. SPEC9와 JEP97에 앞선 PR판이 있으며 P3 C2는 나중 추가. 창설판3건·PR-first 전체 순위 미충족. | JEP/SPEC 첫8 후보의 PR added blob·rename·작성시각을 전수 대조하여 새 모집틀을 봉인하고, 외부 초안의 당시 판을 요청 가능한 공개 위치에서 찾는다. | 선행 판을 모두 포함한 순위와 적격3건이 확정되고, 각 C1/C2가 해당 최초판에 실제 존재하며 열린 선택이라는 직접 증거. |
| W2 | 표본3개 중2개가 조직 운영 문제이며 같은 모델·사전 지식·자동 노출·질의 길이 차이가 있다. 사람의 무힌트 탐색이나 일반적인 개발 검색에 대한 인과 결론을 낼 수 없음. | 새로운 실제 개발 요구를 모집하고 역할 대응과 길이를 통제한 질의를 사전 고정한다. 결과를 보지 않은 판독자의 범위와 비용도 별도 기록한다. | 다른 독립 요구·판독자에서도 같은 비용에 대상 복원이 새로운 조건부 적격 선택을 반복해서 더하거나, 반대로 B가 동등 이상 선택을 반환하는 관측. |
| W3 | 미열람22자리·접근 실패·현재 문서의 시점 제한·목표 실행0 때문에 적격0을 방법의 실패나 후보 부재로 해석할 수 없음. P3 strict validation과 reads는 다른 관측이며 그 차이는 저자도 이미 알았음. | 남은 순위를 새 비용층에서 읽고, 고정 old reader/schema/fixture를 실행하며 작성자의 인지·출시·실제 결과를 별도 대조한다. | 미열람 후보의 같은 구성에서 C1/C2가 함께 확인되거나, 제시된 최소 입력의 실제 실행이 기대 차이를 반박/지지하고 당시 이용 가능·선행 인지가 날짜 있는 원기록으로 확정되는 경우. |
"""

(P / "RESULT.md").write_text(text)
print(json.dumps({"result_bytes": len(text.encode()), "table_1_rows": len(first_rows), "table_2_rows": len(second_rows), "table_3_rows": len(third_rows), "source_rows": source_count, "independent_works": work_count}, ensure_ascii=False))
