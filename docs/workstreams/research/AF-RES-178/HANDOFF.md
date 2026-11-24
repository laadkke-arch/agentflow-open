# HANDOFF — AF-RES-178
status: PARTIAL
result_commit: 3e56429384a418279b291621e48799b54a638b67
branch: work/research-af-res-178
owned_path: docs/workstreams/research/AF-RES-178/
base: 6fa67328360b02bc7e7270d4ad3300bfe0f286bd
plan_base: 128f673685ec804c526a38e3f89d4d8a43fcd299
dependency: AF-RES-169 @ 74925efaf7bd95177273bcdc01cd18cbf1b18057 (중앙 DONE/작업자 PARTIAL)
review: SELF_CHECK only; independent review not performed

## 판정 범위
- 세 지명 소비자/네 티켓 자리를 모두 추적. 정확 same-call 전후 패치 3소비자(그중 Yellowbrick은 open proposal, Elpy는 fork); 실제 upstream 교체 병합 확인은 scikit-learn-extra #167 한 곳. Elpy #1938은 warning 억제, #2051은 setuptools 의존성으로 실제 병합; 두 사건은 별개이고 옛 비교 호출 유지. Yellowbrick #1323은 제안, 이전 #1319와 직접 인과 연결 미확인.
- 47 ledger/frame rows, 42 직접 열람, 35 고유 산입(규약 5, 사건 16, 파일 7, 배포 3, 타 분야 4). 접근 실패 5(고정 packaging 문서 2, tags 3), opened-but-excluded 3, 같은 저작 추가 판 4. 사건 lineage 7; 보강 paired 실제 당사자 보고 2계보(MNE 및 Manjaro); named 동일 값/환경 판정쌍 0 확인(미확인이지 없음 아님). first post-change tag 3소비자 모두 미확인(미병합 포함). values 28, calls 11, advice 5.
- 단일 링크 권고: PEP440 보장뿐 아니라 **표준 순서 의도**가 명시된 경우 Version. 좁은 안정판 최소 gate 동일 결과는 원문 값 기반 규칙 추론. 반례: 유효 dev 판정 회귀 및 비규격 Manjaro parse 순서 차이, 최신 strict 거부 추론. 기존 정책 보존은 operation별 조건부. 역사 source, 호환 후보 looseversion, domain comparator, gate 정책, obsolete 분기 삭제를 대안으로 남김. PEP632 전체 대체표/언어 코드 재모집/제품 DB 결정 없음.
- 필수 산출물 RESULT.md(3 선두 표+정확히 3 약점 마지막 표), SELF_CHECK.md, SCOPE.md, frame.csv, sources.jsonl, calls.csv, values.csv, advice.csv; 보조 OBSERVATIONS.md, COUNTEREXAMPLES.md. ⑤ SHA에서 재열람: 47 unique source IDs, 근거 ID 누락 0, category 수 재확인, 5 commits ahead / 0 behind, 모든 10개 변경 owned_path. 독립 검토/실행은 미실시.
- 통합 dot-control 전체 본문은 GitHub 도구의 oversized 반환/400으로 읽지 못함. 최신 commit diff에서 대상 RUNNING, attempt 1, depends_on 및 경로 확인하고 사용자 지정 dependency HANDOFF로 한정; 다른 작업 결과를 기다리지 않음. dot-control 변경 금지 유지.

## 재개 첫 행동
Codex Cloud에서 먼저 원 소비자 저장소의 exact SHA ancestry와 tags를 확인. #167이 실제 포함된 첫 scikit-learn-extra 배포 tag/파일을 찾고, Yellowbrick #1323의 직접 연결 변경과 Elpy fork의 upstream 포함 여부를 확인할 것. 없다고 가정하거나 임의로 첫 태그를 채우지 말 것. 다음으로 named 소비자 raw version pair와 실제 old/new branch 결과를 로그에서 추적(특히 Elpy installed + PyPI latest와 동일 RPC 환경; Yellowbrick mpl raw value; scikit CI installed logs). 아래 재현으로 inference를 실측과 분리하며 조건부 권고 갱신.

