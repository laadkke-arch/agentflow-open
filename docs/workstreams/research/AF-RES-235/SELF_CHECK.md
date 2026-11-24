# SELF_CHECK — 자체 점검(독립 검토 미실시)
상태 후보 PARTIAL: 핵심 원문과 정오표/소비자 고정판 연결, 최소 자료 수는 충족; 요청의 실제 target id/name은 raw HTML 확인 실패(본문 절과 URL 요청은 관측), 실측 및 일부 날짜 결측. 사용자 요구에 따라 추정값을 확인으로 표시하지 않았다. 
| Q | 관측 근거 | 반례/반증 | 분모 및 미확인 |
|---|---|---|---|
| Q1 | W01–03, W10–12 | W03 제거 표시, W01 Controls 참조 차이 | 날짜판×SC 6/6 본문, raw target 0/6; 실패와 실제 부재 구별 |
| Q2 | W04–09, G01/02/09–13 | 2.2 2022 PR vs 2.0/2.1 2023 notes, 9/6 도구 출시 선행 | 2계열 errata 2/2; 2.1 3 재발행/2.2 1 재발행 관측; 2.0 #13 개별일·CfC 미확인, F08/F09 |
| Q3 | G01–08, G09–12, W01 Status | obsolete F77 자체가 링크 살아 있음, 규범력 없음 | WG category 11 distinct; 2 Understanding editions, 2 F77 editions; 당대 Understanding exact snapshot 미확인 |
| Q4 | A01–27, 4071/4075 merge, fixed release changelog | disable≠delete; aria stays active and review; actual public user A19 | 4 rules×2 tags 8/8; duplicate expected 6/6; fixture aria 2/2, generic same blob; active HTML 미확인; executed 0/6; image-alt expected 0/2 (control not run) |
| Q5 | W02,W05,W08,W09,G06,G08,A03,A06,A23 | synthetic C1/C2/C3; other criterion rather than automatic failure | 3/3 scenarios designed, observed actual audit 0 (not supplied); runtime 0 |
| Q6 | R01–10 | update≠replace; 7230 split; EID499 informative | RFC works/policy/erratum 10; selected direct RFC text/record 8; 2616 successors 6 listed, 7230/7231 original opened 2/6, 7232–7235 separate originals 0/4; EID date missing; 9931 detail missing |
| Q7 | W04/05, A18/19, G13, RFC controls | stale link, warning fatigue, loss of historic wording | 3 purposes×3 storage choices 9/9 evaluated qualitatively; cost measurements 0/9 |

## 수치 및 분류
- source ledger 71 rows: 62 direct opens (including 16 repeat-edition/alias paths excluded from unique count), 9 failures excluded. 46 counted works: W3C 9/7 target, WG 11/4, axe 16/6, RFC 10/5; total 46/22 target. 날짜판 Rec는 distinct edition, rule JSON file path/expected path는 각 work 하나(태그간 반복 제외); Understanding/F77 각 topic 하나; changelog one work, RFC original/status one work, EID499 separate erratum record. F07 raw failure not a claim of 0 DOM nodes. 성공 자료별 원 URL·location·observed claims·limitation·access status·count reason 포함. UTC individual first-open unavailable; window noted, G02 reopened. 
- 독립 변경 사건은 고유 저작 수와 별개: 주요 실질 변경 7개로 범위를 한정(2.2 removal, 2.0 Parsing erratum, 2.1 Parsing note erratum, 2.0 1.1.1 cross-reference erratum, axe deprecate pair A07, axe aria retag A08, 1.1.1 image-alt mapping 유지 대조는 변경 사건 아님, RFC2119 update R02); RFC 별도 대조 4개(2616 split 1, 7230 split/9110–9112 후계 묶음 1, 7234→9111 1, EID499 1) 중 첫 7에 포함된 RFC update 제외. 즉 WCAG 4 + axe 2 + RFC 5 = 11 독립 사건 묶음(분류 기준: 한 편집/정오표/관계 전환 단위; PR proposal, resolution, merge, publish는 동일 사건 내부 시점; 7231→9110은 2022 HTTP successor 묶음에 포함). 전체 역사 모집단은 미정, 독립 사건 11은 이 연구의 선택된 묶음 수이며 통계적 독립성 주장 아님.
- timeline.csv 22 records (6 initial cells + 16 event/republication/control rows), consumer.csv 8 records, citations.csv 3 records; TABLES.md intermediate, RESULT.md authoritative. 모든 실행 결과는 expected/static only. 사용자 설치, 감사 raw artifact, 법적 효과는 범위 밖 또는 결측. 
- P1 supported semantic, raw target unverified; P2 supported; P3 core only (cross-ref correction disproves byte identity); P4 supported A04–06; P5 supported RFC. 
- 2.0 erratum date range is inferential boundary from G01 and W04 last modified; not exact applied_at. PR2797 metadata was found at stage ④ after main observation and incorporated in revised timeline. 47차 plan SHA contains no task ID; start current task brief matched provided text and dependency fixed handoff; not substituted silently.
- 독립 검토: 0. 자체 점검: 위 반례/원문 대조 및 Q별 판정, 후속 result-SHA readback separately in HANDOFF. 제품/axe 실행 없음; static JSON/PR test fixtures inspected. No repository merge, no dot-control edits.
