# AF-RES-133 HANDOFF

**상태: PARTIAL.** 72개 PR 번호·시각·상태, 15개 사건, 15개 계약행, 108개 출처 기록(35 independent counted works)을 원격에 고정했고 Q1~Q7 및 세 표를 제출했다. 단, 모집창 전체 전 스레드 완독·정확한 제안 직전/직후 commit 및 당시 설치/릴리스 계약 검증을 완료하지 못했으므로 DONE으로 올리지 않는다. 적격 링크 전체 분모/실제 채택률 미확인. 중앙 상태를 직접 수정하지 않았다.

## 고정 입력과 산출물

- Repository laadkke-arch/agentflow-open; branch work/research-af-res-133; owned_path docs/workstreams/research/AF-RES-133/만.
- 계획 기준 42260ca230e028e1303667be943b861a1d5953e4, 실제 배정 통합 기준 67eb3c65404bf70de554bee6eb4c126344a3cd4a; 최신 통합 AGENTS/STATE/START_HERE/RESEARCH_BRIEF/RESEARCH_WORKFLOW/DOT_AUTOMATION 및 dot-control blob 9a1f05eb133617b6fa1aadbca0a7873cf10f06e0의 자기 행 읽음. 133 RUNNING, 의존 129 중앙 DONE/실제 인계 PARTIAL 구분.
- 고정 의존: AF-RES-129 [HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/86369e7091b3cb58bbea1e3277bee67967afeaa6/docs/workstreams/research/AF-RES-129/HANDOFF.md), [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/f288c8a0335be5d972c5782dccf021b5dd71e8af/docs/workstreams/research/AF-RES-129/RESULT.md) 및 관련 원장 구간 판독. 129 기존 두 라이브러리 재조사 안 함.
- 결과 SHA [957fffbe6991cef2c5b78f792bd5ea603b1139cd](https://github.com/laadkke-arch/agentflow-open/commit/957fffbe6991cef2c5b78f792bd5ea603b1139cd), [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/957fffbe6991cef2c5b78f792bd5ea603b1139cd/docs/workstreams/research/AF-RES-133/RESULT.md).
- 검사 입력 SHA 6bb60c2debc182aa6656948e2b337e67c4ae31a6, 원격 검사 영수증 SHA [d3f7f3fa70677cf21e3e8d78b86b724afac90eef](https://github.com/laadkke-arch/agentflow-open/blob/d3f7f3fa70677cf21e3e8d78b86b724afac90eef/docs/workstreams/research/AF-RES-133/evidence/remote-check.md). 정식 CLI check SHA/exit 미실시. base→검사 입력 비교 10 changed paths 모두 owned; 대표 파일 재열람 성공; 중앙 상태 불변.

| 묶음 | owned 경로 | commit SHA |
|---|---|---|
| 번호·규칙 사전 고정 | SCOPE.md | 63c4d26fddb91c16fae589ddb9ea9d6d2533721a |
| 본창 판독 | frame.csv (main 48 rows) | 39654dac3264a4fad7e90509a656d08da2096300 |
| 보충층 번호 고정 | evidence/supplement-frame-frozen.csv | df051a6cf23a20b21450fdad1de2590286d4cbc4 |
| 보충 판독 | evidence/supplement-frame.csv | 7ffda11bcc07e0440dc731caf113496b391f660c |
| 사건 근거 | events.jsonl | f2d16077506586ccc3e3a346ad4fbc3abce6fd6b |
| 계약·반례 | contracts.csv | 6a3a0df3ee5c92d11f4769f76973c1df686ac982 |
| frame 합본(층 유지) | frame.csv | 5accf7410f43b5533808e5794d89e9b638ec1f74 |
| hunk·타분야 대조 | evidence/hunks-and-corrections.md | 1034147b70e7afbc8337bd97dc8476d296759699 |
| 원전 원장 | sources.jsonl | 41719ec8fee95d42e8327755f014d71168cadc31 |
| 사건 불확실 anchor 제거 | events.jsonl | 891df53fe40e9c1486574c3d0583d9df364a785c |
| 필수 표 및 Q1~Q7 | RESULT.md | 957fffbe6991cef2c5b78f792bd5ea603b1139cd |
| 자기 검산 | SELF_CHECK.md | 6bb60c2debc182aa6656948e2b337e67c4ae31a6 |
| 원격 검사 영수증/재개 명령 | evidence/remote-check.md | d3f7f3fa70677cf21e3e8d78b86b724afac90eef |

각 묶음 대표 파일 remote fetch로 본문 일치 확인, RESULT 고정판에서 원장 재집계. 별도 세션 판독 없음. 이번 작업의 시간 해상도는 UTC 확인일 day precision; 발언 시각은 원전의 UTC 또는 미확인.

## 판단·색인 제안

- 추천 색인: `link_proposal_attribution` / `same_actor_same_operation` / `prior_fix` / `preserve_contract` / `document_not_execution` / `version_floor` / `editorial_correction`. 129의 후발 리뷰어 발견 기록과 작성자 최초 인지를 합치지 말 것.
- 관찰 15 사건에서 직접 확인한 linked runtime 변경 0, 모집창 비율은 산출 불가. S-N2 #7579 이름 제안은 동일 작성자 명시 응답+exact parent/diff/merge, 단 parallel 이미 선택, dependency 선언 변경만. X-N3 #9589 이름 제안 내부 parser 교체·set specialization 보고+merge hunk. X-N2 #9584 환경 해결 보고, exact hunk 미확인. S-L2-C #7589 doc-only 답과 최종 대체 링크, runtime 변경 귀속 아님.
- S-C1 #7576 sparse 문서 경고 후 다른 actor 보존 변경, default matrix+array opt-in, @ 및 test hunk. S-L3 #7575의 #7699는 링크보다 먼저 생성, 다른 actor. S-L4 clip=False의 기능 존재에도 최종 normalization/default clip 유지, reviewer dark output 보고. Link 대상의 존재·호환·채택·배포·인지 각 독립.
- ONS C1 동일 series 480→479 현재값(즉시 정정판 미확인), C2 코드 R68.8→R68 값 유지, 이름 명시 HMRC C3/C4와 전후표 귀속 별개. 편집자의 수정에 제보자 전부 공로를 부여하지 않음.
- 링크 한 절을 초기 설계 후보로 반환하는 것과 이미 유지 중인 코드를 치환하는 것은 다른 계약. 유지보수자는 구판·반환형·경계 입력·fallback/opt-in 함께 확인. 부족하면 확인 질문/보류. 달력 경과와 작성자 노동시간 분리; 후자는 확인 0건/15(미확인이지 0분 아님).

## 막힌 이유와 첫 재개 행동

웹 연결로 GitHub 읽기/커밋은 가능했으나 로컬 git ls-remote는 DNS 실패(exit 128, Could not resolve host: github.com); checkout manifest 생성·검사 및 시기별 실행 미실시. 통합 PR 응답 및 일부 review thread의 DB id/줄은 얻었으나 pagination, original_commit_id, 최초 후속 SHA, 전체 edited history 미확정. #9618 등 장문 일부만 판독했다. 원본 소실을 단정하지 않는다. 정확한 최초 chain 1/15뿐(비링크). source 최소량을 충족해도 전체 관측 완결 기준은 미충족.

첫 행동: **인증된 checkout에서 이 브랜치를 fetch하여 기존 커밋 유지, manifest 유무 및 실제 base/의존부터 대조.** 없을 때만 아래 start; 중앙 브랜치/상태 변경 금지.
```sh
python -B -m workbench.session start af-res-133 --allow docs/workstreams/research/AF-RES-133/ --dependency work/research-af-res-129=86369e7091b3cb58bbea1e3277bee67967afeaa6 --output docs/workstreams/research/AF-RES-133/manifest.json --fetch
```
다음으로 frame.csv 본창 48 번호 우선 각 issue/comments, pulls/reviews, pulls/comments, pulls/commits 전 페이지 및 GraphQL history/replies 확인. #9580, #9588, #7575/#7589, #7576 원래 SHA부터 채우고 장문 #9618 보충 완독; 본창 링크 수 <2 보충 조건 재판정. 예:
```sh
repo=pydata/xarray; pr=9618
gh api --paginate "repos/$repo/issues/$pr/comments?per_page=100"
gh api --paginate "repos/$repo/pulls/$pr/reviews?per_page=100"
gh api --paginate "repos/$repo/pulls/$pr/comments?per_page=100"
gh api --paginate "repos/$repo/pulls/$pr/commits?per_page=100"
```
인라인 original_commit_id 및 diff_hunk, commit 부모/다음 hunk, release tag, versioned consumer/supplier tests/CI를 잇고 source ledger·세 표를 수정. Q7 C1 즉시 대체판·C3/C4 same-cell 원표 우선. 전수 완료 뒤 별도 세션 검산 및 다음 정식 명령 실제 실행, stdout/stderr/exit와 대상 SHA 보존:
```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-133/manifest.json --fetch
```
현재 위 start/check 및 boundary runtime 실험은 미실시. 파일은 모두 remote commit으로 남기며 이 HANDOFF가 이번 작업 마지막 별도 commit이다.

| 중요한 불일치·약점 | 다음 조사·원문 또는 실험 | 판단을 바꿀 관측 |
|---|---|---|
| 모집 72개는 고정됐지만 전수 완독·보충 조건·엄격 링크 분모 미확인 | 고정 번호 REST/GraphQL pagination 전수 및 #9618 장문, 본창 threshold 재검산 | 이전에 누락된 적격 링크와 직접 author acknowledgment |
| first hunk·original_commit_id·당시 판/실행·배포 미완 | 각 심층 좌석 exact commit chain, 당시 최소판/경계 입력 재현 및 release tag | 동일 actor 동일 조작의 링크 후 변경과 version contract 동시 확인 |
| 수정 선행/다른 actor·ONS 공지 vs 수정판·노동 비용 미확인 | #7699 시각, C1 즉시 대체판·C3/C4 same-cell, 실제 노동 보고/대조 실험 | 선후 뒤집힘, 명시 제보자와 실제 수정 셀 연결, 실측 비용 확인 |
