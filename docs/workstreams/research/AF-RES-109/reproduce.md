# AF-RES-109 재현·재개 절차

## 1. 고정 입력

결과와 인계의 기준은 HANDOFF가 지정하는 검사 대상 결과 SHA다. 최신 브랜치 tip과 검사한 SHA를 구분한다. 이 디렉터리 밖의 연구 파일이나 PLAN#27 결과를 입력에 섞지 않는다. 운영 의존은105 인계 `1a9d75dc7ae6a179522a5a56e99b002651a2f7bd`, 연구 입력은 `9290320c1e9de33f30857af87640926c4d0f8cff`의 RESULT/followup/returns다.

모집 URL은 frame.csv와 sources.jsonl의 FRAME 행에 있다. 각 저장소2024 issue 검색을 생성시각순80건 가져와 같은 시각은 번호순으로 정렬한다. 검색결과의 상태·댓글·linked PR을 판독자에게 출력하지 않는다. 현재 접근 가능한 첫80의 지문이지 삭제된 사건을 포함한 역사적 전체 집합이 아니다.

requests.jsonl의 `full_input_sha256`은 **title + 두 줄바꿈 + 현재 opening body**의 UTF-8 SHA256이다. 원문 URL의 API `/repos/{owner}/{repo}/issues/{number}`에서 title/body만 꺼내 같은 문자열을 만들고 대사할 수 있다. 편집되어 hash가 다르면 현재판을 예전 입력으로 취급하지 않는다. 전체 원문 캐시는 공개 저장소에 재게시하지 않았다. 원문 내용은 공개 출처에서 다시 읽고, 최초판을 확보하지 못하면 결손을 유지한다.

최초판 복구의 최소 다음 행동은 각 issue의 공개 편집 이력에서 생성시점 본문판을 얻는 것이다. REST updated_at, 현재 bodyVersion, 현재 open/closed 상태는 최초판 증거가 아니다. 실제 첫 본문을 얻으면 두 조건·기지 안을 비교하고 새 연구층/새 봉인으로 재실행한다. 기존 표본을 조용히 바꾸지 않는다.

## 2. 검색을 다시 수행할 때

evidence/start/assignment.json의 요청쌍 순서를 지킨다. R1/R3/R5는 A→B, R2/R4/R6는 B→A다. 각각 새로운 문맥에 같은 원문·같은 모델·언어·검색 도구를 제공한다. 다른 방식 출력·후속결정·공여분야·판독결과는 주지 않는다. 원 실행의 부모 표시 모델은 GPT-6 Astra Pro이며 정확한 immutable backend ID는 미확인이므로 동일 백엔드 재현을 주장하지 않는다.

A는 일반 숙련 모델의 자유 검색이다. B는 부분·조건·작동관계를 분해하고 동종 후보와 분야이름 없는 관계형 질의를 시도한다. A에도 타 분야와 재질의를 허용한다. query3 / 명시개봉6 / 최종링크3 상한을 지키며 실패·재개봉·find/click도 개봉으로 센다. 이 실행은 system2_search_query를 양쪽에 사용했다. 새 엔진 결과를 옛 검색노출 원장으로 덮어쓰지 않는다.

실제 query/시간순노출은 search.jsonl과 evidence/search/*/events.jsonl에 보존한다. 검색결과 상위5와 추가 노출을 그대로 보존하고 결과를 재정렬하지 않는다. engine 자동개봉·토큰·금액은 제공되지 않으면 null이다. 원문을 직접 연 자료와 검색요약만 본 자료를 구분한다. 후속이 자동노출되면 삭제하지 말고 엄격분모에서 분리한다.

공통소비량은 요청별 `min(query_A,query_B)`와 `min(open_A,open_B)`에 도달하기 전의 시간순 prefix다. 최종 후보의 acquisition_event가 prefix 밖이면 공통 결과에 넣지 않는다. token/money가 같았다는 뜻은 아니다. 실제 원개발자 선택이나 실행을 보기 전에 양쪽 출력을 원격 커밋한다.

## 3. 판독·후속과 출처

방법·순위를 가린 후보를 별도 문맥에서 판독한다. 새 문맥이 없으면 자기검토라고 기록한다. 후보별 기존 안, 달라지는 저장단위/호출순서/책임/실패처리, 보존조건, 최소 입력/예상 출력, 원전 전제가 깨지는 경우를 choices.csv에 둔다. 연구자가 만든 입력은 제안된 판별시험이며 실제 실행으로 세지 않는다.

그 뒤 같은 issue의 공개 댓글·timeline·PR·릴리스를 열어 동일 주체·시각·변경대상을 연결한다. 닫힘/감사/나중의 비슷한 수정은 원 요청자의 실행이나 이 연구 추천의 인과효과가 아니다. 과거 릴리스·원전의 판을 따로 확인하고 현재 문서를2024년 이용 가능성으로 소급하지 않는다.

출처 count는 URL수가 아니라 original_work_id/계보로 중복 제거한다. 원 요청6, 검색반환 원설계8, 다른계보 시험·반례6, 사후 외부분야4를 각각 대사한다. 같은 사건 PR/패치·미러·번역·실패·재열람은 추가하지 않는다. 원전의 정확한 절·행·심벌과 한계는 sources.jsonl에서 확인한다.

## 4. 결과판 검사

검사 대상 결과 SHA의 깨끗한 사본에서 다음을 실행한다. 실제 종료값·UTC·환경·관측한 세션 수는 검사 영수증을 따른다. 이 문서의 명령 자체는 실행 증거가 아니다.

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-109/manifest.json --fetch
python -B docs/workstreams/research/AF-RES-109/recalculate.py --check
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

`codex-cloud`는 공통 문서가 쓰는 실행 라벨이고 현재 공유 Linux 환경에서 실행했다면 그 사실을 별도 기록한다. 명시 manifest 검사1개와 `docs/tasks/` 자동 발견0개를 합치지 않는다. 공통55개 등 workbench 기능검사는 검색의 추천효과 시험이 아니다.

검사 후 영수증을 붙인 커밋은 원 결과판과 다르다. 원격 고정 RESULT·원장·대표 출처 기록·이 재현 문서를 다시 읽고, 마지막에는 HANDOFF.md만 단독 커밋한다. 검사 중 원장/본문을 바꿨다면 새 결과 SHA로 필요한 gate를 다시 수행한다.
