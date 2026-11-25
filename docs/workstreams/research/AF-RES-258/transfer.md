# Transfer — 상태전이, 단위, 반례 및 실행 인계

## 대응 범위
N=상세/냉방 off, F=간략/냉방 on은 상태 이름의 대응일 뿐 물리 목적·장치 동등성 아님. world distance d, zoom z>0, effective x=d/z; 임계 D=100, h=.1, gap=Dh=10 world units. 온도 냉방 예(ESPHome T01, T05): 설정 23°C, deadband .3°C로 23.3 이상 on; overrun .7°C로 22.3 이하 off; 사이 유지. LOD에서는 N→F x>=100, F→N x<90; 중간 상태 보존. 온도에서 단위는 °C의 절대차, three는 설정 거리 비율, OMRON T04의 %는 센서 입력 스팬: 0–400°C×.2%=.8°C. 절대 온도/거리 수치 복사 금지. T07 비례 제어는 5% 스팬=20°C, SP100에서 50% duty 예; 시각 혼합과 비슷해 보이나 출력 시간 duty/plant feedback이며 LOD 가시 상태와 다름.

- B 봉인: F→N x<=90. P4 오류: 120→90→95에서 F,F,F가 원판, B는 F,N,N. 수정 B′는 x<90; 4/4 사후 적합, 새 사전 점수 아님.
- 단일 냉방 bang_bang 소스 T06 L97–138: >upper, <lower, 양 끝 포함 중간은 유지. 그대로 upper strict를 복사하면 P3에서 오류; lower equality는 LOD와 같음. thermostat 코드 T05 L1045–1095는 >= upper, <= lower, 따라서 B의 등호 선택도 원분야 내 실제 대안. 타 분야는 이력 가설을 좁힐 뿐 부등호 방향을 확정하지 못함.
- 최소 on/off/idle 시간 및 startup delay(T01 L1514–1532, T03 L104–122, T05 L334–380): LOD에는 시간 게이트 없음. 장치가 NaN으로 off하는 안전 처리도 그대로 옮길 수 없음. 예: 120 다음 89.999,95 즉시 처리 F,N,N. 냉방 최소시간이 남았으면 같은 입력 경로라도 F 가능. 이는 합성 반례, 장치 실측 아님.
- Unity E01/E02: 화면 높이 %, spatial blend (두 renderer), timed blend (시간 경과) 대안. 100 world units와 100%는 차원 불일치. 직교 투영 높이 20 world units인 화면에서 같은 거리 100의 높이 2/16 객체는 10%/80%; 50% screen threshold에서 다르게 분류되며 three D=100은 같은 결과. Godot E03/E04: AABB center distance + 절대 margin, disabled fade이면 hysteresis; 렌더러 fallback과 dependency fade는 별도. 
- A+ 반례: near API의 hysteresis 명칭을 아는 독자가 nominal upward, retention downward를 구현 없이 추론하면 이미 N/F/F/F 가설 가능. A는 보수적인 집합으로 봉인했을 뿐이며 분리된 A/B 독립 실험 없음. 따라서 순증분은 이 세 봉인 모델의 조건부 차이만. 출처의 역사적 차용은 미확인.
- C-mix 선형 90..100이면 final 95에서 N/F 각 .5, 단일 visible object 선택과 다른 출력 유형; 사후 채점 시 단일답 불일치 4/4, C 주 점수에는 포함하지 않음.

## Codex 실행용 정확판·입력
다음은 미실행 명령. 새 임시 작업 디렉터리에서 시행하고 원저장소/제품을 수정하지 않는다. Node import 직접 사용, npm install 및 WebGL 불필요. exit code와 raw stdout/stderr, git HEAD, node version, 모든 flag/level/effective distance를 보존. 결과 파일은 AF-RES-258 소유 경로 아래에만 저장하도록 작업자에게 전달; 사용자 화면 관측은 이 시험 범위 밖.

```sh
git clone https://github.com/mrdoob/three.js.git three-r170-check
cd three-r170-check
git checkout --detach beab9e845f9e5ae11d648f55b24a0e910b56a85a
git rev-parse HEAD
node --version
node --input-type=module <<'NODE'
import { LOD } from './src/objects/LOD.js';
import { Object3D } from './src/core/Object3D.js';
import { PerspectiveCamera } from './src/cameras/PerspectiveCamera.js';
import assert from 'node:assert/strict';
const cases=[
 ['P1',.1,false,[80,95],[0,0]],
 ['P2',.1,false,[120,95],[1,1]],
 ['P3',.1,false,[80,100,95],[0,1,1]],
 ['P4',.1,false,[120,90,95],[1,1,1]],
 ['P1-0',0,false,[80,95],[0,0]],
 ['P2-0',0,false,[120,95],[1,0]],
 ['P3-0',0,false,[80,100,95],[0,1,0]],
 ['P4-0',0,false,[120,90,95],[1,0,0]],
 ['unknown-N',.1,false,[95],[0]],
 ['unknown-F',.1,true,[95],[1]],
 ['below90',.1,false,[120,89.999,95],[1,0,0]],
 ['zoom',.1,false,[[95,1],[95,.9],[95,1],[95,1.1],[95,1]],[0,1,1,0,0]],
 ['query-raw-v-effective',.1,false,[[80,.8]],[1]],
];
let failures=0;
for (const [name,h,initialF,seq,expected] of cases) {
 const lod=new LOD(), n=new Object3D(), f=new Object3D(), cam=new PerspectiveCamera();
 lod.addLevel(n,0,0); lod.addLevel(f,100,h);
 n.visible=!initialF; f.visible=initialF;
 lod.updateMatrixWorld(true);
 for (let i=0;i<seq.length;i++) {
  const [d,z]=Array.isArray(seq[i])?seq[i]:[seq[i],1];
  cam.position.set(0,0,d); cam.zoom=z; cam.updateProjectionMatrix(); cam.updateMatrixWorld(true);
  const before=[n.visible,f.visible];
  const queryBefore=lod.getObjectForDistance(d/z)===f?1:0;
  const queryPreserved=before[0]===n.visible&&before[1]===f.visible;
  lod.update(cam);
  const level=lod.getCurrentLevel(), raw=lod.getObjectForDistance(d)===f?1:0;
  const effective=lod.getObjectForDistance(d/z)===f?1:0;
  const receipt={name,h,i,d,z,x:d/z,before,queryBefore,queryPreserved,level,visible:[n.visible,f.visible],raw,effective,expected:expected[i]};
  console.log(JSON.stringify(receipt));
  try {
   assert.equal(level,expected[i]); assert.deepEqual(receipt.visible,[level===0,level===1]);
   assert.equal(queryBefore,level); assert.equal(effective,level); assert.ok(queryPreserved);
   if(name==='query-raw-v-effective')assert.equal(raw,0);
  } catch(err) { failures++; console.error(err.message); }
 }
}
if(failures)process.exitCode=1;
NODE
```
반전 기준: P4 frame2에서 N, P3 frame2에서 N, 또는 동일 초기화 하에서 P1/P2/P3/P4 final이 N/F/F/F와 다르면 원판 추적 재검토. stdout을 JSONL 그대로 저장; 오류·실패도 제외하지 않음. QUnit L143–147 TODO와 자체 검산은 서로 다른 증거. 새 사용자 체감/프레임 검사는 별도 설계(같은 자산, 경계 진동 입력, 시각·전환 이벤트·frame times, renderer, zoom, GPU, 비교 h=0/0.1 필요).