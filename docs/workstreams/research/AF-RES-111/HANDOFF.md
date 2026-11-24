# AF-RES-111 최종 인계

**PARTIAL.** 관측 모집틀에서 6사건을 골라 36요청×2방식 **72/72**를 실행했다. 학습에 쓰지 않은 원자료 24개의 배당은 원 요청 6, 공식 문서·구현 8, 별도 회귀·반대 6, 타 분야 4다. ExifTool 원포럼의 전체 생성순과 FreeCAD 이관 기록의 원시각·검색 상한 밖 순서가 미확인이라 모집 수용 조건은 미달이다. 주 실행 공석은 0이다. [결과](RESULT.md) · [모집](frame.csv) · [원 출처](sources.jsonl) · [수용 증거](evidence/acceptance-evidence.json)

어순 교환 6/6에서 A·B 후보와 근거 ID가 이어졌다. 동의어 말바꿈 6건에서 조건과 근거의 완전 정합은 양쪽 0/6이다. 반대·범위·누락 18변형의 잘못된 승계는 A 7건, B 5건이고 오지지는 A 2건, B 4건이다. 두 방법 모두 필수조건 하나의 지지를 전체 확정으로 승격하지 않았다. Gallim 교정에서는 두 후보 ID와 발견 절이 같았고 Paperless의 직접 인용이 1→0, 상태가 제외→보류로 바뀌었다. [교정](evidence/calibration.json) · [판정과 간선](runs.jsonl) · [검산 분모](evidence/verification.json)

## 식별과 저장

