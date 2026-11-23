# AF-RES-070 검산 기록

연구 상태는 **PARTIAL**이다. 아래 PASS는 원장·계약·해시 검증이며 사용자 질문 정책의 효과나 역사적 제품 실행 성공을 뜻하지 않는다.

## 실행 위치와 대상

모든 아래 shell 검사는 `/workspace/scratch/f1ffe17c302f/agentflow-open`에서 실행했다. 과제 허용 경로는 `docs/workstreams/research/AF-RES-070/`다. 계획 기준은 `320424d87f99e70c42eeb8cb7211467de27f2c2e`, 시작 때 확인한 실제 통합 HEAD 및 계약 base는 `76b8c1d15812fbf91b879f8444fd188ae7445802`, 인수한 유일 dependency 결과는 `367f29c6eb8f3da36c7728eb133f1cca9078efbf`다.

문서·제어 항목은 통합판에서 직접 읽었고, planning REVIEW-16은 `e4c6a79`, AF-RES-066의 HANDOFF/RESULT는 위 dependency SHA에서 읽었다. 중앙 dot-control.json은 수정하지 않았다. 실제 출발판과 나중에 움직인 통합 HEAD를 혼합하지 않는다.

## 실제 명령과 결과

| 검사 | 대상 SHA 또는 입력 | 종료코드 | 확인 결과·영수증 |
| --- | --- | --- | --- |
| 작업 계약 start | base76b8c1d, dependency367f29c6 | 0 | manifest 생성·원격 fetch; evidence/session-start.json |
| build_ledgers.py | C03 봉인 원장 및 후기 파일; 공개 스냅샷C04 | 0 | 64모집·24사례·127사건·48보기·66pin·35결과 |
| merge_sources.py | stream별 source/access 원장 | 0 | 253행,87원저작=63이슈+24공식; 계보중복 제거, 정확UTC누락5건 보존 |
| build_result.py | C04 `74421df3550bf6a02f1ba82d5f9e8c4bb31fc3db`의 수치 원장 | 0 | 필수표 먼저·주12/진단12·Q1–Q8·약점3; 미확인·반례 포함 |
| validate.py | HEAD=C04 및 작성 중인 RESULT/Q_CHECK의 해시로 고정한 입력 | 0 | 646개 검사 통과; evidence/validation.json |
| ledger_independent_audit.py | 현재 ledger 파일별 SHA256 | 0 | 최종 조인·시각·후보48개 패킷·B없음21건 처리 PASS; evidence/ledger-independent-audit.json |
| 독립 판정 검토의 읽기 전용 Python 검사 | C04 원장 파일별 SHA256 | 0 | 37개 판정 검산; evidence/adjudication-audit.json, REVIEW.md |
| git diff-tree | 76b8c1d… → C04 | 0 | 변경136경로 전부 owned_path; outside0; evidence/scope-c04.json |
| workbench.session check --fetch | C04 | 0 | remote_checked / passed, outside0·unmerged0·errors0; evidence/session-check-c04.json |

실제 명령은 다음과 같다. 코드 블록은 위 실행의 재현 명령이며 역사적 rclone/ripgrep/pandoc/jq 동작을 실행하는 명령이 아니다.

```bash
python -B -m workbench.session start af-res-070 --allow docs/workstreams/research/AF-RES-070/ --dependency work/research-af-res-066=367f29c6eb8f3da36c7728eb133f1cca9078efbf --output docs/workstreams/research/AF-RES-070/manifest.json --fetch
python -B docs/workstreams/research/AF-RES-070/tools/build_ledgers.py
python -B docs/workstreams/research/AF-RES-070/tools/merge_sources.py
python -B docs/workstreams/research/AF-RES-070/tools/build_result.py
python -B docs/workstreams/research/AF-RES-070/tools/validate.py
python -B docs/workstreams/research/AF-RES-070/evidence/ledger_independent_audit.py
git diff-tree --no-commit-id --name-only -r 76b8c1d15812fbf91b879f8444fd188ae7445802 74421df3550bf6a02f1ba82d5f9e8c4bb31fc3db
python -B -m workbench.session check docs/workstreams/research/AF-RES-070/manifest.json --fetch
```

