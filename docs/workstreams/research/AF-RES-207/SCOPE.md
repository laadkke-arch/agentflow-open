# AF-RES-207 범위와 사전 판정

한 실행의 인용 구간을 다시 열 수 있는 보관 표현으로 PET 분절의 시간 합계까지 확인할 수 있는지 비교한다. 확인 범위는 고정된 195 결과의 문장과 고정된 196의 원문 재열람 합격 표현이다. 제품에서 숫자를 노출할 조건과 근거 저장 비용은 별도로 보고한다.

## 시작판과 착수 관문

| 항목 | 확인 |
| --- | --- |
| 시작판 | `work/research-af-res-207`을 최신 통합판 `c860f8240ab7b7077e2d5b63e438ddd83ff69a27`에서 생성했다. 계획판 `050278651b11a2a3a49d45baebf41c707c06b700` 이후 네 커밋 `cc51999`, `ca4f683`, `81e21cc`, `c860f82`의 파일 차이는 진행표 한 개다. [계획 대비 GitHub diff](https://github.com/laadkke-arch/agentflow-open/compare/050278651b11a2a3a49d45baebf41c707c06b700...c860f8240ab7b7077e2d5b63e438ddd83ff69a27) |
| 진행표 | 195·196 모두 중앙 DONE과 40자리 result_commit을 확인했다. 207 항목은 RUNNING이며 block_reason에는 배정 계획 시점의 두 RUNNING이 남아 있다. [고정 진행표 L4514–4553](https://github.com/laadkke-arch/agentflow-open/blob/c860f8240ab7b7077e2d5b63e438ddd83ff69a27/docs/automation/dot-control.json#L4514-L4553) · [207 L4791–4813](https://github.com/laadkke-arch/agentflow-open/blob/c860f8240ab7b7077e2d5b63e438ddd83ff69a27/docs/automation/dot-control.json#L4791-L4813) |
| 195 | `a674c67aaf2c4f1a6aaef4b1ac278dabf44188c0`의 자체 PARTIAL 인계와 익명 배정·분절·실제 합계를 직접 읽었다. PET 시간(ms)과 원문 단어 분모가 있다. 정확한 HF TSV 및 독립 검수는 미확인이므로 raw PET 관측만 수치 판정에 쓴다. [고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/a674c67aaf2c4f1a6aaef4b1ac278dabf44188c0/docs/workstreams/research/AF-RES-195/HANDOFF.md) |
| 196 | `6147197ee77016a096412353bd9c3a9f4cd61b1e`의 자체 DONE 인계와 실제 판정·비용을 직접 읽었다. 주표본에서 `bundle_only`, `reopened`, `match`, `recovered`인 표현을 직렬화 바이트 오름차순, 동률은 저장안 이름순으로 고른다. O2의 C가 1,083 B로 최솟값이었다. [고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/6147197ee77016a096412353bd9c3a9f4cd61b1e/docs/workstreams/research/AF-RES-196/HANDOFF.md) · [판정 L7–25](https://github.com/laadkke-arch/agentflow-open/blob/6147197ee77016a096412353bd9c3a9f4cd61b1e/docs/workstreams/research/AF-RES-196/matrix.csv#L7-L25) |
| 운영 규칙 | 시작판의 AGENTS, STATE, DOT_AUTOMATION, RESEARCH_WORKFLOW, 제품 연구 브리프, 연구 색인과 클라우드 절차를 읽었다. 큰 진행표는 GitHub에서 fetch한 고정 Git blob을 열었다. [작업 계약](session.json)에는 원격에서 확인한 두 의존 브랜치와 시작판을 고정했다. 쓰기 범위는 이 디렉터리다. |

## 여섯 자리와 분모

195의 실제 `RESULT.md`에서 같은 유형의 첫 두 건까지 고른다. 표의 한 행이 문장에 해당하면 해당 행 전체를 출처로 삼는다. 행 설명과 핵심 주장으로 유형을 고정한다. 배정표의 예상 분절 수는 배정 메타데이터, 실제 시간의 개별 관측은 단일행, 명시적 `5분절 합`은 합계다. 정확판이나 QA 태그의 일반 caveat, 미완료 백업 단일행의 결측과 별도로, 비교 불가 조건을 명시한 실제 비교 행에서 두 보류를 고른다. [195 결과 L1–53](https://github.com/laadkke-arch/agentflow-open/blob/a674c67aaf2c4f1a6aaef4b1ac278dabf44188c0/docs/workstreams/research/AF-RES-195/RESULT.md#L1-L53)

| 자리 | 기준 원문 위치 | 모집 단위 |
| --- | --- | --- |
| S1, S2 | L30, L31 | TUR 1 HT E1과 E2의 PET 분절 각 하나 |
| M1, M2 | L35, L36 | ITA 1 HT·PE1의 분절 시간 합 각 하나 |
| W1, W2 | L46, L47 | ITA 1·2의 동등 품질·독립 QA 포함 총노동 비교 보류 각 하나 |

주 분모는 여섯 자리 × 두 표현 = 12셀이다. 빈 자리는 입력 결손으로 정산하며 대체 표본으로 채우지 않는다. 네 통제는 동일 합계의 행 교체, ms/초 단위 오독, 누락의 0 대체, 동일 참여자의 관측 복제다. 통제마다 두 표현을 같은 데이터 사본에서 읽고 일반화 분모와 분리한다. 수치의 분모는 분절 행과 영어 원문 단어를 따로 두고 사람·배정·조건도 기록한다. 합산은 번역자 PET 사건창의 ms와 원문 단어 합이다. 독립 검수자·수용 결과·시간이 연결되지 않으면 QA까지 포함한 비교의 수치와 완전 분모를 미확인으로 둔다.

## 두 표현과 관측 규칙

- A는 196의 C와 동일한 여덟 필드 `url`, `sentence`, `type`, `revision`, `relative_path`, `excerpt_sha256`, `locator`, `excerpt_base64`를 쓴다. 인용 범위를 정확히 보존하는 안에 유리한 조건으로, 단일행과 합계에는 195의 `segments.csv` 헤더와 해당 원행의 정확한 구간을 넣는다. 보류는 `assignments.csv` 헤더와 원문 문서의 배정 구간이다. 합계에서 좌표가 이미 행을 모두 특정할 수 있다는 가능성을 시험한다.
- B에는 행 선택식, 그룹, 결측, 단위, 산식의 다섯 필드만 더한다. 단일행에는 자료 차원의 술어를 쓴다. 합계에는 언어·문서·조건과 원자료에 근거한 분모 점검을 쓴다. 추가 필드에 산출값이나 정답 행 목록은 넣지 않는다. 같은 UTF-8 정렬 compact JSON과 마지막 LF를 사용한다. 다섯 필드의 순증분을 중복 없는 순서로 분해하고, 같은 규칙의 공용 저장 가정은 별도 계산한다.
- 확인자는 한 번에 묶음 하나와 같은 익명 로컬 자료만 열 수 있다. 관측한 수치·단위·행 멀티셋·분절/단어/사람 분모·유보 근거를 분리해서 기록한다. 표시 문장의 수치는 주장 검사용이며 관측값은 원행으로 계산한다. 판독 후 열린 자료 범위를 점검한 다음 별도 채점에서만 정답을 연다.
- 정확한 값·단위·행·분모를 전부 복원하면 정답이다. 주장값이 맞아도 틀린 구성 행을 승인하면 오승인이다. 선행 자료의 결손이나 통제의 충돌을 근거로 한 보류는 합리적 보류다. 실행 실패와 근거 있는 부정 판정을 구분한다. 자체 판독기가 어떤 내장 해석을 했는지 결과에 남긴다.
- 읽은 시점의 195 결과표, 배정·분절 일부, 합계 영수증과 196의 실제 판정·비용·정답·표현을 범위 고정 전 확인했다. 작성자는 이 수치를 알고 있다. 정답과 모집 원장을 실행 전에 커밋하고, 판독에 이 두 파일과 원본 저장소 경로를 제공하지 않는다. 작성자와 판독기 작성·채점자는 동일 세션이다.
- 195의 ZIP 추출·조건 효과 실험과 196의 세 안×두 가용성/JSON-LD 복원은 반복하지 않는다. 공식 통계는 단위와 결측 표현을 검토하는 별도 대조다. 공개 원문을 인용할 때 각 파일의 계보와 최초 자료의 관측 사건을 구별한다. 검증 범위는 추출 익명키·관측·수치로 한정한다.

범위 커밋의 필드 개수 설명을 7개에서 8개로 교정했다. 열거 목록과 비교 규칙은 처음부터 위 여덟 필드였다. [196 생성 코드 L67–79](https://github.com/laadkke-arch/agentflow-open/blob/6147197ee77016a096412353bd9c3a9f4cd61b1e/docs/workstreams/research/AF-RES-196/make_bundles.py#L67-L79)
