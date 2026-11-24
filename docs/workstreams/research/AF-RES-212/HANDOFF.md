# AF-RES-212 HANDOFF

status: PARTIAL
result_commit: f4b08aa627c834e4ceb2da232869411470c0e06d
branch: work/research-af-res-212
base_commit: 87ffc1539bcf33da0fccf45eb15982a02d93e409
scope_commit: 6836981286dafcc048057cf45ab6ed911e594797
brief_reference: bb146773bbffba5e724e8c842951e2c25198c2da
dependency: AF-RES-201 2fc69a2d9092330e30097c018427a45b1bd7d0d9 (central DONE, dependency HANDOFF 자체 PARTIAL; no E4)
owned_path: docs/workstreams/research/AF-RES-212/

## 결과
대표 파일 RESULT.md(세 필수 표/Q1–7/마지막 약점 3), sources.jsonl, frame.csv, examples.csv, names.csv, cards.md, COUNTEREXAMPLES.md, SELF_CHECK.md, SCOPE.md.
- 35/22 고유 직접 원자료: W3C 10/5, AT 제작자/시험/제보 6/5, 디자인 13/7, 출판/도서관 4/3, 사용자 연구 2/2. 원장 47행(35 산입, 5 별도 도착/보강, 7 실패/본문 부족). 동일 변형은 저작 중복 산입 금지. 기기/사용자 사건 수 전수 코딩 미실시; 35는 관측 사건수 아님.
- 엄격한 모집 6/12: USWDS 3/3 예시 6/6 앵커, GOV 0/3 및 0/6. USWDS collection default/media/calendar의 반복되는 두 href(고유 2), 실제 목적지 확인. dashboard 이름이 가리키는 것은 소개 기사(L02), sample date Sep 30 vs article Oct 27. GOV link/summary examples #, 독립 card 문서 미확인. 공식 teacher-training 서비스로 1회 이동했지만 raw anchor/aria 미확인; 4 보강 위치는 strict와 분리.
- 규칙 기반 name/description 계산과 실제 출력·발언 구분. 두 탐색(연속 읽기 vs link list: NVDA/VO)에서 대상+목적 이름 유지 후보, 설명은 별도. 같은 href 같은 행동이면 통합 가능; 동일 name 다른 실제 href pair strict 미확인(모의 W06 및 기존 제보/자기보고로만 대조). D09 공백, D10/D11 중복, D13 pseudo 문장부호/RTL/CMS 반례. 출판 PLOS supplement 500, NYPL sample 500, Apple 상세 rotor guide 429. SFPL eBook→실제 Book 카탈로그 확인. Q5 이름 길이 통제 관측 없음.
- 한국어 세 목적(비교 문헌/함수 호출/출판 그림)의 A visible/B 문맥/C hidden suffix/D description 대안. 동일 PDF로 연결하는 비교·그림은 하나의 링크와 위치 설명도 유지; C22 generator는 산출물 아님. 201 결과 재판정 없음.
- **미달 핵심: strict 6/12, 양 시스템 비교 불충분, 실제 동일 accessible name/다른 destination pair와 publisher supplement 파일, 두 AT의 목록별 name/description 실제 노출 미확인.** 이 때문에 DONE 처리하지 않음. 자체 검토만 수행, 독립 검토·실험·성공률 미실시.

## 고정 결과 재열람
HANDOFF 작성 전 GitHub에서 위 result_commit의 9파일을 fetch_file로 다시 읽었다.
|파일|blob|
|---|---|
|SCOPE.md|54591b62e816f91c84f9a2d124b0b2174bac9750|
|frame.csv|7c4321401d3c8bebd08a94d57417281b1c7d69c0|
|sources.jsonl|aced51efb2edd14ccb7a84d213ff40ec15cfaa9d|
|examples.csv|2ff40d2802f755266a6adfb1bd5d451f14ed8c2c|
|names.csv|292dc342e48bd2448236b21b290eb059aea15f9b|
|cards.md|eb162756779cc0fefa2879f76c337180dc383398|
|COUNTEREXAMPLES.md|f6a8c202572158035364720ef9e734beb676ed3d|
|RESULT.md|6ae996bcf5d3f37c119836ace38f3cb4609b503b|
|SELF_CHECK.md|ebdcf3d2bd8598318c43d27b163e6644a6d2ea07|
검증: JSONL 47행 parse, counted 35, 고유 counted work_id 및 URL 35, 유형별 위 수량 일치. CSV 행수 frame23/examples16/names16(헤더 제외), 채택6/결손6/보강4, 모든 names 행 observed_output 미측정 문자열 확인. RESULT 첫 3 필수 헤더 일치, 끝 약점표 3행, 반례 CE 10행 확인. 단순 ID regex 결과의 L67/L22/L32/L51/L92/L34는 본문 추출 위치, F63은 W3C failure 번호로 확인(원장 ID 아님). CSV 정식 parser 및 모든 참조 의미 독립 대조는 후속 검증. Base 대비 result ahead9 behind0, changed files 9개 모두 owned_path, dot-control.json 변경 없음. Scope→frame/sources→examples/names/cards→counterexamples→result/self-check 순서 커밋, 마지막 HANDOFF만 별도. 저장소 작업 규칙의 자체 점검을 독립 검토라 부르지 않음.

