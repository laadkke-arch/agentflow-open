# AF-RES-194 자체점검 — PARTIAL

자체 검토자: 이 작업의 작성자(동일 세션). 독립 검토자: 미배정·미실행. Python 역사 실행 및 새 벤치마크는 하지 않았다. 고정 자체점검 입력: `181b4457f591748616ad4d9f38ee04ed5d833ca2`의 SCOPE, frame, sources, timeline, alternatives, cards, RESULT를 GitHub에서 재열람했다. 후속 자료는 별도 검토 대상이다.

## Q별 검산

| 질문 | 답과 원문 ID·URL | 반증·경쟁 설명 확인 | 판정·남은 미충족 |
|---|---|---|---|
| Q1 | 네 초기판 D01 [3142](https://github.com/python/peps/blob/d5afafae8c9305533c1d3e63084e955b7b1cddaa/pep-3142.txt), D02 [559](https://github.com/python/peps/blob/e8439f8b8080dc3463d4a7631202d38c708109df/pep-0559.rst), D03 [616](https://github.com/python/peps/blob/914ef2c51a6ae6e07b930675994a172e42fc580e/pep-0616.rst), D04 [618](https://github.com/python/peps/commit/11b2de41a7eeb64897494a781274099afcee1102), M06 [Ram](https://mail.python.org/archives/list/python-ideas@python.org/message/6GFUADSQ5JTF7W7OGWF7XF2NH2XUTUQM/): 첫 거짓 종료, 아무 인자 noop, 정확한 affix 제거, lazy 길이 불일치 오류를 각각 원문에서 특정 | 3142의 일반 if는 계속 필터링; 559의 breakpoint는 범용 계약과 다름; 616 strip은 집합 제거; 618 일부 zip은 의도적으로 truncate | 핵심 요구 4/4 확보. 3142 가장 이른 메일, 559 breakpoint 당시 553 정확 판본 미확인. |
| Q2 | A01 [3.0 takewhile](https://github.com/python/cpython/blob/v3.0/Doc/library/itertools.rst#L419-L430), A02 [3.6.2 def](https://github.com/python/cpython/blob/v3.6.2/Doc/reference/compound_stmts.rst#L561-L581), A03 [3.8.2 str](https://github.com/python/cpython/blob/v3.8.2/Doc/library/stdtypes.rst), A04 [cookiejar](https://github.com/python/cpython/blob/v3.8.2/Lib/http/cookiejar.py#L452-L457), A05 [zip_longest](https://github.com/python/cpython/blob/v3.8.2/Doc/library/itertools.rst#L61), A06 [zip](https://github.com/python/cpython/blob/v3.8.2/Doc/library/functions.rst#L1717-L1738), A07 [Mock](https://github.com/python/cpython/blob/v3.6.2/Doc/library/unittest.mock.rst#L204) | A08 [v8.2.0](https://github.com/more-itertools/more-itertools/blob/v8.2.0/more_itertools/more.py) vs A09 [v8.3.0](https://github.com/more-itertools/more-itertools/blob/v8.3.0/more_itertools/more.py), I07 [2020-05-16 release](https://pypi.org/project/more-itertools/8.3.0/): 정식 배포가 최초 제안 뒤임. 당시 도구와 결정 전 새 후보를 혼동 금지. | 4/4 당시 대안, 7개 최초 공개 이전 원문; 비교판 2개. zip_equal 최초 개발 커밋 SHA, 실제 플랫폼 설치·환경·출시 동작 미확인. |
| Q3 | D01–04의 저자 자신의 대안 명시; M04 [559 후속](https://mail.python.org/archives/list/python-dev@python.org/thread/P2ICFUYMJWK2OVUOUB2D3DMDATNM2JI5T/), M05 [616 post](https://mail.python.org/archives/list/python-dev@python.org/thread/XC3D3QGONENQ7PIAUM2SNNEP5BWA6Q4J/), M09 [616 issue](https://github.com/python/cpython/issues/84120#issuecomment-1093865558), M11 [2019 선행 thread](https://mail.python.org/archives/list/python-ideas@python.org/thread/RJARZSUKCXRJIP42Z2YBBAEN5XA7KEC3/), M10 [618 issue](https://github.com/python/cpython/issues/84533#issuecomment-1093869638), M07 [618 토론](https://mail.python.org/archives/list/python-dev@python.org/thread/6HTDN4L5PFMOYMUXLTZCGGJYDYMHJGHC/) | M03 [Michel 후속](https://mail.python.org/pipermail/python-dev/2017-September/149441.html)은 559 기각 뒤. M11의 선행 발언자는 616 저자와 동일 인물이 아님. M10에서 저자가 후보를 논의했다고 처음 알았다는 뜻 아님. | 559/616/618에서 초안→후속 반응 순서 확보; 3142 저자 후속 직접 회신 미확보. 모든 최초 인지일 미확인; 0건의 명시 미인지→변경→시행을 발견했지만 부재 일반화 금지. |
| Q4 | A01–09, M11, M12 [SC 검토/발언](https://github.com/python/steering-council/issues/23), I11 [2017 반대와 재평가](https://mail.python.org/pipermail/python-ideas/2017-August/046653.html), I12 [2013 후대 논의](https://mail.python.org/pipermail/python-ideas/2013-June/021585.html) | takewhile 실패 원소 소비; Mock 호출 기록; 빈 접미사 slicing 함정; strip과 affix; zip_equal Sized 즉시 검사 vs strict lazy, zip_longest sentinel의 추가 읽기; 616 적용 곤란 사례와 표준화 옹호 모두 검토. | 기능 충족·부분·충돌 구분, 최소 각 1 이상. 실제 runtime test 없음. 616 ns 비교는 저자 보고, 3142 기각 당시 이유로 후대 설명을 귀속하지 않음. |
| Q5 | M01 [3142 결정](https://mail.python.org/pipermail/python-dev/2013-May/126136.html), M02 [559 결정](https://mail.python.org/pipermail/python-dev/2017-September/149438.html), M12 [616 SC 통지](https://github.com/python/steering-council/issues/23#issuecomment-616731352), M08 [618 결정](https://mail.python.org/archives/list/python-dev@python.org/message/NLWB7FVJGMBBMCF4P3ZKUIE53JPDOWJ3/), I01 [559 PR](https://github.com/python/cpython/pull/3480), I02 [616 PR](https://github.com/python/cpython/pull/18939), I03 [618 PR](https://github.com/python/cpython/pull/20921), I04 [3.9.0 문서](https://github.com/python/cpython/blob/v3.9.0/Doc/whatsnew/3.9.rst#L167-L174), I08 [3.10.0 문서](https://github.com/python/cpython/blob/v3.10.0/Doc/library/functions.rst#L1825-L1904), I09 [3.10 일정](https://peps.python.org/pep-0619/), I10 [3.9 일정](https://peps.python.org/pep-0596/) | 3142 공식 기각 메일에 takewhile을 이유로 명시한 문장 없음; 559 구현 PR 미병합; 616/618 기존 대안 알고도 채택. D07–09 상태 편집은 실제 결정/병합/출시와 분리. | 네 최종 결정 원문 및 두 채택의 구현·릴리스 확보. 3142 구체적 기각 이유, 616 SC 내부 표결 및 별도 메일 미확인. 기각의 경쟁 설명은 약한 근거로만 남김. |
| Q6 | X01 [Nicollet-Central 대안분석](https://metc2new.metctest.state.mn.us/Council-Meetings/Committees/Transportation-Committee/2013/August-12%2C-2013/Nicollet-Central-AA-Newsletter.aspx), X02 [결의 2013R-422](https://metrocouncil.org/Council-Meetings/Committees/Transportation-Advisory-Board-TAB/TAB-Technical-Advisory-Committee/TAC-Planning-Committee/TransitwayAdvCmte/TAC-Planning-Committee-11-14-13/2013-48-AT-TPP-Modification-for-Streetcars.aspx) | X03 [Newport proposal](https://newportbeach.legistar.com/View.ashx?GUID=4828EC07-D582-4E45-9727-BA5993340F4E&ID=1364783&M=PA), X04 [minutes](https://newportbeach.legistar.com/View.ashx?GUID=94A71A3D-943E-4D0B-BAD7-AE6FA00631F5&ID=1385098&M=PA): 기존 program 유지+신규 branding이지만 정확한 자료 재사용/신규 제작 비교 표결은 아님. 받은 보고는 채택으로 간주하지 않음. | 교통 1 사건/2 원문; 도서관 적격 0/2 원문, 2개 부족. PDF screenshot 도서관 원문 2건은 요청했으나 410/렌더 접근 실패로 본문 텍스트만 확인; 시각 검증 없음. |
| Q7 | cards.csv 12행; C01–03 A01/A02/D01/D02, C04 [I06](https://peps.python.org/pep-0553/) 보류, C05–06 [A03](https://github.com/python/cpython/blob/v3.8.2/Doc/library/stdtypes.rst)/A04, C07–10 [A05](https://github.com/python/cpython/blob/v3.8.2/Doc/library/itertools.rst#L61)/A06/A09/I07, C11 X01, C12 X03–04 보류 | C02의 원문 URL은 첫 보존 01-18, 이전 헤더 01-12 당시 URL 접근 미확인: 자체점검에서 컷오프 01-18로 수정(이전 01-12). C09 05-16 이후만 배포판 카드. 기본 zip을 전부 strict로 바꾸는 오류 방지. | 세 카드 분류 모두 제안. 과거 결정과 당시 기술 충족 분리, 후대 정보와 비용 미확인 표기. 새 인터페이스 권고와 실제 재사용 채택·절감 인과 미확인. |

## 분모와 파일 자체 검산

고정 SHA에서 파싱 결과: sources.jsonl 51행(고유 source_id 51), 산입 39행/서로 다른 URL 39개, 산입 lineage_id 37개(전체 행의 lineage 39개). A08/A09/I07은 같은 more-itertools 계보 3 자료. D01–09는 PEP 동일 계보의 판·편집 9행, X03–04 근접 대조 2행, Z01 보조 1행: 미산입 12행. 검색 미리보기·접근 실패 및 같은 원문 재게재는 산입하지 않음. '독립 원자료'의 문서 단위와 계보 단위가 다르며 사건 단위는 Python 고정 4 + 적격 교통 1 = 5, 도서관 근접 1은 별도. 근접/후대 발언 자체의 다양성을 신규 Python 의사결정 사건으로 늘리지 않았다.

| 구분 | 목표 | 실제 산입 | 부족 |
|---|---:|---:|---:|
| PEP | 4 | 4 | 0 |
| 별도 최초·토론·결정 메시지 | 6 | 12 | 0 |
| 당시판 대안 | 5 | 9 (최초 제안 전 7, 결정 전 비교판 2) | 0 |
| 구현·배포·유지자 반대 | 5 | 12 | 0 |
| 교통·도서관 | 4 | 2 | 2 |
| 합계 | 24 | 39 | 종류별 2 |

frame.csv 61행, 산입 39행이 sources 산입 ID와 정확 일치; timeline.csv 41행; alternatives.csv 16행; cards.csv 12행. CSV 모든 행의 필드 수 일치, CSV source_id/source_ids 참조 미해결 0, JSONL 파싱 오류 0. RESULT 첫 세 표 헤더 원문 지시와 정확 일치, 마지막 표 헤더 일치 및 데이터 3행. 직접 외부 링크 접근 여부는 원장에 기록한 열람 당시 결과이며 이 자체검산은 GitHub에 저장된 근거 주소·내용을 다시 읽은 것(외부 전 링크 재접속 테스트와 구별). 자료 보정: 3142 저자 표기 초기 오기 Michael Foord → Gerald Britton, SCOPE에 기록; C02 컷오프 변경 01-12 → 01-18 및 의사코드 문구 보정은 181b445 commit에서 실시. 

## Codex Cloud 후속 실행 명세 (이 세션 실행 안 함)

고정 입력: CPython v3.0/v3.6.2/v3.8.2/v3.9.0/v3.10.0 태그, more-itertools v8.2.0/v8.3.0 태그. 환경: 격리된 Linux x86-64 컨테이너/VM, C compiler, make; Python 3.0 등 구버전은 현재 OS에서 빌드 실패 가능, 성공한 빌드만 비교하고 실패 원문 및 compiler/OS 버전을 기록. Windows 저자 benchmark와 동일 환경이 아님. 인터넷/설치 허용 및 실행 환경 확인 후, 다음 명령을 다른 실행 세션에서 수행; 결과는 이 owned_path에만 보존할 것.

```sh
git clone https://github.com/python/cpython.git /tmp/af194-cpython
for t in v3.0 v3.6.2 v3.8.2 v3.9.0 v3.10.0; do
  git -C /tmp/af194-cpython worktree add --detach /tmp/af194-$t $t
  (cd /tmp/af194-$t && git rev-parse HEAD && ./configure && make -j2 && ./python -V) > /tmp/af194-$t-build.log 2>&1
done
git clone https://github.com/more-itertools/more-itertools.git /tmp/af194-mi
git -C /tmp/af194-mi log --all --date=iso-strict --format='%H %ad %cd %s' -S 'def zip_equal' -- more_itertools/more.py
git -C /tmp/af194-mi worktree add --detach /tmp/af194-mi82 v8.2.0
git -C /tmp/af194-mi worktree add --detach /tmp/af194-mi83 v8.3.0
```

각 버전에서 다음 fixture를 /tmp/af194-observe.py로 저장하여 실행(소스 판독이 아닌 실제 실행 로그의 예외 종류/발생 단계/읽은 원소를 비교). 비교 대상은 문서의 역사상 코드 그대로가 아니라 명시한 대조용 작은 구현이며, 표준 zip 및 more-itertools는 고정된 실제 구현. stdout/stderr와 commit SHA, 종료 상태를 함께 보존.

```python
from itertools import takewhile, zip_longest
import sys
print("version", sys.version)
print("takewhile", list(takewhile(bool, [1, 0, 2])))
print("filter", [n for n in [1, 0, 2] if n])
def noop(*args, **kwargs):
    return None
print("noop", noop(1, a=2))
def suffix(s, x):
    return s[:-len(x)] if x and s.endswith(x) else s
for s, x in [("abc", ""), ("foofoo", "foo"), ("abc", "z")]:
    print("suffix", repr(s), repr(x), repr(suffix(s, x)), repr(s.rstrip(x)))
    if hasattr(s, "removesuffix"):
        print("native", repr(s.removesuffix(x)))
if hasattr("x", "removeprefix"):
    print("prefix", "foofooBar".removeprefix("foo"), "foofooBar".lstrip("foo"))
    class Sub(str):
        pass
    a = bytearray(b"abc")
    print("copy", a.removeprefix(b"z") is a, type(Sub("abc").removeprefix("z")))
def guard_zip(*args):
    marker = object()
    for row in zip_longest(*args, fillvalue=marker):
        if any(v is marker for v in row):
            raise ValueError("length mismatch")
        yield row
def logged(xs, tag, log):
    for x in xs:
        log.append((tag, x))
        yield x
def observe(name, maker, values, wrap, stop=False):
    log = []
    args = [logged(v, i, log) for i, v in enumerate(values)] if wrap else values
    stage = "call"
    try:
        it = maker(*args)
        stage = "next"
        while True:
            print(name, "yield", next(it), log[:])
            if stop:
                print(name, "early stop", log[:])
                break
    except Exception as e:
        print(name, stage, type(e).__name__, str(e), log[:])
makers = [("zip", zip), ("sentinel", guard_zip)]
if sys.version_info >= (3, 10):
    makers.append(("strict", lambda *a: zip(*a, strict=True)))
try:
    from more_itertools import zip_equal
    makers.append(("zip_equal", zip_equal))
except ImportError as e:
    print("zip_equal unavailable", str(e))
for name, maker in makers:
    for v in [([1], [10,20], [100,200]), ([1,2], [10], [100,200]), ([1],[10]), ([None],[10,20])]:
        for wrap in (False, True):
            for stop in (False, True):
                observe(name, maker, v, wrap, stop)
```

```sh
for t in v3.0 v3.6.2 v3.8.2 v3.9.0 v3.10.0; do
  /tmp/af194-$t/python /tmp/af194-observe.py > /tmp/af194-$t-observe.log 2>&1
done
for m in 82 83; do
  PYTHONPATH=/tmp/af194-mi$m /tmp/af194-v3.8.2/python /tmp/af194-observe.py > /tmp/af194-mi$m-observe.log 2>&1
done
```

기대 관측(검증 전 가설): takewhile [1] / filter [1,2]; noop None; 빈 suffix 원본 유지; 한 번 제거와 집합 제거 차이; bytearray copy와 subclass 반환 타입; zip_equal Sized는 call에서 오류, strict는 next 단계에서 오류, sentinel wrapper와 strict의 iterator 소비 로그 차이; 조기 중단 시 나머지 불일치 미검출. 결과가 다르면 구현 및 환경 확인 후 원장·판정을 보정. 616 pyperf 비교는 M12의 한 입력 'foobar'/'bar'만으로 일반화하지 않고, 후속 필요 시 별도 반복 수·환경·분산 기록. 559 breakpoint 검증은 v3.7.0 추가 빌드 후 PYTHONBREAKPOINT=0 및 빈 값에서 pdb.set_trace를 mock으로 바꿔 비대화식 실행(실제 디버거 대기 금지), override 여부도 테스트. 별도 실행할 618 AST malformed dict fixture는 v3.8.2와 v3.10.0에서 ast.literal_eval(ast.Dict(keys=[ast.Constant(value="XXX")], values=[]))의 실제 반환/예외를 기록하되 다른 변경의 영향 배제 금지. 역사적 근거와 현재 재실행 구분.

## 완료 판단

네 PEP의 대안·결정, 둘 이상 시간 순서, 충분·부분 사례, 12개 카드 확보. 그러나 도서관 적격 원자료 2개 부족 및 3142 결정 이유·저자 직접 회신, 618 정확한 최초 개발판·당시 적용 비용 미확인. 종류별 하한과 일부 핵심 조건 미달로 PARTIAL. 원자료 수를 채우기 위해 근접 사례를 포함하거나 후대 발언을 당시 직접 증거로 변환하지 않는다. 
