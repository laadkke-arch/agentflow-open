# AF-RES-084 인계

**PARTIAL · 시도 1 · Codex Cloud.** 네 고정 사례에서 16셀을 재계산했다. 최초 확보본 10셀은 AF-RES-080과 일치했다. 넓은 참조 범위에서 AN01·CC01·AC01의 문서화된 구성은 양성이고 CN01의 기본 조합은 반박됐다. 개설 본문 0/4, 엄격 판정 0/16, 교정의 실제 성공 소비판 0/2다. 최초 원문을 복원했을 때 판정이 달라지는지 보류한다. 080의 120 자연·200 교정 모집, 엄격 48셀 및 정확 성공판 0/5 분모를 유지했다. [세 표와 분모](https://github.com/laadkke-arch/agentflow-open/blob/73195bd4ec01967d767d855be85e61d21d007500/docs/workstreams/research/AF-RES-084/RESULT.md)

## 고정 이력

| 묶음 | GitHub의 커밋 | 확정 내용 |
| --- | --- | --- |
| ① | [4ebad17a206141a8d9e936816c59989775f2715f](https://github.com/laadkke-arch/agentflow-open/commit/4ebad17a206141a8d9e936816c59989775f2715f) | 고정 양·음성 대조, 불변 ID·번호·UTC, 승인 경로, 복원 검증 |
| ② | [d3ff13eee67c7f81ddd39302d1f35576ef2b4423](https://github.com/laadkke-arch/agentflow-open/commit/d3ff13eee67c7f81ddd39302d1f35576ef2b4423) | GitHub 현재·080 확보 SHA 및 가린 C1·C2, 시간 파일·리비전 시도 |
| ③ | [d183ff516cc648f161acb0f9077666f42dcac914](https://github.com/laadkke-arch/agentflow-open/commit/d183ff516cc648f161acb0f9077666f42dcac914) | 작성자 사슬, 두 질문판·참조판, 공식 wheel과 사전 기대 |
| ④ | [73195bd4ec01967d767d855be85e61d21d007500](https://github.com/laadkke-arch/agentflow-open/commit/73195bd4ec01967d767d855be85e61d21d007500) | 결과, 16셀·48쌍 검산, 재현, 자료 원장과 자체 점검 |
| ⑤ | 이 파일만 커밋 | 다음 행동·검사 범위·원격 검증 |

작업 브랜치는 `work/research-af-res-084`, 소유 경로는 `docs/workstreams/research/AF-RES-084/`다. 계획 SHA `e7a777f2c13b626532b5828591d6388743688b34`, 최신 통합에서의 실제 시작·계약 SHA `f736bd557fa4c40aecb6833165823196cfa42af2`, 유일한 연구 의존성 AF-RES-080 `152f5261ab9a35ab675ab003931ac4dc89966b55`다. [시작 계약](manifest.json) · [080 인계](https://github.com/laadkke-arch/agentflow-open/blob/152f5261ab9a35ab675ab003931ac4dc89966b55/docs/workstreams/research/AF-RES-080/HANDOFF.md)

## 실제 확인과 남은 검증

결과 SHA `73195bd4ec01967d767d855be85e61d21d007500`를 2026-11-23 13:57:02Z에 새 Git 작업공간으로 원격 fetch했다. RESULT, SELF_CHECK, cells, runs, sources, manifest 여섯 파일을 로컬과 바이트 대조했다. RESULT SHA-256은 `41b38ee8c18fee3bda11cf7c6d8fedf05a77b85e00fe663bfef260d6f2ac45e3`다. [고정 결과](https://github.com/laadkke-arch/agentflow-open/blob/73195bd4ec01967d767d855be85e61d21d007500/docs/workstreams/research/AF-RES-084/RESULT.md) · [자체 점검](SELF_CHECK.md)

| 검사 | 대상·결과 |
| --- | --- |
| `python -B "$p/verify_events.py" --self-test` | 양·음성·중복·줄끝 복원 시험 종료 0 |
| `python -B "$p/recalculate.py" --check --upstream /tmp/af-res-084` | 16셀·48쌍, 상류 파일·절 지문 29개, 080 봉인 입력 대조 종료 0 |
| `python -B "$p/verify_result.py"` 및 Git 차이 검사 | 필수 표 3개, 자료 91행·외부 30계보, 근거 없는 개설 승격 0, 종료 0 |
| `python -B -m workbench.session check "$p/manifest.json" --fetch` | 결과 SHA `73195bd4ec01967d767d855be85e61d21d007500`에서 2026-11-23 13:56:36.155179Z에 실행. 종료 0 · `passed / remote_checked` · 통합 `f736bd557fa4c40aecb6833165823196cfa42af2` · 소유 경로 이탈 0 |
| `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 같은 결과 SHA의 깨끗한 작업 트리에서 종료 0. 자동 세션 탐색은 `no_active_sessions`로 보고됐다. 소유 경로 manifest는 위 명시 검사에서 확인했다 |

새로 실행한 10개는 사전 기대와 일치했다. CN01 명시 질문판 2개, CN01·AN01 참조판 4개, CC01 질문판 2개, AC01 역사판 2개다. 080에 있는 CC01·AC01 참조판 4개는 기존 영수증을 읽었다. 최초 CN01 CliRunner 경계는 25초 timeout이었다. 같은 입력·기대의 실제 stdin 파이프로 보정해 CLI 종료와 오류를 확인했다. 저자 성공 환경에서 실행할 6개 입력, 실제 개설 이벤트, #1060 원판, 다른 플랫폼·TTY, 독립 검토는 미확인 또는 미실시다. [실행 원장](runs.jsonl) · [보정과 선행 CSV 줄끝](evidence/fixture-correction.md)

## 다음 첫 행동

읽을 수 있는 승인된 환경에서 attrs #1060의 두 UTC 시간 파일로 먼저 복원 경로를 확인한다. Codex Cloud의 10개 시간 파일 GET은 프록시 403으로 원문 0바이트였고 GitHub GraphQL POST도 403이었다. 공개 S3 미러 및 GitHub 현재 화면에서 생성 리비전 파일을 확보하지 못했다. [실패 경로·시각·영향](attempts.jsonl)

```bash
p=docs/workstreams/research/AF-RES-084
resume_084="$(mktemp -d)"
for h in 0 1; do
  curl -fSL --max-time 180 "https://data.gharchive.org/2022-11-28-$h.json.gz" \
    -o "$resume_084/2022-11-28-$h.json.gz"
done
python -B "$p/verify_events.py" --case EDIT1060 \
  --body-output "$resume_084/original-1060.md" "$resume_084/"*.json.gz
```

대상 저장소 29918975·이슈 1465633178의 유일한 `IssuesEvent/opened`와 두 해시를 얻으면 최신 본문의 `evolve` 구절과 비교한다. 같은 방식으로 네 사례의 open 증거를 얻고 먼저 가린 요구를 커밋한다. 정확 소비판을 확보한 경우에만 해당 목록과 고정 양성·경계를 추가한다. 셀별 최소 재개 입력, 인증 GraphQL 대안과 재생 명령은 아래에 있다. [재현](reproduce.md) · [셀별 결손](cells.csv)

## 색인 반영 제안

`docs/research/INDEX.md`에 AF-RES-084를 AF-RES-080 의존 결과로 연결한다. 상태는 PARTIAL로 기록하고 확보본 10/16 재계산, 엄격/성공판 미확인, 링크로 반환 가능한 조건과 범위를 한 줄로 남긴다. [통합자가 읽을 결과](RESULT.md)
