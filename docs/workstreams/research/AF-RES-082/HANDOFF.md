# AF-RES-082 #1 — HANDOFF

## 연구 판정

**PARTIAL.** 지정한 모집·자료량·A/B 사전 판독·여섯 자리 비교와 카드 작성은 마쳤다. 공개 자료를 보수적으로 합친 **29독립계보**를 직접 읽었고, 원장 전체는201행이다. 그러나 두 조건의 같은 역사적 출판 상태, R의 최종 Pages 성공 상태, 두 단계가 모두 성공했는데 옛 URL만 잘못된 강한 반례를 확정하지 못했다. 원분모와 미확인 자리를 유지했다.

한 링크로 충분할 수 있는 조건은 **그 서비스가 실제 문서 원본의 생성과 목표 판·공개 경로를 담당하거나, 게시 가능한 HTML이 이미 준비된 경우**다. 서비스 밖에서 HTML을 만들어 전달해야 하면 생성기·게시처 두 링크와 완전한 HTML 트리·경로·권한의 교환 조건을 함께 안내해야 한다. 링크 수, 내부 단계 수, 공급자 수는 다르다. 원 소유자의 실제 선택과 연구자가 설계한 대안을 섞지 않았다.

| 핵심 분모 | 결과 |
|---|---|
| 모집틀 / 선정 | pypa58+r-lib164=222행 / 고정6자리 |
| 원요구 | 확인7/12슬롯; 두 독립 조건 확인1/6 |
| 원 소유자 경로 | 구성·생성 이력·현재 사이트로6/6 관측; 종단 성공6/6 아님 |
| 역사 생성 | Python raw 성공 로그3/3; R 생성git HTML3/3 |
| 역사 R Pages | 객체1/3; success확인0/3·미확인3 |
| 두 조건의 같은 역사적 출판 | 확인0/1·미확인1; 나머지5자리는 C2부재로 평가 불가 |
| 현재 공개 진입 / 선정 판 식별 | 6/6 / 3/6(P3·R2·R3) |
| R 대표HTML 무변경 | 2/3자리·4/6파일; 전체 사이트/연속성 아님 |
| 사전 예산 | 12안×2=24논리판독; 고유6문서·HTTP6·재사용18 |
| 원자료 / 사건 / 외부분야 원기록 | 전체201행·29계보 / 최소충족집합7계보 / 8원기록 |
| 대안 실배포·성공률·시간비교 | 배포0/12안; 성공률0/0 산출 불가; 실제 시간·청구 미확인 |

## 기준·범위·의존 고정

- 저장소/브랜치: `laadkke-arch/agentflow-open` / `work/research-af-res-082`.
- 유일 쓰기 범위: `docs/workstreams/research/AF-RES-082/`. 중앙 `dot-control.json`·STATE는 수정하지 않았다.
- 계획 기준: `e7a777f2c13b626532b5828591d6388743688b34`.
- 실제 시작 통합 SHA: `f736bd557fa4c40aecb6833165823196cfa42af2`.
- 유일 선행 연구: AF-RES-078 `f83a48c1c93f39796be82fee3d74b731b1a42f87`. HANDOFF·RESULT Q2–Q7·contracts.csv·cards.md 인수. SQLite·PNG·ZIP 격자/성능 재시험 없음.
- `workbench.session start`를 --allow/--dependency/--fetch로 실제 실행하여 manifest를 만들었고 exit0이었다. 시작 계약 해시: `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`.
- 지정 worker_kind는web-pro이나 실제 도구/모델 환경의 공개 자료 조사다. 별도 웹 UI Pro 세션을 실행했다고 주장하지 않는다.

## 결과 SHA·파일·원격 재열람

**인계 본문 직전의 완결 결과/수용 증거 SHA: `1f7a65f1ea27e5f59c8d7135d7354ae010cc8f41`.** 본 HANDOFF만 그 위에 마지막 단독 커밋한다. 최종 HANDOFF 커밋 SHA는 이 파일 안의 자기참조 값으로 만들지 않고 Git 이력과 최종 응답에서 식별한다.

주요 연구 본문을 확정한 SHA는 **`2e4ab7bc4ad4cf0ff35dc1d13fe97013670f430c`**이며 이후 RESULT 내용은 바뀌지 않았다.