계약 check는2026-11-23T09:16:18.730848Z에 통합 HEAD `dfe4c46e3e27629d44ff12ec2f613ba4e031c42e`까지 fetch해 확인했으며, 작업 base는76b8c1d로 유지했다. C04 계약 출력은 완료 도구 응답의 요약 전사임을 receipt에 표시했다. 최신 결과 SHA의 raw 출력은 후속 검증 절에 추가한다.

## 키·원장·분모 대조

- 기본키: enrollment_id, event_id, view_id, outcome_id, pin_id, source_id의 유일성과 실제 CSV 각 행의 열 수를 확인했다. issue_id로 모집·사례·보기·사건·결과·pin을 조인했다.
- 작성자: 관측 B3건의 numeric OP ID가 원이슈 작성자와 같고, 사건 링크·본문 해시·UTC가 연결된다. 이름 변경을 다른 작성자로 오인하지 않았다.
- 후보:48개 후보의 패킷 구조는 후보당2문서 이하·문서당 지정1절이다. A와 B의 후보 ID·판·절·목적·금지조건은 같다. 실제 추가 열람 준수는 별도 false로 표시했다.
- 수량: 초기32개, 적격31개, 주12·공석0; 확장32개, 선정 진단12개. 최초판56/64 복구이며 선정24개의 최초판은 전부 복구됐다. ripgrep 확장8은 현재 본문만 있으므로 시간순 최초판 분석에서 제외했다.
- 계보: 동일 이슈 댓글·아카이브·매뉴얼 다른판을 별도 원작으로 세지 않았다. 최소량87=63+24. jq2329 부분 로그는 산입하지 않았다. 출처별 확인 주장·판별하지 못하는 것·반례/미확인 열이 존재하며, 의미 범위는 REVIEW와 교차 검토로 보완했다.
- B: 새 값1·중복2·없음/불확정21. B없음21건의 정오값은 모두 unobservable이고 개별0효과가 아니다. 별도 실제 비교와 반사실은 case 슬롯 밖에 있다.
- 표3: 슬롯24=관측불가24. 개선/동일/악화 각 분류건수0; 효과 추정 분모0/N/A. 질문제안8·생략16, 기술층 오탐분모2·분자0; 엄격 예산층 오탐분모0/N/A. 같은 B 문장의 성공 표현은 독립 후속에 재사용하지 않았다.
- 모든 Q1–Q8은 Q_CHECK의 결과행·고정 근거 절·반례 탐색·미확인과 재개 원자료로 연결했다. 약점은 정확히3개이며 결론을 바꿀 증거를 적었다.

## A 봉인과 공개 순서

| 봉인 | 원격 커밋 UTC | 적용 범위 | 첫 후속 열람 |
| --- | --- | --- | --- |
| C02 a6e2f47e6cfa52e249f4d648016cf9d324eccae9 | 2026-11-23T08:40:30Z | 주12 + ripgrep 진단3 | RG08:41:08Z; RCL08:41:12.619911Z; PAN/JQ08:41:19Z |
| C03 39eec0e2cff033c9d34b55ae20e52880378ac4ef | 2026-11-23T08:53:01Z | rclone/pandoc/jq 진단9 | PAN08:53:24Z; JQ08:53:30Z; RCL08:54:02Z 이후 |

21개 pre/A/pins/enrollment 봉인 파일을 GitHub의 해당 고정 SHA에서 다시 가져왔다. 모두 현지 바이트의 Git blob SHA와 일치한다(`evidence/seal-verification.json`). 원문/후대본문 선노출과 pandoc7003 댓글 두 구절 선노출은 이 시간 검사가 지우지 않는다. 재구성층으로 남겼다. RG1808의 현재 편집 댓글은 정확 최초 발화시각이 복구되지 않았다.

## 실패·중단·시정도 남김

