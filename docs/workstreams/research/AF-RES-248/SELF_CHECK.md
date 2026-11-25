# SELF_CHECK — 자체 점검
상태 PARTIAL. ① SCOPE 사전예측 이후 외부 자료 공개; ② 원장; ③ 표 및 matrix/events; ④ 실제 반례 추가 및 정정; ⑤ RESULT와 본 파일 각각 커밋; 고정 결과 재열람은 다음 단계에서 실제 실행. 별도 독립 검토 미실시. 사용자 지정 경로 외 변경하지 않음. 
## 질문별 확인
| 질문 | 근거 ID와 위치 | 반증 탐색 및 관측 | 아직 미확인 |
|---|---|---|---|
| Q1 | R1–R10; T1–T3; S1/S2; W1–W3 | R7/R8/R9 당시 표 끝과 R6 비교, B1 June19 예상과 R3 최종 선언 차이 | 1.14.0 당시 3.13 코드 지원 정확 범위, 최신표 publication date |
| Q2 | T1–T3 pyproject L54/55, classifier L65–68; P1–P3 release metadata; S4 | P3/T3 classifier 3.13 없음 vs R3/W3/P3 wheel | J1–J3 JSON file_requires_python; actual wheel METADATA 0 |
| Q3 | P1 L236–259; P2 L241–264; P3 L241–272; S3/S5/S7; D1–D5 | 표 시작/끝, all displayed rows, cp313t/abi3 none, sdist/macOS/musl 비교 | raw urls 0/3, historic deletion, binary bytes/hash |
| Q4 | R1–R3/R10; P1–P3; S6; B1–B5; release-events | June nightlies vs Aug stable wheels vs Oct Python final | exact published_at, upload_time_iso_8601, chronology within day |
| Q5 | W1–W3/T1–T3; C1–C3; B1–B6 | B2 dev build success but later no run and Windows issue; B5 aarch64 error; B6 cp313t mac failure with log timestamp | exact release tags target job logs, matching digest, user install |
| Q6 | N1–N4 model notice and product date | Windows correct host/wrong model; D850 already 1.31; Z6II already 1.70; Linux host path not asserted | exact downloadable archive hashes, host execution/camera installation |
| Q7 | M1–M9; R6; S7; recommendations | patch shift 3.13, minor shift 3.9, glibc and free-threaded opposing conditions | current user's environment, latest specific compatible file selection |
 
## 분모 및 관측 구분
- 계획 21개 고유 최소 5/6/5/3/2; 원장 50 rows, 32 counted, categories 8/9/7/6/2; 19 lineage (same work/tag blob duplicate not counted). B3/B4 publisher configuration discussion, B1/B2/B5/B6 reported build/test observations; raw exact release CI receipt none. 8 failed, 10 opened supplementary/un-counted. 9 analytic event groups (not statistically independent); release-events.csv 29 events rows including multiple views of one event, raw exact time incomplete.
- Main 9/9 rows: rendered HTML positive 5/9; displayed absence 4/9, NOT raw absence. Raw arrays 0/3; 83 HTML entries (24+1,24+1,32+1) observed, raw denominator unknown. 5 positive file names/date/hash/URLs observed, 0/5 exact UTC; 5 direct binary read failed, digest recomputation 0/5. File requires_python 0/9; for absent HTML rows per-file metadata not applicable to nonexistent displayed candidate but raw unknown. 9 static support/metadata judgments; exact target CI 0/9, not a test failure count.
- Controls: 3 sdists/3 visible, 12 mac-control rows (8 positive files + 4 no match, 9 environment cells with additional min-OS variants), 3 free-threaded cells/0 displayed matches. Total matrix 27 rows, 9+3+12+3. 2 Nikon models, 2 notices and 2 listing dates. No install or firmware update.
- 3 exact tag SHA status queries/3 workflow queries returned 0 items; observed 0 for those query filters only. User install/tests 0 performed by scope. Historical absence, actual users, specific OS/glibc/pip and dependency lock unobserved. Announced dates visible, timezone unverified. No false conversion of unknown to zero.
- Stage ③ preliminary table → ④ corrections: full HTML table coverage 3/3; 1.14.0 code support possibility from B1; classifier failure counterexample; B5/B6 actual report scope. Source time window 2026-11-25 session approximately 00:09 UTC onward; exact source-access upper bound not logged; no fabricated exact seconds. 
- Expected re-read: 8 files SCOPE.md/sources.jsonl/matrix.csv/release-events.csv/TABLES.md/recommendations.md/RESULT.md/SELF_CHECK.md at result SHA, exact headers and CSV widths, links and sources, path diff. Receipt and result SHA in final HANDOFF; external live links not all re-opened after commit; initial direct observation and fixed repo re-read distinct.
