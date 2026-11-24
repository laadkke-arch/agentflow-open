# AF-RES-126 인계

**DONE.** 공개 첫 게시물 10건의 선행 발췌판 해시를 모두 복구했다. 이번 10건에서 활성 별칭 12개의 완전 어절, 조사 허용, 마지막 어절 내부 적중이 모두 0이었다. 새 대조에서는 C가 두 뷰 각각에 직접 링크 3개와 충돌 링크 1개를 추가했다. D는 충돌 링크를 각각 2개 더 표시했다. 기존 구성 C01의 가림에서 D07은 별칭을 켜자 표시 3위에서 조사 4위로 내려갔다. C의 조사 활용과 표시 승격을 검토할 때 반환형과 발화 역할의 근거가 필요하다. [결과](RESULT.md) · [효과 원장](evidence/policy-effects.csv)

## 입력과 변경 구조

- 작업 브랜치는 work/research-af-res-126이며 시작판은 chore/workspace-foundation의 5c0eca97d41e084a76bddd7cb0e976e5e9f792e8이다. 등록 선행은 1fe299790d14a6bd93a101c005ba0802368cba50, 재생에 사용한 선행 결과판은 e69a3f837d400ba8a4820edb5bcd91223dc5f9cc다. 모든 커밋 파일은 소유 경로에 있다. [manifest](manifest.json) · [선행 인계](https://github.com/laadkke-arch/agentflow-open/blob/1fe299790d14a6bd93a101c005ba0802368cba50/docs/workstreams/research/AF-RES-122/HANDOFF.md)
- capture.py는 선행의 NFC·영문 심벌 가림·영문 어절과 B 투영을 재사용하고, 마지막 어절 비교에 필요한 희소 투영을 추가했다. replay.py는 선행의 가중치·순위·공석 구현을 재사용한다. summarize.py에서만 구간 역할과 496개 적격 기준을 순위에 결합한다. 후보 사전은 고정 SHA에서 읽는다. 공개 본문 전체는 임시 입력으로 사용했고 필요 구절·해시·투영을 커밋했다. [재현 명령](reproduce.md) · [원문](openings.jsonl) · [구간](matches.csv)
- 고유 직접 자료 38개는 한국어 원저자 10, 기술 용례·문법 11, 고정 API·시험 9, 철도 3, 도서관 5다. 공개 10건은 모두 동일 발췌판이며 현행 해시 차이 0건, 미확보 요청 0건이다. raw/JSON 경로와 최초 편집 이력, 별칭 A11/A12 원저작 재개봉은 미확인이다. 정규 모집의 8자리 복구, 실제 이용자의 클릭·이해, O5952의 Core ML 실동작은 별도 범위다. [원장](sources.jsonl) · [자가검산](SELF_CHECK.md)

## 검증한 결과판

검사 SHA는 **abcdda426e2a2d19f0732752c221ea4d494458c4**다. 그 SHA의 깨끗한 두 detached checkout에서 실입력의 원문·가림 투영과 48개 구간 위치를 다시 만들고, 원장 5개·집계 3개·필수 표를 커밋과 비교했다. 두 경로의 순위·분모와 각 stdout이 일치했다. 선행 A/B 1,216행, 조회 248건, 기능 점수 3,968행, 도메인 대조 7건이 검산됐다. GitHub에서 결과·자가검산·분모·출처 4개 파일의 blob을 재개봉해 대조했다. [실제 실행·입력 지문·stdout·stderr·종료값](https://github.com/laadkke-arch/agentflow-open/blob/4f8ff99023b7772f1c7accf4c974850cbb992dea/docs/workstreams/research/AF-RES-126/evidence/final-verification.json)

같은 Codex Cloud 작업자가 명시 세션 검사, 공통 검사, 2.5.1+cpu 프로브를 실행했다. 세 명령은 모두 종료값 0이었다. 명시 세션 검사는 원격 최신성 remote_checked, 통합 4ad08bf17c4b1ff6ac6219293ed9fe875743cf38, 범위 위반 0이다. 공통 검사는 공통 단위 55개와 lab 7·9개, demo, 독립 export, Git bundle 복원, reference-audit와 원본 smoke를 통과했다. 자동 세션 발견 결과는 no_active_sessions였다. 명시 검사로 이 manifest를 따로 검증했다. CPU 프로브는 구성 입력의 저장소·좌표·출력 검사다. 별도 독자의 판독은 미실시다. [검사 영수증](evidence/final-verification.json) · [CPU 결과](evidence/cpu-probe.json)

## 묶음별 원격 고정판

| 묶음 | 커밋 | GitHub에서 다시 연 파일 |
| --- | --- | --- |
| ① 규칙·기대·입력 | [b173f19fb035864e237ce39a3abe6583fc362d49](https://github.com/laadkke-arch/agentflow-open/commit/b173f19fb035864e237ce39a3abe6583fc362d49) | SCOPE |
| ② 공개 #1·해시·접근 | [6bbeb0d7ec6396fb7841ad1140984f7ca2ed4f02](https://github.com/laadkke-arch/agentflow-open/commit/6bbeb0d7ec6396fb7841ad1140984f7ca2ed4f02) | openings |
| ③ 출전·구간·여섯 대조 봉인 | [098d0f65c218135dd21b5096411a73c6b418b163](https://github.com/laadkke-arch/agentflow-open/commit/098d0f65c218135dd21b5096411a73c6b418b163) | controls, matches, sources |
| ④ 순위·두 재생 | [cc1a2a57f3dbb4b6cd2accd601338d3d32e95a90](https://github.com/laadkke-arch/agentflow-open/commit/cc1a2a57f3dbb4b6cd2accd601338d3d32e95a90) | replay, replay-runs |
| ⑤ 결과·분모·자가검산 | [abcdda426e2a2d19f0732752c221ea4d494458c4](https://github.com/laadkke-arch/agentflow-open/commit/abcdda426e2a2d19f0732752c221ea4d494458c4) | RESULT, SELF_CHECK, metrics, sources |
| 고정 결과판 검사 영수증 | [4f8ff99023b7772f1c7accf4c974850cbb992dea](https://github.com/laadkke-arch/agentflow-open/commit/4f8ff99023b7772f1c7accf4c974850cbb992dea) | final-verification |
| ⑥ 최종 인계 | [작업 브랜치 head](https://github.com/laadkke-arch/agentflow-open/tree/work/research-af-res-126/docs/workstreams/research/AF-RES-126) | HANDOFF |

색인 제안 · **AF-RES-126 · 한국어 조사 12형과 어절 내부 비교 · 공개 10건 효과 0, 새 대조 C 직접 +3·충돌 +1 및 D 충돌 +2/뷰 · DONE · docs/workstreams/research/AF-RES-126/RESULT.md**

## 다음 첫 행동

위 결과 SHA에서 P01b·P02b·P06b 원문을 꺼내 새 판독자에게 보여 준다. 발화 역할과 후보 입출력 기준을 먼저 확정한 뒤 조사 전용 안과 표시 안을 비교한다. 아래 명령은 그 결과판에서 실행할 세션 검사와 공개 JSON 경로의 재확인이다. JSON GET은 해당 공개 호스트에 접속되는 실행 위치에서 수행한다. [대조문](controls.jsonl) · [재현](reproduce.md)

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-126/manifest.json --fetch
curl -fLsS 'https://discuss.pytorch.kr/t/5952.json' -o /tmp/af126-topic5952.json
curl -fLsS 'https://discuss.pytorch.kr/raw/5952/1' -o /tmp/af126-topic5952-opening.txt
```

| 불일치·약점 | 다음 조사 자료·행동 | 판정을 바꿀 관측 |
| --- | --- | --- |
| 공개 10건에서 별칭 경계 효과 0건이고 직접 적격이 있는 회복은 구성층에서 관측됐다. | 활성 별칭과 실제 직접 적격이 함께 있는 새 한국어 저자 #1 원문을 사전 정의한 표본으로 확보한다. | 동일 기능을 지칭하는 조사 결합이 실제 저자 문장에서 조사·표시의 직접 회복으로 반복된다. |
| 지칭 회복 뒤에도 C01·C06·P05b·P06b의 역할과 입출력 충돌이 남았다. | 독립 검토자가 순위 없이 구절·출력형을 판독하고, 같은 사례에서 조사 전용과 역할 확인 후 표시를 비교한다. | 원문의 직접 링크를 유지하면서 거절·반대 출력의 표시와 후속 판독 비용이 함께 줄어든다. |
| 가림에서 P05a의 거절 이름이 사라지고 O5952의 일부 링크 세 개가 표시에서 빠졌다. | 각 쌍의 원문·가림에서 사라진 이름과 보존된 역할을 독립 판독하고, 자연 원문에 이름이 없는 요청을 별도로 확보한다. | 역할 판독이 유지되는 가림에서도 같은 일부 손실이 반복되거나, 이름 없는 원문에서 다른 회수 경향이 관측된다. |