저장소 `laadkke-arch/agentflow-open`, 작업 `work/research-af-res-111`, Codex Cloud 실행이다. 계획판 `c40ef7723d851b628233bfb60dff8dfd292385cf` 뒤 원격에서 확인한 `9bf49108116e4f68e348869c2687ba36a30dc012`로 작업 브랜치를 만들었다. manifest를 생성할 때 통합 head는 `0bcaf7c90f3324447fd1b8bf12c514187ca4776b`였다. 격차는 중앙 진행표에 국한됐고 두 시작점의 AF-RES-111 행은 같았다. 운영 선행은 AF-RES-107의 [인계](https://github.com/laadkke-arch/agentflow-open/blob/54fccba38c764032f9ecc5fac5a676a9e2a898f5/docs/workstreams/research/AF-RES-107/HANDOFF.md), 연구 입력은 그 [검사 결과](https://github.com/laadkke-arch/agentflow-open/blob/8ae7aad97c7a4e958cdfe078ff49262b3717874e/docs/workstreams/research/AF-RES-107/RESULT.md)와 실행·요소 원장이다. 원형은 `fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c`로 고정했다. [범위](SCOPE.md) · [manifest](manifest.json)

검사 결과 SHA `cf01f72e7b9837661efc3a70bb29ef924a52ad29`. 2026-11-24 02:24 UTC에 새 GitHub checkout에서 해당 판의 35파일을 읽어 커밋 blob과 바이트를 대조했다. GitHub 커넥터로 RESULT·재현 절차·대표 근거/원장 등 10파일을 해당 SHA에서 추가로 읽었다. 첫 세 표를 36/72/17행으로 재생성했고 공개 원문 10곳의 28 구간을 모두 다시 확인했다. 작업자와 별도 세션에서 36요청을 작성했고 다른 별도 세션에서 출판 전에 36행 gold를 봉인했다. 인계 판단과 코드는 본 Codex Cloud 실행이다. [봉인](evidence/gold-seal.json) · [고정 결과판](https://github.com/laadkke-arch/agentflow-open/tree/cf01f72e7b9837661efc3a70bb29ef924a52ad29/docs/workstreams/research/AF-RES-111)

| 묶음 | GitHub 커밋 | 커밋 UTC와 확인 범위 |
| --- | --- | --- |
| ① 계약·규칙·교정 | [cdfa681cc9912ce2c07c85df6763659085bf9624](https://github.com/laadkke-arch/agentflow-open/commit/cdfa681cc9912ce2c07c85df6763659085bf9624) | 01:46:23 · manifest/규칙/교정 · 원격 반영 |
| ① 모집 원장 | [16fd307f6a078b11a30ba8b7d2d1c94ddd16cf40](https://github.com/laadkke-arch/agentflow-open/commit/16fd307f6a078b11a30ba8b7d2d1c94ddd16cf40) | 01:58:57 · frame과 원자료 후보 · 원격 반영 |
| ② 사실·변형 | [e1d3b3faf5cc6dc78caadb7d0dd1fee909020c04](https://github.com/laadkke-arch/agentflow-open/commit/e1d3b3faf5cc6dc78caadb7d0dd1fee909020c04) | 02:01:34 · 사실·요청과 독립 판독 입력 · 원격 반영 |
| ② gold 봉인 | [fd8ea92a0ebdcbd2f809a9137a39d7261dbf9f12](https://github.com/laadkke-arch/agentflow-open/commit/fd8ea92a0ebdcbd2f809a9137a39d7261dbf9f12) | 02:14:30 · 블라인드 gold·실행 입력 지문 · 02:14:41 실행 전 원격 확인 |
| ③ 두 방식·수명주기 | [9ce56e5260f73ee56020147d747fa47bb9fbcb0b](https://github.com/laadkke-arch/agentflow-open/commit/9ce56e5260f73ee56020147d747fa47bb9fbcb0b) | 02:15:14 · 72판정·192간선·10상태, 2회 재생 자료 · 원격 반영 |
| **④ 검사 결과** | [cf01f72e7b9837661efc3a70bb29ef924a52ad29](https://github.com/laadkke-arch/agentflow-open/commit/cf01f72e7b9837661efc3a70bb29ef924a52ad29) | 02:23:15 · RESULT/SELF_CHECK/재현·검산 · 02:24 원격 재열람과 검사 |
| 검사 후 영수증 | [cb5b62db2f28f34ef499b48948409f757f4f27f3](https://github.com/laadkke-arch/agentflow-open/commit/cb5b62db2f28f34ef499b48948409f757f4f27f3) | 고정 결과 검사 후 영수증·수용표 · 원격 확인 |
| 인계 | 이 파일만 추가한 최종 커밋 | 고정 결과와 영수증 원격 확인 뒤 저장 |

경로별 묶음과 원격에서 재확인한 시각은 [커밋 영수증](evidence/commit-files.json)에 있다. 검사 기준과 검사 후 영수증은 별도 커밋이다.

## 실제 검사와 예외

검사 주체는 본 Codex Cloud 실행자이고, Linux x86-64, Python 3.12.14, SQLite 3.53.1에서 실행했다. 아래 명령의 대상은 원격 결과판 `cf01f72…`의 깨끗한 detached checkout이다. [명령·시각·stdout·stderr 지문](evidence/remote-checks.json) · [재생 입력](reproduce.md)

| 실제 명령 | UTC · 종료값 · 관측 |
| --- | --- |
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-111/manifest.json --fetch` | 02:24:42–45 · 0 · 작업 한 건 명시 검사. `remote_checked`. manifest 제외 변경 34, 범위 밖·미병합 0. |
| `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 02:24:45–50 · 0 · doctor, 공통·lab 55+7+9, discovery, original-smoke 통과. 공통 자동 발견은 0건, `not-executed/no_active_sessions`. |
| `python -B docs/workstreams/research/AF-RES-111/tools/run.py --out <새출력>` 2회 | 02:24:50–51 · 양쪽 0 · 결과판에서 새 파일 SQLite로 2회. 최초 작성 시의 2회 및 고정 결과의 2회를 구분했다. 다섯 원장 바이트 일치. |
| `python -B docs/workstreams/research/AF-RES-111/tools/verify.py --replay <새출력1> --replay <새출력2>` | 02:24:51 · 0 · 72판정·192간선·10수명주기, 원문/사용 근거·FK 대조 성공. |
| `python -B docs/workstreams/research/AF-RES-111/tools/tables.py` 및 `check_captures.py --out <글로벌 임시 경로>` | 02:24:51–55 · 양쪽 0 · 표 36/72/17행과 끝 세 행, 공개 원위치 28/28 재확인. |

같은 키 재시도와 현재 판정 변경을 별도로 확인했다. 이전 답 `6b6900a71eba…`와 인용 `565ec63b00d5…`는 유지됐다. 다른 요청판에 같은 키를 쓰면 행수 변화 0과 오류였다. 주석 철회는 새 답 `b383e2cf213a…` 및 새 인용 `650ce53da3f6…`, 재확인 작업 2행으로 이어졌다. 다른 프로젝트의 같은 후보는 새 context를 사용했고 이전 프로젝트 context를 붙이는 삽입은 FK가 막았다. [수명주기 원장](lifecycle.csv)

## 미확인과 다음 첫 행동

F는 rsync 3개, D는 Inkscape 3개다. ExifTool·FreeCAD의 판 명시 원 구현까지 열었고 이 도구의 자연 요청이 먼저 있었는지 전체 원포럼/이관 경로는 미확인이다. F2·F3의 실제 신고 설치판과 D3 입력 첨부 및 Windows 재생도 미확인이다. 작업 비교와 골드의 실제 독립성·자료 하한을 충족했다. 관측 모집틀의 불완전성으로 최종 수용은 PARTIAL이다. [모집 원장](frame.csv) · [자가점검](SELF_CHECK.md)

다음 첫 행동은 이 인계의 부모와 검사 결과 SHA를 고정한 뒤 [모집 검색 파라미터](evidence/recruitment.json)의 F 어구를 2021-01-01부터 F3의 2022-04-02까지 [ExifTool 공개 원포럼](https://exiftool.org/forum/)의 날짜순 원자료에서 다시 대조하는 것이다. 공개 접근이 가능한 경우에만 각 첫 적격 사건과 순번을 별도 층에 기록한다. FreeCAD는 [원 Mantis 제출](https://tracker.freecad.org/view.php?id=4641)의 시각, 동일 날짜 원 ID와 이관 순서부터 확인한다. 현재 판정 재현은 [명령과 입력](reproduce.md)을 사용한다.

색인 제안 · AF-RES-111 · PARTIAL · 원문·어순에서 근거 유지, 동의어·범위·극성에서 보류 및 오승계 · 6 사건, 24 원자료, 72/72 실행 · [검사 결과](https://github.com/laadkke-arch/agentflow-open/blob/cf01f72e7b9837661efc3a70bb29ef924a52ad29/docs/workstreams/research/AF-RES-111/RESULT.md)

| 불일치·약점 | 다음 조사·직접 열 자료 | 어느 관측이면 판단이 바뀌나 |
| --- | --- | --- |
| ExifTool 원포럼 순위와 FreeCAD 이관 동률의 원시각이 미확인이다. | [ExifTool 원포럼](https://exiftool.org/forum/)과 [FreeCAD 원 이관](https://tracker.freecad.org/view.php?id=4641)의 원 시각을 확인해 같은 어구·날짜순으로 대조한다. | 독립적으로 원자료의 생성순을 확인해 첫 적격 세 사건을 양쪽에서 재현한다. |
| B는 F1 수식어의 극성을 잘못 붙였다. 두 방식 모두 동의어 6건의 완전한 근거 재사용을 놓쳤다. | [#195](https://github.com/RsyncProject/rsync/issues/195)와 [#2231](https://gitlab.com/inkscape/inkscape/-/work_items/2231)에서 시점과 행동, 객체를 분리한 새 맹검 시험을 한다. | 동의어 근거 유지가 늘고 F1 오지지와 D3 누락의 오승계가 함께 줄어든다. |
| 원형의 이력은 한 연결에서 검증했다. 다중 연결과 재확인 소비는 미확인이다. | [고정 store](https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/store.py)의 두 연결에서 같은 키와 주석 successor를 교차 실행한다. | 과거 지문을 유지하며 새 판정 하나와 재확인 해소가 원자적으로 남는다. |
