# AF-RES-033 현장 적용과 수신 후속: 관측 범위를 분리한 분석 초안

## 이 분석에서 말할 수 있는 것

**현장 자료는 공표·정정·상태 변화의 일부 절차가 실제 사건에서 사용됐음을 보여 준다. 수신 8건의 후속은 승인, 대체 제안, 구현 단계, 현재 문서의 동작을 구별하게 한다. 이 자료만으로 이번 검색이 반환한 제공 원리를 수신 팀이 채택했다고 판정할 수는 없다.** 직접 제공 원리의 인용과 그 인용이 결정을 바꿨다는 인과관계는 8건 모두 미확인이다. 아래 각 행은 현장 원장 F01–F04 또는 후속 원장 R01–R08·OUT-*의 원문 위치로 돌아간다.

이 초안은 이미 수집된 원장과 캐시만 읽었다. 새로운 웹 검색이나 새 후보 선정은 하지 않았다. 이 판독자 문맥에서 통계 48대응의 최초 판독은 후속 결과를 보기 전에 끝났으며, 이번 후속 인지로 그 판정·후보·질의·원 순위를 수정하지 않았다. 분석 전후 judgments/statistics.jsonl SHA256은 06241f054fd43ac3705111dfd898394e0b6445eab27666e5b4679905f12bd337로 같다. 별도 모델 문맥의 판독과 사후 재검이지 독립 인간 평가 실험은 아니다.

## 1. 시간·분모·직접 열람의 경계

| 관측 단위 | 확인한 범위 | 근거 원장·정확 위치 | 이 범위로 말할 수 없는 것 |
| --- | --- | --- | --- |
| 검색 봉인 | a2ce15d10415c556574d1a65af77718a81052d01, 2026-11-22 17:12:59 UTC. 16회 원 검색과 48개 반환창을 후속 전에 봉인한 커밋이다. | [봉인 커밋][seal]; 이 초안 시도 원장 FF-003의 읽기 전용 git show 영수증 | 후속에서 좋은 결과가 나왔다는 이유로 원 검색의 적중을 고칠 수 없음 |
| 원 수신 PR 후속 | R01–R08 메타데이터 최초 조회 2026-11-22 17:14:22.179–17:14:28.621 UTC. 모두 위 봉인 이후다. 원 PR 5개 병합, 3개 미병합 종료. | [outcome-observations.jsonl](../recipient/outcome-observations.jsonl), R01–R08의 fetched_at_utc, merged, outcome_seal_commit | 미병합 종료 3개를 같은 이유의 거절로 묶을 수 없음. R03·R07은 대체 PR 경로가 있음 |
| 공개 토론 문자열 검사 | 댓글·리뷰 기록 1,315개 중 비어 있지 않은 본문 913개, 별도로 현재 PR 본문 8개. 35개 캐시 입력, 공식 제공기관 도메인 18개에 대해 소문자 literal substring 검색 결과 0건. | [followup-citation-screen.json](../evidence/followup-citation-screen.json), scope/matching/domains/per_recipient/hits. 이 초안에서 27개 토론 캐시의 1,315/913 합계도 재계산 | 기관 별칭, 간접·의미 인용, 연결 구현의 모든 파일, 비공개 대화, 개인의 사전 지식이 없다는 증거가 아님 |
| 의미를 읽은 후속 | 기존 substantive_read_subset은 45개 기록. 이번 초안은 표의 핵심 댓글 13개, 연결 PR·이슈 본문 4개, 현재 공식 문서 3개 해당 절을 캐시에서 직접 재독했다. | 아래 후속 표의 댓글 ID·문서 절. [outcome-linked-sources.jsonl](../recipient/outcome-linked-sources.jsonl), [outcome-doc-sources.jsonl](../recipient/outcome-doc-sources.jsonl); 7개 연결·문서 캐시 해시를 원장과 대조 | 913본문을 전부 독립 의미 판독했다는 뜻이 아님. 일부 내용을 읽은 범위와 문자열 검사 범위를 합쳐 부풀리지 않음 |
| 별도 현장 검증 | 고유 원문 4개, 교통·통계 2분야, 사건 3개. F01·F02는 같은 MTA 감편 과정, F03·F04는 다른 ONS 정정 사건이다. | [field_sources.jsonl](../field/field_sources.jsonl), F01–F04의 duplicate_group; [현장 재개 감사](../field/resume-field-audit.md) RF-A01–RF-A04 | 독립 사건 4개, 독립 운행 측정 두 벌, 세 제공 분야 전체의 현장 검증으로 표현할 수 없음. 도서관 현장 사건은 이 4원문 묶음에 없음 |

