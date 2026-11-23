# V02·V03 보조 재생 및 V03 버전 민감도

## 판정 요약

단계 ② 봉인 `9b13473a76a381fe27d775524aa65416ec28f591`의 V02·V03 재생 계획에 따라 **Vega-Lite 5.1.0 / Vega 5.20.2**에서 여섯 A/B 변형을 실행했다. 다섯 SVG를 생성했고, V02 경계 B 하나는 원래 지정한 escape 제거 때문에 컴파일에서 실패했다. B를 고쳐 다시 그리지 않았다. V03은 A에서 목표 section 라벨 1개가 빨강·9개가 검정, B에서 10개가 검정이었다. 원격 봉인 예측과 비교한 여섯 N/I/D 행은 범주상 일치하며, I와 D는 두 요구 모두 동률이다. **이는 연구자가 고른 판의 보조 재생 결과다. 원작성자의 같은 판 출력 확인과 공개 후속 자료 배당에는 들어가지 않는다.**

| 고정 실행 | 실제 결과 | 봉인 예측과의 대조 | 증거 |
| --- | --- | --- | --- |
| V02 정상 A | 연구자 일반 이름 복사본의 16셀·48점·32축 제목·범례 제목 확인 | 값과 각 title↔field 대응 유지 | [SVG](outputs/V02-normal-A.svg), [셀별 검사](outputs/V02-normal-A.cell-checks.json) |
| V02 정상 B | A와 compiled JSON 및 SVG bytes 동일 | A/B가 같은 출력이라는 범주 예측 일치 | [SVG](outputs/V02-normal-B.svg), [출력 차이](output-differences.json) |
| V02 경계 A | 원문 특수 이름 데이터의 값 접근 유지. 32축 제목과 `Species.` 범례 제목에서 access escape만 제거 | A의 값·표시 분리 예측 일치 | [SVG](outputs/V02-boundary-A.svg), [셀별 검사](outputs/V02-boundary-A.cell-checks.json) |
| V02 경계 B | `Access path missing open bracket: Beak Depth (mm)]`로 compile 실패. SVG 없음 | 값 접근을 보존하지 못한다는 범주 방향은 일치. 빈 점 또는 잘못된 값이 그려질 것이라는 세부 출력은 관측하지 않음 | [실행 영수증](render-receipts.json), [실패 포함 stdout](logs/render.stdout.txt) |
| V03 고정 A | y축 10라벨 중 `4. Hygiene & Cleaning`만 빨강, 나머지 9개 검정 | 사전 1 red/9 black 및 라벨 identity 일치 | [SVG](outputs/V03-fixed-A.svg), [축 검사](outputs/V03-fixed-A.axis-checks.json) |
| V03 고정 B | y축 10라벨 모두 검정 | 사전 0 red/10 black 일치 | [SVG](outputs/V03-fixed-B.svg), [축 검사](outputs/V03-fixed-B.axis-checks.json) |

V02의 16·48·32는 실행 뒤 센 관측 수다. 이 수를 사전에 수치 예측했다고 소급하지 않는다. V03의 1/9/10은 봉인 예측에 있던 수다. 9개 정상 record와 1개 경계 record는 하나의 출력 안의 두 부분집합이다. N/I/D 여섯 행이나 여섯 renderer 호출을 독립 참가자·독립 표본 여섯 개로 세지 않는다.

기계 판독 요약은 [results.json](results.json), 봉인 카드별 대응은 [prediction-comparison.csv](prediction-comparison.csv)에 있다. 연구자 재생의 I-D 비교 분모는 요구 2개이며 동률 2, D 신규 정답 0이다. 역사적 작성자 동일 patch 확인은 0건이고, 이 재생이 새로 제공한 공개 후속 저작도 0개다.

## 고정한 입력과 실제 변경

수신 원문은 `streams/vega/cache/body-only.json`의 #7422·#7507 본문만 읽었다. 댓글·PR·후속 시험·사후 그림에는 접근하지 않았다. 본문에 있는 JSON을 파싱했으며, 코드 블록이나 editor 링크의 코드를 임의 실행하지 않았다. 입력은 inline 데이터뿐이고 외부 데이터·이미지 load를 실행기에서 차단했다. [input-extraction.json](input-extraction.json)에 본문·추출 객체 해시를 기록했다.

