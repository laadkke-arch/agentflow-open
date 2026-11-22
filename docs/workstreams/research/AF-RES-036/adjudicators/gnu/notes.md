# GNU 기준판정 — AF-RES-036

## 결과와 접근 범위

G01–G06은 모두 **KEEP, confirmed=true**다. 6개 원 href를 직접 GET하고 각 목적에 필요한 본문을 읽었다. G01은 HTTP 301→HTTPS 200, 나머지는 직접 200이다. `original_http_status`는 fetchlib가 redirect를 따른 뒤의 terminal status이며, 최초 응답은 별도 `original_initial_http_status`와 redirect chain에 남겼다. 상태 코드만으로 결론을 내리지 않았다.

모든 48결정의 원격 봉인 SHA는 작업 지시상 `5fbde38a04613fbd6f057fd562bd173b7193f2c9`다. 이 문맥은 지시 파일, 자기 input, 허용된 fetchlib, 자기 산출물과 새 공개 원문만 읽었다. 타 카드, N/H, 수집결과, 판독결정, 타 요약/기준 파일은 열지 않았다. 동일 모델계열의 별도 문맥이며 인간·다른 모델의 독립 검증이 아니다. 원출처가 같은 경우를 독립 발행자 근거로 늘리지 않았다.

## 목적·판의 판정

- **G01:** 2018 POSIX Shell and Utilities 실제 본문에 도착한다. B는 shell/utilities를 지목하며 별도 연도나 최신판을 명시하지 않는다.
- **G02:** 원 repository root에서 completion recipe 안내와 실제 GNU find/make 예제에 도달한다. 원 인용은 특정 bash-completion 판/API를 고정하지 않는다.
- **G03:** 원 각주가 명시한 **2018** 판이 그대로 있다. newer 안내의 Issue 8/2024는 같은 요구 판이 아니다.
- **G04:** 현재 Edition 5.4의 원 fragment와 |& / print·printf / getline 설명이 유효하다. 실제 보존 Edition 5.1 chapter와 좁은 기능 의미를 대조했다.
- **G05:** current GCC 원 fragment 및 -MM 규칙이 유효하다. GCC 10.1.0 보존판과 2020-05-07 공식 release history를 대조했으나 B에 없는 target 판을 강제하지 않았다.
- **G06:** 원 directory에 1.0 source가 있고 공식 project page가 latest 1.0, 날짜 있는 공지가 stable 1.0을 확인한다. 원 한 문장에 stable 단어는 없으며 인접 prerelease 구별 및 공지에서 보강했다.

## 실제 반례 관측 — 원 표본을 추가하거나 바꾸지 않음

1. **새판 안내가 있어도 원판 보존이 더 정확함:** 2018 POSIX main은 newer를 안내하되 2018 본문을 계속 제공한다. 새 main을 실제 취득하면 Issue 8 / IEEE 1003.1-2024다. G03을 새판으로 바꾸면 명시된 판을 잃는다.
2. **200이나 expected fragment가 없음:** 2024 `V3_chap02.html#tag_18`을 실제 GET했다. 응답은 200이나 전체 HTML의 `id` 또는 `a[name]`에 `tag_18`이 없다. 실제 chapter anchor는 `tag_19`이며 그 URL도 별도 GET 200, 동일 body SHA-256이었다. 2018 chapter의 `tag_18`은 실제 존재한다. **G01/G03 원 href에는 fragment가 없다.** 이것은 새판으로 검증된 하위절을 기계적으로 옮기는 보조 URI의 반례이지 원 href 자체의 anchor 실패가 아니다.
3. **살아 있는 하위 디렉터리가 기대 예제 모음을 담지 않음:** `https://github.com/scop/bash-completion/tree/ddf4f5e44818e00c51e984c019c15b6d73a2e79b/completions`는 200이지만 tree가 Makefile.am/README.md 두 항목이다. 안내문은 external files 위치라고 하며 구현 예제를 `completions-core`로 보낸다. `https://github.com/scop/bash-completion/tree/ddf4f5e44818e00c51e984c019c15b6d73a2e79b/completions-core`와 그 아래 find.bash/make.bash를 실제 읽었다. 원 B는 repository root이므로 이 반례는 원 href의 KEEP을 바꾸지 않는다.

G04/G05 원 fragment에서는 누락을 찾지 못했다. G06은 latest/stable 문서 대조 범위에서 잘못된 배포 위치를 찾지 못했다. 관측하지 않은 반례를 양성으로 만들지 않았다.

## 기록과 재현

`attempts.jsonl`에는 **34개 직접 GET**과 검색 발견 1건이 있다. 원배포 4개 archive와 인용 member 6개를 재취득했고 input의 모든 SHA-256과 일치했다. GET received-body byte 합계는 **28,497,924 bytes**이며 wire bytes는 측정되지 않아 null이다. elapsed는 각 요청 측정이며 병렬 wall time과 같지 않다. GitHub API 날짜 요청 한 건은 rate-limit 403이었고 공개 commit HTML로 대체해 날짜를 확인했다. 로그인·설치·프로그램 예제 실행은 없었다.

`sources.jsonl`은 실제 읽은 범위, 정확 raw 발췌, 전체 source 및 archive/member SHA-256, 0-based byte 시작/끝(끝 exclusive), 1-based 줄 위치, URL, 판, 날짜의 종류, 조회 UTC, 한계를 기록한다. 날짜가 없는 문서는 publication_date=null이며 copyright/file mtime/commit date/페이지 Updated를 발행일로 바꾸지 않았다. 검색 요약과 API 오류는 count=false다. count=true는 읽은 원문 증거 자격이지 새 고유 출처 수나 독립 출처 수를 뜻하지 않는다. root에서 동일 hash/문서/발행자 중복군을 합칠 수 있다. POSIX 두 원 요청의 body는 같고, 새판 fragment 두 요청도 같은 body다.

발췌는 정확 수신 bytes의 UTF-8 표현이다. Debian changelog만 명시된 gzip 변환 뒤 bytes를 excerpt 대상으로 하며 compressed member hash도 따로 남긴다. 동적 GitHub HTML은 CSRF 등과 함께 달라질 수 있으므로 전체 hash가 재요청에 불일치할 수 있다. 실제 예제/README는 관측 commit SHA에 고정했다. `verify-evidence.py SOURCE_ID`는 한 source를 다시 GET하여 carrier/member/source hash와 excerpt slices를 확인하는 선택적 재현 도구이며 사이트의 이후 변경을 성공으로 숨기지 않는다.

큰 raw archive, HTML 원문과 build 스크립트는 로컬 재현 중간물로만 두고 commit whitelist에서 제외했다. **원격 보존 대상은 `commit-files.json`의 owned-root 상대경로 목록만**이다. 추가 문서 fetch가 필요한 과거 응답이나 검증하지 않은 2.11 판, gettext 1.0 archive 실행/서명 검증을 확인된 사실로 쓰지 않았다.
