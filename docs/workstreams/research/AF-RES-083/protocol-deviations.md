# 판독 중 드러난 절차 해석과 한계

SCOPE의 원문은 첫 원격 커밋7b108414de50ff32f28d1fa3c03ef6f2492724e6에서 고정했다. 아래는 옛 자료를 읽고 기록한 해석이며 후속판에 맞춘 표본 교체가 아니다.

1. **검색어와 적격 조건은 다르다.** pyarrow.parquet처럼 넓은 검색식으로 발견된 primitive a/b/c table 예제는 GeoParquet·geometry/CRS·GEOARROW 연결이 없어 핵심표본에서 제외했다. 같은 방식으로 NumPy trapz, Astropy Trapezoid1D, SciPy quad의 안내를 O02 이름 이관 표본으로 넣지 않았다. 결과는 G04-3과 O02 세 자리 공석이며 코드·연결 안내는 부록이다.
2. **한 guide의 두 지시와 두 저작을 구분한다.** GeoPandas io.rst의 공간정보 roundtrip과 schema_version 선택은 행동/필수조건이 달라 두 원레코드로 기록하되, 독립 하류 저작·발견 계보는1이다. 같은 목적의 read/write 예제를 잘라 독립 성공 수를 만들지 않았다.
3. **정식 발표일이 태그일을 보정했다.** Arrow16.1.0 tagger date는2024-05-09지만 공식 발행목록은2024-05-14다. GDAL3.9.0 발표2024-05-10을 기준으로 옛판은16.0.0, 첫후속은16.1.0이다. tag를출시일로확정한 잘못을 피했다. Astropy는 GitHub 과거release누락으로 annotated tag일을 대용하며, 시간순 첫후속4.0.5가 옛4.2와 다른 maintenance계열인 한계를 보존했다.
4. **최소 자료량과 모집 달성은 다른 검사다.** 보조층에서 직접 읽은 별도 하류 guide는 원저작 자료량에는 들어가지만 빈 core자리를 채우지 않는다. 코드·test·build 설정의 단독 행도 사용안내로 세지 않는다. downloaded/search-scanned 파일 수는 직접 분석한 원저작 수가 아니다.
5. **사전성의 범위.** 후속 tag/release 날짜·SHA metadata는 옛판 선택용으로 읽었고, 소비자 후속본문·같은 문단 git이력·후속test는 원레코드/A/B의 두 번째 원격커밋 이후에만 읽는다. 상류1.11/1.14 설명을 미리 읽은 것은 상류 근거에 해당하며 소비자의 실제 수정 관측이 아니다. 최초 로컬기준 커밋dafdb206245c2bc8b3f26bec3d18d74e47342803은 같은tree로원격7b108414…에게시됐고, 인증없는git push실패 후 승인된GitHub connector로게시했다. 원격branch를force하지 않았다.
