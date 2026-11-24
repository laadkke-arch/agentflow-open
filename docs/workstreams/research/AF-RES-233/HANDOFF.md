# AF-RES-233 HANDOFF
**PARTIAL** — 기관 전거·서지·규정·교재·지침을 판독하고 설계 비교 및 반례를 남겼다. B Kate Davis 두 실제 기관 원레코드 0/2이므로 완료 조건 미달. C와 GNIS로 B를 채우지 않는다. 제품 구현/설치/새 유료 API/중앙 진행표 수정 없음. 자체 점검만 실시, 독립 검토 없음.

## 고정 입력 및 결과
- repository laadkke-arch/agentflow-open; branch work/research-af-res-233; owned_path `docs/workstreams/research/AF-RES-233/`.
- 계획 914dbfa789ebec97063ed97130ea2a71c2e9f503에는 233 직접 항목 없음. 착수 610bcdf35a3dc04bc7f55ce1ecf0a339d9d881e6 (+6/−0, 변경 dot-control.json만). 실제 RUNNING brief, 경로와 depends_on 확인. AF-RES-222 result fe41449d156eb5e723c254a0530863468c084480 중앙 DONE/자체 PARTIAL 유지. 227–229 입력 사용 안 함.
- **결과 고정 SHA (HANDOFF 직전)**: 157d1152dc4f6169d68addaecc149f3761c86e3a
- ① 범위·사전 봉인 9be61a5202fc74c7639d5d06f8fb23c596fd2e7d
- ② 원자료 원장 64c4dc7dee449078a5612e63e1c763a5b828a540, ②b 공식 교재 회복/GNIS 추가 17059a89b8f626ce7b0e28ce7d3bafc7023f77b2
- ③ 필수 표와 CSV 주관측 08fa06818a51b56ba766eaa63715919caf6b1dbc
- ④ 반례·정정·미확인·3×3 판정 2cc1e8591ea52b8fc7074606ea1e1828d2ecea5f
- ⑤ RESULT/SELF_CHECK 157d1152dc4f6169d68addaecc149f3761c86e3a
- ⑥ 이 HANDOFF만 단독 마지막 commit. Git 자기 자신의 SHA를 본문에 넣지 않음.

대표 파일: [RESULT.md](RESULT.md), [sources.jsonl](sources.jsonl), [authority.csv](authority.csv), [works.csv](works.csv), [decisions.csv](decisions.csv), [COUNTEREXAMPLES.md](COUNTEREXAMPLES.md), [unresolved.md](unresolved.md), [SELF_CHECK.md](SELF_CHECK.md), [SCOPE.md](SCOPE.md), [TABLES.md](TABLES.md). 고정 결과 SHA의 파일 10/10 실제 GitHub 재열람(2026-11-24T23:09:40.614Z). JSONL 52행 parse, 27 직접 내용 열람, counted 고유 work_id 25, lineage 8, 중복 source_id 0, 필수 키 누락 0; 미열람/실패/검색 후보 25행, 성공한 동일 원자료의 다른 형식 2행 미산입. CSV 데이터행 authority16, works14, decisions9. RESULT 첫 표 헤더와 둘째 표 헤더 일치, Q1–7 존재, 참조된 개별 source ID 미등록 0, 마지막 약점 세 행 및 반전 조건 확인. E01/E04 동일 교재, G05/G06 동일 서비스; E02 mirror-only로 엄격 기관-host 기준 24/25. result vs 착수 +6/−0, 파일 10개 모두 owned_path, dot-control 변경 없음. branch RESULT blob=고정 SHA RESULT blob. 이는 파일 구조/참조 자체 점검이지 원천 API/제품 실행 또는 독립 검토가 아니다.

