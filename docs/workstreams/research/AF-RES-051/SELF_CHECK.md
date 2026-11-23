# AF-RES-051 자체 검토

| 질문 | 답과 직접 근거 | 반대 증거·실패 시도 | 남은 결손 | 재개 행동 |
| --- | --- | --- | --- | --- |
| Q1 | NYC `date_of_interest`·일별 BX/BK 확진자 수·커밋과 Git 트리, GTFS route·service·direction·trip과 ZIP/멤버를 고정했다. [입력](evidence/inputs.json) · [S01 381·386·387행](https://raw.githubusercontent.com/nychealth/coronavirus-data/88fed814aae58e2b92fd4df5e9fa1ae3dc81f965/trends/data-by-day.csv) · [GTFS 예제](https://gtfs.org/getting-started/example-feed/) | S05 Bronx 누적 건수/율의 단위가 다르다. S01에서 날짜가 다른 228이 재현됐다. T04는 direction_id 공란을 제공한다. F01/F02의 Eurostat API 연결은 403, S2 옛 파일명 오류는 A01로 본 실험 전 정정했다. | 최신 공식 통계 API payload와 실제 영업 GTFS의 독립 feed_version. | 주요 표의 기준일·단위·발행 commit과 실제 날짜가 든 GTFS feed_info 원본을 다시 대조한다. |
| Q2 | 59개 분석 프로세스의 앱 open 원장과 strace가 일치했다. C2 대상 경로 open 관측 0, C3 대상 데이터 필드 조회 관측 0이다. [runs 1–48행](runs.jsonl#L1) · [실행 명령](evidence/execution.json) | C3은 통계에서 1377 B, 교통에서 74 B까지만 읽었다. T4 트립 ID는 조회 후 버렸다. [X01–X04](evidence/contrasts.md) | 준비 과정, 운영 캐시·사전 로드·비계측 프로세스의 부재는 미확인이다. | 다른 분석 자식과 네이티브 파일 접근을 포함하도록 수집 범위를 늘리고 독립 kernel 측정과 조회 원장을 대조한다. |
| Q3 | S는 469+831, T는 AAMV1과 AAMV3을 먼저 정답으로 고정했다. 별도 plain-line/SQLite 수치, OS open, 별도 필드 접근 중단 진단 및 32쌍을 대조했다. [truth 2–17행](truth.csv#L2) · [B-S/B-T](evidence/baseline.json) · [정답 검증](evidence/truth-verification.jsonl) | 두 통계 표현은 발행자 사전에 파생 관계가 있다. T 원문의 독립 txt와 ZIP 멤버의 CRLF가 다르다. [S10](https://raw.githubusercontent.com/nychealth/coronavirus-data/88fed814aae58e2b92fd4df5e9fa1ae3dc81f965/trends/Readme.md) · [T01b](sources.jsonl) | 별도 데이터 생산 계보와 외부 판독은 미실시다. | 범위가 같은 다른 집계의 재생을 확보하고 독립 판독자가 선정 행·반올림 전 값을 대조한다. |
| Q4 | P0 64보류, P1 16일치·48보류, P2 64일치다. 동일성→사용 지름길의 16FP·4FN을 재산출했다. [192 판정](decisions.csv#L2) · [48 구성](packets.csv#L2) | 누락을 완전으로 잘못 표시한 T1-1의 P2에서 A/K/R 거짓 음성 3건. [누락 감도](evidence/receipt-sensitivity.json) | 불완전 로그를 외부에서 탐지하는 일반 방법과 실제 사용자 판독률. | 64사실 중 열린 파일 하나를 사용 후 기록하지 않는 실험을 다른 계측으로 반복한다. |
| Q5 | C2는 네 번 모두 전체 해시가 같고 extra open은 관측 0이다. 같은 내용은 main 경로에서 사용됐다. C3은 헤더를 열어도 조회·감도가 관측 0이다. [판·파일 해시](evidence/inputs.json) · [X01/X02](evidence/contrasts.md) | C3 probe의 후보 해시는 다르다. C4에서 통계는 원산식에 기여하고 교통은 방향에서 버렸다. [16 검증](evidence/truth-verification.jsonl) | 논리 판이 같다는 증명이 파일 해시에서 유일하게 나오지 않는다. | 별도 게시판에서 같은 해시를 가리키는 두 발행 기록과 같은 실행의 경로 정답을 대조한다. |
| Q6 | 통계 C4 원합 1301, 보고 1300. NYC 공식 3/25판 원합 1331, 보고 1300. AAMV의 역방향은 수 2이고 행이 바뀌었다. [보조 49–59행](runs.jsonl#L49) · [X03–X10](evidence/contrasts.md) | 평일 날짜 변경과 FULLW 제거 날짜는 관측 0. NYC 3/20판 3/19 행은 미수록이다. GTFS 두 repo 판의 ZIP 전체가 같다. | 독립적으로 바뀐 운영 피드의 같은 서비스일, 전체 참조 무결성을 유지하는 C4 키 변형. | 동일일을 포함한 사업자 원본 두 개를 확보하고, 단일 비키 변경으로 버린 값의 결과 감도를 다시 본다. |
| Q7 | P1의 +5104 B/16 I, P2의 +29464 B/48 A·K·R을 검산했다. 실제 npm build 영수증과 PyPI publish 영수증을 각각 받은 산출물 해시와 연결했다. [구성 바이트](packets.csv) · [영수증 검산](evidence/attestation-check.json) | npm workflow의 npm ci 물리 I/O는 영수증에 없고 PyPI의 해당 predicate는 null이다. Debian 후보 환경 목록에는 대안도 담긴다. [P02~P07](sources.jsonl) | 실제 서명 신뢰 사슬·보존 기간·프로덕션 기록 비용·사람의 판단 비용은 미확인이다. | 한 빌드에서 원 산출물, 빌드 invocation, 외부 I/O 기록과 검증 가능한 지속성 메타데이터를 묶어 검사한다. |

사전 규약·기준선 커밋이 전체 패널 첫 실행보다 먼저 원격에 게시됐다. 숫자 기준선은 공식 파일·공식 다른 표현·손계산에서 읽었다. 여기서 독립은 같은 계측 함수의 출력을 양쪽에 쓰지 않았다는 의미다. 별도 외부 연구자의 검토는 미실시다.

검증 명령은 Python 3.12.14, Linux, strace 6.13에서 실행했다. 원장 59행을 별도 작업 디렉터리에서 다시 만들었고 두 시각 필드만 빼면 59/59가 같았다. 공개 구성·판정·짝·정답 검증·누락 감도 5개 파일은 바이트까지 같았다. [재실행 영수증](evidence/repeat-check.json)

```sh
python -B docs/workstreams/research/AF-RES-051/replay.py --cache /tmp/af-res-051-cache --fetch --output /tmp/af-res-051-replay
python -B docs/workstreams/research/AF-RES-051/score.py --runs-dir /tmp/af-res-051-replay --output /tmp/af-res-051-judgments
python -B docs/workstreams/research/AF-RES-051/render_result.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-051/manifest.json --fetch
```

원문 배당은 26개 고유 자료로 22개 기준을 충족한다. 42개 직접 열람 행에는 재열람한 다른 판과 보조 저작이 들어 있다. 실패 10행은 배당에서 제외했다. [출처 목록](sources.jsonl) · [수용 상태](evidence/acceptance-evidence.json)

고정 결과 sha를 정한 뒤 RESULT의 16·48행과 수용 원장을 해당 sha로 다시 연다. 이 원격 재열람과 `check --fetch`의 실제 결과는 뒤따르는 [고정 결과 확인](evidence/final-check.json)에 있다.
