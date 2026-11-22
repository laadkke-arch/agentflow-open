"""Assemble source-research records only. This script does not conduct card readings."""
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).parent
RAW = BASE / "raw-web"
NOW = datetime.now(timezone.utc).isoformat()


def raw(name):
    return json.loads((RAW / name).read_text())


def dump(name, value):
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


sources = []


def source(sid, url, publisher, locator, fact, limitation, *, version="미확인", date="미확인", kind="auxiliary", cases=(), counted=False, group=None, refs=(), metadata=None, direct=True, mode="observed_body", outcome="opened", independent=False):
    record = {
        "source_id": sid,
        "original_url": url,
        "pinned_url_or_version": version,
        "publisher": publisher,
        "event_or_publication_date": date,
        "checked_utc": NOW,
        "checked_utc_basis": "ledger_written_after_direct_tool_read; exact fetch time in metadata when available",
        "locator": locator,
        "source_kind": kind,
        "verified_fact": fact,
        "limitation": limitation,
        "question_ids": ["Q1", "Q2", "Q3", "Q6", "Q7"],
        "case_ids": list(cases),
        "duplicate_group": group or sid,
        "counted": counted,
        "count_group": kind if counted else "not_counted",
        "tool_refs": list(refs),
        "claim_mode": mode,
        "access_outcome": outcome,
        "direct_body_read": direct,
        "separate_publisher_edition": independent,
        "scope": "source research/key preparation; not actual card/task reading",
    }
    if metadata:
        m = raw(metadata)
        record["raw_evidence_file"] = "collection/natural/raw-web/" + metadata
        if m.get("checked_utc"):
            record["checked_utc"] = m["checked_utc"]
            record["checked_utc_basis"] = "recorded by direct fetch"
    sources.append(record)


# Exposure ledgers and the four observed consumers.
source("NAT-FRAME-P", "https://pandas.pydata.org/pandas-docs/version/1.5.3/user_guide/index.html", "pandas", "Guides body TOC; HTML lines 568 onward, first 25 distinct document hrefs", "본문 Guides 목차에서 10min, dsintro 순서로 시작하는 고유 문서 25개를 노출 원장으로 고정했다.", "노출 목록은 적격 여부를 모두 읽었다는 뜻이 아니다. 두 적격 문서 뒤의 23개는 미검토이다.", version="pandas 1.5.3", kind="sampling_frame", metadata="np-index.frame-links.json", direct=True)
source("NAT-FRAME-S", "https://www.statsmodels.org/v0.14.0/examples/index.html", "statsmodels", "Examples body TOC; HTML lines 3166 onward, first 25 distinct document hrefs", "본문 예제 목차에서 OLS, GLS, Quantile, Recursive, Rolling 순서로 시작하는 고유 문서 25개를 기록했다.", "10번째 문서에서 두 번째 적격이 확보되었다. 11·12는 병렬 요청으로 링크만 추가 스캔했고 선정에는 쓰지 않았다.", version="statsmodels 0.14.0", kind="sampling_frame", metadata="ns-index.frame-links.json")
source("NAT-PY-CONS", "https://pandas.pydata.org/pandas-docs/version/1.5.3/user_guide/10min.html", "pandas", "String Methods; web lines 602–607; external anchor HTML line 1172", "Series의 str 문맥에서 정규표현식 의미를 설명하는 Python re 문서로 연결한다. 원 href는 https://docs.python.org/3/library/re.html 이며 구체적인 Python 판은 없다.", "pandas 1.5.3의 소비 목적은 확인되지만 소비자가 실제 읽은 Python patch/minor 판은 미확인이다. pandas의 모든 현행 str 기본값을 이 참조로 확정하지 않는다.", version="pandas 1.5.3", date={"consumer_release": "2023-01-18", "date_source_id": "NAT-PANDAS-RELEASE"}, kind="consumer", cases=["N-P-01"], counted=True, group="pandas-1.5.3-10min", refs=["turn956586121view0", "turn827905165view2"], metadata="np01.links.json")
source("NAT-NP-CONS", "https://pandas.pydata.org/pandas-docs/version/1.5.3/user_guide/dsintro.html", "pandas", "Series is ndarray-like; web lines 174–192, especially 185; external anchor HTML line 701", "Series/ExtensionArray를 설명하면서 구체적인 배열인 numpy.ndarray로 연결하고 실제 ndarray가 필요하면 to_numpy 사용을 설명한다. 원 href는 stable 문서의 #numpy.ndarray이다.", "대상 NumPy 판은 소비 본문에 명시되지 않았다. 현행 ndarray 개념과 이 구판 pandas API 전체의 호환성은 서로 다른 질문이다.", version="pandas 1.5.3", date={"consumer_release": "2023-01-18", "date_source_id": "NAT-PANDAS-RELEASE"}, kind="consumer", cases=["N-P-02"], counted=True, group="pandas-1.5.3-dsintro", refs=["turn956586121view1", "turn261720511view1"], metadata="np02.links.json")
source("NAT-FF-CONS", "https://www.statsmodels.org/v0.14.0/examples/notebooks/generated/rolling_ls.html", "statsmodels", "Fama-French example, web lines 89–111, 152–161, 219–239; footer line 312; external anchor HTML line 902", "Ken French 자료에서 월별 요인과 산업 수익률을 가져와 60개월 RollingOLS/CAPM 및 3요인 예제를 수행한다. 출력의 1926-07 Mkt-RF는 2.96이다. 문서 갱신일은 2023-05-05이다.", "갱신일은 statsmodels 릴리스 날짜나 다운로드 컷의 날짜가 아니다. 본문은 오늘의 최신 계열 사용과 과거 표시 출력 재현 중 하나를 명시하지 않는다. 표의 마지막 출력은 2023-03까지라 2022-07 보관 ZIP 전체와 동일판이라고 할 수 없다.", version="statsmodels 0.14.0", date={"consumer_document_last_update": "2023-05-05", "software_release": "미확인"}, kind="consumer", cases=["N-S-01"], counted=True, group="statsmodels-0.14.0-rolling", refs=["turn826237933view2", "turn374538255view0", "turn476703322view0"], metadata="ns05.links.json")
source("NAT-UCLA-CONS", "https://www.statsmodels.org/v0.14.0/examples/notebooks/generated/regression_plots.html", "statsmodels", "Statewide Crime 2009, web lines 303–322; robust regression lines 408–409; footer 501; raw href HTML line 1290", "회귀/영향/강건 추정 그림을 UCLA Stata 예제와 비교하도록 지시하며 자료가 다르고 이전 예제는 주석 해제로 실행할 수 있다고 밝힌다. 원 href는 ats.ucla.edu의 answers4.htm이다.", "소비 문서는 특정 UCLA 판/날짜를 명시하지 않는다. 다른 데이터라는 고지를 무시하고 수치가 동일해야 한다고 채점하면 안 된다.", version="statsmodels 0.14.0", date={"consumer_document_last_update": "2023-05-05", "software_release": "미확인"}, kind="consumer", cases=["N-S-02"], counted=True, group="statsmodels-0.14.0-regressionplots", refs=["turn807193467view2", "turn476703322view1"], metadata="ns10.links.json")

