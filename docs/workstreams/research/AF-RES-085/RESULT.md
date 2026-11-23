## 표 1. 조작과 사전 판정

| 조작 ID | 원 사용자 요구와 연구 조건 | 메뉴·분기 | 편집할 대상 | 입력·버전 SHA | 사전 예상과 반증 조건 | 원문 URL |
| --- | --- | --- | --- | --- | --- | --- |
| X1 | 편곡할 두 성부의 음·길이 보존. 연구는 첫 두 보표의 한 마디를 범위 선택 | Tools → Explode. 다성부 CloneVoice, 1 → 4, tick [0,1920) | 아래 보표 E4. 원 C4와 기존 Violin 피어 유지. RANGE에서 6, 따로 한 번 클릭하면 E4만 온음표 → 2분음표 | [ffc97698e077…](fixtures/x1.mscx) / [f4fcf53ff65c…](manifest.json) | 복제 직후 U/L=1·G=0. 명시 재선택 뒤 같은 목록. RANGE에서 음가 무변화. 분기·대상·재선택 불일치가 반증 | [MuseScore 3 설명](https://musescore.org/en/print/book/export/html/278625) · [역사판 분기](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/cmd.cpp#L2555-L2613) |
| X2 | 단일 성부 C4+E4 화음을 아래·위 한 음씩 보존. X1과 같은 범위의 대조 | Tools → Explode. StaffList → pasteStaff, 목적 staff 1 | 아래 C4. 위 E4와 기존 Violin 피어 유지. RANGE에서 6, 따로 클릭하면 C4만 온음표 → 2분음표 | [763ca31caf1e…](fixtures/x2.mscx) / [f4fcf53ff65c…](manifest.json) | 붙임 직후 U/G/L 모두 0/0/0. 마지막 RANGE에서 C4 1/1/0. 복제 분기 진입 또는 범위 키나 다른 음의 값 변화가 반증 | [MuseScore 3 설명](https://musescore.org/en/print/book/export/html/278625) · [역사판 분기](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/cmd.cpp#L2499-L2554) |
| X3 | 생성 파트의 파란 선택색과 실제 선택을 일치시킬 원 요구. 선택한 비기본 태그 핑거링을 생성 중 숨기는 연구 조건 | -e, shown→hidden, File → Parts → New All → OK, Flute→shown | 새 Flute Fingering 1. V의 실제 목록이 공석이면 무변화. 따로 클릭하면 복제만 visible 1→0. master와 기존 Oboe 값 보존 | [3d21d0f49c8f…](fixtures/layer.mscx) / [f4fcf53ff65c…](manifest.json) | 원본의 숨은 선택 유지가 전제. L은 child callback을 건너뛰고 재표시 때 U/L=1·G=0과 빈 목록. 원본 해제·복사 누락·L callback 또는 V의 값 변화가 반증 | [2019 PR](https://github.com/musescore/MuseScore/pull/4590) · [태그 순회](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/note.cpp#L2229-L2238) |
| X4 | 같은 신고의 표시 계약. 같은 태그와 악보에서 자식이 생성 내내 보이는 대조 | -e, shown 유지, File → Parts → New All → OK, Flute | 같은 Fingering 1과 V, 재클릭 대조 및 다른 파트 보존 조건 | [3d21d0f49c8f…](fixtures/layer.mscx) / [f4fcf53ff65c…](manifest.json) | 복사 U/L=1·G=0. L 방문 후 G/L=0, U=1. 자동 등록·L 미방문·V 값 변화가 반증 | [2019 PR](https://github.com/musescore/MuseScore/pull/4590) · [파트 생성](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/mscore/excerptsdialog.cpp#L505-L562) |

## 표 2. 정식 GUI 24자리

| 조작·빌드·반복 | 실제 분기 | 직후와 메뉴 종료의 flag·목록·mark | 후속 편집 대상·값 | undo·재열기 | 로그·화면 주소 | 미확인 |
| --- | --- | --- | --- | --- | --- | --- |
| X1-U-1 | cloneVoice 1→4 ×1 | 1/0/0 → 1/1/0 (RANGE 2) · 파랑 57px | 목록 E4/C4, 6 무변화. -R tr4 E4 1920→960 | -R 1920 복구 · 주 저장 재열기 0/0/0 | [앱](evidence/gui/X1-U-1/app.jsonl) · [화면](evidence/gui/X1-U-1/03-menu-ended.png) · [재열기](evidence/gui/X1-U-1/reopen.jsonl) | rest 경고의 다른 입력 영향 |
| X1-U-2 | cloneVoice 1→4 ×1 | 1/0/0 → 1/1/0 (RANGE 2) · 파랑 57px | 목록 E4/C4, 6 무변화. -R tr4 E4 1920→960 | -R 1920 복구 · 주 저장 재열기 0/0/0 | [앱](evidence/gui/X1-U-2/app.jsonl) · [화면](evidence/gui/X1-U-2/03-menu-ended.png) · [재열기](evidence/gui/X1-U-2/reopen.jsonl) | rest 경고의 다른 입력 영향 |
| X1-G-1 | cloneVoice 1→4 ×1 | 0/0/0 → 1/1/0 (RANGE 2) · 파랑 57px | 목록 E4/C4, 6 무변화. -R tr4 E4 1920→960 | -R 1920 복구 · 주 저장 재열기 0/0/0 | [앱](evidence/gui/X1-G-1/app.jsonl) · [화면](evidence/gui/X1-G-1/03-menu-ended.png) · [재열기](evidence/gui/X1-G-1/reopen.jsonl) | rest 경고의 다른 입력 영향 |
| X1-G-2 | cloneVoice 1→4 ×1 | 0/0/0 → 1/1/0 (RANGE 2) · 파랑 57px | 목록 E4/C4, 6 무변화. -R tr4 E4 1920→960 | -R 1920 복구 · 주 저장 재열기 0/0/0 | [앱](evidence/gui/X1-G-2/app.jsonl) · [화면](evidence/gui/X1-G-2/03-menu-ended.png) · [재열기](evidence/gui/X1-G-2/reopen.jsonl) | rest 경고의 다른 입력 영향 |
| X1-L-1 | cloneVoice 1→4 ×1 | 1/0/0 → 1/1/0 (RANGE 2) · 파랑 57px | 목록 E4/C4, 6 무변화. -R tr4 E4 1920→960 | -R 1920 복구 · 주 저장 재열기 0/0/0 | [앱](evidence/gui/X1-L-1/app.jsonl) · [화면](evidence/gui/X1-L-1/03-menu-ended.png) · [재열기](evidence/gui/X1-L-1/reopen.jsonl) | rest 경고의 다른 입력 영향 |
| X1-L-2 | cloneVoice 1→4 ×1 | 1/0/0 → 1/1/0 (RANGE 2) · 파랑 57px | 목록 E4/C4, 6 무변화. -R tr4 E4 1920→960 | -R 1920 복구 · 주 저장 재열기 0/0/0 | [앱](evidence/gui/X1-L-2/app.jsonl) · [화면](evidence/gui/X1-L-2/03-menu-ended.png) · [재열기](evidence/gui/X1-L-2/reopen.jsonl) | rest 경고의 다른 입력 영향 |
| X2-U-1 | pasteStaff staff 1 ×1 | 0/0/0 → 1/1/0 (RANGE 2) · 파랑 56px | 목록 C4/E4, 6 무변화. -R tr4 C4 1920→960 | -R 1920 복구 · 주 저장 재열기 0/0/0 | [앱](evidence/gui/X2-U-1/app.jsonl) · [화면](evidence/gui/X2-U-1/03-menu-ended.png) · [재열기](evidence/gui/X2-U-1/reopen.jsonl) | — |
| X2-U-2 | pasteStaff staff 1 ×1 | 0/0/0 → 1/1/0 (RANGE 2) · 파랑 56px | 목록 C4/E4, 6 무변화. -R tr4 C4 1920→960 | -R 1920 복구 · 주 저장 재열기 0/0/0 | [앱](evidence/gui/X2-U-2/app.jsonl) · [화면](evidence/gui/X2-U-2/03-menu-ended.png) · [재열기](evidence/gui/X2-U-2/reopen.jsonl) | — |
| X2-G-1 | pasteStaff staff 1 ×1 | 0/0/0 → 1/1/0 (RANGE 2) · 파랑 56px | 목록 C4/E4, 6 무변화. -R tr4 C4 1920→960 | -R 1920 복구 · 주 저장 재열기 0/0/0 | [앱](evidence/gui/X2-G-1/app.jsonl) · [화면](evidence/gui/X2-G-1/03-menu-ended.png) · [재열기](evidence/gui/X2-G-1/reopen.jsonl) | — |
| X2-G-2 | pasteStaff staff 1 ×1 | 0/0/0 → 1/1/0 (RANGE 2) · 파랑 56px | 목록 C4/E4, 6 무변화. -R tr4 C4 1920→960 | -R 1920 복구 · 주 저장 재열기 0/0/0 | [앱](evidence/gui/X2-G-2/app.jsonl) · [화면](evidence/gui/X2-G-2/03-menu-ended.png) · [재열기](evidence/gui/X2-G-2/reopen.jsonl) | — |
| X2-L-1 | pasteStaff staff 1 ×1 | 0/0/0 → 1/1/0 (RANGE 2) · 파랑 56px | 목록 C4/E4, 6 무변화. -R tr4 C4 1920→960 | -R 1920 복구 · 주 저장 재열기 0/0/0 | [앱](evidence/gui/X2-L-1/app.jsonl) · [화면](evidence/gui/X2-L-1/03-menu-ended.png) · [재열기](evidence/gui/X2-L-1/reopen.jsonl) | — |
| X2-L-2 | pasteStaff staff 1 ×1 | 0/0/0 → 1/1/0 (RANGE 2) · 파랑 56px | 목록 C4/E4, 6 무변화. -R tr4 C4 1920→960 | -R 1920 복구 · 주 저장 재열기 0/0/0 | [앱](evidence/gui/X2-L-2/app.jsonl) · [화면](evidence/gui/X2-L-2/03-menu-ended.png) · [재열기](evidence/gui/X2-L-2/reopen.jsonl) | — |
| X3-U-1 | Flute·추가 Oboe ×2, hidden→shown | 1/0/– → 1/0/– (NONE 0) · 파랑 8px | 목록 공석, V 무변화. -R Flute 자식 visible 1→0 | -R visible=1 복구 · 주 저장 재열기 0/0/– | [앱](evidence/gui/X3-U-1/app.jsonl) · [화면](evidence/gui/X3-U-1/04-shown.png) · [재열기](evidence/gui/X3-U-1/reopen.jsonl) | — |
| X3-U-2 | Flute·추가 Oboe ×2, hidden→shown | 1/0/– → 1/0/– (NONE 0) · 파랑 8px | 목록 공석, V 무변화. -R Flute 자식 visible 1→0 | -R visible=1 복구 · 주 저장 재열기 0/0/– | [앱](evidence/gui/X3-U-2/app.jsonl) · [화면](evidence/gui/X3-U-2/04-shown.png) · [재열기](evidence/gui/X3-U-2/reopen.jsonl) | — |
| X3-G-1 | Flute·추가 Oboe ×2, hidden→shown | 0/0/– → 0/0/– (NONE 0) · 파랑 0px | 목록 공석, V 무변화. -R Flute 자식 visible 1→0 | -R visible=1 복구 · 주 저장 재열기 0/0/– | [앱](evidence/gui/X3-G-1/app.jsonl) · [화면](evidence/gui/X3-G-1/04-shown.png) · [재열기](evidence/gui/X3-G-1/reopen.jsonl) | — |
| X3-G-2 | Flute·추가 Oboe ×2, hidden→shown | 0/0/– → 0/0/– (NONE 0) · 파랑 0px | 목록 공석, V 무변화. -R Flute 자식 visible 1→0 | -R visible=1 복구 · 주 저장 재열기 0/0/– | [앱](evidence/gui/X3-G-2/app.jsonl) · [화면](evidence/gui/X3-G-2/04-shown.png) · [재열기](evidence/gui/X3-G-2/reopen.jsonl) | — |
| X3-L-1 | Flute·추가 Oboe ×2, hidden→shown | 1/0/– → 1/0/– (NONE 0) · L callback 0 · 파랑 8px | 목록 공석, V 무변화. -R Flute 자식 visible 1→0 | -R visible=1 복구 · 주 저장 재열기 0/0/– | [앱](evidence/gui/X3-L-1/app.jsonl) · [화면](evidence/gui/X3-L-1/04-shown.png) · [재열기](evidence/gui/X3-L-1/reopen.jsonl) | — |
| X3-L-2 | Flute·추가 Oboe ×2, hidden→shown | 1/0/– → 1/0/– (NONE 0) · L callback 0 · 파랑 8px | 목록 공석, V 무변화. -R Flute 자식 visible 1→0 | -R visible=1 복구 · 주 저장 재열기 0/0/– | [앱](evidence/gui/X3-L-2/app.jsonl) · [화면](evidence/gui/X3-L-2/04-shown.png) · [재열기](evidence/gui/X3-L-2/reopen.jsonl) | — |
| X4-U-1 | Flute·추가 Oboe ×2, shown 유지 | 1/0/– → 1/0/– (NONE 0) · 파랑 8px | 목록 공석, V 무변화. -R Flute 자식 visible 1→0 | -R visible=1 복구 · 주 저장 재열기 0/0/– | [앱](evidence/gui/X4-U-1/app.jsonl) · [화면](evidence/gui/X4-U-1/04-shown.png) · [재열기](evidence/gui/X4-U-1/reopen.jsonl) | — |
| X4-U-2 | Flute·추가 Oboe ×2, shown 유지 | 1/0/– → 1/0/– (NONE 0) · 파랑 8px | 목록 공석, V 무변화. -R Flute 자식 visible 1→0 | -R visible=1 복구 · 주 저장 재열기 0/0/– | [앱](evidence/gui/X4-U-2/app.jsonl) · [화면](evidence/gui/X4-U-2/04-shown.png) · [재열기](evidence/gui/X4-U-2/reopen.jsonl) | — |
| X4-G-1 | Flute·추가 Oboe ×2, shown 유지 | 0/0/– → 0/0/– (NONE 0) · 파랑 0px | 목록 공석, V 무변화. -R Flute 자식 visible 1→0 | -R visible=1 복구 · 주 저장 재열기 0/0/– | [앱](evidence/gui/X4-G-1/app.jsonl) · [화면](evidence/gui/X4-G-1/04-shown.png) · [재열기](evidence/gui/X4-G-1/reopen.jsonl) | — |
| X4-G-2 | Flute·추가 Oboe ×2, shown 유지 | 0/0/– → 0/0/– (NONE 0) · 파랑 0px | 목록 공석, V 무변화. -R Flute 자식 visible 1→0 | -R visible=1 복구 · 주 저장 재열기 0/0/– | [앱](evidence/gui/X4-G-2/app.jsonl) · [화면](evidence/gui/X4-G-2/04-shown.png) · [재열기](evidence/gui/X4-G-2/reopen.jsonl) | — |
| X4-L-1 | Flute·추가 Oboe ×2, shown 유지 | 1/0/– → 0/0/– (NONE 0) · L callback 1 · 파랑 0px | 목록 공석, V 무변화. -R Flute 자식 visible 1→0 | -R visible=1 복구 · 주 저장 재열기 0/0/– | [앱](evidence/gui/X4-L-1/app.jsonl) · [화면](evidence/gui/X4-L-1/04-shown.png) · [재열기](evidence/gui/X4-L-1/reopen.jsonl) | — |
| X4-L-2 | Flute·추가 Oboe ×2, shown 유지 | 1/0/– → 0/0/– (NONE 0) · L callback 1 · 파랑 0px | 목록 공석, V 무변화. -R Flute 자식 visible 1→0 | -R visible=1 복구 · 주 저장 재열기 0/0/– | [앱](evidence/gui/X4-L-2/app.jsonl) · [화면](evidence/gui/X4-L-2/04-shown.png) · [재열기](evidence/gui/X4-L-2/reopen.jsonl) | — |

## 표 3. 사용자에게 반환할 링크

| 사용자 목적 | G·L·유보 | 차이가 생긴 시점 | 같은 결과의 반례 | 반환할 구현·시험 주소 | 추가 확인 |
| --- | --- | --- | --- | --- | --- |
| 파트의 파란 표시가 실제 선택처럼 보이는 문제를 없애기 | **G**, X3의 숨은 자식까지 초기화해야 할 때 | G는 복제 시 끈다. L은 X3에서 tag gate를 지나지 못해 재표시 뒤에도 파랗다 | X4는 자식 방문 뒤 G/L 모두 기본색. E06의 파란색은 mark가 원인이어서 G/L 모두 동일 | [G, Element 복사 수정](https://github.com/musescore/MuseScore/commit/16851045c9e50eafb016c5cf4f2733f974e841bf) · [X3 G/L 판별 시험](evidence/verify.json) | 다른 태그 자식에서 G/L 각 2회, 4회와 복제·표시·목록 세 시점 |
| 적용 범위를 새 파트로 제한하고 싶음 | **L 조건부**, 방문한 자식에서 확인 | X4에서 layout 뒤 L callback이 flag 1→0 | X3의 같은 타입은 숨겨져 초기화가 빠진다. 화면 필터와 초기화 방문을 분리한 안을 비교할 수 있다 | [L, 새 Excerpt 순회](https://github.com/laadkke-arch/agentflow-open/blob/60d0c8a1c1ea20b4d5f9cf47ae9a24a627012cfc/docs/workstreams/research/AF-RES-081/patches/L-excerpt-selection.patch) · [X4 방문 실측](evidence/gui/X4-L-1/app.jsonl) | X3/X4 × 보강한 L 및 G × 2회, 8회. skip/callback·피어·다른 파트 값을 비교 |
| 다음 명령이 엉뚱한 객체를 고치는 문제 | **유보**. 측정한 경로의 편집 대상은 G/L에서 동일 | 편집 시 실제 목록과 단일 선택 조건이 결정. X3의 화면 차이는 V까지 남았으나 값은 동일 | 분리 클릭 대조는 24회 모두 목적지 한 객체만 수정. 일반 Paste 뒤 duration 회귀가 보고된 후대 사례가 있다 | [선택 소비자](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/select.cpp#L140-L159) · [후속 편집 검산](fixtures/verify.py) | 범위 지원 편집을 X1/X2 × G/L × 2회, 8회. 바뀐 식별자와 값, undo 확인 |
| 복사 시에는 차이가 있으나 메뉴 종료 전에 사라짐 | **유보**. 공통 복사 API의 다른 소비자를 따로 봄 | X1에서 마지막 RANGE 선택이 목적 E4를 등록 | X2는 XML 붙임부터 동일. E05 직접 호출에는 마지막 RANGE 생성이 없고 비트 차이가 명령 종료까지 남았다 | [Explode의 마지막 재선택](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/cmd.cpp#L2609-L2613) · [X1 및 E05 판별](evidence/verify.json) | 재선택이 없거나 선택 필터가 복제음을 제외하는 GUI 경로에서 G/L 각 2회, 4회. 메뉴 전후와 편집 값 검사 |
| 화면은 다르고 재열면 같아짐 | **G**를 세션 중 표시 수정으로 안내. 파일 보존 기준에서는 **유보** | X3의 비트는 주 경로 저장 후 열린 세션에도 남고 새 프로세스 읽기에서 꺼진다 | X1은 저장 이전에도 같았다. GIMP XCF는 픽셀 선택 자체를 파일에 저장한다 | [역사판 selected 읽기 처리](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/element.cpp#L590-L596) · [X3 L 재열기 실측](evidence/gui/X3-L-1/reopen.jsonl) | 저장 전·후 각 상태와 재열기 1회씩을 새 입력 G/L 두 번씩, 4회 비교 |

**분모.** 정식 GUI 24/24, 메뉴와 후속 키 도달 24/24, 편집 전후 모델 판독 24/24, 미완료 자리 0/24. 주 후속 키가 문서 값을 바꾼 경우 0/24. 별도 한 번 클릭 뒤 목표 값 변경 및 undo 복원 24/24. G/L 비교는 조작별 두 반복의 8/8짝과 U 기준의 8/8세트다. G/L 복제 직후 flag 차이 6/8, 다음 키 시점의 화면 차이 2/8(X3), 다음 편집 결과 차이 0/8. 동일 입력의 저장 bytes는 U/G/L와 두 반복에서 일치했다. 공통 빌드 기동 3/3, 보조 직접 API 6/6은 별도다. 앞선 GUI 확인 37건 중 8건은 입력이나 후속 키 도달에 실패했다. 나머지 29건은 정식 분모와 저장 순서가 다른 예비 재현이었다. [원장](runs.jsonl) · [비교 및 화면 검산](evidence/verify.json) · [예비 실행](evidence/gui-attempts.jsonl)

**REVIEW_READY.** 네 입력의 실험 전제, 두 반복 및 U 기준을 확인했다. X3에서는 L이 G와 다른 화면을 남겼고 둘의 실제 V 결과는 같았다. G를 건넬 근거는 이 입력에서의 사용자 표시 오류와 추가 클릭의 필요성이다. 측정한 네 입력에서는 두 구현 중 하나가 편집 대상을 바꾼 사례가 없다. 두 반복과 도구 검산은 같은 연구자의 재현이다. [검산과 원장](evidence/verify.json)

1/0/0은 순서대로 선택 flag·실제 선택 membership·Note mark다. Fingering에는 –를 쓴다. 메뉴 직후의 RANGE 2와 NONE 0은 선택의 종류와 객체 수다. 주 키는 undo 엔트리를 추가하지 않았다. 표의 undo는 명시적으로 재클릭한 -R에서 변경한 값의 복구다. 원 파일은 주 편집 키 뒤, **재클릭 전에** 저장했다. 재열기에는 그 저장본의 SHA를 다시 비교했다. [실행 방법](reproduce.md)

### Q1. 원 요구와 보존 범위

2019년 #4590의 작성자와 댓글은 새 파트에 실제 선택이 없는데 파란 선택 표시가 남는 현상과 복제 기본 동작에서 선택을 초기화할 적용 범위를 논의했다. 당시 검토자는 기존 호출자들이 곳곳에서 명시적으로 선택을 끄고 2.x도 비트를 복사한다는 점을 짚었다. 신고자의 후속 음가·자식 편집은 당시 대화에서 확인되지 않는다. 연구의 E4/C4·Fingering 기대값과 기존 링크 보존 조건은 사전 등록한 가설이다. [PR 본문과 당시 댓글](https://github.com/musescore/MuseScore/pull/4590) · [사전 등록](cases.csv)

MuseScore 3 설명은 voice 1 화음과 복수 성부에 대해 남길 음을 구분하고 필요한 하단 보표의 수를 다룬다. undoExplode의 assertion은 cmdExplode의 저장본과 명령 undo 뒤의 저장본 비교다. 같은 파일의 undoExplodeVoices, undoExplode1 본문은 테스트 파일명 선언만 한다. 파트 시험에는 생성·track map과 Fingering 추가·undo·redo가 있다. 시험의 assertion은 파일 내용을 비교한다. 일시적 플래그와 후속 GUI 대상은 본 실험의 관측 항목이다. [MuseScore 3 문서](https://musescore.org/en/print/book/export/html/278625) · [Explode 원 시험](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/mtest/libmscore/implode_explode/tst_implodeExplode.cpp#L52-L96) · [파트 원 시험](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/mtest/libmscore/parts/tst_parts.cpp#L135-L237)

### Q2. 진입 경로와 재선택

| 경계 | 진입·인자 | 다음 선택이 생기는 시점 |
| --- | --- | --- |
| X1, 매회 1회 | cloneVoice(1,4,0,1920,false,true), CloneVoice의 oldTrack=-1로 원 track 1 음 제거. 보표 0·1 선택 | 직후 G의 E4 0/0/0, U/L 1/0/0. explode_reselected에서 목적음이 모두 RANGE에 합류. X1-G-1의 probe 13→14→19→22 |
| X2, 매회 1회 | pasteStaff(xml, Segment tick=0, staff=1), pasteMode=true. 붙임 경계에 두 음 60·64가 존재 | 붙임의 planned range 뒤 상하 보표별 음을 걸러 최종 explode_reselected. X2-G-1의 probe 16→17→25→28 |
| X3/X4, 각 매회 2회 | Parts dialog가 Flute와 추가 Oboe에 AddExcerpt와 createExcerpt 진입. 기존 Oboe의 ID와 master link를 추적 | Flute의 선택 목록은 생성 시와 탭 활성화 뒤 모두 빈 상태. 화면 flag는 G/L 조건에 따라 다름 |
| A-E05, 매 build 1회 | 081 probe 직접 cloneVoice(0,1,0,1920,false,false), 원 C4는 선택된 채 남음. 목적은 같은 보표 voice 2 | 후속 RANGE 선택이 없다. C1은 G 0/0/0과 U/L 1/0/0. 재열면 모두 0/0/0 |

계측의 selection_clear는 전에 등록된 목록을 남기고 range_members_rebuilt는 새 목록을 남긴다. X1의 G/L 차이는 마지막 deselectAll 및 select(..., RANGE)를 통과한 뒤 사라졌다. X2의 새 음은 역직렬화 뒤부터 세 빌드가 동일했다. [X1 경계](evidence/gui/X1-G-1/app.jsonl) · [X2 경계](evidence/gui/X2-G-1/app.jsonl) · [E05 직접 호출](evidence/api/E05-L/stdout.jsonl) · [선택 재구축](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/select.cpp#L452-L558)

### Q3. 숨은 자식과 L의 초기화

X3 전제를 여섯 번 모두 역사판 experimental 메뉴에서 만들었다. 원 C4의 Fingering은 layer mask=1로 바뀐 뒤에도 tag=2, flag/list=1/1, visible 속성=1을 유지했고 화면에서 사라졌다. 복제 Note와 Fingering은 새 ID였고 원본과 양방향 링크를 가졌다. X3-L-1의 probe 10→16→18→19에서 Note::scanElements는 후보를 한 번 기록했다. tag_pass=false라 자식 callback은 0회였다. X4-L-1의 probe 12→14→15에서는 같은 파일의 mask=3에서 callback 1회와 flag 1→0을 기록했다. all=true여도 해당 tag 조건은 적용된다. 원본 선택 자동 해제와 복사 누락은 각 0/6이었다. [X3 L 원본·복제·scan](evidence/gui/X3-L-1/app.jsonl) · [X4 L 방문](evidence/gui/X4-L-1/app.jsonl) · [Note 복사](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/note.cpp#L559-L620)

기존 Oboe의 음 67, 1920 ticks, 원 master peer는 유지됐다. New All은 기존 Oboe가 있는 이 악보에서 이름이 같은 새 Oboe도 만들었다. 두 새 파트 생성으로 Oboe 링크 그룹 참여자는 한 명 늘었다. 선택이나 VISIBLE이 기존 Oboe로 옮겨 간 경우는 없었다. X1/X2는 파트를 추가하지 않았고 Violin의 기존 피어를 보존했다. [파트 원장](evidence/gui/X3-U-1/app.jsonl) · [저장된 X3](evidence/gui/X3-U-1/saved.mscx)

### Q4–Q5. 화면, 실제 편집, 지속성

X1/X2의 6은 모두 pad-note-2까지 도달했다. RANGE는 단일 chord/rest를 돌려주지 않아 음 길이와 undo index가 그대로였다. 목표 음을 한 번 클릭한 대조에서는 목적 tr4만 1920→960 ticks에 도달했고 undo 뒤 1920이었다. X1 stderr는 여섯 번 모두 기존 rest 경고를 보였다. 저장 XML의 해당 목소리에는 겹치는 rest가 없고 음가·Violin link를 재열어 대조했다. 다른 다성부 입력의 후대 보고에서는 겹치는 rest가 남았다. [정식 X1 로그](evidence/gui/X1-G-1/app.stderr) · [X1 저장본](evidence/gui/X1-G-1/saved.mscx) · [보고 #16896](https://github.com/musescore/MuseScore/issues/16896)

X3의 숨은 Flute 영역에는 자식의 잉크가 없었다. 다시 보일 때 (321,304,3,8) 영역의 파란 픽셀은 각각 두 반복에서 U 8·8, G 0·0, L 8·8이었다. X4에서는 U 8·8, G/L 0·0이었다. Flute의 실제 목록은 모두 비었고 master의 보이는/숨은 핑거링은 선택을 갖고 있었다. 탭 왕복으로 키보드 포커스를 돌려준 뒤 V가 Score에 도달했고 visible 값과 undo index는 그대로였다. 이어지는 별도 클릭 대조에서 V는 Flute 자식만 1→0, undo는 0→1이었다. 주 편집 뒤 저장이 끝난 열린 세션에서도 X3 L의 선택색이 남았다. 재열기에서 같은 링크와 값이 복원되고 파란 픽셀이 사라졌다. [X3 L 화면](evidence/gui/X3-L-1/04-shown.png) · [X3 G 화면](evidence/gui/X3-G-1/04-shown.png) · [X3 L 재열기 화면](evidence/gui/X3-L-1/07-reopened.png) · [단계별 픽셀과 식별자](evidence/verify.json)

E06 보조 API의 U/G/L에서 새 음 flag/list/mark=0/0/1에 curColor는 선택색이었다. 재열기는 모두 0/0/0이었다. 이 대조는 mark setter를 직접 사용했다. 세 GUI 빌드는 no-synthesizer 옵션으로 실행됐고 playback 타이밍은 범위 밖이다. Fingering에는 Note mark가 없다. Xvfb 클릭 좌표는 각 steps.jsonl, A-E05·A-E06에는 직접 API entry mode가 있다. [A-E06 G](evidence/api/E06-G/stdout.jsonl) · [GUI 좌표 예](evidence/gui/X3-L-1/steps.jsonl) · [색 분기](https://github.com/musescore/MuseScore/blob/f4fcf53ff65c56f0efb616a3af209d3faba9b342/libmscore/element.cpp#L334-L366)

### Q6. 다른 분야에서 옮겨올 조건

| 관점 | 원하는 공유 범위 |
| --- | --- |
| 악보 작성자 | 음·박자 등 합의된 내용을 악보와 파트에서 함께 관리한다. Explode로 옮긴 목적음에는 원본 파트 링크와 다른 편집 기대가 있다. |
| 파트 편집자 | 공통 음을 공유하면서 파트용 가시성과 선택을 관리한다. cue 크기 논의처럼 생성 시 가져오는 값과 이후 공유하는 속성을 따로 정한다. [파트 외형 논의](https://github.com/musescore/MuseScore/issues/18772) |
| 공통 API 유지관리자 | clone의 flag와 select의 실제 선택 등록을 각각 문서화한다. 소비자가 새 항목을 계속 편집하려면 해당 명령이 대상을 지정한다. [Paste의 후속 선택 수정](https://github.com/musescore/MuseScore/pull/22352/commits) |

| 분야 | 명령과 반대 관측 | 예측과 적용 경계 |
| --- | --- | --- |
| 벡터·3D | Inkscape Edit → Clone → Create Clone 뒤 Shift+D는 원본을 선택한다. 선택된 별 clone에는 형상 handle이 없다. Relink to Copied 뒤 캔버스에서 사라져 orphaned로 남은 별도 보고가 있다. Blender Duplicate Linked는 데이터를 공유하고 원본의 object 선택을 끈 뒤 새 object를 선택한다 | 링크와 현재 타깃을 따로 확인해야 한다. SVG use는 숨겨져도 shadow tree를 만들고 외부 이벤트의 대상으로 host를 반환한다. MuseScore의 Fingering은 직접 속성을 고칠 수 있다. [Inkscape 명령](https://inkscape-manuals.readthedocs.io/en/latest/cloning-objects.html) · [Relink 신고 원문](https://gitlab.com/api/v4/projects/inkscape%2Finkscape/issues/2379) · [Blender 구현](https://github.com/blender/blender/blob/v4.5.0/source/blender/editors/object/object_add.cc#L4487-L4511) · [SVG 2](https://www.w3.org/TR/SVG2/struct.html#UseShadowTree) |
| 텍스트·다중 뷰 | VS Code의 Split Editor in Group과 Focus Other Side가 뷰를 바꾼다. 선택 문자열과 같은 텍스트 표시가 다른 뷰에 생기지 않는 제보가 있다. CodeMirror 예제는 문서 changes만 dispatch하고 한쪽 history를 사용한다. Emacs는 같은 buffer에서도 창마다 point가 있다 | 탭·포커스·문서 값·목록을 각각 확인하는 예측을 지지한다. 문자열의 위치 모델에서 악보의 원음·복제음 링크는 자동으로 따라오지 않는다. [VS Code 명령](https://code.visualstudio.com/docs/configure/custom-layout#split-in-group) · [다중 뷰 제보](https://github.com/microsoft/vscode/issues/234937) · [CodeMirror 구현](https://github.com/codemirror/website/blob/master/site/examples/split/split.ts) · [Emacs 창별 point](https://github.com/emacs-mirror/emacs/blob/emacs-30.1/doc/lispref/windows.texi#L5114-L5170) |
| 의도적인 공동 선택 | Blender Select Linked → Object Data는 같은 데이터의 원본·인스턴스를 함께 선택한다. Qt 두 뷰는 같은 model에 하나의 QItemSelectionModel을 주면 같은 row를 함께 선택한다 | 이 조건에서는 공동 선택이 요구다. MuseScore X3은 새 파트의 별도 주소와 빈 목록을 읽었다. [Blender 명령](https://github.com/blender/blender/blob/v4.5.0/source/blender/editors/object/object_select.cc#L603-L636) · [Qt 예제](https://doc.qt.io/qt-6/model-view-programming.html#sharing-selections-among-views) |
| 저장과 undo | GIMP는 XCF의 현재 픽셀 선택을 채널로 저장한다. SpreadsheetML은 sheetView에 activeCell/sqref를 둔다. ProseMirror 시험은 undo/redo의 selection bookmark를 검증한다. MusicXML 교환에는 linked staff가 빠지는 보고가 있고 Inkscape PDF에서는 복제 arrowhead를 잃는 보고가 있다 | 파일·undo마다 선택이나 링크를 복원하는 계약을 확인한다. 본 실험이 비교한 것은 동일 native MSCX와 같은 편집 키다. [XCF](https://developer.gimp.org/core/standards/xcf/#selection) · [SpreadsheetML 예제](https://github.com/OfficeDev/office-content/blob/main/en-us/OpenXMLCon/articles/17abd341-abe9-4eee-9bb3-27fded0b04d2.md) · [ProseMirror 시험](https://github.com/ProseMirror/prosemirror-history/blob/master/test/test-history.ts#L221-L243) · [MusicXML 보고](https://github.com/musescore/MuseScore/issues/17481) · [PDF 보고](https://gitlab.com/api/v4/projects/inkscape%2Finkscape/issues/3911) |

직접 읽은 자료는 42행, 독립 계보 **28개**다. 역사 코드와 시험을 같은 계보로 묶었고 같은 결함의 PR·병합도 한 번으로 셌다. 배정은 MuseScore 역사·독립 편집 9, 같은 종류의 편집 사례 5, 벡터/3D 4, 텍스트/다중 뷰 4, 저장·재열기·undo 반례 6이다. 같은 종류 중 4건은 당사자 또는 후속 재현자가 성공·무변화·회귀·실패를 실제 관측했고 Dorico 문서는 사용법의 기준이다. [출처 원장](sources.jsonl) · [열람 실패 및 대체 경로](evidence/access-attempts.jsonl)

### Q7. 링크를 고르는 질문

개발자에게 물을 질문은 **“문제가 새 파트에서만 보이나요, 아니면 일반 복사 직후 재선택 없이 같은 편집을 눌러도 다른 객체가 바뀌나요?”**다. 전자와 X3 같은 태그 조건에는 G의 첫 부모 대비 한 줄과 X3 검증을 짝짓는다. 후자라면 기준 조작의 복제·메뉴 종료 재선택·후속 명령의 입력 목록·객체 값 네 지점을 읽는다. 현재처럼 후속 결과가 같으면 편집 대상을 이유로 한 구현 선택은 유보한다. [G 구현](https://github.com/musescore/MuseScore/commit/16851045c9e50eafb016c5cf4f2733f974e841bf) · [판별 시험](fixtures/verify.py)

### 판단을 바꿀 다음 조사 세 건

1. **RANGE에서의 음가 테스트는 무변화였다.** X1·X2의 메뉴 직후 범위 목록을 소비하는 V 속성 편집을 G/L에서 두 번씩, 총 8회 실행한다. 양 보표 selected ID, visible 전후, undo를 읽는다.
2. **숨은 태그의 화면 차이는 Fingering 한 종류와 -e에서 확인했다.** 같은 비기본 태그의 Note Symbol을 X3/X4 절차에 넣고 G/L에서 두 번씩, 8회 실행한다. callback 방문과 화면, 목록, V가 바꾼 ID를 읽는다. 화면이 다를 때 사용자가 어느 객체를 다시 고를지는 별도 관측이다.
3. **X1에서 rest 교체 경고가 있었고 이 한 마디는 정상 재열기됐다.** X1의 두 마디를 타이로 잇고 목적 보표의 마디 rest 한 개와 나뉜 rest를 대조한다. G/L에서 두 번씩, 8회 실행하고 음·rest의 길이 합과 tick별 겹침, Explode 자체의 undo와 재열기 시 피어를 읽는다. [유사 후대 사례](https://github.com/musescore/MuseScore/issues/16896)
