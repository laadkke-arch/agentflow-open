# 공개 사후 답·채택·실행의 분리

사전 후보 봉인: `a04fbb20ca1a415235f69a1018a93e07e7adc926`. 질문의 현재 메타데이터/채택은 2026-11-23T16:49:40Z부터, 현재 답은16:49:46Z부터, 최초 답 개정은16:50:41Z부터 읽었다. 이전 A/B 검색에는 답·댓글·채택·현재 본문을 사용하지 않았다. API 응답은 모두 has_more=false였다.

## 답 첫 보존판

| 질문 | 답 ID·최초판 | 최초 공개 UTC | 현재 채택 | 최초→현재 본문 |
|---|---|---|---|---|
|J1|[78264532](https://stackoverflow.com/revisions/EA0B9F38-7255-42DC-A735-7877C3053139/view-source)|2024-04-02T23:47:29+00:00|아니오|변경 있음; GUID/해시는 영수증 참조|
|J1|[78264541](https://stackoverflow.com/revisions/0C25E76B-65A7-4BE5-A6A8-1576F3712702/view-source)|2024-04-02T23:51:19+00:00|예|같음|
|J2|[78265948](https://stackoverflow.com/revisions/75CDFE75-DD66-4AB6-9ED7-AE39D1B19380/view-source)|2024-04-03T07:27:13+00:00|예|변경 있음; GUID/해시는 영수증 참조|
|P1|[78275798](https://stackoverflow.com/revisions/71FEDE47-AD45-4CE2-ACEA-5799EBF05343/view-source)|2024-04-04T18:08:10+00:00|아니오|같음|
|J3|[78304820](https://stackoverflow.com/revisions/08368F0F-FFEE-4CB1-A656-5D2F3C9C83B2/view-source)|2024-04-10T13:34:18+00:00|예|변경 있음; GUID/해시는 영수증 참조|
|P2|[78314393](https://stackoverflow.com/revisions/C8A5C488-3B9E-4260-9C49-0750D75A0653/view-source)|2024-04-12T05:45:31+00:00|예|같음|
|P3|[78364883](https://stackoverflow.com/revisions/B3123941-E2B1-490B-AC84-C974E65DF53D/view-source)|2024-04-22T08:29:15+00:00|예|같음|

7개 답은 모두 원 질문 생성 후30일 이내다. 공개 API에서 이후 답0·댓글0이며, 이는 삭제되거나 비공개인 활동이 없다는 증명이 아니다. 현재 채택은5질문, 미채택1질문(P1)이다. 채택시각은 모두 미확인이다. J2의30일 이후 질문 수정은 현재 태그에서 jquery/lib가 빠진 사실과 연결되지만 새 성공 실행 기록은 아니다. J3 R0와 현재 응답의 본문 해시 차이는 코드 블록의 lang-none/prettyprint HTML class만이며 입력·출력·명령 내용은 동일하다.

## 사례별 증거 수준

| 질문 | 공개 주해법 | 질문자·답변자 행동 구분 | 반환 변화 |
|---|---|---|---|
|J1|walk 또는 recursive descent로 food만 갱신. 최초 비채택답의 불필요한 . \| 는 다음 날 제거.|질문자가 jqplay 소개에 감사했으나 이는 실행 성공 확인이 아니다. 이어 --argjson 답의 ... 생략부호를 그대로 실행해 실패했다고 질문. 답변자가 완전 명령을 후속 댓글로 제공. [실행 시도·실패 보고(보조 --argjson 예); 주해법 성공 출력·정확판 미확인](https://stackoverflow.com/questions/78264525#comment137978352_78264541)|유지: 완전한 walk 식을 반환하고 ... 생략 표기를 쓰지 않는다.|
|J2|tasks[]로 선택하고 project="app2"로 갱신. 새 값 app2는 답변자가 택한 예시.|질문자 후속 댓글/실제 출력 없음. 질문 댓글은 모든 대상에 같은 값을 넣는지, 파일을 바꾸려는지 되묻는다. 현재 본문도 끊어진 JSON이다. [채택만 확인; 질문자 실행·출력·정확판 미확인](https://stackoverflow.com/questions/78265746#comment137980464_78265746)|유지: 읽기/갱신 연산은 제공하되 완전 입력·새 값·대상 선택은 질문한다.|
|J3|동적 인덱스 .[$key]와 갱신 연산. 최초 답은 *=10 보조 예와 1998 출력이 불일치했고 약5분 뒤 *=999로 수정.|답변자 출력은 b=1998인 곱셈 예다. 원 요구 b=42의 질문자 출력이나 사용판은 없다. [답변자 예시 출력 + 채택; 질문자 실행 미확인](https://stackoverflow.com/revisions/08368F0F-FFEE-4CB1-A656-5D2F3C9C83B2/view-source)|유지: .[$key] += 40으로 원 기대값42를 보존한다. 답의 숫자999를 복사하지 않는다.|
|P1|LuaLaTeX로 엔진을 바꾸고 luaotfload fallback에 NotoColorEmoji를 넣는 답. 현재 채택 표지 없음.|답에는 PDF YAML만 있고 원 질문자의 PDF/HTML 동시 사용 결과·설치폰트·정확판·코드포인트 보고가 없다. [답변자 설정 예만; 질문자 실행·채택 미확인](https://stackoverflow.com/a/78275798)|보완: fallback/엔진 교체 후보를 사후 카드에 추가하되 HTML 요구와 설치·글리프 커버리지 때문에 부분 유지.|
|P2|toprule/bottomrule 재정의. 공개답은 각 매크로 [2]{}로 뒤의 두 토큰을 소비하며 header-includes 또는 본문 앞에 삽입.|채택 표지만 있으며 실제 원 .tex/PDF 출력·Quarto/Pandoc/TeX 정확판이나 질문자 댓글은 없다. 원 이미지 직접 바이트 접근은403, 웹 도구는 이미지 표시만 반환해 픽셀 검증 못함. [채택만; 원 구현 연결·실제 실행 미확인](https://stackoverflow.com/a/78314393)|정정: 사전 완결은 고정 Pandoc 조건부 판단으로 보존. 원 Quarto 전체사슬은 부분으로 보수 판정; 검색 실패와5접근시도로 엄격 비교불가.|
|P3|Markdown reader의 example_lists 확장과 citation 표기의 충돌. --from=markdown-example_lists로 끄는 주 도구 내부 해법.|질문자가 페이지 번호 추가/제거를 시험했고 Tarleb 답으로 해결됐다고 공개 댓글. 원 명령·bib/CSL·정확판·해결 후 출력은 없다. [질문자 해결 보고 있음; 정확판과 출력 동반 재현은 미확인](https://stackoverflow.com/questions/78358965#comment138159258_78358965)|변경: BBT/CSL 결손 중심의 두 링크 대신 example_lists 비활성화 문서와 공개 후속을 반환. 사전 A/B 부분 판정은 그대로 보존.|

## 중요한 불일치

- J1: 주해법 두 jq 예와 별개로 --argjson 설명의 생략부호가 실제 사용 장벽이 됐다. 채택·demo 감사는 정확한 원 명령의 성공 영수증이 아니다. 두 jqplay 링크는 HTTP403과 웹 도구 접근 실패로 실행판/출력을 확인하지 못했다.
- J3: 답의 방법은 맞는 계열이나 계산값을 그대로 복사하면 원 기대값42와 다르다. 최초 답의 보조 *=10 예는 출력1998과도 불일치했고 뒤에999로 수정됐다. 반환은 원래 +=40 목적을 유지한다.
- P1: 새 답의 LuaLaTeX/luaotfload/NotoColorEmoji는 인접 소비자 설정이라는 점에서 유망하다. 그러나 그 답은 HTML 요구·font 설치·원 Unicode 문자를 검증하지 않았으므로 완결로 올리지 않는다.
- P2: 채택 답의 [2]{} 매크로 재정의와 봉인한 인수 없는 {} 재정의는 문자 그대로 같지 않다. 두 가지 모두 고정 writer의 rule 명령에 관한 후보이나, 실제 Quarto 템플릿·생성 TeX·PDF 결과는 미확인이다. 독립 코드 감사의 부분 권고와 예산 민감도를 수용한다.
- P3: 질문자의 해결 보고는 있지만 전체 command/bib/CSL와 정확판·출력은 없다. 사후 문서·파서 확인은 example_lists 해법이 주 도구 내부임을 지지한다. 이 정보로 사전 B를 성공으로 재채점하지 않는다.

## 결원과 다음 최소 관측

원 질문자가 정확판·실제 명령·입력·출력을 함께 남긴 완전 성공은 확인0/6이다. 실제 성공률의 분모가 될 그 완비 실행은0건이므로 그 성공률은 **산출 불가**다. 확인0/6은 성공이 없었다는 뜻이 아니다. P3 한 건의 해결 자기보고와 J1 한 건의 보조예 실패 보고는 별도로 유지한다.

P2 원 이미지: https://i.sstatic.net/V5Tdz.png 는 직접 접근403이었다. 웹 open은 ImageDisplayed 문자열만 반환해 검사할 래스터가 없었다. 선 개수는 R0 본문 설명을 근거로 삼았고 이미지 픽셀 확인으로 보고하지 않는다.

재열람은 `api-receipts.json`의 질문/답/댓글 API와 `answer-first-receipts.json`의 GUID API를 쓴다. 원출력·사용판이 더 공개되면 outcomes.csv 사후 열을 새 커밋으로 갱신하고 봉인한 candidates.csv는 유지한다.
