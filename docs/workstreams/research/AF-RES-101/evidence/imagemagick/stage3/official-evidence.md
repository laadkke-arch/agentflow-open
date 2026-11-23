# ImageMagick — 봉인 뒤 동작·후속 교차검증

Stage2 원격 봉인 `4e7539906eb03abd46e6910643ed5317f97ddb45` 뒤에만 이 자료와 작성자 후속을 읽었다. `initial-part.json`과 `candidate-part.json`은 바꾸지 않았다. 이 파일의 목적은 후보가 구현하는 동작과 원 목표 전체, 작성자가 새로 알았다는 사실을 나누는 것이다.

## 고정 자료와 실행 경계

공식 문서·구현 5개와 상류 시험 묶음 2개를 고유 자료로 산입한다. 같은 문서의 여러 앵커, 같은 구현의 다른 판, 한 시험의 header/harness/TAP wrapper를 별개 고유 자료로 늘리지 않았다. 상세 원장과 해시는 [sources-official.jsonl](sources-official.jsonl), 취득 시각·URL·HTTP 상태는 [official-acquisition.json](official-acquisition.json)에 있다.

| 자료 ID | 직접 읽은 고정 원문 | 확인한 값·범위 | 한계 |
| --- | --- | --- | --- |
| IM-O1 | [command-line-options.html](https://github.com/ImageMagick/ImageMagick/blob/eeb41d70c9baf418a3aa75c424fb305362a1b280/www/command-line-options.html) | threshold의 raw/percent, brightness/contrast, normalize, Perspective·canvas, size·separate | 전체 원 목적 또는 Ruby wrapper의 정확성을 증명하지 않음 |
| IM-O2 | [command-line-processing.html](https://github.com/ImageMagick/ImageMagick/blob/eeb41d70c9baf418a3aa75c424fb305362a1b280/www/command-line-processing.html) | L561–581, 괄호 안 이미지 스택과 별도 인수 | 셸 변수 안 escape를 자동 재해석한다고 쓰지 않음 |
| IM-O3 | [MagickWand/operation.c](https://github.com/ImageMagick/ImageMagick/blob/eeb41d70c9baf418a3aa75c424fb305362a1b280/MagickWand/operation.c) | brightness-contrast·contrast-stretch 파싱, distort 부호→bestfit, NormalizeImage dispatch | 원판 실행이 아닌 소스 확인 |
| IM-O4 | [MagickCore/distort.c](https://github.com/ImageMagick/ImageMagick/blob/eeb41d70c9baf418a3aa75c424fb305362a1b280/MagickCore/distort.c) | 기본 canvas·bestfit bounds·viewport override | 자동 꼭짓점 추출·종이 굴곡 복원은 구현 증거 범위 밖 |
| IM-O5 | [MagickCore/enhance.c](https://github.com/ImageMagick/ImageMagick/blob/eeb41d70c9baf418a3aa75c424fb305362a1b280/MagickCore/enhance.c) | L4103–4104의 old normalize clipping0.0015/0.9995 | 같은 판 문서와 불일치. 이 판 바이너리는 미실행 |
| IM-T1 | [tests/cli-colorspace.tap](https://github.com/ImageMagick/ImageMagick/blob/eeb41d70c9baf418a3aa75c424fb305362a1b280/tests/cli-colorspace.tap) | rose: 평균 입력, RGB146/89/80 예상값, 19개 변환 검사 | mask/CopyOpacity 전체 시험은 아님 |
| IM-T2 | [tests/validate.h](https://github.com/ImageMagick/ImageMagick/blob/eeb41d70c9baf418a3aa75c424fb305362a1b280/tests/validate.h) + [harness](https://github.com/ImageMagick/ImageMagick/blob/eeb41d70c9baf418a3aa75c424fb305362a1b280/tests/validate.c) + [TAP](https://github.com/ImageMagick/ImageMagick/blob/eeb41d70c9baf418a3aa75c424fb305362a1b280/tests/validate-convert.tap) | rose: 입력과 crop·normalize 등의 명령, ConvertImageCommand 성공 종료 oracle | 한 묶음만 산입. 픽셀 목표 oracle은 없고 전체 C suite는 미실행 |

고정판은 `7.0.10-61`, commit `eeb41d70c9baf418a3aa75c424fb305362a1b280`이다. IM-A2만 이 판을 명시했으며 다른 세 요청은 당시 판이 미확인이다. 실행한 연구판은 `ImageMagick7.1.1-43 Q16 x86_64`이다. 연구판 소스의 고정 commit은 `a2d96f40e707ba54b57e7d98c3277d3ea6611ace`다. C 소스 행 번호는 LF 기준이다. 폼피드를 행으로 세는 `splitlines()` 결과를 사용하지 않았다.

### 연산 별칭의 반례: normalize

7.0.10-61 문서의 normalize 절은 `-contrast-stretch 2%x1%`를 제시하지만, 그 판의 `NormalizeImage` 구현은 black pixel count의0.15%, white 누적한계99.95%를 사용한다. CLI의 white 인수 처리까지 연결하면 높은 쪽 제외분은0.05%다. 따라서 문서상의 별칭을 당시 판에 그대로 적용할 수 없다. 두 자료는 독립적인 증거가 일치한 사례로 세지 않았다.

연구판7.1.1-43의 같은 구현은2%/99%로 바뀌어 있다. [연구판 구현 취득 영수증](research-version-acquisition.json)과 [합성 입력 실행 영수증](probes/results.json)을 대조했다. 연구자가 만든16bit2000픽셀 gradient에서 normalize와2%x1%의 출력은2000/2000 동일했다.0.15%x0.05%는1992/2000픽셀, brightness-contrast0,90은1938/2000픽셀이 normalize와 달랐다. 이는 같은 의미의 다른 표기가 있을 수 있으며 버전과 입력 상태가 그 판정을 바꾼다는 보조 교정이다. 원 QR의 판독 여부는 확인하지 못했다.

### 부호만 다른 호출의 반례: Perspective

80×60 합성 checker의 네 모서리를10픽셀씩 평행 이동시키는 동일 point map을 사용했다. `-distort Perspective`는80×60+0+0, `+distort Perspective`는82×62+9+9의 canvas를 만들었다. `distort:viewport=80x60+0+0`을 명시하면 두 출력의 RGBA SHA256이 같았다. 따라서 부호가 다르면 늘 다른 결과라는 주장도, Perspective라는 이름만 같으면 같은 동작이라는 주장도 성립하지 않는다. 필요한 상태값이 빠진 IM-U2-C1과 명시적인 +distort인 C2를 사전 규칙대로 둘로 둔 판단을 유지한다. 이것은 두 독립 사건이 아니라 한 요청의 두 후보다.

이 실험은 연구자가 모서리를 제공했다. 원 질문의 **자동** 꼭짓점 찾기, 목표 가로세로비, 굴곡 복원을 해결한 것으로 쓰지 않는다. 현재 원 Perspective 링크는404였으며 [실패 영수증](original-link-acquisition.json)을 남겼다. 위 고정 문서는 연구자가 나중에 붙인 근거다.

### 상류 시험의 실제 실행과 한계

고정된 `cli-colorspace.tap` 파일은 수정하지 않고 연구판 바이너리를 가리키는 환경만 생성해 실행했다. TAP19개 모두 성공했고 종료값0이었다. [stdout](probes/upstream-cli-colorspace.stdout.txt)과 [명령·UTC·해시](probes/results.json)를 남겼다. 구형 시험이 현재판에서 통과했다는 결과이며, 구형 바이너리를 실행했다는 뜻이 아니다. 원 mask 파이프라인의 직접 실험은 root가 별도의5픽셀 입력으로 수행하여 [영수증](../../root-supplement/probe-receipt.json)에 남겼다.

상류 validate suite는 명령 옵션과 실제 oracle을 읽었다. `ValidateConvertCommand`는 옵션별 명령의 종료 성공을 확인한다. QR decoder, 회색 제거 후 픽셀 보존, 원 patch의 위치와 크기를 검사하지 않는다. 이 시험을 전부 통과해도 원 목적의 유효 대안이라고 확정할 수 없으며, 전체 C suite는 이번 연구에서 빌드·실행하지 않았다.

## 후보별 원 목표 판정

[assessment-part.json](assessment-part.json)은12자리(10실재+2빈자리)를 모두 담는다. `required_output_status`는 원 필수 출력, `hard_constraint_status`는 변경 불가 조건, `literal_evidence_status`는 읽은 고정판과 연구 환경의 더 좁은 반례다. 이 세 항목을 합쳐서 역사적 성공·실패를 만들어 내지 않았다.

IM-A1-C1은 고정 QuickMagick API 및 threshold raw15의 의미가 문제이며, 실제 작성자가 후속에 실패를 적은 코드는 alpha(off)를 빼고 실행한 수정형이다. C2의 QuantumRange×0.15는 percentage 의도에 맞지만, RMagick4.0.0에서 삭제된 matte=를 써서 고정5.3.0에서는 그대로 맞지 않는다. C3의 grouped CLI는 합성 입력에서 기대한 alpha 차이를 만들지만 전체 Ruby·원 입력 실행은 없고 Shellwords 로딩 조건도 있다. 세 후보 모두 원 사용자의 라이브러리 판은 모른다. [root 고정 wrapper 판정](../../root-supplement/assessment.json)

IM-A2-C1은 변수에 담은 문자열의 역슬래시 괄호와 따옴표가 실제 argv에 남는다는 반례가 있다. 이 실험은 argv만 포착한 것이며 전체 Cygwin 이미지 명령 실행이 아니다. C2는 원 revision1 마지막 블록을 그대로 Bash 구문 검사하면 잔여fi에서 종료값2이고, white patch는30×40으로 고정되어 원 두 분기를 그대로 보존하지 않는다. 수정 가능한 아이디어와 원 후보를 구별하여, 연구자가 고친 코드를 원 당시 추천으로 세지 않았다.

IM-U1의 contrast와 normalize는 공식적으로 확인되는 전처리이지만 일반 QR reader가 읽는 결과라는 필수 목표에는 증거가 없다. 행별 peak 극성 전환 알고리즘에는 구체적인 실행 코드·복원 후 decoder 결과가 없다. [이미지 접근 영수증](image-acquisition.json)의 QR 입력/출력4주소는 모두403이었다.

IM-U2의 네 점 Perspective는 평면 투영 보정의 구성요소로 지지되지만 자동 모서리 검출·실제 목표 비율·굴곡이 있는 입력 전체에 대한 검증이 없다. 두 사진 링크는503이었다. 작성자가 뒤에 de-wrinkling보다 직각 시점을 강조한 사실은 [후속](followup-part.json)에만 놓았다.

## 90일 작성자 기록

4사건 모두 질문별90일 창의 답변·댓글을 끝까지 순회했고 최종 페이지 `has_more=false`를 확인했다. 최초 모집 때 기계가 받은 질문 revision 전체는 첫 봉인 전 숨겼으며, 이후판은 두 번째 봉인 뒤에 읽었다. 90일 자기 답변0, 명시된 외부 결과/patch 링크0이다. 삭제된 댓글·과거 댓글 본문·비공개 실행은 보이지 않는다.

| 요청 | 실제 후속 | 인지·실행 해석 | 최초판과 현재판 |
| --- | --- | --- | --- |
| IM-A1 | revision2와 댓글137114172 | 수정C1 실행·실패 보고1에피소드. 명시 신규인지 및 입력/판/출력 연결 실행은 미확인 | 실제 시도 이력은 바뀜. alpha(off) 누락 및 입력/판 결손 때문에 동일한 전체 후보라고 소급하지 않음 |
| IM-A2 | 댓글137150030·137150039 | 다른 상황에서 유용하다는 말과 목적에 맞는다는 긍정. 실행·신규인지는 미확인 | 현재 본문도 revision1 |
| IM-U1 | revision2와 댓글137059273·137066174 | 흑백 출력 요구와 유용하다는 감사. reader 성공·실행·신규인지 미확인 | revision2는 이미지 링크 배치만 바뀜 |
| IM-U2 | revision2와 댓글137127563 | 직사각형·실제 크기 미지정, 직각 시점 목표 보완. 실행·신규인지 미확인 | 목표 조건이 추가됨. 최초판 actual-use 없음은 그대로 |

총9관측(작성자 댓글6, 수정3)을 세었다. A1의 두 관측을 실행2회로 세지 않았다. 현재 accepted 표시가 있는 것은 A1 답변과 A2 두 번째 답변이지만 수락시점·어느 코드에 대한 것인지는 모른다. 신규 인지로 코딩하지 않았다. 실제 시도 이력 변화1/4, 목표 조건 변화1/4, 단순 서식 변화1/4, 본문 불변1/4이다. 확정적인 A/B 판정 반전은0/4이며 이후 이력을 최초 시점에 넣지 않는다.

## 비교 가능한 분모와 반대 해석

A는 같은 ImageMagick 엔진인5후보를 제외하고4개를 반환한다. B는10개를 유지하고8개를 반환한다. 그러나 추가로 반환되는4개를 곧바로 다른 **유효** 조작4개로 부를 수 없다. 완전한 원 목표·조건을 지지하는 후보가 없어 유효 대안 분모0이고 비율은 산출 불가다. 이 분모 바깥에서는 원 literal 반례1개와 원 목표 미확인9개를 구별한다. 그9개 중에도 고정 wrapper/연구환경의 더 좁은 반례가 있다.

전체 후보를 이미 알았다는 확정 근거도0/10이다. 다만 IM-A1-C3의 core grouped CLI는 최초판에 이미 인용되어 있다. 이 부분만 단위로 잡은 민감도에서 분모1, A제외1, B제외0이다. C3는 B에서도 원순위3이라 실제 반환하지 않는다. Open3/Shellwords까지 이미 알았다고 단정하면 분모를 부풀리므로 주 집계와 분리했다. [분모 원자료](denominators-part.json)

이 결과는 A의 모든 제외가 옳거나 B의 유지가 무용하다는 결론을 주지 않는다. 같은 엔진의 효과가 다른 명령을 구별하는 데 B가 필요할 수 있지만, wrapper 문법이 맞는지·입력이 같은지·사용자가 새로 알았는지는 별도 검증이 필요하다. 반대로 B가 값 결손 때문에 C1/C2를 모두 살리는 U2는 중복 가능성을 남긴다. explicit viewport가 두 부호를 동등하게 만든 실험은 그 반대 가능성을 실제로 확인한 예다.

## 후속 설계자가 보여줄 한 줄의 후보

아래는 봉인 A/B를 다시 계산한 표가 아니라 Q7의 편집 결정 제안이다. 알려진 것·실행한 것·도움이 될 조건을 함께 표시한다.

| 요청 | 선택 | 보여줄 한 줄·연결 절 | 결정을 바꿀 반대 관측 |
| --- | --- | --- | --- |
| IM-A1 | 같은 도구 안의 다른 절 | “인용한 CLI는 이미 보셨고 실제 실행문에는 그룹 괄호가 빠졌습니다. [Image Stack 절](https://github.com/ImageMagick/ImageMagick/blob/eeb41d70c9baf418a3aa75c424fb305362a1b280/www/command-line-processing.html#L561-L581)로 실제 전달 인수부터 확인하세요.” | 같은 입력에 괄호 포함 명령도 이미 실행했고 같은 오류였다는 영수증이면 wrapper 판/API 문제로 초점을 옮김 |
| IM-A2 | 이미 시도했는지 한 가지 되묻기 | “분기에서는 dims/wd만 정하고 convert는 하나로 두는 방식을 이미 시도했나요?” | 그 방식의 정확한 인수·성공 출력이 이미 있으면 재추천 대신 실패한 입력/조건을 조사함 |
| IM-U1 | 이미 시도했는지 한 가지 되묻기 | “이미 시도한 영상 처리 명령과 인수는 무엇인가요?” | 동일 입력·동일 contrast/normalize 실행이 확인되면 같은 후보를 반복하지 않고 모듈 재구성 단계의 필요성을 검토함 |
| IM-U2 | 조건부 두 링크 | “네 꼭짓점이 주어지면 [Perspective 절](https://github.com/ImageMagick/ImageMagick/blob/eeb41d70c9baf418a3aa75c424fb305362a1b280/www/command-line-options.html#L2231-L2243), 출력의 크기·잘림이 다르면 [canvas/viewport 절](https://github.com/ImageMagick/ImageMagick/blob/eeb41d70c9baf418a3aa75c424fb305362a1b280/MagickCore/distort.c#L2018-L2038)을 보세요. 자동 꼭짓점 추출은 아직 제공되지 않았습니다.” | source corners·target viewport가 둘 다 고정되면 두 후보를 같은 조작으로 합칠 수 있음; 굴곡이 핵심이면 평면 Perspective만으로는 부족 |

## 재현·미실시

1. 원 자료를 다시 받으려면 `python -B docs/workstreams/research/AF-RES-101/evidence/imagemagick/stage3/fetch_official.py`와 `fetch_followup.py`를 실행한다. API 응답은 변할 수 있으므로 기록한 revision GUID·본문 해시·창을 비교한다. 이 경로는 API quota/backoff를 따른다.
2. `python -B docs/workstreams/research/AF-RES-101/evidence/imagemagick/stage3/run_core_probes.py`는 연구판 버전을 먼저 기록하고 동일 합성 입력 레시피로 normalize와Perspective 비교 및 고정 상류TAP 시험을 실행한다. stdout·stderr·UTC·종료값·출력 해시를 갱신하므로 기존 연구 결과와 별도 커밋에서 수행한다.
3. `build_stage3.py`, `build_assessment.py`, `build_screening_sources.py`는 취득 영수증과 봉인 자료에서 표·원장을 도출한다. 이들은 후속 자료를 최초판에 쓰지 않는다. 평가문은 연구자가 명시적으로 코딩한 값이다.
4. 원판 검증을 추가하려면 commit `eeb41d70c9baf418a3aa75c424fb305362a1b280`의 ImageMagick을 별도 디렉터리에 빌드하고, 원 `ImageMagick7.0.10-61/Cygwin` 환경·입력 이미지·coords·폰트를 확보해 A2의 원literal과 교정형을 나란히 실행한다. 현재는 원입력/환경이 없어 미실시다.
5. 원 QR 확인의 첫 입력은 `https://i.sstatic.net/iyzQE.png`이다. 접근 회복 뒤 원 바이트 SHA와 reader 이름/판을 고정하고 세 후보의 결과를 decoder에 넣어 payload와 실패를 기록해야 한다. 사진은 두 gyazo 원파일과 목표 사각형 정의가 먼저 필요하다.

| 가장 중요한 불일치·약점 | 다음에 열 자료 또는 실행할 입력 | 어떤 관측이면 결론을 바꿀지 |
| --- | --- | --- |
| 같은7.0.10-61의 normalize 문서와 구현 기본값이 다르며 당시 바이너리는 미실행 | 고정7.0.10-61 빌드에서 기록된2000픽셀 gradient와 두 contrast-stretch 값 실행 | 구형 바이너리가2%/1%와 같거나 compile-time 조건이 소스 읽기 해석을 바꾸면 old alias 판정을 수정 |
| 후보 전체의 prior knowledge와 원 목표 성공 증거가 없어 주 분모가0 | A1 실제 wrapper 판·원입력, A2 실제 교정 코드·Cygwin 출력, QR 원파일+decoder 결과 | 같은 입력의 성공/실패와 특정 후보를 제안 전에 알았다는 명시 증언이 연결되면 해당 후보의 분모 자격 변경 |
| U2 두 Perspective 제안은 값 결손 때문에 둘 다 남았고 자동 보정은 입증되지 않음 | 원 사진, source corners, 목표 aspect·viewport, 자동 검출 단계의 입력/예상 출력 | 동일 mapping·viewport가 확인되면 두 후보 중복으로 합치고, 독립 자동 보정 결과가 있으면 조건부 구성요소를 유효 대안으로 승격 |
