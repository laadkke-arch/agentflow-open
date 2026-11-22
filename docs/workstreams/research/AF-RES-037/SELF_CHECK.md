# AF-RES-037 · 자체 점검

**정해진 표집의 조사·기록을 마쳤지만 수용 조건 일부는 미충족이다.** 엄격 사슬0은 허용되는 관측 결과이며 실패 조건으로 만들지 않았다. 원전 열람 공백·완전 비노출 실패·엄격 반례의 미확인은 별도로 남긴다.

## Q1–Q7 대조

| 질문 | 판단·확인 범위 | 직접 근거·위치 | 반대 근거 | 남은 미확인 |
| --- | --- | --- | --- | --- |
| Q1 · partial | CSS/GDAL 각4 최초 실질 제안을 복원하고 선택·제외·중복·노출을 고정. 완전 결말 비노출은7/8. | [CSS-001](https://github.com/w3c/csswg-drafts/issues/2155) issues.opened Message-ID; body paragraphs 1–3, web lines 19–25 (`sources.jsonl` L1); [CSS-002](https://github.com/w3c/csswg-drafts/issues/2156) issues.opened Message-ID; body web lines 19–50, especially final two alternatives (`sources.jsonl` L2); [CSS-003](https://github.com/w3c/csswg-drafts/issues/2157) issues.opened Message-ID; body web line 19 (`sources.jsonl` L3) | [CSS-007](https://github.com/w3c/csswg-drafts/issues/2157) comments355108465,355117753,355169539; complete API comments page of3 (`sources.jsonl` L7); [CSS-020](https://bugzilla.mozilla.org/show_bug.cgi?id=1425757) description; c2–c5; rule-hash reason, requested spec issue, landed Servo19610 link (`sources.jsonl` L20) | A-C03의 우발 결의 스니펫 노출; 명칭 변경의 포함 경계. 최초판8은 복원됐으나 전체 설계자의 지식은 미확인. |
| Q2 · partial | 고정3분야 쿼리·각 최초10 결과에서 round-robin 4후보 추적. A/B 동일 사건0. B04 원 발행자 본문 미확보. | [B-S06](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf) thesispp5,7,13–14,24,31,36–38,115–118; incidental appendixpp111–113 (`sources.jsonl` L96); [B-S07](https://gdal.org/en/stable/development/rfc/rfc20_srs_axes.html) Summary; Dilemma; The Hack; New methods; importFromEPSG; OGRCoordinateTransformation; webL13–95 (`sources.jsonl` L97); [B-S11](https://lilypond.org/doc/v2.26/Documentation/essay/engraving-details) Essay§1.2 paragraph naming publishers, webL9; footnoteL19–20 (`sources.jsonl` L101) | [B-S13](https://www.ams.org/journals/bull/1979-01-02/S0273-0979-1979-14598-1/S0273-0979-1979-14598-1.pdf) original PDF request403 (`sources.jsonl` L103); [B-S35](https://i.stanford.edu/pub/cstr/reports/cs/tr/78/648/CS-TR-78-648.pdf) requested full report; HTTP503 (`sources.jsonl` L125) | B04 발행자/기관 본문; B01 핵심 hz와 B03 악보 판은 확인되지 않음. 미러를 최소수에 산입하지 않음. |
| Q3 · partial | 12사건의 P/V/I/A와 최초안·연결·변경·반영을 분리. 시간 공백과 날짜 종류를 보존. | [ROOT-P01](https://docs.ogc.org/is/12-063r5/12-063r5.html) §7.5.5 Axis order; web lines998–1008; front matter lines2–32 (`sources.jsonl` L135); [ROOT-P08](https://docs.ogc.org/is/05-047r3/05-047r3.pdf) §7.7 p22; §7.2 pp10–11; AnnexC.5 pp59–60; contributors p.vii (`sources.jsonl` L156); [ROOT-P10](https://docs.ogc.org/bp/03-105r1/03-105r1.zip) ZIP memberGML-3.1.1/GML-3.1.pdf §12.4.3.1 printedp117/PDF139; §9.1.3.1,9.1.4.1; coordinateSystems.xsd L125,142; geometryBasic0d1d.xsd L413–415,475–477 (`sources.jsonl` L159) | [ROOT-P02](https://docs.ogc.org/as/18-005r4/18-005r4.html) §10.1,10.4; web lines1390–1393,1448–1470; revision table lines63–70 (`sources.jsonl` L136); [CSS-021](https://github.com/servo/servo/pull/19610) components/selectors/parser.rs hunks215,769,1864,2496; matching.rs hunk555; style/selector_map.rs hunk415 (`sources.jsonl` L21) | 역사 검색색인·저자 첫 독서일12건 미확인. B03 mtime는 공개일 증명 아님. 원문 접근 실패를 서지로 메우지 않음. |
| Q4 · met_with_recorded_unknowns | 입력·동일 객체·권한·상태 전후·출력 제약을 사건별로 대응. B02의 원안 기준과 코드 기준을 분리. | [GDAL-003](https://trac.osgeo.org/gdal/wiki/rfc73_proj6_wkt2_srsbarn) Motivation/WKT2/WGS84 Pivot; OGRSpatialReference rewrite; Axis order issues; Backward compatibility; initial v2 text L146–251 (`sources.jsonl` L24); [GDAL-C73SRS](https://github.com/OSGeo/gdal/blob/ab9e80368ef662712c963191fd86fde2c5b75600/gdal/ogr/ogrspatialreference.cpp) L117–118,L286–394,L1325–1387,L10344–10413 (`sources.jsonl` L75); [B-S20](https://trac.osgeo.org/gdal/ticket/2131) description; #comment:1; #comment:2; #comment:3 (`sources.jsonl` L110) | [CSS-007](https://github.com/w3c/csswg-drafts/issues/2157) comments355108465,355117753,355169539; complete API comments page of3 (`sources.jsonl` L7); [ROOT-C02](https://www.numdam.org/article/CG_1995___22_61_0.pdf) §1.1–1.3 pp63–66; §4.1–4.4 p75; webL64–154,372–396 (`sources.jsonl` L144) | 정확한 타 분야 원전과 같은 기준선의 인과 변경을 결합한 strict 사슬은0. B04 mapping은 미러의 제한된 근거. |
| Q5 · met_with_recorded_unknowns | 같은 목적의 고정 명세·코드·시험·공지와 미반영 범위를 추적. A후속반영7/8, B정적반영3/4; 역사 실행0. | [CSS-010](https://github.com/w3c/csswg-drafts/commit/f4c6cefb850d1b700202d7a7e333fe57bff3212c) selectors-4/Overview.bs diff hunks L478,L3143,L3180,L3197,L3759 (`sources.jsonl` L10); [CSS-011](https://github.com/w3c/csswg-drafts/commit/cec815f404674408bfd0669908d92a975bacfa1c) css-scoping-1/Overview.bs diff L259,L321,L360; ::slotted grammar and argument matching (`sources.jsonl` L11); [CSS-013](https://github.com/web-platform-tests/wpt/pull/12673) merged PR metadata; compat/webkit-pseudo-element.html L9–45 (`sources.jsonl` L13) | [CSS-016](https://bugzilla.mozilla.org/show_bug.cgi?id=975644) c0 prerequisite constraints; c47/c48 commits landed2017-12-21/22; c39 test report; c53 table-parts scope (`sources.jsonl` L16); [GDAL-M049658](https://lists.osgeo.org/pipermail/gdal-dev/2019-January/049658.html) dated message header and unquoted message body; 049658 (`sources.jsonl` L63) | C01의 실제 페이지 변경, B04의 특정 구현, 모든 역사 런타임. 서로 다른 하위기능·버전의 인과를 합치지 않음. |
| Q6 · partial | 네 반례 목표 모두 추적. 객체 혼동·시간 역전은 직접 관측, 독립 원리 발명과 확정 채택 전 공급자 포기는 미확인. | [CSS-007](https://github.com/w3c/csswg-drafts/issues/2157) comments355108465,355117753,355169539; complete API comments page of3 (`sources.jsonl` L7); [CSS-021](https://github.com/servo/servo/pull/19610) components/selectors/parser.rs hunks215,769,1864,2496; matching.rs hunk555; style/selector_map.rs hunk415 (`sources.jsonl` L21); [GDAL-M049649](https://lists.osgeo.org/pipermail/gdal-dev/2019-January/049649.html) dated message header and unquoted message body; 049649 (`sources.jsonl` L61) | [ROOT-P10](https://docs.ogc.org/bp/03-105r1/03-105r1.zip) ZIP memberGML-3.1.1/GML-3.1.pdf §12.4.3.1 printedp117/PDF139; §9.1.3.1,9.1.4.1; coordinateSystems.xsd L125,142; geometryBasic0d1d.xsd L413–415,475–477 (`sources.jsonl` L159); [C4-RFC72-V1](https://trac.osgeo.org/gdal/wiki/rfc72_pytest) Plan Phase1; cached complete text L71 (`sources.jsonl` L160) | 알고리즘 독립 구현을 원리 독립 발명으로 바꾸지 않음. RFC72 최초 CI 코드가 이미 sugar-off여서 활성→철회 사슬 미확인. |
| Q7 · met | 12카드·세 묶음·카드당 최대2링크. strict 적격 A0/B0이면 조건부 회수율 해당 없음. 코드 기준 감도 B02는 별도. | [GDAL-003](https://trac.osgeo.org/gdal/wiki/rfc73_proj6_wkt2_srsbarn) Motivation/WKT2/WGS84 Pivot; OGRSpatialReference rewrite; Axis order issues; Backward compatibility; initial v2 text L146–251 (`sources.jsonl` L24); [B-S18](https://trac.osgeo.org/gdal/wiki/rfc20_srs_axes?version=1) Summary, WKT Axis Representation, Dilemma; 2457-byte plaintext (`sources.jsonl` L108); [B-S20](https://trac.osgeo.org/gdal/ticket/2131) description; #comment:1; #comment:2; #comment:3 (`sources.jsonl` L110) | [B-S26](https://lists.osgeo.org/pipermail/gdal-dev/2011-June/028981.html) lines30–43; reply to Flo Ledermann (`sources.jsonl` L116); [B-S40](https://blog.typekit.com/wp-content/uploads/2013/09/knuth79.pdf) pp350–354,360–361; refs20,51 (`sources.jsonl` L130) | 검색 실험은 하지 않아 회수율·새 원리 발견 성능 미측정. 조건부 B02 준수 대조를 strict 새 학습 양성으로 사용하지 않음. |

JSON 수용 원장은 각 질문의 전체 source ID·직접 URL·locator·정확한 원장 행을 포함한다. 위 표는 주요 근거만 표시한다.

## 수용 조건

| 조건 | met | 분자/분모 | 부족한 이유 또는 범위 |
| --- | --- | --- | --- |
| AC01 · 계획/배정 SHA·환경·독립 경로·선행 입력 고정 | true | 1/1 | 없음 |
| AC02 · A 각 원장 최대40 내 결정 우선8선정·최초판복원 | true | 8/8 | 없음 |
| AC03 · A 최초판 동결 전 완전한 후속 결말 비노출 | false | 7/8 | A-C03 선정 뒤 최초판 복원 검색에서 후속 결의 스니펫이 보임. 사례 교체 없이0/7감도를 추가. |
| AC04 · B 최소2분야·고정쿼리별 최초10·4후보 추적 | true | 4/4 | 없음 |
| AC05 · B 네 후보 모두 원 발행자/기관 초기 수신 본문 직접 열람 | false | 3/4 | B04 AMS403·Stanford503. Typekit 미러는 읽었으나 최소수/원 발행본 조건에 산입하지 않음. |
| AC06 · B 인과의 핵심 제공 원전 접점을 모두 직접 복원 | false | 1/4 | B02 기술 준수 원전만 좁게 연결. B01 hz1993, B03 정확한 악보 판, B04 Goudy/Zapf 원전과 원 수신본 미확인. Wild·MPA·MOLA로 대체하지 않음. |
| AC07 · 외부 고유1차 원문 최소24 | true | 49/24 | 없음 |
| AC08 · A 최초 수신 원문8 | true | 8/8 | 없음 |
| AC09 · 날짜·판 있는 제공 분야 운영규칙/설계서6 | true | 10/6 | 총량은 충족. 제공 규칙10은 실제 인과 donor10이 아니며 사건별 원전 공백은 별도. |
| AC10 · 수신 후속 결정·반영6 | true | 15/6 | 없음 |
| AC11 · 독립 반대·제약 기록4 | true | 10/4 | 없음 |
| AC12 · 원문별 필수키·URL·판/위치·한계·실패·고유작품 처리 | true | 168/168 | 없음 |
| AC13 · A/B 모든 추적·탈락·미심사 및 중복 처리 복원 | true | 219/219 | A/B 중복0. B 첫10 30행과 상한밖73행, GDAL 경계71행은 선정 분모와 구별. |
| AC14 · 12사건 사슬 접점에 직접 근거 또는 미확인/실패 영수증 | true | 12/12 | 없음 |
| AC15 · 출판·당시공개·역사색인·저자읽기 및 신규대상/신규인지 분리 | true | 12/12 | 역사 검색색인·첫 독서의 미확인을 보존했다는 조건의 충족이며 값 자체가 확인됐다는 뜻이 아님. |
| AC16 · 객체·권한·전후·범위·세 관점 및 반영/미반영 표시 | true | 12/12 | 없음 |
| AC17 · 네 반례 목표의 반대 기록 탐색·조건 기록 | true | 4/4 | 없음 |
| AC18 · 다른 분야 원리 자체의 독립 발명 반례를 직접 확정 | false | 0/1 | 알고리즘 독립 구현은 확인했으나 원리의 독립 발명으로 확대할 수 없음. 새 사례로 표집을 교체하지 않음. |
| AC19 · 확정된 타 분야 채택을 공급자 제약으로 반영 전 새로 포기한 사슬 | false | 0/1 | 조건부 CI 제외·기존 포맷 호환성 제한은 확인. sugar-enabled 이전 상태와 공급자 실패→철회 사슬 미확인. |
| AC20 · 엄격/회고 기준·동일 사건 코드 감도·적격0 처리 분리 | true | 25/25 | 없음 |
| AC21 · 사건별 선택/절/금지조건과 최대2링크의 카드 | true | 12/12 | 없음 |
| AC22 · RESULT 제목 직후 필수표1·표2 및 전체 사건 | true | 2/2 | 없음 |
| AC23 · 마지막 동순위 약점3개와 각각 다음 첫 자료·전복조건 | true | 3/3 | 없음 |
| AC24 · 재계산·CSV 독립 파싱·추적키 결합 검사 | true | 3/3 | 없음 |

## 실제로 수행한 점검

- `python -B docs/workstreams/research/AF-RES-037/evidence/rebuild.py --check`: 원 stream·정정·해석 플래그에서 산출 CSV/JSON의 내용 일치를 점검한다. 사슬 완결과 분모를 상수로 고정하지 않는다.
- `evidence/verify-csv.mjs`: 기본 runtime의 Artifact Tool로 CSV3개를 독립 import, 219/12/25행과 ID 결합·해석별 행을 검사했다. JSON 영수증의 파일 해시와 실제 파일이 일치해야 한다.
- `evidence/validate.py`: 원문 고유성·범주 수·source 참조·두 표의 순서/행·마지막3행·카드 링크 수·허용 경로를 검사한다. 결과 영수증은 `evidence/validation.json`이다.

## 실행하지 않은 검사와 경계

역사적 GDAL·pdfTeX·LilyPond·browser 실행은 하지 않았다. 정적 코드/시험·당대 작성자 보고를 연구자의 실행 성공으로 바꾸지 않았다. 확인한 현재 환경과 버전 차이, 고정 입력·재개 명령은 `streams/b/followup.json`, `streams/gdal/case-analysis.md`에 있으며 최종 HANDOFF에 다시 모은다. 미확정 의존성 SHA는 미확인으로 둔다.

## 커밋 뒤에 수행할 종료 순서

RESULT와 수용 파일을 원격에 커밋한 뒤 그 고정 SHA에서 두 파일을 다시 열고 `python -B -m workbench.session check docs/workstreams/research/AF-RES-037/manifest.json --fetch`를 실행한다. 이 시점의 결과를 아직 실행한 것으로 표시하지 않는다. 실제 명령 출력·고정 SHA·파일 해시·마지막 HANDOFF 별도 커밋은 HANDOFF에 기록한다.

## 첫 결론에 반하는 자료까지 읽었는가

그렇다. 기존 규칙 설명이라는 해석 뒤 B02의 실제 패치·시험과 B03의1998 초기 변경 진술을 찾아 긍정 범위를 보강했다. 반대로 GML 규칙 부재라는 설명은 원 규범을 회수해 수정했고, CI 공급자 제약의 포기 사례는 최초 코드가 이미 off여서 엄격한 철회로 셀 수 없음을 확인했다. 원값·새 근거·분모 영향은 protocol-amendments와 review 파일에 보존했다. 엄격 양성0을 맞추기 위해 실제 변화를 삭제하지 않았다.
