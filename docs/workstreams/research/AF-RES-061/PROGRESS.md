# AF-RES-061 재개 진행 기록

## AF-RES-061#2에서 인수한 상태

- 원격 작업 브랜치: `work/research-af-res-061`.
- 재개 직전 head: `672366cdf4542d4ca9f579963d66c2745f4316ed`.
- 최초 시작판과 기존 manifest는 유지: `1e741fd0def88ef56b1060a478d81f1985a4e760`.
- 재개 시 확인한 통합 브랜치: `a388314d32b2679223f9e3e99b78b93eb1678bf5`.
- `AGENTS.md`, `STATE.md`, `docs/DOT_AUTOMATION.md`, `docs/RESEARCH_WORKFLOW.md`, 최신 control의 AF-RES-061·057 항목과 고정 선행 인계를 읽었다. control의 AF-RES-061은 attempt 2/RUNNING이다. 공통 진행표는 수정하지 않는다.
- ① 범위·판 고정, ② API 및 A/B 예측 봉인, ③ 고정 소스·보조 실행·반례 대조가 이미 커밋되어 있다. 예측 봉인 SHA는 `02359364000057f69b00594d8b43571ac72df298`이다.
- 이전 세션의 `PROGRESS.md`와 `HANDOFF.md`는 없었다. 커밋된 소스 원장·스트림 메모·실행 영수증으로 재개했다. 원시험과 보조 실행을 다시 수행하거나 예측을 소급 수정하지 않는다.

## 남은 묶음 ④

1. 하위 스트림의 후속 독해를 루트 출처 원장에 합치고 고유 저작·배당·비교행·실행 분모를 각각 확인한다.
2. `RESULT.md`의 첫 8행/4행 표, `cards.md`, Q1~Q7의 반증과 결손을 담은 `SELF_CHECK.md`, `evidence/acceptance-evidence.json`을 작성한다.
3. 그래프·애니메이션·출처 계보를 분담 검토한다. 같은 모델의 문서 검토이며 독립 인간 실험이 아니다. 각 검토의 실제 범위와 지적을 보존한다.
4. 구조·수치·봉인·로컬 링크를 검사하고 결과 묶음을 원격 커밋한다. 고정 RESULT와 수용 원장을 다시 열고 지정 `session check --fetch`를 실행한다.
5. 확인한 결과 SHA, 검사 범위, 자료 결손과 다음 첫 행동을 넣어 `HANDOFF.md`만 마지막으로 커밋한다.

## 현재 유지할 판정

주 표본 4구현·8행, API/A/B 24행 중 GV의 A 2행은 자료 결손이다. A/B 운영 예측 차이는 비교 가능한 6행에서 관측 0이다. 같은 판·같은 입력의 독립 보관 원출력은 조사 범위에서 확보 0/8이며, 자체 실행 6행은 보조 증거다. 원전의 조건부 설명을 새 라이브러리 적중으로 바꾸지 않는다. 완전 수용 여부는 ④의 실제 수용 원장에서 판정한다.

## 묶음 ④ 작성·검토 상태

필수8/4행 표·4반환 카드·Q1~Q7자체 반증·37조건 수용 원장을 작성했다. canonical 취득164행/고유 적격31저작, 검색·실패71행을 합쳤다. 같은모델 분담 검토가 source 계보·graph/animation mapping과 report를 확인했고 보고서 출처/분모6건을 수정했다. d3 앵커·CRLF 해시 정정은 별도 영수증에 보존한다. 첫 구조 검사에서 생성될 자기 receipt의 링크2건이 먼저 없어 실패했고 원문을 audit-initial.json에 보존했다. 해당 receipt 생성 후 재검한다. 마지막 원격 재열람·계약 check·HANDOFF는 아직 수행 전이며 아래 후속 커밋/인계가 실제 결과를 기록한다.

## 묶음 ④ 원격 고정·1차 마감 검사

- 결과 묶음 원격 SHA: `941e753f7238f3985a6e2bb4e4d8ce9f7277fd3b`. 첫8행/둘째4행/마지막3행 표,4카드,37수용조건,31고유1차저작을 보존했다.
- RESULT와 acceptance를 위 SHA의 GitHub에서 다시 열어 준비된 내용과 일치함을 확인했다. `evidence/fixed-result-verification.json`.
- 지정 `python -B -m workbench.session check docs/workstreams/research/AF-RES-061/manifest.json --fetch`는 실제 종료0/passed, outside/unmerged/errors 모두0. 검사시각06:37:17–06:37:30UTC, integration a388314d32b2679223f9e3e99b78b93eb1678bf5. `evidence/session-check-stage4.json`.
- 초기 자기receipt 링크2건은 생성 뒤 재검해 구조·봉인·링크34/34 통과. `evidence/audit-initial.json`은 최초 실패를 보존한다.
- 다음은 이 검사 영수증을 포함한 결과를 커밋하고, 그 고정판을 다시 열어 최종check한 뒤 HANDOFF만 마지막 단독커밋하는 것이다. 연구상 부분 인계 판정은 유지한다.

## 고정판 로컬 링크 마감 정정

검사영수증 포함판ac768fc를 다시 열고 계약check가통과한 뒤, 그 고정판에서는 아직 존재하지 않는 HANDOFF를 가리키는 선행 링크2건을 확인했다. 이후 작성될 파일이라는 검사기의 예외를 없애고 RESULT/SELF_CHECK에서 해당 언급을 링크 없는 파일명으로 바꿨다. 사실·분모·예측은 변하지 않았다. 엄격한 로컬 링크 검사도34/34 통과했고 결손링크는0이다. `evidence/closure-corrections.json`. 이 정정을 포함한 새 결과판을 마지막으로 고정·재열람·check한 뒤 HANDOFF만 작성한다.
