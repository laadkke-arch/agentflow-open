# Python 세 자리: 사후 배포 검증과 책임 경계

사전 모집·요구와 A/B 안내는 부모가 봉인한 뒤에 아래 자료를 읽었다. 이 문서는 사전 추천 점수를 갱신하지 않는다. 원자료의 URL·UTC·지문·한계는 `sources.jsonl`, 실제 원격 요청은 `http-receipts.jsonl`과 `attempts.jsonl`, 배포 연결은 `deployments.jsonl`에 있다. 직접 실행한 것은 읽기·원장 정리뿐이며 세 소비 프로젝트의 문서를 새로 빌드하거나 배포하지 않았다.

## 결과와 분모를 먼저

| 관측 | Python 분모 | 해석 |
|---|---:|---|
| 고정 모집틀에서 선택 완료 | 3/3 | pypa 원순번 5·9·10, 나머지 교체 없음 |
| 독립적인 독자 조건 두 개 확인 | 1/3 | P3만 현재판 안내와 Python2 등의 구판 안내가 별도로 존재. P1·P2 조건2 미확인 |
| 원 소유자의 실제 생성·호스팅 경로 관측 | 3/3 | 모두 RTD가 생성과 호스팅에 관여. Sphinx 2, MkDocs 1 |
| 선택 SHA의 역사적 생성 성공 | 3/3 | P1 latest, P2 latest/stable, P3 tag에서 실제 로그 확인 |
| 당시 생성물과 게시 HTML 전체 바이트의 결합 | 0/3 확인, 3/3 미확인 | 독립 배포 manifest나 당시 HTML checksum 미확보. 실패율을 뜻하지 않음 |
| 조건 두 개의 2025년 동시 공존 | 0/1 확인, 1/1 미확인 | P3 구판의 2021 성공과 현재 공존은 확인. 2025 시점 동시 접근의 연속 기록은 없음 |
| 약속한 공개 진입점 현재 열림 | 3/3 | P1 latest, P2 root→stable, P3 stable 및1.x |
| 선택된 2025 판을 현재 식별 가능한 HTML로 열기 | 1/3 | P3 v3.3.0. P1 latest=8.2.0, P2 stable=1.6.1이고 명명 tag URL은404 |
| 연구자가 사전 A/B를 실제 배포 | 0/6안 | 수행하지 않은 실험이다. 승률이나 시간 비교 불가 |

현재 선택판 미접근 2건을 계약 위반으로 세지 않는다. 두 프로젝트에서 immutable tag site 보존 약속이 확인되지 않았기 때문이다. `0/3 확인`과 `3건 실패`는 다르다.

## P1 bandersnatch 7.0.1

