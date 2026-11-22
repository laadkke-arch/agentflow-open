# AF-RES-023 — 조사 범위·사전 판정

## 고정 입력과 실행

- 배정 시 확인한 `chore/workspace-foundation`: `7f66165ad68610278df18855e1196a6cf52b035a`. 2026-11-22 03:06–03:10 UTC에 GitHub connector와 git ls-remote/clone으로 확인했다.
- 계획 기준판: `b507fbcab09724a77270e658355f4b661cc35f02`. 기준판 식별을 보존하며 다른 PLAN 5 작업 결과를 읽거나 기다리지 않는다.
- 의존 입력: AF-RES-020 `856e6b40ae12d43197a6f02f7bf6ab7a7506fd35`; HANDOFF 전체, bundles/B19.md 전체, RESULT.md Q1 L213–230·Q3 L242–250, DECISIONS.md D04–D06 L14–16을 git show로 읽었다. B19는 운영 식별 사건 빈칸이며 정의를 실제 성공/복원으로 세지 않는다.
- AGENTS.md, STATE.md, DOT_AUTOMATION.md, RESEARCH_WORKFLOW.md, product/RESEARCH_BRIEF.md, START_HERE.md, CLOUD_WORKFLOW.md와 dot-control의 AF-RES-023 및 AF-RES-020 항목을 직접 읽었다. STATE의 미배정 문구는 이번 명시 배정을 취소하지 않는다.
- 실행 위치: ChatGPT 공유 Linux workspace `/workspace/scratch/05a4ed6cd8b5/agentflow-open`; 셸·Python·Git, 공개 웹 열람과 GitHub 연결 도구. 사용자 PC에서 실행하지 않는다.
- 세션에 제공된 주 모델 표기: **GPT-6 Astra Pro**. 내부 병렬 조사자 `musicbrainz`, `ror`, `software`도 상속된 같은 모델 계열이다. 웹 Pro UI의 모델 선택을 관측했다는 뜻은 아니다.
- 브랜치: `work/research-af-res-023`, 시작 시 원격에 없어 위 foundation에서 생성. 쓰기 범위는 이 디렉터리뿐이다. 공통 계약·색인·dot-control·제품 코드·main은 변경하지 않는다.
- manifest.json: `workbench.session start af-res-023 --allow docs/workstreams/research/AF-RES-023/ --output docs/workstreams/research/AF-RES-023/manifest.json --dependency work/research-af-res-020=856e6b40ae12d43197a6f02f7bf6ab7a7506fd35 --fetch`가 exit 0. 고정 입력을 최신판으로 치환하지 않았다.

## 질문·단위·표집

Q1 실제 사건, Q2 동일시한 층위, Q3 ID/HTTP/역사 판의 시간순 관계, Q4 취소와 부분복원, Q5 하위 인용 영향, Q6 세 저장 표현의 복원 한계, Q7 분야 간 이전 조건을 답한다. 최종 제품 ID/DB를 정하지 않는다.

목적 표집이며 오병합률 추정이 아니다. 목표는 실제 사건 18개 이상, 시스템 3곳 이상(시스템당 최대 8개 산입), 소프트웨어 한 계열과 음악·지식베이스·연구조직 중 두 계열 이상이다. MusicBrainz·ROR·Homebrew를 병렬 조사하고 Wikidata에서 정정·복원 사례를 추가 탐색한다. 읽을 외부 원문은 사건 18·정책 또는 판 공지 6·독립 하위 소비자 6, 총 고유 30개 이상이다. 동일 편집의 여러 화면은 사건 하나이며 동일 저작·거울·재게시를 독립 근거로 더하지 않는다.

초기 목표 구성은 성공 병합 약 6, 오병합 정정/분리/되돌림 약 6, 승계/기각/정상 별칭 약 6이다. 사건이 없거나 정정판이 막혀 부족하면 빈칸을 성공으로 채우지 않는다. 실제 확보된 분포와 미충족을 종료 때 그대로 남긴다. 정상 rename/alias를 서로 다른 실체의 병합으로 오코딩하지 않는다.

탐색창: 공개되어 열리는 역사 사건 전체(최종 열람 시각까지), 날짜 제한 없이 merge/unmerge/revert/restore/split/successor/inactive/rename/alias와 해당 시스템의 원 ID 검색. 이 창은 모집단 완전성이 없다. 각 수집자의 SEARCH_LOG에 실제 질의·열린 편집 ID·실패를 남긴다. 편집 완료가 확인되지 않은 제안은 제안/거절 사건으로만 세고 완료 병합으로 승격하지 않는다.

## 시스템별 추출 경로와 식별 층

| 시스템 | 사건·전후 판 경로 | 독립 층 | 정답 기준 |
| --- | --- | --- | --- |
| MusicBrainz | edit ID→편집 전후 MBID→후속 edit/새 release·recording→공식 merge/style | URL / MBID catalog entity / work·recording·release / 같은 사용에 대체 가능 | 사후 정정 편집의 대상·판·범위; 투표/편집자 진술과 데이터 상태 분리 |
| Wikidata | revision diff·merge/undo log→QID 전후 revision→restored item/redirect | URL / QID item / 현실 대상·외부 ID / 주장과 인용 | 불변 revision과 undo/revert 기록; 현재 redirect로 과거를 소급하지 않음 |
| ROR | ror-updates issue→release/dump fixed version→inactive/successor | URL / ROR catalog record / 법적 조직·산하 조직 / 인용 당시 소속 | 적용 release의 상태·관계 + 변경 이유; closed issue만으로 적용 판 추정 금지 |
| 소프트웨어 | PR/commit diff→전후 formula/tag→renames·aliases·fork 변경→consumer commit | URL / formula·package ID / project·fork·distribution·version / 요구 기능 | 실제 diff 및 후속 정정 기록; upstream 현실 사건과 카탈로그 편집 별도 |