# Source work 1: Python re. Multiple releases count as one target work.
source("NAT-PY-OLD", "https://docs.python.org/release/3.11.1/library/re.html", "Python Software Foundation", "re — Regular expression operations, introductory paragraph; rendered HTML line 186", "3.11.1 제목이 있는 발행자 HTML에서 정규표현식 matching operations라는 최소 발췌를 직접 확인했다.", "웹 도구는 실패했으나 urllib 직접 열람은 HTTP 200으로 성공했다. 3.11.1은 연구자가 선택한 당대 후보판이며 실제 소비자가 읽었다는 증거가 없다. URL 자체가 2022년에 존재했다는 시점별 캡처는 없다.", version="Python 3.11.1 exact release HTML", date={"target_release": "2022-12-06", "date_source_id": "NAT-PY-RELEASE"}, kind="target", cases=["N-P-01"], counted=True, group="python-re-manual", metadata="python-release-doc.metadata.json", independent=True)
source("NAT-PY-CURRENT", "https://docs.python.org/3/library/re.html", "Python Software Foundation", "re — Regular expression operations, first paragraph web line 7; escape warning line 10", "현재 /3/ 별칭의 제목은 Python 3.15.2이며 같은 정규표현식 연산 정의를 확인했다. escape warning의 표현은 현재 SyntaxWarning으로 보인다.", "가변 별칭이며 현행판은 열람 시점 관측이다. 선택된 최소 발췌는 유지되지만 다른 문구의 변화를 전체 문서 의미 불변으로 일반화할 수 없다.", version="observed Python 3.15.2; URL floating", kind="target", cases=["N-P-01"], group="python-re-manual", refs=["turn993123680view2", "turn664601430view2"], independent=True)
source("NAT-PY-GIT-OLD", "https://raw.githubusercontent.com/python/cpython/v3.11.1/Doc/library/re.rst", "Python Software Foundation / CPython", "Doc/library/re.rst, lines 14–15", "발행자 소스 태그 v3.11.1에서도 같은 최소 발췌를 직접 확인했다.", "동일 매뉴얼의 소스 배포이며 새 저작으로 산입하지 않는다. web 도구 실패 뒤 urllib로 읽었다.", version="cpython tag v3.11.1", kind="target", cases=["N-P-01"], group="python-re-manual", metadata="python-old.observation.json", independent=True)
source("NAT-PY-MINOR-ALIAS", "https://docs.python.org/3.11/library/re.html", "Python Software Foundation", "Title and first paragraph web line 7", "3.11 문서의 현재 제목은 3.11.18이고 선택된 정의는 동일하다.", "소비 시점의 patch 판을 고정하지 못해 exact L 후보에서 제외했다. 이 열람은 진단용이다.", version="observed Python 3.11.18; minor-series alias", kind="target", cases=["N-P-01"], group="python-re-manual", refs=["turn826237933view0", "turn844788299view3"], independent=True)
source("NAT-PY-RELEASE", "https://www.python.org/downloads/release/python-3111/", "Python Software Foundation", "release title and date web lines 21–25; Online Documentation href at 52", "Python 3.11.1의 릴리스 날짜는 2022-12-06이다. 이 릴리스 페이지의 Online Documentation 실제 href는 /3.11/로 현재 patch 별칭이다.", "발행일은 3.11.1이 소비 문서 릴리스 전 존재했다는 증거이나 exact HTML 주소의 당시 존재는 직접 증명하지 않는다. 릴리스 페이지 링크 자체가 exact patch를 고정하지 않는 반례다.", version="Python 3.11.1 release record", date={"target_release": "2022-12-06"}, kind="release_notice", cases=["N-P-01"], refs=["turn672433009view1"], independent=True)
source("NAT-PANDAS-RELEASE", "https://pandas.pydata.org/pandas-docs/version/1.5.3/whatsnew/v1.5.3.html", "pandas", "What’s new in 1.5.3 title/date", "pandas 1.5.3의 공식 릴리스 날짜가 2023-01-18이라고 적혀 있다.", "소비 문서의 릴리스 시점을 주지만 각각의 외부 참조 삽입일은 확인하지 않는다.", version="pandas 1.5.3", date={"software_release": "2023-01-18"}, kind="release_notice", cases=["N-P-01", "N-P-02"], refs=["turn672433009view2"], independent=True)

