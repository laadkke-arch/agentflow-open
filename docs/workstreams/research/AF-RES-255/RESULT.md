| 시험·엔진·반복 | 빌드·폰트 | 원형 판정·픽셀 근거 | 실제 단어별 줄 | 예측·단언 차이 | 원영수증·미확인 |
|---|---|---|---|---|---|
| 002 · Chromium · 1 | 156.0.8078.79 · Ahem 20px · W 399.984 CSS px | PASS, exit 0 · `!=` · Δ 4,800/480,000 px | 123 567 901 / 345 789 123 | cut 3 관측. 공개 단언은 불일치. | [WPT](receipts/primary/chromium-002-r1/summary.json) · [좌표](receipts/geometry/chromium-002-r1/geometry.json) |
| 002 · Chromium · 2 | 156.0.8078.79 · Ahem 20px · W 399.984 CSS px | PASS, exit 0 · `!=` · Δ 4,800/480,000 px | 123 567 901 / 345 789 123 | cut 3 관측. 공개 단언은 불일치. | [WPT](receipts/primary/chromium-002-r2/summary.json) · [좌표](receipts/geometry/chromium-002-r2/geometry.json) |
| 002 · WebKitGTK · 1 | 2.54.3 · Ahem 20px · W 400.000 CSS px | PASS, exit 0 · `!=` · Δ 4,800/480,000 px | 123 567 901 / 345 789 123 | cut 3 관측. 공개 단언은 불일치. | [WPT](receipts/primary/webkitgtk-002-r1/summary.json) · [좌표](receipts/geometry/webkitgtk-002-r1/geometry.json) |
| 002 · WebKitGTK · 2 | 2.54.3 · Ahem 20px · W 400.000 CSS px | PASS, exit 0 · `!=` · Δ 4,800/480,000 px | 123 567 901 / 345 789 123 | cut 3 관측. 공개 단언은 불일치. | [WPT](receipts/primary/webkitgtk-002-r2/summary.json) · [좌표](receipts/geometry/webkitgtk-002-r2/geometry.json) |
| 003 · Chromium · 1 | 156.0.8078.79 · Ahem 15px · W 525.000 CSS px | PASS, exit 0 · `==` · Δ 0/480,000 px | plain·inline 각각 The quickest brown fox / jumped over the lazy dog | cut 4 관측. 기대 줄은 입력에 노출. | [WPT](receipts/primary/chromium-003-r1/summary.json) · [좌표](receipts/geometry/chromium-003-r1/geometry.json) |
| 003 · Chromium · 2 | 156.0.8078.79 · Ahem 15px · W 525.000 CSS px | PASS, exit 0 · `==` · Δ 0/480,000 px | plain·inline 각각 The quickest brown fox / jumped over the lazy dog | cut 4 관측. 기대 줄은 입력에 노출. | [WPT](receipts/primary/chromium-003-r2/summary.json) · [좌표](receipts/geometry/chromium-003-r2/geometry.json) |
| 003 · WebKitGTK · 1 | 2.54.3 · Ahem 15px · W 525.000 CSS px | PASS, exit 0 · `==` · Δ 0/480,000 px | plain·inline 각각 The quickest brown fox / jumped over the lazy dog | cut 4 관측. 기대 줄은 입력에 노출. | [WPT](receipts/primary/webkitgtk-003-r1/summary.json) · [좌표](receipts/geometry/webkitgtk-003-r1/geometry.json) |
| 003 · WebKitGTK · 2 | 2.54.3 · Ahem 15px · W 525.000 CSS px | PASS, exit 0 · `==` · Δ 0/480,000 px | plain·inline 각각 The quickest brown fox / jumped over the lazy dog | cut 4 관측. 기대 줄은 입력에 노출. | [WPT](receipts/primary/webkitgtk-003-r2/summary.json) · [좌표](receipts/geometry/webkitgtk-003-r2/geometry.json) |

표 1의 한 행은 원형 시험 1개×엔진 빌드 1개×신규 프로필 1개다. 계획 8, 원형 판정·PNG 및 별도 기하 각 8, 결측 0. 003 plain과 inline은 한 시험이다. 공개 run은 별도 층에서 미확인이다. 픽셀 분모는 같은 엔진의 800×600 입력·참조를 비교한 값이다.

| 변경 조건 | 실측 폭·줄수 | 가능한 규칙 | 규칙을 가르는 결과 | 적용 범위 |
|---|---|---|---|---|
| C1 Chromium auto → balance | W 159.984 CSS px, 3→3줄, advance [160,120,40] → [80,140,100] CSS px | 최대 접두사, 최소 분산 | cut 2;4 → 1;3, Δ 2,400 px | 고정폭 합성 입력 |
| W7 Chromium auto → balance | W 139.984 CSS px, 3→3줄, advance [120,120,40] → [80,60,140] CSS px | 최대 줄 길이 최소, 최소 분산 | cut 2;4 → 1;3, Δ 3,200 px | 고정폭 합성 입력 |

표 2의 임시 행 단위는 같은 엔진·같은 합성 입력에서의 한 가지 개입이다. 강제 개행·폰트·cue 자료와 반전 재생은 다음 묶음에서 결합한다.

고정 WPT SHA의 입력·참조와 각 엔진의 원 캡처를 확보했다. [실행 원행](runs.csv), [단어별 Range 원행](words.csv), [바이너리 지문](env.json), [재생 방법](replay.md).
