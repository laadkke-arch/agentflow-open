# AF-RES-155 선택 구간과 실제 변환 조건

| 사건·작성자 원문·판 | 선택 구간·목적 | 명시 기대·주체 | 실제 이웃·형제 위치 | 최초판·결측 |
|---|---|---|---|---|
| E2 Pandoc 3.1.11 [#9305](https://github.com/jgm/pandoc/issues/9305) | body L7–14의 133B 전체 table, 둘째 td/pre 포함. plain 변환 | 작성자는 첫째·둘째 셀 두 줄과 순서를 제시. 실제 보고는 첫째 줄만 | B는 같은 표 L10의 첫째 td 27자. A에 이미 있다. 무관 C 결측 | 현재 본문 해시가 148과 일치. 최초판·로컬 table의 EOL 미확인 |
| E3 Pandoc 3.1.11 [#9308](https://github.com/jgm/pandoc/issues/9308) | body L5–7의 62B 안쪽 fence와 `javascript hl_lines="1"`. plain 코드 본문 보존 | 작성자는 들여쓴 코드만 명시. 유지보수자는 CommonMark reader와 중괄호 속성표기를 후속 제시 | B는 L10 소비 명령 23자. A에도 있다. 무관 C 결측 | 최초판 미확인. 이슈의 렌더링에서 fence 경계가 합쳐 보여 API 본문을 사용. 하이라이트 소비자 미확인 |
| X05 Prettier [#15872](https://github.com/prettier/prettier/issues/15872) | body L25–27의 61B 템플릿. 실행 파일은 네 칸의 게시판 표시 들여쓰기만 제거. NBSP를 유지 | 작성자는 외곽 4, 내부 3 백틱의 확장 결과를 바란다. 3/3에서 파손을 보고. 여분 백틱을 기본 보존하자는 선택도 제안 | B는 L21 대입 종류 53자. 정적 예는 목표와 관련된 의미 대조다. 무관 C 결측 | 최초판·실제 도구 판·바인딩 파일·escape·소비 parser 미확인. [같은 작성자의 VS Code 게시](https://github.com/microsoft/vscode/issues/201725)는 저장 시 포맷을 밝힘 |
| E4 Prettier 3.1.0 [#15853](https://github.com/prettier/prettier/issues/15853) | body L72–84의 562B `addCartItem` POST. nested arrow 들여쓰기 조정 | actual/expected는 `updateCartItem` PATCH. 같은 입력의 기대 없음 | L35 선언된 indent 66자 B. L31–32 무관 경고 규칙 66자 C, 후보 끝 40자 절단. B 적용 미확인 | 최초판·첨부 시각 판독·같은 함수·resolved config 및 lint 판 결측. 후속 1건은 config 패키지 제안 |
| 단위·전체 분모·결측 | 저자 사건 4, 현재 본문 4/4. 148의 E5는 재실행 범위 밖 | E2·E3 같은 입력의 명시 plain 2/4. X05는 확장 예시, E4는 입력 불일치 | A/B/C 예정 12, 실물 9, C 결측 3. B 두 중복, 한 선언 적용 미확인. 같은 길이 B/C 1/4 | 최초판 0/4. [본문 원장](evidence/issue-snapshots.jsonl) · [입력](inputs.jsonl) · [패킷](packets.jsonl) |

| 입력·변환 경로·대조 유형 | 두 반복의 실제 명령·근거 | 바이트·AST·다음 출력 | 깨진 보존값 | 작성자 보고 일치·미확인 |
|---|---|---|---|---|
| E2 원 table 및 LF 대조 | W1/W2 `pandoc -t plain table.md`, `pandoc -t json table.md`. E2-default, E2-default-lf | plain 첫째 줄 13B. AST 580B에는 둘째 문자열을 포함한 RawBlock. CRLF→LF 대조의 두 결과 지문 동일 | 정상 종료 0에서 둘째 값 누락. EOL은 이 값에 영향 없음 | 작성자 actual과 일치, 기대 미달 |
| E2 pre 제거·span·HTML reader | W1/W2 원 명령에 각 fixture, HTML reader는 `pandoc -f html -t plain table.md`와 `-t json`. E2-drop-pre, E2-with-span, E2-html-reader | 제거/대체 AST 607/639B, plain 동일 27B 두 줄. HTML reader는 AST Table의 둘째 CodeBlock과 두 셀의 격자 plain 222B | 제거·span·HTML reader 모두 두 값 보존. 격자와 두 줄 레이아웃은 다름 | pre 제거는 저자 보고 일치. span과 HTML reader는 구성 |
| E3 원 fence | W1/W2 `pandoc -t plain code.md`, `pandoc -t json code.md`. E3-default | plain 52B에 info와 코드 한 줄. JSON 158B의 `Para(Code)` | 독립 CodeBlock과 저자가 정한 표시 | 원저자 actual 일치, 기대 미달 |
| E3 같은 fence의 다른 reader 및 다른 opener | W1/W2 `pandoc -f commonmark -t plain code.md`와 `-t json`. 중괄호·언어 단독은 기본 CLI. E3-commonmark, E3-braced, E3-lang-only | plain 32B 세 경로 동일. CodeBlock JSON 130/146/130B. 중괄호판에 hl_lines 키가 남음 | plain 코드는 보존. 하이라이트 속성의 실제 소비는 미측정 | plain 기대와 일치. reader/구문은 후속 제안과 구성 |
| X05 정적·plain 대입과 sentinel | W1/W2 `node …/prettier.cjs --no-config --no-editorconfig --parser markdown` 및 `node pipeline.cjs MODULES expand`와 `parse`. X05-static-example, X05-static-boundary, X05-plain-boundary | 4→3 fence와 CRLF→LF. AST sourcepos 변화. 하나의 hello 코드, HTML과 후속 문단 동일 | 측정한 문자·블록 손실 0 | 정적 포맷 보고 일치. 파서·plain 대입·sentinel은 구성 |
| X05 이중 중괄호 기본 escape | W1/W2 같은 CLI와 Mustache.js 4.2.0 기본, CommonMark.js 0.30.0. X05-nested-example, X05-nested-boundary, X05-format-expanded | 백틱을 `&#x60;`으로 대입. 양 순서 모두 하나의 코드 블록, sentinel 유지. HTML에서 엔티티 표기 자체가 보이는 코드로 남음 | 경계는 유지, 두 순서 모두 원시 백틱 문자는 소실. 사전 예측 빗나감 | 4→3은 일치, 확장 결과는 다름. 실제 도구 설정 결측 |
| X05 같은 입력·비이스케이프 | W3/W4 `node pipeline.cjs MODULES expand-unescaped BINDING`과 같은 포맷·parse. X05-raw-nested-example, X05-raw-plain-boundary, X05-raw-nested-boundary, X05-raw-format-expanded | 4/3/3/4 대비 3/3/3/3. 원본 한 CodeBlock이 빈 코드 두 개와 사이 hello 문단으로 변함. sentinel은 독립. plain 대입은 안정. 확장 먼저 포맷하면 4 유지 | raw 중첩의 코드 문자·경계. 확장 먼저는 EOL 외 코드·다운스트림 HTML·AST 투영 보존 | 저자가 표시한 raw 확장과 맞는 구성 재현. 실제 도구 경로 미확인 |
| E4 동일 함수 및 설정 | W1/W2 E4-same-function 예정. 실행 명령 미구성 | 실제 포맷·lint 미관측. 다른 함수·호출·인자 | 비교할 보존값 미지정 | 출력 및 유지보수자의 제안을 정답으로 채점하지 않음 |
| 단위·전체 분모·결측 | 20경로 × 두 번 40행, 38실행, E4 2 미실행. [실제 명령 원장](runs.jsonl) | 하위 명령 132회 종료 0. 같은 경로의 지문과 요약은 두 반복 동일 | 성공 종료에도 E2 셀 및 E3 독립 코드 블록 손실. X05 문자와 경계 별도 | 주 사건 실제 작성자 전체 경로 2/3, X05 snippet 기반 구성. [공급자 시험 6행](evidence/public-tests.jsonl) 별도 |

| 같은 선택 짝 | A 예측·결과 | 관련 B·무관 C가 가른 조건 | 불필요·누락 필드 | 비용 | 권할 전달 예·한계 |
|---|---|---|---|---|---|
| E2 자연 후보 D01와 동일 바이트 reader D05 | 기본 명령에서 첫 셀만. 구성 HTML reader는 둘째도 격자에 보유 | B는 첫 셀 중복. C 결측. reader는 명령 자체를 바꾼 대조 | 두 줄 목적 기지. 다른 input reader를 고를 문제에서만 판별 필드 후보 | A 349B, B 원문 +27B·전달 +25B. reader 쌍 8회 88.081ms | 원문·범위·목적·판과 명령. 값만이면 pre 제거, 표 구조면 HTML reader 검토 |
| E2 음성 D06/D07 | pre 제거와 span은 AST가 다르고 두 줄 동일. EOL 변경 전후 결과 지문 동일 | 실제 C 결측. B에서 더 얻은 판별값 없음 | span 이름·EOL은 이 plain 목표에 무관. pre 처리 관련 | D06 8회 87.016ms. D07 8회. 행 간 공유 실행 존재 | 목표를 plain 값·순서로 명시. 원래 레이아웃·공백은 별도 요구 |
| E3 자연 후보 D02, 동일 바이트 reader D08, attr D09 | 기본 Para와 CommonMark CodeBlock. 중괄호/언어 단독은 동일 plain, AST 속성 다름 | B는 A의 원 소비 명령 반복. C 결측. reader는 별도 기술 경로 | plain에는 hl_lines 보존 불필요. 실제 renderer의 처리 규약 미확인 | A 319B, B +23B 원문·+21B 전달. reader 쌍 8회 89.705ms | plain이면 CommonMark reader 검토. 속성 보존 필요 시 실제 다음 소비자 참조 |
| X05 구성 D10/D11, 같은 A | raw plain은 같은 렌더링. raw nested의 format-first는 경계 변화. 기본 escape 예상은 빗나감 | nested 종류 B는 raw 정책 고정 시 갈린다. escape까지 밝히지 않음. C 결측 | 유효 판별 정보는 대입 직후 실제 fence 표현. 실제 도구·escape 미확인 | A 306B, B +53B 원문·+51B 전달. raw plain/nested 20회 1393.937ms | 다음 단계로 전달된 작은 expanded sample. raw라면 확장 먼저 또는 외곽 fence 유지 |
| X05 음성·순서 D12–D14 | 포맷 전후 위치와 문자열 또는 목표 경계를 따로 평가. raw 확장 먼저는 HTML 동일 | 정적 예를 무관 C로 취급하면 안 됨. 기본 escape에서 중첩만으로 경계 실패를 예견할 수 없음 | 바이트 목표에는 EOL 필요, 렌더 목표에는 이 예의 EOL 무관 | 정적 10회 535.136ms. raw 확장 후 포맷 8회 551.783ms | 실제 소비 결과와 보존 축을 택한다. 전체 여분 fence 기본 보존은 선호 |
| E4 D04 | A/B/C 모두 보류. 입력과 기대의 신원 불일치 | B는 선언, C는 무관 경고. 어느 쪽도 동일 함수와 lint 적용을 입증 못 함 | 동일 함수 및 resolved 설정·판 결측 | A 834B, B/C 원문 각 +66B. 전달 +70/+76B. 실행 0 | 동일 파일의 함수·설정을 확보하고 비교 |
| 단위·전체 분모·결측 | 유효 자연 짝 0/4 사건. 자연층의 필수 필드 미확인. [구성 및 공석 14행](distinctions.csv) | 명령 바꾼 기술 대조 2행. A 호환 구성의 출력/경로 분기 3행(D10,D11,D13), A 호환 음성 2행(D12,D14). 유효 C가 가른 횟수 0/0 | B 한 필드로 가른 구성은 escape를 고정한 D10. D11은 유효 확장/escape 별도. 독립 판독 0회 | [비용 원장](costs.csv)의 작성량·전달량·실행수·실행시간은 별도. 132회 합 6200.369ms, 사람의 시간 미측정 | 구성 짝은 구별 원리의 증거. 실제 사용자 질문 수나 자연 짝 효과 미확인 |

**상태는 PARTIAL이다.** 두 Pandoc 원 경로와 고정판 구성 경로를 확인했다. X05의 작성자 전체 도구 경로와 문헌의 역사 원면은 결측이다.

## Q1–Q2 원전과 패킷

AF-RES-148의 등록 상태 DONE과 인계의 PARTIAL을 구별한다. 선행 SHA에서 읽은 세 본문의 UTF-8 지문이 GitHub 재열람과 일치했다. X05는 별도 원문을 보존했다. 4건의 최초 게시판 판은 미확인이다. Pandoc 두 건은 정확한 원보고판 3.1.11을 사용했다. #9305를 닫은 변경은 3.1.12에 들어간 매뉴얼 정정이었다. #9308의 2025-08-11 후속 reader/구문 제안은 원 명령에서 분리해 재생했다. [#9305 댓글](https://github.com/jgm/pandoc/issues/9305#issuecomment-1879162730) [T01-P 매뉴얼 정정](https://github.com/jgm/pandoc/commit/b3a471b09f3fb7ed2af960cb44671311a68ad82c) [#9308 후속](https://github.com/jgm/pandoc/issues/9308#issuecomment-3176853337)

12행 사전 예측은 한 연구자가 새 출력 개봉 전에 봉인했다. 공개 보고와 148의 일부 기대는 선노출됐다. 결측 C 세 행에는 관측값이 없다. X05의 NBSP로 인해 범위는 60코드포인트·61바이트다. 실행 파일에서 표시 들여쓰기만 제거했다. E4의 C 후보는 106자 원문에서 끝 40자를 잘랐다. 선택 범위와 전달 payload는 각각 해시 검산했다. [predictions.csv](predictions.csv) [packets.jsonl](packets.jsonl)

## Q3 Pandoc의 갈라지는 단계

#9305에서 둘째 셀의 문자열은 reader를 거쳐 raw HTML 노드에 남는다. plain writer 경로의 결과를 판단하는 데 태그 종류와 실제 출력이 필요하다. 두 줄 목표에는 pre 제거 대조가 일치했다. HTML reader는 원입력을 Table과 CodeBlock으로 읽어 두 값을 격자 표에 남겼다. 혼합 문서에서 전체 reader를 바꾸면 Markdown 부분에 대한 별도 검증이 필요하다. [R05 Jupyter 요구](https://github.com/jgm/pandoc/issues/2716) [T06 HTML pre](https://html.spec.whatwg.org/multipage/grouping-content.html#the-pre-element) [F01 공식 판독 시험](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/test/html-reader.html#L88-L103)

#9308의 기본 reader는 처음부터 독립 코드로 분류하지 않는다. CommonMark reader와 중괄호 속성판은 같은 32바이트 plain을 낸다. 중괄호 AST만 hl_lines 키를 전달한다. 실제 강조 동작을 요구하는 새 요청에서는 그 기능을 사용하는 소비자와 해당 출력이 필요하다. [T01 매뉴얼](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/MANUAL.txt#L3932-L3971) [T02 CommonMark §4.5](https://spec.commonmark.org/0.30/#fenced-code-blocks)

## Q4–Q5 실제 소비와 보류

Prettier 3.1.1은 미확장 AST 값에서 가장 긴 백틱 연속을 찾아 외곽 길이를 정한다. 확장 뒤 원시 백틱이 생기는 구성에서는 네 개가 필요했다. 기본 Mustache.js 4.2.0에서는 문자가 이스케이프되어 예상한 경계 파손이 나타나지 않았다. D11은 대입 전의 내용 종류만으로 경계 결과를 결정할 수 없다는 반례다. Prettier 3.1.1을 시간상 근접판으로 선택했다. 3.1.1은 2023-12-10, 보고는 2024-01-03, 3.2.0은 2024-01-12다. [T03 formatter](https://github.com/prettier/prettier/blob/b86701dd1df5852f5024d322a17c9fb7ef97850c/src/language-markdown/printer-markdown.js#L233-L259) [T04 escaping](https://github.com/janl/mustache.js/blob/bd29972ab8a0f4c592f35483615ab9a274396300/mustache.js#L60-L74) [F03 fixture](https://github.com/mustache/spec/blob/5d3b58ea35ae309c40d7a8111bfedc4c5bcd43a6/specs/interpolation.yml#L36-L66)

#15853의 유지보수자가 권한 eslint-config-prettier는 설정 순서와 plugin 이름에 의존한다. 참고판 9.1.0 목록에는 일반 indent off가 있고 @stylistic/js/indent는 찾지 못했다. 작성자 프로젝트의 충돌 또는 해결을 추정하지 않았다. 동일 함수가 확보되면 그 파일의 prettier 설정 경로, eslint print-config와 실제 진단을 대조한다. 별개 프로젝트의 #4112 반복 저장 예는 같은 문제가 아닌 범위를 보여준다. [R04-C1 유지보수자](https://github.com/prettier/prettier/issues/15853#issuecomment-1874796575) [T07 print-config](https://github.com/eslint/eslint/blob/8e8e9f8476d701e4e981b9b4d9957e5d4855e530/docs/src/use/command-line-interface.md#L775-L785) [T08 호환 설정](https://github.com/prettier/eslint-config-prettier/blob/40c7f3d0624129934bc3b40ab13a8ed938c6313b/README.md#L65-L96) [R06 반복 저장](https://github.com/prettier/prettier/issues/4112)

## Q6 판정 규칙과 적용 한계

선택 바이트와 목적·판을 고정한다. 그 조건에 양립하는 두 실행 상태에서 **요구한 출력 축**이 달라지는지 확인한다. A에 이미 적힌 조건으로 답이 정해지면 전달을 늘릴 근거가 없다. 다른 출력이 가능한 경우 새 참조 하나가 어떤 상태인지 실제로 지목하는지 확인한다. 같은 함수와 실행 맥락이 결측이면 보류한다.

- E2/E3의 명시 명령을 빼면 A의 모호함을 인위적으로 키운다. 동일 실행 입력에서 reader가 만드는 차이는 기술 대조로 남겼다.
- X05에서 raw 정책이 고정된 D10은 대입 종류 하나로 갈린다. D11과 D12는 그 조건이 빠졌을 때 B만으로 구분할 수 없음을 보인다. 실사례의 대입 직후 값을 확인하면 이 변수 두 개를 직접 검사할 수 있다.
- E4의 C는 같은 길이로 만들었으나 같은 함수라는 전제가 깨졌다. C가 기술 분기를 맞히거나 오인시킨 비율은 분모 0으로 산출 불가다.
- 직접 열람 자산은 원요청 6, 기술 9, 별개 배포 시험 7, 디지털 원판본 3, 음악 원자료 3으로 28개다. Mutopia 묶음을 하나로 합친 출판 계보는 26이다. 역사 인쇄 원면 0/2는 공석이다. 같은 발행본의 PDF와 HTML 및 같은 이슈의 후속·교차 게시를 중복 산입하지 않았다. [sources.jsonl](sources.jsonl)

## Q7 다른 분야 판독

Hamlet의 같은 독백에서 Q2 디지털 판본의 sallied, F1 기관 전사의 solid, Folger 편집 본문의 sullied를 읽었다. 근처의 w[e]ary와 ⟨weary,⟩는 편집 관행이 다르다. Folger의 PDF 추출에서 꺾쇠가 보이지 않아 같은 판에서도 전달 경로가 편집 표시에 영향을 줄 수 있다. 요청자가 원증인의 자형을 원하면 소장본과 면을 지정해야 한다. 역사 인쇄 원면의 직접 시각 판독은 미완료다. [Q2 편집 원면 본문](https://internetshakespeare.uvic.ca/doc/Ham_Q2/scene/1.2/index.html) [Bodleian 전사](https://firstfolio.bodleian.ox.ac.uk/ff/ham/1/2) [Folger 발행 본문](https://www.folger.edu/explore/shakespeares-works/hamlet/read/1/2/)

K.498 I Andante m.9에서 Mutopia 총보의 클라리넷과 B♭ 파트는 F5, 바이올린 대체 파트는 E♭5를 기보한다. 실음 E♭5와 음가는 같다. 공개 배포 소스에서 재각보한 실제 보표를 읽었고 원 배포 PDF와 비교하지 못했다. 연주자는 적힌 음을 읽고 변환기는 악기 이조를 적용한다. MIDI 소비자는 음높이와 조표 메타데이터를 서로 다른 층으로 처리한다. 편집자와 요청자는 결과에 어떤 보존 축이 필요한지 고른다. [직접 판독·이미지·재생 기록](evidence/cross-domain.md)

## Q8 전달 계약 후보

**최소안**은 원문, 정확한 범위, 목적, 판을 전달한다. #9305에서 이미 요구된 두 셀 값의 순서를 확인하는 입력이다.

```json
{
  "source": {
    "url": "https://github.com/jgm/pandoc/issues/9305",
    "body_sha256": "5feceda64c521b8ec1fd71a5df8962374765d867a5e9c8106da68c7f8196c95d"
  },
  "selection_utf8_half_open": [187, 320],
  "purpose": "plain 변환에서 첫째·둘째 셀 값과 순서 유지",
  "revision": {
    "tool": "Pandoc",
    "version": "3.1.11",
    "argv": ["pandoc", "-t", "plain", "table.md"]
  }
}
```

**조건부 참조 추가안**은 실제로 값을 공급하는 위치 하나를 더한다. #15872의 현재 본문에서 확인한 범위를 보존한다.

```json
{
  "source": {
    "url": "https://github.com/prettier/prettier/issues/15872",
    "body_sha256": "0832d3ed299a2c501b32424ac3a7defe2a3d5a3b03bf6ffbfa2b00258636cd5f"
  },
  "selection_utf8_half_open": [560, 621],
  "purpose": "확장 직후 코드 문자와 이후 Markdown 코드 블록 경계 보존",
  "revision": {
    "tool": "Prettier Markdown",
    "version": null,
    "version_reason": "작성자 미기재"
  },
  "direct_reference": {
    "role": "producer",
    "source_utf8_half_open": [425, 478],
    "meaning": "작성자 설명상 대입값에 Markdown 코드 블록이 있음",
    "evidence": "현재 이슈 본문. 실제 escape 정책 미확인"
  }
}
```

실제 대입 직후 출력이 확보되면 그 위치를 참조해 유효한 raw fence 여부를 확인한다. 정적 입력의 fence 길이와 plain에서 사용하는 코드와 무관한 하이라이트 키는 여기서 일반 필수값으로 만들 근거가 없다. 전체 문서의 백틱 여분 기본 보존이나 formatter와 linter의 우선권은 작성자가 정할 수 있는 정책이다. 새 포맷이 사용자 이해나 질문 수를 개선할지는 별도 관측이다.

## 추가 분석

E2는 읽은 AST에 값이 raw로 남고 writer에서 탈락한다. E3는 읽는 순간 독립 코드 블록이 사라진다. X05는 formatter 결과가 같아도 다음 확장·판독 조건에 따라 달라진다. 따라서 같은 형식의 로그나 결과 하나로 세 문제를 판정하기 어렵다. [SELF_CHECK.md](SELF_CHECK.md)의 재집계와 [replay](replay/)로 입력부터 결과 지문까지 확인할 수 있다.

| 불일치·약점 | 판단에 미치는 영향 | 다음 조사·자료 | 결론을 바꿀 관측 |
|---|---|---|---|
| 유효 자연 짝 0/4. X05의 기본 이스케이프는 사전 예측을 뒤집었고 저자의 도구·escape·소비자 결측 | 구성상 갈림은 확인했으나 원 프로젝트의 필수 필드 판정은 공석 | #15872의 template, 두 실제 대입, formatter/engine/parser 버전과 effective 설정 고정 | 같은 선택·목적·판의 두 실제 확장값에서 결과가 갈리고 검증된 참조 하나로 구분 |
| E4 입력과 기대가 다른 함수이며 같은 길이 C 사건에 실행 결과 없음 | 무관 형제의 오분기 및 lint/formatter 권고를 채점할 수 없음 | #15853 같은 함수의 입출력과 그 파일의 resolved 설정 확보 | 동일 함수의 출력과 진단으로 B 적용이나 무관성을 확인 |
| 역사 인쇄 원면 0/2. K.498 공식 소스는 재각보했으나 2014 배포 PDF 미열람 | 디지털 표시와 기보/실음 관측을 당대 자형·배포 PDF에 소급할 수 없음 | Folger Q2와 Bodleian F1의 해당 독백을 허용 원면에서 읽고 Mutopia 원 배포 PDF m.9 검사 | 같은 대목의 실제 철자·편집 기호와 원 배포 기보가 현재 판독을 확인 또는 변경 |