# Source work 2: NumPy ndarray.
source("NAT-NP-OLD", "https://numpy.org/doc/1.24/reference/generated/numpy.ndarray.html", "NumPy", "numpy.ndarray, web lines 201–206; anchor #numpy.ndarray", "NumPy v1.24 매뉴얼에서 ndarray는 고정 크기 항목으로 된 다차원 동질 배열이라는 정의를 확인했다.", "1.24 minor 판 주소이며 exact patch 또는 불변 바이트는 확인하지 않았다. 1.24를 실제 pandas 소비자가 읽었다는 증거는 없다.", version="NumPy v1.24 Manual", date={"release_1_24_0": "2022-12-18", "date_source_id": "NAT-NP-NEWS"}, kind="target", cases=["N-P-02"], counted=True, group="numpy-ndarray-manual", refs=["turn826237933view1"], independent=True)
source("NAT-NP-CURRENT", "https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray", "NumPy", "numpy.ndarray signature/definition, web lines 209–212", "stable의 현재 제목은 NumPy v2.5 Manual이며 선택된 ndarray 정의가 v1.24와 같다.", "stable 별칭은 가변이고 타입 signature나 다른 API까지 동일하다고 보지 않는다.", version="observed NumPy v2.5 Manual; stable URL", kind="target", cases=["N-P-02"], group="numpy-ndarray-manual", refs=["turn993123680view3", "turn672433009view3"], independent=True)
source("NAT-NP-NEWS", "https://numpy.org/news/", "NumPy", "NumPy 1.24.0 release entry, web lines 136–144; historical release list at 294", "공식 뉴스는 1.24.0의 공개일을 2022-12-18로 제시한다. 1.24.1은 2022-12-26으로 목록에 있다.", "릴리스가 소비 시점 전 존재했음을 보이나 현재 /doc/1.24/ 문서의 개별 HTML이 당시 같았다는 증명은 아니다.", version="news historical release entries", date={"release_1_24_0": "2022-12-18", "release_1_24_1": "2022-12-26"}, kind="release_notice", cases=["N-P-02"], refs=["turn276894918view1"], independent=True)
source("NAT-NP-RELEASE", "https://numpy.org/doc/1.24/release/1.24.0-notes.html", "NumPy", "NumPy 1.24.0 Release Notes, introduction web lines 126–137", "1.24.0 발행 공지를 별도 문서로 열고 지원 Python 범위 등 릴리스 설명을 확인했다.", "ndarray 선택 문장의 채점 기준 자체가 아니라 판 관계를 보강하는 자료다.", version="NumPy 1.24.0 release notes", date={"release_1_24_0": "2022-12-18", "date_source_id": "NAT-NP-NEWS"}, kind="release_notice", cases=["N-P-02"], refs=["turn844788299view0"], independent=True)

# Source work 3: French factors. Numeric data and notices remain separate.
source("NAT-FF-OLD", "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/Historical_Archives/08%202022%20Update/ftp/F-F_Research_Data_Factors_CSV.zip", "Kenneth R. French / Dartmouth Tuck", "ZIP member Historical_Archives/08 2022 Update/ftp/F-F_Research_Data_Factors.CSV; header line 4; 192607 row line 5", "2022-07 CRSP 컷 보관물의 192607 행은 Mkt-RF=2.96, SMB=-2.56, HML=-2.43, RF=0.22이다. 마지막 월별 행은 202207이다.", "소비 출력의 첫 행과 일치하지만 소비 출력은 2023-03까지 있어 이 ZIP 전체가 실제 소비 판이었다고 할 수 없다. 웹 도구 ZIP 해석 실패 후 직접 다운로드/멤버 해석으로 읽었다.", version="July 2022 data cut / August 2022 archive", date={"data_cut": "2022-07", "archive_release_month": "2022-08", "date_source_id": "NAT-FF-ARCHIVE"}, kind="target", cases=["N-S-01"], counted=True, group="french-three-factors", metadata="ff-old.observation.json", independent=True)
source("NAT-FF-CURRENT", "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip", "Kenneth R. French / Dartmouth Tuck", "ZIP member F-F_Research_Data_Factors.csv; header line 5; 192607 row line 6", "현행 파일의 192607 행은 Mkt-RF=2.89, SMB=-2.42, HML=-2.75, RF=0.22이다. 헤더 컷과 마지막 월별 행은 202609이다.", "현행 파일은 열람 시점의 관측이다. 2.96을 정확히 보존했더라도 최신 계열의 같은 기간 값은 다르지만, 이것만으로 소비자가 최신값을 원했다고 단정하지 않는다.", version="current ZIP, CRSP data cut 202609", date={"data_cut": "2026-09", "publication_day": "미확인"}, kind="target", cases=["N-S-01"], group="french-three-factors", metadata="ff-current.observation.json", independent=True)
source("NAT-FF-INDEX", "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html", "Kenneth R. French / Dartmouth Tuck", "FIZ/CIZ notice web lines 13–15; Fama/French 3 Factors download and historical archives links at 133", "현재 원래 B URL은 요인 파일과 historical archive로 연결한다. FIZ가 2024-12 이후 중단되고 2025-01부터 CIZ를 쓰며 월별 복리/배당 처리 정의가 달라졌다고 설명한다.", "자료 설명과 href를 읽었으며 단순 HTTP 200으로 판을 확정하지 않았다. 2023년 동일 URL 본문을 직접 확보하지 않아 같은 URL의 전후 본문 전체 비교는 미확인이다.", version="floating publisher data library", date={"format_transition": "2025-01", "legacy_last_month": "2024-12"}, kind="target", cases=["N-S-01"], group="french-three-factors", refs=["turn374538255view1"], independent=True)
source("NAT-FF-ARCHIVE", "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors_archive.html", "Kenneth R. French / Dartmouth Tuck", "archive policy web lines 13–18; July 2022 CSV href id 12", "연별 July 컷이 August에 공개되며 해당월이 없으면 다음 보관물을 쓰라는 정책을 확인했고 July 2022 ZIP 실제 href를 따라갔다.", "원 소비자의 실제 다운로드 컷은 알려주지 않는다. 2022-07은 소비 마지막갱신 전의 연별 보관 후보이다.", version="Fama/French 3 Factors historical archive index", date={"archive_release_rule": "July cut released in August"}, kind="release_notice", cases=["N-S-01"], refs=["turn981757178view0"], independent=True)
source("NAT-FF-CHANGES", "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/changes_crsp.html", "Kenneth R. French / Dartmouth Tuck", "Changes in CRSP Data, web lines 14–16", "CRSP 과거 자료 변경과 2025년 FIZ/CIZ 전환을 별도 발행자 설명에서 확인했다.", "이 공지는 선택된 192607 2.96→2.89의 차이 중 어떤 변경이 얼마나 기여했는지 분해하지 않는다.", version="Changes in CRSP Data", date={"format_transition": "2025-01"}, kind="revision_notice", cases=["N-S-01"], refs=["turn981757178view2"], independent=True)
source("NAT-FF-202412", "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library_202412_archive.html", "Kenneth R. French / Dartmouth Tuck", "archive label lines 13–14; historical data revision statement 155; annual archive policy 165", "2024-12 FIZ 보관 페이지는 매달 전체 이력을 다시 만들며 CRSP 변경 때문에 과거 수익률도 달라질 수 있다고 명시한다.", "소비 시점 2023-05보다 늦은 판으로 L 당대판에는 쓰지 않았다. 동일 대상 자료의 다른 판이므로 추가 target 수에 넣지 않는다.", version="December 2024 FIZ archive", date={"data_cut": "2024-12"}, kind="target", cases=["N-S-01"], group="french-three-factors", refs=["turn981757178view1"], independent=True)

