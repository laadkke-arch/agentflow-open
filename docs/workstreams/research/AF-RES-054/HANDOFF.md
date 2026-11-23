# AF-RES-054 · HANDOFF

**판정: 부분 충족 · 부분 인계.** AF-RES-054#2는 원격 `c79740c29d972f6d350f4292c286a91fb20ab5a8`의 완료된 ①–③을 반복하지 않고 ④ 결과·검토·검증부터 이어서 저장했다. 원문·계산·질문별 답과 반증 기록은 갖췄지만 신규 자리·별도 개입 자료 배당·원 종점 원행 결손이 남았다. 완전 충족이나 주효과 입증으로 표시하지 않는다.

## 고정 결과와 이력

- 저장소/브랜치: `laadkke-arch/agentflow-open` / `work/research-af-res-054`
- **최종 고정 결과 SHA: `377facae73f5e49677cb5719a05fdac457d8357b`**
- 결과표·자체 검토 본문 커밋: `7171249fcea5a78f2563e290e2e089dfbef6c774`
- 계획 통합판: `d7e60daf1b5b2c918502c407982566369b7149e3`
- 실제 최초 시작판: `573a8f1a7cafa90b87bcbb4267e73fee12385bda`
- #2 재개 때 확인한 통합판: `921502a4c7729ca39d2a79319901725deecd48e5`
- 최종 check가 확인한 통합판: `243b29448790be6a01f653e649b1d4f3c69b4480`; 공통 계약 해시 유지.
- 의존 HANDOFF: AF-RES-050@`a3e13076e889dd49bfa7b7aa2fad6d149d874452`
- 읽은 050 결과판: `5797f9a9f1a1f0281d54c1922c6698a53093b67a`
- 모든 제출 경로: `docs/workstreams/research/AF-RES-054/`. `dot-control.json`과 공통 문서는 변경하지 않았다. 기존 브랜치·커밋을 초기화하거나 덮어쓰지 않고 자식 커밋으로 전진했다.

| 묶음 | 원격 SHA | 내용 |
| --- | --- | --- |
| ① 모집·종점·계산 규칙 | bea80dac12d7fe982319705b69b5744a8e7852c6 | 결과 열람 전 규칙·manifest·start |
| ①a 검색 문법 적응 | 1127a6f5a84f229f6cb417cd3fe111a6c3e8f8dc | native 문법 실패 후 동치 질의·한계 공개 |
| ①b 교육·설계 선정 동결 | 9cacf328e1ce325e15f1ab6cdd6da396216ea825 | E01/D01 metadata·노출·모집 한계 |
| ①c 소프트웨어 선정 동결 | c3c4eb6a7ccf2815202cc67c2a2cf25c94353e7c | S01–S03 선정·S04 공석 |
| ② 8자리·원문·분모 | de1e2b9b0110e1713715e932849d2b9a5c5e1b99 | 150열람 행·23저작·68metadata와8자리 |
| ③ 연결·정수 경계·반례 | c79740c29d972f6d350f4292c286a91fb20ab5a8 | 다른 단위의 실제 연결·6200정수조합·재현 |
| ④ 결과·자체 검토·재개 정정 | 7171249fcea5a78f2563e290e2e089dfbef6c774 | 두 표·Q1–Q7·수용 원장·229열람 행·부분 판정 |
| 검증 기록 | 377facae73f5e49677cb5719a05fdac457d8357b | 고정판 원격 재열람·session 실제 출력·게이트 판정 |
| 최종 인계 | 이 HANDOFF.md만 추가하는 마지막 자식 커밋 | 위 검증판을 다시 읽고 check한 후 작성; 자체 SHA는 커밋 이력에서 확인 |

수용 원장 A21은 검증판 시점에 `마지막 HANDOFF 단독 커밋 대기`다. 이 파일이 추가되는 마지막 커밋의 변경 경로가 HANDOFF.md 한 개라는 이력으로 완료를 증명한다. 마지막 커밋을 단독으로 유지하려고 수용 원장을 미리 성공으로 바꾸지 않았다.

## 두 표·원장 위치

