# Q7 오디오: 컨테이너·코덱·소비자 경계의 반례

조사 범위: AF-RES-092의 신규 여섯 질문과 별도인 타 분야 대조. A/B 검색·열람 예산 및 승률 분모에 넣지 않는다. 2026-11-23T16:28:32Z–16:29:50Z에 공개 원자료를 직접 읽었다. 아래는 문서·코드 독해와 공개 사용 보고의 대조이며, 이 조사자가 바이너리를 실행하거나 Safari 재생을 재현한 결과는 아니다.

## 직접 확인한 세 계열

| 경계와 주장 | 직접 원자료·판·위치 | 확인한 내용 | 반례·제약 |
| --- | --- | --- | --- |
| 코덱 이름만 같아도 산출물 목적은 다를 수 있다. | AUD-01: [RFC 7845 §4, §5.1](https://www.rfc-editor.org/rfc/rfc7845.html#section-5.1), 2016-04 | Ogg는 Opus 패킷을 담는다. granule position은 채널별 48 kHz PCM 샘플 수를 센다. 헤더의 입력 샘플레이트는 재생 샘플레이트가 아니다. 재생에는 가능하면 48 kHz를 쓰지만 디스크 파일로 복원할 때는 원 입력 샘플레이트로 다시 변환할 수 있다고 구별한다. | 같은 ‘Opus 출력’이라도 즉시 재생과 원 샘플레이트의 PCM 파일 복원은 요구가 다르다. RFC 적합성만으로 특정 브라우저의 시간축 정확성을 보증하지 않는다. |
| 하나의 기존 도구가 둘 이상의 단계를 이미 수행한다. | AUD-02: [FFmpeg n7.1 고정 매뉴얼, Stream copy](https://github.com/FFmpeg/FFmpeg/blob/b08d7969c550a804a59511c7b83f2dd8cc0499b8/doc/ffmpeg.texi#L202-L220); 태그 생성 2024-09-29T23:29:50Z | `-codec copy`는 디코드·인코드를 생략하고 demux와 mux를 수행한다. 코덱을 다시 만들지 않고 컨테이너를 바꿀 수 있다. | 모든 대상 컨테이너에 항상 성공하는 기능은 아니며, 디코드된 데이터에 작용하는 필터를 stream copy에 함께 적용할 수 없다. ‘단계가 둘이니 도구도 둘’이라는 추론은 틀린다. |
| decoder 출력과 파일 소비자 입력은 자동으로 같지 않다. | AUD-03: [opusfile v0.12 공식 예제 코드](https://github.com/xiph/opusfile/blob/a55c164e9891a9326188b7d4d216ec9a88373739/examples/opusfile_example.c#L104-L132), [동일 파일 출력 루프](https://github.com/xiph/opusfile/blob/a55c164e9891a9326188b7d4d216ec9a88373739/examples/opusfile_example.c#L224-L385); v0.12 태그 생성 2020-06-27T02:49:06Z | 예제는 `op_read_stereo`의 PCM을 받아 RIFF/WAVE 헤더를 만들고 little-endian으로 써서 48 kHz·2채널·16비트 WAV를 출력한다. 마지막 샘플 수가 선언값과 다르면 seek 가능한 출력의 헤더를 고친다. | PCM 포인터를 WAV 파일 링크와 이어 놓는 것으로는 완결이 아니다. 헤더·endianness·채널 수 계약이 필요하다. 이 예제는 2 GB 초과 때 비표준 헤더 경고를 내며, 이 코드를 모든 길이·모든 소비자에 보편 성공으로 반환하면 안 된다. |
| 앞단 multichannel 인코딩 변경이 불필요한 경우가 있다. | AUD-04: [opusfile 공식 Decoding API](https://opus-codec.org/docs/opusfile_api-0.12/group__stream__decoding.html), 표시판 `0.12-12-gb23e611`; 원판 발행시각 미확인 | `op_read_stereo`/`op_read_float_stereo`는 디코딩과 stereo downmix를 함께 하므로, 두 채널만 받는 플레이어를 위해 원본을 먼저 stereo로 재인코딩할 필요가 없다. 반환은 48 kHz의 interleaved PCM이며 WAV 컨테이너 자체는 아니다. | 출력이 원 채널 배치를 보존해야 한다면 stereo API는 손실이다. 이 웹 API 문서는 v0.12 태그와 정확히 같은 판이 아니라 후속 12커밋 표시판이므로 코드의 v0.12와 같은 바이트라고 주장하지 않는다. |
| 지원 발표와 실제 목적 달성은 별개다. | AUD-05: [WebKit Safari 18.4 공식 발표, Media](https://webkit.org/blog/16574/webkit-features-in-safari-18-4/#media), 2025-03-31 | macOS 15.4·iOS/iPadOS 18.4·visionOS 2.4에서 Ogg의 Opus/Vorbis 지원을 추가했다고 발표한다. MediaRecorder의 WebM/Opus 생성도 별도로 설명한다. | 지원이라는 한 단어만으로 모든 길이의 재생·seek·표시 시간 및 모든 API의 적합성을 보장하지 않는다. |
| 같은 Opus 비트스트림의 컨테이너만 바꿔도 실제 후속 결과가 달랐다는 보고가 있다. | AUD-06: [WebKit 버그 293310 최초 보고](https://bugs.webkit.org/show_bug.cgi?id=293310#c0), 2025-05-20T19:31:05Z; [후속 대조 #c5](https://bugs.webkit.org/show_bug.cgi?id=293310#c5), 2026-09-01T20:52:04Z | 최초 보고자는 Safari 18.5에서 Ogg/Opus 파일의 기준 길이 07:32:36.61이 7:58:26으로 표시되지만 `ffmpeg -i DB100298.opus -codec copy DB100298.webm`으로 같은 Opus 스트림을 WebM으로 옮기면 올바른 시간이 나왔다고 적었다. Vorbis-in-Ogg 변환도 정상이라고 보고했다. | 원 파일은 최초 보고에 첨부되지 않았고 FFmpeg 정확판도 없다. 후속 #c5는 다른 파일·환경의 별도 재현을 같은 버그 사건에 덧붙이며, 독립 사건 수를 늘리지 않는다. 보고자의 원인 추론을 확인된 구현 결함으로 승격하지 않는다. |

## 실제로 이어지는 반환과 이어지지 않는 반환

**연결한 두 링크가 합당한 자리:** ‘Safari 18.5에서 Ogg/Opus 길이가 틀리며 재인코딩을 피하고 싶다’는 조건이면 [FFmpeg stream copy](https://github.com/FFmpeg/FFmpeg/blob/b08d7969c550a804a59511c7b83f2dd8cc0499b8/doc/ffmpeg.texi#L202-L220)와 [버그 293310의 보고된 Ogg→WebM 대조](https://bugs.webkit.org/show_bug.cgi?id=293310#c0)를 연결한다. 중간 계약은 **압축 Opus 패킷 → WebM의 Opus 트랙 → 해당 Safari의 재생**이다. FFmpeg 문서는 첫 변환의 의미를, 버그 보고는 특정 소비자에서의 관측을 지지한다. 두 링크를 합쳐도 우리 실행 성공은 미확인이다.

**한 링크면 충분한 자리:** ‘Ogg/Opus를 stereo PCM으로 받아 재생하고 싶다’면 [opusfile Decoding API](https://opus-codec.org/docs/opusfile_api-0.12/group__stream__decoding.html)의 `op_read_stereo`가 디코드와 downmix를 함께 담당한다. 앞단 재인코더를 추가하면 도구 수·비용만 늘 수 있다. 다만 소비자가 48 kHz·16비트·interleaved PCM을 받는다는 조건을 먼저 명시한다.

**두 링크여도 불완전한 자리:** 위 PCM API와 ‘WAV를 읽는 소비자’의 링크를 바로 잇는 경우다. 원 API에는 WAV 헤더가 없다. AUD-03 공식 예제는 그 빈 연결을 코드로 메우지만 긴 파일의 헤더 한계도 드러낸다. 출력 목적이 정확한 파일 복원이라면 소비자 요구·파일 길이·헤더 생성 여부가 추가로 필요하다.

## 관점별 반환 결정

| 관점 | 반환 형태와 이유 | 판정을 바꿀 한 가지 확인 |
| --- | --- | --- |
| 질문자 | Safari 특정판의 잘못된 길이가 목적이면 위 두 링크와 무재인코딩 대조를 준다. stereo 재생이 목적이면 opusfile API 한 링크를 준다. | ‘최종 목적이 브라우저에서의 정확한 시간축인가, 원 샘플레이트 PCM/WAV 파일 복원인가?’ 두 값은 다른 반환을 만든다. |
| 도구 유지관리자 | [RFC §4](https://www.rfc-editor.org/rfc/rfc7845.html#section-4)와 [버그 원 관측](https://bugs.webkit.org/show_bug.cgi?id=293310#c0)을 연결하고 원 파일·정확한 플레이어 빌드를 요청한다. | 같은 파일의 granule/PCM 기준 길이와 실제 소비자의 `duration`/seek 결과가 일치하는가? |
| 탐색기 편집자 | 컨테이너·코덱·플레이어·목적·버전을 한 슬롯으로 합치지 않는다. 원본 파일과 정확판이 없으면 ‘보고된 우회법, 현 실행 미확인’으로 유보한다. | 현재 대상판에서도 Ogg만 실패하고 같은 Opus의 WebM은 성공하는가? 양쪽 성공이면 우회 변환 권고를 제거한다. |

## 자체 반증 점검과 분모

직접 읽고 최소량에 산입할 고유 자료는 **6건**, 보수적인 독립 저작/사건은 **5건**이다. AUD-03 코드와 AUD-04 문서는 같은 opusfile 계보로 묶었다. 현행 FFmpeg HTML과 n7.1 고정 원문은 같은 저작의 판이므로 두 건으로 늘리지 않는다. WebKit 버그의 댓글·최초 보고도 한 사건이다. 원장에는 접근 실패와 불충분 독해도 남기고 최소량에서 제외했다.

오디오 자료만으로 여섯 신규 질문에서 B가 우세하다고 추론할 수 없다. 오히려 AUD-02/04는 기존 도구 안에서 이미 여러 단계를 처리해 인접 도구 추가가 불필요한 반례다. AUD-06은 인접 단계가 문제를 우회할 수 있다는 특정 환경의 공개 사용 보고다. 이 차이를 신규 대응쌍의 실험 효과나 독립 맹검으로 바꾸지 않는다.

다음 최소 관측: 버그 293310의 원 파일 또는 공개 후속 표본 한 개를 정확한 FFmpeg·Safari 버전으로 고정하고, Ogg/Opus와 stream-copy WebM/Opus의 패킷 동일성·`ffprobe` 길이·브라우저 `duration`·동일 시간 seek를 대조한다. 현재 조사에서는 실행하지 않았다.
