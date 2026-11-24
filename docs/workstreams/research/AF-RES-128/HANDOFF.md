# AF-RES-128 HANDOFF

**상태: PARTIAL.** 핵심 가림 재판독 18/18, 주장 72, 비교 조합 18/18(공석 0), 고유 외부 1차 저작 24(최소 22), 음성 대조 3 + 동일 작업자 경계 민감도 1, 결과 표 및 원격 재집계까지 수행. 다만 댓글 전체 반환/병렬 열람 때문에 Q4의 경로별 최대 3개 본문을 순차로 엄격히 제한하지 못했고, 원판·원파일·댓글 정확한 시간 및 실음/음표 직접 대조 미확인, checkout DNS 실패로 정식 세션 계약 검사 미실행. 이를 DONE으로 보고하지 않는다. dot-control.json 및 소유 경로 밖 파일 수정 없음.

## 의존·기준·검사 SHA
- 계획 기준: 4a92e22c5356dc7ea2b715f671077e8ab63b2835.
- 작업 시작 통합 head: 5c0eca97d41e084a76bddd7cb0e976e5e9f792e8. 작업 브랜치 신규 생성. AGENTS/STATE/START_HERE/RESEARCH_BRIEF/RESEARCH_WORKFLOW/DOT_AUTOMATION 및 dot-control 자기 행 확인.
- AF-RES-124 등록 인계: 0c1b5733c8ddc76341c6da872e8b405e6ed38963 (registry DONE; 인계 자체의 제한 별도). 결과 고정판 7dd19f7fdac69b9dad4d6170ea247580b857f9b4. 원 질문·면 보관판 120 de99023970ca060e8227594c41448e6938efed23. 124 인계·점수 본문은 가림 봉인 후 열었다.
- **본문/원장 고정 결과판: 3c8a3cf52c84cd9a8c5a06421087733bb8319e6b.** [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/3c8a3cf52c84cd9a8c5a06421087733bb8319e6b/docs/workstreams/research/AF-RES-128/RESULT.md), [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/3c8a3cf52c84cd9a8c5a06421087733bb8319e6b/docs/workstreams/research/AF-RES-128/SELF_CHECK.md).
- 원격 검사: [evidence/result-readback.json](https://github.com/laadkke-arch/agentflow-open/blob/21d177206f3f2739cf80c5a0ab52b8e3aa611fea/docs/workstreams/research/AF-RES-128/evidence/result-readback.json), 검사판 21d177206f3f2739cf80c5a0ab52b8e3aa611fea. 검사 주체는 동일 AF-RES-128 작업자, GitHub 고정 SHA 재열람·도구 내부 JS 재집계. 독립 사람 검사 아님. 최초 검사에서 Q=요청 본문을 E=외부면으로 검사하여 두 건 오탐; 요청 문자열로 재검사해 30 근거 anchor 중 30 일치, 42 무anchor(공석/주장 유형), 실제 miss 0. 봉인 주장·등급을 고치지 않았다. 코드포인트·조합 예산·N 연결·18 unique 슬롯·18 답/72 주장 ID·24 unique work ID 재확인. 비교 고정판 ahead 11/behind 0, 11개 변경 모두 owned path. 정식 workbench 검사는 NOT RUN.
- 작업 브랜치: work/research-af-res-128, 소유 경로 docs/workstreams/research/AF-RES-128/.

## 묶음별 커밋
| 묶음 | SHA | 내용 |
|---|---|---|
| ① 판독 전 규칙 및 누출 시험 | 99746d7da62c5bac396fa1cd6a1b6ac046df6f40 | SCOPE; PASS, seed·판정 우선순위 |
| ② 허용 필드 투영 | 62f09763ccb6d8b55ba93f7dc1258a884f81b885 | 18 packets, 56 archive 무결성, 13 실제 열람 |
| ② 가림 판독 봉인 | 418cf8865711c96c2b3a045f5a94a266fba417d4 | 72 원자 주장; H15/O3, 이전 점수 열기 전 |
| ③ 해제 및 기존 판정 비교 | f1c957a302812f28360a7defd01469211a6ae1ae | concordance 18행, 일치9/불일치9 |
| ④ 후보 검색 | d03a34bc6d56ad86d490c44244405682608cd1b3 | candidates 27행; 상한 위반 및 실패 기록 |
| ④ 연속 구간 보관 | ad610cc4f8a2672387c8d857cdaa7dbcae78f4b1 | 6 N + 민감도/반례 2 exact slices |
| ④ 동예산 조합 | c9dbe949e8543763a321567f707e75ffe72530a6 | 18 조합, 별도 대조 4 |
| ⑤ 원문 원장 | 9ef3061cfdaf72e2c6e7bfa0bab52f9c491b31ff | 45행 read40/failed5, 24 고유 |
| ⑤ 결과 | e24f863891519eaa564ac4baf955b95d9cdc2c2c | 필수 표·해석·3약점 |
| ⑤ 자체검산 | 29e18ea8671fcbbaa9768d0a48ec87c1b1c05dac | Q1–Q7 |
| ⑤ 가림 재현 README 및 고정 결과판 | 3c8a3cf52c84cd9a8c5a06421087733bb8319e6b | projection/README.md (사후 재현 안내, 원 규칙 수정 없음) |
| ⑤ 원격 재집계 | b795c0f73b8c6e3e2cf7549532a3d038c99da070 | 검사 로그 초판 |
| ⑤ 요청 근거 anchor 재검사 | 21d177206f3f2739cf80c5a0ab52b8e3aa611fea | 오탐 두 건 수정한 검사 로그 |
| ⑥ 최종 인계 | 이 파일을 생성하는 별도 마지막 커밋 | 검사판 이후 HANDOFF만 추가 |

## 핵심 판단
- 124의 원답/첫 답/최종 답은 새 답이 아니다. 기존 H12/P6와 새 H15/O3 차이는 핵심 유보 우선 정의 및 확정 표현 해석 차이. 9/18 일치. 완전 지지 0. 후단 12/12 좁은 주장 지지가 있으나 핵심 보류. 동일 사건 반복 인지 12/18 및 B13 원 답 타사건 언급으로 완전 독립 가림 아님.
- F 9,000자; F+O 17,397자; F+N 12,924자 (각각 6자리; 각 면 <=1500, 최대 두 면 <=3000). 같은 상한, 같은 실사용 글자 수는 아님. 새 N 6개는 특정 주장/입력/예외를 좁혀 주지만 새 독자의 효과 미관측. 원 질문 작성자의 입력과 프로그램 실행 입증 분리. 새 실행이나 124 스크립트 재실행 없음.
- 24 고유 외부 저작: 원 요청 6, 정의/구현 6, 별도 시험/예제 6, 서지 3, 악보 3. 동일 계보 합침, failed 5 제외. 실제 편집자 이벤트 정확한 횟수 미계측.
- P3 Writer 반대 방향, J2 JSON/YAML 입력 차이, J1 동일 id 갱신, P3 선택 경계가 dict(zip)을 포함하는지 반례. P1 EOF/P3 첨부 미확보. ISBN/매체 및 이조 파트 안내는 확인했으나 실제 본문·음표 대조 미실시.

**색인 제안:** AF-RES-128 | 당시 근거만 본 18답 별도 판독·정의 불일치 9건 | F/O/N 6×3 최대 3000자 | 동일 입력/동판 구현/예외 조합 | 제목 유사 음성 대조·구간 경계 민감도 | PARTIAL.

## 첫 재개 행동 및 미실행 명령
현재 원격 문서 환경은 GitHub connector 읽기/쓰기 가능하나 local git ls-remote는 DNS 오류로 checkout 불가. manifest.json 위조/현재 head로 시작판 교체 금지. 실제 Git 가능한 환경에서 저장소 fetch 후 고정 시작판을 별도 worktree로 열고 정식 start 계약을 재현할 수 있는지 확인하라. 기존 결과판과 봉인은 보존한다. 계약이 현재 작업 브랜치로 옮겨질 수 있는지 먼저 확인하고 검사한다.

```sh
git fetch origin
git worktree add --detach /tmp/af-res-128-contract 5c0eca97d41e084a76bddd7cb0e976e5e9f792e8
cd /tmp/af-res-128-contract
python -B -m workbench.session start af-res-128 --allow docs/workstreams/research/AF-RES-128/ --dependency work/research-af-res-124=0c1b5733c8ddc76341c6da872e8b405e6ed38963 --output docs/workstreams/research/AF-RES-128/manifest.json --fetch
# 실제 workbench 계약이 결과 브랜치의 시작판을 올바르게 증명할 수 있는지 확인한 뒤 해당 작업 브랜치에서 실행:
python -B -m workbench.session check docs/workstreams/research/AF-RES-128/manifest.json --fetch
```

정식 검사 재개와 별개로 연구를 보강하려면 후보별 단건 열람으로 두 경로를 다시 추적하고, 원 입력 파일/판본과 음표 확인을 기록하라. 가림 답 재판독은 이미 개봉했으므로 새 연구자에게만 배정하고 이 세션에서 독립 관측을 주장하지 않는다.

| 불일치·약점 | 다음 조사 자료·행동 | 판정을 바꿀 관측 |
|---|---|---|
| 동일 사건 반복·답에서 단계 단서가 보이고 등급 우선순위에 따라 9건 불일치 | 제3 평가자에게 사건별 1답만, H 우선/부분 우선 두 축 사전 고정 후 교차표 작성 | 반복 없는 독립 판독에서도 같은 3건 확정 서술 지적 및 6건 유보 우선 차이 재현 |
| 새 면은 입력/구현을 보강하나 원판 실행 및 P1 EOF/P3 첨부 없음 | 원 파일 확보, jq1.6 및 실제 Python판에서 보존·예외별 고정 기대값 검증; J3 다중 cd/SEP 정상 header 음성 시험 | 동일 판·동일 입력에서 조작/보존/예외 모두 직접 지지 또는 명시 반박 |
| 전체 댓글 반환으로 경로당 3개 후보 상한 엄격 위반, 선택 댓글 시점·악보 실음·정식 세션 검사 미완 | 후보별 단건 열람 UI/타임스탬프, 악보 총보·파트 실제 음표 대응 확인 및 고정 시작판 workbench 검사 | 상한 준수 독립 재탐색에서도 N 선택이 유지되고 계약 검사 통과, 실제 판별 일치 |
