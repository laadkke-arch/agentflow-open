# AF-RES-015 인계

## 고정 입력과 실행 환경

- 시작 SHA `55313b44af48ba85e967a96e885bf9b7a7d8c8ba`, chore/workspace-foundation. AGENTS.md, STATE.md, DOT_AUTOMATION, RESEARCH_WORKFLOW, RESEARCH_BRIEF와 진행표의 이 항목을 읽었다.
- AF-RES-011 `478c301b693896e2c6d777f46ac441f071bfdfe8`의 CASES, aging-observations, sources, HANDOFF와 AF-RES-009 `7f627a81199f06da7f7b15f979e7fef25dd17602`의 FAILURES, LANDSCAPE, SYSTEMS, HANDOFF를 직접 읽었다. [계약과 고정 의존성](manifest.json), [입력 해시](VERIFICATION.json)
- 관리형 Codex Cloud Linux의 `/workspace/af-res-015`, Python 3.12.14, package_managers 네트워크 프리셋에서 수행했다. 세션 표시 모델은 GPT-6 기반 Codex다. 세부 모델 변형과 추론 강도는 확인되지 않았다. 연구 작업자 한 명이 판정했다.
- 인계 직전 검증 묶음은 `5fb54b91366fcffa625cf7db7cdf4de7c3226bd3`이다. 원격 작업 브랜치는 `work/research-af-res-015`이며 변경 범위는 이 폴더다.

## 세부 질문별 결론

| 질문 | 결론과 적용 한계 |
| --- | --- |
| Q1 이유 추출 | 고정 스레드 61개·답 위치 635개에서 385개 답, 원자 이유 500개를 코딩했다. 후보 URL을 연결한 것은 194답, 직접 답 URL을 확인한 것은 139답이다. 이유가 없다고 기록한 37행 중 35답에는 별도 이유가 없었다. [추출](EXTRACTION.md), [이유 원장](REASONS.jsonl) |
| Q2 현재 | 195개(162답)를 판정했다. 175개 성립, 6개 약화, 14개 무너짐이며 305개는 현재 판단 불가다. 14개에는 처음부터 틀린 이유도 있다. [결과 표 1](RESULT.md) |
| Q3 당시 | 137개 이유(101답)를 복원했다. Git 고정판 115개(86답)와 날짜 있는 공식 기록 22개(20답)는 일부 답이 겹친다. 검증된 답 날짜와 과거 증거를 모두 갖춘 것은 130개(94답)다. 당시 성립했고 현재도 판정할 수 있는 83개 중 5개(6.0%)가 뒤에 무너졌으며, 정확한 답 날짜가 있는 경우에는 2/77이다. 후보 URL 연결만 한정하면 2/58이다. 처음부터 틀린 4개는 분리했다. [근거](REASONS.jsonl), [변화 구간](results/cadence.json) |
| Q4 신호 | 관측 분모가 있는 8종을 비교했다. 원 주소·이유를 모두 확인한 92행에서 404/410은 무너짐 세 건을 모두 놓쳤고, TanStack 등 두 행에 오경보했다. archived의 적중은 0, 놓침 5행, 오경보 10행이다. 시간 선행을 주장할 신호 계열은 없고 신호마다 독립 사례 다섯 건이 부족하다. [혼동표](results/confusion.json), [신호 원값](SIGNALS.csv) |
| Q5 비용 | 동일 12항목에서 작업자 원문 대조 24쪽, 자동 22 HTTP, 선별 22 HTTP와 14쪽을 관측했다. 선별은 두 후발 무너짐을 놓쳤다. 2개 정확한 사건에서 월·분기·연 확인 재생 중앙 지연은 12.5·58·242일이다. 사람의 실제 판독 시간과 실제 요청 간격은 미계측이다. [COST](COST.md), [재생](results/cadence.json) |
| Q6 다른 분야 | 법률 citator는 쟁점, 학술 정정은 발행물, 위키와 Perma는 원 주소와 사본, SWH는 코드 판의 객체를 관리한다. 운영자 공개 문서에서 법률 편집 반영 SLA나 위키 순회 시간 분포를 확인하지 못했다. [분야 비교](CROSSFIELD.md) |
| Q7 문헌 | 실증 원문 7개를 주소 실패, 원 문맥 재현, 내용 변화의 정의로 대조했다. 015의 조건부 이유 무너짐은 어느 문헌의 URL 실패율과도 분모가 다르다. 같은 사이트당 3개를 적용한 방법 문헌은 32개다. [문헌](LITERATURE.md), [자료 원장](sources.json) |
| Q8 대안 | 요청 시, 보존 링크, 신호 큐, 이유 만료와 정기 확인을 비교했다. 요청 시 이유 확인과 시점이 명확한 보존 링크를 함께 쓰는 안은 실제 판정과 역사 근거를 함께 남길 수 있다. 장기 운영 비용과 선택 효과는 후속 검증 대상이다. [결과 표 3](RESULT.md) |

## 가장 강한 관측 세 건