V02 원문에는 `$schema`가 없으므로 새 schema를 넣지 않았다. 경계 A는 원문 JSON을 그대로 사용하고 `fieldTitle` callback만 행동 옵션으로 공급했다. 공통 logger는 관측 도구이며 입력·표시 옵션이 아니다. 경계 B는 `repeat.row`, `repeat.column`, `color.field`에서 봉인된 정규식으로 access escape만 제거했다. 실패한 `]`를 지우거나 다른 필드명으로 바꾸지 않았다.

V02 정상 보조 입력은 경계의 세 데이터 record에서 literal key의 점·대괄호를 없애고 참조를 같은 일반 이름으로 바꾼 것이다. 원저자의 외부 정상 예제를 재현했다고 쓰지 않는다. 이 복사본과 경계 A의 각 셀에서 원본 값과 local point 좌표의 대응을 확인했다. 전체 화면의 전역 위치·글꼴 폭이 같다는 의미는 아니다.

V03은 원문 schema v2와 10개 record를 그대로 뒀다. A는 `axis.labelColor.condition.test` 문자열만 `datum.value === '4. Hygiene & Cleaning'`으로 바꿨고 B는 원래 `datum.resilience === 0`을 썼다. 실제 compiler는 schema 문자열과 별개로 5.1.0이다. 변환한 입력·공통 속성·실제 변경 위치는 [input-diffs.json](input-diffs.json)에 모두 있다.

## 환경과 무결성

