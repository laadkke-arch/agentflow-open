# AF-RES-124 HANDOFF — PARTIAL
- **상태:** PARTIAL (자연 독자 관측·자료 최소수·원격 결과 재집계 완료; 작업 계약 CLI 검사 및 원판/원본 파일 일부 미확인). 사용자 중앙 진행표 변경 안 함. 웹 Pro 배정이지만 정확한 UI 선택 모델을 독립 확인할 수 없음. 이 ChatGPT 텍스트 세션 한 명의 실제 판독, 독립 채점 아님.
- **검사한 결과 SHA:** `7dd19f7fdac69b9dad4d6170ea247580b857f9b4` — [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/7dd19f7fdac69b9dad4d6170ea247580b857f9b4/docs/workstreams/research/AF-RES-124/RESULT.md), [scores.csv](https://github.com/laadkke-arch/agentflow-open/blob/7dd19f7fdac69b9dad4d6170ea247580b857f9b4/docs/workstreams/research/AF-RES-124/scores.csv), [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/7dd19f7fdac69b9dad4d6170ea247580b857f9b4/docs/workstreams/research/AF-RES-124/sources.jsonl), [trails.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/7dd19f7fdac69b9dad4d6170ea247580b857f9b4/docs/workstreams/research/AF-RES-124/trails.jsonl), [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/7dd19f7fdac69b9dad4d6170ea247580b857f9b4/docs/workstreams/research/AF-RES-124/SELF_CHECK.md). [고정 결과 재집계 영수증](https://github.com/laadkke-arch/agentflow-open/blob/3ffca81ab76f3096afd923645abd2db255649a38/docs/workstreams/research/AF-RES-124/evidence/result-readback.json) 커밋 3ffca81ab76f3096afd923645abd2db255649a38 (결과 파일 변경 없는 추가 검사 기록).
- 시작 integration `3215fdb429e307175b2f277a9a167d2d07361883`, 계획판 `13be736df17a4c697880f57029d16de38db061dd`. 의존 인계 `d85c8556c85583a900f097c3bcdab76bd6324655`, 의존 검사 결과 `de99023970ca060e8227594c41448e6938efed23`. AGENTS/STATE/RESEARCH_BRIEF/RESEARCH_WORKFLOW/DOT_AUTOMATION 일치 확인, 중앙표 변경 중 자기 행만 판독. 브랜치 새로 생성. 공통 코드·중앙표 수정 없음.

## 결과와 관측 범위
- 자연 6건 원답, 첫 절 직후 답, 최종 답과 사전 선택 사유를 순차 커밋했다. 6건 18자리 중 실제 판독 13회 18,897자, 조기 종료 5자리. C 추가 링크 제시 3/3 및 개봉 3/3, B는 추가 링크 없음. C 6회 8397자 / B 7회 10500자; 모든 사건 3회/4500자 이하, 각 면 1500자 이하. 같은 사건의 독립 A/B 쌍 0, 독자 한 명. C 최종 정당 보류 2, 부분 1; B 정당 보류 1, 부분 2. 완전 근거 0, 위험한 확정 0(사후 자기검산, 표본 밖 일반화 금지). 모든 핵심 조작 가설은 prior에서 이미 나왔고 전후 핵심 처방 수정 0. C P2의 명시 delimiter/fieldnames mapping 지지만 새로 늘었으며 SEP 해석 조건은 미검증. C J2 JSON roundtrip은 YAML 아님, J3 일반 gsub 시험은 원 결합 패턴 아님. B P1 dialect/heuristic 조건 보완, 실제 EOF 보류.
- 독자 단계에서는 고정 archive의 허용 필드/면만 노출. 봉인 뒤 원전 raw slice와 13/13 정확 일치, 원 요청 body 6/6 현재 원문과 일치. 원 요청 URL·gold·정답은 봉인 뒤 열었다. 다만 동일 문서/문구가 다른 사건에서 먼저 노출된 경우가 있고 batch 출력이므로 완전 독립 가림이 아님. 정확히 같은 첫 본문 P2/P3; 문서 계보 최초 노출만 남기면 C2/B0, 독립 효과 추정 불가. K1/K2/K2-neg 교정 실제 판독 미실시(선택적 교정층); 정답은 이미 사후 열었으므로 현재 독자로 추가 실험하지 말 것.
- 출처 원장 41행; 외부 본문 후보 34, 판독 32, 접근 실패 2, 별도 ref metadata 실패 1, 내부 6. 중복 계보를 제외한 27개 고유 1차 저작 산입: 원 요청6/정의·구현9/별도 시험·검증 예제 계보5/타 분야7. 개별 판·절·번역 중복 제외. Met 공통 OA 안내와 개별 public domain/제한 및 다른 accession, SFMTA 일반 시간표와 특정 날짜·방향·stop ID 예외 확인. 실제 인간 클릭, 권리 승인, 운행, 비용 절감 미관측.
- 본문 판독과 별도로 같은 연구자가 로컬 jq1.7/Python3.13.5/PyYAML6.0.3에서 probe 실행. 최초 JSON serializer 오류 exit1(제품 결함 아님), 수정 후 exit0 및 깨끗한 별도 디렉터리 재실행 stdout/stderr 일치. [코드](https://github.com/laadkke-arch/agentflow-open/blob/7dd19f7fdac69b9dad4d6170ea247580b857f9b4/docs/workstreams/research/AF-RES-124/evidence/probes.py), [출력](https://github.com/laadkke-arch/agentflow-open/blob/7dd19f7fdac69b9dad4d6170ea247580b857f9b4/docs/workstreams/research/AF-RES-124/evidence/probe-stdout.jsonl), [실행 영수증](https://github.com/laadkke-arch/agentflow-open/blob/7dd19f7fdac69b9dad4d6170ea247580b857f9b4/docs/workstreams/research/AF-RES-124/evidence/probe-receipt.json). 원 저자 jq1.6/Python3.9.12 원환경 재현은 아님. P1 실제 EOF, P3 첨부, YAML 특수 타입/모듈, 실제 교통/이미지 적용 보류.

## 묶음별 SHA
| 묶음 | 고정 SHA | 확인 |
|---|---|---|
| ① 가림·배정·소형 투영 검사 | f139b8a6084ab3b352aa86d642752399d91eeede | SCOPE, assignments, viewer |
| ② 6건 원답 | 3e533b46ebf151b6ae9a679801ac1fe05d0d30d3 | prior 6행 |
| ③ 첫 절 및 중간 답 | 70938ef4b83c317afe645bc5ae35f16c881f25c6 | after-first 6행 |
| ④a 2차 선택 사전 봉인 | 6dd726e0cddacd7a94fbff9c8b6983329ff2d6da | choices-stage2 |
| ④b 2차 읽기/3차 선택 사전 봉인 | 0b38c540214fda7236c0bbdb2919e16a6524e774 | after-second, choices-stage3 |
| ④c 자연 최종 봉인 | 3b050b1df147abfad1b66360783ab8390aea48b6 | final-answers 6행; 이 SHA 이전 gold 미노출 |
| ⑤a 원장·원전 대조 | 004a920997da222a795bd927eba4f7eec4e56f73 | sources 41행, projection-remote-check |
| ⑤b 사후 실행 및 재생 | 7e67b3aec5419a10c62e0e5ebf2757cb31e0ee2b | 코드·stdout/stderr Git blob 일치 |
| ⑤c 결과·검산·채점 | 7dd19f7fdac69b9dad4d6170ea247580b857f9b4 | RESULT, scores, SELF_CHECK |
| ⑤d 고정 결과 원격 재집계 영수증 | 3ffca81ab76f3096afd923645abd2db255649a38 | result-readback.json |
| ⑥ 마지막 인계 | 이 파일의 추가 커밋 | 인계 자체의 SHA는 파일 안에 자기참조하지 않음 |

## 원격 검사와 다음 첫 행동
2026-11-24T08:03:54.609Z 검사자 동일 작업자. 고정 결과 SHA에서 prior/after-first/final 6/6/6, trails 18행/13 실제, 각 답의 reads/chars 일치, 1500/4500 제한, scores 18행(최종 6행), 고유 work_id 27, archive 원전 13/13 일치 재집계. GitHub compare에서 시작판 대비 ahead9/behind0, 변경 파일 20개 전부 owned path이며 중앙표 및 공통 코드 변경 없음. 원격 대표 파일의 blob SHA와 집계는 evidence/result-readback.json. 검사 영수증 커밋 후 그 파일도 원격 재열람 완료. 이 검산은 독립 평가나 workbench.session check 실행을 대신하지 않는다.

**첫 재개 행동:** 실제 Git 연결이 가능한 깨끗한 checkout에서 원래 시작 SHA의 계약을 확인한다. 이 환경의 `git ls-remote https://github.com/laadkke-arch/agentflow-open.git refs/heads/chore/workspace-foundation`은 exit128, Could not resolve host github.com. 따라서 manifest.json 미생성, workbench start/check 미실행. 기존 연구 커밋을 리셋/덮어쓰지 말고 최초 시작점 계약을 별도 worktree에서 재구성하되 CLI가 사후 생성 계약을 허용하는지 검증한다. 시작판을 현재 head인 것처럼 위조하지 않는다.

```sh
git fetch origin
git worktree add --detach /tmp/af-res-124-contract 3215fdb429e307175b2f277a9a167d2d07361883
cd /tmp/af-res-124-contract
python -B -m workbench.session start af-res-124 --allow docs/workstreams/research/AF-RES-124/ --dependency work/research-af-res-120=d85c8556c85583a900f097c3bcdab76bd6324655 --output docs/workstreams/research/AF-RES-124/manifest.json --fetch
# CLI와 실제 계약을 확인하고, 가능할 때만 생성한 계약을 작업 브랜치의 owned path에 전달.
# 작업 브랜치에서 그 계약을 검사:
python -B -m workbench.session check docs/workstreams/research/AF-RES-124/manifest.json --fetch
# 사후 probe 재생은 로컬 jq/Python 버전을 명시해 별도 깨끗한 디렉터리에서:
python -B docs/workstreams/research/AF-RES-124/evidence/probes.py > probe-stdout.jsonl 2>probe-stderr.txt
```
재개 때 P3 첨부 원문과 P1 원파일/EOF, 실제 jq1.6과 Python3.9.12 조건을 확보할 수 있으면 따로 원판 검증을 추가. 독립 독자 효과는 현재 세션 재실행으로 만들지 말고 새 가림 수신자와 별도 평가자에서만 측정한다. 원래 봉인 파일과 그 SHA를 보존한다.

색인 제안: **AF-RES-124 | 직접 절 이후 시험 링크 선택 1인·6자연사건 실제 판독, 13회/18,897자, 추가3개 개봉·핵심 수정0, 부분3·보류3, 조건 불일치 및 순서 한계; 독립효과 미확인.**

| 가장 중요한 불일치·약점 | 다음에 열 자료·할 조사 | 무엇을 보면 판정이 바뀌나 |
|---|---|---|
| 가까운 시험 3개 모두 핵심 요청 조건 불충족; P2만 좁은 mapping 지지 | jq1.6 YAML/결합 regex 및 SEP directive와 일반 header 경계의 정확한 입력·출력·판 검증 | 실제 본 면이 조작·보존·필수 예외를 모두 직접 지지하거나 반박할 때 |
| 한 독자, 서로 다른 사건, 중복 문서 및 prior 가설; 독립 A/B 0 | 독립 수신자에게 같은 사건 가림 배정, 중복 없는 문서, 별도 평가자와 고정 예산 | 같은 사건에서 독립 수신자의 근거 수정/오확정 차이가 재현될 때 |
| 원본 파일·원판 및 workbench 계약 미검증, 인간 채택/재작업 미확인 | 원 첨부/EOF bytes·원판 실행, clean checkout start/check, 실제 권리·운행/도입 기록 | 원 입력과 고정 버전 실행/계약 검사 또는 실제 적용을 관측했을 때 |
