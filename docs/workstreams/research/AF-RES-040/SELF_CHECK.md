# AF-RES-040 — 자체 대조와 미충족 조건

상태는 **REVIEW_READY_WITH_GAPS**다. 원장·계산 검사가 통과한다는 사실과 연구 절차·효과 판정의 충족을 분리한다. 이 파일은 같은 세션의 자체 검토이며 독립 사람 판독이 아니다. 수용 조건별 기계 판독값·파일/행·분자/분모는 [acceptance-evidence.json](evidence/acceptance-evidence.json), 최종 고정 SHA 재열람·세션 검사 결과는 [verification-receipt.json](evidence/verification-receipt.json)과 최종 HANDOFF에 연결한다. 해당 영수증이 작성되기 전에는 검사 성공을 가정하지 않는다.

## Q1. 누구의 어떤 선택을 비교했는가

- **지지:** SCOPE §1에서 두 원장, 정확한 검색어, 2020–2025 기간, 생성시각/번호 오름차순, 최초30, 프로젝트별4와 대체 원장을 고정했다. frame.csv 60행 중8선정이며 원 요청8개 본문을 공급자 자료 전에 봉인했다. G는 첫6에서2제외, S는 최초4선정이다. 원격 사전 커밋 `2ccbf7ab660d6e16dab637eea40867cbc4f83499`, 풀 커밋 `b406236564be8dc6435912912ba67e5d16c98102`.
- **원문·위치:** [GDAL #2150](https://github.com/OSGeo/gdal/issues/2150)의 재현/환경, [#2169](https://github.com/OSGeo/gdal/issues/2169)의 GetNextFeature/Expected behavior, [#2172](https://github.com/OSGeo/gdal/issues/2172)의 FlatGeoBuf·ogrinfo, [#2193](https://github.com/OSGeo/gdal/issues/2193)의 COSMO 파일·환경; [Sphinx #7019](https://github.com/sphinx-doc/sphinx/issues/7019)의 Windows 재현, [#7032](https://github.com/sphinx-doc/sphinx/issues/7032)의 개별/전역 구분, [#7054](https://github.com/sphinx-doc/sphinx/issues/7054)의 doctree-resolved·두 builder, [#7093](https://github.com/sphinx-doc/sphinx/issues/7093)의 둘째 빌드·테마 소스.
- **반증·경계:** #2172는 배포 포맷 가용성을 묻기 때문에 포함했으며 일반 의존 설치 문제 #2158·#2173과 구별했다. 요청자가 과거판 성공을 보고했다고 롤백을 승인한 것은 아니다. S2의 전역 off 거부를 그대로 보존했다.
- **미확인:** 두 프로젝트의 목적 표본이며 일반 소비자 대표성이 없다. 이름만 필요한 요청0/8, 실제 클릭·채택 미관측. 성공적인 완전 대안이 나타나는 소비자 분포까지 일반화할 수 없다.
- **자체 판정:** 8요구 봉인·원장 재현 정보는 충족. 표본의 효과 판정 범위는 제한적.

## Q2. 링크 목록은 누가 어떻게 만들었는가

- **지지:** 공급자 목차→명시된 다른 공급자→레지스트리→공식 예제 순서를 SCOPE §2에 선언했다. pool.csv는48슬롯·39실제링크·9빈칸이고 원 순서·발견 위치·판·시각·열람 상태를 보존한다. 주풀은 원격 봉인 뒤 보조 사례로 채우지 않았다. 고유 URL32와 판별 접근 키17, 중복 제거한 주풀 원문15를 별도 집계한다.
- **원문·위치:** [GDAL v3.0.1 formats_list](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/frmts/formats_list.html)의 HFA 항목과 원 관측 원장의 정확 경로, [Sphinx v2.3.1 contents](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/contents.rst)의 toctree, [builders](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/builders/index.rst#L387), [configuration](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/configuration.rst#L734-L797). 판 실패·대체 위치는 sources의 G-F/S-F 행이다.
- **반증·경계:** S는 자연 명명 항목에서 연구자가 만든 GitHub #L 링크다. S1의 builders→configuration 세부 이동은 전향 고정되지 않았다. G의 HFA 선열람과 Java의 현행색인→역사판 역추적도 완전 전향 순회가 아니다. 최초 요구의 봉인과 후보 탐색 절차의 완전성은 다른 조건이다.
- **미확인:** 다른 정당한 자연 href 순서에서 첫6과 결과가 같을지 미확인. S frozen_utc는 관측 종료시각이며 실제 파일 작성시각은 receipts-S에서 따로 기록했다.
- **자체 판정:** 같은 풀·순서 보존은 충족. 원 href 그대로·후보 본문 노출 전의 완전한 seed 순회는 **미충족**.

## Q3. 두 링크는 같은 무엇인가

- **지지:** 주소·상류·구현·부품·목적·판·역할·양방향·근거 위치를 분리했다. 실제 후보85쌍을 수동 원 판독으로 연결하고 빈슬롯이 포함된35쌍은 unknown으로 둔다. 전체120쌍이다. 같은 문서 호스트에 있는 sphinxcontrib-*는 패키지 Code 링크로 별도 상류임을 확인했다.
- **원문·위치:** [MapInfo](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/ogr/ogrsf_frmts/mitab/drv_mitab.html) L1–39·Creation Issues, [Java](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/swig/java/javadoc.java#L6863-L6878), [OGR C/C++](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/ogr/ogr_apitut.dox#L108-L129); [sphinxcontrib-htmlhelp](https://pypi.org/project/sphinxcontrib-htmlhelp/) Code/Release files, qthelp/applehelp의 같은 필드.
- **반증·경계:** 같은 MapInfo라도 새 쓰기와 갱신의 지원 범위가 다르다. Java/C++는 같은 하위 구현을 쓴다고 wrapper·버그 동등성이 입증되지 않는다. 문자열 key 일치에서 yes/no를 생성하던 초기 계산은 폐기하고 수동 근거를 사용한다.
- **미확인:** G 방향은 문서 역할 치환, S는 완전 원 요구 대체 범위다. G partial 어휘는 원 판정으로 남겼고 yes로 승격하지 않았다. 경로 간 방향 빈도 비교는 할 수 없다. M07에 규칙·편차·영향 분모를 남겼다.
- **자체 판정:** 필드·근거·원 판독 보존은 충족. **모든 방향 판단의 동일 범위·어휘는 미충족**. 실행 호환성 미확인.

## Q4. 같은 세 자리에서 무엇이 보이는가

- **지지:** views.jsonl24행은 같은6후보 순서, 최초 대표, 최초3그룹, 빈칸, 행당 직링크1·설명80자 상한·추가클릭0을 보존한다. CARDS.md가 실제 표시 필드만 렌더링한다. 보이는 카드에 숨은 원문의 근거를 더하지 않았다.
- **원문·위치:** G2 MapInfo/Java와 S1 gettext/config 쌍은 RESULT 필수 표1·2에서 실제 URL로 연결한다. 설명·길이·원 멤버는 views.jsonl `cards`, `all_groups`, `cutoff_groups`, `unfilled_pool_slots`다.
- **반증·경계:** 같은 config 문서의 다른 절은 대표 앵커를 열어도 접근 가능하다. HDF5 원문에 이미 gdalinfo 예제가 있으므로 별도 gdalinfo 카드를 숨겼다고 호출 근거를 잃었다고 세지 않았다.
- **미확인:** 서로 다른 대표의 실제 설명 문자수는 같지 않다. 스크롤·발견 비용, 화면의 실제 이용자 해석은 관측하지 않았다. K는 형제 목록만의 정보와 전원문 접근 상한을 분리하며 실제 총두클릭 실험이 아니다.
- **자체 판정:** 동일3행·원링크·상한·원순서의 재구성은 충족. **동일 실제 설명 길이 및 실제 두 클릭 관측은 미충족/미확인**.

## Q5. 해로운 합침과 이로운 중복 제거는 무엇인가

- **지지:** 전체25필수 atom 중 풀에서8개를 입증한다. A/C8개·B6개 보존, G2.A2·S1-A1 가림. 완전 답변은 각0/8, 조건부 완전 경로 분모0은 해당 없음. 요구별 짝집계와 실제 atom 집합이 결과에 먼저 온다.
- **원문·위치:** G2 Java L6863–6878, S1 MessageCatalogBuilder L386–401+gettext_location L761, G4 HDF5 L21–44·L121–123. losses.csv의 지원/미지원/병합가림/보완묶음 필드를 구분한다.
- **반증·경계:** G4는 B에서도 일반 호출 근거를 보존하며 G1도 첫 HFA 원문에3atom이 있다. G2 정확 URL 중복을 없애 C/C++ 참고를 셋째 자리에 보이게 했지만 완전 적격 대안은 아니다. 기능 중복0과 같은 원문 반복 A7/B6/C7은 다르다. B의 이질 병합48쌍도 실제 해로운 손실48건이 아니다.
- **미확인:** 완전 적격 경로가0이라 대안 회수의 비교효과를 실증하지 못했다. 17개 미지원 atom은 부재의 증명이 아니라 이 풀의 미입증이다. 실제 성공·효용은 미확인이다.
- **자체 판정:** 부정적 결과와 분모 구분·짝 집계는 충족. 완전 대안의 귀환 효과는 판정 불가.

## Q6. 타 분야의 식별 규칙은 어디서 틀리는가

- **지지:** 도서관5·음악11개 운영 원문·구체 레코드를 직접 읽었다. IFLA/LoC 층, Yale 한 URL 두 판, MusicBrainz 같은 MBID의 다른 mix 표기와 같은 work의 별도 원녹음/remix를 비교했다. 제공자·소비자·편집자의 관점을 나눴다.
- **원문·위치:** [IFLA LRM](https://www.ifla.org/wp-content/uploads/2019/05/assets/cataloguing/frbr-lrm/ifla-lrm-august-2017_rev201712.pdf) E3 pp23–25·§5.2 p87; [LoC 운영 교재](https://www.loc.gov/catworkshop/bibframe/Training/Bf2.0/2019/bf-2019-3.html) Unit6/8; [Yale](https://onlineexhibits.library.yale.edu/s/publication-and-prejudice/item/13314) Identifier/Source; [MusicBrainz remix](https://musicbrainz.org/recording/023b1e14-0e7e-4dc1-9ab4-9ef4f0e70ce0) Appears on releases, [work](https://musicbrainz.org/work/adfdfa6c-fa04-3571-aa2c-a13a99e64e96) Recordings.
- **반증·경계:** 같은 Work라는 이름도 모델 간 의미가 다르다. 한 URL에 두 판·양 방향 호출이 있어 URL1=엔터티1이 아니다. 음악의 같은 녹음 연결은 음향 비교 결과가 아니다. 소프트웨어 적용에는 방향·버전·wrapper·ABI·설정·근거 역할이 추가로 필요하다.
- **미확인:** 전체 음원 동일성, MusicBrainz 편집115752742 및 후속 split의 전체 복원 성공·비용 미확인. 공식 Merge 안내의 문서팀 미검토 표지도 남겼다.
- **자체 판정:** 분야별 최소원문과 목적·관점 비교는 충족. 음향·복원 효용으로의 전이는 미확인.

## Q7. 단순 묶음의 충분 조건과 되돌리기

- **지지:** Cairo PNG 읽기/쓰기 한 URL, Cairo PDF 별도 출력, GDAL COG/GTiff 호출·판 차이, libjpeg-turbo의 제한 API/ABI 호환과 역방향 확장 예외, zlib-ng native/compat·fork 차이를 보조 원장에 남겼다. U/Vg/Vr/K는 각각 단일 요소 변경이며 주풀을 교체하지 않는다.
- **원문·위치:** [Cairo PNG](https://www.cairographics.org/manual-1.12.4/cairo-PNG-Support.html) Synopsis; [libjpeg-turbo 고정 README](https://github.com/libjpeg-turbo/libjpeg-turbo/blob/af9c1c268520a29adf98cad5138dafe612b3d318/README.md) API/ABI·Colorspace/Mathematical Compatibility; [zlib-ng PORTING](https://github.com/zlib-ng/zlib-ng/blob/860e4cff7917d93f54f5d7f0bc1d0e8b1a3cb988/PORTING.md) native/compat·Changes from zlib; [MusicBrainz 실제 편집 토론](https://community.metabrainz.org/t/best-way-to-handle-a-recording-that-should-be-merged-but-contains-wrong-tracks-as-well/683297) posts6–9.
- **반증·경계:** 같은 문서 전체가 충분하면 단순 URL 보존이 유효하고, 어떤 목적에는 프로젝트/작품 대표도 충분할 수 있다. 반대로 의미 판정을 재현하거나 원자료 귀속을 복구하려면 원 member·목적·판·역할·방향·근거·정정 이력이 필요하다. 이 제품 저장 설계는 조건부 제안이며 최종 DB 선택이 아니다.
- **미확인:** U 변화 대상0/39, Vg 복수판 사례0/8이며 무변화는 안전성 증거가 아니다. Vr의 완전분모도0. K 상한은 B의 부분근거2개만 회복하고 완전 경로는 만들지 않는다. 별도 구현의 무조건 완전 대체와 실제 사용자 시험은 수행하지 않았다.
- **자체 판정:** 반례와 복원 가능한 표시 데이터·단일요소 계산은 충족. 노출 없는 규칙의 효과·무조건 대체·실제 복원 효용은 미확인.

## 검토와 정정 이력

G1 일반 gdaladdo의 HFA atom 과대 귀속을 제거하고 G4 HDF5 원문 안의 gdalinfo 예제를 반영했다. 주풀을 바꾸지 않고 coding correction_log에 원 라벨과 사유를 보존했다. U/V의 혼합 처치, 관계의 자동 방향 추론, 보완 근거/짝집계 구분, K의 클릭 해석은 amendments와 내부 검토에 남겼다. 처음 compile/recount의 스키마 불일치 오류도 execution-log에서 삭제하지 않았다. 최초 복원 검사가 S pool의 빈 의미필드를 후속 coding과 같다고 잘못 가정한 실패22/23도 보존했다. M09에서 원풀과 의미 판독층을 ID로 따로 복원하도록 검사 전제를 고쳤으며 주 입력·계산은 바꾸지 않았다. 내부 검토의 마지막 코드 해시는 FINAL_METHOD_REVIEW.md에 고정돼 있다.

## 수용에 남기는 세 우선순위

1. **W1:** 완전 적격0/8·이름요청0·U/Vg 무노출. 먼저 고정 요구와 부족 atom을 확인하고, 새 전향 표본에서 실제 대안 비교 기회를 확보한다. 기존8건을 바꾸지 않는다.
2. **W2:** 자연 href/seed 순서·실제 같은 문자수·실제 두 클릭의 엄격 조건 미충족. 첫 자료는 v2.3.1 contents와 GDAL 역사판 형식 목차이며 본문 노출 전에 raw href를 봉인한다.
3. **W3:** 내부 단일 판독·G/S 방향 범위 비균질·무조건 구현 대체/음향 동일성/전체 복원 미확인. 공통 범위의 G2/S1/G4 독립 재판독, IJG v6b 계약, MusicBrainz 편집115752742의 old/new 관계가 다음 최소 자료다.
