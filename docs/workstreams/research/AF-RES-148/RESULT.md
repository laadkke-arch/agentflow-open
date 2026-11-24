| 사건·저장소·판 | 저자 원문 주소·선택 구간 | 바꿀 동작·보존 속성 | 이웃/형제 자료 출처 | 기대값의 주체·가림·미확인 |
|---|---|---|---|---|
| E1 Pandoc 3.1.6 | [R01](https://github.com/jgm/pandoc/issues/9296), Maxwell's equations table, attachment | MediaWiki→LaTeX의 align 오류 제거; 정확한 수식·표 보존 의무는 추론 | [원첨부](https://github.com/jgm/pandoc/files/13804331/Maxwell.s_equations.txt) 미열람; B/C 결측 | 현재 본문 작성자 오류 보고; 정확 기대 출력 없음, 최초판 없음 |
| E2 Pandoc 3.1.11 | [R02](https://github.com/jgm/pandoc/issues/9305), table.md 둘째 td/pre | 텍스트 탈락 방지, 첫째 셀과 순서 유지, plain 출력 | 동일 입력 첫째 td; 이미 A에 있음. 실제 무관 형제 결측 | 현재 저자 명시 expected 두 줄, actual 한 줄; 패킷 초안에서 expected/actual 가림, 수집자는 이미 봄 |
| E3 Pandoc 3.1.11 | [R03](https://github.com/jgm/pandoc/issues/9308), code.md fence | info string이 포함된 code 인식, 코드 문자 보존 | [T02](https://spec.commonmark.org/0.30/#fenced-code-blocks) 작성자 참조; 주변 실제 입력 및 무관 형제 없음 | 현재 저자 expected 들여쓴 코드 한 줄; hl_lines 의미 보존까지 요구하지 않음; 수집자 선노출 |
| E4 Prettier 3.1.0 | [R04](https://github.com/prettier/prettier/issues/15853), Input addCartItem | nested arrow 추가 indent; 의미 보존은 추론 | 본문 eslintrc.json의 @stylistic/js/indent vs no-console 등 rules; B/C 66자 | 저자의 Output/Expected는 updateCartItem; 동일 input 아님; expected 가림 초안, 독립 없음 |
| E5 Prettier 3.1.1 | [R05](https://github.com/prettier/prettier/issues/15868), class A 필드, typescript parser | declare를 private 앞에 유지, readonly/name/type 보존 | 원문 한 필드만; 소비 compiler/version 및 무관 형제 없음 | 현재 저자 입력=기대, 결과 modifier 순서 바뀜; playground/expected 가림 초안 |
| E6 Prettier PR #15870 | [R06](https://github.com/prettier/prettier/pull/15870/files), head a8701062856351f7e2e2f8bbb77b2e7c1cb9b1c3 | 긴 union 처음에도 pipe, 기존 짧은 union 형식 보존 | 현재 diff에 실제 이웃은 있으나 후속 정답 노출이므로 패킷에서 제외 | PR 작성자 구현 및 리뷰, 원요청 #14234의 당시 기대는 결측; 최초 parent 미확인 |
| 단위·분모·결측 | 잠정 사건 6/6 (저장소별 3); 후보창 60행 중 개별 확인 18/60 | 원작성자 현재 본문·같은 입력의 명시 expected 3/6(E2,E3,E5); E4 불일치, E1 결측, E6 후속 PR | 가림 패킷 초안 18행; 비영 추가 B 2/6, C 1/6, 동일 길이 실제 후보 1/6 | 최초판 0/6, 독립 판독 0/18; [frame.csv](frame.csv), [author-evidence.csv](author-evidence.csv) |

| 사건·전달 면·판독자 | 택한 링크 또는 한 질문 | 실제 열린 절·주소 | 예상 출력·A/B가 바꾸는 선택 | 공개 뒤 확인값·반례 | 오승인·보류 |
|---|---|---|---|---|---|
| E1 A/R1 B/R2 C/R3 예정 | 미실시 | 없음 | 없음 | R01 오류만, 정확 기대 결측 | 판정 불가 |
| E2 A/R2 B/R3 C/R1 예정 | 미실시 | 없음 | 없음 | R02 첫째·둘째 셀 값/순서; author report, no replay | 판정 불가 |
| E3 A/R3 B/R1 C/R2 예정 | 미실시 | 없음 | 없음 | R03 plain 코드; T02 info 의미 미규정 | 판정 불가 |
| E4 A/R1 B/R2 C/R3 예정 | 미실시 | 없음 | 없음 | R04 input/expected 다른 함수; B 실제 ESLint rule, 효과 미확인 | 판정 불가 |
| E5 A/R2 B/R3 C/R1 예정 | 미실시 | 없음 | 없음 | R05 선언 순서; 컴파일 미검증 | 판정 불가 |
| E6 A/R3 B/R1 C/R2 예정 | 미실시 | 없음 | 없음 | R06 후속 patch; 원저자 기대 미확인 | 판정 불가 |
| 단위·분모·결측 | 독립 판독 0/18, 결측 18/18 | 실제 판독자 개봉 0회; 수집자 기술자료 읽음은 별도 | A/B 질문 발송 0, 실제 선택 전환 산출 불가 | 독립 봉인 및 개봉 순서 미성립 | 오승인율·보류율 산출 불가; [readings.jsonl](readings.jsonl), [allocation.csv](allocation.csv) |

| 짝·사건층 | 원문→실제 이웃/대조 이웃에서 바뀐 답 | 기술로 닫힌 조건·저자에게 남은 조건 | 추가 문자·개봉·측정비용 | 권할 전달 필드·미확인 |
|---|---|---|---|---|
| E1 회고 | 미관측 | 실제 수식/표 구문 선행; 수식 의미 vs layout 선택 미확인 | B/C 0/0, 개봉 미실시, 시간 미측정 | 원파일·판·선택 경로 |
| E2 회고 | 미관측; B는 A 중복 | T07/I05는 HTML pre 공백 규칙, Pandoc 변환 버그는 미해결; plain 두 줄 기대 이미 명시 | B/C 27/0, 개봉 미실시 | reader/writer·인접 셀·보존 축 |
| E3 회고 | 미관측 | T01/T02/I01/I02로 문법 및 구현 차이 구별; downstream hl_lines 의미 요구는 새 요구일 때만 | B/C 0/0, 개봉 미실시 | producer dialect·target format |
| E4 회고 | 미관측 | T03 tab width와 nesting은 별개, T04 node ignore는 우회책; 동일 입력과 실제 ESLint rule 필요 | B/C 66/66, C 끝 잘림, 개봉 미실시 | consumer rule·resolved config·정확 동일 함수 |
| E5 회고 | 미관측 | T06/I06는 modifier 의도·파서 범위, TS 실제 진단 미확인; 저자는 순서를 지정 | B/C 0/0, 개봉 미실시 | parser/compiler 버전·원문 |
| E6 회고 | 미관측 | T05/I03 optional initial pipe 문법; 원작성자 style 선택과 유효 schema 확인은 별도 | B/C 0/0, 개봉 미실시 | 당시 commit·원요구·짧은 union 제약 |
| 단위·분모·결측 | 원요청 6; 독립 짝 비교 0/6 | 모든 사건 실험 판정 불가; 회고 후보만 기록 | 매칭 후보 1/6; 시간·응답률·편집비용 실측 없음 | [comparisons.csv](comparisons.csv), [packets.jsonl](packets.jsonl); 계약안 2개 미검증 |

## 결론과 수용 범위: PARTIAL

설계 입력의 목적은 자료를 많이 붙이는 것이 아니라 **선택한 부분에 실제로 영향을 주는 생산자/소비자의 계약을 원래 요구와 분리된 증거로 전달하는 것**이다. 이 문장은 아래 회고 원자료에서 제기되는 조건부 설계 가설이지, 이웃 추가의 인과효과 측정 결과가 아니다. 별도 판독자의 생성·운영 권한/도구가 없어 결과를 본 동일 작업자를 독립 판독자로 가장하지 않았다.

### Q1. 최초 전달 시점과 모집

계획판 9ad2ffc5974bf3379ce1f3fb947a9cf19bbdf673, 실제 시작 97a1e63cb48ff4900984104e1d2a3760f324eb79. 차이는 중앙 진행표뿐. 선행 144 인계 92833407f665a6e28e4292491c261b7e0725c69c PARTIAL, 중앙 DONE; C4/Y2의 기술 게이트와 Y3의 CRLF 선택은 교정만 반영. 140/144 CSV·YAML 재실행 안 함. [SCOPE.md](SCOPE.md)

GitHub search_issues의 is:pr 조건이 일반 질의와 같은 issue 결과를 반환하여 search_prs를 별도 사용했다. 양 결과 생성시각 필드 null; 저장소별 번호순 병합 앞 30을 후보창으로만 저장. 개별 18개 직접 조회, 42개는 목록만. 원래 요청의 생성시각 오름차순 합집합을 증명하지 못했다. 6개 모두 현재 본문/PR; edit history 및 최초판 없음. E1 표 구조 보존은 암시적, E6 PR은 원요구 #14234와 후속 패치 섞일 위험이 있다. 선정 규칙을 충족했다고 주장하지 않는다. E1 expected 결측을 제거하지 않았다. 별도 모집 검증 필요.

### Q2. 가림 면, 경로·원문 보존

[request-snapshots.jsonl](request-snapshots.jsonl)에는 현재 API 본문 원문·updated_at·조회 시각·UTF-8 SHA-256을 저장했다. 과거 첫 판은 복원하지 못한다. [packets.jsonl](packets.jsonl)은 LF 정규화한 발췌·구간·해시·extra 문자수 및 잘림 위치를 기록한 초안이다. 제목 자체가 기대 방향을 포함한 경우 원요구 일부이므로 제거하지 않았다. 후속 expected/actual/diff를 수집자에게서 되돌려 가릴 수는 없다. 따라서 18개 모두 ready_for_blind=false. B/C가 실제로 존재하지 않는 경우 생성하지 않았다. E2 B는 같은 table의 첫째 td지만 A 안에 이미 존재하여 정보 증가 대조가 아님. E4의 B는 실제 indent rule, C는 no-console/no-unused-vars/no-duplicate-imports 형제 규칙에서 같은 길이 66자만 잘랐다. C가 정확한 JSON 규칙 전체가 아닐 수 있으므로 무관 정보 비용 대조 후보일 뿐이다. 전체 요청의 복원은 원문 저장소에서만 가능하며, 발췌만으론 부족하다.

### Q3. 기술 조회 vs 한 질문

판독 관측 없음. 다음은 수집자 회고이며 링크 제안 후보이다. R02의 plain 출력이 목적이면 추가 보존 의도를 묻기 전에 [Pandoc 3.1.11 manual](https://github.com/jgm/pandoc/blob/3.1.11/MANUAL.txt#L3420) reader/writer와 raw HTML의 범위를 확인하고 실제 입력을 재현해야 한다. R03은 [fenced_code_attributes](https://github.com/jgm/pandoc/blob/3.1.11/MANUAL.txt#L3932) 및 [CommonMark 0.30](https://spec.commonmark.org/0.30/#fenced-code-blocks)으로 시작한다. R04는 [옵션](https://github.com/prettier/prettier/blob/3.1.1/docs/options.md#L47)과 [ignore](https://github.com/prettier/prettier/blob/3.1.1/docs/ignore.md#L50)만으로 현재 문제의 해결을 선언할 수 없다. 정확한 동일 입력/설정이 기술 요청의 선행 조건이다. R05는 TS compiler 버전이 먼저다. R06은 [GraphQL union 문법](https://spec.graphql.org/October2021/#sec-Unions)으로 기술 가능 범위를 확인하되 원요구의 선택은 아직 미확인이다. R01은 첨부/실제 table selection 확보가 우선이다. 독자당 최대 두 공식 면 규칙은 실제 판독이 실행될 때 적용한다; 수집자 탐색 전체를 독자 관측으로 세지 않았다.

### Q4. 저자 기대와 독립 증거

R02의 저자 입력 중 첫 셀은 `<td>first column</td>`, 둘째는 `<td><pre>second column</pre></td>`. 현재 저자 기대는 `first column\nsecond column`; 보고 actual은 첫 줄뿐. 이 사례는 저자가 값·순서를 고정한 양성 **기대 예**이며 성공 실행 관측은 아니다. R03은 info string이 plain 출력에서 사라져야 하지만 코드 문자는 남아야 한다. R05는 현재 본문 원문 그대로 `declare private readonly name: string;`을 기대한다. R04는 기대와 실제 updateCartItem의 내용상 차이는 들여쓰기이나 입력 예 addCartItem과 다른 함수라 동일 input score 금지.

R06 실제 공개 diff의 long union 일부:
~~~graphql
# input
union SearchResult = Conference| Festival | Concert | Venue | Conference| Festival | Concert | Venue
# stable (excerpt)
    Conference
  | Festival
# main (excerpt)
  | Conference
  | Festival
~~~
[PR files](https://github.com/prettier/prettier/pull/15870/files)에서 ifBreak 첫 토큰이 공백→pipe로 변경되고 짧은 union은 그대로다. [GraphQL.js parser](https://github.com/graphql/graphql-js/blob/v16.8.1/src/language/parser.ts#L1000)는 union types를 별도 named type 목록으로 구문 분석한다. 따라서 같은 표기 아닌 **같은 lexical member sequence**는 관측되지만 유효한 GraphQL schema라는 결론은 아니다(중복 member가 들어 있음; validate 별도 실행 필요). original #14234 저자 기대 및 PR 최초 부모는 미확인. 리뷰의 stable 샘플 변경을 최초 요청자의 선호로 소급하지 않는다. 셸 실행 0회.

### Q5. 기술 조건과 저자 선택 분류 후보

- E2: pre 표준에서 leading newline의 특수 처리는 기술 규칙(T07/I05), 변환 버그의 정확 판별에는 해당 판 실행 필요. plain 두 줄을 원하는 저자에게 다시 값 보존을 묻지 않는다. 별도의 pre 공백/HTML semantics 보존이 목적이면 질문이 달라진다.
- E3: CommonMark 정보 문자열 허용과 특정 속성 의미는 다르다(T02). Pandoc brace attributes(T01) vs Python-Markdown의 unbraced hl_lines(I02), markdown-it token.info와 content 분리(I01)를 비교했다. A=plain 결과만, B=highlighting을 보존할 downstream renderer가 있으면 후보는 각각 plain parser/renderer-specific attribute 처리로 달라질 수 있다. A는 원저자 본문에 이미 명시되어 있으므로 추가 질문은 불필요; B는 새 요구 시만. 실행으로 확정하지 않았다.
- E4: tabWidth=4와 eslint indent rule=4 모두 같은 숫자이지만 nesting 관계를 지정하는 동일 기능이라는 뜻은 아니다. 실제 resolved config·버전과 같은 함수 입력 결측. A=formatter를 최종 권위로 할지 B=lint를 최종 권위로 할지는 둘 다 지원 가능 여부부터 재현할 필요. 문서만으로 충돌 해결 선언 금지. T04 ignore는 코드 노드 제외라는 기술 선택지, 완전한 프로젝트 해법 아님.
- E5: T06 declare field의 runtime 의미와 I06 Babel modifier parse order는 TS compiler legality를 결정하지 않는다. 정확 판 양쪽 진단이 다르면 기술로 닫힌다. 둘 다 유효하면 저자가 현재 본문에서 이미 원하는 순서를 지정. 묻는 대신 명시를 기록한다.
- E6: T05의 optional pipe와 I03 파서 구조는 문법 가능 여부를 뒷받침한다. A=leading pipe 허용, B=금지라면 formatter 정책 후보가 달라지나 original issue에서 어떤 답이 있었는지 미확인. 구현자가 결정한 기본값을 알려진 사용자 선호로 세지 않는다.
- E1: 수식 원파일 결측이 먼저다. align 문맥을 고치는 한 기술이 실제 원문의 보존 요구까지 만족하는지 아직 모른다.

실제 질문 발송 0, 응답률·해결시간·시간 절약 미확인. 모든 Q3 질문 행 자체가 미실시이므로 오승인 평가나 검정 분모 없음.

### Q6. 반례와 타 분야

소프트웨어 별도 반례: [X01](https://github.com/jgm/pandoc/issues/9304)는 two spaces가 tab-stop 값과 commonmark/markdown reader에 따라 코드/문단으로 갈린다는 당사자 보고. 문법 판을 추가하지 않은 동일 문자열이 오히려 위험하다. [X02](https://github.com/jgm/pandoc/issues/9310)는 Jira code opener의 개행과 이후 문단 보존이 함께 관계한다. [X03](https://github.com/jgm/pandoc/issues/9320)은 표가 표시되더라도 row id, cell class가 없어져 parallel-text 내비게이션 목적을 잃는다는 사례. [X04](https://github.com/prettier/prettier/issues/15871)는 whitespace-sensitive Vue interpolation, [X05](https://github.com/prettier/prettier/issues/15872)는 static hello의 4→3 backticks 축소가 무해해 보여도 Mustache로 triple fence를 삽입하면 enclosing fence가 닫혀 버리는 경우를 공개한다. T02 closing fence 규칙 및 I04 Mustache 실제 interpolation test와 비교하면 **실제 downstream expansion 계약**을 붙이는 이유가 분명하다. 이것은 요청자 보고이며 직접 실행 결과 아님. [X06](https://github.com/prettier/prettier/issues/15875) comment duplication, [X07](https://github.com/prettier/prettier/issues/15876) ts-ignore scope, [X08](https://github.com/prettier/prettier/issues/15878) MDX 버전별 comment syntax도 실제 인접 의미가 달라짐을 시사한다. 공유 문단 스타일과 한 예외는 실제 사례 검증 부족; 대표 예 하나를 모든 선택에 강제하지 않는 반증 가설로 남긴다.

텍스트 판본: [D01 Folger 편집자 설명](https://www.folger.edu/explore/shakespeares-works/hamlet/an-introduction-to-this-text/) 및 [textual notes 1.2.133](https://www.folger.edu/explore/shakespeares-works/hamlet/textual-notes/)에서 Q2 sallied와 F solid 및 현대화 sullied가 구별된다. F-only, Q2-only, 편집자 수정 기호도 확인. 동일 대목이라는 정체성과 같은 원문 표현을 구별해야 한다. 두 원면 [Q2](https://digitalcollections.folger.edu/bib163901-157451), [F1](https://digitalcollections.folger.edu/view/group/210127)은 human verification으로 차단되었고 우회 안 함. 따라서 직접 원면 0/2. 같은 편집판 소개·notes는 하나의 저작으로만 계산.

음악: [D02 MusicXML 4.0 transpose](https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/transpose/)와 [C Sounds XML](https://www.w3.org/2021/06/musicxml40/musicxml-reference/examples/concert-score-and-for-part-elements/) 직접 열람. P1 piccolo written C5에 octave-change 1, P2 oboe written C5에 transpose 없음; 같은 표면이 다른 sounding pitch를 낼 수 있다. P3 bass clarinet score C3, for-part part-transpose chromatic -2와 octave-change -1 및 treble clef: 파트 표현과 concert score의 별도 계약을 데이터에 보존한다. 이는 공식 XML 예제이지 역사적 작품 실제 총보/파트를 둘 다 읽은 관측이 아니다. [D03 KV498](https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=250) 발행자 안내는 clarinet의 violin transposition을 제공하지만 ZIP 악보 파일 미열람(설명만, 하한 제외). [D04 KV581](https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=337) 실제 편집자 주석은 autograph 결측과 II악장 30·32마디 dynamics의 추정 편집 개입을 밝힌다. 음표/기호의 표면을 원저자 의도로 단정할 수 없다는 편집자 보고. 원곡 악보/파트 실제 마디 확인 미완. D02의 예와 표준은 같은 저작, D04는 별도 편집자 저작으로 후보 산입. 판본/악보는 소프트웨어 분모에서 제외.

비용: 요청자는 입력 원문과 구간 확보·판 식별에 추가 수고, 검색자는 실제 관련 계약 1개와 출처 확인 비용, 판독자는 가림·재판독 비용, 표시기는 원문/해석/판 차이를 유지할 비용이 생긴다. 부가 정보가 A/B 결정과 무관하면 비용만 늘고, 잘못된 sibling은 더 큰 교정 비용을 유발할 수 있다. 실측은 66자 대조 초안 외 없다. 비용 가설을 제품 성능 개선으로 읽지 않는다.

### Q7. 되돌릴 수 있는 전달 계약

[contracts.json](contracts.json)의 minimal-ref(원문·선택 참조·판·명시 보존/미확인)와 bounded-related-context(실제 직접 관계, 출처와 구간/길이, 선택형 보존 축 및 별도 가정)를 두 조건부 안으로 남긴다. 원문의 URL이 살아도 변경 시 처음 의미를 복원할 수 없고 해시 자체로 원문을 생성할 수 없다. 그래서 원문 snapshot과 reader-facing projection을 분리한다. 기대값 있는 공개 링크를 판독자에게 바로 열게 하면 누출될 수 있으므로 독립 실행에서는 원문 저장부와 기술 검색 허용 목록을 분리해야 한다. 수집자 검산은 JSON의 hash/refs를 비교하는 수준, 별도 사람이 실제 재판독하지 않았다. **전 사건 실험 분류 판정 불가**, 회고상 기술 선행/저자 명시/선호 미지 후보만 비교했다. 현재 근거로 어느 안을 기본값으로 고정하지 않는다.

### 검산

원장 [sources.jsonl](sources.jsonl): 38행, opened 32 고유 work_id(그중 8 auxiliary request + 1 same-repo implementation은 하한 제외); description-only 1, failed 5. 유형 산입 후보 23 = 6 request + 8 technical + 6 independent + 1 text + 2 music. 유형별 최소치 적용하면 21/24 (6/6 + 6/6 + 6/6 + 1/3 + 2/3). T03/T04 같은 문서 계보 및 T08/I04 같은 Mustache 계보를 엄격히 하나로 세는 감도에서는 후보 21개이며 독립 구현군 수가 더 감소할 수 있다. 기술 명세 초판·공개 당시 버전의 모든 자료가 입증된 것은 아니다. [SELF_CHECK.md](SELF_CHECK.md). exact times 없는 원장 행은 UTC interval로 남겨 실제 개별 확인 시각을 꾸미지 않았다. snapshot 6건만 재조회 시각 기록. 실제 source ledger와 표의 ID로 역추적 가능. 후보창 및 판독 결측이 크므로 PARTIAL.

| 불일치·약점 | 판단에 미치는 영향 | 다음 조사와 자료 | 판정을 바꿀 관측 |
|---|---|---|---|
| 생성순 합집합 불확정 및 최초판 0/6; E1 첨부 미열람, E6 원이슈·최초 커밋 결측 | 첫 3건 선정 및 기대값 독립성 보장 불가 | raw GitHub search/issues 생성순, 개별 생성시각·edit history, #14234 및 #15870 첫 commit parent, E1 첨부 | 실제 최초 30개 순서와 적격 3건씩 재현, 동일 판의 원요구·입력·기대값 확인 |
| 독립 판독 0/18, 완전한 동일 길이 후보는 E4 1/6뿐이며 수집자 선노출 | 이웃의 효과·오승인·질문 감소·시간 절약 및 우월한 계약을 실증할 수 없음 | 실제 세 독립 문맥에 라틴 배정; 원본/기대 접근 분리; 짝 전부 실제 이웃/무관 구간 확보 | 봉인 후 개봉한 18개에서 같은 사건 A/B/C 전환 및 오답을 비교, 노출·결측 제외 재집계 |
| E4 다른 함수, E5 컴파일 미확인, E6 문법과 유효 스키마 구별; 판본 원면 0/2 및 실제 총보·파트 0쌍 | 표현/값 동일성의 과잉 확신 위험; 외부 분야 하한 및 실제 원자료 비교 미달 | 같은 함수/버전 리플레이, TypeScript 진단·emit, GraphQL AST/validation, Folger 허용 접근, Mutopia KV498 실제 총보와 대체 파트 | 원입력과 결과의 의미/표현 분리 검증 및 원면·동일 마디 비교가 반례를 확인하거나 뒤집음 |
