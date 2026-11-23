# AF-RES-060 재생·판 식별·비용 산식

## 1. 고정 입력

소유 경로에서만 산출물을 쓴다. 저장소 루트의 최신 실행 계약은 manifest.json에 고정되어 있다. 056 결과판은 `2f8ec01e6b52bef4fc3cd003b1690383b6496526`, 인계판은 `4b7ae5ce472f3a194acaadc950190bb005289441`이다. inputs/af-res-056의 9개 핵심 파일은 evidence/input-byte-audit.json에서 원 Git blob과 바이트까지 맞춘다. 서식 끝에 추가되었던 줄바꿈 한 개의 초기 복제 정정은 의미·순위를 바꾸지 않았다.

F0의 두 목록판은 Schema `1a415f9d36c34fe0eae271c05f86a459746ed00b`, LD `f9e9288d7c41db5643386effff1ff2a3fe820237`이다. 40+22행의 순서는 인수된 catalog.csv가 기준이다. 현재 목록이나 과거 태그 유니버스를 다시 만들어 대체하지 않는다.

## 2. 네 조합의 같은 순위

네트워크가 필요 없는 재생이다. 연구자 판단·공급자 실행을 대신하는 검사가 아니다.

```bash
python -B docs/workstreams/research/AF-RES-060/replay.py --baseline-only
python -B docs/workstreams/research/AF-RES-060/replay.py
```

두 번째 명령은 requirements.json, vocabulary.csv, features.csv가 모두 봉인된 뒤 사용한다. 이것은 matches.csv와 순위 단계의 slots.csv 및 path-plan을 다시 쓰므로 최종 판정이 든 슬롯을 보존하려면 별도 checkout에서 실행한다. 기존 고정 결과파일을 실행 전후 비교한다. 최초 결과가 없는 새 대화에서는 재현을 위해 상위 순위부터 다시 해석하지 말고 HANDOFF의 고정 SHA를 읽는다.

정규화는 casefold, ASCII 하이픈을 공백으로 대체, 연속 공백 축약이다. `(?<!\w)구(?!\w)`의 연속구 일치를 쓰며 어간·수·품사·번역은 바꾸지 않는다. L은 원문 기능구, V는 L과 사전 허용 정의관계만이다. 여러 구는 OR로 후보를 만든다. 분야의 원게시순으로 돌고 정확 destination_url 중복만 제거한다. URL fragment/query, 같은 엔진의 여러 인터페이스는 순위에서 합치지 않는다. 각 공급자의 원표기 기능0–3개를 F0 뒤에 붙이는 것만 F1의 차이다. 개념 URI를 기능 문자열로 복제하지 않는다.

48행은 12요구×L/V×F0/F1이다. 144슬롯은 각 비교의 상위3 자리다. 미모집은 미실시이고 매치0은 관측 무매치다. 풀1–2의 남는 자리는 풀 소진이다. 후보 미확인과 빈 자리는 같은 정확도 분모가 아니다.

## 3. 같은 문서판과 창의 재사용

공급자판은 features.csv와 evidence/features-*/features.json의 40자리 commit, release tag, 원 URL, 실제 fixed URL로 식별한다. 056에 같은 공급자판이 있으면 그 SHA를 우선한다. 이외에는 F0 스냅샷 시각 이하 정식판 우선이며 정식판을 확인하지 못했지만 commit을 고정한 경우 그 한계를 표시한다. 현재 README에 아무 내용이나 섞지 않는다.

원문 응답 SHA256, 표시창 SHA256, word count, 시작절 및 본문 링크 순서를 함께 보존한다. JSON/코드는 제목이 없어도 시작부터 표시 whitespace500단어라는 사전 규칙을 사용한다. Markdown 구문·링크URL·fence는 표시 단어에 세지 않고 코드 자체는 센다. 실제 편집 렌더러와 기계적 정정 기록은 각 하위 evidence에 남긴다.

