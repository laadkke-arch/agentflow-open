# Q6 보충: 현재 공식 지원 범위와 실제 비용의 경계

2026-11-23 UTC에 공식 공개 원문4곳을 직접 열었다. RTD2곳과 GitHub Pages2곳이며, 기존 `OFF-RTD`·`OFF-PAGES` 계보에 합친다. 신규 독립 계보는0이다. 기존 Python 파일·사전 A/B 점수는 수정하지 않았다. 실행·로그인·계정 조회·게시·지원 요청은 하지 않았다.

| 공식 안내 | 현재 직접 확인한 범위·수치 | 이 자료가 입증하지 않는 것 |
|---|---|---|
| [RTD 가격](https://about.readthedocs.com/pricing/) — COST-RTD-PRICE | Community는 공개 저장소·공개 문서·광고 지원이며 OSS에 무료다. Business는 월 $50부터 안내한다. | 소비자의 실제 플랜·청구액·도메인 비용·운영 인건비 |
| [RTD Build resources](https://docs.readthedocs.com/platform/stable/builds.html#build-resources) — COST-RTD-LIMIT | Community: 빌드15분, 메모리7GB, 동시빌드2개, 디스크5GB soft limit. 프로젝트별 빌드시간 증액을 요청할 수 있다. | 대상 프로젝트의 실제 할당·예외 승인·과거 한도·실제 자원 사용량 |
| [Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) — COST-PAGES-LIMIT | 공개 저장소는 GitHub Free/Free for organizations에서 이용 가능. 게시1GB 상한, 배포10분 timeout, 월100GB bandwidth soft limit, 시간당10build soft limit. 마지막 build 제한은 custom Actions workflow에는 적용되지 않는다. | 특정 저장소의 게시 권한·승인·실제 사용량·청구. 이 예외가 모든 Actions/Pages 제한을 없애지는 않는다. |
| [Pages 개요](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) — COST-PAGES-SCOPE | 정적 파일 게시와 선택적 빌드 지원. 사용자/조직 사이트의 기본 루트와 프로젝트 사이트의 기본 하위 경로가 다르고 custom domain도 지원한다. | 실제 DNS 권한·기존 딥링크 보존·구판 디렉터리 유지·generator 설치 작업의 완료 |

## 결과에 반영할 구분

**공급자 지원**은 공개 문서를 게시할 수 있는 현재 이용 범위와 기본 자원 조건이다. **프로젝트 권한·작업**은 선택된 저장소의 설정, 운영자의 공개 결정·실행 기록, 연결된 배포 근거에서 확인해야 한다. **실제 비용**은 청구·사용량·사람의 소요시간 자료가 필요하다. 무료 플랜 존재를 프로젝트 총비용0이나 담당자 시간0으로 바꾸지 않는다.

현재 가격과 제한을2024–2025 사건 당시의 계약으로 소급하지 않는다. 원문에서 무료 OSS 경로가 확인됐더라도, 연구 대상 프로젝트가 실제로 그 기본 할당을 받았는지와 특별 지원을 받았는지는 미확인이다. RTD의 프로젝트별 증액 가능성 역시 이미 부여된 권한으로 세지 않는다.

Pages의 소스 저장소1GB는 **권장치**, 게시 사이트1GB는 **상한**이다. 일반적인 상업거래나 SaaS를 운영하는 무료 호스팅 용도 제한도 있으므로, 공개 저장소라는 사실 하나로 모든 웹 서비스 목적을 승인하지 않는다. 이번 비교 대상의 문서 게시와 제품 서버 운영을 합쳐 평가하지 않는다.

이 보충으로 실제 과금 자료가 있는 사례 수나 사람 작업시간을 관측한 사례 수가 늘지는 않는다. 기존 설정 블록·원문 열람·별도 아티팩트·확인된 수작업 수는 유지하고, 금전·시간의 빈칸은 계속 **미확인**으로 둔다. 추정 시급·과금 환산·월간 비용 합계는 만들지 않았다.

## 열람·검산

성공 원문4행은 `sources.jsonl`에 URL·절/행·UTC·확인 내용·한계로 남겼다. RTD의 처음 시도한 limits.html은 접근 실패였고, 공식 도메인 검색으로 찾은 builds.html을 직접 열어 대체했다. 실패와 검색 스니펫은 `attempts.jsonl`에만 기록했으며 최소 자료 수에 넣지 않았다. About Pages는 What is GitHub Pages로 redirect된 최종 URL을 기록했다. 원문 전체는 복제하지 않았다.

JSONL 파싱, 고유 source ID4개, 기존 계보2개·추가 계보0개, 각 source의 Q6 및 한계 필드를 확인했다. 웹 도구가 실제 origin HTTP 횟수나 바이트 지문을 노출하지 않아 이를 추정하지 않았고 논리적 open 수만 각각1로 남겼다.
