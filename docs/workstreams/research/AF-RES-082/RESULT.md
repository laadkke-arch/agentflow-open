# AF-RES-082 — 문서 사이트의 한 링크와 생성·게시 두 링크

## 표1. 여섯 자리의 원래 요구와 실제 책임

| 사례ID·원순번 | 실제 목적 | 필수조건 1·2와 발화 위치 | 당시 판·URL | 빌드·게시 책임자 | 근거의 한계 |
|---|---|---|---|---|---|
| P1 · pypa 5 · bandersnatch | 패키지 미러 운영자가 사용 문서를 읽음 | C1: README의 문서 진입 안내. [고정 README][p1-readme] L4·18·99. C2: 미확인 | 7.0.1, `7a9e6510…`; [en/latest][p1-site] | 프로젝트가 Sphinx 설정·의존을 제공, Read the Docs(RTD)가 생성·호스팅 | 선택 SHA의 성공 run30720077은 latest. 현재 latest는 8.2.0, named 7.0.1은 비활성/404. 옛판 영구 보존 약속은 발견하지 못함 |
| P2 · pypa 9 · build | Python 빌드 도구의 전체 사용설명 제공 | C1: [고정 README][p2-readme] L7·13·30–31의 문서 안내. C2: 미확인 | 1.3.0, `60e8752f…`; [build.pypa.io][p2-site] | 프로젝트 custom commands가 uv·Sphinx를 실행, RTD가 출력 수집·호스팅; DNS·계정 권한은 별도 담당 | 같은 SHA의 stable29061794/latest29061621 성공. 현재 root→stable은 1.6.1, named 1.3.0은 비활성/404. 현재 HTML을 2025 배포로 합치지 않음 |
| P3 · pypa 10 · cibuildwheel | 현재 지원 Python과 지원 종료 Python 이용자 모두에게 맞는 문서 안내 | C1: [고정 README][p3-readme] L5 stable, L44·140 options/#enable. C2: L53은 Python2 등 이용자를 1.x 문서로 안내 | v3.3.0, `63fd63b3…`; [stable][p3-site], [1.x][p3-old]; 현재 [v3.3.0][p3-tag-site]도 확인 | 프로젝트 native MkDocs 명령·plugin·nav; RTD가 생성·호스팅·판 라우팅 | tag 성공 두 run과 현재 세 경로를 확인. 2025-11-12 당시 현재판·1.x의 동시 공개 기록은 미확인. 1.x는 patch 불변 주소가 아님 |
| R1 · r-lib 4 · archive | R 패키지 사용·함수 문서 제공 | C1: [고정 DESCRIPTION][r1-desc] L18의 사이트 URL. C2: README·NEWS·DESCRIPTION에서 미확인 | v1.1.12, `a4c6ec37…`; [archive.r-lib.org][r1-site] | GitHub Actions의 pkgdown `deploy_to_branch()`가 생성+branch push; GitHub Pages가 serving | 선택 SHA→생성 HTML `45e0d9eb…` 연결. deployment 객체2328795124는 있으나 성공 상태 미확인. 현재 root는1.1.14 |
| R2 · r-lib 5 · asciicast | 터미널 녹화 패키지의 안내·예제 제공 | C1: [고정 DESCRIPTION][r2-desc] L19의 사이트 URL. C2: 미확인 | v2.3.1, `f992b26f…`; [asciicast.r-lib.org][r2-site] | pkgdown→`docs`→JamesIves v4.4.1→`gh-pages`; Pages serving | 생성 HTML `92fecbc0…`의 index·article이 현재 응답과 각각 바이트 동일. 역사적 Pages 성공 상태·전체 사이트 보존은 미확인 |
| R3 · r-lib 9 · bench | 벤치마크 패키지의 안내·함수 문서 제공 | C1: [고정 DESCRIPTION][r3-desc] L14의 사이트 URL. C2: 미확인. 사후 upkeep#151은 운영 작업 기록이며 새 독자 약속으로 넣지 않음 | v1.1.4, `45c72b2d…`; [bench.r-lib.org][r3-site] | pkgdown→`docs`→JamesIves v4.5.0→`gh-pages`; Pages serving | 생성 HTML `b352fa49…`의 index·reference가 현재 응답과 각각 바이트 동일. 당시 최종 Pages 상태·연속 가용성은 미확인 |

## 표2. 동결한 A/B와 두 번의 판독, 이후 배포 검증

아래 “2문서”는 사례별 논리 판독이다. 12안×2=24회이며, 서로 다른 공식 문서는6개·최초 HTTP6회·사례 간 재사용18회였다. 모든 최초 링크·사전 판정은 사후 배포 자료를 열기 전에 커밋했다.

