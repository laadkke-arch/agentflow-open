# 커뮤니티 웹 개발 방식 비교와 실제 적용

확인일: 2026-11-15. 목적은 AgentFlow Open 탐색기 구현 전에 여러 프로젝트를 조사·개발·검증·기록할 실제 웹 작업환경을 갖추는 것이다. 제품 코드는 아직 본격 구현하지 않는다.

## 원문과 기존 구성에서 부족했던 부분

사용자가 제공한 글의 핵심은 Git 기록, 실행기, 실패에서 개선한 절차의 재사용이다. 그러나 그 글의 1~15단계만으로 다음 부분이 자동 구현되는 것은 아니다.

- 매번 GitHub 업로드와 Actions를 기다리지 않는 직접 편집·명령 실행 경로.
- 오래 걸리는 명령을 중복 시작하지 않고 같은 실행을 관찰·중지하는 기능.
- 대화가 끝났을 때 이어 보낼지 판단하는 Goal/Loop와 새 대화로 옮기는 Compact 계층.
- 여러 프로젝트의 기억을 섞지 않고 필요한 이전 판단을 다시 읽는 경계.
- 작업 파일·기억·Git 커밋·원격 push·서비스 배포의 서로 다른 지속성.

기존 자체 Python workbench는 검사와 기록의 보조 도구로 유지한다. 그것만으로 사용자가 요청한 웹 작업환경을 완성했다고 취급하지 않는다.

## 커뮤니티에서 확인한 사용 방식

