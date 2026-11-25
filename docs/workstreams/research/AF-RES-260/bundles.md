# 전달물·제거 대조 — 고정판의 정적 기대 (실행 아님)
기준: [사용 문서](https://github.com/twbs/icons/blob/8d88686c03c3768a2d82ba4f20c3c4e1b100fa29/docs/content/_index.md), [원 SVG](https://github.com/twbs/icons/blob/8d88686c03c3768a2d82ba4f20c3c4e1b100fa29/icons/alarm.svg), [sprite](https://github.com/twbs/icons/blob/8d88686c03c3768a2d82ba4f20c3c4e1b100fa29/bootstrap-icons.svg), [SVG2 use](https://www.w3.org/TR/SVG2/struct.html#UseElement), [SVG 처리모드](https://www.w3.org/TR/SVG2/conform.html). 모든 로컬 파일은 cold-cache, 동일 출처 HTTP, 동일 base, 16×16 슬롯, 스크립트 없음 조건. HTTP 서버와 브라우저는 실행 전제이지 복사 파일 수에 포함하지 않는다. MIT 라이선스 고지 A10 별도 보존(배포 시 필요 범위); 런타임 의존은 아님. 원본 파일의 온라인 URL은 출처 링크, 호스트 href는 배포 위치: 서로 다르다.

## 목적 × 삽입 방식
| 목적 | A 인라인 | B 외부 sprite | C img |
|---|---|---|---|
| 기존 페이지 표시 | 호스트 1개(아이콘 path 포함) | 호스트 + sprite 2개 | 호스트 + 개별 SVG 2개 |
| 형상 편집/추출 | 원 SVG 링크 또는 호스트의 해당 path + viewBox/fill-rule | 개별 원 SVG 링크 우선; sprite의 symbol ID+path도 가능하나 standalone svg wrapper, fill 복원 | 개별 원 SVG + viewBox/fill-rule; 페이지와 별개 |
| 오프라인 페이지 재현 | 호스트 1개, 내장 CSS | 호스트+sprite 2개, base와 상대 위치 유지 | 호스트+해당 SVG 2개, base와 상대 위치 유지 |
두 아이콘 동시: A 호스트 1, B 호스트+sprite 2, C 호스트+개별 SVG 2개=3; 여섯 자리 통합은 호스트+sprite+두 원 SVG=4. 색/접근성/스타일의 기존 외부 CSS, 필터, 폰트 의존은 이 표본에 없도록 작성; 기존 프로젝트의 추가 CSS 등은 별도 폐쇄를 구한다. 스프라이트 2050 symbol 중 선택 ID 2개; 파일 하나라는 말로는 나머지 2048개의 필요성을 말할 수 없다. 개별 alarm 689 ASCII bytes, arrow-right 311, sprite 1098145; connector로 읽은 텍스트의 길이이고 HTTP 압축·헤더·캐시 실제 전송량 아님.

## 한 파일씩 빼기
| 제거 | 영향(예상) | 남는 것 | 검산 |
|---|---|---|---|
| host | 여섯 슬롯 모두 재현 불가 | 원 SVG standalone 편집 가능, sprite symbol 추출 가능 | 같은 URL로 host 404; source editor 열기 |
| sprite | B1/B2 표시 불가 | A/C 해당 파일과 호스트 유지되면 정상 기대 | 응답 404 또는 요청 실패와 별도 pixel crop |
| alarm.svg | C1 불가 | A1 이미 복사, B1 sprite에서 유지 | C1 load/error, A1/B1 crop 비교 |
| arrow-right.svg | C2 불가 | A2/B2 유지 | C2 load/error, A2/B2 crop 비교 |
| 원 SVG 링크(파일 아닌 provenance) | B/A 표시 변동 없음 | 후속 편집에서 고정 원문 찾기 어려움 | provenance 제거 전후; 화면 비교와 독립 |
캐시·SW·외부 인터넷으로 누락 파일을 보충하지 않는다. file:// 외부 use 허용을 전제하지 않는다. offline은 로컬 HTTP + 외부망 차단 + 새 브라우저 컨텍스트를 의미한다. 편집용 최소 파일은 한 icon 원본 1개(원본 자체 외부 참조 0); 문맥 색이나 배치까지 편집하면 호스트도 필요하다.

## 네 통제 (X는 작성한 통제; O는 원본 관찰)
| ID | 입력/변경 | 정적 기대 | 반전 또는 확인 |
|---|---|---|---|
| X1 | fixture B1 href를 bootstrap-icons.svg#af-res-260-missing으로 변경; 원 sprite 문자열에 해당 id 없음 확인 | 리소스는 같아도 대상 미해결로 미표시 | target 없음에도 새 컨텍스트에서 동일 icon 표시하면 다른 fallback/cache/구현을 조사; 네트워크 200과 분리 |
| X2 | /assets/alt/icons/alarm.svg에 원 arrow-right.svg 바이트를 복제; C1 src=alt/icons/alarm.svg | basename alarm.svg 같아도 URL과 d가 다르므로 다른 형상 기대 | 응답 hash, 경로, 픽셀 비교; 경로만 같고 도메인 다른 경우도 가능 |
| X3 | A1 svg 내부에 <defs><g id="unused"><image href="never.svg" width="16" height="16"/></g></defs> 삽입; never.svg 미제공, CSS/선택 없음 | 원 path는 변함없고 defs는 직접 그려지지 않음; 해당 외부 자원이 화면에 불필요한지 테스트 가능. 요청 유무는 미확인 | 요청이 있더라도 그려진다고 단언하지 않음; 요청 및 화면 separately; 표시 실패 시 분리 가설 수정 |
| O4 | 원 alarm.svg, arrow-right.svg root와 path의 href/url()/외부 링크/defs 없음. xmlns는 namespace 식별자 | 원 SVG 자체 외부 자원 정상 공석(0); C host가 해당 파일을 가리키는 것과 구별 | XML 속성/스타일 파싱; 원본에 외부 참조 발견 시 철회 |
추가 X5: B1 host fill=currentColor 제거, color red는 유지; 선택 symbol에 fill 없으므로 initial fill black 기대 (N04). A/C는 원 root에 currentColor 존재. 이 대조는 currentColor가 파일의 이름/경로 형상 속성이 아니라 소비 문맥의 paint 선택임을 보여준다. forced colors 등은 별도 시험.

## 다른 분야: GeoPackage
[OGC 1.4] (G01) §1.1.3 및 §2.2.6–7: gpkg_contents.table_name -> gpkg_tile_matrix_set.table_name -> gpkg_tile_matrix(table_name,zoom_level) -> 해당 user tile table(zoom_level,tile_column,tile_row,tile_data). CRS/extent와 pixel size, tile dims가 해석에 관여. [GDAL SQL 표본](https://github.com/OSGeo/gdal/blob/6d7a6388745ef760b68d3ea460d700f4be5479c4/autotest/gdrivers/data/gpkg/byte.gpkg.sql) (G02): x/tiles, srs_id=26711, matrix extent 440720,3735960,456080,3751320; z0 matrix1×1 tile256×256 pixel60. 폭/높이 15360=1×256×60. x 행 id1,z0,col0,row0; PNG hex header IHDR 256×256. contents bbox 440720,3750120,441920,3751320과 다르며 파일의 모든 contents가 선택된 타일이 아니다. 파일 하나만 제공하면 layer와 zoom/col/row 선택 의도가 빠진다. OGC guide G03의 artifact 74984 본체 G05 미수신; GDAL SQL은 발행자 테스트 표본이며 본체와 동일하다고 볼 수 없다. 추가 [G06 실제 바이너리](https://github.com/OSGeo/gdal/blob/6d7a6388745ef760b68d3ea460d700f4be5479c4/autotest/gdrivers/data/gpkg/byte.gpkg) 12800 B를 base64로 받아 SQLite fileformat §1.6–7, §2.1–3에 따라 정적 b-tree record decode: contents root page5, matrix_set root13, matrix root16, user table byte root20. 네 행의 table_name은 x가 아니라 byte, contents last_change=2017-06-04T20:58:07.578Z; extents/matrix 수치 동일, user rowid1 z0 col0 row0 PNG blob712B IHDR256×256. evidence JSON에 page/offset/serial types/overflow 보존. SQL engine/표준 적합 실행 아님. 아이콘의 브라우저 관측을 여기에서 추론하지 않는다.

## 전달 구조 대안
1. 원 SVG 우선: 디자이너 편집에 유리, 2개 소형 파일; 직접 색 적용 필요 시 인라인 또는 명시적 wrapper. 원본을 고정해 수정본과 구분. 
2. 소비 호스트+sprite: 개발자의 여러 슬롯/일관된 테마에 유리. 전체 sprite는 편리하나 큰 전송 후보; 실제 효율은 반복, 압축, 캐시 계측 전 판단 금지.
3. 작성한 subset sprite: 두 symbol만 포함하면 파일 수는 B와 같아도 내용이 다르다. 공식 배포 파일 아님; 생성 입력+ID mapping+license+새 hash 제공, 누락/ID 충돌 검증. 
4. img 파일 전달: 호스트 마크업 짧고 독립 재사용 가능; 문맥 color 상속 불필요한 때만. CSS mask/inline/명시 fill로 recolor하는 변형은 표본 밖; 원본과 동일 표시라고 부르지 않는다.
