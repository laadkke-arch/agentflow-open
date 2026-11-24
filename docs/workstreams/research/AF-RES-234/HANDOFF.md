# AF-RES-234 HANDOFF

**상태: PARTIAL** — 자료량 기준은 충족했으나 사전 표집 규칙의 실제 적격 6자리 채택 0/6(확정 공석 3 + 공식 full style JSON 미확보 3). 코드 후보 3 및 OSM Bright 대조군 3은 정식 표본에 합산하지 않음. 실제 통제 렌더링 0/4, offline 성공 영수증 0. 자기 점검 시행, 독립 검토 미실시.

## 고정 입력과 결과
- 통합 착수 SHA 610bcdf35a3dc04bc7f55ce1ecf0a339d9d881e6, 47차 계획판 914dbfa789ebec97063ed97130ea2a71c2e9f503, 착수판에서 234 RUNNING attempt1/depends 223 추가 확인. 계획판엔 234 없음. 223 중앙 DONE, 고정 HANDOFF 27518e859181f0ece5de42dc54844d5b83688b7a 내부 PARTIAL 유지. 227–229 자료 사용 안 함.
- MapLibre style/tree 601ae60796ceceda2cbd2ed3d2ea92d17a84be4b, Protomaps generator/tree 42ffaaa4a85a41bfcb23e43cc0f5b492a5eca123, assets 028c18f713baecad011301ff7a69acc39bcc2ae7, GL JS source/tests edbe4866e964d3b9346c9e696ea47e54b59b69cb, EPUB samples 7651e2002b631e6577fadf7e9e0692fa6efb8746. 각 고정판 Git 파일 조회와 당시 실제 배포는 구분.
- 결과 SHA **273d94fc4c65b25d4a0b3c7739d0000e801d28e7** (HANDOFF 직전 고정판), branch work/research-af-res-234.
- ① 46dd18370b65172743d2106009e5bedf304418b5 SCOPE 사전 봉인, ② e0ea76fb6b88bb5b19ad9ab2014a1b7adacfd602 원장, ③ fe729dd86deea53acc4b922494acbd161bd3e68b 표/자산, ④ 17350c798ad6b4b7f4f29235ea37ac64ee48b562 반례/조합, ⑤ 273d94fc4c65b25d4a0b3c7739d0000e801d28e7 RESULT/SELF_CHECK. ⑥ 이 문서 단독 커밋.

## 대표 파일과 확인 결과
- RESULT.md 첫 두 표(6/4행), Q1–Q7, 마지막 3약점. layers.csv 12행(엄격6+OSM3+World3), resources.csv 21행, bundles.csv 33행, examples.md 지도/EPUB 대조, sources.jsonl 70행, SCOPE.md, SELF_CHECK.md.
- 원장 고유 source_id 70, 실패 7, 산입 고유 work_id 45 (제작자25, 규격/로더/시험6, 소비자9, EPUB5), 산입 lineage_id 15. 독립 실험 0, 구별 사례 6. 개별 처음 열람 UTC 미복구, 시간창 사용; Git commit date와 file 최초 발행일은 다름.
- 고정 결과 SHA에서 위 8개 파일 직접 재조회 모두 비어 있지 않음. 원장 JSON 파싱 성공, 모든 명시적 source ID 토큰 대조 결과 누락 0; RESULT 표 정확한 열/6·4·3행, Q1–Q7 확인. CSV data rows 12/21/33. 통합 시작 SHA 대비 ahead 5, behind 0, 추가 파일 8개 모두 owned_path 내부, dot-control.json 변경 없음. 이것은 정적 자료·구조 확인이며 실제 브라우저 렌더 검사는 아니다.
- MapLibre 엄격 Debug는 raster/hillshade 2개 layer: 세 역할 공석, 숫자 9는 실제 PNG. OSM 보조 M09 실제 tile poi id40551996 class=school rank32 Point -> school_11 index M10 (85,123,17,17) -> M11 atlas; waterway id143789705 Inn -> M12 0–255 실제 PBF glyph U+0049/006E. P 코드 arrow -> P08/09 실제 index/atlas; 주소 합성 12 -> P13 실제 PBF digits(실제 주소 미확인). P08/P10 동일 index blob과 P09/P11 다른 atlas blobs, M15/P08 없는 이름 0; runtime injection 별개. EPUB E03–E05 manifest/CSS/TTF와 E06–E08 시스템 font 대조. C09 Athens expected PNG는 게시 시험 기대, 실제 offline 실행 영수증 아님.
- 약점 세 가지: (1) 엄격 6자리 결측/공석, (2) runtime 선택·DPR·tile bounds·missing image·local glyph 미실행, (3) Protomaps mutable build/배포 SHA·EPUB reader 실제 선택 미확인. RESULT 말미의 반전 조건을 따른다.

