# AF-RES-205 반례와 타 분야 대조

## 출력 값, 겹침, 쓰기 가능, 실제 전파

| 대조 | 처음 값 | 겹침 | 출력 쓰기 | 관측한 변경 | 영수증 |
| --- | --- | --- | --- | --- | --- |
| 독립 NumPy copy | `[0,1,2]` | False | True | output[0] → 99, 원본 0 → 0 | [1.26.4 r1/r2](receipts/controls.jsonl#L1-L2) · [2.0.0 r1/r2](receipts/controls.jsonl#L15-L16) |
| 가변 NumPy view | `[0,1,2]` | True | True | output[0] → 99, 원본 0 → 99 | [1.26.4 r1/r2](receipts/controls.jsonl#L3-L4) · [2.0.0 r1/r2](receipts/controls.jsonl#L17-L18) |
| 읽기전용 NumPy view | `[0,1,2]` | True | False | 양쪽 0 유지, 쓰기 미시도 | [1.26.4 r1/r2](receipts/controls.jsonl#L5-L6) · [2.0.0 r1/r2](receipts/controls.jsonl#L19-L20) |
| Arrow primitive 직접 view | `[0,1,2]` | True | False | 원본 0 유지, 쓰기 미시도 | [ARROW-readonly r1/r2](receipts/controls.jsonl#L29-L30) |
| Arrow primitive 직접 writable 변환 | `[0,1,2]` | False | True | output[0] → 99, 원본 0 → 0 | [ARROW-writable r1/r2](receipts/controls.jsonl#L31-L32) |

[A04-A1 False](receipts/A04/runs.jsonl#L3-L4), [A04-A2 False](receipts/A04/runs.jsonl#L7-L8), [A04-A2 기본](receipts/A04/runs.jsonl#L5-L6)도 각각 가변 alias, 읽기전용 alias, 읽기전용 입력에서 만든 독립 가변 사본을 보였다. 출력 변경을 시도한 경우와 쓰기 불가로 미시도한 경우를 구분한다. NumPy 겹침 및 flags 계약과 Arrow의 primitive/no-null 조건에서 분류 규칙을 확인했다. [N04](https://numpy.org/doc/2.0/reference/generated/numpy.shares_memory.html) · [N05](https://numpy.org/doc/2.0/reference/generated/numpy.ndarray.flags.html) · [N06](https://github.com/apache/arrow/blob/apache-arrow-16.1.0/python/pyarrow/array.pxi#L1542-L1597)

## 판정을 바꾼 관측

- **Datasets에서 먼저 복사가 필요한 단계.** Arrow 단계가 성공해도 마지막 NumPy 생성이 실패할 수 있었다. 패치 전 H02-H1/H2에서는 양 반복 모두 Arrow chunk의 `zero_copy_only=True` 다음에 Python list `[0,1,2]`를 관측하고, `formatting.py:197`에서 exit 10이 났다. H02-H3은 Arrow의 `False` 다음에 `[1.0, NaN, 3.0]` list를 만들어 object 분기 L196에서 exit 10이었다. H04의 list는 동일했고 L201 또는 L198에서 값이 반환되었다. Python trace를 사용한 보강 실행의 반환/예외 및 변경 결과는 trace 없는 두 원영수증과도 일치했다. [T01](https://github.com/huggingface/datasets/blob/98fdc9e78e6d057ca66e58a37f49d6618aab8130/src/datasets/formatting/formatting.py#L154-L197) · [T02](https://github.com/huggingface/datasets/blob/a1b5a32365cd2c6631fa4ad236a881f9f62bf32b/src/datasets/formatting/formatting.py#L154-L203) · [TRACE 16개](receipts/controls.jsonl#L39-L54)
- **Astropy의 dtype 요청 위치가 결론을 바꾼다.** ③의 A04-A3은 dtype을 명시했을 때 `ValueError`였고 그 근거는 생성자의 `np.array` 단계에 한정된다. 같은 정수 입력에 dtype 인자를 생략하고 `copy=False`를 유지하니 float64 `[0.0,1.0,2.0]`이 나왔다. 출력 변경 0.0→99.0에서 원본은 0→0이었다. default `np.inexact`의 후속 `astype(float)` 구간을 근거로 explicit dtype의 거부를 모든 정수→float 요청으로 확대하는 해석을 기각한다. A04-A4도 같은 False로 cm/s 사본을 반환하되 변환은 더 앞의 `.to`에서 일어난다. [T05 생성자](https://github.com/astropy/astropy/blob/e97756f0ecaa401e453745dd34d01980657ffa35/astropy/units/quantity.py#L429-L573) · [명시 dtype r1/r2](receipts/A04/runs.jsonl#L11-L12) · [생략 dtype r1/r2](receipts/controls.jsonl#L55-L56) · [단위 변환 r1/r2](receipts/A04/runs.jsonl#L15-L16)
- **NumPy 단독 계약의 경계.** `np.asarray(...,copy=False)`는 1.26.4의 동일 dtype·읽기전용·list·지정 dtype 입력 모두에서 TypeError였다. 2.0.0은 list와 명시 cast에 ValueError, 호환 가변 ndarray에서 공유와 전파, 읽기전용 ndarray에서 공유와 쓰기 불가였다. 같은 구문을 하류 API 전체에 적용하면 위 Astropy 두 반례를 놓친다. [N09](https://numpy.org/doc/1.26/reference/generated/numpy.asarray.html) · [N03](https://numpy.org/doc/2.0/reference/generated/numpy.asarray.html) · [1.26.4 네 쌍](receipts/controls.jsonl#L7-L14) · [2.0.0 네 쌍](receipts/controls.jsonl#L21-L28)

## OS와 보존 자료에서 가져올 기준

| 관점 | 원문 기준 | 대조 결과 및 가져올 범위 |
| --- | --- | --- |
| Linux 파일 매핑 | MAP_SHARED 업데이트는 같은 영역의 다른 공유 매핑에서 보인다. MAP_PRIVATE 쓰기는 사적 페이지로 분리된다. PROT_WRITE와 파일 반영 시점은 별도 조건이다. [X03](https://man7.org/linux/man-pages/man2/mmap.2.html#DESCRIPTION) | 두 매핑의 NumPy 주소는 겹치지 않았다. `ACCESS_WRITE`는 다른 매핑과 파일을 모두 `[99,1,2]`로 바꿨고 `ACCESS_COPY`는 출력만 바꿨다. `ACCESS_READ`는 쓰기 미시도다. 주소 겹침을 파일의 관계나 전파로 대신할 수 없다. [MMAP 6회](receipts/controls.jsonl#L33-L38) |
| Windows 파일 뷰 | FILE_MAP_READ, FILE_MAP_WRITE, FILE_MAP_COPY는 별개다. COPY에 쓰면 사적 페이지가 생기고 파일에 기록되지 않는다. [X04](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-mapviewoffile#parameters) | 초기 바이트와 쓰기 권한 및 지속성 분류에만 사용한다. Windows 실행은 미확인이다. |
| NARA 보존·접근 | 원본 필름을 보관한다. 장기 보존용은 고충실도, 접근용은 재생 용이성을 요구한다. 전자는 수백 GB가 될 수 있고 접근용은 낮은 해상도 등을 허용한다. [X01](https://www.archives.gov/preservation/formats/motion-picture-film-playback-digitize.html) | 원본과 접근 표현을 분리하면 H3의 null 위치 보존과 int64 표현을 함께 보고할 수 있다. 이 연결은 실험 설계 해석이며 기록물 보존 충실도를 배열 자료로 판정할 수 없다. |
| LOC 보존·대체·접근 | 첫 포착이 이후 품질의 상한이다. 물리 워터마크나 종이 속성은 스캔에 없을 수 있고 접근 파생본은 전송비를 낮출 수 있다. [X02](https://www.loc.gov/preservation/resources/rt/guide/guid_asp.html) | 두 표현에 공통인 사용 목적과 잃는 속성을 먼저 고정한다. H3의 NaN 또는 A4의 변환된 수치로 원본을 복구할 수 있는지는 이번 fixture의 성공 조건 밖이다. |

보강 실행 56개는 주표본 32셀과 원자료 하한에서 제외했다. 다른 임시 경로에서 해시 고정 lock으로 주표본 112회 전체를 재현했고 정상 resolver는 A02를 다시 차단했다. [별도 재생 검산](receipts/replay-check.json) · [공식 tag refs](receipts/tag-refs.json)