| 파일 | 내용 |
|---|---|
| [RESULT.md](RESULT.md) | 필수 표1→표2→표3→분모, Q1–Q8, 정확히3약점/다음조사 |
| [FRAME.csv](FRAME.csv), [SCOPE.md](SCOPE.md) | 두 전체목록·원순번·포함/제외·시점한계·사전규칙 |
| [requirements.csv](requirements.csv) | 원문 조건·역할·태그·SHA·위치, C2공석5 |
| [prelinks.csv](prelinks.csv), [paths.csv](paths.csv) | 최초 A/B·순서·예산·재사용, 사후 판정 분리 |
| [sources.jsonl](sources.jsonl) | 각 원문 URL·판/절/행·UTC·내용·한계·지지/반증·계보 |
| [deployments.jsonl](deployments.jsonl) | 역사 생성/출력·현재 응답·실패·PDF/git 지문과 아카이브 공석 |
| [cards.md](cards.md) | 실제 보여 줄 짧은 답6개 |
| [SELF_CHECK.md](SELF_CHECK.md) | Q별 주장/원문·반대 탐색·공석·최소 후속 대조 |
| [COMMIT_LOG.md](COMMIT_LOG.md) | 요청 순서별 독립 묶음 커밋SHA |
| [evidence/validation.json](evidence/validation.json) | 27개 원장검사와 입력지문, source 참조 조인 |
| [evidence/acceptance.json](evidence/acceptance.json), [evidence/workbench-check.json](evidence/workbench-check.json) | 고정 결과의 --fetch 범위검사·원격 파일 재열람 |
| streams/python·r·publication·incidents·costs | 조사별 책임·증거·실패시도·원문 읽기 영수증 |

원격 재열람은 두 층으로 했다. 모든 묶음을 GitHub에 커밋한 뒤 public git fetch로 전체 tree를 다시 받아 로컬 tree와 `git diff --exit-code` 비교를 통과했다. 이어 고정 `2e4ab7bc…`의 RESULT.md를 GitHub connector로 직접 재열람했고 파일 blob SHA `8604f359eb4632b2b2b091e320be2808df97494c`가 로컬 git 객체와 같았다. 수용 증거 커밋 `1f7a65f1…`의 tree `b91849ddaab45378cd3a56379540562440e635a0`도 원격 재취득·동일성 비교를 통과했다.

## 실제 검사와 미실시

실제 실행:

```bash
python -B docs/workstreams/research/AF-RES-082/tools/assemble_ledgers.py
python -B docs/workstreams/research/AF-RES-082/tools/validate_research.py --final
python -B -m workbench.session check docs/workstreams/research/AF-RES-082/manifest.json --fetch
```

- 원장 검사: exit0, **27pass**, pending0. 고정6자리·FRAME222·요구12/7확인·C2한자리·12안/24판독·고유6/HTTP6/reuse18·source201개유일·참조208회/91종의 미해결0·29계보·사건7·외부분야원기록8을 검산했다.
- prelinks는 `8ba1d686d4c7e50067f9d52bc753a4e02708cd42`와 byte동일, paths의 사전32열은 `5f881c7094bf30be13069554b412a00c5b01f7c0`와 같다. 사후 채택으로 사전 판정을 바꾸지 않았다.
- 첫 범위검사: 대상 `2e4ab7bc4ad4cf0ff35dc1d13fe97013670f430c`,2026-11-23T14:05:44Z, exit0/pass/remote_checked. 전체 출력은 evidence에 커밋했다.
- **HANDOFF 작성 직전 재검사:** 대상 `1f7a65f1ea27e5f59c8d7135d7354ae010cc8f41`, 검사시각 `2026-11-23T14:07:27.971029+00:00`, **exit0 / passed / remote_checked**. 검사 전 working tree는 clean이었다. 비교된 통합 SHA는 `fe18482050b7b911e17267fa7dcaaa5b5fb46eb2`; changed_paths140, outside_paths=[], unmerged_paths=[], errors=[]이다.
- `git diff --check`와 원격 tree 비교도 exit0. 원장 검산·범위검사는 소비 사이트의 새 실행 성공을 증명하는 검사가 아니다.

실행하지 않은 것: 소비 프로젝트의 신규 빌드·배포, A/B 대안12안의 실험, 계정/DNS/토큰권한 변경, 유료 지원 요청, 사람 작업시간·사업자 청구 관측. 역사적 공개 로그가 빈 곳을 임의 실행으로 대체하지 않았다. 현재 사이트의 HTML과 당시 생성물을 읽은 결과만 기록했다.

## 막힌 이유와 첫 다음 행동

R1의 최종 Pages 상태 조회에서 공개 GitHub API가 remaining=0을 반환했다. 반환된 reset은 **2026-11-23T14:22:27Z**다. connector는 deployments endpoint를 지원하지 않아400을 반환했고 공개웹의 대체경로도 성공하지 못했다. 이를 회피하거나 실패율에 넣지 않았다. P3의 역사적 동시 공개와 RTD의 파일↔run manifest는 공개 자료에서 확보하지 못한 별도 증거 공석이다.

