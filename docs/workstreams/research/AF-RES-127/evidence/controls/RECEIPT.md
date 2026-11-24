# 대조 입력 원장

`92e6fd713ac324be2e2ca7981a46949be371b85f`에서 본행과 같은 봉인 입력으로 `node replay/drive.mjs --mode controls --out evidence --chromium /usr/bin/chromium`을 보냈다. 12/12 실행·비교 가능, 미실행·비교 불가 각 0. R1/R2는 각 조건의 새 지도다. [stdout](stdout.log) · [stderr](stderr.log) · [종료값](exit.txt) · [입력·환경](environment.json)

| 조건 | 원 로그 두 반복 | down hit / 시작 처리 | 정착 기하 / 중심 |
| --- | --- | --- | --- |
| Translate만 | [R1](C-translate-only-r1.json) · [R2](C-translate-only-r2.json) | parcel-01/owned / T | (-56,40) / (0,0) |
| DragPan만 | [R1](C-pan-only-r1.json) · [R2](C-pan-only-r2.json) | parcel-01/owned / P | (-128,80) / (-64,36) |
| 둘 다 비활성 | [R1](C-both-off-r1.json) · [R2](C-both-off-r2.json) | parcel-01/owned / 공집합 | (-128,80) / (0,0) |
| 이동 없는 클릭 | [R1](C-click-r1.json) · [R2](C-click-r2.json) | parcel-01/owned / T가 down과 up 수락, pointerdrag 0 | (-128,80) / (0,0) |
| 경계 바깥·0px | [R1](C-edge-zero-r1.json) · [R2](C-edge-zero-r2.json) | 공집합 / P | (-128,80) / (-64,36) |
| 같은 경계 바깥·6px | [R1](C-edge-six-r1.json) · [R2](C-edge-six-r2.json) | 0px 공집합·6px parcel-01/owned / T | (-56,40) / (0,0) |

경계 두 조건의 down은 CSS (298,180), map pixel (274,160), 투영 좌표 (-92,80)이다. 겉보기와 스타일은 같았고 Translate가 받는 허용오차만 바뀌었다. click은 `translatestart`와 `translateend`가 있었고 translating은 0이었다. 대조 12행의 1,012 record에서 동시 변화는 0/12였고 둘 다 유지된 행은 4/12였다. 본행의 동시 변화 2/16과 구분한다. [본 입력](../main/RECEIPT.md) · [보충 입력](../supplement/RECEIPT.md)
