# GNU N/H 수집 묶음 — 판독·기준판정 이전

원 B는 원격 `bd3c17ef2f989b3d9e0566405d82357fc17f47bb`에서 봉인된 뒤 N/H를 수집했다. 이 묶음에는 유지·교체·보류 결정이나 기준판정을 쓰지 않았다. `references.jsonl`과 `base/G01.txt`–`base/G06.txt`는 변경하지 않았다.

## 바로 사용할 입력

`evidence-components.jsonl`의 `reference_id`, `N.text`, `H.text`가 정확한 입력 문자열이다. 별도 파일 `components/G01-N.txt`–`components/G06-H.txt`와 바이트가 같다. 각 성분에는 SHA-256, 유니코드 문자 수, UTF-8 바이트 수, 출처 ID, 원문 SHA-256, 정규화 방식·정규화 원고 SHA-256·문자 offset이 있다. `N.original_request`에 조회 UTC·실제 상태·redirect·최종 URL을, `H.historical_documents`에 사건/판 시각과 원 URL을 분리했다. 메타데이터는 원문 발췌 문자열에 끼워 넣지 않았다.

| 참조 | N 원문 문자/바이트 | H 원문 문자/바이트 | 직접 확인한 자료·위치 | 특별한 제한 |
| --- | ---: | ---: | --- | --- |
| G01 | 143 / 143 | 652 / 652 | G-N01: POSIX 2018 목차와 Shell Command Language 실제 장; G-H01: 2020-12-07 Bash 5.1 발행 공지 | 원 HTTP는 실제 301→HTTPS 200. N에 newer-edition 문구가 있다. H는 발행자 배경·문서 역할 설명이고 URI 변경 이력은 아니다. |
| G02 | 475 / 475 | 458 / 458 | G-N02: bash-completion 현재 README Introduction; G-H02: 2.11 태그 README; G-H05: 2020-07-25 2.11 발행 기록 | 현재 default branch와 release text는 가변적이다. 2.11 태그의 조회 바이트는 해시로 고정했지만 태그 자체를 완전 commit SHA로 pin하지는 않았다. |
| G03 | 143 / 143 | 102 / 102 | G-N01 공유; G-H06: gawk 5.0.1 배포 `doc/gawk.info` Preface 각주 | B는 2018이라고 쓰지만 이전 5.0.1 문서는 2008이라고 쓴다. H 원문을 B에 맞춰 고치지 않았다. N에 newer-edition 문구가 있다. |
| G04 | 1519 / 1532 | 890 / 890 | G-N04: 현재 GNU gawk §12.4 및 원 fragment; G-H06: 5.0.1 info의 Two-way I/O node | 원 fragment 존재와 `|&`·print/printf/getline 문장을 직접 읽었다. 프로그램 실행은 하지 않았다. G03과 H 원고 1개를 공유한다. |
| G05 | 372 / 377 | 349 / 353 | G-N05: 현재 GCC `index-MM`; G-H03: GCC 10.1.0 versioned manual의 -MM 절 | 원 `Preprocessor-Options` fragment와 필요한 `index-MM` 절을 모두 확인했다. 과거 문서 날짜는 HTTP Last-Modified이며 최초 발행 시각으로 보지 않는다. |
| G06 | 271 / 276 | 180 / 180 | G-N06: GNU gettext 배포 목록의 1.0 실제 행; G-H07: 2020-07-27 gettext 0.21 발행 공지 Download 절 | 표집 중 같은 목록을 이미 연 G-GET035 노출을 유지한다. 원 B 선택을 바꾸지 않았다. directory timestamp는 최초 발행 시각과 같다고 가정하지 않는다. |

N/H 각각 원문 총문자도 모두 1600 이하이다. 여러 span을 잇는 경우 빈 줄 두 개를 정확한 구분자로 사용했으며 카드 SHA-256은 그 구분자까지 포함한다. G01/G03 N은 문자열과 해시가 완전히 같다.

## 현재 확인창과 추가 조회

