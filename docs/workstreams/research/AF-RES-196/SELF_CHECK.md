# AF-RES-196 자체점검

판정은 **DONE**이다. 아래 점검은 동일 작업자가 수행했다. 정답표를 읽는 채점 프로세스를 복원 프로세스와 분리했고 별도 checkout에서 재실행했다. 독립 작업자 검토는 미실시다.

| 질문 | 답과 근거 | 스스로 찾은 반증과 대조 | 판정·미충족 |
| --- | --- | --- | --- |
| Q1 | 당시 제출 두 건과 새 관측 두 건을 먼저 봉인했다. 당시 제출은 E01·E02, 새 관측은 R01·R07이다. [E01](https://github.com/w3c/json-ld-api/blob/8811ba2a3bcae883ac91efacffb70ef08d84e92f/reports/jsonld-gold-earl.ttl#L31-L42) · [E02](https://github.com/w3c/json-ld-api/blob/8811ba2a3bcae883ac91efacffb70ef08d84e92f/reports/jsonld-js-earl.ttl#L29-L40) · [R01](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/gold-T01-r1/receipt.json#L50-L54) · [R07](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/js-T01-r1/receipt.json#L53-L57) | 186 frame의 제외와 실제 미실행을 대조했다. 실행 원장 40행의 미실행 사유는 모두 비어 있다. [M05](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/runs.csv) · [M06](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/frame.csv) | 실재 4/6 및 증거 유형 2개 충족. N1·N2 원래 입력 결측. H1 시간대 미확인. |
| Q2 | 동일한 네 인용의 A·B·C 12표현이 있다. O1은 3구간 291바이트다. [R01](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/gold-T01-r1/receipt.json) · [목록](receipts/bundles/package-manifest.json) | C에 전체 파일을 저장한 것으로 보일 수 있어 각 locator 길이의 합과 원파일 크기를 구별하여 검산했다. B와 C의 키 집합이 요청한 필드와 일치한다. [정답표](gold.json) · [크기](costs.csv) | 직렬화 크기와 구간 SHA 확인. 압축·중복 제거 미측정. |
| Q3 | 245파일 고정 거울 및 묶음 단독 조건을 독립 임시 디렉터리로 만들었다. [M01](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/HANDOFF.md) · [실행 로그](receipts/core.jsonl) | 정답표나 외부 파일에 몰래 도달했다는 설명을 확인했다. 두 커널 차단 확인가 모든 실측·통제 회차에서 막혔고 묶음 단독 조건의 descriptor는 1개다. 두 EARL의 입력 준비는 별도 HTTP 200이었다. [봉인 기록](inputs.json) · [재실행](receipts/replay.json) | 실측 24/24, 통제 7/7에서 격리 확인. 외부 서비스 장기 가용성 미확인. |
| Q4 | 표의 표시 값, 원문 주체·기준일, 정확 구간 및 실제 다이제스트 상태를 각각 확인했다. [E02](https://github.com/w3c/json-ld-api/blob/8811ba2a3bcae883ac91efacffb70ef08d84e92f/reports/jsonld-js-earl.ttl#L29-L40) · [원장](matrix.csv) | B의 묶음 단독 로그는 stored SHA가 있으나 observed SHA가 없었다. C의 동봉 바이트는 해시까지 계산했으며 동일 체크섬과 조각을 함께 바꿔 독립 진위가 빠진 경우도 만들었다. [B 회차](receipts/core.jsonl#L4) · [동시 변경](receipts/controls.jsonl#L5) | 주 표본 원문 일치 16회의 정확한 바이트 위치를 재대조. 전체 파일과 과거 실행의 독립 진위 미검증. |
| Q5 | 같은 `receipt.json` 이름의 Gold와 JS, 한 바이트 변경, 주소만 남은 사본을 대조했다. [R01](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/gold-T01-r1/receipt.json) · [R07](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/js-T01-r1/receipt.json) | 두 정상 로그가 같은 `[]`를 갖는 경우에 basename 대체가 주체·날짜를 오판했다. 정본 경로 대조는 복원했으며 URL-only도 거울이 있으면 원문의 사실을 찾았다. [대조 7건](receipts/controls.jsonl) | 음성 및 양성 제어가 함께 작동. 주 표본의 분모에는 0건 산입. |
| Q6 | BagIt의 파일·manifest·fetch 역할을 분리하고 NIST 2197의 기간판 제품 행과 두 로트의 공식 성적서를 연다. [B01](https://www.rfc-editor.org/rfc/rfc8493.html#section-2.2.3) · [B02](https://blogs.loc.gov/thesignal/2012/01/from-there-to-here-from-here-to-there-digital-content-is-everywhere/) · [P01](https://tsapps.nist.gov/srmext/certificates/archives/2197_LotLL-198_Cert_2024-07-17.pdf#page=1) · [P02](https://tsapps.nist.gov/srmext/certificates/documents/Annual_SRM_Product_List.pdf#page=50) | 다른 LL-165의 값과 로트가 바뀌며 제품 번호만 맞았다. 공식 아카이브 인덱스를 쓸 수 있으면 제품명에서 정확판까지 갈 수 있는 예도 확인했다. [P03](https://tsapps.nist.gov/srmext/certificates/archives/2197_LotLL-165_Cert_2017-11-09.pdf#page=1) · [P04](https://shop.nist.gov/ccrz__CCPage?pageKey=SRMArchive) | 직접 읽은 절·페이지의 필드를 동결하고 로컬 대조 완료. PDF 원바이트와 실시간 상점 상세 미확인. |
| Q7 | 거울 없이는 원증거까지 C만 4/4. 표시값은 A/B/C 각각 4/4. 거울에서는 A도 원문 4/4를 회수했다. [E01](https://github.com/w3c/json-ld-api/blob/8811ba2a3bcae883ac91efacffb70ef08d84e92f/reports/jsonld-gold-earl.ttl#L31-L42) · [R01](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/gold-T01-r1/receipt.json) | A의 URL에 SHA와 경로가 이미 포함돼 B의 그 두 필드가 이번 표본에서 대체 효과를 못 낼 수 있음을 확인했다. 비교 가능한 저장 지문과 바이트 동봉의 역할은 A/B/C에서 실제로 구별된다. [matrix](matrix.csv) · [costs](costs.csv) | 36 예정셀 모두 실측 또는 입력 결측으로 기록. 구조·비용과 새 checkout 재실행 일치. |

## 직접 열람 수와 사건 수

| 분모 | 실재 · 기준 | 산입 |
| --- | --- | --- |
| 186 원영수증·원로그 | 16 · 최소 12 | 최초 반복의 영수증 12개와 해당 실행들에 속한 stdout/stderr 4개. 파일은 16개이고 실행 ID는 12개다. |
| 인계·목록·실행 메타·연결 정확판 | 10 · 최소 6 | 186 내부 자료 8개와 별도 버전 고정 EARL 2개. 미선택 단언 18개는 URL만 기록했다. |
| BagIt/의회도서관 | 3 · 최소 2 | RFC 원문, 의회도서관 이관 설명, bagit-python 원 문서. |
| NIST 명시 로트 원성적서와 제품 레코드 | 2 · 최소 2 | LL-198 원성적서 p.1과 2026 NIST 제품 목록의 SKU 2197 행 p.50. |
| 다른 공개 원문 직접 열람 | 5 · 보조 | 같은 SKU의 LL-165, 공식 아카이브, Charpy 프로그램, 1575a 원연구와 2022 성적서. |
| 고유 자료와 계보 | 36 직접 열람 · 11 계보 | URL의 인용 앵커를 제외한 고유 원문 36개다. 이 중 Git·HTTP 원바이트 SHA-256 고유 26개, 공개 웹 본문 판독 고유 10개다. 별도 기록 11행은 보조·중복 메타 2개와 접근 실패 9개다. 최초 재실행 영수증은 보강 전 출처 원장 44행을 점검했다. |
| 196 주표본의 증거 사건 | 4 문장 · 2 시험 키 | 보존된 역사 단언 2개와 새 관측 실행 ID 2개. 역사 실행의 독립 수 미확인. 이번 검사의 24 본 회차·7 통제는 기존 실행 사건과 별도다. |

접근 실패와 미열람 후보의 주소 및 판단 근거는 모집표와 원장에 남겼다. [모집표](frame.csv) · [출처 원장](sources.jsonl) · [공개 판독의 지문 범위](receipts/public-freeze.json)

## 재실행과 검사 경계

봉인 커밋 `eed4d55bad851d084a5a762f0b81278bbf68cc16`이 실행 커밋보다 앞선다. GitHub에서 새로 복제한 코드 판 `258f78614227ba89dd116636e96fbad56a23c30c`에서 입력·정답표·거울을 재사용했다. 핵심 24회, 통제 7회, 공개 대조를 되돌려 12묶음 및 주요 CSV·JSONL·공개 대조 결과를 바이트 단위로 비교했다. Python 3.12.14, libseccomp2 2.6.0-2, 실행 종료 0이다. [묶음 실행](receipts/build-run.json) · [본 실행](receipts/core-run.json) · [통제 실행](receipts/controls-run.json) · [재실행](receipts/replay.json)

동 코드 판의 공통 클라우드 검사와 세션 단건 검사는 각각 종료 0이다. 공통 세션 탐색은 `no_active_sessions`였고, 196 허용경로·의존 해시의 `remote_checked` 판정은 별도 단건 검사에서 확인했다. 통합판은 단건 재확인 시점에 진전했으나 계약 SHA는 같다. [검사 기록](receipts/replay.json)

정답의 판독과 실험 주체는 동일하다. 독립 검토, 과거 JSON-LD 제출 당시 실제 실행 확인, 다른 환경의 엔진 재현, NIST 원 PDF 바이트 보존은 미실시 또는 미확인이다.
