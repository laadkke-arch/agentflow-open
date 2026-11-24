# 순위 공개 전 판독

판독자와 카드 작성자는 같은 Codex Cloud 작업자다. 카드·요구·판독 파일은 서로 다른 커밋에 봉인했다. 이 파일을 커밋할 때까지 자연 표본에 대한 A·B·C 후보와 순위를 생성한 횟수는 0이다. 역할 분리의 산출물 근거는 Git 부모 이력과 세 지문이다. 별도의 판독자나 독립 인간 검토는 없었다.

두 필수조건에 대해 해당 기능이 제공하는 입력·조작·출력을 대조했다. 목적·객체가 다른 기능은 확인된 충돌로 두고, 하나의 가까운 동작만 지지하면 일부로 표시했다. 명칭만 같은 동작을 지지로 올리지 않았다. `truth.csv`의 144행은 각 판의 근거 식별자와 위치를 보관한다. `unknown`은 그 기능의 지정 범위에 대한 유보이며 파일이나 제품 전체에서의 부재를 뜻하지 않는다.

- Q-PA에서 문서 목록은 두 판 모두 기능 단위 직접 지지다. 사용자 가이드의 Document List 지정, classifier→`add_nested_tags`→`Document.tags`, bulk `modify_tags`가 잇는다. 자동 여부가 별도 조인 키가 아니며 확인된 관리자/편집 권한을 전제로 한다. 브라우저의 태그 드롭다운이 원래 이슈처럼 미선택 상태인지와 실제 재현은 미확인이다.
- Q-MK의 문서·테마 기능은 생성 페이지까지 지원한다. 요청한 복사/컨텍스트 메뉴 제한을 해당 장에서 확인하지 못했다. 브라우저 기능의 강제 보안이나 사이트 전체 부재로 해석하지 않는다.
- Q-GD에서 코어의 WGS84 병행 수명 관리와 정보 CLI의 CRS 출력은 범위가 다르다. 공간 참조의 진단 출력은 일부다. 스레드 안전성의 원래 장애 재현이나 동시 실행은 미확인이다.
- Q-DU의 Appender는 이미 존재하는 테이블로 row를 버퍼링하는 API다. 해당 판독 절에 중첩 CHECK 평가와 참조 열 바인딩 근거가 부족하다. SQL ANY/ALL의 ARRAY 감싸기는 별도 기능이다.

## 별칭과 기능 동일성

MARC 400 계열 변형 이름과 500 계열 별도 표목 사이의 see-also는 서로 다른 관계다. NDL은 Carroll 표목에 Dodgson과 일본어 변형들을 함께 두면서 저작을 개별로 찾을 수 있게 한다. Oregon의 원 소장처 안내는 Alice Sheldon이 두 필명에 서로 다른 발표 용도를 두었다고 기록한다. 저작 귀속을 찾는 요청이 키워드에서 같은 실인물로 모이는 것과 해당 필명으로 발표된 자료만 정확히 찾는 것은 다르다. 모든 이명을 확정 동일 표목 또는 저작 ID로 쓰면 후자의 검색 결과를 틀리게 합친다는 반례다. 실제 소장처에서 잘못 병합했다는 관측은 없다. SKOS의 closeMatch는 검색 가능한 관계이고 전이성을 부여하지 않으며, PREMIS는 보존 객체 식별과 이벤트를 구분한다. [MARC tracing](https://www.loc.gov/marc/authority/adtracing.html) · [NDL 표목 00435403](https://id.ndl.go.jp/auth/ndlna/00435403) · [Oregon Coll 455](https://archiveswest.orbiscascade.org/ark:/80444/xv02319) · [SKOS §10](https://www.w3.org/TR/skos-reference/#mapping) · [PREMIS 3.0](https://loc.gov/standards/premis/v3/premis-hierarchical-3-0.html)

ELF의 같은 C 심벌 명칭은 런타임 동등성을 결정하지 않는다. GNU ld는 동일 이름을 여러 버전 노드에 묶고 실행 파일은 필요한 버전 노드를 기록한다. glibc 2.13의 복사 순서 변화에서 겹치는 메모리에서 우연히 작동하던 앱이 깨졌고 2.14는 옛 바이너리를 위한 버전 심벌을 뒀다. x86-64 소스에서 새 memcpy의 GLIBC_2_14 결합을 확인했다. 겹침은 C/POSIX memcpy 계약의 지원 조건 밖이었다. Debian SONAME 유지와 심벌별 최소 판은 함수 의미·ABI·배포 범위를 따로 보존하는 추가 대조다. [GNU ld VERSION](https://sourceware.org/binutils/docs/ld/VERSION.html) · [Linux memcpy Caveats](https://man7.org/linux/man-pages/man3/memcpy.3.html#CAVEATS) · [glibc memcpy 소스](https://raw.githubusercontent.com/bminor/glibc/master/sysdeps/x86_64/multiarch/memcpy.c) · [Debian Shared libraries](https://www.debian.org/doc/debian-policy/ch-sharedlibs.html#the-symbols-system)

두 대조에서 가져올 최소 구조는 별칭·대체 경로를 조회용으로 기록하되, 근거 판과 적용 대상의 자리에는 표목/의미/런타임 경계를 남기는 것이다. 사이트 주소·표시 이름이 재사용될 때 목적별 호환이 계속되는지는 별도의 증거로 확인한다.
