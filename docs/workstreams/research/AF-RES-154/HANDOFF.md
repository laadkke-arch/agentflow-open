# AF-RES-154 HANDOFF

**작업자 판정 COMPLETE · 수용 상태 REVIEW_READY**

시도 1, Codex Cloud, 저장소 `laadkke-arch/agentflow-open`, 브랜치 `work/research-af-res-154`. 소유 경로는 `docs/workstreams/research/AF-RES-154/`이다. 계획 통합판은 `f140af3179b7d9271710778104ccee5b4812e2ef`, 실제 시작판은 `9e378ca91c399454466196617cf362d0cdb514f9`이다. [작업 범위](SCOPE.md) [등록 선행 AF-RES-146](https://github.com/laadkke-arch/agentflow-open/blob/9bf267b71a0000aae5f098e82eab3f84c0dd7714/docs/workstreams/research/AF-RES-146/HANDOFF.md)

검사한 **결과판**은 `b19c8f966e3f5ae95c0f8714ebcd09122dabdc35`다. 2026-11-24 16:24:16 UTC에 새 체크아웃의 재생·자료 검산·Git clean을 확인했다. 실행 증거 영수증은 별도 커밋 `829a29e49ab7c978289be7010b9490195e795106`에 있다. 이 인계와 영수증은 결과판 검사 뒤에 작성했다. 자기 검토를 마쳤고 독립 검토는 미실시다. [결과판](https://github.com/laadkke-arch/agentflow-open/blob/b19c8f966e3f5ae95c0f8714ebcd09122dabdc35/docs/workstreams/research/AF-RES-154/RESULT.md) [자기 검산](SELF_CHECK.md) [검사 요약](evidence/verification/summary.json)

## 결과와 답에 쓸 조건

- 공식 Paperless-ngx v2.2.1, 두 설정, 서로 독립인 상태 두 반복에서 입고 16/16을 관측했다. 성공 10·실패 6, 명시 원본 10/10 동일, 기본 다운로드 6/10 동일이다. 입고 실패 여섯 건에는 다운로드 문서 ID가 없었다. 서명 입력 중 기본 설정 성공은 0/4다. `always`의 서명 텍스트 2/2는 OCRmyPDF·문자 인식 각 0이고 두 반환의 바이트와 서명 무결성이 유지됐다. `always`의 서명 이미지 2/2는 래퍼가 두 번씩 호출됐고 인식 전에 입고에 실패했다. [입고 및 출력 원장](runs.jsonl)
- P01·P04·L01은 성공 입고가 있어야 원본 보관→명시 회수→사전 지문 대조로 연결된다. 같은 서명 파일은 통제 CA 문맥에서 신뢰했으며 신뢰점 0의 문맥에서 미신뢰였다. 별도 X에서는 서명 이미지의 명시 원본을 회수했으나 문자 인식이 있었고 기본 파생 응답의 서명 개수는 0이었다. 초기 무 OCR의 사용자 요구와 후속 파생 허용을 별도 판단으로 둔다. [판정표](RESULT.md) [X 실측](evidence/runtime/S1-X/S1-X-SI/receipt.json)
- 쓰기 실패·동일 바이트 재입고·중복 거절은 각 2건이다. 첫 실패에서 DB 문서 수는 3→3, 권한 복구 후 3→4, 중복에서 4→4였다. 소비 사본은 실패 뒤에 남았다. 로그는 실패 원인·파일명을 표시했고 미저장 사실과 복구 사본을 함께 알리는 원 작성자의 통지는 입증되지 않았다. 세 링크를 한 번에 약속하려면 수용한 입력에서 무 OCR 저장·원본 회수를 확인하고, 실패에서 이 통지가 도달하는 절차도 검증해야 한다. [쓰기 및 복구](evidence/runtime/R1-A/write-retry.json) [저장 실패 로그](evidence/runtime/R1-A/R1-A-W/paperless.log)
- 원전 31저작을 직접 확인했다. NDNP·Portico와 Dataverse·DataONE·Zenodo에서 원본과 접근본, 묶음 목록·경로·입고 검증의 별도 역할을 확인했다. 동일 픽셀의 변조 PDF가 `pdfsig` 종료 0과 Digest Mismatch를 같이 냈고, PDF 지문이 같아도 동반 파일이 빠진 Bag 검증은 실패했다. [출처 원장](sources.jsonl) [렌더·BagIt](evidence/controls/bag-and-render.json)

## 실제 검사

GitHub에서 결과판을 새로 받았다. 검사의 통합 팁은 `c17f19265ce2c3603c9d1e6915959271867af7f6`, 계약 v2의 지문은 세션 시작과 같고 등록 선행 `9bf267b71a0000aae5f098e82eab3f84c0dd7714`도 일치했다. 행 순서 `UT UI ST SI`와 각 고정 SHA-256으로 만든 주 입력 영수증의 지문은 `9411f18d0b6807221e74eeefc7afb9d6a642ba8513a1281a72f58ca8a9f7b5ee`다. [정확한 파일·지문](evidence/verification/inputs.json) [명령·종료·시간](evidence/verification/command-receipts.json)

| 실행 명령 | 종료 코드 | 확인한 결과 |
| --- | --- | --- |
| `python -m workbench.session check docs/workstreams/research/AF-RES-154/session.json --fetch` | 0 | 원격 계약·의존·경로 통과. 허용 경로 밖 0. |
| `python scripts/check.py --require-git` | 0 | 공통 55, 기존 lab 7·9 및 demo·내보내기·Git bundle 복원 통과. |
| `python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 0 | 시작·끝 clean인 결과판으로 doctor·공통 검사·smoke 통과. 전역 sessions는 `no_active_sessions`이고 이 과제의 매니페스트는 위 개별 검사로 확인했다. |
| `fixtures.py` 및 `controls.py`를 별도 venv에서 실행 | 각 0 | 입력 6개의 해시·크기·페이지 텍스트·서명 값과 렌더/BagIt 대조가 재현됐다. |
| `run.py --out` 및 `verify.py --replay-dir` | 각 0 | 23/23 결합 동작 일치, 본 16/16과 쓰기·재시도·중복·옵트인 포함. 원본 바이트는 고정 입력과 일치했고 PDF/A 파생 5건의 실행별 지문은 모두 달랐다. |
| `git diff --check 9e378ca91c399454466196617cf362d0cdb514f9..HEAD` 및 새 checkout 전후 `git status --porcelain` | 각 0 | diff 오류 0, 새 체크아웃 전후 변경 0. |

초기 X 기동은 HTTP 준비 단계에서 종료 1이었다. 업무 입고 전의 인터페이스 재시도를 적용한 뒤 별도 X에서 정상 입고했고, 결과판의 전체 재생도 종료 0이었다. 당시 이미 끝난 16건의 분모는 동일하다. 실제 저자 인보이스, 업로드·메일 경로의 실패 복구, 운영자에게 외부 알림이 전달되는지, 수신자의 신뢰 정책은 미확인이다. [초기 기동 중단](evidence/setup-initial-x/harness-errors.json) [재생 대조](evidence/verification/commands/artifact-and-replay-verify.stdout)

## 묶음별 원격 확인

각 묶음은 원격 브랜치 HEAD를 조회한 뒤 정확한 커밋의 GitHub raw 대표 파일을 다시 읽고 로컬 Git blob과 비교했다.

| 묶음 | 원격 커밋 | 대표 파일 | Git blob | 읽은 UTC |
| --- | --- | --- | --- | --- |
| ① 범위 | `8d577c435c8f64a417afaa182aa4302c9c880870` | SCOPE.md | `1b399b41b6da12daa003ef8aecda57c131518dda` | 15:54:19 |
| ② 입력과 초기 원전 | `3250d6ba8c6a5c3fe2a364980b7dc7452e312d74` | fixtures.jsonl | `46bb08c40553b8662bd6eab0fd7fd344bd0fddcc` | 16:01:07 |
| ② 공개 검증 자료 보정 | `6925b6464fc32d4c9b2402f228f7159ccfec2436` | replay/fixtures/qa-root.crt | `db5b735c74cf4547459068f288c6f469e8200da5` | 16:03:44 |
| ③ 본 관측 | `7238fe4aa94e25255b3b3ea129240324006559f5` | runs.jsonl | `e44d6ecb905e1dab84f4bceda49ed8153a73eaf2` | 16:05:58 |
| ④ 반례·대조·비용 | `c502df7c586127ea449bc28bab24e02410f7b900` | sources.jsonl | `440227ec5dc2841ea9318bb6df7cdde437696b45` | 16:12:16 |
| ⑤ 결과표와 자기 검산 | `b19c8f966e3f5ae95c0f8714ebcd09122dabdc35` | RESULT.md | `3dc11c00bd279dfcee0b27dbf730a3b882b1cd91` | 16:19:15 |
| ⑤ 실제 검사 영수증 | `829a29e49ab7c978289be7010b9490195e795106` | evidence/verification/summary.json | `faf202269bb885280b1a8432b831107c4aa0a870` | 16:24:31 |

## 다음 첫 행동

위 결과판에서 [R1-A-ST](evidence/runtime/R1-A/R1-A-ST/receipt.json), [R1-D-SI](evidence/runtime/R1-D/R1-D-SI/receipt.json), [R1-A-W 로그](evidence/runtime/R1-A/R1-A-W/paperless.log)를 먼저 대조한다. 결과를 채택할 검토자는 `replay/fixtures/st-signed-text.pdf`와 `replay/fixtures/si-signed-image.pdf`를 같은 OCI 지문의 시험 인스턴스에서 UI/API와 소비 폴더에 각각 투입해 미저장 통지와 원본 보유를 확인한다. 제품 API 경로의 첫 입력은 `si-signed-image.pdf`를 `POST /api/documents/post_document/`에 제출한 뒤 반환된 작업 UUID로 `GET /api/tasks/?task_id=<uuid>`를 읽는 조합이다. 권한이 있는 테스트 인스턴스에서 공급 원본은 읽기 전용으로 보관한다. [고정 API 안내](https://github.com/paperless-ngx/paperless-ngx/blob/a7ac71971162838b8b1ee9e3b431543e69618e21/docs/api.md#L257-L289) [전체 재생 명령](replay/README.md)

색인 제안 한 줄. AF-RES-154 · P-A의 고정 카드 3개 · v2.2.1의 텍스트 서명만 `always`에서 무 OCR·원본 회수 관측 · 이미지와 실패 알림의 결합은 미확인 · 16셀, 보조 7건, 외부 31저작.

| 불일치·약점 | 판단에 미치는 영향 | 다음 조사·자료 | 결론을 바꿀 관측 |
| --- | --- | --- | --- |
| 합성 한 페이지, 한 호스트, 정상 소비 폴더 | 무 OCR·보존 결합은 실제로 입고한 텍스트 입력 범위다. | 같은 제품판의 짧은·혼합 페이지, 암호화 및 복수 서명 QA를 포함해 UI·소비 폴더를 대조한다. | 기본 판에서 서명 이미지도 유효 원본·무 OCR·정상 저장을 달성하거나 A에서 이 조건이 깨진다. |
| 실패 주입 지점 한 곳, 경보 전달 미관측 | DB·대기 사본 상태는 확인했으나 원 작성자의 미저장 알림 및 모든 복구 경로를 보장할 수 없다. | 앱 재시작, 원본 복사 이후 장애, 업로드/메일 및 외부 운영자 통지를 작업 ID로 연결한다. | 실패가 명시적으로 통보되고 재처리 후 원본과 단일 레코드가 유지된다. |
| 합성 신뢰점, 단일 PDF 지문 | PDF 무결성, 수신자 신뢰, 원래 경로 및 기대 묶음의 검증은 각각 증거가 필요하다. | 수신자 정책·시간 증거에 맞는 공개 QA 서명 체인과 기대 목록, 속성 명세를 비교한다. | 서명 무결성·신뢰·경로·완전성 검사가 모두 통과하고 같은 입고 영수증에 연결된다. |
