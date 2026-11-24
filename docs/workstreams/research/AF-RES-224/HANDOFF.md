# AF-RES-224 HANDOFF · PARTIAL

- 작업 상태: **PARTIAL**. 문서/정의/방법/사례 조사 및 합성 12개 통제 수동 판독 완료. 요청된 네 카운티 실제 공표 행 0/4, 원값 0/48, 실제 유도율 0/2, 실제 통제 0/12, MOE 0/2. 결측은 0으로 대체하지 않음. 직접 열람 산입 저작 22(6/5/4/4/3), 원장 37개 중 접근 성공 32/실패 5, 계보 8; 실제 수치 사례 계열 3, 네 대상 카운티 독립 검증 0. 별개 표와 LAUS·MLB 경기 원행 미확인으로 자료 유형별 실측 조건도 미달.
- 저장소: laadkke-arch/agentflow-open, 작업 브랜치 work/research-af-res-224, owned_path docs/workstreams/research/AF-RES-224/. 계획 fc095c323d0177401d34f1daa7b4d1c529e2351f, 착수 f3895893e32e2c055cefde446d34f1467fa27b4c. 의존 206 94e2c0ebe8fe36ad66ee1c23c05a91b3ae787db2, 207 ded4731e82fd2e9efd1e10cec6c60f2dd55f7259. dot-control.json 미변경.
- **결과판 SHA: 0cfc6fc18747ab78d4dcae2c0d1850ef6914c33f** (이 HANDOFF 바로 전). [RESULT](./RESULT.md), [SELF_CHECK](./SELF_CHECK.md), [SCOPE](./SCOPE.md), [sources](./sources.jsonl), [rows](./rows.csv), [ratios](./ratios.csv), [controls](./controls.csv), [cards](./cards.md), [observations](./observations.md).
- 단계별 커밋: ① 1c190d9295502e735668af726ae870d061b34fc8; ② 270fc3aa4637a57e2ad0a5f2de2f9bdb639b539e, fa969cbe7a1f882432a7bf911878f41c356efcf8, 08383002166c3fefba612913ea57988c65b1852a; ③ 238421b2478e2c8420fdb028bf2dbcc4b7ac7bde, 24b2a1e44b3c2d39f1a5b304f92211878ef12d1a; ④ 031a24b2c8e182590f52a0902b0d4a0cbdd557aa, c07fa6e77b4b017452a5bca2e00fb74303709ad6; ⑤ 9041a7cafec83c8af1143247cf0cda7d4326e2c3, 0a41c9e54de0996975950a10e22a4b7761c7214d, 0cfc6fc18747ab78d4dcae2c0d1850ef6914c33f. GitHub contents API에서 다중 파일 원자 커밋 대신 파일별 순차 커밋. 최종 HANDOFF 단독.
- 결과판 읽기 검토: 0a41c9e...에서 9개 파일을 다시 열어 Q별 근거/반례/미달과 표/행 위치를 대조. CSV 구분자 정정 후 0cfc6fc...에서 controls.csv 12행 전체와 RESULT/SELF_CHECK blob 동일성 재확인. RESULT blob 6c797377d3e6d7071f331323d999650042fe5394, SELF_CHECK f7c4915aebbd7cb5c0ce46a4c9649336d702b3e3, controls 609bc0761075a6d7af42287affa9f92ba47d2e95. 자체 수동 확인만 실시, 독립 검토·자동검사 미실시.
- 주요 판정: 005E/003E와 005E/001E의 역할 구분, 분모가중 합계, 지리 키와 계층의 중요성. 링크+문장만으로는 검산을 보류, 역할·원정수 추가로 분모/평균 오류를 거부, 지리·판·겹침 규칙 추가로 복제/주+카운티 오류도 거부 가능. 실제 사례 아닌 합성 구조 판독. 설명 자체에 오류가 있으면 A도 검출, C도 원행 오류에 취약. 2019–2023 ACS5 발표일 2024-12-12, 공표 당시 바이트와 조회판 동일성 미확인.

## 막힌 위치
공식 B23025 bulk 39,934,106 bytes reported (web reader size limit; 원기관 HTTP 상태 단정 금지); data.census.gov는 JS 요구; API 응답 미열람, 인증 여부 단정 금지. S09–S11. 다른 판으로 대체 금지. S2301/DP03/LAUS의 매칭 county 행, MLB game box 행, 실제 MOE/EA/MA 미확인. S18 worked example p6의 설명/식/번호 차이와 S14 지침 비교, S15 B23025 replicate 가용성 미확인.

## 다음 첫 행동 — Codex에서 실제 공식 파일을 수신 (아래 미실행)
실행·설치·자동 검사 요청 범위 제외인 웹 연구에서 실행하지 않았다. 승인된 환경에서 기존 도구 사용. 임시 디렉터리에서 원자료를 다루고, 결과/영수증만 owned_path 내 저장. 키가 이미 승인·제공되어 있다면 환경변수로만 사용, 저장소에 기록 금지. 과제 이외 경로 수정 금지.