| 사례ID | A 또는 B | 사용자에게 줄 링크 | 열어 본 절·열람 수 | 중간 산출물·필수 설정 | 두 조건의 같은 배포 근거 | 반례·미확인 |
|---|---|---|---|---|---|---|
| P1 | A | [RTD 시작][rtd] | Import / first build / versioning + [config v2][rtd-config]의 jobs·commands·Sphinx. 2문서 | RTD 내부 HTML 트리; conf·문서 의존·출력 수집·활성 버전 | C2가 없어 평가 불가. 선택 SHA의 Sphinx8.2.3 HTML 생성 성공은 직접 확인 | 한 링크가 설정을 제거하지 않음. current latest≠7.0.1 |
| P1 | B | [Sphinx][sphinx] + [Pages 게시 원본][pages] | CLI source/output / -b·-M + branch·Actions 구분. 2문서 | 완전한 HTML·정적 파일 트리→선택한 Pages 게시 원본. base path·권한·`.nojekyll` 검토 | 연구자 대안은 배포하지 않음. 당시 실제 경로는 RTD | GitHub의 검사 출력 `docs/html`과 RTD `_readthedocs/html`을 같은 게시 경로로 합치지 않음 |
| P2 | A | [RTD 시작][rtd] | 위 RTD 두 원문 재사용. 2문서 | custom Sphinx 명령→`$READTHEDOCS_OUTPUT/html`; docs group·도메인·버전 활성화 | C2 평가 불가. stable29061794의 실제 Sphinx7.4.7 실행·exit0 확인 | 서비스 채택 후에도 사용자 명령이 실패할 수 있음: 별도 사건1031의 docstrfmt exit1 |
| P2 | B | [Sphinx][sphinx] + [Pages 게시 원본][pages] | 위 CLI·게시 원본 절 재사용. 2문서 | `docs` 입력+확장 의존→HTML 전체; Pages 권한·custom domain·옛 주소 처리 | 조건부 기술 대안. 실제 채택/종단 실험 없음 | DNS·RTD owner·원문 URL 수정은 서로 다른 작업. 링크2개로 이전 권한을 확보했다고 볼 수 없음 |
| P3 | A | [RTD 시작][rtd] | 위 RTD 원문 중 MkDocs·commands·versioning 포함. 2문서 | native MkDocs/plugin 출력→RTD HTML; stable/tag/1.x 라우트 유지 | 현재 stable 심층링크·v3.3.0·1.x 접근 확인. 역사적 두 조건 동시 성립은 **확인0/1·미확인1** | 두 성공 run 및 파일 Last-Modified가 달라 하나의 산출물 manifest로 합칠 수 없음 |
| P3 | B | [Sphinx][sphinx] + [Pages 게시 원본][pages] | 위 CLI·게시 원본 절. 2문서 | 사전 Sphinx 안에 MkDocs 매크로·nav·theme·구판 경로의 대응 계약이 없음 | 원 B 보류. 사후 MkDocs+Pages 대안은 별도 B′이며 검증하지 않음 | Markdown이라서 Sphinx가 불가능하다는 기각은 하지 않음. native 동등성이 미확인인 것 |
| R1 | A | [Pages 게시 원본][pages] | branch/Actions + [custom workflow][pages-workflow]의 artifact·권한·environment. 2문서 | 이미 생성된 HTML 또는 적절한 빌드 workflow 필요. 서비스는 R 원본을 자동 해석하지 않음 | C2 평가 불가. tag→생성 branch는 관측, Pages success는 미확인 | artifact 방식 설명을 실제 `gh-pages` push 방식과 섞으면 다른 배포를 합친 것 |
| R1 | B | [pkgdown build_site][pkgdown] + [Pages 게시 원본][pages] | build components·destination + branch/Actions. 2문서 | 패키지·man·README→HTML→`gh-pages`; 실제 함수는 생성+push를 내부 수행 | 실제 책임 구성이 이 설명과 연결됨. 다만 당시 serving 상태는 미확인 | `deploy_to_branch()`가 Pages 활성화·HTTP 재확인까지 맡지는 않음 |
| R2 | A | [Pages 게시 원본][pages] | R1-A 원문 재사용. 2문서 | HTML/branch 준비 완료면 다음 게시 설정 안내로 충분 | C2 평가 불가. 현재 대표 HTML2개는 옛 생성물과 같음 | 현재 byte 일치는 역사 serving 성공·전체 보존의 대체 증거가 아님 |
| R2 | B | [pkgdown build_site][pkgdown] + [Pages 게시 원본][pages] | build/destination + publishing source. 2문서 | `docs` 전체→JamesIves→`gh-pages`; contents:write, clean:false, release/dev 정책 | 실제 구성·생성 커밋·현재 대표 파일은 연결. 과거 Pages 최종 성공은 미확인 | clean:false가 모든 옛판을 불변으로 보존한다는 보장은 없음 |
| R3 | A | [Pages 게시 원본][pages] | R1-A 원문 재사용. 2문서 | 이미 준비된 HTML/branch가 전제. 공개 설정·권한을 확인 | C2 평가 불가. 현재 대표 HTML2개는 옛 생성물과 같음 | released-site 재게시 필요성은 운영 기록. 게시 완료 런으로 채점하지 않음 |
| R3 | B | [pkgdown build_site][pkgdown] + [Pages 게시 원본][pages] | build/destination + publishing source. 2문서 | `docs` 전체→JamesIves→`gh-pages`; trigger/ref·권한·URL·dev 디렉터리 | 실제 생성·전달 경로 확인. source→HTML은 근거 있고 serving 기록은 공석 | 현재 root와 dev가 서로 다른 판. 한쪽 성공을 다른 쪽 보존 성공으로 합치지 않음 |

## 표3. 실제 경로에서 권고할 다음 행동으로