**첫 다음 행동은 정상 조회 가능 시 archive의 이미 발견한 deployment2328795124 상태를 읽는 것이다.** 아래는 미실시 재개 명령이다. 대상 repository·deployment ID·출력 경로를 고정했다.

```bash
mkdir -p docs/workstreams/research/AF-RES-082/evidence/resume
curl --fail-with-body --location --silent --show-error \
  -H 'Accept: application/vnd.github+json' \
  'https://api.github.com/repos/r-lib/archive/deployments/2328795124/statuses' \
  -o docs/workstreams/research/AF-RES-082/evidence/resume/archive-2328795124-statuses.json
```

입력 연결은 source `a4c6ec37fc8737a189ca7ec7095ec0161888f9e8` → 생성 HTML commit `45e0d9ebc168cf3632bc2d737c9db2318668a826`이다. 관측할 것은 최종 state, environment_url, log_url, 게시 입력 SHA의 일치다. status가 비어 있으면 미확인을 유지한다. success가 확인되어도 C2는 새로 생기지 않는다.

나머지 R 두 자리의 최초 조회 입력:

```bash
curl --fail-with-body --location --silent --show-error \
  -H 'Accept: application/vnd.github+json' \
  'https://api.github.com/repos/r-lib/asciicast/deployments?sha=92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1&per_page=100' \
  -o docs/workstreams/research/AF-RES-082/evidence/resume/asciicast-deployments.json
curl --fail-with-body --location --silent --show-error \
  -H 'Accept: application/vnd.github+json' \
  'https://api.github.com/repos/r-lib/bench/deployments?sha=b352fa4902c7fc0d1edc17f957c646072bfd8b9c&per_page=100' \
  -o docs/workstreams/research/AF-RES-082/evidence/resume/bench-deployments.json
```

생성 branch SHA의 조회가 비어 있으면 원태그 source SHA `f992b26f3cb30c799fbb95f6148852d8ae8a7f18` / `45c72b2dcbba2b181d24c175ebb90ff8ed5eccad`와 Pages 이력을 대조한다. 조회 빈 배열만으로 배포 부재를 단정하지 않는다. Link pagination이 있으면 끝까지 읽는다.

P3 후속의 입력은 RTD builds30298914/30298916, source `63fd63b352a9a8bdcc24791c9dbee952ee9a8abc`, 공개 URL `https://cibuildwheel.pypa.io/en/stable/`·`/en/v3.3.0/`·`/en/1.x/`, 역사 창2025-11-11~13 UTC다. 당시 capture/manifest에서 두 판과 심층 경로가 함께 식별되는지 찾는다. 이미 읽은 현재 HTML을 다시200으로 확인하는 것만으로 그 빈칸을 해소할 수 없다.

## 색인 반영 제안 — 배정자 작업

중앙 행에는 **PARTIAL과 재개 입력을 유지**하고, 이 HANDOFF 단독 커밋의 전체 SHA를 result_commit으로 사용하도록 제안한다. 원자료/필수문서 완료와 역사적 종단 검증 미확인을 각각 색인한다. suggested keywords: 문서배포, 관리형생성·게시, HTML교환조건, movingURL/고정판, source/build/publish구분, pkgdown, RTD, Pages, DOI/정정. AF-RES-078 연결 원칙을 문서 사이트의 입력판·출력경로·공개판으로 확장했음을 적되 다른 같은 회차 결과를 의존으로 추가하지 않는다. 중앙 편집·상태 변경은 수행하지 않았다.

## 가장 중요한 불일치·약점과 다음 조사 — 정확히 세 건

1. **두 원요구의 분모는1/6이며 과거 조직 소속도 미확인이다.** 같은 여섯 태그의 문서 정책·릴리스 토론·이전 기록을 입력으로 읽어 실제 독립 약속과 당시 소속을 찾는다. 원문이 나오면 평가 가능 분모를 바꾸되 표본은 교체하지 않는다.
2. **생성에서 역사적 공개로 이어지는 증거가 비었다.** archive2328795124/statuses, R2/R3 출력SHA, P3 두 run의 manifest와2025-11-12 전후capture를 입력으로 삼는다. 최종success·당시URL·지문·두 판 공존이 연결될 때 종단 판단을 바꾼다.
3. **동일 조사자의 조건부 안내 비교이며 강한 반례 런 쌍이 없다.** 동결12안·태그·2문서 예산의 독립 판독과, 공개 build-success/publish-success 런+잘못된옛URL 응답을 수집한다. 입력/산출물/route를 합치는 오류가 실제로 발생하는지 관측한 뒤 안내 충분성을 갱신한다. 현재 승률·사람시간·실제과금은 추정하지 않는다.

