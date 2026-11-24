# AF-RES-149#1 보충 자체검사 — 실제 실행 결과

검사 대상: 원 fbd9a00b105da2666af5a158ee2678740572cf38 / 보충 결과 d8bf7d96dc4c6d158fc37d707357889a08057799. 2026-11-24 UTC. 실행·판독·추론 구분. 제3자 독립 검토나 제품 실행은 하지 않았다.

| 검사 | 실제 방법과 결과 | 판정/한계 |
|---|---|---|
| 사전등록과 순서 | f9438d8c45d0c02b3cde985c06897c534b552407 PROTOCOL 커밋, 이후 모집 원장 커밋 055fa2a4ac1348f9e64a96fbfc20835fc5013a93 | 사전 고정한 2창·3경로·R1~3·첫 6순위; 성과를 본 뒤 날짜나 경로 변경 없음 |
| 원본 무결성 | GitHub fetch_file로 기준/결과 SHA 양쪽 SCOPE, frame, paths, sources, judgments, cost, OPTIONS, RESULT, SELF_CHECK, HANDOFF 각각 blob SHA와 내용 일치 10/10 | 통과(인계 갱신 직전까지); 마지막 HANDOFF만 변경 예정 |
| 범위 | GitHub compare_commits fbd9a00b… → d8bf7d96… ahead 17, behind 0, 파일 17개 모두 supplement/ 신규, 기존 수정/삭제 0 | 통과; 최종 인계 직전/이후 별도 범위 확인 |
| 모집 원장 재개봉 | CSV parser로 frame 36행×14열, paths JSONL 36행, event_id 각 36 고유. 실제31, 시도31, 열림21, 실패10, 구조적 없음5 | 통과(기록 보존); 원 32/36 유지, 누적 63/72. 모집 부족 4의 누적 보완, 각 셀 6개는 실패 |
| 판정 원장 | judgments 108행×16열, (event_id,requirement) 108 고유, frame 및 primary source 연결 오류 0. 실제 93쌍/미관측15, strict 0. historical_diagnostic의 partial/transfer 및 relaxed direct는 별도 열 | 통과(분리); R1~R3 각 동일 기준, 노출 수치 미사용. 독립 블라인드 아님 |
| 출처 | JSONL parse 성공 sources37, paths36, history20+addendum4, languages18; source_id 고유 37/37·history24/24, secondary8 | 원 41 산입+보충17 산입(기록 58, 중복 work_id 제외 56). 보충 진단/언어를 산입 하한에 추가하지 않음 |
| 원 비용 | 재개봉한 원 CSV의 24행×24 수치 필드를 집합 및 분모에서 재계산, 576/576 일치 | 통과; 원 값 수정 없음 |
| 보충 비용 | 결과 저장 이후 frame·sources·cost를 별도 재개봉, route/window/budget별 실제/예정/결손/시도/성공/제작자/중간/실패/고유 라벨/자리 상한 10항목×24행 재계산 | 240/240 일치; 2차 및 진단 판정은 recalculation.json에 생성 시 산출. 같은 실제 시간 예산 증명 아님 |
| 교집합 | 원 label 29, S1 28, 겹침 zed/electron/seaorm 3, 합 54; 실제 자리 상한 63 | 동일성 미결 유지 |
| 시간/호출 | calls.csv 59행×9열; web_batch 142 subrequests, search_commits15/search_issues4/fetch_file12/fetch_commit8 = GitHub39, shell3; final_attempts W20 +6 web | 연구 원장 합 web148/20 tool invocations, GitHub39, shell3. web bracket은 상한, 내부 개별 wait는 미확인. 작업관리 호출 제외 |
| 외부 재방문 | W20 archive availability 5 접근 불가, 프랑스어 과거 큐레이션 본문 직접 열림. 2025 정확 노출값 복구 0/63; 2026-11-24 두 한국어 실제 발견 점수 별도 | 실패와 무결과 구분; audience 대체 금지 |
| 로컬 계약 | git ls-remote GitHub 2회 DNS 실패 exit128; curl TWIR DNS 실패 약4.767초. 2차 git 16:11:20.329–16:11:20.345 UTC | checkout/contract CLI 미실행, 검사 통과 주장 금지. GitHub 커밋 비교는 계약 CLI 대체 아님 |

재계산 방법: CSV 인용부호/이스케이프 처리 후 event_id 집합, route/window/position<=3 또는6 필터. attempted=1 실모집, opened=1 성공, sources.type=maker 제작자. 다른 성공 중간, 실패=attempted-opened, 결손=planned-attempted. 고유 work_id Set, 실제 자리 상한. primary_status에서 직접/부분/전이 적격 집계, secondary_strict_status와 relaxed 및 historical_diagnostic_status는 각각 따로 계산. A 대비 추가는 같은 창/예산 차집합, 0분모는 산출 불가. [cost.csv](cost.csv), [recalculation.json](recalculation.json), [historical_judgments.csv](historical_judgments.csv). 실제 수행된 원 비용 576 필드 비교와 보충 240 필드 재계산의 오류 0을 확인했으며 모든 텍스트 주장/런타임을 자동 검증한 것은 아니다.

결과문 검토: 첫 세 표는 경로/비교/대안, 그 뒤 Q1~7 및 정확히 3약점. 주 비교 0 S1, 2차 완화1, 추가 역사 진단2 분리; 원 역사 후보 2→4는 추가 증거, 원 판정 그대로. 원+보충 역사 진단6 후보/11쌍은 가변 비용, 직접 0; Notesnook 현재 직접1은 비교 밖. Telegram JSON 추론, ciphernotes 당시 APK/자동 reconnect, Calisthenics 정확 편입판 미확인. 언어 날짜 목록 4/4이나 Show 전용 과거 미확인. 현재 지표를 2025 값으로 소급하지 않음.

**판정: 보충 실행 및 저장/재열람 검산 완료. 원 과제 strict PARTIAL 유지.** 추가 표본은 구조적으로 존재하지 않는 자리와 정확 역사 지표의 증거 결손을 지우지 않는다. 다음 첫 단계는 실제 전문 목록 6개 이상이 있는 독립 사전등록 창, 한국어 동일 종류 역사 목록, 2025 snapshot/정확 배포판 및 네트워크 가능 환경의 계약 검사. 원 원장은 보존. 최종 HANDOFF는 이 문서와 결과 저장 뒤 단독 커밋한다.
