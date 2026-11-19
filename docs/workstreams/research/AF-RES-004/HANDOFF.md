# AF-RES-004#1 HANDOFF

## 1. 식별

- 작업 ID / 시도: **AF-RES-004 / 1**
- 상태: **REVIEW_READY — 지정된 문서 연구·판정팩 인계 범위 완료**
- 작업 종류: web-pro
- 실제 모델·실행 위치: 세션에 제공된 식별은 **GPT-6 Astra Pro**. ChatGPT의 공유 Cloud 작업공간과 GitHub 연결 도구를 사용했다. 계정 UI의 모델명·사용량을 별도로 검증한 것은 아니다.
- 작업자 참조: 이 작업 ID, 저장소, 브랜치로 조회. 외부 native 작업 URL은 제공받지 않아 기록하지 않는다.
- 저장소 / 브랜치: `laadkke-arch/agentflow-open` / `work/research-af-res-004`
- 시작 커밋: `bdc2e052900b1658981dfcec354682f4e1fc29fb` — 시작 시 GitHub에서 확인한 `chore/workspace-foundation` HEAD. 작업 브랜치가 없음을 확인한 뒤 이 SHA에서 생성했다.
- 연구 데이터 실제 검사 SHA: `79a2f76e702c35b2832d245499230f319aab7b5e`
- 인계 작성 직전 마지막 확인·원격 저장 SHA: `677829d6e2abf4facacf665294140ede9644ded8` — VERIFICATION.json 추가 커밋. 브랜치 HEAD와 파일 본문을 다시 읽어 확인했다.
- **최종 result_commit은 이 HANDOFF.md를 추가한 커밋이다.** 위 두 SHA는 검사 입력과 인계 직전 저장점이다. 진행 담당은 최종 브랜치 HEAD/이 파일의 추가 커밋을 조회해 result_commit에 기록한다.
- 마지막 실제 진행 증거: 11개 데이터 파일의 원격 blob 일치, JSON/ID/원문 참조/독립 응답 구조 검사 exit 0, 허용 경로 비교, dot-control blob 불변, VERIFICATION 원격 본문 동일성.
- 인계 작성 전 최종 확인: **2026-11-19 16:37:10 UTC / 2026-11-20 01:37:10 KST**.
- PR: 생성하지 않음. main/foundation 병합·배포를 하지 않음.

## 2. 사용자 요구와 작업 범위

질문은 이름이 비슷한 후보와 실제 요구에 맞는 후보, 다른 분야의 유용한 참고 원리를 어떻게 구별할지다. 고정 문제·후보·기대 판단·반례·독립 평가 절차를 작성하고 공개 자료를 실제 열어 비교했다. 최종 DB/API/검색 스택이나 제품 구현은 결정하지 않았다.

시작 SHA에서 GitHub로 직접 읽은 자료는 AGENTS.md, STATE.md, docs/DOT_AUTOMATION.md, docs/RESEARCH_WORKFLOW.md, dot-control.json의 AF-RES-004, RESEARCH_BRIEF, INDEX, START_HERE, product README/RESEARCH_PROTOCOL/ROADMAP, HANDOFF_TEMPLATE이다.

