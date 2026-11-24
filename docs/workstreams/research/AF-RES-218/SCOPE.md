# AF-RES-218 범위와 판정 규칙

## 착수

같은 프로세스에서 `Quantity`를 통해 원배열을 바꾼 개발자가 기존 FITS 파일을 새 프로세스로 다시 열 때, 어느 저장 경계부터 같은 HDU·픽셀·단위의 새 값을 읽는지 확인한다. 제품 브리프의 부분 구조 탐색 사례이며 결과에서 임시 계산, 기존 파일 수정, 별도 산출물에 각각 필요한 원문을 안내한다. [연구 브리프](https://github.com/laadkke-arch/agentflow-open/blob/bb146773bbffba5e724e8c842951e2c25198c2da/docs/product/RESEARCH_BRIEF.md) · [연구 운영 규칙](https://github.com/laadkke-arch/agentflow-open/blob/bb146773bbffba5e724e8c842951e2c25198c2da/docs/RESEARCH_WORKFLOW.md)

- 저장소 `laadkke-arch/agentflow-open`, 브랜치 `work/research-af-res-218`, 소유 경로 `docs/workstreams/research/AF-RES-218/`. 2026-11-24 21:30:16 UTC에 생성한 계약은 최신 통합 `87ffc1539bcf33da0fccf45eb15982a02d93e409`에서 시작했다. [작업 계약](session.json)
- 계획 기준 `bb146773bbffba5e724e8c842951e2c25198c2da`에는 205가 `RUNNING`이고 `result_commit`이 비어 있다. 최신 기준과의 다섯 커밋은 모두 진행표 변경이다. `c87f64b`가 205의 완료를 기록했고 `d9d16d4`가 218을 가져와 의존을 연결했으며 `87ffc15`가 218 시도 1을 `RUNNING`으로 기록했다. 206·207 변경은 진행표 차이의 일부다. 해당 작업의 산출물은 이 시험의 입력에서 제외했다. [계획 기준 진행표](https://github.com/laadkke-arch/agentflow-open/blob/bb146773bbffba5e724e8c842951e2c25198c2da/docs/automation/dot-control.json) · [착수 진행표](https://github.com/laadkke-arch/agentflow-open/blob/87ffc1539bcf33da0fccf45eb15982a02d93e409/docs/automation/dot-control.json)
- 착수 진행표의 AF-RES-205는 `DONE`, `result_commit`은 `3853289f5189ad8af242c0f62d6cad566f31bc66`이다. 이 SHA의 205 인계, 표 순서, 실행 코드, 입력, A01 원영수증을 먼저 읽었다. 첫 적격 셀 `A01-A1`, 옵션 `false`의 두 번 모두 가변 ndarray의 첫 원값이 `0.0 → 99.0`으로 바뀌었다. 같은 셀의 기본 옵션은 비교에서 제외한다. 반환값만 바뀐 관측이기 때문이다. [205 인계](https://github.com/laadkke-arch/agentflow-open/blob/3853289f5189ad8af242c0f62d6cad566f31bc66/docs/workstreams/research/AF-RES-205/HANDOFF.md) · [205 표 행](https://github.com/laadkke-arch/agentflow-open/blob/3853289f5189ad8af242c0f62d6cad566f31bc66/docs/workstreams/research/AF-RES-205/matrix.csv#L18) · [205 원영수증](https://github.com/laadkke-arch/agentflow-open/blob/3853289f5189ad8af242c0f62d6cad566f31bc66/docs/workstreams/research/AF-RES-205/receipts/A01/runs.jsonl#L1-L4)
- 정확 환경은 Linux x86_64, CPython 3.11.15, NumPy 1.26.4, Astropy 6.0.1의 W03 wheel `2c00922548a666b026e2630a563090341d74c8222066e9c84c9673395bca7363`이며 205의 A01 해시 잠금을 사용한다. `Quantity(original, unit=u.Unit("m / s"), copy=False)`에서 `dtype` 인수는 생략한다. 205의 네 wheel·32셀은 재실행 범위 밖이다. [205 실행 코드](https://github.com/laadkke-arch/agentflow-open/blob/3853289f5189ad8af242c0f62d6cad566f31bc66/docs/workstreams/research/AF-RES-205/probe.py#L247-L278) · [205 환경 잠금](https://github.com/laadkke-arch/agentflow-open/blob/3853289f5189ad8af242c0f62d6cad566f31bc66/docs/workstreams/research/AF-RES-205/receipts/A01/requirements.lock)

## 표집과 경계

합성 `PrimaryHDU` 이미지 하나를 만든다. HDU 0, 1차원 `float64`의 `[0.0, …, 9.0]`, `BITPIX=-64`, `NAXIS=1`, `NAXIS1=10`, `BUNIT='m s-1'`, `BSCALE`·`BZERO` 카드 없음이다. FITS 0번 픽셀을 `0.0 → 99.0 m / s`로 수정한다. 표준의 저장 순서인 `>f8`을 직접 바이트로 확인한다. 매 사례에 별도 사본을 사용하고 같은 파일의 사전 SHA-256을 기준 파일과 맞춘다. 공개 관측물에는 접근하거나 쓰지 않는다.

| 집합 | 예정 분모 | 배정과 제외 |
| --- | ---: | --- |
| 선행 후보 | 첫 적격 셀 1 | 원표 순서에서 최초 실제 전파. `default`는 같은 셀의 배제 대조. 뒤 셀은 재시험 범위 밖 |
| 예비 양성·형식 확인 | 3 | 네이티브 `float64` 힙, `>f8` 힙, 별도 FITS 사본의 매핑. 재현된 네이티브 전파를 착수 전제에서 확인하고 파일에서의 추가 복사는 관측으로 남김 |
| 메모리 경로 | 6 | `readonly`·`copyonwrite`·`update` × HDU 배열 직접 쓰기·고정 `Quantity` 반환값 쓰기. 각 writer는 `memmap=True` |
| 원경로 영속성 | 12자리 × 2회 = 24 | 각 메모리 경로에서 기본 `close` 또는 명시적 `flush` 뒤 `close`. 입력 사본과 writer 프로세스를 분리 |
| 별도 FITS 통제 | 6 | 새 경로 `writeto`, 깊은 사본, 쓰기 없는 `update` 닫기, 버퍼 사용 `update` 직접 쓰기, 헤더만 변경, 기존 출력 경로 덮어쓰기 거부 |
| 외부 비교 | SQLite 원문 3 이상 | 공식 커밋·별도 연결 사례 대조. 합성 재생을 할 경우 FITS 분모 밖 |
| 고유 직접 자료 | 22 이상 | 205 인계·관측·호출·환경 4, 동일판 Astropy FITS 8, FITS 규격·공식 해설·예제 4, NumPy/Python 3, SQLite 3. 원문 중복과 탐색 입구는 하한 밖 |

## 판정

1. 메모리 반영은 수정 대상을 `99.0`으로 읽고 같은 writer의 HDU 배열에서도 `0.0 → 99.0`을 읽었을 때 기록한다. `np.shares_memory`, writeability, dtype과 단위는 각각 기록한다. 쓰기 예외, 복사, 환경·실행 실패는 각각 별도 결과다.
2. 새 reader 프로세스를 수정 직후와 명시적 flush 뒤(해당 조건만), HDU close 직후, writer 종료 뒤에 실행한다. 원경로의 HDU·픽셀·단위·원픽셀 바이트와 전체·헤더·데이터 SHA-256, 각 reader의 종료코드를 기록한다. 마지막 reader는 writer 종료코드를 받은 뒤 부모가 실행한다. 새 경로는 생성한 사례에서 같은 절차로 읽는다.
3. 원경로 영속 확인에는 writer 종료 뒤 reader의 성공, 원경로 동일성, HDU 0의 픽셀 값과 BUNIT, 원픽셀 바이트의 일치가 필요하다. 원값과 원바이트가 확인되면 원픽셀 불변으로 판정한다. 바뀐 해시만 보이거나 flush 반환만 성공하면 픽셀 판정의 근거가 부족하다. 헤더·데이터 영역 지문으로 헤더만 변경된 경우를 검출한다.
4. `flush` 및 `close`의 반환, 경고, 예외는 별도 수집한다. 지원이 거부된 동작을 통제에서 실제 예외로 확인한다. 파일 잠금, 동시 writer, 다른 OS나 FITS 형식, 장애·전원 상실 뒤의 내구성은 시험 범위 밖이다.
5. 예정 슬롯·실제 판정·실행 실패·보강을 모집표에서 구별한다. 직접 관측은 실행 로그, 기대값은 판정 규칙, 공급자의 설명은 출처 원장에 연결한다. 독립 프로세스의 집계 재생과 독립 연구자 검토 여부를 따로 기록한다.

2026-11-24 21:30 UTC 범위 고정 전에 205 인계와 선택 셀의 양성 및 기본 옵션의 음성 원로그를 읽었다. 당시 이 작업의 FITS 생성·모드별 결과와 SQLite 대조는 미실행이었다. 동결 뒤 추가하는 근거/통제는 모집표에서 표시한다.
