# 좌표와 이동 문턱 파일럿

Translate·DragPan 두 처리기 모두 비활성. CanvasVectorLayerRenderer, Chromium 156.0.8078.79, DPR 1의 새 지도 세 개에 실제 마우스 이벤트를 보냈다. 이 원장은 위치와 이동 문턱을 고정하는 데에만 썼다.

| 원 로그 | CSS client / map pixel / 투영 좌표 | down 0px / 설정 tolerance의 피처 | 첫 pointerdrag |
| --- | --- | --- | --- |
| [P-feature-r1](P-feature-r1.json) | (280,180) / (256,160) / (-128,80) | parcel-01 / parcel-01 | (+4,+2) |
| [P-background-r1](P-background-r1.json) | (280,280) / (256,260) / (-128,-120) | ∅ / ∅ | (+4,+2) |
| [P-edge-r1](P-edge-r1.json) | (298,180) / (274,160) / (-92,80) | ∅ / parcel-01 (6) | (+4,+2) |

모든 down의 DOM target은 CANVAS였다. (+1,0)과 (+3,+3)에서는 pointermove만 받았다. 첫 드래그는 tolerance 3px를 넘기는 (+4,+2)였다. 세 지도 초기 center [0,0], 해상도 2, 회전 0, 반지름 16은 같았다. 경계 거리 18px와 동일 x의 빈 위치를 채택했다. Canvas scratch hit의 getImageData readback 경고는 raw notices에 보존했다. [고정 계획](../../plan.json) · [실제 입력 지문·환경](environment.json)
