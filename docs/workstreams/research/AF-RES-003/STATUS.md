# AF-RES-003 작업 상태

## 계약과 범위

- 작업: AF-RES-003 / 시도 1 / identity + storage 연구.
- 시작 통합 커밋: `9d728dfe2c2f3a13d9995b5fdc14a252aeddfdad`.
- 브랜치: `work/research-af-res-003` (없음을 원격에서 확인한 뒤 위 SHA에서 생성).
- 허용 경로: `docs/workstreams/research/AF-RES-003/`.
- `dot-control.json`의 `depends_on`: 빈 배열. 다른 연구 결과를 전제하지 않는다.
- 작업 배정은 현재 사용자 지시와 위 SHA의 AF-RES-003 항목으로 확인했다. STATE/브리프의 과거 “미배정” 문구는 저장 당시 상태이며 이번 지시를 취소하지 않는다.
- 실제 실행 환경: 이 ChatGPT 대화의 클라우드 작업공간. 사용자 PC, 사용자 Codex Cloud 환경 연결, native Dot 작업자 생성 성공을 주장하지 않는다.
- 확인 시각: 2026-11-19 15:40 UTC / 한국 2026-11-20 00:40.

## 직접 읽은 저장소 입력

위 고정 SHA의 `AGENTS.md`, `STATE.md`, `docs/DOT_AUTOMATION.md`, `docs/RESEARCH_WORKFLOW.md`, `docs/automation/dot-control.json`의 해당 항목, `docs/product/RESEARCH_BRIEF.md`, `docs/research/INDEX.md`를 GitHub에서 읽었다. 추가로 `docs/START_HERE.md`, `docs/product/{README,RESEARCH_PROTOCOL,ROADMAP}.md`, `docs/CLOUD_WORKFLOW.md`, `docs/collaboration/{README,HANDOFF_TEMPLATE}.md`, 기존 `docs/research/discovery-case-2026-11-19.json`과 계약 실행 코드 `workbench/session.py`를 읽었다. 기존 조사 표본은 분류·미확인의 사례이며 이번 연구의 외부 원문 열람 수에 포함하지 않는다.

## 조사 묶음과 완료 기준

1. 제품·repo·docs·서비스, fork·rename: 별도 하위 조사. `SOURCES-IDENTITY.md`.
2. 독립 기능과 유사 메커니즘의 경계: 별도 하위 조사. `SOURCES-MECHANISMS.md`.
3. 식별·출처 표준과 서지/연구자료 분야의 반례: 본 작성자. `SOURCES-STANDARDS.md`.
4. 동일 사례에 링크+설명 / 대상+링크 / 주장+근거 저장원리를 적용하고 최소 표현, 병합·분리·대체 보존, 확장·중단 조건을 정리. `RESEARCH.md`와 재현용 사례.
5. 별도 검토자에게 원문과 주요 결론 대조를 요청하고 이견·수정을 보존. 이후 범위·링크·출처 연결과 계약 확인, 마지막 `HANDOFF.md` 커밋.

완료 기준은 외부 원문 20개 이상 직접 열람(검색 결과·차단 페이지·저장소 관리문서 제외), 자료별 URL/시점/위치/관측/한계, 같은 사례의 세 저장대안 비교, 오병합과 과분할 반례, 필드별 방지 오류, 미확인과 다음 최소 확인이다. 저장 스택·테이블 수·최종 API·검색순위·크롤러·갱신주기는 정하지 않는다.

## 현재 진행

**REVIEW_READY — 조사·수작업 대조·별도 검토 완료, 통합 검토 대기.** 원문 33개와 동일 사례 9개의 비교를 보존했다. 연구/검토 커밋 `caf806738b0ed07fe5bce8d4c5c173bada5286b3`의 개별 계약 검사와 문서 감사는 통과했다. 이 상태 문서와 최종 인계의 후속 커밋을 앞선 검사에 포함시키지 않는다.

- 읽을 순서: [최종 인계](HANDOFF.md) → [연구 본문](RESEARCH.md) → 필요한 [사례](CASES.md)·[별도 검토](REVIEW.md)·원장.
- 검증 명령·입력 SHA·종료 코드: [VALIDATION.json](VALIDATION.json).
- 통합 대상 초안 PR: [#5](https://github.com/laadkke-arch/agentflow-open/pull/5), `chore/workspace-foundation` 대상.
- 저장 구조의 최종 채택, 작성 비용·오병합률 실측, 제품 조합 실행은 이번 결과가 확정하지 않는다. 다음 첫 행동과 색인 변경 제안은 HANDOFF에 있다.
