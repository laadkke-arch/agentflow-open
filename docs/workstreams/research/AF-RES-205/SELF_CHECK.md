# AF-RES-205 자체점검

| 질문 | 확인 원자료 및 정확 위치 | 찾아본 반례·경쟁 조건 | 반증 또는 남은 경계 |
| --- | --- | --- | --- |
| Q1 | [W01–W04 ZIP/RECORD/태그 지문](artifacts.csv) · [공식 tag refs](receipts/tag-refs.json) · [T06](https://github.com/astropy/astropy/blob/78cf5340ddf9fe9731906224a638c4888849c93f/astropy/utils/compat/numpycompat.py#L24-L32) · [T07](https://github.com/astropy/astropy/blob/e97756f0ecaa401e453745dd34d01980657ffa35/astropy/utils/compat/numpycompat.py#L23-L30) | 게시 해시/크기, zip RECORD, 원문 member SHA/구간 SHA, 실제 로드 파일까지 대조. 두 Astropy wheel에서 compatibility module 존재 여부를 다시 확인 | 네 wheel 및 관련 파일 여섯 개 일치. module 제거 해석 기각. 제거 대상은 T05 inline override |
| Q2 | [W03 Requires-Dist](https://pypi.org/pypi/astropy/6.0.1/json) · [A02 resolver](receipts/A02/setup.jsonl#L3) · [A04 정상 import](receipts/A04/setup.jsonl#L6) · [H02 정상 import](receipts/H02/setup.jsonl#L6) | 선언 충돌, 호환 wheel 부재, ABI, 정상 import 이후 행동 예외를 따로 조회. 가능한 7개를 파일 해시 잠금으로 재실행 | 선언 충돌 하나. 같은 실패로 묶는 해석 기각. 다른 플랫폼 ABI 미확인 |
| Q3 | [N06](https://github.com/apache/arrow/blob/apache-arrow-16.1.0/python/pyarrow/array.pxi#L1542-L1597) · [N07](https://arrow.apache.org/docs/16.1/python/generated/pyarrow.ChunkedArray.html#pyarrow.ChunkedArray.to_numpy) · [T01/T02](artifacts.csv) | H1 직접 배열 view 대조, H2–H4의 원본 구성 버퍼 및 H02/H04에서 중간 list를 새 프로세스 trace로 직접 확인. [TRACE L39–54](receipts/controls.jsonl#L39-L54) | chunk zero-copy → 최종 alias라는 설명 반증. H2–H4의 단일 논리 원버퍼 겹침은 해당 없음 |
| Q4 | [T03](https://github.com/huggingface/datasets/blob/a1b5a32365cd2c6631fa4ad236a881f9f62bf32b/tests/test_formatting.py#L51-L100) · [T05](https://github.com/astropy/astropy/blob/e97756f0ecaa401e453745dd34d01980657ffa35/astropy/units/quantity.py#L429-L573) · [T08](https://github.com/astropy/astropy/blob/e97756f0ecaa401e453745dd34d01980657ffa35/astropy/units/tests/test_quantity.py#L165-L190) | H3 보고 `None`/NaN 및 object dtype, A04 같은 정수에 explicit·implicit dtype, cm/s 단위 변경. [H04 H3](receipts/H04/runs.jsonl#L9-L12) · [A04 explicit](receipts/A04/runs.jsonl#L9-L16) · [implicit](receipts/controls.jsonl#L55-L56) | 결측 위치 보존의 조건 명시. 변환 요구 전체에 strict를 적용한다는 해석 반증 |
| Q5 | [N04](https://numpy.org/doc/2.0/reference/generated/numpy.shares_memory.html) · [N05 WRITEABLE](https://numpy.org/doc/2.0/reference/generated/numpy.ndarray.flags.html) · [A04 A1/A2](receipts/A04/runs.jsonl#L1-L8) | 동일한 초기 값의 NumPy copy, 가변 view, readonly view와 직접 Arrow 두 옵션. 원본과 출력의 실제 첫 원소 및 flag를 확인. [통제군](COUNTEREXAMPLES.md) | 정확한 값, 공유, 쓰기 가능, 전파를 서로 대신할 수 있다는 해석 반증. 주표본 88회 테스트 중 6회 전파, 82회 변화 없음, 6회 반환에서 쓰기 미시도 |
| Q6 | [X01 vendor/spec](https://www.archives.gov/preservation/formats/motion-picture-film-playback-digitize.html) · [X02 USE](https://www.loc.gov/preservation/resources/rt/guide/guid_asp.html) · [X03 prot/flags](https://man7.org/linux/man-pages/man2/mmap.2.html#DESCRIPTION) · [X04 dwDesiredAccess](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-mapviewoffile#parameters) | NARA 원본 유지와 접근 비용, LOC 포착 바깥의 워터마크, Linux shared/private/read permissions. [MMAP L33–38](receipts/controls.jsonl#L33-L38) | 두 virtual NumPy 배열의 겹침이 False여도 공유 파일 매핑으로 전파됨. Windows와 보존 자체는 원문 기반 비교 |
| Q7 | [D04 R01–R03](https://github.com/laadkke-arch/agentflow-open/blob/4dd004ba7bebb19ebc03f2539bf5716a14bd1787/docs/workstreams/research/AF-RES-187/advice.csv#L2-L4) · [J02 첫 두 traceback](https://discuss.huggingface.co/t/valueerror-unable-to-avoid-copy-while-creating-an-array-as-requested/93584) · [J03 초기 제안](https://github.com/astropy/astropy/issues/16167) | 같은 어휘의 1.26/2.0 direct strict, 설치 실패와 행동 오류 구분, writable/readonly/copied 변환 대조. [N03](https://numpy.org/doc/2.0/reference/generated/numpy.asarray.html) · [N09](https://numpy.org/doc/1.26/reference/generated/numpy.asarray.html) · [대응 원장](advice.csv) | R01과 R03 유지, R01 표현과 R02 하류 적용은 범위 축소. Astropy 전체 strict 해석 반증. 역사 환경 0건 확인으로 유지 |

## 원자료와 모집 결산

| 종류 | 고유 직접 산입 | 목표 | 미달 | 범위 |
| --- | ---: | ---: | ---: | --- |
| Wheel 본문 | 4 | 4 | 0 | W01–W04 |
| Upstream 고정 tag 구현·fixture | 8 | 6 | 0 | T01–T08 |
| NumPy/PyArrow 계약·구현 | 7 | 4 | 0 | N01–N07 |
| 187 고정 호출·관측 원자료 | 5 | 4 | 0 | J01–J05 |
| 보존·OS 매핑 | 4 | 4 | 0 | X01–X04 |
| 합계 | **28** | **22** | **0** | [원출처 및 위치](sources.jsonl) |

- 직독 원장 41행이다. 28개 산입, 공개 원문 보강 T09·N09 두 개, 의존 기록 D01–D05 다섯 개, 중복·같은 배포물의 교차 확인 여섯 개를 보존했다. 모집표 113행 중 적격 35, 관측 57, 차단 5, 제외 8, 중복 6, 보강 열린 원문 1, 역사 증거 미확인 1이다. 차단 5는 A02 환경 1과 그 셀 4이며 중복 가산하지 않았다. 모집한 주 원자료의 접근 실패는 0이다. [모집표](frame.csv)
- 산입 원문의 lineage_id는 13개, 의존 문서 계보를 포함한 원장 전체는 14개다. 고정 역사 사례는 서로 다른 3건이다. Datasets 패치의 MTEB 오류 언급, 포럼 초기 제보의 두 진입점 한 건, Astropy 이슈·두 PR 한 건으로 계산했다. 이 사례의 독립 이용자 재시험은 0이다. 네 타 분야 문서는 두 OS 계약과 두 기관 지침이고 별도 사용자 사건으로 세지 않았다.
- 예정 셀 32/32에 상태가 있다. 성공·실패를 관측한 셀 28, 설치 불가 사유만 있는 셀 4다. 독립 프로세스 112개는 반환 94, 행동 예외 18이고 옵션별 반복 56쌍이 PID를 제외한 동일 결과였다. 주표본 밖 보강 56개 및 별도 잠금 재실행 112개는 원자료 수에 산입하지 않았다. [matrix](matrix.csv) · [잠금 재실행](receipts/replay-check.json)

## 검사 경계

- ③ 주표본은 `e262deee47cf50b0978f0bd849c696aae092ff3a`에 보존한 probe 바이트와 `inputs.json` 지문을 원영수증에서 확인했다. ④는 lock CLI 경로를 자식 작업 디렉터리 기준 문제가 없도록 절대 경로화하고 다른 임시 작업에서 결과와 stderr를 112회 대조했다. 두 probe 해시가 재생 영수증에 있다. [runtime](receipts/runtime.json) · [replay](receipts/replay-check.json)
- GitHub에서 별도 새 checkout을 만들고 ④ `de65e7186c8e24a7ae502223a3ae5b50d3afe1c6`에서 `workbench.session check ... --fetch`의 범위·의존 핀 및 원격 최신성을 확인했다. `scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean`은 exit 0이며 공통 55, lab 7·9 시험을 포함한다. 공통 check-all의 세션 목록은 no_active_sessions였으며, 이 작업의 개별 manifest 확인 결과는 별도다. 통합 기준은 검사 시 `bb146773bbffba5e724e8c842951e2c25198c2da`, 계약 내용은 시작 pin과 같았다. [검사 영수증](receipts/workbench-stage4.json)
- 자료 ID·type별 하한·행 선택·옵션별 영수증·주요 부울 값 및 표 순서를 자체 점검했다. 독립 세션 검토는 미실시다. 원제보자 환경, 다른 wheel 및 소스 배포, 시기·성능 일반화는 미확인이다. 지정된 4 wheel/32셀, 양 하류의 실측 및 copy/view 통제 기준의 미충족은 0이다.
