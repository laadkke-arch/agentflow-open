# R1/R2 독립 검토

검토자: AF-RES-086 incidents 연구자. 최초 검토 시각: 2026-11-23T15:07Z. 최종 카드 및 수정 재열람: 2026-11-23T15:10Z. 검토 중에는 incidents 산출물과 R 산출물을 수정하지 않았고 이 파일만 작성했다. 공개 HTTP를 재요청하지 않고 R 연구자가 확보한 원 응답, 영수증, 짧은 추출 및 원장을 독립적으로 읽고 로컬 해시를 다시 계산했다.

## 판정과 최소 수정

**검토한 R 원장의 핵심 사실·분모에 차단 오류 없음.** `inactive`를 과거 `success`로 바꾸지 않고, 현재 파일 일치와 과거 독자 응답을 분리한 판정은 확보 원문과 맞는다. 역사적 게시 성공·독자 판 확인의 누락을 해소하지는 못하므로 이 검토는 전체 연구의 REVIEW_READY를 뜻하지 않는다.

1. 재게시 원장의 `earlier deleted success statuses` 문구가 이전 success의 존재와 삭제를 전제할 수 있음을 지적했다. 재검토한 `routes.jsonl`에는 이 문구가 0회이며 수정 완료를 확인했다.
2. `R-SERVICE-STATUS.version`의 모호한 과거 기록 라벨을 지적한 뒤 `current service documentation @2026-11-23`으로 수정된 것을 확인했다. 같은 행의 본문과 한계는 2025년 개별 삭제·자동 inactive를 증명하지 못한다고 정확히 적었다.
3. 최종 `cards.md`와 `postrecommendations.json`을 읽었다. 생성 커밋의 GitHub blob/raw 링크를 보존 HTML 원문·다운로드로 설명하며 렌더링된 옛 사이트와 구분했다. 원 raw 영수증의 Content-Type은 `text/plain; charset=utf-8`, `X-Content-Type-Options: nosniff`이고 CSP도 sandbox이므로 이 설명은 관측과 맞는다. 카드의 파일·판·목적 절·보류 조건도 확인했다.
4. 최종 사후 권고의 `inactive 후 NEXT/LAST` 문구는 NEXT 생성 시각에 맞지 않아 지적했다. R 작성자가 `inactive 직전 NEXT 생성(12:37:22Z)와 이후 LAST 생성(16:07:18Z)`으로 수정했음을 사후 권고와 NOTES에서 재열람했다. 선택 inactive는 12:38:03Z다. 두 생성 스냅샷 전체를 inactive 이후로 묶는 오류가 해소되었다. 마지막으로 추가된 CURRENT 주장 정의 3행도 현재 관측·일반 도움말의 한계를 유지함을 확인했다.

**미해결 수정 요청: 없음.** 검토 범위의 보류는 역사 원자료가 없다는 연구 결과이며, 로컬 문구 수정으로 없어질 공석이 아니다.

## 원문에 대조한 결론