- 독립 원장 감사의 첫 실행은 exit1이었다. unknown 문자열을 값존재로 오인한2행, 최초판 미복구8행의 verified 플래그, numeric OP ID4개, 별도 관측 대조, RCL4914 후대 링크 노출, archive 줄 번호, CF source/event 오조인을 고쳤다. 첫 보고서는 evidence/ledger-independent-audit-first.json에 보존했고 최종 재실행은 exit0이다.
- ripgrep의 `git diff` 검증 시도는 중단되어 exit130이었다. 대신 원격 봉인 blob과 실제 바이트를 대조했다. 남은 0바이트 index lock 때문에 root의 첫 `git reset --mixed --no-refresh`는 exit128이었다. 실행 git 프로세스가 없음을 확인한 뒤 해당 오래된 잠금만 정리하고 재실행 exit0을 얻었다. evidence/git-lock-recovery.json과 stream 검산 파일에 기록했다.
- 최초 seal 목록 스크립트가 존재하지 않는 jq/pins.json을 가정해 exit1이었다. jq의 pin은 pre.json 안에 있음을 확인하고 실제 존재하는21개 파일만 대조해 전부 일치했다.
- jq의 역사 repo 이름을 현재이름으로 검색한3회는 HTTP200 응답에도 opening event를 찾지 못했다. stedolan/jq와 stable repo ID를 사용해 복구했다. 빈 잘못된 문서 경로 응답은 근거로 쓰지 않았다.
- 공개 /edits 및 일부 Archive의403/404·최초 댓글판 복구 실패는 우회하지 않았다. 실패 기록13행과 정확UTC누락5건은 SOURCES에 비산입으로 남겼다. API 도구 호출에는 shell 종료코드를 꾸며 넣지 않고 HTTP/접근 상태를 쓴다.

## 미실시와 남은 한계

역사적 제품 바이너리 실행, 작성자의 실제 환경 복제, 통제된 질문 실험, 질문 비용 측정은 미실시다. 부분 자료와 조건부 판만으로 완전한 실사용 성공을 주장하지 않는다. REPRODUCE.md에 필요한 판 SHA·실행 환경·명령·입력과 해시 대조 방법을 적었다. 해당 실행을 성공시켜도 과거 OP의 새 B나 질문 인과효과를 만들어내지는 않는다.

GitHub 결과 커밋의 표·원장 재열람을 수행했고 아래에 실제 SHA·결과를 고정했다. 이 검증 기록을 동결한 뒤 최종 결과 SHA를 다시 읽고 HANDOFF.md만 마지막 단독 커밋한다. 그 최종 재열람 영수증은 HANDOFF 본문에 남긴다.


## 결과 발행 뒤 실제 원격 재검증

- 검증 대상 결과 SHA: `f2e13005ff9e0ef8fe307ed48f2d13fbeba1dedc` (C05).
- GitHub 재열람 확인 UTC: `2026-11-23 09:26:55 UTC`. GitHub contents API의 해당 ref에서18개 파일의 완전한 디코딩 본문을 다시 가져와, 발행한 로컬 바이트와 일대일 비교했다.18/18일치, 잘린 본문이나 메타데이터만으로 통과시킨 파일0.
- 원격 CSV/JSONL을 다시 파싱해 ENROLLMENT64, EVENTS127, VIEWS48, OUTCOMES35, SOURCES253, PINS66, PAIRS10, Q_CHECK8, SEARCHES8행을 확인했다. RESULT 원격 표의 자료행은4/12/12/6/4/4이고 Q1–Q8 및 약점3개가 있다. 자세한 파일별 Git blob 기대값·본문 비교·열 수는 `evidence/remote-result-c05.json`에 있다.
- C05 checkout 뒤 `python -B docs/workstreams/research/AF-RES-070/tools/validate.py`를 다시 실행했다. exit0,646체크 통과. 입력별SHA256과실행cwd/대상HEAD는`evidence/validation.json`에 있다.
- `python -B -m workbench.session check docs/workstreams/research/AF-RES-070/manifest.json --fetch`를 C05에서실행했다. exit0, status=passed, checked_at=2026-11-23T09:27:28.121639+00:00, freshness=remote_checked. 실제stdout JSON과stderr를`evidence/session-check-c05.json`에보존했다. outside0·unmerged0·errors0이다.
- C05의diff-tree대조는exit0,141변경경로가모두owned_path에있었다(`evidence/scope-c05.json`). 중앙원장·다른작업브랜치의수정은없다.
- 이절은원격읽기와계약검증완료를뜻한다. 역사적도구실행·질문실험·빈정오효과분모를완료로바꾸지않으며연구상태는PARTIAL로유지한다.