# Source work 4: UCLA historical page remains unresolved.
source("NAT-UCLA-CURRENT", "https://stats.oarc.ucla.edu/stata/webbooks/reg/chapter4/regressionwith-statachapter-4-answers-to-excersises/", "UCLA OARC", "archive warning web line 36; Answer 1 lines 40–66; robust variants 75–139", "공식 보관 답안은 더 이상 유지하지 않는 페이지라고 밝힌다. Answer 1에서 murder를 pctmetro/poverty/pcths/single로 설명하는 51개 관측 회귀와 DC 영향 및 강건 변형을 다룬다.", "공개일·수정일·버전 연결은 미확인이다. 지금 읽은 본문을 소비 당대의 같은 절로 단정할 수 없으므로 역사 X를 추출하지 않았다. 최신 방법의 권고 기준으로 확장하지 않는다.", version="undated publisher archived page; not version pinned", kind="target", cases=["N-S-02"], counted=True, group="ucla-stata-ch4-answers", refs=["turn534018895view0", "turn534018895view1"], metadata="ucla-current.metadata.json", independent=False)
source("NAT-UCLA-BOOK", "https://stats.oarc.ucla.edu/stata/webbooks/reg/stata-web-books-regression-with-stata/", "UCLA OARC", "chapter 4 TOC, web lines 76–92; answers href id 16", "공식 책 목차에서 현재 답안 페이지로 가는 실제 href를 확인했다.", "목차 링크는 현재 탐색 경로이며 옛 ats 주소와 현판의 문장 동일성을 보증하지 않는다.", kind="navigation", cases=["N-S-02"], refs=["turn364401805view1"])
source("NAT-UCLA-CH4", "https://stats.oarc.ucla.edu/stata/webbooks/reg/chapter4/regressionwith-statachapter-4-beyond-ols-2/", "UCLA OARC", "self-assessment and answer link, web lines 1324–1371; answers href id 8", "공식 장의 자기평가 부분에서도 답안으로 가는 실제 링크를 확인했다.", "장 본문이 현재 공개되어 있다는 사실은 당대 답안의 판 고정 증거가 아니다.", kind="navigation", cases=["N-S-02"], refs=["turn364401805view0"])
source("NAT-UCLA-ISSUE", "https://api.github.com/repos/statsmodels/statsmodels/issues/808/comments", "statsmodels maintainers / GitHub", "comment id 17410423; html anchor https://github.com/statsmodels/statsmodels/issues/808#issuecomment-17410423", "jseabold가 2013-05-03에 원 ats UCLA URL을 제시하며 regression plots notebook을 작성할 때 사용했다고 직접 진술했다.", "실제 소비 목적과 원 주소의 오래된 참조 흔적은 보강하지만 URL의 당시 접근 성공·발행판 내용 동일성·현재 OARC 페이지로의 공식 판 관계는 확인하지 않는다.", date={"consumer_author_statement": "2013-05-03T18:28:55Z"}, kind="consumer_provenance", cases=["N-S-02"], refs=["turn377332176view0"], metadata="ucla-issue808.comments.metadata.json", mode="author_statement")
source("NAT-STATSMODELS-RELEASE", "https://www.statsmodels.org/v0.14.0/release/version0.14.0.html", "statsmodels", "Release 0.14.0 heading and release content", "0.14.0 발행 기록을 별도로 열었다.", "정확한 릴리스 날짜를 이 열람 범위에서 확인하지 못했다. 예제의 Last update 날짜를 릴리스일로 대체하지 않는다.", version="statsmodels 0.14.0", kind="release_notice", cases=["N-S-01", "N-S-02"], refs=["turn664601430view1"])

