"""Render the research report from sealed references and observed ledgers.

No network access. Does not modify sampling, references, sources, or judgments.
Narrative cells are authored interpretations, not additional primary evidence.
"""
from pathlib import Path
import csv
import json

P = Path(__file__).resolve().parents[1]
CASES = json.loads((P / "evidence/cases-normalized.json").read_text())
REFS = {r["reference_id"]: r for r in map(json.loads, (P / "references.jsonl").read_text().splitlines())}
SOURCES = {r["source_id"]: r for r in map(json.loads, (P / "sources.jsonl").read_text().splitlines())}
COMPS = {r["reference_id"]: r for r in csv.DictReader((P / "comparisons.csv").open())}

def link(label, url):
    return f"[{label}]({url})" if url else f"{label}（URL 미확인）"

def src(sid):
    return link(sid, SOURCES[sid]["original_url"])

def cell(x):
    return str(x).replace("|", "\\|").replace("\n", " ")

def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"] + ["| " + " | ".join(map(cell, row)) + " |" for row in rows])

def boundary(c):
    old, new = c.get("last_old"), c.get("first_observed_new")
    def one(x):
        if not x:
            return "미관측"
        return link(x.get("version", "판"), x.get("url") or x.get("archive_url"))
    return one(old) + " → " + one(new)

