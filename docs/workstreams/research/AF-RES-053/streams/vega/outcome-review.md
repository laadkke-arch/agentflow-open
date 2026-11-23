# Vega-Lite 후속 자료 대조

예측 봉인: `9b13473a76a381fe27d775524aa65416ec28f591` (원격 commit 시각 2026-11-23T01:55:36Z). `git ls-remote`와 원격 commit metadata로 이 SHA를 확인한 뒤, **2026-11-23T01:58:10.743Z**에 첫 후속 댓글 요청을 시작했다. frozen `predictions.csv`, `cards.csv`, `operations.json`, `evidence/operation-refinements.json`의 해시는 `outcome-retrieval-receipts.json`에 있다. 조사자: `/root/vega_frame`; 독립 검토는 미실시.

## 1. 결과와 분모

| 요구 | 봉인 N / I / D | 확보한 새 후속 근거 | 정확한 판·입력·조작·출력 충족 | I 대 D |
| --- | --- | --- | --- | --- |
| V01 / #7278 | 판별불가 / 판별불가 / 판별불가 | 다른 ecommerce 입력의 nested/alias 그림 및 입력 JSON | 0/4 cells; 원래 135행의 frozen A 미확보 | 예측은 같음. 역사 출력에 대한 우열 미확인 |
| V02 / #7422 | A만 / A만 / A만 | 다른 사용자의 dot field 실패 진술과 explicit title 제안 | 0/4 cells; formatter A의 실제 그림 미확보 | 예측은 같음. 역사 출력에 대한 우열 미확인 |
| V03 / #7507 | A만 / A만 / A만 | 유지보수자의 category 조건과 작동 진술 | 0/4 cells; 1 red/9 black 직접 출력 미확보 | 예측은 같음. 역사 출력에 대한 우열 미확인 |

여기서 4 cells는 normal/boundary × A/B이다. V03의 normal 9행과 boundary 1행은 **한 출력의 부분집합**이지 독립 실행 10회가 아니다. strict 완전 충족은 **관측 0/12**이며 runtime patch·입력·조작·직접 출력 중 결손을 가진 각 cell의 판정은 미확인이다. 0/12를 실패율이나 A/B 동률로 해석하지 않는다.

세 사례에서 I와 D의 사전 선택 및 출력 예측은 모두 같다(3/3). 서로 다른 사전 예측이라는 조건부 분모는 0이므로 **D의 새 정답 판정은 해당 없음**이다. 실제 성능의 동률은 자료가 부족해 미확인이다. 결과를 보고 기존 표본·A/B·예측을 고치지 않았다.

열람은 댓글 17개(10/1/6), timeline 39 events(23/6/10), 후속 PNG 5개, baseline PNG 2개, 후속 ecommerce 첨부 1개, 연결 compressed editor 입력 6회(고유 decoded payload 4개)이다. source ledger는 23행이나 고유 work_id는 기존 요청자 이슈 **3개**다. 댓글·그림·첨부를 별도 저작으로 늘리지 않아 **요청자 저작 외 새 고유 후속 저작은 0**이다. 후속 저작 6건 배당의 충족 자료로 부풀리지 않는다.

## 2. normal/boundary × A/B 위치

| 요구 | normal A | normal B | boundary A | boundary B |
| --- | --- | --- | --- | --- |
| V01 | barley에서 alias A의 출력 없음 | maintainer의 barley 그림은 좌우 축을 보임. 정확 runtime·역사 data snapshot·전체 panel 미확인 | 원래 asset 135행의 3-alias A 출력 없음 | 원문 그림에서 축 위치 문제를 확인. 이미 알고 있던 baseline이며 runtime 미확인 |
| V02 | formatter A 출력 없음 | escape 제거 B 출력 없음 | 원문 4×4 그림은 escaped access+default title인 baseline. A callback 실행이 아님 | 후속 사용자의 `foo.bar` 빈 chart 진술은 다른 입력·제품판 미상. 원래 repeat 출력 없음 |
| V03 | category 조건이 작동한다는 maintainer 진술, 비zero 9개 실제 색 미확인 | 본문 B 보고 외 새 실제 출력 없음 | 같은 category를 비교하라는 답과 작동 진술, 실제 1 red/9 black 미확인 | 본문 zero 라벨이 black인 문제는 사전 노출. 새 출력 없음 |

## 3. V01 — 유사한 성공 그림이 frozen A를 검증하지 못하는 이유