편집 기능창은 이용자의 첫창이 아니다. 이용자 첫창은 원대표 URL에 대응하는 고정 README의 첫 제목(또는 명시 fragment)에서 시작한다. P1은 첫 문서만, P2는 첫창의 첫 정보링크, P3는 둘째 정보링크를 각각 이어간 경로다. 같은 경로에서 최대 두 문서만 조건 근거로 쓴다. 다른 경로의 C1/C2를 이어붙이지 않는다. 같은 raw response에서 만든 창은 query/field 조건들 사이에서 재사용한다. 같은 캐시의 재해석을 새 외부문서 취득으로 더하지 않는다.

F1의 편집 출처 링크로 바로 가는 사후직링크와 상위4·기능1개·넓은말/파생형 감도는 주표와 분리한다. 표준·테스트의 기대값을 읽은 것, 특정 버전의 실행, 실제 사용자의 성공은 서로 다른 근거다.

## 4. 비용과 성과의 단위

비용은 서로 다른 분모로 보고한다.

- 편집 시도 행 = 62. 기능 추가행 = added_features_json 길이가1 이상인 행. 같은 행의 기능 세 개를 문서 세 개로 세지 않는다.
- 본문 취득 요청 = 성공·실패 원문 HTTP/connector 요청. metadata 요청(릴리스·태그·commit·디렉터리)은 별도다. 같은 URL 재시도는 원문 요청 비용에는 남기되 고유저작에는 더하지 않는다.
- 읽은 원문/창 = 실제 표시해 독해한 문서·창. 내려받은 bytes는 읽은 words가 아니다. 행당 최대2본문, 창당 최대500표시단어다.
- 편집 읽기량 = 전수 행의 독해창 word count 합계. 공유 문서를 두 행에서 읽는 행노출 비용과 고유문서 비용은 따로 센다.
- 이용자 도착문서 = 허용 P1/P2/P3에서 실제 취득한 고유응답. 경로당 행동 최대2와 전체경로의 합계는 다르다. 실제 사람의 클릭시간·만족·채택은 측정하지 않았다.
- 판 갱신 시 재확인 항목 = 기능 추가행별 원표기0–3개·지원역할/engine·판·창위치·개념관계·링크생존. 갱신시간/화폐비용을 관측하지 않은 경우 숫자를 추정하지 않는다.

기존 F0 구축비용은 이 작업에서 재실측하지 않았다(재구성 제외). 이번 F0 인수비용과 F1의 신규 편집비용을 비교하며 원래 F0를0비용으로 구축할 수 있었다고 주장하지 않는다.

성과는 비어 있지 않은 요구수, 전체후보, 상위3 채움, 같은경로 완결/부분/오답/미확인을 분리한다. 반복된 후보를 독립 표본으로 보는 유의성 검정은 하지 않는다. 정확도는 분모가0이거나 진위미확인 후보를 포함할 때 산출 불가다. 확정 오답0도 실제판정 분모가 없으면 오탐률0이 아니다.

