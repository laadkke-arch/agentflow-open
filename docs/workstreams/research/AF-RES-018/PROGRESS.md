# AF-RES-018 — PROGRESS

- 상태: 사전등록 준비, A/P 0개 실행.
- source_commit: `f9f2139d4a87d0879b041545baffdfdee6e604c5`
- 작업브랜치: work/research-af-res-018 (시작 때 원격 없음).
- 고정입력7개 fetch 및 각각 HANDOFF·필수규칙 직접열람. 다른017~020결과는읽지않음.
- 실제모델표시: GPT-6 Astra Pro, 지식cutoff미노출.
- 실행위치: ChatGPT 공유Linux workspace `/workspace/scratch/4d9059979b5e/agentflow-open`.

## 첫 커밋 전 익명 네트워크 관측

| 요청 URL | UTC | 코드 | 처리 |
|---|---|---|---|
| https://github.com/laadkke-arch/agentflow-open | 2026-11-21T03:49:24.428628+00:00 | 200 | 단회 응답; 개별본문 접근은 별도 확인 |
| https://api.github.com | 2026-11-21T03:49:24.429517+00:00 | 200 | 단회 응답; 개별본문 접근은 별도 확인 |
| https://raw.githubusercontent.com | 2026-11-21T03:49:24.430147+00:00 | 200 | 단회 응답; 개별본문 접근은 별도 확인 |
| https://softwarerecs.stackexchange.com | 2026-11-21T03:49:24.430693+00:00 | 200 | 단회 응답; 개별본문 접근은 별도 확인 |
| https://api.stackexchange.com/2.3/info?site=softwarerecs | 2026-11-21T03:49:24.431780+00:00 | 200 | 단회 응답; 개별본문 접근은 별도 확인 |
| https://news.ycombinator.com | 2026-11-21T03:49:24.432514+00:00 | 200 | 단회 응답; 개별본문 접근은 별도 확인 |
| https://hn.algolia.com | 2026-11-21T03:49:24.434259+00:00 | 200 | 단회 응답; 개별본문 접근은 별도 확인 |
| https://www.reddit.com | 2026-11-21T03:49:24.435274+00:00 | 200 | 단회 응답; 개별본문 접근은 별도 확인 |
| https://grep.app/api/search?q=offline | 2026-11-21T03:49:30.156741+00:00 | 200 | 단회 응답; 개별본문 접근은 별도 확인 |
| https://aclanthology.org | 2026-11-21T03:49:30.826979+00:00 | 200 | 단회 응답; 개별본문 접근은 별도 확인 |
| https://arxiv.org | 2026-11-21T03:49:30.913938+00:00 | 200 | 단회 응답; 개별본문 접근은 별도 확인 |
| https://pmc.ncbi.nlm.nih.gov | 2026-11-21T03:49:30.919954+00:00 | 203 | 단회 응답; 개별본문 접근은 별도 확인 |
| https://pubmed.ncbi.nlm.nih.gov | 2026-11-21T03:49:31.097998+00:00 | 200 | 단회 응답; 개별본문 접근은 별도 확인 |
| https://www.nejm.org | 2026-11-21T03:49:31.265213+00:00 | 403 | 호스트차단; 웹열람 또는 정상 공개저자판만 대체 |
| https://doi.org | 2026-11-21T03:49:31.598425+00:00 | 200 | 단회 응답; 개별본문 접근은 별도 확인 |
| https://web.archive.org | 2026-11-21T03:49:38.021810+00:00 | 200 | 단회 응답; 개별본문 접근은 별도 확인 |

원장은 evidence/network-initial.json. 문헌/새질문 담당의 추가호스트 관측은 해당 evidence/*/network*.json 및 questions/new-draft에보존. 단회200은원문확보성공을뜻하지않는다. NEJM403을우회하지않는다.

## 다음 행동

1. 사전등록묶음을원격커밋.
2. 01130개+보완3개, 새질문20개확보·원문판시도·동결.
3. gold/검사후보동결후에만새문맥A/P시작.

## 사전등록과 문헌 묶음 완료

- 사전등록 원격 커밋: `fe6eef0008a6ba27dc6f71d097ff6ef2c56b5858`. 아직 A/P 실행 0건.
- 일반 Git push는 자격 증명이 없어 실패했다. 이미 연결된 GitHub 도구의 tree/commit/ref 기능으로 동일 트리를 원격 브랜치에 기록했다. 새 로그인·권한 변경은 하지 않았다.
- 방법·비교 문헌 29편의 본문을 내부 별도 조사 에이전트들이 직접 읽었다. `evidence/structured/` 14편(5분야), `evidence/evaluation/` 15편이다. 본문/초록/실패 경로를 분리하며 동일 표본의 논문은 독립 재현으로 세지 않는다.
- 질문 최초판은 011 선택33개 중 SE19개에서 회수했다. 나머지14개는 고정011 요약을 사용한다. 최초판과 나중 조건의 차이를 `questions/ORIGINAL_AUDIT.md`에 기록 중이다.
- 다음 첫 행동: 새 질문20개 날짜·답변 기록을 확정하고 질문 묶음을 동결, 검사 후보의 공식문서 근거를 완성해 gold 묶음을 동결한다.
