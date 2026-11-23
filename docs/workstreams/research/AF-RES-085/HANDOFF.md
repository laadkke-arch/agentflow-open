# AF-RES-085 · 인계

## 1. 식별

- 작업 ID와 시도는 **AF-RES-085 / 1**이다. 실행은 Codex Cloud, Debian 13.6 amd64에서 했다. 공개 조회는 작업 ID와 브랜치를 사용한다.
- 작업 브랜치는 **work/research-af-res-085**다. 계획판 184137d2f257f5d1a7ef584e0f3a6b35f3d280cd를 읽고 당시 작업 행이 있는 최신 통합판 **9dcae48a47b05d7ba2a1320444be28f5d0fcd739**에서 시작했다.
- 마지막 결과와 검사 SHA는 **9ce697f2552133108861cc5504ed64722dfde427**다. 그 뒤 이 파일을 단독 커밋했다. 원격 결과를 2026-11-23 15:22:54 UTC에 별도 checkout으로 다시 읽었고, 결과판 공통 검사는 15:23:04 UTC에 끝났다. [원격 결과 트리](https://github.com/laadkke-arch/agentflow-open/tree/9ce697f2552133108861cc5504ed64722dfde427/docs/workstreams/research/AF-RES-085)
- **REVIEW_READY.** 정식 24/24회의 GUI 경로·후속 키와 객체를 확인했다. G/L의 비교 가능한 8/8짝에서 화면 차이는 X3의 2/8, 다음 값 변경의 차이는 0/8이다. 명시적 재클릭 뒤 별도의 편집·undo는 24/24회 목표 객체에 적용됐다. [세 필수 표](RESULT.md) · [검산](SELF_CHECK.md)

## 2. 사용자 요구와 작업 범위

2019년 MuseScore의 Element 복사 초기화 G와 새 파트 순회 L을 같은 첫 부모로 재구성했다. 목표는 선택색이 다른 복제본이 실제 후속 편집 대상이 되는지 UI에서 판별하는 것이다. 허용 경로는 docs/workstreams/research/AF-RES-085/이고 선행 작업은 AF-RES-081@60d0c8a1c1ea20b4d5f9cf47ae9a24a627012cfc 하나다. 합성 악보와 공개 원자료를 사용했다. [범위](SCOPE.md) · [계약](manifest.json) · [081 인계](https://github.com/laadkke-arch/agentflow-open/blob/60d0c8a1c1ea20b4d5f9cf47ae9a24a627012cfc/docs/workstreams/research/AF-RES-081/HANDOFF.md)

## 3. 실제 변경

| 묶음 | 고정 SHA | 내용과 확인 |
| --- | --- | --- |
| ① | dc8abfe421d97e7476c025896ff2a9621513142b | 네 입력과 목표, 반증 조건, 계약 pin |
| ② | 9578255623ea06444422790daacfa8add3701364 | 세 build, Xvfb 기동 3/3, 공통 읽기 계측, 합성 악보의 독립 파트 링크 보정 |
| ③ | e14cecbc3df620a7bc17c3835ee79742494bae43 | GUI 24회, 직접 API 6회, 예비 실행·raw 로그·화면, 28개 독립 계보 |
| ④ | 9ce697f2552133108861cc5504ed64722dfde427 | 세 표, 두 반복의 대응, 픽셀·입출력·링크 검산 |
| ⑤ | 이 파일의 커밋 | 인계만 추가 |

정식 입력·명령은 [cases.csv](cases.csv)와 [reproduce.md](reproduce.md)에 있다. GUI의 실행 파일·argv·exit, 화면 및 저장 SHA는 [runs.jsonl](runs.jsonl), 독립 원독 42행과 한계는 [sources.jsonl](sources.jsonl)이다. 빌드 전 교정에서 실제 링크가 복원되는 것을 확인했다. X3/X4의 키 포커스는 두 조건 모두 탭 왕복으로 맞췄다. 해당 조작은 악보에서 재선택하기 전에 이루어졌다. [빌드 증거](evidence/build/) · [실행 시도 원장](evidence/gui-attempts.jsonl)

## 4. 실제 검증과 영수증

GitHub에서 작업 브랜치를 새로 받아 ④와 head가 같은지 확인했다. 소유 tree b8de1bf6a5463c2cf4aba53f19a46ec11e79f069의 594개 파일을 읽었다. 검산기가 527개 기록 파일의 지문과 24자리, 선택·음가·visible·재열기·픽셀을 다시 계산했다. 커밋한 verify.json과 재계산 결과는 바이트 일치했다. 기록된 결과의 SHA-256은 c8303be9f2a628a0ed6eaecf585de2cb8469f71b7b74b57db3a36249364cb39f다. [원격 검산 결과](https://github.com/laadkke-arch/agentflow-open/blob/9ce697f2552133108861cc5504ed64722dfde427/docs/workstreams/research/AF-RES-085/evidence/verify.json)

```bash
AF085_PACKET=docs/workstreams/research/AF-RES-085
python -B "$AF085_PACKET/fixtures/verify.py" --out /tmp/af085-verify.json
cmp /tmp/af085-verify.json "$AF085_PACKET/evidence/verify.json"
python -B -m workbench.session check "$AF085_PACKET/manifest.json" --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

| 검사 | 실제 결과 |
| --- | --- |
| 정식 GUI | 24/24, 모든 앱·재열기 종료 0. 반복 셀 12/12. 다음 키 무변화 24/24, -R 값 변경+undo 24/24, U 기준 8/8세트 |
| 직접 API | 6/6 종료 0. E05 복제 U/L 1/0/0 및 G 0/0/0. E06 세 판 0/0/1과 색 분기 통과. 둘의 재열기는 모두 0/0/0 |
| 자가검산 재실행 | ④ 원격 clean checkout, verify.py와 cmp 모두 0. Git diff 범위와 로컬 링크 검사 0 |
| workbench.session check | ④, 2026-11-23 15:22:58.014199 UTC, exit **0**, passed, remote_checked. 통합 ref 7045487ef36f67d5876f29a69372d645952757e9 |
| cloud_check | ④, 15:22:58–15:23:04 UTC, exit **0**. doctor, acceptance, research-case, original-smoke 및 sessions subprocess 모두 0. 전역 세션 검색은 no_active_sessions, 과제별 검사는 위에서 별도 실시 |

과제별 검사 영수증에서 변경 경로 배열을 개수로 요약했다.

```json
{
  "task_id": "af-res-085",
  "checked_at": "2026-11-23T15:22:58.014199+00:00",
  "checked_out_commit": "9ce697f2552133108861cc5504ed64722dfde427",
  "task_base_commit": "9dcae48a47b05d7ba2a1320444be28f5d0fcd739",
  "scope_base_commit": "9dcae48a47b05d7ba2a1320444be28f5d0fcd739",
  "integration_commit": "7045487ef36f67d5876f29a69372d645952757e9",
  "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
  "exit_code": 0,
  "status": "passed",
  "freshness": "remote_checked",
  "changed_path_count": 593,
  "outside_paths": [],
  "unmerged_paths": [],
  "errors": [],
  "raw_stdout_sha256": "ba0871e7db79050b424559782879e766e54978cb2825c337e5268acfabcac6f5"
}
```

공통 검사 raw receipt SHA-256은 4793585b4a94456d309311f75847520fc306a98f861bf0ce7716ec899d791007이다. 081의 36회 및 원 MuseScore CTest 21개 전수와 실제 재생 타이밍은 범위에서 제외했다. 예비 UI 및 build 실패와 복구는 적힌 시각으로 조회할 수 있다. 현재 남은 실행 장애는 없다. [실패 및 범위](SELF_CHECK.md)

## 5. 판단과 근거

X1의 복제 직후 비트 차이는 악보 모델의 마지막 범위 재선택에서 사라졌다. X2는 새 음을 역직렬화하는 분기부터 같았다. X3의 숨은 Fingering은 복제됐고 L의 tag 필터가 초기화 callback을 건너뛰었다. 재표시 후 L의 파란 자식에는 실제 선택이 없었다. 같은 V가 G/L에서 문서 값을 바꾸지 않았으므로 이 입력에서는 표시를 위해 G 링크를 추천하고 다음 편집 대상을 이유로 한 전역 선택은 유보한다. L은 보여 있는 X4의 자식을 초기화했다. [X3 대조](evidence/gui/X3-L-1/app.jsonl) · [X4 대조](evidence/gui/X4-L-1/app.jsonl) · [표 3과 적용 경계](RESULT.md#표-3-사용자에게-반환할-링크)

## 6. 다음 대화의 첫 행동

다음 작업자는 원격 브랜치 head와 ④의 검사 SHA를 확인한다. X3-L-1의 clone, tag skip과 주 키·저장 시점·재열기에서 같은 Fingering을 찾고 X3-G-1과 비교한다. 그다음 다른 답을 가르는 첫 실험은 x1.mscx와 x2.mscx의 메뉴 직후 6을 범위 지원 V로 바꾼 독립 조건이다. G/L 각 두 번씩 8회에서 selected IDs, visible과 undo를 읽는다. 이 계획에는 변경된 runner와 별도의 다음 실험 원장이 필요하다.

```bash
git ls-remote https://github.com/laadkke-arch/agentflow-open.git refs/heads/work/research-af-res-085
git fetch origin 9ce697f2552133108861cc5504ed64722dfde427
git show 9ce697f2552133108861cc5504ed64722dfde427:docs/workstreams/research/AF-RES-085/evidence/gui/X3-L-1/app.jsonl
```

중앙 색인 반영 제안 · **AF-RES-085 · REVIEW_READY · MuseScore 복제 플래그와 다음 GUI 편집 · 24/24, G/L 다음 편집 차이 0/8, X3 화면 차이 2/8 · AF-RES-081 pin · RESULT@9ce697f2552133108861cc5504ed64722dfde427.**
