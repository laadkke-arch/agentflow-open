# 최초판 적격성 별도 판독과 사전 합의

판독자: 별도 모델 분담자 `contract_prior_audit`; 범위는 Blender 최초4건과 QGIS 최초8건의 최초 revision 본문 및 마스킹된 목록이다. 후속·답·댓글·점수·채택과 원 그림은 이 검토에서 읽지 않았다. root는 QGIS 최초8건 본문을 직접 다시 읽어 이견을 조정했다. 이 기록은 묶음1 원격 봉인 이전에 작성했다.

## 이견1 — QGIS 모집순위4를 넣는가

- 원문: https://gis.stackexchange.com/revisions/868C2CC1-4201-41CA-9316-7127F1AB66FB/view-source (질문473594).
- 최초 사이트 판독자는 순수 표시 설정을 처리 범위 밖으로 보는 좁은 해석에서 순위1·3·7·8을 제시했다.
- 별도 검토자는 point shapefile의 Location_Names로 실제 라벨링했고 이름이 중복되는 결과를 보았으므로 대상·관측목표·실제 조작의 세 조건을 충족한다고 보았다. 정확한 설정이 없다는 것은 매개변수 미확인이지 시도 없음이 아니다.
- **봉인 전 결정:** 주표는 순위1·3·4·7로 한다. 순위4는 기존 라벨 적용을 T/O로, GROUP BY는 제안된 생각 N으로만 코딩한다. 순위8(473619)은 적격이나 다음 순위로 남긴다. 원 해석은 삭제하지 않고 민감도/판독 이견으로 보존한다. 후속을 보고 교체한 것이 아니다.

## 이견을 피하기 위한 최초판 한정

| 원글/순위 | 검토 결과와 제한 |
| --- | --- |
| Blender309037/1 | 기존 island당 edge1 선택 결과는 실제 보고; 원 노드/숫자는 그림 판독 범위로 한정 |
| Blender309047/2 | Map Range 시도/실패 명시; 정확한 연결·분포·값은 미확인 |
| Blender309058/3 | to_curve 그룹을 만든 것은 T; bulk 부착/적용 코드는 원하는 골격이며 실행했다고 쓰지 않음 |
| Blender309084/4 | dodecahedron 생성과 edge 추가는 수행; centre-edge collapse는 희망 단계 |
| QGIS473575/1 | centroid 계산·snapping은 수행; adjacency graph는 아직 희망, 원 작성자 공개ID 미확인 |
| QGIS473578/2 | 설치/제공자 복구로 제외. 구체적인 설치 시도가 없어서 제외하는 것이 아님 |
| QGIS473591/3 | 20개 점 배치 expression 실제 보고; 거리 label은 희망. 본문 괄호 불완전성 그대로 보존 |
| QGIS473594/4 | label-by-Location_Names의 중복 관측으로 포함; GROUP BY 실행 미확인 |
| QGIS473605/5 | 공동 작업/호스팅 구성 범위로 제외; demo publish 실제 수행은 인정 |
| QGIS473607/6 | zoom 조작과 화면 현상은 존재하나 구체적인 GIS 처리/편집 조작과 diagram 설정 미식별로 제외. 아무 시도도 없었다는 뜻 아님 |
| QGIS473611/7 | merge→reproject와 역순 둘 다 시도; 실제 출력차·resampling/grid·NoData/판 미확인 |
| QGIS473619/8 | PDF loading·preview 해상도 저하만 지지. 최종 georeference 실행/최종 raster 해상도를 관측한 것으로 쓰지 않음 |

후속 결과의 독립 맹검 평가, 사람의 검토, 두 사이트 전체80건의 이중 판독을 했다는 주장은 하지 않는다.