원 href 여섯 개는 2026-11-22 15:57:09 UTC에 같은 배치로 요청했다. 여섯 요청의 종료는 15:57:25 UTC 이전이다. 원 G01의 HTTP를 HTTPS 지원 요청으로 대체하지 않았고, 실제 301 redirect를 기록했다. 여섯 original GET의 최종 상태는 모두 200이었다. 이는 본문·판·목적 적합 판정이 아니다.

POSIX 도착 페이지가 frameset이어서 실제 필요한 내용을 읽기 위해 다음 세 요청을 추가했다. G01/G03은 물리적 1회 취득을 각각 논리적으로 사용한다.

1. G-NGET007: `https://pubs.opengroup.org/onlinepubs/9699919799/mindex.html`
2. G-NGET008: `https://pubs.opengroup.org/onlinepubs/9699919799/utilities/toc.html`
3. G-NGET009: `https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18`

실제 필요한 절까지 포함한 N 확인창은 15:57:09.267926–16:00:08.752615 UTC다. 원래 여섯 요청과 이 추가 세 요청을 혼합해 여섯 번만 요청했다고 세지 않는다. URL fragment는 HTTP 서버에 별도 전송되지 않으며, 도착 HTML의 `id`/`name`을 로컬에서 확인했다.

## 출처 중복과 직접 읽기 범위

`sources.jsonl`에는 B 원배포 문서 6개, 적격 현재 원고 5개, 적격 독립 과거 원고 6개, 최소수에서 제외한 보조 원고 2개가 있다. 적격 합계는 17개다. 과거 README와 발행 공지는 다른 원고이나 같은 사건이므로 독립 사건 수가 6개라는 의미는 아니다.

현재 POSIX의 root·frame·목차·실제 장과 G01/G03 요청은 한 원고로 센다. gawk 5.0.1 info의 Preface와 Two-way I/O 두 절도 한 원고로 센다. G-H06은 실제 공식 source tarball에 포함된 info 문서이고, 빌드 HTML이라고 부르지 않는다. H에 원 B 문서만 재활용해서 과거 독립 수를 채우지 않았다.

과거 적격 고유 출처는 다음과 같다.

- G-H01: `https://lists.gnu.org/archive/html/info-gnu/2020-12/msg00003.html` — Bash 5.1 발행 공지.
- G-H02: `https://github.com/scop/bash-completion/raw/refs/tags/2.11/README.md` — 2.11 태그 README.
- G-H03: `https://gcc.gnu.org/onlinedocs/gcc-10.1.0/gcc/Preprocessor-Options.html` — versioned GCC 10.1.0 문서.
- G-H05: `https://github.com/scop/bash-completion/releases/tag/2.11` — 2.11 발행 설명과 실제 datetime 속성.
- G-H06: `https://ftp.gnu.org/gnu/gawk/gawk-5.0.1.tar.xz` → `gawk-5.0.1/doc/gawk.info` — 두 절이 들어 있는 이전 배포 원고.
- G-H07: `https://lists.gnu.org/archive/html/info-gnu/2020-07/msg00009.html` — gettext 0.21 발행 공지.

현재 IEEE catalog(G-H04)는 과거 표준 발행 날짜와 2024 supersession을 함께 담은 오늘의 기록이므로 H 카드와 strict 과거 최소수에서 뺐다. Open Group 2018 회고(G-X01)는 관련 UNIX 부분을 직접 읽었지만 필요한 POSIX 판 식별을 제공하지 않아 카드와 최소수에서 뺐다. archive thread index 세 개는 발견용 조회로만 기록했다.

## 누출·배경·노출 민감도에 넘길 표지

- **카드 N 자체에 과거/후속 이력이 보이는 경우:** G01/G03의 `A newer edition of this standard exists`. N이 순수하게 현재 내용만 제공한다고 주장할 수 없다.
- **전체 현재 원고에 이력이 있으나 선택된 N span에는 없는 경우:** G02의 README 후반 이전 Bash 버전 설명, G06의 과거 배포 행. strict source-level 제외와 selected-excerpt-level 제외를 구분할 수 있다.
- **사전 현재 목적지 노출:** G06. source discovery용 디렉터리 관측 G-GET035가 B 봉인보다 앞선다. stricter 현재 열람 전 표집 분석에서 제외할 수 있도록 보존한다.
- **발행자 배경 H:** G01. 발행자 설명이 주는 배경과 특정 URI 변경 이력을 같은 종류로 세지 않는다.
- **판독 노출:** 이 수집자는 B/N/H와 전체 자료를 읽었다. 이 수집자의 자체 재검을 새 미노출 판독으로 계산하지 않는다. 실제 48판독은 root의 별도 문맥 배치가 담당한다.

