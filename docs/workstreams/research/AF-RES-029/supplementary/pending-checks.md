# 미실시 검사와 재개 입력

이 문서는 미실시 작업의 입력과 명령을 남긴다. 아래 명령의 종료 코드를 얻었다고 주장하지 않는다. 이미 실행한 명령·환경·출력은 `runtime-probes.json`, `additional-runtime-probes.json` 및 인계 전 셸 영수증에 따로 있다. 후속 실행은 원 A/B 반환을 소급 변경하지 않는다.

## 1. Q12 — 새 헤더로 만든 확장을 이전 런타임에서 로드

**미실시 이유:** 현재 설치된 NumPy는 2.3.5 하나다. Python 3.11과 NumPy 2.1.0/1.23.5의 분리 환경 및 해당 wheel 공급 경로를 마련하지 않았다. 문서 계약 점수와 실제 ABI 실행 검증을 구별한다. [Build-time dependency](https://numpy.org/doc/stable/dev/depending_on_numpy.html#build-time-dependency)와 [NumPy 2.0-specific advice](https://numpy.org/doc/stable/dev/depending_on_numpy.html#numpy-2-0-specific-advice)가 마지막 확인 위치다.

**입력:** Python 3.11, 빌드 NumPy 2.1.0, 실행 NumPy 1.23.5, `NPY_TARGET_VERSION=NPY_1_22_API_VERSION`; 다음 C 소스. 소스의 실제 확장 빌드/로드는 아직 실행하지 않았다.

```c
#define PY_SSIZE_T_CLEAN
#ifndef NPY_TARGET_VERSION
#define NPY_TARGET_VERSION NPY_1_22_API_VERSION
#endif
#include <Python.h>
#include <numpy/arrayobject.h>

static PyObject *versions(PyObject *self, PyObject *args) {
    return Py_BuildValue("(kkkk)",
        (unsigned long)NPY_API_VERSION,
        (unsigned long)NPY_FEATURE_VERSION,
        (unsigned long)PyArray_GetNDArrayCVersion(),
        (unsigned long)PyArray_GetNDArrayCFeatureVersion());
}
static PyMethodDef methods[] = {
    {"versions", versions, METH_NOARGS, "Return compiled and runtime API versions."},
    {NULL, NULL, 0, NULL}
};
static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT, "abi_probe", NULL, -1, methods
};
PyMODINIT_FUNC PyInit_abi_probe(void) {
    import_array();
    return PyModule_Create(&module);
}
```

소스를 소유 경로의 `supplementary/abi-run/abi_probe.c`에 저장하고 같은 디렉터리에 다음 `setup.py`를 둔다.

```python
from setuptools import Extension, setup
import numpy
setup(name="af029-abi-probe", version="0",
      ext_modules=[Extension("abi_probe", ["abi_probe.c"],
                             include_dirs=[numpy.get_include()])])
```

저장소 루트에서 실행할 명령:

```sh
TASK_ABI=docs/workstreams/research/AF-RES-029/supplementary/abi-run
python3.11 -m venv "$TASK_ABI/build-env"
python3.11 -m venv "$TASK_ABI/old-env"
"$TASK_ABI/build-env/bin/python" -m pip install --no-cache-dir numpy==2.1.0 setuptools==75.1.0 wheel==0.44.0
"$TASK_ABI/old-env/bin/python" -m pip install --no-cache-dir numpy==1.23.5
cd "$TASK_ABI"
build-env/bin/python setup.py build_ext --inplace
old-env/bin/python -B -c 'import numpy, abi_probe; print(numpy.__version__, abi_probe.versions())'
```

버전·컴파일러·확장 파일 해시·명령별 종료 코드·stderr를 저장한다. 이 하나의 로드 성공만으로 새 API 은폐, 모든 dtype/ufunc, 모든 플랫폼 ABI를 확인했다고 하지 않는다. 기본값의 은폐까지 보려면 `NPY_TARGET_VERSION` 정의를 제거한 **별도** 소스로 다시 빌드하고, 고정판 헤더의 새 API `#if NPY_FEATURE_VERSION` 경계 및 음성 컴파일 입력을 먼저 확정해야 한다. 그 정확한 헤더가 답을 바꿀 다음 자료다.

## 2. Q05 — 유지한 frame view의 generator·thread 경계

**미실시 이유:** 현재 Python은 3.12.14이며, 반환된 긍정 계약은 3.13 이후 proxy를 설명한다. 설치되지 않은 판의 동작으로 추정하지 않았다. 마지막 확인은 [3.13 frame C API](https://docs.python.org/3.13/c-api/frame.html#c.PyFrame_GetLocals) 및 [frame objects](https://docs.python.org/3/reference/datamodel.html#frame-objects)이다.

Python 3.13 이상에서 다음을 `python3.13 -B`의 표준입력으로 실행한다. 반환된 기존 local을 수정하고 같은 view에서 다음 변경을 읽는 입력이다. 이 시험은 generator 한 개의 한 스레드 전환이며, 모든 coroutine·free-threading 보장을 증명하지 않는다.

```python
import sys, threading
def g():
    x = 1
    yield sys._getframe()
    assert x == 2
    x = 3
    yield x
it = g()
frame = next(it)
view = frame.f_locals
view["x"] = 2
out, errors = [], []
def resume():
    try:
        out.append(next(it))
    except BaseException as exc:
        errors.append(repr(exc))
t = threading.Thread(target=resume)
t.start()
t.join(10)
assert not t.is_alive()
assert not errors, errors
assert out == [3] and view["x"] == 3, (out, dict(view))
print(sys.version, out, dict(view))
```

첫안의 `locals()`도 live여야 한다는 전체 요구와 이 부분 frame 검사는 별개다. 원안의 잘못된 `nonlocal` 예제를 조용히 고쳐 전체 성공으로 세지 않는다.

## 3. Q01 — 의미 일치와 실제 Go 호출자 사이

**미실시 이유:** 반환에 Go↔PHP/JavaScript 값 연결 부품이 없다. 이미 실행한 JavaScript 추출 예제는 입력 `[10]`, 폭 3에서 `[10,null,null]`, 입력 `[10,20,30]`, 폭 2에서 `[10,20]`을 만들었다. 이것은 Go의 `[]interface{}` 입력·nil·타입 보존을 검증하지 않는다.

다음 첫 자료는 실제 Go 호출자와 반환된 언어의 값을 왕복시키는 공급자 어댑터 명세·태그판 구현이다. 그 부품을 확보한 뒤 사용할 고정 입력은 `[]interface{}{int64(10), "x", nil}`, 빈 배열, 폭 0/2/5, 길이 초과 입력이다. Go nil과 숫자/문자열 타입을 보존하고, **어댑터 자체가 추출/패딩 핵심 기능을 새로 구현하지 않는지** 점검해야 한다. 현재는 그런 구현이 없으므로 가상의 `go test` 패키지/명령을 만들지 않는다. 실행 가능한 부품이 생긴 시점에 패키지의 실제 테스트 명령과 판을 추가한다.

## 4. 엄격 표집·노출·탐색 예산의 재실험

과거의 상태 노출은 현재 파일을 고쳐 없앨 수 없다. `audits/method-input-audit.md`의 최초판/표집 한계와 `evidence/exposure-audit.json`을 입력으로, 별도 문맥에서 제목·첫 시각·첫 목적만 보이는 원장을 새로 투영해야 한다. 새 회차임을 명시하고 원본 결과를 보존한다.

원 영수증을 재검하는 현재 재현 명령은 다음과 같다.

```sh
python -B docs/workstreams/research/AF-RES-029/validate_artifacts.py --require-routes --output evidence/recheck-artifacts.json
python -B docs/workstreams/research/AF-RES-029/recount.py --check
python -B -m workbench.session check docs/workstreams/research/AF-RES-029/manifest.json --fetch
```

`find`도 탐색 1회로 세는 재실험에서는 Q06-B, Q07-B, Q09-A, Q11-B의 원 결과를 잘라서 수리하지 않는다. 2회 예산을 사용 전에 차감하는 새 선택기를 별도 입력·반환으로 실행한다. 원 비교에서는 이 네 경로를 보존하고, 두 경로 모두 해당 해석을 지킨 8쌍을 따로 집계한다.

## 5. 제조사 자료 충돌과 박물관 객체 식별

[1591XXASBK 개별 기록](https://www.hammfg.com/part/1591XXASBK)과 [도면](https://www.hammfg.com/files/parts/pdf/1591XXASBK.pdf)의 치수·나사 불일치는 실제 조립이나 제조사 개정 이력으로 해결하지 못했다. 다음 자료는 **동일 부품 번호와 개정일이 표시된 제조사 승인 도면**이다. 근거 없는 최신판 선택이나 제조사 문의 발송은 하지 않았다.

[Met API](https://metmuseum.github.io/)는 accessionNumber가 항상 고유하지 않다고 명시한다. 현재 사례에서는 동일 번호 계열의 다른 실물 두 개를 실제로 대응하지 않았다. 다음은 같은 accessionNumber를 공유하는 두 objectID의 현재 객체 기록이며, 이 보강은 12개 설계 사건의 적합률에 넣지 않는다.

