# AF-RES-116 ImageMagick 독립 기준 판독

작성 역할: `/root/gold_imagemagick`. 언어: 한국어. 판독과 파일 검사는 2026-11-24 UTC에 실시했다. 원요청 봉인은 `seal878f2e1b8d053f6eea4e3473d5b467ca98476a01`, 고정 corpus 봉인은 `seal27bdf61aac1c24299401879749fcbca1ce43e8a4`, 꾸러미 봉인은 `seal762fe1fc57b3b5f765f9d13537fa9c15b71b5b80`이다.

## 결론과 남은 한계

**I1과 I2는 회수한 TIFF의 실제 표지와 샘플을 확인해 조건부 기준 답을 정했다. I3는 파일별 색/채널 의미를 확정할 수 없어 보류한다.** 세 사건 모두 지정된 역사적 ImageMagick 바이너리로 실행한 결과는 없다. 이 문서의 `semantic_complete`는 필수 예외를 포함하는 한정 답의 내용이 정해졌다는 뜻이다. 실행 성공이나 3개봉의 충분한 문서 지원을 뜻하지 않는다.

| 사건 | 직접 확인한 핵심 | 기준 답 | 아직 확인하지 못한 것 |
|---|---|---|---|
| I1, #6159 | 원첨부 TIFF의 RGB, 4 samples, ExtraSamples=0. RGB 전샘플이 원 PNG와 동일. 추가 plane은 비상수 | meta와 alpha를 구분한다. 올바른 TIFF를 특정 viewer가 alpha처럼 보일 수 있다는 한정 설명 | 7.1.1-3 재생성 결과, 당시 Mac Preview/GraphicConverter/Photoshop/display 재현 |
| I2, #6187 | 원첨부 TIFF의 ExtraSamples=0. 네 번째 plane은 0–255의 105개 값 | 실제 TIFF alpha가 아닌 meta를 요청 대상 plane으로 분리한다. mask 의도가 확인됐을 때 alpha로 복사한 뒤 추출 가능 | 7.1.0-28 대 7.1.1-4 실행 비교, exact PNG 결과값 |
| I3, #6237 | 고정 JP2 reader의 성분 수 기반 alpha 선택을 코드에서 확인 | 4 components에서 RGBA를 추론하지 않고 원파일/box/band 기준을 요구하는 정당한 보류 | 원 JP2 바이트, 실제 colr/cdef/cmap, 해당 tile의 기준 색/IR 의미, 당시 delegate와 decode 결과 |

완전한 기준 설명에 필요한 TIFF/JP2 규격, 고정 구현, 원입력 태그가 fixed `www/*.html` corpus 밖에 있다. 따라서 `fixed_corpus_semantic_complete=false`, `fixed_corpus_answer_status=unknown`을 세 사건에 각각 명시했다. 이 판독자는 수신자 경로를 실행하거나 3개봉 그래프를 열거하지 않았으며 `unreachable`을 선언하지 않는다. 파일별 미확인과 문서 예산상 미확인을 혼동하지 않는다.

## 가림, 실제 읽기, 버전

`AGENTS.md`, `SCOPE.md`, `cases.json`의 I1/I2/I3, 선택된 원 issue body, 고정 corpus, 공개 공식 문서/코드/규격과 별도 공개 반례만 읽었다. `authoring/`, `packets.jsonl`, `inputs/`, `readers/`, 수신자의 trails/answers, 다른 gold, 힌트는 읽지 않았다. 공유 파일시스템에서의 절차적 가림이며 OS 격리는 아니다. 원 issue 댓글과 첨부는 모집 이후 이 기준 읽기에서 처음 확인한 **추가 층**이다.

| 사건 | 고정 버전 | upstream commit |
|---|---|---|
| I1 | 7.1.1-3 | `c5d5e7117fb07096158bcad05e1086f0c2fff172` |
| I2 | 7.1.1-4 | `10ad43dc3e5113fa1969a55583a080c5a6a23f65` |
| I3 | 7.1.1-6 | `b2dd67b1681e23d0e0b9769d81bed23f05129e2a` |