정확 도메인 검사 목록은 spl.org, denverlibrary.org, multcolib.org, tpl.ca, hclib.org, vpl.ca, ons.gov.uk, statcan.gc.ca, abs.gov.au, bls.gov, bea.gov, stats.govt.nz, kingcounty.gov, mbta.com, ttc.ca, translink.ca, trimet.org, sfmta.com이다. 해당 문자열을 포함하는 하위 도메인은 검출하지만, 본문에 도메인을 쓰지 않은 기관명·책·구두 전달을 검출하지 않는다. 따라서 적절한 표현은 **“정해진 공개 본문 범위의 제공기관 도메인 문자열 일치가 없었다”**이다. “타 분야 지식이 없었다”나 “독자 발명임을 입증했다”는 결론은 붙이지 않는다. 근거는 위 기계검사 영수증이다.

## 2. 수신 8건: 결정·구현·인용을 따로 판정

현재 문서는 2026-11-22 17:19:27 UTC에 캡처한 가변 페이지다. OUT-DOC-*의 raw_sha256으로 이 판을 식별한다. 현재 문서가 설명하는 동작과 2020년 최초 설계의 모든 필수 조건을 같게 취급하지 않는다. ‘직접 인용 미확인’은 각 PR의 기계 검색 0건과 한정된 의미 판독을 뜻하며, 개인의 지식 부재를 뜻하지 않는다.

