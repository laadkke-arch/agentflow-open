# AF-RES-121 HANDOFF — PARTIAL
- status: PARTIAL (조사 결과·최소 출처 충족, 실제 실행·공식 workbench 검증 및 당시 기록 공백 남음).
- repository: laadkke-arch/agentflow-open; branch: work/research-af-res-121; owned_path: docs/workstreams/research/AF-RES-121/
- start_commit: 3215fdb429e307175b2f277a9a167d2d07361883 (통합 head; 계획 13be736df17a4c697880f57029d16de38db061dd 이후 중앙표만 3 commits). dependency: AF-RES-117 HANDOFF 87081e48fd51ed74dd038070b1c46c7f3a7a8da2, RESULT 63d6852aa4693902bfafa420c319144e93d741a7.
- result_commit (고정 검사판): 97e69009bd64d56a96d12ed5d7e6614e395f0fce. [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/97e69009bd64d56a96d12ed5d7e6614e395f0fce/docs/workstreams/research/AF-RES-121/RESULT.md). 이 HANDOFF만 후속 별도 커밋; 자신의 SHA는 커밋 후 외부에서 확인.
- index proposal: AF-RES-121 PARTIAL / 5 사건·6 목표 연결·17 claims·31 고유 원저작 / 목표 직접 귀속 확인 0/6 / 선행 변경·문구 정정·독립 원인·실행 영수증 구분 / RESULT 97e69009bd64d56a96d12ed5d7e6614e395f0fce.

## 핵심 인계
R1 1/13 output 폐기 유보가 1/19 io-mux 인용보다 선행; 01030129는 순서/출처 주장의 신뢰성 문구 완화, 서명/시험 무변경. R3 enum_dispatch 최초 확인을 1/8에서 1/6 02:12:25로 정정; wrapper 반례는 Pod 인용보다 먼저, 자동 위임의 안전 제약은 TODO와 미해결, 가용시간 진술 후 unmerged 종료. P4 2/13 commit 08:14:08 vs #13838 인용 08:19:22(314초, 공개 push 미확인); September rewrite는 독립 사용례 부족/피드백을 명시. October other_keys/readonly flag 유보는 Pyright 7/17 narrowing 구현·PEP728·사용 혼란이라는 새 경쟁원인; 기능 기여는 확인되지만 exact contemporaneous link 독서 및 728 exact 당시판 공백이므로 링크 직접 귀속 D3로 세지 않음. R2 사후 anyhow 비유 및 R4 GHC 기존 prior art 용어 정정 대조; R4 후속 정책은 design meeting 별개. 근접 3, 대조 2에서 목표 6 선례 직접 귀속 확인 0; 무영향이 아님. 교통 3A 기각 후에도 Powell 용량/안전 제약 보존; 미술 NG194 Board 2023-03-30 treatment 승인과 2024-05-23 재전시 승인 확보, 구체 대안별 사전 보고서 미확인. 역할별 제안·보류·조합 링크는 fields-and-returns.md.

## 묶음별 SHA (원격 커밋 후 대표 파일 재조회)
1. 21ac5f6232c1037d364d75602ff8cace1d76a299 — SCOPE/초기 선택 봉인.
2. 95c527aede263780b1e75da249b83c3ea5961d8e — 당시 버전 및 공백.
3. 151862b25dab95b819a026a98e84e3cdf9e4856e — 반응/전후 hunk/경쟁원인.
4. 96f2979387b0940d45f53cb8a2798f74a6e34fe5 — 대조/분야/역할 및 원장.
5. 97e69009bd64d56a96d12ed5d7e6614e395f0fce — 필수표·claims·SELF_CHECK·검산, P4 경쟁원인 보강 및 중복 조정.
6. 이 HANDOFF 별도 커밋.

