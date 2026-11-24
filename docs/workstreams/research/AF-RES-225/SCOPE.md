# AF-RES-225 — 범위 및 선판정

착수 통합 HEAD f3895893e32e2c055cefde446d34f1467fa27b4c; 계획 fc095c323d0177401d34f1daa7b4d1c529e2351f 대비 ahead 5/behind 0, dot-control.json만 변경. 계획판 tasks에 225 없음, 최신 RUNNING/depends_on 214/지정 branch·owned_path 일치. 두 blob 각각 50d8d51cbaf7d7a51234b097423cbf504c805717, 449f580659cac8affef11c502e23cbb25305152d (contents 응답 빈 문자열, blob 직접 읽어 해결). AGENTS/STATE/DOT/RESEARCH_WORKFLOW 읽음. 214 result_commit 81cb77570c6bb620316be4d1fb98d47276e5303c의 HANDOFF/RESULT/changes/decisions 읽음: 링크→동일인 선택 변경 완전 사슬 0/4, 지원 조건 변동. 216~218 및 dialog/Clippy/연구자 생성 패치/당사자 연락 제외.

## 동결
공개 GitHub 검색 repo:pandas-dev/pandas is:pr created:2024-03-01..2024-03-31 sort:created-asc. 최초 60 또는 기간 끝. 동시각 번호 오름차순. 파일 목록에서 pandas/tests/ 포함 최초 20(그 미만 전부), 그 밖은 제외/상한 명시. 파일 목록 판독 후 프레임 커밋 전 댓글 열지 않음. 각 적격 PR 공개 리뷰 전수; 첫 비작성자 동료의 기존 프로젝트 시험 helper 대체 권고만 PR당 1, 최대 6. 별도 보강 최대 3: 동일 저장소에서 지정 세 helper 명시 공개 inline 의견, 검색 기간/상한 명시; 원 모집과 합산 금지. 검색 순서가 불확실하면 순서와 결측 명시, 편의표본으로 대체하지 않음. 자동 lint, self-review, non-test, generic test request는 따로 분류. 작성자/커미터/merge는 분리.

## 선판정 (결말·의견 열기 전)
- 원 코드의 요구와 비교 차원을 우선 고정. 비슷한 helper가 존재해도 판 당시 가용성과 값/dtype/축/순서/NaN/허용오차 동등성은 별도. 직접 실행하지 않음.
- 존재(E) → 제시(R: 링크/이름/suggestion) → 동일인 후속 diff(A) → 명시적 사전 미인지(K) → 선택 인과(C). merge alone ≠ A, A alone ≠ K/C. 답글 alone ≠ 실제 diff. 수정된 댓글의 최초 내용은 복원 불가할 수 있음. 관측 0과 미확인 구별.
- 예측(가설): 리뷰에서 이름만 제안해도 이후 사용 가능; 팀 기존 관례와 같은 작성자 과거 사용이 '처음 발견'을 반증할 수 있다. 자동 제안 적용/타인 수정/부분 치환/거절/편집 시점은 경쟁 설명. PR base/head나 squash는 최초 parent→child 대체 불가.
- 다른 분야 eLife/JOSS 의견·답·수정판을 한 계보로 묶고 자기보고와 artifact를 구분.
- 목표 직접 자료 22=PR/review 6, 당시 소스/가이드/시험 5, patch/history 5, GitHub 규약 3, 학술 3. 목록/재표시/실패 불산입; 서로 다른 work_id와 계보 분리. 목표 사건 최대 6+3 별도, 프레임 60/적격 20. 하한/핵심 결손 PARTIAL. 순차 노출·자체 검토만 가능, 독립 검토 미실시.
- 실행/설치/자동 검사 제품 구현 금지. 필요 명령은 HANDOFF. 커밋은 owned_path만, control 변경 없음.