| 수신 ID·최초 목적 | 후속 결정과 정확 근거 | 구현·동작에서 실제 확인한 범위 | 제공 원리 직접 인용·채택 | 남는 미확인과 결론을 바꿀 첫 자료 |
| --- | --- | --- | --- | --- |
| R01 — asm! 이름을 바꾸되 기존 호출을 연결하고 이후 경고 | RFC #2843은 2020-03-20 병합. [수락 댓글 601564223][r01-accept]과 outcome-observations:R01 메타데이터. | [구현 PR #68404][r01-impl] 본문 두 번째 문단은 기존 asm!을 llvm_asm!으로 forwarding하되, stdarch 등 하위 모듈 이주 때문에 deprecation은 아직 하지 않는다고 명시. 2020-03-27 병합 메타데이터까지 확인. 원장 OUT-R01-rename-implementation. | 직접 제공 인용·인과적 채택 모두 미확인. 댓글/리뷰 36기록·32본문 및 현재 PR 본문에서 도메인 일치 0. 수락/구현은 제공 자료의 영향 증거가 아님. | 최초 요구의 경고 조건까지 완료됐다고 할 수 없음. 첫 자료는 수락 댓글이 연결한 [추적 이슈 #70173][r01-track]와 #68404 뒤의 실제 deprecation 변경·컴파일 진단 시험. 어느 릴리스에서 경고가 추가됐는지를 확인하면 단계 완료 판정을 바꿀 수 있음. |
| R02 — 하위 trait의 항목 선택과 명시적 충돌을 구분 | RFC #2845는 2021-09-21 병합. [댓글 720705642][r02-choice]는 supertrait 변경의 호환성 동기와 호출자 disambiguation을 지지. [댓글 910114408][r02-boundary]의 첫 답변 문단은 명시적 Sub + Super와 무관한 trait 충돌의 일관성·사용 지점의 문법을 논함. 원장 outcome-observations:R02. | 이 조사에서 컴파일러 구현 PR, 배포 버전, 실행 결과는 확인하지 않음. 현재 PR 본문과 승인 토론은 설계 의사결정 근거다. | 직접 제공 인용·인과적 채택 미확인. 40기록·40본문 및 현재 PR 본문에서 도메인 일치 0. 유사한 선택 규칙이 다른 분야에서 보인다고 기원을 확정할 수 없음. | 다음 첫 자료는 [병합된 RFC #2845][r02-pr]에서 연결되는 구현·추적 기록. implicit Sub, explicit Sub + Super, fully qualified 두 호출을 같은 고정 컴파일러에서 비교할 시험·출시 커밋이 필요. 병합 사실만으로 실행 의미가 모두 구현됐다는 결론은 달라지지 않음. |
| R03 — inline asm의 입력·출력과 lateout 재사용 경계 | 최초 #2850은 2020-03-03 미병합 종료. [댓글 593702000][r03-continue]은 긴 토론을 #2873으로 이어 간다고 명시. [후속 #2873][r03-replacement]은 2020-07-20 병합. 원장 outcome-observations:R03, OUT-R03-replacement-rfc. | [Rust Reference의 in/out/lateout 절][r03-doc]은 입력 초기값, 출력 목적지 복사, 모든 입력을 읽은 뒤에만 lateout 입력 레지스터 재사용을 설명. 원장 OUT-DOC-ASM, web-reader L333–414. 이 연구는 실행하지 않음. | 직접 제공 인용·인과적 채택 미확인. 최초 PR의 429기록·267본문 및 현재 PR 본문에서 도메인 일치 0. 현재 의미가 최초 일부 조건과 닮음은 독립 유사성을 보일 수 있으나 ‘독립 발생’을 입증하지도 않음. | 미병합 종료를 설계 거절로 세는 해석은 이미 반증됨. 다음 첫 자료는 #2873 본문이 연결한 [구현 #69171][r03-implementation]과 고정 버전의 allocator/compiletest. 2020년 전체 설계가 그대로 출시됐다는 주장은 여전히 미확인. |
| R04 — 프로젝트 그룹의 중단·보존·재개 | RFC #2856은 2020-05-21 병합. [수락 댓글 632236575][r04-accept]. [리뷰 404969272][r04-restoration]은 Restoration이 형성 단계를 생략하는 경로를 뜻하지 않는다고 설명. 원장 outcome-observations:R04. | 규칙의 채택은 확인. 실제 중단 그룹 한 곳의 저장소 보존·프라이버시 처리·연락 역할·상위 팀 합의·재개 사건은 추적하지 않음. | 직접 제공 인용·인과적 채택 미확인. 171기록·116본문 및 현재 PR 본문에서 도메인 일치 0. 통계의 보존/정정 공지가 이 governance 규칙의 기원이라는 근거는 없음. | 첫 자료는 [#2856 Restoration 토론][r04-restoration]에서 이름이 확인되는 실제 프로젝트 그룹의 중단/재개 공지와 해당 팀 회의록. 동일 그룹 ID의 중단일·read-only 저장·새 연락자/합의·재개일을 연결해야 실제 절차 적용 판정을 바꿀 수 있음. 이름이 예로 든 traits 그룹이 실제 이번 조건대로 재개됐다고 먼저 가정하지 않음. |
| R05 — mixed-protocol Service를 허용하되 제공자 능력에 맡김 | KEP #1438은 2020-07-14 병합. [리뷰 367654556][r05-gcp]은 API 필터를 제거하면 당시 GCP 구현이 첫 protocol을 모든 포트에 적용하고 오류를 알리지 않을 위험을 지적. [리뷰 445056251][r05-aws]은 UDP 지원을 넣은 AWS 구현도 mixed TCP/UDP에는 추가 작업이 필요하다고 지적. 원장 outcome-observations:R05. | [현재 Service 문서][r05-doc]의 mixed protocol 절은 API 허용과 cloud-provider 추가 제한을 함께 기술하고 1.26 이후 stable로 표시. 원장 OUT-DOC-MIXED, web-reader L1283–1291. 실제 cloud-provider 실행·패킷 시험은 하지 않음. | 직접 제공 인용·인과적 채택 미확인. 184기록·127본문 및 현재 PR 본문에서 도메인 일치 0. 수신 원문이 이미 알고 있던 API/제공자 경계를 후속에서 확인한 것임. | 첫 자료는 리뷰가 연결한 [AWS 변경 #92109와 discussion_r439730341][r05-aws-next], 이어 동일 Service의 TCP/UDP 각 포트 결과와 provider 버전이 있는 시험. API 객체 수락과 실제 프로토콜 노출이 갈릴 수 있으므로 ‘검증 완화=문제 해결’ 결론을 바꿀 수 있음. |
| R06 — 공유 설정과 인스턴스 설정을 나눔 | KEP #1439는 2021-07-09 미병합 종료. [댓글 763190786][r06-kyaml]은 KYaml 2-way merge 대안을 제안. [763476786][r06-semantics]과 [775880476][r06-spec]은 보조 라이브러리 구현에 API를 맡기기보다 병합 의미의 명세를 요구. [877198773][r06-close]은 rotten 비활성 종료. 원장 outcome-observations:R06. | 이 PR에서 API가 승인·구현됐다는 근거 없음. 논의된 대안과 lifecycle 종료를 확인했을 뿐 다른 경로의 구현 부재는 검사하지 않음. | 직접 제공 인용·인과적 채택 미확인. 165기록·123본문 및 현재 PR 본문에서 도메인 일치 0. 격리·인증 원리의 부분 유사성이 구성 필드 우선순위/보존 알고리즘을 제공하지 않음. | 첫 자료는 [763476786의 KYaml 명세 요청][r06-semantics]에 응답한 고정 알고리즘 문서·테스트. 두 Kind의 파일 혼합, 명령행 덮어쓰기, 원격 공유 갱신에서 로컬 값 보존 사례가 필요. 이를 갖춘 대체 구현이 나오면 ‘다른 경로는 미확인’에서 이동 가능. |
| R07 — AppArmor annotation에서 전용 필드로 넘어가는 버전 호환 | 최초 #1444는 2022-07-07 미병합 종료. [댓글 1178154542][r07-supersede]은 #3298이 대체한다고 말함. [#3298][r07-replacement] 본문도 supersedes #1444이나 현재 메타데이터는 2024-01-19 미병합 종료. 원장 outcome-observations:R07, OUT-R07-replacement-kep. | [현재 AppArmor 문서][r07-doc]는 appArmorProfile 필드와 1.30 이전 annotation API, 1.31 이후 stable을 설명. 원장 OUT-DOC-APP, web-reader L908–959. 최초의 7개 skew/변환/불변성 조건 전부가 그대로 배포됐다는 확인은 없음. | 직접 제공 인용·인과적 채택 미확인. 257기록·186본문 및 현재 PR 본문에서 도메인 일치 0. 기능 존재는 특정 초기 PR이나 통계 개정 원리의 채택을 증명하지 않음. | 첫 자료는 #3298이 연결한 [KEP 이슈 #24][r07-track]에서 실제 최종 병합판을 확인하고, 1.29–1.31 경계의 API/kubelet 변환·일치검사·annotation update·immutability 시험을 최초 7조건과 대조하는 것. N+4 보존 창은 따로 확인해야 함. |
| R08 — 기존 taint-based eviction을 동작 변경 없이 GA로 승격 | KEP #1450은 2020-01-20 병합. [추적 이슈 #87161][r08-tracking]은 2020-03-12 닫혔고 본문 Tasks의 KEP·시험·feature gate 정리·문서가 완료 체크되어 있음. 원장 outcome-observations:R08, OUT-R08-ga-tracking. | 유지관리자의 완료 기록과 연결된 작업을 확인. 이 연구가 클러스터를 실행해 기본 on 및 기존 동작 동일성을 검증한 것은 아님. | 직접 제공 인용·인과적 채택 미확인. 33기록·22본문 및 현재 PR 본문에서 도메인 일치 0. 단계 명칭 변경과 실제 상태 변화/수정은 다른 관계임. | 첫 자료는 #87161 Tasks가 연결한 [시험 #88152][r08-tests]와 [feature gate 정리 #87487][r08-gate]. 고정 1.18 빌드의 이전·이후 taint/tolerationSeconds 동작과 기본값 시험으로 ‘이 연구의 실행 미확인’을 줄일 수 있음. |