## 고정 결과 SHA 원격 검사 (작업자 자체)
GitHub connector로 97e69009bd64d56a96d12ed5d7e6614e395f0fce의 sources.jsonl/claims.csv/versions.csv/timeline.csv/RESULT.md/SELF_CHECK.md/evidence/ledger-check.json/initial-choices.csv/fields-and-returns.md/evidence/replay.md를 다시 fetch. JS로 실제 JSON·CSV parse: 107 source rows, source_id 107 고유, 후보 주소 106, 본문 83행/83주소, metadata 9, 실패 시도 15, 중복제거 고유 1차 저작 31, 초기 5행, 버전 6행, timeline 58행, 주장 17행, 참조 188개 누락 0, CSV 폭 각각 18/10/6/8 일정; SELF_CHECK 7 Q행; RESULT 첫 3표 및 끝 3행 약점표. 목표 D3 0, 실제 receipt 및 노동시간 관측 0, 각각 실제 발생 미확인. 후보 수는 원장 기록 범위이지 전체 검색 후보 전수 아님. 동일 저작 및 중복 SC 승인 제외. 개별 열람 UTC 미보존; 세션 범위만 기록.
GitHub compare start...result: ahead_by=5, behind_by=0, total_commits=5, 파일 14개 모두 added, 모두 owned_path 내부, 중앙표·제품 코드 수정 0. 결과 파일 검산 수행자는 본 ChatGPT 작업자, 독립 판독 없음. 제품 동작·외부 regression 실행은 관측하지 않음. 이 검산을 workbench 통과로 표기하지 않는다.

## 미달·재개
실행 환경에서 git ls-remote https://github.com/laadkke-arch/agentflow-open.git refs/heads/chore/workspace-foundation (2026-11-24T07:53:04Z): exit 128, stderr Could not resolve host: github.com. checkout 불가하여 정식 manifest 생성 및 session check 미실행. GitHub API로 커밋/검증했다. **첫 재개 행동**: 네트워크 되는 허가된 checkout에서 original start SHA와 dependency를 fetch/확인하고 workbench.session의 manifest 생성 계약을 읽어 별도 깨끗한 worktree에서 원 시작판을 재현. 시작판을 현재 branch head로 바꾸어 성공을 흉내내지 말 것. 다음 명령은 원 계약의 재실행 입력(미실행):
```sh
git fetch origin chore/workspace-foundation work/research-af-res-121 work/research-af-res-117
git cat-file -t 3215fdb429e307175b2f277a9a167d2d07361883
git cat-file -t 87081e48fd51ed74dd038070b1c46c7f3a7a8da2
# session 계약에 따라 원 시작 SHA의 별도 worktree에서:
python -B -m workbench.session start af-res-121 --allow docs/workstreams/research/AF-RES-121/ --dependency work/research-af-res-117=87081e48fd51ed74dd038070b1c46c7f3a7a8da2 --output docs/workstreams/research/AF-RES-121/manifest.json --fetch
# result SHA 검사용 checkout으로 올바르게 manifest를 옮겨 원 계약 유지 후:
python -B -m workbench.session check docs/workstreams/research/AF-RES-121/manifest.json --fetch
```
stdout/stderr/exit, SHA 및 manifest start 확인 후 기록. 원 시작 계약 재현 불가하면 실패 사유를 남기고 새 manifest로 덮어쓰지 않음. evidence/replay.md에 fixed version·시험 후보·입력·명령(당시 runner 확인 필요), 과거 실행 receipt vs 새 실행 구분. 레지스트리 exact 초 단위·작성자 실제 독서판·force-push/이전 Zulip·mailing-list·원안 push 시각, SFMTA 2/19 당대 결의 및 NG194 사전 대안 보고서, 실제 테스트 영수증/노동시간 미확인. 독립 reviewer 미수행. 중앙 진행표는 수정하지 않았다.

| 가장 중요한 불일치·약점 | 다음에 열 자료·할 조사 | 무엇을 보면 판정이 바뀌나 |
|---|---|---|
| P4 Feb commit metadata 선행; September pivot과 mypy 인용 단절; October checker 변화 별개 | #2997 push timeline/이전 draft, 6/9 공개 기록, #3440 mailing-list 원문, 당시 PEP728 immutable patch | 동일 선택/시험을 #13838로 바꿨다는 당시 당사자 발언+전후 diff+당시판 |
| R3 enum_dispatch 최초 관측 1/6으로 정정; Pod·wrapper·macro·TODO 혼재, registry UTC 불완전 | 이전 공개 토론/force-push 보존판, crates.io version JSON, TODO 이후 제약/시험 hunk | 승인 제약/시험의 원인 특정 및 당시판 확인; 먼저 같은 제약이면 사후 근거 |
| NG194 사전 승인 확보, 구체 대안 보고서 없음; T2 용량자료는 Feb 결정 이후; 실행/시간 미확인 | NG194 examination/treatment dossier, 2/19 SFMTA 원 결의, TST-2 monitor, 시험 receipt/노동 기록 | 날짜·권한자·같은 대안 선택 이유 및 실제 receipt 확보 |
