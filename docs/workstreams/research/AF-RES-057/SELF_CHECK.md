# AF-RES-057 자체 검토

## 판정과 검토 주체

**PARTIAL.** 여섯 자리·18보기의 봉인과 후속 대조, 외부 고유 저작 최소 수와 자료군 배당, 보조 실행과 반례 조사, 파일 구조는 확인했다. 그러나 여섯 자리의 **원사건·동일판·같은 두 조작·redo까지 연결된 공개 출력**은 완성하지 못했다. 이 결손은 26개 연구 변형의 실행이나 66저작의 수로 대신하지 않는다. [결과](RESULT.md), [수용 조건](evidence/acceptance-evidence.json), [비교 계수](evidence/comparison-counts.json).

검토 주체는 root와 동일 모델의 Yjs·ProseMirror·donor 분담자다. root는 인수·프로토콜·모집 원장·봉인 파일·후속 관측·출처 계보·최종 표를 대조하고 지도 객체 이력과 일부 원논문/API/원장 자료를 다시 열었다. 원자료 전부를 root가 혼자 읽었다고 주장하지 않는다. 각 분담자가 직접 열어 읽은 범위와 시각은 sources.jsonl의 reader/opened_UTC/location 및 각 stream 원장에 있다. **독립 사람·외부 전문가 검토, 독립 모델 실험, 사람의 링크 읽기 시간 측정은 미실시**다.

다른 분담자의 실제 검토 범위:

- [donor 봉인 원장 검토](streams/donors/sealed-ledger-review.md): 원장 ID, 18창 단어수, E/D 여섯 예측의 동일성, 노출 기록. 수신 제품의 후속 출력은 당시 읽지 않았다.
- [최종 출처 계보 검토](streams/donors/final-source-audit.md): 세 source ledger 전체와 source-counts. 원시 실행을 새로 한 검토가 아니다.
- [Yjs 최종 검토](streams/yjs/final-review.md): RESULT·observations·계수의 Yjs 주장과 raw before/undo/redo/깊이, 링크 범위. 같은 분담자의 자기 stream 교차 확인이다.
- [ProseMirror 최종 검토](streams/prosemirror/final-review.md): 원사건/metadata 보조/역사 core 감도의 분리, 상태와 명령 반환값, 선노출와 분모.
- [donor 최종 검토](streams/donors/final-review.md): Q4/Q5/Q7, 원전과 화면 텍스트의 다른 보존 목표, 출처·관측 원장의 중복 집계 여부.

검토에서 나온 자연6자리 오기, Yjs CI 조회 범위, YT1 반환 링크 라벨, PN1에 한정되는 삭제 사건열, '질문의 유용성 입증' 표현을 고쳤다. 이 정정은 **봉인 예측·창·사례·사건열의 변경이 아니다**. 고정한 10개 파일의 SHA256은 [freeze](evidence/prediction-freeze.json)와 [최종 구조 검사](evidence/audit-final.json)로 다시 대조한다.

## Q1. 사용자의 되돌리기는 어느 주체의 어느 변경인가?

**주장.** 사용자 목표를 작성자 이름 하나로 표현할 수 없다. YN1은 특정 보호 문구의 추적 제외, YN2는 옮긴 이력에서 삭제분 복원과 새123의 존속, PN1은 선택 위치와 협업 오류, PN2는 자신의 입력과 자동변환의 분리다. 두 진단층의 마지막 입력만 취소 목표는 연구자가 보충한 목표다.