| 산출물 | 위치·범위 |
| --- | --- |
| 표 1 | [RESULT.md](RESULT.md) 첫 제목,1–12줄: 기준2·새 소프트웨어4·교육1·CAD1의8자리 |
| 표 2 | RESULT.md 두 번째 제목,14–47줄: 조건·대비·결측30행 |
| Q1–Q7 | RESULT.md 51/59/71/89/127/135/168줄의 각 제목 |
| 마지막 약점3건 | RESULT.md 261줄부터. 이 인계서 마지막 표에 동일하게 보존 |
| 선정·종점·연결·경계 | [frame.csv](frame.csv)76행=68metadata+8자리; [endpoints.csv](endpoints.csv)19행; [joins.csv](joins.csv)10행; [bounds.csv](bounds.csv)34행 |
| 손계산·재실행 | [reproduce.md](reproduce.md): 실제 eXoaDocs와 구성 반례, 정확한 명령·입력 해시 |
| 원문 기록 | [sources.jsonl](sources.jsonl)229행; [source-index.csv](evidence/source-index.csv); [source-counts.json](evidence/source-counts.json) |
| 계약·범위 | [manifest.json](manifest.json), [SCOPE.md](SCOPE.md), [PROGRESS.md](PROGRESS.md) |
| 자체 검토·수용 | [SELF_CHECK.md](SELF_CHECK.md), [acceptance-evidence.json](evidence/acceptance-evidence.json) |
| 재개 입력·정정 | [resume-inputs.json](evidence/resume-inputs.json), [resume-review-resolutions.json](evidence/resume-review-resolutions.json), streams/resume-*/review.md |
| 실제 검사 | [resume-validation-execution.json](evidence/resume-validation-execution.json), [deliverable-check.json](evidence/deliverable-check.json), [remote-reopen.json](evidence/remote-reopen.json), [session-check.json](evidence/session-check.json), 아래 최종판 영수증 |

## 핵심 결과

**목표 공동 종점을 공개 원행에서 직접 계산한 연구는 확보0건이다.** 분모는 이름 있는6연구/계획8자리이며 연구의 자료 확보 개수다. 참가자의 공동 성공을0으로 관측했다는 뜻이나 전 분야의 공개율이 아니다. S04/D01은 빈 자리이고, Casdoc은 선정 후 별도 배정 대비가 없음을 확인했다. 새6자리 중 이름 있는4, 실제 배정 비교3을 구분한다.

**저자가 같은 제한시간·정확성 교집합을 명시한 경우는 eXoaDocs B02다.** 40분 안 네 java.sql 과제를 모두 정확히 완료한 저자 집계는3/12 대1/12이며, 표본의 산술 차이는 `1/6=+16⅔%p`다. 공개 개인 원행을 재계산한 값이나 신뢰구간·모집단 주효과 입증은 아니다. 과제3만의3/12 대4/12는 다른 종점이라 반대 방향이 동시에 성립한다. [원문][exoa] §5.3.2/Table XII.

정확한 동일-N 주변수만 있을 때 `max(0,q+t−N)≤x≤min(q,t)`를 적용한다. 현재 선정 연구에서 두 실측 주변수만으로 새 비자명1차 구간을 얻은 사례는 없었다. 가상 `N10,q8,t9` 대 `N10,q8,t8`는 `[−10,+20]%p`를 허용한다. 각 정수 극단표를 제시했으며 관측 연구값으로 바꾸지 않았다. B02의 t3–12/1–12는 x=q만 넣은 약한 조건부 외피다. 부분 정답 제출을 같은40분 제출 사건에 연결하면 하단 t11/10이 필요하다는 감도를 함께 남겼다.

다른 자료에서 실제 확인한 연결은 Newton24개 사람×조건의 파일/응답 존재, Casdoc122검색 조각, 표본 밖 Pillai112분석행이다. 이들을 배정×시각×최종품질 공동 행으로 승격하지 않았다. Blueprint 순위형 품질에 새 통과선을 붙이지 않았고, Newton 완료6/4는 원 판정식·제출 정의가 부족한 보조 종점으로 보존했다. DesignPatternDoc의 더 짧은6단계 합계는 원 채점 대상의 분실·강제 마감 미확인 때문에 동등 품질 총시간이 아니다.

## 원문 배당과 부분 판정

