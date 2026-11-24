# 네 판의 첫 드래그

본 24셀에 2반복을 실행했다. 예정 48, 실행 48, 비교 가능 48이다. 48/48의 down에서 동일한 지도 hit `parcel-01/owned`와 left primary trusted mouse를 기록했다. geometry만 16/48, center만 32/48, 둘 다 변화·둘 다 유지 각각 0/48이다. 48/48은 봉인한 hit·수락·범주와 callback 최소 횟수를 충족했다. [공개된 사전 예측](https://github.com/laadkke-arch/agentflow-open/blob/4aef99bcf8c6a59bf7436fc2aa32e822129fa179/docs/workstreams/research/AF-RES-131/predictions.csv) · [원장](../../runs.jsonl) · [stdout](main.stdout.log) · [stderr](main.stderr.log) · [종료값](main.exit)

같은 경계 판의 거부 행 ④에서 6.6.1은 down에 layers→filter→layers→layers, 6.7.0은 설정 콜백 0회다. ⑤에서는 6.6.1의 layer predicate만 down 3회 false로 돌아오고 6.7.0에서는 설정 콜백 0회다. 구판의 T false → P true에서는 center 첫 이동이 세 번째 명령에서 일어났다. 신판의 T true → 전파 중단에서는 geometry 첫 이동이 두 번째 명령에서 일어났다. 첫 1px 이동은 48/48에서 두 값을 유지했다. [6.6.1 ④](main/main-6.6.1-04-r1.json) · [6.7.0 ④](main/main-6.7.0-04-r1.json) · [6.6.1 ⑤](main/main-6.6.1-05-r1.json) · [6.7.0 ⑤](main/main-6.7.0-05-r1.json)

## 판별을 보존한 입력 어댑터

- Select 스타일은 기존 null과 같은 색·반경을 목표로 한다. 6.0.0 Select는 null에서 기본 선택 스타일을 쓰므로 같은 `parcelStyle` 객체를 명시했다. 6.6.1 이후에는 null을 사용했다. `layer.set`으로 동일 ID를 부여했고, 구판에 없는 `all`은 `noModifierKeys && primaryAction`으로 전개했다. 6.0.0 Translate에는 condition을 생략했다. 실제 매 행의 down이 동일한 비수식 primary mouse며, old/modern 모두 수락 가능한 입력이다. [어댑터](../../fixture/map.js) · [판별 옵션과 모듈 핀](../../fixture/versions.json)
- 6.0.0의 raw DOM target은 12/12 건이 `DIV.ol-overlaycontainer-stopevent`였다. 해당 판의 루프는 overlay의 직계 자식에서 중단하므로 이 컨테이너 자체는 Map으로 전달됐다. 나머지 36/36은 CANVAS였다. raw 지도 hit·스타일 입력·DPR과 투영값은 동일했다. 초기 화면 해시는 6.0.0 12건에서 한 값, 나머지 판 36건에서 또 한 값으로 일치했다. 6.0.0의 DOM·PNG 차이와 overlay 자식 위의 다른 계약을 보존한다. [6.0.0 전달](https://github.com/openlayers/openlayers/blob/55adb4ee33f6cd08b2b91511b5c9d2bdcc6f62e4/src/ol/PluggableMap.js#L1106-L1143) · [원 로그](main/main-6.0.0-04-r1.json)
- tarball 핀, 설치 모듈, bundle의 출처·바이트 수, 브라우저에서 삽입한 script SHA를 대조했다. 모든 판에서 CanvasVectorLayerRenderer 기반이다. 생성자 이름의 숫자 접미사는 bundle 기호이며 모듈 경로와 SHA도 함께 남긴다. Chromium은 156.0.8078.79이고 CDP의 GPU 보고는 SwiftShader다. [환경 및 입력 지문](environment-main.json)

실행 시작 당시 HEAD는 예측 커밋이다. 실행기·fixture는 당시 작업 트리의 파일 SHA로 기록했고 이 묶음에서 고정했다. npm 설치 및 정상 실행의 stdout·stderr·종료값을 함께 보존한다. 첫 실행기의 긴 `TMPDIR` 시도는 Unix socket 경로 제한으로 포인터 0건에서 종료 1이었다. 시스템의 짧은 임시 위치로 바꾸고 같은 입력에서 성공했다. [설치 stdout](npm-ci.stdout.log) · [시작 실패](startup/long-tmp.stderr.log) · [실패 종료값](startup/long-tmp.exit)
