# AF-RES-205 범위와 판정 규칙

## 입력과 시작점

- GitHub `chore/workspace-foundation` 시작 SHA `c860f8240ab7b7077e2d5b63e438ddd83ff69a27`. 계획 SHA `050278651b11a2a3a49d45baebf41c707c06b700`의 후손이다. 사이 네 커밋 `cc51999`, `ca4f683`, `81e21cc`, `c860f82`의 변경 파일은 `docs/automation/dot-control.json` 하나이며 최신 AF-RES-205 행은 RUNNING, 의존은 AF-RES-187 하나다.
- 원격에 배정 브랜치가 없어 시작 SHA에서 `work/research-af-res-205`를 만들었다. [작업 계약](session.json)은 의존 브랜치의 정확한 SHA와 편집 허용 경로를 고정한다. [작업 규칙](https://github.com/laadkke-arch/agentflow-open/blob/c860f8240ab7b7077e2d5b63e438ddd83ff69a27/AGENTS.md), [현재 상태](https://github.com/laadkke-arch/agentflow-open/blob/c860f8240ab7b7077e2d5b63e438ddd83ff69a27/STATE.md), [Dot 절차](https://github.com/laadkke-arch/agentflow-open/blob/c860f8240ab7b7077e2d5b63e438ddd83ff69a27/docs/DOT_AUTOMATION.md), [연구 운영](https://github.com/laadkke-arch/agentflow-open/blob/c860f8240ab7b7077e2d5b63e438ddd83ff69a27/docs/RESEARCH_WORKFLOW.md), [배정 행](https://github.com/laadkke-arch/agentflow-open/blob/c860f8240ab7b7077e2d5b63e438ddd83ff69a27/docs/automation/dot-control.json), [제품 브리프](https://github.com/laadkke-arch/agentflow-open/blob/c860f8240ab7b7077e2d5b63e438ddd83ff69a27/docs/product/RESEARCH_BRIEF.md), [연구 색인](https://github.com/laadkke-arch/agentflow-open/blob/c860f8240ab7b7077e2d5b63e438ddd83ff69a27/docs/research/INDEX.md)을 읽었다.
- AF-RES-187 `4dd004ba7bebb19ebc03f2539bf5716a14bd1787`의 [HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/4dd004ba7bebb19ebc03f2539bf5716a14bd1787/docs/workstreams/research/AF-RES-187/HANDOFF.md), RESULT, calls.csv, advice.csv 및 필요한 sources 행에 먼저 노출됐다. 2.20.0의 list→strict False 실패 가설, 2.21.0의 asarray 복구 가설, Astropy의 같은 단위 view 및 다른 단위 할당 예상은 이미 알고 있다. 조사·분류가 맹검이라는 전제는 두지 않는다. 시작 시 신규 wheel 본문과 fixture 실행 판정은 비어 있다.
- AF-RES-195/196의 자료 및 동시 과제는 입력에서 제외한다. 포럼·후계 정책 조사와 새 제보 모집, 전체 릴리스 최초 도달 지점 전수, 성능·전체 ABI 조사, 제품 설계 선택은 이번 범위 밖이다. 공개 원문 중 187이 고정한 호출의 해당 위치만 다시 연다. 최초 이용자의 실제 과거 환경·입력·해결 여부는 별도 증거 자리로 유지한다.

## 분모와 fixture

Linux x86_64, CPython 3.11을 사용한다. HF는 PyArrow 16.1.0을 고정한다. 각 환경에서 별도 임시 venv로 NumPy와 하류 wheel을 정상 resolver에 함께 제공한다.

| 환경 | 패키지 | NumPy |
| --- | --- | --- |
| H01 | Datasets 2.20.0 | 1.26.4 |
| H02 | Datasets 2.20.0 | 2.0.0 |
| H03 | Datasets 2.21.0 | 1.26.4 |
| H04 | Datasets 2.21.0 | 2.0.0 |
| A01 | Astropy 6.0.1 | 1.26.4 |
| A02 | Astropy 6.0.1 | 2.0.0 |
| A03 | Astropy 6.1.0 | 1.26.4 |
| A04 | Astropy 6.1.0 | 2.0.0 |

| ID | 합성 원입력 | 공통 호출 |
| --- | --- | --- |
| H1 | Arrow int64 `[[0,1,2]]`, 단일 chunk | `NumpyArrowExtractor().extract_column(table)`, `extract_batch(table)["x"]` |
| H2 | Arrow int64 `[[0,1],[2]]`, 두 chunk | 두 공개 extractor 메서드 각각 |
| H3 | Arrow int64 `[[1,null,3]]` | 두 공개 extractor 메서드 각각 |
| H4 | Arrow string `[["foo","bar","foobar"]]` | 두 공개 extractor 메서드 각각 |
| A1 | `np.arange(10.0)`, float64, 가변 | `Quantity(a, m/s)`, 같은 호출에 `copy=False` |
| A2 | A1과 같은 값·dtype, writeable=False | `Quantity(a, m/s)`, 같은 호출에 `copy=False` |
| A3 | `[0,1,2]` int64, 생성 요청 `dtype=np.float64` | `Quantity(a, m/s, dtype=np.float64)`, 같은 호출에 `copy=False` |
| A4 | `Quantity(np.arange(10.0), m/s)` | `Quantity(q, cm/s)`, 같은 호출에 `copy=False` |

32개 예정 셀, 각 셀에 옵션 두 개, 옵션당 새 프로세스·새 원입력 두 번으로 최대 128회다. 같은 입력을 옵션 사이에 재사용하지 않는다. 통제 행은 독립 copy, 가변 view, 읽기전용 view이며 32개 분모 밖이다. A3의 target dtype을 생략하는 대조 역시 분모 밖이며 Astropy가 내부에서 형을 바꾸는지 확인할 수 있다.

## 모집 순서와 규칙

1. PyPI의 네 exact release와 Linux x86_64/CPython 3.11 호환 wheel 한 개씩을 찾고, sha256과 compatible tag를 확인한다. zipfile의 관련 파일·METADATA·RECORD를 직접 읽고 187의 고정 tag SHA 및 경로와 바이트 및 관련 구간 지문을 대조한다. release 페이지와 같은 wheel 속성은 별도 최소치로 더하지 않는다.
2. 상류 고정 tag의 구현·fixture 6개 이상, NumPy/PyArrow 계약·구현 4개 이상, 187에 고정된 호출·관측 원자료 4개 이상, 187의 Linux/Microsoft/NARA/LOC 원문 4개를 연다. 네 wheel을 포함한 고유 원자료 하한은 22개다. 같은 문서의 절, 같은 파일의 동일 blob, 수정되지 않은 판, 미열람·접근 실패·중복, 자체 생성 로그는 분모 충족에 쓰지 않는다. 사건은 문서 수와 따로 집계한다.
3. resolver는 정확한 wheel들과 NumPy·PyArrow 핀을 정상 설치한다. 선언된 충돌, 호환 wheel 부재, ABI 실패, 기타 설치/로드 오류, fixture에서 발생한 행동 예외를 각각 기록한다. 지원 선언, 설치/로드 성공, 각 호출의 성공을 독립적으로 해석한다. 상위 핀 외 보조 의존성은 resolver가 고른 실제 판을 보존한다.
4. 실행 결과의 값·dtype·단위·shape·예외, 원버퍼의 실제 겹침, 출력 쓰기 가능, 쓰기 전후 원본값을 분리한다. H1 기준은 원본 Arrow data buffer를 가리키는 직접 zero-copy NumPy view다. H2–H4에서는 단일 비교 원버퍼 여부, 구성 buffer별 겹침, 추출기의 중간 list 및 논리적 원본의 값 전파를 구분한다. 관측 불가나 쓰기 미시도는 음성 결과와 별도 표기한다. 읽기전용 입력을 그대로 유지한 채 쓰기 가능한 독립 결과에서만 쓰기를 시도한다.
5. 값만 필요한 이용자, 쓰기 전파가 필요한 이용자, 배포 관리자, 보존 원본/접근 사본 담당자의 판정 기준을 대조한다. 정상 값의 독립 사본, 읽기전용 공유 view, 단위 및 dtype 변환, 설치 차단을 반례로 사용한다. 각 결과는 이 입력·호출·wheel·환경에 한정한다.
