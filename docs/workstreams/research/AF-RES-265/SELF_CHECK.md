# AF-RES-265 자기 점검

작성자가 두 실행 회차·자료 하한·반례·문서 링크를 다시 대조했다. 제3자 또는 별도 모델의 독립 검토는 미실시다. 아래의 다음 시험은 남은 일반화와 원인 확인에 해당한다.

| 질문 | 원근거와 위치 | 자기 결론을 깰 관측 또는 찾아본 사례 | 남은 미확인과 첫 확인 |
| --- | --- | --- | --- |
| Q1 | [입력 manifest](receipts/input-manifest.json) 세 GLB의 tree blob·git_cat_file_size·raw SHA-256, [파서](receipts/python-static.json) glb/headerHex/chunks/buffers | Lamp 원문이 크기와 다르거나 외부 URI가 있는지 실제 바이트로 탐색. BoxTextured·Lamp의 미참조 buffer 꼬리는 chunk pad가 아님을 정정. N01, A02/A16/A20 | 표본 밖 모델·후속 commit에서 head 트리/원본 바이트를 동일 명령으로 다시 비교 |
| Q2 | [chunks.csv](chunks.csv) 13 primitive의 POSITION/indices, [브라우저 배열](receipts/round-2/Lamp-G.json) `/outcome/geometry` | L08 stride 32 B, 같은 Box 계열의 순서 있는 POSITION 지문 차이. 본 모델별 GLB/외부 배열과 최소 기하 6/6 대응 고려 | sparse/Draco와 UV/tangent 자체의 바이트 동일성은 범위 밖. 필요 시 지정 accessor와 decoder를 추가 |
| Q3 | [Lamp 장면](receipts/round-2/Lamp-O.json) `materials/decode/draw/frame`, [프레임 차이](frame-diffs.csv), 저자 A01·N03 | 같은 mesh에서 anisotropy 제거로 PNG 1개·픽셀 18,884개 변화(≥3), 로고 링크 제거. 투과 pass가 draw 통계를 바꾼다 | 각 shader의 texel 기여, 작성자 Studio Neutral/ACES 재현 미실행. 같은 HDR/카메라 판을 고정해 두 실행 비교 |
| Q4 | [O 2회 예](receipts/round-2/BoxTextured-O.json) `paths/serverHttp/browserHttp`, [차단 probe](receipts/round-2/offline-probe.json) | X02 GLB+external.bin에서 파일 결손 onError. 같은 200 뒤 `finish` 또는 `ERR_ABORTED`가 나오는 종료 추적 반례 | Chromium 종료 이벤트 차이의 원인 미확인. CDP requestId와 바디 소비를 연결한 뒤 route가 없는 loopback 비교 |
| Q5 | [PNG/KTX2 원필드](receipts/python-static.json), [WASM 누락](receipts/round-2/ktx-wasm-absent.json), [양쪽 source 결손](receipts/round-2/fallback-ktx-absent.json), N02/N04/L01–L07 | 같은 required JSON에서 미등록은 onError이고, 등록했지만 WASM이 없으면 200인 KTX2가 decode에 실패하며 onLoad 이후 저하. X03에서 core source도 재시도하지 않았다 | 고정 Three 밖의 fallback/코덱 결과 미확인. 독립 viewer에 같은 모델과 decoder 출력을 공급 |
| Q6 | [unused-present](receipts/round-2/unused-present.json)와 [referenced-absent](receipts/round-2/referenced-absent.json), [validator](receipts/validator.json) calls, N01·X01–02 | 같은 픽셀인데 0 요청과 PNG 404라는 서로 다른 경로를 확인. 보조 검증기는 unused 이미지를 읽었다. 합법 GLB URI에서 외부 BIN 결손은 전체 실패 | 타 로더 eager 전략 일반화 미실행. 원 fixture와 같은 파일·render 조건으로 해당 로더 실행 |
| Q7 | [EPUB 판독](receipts/epub-read.json) 두 추출의 `opf/manifest/spine/references`, E02–10, [빈 폴더](receipts/clean-replay.json) | p20 두 영상이 실제 들어 있어도 어느 하나를 선택했다는 단서가 아니다. C03–C04의 대안 두 개 모두 원격인 반례 | 원 배포 ZIP과 reader의 실제 선택은 표본 밖. 고정 배포물과 reader를 별도로 구해 첫 영상 요청과 픽셀 비교 |

- 표 1은 18×6, 표 2는 13×5, 맨 끝 표는 3×4이고 Q1–Q7이 이어진다. 18개 주검사 행을 고정 raw URL·실행 JSON으로 연결했다. 프레임 12/12, O의 원 GLB 단독 모델 자원 6/6, R/O 픽셀 일치 6/6, G loader 배열 6/6. 정상 이미지 공석 6회, geometry-only draw 적용 대상 밖 6회, 주검사 입력 미수신·미실행·필수지표 미확인 각 0회. 관측된 진단 종료 이벤트는 원로그와 표에 표시했다.
- 추가 30회는 정상 20·재질 저하 6·실패 4. 의도한 HTTP 결손은 실제 404이며 접근 미수신과 구분했다. 두 파서 7/7 직렬화, 13/13 primitive, GLB 3/3, validator와 EPUB 2/2 추출을 대조했다. 두 번째 빈 폴더의 48회+2 probe에서는 요청·판정·프레임이 일치했고 종료 방식과 한 저하 조건의 draw 콜백 순서가 달라졌다. 실험·재생·수정 probe 분모를 별개로 둔다.
- 원자료 57행 중 직접 접근 성공 54, 실패 3. 산입 원저작 25개 및 18개 계보. 자산 7≥7, 규범/공식 5≥4, 구현/검사 8≥6, 소비 사례/출판 5≥4. Box/BoxTextured의 공통 cube 계보와 Lamp PNG/KTX2 재인코딩, EPUB의 같은 권 파일은 보수적으로 중복을 제외했다. 합성 X01–04와 실패는 하한 밖이다. [원장](sources.jsonl)
- 소유 디렉터리는 `docs/workstreams/research/AF-RES-265/` 하나다. 계약 핀은 직접 의존 247의 result SHA를 사용했다. SCOPE의 사전판, 결과판 링크와 마지막 인계 커밋을 분리했다. 새 폴더에서 재생을 확인한 코드와 산출물 고정판은 인계에 있다. [계약](session.json), [범위](SCOPE.md), [재생](replay.md)
