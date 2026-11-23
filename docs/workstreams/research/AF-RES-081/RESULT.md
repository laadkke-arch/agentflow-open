# AF-RES-081 · MuseScore 파트 생성과 공통 요소 복사의 선택 상태

## 표 1. 조작과 사전 예상

| 조작ID | 작성자 요구·연구 조건 | 소스판·입력 지문 | 도달 경로 | 시점 | 세 빌드의 사전 예상 | 원문 URL |
| --- | --- | --- | --- | --- | --- | --- |
| E01 | 신고의 선택 음표. 연구 조건은 두 파트의 음과 링크 보존 | 첫 부모 `f4fcf53` · `c88ee55c6cb5…` | 선택한 master C4 → `AddExcerpt` → `createExcerpt` | P1 생성 직후, 명령 종료, 저장·재열기 | P1 flag/목록/mark U 1/0/0, G·L 0/0/0 | [PR #4590](https://github.com/musescore/MuseScore/pull/4590) · [dialog 호출](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/mscore/excerptsdialog.cpp#L505-L528) |
| E02 | 선택하지 않은 연구 대조 | 같은 첫 부모 · 같은 bytes | 비선택 master → P1 생성 | E01과 동일 | U·G·L 0/0/0, 음과 링크 유지 | [createExcerpt](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/excerpt.cpp#L120-L183) |
| E03 | 음표 아래 핑거링까지 선택 표시 정리 | 같은 첫 부모 · 같은 bytes | 핑거링 선택 → `Chord::linkedClone` → `Note` 복사 → child | 생성 직후의 음과 핑거링, 저장·재열기 | 핑거링 U 1/0/–, G·L 0/0/–. 세 P1 음 모두 0/0/0 | [Note copy](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/note.cpp#L559-L620) |
| E04 | 신고의 선택 음표에 독립 P2 편집과 undo 조건 추가 | 같은 첫 부모 · 같은 bytes | P1 생성 → P2 G4→A4 → P1 C4→D4 → 마지막 명령 undo | 생성 직후, 수정들 및 undo, 저장·재열기 | flag는 E01과 동일. 세 빌드 모두 P1 60→62→60, P2 67→69 유지 | [음 높이와 링크](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/edit.cpp#L3414-L3419) |
| E05 | 파트 밖 비링크 복사와 원 선택 유지 대조 | 같은 첫 부모 · 같은 bytes | 선택한 master C4 → `cloneVoice(0,1,…,false,false)` | 삽입 직후, 명령 종료, 저장·재열기 | C1 U·L 1/0/0, G 0/0/0. 원본 모두 1/1/0 | [cloneVoice](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/edit.cpp#L3076-L3103) |
| E06 | 선택하지 않은 음에 sequencer mark를 주입하는 색 대조 | 같은 첫 부모 · 같은 bytes | `setMark(true)` → P1 생성 | 생성 직후의 flag·목록·색, 저장·재열기 | U·G·L 모두 0/0/1로 선택색. 재열기 뒤 0/0/0 | [curColor](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/element.cpp#L334-L366) · [sequencer](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/mscore/seq.cpp#L1506) |

소스 SHA와 tree, fixture의 전체 SHA-256, 원순번, 반증 조건은 [SCOPE.md](SCOPE.md)와 [cases.csv](cases.csv)에 있다. 표의 `목록` 수치 0/1은 해당 객체의 실제 membership이다. 원 목록의 크기는 표 2에 병기했다.

## 표 2. 같은 입력의 재구성 실측

| 입력ID | 빌드·반복 | flag·목록·mark | 링크·음·다른 파트 | 저장·재열기 관측 | 원 출력·종료값 | 미실시·미확인 |
| --- | --- | --- | --- | --- | --- | --- |
| E01 | U 1·2 (01) | P1 1/0/0, 목록 0개, 선택색 | M1↔P1 60, M2↔P2 67, P2 offset 0.75 | 음·링크 유지, P1 0/0/0 | [r1](evidence/runs/01-E01-U/r1/stdout.jsonl) · [r2](evidence/runs/01-E01-U/r2/stdout.jsonl) · exit 0 · 0 | — |
| E01 | G 1·2 (02) | P1 0/0/0, 목록 0개, 기본색 | M1↔P1 60, M2↔P2 67, P2 offset 0.75 | 음·링크 유지, P1 0/0/0 | [r1](evidence/runs/02-E01-G/r1/stdout.jsonl) · [r2](evidence/runs/02-E01-G/r2/stdout.jsonl) · exit 0 · 0 | — |
| E01 | L 1·2 (03) | P1 0/0/0, 목록 0개, 기본색 | M1↔P1 60, M2↔P2 67, P2 offset 0.75 | 음·링크 유지, P1 0/0/0 | [r1](evidence/runs/03-E01-L/r1/stdout.jsonl) · [r2](evidence/runs/03-E01-L/r2/stdout.jsonl) · exit 0 · 0 | — |
| E02 | U 1·2 (04) | P1 0/0/0, 목록 0개, 기본색 | M1↔P1 60, M2↔P2 67, P2 offset 0.75 | 음·링크 유지, P1 0/0/0 | [r1](evidence/runs/04-E02-U/r1/stdout.jsonl) · [r2](evidence/runs/04-E02-U/r2/stdout.jsonl) · exit 0 · 0 | — |
| E02 | G 1·2 (05) | P1 0/0/0, 목록 0개, 기본색 | M1↔P1 60, M2↔P2 67, P2 offset 0.75 | 음·링크 유지, P1 0/0/0 | [r1](evidence/runs/05-E02-G/r1/stdout.jsonl) · [r2](evidence/runs/05-E02-G/r2/stdout.jsonl) · exit 0 · 0 | — |
| E02 | L 1·2 (06) | P1 0/0/0, 목록 0개, 기본색 | M1↔P1 60, M2↔P2 67, P2 offset 0.75 | 음·링크 유지, P1 0/0/0 | [r1](evidence/runs/06-E02-L/r1/stdout.jsonl) · [r2](evidence/runs/06-E02-L/r2/stdout.jsonl) · exit 0 · 0 | — |
| E03 | U 1·2 (07) | P1F 1/0/해당 없음, 목록 0개, P1 음 0/0/0, 선택색 | M1↔P1 60, M2↔P2 67, P2 offset 0.75, 핑거링 1 링크 M1F↔P1F | 음·링크 유지, P1F 0/0/해당 없음 | [r1](evidence/runs/07-E03-U/r1/stdout.jsonl) · [r2](evidence/runs/07-E03-U/r2/stdout.jsonl) · exit 0 · 0 | — |
| E03 | G 1·2 (08) | P1F 0/0/해당 없음, 목록 0개, P1 음 0/0/0, 기본색 | M1↔P1 60, M2↔P2 67, P2 offset 0.75, 핑거링 1 링크 M1F↔P1F | 음·링크 유지, P1F 0/0/해당 없음 | [r1](evidence/runs/08-E03-G/r1/stdout.jsonl) · [r2](evidence/runs/08-E03-G/r2/stdout.jsonl) · exit 0 · 0 | — |
| E03 | L 1·2 (09) | P1F 0/0/해당 없음, 목록 0개, P1 음 0/0/0, 기본색 | M1↔P1 60, M2↔P2 67, P2 offset 0.75, 핑거링 1 링크 M1F↔P1F | 음·링크 유지, P1F 0/0/해당 없음 | [r1](evidence/runs/09-E03-L/r1/stdout.jsonl) · [r2](evidence/runs/09-E03-L/r2/stdout.jsonl) · exit 0 · 0 | — |
| E04 | U 1·2 (10) | P1 1/0/0, 목록 0개, 선택색 | M1↔P1 60→62→60, M2↔P2 67→69, P2 offset 0.75 | 음·링크 유지, P1 0/0/0, undo 없음 | [r1](evidence/runs/10-E04-U/r1/stdout.jsonl) · [r2](evidence/runs/10-E04-U/r2/stdout.jsonl) · exit 0 · 0 | — |
| E04 | G 1·2 (11) | P1 0/0/0, 목록 0개, 기본색 | M1↔P1 60→62→60, M2↔P2 67→69, P2 offset 0.75 | 음·링크 유지, P1 0/0/0, undo 없음 | [r1](evidence/runs/11-E04-G/r1/stdout.jsonl) · [r2](evidence/runs/11-E04-G/r2/stdout.jsonl) · exit 0 · 0 | — |
| E04 | L 1·2 (12) | P1 0/0/0, 목록 0개, 기본색 | M1↔P1 60→62→60, M2↔P2 67→69, P2 offset 0.75 | 음·링크 유지, P1 0/0/0, undo 없음 | [r1](evidence/runs/12-E04-L/r1/stdout.jsonl) · [r2](evidence/runs/12-E04-L/r2/stdout.jsonl) · exit 0 · 0 | — |
| E05 | U 1·2 (13) | C1 1/0/0, 목록 1개, 선택색 | M1 60, P1 공석, M2↔P2 67, C1 60 무링크, P2 offset 0.75 | 음·링크 유지, C1 0/0/0, C1 track 1 | [r1](evidence/runs/13-E05-U/r1/stdout.jsonl) · [r2](evidence/runs/13-E05-U/r2/stdout.jsonl) · exit 0 · 0 | — |
| E05 | G 1·2 (14) | C1 0/0/0, 목록 1개, 기본색 | M1 60, P1 공석, M2↔P2 67, C1 60 무링크, P2 offset 0.75 | 음·링크 유지, C1 0/0/0, C1 track 1 | [r1](evidence/runs/14-E05-G/r1/stdout.jsonl) · [r2](evidence/runs/14-E05-G/r2/stdout.jsonl) · exit 0 · 0 | — |
| E05 | L 1·2 (15) | C1 1/0/0, 목록 1개, 선택색 | M1 60, P1 공석, M2↔P2 67, C1 60 무링크, P2 offset 0.75 | 음·링크 유지, C1 0/0/0, C1 track 1 | [r1](evidence/runs/15-E05-L/r1/stdout.jsonl) · [r2](evidence/runs/15-E05-L/r2/stdout.jsonl) · exit 0 · 0 | — |
| E06 | U 1·2 (16) | P1 0/0/1, 목록 0개, 선택색 | M1↔P1 60, M2↔P2 67, P2 offset 0.75 | 음·링크 유지, P1 0/0/0, 색 #ff000000 | [r1](evidence/runs/16-E06-U/r1/stdout.jsonl) · [r2](evidence/runs/16-E06-U/r2/stdout.jsonl) · exit 0 · 0 | — |
| E06 | G 1·2 (17) | P1 0/0/1, 목록 0개, 선택색 | M1↔P1 60, M2↔P2 67, P2 offset 0.75 | 음·링크 유지, P1 0/0/0, 색 #ff000000 | [r1](evidence/runs/17-E06-G/r1/stdout.jsonl) · [r2](evidence/runs/17-E06-G/r2/stdout.jsonl) · exit 0 · 0 | — |
| E06 | L 1·2 (18) | P1 0/0/1, 목록 0개, 선택색 | M1↔P1 60, M2↔P2 67, P2 offset 0.75 | 음·링크 유지, P1 0/0/0, 색 #ff000000 | [r1](evidence/runs/18-E06-L/r1/stdout.jsonl) · [r2](evidence/runs/18-E06-L/r2/stdout.jsonl) · exit 0 · 0 | — |

매트릭스는 **18/18셀, 36/36회 완료, 36/36회 판독 가능, 미실시 0, 판별불능 0**이다. 두 반복의 정규화 출력이 맞은 셀은 18/18이다. E01–E04의 UI 모델 경계 12셀/24회와 E05–E06의 API 대조 6셀/12회를 별도로 집계했다. 분모는 봉인한 사례와 빌드의 조합이다. [원장·입출력 지문](runs.jsonl)

| 대조 | 같은 결과 | 다른 결과 | 판별불능 |
| --- | ---: | ---: | ---: |
| G 대 L, 전체 6입력 | 5/6 | **1/6 E05** | 0/6 |
| G 대 L, UI 호출 모델 4입력 | 4/4 | 0/4 | 0/4 |
| G 대 L, API 대조 2입력 | 1/2 | **1/2 E05** | 0/2 |
| U 대 G, 6입력 | 2/6 | 4/6 E01·E03·E04·E05 | 0/6 |
| U 대 L, 6입력 | 3/6 | 3/6 E01·E03·E04 | 0/6 |
| 세 빌드의 저장 bytes, 6입력 | 6/6 | 0/6 | 0/6 |

화면 보조 재현은 E01과 같은 악보에서 File → Parts → New All을 쓴 **6/6회**다. P2를 먼저 만드는 매트릭스와 생성 순서가 다르다. master C4의 파란 픽셀은 매회 65개였다. Flute 음표의 파란 픽셀은 U 65·65, G 0·0, L 0·0이었다. Oboe 음표는 매회 0개였다. Flute Inspector는 세 빌드 모두 “Nothing selected”라고 표시했다. [U 화면](evidence/desktop/U-1/flute.png) · [G 화면](evidence/desktop/G-1/flute.png) · [L 화면](evidence/desktop/L-1/flute.png) · [좌표·지문·픽셀](evidence/desktop-pixels.json)

직접 판독 원장 43행 중 보수 합산 **28개 독립 저작·사건**, 그중 악보 분야 밖 **13개**, 별도 실패·무변화 계보 **8개**다. 코드, handbook, build, mtest 소스와 실제 악보는 MuseScore 코드베이스 한 계보로 묶었다. #281441·PR·병합은 한 사건이며, #29407/#11212와 #28584/#32481도 각각 한 계보로 집계했다. [출처 원장](sources.jsonl) · [제외한 열람 시도](evidence/access-attempts.jsonl)

## 표 3. 반환할 원리와 적용 경계

| 반환할 원리·구현 링크 | 차이를 보인 입력 | 같은 결과의 반례 | 계약이 지지하는 적용 범위 | 남은 비용·미확인 |
| --- | --- | --- | --- | --- |
| 새로운 파트에만 선택 비트 초기화. [L 패치](patches/L-excerpt-selection.patch) · [실제 G 병합](https://github.com/musescore/MuseScore/commit/16851045c9e50eafb016c5cf4f2733f974e841bf) | U의 P1에 E01·E04 음표, E03 핑거링 ghost. G·L은 비트를 같이 초기화 | E02는 세 빌드 모두 비선택. E06의 색은 세 빌드 동일 | 이 새 part와 실제 방문한 음·핑거링. P1–master 링크와 별도 P2 링크를 보존 | L의 방문 누락, 파트 생성 중간의 transient flag, layout 비용 미측정 |
| 파트 밖 비링크 복사에서 복제 비트와 선택 등록을 따로 처리. [cloneVoice](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/edit.cpp#L3076-L3103) · [G 패치](patches/G-global-selection.patch) | E05의 C1 G 0/0과 U·L 1/0. M1은 세 빌드에서 1/1 유지 | E05 재열기 때 세 빌드의 C1은 0/0, 저장 bytes 동일. 원 copypaste suite도 같이 통과 | G는 이 복사에서 목록 밖의 선택색을 방지한다. L은 원래 API의 bit 복사를 보존한다. 등록이 필요한 소비자는 새 객체를 명시적으로 선택할 수 있다. [후대 paste 선택 수정](https://github.com/musescore/MuseScore/pull/22352) | E05 매개변수의 직접 메뉴 호출 및 그 비트에 의존하는 2019 소비자 계약 미확인 |
| 공유 음악에 포함된 part 범위, 로컬 선택, 표현용 mark를 각각 확인. [Qt 모델/뷰](https://doc.qt.io/archives/qt-5.15/model-view-programming.html#sharing-selections-among-views) · [Blender 복제](https://github.com/blender/blender/blob/v3.6.0/source/blender/editors/object/object_add.cc#L3762-L3870) | E04의 P1 undo 뒤 P2 편집은 남고, E06은 목록 비어도 선택색 | E04의 음·링크 및 E06의 mark 결과는 U·G·L 동일 | 링크 참여, 편집 전파, 선택 이전과 색 렌더링은 각기 해당 호출 계약이 필요 | 어떤 뷰에서 선택을 공유할지와 playback mark의 유지·표시 정책은 별도 결정 |

연구 상태는 **PARTIAL**이다. 세 빌드의 실행과 자료량은 채웠다. 원 tracker의 첫 revision과 신고 설치물의 지문을 직접 확보하지 못했다.

## Q1. 요구와 판본

ericfont의 2019-01-16 PR 본문은 선택된 요소를 둔 채 파트를 만들면 새 part의 Selection에 항목이 없어도 해당 요소가 파랗게 나온다고 설명한다. 작성자는 같은 이유로 공통 clone에서 SELECTED를 지우자고 제안했고, dmitrio95는 명시적으로 비트를 지우던 기존 `addClone` 예를 들면서 적용 범위에 동의했다. 077의 공식 tracker 부분 캐시는 ericfontainejazz, 표시 날짜 2019-01-08 19:55, Reported version 3.0과 본문에서 함께 본 2.3.2를 기록한다. 시간대와 첫 revision은 미확인이다. 이번에는 공식 URL이 403을 반환했다. E01·E04의 즉시 음표 표시가 신고 조건이다. E03의 자식, 독립 P2, undo 및 저장은 연구 조건이다. [원 tracker](https://musescore.org/en/node/281441) · [원 PR과 댓글](https://github.com/musescore/MuseScore/pull/4590) · [077 캐시 판독](https://github.com/laadkke-arch/agentflow-open/blob/a6338ffd6bc04d45f97e211031bd22aa870fbba0/docs/workstreams/research/AF-RES-077/evidence/ERRATA.md)

2019-03-07 09:53:22 UTC에 병합된 `16851045…`의 부모는 `f4fcf53…`과 `3cfc174…`다. 부모 2의 작성은 2019-01-16 04:57:06 UTC였다. 첫 부모 비교는 `libmscore/element.cpp`의 `_flags` 복사 직후 `setFlag(ElementFlag::SELECTED, false)` 한 줄이다. 세 바이너리를 동일한 첫 부모의 3.1.0 unstable tree로 재구성했다. v3.0.1의 source tag는 신고 뒤인 2019-01-15판이다. v3.0.1, v3.0, v2.3.2, 첫 부모의 tree 및 element.cpp blob은 서로 다르다. v2.3.2는 별도 `_selected` 멤버를 복사하는 코드였다. [병합](https://github.com/musescore/MuseScore/commit/16851045c9e50eafb016c5cf4f2733f974e841bf) · [판본 지문](evidence/upstream-revisions.txt) · [v3.0.1](https://github.com/musescore/MuseScore/releases/tag/v3.0.1)

## Q2. 만나는 경로와 갈라지는 경로

File → Parts는 `MuseScore::startExcerptsDialog`를 연다. Dialog `accept`가 각 `createExcerptClicked`를 호출한다. 새 `Score`와 `AddExcerpt`를 만든 뒤 `Excerpt::createExcerpt`가 staff·track을 대응시키고 `cloneStaves`를 부른다. 이 경로를 E01의 GUI 증거와 모델 실행에서 확인했다. segment의 Chord는 가상 `linkedClone`의 Chord override로 가고, `Chord(const Chord&, true)`가 노트와 하위 요소를 복제하며 Link를 기록한다. 일반 `Element::linkedClone`은 `clone`과 Link를 조합한다. 공통 시작점인 `Element` 복사에서 flag가 들어간다. G는 그 자리에서 지우고 L은 생성 끝의 새 part 방문 객체에서 지운다. [dialog](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/mscore/excerptsdialog.cpp#L505-L566) · [cloneStaves](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/excerpt.cpp#L541-L567) · [Chord override](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/chord.h#L101-L102)

E05의 같은 master 내 `cloneVoice`는 `link=false`인 복사로 `Chord::clone`과 `undoAddCR`을 거쳐 성부 2의 새 음을 넣는다. 이 호출에선 L의 새 part 경계를 지나지 않는다. 외부 조작 중 Tools → Explode의 복수 성부 가지는 `CloneVoice`를 만들고 끝에서 범위를 명시적으로 다시 선택한다. 단일 성부 가지는 selection MIME을 `pasteStaff`로 읽는다. `tst_copypaste`도 MIME 경로의 별도 원시험이다. 따라서 메뉴 이름 대신 실제 분기와 selection 재설정 시점을 확인할 필요가 있다. 이 연구가 직접 호출한 E05의 매개변수는 API층에 있다. [cloneVoice](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/edit.cpp#L3076-L3103) · [Explode](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/cmd.cpp#L2474-L2613)

## Q3. 색의 혼동과 판독

`Selection::add/clear`는 `_el`을 관리한다. 빈 Selection의 `clear`로 목록 밖의 inherited flag를 발견할 수 없다. `curColor`는 printing·drop target을 먼저 처리하고, visible 조건 아래 `selected() || Note::mark()`의 색으로 분기한다. `Note` 복사는 `_mark`도 옮긴다. E06에서 출력된 `0/0/1`은 색만 보면 E01-U와 혼동된다. 실측에서는 객체 포인터, 소속 score와 실제 selection 포인터, `mark`, 렌더 분기 조건을 함께 읽었다. G와 L은 `ElementFlag::SELECTED` 한 종류를 다룬다. [Selection clear/add](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/select.cpp#L295-L337) · [표시 분기](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/element.cpp#L334-L366)

재열기 뒤에는 role/title, tick 0, track과 Chord의 음 순번 0으로 다시 찾았다. 재열린 master의 객체 주소는 같은 프로세스 안의 원 master와 달랐다. 저장 XML의 음과 link marker가 새 객체의 pitch와 link peer를 지지했다. 이번 MSCX에 `selected`·`mark` tag가 없고 모두 재열기 뒤 기본값이었다. `curColor` 판독, 실제 Xvfb 화면과 선택 목록, 직렬화 속성은 각각 별도 영수증이 있다. [저장 경로](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/scorefile.cpp#L640-L652) · [E06 raw](evidence/runs/18-E06-L/r1/stdout.jsonl) · [E06 MSCX](evidence/runs/18-E06-L/r1/roundtrip.mscx)

## Q4. 입력의 판별력

공통 악보에는 마스터 Flute C4와 Oboe G4가 각각 한 staff/voice에 있다. 먼저 Oboe를 P2로 만든 뒤, 봉인한 선택·비선택·child·편집·복사·표시 조건을 마련했다. E02는 선택 입력이 없으면 원판에도 차이가 생기지 않는 대조다. E03은 root chord만 초기화할 경우 놓칠 수 있는 child를 확인한다. E04는 별도 파트 편집이 먼저 들어간 뒤 마지막 pitch command만 undo하는 순서다. E05는 P1 생성 단계를 제거하고 source track 0→같은 악보 track 1을 쓰며, E06은 playback timing을 제거하고 `setMark`를 명시한다. 두 API 대조의 목적과 반증 조건은 실행 전에 저장했다. [봉인 커밋](https://github.com/laadkke-arch/agentflow-open/commit/f8eaddd660557f8070efa762f4cb8e2fbc742375) · [fixture](fixtures/two-parts.mscx)

## Q5. 실행 차이와 분모

유일한 G/L 분기는 E05 세트다. G에서 C1은 unlinked C4, flag 0 및 실제 목록 밖이었다. L에서 C1은 같은 C4와 링크 상태에 flag 1을 유지했고 생성 직후 및 `endCmd` 뒤에도 실제 목록 밖이었다. 시작한 M1의 목록에는 세 빌드 모두 M1만 있었다. 저장 파일의 SHA와 reopen 관측은 E05에서도 세 빌드 동일했다. E04의 M2↔P2는 69에 그대로 있고 P1의 링크 pair만 60으로 되돌아왔다. E02·E06에서 세 빌드 관측 자체가 같았다. [E05 U](evidence/runs/13-E05-U/r1/stdout.jsonl) · [E05 G](evidence/runs/14-E05-G/r1/stdout.jsonl) · [E05 L](evidence/runs/15-E05-L/r1/stdout.jsonl) · [E04 G](evidence/runs/11-E04-G/r1/stdout.jsonl)

## Q6. 결함 판단

| 판정 | 이 실험에서 해당하는 값 | 판단 근거 |
| --- | --- | --- |
| 요구 위반 | U의 E01·E04 P1 음표 | 선택되지 않은 새 파트에서 copied flag가 음표를 칠한다. 신고의 직접 조건을 충족하지 못하며, GUI U에서도 파란 음과 빈 Inspector가 보였다. |
| 예상과 같지만 요구 우열 미확인 | E03의 child 범위와 E05의 외부 복사 차이 | E03은 추가 coverage이고 G/L 둘 다 고쳤다. E05에서 G는 PR의 일반화된 ghost 방지 규칙을 만족한다. L은 파트 밖 API가 이전에 복사하던 비트를 유지한다. 그 비트를 유지하거나 새 객체를 자동 등록해야 하는 2019 소비자 요구는 찾지 못했다. |
| 동일 출력 | G/L E01–E04·E06, 세 빌드 E02·E06 및 6개 저장 결과 | 비교 범위는 기록한 객체와 시점이다. P2 offset·링크, 음, 재열기 및 원 mtest 계약에서 우열을 관측하지 못했다. |

다른 결과였을 경우를 확인하기 위해 유지보수자 댓글에 나온 `addClone`, `cloneVoice`, 일반 paste, Explode를 따라갔다. `addClone`은 root의 selected를 별도로 끈다. `cloneVoice`의 이 분기는 child flag를 옮기면서 목록 등록은 생략했다. E05에서 G가 이 경계의 ghost도 없앴다. L은 같은 범위의 원본 선택과 복제 비트를 보존한다. 원본 선택 자체는 G에서도 보존됐다. flag 보존이 필요한 소비자를 가정하려면 실제 호출 계약이 더 필요하다. 후대의 별개 #22320에서는 paste 직후 변경할 올바른 Note를 반환해 선택하는 수정이 병합됐다. 이 사례는 명시적인 post-copy 선택의 필요를 보여 준다. #33610에서는 사용자가 편집한 영속 라벨의 손실을 별도 회귀로 보고한다. [당시 댓글](https://github.com/musescore/MuseScore/pull/4590#issuecomment-454675696) · [paste 후 선택](https://github.com/musescore/MuseScore/pull/22352) · [표시 라벨 회귀](https://github.com/musescore/MuseScore/issues/33610)

추가 네 관측은 “선택색이면 복사된다”, “여러 대상 선택이면 모두 붙여넣는다”, “음이 공유되면 출력 표현도 유지된다”를 제한한다. Select Similar 목록에서는 paste 무동작이 보고됐고, 다중 staff 대상에는 선택의 top staff만 붙여넣었다. 선택색인 tempo가 범위 복사에서 빠졌고, MIDI part에서는 staccato/swing 표현이 바뀌었다. 별개 4.x spanner 복사 보고는 동일 내용 조작에서 큰 지연을 보였고 Krita의 flatten은 clone의 배치 위치를 잃었다. 이 원전들은 자신의 입력·판본을 주장한다. [선택 목록](https://github.com/musescore/MuseScore/issues/28584) · [대상 범위](https://github.com/musescore/MuseScore/issues/11212) · [tempo](https://github.com/musescore/MuseScore/issues/15590) · [MIDI](https://github.com/musescore/MuseScore/issues/22911) · [spanner 비용](https://github.com/musescore/MuseScore/issues/27399) · [Krita flatten](https://bugs.kde.org/show_bug.cgi?id=437431)

## Q7. 원리를 옮길 수 있는 범위

| 원전 | 옮기는 관계 | 관계가 깨지는 입력 |
| --- | --- | --- |
| TEI P5 §13.1.4.3 및 Versioning Machine | 어떤 witness가 그 위치의 reading에 참여하는지 확인한 뒤 범위를 해석한다. 악보는 현재 대응 track과 실제 link peer를 확인해 적용 대상을 좁힐 수 있다. | lacuna나 겹치는 lemma의 witness를 전체 complement에 넣으면 판독 귀속이 달라진다. marker의 목록으로 과거 음 높이 또는 undo command를 제공할 수 없다. [TEI 고정판](https://tei-c.org/Vault/P5/4.8.0/doc/tei-p5-doc/en/html/TC.html#TCAPWL) · [실제 복수 witness 판독](https://digitalmitford.org/v-machine/samples/faith.html) |
| Blender linked duplicate 및 Inkscape clone | 공유 geometry/shape와 복제 개체의 인스턴스 위치·선택 권한을 나눈다. Blender 선택 이전은 operator가 새 Base를 명시적으로 선택한다. | source에 고정한 색은 Inkscape clone에서 자유롭게 바꿀 수 없다. Krita Flatten은 다른 제품에서도 local 배치가 별도 변환 계약임을 보여 준다. [Blender 코드](https://github.com/blender/blender/blob/v3.6.0/source/blender/editors/object/object_add.cc#L3762-L3870) · [Inkscape](https://inkscape-manuals.readthedocs.io/en/latest/cloning-objects.html) · [Krita 오류](https://bugs.kde.org/show_bug.cgi?id=437431) |
| Qt view selection model | 동일 data model에 view별 selection을 두고, 의도하면 selection model도 공유한다. 원본 음과 표시는 별도 상태로 다룰 수 있다. | 여러 view에서 selection을 일부러 동기화하는 제품은 로컬 초기화만으로 요구를 만족하지 못한다. ProseMirror는 editor state JSON에 선택을 저장할 계약도 제공한다. [Qt](https://doc.qt.io/archives/qt-5.15/model-view-programming.html#sharing-selections-among-views) · [ProseMirror 소스](https://github.com/ProseMirror/prosemirror-state/blob/1.4.3/src/state.ts) |

악보 작성자는 연결된 pitch와 리듬의 전파를, part 담당자는 다른 파트와 독립된 조판과 정확한 현재 선택 표시를, 공통 API 담당자는 복제 객체를 누가 선택 목록에 등록하는지 보존할 근거가 필요하다. Dorico의 layout과 Finale의 속성별 link 규칙은 앞의 두 관계가 동시에 필요할 수 있음을 보여 준다. 링크 하나는 관계의 방향과 후보 구현을 전달한다. E01·E05·E06의 판별 시험을 함께 주면 생성 경계, 일반 복사, 색 혼동 중 어느 것에 근거하는지 선택할 수 있다. [Dorico](https://www.steinberg.help/r/dorico-elements/6.2/en/dorico/topics/program_concepts/program_concepts_layouts_c.html) · [Finale](https://usermanuals.finalemusic.com/FinaleMac/Content/Finale/Linking_Details_for_Linked_Parts.htm)

## Q8. 재검산

| 원 시험 소스 | 확보한 보존 과거 CI | 이번 실측 |
| --- | --- | --- |
| `tst_parts`가 part/자식 추가·삭제·undo 및 MSCX reference를 비교. `tst_links`, `tst_element`, `tst_exchangevoices`, `tst_readwriteundoreset`, `tst_implodeExplode`, `tst_copypaste` 사전 판독 | Travis source는 GCC 4.9, CMake 3.10.1, Qt 5.9.3 archive와 xvfb-run CTest를 명시. 조회한 SHA의 CI 상태는 빈 배열, PR checks의 보존 job 출력 0건 | 재구성 U·G·L에서 같은 7개를 CTest로 실행, **21/21** 타깃 통과. QTest XML의 testcase 결과와 failure/error element도 확인 |
| 기존 reference 및 corpus XML에는 이 조사의 즉시 flag/list/mark 조건이 없다 | 2019 실행 여부 미확인 | 추가 `af_res_081` **36/36**회 및 desktop 보조 **6/6**회 실행. 최초 기동 실패 및 다시 준비한 명령을 함께 보존 |

[원 suite](evidence/original/) · [CI 조회](evidence/original-ci.json) · [빌드 구성](evidence/build/build-info.json) · [재현 명령](reproduce.md)

별도 clean checkout에서 GitHub pin과 G diff를 다시 확인하고 user prefix·세 빌드를 새로 준비했다. 재실행 **36/36**의 정규화 시점별 출력과 저장 SHA가 첫 36회와 같았다. 이 재검증은 최초 매트릭스 분모 밖이다. [독립 작업 폴더 재생](evidence/replay/)

## 판단을 바꿀 다음 확인 세 건

1. **신고판과 처음 보고된 조건의 지문이 비어 있다.** 첫 부모의 현상은 재현했지만 #281441의 최초 본문과 reporter 설치물은 미확인이다. 다음은 #281441의 보존된 원 revision과 3.0·2.3.2 release artifact에 E01의 선택→파트 조작을 적용해 설치 지문, 생성 직후 표시와 편집기 목록을 기록하는 조사다.
2. **G/L의 유일한 차이는 비링크 복사 하위 API에서 관측했다.** 두 실제 성부를 가진 악보에서 Tools → Explode를 실행해 `CloneVoice` 분기와 마지막 범위 재선택 전후의 새 음 flag·목록 및 후속 편집 대상을 함께 확인해야 일반 화면 조작의 계약을 판단할 수 있다.
3. **L의 모든 생성 객체 방문 여부는 미확인이다.** `Note::scanElements`는 tag가 현재 layer에서 유효한 child만 방문한다. 선택된 비기본 tag 핑거링을 가진 악보에서 layer를 바꾸고 part를 만든 뒤 해당 tag를 다시 보여 주는 입력을 써서, 원본 flag 지속과 새 child의 flag·목록·색을 G/L에서 대조할 수 있다. [tag 검사](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/note.cpp#L2229-L2248)
