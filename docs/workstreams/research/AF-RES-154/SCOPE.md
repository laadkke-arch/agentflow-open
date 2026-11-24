# AF-RES-154 범위와 관측 규칙

범위 봉인 전 확인일 2026-11-24 UTC. 연구 질문은 서명 PDF의 입고, 원본 바이트 보존, OCR 미실행, 저장 실패의 명시적 통지를 Paperless-ngx 한 판에서 함께 확인할 수 있는 조건이다.

## 배정과 고정 근거

- 저장소 `laadkke-arch/agentflow-open`, 작업 브랜치 `work/research-af-res-154`, 소유 경로 `docs/workstreams/research/AF-RES-154/`. [작업 매니페스트](session.json)
- 계획 통합판 `f140af3179b7d9271710778104ccee5b4812e2ef`. 배정 확인 때의 팁 `898409b64886fba63e0d2c4ffe43b12ab656375e`. 첫 커밋 전에 확인한 실제 시작판 `9e378ca91c399454466196617cf362d0cdb514f9`. 계획판 이후 세 커밋의 변경 파일은 진행표 한 개다. 통합판 원격의 HEAD와 계약 v2를 세션 시작 때 확인했다. [세 커밋 비교](https://github.com/laadkke-arch/agentflow-open/compare/f140af3179b7d9271710778104ccee5b4812e2ef...9e378ca91c399454466196617cf362d0cdb514f9)
- 이 판의 AGENTS.md, STATE.md, DOT_AUTOMATION.md, RESEARCH_WORKFLOW.md, RESEARCH_BRIEF.md, CLOUD_WORKFLOW.md, 진행표의 AF-RES-154 및 AF-RES-146 행을 확인했다. 등록 선행은 DONE인 AF-RES-146 한 건이다. [진행표](https://github.com/laadkke-arch/agentflow-open/blob/9e378ca91c399454466196617cf362d0cdb514f9/docs/automation/dot-control.json)
- 146의 고정 자료는 인계와 원장 `9bf267b71a0000aae5f098e82eab3f84c0dd7714`의 HANDOFF.md, requests.jsonl P-A, transitions.csv의 5·7·8위 P01·P04·L01과 truth.csv의 해당 판정, 그리고 RESULT.md `91b10340abca933bb2696ff7372c3168999892ac`이다. 순위·검색 폭·독립 판독 48쌍·외부 27저작은 재산정 범위 밖이다. [선행 인계](https://github.com/laadkke-arch/agentflow-open/blob/9bf267b71a0000aae5f098e82eab3f84c0dd7714/docs/workstreams/research/AF-RES-146/HANDOFF.md) [선행 결과](https://github.com/laadkke-arch/agentflow-open/blob/91b10340abca933bb2696ff7372c3168999892ac/docs/workstreams/research/AF-RES-146/RESULT.md)

## 작성자 기준

#5215의 2024-01-03 tmaier 본문은 AWS 인보이스가 입고 과정에서 DigitalSignatureError로 저장되지 않았고 로그가 저장 실패의 결과를 충분히 알리지 않았다고 보고한다. 기대 동작은 서명 PDF를 변경 없이 들이고 OCR을 건너뛰며, 저장할 수 없으면 데이터 손실 위험이 드러나는 로그를 남기는 것이다. 후속 댓글의 파생본 허용은 별도 층에 둔다. 원 작성자의 인보이스 바이트와 전체 설치 설정은 미확인이다. 최초 경로 보존은 별도 가정이고, 소비 폴더와 제공자가 보유하는 최초 파일을 따로 기록한다. [작성자 본문과 후속 댓글](https://github.com/paperless-ngx/paperless-ngx/issues/5215)

## 고정 실행판과 두 설정

- 공식 Linux/amd64 Paperless-ngx 이미지 `2.2.1`의 OCI digest `sha256:096719d7f44e5f8538ca4cf8c717d3a10d8fec699c85f494cdf94ded91bed666`, 검증한 소스 리비전 `a7ac71971162838b8b1ee9e3b431543e69618e21`. Pipfile.lock에서 OCRmyPDF 15.4.4, pikepdf 8.10.1, Django 4.2.8, Celery 5.3.6을 확인했다. 비교는 공식 이미지 SQLite와 별도 Redis 7.2.3-alpine OCI digest `sha256:090276da2603db19b154602c374f505d94c10ea57e9749fc3e68e955284bf0fd`로 실행한다. 이미지가 실행되지 않으면 같은 소스 태그로 정상 입고 준비를 시도하고 차이를 남긴다. [소스 태그](https://github.com/paperless-ngx/paperless-ngx/releases/tag/v2.2.1) [잠금 파일](https://github.com/paperless-ngx/paperless-ngx/blob/a7ac71971162838b8b1ee9e3b431543e69618e21/Pipfile.lock#L1111-L1157)
- D는 해당 판의 OCR 기본값 `skip`과 아카이브 기본값 `never`를 그대로 쓴다. A의 단일 변경은 문서화된 `PAPERLESS_OCR_SKIP_ARCHIVE_FILE=always`다. v2.2.1에서 전체 PDF의 OCR을 서명 여부로 차단하는 지원 설정은 이 경로에서 찾지 못했다. `always`는 영구 아카이브를 생략하며, `with_text`와 같이 추출 문자열 길이가 50을 넘는 PDF에서 래퍼 전 조기 반환을 공유한다. 입력을 읽어 텍스트를 추출하는 동작과 OCR은 별개다. [동시대 설정](https://github.com/paperless-ngx/paperless-ngx/blob/a7ac71971162838b8b1ee9e3b431543e69618e21/docs/configuration.md#L546-L587) [파서 분기](https://github.com/paperless-ngx/paperless-ngx/blob/a7ac71971162838b8b1ee9e3b431543e69618e21/src/paperless_tesseract/parsers.py#L284-L338)
- 각 반복 1·2의 D/A는 각각 빈 SQLite·Redis·미디어·소비 폴더로 시작한다. 두 반복은 같은 클라우드 호스트의 독립 작업공간이다. worker/페이지 thread 각 1, UTC, 영어 기본, 내장 감시와 로컬 HTTP, 테스트 전용 사용자, 이미지 기본 서비스를 쓴다. 정상 입고 채널은 전 셀에서 소비 폴더다. 저자 보고의 업로드와 입구가 다르므로 경로 차이를 남긴다.

## 입력·관측 사전 규칙

| 항목 | 판정 및 증거 |
| --- | --- |
| 예정 16셀 | R1·R2 각각 D/A에 UT(미서명 텍스트), UI(미서명 이미지), ST(서명 텍스트), SI(서명 이미지)를 동일 바이트로 투입한다. 파일명을 역할마다 분리하고 셀을 직렬 처리한다. 두 서명 PDF는 사전 검사에서 전체 파일 서명 범위, 내용 무결성, 통제 신뢰점 검증을 통과해야 한다. |
| 입고 | 소비 감시 등록 → Celery 실행/종료 → DB 문서 수와 소비 경로 잔존 → 내부 원본/파생 존재 → 인증한 HTTP 다운로드 순서다. 성공 업무분모는 레코드 생성과 정상 작업 종료이며, 실패는 입고 분모에 남기고 다운로드 분모에서 제외한다. |
| 래퍼 호출 | 파서 로그의 첫 `Calling OCRmyPDF with args:`와 `Fallback: Calling OCRmyPDF with args:`를 각각 1회로 센다. 조기 반환 로그와 정상 작업 종료가 함께 있을 때 기록된 0을 판정한다. 오류로 래퍼가 호출된 셀은 엔진 인식이 0이어도 무 OCR 약속의 엄격한 기준에서 제외한다. |
| 실제 인식 | 기본 서비스의 Tesseract 외부 호출을 투명 전달하는 계측으로 인수를 남긴다. 버전·언어 조회, 방향 판별, HOCR/텍스트 인식을 구분한다. 실행된 엔진 인식 횟수와 래퍼 호출 수를 따로 센다. 누락된 계측은 미확인이다. 기동 점검 및 이미지 셀을 양성 대조로 삼는다. |
| 원본·기본 반환 | 두 HTTP 200 응답 각각의 SHA-256·바이트 수·직접 바이트 동일성·서명 출력·페이지 텍스트를 입고 전 파일과 비교한다. 기본 반환은 아카이브가 있으면 이를 우선한다. 소비 경로, 내부 원본 경로, 제공자 사본은 독립으로 기록한다. |
| 무결성과 신뢰 | 동일 PDF에 대해 서명 암호학과 전체 서명 범위, 테스트 루트가 있을 때의 신뢰, 루트를 지정하지 않았을 때의 신뢰를 독립 기입한다. 가시 내용이 같은 상이 바이트와 서명 범위 내 비시각 메타데이터 변조 대조를 별도 검증한다. 현재 공개 신뢰 또는 법적 서명 유효성은 판단 범위 밖이다. |
| 실패와 재시도 | 각 A 반복의 본 관측 뒤 별도 바이트의 텍스트 PDF를 내부 원본 디렉터리 쓰기 금지 하에 입고한다. 권한을 되돌린 뒤 동일 바이트를 다시 입고하고, 성공 뒤 동일 바이트를 한 번 더 넣어 중복을 구분한다. 원인·메시지·잔존·DB 수를 재기록한다. 작성자 로그 조건은 작업 식별·입고 실패·미저장 결과가 알아볼 수 있어야 충족으로 판정한다. 원본 잔존/재시도 명시 여부를 따로 표시한다. |
| 시간·결측 | 이미지 준비, 인스턴스 준비, 소비 폴더 투입→Celery 완료, 다운로드/검증을 구분해 실제 벽시계 시간을 기록한다. 지원 설정 밖 비교는 별도 분모다. 예정 시도, 실행된 시도, 진짜 관측 0, 실행되지 않은 결측, 해당 없는 반환을 각각 표시한다. |

관측 자료에는 모의 인보이스만 사용한다. 시험 전용 키는 생성 프로세스의 임시 디렉터리에서 사용한다. 공개 검증용 PDF·공개 루트·재생법·로그·영수증을 남긴다. 시험 범위를 좁힐 수 있는 후대 기능과 기관 사례는 고정판 관측과 구분한다.
