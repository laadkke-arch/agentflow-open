# AF-RES-144 조사 범위와 판정 규칙

배정 직후 기존 checkout HEAD는 `24d4766a70c3153dbe1ee4f14f202d1b12c94b25`였다. GitHub 통합 브랜치를 다시 가져와 `d35bf54869a828cd76a74cf3075be094f62e5a59`에서 작업 브랜치를 만들었다. 계획 기준은 그 조상인 `d950356cdfae3edf799870cdeb90b93b5bd4ffd3`이다. 기존 `work` ref는 그대로 두고 새 단일 브랜치 checkout을 사용했다. 세션 시작 명령의 fetch에서 통합판이 `c088f5af075c3b010102d002e66c84d9263fe5de`로 전진했다. 그 사이 변경은 중앙 진행표 하나다. 시작 영수증의 작업 base와 통합 계약 SHA를 각각 보존한다.

당시 규칙은 통합판의 AGENTS.md, STATE.md, START_HERE, DOT_AUTOMATION, RESEARCH_WORKFLOW, CLOUD_WORKFLOW, RESEARCH_BRIEF를 읽었다. 중앙 행은 AF-RES-144 RUNNING, attempt 1, codex-cloud, owned_path가 이 디렉터리, source_commit 미입력이다. 유일한 등록 선행 AF-RES-140은 중앙 DONE, 고정 인계 PARTIAL이다. [중앙 진행표](https://github.com/laadkke-arch/agentflow-open/blob/d35bf54869a828cd76a74cf3075be094f62e5a59/docs/automation/dot-control.json) · [고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/e9ee53c53188449c289d4a7ea563e836eded1468/docs/workstreams/research/AF-RES-140/HANDOFF.md) · [고정 결과](https://github.com/laadkke-arch/agentflow-open/blob/a43dad1ece967452a996985541773396ea4363a5/docs/workstreams/research/AF-RES-140/RESULT.md)

고정 인계 SHA의 frame.csv, requirements.csv, first-links.csv, branches.csv, followup.csv, evidence/remote-recheck.json을 읽고 그 지문을 봉인한다. 이전 60개 모집창과 8사건, 최초판 0/8, 둘째 절 7/8·새 핵심 해결 0/7, 가상 질문 실제 발송 0회를 유지한다. Y1의 404도 이력에 그대로 둔다. 이번 판독자는 140의 사후 답을 아는 상태에서 C3·C4·Y2·Y3와 Y4 대조군을 재검사한다. 처음 상태는 140의 기록에서 인용하고 최초판층을 별도 검증한다. 날짜·작성자·편집과 본문 지문을 나눠 저장하며 공개 생성 이벤트 또는 생성본을 포함한 실제 편집 이력만 최초판 증명으로 센다.

## 입력과 성공 분모

| 등급 | 뜻 | 현재 계획 |
| --- | --- | --- |
| 저자 제공 원파일 | 내려받은 byte 원본 | 5건에서 별도 탐색. 없으면 결측 |
| 저자 본문 그대로 복원 예 | 명령에 표시된 bytes 또는 코드블록의 글자. 생성에서 선택한 개행은 명시 | C3 공개 printf, C4 공개 행, Y4 공개 배열 |
| 제3자 최소 재현 | 제3자가 제공한 예·옵션. byte가 없으면 실제 제공물과 재구성을 분리 | Y2 세/두 줄 제보와 같은 호출. upstream의 시험 bytes도 별도 집계 |
| 연구자 구성 대조 | 가정 또는 확장한 입력 | C3 실제 탭·따옴표·escape 충돌, C4 혼합/유효 날짜, Y2 각 개행과 빈 값, Y3 LF/CRLF × 최종개행, Y4 흐름형/주석 |

파일 bytes, CLI 상태, 다시 해석한 필드/노드, 원저자가 지정한 표현을 네 축으로 판정한다. 출력 실패를 재현한 실행은 실행 관측으로 센다. 원저자 문제 재현 성공 분모에는 원저자가 제공한 정확한 입력이나 그대로 복원한 예에서 해당 실패나 요구를 확인한 행만 넣고, 부분 등가의 런타임·OS는 남긴다. 구성 입력의 성공은 별도다. 로케일과 런타임, stdout과 stderr, 변경/보존된 파일을 기록한다. CSV 출력은 유효 방언을 선언한 독립 독자와 대조 독자를, YAML은 yq와 계보가 다른 파서의 scalar·태그·순서와 bytes를 확인한다.

## 계획된 분기와 반증

| 사건 | 실행 판과 비교 | 판정을 바꾸는 근거 |
| --- | --- | --- |
| C3 | csvkit 1.0.7·CPython 3.11.2. 기본, TSV, -B·escape, 빈 escape, 대체 quotechar, 충돌 입력 | 두 소비자 방언의 열 수 또는 필드값 차이. 발언에서 bare quote와 수신 프로그램 각각 확인 |
| C4 | 1.0.5·Python 3.8.16, 1.1.0 비교. 직접, 없는 옵션, in2csv 후 csvstat. 정상·모호·빈·잘못된 날짜 | ISO 변환에도 통계 타입이 그대로거나, 한 오류행으로 열 전체의 변환이 바뀜. 버전 고정 양쪽이 같은 경로인지 확인 |
| Y2 | 릴리스 4.30.5/.6/.7. 제3자 호출, LF/CR/CRLF 두세 개, 0 bytes, null, 빈 맵 | .7도 같은 입력에서 실패하거나 null 정책 선택에 따라 .6의 공개 호출이 나아지는 경우. 원 CI와 분리 |
| Y3 | 4.30.6. load_str, flow, literal, LF 정규화 사본, 최종개행 변형 | CRLF literal에서 코드포인트 등가 검증, LF에서도 실패하는 조건, 명시적 정규화 수락 발언 |
| Y4 | 4.30.6 비교. prepend, append, index replace, 주석·flow 대조 | 명시 순서가 다르거나 추가 서식 의무가 원문에서 확인됨 |

질문은 두 답에서 기술적으로 가능하고 정당화된 추천이 실제로 바뀔 때만 선택한다. 같은 결함이나 같은 옵션/처방으로 귀결되면 해당 문서나 수정판을 먼저 연결한다. 선택한 직접 링크와 조건부 링크는 과거 시점에서 알 수 있었던 것과 오늘의 재현으로 보강된 것을 구분한다. 저자의 수락·운영 반영·해결 시간은 별도 발언이 있어야 채운다. 원저자에게 새 답변을 보내지 않는다.

## 원문 열람과 기록

최소 하한은 이슈 5, 독립 CLI 기능 5, 별도 상류 수정/시험/공개 재현 6, 형식 계약 2, 신문과 음악 각 2로 22개의 고유 저작이다. 같은 저작의 댓글·판 사본, 같은 면 스캔·OCR, 같은 편곡 총보·파트는 하나로 센다. 개별 관측물도 기록한다. 작품과 기관 설명은 별도 저작이다. 검색 결과와 실패는 접근 원장에만 남긴다.

신문은 LOC Trek 1942-12-01 ed-1 image 5를 시도하고, 독립 스캔 또는 raw OCR이 끊기면 University of Oregon의 Morning Oregonian 1900-01-01 ed-1 seq-1 한 면을 대체 사례로 사용한다. 원판을 보고 OCR의 철자와 분단된 단어의 좌표·검색값을 대조한다. 음악은 같은 편곡의 총보와 이조 파트의 마디·성부를 직접 열고 기보음, 실음, 음역을 확인한다. 같은 판과 같은 주장을 확인하기 위한 최소 인용과 지문을 공개 브랜치에 남긴다.
