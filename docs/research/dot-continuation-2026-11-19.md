# GitHub 인수인계와 Dot의 가벼운 진행 연결

확인일: 2026-11-19. 최근 사례 범위: 2026-11-01~19. 대상은 탐색기를 조사·설계·검증할 공통 환경이다.
문서·사용자 보고(D1), 고정 소스 관찰(D2), 우리 환경 실행(D3/D4)을 구분한다. 이번 연결의 D3/D4 증거는 없다.

## 1. 선택한 구성

**GitHub에 작업 상태를 남기고 Dot이 필요한 때 새 작업자에게 읽히면 세션을 교체하며 이어갈 수 있다.**
한 대화를 끝없이 유지하거나 새 기억 시스템을 만드는 것이 목표가 아니다.
웹 ChatGPT Pro는 깊은 조사·설계·독립 검토의 중심으로 유지하고, Codex Cloud는 반복 구현·실험의 보조 실행환경으로 쓴다.

| 구성 | 맡길 역할 | 이번에 확인할 경계 |
| --- | --- | --- |
| 웹 ChatGPT Pro / Astra | 문제 정의, 근거 조사, 설계 판단, 결과 검토 | 원하는 모델의 새 웹 작업자를 실제로 만들고 인계할 수 있는가 |
| Dot | 작업 묶음 전달, 완료·정체 확인, 필요할 때 교체 | 매 도구 호출에 개입하지 않고 기존 작업자 ID를 먼저 확인 |
| Dot의 OpenAI 클라우드 컴퓨터 | Git 상태·필요한 파일·diff·receipt 확인, 작은 검사 | 영구 저장소나 무기한 실행 호스트로 가정하지 않음 |
| Codex Cloud / Sol Max | 반복 편집, 디버깅, 테스트 | 웹 Pro 역할을 대신하는 유일한 작업자로 바꾸지 않음 |
| GitHub + Actions | 상태·결정·코드·검사 커밋과 결과 보존 | 저장만으로 새 모델 작업이 자동 시작되는 것은 아님 |

이는 역할 배분과 연결 시험의 설계다. native Dot이 임의의 일반 웹 Pro 대화를 원하는 모델로 생성·교체한다는 기능은 아직 확인하지 못했다.
GitHub 인수인계의 가능성과 그 대화를 실제 생성하는 제어 경로를 구분해 확인한다.

## 2. 11월 실사용 자료에서 얻은 운영 판단

아래는 작성자의 경험이며 우리 계정에서 재현한 결과가 아니다. 후기의 작업 기간을 단일 모델 세션의 최대 시간으로 바꾸지 않는다.