| 검토 항목 | 직접 다시 읽은 입력 | 확인한 값과 허용 결론 | 금지할 확장·판단을 바꿀 다음 관측 |
|---|---|---|---|
| R1 배포 객체와 상태 | `R1-DEPLOYMENT`, `R1-DEPLOYMENT-STATUSES.original.json` 및 raw | deployment `2328795124`는 생성 커밋 `45e0d9ebc168cf3632bc2d737c9db2318668a826`을 가리킨다. 남은 상태는 `6150834411`, `inactive`, `2025-03-24T12:38:03Z` 한 행. environment_url은 빈 문자열이고 log_url은 run `14035386117` / job `39292155301`이다. | 과거 성공 1회, 실패, 마지막 정상 제공 시각 중 어느 것도 inactive 한 행에서 산출할 수 없다. 상태 원문 또는 발행자의 같은 run 성공 로그와 당시 독자 응답이 다음 입력이다. |
| R2 배포 객체와 상태 | `R2-DEPLOYMENTS-OUTPUT`, `R2-DEPLOYMENT-STATUSES.original.json` 및 raw | deployment `1283145596`는 생성 커밋 `92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1`을 가리킨다. 남은 상태는 `3093912083`, `inactive`, `2024-01-21T20:58:36Z` 한 행. environment_url은 빈 문자열이며 run `7603761786` / job `20705898489`가 log_url에 남았다. | inactive를 success로 재분류하지 않는다. 현재 root·leaf의 일치도 2024년 성공 상태를 복원하지 않는다. |
| 현재 90일 보존 설명 | `R-SERVICE-STATUS` 원 HTML·텍스트 및 현재 공식 deployments/statuses 문서 | 2026-11-23에 읽은 공식 문서는 이전 상태 90일 보존, 현재 상태 유지, auto_inactive의 조건을 설명한다. 다른 상태가 현재 없을 수 있는 일반적 설명이다. | 2025년의 정책 시작일, 이 두 배포의 특정 success 존재·삭제, 이 inactive가 자동 생성됐다는 사실은 증명하지 않는다. inactive 상태를 직접 기록하는 API도 있으므로 자동 전환 하나로 단정하지 않는다. |
| R1 릴리스 이슈 113 | `R1-RELEASE-ISSUE` 본문·created/updated 시각 | 2025-03-20 생성, 2025-03-24T12:33:05Z 업데이트된 발행자의 체크리스트가 URL 검사·CRAN 릴리스·개발판 전환을 체크했다. 발행자가 완료 표시를 했다는 정적 기록이다. | 실행된 `urlchecker::url_check()` 로그, URL별 HTTP 응답, 특정 HTML 판, Pages run 성공을 대신하지 않는다. 완료 체크만으로 Q3 빈칸을 채우지 않는다. |
| R1 이후 생성물의 root 보존 | `R1-NEXT-COMMIT`, `R1-LAST-COMMIT`, 각 ROOT/LEAF raw | NEXT `64824c63fde2815880537223d9820b0d4a987dad` (12:37:22Z)는 변경 14개가 모두 `dev/` 아래다. LAST `3f2c1d51e828a63cde37621492caa44165f33daa` (16:07:18Z)는 변경 2개가 모두 `dev/` 아래다. 두 스냅샷의 root와 `reference/archive_read.html`은 최초 1.1.12 생성 파일과 각각 바이트 일치하여 4/4다. | 모든 중간 트리·전체 자산·게시 성공·연속적인 root 제공을 증명하지 않는다. “개발판 생성 커밋이 생겨 root도 즉시 개발판으로 바뀌었다”는 단순 추정은 이 두 파일에서 반박된다. 실제 공개 응답이 다음 구분점이다. |
| R1 재게시 시점 | `R1-republish-timeline.json`, 11개 배포·상태 원문 | 주 관측창의 배포 객체 11개. retained status 중 10개 시각이 주 창 안, 마지막 하나는 2025-10-21로 주 창·보조 창 밖이다. | 11회 성공 또는 실패 뒤 성공 1회로 세지 않는다. 외부 시점 inactive는 3월의 최종 응답 판이나 게시 구간 끝을 정하지 못한다. |
| R1 현재 vs 생성 파일 | `R1-GENERATED-ROOT/LEAF`, `R1-CURRENT-ROOT/LEAF` raw | 생성 root 21,930 bytes와 leaf 14,289 bytes는 1.1.12. 현재 2026-11-23 응답은 각각 21,708 / 14,062 bytes, 1.1.14이며 둘 다 바이트 불일치다. | 현재 root를 1.1.12 고정판으로 반환하지 않는다. 현재 불일치만으로 2025년 제공 실패를 판정하지도 않는다. |
| R2 현재 vs 생성 파일 | `R2-GENERATED-ROOT/LEAF`, `R2-CURRENT-ROOT/LEAF` raw | 2026-11-23의 root 18,909 bytes와 demo leaf 15,974 bytes가 지정 생성 커밋의 두 파일과 각각 바이트 일치한다. 2/2, 두 HTML 범위의 강한 동일성이다. | 같은 판이 당시에도 제공됐음, 전체 사이트·자산·대화형 데모가 동일함, 앞으로 주소가 고정됨을 뜻하지 않는다. 현재 편의 링크를 유지하는 근거가 되지만 역사적 보증은 유보한다. |
| R1 보조 보관 응답 | `R1-ARCHIVED-FEB27` 원 응답·gzip/decoded 해시 | 2025-02-27T04:30:36Z의 root 보관판은 1.1.11이며 허용한 ±30일 보조 창 안이다. | v1.1.12 주 관측창의 응답으로 옮겨 세지 않는다. 다운로드 gzip 해시와 디코딩된 HTML 해시는 서로 다른 바이트 객체다. R2 창 밖 가까운 캡처도 주 창으로 들이지 않는다. |
| 소유자 약속 | 양쪽 고정 DESCRIPTION, README, NEWS 및 `claims.csv` | R1 DESCRIPTION L18은 root, R2 L19는 root 안내. 독립된 구판 유지·동시 제공 기간 약속은 확인하지 못했다. C1 2개, C2 미확인 2개, A1 연구 질문 2개가 분리돼 있다. | 연구자가 요구한 고정판 보존 조건을 소유자의 약속으로 추가해 분모를 키우지 않는다. R 소표본 dual-owner 0/2, 공동 확인 0/0은 산출 불가다. 원 082의 6개 모집단은 별개다. |

## 직접 재계산한 파일 식별값

발행자 Git blob SHA-1은 `SHA1("blob " + byte_length + NUL + bytes)`로 재계산했다. 다운로드 SHA-256과 알고리즘·대상이 다르므로 같은 열로 합치지 않았다.

