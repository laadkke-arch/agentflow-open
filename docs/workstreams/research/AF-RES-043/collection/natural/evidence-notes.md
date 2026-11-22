# 자연 표본 수집: 원 소비 요구와 판 관계

이 묶음은 ① 사전 계획 원격 봉인 `a6cc61d4c2b6baf7cae47569c1454b371986ce47` 뒤에 수행한 출처 조사다. 카드 실험이나 독립 독자 판독이 아니다. 직접 읽은 본문의 범위, 원 href, 판 관계 및 부족한 관측을 보존하며 루트 작성자가 ② 대조키를 봉인하는 입력으로 사용한다. 하위 조사자는 git 브랜치 전환·커밋을 하지 않았다.

## 표집 순서와 미검토

`frame.csv`는 두 원장 각각 최초 25개 고유 문서 노출을 보존한 50행이다. 원 목차와 후보 문서의 raw href·HTML 행·조회 시각·HTML 해시는 `raw-web/*.links.json`과 `*.frame-links.json`에 있다. HTML 전체나 발행 저작 전체는 저장하지 않았다.

| 원장 | 최초 적격 순서 | 탈락/미검토 경로 | 대체 원장 |
| --- | --- | --- | --- |
| pandas 1.5.3 user guide | 1번 10min→Python re, 2번 dsintro→NumPy ndarray | 3–25번은 정원 충족 뒤 본문 미검토 | 미사용 |
| statsmodels 0.14.0 examples | 5번 rolling_ls→Ken French, 10번 regression_plots→UCLA | 1·2 외부 href 없음; 3·4 서지 텍스트 있으나 외부 원문 href 없음; 6 같은 발행자 stable 문서만; 7–9 외부 href 없음. 11·12는 9·10과 병렬 링크 요청이 시작되어 링크만 읽었으나 선정에 사용하지 않음. 13–25 미검토 | 미사용 |

내부 navigation·fragment는 문서 중복으로 제거했다. 공개 본문에 외부 저작의 이름만 있는 경우 원 href가 확인되지 않아 적격으로 쓰지 않았다. 데이터가 변한 사례를 얻기 위해 앞의 적격 사례를 교체하지 않았다. 네 원 href 모두 가변 주소이고, 소비자는 대상의 구체적인 판을 명시하지 않는다. 소비 문서의 자체 고정판(예: pandas 1.5.3)을 외부 대상판으로 옮겨 적지 않았다.

## 네 사례의 관측과 조건부 기준