| 출처 | 읽은 범위와 얻은 내용 | 적용 판단 |
| --- | --- | --- |
| [디시 웹쫀쿠 효율적으로 쓰는법](https://gall.dcinside.com/mgallery/board/view/?id=ai_utilize&no=20263) | 본문. Oracle·DevSpace로 웹 대화와 로컬 작업을 연결하는 사용자 설명. | Git 아카이브와 직접 실행 연결은 별개라는 출발점. 개인 성능·한도 체감은 일반 사실로 쓰지 않는다. |
| [디시 웹쫀쿠 자동 세팅하기](https://gall.dcinside.com/mgallery/board/view/?id=ai_utilize&no=22829) | 본문. MCP 편집, 작업 분리, PR·검사, 상태·체크포인트를 묶는 구성 요청. | 완성된 배포 패키지가 아니라 설치·구현 지시문이다. 보호 범위와 결과 대조를 참고하며 자동 병합 지시는 채택하지 않는다. |
| [디시 연결 안내 67044](https://gall.dcinside.com/mgallery/board/view/?id=ai_utilize&no=67044) | 검색에 노출된 본문. CoS, 터널, 로컬 연결 확인 순서. | 오래된 화면·설정 이름을 그대로 설치 계약으로 사용하지 않고 실제 원본과 대조한다. |
| [DevSpace 개발자 Reddit 소개](https://www.reddit.com/r/codex/comments/1ubrhup/openai_ended_the_2x_codex_promo_so_i_fixed_it_by/) | 본문. 웹에서 조사·계획·검토하고 로컬 에이전트와 작업을 나누는 개발자 사례. | 실제 기능의 근거는 원본 코드로 확인한다. 사용량을 늘리는 마법이나 제한 우회로 해석하지 않는다. |
| [GPT Repo MCP 개발자 사례](https://www.reddit.com/r/codex/comments/1tyba25/i_built_a_local_mcp_to_make_chatgpt_codex/) | 본문. ChatGPT와 코딩 도구 사이의 읽기·검토·인수인계 방식. | 검증 프로필·stale-state 검사를 비교했다. 모든 셸 작업을 허용해야 하는 것은 아니다. |
| [mcp-agentic-server 개발자 사례](https://www.reddit.com/r/codex/comments/1v2sf96/i_built_an_mcp_server_to_bring_more_of_the_codex/) | 본문. 구조화된 편집과 worktree·패키지 작업 연결. | 후보로 보관. 현재 Python 기반 공통 실험에는 우선 설치하지 않는다. |
| [SpaceDock 작성자 소개](https://siriusstars.tistory.com/67) | 검색에서 확보한 작성자 본문. 직접 페이지 접속은 실패. | 구조화된 도구·명령 세션·recall 후보를 발견했다. DevSpace보다 빠르거나 안전하다는 작성자 평가는 독립 검증하지 않았다. |

커뮤니티 글은 실사용의 발견 근거다. 이번에 최신 댓글 전체를 읽거나 커뮤니티 전체를 조사했다고 주장하지 않는다. 과거 글을 원글의 최신 후속 버전이라고 부르지도 않는다.

## 실제 구현 후보 비교

| 후보 | 역할 | 이번 판단과 근거 수준 |
| --- | --- | --- |
| [repairer5812/webjjonku](https://github.com/repairer5812/webjjonku) + [starlove7/spacedock](https://github.com/starlove7/spacedock) | Docker 안의 OAuth·파일 편집·명령 세션·worktree·recall | 이번 직접 실행 계층으로 채택. 서버를 새로 구현하지 않고 원본의 고정 커밋을 빌드하고 실제 MCP로 시험한다. |
| [Chat On Steroids](https://github.com/totec448-spec/chat-on-steroids) | 데스크톱 앱·브라우저 확장·작업자·Goal·Loop·Compact & Resume | 사용자가 요구한 긴 작업 지속에 가장 직접적인 후보. README, setup, recovery inventory와 goal.ts를 확인했다. 개인 PC·브라우저 로그인과 연결 권한이 없으므로 설치나 웹 실사용을 완료했다고 하지 않는다. |
| [DevSpace](https://github.com/Waishnav/devspace) | 로컬 작업공간과 여러 CLI 에이전트 연결 | 실행·편집·별도 worktree와 다양한 에이전트 활용 후보. 원본 README, package.json과 MCP 테스트 소스를 검토했다. 이번에는 중복 런타임으로 설치하지 않는다. |
| [웹쫀쿠 via Agents](https://github.com/magama01/webjjonku-via-agents) | Oracle·DevSpace를 묶어 Claude/Codex/Antigravity에서 웹에 작업 위임 | IDE/CLI가 주 작업자일 때의 대안. 세션별 ChatGPT Project, 제출 락, 연결 마법사는 참고. 개인 브라우저를 자동 사용하지 않았고 실제 로그인 실행은 미실시. |
| [GPT Repo MCP](https://github.com/CAHN91/gpt-repo-mcp) | read/write/ship 모드와 승인한 검사, 실제 diff·로컬 커밋 | 좁은 권한의 저장소 작업에 적합한 후보. 임의 셸·자동 push·자동 배포를 제공하지 않는다고 원본이 명시한다. 현재 선택과 중복 설치하지 않는다. |
| [mcp-agentic-server](https://github.com/hugolsramos01-bit/mcp-agentic-server) | 파일 편집·작업공간·웹 프로젝트 도구 | 개발자 사례를 확보한 탐색 후보. 독립 빌드·원본 전체 보안 검토는 하지 않았으므로 실행 검증 후보와 구분한다. |

## Goal을 단순한 수동 인수인계와 구분

CoS 원본은 Goal·Loop·Compact & Resume를 실제 기능으로 설명한다. goal.ts에는 종료한 대화에 대한 다음 메시지를 준비하고 브라우저가 전달하는 구조가 있으며, 복구 목록은 자동 Continue, 실패·정지 상태, 재시도 예산과 승인 대기를 구분한다. 따라서 '모든 웹쫀쿠는 사람이 매번 이어가라고 해야 한다'는 설명은 부정확하다.

동시에 이 기능이 현재 채팅에 설치된 것도, 무한 연산을 보장하는 것도 아니다. 작성자가 공개한 2026-10-13 야간 사례에서는 자동 Continue를 페이지가 수집하지 않아 재시도 예산이 소진된 뒤 수동 복구가 필요했다. 실제 한계와 실패 사례가 있는 자동 진행 장치로 평가한다.

근거:
- https://github.com/totec448-spec/chat-on-steroids/blob/main/README.md
- https://github.com/totec448-spec/chat-on-steroids/blob/main/docs/recovery-inventory.md
- https://github.com/totec448-spec/chat-on-steroids/blob/main/src/main/goal.ts
- https://github.com/totec448-spec/chat-on-steroids/blob/main/docs/setup.md

## 우리에게 적용한 변경

1. **원본 재사용:** OAuth, MCP 서버, 명령 세션, worktree, recall은 WebJjonku/SpaceDock 원본을 사용한다.
2. **프로젝트 기억 분리:** recall 소스가 root_id로 검색·쓰기한다는 것을 확인했다. demo·agentflow-open·shared를 별도 root로 설정하고 shared의 command.execute를 제외했다. 이는 악성 코드 사이의 보안 격리가 아니다.
3. **호환 환경:** 원본 Debian Python은 3.11이고 기존 workbench doctor의 계약은 3.12 이상이다. 검사 일부가 통과해도 실제 시작 명령이 실패할 수 있어 Python 3.12를 이미지에 추가하고 doctor를 실제 MCP로 검증하도록 했다.
4. **보존:** 전용 named volume, 재생성 시험, 명시적 Git 커밋을 사용한다. 로컬 커밋과 원격 push를 혼동하지 않는다.
5. **연결 승인:** 기본 설치는 공개 터널을 만들지 않는다. 사용자가 허용한 별도 connect 단계에서만 임시 HTTPS를 연다. 사용자 홈·SSH 키·Docker 소켓은 마운트하지 않는다.
6. **장기 진행 계층:** CoS의 Goal/Compact를 참조하되 현재 로컬 승인 없이 브라우저 기록 수집이나 자동 메시지 전송을 켜지 않는다. CoS Core와 SpaceDock의 역할이 겹치므로 두 실행기를 무조건 함께 설치하지 않는다.

## 실제 테스트와 아직 필요한 연결

실행 기록은 docs/sessions/의 community-runtime 결과를 따른다. 직접 검증한 것은 일회용 Linux 컨테이너의 upstream HTTP OAuth, 실제 stdio MCP, 기존 두 프로젝트 실행, 기억 분리·재시작, worktree, 설치 프로필의 재생성이다. 사용자 Windows Docker Desktop과 실제 ChatGPT 앱 연결은 별도 확인 대상이다.

최종 사용자 흐름은 '웹에서 조사·작업 → 직접 런타임에서 수정·검증 → 검토한 결과를 GitHub에 저장 → 필요한 기록만 다음 작업에서 읽기'다. GitHub Actions는 이 흐름을 별도 환경에서 검증하는 수단이지 편집 도구나 무한 모델 호출기가 아니다.
