# AF-RES-115 자체 검토

판독자는 작성과 실행을 맡은 동일 Codex Cloud 작업자다. 원격 gold 봉인 이전에 전체 E05 JSON과 M60 앞뒤 MSCX, 공식 코드·스키마, 각각의 합성 파일을 읽었다. 원격 봉인 뒤 두 별도 경로의 비교기 결과는 원장을 재계산하는 프로그램으로 대조했다. 사람 또는 독립 에이전트의 판독은 미실시다.

| 질문 | 답 또는 미확인 | 직접 읽은 위치·행 | 결론을 뒤집을 반례와 관측 | 예정·실제·결손 | 판단을 바꿀 관측 |
| --- | --- | --- | --- | --- | --- |
| Q1 | 생성순 60+60을 갖췄다. 원 첨부 적격 3+3 선택은 미달이다. | [frame](frame.csv) E05/E08/E16/M01/M03/M04/M60 · [접근](evidence/attachment-attempts.jsonl) | E26에 직렬화된 SVG가 있었지만 기대 출력이었다. M60은 원글 링크의 선행 fixture를 발견해 보조층에 넣었다. M03의 두 파일은 단일판 추정에 반하는 대조다. | opening 120/120 · 엄격 본 입력 1/6 · 첨부 공석 5 | 첫 미확정 원 링크에서 원 바이트와 재현판·보존 조건을 확인 |
| Q2 | E05의 시작점 사각형은 확인됨, 편집할 text는 미확인. M60 주석과 점프를 분리했다. | [E05 타입](https://github.com/excalidraw/excalidraw/blob/0896892f8ad03f42d1bd8312fe6bd938f6a3f8aa/src/element/types.ts#L39-L153) · [M60 원본 L1478–1504](https://github.com/musescore/MuseScore/blob/ee7506f7a877b79f905fc15b3f0051e468d397de/src/engraving/tests/repeat_data/repeat14.mscx#L1478-L1504) · [M-XSD](sources.jsonl) | 이름/위치가 같아도 e-label/e-copy, 두 TBox 및 MusicXML n-d/m-copy는 서로 다른 occurrence다. | 본 구조 1/6 · 원 링크 보조 1 · original MusicXML 첨부 0 | E05에 빠진 text와 같은 판 파일에서 실제 ID와 편집 선택 확인 |
| Q3 | 동일 4/1,600 한도 및 실제 길이 대조를 재생했다. | [views](views.jsonl) · [교집합·잘림](evidence/verification.json) | E05의 B=C. M60은 412자만으로 B와 C 모두 같은 주석을 골랐다. 합성 CE·CM의 C 단독 개선은 같은 문자 수에서도 남았다. | 본 3/18 · 추가 보조/대조 기본 24 · 동일상한 B/C 18 | 자연 사건에서 동일 길이 C만의 직접 근거 확인 |
| Q4 | 저장 근거와 UI 영향에 다른 값을 줬다. | [gold](truth.csv) E05, M60 · [C++ L153–174](https://github.com/musescore/MuseScore/blob/ee7506f7a877b79f905fc15b3f0051e468d397de/src/engraving/tests/tst_repeat.cpp#L153-L174) | M60의 C++ 기대는 이미 19로 맞으므로 변경 대상은 TBox 저장 주석으로 정정. E05 WYSIWYG의 전제 판이 미상이라 보류. | 독립 원작성자가 명시한 정규화 ID 0/1 · 지원 후보의 런타임 실측 0 | 이전판·이후판에 똑같은 앱 조작과 바뀐/보존 레코드 대조 |
| Q5 | 동명·방향·공유 정의를 따로 시험했다. | [cases](cases.csv) · [누락](evidence/provenance.json) · [#11013](https://github.com/musescore/MuseScore/issues/11013) | Flute 제한 없이 링크만 따라가면 IOb를 지지. 방향을 지우면 start를 head로 승계. 어느 경우에도 실제 기본 비교에 이 확정을 내보내지 않았다. | 본 합성 0/12 · 원 링크 변형 1/2 · 별도 4/4 · XSD 3/3 | 실제 저자가 만든 구조에서 같은 형태의 반례 확보 및 실행 |
| Q6 | 동일 45자리의 두 경로를 대조했다. | [runs](runs.jsonl) · [audit](evidence/replays.json) · [판정](evidence/verification.json) | e-label의 역배열을 B가 봐도 arrow 본체가 없어 끝방향이 미확인. 다중 후보 해결을 가정하면 CE-d의 부당 확정이 나타난다. | 본 3/18 · 본 변형 0/36 · 실제 45×2 · 오확정 0 본 규칙, 사후 누락 별도 | 더 다채로운 자연 문구와 판정 가능한 본표본 재생 |
| Q7 | 해시·명시 선택/후보·방향·판이 깨지는 행을 확인했다. | [실제 NGA·Sakay 및 해시](evidence/provenance.json) · [E08 답변](https://github.com/excalidraw/excalidraw/issues/4578#issuecomment-1010918096) | 가상 parent는 보존 대상인 물리 패널과 별개이며 같은 route/service도 서로 다른 trip 두 개다. | 규격+실데이터 각 분야 2/2 · 적용 서비스의 공동 변경 실측 미실시 | 합법적인 저장 변경 후 어느 요소/출력까지 실제로 바뀌는지 측정 |

### 손 판독 대조

- E05 원문에서 표시 수치를 읽고 붙여 넣는 객체 ID를 따로 추적했다. `/elements/0`만 있고 text는 없다. 원래 B/C 382자의 마지막 완결 JSON은 같은 사각형이고, `E.wysiwyg` 지지 0·보류 2다. `e-label`로 보이는 추가 자료는 원글에 없다. [입력](inputs.jsonl) · [보기](views.jsonl)
- M60 선행·후속의 직접 바이트를 같은 위치로 비교했다. 하나의 변경은 TBox 배열 occurrence이며 C++ assertion의 상수는 이미 19다. B/C가 선택한 `staff:1/TBox:1/Text:1`과 A가 인식한 문자열 구간의 차이가 맞았다. [정확 바이트](evidence/provenance.json) · [판정](runs.jsonl)
- M60-d와 CE-d의 두 후보를 원 배열 순번에서 각각 확인했다. C가 참조하는 연결 하나가 의도를 결정하지 않았다. CM-r은 실제로 IOb를 보며 C가 이름을 반박한다. 독립 후처리 집계, 수작업 판독 및 2회 출력에 차이가 없다. [후처리](tools/verify.py) · [파일 읽기](evidence/replays.json)

자료 규격 읽기와 초기에 확보되지 않은 원 입력의 수를 따로 댔다. 결손은 보류 성공으로 세지 않았다. 첫 3개 표는 원장과 규칙에서 다시 만들고 기록한 실측 영역에만 정확 판정을 적용했다. 미확정 사건·날짜·해시는 원장에 비워 뒀다. 한도 시험과 합성 결과를 데이터 하한 및 자연 원본 충족과 혼동하지 않았다.
