# AF-RES-042 · 실행 전 판정 고정

배정 브랜치의 시작은 `65c60c084fe29047670ae40534939eb23c3e8fb5`다. `session start --fetch`가 읽은 통합판은 `333e83c9a46b0c005d22efcccbb5a055b27e904e`이며 그 사이 진행표만 전진했다. 상류 AF-RES-038 입력 SHA, 읽은 자료와 모델 표시 범위는 [manifest.json](manifest.json)에 있다. 원 드라이버를 Git 객체에서 바이트 그대로 추출했다. SHA-256은 `de8bad4712e00e626cccf3a6f3c6974c6c1f0797e0d91b5a2fdeb41e63bb709f`다. [AF-RES-038의 고정 입력과 명령](https://github.com/laadkke-arch/agentflow-open/blob/5a1699b24679cd7c58242cb98c40fa9fc9c6851a/docs/workstreams/research/AF-RES-038/streams/pandas/execution-next.md#L16-L46)

## 요구와 실행 범위

- P04의 각 독립 batch에 한 형식만 적용한다. DMY와 MDY는 모두 채점상 허용된다. 실제 선택 형식에서 불가능한 두 번째 문자열은 정당하게 거부해야 한다. 벡터와 Python loop의 반환 타입이 달라도 같은 날짜 의미를 충족할 수 있다. 첫 비결측 추론 경로는 한 번 정한 형식을 explicit으로 전달한다. PDEP가 소개하는 일반 오류 정책 중 이 과제는 `raise`를 택한다. [PDEP-4 최초판 L9–51](https://github.com/pandas-dev/pandas/blob/e59b6ffd4881ecebb1d3739080d16e162660ae83/web/pandas/pdeps/0004-consistent-to-datetime-parsing.md#L9-L51)
- P06는 매 probe를 독립 `[1,2,3]`에서 시작한다. 호환 int·whole float는 값과 선언 dtype을 보존한다. fractional·text는 명시적 오류와 기존 값·dtype의 유지로 판정한다. 원 드라이버는 t0의 두 대입을 이어서 한다. 독립 `2.0` probe의 초깃값과 원 드라이버의 직전 `4` 대입 후 상태를 각각 기록한다. `3.0`은 현재 값과 달라 실제 호환 대입을 구별한다. [PDEP-6 최초판 L65–123](https://github.com/pandas-dev/pandas/blob/1fb0adb5a7b1ba909fb34a19b1d27c7eccdf4119/web/pandas/pdeps/0006-ban-upcasting.md#L65-L123)
- P04 pandas 1.4.4와 P06 pandas 1.5.2를 CPython 3.10.6에서 각각 실행한다. NumPy 1.23.5, python-dateutil 2.8.2, pytz 2022.2.1, six 1.16.0은 038이 고른 재현판이다. P04 이슈·원제안과 P06 최초판에는 사례 코드가 있으나 작성자의 OS/ABI, 설치 전체나 wheel은 미확인이다. P06의 3.10.6은 비교용 선택이다. P04의 2022년 9월에 11월 공개 NumPy 1.23.5가 설치됐다고 추정할 수 없다. [Python 3.10.6 공개](https://www.python.org/downloads/release/python-3106/) · [NumPy 1.23.5 공개](https://numpy.org/doc/1.23/release/1.23.5-notes.html)
- P02 빌드, N08 최초판·가림 판독, AF-RES-034 문헌, 사람 시험, 시차·성능·locale·일반 결측·overflow·bool·묶음 쓰기는 범위 밖이다. 타 분야 규칙과 실자료는 스키마 선택의 반례로 읽는다. 아래 원과제 실행 분모는 해당 사례 없이 계산한다.

## 판정 단위와 실패 가설

| 구분 | 봉인한 단위 | 판정 |
| --- | --- | --- |
| 원 드라이버 P04 | 6 메서드, 그중 일반 계약 4, 오답 관행 관측 1, expectedFailure 1 | 일반 테스트가 실제 혼합 날짜를 확인하고 예상 실패는 오류가 안 나서 실패한 assertion이어야 한다. |
| 원 드라이버 P06 | 8 메서드, 그중 typed fixture 1, 일반 계약 2, 오답 관행 관측 2, expectedFailure 3 | 두 관측 메서드에서 float/object 승격과 배열 잘림을 확인한다. expectedFailure 수와 예상 밖 성공 0을 대조한다. |
| 독립 P04 | 3 batch × 6경로 = 18행. 드라이버 정답 계열 12, explicit MDY 추가 3, legacy 비교 3 (그중 한 형식 위반을 입증할 행 1) | 12-01/13-01은 DMY의 둘 다 성공, MDY의 두 번째 오류, legacy의 Dec 1/Jan 13 혼합을 구별한다. 12-01/01-13에서는 MDY의 둘 다 성공과 DMY의 두 번째 오류를 검증한다. |
| 독립 P06 | 5 typed literal × 5경로 = 25행. 허용 10, 비교 15 (그중 위반을 입증할 행 4) | 두 정상 구현 각각 3호환+2오류. 비교 경로의 작은 정수·whole float와 일부 오류는 일치해도 fractional/text 반례까지 봐야 한다. |
| 실행 및 빈 환경 반복 | 환경 2개 × 설치부터 독립 시도 2회 = 4회 | 설치, import, 원 테스트 시작, 의미 확인을 시도별로 기록한다. 이미지 및 wheel SHA, 입력 SHA, 종료코드, 결과를 대조하고 UTC·타이밍 등 변동을 따로 남긴다. |
| expectedFailure 민감도 | 실제 실패 4개와 일반 관측의 대응, 별도 런타임 예외 주입 4개와 import 차단 2개 | 같은 expectedFailure 카운트가 엉뚱한 오류로도 나올 수 있다. ordinary test의 실패 및 import 차단의 0 테스트 시작을 따로 검산한다. 주입 실행은 원 드라이버 분모와 별개다. |

일반 관측 없이 expectedFailure만 맞거나, input 타입이 바뀌거나, 올바른 분류에 잘못된 날짜·값·오류 후 상태가 뒤따르면 실측 동등을 거부한다. 버전 불일치 또는 주입하지 않은 import 실패는 테스트 시작 전 차단으로 남긴다. 본래 관측에서 판독 경계가 바뀌면 첫 기준과 결과를 보존하고 별도 진단으로 다룬다. [Typed 입력 및 사전 기대](inputs.jsonl) · [환경 계약](environments.json)

호환 float를 무조건 거부하는 경로, `2.0`을 건드리지 않는 경로, `1.5`를 정수로 자르는 경로는 일부 관측을 우연히 충족할 수 있다. P04 legacy는 t0나 MDY에 맞는 t1 batch에서 일치할 수 있다. 이 행만으로 계약 전체를 판정하지 않는다. 날짜 정밀도나 공식 통계의 단위·결측 스키마가 달라지면 엄격성의 비교도 달라진다. [당시 pandas 날짜 테스트 L2033–2068](https://github.com/pandas-dev/pandas/blob/ca60aab7340d9989d9428e11a51467658190bb6b/pandas/tests/tools/test_to_datetime.py#L2033-L2068) · [NumPy 배정의 값 손실 예시](https://numpy.org/doc/1.23/user/basics.indexing.html#assigning-values-to-indexed-arrays)
