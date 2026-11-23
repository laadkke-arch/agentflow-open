# AF-RES-089 · 시작 계약과 사전 판정

계획판은 `62a80b9f111c695527a8ca87bcb867796d2e96bb`다. GitHub에서 `chore/workspace-foundation`의 처음 조회 ref `f10c81baa98d9bad0407c9af8b4fa91cf9b70f6e`를 읽고, 별도 복제와 후속 ref 조회에서 최신 통합판 `c2709abf8d25163eed75a7553ebcbde966105b55`를 확인해 여기서 `work/research-af-res-089`를 만들었다. 두 통합판의 지침 6개는 동일했다. 최신판의 AGENTS.md, STATE.md, DOT_AUTOMATION.md, RESEARCH_WORKFLOW.md, START_HERE.md, RESEARCH_BRIEF.md, CLOUD_WORKFLOW.md, 협업 규칙과 진행표의 AF-RES-089 및 AF-RES-085 행을 읽었다. 자기 행은 RUNNING, attempt 1이다. 소유 경로는 `docs/workstreams/research/AF-RES-089/`다. [통합판](https://github.com/laadkke-arch/agentflow-open/tree/c2709abf8d25163eed75a7553ebcbde966105b55) · [배정 행](https://github.com/laadkke-arch/agentflow-open/blob/c2709abf8d25163eed75a7553ebcbde966105b55/docs/automation/dot-control.json) · [계약](manifest.json)

연구 의존은 AF-RES-085 하나다. 진행표의 DONE 결과 `7fc799ccbd5e458c94a5e680cae986c74c4a8671`에서 HANDOFF를, 그 결과판 `9ce697f2552133108861cc5504ed64722dfde427`에서 RESULT, cases, reproduce, verify, X1-G-1과 X3-L-1의 app 로그를 열었다. X1 로그 seq 12/14/19에서 voice 2 E4의 원본→복제와 최종 목록을, X3 로그 seq 18/37에서 숨은 Fingering의 tag 제외와 현재 파트의 빈 목록을 확인했다. AF-RES-081의 고정판은 085가 사용한 패치와 Debian 도구를 얻기 위한 경로다. [085 인계](https://github.com/laadkke-arch/agentflow-open/blob/7fc799ccbd5e458c94a5e680cae986c74c4a8671/docs/workstreams/research/AF-RES-085/HANDOFF.md) · [085 결과판](https://github.com/laadkke-arch/agentflow-open/tree/9ce697f2552133108861cc5504ed64722dfde427/docs/workstreams/research/AF-RES-085)

## 실행 자리와 사전 객체 대응

X1/X2 × G/L × 독립 프로세스 2회, 총 8자리와 같은 반복 번호의 4쌍이다. X2 바이트로 수동 RANGE 양성 P와 Esc로 비운 음성 N을 G/L에 각각 한 번, 4자리 추가한다. 매 자리 새 프로필을 쓰고 같은 Xvfb 화면 규격, Qt xcb, 키맵과 master 악보의 포커스를 사용한다. X1/X2는 master Flute의 첫 C4 클릭, Oboe 첫 쉼표 Shift 클릭, Tools → Explode를 거친다. 메인 화면의 악보를 다시 클릭하기 전에 V를 한 번 보낸다. P는 같은 두 보표의 수동 RANGE에서 메뉴 없이 V를 보낸다. N은 같은 몸짓 후 Esc로 비우고 같은 ScoreView 포커스에서 V를 보낸다. [12자리와 악보 지문](cases.csv) · [역사판 V 키맵](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/mscore/data/shortcuts.xml#L772-L775)

대응 키는 `(master/파트 이름, track, tick, 종류, MIDI 음높이)`다. 모든 아래 입력 위치의 tick은 0이다. `M`은 master, `Violin`은 기존 파트이며 staff는 0 기반이다. 한 프로세스 안에서 score/객체 주소, 부모 주소, 링크 주소와 선택 flag·목록·mark를 유지한다. 새 기동 및 재열기에는 대응 키와 링크 상대를 비교한다. 원본에서 이동한 표본의 주소를 복제본 주소로 대체하지 않는다.

| 입력/시점 | 위 보표 master staff 0 | 아래 보표 master staff 1 | 범위 밖 master staff 2와 기존 파트 |
| --- | --- | --- | --- |
| X1 메뉴 전 | track 0 Chord·Note 60, track 1 Chord·Note 64 | track 4 Rest | M track 8 Chord·Note 67 ⇄ Violin track 0 Chord·Note 67 |
| X1 직후 | track 0의 C4 유지. track 1 E4가 cloneVoice의 원본 | track 4에 E4 Chord·Note 삽입. 원 Rest와 track 1 원본은 최종 활성 객체에서 제외 예상 | 같은 링크와 객체값 보호 |
| X2 메뉴 전 / P / N | track 0 Chord 내 Note 60/64 | track 4 Rest | 같은 두 Violin 링크 보호 |
| X2 paste 직후 | track 0에 원 C4+E4 | track 4에 역직렬화한 C4+E4 Chord와 음 | 같은 링크와 객체값 보호 |
| X2 메뉴 종료 | track 0 Chord 내 Note 64 유지 | 삽입된 track 4 Chord 내 Note 60 유지. 두 보표에서 나머지 음 제거 예상 | 같은 링크와 객체값 보호 |

## 편집과 실패 기대의 봉인

- X1은 `cloneVoice(1,4,0,1920,false,true)` 1회, 복제 Note 64의 G/L flag 0/1과 membership 모두 false 예상이다. X2는 `pasteStaff` 1회(staff 1, tick 0, pasteMode), 삽입 음은 모두 flag와 membership false 예상이다. 메뉴 끝에서 두 경로 모두 [staff 0,2) × [tick 0,1920) RANGE를 다시 만들고 주 시험의 예상 Note 두 개를 등록한다. [Explode 분기와 재선택](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/cmd.cpp#L2474-L2613)
- RANGE 생성은 Chord 컨테이너를 통째로 추가하는 대신 그 음과 조건에 맞는 자식을 등록한다. 두 주 입력은 온음표이고 종료 목록은 X1 M:0:Note60 + M:4:Note64, X2 M:0:Note64 + M:4:Note60으로 예상한다. P 목록은 M:0:Note60 + M:0:Note64 + M:4:Rest다. 등록된 Note 및 Rest만 visible true→false로 예상한다. 예상된 목록 밖 Chord의 자체 visible, master Violin과 part의 Chord/Note, 대응 링크, duration과 pitch를 보호한다. 역사판의 VISIBLE은 propertyLink=false다. 초판 입력에는 새로 분리된 음에 대한 파트 피어가 없으므로 기존 Violin은 범위 밖 보존 대조다. [범위 구성](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/select.cpp#L405-L529) · [V 순회](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/cmd.cpp#L3471-L3483) · [VISIBLE 등록](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/property.cpp#L40-L54) · [링크 분기](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/scoreElement.cpp#L250-L278)
- 실제 V 도달은 X11 입력뿐 아니라 `gui_action` 및 `toggle_visible_enter`에서 확인한다. P에서 지정 음의 실값이 변하고 편집 macro 인덱스가 +1, Undo 1회로 편집 직전 인덱스와 객체값 복구를 예상한다. N은 NONE 및 공집합, 인덱스와 값 무변화 예상이다. 주 시험에서 메뉴 종료 시점보다 V 후 인덱스 +1을 예상한다. 실제 값이 변한 자리에서 V의 독립 macro임을 확인한 뒤 한 번만 Ctrl+Z를 보내며 Explode 구조와 주소를 대조한다. Undo는 RANGE의 복원을 가정하지 않는다. 상태마다 실제 목록을 기록한다. [명령 경계](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/cmd.cpp#L146-L191) · [UndoStack](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/undo.cpp#L319-L386)
- 작동하는 두 빌드에 한한 일치 결론은 P/N 유효, 각 메뉴 분기와 V 도달 확인, 두 반복의 실제 변경 키/전후 값/Undo/재열기 대조가 전제다. V가 도달했으나 무변화, 포커스 이탈·액션 미도달, 프로세스/저장/식별 실패를 개별 집계한다. 색이 같아도 피어 효과 또는 Undo가 다르면 실질 불일치다. 개체가 없거나 분모가 0이면 각각 미확인과 산출 불가로 표기한다. 모델·UI·재열기 근거와 두 반복을 보존한다.
- 제외는 081 직접 API, 085의 네 메뉴·픽셀 전수·원 CTest, 도착 보표에 음이 이미 있는 입력, 선택 필터를 변경한 정식 자리다. 실제 사람의 조작 비용은 조사 자료로 확인할 때만 평가한다.

## Q6 탐색 추가 조건

정식 12자리 실행을 마친 뒤 ④의 자기 결론 점검에 한해 아래 탐색을 고정한다. 정식 자리, 입력 바이트와 사전 기준은 ① 그대로다. 탐색 결과가 빠져도 사전 표를 채워 넣지 않는다.

- **F-P / F-X**는 동일한 X1 및 G/L 각 새 프로세스의 Selection Filter에서 Voice 1만 끈다. 수동으로 동일한 두 보표를 범위 선택하면 voice 2의 원 E4만 목록에 남아 V가 바뀔 것을 예상한다. F-X에서는 같은 몸짓 뒤 Tools → Explode가 E4를 아래 보표 voice 1로 옮기므로 같은 범위 좌표에도 목록이 비고 V의 undo macro가 생기지 않을 것을 예상한다. 반증은 V 도달 확인 후 포커스가 동일한데 F-P가 무변화이거나 F-X가 요소를 하나라도 변경하는 경우다.
- **PEER**는 X2 master의 Violin staff 2 첫 G4만 포함하는 수동 RANGE다. G/L 각 새 프로세스에서 master Note 67만 1→0, 링크된 Violin 파트의 Note 67은 1 유지, 링크 두 방향 보존을 예상한다. Q6의 피어 확인으로 쓴다. 이 범위에 우연히 딸려 온 객체는 실제 목록에 기록한다.
- 추가 조건은 탐색에 따른 선택 편향이 가능한 사례다. 각각 두 빌드의 한 번씩을 증거로 남기고, 정식 8+4 및 두 반복의 결론과 분리한다. [선택 필터의 범위 생성](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/select.cpp#L479-L531)
