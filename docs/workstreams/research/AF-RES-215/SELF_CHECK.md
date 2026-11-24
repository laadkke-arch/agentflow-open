# AF-RES-215 SELF_CHECK — 자체 검토 (독립 검토 아님)

- 판정: PARTIAL. 실제 자료 하한 충족(38/23); 원사건 4/4, Inoreader 6/4, OPML 4/4, FreshRSS 고정 8/7, Zotero 7/4, 별도 보강 9. 제외 9/47(7 실패 + 1 shell-only + 1 TTL test; 실제 row status 분류에서 실패 7: X02, X03, X05–X09). 13 공급 계보. URL 기준 중복 없음. Z03 재열람 산입; X02/X03 HTTP→HTTPS 재실패 1 work씩만 유지.
- 12/12 계획 필드 행: 2 목록 규격 양단, 4 OPML item-action 비지원, 6 archive 조건부 mapping. Same-direction actual 0/12 field observations (no sample of success/failure); fixed case denominator 4. 별도 1 incident S08 다른 수신기, 독립 사례 분모 아님. S02/S03 2 work /5 item sample shapes, not 5 cases.
- actual execution 0, external APIs called 0, no sign-in/new account, no runtime or test code execution. Public documents/code/test expectation reading only. Scoped to own path, no dot-control mutation. Other work 205–207 not read. No result from prior conversations presumed.
- 선행 노출: 작업 brief의 questions, URLs, fixed issues, anticipated counterexamples; 조사자가 초기 결과 작성 후 추가 검색·정정 수행. Blind/independent review not performed. Case authors and maintainers are evidence authors, not independent evaluators.
- SOURCE completeness: 47 line records, each source_id/work_id/lineage_id/question_id/case_id/url/author/version/checked_utc/location/finding/raw_value/unit/evidence_type/limitations/access_status/included/inclusion_reason. Dates for live docs checked date rather than false publication date. Issue comments counted within work. Public fixture values sanitized; personal attachment not opened. Code lines from fixed ref, not latest UI.
- Frame lists all source attempts and 12 planned slots now assessed, 4 fixed cases + 1 supplemental (not denominator). Explicit exclusions in SCOPE. fields.csv and migrations.csv include source references and separate field-specific observation. RESULT starts three required tables, ends with exactly three weakness rows. Prior revision and reasons REFINEMENTS. Source links included with ID/sections.

| Q | 판정 | 직접 근거 | 반례/미확인 | 다음 첫 원자료 또는 검증 |
|---|---|---|---|---|
| Q1 | 4 고정 case origin/status/후속 구분 | C01–C04 | success banner vs star 0; #4086 order; no exact same count evidence | C02/C03 comments and publicly sanitized paired report |
| Q2 | OPML standard/extension/no field | O01–O04 F02 F07 | nested parse vs actual folder; official examples timeout | X02/X03 accessible original; O03/F02 input comparison |
| Q3 | documentation+2 sanitized starred specimens; scope partial | I01–I06 S01–S05 | public article history != individual action export; no full ZIP | full public sanitized archive manifest/README, per-tag file/dates |
| Q4 | fixed code links 12 slots; no runtime | F01–F08 S04 | current filename/wrapper vs F09 historical patch; test belongs other reader | S02/S03 input fixed FreshRSS F06, compare DB rows |
| Q5 | 4 separate cases and supplemental S08 | C01–C04 F09 F01 S08 | same-account/field data absent; origin URL identity not confirmed | fixed cases followup and same-direction paired values |
| Q6 | cross-domain field/attachment/library boundary | Z01–Z07 | RIS notes partially supported; RDF export not full backup | RDF actual non-private specimen and attachment/collection mapping |
| Q7 | 3 routes and loss gates | I01–I06 F01 F05 F06 S05–S08 | closure/no original; narrow goal may need fewer fields | manifest, exact receiver version+output, closure condition |

### 자체 검토자와 검증 범위
현재 조사 세션 자체 검토. 이 단계 이전 4차 SHA db4f4a0a22e4fff189bd50fae8582f052c0d2047의 모든 파일을 GitHub에서 재열람해 원장/필드/사건/표/정정 확인. 최종 5차 SHA의 재열람 및 path scope 확인을 HANDOFF 작성 전 별도로 수행한다. 신규 테스트·벤치마크와 independent reviewer는 미실시. FreshRSS 고정 tree에서 import-specific fixture 찾지 못함; F07 bundled parser example, O03 default OPML, S04 다른 receiver expected output은 대체 증거일 뿐. RDF actual export fixture 미확인. PARTIAL 해소에는 원자료와 실제 출력 필요.
