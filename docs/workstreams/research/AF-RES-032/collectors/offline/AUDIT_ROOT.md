# Python·root B 결과의 별도 내부 재검

**원 바이트·해시·판 경계·산술의 확정 오류는 찾지 않았다. 시각 역할과 관측 정밀도의 설명을 보강할3항목을 남겼다.**

| 검토 범위 | 직접 재검 결과 |
|---|---|
| Python3.8.2–3.8.20 | actual tar19개, about/bugs HTML38개를 다시 읽고 archive/member SHA256 대조 통과 |
| httr1.4.1–1.4.8 | actual tar8개, api-packages HTML8개와 DESCRIPTION8개 재독 |
| 핵심 경계 | Python3.8.14→3.8.15의 query 변경, httr1.4.2→1.4.3의 domain 변경, httr1.4.6→1.4.7의 추천 폐기를 확인 |
| 산술 | Python13,480,547초(156일00:35:47), httr14,044초(3시간54분04초) 일치 |
| 중복 | httr1.4.7/1.4.8의 전체 HTML 멤버 바이트 동일. 검토한 두 sources 원장에서1.4.8 추가 산입 없음 |
| 독립성 | 원 수집자와 다른 내부 에이전트의 재판독. 기존 결론을 먼저 읽었으며 맹검·외부 사람 검토 아님 |

재검 시점의 HEAD,13개 입력 파일 SHA256, 판별 archive/member/DESCRIPTION 해시, 검사별 결과와 남은 미확인은 `audit-root.json`에 고정했다. 이 검토는 원장이나 원 결론을 수정하지 않았다. 같은 원문을 다시 읽은 것이므로 최소 고유 원문 수를 늘리지 않는다.

## 보강이 필요한3항목