## 결론/분모와 약점
- A 역사 n79090096 2004 전사(2008 교재) 안에서 100 Tennessee Williams와 400 Thomas Lanier, 670 근거 관측. 현재 LC 0/1, 010/005/100/400/500/670 current 0/6. NDL A05 외부 exactMatch이지 LC 원필드 아님. 로마자 전사 parsed 화면 불일치와 screenshot 실패.
- B 두 교육 자리 2/2, 실제 기관 전거 0/2, 실제 저작 역방향 0/3. 검색 미확인 != 존재 부재. 절대 C 대체 금지.
- C BnF 2/2 및 NDL 추가 2/2 별개 자체 번호/출처, BnF 대표 저작 role 2/2. LC 0/2, VIAF 원클러스터 미열람. BnF Jalin 공동 필명 관계 반례, W01 한 서지 두 Dumas, W05 subject != author. 서지 5 표시, underlying 작품 4, raw MARC 및 표제면 영상 각각 0/5. 
- 400은 same authority 검색 안내, 500은 관계 탐색, canceled/invalid 010 z는 이력과 명시 교체시만 redirect. 현행 LC 500/취소 사례 미확인. obsolete ISNI 별개 namespace. GNIS 지침/서비스 5, 실제 ID pair/variant 0/3. 공식 2026-10 서비스 schema만 확인, 실제 query 실패, 0 rows 아님. 
- 독립 지정 실체 사건 A/B/C 3개 중 C 1개 부분 확인, A/B 2 결측, 완결 0/3. 지정 5자리 완결 0/5, C2 부분, A1/B2 결측. 자료 수 25≠사건 수. 
- 가장 중요한 약점 세 건은 RESULT 마지막 표: B 원레코드, LC 원필드와 취소, 실제 GNIS/표제면. 실제 검사 기대와 관측은 구분.

## 다음 첫 행동 (재개, Codex/웹 원문)
**첫째 B**: LC Authorities https://authorities.loc.gov/ 에서 Davis, Kate 1951- / 1959- / 무수식 exact 및 variants, LC Catalog https://catalog.loc.gov/ 에서 Rough road c2000, Secretary of the Interior 2003, Raptors of the Rockies 2002를 제목+책임표시 역검색. 후보 ISBN 9781584760412 / 9780878424610, 후보 bib https://lccn.loc.gov/2002004917 는 아직 확인 안 됨. 교육 E04 L3613–3642, E02 정답은 검색 입력만. 원기관의 영구 URI/010/005/100/400/500/670, bibliographic 100/700 $0/$1/역할과 판/실물 표제면을 대조. 양쪽의 고유 ID+해당 저작 연결 확인이면 B 판정 갱신; 없거나 충돌하면 보류, 이유 기록. A와 C, 실제 GNIS, cancellation 재개 주소/판은 unresolved.md.

## 실행 담당에 넘기는 명령·입력 (미실행)
아래는 공개 정상 조회 및 읽기 전용 확인 제안이며 이 세션에서 shell/API/테스트를 실행하지 않았다. 응답 실패/429이면 중단하고 상태와 원주소 기록, 인증 우회/요청 반복 금지. 실제 원자료 회수 후 SHA256/UTC/HTTP status/정확 판을 기록하고 evidence ledger를 갱신. 다음 예시는 결과 저장소 외 임시 디렉터리에 쓰고 승인된 owned_path에 근거만 반영.

