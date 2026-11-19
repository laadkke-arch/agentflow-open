# B — Data contract 작업 현황

상태: READY_NOT_STARTED. 작성: 2026-11-19.
- 이슈: https://github.com/laadkke-arch/agentflow-open/issues/3
- 브랜치: `work/data-model`
- 수정 범위: `docs/workstreams/data/`만
- PR 대상: `chore/workspace-foundation`
- 기준문서: `docs/product/DATA_MODEL_DRAFT.md`, `docs/product/ROADMAP.md`

목표: 5개 테이블의 PK/FK·1:N·JOIN·CRUD, 중복 자원/URL, 출처·가격·라이선스 unknown, 관리 권한, 삭제 참조 정책을 검증 가능한 계약으로 구체화.

최초 행동: 5테이블 설계 tradeoff와 정규화 확인 → 독립 SQL/테스트 예제(가능하면 자기 폴더 내 실행) → 실제 실행 환경/결과/DB별 차이 기록. SQLite 통과를 TiDB 통과로 오인하지 않는다.

필요한 결과: 자기 폴더의 제안·테스트 자료, `STATUS.md`, `HANDOFF.md`, 실제 커밋/PR. 유료 DB·토큰·Render를 승인 없이 만들지 않는다.
