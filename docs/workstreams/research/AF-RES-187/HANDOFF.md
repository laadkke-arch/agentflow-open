# AF-RES-187 HANDOFF — PARTIAL

- 결과 고정 SHA(⑤, 이 인계 직전): 1c1ebcecc3b2d0e5881818e5b619b67a42d44452
- 브랜치 work/research-af-res-187; base 72cf39aea54e2de2ba78a245593aefdc40205a16; owned_path docs/workstreams/research/AF-RES-187/. 계획 기준 0f6765df46ad2128c7fdfa92c3bf917bbfe0c5e6. 의존 AF-RES-178 bbdf4dd15393062e59c16a9d46b38d8255c672f3 읽음. 다른 작업 대기 없음. dot-control 미변경.
- 대표: [RESULT.md](RESULT.md), [sources.jsonl](sources.jsonl), [calls.csv](calls.csv), [behaviors.csv](behaviors.csv), [advice.csv](advice.csv), [SELF_CHECK.md](SELF_CHECK.md). [OBSERVATIONS.md](OBSERVATIONS.md) exact parent/merge/tag; [COUNTEREXAMPLES.md](COUNTEREXAMPLES.md) 반증 및 분야 대조; [SCOPE.md](SCOPE.md), [frame.csv](frame.csv) 모집/경계.
- 자료 32 고유 (NumPy5, 당사자5, 고정 호출/시험10, 배포8, 분야4; 모든 최저치 부족 0). frame 52, duplicate 7, failed 10, unread 2, excluded 1; 10 고유 lineage ID; 2 downstream change lineages, 3 PR, 실제 1 최초 제보자의 두 caller 입구, 별도 후속 제보자 1명(동일 call 미확인), Astropy 설계 이슈 1(실제 입력 없음). 실제 동작 새 실행 0. 독립 검토 없음.
- 달성: Datasets 2.20.0 old formatting blob과 2.21.0 new blob 직접 확인; Astropy v6.0.1 shim/old helper와 v6.1.0 helper+shim removal 파일 직접 확인; 두 프로젝트 tag 확인 2/2. NumPy copy-if-needed와 strict false의 조건부 권고, Astropy의 unit conversion/astype 반례 확보. NARA/LOC 및 Linux/Microsoft 분야 대조.
- 미충족: HF 제보자의 정확 datasets/NumPy/Arrow 판, dtype/schema/값/실제 재시험 미확인; Astropy 원제보의 실제 입력/traceback 없고 정책 토론과 fixture로 대체(원요구→실제 객체 연결 1/2 부분, 0/2 완전 연결). 양 프로젝트 wheel/sdist 내용 직접 검증 0/2, 설치/동일 입력 재시험 0/2, 직접 mutation 실측 0. 최초 태그 전수 미확인. HF direct follow-up 0 특정; MTEB #938 원문 미열람; 동일 오류의 12월 fasttext report는 별도. 주어진 최소 자료 수를 채웠어도 이 빈 고리로 PARTIAL. 새 실행/빌드/검사는 Codex에 인계.
- 자기점검: ⑤ 고정 SHA에서 10개 파일 모두 GitHub fetch로 재열람(52 ledger/frame rows, IDs unique52, 참조 ID 누락0, call8/behavior18/advice3, last weakness rows3); base→⑤ compare ahead5 behind0, 10개 변경 파일 모두 owned_path. 이것은 구조/원장 연결 검사이지 실제 Python/CI 테스트나 독립 검토가 아님.

## 첫 재개 행동 및 Codex Cloud 실행 계획 (미실행)

1. 먼저 H01이 직접 지목한 https://github.com/embeddings-benchmark/mteb/pull/938 의 실제 stack 및 환경을 읽어 H02와 같은 caller인지 확인; forum 93584에서 최초 이용자의 exact version, Arrow dtype/input, 후속 설치·재시험 찾아보기. 실제 기록 없으면 미확인 유지. Astropy #16167/#16181에서 실제 실패 입력·CI 로그 공개 여부 확인. 동시 작업의 결과를 기다리지 않는다.
2. 아래는 Codex Cloud에 넘길 재현 명령. 공개 자료만, 임시 디렉터리 사용; 연구 repo에서는 owned_path 안 결과만 커밋. 환경 예 Python 3.11 (H02 보고는 3.12이므로 3.12 추가 재현), Linux x86_64, pip resolver와 실행판 기록. 의존성 설치 불가/ABI 문제는 별도 결과로 기록하고 우회하거나 성공 추정 금지. 아래 fixture는 원 보고자의 실제 데이터가 아님을 명시.

