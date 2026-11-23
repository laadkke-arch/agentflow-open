# AF-RES-069#1 · 부분 인계

## 1. 식별

- 작업 ID / 시도: **AF-RES-069 / 1**.
- 작업 종류: web-pro 공개 원문 연구 및 자기 경로의 Git 기록.
- 모델·위치: 세션 지시의 제품명 GPT-6 Astra Pro, ChatGPT cloud workspace. 별도 런타임 model ID는 확인하지 못했다. A/B와 재판독은 같은 모델의 별도 문맥이며 독립 인간 판독은 없다.
- 공개 작업자 참조: AF-RES-069#1, 이 저장소·브랜치·고정 커밋.
- 저장소 / 브랜치: `laadkke-arch/agentflow-open` / `work/research-af-res-069`.
- 실제 시작 foundation: `76b8c1d15812fbf91b879f8444fd188ae7445802`.
- 계획 기준: `320424d87f99e70c42eeb8cb7211467de27f2c2e`.
- 마지막 확인·원격 저장 결과 커밋 **(이 HANDOFF 작성 직전)**: **`fb710fce01052a5b907398e2da6840b59d3cfa08`**.
- 연구 내용 커밋: `0c3ab1c1c8359d3c5f85c8b9e51dc7119f8b2dec`; 최종 결과 커밋은 위 내용에 실제 검사·원격 대조 영수증을 더한 판이다.
- 원실험 봉인: `de1727aada52835ebcde4ff1c92c3940db215476`; 문제·질의 봉인: `03d1e436cfa7dc209b57b19508ef4b2e75942824`.
- 마지막 실제 증거: 최종 결과 HEAD의 session check/41항목 delivery 검사 종료0, 이어서 같은 SHA의 GitHub17파일 대조8항목 통과.
- 최종 원격 재열람 UTC: **2026-11-23 09:30:02 UTC**.
- PR: 이 연구 작업으로 새 PR를 만들지 않았다.
- 상태: **PARTIAL**. 사용자가 지정한 부분 인계 상태다. 기록·계약 검사의 통과를 연구 완료로 승격하지 않는다.

이 파일은 모든 결과·수용 파일을 고정 SHA로 다시 읽고 대조한 뒤 쓰는 마지막 파일이다. 자신의 미래 커밋 SHA를 본문에 넣을 수 없으므로 위 SHA는 부모 결과판이다. 마지막 커밋의 변경 파일이 이 HANDOFF 하나인지 Git diff로 확인하면 된다.

## 2. 사용자 요구와 작업 범위

목표는 원 분야 이름을 모르는 관계 표현이 실제 소프트웨어 요구에 추가 대안을 주는지, 일반 탐색과 같은 조건으로 비교하는 것이다. 최초20원문 이상의 직접 독해, 후보별 반례, 봉인 뒤 실제 개발자 논의·타분야 절차 비교, Q1~Q8의 근거 대응을 기록했다.

