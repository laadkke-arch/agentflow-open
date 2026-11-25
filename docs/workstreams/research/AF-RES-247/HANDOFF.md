# AF-RES-247 HANDOFF

## 상태: PARTIAL
지정 모델 3개와 9개 목적별 반환 후보, 전체 트리 10개 직렬화, 읽힌 9개 JSON의 소비 참조 및 25개 고유 원자료를 기록했다. 그러나 AnisotropyBarnLamp GLB 실제 JSON chunk는 확보하지 못했고, 동일 변형 렌더·오프라인 실행 영수증은 0/9. 실제 외부 URI GLB fixture도 확보 못해 규범 예와 명시적으로 구별했다. 자료 하한(8/6/5/6 ≥ 7/4/5/5)은 충족. 실제 렌더 실패라고 판정하지 않음.

- 배정 브랜치: `work/research-af-res-247`
- 착수 통합 SHA: 25201d7f3b727e1efb738bef210e92610cf9df92
- 배정·선행: 최신 control blob 2ccda40f65847c98b4ce293bd9aafe7ae15eb9fb, RUNNING attempt1, 234 DONE / result_commit 6513921a9aa6f05b7424b4862700daea230d8f9c (234 자체 PARTIAL). 요청의 계획판 7369707441e2eb70e84004ca6cb3bfeefc8b4061 기록; 전체 계획판 diff는 미실시. 238–242 미사용.
- 고정 자산 SHA: e124e8d8d7330a5372bc2b4d00d39a4a9d7997ea
- **결과 SHA: f82aaf0beb0456164253ec17cf494ef741ade353** (HANDOFF 직전; 이 SHA의 결과를 고정 입력으로 사용)
- [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/f82aaf0beb0456164253ec17cf494ef741ade353/docs/workstreams/research/AF-RES-247/RESULT.md) 필수 9/8 행, Q1–7 및 3 약점; [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/f82aaf0beb0456164253ec17cf494ef741ade353/docs/workstreams/research/AF-RES-247/SCOPE.md), [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/f82aaf0beb0456164253ec17cf494ef741ade353/docs/workstreams/research/AF-RES-247/sources.jsonl), [assets.csv](https://github.com/laadkke-arch/agentflow-open/blob/f82aaf0beb0456164253ec17cf494ef741ade353/docs/workstreams/research/AF-RES-247/assets.csv), [references.csv](https://github.com/laadkke-arch/agentflow-open/blob/f82aaf0beb0456164253ec17cf494ef741ade353/docs/workstreams/research/AF-RES-247/references.csv), [bundles.md](https://github.com/laadkke-arch/agentflow-open/blob/f82aaf0beb0456164253ec17cf494ef741ade353/docs/workstreams/research/AF-RES-247/bundles.md), [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/f82aaf0beb0456164253ec17cf494ef741ade353/docs/workstreams/research/AF-RES-247/SELF_CHECK.md).
- 변경은 owned_path 안뿐이며 dot-control.json 변경하지 않았다. 사용자가 지정한 ①–⑤ 단계의 커밋을 분리했으며 여러 파일 단계는 connector 단일 파일 커밋을 사용했다: scope 1a26ce785146d22b559b95e5e516d64aa09e3dca; ledger 4f7bab7f41183e17102c1c5f77d6c2f780f3369e; inventory e86d3ebe88c26ac0d8d6d29f3853300ba2c721e1; refs c220f496b5291a5426dc487c562bb76e8992d3f6; initial result 48e0d778c2e05eab36012d936359e05d09465bbf; counterexample 9091c7c7573b45171a80cb806be71c4c091f51aa 및 후속 보정; final RESULT 9c691f49c7bb494412123beb423ce1b785cdd9d0; SELF_CHECK/result SHA 위와 같음.

## 고정 결과 재개봉 검사 (시행함)
GitHub connector에서 위 결과 SHA의 7개 필수 파일 본문 모두 다시 읽고 구조 검사했다. 84 JSONL rows / 84 unique IDs / 76 성공 / 8 실패(F01–F08), counted 25 distinct works / 16 lineage IDs. CSV assets 52×13 및 references 284×11 데이터 행, source_id 미해결 0. RESULT 첫 두 표 각각 9×6, 8×5, 마지막 3×4, Q1–7 존재; bundles 9행. 고정 자산 링크 및 구성한 raw 링크의 경로를 inventory/ledger와 대조, 미대응 0(링크 실시간 fetch 검사는 아님). 통합 base와 결과 SHA 비교 13 commits ahead, behind0, changed 7 files 전부 owned_path. 원본 파일 보존; independent review 미실시. 이 HANDOFF는 마지막 단독 커밋.

## 핵심 판단
- Box/BoxTextured GLB 내부 JSON/BIN 직접 판독 및 C01–03: 외부 BIN 648/840 B, PNG 3750B와 해당 Embedded/GLB payload 바이트 일치; 화면 동일성은 별도. GLB 확장자만으로 외부 의존 0 보장 불가(N01).
- Lamp PNG와 KTX2는 같은 geometry BIN blob, metal 6 textureInfo→4 images; 5 optional material extensions, KTX2 variant basisu required/no core source. PNG 별도 변형은 자동 fallback 아님. GLB는 7,833,440B tree만 확인; F01/F07/F08 응답 실패(UTF-8 경로 포함), invalid GLB 증거 아님.
- 이미지 존재≠선택됨≠접근 안 함. L06/07 C13 unused 반례와 L05 eager read. EPUB local media 두 출판물 OPF→XHTML/SMIL, 원격은 EPUBCheck fixture와 규격만 확인. license/author metadata vs 실제 payload 구별.

## 재개 첫 행동 및 정확한 입력 (미실행)
우선 허용된 실행 담당 환경의 임시 작업 디렉터리에서 실제 대형 GLB를 바이너리 그대로 내려받고 고정 blob을 검증한다. 아래는 실행 명령; 이번 웹 연구가 실행한 명령이 아니다. 사용자 repo나 통합판 수정 금지.
```sh
git clone --no-checkout https://github.com/KhronosGroup/glTF-Sample-Assets.git samples
git -C samples checkout e124e8d8d7330a5372bc2b4d00d39a4a9d7997ea
git -C samples rev-parse HEAD
git -C samples ls-tree -r -l HEAD -- Models/Box Models/BoxTextured Models/AnisotropyBarnLamp
git -C samples hash-object Models/AnisotropyBarnLamp/glTF-Binary/AnisotropyBarnLamp.glb
python3 - <<'PY'
from pathlib import Path
import struct, json, hashlib
root = Path('samples/Models')
for m, expected in [('Box',1664),('BoxTextured',5956),('AnisotropyBarnLamp',7833440)]:
    p = root/m/'glTF-Binary'/(m+'.glb')
    b = p.read_bytes()
    magic,ver,n = struct.unpack_from('<4sII',b)
    assert magic == b'glTF' and ver == 2 and n == len(b) == expected
    off=12; chunks=[]; doc=None
    while off < len(b):
        length,kind=struct.unpack_from('<I4s',b,off)
        off+=8
        assert off+length <= len(b)
        chunks.append((kind.decode('ascii'),length))
        if kind == b'JSON':
            doc=json.loads(b[off:off+length].decode('utf-8'))
        off+=length
    assert off==len(b) and doc is not None
    print(json.dumps({'entry':str(p),'bytes':len(b),
      'sha256':hashlib.sha256(b).hexdigest(),'chunks':chunks,
      'buffers':doc.get('buffers',[]),'images':doc.get('images',[]),
      'textures':doc.get('textures',[]),'extensionsUsed':doc.get('extensionsUsed',[]),
      'extensionsRequired':doc.get('extensionsRequired',[])},ensure_ascii=False))
PY
```
예상 git blob Lamp c402216f49148c10267391430391b505594d6305. Box JSON988/BIN648, BoxTextured JSON1336/BIN4592, image0 view3 offset840 len3750; Lamp JSON/BIN 예상치를 임의로 채우지 말 것. 반환 JSON 내 URI가 external이면 전이 자원 및 파일 byte hash 보충; no external URI이고 모든 view bounds 유효하면 정적 폐쇄 후보로 갱신. core URI 외 확장 URI도 검사. 영수증: 실행 명령, pinned repo SHA, asset path, git blob SHA, SHA256, byteLength, chunks, JSON output, exit code 및 원 로그.

두 번째: 같은 자산 버전·직렬화의 실제 loader 비교. 실행 입력은 assets.csv 고정판 10 entrypoint이며 우선 Box/BoxTextured GLB, Lamp PNG/KTX2/GLB를 별도 행. Three.js 고정 084ec06444244980752a420f0e1af5cd8f112aa1의 GLTFLoader.js/KTX2Loader.js를 사용; 필요한 환경/fixture 작성은 실행 담당에게 남김. 예시 명령:
```sh
git clone https://github.com/mrdoob/three.js.git three
git -C three checkout 084ec06444244980752a420f0e1af5cd8f112aa1
find three/examples/jsm/libs -iname '*transcoder*' -o -iname '*draco*'
python3 -m http.server 8765 --bind 127.0.0.1
```
로컬 HTTP server와 미리 설치한 Playwright/브라우저 사용; harness는 아직 없음. HTML import map의 three=/three/build/three.module.js, three/addons/=/three/examples/jsm/로 지정, GLTFLoader.loadAsync('/samples/Models/<model>/<serialization>/<file>')를 호출, KTX2Loader는 setTranscoderPath('/three/examples/jsm/libs/basis/') 및 detectSupport(renderer) 후 setKTX2Loader. Draco decoder는 위 find 결과 실제 경로 확인 후 설정. 브라우저 route에서 localhost:8765 외 모든 HTTP(S) 차단, fresh context/no cache, 요청·response/failure, console, loader result, draw primitive/vertex count, screenshot을 저장. 카메라·viewport·light·renderer·color/tone map·GPU/browser 버전 고정; 제작자 A03 Studio Neutral 및 ACES Hill 환경과 camera의 정확한 파일/버전 확인 전에는 작성자 화면 재현이라고 부르지 말 것. 
통제 입력:
- BoxTextured glTF 원본 → 복제 JSON에서 /materials/0/pbrMetallicRoughness/baseColorTexture만 제거(단, unused image 항목 유지) vs 원본에서 BoxTextured0.bin만 제거. 전자는 UV/기하 동일, 외관 및 fetch 차이, 후자는 기하 도달 실패 예상. PNG byte와 UV는 고정. 
- Lamp PNG J06 vs J07 KTX2: decoder 미설정/설정, KTX2 no core source → 미설정 required 실패 예상. N02 fallback 예를 별도 시험 모델에 적용(원본 수정 금지); core source PNG가 있는 optional 조건에서 loader 지원 여부만 변경. fallback과 PNG 별도 variant 혼동 금지.
- Lamp PNG 동일 bytes에서 anisotropy extension 사용만 비활성화; 기하 동일 예상, 방향성 반사 비교. Renderer가 optional effect를 무시해도 오류인지 degradation인지 분리.
- 규범 N01 외부 URI GLB: 별도 유효 fixture 검색하거나 spec example로 테스트용 생성(새 fixture임을 표시); external URI가 필요한 buffer를 소비하게 하여 네트워크/파일 차단 전후 요청/기하 결과 대조. 실제 fixture 미확보 상태를 임의 보정 금지.
- EPUB: E03–E11 fixed publication OPF/XHTML/SMIL + assets로 reader 실제 MP4/WebM 선택, audio fragment/clip, network blocked log 확인. E12–17 example domains는 validator fixture일 뿐; remote-media 실제 책을 새로 고정 확보해야 한다.
영수증 한 행 단위: entry SHA+serialization+scenario+loader build SHA+decoder configuration+runtime environment+asset manifest SHA256+network policy+requested URIs/status+load/draw result+pixel artifact+exit status/log; 반전 조건은 RESULT 마지막 표. offline 성공은 동일 변형, 해당 목적, 새 context, 외부 요청 차단에서 실제 기능 성공이 필요. 단순 로드 완료/validator zero errors는 불충분.

## 색인 제안
AF-RES-247: prior art 반환의 resource closure/consumer reference/loader capability/fallback/URI delivery evidence 묶음으로 색인. 234의 지도 역할 및 바이트/선택 분리와 연결하되 엄격 공석을 채운 사례로 간주 금지. 3D 모델/EPUB 소비 경로에 대한 독립 근거이며 후속 설계의 확정 schema 아님. 재개 우선순위 Lamp GLB binary→정적 closure→동일 변형 offline receipt.
