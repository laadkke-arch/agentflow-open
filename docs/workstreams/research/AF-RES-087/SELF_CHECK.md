# AF-RES-087 자가검산

| 질문과 주장 | 원문/실행행 | 틀릴 사례를 찾은 경로·발견 또는 공석 | 판단을 바꿀 최소 확인 |
|---|---|---|---|
| Q1. 공간 정보의 의도는 geometry·CRS다. 정확한 열 순서까지 언급한 원 안내는 없다. | S01–S04·S06–S13·S20–S22, [원 assert/skip](evidence/upstream/notes.md), [실측](evidence/upstream/receipts.json) | 원 안내 앞뒤에서 “any version” 직전 1.0.0을 찾았다. `check_like=False`로 열 순서를 요구하는 시험은 존재한다. GDAL 3.5.0의 실제 0.3.0/WKB가 양쪽에서 읽혀 writer 목록 = reader 목록 가정을 반박했다. N은 1.1.0 쓰기 능력이 추가되어도 WKB 기본값이 1.0.0이었다. | 실제 독자가 인용한 원 절과 당시 계약을 확보해 열 순서도 해당 목적에 포함됐는지 확인. |
| Q2. O/N은 태그의 동결 코드와 동일 resolved 의존 스택으로 실행했다. | S28–S31, [환경](environments.json), [설치](evidence/build/installation.json), [L1–16](runs.jsonl#L1-L16) | editable 설치가 이름만 맞을 위험을 import 파일 경로와 Git HEAD·파일 hash로 검사했다. Shapely/PyArrow/GEOS/PROJ는 같았으나 벡터 I/O 기본 backend는 달라진다. CI 최소 request의 판 차이와 역사 배포 lock 공석을 남겼다. | 같은 네 SHA에서 한 번에 PyArrow 또는 Shapely 한 판만 교체. GDAL 입력 vector path가 문제면 동일 태그·데이터에서 engine만 고정 교체. |
| Q3. F2/F3는 metadata 판을 분리했고 F1/F2 및 F3/F4에는 동반 metadata 또는 물리 배치가 바뀐다. | S03–S05·S13–S16·S20–S28, [writer·footer](files.csv), [diff](evidence/build/footer-differences.json), [data SHA](evidence/build/data-sections.json) | file hash가 다르면 data 값도 다르다는 가정을 검사했다. F1–F3 본문 bytes는 같았다. F1/F2의 creator·geometry Arrow 확장·pandas geometry 표시 동반을 보았다. F4는 storage 동반, 전체 bbox는 그대로, covering 열은 없었다. | writer 같은 상태에서 extension field만 제어한 WKB 쌍을 별도 만들어 제3의 extension 기반 consumer에 전달. |
| Q4. 14반환에서 두 계약이 성립했고 두 O 거절은 평가 불가다. | S09·S20–S21·S24–S27·S32–S33, [16자리](runs.jsonl), [D 축/CRS](evidence/auxiliary/D-axis-comparison.json) | 같은 box만 비교하는 편향을 다중 geometry 열과 (117,23)으로 깼다. CRS 문자가 달라도 XY에서 같을 수 있고 authority 순서로 넘기면 무한대가 나왔다. 명시 null에서는 두 reader가 성공 종료해도 공간 기준이 깨졌다. | 고정된 비대칭 EPSG:3857 또는 타원체, axis order·수치·CRS key 생략 조건을 대조해 default 오해를 확인. |
| Q5. 열기, 공간 보존, 엄격 속성은 분리되며 N native도 혼형 타입을 바꾼다. | [A–G 증거](evidence/auxiliary), S11–S12·S22·S34–S41, [F4 거절](evidence/reads/F4-O-1.stderr.txt) | plain Arrow 표는 geo 키를 갖지만 활성 geometry가 없다. B 한 칸 변화와 F dtype 변화를 포착했다. C null/EMPTY 합쳐짐은 고정 스택에서 발견되지 않았다. G는 동일 위상이고 Point→MultiPoint가 생겼다. 처음 F 보조의 오류는 harness·footer 단계에서 발생했다. 같은 bytes를 재실행해 reader 결과를 별도 남겼다. | 다른 진짜 consumer의 file hash와 지문을 확보하고, G의 Z/혼형 및 C를 reader의 Shapely 버전만 바꿔 검사. |
| Q6. 결과를 반환할 조건은 독자 목적에 따라 바뀐다. | S01–S02·S17–S19, [F2](runs.jsonl#L5-L8), [F4](runs.jsonl#L13-L16), [E](evidence/auxiliary/E-added.json), [B](evidence/auxiliary/B-cell.json)·[F](evidence/auxiliary/F-no-pandas-meta.json) | F4는 reader를 O로 제한하면 보류, 동일 제약의 F2는 유지. E에 새 열 허용만 바꾸면 수용, B와 F는 그대로 보류다. 이슈/PR에서 원 G04 문구의 하류 직접 실패 사례는 찾지 못했다. | 실제 인용·실제 파일·당시 reader의 한 묶음을 확보해 범위 문구를 바꿨을 때 선택이 바뀌는지 확인. |
| Q7. 파일판 및 표시 성공과 사용자가 요구한 기능의 보존은 서로 다른 관측이다. | S42–S55, [PDF reader 실제 순서](evidence/other/pdf-tag-order.json) | 색상은 Firefox 초기 실패와 Lilley 실제 성공을 찾았다. PDF는 같은 1.7/Tagged가 두 다른 순서를 보였고, Adobe 연속표에서는 최초 NVDA 성공 인용을 저자가 페이지 단위로 반박했다. 두 분야 다 원 규격과 독립 기록을 열었다. | 동일 입력을 고정 프로파일 또는 AT 판과 실제 디스플레이/음성 경로에 재생해 측정. GeoParquet에서는 좌표·CRS를 raw 수치로 추가 대조. |

## 원래 분모와 경계

- 생성 4/4, footer 4/4, 변화 대조 3/3, 동일 SHA로 O/N 대응 4/4, reader 셀 8/8, 서로 다른 프로세스 16/16. 각각의 비교 입력이 일치하며 표 2와 실행행은 1:1이다. 생성 실패·장비 오류·스킵은 주 격자에서 각각 0이다.
- 원 시험의 선택 48/48 통과를 dtype·CRS와 topology assert 범위로 읽었다. 선언된 skip 조건과 실제 스킵 0을 확인했다. 공식 fixture와 N의 복사본은 12/12 같은 바이트라 별개 출처로 세지 않았다. C·G의 서로 다른 입력, D와 PyArrow 표를 합친 보조 최종 20회와 F 계기 초기 실패 2회는 주 격자 밖이다.
- 원장 60행에서 연구 상속 5행을 제외했다. 55 산입행, URL fragment를 접은 문서 51개, 이후도 같은 guide의 고정판 둘, GeoParquet 규격 두 판, native 읽기·쓰기 PR과 그 구현, PDF PASS/FAIL fixture 등은 독립 원저작·사건 ID로 합쳐 35개다. 교차 프로젝트 소비 시험과 실제 사용 보고 8사건 중 보고는 6사건이다. 역방향·무변화·부분 보존의 근거 9사건, 분야별 원 적용/실패 각 2사건. 검색-only·접근 실패와 연구 산출물은 제외했다. [자료·시간·한계](sources.jsonl) · [시도 기록](attempts.jsonl).
- 봉인 결과와 주 격자의 방향은 일치했다. 사후에는 F1/F2의 metadata 차이, F3/F4의 storage 동반 변화, F의 dtype 변화, G의 혼형 geometry 승격을 별도 채웠다. `manifest.json`의 판·주 격자·기준 및 SCOPE의 hash는 처음 그대로다.

`python -B docs/workstreams/research/AF-RES-087/audit.py`는 파일·footer·해시, 판 지문, 두 반복, 원 시험, 보조 시험, 출처 분모와 표 순서를 검산한다. 결과 SHA를 고정한 뒤의 실제 종료와 원격 바이트 재열람 영수증은 인계에 붙인다.
