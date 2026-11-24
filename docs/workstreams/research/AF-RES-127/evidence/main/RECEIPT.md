# 본 입력 원장

봉인판 `ed2d7895451b3653d72fc7665a27281f2e20e1ee`에서 `node replay/drive.mjs --mode main --out evidence --chromium /usr/bin/chromium`을 실행했다. 종료 0, 본 16/16 실행·16/16 trusted 포인터 비교 가능, 8/8 셀의 R1/R2가 같은 범주 및 같은 전후 좌표였다. 비교 불가·미실행 각 0. [실행 stdout](stdout.log) · [stderr](stderr.log) · [입력·번들·환경](environment.json) · [시도 원장](../../runs.jsonl)

| 같은 초기 그림의 대표 | 실제 down과 처리 | 정착한 기하 / 중심 / 피처 pixel |
| --- | --- | --- |
| [선택·피처·P,T 등록](M-in-feature-pan-translate-r1.json) | CANVAS의 parcel-01/owned. T down true, stopDown true, 외부 false. 첫 drag는 T만 처리했다. | (-56,40) / (0,0) / (292,180) |
| [선택·피처·T,P 등록](M-in-feature-translate-pan-r1.json) | 같은 hit. P down true, stopDown false, 외부 true. T down true, 외부 false. P와 T가 뒤이은 drag를 받았다. | (-96,62) / (-64,36) / (304,187) |
| [미선택·피처·P,T 등록](M-out-feature-pan-translate-r1.json) | 같은 hit. T 후보는 parcel-01이나 목록 검사에서 거부. P가 처리했다. | (-128,80) / (-64,36) / (288,178) |
| [선택·배경·P,T 등록](M-in-background-pan-translate-r1.json) | 같은 CANVAS에서 지도 hit 공집합. P가 처리했다. | (-128,80) / (-64,36) / (288,178) |

16행에서 관측한 record 1,942건은 DOM·MapBrowserEvent·핸들러·값과 공개 이벤트를 포함한다. 전 행에서 1px 첫 이동은 pointermove, (+4,+2)의 둘째 이동은 첫 pointerdrag였다. Pan 단독 변화 행의 첫 drag는 centroid를 고정하고 둘째 drag부터 center가 바뀌었다. view 해상도 2, 회전 0, 피처 ID와 초기 선택 목록을 보존했다. 전 행의 초기 지도 PNG가 하나의 SHA-256으로 일치했다. [초기 지도 표면](../surfaces/51b9806235305c705fef7a4da697e19e31e4830120bd42571fa59b726b7bf062.png)
