# AF-RES-154 자기 검산

제품 실험의 기본 단위는 한 고정 PDF를 한 빈 설치의 지원 설정으로 관측한 소비 작업이다. R1·R2는 독립 SQLite·Redis·미디어·소비 상태로 시작했고 관리 호스트와 OCI 이미지를 공유했다. 검토는 작성자가 수행했다. 외부 유지보수자 보고를 비교 원전으로 썼고 별도 검토자가 이 결과를 검토하지는 않았다.

| 질문 | 주장과 근거 원절 | 실행·원장 연결 | 무효화 조건 또는 한계 |
| --- | --- | --- | --- |
| Q1 | 5215 최초 본문 Description·Expected behaviour·Steps 및 1월 후속 댓글. AF-RES-146 P-A에서 고정한 원 CRLF·LF 지문과 일치. [E01 본문](https://github.com/paperless-ngx/paperless-ngx/issues/5215#issue-2063137483) | E01–E06, 146 requests.jsonl 3행·transitions.csv 13/15/16행·truth.csv의 P-A, 현 RESULT 표 1 및 Q1. [원장](sources.jsonl) | 공개 파일 · 실제 저자 설정 미확인. 유효 원본 또는 편집 이력으로 최초 요구가 달라지면 표 1을 정정한다. |
| Q2 | v2.2.1 파서 284–397, 소비·저장 consumer 376–385·431–585. OCRmyPDF v15.4.4 gate 188–203과 Tesseract 157–214·309–312·366–385. [파서](https://github.com/paperless-ngx/paperless-ngx/blob/a7ac71971162838b8b1ee9e3b431543e69618e21/src/paperless_tesseract/parsers.py#L284-L397) | X01–X04·X06·X08·X09, T01·T02, 표 2와 A/UI engine·container 로그. [양성 호출](evidence/runtime/R1-A/R1-A-UI/tesseract.tsv) | 계측이 보지 못하는 엔진 경로가 있거나 noarchive 로그 직후 인식 출력이 있으면 무 OCR 판정을 철회한다. 암호화 공개 샘플은 보조 parser 분기다. |
| Q3 | T03–T06·T09와 X05·X07. 시각 픽셀, 서명 범위, 신뢰 루트를 독립 검사. [검증 문맥](https://docs.pyhanko.eu/en/v0.25.3/lib-guide/validation.html#validation-contexts) | fixtures.jsonl의 4 주입·2 보조, 공개 CA·고정 검증 시각, BagIt/렌더링·PDF 도구 출력. [픽스처](fixtures.jsonl) [변조 대조](evidence/controls/bag-and-render.json) | pyHanko의 `valid` 단독과 pdfsig exit 0은 내용 무결성 충분조건이 아니다. 실제 인증·폐기·LTV 정책이 다르면 신뢰 판정도 달라진다. |
| Q4 | X01 API 61–90, X02 views 331–351 및 486–491. [반환 선택](https://github.com/paperless-ngx/paperless-ngx/blob/a7ac71971162838b8b1ee9e3b431543e69618e21/src/documents/views.py#L331-L351) | 예정 16행, 큐 SUCCESS 10·FAILURE 6, 원본 10/10·기본 6/10 일치. 출력의 서명/페이지별 텍스트 영수증과 실제 상이 응답 파일. [입고 원장](runs.jsonl) | 성공 ID가 있는데 명시 원본 SHA가 다르거나 기본·명시 경로가 뒤집히면 P01/P04 문장을 철회한다. 허용 입고 채널과 권한을 넘는 주장은 미확인이다. |
| Q5 | E01 실패 기록, X02 consumer 106–115·143–159·473–585. [원본 쓰기 전후](https://github.com/paperless-ngx/paperless-ngx/blob/a7ac71971162838b8b1ee9e3b431543e69618e21/src/documents/consumer.py#L507-L585) | R1/2-A-W/R/DUP와 write-retry.json, 3→3→4→4. 6개 서명 실패와 두 관리경로 권한 실패, 별도 중복 두 건. [R2 대조](evidence/runtime/R2-A/write-retry.json) | 서명 거부의 실패 위치가 문서마다 다를 수 있다. 외부 통지와 늦은 저장 실패, 종료 후 자동 재시작은 시험하지 않았다. |
| Q6 | P01 원본 저장·P04 HTTP 반환·L01 사전 지문. E03·E04에서 별도 파생 허용 논의. [후속 절충](https://github.com/paperless-ngx/paperless-ngx/discussions/5986) | A/ST 성공, A/UI 인식과 원본 반환, D/ST·SI와 A/SI 파싱 실패, X/SI 원본 보존·기본 서명 부재. [결정 원장](decisions.csv) | D에서 유효 서명 파일의 전체 성공이 모두 확인되거나 A/ST에 래퍼 호출이 잡히면 추천 조건이 달라진다. 실패 문구까지 갖춘 조합은 이 연구에서 관측되지 않았다. |
| Q7 | L01 표준 및 A01–A04·R01–R04의 기관 사례. [묶음 검증](https://www.rfc-editor.org/rfc/rfc8493.html#section-3) | 같은 SHA의 attrs/경로 변경, 빠진 동반 파일 등 BagIt 대조. Zenodo 본문 재조합, 비용 JSON과 각 정상·보조 영수증. [비용](evidence/controls/costs.json) | 파일 속성·묶음·신뢰는 별도 확인이 필요하다. raw Zenodo HTTP는 403, 1/3 합치며 운영 비용·호스트 간 변동은 미측정이다. |

## 분모·판정 역추적

- 외부 원장 40행 중 실제 열람한 고유 원전 31저작을 산입했다. 사건 5, 실행 계약·구현 8, 공개 시험 3·검증 도구 3·입력 생성 2·입력 검증 명세 1, 기록보존 4, 연구데이터 4, 패키지 표준 1이다. 같은 사건의 E03과 같은 제품 계약의 X09는 열람했으며 하한에서 제외했다. 실패 접근 7행은 소스 시도로 남겼다. 같은 제품 매뉴얼의 사용·설정·API, 같은 BagIt의 두 판 및 동일 포털 자료의 동일 저작을 한 번씩 셌다.
- 결과표 2와 runs.jsonl의 주 항목은 16/16, 관측 결측 0, 성공 10·실패 6이다. 실패 6의 다운로드 적용 분모는 0이다. 주 실행의 정상 응답은 20/20 HTTP 200이다. 추가 권한·복구·중복은 각 2회, X는 1회다. 합계 입고 23회의 응답 26과 준비 단계 중단 1회는 서로 다른 단위다. OCRmyPDF 래퍼 18·Tesseract 인식 4는 본 16건에서 관측됐다. X는 각 1이고 권한·복구·중복은 각 0이다.
- decisions.csv에는 23개 실제 입고 ID와 7개 독립 요구/관측 열의 교차 161행이 있다. 조건부 문장의 원전 ID, 실행 증거와 본문 표의 화면을 대조했다. 원본·기본·서명·미신뢰·위치·실패는 같은 진릿값으로 채우지 않았다. R-LOG는 명시 실패가 걸리지 않은 성공, 잘 설명된 중복, 일반 실패 진단을 각각 표시한다.
- 직접 반례는 A/UI의 두 회수 바이트 일치와 인식 실행, D/UT의 인식 0과 래퍼·다른 PDF/A, A/SI의 등록 실패, X/SI의 유효 명시 원본과 기본 무서명, 권한 회복 뒤 남는 실패 사본, 가시 결과 동일·내용 검증 실패, 유효 Bag과 별도 작업 목록의 불완전이다. 표 3에 각 기준을 바꿀 관측을 연결했고 RESULT의 마지막 세 행에서 후속 자료를 지정했다.

## 재생·검사 범위

`python replay/verify.py`는 공개 파일 SHA·바이트 수, 통제/무앵커의 서명 값, 원본·파생의 두 응답과 DB·소비 잔존, 권한·중복 일관성, 공개 원장 스키마·개수와 161개 결정의 행 연결을 검사한다. `--replay-dir`은 새 실제 실행의 동작을 대조한다. 큐 UUID·시간과 새 파생 PDF/A의 정확한 지문은 변할 수 있으며 각 실측 파일의 자체 해시와 내용은 별도로 검산한다. 결과 커밋에서 새 checkout의 전체 재생·workbench 계약·공통 검사 결과는 검증 후 별도 영수증으로 남기는 절차다.

최초 X 서비스는 준비 HTTP 연결이 끊겨 입고를 시작하지 못했다. 준비 단계의 연결 재시도를 적용해 새 인스턴스에서 X/SI를 정상 관측했다. 결과판 재생에는 이 수정이 포함된다. 앞선 픽스처 커밋 이후 공개 인증서를 gitignore 대상 밖의 .crt로 수록했고 이는 동일 인증서 바이트다. 글꼴 렌더링 캐시를 임시 경로에서 생성하도록 변경했다. 두 보정은 제품 이미지와 고정 입력 지문을 바꾸지 않는다. [초기 기동 증거](evidence/setup-initial-x/harness-errors.json) [입고 영수증](evidence/runtime/S1-X/S1-X-SI/receipt.json)
