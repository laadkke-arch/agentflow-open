## 표 1. 요구 원문과 적격 분모

| 요구ID·언어 | 현행·직전 대상 판과 원조작·조건 | 직접 적격·미확인, 기능·페이지 | 원근거 URL·절 |
| --- | --- | --- | --- |
| Q-SP · en/ko | v9.2.0 · v9.1.1 · Automatically modernize source-code type annotations during pre-commit checks / Keep the code compatible with Python 3.8 by postponing annotation evaluation. | 현행 0/24, 미확인 0 · 직전 0/24, 미확인 0 · 직접 페이지 0/21 · 0/21 | [작성자 본문](https://github.com/sphinx-doc/sphinx/issues/11065) · L1–L7 |
| Q-MK · en/ko | 1.6.1 · 1.6.0 · Restrict copying, cutting, pasting and right-clicking the text / The restriction must apply to pages emitted by the static documentation build. | 현행 0/24, 미확인 0 · 직전 0/24, 미확인 0 · 직접 페이지 0/21 · 0/21 | [작성자 본문](https://github.com/mkdocs/mkdocs/issues/3085) · L3–L5 |
| Q-PA · en/ko | v3.5.1 · v3.5.0 · Set or unset tags directly from saved views or the document list / The action must work when a document already has automatically assigned tags. | 현행 1/24, 미확인 0 · 직전 1/24, 미확인 0 · 직접 페이지 1/21 · 1/21 | [작성자 본문](https://github.com/paperless-ngx/paperless-ngx/issues/2300) · L3–L13 |
| Q-DA · en/ko | release-5.6.2 · release-5.6.1 · Close the image editor module whose header is left-clicked / Keep the other expanded modules open. | 현행 0/24, 미확인 0 · 직전 0/24, 미확인 0 · 직접 페이지 0/21 · 0/21 | [작성자 본문](https://github.com/darktable-org/darktable/issues/13250) · L2–L15 |
| Q-DU · en/ko | v2.0.1 · v2.0.0 · Create and evaluate a table CHECK constraint with nested lambda expressions / The nested expression must continue to see the other referenced table column. | 현행 0/24, 미확인 1 · 직전 0/24, 미확인 1 · 직접 페이지 0/21 · 0/21 | [작성자 본문](https://github.com/duckdb/duckdb/issues/5816) · L3–L12 |
| Q-GD · en/ko | v3.13.3 · v3.13.2 · Resolve the WGS84 spatial reference when opening a dataset / Spatial-reference cleanup on another Windows thread must remain safe. | 현행 0/24, 미확인 0 · 직전 0/24, 미확인 0 · 직접 페이지 0/21 · 0/21 | [작성자 본문](https://github.com/OSGeo/gdal/issues/7010) · L1–L5 |

## 표 2. 표시 후보의 순위와 실제 반환 위치

굵은 숫자는 표시, 나머지 숫자는 12개 조사 후보 안의 순위다. 메모 칸은 B가 더한 토큰과 C 충돌 판별이다.

| 요구·후보 | A / B / C | 메모 토큰·판/목적 충돌 | 순위 공개 전 판정·대상 | 실제 반환 위치 |
| --- | --- | --- | --- | --- |
| Q-SP/en · GD-X1.old | **1** / **3** / **2** | in · — | 충돌 · COG pyramid / reduced-resolution overview levels | [L11-L29](https://github.com/OSGeo/gdal/blob/b40672525acf3f5c4f29d8541aa7dcff1e18eb92/doc/source/drivers/raster/cog.rst#L11-L29) |
| Q-SP/en · GD-X2.current | **2** / — / — | — · — | 충돌 · opened or created raster and companion header | [L11-L39](https://github.com/OSGeo/gdal/blob/c8b4c45fca87d3e6fbf80e7a7898b8a661ad0edc/doc/source/drivers/raster/envi.rst#L11-L39) |
| Q-SP/en · GD-X1.current | **3** / 6 / 5 | in · — | 충돌 · COG pyramid / reduced-resolution overview levels | [L11-L29](https://github.com/OSGeo/gdal/blob/c8b4c45fca87d3e6fbf80e7a7898b8a661ad0edc/doc/source/drivers/raster/cog.rst#L11-L29) |
| Q-SP/en · MK-X2.current | — / **1** / **1** | in·python·while · — | 충돌 · warnings filtered and formatted | [L48-L62](https://github.com/mkdocs/mkdocs/blob/bb7e8b62185b11d9f59bb7f50b13c15134f62f8a/mkdocs/__main__.py#L48-L62) |
| Q-SP/en · SP-X1.current | — / **2** / 11 | 3·python · python:3.8 | 충돌 · installable distribution and runnable builder | [L17-L28](https://github.com/sphinx-doc/sphinx/blob/7b2c103eaa4cabf0ac47224c444cf0cbc7c745e5/pyproject.toml#L17-L28) |
| Q-SP/en · MK-X1.old | — / 4 / **3** | source·while · — | 충돌 · timestamp used by site build | [L47-L83](https://github.com/mkdocs/mkdocs/blob/0998fec7eb32d269f02c6d87071d6163c251db30/mkdocs/utils/__init__.py#L47-L83) |
| Q-SP/ko · SP-X1.current | — / **1** / **2** | 3·python · python:3.8 | 충돌 · installable distribution and runnable builder | [L17-L28](https://github.com/sphinx-doc/sphinx/blob/7b2c103eaa4cabf0ac47224c444cf0cbc7c745e5/pyproject.toml#L17-L28) |
| Q-SP/ko · SP-X1.old | — / **2** / **3** | 3·python · python:3.8 | 충돌 · installable distribution and runnable builder | [L17-L28](https://github.com/sphinx-doc/sphinx/blob/479428338eb86b6fe2984ef22eee1f73269f9cb4/pyproject.toml#L17-L28) |
| Q-SP/ko · MK-X2.current | — / **3** / **1** | python · — | 충돌 · warnings filtered and formatted | [L48-L62](https://github.com/mkdocs/mkdocs/blob/bb7e8b62185b11d9f59bb7f50b13c15134f62f8a/mkdocs/__main__.py#L48-L62) |
| Q-MK/en · MK-X1.old | **1** / 7 / 7 | a·site · — | 충돌 · timestamp used by site build | [L47-L83](https://github.com/mkdocs/mkdocs/blob/0998fec7eb32d269f02c6d87071d6163c251db30/mkdocs/utils/__init__.py#L47-L83) |
| Q-MK/en · MK-X1.current | **2** / 8 / 8 | and·site · — | 충돌 · timestamp used by site build | [L47-L83](https://github.com/mkdocs/mkdocs/blob/bb7e8b62185b11d9f59bb7f50b13c15134f62f8a/mkdocs/utils/__init__.py#L47-L83) |
| Q-MK/en · DU-X2.current | **3** / 10 / 10 | a·by · — | 충돌 · boolean result including SQL NULL semantics | [L57-L125](https://github.com/duckdb/duckdb-web/blob/9812b681ecdedd0419c2250bf8163280c90124e6/docs/2.0/sql/expressions/subqueries.md#L57-L125) |
| Q-MK/en · SP-X1.current | — / **1** / **1** | a·and·documentation·on · — | 충돌 · installable distribution and runnable builder | [L17-L28](https://github.com/sphinx-doc/sphinx/blob/7b2c103eaa4cabf0ac47224c444cf0cbc7c745e5/pyproject.toml#L17-L28) |
| Q-MK/en · SP-G2.old | — / **2** / **2** | and·build·documentation·right · — | 일부 · 일부 조건 지원 | [L20-L50](https://github.com/sphinx-doc/sphinx/blob/479428338eb86b6fe2984ef22eee1f73269f9cb4/doc/usage/markdown.rst#L20-L50) |
| Q-MK/en · MK-G2.old | — / **3** / **3** | a·and·documentation·generated · — | 일부 · 일부 조건 지원 | [L1-L21](https://github.com/mkdocs/mkdocs/blob/0998fec7eb32d269f02c6d87071d6163c251db30/docs/user-guide/choosing-your-theme.md#L1-L21) |
| Q-MK/ko | — / — / — | — | 표시 공석 각 3 | — |
| Q-PA/en · PA-G2.old | **1** / **1** / **1** | documents·or·tags · — | 직접 · 동작+조건 | [L75-L83](https://github.com/paperless-ngx/paperless-ngx/blob/bfd0d7fe3671cb8ffa28fb5ea69f6aef817dca5a/docs/usage.md#L75-L83) |
| Q-PA/en · PA-G2.current | **2** / **2** / **2** | documents·or·tags · — | 직접 · 동작+조건 | [L75-L83](https://github.com/paperless-ngx/paperless-ngx/blob/35b0439195bbdb87a6d519152e6782abe0720c3b/docs/usage.md#L75-L83) |
| Q-PA/en · PA-X1.old | **3** / 7 / 7 | documents·or · — | 충돌 · visible streamed answer in the toolbar chat | [L343-L345](https://github.com/paperless-ngx/paperless-ngx/blob/bfd0d7fe3671cb8ffa28fb5ea69f6aef817dca5a/docs/usage.md#L343-L345) |
| Q-PA/en · DA-X2.current | 4 / **3** / **3** | already·or·the · — | 충돌 · profile update with foreground focus preserved by this path | [L2042-L2070](https://github.com/darktable-org/darktable/blob/20891f6c6fa7be995e5bf9dff9d1ee5062051773/src/common/colorspaces.c#L2042-L2070) |
| Q-PA/ko | — / — / — | — | 표시 공석 각 3 | — |
| Q-DA/en · DA-X1.old | **1** / **1** / **1** | image·its·the·with · — | 충돌 · corrected highlights or clipping fallback | [L26-L68](https://github.com/darktable-org/dtdocs/blob/fb1850bb71f45ecc738b6a9603e99b13e0c6cd0d/content/module-reference/processing-modules/highlight-reconstruction.md#L26-L68) |
| Q-DA/en · DA-X1.current | **2** / 5 / 5 | image · — | 충돌 · corrected highlights or clipping fallback | [L26-L68](https://github.com/darktable-org/dtdocs/blob/9427e1402fa49e5fa78eb138751b4a2e93664d36/content/module-reference/processing-modules/highlight-reconstruction.md#L26-L68) |
| Q-DA/en · DA-G2.old | **3** / 8 / 8 | with · — | 충돌 · ordered image sequence | [L7-L25](https://github.com/darktable-org/dtdocs/blob/fb1850bb71f45ecc738b6a9603e99b13e0c6cd0d/content/lighttable/digital-asset-management/sequence.md#L7-L25) |
| Q-DA/en · GD-X2.old | — / **2** / **2** | header·open·the·with · — | 충돌 · opened or created raster and companion header | [L11-L39](https://github.com/OSGeo/gdal/blob/b40672525acf3f5c4f29d8541aa7dcff1e18eb92/doc/source/drivers/raster/envi.rst#L11-L39) |
| Q-DA/en · GD-X2.current | — / **3** / **3** | header·open·with · — | 충돌 · opened or created raster and companion header | [L11-L39](https://github.com/OSGeo/gdal/blob/c8b4c45fca87d3e6fbf80e7a7898b8a661ad0edc/doc/source/drivers/raster/envi.rst#L11-L39) |
| Q-DA/ko | — / — / — | — | 표시 공석 각 3 | — |
| Q-DU/en · DU-X2.current | **1** / **1** / **1** | a·to·with · — | 충돌 · boolean result including SQL NULL semantics | [L57-L125](https://github.com/duckdb/duckdb-web/blob/9812b681ecdedd0419c2250bf8163280c90124e6/docs/2.0/sql/expressions/subqueries.md#L57-L125) |
| Q-DU/en · DU-X2.old | **2** / **3** / **3** | a·to · — | 충돌 · boolean result including SQL NULL semantics | [L57-L125](https://github.com/duckdb/duckdb-web/blob/b1c51f38bf83a5033d31cc0cdf0bf000d7e34d7c/docs/2.0/sql/expressions/subqueries.md#L57-L125) |
| Q-DU/en · DU-G1.current | — / **2** / **2** | a·and·column·table·with · — | 충돌 · SQL relation or table | [L13-L64](https://github.com/duckdb/duckdb-web/blob/9812b681ecdedd0419c2250bf8163280c90124e6/docs/2.0/data/csv/overview.md#L13-L64) |
| Q-DU/ko · DU-X2.current | **1** / **1** / **1** | — · — | 충돌 · boolean result including SQL NULL semantics | [L57-L125](https://github.com/duckdb/duckdb-web/blob/9812b681ecdedd0419c2250bf8163280c90124e6/docs/2.0/sql/expressions/subqueries.md#L57-L125) |
| Q-DU/ko · DU-X2.old | **2** / **2** / **2** | — · — | 충돌 · boolean result including SQL NULL semantics | [L57-L125](https://github.com/duckdb/duckdb-web/blob/b1c51f38bf83a5033d31cc0cdf0bf000d7e34d7c/docs/2.0/sql/expressions/subqueries.md#L57-L125) |
| Q-GD/en · DA-X1.old | **1** / 9 / 9 | the · — | 충돌 · corrected highlights or clipping fallback | [L26-L68](https://github.com/darktable-org/dtdocs/blob/fb1850bb71f45ecc738b6a9603e99b13e0c6cd0d/content/module-reference/processing-modules/highlight-reconstruction.md#L26-L68) |
| Q-GD/en · DA-X1.current | **2** / — / — | — · — | 충돌 · corrected highlights or clipping fallback | [L26-L68](https://github.com/darktable-org/dtdocs/blob/9427e1402fa49e5fa78eb138751b4a2e93664d36/content/module-reference/processing-modules/highlight-reconstruction.md#L26-L68) |
| Q-GD/en · SP-X1.current | — / **1** / **1** | a·on·the · — | 충돌 · installable distribution and runnable builder | [L17-L28](https://github.com/sphinx-doc/sphinx/blob/7b2c103eaa4cabf0ac47224c444cf0cbc7c745e5/pyproject.toml#L17-L28) |
| Q-GD/en · MK-X1.old | — / **2** / **2** | a·the·while · — | 충돌 · timestamp used by site build | [L47-L83](https://github.com/mkdocs/mkdocs/blob/0998fec7eb32d269f02c6d87071d6163c251db30/mkdocs/utils/__init__.py#L47-L83) |
| Q-GD/en · SP-X1.old | — / **3** / **3** | a·on·the · — | 충돌 · installable distribution and runnable builder | [L17-L28](https://github.com/sphinx-doc/sphinx/blob/479428338eb86b6fe2984ef22eee1f73269f9cb4/pyproject.toml#L17-L28) |
| Q-GD/ko | — / — / — | — | 표시 공석 각 3 | — |

## 표 3. 방식·영역별 상위3과 비용

각 행은 요구 2×표시 3=6, 조사 2×12=24다. 순서는 현행/직전이다. 비용은 DB/단어표·색인 바이트와 1회차 두 요청의 조회횟수·경과 시간이다. C의 경과는 B 조회와 재정렬의 합이다.

| 언어·방식·영역·판 | 표시 직접 적격·오추천·일부·미확인 | 빠진 적격과 빈 자리 | 준비·조회 비용 | 두 번 재생 |
| --- | --- | --- | --- | --- |
| en · A · 문서 출판 · 현행/직전 | 직접 0 / 0 · 오추천 4 / 2 · 일부 0 · 미확인 0 | 누락 기능 0 / 페이지 0 · 표시 0/6 · 조사 12/24 | 180,224/90,112 B · 2회 · 0.652 ms | 일치 |
| en · A · 파일·미디어 보관 · 현행/직전 | 직접 1 / 1 · 오추천 1 / 3 · 일부 0 · 미확인 0 | 누락 기능 0 / 페이지 0 · 표시 0/6 · 조사 14/24 | 180,224/90,112 B · 2회 · 0.381 ms | 일치 |
| en · A · 표·지리 변환 · 현행/직전 | 직접 0 / 0 · 오추천 2 / 2 · 일부 0 · 미확인 0 | 누락 기능 0 / 페이지 0 · 표시 2/6 · 조사 20/24 | 180,224/90,112 B · 2회 · 0.304 ms | 일치 |
| en · B · 문서 출판 · 현행/직전 | 직접 0 / 0 · 오추천 3 / 1 · 일부 2 · 미확인 0 | 누락 기능 0 / 페이지 0 · 표시 0/6 · 조사 0/24 | 299,008/208,896 B · 2회 · 0.867 ms | 일치 |
| en · B · 파일·미디어 보관 · 현행/직전 | 직접 1 / 1 · 오추천 2 / 2 · 일부 0 · 미확인 0 | 누락 기능 0 / 페이지 0 · 표시 0/6 · 조사 0/24 | 299,008/208,896 B · 2회 · 0.734 ms | 일치 |
| en · B · 표·지리 변환 · 현행/직전 | 직접 0 / 0 · 오추천 3 / 3 · 일부 0 · 미확인 0 | 누락 기능 0 / 페이지 0 · 표시 0/6 · 조사 0/24 | 299,008/208,896 B · 2회 · 1.094 ms | 일치 |
| en · C · 문서 출판 · 현행/직전 | 직접 0 / 0 · 오추천 2 / 2 · 일부 2 · 미확인 0 | 누락 기능 0 / 페이지 0 · 표시 0/6 · 조사 0/24 | 299,008/208,896 B · 공유 2, 추가 0회 · 0.917 ms | 일치 |
| en · C · 파일·미디어 보관 · 현행/직전 | 직접 1 / 1 · 오추천 2 / 2 · 일부 0 · 미확인 0 | 누락 기능 0 / 페이지 0 · 표시 0/6 · 조사 0/24 | 299,008/208,896 B · 공유 2, 추가 0회 · 0.761 ms | 일치 |
| en · C · 표·지리 변환 · 현행/직전 | 직접 0 / 0 · 오추천 3 / 3 · 일부 0 · 미확인 0 | 누락 기능 0 / 페이지 0 · 표시 0/6 · 조사 0/24 | 299,008/208,896 B · 공유 2, 추가 0회 · 1.123 ms | 일치 |
| ko · A · 문서 출판 · 현행/직전 | 직접 0 / 0 · 오추천 0 / 0 · 일부 0 · 미확인 0 | 누락 기능 0 / 페이지 0 · 표시 6/6 · 조사 24/24 | 180,224/90,112 B · 2회 · 0.142 ms | 일치 |
| ko · A · 파일·미디어 보관 · 현행/직전 | 직접 0 / 0 · 오추천 0 / 0 · 일부 0 · 미확인 0 | 누락 기능 1 / 페이지 2 · 표시 6/6 · 조사 24/24 | 180,224/90,112 B · 2회 · 0.177 ms | 일치 |
| ko · A · 표·지리 변환 · 현행/직전 | 직접 0 / 0 · 오추천 1 / 1 · 일부 0 · 미확인 0 | 누락 기능 0 / 페이지 0 · 표시 4/6 · 조사 22/24 | 180,224/90,112 B · 2회 · 0.347 ms | 일치 |
| ko · B · 문서 출판 · 현행/직전 | 직접 0 / 0 · 오추천 2 / 1 · 일부 0 · 미확인 0 | 누락 기능 0 / 페이지 0 · 표시 3/6 · 조사 21/24 | 299,008/208,896 B · 2회 · 0.193 ms | 일치 |
| ko · B · 파일·미디어 보관 · 현행/직전 | 직접 0 / 0 · 오추천 0 / 0 · 일부 0 · 미확인 0 | 누락 기능 1 / 페이지 2 · 표시 6/6 · 조사 24/24 | 299,008/208,896 B · 2회 · 0.103 ms | 일치 |
| ko · B · 표·지리 변환 · 현행/직전 | 직접 0 / 0 · 오추천 1 / 1 · 일부 0 · 미확인 0 | 누락 기능 0 / 페이지 0 · 표시 4/6 · 조사 22/24 | 299,008/208,896 B · 2회 · 0.176 ms | 일치 |
| ko · C · 문서 출판 · 현행/직전 | 직접 0 / 0 · 오추천 2 / 1 · 일부 0 · 미확인 0 | 누락 기능 0 / 페이지 0 · 표시 3/6 · 조사 21/24 | 299,008/208,896 B · 공유 2, 추가 0회 · 0.211 ms | 일치 |
| ko · C · 파일·미디어 보관 · 현행/직전 | 직접 0 / 0 · 오추천 0 / 0 · 일부 0 · 미확인 0 | 누락 기능 1 / 페이지 2 · 표시 6/6 · 조사 24/24 | 299,008/208,896 B · 공유 2, 추가 0회 · 0.104 ms | 일치 |
| ko · C · 표·지리 변환 · 현행/직전 | 직접 0 / 0 · 오추천 1 / 1 · 일부 0 · 미확인 0 | 누락 기능 0 / 페이지 0 · 표시 4/6 · 조사 22/24 | 299,008/208,896 B · 공유 2, 추가 0회 · 0.182 ms | 일치 |

## 결론과 수용 범위

**PARTIAL.** 고정한 여섯 공개 작성자 게시물에서 메모가 추가로 찾은 직접 적격 기능은 0개다. 영어 상위3은 A·B·C 모두 같은 1기능과 두 판 페이지를 찾았다. 한국어에서 메모가 채운 세 표시는 모두 충돌이었다. 순위가 봉인된 단일 작업자 판독과 두 번의 SQLite 재생까지 실행했다. 최초 생성 순간의 본문 0/6 확인과 별도 독립 판독 0건이 수용 결손이다.

### Q1 · 모집과 적용 범위

문서 출판·파일/미디어 보관·표/지리 변환 각 8기능이다. 원 목차 일반 12자리와 공식 변경 12자리, 공석 0의 24자리를 고정했다. 판별 기준일은 2026-11-23 00:00 UTC다. 공식 목록의 안정판/직전판 여섯 쌍과 코드 SHA를 확인했고, DuckDB 웹 문서와 darktable 매뉴얼은 패치 코드와 별도 발행 계보를 기록했다. 해당 두 매뉴얼의 문구만으로 패치의 실행 차이를 판정하지 않았다. 기능별 후보 선정 순번·제외 이유·사전 예측과 두 판의 실제 경로는 모집 원장과 변경 원장에 있다. [frame.csv](frame.csv) · [editions.json](evidence/editions.json) · [changes.csv](changes.csv)

두 조건을 지지한 기능은 Paperless 계열 문서 목록 한 자리였다. 2023년 초의 선두 이슈 창은 대체 검색 요구의 희소성을 보여준다. 실제 요구형으로는 설명할 수 있는 근거이고 제품 전체에서 필요한 기능의 부재는 확인한 바 없다. 예를 들어 표본 외 darkroom 설정은 모듈 확장·접기 범위를 바꾸는 UI를 기록한다. 해당 설명도 원래 왼쪽 클릭 닫기 동작의 모든 조합을 입증하지 않는다. [고정 밖 darkroom 설정](https://github.com/darktable-org/dtdocs/blob/9427e1402fa49e5fa78eb138751b4a2e93664d36/content/preferences-settings/darkroom.md#L43-L50)

### Q2 · 질문 없이 편집한 메모와 판 근거

요구를 열기 전에 48개 영어 카드를 봉인했다. URL·제목·한 문장 용도·입력·출력·제한·판·원 절을 함께 남겼다. 광범위한 동작이 유지되는 두 판 12쌍은 원 설명을 재사용했고 한 판의 세부 조건이 달라지는 나머지 12쌍은 목차·절·발행 사건과 실제 코드를 연결했다. 48판의 메모는 고유 문장 36개다. 예전판 메모가 현재판에도 잘 맞는 대조로 darktable의 film roll과 image sequence, Sphinx의 Markdown 설정 등을 확인했다. [catalog.jsonl](catalog.jsonl) · [카드 봉인](evidence/cards-seal.json) · [darktable film rolls 원 절](https://github.com/darktable-org/dtdocs/blob/9427e1402fa49e5fa78eb138751b4a2e93664d36/content/lighttable/digital-asset-management/collections.md#L7-L13)

두 판에서 darktable의 highlight 재구성 문서 바이트가 같았다. 실제 5.6.2 코드는 4BAYER에서 clipping만 남기고 이전 편집도 변환한다. 문서와 이름에 의존하면 일반 Bayer의 복원 가능성을 네 색 CFA에도 붙일 수 있다. Sphinx의 같은 pyproject.toml 경로는 3.12에서 3.13으로 최소 Python 런타임을 옮겼다. DA-X2는 예상 파일을 찾지 못했고 두 실제 판의 colorspaces.c를 다시 확인했다. 이 경로 교정은 파일 이관 관측과 구별한다. [darktable 패치](https://github.com/darktable-org/darktable/commit/994efc3e5a048ed24355c21598541db2b233edb0) · [Sphinx #14762](https://github.com/sphinx-doc/sphinx/pull/14762)

### Q3 · 여섯 공개 요구와 두 언어

생성 UTC·번호 순으로 여섯 개의 앞 30개를 대조했고 30/31번째 경계 동시각은 0건이었다. 현재 공개 첫 게시물의 통과 번호는 Sphinx #11065, MkDocs #3085, Paperless #2300, darktable #13250, DuckDB #5816, GDAL #7010이다. 이슈 작성자 게시물 스냅샷의 동작·조건·브랜드 제외 표지·원문 위치가 있다. 최초 생성 순간의 본문이 현재와 같은지 0/6 확인됐으므로 표1 분모는 **스냅샷 조건부**다. #3085의 댓글 한 줄과 #7010의 댓글 편집 메타데이터가 보조 재열람에서 노출됐고 후속 구현 설명은 검색에 사용하지 않았다. 번역된 검색문은 같은 여섯 요청으로 유지했다. [issue-frame.csv](issue-frame.csv) · [queries.jsonl](queries.jsonl) · [노출 기록](evidence/issue-audit.md)

### Q4 · A, B, C가 다르게 한 일

원형에서 메모의 합성 토큰 `quartzleaf`는 저장 후 조회 0개였다. 같은 키를 제목에 보충하자 기존 URL의 동일 ID가 반환됐다. 별도 원형 `publish_answer`에서 budget 0은 discover를 생략하고 1·2·3을 각각 동일한 조회 상한으로 전달했다. 주 실험의 조사 12·표시 3은 별도다. A는 원형 SQL과 고정 관계를 실행했고 B는 토큰 집합에 메모만 합쳤다. 자연 요구에서 자동으로 추출된 원형 관계 키는 0개였으며 관계 경로를 사용한 대조는 원형 교정에 있다. C의 목적·버전 충돌은 동일 B 후보 내의 순서만 바꿨다. [교정 영수증](evidence/calibration.json) · [원형 Catalog](https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/catalog.py#L117-L145) · [원형 shortlist](https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/roundtrip.py#L93-L122)

C는 버전 확인과 목적의 참조 범위를 혼동할 수 있다. Q-SP가 지정한 Python 3.8은 **변환된 코드**의 호환성이다. C는 구문만 읽어 **빌더를 실행하는 인터프리터**의 최소 판과 비교했다. 실제론 후보 기능 자체가 다른 조작이므로 순위 하강은 맞는 효과였으나 판 근거의 적용 층은 틀렸다. 영어 Sphinx 최신 메타데이터는 B 2위에서 C 11위가 됐고 C의 새 3위도 충돌이었다. 한국어는 같은 세 오추천의 순서만 달라졌다. [봉인된 C 입력](tools/policy.py) · [행별 판별](ranks.csv)

### Q5 · 근거가 지지하는 조건과 다른 분야 대조

144기능–요구 행에 직접 1, 일부 6, 충돌 136, 미확인 1, 옛판만 0, 공석 0이다. 그 행에 직전·현행 판 판독 288개가 들어 있다. Q-PA의 읽기에서 자동 부여 태그는 수동 편집과 같은 Document.tags에 저장된다. 문서 목록이 태그 편집을 제공하며 `modify_tags`는 해당 조인 테이블을 문서 ID로 갱신한다. 자동 지정된 항목을 조작하는 코드 근거는 확인했고 실제 브라우저 사전 선택 표시는 미확인이다. GDAL info의 CRS 출력은 Q-GD 병행 cleanup을 입증하지 않는다. DuckDB Appender의 flush 시 제약 검사는 Q-DU의 중첩 람다 CHECK 바인딩과 별개다. [truth.csv](truth.csv) · [Paperless 자동 태그](https://github.com/paperless-ngx/paperless-ngx/blob/35b0439195bbdb87a6d519152e6782abe0720c3b/src/documents/signals/handlers.py#L246-L278) · [태그 편집](https://github.com/paperless-ngx/paperless-ngx/blob/35b0439195bbdb87a6d519152e6782abe0720c3b/src/documents/bulk_edit.py#L271-L317)

문헌 전거에서는 이명 표기와 별도 표목의 상호 참조가 다르다. Alice Sheldon의 두 발표 페르소나에 대해 실인물 한 ID로 모을 수 있어도 해당 필명으로 발표한 원 저작의 귀속을 합치면 요청에 따라 오답이 된다. 소프트웨어에서 같은 심벌 이름도 런타임 계약을 정하지 않는다. GNU ld와 glibc의 memcpy는 같은 이름의 여러 심벌 판을 구별했다. 옛 바이너리에 대한 호환 경로가 새 호출에도 겹치는 메모리 동작을 보장하지 않는다. 검색용 별칭과 인용의 판·적용 조건을 유지하는 설계 가설로 옮길 수 있다. [MARC](https://www.loc.gov/marc/authority/adtracing.html) · [Oregon Coll 455](https://archiveswest.orbiscascade.org/ark:/80444/xv02319) · [GNU ld VERSION](https://sourceware.org/binutils/docs/ld/VERSION.html) · [memcpy Caveats](https://man7.org/linux/man-pages/man3/memcpy.3.html#CAVEATS)

직접 열람한 고유 1차 저작 30개는 기능 원설계/규격 10/8, 독립 사용 게시물 6/6, 발행자 변경 원 사건 6/6, 분야 밖 전거·보존·호환 8/4다. 12개의 기능 변경 사건을 검토했으며 안전한 고유 산입은 프로젝트별 원 사건 1개씩으로 제한했다. 원장 450행에는 범위 조회, 같은 문서의 양판·절, 댓글 제외 본문, 번역, 실패, 사후 3건이 포함된다. 30과 합산하지 않았다. [sources.jsonl](sources.jsonl) · [대사](evidence/summary.json) · [판독·외부 대조](evidence/judgment-log.md)

### Q6 · 회수, 오추천과 동점

두 언어 모두 유일한 직접 적격 요청은 Q-PA다. 요청 5개의 적격 분모가 0이라 해당 recall을 산출할 수 없다. 영어는 A/B/C가 각각 고유 기능 1/1과 페이지 2/2를 반환했다. 한국어는 각각 0/1과 0/2다. 같은 기능의 현행·직전 페이지 둘을 반환하여 영어에서는 이미 두 표시 슬롯을 썼다. 한 기능을 두 성과로 합치지 않았다. 직접 적격의 A만/B만/C만은 각 0개다. [요청별 대사](evidence/summary.json)

영어의 표시 결과는 A가 직접 2·오추천 14·공석 2이고 B와 C는 직접 2·오추천 14·일부 2다. 영어에서 B가 채운 조사 슬롯은 26개에서 72개로 늘었지만 상위3의 새 직접 적격은 0개다. 한국어에서 A는 오추천 2·공석 16, B/C는 오추천 5·공석 13이다. 메모와 검색문의 단어 겹침이 같은 용도라는 증거는 아니다. Q-DA/en의 B 2위 ENVI 옛판은 `open`, `header`가 새로 맞았지만 지리 래스터를 파일 헤더와 함께 열며 UI의 편집 모듈 머리글과 충돌한다. A 조사 12위 안에 없던 후보가 B/C의 2위에 나타난 반례다. [실제 ENVI 절](https://github.com/OSGeo/gdal/blob/b40672525acf3f5c4f29d8541aa7dcff1e18eb92/doc/source/drivers/raster/envi.rst#L11-L39) · [ranks.csv](ranks.csv)

동점에서 마지막 ID 정렬을 역순으로 바꾸면 12변형 중 상위3 구성집합은 A 4, B 6, C 6변형에서 달라졌다. 직접 적격 기능 변경은 0이다. 12후보 경계 동점은 A 0, B 5변형이다. 메모에는 빈 슬롯을 줄인다는 효용과 후보 확인 비용을 늘린다는 대가가 함께 있었다. 인덱스 언어는 영어 48판뿐이다. Korean tokenizer 효과와 번역 카드 가치의 인과는 이 설계로 분리할 수 없다. [동점의 별도 조회](evidence/replay.json) · [영역·언어·판 분모](evidence/summary.json)

### Q7 · 준비, 조회, 재생과 판 교체

준비 문서 응답은 카드 근거 65회·2,046,749 B였다. 동일 내용 해시를 합치면 문서 46개·1,450,865 B다. 저장 카드 63,552 B, 메모 6,406자/6,406 B, 고유 문장 36개, 관계 4개, 적용판 판단용 별도 필드 574 B였다. 편집 손길의 수량 지표이며 실제 편집 노동 시간과 호스팅 비용은 미측정이다. SQLite 3.53.1, 페이지 4096 B, 캐시 –2048 KiB, DELETE journal에서 DB는 A→B 180,224→299,008 B, 단어표·색인은 90,112→208,896 B다. 단어 행은 514→1398이다. C는 B를 공유한다. [준비·측정 원장](evidence/replay.json)

두 빈 DB 세트에서 총 자연 72실행 행, 864조사 슬롯, Catalog.discover 48회와 678 SQL 문을 기록했다. C의 추가 Catalog/SQL은 0이다. 두 재생의 순위·동점·충돌 지문은 동일한 `ad71cc3c3696b642800d51bb9e70a17b6e35611f73ad7d596ca2ddb5a56ef303`이다. 동점 민감도는 별도 48회, 판 교체 합성 비교는 별도 12회다. 소규모 warmed-cache 관측의 경과 시간은 표3의 현재 실행으로 해석한다. [runs.jsonl](runs.jsonl) · [replay.json](evidence/replay.json)

보조층에서 카드 하나만 바꿨다. 직전 Sphinx의 Python 3.12 지원 확인판과 현행 3.13 최소판을 같은 입력으로 재생했다. 옛 인용의 SHA·행·문장은 교체 뒤 옛 DB를 재구성했을 때 다시 일치했다. 마침표 없이 끝나는 `Python 3.12`를 C가 읽으면 교체 전 1위와 교체 후 11위이고 B는 둘 다 1위다. 마침표가 붙으면 C가 버전을 못 읽고 교체 뒤에도 1위다. 마침표 대조는 정규식 실패 관측 뒤 추가한 보조 질문이며 자연 지표에 산입하지 않았다. 빌더의 실제 구동 대신 공개 배포 메타데이터를 검증했다. [교체 입력](evidence/replacement-input.json) · [재생 결과](evidence/replacement.json)

| 불일치·약점 | 다음 조사·직접 열 자료 | 어느 관측이면 판단이 바뀌나 |
| --- | --- | --- |
| 여섯 작성자 게시물의 최초 제출본 0/6이 미확인이다. | GitHub Issue `lastEditedAt`·`userContentEdits` 또는 생성 UTC 시간의 `IssuesEvent/opened`를 열어 우선 선두 1~3위와 선택 본문 해시를 대조한다. | 새로운 원본에서 앞자리의 두 조건 또는 선택 본문의 조건이 달라지면 그 요청과 적격·순위를 새 판으로 재생한다. |
| 단일 작업자의 순위 맹검이다. 직접 적격은 한 기능이고 브라우저 사전 선택은 미확인이다. | 새 판독자가 봉인 카드·요구와 원 절만 받아 144행을 봉인한다. Paperless 두 판의 테스트 배포에서 자동 태그가 붙은 문서를 목록에서 선택한다. | 두 조건에 대한 독립 불일치 또는 태그 편집 실패가 재현되면 해당 분모와 회수 판정을 갱신한다. |
| 영어 메모는 동명·일반 단어를 밀어 올렸다. C는 버전의 적용 층과 마침표를 혼동했다. | ENVI 헤더와 UI 머리글 대조, 종료 마침표 쌍, 질의 버전을 런타임/결과물로 나눈 별도 사전 봉인 평가를 실행한다. | 동명 오추천이 줄고 두 조건의 새 직접 적격이 늘며 문장부호 대조에서 순위가 같아지면 메모 증분과 재정렬의 채택 근거가 생긴다. |