| 요건 | 실측 | 판정 |
| --- | --- | --- |
| 고유1차 저작 최소22 |23 | 총수 충족;229열람/접근 행과 구별 |
| 새 원연구 논문6 | 선정4+진단4=8열람 | 열람 총수 충족; 적격 신규 배정 비교3/6. 진단을 빈 자리에 대체하지 않음 |
| 기준 원논문2 |2 | 충족 |
| 별도 저자 연구자료4 |6 | 충족; 같은 패키지 내부 CSV/README/과제지는 재산입하지 않음 |
| 별도 개입·과제·루브릭4 |1 | 미달. 독립 도구 repo1개이며 실험 바이너리 동일성도 미확인 |
| 원 방법4 |4 | 충족 |
| 사전등록·직접복제 출판물2 |2 | Urry2021 및 Bichler2026 분석 복제. 후자는2016/2022 분석을 E01의115명에 적용해 E01과 참가자 중복 |
| 신규6자리 | 이름 있는4, 적격 배정 비교3 | S04/D01 공석, S03 대비 부적격 |
| 모집 재현 | 일부 검색 이력·native 질의 동등성 제한 | SCOPE R1a/R1b와 search-audit에 공개; 전수·완전무노출 주장 없음 |

별도23저작이라는 합계가 개입 자료1/4나 빈 자리를 보완하지 않는다. 최종 출판본·정오표를 읽지 못한 E01 사전평균4.75 대 SAV4.573275862 불일치는 원인 미확인으로 유지했다. 최종 출판본의 오류라고 단정하지 않는다.

## 재개 검토의 변경과 검증 범위

- 이전 root151행에 빠졌던 동일 DOI 접근15행과 재개 조사자·편집자의 확인63행을 합쳐229행으로 맞췄다. 같은 저작 재열람·실패이므로 고유23은 유지했다.
- Casdoc은13명 모두에게 선택 연장을 제안했고3명이 사용했다. 원장도 맞췄으며2400초를 강제 deadline 대신 계획시간으로 분리했다.
- Newton 로그의33.0–68.3분은 timestamp 최대−최소 범위로 명시했다. 새 과제 시계나 최종 제출시간이 아니다.
- 구성 패턴표가 만족하는 범위를 Table XII/§5.3.2 제약으로 한정했다.
- 신규 논문 열람 수와 적격 표본 배당, Bichler 분석 복제와 참가자 재사용을 분리했다.

검토자는 root와 별도 assistant 세 명(baseline_review/software_review/acceptance_review)이다. 각 검토의 입력 해시·읽은 원문·미확인을 보존했다. 외부 사람 심사·독립 참가자 실험·독립 원논문 재현으로 보고하지 않는다.

실제 산술 검산은6,200개 정수 q/t 조합, eXoa 네 과제 구성표와 대비를 확인했다. 문서 검사는 두 필수 표,7질문,3약점,모든 source ID와 stream 합집합,수용 원장의 source 행/제목 위치,허용 경로와 링크를 확인했다. 새 사람 모집, 저자 연락, 연구 도구/참가자 코드 실행, 공개되지 않은 원행 연결, 원래 없는 통과선·개인 인과효과·신뢰구간 계산은 미실시다.

## 막힌 이유와 다음 첫 행동

