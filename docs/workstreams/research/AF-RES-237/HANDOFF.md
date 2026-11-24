# AF-RES-237 HANDOFF — PARTIAL

## 실제 상태와 고정 결과
- web-pro 조사·판독. 중앙표 수정 없음. 브랜치 `work/research-af-res-237`, owned path `docs/workstreams/research/AF-RES-237/`.
- 고정 결과 SHA(⑤, HANDOFF 전): `23c2bd58e9f08816231c81f796aaa75a8500cead`. 통합 착수 `610bcdf35a3dc04bc7f55ce1ecf0a339d9d881e6`, 요청판 `914dbfa789ebec97063ed97130ea2a71c2e9f503`, +6/-0 dot-control만 변화, 237 신규 RUNNING, 226 중앙 DONE 고정 인계 `d166817bc25f79650f2d02835b0f5f42617cdbdd` (226 자체 PARTIAL). 범위/표집 규칙 먼저 커밋 후 외부 근거 열람. 227–229 결과 사용하지 않음.
- 12자리 원행·배정·작성자 시간 정의 연결 완료, 품질/독립 검수/사용자 인수의 결손을 근거로 총노동 절감률 보류. 자료 수 23(그 중 원저자 초록만 2; 엄격 full artifact 21), 16 lineage, 31 ledger entries, early category 4/5로 미달. 독립 study tool/별도 protocol 원자료 미확인(부록을 별 연구로 세지 않음). 원자료 수와 분류 하한 모두 충족해야 하므로 **PARTIAL**. 원저작/사건 구분, PDF 화면 실패, 개별 UTC 시간창 제한 기록. 독립 리뷰, 전수 회귀 실행 미실시.
- 대표 파일: [RESULT.md](RESULT.md), [SCOPE.md](SCOPE.md), [sources.jsonl](sources.jsonl), [cohort.csv](cohort.csv), [stages.csv](stages.csv), [estimands.md](estimands.md), [evaluation.csv](evaluation.csv), [SELF_CHECK.md](SELF_CHECK.md), [counterexamples.md](counterexamples.md), [primary-observations.md](primary-observations.md).

## 묶음 커밋
| 단계 | commit SHA | 결과 |
|---|---|---|
| ① 범위·예측/표집 사전 봉인 | 8b045808fee35d93676180cc3a4d495d0bfbbd00 | SCOPE |
| ② 원자료 원장·영수증 | 05a3c1a4d1c83e7df559c8095e42a5ed5634e2ae | sources |
| ③ 필수 표 원행 및 주관측 | fbbb2e775279124e2ad22025f41a970d5fcb238a | cohort, stages, primary observations |
| ④ 반례·정정 | 9e0dff6fb2ef803fa3d9eebcd7d8aee53d9a0697 | counterexamples, ledger 추가 |
| ⑤ RESULT·SELF_CHECK | 23c2bd58e9f08816231c81f796aaa75a8500cead | RESULT, estimands, evaluation, SELF_CHECK |
| ⑥ HANDOFF | 이 파일의 단독 최종 commit | 이 파일 |

## 관측과 약점
- METR early fixed `7ff2d7670235f531dff77eff58355bd77392f396`; 246 완료(110/136), 16 dev; 12 sample(6+6) all dev655, 두 시간 모두 작성자 분, 7 observed zeros, 0 missing sample. 246 initial nonmissing, post230 observed, 16 blank; 논문 C.3.4 27/~12%와 불일치. README external resources coding vs G.2.1 지침 방향 충돌. 12 단순 평균 146.50 vs226.67분, 대표성/인과 없음. 발표 로그 조정 ratio +18.8%, 별도 산술비 다름. 공개 reviewer/acceptance key 연결 0/12(미확인, 0 노동이 아님).
- Late fixed `55f007216a26493f0a9b7650ab3191cad7fb9e7f`; 1134 = complete828/incomplete244/ditched57/cheating2/corrupted3; author code filter 조건 직접 대조 827 valid complete, 900 started 중 이상 상태 5. README와 원행 상태 불일치. 회귀 실행 안 함. 사전 선택과 concurrent AI, 실패비용 누락. 두 실험 합산 금지.
- Temizöz pilot 두 역할 실제 79.17분 Pass 93.36%, 66.36분 Fail 66.39% (별도 연구 QA, 고객 인수 아님). 추천 평가: 모든 배정+실패, 노출/사용 분리, 동일 요구·artifact version, reviewer/person-min, rework, 최종 acceptor/기준/판정, 비용/acceptance fraction 동시 보고. 기존 AI 허용 효과를 링크 추천에 옮기지 않음.
- 결정적 세 약점: (1) 결측 수와 척도 판본 불일치 및 early fifth 독립 원자료 미확인, (2) reviewer/acceptance unjoined, (3) late status/exclusion 및 completion selection. RESULT 최종 표에 반전 조건.

