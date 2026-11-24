# GitHub 묶음 재열람

작업 브랜치를 GitHub에서 `git fetch origin work/research-af-res-155`로 다시 읽고 `git rev-parse FETCH_HEAD` 및 `git show FETCH_HEAD:docs/workstreams/research/AF-RES-155/<파일> | sha256sum`을 로컬 해시와 비교했다. 마지막 인계의 원격 확인값은 인계 커밋 다음 외부 응답에서 보고한다.

| 묶음 | 원격 SHA | 대표 파일 | 동일한 SHA-256 | 확인 UTC |
|---|---|---|---|---|
| ① | 932cf329952886bec4fe20a33b248709915a9ca2 | SCOPE.md | 1f31cffac8e799fe7c3febd8a1aa9516cd30fc215461ca2448a6ceac72881a15 | 2026-11-24T15:51:01Z |
| ② 기준 입력·예측 | dee0da5de6ba1f93d60177d5a9b11f72b8b81557 | predictions.csv | bfda567a88c3cd50b29eaf05da6b02db84bba31e3d9288590747bc89f613b1d9 | 2026-11-24T15:55:34Z |
| ② 실행기 | 9f1c49d76cf75589839cf372d6f32bfe4470ab37 | replay/run.py | 75f6626c0541b07ef3d7b65a96892f0053829b390c6734fd56989eb84110d2d0 | 2026-11-24T15:57:35Z |
