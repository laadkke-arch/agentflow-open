# Vega-Lite N/I 원문 검토 — 예측 봉인 전

선정·A/B는 단계① `a6b1624c899eacf118c0e01350f52cbd53e21dae`의 operations.json을 따랐다. 이 파일은 수신 제품의 당시 설명·선행 예제만 다룬다. 선택된 issue의 댓글, 연결 PR, 후속 release body, 사후 시험·기대 SVG/그림은 열지 않았다. 실제 chart rendering도 실행하지 않았다. 원래 본문 URL의 JSON payload 복원은 입력 읽기이며 결과 실행과 구분한다.

## 1. 판 고정과 실제 작성자 판의 결손

| 요구 | 연구용 기준판 | 고정 commit | 근거·제한 |
| --- | --- | --- | --- |
| V01 #7278 | v5.0.0, 공개 2021-02-24 | `d7cecefe310811d00276bb09bfd78312f1a19759` | issue 2021-03-02 이전 최신 공개 release. 저자가 적은 schema는 v4이며 실제 runtime을 v5라고 주장하지 않음. schema major에 맞는 이전 v4.17.0도 보조 확인 |
| V02 #7422 | v5.1.0, 공개 2021-04-16 | `64739639fd85d9be605704c91425d26450d25b9c` | issue 2021-04-30 이전 최신 공개 release. 저자 runtime patch는 미명시 |
| V03 #7507 | v5.1.0, 공개 2021-04-16 | `64739639fd85d9be605704c91425d26450d25b9c` | issue 2021-06-04 이전 최신 공개 release. 본문의 schema v2가 실제 renderer를 증명하지 않으므로 조건부 분석 기준판으로만 사용 |

GitHub release API의 tag/date/prerelease/draft만 출력했고 changelog body는 가렸다. 추가로 tag 날짜를 확인해 v5.1.1(2021-09-06), v5.2.0(2021-11-23)이 세 요구 뒤임을 확인했다. 미래 본문은 읽지 않았다. v4.17.0의 commit은 `4b15519fdc74c0853ecbf165fa76617fd9c8c84b`다. V01에 쓰는 field 절은 v4.17.0과 v5.0.0에서 파일 SHA256이 동일하다. 문서 동일성을 동작 동일성으로 확대하지 않는다.

## 2. 카드 후보와 정확한 읽기 창

최종 예측은 root가 작성한다. 아래 카드는 원문 URL·고정판·연속 행·창 SHA256으로 재구성할 수 있다. 원문 전체나 긴 발췌를 공개 복제하지 않고 자체 요약을 남겼다. 실제 창은 커밋하지 않는 cache의 `*-window.txt`에서 root가 읽을 수 있다. 단어 수는 정확한 raw UTF-8 slice의 Python `str.split()`이며 Markdown·코드 토큰도 포함한다. 도표 이미지는 모두 0개를 보여 주었다.

