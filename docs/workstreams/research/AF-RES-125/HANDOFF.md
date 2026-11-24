# AF-RES-125 HANDOFF

- **status: PARTIAL**
- 사유: 지정된 제목 모집창의 48개 후보를 판독했으나 NumPy/SciPy의 이름 있는 연산으로 자체 계산을 제거한 본 사례 관찰 0, 본 자리 6 공석. 일부 병합 patch 발췌·최초 공급 구현/배포 및 소비자 도입 이력·개별 객체 전환·정식 세션 검사 미완. 이 결과를 직접 발견 귀속 실패율 0% 또는 성공률 0%로 해석하면 안 된다(본 분모 0).
- 시작 통합 SHA: `5c0eca97d41e084a76bddd7cb0e976e5e9f792e8`; 계획 기준 `4a92e22c5356dc7ea2b715f671077e8ab63b2835`. 배정행 RUNNING, 소유경로/branch/의존 일치 확인. 통합 문서 AGENTS.md, STATE.md, START_HERE.md, product/RESEARCH_BRIEF.md, RESEARCH_WORKFLOW.md, DOT_AUTOMATION.md 및 control blob `71a6140048f6d33851acd56356ca726ebbca0c94` 확인. dot-control.json 변경 없음.
- dependency AF-RES-121: HANDOFF `fe74c5eec9b3f2dd833409d59460c0b82f4cfe79`, RESULT 및 claims.csv/versions.csv `97e69009bd64d56a96d12ed5d7e6614e395f0fce` 읽음. 121 사건 재조사하지 않음.
- 결과 본문 커밋: `fbbc6bdf0b818233e5c93c46f762b0d15ba5afe0`; 원장·자기검산까지 포함한 고정 결과 SHA: `475723b218349b4a724b61beba8bc92e9ecce3e3`.
- 원격 검사 기록 SHA: `e72f7fd512c33cc9c802c4b86592a33d67ef51e5` [evidence/remote-check.json](https://github.com/laadkke-arch/agentflow-open/blob/e72f7fd512c33cc9c802c4b86592a33d67ef51e5/docs/workstreams/research/AF-RES-125/evidence/remote-check.json), 2026-11-24T09:09:14.773Z, 본 작업자 GitHub 고정 SHA 재조회 및 JS 집계. 96 frame행(89 window/7 boundary), 88 unique(47/41), 48 changes행(각24), 본0/대조2, sources 67행·58 고유 저작(4 excerpt 제외 54), decisions 9행; missing decision/change/supplier ID 0, 후보 연결 및 순위 오류 0, 소유경로 밖 변경 0(시작→고정 결과 26 files). 최종 3행 표 확인. 정식 세션 검사와 별개.
- 중간 원격 재열람 기록 SHA `7af3585c12e384ec5186baf12e0632d010d876ad`, evidence/intermediate-readback.json, 17개 original commit 대표 파일 재조회 성공. 초기 scope/frame 및 고정 결과 대표 파일도 원격 재조회함.
- 독립 저작 세부: PR 41, 소비자 독립 4, 공급 6, 측지 3, 도서관 4. backport/동일 distance.py 계보 통합. 일부 발췌와 exact boundary test 관련성 제한은 RESULT/원장에 표시. 실패 NCAT API timeout 1, 대체 NCAT 원문. 사용자 실제 실행/노동시간 입증 0건(실제 시간이 0이라는 뜻 아님).

## 묶음별 커밋
| 묶음 | 고정 SHA(들)·파일 |
|---|---|
| ① 모집·기준 | b9d6b37087fdfd634d5fb550aa935951179d3fc3 SCOPE.md, 후보 본문 이전 |
| ② 검색·경계·선택 | d2f6e327130fce6fd12119047d56dea70a738f6e, 8b9257138a248ce1108e3142c98c5a970a74eb39, 017af731665d43858b52b3747981934e63df6b68, 7705c54663006419b85b8585ae4b518c6516e980, 78041944aa9f9f23bd0a02541125984ddaac83dc, 7117985a1dfe087fc05bf488f079013ad7f66de1, 5b4810eaf8a575e7419d7c44c119b1360a382e1c (metadata); e2e12a010be5d77196b623157ac822af5cfed53c frame.csv; 76b5e897c6e4d7964d5b3935ee6378c982ef3e36, 4104be717257c92eac62ca19319aeaf28299fade, 620d18f1b57a1316f60a743459758bf78e1faa25, c75253b38d17abe90a8cf024b1ff8f37de486b0b (patch); 02e9ecfd1fdc1f3302165418c9a9cffaa8fcadfb, d10a4135a7d07695464b4f499b7152c092ccc9b8, b201f85b71659627e870ab4e79c516b91449376d, 92a088c1162e5d5a5e6dab119fccd0f981215b81 (parent compare); 5bbf5ef36a8f9682392008a4f8fe779ee95e36e7 changes.csv |
| ③ 버전·지원 요건 | 8b85e5452d084f6b59b683b3fee900c78df4845b evidence/version-read.json |
| ④ 발언·반례·타 분야 | e9e5a6fceada070fa4a5c3caff58eb23698796bc evidence/pr-discussions.json; 0262e9400ea128e221480b11c8371d1ceeb8d16d evidence/pr-sources.jsonl; 0414990e786a9e5f09cbeb004069546ebb082842 sources.jsonl; d11a4c1a9dfb9075bee314c9a0941211a9dfa56d counts-precheck; 7fe1d3645da158e09e27ea32fa48ac8e628408a5 decisions.jsonl |
| ⑤ 결과·자기검산 | fbbc6bdf0b818233e5c93c46f762b0d15ba5afe0 RESULT.md; 475723b218349b4a724b61beba8bc92e9ecce3e3 SELF_CHECK.md; e72f7fd512c33cc9c802c4b86592a33d67ef51e5 remote-check; 7af3585c12e384ec5186baf12e0632d010d876ad intermediate-readback |
| ⑥ 최종 | 이 HANDOFF.md 단독 커밋; self-referential SHA는 본문에 기록하지 않음 |

자료 접근 효율 때문에 일부 발언 수집이 부모 SHA 검산 전, selection 최종 CSV가 version-read 후 커밋됨. 묶음의 논리 순서와 실제 커밋 interleave를 숨기지 않는다. 시작 범위 고정은 검색 이전이다.

## 다음 실행·검사
원격 GitHub 연동은 읽기/쓰기 가능했으나 checkout 런타임의 git ls-remote 및 curl API DNS 해석 실패로 로컬 복제와 workbench CLI 미실행. 공식 manifest.json 없음(수동 위조하지 않음); formal check status NOT RUN. checkout 가능한 승인 환경에서 통합 시작판과 기존 작업 브랜치/의존 SHA를 먼저 fetch하고 작업판의 원래 시작 SHA가 보존되도록 workbench.session start의 기존 브랜치 처리 규칙을 확인한 뒤 아래 실행한다(기존 결과 삭제/강제 reset 금지). 실제 경로는 repo root.
```sh
git fetch origin chore/workspace-foundation work/research-af-res-125 work/research-af-res-121
git switch work/research-af-res-125
python -B -m workbench.session start af-res-125 --allow docs/workstreams/research/AF-RES-125/ --dependency work/research-af-res-121=fe74c5eec9b3f2dd833409d59460c0b82f4cfe79 --output docs/workstreams/research/AF-RES-125/manifest.json --fetch
python -B -m workbench.session check docs/workstreams/research/AF-RES-125/manifest.json --fetch
```
정식 검사 결과와 manifest가 다른 시작판을 기록하면 중단하고 원래 통합 SHA 및 결과 SHA를 대조한다. 소비자 별도 공개 checkout에서는 아래 예로 4개 발췌 전문과 원래 구현을 확인; checkout 가능한 환경에서만 실행한다.
```sh
# scikit-learn root (read only)
git diff 306826f7b6bf5fd61af74062c0ba8f0f21aa3dae 468c3f40577da8d7b3699400ad86f36e5bb5ab60
git log -S 'wminkowski' -- sklearn/metrics/tests/test_pairwise.py
# matplotlib root (read only)
git log -S 'needed for 1.14.4' -- lib/matplotlib/transforms.py
# scipy root (read only)
git log -G 'def minkowski\(' -- scipy/spatial/distance.py
```
입력 회귀 검증: historical SciPy 0.19.1/1.0.0/1.6.0/1.8.0에서 u=[3],v=[0],w=[4],p=1,2 및 지원판 분기; historical NumPy 1.15.x/1.16.0에서 float32/64 NaN, empty Bbox와 warning captured. 각 version 환경·test definition·실제 stdout/stderr·release 별도 저장. 여기서는 분석식만 확인했고 실행 안 함.
첫 재개 행동: 고정 결과 475723b…와 SCOPE에 고정한 24번째까지의 전체 부모 diff를 재조회해 4개 발췌를 완전 판독하고 공석/대조를 재판정. 이어 최초 도입/릴리스와 기관 동일 객체 이력을 확보. 추가 모집은 별도 승인된 창으로만 실시.

색인 제안: `conditional substitute / support-floor / semantic boundary / announcement ≠ deployment / no eligible within title frame` — AF-RES-125를 121의 직접 귀속 조건을 강화하는 부정·보류 사례로 색인하고 효과 크기 추정에는 넣지 않는다.

| 불일치·약점 | 다음 조사 자료·행동 | 판정을 바꿀 관측 |
|---|---|---|
| 48개 중 본 적격 관찰 0; 4개 발췌 한계와 대조 정의 민감도 | 원격 고정 부모 SHA에서 git diff 전문 재판독 및 Q2 재코딩; 별도 승인 시 새로운 모집창 | 기존 자체 계산 삭제와 동일 경계 새 NumPy/SciPy 호출을 발견하면 본 슬롯 채움 |
| w/NaN 당시 계약 반례는 확인했지만 최초 구현/도입/첫 배포/실행 미확인 | git log -S/-G/blame→부모, release tag/배포 날짜 및 최소 CI; p=1,2·NaN·empty 회귀 실행 로그 | 모든 지원판 동작 일치 및 author의 인지·채택 근거가 같은 hunk로 연결되면 D3 |
| 기관 정책·롤아웃/소급 교체와 개별 객체 수정일 차이 | NGS 사용자 기관 동일 survey point 전후, GPO/LOC 동일 MARC 001/003/005/650 전후 export; workbench check | 객체·시각·사용판이 일치하는 전환 receipt 및 공식 검사 성공 |
