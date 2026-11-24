# AF-RES-196 범위와 사전 판정

이 검사는 공개 추천 문장을 읽는 독자가 당시 주체, 기준일, 정확한 원문 위치와 바이트를 어디까지 되찾는지 측정한다. W3C 실행, 출력 재생, 채점, 성능 비교는 선행 입력의 주장으로 취급한다. 제품의 DB·API·수집기·순위는 설계 범위 밖이다.

## 시작점과 노출 이력

| 항목 | 고정판·근거 |
| --- | --- |
| 계획판 | `0f6765df46ad2128c7fdfa92c3bf917bbfe0c5e6`. 진행표에 186은 RUNNING, 결과 SHA는 null, 196 행은 아직 없다. [계획판 진행표](https://github.com/laadkke-arch/agentflow-open/blob/0f6765df46ad2128c7fdfa92c3bf917bbfe0c5e6/docs/automation/dot-control.json) |
| 실제 시작판 | `72cf39aea54e2de2ba78a245593aefdc40205a16`에서 `work/research-af-res-196` 생성. 계획 이후 세 커밋의 변경 경로는 진행표 한 개다. 186은 DONE, 196은 RUNNING 1차이며 186 한 건을 의존한다. 196의 block_reason은 계획 시점 문구다. [실제 진행표](https://github.com/laadkke-arch/agentflow-open/blob/72cf39aea54e2de2ba78a245593aefdc40205a16/docs/automation/dot-control.json) · [의존 해소 커밋](https://github.com/laadkke-arch/agentflow-open/commit/22dd923) |
| 착수 자료 | GitHub에서 `AGENTS.md`, `STATE.md`, `docs/DOT_AUTOMATION.md`, `docs/RESEARCH_WORKFLOW.md`, 제품 브리프와 연구 색인을 읽었다. 진행표의 파일 API 본문이 비어 두 판의 고정 blob `2d3a6fd86da2fabd965eb7be19f870803abe777a`, `f0c9a6ea6f8a385ca103fabcb95df3b1a3bd130e`를 열어 행을 추출했다. 색인 blob `e76a22c3c4fbd588d61b7f1480049183adaeef7b`는 두 판에서 같다. [색인](https://github.com/laadkke-arch/agentflow-open/blob/72cf39aea54e2de2ba78a245593aefdc40205a16/docs/research/INDEX.md) |
| 직접 의존 | 중앙 result_commit `7042060cd73aad96f70ff290ec6d5f6adf22570b`에서 186 HANDOFF, RESULT 앞 38행, Gold T04 r1 stdout, JS T04 r1 stderr, 실행 audit stdout의 본문·위치를 열었다. 선행 자체 DONE, 독립 검토 미실시. 인계가 가리키는 직전 결과판은 `7182108b635189f6b866d99e2eaadc210d59d9f9`이며 이번 의존은 인계까지 포함한 중앙 SHA다. 착수 전에 고정 tree 목록 및 comparison/runs/frame의 헤더를 보았다. [고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/HANDOFF.md) |
| 누적 참고 | 147의 112 과거 답은 그 조사에 봉인된 입력·증빙의 재생 건수다. 184는 입력·산출 해시의 대상 구분을 요구하며 배포와 재빌드의 동일 산출물 연결까지는 확보하지 못했다. 두 인계는 이번 사건 또는 직접 열람 최소치에 산입하지 않는다. [147](https://github.com/laadkke-arch/agentflow-open/blob/30afd115c302f468d5007e380f72228c45130c37/docs/workstreams/research/AF-RES-147/HANDOFF.md) · [184](https://github.com/laadkke-arch/agentflow-open/blob/2b83f0fa4f86e97b9643eafaeecc6596cd245561/docs/workstreams/research/AF-RES-184/HANDOFF.md) |

위 착수 노출은 숨기지 않는다. 이하 규칙을 커밋한 뒤 개별 후보를 봉인하고 복원 출력을 만든다. 읽기 대상은 186 고정 tree 및 그 작성자가 명시적으로 연결한 고정 원문이며 186 작업 브랜치의 진행 파일은 열지 않는다. 저장소 변경은 AF-RES-196 경로 안에서만 한다.

## 예정 모집

- 문장 자리 6개. 당시 제출 H1·H2, 새 관측 O1·O2, 미실행 N1·N2. 유형마다 최대 2개. 당시 제출은 작성자가 `comparison.csv`에서 연결한 정확판 EARL 주소로 시작한다. 고정 원본의 저장소 상대경로를 정렬하고 한 파일에서 원래 인용의 시작행이 가장 이른 완전한 단언을 택한다. 서로 다른 파일을 우선한다. 외부 원본은 해당 고정 인용의 로컬 사본으로 넣는다.
- 새 관측은 `runs.csv`에 연결된 최초 반복 `receipt.json`의 상대경로를 정렬하고, 엔진별 가장 이른 완전한 한 건을 택한다. 영수증과 연결 원로그를 읽어 귀속을 확인한다. 미실행은 같은 원장의 `not_run_reason` 등 작성자가 명시한 행에서 안정 정렬하며, 실제 주체·기준일·원문을 확인할 수 있어야 한다. 빈 유형은 frame과 36셀 상태에 표시하고 정답표에는 추가하지 않는다.
- 제출의 기준일은 제출 레코드의 원래 날짜 필드, 새 관측은 선택 영수증의 시작 UTC, 미실행은 기록일이다. 제출일·저장소 수정일·실행일은 서로 바꿔 쓰지 않는다. 권고 문장으로 바꿀 때 작성자가 남긴 결과값과 당시 주체·날짜의 의미를 유지한다.
- 직접 열람 최소 22자료. 186에서 공개한 영수증·원로그 12개는 `runs.csv` 최초 반복 기준으로 상대경로 정렬 후 엔진별 처음 6개 영수증을 읽는다. 최소 6개 메타·정확판 자료에는 HANDOFF, RESULT, comparison, inputs, runs, frame을 포함한다. 별도 두 칸씩은 BagIt/의회도서관 원문과 NIST 로트 원성적서·동일 제품 레코드로 채운다. 외부 URL·복제본·미리보기와 동일 원문의 변형을 추가 건수로 세지 않는다. 직접 읽은 문서 수, 고유 바이트 지문 수, 계보, 186 실행 ID·제출 단언과 196 시험 셀을 각각 기록한다.

## 저장, 접근, 판정

- A는 원저자가 연결한 근거 주소와 한 줄 문장이다. 상대 링크는 고정판에서 절대 주소로 해석한다. 원래 주소의 SHA·경로·앵커는 보존한다. B는 거기에 근거 유형, 고정판, 원문 상대경로, 인용 바이트 SHA-256을 보탠다. C는 B에 원문 구간 각각의 바이트(Base64)와 locator를 보탠다. 동일한 UTF-8 JSON 직렬화에서 실제 저장 바이트를 잰다. 사전 동결 입력 목록에는 전체 원파일 SHA-256과 크기도 남긴다. 한 문장이 여러 비연속 구간을 필요로 하면 구간 순서를 고정하고 구간 경계를 포함해 해시한다. C의 비교 대상은 저장한 인용 구간이다.
- 거울 조건은 186 고정 경로 전체와 선택된 외부 정확판 원자료를 매 회 독립 임시 디렉터리에 둔다. 묶음 조건은 같은 시험 묶음만 둔다. 외부 주소를 호출하지 않고 알려진 원저장소와 경로 규칙으로만 해석한다. 가려진 원자료와 정답표는 복원 프로세스에 제공하지 않는다. Python worker가 허용 파일의 descriptor만 먼저 열고 seccomp로 신규 파일 열기와 소켓을 막을 수 있음을 사전 확인했다. 실행 영수증에는 양 접근의 차단 probe와 실제 원문 읽기 경로를 남긴다. 구현 또는 격리가 실패하면 그 회차를 미확인으로 남긴다.
- 발표 문장의 텍스트, 주체, 기준일, 정확 위치를 각각 판정한다. 문장 자체에 명시된 주체·날짜는 텍스트로 복원될 수 있다. 원문 바이트를 확보하고 고정판·창을 특정해야 원문 재열람으로 진입한다. 원문을 새로 읽었거나 C의 바이트를 디코딩해 실제 SHA-256을 다시 계산했을 때만 해시 대조로 친다. 판정자는 worker 산출을 미리 고정된 정답과 나중에 대조한다. 오판은 주장된 필드가 정답과 다르거나 잘못된 구간을 정본으로 인정한 경우, 보류는 입력·판독·근거가 부족한 경우다. 입력 결측은 어느 결과의 분모에도 넣지 않는다.
- 부모 프로세스의 준비·복사와 worker가 실제 읽은 파일을 분리해 센다. 묶음 읽기 수, 원자료 읽기 수, 조회 실패 수를 기록하고 외부 거울 운영비는 별도 범위로 둔다. 대표 결론은 예정 36셀과 실제 유효 셀을 먼저 공개한다.
- 통제는 본 표본 밖에 둔다. 서로 다른 경로의 같은 basename을 진짜/대체로 대조하고, 한 바이트 변조에서 해시 문자열이 남아도 판독을 보류하는지 확인한다. 주소만 있는 묶음을 접근 양 조건에서 비교한다. 잘못된 basename 채택과 무조건 보류를 함께 볼 수 있도록 정상 원문 회수 통제도 둔다. BagIt의 manifest·payload·fetch와 NIST 성적서 판·로트·제품 주소는 별도 비교하며 186의 실행 상태를 판정하는 데 사용하지 않는다.