[5.1.0 package](https://raw.githubusercontent.com/vega/vega-lite/v5.1.0/package.json)의 peer 요구는 Vega `^5.20.0`이다. [동일 tag yarn.lock](https://raw.githubusercontent.com/vega/vega-lite/v5.1.0/yarn.lock)의 `vega@5.20.2` entry를 직접 확인해 runtime 5.20.2를 선택했다. 원 lock의 transitive pin을 유지하고, 원 프로젝트 자체라 lock에 없던 `vega-lite@5.1.0` entry만 공식 npm metadata에서 덧붙였다. 설치 후 lock hash가 바뀌지 않았음을 확인했다.

실제 import는 Vega-Lite 5.1.0, Vega 5.20.2이며 Node host는 v24.22.3이다. [versions.json](versions.json)에 installed/imported package 판과 main 파일 해시를 보존했다. [dependency-pins.json](dependency-pins.json), [dependency-integrity.json](dependency-integrity.json)은 package/lock의 SHA256과 실제 tarball SHA1·SHA512 SRI 일치를 보여 준다. compiler와 runtime 두 tarball 모두 공식 metadata/lock의 integrity와 일치했다.

Yarn 1.22.10에 `--frozen-lockfile --ignore-scripts --ignore-optional`을 지정했다. native canvas는 설치하지 않았다. 고정된 vega-scenegraph 4.9.4의 `src/util/text.js` L7–27은 canvas context가 없을 때 글자 수·글꼴 크기로 폭을 추정한다. 따라서 이 결과는 색·필드 접근·SVG 구조 확인에 사용할 수 있지만 역사적 폰트 픽셀 폭·겹침 허용차·독자 가독성 실측으로 사용할 수 없다.

렌더 로그의 `warnings` 배열에는 logger를 통해 수집한 debug 메시지도 들어 있다. 5.1.0 compiler/render의 warn/error 로그는 없었으며, B의 실제 compile exception은 별도 `error`에 보존했다. 전체 render 명령 종료 코드 1은 이 한 실패를 숨기지 않고 반영한 것이다.

## 실제 출력과 예측의 차이 보존

완전한 expected SVG는 사전에 만들거나 봉인하지 않았다. [pre-render-review.json](pre-render-review.json)은 첫 실행 전에 이를 명시했다. 봉인한 것은 범주 예측과 V03의 색 개수다. 실제 compiler JSON·SVG·scenegraph는 `outputs/`에 원형으로 남겼고, 결과를 보고 expected snapshot을 만들지 않았다.

[output-differences.json](output-differences.json)은 실제 출력들끼리 비교한다. V02 정상 A/B는 compiler JSON 및 SVG가 동일하다. V03의 compiled A/B 차이는 축 fill의 test 한 곳이다. SVG의 23개 구조 차이 중 하나는 목표 라벨의 red/black이고, 나머지 22개는 동일 프로세스 내 clip/gradient 식별자 및 그 참조다. 관측 scenegraph에서는 목표 fill과 gradient ID 두 곳만 달랐다. 원 SVG ID를 다시 쓰지 않았다.

SVG의 axis-title을 scenegraph의 scale에 연결해 각 셀의 x/y field와 대조했다. 점은 16개 셀마다 원문 세 record의 datum이 보존되고 x/y가 유한한지 확인했다. SVG text의 다중집합과 scenegraph title text도 일치한다. 제목 하나를 모든 셀에 복사한 결과가 아니다.

V03의 축 색은 legend text·막대 fill·빨강 기준선을 제외하고 `axis-label`의 target identity와 fill만 셌다. SVG와 scenegraph는 같은 색 결과를 보였다. 긴 라벨 **6개는 기본 limit/추정 폭에 따라 SVG에서 줄임표 처리**된다. 실제 SVG를 Inkscape로 PNG 변환해 같은 모델 보조자가 직접 보았을 때 일부 검정 라벨 앞부분은 원 spec의 막대가 덮고 있었다. 목표 zero 라벨 자체는 A에서 빨강, B에서 검정으로 읽힌다. 색 변경 성공을 모든 라벨 완전 식별 성공으로 바꾸어 말하지 않는다. [preview-observations.json](preview-observations.json), [preview-receipts.json](preview-receipts.json)에 형식 변환과 판독 한계를 남겼다. PNG는 재생성 가능한 scratch이며 원 SVG가 커밋 대상이다.

## 추가 탐색: 같은 V03 입력을 2.7.0에서 실행

이 비교는 원 봉인 이후 root가 요청했고, 5.1.0 주재생을 마친 다음 수행했다. [sensitivity-plan.json](sensitivity-plan.json)에 당시 알고 있던 결과와 탐색 상태를 남겼다. 원 predictions/operations를 수정하지 않았고, 추가 두 실행은 사전 예측 점수나 공개 후속 저작 수에 넣지 않는다.

2.7.0 공식 package의 Vega peer는 `^3.0.0 || ^4.0.0`, 같은 tag lock의 실제 해소는 Vega **4.4.0**이었다. compiler 2.7.0과 그 runtime·의존 묶음을 함께 고정했다. 이는 compiler 하나만 바꾸는 격리 비교가 아니다. A/B 입력 파일은 5.1.0 재생에서 저장한 파일을 그대로 읽어 bytes와 해시가 동일하다.

| 추가 탐색 실행 | 같은 입력의 실제 결과 | 5.1.0과 비교 |
| --- | --- | --- |
| V03 v2.7.0 A | 대상 y축 10라벨 모두 `#000`; A/B compiler JSON 동일 | 5.1.0의 A=1 red/9 black과 다름 |
| V03 v2.7.0 B | 대상 y축 10라벨 모두 `#000`; 두 test 모두 compiled output에서 사라짐 | 5.1.0의 B=10 black과 색 결과는 같지만 조건이 보존된 같은 API 조작은 아님 |

2.7.0 artifact의 `src/axis.ts` L140–185 목록에 `labelColor`는 없고, `src/compile/axis/parse.ts` L184–215는 정해진 속성 목록과 `axis.encoding`으로 guide encode를 구성한다. 실제 두 compiled JSON은 byte-identical이며 A/B test가 둘 다 없다. 따라서 이 구판에서는 입력 수준 A를 적었어도 같은 행동 옵션이 구현되지 않는다. 유효한 구판 API로 대체해서 성공시키지 않았다.

구판 출력에는 대상 y축 10라벨 외 x축 tick 라벨 6개도 생긴다. 전체 16개를 y축 색 판정 분모로 사용하지 않았다. 구판 SVG는 fill을 속성 대신 inline style로 저장하므로 그 style을 파싱해 10개 `#000`을 확인했다. [sensitivity-results.json](sensitivity-results.json), [A SVG](outputs/V03-v270-A.svg), [B SVG](outputs/V03-v270-B.svg), [실행 영수증](sensitivity-render-receipts.json)이 근거다. 실제 imports와 artifact integrity는 [imported-versions-runtime-v270.json](imported-versions-runtime-v270.json), [sensitivity-dependency-integrity.json](sensitivity-dependency-integrity.json)에 있다.

2.7.0 설치 첫 시도는 공식 npm tarball의 HTTP 503으로 종료 1이었다. 동일 URL·동일 신원·동일 lock으로 한 번 재시도해 종료 0으로 설치했고, 두 실행은 종료 0으로 완료했다. 실패 영수증도 지우지 않았다. 이 비교는 **같은 입력 수준 조작이 판과 API 가용성에 따라 다른 결과를 낼 수 있다는 관측 반례**다. 원작성자가 실제 2.7.0을 썼다는 증거는 아니다.

## 재현 명령과 실행 영수증

저장소 루트에서 다음 명령을 각각 실행한다. `render`의 종료 1을 곧바로 중단 조건으로 삼는 `&&` 사슬로 묶지 않는다. 예정된 경계 B compile 실패도 결과이므로 이후 분석은 별도 명령으로 실행한다.

```bash
python -B docs/workstreams/research/AF-RES-053/replay/reproduce.py setup
python -B docs/workstreams/research/AF-RES-053/replay/reproduce.py render
python -B docs/workstreams/research/AF-RES-053/replay/reproduce.py analyze
python -B docs/workstreams/research/AF-RES-053/replay/compare_outputs.py
python -B docs/workstreams/research/AF-RES-053/replay/sensitivity.py setup
python -B docs/workstreams/research/AF-RES-053/replay/sensitivity.py render
python -B docs/workstreams/research/AF-RES-053/replay/analyze_sensitivity.py
```

| 실제 기록 | 시작 UTC | 종료 코드 | 범위 |
| --- | --- | --- | --- |
| [install](logs/install.receipt.json) | 2026-11-23T02:00:35Z | 0 | 5.1.0/5.20.2 고정 설치 |
| [versions](logs/versions.receipt.json) | 2026-11-23T02:01:30Z | 0 | 실제 import 판 검사 |
| [render](logs/render.receipt.json) | 2026-11-23T02:01:37Z | 1 | 6변형 중 5 SVG, 지정 경계 B compile 실패 |
| [analyze](logs/analyze.receipt.json) | 2026-11-23T02:03:18Z | 0 | SVG/scenegraph/field 연결 검사 |
| [analyze-label-correction](logs/analyze-label-correction.receipt.json) | 2026-11-23T02:03:49Z | 0 | `independent`라는 부정확한 분모 이름만 `A/B variant`로 정정; 재렌더 없음 |
| [output-differences](logs/output-differences.receipt.json) | 2026-11-23T02:08:37Z | 0 | 실제 A/B compiler·SVG·scenegraph 차이 |
| [install-v270](logs/install-v270.receipt.json) | 2026-11-23T02:05:01Z | 1 | 공식 tarball HTTP503 |
| [install-v270-retry-once](logs/install-v270-retry-once.receipt.json) | 2026-11-23T02:07:46Z | 0 | 동일 주소 한 번 재시도 |
| [render-v270](logs/render-v270.receipt.json) | 2026-11-23T02:08:45Z | 0 | 같은 V03 A/B bytes, 구판 2실행 |
| [analyze-v270](logs/analyze-v270.receipt.json) | 2026-11-23T02:10:02Z | 0 | 대상 y축 10라벨 분리 확인 |

실행 영수증은 각 argv·cwd·시작/종료 UTC·stdout/stderr 파일과 해시를 포함한다. 모든 설치·캐시·package·node_modules는 `replay/scratch/`에 있고 재현 명령의 쓰기 범위는 이 `replay/` 아래다. 현재 환경의 공개 배포 접속이 다시 실패하면 위 고정 URL·입력·명령과 이미 보존한 hash로 재개할 수 있다. 구판 실험을 다른 새 compiler로 대체하지 않는다.

## 출처 수·검토 범위

[sources-new.jsonl](sources-new.jsonl)은 package·lock·공식 artifact 코드·접근 실패·입력 캐시 재열람 **13행**이다. 모두 `count_for_primary_minimum:false`다. 재생 판을 고정하는 근거로 유지하되, 22개 원전 및 공개 후속 6개 배당에는 산입하지 않는다. 자기 생성 SVG도 공개 선행·후속 원전이 아니다.

검토자는 root와 같은 모델의 `/root/donor_sources`이며, 설치·실행·기계 판독·보조 그림 판독을 수행했다. 별도 사람 검토, 원작성자 수락, 역사적 실행환경 재현, 독자 시험은 수행하지 않았다. 가장 큰 해석 한계는 작성자의 실제 patch 미확인, 일반 이름 정상 입력의 연구자 구성, 현대 Node/무canvas 환경의 폰트·가독성 미확인이다. 2.7.0 결과는 이 한계를 지우는 대신 버전 가정을 바꾸면 A의 성공 결론이 깨지는 실제 사례를 추가한다.