다운로드 완료를 직접 읽기로 세지 않았다. `read-events.jsonl`은 실제 표시/검사 UTC와 구간을 기록한다. 처음 긴 출력 하나가 잘렸으므로 해당 batch를 표시했고, 의존하는 댓글·코드 부분을 좁게 다시 표시했다. `sources-imagemagick.jsonl`은 그 차이를 유지한다. PDF는 텍스트 추출과 함께 TIFF p31 및 T.800 PDF p162의 렌더된 표를 04:29:04 UTC에 직접 확인했다.

현재 환경은 `ImageMagick 7.1.1-43 Q16 x86_64 22550`이다. 이 바이너리는 버전 확인 및 아래 **별도 합성 반례**에만 사용했다. 원 사건의 7.1.1-3/-4/-6 성공으로 소급하지 않는다. 원첨부의 TIFF 태그와 무압축 8-bit strip은 Pillow 13.0.0 및 원시 byte 배열로 검사했다. 이 검사는 ImageMagick 역사판의 실행이 아니다. 자세한 배열 해시와 수치는 `input-inspection.json`에 있다.

## I1: RGB + meta TIFF의 표시

### 원요청이 말한 것과 나중에 확인한 것

[원 issue #6159](https://github.com/ImageMagick/ImageMagick/issues/6159)는 grayscale 이미지를 RGB의 meta 채널에 넣었는데 alpha처럼 보인다고 했다. 원 body에는 표시 앱 이름이나 TIFF ExtraSamples 값이 없다. body의 명령 끝에는 typographic quote가 있으므로 gold의 명령은 그 의도를 ASCII 따옴표로 정상화했다. 정상화한 문자열 자체를 원문 그대로라고 부르지 않는다.

추가 댓글에서 maintainer는 unspecified extra sample을 alpha로 해석하면 안 된다고 설명했고, 작성자는 display와 Photoshop은 정상, Mac Preview와 GraphicConverter는 alpha처럼 표시한다고 보고했다. 이 내용은 **당시 작성자/maintainer의 보고**다. 이 세션에서 그 네 앱을 실행하지 않았다. `issue-6159-comments`가 원 issue와 별도의 고유 저작이 되지는 않는다.

회수한 `meta.tif`의 값은 다음과 같다.

| 항목 | 직접 검사 값 |
|---|---|
| 크기 | 256×256 |
| PhotometricInterpretation | 2, RGB |
| SamplesPerPixel / BitsPerSample | 4 / 8,8,8,8 |
| ExtraSamples | 0, unspecified |
| 압축/배치 | 무압축, chunky |
| RGB 대 원 lena.png | 전 샘플 동일, 최대 절대 차이 0 |
| 추가 plane | 최소 3, 최대 220, 고유 값 216 |

파일 전체 SHA는 `1290cdd5eb69e627a428996b827986a7895689d6cc45b78c088b70cc0d65703a`다. 원 입력 두 개는 모두 256×256 RGB로 확인했다. 원 RGB PNG의 Pillow info에는 ICC가 없었고 TIFF의 IFD에도 ICC tag는 없었다. 이 제한된 관찰을 모든 color profile과 모든 viewer의 외관 보존으로 확장하지 않는다.

### 정의와 구현의 교차 확인

[TIFF 6.0 공식 ITU 배포 사본](https://www.itu.int/itudoc/itu-t/com16/tiff-fx/docs/tiff6.pdf)의 pp31–32는 ExtraSamples 0/1/2를 각각 unspecified, associated alpha, unassociated alpha로 구분한다. p77은 associated alpha의 RGB가 alpha와 곱해진 저장 형태라는 조건을 설명한다. 따라서 4 samples라는 수는 alpha의 충분한 근거가 아니다.

[7.1.1-3의 TIFF coder](https://raw.githubusercontent.com/ImageMagick/ImageMagick/c5d5e7117fb07096158bcad05e1086f0c2fff172/coders/tiff.c)에서 reader lines1700–1737과 writer3622–3655를 확인했다. writer는 실제 alpha와 meta 채널 수를 따로 보고, alpha가 없는 meta extra sample을 unspecified로 둔다. reader도 associated/unassociated 표지가 있는 경우에 alpha를 활성화하고 나머지 extra를 meta로 다룬다. 이것은 직접 확인한 첨부 태그와 일치한다.

판정은 **현재 회수한 출력의 RGB 값과 meta 표지는 요청 의도와 부합한다**는 것이다. 원 JPEG의 역사적 grayscale 변환값을 새로 계산한 것도, 모든 viewer에서 같은 외관을 보장한 것도 아니다. 추가 정보를 alpha로 바꾸는 처방은 이 사건의 채널 의미 보존 목표를 바꾼다.

## I2: 흰 alpha extraction과 살아 있는 meta 값

[원 issue #6187](https://github.com/ImageMagick/ImageMagick/issues/6187)의 이전 판 성공과 7.1.1-4의 흰 결과는 원저자 보고다. 원 body에는 TIFF extra sample의 실제 선언이 없다.

현재 회수한 `demo.tif`는 472×392, RGB, 8-bit×4, 무압축이며 ExtraSamples=(0,)이다. 네 번째 plane은 최소 0, 최대 255, 고유 값 105로 비상수다. 파일 SHA는 `79c2a9ccbf36de73a34b9090732cb19107fbc875b76e71020538073a72aac223`다. TIFF의 소프트웨어 필드는 Photoshop24.2(Windows)를 가리킨다. Photoshop UI에서 Alpha1이라고 부르는 것과 TIFF transparency 선언은 별개다.

[7.1.1-4 TIFF coder](https://raw.githubusercontent.com/ImageMagick/ImageMagick/10ad43dc3e5113fa1969a55583a080c5a6a23f65/coders/tiff.c)의 lines1700–1737은 unspecified extra를 meta로 읽는 흐름을 보여준다. 같은 판의 `GetPixelAlpha`는 alpha trait가 undefined이면 opaque를 반환한다. `ExtractAlphaChannel`은 AlphaCompositeOp를 실행하며 composite 코드가 source alpha를 output 값으로 사용한다. 따라서 이 입력을 alpha로 추출한 결과가 흰 mask라는 보고는 고정 코드와 부합한다. **흰 mask는 원 TIFF의 네 번째 plane이 흰색이라는 증거가 아니다.**

원 데이터 값을 꺼내는 한정 경로와, 그 plane을 의도된 opacity mask로 해석할 때의 경로를 구분했다. 다음 명령은 7.1.1-4에서 **실행하지 않았다**.

```sh
magick demo.tif -channel-fx 'meta' extract.png
magick demo.tif -channel-fx 'meta=>alpha' -alpha extract extract.png
```

첫 명령은 확인된 plane의 값을 grayscale로 분리하는 정적 소스 기반 경로다. `ChannelFxImage`의 source 채널 확인, 복사/추출, 단일 채널 grayscale 설정을 읽었다. 둘째는 meta가 사용자가 의도한 mask라는 조건에서만 해석한다. 원 작성자는 후속 댓글에서 meta=>alpha가 잘 작동한다고 했지만, 위 exact grayscale PNG 조합의 역사판 결과를 이 세션에서 확인하지는 않았다.

`-alpha set`이나 `opaque`는 데이터 복구 근거가 아니다. 고정 매뉴얼은 꺼져 있던 alpha에 `set`을 적용하면 opaque로 초기화할 수 있다고 한다. 또한 associated 표지를 붙이는 변경은 RGB premultiplication 뜻까지 바꾼다. 후속 댓글의 associated 제안을 모든 TIFF에 무조건 적용하는 기준 답으로 채택하지 않았다. 실제 opacity가 선언된 다른 파일은 alpha대로 처리해야 한다.

## I3: JP2 4 components의 뜻과 정당한 보류

[원 issue #6237](https://github.com/ImageMagick/ImageMagick/issues/6237)는 identify의 gray+alpha, ExifTool의 4 components와 Grayscale을 보고했으며, RGBA라는 해석은 작성자도 의심했다. 원 정상 RGB 기준 파일이나 확정 색 샘플은 없었다.

원첨부의 HTTP URL과 HTTPS 대체 URL은 모두 404였다. 작성자가 제시한 원 배포 디렉터리도 404였다. 영수증을 보존했으며 **파일을 읽은 것, 다운로드에 성공한 것, RGBA/IR metadata를 직접 확인한 것 모두로 세지 않았다.**

[ITU-T T.800 (11/2015)](https://www.itu.int/rec/dologin_pub.asp?id=T-REC-T.800-201511-S%21%21PDF-E&lang=e&type=items)의 PDF155–159와162–164를 읽었다. NC는 codestream component 수다. colr는 enumerated colourspace 또는 ICC를 통한 색 해석이고, cmap/cdef는 component를 채널로 매핑하고 각 채널의 type과 association을 지정한다. cdef는 색 데이터, opacity, premultiplied opacity, unspecified를 구별한다. auxiliary channel이 있다면 완전한 channel definition이 필요하다는 규정도 있다. 이 항목들을 단순 component 수 하나로 대체할 수 없다. 규격에는 sRGB도 있으므로 후속 댓글의 JPEG2000 전체에 대한 과도한 색 모델 일반화를 기준 사실로 채택하지 않았다.

[7.1.1-6 JP2 coder](https://raw.githubusercontent.com/ImageMagick/ImageMagick/b2dd67b1681e23d0e0b9769d81bed23f05129e2a/coders/jp2.c)의 lines429–446,511–545는 OpenJPEG의 grayscale 색공간이면 GRAY로 설정하며, 여러 성분/4성분 이상에서 alpha를 활성화하고 component3을 alpha에 저장하는 흐름이다. 별도로 [OpenJPEG2.5.0 header](https://raw.githubusercontent.com/uclouvain/openjpeg/v2.5.0/src/lib/openjp2/openjpeg.h)의 enum2=GRAY와 component.alpha 필드를 확인했다. 이 header가 원저자가 링크한 실제 delegate 버전이었다고 주장하지 않는다.

후속 저자는 메타데이터를 확인한 뒤 네 번째 채널이 near-IR라고 보고했다. [NRW 공식 제품 이력 FAQ](https://www.bezreg-koeln.nrw.de/system/files/media/document/file/geobasis_lusat_hist_dop_nutzerinfo_hist_dop_faq.pdf) p7의 표와 각주도 RGBI 제품군의 네 번째 채널이 near-IR임을 설명한다. 이는 **제품군과 저자 보고**에 대한 뒷받침이며, 회수하지 못한 정확한 2021 tile의 header/bytes 검증은 아니다.

이 자료는 RGBI가 alpha로 소비될 **구현상 위험**을 확인해 준다. 실제 파일의 color/auxiliary 선언을 모르는 상태에서 “틀린 grayscale”이나 “올바른 파일 해석” 어느 쪽도 확정하지 않는다. 이미 결합·누락된 plane을 뒤의 `-colorspace sRGB`로 복원할 수 있다고 주장하지 않는다. 다음 최소 입력이 있어야 파일별 판정을 닫을 수 있다.

1. 원첨부 또는 동일성이 입증된 원배포 JP2 바이트와 SHA-256.
2. ihdr/colr/cmap/cdef 및 codestream header, exact tile/배포 시점의 band 정의.
3. 7.1.1-6의 linked OpenJPEG 정보와 모든 component를 따로 확인할 수 있는 기준 decode.

`gold.json`에는 `magick identify -verbose`, `exiftool -G1 -a -s`, `opj_dump -i`의 exact 미실행 명령과 각 명령이 확인할 수 없는 범위를 넣었다. 입력이 없다는 사실은 소프트웨어상 불가능의 증명이 아니다.

## 잠정 결론의 반증 기록

아래는 원요청에서 나올 수 있는 잠정 결론을 실제 근거로 시험한 기록이다. 읽기 전에 이 결론들을 확신했다는 회고나 사전등록으로 꾸미지 않는다.

| 잠정 결론 | 반증·제약 근거 | 남긴 결론 |
|---|---|---|
| I1의 네 번째 plane이 alpha처럼 보였으므로 writer가 RGB를 훼손했다 | ExtraSamples0, 전 RGB 샘플 동일, fixed writer 분기, 앱별 후속 관찰 | 표시 현상과 저장 데이터/채널 의미를 분리 |
| I2가 예전 판에서 됐으므로 같은 plane은 규격상 alpha이며 새 extraction이 항상 고장났다 | 입력 ExtraSamples0, 비상수 raw plane, fixed reader가 meta로 분류, absent-alpha opaque fallback | 이 파일의 선언 차이를 먼저 설명. 일반 회귀 진단은 보류 |
| I3의 4 components는 RGBA다 | JP2 NC/colr/cdef 구분, RGBI 제품군, fixed reader의 count 휴리스틱, 원파일 unavailable | RGBA/alpha 확정 금지, 파일별 보류 |
| 채널명 srgba가 있으면 원 alpha 값도 살아 있다 | 별도 #7848의 같은 채널명·다른 alpha 내용 보고 | label과 plane 값 검증을 분리 |
| alpha가 보존되거나 alpha 조작이 성공하면 color profile도 보존된다 | #8022 및 아래 양방향 합성 반례 | 두 보존 조건의 독립 검증 |

## 독립 보조 저작과 반례

최소 할당은 아래와 같이 **정의 4 + 별도 회귀/반대 입력 3**이다. ImageMagick의 모든 manual 페이지와 버전은 한 저작으로 묶었다. 본문의 앵커 여러 개, 같은 댓글·첨부·fix 설명을 여러 저작으로 세지 않았다.

| 할당 | 고유 저작 | 독립성 및 용도 |
|---|---|---|
| 정의 1 | ImageMagick 공식 매뉴얼 | 요청 연산·채널·형식 설명. 모든 읽은 페이지/버전 합쳐 1 |
| 정의 2 | TIFF6.0 | ExtraSamples와 associated alpha의 독립 원규격 |
| 정의 3 | ITU-T T.800 (11/2015) | JPEG2000 component/color/channel의 독립 원규격 |
| 정의 4 | W3C PNG Second Edition(2003) | alpha와 ICC 정보를 별도 정의하는 독립 원규격 |
| 반례 1 | [Discussion#6299](https://github.com/ImageMagick/ImageMagick/discussions/6299) | 다른 저자·다른 64×64 LZW icon 입력. 실제 tag0 확인. #6187과 같은 기전이므로 새 fix로 세지 않고 독립 counter-input으로만 배당 |
| 회귀 2 | [Discussion#7848](https://github.com/ImageMagick/ImageMagick/discussions/7848) | 7.1.1-40→41의 sample_info refactor 회귀. 공개 Car 입력의 tag1 및 raw alpha 0–255/256고유값 확인. 댓글·첨부·maintainer 수정 설명 합쳐 1 |
| 회귀 3 | [Issue#8022](https://github.com/ImageMagick/ImageMagick/issues/8022) | JXL alpha 제거 성공과 ICC 변경이라는 다른 조건 불일치. upstream libjxl 논의도 별도 저작으로 늘리지 않음 |

고정 ImageMagick 코드, OpenJPEG header, NRW FAQ는 관련 있는 additional 근거로 남겼으며 이 quota를 더 늘리지 않았다. 자연 원요청3은 이미 배당된 요청이고 댓글도 원 issue lineage다. #6299가 다른 첨부를 가진다고 해서 I1/I2와 기전이 독립인 실험 반복이라고 주장하지 않는다.

#7848의 입력은 1000×750 무압축 TIFF, ExtraSamples=1이며 실제 alpha가 256개 값을 가진다. 즉 모든 추가 plane 문제를 “원파일 unspecified이므로 정상”으로 처리할 수는 없다. 원저자와 maintainer가 후기 버전 회귀를 보고했고 두 버전 모두 srgba로 표시될 수 있다고 했다. 역사적 출력 재현은 하지 않았다. short SHA `15ec380`에 대한 API 조회는422로 실패했으므로 그 fix diff를 직접 읽었다고 기록하지 않았다.

#8022는 7.1.1-44/libjxl0.10.4에서 alpha가 제거되면서 원 ICC가 9080bytes에서 다른 536bytes profile로 바뀌었다는 원저자 입출력 기록이다. 후속 글은 겉보기 색 차이가 작거나 없을 수 있음을 말한다. 이 사실은 원 ICC의 동일성이 보존됐다는 증거가 아니다. JXL 첨부는 회수했고 archive entry/signature까지 읽었으나 이 환경에 JXL delegate가 없어 ICC와 channel 내용은 독립 디코드하지 않았다. profile 변경이 반드시 눈에 띄는 색 오차라는 주장도 하지 않는다.

### 알파와 ICC의 양방향 합성 반례

자연 사건과 별개로 2×2 RGBA 입력에 내장 sRGB ICC와 alpha값 `[0,85,170,255]`를 넣었다. 설치된 **7.1.1-43**에서만 다음 결과를 직접 확인했다.

| 조작 | alpha sample 동일성 | ICC byte 동일성 |
|---|---:|---:|
| `-strip` | true | false, ICC 없음 |
| `-alpha off` | false, 모두255 | true |

이것은 같은 입력에서 한 조건이 true여도 다른 조건이 false일 수 있는 구체적 반례다. 입력은 연구자가 만든 보조 층으로 명시했고, 자연 사례/역사판 결과/추가 공개 저작으로 세지 않았다. `supplementary-constructed-results.json`에 실제 명령·UTC·exit code·input/output/profile hash가 있고 `make_counterexample.py`로 같은 fixture를 재사용할 수 있다. 이 검사는 alpha의 값과 ICC bytes의 보존을 다루며 profile 제거가 이 tiny sRGB fixture에 눈에 띄는 색 차이를 만든다는 실험은 아니다.

## corpus 구간과 정확한 본문 도달 기준

`minimal-intervals.json`의 모든 `start/end`는 `corpus.json.gz`의 `documents[].text`에서 **Unicode code point 기준, 0-based 반개구간**이다. 원 HTML의 `source_sha`와 정확한 commit·version을 함께 저장했다. 기준에 필요한 외부 규격/구현 구간은 `gold.json`의 `outside_corpus_minimal_intervals`에 따로 보존했다. corpus literal 검색 결과도 저장했으나 문자열 미발견을 의미상 부재나 도달 불가능의 완전한 증명으로 사용하지 않았다.

`target-spans.json`은 C/packet/수신자 선택을 보지 않고 요청 연산의 본문으로 고정했다.

| 사건 | 근접 연산 본문 target | 해석 |
|---|---|---|
| I1 | `i7113_command-line-options[37371:37449]` | channel-fx 이름과 채널 연산 정의의 첫 문장 |
| I2 | `i7114_command-line-options[12856:13022]` | Extract subtype과 grayscale mask로 복사하는 실제 첫 문장 |
| I3 | `i7116_formats[12648:12805]` | JP2 지원 형식의 본문 행. encoding 안내 주석이 있어 coarse capability 도달로만 해석 |

목차 label이나 anchor 이름만 노출된 경우는 이 target 도달이 아니다. 세 사건의 결정적 답 target은 모두 `outside`다. I3의 row 도달은 decoding의 실제 색/채널 보존 답을 찾은 것이 아니다. 노출 예산에 맞춰 correctness나 target을 줄이지 않았다.

## 저장물과 재현 범위

핵심 파일은 `gold.json`, `gold-notes.md`, `sources-imagemagick.jsonl`, `minimal-intervals.json`, `target-spans.json`이다. 공개 스냅샷·원첨부·수신 영수증·원시 입력 검사 결과도 같은 소유 폴더에 보존했다. Git/global 파일은 수정하지 않았다.

GitHub attachment의 실제 도착 URL은 서명 query를 제거한 origin/path만 저장했다. 영수증에 제거한 key 이름과 **관측 canonical URL이 아님**을 명시했다. #7848의 공개 HTML에 포함된 두 screenshot href/src의 JWT query도 제거했다. 그 HTML의 `sha256`은 원수신 body 해시, `stored_sha256`은 서명 query를 제거한 스냅샷 해시이며 원장에도 차이를 표시했다. 댓글 본문은 바뀌지 않았고 해당 screenshot 픽셀은 읽지 않았다. URL의 query를 제거한 것을 실제 canonical redirect로 오해하면 안 된다. ZIP은 경로 탈출·절대 경로·symlink 및 총 압축해제 크기를 검사한 뒤 필요한 파일만 회수했다.

`build_gold.py`는 이 reader의 자료와 고정 corpus에서 gold/원장을 다시 만든다. `inspect_inputs.py`는 원 TIFF IFD와 무압축 8-bit sample 및 PNG RGB의 현재 검사를 재현한다. `make_counterexample.py`는 별도 7.1.1-43 보조 반례만 재현한다. **이 파일들의 성공이 원소프트웨어 역사판, 당시 사람의 시간 절약, 원저자 채택, 새로운 수신자의 선택을 입증하지 않는다.**
