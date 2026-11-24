# AF-RES-141 HANDOFF — PARTIAL

- status: PARTIAL. 연구 산출물은 커밋되어 있다. 중앙 dot-control 상태는 수정하지 않았다. 전체 모집/편집/최초 배포 확인의 미완을 완료로 보고하지 않는다.
- branch: work/research-af-res-141
- owned_path: docs/workstreams/research/AF-RES-141/
- plan base: d950356cdfae3edf799870cdeb90b93b5bd4ffd3; actual integrated base: c088f5af075c3b010102d002e66c84d9263fe5de. 통합 계약을 먼저 읽고 최신 브랜치에서 분기했다.
- sole dependency: AF-RES-137 central DONE, fixed HANDOFF PARTIAL. [fixed HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/48475acf84dd9e9e49c6fc24958ad50b7aee1440/docs/workstreams/research/AF-RES-137/HANDOFF.md), [fixed RESULT](https://github.com/laadkke-arch/agentflow-open/blob/ae8b00dad97ba242d7f274a539964cc66c1f1070/docs/workstreams/research/AF-RES-137/RESULT.md). events/coverage fixed handoff SHA에서 읽었으나 coverage의 모든 원문 행을 별도 재판독하지 않았다. 137 X18-type, X9-parser, S6-pixel 비교 라벨만 재사용했다.
- verdict: 출전 전체는 탐색용으로 연결하되 추천 이유·실행 경로·누락 조건은 조작 단위로 제한해야 한다. 출전 참고 R, 차용 자인 A, 실행 경로 D, 최초 인지 K, 사람 노동 L은 독립이다. Matplotlib #24976은 직접 URL을 받기 전에 이미 외부 스텁을 알고 있었고 zorder float를 유지했다. Pillow #6897은 test harness를 차용했으나 병합된 readline 변경이 #6879에서 철회되고 binary/ASCII 조건을 나눈 새 parser가 배포 소스에 남았다. #6850은 출전 문서를 복사했으나 runtime patch #6842는 선행한다. #6926 내부 wrapper 복사 자인은 branch 수준이며 open PR. 무링크 #24891 redirect/title도 배포 소스에서 확인. 양성 추가 비교 #26278은 두 예제의 부분 조합, #26908은 issue repro→회귀 test의 정확한 일부 차용. 원문 전체 차용과 노동 절감은 주장하지 않는다.
- index 제안 한 줄: `AF-RES-141 | PARTIAL | 소비자 2종/8 PR·11 조작 provisional; 52/64 슬롯, 33 독립 저작; 원전 링크·부분 차용·선행인지·release branch·노동 분리, 전체 모집 판독 미완 | RESULT.md`.

## 산출물과 커밋 (고정 SHA에서 GitHub 다시 열어 content 일치 확인)

| 묶음 | commit SHA | 대표 경로 | 확인 |
|---|---|---|---|
| ① scope | 88b4523c8828cdfe4f34ae197ab2a7519c19712d | SCOPE.md | blob 0ed8caec30be1a35ce06011fcc4e5b77a455629f, match |
| ② 모집 동결 | af05fe6b52e53a3b9503eef357d1ff9de3c86c0b | frame.csv | blob f78a18adc99436ff849812b30e3740071f08581f, match |
| ③ 사건 | 500de286dbd0ab6c60ada73365483260b92471ac | events.jsonl | blob c23a7bbbaa98d3e629d8e0e8989fa7990be37d73, match |
| ④ 대응·반증 | 1d9129df6118eb438596f7eeddad3dff3a7f9720 | transfer.csv | blob 54a4ffb836a43ee1e0152634c6ae367f3c5c1d9c, match |
| ⑤ 원장 | 17c280d9781182c28487a4d50c70a7b8c06f21b7 | sources.jsonl | blob fee73c0412a218f214edfc20e44e61b24e776229, match |
| ⑤ 후속 원전 | f61926ac63f61e0fb103088701c91000ecaa6536 | sources.jsonl | blob ebe2ae652446e8f51ac5c68b08215ea423aaf127, match |
| ⑤ coverage | e5fb47f6c03428fbbeae379b164d4fc392849173 | frame.csv | blob 1c11a546dd968802e2781ff2ce84bb2ec8571dd8, match |
| ⑤ 결과 | 764e89364f0491d6f27f12347b5bf1b2b4af98e4 | RESULT.md | blob d0d16d0f97703ae0062ef6700ad3d47337379ca0, match |
| ⑤ 후검산 | fb9a16378b7a505292f0b668526c7d84b549495d | events.jsonl | blob 6f21d1cc5b60605df3c6f82821461976282ab4de, match |
| ⑤ 후검산 | 5795d00de1c3156c329d99cc3f1618c28f7fb466 | transfer.csv | blob f30fbe25474233df0383300fef5a2e5d1b2e78f8, match |
| ⑤ 자기검산 | d411a06fa49c6025a7b2375c92dd73e8f73797c3 | SELF_CHECK.md | blob 4ad08b161462e009ba0c7d6bb80cc0594d2b1879, match |

인계 전 [compare](https://api.github.com/repos/laadkke-arch/agentflow-open/compare/c088f5af075c3b010102d002e66c84d9263fe5de...d411a06fa49c6025a7b2375c92dd73e8f73797c3)를 직접 열어 ahead 11 / behind 0, changed paths 7 모두 owned_path 아래임을 확인했다. HANDOFF 자체는 다음 별도 마지막 커밋이므로 자기 SHA를 본문에 미리 쓸 수 없다; 커밋 후 fixed SHA 재조회 및 compare를 외부 실행 결과로 확인한다. 별도의 merge/deploy/central update 없음.

## 수치와 실제 검사 범위

- 64 고정 슬롯: M 20 neutral + 8 purpose actual /4 empty; P 20 neutral +4 purpose actual /8 empty. 52 unique PR, 45 merged, 6 closed unmerged, 1 open. 0 overlap. 검색 창의 관측치만이며 적격/채택 분모가 아니다.
- 19 PR body 또는 conversation/diff 직접 회수, 12 page1 세 conversation surfaces retrieval, 7 partial, 33 index-only. 8 provisional deep PRs(4+4), 11 unique operation IDs, transfer 18 correspondence rows. 앞 슬롯의 모든 적격 여부가 미확정이므로 심층 순서가 변경될 수 있다.
- 132 source rows, 33 counted unique work_id = PR 15 + provider 8 + consumer regression/corrective/test/release 6 + cross-domain 4. Category floor 8/6/6/4 충족. 同一 PR/diff/release 중복 산입하지 않음; #24857/8 backport 제외, #26908 regression bucket만. 원장 날짜 granularity UTC, exact minute 미기록.
- 원격 same-reader: sources, events, transfer, frame을 다시 읽어 JS 재집계; source ID 중복0, event source IDs 결측0(stage5c; 후검산 참조는 추가 원장에 존재). fixed commit representative 11 checks. 실제 독립 판독, Python 실행/회귀 테스트, build, wheel, 음원 실행 없음. PDF 원작/편곡 p1 visual comparison 수행. 동일 글리프 2 master raw coordinate 확인했으나 렌더된 specimen과 exact base는 미확인.
- API GitHub search GET에서 p10 반환 한계, complete global tail 미확인. 64-call batch attempted, code-mode tool cap exceeded; 성공으로 세지 않았다. 일부 대화 결과 길이 truncation과 raw pagination header 미회수. Historical Divio/Chromium source/first hunk/first deployment/exact edit timeline 미회수. Container checkout 및 GitHub DNS 실패로 `workbench.session start/check --fetch` 실행하지 못했다. 원격 compare와 fixed blob read가 대체 확인이지만 동일한 검사는 아니다.
- 중단 이유: 자료/전체 리스트 미회수 및 최초 배포/원전 일부 미완. PASS/완료로 승격 금지. R/A/D/K/L의 미확인 칸을 0으로 채우지 않았다.

## 다음 첫 행동 (정확한 입력)

1. 동일 branch를 checkout할 수 있는 Codex/worker에서 현재 마지막 커밋을 fetch한다. 기존 stage 보존, 이후 correction 별도 필드/commit으로만 작성한다. 원격 확인은 아래 명령으로 재현 가능하다. 아래 명령은 이 세션에서 실행되지 않았다.
```sh
git clone https://github.com/laadkke-arch/agentflow-open.git
cd agentflow-open
git fetch origin chore/workspace-foundation work/research-af-res-141 work/research-af-res-137
git switch --track origin/work/research-af-res-141
git diff --name-only c088f5af075c3b010102d002e66c84d9263fe5de...HEAD
git show 48475acf84dd9e9e49c6fc24958ad50b7aee1440:docs/workstreams/research/AF-RES-137/HANDOFF.md
python -m workbench.session start af-res-141 --allow docs/workstreams/research/AF-RES-141/ --output docs/workstreams/research/AF-RES-141/session.json --dependency work/research-af-res-137=48475acf84dd9e9e49c6fc24958ad50b7aee1440 --fetch
python -m workbench.session check docs/workstreams/research/AF-RES-141/session.json --fetch
```
기존 branch가 이미 있으면 switch만 하고 overwrite하지 않는다. manifest base가 새 통합 SHA와 불일치하면 명령 출력 그대로 기록하고 통합 담당에게 조정 요청; 임의 rebase/merge 금지. manifest를 owned_path 안에 두는 이유는 사용자 경로 제한이다.

2. 첫 판독: frame.csv의 첫 index-only M #24863 (그다음 #24864…), P #6853부터 순차로. gh CLI가 연결된 곳에서 원문+response Link header를 회수하고 page n이 empty인지와 실제 next link를 기록한다.
```sh
gh api --include 'repos/matplotlib/matplotlib/pulls/24863'
gh api --paginate --include 'repos/matplotlib/matplotlib/issues/24863/comments?per_page=100'
gh api --paginate --include 'repos/matplotlib/matplotlib/pulls/24863/reviews?per_page=100'
gh api --paginate --include 'repos/matplotlib/matplotlib/pulls/24863/comments?per_page=100'
gh api --include 'repos/python-pillow/Pillow/pulls/6853'
gh api --paginate --include 'repos/python-pillow/Pillow/issues/6853/comments?per_page=100'
gh api --paginate --include 'repos/python-pillow/Pillow/pulls/6853/reviews?per_page=100'
gh api --paginate --include 'repos/python-pillow/Pillow/pulls/6853/comments?per_page=100'
gh api --method GET --include search/issues -f q='repo:matplotlib/matplotlib is:pr created:2024-12-01..2024-12-31' -f sort=created -f order=asc -F per_page=100 -F page=1
gh api --method GET --include search/issues -f q='repo:python-pillow/Pillow is:pr created:2024-12-01..2024-12-31' -f sort=created -f order=asc -F per_page=100 -F page=1
```
월별 partition은 전체 검색 API cap의 보조 검산이다. 전체 2023-01~2024-12 각 월도 같은 방식으로 확인, 월별 1,000 초과 시 일자로 재분할하고 최초 20 prefix 유지/대조. 목적층 3 어구는 original queries 그대로 유지, 새 검색어 추가 금지. `frame.csv`의 depth_observed와 adjudication_observed에 따라 남은 33 + 7 부분+12 page1 list ends 재검토. 24976 33 issue comments/58 inline의 긴 body를 paginate하여 원문 편집시각, 최초 공개·응답·변경을 구별. #6926 current open/release chain, Chromium fixed revision, #24891 historical Divio archive, #24861 original commit/rebase chronology, #7580 first merged test predicate, wheel release. #25386 #26702 #24987 #25018 목적 후보 회수. 최초 적격 슬롯이 달라지면 기존 선발 행 삭제 대신 postcheck 새 판정 추가.

3. 실행 가능할 때 별도 local checkout에서 해당 고정 태그를 fetch하여 제안 전/후 patch 비교 후 실제 테스트 명령: Matplotlib v3.8.1 `python -m pytest lib/matplotlib/tests/test_contour.py -k 'allsegs_allkinds or contour_clip_path'`; Pillow 9.5.0 `python -m pytest Tests/test_file_eps.py -k 'ascii_comment_too_long or long_binary_data or timeout'`; Pillow 9.4.0 `python -m pytest Tests/test_image.py -k empty_image`. 패키지/빌드 준비가 없으면 실행 불가 이유 남김, 설치 권한 없으면 임의 설치 금지. 제공된 test fixture만 사용. 실행 시 tag/commit, environment, result, actual elapsed와 CPU time, test output 기록. 노동과 별개. 독립 재판독자는 원고를 보지 않고 R/A/D/K/L 및 연결을 새로 코딩하도록 한다. 서체 U+006C same master normalized specimen 및 실제 score base edition도 재확인.

| 가장 중요한 불일치·약점 | 현재 판정에 미치는 영향 | 다음 조사·찾을 자료 | 판정을 바꿀 관측 |
|---|---|---|---|
| 52 PR 전체 dialogue/편집/last page 미완, API cap | 최초 적격 순서·전체 링크/무링크 분모·비율 미확정 | 남은 33+7 및 12 page1 끝 재판독, 월/일 partition, header 기록 | 더 이른 적격·중복·반려 사건이 발견되면 선발과 분모 재판정 |
| 당시 Divio/Chromium 공급자, rebase 뒤 첫 hunk 및 실제 first release/wheel 미회수 | reference/partial adoption 범위만 주장; whole runtime causation 불가 | #24891 archive, #24861 original hunk, #6926 fixed source/release, #7580 first test diff | 직접 신규 인지·정확한 원전 분기·실제 release 보존 또는 선행 구현 |
| 원전 하한 충족과 독립 판독/실험/사람 노동은 별개; exact glyph specimen·악보 원판 미확인 | 인과·전체 기능·노동 절약 강한 문구 불가 | blinded reader, replay, 노동 기록, normalized glyph/arranger exact base edition | 독립 기록이 링크 후 최초 인지/실제 작업시간을 입증하거나 기존 조작 대응을 반증 |
