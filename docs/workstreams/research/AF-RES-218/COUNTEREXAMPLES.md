# AF-RES-218 반례와 판정 수정

## 같은 초기 FITS에서 관측한 반례

모든 표의 픽셀은 HDU 0의 인덱스 0이고 단위는 m/s다. 별도 사본마다 종료 후 새 reader를 실행했다. 원출력의 `before_flush_or_close`, `after_flush`, `after_hdul_close`, `after_writer_exit`로 시점을 구별한다. [R03 본시험](receipts/matrix.jsonl) · [R05 통제 원출력](receipts/controls.jsonl) · [통제 집계](receipts/controls.csv)

| 검토한 주장 | 반증 관측 | 적용되는 결론 |
| --- | --- | --- |
| writable이고 `shares_memory`가 참이면 기존 파일도 바뀐다 | `readonly`와 `copyonwrite` 16회 모두 HDU 0→99, 독립 reader의 원경로는 0.0이고 파일 지문도 기준과 같다. [R03 L1–16](receipts/matrix.jsonl#L1-L16) | 임시 메모리 링크에는 파일 모드와 재열람을 같이 안내한다. |
| 원경로의 새 값은 반드시 명시 flush나 close 뒤에 처음 보인다 | 매핑된 `update` 8회는 대입 직후 99.0. `memmap=False` 통제는 대입 직후 0.0, flush 뒤 99.0. [R03 L17–24](receipts/matrix.jsonl#L17-L24) · [R05 L4](receipts/controls.jsonl#L4) | 접근 방식이 가시성 시점에 관여한다. 새 reader는 그 단계에서 볼 수 있었던 값을 확인한다. |
| update에서 공유하는 Quantity를 수정하면 영속한다 | 깊은 사본에 붙인 Quantity는 사본과 공유하고 99.0을 읽었다. HDU는 0.0, update flush/close 뒤 원파일도 0.0과 기준 지문이다. [R05 L2](receipts/controls.jsonl#L2) | 동일한 원본의 저장소와 겹치는지를 확인한다. |
| 파일 SHA-256 변화로 목표 픽셀 변경을 판정할 수 있다 | HISTORY를 추가하자 전체 지문이 `00360841…`에서 `bfe4bea7…`로 바뀌었다. 헤더 지문은 `db2e6b4d… → eceaf2e4…`, 데이터 블록 지문 `70b35c3a…`과 픽셀 0.0은 그대로다. [R05 L5](receipts/controls.jsonl#L5) | 대상 위치와 단위, 원픽셀을 확인한다. 쓰기 없이 닫은 대조에서는 원파일 지문이 같았다. [R05 L3](receipts/controls.jsonl#L3) |
| 새 파일의 보존을 확인하면 원파일 수정도 입증된다 | copyonwrite에서 원배열을 바꿔 `export.fits`에 저장하면 새 경로는 99.0, 지문 `c7938189…`이다. 원경로는 0.0, 지문 `00360841…`이다. 이미 존재하는 경로에 `overwrite=False`는 `OSError`를 냈다. [R05 L1, L6](receipts/controls.jsonl#L1-L6) | 의도한 경로를 성공 조건에 포함한다. |
| 모든 영상에서 저장 픽셀 숫자와 물리값이 일치한다 | NASA VLA 예에는 `BITPIX=16`, `BSCALE=7.04625720812E-05`, `BZERO=2.18688869476`, `BUNIT=JY/BEAM`이 있다. Astropy의 공식 테스트는 같은 fixture의 raw `>i2`와 스케일된 `float32`를 구분한다. [F03 BSCALE/BZERO/BUNIT](https://fits.gsfc.nasa.gov/users_guide/users_guide/node102.html) · [A05 L632–637](https://github.com/astropy/astropy/blob/78cf5340ddf9fe9731906224a638c4888849c93f/astropy/io/fits/tests/test_image.py#L632-L637) | 별도 형식 사례의 원문 증거다. 이번 형식의 수치 판정은 무스케일 IEEE double에 한정한다. |

같은 파일과 버퍼를 썼으므로 닫기 직전 reader까지 +99가 항상 보인다는 경쟁 설명은 `FC-BUFFERED`에서 틀린다. 읽기 전용이 곧 `ndarray.flags.writeable=False`라는 설명은 이 환경의 `readonly` 실측에서 틀린다. 반면 상류의 ENOMEM 주입 테스트는 `readonly`에서 실제 읽기 전용 배열로 내려가는 경우를 제시한다. 이번 시험의 `readonly` 추천 조건에는 파일 매핑 지원과 실제 writeability를 둔다. [A01 L342–395](https://github.com/astropy/astropy/blob/78cf5340ddf9fe9731906224a638c4888849c93f/astropy/io/fits/file.py#L342-L395) · [A06 L1082–1111](https://github.com/astropy/astropy/blob/78cf5340ddf9fe9731906224a638c4888849c93f/astropy/io/fits/tests/test_core.py#L1082-L1111)

## 별도 분야의 두 커밋 사례

| 공식 사례와 합성 대조 | writer 응답과 재열람 | FITS로 가져올 원리와 경계 |
| --- | --- | --- |
| WAL에서 이미 열린 X와 새 연결. 상대가 갱신한 뒤 오래된 X를 writer로 올리는 두 번째 예도 같은 DB에서 재생했다. [D02 X/Y 예](https://www.sqlite.org/isolation.html#isolation_and_concurrency) | SQLite 3.53.1에서 writer COMMIT 반환 성공. X의 열린 read transaction은 0.0, 새 연결과 X의 새 트랜잭션은 99.0. 오래된 X의 쓰기 전환은 코드 517 `SQLITE_BUSY_SNAPSHOT`. [R06 SQL-WAL](receipts/sqlite-command.jsonl) | 관측자의 시작 경계를 기록한다. SQLite는 WAL에서 스냅샷을 정의하고 FITS의 묶음은 writer를 경계에서 멈춘 뒤 항상 새 reader를 열었다. |
| rollback journal `DELETE`에서 다른 reader가 살아 있는 동안 명시 COMMIT. [D01 §2.3](https://www.sqlite.org/lang_transaction.html#implicit_versus_explicit_transactions) | UPDATE 뒤 writer는 99.0을 읽었으나 첫 COMMIT은 코드 5 `SQLITE_BUSY`, 트랜잭션은 유지됐다. X가 끝난 뒤 재시도 성공, 신규 연결 99.0. [R06 SQL-DELETE](receipts/sqlite-command.jsonl) | 호출 종류와 ACK를 지정한다. FITS에서 flush가 경고하고 반환해도 재열람 값은 원값일 수 있다. SQLite의 journal·잠금·복구를 FITS 쓰기로 옮길 근거는 없다. [D03 §3.10–3.12](https://www.sqlite.org/atomiccommit.html#deleting_the_rollback_journal) · [D04 C API 반환](https://www.sqlite.org/c3ref/step.html) |

CFITSIO의 C 예는 새 영상의 헤더와 픽셀을 각각 명시적으로 쓰고 닫은 뒤 상태를 확인한다. 다른 라이브러리에서도 대상 경로·픽셀과 API 상태를 함께 기록할 수 있는 절차 예시다. 그 예에는 독립 reader와 동시 변경 조건의 관측이 없다. [F04 §2.6](https://heasarc.gsfc.nasa.gov/docs/software/fitsio/c/c_user/node17.html)

## 앞선 표현과 출처의 정정

| 이전 문구·예정 상태 | 고정 근거 | 갱신 |
| --- | --- | --- |
| ③ 표 3의 별도 산출물 마지막 단계는 미확인 | R05 L1의 독립 reader 두 경로와 파일 지문 | 새 파일 경로에서만 `99.0 m/s`가 보존됨을 채운다. |
| v6.0.1 검증 문서에서 `flush` 기본 `output_verify`를 `exception`으로 열거 | [A09 L64–69](https://github.com/astropy/astropy/blob/78cf5340ddf9fe9731906224a638c4888849c93f/docs/io/fits/usage/verification.rst#L64-L69) · [A02 L875, L1048](https://github.com/astropy/astropy/blob/78cf5340ddf9fe9731906224a638c4888849c93f/astropy/io/fits/hdu/hdulist.py#L874-L895) · [R09 설치판 함수 서명](receipts/signatures.jsonl) | 명시 `HDUList.flush()`는 `fix`, 기본 close가 호출하는 flush에는 `exception`이 전달된다. 올바른 고정 영상에서 양쪽 경계를 검사했다. 잘못된 FITS에 대한 결과는 미확인이다. |
| ③ 표 2의 종료 후 범위와 파일명 | R03 및 R05 | HDUList close 직후에도 배열 참조의 mmap은 열려 있었다. writer 종료 뒤 부모가 새 reader를 실행한 시점을 최종 판단으로 유지한다. |
