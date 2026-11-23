# AF-RES-089 · REVIEW_READY

결과는 [4f7ace747bfc5313679b8023ce85b4e7cc3217f2](https://github.com/laadkke-arch/agentflow-open/commit/4f7ace747bfc5313679b8023ce85b4e7cc3217f2)다. 기본 필터의 X1/X2 메뉴 직후 V는 8/8 작동했고, 4/4 G/L 쌍이 같은 두 음을 바꿨다. 독립 V Undo는 8/8, 양성 2/2와 음성 2/2, 정식 재열기 22/22가 판정과 일치했다. Voice 1 제외 X1은 수동 V가 작동하지만 메뉴 뒤 양쪽 V가 무반응이었다. 이때 L에만 하단 E4 선택색이 남았다. [세 필수 표](RESULT.md) · [Q6 화면](evidence/aux/F-X-L/02-before-v.png) · [Q1–Q7 검토](SELF_CHECK.md)

## 고정 원격판

| 단계 | 원격 SHA |
| --- | --- |
| 배정 시 통합판 | [c2709abf8d25163eed75a7553ebcbde966105b55](https://github.com/laadkke-arch/agentflow-open/commit/c2709abf8d25163eed75a7553ebcbde966105b55) |
| ① 입력·대상·반증 봉인 | [a00648339b3bbda1eaac03bc23c7c7eb4e10cd42](https://github.com/laadkke-arch/agentflow-open/commit/a00648339b3bbda1eaac03bc23c7c7eb4e10cd42) |
| ② G/L 빌드 및 4대조 | [edebce1ba7d504daacbc818e725b0ab3cc1d52ae](https://github.com/laadkke-arch/agentflow-open/commit/edebce1ba7d504daacbc818e725b0ab3cc1d52ae) |
| ③ 메뉴 8자리 원 실행과 저장 | [ccdb1eb711fbcd707475cef6cfc83fa3b65b4fe2](https://github.com/laadkke-arch/agentflow-open/commit/ccdb1eb711fbcd707475cef6cfc83fa3b65b4fe2) |
| ④ 결과·자가검산·원자료 | [4f7ace747bfc5313679b8023ce85b4e7cc3217f2](https://github.com/laadkke-arch/agentflow-open/commit/4f7ace747bfc5313679b8023ce85b4e7cc3217f2) |

작업 브랜치는 `work/research-af-res-089`, 유일한 연구 의존은 DONE [AF-RES-085@7fc799c](https://github.com/laadkke-arch/agentflow-open/blob/7fc799ccbd5e458c94a5e680cae986c74c4a8671/docs/workstreams/research/AF-RES-085/HANDOFF.md)다. ④ 이후 이 인계만 추가했다. [manifest](manifest.json) · [출처 46계보](sources.jsonl)

## ④에서 실시한 검사

| 검사 | 원격 결과 SHA에서 본 종료값과 범위 |
| --- | --- |
| GitHub 원격 재열람과 소유 경로 | 새 clone과 고정 Contents에서 ④를 읽었다. 지정 경로 tree `ab971bf407aeae5ae27185ebe32e6f78ff372e82`의 450개 파일, 계약 diff 449개 변경, 경로 이탈 0. 진행표 차이 0. 표 1의 12자리와 표 2의 6행, 표와 원 로그의 키·입력 지문을 확인했다. |
| 작업 원장 재계산 | `fixtures/write_runs.py`, `fixtures/verify.py`, 각 `cmp` 종료값 **0**. ④의 `verify.json` SHA-256은 `8d152339f398abe969ca5ec5bf520a5aae75217bcf04b89096b0e37cc4e6f58c`다. |
| 개별 계약 | `python -B -m workbench.session check docs/workstreams/research/AF-RES-089/manifest.json --fetch` 종료값 **0**, 16:59:20 UTC, remote_checked. 통합판 c2709ab, outside_paths·unmerged_paths·errors 공집합. 원 stdout SHA-256 `294b1fc92e6fc90a017be8bdfe62a60e6df35203ffae8ae4174d0a4bad8d45ed`. |
| 공통 검사 | `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` 종료값 **0**. doctor·acceptance·research-case·original-smoke·sessions subprocess 0. 전역 검색은 no_active_sessions이며 과제별 검사를 위에서 별도 실행했다. receipt SHA-256 `a51063033382b8d308b2ef8090d150ebd8f8ea8845977ef5cc4afee3fa787169`. |

미실시는 원 MuseScore CTest 재실행, 타 OS 및 Inkscape/Calc GUI 재실행이다. 원 포럼 #281441과 Calc Bugzilla의 일부 원 본문은 접근 제한으로 미확인이다. CTest의 assertion과 외부 구현·회귀 소스는 직접 열었다. [범위와 제외](SCOPE.md) · [재현 명령](reproduce.md)

## 다음 첫 행동

[④ 결과](https://github.com/laadkke-arch/agentflow-open/blob/4f7ace747bfc5313679b8023ce85b4e7cc3217f2/docs/workstreams/research/AF-RES-089/RESULT.md)와 [F-X-L seq 17–30](https://github.com/laadkke-arch/agentflow-open/blob/4f7ace747bfc5313679b8023ce85b4e7cc3217f2/docs/workstreams/research/AF-RES-089/evidence/aux/F-X-L/app.jsonl#L17-L30)을 원격에서 연다. 아래 보표의 새 E4 주소가 유지된 채 flag=1·membership=0이고 V의 Undo 인덱스가 1→1임을 대조한 뒤, 사용자 목적에 해당하는 표 3의 첫 구현·시험을 선택한다.

핵심 약점의 조사 후보는 세 가지다.

1. 두 마디 부분 범위의 경계 밖 음 또는 crossover tie가 메뉴 목록이나 V 변경 집합에 들어가는지 본다.
2. 목적 보표에 파트 링크가 있는 경우 master/part 양쪽에서 VISIBLE과 PITCH를 실행하고, linked peer의 값과 재열기 차이를 본다.
3. NoteDot과 spanner를 포함해 Note visible이 복구돼도 자식·tie·Undo 인덱스가 달라지는지 본다.

색인 제안 · **AF-RES-089 · REVIEW_READY · MuseScore Explode 직후 V · 변경 8/8, G/L 대상 일치 4/4, Undo 8/8 · Voice 1 제외에서 L 선택색 잔존과 공통 무반응 · AF-RES-085 pin · RESULT@4f7ace747bfc5313679b8023ce85b4e7cc3217f2.**
