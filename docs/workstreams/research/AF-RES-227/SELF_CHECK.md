# AF-RES-227 자체점검

핵심 상태 **REVIEW_READY**. 기본 64자리와 C1/C2 내부 관측의 예정·관측·결측 조건을 만족했다. 자료 유형 하한을 모두 만족했다. 이 작업자가 별도 checkout에서 다시 실행하고 소스·원로그를 대조했다. 독립 평가자 검토는 미실시다.

| 질문 | 근거 ID와 정확한 위치 | 반증 확인 및 판단 경계 |
| --- | --- | --- |
| Q1 | O05–O06 열람, P01–P06 의존, G01/G06 비교 규칙, B01/B02/B04/B06 버전과 backend, [session](session.json), [inputs](inputs.json), [환경](environment.json) | 원표 배열과 지문 대조. R4 원래 vs LF를 실제 각각 관측. R1에는 trailing change가 없고 W1 on/off에서 차이와 exit 0을 분리했다. |
| Q2 | G08/G09/G10, G11/G12, B03, E03. [fixture F01–F11](fixtures.csv) · [공개 assertion](receipts/public-crosschecks.json) | t4033/t4050이 공유하는 full hunk를 독립 fixture로 두 번 더하지 않았다. R1 grep과 R4 pairs 단언을 full hunk로 채점하지 않았다. |
| Q3 | G01, B01/B02, [기본](receipts/base.jsonl) · [재생](receipts/replay-summary.json) | 독립 경로 aggregate 로그를 바이트/exit/blocks 대조. 정상 Git 1을 오류나 동일로 분류하지 않았다. R2의 동일 헤더·개수와 다른 본문을 확인했다. |
| Q4 | G02/G03/G04/G07, B01. [C1–C2 raw trace](receipts/diagnostic-base.jsonl#L17-L24) · [앵커](anchors.csv) | C1 Git root common=1과 R3 common=0을 대조. C2 두 순서와 실제 rank, 증인을 관측했다. 후처리 전·후를 같은 값으로 가정하지 않았다. |
| Q5 | G04/G05/G11/G12, B02/B03, E02/E03. [통제](receipts/controls.jsonl) · [컴팩션 차이](receipts/diagnostic-comparison.json) | C4 동일 앵커, 두 context. 48개의 indent 단독 차이 0을 upstream indent 차이 범위와 대조. R4의 pre/post 이동 및 C3 역방향 환산을 확인했다. 일부 도구의 초깃값과 Empty range는 의미/바이트 구분이 필요하다. |
| Q6 | P01/P02/P04/P05, G08/G10/B03. [32행 대조](predictions-comparison.csv) | 단계 노출과 측정 단위를 각 행에 유지. C1/C2 핵심 역전 0. R4 suffix의 추정 메커니즘을 정정. C3 histogram 최종 방향효과 0이고 선행 문장은 가능성만 적었다. |
| Q7 | A01–A04, E01–E04. [Math/DP 실행](receipts/lis.json) · [raw C1 경쟁 matcher](receipts/challenges.jsonl#L8) | 길이만 같고 서로 다른 증인과 잘못 읽은 tops를 재현했다. 반복값 strict/비감소 차이 검산. A02와 E01은 RSK 공통 계보이며 별도 역사적 채택 근거로 셀 수 없다. |

## 예정·관측·결측과 독립성

| 단위 | 예정 | 유효 관측 또는 산입 | 결측·미산입 | 재생 |
| --- | --- | --- | --- | --- |
| 직접 원문 | 최소 22 | 29. 210 4/4, Git 11/7, Breezy 6/5, 원리 4/3, 표시 4/3 | 하한 결측 0. 원장 55행 중 미산입 26 | 각 고정 원본·위치 [원장](sources.jsonl) |
| 독립 출전 계보 | 별도 계수 | 산입 29건의 15 lineage | 동일 저작 두 번째 주소, 공유 helper 및 소스/배포의 연관성 기록 | 통계적 독립성과 별개 |
| 기본 입력 사건 | 고유 8쌍 | 8 (공개 유래 4, 합성 4) | 0 | 동일 8쌍. 추가 통제에서 별도 고유 5쌍 |
| 기본 method×pair×repeat | 64 | 64. Git 48 exit 1, Breezy 16 exit 0 | 0 오류, 0 결측 | 64/64 일치 |
| 표시 완전교차 | 112 | Git 96, Breezy 16 | 0 결측. Breezy indent 적용 범위 밖 | 112/112 일치 |
| 추가 통제 | 22 | 22 | 0 | 22/22 일치 |
| C1/C2 기본 내부 분기 | 8 셀 | 8. 두 입력×네 방법 | 0. Myers는 unique LIS 필터 적용 범위 밖 | 나머지 기본과 함께 재생 |
| 전체 진단 | 32 기본+112 표시 | 144. 순정 stdout/exit/해당 blocks 일치 144 | 0 | 144/144 원 trace 포함 일치 |
| 공개 전체 suite | 5 | 5 exit 0. Git 91/91, Breezy 실행 14 pass | C 관련 12 skip. 기본 Python 대상 밖 | 5/5. unittest 시간만 비교 제외 |
| 직접 고정 공개 단언 | 반복당 8, 총 16 | 16 일치 | R1 full hunk, R4 full hunk는 원래 범위 밖 | 순정 64를 재검산 |
| 원리·증인 별도 실행 | 1 | 1. 예 7, upstream DP doctest 6 | Sage 자체 실행과 Fredman 본문은 미확인 | 1/1 |
| 사용자·독립 평가자/환경 | 범위 밖 | 실행자 자체점검 및 별도 checkout·재빌드 | 독립 평가자, 사람 연구, 다른 OS의 자체 실행 미실시 | 별도 checkout은 동일 Cloud 호스트 |

G10은 t4033/t4050 공유 fixture를 한 번 산입한다. G08은 R1 별도 grep이라는 본문 원자료 때문에 산입했다. B07은 C 비교용 직접 읽기이며 Python 계보·범위 밖이라 미산입했다. E02와 E03은 서로 다른 소스/시험 문서이고 CPython 계보 하나로 센다. 한편 PyPI는 B05 README 재게시분을 제외한 배포 메타데이터 B06을 사용했다. Schensted 출판사 초록은 A02 원면과 중복, Sage 이동판 문서는 E01의 동일 예라 미산입했다. Fredman은 원문 경로 timeout/403, GNU 매뉴얼은 timeout, 고정 CPython HTML 경로는 열기 실패로 기록했다. 이를 각 유형의 성공 건수에 넣지 않았다. [출처 필드와 실패 경로](sources.jsonl)

별도 GitHub checkout에서 실행한 작업본은 `8377dbb…`이다. 두 독립 브라우저나 평가자의 관측으로 승격할 수 없다. 기본 반복 전에 고정한 입력과 순정 기록 이후에만 내부를 계측한 순서를 커밋 이력으로 확인한다. 원격 결과판의 공통 검사와 허용 경로 확인은 마지막 인계에서 판 SHA와 연결한다.
