# AF-RES-081 · 인계

## 1. 식별과 연구 판정

시도 1, Codex Cloud의 Debian 13.6 amd64. 작업 branch는 `work/research-af-res-081`, 허용 경로는 이 폴더다. 계획판 `e7a777f2c13b626532b5828591d6388743688b34`의 후손인 배정 시 통합판 **`f736bd557fa4c40aecb6833165823196cfa42af2`**에서 시작했다. 의존 결과는 **`AF-RES-077@a6338ffd6bc04d45f97e211031bd22aa870fbba0`** 하나다. [계약 manifest](manifest.json) · [077 인계](https://github.com/laadkke-arch/agentflow-open/blob/a6338ffd6bc04d45f97e211031bd22aa870fbba0/docs/workstreams/research/AF-RES-077/HANDOFF.md)

**PARTIAL.** 세 빌드의 모델 18셀·36회와 별도 화면·원시험을 실행했다. G/L을 가른 입력은 E05의 unlinked `cloneVoice`다. G는 복제 C1의 SELECTED를 지우고 L은 파트 밖의 이전 복사 비트를 남겼다. 두 경우 모두 C1은 Selection 목록 밖이다. 원래의 새 파트 신고 증상은 U에서 재현됐으며 G와 L이 모두 해결했다. 공식 tracker #281441과 첫 revision의 직접 재열람, 신고 설치물의 지문이 비어 있어 모집·출처 판정은 부분 완료다. [결과표와 적용 범위](RESULT.md) · [실측 원장](runs.jsonl)

첫 부모 `f4fcf53ff65c56f0efb616a3af209d3faba9b342`를 세 native 타깃에 사용했다. G는 실제 2019년 병합의 SELECTED 한 줄, L은 이번 연구 구현이다. 세 군의 probe, GCC 호환 수정과 flags는 공통이다. GUI 재현에는 별도의 Qt stream overload/LAME build 호환 수정과 workspace 데이터가 들어갔다. 077의 v3.0.1과 신고판의 release tags는 소스 지문을 확인한 별도 판이다. [역사 소스와 선택안](SCOPE.md) · [빌드 지문](evidence/build/build-info.json)

## 2. 결과 커밋과 원격 재열람

| 회차 | GitHub SHA | 내용 |
| --- | --- | --- |
| ① | `f8eaddd660557f8070efa762f4cb8e2fbc742375` | 역사판, 소유 경로, 의존 SHA, 여섯 입력과 사전 예상 봉인 |
| ② | `13cc9adfe24e543eeae20026c11867684d980b7f` | G/L·공통 probe 패치, 최소 MSCX, 세 빌드와 기동 확인 |
| ③ | `1e19e0d710b1b6f4607154a98204b1a3f9ae3eb5` | 36회 원 출력과 MSCX, 새 화면 6회, 원 CTest 21개, 독립 자료와 재현 도구 |
| ④ | **`d9ea5450a27b80f74e1efd30a7e8f933e3d256bd`** | 결과표와 자가검산, 새 clean checkout을 사용한 36회 비교 검증 |
| ⑤ | 이 파일의 커밋 | 인계만 추가 |

2026-11-23 14:06:04 UTC에 별도 빈 Git 저장소에서 [원격 결과 SHA](https://github.com/laadkke-arch/agentflow-open/tree/d9ea5450a27b80f74e1efd30a7e8f933e3d256bd/docs/workstreams/research/AF-RES-081)를 다시 fetch했다. 소유 tree `625055b8981b93e6d9bef122993ab683c8f3e4fc`와 384개 파일을 확인했다. RESULT, SCOPE, SELF_CHECK, cases, runs, sources, reproduce, manifest, verify receipt, G/L 패치, fixture의 원격 bytes를 해시해 **12/12** 로컬 결과판과 일치했다. 원격 checkout에서 검산기·픽셀·재실행 원장을 다시 읽은 명령도 exit 0이었다. [RESULT의 원격 파일](https://github.com/laadkke-arch/agentflow-open/blob/d9ea5450a27b80f74e1efd30a7e8f933e3d256bd/docs/workstreams/research/AF-RES-081/RESULT.md)

## 3. 실행 검사

| 실행 | 지문·결과 | 증거 |
| --- | --- | --- |
| Native 18셀 × 2 | 36/36 exit 0, 36/36 판독 가능. 반복 18/18 일치. G/L 동일 5/6, 상이 E05 1/6, 판별불능 0/6 | [raw·명령·SHA](runs.jsonl) · [검산](evidence/verify.json) |
| GUI File→Parts→New All | 3빌드 ×2, 6/6 exit 0. Flute 선택색 U에서만 보임. 실제 note click·dialog·tab의 별도 증거 | [Xvfb 기록과 화면](evidence/desktop/) |
| 고정판 CTest | 7 targets × 3 빌드, 21/21. 기존 source assertions와 현재 런타임을 판독. 과거 CI job 원 출력 확보 0 | [xUnit와 종료값](evidence/original/) · [CI 조회](evidence/original-ci.json) |
| 독립 작업 폴더 재생 | 13:58:21–14:02:01 UTC, 3 fresh binaries와 36/36 native replay. 최초 36회의 위치·시점 정규화 및 MSCX SHA와 일치 | [재실행 원장과 build](evidence/replay/) |
| 원장 | 43행, 독립 저작·사건 28, 다른 분야 13, 독립 실패·무변화 8 | [직접 판독](sources.jsonl) · [미접근 기록](evidence/access-attempts.jsonl) |

결과판의 clean checkout에서 아래 명령을 실행했다.

```bash
AF081_PACKET=docs/workstreams/research/AF-RES-081
python -B "$AF081_PACKET/tools/verify.py" --pixels --replay "$AF081_PACKET/evidence/replay"
python -B -m workbench.session check "$AF081_PACKET/manifest.json" --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

- 검산기 exit 0. [자가검산과 파일별 대응](SELF_CHECK.md).
- manifest 검사의 최종 실행은 14:07:03.848 UTC, 검사 SHA **`d9ea5450a27b80f74e1efd30a7e8f933e3d256bd`**, 통합 ref **`fe18482050b7b911e17267fa7dcaaa5b5fb46eb2`**, freshness `remote_checked`, exit **0**이다. 계약 v2 SHA-256 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`. 외부 경로·미병합 경로·오류가 모두 비었다. checker 변경 경로 383개와 owned tree 파일 384개는 manifest를 포함하는 셈에서 차이가 난다.
- 공통 검사는 같은 SHA의 별도 clean worktree에서 14:06:02–14:06:10 UTC에 실행했다. subprocess 종료값과 checker receipt는 **0**, 도구 wrapper는 1을 표시했다. unit 55, lab 7·9, demo·export·Git bundle 복원, discovery·smoke는 통과했다. 전역 session 목록은 `no_active_sessions`였고 위 manifest 검사는 별도로 통과했다.

## 4. 미실시·첫 다음 행동

공식 tracker와 history 조회는 접근 실패였고 기존 부분 캐시와 PR이 현재의 요구 근거다. 공식 v3.0.1 ZIP의 bytes, 원 신고자 binary, 과거 CI stdout은 미확인이다. E02–E04 전체 GUI, E05의 정확한 인자에 대응하는 GUI 조작, E06 playback timing과 숨은 tag child의 비교는 기록된 실행 범위 밖이다. 향후 L의 비용도 측정할 수 있다. [세 가지 우선 공백](RESULT.md#판단을-바꿀-다음-확인-세-건)

첫 행동은 원격 branch와 위 검사 SHA를 확인한 뒤 원 tracker의 확보 가능한 첫 revision과 3.0/2.3.2의 실제 release 자료를 찾는 것이다. #281441의 first revision을 확보하면 author/date/version/최초 조작을 PR 당시 문구와 대조한다. 그 뒤 release bytes의 SHA-256을 기록하고 [같은 fixture](fixtures/two-parts.mscx)에서 master C4를 선택한 채 Parts를 만든 직후 음과 목록을 읽는다. 이전 조회가 403이면 해당 상태와 새 입력을 유지한다.

```bash
git ls-remote https://github.com/laadkke-arch/agentflow-open.git refs/heads/work/research-af-res-081
curl --fail --location --max-time 30 https://musescore.org/en/node/281441
git ls-remote https://github.com/musescore/MuseScore.git 'refs/tags/v3.0*' 'refs/tags/v2.3.2*'
```

실행 계획과 명령은 [reproduce.md](reproduce.md)에 있다. 다음 native 판별은 두 성부의 range를 선택하고 Tools → Explode를 실행하는 입력으로 `CloneVoice` 진입, 복제 직후, 마지막 재선택, 후속 duration edit를 함께 읽는다. 새 part traversal은 비기본 tag의 기존 selected fingering을 숨겼다가 part 생성 뒤 다시 보이게 만들어 검사한다. 두 입력은 봉인한 여섯 자리를 교체할 필요 없이 추가 검증으로 기록한다.

## 5. 색인 반영 제안

`docs/research/INDEX.md`에 AF-RES-081, PARTIAL, “MuseScore 파트 생성과 공통 복사에서 선택 비트를 제거하는 적용 범위”, [RESULT](RESULT.md), AF-RES-077 선행 pin을 한 줄로 추가한다. 요약 값은 모델 36/36, G/L 1/6 차이, 원 tracker 첫 revision 미확인이다. 색인과 진행표 반영은 배정자가 수행한다.