```sh
git fetch origin chore/workspace-foundation work/research-af-res-224
git show 0cfc6fc18747ab78d4dcae2c0d1850ef6914c33f:docs/workstreams/research/AF-RES-224/rows.csv
tmp=$(mktemp -d)
url='https://www2.census.gov/programs-surveys/acs/summary_file/2023/table-based-SF/data/5YRData/acsdt5y2023-b23025.dat'
curl --fail --location --dump-header "$tmp/b23025.headers" "$url" --output "$tmp/b23025.dat"
wc -c "$tmp/b23025.dat"
sha256sum "$tmp/b23025.dat"
head -n 1 "$tmp/b23025.dat"
grep -E '^0500000US(06001|06003|48201|48301)\|' "$tmp/b23025.dat"
grep -E '^0400000US(06|48)\|' "$tmp/b23025.dat"
```

실제 헤더가 예상 pipe-delimited GEO_ID 첫 열인지 검사하고 다르면 CSV/TSV/pipe 파서를 그 헤더에 맞춤. B23025_E001/E003/E005와 M001/M003/M005(이름 실제 헤더에서 확인) 원 토큰, 파일 sha, 행 위치, HTTP 날짜/수정일 보존. grep 결과 공란이면 대체 값을 쓰지 말고 실제 행/헤더 형태를 확인. 주 행은 C4 통제에만 쓰기.

API는 동일 판에서 GEO_ID, NAME, E/M/EA/MA 확보 목적. 아래 GET 2개를 실행하고 본문이 JSON 배열인지 검사. 인증 필요 시 승인된 CENSUS_API_KEY가 있을 때만 --data-urlencode "key=$CENSUS_API_KEY" 추가. 오류도 보존. raw null/""/special code/0 구분. API/벌크 일치도 확인하되 EA/MA는 bulk에 없다면 API/공표 각주로만 보완.

```sh
api='https://api.census.gov/data/2023/acs/acs5'
vars='NAME,GEO_ID,B23025_001E,B23025_003E,B23025_005E,B23025_001M,B23025_003M,B23025_005M,B23025_001EA,B23025_003EA,B23025_005EA,B23025_001MA,B23025_003MA,B23025_005MA'
curl -fL -G "$api" --data-urlencode "get=$vars" --data-urlencode 'for=county:001,003' --data-urlencode 'in=state:06' -D "$tmp/ca.headers" -o "$tmp/ca.json"
curl -fL -G "$api" --data-urlencode "get=$vars" --data-urlencode 'for=county:201,301' --data-urlencode 'in=state:48' -D "$tmp/tx.headers" -o "$tmp/tx.json"
sha256sum "$tmp/ca.json" "$tmp/tx.json"
```

실제 값으로 ratios.csv에 U1+U2, L1+L2, 원분수, 평균 및 마지막 반올림을 채운다. rows.csv 48개 토큰 중 어떤 값이 진짜 0/결측인지 판정. 실제 4개 통제×3안과 카드의 동일 정보 노출 비교를 독립 검토자가 읽도록 한다. 원행 검증 전 현재 합성 통제를 실측으로 승격 금지. S14/S18 산식·MOE 재확인, S2301_C04_001E 및 DP03_0009PE/M/annotation을 해당 4 FIPS에 조회, LAUS 2023 annual averages XLSX (S24)에서 해당 FIPS와 자료원 차이 보존. MLB 공식 game feed gamePk 717838/718034로 원 경기 H/AB와 선수 ID 확인, 중복 경기 통제 분리. 정적 box 본문 실패 시 공개 stats API를 시도하고 실패도 기록.

후속에서 저장소 기존 계약에 따른 검사 명령(미실행): python -m workbench.session check af-res-224 --fetch (manifest 미생성/이름 및 사용법은 현재 AGENTS/도구 help 확인, owned_path 밖 쓰기 금지). 실제 CSV 열 수, 출처 ID 연결, 4 GEO_ID 48 원토큰, 2 파생율, 12 실제 통제를 검사할 재현 입력은 위 SHA의 rows.csv, ratios.csv, controls.csv. 독립 검토 여부 별도 기록.

## 색인 반영 제안
AF-RES-224: 지역비율 재사용의 역할·지리·판 보관 비교 / PARTIAL / result 0cfc6fc18747ab78d4dcae2c0d1850ef6914c33f / 22 직접 저작, 합성 12 통제, 실제 4 지역·2 유도율 미확인 / 다음 첫 행동 official DAT 다운로드와 API annotation 획득. 중앙 dot-control 및 색인은 작업자가 수정하지 않음.
