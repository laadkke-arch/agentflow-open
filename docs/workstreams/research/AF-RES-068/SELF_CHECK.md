# 자체 검토

판독·실행·검산 담당은 같은 Codex Cloud 연구자다. 통합 대상 결정이나 독립 검토를 아직 받지 않았다.

| 질문 | 주장과 직접 근거 위치 | 반대 근거·탐색 범위 | 답이 달라지는 관측·남은 공백 |
| --- | --- | --- | --- |
| Q1 | 두 GitHub 목록 6쪽과 본문 120건에서 순서를 검사했고 6자리씩 확정했다. release 3/2/7층 및 원 입력/보고/해석을 [frame](frame.csv), [issue provenance](evidence/issue-provenance.json), [배포 메타데이터](evidence/pins.json)에 대조했다. | #1874는 object/optional을 서로 함께 요구하는지 불명. #1883은 대입 진단만 있다. GraphQL 403, issue edit URL 404, GH Archive·Wayback 미입수. 최초 제목 변경과 본문 변경을 구별했다. [원 요청 #1874](https://github.com/ajv-validator/ajv/issues/1874) · [탐색](search-log.jsonl) | 변경 이력이 있는 선두 후보의 opened raw 또는 공개 UserContentEdit의 초기 diff와 당시 lock. C 첫 심볼/포함 순서가 달라지면 해당 자리 재생. 현재 시각 일치 2/12는 편집판 보관의 대리 지표다. |
| Q2 | [rules](rules.json), [selector-cases](selector-cases.json) 및 [mentions](mentions.jsonl)로 제목/선언 인덱스만 사용해 36행을 만들었다. [A04 C 출처](https://github.com/ajv-validator/ajv/blob/b2bf7504bab515db60ad276dc015b9c14f775607/docs/options.md?plain=1#L343-L376) | A04 code는 일반 명사이고 다음 validateSchema도 wrapper/엔진의 뜻이 다르다. A06은 너무 짧은 입력 span에서 L3 const를 놓쳤다. L03은 URL fragment를 제거하면 C 없음. [사후 변화](evidence/postseal.json) | 최초 본문의 공용 이름에 좁은 구문 조건을 적용하고 재생한다. 여전히 같은 메타데이터로 첫 위치가 바뀌면 해당 알고리즘의 안정성을 다시 본다. |
| Q3 | [경계 결과](evidence/boundary.json) 8행, [두 cold cache 비교](evidence/replay-comparison.json), [창](windows.jsonl) 및 [행동](evidence/route-actions.jsonl). raw·표시 크기, 쪼갠 코드, 잘린 행과 참조 창을 실제로 대조했다. | 적격 둘째 후보 0은 합성 깨진 앵커의 실패와 다르다. VuePress가 있는 두 실제 창은 fence 투영·code 계수에서 결손이다. 동일 해시와 overlap을 [실제 노출](evidence/actual-exposure.json)에 남겼다. | 원형 code-group 지원과 한 번의 실제 표시를 독립 판정자에게 제공해 두 창으로 증거가 늘어나는지 확인한다. GitHub 화면 픽셀, RST 모든 문법 및 사람 시간 미실측. |
| Q4 | [판정](judgments.csv)에서 환경 D 세 개와 T 한 개의 같은 경로와 원위치를 확인했다. [A01 B](https://github.com/ajv-validator/ajv/blob/b2bf7504bab515db60ad276dc015b9c14f775607/docs/guide/schema-language.md?plain=1#L13-L77) | L02 C는 이름만 나열한다. A01 C는 일반 생성자. 가명 창을 혼합했지만 조사자가 요구를 먼저 알고 있었다. [처음 판독](evidence/blind-readings.jsonl) · [A01 C](https://github.com/ajv-validator/ajv/blob/b2bf7504bab515db60ad276dc015b9c14f775607/docs/api.md?plain=1#L7-L72) | 최초 문맥의 오염이 없는 독립 판독자가 동일판 같은 창으로 두 조건과 도입 전제를 인용할 때 공동 확인을 바꾼다. |
| Q5 | 실행 전 [봉인](evidence/doc-seal.json)과 실제 [16군](runs.jsonl) 및 타르볼·lock을 대조했다. A01 G3은 선언판과 다른 minContains 적용, L01 G3은 객체 유형, L02 G1은 키와 값/형을 나눌 수 있다. | Node24 JSON-LD 로더 실패를 버리지 않고 같은 8입력의 Node14 성공과 연결했다. A02 처음 예외를 별도의 compile 단계 진단으로 확인했다. [초기](evidence/runtime) · [회복](evidence/runtime-recovery) | 작성자의 정확 배포 lock·Node·wrapper와 mode에 두 대조 입력을 넣어 실제 값 또는 컴파일 성공이 달라지는지 확인한다. |
| Q6 | [A06 const 원문](https://github.com/ajv-validator/ajv/blob/979d46b1585a92e4343bf9e4505f61139c3eecf8/docs/json-schema.md?plain=1#L1014-L1044), [원시험](https://github.com/ajv-validator/ajv/blob/979d46b1585a92e4343bf9e4505f61139c3eecf8/spec/extras/%24data/const.json?plain=1#L3-L49), [B의 환경 차이](evidence/metrics.json). 같은 값과 숫자/문자열 반례를 봤다. | 빈 객체도 허용하는 예에는 required가 없다. L04 C의 위임 검사에서 공백 제한이 잘렸고, L06 C 뒤 RDF 포맷은 budget 밖이다. [공백](https://github.com/digitalbazaar/jsonld.js/blob/6a9ecfc3da5f986672ba70d58a4912adfb5beebc/lib/url.js?plain=1#L276-L291) · [RDF 절](https://github.com/digitalbazaar/jsonld.js/blob/6a9ecfc3da5f986672ba70d58a4912adfb5beebc/README.md?plain=1#L277-L304) | 두 조건, 모드 및 그 반대 예를 모두 가진 짧은 본문이 봉인된 선택에서 처음 두 창에 도달하는지 새 샘플로 확인한다. |
| Q7 | [The Met JP1847](https://www.metmuseum.org/art/collection/search/45434) Object Details 및 [AIC 1926.417 API](https://api.artic.edu/api/v1/artworks/28560)와 각각 넓은 기관 글을 비교했다. [대조](evidence/museum-comparison.md) · [비용](evidence/costs.json) | 제목 입구가 인출 추정 또는 판의 연대·선후를 더 잘 보여 준다. 정확 번호 질의 응답은 미확인. 물건·웹 문서 버전·다운로드를 구별했다. | 검색·직접 링크가 실물 접근과 필요한 맥락에 도달하는지 각각 확인한다. 사람 읽기 시간은 계측 후 추가한다. |

## 첫 재개 명령

공개 GitHub GraphQL에 적절한 읽기 접근이 있는 환경에서 초기 두 번호부터 실행한다. 응답의 편집 시각·diff 순서와 원본 삭제 여부를 보존한다. 편집 이력이 없고 최초 상태가 확인되면 기존 SHA와 대조한다.

```sh
gh api graphql -F owner=ajv-validator -F repo=ajv -F number=1872 \
  -f query='query($owner:String!, $repo:String!, $number:Int!) { repository(owner:$owner,name:$repo) { issue(number:$number) { createdAt lastEditedAt includesCreatedEdit body userContentEdits(first:100) { pageInfo { hasNextPage endCursor } nodes { editedAt deletedAt diff } } } } }'
```

두 번째 입력은 owner=digitalbazaar, repo=jsonld.js, number=465다. API에서 못 받으면 GH Archive의 해당 UTC 시간 opened 이벤트에서 payload.issue.body, payload.issue.title, created_at과 repo/issue 번호를 대조한다. [GH Archive 형식](https://www.gharchive.org/) · [수집 시각](frame.csv)

경로를 재개할 때는 [재현 명령](reproduce.md)으로 빈 캐시 결과를 만든 뒤 `python -B docs/workstreams/research/AF-RES-068/audit.py --report --replayed <새 결과 위치>`로 원장과 표를 검산한다.
