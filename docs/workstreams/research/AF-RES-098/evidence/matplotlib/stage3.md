# Matplotlib ③ 본문·실물·발행 조사

② 원격 봉인 `0df9ea9edbcee995d631eef54b65fd43f73c245f` 뒤 원 payload를 읽었다. 주 4자리 모두 P=YES/U=YES/G=UNKNOWN, 두 사전 U 예측은 참이다. 상세 지문·URI·태그·절·변형은 [audit.json](audit.json), 4행은 [lineage.csv](lineage.csv)에 있다.

## 실제 참조와 바이트

3.7.0의 `410d8388303fab638bbedbd1d2eace0e5efb0de9`는 final 문서 업데이트, 3.7.1의 `dbd81bd88621dbfee4c0da45e62a5aeb5722378c`는 Add docs for 3.7.1 발행이다. 두 예제 본문의 버전 title과 정확 h1 절을 확인했다. 각 본문에 base 요소는 없고, 해당 절의 PNG src 및 2.0x srcset을 각각 실제로 받았다. 두 판·두 예제·두 배율의 PNG는 8개이며 1x가 주 판정 대상이다. HTTP image/png와 PNG signature/CRC가 맞는다. 실제 브라우저의 DPR별 선택이나 애니메이션 실행은 관측하지 않았다.

- MP1 `#pyplot-animation`: 1x는 두 판 모두 17,836B, 640×480. 파일 SHA는 `3414ef1e71a2…`→`2280b66b044b…`.
- MP2 `#pausing-and-resuming-an-animation`: 1x는 두 판 모두 18,016B, 640×480. 파일 SHA는 `677df082dba5…`→`5adbb2acc3c6…`.
- 네 배율 대응쌍 모두 바뀐 PNG data chunk는 Software tEXt뿐이다. CRC도 그 내용에 따라 바뀐다. IDAT와 압축 해제 scanline은 같다. 따라서 같은 이름·같은 길이가 같은 바이트를 보장하지 않지만, 바이트 변경이 그림 픽셀 변경을 뜻하지도 않는다.

같은 두 Python 예제 소스는 두 release source commit에서 각각 같은 바이트다. 새 HTML의 실제 .py download 두 개도 그 source와 일치한다. MP1에는 난수 seed 19680801이 있고 최종 frame49가 보인다. MP2의 source는 정적 문서에서 상호작용을 볼 수 없음을 설명한다. 현재 보여지는 PNG를 실행 가능한 pause/resume 기능으로 오인하지 않는다.

## 생성 기록의 경계

v3.7.0 source는 `d6dd1b79142e4e2483244c25ff1e3ddb664722d3`, v3.7.1은 `b3bd929cf07ea35479fded8f739126ccc39edd6d`다. 공식 release guide는 tagged library를 설치하되 ver-doc 브랜치에서 문서를 만들고, 결과를 rsync하여 발행 저장소에 넣도록 한다. 태그만으로 정확한 ver-doc 입력이나 의존성 전체를 고정할 수 없다. requirements의 sphinx-gallery>=0.10도 실제 실행판을 특정하지 않는다.

소스 SHA에 대한 현재 Actions 목록은 total_count=0이었다. 발행 SHA의 직접 HTTP 질의는 403이고, 승인된 GitHub connector로 같은 공개 질의를 읽자 total_count=0이었다. 실패/빈 목록을 역사적 작업 부재로 판정하지 않았고 최소 자료 수에도 넣지 않았다. [fallback](actions-fallback.json)

공식 Sphinx-Gallery 0.11.1의 source MD5/`run_stale_examples` 분기를 읽었다. unchanged example을 건너뛰는 기전이 있지만, 이것을 이 release가 실제 사용한 정확 버전·실행으로 격상하지 않는다. Matplotlib의 release 절차는 별도의 clean build를 지시한다. 서로 다른 규칙의 존재와 실제 실행 관측을 구분한다. [짧은 규칙 발췌](build-excerpts.json)

PNG의 Software 버전 표지는 producer 설명이다. 이번 특정 job이 이 바이트를 생성했다는 입력·실행·출력 digest 연결은 찾지 못했다. G는 네 자리 모두 UNKNOWN이다.

## 내장 data URI 보조

모집 순서 첫 `animate_decay.html`에는 이름 있는 외부 결과 이미지 대신 JavaScript의 100개 frames가 있고, 첫 frame은 data:image/png;base64이다. 실제 첫 PNG를 디코딩해 SHA256 `b83a9adafd5ed3a13a70ae4258c84147720a17b7b79c922de96f868398a3d0e4`와 CRC를 확인했다. `new Image().src=frames[i]`, `new Animation(frames, img_id, ...)`의 정적 연결도 읽었다. 별도 웹 PNG URL은 필수가 아니다. 애니메이션 재생 성공은 미검증이다. 이 본문은 실제 읽은 자료이며 주 6쌍에는 추가하지 않는다.

## 비용과 재현

선정된 두 예제의 두 판 HTML은 4개, 1x PNG는 4개, srcset PNG는 4개로 주요 읽기 대상 12개다. 동일 bytes가 아닌 자료의 source-count와 실제 GET 횟수는 구분한다. 소스 4개·실제 download 2개·메타데이터/규칙 요청은 영수증에서 별도로 읽는다. 선행 제외 예제 7개와 버전 주소의 역사 wrapper 차이를 확인한 요청도 주 payload 검증 비용과 분리한다.

`python -B docs/workstreams/research/AF-RES-098/tools/inspect_mpl.py`는 수집 시 임시 캐시로 HTML/PNG를 판독한 절차다. 원문·이미지 전체는 커밋하지 않았다. 일반 재확인은 최종 reproduce.md의 정확 URL 재수신 절차를 사용한다. 로컬 파서 첫 시도에서 JS 세미콜론을 가정해 실패한 것은 수정 후 유효 PNG를 다시 검사했고 [접근·교정 기록](../access-notes.json)에 남겼다.