- [AF-RES-004 배정 원문](https://github.com/laadkke-arch/agentflow-open/blob/bdc2e052900b1658981dfcec354682f4e1fc29fb/docs/automation/dot-control.json)
- [제품 연구 브리프](https://github.com/laadkke-arch/agentflow-open/blob/bdc2e052900b1658981dfcec354682f4e1fc29fb/docs/product/RESEARCH_BRIEF.md)
- [연구 작업 규칙](https://github.com/laadkke-arch/agentflow-open/blob/bdc2e052900b1658981dfcec354682f4e1fc29fb/docs/RESEARCH_WORKFLOW.md)

`depends_on: []`이므로 의존 작업 result_commit의 인계는 없다. 과제에 명시된 경계 확인용으로만 [AF-DOT-002의 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/06a57eba60c64389c614b5ce01238d9c4e337fbf/docs/workstreams/dot-trial/AF-DOT-002/HANDOFF.md)를 읽었다. 다른 새 AF-RES 결과는 열람하거나 선행조건으로 삼지 않았다.

**편집 경로는 `docs/workstreams/research/AF-RES-004/`뿐이다.** dot-control.json, 공통 색인·계약, 제품 코드, 기존 AgentFlow Studio는 수정하지 않았다. GitHub 파일 API로 연구 산출물을 묶음별 커밋했으며, 공유 작업공간은 전체 Git checkout이 아니다.

## 3. 실제 변경과 진입점

| 파일 | 내용과 이유 | 확인 |
| --- | --- | --- |
| [PROTOCOL.md](PROTOCOL.md) | 4축·4라벨·보류/채점·블라인드 절차. v1 사전 동결, v1.1 적용 층위 명확화 | 동결 커밋 순서와 변경 이력 |
| [CASES.json](CASES.json), [EXPECTED.json](EXPECTED.json) | 4개 문제·18행. 입력과 답 분리, 조건별 근거·반례·최소 확인. 현재 v1.2 | JSON/ID/참조 검사, 원문 대조, 원래 v1 블라인드와 수정 검토 |
| [sources.json](sources.json), [methodology-notes.json](methodology-notes.json) | 기능/규격 27개 + 방법론 6개. 각 URL·읽은 범위·확인 내용·한계 | 직접 열람 및 제한 기록. 실패/중복 열람 제외 |
| [source-pins.json](source-pins.json) | 공식 원본 문서 10개의 commit/path/blob SHA | 작성자도 10/10 고정 원본 재조회·blob 일치 |
| [RESEARCH.md](RESEARCH.md) | 결론·대안·비용/전제·반례·분야 간 조합·미해결·색인 제안 | 실제 읽은 원문 URL와 사례 연결 |
| [blind-review-a.json](blind-review-a.json), [blind-review-b.json](blind-review-b.json) | 기대 답을 숨긴 18행씩의 원래 내부 판정 | A는 26자료, B는 27자료 직접 열람. 원판정 불변 보존 |
| [revision-review.json](revision-review.json), [REVIEW.md](REVIEW.md) | 이견·채택·v1.1 잔여 결함·v1.2 한 항목 후속 확인 | 원응답/입력 SHA/범위/미실시와 수정 이유 보존 |
| [VERIFICATION.json](VERIFICATION.json) | 실제 명령·입력 SHA·파일 해시·exit code·원격 경로 비교·미실시 | 아래 §4 |
| HANDOFF.md | 이 인계. 마지막 커밋으로 추가 | 저장 뒤 최종 HEAD와 본문을 읽기 전용으로 확인 |

자료는 **서로 다른 33개**다. 31개는 명시한 본문 절을 직접 읽었고 M01/M03 두 개는 공식 초록·서지만 읽었다. 전 페이지 완독을 뜻하지 않는다. 검색 결과만 본 자료, 접근 실패, 문서의 Git 사본 10개, 검토자의 반복 열람, 저장소 운영 지침은 추가 자료로 세지 않았다. 확인일은 UTC 2026-11-19 / KST 2026-11-20이다.

## 4. 실제 검증과 미실시

### 실제 수행

검사 입력은 `79a2f76e702c35b2832d245499230f319aab7b5e`다. 정확한 실행 명령은 VERIFICATION.json의 `executed_check.command`, 전체 출력은 `executed_check.log`에 있다.

- 인라인 Python으로 JSON 8개를 파싱하고 문제 4개·입력/기대 각 18행·자료 ID 27개·방법론 6개·pin 10개를 확인했다. 중복/누락, source 참조, 조건 ID·상태, 검토 A/B 순서와 필수 필드를 검사했다. **exit code 0**.
- 데이터 파일 11개를 해당 원격 커밋에서 다시 읽고 로컬 Git blob SHA와 **11/11 byte 일치**를 확인했다. 각 SHA-256도 기록했다. 로컬 말단 LF 차이가 있던 3개 파일은 원격 커밋 내용에 맞췄다.
- 시작 SHA→검사 SHA의 GitHub compare에서 변경 11개가 모두 owned_path 내부이며 공통 파일 변경이 없음을 확인했다.
- dot-control.json의 시작/검사 커밋 blob은 모두 `881fc991a56d7bb52ebdf2aa06a7876c4d0ecfd0`다.
- VERIFICATION은 후속 커밋 `677829d6…`에서 원격 본문을 다시 읽어 저장 내용과 일치함을 확인했다.
- 최초 블라인드 입력/기대 답과 현재 v1.2를 구분한다. 최초 결과는 A/B 각각 라벨 18/18 일치지만 세부 H 이견과 후속 결함을 실제로 발견·기록했다.

이 검사는 **산출물 구조와 커밋된 파일의 무결성** 검사다. 후보의 의미적 유용성을 자동 채점하는 평가기를 만든 것이 아니다. 뒤에 추가하는 VERIFICATION/HANDOFF 두 메타데이터 파일이 앞의 11파일 검사에 포함됐다고 주장하지 않는다. 최종 저장 뒤 브랜치 HEAD·인계 본문·변경 경로를 다시 확인한다.

### 수행하지 못했거나 범위 밖인 검사 — 명령과 입력

전체 checkout과 scripts가 없는 GitHub 파일 API 기반 작업이어서 다음 저장소 공통 검사를 실행하지 않았다. **git status clean, 전체 CI, 백업 회귀 검사 통과를 보고하지 않는다.** 진행 담당이 완전한 checkout과 저장소가 정한 실행 환경에서 후속 gate로 실행할 경우 입력은 이 브랜치의 **최종 result_commit**이다.

```bash
# 입력: 최종 result_commit을 checkout한 완전한 laadkke-arch/agentflow-open 저장소
python scripts/check.py --require-git
python scripts/cloud_check.py --environment codex-cloud --fetch-contract
```

이 명령은 시작 SHA의 AGENTS.md에 있는 실제 공통 명령이다. 실행 환경과 계약이 필요한 검사는 docs/CLOUD_WORKFLOW.md의 조건을 함께 확인해야 한다. 실행 가능한 새 PROJECT/test/demo는 만들지 않았으므로 `workbench run PROJECT test`나 `workbench.session start / check --fetch`에 임의의 PROJECT/manifest를 넣지 않았다. 문서 연구를 위해 공통 계약을 바꾸지도 않았다.

브라우저 오프라인 재진입, broker 장애 주입, SQS API 호출, Python adapter, backup 복원 등의 D3/D4 시험은 **미실시**다. 이번 기대 판단은 D1이므로 이를 완료 주장에 사용하지 않는다. 향후 별도 실행 과제가 배정되면 CASES의 버전·고정 입력·실패 시점과 EXPECTED의 `minimum_next_check`를 받아 실행용 manifest/명령을 구체화해야 한다. 사람 사용자 시험·다른 모델 계열 검증·새 holdout 평가는 미실시다.

## 5. 판단과 근거

핵심 제안은 **문제 × 후보 × 역할 × 설정 × 근거**를 판정 단위로 삼고, 출처 연결(L), 원문 뒷받침(E), 필수 조건별 충족(H), 전이 관계(T)를 분리하는 것이다. 링크 생존이나 제품 인기로 결정적 제약 위반을 상쇄하지 않는다. 필요한 설정이 없으면 부적합으로 단정하지 않고 자료 부족으로 남긴다.

현재 18행의 라벨은 문서상 직접 적합 **7**, 조건부 전이 **3**, 알려진 제약 위반 **6**, 자료 부족 **2**다. 이는 작성자의 문서 기반 기대 판단이고 검증된 실효성·제품 순위가 아니다. CRDT/저장, FIFO 송신 중복 제거/외부 효과, 시간당 처리율/동시 개수, 단일 mirror/과거 판, Merkle 포함 증명/실제 복원을 구분하는 반례를 포함한다.

블라인드 검토의 라벨 일치만으로 끝내지 않았다.

- R03의 patch log 보존을 본문 복구로 확정한 H2, R04의 local setter를 offline 편집 수명으로 확정한 H1을 unknown으로 좁혔다.
- 총 경과시간과 visibility 한계를 명시하고, 참고 설계의 조건부 충족과 미관측 구현을 별도 필드로 구분했다.
- B의 v1.1 비블라인드 수정 검토가 다시 지적한 R12의 producer 대기 연결을 v1.2에 **새 설계 조건**으로 추가했다. 이 사실과 v1.1의 잔여 이견을 보존했다.
- B가 v1.2 R12만 다시 확인해 문서상의 연결 누락이 해소됐다고 응답한 기록은 REVIEW §5에 있다. 이를 새 블라인드/독립 합의/제품 시험으로 세지 않았다.

실행 증거의 상한은 후보에 대해 **D1 문서·규격 열람 + 명시된 합성 조건에서의 논리 반례/전이 가설**이다. 방법론에는 정보검색 평가, 사실/인용 검증, 인지과학의 유추를 비교했고, 제조업·스트림 프로토콜·인증서 로그의 참고 원리를 추가 조건과 실패 경계에 연결했다. 공개 원문·합성 사례만 저장했으며 새 유료 API·계정 변경·상시 수집·배포는 수행하지 않았다. 최신 보안 추천이나 라이선스 채택 판단을 하지 않았다.

다른 새 작업과의 구현 충돌은 만들지 않았다. 최종 제품 설계자가 선택·폐기·재조합할 연구 제안이며 사용자 확정 요구를 대체하지 않는다. 공통 색인 변경은 다음 **제안만** 남긴다.

| ID | 질문 | 상태 제안 | 진입점 | 경계 |
| --- | --- | --- | --- | --- |
| AF-RES-004 | 이름 유사성·요구 적합·타 분야 전이를 어떻게 구분하는가 | REVIEW_READY | docs/workstreams/research/AF-RES-004/RESEARCH.md | 의존 없음; D1 기대 판단·내부 검토, D3/D4 미검증 |

## 6. 다음 담당자의 첫 행동

1. **이 작업 브랜치의 최종 HEAD와 이 HANDOFF를 GitHub에서 다시 읽는다.** 이 파일을 추가한 최종 커밋이 result_commit이다. 예를 들어 이미 허용된 저장소 checkout에서 읽기용으로 다음을 수행할 수 있다.

   ```bash
   git fetch origin work/research-af-res-004
   git rev-parse FETCH_HEAD
   git show FETCH_HEAD:docs/workstreams/research/AF-RES-004/HANDOFF.md
   git diff --name-only bdc2e052900b1658981dfcec354682f4e1fc29fb FETCH_HEAD
   ```

2. 데이터 검사 SHA `79a2f76e…`와 최종 HEAD 사이가 VERIFICATION/HANDOFF 메타데이터 추가뿐인지 확인하고, 필요하면 §4의 공통 검사를 완전한 checkout에서 실행한다. 실행하지 않은 gate를 통과로 입력하지 않는다.
3. 진행 담당이 검토 후 AF-RES-004의 result_commit/완료 근거와 색인 제안을 자기 허용 범위에서 반영한다. **본 작업에서는 dot-control.json을 수정하지 않았다.**
4. 연구 내용을 읽을 때 RESEARCH → REVIEW → 필요한 CASES/EXPECTED·원문 순서로 읽는다. 새 블라인드 평가자는 EXPECTED·RESEARCH·REVIEW를 먼저 보지 않고 PROTOCOL/CASES와 원문만 받도록 분리한다.
5. 현재 문서 수정 범위의 미해결 차단 사유는 없다. 후속 실효성 연구는 독립 holdout 또는 D3/D4/사용자 과제를 별도 배정한다. 이번 인계를 위해 추가 사용자 확인은 필요하지 않다.

새 대화가 이 자료를 자동으로 기억하거나 읽었다고 가정하지 않는다.
