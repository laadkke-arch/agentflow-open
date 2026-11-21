# AF-RES-020 진행 기록

## 시작

- 2026-11-21T04:59:35Z: 익명 네트워크 확인. GitHub 저장소 ls-remote·clone·고정 SHA fetch 성공.
- source_commit: `7b4334e55a0563225295618eaf3ad299b415d9f7`; 진행표 AF-RES-020은 RUNNING, source_commit은 null이므로 본 산출물에 고정했다. dot-control.json은 수정하지 않았다.
- work/research-af-res-020은 원격에 없어 위 SHA에서 새로 생성했다. 기존 작업을 덮어쓰지 않았다.
- 실행 위치: ChatGPT 공유 Linux workspace `/workspace/scratch/ec9dced9df4a/agentflow-open`; 모델 표시: GPT-6 Astra Pro.
- 읽은 운영 파일: AGENTS.md, STATE.md, DOT_AUTOMATION.md, RESEARCH_WORKFLOW.md, RESEARCH_BRIEF.md, INDEX.md, AF-RES-020 진행 항목. 의존 result_commit 12개가 사용자 고정 SHA와 일치한다.

## 첫 커밋 전 호스트 확인

익명 GET 각 1회, 루트 URL, 2026-11-21T04:59:35Z. HTTP 200은 논문 본문 접근을 보장하지 않는다. 이후 source 항목에서 실제 문서 본문 성공 여부를 별도 기록한다.

| 호스트 | 코드 | 사용 경로 / 제약 |
| --- | --- | --- |
| github.com | 200 | git clone/fetch 및 고정 SHA git show |
| raw.githubusercontent.com | 200 | 루트는 github.com으로 리디렉트; 실제 문서 별도 확인 |
| sloanreview.mit.edu | 200 | Toyota 원문 후보 |
| deepblue.lib.umich.edu | 403 | 미확인(호스트 차단); 재시도는 `curl -I https://deepblue.lib.umich.edu/` |
| web.mit.edu | 200 | 모듈화·real options 저자 원문 후보 |
| www.cs.umd.edu | 200 | 모듈화 원문 후보 |
| www.cs.virginia.edu | 200 | Sullivan 저자 원문 후보 |
| www.cs.cmu.edu | 200 | 설계 논증 원문 후보 |
| michaelnygard.com | 200 | ADR 저자 원문 후보 |
| www.bmj.com | 403 | 미확인(호스트 차단); 허용된 웹 열람/공개 저자판 사용. `curl -I https://www.bmj.com/` |
| pmc.ncbi.nlm.nih.gov | 203 | 본문 대신 확인 페이지일 수 있음; 실제 본문 확인 필요 |
| www.3ieimpact.org | 200 | 근거 격차 지도 원문 후보 |
| www.campbellcollaboration.org | 200 | 근거 격차 지도 방법 |
| www.aboutamazon.com | 200 | one-way/two-way door 원문 |
| pubmed.ncbi.nlm.nih.gov | 200 | 논문 메타데이터; 초록만은 본문 최소수에 미포함 |
| doi.org | 200 | 식별자; 대상 본문 별도 확인 |

막힌 호스트의 제한을 변경하거나 우회하지 않는다. brief가 허용한 웹 검색·열람과 별도 공개 원문을 쓴다. 추가 발견 호스트는 첫 사용 전에 익명 열람을 확인하고 외부 읽기 기록에 추가한다.

## 다음 행동

SCOPE 선커밋 후 고정 입력의 HANDOFF와 원 결과 전부 읽기, 내부 2개 묶음과 외부 방법 비교를 병렬 내부 별도 작업으로 분리한다. 커밋은 총괄만 수행한다.

## 원격 저장 경로

- 첫 로컬 커밋의 HTTPS git push는 셸 자격증명 부재로 실패했다(Username 프롬프트를 읽을 수 없음). 로그인·권한 변경 없이 이미 연결된 GitHub 도구의 laadkke-arch 계정으로 브랜치 생성과 tree/commit/ref 갱신을 사용한다. 각 묶음을 원격 커밋한 즉시 git fetch로 다시 읽는다. 이것은 네트워크 제한 우회가 아니라 허용된 기존 연결의 쓰기 기능이다.

## 운영 계약 검사 시도

- workbench.session start --fetch는 고정 AF-RES-013 result_commit과 현재 브랜치 HEAD가 달라 종료2로 중단됐다. 실제 응답과 두 SHA는 evidence/contract-start-attempt.json. 역사 자료 감사에서 최신 branch로 입력을 바꾸지 않았고 검사기를 약화하지 않았다. 고정 SHA 입력·범위·문서 연결은 이 과제의 검사로 별도 확인한다.

## 커밋 묶음 2

초기 묶음12개(B01–B07, B11, B12, B19, B20, B22)와 고정 원 결과 읽기 기록을 분리 저장한다. 표본의 정의/분모 차이를 수치 모순으로 잘못 합치지 않도록 원 단위와 관측 창을 병기했다.

## 커밋 묶음 3

24묶음의 8개 항목과 기계 판독 목록을 완성했다. 각 묶음은 최소3개의 고정 원 결과 주장을 가지며 브리프 8질문을 모두 덮는다. 내부 별도 감사 2건의 고정판 파일별 읽기 기록을 추가했다. 서로 다른 모델 선택이 가능하여 변별력 통제 문장과 숨은 의존 검토를 `gpt-6.2-sol`에 맡겼다. 초기 감사와 총괄은 세션 표기의 GPT-6 Astra Pro다. 사람 검토로 세지 않는다.

## 커밋 묶음 4

고정 원 결과 주장73행(명시 재사용3행을 묶으면70개 주장군)을 대조했다. 일치72·불일치1·확인불가0, 2단계 원 파일 대조57/73이다. C-B07-04의 역할/제안한 사용 방식 축 차이를 실제 전달 불일치로 기록했다. 일치72/73 편중을 점검하기 위해 별도 모델 gpt-6.2-sol이 심은 오류12·정확문장4·미측정효과2를 키 없이 검토했고 준비된 판정18/18과 일치했다. 통제18은 실제 주장 수·불일치 수에 더하지 않는다. 원래012/014검색 파이프라인을 새로 실행했다는 주장은 하지 않는다.