위 표에서 확인한 최초 PR 병합 5/8, 후속 대체 PR 중 병합 1/2 등의 수는 **후속 분류**다. 폐쇄 후보 18문서의 회수 성공률, 전이 적합 분자 또는 실제 웹 전체 검색 성능과 합산하지 않는다. 수신 팀의 직접 원리 인용 및 실제 채택은 8/8 미확인이다. ‘미확인’ 8건을 ‘채택하지 않은’ 8건으로 바꾸지 않는다.

## 3. 현장 4원문·2분야·3사건의 비교

F01·F02는 발행 기관과 작품은 다르지만 동일한 감편 과정을 다룬다. DCP가 MTA 자료를 집계했으므로 독립적으로 측정한 두 운행 실적은 아니다. F03의 여러 이전판과 F04의 두 XLSX·목록은 각각 한 작품으로 묶었다. 이 초안의 재독·해시 대조도 고유 원문 수에 추가하지 않는다. 네 현장 자료는 수신 최초 제안의 2020년 1월 이후 사건/정정이므로, 현재 전이 검토용 현장 증거와 당시 이용 가능성을 구분한다. F04의 2023-12-19는 정정일이며 최초 발행일은 원장에서 미확인이다.

| 원장 ID·사건·분야 | 사건과 원문 위치 | 실제 확인 | 예외·반대 해석 | 옮길 수 있는 관계와 남는 핵심 |
| --- | --- | --- | --- | --- |
| F01 / FIELD-TRANSIT-PLAN / 교통 사건 1 | [MTA 2020-03-24 발표][f01], Subways and buses / Long Island Rail Road and Metro-North / communication channels. 캐시 F01.txt L23–30; RF-A01. | 단계별 적용일, 운행 중단 노선을 보완하는 local service, 필요시 서비스 보충 인력·차량, 웹·앱·역 표시를 공표. | 발표는 시행 의사·운영자의 설명이다. 모든 이후 출발, 충분한 빈도, essential-worker의 이동 성과는 확인하지 않음. | 변화 권한을 가진 주체가 새 상태·전환일·대체 경로·고지 채널을 연결한다는 절차는 검토 가능. 동일한 공지를 만들면 실제 실행 권한이나 여분 자원이 생긴다는 가정은 버려야 함. |
| F02 / FIELD-TRANSIT-EXCEPTION / 교통 사건 1 | [NYC DCP 2020-04-21 PDF][f02], 인쇄 p13 / PDF page index 12, Subway System Service Changes. 그래프의 2/13·3/12·4/16 및 우측 설명·하단 출처; RF-A02. | 해시가 고정된 PDF는 **MTA Real Time data**를 출처로 명시. DCP는 시간대별 정차 집계에서 첨두 서비스 감소와 주간 첨두/비첨두 구분 약화를 보고. | 이전 GTFS/정적 예정 운행 해석은 철회. 반대로 real-time이라는 말만으로 원시 feed·집계 코드·실제 운행 전수가 재검증됐다고 할 수도 없음. F01과 날짜·척도가 달라 즉시 약속 위반으로 계산하지 않음. | 공표 계획과 이후 집계를 다른 증거 층으로 연결할 수 있음. 옮길 핵심은 운영 관측의 별도 수집·판독. 데이터가 예측인지 실현인지, 누락/취소를 어떻게 센 것인지는 다음 확인이 필요. |
| F03 / FIELD-STATS-HISTORY / 통계 사건 2 | [ONS 이전판 v1][f03-v1] §5 첫 문단, F03-v1.txt L152; [v2][f03-v2] L156; [정정된 현재 캡처][f03-current] §5 L159 및 정정 배너 L75–82; RF-A03. | v1·v2의 ‘여성 90세 이상도 낮은 추정’이라는 설명이 이후 본문에서 제거됐음을 대조. 2023-02-28의 그림 4·5 지역 라벨 순서 정정과 2023-03-01 문장 정정은 다른 공지로 연결됨. | 이전판을 보존하고 차이를 설명한 사실은 소비자가 업데이트를 보거나 사본을 자동 취소했다는 증거가 아님. 그림 데이터 전체의 독립 재계산은 하지 않음. | 이전/이후 주장, 수정 위치, 이유, 시점을 연결하는 구조는 재사용 가능. 발행자의 수정 권한을 downstream 소비자의 변경/회수 권한으로 대체하면 깨짐. |
| F04 / FIELD-STATS-BOUNDARY / 통계 사건 3 | [ONS 공식 전후판 목록][f04-index] Reason for update, 캐시 L98–101; v1·v2 XLSX의 MYE3!A9:O365와 v2 Correction notice!A1:A3. [v1][f04-v1] / [v2][f04-v2]; RF-A04. | 기존 감사는 지역코드 357개로 조인해 39행·78셀의 H/I 변경, J/O 불변을 재현. 이번 초안도 A/B/H/I/J/O 9–12행 및 정정 공지를 두 워크북의 저장값에서 직접 대조. | 변하지 않은 최종 순이동/인구가 중간 구성값의 정확성을 보장하지 않음. 전 워크북 또는 추정 모형 재현이 아님. 357개 전수 수치 재검산은 기존 RF-A04에 의존하며 이번 표본 셀 재독과 구별. | 같은 경계 내부 이동을 총 유입·유출에서 제외해야 한다는 역할/범위 조건을 검사할 수 있음. 표면적으로 최종 출력이 같다는 이유로 입력·경계·중간 상태를 생략하면 대응을 잘못 판정함. |