| 실제 공개 경로·증거 수준 | 권고할 선택·사용 조건 | 두 선택이 같거나 갈린 이유 | 되물을 필드 | 유지 비용·분모 |
|---|---|---|---|---|
| P1: RTD/Sphinx. 선택 SHA 생성 성공+현재 latest. 옛 named URL404 | **A 조건부 우선**. 선택 소스·conf·의존을 유지하고 목표 버전을 활성화. 옛판 고정 요구라면 먼저 필드 확인 | A가 생성·게시를 함께 맡을 수 있음. B도 완전한 HTML 전달 조건이면 가능하나 실제 채택 아님 | `필요한 주소 = moving latest / 7.0.1 고정` → 기존 latest 운영 / 별도 판 활성화·게시 및 URL 검증 | A1/B2링크. 실제 경로 설정 블록5, 생성·호스팅 사업자1, 소스 저장까지2. 남은 수작업 수·시간·실제 요금 미확인 |
| P2: RTD/Sphinx custom command. stable 생성 성공+현재1.6.1; 옛 도메인 redirect | **A 조건부 우선**. custom command·출력·도메인 권한 확인. B는 승인된 도메인 이전이 필요한 별도 대안 | 두 안 모두 생성/게시를 구성할 수 있으나 DNS·권한·옛 URL 보존은 링크 수로 해결되지 않음 | `독자 대상 = moving stable / 1.3.0 고정` → 현 alias / 활성 고정판 또는 별도 아카이브 | 설정 블록5. 도메인 사건의 사람 작업5종류를 확인했지만 각 시간·과금은 미확인. 현재 alias HTML 지문 짝1/1 |
| P3: RTD/MkDocs. 현재 tag·stable·1.x, legacy source SHA 연결 | **A+기존 두 경로 보존 조건**. 원 B는 보류. B′=MkDocs+Pages는 사후 대안 | 서비스 하나는 native generator를 지원. 원 Sphinx B는 현재 입력/경로 계약이 비어 있음 | 원 프로젝트의 `1.x 유지 = 예`는 이미 답이 있음. 새 요구에서만 아니오라면 단일 사이트, 예라면 버전 병존/이전 경로 검증 | 설정 블록5. 조건2개1자리 중 당시 동시 공개0확인/1미확인. 현재 두 문서 진입+심층링크는 관측 |
| R1: pkgdown 함수→gh-pages→Pages. 생성물 commit 있으나 현재 root는 새 판 | **B 조건부 우선**, HTML/branch가 이미 준비되었다면 A도 다음 행동으로 가능 | 한 함수에 생성과 push가 있어도 Pages 설정·serving은 남음. A/B 차이는 준비된 입력과 설명 범위 | `현재 준비물 = 패키지 원본 / 게시 가능한 HTML` → pkgdown부터 / Pages 설정부터 | 실제 경로 설정 블록6+외부 Pages/UI·DNS 미확인1. 공급자 GitHub1. 전체시간·실제권한·청구 미확인 |
| R2: pkgdown→JamesIves→gh-pages→Pages. 대표 HTML2개 현재 동일 | **B 조건부 우선**, 생성물 준비시 A도 가능 | 원본에서 게시까지 설명하려면 HTML 전달 계약이 필요. 실제 운영은 GitHub 한 공급자 안 두 단계 | `대상 = 정식판 / 개발판` → root / dev; 옛판 고정이면 별도 보존 경로 확인 | 설정6+미확인1. 비교 파일2/2 byte동일, 전체 사이트 분모 아님. 수동 승인·실제 비용 미확인 |
| R3: 같은 생성/branch 경로, 대표 HTML2개 동일; 재게시 운영 기록 | **B 조건부 우선**, 기존 완성 HTML이면 A도 가능 | 같은 숫자 판의 사이트 수정도 재게시를 요구할 수 있음. A/B 링크 개수만으로 이 행동을 정하지 못함 | `대상 = 정식판 / 개발판` → root / dev; 정식 사이트 수정은 release 재게시 경로 | 설정6+미확인1. 비교 파일2/2 동일. upkeep 완료 발화1건은 런 성공1건으로 세지 않음 |

## 분모와 완료 수준

| 집계 대상 | 분자 / 원분모 또는 실제 수 | 해석 |
|---|---:|---|
| 고정 공개·비포크 모집틀 | pypa58 + r-lib164 = **222행** | 이름·언어·원순번·포함/제외·미검사 이유를 FRAME.csv에 보존 |
| 이름순 검사 | pypa10행 중 기간 적격5, r-lib9행 중 적격7 | 각각 최대15 적격 후보 한도 안에서 첫3개로 중단. 후순위48/155개 미검사 유지 |
| 선정·소비 프로젝트 출판 계보 | **6/6** | 소속·언어·서비스·요구량·성공에 따른 사후 교체0 |
| 원래 독자 조건 | **확인7/12슬롯**, C2 미확인5 | 두 독립 조건이 있는 자리 **1/6** |
| 원 소유자의 실제 생성/게시 경로 관측 | **6/6** | 구성·생성 이력·현재 사이트의 결합. 종단 성공6건이라는 뜻 아님 |
| 선택 소스의 역사적 생성 | Python 성공 로그 **3/3**; R 생성 git HTML **3/3** | 두 증거 종류를 CI 성공6/6으로 합치지 않음 |
| 역사적 R Pages 최종 상태 | 객체 **1/3**, success **확인0/3·미확인3** | 조회 공백은 실패가 아님 |
| 두 조건의 같은 역사적 출판 상태 | **확인0/1·미확인1** | C2가 없는5자리는 평가 불가. R만은0/0 산출 불가 |
| 현재 약속한 공개 진입점 | **6/6** | 현재HTTP·판독 관측. 과거 연속 가용성 아님 |
| 현재 선정 판을 식별하는 공개 HTML | **3/6**: P3·R2·R3 | 조사한 named/entry URL과 판 식별에 한정. 모든 가능한 아카이브를 소진한 결과 아님 |
| R 역사 생성물과 현재 대표 HTML 일치 | **2/3자리, 4/6파일** | index+leaf1개씩. 전체 asset·JS·수년 연속성 미검사 |
| A의 조건부 범위 | source→site 담당 가능 **3/6**; 완성HTML 전제 **3/6** | 어느 안도 무설정·무조건 종단 성공으로 승인하지 않음 |
| B의 기술 계약 | native 입력에 조건부 대응 **5/6**, 대응 계약 미확인/보류 **1/6** | P3 Sphinx안. 불가능 판정0/6; 실험으로 승인한 대안0/12 |
| 사전 예산 | **12안×2=24 논리 판독, 고유6문서, HTTP6회, 재사용18회** | 별도 독립 사용자24명·실제 클릭24회가 아님. 사후 검증은 이 예산 밖 |
| 원자료 | **전체201행 / 보수적29독립계보** | 201행에는 모집 메타데이터·반복 읽기도 있음. 29계보 산입에서는 모집 메타데이터를 제외하고 공급자 같은 설명서·다른 판, 이슈+PR, DOI별칭·반복 읽기를 합침. 실패·스니펫은 시도 원장에만 기록 |
| 실패/무변경 보존 최소 충족 집합 | **7계보 / 최소4** | 독립 문서 사건4 + build1031 실제 실패1 + R2/R3 대표HTML 무변경2. 추가 사건을 섞어 비율을 키우지 않음 |
| 다른 분야 공개 발행 원기록 | **8개 / 최소4**, 필수 두 쌍은4원기록·2계보 | 원장20행·9계보와 별도 분모. PDF 표현·DOI alias를 추가 사건으로 세지 않음 |
| “생성·게시 모두 성공했으나 옛 URL 오류”의 공개 런 쌍 | **확인0/검토 독립 문서사건4** | 관련 사용자 보고는 있으나 두 성공 런이 없어 강한 반례 자리는 공석 |
| A/B 실사용 성공률·시간/비용 비교 | **0/0, 산출 불가** | 대안 배포·사용자 시험·실제 작업시간·사업자 청구 데이터가 없음 |

