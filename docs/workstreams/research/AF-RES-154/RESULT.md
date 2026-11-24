# AF-RES-154 Paperless-ngx v2.2.1 서명 PDF 입고와 원본 회수

| 요구와 제안된 링크 | 작성자 구절·주소 | 해당 판의 실제 보증 구간 | 필요한 선행 조건 | 미확인 |
| --- | --- | --- | --- | --- |
| 입고·내부 원본 보관 / P01 | “Just import it.” [#5215 본문](https://github.com/paperless-ngx/paperless-ngx/issues/5215#issue-2063137483) | 성공한 소비 작업이 제공 사본의 바이트를 media의 원본으로 쓰고 행을 만든다. 성공 10/10에서 내부 원본 해시가 일치했다. [v2.2.1 사용법](https://github.com/paperless-ngx/paperless-ngx/blob/a7ac71971162838b8b1ee9e3b431543e69618e21/docs/usage.md#L45-L103) | 형식·중복 검사를 통과하고 파싱·저장이 완료되어야 한다. | 작성자 AWS PDF와 업로드 경로의 바이트·잔존은 미확인이다. |
| 변경 없는 명시 원본 회수 / P04 | “Do not try to alter/OCR the PDF.” [#5215 본문](https://github.com/paperless-ngx/paperless-ngx/issues/5215#issue-2063137483) | 성공 10/10에서 `original=true` 응답이 입력과 바이트 동일했다. 기본 응답은 실측 4/10에서 아카이브를 반환했다. [v2.2.1 REST 계약](https://github.com/paperless-ngx/paperless-ngx/blob/a7ac71971162838b8b1ee9e3b431543e69618e21/docs/api.md#L61-L90) | 정상 작업 종료·유효한 레코드 ID·파일 존재·다운로드 권한. 아카이브가 있으면 원본을 명시한다. | 다른 권한·HTTP UI·스토리지 조합은 미시험이다. |
| 입고 전후 바이트 대조 / L01 | 변경 금지를 해시·길이 대조로 관측했다. [#5215 본문](https://github.com/paperless-ngx/paperless-ngx/issues/5215#issue-2063137483) | L01은 수신 파일을 사전 지문과 비교하는 원리다. 성공 응답에서 해시와 실제 바이트를 대조했다. [BagIt 0.97 §2.1.3](https://digitalpreservation.gov/documents/bagitspec.pdf#page=7) | 제출 전 제공자로부터 고정한 입력과 지문이 필요하다. 묶음에서는 기대 목록과 각 경로·지문을 확보한다. | 단일 해시로 내부 서명 신뢰, 외부 속성·최초 경로·누락 동반 파일은 미확인이다. |
| 무 OCR / 세 링크 밖 파서 분기 | “skip the OCR step.” [#5215 본문](https://github.com/paperless-ngx/paperless-ngx/issues/5215#issue-2063137483) | `always`의 ST 두 건에서 래퍼·인식 각 0과 조기 반환 로그를 확인했다. SI 두 건은 래퍼 2회씩 호출 후 실패했다. [고정 파서](https://github.com/paperless-ngx/paperless-ngx/blob/a7ac71971162838b8b1ee9e3b431543e69618e21/src/paperless_tesseract/parsers.py#L284-L338) | 이 판에서 파서가 추출하는 문자열 길이 >50과 지원되는 archive 생략 분기, 정상 입고. | 짧은·혼합 페이지, 다른 서명 유형·추출기에서 동일 입력 경계는 미시험이다. |
| 저장 실패를 뚜렷하게 알림 / 세 링크 밖 작업 상태·알림 | “the file will not be stored” [#5215 본문](https://github.com/paperless-ngx/paperless-ngx/issues/5215#issue-2063137483) | 파싱과 쓰기 실패의 원인·파일명 및 큐 `FAILURE`가 기록됐다. 서명 거절 로그에 미저장 및 재시도 가능 여부를 명시한 문장은 없었다. 저장 단계의 EACCES는 별도 메시지에서 식별됐다. [고정 consumer](https://github.com/paperless-ngx/paperless-ngx/blob/a7ac71971162838b8b1ee9e3b431543e69618e21/src/documents/consumer.py#L473-L585) | 파일명·작업 ID에 대한 종료 상태 관찰, 명시적 미저장 표시와 정상 사본의 대기·재시도 절차. | 운영자 메시지 전달, UI 문구, 원본 저장 뒤의 늦은 장애와 삭제·충돌은 미시험이다. |
| PDF 서명 무결성·수신자 신뢰 | 서명 파일을 수정 없이 들이는 목표에서 파생한 관측값이다. [#5215 본문](https://github.com/paperless-ngx/paperless-ngx/issues/5215#issue-2063137483) | A의 ST 원본·기본 반환 모두 전체 서명 범위의 무결성 유지. 시험 루트가 있는 검증에서 신뢰, 앵커 0에서는 미신뢰. [검증 영수증](evidence/runtime/R1-A/R1-A-ST/receipt.json) | 수신자는 별도 검증 시각·신뢰점·인증서 정책을 정한다. | 실제 작성자 파일의 인증서 체인·타임스탬프·폐기 상태는 미확인이다. |
| 제공자 위치와 소비 폴더 / P01 적용 경계 | 최초 위치 유지는 146에서 별도 가정이었다. [146 P-A 원장](https://github.com/laadkke-arch/agentflow-open/blob/9bf267b71a0000aae5f098e82eab3f84c0dd7714/docs/workstreams/research/AF-RES-146/requests.jsonl#L3) | 성공 소비 경로는 10/10 정리됐다. 별도 제공자 사본은 모든 본 실험에서 유지됐다. [소비 폴더 안내](https://github.com/paperless-ngx/paperless-ngx/blob/a7ac71971162838b8b1ee9e3b431543e69618e21/docs/usage.md#L76-L102) | 최초 위치가 필요하면 제공자 사본과 별개로 소비 폴더에 복제한다. | 작성자 파일 최초 경로와 관리 속성은 미확인이다. |
| 단위·전체 분모·결측 | 고정 카드 3개와 연계 관측 4행. 원저자 요구 4가지 | 입고 16, 성공 10, 다운로드 20회. 별도 권한·재시도 6회와 서명 옵트인 1회 | 이 표에서 원본 보관·회수의 성공 분모는 10건 | 저자 인보이스·신뢰·전체 앱 채널 미시험. 실패 6건의 다운로드는 해당 없음 |

| 입력·판·설정·반복 | 입고·로그 | 래퍼·실제 OCR 호출 | 원본·기본 반환 해시 | 서명 무결성·신뢰 | 실패·재시도·문서 수 |
| --- | --- | --- | --- | --- | --- |
| [R1-D-UT](evidence/runtime/R1-D/R1-D-UT/receipt.json) · UT · 2.2.1 | 큐 등록·SUCCESS·성공 | 1/0 | 원 1,638 B · `c39c75994e7e4f8fbc504e7a587aca7cf576432e2012e2bc1bc382085ebe0987`<br>기 7,784 B · `f7120be070b73ef37e2ce6b10a39adffa6b467280b75c263e1912f5177a65416` | 미서명 입력 | 소비 사본 제거 · DB 0→1 |
| [R1-D-UI](evidence/runtime/R1-D/R1-D-UI/receipt.json) · UI · 2.2.1 | 큐 등록·SUCCESS·성공 | 1/1 | 원 59,137 B · `e0b00798334335e3e59b23be9f98421a94594ebeff2414aae387e6d7892bcc01`<br>기 132,041 B · `c9e5cbf0bf317f3acba6d91f616419050c3b871786043845168e8281e9b2b798` | 미서명 입력 | 소비 사본 제거 · DB 1→2 |
| [R1-D-ST](evidence/runtime/R1-D/R1-D-ST/receipt.json) · ST · 2.2.1 | 큐 등록·FAILURE·서명 감지 실패 | 2/0 | 해당 없음 (문서 ID 미생성) | 입고 전 무결성 통과, 반환 해당 없음. 통제 CA 신뢰·앵커 0 미신뢰 | 소비 사본 잔존 · DB 2→2 |
| [R1-D-SI](evidence/runtime/R1-D/R1-D-SI/receipt.json) · SI · 2.2.1 | 큐 등록·FAILURE·서명 감지 실패 | 2/0 | 해당 없음 (문서 ID 미생성) | 입고 전 무결성 통과, 반환 해당 없음. 통제 CA 신뢰·앵커 0 미신뢰 | 소비 사본 잔존 · DB 2→2 |
| [R1-A-UT](evidence/runtime/R1-A/R1-A-UT/receipt.json) · UT · 2.2.1 | 큐 등록·SUCCESS·성공 | 0/0 | 원·기 1,638 B · `c39c75994e7e4f8fbc504e7a587aca7cf576432e2012e2bc1bc382085ebe0987` | 미서명 입력 | 소비 사본 제거 · DB 0→1 |
| [R1-A-UI](evidence/runtime/R1-A/R1-A-UI/receipt.json) · UI · 2.2.1 | 큐 등록·SUCCESS·성공 | 1/1 | 원·기 59,137 B · `e0b00798334335e3e59b23be9f98421a94594ebeff2414aae387e6d7892bcc01` | 미서명 입력 | 소비 사본 제거 · DB 1→2 |
| [R1-A-ST](evidence/runtime/R1-A/R1-A-ST/receipt.json) · ST · 2.2.1 | 큐 등록·SUCCESS·성공 | 0/0 | 원·기 9,892 B · `599a541e92dee51d8710a00f2ffd0bfbd03bfb2a59cbc6a2a70567bc7eda7984` | 두 반환 모두 전 범위 무결성. 통제 CA 신뢰·앵커 0 미신뢰 | 소비 사본 제거 · DB 2→3 |
| [R1-A-SI](evidence/runtime/R1-A/R1-A-SI/receipt.json) · SI · 2.2.1 | 큐 등록·FAILURE·서명 감지 실패 | 2/0 | 해당 없음 (문서 ID 미생성) | 입고 전 무결성 통과, 반환 해당 없음. 통제 CA 신뢰·앵커 0 미신뢰 | 소비 사본 잔존 · DB 3→3 |
| [R2-D-UT](evidence/runtime/R2-D/R2-D-UT/receipt.json) · UT · 2.2.1 | 큐 등록·SUCCESS·성공 | 1/0 | 원 1,638 B · `c39c75994e7e4f8fbc504e7a587aca7cf576432e2012e2bc1bc382085ebe0987`<br>기 7,784 B · `9563c5ab25be949cb1aed664dcd2f32496b5db531f63a10e6522d08296fb04f8` | 미서명 입력 | 소비 사본 제거 · DB 0→1 |
| [R2-D-UI](evidence/runtime/R2-D/R2-D-UI/receipt.json) · UI · 2.2.1 | 큐 등록·SUCCESS·성공 | 1/1 | 원 59,137 B · `e0b00798334335e3e59b23be9f98421a94594ebeff2414aae387e6d7892bcc01`<br>기 132,041 B · `53b3d4a70ab32df1562f572a68534ef2e5ab41639689e5ed89c98e75253b93ea` | 미서명 입력 | 소비 사본 제거 · DB 1→2 |
| [R2-D-ST](evidence/runtime/R2-D/R2-D-ST/receipt.json) · ST · 2.2.1 | 큐 등록·FAILURE·서명 감지 실패 | 2/0 | 해당 없음 (문서 ID 미생성) | 입고 전 무결성 통과, 반환 해당 없음. 통제 CA 신뢰·앵커 0 미신뢰 | 소비 사본 잔존 · DB 2→2 |
| [R2-D-SI](evidence/runtime/R2-D/R2-D-SI/receipt.json) · SI · 2.2.1 | 큐 등록·FAILURE·서명 감지 실패 | 2/0 | 해당 없음 (문서 ID 미생성) | 입고 전 무결성 통과, 반환 해당 없음. 통제 CA 신뢰·앵커 0 미신뢰 | 소비 사본 잔존 · DB 2→2 |
| [R2-A-UT](evidence/runtime/R2-A/R2-A-UT/receipt.json) · UT · 2.2.1 | 큐 등록·SUCCESS·성공 | 0/0 | 원·기 1,638 B · `c39c75994e7e4f8fbc504e7a587aca7cf576432e2012e2bc1bc382085ebe0987` | 미서명 입력 | 소비 사본 제거 · DB 0→1 |
| [R2-A-UI](evidence/runtime/R2-A/R2-A-UI/receipt.json) · UI · 2.2.1 | 큐 등록·SUCCESS·성공 | 1/1 | 원·기 59,137 B · `e0b00798334335e3e59b23be9f98421a94594ebeff2414aae387e6d7892bcc01` | 미서명 입력 | 소비 사본 제거 · DB 1→2 |
| [R2-A-ST](evidence/runtime/R2-A/R2-A-ST/receipt.json) · ST · 2.2.1 | 큐 등록·SUCCESS·성공 | 0/0 | 원·기 9,892 B · `599a541e92dee51d8710a00f2ffd0bfbd03bfb2a59cbc6a2a70567bc7eda7984` | 두 반환 모두 전 범위 무결성. 통제 CA 신뢰·앵커 0 미신뢰 | 소비 사본 제거 · DB 2→3 |
| [R2-A-SI](evidence/runtime/R2-A/R2-A-SI/receipt.json) · SI · 2.2.1 | 큐 등록·FAILURE·서명 감지 실패 | 2/0 | 해당 없음 (문서 ID 미생성) | 입고 전 무결성 통과, 반환 해당 없음. 통제 CA 신뢰·앵커 0 미신뢰 | 소비 사본 잔존 · DB 3→3 |
| [R1-A-W](evidence/runtime/R1-A/R1-A-W/receipt.json) · WT · 2.2.1 | 큐 등록·FAILURE·EACCES 저장 실패 | 0/0 | 해당 없음 (문서 ID 미생성) | 미서명 입력 | 권한 금지·잔존 · DB 3→3 |
| [R1-A-R](evidence/runtime/R1-A/R1-A-R/receipt.json) · WT · 2.2.1 | 큐 등록·SUCCESS·성공 | 0/0 | 원·기 1,640 B · `0d548f067947e07c7bd00f92174f796251467a6bad4eafe9a0743afe57261ea6` | 미서명 입력 | 권한 복구 후 동일 바이트·제거 · DB 3→4 |
| [R1-A-DUP](evidence/runtime/R1-A/R1-A-DUP/receipt.json) · WT · 2.2.1 | 큐 등록·FAILURE·중복 거절 | 0/0 | 해당 없음 (문서 ID 미생성) | 미서명 입력 | 동일 바이트 중복·잔존 · DB 4→4 |
| [R2-A-W](evidence/runtime/R2-A/R2-A-W/receipt.json) · WT · 2.2.1 | 큐 등록·FAILURE·EACCES 저장 실패 | 0/0 | 해당 없음 (문서 ID 미생성) | 미서명 입력 | 권한 금지·잔존 · DB 3→3 |
| [R2-A-R](evidence/runtime/R2-A/R2-A-R/receipt.json) · WT · 2.2.1 | 큐 등록·SUCCESS·성공 | 0/0 | 원·기 1,640 B · `0d548f067947e07c7bd00f92174f796251467a6bad4eafe9a0743afe57261ea6` | 미서명 입력 | 권한 복구 후 동일 바이트·제거 · DB 3→4 |
| [R2-A-DUP](evidence/runtime/R2-A/R2-A-DUP/receipt.json) · WT · 2.2.1 | 큐 등록·FAILURE·중복 거절 | 0/0 | 해당 없음 (문서 ID 미생성) | 미서명 입력 | 동일 바이트 중복·잔존 · DB 4→4 |
| [S1-X-SI](evidence/runtime/S1-X/S1-X-SI/receipt.json) · SI · 2.2.1 | 큐 등록·SUCCESS·성공 | 1/1 | 원 67,456 B · `7f24f7610dca85a6909916e061f5990c656d8c0df9fdd1c6a36d6c95252e3341`<br>기 132,042 B · `8c14fbb09481eae06189d6defc5bda1a00d87de1483944f53beb8ea0e3cbea95` | 원본 전 범위 무결성, 통제 CA 신뢰·앵커 0 미신뢰. 기본 서명 0 | 소비 사본 제거 · DB 0→1 |
| 단위·전체 분모·결측 | 예정·실시 16/16, 성공 10·실패 6. 보조 7/7, 성공 3·실패 4. X의 기동 중단 1건은 미입고 | 본 실험 호출 18/4, 보조 1/1. 툴 조회·방향·보정은 별도 | 주 결과 20회 HTTP 200. 성공 10건에서 원본 10/10, 기본 6/10 일치. 실패 6건 응답 해당 없음. 보조 6회 200 | 서명 입력 본 8건 중 성공 2건, 반환 4개 무결성 확인. 실패 반환 분모 0 | 예정·실시 입고 결측 0/16. 권한 실패 2·재입고 성공 2·중복 2, 별도 옵트인 성공 1. 측정 범위는 단일 호스트 |

| 결합 조건 | 성립한 작성자 요구 | 깨진 조건·반례 주소 | 답에 쓸 문장 | 근거 실행 ID | 측정 비용·미측정 |
| --- | --- | --- | --- | --- | --- |
| A + 유효 서명 + 충분한 추출 텍스트 | 입고·원본 동일·래퍼 0·인식 0. 원본 및 기본 반환에서 전체 서명 무결성 유지 | 신뢰 앵커 0에서 미신뢰. 입고 성공의 실패 로그는 해당 없음. [서명·응답 영수증](evidence/runtime/R1-A/R1-A-ST/receipt.json) | **직접 관측** v2.2.1에서 이 서명 텍스트 PDF는 `always`로 OCRmyPDF 호출 없이 입고됐고 `original=true`의 바이트와 서명 무결성이 유지됐다. | R1-A-ST, R2-A-ST | 처리 1.718·1.577초. 수신자 실제 신뢰·법적 검증 미측정 |
| D + ST/SI, A + SI | 입력 소비 사본은 해당 실패에서 잔존했다 | 등록 0/6, 반환 요청 분모 0/6, 래퍼 각 2회·인식 0. 서명 감지 예외는 저장 전에 발생했다. [D/ST 실패 로그](evidence/runtime/R1-D/R1-D-ST/paperless.log) [A/SI 실패 로그](evidence/runtime/R1-A/R1-A-SI/paperless.log) | **직접 관측** 기본값에서 두 유효 서명 유형은 모두 입고에 실패했다. `always`에서도 서명된 이미지 전용 PDF는 이 파일에서 등록되지 않았다. | R1/2-D-ST, R1/2-D-SI, R1/2-A-SI | 처리 1.034–2.502초. 실패 다운로드는 해당 없음 |
| D + 미서명 텍스트 / A + 미서명 이미지 | 각각 명시 원본 바이트 보존 | D/UT 래퍼 1·인식 0·PDF/A 파생 반환. A/UI는 두 응답 동일·영구 파생 없음·실제 인식 1. [D/UT](evidence/runtime/R1-D/R1-D-UT/receipt.json) [A/UI](evidence/runtime/R1-A/R1-A-UI/receipt.json) | **직접 관측** 원본 응답이 입력과 같아도 OCRmyPDF 호출과 실제 인식은 각각 일어날 수 있다. | R1/2-D-UT, R1/2-A-UI | 처리 1.891–5.052초. 호스트 CPU 미측정 |
| X + 삽입 서명 SI + 파생 변환 허용 | 입고와 명시 원본 일치, 명시 원본 전체 서명 무결성 유지 | 실제 인식 1, 기본 반환 PDF/A의 서명 필드 0. [X 영수증](evidence/runtime/S1-X/S1-X-SI/receipt.json) [유지보수자 비교](https://github.com/paperless-ngx/paperless-ngx/discussions/5986) | **조건부 안내** 접근 사본에 OCR을 허용한다면 이 판과 입력에서 원본을 명시 회수할 수 있었다. 기본 응답에는 시험 서명 객체가 없었다. | S1-X-SI | 처리 5.204초·다운로드 2회. 기본/대체보다 별도 비교 1회 |
| 원본 저장 경로 EACCES → 권한 복구 → 동일 바이트 재입고·중복 | 실패 단계·원인·작업의 종료 로그. 복구 시 원본 일치와 문서 1개 증가 | 일반적인 미저장 문구/파일 회수 안내는 없었다. 중복만 명시적 거절 및 기존 ID를 남겼다. [실패·재시도 파일 기록](evidence/runtime/R1-A/write-retry.json) | **조건부 안내** 작업 `FAILURE`와 저장 원인으로 경보를 만들고, 미저장 사실과 복구할 사본을 명시하는 통지가 실제로 전달되는지 확인한다. | R1/2-A-W, R1/2-A-R, R1/2-A-DUP | 반복당 3회, 처리 합 3.742·3.556초. 외부 경보 전달 미측정 |
| A 소유자 원본 + P01·P04·L01 + 외부 상태 확인 | 성공 입고 뒤의 원본 일치와 재검증 경로를 연결할 수 있다 | 동일 바이트인 파일이 있어도 묶음의 동반 파일 누락, 원경로 변경, 수신자 미신뢰가 가능하다. [BagIt·렌더 검산](evidence/controls/bag-and-render.json) | **추가 확인** 이 파일의 텍스트 추출 분기와 회수 지문을 먼저 확인한다. 실패에서 미저장·사본 위치·재처리를 알리는 경로를 따로 입증해야 세 조건을 함께 약속할 수 있다. | R1/2-A-ST, R1/2-A-W, BagIt 검산 | 외부 운영 구현 비용·실제 입력 검증 비용 미측정 |
| 단위·전체 분모·결측 | 본 실험 결합 16건, 서명 8건, 엄격한 성공 경로 2건 | D에서 서명된 성공 경로 0/4. 원요구 전체의 시스템 보증을 승인한 조합 0. 선택 입력 범위 밖은 미확인 | 응답 문장은 관측된 지원 판·조건을 붙인다 | 본 16, 재시도 대조 6, X 1. X의 선행 기동 중단 1회는 입고 분모 밖 | 준비·처리·검증 비용은 분리했다. 운영 경보·다중 호스트·실제 인보이스는 미측정 |

## Q1. 작성자의 성공 기준

146의 P-A 요청·전환·전수표에서 P01 5위, P04 7위, L01 8위와 조건부 판정을 재사용했다. GitHub가 반환한 #5215 본문은 110행이다. 본문 앞부분의 Description과 Expected behaviour가 입고·무변형·무 OCR·실패 로그 요구의 위치다. 현 본문의 원 CRLF 지문 `f45ab39c…`과 LF 정규화 지문 `048c9105…`는 146의 두 지문과 각각 일치했다. 발행일은 2024-01-03이고 이 비교로 중간 편집 이력은 알 수 없다. 2024-01-03 저자의 아카이브 변형 허용 댓글과 #5542는 최초 요구의 별도 후속이다. #4705의 설정 적용, #5986의 유지보수자 원본 해시, #6637의 별도 이전 판 실패, #8124의 후대 신고를 각각 대조했다. 실제 AWS PDF와 당시 비기본 설정은 공개 근거에서 확인되지 않았다. [원문 지문 E01과 사건 E02–E06](sources.jsonl) [저자 댓글](https://github.com/paperless-ngx/paperless-ngx/issues/5215#issuecomment-1875261885)

## Q2. 감시·파서·엔진·저장·응답

소비 폴더 `MOVED_TO` → watcher의 큐 등록 → Celery `consume_file` → 소비 사본과 작업 사본 생성 → 추출/파싱 → thumbnail → DB 및 원본·선택 파생 저장 → 소비 파일 정리 → 다운로드 순서다. 파서 앞에서 기존 텍스트를 추출하고 텍스트가 충분한 A 조건에서 반환한다. OCRmyPDF 15.4.4는 `AcroForm.SigFlags` 비트를 검사하며 이 신호는 PDF의 암호학적 검증과 별개다. 게이트가 막는 경우 primary와 force fallback이 호출될 수 있다. 두 호출은 서명 오류 때문에 실제 인식 실행 전 멈췄다. 패키지 잠금과 Linux/amd64 공식 이미지의 코드 레이블·실제 패키지 버전을 맞췄다. [고정 소스 X02–X04·X09](sources.jsonl) [실행판](evidence/runtime/platform.json)

호출은 파서 로그와 Tesseract 인수·종료값으로 관측했다. 4회 인식은 각각 exit 0과 인덱스 텍스트로 확인했다. `other` 8회는 이미지 경로의 `--psm 2` deskew 호출이다. 기동 점검의 probe는 각 인스턴스에서 관측됐고 본 실험 계수에서는 제외했다. A의 UI에도 OCRmyPDF가 임시 PDF/A 출력을 보고했다. 이후 미디어/DB에 영구 파생이 없었으며 기본 응답의 페이지는 텍스트가 없고 인덱스에는 인식 텍스트가 있었다. PDF/A 출력 로그는 OCRmyPDF 자체의 보고다. 별도 적합성 검증은 수행하지 않았다. [엔진 추적](evidence/runtime/R1-A/R1-A-UI/tesseract.tsv) [제품 stdout/stderr](evidence/runtime/R1-A/container.stderr) [OCRmyPDF 출력 점검](https://github.com/ocrmypdf/OCRmyPDF/blob/c90d5cd84b0e27906310c28f0d78c3ded9106d65/src/ocrmypdf/_pipelines/_common.py#L430-L454)

Paperless의 공개 회귀 `test_signed`는 성공 파싱을 기대한다. 공식 이미지에서 동일 공개 파일을 parser 층으로 재생하니 기본 archive `never`의 parser는 암호화 격리 경고 후 텍스트 135자를 반환했다. 공개 샘플은 SigFlags 3과 유효한 전체 서명이 있고 PDF 권한에서 AES 암호화가 확인됐다. `always`에서도 텍스트 135자를 반환했다. 이 회귀는 서명과 별개인 암호화 예외 경로를 보여 준다. OCRmyPDF의 별도 단위시험은 실제 암호학적 서명 대신 SigFlags를 설정하고 기본 거부를 기대한다. 둘 다 소비 폴더·DB·HTTP의 end-to-end 성공에 대한 단위시험은 아니다. [샘플 구조·검사](evidence/controls/upstream-signed-pdf.txt) [never stdout](evidence/controls/upstream-parser-never.stdout) [never stderr](evidence/controls/upstream-parser-never.stderr) [T01·T02](sources.jsonl)

## Q3. 검증 가능한 입력

UT/ST의 1페이지 텍스트는 Poppler 추출 165자다. UI/SI의 한 페이지는 같은 내용의 래스터 이미지이며 기존 추출 텍스트가 0자다. Pillow의 내장 글꼴과 ReportLab을 쓰고 pyHanko로 두 PDF에 증분 CMS 서명을 넣었다. 두 서명 입력의 `ENTIRE_FILE`, 내용 무결성, CMS 유효성 및 로컬 루트 신뢰를 입고 전에 관측했다. 신뢰점 0의 문맥에서는 같은 서명 바이트가 미신뢰였다. 검증 문맥의 시간은 고정 입력 폴더의 UTC 파일로 기록했다. 공개 인증서와 고정 바이트만 커밋했다. 작동 증거는 가상 저자·가상 문서로부터 얻었다. [입력 원장](fixtures.jsonl) [재생법](replay/README.md)

ST의 서명 범위에 포함된 Title 한 바이트를 `A`에서 `B`로 바꾼 대조는 9,892바이트로 길이와 렌더링 픽셀 해시가 같았다. 파일 해시는 달라지고 양쪽 신뢰 설정에서 `intact=false`가 됐다. `pdfsig -nocert`의 문구는 Digest Mismatch였으나 종료 코드는 0이었다. CMS 객체에 대한 `valid`와 PDF 내용에 대한 `intact`를 동시에 확인해야 한다. [렌더링·서명 대조](evidence/controls/bag-and-render.json)

## Q4. 정상 입고와 회수

두 반복의 D/A는 각각 빈 SQLite와 Redis 및 새 media/consume으로 시작했다. 보존한 호스트 제공 사본을 복제해 같은 watcher와 기본 Celery 경로로 보냈다. 성공 10/16, 실패 6/16이었다. 모두 큐 종료, DB 변화 유무, 소비 사본 잔존을 확인했다. 명시 원본은 10/10 일치했다. 기본 다운로드는 A에서 6/6 일치하고 D의 성공 4/4는 다른 PDF/A 바이트였다. 서명된 주 입력은 A의 ST만 2/2 성공했다. 기본 설정이 서명 입력의 입고·원본·무 OCR을 함께 만족한 셀은 네 건 중 0이었다. SHA-256·바이트 수·페이지 텍스트·`pdfsig` 출력·신뢰 프로필은 응답 영수증에 있다. D의 파생본은 두 반복 사이에 해시가 바뀌었다. 같은 정규화 분기에서 원본 해시가 안정적이어도 파생 바이트를 새로운 입고의 고정 정답으로 삼을 수 없다. [실행 원장](runs.jsonl)

## Q5. 실패·재입고·중복

본 실험의 서명 실패 6건에서 파일명과 원인이 기록됐고 DB는 증가하지 않았다. 소비 경로에서 입력 해시가 일치하는 파일이 남았고 제공자 사본도 남았다. 최초 작성자의 업로드는 이 watcher 실험과 다른 입구다. 앱에 나타나지 않은 일과 사용자 원본의 물리적 삭제를 같은 사건으로 판정할 수 없다. [D/SI 영수증](evidence/runtime/R2-D/R2-D-SI/receipt.json) [#5215 업로드 절](https://github.com/paperless-ngx/paperless-ngx/issues/5215#issue-2063137483)

쓰기 대조에서 각 A의 originals 디렉터리가 paperless 계정에 쓰기 불가인 것을 확인했다. 파싱 뒤 원본 저장에서 EACCES로 실패했고 적재 문서 수 3→3, 기존 원본 목록 유지, 별도 소비 사본의 동일 SHA-256 잔존을 관측했다. 권한 복구 후 같은 바이트를 새 소비 이벤트로 투입하면 3→4가 됐다. 그 뒤 동일 바이트 재투입은 기존 레코드 #4를 가리키는 의도된 중복 거절로 4→4, 대기 사본 잔존이었다. 실패 사본 자체는 명시적 재입고가 끝난 뒤에도 소비 폴더에 남았다. 실제 recovery는 동일 바이트의 새 이벤트로 확인했으며 실패 파일의 자동 재전송은 관측하지 않았다. 서명 실패 로그와 EACCES 로그는 운영자가 원인·실패 단계를 알 수 있게 했지만, 원 작성자가 요구한 미저장·손실 위험의 분명한 통지까지 입증하지 못했다. [R1 권한/파일](evidence/runtime/R1-A/write-retry.json) [R2 권한/파일](evidence/runtime/R2-A/write-retry.json) [R1 저장 오류](evidence/runtime/R1-A/R1-A-W/paperless.log)

## Q6. 카드 판정과 사용할 경로

소비자는 성공 레코드에서 `original=true`를 선택한다. 운영자는 대기·실패/성공 및 원본 ID, 추적 가능한 사본, 복구 이후 동일 파일로 검증된 결과가 필요하다. 제공자는 입고 전 해시와 최초 보관 사본을 갖고 소비 폴더에는 복제본을 둔다. 검증 수신자는 회수 PDF의 서명 범위·내용 무결성과 신뢰 문맥을 검사한다. P01의 시작점은 파서가 끝난 뒤의 저장이다. P04의 시작점은 문서 ID와 파일이 존재하는 회수 단계다. L01은 사전 영수증이 있는 바이트 대조 단계다. 세 링크에는 서명별 파서 우회와 실패 후 사용자가 받는 상태 경로가 비어 있다. [판정 원장](decisions.csv)

배포자가 이 세 조건을 함께 약속하려면 적용 판과 대상 PDF 범위를 먼저 고정하고, 그 클래스에서 OCR 미실행·원본 저장·회수 무결성을 확인해야 한다. 실패가 사용자에게 미저장 사실과 재처리 가능한 사본으로 이어지는 경로도 같은 경계에서 실측해야 한다. 이번 판의 A는 충분한 기존 텍스트에 유효한 조건부 구성이다. 작성자 후속 완화처럼 파생 OCR을 허용하면 X의 명시 원본이 선택지가 된다. X는 초기 무 OCR 요구에 어긋나므로 146의 고정 카드에 직접 적용하지 않는다. 서명 이미지에서 엄격한 무 OCR이 필요하면 별도 보존 인수 또는 파서를 통하지 않는 제품 경로를 검증해야 한다. v2.2.1의 두 지원 설정 셀에서 그 경로를 찾지 못했다. [X 원본·파생 대조](evidence/runtime/S1-X/S1-X-SI/receipt.json) [후속 논의](https://github.com/paperless-ngx/paperless-ngx/discussions/5542)

## Q7. 바이트와 외부 의미 및 비용

- **기록 보존의 인수와 열람**. Library of Congress NDNP의 실제 1898년 신문 1쪽은 인수 배치의 TIFF와 별도의 PDF·JPEG2000·METS/ALTO OCR을 제공한다. 항목들의 역할은 매체와 배치 명세로 유지된다. Portico는 제공자 인수 뒤 원본·변환본·처리 이력을 남기고 정기 fixity 및 별도 전달을 운영한다. Watergate 사진 사례는 실물의 상태를 남긴 채 여러 관점을 제공하는 다른 대상의 원리다. LC–SDSC 실제 복제는 AIX 검사 도구 오류를 고친 뒤 재검증했으며, 파일시스템 매핑은 별도 복원해야 했다. [NDNP](https://www.loc.gov/ndnp/guidelines/examples.html) [Portico 처리](https://www.portico.org/our-work/preservation-step-step/) [NARA Watergate](https://www.archives.gov/news/articles/watergate-50th-anniversary) [LC–SDSC §2.4–2.6](https://www.digitalpreservation.gov/documents/SDSC_LC_data-storage_report_3.pdf#page=11)
- **연구데이터 배포와 재검증**. Dataverse는 활성화된 BagIt 처리에서 전체 목록에 대한 불일치를 보고하고 재업로드하게 한다. DataONE은 체크섬과 파일의 과학적 관계 및 `prov:atLocation`을 별도로 적어 상대 경로를 복구한다. Zenodo의 실제 연구자료에는 3개 항목의 발행 MD5가 있다. `iris.csv`의 공식 본문 151줄을 LF와 끝 줄바꿈으로 재조립한 4,026바이트가 발행 MD5에 맞았다. CRLF 및 마지막 개행 차이는 모두 불일치였다. 셸의 원 HTTP 바이트 수신은 403이었고 재구성 1/3 파일이 관측 범위다. [Dataverse](https://guides.dataverse.org/en/6.5/user/dataset-management.html#bagit-support) [DataONE](https://dataoneorg.github.io/api-documentation/design/DataPackage.html#describing-filesystem-hierarchies) [실제 Zenodo 레코드](https://zenodo.org/records/7421899) [검산 영수증](evidence/controls/zenodo-rendered-recheck.json)
- **파일 속성과 묶음의 반례**. SHA-256이 같은 서명 PDF를 담은 Bag은 mtime·모드·Bag 루트를 바꾼 뒤 유효했다. 기존 manifest에 든 README를 지우면 PDF가 그대로여도 Bag 검증은 실패했다. PDF만 포함한 새 작은 Bag은 자기 manifest에 대해 유효했다. L01을 답에 붙일 때 출발 지문·대조 출력·기대 목록을 적어야 한다. 이름·시각·모드·수신자 신뢰·보존할 내용의 관계는 한 파일의 바이트에서 확인되지 않는다. [L01 초안](https://digitalpreservation.gov/documents/bagitspec.pdf#page=7) [RFC 8493 완전성](https://www.rfc-editor.org/rfc/rfc8493.html#section-3) [로컬 대조](evidence/controls/bag-and-render.json)
- **준비와 처리 시간**. 이미지 pull은 Paperless 44.291초, Redis 4.363초로 각각 측정했다. 공통 fixture 생성·검증은 1.528초다. R1 인스턴스 준비 D/A는 28.006/28.750초, R2는 34.662/25.644초다. 본 8건의 투입 준비 합은 3.179/2.727초, 처리 합(파일 이동→큐 종료 관측)은 19.210/20.256초다. 각 반복에서 다운로드 10, 래퍼 9, Tesseract 인식 2, 다른 Tesseract 호출 36, 입고 실패 3, 예정 조합의 재시도 0이었다. 각 반복의 쓰기 대조 3건에서 권한 실패 1·명시 재입고 1·중복 거절 1이며 다운로드 두 번이다. 본 HTTP 전송 합은 1.959/1.792초이고 반환 검증은 0.527/0.444초다. 최초 X 기동은 HTTP 준비 단계에서 24.130초 뒤 멈췄다. 제한된 준비 재시도로 별도 실행 X가 통과했다. 모의 파일·동일 클라우드 호스트·단일 worker의 벽시계 값이며 동시성·다른 스토리지·작성자 환경의 비용은 미측정이다. [비용·분모](evidence/controls/costs.json) [기동 중단](evidence/setup-initial-x/harness-errors.json)

## 대안과 적용 한계

장기 보존에서 제공자 사본을 먼저 별도 인수하면 실패 후 재시도를 복구할 재료가 생긴다. 비용은 원본 보관·조합별 정책·작업 상태 운용이다. OCR된 접근 사본을 허용하는 경우에는 X에서 원본 보존과 텍스트 검색을 모두 확인했으나 기본 다운로드와 수신자에게 보내는 파일의 종류를 관리해야 한다. 본 연구의 A는 텍스트 분기만 통과한 설치 옵션이므로 별도의 이미지 서명 저장 경로나 경보 전달을 마치면 카드의 적용 범위가 넓어진다. 두 반복은 새 상태를 검증했다. 새로운 플랫폼·복합 페이지·실제 제공자 파일에 대한 반복은 남아 있다.

| 불일치·약점 | 판단에 미치는 영향 | 다음 조사·자료 | 결론을 바꿀 관측 |
| --- | --- | --- | --- |
| 한 페이지 합성, 단일 호스트, 소비 폴더. 저자 파일·원래 UI 미확인 | A/ST의 근거는 동일 파일과 지원 분기다. 샘플 바깥에 보장하면 실패를 숨길 수 있다 | 같은 digest에 짧은·혼합 텍스트, 공개 인증/다중 서명, 허용된 작성자와 같은 형식의 QA PDF를 UI와 watcher로 입고 | 기본 판에서 서명 이미지도 입고·원본 동일·래퍼 0·인식 0을 만족하거나 A의 텍스트 입력에서 그 보장이 깨진다 |
| 쓰기 금지는 원본 복사 단계 한 지점이며 외부 통지 미검증 | 소비 사본 잔존이 재시작 또는 후발 장애까지 일반화되지 않는다 | 원본 복사 뒤 썸네일/아카이브 실패, 앱 재기동, UI/운영자 알림과 별도 영수증을 같은 입력으로 추적 | 미저장과 복구 사본이 명시 통지되고 실패 뒤 재시작에서도 일치 원본·단일 DB 기록이 보존된다 |
| 통제 루트와 한 PDF 지문, 실제 체인과 업무 기대 목록 미확인 | 서명 내용 보존은 수신자 신뢰·경로·묶음 완전성에 대한 약속을 지지하지 않는다 | 수신자 신뢰 정책·시각 증거를 넣은 공개 QA 체인, 별도 경로/동반 파일 명세와 Bag 검증 | 신뢰 검증, 기대 목록과 외부 속성 대조가 독립적으로 통과하고 각 결과가 동일한 성공 영수증에 연결된다 |
