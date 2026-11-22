# NCQ 별도 원산출물 판독

저자 논문 [Swb-P07, p2의 Artifacts](https://brittany-reid.github.io/publication/reid-2023-ncq/reid-2023-ncq.pdf)가 직접 연결한 원 저장소를 GitHub 연결로 읽었다. 원 저장소의 고정판은 **ce14f193f7014c120f04619826cb251818d99b0e**다. 이 판의 commit은 2022-04-07 원 study snippet analysis 추가이며, 이 분석에서 파일을 임의로 나누지 않았다.

| 원장 ID·원본 고정 주소 | 직접 읽은 독립 내용 | 논문과의 연결 및 한계 |
| --- | --- | --- |
| [Swb-A01 · docs/instructions.md](https://github.com/Brittany-Reid/node_code_query/blob/ce14f193f7014c120f04619826cb251818d99b0e/docs/instructions.md) | CLI/REPL 명령, 검색 모드에만 있는 package/sample/task 검색, snippet 순환·편집·저장·키바인딩 전체 | §7.1.5는 실험 화면 오른쪽에 키/명령 문서를 제공했다고 명시. 이 파일의 어느 판이 실제 제시됐는지는 미확인. **원 도구 조작 지시문**이며 task brief라고 주장하지 않음. |
| [Swb-A02 · codesnippets1.csv](https://github.com/Brittany-Reid/node_code_query/blob/ce14f193f7014c120f04619826cb251818d99b0e/data/user-study/codesnippets1.csv) | 첫 연구의 노출/사용 코드와 실행 오류 코딩. 142레코드 중1개는빈 placeholder, 실제 snippet141. `Used?=1`41행, `0`100행 | Swb-A04 주석이 **first user study**로 명시. P1–P10,T1/T2. 행은 사람/전체과제/시간 측정이 아님. |
| [Swb-A03 · codesnippets2.csv](https://github.com/Brittany-Reid/node_code_query/blob/ce14f193f7014c120f04619826cb251818d99b0e/data/user-study/codesnippets2.csv) | 둘째 연구의 별도 코드 관측156레코드. `Used?=1`38행, `0`118행 | Swb-A04 주석이 **second user study**로 명시. P1–P10를 새 코호트에 다시 사용하므로 사람ID만으로 두 파일을 합치지 않음. |
| [Swb-A04 · user-study-snippets.js](https://github.com/Brittany-Reid/node_code_query/blob/ce14f193f7014c120f04619826cb251818d99b0e/data/scripts/user-study-snippets.js) | 두 CSV의 코호트 매핑, 입력4번째열의 lint 판정, 오류수 출력, 기본 첫 파일 실행/둘째 파일 주석 처리 | 원 분석 방법·실행 코드로 CSV와 내용이 다르다. runtime 오류 판정 전체, 최종과제 테스트, 시간 원자료는 포함하지 않음. Google sheet로 결과를 옮겼다는 설명까지만 확인. |

두 CSV의 필드는 `P,T,Package,Snippet,Used?,Runs?,Error`다. bytes를 UTF-8로 엄격 해석할 때 첫 파일의 byte0x85에서 실패하여 cp1252로 다시 읽고 전 레코드를 파싱했다. 실패와 재실행 결과는 `attempts.jsonl`에 남겼으며 파일별 SHA256은 `download-receipts.json`에 있다. 원문 전문/코드 원자료는 `tmp/`에만 두었고 커밋 대상에는 이 판독 결과와 출처만 남겼다.

## 실행한 것과 실행하지 않은 것

실행한 것은 파일 다운로드, CSV 파싱·행 수·사용 표시 수 집계, 논문 보고값 산술 재계산이다. 저자 lint 실행을 재생하거나 새 사람 실험을 실행하지 않았다. 다른 도구에서 나온 packet/실행 시간도 사람 노동 수치로 채우지 않았다.

재생하려면 고정판 NCQ와 README가 마지막 시험 환경으로 적은 Node14.17.0/lockfile을 격리 환경에 두고 원 명령 `node data/scripts/user-study-snippets`를 실행한다. 기본은첫 CSV이고, 둘째는 `main`에서 선택해야 한다. 원 스크립트가 오류수만 순서대로 출력하므로 CSV레코드와 결과의 대응을 보존해야 한다. 이것을 재생해도 Fig20 총 완료시간은 검산할 수 없다. 총시간을 다시 계산하려면 참가자·과제·조건·시작·완료의 타임스탬프 자료가 추가로 필요하다.

현재 저장소의 `README.md`와 일반 npm corpus(연결된 Zenodo5094598)는 위4개와 별도로 최소수에 더하지 않았다. README는 지시문과 겹치고, npm corpus는 사람 수행시간 데이터가 아니기 때문이다.