# Each entry: surrounding-text paraphrase, upstream evidence, consumer outcome,
# concrete unknown and next material, clock start, clock end, qualification,
# counterexample for the three-view table. Original wording remains in REFS.
N = {
"A-D01": [
    "Python 도움말은 reStructuredText 원문을 Sphinx로 만든다고 설명한다. 문서 형식의 배경을 읽는 목적이다.",
    f"2026-11-22 원 URL은 301→301→200으로 SourceForge.io에 도착. 공식 형식 설명은 존재({src('P-U01')}); 이전 시행일 미확인.",
    "3.8.2–3.8.20 전체 19판의 about.html에서 원 href 유지. 신규 href 판 없음.",
    "미확인: 이동일·과거 본문 연속성. 마지막 확인은 현재 본문과 19판; 다음은 날짜 고정 Docutils 이전/redirect 기록.",
    "상류 시행 미확인; 현재 관측 2026-11-22", "19판에서 변경 종점 미관측", "엄격 부적격; 시작 미상, 검열 아님",
    "오래된 호스트명이지만 현재 같은 형식 설명을 제공한다. 특정 markup 판 재현 요구는 원문에 없다."],
"A-D02": [
    "문서 오류를 신고하기 전 기존 열린 문서 오류를 찾는 query다. 현재 문제의 중복 신고를 피하는 목적이다.",
    f"공식 상태 보고 2022-04-08 18:15Z read-only, 04-10 19:30Z 이전 완료({src('P-U04')}, {src('P-U05')}). 원 query는 현재 200이지만 동결 목록.",
    "3.8.14(2022-09-06) 옛 query → 3.8.15(2022-10-11) GitHub docs-label query. 3.8.2–20 전 19판 확인, 사이 누락 0. 날짜는 판 공표일이며 HTML 최초 공개 UTC는 미확인.",
    "미확인: 서버 실제 잠금 시각·해당 tarball 최초 출판 UTC·동일 offline 판 독자 클릭. 다음은 3.8.15 HTML hash를 명명한 출판 영수증.",
    f"공식 상태 관측 2022-04-08 18:15Z ({src('P-U04')}); 실제 시행 시각은 미확인",
    f"소스 committer 2022-09-11 18:50:47Z ({src('P-C01')}); 3.8.15 판 공표 2022-10-11",
    "엄격 부적격. 상태 보고→committer 명목 차이 13,480,547초(156일 00:35:47)만. 분 표시를 실제 시행의 60초 bound로 쓰지 않음.",
    "HTTP 200인 동결 목록은 현재 열린 문서 오류를 찾는 목적을 충족하지 못한다. 실제 독자 보고는 live /3/ 페이지여서 이 offline 사슬과 합치지 않음."],
"A-D03": [
    "약어 표에서 ANSI의 전체 이름을 외부 설명에 연결한다. 표준기관 명칭의 배경 읽기다.",
    f"현재 문서의 기관 설명 확인({src('PG-U01')}). 2020 revision 938900783 metadata는 확인했지만 본문 403; 옛 의미 상태 미확인.",
    "PostgreSQL 12.2–12.22의 실제 archive 21개 모두 acronyms.html의 href 유지.",
    "미확인: 2020 본문·독자 클릭. 다음은 revision 938900783의 날짜 고정 전체 본문.",
    "상류 변경 시작 미관측", "12.22(2024-11-21 판 공표)까지 원 href", "엄격 부적격; 변화가 없었다는 역사 전체 주장 불가",
    "현재 배경 설명은 맞지만 현재 내용만으로 2020 본문이 같았다고 소급하지 않는다."],
"A-D04": [
    "psql의 CSV 출력에서 쉼표·줄바꿈·따옴표 처리 규칙을 RFC 4180으로 설명한다. 번호가 고정된 형식 명세를 읽는 목적이다.",
    f"2022-06-17 IETF 전환 공지 및 09-14 완료 보고. 특정 /html/rfc4180 시행일 미확인. 현재 옛 URL의 최종 RFC Editor 본문에도 필요한 §2 존재({src('PG-U02')}, {src('B05-U-BOARD20220914')}).",
    "12.18(2024-02-08) tools.ietf → 12.19(2024-05-09) datatracker.ietf. 12.2–22 전 21판, 사이 누락 0. 같은 CSV 문단의 href만 변경.",
    "미확인: RFC별 redirect 시행·HTML 최초 공개 UTC·독자 실패. 다음은 RFC4180 경로의 날짜 있는 배포/config 영수증.",
    f"상류 일반 서비스 전환 공지/완료 보고; 특정 URI 시행 미확인 ({src('B-U05')}, {src('B05-U-BOARD20220914')})",
    f"소스 2024-04-10 11:53:25Z ({src('PG-F-SOURCE12')}); 12.19 공표 2024-05-09 ({src('PG-F-NEWS1219')})",
    "엄격 부적격. 공표일과 소스 날짜의 달력 차이 29일만; 공표 시차·정확 HTML 공개시각 미상이라 UTC 지연 아님.",
    "편집자가 왕복 redirect를 줄이려고 href를 바꿔도 원 독자는 여전히 같은 RFC를 읽을 수 있다. 수정됨과 지금 교체 필요는 다름."],
"A-D05": [
    "SQLite 파일의 이식성을 설명하며 big/little endian 개념에 링크한다. 엔디언의 배경 설명이다.",
    f"현재 HTTPS 도착 본문은 개념 설명을 제공({src('SQL-U01')}). 2020 revision 936140889 본문 403.",
    "3.31.0·3.35.0·3.37.2·3.41.0·3.47.2의 5판에서 원 href. 공개 목록 51판 중 46판 미열람.",
    "미확인: 중간 46판·2020 본문. 다음은 sqlite-doc-3310100.zip/about.html. 다섯 점을 연속 유지로 읽지 않음.",
    "상류 사건 미관측", "3.47.2(2024-12-07 공표) 관측점까지 동일 href", "엄격 부적격; 5/51 관측, 우측 검열 아님",
    "현재 의미는 맞지만 성긴 배포 관측은 중간 href 변화와 복귀를 배제하지 못한다."],
"A-D06": [
    "application_id를 설명하며 파일의 응용 프로그램 형식을 알아보는 file(1) 도구를 가리킨다. 우선 도구 정체를 알아보는 목적이다.",
    f"현재 HTTPS 공식 file 홈페이지에서 도구 확인({src('SQL-U02')}). HTTP→HTTPS 시행일은 미확인.",
    "A-D05와 같은 5판의 aff_short.html에서 원 href 유지. 46판 내용은 미검사.",
    "미확인: 특정 file 버전의 application_id 인식·실행. 다음은 그 magic 정의를 포함한 공식 file 태그/릴리스. 중간 첫 미검사판도 3.31.1.",
    "상류 시행 미확인", "5개 checkpoint의 실제 배포 HTML", "엄격 부적격; 도구 설명과 특정 버전 실행 성공을 구분",
    "홈페이지가 맞다는 사실은 사용자의 설치된 file 버전이 application_id를 인식한다는 증거가 아니다."],
"A-R01": [
    "mtcars의 HTML 표를 DataTables로 향상시키는 예시다. 문서 말미는 toy example이라 하고 DT를 권한다. 특정 JS 판 고정은 요구하지 않는다.",
    f"현재 공식 DataTables 안내가 목적을 충족({src('R-U01')}); HTTP/www 이전 시행일 미확인. 2024 DataTables 2 공지는 판 차이를 보여 줌({src('R-U07')}).",
    "1.29→1.30(2020-09-22 16:30:03Z) HTTP→HTTPS; 1.46→1.47(2024-05-29) www 제거. 1.49→1.50(2025-03-16)은 다른 simple-datatables 예시로 대체. 26판 전부 확인.",
    "미확인: 상류 redirect 시행일·원 JS 실행. 다음은 당시에 고정된 DataTables 이전 공지/HTTP 보존본.",
    f"소스 committer 2020-09-22 01:53:23Z ({src('R-C01')})",
    f"knitr 1.30 DESCRIPTION Date/Publication 2020-09-22 16:30:03Z + 실제 HTML ({src('R-F023')})",
    "보조 소스→출판 적격 52,600초=14:36:40. A-R02와 같은 소스 사건. 엄격 상류→출판은 부적격.",
    "현재 일반 라이브러리 설명은 유지 가능. 후속 판의 다른 라이브러리는 원 예시 링크의 동등한 정정이 아님."],
"A-R02": [
    "knitr의 Docco 스타일 문서가 유래한 Docco 형식과 모양을 읽는 링크다. 이름이나 버전만으로 실행 재현 요구를 붙이지 않는다.",
    f"현재 Docco 설명으로 redirect({src('R-U02')}). 2017-06-20 CNAME 소스 수정은 실제 배포시각이 아님({src('R-U12')}).",
    "1.29→1.30(2020-09-22 16:30:03Z) jashkenas.github.io → ashkenas.com/docco. 1.46에서 소개 링크가 없어졌으나 스타일 사용 설명은 남음. 26판 확인.",
    "미확인: CNAME 실제 적용·독자 실패. 다음은 당시 Docco HTTP/config 배포 영수증.",
    f"소스 committer 2020-09-22 01:53:23Z ({src('R-C01')})",
    f"knitr 1.30 출판 2020-09-22 16:30:03Z ({src('R-F024')})",
    "보조 적격 52,600초=14:36:40; R01과 독립 사건으로 두 번 세지 않음. 엄격 부적격.",
    "새 주소는 같은 스타일 설명을 제공하므로 정규 주소 병기가 가능하나 원 href와 인용 계보를 지울 필요는 없음."],
"A-R03": [
    "pagebreak 변환이 만드는 page-break-after를 설명한다. 원판 뒤 문단부터 break-after와 구 속성의 호환성 역할을 구분한다.",
    f"현재 MDN 경로는 301→200, Page break aliases 절 존재({src('R-U03')}). 2025-10-30 경로 소스 수정은 시행일이 아님({src('R-U17')}).",
    "rmarkdown 2.1–2.32의 32판 모두 raw href 유지. 2.32 Date/Publication은 2026-09-01 13:10:02Z. 고장 시작은 관측하지 못함.",
    "미확인: MDN redirect 시행일. 다음은 해당 경로의 날짜 고정 배포/HTTP 영수증. 유지 관측을 검열 사건으로 만들지 않음.",
    "MDN 소스 경로 변경 2025-10-30 16:59:53Z; 실제 시행 미확인", "32판에서 같은 raw href; 정정 종점 없음", "엄격 부적격; 소비자 원 호환성 목적 유지",
    "deprecated라는 표시만으로 break-after 문서로 덮어쓰면 실제 생성되는 구 CSS를 설명할 근거가 약해진다."],
"A-R04": [
    "rmarkdown은 Pandoc≥1.12.3을 요구하며 RStudio를 설치하면 별도 Pandoc 설치가 필요 없다고 설명한다. 왜 preview 경로를 골랐는지는 불명이다.",
    f"현재 IDE guide의 #rstudio-ide-oss-downloads span은 실제 존재({src('R-U04')}, {src('R-U14')}). Posit 변경 공지는 2022-07-27({src('R-U08')}).",
    "2.3(2020-06-18)까지 pandoc.html 존재 → 2.4(2020-09-30 18:40:06Z) 부재. 32판 전체 확인; 문서 폐기는 Posit 공지보다 이르며 같은 목적 링크 정정이 아님.",
    "미확인: preview 의도·선택한 현 IDE의 Pandoc payload·rmarkdown 2.1 호환성. 다음은 원 preview 설명 또는 고정 IDE/Pandoc 배포 manifest.",
    f"문서 폐기 소스 2020-09-30 03:10:09Z ({src('R-C03')})", f"2.4 출판 2020-09-30 18:40:06Z, HTML 멤버 부재 ({src('R-F026')})",
    "55,797초=15:29:57은 문서 폐기 산술. 같은 목적 정정 지연에서 제외. 2022 이관과 잇지 않음.",
    "앵커가 살아 있고 다운로드 안내가 있어도 특정 구판 요구를 만족하는 바이너리를 확인한 것은 아니다. 좁은 다운로드 안내라면 유지 가능하지만 추천 전체는 보류."],
"A-R05": [
    "dplyr에서 분리된 데이터베이스 backend를 dbplyr에서 찾으라고 안내한다. 패키지 계보와 저장소 정체를 읽는 목적이다.",
    f"현재 원 GitHub 경로는 tidyverse/dbplyr로 이어짐({src('R-U05')}); owner 이전 실제 시행일은 미확인.",
    "1.0.1(2020-07-31) hadley → 1.0.2(2020-08-18 12:30:02Z) tidyverse. 20판 확인. compatibility.html은 1.1.1에서 폐기; 다른 in-packages 예시는 별도 목적.",
    "미확인: owner 이전·redirect 시행일·개별 API 실행. 다음은 dbplyr의 날짜 있는 이전 기록.",
    f"소스 committer 2020-08-12 14:47:36Z ({src('R-C02')})", f"dplyr 1.0.2 출판 2020-08-18 12:30:02Z ({src('R-F021')})",
    "보조 적격 510,146초=5일 21:42:26. 상류 실제 이전 시계가 없어 엄격 부적격.",
    "주소 소유자 변경은 동일 패키지의 이동이다. 이를 API 호환성 변화나 설치 성공으로 읽으면 안 됨."],
"A-R06": [
    "2013년 뉴욕 출발 항공 자료를 설명하면서 BTS 원 출처를 연결한다. 연도·자료의 출처 확인 목적이며 가공 데이터의 byte 고정 약속은 없다.",
    f"현재 원 URL은 302→200 뒤 BorderCrossing.aspx 본문/JS 안내로 도착, 항공 목적 불충족. 공식 2013 월별 항공 목록은 확인({src('R-U11')}); 변경 시행일 미확인.",
    "0.8.5(2020-03-07)까지 항공 예시 → 1.0.0(2020-05-29 15:00:03Z) Star Wars 예시. 같은 목적 링크 수리가 아님. 소스 수정 뒤 나온 0.8.5도 옛 본문.",
    "미확인: 잘못된 도착의 시작·2013 원파일과 nycflights13 가공 동일성. 다음은 날짜 고정 옛 DB_ID=120 본문; 재현에는 월별 ZIP+생성 스크립트.",
    f"예시 변경 소스 2020-02-22 22:56:02Z ({src('R-C04')})", f"새 예시 1.0.0 출판 2020-05-29 15:00:03Z ({src('R-F012')}); 그 사이 0.8.5는 옛 예시",
    "8,352,241초=96일 16:04:01은 목적 폐기 산술. 엄격 및 같은 목적 소스→출판 정정에서 제외.",
    "같은 기관·HTTP 200이어도 대상이 다른 자료다. 2013 출처 확인 링크로 교체하되 Star Wars나 최신 연도 표로 교체하지 않음."],
"B01": [
    "Rails의 package.json 설명에서 Yarn의 JavaScript 의존성 관리 역할을 읽는다. 설치 성공을 주장하는 링크는 아니다.",
    f"2020-01-24 Yarn 2 공지에서 Classic 분리, 2월1일 예정({src('B-U01')}). 현재 원 경로는 301→200 Classic 설명. 예정일은 시행 영수증 아님.",
    "Rails 6.0.2.1→6.0.3의 공식 versioned web HTML은 이 배경 href를 유지. 별도 Classic 설치 링크 추가는 다른 목적. immutable archive 및 HTML 최초 공개일 미확인.",
    "미확인: 전체 중간판·HTML 출판 시각. 다음은 Rails 6.0.x 날짜 있는 HTML build artifact. 질의3/후보4; JupyterLab 후보의 범위 위반·404 보존.",
    f"공지 2020-01-24, 이관 예정일만 ({src('B-U01')})", "Rails 두 versioned HTML, 해당 본문의 최초 출판일 미확인", "엄격 부적격; 예정일→추정 릴리스일 차이를 계산하지 않음",
    "Classic 설치 링크가 추가돼도 같은 package.json 배경 링크가 정정됐다는 뜻은 아니다."],
"B02": [
    "httr api-packages 도움말은 API rate limit과 기다렸다가 재시도하는 규칙을 API client 작성자에게 연결한다.",
    f"2020-07-02 docs.github.com 공지({src('B-U02')}). 현재 원 URI는 301/301/302→200 REST 개요이며 #rate-limiting 없음. 별도 공식 rate-limit 절에는 대기 규칙 존재({src('B02-old')}, {src('B02-new')}).",
    "httr 1.4.2(2020-07-20) developer.github → 1.4.3(2022-05-04 00:20:02Z) docs.github/v3/#rate-limiting. 1.4.1–1.4.8 전 8판 확인. 1.4.7은 문서 전체를 httr2 추천으로 대체.",
    "미확인: 개별 redirect·anchor 소실의 시작. 다음은 날짜 고정 옛 #rate-limiting 본문. 질의3/후보5; gh는 이미 새 링크여서 정정 아님.",
    f"소스 committer 2022-05-03 20:25:58Z ({src('B02-SOURCE')}); author는 20:23:19Z로 별도", f"1.4.3 CRAN Date/Publication 2022-05-04 00:20:02Z ({src('B02-httr-1.4.3')})",
    "보조 적격 14,044초=03:54:04. 2020 공지→2022 출판을 실제 시행 지연으로 계산하지 않음.",
    "도메인을 새것으로 고친 배포판도 현재는 anchor가 없는 개요에 도착한다. 현재 부적합을 2022년에도 그랬다고 소급하지 않음."],
"B03": [
    "Debian PycURL Quickstart가 libcurl의 curl_easy_setopt 옵션을 Python 상수와 연결한다. 옵션 명칭과 설명을 찾는 목적이다.",
    f"2020-11-04 curl 도메인 공지는 당시 자동 redirect가 아직 아니었다고 설명({src('B-U03')}). 현재 원 API 경로는 301→200 같은 기능 설명({src('B03-old')}).",
    "실제 Debian .deb 7.43.0.2-0.1, 7.43.0.6-5, 7.45.2-3의 quickstart.html 모두 옛 href. PyPI sdist는 HTML0이라 노출 매체로 쓰지 않음.",
    "미확인: .deb 최초 출판·중간판·구 libcurl 옵션별 호환성. 다음은 snapshot.debian.org의 해당 binary 출판 원장. 질의3/후보2.",
    f"도메인 결정 공지 2020-11-04 ({src('B-U03')}); 실제 redirect 시행 미확인", "2019/2021/2023 계열 .deb 관측; mtime/changelog는 출판시계로 쓰지 않음", "엄격 부적격; 성긴 3판을 연속 미정정/우측 검열로 취급하지 않음",
    "옛 href가 계속 배포돼도 같은 API 설명으로 전달된다. 구판 실행이나 특정 옵션 가용성은 별도로 확인해야 함."],
"B04": [
    "여러 sitemap을 하나의 sitemapindex에 묶는 구조와 예시를 읽는 목적. 여기의 원 문자열은 배포 README의 reST 링크이며 과거 HTML href는 미확인이다.",
    f"2020-11-11 Search Central 공지는 도움말 이동 범위를 나눔({src('B-U04')}). 현재 원 경로 shell GET429; 새 canonical sitemap 설명은 읽었음.",
    "2.1.0/2.2.0/2.2.1 source README는 원 URI 유지. tarball HTML0, 과거 HTMLzip404. source 업로드를 HTML 출판으로 간주하지 않음.",
    "미확인: 과거 렌더링 HTML·원 경로 최종 상태·개별 시행일. 다음은 2.2.0 또는 2.2.1의 날짜 있는 HTML artifact. 질의3/후보2.",
    f"공지 2020-11-11 ({src('B-U04')}); 특정 URI 시행 미확인", "PyPI source 업로드 2020-08-06 02:13:55.526488Z / 2022-11-12 03:41:08.913002Z; HTML 날짜 아님", "HTML 기준 평가불가 1/6. 엄격 부적격, 보류 유지",
    "소스 안 링크와 현재 HTML이 있어도 그 사이 독자에게 배포된 HTML을 만들어 냈다고 주장할 수 없음."],
"B05": [
    "A-D04와 같은 PostgreSQL psql CSV/RFC4180 목적. 같은 소비자·기능·상류 이동을 재발견한 중복이다.",
    f"2022-06-17 공지({src('B-U05')}), 2022-09-14 회의록 p6에서 일반 서비스 종료/redirect 완료({src('B05-U-BOARD20220914')}). RFC별 시각 미확인.",
    "A-D04의 실제 12.18→12.19 HTML을 재사용. B의 href 변경 2건에는 포함하되 독립 신규 변경은 아님. 질의3/후보1.",
    "미확인: 특정 URI 시행·동일 목적 독자 실패. 다음은 RFC4180 경로 배포 영수증. 2026-10-29 공지 수정 내용을 2022로 소급하지 않음.",
    "IETF 공지/일반 완료 보고; 개별 URI 시각 미확인", "A-D04와 같은 소스/출판 관측", "엄격 부적격; A와 중복, 독립 지연 또는 소비자 분자에 추가하지 않음",
    "사건부터 찾으면 양성이 다시 보이지만 독립 사례가 늘어난 것은 아니다."],
"B06": [
    "StarlingX Vault Aware 문맥에서 curl로 Vault HTTP API를 호출·인증하는 안내를 읽는다.",
    f"2022-06-21 Developer beta는 Vault/Waypoint 문서의 당일 mirror 안내({src('B-U06')}); 옛 사이트 종료일 아님. 현재 원 URI는 308×3→200 같은 API tutorial.",
    "StarlingX 6.0/7.0의 공식 versioned HTML은 learn.hashicorp 원 href 유지. 전체판·HTML 최초 공개일·immutable archive 미확인.",
    "미확인: Learn redirect 시행·6/7판의 HTML 출판 시각·실행. 다음은 Vault Aware의 날짜 있는 build/출판 영수증. 질의3/후보3.",
    f"beta mirror 공지 2022-06-21 ({src('B-U06')})", "StarlingX 6.0/7.0 본문; 첫 공개시각 미확인", "엄격 부적격; 새 사이트 공개를 옛 URI 고장 시작으로 간주하지 않음",
    "새 사이트가 열렸다고 옛 링크가 틀린 것은 아니다. vaultr의 다른 vaultproject.io 링크는 이 사건에서 제외."],
}

