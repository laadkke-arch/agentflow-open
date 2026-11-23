# AF-RES-092 인계 · 시도 2

**PARTIAL · 재개 감사·원격 재열람·검사 완료.** P2의 탐색 공평성과 원 Quarto 연결이 미완료여서 전체 여섯 쌍의 효과 판정은 완료하지 못했다. 결과는 [`707216d8a7f2f09948bb79bfb30e9b2d62cde9ef`](https://github.com/laadkke-arch/agentflow-open/blob/707216d8a7f2f09948bb79bfb30e9b2d62cde9ef/docs/workstreams/research/AF-RES-092/RESULT.md)에 있다. 검사 통과는 연구 결손을 해소하지 않는다.

브랜치 `work/research-af-res-092`, 쓰기 범위 `docs/workstreams/research/AF-RES-092/`. 이 HANDOFF만 마지막 단독 커밋한다. `dot-control.json`·다른 과제·통합 브랜치·main은 수정하지 않았다.

읽는 순서: [RESULT의 필수 세 표·분모](RESULT.md) → [cards](cards.md) → [SELF_CHECK](SELF_CHECK.md) → [원장](sources.jsonl).

## 커밋과 재개 범위

|묶음|원격 SHA|내용|
|---|---|---|
|①|`498feab24f0671273a0a91a8868e5c318e8093a3`|R0·요구·기준판·검색식|
|②|`a04fbb20ca1a415235f69a1018a93e07e7adc926`|12경로·후보·사전판정 봉인|
|③|`91cd24b66372174e6734c6478049e22aa9a2d9e2`|공개후속·교정3·타 분야|
|④|`b40b4dfeb8b7079f6568e511105117b02f477d14`|대응쌍·카드·자가검산; 재개 때 실제 최신판|
|④b|`707216d8a7f2f09948bb79bfb30e9b2d62cde9ef`|재개 감사와 조건부 추론 표현 보정|
|⑤|이 파일의 마지막 단독 커밋|검사·미확인·다음 행동|

사용자 체크포인트91cd24b의 후속 b40b4df를 원격에서 확인해 완료한 묶음은 반복하지 않았다. 최초 통합판 `c2709abf8d25163eed75a7553ebcbde966105b55`, 계획판 `62a80b9f111c695527a8ca87bcb867796d2e96bb`, 재개 통합판 `0537c02a3f84a8807a38cbb5c8d3dccdc3743243`을 구별한다. 필수 규칙 파일은 시작판 이후 동일했고 기존 manifest를 유지했다. AF-RES-088 HANDOFF는 `a4c5f217313b5682d9d86c8507a7b5639dda89dd`; e173b53의 인수5파일은 원바이트와 일치했다. [인수 영수증](evidence/resume/intake.json).

수치·봉인 순서 오류는 찾지 못했다. P3 reader 원인을 실제 원 AST에서 관측한 듯한 한 문장은 **공개 보고와 코드가 지지하는 추론이며 원 AST는 미확인**으로 고쳤다. P2의 `[2]{}`는 두 필수 인수를 소비한다고 명확히 했다. frame/search_plan/candidates/searches와 사전판정은 보존했다. [분모](evidence/review/resume-denominator-audit.md)·[기술](evidence/review/resume-claims-audit.md)·[타 분야](evidence/review/resume-crossdomain-audit.md) 검토는 사후 협업 감사이며 독립 맹검 탐색이 아니다.

## 핵심 결과

- 모집6·경로12·계획쌍6. 엄격 유효5쌍은 A만0/B만0/양쪽2(J1·J3)/어느쪽도아님3; P2 비교불가1.
- B만 완결0/5이며 실제 허용 집합이 다른 유효 P1/P3에서도0/2. 불일치쌍 승률은 분모0으로 산출 불가다. 인접 검색 노출0과 별도 경로 탐색9가 섞여 범위 자체의 효과를 입증하지 못했다.
- 검색24·성공본문33·실패접근1. P2-B는 본문4지만 시도5이고 검색1 부분결원·검색2 실패다.
- 최소량 산입40자료(6+14+8+6+6), 저작/사건29그룹·계보33. 원장123행 중 재개 재열람17회·실패2회는 신규 자료/독립 사건/12경로 기여0.
- 공개 답7·댓글7 모두30일 이내, 현재 채택5질문, P3 해결 보고1건. 정확판·입력·명령·출력 완비 실행 확인0/6이며 실행 성공률은 완비 분모0으로 산출 불가.
- J2/P2의 C2는 공석. 교정 JN2/PN1/PE1 세 건은 주 승률에 합산0. P3의 사후 reader 해법을 최초 A/B 성공으로 소급하지 않았다.

## 실제 검사

검사 대상은 모두 결과 SHA `707216d8a7f2f09948bb79bfb30e9b2d62cde9ef`다. 마지막 HANDOFF 문서는 포함되지 않는다.

```bash
python -B docs/workstreams/research/AF-RES-092/audit.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-092/manifest.json --fetch
python -B scripts/cloud_check.py --environment chatgpt-cloud --fetch-contract --require-clean
```

|검사|실시·종료값·범위|
|---|---|
|audit.py|0. 분모·자료·봉인4파일 불변. 일부 헤드라인은 현재 실험용 리터럴이므로 별도 원로그 재계산으로 확인.|
|개별 session check --fetch|0, passed/remote_checked, UTC 2026-11-23T17:18:13.789140+00:00. 통합0537c02, 계약동일, 변경107경로·범위밖0·충돌0·오류0.|
|공통 첫 실행|1, UTC 17:18:32–17:18:42. 55+7+9시험 통과 후 shallow checkout의 누락 부모 때문에 Git bundle 복원 실패.|
|이력 복구|지정 세 브랜치에 `git fetch --unshallow --no-tags origin` 실행, 0. shallow=false와 누락 부모 commit 확보 확인. 검사 코드·기준은 변경하지 않음.|
|공통 재실행|0, UTC 17:19:32–17:19:42. Python3.12.14; 시작·종료 clean. doctor, acceptance, research-case, original-smoke 통과; 단위55·lab7/9·demo·분리 export·Git bundle 복원 확인.|
|공통 sessions 자동 검색|명령0이나 `no_active_sessions`로 자동 세션검사 미실시. owned_path manifest는 위 개별 명령으로 실제 검사.|
|표·범위·공백|표1/2/3은6/12/6행·5/7/6열, 마지막 약점3건, owned path·작성 diff 공백 검산 통과.|

최초 실패 원문은 `Could not read f10c81baa98d9bad0407c9af8b4fa91cf9b70f6e`와 `Failed to traverse parents of commit c2709abf8d25163eed75a7553ebcbde966105b55`였다. 정상 이력 취득 후 **같은 소스**에서 복원까지 통과했다. 성공 bundle SHA-256은 `ca27fa93ea73f67465c255ef77a248bcee8e6d8d77312d2228b4d76fd4acc29b`다. 공통 계약 지문은 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`다.

`chatgpt-cloud`는 실행 위치 라벨이며 사용자 Codex 계정·새 웹 Pro 연결의 검증이 아니다. 판 고정 jq/Pandoc/Quarto 변환, 원 질문자 재현, 탐색 인과효과는 미실시·미확인이다.

## 원격 결과 재열람

UTC `2026-11-23T17:18:52.285Z`에 결과 SHA의 아래8파일을 GitHub에서 다시 열고 작업 사본과 대조했다. 모든 blob이 일치했고 원격 원장123행/산입40 및 쌍 분류도 일치했다.

|파일|원격·로컬 동일 blob SHA|
|---|---|
|RESULT.md|`f3e84db7374c17d58edfff20c2ed80cb2a21c2d6`|
|sources.jsonl|`0422dd4d3f73b04684ceb2d8d645ab0e7302075d`|
|metrics.json|`0d215c465fecd458fc3e91daacf35080c9087b12`|
|outcomes.csv|`c086e423a6b08c7093efc3a738fd285b41e254a6`|
|cards.md|`878ff654f914040f38c2c8ee9b4ad5eba0344d37`|
|evidence/outcomes/report.md|`e187132cec5c29df390e3e5eadb0d78e879bae8f`|
|evidence/outcomes/answer-first-receipts.json|`16c49560dde450db1c08c7d68aefecdbb4c457ea`|
|manifest.json|`16fdaa132a77d3d63773e8079b047c63230dbe13`|

RESULT SHA-256: `3d5f5bf880701073a7b6f2e8077cda35d4cdc3552fd16e8904a238bc9b2255b3`. 소유 경로 밖 변경0. 원 질문자의 실제 출력이 없는 행은 답변자 예·댓글 영수증까지 확인한 범위다.

## 다음 첫 행동·실행 대기 명령

**P2의 원 Qmd→Quarto1.4.553→생성 tex/PDF 연결을 먼저 확인한다.** [NEXT_ACTIONS.md](NEXT_ACTIONS.md)에 전체 명령과 [원·파생 입력](evidence/next-inputs/README.md)이 있다. 현재 Quarto는 없고 jq1.7/Pandoc3.1.11.1/TeX Live2025-dev는 고정 연구판과 달라 정확판 변환을 실행하지 않았다. 당시 원 사용판도 여섯 건 모두 미확인이다.

```bash
quarto --version
mkdir -p docs/workstreams/research/AF-RES-092/evidence/_cache/next-runs
cp docs/workstreams/research/AF-RES-092/evidence/next-inputs/P2-*.qmd docs/workstreams/research/AF-RES-092/evidence/_cache/next-runs/
quarto render docs/workstreams/research/AF-RES-092/evidence/_cache/next-runs/P2-original.qmd --to pdf -M keep-tex:true
quarto render docs/workstreams/research/AF-RES-092/evidence/_cache/next-runs/P2-sealed-macros.qmd --to pdf -M keep-tex:true
quarto render docs/workstreams/research/AF-RES-092/evidence/_cache/next-runs/P2-answer-macros.qmd --to pdf -M keep-tex:true
```

위 명령은 미실행이다. 실제 Quarto/bundled Pandoc/TeX판, 입력 SHA-256, stdout/stderr/종료값과 tex/PDF를 보존한다. `{}`와 `[2]{}`를 별도로 비교해 booktabs 로드 순서·noalign 인수·표 내용 보존을 확인한다. 성공해도 최초 P2 비교불가를 지우지 않는다. P3의 두 reader 모드 AST 명령, J1/J3 입력, P1에 필요한 코드포인트/fontfile/Rmd도 NEXT_ACTIONS에 있다.

## 중앙 색인 제안 한 줄

AF-RES-092 · PARTIAL · 신규6질문/12경로/6쌍, 유효5쌍 B만완결0·양쪽2·P2비교불가1, 원자료40/저작사건29, P3 주도구 내부 누락·인접검색 노출0 · 결과 707216d8a7f2f09948bb79bfb30e9b2d62cde9ef · 개별계약/공통검사0 · 다음 P2 원 Qmd→고정판 tex/PDF 연결.

## 핵심 약점과 다음 조사 — 정확히 3건

1. **틀릴 수 있는 주장:** 추가 완결0이 인접 범위 자체의 효과라는 해석. **다음 대상·입력:** 새 미노출 질문과 사전 고정한 파일 단위 순위·인접 소스 할당·실패/경로 탐색 과금. **바꿀 관측:** 인접 원문이 실제 노출·선택된 같은 예산에서 B만 또는 A만 완결하는 쌍. 기존 여섯 질문의 사후 재실행으로 원 실험을 대체하지 않는다.
2. **틀릴 수 있는 주장:** P2의 고정 Pandoc 매크로가 원 Quarto의 완결 해법이라는 해석. **다음 대상·입력:** 원/두 파생 Qmd, Quarto1.4.553의 template·생성 tex/PDF·프로그램판. **바꿀 관측:** 내용 보존·두 선 제거·인수/로드 연결 확인이면 부분을 올리고, 인수 누출·후속 재정의·다른 writer면 수정/반박한다.
3. **틀릴 수 있는 주장:** 채택·P3 해결 보고만으로 정확한 목적 달성이 확인됐다는 해석. **다음 대상·입력:** P3 원 Markdown/bib/CSL/명령/정확판과 두 reader 모드의 AST·출력; P1 글리프/HTML, J1 생략 없는 실행 출력. **바꿀 관측:** 동일 입력·완전 명령·정확판·목표 출력의 연결 또는 그 조건에서의 실패. 현재 완비 실행 분모0과 미확인을 유지한다.
