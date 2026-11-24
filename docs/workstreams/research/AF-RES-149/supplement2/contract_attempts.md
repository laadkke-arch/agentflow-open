# 실제 계약 실행 재시도 — 실패와 독립 검산 구별

기준 f06a999fc72112bd7d8a9ae9e12c4d61cab6d175의 AGENTS.md blob 9dabe506eac7f7f013d68174062dd6eeb682fd7d L15–17,43: session check --fetch, python scripts/cloud_check.py --environment codex-cloud --fetch-contract, python scripts/check.py --require-git. docs/DOT_AUTOMATION.md blob 12ee268c493806c2fec83f261dc1ae08ecdee9c8 L71–80: 실제 checkout에서 소문자 manifest_id 준비. docs/RESEARCH_WORKFLOW.md blob e707baa2c8b366f960f9da0c4ea7c1ea60f62b00 L13,53,57: 검증·인계. 이 작업에 기존 manifest 실제 이름/내용 미확인; 아래 af-res-149는 명령 진입 시험용 ID, 계약 생성이나 변경 안 함.

- UTC 2026-11-24 16:31:45.657465–16:31:50.689100: git ls-remote https://github.com/laadkke-arch/agentflow-open.git ... exit128 DNS; TWIR curl exit6 HTTP000 total 4.767607s. 작업 branch 정확 checkout 미생성.
- UTC 16:36:36.945569822–16:36:38.709858478, cwd /, /mnt/data 비어 있음. 실제 명령 진입 시도:
  - git rev-parse --show-toplevel -> fatal: not a git repository (or any of the parent directories): .git; exit128.
  - python -m workbench.session check af-res-149 --fetch -> Error while finding module specification for 'workbench.session' (ModuleNotFoundError: No module named 'workbench'); exit1.
  - python scripts/cloud_check.py --environment codex-cloud --fetch-contract -> python: can't open file '//scripts/cloud_check.py': [Errno 2] No such file or directory; exit2.
- UTC 16:38:49.609532207–16:38:50.512420795: python scripts/check.py --require-git -> python: can't open file '//scripts/check.py': [Errno 2] No such file or directory; exit2.

공통 계약 CLI 본체 실행/판정 실패, 통과 미확인. 네트워크 DNS와 체크아웃 부재. 검사기를 약화하거나 가짜 manifest 생성하지 않음. 보조로 GitHub read/compare 및 독립 CSV/JSON 집합 검산 시행(SELF_CHECK 참고); 공통 계약과 동치 아님.