읽은 시작 통제는 foundation의 AGENTS.md, STATE.md, docs/product/RESEARCH_BRIEF.md, docs/RESEARCH_WORKFLOW.md, docs/DOT_AUTOMATION.md, docs/automation/dot-control.json의 AF-RES-069 항목이다. [기준 제품 brief](https://github.com/laadkke-arch/agentflow-open/blob/76b8c1d15812fbf91b879f8444fd188ae7445802/docs/product/RESEARCH_BRIEF.md), [배정·읽기 기록](https://github.com/laadkke-arch/agentflow-open/blob/fb710fce01052a5b907398e2da6840b59d3cfa08/docs/workstreams/research/AF-RES-069/evidence/assignment.json)을 기준으로 했다.

선행 인수는 [AF-RES-065 HANDOFF@18e4449e…](https://github.com/laadkke-arch/agentflow-open/blob/18e4449eb0ac04464aee8fa6cc07f1f6a54d0b5d/docs/workstreams/research/AF-RES-065/HANDOFF.md) 한 건이다. 그 과거 연구 결과·후보 원장·연결 자료는 다시 열지 않았다. 065의 기간 내 채택 공백을 이번 연구의 채택 성공으로 채우지 못했다.

허용 편집 경로는 `docs/workstreams/research/AF-RES-069/`뿐이다. 중앙 dot-control, 다른 작업 브랜치, 제품 코드, 실제 서비스·장치는 변경하지 않았다. 공개 이슈·문서·논문·특허·코드·업무 절차를 읽고 자기 경로를 커밋했다. 외부 당사자에게 메시지를 보내지 않았다.

## 3. 실제 변경

| 파일·묶음 | 변경 사항과 이유 | 확인 방법 |
| --- | --- | --- |
| SCOPE.md, frame.csv, manifest.json | T0 모집식과75행, 실제 foundation·선행·허용 경로 고정 | 첫 커밋 tree, 입력 audit, session start 종료0 |
| problems.jsonl, queries.jsonl | 관측 문제3개, 조건·경계·사전 노출, A/B 질의18개 봉인 | 03d1e436…과 바이트 일치 |
| runs.jsonl, judgments.csv, arms/ | 90원순위·분류·조건 근거·반례·실제 비용, 원 worker 기록 보존 | de1727aa…과 바이트 일치; 조인·23열 검산 |
| sources.jsonl | 봉인85행의 정확한 바이트에 사후14행 추가; 최종99접근/자료 기록 | source ID·계보·산입 플래그·UTC·근거·한계 검사 |
| RESULT.md, decisions.md | 선두 표1~3, 상세30후보/18질의, Q1~Q8, 선택 변화와 마지막 약점3건 | 원행 대조·같은 모델 최종 주장 검토17항목 |
| SELF_CHECK.md, evidence/acceptance-evidence.json | PARTIAL 수용·미실시·실제 검사·원격 대조 상태 | 최종 고정 SHA에서 다시 읽음 |
| evidence/*audit*, *review*, postseal*, aviation* | 실패도 포함한 감사, 댓글·PR 맥락, 실제 FAA 절차 비교 | 원문 절·메타데이터·고정 head·별도 비용 보존 |
| evidence/resume-checks.md, verify.py | 못 한 검사의 환경·명령·입력, 실행 가능한 원장 검산 | delivery checker 실제 종료0; 제품 실행은 미실시 |
| HANDOFF.md | 부분 인계와 다음 첫 행동, 최종 검사·재열람 증거 | 마지막 단독 커밋 대상으로 작성 |

첫 모집 커밋은 `c5b0410ef23fa44fdc3c4129682f9a468330b783`이다. shell push는 인증 부재로 종료128이었고, 이미 허용된 GitHub 연결로 동일 tree를 발행했다. 첫 본문 독해는 로컬 봉인 뒤·원격 발행 완료 전이었다. 이 차이를 숨기지 않았다. 이어 입력 봉인 → 입력 감사 → 두 초기 갈래 checkpoint → 전체 검색/초기 판정 봉인 → 결과 → 실제 검증 묶음 순으로 커밋했다.

## 4. 실제 검증 결과

실행 위치는 `/workspace/scratch/41ae7a55914b/agentflow-open`다. 요구한 `python -B -m workbench.session start af-res-069 --allow docs/workstreams/research/AF-RES-069/ --dependency work/research-af-res-065=18e4449eb0ac04464aee8fa6cc07f1f6a54d0b5d --output docs/workstreams/research/AF-RES-069/manifest.json --fetch`는 실제 종료0이며 [시작 영수증](https://github.com/laadkke-arch/agentflow-open/blob/fb710fce01052a5b907398e2da6840b59d3cfa08/docs/workstreams/research/AF-RES-069/evidence/session-start.json)에 있다.

연구 내용 SHA `0c3ab1c1c8359d3c5f85c8b9e51dc7119f8b2dec`의 첫 session check도 종료0이고 [전체 출력 영수증](https://github.com/laadkke-arch/agentflow-open/blob/fb710fce01052a5b907398e2da6840b59d3cfa08/docs/workstreams/research/AF-RES-069/evidence/session-check-result.json)에 있다. 검사 영수증을 커밋한 최종 결과 SHA **fb710fce01052a5b907398e2da6840b59d3cfa08**에서도 아래 검사를 다시 실행해 종료0을 확인했다. 이번 최종 검사의 핵심 원출력 필드와 전체 stdout 해시를 이 마지막 파일에 기록한다. 제품 실행 검사와 구분한다.

```json
{
  "command": "python -B -m workbench.session check docs/workstreams/research/AF-RES-069/manifest.json --fetch",
  "cwd": "/workspace/scratch/41ae7a55914b/agentflow-open",
  "tested_head_sha": "fb710fce01052a5b907398e2da6840b59d3cfa08",
  "started_utc": "2026-11-23T09:29:35.911923+00:00",
  "completed_utc": "2026-11-23T09:29:45.329560+00:00",
  "exit_code": 0,
  "status": "passed",
  "freshness": "remote_checked",
  "integration_commit": "dfe4c46e3e27629d44ff12ec2f613ba4e031c42e",
  "task_base_commit": "76b8c1d15812fbf91b879f8444fd188ae7445802",
  "scope_base_commit": "76b8c1d15812fbf91b879f8444fd188ae7445802",
  "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
  "changed_path_count": 76,
  "outside_paths": [],
  "unmerged_paths": [],
  "errors": [],
  "stderr": "",
  "stdout_sha256": "6c25c9a43b99efd1e737fe9c0e81591d6c4bae2da521302d883d6676a92ea7d9",
  "delivery_audit": {
    "command": "python -B docs/workstreams/research/AF-RES-069/evidence/verify.py",
    "exit_code": 0,
    "head_sha": "fb710fce01052a5b907398e2da6840b59d3cfa08",
    "check_count": 41,
    "failed_count": 0,
    "failures": []
  },
  "working_tree_clean_before_handoff": true
}
```

fetch 시 통합 HEAD는 **dfe4c46e3e27629d44ff12ec2f613ba4e031c42e**로 시작판에서 이동했다. 시작판·선행판을 바꾸거나 rebase하지 않았고, 계약 hash와 허용 경로 검사에 통과했다. 선행 remote는 `18e4449eb0ac04464aee8fa6cc07f1f6a54d0b5d` 그대로다.

최종 원격 확인은 GitHub connector의 exact-ref fetch_file로 실제 본문을 다시 얻어 수행했다. 로컬의 동등한 커밋 tree와 **17파일의 Git blob SHA 및 전체 문자 길이**를 비교하고, 원격 내용 자체에서 JSON/CSV/표를 다시 파싱했다. RESULT 표의 데이터 행은3/6/4/30/18, frame75행18열, judgments90행23열, source99행, 독립 산입26계보가 맞았다. 원격 수용 상태도 PARTIAL이다. 파일과 blob은 다음과 같다.

| 고정 결과판의 파일 | Git blob SHA |
| --- | --- |
| SCOPE.md | 2841230504ae9a179e844be03f32b4500f626b88 |
| frame.csv | 84373d6b85242ab4282a56771e1ce7d8c5b2497e |
| problems.jsonl | ff25ba065100699dac126dd5a0a7e7b444aef25a |
| queries.jsonl | e73e7f7a593e7338588e6b6b9946a03827aa91b8 |
| runs.jsonl | e091e5bc080f1d88ddee73b48f770de4262c1f00 |
| sources.jsonl | d88f78d008bb3b7929209f48eceb181edb90b0b2 |
| judgments.csv | 5f9b9ccdc7faf241d05f7bf0c1957d1919addcba |
| decisions.md | 00bd11272bc976a7cc67a0085d45bece6c9dbe6b |
| SELF_CHECK.md | ae3dc5bdabbcaa4954ad0c5bc2aa527f15137f71 |
| manifest.json | df89dc668a2e0953dca00fe59073683986791f2b |
| evidence/final-counts.json | c2b31e0fa45425b0dd4ae8763cc27eac6f82f792 |
| RESULT.md | 9c01a5f1ee74c3b25467154bc3a01f834bc6d365 |
| evidence/acceptance-evidence.json | 3205eb424ff1bc3ea67cdcdadc137e3da3c51d02 |
| evidence/delivery-audit-committed.json | cddecf454d6bb2d5a603f2be105e2019f6c437cb |
| evidence/result-claim-review.json | 25ad92d4a7ca5c54ea0c4979953c9248e35a487c |
| evidence/session-check-result.json | 47e6bd3908233cb63698a3c9b27d01a981535468 |
| evidence/result-remote-verification.json | 46252e9e5199b88b8e83a782491211015ac3d1f7 |

원격 검사 **8항목/실패0**, 확인 시각 **2026-11-23 09:30:02 UTC**. 앞선 내용 SHA의13파일 재열람은 [별도 영수증](https://github.com/laadkke-arch/agentflow-open/blob/fb710fce01052a5b907398e2da6840b59d3cfa08/docs/workstreams/research/AF-RES-069/evidence/result-remote-verification.json)에 있다. 최종17파일 대조는 위 SHA와 표에 기록했으며 이후 결과 파일은 바꾸지 않았다.

기록 오류도 보존했다. 과거 checkpoint의 JSONL 빈 줄4건은 감사 종료1 뒤 최종 봉인 전에 고쳤다. 후행 JSON 키 차이에 따른 대조 생성 종료1, source JSON 공백 재직렬화로 바이트 검사가 실패한 종료1도 삭제하지 않았다. source 값은 동일함을 확인한 뒤 봉인 바이트를 그대로 복원하여 append만 남겼다. 마지막41항목 검사는 모두 통과했다. 근거 범위보다 강했던 보고서 표현3곳도 수정·재열람했다.

**미실시/미확인:** 제품 통합·프로그램 회귀 실행·실물 Chime 조작·GUI 렌더링·초보자 시험0회. 최초 이슈 본문판, T0 정확한 모집 snapshot, GitLab bot flag, P3 댓글/이력, target revision 동일성, 원 개발자 채택·시간 절감·전체 웹 재현율은 미확인 또는 미측정이다.

## 5. 판단과 근거

### 관측 결과

- 관측층3짝, 엄격층0짝. 빈 엄격층에0%를 계산하지 않는다.
- 질의18, 원순위90, 최초 접근30. 직접 읽은 반환 원문은27 URL/18계보, 반환 합집합은76 canonical URL/52계보다.
- 원실험 독립 원저작25=선정 문제3+선별6+반환 신규16. 사후 FAA2문서를1관련 절차 계보로 보수적으로 추가해 최종26이다. 댓글/연결 PR/미러/재열람은 추가0이다.
- 확정 적합은 A만0/B만0/공통0/둘 다 미확정3. 미열람까지 전부 실패했다는 뜻이 아니다.
- 같은 질의·최초 접근 상한은 지켰지만 추가 접근 포함 비용은 **A25/B33**, 총58회다. 동일 비용 우열은 판단하지 않는다. FAA의 사후3연산은 원실험 밖이다.

### 실제로 얻은 것과 거부한 대응

P1에서 A는 CLI·설정층 시험 재료를, B는 무관한 기록 보존 문헌을 반환했다. 완료 표식이라는 일반 생각은 사전 노출이며, 사후 작성자 댓글과 PR19648에서도 이미 검토된 대안이었다. 더 직접적인 사후 PR를 A의 원실험 성공으로 넣지 않았다.

P2에서 A는 기존 Chime entity/action과 Mini/Hub-Pro 연결 차이를, B는 ID·능력·native 제어 및 중간 수락/실제 결과 분리라는 조건부 시험 관점을 제공했다. decision tree의 leaf를 물리 말단 기기로, 무선 동기화 유지와 고정 pairing 유지를 같은 것으로 읽는 후보는 거부했다. 실제 leaf setter·결과 계약은 얻지 못했다. 신고자의 기준일 전 Mini 반품은 open 이슈가 실제 진행 중인 채택 기회를 보장하지 않는 반례다.

P3에서 A가 찾은 TreeView의 숨김 설정과 제목·데이터 바인딩은 구체 수정 지점이다. 이것이 곧 e1e8684에서 작동한 해법은 아니다. B의 명확한 약칭/줄바꿈은 폭과 높이를 바꾸는 동종 UI 원리이며 대상 성공을 입증하지 않는다. ColumnView API를 TreeView에 바로 적용하거나 데이터 셀의 ellipsize를 머리글에 옮겨 말하지 않았다.

FAA의 실제 절차는 수신·의도·지시 확인과 실제 상태 근거를 구분하는 사후 보조 비교다. readback이라는 이름만으로 실제 getter와 같다고 보지 않는다. native 기능이 있으면 동종 부품이 더 직접적이며, 기능이 없으면 타분야 원리가 API를 만들어 주지 못한다. root가 봉인 뒤 고른 분야이므로 B 적중에는0으로 산입했다.

상세 원행·근거 절·반례는 [RESULT 표1~3와 Q1~Q8](https://github.com/laadkke-arch/agentflow-open/blob/fb710fce01052a5b907398e2da6840b59d3cfa08/docs/workstreams/research/AF-RES-069/RESULT.md), [자료 원장](https://github.com/laadkke-arch/agentflow-open/blob/fb710fce01052a5b907398e2da6840b59d3cfa08/docs/workstreams/research/AF-RES-069/sources.jsonl), [90행 판정 원장](https://github.com/laadkke-arch/agentflow-open/blob/fb710fce01052a5b907398e2da6840b59d3cfa08/docs/workstreams/research/AF-RES-069/judgments.csv), [질문별 근거·반례 연결](https://github.com/laadkke-arch/agentflow-open/blob/fb710fce01052a5b907398e2da6840b59d3cfa08/docs/workstreams/research/AF-RES-069/evidence/question-coverage.json)에 있다. 인용 지침 자체를 읽은 것과 그 지침이 인용한 원실험을 검증한 것을 구별했다.

### PARTIAL인 이유

최소20원저작과 기록·Git 검사 조건은 충족했지만 최초판/엄격층과 정확한 모집 증거, 동일 실제 비용, 대상판 적용 확인, 실제 진행 중인 원 개발자 선택의 근거가 부족하다. 원문을 더 읽었다는 이유로 이 공백을 완료로 처리하지 않았다. 조사자 명시 노출 이후의 새 문서·기능과 원 개발자에게의 새로움도 분리했다. P3 댓글은 공개 notes401/웹 DisabledError로 막혀 미확인으로 남겼다.

다른 세션과의 잠재 충돌은 통합 HEAD의 이동이다. 이 작업은 중앙 원장을 바꾸지 않고 시작 manifest를 유지했으며, 종료 직전의 실제 fresh check는 통과했다. 공개 자료와 연구자가 작성한 요약·메타데이터만 저장했고 인증정보·장치 비밀·비공개 대화는 저장하지 않았다. 원저작 전체를 복제하지 않고 직접 읽은 절과 허용되는 주장·한계를 남겼다.

## 6. 다음 대화의 첫 행동

1. `work/research-af-res-069`의 최신 SHA와 마지막 HANDOFF를 먼저 읽고, 검증 결과판 **fb710fce01052a5b907398e2da6840b59d3cfa08** 이후의 diff를 확인한다. 새 대화가 이 결과를 자동 기억한다고 가정하지 않는다.
2. 첫 구체 작업은 **선정된 원이슈의 최초 본문판·기준일 맥락 확인**이다. 입력은 P1 #19647, P2 #180207, P3 #13819, T0 `2026-11-23T08:24:37Z`, `problems.jsonl`의 body hash와 생성/갱신 시각이다. 동일 공개 원자료의 편집 이력 또는 정당하게 제공된 export를 관측본과 대조한다. 현재 body와 updated_at만으로 최초판을 선언하지 않는다. P2는 반품 이후 실제로 열린 설계 선택/시험 가능한 당사자가 있는지 날짜 있는 근거부터 확인한다.
3. 원자료를 얻지 못하면 엄격층은 비워 두고 PARTIAL을 유지한다. 미열람 후보를 후행으로 읽더라도 봉인된 A/B 순위·질의·실패·점수에 소급하지 않는다. 동일 비용 비교를 다시 할 경우 추가 line/find/screenshot까지 포함한 총예산과 새 문제·질의를 새로 봉인한다.
4. 제품 확인이 필요한 후속 범위에서는 아래 명령·입력을 사용한다. 실제 테스트 의존성이 준비된 별도 checkout/장치 환경이 필요하며 이번에는 실행하지 않았다. 전체 입력 행렬과 미확인 경로는 [resume-checks](https://github.com/laadkke-arch/agentflow-open/blob/fb710fce01052a5b907398e2da6840b59d3cfa08/docs/workstreams/research/AF-RES-069/evidence/resume-checks.md)에 있다.
5. 새 승인 요청을 기다리는 상태가 아니다. 현재 작업은 공개 읽기와 자기 경로 기록을 완료하고, 범위 밖 실제 제품/장치 검증과 접근 불가 원자료를 특정하여 부분 인계한다. 외부 당사자 연락이나 중앙 원장 변경은 수행하지 않는다.
6. 다른 세션 의존성은 AF-RES-065 HANDOFF의 고정판 한 건뿐이다.

재개 시 기록 검사 명령(저장소 root):

```sh
git rev-parse HEAD
python -B docs/workstreams/research/AF-RES-069/evidence/verify.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-069/manifest.json --fetch
git status --porcelain
```

미실시 제품 확인의 최소 명령·입력:

- **P1:** 별도 JupyterLab checkout HEAD=`f12cea5b7d7296fabfabcb362005763a879ae06f`, Python3.12/test 의존성 준비 후 그 root에서 `python -m pytest jupyterlab/tests/test_jupyterlab.py -k test_disable_extension_does_not_lock_it -q`. 추가 입력은 초기 빈 설정/구판 disabled/기존 lock=True, 새 프로세스, 같은·다른 설정 경로다. 이 PR test 하나가 모든 경계를 검증하지는 않는다.
- **P2:** `HA_CORE_CHECKOUT`에 외부 읽기 checkout 경로를 두고 `git -C "$HA_CORE_CHECKOUT" grep -n -i -E 'chime|volume' 2026.8.3 -- homeassistant/components/reolink`. 실제 입력은 Mini `v3.3.0.441_26022721`, Doorbell `v3.0.0.6543_26052720`, 고정 pairing과 정확한 Chime ID다. leaf setter가 아직 특정되지 않아 허구의 쓰기 endpoint 명령은 만들지 않았다. 첫 확인은 코드가 쓰는 dependency 판과 실제 명령 계약이다.
- **P3:** `git -C "$INKSCAPE_CHECKOUT" rev-parse 'e1e8684^{commit}'`, 이어 `git -C "$INKSCAPE_CHECKOUT" show e1e8684:src/ui/dialog/undo-history.cpp`, `"$INKSCAPE_BINARY" --version`과 GUI 실행. 입력은 원래 창 폭/높이·언어·글꼴·배율 및 연속 행동 묶음이다. Doxygen/1.4-6으로 target 판을 대신하지 않는다.
- **P3 댓글 원자료:** 공개 접근 재확인 명령은 `curl --fail-with-body --location 'https://gitlab.com/api/v4/projects/inkscape%2Finbox/issues/13819/notes?per_page=100&sort=asc&order_by=created_at'`. 이번 관측은401이다. 접근 불가가 유지되면 승인된 원자료 제공 환경을 특정하고 미확인으로 남긴다.

최종 결과의 약점3건과 결론을 바꿀 최소 관측은 RESULT 마지막 절에 있다. 새로 읽힌 유효 후보 한 건, 정확한 target 경계의 실행 성공 한 건, 또는 최초판/실제 진행 중 선택의 날짜 있는 증거 한 건은 해당 제한된 결론을 바꿀 수 있다. 현재 기록을 지우거나 원실험 성공으로 소급하는 근거는 아니다.