| 관측·게시 시점 | 1차 출처와 관측 | 적용할 판단 |
| --- | --- | --- |
| 11-03 색인, 11-04 댓글 | [Dot을 개발 중간 관리자로 사용](https://www.reddit.com/r/codex/comments/1xn92w0/holy_smokes_the_dot_is_an_amazing_middle_manager/): Chat 기획을 Dot이 Codex에 전달하고 완료·판단 요청을 알렸다는 경험. 댓글에는 약 4일 작업 감시와 2시간 간격 보고 사례가 있음 | 인계·완료 확인은 유용한 역할. 4일 연속 추론이나 PC 전원 종료 검증은 아님 |
| 같은 글의 다른 사용자 | GitHub 문서를 가리켜 작업시키지만 Dot이 지나치게 개입하면 더 느려졌다는 보고, 조용히 멈추거나 알림이 오지 않았다는 반대 경험도 있음 | 정상 진행 중에는 간섭하지 않고 완료·실패·정체에만 개입 |
| 11-10 | [지속 작업의 후속 실행 질문](https://www.reddit.com/r/codex/comments/1xslemm/how_do_you_get_codex_and_dot_to_follow_through_on/): 한 번 전달한 뒤 후속 확인이 약하다는 경험과 repo 작업 파일·짧은 완료 조건으로 개선됐다는 댓글 | 다음 미완료 항목과 완료 조건을 GitHub에 명시 |
| 11-04 관측, 11-05 작성, 11-06 후속 | [openai/codex #59687](https://github.com/openai/codex/issues/59687): 같은 Dot의 작업 문맥이 이어지지 않았으며 과거 메시지 재검색으로 일부 사실만 복구됐다는 보고 | 새 세션이 현재 상태·결정·다음 행동을 직접 읽게 함 |
| 11-16 관측·작성 | [openai/codex #61856](https://github.com/openai/codex/issues/61856): 다른 대화의 답변 ID·시각은 찾지만 본문은 `content_omitted: true`였다는 보고 | 다른 채팅 검색만 기대하지 않고 산출물·커밋·검사 결과로 인계 |

첫 Reddit 글은 날짜가 명시된 검색 색인과 댓글을 기준으로 기록했다. 열린 페이지의 캐시된 상대 시간으로 날짜를 다시 계산하지 않았다.
11-10 글은 검색에 노출된 본문·댓글을 확인했으며 전체 페이지는 읽기 오류였다. 이를 전체 토론을 검토한 것으로 표현하지 않는다.
#59687의 11-16, #61856의 11-18 후속 활동에는 무관한 홍보 댓글이 있어 새 장애나 해결 근거로 세지 않았다.
이 사례들은 사용자 제안인 GitHub 인수인계를 뒷받침한다. 세션 교체 자체를 피해야 한다는 결론은 아니다.

## 3. CoS는 실제 자동 이어가기 구현이 있지만 이번 기본 경로의 선행조건은 아니다

| 구분 | 확인한 버전·시각 | 의미 |
| --- | --- | --- |
| [안정판](https://github.com/totec448-spec/chat-on-steroids/releases/tag/v2.1.53) | v2.1.53, 11-13 15:00 UTC; `dac3387f6109aa1a62ab9228798d8da6594212af` | 기본 Goal·Loop·Compact & Resume 제공 |
| 읽은 main | 11-16 23:28 UTC; `4d16de787ea9e79bbf880329ca0d5518ecf6213d` | 안정판 이후 복구 수정 포함 |
| [Canary](https://github.com/totec448-spec/chat-on-steroids/releases/tag/canary) | 11-17 00:17 UTC, 위 main SHA의 시험 빌드 | 정식 릴리스가 아니며 자동 안정판 업데이트와 다름 |
| 2.1.54 | 11-19 확인 시 releases에 없음 | 유지보수자의 배포 예정 언급을 출시로 취급하지 않음 |

main에서 직접 읽은 코드:

- [goal.ts](https://github.com/totec448-spec/chat-on-steroids/blob/4d16de787ea9e79bbf880329ca0d5518ecf6213d/src/main/goal.ts)의 `GOAL_RESPONSE_FORMAT`은 stop/continue, `LOOP_RESPONSE_FORMAT`은 continue만 허용한다.
- 같은 파일의 `startGoalDraft()`는 같은 턴의 draft를 재사용하고 다른 탭의 중복 작성권을 거부한다. `pauseRepeatingGoal()`은 반복 답변으로 멈추는 경로다.
- [config.ts](https://github.com/totec448-spec/chat-on-steroids/blob/4d16de787ea9e79bbf880329ca0d5518ecf6213d/src/main/config.ts)의 기본 Goal·Loop backend는 `chatgpt`다. 별도 모델 API backend는 선택 사항이다.
- [continuation.ts](https://github.com/totec448-spec/chat-on-steroids/blob/4d16de787ea9e79bbf880329ca0d5518ecf6213d/src/main/session/continuation.ts)의 `attachSummary/capture`는 요약 저장, `claimContinuationNow`는 단일 claimant, `commitContinuationResult`는 새 대화로 세션 결합을 맡는다.
- `recoverContinuationFromRecordedBootstrap()`는 RESUME marker·저장 summary·message ID·목적 대화 일치를 확인한다. `restoreContinuations()`는 저장 상태를 복원한다.
- 이 continuation 파일은 안정판에서도 같은 blob `2198933abce3e21d678ab9b1cd1705687e65f229`였다. 기본 이전 구조와 최신 복구 수정을 혼동하지 않는다.
- [handoff.ts](https://github.com/totec448-spec/chat-on-steroids/blob/4d16de787ea9e79bbf880329ca0d5518ecf6213d/src/main/session/handoff.ts)의 `prepareHandoff()`는 빈 요약·길이를 검사하고 저장된 계획·요청을 붙인다. `resumeBootstrapMatches()`는 전달 본문을 대조한다.

이 검사는 전달 정체성과 저장 상태를 확인한다. 요약에 과거 요구가 의미상 모두 보존됐다는 증명은 아니다.
너무 긴 요약은 길이 제한으로 줄어드는 경로도 있으므로 중요한 결정·실행 증거는 GitHub에서 다시 읽을 수 있어야 한다.

### 선택 모델의 자동 compaction 예외

[store.ts의 automaticCompactionAllowed](https://github.com/totec448-spec/chat-on-steroids/blob/4d16de787ea9e79bbf880329ca0d5518ecf6213d/src/main/session/store.ts)는 자동 압축 설정이 켜져 있어도 선택 모델이 `isProModel()`이면 제외한다.
[chat-models.ts](https://github.com/totec448-spec/chat-on-steroids/blob/4d16de787ea9e79bbf880329ca0d5518ecf6213d/src/shared/chat-models.ts)는 Astra·Pro 모델 또는 pro effort를 이 범주에 넣는다.
**ChatGPT Pro 요금제 전체의 예외가 아니라 선택 모델의 예외다.** Sol max 등과 Astra/Pro를 같은 자동 세션 교체 조건으로 취급하지 않는다.

### 최근 실패와 수정의 범위

- [#2184](https://github.com/totec448-spec/chat-on-steroids/issues/2184), 11-13~16: writing/opening 멈춤과 저장된 대화가 live 화면을 따라오지 않는 사례. 11-19에도 open이었다.
- [#2189](https://github.com/totec448-spec/chat-on-steroids/pull/2189), [#2193](https://github.com/totec448-spec/chat-on-steroids/pull/2193), [#2195](https://github.com/totec448-spec/chat-on-steroids/pull/2195)는 11-14~15 main에 merge됐다.
- [bridge.ts](https://github.com/totec448-spec/chat-on-steroids/blob/4d16de787ea9e79bbf880329ca0d5518ecf6213d/src/main/bridge.ts)의 `continueStuckFromSavedSummary/inspectOwedCompactions/noteSavedCopyBehind`가 조건부 저장 요약 복구를 구현한다.
- 유지보수자는 #2195의 원래 서비스 현상을 재현하지 못해 제공된 타임라인으로 시험했다고 밝혔다. 작성자의 마지막 답변도 새 릴리스 후 확인 예정이므로 실사용 해결 확인은 아니다.
- [#2208](https://github.com/totec448-spec/chat-on-steroids/issues/2208), 11-16~18: Loop 조기 종료라는 제목이지만 사용자가 Normal 모드였다고 정정했다. 제목만으로 Loop 결함을 주장하지 않는다.

## 4. gh-aw와 AO에서 가져올 것

### gh-aw: 작업 큐의 설계 참고

[공식 Codex engine 문서](https://github.github.com/gh-aw/engines/codex/)는 ChatGPT 구독 로그인을 지원하지 않는다고 설명한다.
따라서 gh-aw를 이번 웹 Pro 구독의 자동 실행 엔진으로 채택하지 않는다.
[고정 work-queue 문서](https://github.com/github/gh-aw/blob/a89e7f6c629005a60eae829079af9be36ff29802/docs/src/content/docs/reference/work-queue.md)의 작업 식별·인수인계·모호한 시작 상태 복구를 프로토콜 참고로 삼는다.
확인 revision은 `a89e7f6c629005a60eae829079af9be36ff29802`다. 별도 프레임워크 설치 없이 기존 worker ID·시도 번호·receipt를 재사용한다.

### AO: 모바일 클라우드 운영의 선택형 외부 서비스

[11-14 공식 업데이트](https://orchestrator.inc/changelog/2026-11-14-weekly-update/)는 모바일 2.4.0의 클라우드 세션 생성·제어와 로그인 흐름을 소개한다.
[11-11 merge된 PR #8085](https://github.com/OrchestratorInc/agent-orchestrator/pull/8085)의 작성자는 iPhone·Pixel 시험을 보고했다. 우리 계정의 실행·PC 종료 검증은 아니다.
코드 참고는 [agentLogin.ts](https://github.com/OrchestratorInc/agent-orchestrator/blob/4a2cf027d1724f754b5287e73cd4b491213347f9/packages/mobile/lib/cloud/agentLogin.ts), revision `4a2cf027d1724f754b5287e73cd4b491213347f9`다.
AO는 별도 서비스·이용 조건을 갖는다. native Dot의 클라우드 컴퓨터를 쓰려는 이번 목표에 먼저 추가할 이유는 없다.
ChatGPT 로그인 지원을 일반 웹 Pro 모델의 임의 세션 생성·제어 증거로 확대하지 않는다.

## 5. PC 종료와 실행 호스트의 수명

CoS의 후속 메시지·로컬 MCP·브라우저 복구는 실행 중인 CoS 앱과 로그인된 브라우저 호스트에 의존한다.
그 호스트를 끄면 저장된 상태는 남을 수 있어도 해당 프로세스가 일을 계속하지는 않는다.
이미 전송된 서버 턴의 지속과 다음 턴·도구를 실행하는 호스트의 지속은 별개다.
별도 원격 호스트나 Dot 컴퓨터에 브라우저를 두는 안은 추가 배치 후보이며 설치·로그인·수명·복구를 시험하지 않았다.
클라우드 작업을 사용하는 설계도 임의의 셸·브라우저 프로세스가 영구히 살아 있다는 보장은 아니다.
이번 자료에는 사용자 PC를 실제 끈 뒤 후속 작업까지 수행한 검증이 없다.

## 6. 이번 저장소에서 재사용할 연결 방식

1. GitHub 최신 branch/SHA와 `STATE.md`, 해당 과제의 handoff를 읽는다.
2. 웹 Pro에 조사·설계·검토 묶음을 맡기고, 반복 구현이 필요한 부분만 Codex Cloud에 보낸다.
3. Dot은 기존 작업자 ID·실제 진행 증거를 먼저 확인한다. 정상 진행 중인 작업을 반복해서 조종하지 않는다.
4. 완료 시 산출물·검사 SHA·receipt·미확인·다음 첫 행동을 저장한다.
5. 새 작업자는 이전 채팅 원문 없이 그 기록을 읽어 이어간다. Dot은 연결과 완료 조건만 확인한다.

기존 `HANDOFF_TEMPLATE.md`, `workbench.session`, `cloud_check.py`와 Actions 결과를 활용한다.
새 기억 DB나 거대한 오케스트레이터를 선행 구축하지 않는다.
초기 연결 시험은 웹 Pro 작업자 두 개의 실제 인계로 한정한다. Codex 작업만 성공했다면 웹 Pro 세션 교체까지 통과했다고 쓰지 않는다.
구체적인 준비·현재 연결 상태는 [DOT_AUTOMATION.md](../DOT_AUTOMATION.md)를 따른다.

**선택은 GitHub 상태 + 가벼운 Dot + 클라우드 작업자다. native 웹 Pro 생성·교체 연결, 사용자 PC 종료 후 이어가기, 장기 연속 가동은 아직 미검증이다.**
