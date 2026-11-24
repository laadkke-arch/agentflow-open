# AF-RES-241 사전 범위·예측

## 고정 입력

- 2026-11-24 UTC 착수. 계획판 [914dbfa](https://github.com/laadkke-arch/agentflow-open/blob/914dbfa789ebec97063ed97130ea2a71c2e9f503/docs/automation/dot-control.json), GitHub 최신 통합 착수판 [64e139f](https://github.com/laadkke-arch/agentflow-open/blob/64e139f16309e41e30f9ec634eabe17fef908bbd/docs/automation/dot-control.json). 커넥터의 대형 JSON 빈 결과를 GitHub Git으로 복구한 뒤 양쪽 전체 JSON에서 ID를 검색했다. 계획판에는 AF-RES-241 항목이 없다. 47차 배정 가져오기 b4cf83f와 착수 기록 64e139f를 거친 착수판에 RUNNING / attempt 1, codex-cloud, 소유 경로와 브랜치, 단일 의존 AF-RES-223이 있다. 네 운영 문서와 CLOUD_WORKFLOW, START_HERE, RESEARCH_BRIEF의 해시도 비교했다. 이 파일들의 내용과 AF-RES-223 의존 SHA는 동일하다. AF-RES-227·228·229 상태는 이번 표집 입력에서 제외한다.
- 유일한 의존 AF-RES-223의 중앙 상태 DONE, 중앙 result_commit 및 브랜치 팁은 [27518e8](https://github.com/laadkke-arch/agentflow-open/blob/27518e859181f0ece5de42dc54844d5b83688b7a/docs/workstreams/research/AF-RES-223/HANDOFF.md). 해당 HANDOFF 내부 자가 판정 PARTIAL 및 본문 결과판 c3895c3c8ad5a7be5c94cfa112ca89ac456c18b6을 유지한다. 27518e8에서 HANDOFF, RESULT, anchors.csv, returns.csv, SCOPE를 직접 읽었다. 소스 연결 8/12, 동일 화면 클릭·복귀의 작성된 기대 2/8, 런타임 DOM/AX/클릭 0건을 착수 기준으로 삼는다.
- 최신 통합 SHA에서 만든 작업 브랜치 work/research-af-res-241, 허용 경로 docs/workstreams/research/AF-RES-241/. [session.json](session.json)은 실제 workbench.session start --fetch와 의존 핀으로 생성했다.
- Apply a8244a455a02955bee016058484b06a485a0518d, Register 76099e8258aec4695442d7eccc98a506844668ca. 공개 Git 소스의 핀이다. 신규 서칭으로 원 모집의 Register 결측 네 자리를 채우지 않는다. 한국어 문구와 선호 재평가, 운영 계정·데이터·거래는 범위 밖이다.

## 모집과 순서

| 앵커 | 공존을 확인할 화면/행 | 처음 편집 가능한 입력의 예측 | 입력·복귀에서 틀릴 수 있는 구체적 조건 |
|---|---|---|---|
| A1-1 | Apply accept offer · Type | 같은 reference ID의 referee_type | 요청된 reference는 링크 제외. 같은 이름의 별도 reference는 계산 이름 충돌 가능 |
| A1-2 | Apply accept offer · Name | 같은 reference ID의 name | type 및 나머지 값 보존과 accept-offer 복귀는 별도 판정 |
| A2-1 | Apply course review · Course | application_choice의 course_id | course가 달라지면 site/option/mode 연동값이 바뀔 수 있음 |
| A2-2 | Apply course review · Full time or part time | 같은 choice·course의 study_mode | 선택된 site 또는 후속 단계는 조건에 따라 달라짐 |
| A3-1 | Apply contact review · Phone number | application_form의 phone_number | return-to 처리와 포커스 별도 |
| A3-2 | Apply contact review · Address | address_type와 조건부 country, 그 다음 주소 필드 | 첫 URL/입력과 실제 변경할 주소 줄이 다를 수 있음 |
| R1-1 | Register Check details · Course | 같은 trainee의 training_route | Course 이름 뒤에 여러 단계와 연동 필드가 있을 수 있음 |
| R1-2 | Register Check details · Education phase | 같은 trainee의 course_education_phase | 코스 양식 및 임시 데이터가 먼저 나타날 수 있음 |

행 단위는 한 앵커다. 기준 화면 네 개, 앵커 여덟 개, 각각 저장(S) 및 변경 없이 복귀(B)의 16 기본 여정. 위 순서에서 각 S 후 B를 각각 독립 초기 상태로 실행한다. A2의 기존 두 기대는 별도 실행한다. 공유 피드백 폼의 두 목적이 같은 입력 집합에 도달하는지 가능한 경우 각각 새 세션에서 대조한다. 양성·오류 각각 하나는 고정 입력으로 별도 깨끗한 재실행 대상으로 남긴다. 반복 렌더는 같은 원저작을 늘리지 않는다.

## 사전 가설과 기각 조건

- 조건부 예측은 모든 목표 링크의 시각적 이름 Change와 각 행·객체 suffix로 인해 같은 화면 안의 AX 이름이 구별된다는 것이다. 순서, 철자/대소문자/공백, 링크 역할 및 설명은 실제 DOM/AX 비교 대상으로 둔다. 행 key가 AX 이름에 포함된다고 가정하지 않는다. 같은 이름의 대상·별도 ID, 요소 미렌더, 숨김 CSS/aria override, suffix와 목적 입력 불일치가 반증이다.
- Tab/Enter로 실제 진입 이력과 activeElement, 문서 제목, 해당 ID와 첫 양식의 name/id·기존값을 별도로 기록한다. 선택·단계에 맞는 정상 Save and continue를 사용한다. 한 의미값 변경 시 나머지 모델·요약 행의 변화도 비교한다. 메타데이터, FK/파생 필드, 잠정 Wizard 상태, 사용자 입력을 각각 식별한다.
- B에서는 보이는 앱 Back/Cancel을 우선한다. 없으면 브라우저 이력으로 이동하고 복귀 수단과 시점, 확인한 중간 값과 절대 URL을 표시한다. 원 화면으로 돌아오지 않아도 관측 결과다. 필드·렌더 사실, 소스에서만 읽은 예상, 미확인 및 실제 관측 0을 분리한다. AX 트리와 실제 AT 발화의 분모를 분리한다.
- 키보드 이용자는 진입 전 대상 구별과 재탐색 부담, 편집기 개발자는 안정적 ID·입력 계약·검증·부수 변경, 도서관 이용자는 판·소장·거래 대상의 구별을 판정한다. 같은 href 또는 같은 폼의 서로 다른 목적, 표준상의 context 조건, 같은 책 제목의 다른 판, 저장 전 앱 Back과 브라우저 Back 차이를 반증 경로로 둔다.

## 노출 순서와 분모

1. GitHub 통합·계획판·AF-RES-223 파일을 읽고 본 범위와 session.json을 먼저 커밋한다. 선행 판의 예상 이름·필드와 반례를 알고 있으므로 블라인드 시험이 아니다.
2. 공개 고정 소스의 실행 지침 및 의존성을 열고, 실제 component/view 5, route/controller/form/fixture 6, 기존 시험·실행지침 5, AX·GOV 원규격 3, 공개 서지·운영 원자료 3 이상의 원저작을 직접 읽는다. UTC, 원문 위치, 명제, 한계와 실패를 source ledger에 기록한다. 공동 계보·별도 렌더·실패 응답은 독립 이용 사건으로 늘리지 않는다.
3. 실제 정상 route에서 여정을 실행하고 영수증과 기본 표를 먼저 남긴다. 이어 별도 대조와 오류 재실행, 도서관 두 판 및 운영 근거를 검토한다. 상충 결과는 잔존 조건과 함께 정정한다.
4. 결과판에서 실제 검사와 자체 점검을 하고 독립 검토 여부를 별도 표시한다. 기본 여정의 단계가 비거나 엔진·fixture 부팅이 실패하면 PARTIAL이다. 출처 수와 실행 분모는 별도다.