## 사전 코딩

- 사건 코드: SUCCESS_MERGE(허용되어 적용된 중복 병합), CORRECTED_MERGE(오병합 후 정정), SPLIT(하나→여럿), REJECTED(제안 기각/취소), SUCCESSION(현실 승계와 연결된 catalog 변경), ALIAS(동일 대상을 가리키는 이름 변경). 다중 사건은 시간순 하위 동작을 보존한다.
- 출처 수준: D0 검색/snippet(산입 제외), D1 원문/정책, D2 고정 코드/덤프, D3-fetch 실제 응답 관측, D3-run 이번 검사 실행, H 연구자 해석. 사실 / 편집자 주장 / 이번 관측 / 추론을 구별한다.
- HTTP: 직접 응답 코드가 있을 때만 200/301/404 등을 쓴다. web open의 렌더 성공은 HTTP 코드 미확인이다. HTTP 생존·redirect와 역사적 실체 상태를 별개 필드로 유지한다.
- 복원 항목: label, external identifier, citation, version, multiple successors 각각 AUTO(표시 자료로 유일 결정), MANUAL(근거가 있으나 선택/대조 필요), LOST(공식 정정에서 실제 정보 손실 확인), UNVERIFIED_ACCESS(원문 접근 실패), UNVERIFIED_RECORD(원문에 관계/범위 미기록). 미열람과 실제 소실을 혼동하지 않는다.
- 하위 소비자: 별도 파일/문서에서 옛 ID가 쓰인 문맥·시점과 후속 수정이 있는지 기록한다. 소비자 기록이 없으면 기계적 오도착 가능성까지만 말하고 실제 사용자 오추천은 미확인이다.

## Q6 자료 분리와 열람 순서

같은 사건·동일 사용 질문·원 자료 풀을 세 표현에 사용한다. ① URL+짧은 이유, ② 여기에 당시 ID·판·근거 절, ③ 여기에 합침/갈라짐·후계·유효시점 관계 이력. 각 표현의 누락 조건을 카드에 명시한다. 동명이인 무조건 분리로 실제 중복을 놓치는 경우, 단순 alias 충분 사례, 이력으로도 한 후계를 고를 수 없는 사례를 포함한다.

수집자는 사후 정정 원문을 읽어 answer-key.json을 만들 수 있다. root는 이 자료에 노출된 편집자이며 blind judge가 아니다. 보기와 키를 서로 다른 파일로 먼저 고정하고 SHA256·생성시각·열람자를 evidence/exposure-log.jsonl에 기록한다. 다음 별도 문맥의 내부 판독자 3명은 각각 한 표현의 카드만 읽고 외부 열람 없이 답한다. 답 파일을 고정한 뒤 정답표와 대조한다. 시스템 원문을 모른다는 보장은 할 수 없고 같은 모델 계열이므로 사람/외부 독립 시험으로 부르지 않는다. 그 절차를 수행하지 못하면 자기 점검으로 낮춰 적는다.

정답 키는 사후 정정 원문의 대상·판·인용 범위다. 미기록 항목에 연구자 정답을 만들어 채점하지 않는다. 사건별 3행을 유지하며 target/function-version-reason를 따로 PASS/PARTIAL/WRONG/HOLD/UNVERIFIED로 기록한다. 정답 접근 실패와 관계 미보존은 별도 원인이다. 분모에서 미확인/보류를 빼지 않는다. 성공률 차이를 운영 효과나 인과 추정으로 부르지 않는다.

## 저장과 점검

각 묶음 직후 root가 커밋하고 원격 고정판을 다시 읽는다. 순서: (1) 범위/추출/복원 규칙 (2) 시스템별 사건 (3) 소비자·세방식 비교 6사건씩 (4) 교차 분야·자기 점검 (5) HANDOFF 단독 최종 커밋. 출처 본문 전문이나 사용자명/프로필을 저장하지 않고 URL·고정ID·짧은 자기말 요약만 남긴다. 원 출처당 직접 인용은 25단어 이내다.

필수 산출물: events.jsonl, citations.csv, reconstruction.csv(최소18×3행), alternatives.md, RESULT.md(표1~4 먼저, 끝에 정확히3개 약점 행), sources.json, PROGRESS.md, SELF_CHECK.md, evidence/acceptance-evidence.json, HANDOFF.md. 수용 조건은 met=false를 허용하며 부족한 조건은 가능한 보강 뒤 REVIEW_READY_WITH_GAPS 또는 BLOCKED로 인계한다.

## 실제 실행의 추가 관측과 편차

- 조사 원문 관측 창은2026-11-22 03:09–04:09 UTC. 사용자시간대Asia/Seoul로는같은날12:09–13:09이다. 파일생성·검사·커밋은그뒤종료까지이어진다. 각source의UTC정밀도는별도기록했으며일단위값을초단위로꾸미지않았다.
- 본표본18의실제구성은5허용/9정정·분리·되돌림/4기타로초기약6/6/6목표에미달. literalmerge정정은3이다.
- Q6의v1입력오류를보존하고v3를새문맥으로판독했다. 원문에는있는MB05/SW03두필드의보기누락을고친v4두사건재판독6행과v3동일16사건48행을결합했다. key는처음부터불변. 상세protocol-errata/manifest/answer-freeze/exposure-log참조. root채점은자기점검이다.
- session check --fetch는04:07:39 UTC에최신integration2f3593a43f77f6023d0d176bcc0f21905883af45를확인하고통과했다. 배정시base7f66165ad68610278df18855e1196a6cf52b035a와고정입력020SHA는바꾸지않았다.