1. T009.A001 Directus. 답에 바로 앞선 Git GPL 파일과 2023-04-26 BSL 전환을 모두 확인했다. 현재 v12에도 회사 규모와 별도 권리가 붙어 있다. 회사의 가격표는 14일 Cloud 시험과 유료 호스팅을 구분한다. [답 시점 고정 GPL](https://raw.githubusercontent.com/directus/directus/874dda80788db252e8df799c508197de6d60c248/license), [이행 공지](https://directus.com/resources/changing-our-license-one-year-later), [현재 판](https://directus.com/resources/directus-v12-license-change)
2. T051.A001 TanStack Table. 011의 기존 URL D039 404와 현재 공식 v8 열 필터를 같은 이유에 연결했다. 추천보다 앞선 v8.21.3의 코드 문서에도 열별 필터 상태가 있다. [원 스레드](https://github.com/perses/perses/discussions/3862), [현재 문서](https://tanstack.com/table/v8/docs/guide/column-filtering), [고정판](https://raw.githubusercontent.com/TanStack/table/v8.21.3/docs/guide/column-filtering.md)
3. T020.A001 Dcoder. 제작사 연혁이 추천 당시 모바일 편집·실행 제공을 뒷받침하며 같은 사이트에 2026-03-31 종료가 표시된다. 2019년 답의 앱스토어 링크와 살아 있는 제작사 페이지를 구분했다. [제작사 종료와 연혁](https://dcoder.tech/), [연결과 분모](RESULT.md)

## 결과 §4의 세 약점

1. 확인 가능한 과거 근거가 공개 Git 쪽에 편중되고, 직접 추천 주소와 두 시점 판정까지 모두 있는 교집합이 작다. 150개 직접 링크 답을 연도·이유 유형별로 층화할 가치가 있다.
2. 당일 신호로는 선행 경보를 확인할 수 없다. 저장소 이동의 두 적중 행은 Almond 한 사건이다. 날짜 있는 독립 무너짐 30건과 성립 대조 30건의 전이 기록이 필요하다.
3. 비용의 12항목은 Codex 대조이며 정확한 시점의 과거 사건은 둘이다. 최소 세 명·30개 이유의 판독과 10개 이상 날짜가 있는 사건을 사용한 추가 검증이 필요하다. [최소 입력과 영향](RESULT.md#4-가장-중요한-불일치약점-3건과-다음-조사-제안)

## 검증한 것과 남은 것

- 분석 출력 11개 바이트 재생, 작업별 단위 검사 11개, 원격 작업 계약, 범위 검사, 별도 checkout의 공통 Workbench 검사를 실행했다. 공통 검사는 결과 표 SHA에서 수행했고, 날짜 근거 보정은 작업별 검사에서 확인했다. 초기 공통 검사기의 임시 경로 실패는 별도 checkout 바깥의 실험용 경로로 옮기고 통과했다. [검증 영수증](VERIFICATION.json), [공통 검사](results/workbench-cloud-check.json)
- 네 지정 익명 API 호스트는 원격 응답 전 403이었다. Wayback·SWH 사본, Scorecard 시계열과 RDAP 양시점 등록 자료, 신호별 독립 놓침과 오경보 5건, 사람 시간, 실제 캡처에서의 오인 인과와 새 모델의 별도 인계를 미실시·미확인으로 남겼다. [자체 점검](SELF_CHECK.md), [재개 입력](PROGRESS.md)

## 색인 변경 제안

| 작업 | 등록 문서 | 판단 |
| --- | --- | --- |
| AF-RES-015 추천 이유의 노후화 | RESULT.md, HANDOFF.md, VERIFICATION.json | 관측 결과 및 4개 표를 연결한다. 신호별 반례·사람 비용과 외부 API 차단을 수용 근거에 함께 표시한다. |

## 다음 첫 행동

고정 산출물을 읽고 아래의 오프라인 재생을 먼저 실행한다. 011·009 결과 커밋 객체가 없다면 그 두 브랜치만 fetch한다. 그 뒤 해당 주소 접근이 이미 허용된 환경에서 동일한 이유의 과거 공개 근거를 확인한다. T013.A001의 2018-10-25 Developer Program 사용 기간과 자격을 첫 사본 확인에 사용한다. 이는 원 답의 텍스트 드러난 제품에 대해 제안한 당시 공식 URL 후보이며 직접 링크로 세지 않았다. [재개 명령과 추가 입력](PROGRESS.md)

```sh
git fetch --no-tags origin refs/heads/work/research-af-res-011 refs/heads/work/research-af-res-009
p=docs/workstreams/research/AF-RES-015
PYTHONDONTWRITEBYTECODE=1 python "$p/src/verify.py" --fetch
curl --fail-with-body --silent --show-error --max-time 25 -D - --get 'https://web.archive.org/cdx/search/cdx' \
  --data-urlencode 'url=https://docs.microsoft.com/en-us/office/developer-program/microsoft-365-developer-program' \
  --data-urlencode from=2018 --data-urlencode to=2020 --data-urlencode output=json \
  --data-urlencode 'fl=timestamp,original,statuscode,digest' --data-urlencode limit=20
```