**직접 근거.** [Yjs #157](https://github.com/yjs/yjs/issues/157), [#204](https://github.com/yjs/yjs/issues/204), [PM #892](https://github.com/ProseMirror/prosemirror/issues/892), [#1341](https://github.com/ProseMirror/prosemirror/issues/1341)의 회복 가능한 본문을 모집 순서로 읽었다. [events.csv](events.csv)의 초기값·주체·연산 순서와 [cases.json](cases.json)의 original_request/researcher supplement를 대조했다. YN1의 두 사건을 같은 null 원점에 놓은 실제 [연구 대조](streams/yjs/replay/YN1.stdout.json)에서는 보호 문구를 취소하므로 origin=사람이라는 추론을 배제했다.

**반대 자료/한계.** PN1이 본문에서 명시한 보존 대상은 텍스트가 아니라 선택25..30이다. 최초 authored body revision도 네 건 모두 완전히 회복하지 못했다. [Yu·André·Ignat2015 §3](https://members.loria.fr/CIgnat/files/pdf/YuDAIS15.pdf)는 앞 내용에 종속된 나중 문자열을 함께 숨기는 정책을 보여 준다. 그러므로 모든 뒤 문자를 항상 보존한다는 것을 보편 정답으로 두지 않는다.

**뒤집힐 조건과 최소 입력.** 최초 본문 또는 작성자의 정확 사건열이 현재 해석과 다른 목표를 드러내면 그 자리의 적격성과 목적을 바꿔야 한다. 엄격한 '명시적 남길 텍스트'만 요구하면 PN1을 제외해5/6자리다. 더 늦은 이슈로 조용히 교체하지 않는다. 필요한 첫 입력은 각 자연 요청의 최초 본문·실제 설치판·actor/origin 부여·완전 초기 문서다.

## Q2. 그 판에서 가능한 두 조작은 무엇인가?

**주장.** 각 opA/opB는 실제 호출 또는 설정 차이로 고정했다. 추상적인 전체 롤백을 실행한 척하지 않았다. YN1은 당시의 위치 인자 생성자에 넘긴 origin 집합, YN2는 두 Doc에 공통 적용한 gc, YT1은 stopCapturing 호출, PN1 보조는 addToHistory, PN2는 history.undo/undoInputRule 명령 범위, PT1은 closeHistory다.

**직접 근거.** [alpha UndoManager 생성자](https://github.com/yjs/yjs/blob/dd2b8bc6c79d98e2fb8d773339d9de7532114eba/src/utils/UndoManager.js#L101-L130), [13.0.8 Doc GC](https://github.com/yjs/yjs/blob/772bb87d5cfcc4d9e87ba970731c6aa58f6809bf/README.md#L466-L470), [13.6.28 stopCapturing](https://github.com/yjs/yjs/blob/0a09ff854b2ecd942b3c0f0e741253a214cee1bf/src/utils/UndoManager.js#L321-L343), [inputrules1.2.0](https://github.com/ProseMirror/prosemirror-inputrules/blob/40ef4104e086517283081c713727a7f029b565c1/src/inputrules.ts#L105-L107), [history1.5.0 closeHistory](https://github.com/ProseMirror/prosemirror-history/blob/554d6eedb76704d1db62d85768611ce4b611abd2/src/history.ts#L363-L366)와 고정 script를 대조했다. npm gitHead와 source bytes는 Yjs3판/PM5package에서 맞았다. [Yjs 판 검증](streams/yjs/replay/package-pin-verification.json), [PM 판 검증](streams/prosemirror/replay/source-runtime-check.json).

**반대 자료/한계.** YN1 당시 마지막 정식판과 보조 alpha는 같지 않으며 원작성자 판은 모른다. YN2 private undoStack 복사는 공개 API 보장이 아니다. PN1 metadata 대조는 실제 rebase 장애의 고정 전후 비교와 다르다. PN2는 한 metadata bool 변경이 아니라 취소할 대상 범위가 다른 명령 선택이다. 설치 source가 같아도 현대 Node/전이 의존성과 원작성자의 브라우저가 같지는 않다.

**뒤집힐 조건과 최소 입력.** 실제 역사판에 이 호출이 없거나 구현이 다르면 보조 결과를 원사건으로 이식할 수 없다. YT1을13.0.8에서 재실행했을 때 두 op가 모두 빈 배열을 남긴 [사후 반례](streams/yjs/replay/YT1-sensitivity-1308.stdout.json)가 이미 판 제한을 보여 준다. 원작성자 lock·정확 버전·실행 환경을 확보한 뒤 그 입력을 별도로 재실행해야 한다.

## Q3. 같은 분야 자료가 이미 가르는 경우는 무엇인가?

**주장.** 공통 API가 원점 필터·그룹 경계·마지막 input rule 조건을 이미 가르는 경우 D를 붙여도 추가 선택이 생기지 않았다. E/D가 모두 보류하는 YN2도 그대로 남겼다.

**직접 근거.** [cards.csv](cards.csv)의 실제 절단 창과 [predictions.csv](predictions.csv)의 basis/donor_increment를 대조했다. [Yjs drawing 저자의 예제](https://discuss.yjs.dev/t/infinite-drawing-app/789/4)는 원점·그룹의 작업 맥락을 별도로 제공한다. PM의 E는 본문 API 호출 배선만 있는 예제를 배제하고 실제 작업/시험 예제로 봉인 전에 교정했다.

**반대 자료/한계.** 고른 E 외의 전체 절/시험에서 본 결과도 지식이다. PT1은 multilevel 예제의 기본 그룹 결과가 의미상 먼저 드러났으므로 공개 독해 진단이다. 과거 Yjs README의 'origin41은 추적하지 않음' 설명과 뒤의 빈 문자열 출력 주석은 충돌하며, 현재 README가 이를 다르게 적는 것은 과거 실행 증거가 아니다. [root 재확인](evidence/root-source-rechecks.json), Y-DOC-ALPHA/Y-DOC-1308/Y-DOC-DIAG의 각 고정판 기록.

**뒤집힐 조건과 최소 입력.** 같은 API 창에서 선택할 수 없는 쟁점에 대해 E 또는 D가 서로 다른 상태를 사전에 예측하고, 그 차이를 판별하는 동일 조건의 미노출 기대값이 있으면 추가성 판정을 다시 할 수 있다. 현재 창을 결과 뒤에 늘려 원래 비교로 소급하지 않는다. 새 비교는 새 창/새 입력을 별도 봉인해야 한다.

## Q4. 지도와 회계의 정정에는 무엇이 남는가?

**주장.** 지도에서는 객체 ID·버전 이력과 현재 tag/node 상태를, 회계에서는 원거래·역분개·현재 합계·대사 상태를 나누어 읽어야 한다. 그 구분을 편집기의 보이는 문자·다른 작성자의 작업·undo/redo 이력에 대응시킬 수 있으나 구현 동치가 되지는 않는다.

**직접 근거.** [Casablanca 객체 이력](https://api.openstreetmap.org/api/0.6/way/284293874/history)의 v10~15와 작성자를 비교했고, v15의 tag/node가 v10과 같음을 확인했다. [Payap 사례](https://community.openstreetmap.org/t/deletions-around-payap-university-chiang-mai/71883/9)에서는 way224498221의 삭제/복구와 같은 ID의 v1/v3 상태를 확인했다. [GnuCash 예제 원장](https://www.gnucash.org/docs/v5/C/gnucash-guide/cc-enterpay1.html)의 purchase/refund를 그림과 함께 읽었다. [2017 대사 보고](https://lists.gnucash.org/pipermail/gnucash-user/2017-May/070671.html)는 잔액 회복과 다음 대사의 문제가 서로 다른 주장임을 보여 준다. [donor 관측](streams/donors/donor-analysis.md), [root 객체 재검산](evidence/root-map-recheck.json).

**반대 자료/한계.** Casablanca에서 name:fr를 나중에 넣은 사람은 원 문제 변경의 같은 작성자다. 다른 사람의 독립적인 새 문장을 제거한 반례로 부르지 않는다. v12의 access 부재는 정상 기초 상태에도 없어서 선택적 보존과 단순 초기상태 복귀를 가르지 못한다. Payap은 뒤 편집이 없는 한 객체만 상태를 검증했고295개 모든 객체 상태를 확인하지 않았다. 회계 수치 원장은4사례 중3사례에서만 확보했다. 역분개 코드도 원거래에 reversed-by 연결을 쓰므로 '원기록 존재'는 '모든 필드 불변'과 다르다. [GnuCash 고정 엔진](https://github.com/Gnucash/gnucash/blob/038405b3700aca653f04fb4f2179f22266146262/libgnucash/engine/Transaction.cpp#L2817-L2854).

**뒤집힐 조건과 최소 입력.** 다른 작성자의 독립적인 뒤 기여가 있는 같은 지도 ID를 선택적으로 보존/제거하는 수치 trace, 또는 원장 원거래·역분개·대사 상태가 모두 주어진 사례가 기존 대응을 반박할 수 있다. 현재 사례가 dirty rollback의 일반 해결책 또는 불변 원장을 입증한다고 넓히지 않는다. 설계자의 보존 목표를 묻는 용도로만 쓰는 경우를 명시한다.

## Q5. 결과를 모를 때 누가 무엇을 예측했는가?

**주장.** 원격 봉인 시점 이전의 예측은 여섯 자리×A/E/D18행이며, E/D의8개 주요 결과 필드가6/6 동일하다. 조건부 추가 정답·오답률은 분모0으로 해당 없음이다.

**직접 근거.** 원격 [봉인 커밋](https://github.com/laadkke-arch/agentflow-open/commit/74dc9f887bc47bc0a92b9a75ea327ffa30aca70b)은2026-11-23T03:32:00Z다. cards/predictions/freeze를 같은 SHA에서 다시 읽은 [영수증](evidence/seal-remote-readback.json)이 있다. 보류한 assertion 첫 열람은 PM03:32:31.973Z, Yjs03:32:32.205236Z로 그 뒤다. 각 행은 판정·undo·redo·상대 변경·정상/경계·근거·노출을 함께 저장한다.

**반대 자료/한계.** 시각 순서를 지켰다고 미노출 실험이 되는 것은 아니다. YN2의 실패와 근사 기대값, PN1의 선택 범위, PN2의 기존 undo 방향은 본문에서 보였다. PT1의 답은 E에서 의미상 노출됐다. 한 모델의 기존 지식과 창 밖 자료도 통제하지 못했다. D 작성 순서를 먼저 둔 기록은 독립 참가자 무작위 배정이 아니다. [노출 원장](evidence/root-exposure.json), [D 준비](evidence/root-D-preparation.json), [방법 검토](streams/donors/method-review.md).

**뒤집힐 조건과 최소 입력.** 원격 봉인 내용과 로컬 원장에 차이가 있거나 결과 열람이 실제 봉인보다 앞서면 사전성을 철회해야 한다. 현재10개 고정 hash가 그대로인지를 검사한다. 다른 예측이 생긴 경우에도 유효 출력이 없으면 새 적중은 미확인이다. 답을 본 뒤 선택적 자리 삭제·donor 교체는 하지 않았다.

## Q6. 기대 상태와 실제 상태는 얼마나 일치하는가?

**주장.** 원진단 opA 기대2개는 직접 읽었고 YT1 하나만 기대 미노출 조건을 유지했다. 연구용26변형은 모두 실행을 마쳤고 비보류 상태 예측과 일치했다. 그러나 이를26개의 독립 새 정답이나 원작성자 실행이라고 세지 않는다. 보류한 결과는 보류 그대로다.

**직접 근거.** [YT1 원 assertion](https://github.com/yjs/yjs/blob/0a09ff854b2ecd942b3c0f0e741253a214cee1bf/tests/undo-redo.tests.js#L49-L57), [PT1 원 assertion](https://github.com/ProseMirror/prosemirror-history/blob/554d6eedb76704d1db62d85768611ce4b611abd2/test/test-history.ts#L31-L47), 각 stream의 실행 영수증·잠금·버전 검증·raw JSON을 대조했다. [observations.csv](observations.csv)는 public test/CI/author statement/research replay를 분리한다. YN2 gc=false의 실제 결과는 Hello123 World이며 근사 주석의 공백과 다르다. PN2의 undoInputRule 뒤 history.redo는 false/dispatch0이다.

**반대 자료/한계.** 원격 변경의 소유/ID와 문자열 동등은 다르다. YN1·PN1 역순 연구에서 첫 undo의 텍스트는 같지만 남은 undo 깊이는0/1이었다. [Yjs external updates 원 논의](https://discuss.yjs.dev/t/undomanager-with-external-updates/454)는 복원 내용이 상대에게 새 삽입으로 보일 수 있다는 한계를 남긴다. PN1의 사후 작성자 trace와 유지보수자 축약 입력도 성공판의 텍스트/선택 결과가 다르다. [역사 core 출력](streams/prosemirror/replay/historical/results.json). 별도 사후8실행 중 구판 RangeError3레코드는 실패를 숨기지 않고 보존했다.

**CI 범위.** Yjs 진단/수정4SHA와 PM 진단/수정4SHA에서 보존된 조회 레코드는0개였다. 이를 CI 실패 또는 실제 실행 중인 pending으로 해석하지 않는다. YN1 alpha/YN2 13.0.8의 역사 SHA를 직접 조회한 것으로 확대하지 않는다. 앞선 원장은 당시 공식 원시험 runner0회를 기록했으나, 최종 검토 뒤 원시험 fixture 차이를 확인하기 위해 원소스·helper·실행기로 진단별1개를 로컬 실행했고2/2 통과했다. Yjs는 원 lock, PM은 명시한 현대 buildhelper/core를 쓰며 모두 Node24.22.3이다. [Yjs 동반 기록](streams/yjs/upstream-verification/verification.json), [PM 동반 기록](streams/prosemirror/upstream-verification/verification.json). 원군 opA만 확인했으며26연구변형/8감도와 다른 단위다. 새 사전 적중이나 같은판 공개CI 통과 증거는 아니다.

**뒤집힐 조건과 최소 입력.** 동일한 초기값·주체·판·두 조작·redo를 가진 공개 fixture와 실행 아티팩트, 또는 원작성자의 정확 로그가 보조 실행과 다르면 그 자리 결론을 재검토해야 한다. 새 실행은 [Yjs 재현](streams/yjs/replay/reproduce.md)/[PM 재현](streams/prosemirror/replay/reproduce.md)의 lock으로 구분해 수행한다. 이 명령의 미래 실행을 이미 수행한 것처럼 기록하지 않는다.

## Q7. 설계자에게 돌려줄 마지막 링크가 언제 바뀌는가?

**주장.** 이번 비교에서는 D가 E의 보류를 맞힌 답으로 바꾸거나, 오답을 정정하거나, 새 오답을 만든 사례가 관측되지 않았다. 그 세 전환의 조건부 분모는0이다. 구현 선택은 해당 판 origin/group/input-rule API 또는 실제 mapping 수정 링크가 우선이다. 외부 원전은 원기록·현재 효과·뒤 변경·후속 이력 중 무엇을 보존할지 묻는 참고로 반환할 수 있다.

**직접 근거.** [RESULT 둘째 표](RESULT.md), [comparison-counts](evidence/comparison-counts.json), [return-cards](return-cards.md), [봉인 예측](predictions.csv)을 행별로 대조했다. 순서·metadata·원점이 구체적인 상태 차이를 만들지만 D의 짧은 절에는 그 제품별 호출 계약이 들어 있지 않다.

**반대 자료/한계.** 더 풍부한 지도 절의 '뒤 변경이 오류 보정인지 독립 새 지형인지' 구분은 보존 목표 질문에 더 적합할 수 있다. 그러나 그 절은18단어 D창 밖에 있었고, 지금 결과에 적용해 D의 우위를 소급할 수 없다. 회계의 원거래 보존을 편집 화면의 원문 보존으로 옮기면 사용자가 원하지 않는 문구까지 남기는 새 오답이 될 수 있다. 이것은 위험 가설이며 실제 D 오답 관측과 다르다.

**뒤집힐 조건과 최소 입력.** 사전에 서로 다른 E/D 예측과 그것을 판별하는 미노출 동일판 출력이 함께 나타나면 전환별로 새 정답·새 오답·보류 해소를 셀 수 있다. 지금 얻은 것만으로 사람이 더 빨리 읽거나 더 잘 설계한다는 주장은 하지 않는다. 원저작·제품 API·문서 작성자·상대 편집자·이력 구현자·지도/원장 관리자의 목표 차이는 사용 조건으로 반환한다.

## 수치·형식·저장 검증의 해석

[audit.py](audit.py)는 모집/자리/보기/예측 동일성·source ID·고정 hash·첫18행/둘째6행/마지막3행과 Q1~Q7 존재를 검사한다. 기계 검사는 의미 검토나 연구 완전 충족을 대신하지 않는다. 원130취득 행과 뒤에 추가한 자체 원시험 실행2행을 합한132행 가운데 외부 적격112행을 같은 계보로 합치면66저작이며,20개 배당은 서로 겹치지 않는다. 같은 원전의 HTML/PDF·개정·미러·같은 시험의 줄·실행 로그를 저작 수로 늘리지 않았다. [정확 계수](evidence/final-counts.json), [별도 재검산](streams/donors/final-source-audit.json).

계약 검사는 정확 결과판에서 `python -B -m workbench.session check docs/workstreams/research/AF-RES-057/manifest.json --fetch`로 수행하고 실제 command/SHA/UTC/exit/stdout을 실행 영수증과 HANDOFF에 남긴다. 결과·수용 원장은 원격 고정 SHA에서 다시 연다. HANDOFF는 이 검사가 끝난 뒤 작성하며 마지막 단독 커밋으로 올린다. **원격 파일 저장 성공과 PARTIAL 연구 판정은 동시에 참일 수 있다.**