### F02 정정의 근거와 영향

[현장 정정 원장](../field/resume-field-correction.json)은 F01·F02 설명 수정 전 행과 파일 해시를 보존한다. 고정 PDF SHA256은 b3e6689d94b496817a35f072d175b5b4be9149429a87d8adcaf7c8ff5e904bcc다. 기존 캐시의 텍스트·로컬 렌더·동일 바이트 직접 재다운로드는 MTA Real Time 표기로 일치했고, 웹 screenshot은 해시를 제공하지 않은 GTFS 표기를 반환했다. 이 초안은 [재개 감사의 확인 경로별 표](../field/resume-field-audit.md)를 인용하며, 네트워크를 다시 요청하지 않았다.

이 정정은 ‘정적 시간표만 보았다’는 낮은 증거 분류를 바로잡는다. 그래도 DCP의 사후 집계 보고를 원시 실제 출발 로그와 동일시하지 않는다. 고정 검색 순위·적합 분자·원문 수·사건 수는 수정하지 않는다. 다음 자료는 2020-02-13·03-12·04-16 보존 feed, 당시 DCP 집계 코드, 예측과 실현 운행을 가른 규칙이다. 현재 API 페이지를 열어도 그 과거 판·분모가 복원되는 것은 아니다.

### F04에서 최종 출력만 비교할 때 놓치는 것

