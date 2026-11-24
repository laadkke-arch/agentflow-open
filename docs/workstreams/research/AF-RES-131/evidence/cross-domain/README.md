# 다른 분야의 선택과 동작 허용

## QGIS 3.40의 활성 레이어와 편집 상태

일반 도구의 선택은 현재 활성 레이어에서 작동한다. 편집 절은 공급자의 쓰기 지원과 레이어 편집 상태를 요구하고, Move Feature(s)는 첫 클릭의 위치와 두 번째 클릭의 목적지를 받는다. 활성 편집 레이어의 선택이 비었으면 첫 클릭 아래의 가까운 피처 하나를 찾는다. 교육 예제의 school_property도 레이어를 활성화한 뒤 Toggle Editing을 켜야 도구가 활성화되며, Vertex Tool의 두 클릭 예는 편집 모드에서 좌표를 바꾼다. [선택 도구](https://docs.qgis.org/3.40/en/docs/user_manual/introduction/general_tools.html#selecting-features) · [편집과 이동](https://docs.qgis.org/3.40/en/docs/user_manual/working_with_vector/editing_geometry_attributes.html#move-feature-s) · [교육 예제](https://docs.qgis.org/3.40/en/docs/training_manual/create_vector_data/create_new_vector.html) · [3.40.6 Move Feature 구현](https://github.com/qgis/QGIS/blob/5d7f6a3e2657224f6eaede0f9ef245e52d6225e9/src/app/qgsmaptoolmovefeature.cpp#L91-L154)

QGIS 3.40.6-Bratislava의 별도 Xvfb 프로필에서 memory 레이어 A·B를 쓰고 실제 도구에 QtTest click→move→click을 보냈다. 시도 4개 중 액션 상태 4개와 실제 두 번의 좌표 변경 2개를 확인했다. EPSG:3857 좌표의 나머지 소수는 실제 픽셀 반올림 차이로 남겼다.

| 설정 | 도구와 조작 | 좌표 결과 |
| --- | --- | --- |
| A 활성, 1 선택, 편집 꺼짐 | Move Feature 비활성, 클릭 0 | A (20,30) 유지 |
| A 활성, 1 선택, 명시적 읽기 전용 | Move Feature 비활성, 클릭 0 | A (20,30) 유지 |
| A 활성, 선택 ∅, 편집 켜짐 | A hit, 두 클릭 | A (20,30) → (31.904762,38.730159), B 유지 |
| A의 1 선택, B 활성·편집 켜짐·선택 ∅ | B hit, 두 클릭 | A 유지, B (65,72) → (77.301587,81.126984) |

이 관측은 선택과 편집 자격을 UI에서도 분리할 근거다. QGIS의 이동은 클릭→미리보기→클릭이고, 레이어 provider가 실제 파일 쓰기를 승인하고 저장하는 경로는 이 memory fixture에서 검사하지 않았다. OpenLayers의 목록 우선이나 어느 이벤트가 DragPan에 전파되는지에 그대로 대입할 수 없다. [명령 입력 코드](../../replay/qgis_move.py) · [실측 stdout](qgis.stdout.log) · [stderr](qgis.stderr.log) · [종료값](qgis.exit)

## Audacity 3.7.5의 파형·클립 핸들·시간 범위

Audio Clips 매뉴얼과 편집 실습은 waveform의 시간 선택과 clip-handle의 이동을 구분한다. 범위 안의 handle에서 복수 선택을 움직이면 시간 선택도 함께 옮겨지고, 선택 밖의 handle을 잡으면 그 클립만 움직인다. 인접 클립 사이 간격 부족이나 오른쪽 클립 고정 설정은 다른 제약이다. Sync-Lock의 공식 실연에선 시간상 겹치는 비선택 트랙의 clip과 라벨도 움직일 수 있다. Audacity 4.0.0은 Sync-Lock을 없앴으므로 3.x 절을 반환할 때 제품 판을 먼저 맞춘다. [트랙과 클립](https://manual.audacityteam.org/man/audacity_tracks_and_clips.html#moving) · [시간 및 트랙 선택](https://manual.audacityteam.org/man/audacity_selection.html#selection_toolbar) · [편집 실습](https://support.audacityteam.org/basics/audacity-editing#moving-sections-of-audio-clips) · [Sync-Lock 실연](https://manual.audacityteam.org/man/sync_locked_track_groups_time_shifting.html#example_moving_a_clip) · [4.0 릴리스](https://github.com/audacity/audacity/releases/tag/Audacity-4.0.0)

공식 3.7.5 AppImage의 SHA-256을 확인한 뒤 4초 440Hz 합성 음원 하나를 열었다. 신호·샘플은 탐색용 가상 데이터다. 개별 X11 포인터 입력에서 horizontal delta +220px와 첫 x=380을 고정하고 y만 파형 274 또는 핸들 221로 바꿨다. 선택 시작값은 command pipe로 만들고, 전후 clip 값과 트랙 선택은 `GetInfo` JSON으로 읽었다. 시간 범위는 Selection Toolbar의 표시를 1ms 정밀도로 재독했다. 예정·실행·비교 가능 각각 3이다.

| 시작 | 실제 위치 | clip 구간 전후·시간 선택 전후 |
| --- | --- | --- |
| track 0 선택, 0.300–1.200s | waveform | clip 0–4s 유지. 시간 선택 0.779–1.685s. [전](audacity/selected-waveform-before.png) · [후](audacity/selected-waveform-after.png) |
| track 0 선택, 0.300–1.200s | clip handle, 시간 선택 안 | clip 0.906281–4.90628s. 시간 선택 1.206–2.106s. [전](audacity/selected-clip-handle-before.png) · [후](audacity/selected-clip-handle-after.png) |
| track 0 미선택, 커서 0s | clip handle | clip 0.906281–4.90628s. track 0 선택 없음, 시간 선택 0.000–0.000s 유지. [전](audacity/unselected-clip-handle-before.png) · [후](audacity/unselected-clip-handle-after.png) |

clip 길이는 1ms 이내에서 보존됐다. 1차 시도의 clip JSON은 같았지만 연속 script 명령 직후 캡처에서 이전 화면이 남았다. 캡처 전 550ms 대기를 추가해 세 동작을 새로 실행하고 화면과 JSON을 맞췄다. Sync-Lock의 예제, 스테레오, 다른 클립 간격과 4.0의 새로운 편집 도구는 문서 범위다. OpenLayers로 옮길 것은 대상·동작 영역·유지할 값의 구분이며, 오디오의 스냅·동기화·시간 단위 계약은 오디오 안에서만 적용된다. [실측 stdout](audacity.stdout.log) · [정상 종료값](audacity.exit) · [첫 캡처 시도의 JSON stdout](audacity-pre-redraw.stdout.log) · [스크립트](../../replay/audacity_pointer.py)

Xvfb 1200×780×24, no TCP인 로컬 화면만 사용했다. QGIS의 초기 시도는 DISPLAY 부재 및 Qt offscreen의 signal 11에서 종료됐다. Xvfb에서 정상 실행했다. 테스트에서 남긴 파일은 별도 프로필과 경로 아래다. QGIS와 Audacity의 시도는 지도 84회 분모에 포함하지 않는다. [환경](environment.json) · [첫 QGIS 실패](qgis-no-display.stderr.log) · [두 번째 QGIS 실패](qgis-offscreen.stderr.log)