**다음 첫 행동은 Newton의 동일12명 실험판에서 원래 기능적 완료 판정식과 최종 제출 사건을 확인할 수 있는 파일을 찾는 것이다.** 이미24개 조건 단위의 파일/응답 연결은 있으므로, 먼저 [저자 패키지](https://zenodo.org/records/10459420)의 기존 판 이후 공개판·파일 목록에서 `participant,task,condition,period,task_start,final_submit,original_pass,overrun_or_withdrawal` 및 원 completion checklist/codebook이 추가됐는지 확인한다. 기존 로그 timestamp나 notebook 존재만으로 채우지 않는다. 아직 확인되지 않은 파일명을 실제 존재하는 실행 입력처럼 만들지 않는다.

그 다음 최소 재개 자료는 연구별로 다르다.

| 대상 | 필요한 최소 자료·행동 | 자료 확보 전 제한 |
| --- | --- | --- |
| B01 | 기존 품질 기준이 이진 판정을 실제로 포함했는지와20명 완료·채점 원장의 공통키 | 순위에서 사후 pass를 만들지 않음 |
| B02 |24명 배정/제출/기능검사 원장과 시간표 포함지시자 | 저자3/1을 원행 재현이라고 부르지 않음 |
| S02 | 원 강제 종료·초과 처리 규칙,21명 ID 연결표,복구된 코드/도표·과제 검증 결과 | 시간 셀 완전성을 품질 pass로 바꾸지 않음 |
| S03 | 과제별 성공/연장 원장은 기술적 완료를 위해 유용; 형식 배정 대비는 원 설계에 없음 | 파일 복구로 존재하지 않은 배정 대비를 만들지 않음 |
| E01 | 원 배정·제외 대장,검사 제출시각,원고/최종본/정오표·SAV 판 대응 | 원래 없는26점 pass선을 새로 붙이지 않음 |
| S04/D01·개입 자료 | 결과를 보기 전 새로운 metadata 탐색 범위·정렬·상한을 먼저 동결하고 적격 공개 패키지·독립 자료 확인 | 현재 공석을 진단 연구로 소급 교체하지 않음 |

E01 판 대응의 구체적인 첫 URL은 `https://psycnet.apa.org/journals/edu/112/7/1320.pdf`이고 입력은 DOI `10.1037/edu0000433`, `Cond=0,TimeP=0,KPre`, 원고 TableB2의4.75와 SAV평균4.573275862다. [final-version-check.md](streams/crossdomain/final-version-check.md)에 실패한 공식/기관 URL·단계·필요한 판을 남겼다.

기존 집계/경계를 재현하는 명령은 다음과 같다. 저장소 루트에서 실행하고 새 출력 시각과 기존 영수증을 구별한다.

```sh
python -B docs/workstreams/research/AF-RES-054/fetch_inputs.py --download
python -B docs/workstreams/research/AF-RES-054/calculate_bounds.py
python -B docs/workstreams/research/AF-RES-054/build_ledgers.py
python -B docs/workstreams/research/AF-RES-054/validate_deliverables.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-054/manifest.json --fetch
```

정적 파일 감사의 세부 명령·입력 SHA256·필요 라이브러리는 reproduce.md §6과 각 stream 재현문서에 있다. 새 원행을 얻으면 배정키 유일성→1:N 이벤트 집계→배정표 왼쪽 결합→전후 수/미연결/철회/실패/결측→x와 주변 경계의 일치를 이 순서로 확인한다.

**색인 제안:** AF-RES-054 | 제한시간 내 정확 완료의 공개기록 식별 감사 |8자리·23저작·목표 원행 직접계산0·저자 공동집계1·자료배당 부분 | RESULT.md / HANDOFF.md. 공통 색인 변경은 이 작업에서 하지 않았다.

## 최종 고정판 원격 재열람

아래는 검증 기록까지 포함한 최종 결과판의 실제 재열람이다. 두 파일의 전체 반환 내용이 게시 내용과 동일했다. 이전717판 영수증과 구별한다.

```json
{
  "result_commit": "377facae73f5e49677cb5719a05fdac457d8357b",
  "checked_utc": "2026-11-23 02:45:10 UTC",
  "files": [
    {
      "file": "RESULT.md",
      "git_blob_sha": "91ed4ae996761394518c6c63a73479006ba364d2",
      "url": "https://github.com/laadkke-arch/agentflow-open/blob/377facae73f5e49677cb5719a05fdac457d8357b/docs/workstreams/research/AF-RES-054/RESULT.md",
      "characters": 29745,
      "exact_content_match": true
    },
    {
      "file": "evidence/acceptance-evidence.json",
      "git_blob_sha": "92da78e087813f66b6d3b7a2edc2e94c29dac3c7",
      "url": "https://github.com/laadkke-arch/agentflow-open/blob/377facae73f5e49677cb5719a05fdac457d8357b/docs/workstreams/research/AF-RES-054/evidence/acceptance-evidence.json",
      "characters": 24497,
      "exact_content_match": true
    }
  ],
  "status": "passed"
}
```

## 최종 고정판 session check 실제 출력

명령: `python -B -m workbench.session check docs/workstreams/research/AF-RES-054/manifest.json --fetch`

시작 UTC: `2026-11-23T02:45:10.842758+00:00`; 종료 UTC: `2026-11-23T02:45:18.391325+00:00`; **exit_code: 0**. stderr는 빈 문자열이다. 이는 Git 계약·허용 경로·원격 최신성 검사이며 과학적 주효과 검증이 아니다. 아래 stdout 전체가 최종 결과SHA에 대한 실행 증거다. 이후 HANDOFF 단독 커밋을 이 검사에 포함됐다고 소급하지 않는다.

```json
{
  "status": "passed",
  "task_id": "af-res-054",
  "freshness": "remote_checked",
  "checked_at": "2026-11-23T02:45:18.381213+00:00",
  "checked_out_commit": "377facae73f5e49677cb5719a05fdac457d8357b",
  "task_base_commit": "573a8f1a7cafa90b87bcbb4267e73fee12385bda",
  "integration_commit": "243b29448790be6a01f653e649b1d4f3c69b4480",
  "scope_base_commit": "573a8f1a7cafa90b87bcbb4267e73fee12385bda",
  "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
  "changed_paths": [
    "docs/workstreams/research/AF-RES-054/.gitignore",
    "docs/workstreams/research/AF-RES-054/PROGRESS.md",
    "docs/workstreams/research/AF-RES-054/RESULT.md",
    "docs/workstreams/research/AF-RES-054/SCOPE.md",
    "docs/workstreams/research/AF-RES-054/SELF_CHECK.md",
    "docs/workstreams/research/AF-RES-054/bounds.csv",
    "docs/workstreams/research/AF-RES-054/build_ledgers.py",
    "docs/workstreams/research/AF-RES-054/calculate_bounds.py",
    "docs/workstreams/research/AF-RES-054/endpoints.csv",
    "docs/workstreams/research/AF-RES-054/evidence/acceptance-evidence.json",
    "docs/workstreams/research/AF-RES-054/evidence/analysis-execution.json",
    "docs/workstreams/research/AF-RES-054/evidence/bundle2-files.json",
    "docs/workstreams/research/AF-RES-054/evidence/bundle3-files.json",
    "docs/workstreams/research/AF-RES-054/evidence/calculation-check.json",
    "docs/workstreams/research/AF-RES-054/evidence/calculation-execution.json",
    "docs/workstreams/research/AF-RES-054/evidence/deliverable-check.json",
    "docs/workstreams/research/AF-RES-054/evidence/final-calculation-execution.json",
    "docs/workstreams/research/AF-RES-054/evidence/input-fetch-check.json",
    "docs/workstreams/research/AF-RES-054/evidence/ledger-build-check.json",
    "docs/workstreams/research/AF-RES-054/evidence/pilot-query.json",
    "docs/workstreams/research/AF-RES-054/evidence/remote-reopen.json",
    "docs/workstreams/research/AF-RES-054/evidence/resume-inputs.json",
    "docs/workstreams/research/AF-RES-054/evidence/resume-review-resolutions.json",
    "docs/workstreams/research/AF-RES-054/evidence/resume-validation-execution.json",
    "docs/workstreams/research/AF-RES-054/evidence/resume-workspace.json",
    "docs/workstreams/research/AF-RES-054/evidence/review-resolutions.json",
    "docs/workstreams/research/AF-RES-054/evidence/session-check.json",
    "docs/workstreams/research/AF-RES-054/evidence/session-start.json",
    "docs/workstreams/research/AF-RES-054/evidence/source-counts.json",
    "docs/workstreams/research/AF-RES-054/evidence/source-index.csv",
    "docs/workstreams/research/AF-RES-054/evidence/study-register.json",
    "docs/workstreams/research/AF-RES-054/fetch_inputs.py",
    "docs/workstreams/research/AF-RES-054/frame.csv",
    "docs/workstreams/research/AF-RES-054/joins.csv",
    "docs/workstreams/research/AF-RES-054/reproduce.md",
    "docs/workstreams/research/AF-RES-054/sources.jsonl",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/bounds.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/calculate_baseline.py",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/calculation-execution.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/calculation-output.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/endpoints.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/findings.md",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/joins.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/ledger-review.md",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/method-bibliography-check.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/result-review.md",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-balke.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-bichler-ffp-lmu.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-bichler-prereg.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-bichler2020-original.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-bichler2020.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-blueprint.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-brandt-dissertation.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-crossref-bichler.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-exoa.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-frangakis-xml.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-frangakis.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-imbens.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-lee.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-manski.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-osf-czsrp-node.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-osf-dx6qv-files.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-osf-dx6qv-node.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-osf-dx6qv-registration.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-osf-dx6qv-registrations.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-osf-dx6qv-wikis.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-rubin.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/retrieval-urry.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/root-review.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/root-review.md",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/source-counts.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/sources.jsonl",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/stream-validation.json",
    "docs/workstreams/research/AF-RES-054/streams/baseline-methods/studies.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/audit-crossdomain-receipt.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/audit_crossdomain.py",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/bichler-analysis-aggregate.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/bichler-data-schema-audit.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/bichler-metadata.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/bounds.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/dependency-install-receipt.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/education-linkage-metadata.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/endpoints.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/final-version-check.md",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/findings.md",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/frame.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/integration-review.md",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/joins.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/native-search-attempts.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/native-search-followup.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/osf-link-metadata.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/osf-screen-filelists.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/osf-screen-relations.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/osf-title-metadata.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/pillai-analysis-aggregate.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/postfreeze-fetch-receipts.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/postfreeze-fetch-receipts2.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/postfreeze-fetch-receipts3.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/postfreeze-fetch-receipts4.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/reproduce.md",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/result-review.md",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/search-audit.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/selection-preliminary-superseded.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/selection.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/self-check.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/source-counts.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/sources.jsonl",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/studies.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/web-search-records.json",
    "docs/workstreams/research/AF-RES-054/streams/crossdomain/zenodo-metadata.json",
    "docs/workstreams/research/AF-RES-054/streams/resume-acceptance/review.md",
    "docs/workstreams/research/AF-RES-054/streams/resume-acceptance/sources.jsonl",
    "docs/workstreams/research/AF-RES-054/streams/resume-baseline/review.md",
    "docs/workstreams/research/AF-RES-054/streams/resume-baseline/sources.jsonl",
    "docs/workstreams/research/AF-RES-054/streams/resume-root/sources.jsonl",
    "docs/workstreams/research/AF-RES-054/streams/resume-software/review.md",
    "docs/workstreams/research/AF-RES-054/streams/resume-software/sources.jsonl",
    "docs/workstreams/research/AF-RES-054/streams/root/audit-casdoc-execution.json",
    "docs/workstreams/research/AF-RES-054/streams/root/audit_casdoc.py",
    "docs/workstreams/research/AF-RES-054/streams/root/casdoc-audit.json",
    "docs/workstreams/research/AF-RES-054/streams/root/casdoc-download-receipt.json",
    "docs/workstreams/research/AF-RES-054/streams/root/intervention-read-receipt.json",
    "docs/workstreams/research/AF-RES-054/streams/root/sources.jsonl",
    "docs/workstreams/research/AF-RES-054/streams/software/.gitignore",
    "docs/workstreams/research/AF-RES-054/streams/software/audit-execution.json",
    "docs/workstreams/research/AF-RES-054/streams/software/audit_software.py",
    "docs/workstreams/research/AF-RES-054/streams/software/bounds.json",
    "docs/workstreams/research/AF-RES-054/streams/software/casdoc-download.json",
    "docs/workstreams/research/AF-RES-054/streams/software/designpattern-access-retries.json",
    "docs/workstreams/research/AF-RES-054/streams/software/endpoints.json",
    "docs/workstreams/research/AF-RES-054/streams/software/findings.md",
    "docs/workstreams/research/AF-RES-054/streams/software/frame.csv",
    "docs/workstreams/research/AF-RES-054/streams/software/frame.json",
    "docs/workstreams/research/AF-RES-054/streams/software/fulltext-downloads.json",
    "docs/workstreams/research/AF-RES-054/streams/software/fulltext-retries.json",
    "docs/workstreams/research/AF-RES-054/streams/software/further-downloads.json",
    "docs/workstreams/research/AF-RES-054/streams/software/joins.json",
    "docs/workstreams/research/AF-RES-054/streams/software/newton-tool-receipt.json",
    "docs/workstreams/research/AF-RES-054/streams/software/newton-woz-receipt.json",
    "docs/workstreams/research/AF-RES-054/streams/software/result-review.md",
    "docs/workstreams/research/AF-RES-054/streams/software/retrieval-receipts.json",
    "docs/workstreams/research/AF-RES-054/streams/software/schema-audit.json",
    "docs/workstreams/research/AF-RES-054/streams/software/search-log.json",
    "docs/workstreams/research/AF-RES-054/streams/software/selection.json",
    "docs/workstreams/research/AF-RES-054/streams/software/self-check.json",
    "docs/workstreams/research/AF-RES-054/streams/software/sources.jsonl",
    "docs/workstreams/research/AF-RES-054/streams/software/stream-validation.json",
    "docs/workstreams/research/AF-RES-054/streams/software/studies.json",
    "docs/workstreams/research/AF-RES-054/validate_deliverables.py"
  ],
  "outside_paths": [],
  "unmerged_paths": [],
  "errors": [],
  "boundary": "Git contract and ownership checks; not a new AI chat or product verification"
}
```

[exoa]: https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf
[dp-paper]: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11419627/fullTextXML?format=xml
[bichler]: https://www.researchgate.net/profile/Sarah-Bichler/publication/337692670_How_working_memory_capacity_and_shifting_matter_for_learning_with_worked_examples-A_replication_study/links/5e2e966292851c6af5452cf7/How-Working-Memory-Capacity-and-Shifting-Matter-for-Learning-With-Worked-Examples-A-Replication-Study.pdf
[bichler-data]: https://osf.io/mykxc/

## 가장 중요한 불일치·약점 3건

| 불일치·약점 | 영향받는 주장 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀔 조건 |
| --- | --- | --- | --- | --- |
| **모집·배당의 불완전성:** S04/D01 빈 자리, S03 배정 대비 부적격, 별도 개입 자료1/4, 일부 보조 질의 이력 결손 | “여섯 신규 적격 연구를 모두 확보했고 엄격 배당·모집 재현을 완전히 충족했다”는 주장 | [frame.csv](frame.csv) SLOT-S03/S04/D01; [source-counts](evidence/source-counts.json); [검색 감사](streams/crossdomain/search-audit.json); RT-02 | 결과를 보지 않은 새 metadata 모집 범위·검색문법/순서를 먼저 동결하고, 적격 공개 패키지·독립 자료를 확인 | 규칙에 맞는 추가 자리와 별도 자료, 빠진 검색 기록을 확보하거나 범위를 명시적으로 새로 승인한 후속 연구일 때만 완전성 재판정 |
| **원 종점·분모·연결자료 부족:** B02 저자 교집합 외에 목표 원행 직접 계산 없음. Blueprint/E01 통과선 부재, Newton 판정·제출 정의 미확인, DesignPattern 검증 대상 분실, Casdoc 대비 부재 | 제한시간 내 정확 완료율 개선, 동일 품질 전원 총시간, 설명 단독 효과 | [joins.csv](joins.csv) B01-J1/B02-J1/S01/S02/S03/CD-J01; [원문][exoa] §5.3.2; [분실 보고][dp-paper] Data collection | 같은 코호트의 원 기준/배정·제외·제출·채점 원장과 공통키를 먼저 확보. 설계에 없는 대비는 파일 복구로 만들지 않음 | 원래 사건과 분모가 존재하고 실제 연결이 확인되면 직접 계산/더 좁은 범위로 승격; 새 기준이면 후속 제안으로만 구분 |
| **E01 저자 원고와 공개 데이터의 사전평균 불일치:** 무압박 문제풀이58명에서 원고4.75 대 SAV4.573275862 | 해당 표의 사전점수·증가량을 동시에 정확히 재현했다는 주장; 판 혼합의 위험 | [읽은 저자 원고][bichler] Appendix B Table B2, CD-P01-VIS; [SAV][bichler-data] Cond0/TimeP0/KPre, CD-D01; [집계](streams/crossdomain/bichler-analysis-aggregate.json) | 최종 출판본 해당 표·정오표와 OSF file-version 기록을 먼저 대조 | 동일 최종판·코호트·열 정의가 확인되거나 수정판이 불일치를 설명할 때 변경. 현재는 최종 출판본의 확정 오류라고 단정하지 않음 |
