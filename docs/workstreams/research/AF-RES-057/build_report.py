"""Assemble the report from the sealed predictions and observed evidence."""
from pathlib import Path
import csv
import json

P = Path(__file__).resolve().parent
BASE = 'https://github.com/'
ORDER = ['YN1', 'YN2', 'YT1', 'PN1', 'PN2', 'PT1']


def main():
    counts = json.loads((P / 'evidence/final-counts.json').read_text())
    cards = {(r['case_id'], r['view']): r for r in csv.DictReader((P / 'cards.csv').open())}
    brief = {
        'YN1': {
            'layer': '자연 · 원요구/연구 정규화 구별',
            'goal': '보호 문구 `this text can not be undone` 유지; 일반 편집은 취소; 원점과 사람 식별 구별',
            'setup': '원작성자 판 미확인. 보조 `13.0.0-94@dd2b8bc6`; `mine `→SKIP 보호문구. opA 원점 집합 `[null]`, opB `[null,SKIP]`; 당시 위치 인자 생성자 사용',
            'prediction': '보조 정상 A만: opA 보호문구, opB `mine `; redo는 둘 다 보호문구+`mine `. 역순 첫 undo는 동률이나 두 번째 undo에서 opB 보호문구 소실. 원요구 동일판은 미확인',
            'output': '[원요구·후속](https://github.com/yjs/yjs/issues/157)에는 제안/권고·수락, 동일 A/B 원출력 없음. [13alpha 재생](streams/yjs/replay/YN1.stdout.json)은 정상·역순·한 원점·단일 보호 삽입 8변형을 기록',
            'verdict': '보조 비보류 예측 일치. 원작성자 판·원사건 A/B 검증은 미확인; D 새 판별 없음',
            'ed': 'A만은 연구 정규화에 조건부; 원요구는 미확인',
            'change': 'E↔D 변경 없음. 원점 집합과 실제 문구/남은 stack 대조는 보조 재생 근거',
            'return_url': 'https://github.com/yjs/yjs/blob/dd2b8bc6c79d98e2fb8d773339d9de7532114eba/src/utils/UndoManager.js#L101-L130',
            'return_use': '해당 판 원점 필터 API/구현 — 어느 변경을 추적할지 정할 때',
            'stop': '모든 변경이 null 원점이거나 실제 판의 인자 형식이 다르면 보호정책을 보장하지 못함; 사람 신원으로 origin을 해석하지 않음'
        },
        'YN2': {
            'layer': '자연 · 본문 기대값 선노출',
            'goal': '복사한 문서에서 삭제한 Hello 복원, 새 작성자의 `123`·기존 World 유지; undo/redo와 삭제 데이터 존속',
            'setup': '`13.0.8@772bb87d`; Hello 삭제→업데이트 복사→123 삽입→private undoStack 대입. opA 두 Doc의 공통 gc=true, opB gc=false',
            'prediction': '둘 다 판별 불가. GC 해제가 삭제 내용 존속에 도움이 될 수 있다는 가설만 기록; private stack 이동·정확 순서/공백·redo 보증은 보류',
            'output': '[원문 및 후속](https://github.com/yjs/yjs/issues/204), [고정 재생](streams/yjs/replay/YN2.stdout.json): opA `123 World`, opB `Hello123 World`; 둘 다 redo `123 World`. 삽입 대조는 둘 다 `123`',
            'verdict': '봉인 보류 유지. 사후 opB 작동을 D 적중으로 소급하지 않음. 원문 `~Hello 123 World`와 실제 공백은 별개',
            'ed': '판별 불가',
            'change': 'E/D 모두 보류. gc=false 후속 설명·보조 출력은 사후 지식이며 사전 선택을 바꾸지 않음',
            'return_url': 'https://github.com/yjs/yjs/blob/772bb87d5cfcc4d9e87ba970731c6aa58f6809bf/README.md#L466-L470',
            'return_use': '해당 판 Y.Doc.gc 절 — 삭제 데이터의 보존 가능성을 확인; #204 후속과 함께 한계 점검',
            'stop': 'GC를 꺼도 private stack의 영속화·다른 문서로의 이동이 공개 계약이 되지 않음; 원자료가 이미 소실되면 단순 상쇄 원리로 복원 불가'
        },
        'YT1': {
            'layer': '시험 · 기대값 후열람',
            'goal': '첫 push `[1,2,3]` 유지, 다음 `[4,5,6]`만 취소; 순서·undo 그룹·redo 구별',
            'setup': '`13.6.28@0a09ff85`; 최초 적격 `testInfiniteCaptureTimeout`; captureTimeout=Number.MAX_VALUE. opA stopCapturing 호출, opB 그 호출만 생략',
            'prediction': 'A만: opA `[1,2,3]`, opB `[]`; redo 둘 다 `[1,2,3,4,5,6]`; 같은 redo 배열이라도 남은 undo 그룹은 다름',
            'output': '[원 assertion L56](https://github.com/yjs/yjs/blob/0a09ff854b2ecd942b3c0f0e741253a214cee1bf/tests/undo-redo.tests.js#L49-L57)은 opA `[1,2,3]`. [A/B·redo 재생](streams/yjs/replay/YT1.stdout.json)은 봉인 예측과 일치. [후속 원실행기](streams/yjs/upstream-verification/verification.json)도 원 opA 시험1개 통과',
            'verdict': '원시험 opA 기대 일치 1자리. opB·redo는 연구 확장; 같은 판 공개 CI는 확보 못함. D의 추가 예측은 없음',
            'ed': 'A만',
            'change': 'E↔D 변경 없음. 후열람 원 assertion은 공통 API가 이미 준 그룹 예측과 일치',
            'return_url': 'https://github.com/yjs/yjs/blob/0a09ff854b2ecd942b3c0f0e741253a214cee1bf/src/utils/UndoManager.js#L321-L343',
            'return_use': 'stopCapturing API — 묶음 경계를 구현할 때; 원시험은 첫 표의 별도 링크',
            'stop': '13.0.8 사후 감도에서는 같은 MAX_VALUE 입력의 경계 호출도 두 push를 합침; 판을 확인하지 않은 API 설명의 일반화 중단'
        },
        'PN1': {
            'layer': '자연 · 명시 보존 속성은 선택 범위',
            'goal': 'U2 삭제의 undo에서 RangeError 없이 선택25..30 복원; U1 계속 입력의 보존은 별도 추론 조건',
            'setup': '실제 판 Latest로 미확인, 시대 기준 history1.0.3. 원사건 입력 미완성. 연구 보조는 U2 삭제·U1 R 삽입, opA addToHistory=false, opB=true',
            'prediction': '원사건 판별 불가. 정상 보조는 A만: opA 삭제분 복원+R 유지, opB R 삭제. 순서 반전은 같은 텍스트이나 남은 undoDepth 0/1 예측',
            'output': '[원요구·수정 논의](https://github.com/ProseMirror/prosemirror/issues/892), [고정 보조 출력](streams/prosemirror/replay/results.json): 정상/역순 예측 일치. [작성자 trace·역사 core 재생](streams/prosemirror/replay/historical/results.json)은 별도 사후 판 비교',
            'verdict': '연구 metadata 대조는 일치; 실제 협업 mapping 결함·원문25..30의 정확 A/B 출력은 미확인. 수정판 대조를 봉인 조작으로 대체하지 않음',
            'ed': '원사건 판별 불가; 보조 정상 A만·역순 텍스트 동률',
            'change': 'E↔D 변경 없음. #892 수정은 selection mapping 근거이며 metadata 개입의 원사건 효과를 증명하지 않음',
            'return_url': 'https://github.com/ProseMirror/prosemirror-history/commit/9bdb3774203d21e3ec14e621eb444524c629b7a3',
            'return_use': '#892 선택 mapping 수정 — 원 RangeError를 조사할 때. 캡처 범위 질문이면 해당 판 addToHistory 절',
            'stop': '원격 수신·rebase·selection·appendTransaction 순서가 다른 입력을 같은 사건으로 합치지 않음; 엄격한 명시적 남길 텍스트 기준에서는 PN1 제외'
        },
        'PN2': {
            'layer': '자연 · 최소 입력 보충',
            'goal': '`...`→`…` 자동변환만 취소하고 입력한 세 점 유지; 후속 x·redo는 연구 경계',
            'setup': '설치판 미확인, 시대 기준 history1.3.0/inputrules1.2.0. opA history.undo, opB undoInputRule; t=1000..1004의 최소 headless 입력 고정',
            'prediction': '즉시 취소 B만: opA 빈 문단, opB `...`; opA redo `…`, opB redo는 미확인. 뒤에 x가 있으면 opB false/`…x`, opA·redo 세부는 보류',
            'output': '[저자 API](https://github.com/ProseMirror/prosemirror-inputrules/blob/40ef4104e086517283081c713727a7f029b565c1/src/inputrules.ts#L105-L107), [후속](https://github.com/ProseMirror/prosemirror/issues/1341), [재생](streams/prosemirror/replay/results.json): opB `...`, 이어 redo=false; x 뒤 opB=false로 `…x` 유지',
            'verdict': '비보류 보조 예측 일치; opB redo/경계 opA는 사전 보류였음. 실제 원작성자 환경·브라우저 실행은 미확인',
            'ed': '즉시 B만; redo 일부·후속 편집 경계 보류',
            'change': 'E↔D 변경 없음. API의 마지막 동작 조건이 선택을 이미 가름. 회계 원리로 redo를 보장하지 않음',
            'return_url': 'https://github.com/ProseMirror/prosemirror-inputrules/blob/40ef4104e086517283081c713727a7f029b565c1/src/inputrules.ts#L105-L107',
            'return_use': 'undoInputRule의 마지막 동작 조건 — 자동변환만 즉시 취소할 때',
            'stop': '다른 입력이 이어졌거나 원래 ellipsis로 redo할 것을 요구하면 같은 API 계약으로 해결됐다고 하지 않음'
        },
        'PT1': {
            'layer': '시험 · 공개 독해 진단',
            'goal': '연구 목표는 a를 남기고 b만 취소; 원시험 목표는 일반 undo 가능. 같은 작성자와 원격 b를 구별',
            'setup': '`history1.5.0@554d6eed`; 최초 enables undo: 빈 문단→a→b. opA 기본 그룹, opB 두 입력 사이 closeHistory 추가',
            'prediction': '연구 목표 B만: opA 빈 문단, opB a; redo 둘 다 ab. 원격 b를 이력에서 제외한 변형에서는 둘 다 b를 남김',
            'output': '[원 assertion L31-38](https://github.com/ProseMirror/prosemirror-history/blob/554d6eedb76704d1db62d85768611ce4b611abd2/test/test-history.ts#L31-L47)은 opA 빈 문단; 이어 별도 redo 시험은 ab. [A/B·원격 변형 재생](streams/prosemirror/replay/results.json)도 예측과 일치. [후속 원실행기](streams/prosemirror/upstream-verification/verification.json)에서 원군1개 통과',
            'verdict': '기대·재생 일치. E의 별개 multilevel 시험에서 기본 그룹 결과가 선노출되어 새 적중은 미확인; 원시험에 opB/redo 확장은 없음',
            'ed': '연구 목표 B만; 원격 b 변형 둘 다',
            'change': 'E↔D 변경 없음. E의 의미적 선노출 때문에 기대 일치를 새로운 발견으로 세지 않음',
            'return_url': 'https://github.com/ProseMirror/prosemirror-history/blob/554d6eedb76704d1db62d85768611ce4b611abd2/src/history.ts#L363-L366',
            'return_use': 'closeHistory API — 사용자가 생각하는 한 번의 편집과 undo 그룹을 맞출 때',
            'stop': '원래 그룹 전체 취소가 목표이면 a까지 사라지는 것은 실패가 아님; 원격 제외 메타데이터와 그룹 경계를 혼동하지 않음'
        }
    }
    first = ['| 자리·자연/시험층 | 사용자 목적·보존 변인 | 제품판·사건열·A/B | 보기·직접 읽은 주소/절 | 봉인한 정상·경계 예측 | 시험 기대 상태·출력 근거 주소 | 일치·충돌·미확인 |',
             '| --- | --- | --- | --- | --- | --- | --- |']
    for case in ORDER:
        b = brief[case]
        for view in ['A', 'E', 'D']:
            card = cards[(case, view)]
            link = f"{view}: [{card['source_id']}]({card['url']}) · {card['location']} · {card['word_count']}단어"
            if view != 'A':
                a = cards[(case, 'A')]
                link = f"공통 [A]({a['url']}) + " + link
            cells = [case + ' · ' + b['layer'], b['goal'], b['setup'], link, b['prediction'], b['output'], b['verdict']]
            first.append('| ' + ' | '.join(x.replace('|', '\\|').replace('\n', ' ') for x in cells) + ' |')
    second = ['| 자리 | 같은 분야 E의 판정 | 외부 D의 판정 | 새 정답·새 오답·동률·보류 | 판단을 바꾼 증거 위치 | 돌려줄 링크와 쓰임 | 일반화가 깨지는 조건 |',
              '| --- | --- | --- | --- | --- | --- | --- |']
    for case in ORDER:
        b = brief[case]
        label = '같은 보류; 새 정답/오답 조건부 평가 해당 없음' if case == 'YN2' else '동일 예측; 원사건 보류와 보조 일치를 분리; D 추가성 해당 없음' if case in ['YN1', 'PN1'] else '동일 예측; 확인 범위에서 일치, D 추가 적중 해당 없음'
        second.append('| ' + ' | '.join([case, b['ed'], b['ed'], label, b['change'], f"[{b['return_use']}]({b['return_url']})", b['stop']]) + ' |')
    sections = r'''
# AF-RES-057 결과와 판정 범위

**판정: PARTIAL — 조사·예측 봉인·보조 실행·저장은 수행했지만, 여섯 자리 모두의 원사건·동일판·같은 두 조작의 공개 출력 검증은 충족하지 못했다.** 같은 분야 E와 외부 원전 D의 사전 선택·undo/redo 상태·정상/경계 예측은 **6/6자리에서 같다**. 상이 예측은 **관측 0/6**, 상이 예측에 조건을 건 D 새 정답·새 오답률의 분모는 **0이므로 해당 없음**이다. 이 수치는 D가 무용하다거나 정확률이 0%라는 뜻이 아니다. [봉인 예측](predictions.csv), [봉인판 자체 검산](evidence/audit-sealed.json), [다른 분담자의 원장 검토](streams/donors/sealed-ledger-review.md).

위 첫 표는 **6자리×3보기=18행**이며 독립된 18사건이 아니다. 둘째 표는 **6행**이다. 보기 A는 공통 API, E는 A+같은 분야 예제, D는 A+지도/회계 원전이다. **opA/opB는 비교 조작**이며 보기 A와 다르다. 빈 문자열은 빈 문단/빈 텍스트, `[]`는 빈 배열이다. 정상·경계의 연구자 보충은 원요구의 실측으로 승격하지 않았다. 정밀 초기값·주체·호출·타이밍·입출력 자료형은 [cases.json](cases.json)과 [events.csv](events.csv), 실제 창과 노출은 [cards.csv](cards.csv)에 있다.

## 연구 순서·표본·분모

실제 시작은 `chore/workspace-foundation@3f4d43b19cd76d56983e6f500eebe7010eb3fa51`, 계획판은 `8036b862…`이다. AF-RES-053의 인계 `94231403…`와 결과 `87a375d7…`에서 예측 사전 고정, 두 보기 동일 예측5/5, 동일판 공개 새 출력0/20논리셀, 창밖 지식의 한계를 인수했다. control의 DONE 표기와 053 HANDOFF의 부분/BLOCKED 판정은 구별했다. 이전 Matplotlib·Vega-Lite·libass·인쇄/지도 라벨을 새 표본으로 재조사하지 않았다. [계약](manifest.json), [인수 기록](evidence/governance-read.json), [SCOPE](SCOPE.md).

예측 봉인 원격 SHA는 **`74dc9f887bc47bc0a92b9a75ea327ffa30aca70b`**, 서버 커밋 시각은 **2026-11-23T03:32:00Z**다. predictions/cards/freeze를 그 SHA에서 다시 읽어 내용 일치를 확인한 뒤 결과 열람을 허용했다. 첫 보류 결과 열람은 ProseMirror **03:32:31.973Z**, Yjs **03:32:32.205236Z**로 기록됐다. 이 순서는 사후 재구성이 아니다. 다만 허용된 E 예제에서 PT1의 의미적 기대 상태를 먼저 본 사실은 봉인 파일에 남아 있다. [원격 재열람](evidence/seal-remote-readback.json), [Yjs 시각](streams/yjs/postseal-first-read.json), [PM 시각](streams/prosemirror/post-read-receipts.json).

자연층은 기간2019-01-01~2025-12-31UTC, PR 제외, 제목 substring undo/redo/history, 작성 시각·번호 오름차순을 유지했다. 단어 검색의 누락을 **본문 열람 전에** 제목 목록과 대조해 Yjs UndoManager, PM undoing/undoInputRule을 회복했다. Yjs는 첫30본문, PM은 해당 기간 후보 전부17본문을 읽었다. PM의 모집 순번18~30은 실제 후보가 없어 빈 행이며, 여섯 연구 자리의 빈 자리와 다르다. [frame.csv](frame.csv)는 자연 모집60순번(실제47+빈13)과 진단2행, 총62행이다.

자연 선정은 Yjs #157/#204, PM #892/#1341이다. #892의 명시 보존 변인은 선택25..30이고 상대방 텍스트 보존은 추론이다. 명시적으로 남길 **텍스트**만 허용하는 엄격 감도에서는 PN1을 제외해 **5/6자리**로 낮아진다. 최초 작성 본문 revision은 네 건 모두 완전히 복원하지 못했다. 현재 회복 가능한 본문과 원문 생성시각·본문 해시를 기록했고, updated_at만으로 본문이 수정됐다고 단정하지 않았다. 본문에서 두 조작의 결과가 이미 드러난 후보와 단순 API 질의는 사유를 남겼다.

진단판은 Yjs v13.6.28(2025-12-17 정식 release), PM history1.5.0(2025-11-13 annotated tag)이다. 시험 경로를 먼저 고정하고 선언순 최초 적격군을 골랐다. Yjs의 초기 정규식이 `.push`를 놓친 오류는 assertion 열람 전 의미 검토로 고쳐 앞선 `testInfiniteCaptureTimeout`을 선정했다. PM은 최초 `enables undo`를 유지했다. 두 원군 모두 원래 redo가 없고, opB/redo 확장은 연구자 입력이다. 같은 파일의 assertion·주석은 기계적으로 가리고 입력만 표시했다. [Yjs 교정](streams/yjs/diagnostic-selection-correction.json), [PM 가림](streams/prosemirror/masking-receipt.json).

E/D의 추가 창은 지도 자리18단어, 회계 자리22단어이며 **6/6쌍에서 단어·도판 수가 같다**. 모두0도판이다. E 코드 행 수는 별도로 기록했으며 D는0이다. 짧은 단어 수 일치는 정보량·코드와 prose의 밀도·읽는 시간을 같게 만들지 않는다. 한 모델이 전체 문헌도 읽었으므로 창만의 인과효과나 사람의 링크 읽기 시간은 평가하지 않았다. YN1-A의 코드 행0 기재 오류는 봉인판을 유지한 채 **실효값1**로 정정했다. [정확 창](evidence/card-windows.json), [정정](evidence/card-metadata-corrections.csv), [사후 변경 원장](evidence/postseal-amendments.json).

## Q1. 누구의 어느 변경을 되돌리고 무엇을 남기는가?

자연 요청은 서로 다른 문제를 가리켰다. YN1은 특정 구간에 들어간 문구를 undo 대상에서 제외하려는 제안이다. YN2는 복사 후 새 문서에 들어간123을 남기며 이전 삭제를 되돌리려는 요청이다. PN1은 동시 입력 중 선택 위치 mapping이 잘못되는 실제 장애이며, PN2는 같은 사람의 입력과 자동 교정을 별도 취소 단위로 나누려는 요청이다. 배열·문단 진단은 이런 원요구를 대표하는 자연 사례가 아니라 고정 시험에서 시작한 별도 층이다. [선정 원문](frame.csv), [사건표](events.csv).

**작성자와 origin은 같은 변수가 아니다.** YN1 연구에서 두 편집을 둘 다 null 원점으로 보내면 두 origin 집합 모두 보호 문구를 추적해 취소할 수 있었다. 같은 사람이라도 별도 origin으로 표시하면 제외할 수 있고, 다른 사람의 변경도 같은 origin에 섞이면 이름만으로 분리되지 않는다. PM의 addToHistory도 특정 거래를 이력에서 제외하는 설정이며 사람 인증을 수행하지 않는다. [YN1 한 원점 대조](streams/yjs/replay/YN1.stdout.json), [PM metadata 대조](streams/prosemirror/replay/results.json).

사건 순서도 보존 목적과 함께 읽어야 한다. PN1 연구 변형의 정상 순서에서는 내 삭제 뒤 상대 삽입을 함께 이력에 넣으면 상대 삽입이 먼저 취소된다. 순서를 반대로 하면 첫 undo 뒤 텍스트가 같아져도 다음에 취소할 상대 사건이 남을 수 있다. 마지막 화면이 같다는 조건만으로 '상대 편집을 계속 보존한다'를 판정하지 않았다. 한 번의 편집이라는 단위도 입력 호출, transaction, capture group 중 무엇인지 명세해야 한다.

반증은 두 원논문에서도 확인했다. Prakash·Knister1992는 선택할 연산·옮겨진 위치·연산 사이 충돌을 각각 다룬다. Yu·André·Ignat2015 §3은 앞 문구가 사라진 뒤 나중에 넣은 부정어만 남으면 의미가 없어질 수 있다고 설명하며, 종속 변경을 함께 숨기는 정책과 사용자 예외를 제안한다. 따라서 모든 상대 글자를 언제나 남기는 것이 유일한 보편 undo 정의는 아니다. 이번에는 각 원요구의 목적을 기준으로 채점하고 논문의 정책을 강제로 대입하지 않았다. [D07](https://web.eecs.umich.edu/~aprakash/papers/prakash-knister-cscw92.pdf), [D08](https://members.loria.fr/CIgnat/files/pdf/YuDAIS15.pdf).

## Q2. 해당 판에서 실제 호출할 두 조작은 무엇인가?

YN1의 당시 공개 개발판 생성자는 원점 집합을 **두 번째 위치 인자**로 받았다. 현재의 options-object 형식을 과거판에 대입하지 않았다. 원문은 설치판을 밝히지 않았고 마지막 정식12.3.3에 같은 API를 확인하지 못했으므로, 시대에 공개된13.0.0-94 재생을 원작성자 실행으로 부르지 않는다. YN2는 본문 명시13.0.8을 사용하되, gc라는 한 공통 bool만 두 Doc 생성에 적용했다. private undoStack 이동 자체는 공개 보장 API가 아니다. YT1은 MAX_VALUE를 고정하고 stopCapturing 한 호출만 바꿨다. [Yjs 판과 생성자](streams/yjs/cases.json).

PN1은 연구 보조에서 동일 원격 표시 transaction의 addToHistory bool만 바꿨다. 실제 원격 전달/rebase 장애의 수정과는 다른 개입이다. PN2는 마지막 history event를 취소하는 undo와 마지막 input rule을 취소하는 undoInputRule을 비교하므로 바뀌는 것은 취소 범위다. PT1은 같은 두 입력 사이 closeHistory만 추가했다. 존재하지 않는 startSkipping/stopSkipping 제안이나 추상 '전체 롤백'을 실행한 조작으로 세지 않았다. [PM 조작·입출력형](streams/prosemirror/cases.json).

Yjs의 읽을 출력은 text.toString()/array.toArray()와 stack 깊이이고 undo/redo는 StackItem 또는 null이다. PM Command는 boolean을 반환하고 dispatch할 수 있으며 결과 EditorState의 문서·선택·undoDepth/redoDepth를 별도로 읽었다. 반환 true와 원하는 문서 상태를 같은 성공으로 처리하지 않았다. PN2의 rule 취소는 true여도 뒤 history.redo는 false였고, 뒤에 x를 입력한 경우 rule 취소부터 false였다. [실제 반환/상태](streams/prosemirror/replay/results.json).

## Q3. 수신 분야 자료가 이미 가르는 경우와 못 가르는 경우

공통 API가 원점 제외(YN1), capture 경계(YT1), 이력 제외(PN1 연구 보조), 마지막 input rule(PN2), closeHistory(PT1)의 핵심 변수를 이미 명시했다. E의 첫 적격 예제도 이 조건을 더 자세히 보여 줄 수 있지만, 이번 봉인에서는 E가 A와 다른 조작 선택을 만들지 않았다. YN2의 그룹 예제는 GC와 private stack 이동의 정확 출력을 가르지 못해 E도 보류했다. API가 존재한다는 사실을 모든 판·외부 상태의 성공 보증으로 확장하지 않았다. [cards.csv](cards.csv), [predictions.csv](predictions.csv).

PM의 일반 history/keymap 배선 예제는 동작 범위·보존을 실제 다루지 않아 예측 봉인 전에 기각했다. 정해 둔 다음 순서인 별개 시험에서 capture/group 예제를 취했다. PN2에는 같은 판 inputrules 전용 시험 파일이 없어 그룹 예제를 사용했다는 한계를 남겼다. PT1의 별개 multilevel 예제를 전체 읽는 과정에서는 a+b 그룹이 빈 문단으로 취소되는 기대 상태가 선노출됐다. 선택 시험의 assertion을 나중에 열었다고 이 자리를 새 적중으로 만들지 않았다. [E 선택 기록](streams/prosemirror/E-selection-log.json).

문서 자체의 반대 근거도 남겼다. Yjs13alpha/13.0.8 README의 원점41 예제는 추적하지 않는다고 쓰면서 출력은 빈 문자열로 표시한다. 더 최신 판의 서술과 대조되는 이 긴장은 선택한 짧은 E 창 밖에서 읽은 것이다. 그 문구 하나를 실제 실행 결과로 사용하지 않았고 별도 원점 재생·고정 구현과 구분했다. [13.0.8 README](https://github.com/yjs/yjs/blob/772bb87d5cfcc4d9e87ba970731c6aa58f6809bf/README.md#L725-L746), [root 재열람 범위](evidence/root-source-rechecks.json).

## Q4. 지도와 회계의 정정에는 실제로 무엇이 남았는가?

표시한 지도18단어는 정정이 과거 흔적을 모두 없애지 않는다는 절이고, 회계22단어는 원거래와 역분개가 함께 원장에 남는다는 절이다. 각각2018년 OSM 역사판과2017년 GnuCash 저자 커밋에도 같은 창이 있다. 원래 사용자들이 그 링크를 읽었거나 채택했다는 근거는 아니다. 같은 문헌의 더 강한 후속 편집 설명을 창 밖에서 읽었다면 그 지식을 짧은 D 카드의 추가 효과로 세지 않았다. [고정 창/역사판](streams/donors/windows.json).

지도 지침의 Clean and dirty reverts는 뒤 편집이 잘못된 데이터를 임시로 고친 것인지, 새 현장 정보를 더한 것인지 구별하라고 요구한다. 실제 Casablanca way284293874에서는 v11의 도로 분류·속도 변경 뒤, 다른 주체가 v12에서 access=no를 없애고 원래 문제 작성자가 v13에서 name:fr를 더했다. v14/v15 정정 뒤 태그·노드 참조는 v10과 같고 name:fr는 없어졌다. 모든 이력 버전은 남았다. v12의 access 제거 효과가 남은 것은 선택적 보존과 단순 기준판 복원 중 어느 이유인지 외형만으로 구별되지 않는다. **'뒤 편집을 모두 남긴다'는 일반화가 깨지지만, 이 사례를 다른 사람의 독립 문장을 지운 동일 사건으로 바꾸지 않았다.** [객체 이력](https://www.openstreetmap.org/way/284293874/history), [정확 버전 대조](streams/donors/map-case-observations.json), [root 독립 재확인](evidence/root-map-recheck.json).

Payap의 DWG 정정은 다른 정상 대조다. 선택 객체 way224498221은 v1의 주차장 통로, v2 삭제, v3 같은 ID의 복원이며 v1/v3 표시 여부·태그·노드 참조가 같다. 삭제/정정 두 changeset의295개 ID 집합은 같지만 상태를 직접 비교한 객체는 이1개다. 그 사이 다른 수정 버전이 없는 clean 복원을 dirty-revert 성공으로 세지 않았다. [원 실행 진술](https://community.openstreetmap.org/t/deletions-around-payap-university-chiang-mai/71883/9), [객체](https://www.openstreetmap.org/way/224498221/history), [범위](streams/donors/payap-case-observations.json).

GnuCash 저자 원장 예제에서는74.99 구매와74.99 환불이 각각 행으로 남으며 Visa 잔액은500.00→574.99→500.00, Clothes는74.99→0.00이다. 금액 효과 상쇄와 기록 삭제는 별개다. 다만 이 매뉴얼은 삭제·수정도 제공하고, 고정 엔진의 reverse는 원거래의 reversed-by 참조 등을 바꾼다. 원기록 존속을 완전 불변 감사 로그로 해석할 수 없다. 또2017년 작성자 보고는 현재 잔액을 맞춰도 다음 대사 시작잔액 문제가 남을 수 있음을 보여 준다. 그 보고에는 수치 원장·정확판이 없으므로 제품 결함을 확정하지 않았다. [환불 예제](https://www.gnucash.org/docs/v5/C/gnucash-guide/cc-enterpay1.html), [고정 Reverse 코드](https://github.com/Gnucash/gnucash/blob/038405b3700aca653f04fb4f2179f22266146262/libgnucash/engine/Transaction.cpp#L2817-L2854), [대사 보고](https://lists.gnucash.org/pipermail/gnucash-user/2017-May/070671.html).

직접 사례는 지도2·회계2의4계보다. 수치 원장 또는 같은 객체 상태를 읽은 것은3/4, 수치 없는 작성자 보고는1/4다. 화면 텍스트 삭제, 내부 연산/식별자 존속, 사용자에게 보이는 감사 기록, 현재 값/잔액, 다음 undo/redo 또는 대사 가능성은 각각 별도 보존 변인이다. 이 구분은 설계 질문으로 유효하지만 제품의 정확 출력을 계산하는 공식은 아니다. [donor 분석과 제한](streams/donors/donor-analysis.md).

## Q5. 결과 전 예측은 어떻게 봉인했고 무엇을 이미 알았는가?

각 자리의 세 보기는 같은 초기 상태·사건열·두 조작을 공유하고, 각 행에 opA/opB의 undo·redo와 정상·경계 예측을 넣었다. Yjs 역순/한 원점/단일 삽입과 PM 역순/후속 x/원격 b는 원사건에 없으면 연구 변형이라고 표시했다. 원문 본문에 이미 있는 실패·기대값도 노출이다. YN2 본문의 근사 기대 문구를 새 예측 정답으로 세지 않았고, PN1의25..30은 사용자 기대이지 새 실행 성공이 아니다.

결론을 맞추려고 donor나 사례를 다시 고르지 않았다. D는 배정대로 자연1=지도, 자연2=회계, Yjs진단=회계/PM진단=지도를 유지했다. 표시 창의 첫 적격 절과 검색·판 선택 규칙은 앞서 저장했다. D의 큰 문헌 전체를 알고 있었던 동일 모델의 판단이라는 한계도 보존했다. root의 D 초안은 교정된 PM E 전달 전에 작성됐지만 독립 사람·독립 모델·완전 차폐 실험이 아니다. [D 준비](evidence/root-D-preparation.json), [분담 검토의 실제 읽은 범위](streams/donors/preoutcome-review-exposure.json).

봉인 뒤에는 예측 파일을 수정하지 않았다. 결과를 보고 추가한 구판 MAX_VALUE와 #892 수정판/역사 core 실행은 사후 감도이며, 그 성공·실패를 기존 예측의 적중/오답으로 재분류하지 않았다. 원래 카드의 단순 코드 행 메타데이터 오류도 별도 정정표로 남겼다. 최종 해시 검산이 봉인10파일의 불변을 확인한다. [freeze](evidence/prediction-freeze.json), [최종 검산](evidence/audit-final.json).

## Q6. 선언된 기대·실행·원작성자 결과는 어디까지 같은가?

엄격한 원진단 기대값은 YT1 opA `[1,2,3]`, PT1 opA 빈 문단을 직접 읽었다. 두 원군에 opB나 redo가 들어 있지는 않다. PT1은 관련 E로 의미가 선노출되어 공개 독해로 남긴다. 같은 판의 공개 CI 통과 로그·아티팩트를 확보하지 못한 것은 테스트가 실패했다는 뜻도, CI가 없었다는 뜻도 아니다. 추가로 두 진단을 원시험 소스·helper·실행기로 각각1개 선택해 로컬에서 통과시켰다. [Yjs 원실행기 영수증](streams/yjs/upstream-verification/verification.json), [PM 원실행기 영수증](streams/prosemirror/upstream-verification/verification.json). 이는 사후 fixture 확인2건이며 앞선26 연구변형·8감도·공개CI와 별도다. Yjs는 원 lock의 lib0.2.99/y-protocols1.0.6, PM은 명시 고정한 현대 buildhelper/core를 썼고 두 실행 모두 Node24.22.3이다. Yjs 등록206시험 중 실제 선택은1개다. 전체206통과로 세지 않는다.

조회한 정확 SHA의 statuses/check-runs/actions 반환 범위를 기록하고 선언된 assertion과 별도로 표시했다. Yjs 조회는 진단13.6.28과 수정7395229/a22b3cd/abf3fab 범위이며 YN1 alpha·YN2 13.0.8 역사 SHA를 직접 조회한 것은 아니다. PM은 진단1.5.0과 수정9bdb377/c8f47ad/f70697e 범위다.

연구자 재생은 봉인된26변형(Yjs14, PM12)을 수행했다. 비보류로 구체화한 상태는 대응 범위에서 일치했다. YN2처럼 보류한 자리까지 맞힌 것으로 만들지 않았고, PN2의 보류했던 redo와 경계 opA 결과도 사후 관측으로만 채웠다. 현재 Node24.22.3·headless harness·고정 패키지 묶음의 관측이며, 실제 원작성자 브라우저/IME/동시 네트워크 실행이 아니다. 버전 gitHead·source provenance, lock·stdout/stderr·종료코드·명령·입력 해시를 함께 보관했다. [Yjs 실행](streams/yjs/replay/), [PM 실행](streams/prosemirror/replay/), [관측 원장](observations.csv).

| 구체 반례 | 직접 관측 | 어떤 일반화를 막는가 |
| --- | --- | --- |
| YN1 역순 첫 undo | 두 조작 모두 보호문구가 보이지만 다음 undo 가능성이 다르고, opB는 결국 보호문구도 없앰 | 첫 화면 일치만으로 상대/보호 편집의 지속 보존을 판정할 수 없음 |
| PN1 역순 | 같은 복원 텍스트 뒤 남은 undoDepth는 opA0/opB1 | 같은 텍스트와 같은 이력/소유 범위는 다름 |
| PN2 rule 취소 | `...`는 복원되지만 history.redo는 false; x를 입력한 뒤 undoInputRule도 false | 역분개의 '반대 거래' 개념으로 redo 가능성을 보증할 수 없음 |
| YT1 구판 감도 | 같은 MAX_VALUE 입력을13.0.8에 적용하면 opA/opB 모두 `[]` | stopCapturing 설명이 모든 역사판/경계에서 성립한다고 일반화할 수 없음 |
| YN2 삭제/삽입 대조 | 삭제는 gc 설정에 따라 Hello 복원 여부가 다르지만 삽입 대조는 둘 다123 | 쉬운 삽입 정상 대조 통과를 삭제 payload/stack 이동 성공으로 대체할 수 없음 |

#892에는 이후 공개된 작성자의 JSON trace와 유지보수자의 축소 회귀 입력도 있었다. 둘을 분리해 역사 core 버전으로 재생했다. 원작성자 trace의1.0.3은 Position22 오류,1.0.4는 `123456789ABCED`·선택6..15이고, 축소 회귀의1.0.3은 Position21 오류,1.0.4는 `123456789ABCDE`·선택6..13이다. 같은 이슈 계보여도 세부 사건열·출력이 다르다. 이 판 비교는 frozen metadata bool 비교가 아니며 원문25..30의 실행을 재현했다고 하지 않는다. [역사 core 결과](streams/prosemirror/replay/historical/results.json).

사후 감도는 Yjs2변형과 PM6변형, 총8변형이다. 전체34변형 실행 중3개 PM 역사 회귀 변형은 의도된 구판 RangeError를 기록했다. 실행 wrapper의 exit0과 모든 사례의 무오류 성공은 다르다. 사후 실행은 버전·의존 묶음이라는 구체적 남은 위험을 확인하는 데만 썼다. 새로운 입력이나 지표를 만든 뒤 원래 예측을 다시 채점하지 않았다.

## Q7. 설계자가 열 마지막 링크는 언제 달라지는가?

이번 여섯 자리에서는 **D가 E와 다른 사전 판단을 만들지 않아**, E보류→D정답, E오답→D정답, D새오답의 조건부 비율은 모두 분모0이다. 보조 재생의 일치와 원문 기대의 일치를 구별해도 이 사실은 바뀌지 않는다. 원자료가 비어 있는 자리를 자동으로 정확한 동률로 판정하지 않았다. YN2의 실제 gc=false 작동도 E와 D가 함께 보류했던 사실을 지우지 않는다.

반환 링크의 선택은 질문의 성격에 따라 달라진다. 특정 문구를 추적에서 제외하려면 해당 판 origin API, 한 번의 취소 단위를 나누려면 stopCapturing/closeHistory, 바로 전 자동교정만 취소하려면 undoInputRule의 전제, 실제 mapping 장애라면 연결 수정과 회귀 입력을 먼저 준다. 외부 원전은 원기록·효과·뒤 변경·다음 undo/redo 중 무엇을 보존하려는지 아직 명세하지 못했을 때 질문을 정교하게 하는 링크로 반환할 수 있다. **이번 자료에서 확인한 것은 서로 다른 보존 변인의 구분이다. 질문의 실제 유용성이나 외부 링크가 더 정확한 구현 선택을 낳는 효과는 측정하지 않았다.** [사례별 반환 카드](return-cards.md).

## 설계 대안의 사용·중단 조건과 관점

| 관점/대안 | 사용할 조건 | 보존할 것과 대가 | 멈추거나 재질문할 조건 |
| --- | --- | --- | --- |
| 문서 작성자 · 그룹 경계 | 사용자가 말한 마지막 편집 단위를 transaction/capture group으로 표현할 수 있음 | 앞 입력 유지와 마지막 입력 취소; 경계를 많이 넣으면 undo 횟수가 늘어남 | 실제 목표가 문장 전체 취소인지 한 키 입력 취소인지 불명확 |
| 공동 편집 상대 · 원점/이력 제외 | 원격·보호 변경을 분리하는 신뢰할 수 있는 provenance가 있음 | 다른 범위의 변경 유지; 추적되지 않은 변경은 같은 undo 이력으로 복원 못함 | origin이 사람과 일치한다고 가정하거나 모두 같은 null에 섞임 |
| 이력 구현자 · 식별자/삭제 자료 | undo할 원자료와 매핑 정보를 보존하고 같은 판의 경계 시험이 있음 | 삭제 내용·변환된 위치·남은 redo를 처리; 저장량과 수명 관리 필요 | private stack을 임의로 이식하거나 이미 GC된 내용까지 복원 가능하다고 추정 |
| 지도 편집자 · 의미적 뒤 변경 검토 | 뒤 기여가 원 오류의 보정인지 독립 추가인지 판별 가능 | 객체 ID·이력과 유효한 현재 내용을 별도로 관리 | 모든 뒤 변경을 무조건 남기거나 지우는 정책으로 단순화 |
| 원장 관리자 · 보상 기록 | 현재 효과와 원기록/정정기록의 존속을 분리해야 함 | 원거래와 정정을 함께 설명; 날짜·대사·연결 상태도 확인 | 수치 상쇄를 텍스트 위치 변환이나 모든 redo 가능성으로 옮김 |

세 대안은 함께 쓸 수 있다. 예컨대 원점으로 추적 대상을 정하고, 그룹 경계로 사용자가 생각하는 편집 단위를 정하고, 별도 감사 기록으로 원행위와 정정행위를 보관할 수 있다. 이것은 **설계 가설**이다. 이번 작업은 제품 구현·DB 구조·UI 또는 하나의 최종 설계를 확정하지 않았다. 특히 감사 로그의 존속을 화면에서 삭제된 문구의 존속과 합치면 사용자의 '되돌리기' 목적이 바뀐다.

## 추가 분석·자료 배당·재현·검토 범위

__COUNTS_BLOCK__

고유 저작 수는 사례 검증 수를 대신하지 않는다. 후보에서 제외한 이슈도 직접 읽은 원저작일 수 있지만 선정 요청4건 배당을 대신하지 않고, 같은 수정의 issue/PR/test/CI는 하나의 사건 계보로 묶는다. PM 기본/E 시험군은 서로 다른 도입 변경이 입증되지 않은 경우 한 suite 계보로 보수화한다. Yjs 진단과 그 MAX_VALUE 수정도 같은 계보다. 입력만 읽은 시험은 엄격 최소수에서 제외하고, 봉인 후 기대값의 별도 취득이 있으면 한 계보로 셀 수 있다. 분담자의 독립 원장 재검산은 원130행을 봤으며, 마지막 원시험 로컬 실행2행은 외부 최소수에서 제외한 뒤 추가했다. 적격112행/고유66저작은 그대로다. [최종 계수](evidence/final-counts.json), [출처 원장](sources.jsonl).

재현 절차는 [Yjs](streams/yjs/replay/reproduce.md), [ProseMirror](streams/prosemirror/replay/reproduce.md)에 있다. 저장된 lock/pin으로 task cache에 의존성을 복원하고 실제 script를 실행한다. ignored cache 경로만 재현 자료로 남기지 않았다. research fixture와 원문 fixture, 사전26과 사후8, 선언된 expectation과 실제 실행 결과를 구분했다. 재현 명령은 미래 실행을 이미 성공한 것으로 표시하지 않는다. 원시험 실행기 추가 확인의 별도 복원 명령은 [Yjs](streams/yjs/upstream-verification/README.md), [PM](streams/prosemirror/upstream-verification/verification.md)에 있다. 과거 stream의 원실행0 기록은 그 시점의 상태이고, 마지막 동반 기록의 로컬2실행이 이후 상태다.

root가 출처·원장·계수·형식을 자체 검토하고, 같은 모델의 다른 분담자가 donor 의미론·봉인 원장·최종 보고서의 지정 범위를 대조했다. 독립 사람/외부 전문가 검토는 미실시다. 다른 분담자가 실제로 읽은 파일과 시각은 review 파일에 남겼다. 정확 원격 결과판의 재열람과 `python -B -m workbench.session check ... --fetch`의 실제 SHA·종료코드는 HANDOFF와 실행 영수증에 있으며, 계약 검사는 원문 사실이나 연구 완전 충족을 자동 인증하지 않는다. [SELF_CHECK](SELF_CHECK.md), [수용 조건](evidence/acceptance-evidence.json).

남은 최소 입력은 최초 본문·실제 설치판·완전 사건열, 그리고 봉인한 두 조작에 대응하는 공개 동일판 출력이다. PN1은 선택25..30의 원사건을 metadata bool 대조와 연결할 근거가 특히 필요하다. PN2는 실제 schema/IME/입력 rule과 timing, YN1은 실제 당시판과 원점 부여, YN2는 원작성자 환경과 private stack의 지원 범위를 확인해야 한다. 새 richer donor 창이나 새 사례를 평가하려면 별도 사전 프로토콜을 만들고 현재 봉인을 소급 수정하지 않는다.

## 불일치·약점 3건

| 불일치·약점 | 영향받는 주장 | 근거 주소·위치 | 다음 최소 조사 | 판정이 바뀔 조건 |
| --- | --- | --- | --- | --- |
| 네 자연 요청의 최초 본문·실제판/완전 사건이 모두 복원되지 않음; PN1의 명시 대상은 선택 범위 | 여섯 자리 전체의 동일판·동일 A/B 출력 검증 및 대표성 | [frame](frame.csv), [cases](cases.json), [#892](https://github.com/ProseMirror/prosemirror/issues/892), [#157](https://github.com/yjs/yjs/issues/157) | 실제 설치판·최초 본문·원사건 trace와 frozen 조작 대응 확보; 명시 텍스트만 요구하는 감도5/6 유지 | 같은 판·입력·주체·두 조작의 출력이 연결되고 엄격 모집 기준을 충족 |
| 원진단은 opA만 있고 opB/redo는 연구 확장; 공개 같은판 CI 미확보; PT1 E 의미 노출 | 새 독립 적중·원작성자 실행·CI 통과 주장 | [YT1원시험](https://github.com/yjs/yjs/blob/0a09ff854b2ecd942b3c0f0e741253a214cee1bf/tests/undo-redo.tests.js#L49-L57), [PT1원시험](https://github.com/ProseMirror/prosemirror-history/blob/554d6eedb76704d1db62d85768611ce4b611abd2/test/test-history.ts#L31-L47), [관측](observations.csv) | 정확 A/B/redo의 공개 fixture·실행 아티팩트 확보; 노출 없는 새 사전 비교 필요 | 선언·수정·CI·저자 실행이 동일 입력판으로 연결되고 새 출력은 예측 후에만 열람 |
| E/D 예측6/6 동일, 짧은18/22단어와 동일 모델 창밖 지식 | D가 새 정확도를 더하거나 사람의 읽기 비용/창의성을 개선한다는 주장 | [봉인](predictions.csv), [창](cards.csv), [방법 검토](streams/donors/method-review.md), [D준비](evidence/root-D-preparation.json) | 더 풍부한 첫 적격 절·노출 분리·새 입력을 새 프로토콜에서 미리 고정 | 서로 다른 사전 예측과 그 차이를 판별하는 같은 조건의 독립 출력이 함께 생김 |
'''
    block = f"""| 분모/조건 | 계획 | 실제와 판정 |
| --- | ---: | --- |
| 자연 원문 모집 | 제품당 첫30 | Yjs30 + PM17 실제 본문; PM빈13순번 보존 |
| 자리/보기 | 6 / 18 | 6 / 18; PN1 엄격 명시 텍스트 감도5 / 15 |
| 출처 행 / 고유 적격 원저작 | >=20저작 | {counts['source_records']}행 / 보수적 {counts['unique_primary_works']}저작; 같은 저작 재취득 중복 제외 |
| 요청·제품API·서로 다른 시험/수정·지도/회계사례·원논문 | 4/4/6/4/2 | {counts['quota_summary']} |
| E/D 단어/도판 예산 일치 | 6쌍 | 6/6; 18또는22단어, 0도판 |
| E/D 동일/상이 예측 | 사전6자리 전체 | 동일6/6, 상이0/6; 조건부 새 정답 분모0 |
| 고정 원진단 expectation | 2자리 | 2/2 opA기대 직접 열람, 결과미노출1/2; opB/redo는원군에없음 |
| 여섯 자리 모두의 공개 동일판 원사건 A/B 검증 | 6 | 0/6 완전 연결; 미확인은 실패율0%와 다름 |
| 봉인 입력 보조 실행 / 사후 감도 | 별도 | 26변형 / 8변형; 오류도 결과로 기록 |
| 후속 원시험 실행기 확인 | 진단별1개 | 로컬2/2 통과; 원 opA만, 신규 예측/공개CI와 별도 |
| 같은 SHA 공개CI 통과 증거 | 해당 시험별 | 확보0; 조회한 정확 SHA 범위와 미확인 사유를 별도 보존 |
"""
    sections = sections.replace('__COUNTS_BLOCK__', block)
    (P / 'RESULT.md').write_text('\n'.join(first) + '\n\n' + '\n'.join(second) + '\n' + sections)
    return_cards = ['# 사례별 반환 링크와 사용 조건', '', '선택은 이번 증거 범위의 반환 제안이다. D의 더 높은 조작 선택 정확도를 입증한 결과가 아니다.', '']
    for case in ORDER:
        b = brief[case]
        return_cards.extend([f"## {case}", '', f"[{b['return_use']}]({b['return_url']}). {b['goal']}. 이번 사전 E/D 판정은 {b['ed']}로 같다. {b['change']}. 중단 조건: {b['stop']}. 지도·회계 원전은 내부 기록·현재 효과·뒤 변경·다음 이력 중 보존 목표를 묻는 참고로만 연결하고, 같은 입력판의 제품 출력 보증으로 바꾸지 않는다.", ''])
    (P / 'return-cards.md').write_text('\n'.join(return_cards))
    print(json.dumps({'result_lines': len((P / 'RESULT.md').read_text().splitlines()), 'first_table_rows': 18, 'second_table_rows': 6}, ensure_ascii=False))


if __name__ == '__main__':
    main()
