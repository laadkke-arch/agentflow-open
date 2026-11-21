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