## 다음 첫 행동 / Codex 인계
1. **첫 행동:** 공식 Protomaps viewer https://maps.protomaps.com/ 의 Get style JSON에서 version 5.7.2, flavor light, lang en, 정확한 source/tileset 조건을 기록하고 내보낸 원본 JSON/hash/배포판을 확보한다. 아래 versioned array endpoint 실패는 이 연구 환경의 접근 실패(F01)이며 삭제/404를 뜻하지 않는다. JSON이 얻어져도 array-only이면 root/full JSON과 구별. 같은 판 대응 증거가 없으면 PARTIAL 유지. 실제 공석 Debug를 후순위 OSM으로 교체하지 않는다.

실행 가능한 명령/입력(여기서 실행하지 않음; 승인된 격리 환경에서만 의존성 설치, 다운로드·테스트):
```sh
git clone https://github.com/protomaps/basemaps.git
cd basemaps
git checkout 42ffaaa4a85a41bfcb23e43cc0f5b492a5eca123
curl -fL 'https://npm-style.protomaps.dev/layers.json?version=5.7.2&theme=light&lang=en' -o layers-5.7.2-light-en.json
cd styles
npm ci
npm run generate_style style.json https://example.com/tilejson.json light en
# 이 생성 결과는 placeholder source를 쓰는 비교용; 공식 배포판과 동일하다고 말하지 말 것.
# 실제 viewer export를 별도 파일로 받아 비교. 정확한 dated TileJSON/PMTiles source로 다시 생성.
jq -c '.layers|to_entries[]|select((.value.type=="background" and (.value.paint["background-color"]|type=="string")) or (.value.type=="fill" and (.value.paint["fill-color"]|type=="string")) or (.value.layout["icon-image"]!=null) or (.value.layout["text-field"]!=null))|{index:.key,id:.value.id,type:.value.type,source:.value.source,source_layer:.value["source-layer"],layout:.value.layout,paint:.value.paint,filter:.value.filter,minzoom:.value.minzoom,maxzoom:.value.maxzoom}' style.json
sha256sum style.json
```
generation command line은 고정판 P01/P06 README·package를 따른다. jq는 전체 적격 배열을 인쇄하므로 A/I/T마다 최초 index를 별도 선택. endpoint/live viewer와 source generator/asset commit 사이 차이를 보존. P01 source url TileJSON 입력 vs C04 PMTiles protocol URL 차이 검토. source PMTiles 실제 header/bounds/hash는 먼저 날짜 고정 build 목록과 대조; mutable 비교 후보 `pmtiles show https://latest.protomaps.com/v4.pmtiles` (설치된 CLI일 때) 결과를 조회 UTC 및 원 archive URI와 함께 기록. 전체 planet 약 120GB 다운로드하지 말고 사용 승인된 작은 extract를 택한다. exact release/build 주소를 확보하지 못했으므로 임의 생성 금지. P 주소/oneway 실제 피처가 있는 작은 extract를 선정해 buildings kind=address/addr_housenumber min18 및 roads oneway=yes min16 관측, source maxzoom/overzoom 분리.

