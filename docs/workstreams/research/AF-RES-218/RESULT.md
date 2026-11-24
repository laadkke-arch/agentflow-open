# AF-RES-218 · FITS 배열의 수정 전파와 재열람

| 205 셀·호출 | 고정 환경·출전 | 확인된 메모리 전파 | 파일 시험으로 남은 조건 |
| --- | --- | --- | --- |
| 표의 첫 Astropy 셀 `A01-A1`의 `false`. `u.Quantity(original, unit=u.Unit("m / s"), copy=False)`에서 `dtype` 생략, `output.value[0] = 99.0`. [P03 L127–149, L247–278](https://github.com/laadkke-arch/agentflow-open/blob/3853289f5189ad8af242c0f62d6cad566f31bc66/docs/workstreams/research/AF-RES-205/probe.py#L247-L278) · [P07 L18](https://github.com/laadkke-arch/agentflow-open/blob/3853289f5189ad8af242c0f62d6cad566f31bc66/docs/workstreams/research/AF-RES-205/matrix.csv#L18) | Linux x86_64, CPython 3.11.15, NumPy 1.26.4, Astropy 6.0.1 W03 SHA-256 `2c00922548a666b026e2630a563090341d74c8222066e9c84c9673395bca7363`. [P04 L1–6](https://github.com/laadkke-arch/agentflow-open/blob/3853289f5189ad8af242c0f62d6cad566f31bc66/docs/workstreams/research/AF-RES-205/receipts/A01/requirements.lock#L1-L6) · [P09 wheel JSON](https://pypi.org/pypi/astropy/6.0.1/json) | 두 false writer의 같은 가변 원배열에서 `0.0 → 99.0`, shares_memory true, 출력 `m / s`, 종료 0. 원래 ndarray는 unit 속성이 없다. [P02 L3–4](https://github.com/laadkke-arch/agentflow-open/blob/3853289f5189ad8af242c0f62d6cad566f31bc66/docs/workstreams/research/AF-RES-205/receipts/A01/runs.jsonl#L3-L4) | FITS의 `>f8`과 `BUNIT`, 파일 매핑 모드 및 같은 경로의 독립 reader가 바뀐 픽셀을 언제 보는지를 추가 검사했다. [R01 기준 reader](receipts/baseline-reader.json) |

| FITS 모드·저장 경계 | 메모리·HDU 값 | 원경로 재열람 값·단위 | 새 파일 값·지문 | 반복·원로그 | 미확인 |
| --- | --- | --- | --- | --- | --- |
| readonly · 직접/Quantity · 기본 close | 각각 HDU 0→99, 공유·쓰기 가능 `>f8` | 쓰기 직후 → HDU close 뒤 → writer 종료 뒤 모두 0.0 m/s, 원본 바이트 그대로 | 해당 경로에서 생성 계획 없음 | 4/4 [R03 L1–2, 5–6](receipts/matrix.jsonl#L1-L6) | 다른 플랫폼의 fallback |
| readonly · 직접/Quantity · flush 뒤 close | 각각 HDU 0→99, 공유·쓰기 가능 `>f8` | 쓰기 직후 → flush 뒤 → close 뒤 → writer 종료 뒤 모두 0.0 m/s, 원본 바이트 그대로 | 해당 경로에서 생성 계획 없음 | 4/4 [R03 L3–4, 7–8](receipts/matrix.jsonl#L3-L8) | flush는 지원하지 않는다는 경고 후 반환 |
| copyonwrite · 직접/Quantity · 기본 close | 각각 HDU 0→99, 공유·쓰기 가능 `>f8` | 쓰기 직후 → close 뒤 → writer 종료 뒤 모두 0.0 m/s, 원본 바이트 그대로 | 해당 경로에서 생성 계획 없음 | 4/4 [R03 L9–10, 13–14](receipts/matrix.jsonl#L9-L14) | 압축 파일 |
| copyonwrite · 직접/Quantity · flush 뒤 close | 각각 HDU 0→99, 공유·쓰기 가능 `>f8` | 쓰기 직후 → flush 뒤 → close 뒤 → writer 종료 뒤 모두 0.0 m/s, 원본 바이트 그대로 | 해당 경로에서 생성 계획 없음 | 4/4 [R03 L11–12, 15–16](receipts/matrix.jsonl#L11-L16) | flush는 지원하지 않는다는 경고 후 반환 |
| update · 직접/Quantity · 기본 close | 각각 HDU 0→99, 공유·쓰기 가능 `>f8` | 쓰기 직후 → close 뒤 → writer 종료 뒤 모두 99.0 m/s, 대상 픽셀 바이트만 변경 | 해당 경로에서 생성 계획 없음 | 4/4 [R03 L17–18, 21–22](receipts/matrix.jsonl#L17-L22) | 파일 잠금·동시성, 장애 복구 |
| update · 직접/Quantity · flush 뒤 close | 각각 HDU 0→99, 공유·쓰기 가능 `>f8` | 쓰기 직후 → flush 뒤 → close 뒤 → writer 종료 뒤 모두 99.0 m/s, 대상 픽셀 바이트만 변경 | 해당 경로에서 생성 계획 없음 | 4/4 [R03 L19–20, 23–24](receipts/matrix.jsonl#L19-L24) | 파일 잠금·동시성, 장애 복구 |

| 개발 목적 | 안내할 원문 | 보장되는 마지막 단계 | 반례·예외 | 갱신할 근거 |
| --- | --- | --- | --- | --- |
| 임시 메모리 작업 | [P10 Quantity L423–465](https://github.com/astropy/astropy/blob/78cf5340ddf9fe9731906224a638c4888849c93f/astropy/units/quantity.py#L423-L465) · [A01 매핑 모드 L78–95](https://github.com/astropy/astropy/blob/78cf5340ddf9fe9731906224a638c4888849c93f/astropy/io/fits/file.py#L78-L95) | 지정 호출과 fixture에서 같은 HDU 배열에 반영 | dtype·단위 변환, readonly 매핑 fallback | 변환을 쓰는 호출의 dtype·원본 전후값 |
| 같은 경로 수정 | [A07 Save File Changes L620–646](https://github.com/astropy/astropy/blob/78cf5340ddf9fe9731906224a638c4888849c93f/docs/io/fits/index.rst#L620-L646) · [A02 flush/close L875–897, L1067–1080](https://github.com/astropy/astropy/blob/78cf5340ddf9fe9731906224a638c4888849c93f/astropy/io/fits/hdu/hdulist.py#L1067-L1080) | update writer 종료 뒤 별도 reader에서 같은 HDU·픽셀·단위 확인 | 비공개 매핑에서 메모리 수정만 전파, 동시성 미확인 | 다른 파일시스템·스케일·동시 writer |
| 별도 산출물 | [A02 writeto L974–1000](https://github.com/astropy/astropy/blob/78cf5340ddf9fe9731906224a638c4888849c93f/astropy/io/fits/hdu/hdulist.py#L974-L1000) · [A07 Save File Changes L620–634](https://github.com/astropy/astropy/blob/78cf5340ddf9fe9731906224a638c4888849c93f/docs/io/fits/index.rst#L620-L634) | 미확인. 새 경로/원경로 대조 통제 예정 | overwrite 기본값 False | 별도 reader 두 경로 원영수증 |

주시험 24/24. 실행 번호, 쓰기 전후값, 원픽셀 바이트, reader PID와 종료코드는 [R03 원로그](receipts/matrix.jsonl)와 [집계 CSV](persistence.csv)에 있다. 별도 FITS·SQLite 통제 및 Q1–Q7 분석은 다음 묶음에서 채운다.
