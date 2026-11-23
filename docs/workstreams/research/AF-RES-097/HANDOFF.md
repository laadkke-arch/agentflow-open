# AF-RES-097 인계

**상태 DONE.** 원 입력 두 개와 본 실험 세 환경을 확보했다. 주 실행 **24/24**, 동일 호출 반복 **12/12**, 사건×판 판정 **양쪽 일치 3/6·한쪽만 충족 3/6·양쪽 미충족 0/6·미확인 0/6**이다. HTML의 현재 본문·편집 공개 기록은 확인했다. GraphQL의 이전 본문/댓글 전체 이력과 실제 신고 OS 설치는 미확인 범위로 남긴다. [결과 세 표](RESULT.md) [Q1–Q7 자기 검토](SELF_CHECK.md)

**핵심 반환.** #5593은 세 판을 함께 안내할 때 원 P에서 곧바로 `convert('RGBA')`. 8.2.0의 이 원 PNG에는 `convert()`도 가능하다. 8.3.0과 8.3.1의 기본 반환은 `RGB`이며 검정 색 키가 남는다. 이를 다시 RGBA로 승격한 별도 대조에서 불투명 검정 199개도 투명해졌다. #5595는 8.2.0까지 지원하려면 `putpalette(p, rawmode='RGB')`를 대표 링크로 선택한다. 8.3.0·8.3.1은 원 p의 저장 전 팔레트·번호·RGB 목표에서 두 경로를 안내할 수 있다. [재승격 원 출력](evidence/experiment/promotion-5593-8.3.0-default-1.stdout.json) [8.2.0 배열 차이](evidence/experiment/5595-8.2.0-object-1.stdout.json)