[첫 후속 maintainer 그림](https://github.com/vega/vega-lite/issues/7278#issuecomment-789105122)은 본문의 barley 예시와 연결된다. site별 bar/line와 좌우 y축이 보이지만 아래쪽 panel은 잘린다(VO10). runtime patch와 당시 `data/barley.json` 내용은 고정되어 있지 않다.

이후 원작성자는 [ecommerce 입력과 그림](https://github.com/vega/vega-lite/issues/7278#issuecomment-789489604)을 올렸다. 첨부 JSON은 `data.values.hits.hits` 4,675행이다(VO15). 이 댓글의 inline editor와 다음 참여자의 minimal 재현은 10행이다. **원문 asset 135행, ecommerce 첨부 4,675행, minimal editor 10행을 서로 같은 입력으로 취급하지 않는다.**

[nested 재현](https://github.com/vega/vega-lite/issues/7278#issuecomment-792093389)과 [alias 변형](https://github.com/vega/vega-lite/issues/7278#issuecomment-792119011)의 원본 PNG를 직접 열었다(VO12/13). 앞 그림은 count 축이 plot 내부/왼쪽에 있고 뒤 그림은 오른쪽 경계에 있다. 이 범주적 위치 차이는 관측되었다. 다만 decoded payload를 비교하면, 후자는 `day_of_week` alias를 만들어 두 x뿐 아니라 **line y의 count field도** 그 alias로 바꾼다(VO21). 댓글의 x만 바꾸었다는 설명을 그대로 구현 사실로 옮기지 않았다. 이는 frozen A의 세 alias 및 원래 135행과 일치하지 않는다.

마지막 [maintainer의 3-alias 링크](https://github.com/vega/vega-lite/issues/7278#issuecomment-792800527)도 해독했다(VO23). field 접근 외에 inner axis resolve, line count의 field, zero:false 등이 함께 빠진다. 따라서 이 링크의 작동 진술을 frozen A의 성공으로 채점할 수 없다. payload 해독은 입력 확인이며 현재 editor 렌더는 미실시했다.

**저자 수락 / 패치 / 시험 / 출력:** 원작성자의 성공 수락 진술 관측 0/1; 실제 수락·사용 결과는 미확인. 댓글과 전체 timeline에 연결 PR·commit event 관측 0이나 구현 패치 존재 여부는 미확인. 고정 회귀시험·기대 SVG는 미확보. 실제 후속 그림은 존재하지만 frozen 비교 조건과 불일치한다.

**사용 링크와 중단 조건:** 위 nested/alias 댓글은 field materialization과 axis 배치가 연결될 수 있는 재현을 읽는 데 쓸 수 있다. 원래 135행 또는 다른 renderer로 확대하려면 멈추고 동일 입력·resolve·aggregate를 고정해야 한다. 카드를 읽은 것만으로 해당 bug의 보편적 수정을 약속하지 않는다.

## 4. V02 — 다른 사용자의 실패 경험과 제3 조작

[유일한 후속 댓글](https://github.com/vega/vega-lite/issues/7422#issuecomment-925118846)은 `foo.bar`라는 literal field를 포함한 3행 bar spec이다(VO02). 사용자는 escape 제거 때 빈 chart를 경험했다고 말하고 escaped field와 별도의 unescaped title를 함께 주는 방법을 제안한다. 이 사례는 데이터 접근 문자열과 표시 문자열을 분리해야 한다는 방향을 뒷받침하지만, 원문의 penguin 3행 repeat 4×4와는 다른 입력이다. explicit title은 frozen `fieldTitle` callback A와 다른 조작이다.

원문 PNG를 봉인 뒤 직접 열어 4×4 점과 field별 축 제목·범례의 backslash를 확인했다(VO17). 이는 이미 읽은 본문 문제의 baseline 확인이다. **formatter A의 결과나 B의 원문 repeat 실패를 새로 관측한 것이 아니다.** 당시 문서의 `titleFormat`/구현의 `fieldTitle` 불일치도 실제 후속 chart를 증명하지 않는다.

**저자 수락 / 패치 / 시험 / 출력:** 원작성자 수락 진술 관측 0/1, 실제 사용결과 미확인. 연결 PR·commit event 관측 0/6 timeline events; 번호 없이 진행된 구현 수정은 미확인. 공개 고정 시험 및 후속 PNG/SVG는 미확보.

**사용 링크와 중단 조건:** 후속 댓글은 literal dot 접근과 title 생성의 결합 오류를 재현하는 데 쓸 수 있다. 모든 repeat 셀에 맞는 title인지 확인하지 않은 채 하나의 explicit title을 전체 셀에 복사하면 중단해야 한다. 정확한 callback과 전체 repeat 출력 없이는 A의 조건부 예측을 검증된 해결로 제공하지 않는다.

## 5. V03 — maintainers의 작동 진술과 실제 출력의 차이

유지보수자는 [category 조건 예시](https://github.com/vega/vega-lite/issues/7507#issuecomment-854816048)를 주었고, [후속 답](https://github.com/vega/vega-lite/issues/7507#issuecomment-854963205)에서 작동하며 `warn`을 제거할 수 있다고 말했다(VO03). 따라서 진술의 조건을 정규화하면 frozen `datum.value` A와 대응한다. 그러나 직접 그림·SVG·색별 라벨 목록은 없다. 원작성자의 답은 다른 방법을 찾아보겠다는 내용이며 성공 실행 확인으로 읽지 않는다. 뒤의 감사는 다른 참여자의 댓글이다.

[scale domain 설명](https://github.com/vega/vega-lite/issues/7507#issuecomment-856020988)은 axis dataset과 원본 행의 다른 필드 사이에 항상 일대일 대응이 있지 않음을 밝힌다. 이는 Q4/Q7의 중요한 적용 한계다. 고정 10행의 특정 category를 고르는 A가 새로운 zero-category를 자동 추적하는 요구까지 해결했다고 주장하면 목표를 바꾼 셈이다.

**저자 수락 / 패치 / 시험 / 출력:** maintainer의 명시적 작동 진술은 관측했다. 원작성자의 성공 수락 진술 관측 0/1, 실제 사용결과 미확인. maintainer가 completed로 닫은 metadata는 author 수락이나 패치/시험이 아니다. 연결 PR·commit event 관측 0/10 timeline events; 고정 회귀시험과 실제 출력은 미확보. 원문 schema v2와 연구 기준 v5.1.0의 차이는 계속 남는다.

**사용 링크와 중단 조건:** 위 답은 label expression이 보는 객체와 scale-domain의 관계를 점검할 때 유용하다. schema/runtime를 동일시하거나 fixed-category 조건을 일반적인 원행 속성 join으로 간주하려면 적용을 중단해야 한다.

## 6. 후속 탐색의 경계와 사후 복원

각 comments/timeline 응답은 100개 미만이었고 issue metadata의 comments 수 10/1/6과 맞았다. 세 timeline에 연결 PR나 commit event는 없었다. 로컬 repository clone의 모든 보유 refs에서 `(#|issues/)(7278|7422|7507)([^0-9]|$)`를 commit message에서 찾은 결과도 0이었다(실행 명령과 exit 0은 영수증). 이 제한된 탐색은 **관련 구현 패치가 전혀 없다는 증명은 아니다**. 연결이 없어서 특정 PR의 release/test baseline을 연쇄 추적할 출발점도 확보하지 못했다. 무관한 후속 저작으로 배당을 채우지 않았다.

| issue | 사후 timeline에서 복원한 이전 제목 | 이후 제목 | 후보 membership |
| --- | --- | --- | --- |
| #7278 | Independent Y axes for dual axis wrapped facet | Independent Y axes for dual axis wrapped facet and nested fields breaks axis layout | 둘 다 `axis` 포함; 불변 |
| #7422 | Axis labels render with escaping characters | Axis/legend labels render with escaping characters | 둘 다 `axis` 및 `label` 포함; 불변 |

제목 수정 시각은 각각 2021-03-08T14:42:18Z와 2021-04-30T08:15:42Z다(VO04/05). 이 사후 지식을 `outcomes.json`에 남겼으며 기존 `frame.csv`를 바꾸지 않았다. 최초 본문의 edit history는 여전히 복원하지 못했다.

## 7. 재개에 필요한 최소 자료

V01은 원래 asset 135행과 역사 barley snapshot, 작성자 runtime patch, frozen A/B의 전체 출력이 필요하다. V02는 원작성자 runtime과 원문 penguin repeat에서 정확한 callback A 및 accessor escape 제거 B의 전체 출력이 필요하다. V03은 실제 renderer 버전과 같은 10행 A/B의 SVG 또는 색별 label 목록이 필요하다. 연구 기준판에서 새로 재생하더라도 역사 작성자 출력과 별도 panel에 두어야 한다.

이번 작업에서 renderer 실행, live editor 실행, 역사 binary 재생은 **미실시**다. 공개 후속 자료와의 대조에는 필수 출력이 부족하고, 공개 자료의 결손을 새 실행으로 대체하지 않았다. 부모 인계의 실행 명령은 `outcome-retrieval-receipts.json`의 decoded 입력 hash, frozen operation refinements 및 위 version/input 결손을 정확히 참조해야 한다.

## 가장 중요한 불일치·약점 3건

| 불일치·약점 | 영향받는 주장 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀔 조건 |
| --- | --- | --- | --- | --- |
| V01 성공처럼 보이는 후속 그림은 다른 입력·다른 조작 | frozen A가 원래 nested135행을 고친다는 주장 | [alias 댓글](https://github.com/vega/vega-lite/issues/7278#issuecomment-792119011), [3-alias 댓글](https://github.com/vega/vega-lite/issues/7278#issuecomment-792800527); VO13/21/23 | 원래135행에 A만 적용하고 resolve/aggregate 동일한 역사 output 확보 | 같은 판·입력·A/B의 축 위치/값 대응 결과가 모두 존재 |
| V02는 formatter 출력 없이 제3 방법만 제안 | N/I/D의 A 예측이 맞았다는 주장 | [후속 댓글](https://github.com/vega/vega-lite/issues/7422#issuecomment-925118846); VO02 | exact callback과 원래 repeat4×4의 A/B 전체 SVG 확보 | 셀별 제목 및 값 접근이 함께 검증됨 |
| V03은 maintainer 진술만 있고 schema/runtime도 다름 | 1 red/9 black 예측의 실제 검증·저자 수락 | [작동 진술](https://github.com/vega/vega-lite/issues/7507#issuecomment-854963205); VO03 | 작성자 renderer patch와 원10행 A/B 출력 확보 | 같은 판에서 실제 label 색 목록이 대응하고 author 실행결과가 확인됨 |
