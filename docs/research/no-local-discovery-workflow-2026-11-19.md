# 탐색기를 위한 로컬 설치 없는 공통 환경

확인일: 2026-11-19. 대상: `laadkke-arch/agentflow-open`. 조사 시작 head: `1b422f6e1ac0aa5c844c49ee8928c3d65ed4c552`. 이 문서는 중요한 후보의 비교·실행 근거이며 시장 전체 조사나 제품 구현 완료 선언이 아니다.

## 목적과 선택

최종 제품은 개발 문제에서 **재사용할 도구를 발견하고 프로젝트 조건별 근거·제약을 비교하는 탐색기**다. 이번 작업은 그 제품을 여러 대화에서 조사·설계·검증할 기반을 개선한다. 실행 장소만 정하는 것으로는 목적을 달성하지 못한다.

실제 조사 질문은 '이 탐색기의 자원 발견·메타데이터·비교를 만들 때 무엇을 재사용할까?'였다. 기존 디렉터리와 API를 발견·메타데이터 공급원으로 활용하고, 프로젝트별 적합성 판단과 출처 이력을 우리의 검증 대상으로 둔다. 이것이 시장 전체에서 유일하다는 증거는 없다. 다음 제품 조사는 실제 개발 과제에서 탐색 시간·놓친 후보·잘못된 추천을 비교해야 한다.

## 원문과 현재 제약

