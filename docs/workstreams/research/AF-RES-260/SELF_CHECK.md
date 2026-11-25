# AF-RES-260 SELF_CHECK — 작업자 자체 검토 / PARTIAL
고정 본표 및 자료 판: c5be8efad40b212b7875692f3c55a111430296e3. 현재 세션의 자체 재독/정적 자료 확인만, 독립 연구자·Codex·브라우저 실행 없음.

| 질문 | 직접 원근거·위치 | 결론을 깨는 실제/탐색 사례 | 남은 미확인 및 최소 다음 확인 |
|---|---|---|---|
| Q1 | A01/A02 root와 ordered path tags, A03 선택 symbol, A04 removeAttrs/viewBox, A05 package version/files, A11/A12 title front matter, A13 tag commit | 동일 d인데 root fill=currentColor와 symbol fill 생략. title 문서와 XML 요소 구분; 원본 vs 배포 변환 가능 | 3/3 path exact string match 확인; release ZIP/npm 바이트 미수신. tag 자산과 archive SHA256/선택 d 비교 |
| Q2 | N01 SVG2 §5.5, N03 linking §16.1–3, N06 HTML base, N09 URL §4.3–4.4; A06 usage, contexts.csv A1..C2 | T02 cross-origin, T04/T05 nested, T06 target context; X1 동일 file/없는 fragment, X2 같은 basename/다른 URL. I02 GET 보고 | 여섯 정적 locators 확인, 실제 request/HTTP status/cache/instance target/pixel 0/6; fixture + local HTTP trace |
| Q3 | N07 Color4 §3.2,6.4; N08 Cascade5 §7.2; N01 §5.5.2–3; N02 conform; N04 paint §13.3–4. T03/T08/T08a/T08c/T10 | C 초기 color CanvasText, 검정 보편 규칙 철회. B fill 제거 X5; T03 selector scope, T10 override, C external red CSS 기대 비적용 | A/B red vs C UA CanvasText 예상뿐. light/forced-colors 조건 명시하고 exact crop, same-origin browser engines 실행 |
| Q4 | A01/02/03/04/06/10; I01,I02,I06; bundles.md 9 목적·모드 및 제거 | 2050 symbols 중 2개 선택, cache와 file presence 혼동; custom subset 별도 자산; source link 편집 vs runtime | 단일/양쪽 모드 번들 물리 파일 제거 0/9. 서버 root를 독립 구성하고 cold-context 비교; license 및 host/asset 경로 보존 |
| Q5 | T01..T08,T10 inputs/ref 및 support, WPT db19ea407e861bab8158d86f07823aec5a490a4e; T08c red rule; T00/T09 미산입 | T07 존재하나 display:none, T02 cross-origin, T04/T05 nested. I03 과거 장애 당사자 보고; 이름 집합 검사 T00 render 보증 못함 | 9 test works 기대만 확인; browser/version/run receipt 미실행. WPT 실행 별도, 대상 fixture runtime 로그와 분리 |
| Q6 | O4 A01/A02 실제 href/url()/defs 없음; A03 ID 텍스트; X1–3 합성 통제; N01, T04,T05,T07 | 존재하지만 무효 ID/표시 불가; 같은 이름 다른 바이트; 미사용 defs href는 선언 vs 선택 vs 실제 요청 구별 | 작성 통제 실행 0/3; O4 정상 공석 2/2 원문 확인. X1 missing ID와 HTTP 200, X2 decoy hash, X3 never.svg trace 및 crop |
| Q7 | G01 OGC §1.1.3, §2.2.6–7; G02 SQL INSERT; G06 actual binary blob 43dbc0e791c8ab690950f617186b3f78cc69dbeb; G07 SQLite format §1.6–7·2.1–3; gpkg_byte_evidence.json | G02 x와 G06 byte는 동일 데이터 아님(이름/last_change 다름); contents vs matrix extents 다름. GP10 header 오래된 버전; G05 OGC 본체 미수신 | 독립 SQLite 읽기·integrity check, OGC artifact 74984 받기; SQL/바이너리 식별 차이 검산. 지도 렌더/1.4 conformance 실행 안 함 |

## 재독 검사
- 실제 GitHub 고정 SHA c5be8efad40b212b7875692f3c55a111430296e3에서 SCOPE, sources, icons, contexts, fixture, bundles, counterexamples, gpkg evidence, RESULT 9개 재조회 성공. compare start becd6b705eebf9c5b77d04ff2bc0f19e11e85415..c5be8efad40b212b7875692f3c55a111430296e3: ahead16 behind0, 9 added files 전부 owned_path 아래. control 파일 변경 없음.
- 두 필수 표: 정확한 지정 열 이름/순서, 6행 및 9행, 분모 바로 아래, 마지막 3행 약점 표. Q1–7 모두 있음. (Q5 추가 표 9개 사례는 필수 표 분모 아님.)
- 원장: 58 rows, 58 unique source IDs, 34 counted distinct work IDs; 발행12/규격5/시험9/결함사례5/Geo3 (각 하한6/5/6/3/2). 비산입24(실패 F01,F02,G05 3, 중복/보조21). F02 sprite fetch_file empty 후 blob 성공, 원장 실패 행 유지. source_id/버전/위치/접근/산입 사유 포함; 정확한 발행 날짜가 없는 고정 source는 SHA 또는 access date, 시간은 수집 묶음 UTC. test/ref 중복·동일 spec anchor 비산입. G02/G06는 같은 lineage이나 다른 artifact/실제 row identity라 별도 work. 범위 밖 독립 전체 호출수 미확인.
- 실제 CSV/JSONL/HTML 문자열 구조 파싱 결과: {"ledger":58,"uniqueIds":58,"missing":[],"counts":{"publisher":12,"spec":5,"test":9,"issue":5,"geo":3},"iconsRows":3,"iconsCols":21,"iconsValid":true,"contextsRows":6,"contextsCols":15,"contextsValid":true,"controlLabels":true,"gpkg":[null,0,0,0,{"blob_len":712,"head_hex":"89504e470d0a1a0a0000000d4948445200000100000001000804000000f67b60"}]}. 3 path data rows / 21 cols; contexts 6 rows / 15 cols; source_ids 해소, fixture #A1/#B1/#C1/#A2/#B2/#C2 존재. JSON evidence static record values 포함. 이 검산은 문서/바이트 판독이고 제품 실행 아님. 자체 검토이지 독립 검토 아님.
- 정상 공석: A 외부 fetch 자원 2/2, 원 SVG 외부 참조 2/2, XML title 없음. 미수신: OGC 원 artifact 및 release ZIP/npm 실물. 미실행: browser 6/6, 제거 9/9, WPT 9/9, 통제 X1–3 및 X5. 접근 실패는 성공 하한에 불산입. O4는 합성하지 않은 원본 관측. 환경 미확인 값 black/네트워크 횟수/픽셀 동일성에 대해 결과 과장 없음.

## 자체 판정
PARTIAL. 정적 2×3 및 자료 하한/원본 대응/전달 조합/반례 4개/실제 GDAL 바이너리 선택 키 모두 확보. 공식 OGC guide artifact 및 release ZIP/npm 실배포 파일의 바이트 대조 미확인, 지정 여섯 슬롯과 제거/합성 통제 실제 영수증 미실행(웹 역할 범위 밖이어서 Codex 계획 제공). 불완전한 항목을 완료로 바꾸지 않는다. 다음 첫 행동은 HANDOFF의 고정 자산 확보와 독립 byte 검사, 이어 fixture 실행.