# Exact attempted addresses: failures are never counted as read originals.
for sid, url, ref, reason, case, metadata in [
    ("NAT-FAIL-PY-RENDERED", "https://docs.python.org/release/3.11.1/library/re.html", "turn672433009view0", "web tool open failed; later direct urllib body read succeeded (NAT-PY-OLD)", "N-P-01", None),
    ("NAT-FAIL-PY-RAW", "https://raw.githubusercontent.com/python/cpython/v3.11.1/Doc/library/re.rst", "turn276894918view0", "web tool DisabledError; later urllib body read succeeded", "N-P-01", None),
    ("NAT-FAIL-PY-BLOB", "https://github.com/python/cpython/blob/v3.11.1/Doc/library/re.rst", "turn807193467view1", "web tool body access failed; raw publisher source later read", "N-P-01", None),
    ("NAT-FAIL-FF-OLD-ZIP", "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/Historical_Archives/08%202022%20Update/ftp/F-F_Research_Data_Factors_CSV.zip", "turn844788299view1", "web tool could not decode ZIP; later direct member read succeeded", "N-S-01", None),
    ("NAT-FAIL-FF-CURRENT-ZIP", "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip", "turn844788299view2", "web tool could not decode ZIP; later direct member read succeeded", "N-S-01", None),
    ("NAT-FAIL-UCLA-ATS", "http://www.ats.ucla.edu/stat/stata/webbooks/reg/chapter4/statareg_self_assessment_answers4.htm", "turn807193467view0", "web upgraded/attempted legacy ats endpoint and failed; historical body remains unverified", "N-S-02", None),
    ("NAT-FAIL-UCLA-IDRE", "https://stats.idre.ucla.edu/stat/stata/webbooks/reg/chapter4/statareg_self_assessment_answers4.htm", "turn664601430view0", "web failed and direct urllib returned HTTP 404", "N-S-02", "ucla-legacy-idre.failure.json"),
]:
    source(sid, url, "publisher endpoint attempted", "attempted complete document/member; no body from this attempt", "미확인", reason + "; first resume evidence: " + {"N-P-01": "NAT-PY-OLD", "N-S-01": "NAT-FF-OLD/NAT-FF-CURRENT", "N-S-02": "dated publisher archive of original ats URL"}[case], kind="access_failure", cases=[case], refs=[ref], metadata=metadata, direct=False, mode="access_observation", outcome="failed")

# Unselected candidates: preserve href-scan exclusions without claiming semantic target reads.
excluded = {
    1: ("no_external_body_href", "외부 발행자 본문 href 없음"),
    2: ("no_external_body_href", "외부 발행자 본문 href 없음"),
    3: ("bibliography_without_href", "Koenker/Hallock 등의 서지 텍스트는 있으나 외부 원문 href 없음"),
    4: ("bibliography_without_href", "Lucas/Sargent 등 서지 텍스트는 있으나 외부 원문 href 없음"),
    6: ("same_publisher_links_only", "statsmodels stable 진단/그래픽 href는 동일 발행자 내부 문서"),
    7: ("no_external_body_href", "외부 발행자 본문 href 없음"),
    8: ("no_external_body_href", "외부 발행자 본문 href 없음"),
    9: ("no_external_body_href", "외부 발행자 본문 href 없음"),
}
for n, (status, reason) in excluded.items():
    m = raw(f"ns{n:02}.links.json")
    source(f"NAT-S-SCAN-{n:02}", m["requested_url"], "statsmodels", "body article href scan; exact HTML lines in raw-web metadata", reason, "후보 적격성 확인용으로 본문 링크를 검사했다. 외부 주장 본문을 직접 읽은 출처 수에는 넣지 않는다.", version="statsmodels 0.14.0", kind="candidate_scan", metadata=f"ns{n:02}.links.json", direct=False, mode="observed_href_scan")
for n in (11, 12):
    m = raw(f"ns{n:02}.links.json")
    source(f"NAT-S-SCAN-{n:02}", m["requested_url"], "statsmodels", "body article href scan; exact HTML lines in raw-web metadata", "9·10번 후보와 함께 시작한 병렬 링크 요청의 메타데이터만 확인했다.", "10번에서 정원이 찼으므로 사례 선택이나 주장 근거에 사용하지 않았다. 외부 원문 수에 산입하지 않는다.", version="statsmodels 0.14.0", kind="candidate_scan_after_quota", metadata=f"ns{n:02}.links.json", direct=False, mode="observed_href_scan")
source("NAT-UCLA-ISSUE-PAGE", "https://github.com/statsmodels/statsmodels/issues/808", "statsmodels maintainers / GitHub", "issue title web 135; author/open date 162–164; body 167–186", "RLM influence statistics issue가 2013-05-03에 열렸고 예제 코드를 포함함을 확인했다.", "일반 웹 열람 결과에는 UCLA 참조 댓글이 생략되어 별도 공개 comments API로 해당 댓글을 읽었다. 이 페이지 열람만으로 UCLA 참조를 확인했다고 하지 않는다.", date={"issue_opened": "2013-05-03"}, kind="consumer_provenance", cases=["N-S-02"], refs=["turn377332176view0"], mode="author_statement")

with (BASE / "sources.jsonl").open("w") as f:
    for row in sources:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