## Codex Cloud 실행 명령/입력 (이 작업에서 실행하지 않음)
공개 읽기 전용 원본 clone 및 별도 임시 venv. 저장소 밖 경로에 clone/install, owned_path 이외 변경 금지. 네트워크/공개 git 접근과 Python 3.11, 3.12 사용 가능 여부 선행 확인. 명령 실패와 stdout/stderr, Python/packaging/setuptools/looseversion 정확판 기록. 외부 dependency 설치는 Codex의 환경 허가와 공개 패키지 검증 아래에서만.
```sh
git clone https://github.com/scikit-learn-contrib/scikit-learn-extra.git /tmp/af178-sk
git clone https://github.com/DistrictDataLabs/yellowbrick.git /tmp/af178-yb
git clone https://github.com/jorgenschaefer/elpy.git /tmp/af178-el
git -C /tmp/af178-sk show --stat 0f95d8dda4c69f9de4fb002366041adcb1302f3b
git -C /tmp/af178-sk tag --contains 0f95d8dda4c69f9de4fb002366041adcb1302f3b --sort=creatordate
git -C /tmp/af178-yb tag --contains 5e493f212aca0efc845c63dadc4736c0bfcfa96f --sort=creatordate
git -C /tmp/af178-el tag --contains bcfd5e8c25e5efbcb26cfcf389f1bf01c2e2f44f --sort=creatordate
git -C /tmp/af178-el tag --contains 213a26a5af3de7a3474e9188f6d07e8e75195841 --sort=creatordate
git -C /tmp/af178-el tag --contains 208e5f09f61aa998cc6d9b61965cbec67e9134d2 --sort=creatordate
# fork SHA 미포함이면 원 PR/commit ref를 공개적으로 fetch할 수 있는지 확인 후 재시도; tag 결과 빈 값과 SHA 접근 실패는 구분.
# 후보 태그마다 git show TAG:FILE 및 release / wheel metadata / 실제 수정 포함 diff 대조.
git -C /tmp/af178-sk diff 627f97b011cb267828e89cdf9257e35f59b328e7 0f95d8dda4c69f9de4fb002366041adcb1302f3b -- conftest.py sklearn_extra/cluster/_commonnn.py setup.py
git -C /tmp/af178-yb diff f7a8e950bd31452ea2f5d402a1c5d519cd163fd5 5e493f212aca0efc845c63dadc4736c0bfcfa96f -- yellowbrick/style/colors.py yellowbrick/style/rcmod.py
git -C /tmp/af178-el diff d3d208551e4f4d9e0d7b4d5abb7d3218060a4a06 213a26a5af3de7a3474e9188f6d07e8e75195841 -- elpy.el
python3.11 -m venv /tmp/af178-p21
python3.11 -m venv /tmp/af178-p23
/tmp/af178-p21/bin/python -m pip install packaging==21.3
/tmp/af178-p23/bin/python -m pip install packaging==23.0
# looseversion: PyPI release/version/hash 확인 후 정확판 고정하여 별도 venv에 설치; 최신값을 추정하지 말 것.
# old stdlib distutils vs setuptools shim 분리: SETUPTOOLS_USE_DISTUTILS=stdlib 환경에서 old __file__ 확인.
```
두 packaging venv에서 다음 고정 입력을 반복. old는 CPython 3.11 stdlib인지 path로 확인하고 shim 결과 별도 기록. 3.12 clean 환경에서 import 실패/설치 후 shim 여부도 별도 기록. 실제 입력은 V01/V04/V05/V06/V07/V15/V16와 S21 test fixtures; actual user pair 없는 Elpy 값은 비교 쌍을 만들지 말고 acceptance만 검사. 예상 관측은 아래 표에 적되 실행 전 확정하지 않음.
```python
import sys, operator, packaging
from packaging.version import Version, parse
try:
    import distutils.version as dv
    old = dv.LooseVersion
    print("old_source", dv.__file__)
except Exception as e:
    old = None
    print("old_import_error", repr(e))
print(sys.version, packaging.__version__)
pairs = [
    ("1.0.dev0", "1.0"),
    ("5.15.12-1-MANJARO", "5.10"),
    ("3.4.1", "1.5.0"),
    ("1.19.4", "1.14"),
    ("1.26.1", "1.14"),
    ("1.23.0.dev0+782.g1168868df6", "1.23"),
    ("1.9.0.dev0+1485.b06254e", "1.9"),
    ("3.6.0.dev1651+g30d6161406", "3.6"),
    ("1.1.dev0", "1.1"),
    ("0.56.0dev0+39.gef1ba4c10", "0.56"),
    ("9.1.0.rc1", "9.1"),
    ("0.3dev0", "0.3"),
    ("0.2.2.dev0", "0.2.2"),
    ("3.2.2+150.g1e93bd5d", "3.2.2"),
    ("1.2.3", "1.2.3"), ("1.2", "1.2"), ("1", "1")
]
constructors = [("Version", Version), ("parse", parse)]
if old is not None:
    constructors.append(("old", old))
try:
    from looseversion import LooseVersion as compat
    constructors.append(("compat", compat))
except ImportError:
    pass
for name, ctor in constructors:
    for a,b in pairs:
        for op in (operator.lt, operator.ge, operator.eq, operator.le):
            try:
                print(name, a, b, op.__name__, op(ctor(a),ctor(b)))
            except Exception as e:
                print(name,a,b,op.__name__,type(e).__name__,str(e))
    for v in ("3.4j","3.2.pl0","21.9b0","0.18.0","1.5.7","0.31.0"):
        try:
            print("accept",name,v,repr(ctor(v)))
        except Exception as e:
            print("reject",name,v,type(e).__name__,str(e))
```
Expected (규칙 및 기존 보고, 새 실측 아님): 1.0.dev0 >=1.0 old True/strict False; Manjaro <5.10 old False/21.3 parse True/23.0 reject; 3.4.1>=1.5.0 양쪽 True; 1.19.4 및 1.26.1 <1.14 양쪽 False; MNE strict/strip fixture는 S21의 고정 test expectations와 대조; compat는 old와 일치하는지 확인(예상만). old token mixed-type TypeError도 그대로 기록. 재현 성공은 과거 사용자 로그/배포를 대체하지 않는다. 실제 consumer test가 필요하면 원판의 dependency/CI 환경 재현 후 최소 gate를 분리 검증.
Repo 검증: `git diff --check 6fa67328360b02bc7e7270d4ad3300bfe0f286bd..HEAD`, `git diff --name-only 6fa67328360b02bc7e7270d4ad3300bfe0f286bd..HEAD`, 허용 경로만 확인. `python scripts/cloud_check.py --environment codex-cloud --fetch-contract`은 해당 통합판에서 존재/계약 확인 후 실행. 본 작업은 GitHub 비교/재열람만 시행.

## 커밋 순서
① c7dae88863c9513b9c00cacc0ec9e988c3db812d
② a355bfd8a047e4fcb452dbc1a00ffca77c6c2995
③ ea5d8da22ef1faa55427d242485139337955b313
④ 309c62406fd0c179874c889a655df29d62cfe726
⑤ 3e56429384a418279b291621e48799b54a638b67 (result, 보정 포함)
⑥ 이 HANDOFF 커밋이 branch head. 자기 SHA는 본문에 넣지 않음.

색인 제안: AF-RES-178 PARTIAL — LooseVersion 후계는 입력 도메인+연산+오류/정렬 정책으로 분기; 35 원자료, 3 named exact patch(1 실제 merged), 2 보강 반례 계보, 배포/실행 연결 미확인; RESULT.md 및 values.csv.