| 파일 | 직접 SHA-256 | 직접 재계산 Git blob SHA-1 | 발행자 commit 파일 SHA와 일치 |
|---|---|---|---|
| R1 지정 생성 root | `409a0d3bc2e664494b288d359d31ead7b0bacdbccf3aed9836397a422bdcbece` | `0be250ebe7b27b29771760d6f042448e162ae96c` | 예 |
| R1 지정 생성 archive_read | `0c0efbe4b86a97aa6d5662af71fa2dd8bf04a91e6caf6793c08c5ccd407722b3` | `8646eb01f28b62e0ec4153184d92a46583e98ae0` | 예 |
| R2 지정 생성 root | `cd5bab13fd944d99cae00a71e1877d1c140c527cfbea5a9a2d258d0525c2d6f0` | `77dec6a7cdb241b249895cf8950bec28838c0e84` | 예 |
| R2 지정 생성 demo | `c812426f5a97f8361e64a7a3beb8a35d5dde4bd2270b70dc1f1567080471ca0c` | `269393798d0a0160e579047662f81b32b8455737` | 예 |

R1 생성 커밋 메시지의 `a4c6ec3`은 발행자가 남긴 단축 식별자다. 고정 요구의 40자리 source SHA와 구분한 현재 route 모델이 정확하다. R2 메시지는 전체 source SHA를 직접 남겼다. 두 사례 모두 생성 커밋의 존재와 그 메시지만으로 실제 사이트 응답을 동일시하지 않는다.

## 원장·분모 검산

2026-11-23T15:04:55Z 생성된 `summary.json`을 기준으로 다시 셌고, 15:08:32Z 갱신본에서 수치가 유지됨을 확인했다.

| 지표 | 재계산 | 해석 |
|---|---:|---|
| sources 행 / 고유 ID / receipts | 73 / 73 / 73 | 모든 행의 receipt 경로를 열었다. |
| source→receipt SHA-256 일치 | 73/73 | 메타데이터 내부 일치. |
| 로컬 원 body→receipt SHA-256 일치 | 73/73 | `.workbench`의 원 body를 읽어 독립 재계산. |
| 다운로드 body 바이트 합 | 1,619,294 | wire 비용이나 검색 응답 바이트가 아니라 기록된 body 합. |
| 최소 자료량 적격 행 | 46 | 접근 실패·빈 결과·중복 관측 4개를 제외한 현재 적격 플래그 합. 46개의 독립 사건이라는 뜻은 아니다. |
| 보수적 독립 계보 | 3 | archive 1.1.12, asciicast 2.3.1, GitHub Pages 공식 계약. 한 계보의 배포·상태·파일 여러 행을 중복 계보로 세지 않는다. |
| 발행자 생성 연결 | 2/2 | 단축 SHA/full SHA 차이를 명시한 수준. |
| 선택한 배포의 success 직접 관측 | 0/2 | retained inactive 2/2와 분리. |
| 주 창에서 식별한 실제 독자 HTML 경로 | 0/4 | root+leaf 각 2개; 생성 파일은 응답 분자에 넣지 않는다. |
| 현재 응답에서 지정판 식별 / 지정 생성 HTML과 바이트 일치 | 2/4 / 2/4 | R2 두 경로. |
| R1 NEXT/LAST의 두 HTML 보존 | 4/4 | 선택한 두 추가 생성 스냅샷만의 비교. |
| R 소표본 두 원 독자 조건을 약속한 프로젝트 | 0/2 | 소유자 약속 분모. |
| R 소표본 두 조건 공동 확인 | 0/0 산출 불가 | 0%로 적으면 안 된다. 전체 P3 중심 분모와 혼합하지 않는다. |

검산은 네트워크 실행이나 HTTP 재생을 수행하지 않았다. 기존 원 HTTP 영수증을 다시 읽고 같은 바이트의 로컬 식별값을 검증한 것이다. API가 현재 비어 있거나 404라고 해서 당시 실행 실패·개별 삭제를 사실로 확정하지 않았다.

## 검토 스냅샷

| 파일 | 검토 시 SHA-256 |
|---|---|
| `streams/r/routes.jsonl` | `0973bcefdad41bae8f2475d0881e46da8eae3ade9bc5be7ea85ab60520854d2f` |
| `streams/r/sources.jsonl` | `a6e8975109f902375c4c614fb3e3dec92f253586b2a72d1ecd01b61438b3fb42` |
| `streams/r/summary.json` | `fd6d3d693fedd1f5050b6646222fe7f4a5ea5ea08642dde8cf7710d9e58c4b93` |
| `streams/r/claims.csv` | `6e0e49759a40a760dab9003759944a42c2f913338ac258f8f856461edbddd921` |
| `streams/r/NOTES.md` | `a5a317c8a135a51f8d6263d3a29f798559ba0911537c12e18b341d56c30f32d9` |
| `streams/r/cards.md` | `b6b67ddc3776bdadda05494a50daf42b45702bd7c0e42fadd48513fbaa0fe42c` |
| `streams/r/postrecommendations.json` | `81dee96571a4d4443005e5c12fe0ec67bbc07390e009b63342ef31e110f25c52` |

검토에 사용한 원 body는 R 작업자의 로컬 `.workbench` 파일이고, 커밋 가능한 짧은 추출과 영수증은 `streams/r/evidence/`에 있다. 새 checkout에서 모든 body 재검산을 재현하려면 영수증의 고정 URL을 먼저 내려받아야 하며, 현재 HTTP가 다시 같다는 보장은 없다. 이 감사가 확보 원문보다 강한 역사적 성공 주장을 추가하지는 않는다.
