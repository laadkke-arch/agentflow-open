# AF-RES-137 고정 범위와 판정 규칙

계획 기준 `1d65b0b7aaef85350df8842dfc05a6be69148b38`, 배정 시 GitHub 통합 head `588e642b99e695e710573b9418b60364d7f3880b`. 이 판에서 AGENTS.md, STATE.md, DOT_AUTOMATION.md, START_HERE.md, RESEARCH_BRIEF.md, RESEARCH_WORKFLOW.md, CLOUD_WORKFLOW.md, 협업 규칙과 dot-control 자기 행을 읽었다. 중앙 행은 AF-RES-137 RUNNING, 시도 1, source_commit/result_commit 미설정, 단일 의존 AF-RES-133. AF-RES-133 중앙 DONE과 [실제 인계 PARTIAL](https://github.com/laadkke-arch/agentflow-open/blob/b84d3a1322f7c247380f960a48b1316d9240db00/docs/workstreams/research/AF-RES-133/HANDOFF.md)을 각각 보존한다. 선행 [결과판](https://github.com/laadkke-arch/agentflow-open/blob/957fffbe6991cef2c5b78f792bd5ea603b1139cd/docs/workstreams/research/AF-RES-133/RESULT.md)의 frame.csv, events.jsonl, contracts.csv 및 evidence/hunks-and-corrections.md에서 이 표본과 타 분야 정정에 해당하는 부분을 읽었다.

| 저장소 | 번호 | 원래 층·순번 | 고정 사유 |
|---|---:|---|---|
| pydata/xarray | 9580 | 본창 10 | Decimal 문맥 유추, 대체 PR 확인 |
| pydata/xarray | 9588 | 본창 15 | 미병합 PR을 통한 시험 제안과 기존 구현 |
| pydata/xarray | 9589 | 본창 16 | 내부 함수 이름과 실제 동일 조작 변경 |
| pydata/xarray | 9618 | 보충 3 | 앞 18개 이후 판독 공백과 대체 구현 |
| scikit-image/scikit-image | 7575 | 본창 12 | NumPy 도구 링크와 다른 작성자의 선행 패치 |
| scikit-image/scikit-image | 7576 | 본창 13 | sparse 문서 경고와 반환 계약 보존 |
| scikit-image/scikit-image | 7579 | 본창 15 | 의존성 extra 이름과 직접 인용한 수정 |
| scikit-image/scikit-image | 7589 | 본창 22 | 기존 Poisson 호출, 문서용 링크, normalization과 clip |

분모는 고정 8 PR(본창 7, 보충 1). 회수 분모는 PR마다 메타데이터, 대화, 제출 리뷰, 인라인, 답글, 커밋, 타임라인으로 나눈다. REST 페이지의 Link 또는 끝 다음 빈 고정 크기 페이지를 기록하고, GraphQL 스레드가 열리면 목록과 개별 답글 커서를 따로 확인한다. REST pulls/comments 답글은 같은 컬렉션의 in_reply_to_id로 복원한다. 커밋 REST 250 상한은 PR 메타데이터와 Git 도달 관계로 대조한다. 비공개·삭제·과거 편집은 현재 공개 페이지와 별도 판정한다. 타임라인이 반복 노출한 대화/리뷰/커밋 ID는 원래 종류에 귀속하고 공개 이벤트 분모를 따로 유지한다.

사건 단위는 제안자·수신자·시각·조작의 조합이다. 같은 스레드의 재표시는 같은 ID, 새 행으로 센 명시적 후속 제안·거절은 고유 ID로 남긴다. 공개 실행 기능, 이름, 미병합/내부 코드, 문서/도구, 유추, 호환성 경고를 기록한다. 봇·단순 상호참조·작성자의 자기 링크·표면 문구를 판독 장부에는 남기되 독립 추천으로 올릴 때에는 구체적으로 제안한 조작이 필요하다. 제안 당시 이미 존재·공개한 대상의 판을 확인한다.

직접 귀속은 구체 제안, 같은 PR 작성자 응답이나 동기를 명시한 발언, 제안 전후 같은 조작의 실제 첫 hunk를 요구한다. 기존 기능의 최초 인지는 별도 명시 발언을 요구한다. 링크의 존재, 답변, 발견, 코드 채택, 배포, 보고한 사람 노동 시간은 각각 판정한다. Git author/committer 시각, 공개 댓글과 공개 푸시 시각, PR 생성과 병합, 태그와 패키지 업로드를 각각 기록한다. 다른 actor, 선행 hunk, 문서 변경, 동작 보존, 명시적 거절, 침묵을 대조한다. 제안 위·아래의 공개 기록을 다 읽어도 당시 편집 전 문장과 실제 개인 노동은 별도 증거가 필요하다.

선행 가설은 #7579의 선언 변경은 귀속 가능하고 병렬 실행 선택은 선행했다는 것이다. #7576은 경고→보존이며 작성자 동일성은 경쟁 가설로 검증한다. #7589의 clip 대안은 출력 계약을 바꿀 수 있으며 #9618의 누락 구간에는 새 적격 반례가 있을 수 있다. 정상·경계 입력은 요인별 입력을 고정하고, 설치판·실행·당사자 보고를 분리한다. 시차는 시·분·초 단위다. 이 고정 표본에서 모집단 채택률을 산출할 수 없다.
