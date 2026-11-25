# 재생 방법과 원영수증

## 실행 환경

Debian 13 x86-64의 Python 3.12.14, Node 24.22.1, npm 11.9.0, Chromium 156.0.8078.79와 ANGLE Vulkan SwiftShader를 썼다. Python lxml 6.1.1, Pillow 13.0.0과 Info-ZIP UnZip 6.00은 archive와 프레임 대조에 사용했다. Three.js Git `084ec06444244980752a420f0e1af5cd8f112aa1`의 REVISION 188dev와 GLTFLoader/KTX2Loader/RoomEnvironment/Basis를 파일별 고정하고, Playwright Core 1.56.1 및 gltf-validator 2.0.0-dev.3.10은 npm lock의 integrity를 확인했다. [호스트 출력](receipts/host.stdout), [npm lock](tools/package-lock.json), [파일별 SHA-256](receipts/input-manifest.json)

모델 원파일과 EPUB은 실행 스크래치에 내려받는다. 고정 Git tree와 raw payload가 같을 때만 계속한다. 브라우저 단계는 loopback 전용 서버, 새 컨텍스트, HTTP cache 비활성화, SW 차단과 외부 요청 차단을 적용한다. 서버는 각 케이스의 `paths`만 모델 파일로 공급한다. `geometry`는 로더의 실제 배열까지, `material`과 `offline`은 고정 장면의 픽셀까지 검사한다. KTX loader 모듈과 Basis decoder 파일의 요청은 역할이 다르다. PNG 픽셀 재생은 이 Chromium/SwiftShader 및 조명 설정 범위다. [케이스별 제공 목록](receipts/cases.json), [브라우저와 서버 명령](receipts/experiment-commands.json), [실행 코드](tools/browser.mjs), [장면](tools/harness.mjs)

## 빈 폴더에서 실행

GitHub에서 작업 브랜치를 fetch한 checkout에서 결과 SHA를 인계 파일의 고정값으로 설정한다. 아래 실행 폴더에는 이전 npm cache·파일·Chrome 프로필이 없다. `representative`는 BoxTextured와 Lamp의 G/R/O, KTX on/off, PNG 누락, external URI 누락, fallback-off 및 차단 probe를 새 컨텍스트에서 실행하고, 양쪽 파서·검증기·EPUB도 재생한다. `full`은 24조건 전체를 2회 돌린다. 준비 단계에는 git/raw GitHub와 npm registry 접근이 필요하다.

```sh
owned=docs/workstreams/research/AF-RES-265
fixed_result=$(git log -1 --format=%H --fixed-strings --grep='Freeze AF-RES-265 result and self-check')
test -n "$fixed_result"
replay_root=$(mktemp -d)
mkdir "$replay_root/export"
git archive "$fixed_result" "$owned" | tar -x -C "$replay_root/export"
bash "$replay_root/export/$owned/tools/replay.sh" "$replay_root/input" representative
```

각 명령·stdout/stderr·종료값은 `input/commands/` 아래에 남는다. 합성 JSON/GLB는 원본 SHA를 바꾸지 않고 실행 폴더에서만 만든다. 재생 비교는 input/runtime 파일 지문, validator issue/callback, 두 추출기, 자원 요청/상태/바디 지문, 진입 콜백, 실제 decoded/bound 이미지, 배열, draw 횟수·mesh, 프레임 PNG/RGBA 지문을 본다. 동적 port와 blob ID는 비교에서 정규화한다. 원로그에는 각각 기록한다. [재생 비교 코드](tools/check_replay.py)

## 실제 별도 폴더 수행

측정 코드가 들어 있는 `7c002297b6f2fa7ebeaf74b7e623be757463872c`를 git archive로 펼쳐 처음부터 준비했다. 60개 파일과 EPUB archive 해시, 두 파서와 EPUB 두 경로, validator를 재현했다. 브라우저 실행 두 회차는 exit 0이고 probe를 포함해 50개 case를 기록했다. 첫 번들 명령은 비교기의 종료 신호/콜백 순서 차이로 exit 1이었다. 해당 비교에서 나온 원문을 보존했다. 이어 도착 URL·HTTP·자원 바디·기하·선택·콜백·draw 횟수·픽셀·PNG 지문을 엄격 대조하고 종료 이벤트/순서를 따로 보고하는 비교기에서 같은 원자료 모두 일치, exit 0을 받았다. 이 차이는 원본 두 회차의 성공과 렌더 품질 판정과 구분한다. [검사 원문·출력 SHA-256](receipts/clean-replay.json), [BoxTextured 재생 원행](receipts/clean-examples/round-2-BoxTextured-O.json), [Lamp 재생 원행](receipts/clean-examples/round-2-Lamp-O.json), [정정 내역](COUNTEREXAMPLES.md)

별도 폴더의 반복은 동일 실행자가 수행했다. 공개 저장소의 콘텐츠는 실험 영수증·렌더 결과·해시·코드이며, 원본 파일은 고정 URL에서 받는다. Khronos 표기의 Box/BoxTextured 제작자는 Cesium이고, 로고 표기가 별도로 있다. Lamp는 Wayfair/Eric Chadwick이다. EPUB OPF는 Creative Commons를 발행자, Jesse Dylan을 저자로 표시한다. [BoxTextured 크레딧](https://github.com/KhronosGroup/glTF-Sample-Assets/blob/e124e8d8d7330a5372bc2b4d00d39a4a9d7997ea/Models/BoxTextured/README.md#L28), [Lamp 크레딧](https://github.com/KhronosGroup/glTF-Sample-Assets/blob/e124e8d8d7330a5372bc2b4d00d39a4a9d7997ea/Models/AnisotropyBarnLamp/README.md#L140), [출판물 OPF](https://github.com/IDPF/epub3-samples/blob/7651e2002b631e6577fadf7e9e0692fa6efb8746/30/cc-shared-culture/EPUB/package.opf#L4)
