# 보충 입력 원장

`node replay/drive.mjs --mode supplement --out evidence --chromium /usr/bin/chromium`에서 10/10 실행했다. 포인터 전 과정 비교 8/8과 옵저버 없이 정착 비교 2/2다. 아래의 두 반복 합계는 본 16행과 대조 12행의 분모와 별개다. [stdout](stdout.log) · [stderr](stderr.log) · [종료값](exit.txt) · [입력·환경](environment.json)

| 입력 | 원 로그 | 판정 |
| --- | --- | --- |
| 임곗값 이내 이동 | [R1](S-tiny-r1.json) · [R2](S-tiny-r2.json) | (1,0), (3,0), (3,3) CSS px. T down 수락 2/2, 첫 pointerdrag 0/2, geometry·center 모두 보존 2/2. |
| features와 거부 filter | [R1](S-features-and-filter-deny-r1.json) · [R2](S-features-and-filter-deny-r2.json) | 목록의 parcel-01이 이동했다. 두 행에서 제공한 filter callback은 0회. |
| features 생략과 거부 filter | [R1](S-filter-alone-deny-r1.json) · [R2](S-filter-alone-deny-r2.json) | 두 행에서 filter 5회씩 모두 false. down 후보가 거부되고 DragPan이 center를 움직였다. |
| features 생략과 허용 filter, 빈 선택 | [R1](S-filter-alone-accept-no-selection-r1.json) · [R2](S-filter-alone-accept-no-selection-r2.json) | 두 행에서 filter 4회씩 모두 true. 별도 사전 선택 없이 첫 드래그의 피처만 움직였다. Select는 지도에 등록돼 있고 선택 결과는 빈 목록이었다. |
| 동시 처리에서 live 옵저버 해제 | [R1](S-observers-off-simultaneous-r1.json) · [R2](S-observers-off-simultaneous-r2.json) | 초기와 정착 읽기는 유지했다. DOM·handler 원장 공석은 설계된 미관측이다. 두 정착 기하·center·피처 pixel 및 PNG가 [관측 켠 같은 조건](../main/M-in-feature-translate-pan-r1.json)과 같았다. |

filter 호출 횟수에는 hover와 up의 cursor 갱신도 포함된다. 호출이 없었던 결합 조건과 같은 초기 피처의 거부 단독 조건을 비교했다. 병합 당시 v6.0.0의 filter와 목록 결합은 소스에서 확인됐다. 이 브라우저 실험은 10.11.0의 조합이다. [판별 소스](../map-sources.md)
