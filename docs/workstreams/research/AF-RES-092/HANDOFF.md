# AF-RES-092 인계 · 최종 합류판

**상태: PARTIAL.** 지정 6질문·12경로의 봉인, 공개 후속·교정·타 분야 대조, 원격 커밋·재열람·검사를 완료했다. P2의 동일 예산 비교와 원 Quarto 연결에 결손이 남아 **전체 여섯 쌍의 공평한 효과 판정은 완료하지 못했다.** 검사 통과로 이 연구 결손을 해소했다고 보지 않는다.

- **결과 SHA:** [`dbf432a7fefc556e9da08a645a017ca37464cf3e`](https://github.com/laadkke-arch/agentflow-open/blob/dbf432a7fefc556e9da08a645a017ca37464cf3e/docs/workstreams/research/AF-RES-092/RESULT.md).
- **새 검사·원격 재열람 영수증 SHA:** [`127a9a8e73349db0b1621f0cdcc72483cc04a6e2`](https://github.com/laadkke-arch/agentflow-open/tree/127a9a8e73349db0b1621f0cdcc72483cc04a6e2/docs/workstreams/research/AF-RES-092/evidence/verification-merged).
- **브랜치·경계:** `work/research-af-res-092`; 작성은 `docs/workstreams/research/AF-RES-092/` 안에만 했다. `dot-control.json`·다른 과제·통합 브랜치·main은 수정하지 않았다. 이 HANDOFF만 마지막 단독 커밋한다.

읽는 순서: [RESULT의 필수 세 표·분모](RESULT.md) → [독자 카드](cards.md) → [Q1–Q7 자가검산](SELF_CHECK.md) → [원장](sources.jsonl). [NEXT_ACTIONS.md](NEXT_ACTIONS.md)에 실행 대기 명령·입력과 판정을 바꿀 최소 관측을 모았다.

## 계약·중간 SHA·병행 이력

|묶음|원격 SHA|보존한 내용|
|---|---|---|
|①|`498feab24f0671273a0a91a8868e5c318e8093a3`|R0·요구·기준판·두 경로 검색식|
|②|`a04fbb20ca1a415235f69a1018a93e07e7adc926`|12경로·후보·사후 답을 가린 사전판정 봉인|
|③|`91cd24b66372174e6734c6478049e22aa9a2d9e2`|공개 후속·교정3건·상류/타 분야 반례|
|④|`b40b4dfeb8b7079f6568e511105117b02f477d14`|6대응쌍·카드·자가검산·후속 입력|
|병행 감사|`707216d8a7f2f09948bb79bfb30e9b2d62cde9ef`|19회 제외 재열람과 P3 추론/P2 인수 표현 보정|
|병행 인계|`e0d7ecda64bab2bd5d5779a9fb2a18d39a83bcdf`|그 세션의 HANDOFF·707 대상 검사 기록|
|검증 객체|`8e165316528616b84d79e9d3223ba85c04f79835`|b40 대상 원 검증 로그. 최초 ref 갱신은 병행 진전으로 거절됐고 이후 합류의 두 번째 부모로 보존|
|합류 결과|`dbf432a7fefc556e9da08a645a017ca37464cf3e`|e0d7·8e165 두 부모 보존; 재열람 메타데이터9행·P2 사후 설명 정정|
|합류 검증|`127a9a8e73349db0b1621f0cdcc72483cc04a6e2`|정확 합류 결과 SHA의 검사·원격11파일 재열람 원 영수증|
|최종 인계|이 파일의 마지막 단독 커밋|상태·검사 범위·실행 대기·다음 행동|

실제 최초 통합판은 `c2709abf8d25163eed75a7553ebcbde966105b55`, 계획판은 `62a80b9f111c695527a8ca87bcb867796d2e96bb`다. AF088 HANDOFF `a4c5f217313b5682d9d86c8507a7b5639dda89dd`와 결과/인수5파일 `e173b53f071aabfa749d33ab7da7ce970d5641b5`를 읽었다. manifest 계약은 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`로 유지했다. 마지막 개별 검사에서 확인한 통합판은 `e2a80afec762b10ee7979136c6332473c70905bb`다.

병행 업데이트를 덮어쓰지 않고 두 이력을 합쳤다. [정정 영수증](evidence/concurrency/reconciliation.json)에 성공 재열람3행의 실패 계보, 전자책 재열람4행의 보조 산입 플래그, 실패2행의 열람 표시를 이전 값·이유·시각과 함께 남겼다. 기존 봉인 frame/search_plan/candidates/searches와 판정은 불변이다. P3 원 AST는 **공개 보고·고정 코드가 지지하는 추론이며 미확인**, P2 `[2]{}`는 **두 필수 인수**라는 병행 보정을 보존했다.

## 판정과 분모

- 모집6·경로12·계획쌍6. 엄격 유효5쌍은 **A만0 / B만0 / 양쪽2(J1·J3) / 어느 쪽도 완결하지 못함3**이며 **P2 비교불가1**이다. 사전 P2의 조건부 완결은 역사적으로 보존하고 원 Quarto 전체 연결은 부분으로 낮췄다.
- B만 완결0/5; 실제 허용 집합이 다른 유효 P1/P3에서도0/2. jq3건은 관계 근거가 없어 B=A다. 불일치쌍 분모0이므로 불일치쌍 중 승률은 **산출 불가**다. 같은 조사자의 교차 순서를 독립 맹검으로 부르지 않는다.
- 검색24회(출력23, 그중 부분 코퍼스1; 전면실패1), 성공본문33/48회, 실패접근1을 포함한 접근34회. P2-B는 성공본문4이나 시도5이며 검색2도 실패했다. 경로명 탐색9회, 인접 검색 노출0행, 직접 선택한 인접 원문6개다. 이 절차는 소스 범위 자체의 효과를 분리하지 못한다.
- 산입 원자료 **40건 = R0 6 + 고정 매뉴얼/코드14 + 상류 동작8 + 오디오6 + 전자책6**. 보수적 저작/사건29그룹·계보33, 총 원장123행이다. 17회 재열람·2회 실패는 최소량·독립 사건·12경로에 기여0이다. 검색 요약·자기 실행·교정3건도 산입하지 않았다.
- 공개 답7·댓글7은 모두30일 이내; 현재 채택5질문, P3 해결 보고1건, J1 보조예 실행 실패 보고1건이다. 30일 이후 공개 답/댓글0은 삭제·비공개 활동 부재를 뜻하지 않는다. 원 질문자의 정확판·입력·명령·출력 완비 확인0/6; 완비 실행 분모0이므로 실행 성공률도 **산출 불가**다.
- J2/P2의 두 번째 제약은 공석이다. P3의 사후 주 도구 내부 `example_lists` 해법은 A/B 모두 놓친 정식 결과로 유지한다. P1/P3에서 B의 추가 본문1/2회는 완결을 늘리지 않았다. JN2/PN1/PE1 교정3건과 오디오·전자책 대조는 신규 승률에 섞지 않았다.

## 실제 실시한 검사와 원격 대조

**아래 세 검사의 대상은 모두 `dbf432a7fefc556e9da08a645a017ca37464cf3e`다.** 영수증 보존127a9a8 및 이 마지막 HANDOFF 커밋을 이전 검사에 포함했다고 주장하지 않는다. 전체 Git 이력, OS 기본 임시 경로, 정확 SHA의 clean worktree를 사용했다.

```bash
python -B docs/workstreams/research/AF-RES-092/audit.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-092/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

|검사|UTC 시각·종료값|확인 범위|
|---|---|---|
|자료 감사|2026-11-23 17:35:07, 0|6/12·분모·원자료 최소량·봉인4파일·재열람 메타데이터 일치|
|개별 계약 `--fetch`|17:35:07–17:35:15, 0|remote_checked, 계약동일, 통합e2a80afe, 변경140경로·범위밖0·충돌0·오류0|
|공통 검사|17:35:15–17:35:25, 0|정확 결과SHA에서 시작/끝 clean; doctor/acceptance/research-case/original-smoke/sessions 명령 종료0|
|공통 자동 세션 발견|명령0이나 실제 `not-executed/no_active_sessions/count0`|활성 세션 검증은 미실시; 위 개별 AF092 manifest 검사는 별도 실제 실시|
|GitHub 결과 재열람|11파일 blob 일치|RESULT 필수표6/12/6행·5/7/6열, 원장123/산입40, outcomes·카드·최초답/댓글/상류 영수증 일치, dot-control 미변경|

[원 로그·영수증](evidence/verification-merged/README.md)과 [11파일 지문·대조 범위](evidence/verification-merged/remote-readback.json)를 보존했다. b40 대상 외부 원문 재열람에서 최초답7/7·댓글7/7 본문 해시와 고정 Pandoc6836 원 파일을 대조했고, 이 관련 영수증 blob들은 합류판에서도 동일하다. [그 원 출력 대조](evidence/verification/primary-readback.json). 잘못 요청한 집계 영수증 파일명404도 남기고 실제 개별 파일로 바로잡았다.

이전 실패도 지우지 않았다. b40 검사의 첫 TMPDIR 자기 복사 시간초과와 다음 shallow 이력의 부모 결손은 [원 실패·복구 로그](evidence/verification/README.md)에 있다. 정상 임시 경로·전체 이력으로 같은 b40 검사가 통과했고, 합류 후에는 dbf에서도 새로 통과했다. 병행707 검사는 e0d7 HANDOFF의 기재를 확인한 수준이며 그 실행의 원 로그를 독립 대조하지 못했다. 이 서로 다른 SHA·실행 계열을 합쳐 보고하지 않는다.

`codex-cloud`는 호출자 환경 라벨이다. 이 검사들은 자료 구조·Git 계약·workbench를 검증하며 문헌 진실성·새 AI 연결·원 사용자의 구현 성공을 인증하지 않는다.

## 미실시·막힌 이유와 다음 첫 행동

**다음 첫 행동은 P2의 원 Qmd→Quarto1.4.553→생성 tex/PDF 연결 확인이다.** 현재 Quarto는 없으며 설치된 jq1.7/Pandoc3.1.11.1/TeX Live2025-dev는 연구 기준판과 다르다. 정확판 변환을 실행하지 않았다. 여섯 질문의 당시 사용판, P1 실제 코드포인트/fontfile·전체 Rmd, P3 전체 Markdown/bib/CSL/명령도 미확인이다. P2 이미지·J1 jqplay는 접근 실패, booktabs 고정 본문/바이트는 결손이다. 관련 주소·실패·판정을 바꿀 관측은 sources/SELF_CHECK에 있다. 제외된 AF088 판정64개·개설시각 바이트·PE1 이미지·고정 바이너리 시험은 재조사하지 않았다.

입력은 [원/파생 Qmd와 출처 설명](evidence/next-inputs/README.md)에 준비했다. 다음 명령은 **미실행**이며 연구 참조판 Quarto1.4.553의 판·설치 영수증을 먼저 확보한 환경에서 사용한다. 이를 원 질문자의 사용판으로 추정하지 않는다.

```bash
quarto --version
mkdir -p docs/workstreams/research/AF-RES-092/evidence/_cache/next-runs
cp docs/workstreams/research/AF-RES-092/evidence/next-inputs/P2-*.qmd docs/workstreams/research/AF-RES-092/evidence/_cache/next-runs/
quarto render docs/workstreams/research/AF-RES-092/evidence/_cache/next-runs/P2-original.qmd --to pdf -M keep-tex:true
quarto render docs/workstreams/research/AF-RES-092/evidence/_cache/next-runs/P2-sealed-macros.qmd --to pdf -M keep-tex:true
quarto render docs/workstreams/research/AF-RES-092/evidence/_cache/next-runs/P2-answer-macros.qmd --to pdf -M keep-tex:true
rg -n 'booktabs|toprule|bottomrule|noalign|renewcommand' docs/workstreams/research/AF-RES-092/evidence/_cache/next-runs/P2-*.tex
```

Quarto/bundled Pandoc/TeX판, 입력 SHA256, stdout/stderr/종료값과 tex/PDF를 보존한다. 후속 출력·로그·지문은 소유 경로의 추적 가능한 증거 파일로 옮겨 커밋하고 `_cache`에만 남기지 않는다. `{}`와 `[2]{}`를 별도 후보로 비교해 booktabs 로드순서·호출 인수·내용 보존을 확인한다. 성공해도 최초 P2 비교불가를 지우지 않는다.

P3 최소 입력 `evidence/next-inputs/P3-reader-minimal.md`는 합성형이며 원 전체 입력이 아니다. `$AF092_PANDOC_BIN`을 검증한 Pandoc3.1.11 절대경로로 지정한 뒤 아래 **미실행** 두 명령으로 reader 차이를 관측한다. 전체 서지/출력 성공은 원 Markdown/bib/CSL/명령을 추가 확보한 뒤 판정한다.

```bash
"$AF092_PANDOC_BIN" --from=markdown --to=native docs/workstreams/research/AF-RES-092/evidence/next-inputs/P3-reader-minimal.md
"$AF092_PANDOC_BIN" --from=markdown-example_lists --to=native docs/workstreams/research/AF-RES-092/evidence/next-inputs/P3-reader-minimal.md
```

J1/J3의 준비 입력 `J1-reference.json`/`J3-reference.json`과 jq1.7.1 실행 명령, P1의 필수 입력은 [NEXT_ACTIONS.md](NEXT_ACTIONS.md)에 있다. 원 사용자의 미제공 자료를 임의 예로 대신해 성공으로 세지 않는다.

## 중앙 색인 제안 한 줄

AF-RES-092 · PARTIAL · 신규6질문/12경로/6쌍, 유효5쌍 B만완결0·양쪽2·P2비교불가1, 원자료40/저작사건29, P3 주도구 내부 누락·인접검색 노출0 · 결과 dbf432a7fefc556e9da08a645a017ca37464cf3e · 개별계약/공통검사0 · 다음 P2 원 Qmd→고정판 tex/PDF 연결.

## 핵심 약점과 다음 조사 — 정확히 3건

1. **틀릴 수 있는 주장:** 추가 완결0이 인접 범위 자체의 효과라는 해석. **다음 대상·입력:** 기존6R0·고정판·질의의 재검사는 노출·과금 기전 확인용으로 한정하고, 효과의 다음 평가는 새 미노출 질문에 파일 단위 순위·인접 소스 할당·실패/경로 탐색 과금을 사전 고정한다. **판정을 바꿀 관측:** 인접 원문이 실제 노출·선택된 동일 예산에서 B만 또는 A만 완결하는 쌍. 사후 재실행으로 최초 비교를 대체하지 않는다.
2. **틀릴 수 있는 주장:** P2의 고정 Pandoc 매크로가 원 Quarto의 완결 해법이라는 해석. **다음 대상·입력:** 원/두 파생 Qmd, Quarto1.4.553의 template·생성 tex/PDF·정확 프로그램판. **판정을 바꿀 관측:** 내용 보존·두 선 제거·인수/로드 연결 확인이면 부분을 올리고, 인수 누출·후속 재정의·다른 writer면 수정/반박한다.
3. **틀릴 수 있는 주장:** 채택·P3 해결 보고만으로 정확한 목적 달성이 확인됐다는 해석. **다음 대상·입력:** P3 원 Markdown/bib/CSL/명령/정확판과 두 reader 모드 AST·출력, P1 글리프/PDF/HTML, J1 생략 없는 실행 출력. **판정을 바꿀 관측:** 동일 입력·완전 명령·정확판·목표 출력의 연결 또는 그 조건에서의 실패. 현재 완비 실행 분모0과 미확인을 유지한다.
