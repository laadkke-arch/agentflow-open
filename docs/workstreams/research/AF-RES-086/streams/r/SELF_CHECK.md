# R 부분 자체 검산

범위는 R1·R2와 GitHub Pages 상태 해석이다. Q2의 RTD run 선택, Q4의 P3 동시 제공, Q6의 별도 사건 우선 표본, Q7의 타 분야 판 관계는 다른 스트림의 결과와 중앙 검산에서 결합해야 한다. 아래에서 그 빈자리를 R 자료로 대신 세지 않는다.

| Q | R 부분 주장 | 직접 원문 / 실행행 | 자기 결론이 틀릴 조건·찾아본 경로 | 다음 최소 확인 |
|---|---|---|---|---|
| Q1 | 두 고정 DESCRIPTION은 root를 안내하지만 구판 동시 제공·유지 기간을 찾지 못함 | R1/R2-REQ-DESCRIPTION·README·NEWS, 릴리스 원문, R1-MAINTENANCE·RELEASE-ISSUE; `claims.csv` | R1 주창±30일 issue/PR 생성순 #111–113과 #112 댓글을 읽었으나 기간 약속 없음. 별도 Discussions 영역의 약속은 남은 가능성 | 그 시기 발행자 원문에서 옛판 경로와 기간이 함께 명시된 행 |
| Q2 | 선택 생성물 네 HTML의 실제 Git blob 해시가 발행자 메타데이터와 같음; R1 메시지는 소스 접두만 기록 | `evidence/file-comparison.json`, R1/R2-GENERATED-COMMIT, GENERATED-ROOT/LEAF, PKGDOWN-MANIFEST; `curate.py`의 assert | 같은 소스를 사용한 다른 실행과 산출물 오인 가능성을 염두에 두고 Git commit·blob을 분리. RTD 두 실행은 이 스트림 범위 밖 | 실행 ID와 전체 source SHA 및 산출물 manifest를 묶은 공개 원로그 |
| Q3 | 선택 상태는 두 사례 모두 inactive 1개만 현재 남음; success는 직접 읽지 못함 | 배포·상태 원 JSON, R1 상태11개, R-SERVICE-STATUS, 404/빈 Actions 이력 영수증 | inactive를 구판 소실로 읽는 결론은 R1 NEXT/LAST의 동일 파일로 반박. NEXT12:37:22는 inactive12:38:03 직전이고 LAST16:07:18은 이후 | 선택 배포의 과거 상태 원행과 환경 URL. 현재90일 문서만으로 과거 success/삭제를 단정하지 않음 |
| Q4 | R 주창 실제 경로 판 식별0/4; 현재와 생성물일치2/4 | R1 정확 root/leaf CDX 빈배열; R2 주창/보조 CDX 빈배열; 현재4응답·생성4HTML; 보조 Feb27root1.1.11 | 빈 색인=미제공이라는 결론은 채택하지 않음. 보조 root는 실제 과거 응답이지만1.1.12전판 | 고정 창 안의 실제 경로 응답 또는 내용을 식별하는 날짜 붙은 발행 기록. P3 공동 조건은 다른 스트림 |
| Q5 | R1 withhold→generated_artifact; 현재사용 목적 R2 moving_alias 유지. 과거 제공 보류는 유지 | bundle2 고정 `prerecommendations.json`; `postrecommendations.json`; `local-check.json` byte불변true | 현재 판과 옛 생성물 판이 다를 수 있음(R1), 같아도 당시 제공을 입증하지 못함(R2). inactive 후 root내용이 남는 경우도 검사 | 목적을 바꾸지 않은 채 당시 응답·판 지문을 추가하여 권고 재판정 |
| Q6 | R1 재게시 스냅샷 반례는 고정 사례 내부 대조이며 별도 사건 표본 아님 | R1-NEXT/LAST-COMMIT·ROOT·LEAF, 재게시 원장 | 생성·게시 성공 뒤 잘못된 독자 경로라는 강한 사건 조건을 이 자료만으로 채우지 않음 | 별도 사건 우선 표본에서 build+publish+route+recovery 같은 ref 원행 |
| Q7 | 읽기/운영/서비스 계약의 요청과 바이트를 구분 | 영수증73개, `summary.json`; 검색2호출5식은 별도 `search-log.json` | 원자료 행46을46독립사건으로 세면 틀림: 계보3. gzip전달/해제바이트도 분리 | 서비스 제공자가 보존한 원상태·산출물·경로 기록. 타분야 제도·실제 판쌍은 별도 스트림 |

## 실행한 검산과 한계

- `python docs/workstreams/research/AF-RES-086/streams/r/curate.py` 실행 종료값 0. 고정4파일의 발행자 Git blob SHA와 직접 계산 SHA 비교, R1 현재두파일 불일치, R2 현재두파일 일치의 세 assert가 모두 참이다. 네 대표파일 외 전체 사이트 assets 동작은 검사하지 않았다.
- 출처73행·경로22행 ID 고유성, source→claim·route→source 참조, evidence 파일 존재, 묶음2 사전 권고의 byte불변을 확인했다. 최종 종료값0, 시각2026-11-23T15:10:00Z. `local-check.json`에 결과를, `local-check-history.jsonl`에 첫 검사에서 CURRENT claim 세 개의 정의 공석을 발견한 종료1과 정의 추가 후 종료0을 남겼다. 사전 권고 내용은 변경하지 않았다.
- 별도 에이전트가 원 영수증→다운로드 SHA, Git blob 네 개, 상태 원문, 카드의 HTML 원문/렌더링 구별을 읽기 전용으로 검산했다. 감사 지적에 따라 NEXT의 생성시각이 inactive 직전임을 수정하고 현재90일 정책의 판 표기를 명확히 했다. 중앙 감사 결과 파일은 부모가 연결한다.
- `workbench.session check --fetch`, 작업 브랜치 커밋과 원격 고정 결과 재열람은 부모의 작업이다. 이 하위 에이전트는 브랜치·커밋·push를 하지 않았다. 여기 적은 로컬 확인을 중앙 저장소 검사의 대체로 부르지 않는다.
