# AF-RES-255 자체 점검

| 질문 | 원근거와 실제 확인 위치 | 반증을 찾은 곳과 결과 | 미확인·경계 |
|---|---|---|---|
| Q1 | W01/W01R, W02/W02R의 SHA·link, W03·W04·W09·W10 및 `manifest.json` | 고정 `css/css-text` 3,183경로에서 002 전 2,637경로를 다시 확인. 구조 검사에서 1,182개 declared reftest·482개 Ahem marker, balance와 Ahem을 겸한 앞선 reftest 0 | 스크립트가 동적으로 조립해 불러오는 자원은 미확인. 원래 지명 유지 |
| Q2 | W06/W06F, W07/W08, S04, B04·B07·B09·B12, `env.json`·`receipts/setup/versions.json` | 실제 driver와 MiniBrowser의 일치 판, WPT SHA·TTF SHA를 확인. 포트·TLS, libexec와 eager timeout을 분리한 뒤 정상 실행에 도달했다. 404에서 `FontFace.error`와 국소 레이아웃 변화를 확인 | WebKitGTK FontFaceSet DOM `loadingdone` callback의 직접 수신 0, 별도 HTTP·resource·face 성공은 4/4. 공개 API 및 GCS 경로 X02/X03 결과 미확인 |
| Q3 | W01/W01R, W02/W02R, W05·W07, `receipts/primary/` | 각각 raw `test_end`와 보고서 status, 관계·URL 및 PNG decode와 pixel diff 확인. 002의 cut 2와 cut 3이 모두 불일치 | 설정 실패는 기본 슬롯과 다름. 8기본 중 timeout·FAIL 관측 0 |
| Q4 | S03/S04, W06, `measure.js`·`words.csv`·`receipts/geometry/` | nested inline과 plain의 각 Range 및 word index의 같은 cut을 확인. Chromium 003에는 동일 픽셀과 공존하는 소수 폭 차이. r1/r2 좌표·폭·폰트 해시 재비교 | 해당 LTR ASCII 표본의 y 기반 분류. 글자 선택의 복잡한 fragment·수직 writing mode는 범위 밖 |
| Q5 | S01·S02·S05B, B01–B03·B06·B13, 두 `controls.json` | W7을 exact fit, +1/64 및 +1 CSS px로 흔들어 순수 max-line 최소 해석을 뒤집음. C1 강제 오른쪽 chunk가 Chromium에서 minvar 예상과 어긋남 | 런타임 내부 분기, Debian의 전체 빌드 플래그 및 브라우저 일반화 미확인 |
| Q6 | V01–V04와 X01, 두 `captions.json` | DCMP의 문법 예와 명시 시간표가 다른 목표를 준다. 두 엔진에서 한 cue의 표시 줄을 변경하고 원행·시간·구간이 유지되는 실제 예를 찾음 | 원 BBC 접근 제한. overlay·음성·독자 선호는 적용 대상 밖 |
| Q7 | S05H·S05P, B10/B11, `COUNTEREXAMPLES.md`, `receipts/replay/comparison.json` | 002 대체 cut, Chromium 003의 Ahem 없는 픽셀 일치, 003 엔진 간 diff, C1과 003 새 프로필 재생에서 반증을 탐색 | 공개 과거 제출 미확인. 가림 독립 정확도와 별도 독립 검토는 시행하지 않음 |

## 분모 검산

- 원형 계획 8, 정규 runner 판정 8, 이미지 쌍 8, 별도 기하 8, 결측 0. 반복을 접은 build×test 조건 4/4를 관측했다. 공개 작품은 두 시험이며 반복과 참조는 별도 독립 사건이 아니다. 232의 관측 0/4와 이 작업의 로컬 관측은 다른 층이다.
- 단어 fragment는 주 시험 96/96, 내장 비교 36/36, 외부 참조 132/132다. `words.csv` 총 264행이다. 모든 선택된 단어에서 fragment 하나를 관측했다. 003의 두 초록 블록은 한 원형 시험에 속한다.
- 합성 기본 조건 16/16, exact-fit·폭 감도 10/10, 002 대조 입력/참조 6/6, 폰트 실패 4/4쌍, native VTT 2/2로드 및 선택 cue 4/4, cue 폭 측정 8/8이다. 셸/runner 준비 오류, 새 프로필 재생과 앞서 두 차례 조회한 같은 자료는 이 집계에서 별도 층이다.
- `sources.jsonl` 43행 중 직접 산입한 고유 원저작 27개, lineage 12개다. 원저작은 WPT/규약/폰트 9, 엔진 구현·배포 및 제작자 9, CSS/결정/232 5, 자막 4다. 002/003의 참조와 232 원표, 동일 구현의 판별 지문은 보조 행이다. 접근 실패는 3행이고 산입 0이다. WPT 공개 이전 제출 획득 0이며 모집 존재 여부와 분모는 미확인이다.
- 002/003은 기대가 이미 노출된 상태에서 시작했다. 가림 적중의 적격 분모는 정상 공석 0이다. 인간의 가독성 연구 분모는 적용 대상 밖이다. 픽셀 차이 0은 실제 값으로 기록한다.

자체 점검에서 표 1의 8행·6열, 표 2의 13행·5열, 마지막 약점 표의 3행·4열을 각 원행과 연결했다. 원형과 폰트 실패와 별도 기하의 스크린샷 비교 출처를 확인했다. 인계 직전 결과 커밋의 재열기, 저장소 검사 범위 및 새 프로필 결과는 `HANDOFF.md`에 해당 결과 SHA와 연결한다. 별도 독립 검토는 미실시다.