frame_rows = []
for frame_id, filename in [("N-P", "np-index.frame-links.json"), ("N-S", "ns-index.frame-links.json")]:
    ledger = raw(filename)
    for n, link in enumerate(ledger["links"][:25], 1):
        case_id, status, reason, semantic = "", "not_reviewed_quota_filled", "첫 두 적격 이후 본문 미검토", False
        if frame_id == "N-P" and n <= 2:
            case_id, status, reason, semantic = f"N-P-{n:02}", "selected", "첫 적격 문서/대상; 외부 목적과 원 href 확인", True
        elif frame_id == "N-S":
            if n in (5, 10):
                case_id, status, reason, semantic = ("N-S-01" if n == 5 else "N-S-02"), "selected", "문서 순·본문 외부 href 순에서 첫 적격", True
            elif n in excluded:
                status, reason = excluded[n]
            elif n in (11, 12):
                status, reason = "link_scanned_after_quota", "9·10과 병렬 요청되어 링크 메타데이터만 읽음; 후보 교체에 사용 안 함"
        frame_rows.append({
            "frame_id": frame_id, "exposure_order": n, "ledger_url": ledger["index"],
            "query": "body TOC order; no search query", "period_or_version": "pandas 1.5.3" if frame_id == "N-P" else "statsmodels 0.14.0",
            "candidate_title": link["label"], "candidate_url": link["resolved_href"], "raw_href": link["raw_href"],
            "index_html_line": link["html_line"], "status": status, "case_id": case_id, "reason": reason,
            "semantic_consumer_read": semantic, "duplicate_rule": "fragment stripped; first unique document URL; external target work unique",
            "replacement_ledger_used": False, "checked_utc": ledger["checked_utc"], "evidence_file": "collection/natural/raw-web/" + filename,
        })
