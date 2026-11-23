# ProseMirror 후속 대조와 반증

검토 주체: 동일 모델의 ProseMirror 보조 조사자. 원문 모집·카드·예측과 후속을 같은 조사자가 읽었고, 사람 독립 검토나 창만의 인과 효과 검정은 아니다. 봉인판은 `74dc9f887bc47bc0a92b9a75ea327ffa30aca70b`, 첫 후속 열람은2026-11-23T03:32:31.973Z. 최초 자연 본문판은 복원하지 못했고 현재 REST 본문의 해시를 보존했다.

## 직접 확인한 핵심

PN1(#892)의 원래 실패는 원격 변경을 undo에서 제외하는 옵션만으로 설명되지 않는다. [연결 수정9bdb377](https://github.com/ProseMirror/prosemirror-history/commit/9bdb3774203d21e3ec14e621eb444524c629b7a3)은 rebasing 때 선택 북마크를 이미 처리한 mapping까지 다시 통과시키던 오프바이원 문제를 고친다. 새 시험도 `addToHistory=false`를 사용한다. 따라서 같은 옵션을 사용하는 구현에서도 구판의 선택 범위가 잘못될 수 있다. [유지보수자](https://github.com/ProseMirror/prosemirror/issues/892#issuecomment-465075360)는1.0.4를 안내하고 [요청자](https://github.com/ProseMirror/prosemirror/issues/892#issuecomment-465079148)는 해결됐다고 답했다. 이 대화는 고정한 metadata opA/opB의 정확 출력 비교가 아니다.

원작성자 [재현 코드](https://github.com/johanneswilm/pm-collab-test/blob/50aca6003eac6890a36fd7b21a2e90a99b8bf7c6/src/index.js), [초기 HTML](https://github.com/johanneswilm/pm-collab-test/blob/50aca6003eac6890a36fd7b21a2e90a99b8bf7c6/index.html), [lock](https://github.com/johanneswilm/pm-collab-test/blob/50aca6003eac6890a36fd7b21a2e90a99b8bf7c6/package-lock.json)을 뒤에 확보했다. 그 입력은 모집 본문25..30보다 줄인6..13 선택이며 원격 삽입의 구체적 순서가 있다. 사후에 새로 알게 된 이 입력을 봉인 때 알았다고 소급하지 않았다.

PN2(#1341)에서 같은 분야의 마지막 링크는 [undoInputRule API](https://github.com/ProseMirror/prosemirror-inputrules/blob/40ef4104e086517283081c713727a7f029b565c1/src/inputrules.ts#L105-L107)다. [댓글](https://github.com/ProseMirror/prosemirror/issues/1341#issuecomment-1343353599)도 이 명령을 가리키지만 실제 출력·redo·판은 보여 주지 않는다. 최소 보충 입력을 실행하니 즉시 opB는 `...`를 복원하고 `undoDepth=1, redoDepth=0`을 남긴다. 다음 `history.redo`는 false이고 transaction을 보내지 않는다. 같은 목표에 나중 `x`가 끼면 opB 자체가 false여서 `…x`가 남는다. 단어가 돌아오는 것, 나중 작업을 보존하는 것, 기존 history.redo를 사용할 수 있는 것은 별개다.

PT1의 [원시험](https://github.com/ProseMirror/prosemirror-history/blob/554d6eedb76704d1db62d85768611ce4b611abd2/test/test-history.ts#L31-L38)은 `a`, `b`를 연속 넣고 undo 후 빈 문단을 기대한다. 이 기대는 봉인 전에 E의 다른 그룹 시험에서 의미상 노출됐으므로 신규 적중으로 세지 않는다. 다음 `enables redo` 시험은 다른 선언이며 선택 시험에 원래 포함된 것으로 합치지 않는다. 연구자가 추가한 closeHistory opB는 `a`만 남기며, 원격 `b`가 capture에서 제외된 경계에서는 A/B 모두 `b`를 남긴다.

## Q별 주장·반대 근거·뒤집힐 조건

| Q | 이 stream이 답한 내용 | 직접 근거 | 반대·한계 | 뒤집힐 최소 확인 |
| --- | --- | --- | --- | --- |
| Q1 | PN1은 다른 작성자 텍스트 보존이 추론이고 선택25..30이 명시 목표다. PN2는 세 점을 남기는 목표가 명시돼 있다. | P-I892,P-I1341,frame.csv | PN1을 순수한 ‘상대 문장 보존’ 요청이라고 재서술하면 원뜻을 넘는다. 엄격한 literal retained-text 기준에서는 PN1 제외. | 원작성자의 최초 본문판에서 명시한 보존 텍스트와 사건열 확보 |
| Q2 | metadata capture, history 경계, last InputRule undo는 구현에서 구별된다. | P-API103/P-API150/P-IR120; source-runtime-check5/5 | PN2는 같은 flag 변화가 아니라 command의 대상 범위 변화다. 이 차이를 숨기면 균일한 A/B 실험이 아니다. | 같은 history API 한 flag만으로 원 PN2 목표를 충족하는 판·동작 확인 |
| Q3 | 관련 작업 예제 E는 API가 말하는 제외/그룹을 구현 예로 보여 주지만 PT1 정답을 미리 노출했다. | P-E103-CAPTURE,P-E130-GROUP,P-E150-GROUP | 일반 wiring 예제는 relevance 부족으로 봉인 전 제외. 짧은 코드 창과 자연어 D는 단어·그림 수가 같아도 정보 밀도·코드 행수가 다름. | 정보 단위를 통제한 별도 사전 실험에서 E/D 선택이 갈리는 근거 확보 |
| Q4 | 현재 텍스트와 남은 이력의 보존을 다른 변수로 물어야 한다. | PN1 역순 replay undoDepth0/1; PN2 redo false | 지도·회계 원전의 사실 검토는 다른 stream 소관이다. 이 실행만으로 감사 원장의 영속 ID/불변 기록을 증명하지 않는다. | 원장의 취소가 보존하는 변수와 editor stack/identity의 일대일 계약을 실제 시험으로 연결 |
| Q5 | 세 자리 A/E 예측은 바뀌지 않았고 원래 unknown과 연구 보충을 유지했다. | 봉인cases.json; root predictions.csv | E 밖의 API·다른 시험·모델 지식이 이미 노출됨. 독립 읽기 참가자 성과가 아니다. PT1 신규성 제외. | 출력과 의미상 같은 시험도 가린 새 모집·예측·관측의 순서 |
| Q6 | 선언된 원시험, 작성자 수정 수락, 코드 수정, 연구 실행을 분리했다. | observations.json, P-T150-OUT,P-FIX892,P-O892-C,replay receipts | 네 정확 SHA의 CI 조회는 전부0기록; ‘pending’은 기록 없는 aggregate일 뿐. 공개 같은 A/B 쌍 검증은0/3. | 같은 원판·원입력·두 조작과 전체 텍스트/선택/stack을 담은 공개 실행 증거 |
| Q7 | 여기서 반환할 구현 링크는 PN1 rebasing fix, PN2 undoInputRule 조건, PT1 closeHistory 경계다. | 아래 반환 조건, 실제 출력·패치 | D의 새 정답 판정은 root가6자리 원장 전체에서 해야 한다. 이 stream 단독으로 donor 우열을 주장하지 않는다. | E가 못 고른 상태에서 D의 사전 고유 예측이 같은 입력·판의 출력으로 확인됨 |

## 다른 변화에서 나온 세 가지 반례

1. [#892 수정](https://github.com/ProseMirror/prosemirror-history/commit/9bdb3774203d21e3ec14e621eb444524c629b7a3): 원격 편집이 undo 대상에서 제외돼도 선택 북마크 mapping 구현이 틀릴 수 있다. 원기록의 유지라는 목표와 그 목표를 구현하는 버그 없는 알고리즘은 분리해야 한다. 원래 추가 시험에는 최종 텍스트 assertion이 없다는 점을 보존했다.
2. [#984 수정](https://github.com/ProseMirror/prosemirror-history/commit/c8f47adf3db77f2fe8756fb28451f8fa1c984958): 늦게 append된 트랜잭션을 이전 그룹에 붙이는 [선행 패치](https://github.com/ProseMirror/prosemirror-history/commit/ab0951c27445a2a154937e53c61ad87363b2d4ee)가 명시적으로 닫은 history 경계까지 무시했다. 요청자의 [복수 변경 작업 우회](https://github.com/ProseMirror/prosemirror/issues/984#issuecomment-555118638)와 [후속 수정 수락](https://github.com/ProseMirror/prosemirror/issues/984#issuecomment-563340744)을 모두 읽었다. 같은 사건의 두 패치를 독립 두 저작·두 요구로 늘리지 않았다.
3. [#1311 수정](https://github.com/ProseMirror/prosemirror-history/commit/f70697ef0cb6f06f0f9e0b719865d115f8c5f1c6): 동일한 composition이 선택 이동·시간 지연 때문에 여러 undo event로 쪼개지는 문제를 composition ID로 묶는다. 한 사람이 연속 입력했다는 서술만으로 독립 undo 단위가 결정되지 않는다. 해당 patch에 새 시험이 없으며 플랫폼별 원보고도 서로 달랐다.

## 설계자에게 돌려줄 링크와 중단 조건

**PN1.** [선택 mapping 수정](https://github.com/ProseMirror/prosemirror-history/commit/9bdb3774203d21e3ec14e621eb444524c629b7a3)을 열면 캡처 제외와 rebasing correctness가 별개라는 구현 근거를 얻는다. 상대 입력을 보존할지 먼저 묻는 원리는 도움이 될 수 있지만, 실제 RangeError가 있는 판을 metadata 설정으로 해결했다고 판단하면 멈춰야 한다. 정확 적용 판·step map·선택 bookmark의 재생이 필요하다.

**PN2.** [undoInputRule](https://github.com/ProseMirror/prosemirror-inputrules/blob/40ef4104e086517283081c713727a7f029b565c1/src/inputrules.ts#L105-L107)은 마지막 동작이 input rule이었던 경우에만 사용할 수 있다. 세 점 복원이 목표이면 구현 후보지만 뒤에 문자가 끼었거나 그 정정을 history.redo로 다시 수행해야 하면 이 카드만으로 결정하지 않는다. 나중 편집·redo 경로를 별도 요구로 둔다.

**PT1.** [closeHistory](https://github.com/ProseMirror/prosemirror-history/blob/554d6eedb76704d1db62d85768611ce4b611abd2/src/history.ts#L363-L366)는 제품이 정의한 사용자 행동 단위를 transaction 경계에 맞출 때 유효하다. 같은 사람의 두 입력을 하나의 타이핑 그룹으로 다루는 목표라면 중간 경계가 오히려 보존 조건을 바꾼다. ‘마지막 편집’이 호출·타이핑 그룹·의도된 행위 중 어느 것인지 미정이면 먼저 목적을 정해야 한다.

## 자체 확인 범위

파일 간 source ID 연결과3자리×2변형×2조작의 실제 결과수를 검산했다. 다섯 main package의 npm gitHead 및 source bytes를 GitHub 고정판과 비교했다. 실제 실행 기록18개 중 예측 변형은12개이며 나머지6개는 사후 감도다. core 의존판 차이라는 구체적인 불확실성을 줄이기 위해 역사 lock의4개 감도만 추가했다. 확인된 주장 이상의 추가 시험은 진행하지 않았다. 사람 검토·저자 실행 원로그·원판 동일 공개 CI는 확보하지 못했다.