```sh
git clone https://github.com/huggingface/datasets.git /tmp/af187-datasets
git clone https://github.com/astropy/astropy.git /tmp/af187-astropy
git -C /tmp/af187-datasets tag --contains 84d9dea52098c9403efb43d5b542dd6d45000bec
git -C /tmp/af187-astropy tag --contains 35d18ce8bd682a36e30a8f7ee86a8d5fac89e2bf
git -C /tmp/af187-datasets diff e47a746bcda4b97db2467542b76d3215b3569ff0 84d9dea52098c9403efb43d5b542dd6d45000bec -- src/datasets/formatting/formatting.py
git -C /tmp/af187-astropy diff cf68c08c5479020e53a52937f587d27ef3f579c6 35d18ce8bd682a36e30a8f7ee86a8d5fac89e2bf -- astropy/units/quantity.py astropy/utils/compat/numpycompat.py
# PyPI artifact: choose exact compatible wheel, record filename, hash and upload time.
mkdir -p /tmp/af187-wheels
for spec in datasets==2.20.0 datasets==2.21.0 astropy==6.0.1 astropy==6.1.0; do
  python -m pip download --no-deps --only-binary=:all: --dest /tmp/af187-wheels "$spec"
done
sha256sum /tmp/af187-wheels/*
# inspect zipped path datasets/formatting/formatting.py,
# astropy/units/quantity.py, astropy/utils/compat/numpycompat.py; compare exact tag files.
python -m zipfile -l /tmp/af187-wheels/<exact-wheel-filename>
# extract exact wheel to its own temp dir (replace placeholder before running):
python -m zipfile -e /tmp/af187-wheels/<exact-wheel-filename> /tmp/af187-unpacked/<exact-version>
```

Separate environments per combination, not upgrading in place:
```sh
for nv in 1.26.4 2.0.0; do
  for dv in 2.20.0 2.21.0; do
    e="/tmp/af187-hf-$nv-$dv"
    python3.11 -m venv "$e"
    "$e/bin/python" -m pip install "numpy==$nv" "datasets==$dv" "pyarrow==16.1.0"
    "$e/bin/python" -m pip freeze
    "$e/bin/python" /tmp/af187-hf-test.py
  done
  for av in 6.0.1 6.1.0; do
    e="/tmp/af187-a-$nv-$av"
    python3.11 -m venv "$e"
    "$e/bin/python" -m pip install "numpy==$nv" "astropy==$av"
    "$e/bin/python" -m pip freeze
    "$e/bin/python" /tmp/af187-a-test.py
  done
done
```
Do not interpret dependency solver or ABI failure as copy behavior. Save stdout/stderr, package version/installation file location, exact input and output dtype/shape/exception, shares_memory and writeability, actual original values before/after mutation. If import failure, stop that cell, not other independent cells. PyArrow 16.1.0 is a planned pin, not verified original H02 version. Substitute exact tested original versions if recovered.