## 5. 실제 검사와 재개

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-060/manifest.json --fetch
```

검사 시각·대상 HEAD·종료코드·stdout/stderr는 evidence/verification에 저장한다. 이 검사는 경로·계약·의존 최신성의 기계검사이며 연구의 사실성과 충분성을 인증하지 않는다. 고정 RESULT 및 수용원장을 GitHub에서 다시 열어 hash/byte를 대조한 뒤 HANDOFF를 마지막 단독파일 커밋으로 발행한다. 실행하지 못한 원환경 시험이나 원문 결손은 HANDOFF에 최소 입력·명령을 남긴다.

## 6. 최종 원장 재집계 순서

현재 결과를 바꾸지 않고 확인할 때는 아래 read-only 재생 검사를 쓴다. 자체 영수증만 owned_path 아래 기록한다. 네트워크 요청·공급자 실행은 없다.

```bash
python -B docs/workstreams/research/AF-RES-060/verify_local.py
```

고정 결과의 별도 checkout에서 산출물을 처음부터 재생할 때는 다음 순서다. 원시 HTTP 전체 cache는 출판하지 않았지만 순위 입력, 독해 창, 문서/창 SHA, 원URL/판, 모든 관측 JSON은 출판했다. 아래 명령은 고정 관측을 다시 **집계**하며 새로운 독립 독해나 구현 실행이 아니다.

```bash
python -B docs/workstreams/research/AF-RES-060/replay.py
python -B docs/workstreams/research/AF-RES-060/assemble_sources.py
python -B docs/workstreams/research/AF-RES-060/analyze_comparisons.py
python -B docs/workstreams/research/AF-RES-060/summarize_sensitivities.py
python -B docs/workstreams/research/AF-RES-060/build_acceptance.py
python -B docs/workstreams/research/AF-RES-060/render_report.py
python -B docs/workstreams/research/AF-RES-060/verify_local.py
```

`replay.py`는 slots를 순위 단계 상태로 다시 쓰므로 `analyze_comparisons.py`까지 실행해야 최종 판정이 돌아온다. JSON 집계의 실행 UTC는 달라질 수 있으나 frozen feature/query/match bytes와 실제 분모는 같아야 한다. `assemble_features.py`를 다시 실행해 새 시각의 F1 봉인처럼 만들지 않는다. F1 바이트는 `3ae6f5bab20cf121ecf9197aa38f4f666734d3a5d2a7a53e7022c7d160739dd7`이다.

세 관측 원장은 evidence/paths-schema/observations.json(51경로), paths-ld/observations.json(27), root-paths/observations.json(6)이다. root6 중 JS-4의3은056 인수, JS-6의3은 새 독해다. 전체28쌍/84경로이고 부분3은 JS-6/Ajv의 같은 첫창을 공유한다. strict literal 감도에서는 부분0이다. 전체48비교의18슬롯 중 부분1·미확인17이며 정확도 분모는0이다.

## 7. 비용·출처 계보의 실제 재계산

편집 비용은 features.csv의 행별 `primary_document_actions_attempted`, `logical_windows_read`, `logical_display_words`, `metadata_requests_observed`, `extra_interpretation_display_words`를 합친다. 물리 요청72와 논리 행동78은 다른 값이다. 논리 읽기30,943단어와 고유 저장창28,943단어, 추가 해석1,411단어를 따로 보고한다. Metadata는 최소190이며 정확한 전체 요청수가 아니다.

경로 비용은 각 관측의 documents/cost와 팀 summary에서 같은 응답 재사용을 구분해 합친다. 새 논리행동130+인수5=135, 알려진 지정창 단어51,095+인수2,000=53,095, 인수JSON1창의 단어수는 미확인이다. SC-036 P3의 고유 초과111단어는 두 경로 논리합222단어에 해당한다. 새 본문29요청·metadata6요청이며 F1 캐시를 읽은 것은 새 네트워크0이다. 팀별 고유창 합은 공유 응답/fragment가 겹치므로 전역 고유 독해량으로 더하지 않는다. [cost-audit](evidence/cost-audit.json).

출처는 사건193, 실질 직접독해165, 계보113원저작/신규95다. 같은 저작의 fragment·번역·판·LOC JSON/XML을 합치고, front matter·패키지 metadata만 읽은 창을 substantive quota에서 뺀다. `eligible_for_new_primary_minimum=false`는 같은 연구 안 재사용을 뜻하기도 하므로 무조건 실제독해 제외로 해석하지 않는다. 같은 엔진 wrapper의 글은 별도 저작이더라도 독립 엔진 증거가 아니다. 최종 계보 정정은 [감사](evidence/review/final-audit.md)에 있다.

## 8. 판정 해석과 예산 결손의 재현

JS-6/Ajv C2는 문서의 object.properties.bar.type=string에서 일반 속성명만 id로 바꾼 조건부 전이다. 다른 타입·연산·런타임까지 전이하지 않는다. 이는 표준 정의 또는 일반 준수만으로 두 조건을 확인한 것이 아니며 실제 id 실행은 미실시다. [미실행 fixture/명령](evidence/next-checks/README.md)을 쓸 때도 현재 주판정과 분리한다.

두611/500 초과 경로와 인수 JSON 경계 미확인을 원장에 유지한다. static HTML renderer의 whitespace split은 CSS/JS를 실행한 실제 브라우저 픽셀 표시 측정이 아니다. 동일 응답과 선언된 renderer로 창을 재생할 수 있다는 범위만 주장한다. 추가 독해·코드 실행·새 판 교체가 필요하면 새 사건·새 감도로 기록하며 기존 주표에 끼워 넣지 않는다.