| 원문 좌표·지역 | v1 유입 / 유출 | v2 유입 / 유출 | 전후 순이동 J열 | 전후 인구 O열 |
| --- | --- | --- | --- | --- |
| MYE3!H9:O9, England and Wales | 3,768,798 / 3,778,598 | 47,924 / 57,724 | −9,800 | 60,238,038 |
| MYE3!H10:O10, England | 3,628,364 / 3,648,816 | 112,337 / 132,789 | −20,452 | 57,106,398 |
| MYE3!H11:O11, North East | 133,150 / 123,406 | 66,260 / 56,516 | 9,744 | 2,683,040 |
| MYE3!H12:O12, County Durham | 29,011 / 23,640 | 29,011 / 23,640 | 5,371 | 528,127 |

출처는 [v1 XLSX][f04-v1]와 [v2 XLSX][f04-v2]의 표시 좌표다. 워크북 정정 공지는 큰 지역 안의 이동을 총 유입·유출에서 제거해야 했으며 순이동과 인구 총계에는 영향이 없었다고 설명한다. 수치 대조는 이 설명을 MYE3 저장값 범위에서 뒷받침한다. 따라서 “같은 출력이면 같은 원리”라는 판정 규칙의 반례는 유지된다. 반례의 범위를 표의 모든 통계 추정이 틀렸다는 주장으로 넓힐 수는 없다.

## 4. 실제 자료가 막는 과대해석

