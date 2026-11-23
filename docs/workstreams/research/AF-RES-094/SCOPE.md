# AF-RES-094 연구 범위

2026-11-23 UTC. `laadkke-arch/agentflow-open`의 `work/research-af-res-094`에서 `docs/workstreams/research/AF-RES-094/`를 소유한다.

- 계획 기준 `e2a80afec762b10ee7979136c6332473c70905bb`. 실제 시작 통합판 `f72073277e6be643302a33f204d70baeb2c749a4`는 브랜치 부재 확인 뒤 GitHub에서 받아 고정했다. [시작 커밋](https://github.com/laadkke-arch/agentflow-open/commit/f72073277e6be643302a33f204d70baeb2c749a4)
- 통합판의 `AGENTS.md`, `STATE.md`, `docs/DOT_AUTOMATION.md`, `docs/RESEARCH_WORKFLOW.md`와 `dot-control.json`의 AF-RES-094를 읽었다. AF-RES-094의 직접 의존은 AF-RES-090 하나다. [배정표](https://github.com/laadkke-arch/agentflow-open/blob/f72073277e6be643302a33f204d70baeb2c749a4/docs/automation/dot-control.json#L2177)
- 선행 인계는 배정표의 `result_commit`인 `e5f6cf5b1cb27b926ebc2356f9a8b763cebfcc87`. 090의 결과·카드·대상·파일 지문·경로는 `03c6102d6c0d90f6722550d5e2cb1c7219e49b5f`를 읽었다. 당시 본문 엄격 3/8, 후속 엄격 0/8은 비교의 배경이다. [인계](https://github.com/laadkke-arch/agentflow-open/blob/e5f6cf5b1cb27b926ebc2356f9a8b763cebfcc87/docs/workstreams/research/AF-RES-090/HANDOFF.md), [결과](https://github.com/laadkke-arch/agentflow-open/tree/03c6102d6c0d90f6722550d5e2cb1c7219e49b5f/docs/workstreams/research/AF-RES-090)
- 판별 대상은 탐색기가 특정 목적에 도움이 되는 제품·부품·원리를 반환할 때 공통 본문 옆에 후속 주소 하나를 넣는 조건이다. [제품 연구 브리프](https://github.com/laadkke-arch/agentflow-open/blob/e2a80afec762b10ee7979136c6332473c70905bb/docs/product/RESEARCH_BRIEF.md)

## 질문과 봉인

| 질문 | 관측 입력 |
|---|---|
| Q1 목적과 판 관계 | `freeze.json`의 여섯 목적, 출처·파일명·원URI·지문. 본문 두 자리는 지정 릴리스의 본문 자체가 끝점이다. |
| Q2 카드 차이 | `cards.csv`의 공통 첫 주소·본문 문구를 동일하게 제시한다. B만 검증 근거가 있는 추가 URL을 명시한다. R2-next의 추가 URI는 미확인으로 세며 실제 링크를 제공하지 않는다. |
| Q3 접근과 시간 | 새 Chromium 세션 (카드·목적별 별도 쿠키/저장소/캐시)과 쿠키 없는 GET. 각 목적 네 경로는 같은 고정 UTC 10분 구간에서 시작한다. A/B 순서는 표의 `card_order`를 목적별 교차한다. 시작이 구간을 넘는 행은 그대로 남긴다. |
| Q4 열람 예산 | 첫 문서는 공통 입구. 남은 한 번은 B의 명시 링크 또는 A의 실제 노출 주소다. 첫 실패 뒤에도 B의 명시 링크는 한 번 시도할 수 있다. 본문 대조는 첫 화면에서 목적을 충족하면 종료한다. 자동 3xx, 같은 문서 앵커, 메뉴 펼침, 브라우저 하위요청은 별도 열. 실패, 새 문서 raw 전환도 한 번이다. |
| Q5 판독 | 도착·본문·후속 payload·판 관계는 독립 열이다. 릴리스는 고정 source/tag, 실제 표시 또는 복원·원파일 지문으로 확인한다. 후속이 필요한 경우 본문·payload·판 관계 모두 충족해야 엄격 성공이다. P1에서 현재 서비스 목적과 7.0.1 당시 동일판 귀속을 별도 점수로 둔다. |
| Q6 효과 | 수단별 6쌍. B 단독·A 단독·양쪽·둘 다 실패·비교불가를 센다. 카드 명시 주소 변경 3자리와 실제 두 번째로 요청한 URL이 양쪽에서 달랐던 쌍을 독립 집계한다. 한쪽만 요청한 쌍도 별도 집계한다. 090의 R1/R2 blob 두 주소는 주 구간 UI/GET 대조, 차이가 남으면 각 1회 추가. |
| Q7 타 분야 | 090의 IIIF Cookbook 0001/Archive 사건 61 및 Accessible EPUB 3과 다른 공개 사례. IIIF 내장 Canvas, 그 id, painting body를 각각 확인한다. EPUB은 패키지·내부 표지·외부 참조를 확인하고 웹과 ZIP 내부 파일 수를 분리한다. |

## 선택과 채점 규칙

1. A에서 다음 자원을 선택할 수 있을 때 목표 자원의 이름, 판, 문서순으로 고른다. P3의 정확한 root 표가 없다면 실제 노출된 1.x의 대응 options가 대조 후보다. R1에서는 Examples 첫 `system.file` URI만, P1에서는 첫 `Minmal` 코드 블록의 `master`만, R2에서는 이 절에 귀속된 SVG 또는 cast만 선택한다. 옵션 설명, 로고, 별도 데모는 R2의 대체 payload가 아니다. 공개 화면에서 전체 URI 복사는 가능하며 링크 클릭과 구별한다. HTTP의 후보는 그 응답의 HTML·복원한 파일에서 직접 노출된 주소다. 다른 클라이언트에서만 발견한 동적 주소와 예측·조립한 주소는 보조 관측이다.
2. 첫 문서가 오류이면 A는 노출 근거가 없는 한 종료한다. B의 명시 주소는 첫 실패를 보존한 채 시도한다. 조회 또는 MIME 성공만으로 목적을 올리지 않는다. 접근 가능한 목록에서 목표 payload를 얻지 못하거나 판 연결을 확인할 수 없으면 `미확인`이다. 필요한 요청 자체가 막히면 `접근 실패`다. 접근 실패를 요청으로 세고 상태·원주소·본문 표본·다음 최소 관측을 남긴다. 계측이 빠지거나 시간 기준이 어긋나면 대응쌍의 비교불가로 남긴다.
3. 긍정적 예상은 P3 B의 root 직행, P1 master 문자 복사의 A/B 동률, 내장 R2 정적 `<pre>` 한 링크다. 반증 대상은 v3.3.0 options가 root를 직접 노출하는 경우, P1 링크가 A에서만 작동하는 일시 차이, R1 도움말의 생성판 식별 가능성, R2의 이 절에서 드러나는 외부 파일 또는 인라인 실제 SVG나 재생 데이터다. HTTP 200 오류, 503, 404, 같은 본문에 다른 후속판, URI 부재를 추적한다.
4. 본문의 완전한 응답 지문, 복원한 소스 지문, 선택 영역 지문을 별개로 둔다. 사이트·발행자의 버전 근거와 연구자의 채점, 설계 제안을 구별한다. 090의 배포·게시 이력, 가능한 모든 최단 경로, 전체 예제·재생 실행은 별도 범위다. HTTP 바이트·시간은 사람의 독해 비용으로 환산하지 않는다.
5. 외부 1차 자료 하한은 발행자·고정 소스 8, 실제 문서·후속·서비스 8, 공식 규칙 4, IIIF와 EPUB 각각 규격·발행물 최소 2로 총 24다. 같은 원문의 반복·미러, 검색 요약, 오류, 선행 자료, 자체 출력을 하한에서 제외한다. 외부 고유 원문과 문서의 저작·사건 계보 수를 따로 센다. 주 경로 밖 직접 열람은 출처 근거로만 쓰고 주 점수를 보정하지 않는다. 분모 0은 `산출 불가`다.
