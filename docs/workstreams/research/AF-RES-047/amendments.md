# 관측 뒤 해석·수집 변경 원장

원 SCOPE와 최초 frame/selection은 5c75f3571ab8473f3fba72d92a70bd201c0cf189 및 6b74510d9b660fc1a3fe76c9f7845d727b930297에 보존한다. 아래 변경을 원래부터 적용한 것으로 설명하지 않는다.

## A01 — ESSD 실제 사용의 선정과 사용판·필드 연결의 검증을 분리

- 원규칙: SCOPE §2의 '제3자 공개 자료를 실제 입력으로 사용했고 표·그림·출력 예에 수치/분류가 있는 최초3편'. 최초 시행은 '그 output field가 외부 원자료에서 넘어왔는지까지 확인돼야 적격'으로 좁게 읽었다.
- 원선정: N-E01=essd-14-19-2022, N-E02=essd-14-33-2022, N-E03=essd-14-57-2022. 앞순위 essd-14-1-2022는 boundary_unresolved였다. 6b74510의 collection/essd/selection.json과 frame.csv를 덮어쓰지 않는다.
- 반대 근거: [essd-14-1-2022](https://essd.copernicus.org/articles/14/1/2022/) §3 L260은 WoRMS에 따라 species nomenclature를 표준화했다고 명시한다. Table2의 분류·숫자도 존재한다. §3 L261은 groups가 엄격한 taxonomic rank가 아닌 functional group이라고 명시한다. 따라서 실제 재사용은 명시됐고, Table2의 첫 Group=Amphipoda와 WoRMS 입력 필드의 정확한 연결은 후속 검증의 결측이다. 결측을 이유로 이 소비자를 건너뛰면 판 보존성이 약한 사례를 사전에 제거하는 편향이 생긴다.
- 결정: N-E00=essd-14-1-2022를 primary 소비 슬롯에 포함하고 주 ESSD3은 N-E00/N-E01/N-E02로 한다. N-E03의 원선정·원문·필드·판독을 legacy/sensitivity 보조로 모두 남긴다. 이 결정은 root가 원소비 본문을 직접 재독한 후, N-E00의 WoRMS 발행판·값을 열기 전에 이루어졌다. 판·정정 성공을 본 뒤 표본을 골라 바꾼 것은 아니다. 단 E01/E02/E03의 일부 후속 결과에는 이미 노출됐으므로 전체 절차가 전부 사전등록이었다고 하지 않는다.
- 바뀌지 않는 것: 첫30의 노출순, first field 규칙, P/U/R/V 합격선, 실제 입력 판/실행/값 미확인의 처리. N-E00의 Table2와 WoRMS의 연결을 확인된 것으로 승격하지 않는다.
- 영향: 주표의 ESSD 마지막 슬롯에 N-E03 대신 N-E00을 포함한다. 원선정 집계(RJ01–03+N-E01–03)와 정정선정 집계(RJ01–03+N-E00–02)를 analysis-summary.json에 둘 다 계산한다. 8/24 주표 밖 N-E03의3구성은 collection/essd에 보존한다.
- 한계: 초기 선정 해석의 일탈이다. strict preregistration adherence는 미충족으로 보고한다. 사용판 실제 확인 여부를 판정하는 문턱은 낮추지 않는다.

## A02 — R Journal 실행 메타데이터를 데이터 필드로 잘못 읽을 가능성 제거

RJ-2022-007의 Fig3 runtime/error와 missues node ID는 Iris 변수나 그 변수에서 도출한 통계량이 아니다. '첫 해당 필드' 규칙에 따라 최초 실제 통계 출력인 Species 행 Df=2를 고정했다. 해석은 발행자 자료 열람 전 collection/rjournal/selection_freeze.json에 기록했고 6b74510에 봉인했다. runtime 숫자를 처음부터 통계 필드였던 것처럼 바꾸지 않으며 그 후보는 같은 파일 alternative_field/field_selection_exclusion에 남아 있다. 사용판 성공 결과를 보고 바꾼 것은 아니다.

## A03 — 실행 목록의 연결 저장소 확장

원목록+연결 논문 목록의 최초 metadata는19개였고 2021–2024로 확인되는 항목은14개였다. 원본은 collection/runs/frame-metadata-frozen.csv 및 metadata-freeze.json으로 6b74510에 저장했다. SCOPE§3이 허용한 실제 링크의 공개 examples 저장소 목록을 추가 확인해38 metadata 노출로 확장했다. 추가 목록도 공개일·식별자를 확인하고 처음30의 포함/제외를 별도 frame에 남긴다. 값 일치·정정 성과로 후행 사례를 교체하지 않는다. 선정이 앞선19의 상태에서 진행된 범위와 추가 후보가 먼저 위치하는지에 대한 점검은 실행 원장에 명시한다.

## A04 — 시각 정밀도 및 바이트 관측의 범위

일부 웹 open 호출은 도구 반환에 정확한 시작 UTC가 없다. 해당 rows는 뒤의 실제 clock 상한 또는 두 clock 사이의 분 단위 구간이라고 표시한다. 셸 HTTP receipt의 시작/끝 UTC와 섞어 초 단위 정확성을 주장하지 않는다. domain/S-D09–14는 실제22:06:00~22:07:00 UTC 구간이고 정확초는 미확인이다. consumer/publisher의 순서는 selection seal과 후속 receipt로 구분한다.