Save to /tmp/af187-hf-test.py:
```python
import sys, numpy as np, pyarrow as pa, datasets
from datasets.formatting.formatting import NumpyArrowExtractor
print(sys.version, np.__version__, pa.__version__, datasets.__version__)
e = NumpyArrowExtractor()
for chunks in [[pa.array([0,1,2], type=pa.int64())],
               [pa.array([0,1], type=pa.int64()), pa.array([2], type=pa.int64())],
               [pa.array([1,None,3], type=pa.int64())],
               [pa.array(["foo","bar","foobar"])]]:
    col=pa.chunked_array(chunks)
    t=pa.table({"x":col})
    for name, fn in [("column",e.extract_column),("batch",e.extract_batch)]:
        try:
            y=fn(t)
            if isinstance(y,dict): y=y["x"]
            print(name, col.type, y.tolist(), y.dtype, y.shape, y.flags.writeable)
            if col.num_chunks == 1 and col.null_count == 0 and pa.types.is_integer(col.type):
                a=col.chunk(0).to_numpy(zero_copy_only=True)
                print("arrow view",np.shares_memory(a,y),a.flags.writeable)
                if y.flags.writeable:
                    before=a.copy(); y[0]=99
                    print("actual arrow change",a.tolist(),before.tolist())
        except Exception as exc:
            print(name,col.type,type(exc).__name__,str(exc))
```
Expected observation only: list→np.array(copy=False) old 2.x may raise; new 2.x asarray returns values where convertible; shared original Arrow buffer not guaranteed. For nested extension/NaN object branch extend with fixed F03 test fixtures exactly; execute checked-out original formatting tests only if deps and environment are available. No generic synthetic list result counts as user reproduction.

Save to /tmp/af187-a-test.py:
```python
import sys, numpy as np, astropy
import astropy.units as u
print(sys.version, np.__version__, astropy.__version__)
for base in ([1,2], np.arange(10.0), np.arange(3,dtype=np.int64)):
    for flag in (False,None,True):
        try:
            q=u.Quantity(base,u.m/u.s,copy=flag)
            print(type(base).__name__,getattr(base,"dtype",None),flag,q.dtype,q.shape,q.value.tolist())
            if isinstance(base,np.ndarray):
                print("share",np.shares_memory(base,q.value),"write",q.flags.writeable)
        except Exception as e: print(type(base).__name__,flag,type(e).__name__,str(e))
a=np.arange(10.0)
q0=u.Quantity(a,u.m/u.s)
for unit, obj in [(u.m/u.s,a),(u.m/u.s,q0),(u.cm/u.s,q0)]:
    try:
        q=u.Quantity(obj,unit,copy=False)
        raw=obj.value if isinstance(obj,u.Quantity) else obj
        before=raw.copy()
        print("unit",unit,"is",q is obj,"share",np.shares_memory(raw,q.value),"write",q.flags.writeable)
        if q.flags.writeable:
            q.value[0]=99
            print("before",before[0],"after",raw[0],"new",q.value[0])
    except Exception as e: print(type(e).__name__,str(e))
for x in ([1,2],np.arange(3,dtype=np.float32)):
    for dt in (None,np.float64):
        for flag in (False,None,True):
            try:
                y=np.asarray(x,dtype=dt,copy=flag)
                print("np.asarray",type(x).__name__,dt,flag,y.tolist(),y.dtype,
                      np.shares_memory(x,y) if isinstance(x,np.ndarray) else "not ndarray")
            except Exception as e: print("np.asarray",type(x).__name__,dt,flag,type(e).__name__,str(e))
```
1.x asarray(copy=...) expected TypeError because unsupported keyword; additionally run plain np.asarray(x,dtype=dt) and np.array(x,dtype=dt,copy=False) for both versions. For 6.1 Quantity unit change expected new base even with explicit False per F08/F09; check value, sharing, mutation separately. Add same-unit readonly ndarray fixture; no writing to read-only. Test cases are designed to potentially falsify current expectations, not to prove historical reporter's run.

## 커밋/인계
① 51a641f59f0de7af4be8bba288cce140aa15e3f2 범위
② 5decef5b9051110ee2ba05dbe1bdf0e682716509 원장
③ 757f8149edfa47d18e0da03242353ba540eb78ed 호출/관측
④ 8f6a8c626af1ebf9619991fdc82ea64d4d88a6b8 반례/분야
⑤ 1c1ebcecc3b2d0e5881818e5b619b67a42d44452 결과/자체점검
⑥ 이 파일 마지막 commit.

색인 제안: AF-RES-187 PARTIAL — NumPy 복사 계약 migration, HF Datasets 2.20.0→2.21.0 및 Astropy 6.0.1→6.1.0 실제 태그 대비, Quantity 단위 변환 strict 반례; 32개 원문; RESULT.md/advice.csv; 실제 사용자 입력·설치·재시험 미확인.