**재개 첫 행동.** 다음 질문이 단일 alpha 밖의 적용 범위라면 고정 [상류 다중 alpha 시험](https://github.com/python-pillow/Pillow/blob/51591a80a4e14543ea8cbe93026db5e79354b8c4/Tests/test_file_png.py#L220-L228)의 [pil123p.png](https://github.com/python-pillow/Pillow/blob/51591a80a4e14543ea8cbe93026db5e79354b8c4/Tests/images/pil123p.png)를 내려받아 먼저 bytes SHA와 tRNS를 등록한다. `run.py`의 `make_indexed_png`로 동일 palette에서 `[0,128]` tRNS의 mini PNG를 만들고, 새 테스트 슬롯에서 두 호출 및 index별 alpha를 재측정한다. 이 원 실험의 24행과 입출력 SHA는 보존한다. [재현](reproduce.md)

색인 제안 한 줄 **AF-RES-097 · DONE · Pillow 원 입력 2건×3판, 24/24·반복 일치 12/12·대체 가능 3/6, #5593 8.3.0/1 명시 RGBA만, #5595 8.2.0 raw만 · 결과 `f475e1a55c5be68cd6d9bcca1a7c7b4f9893e24c`.**

## 원격 커밋 및 변경

| 단계 | GitHub SHA | 변경 경로 |
| --- | --- | --- |
| 시작 최신 통합판 | `01177554d0fbd33a914ea9c982c348d442d1358d` | 계획판 `fcde6becc49120c5be91adf43fb5b4aa42e71d48`과의 차이는 중앙 진행표. 원격 의존 및 읽은 인계 `ca82b938e429779d73d9de134ddac93e462ff03d`, 연구 결과 입력 `4b1233ead75c0a701b497226b446794eedea3ceb`. [범위와 blob](SCOPE.md) |
| ① 이슈·입력·봉인 | `64dc8ea05ad1d9e41439c0229ed9232132e80133` | `SCOPE.md`, `evidence/issue-history.md`, `inputs.json`, `manifest.json`, 입력 판독용 `run.py`, 초기 24행 `runs.jsonl`. [변경 목록](https://github.com/laadkke-arch/agentflow-open/commit/64dc8ea05ad1d9e41439c0229ed9232132e80133) |
| ② 판별 환경 및 교정 | `ff43fe4ec2c4ed329427ddd646f376f74944c861` | `environment.json`, `evidence/calibration/` 10파일, `evidence/install/` 20파일, `inputs.json`, `reproduce.md`, `run.py`, 총 34경로. [변경 목록](https://github.com/laadkke-arch/agentflow-open/commit/ff43fe4ec2c4ed329427ddd646f376f74944c861) |
| ③ 실행 원장 | `8ee098ca76377c8183aef3079af3e41e71317e88` | `runs.jsonl`, `evidence/experiment/` 86파일, 총 87경로. [변경 목록](https://github.com/laadkke-arch/agentflow-open/commit/8ee098ca76377c8183aef3079af3e41e71317e88) |
| ④ 결과·검사 대상 | `f475e1a55c5be68cd6d9bcca1a7c7b4f9893e24c` | `RESULT.md`, `SELF_CHECK.md`, `audit.py`, `evidence/cross-domain.md`, `evidence/issue-history.md`, `evidence/reconciliation.json`, `evidence/replay.json`, `reproduce.md`, `sources.jsonl`. [변경 목록](https://github.com/laadkke-arch/agentflow-open/commit/f475e1a55c5be68cd6d9bcca1a7c7b4f9893e24c) |

각 묶음의 commit 직후 `work/research-af-res-097`에 push했다. 130개 결과 변경 경로는 모두 `docs/workstreams/research/AF-RES-097/`다. 초기 checkout의 로컬 `work` ref 충돌은 별도 신규 clone으로 해결했다. `manifest.json`은 요청의 작업별 정확한 start 명령과 시작판에서 생성됐다. [작업 계약](manifest.json)

## 핵심 근거와 분모

| 파일 | 관측 범위 |
| --- | --- |
| [입력 지문](inputs.json) | Gist 고정 ZIP의 304B `indexed_with_transparency.png`, SHA-256 `a4fa91aa20ae6115d4c5520d11fc8e2f1a52a4d3df53860175a51eaa94ce12be`, IHDR/PLTE/tRNS/CRC, index 좌표·개수. #5595의 literal SHA-256 `3d188159bb897e885f2910b00dff302d0b284f9c0daa7a012bcd347cd88831af`. Gist raw 접속 제한 뒤 GitHub codeload의 동일 리비전으로 받았다. |
| [환경](environment.json) [교정](evidence/calibration/ledger.jsonl) | 공식 wheel, 태그, CPython 3.9.23, 실제 `PIL`·`_imaging`. 주 교정 6/6, 보조 8.4.0 교정 2/2, 설치 결손 0/3. |
| [77행 원장](runs.jsonl) [stdout·stderr](evidence/experiment) | 주 24, 보조 53. 보조는 47 출력+6 의도한 RGB mode 거절. 저장 재열기 6, 같은 객체 비교 2, 소형 PNG 30, 재승격 3, 수정판 원 PNG 2와 Hopper 4행. 현재 연구자 실행과 2021년 공개 댓글을 별도 관측으로 귀속했다. |
| [자료 원장](sources.jsonl) [타 분야](evidence/cross-domain.md) | 외부 1차 자료 40개, 전체 61행. Q별 실제 읽은 근거·정확한 절·시각·출처 지문과 미확인. Arrow 18.1.0과 GDAL 3.10.0의 원 시험은 직접 읽었고 양쪽 실행은 미실시. |
| [재계산](evidence/reconciliation.json) [재현](reproduce.md) [독립 환경 재생 영수증](evidence/replay.json) | 실제 셸 재생에서 새 venv와 wheel SHA를 만들고, 연구자 원장의 관측·오류·입력 지문을 대조했다. 실험 77/77, 교정 8/8 일치. 이번 작업자의 자기 검토이며 독립 타인 검토는 미실시. |

## 결과 SHA에서 실행한 검사

전부 `f475e1a55c5be68cd6d9bcca1a7c7b4f9893e24c`, `2026-11-23T19:57:21Z`부터 `19:57:29Z` 사이, Python 3.12.14에서 수행했다. 검사 전후 working tree는 clean이었다. Pillow child는 별도 Python 3.9.23이다. 결과판에 대한 검사이며 이 인계 커밋은 아래 결과판 검사에 포함되지 않는다.

| 실제 명령·하위 검사 | 종료값과 확인 범위 |
| --- | --- |
| `python -B docs/workstreams/research/AF-RES-097/audit.py` | **0**, 저장 재계산과 일치. stdout SHA-256 `f8f6f193f6be630d273b8b1e1aae1b19ed24151769ae7b61f9a9ee6ebf674b2c`. |
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-097/manifest.json --fetch` | **0**, `passed`, `remote_checked`, `2026-11-23T19:57:24.836165+00:00`. 통합 SHA `01177554d0fbd33a914ea9c982c348d442d1358d`, 의존 현재 SHA `ca82b938e429779d73d9de134ddac93e462ff03d`. 변경 파일 130·허용 밖 0·충돌 0·오류 0. stdout SHA-256 `5cff542d0e0cb1d0c9849a005cd51150598013cdc9ea5a77cb0a862e91bd34ce`. |
| `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | **0**, `passed`. 시작/종료 SHA 모두 결과판. stdout SHA-256 `c5e2643fe716608cb89f6231362c0509dee0b68816ae3271718d66ac8f11ed28`, cloud receipt SHA-256 `5441e0b9c05481b90e9f483c382e252d4be1b4bf206edb17eafdadfa71a2ed9d`. |
| cloud `doctor`, `acceptance`, `research-case`, `original-smoke` | 각 **0**. `acceptance`는 단위 묶음 55·7·9개, 프로젝트 test/demo, export, 해당 SHA의 Git bundle 복원. 공통 검사 라벨은 제품·브라우저 연동 실측을 보증하지 않는다. |
| cloud `python -m workbench.session check-all --fetch` | **0**이지만 `session_validation=not-executed / no_active_sessions`, count 0. `docs/workstreams`의 본 작업 manifest가 공통 단계에서 개별 검사되지 않았으므로 위에서 명시적으로 검사했다. |

세 검사 stderr는 비어 있었다. GitHub에서 결과 SHA의 `RESULT.md`, `reproduce.md`, manifest, SELF_CHECK, 입력·환경, reconciliation, 대표 stdout 5개와 cross-domain 본문을 다시 가져왔다. 13/13 blob SHA가 로컬과 동일했다. RESULT의 세 표 행 수 `2/24/6`과 마지막 3행, 재현 절차의 입력 지문을 본문에서 확인했다. GitHub에서 새 full clone 후 결과 SHA를 확인하고 `audit.py` 종료 0으로 전체 stdout/stderr와 원장 지문을 검산했다. 이 readback의 stdout SHA는 위 로컬 audit와 동일했다.

| GitHub에서 다시 연 항목 | 고정 결과판 blob |
| --- | --- |
| RESULT, 재현 절차, SELF_CHECK | `83f489f91ce7653128fa8c4dc857051c42dd1d29`, `9e2eaf9d791f3f2dcfe1e24d3627c010dead1b90`, `6130922b93b5839b597cba7599d7c73ce680087f` |
| manifest, 입력, 환경, 분모 | `b5ebfd03cb015e8d9ae6238d71a3010184d9e3cf`, `6150f03fdb799014b806330937ddf2c28436b85f`, `89a244885dbeb029396726b17833cca433aa0c89`, `db8d9f180d05c7c3953a5ecb3121ae5039952122` |
| #5593 8.3.1 default-1/rgba-2, #5595 8.2.0 object-1/8.3.0 raw-2, #5593 8.3.0 재승격, 타 분야 | `44fadab70bc0db2fbeb1dc8e5410b830409d1f09`, `0142fa757b53aaf582dced2de622061961f03a8b`, `2e3ad77e8371428c498aa2efd7532d378784ea13`, `b96caa573a0d718a7580430fc32d157331f00125`, `c8ba45c011b50c748d7e9aaad13ea2b8aae937ff`, `175d02653edb4eb30f738b9966db0ea829679a6a` |

## 미실시 확인과 필요한 입력

- **이슈 최초 본문·과거 댓글.** `gh api graphql`의 공개 이슈 revision 요청은 종료 1, `Forbidden`. [이력과 시각](evidence/issue-history.md)에 남겼다. 접근 가능한 GitHub API에서 아래 query를 실행하고 `lastEditedAt`, `totalCount`, `diff`를 현재 본문과 대조한다. 타임라인의 제목 수정과 글 수정은 서로 다른 사건이다.

```sh
gh api graphql -f query='query { repository(owner:"python-pillow",name:"Pillow") { a:issue(number:5593) { number lastEditedAt includesCreatedEdit userContentEdits(first:20) { totalCount nodes { editedAt diff } } } b:issue(number:5595) { number lastEditedAt includesCreatedEdit userContentEdits(first:20) { totalCount nodes { editedAt diff } } comments(first:10) { nodes { databaseId lastEditedAt userContentEdits(first:20) { totalCount nodes { editedAt diff } } } } } } }'
```

- **당시 Python/OS와 화면.** #5593의 Ubuntu 18.04/Python 3.7에서 원 Gist ZIP을 풀고 `python3.7 -m pip install Pillow==8.3.1 pytest==6.2.4`, `python3.7 -m pytest -q test_convert.py`로 원 assertion을 재현한다. 같은 원 input SHA에서 `convert()`와 `convert('RGBA')`를 별도 프로세스에 주고 `(29,24)`, `(0,0)`, `(75,53)`을 읽는다. 8.3.0과 대조 시 별도 venv에서 `Pillow==8.3.0`으로 고정하며 original requirements의 8.3.1 핀과 구별한다. 현재 `run.py`의 CPython 3.9+ 경로 검사는 실험 환경 재현용이다. #5595의 Arch/Python3.9에서 두 P 호출과 필요 시 `Image.show()`를 별도로 비교한다. 현재 화면 근거는 외부 뷰어 대신 RGB 픽셀이다.
- **타 분야 원 스위트.** [Arrow의 GoogleTest filter와 GDAL pytest, 정확한 입력](evidence/cross-domain.md)을 고정판 빌드에서 실행한다. Go 1.23.2에서 `go test image/png -run 'TestDecodePalettedWithTransparency|TestMultipletRNSChunks|TestWriterPaletted'`. libpng v1.6.44에서 `cmake -S . -B build`, `cmake --build build`, `ctest --test-dir build -R pngvalid --output-on-failure`. 이들은 이번 소스 해석과 독립된 추가 실행이다.

| 가장 중요한 불일치·약점 | 다음에 열 자료 또는 실행할 입력 | 어떤 관측이면 결론을 바꿀지 |
| --- | --- | --- |
| #5593 원본은 단일 투명 인덱스 분기다. 8.3.x 기본 RGB→RGBA의 투명 199개 증가는 이미 실측했다. | `pil123p.png`와 `tRNS=[0,128]`의 동일 P 입력을 각각 새로 열어 본판·보조판의 alpha를 비교. [원 상류 시험](https://github.com/python-pillow/Pillow/blob/51591a80a4e14543ea8cbe93026db5e79354b8c4/Tests/test_file_png.py#L220-L228) | 또 다른 입력에서 기본만 부분 alpha를 보존하거나 명시 경로가 잃으면 그 입력군의 링크 선택을 다시 결정. |
| #5595 새 객체의 두 경로 일치는 특정 p·RGB·8.3.0/1이다. 8.2.0 dirty는 raw도 바꾼다. | 같은 p의 dirty·다른 저장 옵션과 `size` 제거 이후의 두 호출을 비교. [size 변경 기록](https://github.com/python-pillow/Pillow/blob/40e7ff622669550733b26f14dc817fb72e096250/docs/releasenotes/8.4.0.rst) | 한 경로가 배열·RGB·번호를 잃거나 입력을 거절할 때 그 조작의 대체 가능 안내를 해제. |
| 당시 환경·최초 본문 전 이력, Arrow·GDAL 번호 선택 실측에 공백이 있다. | GitHub `userContentEdits`, Ubuntu/Python3.7 실제 wheel, 고정 Arrow/GDAL의 번호 선택 실험. [이력](evidence/issue-history.md) [방법](evidence/cross-domain.md) | 다른 원 요구나 반대 환경 출력이 나오면 사용자판 안내를 수정. 타 분야 마스크가 계산과 다르면 전이 범위를 수정. |