| 반례 ID | 성급한 결론 | 맞지 않는 관측·정확 근거 | 이 분석이 유지하는 판정 |
| --- | --- | --- | --- |
| FF-C01 | 승인·병합됐으므로 최초 요구의 모든 조건이 구현됐다. | R01 [#68404 본문 두 번째 문단][r01-impl]이 deprecation을 명시적으로 미룸. | 승인, forwarding 구현, 경고 완료는 별도 단계. 경고 완료는 미확인. |
| FF-C02 | 최초 PR이 닫혔으므로 설계가 거절됐다. | R03 [593702000][r03-continue]과 #2873 병합, R07 [1178154542][r07-supersede]와 #3298의 대체 연결. | 종료 원인을 확인하고 대체 경로를 따로 기록. R07의 현 기능 존재로 #3298 병합을 꾸며내지 않음. |
| FF-C03 | API가 입력을 허용하면 제공자가 의미대로 실행한다. | R05 [367654556][r05-gcp]은 잘못된 protocol 적용과 오류 미고지 가능성을, [445056251][r05-aws]은 UDP 지원과 mixed 지원의 차이를 지적. | 수락 단계와 실행 책임을 분리. 실제 provider 시험 미확인. |
| FF-C04 | 원리 이름이나 구현 라이브러리를 찾으면 필요한 명세도 얻는다. | R06 [763476786][r06-semantics], [775880476][r06-spec]은 병합 의미 명세를 요구. | 모듈·원리 이름은 부분 단서일 수 있음. 우선순위와 불변조건의 핵심 설계가 남으면 완결로 올리지 않음. |
| FF-C05 | real-time 표기이므로 모든 실제 운행을 검증했다. | F02 [p13][f02]은 집계 보고이고 raw feed·집계 코드·실현 판별을 이 연구가 재실행하지 않음; RF-A02. | GTFS 오분류는 철회하되 사후 집계와 원시 운행 재현의 차이는 유지. |
| FF-C06 | 기록을 보존하고 공지했으므로 모든 소비자 상태가 복구됐다. | F03 [정정 배너/이전판][f03-current]은 발행자 쪽 변경·이력을 보여 줄 뿐 소비자의 상태 이력을 제공하지 않음. | 추적 가능성과 실제 전달/적용/회수 성공을 분리. 부재를 실패로 단정하지 않고 미확인. |
| FF-C07 | 최종 숫자가 같으므로 입력 경계와 과정도 맞는다. | F04 [v1][f04-v1] / [v2][f04-v2], MYE3 H/I 변경과 J/O 불변. | 출력 외에 입력·범위·상태·주체를 검토할 필요가 있다는 실제 반례. |
| FF-C08 | 공개 도메인 검색 0건이므로 수신 팀은 원리를 몰랐다. | [followup-citation-screen.json](../evidence/followup-citation-screen.json)의 literal substring과 제외 범위. | 직접 제공 인용은 확인되지 않음. 사적 지식·간접 영향·독립 발생·실제 채택은 미확인. |

이 반례들은 서로 다른 경계를 공격한다. R01은 구현의 시간 단계, R05는 행위 주체의 능력, F03은 수정 권한과 downstream 반영, F04는 입력 경계와 출력 동일성이다. 따라서 한 가지 성공 요건으로 합쳐 성공률을 만들지 않는다. 같은 원리 후보라도 필요한 경계 조건이 달라지면 판정이 달라져야 한다는 검토 기준으로 쓴다.

## 5. 세 입장에서 검토할 한 줄과 다음 행동

| 입장·사례 | 짧게 반환할 설명 | 바로 확인할 원문 | 옮겨야 할 한 단계 | 옮기면 깨지는 한 조건 |
| --- | --- | --- | --- | --- |
| 수신 설계자 / R01 보류 | 기존 호출을 연결하는 단계와 사용자 경고를 켜는 단계를 각각 추적하라. | [#68404 본문 두 번째 문단][r01-impl], OUT-R01-rename-implementation | 변경을 적용받아야 하는 하위 의존자 목록과 경고 활성화 조건을 따로 기록. | forwarding 병합을 경고 완료로 읽으면 최초 필수 조건 하나를 빠뜨림. |
| 절차 운영자 / F01–F02 적용과 예외 | 새 상태의 공표 뒤에는 같은 대상을 실제로 관측하는 자료가 따로 필요하다. | [F01 Subways and buses][f01], [F02 p13][f02] | 공표일·운행일·집계일·관측 단위와 결측 규칙을 묶어 비교. | 발표와 사후 집계의 날짜/척도가 다르거나 실시간 예측을 실제 운행으로 세면 허위 성공·실패가 생김. |
| 반례 검토자 / F04 충돌 | 최종 합계가 같아도 경계가 다른 구성값은 틀릴 수 있다. | [F04 v1][f04-v1]·[v2][f04-v2] MYE3!H9:O12 및 Correction notice!A1:A3 | 지역키로 두 판을 조인하고 총유입/유출·순이동·인구를 각각 비교. | 순이동만 남기거나 ‘정정’이라는 단어만 보존하면 핵심 반례가 사라짐. |

이 표의 짧은 문장은 **후속·현장 판독 뒤 작성한 제안 표현**이다. 최초 S/R 질의·최초 반환 설명으로 제시하지 않는다. 원리를 단순한 공통 단어로 줄이거나 발행자와 소비자 역할을 뒤집으면 F03의 수정 권한과 R05의 제공자 실행 능력이 보이지 않는다. F04의 H/I 전후 셀 근거를 제거하면 경계 오류라는 결론을 확정할 수 없어야 한다. 이 근거 제거 검사는 최초 검색의 재평가가 아니라 검토 설명이 무엇에 의존하는지를 드러내는 사후 분석이다.

## 6. 통합에 넘기는 제한과 다음 판별

직접 원리 인용을 확정하려면 수신 팀이 어떤 제공 자료를 언제 알고 어떤 조건 때문에 결정을 바꿨는지를 연결하는 공개 설계 기록 또는 참여자 확인이 필요하다. 단순 후속 유사성은 이 연결을 제공하지 않는다. 또 현재 문서가 최초 부분 조건과 맞더라도 이전 판의 가용성·구현 시점·실제 사용자의 채택은 따로 확인해야 한다. 이 초안은 그런 자료를 새로 찾지 않았으며, 검색 순위와 144대응의 분자를 고치는 입력으로 사용하지 않는다.

| 가장 중요한 불일치 또는 약점 | 근거 자료 주소 | 영향을 받는 결론 | 다음 조사 제안과 첫 자료 |
| --- | --- | --- | --- |
| 공개 문자열 0건과 부분 후속 유사성으로는 직접 제공 원리 인용·인과적 채택을 판정하지 못함. | [도메인 검사 영수증](../evidence/followup-citation-screen.json); [R05 당시 제공자 리뷰][r05-gcp]; [R03 대체 RFC][r03-replacement] | 실제 사용자 채택·사전 미인지·독립 발생은 8건 모두 미확인. 폐쇄 집합 회수와 별도 결론. | 첫 자료는 해당 리뷰/대체 RFC 작성자가 참조한 설계 자료 목록·의사결정 기록. 제공 문서 ID와 결정 전 날짜를 연결한 명시적 인용이 나오면 직접 영향 판정을 바꾸되 원 검색 적중은 유지. |
| R01 단계 구현과 R07 대체 경로 때문에 승인/현재 문서만으로 최초 모든 조건 완료를 확정할 수 없음. | [R01 구현 #68404][r01-impl]; [R07 #3298][r07-replacement]; [현재 AppArmor 문서][r07-doc] | R01의 경고 완료, R07의 최초 7조건·N+4 창 구현 여부. | R01은 [#70173][r01-track]의 deprecation 변경·진단 시험을 먼저 읽고, R07은 [#24][r07-track]의 최종 병합판과 1.29–1.31 변환/불변성 시험을 최초 조건별로 대조. |
| F02의 원시 실시간 자료와 F04의 전 추정 과정은 이 연구가 재현하지 않음. | [F02 p13][f02]; [F04 v1][f04-v1] / [v2][f04-v2]; [현장 감사](../field/resume-field-audit.md) | 실제 모든 운행·약속 위반 또는 전체 통계 모형 검증이라는 확대 주장을 막음. 현장4원문/2분야/3사건 및 MYE3 반례는 유지. | F02는 2020-02-13·03-12·04-16 보존 feed와 당시 DCP 집계/실현판별 코드를 먼저 대조. F04는 v2 Correction notice가 가리킨 MYE3의 지역 포함관계·집계식과 원자료를 확인해 저장값 비교를 넘어 오류 원인 재현 여부를 판별. |

[seal]: https://github.com/laadkke-arch/agentflow-open/commit/a2ce15d10415c556574d1a65af77718a81052d01
[r01-accept]: https://github.com/rust-lang/rfcs/pull/2843#issuecomment-601564223
[r01-impl]: https://github.com/rust-lang/rust/pull/68404
[r01-track]: https://github.com/rust-lang/rust/issues/70173
[r02-pr]: https://github.com/rust-lang/rfcs/pull/2845
[r02-choice]: https://github.com/rust-lang/rfcs/pull/2845#issuecomment-720705642
[r02-boundary]: https://github.com/rust-lang/rfcs/pull/2845#issuecomment-910114408
[r03-continue]: https://github.com/rust-lang/rfcs/pull/2850#issuecomment-593702000
[r03-replacement]: https://github.com/rust-lang/rfcs/pull/2873
[r03-implementation]: https://github.com/rust-lang/rust/pull/69171
[r03-doc]: https://doc.rust-lang.org/reference/inline-assembly.html#asm.operand-type.supported-operands-lateout
[r04-accept]: https://github.com/rust-lang/rfcs/pull/2856#issuecomment-632236575
[r04-restoration]: https://github.com/rust-lang/rfcs/pull/2856#discussion_r404969272
[r05-gcp]: https://github.com/kubernetes/enhancements/pull/1438#discussion_r367654556
[r05-aws]: https://github.com/kubernetes/enhancements/pull/1438#discussion_r445056251
[r05-aws-next]: https://github.com/kubernetes/kubernetes/pull/92109#discussion_r439730341
[r05-doc]: https://kubernetes.io/docs/concepts/services-networking/service/#load-balancers-with-mixed-protocol-types
[r06-kyaml]: https://github.com/kubernetes/enhancements/pull/1439#issuecomment-763190786
[r06-semantics]: https://github.com/kubernetes/enhancements/pull/1439#issuecomment-763476786
[r06-spec]: https://github.com/kubernetes/enhancements/pull/1439#issuecomment-775880476
[r06-close]: https://github.com/kubernetes/enhancements/pull/1439#issuecomment-877198773
[r07-supersede]: https://github.com/kubernetes/enhancements/pull/1444#issuecomment-1178154542
[r07-replacement]: https://github.com/kubernetes/enhancements/pull/3298
[r07-track]: https://github.com/kubernetes/enhancements/issues/24
[r07-doc]: https://kubernetes.io/docs/tutorials/security/apparmor/#securing-a-pod
[r08-tracking]: https://github.com/kubernetes/kubernetes/issues/87161
[r08-tests]: https://github.com/kubernetes/kubernetes/pull/88152
[r08-gate]: https://github.com/kubernetes/kubernetes/pull/87487
[f01]: https://apps.cio.ny.gov/apps/mediaContact/public/view.cfm?parm=926C019C-DE79-DD17-D6493016DF74143F_5D9C1A27-C9C7-90C0-217C93A974EEA6D8
[f02]: https://www.nyc.gov/assets/planning/download/pdf/planning-level/transportation/covid19-transportation/20200421.pdf#page=13
[f03-v1]: https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/articles/reconciliationofmidyearpopulationestimateswithcensus2021englandandwales/2023-02-28/previous/v1
[f03-v2]: https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/articles/reconciliationofmidyearpopulationestimateswithcensus2021englandandwales/2023-02-28/previous/v2
[f03-current]: https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/articles/reconciliationofmidyearpopulationestimateswithcensus2021englandandwales/2023-02-28/previous/
[f04-index]: https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/estimatesofthepopulationforenglandandwales/mid20222023localauthorityboundaires
[f04-v1]: https://www.ons.gov.uk/file?uri=%2Fpeoplepopulationandcommunity%2Fpopulationandmigration%2Fpopulationestimates%2Fdatasets%2Festimatesofthepopulationforenglandandwales%2Fmid20222023localauthorityboundaires%2Fprevious%2Fv1%2Fmye22tablesew2023geogs.xlsx
[f04-v2]: https://www.ons.gov.uk/file?uri=%2Fpeoplepopulationandcommunity%2Fpopulationandmigration%2Fpopulationestimates%2Fdatasets%2Festimatesofthepopulationforenglandandwales%2Fmid20222023localauthorityboundaires%2Fprevious%2Fv2%2Fmye22tablesew2023geogsv2.xlsx
