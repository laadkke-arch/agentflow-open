# AF-RES-111 · 조사 범위와 사전 고정 절차

## 시작판

계획 `c40ef7723d851b628233bfb60dff8dfd292385cf`. GitHub `ls-remote`에서 2026-11-24 01:42 UTC에 작업 브랜치가 없고 통합 head가 `9bf49108116e4f68e348869c2687ba36a30dc012`임을 확인했다. 그 head에서 작업 브랜치를 만들었다. 01:43:27의 `session start --fetch` 시점의 원격 통합은 `0bcaf7c90f3324447fd1b8bf12c514187ca4776b`였다. 계획판부터 이 판까지 세 커밋과 브랜치 생성 뒤의 한 커밋은 모두 중앙 진행표만 바꿨다. 두 시작판의 AF-RES-111 행은 같았고, 읽을 계약·브리프·작업 규칙에 차이가 없었다. manifest의 base와 원격 통합 핀은 이 관측을 구분한다. 중앙 진행표의 AF-RES-111 행만 작업 지시로 사용했다.

고정 입력은 [통합의 작업 규칙](https://github.com/laadkke-arch/agentflow-open/blob/9bf49108116e4f68e348869c2687ba36a30dc012/AGENTS.md), [상태](https://github.com/laadkke-arch/agentflow-open/blob/9bf49108116e4f68e348869c2687ba36a30dc012/STATE.md), [Dot 절차](https://github.com/laadkke-arch/agentflow-open/blob/9bf49108116e4f68e348869c2687ba36a30dc012/docs/DOT_AUTOMATION.md), [제품 브리프](https://github.com/laadkke-arch/agentflow-open/blob/9bf49108116e4f68e348869c2687ba36a30dc012/docs/product/RESEARCH_BRIEF.md), [연구 절차](https://github.com/laadkke-arch/agentflow-open/blob/9bf49108116e4f68e348869c2687ba36a30dc012/docs/RESEARCH_WORKFLOW.md)다. [AF-RES-107 인계](https://github.com/laadkke-arch/agentflow-open/blob/54fccba38c764032f9ecc5fac5a676a9e2a898f5/docs/workstreams/research/AF-RES-107/HANDOFF.md)와 [검사 결과](https://github.com/laadkke-arch/agentflow-open/blob/8ae7aad97c7a4e958cdfe078ff49262b3717874e/docs/workstreams/research/AF-RES-107/RESULT.md), 그 판의 실행·요소 원장을 읽었다. 단일 A 0/6, B 6/6, 전체 양쪽 6/6이며 g12/g21, m-start/m-end, e01/형제 집합의 판별을 이번 질문으로 가져온다. 원형은 `fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c` 네 파일을 읽고 원형이 import하는 모듈은 실행 의존으로만 사본에 둔다.

## 모집

사건 생성 시각이 2021-01-01 00:00:00 UTC 이상이고 2026-01-01 00:00:00 UTC 미만인 공개 원 요청을 대상으로 한다. F는 ExifTool 원 포럼·공식 저장소 문의와 rsync 공식 저장소 이슈, D는 Inkscape 공식 GitLab 이슈와 FreeCAD 공식 GitHub 이슈를 대상으로 한다. 원 제목·요청 본문에만 아래 탐색어를 적용한다. Unicode casefold, 연속 공백의 단일화와 함정 방지를 위한 단어 경계를 쓴다. 발췌된 답글이 이미 검색된 경우 원문에서 다시 맞춰 본다.

| 층 | 영어 탐색어 | 한국어 탐색어 |
| --- | --- | --- |
| F | `remove-source-files`, `preserve original`, `keep original`, `copy files`, `move files`, `copy photos`, `move photos` | 원본 보존, 원본 유지, 파일 복사, 파일 이동, 사진 복사, 사진 이동 |
| D | `clone`, `linked object`, `App::Link`, `symbol instance`, `edit instance`, `edit all` | 복제, 연결 객체, 심볼 인스턴스, 한 개 수정, 모두 수정 |

원 서비스 검색을 우선한다. 서비스 검색에서 OR가 지원되지 않으면 어구별로 찾은 뒤 합친다. D의 단어는 동작과 적용 범위를 확인할 수 있는지 적격 판독에서 따진다. 수집 가능한 각 검색이 30건에 이르거나 소진될 때까지 목록을 받고 원 표면과 시각·동률 ID로 합친다. 날짜는 초 단위 UTC, 동률은 저장소/포럼 이름과 정수 ID 오름차순이다. 동시 같은 사건의 이동·미러·체크아웃은 최초 원 요청과 묶는다. 각 층에서 이 순서 첫 30건 또는 소진까지 원 요청을 직접 열고, 판/특정 가능 환경·대상·조작·보존 조건·고정 가능한 원 절이 모두 있는 첫 세 사건을 고른다. 모집 범위가 일부 막히면 관측된 하위틀은 읽되 전역 순위와 적격을 풀어 쓰고 전체 재현성은 미확인으로 남긴다. 검색 스니펫은 탐색 기록만 된다. 후보가 비면 결과 분모에 6자리씩 남긴다. 기준의 원문은 저자의 원어 그대로 인용 위치를 잡고, 번역은 변형으로 표시한다.

## 고정 비교 규칙

개발 예 D0 두 건은 GNU coreutils v9.5 `src/cp.c`의 `--attributes-only`, `--backup`, `--preserve`와 PostgreSQL 17 `ALTER TABLE`의 `ONLY`, `DISABLE/ENABLE TRIGGER`, `DROP COLUMN`이다. 전자는 파일 바이트·속성과 기존 목적지 파일을 구분한다. 후자는 이름으로 지정한 테이블·파티션·clone trigger와 열 참조의 적용 범위를 구분한다. 규칙은 아래와 `rules.json`으로 먼저 고정한다.

- 두 방식은 같은 사건별 원문 요청판, 원문 부분지도, 후보 ID·판, 절과 사실·상태, 후보당 조사 예산(후보 1, 조건당 절 최대 4), 조건별 공통 평가기를 받는다. 부분지도는 두 방식에 동일하다. 결정 공개 전 평가 실행 입력에는 gold, 변형 작성자의 해석·변형 분류·기대값을 전달하지 않는다. 출판 단계가 읽는 파일과 해시를 기록하고, 독립 검산에서 금지 필드와 원 위치를 검사한다.
- A는 원 요청의 조작·부품명·조건 어구를 사건별 정확 문자열로 대조한다. 해당 사건의 공통 후보에 한정한 문자열 비교기다. 대소문자와 어구 경계의 처리만 고정한다. 별도 교정 실행의 원형과 구분한다.
- B는 각 요청 절의 원문 문자 구간에 대상·행동·극성·유지 대상·범위·판의 슬롯 근거를 단다. 규칙에 없는 말, 상충하는 범위, 같은 이름 두 발생 및 미상 판은 단정하지 않는다. 대상 명세의 입력 제공자 명시, 원 요청자의 추정 가능 문구, 동명이거나 공백인 상태를 출력에서 구분한다. 사건 고유의 공개 부분지도는 원문의 동일한 별칭·ID·환경만 담으며, 특정 변형의 정답 대상이나 범위를 싣지 않는다. 변경과 보존은 별도 필수 조건이다. 어휘에 없거나 버전의 직접 근거가 없는 판정은 미확인이다.
- 주 표본은 original, synonym, order, polarity, scope, omission의 여섯 자리다. 작성자 해석은 gold 판독과 실행에 제시하지 않는다. 판독자는 실행 결과 없이 원 저작의 고정 절, 대상과 상반 조건을 읽어 지지·반박·미확인을 봉인한다. `can/allow`는 금지의 단순 논리 부정으로 취급하지 않는다. 같은 출처가 실제로 양쪽 요구에 충분한지를 검토한다.
- 행 단위의 결과는 후보/근거 안정성, 문장 의미층과 실제 관측 분모를 함께 센다. 반대·범위·누락 층에서 잘못 승계한 인용, 오지지, 정당 보류, 놓친 근거를 따로 센다. 표시된 근거 ID가 같아도 해당 조건과 판이 실제로 같아야 한다. 모든 필수조건이 직접 지지될 때만 verified다.
- 재시도·수정은 정확한 원형 UI 입구에서 실제 파일 SQLite로 실행한다. 주 실행도 고정 스키마의 decision/run_claim 경로를 쓴다. 테스트 분모에는 교정·교란 대조·두 번째 재생을 더하지 않는다. 자료의 범위와 사례 수, 해석으로 얻은 조건과 저자가 실제로 시험한 조건을 분리한다.
