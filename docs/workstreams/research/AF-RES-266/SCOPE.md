# AF-RES-266 범위와 사전 판정

## 착수판과 이미 본 답

- GitHub 통합 기준은 [3c32c1b44bd139819485548cb50e69e254288fad](https://github.com/laadkke-arch/agentflow-open/tree/3c32c1b44bd139819485548cb50e69e254288fad). [AGENTS.md](https://github.com/laadkke-arch/agentflow-open/blob/3c32c1b44bd139819485548cb50e69e254288fad/AGENTS.md), [STATE.md](https://github.com/laadkke-arch/agentflow-open/blob/3c32c1b44bd139819485548cb50e69e254288fad/STATE.md), [DOT_AUTOMATION.md](https://github.com/laadkke-arch/agentflow-open/blob/3c32c1b44bd139819485548cb50e69e254288fad/docs/DOT_AUTOMATION.md), [RESEARCH_WORKFLOW.md](https://github.com/laadkke-arch/agentflow-open/blob/3c32c1b44bd139819485548cb50e69e254288fad/docs/RESEARCH_WORKFLOW.md) 및 저장소 실행 안내를 읽었다. 과제의 [계획판 진행표](https://github.com/laadkke-arch/agentflow-open/blob/933a0f7d534314470c083b0aa284044a9ad45443/docs/automation/dot-control.json)에는 266 행이 없고, [착수판 진행표](https://github.com/laadkke-arch/agentflow-open/blob/3c32c1b44bd139819485548cb50e69e254288fad/docs/automation/dot-control.json)의 blob `3b6997ad21b0ae605433c65d930a2fff3b68b6c3`에는 266 RUNNING, `work/research-af-res-266`, `docs/workstreams/research/AF-RES-266/`, 의존 작업 248 하나가 있다. 원격 조회에서 작업 브랜치가 공석이었다. 첫 clone과 session fetch 사이에 진행표가 한 판 전진해 첫 핀을 영수증으로 보존하고 첫 커밋 전에 fast-forward 후 다시 시작했다. 소유 경로 내 [계약 핀](session.json)을 사용한다.
- 고정 기초판 [RESEARCH_BRIEF](https://github.com/laadkke-arch/agentflow-open/blob/933a0f7d534314470c083b0aa284044a9ad45443/docs/product/RESEARCH_BRIEF.md), [RESEARCH_WORKFLOW](https://github.com/laadkke-arch/agentflow-open/blob/933a0f7d534314470c083b0aa284044a9ad45443/docs/RESEARCH_WORKFLOW.md). 248은 중앙 DONE, 자체 PARTIAL. 중앙 result_commit과 원격 248 브랜치 tip 모두 `4a690fc68182b8b2792c15d921ed3baeeaa7220e`. [인계](https://github.com/laadkke-arch/agentflow-open/blob/4a690fc68182b8b2792c15d921ed3baeeaa7220e/docs/workstreams/research/AF-RES-248/HANDOFF.md)가 기록한 고정 결과 SHA는 `b55e3a7a283076085b09e70fbb4eacbdc3ae92fd`. 사용자 지명 인계판에서 [결과](https://github.com/laadkke-arch/agentflow-open/blob/4a690fc68182b8b2792c15d921ed3baeeaa7220e/docs/workstreams/research/AF-RES-248/RESULT.md), [matrix](https://github.com/laadkke-arch/agentflow-open/blob/4a690fc68182b8b2792c15d921ed3baeeaa7220e/docs/workstreams/research/AF-RES-248/matrix.csv), [events](https://github.com/laadkke-arch/agentflow-open/blob/4a690fc68182b8b2792c15d921ed3baeeaa7220e/docs/workstreams/research/AF-RES-248/release-events.csv), [recommendations](https://github.com/laadkke-arch/agentflow-open/blob/4a690fc68182b8b2792c15d921ed3baeeaa7220e/docs/workstreams/research/AF-RES-248/recommendations.md)를 읽었다.
- 사전 노출은 2026-11-25 00:58 UTC 착수 단계의 배정문과 위 고정판이다. HTML 5개 표시와 4개 공석, 표시 해시·날짜, 전체 표시 25/25/33, 1.14.1 cp313과 classifier 불일치, Nikon D850/Z 6II 대상, JSON 0/3 및 당시 CI 미확인을 이미 알고 시작한다. 이 커밋 전에 이번 PyPI JSON, Simple, 원 wheel, GitHub 릴리스 API 또는 Nikon 본문을 새로 열지 않았다.

## 표집과 판별

3개 SciPy 최종판(1.13.1/1.14.0/1.14.1) × 3개 일반 GIL CPython(3.9/3.10/3.13) × Linux glibc x86_64 1개로 9셀. 플랫폼 기준은 관측 파일의 manylinux 2.17 이상을 받아들이는 Linux x86_64이며 별도 glibc 2.16 경계를 대조한다. 원배열 파일(0부터의 인덱스), 환경 셀, 비교 파일, 공지 이벤트, 시험 실행, 직접 읽은 원자료와 원천 계보를 별도 모집 단위로 둔다. sdist, cp313t, macOS arm64 및 다른 libc/아키텍처는 반례로 격리한다. 탈락 원인을 태그, Requires-Python, yanked, 실행과 구분한다. 바이트를 받는 5개는 filename+SHA-256으로 248·PyPI JSON·Simple과 연결하고, ZIP 내부 태그와 METADATA와 Simple sidecar의 값을 대조한다. 역사적 공개·삭제는 시점 원자료가 있어야 판단한다.

216/229 철회판 설치, 일반 지원 정책 재조사, 무관 플랫폼 설치, 242/251/254/255 입력은 제외한다. 248의 Nikon 두 모델은 제조사 페이지의 교차 사례로만 사용한다. 펌웨어 적용을 실행하지 않는다.

| 질문 | 사전 예측과 경쟁 설명 | 합격·반전 관측 |
|---|---|---|
| Q1 | 세 판 정상 응답이면 표시 목록과 같은 규모일 가능성. 이전 프록시 실패 재현 또는 누락·변경 가능성 | 정상 상태·원본 URL/응답 헤더·본문 SHA/길이·정확한 info.version·전체 urls 구조. 실패는 미수신 |
| Q2 | HTML의 셀별 1,1,0 / 0,1,0 / 0,1,1이 현재도 유지. 복합 태그를 두 파일로 세거나 빈 셀 후보를 놓칠 가능성 | 두 파서, 원순서, 전체 분모와 파일 단위 중복 방지. 반대 파서 또는 정식 일치 파일이 나오면 수정 |
| Q3 | 다섯 파일은 표시 digest와 같을 것. 릴리스/파일/ZIP 요구값은 같을 수도 다를 수도 있음 | 직접 계산한 바이트 digest·크기와 WHEEL/METADATA를 연결하고 실제 차이를 보존 |
| Q4 | 날짜 일치만으로 선후 판단 불가. 같은 판에서도 업로드와 공지 선후가 갈릴 수 있음 | PyPI 파일별 마이크로초와 공식 공지 UTC 초를 비교. 최초 공개·삭제 이력과 구분 |
| Q5 | Simple과 버전 JSON은 키가 같을 가능성. 캐시 직렬 차이·누락·null·sidecar 불일치 가능 | 정상 두 응답에서 exact version 파일 집합 및 필드값 비교. 0건은 정상 두 모집단으로만 판정 |
| Q6 | sdist는 하한으로 통과해도 wheel 아님. free-threaded·arm64는 환경문을 바꾸면 오탐을 재현할 수 있음 | 실파일 또는 정상 인덱스 공석, 양성 대조와 탈락 조건. Nikon 모델/C 버전/호스트를 각각 확인 |
| Q7 | 태그 CI 설정이 있어도 공개 wheel 해시의 실행까지 못 이을 수 있음. 해당 job의 provenance가 남았을 가능성 | 실제 tag/job/해시 사슬 또는 미확인, 별도의 정확한 로컬 양성 시험, 빈 폴더에서 저장 응답으로 재계산 |

직접 원자료 하한은 그룹별 4/5/5/4/2, 총 20이다. 같은 원저작의 미러·재요청·실패는 성공 개수에 포함하지 않는다. 공식 PyPI/파일 호스트 원바이트 공개 응답과 재생용 파일 지문을 남긴다. 새 관측이 들어오면 사전판을 보존하고 반례/정정 단계에서 바뀐 결론을 기록한다.
