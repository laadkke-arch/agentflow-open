# 개봉 뒤 찾아본 반례와 비용

사전판 [8000ac5d](https://github.com/laadkke-arch/agentflow-open/tree/8000ac5d54c7564bb5cec61566e13ea8d78980f1/docs/workstreams/research/AF-RES-159)의 모집·패킷·예측을 유지했다. 아래 추가 입력은 개봉 뒤 반례를 찾은 판으로 본 표본 분모에 합산하지 않는다.

| 반례 | 고정 자료와 실제 관측 | 반환 링크 조건 |
|---|---|---|
| 같은 문자열로 다른 표시 또는 동작 G01, G05, I03-ko, I04–06 | G01에서 두 비활성 `(Varies)` 값은 각 언어에서 같다. 브러시의 종횡비 및 사각형의 종횡비 표시도 언어별 동일하다. I03-ko `그룹`은 기존 그룹 종류와 그룹화 명령에 둘 다 나온다. | 문자열 일치는 의미 채점의 분리 조건이다. 코드·위치·소비 역할을 사용한다. |
| 다른 문자열로 같은 기능 G15 | GIMP 모집 순위 15 `Connect to another display`, 두 실제 툴팁은 ko `다른 디스플레이와 연결합니다`/ `다른 보기 창과 연결합니다`. 두 액션이 `window_open_display_cmd_callback`의 같은 대화상자를 호출한다. 위젯 부모가 다를 수 있으며 실제 원격 디스플레이 연결은 실행하지 않았다. [Dock](https://github.com/GNOME/gimp/blob/a77e8fd05d3d08a58650531a3700100f6a3216b7/app/actions/dock-actions.c#L50) [View](https://github.com/GNOME/gimp/blob/a77e8fd05d3d08a58650531a3700100f6a3216b7/app/actions/view-actions.c#L157) [공유 핸들러](https://github.com/GNOME/gimp/blob/a77e8fd05d3d08a58650531a3700100f6a3216b7/app/actions/window-commands.c#L64) | 구현 원리 링크 목적이면 핸들러를 합친다. 도킹/보기 메뉴 배치나 그곳의 한국어가 요구되면 출원을 보존한다. |
| 빈 번역, 키 누락, fuzzy | G35 한국어 `Luminance` 두 msgstr가 빈값이다. 히스토그램 [측정 채널](https://github.com/GNOME/gimp/blob/a77e8fd05d3d08a58650531a3700100f6a3216b7/app/widgets/gimphistogrameditor.c#L154)과 [레이어 혼합 모드](https://github.com/GNOME/gimp/blob/a77e8fd05d3d08a58650531a3700100f6a3216b7/app/operations/layer-modes/gimp-layer-modes.c#L752) 모두 원문 반환. G07은 fill-style의 한국어 활성 키 결측, gradient-color의 키는 배경색. `fill-style`의 `style`은 [fill editor](https://github.com/GNOME/gimp/blob/a77e8fd05d3d08a58650531a3700100f6a3216b7/app/widgets/gimpfilleditor.c#L123)가 소비한다. G03a/G04b는 빈값과 달리 fuzzy msgstr가 있으나 MO에 없다. | 소스의 UI 근거를 보고할 수 있다. 번역 표시를 약속하려면 해당 PO의 유효 상태와 MO 조회로 확인한다. |
| 조용히 성공한 다른 실재 문맥 | 봉인한 자연 48 호출×언어의 다른 실재 키 조회에서 38회는 실제 키와 동일 출력. 10회는 다르고 그중 2회가 원문 fallback이다. 별개 C 구성인 없는 키 또는 초기 기본 도메인에서는 56/56씩 원문. 무문맥은 12 실제 값/44 원문(원장상 absent 38·obsolete 6)이다. | 조회 종료 0이나 선택 원문과의 동일성으로 정확한 문맥을 승인하지 않는다. MO 키 유무와 호출 근거를 사용한다. |
| 파일 이웃이 우연히 맞는 C | 24개 원 C의 참조값을 A 후보 파일들에서 부분 문자열로 찾아 한 문맥만 남기는 사후 휴리스틱은 15회 우연히 해당 문맥, 9회 여러 문맥. 예로 I03b의 `app.copy`를 도구바 후보 파일에서 찾으면 Verb만 남는다. 실제 action은 `app.selection-group`이다. 쌍의 C를 교환한 구성에서는 예산 내 17회의 9회가 잘못된 유일 판정, 8회 다의. 예산 밖 7회 제외. | 파일 단서로 후보를 탐색할 수 있다. 선택의 consumer까지 연결되기 전에는 유일 판정을 표시하지 않는다. |

상태의 “같음”과 “다름”은 [조회 원장](../runs.jsonl) W1와 W2에서 재현됐다. 보충층 입력 6개와 [두 반복](supplement-runs.jsonl)은 나중에 골랐으며 대체 모집이 아니다. G07a의 카탈로그 키는 공석이고, [G07·G35](supplement.csv)의 기능 연결은 레이블/enum을 사용하는 구현에서 판독했다. G02b의 C는 다른 enum이지만 같은 버킷 기능군이고, I04/I06의 C는 인접 채널이다. 완전히 독립적인 C라는 더 강한 추정에 쓰지 않는다.

[비용·채점](scores.csv)의 280행에서 실제 전달 JSON의 추가 UTF-8은 A+위치 105–123B(중앙 110.5), B 21–55B(35.5), C 21–50B(29.5), 직접 키 16–39B(28). 고정 커밋·경로·줄을 넣는 A+위치는 이 형식에서 길다. B/C의 추가 내용 원바이트와 JSON overhead를 따로 재계산한다. [C 사후 민감도](neighbor-sensitivity.csv)의 예산은 C 내용 한 값이다. 순수 소스 위치 회수 도구의 비용, 사람의 읽기 시간과 우연 일치율의 모집단은 미확인이다.