| 사례 | 실제 소비 목적과 원 위치 | 추가 L / 같은 절 X | 현재 과업 기준 | 과거 과업 기준과 한계 |
| --- | --- | --- | --- | --- |
| N-P-01 | [pandas String Methods](https://pandas.pydata.org/pandas-docs/version/1.5.3/user_guide/10min.html), web 602–607, raw href HTML 1172. Series.str의 정규표현식 의미 참조 | [Python 3.11.1 re](https://docs.python.org/release/3.11.1/library/re.html), 첫 문단 HTML 186. X는 7단어 최소 발췌 | 선택된 기본 정의는 [현행 re](https://docs.python.org/3/library/re.html) 첫 문단과 같아 **유지**. pandas 현행 기본 인수나 전체 API에 대한 기준이 아님 | 3.11.1 직접 대조는 가능. 실제 소비자가 읽은 Python 판은 **미확인** |
| N-P-02 | [Series is ndarray-like](https://pandas.pydata.org/pandas-docs/version/1.5.3/user_guide/dsintro.html), web 174–192, raw href HTML 701. 구체 배열 개념/변환 목적 | [NumPy 1.24 ndarray](https://numpy.org/doc/1.24/reference/generated/numpy.ndarray.html#numpy.ndarray), 첫 정의. X는 6단어 | 선택된 정의가 [현행 stable ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)와 같아 **유지**. 전체 버전 호환성 판단은 아님 | 1.24 계열의 해당 절 대조 가능. exact patch와 실제 소비판은 **미확인** |
| N-S-01 | [Rolling Regression](https://www.statsmodels.org/v0.14.0/examples/notebooks/generated/rolling_ls.html), web 89–111·152–161. 월별 요인으로 60개월 이동 회귀 | [July 2022 archive ZIP](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/Historical_Archives/08%202022%20Update/ftp/F-F_Research_Data_Factors_CSV.zip), 멤버 `Historical_Archives/08 2022 Update/ftp/F-F_Research_Data_Factors.CSV` 5행. X는 192607 수치 행 | 주 기준 **보류(time_intent_unknown)**. 첫 과거 행 재현이면 2.96 유지, 오늘 제공되는 계열 분석이면 [현행 ZIP](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip) 멤버 `F-F_Research_Data_Factors.csv` 6행의 2.89로 교체 | 2022-07 보관물의 해당 행은 직접 확인. 소비 출력은 2023-03까지라 그 ZIP 전체가 실제 소비판은 아님. 실제 다운로드 컷 **미확인** |
| N-S-02 | [Regression Plots](https://www.statsmodels.org/v0.14.0/examples/notebooks/generated/regression_plots.html), web 303–322·408–409, raw href HTML 1290. 자료 차이를 고지하며 Stata 예제와 비교 | L은 [현 UCLA 보관 답안](https://stats.oarc.ucla.edu/stata/webbooks/reg/chapter4/regressionwith-statachapter-4-answers-to-excersises/), Answer 1의 **대체 위치**일 뿐. 판 고정 false. X는 **미확인** | 독립적인 최신 권고/판 연결 기준이 없어 확정 gold는 **미확인**. 잠정 보류 사유 criterion_unknown | 원 ats 주소 및 다음 IDRE 주소 실패. 당시 절 본문과 현재 페이지의 날짜/판 관계 **미확인**. 완전 4요소 비교 미충족 |

`cases.json`의 `historical_gold_strict`와 `historical_reconstructed_gold`는 분리되어 있다. 전자는 소비자가 실제 본 판을 묻는 엄격 기준이며 네 사례 모두 판 미명시로 미확인이다. 후자는 연구 자극으로 명시한 공개 옛판의 해당 절 대조 가능성이다. 세 사례의 후자를 네 사례의 전자로 대체하면 L의 기여를 과장한다.

## 날짜와 L의 존재 증거

Python 3.11.1은 [공식 릴리스 기록](https://www.python.org/downloads/release/python-3111/) web 21–25에서 2022-12-06 공개를 확인했다. pandas 소비 릴리스는 [공식 1.5.3 공지](https://pandas.pydata.org/pandas-docs/version/1.5.3/whatsnew/v1.5.3.html)의 2023-01-18이다. Python의 exact 릴리스 HTML은 웹 도구 실패 후 urllib로 읽혔고 제목·HTML 186행·해시를 기록했다. 발행일은 판의 선재성을 보이지만 exact URL이 당시에 존재했다는 시점별 캡처는 아니다.

NumPy [공식 뉴스](https://numpy.org/news/)의 1.24.0 항목 web 136–144는 2022-12-18 공개를 명시한다. 1.24 URL은 minor 계열 위치이며 exact patch 고정이나 불변 바이트를 뜻하지 않는다. [별도 릴리스 노트](https://numpy.org/doc/1.24/release/1.24.0-notes.html)도 직접 열었다.

French [보관 원장](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors_archive.html) web 13–18은 July 컷의 August 공개를 설명한다. 직접 따라간 2022년 보관 ZIP과 현행 ZIP의 멤버 이름·수치 행·해시를 저장했다. 192607은 관측 기간으로 X에 들어 있지만 공개판의 날짜 단서는 아니다. statsmodels 예제의 2023-05-05는 문서 Last update이며 소프트웨어 릴리스일은 이번 범위에서 미확인이다.

## UCLA 추가 재개 탐색과 실패의 범위

최초 실패 뒤 공식 UCLA 책 목차와 Chapter 4의 실제 답안 href를 통해 현재 OARC 보관 답안을 열었다. 본문 web 36은 보관되어 더 이상 유지하지 않는다고 밝힌다. 날짜 메타데이터 검색에서도 발행일/수정일을 발견하지 못했다. 원 `ats.ucla.edu` URL의 실패, `stats.idre.ucla.edu/stat/.../statareg_self_assessment_answers4.htm`의 HTTP 404, 현 OARC의 HTTP 200을 각각 기록했다. 200을 당대판 확인으로 승격하지 않았다.

추가 검색 순서는 다음과 같다. 검색 결과만 읽은 자료는 최소 원문 수에 넣지 않았다.

1. `site:stats.oarc.ucla.edu stata "self assessment" "chapter 4"`
2. `site:stats.idre.ucla.edu "statareg_self_assessment_answers4"`
3. `"statareg_self_assessment_answers4.htm" "UCLA"`
4. `site:stats.oarc.ucla.edu "Answers to Excersises" date`
5. `site:stats.idre.ucla.edu "statareg_self_assessment_answers4.htm" archive`

세 번째 검색은 [statsmodels issue 808](https://github.com/statsmodels/statsmodels/issues/808)을 반환했다. 일반 웹 열람에는 댓글이 생략되어 [공개 GitHub comments API](https://api.github.com/repos/statsmodels/statsmodels/issues/808/comments)에서 comment `17410423`을 직접 읽었다. jseabold는 2013-05-03T18:28:55Z에 원 ats URL을 제시하며 이 자료를 regression plots notebook에 사용했다고 진술한다. 이는 실제 소비 목적의 오래된 흔적이다. 당시 URL의 접근 성공과 발행판의 문장 동일성을 입증하지는 않는다. 원문 동일성의 첫 재개 자료는 UCLA의 날짜 있는 발행 snapshot 또는 공식 이관/판 기록이다.

## 처음 기대를 반박한 관측

- 영속적으로 보이는 릴리스 안내가 항상 exact 판 본문으로 이동하지 않는다. Python 3.11.1 릴리스 페이지의 실제 Online Documentation href는 `/3.11/`이며 현재 3.11.18로 열린다. exact 릴리스 주소와 별칭을 구분해야 한다.
- 오래된 수치를 정확히 보존하면 항상 현재 분석에도 유익하다는 결론은 French의 직접 읽은 값 차이로 제한된다. 그러나 소비 시간 의도를 모르는 상태에서 무조건 교체를 정답으로 만드는 것 역시 근거가 없다. 원출력의 해당 행 재현과 현재 수정 계열 사용의 조건부 결론을 나눴다.
- 옛판 전용 L이 있으면 실제 소비판까지 복원된다는 결론은 세 사례 모두 성립하지 않는다. 당대 후보판의 공개본문은 확인했지만 소비자가 본 판은 특정되지 않는다. French의 마지막 출력 범위는 선택한 보관 ZIP과 다르다는 반증도 있다.
- 고장 난 원 URL을 공식 현 보관 페이지로 교체해도 X를 역사 원문으로 만들 수 없다. UCLA는 현재 설명이 적절해 보여도 과거판 동일성의 증거가 없다.
- 선택된 Python/NumPy 정의는 옛판과 현판이 같아 C 목적에는 L/X가 실질적 정보를 더하지 않을 수 있다. 이는 실제 카드 결과를 아직 관측한 것이 아니며, 후속 판독에서 확인해야 한다.

이 자연 표본에서는 원 B가 이미 판 전용 주소인 예가 선택되지 않았다. 또한 동일 URL이 두 시점 모두 HTTP 200이면서 절 의미가 달라졌다는 엄격한 관측은 없다. French의 발행자 변경 공지는 변화를 설명하지만 과거 같은 index URL 본문을 직접 확보하지 못했기 때문이다. 이 두 반례를 이미 확보했다고 보고하지 않는다.

## 산입·가림·후속 사용

`sources.jsonl` 45행 중 기본 최소수 산입은 고유 소비 문서 4와 대상 저작 4다. 같은 대상의 옛판·현판·배포 소스는 한 저작으로 묶었다. 별도 릴리스/변경 공지는 보조 근거로 두었고, 자연층의 임의 공지를 정정우선층 4공지 정원으로 중복 산입하지 않았다. 실패 및 후보 링크 스캔은 최소수에서 제외했다.

원문 전체를 저장하지 않았다. X는 각각 7·6단어 또는 짧은 수치 행이며 UCLA는 결측이다. source ledger의 `verified_fact`는 직접 본 사실의 한국어 요약이고 `claim_mode=author_statement`는 저자 진술을 뜻한다. 조건부 행동 기준은 직접 사실에 사전 판정 규칙을 적용한 연구자 해석이다. 원장 생성 시각과 실제 fetch 시각은 `checked_utc_basis`로 구분했다.

출처 작성자는 원판·현판·기준을 모두 보았다. 루트 또는 같은 모델 계열의 후속 판독을 외부 독립 가림 실험이라고 할 수 없다. 카드의 추가 URL/판명은 B 원문에 넣지 않아야 하며, 역사 과업의 실제 소비판과 재구성판을 혼합하면 안 된다. 이 파일의 진단 URL은 카드에서 접근 허용된 URL이 아니다. 각 과업의 실제 2회 예산 판독은 별도로 수행해야 한다.

검산 명령은 `python -B docs/workstreams/research/AF-RES-043/collection/natural/build_records.py`이다. 출력은 4사례, 50프레임행, 45출처행, 소비4/대상4, 실제 소비판 확인0, 재구성 옛절 확인3, UCLA 완전비교 미충족이다. 이 명령은 공개 웹을 재조회하거나 카드 판독을 수행하지 않는다.