def row_note(c):
    rid = c["reference_id"]
    r = REFS[rid]
    out = [f"# {rid} 근거 경로", "", f"판정: **{c['verdict']}**. 판정 주체는 봉인한 목적을 현재 관측에 적용한 연구 수집자다. 원문/목적 봉인은 [references.jsonl](../../references.jsonl), 전후판은 [editions.csv](../../editions.csv), 시계는 [chains.csv](../../chains.csv), 가림 판독은 [comparisons.csv](../../comparisons.csv)에 있다.", "", "## 원 배포물과 인용 식별", ""]
    fields = [
        ("sample / project / edition", f"{c['sample']} / {c['consumer']} / {c['version']}"),
        ("artifact URL", c.get("artifact_url")), ("artifact SHA256", c.get("artifact_sha256")),
        ("member", c.get("member")), ("member SHA256", c.get("member_sha256")),
        ("raw href", c.get("raw_href")), ("resolved URL", c.get("resolved_url")),
        ("base URL", r.get("base_url", "B 후속 추출; 원 수집 references 참조")),
        ("resolution / literal role", r.get("resolution_rule") or r.get("raw_href_string_role") or "선택 href는 절대 URI; 기준 주소가 결과를 바꾸지 않음"),
        ("anchor", r.get("fragment", "원 수집 기록 참조")), ("link text", c.get("link_text")),
        ("publication value", r.get("publication_date_value") or r.get("publication_utc") or "미확인; 시계 표 참조"),
        ("purpose", c.get("purpose")), ("minimum success", c.get("minimum_success")),
        ("unknown intent", c.get("intent_unknown")), ("A/B duplicate", c.get("duplicate_of_A")),
        ("literal same-purpose href changed", c.get("same_purpose_href_changed")),
    ]
    out += [table(["필드", "값"], [(k, "미확인/해당 없음" if v is None else v) for k,v in fields]), "", "원문 주변 문장·raw anchor는 위 references 행과 collector excerpt에 그대로 보존했다. 아래 설명은 번역/요약이며 추가 원문 열람으로 세지 않는다.", "", N[rid][0], "", "## 현재 관측과 날짜 역할", "", "```json", json.dumps({"current_http": c.get("current_http"), "dates": c.get("dates"), "last_old": c.get("last_old"), "first_observed_new": c.get("first_observed_new"), "other_boundaries": c.get("boundaries")}, ensure_ascii=False, indent=2), "```", "", "## 미확인과 다음 최소 자료", "", "```json", json.dumps(c.get("unknowns"), ensure_ascii=False, indent=2), "```", "", "## 직접 읽은 원문 연결", ""]
    ids = list(dict.fromkeys(r.get("source_ids", []) + c.get("source_ids", [])))
    out += [table(["source ID·주소", "판·발행일 / 관측 UTC", "읽은 위치", "확인한 내용", "한계·최소수"], [(src(sid), f"{SOURCES[sid].get('version')} / {SOURCES[sid].get('publication_date')} / {SOURCES[sid].get('observed_at_utc')}", SOURCES[sid].get('read_location'), SOURCES[sid].get('findings'), f"{SOURCES[sid].get('limits')}; count_minimum={SOURCES[sid].get('count_minimum')}") for sid in ids if sid in SOURCES]), "", "## 반대 설명", "", N[rid][7], "", f"원 수집 case: [{c['collector_case_file']}](../../{c['collector_case_file']})", ""]
    return "\n".join(out)