**연구 판정: PARTIAL.** 모집·필수 자료량·사전 안내 비교·여섯 카드의 산출은 완료했다. 다만 필수 검증 중 당시 두 조건의 동시 공개, R의 역사적 최종 Pages 성공, 두 단계 성공 뒤 옛 URL만 잘못된 강한 반례는 공개 근거로 확정하지 못했다. 이 공백을 성공 또는 실패로 채우지 않고 재개 입력을 남긴다. 판독 결과가 지지하는 것은 **서비스가 해당 원본의 생성·목표 판·공개 경로를 담당하면 한 링크로 시작할 수 있고, 선택한 서비스가 원본 생성을 맡지 않아 외부에서 생성물을 준비·전달해야 하면 두 부품과 교환 조건을 설명해야 한다**는 조건부 판단이다. 완성 HTML이 이미 있으면 게시 서비스 한 링크가 다음 행동에 충분할 수도 있다.

## Q1–Q2. 독자의 약속과 공급자의 기능을 구별하기

원 프로젝트가 공개한 주소는 독자를 어디로 보낸다는 증거다. 이것만으로 “모든 과거 태그를 영구 보존”이라는 두 번째 약속을 만들 수 없다. P1/P2의 latest·stable과 R의 root는 실제로 움직이거나 새 판을 돌려준다. 반면 P3는 현재 독자와 지원 종료 Python 이용자를 명시적으로 갈라 1.x로 안내한다. 이 차이 때문에 C2가 필요한 분모는 여섯이 아니라 하나다. 원문의 역할·판·발화 위치와 공석은 requirements.csv에 남겼다. [PY-P1-README, PY-P2-README, PY-P3-README, R-016, R-023, R-043]

RTD의 시작 안내는 소스 저장소 연결, 첫 빌드, 공개 문서 보기, 여러 버전 운영을 한 서비스 경계 안에서 설명한다. 그러나 프로젝트의 Python·Sphinx/MkDocs·확장 의존·입출력을 대신 정하지 않는다. P2/P3는 custom commands를 택했으며, v2 문서는 이때 기본 build jobs를 대신해 사용자가 출력 디렉터리를 채워야 한다고 설명한다. 당시 선택 태그의 코드와 로그로 native generator와 실제 실행판을 다시 확인했다. P1은 Sphinx8.2.3, P2는7.4.7, P3는MkDocs1.6.1 계열 설정이다. 첫 설치에 보이는 버전이나 현재 설명서 판을 실제 역사 실행판으로 삼지 않았다. [ROOT-RTD-START, ROOT-RTD-CONFIG, PY-P1-RAWLOG, PY-P2-RAWLOG, PY-P3-RTD, PY-P3-RAWLOG]

R의 원래 경로는 소스 패키지→생성 HTML→git branch→Pages였다. archive의 pkgdown v2.1.1 구현은 함수 하나에서 생성과 push를 연속 수행한다. asciicast/bench의 `build_site_github_pages()`는 HTML과 필요한 Pages용 파일을 만들고, 그 뒤 JamesIves가 branch에 올린다. “deploy”라는 이름, 또는 action의 성공이라는 말이 최종 URL의 판과 모든 옛 링크까지 검증했다는 뜻은 아니다. 고정판 코드·README의 책임 범위를 대조했다. [R-P029–R-P037; 세부는 streams/r/RESPONSIBILITY.md]

공식 안내와 실제 경로의 시간도 다르다. 사전 판독에는 조사일의 RTD·Pages·Sphinx·pkgdown 안내를 썼고, 역사 검증에는 소비자의 고정 SHA와 확인 가능한 당시 generator/action 판을 썼다. 공개 서비스의 현재 약관·UI·제한을 2024–2025 당시와 같았다고 가정하지 않는다.

## Q3. 두 번 읽고 확인할 수 있는 것과 없는 것

먼저 A/B의 링크와 순서를 고정한 커밋은 `8ba1d686d4c7e50067f9d52bc753a4e02708cd42`, 예산 판정을 봉인한 커밋은 `5f881c7094bf30be13069554b412a00c5b01f7c0`이다. 상세 절·읽은 UTC·재사용·최초 취득 배분은 paths.csv와 evidence/budget-seal.json에 있다. 네트워크는 독립 요청을 병렬 취득했으므로 `allocated_first_fetches`는 사례순 회계 배분이며 실제 시간순 클릭을 뜻하지 않는다. 사전 README의 RTD 배지 등 노출도 SCOPE에 기록했다.