## 재개 첫 행동 및 Codex 검증 항목
1. 현재의 정규 GOV 6자리 결손부터 해소. SCOPE의 문서 순서와 기존 frame 보존. D01/D02에 링크된 실제 공식 서비스의 공개 HTML/공식 소스 확인(1회 jump 규칙). F01 독립 card 경로 대신 실제 summary card가 D02 안에서 제공되는지 source 경계 기록. 먼저 L03 원 DOM과 첫 두 anchor의 href/텍스트/ARIA/부모/계산 CSS를 확인. 적격이면 이전 raw 미확인/보강 판정을 변경한 이유, 날짜, source ID를 별도 기록; 새 사례를 사전 샘플처럼 합치지 말 것. 실제 href 두 개 없는 후보는 탈락. 원 모집 전체 후보와 미발견 공식 서비스 링크를 확인. USWDS source도 동일 절차로 전수 확인. 새 구현을 제품에 적용하거나 중앙 파일을 수정하지 말 것.
2. 파일 검증(아래 명령은 이 세션에서 실행하지 않았음; connector readback만 수행). 이미 허용된 임시 checkout에서:
   ```sh
   git fetch origin work/research-af-res-212
   git show f4b08aa627c834e4ceb2da232869411470c0e06d:docs/workstreams/research/AF-RES-212/RESULT.md
   git diff --name-only 87ffc1539bcf33da0fccf45eb15982a02d93e409 f4b08aa627c834e4ceb2da232869411470c0e06d
   git diff --exit-code 87ffc1539bcf33da0fccf45eb15982a02d93e409 f4b08aa627c834e4ceb2da232869411470c0e06d -- docs/automation/dot-control.json
   ```
   해당 result SHA checkout에서 python 표 검증: `python -c 'import csv,json,pathlib,collections; p=pathlib.Path("docs/workstreams/research/AF-RES-212"); s=[json.loads(l) for l in (p/"sources.jsonl").read_text().splitlines()]; c=[r for r in s if r["counted"]]; print(len(s),len(c),len({r["work_id"] for r in c}),collections.Counter(r["category"] for r in c)); print([(f,len(list(csv.DictReader((p/f).open())))) for f in ("frame.csv","examples.csv","names.csv")])'` 기대 47,35,35, 카테고리 위 수량; 23,16,16. 코드나 검사 설정 변경 없음.
3. 링크 목록/연속 탐색 검증은 별도 승인된 AT 환경에서만. 입력: cards.md의 A/B/C/D × 세 목적(비교/호출/출판 그림), D02 G-S1/G-S2, D05 U1a/U1b 원 예시, 동일 href pair와 같은 accessible name 다른 href 실제 pair. 원 HTML/fixture와 브라우저/OS/AT 버전 및 기본/변경 설정 기록. A: visible 대상+목적. B: 동일 visible text, 다른 주변 heading 및 문단. C: visible prefix + clipped span suffix; C2 공백 삭제/중복 suffix. D: 동일 visible text, 고유 aria-describedby; title-only 별도. 동일 실제 목적지 및 동작 variant 통합, 다른 fragment/target 별도. 접근성 tree에서 name/description 별개 기록. Windows NVDA+F7→Links 목록/필터, browse mode 연속 읽기 및 Tab; macOS VoiceOver 웹 로터 Links 및 연속 VO navigation. 가능한 기존 검증 기기에서 Speech Viewer/Caption Panel 원출력을 기록; 링크 목록과 문단 모드 구분. 음성 명령 환경은 보이는 label로 선택, 동일 label 모호성과 번호 대안 확인. 기대: A 명확 대상/목적, C 조건부 suffix 유지, B/D 목록 name만으로 구별 불가 가능. 반전: description이 두 목록에 안정적으로 노출되면 B/D 재평가, C suffix 누락/붙음/중복 또는 visible prefix 선택 실패시 A/C 전환, 동일 목적지 통합이 탐색을 개선하면 링크 수 감소. 사용자 성공률은 새 참가자 시험 승인·자료 없이 산출 금지. 새로운 설치·유료 API·외부 권한 확대 금지.
4. 실제 same accessible name/different URL pair의 공식 HTML+두 도착 객체 및 same URL same name pair 비교. D03 GIF 본체 확인 불가하면 example code만 유지. P01 supplement DOI/F04, P04 sample/F06은 공개 공식 landing/file만 합법적으로 다시 열고 차단 우회 금지. 객체와 file format/title 확인, label/설명 차이 기록. 201 원논문 그림 재판정하지 말 것. 기존 결과에서 원본 artifact link가 확인되지 않으면 C 그림은 출판 PDF와 위치 설명으로 유지. Apple 상세 guide 접근 실패는 재현/기존 관측 없이는 미확인 유지. D13 final merged vs prior tests 분리. 시간·검색어 노출 기록.
5. 독립 검토자에게 result SHA와 모집/근거/반례 대응, 35개 저작 count 적절성(동일 계보 중복 관측), 엄격 분모, date/object mismatch, 실제 측정 주장 부재를 확인 요청. PARTIAL을 DONE으로 올리기 전에 결손을 확인하고 교정 이력 보존.

## 색인 반영 제안 (수정하지 않음)
AF-RES-212 PARTIAL; 대표 RESULT.md, cards.md, SELF_CHECK.md. 주제: recommendation link target object + role + accessible name ≠ description, link-list vs continuous reading; same destination merge exception; strict 6/12, sources 35/22, no new AT run; AF-RES-201 dependency. 색인/control 상태 갱신과 merge는 조정자가 수행. 이 HANDOFF 이후 작성 세션에서 추가 변경하지 않음.