rows1, rows2, rows3 = [], [], []
for c in CASES:
    rid=c["reference_id"]; r=REFS[rid]; n=N[rid]; comp=COMPS[rid]
    ident=link(rid, f"evidence/rows/{rid}.md") + f" · {c['sample']}" + (" (A-D04 중복)" if rid=="B05" else "")
    origin=f"{c['consumer']} {c['version']}; {link('원 배포/본문',c['artifact_url'])}; member `{c['member']}`; raw href {link(c['raw_href'], c['raw_href'])}. resolved는 원 문자열과 같음."
    if rid=="B04": origin += " **과거 HTML 아닌 source README 후보**."
    consumer=n[2]
    if c.get("last_old") or c.get("first_observed_new"): consumer += " 배포물: " + boundary(c)
    rows1.append([ident, origin, n[0]+f" 원문 위치·hash·최소 성공: [{rid}](evidence/rows/{rid}.md).", n[1], consumer, c["verdict"]+" — 봉인 목적의 현재 재사용 판단", n[3]])
    rows2.append([ident+" / "+str(c.get("event_key") or "변경 사건 미확인"),n[4],n[5],"시계별 값·역할은 행 근거의 dates. source/merge/build/publication/reader를 별도 보존; null은 미확인.",n[6],n[3]])
    rows3.append([ident+" / "+c["purpose"],comp["L1_decision"]+" — "+comp["L1_rationale"],comp["L2_decision"]+" — "+comp["L2_rationale"],comp["L3_decision"]+" / 대조 분류 "+comp["L3_comparison"],n[7],f"추가 외부 원문 열람 L1/L2/L3=0/0/0; L3 source cards={comp['L3_source_cards']}. merge/build/reader_report 빈 역할={comp['missing_clock_count']}/3 (모든 날짜의 결측 총수는 아님). "+("사전 노출 표시. " if comp['possible_prior_exposure']=='True' else "")+comp["L3_remaining_unknown"]])

report=["# AF-RES-032 · 독자가 받은 도움말의 링크는 어느 배포판에서 실제로 바뀌었는가", "", table(["참조 ID·A/B", "원 배포판·멤버·href·URL", "주변 문장·클릭 목적", "상류 전후 근거 URL·시점", "소비자 배포 전후 URL·시점", "유지/교체/보류", "미확인"],rows1), "", "## 2. 날짜쌍과 단절", "", table(["사건·참조", "시작 관측·근거", "끝 관측·근거", "시각 역할·정밀도", "계산 적격·구간", "끊긴 고리·필요 자료"],rows2), "", "## 3. 재확인 보기 및 비용", "", table(["사례·목적", "URL만의 판정", "용도·판 추가 판정", "배포 이력 추가 판정", "원문 대조·반례", "재열람 수·미확인"],rows3), ""]