## 실제 비용과 미계측

`costs.csv`는 `attempts.jsonl`의 원 시각·상태·byte·경과와 조인된다. N은 실제 GET 호출 9회, 실패 0회, 받은 최종 응답 body/저장된 응답 각각 1,158,390바이트, redirect hop 1회였다. H 수집·대체 탐색은 GET 호출 11회, 실패 0회, 각각 3,647,599바이트, redirect hop 1회였다. H 11회에는 카드에 넣지 않은 catalog·회고·목록 탐색도 포함한다. 최소 HTTP 요청 수는 각 호출에 기록된 redirect hop을 더한 값이다. 중간 redirect 응답 body와 프로토콜 overhead는 body 바이트 합계에 포함되지 않는다.

N 각 요청 경과의 합 61.642127초와 H 합 72.182722초는 네트워크 도구 요청 경과 합계다. 병렬 요청이 있으므로 연구자 wall time이나 노동 시간으로 부르지 않는다. 전체 G-GET001–053 초기 발견 조회는 53회·오류 7회·77,473,354 응답 바이트로 별도 기록했다. 이것만으로 C0의 전체 최초 발견 비용을 관측했다고 말할 수 없다.

카드 독해 시간, 사람 노동, 실서비스 비용, 재열람 클릭 수, TCP/TLS 비용, 실제 disk block 할당은 미계측이다. fetch가 기록한 저장 바이트는 원 응답 저장량이고 추출·파싱 파일의 중복 저장 전체를 뜻하지 않는다. 이 단계에서 두 번째 C1/C2 조회의 실제 재생을 하지 않았다. 이 파일에는 비용 이익 추정이나 모델 계산을 넣지 않았다.

## 재구성 검사와 원격 보존 경계

실제 실행한 검사:

```sh
python -B docs/workstreams/research/AF-RES-036/collectors/gnu/reconstruct_nh.py
```

종료 코드 0. `nh-reconstruction-receipt.json`: 12개 성분의 원 소스 바이트·정규화·offset·정확 문자열 일치, 출처 ID 전체 조인, B6 불변. 이 검사는 자료 생성자의 자체 재검이며 독립 판독이 아니다. 컴파일·shell coprocess·Bash completion 실행은 수행하지 않았다.

커밋된 작은 파일만으로 정확한 입력을 재검할 명령:

```sh
python -B docs/workstreams/research/AF-RES-036/collectors/gnu/reconstruct_nh.py --cards-only
```

원 응답 파일이 없을 때 실제 재취득하는 명령:

```sh
python -B docs/workstreams/research/AF-RES-036/collectors/gnu/reconstruct_nh.py --download-missing
```

후자는 재요청을 별도 `replay-nh/attempts.jsonl`에 기록한다. 가변 현재 페이지는 나중에 전체 응답 SHA가 달라질 수 있다. 그 경우 기존 카드와 기록한 해시는 보존하고 byte drift를 실패로 보고하며 새 내용으로 바꿔 통과시키지 않는다. 과거 gawk source archive는 기록된 SHA를 검사한 뒤 지정 info member를 추출한다.

원격 커밋 후보는 `commit-files-nh.json`에 열거한다. 큰 원 배포물과 현재 전체 HTML을 모두 원격 보관했다고 주장하지 않는다. 원 URL, 시점, exact excerpt, source/member/normalization SHA, offset과 재취득 코드를 함께 남긴다. HTTP body가 사라지거나 바뀌면 exact 카드 자체는 재생 가능하지만 원 전체 문맥 재구성은 실패할 수 있다는 한계를 유지한다.
