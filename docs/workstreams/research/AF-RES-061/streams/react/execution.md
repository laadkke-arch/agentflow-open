# React Spring 재현·검사 범위

## 실행한 대상과 시각

주체는 `/root/react_release`, Linux x64의 Node **v24.22.3**다. GitHub source는 `b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a`, 실행한 배포 구성요소는 **@react-spring/core 10.0.3 CommonJS development**다. animated/shared/rafz/types도 10.0.3, React는 19.1.2로 명시 고정했다. 사용자 브라우저·기기·과거 이슈 작성자의 실행이 아니다.

2026-11-23T05:34:48.789Z에 `probes.cjs` 25개 논리 probe를 마쳤고 exit 0이었다. 05:38:23.329Z의 `stop-events.cjs` 2개 교정 probe도 exit 0이다. 그 이전 단일 16ms smoke probe 1개는 환경 확인이며 독립 입력을 늘리지 않는다. `advance`의 내부 1ms 반복이나 trace 행을 독립 실험 수로 세지 않는다.

## 동일 배포 증명

[`runtime-manifest.json`](runtime-manifest.json)에 registry URL, gitHead, 6개 package version·tarball URL·integrity와 실행 파일 SHA256을 기록했다. Registry의 core/shared gitHead는 위 소스 SHA다. npm 캐시의 core tarball을 직접 해시하여 공식 SHA1 `3b4f3991f5902ce46770c2c1ef05c8e53c3a0f73`과 SHA512가 일치함을 검사했다. tarball 안의 development CJS 파일과 실제 설치 파일도 바이트 단위로 같았다. 해당 파일 SHA256은 `158b31080852b71a4787a586ae7f10cac85d2eef002d22e476c3d875ff63a520`이다.

원 TypeScript와 transpiled JavaScript가 바이트 단위로 같다고 주장하지 않는다. 배포에는 source map이 없었다. `advance`의 배포 코드와 고정 소스에서 1ms step, ceil, 힘의 변환 계수, restVelocity·precision fallback, clamp 순서를 직접 대조했다. 실제 실행 파일이 이 릴리스에 해당한다는 증거와 라이브러리 소스를 재빌드했다는 주장은 다르다. 재빌드는 **미실시**다.

## 명령

저장소 루트에서 실행한다. 모든 새 파일·npm cache·source checkout은 소유 경로 안에 들어간다. 설치 시 lifecycle script를 실행하지 않았다.

```sh
AF_RES_061_REACT=docs/workstreams/research/AF-RES-061/streams/react
npm --cache "$AF_RES_061_REACT/.workbench/npm-cache" --prefix "$AF_RES_061_REACT/.workbench/runtime" install --ignore-scripts --no-audit --no-fund --package-lock=true @react-spring/core@10.0.3 @react-spring/animated@10.0.3 @react-spring/shared@10.0.3 @react-spring/types@10.0.3 @react-spring/rafz@10.0.3 react@19.1.2
node "$AF_RES_061_REACT/probes.cjs" > "$AF_RES_061_REACT/probe-stdout.json"
node "$AF_RES_061_REACT/stop-events.cjs"
```

설치 결과는 `added 6 packages`, exit 0이었다. npm의 http-proxy 환경 설정 deprecation 경고는 실행 실패가 아니었다. npm이나 Node를 업그레이드하지 않았다.

소스 직접 읽기에는 아래 checkout을 사용했다. detached HEAD는 예상한 태그 커밋이다.

```sh
git clone --depth 1 --branch v10.0.3 https://github.com/pmndrs/react-spring.git "$AF_RES_061_REACT/.workbench/source"
```

## 출력과 입력의 구분

- [`raw-outputs.json`](raw-outputs.json): 25개 probe의 전체 출력, 주 사례의 기록된 frame trace, 환경.
- [`probe-stdout.json`](probe-stdout.json): 같은 실행의 요약 stdout. 별도 독립 실행이 아니다.
- [`stop-correction.json`](stop-correction.json): onRest를 초기 start에 연결한 교정 입력의 결과. 기존 probe에서 후속 no-op start로 연결한 listener는 null이었다. 이를 취소 callback 결함으로 해석하지 않는다. 원출력을 삭제하지 않았다.
- [`observations.json`](observations.json), [`observations.csv`](observations.csv): 봉인된 RS-N/RS-B 두 사례의 관측 연결.
- [`counterexamples.csv`](counterexamples.csv): 봉인 이후 추가한 경계 탐색. 주 사례나 사전 적중으로 합산하지 않는다.

16ms와 250ms 직접 관측은 **매번 초기값 0, 목표 1에서 새 인스턴스로 각각 한 번 advance**했다. 1ms/16ms/60Hz trace는 별도 frame schedule이다. 브라우저 RAF 250ms 공백은 첫 16.667ms 콜백 다음 시간 간격을 250ms로 둔 가짜 시계로 조사했으며, raw advance(250)의 결과와 구별했다.

## 미실시·미확인

상류 Jest 전체 suite, 공개 CI job 재실행, 브라우저 렌더링, OS의 reduced-motion 설정 전환, React Native 기기 실행은 **미실시**다. 이 작업에 필요한 공개 시험의 assertion과 snapshot은 직접 읽었다. 주 입력과 같은 고정판의 독립 보관 출력은 **미확인**이다. 연구자가 이번에 실행한 값은 그 결손을 메운 독립 원출력으로 세지 않는다.