2문서만으로 A/Python은 “서비스가 빌드와 공개를 함께 담당할 수 있다”, B/Python은 “소스와 설정에서 만든 HTML 트리를 Pages에 넘겨야 한다”까지 읽을 수 있었다. A/R은 “완성 HTML 또는 사용자 workflow가 있어야 한다”, B/R은 “pkgdown 결과의 destination과 게시 원본을 맞춰야 한다”까지다. 각 소비자의 설치 의존, 도메인 권한, 활성 판, 당시 성공 런과 HTML은 이후 별도 검증 대상이었다. 안내의 충분성과 배포의 사실을 같은 점수로 만들지 않았다.

기각한 **연구자 조립 오류**는 branch 게시 설정과 artifact 게시 설정을 한 경로로 합치는 것이다. `docs→gh-pages`+contents:write를 채택한 실제 R workflow에 `upload-pages-artifact`·`deploy-pages`의 artifact ID, pages:write, id-token, environment를 붙여 한 당시 배포라고 서술하면 다른 전달 방식을 섞게 된다. 각 방식은 독립 대안으로 검토할 수 있지만 해당 원 프로젝트가 둘을 함께 썼다는 증거는 없다. 이는 원 유지관리자의 설정 오류를 발견했다는 주장이 아니다. [ROOT-PAGES-SOURCE, ROOT-PAGES-WORKFLOW, R-P036, R-P037]

P3는 사전안의 한계가 드러난 자리다. native MkDocs의 매크로·plugin·nav·theme와 1.x 경로를 Sphinx로 옮기는 계약을 원 B가 제공하지 않았다. MyST 등으로 Markdown을 다룰 가능성을 배제하지 않으면서도, 대응 없는 상태를 “기술적으로 가능하므로 충분”으로 승인하지 않는다. 뒤늦게 발견한 MkDocs `gh-deploy`나 RTD 실제 채택을 사전 B의 성공으로 소급하지 않는다. [PY-P3-MKDOCS, PY-MKDOCS-161]

## Q4. 생성 성공, 게시 상태, 현재 HTML을 연결하는 한계

Python의 named tag가 비활성이라는 관측에서 멈췄다면 P1/P2를 잘못 판정했을 것이다. 선택 SHA로 조회한 전체 결과는 P1 latest30720077, P2 stable29061794/latest29061621의 성공을 보여 줬다. raw log까지 읽어 HTML 생성 명령과 exit0을 확인했다. named URL404는 현재 그 이름의 사이트를 못 연다는 관측이며, 같은 소스가 당시 latest/stable로 생성되지 않았다는 반증이 아니다. [PY-P1-SHABUILDS, PY-P2-SHABUILDS, PY-P1-RAWLOG, PY-P2-RAWLOG]

P3의 현재 v3.3.0 changelog 첫 판과 options anchor, 1.x의 changelog와 served metadata는 요청한 두 계열의 내용을 식별한다. 특히 1.x의 served commit은2021 성공 build14073318과 연결된다. 그러나 두 서로 다른 판이2025-11-12의 같은 출판 상태에서 함께 제공됐는지는 당시 아카이브가 있어야 한다. 두 판은 원래 서로 다른 빌드일 수 있으므로 “같은 run ID가 아니다”만으로 실패라고 판단하지도 않는다. 현재 같은 조사 회차에 둘이 열린다는 더 좁은 사실만 확인했다. [PY-P3-TAG-CHANGELOG, PY-P3-TAG-OPTIONS, PY-P3-LEGACYRUN, PY-P3-LEGACYDATA, ROOT-P3-STABLE-ENABLE]

P3의 run30298916 API 시간과 raw command 시간 사이에는 약5분 차이가 있고, 현재 root와 leaf의 Last-Modified도 다르다. run30298914도 같은 소스에 있다. 대기시간이나 두 빌드의 수집 의미를 추정해 덮지 않고 파일별 artifact manifest가 없는 상태로 남겼다. 따라서 현재 파일의 checksum을 특정 하나의 과거 게시 트랜잭션에 연결하지 않는다. [PY-P3-TAGBUILDS, PY-P3-RAWLOG; deployments.jsonl]

R 세 태그에서는 생성 커밋 메시지의 입력 SHA, HTML의 판 표기, 내부 leaf 링크를 대조했다. R2/R3의 두 HTML씩은 당시 git blob과 현재 HTTP 응답 SHA-256이 같다. 이것은 단순한 URL 생존보다 강한 근거지만 전체 사이트, 외부 JS, 이미지, 중간 기간의 가용성을 증명하지 않는다. R1의 옛 생성물도 git에 있으나 현재 root는 다른 판이므로 “복구할 수 있는 파일”과 “독자가 현재 원 URL에서 받을 판”은 갈린다. [R-P003–R-P028]

GitHub 공개 API의 한도 소진 후 R1 deployment2328795124의 statuses를 못 읽었고, connector는 그 endpoint를 지원하지 않았다. Actions 조회0건·combined statuses 빈 배열은 당시 실행 부재의 증명이 아니다. 정확한 재개 URL, 입력/출력 SHA와 제한 응답은 streams/r/attempts.jsonl 및 RESPONSIBILITY.md에 있다. 생성 성공으로 게시 성공을 대신하지 않는 것이078에서 인수한 핵심이다.

## Q5. 작은 변경이 안내를 뒤집은 실제 경계

