# 원본 접근과 복구

- SQLite 출시판 소스의 shell 직접 HTTP와 canonical Fossil file/artifact의 웹 열람이 실패했다. 공개 SQLite 프로젝트 GitHub mirror의 고정 tarball에서 시험 바이트를 얻었다. 릴리스 manifest에서 지시한 마지막 라인을 제거한 SHA3-256이 SQLite 공개 release source ID와 일치했다. 네 시험 바이트의 SHA3-256도 해당 manifest 항목과 일치했다. 스크립트 최초 실행은 Git용 지시 라인까지 포함해 manifest 검산에서 종료 1이었다. 지시 라인만 제거해 재개했다. 원 artifact 사이트 직접 열람은 미확인이다.
- SQLite 3.51.1 문서 ZIP, 날짜 기반 Fossil docsrc 네 파일 및 타임라인은 Cloud 또는 web에서 읽지 못했다. 출판자 본문 네 페이지의 전체 번호 붙은 라인을 비교했다. 과거판과의 동일성, 원시 HTML 좌표는 미확인이다.
- W3C 2025 스냅샷은 web에서 직접 열었다. Cloud 셸에서 원시 HTML CONNECT는 HTTP 403이었다. 번호 붙은 HTML 텍스트 보기의 SHA 및 좌표를 보존했다. 원시 HTML 좌표는 미확인이다.
- The Open Group POSIX.1-2017/2024 fnmatch는 두 웹 경로의 직접 열기에서 403이었다. GNU Savannah 원 시험 링크도 열리지 않았다. 교정에서는 man7가 재게시한 POSIX 문서와 공식 Gnulib의 GitHub mirror 시험을 읽고 실제 C 출력을 비교했다. 양쪽 원 도메인 직접 열람은 미확인이다.
- SVG manual fixture의 Chromium file URL은 net::ERR_BLOCKED_BY_ADMINISTRATOR였다. 같은 고정 SVG 바이트를 localhost 테스트 응답으로 공급해 원 경로 좌표의 성공 출력을 얻었다. 주 WPT 실행은 처음부터 localhost에서 했다.
