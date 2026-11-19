# 독립 세션의 결과 검토 및 안전한 통합

작성: 2026-11-19. `main` 대신 `chore/workspace-foundation`을 **제품 문서·공통 작업환경의 통합 브랜치**로 유지한다.

## 세션별 독립 영역
- A `work/discovery` → `docs/workstreams/discovery/` → [#2](https://github.com/laadkke-arch/agentflow-open/issues/2)
- B `work/data-model` → `docs/workstreams/data/` → [#3](https://github.com/laadkke-arch/agentflow-open/issues/3)
- C `work/experience` → `docs/workstreams/experience/` → [#4](https://github.com/laadkke-arch/agentflow-open/issues/4)
- 공통 제품·시작·협업 문서 및 루트 `STATE.md`는 통합 담당만 수정한다.

## 각 세션이 PR을 준비할 때
0. 최신 통합 계약과 의존 SHA를 다시 확인한다. 클라우드 checkout에서는 `python -m workbench.session check docs/tasks/과제.json --fetch`를 실행한다. 계약이 달라졌다면 영향 분석 후 새 핀으로 작업한다. 과제 manifest가 없는 경우 이 검사는 미실시로 기록한다.
1. 이슈 요구와 실제 변경 파일을 대조한다. 담당 폴더 이외에 편집했다면 근거와 함께 수정 범위를 좁힌다.
2. 조사 결과의 실재 URL/확인일, D0–D4 증거 수준, 미확인 항목, 선택/제외 이유를 확인한다.
3. 테스트를 했다면 **명령·실행 환경·종료 코드·검사한 SHA/데이터**를 제공한다. 코드를 안 돌렸으면 '검사 미실시'라고 한다.
4. 민감 정보·비공개 파일·저작권 위반 복제 여부 확인.
5. `STATUS.md`·`HANDOFF.md`를 최신화하고 자기 브랜치 → `chore/workspace-foundation`으로 PR을 연다.

## 통합 담당
1. 세 PR의 현재 head/변경 파일/근거를 읽는다. 오래된 대화의 완료 주장을 대신하지 않는다.
2. A 후보 데이터와 B 필드, C 화면·추천 계약 사이의 충돌(유형/URL 정규화/기능/증거/unknown)을 찾는다.
3. 독립 폴더의 안전한 변경부터 검토·통합한 뒤 공통 제품문서에서 승인된 결론만 업데이트한다.
4. 자동 병합이나 `main` 배포 없이 PR/커밋·상태 보드를 갱신한다.
5. 코드 수정이면 실제 실행/검증 기록을 남긴다. 문서 추가만으로 코드·DB·배포가 통과했다고 하지 않는다.

## 주의
- 브랜치 세 개만으로 ChatGPT 세션을 자동 실행·동기화하는 기능은 없다.
- `workbench.yml`은 코드·실습·검사 변경을 Ubuntu/Windows에서 검사한다. 제품·협업·workstreams·tasks 문서는 별도 `session-check.yml`에서 검사한다. 활성 manifest가 0개인 실행은 협업 통과가 아니라 미실시다.
- CI 결제/한도 오류를 성공으로 처리하지 않는다. 로컬 실행 결과와 GitHub hosted Windows/Linux 실행 결과를 구분한다.
- 공개 저장소에서 API 키·고객 데이터·대화 원문·비공개 사업 기획을 유출하지 않는다.