| 경계와 원자료 | 실제 관측 | 안내에 반영할 변화 | 관측하지 못한 것 |
|---|---|---|---|
| 하위 경로: [mike#175](https://github.com/jimporter/mike/issues/175), INC01 | 사용자는 제품별 `/uem/<version>`·`/iot/<version>`을 원했고, site_url/Nginx 시도 뒤 `--prefix` 안내로 작동했다고 보고 | 사이트 루트 변경에는 생성 대상 prefix·기존 branch 파일 이동을 함께 명시 | 실제 런·원 사이트·옛 링크 복원 확인 없음 |
| alias 표현: [mike#188](https://github.com/jimporter/mike/issues/188), INC02 | mike2의 alias symlink 전환 후 일반 URL은 안 열리고 버전 URL은 열린다는 보고. rollback/redirect 방식의 해결 발화 | 같은 HTML이어도 호스트의 symlink 처리와 redirect 파일 계약을 확인 | 비공개 프로젝트라 생성·게시 성공 런 쌍은 없음. 과거 버전 파일 삭제라고 확대하지 않음 |
| 태그 권한: [deploy-pages#76](https://github.com/actions/deploy-pages/issues/76), INC03 | 태그 환경 보호규칙 거부, 이후 담당자의 정책 변경 설명과 사용자 성공 확인 | artifact 존재와 게시 권한·environment 정책을 따로 확인 | 역사적 우회책을 현재 보안 설정 권고로 재사용하지 않음. 실제 job log 없음 |
| 관리형 루트: [RTD#12181](https://github.com/readthedocs/readthedocs.org/issues/12181), INC04–05 | 하위 문서는 있어도 루트 프로젝트 활성/빌드 판이 없어 robots.txt404라는 운영자 진단; 현재 같은 URL200 | 하위 프로젝트 성공으로 root URL·공통 파일 제공을 추정하지 않음 | robots 정책은 접근 통제·내용 삭제가 아님. 당시 생성/게시 런과 불변 지문 없음 |
| moving URL와 old series: P1/P2, [cibuildwheel#657](https://github.com/pypa/cibuildwheel/issues/657) | named tag404와 같은 SHA latest/stable 성공 공존; 1.x 문서 유지 결정 및 현재 legacy source 연결 | 고정판을 원하는지, 현재 alias인지, old series가 필요한지에 따라 활성 판/라우팅 확인 | 1.x를 immutable patch archive로 승격하지 않음 |
| 같은 판 재게시: [bench#151](https://github.com/r-lib/bench/issues/151), R-P038 | 유지관리자가 필요시 released-site 재게시를 별도 작업으로 표시. root/dev 실제 판이 다름 | 코드 버전 숫자만 보지 말고 어느 ref·release/dev 경로를 재게시할지 결정 | 체크리스트를 success 런으로 세지 않음 |
| 사용자 빌드 실패: [build#1031](https://github.com/pypa/build/issues/1031), PY-INC-STUCK-LOG | RTD32209794에서 docstrfmt가 CHANGELOG 제목 계층 오류로 exit1, Sphinx 생성 전 중단 | 한 서비스도 사용자 사전 명령의 성공에 의존. 첫 실패 위치부터 복구 |2026 사건을2024–2025 여섯 자리의 실패율에 넣지 않음 |

한 서비스로 시작할 수 있는 사례와, 한 도구 안에 두 단계가 들어 있는 사례를 모두 유지했다. RTD는 생성·호스팅을 맡고, archive의 pkgdown 함수 및 공식 MkDocs1.6.1 `gh-deploy`는 생성+push를 내부 수행한다. 반대로 단계를 둘로 나눠도 root·alias·권한이 맞지 않으면 독자가 원하는 경로를 얻지 못할 수 있다. 이 방향의 실제 보고는 찾았지만 **두 공개 성공 런 뒤 옛 링크가 틀렸다는 가장 강한 형태의 사건은 확보하지 못했다.** “가능한 고장” 설명과 “관측한 실행 실패”를 구분한다.

## Q6. 확인 비용은 누구의 무엇을 세었는가

설정 블록은 YAML 줄 수가 아니라 책임을 확인할 단위다. Python은 저장소/서비스 연결, 환경/의존, generator 입출력, 게시 target/권한, URL/판의5블록이다. R은 trigger/ref, 환경/의존, 생성/출력, branch 전달, token/write, URL/release-dev의6블록과 공개되지 않은 Pages/UI·DNS1블록이다. 원 프로젝트에는 많은 설정이 이미 존재하므로 이를 “새로 남은 작업5개/7개”라고 세지 않는다. 신규 요청자의 환경·권한·완성물 유무가 없으면 실제 잔여 설정 개수는 미확인이다.

| 관점 | 이번에 실제로 센 것 | 관측한 수·범위 | 비어 있는 비용 |
|---|---|---|---|
| 설계자/사용자 | 시작 링크, 책임 블록, 외부 교환물 | A1/B2링크; 실제 경로5 또는6+미확인1블록. A/RTD는 서비스 밖 HTML 전달0, B는 완전한 HTML 트리1종 전달 | 설정 완료까지 걸리는 시간, 사용자의 기존 권한, 실제 새 설정 수 |
| 릴리스 담당자 | 실행 입력·출력, 게시 주체, 공개 사람 작업 | P2 domain 사건에서 동의·권한 추가·DNS·RTD 도메인 입력·원문 링크 수정5종류. R3 재게시 체크리스트1건 | 각 작업의 소요시간·수동 승인 필요 여부·실제 청구액 |
| 독자/검토자 | URL과 판·대표 파일을 추가 확인 | R은 역사/current 각 index+leaf의6파일쌍 중4쌍 동일. P3는 stable deep link·tag·legacy의 판별 읽기 | 전 사이트의 테스트시간·연속 가용성·전체 링크 수와 실패율 |

운영 공급자의 분모도 고정했다. Python 실제 생성·호스팅 사업자는RTD1곳이며 소스 저장GitHub까지 포함하면 SaaS조직2곳이다. R의 생성 실행Actions와 호스팅Pages는GitHub1곳이다. Sphinx·MkDocs·pkgdown·JamesIves는 구현/도구이며 별도 호스팅 사업자로 세지 않았다. 다운로드 저장소·CDN 등 전체 공급망의 사업자 수는 조사하지 않았다. 따라서 링크1→2가 공급자1→2로 증가한다는 결론은 성립하지 않는다.

현재 [RTD 가격](https://about.readthedocs.com/pricing/)은 공개 OSS의 Community 무료 경로를 안내하고, [현재 자원 문서](https://docs.readthedocs.com/platform/stable/builds.html#build-resources)는 제한과 증액 요청 가능성을 명시한다. [Pages 제한](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)은 공개 저장소의 무료 이용 범위, 용도와 자원 제한을 설명한다. 이 공개 지원 범위는 특정 프로젝트의 실제 플랜·특별 할당·관리자 권한·SLA·결제 내역을 입증하지 않는다. 현재 조건을2024–2025 계약으로 소급하지 않았다. 자세한 현재 수치는 streams/costs/NOTES.md에 분리했다. [COST-RTD-PRICE, COST-RTD-LIMIT, COST-PAGES-LIMIT, COST-PAGES-SCOPE]

예산 판독의 HTTP6회는 완전하게 계수했다. 이후 전체 탐색에는 검색 배치·connector·웹 retrieval이 섞여 origin HTTP 수가 노출되지 않는 요청이 있으므로 **사후 전체 HTTP 총수는 산출 불가**다. 성공 원문/실패/검색/재열람을 기록했으나 attempts 행 수를 전부 실제 HTTP 횟수로 바꾸지 않았다. 빌드 duration도 사람의 시간이나 과금시간으로 환산하지 않는다.

## Q7. 다른 분야의 판 관계에서 옮길 수 있는 것

| 분야·공식 정책·실제 쌍 | 직접 읽은 원기록 | 확인된 관계와 반례 | 웹 배포에 옮길 수 있는 검증 항목 |
|---|---|---|---|
| 학술: PLOS 정정 정책·Crossmark 정책 + PLOS 실제 정정 | [원논문0301852](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0301852), [정정0316774](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0316774), 공지의 S1/S2 PDF | 2024-12-17 재발행·12-30 공지. 구판/정정판 PDF를 실제 다운로드해 읽었고 둘은 원논문 DOI/원발행일을 공유하지만 bytes·텍스트가 다름 | 식별자, 판 관계 공지, 실제 옛 파일, 현재 접근을 따로 검사. DOI하나를 불변 bytes로 읽지 않음 |
| 소프트웨어 보관: Zenodo 버전/파일 정책 + matplotlib 실제 두 판 | [v3.1.0 record2893252](https://zenodo.org/records/2893252), [v3.2.0 record3695547](https://zenodo.org/records/3695547), concept592536 | 판별 DOI·파일 manifest는 다르고 concept DOI는 최신 판을 가리킴. 현재 concept은v3.11.2. ZIP은 다운로드/실행하지 않았음 | moving 별칭과 고정판 식별자를 구분하고 실제 파일 제공·지문을 함께 확인 |
| 주소는 달라도 같은 판 | DOI2893252와 이전 `/record/2893252` 주소 | 둘 다 현재 `/records/2893252`로 가며 최종 HTML SHA-256이 같음. P2의 옛/새 도메인도 같은 현재 HTML로 연결 | URL 문자열 차이만으로 판 차이·마이그레이션 실패를 결론내리지 않음 |
| 식별자만 남는 반례 | Zenodo tombstone [22705920](https://doi.org/10.5281/zenodo.22705920), API record17295496 | DOI·인용 정보는 남지만 의도된410 tombstone에 옛 파일은 제공되지 않음. 단순 요청 실패가 아니라 원문 철회 기록을 읽음 | 영구 ID의 지속과 독자의 옛 내용 접근은 별도 조건. 서비스 장애와 정책상 철회를 구분 |

학술 필수 쌍의 S1/S2는 각각18쪽이며 SHA-256은 `e641e5c2…`와 `167af964…`다. 실제 내용 차이가 있다는 확인과 기계적 diff 수가 곧 실질 정정 수는 아니라는 한계를 함께 남겼다. Zenodo의 ZIP MD5는 발행자가 공개한 manifest 값으로서 연구자가 내려받아 계산한 값이 아니다. 전문·메타데이터·발행자 선언의 근거 수준을 섞지 않았다. [PUB07–10, PUB12–16; streams/publication/pdf-comparison.json]

추가로 eLife의 실제 그림 정정 공지와 PLOS의 다른 재발행 공지도 읽었다. eLife 원논문 전체/그림 bytes에는 접근하지 못했고, 다른 PLOS 공지에서 구판 PDF 쌍 링크가 없다는 사실만으로 인터넷 전체에서 구판이 사라졌다고 말하지 않는다. Zenodo의 현재 minor-correction 정책도 특정 matplotlib 파일이 실제로 바뀌었다는 증거가 아니다. [PUB03, PUB11, PUB20]

외부 분야에서 가져올 것은 **판 식별자↔발행 관계↔실제 파일↔현재 접근**의 검사 항목이다. DOI 정책이 RTD나 Pages의 route·artifact·게시 권한을 승인하는 근거가 될 수는 없다. 이번 비교에서 외부 분야 자료로 비어 있는 소비자 C2나 Pages success를 채운 곳은 없다.

## Q8. 짧은 답에 반드시 남길 행동 정보

실제 사용자용 여섯 답은 cards.md에 있다. 각 답에는 한 링크/두 링크의 선택, 입력판과 전달 산출물, 바뀌면 행동이 달라지는 한 필드, 아직 승인하지 못한 부분을 넣었다. P1/P2는 moving URL 대 옛판 고정, R1은 원본 대 완성 HTML, R2/R3는 정식판 대 개발판의 실제 두 값을 대비했다. P3의 1.x 보존은 원문이 이미 요구하므로 질문으로 다시 떠넘기지 않는다. 새 목적에서 이를 버릴 수 있다고 정할 때만 단일 사이트 대안을 별도로 다룬다.

같은 선택을 유지하는 결과도 유효하다. R2/R3에서 정식판/개발판을 바꾸어도 기본 선택은 B로 같고 목적 경로만 root/dev로 달라진다. P1/P2에서도 옛판 활성화를 지원하는 같은 서비스에 머물 수 있으므로 질문의 답이 반드시 공급자 변경을 낳는 것은 아니다. 다음 행동이 달라지는지를 확인하며, 억지로 A/B 승패를 만든 것이 아니다.

## 재현·파일·검사

- 모집/원요구/비교: SCOPE.md, FRAME.csv, requirements.csv, prelinks.csv, paths.csv. 사전 파일·열의 봉인 SHA와 비교하는 검산은 `tools/validate_research.py --final`이다.
- 직접 읽은 원문: sources.jsonl의 자료ID·원저작/사건 계보·URL·판·절/행·UTC·관측·한계·지지/반증. 총행과 독립계보는 evidence/lineage-index.json에서 분리한다.
- 출판 연결·실패·지문: deployments.jsonl, streams/python/RESPONSIBILITY.md, streams/r/RESPONSIBILITY.md, streams/publication/NOTES.md, streams/incidents/NOTES.md. 현재 응답 지문과 역사 git/PDF 지문은 다른 필드다.
- 실제 검산과 수용 대상은 SELF_CHECK.md, evidence/validation.json 및 인계 전 workbench 검사 기록에 남긴다. 소비 프로젝트 빌드/게시, SQLite·PNG·ZIP 실험, 계정 권한 변경은 실행하지 않았다.

## 가장 중요한 불일치·약점과 판단을 바꿀 다음 조사 — 정확히 세 건

1. **요구 분모가 작고 조직의 과거 소속이 고정되지 않았다.** C2는1/6만 확인했으며 현재 조직 목록을 사용했다. **다음 조사:** 같은 여섯 태그를 대상으로 당시 문서 정책·릴리스 토론·저장소 이전 기록을 입력으로 읽는다. 관측 목표는 독립적인 옛판/시점 약속의 정확한 발화와 당시 소속이다. 새로운 약속이 나오면 평가 가능 분모를 갱신하되 표본을 교체하지 않는다.
2. **생성과 역사적 공개의 연결이 비었다.** R Pages success3건, P3의2025 동시 접근, 일부 RTD 파일↔run 결합이 미확인이다. **다음 조사:** archive deployment2328795124/statuses와 R2/R3 출력 SHA, RTD30298914/30298916의 artifact manifest 및2025-11-12 전후 stable/1.x capture를 입력으로 조회한다. 성공 state·당시 URL·파일 지문·동시 판 식별이 연결되면 종단 판정을 바꾼다. 빈 상태/404만으로 실패 판정하지 않는다.
3. **안내 비교는 동일 조사자의 조건부 판독이며 강한 반례 런 쌍이 없다.** 자료를 재사용했고 P3 원 B는 native generator 대응이 비어 있다. **다음 조사:** 이미 동결한12안·동일 태그·동일2문서 예산을 독립 판독자에게 주고, 별도로 공개 저장소의 build-success·publish-success 런 쌍과 잘못된 옛 URL 응답을 수집한다. 원요구/산출물/route를 잘못 합치는지와 실제 반증을 관측한 뒤 안내 충분성 판단을 갱신한다. 현재 실사용 성공률·시간 비교는 산출하지 않는다.

[rtd]: https://docs.readthedocs.com/platform/stable/tutorial/
[rtd-config]: https://docs.readthedocs.com/platform/stable/config-file/v2.html
[sphinx]: https://www.sphinx-doc.org/en/master/man/sphinx-build.html
[pages]: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
[pages-workflow]: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
[pkgdown]: https://pkgdown.r-lib.org/reference/build_site.html
[p1-readme]: https://github.com/pypa/bandersnatch/blob/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/README.md
[p2-readme]: https://github.com/pypa/build/blob/60e8752f69178d2b2c3563e9c8fa17aa6e11b12c/README.md
[p3-readme]: https://github.com/pypa/cibuildwheel/blob/63fd63b352a9a8bdcc24791c9dbee952ee9a8abc/README.md
[r1-desc]: https://github.com/r-lib/archive/blob/a4c6ec37fc8737a189ca7ec7095ec0161888f9e8/DESCRIPTION#L18
[r2-desc]: https://github.com/r-lib/asciicast/blob/f992b26f3cb30c799fbb95f6148852d8ae8a7f18/DESCRIPTION#L19
[r3-desc]: https://github.com/r-lib/bench/blob/45c72b2dcbba2b181d24c175ebb90ff8ed5eccad/DESCRIPTION#L14
[p1-site]: https://bandersnatch.readthedocs.io/en/latest/
[p2-site]: https://build.pypa.io/
[p3-site]: https://cibuildwheel.pypa.io/en/stable/
[p3-old]: https://cibuildwheel.pypa.io/en/1.x/
[p3-tag-site]: https://cibuildwheel.pypa.io/en/v3.3.0/
[r1-site]: https://archive.r-lib.org/
[r2-site]: https://asciicast.r-lib.org/
[r3-site]: https://bench.r-lib.org/