[DCInside 글](https://gall.dcinside.com/mgallery/board/view/?exception_mode=recommend&id=ai_utilize&no=177968&page=1)은 2026-11-11 작성이며 11월 19일 본문을 읽었다. page=2 주소의 읽기 실패 뒤 같은 게시물 page=1로 확인했다. 댓글 본문은 미확인이다.

채택할 핵심은 웹 Pro의 조사·설계를 GitHub 기록과 실제 실행 결과로 연결하는 순환이다. 원문도 Actions 빌드·테스트를 제시한다. PC 실행은 선택 경로다. '무제한', 저장량과 실행량을 섞은 수치, 근거 없는 향후 차단 예측은 환경의 계약으로 삼지 않는다.

| 실행 후보 | 확인한 사실 | 결정 |
| --- | --- | --- |
| 공개 Actions 표준 러너 | 표준 hosted 실행 무료. job 최대 6시간, 동시 실행·저장 제한 별도. larger runner 유료 | **채택**: 커밋 검사. 현재 workflow 제한은 10분 |
| Codex Cloud | 작업별 workspace, 재사용 환경 발행, 기존 작업별 상태 제공 | **보조 채택**: 반복 편집·실험. 사용자 계정 발행 미완료 |
| 현재 제공된 클라우드 작업공간 | 실제 clone·명령·시험 실행 가능 | **실제 사용**: Actions 없이 검사 지속 가능성 확인 |
| Codespaces | Free 120 core-hours/15 GB-month, GitHub Pro 180/20. 중지 후 저장량은 남음 | **예비**: 사람이 브라우저 IDE를 직접 쓸 때. ChatGPT Pro와 별도 |
| Render Free | 15분 비활동 sleep, 일시적 파일시스템. 무료 Postgres 30일 만료 | **추후 시연**: 장기 기억·상시 MCP의 기본 저장소로 사용하지 않음 |
| WebJjonku/SpaceDock | 지속 호스트에서 파일·명령 MCP 실행 | **선택 유지**: 호스트 접근이 실제 필요한 경우 |
| CoS | Goal·Loop·Compact 등 웹 대화 자동 진행 | **보류**: 기본 경로에는 설치·연결하지 않음 |

Actions는 검토한 코드를 실행하며 모델 자체를 제공하지 않는다. 시간 제한을 계속 우회하는 상시 MCP 호스팅으로 구성하지 않는다. 필요한 때만 실행하므로 사용자 PC를 켜둘 필요가 없다.

공식 문서는 Work와 Codex의 사용량 공유, API-key 별도 과금을 설명한다. 사용자가 허용한 GPT-6.2 Sol Max를 활용하되 Max 추론 강도와 속도 옵션을 구분한다. 실제 잔여량은 계정 화면을 따른다. 구독의 특정 시점 혜택을 장기 지속성의 전제로 삼지 않는다.

출처: [Actions 요금](https://docs.github.com/en/billing/concepts/product-billing/github-actions), [제한](https://docs.github.com/en/actions/reference/limits), [이용 조건](https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features), [Codespaces](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces), [Codex Cloud](https://learn.chatgpt.com/docs/environments/cloud-environments), [모델](https://learn.chatgpt.com/docs/models), [사용량](https://learn.chatgpt.com/docs/pricing), [Render Free](https://render.com/docs/free).

## 커뮤니티 구현을 읽고 내린 판단

| 대상·고정 revision | 읽은 구현 | 적용 |
| --- | --- | --- |
| [WebJjonku](https://github.com/repairer5812/webjjonku/tree/e0cef9118f612ed148c6db2806f1f8b6ea2661ad) | Dockerfile, Compose, entrypoint | SpaceDock 0.1.6 기반. 1 CPU/1 GiB는 설정 제한값이며 실측 소비량 아님. 기존 통합 보존 |
| [SpaceDock](https://github.com/starlove7/spacedock/tree/41df6ed1519242e742079c84989cd15b5a4e441b) | `internal/command/manager.go`, `internal/workspace/worktree.go` | 명령 세션·제한 시간·분리 worktree 제공. in-memory session map을 영구 작업 큐로 오인하지 않음 |
| [CoS](https://github.com/totec448-spec/chat-on-steroids/tree/4d16de787ea9e79bbf880329ca0d5518ecf6213d) | `src/main/goal.ts`와 상태 관리 | 웹 ChatGPT 기본 backend와 선택형 API backend 구분. 모든 사용이 API 과금이라는 설명은 틀림 |
| [GPT Repo MCP](https://github.com/CAHN91/gpt-repo-mcp/tree/986f2135f00959f8e0d214ed8d173a7054f4cea1) | validation-service, handoff-service | 검사 프로필·버전·인수인계 원칙만 부분 채택. 실행기 중복 설치 안 함 |

[CoS #2184](https://github.com/totec448-spec/chat-on-steroids/issues/2184)는 11월 13일 v2.1.53 compact 후 이어가기 실패 보고다. 독립 재현이나 최신 main 전체 장애 증거는 아니다. 대화 자동화가 멈춰도 GitHub의 근거·결정이 남아야 한다는 운영 판단에 반영했다.

현재 기본은 진행·통합 담당 1개와 독립 검토 1개다. 독립 출처 조사에는 추가 세션을 사용하되 분류·데이터 계약 합의 전에 DB·UI 구현을 각자 확정하지 않는다. 세 세션이 항상 느리다는 실험 결과가 있는 것은 아니다. 의존성과 재조사 비용을 줄이는 설계 선택이다.

## 제품이 재사용할 후보

| 후보 | 확인한 역할 | 우리 관계·결정 | 미확인 |
| --- | --- | --- | --- |
| GitHub Search | 저장소·README·코드 발견 | component, 채택 | 질의별 회수율·기능 적합성 |
| ecosyste.ms | 저장소·패키지 메타데이터. GET 1회 HTTP 200 | component, 부분 채택 | 신선도·지속 한도·최종 재배포 형태 |
| OpenAlternative | 현재 공개 저장소는 큐레이션 목록 | reference, 부분 참고 | 현재 상용 사이트 앱 구현 |
| OSSInsight | GitHub 활동 분석. Explorer 문서와 현재 점검 상태 차이 | reference/component, 활동 자료만 검토 | 자연어 Explorer 재활성화·API 품질 |
| Libraries.io | 패키지 검색·버전·라이선스·의존 자료 | component, 보류/비교 | 우리 계정 키·실제 API·갱신 상태 |
| AlternativeTo | 서비스와 OSS 대안 발견·사용자 비교 | reference, 외부 참고 | 허가 없는 경쟁 DB 수집원으로는 제외 |

[GitHub Search API](https://docs.github.com/en/rest/search/search)는 검색당 최대 1,000개 결과와 `incomplete_results`를 설명한다. 검색 결과 누락을 자원 부재로 저장하지 않는다. 발견한 후보와 코드·실험으로 입증한 기능은 별개다.

실제 판단을 바꾼 네 가지:

1. [OpenAlternative 고정 README](https://github.com/piotrkulpinski/open-source-alternatives/blob/156045dde3d74a6bfdad675c13521718ca0e50b5/README.md)는 공개 저장소가 목록으로 바뀌었다고 설명한다. 예전 Next.js 앱을 그대로 fork한다는 제안은 현재 상태와 맞지 않는다.
2. OSSInsight [About](https://ossinsight.io/docs/about)의 자연어 기능 설명과 [현재 Explore](https://ossinsight.io/explore/)의 점검 안내를 함께 저장한다. [고정 ask 경로](https://github.com/pingcap/ossinsight/blob/77538008b8fe8b0dd3dc6caa3fc4ba987e10360a/apps/web/app/api/explorer/ask/route.ts)는 모델 실행 전에 503을 반환한다. 실제 POST 시험은 하지 않았다.
3. Libraries.io [검색 API 코드](https://github.com/librariesio/libraries.io/blob/16ef5c54bc2d2b984963aa1b342a47e595c8a85b/app/controllers/api/search_controller.rb)는 키를 요구한다. [#3616](https://github.com/librariesio/libraries.io/issues/3616)은 키 발급 문제 보고이며 독립 재현 아님. [#3620](https://github.com/librariesio/libraries.io/issues/3620)은 10월 14일 closed여서 현재 미해결이라고 쓰지 않는다.
4. AlternativeTo [2026-10-07 약관](https://alternativeto.net/about/terms/)은 경쟁 DB 구축에 내용을 사용하는 것을 금하며 등록 소프트웨어의 검증을 보장하지 않는다. 외부 발견 링크로 참고하고 기능·가격은 원제작자 자료로 다시 확인한다.

주장별 URL·revision·확인 범위·반례는 [조사 사례 JSON](discovery-case-2026-11-19.json)에 있다. [실습 fixture](../../lab/reference-audit/fixtures/discovery.json)는 기존 출처 연결 검사로 실행한다. 출처 연결 무결성과 외부 사실의 진실성은 다르다.

### ecosyste.ms: 실행 결과와 문서 충돌

인증 없이 OSSInsight 저장소를 조회해 HTTP 200을 받았다. [응답 요약](ecosystems-probe-2026-11-19.json)에 URL·시각·선택 필드·한계를 저장한다. 우리 확인 시각과 API의 `last_synced_at`을 구분한다.

[현재 가격표](https://home.ecosyste.ms/pricing)는 무료 300회/시간, [읽은 README](https://github.com/ecosyste-ms/repos/blob/6882e528ed845e9e21ffb9c244e62c5006741572/README.md)는 5,000회/시간을 설명한다. 계획은 보수적으로 가격표를 기준으로 하고 실제 사용 전 한도를 재확인한다. [공식 라이선스 문서](https://docs.ecosyste.ms/docs/usage/licences/)는 코드 AGPL과 데이터 CC BY-SA 4.0을 구분한다. 현재는 최소 관측값과 링크만 저장하며 대규모 재배포는 별도 검토한다.

## 저장·검색·갱신 구조

| 내용 | 현재 선택 | 확장 조건 |
| --- | --- | --- |
| 요구·계약·선택·실패 원인 | Git Markdown + 작은 JSON | 계속 검토 가능한 단위 유지 |
| 조사 표본·출처 | claim ID, URL/revision, checked_at, unknown, 관계·판정 | 운영 수집량이 커지면 제품 DB |
| 원시 실행 로그 | 제한된 CI artifact, 영구 요약은 docs/sessions | 모든 로그를 매 대화에 넣지 않음 |
| 운영 자원·가격·관계·이력 | 아직 제품 DB 없음 | CRUD·권한·중복·조회 계약 뒤 관계형 DB |
| 전문·벡터 검색 | 보류, 현재 필요한 Git 자료만 선택해 읽음 | 실제 질의셋에서 품질 이득과 비용 검증 |

자원, 기능 주장, 출처 관측, 프로젝트별 판단을 의미상 분리한다. 자원 전체의 `verified=true` 한 개로 모든 기능을 인증하지 않는다. '문서 설명'과 '현재 비활성'은 함께 존재할 수 있다. 판단에는 요구조건과 사용한 근거, 재검토 조건을 남긴다.

기존 5테이블은 수업 조건을 고려한 초안이다. 위 의미를 어느 테이블·JSON·이력으로 표현할지는 다음 설계 검토 대상이다. 이번 작업에서 최종 DB를 고정하지 않는다. 검색 엔진은 이미 가진 자료를 찾는 부품이므로 자료 공급원과도 구분한다.

개발 기록의 재사용은 현재 상태와 관련 근거만 먼저 읽고 필요할 때 원문·코드·로그를 여는 방식이다. 원문 전체를 모든 채팅에 복사하지 않는다. 웹 Claude를 추가하더라도 같은 계약과 인수인계를 적용할 수 있지만 이번 기본 구성에는 추가 연결하지 않았다.

## 실행·완료 경계

공통 cloud wrapper, 문서 변경 CI, 과제 계약·경로·의존 검사, 실제 조사 표본을 추가했다. 실패·timeout·계약 drift·병합·충돌 복구는 Git/프로세스로 시험한다. 최신 결과는 [STATE.md](../../STATE.md)의 검사 SHA와 실행 링크로 확인한다.

사용자 Codex 환경 발행, 별도 사용자 웹 채팅 인수인계, 제품 검색 품질, DB·앱 배포는 미완료다. Render에는 선택된 workspace가 없어 자원을 만들지 않았다. 현재 판단은 **로컬 PC 없이 조사와 작은 구현·검증을 이어갈 기반을 사용할 수 있다**는 것이며 모든 제품 설계가 최적이라는 선언이 아니다.
