# AF-RES-120 HANDOFF — PARTIAL

- 상태: **PARTIAL**, 자연층 6건 유지; 엄격 기회층 0/2(후보 jq 28/CPython 0), 독립 수신자 0, 가림 채점 0. 0 성공률로 오독 금지. 제어표는 수정하지 않음.
- 시작판 ba55c71bf1382dc7b83cf46b2439f590866fc50f; 계획 기준 101426a5e76154bb89b642dd9bd3c52fc1229c30 이후 3 commits, dot-control.json만 변경. 의존 116 handoff 23b14602ad6d400be6e00966815812a6b36cb0e6 및 result 31cc131279e606c9d691524525cbdbdf7dc7b44a.
- 검사 결과 SHA **de99023970ca060e8227594c41448e6938efed23**. [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/de99023970ca060e8227594c41448e6938efed23/docs/workstreams/research/AF-RES-120/RESULT.md), [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/de99023970ca060e8227594c41448e6938efed23/docs/workstreams/research/AF-RES-120/SELF_CHECK.md), [pairs.csv](https://github.com/laadkke-arch/agentflow-open/blob/de99023970ca060e8227594c41448e6938efed23/docs/workstreams/research/AF-RES-120/pairs.csv). 검사 증거는 6451665cf98aa567af7299b2eaa6871b8a21adeb의 [acceptance-evidence.json](https://github.com/laadkke-arch/agentflow-open/blob/6451665cf98aa567af7299b2eaa6871b8a21adeb/docs/workstreams/research/AF-RES-120/evidence/acceptance-evidence.json); 그 전 92c8bff evidence SHA의 경로 검사 포함. 
- 시작판 대비 결과 파일 31개 모두 소유 경로; dot-control 변경 없음. 결과 고정 SHA 재열람, 대표 INDEX 정의와 EOF 회귀 소스 assertion 확인, 892 제한 경로의 길이/문자/구간/마커 및 56 raw 패널 fingerprint 재검산 오류 0(동일 작업자, 독립 아님). 105 기회 패널은 생성 시 hash, 재검산은 metadata. 111 packet/route rows; 99 계획 stage rows; 33 judgments rows(실제 답 없음), 22 pair rows(실제 비교0). 28 고유 1차 산입(6+12+6+4), ledger 66행; test/example 계보 더 엄격히 합치면 회귀 최소수 위험. 
- 자료와 결론: B는 A보다 관련/인접 정의 마커를 더 자주 노출(1/6→6/6), C는 6/6에서 인접 시험까지 2회 안에 노출. 자연층 완전 기회 모두 미확인. JSON↔YAML, delimiter↔SEP, blank row↔empty field, writer↔reader 등 **같은 제목과 정답 조건은 다르다**. K1 B/C N33 1회 1500자 충분, K2 C N51+N54 2회 3000자에서만 EOF/strict 경계 증인, 음성 C 시험 잘못 연결. O42 A에서 3회 문서 월 규칙, O50 B/C 1회 -e 계약; 엄격한 실제 적용 기회층으로 승격하지 않음. jq1.7/Python3.13.5 다른 판 로컬 대조는 evidence/local-probes.md; 원저자 판 실행 아님.
- 제품 색인 제안 한 줄: **직접 절 주소 + 입력/판/보존/필수 예외 일치 검증된 추가 증거를 선택적으로 붙이고, 위치 도달·조건 증거·실행 관측·기존 사용자 인지를 별도 기록; C 효과는 아직 미측정.**

## 묶음 원격 커밋
| 묶음 | SHA |
|---|---|
| ① 모집·예산·채점 계약 | 192d7bfd2d05ed615fb5c8c6bc0da8fa6a8300c2 |
| ② 자연 모집·세 반환 봉인 | e1306691698e6b4d6a7c25431e850ec420801a5d |
| ② 기회 후보 41–42 사전 봉인 | 290dbaef65bdf39b3ab6607aac4029eb0c675842 |
| ② 기회 후보 43 사전 봉인 | 51ae34a48834a0c3a38cfb3b32902aad23fbe4ca |
| ② 기회 후보 44–50 사전 봉인 | 74899c05acd1c8007727f38d354356c155173b94 |
| ③ 직접 읽은 출처 원장 | d48216f9101fd3b8be4daba853261a36325d5193 |
| ③ 자연 및 구성 348 경로 | addb8c1b746ff21b96040d693141f386978941c0 |
| ② 기회 후보 51–68 사전 봉인 | 29201a391decc1ae5a1c36abdfc48464e97a6f28 |
| ③ 기회 544 경로·공석 유지 | 70f6572fc2d04a15a2f75942524dabc5d2893f00 |
| ③ 기준·로컬 대조·통합 packet | 0984a920b2ed954d9191b866f128879e385dc735 |
| ④ 실제 독자 결손 99 계획 슬롯 | 92c8bffc8d1bdde6405a2ee52340bd11d5667e9e |
| ⑤ 결과·pairs·judgments·자가점검 | de99023970ca060e8227594c41448e6938efed23 |
| 고정 결과 검사 증거 | 6451665cf98aa567af7299b2eaa6871b8a21adeb |

## 보류·다음 첫 행동
첫 행동: [RESULT 표 1–3](https://github.com/laadkke-arch/agentflow-open/blob/de99023970ca060e8227594c41448e6938efed23/docs/workstreams/research/AF-RES-120/RESULT.md), [reproduce.md](https://github.com/laadkke-arch/agentflow-open/blob/de99023970ca060e8227594c41448e6938efed23/docs/workstreams/research/AF-RES-120/reproduce.md), [packets.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/de99023970ca060e8227594c41448e6938efed23/docs/workstreams/research/AF-RES-120/packets.jsonl), [gold.csv](https://github.com/laadkke-arch/agentflow-open/blob/de99023970ca060e8227594c41448e6938efed23/docs/workstreams/research/AF-RES-120/gold.csv)를 분리하여 읽고, 독립 독자 18개 문맥을 실제 생성할 수 있는 환경인지 확인. gold/routes는 수신자에게 전달하지 않는다. 수신자에게 자기 packet만 주고 노출 전 원답을 저장. 엄격 기회층 2자리 미확인/공석은 자연층으로 대체 금지. 후보 39/84 시작 링크 공석과 판/입력 일치 결손을 먼저 보완. 
P3 원첨부 https://github.com/python/cpython/files/13635549/test_csv.csv 는 웹/connector 접근 실패; 허용된 공개 파일 다운로드로 실제 header 81/duplicate/empty를 대조할 것. J1/J3 jq1.6 고정판 및 O42/O59 jq1.7.1, O50 jq1.6 원 입력 실행. 실제 운영 소스의 browser anchors/TOC/literal links 확장 및 제작자 open/char 로그 필요. 
저장소 authenticated Git worktree 없음. manifest.json은 수동 provenance이지 workbench 생성 결과 아님. 재현 명령(미실행):
~~~sh
git fetch origin
git switch work/research-af-res-120
python -B -m workbench.session check docs/workstreams/research/AF-RES-120/manifest.json --fetch
~~~
manifest의 CLI schema 불일치 가능성이 있다. 정확히 시작판을 재구성한 별도 worktree에서 원래 start 명령(기존 파일 exclusive-create, 덮어쓰기 금지)을 재현하고 검사 SHA에 맞춰 기록할 것. 
~~~sh
python -B -m workbench.session start af-res-120 --allow docs/workstreams/research/AF-RES-120/ --dependency work/research-af-res-116=23b14602ad6d400be6e00966815812a6b36cb0e6 --output docs/workstreams/research/AF-RES-120/manifest.json --fetch
~~~
위 명령은 수행하지 않았고 출력/exit code 없음. 별도 원판 테스트 및 독립 판독 미실시. 결과가 실제 독자 효과까지 검증된 것처럼 승인하지 않는다. 

| 가장 중요한 불일치·약점 | 다음 조사와 직접 열 자료 | 어떤 관측이면 판단이 바뀌나 |
|---|---|---|
| 독립 독자·가림 채점 0 | 봉인 [packets](https://github.com/laadkke-arch/agentflow-open/blob/de99023970ca060e8227594c41448e6938efed23/docs/workstreams/research/AF-RES-120/packets.jsonl), [views](https://github.com/laadkke-arch/agentflow-open/blob/de99023970ca060e8227594c41448e6938efed23/docs/workstreams/research/AF-RES-120/evidence/natural-views.jsonl), 분리 [gold](https://github.com/laadkke-arch/agentflow-open/blob/de99023970ca060e8227594c41448e6938efed23/docs/workstreams/research/AF-RES-120/gold.csv) | 자연 A/B·B/C의 실제 완전 근거 답, 보류, 위험확정 비교 |
| 원판·입력 불일치와 strict 기회 공석 | [P3 첨부](https://github.com/python/cpython/files/13635549/test_csv.csv), [jq INDEX](https://github.com/jqlang/jq/blob/2e01ff1fb69609540b2bdc4e62a60499f2b2fb8e/src/builtin.jq#L297-L303), [stream 이슈](https://github.com/jqlang/jq/issues/3273) | 원판 동일 입력의 경계값 검증과 3회 내 완전 증인 |
| 고정 raw 뷰어와 실제 UI·비용 차이 | [DictReader](https://github.com/python/cpython/blob/deaf509e8fc6e0363bd6f26d52ad42f976ec42f2/Doc/library/csv.rst#L149-L166), [EOF 시험](https://github.com/python/cpython/blob/deaf509e8fc6e0363bd6f26d52ad42f976ec42f2/Lib/test/test_csv.py#L316-L321), 실제 렌더링 문서와 편집 로그 | 실제 UI에서도 기회 재현 및 C의 완전 근거 증가가 추가 비용 상쇄 |
