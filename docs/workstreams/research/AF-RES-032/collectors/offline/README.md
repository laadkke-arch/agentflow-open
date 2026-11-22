# 경로 D 중 PostgreSQL·SQLite: A 원판 봉인 준비

2026-11-22T07:15:14.803009Z에 4참조를 준비했다. 전체 A를 원격 봉인하는 root의 gate 이전에는 링크 목적지와 소비자의 후속 배포판을 열지 않았다. `references.jsonl`은 이 단계 원판 판단이고, 이후 사실은 별도 파일에 추가해야 한다.

| ID | 실제 배포판·멤버 | 원 href | 원문에서 읽은 목적 |
| --- | --- | --- | --- |
| A-D03 | PostgreSQL 12.2 / doc/src/sgml/html/acronyms.html | https://en.wikipedia.org/wiki/American_National_Standards_Institute | ANSI 약어가 가리킨 기관의 배경 |
| A-D04 | PostgreSQL 12.2 / doc/src/sgml/html/app-psql.html | https://tools.ietf.org/html/rfc4180 | psql CSV 출력의 명시된 RFC 4180 인용부호 규칙 |
| A-D05 | SQLite 3.31.0 / about.html | http://en.wikipedia.org/wiki/Endianness | 플랫폼 간 파일 복사의 big/little-endian 배경 |
| A-D06 | SQLite 3.31.0 / aff_short.html | http://www.darwinsys.com/file/ | application_id 맥락의 file(1) 파일 유형 판별 도구 |

PostgreSQL에서 `ftp.postgresql.org/pub/doc/`와 `/pub/doc/12.2/`, 웹 `/ftp/docs/12.2/`는 직접 GET 404였다. 공식 `/pub/source/v12.2/`에 공개된 `postgresql-12.2.tar.bz2`를 열었더니 이미 빌드된 HTML 1,099개가 `doc/src/sgml/html/`에 들어 있었다. 따라서 별도 docs 전용 tar가 있다고 주장하지 않고 **공식 source 배포 tar에 포함된 오프라인 HTML**이라는 실제 형식을 기록했다. 제품 소스의 `.sgml`만 본 것이 아니며, HTML을 새로 빌드하지도 않았다.

PostgreSQL 원장의 2020-02-10 22:29는 파일시각이고 공식 배포물 안 `release-12-2.html`은 Release date 2020-02-13을 말한다. 날짜 역할이 다르므로 원장시각을 최초 출판일로 바꾸지 않는다. SQLite 공식 chronology와 배포물의 `releaselog/3_31_0.html`은 2020-01-22를 말한다. 두 제품 모두 실제 독자의 열람/실패는 미확인이다.

사전 경로순 표집은 31문서까지 검사해 외부 URL 없는 문서27개와 선택4개를 기록했다. 선택된 문서의 첫 절대외부링크는 모두 본문이었다. 따라서 탐색 범위 안 navigation/footer/가상 URL 때문에 제외한 절대외부링크는 각각0이다. 표집 스크립트가 그 뒤 몇 개 원판 문서의 링크 요약도 출력했으나 표본은 첫2개로 그대로 유지했으며 목적지는 열지 않았다. HTML 파서의 내부링크 수와 문서별 검사는 `frame.csv`에 남았다. 개별 패키지명 토큰은 전수 세지 않았으므로 URL 없는 패키지명 제외를 별도 수치로 꾸미지 않는다.

`excerpts/`의 4개 표본 HTML은 원본 bytes 그대로다. 원 배포물은 각각 SHA256과 멤버 경로로 재다운로드할 수 있다. 대형 archive와 원장 캐시는 `cache/` 아래 있으며 커밋에서 제외한다. `build_a.py`는 이미 받은 archive만 읽으며 네트워크 요청을 하지 않는다. 실행은 소프트웨어 설치/부팅/동작 시험이 아니라 문서 bytes 추출이다.

수집 과정의 최초 보조 파싱에서 `bs4`가 설치되지 않아 한 셸 실행이 종료코드1로 끝났다. 신규 패키지를 설치하지 않고 표준 라이브러리 `html.parser`로 바꿔 완수했다. 접속시도와 실패는 `attempts.jsonl`에 기록했다. 그 스크립트가 끝나기 전에 요청한 원장은 이후 명시적으로 다시 읽어 기록했고, 미기록 응답을 성공 원문으로 세지 않았다.
