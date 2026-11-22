# AF-RES-037 · 선택 단위 반환 카드

각 행은 특정 설계 선택·근거 절·가져오면 안 되는 조건과 최대2개 링크다. 새 원리 발견 여부와 사용 가능한 선례를 분리한다. 표집 사건12개를 한 번씩만 둔다.

## 시점·용도 한정 선례

엄격 역사적 양성 대조는 A0/B0, 조건부 회수율은 해당 없음이다. B02만 표준 포함·기존 코드 기준을 사전 선언한 별도 검사에서 좁은 준수 대조 후보가 될 수 있다. A-G03는 기존 선택 설명이며 신규 변화 양성으로 쓰지 않는다.

| 사건 | 독립 부분·범위 | 도움이 되는 선택 | 근거 절 | 가져오면 안 되는 조건 | 근거 링크 | 판정 |
| --- | --- | --- | --- | --- | --- | --- |
| A-G03 | GDAL RFC73 CRS 축과 데이터 축 매핑 | 권위 있는 객체 정의를 유지한 채 데이터 표현 순서를 별도 매핑 | WKT2015 §7.5.5; RFC73 v2 축 매핑 | CRS 식별자를 유지하면서 규범 축 자체를 바꾸거나 모든 API의 기본 변경으로 확대하지 않음 | [근거1](https://docs.ogc.org/is/12-063r5/12-063r5.html) · [근거2](https://trac.osgeo.org/gdal/wiki/rfc73_proj6_wkt2_srsbarn?version=2) | C1 |
| B02 | GDAL RFC20 전체 정책 / 독립 GMLJP2 축 패치 | 파일 경계에서 권위 좌표 순서를 내부 데이터 순서로 변환 | GML §12.4.3.1·§9.1.3.1; 패치13570 | 격자 방향·지리 위치를 바꾸거나 모든 CRS·전체 RFC20에 일반화하지 않음 | [근거1](https://docs.ogc.org/bp/03-105r1/03-105r1.zip) · [근거2](https://github.com/OSGeo/gdal/commit/bef1fa8ffa1d445f0f6c64a970000d0138e17dcd) | C1 |

## 유사 오답

| 사건 | 독립 부분·범위 | 도움이 되는 선택 | 근거 절 | 가져오면 안 되는 조건 | 근거 링크 | 판정 |
| --- | --- | --- | --- | --- | --- | --- |
| A-C01 | CSSWG #2155 표 머리글 sticky | 표 sticky에서 규범 허용과 브라우저 지원을 분리 | CSS Position 3 L725–790; Mozilla 975644 c48 | 기존 허용 규칙을 새로운 원리 도입으로 세거나 전체 브라우저에 일반화하지 않음 | [근거1](https://github.com/w3c/csswg-drafts/blob/85d366602c156b1735da30d99b68f3fe0908ed60/css-position-3/Overview.bs) · [근거2](https://bugzilla.mozilla.org/show_bug.cgi?id=975644#c48) | C1 |
| A-C02 | CSSWG #2156 unknown -webkit pseudo-element 파싱 | legacy 입력의 파싱 수용과 미지원 의미 실행을 분리 | #2156 2018-04-19 발언; 2940a79 부록B | 다른 분야 발견이나 모든 unknown selector 허용으로 확대하지 않음 | [근거1](https://github.com/w3c/csswg-drafts/issues/2156#issuecomment-382833720) · [근거2](https://github.com/w3c/csswg-drafts/commit/2940a794c64763ce10adb18292aac1611e2be2a1) | N |
| A-C03 | CSSWG #2157 :nth-column 이름 변경 | 기존 용어를 API에 옮길 때 실제 선택 대상을 먼저 확인 | #2157 회의 댓글; f4c6cef 명세 | col 요소와 논리 열의 셀을 동일시하지 않음 | [근거1](https://github.com/w3c/csswg-drafts/issues/2157#issuecomment-355169539) · [근거2](https://github.com/w3c/csswg-drafts/commit/f4c6cefb850d1b700202d7a7e333fe57bff3212c) | C1 |
| A-C04 | CSSWG #2158 ::slotted 단일 인자 | 구현 제약 때문에 문법을 줄일 때 결정과 후속 명세화를 구별 | Servo PR19610; Scoping cec815f | 후속 표준 인용을 선행 구현의 원인으로 연결하지 않음 | [근거1](https://github.com/servo/servo/pull/19610) · [근거2](https://github.com/w3c/csswg-drafts/commit/cec815f404674408bfd0669908d92a975bacfa1c) | C1 |
| A-G01 | GDAL RFC71 저장소 이전 | 이전할 때 이슈 번호 권위와 PR 관계 보존 비용을 따로 확인 | RFC71 Details; 완료 메일 | 백업·위키·과거 티켓 전체 이관까지 완료했다고 읽지 않음 | [근거1](https://trac.osgeo.org/gdal/wiki/rfc71_github_migration?version=1) · [근거2](https://lists.osgeo.org/pipermail/gdal-dev/2018-March/048296.html) | C1 |
| A-G02 | GDAL RFC72 pytest 전환 | 시험 도구 도입 시 실행·미실행과 격리 단위를 명시 | RFC72 Phase1; ASAN script L49–66 | 포팅을 시험 독립성 확보나 C API 직접 검증으로 확대하지 않음 | [근거1](https://trac.osgeo.org/gdal/wiki/rfc72_pytest?version=1) · [근거2](https://github.com/OSGeo/gdal/blob/59d0840b1980d1a1a84701b6dae5fc5c78e999f5/gdal/ci/travis/gcc52_stdcpp14_sanitize/script.sh) | C1 |
| A-G04 | GDAL RFC74 Sphinx 문서 이관 | 문서 플랫폼 결정에서 선행 작업·공식 승인·배포 범위를 분리 | RFC74 v1; May23 완료 메일 | 번역·전체 redirect까지 반영됐다고 확대하지 않음 | [근거1](https://trac.osgeo.org/gdal/wiki/rfc74_sphinx?version=1) · [근거2](https://lists.osgeo.org/pipermail/gdal-dev/2019-May/050273.html) | C1 |
| B04 | Knuth의 수학적 글자 설계와 역사 자료 독서 | 역사적 유사성을 발견했을 때 원래 설계 선택의 선후를 점검 | Mathematical Typography 미러 pp350–354; 원 발행자 재확인 필요 | 놀람·인용을 설계 변경의 원인이나 전체 TeX/METAFONT의 기원으로 세지 않음 | [근거1](https://www.ams.org/journals/bull/1979-01-02/S0273-0979-1979-14598-1/S0273-0979-1979-14598-1.pdf) · [근거2](https://blog.typekit.com/wp-content/uploads/2013/09/knuth79.pdf) | C1/U |

## 보류

| 사건 | 독립 부분·범위 | 도움이 되는 선택 | 근거 절 | 가져오면 안 되는 조건 | 근거 링크 | 판정 |
| --- | --- | --- | --- | --- | --- | --- |
| B01 | pdfTeX의 미세 조판 기능 | 공백만으로 고른 문단을 만들기 어려울 때 줄바꿈 보존·변경 모드를 선택 | Thành §4; Wild §2 | 합자·약자·대체 활자를 무조건적인 글리프 폭 확대와 동일시하지 않음 | [근거1](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf) · [근거2](https://www.numdam.org/article/CG_1995___22_5_0.pdf) | C2/R |
| B03 | LilyPond Feta 음악 글꼴 교체 | 음악 글리프를 설계할 때 실제 판각 본보기와 연주 가독성 조건을 확인 | 1.0.1 ANNOUNCEMENT·fonts.doc; Essay §1.2 | 출판사 이름만으로 특정 판의 규칙을 추정하거나 글리프·spacing·크기를 한 변경으로 합치지 않음 | [근거1](https://lilypond.org/download/sources/v1.0/lilypond-1.0.1.tar.gz) · [근거2](https://lilypond.org/doc/v2.26/Documentation/essay/engraving-details) | C2 |

## 사용 조건

새로 찾은 대상은12개지만 저자가 당시 처음 알게 된 원리로 확정한 수는0이다. 미확인은 부재가 아니며, 이 카드는 검색 성능 측정 결과가 아니다. B04는 원 발행본 접근 실패와 미러 여부를 유지하고 양성 대조로 쓰지 않는다.