```sh
git checkout work/research-af-res-233
git show 157d1152dc4f6169d68addaecc149f3761c86e3a:docs/workstreams/research/AF-RES-233/RESULT.md
# LC: F02와 동일 정상 공개 MARCXML 후보. Accept/형식은 성공 응답에서 확인.
tmp=$(mktemp -d)
for id in n79090096 n79042162 n81120314 n80022124 n80014241; do
  curl --fail --location --max-time 30 --silent --show-error \
    -H 'Accept: application/xml' \
    "https://id.loc.gov/authorities/names/$id.marcxml.xml" -o "$tmp/$id.xml" || break
done
# HTTP success라도 XML/record가 실제 맞는지 확인; 오류 HTML/redirect를 근거로 세지 않음.
python3 - "$tmp" <<'PY'
import sys, pathlib, xml.etree.ElementTree as ET, hashlib
for p in sorted(pathlib.Path(sys.argv[1]).glob("*.xml")):
    raw=p.read_bytes()
    try: root=ET.fromstring(raw)
    except ET.ParseError: print(p.name,"not XML"); continue
    print(p.name,"sha256",hashlib.sha256(raw).hexdigest())
    for e in root.iter():
        tag=e.attrib.get("tag")
        if tag in {"005","010","100","400","500","670"}:
            print(tag, e.text if tag=="005" else [(x.attrib.get("code"), x.text) for x in e])
PY
# GNIS: official National Map 2026-10 release G05/G06; actual data refresh may change.
curl --fail --location --max-time 30 --silent --show-error --get \
  'https://cartowfs.nationalmap.gov/arcgis/rest/services/geonames/FeatureServer/0/query' \
  --data-urlencode 'where=gaz_id IN (735864,400107,203868)' \
  --data-urlencode 'outFields=gaz_id,gaz_name,gaz_featureclass,state_alpha,county_name' \
  --data-urlencode 'returnGeometry=true' --data-urlencode 'f=pjson' \
  -o "$tmp/gnis.json"
python3 -m json.tool "$tmp/gnis.json"
```

LC 정상 기대: 실제 MARC record 내 010 $a, 005, 100, 400, 500, 670 및 z를 판별하고 E04 역사 화면과 비교. 후보 n80022124/n80014241는 R01 규정 예제라 실제 replacement 관계가 확인되기 전 redirect 금지. XML이 없으면 공식 LCNAF 배포/authorities UI의 MARC export를 정상 경로로 확인. B의 경우 실제 authority 번호를 얻은 뒤 같은 input에 추가. 다른 010 또는 역할 근거, 500 relation 및 변경판 충돌은 현행 연결 가설을 반전시키며 기관 주장/판을 남긴다.
GNIS 정상 기대: Springfield 서로 다른 ID의 actual name/class/state/county/coordinates 확인. JSON `error` 또는 features 필드 없음은 실패; 실제 빈 features 배열만 해당 질의·판의 0. WFS schema에는 variant 없음: G03 https://www.usgs.gov/us-board-on-geographic-names/download-gnis-data 에서 최신 DomesticNames 및 Topical All Names, 동봉 XML metadata 다운로드/정확 파일명 및 hash, Feature ID로 join; 상세 페이지 F18–F20 CSV 및 variant 탭 확인. North Springfield in-part가 전체 이름 동치인지 원값 확인. ID/좌표/종/이형 값이 후보와 다르면 그 후보 철회. 
설계 테스트 입력: authority.csv, works.csv, decisions.csv, sources.jsonl. 400 same verified record→search redirect, 500/Jalin→related not union, $z only verified replacement→redirect with old literal, C normalized name→2 candidates, W01 both agents, W05 subject not author, B unknown→hold 2 educational candidates, A current not verified→hold; GNIS 실제 rows 확보 후 ID disambiguation. 실제 기대값 검증 코드/제품 실행은 아직 0. 원자료 또는 사용자 판별 요청의 역할이 달라지면 갱신.

## 색인 반영 제안 (중앙 수정하지 않음)
index 키워드: authority identity vs record identity, name literal/variant/related, namespace+ID, bitemporal revision & source, 010 canceled/invalid, role edge, bibliographic work/edition, collective pseudonym, cross-institution provenance, GNIS unique feature IDs. 222의 code alias 규칙과 사람/공동 필명 차이: 동일 기관의 동일 레코드 400만 검색 안내, 관련 접근점은 별도; 원래 인용/판 보존; 미확인 후보 공개 추천으로 승격 금지. AF-RES-233 PARTIAL 그대로 등록; B 확보 전 DONE 금지.