| 카드 | 당시 원문·절 | 행 | 실제 단어 | 카드에 보인 내용 | 카드에 없는 내용 |
| --- | --- | --- | ---: | --- | --- |
| VN01 | [v5.0.0 Field](https://github.com/vega/vega-lite/blob/d7cecefe310811d00276bb09bfd78312f1a19759/site/docs/encoding/field.md), 문자열 field 절 | 28–36 | 130 | nested dot/bracket 접근, literal 점·괄호의 escape, JSON escape | calculate의 정의; wrapped facet·dual axes의 실제 출력; 빈 문자열 aggregate |
| VI01 | [v5.0.0 nested aggregate example](https://github.com/vega/vega-lite/blob/d7cecefe310811d00276bb09bfd78312f1a19759/examples/specs/test_aggregate_nested.vl.json), 독립 spec 전체 | 1–36 | 72 | nested properties를 직접 field로 참조해 sum bar를 정의한 2행 숫자 입력 | facet, 서로 다른 두 Y 축, 원문 135행 및 문자열 수치, 실제 기대그림 |
| VN02 | [v5.1.0 CompileOptions](https://github.com/vega/vega-lite/blob/64739639fd85d9be605704c91425d26450d25b9c/src/compile/compile.ts), 공개 API interface | 24–39 | 33 | `fieldTitle` formatter option의 존재 | callback의 정확한 입력 signature, escape 제거 구현, 반복 셀별 실제 title 출력 |
| VI02 | [v5.1.0 formatter usage](https://github.com/vega/vega-lite/blob/64739639fd85d9be605704c91425d26450d25b9c/site/usage/compile.md), Customized Field Title Formatter | 57–72 | 68 | 문서가 `titleFormat`으로 부르는 callback 예제; field·aggregate·timeUnit·bin에 따른 표시 title | N과의 이름 불일치 해결법, escape 제거 코드, 실제 예제 출력 |
| VN03 | [v5.1.0 Conditional Axis Properties](https://github.com/vega/vega-lite/blob/64739639fd85d9be605704c91425d26450d25b9c/site/docs/encoding/axis.md), 해당 API 절 | 119–127 | 84 | 축 datum에 label/value/index가 있다는 설명 | 원본 record의 resilience가 전달된다는 보장, v2 가용성, 실제 색상 출력 |
| VI03 | [v5.1.0 conditional axis example](https://github.com/vega/vega-lite/blob/64739639fd85d9be605704c91425d26450d25b9c/examples/specs/line_conditional_axis.vl.json), 독립 spec 전체 | 1–39 | 114 | time tick의 datum.value와 month 조건을 사용하는 라벨·대시 예제 | nominal section에서 다른 원본 record 속성을 join하는 방법, 실제 원 요청 색상 출력 |

I의 실제 창은 각각 72/68/114단어이고 허용 상한은 200단어·그림1점이다. D도 같은 상한을 적용해야 한다. 실제 길이까지 일치시키려면 사례별 위 수치에 맞추거나 그 차이를 감도·제한으로 남겨야 한다. API N의 공통 창은 I와 D에 동일하게 포함해야 한다.

## 3. I 선택 경로와 추가 노출

| 요구 | 제목·파일명 검색 순서 | 첫 적격 절·탈락 | 실제 노출 |
| --- | --- | --- | --- |
| V01 | tag의 examples/specs에서 `nested` → `aggregate` | lexical 첫 `nested_concat_align`은 view nesting/axis extent이며 data field access가 아니어서 제외; 다음 `test_aggregate_nested` 채택; 뒤 `test_subobject_nested`는 읽지 않음 | nested_concat_align은 v5.1.0판에서 부수 확인했으므로 V01보다 뒤 판의 예제 노출이다. 그 내용을 V01 카드·동시대 판단에 쓰지 않음. field 문서 v4.17.0→v5.0.0과 calculate 정의도 읽음 |
| V02 | 공개 API의 `fieldTitle` → usage의 Field Title Formatter 표제 | formatter 절을 첫 적격 예제로 채택. repeat_splom은 repeat 원 입력 대응에는 유용하지만 callback을 설명하지 않아 I에서 제외 | usage 전체의 option 목록·컴파일 코드 호출부·channeldef callback signature·field escape 문서·repeat_splom 입력을 카드 밖에서 읽음. 잘되는 철자로 문서 예제를 고치지 않음 |
| V03 | axis 조건 표제 → examples/specs의 `conditional_axis` | lexical 첫 `line_conditional_axis` 채택; 뒤 `line_conditional_axis_config`는 미열람 | axis manual 전체를 먼저 읽어 다른 절·예제 이름도 노출됨. v5.1 타입과 v2.7 타입·매뉴얼은 가용성 보조 확인이며 N/I 창에는 없음 |

카드는 제목·색인으로 찾은 첫 적격 내용이지만, 이 작업자는 후보 창보다 넓은 문서와 구현도 읽었다. 이 지식을 N/I에 보인 문구의 효과로 돌릴 수 없다. 특히 V02·V03의 구현 확인은 실제 선택지를 구성하기 위한 가용성 확인이지, N만 읽은 사람의 반응을 관측한 결과가 아니다.

## 4. 조작 가용성에 관한 확인·반례

### V01 — 문서가 nested 자체를 금지하지 않는다

Field 절은 nested object lookup을 지원한다고 설명한다. [calculate 정의](https://github.com/vega/vega-lite/blob/d7cecefe310811d00276bb09bfd78312f1a19759/site/docs/transform/calculate.md) L8–24는 표현식으로 새 필드를 만들 수 있게 한다. 따라서 고정 기준판에서 direct nested 접근 B와 alias materialization A를 표현할 문법 근거는 있다. 다만 calculate 절은 VN01 밖이다. nested aggregate 예제도 단일 bar와 숫자 두 행만 갖고 있어 원문의 compound facet/dual axes 경계를 보장하지 않는다. 문서만으로 A가 필수라고 결론 내리면 지원 문구와 충돌할 수 있다.

### V02 — 옵션 이름과 예제가 실제로 충돌한다

공개 CompileOptions 및 compile의 설정 코드는 `fieldTitle`이다. usage의 앞 목록도 같은 이름이지만 formatter 절과 example은 `titleFormat`을 쓴다. 이 불일치는 현재 코드와 현재 문서의 일반론이 아니라 같은 v5.1.0 고정판에서 직접 확인했다. I에 보여 주는 예제를 고쳐서 N과 일치시켜서는 안 된다.

[channeldef.ts](https://github.com/vega/vega-lite/blob/64739639fd85d9be605704c91425d26450d25b9c/src/channeldef.ts) L861, L904–923, L957–959는 formatter가 field definition/config를 받아 문자열을 반환하고 defaultTitle이 그 formatter를 부르는 구현을 보인다. 이는 카드 밖 정보다. user spec의 서로 다른 repeat fields가 각자 적절한 문자열을 얻는 실제 출력은 아직 확인하지 않았다. B의 accessor escape 제거가 data lookup 의미를 바꾼다는 위험은 별도 field 문서에서 알고 있으나 VN02에 해당 설명이 들어 있다고 주장하면 안 된다.

### V03 — 최신 당시판과 schema major의 조건문 지원이 다르다

v5.1.0 [src/axis.ts](https://github.com/vega/vega-lite/blob/64739639fd85d9be605704c91425d26450d25b9c/src/axis.ts) L159–168/L266–318은 labelColor에 조건 객체를 허용한다. 반면 v2.7.0의 src/vega.schema.ts L654–657은 axis labelColor를 string으로 선언한다. 이 비교는 타입·공식 API 가용성 차이이며 실제 렌더 출력 차이를 관측한 것은 아니다. 저자의 `$schema: v2`를 실제 v2 renderer로 확정하지 않는다. 원래 조건식을 이용한 A/B의 판정은 연구 기준 v5.1.0에서만 조건부로 작성할 수 있다.

축 datum의 value가 ordinal section identity라는 연결은 VN03의 value 설명과 입력 encoding을 함께 읽어 세우는 해석이다. 원본 resilience 속성이 그대로 axis datum에 있다고 보는 연결은 N이 보장하지 않는다. A의 고정 category 문자열은 원문 10개 record에 한정되며 zero-category가 바뀌는 입력에 대한 일반 해결은 아니다.

## 5. V01 정상 editor 입력 복원

원 body 첫 editor URL의 payload를 [lz-string 1.4.4 원본](https://github.com/pieroxy/lz-string/blob/1.4.4/libs/lz-string.js)의 URI decompressor로 복원했다. 원본의 알파벳·decoder·module export를 읽은 뒤 `decompressFromEncodedURIComponent`와 `JSON.parse`만 실행했다. chart/표현식 실행은 없었다. 도구 코드의 SHA256은 `54a9eaac48d4fc5f190b88550c6f942c6f7af9576e171fe5de24c16a0dba82c3`이고 실행 exit는 0이다.

정상 payload는 barley.json, facet site, bar median(yield)+year color, line sum(yield)다. 원 경계는 `_source` 135행, bar sum(Readability), line count(Unit_Key_Message)다. 두 spec에 inner/outer independent resolve가 모두 있지만 **data·aggregate·color도 달라 정상→경계의 차이를 nested 여부 하나의 효과로 귀속할 수 없다.** 같은 입력에서 A/B를 비교하는 조건은 따로 유지해야 한다. barley dataset과 실제 출력은 읽지 않았다.

입력·출력 해시와 source URL, 방법은 decode-7278-receipt.json, 복원 JSON은 cache/7278-normal-decoded.json이다. 같은 issue 원문의 복원이며 독립 저작 수를 추가하지 않는다. 단계①의 미복원 상태를 지워 사전에 알았던 것처럼 만들지 않는다.

## 6. 저작 수와 조사 한계

- receiver-sources.jsonl은 19개 실제 내용 열람 행과 메타데이터 1행·경로 실패 2행(총 22행)을 가진다. Vega-Lite 공식 manual의 여러 절·판은 `vl-official-manual` 하나다. 코드의 여러 파일·판은 `vl-implementation` 하나다.
- 독립적으로 구성된 예제는 nested aggregate, conditional axis, repeat splom, nested concat align 네 저작이다. 카드에 쓴 독립 예제는 앞 두 개다. usage formatter는 manual의 일부이므로 독립 예제 배당으로 따로 더하지 않는다.
- lz-string은 입력 복원 도구이며 수신 공식 설명 배당에 넣지 않는다. decoded URL도 #7278과 같은 저작이다. release metadata는 문헌판 고정에만 사용하며 실질 설명 저작으로 추가하지 않는다.
- 실패 경로 `v5.1.0:src/fielddef.ts`, `v2.7.0:site/docs/axis.md`는 각각 실제 channeldef.ts와 site/docs/encoding/axis.md로 바로잡았다. 이 잘못 추정한 경로는 원문 수에 넣지 않는다.
- 최초 요청 수정판·정확 author runtime, 사용자 채택·시간·창의성, 같은 입력의 두 조작 렌더 출력은 모두 미확인이다. 근거의 설명력과 실제 사용자 효용을 구별한다.