태그 SHA `7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74`의 [RTD 설정](https://github.com/pypa/bandersnatch/blob/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/.readthedocs.yml)은 Ubuntu24.04/Python3.12, `docs/conf.py`, Sphinx HTML, 경고 실패, PDF/HTMLZIP/EPUB, 프로젝트와 문서 의존 설치를 정한다. `docs/conf.py`는 설치된 패키지의 버전을 쓰며 CLI·API 문서와 MyST/Furo를 구성한다. `requirements_docs.txt`는 Sphinx8.2.3을 고정한다. 이는 사용자 소유 코드·의존·설정이고 RTD가 대신 작성한 것이 아니다.

[공개 로그30720077](https://app.readthedocs.org/api/v2/build/30720077.txt)의 헤더는 선택 SHA, latest, 2025-12-16, 성공을 연결한다. L645–720은 Sphinx8.2.3 HTML 명령의 exit0과 `_readthedocs/html` 생성을 보여 준다. 처음 설치된 Sphinx9.0.4가 뒤에서 pinned8.2.3으로 교체되어 실제 실행되므로 초기 다운로드 문자열을 실행판으로 오독하지 않는다. PDF와 EPUB 생성도 관측되지만 README의 독자 보존 조건2로 승격하지 않는다.

현재 RTD의 7.0.1 named version은 inactive/built=false이고 해당 경로는404다. 그러나 SHA 필터의 전체 결과(count1,nextnull)에 위 latest 성공이 있다. **명명 tag가 비활성이라는 이유로 그 source가 배포되지 않았다고 판정하면 틀린다.** 현재 [latest HTML](https://bandersnatch.readthedocs.io/en/latest/)은 8.2.0으로 바뀌었다. 7.0.1 당시 제공된 HTML 바이트나 그때 독자 접근을 입증할 별도 아카이브는 없다.

GitHub `doc_build` workflow와 tox는 HTML/linkcheck를 `docs/html`에 생성한다. 이 검사용 경로와 RTD가 수집하는 `_readthedocs/html`을 하나의 게시 워크플로로 합치지 않는다. A는 기존 문서 소스·conf·의존과 moving latest 요구를 유지할 때 한 RTD 시작 링크로 진입 가능하다. B의 Sphinx→Pages는 HTML 디렉터리 전체와 상대 링크/정적 파일을 넘기고 Pages 게시 권한·경로를 별도로 맞춰야 하는 연구자 대안이며 실제 채택 기록은 없다.

## P2 build 1.3.0

태그 SHA `60e8752f69178d2b2c3563e9c8fa17aa6e11b12c`의 [RTD 설정](https://github.com/pypa/build/blob/60e8752f69178d2b2c3563e9c8fa17aa6e11b12c/.readthedocs.yml)은 custom commands를 사용한다. Ubuntu22.04/Python3.12에서 uv latest를 설치한 뒤 docs dependency group으로 Sphinx를 실행하고 `$READTHEDOCS_OUTPUT/html`에 쓴다. 태그 의존 제약은 `sphinx~=7.0`이지만 [stable 로그29061794](https://app.readthedocs.org/api/v2/build/29061794.txt) L94에서 **실제로 실행된 Sphinx7.4.7**을 확인했다. 해당 고정판 공식 CLI 원문을 별도로 읽어 출력 디렉터리 계약을 대조했다.

SHA 필터 전체 결과(count2,nextnull)는 2025-08-01 stable29061794와 latest29061621의 성공을 보여 준다. named1.3.0은 inactive/404라도 이 실제 경로를 놓쳐서는 안 된다. 다만 현재 [root](https://build.pypa.io/)는 stable로 이동하며 1.6.1을 제공한다. 선택 SHA의 생성과 현재1.6.1 HTML을 같은 배포 증거로 합치지 않았다.

실제 [도메인 변경 사건715](https://github.com/pypa/build/issues/715)의 댓글은 저장소 유지관리자 동의, DNS 담당자, 당시 한 명뿐이던 RTD owner, 추가 권한 부여, RTD 도메인 입력과 링크 수정의 역할을 드러낸다. [PR717](https://github.com/pypa/build/pull/717)은 2024-01-17에 README·패키지 URL 변경을 병합했다. 현재 옛 `pypa-build.readthedocs.io/en/stable/`는 `build.pypa.io/en/stable/`로 redirect하며 최종 HTML 지문은 독립적으로 연 root의 지문과 일치한다. 다른 주소가 반드시 다른 판을 뜻하지 않는 현재 반례다. 2024 이후 중단 없는 redirect 지속은 입증하지 않았다.

A의 링크 수는1이지만 custom command와 도메인 권한은 남는다. B에는 Sphinx7.4.7을 포함한 원 프로젝트 확장 의존, `docs` 입력, HTML 디렉터리, Pages 권한·라우트·기존 custom domain 이전을 명시해야 한다. DNS 소유와 RTD 권한을 가지고 있다고 연구자에게 추정하지 않는다.

## P3 cibuildwheel v3.3.0과1.x

태그 SHA `63fd63b352a9a8bdcc24791c9dbee952ee9a8abc`는 [RTD 설정](https://github.com/pypa/cibuildwheel/blob/63fd63b352a9a8bdcc24791c9dbee952ee9a8abc/.readthedocs.yml)의 사용자 명령으로 MkDocs를 실행한다. Python3.14를 uv가 관리하며 strict build가 `_readthedocs/html`을 출력한다. 태그는 MkDocs1.6.1을 고정하지만 여러 plugin 의존은 범위 지정이다. `mkdocs.yml`의 theme override, include-markdown, docs/main 매크로, custom delimiter, nav와 경로를 함께 보존해야 한다. Markdown이라는 이유만으로 Sphinx를 배제하지 않는다. **사전 B의 Sphinx 안내가 이 실제 설정·매크로·라우트에 대응하는 변환을 제공하지 않은 점**이 확인해야 할 경계다.

[로그30298916](https://app.readthedocs.org/api/v2/build/30298916.txt)는 선택 SHA, MkDocs 명령 exit0, HTML 생성 완료를 보여 준다. 같은 tag의 다른 성공 run30298914도 있다. 현재 [tag HTML](https://cibuildwheel.pypa.io/en/v3.3.0/), [options/#enable](https://cibuildwheel.pypa.io/en/v3.3.0/options/#enable), [changelog](https://cibuildwheel.pypa.io/en/v3.3.0/changelog/)은 각각 열리며 anchor와 첫 v3.3.0 heading을 확인했다. 단, API의 created/finished는19:28:06/19:28:22, raw command 시각은19:33:07–19:33:20이다. root Last-Modified19:33:23과 options/changelog19:28:18은 서로 다르다. 두 run·대기시간·필드 의미가 관계할 수 있지만 artifact manifest 없이 단일 게시시각이나 파일별 run을 확정하지 않는다.

조건2는 Python2 등의 사용자를1.x로 보내는 태그 README의 실제 안내다. [2021년2.0 계획657](https://github.com/pypa/cibuildwheel/issues/657)은 1.x 브랜치·문서와 구판 링크를 별도로 유지하기로 한 결정을 기록한다. 1.x 공개 build history14개를 마지막 페이지까지 읽었으며 마지막 성공은2021-06-22의14073318이다. 현재 [1.x의 served metadata](https://cibuildwheel.pypa.io/en/1.x/readthedocs-data.js)는 그 run과 같은 commit `da84127892e79fab70b0ca4a4d22a23c1db53116`을 담고, [legacy changelog](https://cibuildwheel.pypa.io/en/1.x/changelog/)는v1.12.0부터 시작한다. 이는 현재 오래된 콘텐츠가 남아 있다는 강한 연결이고, 2025년 두 사이트가 동시에 열렸다는 독립 아카이브는 아니다. 1.x를 immutable patch판으로 해석하지 않는다.

A는 기존 RTD 안에 현재와1.x 버전을 함께 유지하고 native MkDocs 명령을 보존하는 조건에서 가능하다. B를 쓰려면 native MkDocs+Pages라는 **사후 대안**으로 구별하고 구판 디렉터리·route·custom domain·상대 URL을 함께 보존하는 교환 계약이 필요하다. MkDocs1.6.1의 [공식 배포 문서](https://github.com/mkdocs/mkdocs/blob/1.6.1/docs/user-guide/deploying-your-docs.md)는 `gh-deploy` 한 명령에 생성과 push가 이미 들어 있음을 밝힌다. 이는 도구 내부 단계2개가 사용자 링크2개를 강제하지 않는 반례지만, cibuildwheel의1.x 보존까지 자동 승인하지 않는다.

## 설정 블록·공급자·사람의 비용

SCOPE의 단위는 YAML 필드 개수가 아닌 설정 블록이다. 세 자리마다 아래5개 경계를 열거한다. 이 수를 신규 설정5개나5단계 수작업으로 해석하지 않는다.

| 설정 블록 | P1 | P2 | P3 |
|---|---|---|---|
| 저장소/서비스 연결 | RTD가 pypa/bandersnatch를 clone한 로그 | RTD가 pypa/build를 clone한 로그 | RTD가 pypa/cibuildwheel를 clone한 로그 |
| 빌드 환경/의존 | OS·Python·requirements pin | OS·Python·uv·docs group; 실제Sphinx7.4.7 | OS·uv Python3.14·MkDocs/plugin group |
| generator 입력/출력 | conf.py, HTML와 추가형식 | 사용자 Sphinx 명령, docs→RTD HTML | 사용자 MkDocs 명령, nav/plugin→RTD HTML |
| 게시 target/권한 | RTD 프로젝트·host 관측, 현재 계정 권한 미확인 | RTD owner 추가의 역사 기록; 현재 권한 미확인 | RTD 프로젝트·host 관측, 현재 계정 권한 미확인 |
| URL/판 routing | latest 및 inactive namedtag | root/stable/custom domain/옛 domain redirect | stable/v3.3.0/1.x 및 relative deeplinks |

따라서 A는 안내1링크,5개 책임 경계, 호스팅 사업자RTD1곳이다. 소스 저장 SaaS인 GitHub까지 세면 고유 외부 SaaS조직2곳이며 generator 구현은 Sphinx 또는MkDocs1개로 별도 계산한다. B를 GitHub Actions+Pages로 설계한다면 hosting/build/source의 SaaS조직은 GitHub1곳이고 generator는 여전히 별도 구현이다. **링크 수1→2가 공급자 수1→2를 의미하지 않는다.** 연구자가 그 B를 설정하거나 서비스 권한을 받지는 않았다.

릴리스 담당자 관점에서 P2 도메인 사건은 동의, 권한 추가, DNS, RTD 도메인 설정, 원문 링크 수정이라는5종류의 사람 작업을 명시한다. 권한 추가·DNS 완료는 당사자 보고, 링크 변경은 병합diff, RTD 입력은 후속 지시와 현재 동작으로만 보인다. 각 작업의 소요시간·사업자 실제 청구는 미확인이다. 빌드 로그의 seconds를 사람 작업시간이나 과금시간으로 환산하지 않는다. 독자 관점에서는 P3의 현재판과1.x 양쪽 링크가 필요하고 P1·P2에서 구판을 요구할 경우 추가 확인이 필요하다.

## 독립 반대 근거 네 계보

1. **build stable 갱신 실패1031:** [공개 raw log32209794](https://app.readthedocs.org/api/v2/build/32209794.txt)는2026-04-10 stable에서 build1.4.3을 설치한 후 CHANGELOG 제목 수준 오류로 docstrfmt exit1이 나 Sphinx 생성 전에 중단됐음을 보여 준다. 이슈의1.4.0 잔류 보고와 함께 서비스 채택만으로 최신판 게시를 보장할 수 없음을 보인다. 2024–2025 표본 성과와 분리했다.
2. **bandersnatch theme2090/2092:**7.0.0 URL의 가독성 실패가 보고되고 Furo 교체가 병합됐다. 댓글의 개선 확인은 latest에 대한 것이므로 원래7.0.0 링크가 복구됐다고 결론내리지 않는다. 이슈+PR+댓글은 한 사건이다.
3. **build custom domain715/717:** 도메인·RTD 계정·원문 URL이 서로 다른 책임이다. 현재 옛 주소와 새 주소가 동일 HTML로 연결되며 주소 차이가 판 차이와 같지 않다. 지속 가용성은 미확인이다.
4. **cibuildwheel legacy657:** 구판 Python 지원 종료 후 별도1.x 문서 유지 결정을 현재 surviving source identity까지 연결했다. 그 branch 주소가 patch 불변성을 보장하지는 않는다.

## 바꿀 판단과 최소 후속

P1·P2에 되물을 필드는 **독자가 필요한 판이 moving latest/stable인가, 선택된 옛판 고정주소인가**다. 전자는 실제 owner 경로와 현재 공개 진입이 지지한다. 후자는 현재 namedtag404 때문에 활성화·별도버전 게시·아카이브 중 하나를 검토해야 한다. 현재 sourceSHA 역사적 생성성공만으로 후자를 승인하지 않는다.

P3의 구판 안내 요구는 이미 README에서 답을 얻었으므로 다시 묻는 비용으로 숨기지 않는다. 아직 새 목적지가 정해지지 않은 요청이라면 **기존1.x URL을 유지해야 하는가**라는 필드의 yes는 기존 RTD 병존 또는 route-preserving migration을, no는 단일 native MkDocs 사이트 구성을 허용한다. 후자는 원 프로젝트의 확인된 두 조건을 충족하는 추천으로 점수화할 수 없다.

최소 후속은 P1/P2에서 선택판의 실제 archived HTML 또는 RTD 산출물 manifest를 확보해 source SHA·출력파일 지문·당시 URL을 연결하는 일이다. P3는2025-11-12 전후 stable/tag와1.x가 함께 열리는 독립 capture가 필요하다. API와 raw command 시간 차이는 두 run의 공급자 타임필드 정의와 artifact manifest를 입력으로 조회해야 해소할 수 있다.