with (BASE / "frame.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(frame_rows[0]))
    writer.writeheader(); writer.writerows(frame_rows)


def consumer(case, sid, name, url, href, locator, purpose, quote, explicit, last_update, **extra):
    return {"case_id": case, "stratum": "natural", "consumer_source_id": sid, "consumer_title": name, "consumer_url": url, "original_raw_href": href, "consumer_locator": locator, "observed_purpose": purpose, "purpose_status": "researcher paraphrase of observed consumer sentence", "consumer_short_quote": quote, "consumer_explicit_target_version": explicit, "consumer_date": last_update, "B_already_pinned": False, "B_target_version_is_unknown": True, "actual_consumer_target_version_uncertain": True, "collection_stage": "source research only; no card reading or judgment performed", **extra}


cases = []
cases.append(consumer(
    "N-P-01", "NAT-PY-CONS", "10 minutes to pandas — String Methods",
    "https://pandas.pydata.org/pandas-docs/version/1.5.3/user_guide/10min.html",
    "https://docs.python.org/3/library/re.html", "String Methods; web 602–607 / raw href HTML 1172",
    "Series.str에서 쓰는 정규표현식의 의미를 이해하기 위해 Python re 문서를 참조", "regular expressions", "Python 3 family only; minor/patch 미확인", "2023-01-18 release",
    frame_id="N-P", frame_order=1, body_external_href_order=1,
    intended_time="소비자의 구체적인 Python 판은 미확인; 선택된 정의의 참조 목적은 구판과 현판 모두에 성립",
    reconstructed_target_edition="Python 3.11.1",
    selection_rule="소비 릴리스 전 2022-12-06에 공개된 Python 3.11.1을 당대 후보판으로 재구성; 실제 소비판 또는 모든 후보 중 최신이라고 주장하지 않음",
    old_target_url="https://docs.python.org/release/3.11.1/library/re.html",
    old_target_locator="re — Regular expression operations, introductory paragraph, HTML line 186",
    old_target_source_id="NAT-PY-OLD", current_target_url="https://docs.python.org/3/library/re.html",
    current_target_locator="first definition, web line 7; observed title Python 3.15.2", current_target_source_id="NAT-PY-CURRENT",
    L={"url": "https://docs.python.org/release/3.11.1/library/re.html", "locator": "re — Regular expression operations, introductory paragraph", "version_pinned": True, "granularity": "exact release 3.11.1", "locator_kind": "reconstructed_contemporaneous_edition", "existed_at_consumer_time": "edition release confirmed; exact URL existence 미확인", "existence_source_id": "NAT-PY-RELEASE"},
    X={"text": "This module provides regular expression matching operations", "source_id": "NAT-PY-OLD", "locator": "HTML line 186", "available": True, "verified_same_reconstructed_old_section": True, "verified_actual_consumer_old_edition": False, "contains_version_cue": False, "contains_url_cue": False, "word_count": 7},
    current_gold_action="유지", current_gold_scope="정규표현식 연산에 관한 참조의 선택된 기본 정의만; pandas 현행 API 전체나 default 인수값은 제외",
    current_gold_basis="구판과 현행 별도 발행본문에서 같은 정의 확인", current_criterion_confirmed=True, current_criterion_independent_edition=True, current_criterion_source_ids=["NAT-PY-OLD", "NAT-PY-CURRENT", "NAT-PY-RELEASE"],
    historical_gold_strict="미확인", historical_strict_criterion_confirmed=False,
    historical_reconstructed_gold="publisher_edition_match possible for explicitly reconstructed 3.11.1; actual consumer edition remains unknown",
    historical_reconstructed_criterion_confirmed=True,
    limits=["원 Python 판 미명시", "작성자가 원판/현판을 이미 읽었으므로 후속 판독은 비가림", "release page의 Online Documentation은 /3.11/ 가변 patch 별칭"]
))
cases.append(consumer(
    "N-P-02", "NAT-NP-CONS", "Intro to data structures — Series is ndarray-like",
    "https://pandas.pydata.org/pandas-docs/version/1.5.3/user_guide/dsintro.html",
    "https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray", "Series is ndarray-like; web 174–192 / raw href HTML 701",
    "Series/ExtensionArray의 구체 배열을 이해하고 실제 ndarray가 필요할 때 to_numpy 사용 맥락을 확인", "numpy.ndarray", "미확인", "2023-01-18 release",
    frame_id="N-P", frame_order=2, body_external_href_order=1,
    intended_time="대상 NumPy 판은 미명시; 선택된 ndarray 개념의 의미는 비교한 두 판에서 동일",
    reconstructed_target_edition="NumPy v1.24 minor-series manual",
    selection_rule="소비 릴리스 전 2022-12-18에 공개된 1.24 계열 매뉴얼을 당대 후보로 재구성; exact patch/실제 소비판 미확인",
    old_target_url="https://numpy.org/doc/1.24/reference/generated/numpy.ndarray.html#numpy.ndarray",
    old_target_locator="numpy.ndarray definition, web lines 201–206", old_target_source_id="NAT-NP-OLD",
    current_target_url="https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray", current_target_locator="numpy.ndarray definition, web line 212; observed v2.5", current_target_source_id="NAT-NP-CURRENT",
    L={"url": "https://numpy.org/doc/1.24/reference/generated/numpy.ndarray.html#numpy.ndarray", "locator": "numpy.ndarray, first definition", "version_pinned": True, "granularity": "minor series 1.24 only; patch/byte immutability 미확인", "locator_kind": "reconstructed_contemporaneous_edition", "existed_at_consumer_time": "series release confirmed; exact URL existence 미확인", "existence_source_id": "NAT-NP-NEWS"},
    X={"text": "multidimensional, homogeneous array of fixed-size items", "source_id": "NAT-NP-OLD", "locator": "numpy.ndarray first definition, web line 206", "available": True, "verified_same_reconstructed_old_section": True, "verified_actual_consumer_old_edition": False, "contains_version_cue": False, "contains_url_cue": False, "word_count": 6},
    current_gold_action="유지", current_gold_scope="ndarray의 선택된 개념 정의; pandas 구판 코드와 NumPy 현행판 전체 호환성은 제외",
    current_gold_basis="1.24와 현행 2.5 별도 발행 매뉴얼의 선택 문장이 동일", current_criterion_confirmed=True, current_criterion_independent_edition=True, current_criterion_source_ids=["NAT-NP-OLD", "NAT-NP-CURRENT", "NAT-NP-NEWS"],
    historical_gold_strict="미확인", historical_strict_criterion_confirmed=False,
    historical_reconstructed_gold="publisher_edition_match possible for stated NumPy 1.24 series; patch and actual consumer edition remain unknown",
    historical_reconstructed_criterion_confirmed=True,
    limits=["원 NumPy 판 미명시", "1.24 URL은 exact patch 불변 주소가 아님", "선택된 짧은 정의의 동일성을 전체 API 불변으로 확장하지 않음"]
))
cases.append(consumer(
    "N-S-01", "NAT-FF-CONS", "Rolling Regression — Fama-French factors",
    "https://www.statsmodels.org/v0.14.0/examples/notebooks/generated/rolling_ls.html",
    "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html", "Fama-French data 89–111; 60-month CAPM 152–161; updated at 312; raw href HTML 902",
    "월별 Fama-French 요인 및 산업 수익률로 60개월 이동 CAPM/3요인 회귀 예제를 수행", "monthly returns", "미확인", "2023-05-05 document last update; software release date 미확인",
    frame_id="N-S", frame_order=5, body_external_href_order=1,
    intended_time="미확인", intended_time_evidence="목적은 월별 자료를 받는 교육 예제이며 start=1926과 출력 수치가 있으나 원출력 복원/오늘 최신 개정계열 중 하나를 명시하지 않음",
    reconstructed_target_edition="July 2022 data cut / August 2022 annual archive",
    selection_rule="2023-05-05 문서 갱신 전의 연별 July 보관물 중 가장 가까운 July 2022 실제 href 선택. 소비 출력은 2023-03까지이므로 이 archive 전체가 실제 소비판이라는 주장은 금지",
    old_target_url="https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/Historical_Archives/08%202022%20Update/ftp/F-F_Research_Data_Factors_CSV.zip",
    old_target_locator="Historical_Archives/08 2022 Update/ftp/F-F_Research_Data_Factors.CSV, line 5 / record 192607", old_target_source_id="NAT-FF-OLD",
    current_target_url="https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip", current_target_locator="F-F_Research_Data_Factors.csv, line 6 / record 192607; CRSP cut 202609", current_target_source_id="NAT-FF-CURRENT",
    L={"url": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/Historical_Archives/08%202022%20Update/ftp/F-F_Research_Data_Factors_CSV.zip", "locator": "member Historical_Archives/08 2022 Update/ftp/F-F_Research_Data_Factors.CSV; record 192607", "version_pinned": True, "granularity": "annual publisher archive July 2022", "locator_kind": "reconstructed_preconsumer_data_cut", "existed_at_consumer_time": "publisher annual archive policy supports August 2022 release; exact original URL timestamp 미확인", "existence_source_id": "NAT-FF-ARCHIVE"},
    X={"text": "192607,    2.96,   -2.56,   -2.43,    0.22", "source_id": "NAT-FF-OLD", "locator": "ZIP member line 5, columns month/Mkt-RF/SMB/HML/RF", "available": True, "verified_same_reconstructed_old_section": True, "verified_actual_consumer_old_edition": False, "contains_version_cue": False, "contains_url_cue": False, "contains_observation_period": True, "observation_period_is_not_release_version": True, "word_count": 5},
    current_gold_action="보류", current_gold_hold_reason="time_intent_unknown", current_gold_scope="소비 목적의 시간 의도가 미명시이므로 값 선택을 유보; 읽을 수 없어서 생긴 보류가 아님",
    current_gold_basis="사전 규칙에서 시간 의도 미명시는 보류. 독립 발행자료는 옛값과 현값의 차이는 확인하지만 소비자 의도를 정하지 않음", current_criterion_confirmed=True, current_criterion_independent_edition=True, current_criterion_source_ids=["NAT-FF-CONS", "NAT-FF-OLD", "NAT-FF-CURRENT", "NAT-FF-CHANGES"],
    current_conditional_expectations=[{"condition": "표시된 과거 192607 첫 행 재현", "action": "유지", "value": "Mkt-RF 2.96", "scope_limit": "선택한 첫 행만; 전체 notebook 출력 재현은 이 archive로 불가능"}, {"condition": "오늘 제공되는 수정 계열로 같은 기간 분석", "action": "교체", "value": "Mkt-RF 2.89 as observed at checked_utc", "scope_limit": "현행 자료 컷/형식 명시 필요"}],
    historical_gold_strict="미확인", historical_strict_criterion_confirmed=False,
    historical_reconstructed_gold="publisher_edition_match possible for July 2022 archive record 192607; actual consumer download version unknown",
    historical_reconstructed_criterion_confirmed=True,
    observed_content_difference={"record": "192607", "field": "Mkt-RF", "old": "2.96", "current": "2.89", "causal_attribution_of_change": "미확인", "actual_X_caused_current_error": "not tested; no card reading yet"},
    limits=["통계 기준월과 공개/개정월 구분", "원출력 재현과 최신분석 목적 분리", "선택한 보관 ZIP은 consumer 전체출력과 같은판이 아님", "동일 URL 과거 HTTP 본문 캡처는 확보하지 못함"]
))
cases.append(consumer(
    "N-S-02", "NAT-UCLA-CONS", "Regression Plots — Statewide Crime 2009",
    "https://www.statsmodels.org/v0.14.0/examples/notebooks/generated/regression_plots.html",
    "http://www.ats.ucla.edu/stat/stata/webbooks/reg/chapter4/statareg_self_assessment_answers4.htm", "web 303–322, 408–409; raw href HTML 1290; footer 501",
    "다른 데이터라는 고지 하에 Stata 예제와 회귀/영향/강건 추정 그림을 비교하고 원 예제 재실행 경로를 제공", "Compare the following", "미확인", "2023-05-05 document last update; 2013-05-03 author reference in issue comment",
    frame_id="N-S", frame_order=10, body_external_href_order=1,
    intended_time="특정판/최신방법 권고 여부 미확인; 소비 문서 목적은 예제 비교",
    reconstructed_target_edition="미확인", selection_rule="첫 적격 소비 문서를 유지; legacy 실패를 성공 사례로 교체하지 않음",
    old_target_url="http://www.ats.ucla.edu/stat/stata/webbooks/reg/chapter4/statareg_self_assessment_answers4.htm", old_target_locator="미확인", old_target_source_id="NAT-FAIL-UCLA-ATS",
    current_target_url="https://stats.oarc.ucla.edu/stata/webbooks/reg/chapter4/regressionwith-statachapter-4-answers-to-excersises/", current_target_locator="archived warning at web 36; Answer 1 at 40–139", current_target_source_id="NAT-UCLA-CURRENT",
    L={"url": "https://stats.oarc.ucla.edu/stata/webbooks/reg/chapter4/regressionwith-statachapter-4-answers-to-excersises/", "locator": "Answer 1", "version_pinned": False, "granularity": "미확인", "locator_kind": "replacement_locator_only", "existed_at_consumer_time": "미확인", "existence_source_id": "NAT-UCLA-ISSUE supports original URL reference, not replacement existence"},
    X={"text": "미확인", "source_id": "미확인", "locator": "미확인", "available": False, "verified_same_reconstructed_old_section": False, "verified_actual_consumer_old_edition": False, "contains_version_cue": "미확인", "contains_url_cue": "미확인", "word_count": "미확인", "missing_reason": "당대 발행판의 같은 절을 확인할 수 없어 현 보관본문을 역사 X로 전용하지 않음"},
    current_gold_action="미확인", current_gold_scope="현 UCLA 보관 예제는 비교 소재로 열리지만 독립적인 최신 사용 권고/판 관계가 없어서 확정 채점 기준은 미확인",
    current_gold_basis="현재 보관 페이지의 예제와 archived 고지는 확인; 시대/판을 넘는 방법의 적합성은 별도 기준 부재", current_criterion_confirmed=False, current_criterion_independent_edition=False, current_criterion_source_ids=["NAT-UCLA-CURRENT", "NAT-UCLA-ISSUE"],
    current_provisional_action="보류", current_provisional_hold_reason="criterion_unknown",
    historical_gold_strict="미확인", historical_strict_criterion_confirmed=False, historical_reconstructed_gold="미확인", historical_reconstructed_criterion_confirmed=False,
    historical_original_url_provenance={"source_id": "NAT-UCLA-ISSUE", "author_statement_at": "2013-05-03T18:28:55Z", "proved": "원작성자의 원 URL 사용 진술", "not_proved": "발행자의 해당시점 본문/판·현 OARC 주소 동일성"},
    acceptance_deficit="4요소 완전 비교 미충족: L은 판 고정 주소가 아니고 X는 역사 원문 확인 불가",
    first_resume_action="UCLA 발행자의 날짜 있는 ats 원 URL snapshot/이관 기록 또는 같은 답안의 dated publisher release 확보",
    limits=["당대 원본문 없음", "현재 보관 페이지 날짜 없음", "HTTP 200과 현재 문장 존재를 당대판 대조 성공으로 취급하지 않음"]
))
dump("cases.json", cases)

assert len(cases) == 4
assert len(frame_rows) == 50
assert sum(s["counted"] and s["source_kind"] == "consumer" for s in sources) == 4
assert sum(s["counted"] and s["source_kind"] == "target" for s in sources) == 4
assert len({s["source_id"] for s in sources}) == len(sources)
assert all(s[k] is not None for s in sources for k in ["source_id", "original_url", "pinned_url_or_version", "publisher", "event_or_publication_date", "checked_utc", "locator", "source_kind", "verified_fact", "limitation", "question_ids", "case_ids", "duplicate_group", "counted"])
print(json.dumps({"cases": len(cases), "frame_rows": len(frame_rows), "source_rows": len(sources), "counted_consumers": 4, "counted_target_works": 4, "actual_consumer_edition_verified": 0, "reconstructed_old_sections_verified": 3, "UCLA_full_factorial_deficit": True}, ensure_ascii=False))
