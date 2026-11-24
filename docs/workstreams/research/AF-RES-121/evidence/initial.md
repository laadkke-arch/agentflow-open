# 초기 선택 판독

GitHub fetch_commit의 files[].patch에서 다음 hunk를 판독. 신규 direct commit metadata wrapper에서는 date 미노출(위 날짜는 117에서 상속). 최초 patch @@ -0,0 +1,N @@로 부모 대비 새 제안 파일임을 확인. 별도 부모 파일 전체 검색은 안 함.

- R1 https://github.com/rust-lang/rfcs/commit/2a26454c6b26c45c9b4b1f1ef1ddd8b51f0e39be — Summary, deprecations; +525 lines; 8e96f69에서 폐기 의무 삭제, future 가능성으로 이동
- R2 https://github.com/rust-lang/rfcs/commit/a41f7ebed2d63405fb002a662068914d0429351b — Summary, Mapping re-exports; +198 lines; earlier core::assert draft 자체는 미확인
- R3 https://github.com/rust-lang/rfcs/commit/7eafd50161dcf6d0038c25ce973b11d63db6889c — Summary/Motivation/Desugaring; +574 lines
- R4 https://github.com/rust-lang/rfcs/commit/b9bf6adfedd4f4a6282474029f03804694ebce35 — Summary/Reference-level +222 lines; GHC bullet 별도 재확인 예정
- P4 https://github.com/python/peps/commit/56cedcde02c874e3feb3172a28b0c49fff87111b — Specification/Type consistency/Rejected alternatives +224 lines
- R1 전환 https://github.com/rust-lang/rfcs/commit/8e96f69cadf0181bf07273ef96ddd952d8bb4d00: @@ -94,9 +94,6 @@ 폐기 문장 삭제, @@ -169,10 +166,6 @@ deprecations bullet 삭제, 뒤 unresolved question에서 future 가능성. 해당 이유·시각은 다음 묶음에서 직접 확인. 인용 전 변경이라는 선행 관측 유지.
- 일반 웹 6 commit URL 각각 DisabledError; GitHub connector로 동일 원문 복구. 접근 실패는 별도 경로 실패로 계산, 원저작은 중복 세지 않음.
