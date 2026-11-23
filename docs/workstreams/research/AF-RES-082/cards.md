# AF-RES-082 — 사용자에게 보여 줄 짧은 답 여섯 자리

여섯 자리는 고정 모집 결과다. A의 링크1개/B의 링크2개는 **시작 안내 링크**의 수다. 근거용 링크나 독자가 읽을 공개 사이트 URL은 별도다. 실제 소비자의 채택은 사후 사실이며, 연구자가 아래 대안을 새로 배포하지 않았다.

## P1 · bandersnatch 7.0.1 — A 조건부 우선

이 문서는 기존 Sphinx 설정을 유지해 [Read the Docs 시작 안내](https://docs.readthedocs.com/platform/stable/tutorial/)로 진행할 수 있습니다. 선택한 소스와 문서 의존을 연결하고, 빌드 출력이 공개될 판을 활성화한 뒤 목표 URL을 확인하세요. Read the Docs가 생성과 호스팅을 함께 맡지만 프로젝트의 설정은 필요합니다.

판이 정해지지 않았다면 한 가지만 확인합니다: **계속 갱신되는 latest 주소가 필요한가요, 7.0.1에 고정된 주소가 필요한가요?** 전자는 기존 latest 운영을 이어가면 됩니다. 후자는 별도 버전 활성화·게시와 최종 URL 검증이 필요합니다. 현재 latest는8.2.0이고 named7.0.1은404이므로 지금 그 주소를 옛판의 완성된 배포라고 안내할 수 없습니다.

근거: PY-P1-README·RTD·RAWLOG·VERSION·LATEST. 선택 SHA의 latest run30720077 생성 성공과 현재 URL은 별개 관측이다. C2는 미확인. [결과 표1–3](RESULT.md).

## P2 · build 1.3.0 — A 조건부 우선, 도메인 책임 명시

[Read the Docs 시작 안내](https://docs.readthedocs.com/platform/stable/tutorial/)에서 기존 custom Sphinx 명령과 `docs` 의존을 연결하세요. 결과 HTML은 RTD가 수집하는 출력 디렉터리에 있어야 하고, `build.pypa.io`를 쓸 때에는 도메인과 RTD 프로젝트 권한이 필요합니다.

판이 정해지지 않았다면 **moving stable이면 충분한가요, 1.3.0을 계속 열 수 있어야 하나요?** 전자는 기존 root/stable 경로를 사용할 수 있습니다. 후자는 고정 버전을 활성화하거나 별도 보존 경로를 마련해야 합니다. 현재 root는1.6.1이고 named1.3.0은404입니다. Pages로 옮길 경우에는 별도 대안으로 Sphinx의 완전한 HTML 트리와 옛 도메인의 처리 조건을 함께 설계해야 합니다.

근거: PY-P2-README·RTD·RAWLOG·ROOT, PY-INC-DOMAIN/PR/DIFF. 당시1.3.0 소스가 stable에서 성공한 사실은 현재1.3.0 주소를 보증하지 않는다. 실제 시간·청구는 미확인.

## P3 · cibuildwheel v3.3.0 — A와 기존 1.x 경로 보존

[Read the Docs 시작 안내](https://docs.readthedocs.com/platform/stable/tutorial/)를 쓰되, 이 프로젝트의 native MkDocs 설정·plugin과 stable/선택판/1.x 경로를 함께 유지하세요. README가 지원 종료 Python 이용자를1.x 문서로 보내므로, 이 경로 보존은 이미 확인된 요구입니다. 새 사이트의 옵션 심층링크도 실제 HTML에서 확인해야 합니다.

사전에 비교한 Sphinx+Pages 두 링크만으로는 MkDocs 매크로·nav·theme와 구판 경로의 대응이 확인되지 않아 보류합니다. MkDocs+Pages는 별도 대안으로 검토할 수 있지만, 구판 디렉터리와 alias까지 포함한 HTML 트리를 건네야 합니다. **새 요청이 1.x를 버려도 된다고 명시할 때만** 단일 사이트로 단순화할 수 있습니다. 원 프로젝트 요청에는 그 단순화를 적용하지 않습니다.

근거: README L5·44·53·140, PY-P3-MKDOCS·RAWLOG·TAG-OPTIONS·LEGACYDATA, ROOT-P3-STABLE-ENABLE. 현재 두 계열은 열리지만2025 당시 동시 공개의 독립 기록은 미확인이다. 원 B를 사후 B′로 바꿔 성공 처리하지 않는다.

## R1 · archive v1.1.12 — B, 완성 HTML이 있으면 A도 가능

패키지 원본부터 시작한다면 [pkgdown 생성 안내](https://pkgdown.r-lib.org/reference/build_site.html)와 [GitHub Pages 게시 원본 안내](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)를 함께 사용하세요. 패키지·man·README에서 만든 HTML 트리 전체를 `gh-pages`에 전달하고, Pages가 그 원본을 게시하도록 연결해야 합니다. 이 프로젝트의 `deploy_to_branch()`는 생성과 branch push를 한 함수 안에서 합니다.

한 가지만 확인하면 시작점이 정해집니다: **지금 준비된 것이 R 패키지 원본인가요, 게시 가능한 HTML/branch인가요?** 원본이면 pkgdown 생성부터, 완성 HTML이면 Pages 게시 설정부터 진행합니다. root가 현재1.1.14이므로1.1.12 고정 보존까지 필요하면 별도 판 경로를 확인해야 합니다.

근거: R-016, R-P001–R-P010, R-P029–R-P035. 생성 commit45e0d9eb는 확인했지만 역사적 Pages 성공 상태는 미확인. 함수 이름만으로 서비스 활성화와 독자 접근까지 완료됐다고 판단하지 않는다.

## R2 · asciicast v2.3.1 — B, root/dev 목적 구분

[pkgdown 생성 안내](https://pkgdown.r-lib.org/reference/build_site.html)에서 완전한 `docs` HTML을 만든 뒤 [GitHub Pages 게시 원본 안내](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)에 맞는 branch로 전달하세요. 실제 프로젝트는 JamesIves action으로 `docs→gh-pages`를 수행하므로 branch·쓰기 권한·기존 디렉터리 유지 조건을 함께 확인해야 합니다. 이미 HTML과 branch가 완성돼 있다면 Pages 링크 하나가 다음 행동을 안내할 수 있습니다.

대상만 확인하면 됩니다: **정식판 문서인가요, 개발판 문서인가요?** 정식판은root, 개발판은`/dev/`입니다. 두 경우 모두 기본 생성·게시 구성은 같고 목적 경로가 달라집니다. 임의의 옛판을 고정하려면 이 두 경로만으로 충분한지는 별도 확인해야 합니다.

근거: R-023, R-P011–R-P019, R-P033, R-P036. 현재 정식2.3.1의 index·article은 과거 생성물과 각각 동일하고 dev는2.3.1.9000이다. 전체 사이트 보존이나 역사적 Pages 성공 상태까지 확인한 것은 아니다.

## R3 · bench v1.1.4 — B, 정식 사이트 재게시도 명시

[pkgdown 생성 안내](https://pkgdown.r-lib.org/reference/build_site.html)와 [GitHub Pages 게시 원본 안내](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)를 함께 사용하세요. `docs`의 HTML과 정적 파일을 `gh-pages`에 전달하고, 정식판과 개발판의 경로를 유지해야 합니다. 코드 판 번호가 같아도 정식 사이트의 내용을 고쳤다면 그 사이트를 다시 게시해야 할 수 있습니다.

한 필드는 **정식판을 바꾸려는가, 개발판을 바꾸려는가**입니다. 전자는root와 정식 소스/ref의 재게시를, 후자는`/dev/`와 개발 소스를 확인합니다. 기본 선택은 두 경우 모두 B이며, 이미 생성물이 준비되어 있다면 A의 Pages 안내만으로 이어갈 수 있습니다.

근거: R-043, R-P020–R-P028, R-P034, R-P037–R-P038. 현재1.1.4 index·reference 두 파일은 과거 생성물과 같고 dev는1.1.4.9000이다. 유지관리자의 재게시 체크리스트를 실제 실행 런이나 옛판 영구 보존 약속으로 대신하지 않는다.