report.append("""## 고정 결과와 분모

상태는 **REVIEW_READY_WITH_GAPS**다. A 출발 표본·고유 원문 최소수는 충족했다. 배포 링크 수정은 관측했지만, 상류의 실제 시행부터 같은 목적의 소비자 HTML 출판까지 연결되는 엄격한 지연은 계산할 수 없다. 별도 내부 판독과 통합 검산을 했으며 외부 사람 검토는 아니다.

| 측정량 | 결과와 단위 | 판정 주체·제한 |
| --- | --- | --- |
| A 출발 | 12참조 / 서로 다른 배포 HTML 12문서 / 6프로젝트; D6, R6; 프로젝트당 2 | 원 배포물 hash·멤버·href·목적을 먼저 봉인 |
| A 실제 후속 관측 | archive 123개, 문서 상태 246회 = HTML 존재·열람 211회 + 멤버 부재 35회 | 246개를 모두 읽은 HTML이나 독립 원고로 세지 않음 |
| 같은 목적의 href 수정 | A 5/12참조, 독립 소스 수정 사건 4개 | knitr의 두 문서가 같은 commit. 최초 수정 경계 기준; R01의 후속 www 정리까지 포함한 모든 edit 횟수는 아님 |
| 현재 추천 재사용 | A 유지9 / 교체2 / 보류1; B 유지4 / 교체1 / 보류1 | 봉인한 최소 목적에 대한 수집자 판정. 실제 이용자 성공률이 아님 |
| B 사건 우선 탐색 | 6시도, 질의18, 후보 문서 계열17 | 각 사건 질의≤3, 후보≤5; 성공한 소비자로 사건을 다시 고르지 않음 |
| B 노출 매체 | HTML 관측5/6: 실제 archive3, versioned web만2; 과거 HTML 미확인1 | B05는 A-D04 중복. 추가 독립 HTML 소비자·목적 사례4개 |
| B 실제 같은 목적 href 수정 | 중복 포함2/6시도; A 중복 제외 신규1/5시도 | B02만 신규. B04도 미확인 시도로 분모에 남김 |
| 엄격 지연을 찾은 비율 | A 0/12, B 0/6 | 조건부 계산 적격 분모는 **0, 해당 없음**. 평균0일이나 전파율0%로 해석하지 않음 |
| 우측 검열 / 같은 매체 독자 실패 사슬 | 0 / 0 | 시작을 모르는 사건을 검열로 만들지 않음. live web의 별도 독자 보고1건은 있음 |
| 보조 소스→출판 | A 3참조쌍 / 독립2사건; B 1쌍 / 1사건 | 상류 시행 지연과 구분. 정확한 committer/CRAN 출판 시각의 차이 |
| 직접 읽은 고유 원문 최소 산입 | **75** / source 레코드395 | 동일 URL·archive·원고·사건·행은 서로 다른 계수 단위 |
| 필수 원문 범주 | A12/요구12, 상류34/요구8, 후속8/요구6, 타 분야8/요구4 | 후속8은 변경 HTML6(다른 목적 예시1 포함)+독립 공식 공표 자료2. 기타1+B 소비자5+B 보조7은 추가 산입 |
| 독립 사례 | A12 + 추가 B HTML4 = 16개 소비자·목적 사례; 타 분야2쌍은 별도 | 18시도에서 B 중복1과 과거 HTML 미확인1을 구분. 사건별 출처 수는 event-source-counts.csv |

집계의 직접 입력은 [counts.json](evidence/counts.json), [source-deduplication.json](evidence/source-deduplication.json), [event-source-counts.csv](evidence/event-source-counts.csv), [sources.jsonl](sources.jsonl)이다. source의 `duplicate_group`은 같은 멤버 바이트/같은 원고 주소를 뜻한다. `minimum_counting_group`은 보다 보수적으로 최소수를 세기 위한 묶음이며, 다른 의미 상태나 문서 부재까지 들어갈 수 있으므로 “본문이 같다”는 주장이 아니다. 같은 archive URL의 서로 다른 HTML 멤버는 문서별 hash로 나눴다. 검색 요약·접근 실패·같은 원고의 미러는 최소수에서 제외했다.

## Q1–Q2. 무엇을 배포판으로 보았고, 언제 목적을 고정했는가

실제 시작 SHA는 `172c6bc37bdf91b91c86b9b3be29cb5b44fa4971`, 의존 AF-RES-027은 `42dadeeb632301108e1fc83ba393db971ec28b15`다. 이전 작업의 패키지 18행을 A 출발표본에 재사용하지 않고 원 배포 HTML의 본문 링크에서 시작했다. 사라진 CI는 재조사하지 않았다. B01에서 제외 후보 JupyterLab을 조회한 편차는 별도 기록했다. 조사 개시는 2026-11-22 07:05 UTC다. 원문 원장의 확인창은07:11:58.976247–07:40:36.378887Z이며, 별도 archive 재독은07:50:37.814656Z, root fresh GET 재검은07:58:20.761822Z까지다. 그 뒤는 분석·검산·원격 고정 단계이며 [research-window.json](evidence/research-window.json)에 구분했다. 역사 출발창은 2020–2024였고 모든 최종 A 원판은 2020년이며 관측일까지 12개월 이상의 후속창을 갖는다. 날짜가 지난 것이 연속 관측을 뜻하지는 않는다.

두 유통 경로를 분리했다. D는 Python의 HTML tarball, PostgreSQL의 공식 source archive에 이미 포함된 빌드 HTML, SQLite의 HTML ZIP이다. source tarball이라는 이름만으로 HTML이 있다고 가정하지 않았으며 실제 member를 열었다. R은 CRAN package tarball의 `inst/doc/*.html`이다. R의 DESCRIPTION Date/Publication과 파일 mtime을 구분했고, D의 소프트웨어 릴리스 날짜를 해당 HTML tarball의 최초 HTTP 공개 UTC로 승격하지 않았다. 공식 시작 원장은 [Python 문서 archive](https://docs.python.org/ftp/python/doc/), [PostgreSQL 12.2 archive](https://ftp.postgresql.org/pub/source/v12.2/), [SQLite chronology](https://www.sqlite.org/chronology.html), [CRAN Archive](https://cran.r-project.org/src/contrib/Archive/)다.

선택은 공개 모집단의 무작위 표본이 아니다. D의 사전 지정 발행자별 첫 접근 가능한 2020판, R의 후보10프로젝트 첫 2020 archive를 조사했다. 최초 R 초안은 프로젝트 우선으로 적어 사용자 날짜 우선 요구를 잘못 옮겼다. 목적지나 후속판을 열기 전에 날짜순으로 고쳐 knitr/rmarkdown/dplyr를 선택했고 잠정 DBI/curl/data.table 문서6개는 제외 원장에 남겼다. 이 정정은 [preseal-order-correction.md](evidence/preseal-order-correction.md)에 있다. 선택 후의 실패나 양성을 보고 A를 바꾼 일은 없다.

[frame.csv](frame.csv)는 선택12, 외부 URL 없는 문서27, 같은 문서의 추가 링크 제외11, 표본6문서 충족 뒤 도달하지 않은 R 후보7을 구분한다. nav/footer 제외는 수집별 일부 계수만 있어 전체 탐색 문서의 완전한 유형별 제외 총수는 **미확인**이다. 현재 웹만 있는 문서, URL 없는 패키지명, 가상 URL, navigation/footer는 A 출발표본에 넣지 않았다. “도달하지 않음”은 접근 실패가 아니다.

A12의 원 archive/member hash, raw href, 기준 URL, anchor, 링크 텍스트, 주변 문장, 목적, 최소 성공, 불명 의도는 `168d90b8519bcb4f673acc659bbaae895f79fca5`에 봉인하고 07:18:08Z 원격 재독했다. 그 뒤에만 대상 URL과 후속 판을 열었다. 현재 references의 A prefix SHA256은 `b3c2f68b905102f0fa682ab45a34c0f3401a69b61ba0a59327045e04a626d562`로 그대로다. B6은 별도 사건 봉인 뒤 추가한 행이다. A에서 선택한 href는 모두 절대 URI여서 기준 주소에 따라 해소 결과가 달라지는 실례는 없다. 해소 규칙과 base를 저장했지만 상대 링크의 효용을 실증했다고 주장하지 않는다.

## Q3–Q4. 주소 변경과 소비자 배포 변경은 다른 관측이다

가장 분명한 실제 배포 경계는 다음과 같다. 이 “최초”는 열거한 같은 계열의 보존판 안에서만 성립한다. 다른 major, 삭제된 판, website의 최초 순간까지 확장하지 않는다.

| 참조 | 마지막 옛 판 → 최초 관측 새 판 | 읽은 완전 계열 / 사이 누락 | 바뀐 것 |
| --- | --- | --- | --- |
| A-D02 | Python 3.8.14 → **3.8.15** | 3.8.2–3.8.20, 19판 / 0 | 열린 문서 오류의 Roundup query → GitHub docs query |
| A-D04 | PostgreSQL 12.18 → **12.19** | 12.2–12.22, 21판 / 0 | 같은 CSV 문단의 RFC4180 tools → datatracker href |
| A-R01 | knitr 1.29 → **1.30** | 1.27부터 보존된 26판 / 0 | DataTables HTTP → HTTPS |
| A-R02 | knitr 1.29 → **1.30** | 같은 26판 / 0 | Docco의 host 경로 변경 |
| A-R05 | dplyr 1.0.1 → **1.0.2** | 0.8.4부터 보존된 20판 / 0 | dbplyr 저장소 owner 경로 변경 |
| B02 | httr 1.4.2 → **1.4.3** | 1.4.1–1.4.8, 8판 / 0 | 같은 rate-limit 문장의 developer → docs 호스트 |

이 표의 바이트·href·출판 정보는 [editions.csv](editions.csv)와 첫 필수 표의 전후 archive 링크 및 행별 근거에 연결된다. R은 26+32+20=78 archive, Python19, PostgreSQL21, SQLite5로 A의 실제 archive는123개다. SQLite는 51판을 열거했으나 5판만 읽었다. 나머지46개는 존재하지 않는 판도, 정상 유지가 확인된 판도 아니다. SQLite에 연속 유지나 “최초 수정 없음” 결론을 붙이지 않았다.

링크의 현재 상태는 HTTP code, 최종 URL, fragment 존재, 필요한 절, 목적 충족의 다섯 필드로 나눠야 했다. A-R06은 같은 BTS 도메인의 200 응답이지만 다른 대상인 국경 통과 자료로 도착한다. B02는 새 문서 도메인으로 들어가도 필요한 rate-limiting anchor가 없고 REST 개요에 머문다. 반대로 A-D04는 최종 URL 모양이 RFC Editor info 경로여도 실제 본문에 필요한 CSV 절이 들어 있다. A-R04에서는 redirect가 추가한 도착 anchor도 실제로 살아 있다. 원 raw href에는 fragment가 없었다. URL 패턴만 보고 이 두 행을 “fragment 소실”로 분류했다면 틀렸을 것이다. 근거는 각 행의 `current_http`와 [BTS 2013 월별 안내](https://www.bts.gov/browse-statistical-products-and-data/bts-publications/airline-service-quality-performance-234-time), [GitHub rate limit 본문](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api), [RFC4180](https://www.rfc-editor.org/info/rfc4180/), [Posit IDE guide](https://docs.posit.co/ide/user/?ref=rstudio-legacy#rstudio-ide-oss-downloads)다.

문서 제거도 정정과 구별했다. rmarkdown pandoc.html은2.4에서 없어졌고, dplyr의 항공 예시는1.0.0에서 Star Wars로 바뀌었다. 후자는 2020-02-22 소스 수정 이후 출판된0.8.5가 여전히 옛 예시를 포함한다. 따라서 “소스 commit 다음 릴리스에 배포됐을 것”이라는 추정은 이 표본 안에서 반증된다. httr1.4.7의 긴 vignette 폐기와 knitr1.50의 다른 JS 라이브러리 추천도 같은 목적 정정의 분자에 넣지 않았다. 실제 전후 멤버는 A-R04/R06/B02 행에 연결된다.

## Q5. 사건부터 찾은 B가 추가한 것과 실패

B는 2020–2024 공식 이관 공지 탐색에서 직접 읽은 사건을 날짜순으로 고정했다. Yarn(2020-01-24), GitHub(07-02), curl(11-04), Google(11-11), IETF(2022-06-17), HashiCorp(06-21)의6개다. 공개 사건 전체를 망라한 대표 표본은 아니다. `ffbce62e4c01459ebbfb006a5d6c67e425ed7c17`의 [B 봉인](collectors/b/b-sealed.jsonl) 뒤 소비자 질의에 들어갔다. 사건별3질의, 후보4/5/2/2/1/3개를 기록했다.

새로운 같은 목적의 실제 href 수정은 httr B02에서1건 찾았다. B05는 A-D04의 PostgreSQL을 다시 찾았으므로 A와 합산하지 않았다. Rails의 배경 링크는 그대로였고 별도 설치 링크가 추가됐다. gh의 실제 vignette는 원래부터 새 PAT URI였다. vaultr는 다른 vaultproject.io 계열이라 봉인한 Learn 사건의 소비자로 쓰지 않았다. PycURL의 PyPI source에는 HTML이 없어 Debian의 실제 문서 binary로 확인했으며, Sphinx Sitemap은 source README와 현재 HTML만 확인했으므로 과거 출판 HTML은 **미확인**으로 남겼다. 각 실패와 제외는 [B root review](collectors/b/ROOT_REVIEW.md), [cross B review](collectors/cross/b/REVIEW.md), [B05 review](collectors/offline/b05/README.md)와 attempts 원장에 있다.

B01 탐색 중 명시적으로 제외된 JupyterLab의 과거 HTMLzip을 세 번 요청한 절차 오류가 있다. 모두404이고 직접 원문·최소수·수정 분자는0이다. 후보1개와 GET3회는 실제 비용에 남겼다. 이를 없었던 일로 지우지 않았고 [scope-deviations.md](evidence/scope-deviations.md) 및 수용조건에 false로 기록했다. 제외한 소비자를 재추적해 양성을 늘리는 작업은 계속하지 않았다.

## Q6. 계산할 수 있는 두 시계와 끊긴 두 시계

소스 committer와 같은 archive의 CRAN Date/Publication은 짝지을 수 있었다. knitr 두 문서는 각각14시간36분40초, dplyr 저장소 경로는5일21시간42분26초, httr는3시간54분04초다. 앞의 두 knitr 행은 같은 소스 사건이므로 A의3참조쌍은 독립2사건이다. 이 숫자는 소스 수정에서 CRAN 출판까지의 간격이다. merge와 HTML build의 별도 영수증은 없으며 committer나 `Packaged` 시각을 그 역할로 대체하지 않았다. [intervals.csv](intervals.csv)의 보조7행은 적격4행, 문서/목적 폐기2행, Python 명목 상태 보고 차이1행을 구분한다.

Python의 공식 read-only 상태 보고가 표시한2022-04-08 18:15와 소스 committer2022-09-11 18:50:47의 명목 차이는156일00:35:47이다. 보고의 분 정밀도는 실제 서버 시행이 그60초 안에 있었다는 관측이 아니다. 그래서 하한/상한을 null로 두고 실제 시행 지연에서는 제외했다. Python3.8.15와 PostgreSQL12.19의 공식 판 공표일은 확인되지만 특정 HTML archive가 최초로 공개된 UTC 영수증은 없다. source tarball 안의 실제 새 HTML은 “그 판의 내용”을 증명하고, 공표일은 다른 시계다.

실제 독자가 문서 오류 추적기의 잠금을 겪었다는 [2022-04-10 당사자 글](https://discuss.python.org/t/status-of-documentation-bug-tracker/14957)은 읽었다. 그러나 그 글이 명명한 것은 live `/3/bugs.html#using-the-tracker`이며 A의 offline3.8.2 또는 봉인한 docs-query를 클릭했다고 말하지 않는다. 이 사슬에 합치지 않았다. 후대 자동 preview의3.12.1 표기도2022년의 판으로 소급하지 않았다. 출판된 도움말의 접근 가능성과 실제 클릭/실패는 다른 관측이다.

따라서 엄격한 상류 실제 시행→소비자 같은 목적 HTML 출판 쌍은 A0/12, B0/6이며 계산 조건부 분모0은 해당 없음이다. 양성0은 조사 종료를 막는 조건이 아니다. 이 자료로 보관 추천의 만료 기간을 “몇 일”로 정하거나 평균 정정 지연을 추정할 수 없다. 사건을 관측창 끝까지 따라갔다는 근거가 부족한 시작 미상 행은 우측 검열로 만들지 않았다.

## Q7. 정정이 오히려 목적을 손상시키는 경우

서로 다른 행위자의 올바른 목적지를 분리하면 모순이 줄어든다.

| 관점 | 이번 자료에서 관측한 요구 | 적절한 처리 |
| --- | --- | --- |
| 도움말 편집자 | PostgreSQL은 redirect 왕복을 줄이는 href 정리, dplyr는 예시 교체 | 전자는 같은 링크 수정, 후자는 추천 목적 폐기로 기록 |
| 링크 대상 발행자 | IETF/MDN은 경로 정리와 설명 유지, GitHub는 문서 통합 | 일반 공지와 특정 URI의 시행·fragment 상태를 분리 |
| 특정 판을 재현하려는 독자 | 구 CSS 생성 결과, 2013 데이터 출처, 역사 카탈로그의 논증 | 원판·원문 목적 보존; 새 정보는 병기. 실제 재현 요구가 없는 문서는 임의로 역사판 요구로 만들지 않음 |
| 오늘 같은 일을 하는 설계자 | 현재 열린 오류 목록, 현재 rate-limit 동작, 조건에 맞는 다운로드 | 목적에 필요한 현재 절/판을 재확인. URL200만으로 승인하지 않음 |

공공 통계 반례는 “같은2021년”이라는 표기가 충분하지 않음을 보인다. [ONS Blue Book2022](https://www.ons.gov.uk/economy/grossdomesticproductgdp/compendium/unitedkingdomnationalaccountsthebluebook/2022/nationalaccountsataglance)의2021년 실질 GDP 증가율은7.5%, [2023년6월 QNA](https://www.ons.gov.uk/economy/grossdomesticproductgdp/bulletins/quarterlynationalaccounts/januarytomarch2023)는7.6%, [2023년9월 개정 공표](https://www.ons.gov.uk/economy/grossdomesticproductgdp/articles/impactofbluebook2023changesongrossdomesticproduct/2023-09-01)는8.7%다. 그 공표의1.1%p 개정은7.6을 기준으로 한다. 2022 연차판의7.5와 빼면1.2%p로 다른 비교가 된다. [Bank of England2023년11월 보고서 Box C](https://www.bankofengland.co.uk/monetary-policy-report/2023/november-2023)의 실제 링크·논증은 당시 통계의 개정 전후를 비교한다. 역사적 논증의 인용을 가장 최근 값으로 덮어쓰면 그 비교가 무너진다. 이 관측을2026년 최신 GDP 값이라고 주장하지 않는다.

박물관 반례는 [MoMA1936년 전시 카탈로그](https://www.moma.org/documents/moma_catalogue_2748_300086869.pdf)의 figure114/작품152로서 현재 Airplane Flying으로 식별되는 작품을1914로 표기한 것과 [현재 작품79269](https://www.moma.org/collection/works/79269)의1915(뒷면1914 기재)를 나란히 둔다. [Lowry2012 글](https://www.moma.org/momaorg/shared/pdfs/docs/archives/InventingAbstraction_GLowry_359_363.pdf)은1936년 카탈로그 표지 도식이 만든 미술사의 틀을 명시적으로 인용한다. 그러므로 과거 도식의 역할을 논하는 인용은 현재 개체 기록으로 대체하면 목적을 잃는다. 다만 Lowry가 작품152의 연대 변경을 인용했다고 읽지는 않는다. 이것은 역사 카탈로그와 현재 개체 기록의 역할 비교이며 같은 작품 연대 정정의 엄격한 전파 사슬이 아니다. 기록관의1937 corrected dummy도 그 자체로 실제 공개 교정판 출판을 입증하지 않는다.

이 두 분야는 [cross REVIEW](collectors/cross/REVIEW.md)의2쌍, 최소 원문8개로 보존했다. 소프트웨어 수정 분자·지연 분모에는 합치지 않는다. 유지의 강한 원사례는 A-R03의 호환성 CSS와 역사 논증의 카탈로그이며, 교체의 강한 원사례는 A-D02의 현재 오류 목록과 A-R06의 잘못된 자료 도착이다. A-R04/B04는 유지·교체 양쪽 모두를 끝까지 확정하지 못한 사례다.

## Q8. 어떤 필드가 판단을 바꾸었으며, 무엇은 검증하지 못했는가

| 표본·보기 | 원문 대조에 맞는 행동 / 분모 | 오교체 | 잘못 유지 | 보류 | 해석 |
| --- | --- | --- | --- | --- | --- |
| A URL만 | 0/12 | 0 | 0 | 12 | 목적/현재 내용이 없어 12행 모두 보류 |
| A 용도·판 추가 | 0/12 | 0 | 0 | 12 | 목적은 구체화됐지만 현재 전달 증거 없음 |
| A 현재 관측·배포 이력 추가 | 11/12 | 0 | 0 | 1 | 유지9+교체2; A-D04 사전 노출 제외 시10/11, 보류1 |
| B URL만 | 0/6 | 0 | 0 | 6 | B04 과거 HTML 평가불가1, B05 A중복1을 포함한 시도 분모 |
| B 용도·판 추가 | 0/6 | 0 | 0 | 6 | 같은 분모 유지 |
| B 현재 관측·배포 이력 추가 | 5/6 | 0 | 0 | 1 | 유지4+교체1; B03 사전 배경 노출 제외 시4/5, 보류1 |

표의 “맞는 행동”은 원문을 읽은 수집자의 기준판정과 내부 판독의 일치다. 보류는 기준판정도 보류인 경우에도 정답으로 올리지 않았다. A-D04는 L1/L2 뒤 B05 공지 요약을 보았고, B03 판독자는 잠정 curl 표본의 배경을 알고 있었다. 두 행의 노출을 표시했다. B에서 중복과 과거 HTML 미확인을 제외한 독립 평가 가능 소비자는4개다. 실제 이용자 정확도, 교체 오류의 모집단 비율, 완전한 무정보 맹검으로 해석하지 않는다.

특히 L3는 배포 이력과 함께 현재 응답·내용을 처음 제공했고, 카드에 수집자의 요약과 일부 해석도 들어 있다. L1/2의 보류가 L3에서 해소됐다고 해서 이력 필드만의 효과라고 할 수 없다. A-D01/D03/D05/R01/R02처럼 배경 읽기 목적은 현재 본문과 목적만으로 유지 판단이 가능했을 것이라는 설명은 **사후 추론**이다. 실제 L1/2에서 옳게 유지한 수가 아니다. A-R04/B04는 이력을 더해도 결론이 남는다. 원 URL만 보고 보류했던 것은 적절한 불확실성 처리지만 정답률로 부풀리지 않았다.

비용은 실제 셀 수 있는 단위로 기록했다. 추가 외부 페이지 재열람은 판독 L1/L2/L3 모두0이며, A L3 source card50개/고유ID46개/입력97,612바이트, B L3 card23개/입력40,535바이트다. 카드를 새로 연 웹페이지로 세지 않는다. 수집 비용은 A archive123·HTML211·부재35, B 질의18·후보17, source 레코드395로 별도다. comparisons의 빈 날짜는 merge/build/reader_report 세 역할 중 빈 칸으로 한정하며 상류 시행 등 모든 시계의 결측 총수는 아니다. 사람 소요시간이나 유료 비용은 추정하지 않았다. [comparison-protocol-note.md](evidence/comparison-protocol-note.md), 각 L1/L2/L3 입력·decision·receipt가 판단 순서를 보존한다.

제품에 권하는 저장 단위는 `URL`보다 “이 배포판의 이 문장이 왜 그 자료를 연결했는가”다. 이는 관측에서 도출한 설계 제안이며 구현 또는 성능 검증 결과는 아니다.

| 필드 묶음 | 최소 필드 | 필요한 이유·반례 |
| --- | --- | --- |
| 원 인용 | raw href, raw anchor, resolved URL, base URL·해소 규칙, link text, 앞뒤 문장 | query/fragment를 정규화 중 지우면 Python/httr의 목적이 바뀜 |
| 클릭 목적 | 목적 유형, 최소 성공조건, 대상·연도·판, 의도 미확인 | BTS2013과 최신 자료, 구 CSS와 새 속성, 역사 카탈로그를 구분 |
| 노출 매체 | 발행자, 배포 ID·판, archive SHA256, member 경로·SHA256 | source diff와 실제 받은 HTML, README와 built HTML을 구분 |
| 시간·이력 | upstream/source/merge/build/publication/reader/observed_at의 각각 값·역할·정밀도·근거 | commit/mtime/공지/현재200을 같은 사건 시각으로 만들지 않음 |
| 현재 확인 | 상태열, 최종 URL, fragment 존재, 필요한 절·대상·버전, 관측 UTC | 같은 도메인200의 오도착과 살아 있는 legacy anchor 구별 |
| 판단과 재개 | 유지/교체/보류, 판정 주체, 대안, 마지막 확인 위치, 답을 바꿀 다음 자료 | 근거 부족 상태를 보존하고 다음 확인 비용을 줄임 |

원판 재현·역사 인용에는 원 URL과 판을 남기고 정정/현행 기록을 병기한다. 현재 업무를 위한 추천은 현재 절과 필요한 판·조건을 다시 확인한다. 새 정보가 원래 대상의 정정인지, 내용 이동인지, 다른 추천인지 구분한다. 이 조사로 일률적인 만료일이나 자동 교체 정책의 정확도를 정할 수는 없다. 실제 시행일과 출판·사용 시계가 확보되면 그때 해당 목적별 재확인 간격을 다시 평가해야 한다.

## 검산·수용과 인계 범위

원문을 재열람한 동일 작업자의 검사와 별도 내부 판독을 나눴다. CRAN 경계검산18/18, root fresh GET4/4, 별도 내부 Python/httr archive27개·HTML46개·DESCRIPTION8개 재독에서 바이트/경계/산술 결함0이었다. 통합 감사27/27은 A봉인, source395ID와 조인, 최소수75, archive/member 계수, 질의 상한, 보조7행 산술을 확인했다. 그 감사자는 R 수집에도 참여했으므로 완전히 독립적인 원문 검토는 아니다. 세 시각 역할 보강, duplicate 그룹 의미 분리, source join 복구, B 최소 성공·출판 clock 보강은 정정 원장에 남겼다.

실행한 검사의 대상 HEAD·입력 hash·exit code는 각 [collector audit](collectors/offline/AUDIT_ROOT.md), [integration audit](collectors/cran/INTEGRATION_AUDIT.md), [primary-reread](evidence/primary-reread.json), [공통 gate 영수증](evidence/checks/common-retry-execution.json)과 [pre-result 세션 검사](evidence/checks/session-pre-result-execution.json)에 있다. 공통 gate의 대상은6ac3d4d 고정 commit이며 공식 원격 freshclone에서5/5 exit0이었다. 첫 localclone의 누락Gitobject에 따른 backup 실패도 보존했다. 후기 결과 문서의 내용·구조 검산은 [deliverable-check.json](evidence/deliverable-check.json)의 별도 입력hash를 따른다. 원격 파일 재독은 셸 실행 검사와 별도로 보고한다. 최종 [SELF_CHECK.md](SELF_CHECK.md)는 Q1–Q8 반증 경로를, [acceptance-evidence.json](evidence/acceptance-evidence.json)은 충족/거짓 조건과 재개 자료를 갖는다. common index와 dot-control은 변경하지 않는다. 결과·수용 파일의 고정 원격 SHA를 재독한 뒤 HANDOFF를 별도 마지막 commit으로 쓴다.

## 가장 중요한 불일치 또는 약점

| 가장 중요한 불일치 또는 약점 | 근거 URL | 영향을 받는 판단 | 다음 조사 제안·첫 자료 |
| --- | --- | --- | --- |
| 실제 상류 시행·특정 HTML 최초 출판·같은 offline 독자의 연결이 빠짐. 확인한 릴리스 경계와 엄격한 시간 지연은 다름 | [Python3.8.15 archive](https://docs.python.org/ftp/python/doc/3.8.15/python-3.8.15-docs-html.tar.bz2), [공식 상태 보고](https://discuss.python.org/t/github-issues-migration-status-update/14573), [독자 원문](https://discuss.python.org/t/status-of-documentation-bug-tracker/14957) | A0/12·B0/6 엄격 쌍; 보관 추천 TTL·평균 전파 지연·피해율 추정 불가 | 첫 자료는 이 HTML tarball hash를 명명한 공식 최초 출판 영수증. 이후 동일 query/매체의 독자 보고와 실제 잠금 시행 기록을 연결 |
| 배포 범위·절차에 남은 틈: SQLite46판 미열람, B04 과거 HTML 부재, B01의 제외 후보 접근, 일부 제외 유형 총수 미완성 | [SQLite chronology](https://www.sqlite.org/chronology.html), [Sphinx Sitemap2.2.0](https://pypi.org/project/sphinx-sitemap/2.2.0/), [편차 원장](evidence/scope-deviations.md) | 연속 유지·모집단 전파율·완전한 범위 준수는 주장 불가; REVIEW_READY_WITH_GAPS | 첫 미열람 배포물은 [sqlite-doc-3310100.zip](https://www.sqlite.org/2020/sqlite-doc-3310100.zip)의 about.html/aff_short.html. B04는 날짜 고정2.2.0 HTML artifact부터 |
| 세 보기 판독에서 현재 상태와 이력이 함께 추가되고 카드 해석·사전 노출이 있음. 박물관의 역할 비교도 같은 작품 정정 사슬은 아님 | [보기 입력·한계](evidence/comparison-protocol-note.md), [B02 실제 archive](https://cran.r-project.org/src/contrib/Archive/httr/httr_1.4.3.tar.gz), [Lowry 원문](https://www.moma.org/momaorg/shared/pdfs/docs/archives/InventingAbstraction_GLowry_359_363.pdf) | 이력만의 효과·실사용자 정확도·박물관 정정 전파율 추정 불가 | 같은 현재 증거를 고정한 current-only/전체이력 카드로 새 비노출 판독부터. 역사 카탈로그 연대 사슬에는 작품152를 명시적으로 인용한 정정/후속 출판 본문이 먼저 필요 |
""")

(P / "evidence/rows").mkdir(exist_ok=True)
for c in CASES:
    (P / "evidence/rows" / (c["reference_id"] + ".md")).write_text(row_note(c), encoding="utf-8")
(P / "RESULT.md").write_text("\n".join(report), encoding="utf-8")
print(json.dumps({"rows":len(CASES), "result_bytes":(P/"RESULT.md").stat().st_size, "row_notes":len(CASES)}, ensure_ascii=False))