## 결과 SHA 자체 재검사
⑤ SHA로 GitHub 10개 파일 모두 직접 fetch readback (blob SHA 및 lengths 확인), RESULT 첫 두 표, cohort12행 6/6, same dev1, zero7, 12개 row 값 table 일치, Q1–Q7 headings, 마지막 약점 3행, 원장 31행/23 distinct work/16 lineage/4·6·5·4·4, SELF_CHECK 독립검토 미실시 확인. 통합 착수판 대비 +5/-0, 변경 파일 10개 전부 owned path; dot-control 없음. 데이터 원행 재판독 JS 조건/산술 수행, 실행 기반 모델 검증·별도 제3자 리뷰 아님. 원문 일부 screenshot timeout 또는 502, parsed PDF 성공 여부 ledger 분리. 초기 논문 v2와 repo 공개 판은 고정했으나 완전 정합 미확인.

## 다음 첫 행동 — 미실행 Codex 입력/기대/반전
1. 고정 저자 저장소에서 README·data·regression 원본 blob/commit 재대조. 아래 CLI는 ⑤ 뒤 고정 README 직접 재열람하여 확인함. estimands.md의 positional 예는 실행 예고가 아니라 README 확인 전 후보이며 **정확한 진입점은 --input-data**. 임시 작업환경에서만, 설치/실행 정책이 허용된 Codex 작업으로 넘긴다.
```sh
git clone https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs.git early237
cd early237
git checkout --detach 7ff2d7670235f531dff77eff58355bd77392f396
git rev-parse HEAD
git hash-object data_complete.csv regression.py README.md
# author README dependencies (approved isolated env only):
# pip install statsmodels==0.14.4 scipy==1.15.2
python regression.py --input-data data_complete.csv
cd ..
git clone https://github.com/METR/Measuring-Late-2025-AI-on-OSS-Devs.git late237
cd late237
git checkout --detach 55f007216a26493f0a9b7650ab3191cad7fb9e7f
git rev-parse HEAD
git hash-object data.csv regression.py README.md
# author README dependencies (approved isolated env only):
# pip install pandas numpy statsmodels scipy
python regression.py --input-data data.csv
```
   기대 early blob data b61294d8214aa723d2b15986ab050e516955004a; regression fd2cfc600b4c7e774ab50c0a03bfba823410b5c1; README 60b37cf6df948e51002afa5c727b22632d6c8552. late blob data 96ce351cc1bbdb3d3bfc863d4beca038754392d2; regression 2b56c17779ac47eae69f1e4530a109b8e808af5a; README 37c0c0bb74aa0f7a1b2ef55ebd34dbf88b145f91. Early output 0.188, nonrobust(0.013,0.395), HC3(0.013,0.394), clustered(0.016,0.390) author expectation, not actual run. Verify missing16, actual zeros109, mean impute by treatment, 12 numeric first ids as cohort, coefficient/SE/CI and version history. Divergence -> preserve stdout and dependency versions, no silent input replacement. 
2. Late regression compare exact complete valid827/started900 as raw condition counts, sensitivity excluding cheating/corrupted from started (expected 895 before other model drop) vs as-published; status/validity rules, per-panel and new counts. Do not infer acceptance from complete, report failed/censored costs and missing bounds, no pooling. 
3. Find standalone original early experimental app/task-entry form/instruction artifact separate from paper/README (public only), resolve 27↔16 and resource coding from author history; direct full originals for D02/T04, screenshot p108–112 Temizöz retry if available. No identity tracing. If missing, remain PARTIAL; if resolved and category gate met, new reviewer can adjudicate. 
4. Run exploration product pilot only after protocol approved; use evaluation.csv. Same req hash, all assignment rows, person-min by actor, same final artifact acceptance; test unused exposure and review burden reversals. 
색인 제안: central result pointer to this final HANDOFF commit, preserve self status PARTIAL and reason (early source category shortfall; independent regression not executed; total labor/acceptance unobserved). No central edits by worker. Next work should reference fixed ⑤ for research and final HANDOFF for execution instructions; not label METR effect as product efficacy.
