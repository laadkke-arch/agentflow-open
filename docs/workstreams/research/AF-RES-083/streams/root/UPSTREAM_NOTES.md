# 상류 원문과 079 관측의 적용 범위

소비자 후속판을 읽기 전 열 수 있는 상류 설명·호환 선언·고정 소스의 판독이다. 079 실행을 다시 수행하지 않았다. 원문 위치·UTC·해시는 sources.jsonl과 acquisition.jsonl에서 연결한다.

## G04

GDAL 3.8.0 Parquet manual은 GEOMETRY_ENCODING의 기본값을 WKB로 두고 GEOARROW/WKT를 규격 밖 확장으로 설명한다(L70–77). 3.9.0 manual은 WKB를 그대로 기본으로 두면서 기존 GEOARROW 이름을 GEOARROW_INTERLEAVED로 옮겼고, GEOARROW는 GeoParquet1.1의 struct 인코딩을 뜻한다고 명시한다(L68–83). 같은 현재 페이지가 이 두 판의 뜻을 구분하지 않는 별칭표를 대신할 수 없다.

GeoParquet1.0의 Geometry columns/encoding은 WKB를 요구한다.1.1은 WKB와 native single-geometry 인코딩을 구별하며 native coordinates는 separated struct를 사용한다.1.1 Version Compatibility는 옛 reader가 새 데이터를 정확히 해석하거나 해석할 수 없음을 인식하도록 요구한다. 따라서 minor version의 forward compatibility는 모든 신파일의 성공적 읽기라는 약속이 아니다. GeoArrow 메모리 규격 자체는 separated/interleaved 두 표현을 설명하므로, GeoArrow 지원과 특정 GeoParquet 판의 encoding 지원을 합치지 않는다.

079의 GN04–07은 GDAL3.8/3.9 지정 writer/reader·입력파일에 관한 관측이다. WKB 정상읽기, struct→구reader에서 geometry/CRS 손실, interleaved→geometry복구와 bbox추가, null/EMPTY 차이가 각각 다른 관측이다. GeoPandas와 Arrow의 공개 안내에 그 exact writer/reader/encoding/fixture가 없으면 이 성공·실패 결과를 그 안내의 검증 결과로 복사하지 않는다.

## O02

SciPy1.6.0 release note는 옛 적분 이름을 호환 목적으로 남긴다고 설명한다(L52–57). 같은 판 _quadrature.py는 NumPy trapz를 공용 trapezoid로 가져오고(L7–9), trapz wrapper는 그대로 인자를 넘긴다(L37–43). cumtrapz wrapper(L273–279), simps wrapper(L407–413)도 존재한다. simpson 당시 기본 even='avg'와 허용 even 값은 별도로 기록해야 한다. namespace가 scipy.integrate인 공개계약과 내부 계산이 NumPy 구현이라는 사실은 함께 성립한다.

1.6.0 공급자 시험에는 y=arange(4), x=2**y에서 simps/simpson의 alias 비교와 누적적분 alias 비교가 존재한다. 이번 세션은 이 시험의 소스를 읽었다. 시험을 실행했다고 주장하지 않는다. 079도 trapz의 지정 입력은 실행했지만 simps/cumtrapz 개별 실행은 없었다.

후속 상류의 별도 조건 변경도 확인했다.1.11.0의 PR18209(merge572a373aac2bf14ee6a0c164aac9734b54594b8f)는 짝수 표본에서 마지막 구간을 계산하는 기본 방법을 바꿨고, 유지관리자는 기존 하류 수치가 달라질 수 있다고 설명했다.1.14.0은 옛 세 이름을 제거하고 simpson의 even 인자와 positional keyword 인자 사용도 제거했다. 따라서1.6의 별칭 전달을1.14의 모든 호출·수치 동등성으로 넓힐 수 없다. 제거 예고판(1.11문서의1.13)과 실제 제거판(1.14)도 구분한다.

## 재사용 금지선

- 포맷명 Parquet만 같은 일반 a/b/c table 예제는 GeoParquet geometry/CRS 또는 GDAL GEOARROW 인코딩을 증명하지 않는다.
- numpy.trapz를 사용하는 하류 호출은 scipy.integrate.trapz 제거만으로 수정 필요가 생기지 않는다. NumPy 자체 이관은 별도 변경이다.
- 내부 simps 호출을 찾았다는 사실만으로 발행된 문서가 독자에게 simps 사용을 권했다고 판정하지 않는다.
- 정적 alias/시험의 존재, 079의 실제 지정 실행, 이번 소비자의 실제 설치 build는 다른 근거다. 어느 하나를 다른 것으로 바꾸어 적지 않는다.