2. MapLibre 원본 및 assets 고정:
```sh
git clone https://github.com/maplibre/demotiles.git
git -C demotiles checkout 601ae60796ceceda2cbd2ed3d2ea92d17a84be4b
git -C demotiles ls-tree -r --name-only HEAD | grep '\.json$' | LC_ALL=C sort
git clone https://github.com/protomaps/basemaps-assets.git
git -C basemaps-assets checkout 028c18f713baecad011301ff7a69acc39bcc2ae7
sha256sum demotiles/tiles-omt/14/8711/5744.pbf demotiles/styles/osm-bright-gl-style/sprite.json demotiles/styles/osm-bright-gl-style/sprite.png basemaps-assets/sprites/v4/light.json basemaps-assets/sprites/v4/light.png basemaps-assets/sprites/v4/dark.png
```
Pillow가 승인 환경에 이미 있으면 다음 crop 검사를 실행하고 SHA/픽셀 비교(파일 재배포하지 않음):
```sh
python - <<'PY'
from PIL import Image
from hashlib import sha256
for path,box in [
 ("demotiles/styles/osm-bright-gl-style/sprite.png",(85,123,102,140)),
 ("basemaps-assets/sprites/v4/light.png",(0,57,19,76)),
 ("basemaps-assets/sprites/v4/dark.png",(0,57,19,76))]:
 im=Image.open(path).convert("RGBA").crop(box)
 print(path,im.size,sha256(im.tobytes()).hexdigest())
PY
```
DPR2 별도 index+PNG 존재와 실제 요청 확인. MapLibre MVT에서 exact feature ids와 property/rank를 직접 검증하는 테스트, OSM waterway 문자열과 fixed PBF glyph 범위 테스트. C03 정상 진입점 demotiles/tiles-omt/index.html을 pinned JS/CSS 및 로컬 절대 resource URL로 수정한 별도 시험 사본만 사용. 카메라 [11.40416,47.26475] z14 및 z16; min16 전후, collision/placement 및 z14 tile overzoom 분리. Protomaps 정상 C04 examples/basic.html London [-0.12,51.5] z13에서 min16/18 이전과 이후 비교; C06 local.html Monaco 경로 실제 파일 위치 검증, remote CDN까지 로컬화. C08 Athens test expected의 당시 renderer/tiles 버전이 없으면 현재 재현과 역사적 생성판을 구분. 
3. 네 통제 단일 조건 변경: C1 격리 background #f8f4f0 또는 #cccccc, sources={}, glyphs/sprite 생략(전체 style에서의 사전 fetch와 분리); C2 known school_11/arrow vs af234_missing_zz, static index 및 styleimagemissing/addImage 등록 전후 차이, 이미지 오류/네트워크 로그; C3 같은 문자·font stack·camera에서 renderer 5.0.1과 glyphs 생략 지원 5.11+를 별도 판으로 비교하고 remote vs local, localIdeographFontFamily와 실제 local fonts 및 network range 확인; C4 OSM bounds [11,47,12,48] 내부 Innsbruck vs 외부 London, source tile 요청 기록 및 배경 유지 확인, P는 실제 fixed extract bounds 확정 후 안/밖 선정. 매번 browser renderer version/OS/local fonts/locale/DPR/viewport/style/tiles/assets hashes, request URL/status 및 screenshot, network 차단 시 성공·실패를 원자료로 저장. 기대와 반전: background isolated에도 source 필요하면 C1 재검토; 없는 이름이 등록 없이 해결되면 namespace/index 경로 검토; local 문자에 remote 요청이 계속되면 정책 범위 축소; bounds 밖 source 요청이 발생하면 viewport overlap/overscan 및 renderer 판 검토. Offline 성공은 네트워크 차단과 실제 정상 화면 증거가 있을 때만. EPUB은 동일 reader 판에서 OPF/CSS/TTF 연결, system-only title font inventory·실제 선택을 검증; font 재배포하지 않음. 해당 시험 자체와 독립 검토는 본 세션에서 미실시.
4. 후속 실행 worker에 별도 승인/계약이 필요한 경우 repo AGENTS/workbench 절차에 맞춰 manifest를 owned_path 안에 생성하고 contract check; 이 연구에서 설치/테스트/배포/새 API 키/계정 변경 안 함. 사용자가 승인한 실행 범위에서 `python scripts/cloud_check.py --environment codex-cloud --fetch-contract` 등 정확판 검사를 수행하고 결과를 기록. 점검용 `git diff --name-only 610bcdf35a3dc04bc7f55ce1ecf0a339d9d881e6 273d94fc4c65b25d4a0b3c7739d0000e801d28e7`는 API compare로 확인된 8 owned files에 대응한다.

## 색인 반영 제안
통합 담당자에게만 제안: AF-RES-234 PARTIAL, result_commit=이 고정 결과 SHA(그리고 HANDOFF 커밋 SHA 별도 기록), tag style-resource-bundle / source-layer / sprite-atlas / glyph-policy / offline-reproduction / epub-font; six-slot strict empty/missing 분리, OSM contrast, code projection flag, evidence lineage, 4 controls execution unobserved. 다음 action은 공식 Protomaps full JSON+same-version 검증 후 fixed tile feature·runtime controls. 자료 수 충족만으로 DONE 전환 금지. dot-control.json/중앙 상태/색인 직접 변경하지 않음.
