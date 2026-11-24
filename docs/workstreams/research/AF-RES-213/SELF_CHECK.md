# SELF_CHECK — AF-RES-213
- 작성자 자기검토: 본 작업 대화의 동일 작성자, 독립 검토자 아님. 별도 에이전트/사용자 검증 0. 검색 결과 노출 후 판단; 모집·판정규칙을 SCOPE에 먼저 커밋했으나 blind review 아님.
- 기준 branch 87ffc1539bcf33da0fccf45eb15982a02d93e409, planning bb146773bbffba5e724e8c842951e2c25198c2da, AF-RES-202 cc543b8d1b8f8748fa363999b76a55f05de2266c. 최초 control 접근 실패 정정은 SCOPE. 작업 경계 내 파일만 쓰고 dot-control/제품 DB/다른 브랜치 변경 금지.
- 표집: A 7/7, B 5/4, C 15/5, D 7/4, E 5/3 = 39/23 고유 work_id; ledger 총64(39 산입 +18 열람 비산입 +7 실패). 7/7 actual XML, 동일 A03 parent 1개, 3 locale all same term. 12/12 목적 자리, 24/24 consumer static rows. 원제보 6 사건, 자료 7; 정확 A01/A02 직접 제보 0/2, exact journal→merged XML→회신 1(R04 Nature Communications). 프레임 78행(64 source+12 purpose+2 gap/exclusion). 검색 요약·실패·미러/동일 work는 하한 제외; vendor/version duplicates 및 post hoc contrast conservatively not counted. 날짜는 작업 시작 UTC 환산이며 exact retrieval time 미측정.
- 목적별 추천: 자료 존재/내용/선택/load 각각 구분; locale file과 installed assets 구분; same parent different locale와 동일 약어 충돌 실제 XML/JSON 사례 확인. No new programs/benchmarks/renderers, 실행 0. GitHub connector의 JSON 읽기 및 정적 집계만 사용. 
- 자체 점검 표:

| Q | 직접 근거·결손 | 반례/경쟁 설명 | 판정/다음 원문 |
|---|---|---|---|
| Q1 | A01–A07; B01–02 | template != parent; alias zero body | 7/7 XML 직접 판독; runtime 별도 |
| Q2 | A03/04, B01/02, C02, D04/D07/X05 | shared edit changes siblings; R02 wrong parent | independent copy for local format; journal official docs F01/F07 blocked |
| Q3 | A05–07 term/date, A04 override, B03–05 existing fixtures; C03/C12 | X12–17 same parent different locale; same et-al/symbol not all differences | source-derived, fixture expected not measured; missing-unit fallback runtime |
| Q4 | C01,C03–14,X01–02,X06–08 | wrong basename; hidden vs remote; bundled != installed | two consumers pinned; version-specific offline check required |
| Q5 | D01–07, X03–05,X09–11,X18 | R02 actual bracket parent; data instead of style; same abbreviation multiple keys | R04 same journal link confirmed; two target journal reports & publisher access missing; PARTIAL |
| Q6 | E01–05 actual WP files + rules | specific parent vs generic child; functions.php both; CSL forbids dependent layout | domain distinction supported; activation untested |
| Q7 | objects/resolutions/requests; all above | already present; data field missing; locale in-style override | 12×2 static classification complete; consumer installed inventory remains unknown |

- evidence classification: 직접 XML/JSON 내용/metadata, 제작자 문서 및 고정 source rule, 당사자 보고, 기존 시험 expected, 추론 분리. 실제 cache hit 0, offline success 0, journal approval 0. 명령 및 입력 제안만 HANDOFF에 기록.
- 정정: SCOPE control source/API; R02 historical Nature -> actual nature-brackets X09/X10; R03 exact path 404 not total absence; R04 alias X11 checked; E05 supplemental; frame actual count fix. 이전 판은 phase 1–4 commits에 남음.
- RESULT 시작 3 필수 표 순서/열, 마지막 3 약점; source ledger에서 URL/구간 참조. 완성 SHA의 파일 재열람·행 수 검사 및 branch path 비교는 별도 HANDOFF에서 결과 기록(이 문서 시점에는 미실행). 
- 상태 PARTIAL: 하한과 정적 자리 충족, 정확 대상 저널 사용자 제보/현재 official instruction 미확인. 렌더 실행은 범위 제외이며 이를 완료한 것으로 적지 않음. 다음 첫 행동: 정확 두 저널 official guideline/author report+matching changes, 이후 별도 권한 Codex offline trace. 