| ID·영향 | 확인한 사실 | 제안 |
|---|---|---|
| AUD-ROOT-01 · 중간: 분 단위 구간의 전제 | [Python 상태 로그](https://discuss.python.org/t/github-issues-migration-status-update/14573)의 post1은 모든 시각을 UTC로 표시하고18:15에 read-only 상태를 보고한다. 사후 편집된 운영자 상태 기록이며 서버 이벤트의 초 단위 로그나 반올림/절삭 규칙은 아니다. | 156일00:34:47–00:35:47은 **표시된 분을 해당 분의 구간으로 해석했을 때의 조건부 산술**이라고 명시한다. 실제 서버 시행이 그60초 안이라는 독립 실측 경계로 표현하지 않는다. 명목 시간차 계산과 strict publication0은 유지할 수 있다. |
| AUD-ROOT-02 · 낮음: httr source 시각 역할 | [httr commit](https://github.com/r-lib/httr/commit/b6c03b6f6611a4bbca4057268ffbc1096bc11e65)을 GitHub API로 다시 읽으니 author는2022-05-03T20:23:19Z, **committer는20:25:58Z**다. 실제1.4.3 DESCRIPTION의 Date/Publication은2022-05-04 00:20:02UTC다. | 현재3시간54분04초는 정확히 **committer→CRAN Date/Publication**이다. source_edit라는 이름에 이 역할을 명시한다. DESCRIPTION의 Packaged20:41:18UTC는 별도 포장 시계이며 HTML build 시각으로 대체하지 않는다. |
| AUD-ROOT-03 · 낮음: reader 목적의 해상도 | [독자 원 게시물](https://discuss.python.org/t/status-of-documentation-bug-tracker/14957)은 문서 개선 issue를 만들려는 목적이며 live `/3/bugs.html#using-the-tracker`를 가리킨다. 봉인한 docs-query를 클릭했거나 offline3.8 도움말을 읽었다는 말은 없다. | `same_purpose:true`는 **넓은 작업 목적의 겹침**으로 한정하고 selected-link click은 미확인으로 분리한다. 기존 `same_exposure_medium:false`와 strict reader chain 제외는 적절하다. |

첫 항목은 시간값의 뺄셈 오류가 아니라 보고 시각의 정밀도를 실제 시행 시각의 엄격한 구간으로 해석할 때 필요한 전제다. 세 항목 모두 선택된 원 href나 실제 최초 새 판의 결과를 뒤집지 않는다.

## 원 바이트로 확인한 핵심 주장

### Python의 첫 새 판

[3.8.14 archive](https://docs.python.org/ftp/python/doc/3.8.14/python-3.8.14-docs-html.tar.bz2)의 `bugs.html`은 원 Roundup documentation query를 포함한다. [3.8.15 archive](https://docs.python.org/ftp/python/doc/3.8.15/python-3.8.15-docs-html.tar.bz2)는 같은 `Documentation bugs` 항목에 GitHub `is:issue is:open label:docs` query를 둔다. 주변 문서는 새 문제를 보고하고 중복 보고를 피하라는 현재 작업 문맥이므로 같은 목적의 링크 교체라는 해석이 맞다.

현재 공식 원장의 stable3.8.2–3.8.20을 모두 대조했고19개 archive의38개 선택 멤버 해시가 원장과 맞았다. 먼저 새 주소가 들어간 판이나 나중에 되돌린 판을 찾으려 했으나 이 계열에서는 찾지 못했다. **3.8.15가 처음이라는 표현은 이 검사 범위에 한정**해야 하며, 모든 major나 첫 HTTP 배포 순간이라는 표현은 허용하지 않는다. 현재 cases의 한정은 적절하다.

[Python 소스 수정](https://github.com/python/cpython/commit/246a044641388dfd5023cb4b8dbe5519cb41d943)의 author와 committer는 모두2022-09-11T18:50:47Z다. 실제 GitHub API diff가 원 query의 변경과 맞는다. 공식 제품/문서 판 날짜, archive의 Last-Modified, footer의 갱신일을 exact first-public UTC로 쓰지 않은 판단도 적절하다.

### httr의 같은 목적 교체와 추천 폐기

[1.4.2](https://cran.r-project.org/src/contrib/Archive/httr/httr_1.4.2.tar.gz)의 `httr/inst/doc/api-packages.html`은 `developer.github.com/v3/#rate-limiting`을, [1.4.3](https://cran.r-project.org/src/contrib/Archive/httr/httr_1.4.3.tar.gz)은 `docs.github.com/v3/#rate-limiting`을 포함한다. 두 판의 해당 문단은 오류 처리와 다음 요청까지 기다릴 시간을 설명한다. 주소의 host가 바뀌었으며 목적이 같은 수정이다. 실제1.4.3 DESCRIPTION의 UTC 출판 필드로 committer와 출판 날짜쌍을 연결한 근거도 맞는다.

1.4.4·1.4.5·1.4.6에서는 그 같은 문단과 새 host가 유지된다. [1.4.7](https://cran.r-project.org/src/contrib/Archive/httr/httr_1.4.7.tar.gz)에는 기존 긴 API 작성법이 없고 새 코드는 httr2를 권한다는 짧은 본문이 들어 있다. 따라서1.4.7은 같은 rate-limit 링크의 추가 수리로 세면 안 된다. 원 결과가 이를 **문서·추천의 교체**로 분리한 것은 맞다.1.4.8은 이 멤버 전체가1.4.7과 동일하므로 새 원문을 하나 더 센다면 중복이지만, 현재 원장은 그렇게 세지 않았다.

원장에는1.4.2와1.4.3 사이,1.4.6과1.4.7 사이에 다른 판이 없다.1.4.1도 직접 재독했으며2019-08-05 출판이므로2020 GitHub 공지 전의 소비자판이다.2020-07-20의1.4.2는 공지 뒤에도 옛 주소를 남겼다는 관측으로 구별할 수 있다. 다만 **2026의 target fragment 부재를2020/2022 당시의 실패로 소급할 수 없다**는 원 결과의 제한은 유지해야 한다.

### 잘못된 날짜쌍을 찾으려 한 경로

httr의2021 `Update URLs` commit도 다시 읽었다. 그 diff는 Wikipedia content-negotiation 링크의 scheme 수정이며 이번 rate-limit 사건이 아니다.2022의 맞는 patch를 선택한 원 결과를 확인했다. Python의 상태 로그에서는 read-only, migration completion, issue mapping이 서로 다른 작업이고, 현재 원장은 이들을 별도 시각으로 구분한다. 독자 post의 미리보기나 현재 `/3/` 페이지 판을2022독자의 판으로 사용하지 않은 것도 맞다.

## 검토의 한계와 다음 행동

B03 Debian PycURL은 cases의 논리·미확인 표기만 검토했다. 이 감사에서 `.deb` 원 바이트를 독립적으로 다시 열지는 않았으므로 그 멤버에 대한 별도 재검 완료라고 부르지 않는다. sparse followup, 공개 시각 미확인, 독자 실행 미확인이라는 제한 자체는 타당하다.

중복 감사는 Python followup과 root B의 두 sources 원장 범위다. 전 작업의 글로벌 합본, provisional/최종 표본이 모두 섞이지 않았는지, 다른 수집자의 동일 URL 원고까지는 이 문서가 인증하지 않는다. 첫 행동은 위3개 역할·정밀도 표현을 통합본에 명확히 하고, 수정 후 파일 SHA를 이 감사의 입력 스냅샷과 구분하는 것이다.
