# AF-RES-195 조사 범위와 판정 기준

## 시작점과 입력

- 2026-11-24 UTC에 GitHub에서 최신 통합 브랜치 `chore/workspace-foundation`의 `72cf39aea54e2de2ba78a245593aefdc40205a16`을 확인했다. 계획판 `0f6765df46ad2128c7fdfa92c3bf917bbfe0c5e6`부터 세 커밋이며 좌우 차이 0/3, 변경 경로는 `docs/automation/dot-control.json` 한 곳이다. 작업 브랜치 `work/research-af-res-195`는 시작 조회에서 없었고 해당 통합판을 로컬 시작점으로 삼았다.
- 최신 `AGENTS.md`, `STATE.md`, `docs/DOT_AUTOMATION.md`, `docs/RESEARCH_WORKFLOW.md`, `docs/research/INDEX.md`, 관련 제품·클라우드·인계 규칙을 읽었다. 색인은 현재 AF-RES-195/181 개별 항목을 싣지 않는다. 진행표 본문 응답이 비어 Git blob `f0c9a6ea6f8a385ca103fabcb95df3b1a3bd130e`와 체크아웃을 읽었다. 이 판의 195는 RUNNING, 의존성은 181 하나다. 181 중앙 DONE·작업자 PARTIAL의 결과와 `HANDOFF.md` 고정점은 `a5d9b2cc5f295fe5cb15764e3965c14326c872d9`다. 181의 `assignments.csv`, `effort-quality.csv`, `bounds.csv`, 고정 대조 주소가 있는 `sources.jsonl`을 읽었다. 172는 그 이력이고 186은 별도 과제다. [진행표](https://github.com/laadkke-arch/agentflow-open/blob/72cf39aea54e2de2ba78a245593aefdc40205a16/docs/automation/dot-control.json) · [181 인계](https://github.com/laadkke-arch/agentflow-open/blob/a5d9b2cc5f295fe5cb15764e3965c14326c872d9/docs/workstreams/research/AF-RES-181/HANDOFF.md)
- 실험 입력은 DivEMT `934c4106001adeaa982a882d063f33ce0a398217`의 `data/raw/ita.zip`, `data/raw/tur.zip`, 저자 파서·전처리·분석 코드와 EMNLP 논문이다. 배포 처리판은 HF `9abd1d1cea118ad7a9946e7f1f5a1a29c2a01762`다. 181의 다섯 행은 재현 검사 기준으로만 쓴다. [DivEMT 고정 트리](https://github.com/gsarti/divemt/tree/934c4106001adeaa982a882d063f33ce0a398217) · [논문](https://aclanthology.org/2022.emnlp-main.532/) · [HF 고정 트리](https://huggingface.co/datasets/GroNLP/divemt/tree/9abd1d1cea118ad7a9946e7f1f5a1a29c2a01762)
- 노출 이력은 작업 시작 전에 인계의 TUR 후보 doc 1과 다섯 기대행을 이미 보았고 연구 설계와 비교 원문 링크가 고정돼 있었다. 전체 ZIP 목록을 해석하기 전에 이 문서에 모집과 판정 규칙을 적었다. 첫 로컬 HF API·ACL PDF 요청은 403이었다. ACL 출판 원문은 별도의 공개 웹 판독 경로에서 열렸고 HF 고정 데이터의 실제 파일 및 우회 없는 접근 가능성은 이 시점에 미확인이다. 셸에서 원자료 다운로드와 결과 생성은 실제 실행 증빙에 남긴다. 공개 결과물에는 번역문, 개인 속성 또는 XML의 IP·절대 시각을 넣지 않는다.

## 모집과 비교

1. `git rev-parse`와 Git 트리에서 원자료 판과 blob을 확인하고 ZIP 바이트 SHA-256, `ZipInfo` entry CRC·크기·순번 및 실제 읽기 결과를 기록한다. LFS 포인터, 해시/판 불일치, 손상, 접근 실패를 따로 판정한다.
2. ZIP의 작업 파일마다 XML job id/status를 열어 보고 main/warmup을 분리한다. 각 언어에서 main 숫자 doc_id 오름차순 첫 네 문서를 고정한다. 파일명이나 앞선 후보 숫자로 문서를 채우지 않는다. 설계상 예정 분모는 2언어 × 4문서 × 3조건 = 24자리다. 순위 선정 근거와 제외 및 실패를 `frame.csv`에 기록한다. 원래 예정표가 개별 키까지 확인되지 않으면 설계 슬롯과 관측 배정을 구별한다. 중복·비완료 및 매핑 실패를 숨기지 않고 모든 XML 상태·사람을 남긴다.
3. 배정은 익명 사람·문서·조건과 나중의 분절을 구별한다. 원문/FLORES 키, PIT/PET 작업의 입출력 지문, 주어진 초안과 최종 출력 지문, 완료 상태가 있는지 확인한다. 원파일 존재, 파싱, HF left join, 비교 자격, 독립 검수/시간을 각각 판정한다. 동일 사람이 세 조건을 수행했는지는 키로 검산한다.
4. 저자 시간 산식을 먼저 읽고 독립 산식의 ms를 나란히 둔다. 저자 시간과 별개로 모든 방문·마지막 이벤트·키 편집 여부 및 긴 휴지 등을 확인한다. 긴 휴지 감도는 한 가지 문턱마다 겹치는 구간을 한 번만 뺀다. HF 배포 자료 실측, Git 고정 저자 처리 재실행 결과, 181 전재행을 별도로 표시한다. 키나 판이 불명확하면 연결하지 않는다.
5. 같은 원문에 세 조건을 놓고 작업자별 번역 작업창만 비교한다. 분절의 완전 3조건/쌍별 분모, PE>HT·동률·미완료·누락의 실측 사례를 찾는다. 원자료의 실제 0과 없는 시간을 구별한다. OCR Kokos와 METR의 181 고정 자료로 독립 역할을 잘못 더했을 때를 검증한다. 최종 출력 해시와 결합할 독립 평점·검수시간이 없으면 총노동과 수용 품질은 미확인이다.
6. 양쪽 ZIP과 24자리, 언어별 완전 문서 1개 이상에서 독립 산식과 고정 처리판 대조, TUR 다섯 행 재현 또는 불일치 설명이 핵심이다. .per 12개, 코드/노트북 3개, 설계·스키마·처리 3개, 선행/타 분야 4개 이상을 직접 열고 출처·위치·한계를 남긴다. 고유 파일, 계보와 사건 수는 서로 다른 분모다. 핵심이나 종류별 최소치가 부족하면 자체 상태 PARTIAL이다.

이번 범위는 위 입력의 실행·검사와 두 언어 번역 작업창이다. 새 참여자/번역 실행, 다른 언어 조사, 공개 연구 재검색, 172의 CSV 재실행, 186의 결과·코드·채점 이용, 제품 DB/API/수집기/순위 결정은 배정에서 제외됐다. 영구 결과 경로는 이 폴더이며 중앙 진행표에는 쓰지 않는다. 입력 캐시와 일시적 검산 파일은 checkout 밖에 둔다.
