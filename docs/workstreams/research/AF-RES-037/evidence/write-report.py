#!/usr/bin/env python3
"""Create the requested report/card views from the committed research decisions."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
cases = json.loads((ROOT / "evidence/case-decisions.json").read_text())
recount = json.loads((ROOT / "evidence/recount.json").read_text())
weaknesses = json.loads((ROOT / "evidence/weaknesses.json").read_text())


def esc(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"] + ["| " + " | ".join(esc(x) for x in row) + " |" for row in rows])


donors = {
    "A-G03": "[WKT2015 §7.5.5](https://docs.ogc.org/is/12-063r5/12-063r5.html); [WCS2 §6.3](https://docs.ogc.org/is/09-110r4/09-110r4.pdf). WCS core는 당시 관련 규범이며 원안의 GeoServer 문서 자체와 구별.",
    "B01": "[Wild1995 §2 pp12–14](https://www.numdam.org/article/CG_1995___22_5_0.pdf): 저자가 인용했지만 작동이 다름. 핵심 hz1993 본문 미확인.",
    "B02": "[GML3.1.1 §12.4.3.1·§9.1](https://docs.ogc.org/bp/03-105r1/03-105r1.zip); [GMLJP2 §7.7](https://docs.ogc.org/is/05-047r3/05-047r3.pdf)",
    "B03": "미확인: 명명된 인쇄 악보의 정확 판·본문. MPA1993·MOLA2017은 비교 원문이며 해당 빈칸을 대신하지 않음.",
    "B04": "미확인: Goudy1940·Zapf1970 원전. 서지·미러만으로 원전 열람을 대신하지 않음.",
}
rows1 = []
for c in cases:
    reflection = c["implementation_scope"]
    if c["implementation_url"] != "미확인":
        reflection = f"[고정 기록]({c['implementation_url']}) — " + reflection
    else:
        reflection = "미확인 — " + reflection
    judgment = c["strict_code"]
    if c["case_id"] == "B02":
        judgment += "; 코드 기준 감도만 준수 사슬1"
    rows1.append([c["stratum"], c["case_id"] + " · " + c["decision_unit"], c["purpose"] + "; " + c["before_choice"], c["donor_description"], donors.get(c["case_id"], "타 분야 제공 원문 미관측; 같은 분야 근거는 chains.csv에 보존"), f"[연결 기록]({c['connection_url']}) · {c['connection_date']}", c["after_choice"] + "; " + c["changed_part"], reflection, judgment, "; ".join(c["unknowns"])])
head1 = ["층", "사건 ID", "원래 목적·기존 선택", "타 분야 원리·행위자", "당시 원문 URL·절", "연결 발언 URL·날짜", "달라진 선택", "같은 목적 반영 URL·범위", "판정", "미확인"]
rows2 = []
for r in recount["table2_rows"]:
    a = r["stratum"] == "A"
    relaxed = r["interpretation"].startswith("retrospective")
    label = r["stratum"] + (" · 회고·유추 허용, 같은 원안 기준" if relaxed else " · 명시 인과, 고정 원안 기준")
    changes = str(r["explicit_change_confirmed"])
    if not a:
        changes += " (B01 회고 + B03 초기 진술)" if relaxed else " 진술 (B03; 고정 원안 전후 미확인)"
    else:
        changes += " (연결 미관측·기존 선택 설명)"
    rows2.append([label, r["unique_cases"], f"{r['contemporary_source_confirmed']} 확인 / {r['unique_cases']-r['contemporary_source_confirmed']} 미확인", f"{r['author_citation_primary_confirmed']} 확인 / " + ("7 미관측" if a else "1 미러만"), changes, f"{r['actual_reflection_confirmed']} 정적 확인 / " + ("1 기존 구현만" if a else "1 미확인"), r["complete_chain"], "0 (B02 기준선 혼합 정정은 별도)" if not a else "0"])
rows2.append(["B · 별도 감도: 표준 포함 + 기존 코드 기준", 4, "1 확인 / 3 미확인", "3 확인 / 1 미러만", "2 (B02 코드 + B03 글꼴)", "3 정적 확인 / 1 미확인", "1 — B02의 독립 GMLJP2 부분", "0; 기준선 변경을 공개"])
head2 = ["층·조건", "고유 사건", "당대 가용", "작성자 인용", "명시적 선택 변경", "실제 반영", "사슬 완결", "반증 시 뒤집힌 수"]

body = r'''
## 결과와 집계의 뜻

**사전 고정한 원안 기준의 엄격 사슬은 A 0/8, B 0/4다.** B02에서는 실제 코드가 바뀌었다. 그러나 복원한 최초 RFC20은 이미 외부 축 순서와 호환성 정책을 제안하므로, 그 뒤의 표준 인용을 새로 바뀐 원안으로 세지 않았다. 지도 인터페이스 표준을 제공 분야로 포함하고 비교 기준선을 기존 실행 코드로 옮기면, 같은 B02 안의 GMLJP2 패치 사슬 1건을 별도 감도로 인정할 수 있다. 표집 사건은 여전히12개이며 이 결과를 열세 번째 사건으로 더하지 않는다. [RFC20 최초판](https://trac.osgeo.org/gdal/wiki/rfc20_srs_axes?version=1), [작성자 발언](https://trac.osgeo.org/gdal/ticket/2131#comment:1), [고정 패치](https://github.com/OSGeo/gdal/commit/bef1fa8ffa1d445f0f6c64a970000d0138e17dcd)가 그 구분의 직접 근거다.

필수 표1은 전체12개 사건, 필수 표2는 두 해석 기준과 별도 감도다. 각 열은 **서로 독립된 접점 확인 수**다. 예컨대 명세·구현 반영이 있어도 타 분야 출처의 인과가 확인되지는 않는다. A의 반영7은 C02/C03/C04/G01/G02/G03/G04이며 C01은 기존 구현만 확인했다. C03/C04의 후속 명세 변경은 실제 브라우저 실행과 구별한다. B의 반영3은 B01/B02/B03의 정적 문서·코드·시험 정의다. 실행한 역사적 프로그램 시험은0건이다.

‘당대 가용’의 확인은 특정 관련 원문을 당시 사용할 수 있었다는 근거이며, 정확한 최초 독서나 검색색인 기록을 뜻하지 않는다. A-G03과 B02만 해당 접점을 확인했다. 나머지는 해당 사슬의 정확한 제공 원전 접점이 미확인인 상태다. B01은 인용된 Wild의 선행 발행을 확인했지만 폭 확장 선택의 직접 매개인 hz 원문은 미확인이라 그 열을 확인으로 채우지 않았다. B03의 초기 변경 진술은 실제 소스에 있으나 archive 파일 날짜가 공개일을 확정하지 않는다. `chains.csv`는 출판 P·당시 공개 V·역사 색인 I·저자 인용 A를 별도 열로 보존한다. 당시 검색색인과 저자의 첫 노출 시각은12건 모두 완결 확인되지 않았다.

‘명시적 선택 변경’ 열은 **저자가 출처와 두 상태의 변화를 직접 연결한 진술**의 확인 수다. B03의1998 발표문은 기존 글꼴→Feta라는 초기 저자 진술이며, 복원된 고정 원안→수정안의 비교가 아니다. 그래서 진술1은 세되 사슬 완결은0이다. B01의2000 회고는 넓은 해석에서만 추가한다. `judgments.csv`는 이 진술 플래그와 `changed_same_baseline_confirmed`를 분리하고, 완결 수는 정확한 원리·당대 가용·저자 연결·동일 기준선 변경·반영을 모두 만족할 때만 계산한다.

반증 뒤집힘0은 **동일 기준·범위의 기존 C3 판정을 반증 때문에 취소한 사건 수**다. 세부 설명을 고친 일이0이라는 뜻이 아니다. B02의 잠정 stream이 코드 기준을 원안 기준과 혼합한 정정1건, GML 규칙이 없다는 잠정 설명을 원문으로 바로잡은 검토 정정, 시험 revision의 오기 복원을 각각 기록했다. `evidence/protocol-amendments.jsonl` AM07–11과 두 독립 검토 파일에서 전값·사유·분모 영향을 확인할 수 있다.

## Q1·Q2 — 어떤 사건을 먼저 보았는가

`SCOPE.md`를 먼저 고정하고 최초판 묶음을 원격 `7a33c17be2d25b2c1936038205187e8108bf4482`에 봉인한 뒤 별도 후속 기록을 읽었다. CSSWG는 2018–2024 생성 issue를 created ascending·번호 ascending으로 조회한 최초40 metadata 중 첫4개가 행동·대안 적격이었다. 36개는 미심사이며 탈락으로 세지 않는다. 네 최초 본문은 W3C의 동일 저자 `issues.opened` 알림으로 복원했다. 현재 #2157 본문에 추가된 문장과 #2158 제목의 후속 `:host`는 초기 범위에 넣지 않았다. [#2157 최초 알림](https://lists.w3.org/Archives/Public/public-css-archive/2018Jan/0020.html), [#2158 최초 알림](https://lists.w3.org/Archives/Public/public-css-archive/2018Jan/0033.html).

#2157은 공개 selector의 이름·문법 대안이므로 포함했다. 다만 선정 뒤 최초판을 복원하던 검색에서 후속 결의 스니펫이 우발적으로 보였다. 완전한 결말 비노출 조건은 **7/8**이다. 명칭 변경을 설계 사건에서 제외하거나 이 노출을 이유로 제외하는 감도는 A **0/7**이며 다음 순위 사례로 바꾸지 않았다. 초기안의 출처명과 제목의 제공자 노출도 그대로 유지했다. `frame.csv`와 `streams/csswg/method.md`에 순서·사유·노출이 있다.

GDAL은 최초 **실질 번호 RFC**를 단위로 삼았다. 선택은 RFC71·72·73·74이며, 번호73 v1은 제목뿐이라 행동·대안이 없어 보존한 뒤 v2를 최초 실질판으로 삼았다. 이 해석은 v2를 읽기 전에 AM01로 기록했다. 번호72의 더 이른 PR, 번호74의 선행 sprint, 번호73의 squash author date를 번호 RFC의 생성일과 섞지 않았다. 기간 내 접두부는 실질4건과 제목 자리표시자1건으로 상한40 이내다. 기간 경계 확인71행은 별도다. 초기15개 실패 URL은 한 번의 낮은 병렬도 재시도로 모두2018년 이전 생성일을 확인했다. 전체 GDAL frame76행과 이전 실패값이 남아 있다. [RFC73 v1](https://trac.osgeo.org/gdal/wiki/rfc73_proj6_wkt2_srsbarn?version=1), [v2](https://trac.osgeo.org/gdal/wiki/rfc73_proj6_wkt2_srsbarn?version=2).

B는 사전 영어 검색어3개·기본 relevance·각 최초10을 보존했다. 인쇄1→지도1→음악1→인쇄2의 round-robin으로 **typography5=B01, cartography1=B02, music4=B03, typography6=B04**를 골랐다. 첫10이30행이며 도구가 더 반환한73행도 상한 밖 미심사로 보존했다. batched 검색의 결과 소속이 섞인 문제는 본문 선정 전에 같은 쿼리를 각각 다시 실행해 교정했다. B의 회고 서술·검색 스니펫 노출은 이 경로의 특성이며 A의 비노출 조건과 같은 것으로 주장하지 않는다. 원문 접근이 막힌 B04도 다른 후보로 교체하지 않았다. 세 분야를 포함했고 A/B 동일 사건은0이다. RFC20과 RFC73은 같은 프로젝트의 서로 다른 결정이다.

따라서 통합 `frame.csv`는219행(CSS40+GDAL76+B103)이며 실제 선정은12행이다. 이전017의40사건·기원7경로,022의33사건,033의수신8·제공18과 사건/저작 단위로 대조했다. 같은 프로젝트라는 이유만으로 다른 결정을 제외하지 않았다. `evidence/prior-exclusions.json`이 입력 SHA와 제외 원장이다. 기존 BM25·200토큰 창·기원7경로·과거 성공률은 재실험하지 않았다. 이 접두부와 B의 발견 경로는 자연 발생 채택률의 표본이 아니다.

## Q3 — 시점을 연결했을 때 남는 빈칸

| 사건 | 선행 원문·공개 근거 | 저자 연결과 선택 | 반영·남은 시간 공백 |
| --- | --- | --- | --- |
| A-C04 | [2017-12-17 버그](https://bugzilla.mozilla.org/show_bug.cgi?id=1425757#c0)의 소프트웨어 최적화 | [Servo PR19610](https://github.com/servo/servo/pull/19610)이2017-12-20 병합; CSS 최초안은2018-01-02 | 명세 정정은2020-11-11. 후속 표준이 앞선 구현의 원인이 될 수 없음 |
| A-G03 | WKT2015·WCS2012는 선행. Topic2:2019는 최초안 뒤 | 최초 실질안2019-01-09에 축 매핑이 이미 존재. [Jan28 메일](https://lists.osgeo.org/pipermail/gdal-dev/2019-January/049665.html)은 새 Topic2 판이 아직 공개 예정이라고 설명 | [Jan31 합병](https://github.com/OSGeo/gdal/commit/ab9e80368ef662712c963191fd86fde2c5b75600). squash의2018 author date로 최종 코드의 당시 공개를 단정하지 않음 |
| B01 | [1997 저자 매뉴얼](https://tug.org/TUGboat/tb18-4/tb57than.pdf)과 Wild1995 확인; hz1993 핵심 본문 미확인 | 2000 논문 §4의 회고 영향 진술. 처음 읽은 날·처음 바꾼 날은 미확인 | [2001 사용 예제](https://tug.org/TUGboat/tb22-3/tb72thanh.pdf)는 구현 사용법을 확인하지만 최초 독서 시점을 메우지 않음 |
| B02 | GML2004·GMLJP2/WMS2006. 2006 표준이 GML을 규범 참조 | RFC v1 2008-01-04에 정책 존재; Jan22 작성자가 generator를 EPSG 축에 맞춰 바꿨다고 설명 | 시험13569는 **20:19:46Z**, 코드13570은20:21:49Z. 동일 UTC 타임라인은 B 원장 참조. 검색색인·첫 독서는 미확인 |
| B03 | [1.0.1 archive](https://lilypond.org/download/sources/v1.0/lilypond-1.0.1.tar.gz)에1998-04~08 파일 날짜·출판사/작품명이 있음 | ANNOUNCEMENT는0.1 이후 새 Feta와 기존 글꼴 불만을 연결 | 날짜는 파일 mtime 경계. 정확한 원전 판·초기0.1 코드·당시 공개 posting은 미확인 |
| B04 | AMS1979·기관 보고서1978의 원래 주소는 접근 실패 | 열람 가능한 미러의 서술은 수학적 선택 뒤 역사 독서·놀람 | 미러는 최소수 제외. 특정 변화에 대응하는 고정 구현도 미확인 |

날짜가 같다는 이유로 당일 선후를 추정하지 않았다. B02는 티켓·커밋의 명시 시각을 썼고, B03는 공개일을 파일 날짜로 치환하지 않았다. B04의 역사적 선례를 몰랐다는 진술은 **미러에서 읽은 진술**이며 설계 방향 자체를 몰랐거나 원전 때문에 방향을 바꿨다는 증거와 구별했다. 이번 연구에 새 사건인12개와 저자에게 새 원리인 사건의 수는 같은 변수가 아니다. 후자는 확정하지 못했다.

## Q4·Q5 — 작동을 대응시키고 반영 범위를 좁힘

### 지도 좌표: 같은 위치를 보존하는 두 표현

A-G03의 입력은 공식 CRS와 데이터 좌표다. 유지할 객체는 좌표가 가리키는 위치와 CRS의 권위 식별이다. CRS 권위기관이 축의 의미·순서를 정하고, GDAL 구현자·호출자가 데이터 순서를 별도로 매핑한다. 최초안은 공식 축을 바꾸고 같은 EPSG 코드를 붙이는 대안, 코드 자체를 지워 정체성을 잃는 대안을 피한다. 고정 구현·시험은 기본 좌표 `(32,-117.5)`와 명시한 GIS 좌표 `(-117.5,32)`를 같은 UTM 결과에 연결한다. [합병 코드 L286–394](https://github.com/OSGeo/gdal/blob/ab9e80368ef662712c963191fd86fde2c5b75600/gdal/ogr/ogrspatialreference.cpp), [같은 목적 시험 L73–140](https://github.com/OSGeo/gdal/blob/ab9e80368ef662712c963191fd86fde2c5b75600/autotest/osr/osr_ct.py).

그와 별개로 **출력 기본값은 후속 논의에서 실제 조정됐다.** [Jan25 작성자 메일](https://lists.osgeo.org/pipermail/gdal-dev/2019-January/049658.html)은 VRT/aux.xml 호환성 때문에 API `exportToWKT`의 기존 기본을 유지하고 CLI만 WKT2로 전환한다고 말한다. 이 변경을 누락하면 ‘아무것도 바뀌지 않았다’는 잘못된 결과가 된다. 이를 축 매핑의 새 발상으로 합치면 다른 하위 결정의 인과를 혼합하게 된다. 같은 이름의 BBOX도 [Jan22 Extent 토론](https://lists.osgeo.org/pipermail/gdal-dev/2019-January/049649.html)에서 CRS의 권고 범위와 grid 연산의 엄격한 자료 범위로 갈린다.

B02의 독립 부분은 파일 경계의 `origin`과 `offsetVector`다. [GML3.1.1](https://docs.ogc.org/bp/03-105r1/03-105r1.zip)의 `GML-3.1.1/GML-3.1.pdf` §12.4.3.1(인쇄p117/PDF139)은 축의 순서가 좌표 tuple 순서를 결정한다고 명시한다. §9.1.3.1과 §9.1.4.1의 DirectPosition·Vector, RectifiedGrid의 origin·offsetVector가 그 규칙을 대상 객체에 연결한다. [GMLJP2 §7.7](https://docs.ogc.org/is/05-047r3/05-047r3.pdf)은 CRS 식별자의 권위를 연결한다. WMS의 BBOX 규칙만으로 GML 벡터의 의무를 대신하지 않았다.

작성자는 [#2131 c1–2](https://trac.osgeo.org/gdal/ticket/2131#comment:1)에서 generator를 EPSG 축에 맞추도록 수정했다고 설명했고, 패치는 읽기에서 EPSG4xxx URN, 쓰기에서 geographic CRS 조건에 따라 반전한다. `GDAL_IGNORE_AXIS_ORIENTATION` 예외가 있어 당시에도 무조건적인 일반 해법은 아니었다. 티켓에 적힌 시험 r13499는 다른 RFC19 메모리 변경으로 확인됐다. 실제 동일 목적 시험은 [13569 / 805a866](https://github.com/OSGeo/gdal/commit/805a8665fc5ed29e5082720eb5391efefe4f77d4), 구현은13570 / bef1fa8로 복원했다. [2011 작성자 메일](https://lists.osgeo.org/pipermail/gdal-dev/2011-June/028981.html)은 일반 PROJ 축 왕복 손실과 복잡한 부작용을 말하지만 이유를 ‘likely’로 한정한다. 전체 RFC 실패나 확정적 공급자 원인으로 넓히지 않았다.

### 활자와 음악: 품질 목표가 같아도 변경 가능한 대상이 다름

[Wild1995 §2](https://www.numdam.org/article/CG_1995___22_5_0.pdf)의 조판 설명은 대체 글리프·합자·약자와 광학적 여백을 포함한다. pdfTeX의 폭 조정은 문자 내용은 유지하면서 글리프 형태·줄 폭 계산을 바꾼다. 같은 균일한 문단 목표만으로 두 메커니즘을 같게 만들 수 없다. [Thành2000 §4](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf)는 hz 출판물의 영감을 직접 밝히면서, 구현 정보가 없어 알고리즘은 처음부터 만들었다고 말한다. 이것은 **영감의 연결과 구현 독립성**을 함께 지지한다. 다른 분야 원리의 독립 발명을 입증하는 문장은 아니다.

[2001 운용 예제 pp146–148](https://tug.org/TUGboat/tb22-3/tb72thanh.pdf)는 확대 글꼴 준비, 폰트/문자별 설정, 기존 줄바꿈 유지와 줄바꿈 변경 모드를 구별한다. 제안된 작은 확장 폭을 모든 글꼴·문자체계의 안전 범위로 일반화하지 않았다. [André1995 §1.1–1.3·§4.1–4.4](https://www.numdam.org/article/CG_1995___22_61_0.pdf)는 glyph와 character, kerning과 ligature를 구별하고 문자 대체가 맞춤법·하이픈 처리와 충돌하는 경우를 설명한다. 제공 분야의 예외가 실제 소프트웨어 입력 모델을 제한하는 사례다.

LilyPond에서는 현대 Essay의 회고만으로 멈추지 않았다. [1.0.1 소스](https://lilypond.org/download/sources/v1.0/lilypond-1.0.1.tar.gz)의 ANNOUNCEMENT14–20·fonts.doc11–23은 기존 글꼴에 대한 불만과 새 Feta 제작을 연결하고, 악보 본보기와 Wanske/Ross를 명명한다. `mf/feta-toevallig.mf`는 Bärenreiter의 Schubert *Auf dem Strom*, Hofmeister의 Müller *Etüden für Horn*을 구체적으로 지목한다. 반면 관찰한 sharp beam 특징을 Wanske가 언급하지 않는다는 이유로 무시한 코드 주석도 있어, 실무 전례를 모두 복사한 과정은 아니다. 정확한 악보 판을 아직 읽지 못했으므로 특정 판각 규칙이 어떤 이전 글리프를 바꿨는지까지 닫지 않았다.

비교 원문 [MPA1993 pp1–3](https://www.mpa.org/wp-content/uploads/2018/06/standard-practice-engraving.pdf)은 규칙을 명료성을 위한 지침으로 제한하고 줄기 방향의 문맥을 구분한다. 이는 LilyPond가 인용한 MPA1996 pamphlet과 **다른 작품**이다. [MOLA2017 pp3·5–6](https://mola-inc.s3.eu-west-1.amazonaws.com/files/mola3/MOLA-Guidelines-for-Music-Preparation.pdf)은 페이지 넘김·파트별 검토·연주자가 정할 사항을 구분한다. 이 후기 실무 규칙을1998 Feta의 원인으로 소급하지 않았다. 관련 현대 optical spacing 회귀 시험 역시 초기 글꼴 교체와 같은 역사적 결정으로 합치지 않았다.

### 누가 무엇을 확인할 수 있는가

| 관점 | 직접 확인 가능한 사건·기록 | 이번에 확인하지 못한 결과 |
| --- | --- | --- |
| 구현자 | C02 병합 WPT·Gecko 기록, C04 Servo parser/거부 시험, G02 pytest/ASAN 설정, G03 매핑 코드, B02 축 패치·fixture, B03 Feta 소스 | 당시 환경에서의 실제 실행·성능·모든 driver와 browser |
| 명세 편집자·관리자 | C01 기존 규칙, C03 이름 변경, C04 후속 grammar, G01 운영 이전 공지, G03 API/CLI 범위, G04 배포 범위 | 규범 변경이 모든 구현과 사용자에게 동시에 전파됐다는 보장 |
| 최종 사용자·작성자 | C01의 해결·legacy caveat, C02 깨진 페이지 호환 동기, B01 줄바꿈 모드, B02 지리 위치 오류와 복구 fixture, 음악 실무의 넘김·가독성 조건 | 실사용 과업 성과·가독성 개선량·검색 때문에 절약한 시간 |

## Q6 — 반대 설명을 찾은 결과

| 사전 반례 목표 | 읽은 반대 근거·위치 | 관측 범위와 한계 |
| --- | --- | --- |
| ① 같은 이름, 다른 객체·권한 | [#2157 회의 댓글](https://github.com/w3c/csswg-drafts/issues/2157#issuecomment-355169539)의 col 요소/논리 열 cell; [RFC73 Extent 토론](https://lists.osgeo.org/pipermail/gdal-dev/2019-January/049649.html)의 CRS/operation BBOX | 직접 관측. 입력 객체와 권한을 대응하지 않으면 같은 명칭이 반대 판단을 유도 |
| ② 유사하지만 독립 발명 | [Thành §4 p38](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf)의 알고리즘 직접 개발 진술; B04 미러의 선택 뒤 역사 독서 | **독립 구현은 확인**, 다른 분야 원리 자체의 독립 발명은 미확인. 인용 부재만으로 독립 발명이라고 쓰지 않음 |
| ③ 인용이 결정 뒤 | [Servo PR19610](https://github.com/servo/servo/pull/19610)→CSS 최초안; [RFC74 공지](https://lists.osgeo.org/pipermail/gdal-dev/2019-May/050244.html)의 선행 sprint 공식화; B02 최초 RFC 정책 | 직접 관측. 후속 문서화·기존 결정 설명을 새로운 발견으로 읽는 시간 역전을 차단 |
| ④ 반영 전에 공급자 제약 때문에 포기 | [RFC72 채택판](https://trac.osgeo.org/gdal/wiki/rfc72_pytest?version=14)의 CI sugar/ASAN 제약; [RFC73 Jan25](https://lists.osgeo.org/pipermail/gdal-dev/2019-January/049658.html)의 전역 WKT2 기본 미채택; [B02 2011 메일](https://lists.osgeo.org/pipermail/gdal-dev/2011-June/028981.html)의 한정적 회고 | 동일 분야의 범위 축소·호환성에 의한 미채택은 관측. 특정 타 분야 전이를 공급자 제약 때문에 포기했다는 완전한 역사 사슬은 미확인. 현재 Kakadu 실행 제약도 당시 포기 근거로 사용하지 않음 |

④는 최초안과 보존된 CI 도입 코드까지 추가 대조했다. RFC72 v1은 Travis buffering과 맞도록 하거나 CI에서 끄는 조건부 계획이고, [v11](https://trac.osgeo.org/gdal/wiki/rfc72_pytest?version=11)은2018-12-03 23:43:36Z에 buffering 때문에 끄라고 명시한다. 그러나 [최초 보존 CI 도입 커밋](https://github.com/OSGeo/gdal/commit/75c0dc375faabbe7d27d9d9a0eb4a98bd41cf44f)의8개 Travis 명령부터 이미 `-p no:sugar`다. 따라서 ‘병합 전에 조건부 제외를 확정’은 확인되지만 ‘활성화한 선택을 새로 포기’는 미확인이다. author date와 rebase committer date도 구별했다. `streams/review-counts/countertype4.json`에9개 보조 열람 기록과 첫 재개 자료를 남겼고 새 사건·고유 저작은 추가하지 않았다.

자료를 읽기 전 예상한 ‘규칙을 지키면 축 순서가 정리된다’는 일반화도 반례를 만났다. [GeoPackage1.3 §2.1.3.1.1](https://www.geopackage.org/spec130/)은 기존 WKB 호환성 때문에 metadata의 축 순서와 독립인 x,y payload 규칙을 둔다. [OGC VTP2 §11.1](https://docs.ogc.org/per/19-088r2.html)은 참여자 간의 축 순서 해석·복잡성 차이와 명시적 필드 제안을 기록한다. [Testbed12 WCS §7.2.3·§9.4–9.5](https://docs.ogc.org/per/16-033r1.html)는 실제 공급자 출력과 배열의 축을 확인하기 위한 별도 handshake·시험 비용을 보여 준다. 이들 후대 자료는 보편화의 한계를 보여 주며2008/2019의 저자 노출 근거로 세지 않는다.

반대로 ‘당시 GML 규칙이 없었다’는 부정 설명도 철회했다. [DGIWG104 §6.3 p15](https://portal.dgiwg.org/files/9389)는 GML3.1.1 지침이 불명료하다고 말하고, GMLJP2의 EPSG:4326 예시는 혼동을 키운다. 그러나 직접 회수한 GML3.1.1 규범의 ordered `usesAxis`·DirectPosition·Vector 연결은 존재한다. 실무자가 모호함을 겪었다는 기록과 규범의 부재는 다르다. 독립 검토는 이 부정 설명을 수정하면서도, 정확한 규칙이 있다는 사실을 저자의 새 학습 증거로 확대하지 않았다.

### 분야별 실패가 다른 이유

| 비교 | 인쇄·음악(B01/B03/B04) | 지도·지리 인터페이스(A-G03/B02) |
| --- | --- | --- |
| 연결 근거가 강한 곳 | 저자가 본보기·영감을 직접 이름 붙임. B03는 초기 발표문까지 회수 | 원문 규칙·권한·실제 코드/시험 연결이 구체적 |
| 끊기는 곳 | 정확한 제공 원전 판, 초기 선택, 노출·공개 날짜. B04는 원 발행자 접근 실패 | 원안에 이미 선택이 있고 기술 표준 준수와 타 분야 발견의 경계가 남음 |
| 현장의 반대 조건 | 글리프와 문자 동일성, 줄바꿈 모드, 실제 연주 가독성, 선택적인 관찰 채택 | metadata 규범과 파일 payload 관행, grid와 CRS 축, 기존 포맷·driver 호환성 |
| 대체 설명 | 이미 있던 품질 목표에 참고 전통·독립 구현을 붙였을 수 있음 | 이미 알고 있던 표준을 뒤늦게 일관되게 구현했을 수 있음 |

## Q7 — 탐색기에 반환할 단위

반환 단위는 **사건 내부의 특정 선택 + 근거 절 + 옮기면 깨지는 조건**이다. `cards.md`에12개 카드를 세 묶음으로 두고 각 카드 링크는 최대2개다. 시점·용도 한정 선례는 A-G03/B02, 보류는 B01/B03, 유사 오답은 나머지8개다. 이 묶음은 검색 결과를 읽을 때의 용도이며 인과 완결 등급을 바꾸지 않는다.

대표 카드 A-G03은 ‘권위 객체를 유지하면서 표현 순서를 별도 상태로 둔다’는 설계 선택에 도움을 줄 수 있다. 근거는 WKT2015 §7.5.5와 RFC73 최초 실질안이며, 공식 CRS를 바꾼 뒤 같은 authority code를 붙이는 조건에는 가져오면 안 된다. B02는 파일 경계의 좌표 순서 변환에 한정된다. B03는 실제 악보 판을 읽기 전까지 특정 판각 규칙의 인과 선례로 추천할 수 없다. B04는 유용한 역사 인용이 있어도 선택 변경을 입증하지 않는 오답이다.

엄격한 역사적 양성 대조 적격은 **A0/B0**, 조건부 회수율은 **해당 없음**이다. B02는 표준 포함·기존 코드 기준의 별도 실험을 사전 선언할 때만 쓸 수 있는 조건부 준수 대조 후보1건이다. 첫 노출이나 새 원리 발견을 확인한 양성 대조로 쓰지 않는다. 어떤 검색기를 돌려 회수 여부를 측정한 실험도 하지 않았다.

| 해석을 바꾸어 재집계하는 방법 | A | B | 무엇을 세는가 |
| --- | --- | --- | --- |
| 고정 원안·명시 인과·모든 접점 | 0/8 | 0/4 | 엄격 완결 사슬 |
| 기존 선택 설명을 신규 변화로 잘못 바꿔 부르는 후보 | 1/8: A-G03 | 1/4: B02 | 실제 C3가 아닌 설명 후보; 판정 오류의 크기 |
| 설명 후보와 회고·유추의 유용성까지 모두 허용 | 1/8: A-G03 | 3/4: B01/B02/B03 | `plausible_mechanism`; 완결 사슬은 여전히0 |
| 기준선을 기존 코드로 옮기고 표준 준수를 포함 | 해당 감도 대상 없음 | 1/4: B02 | 같은 사건 안의 좁은 GMLJP2 준수 사슬 |

`judgments.csv`는 엄격12행·회고/유추12행·B02 조건부 감도1행이다. `evidence/case-decisions.json`의 플래그와 `evidence/rebuild.py`로 분자·분모를 다시 계산한다. 감도1행을 독립 사건으로 세거나 나머지 미확인을 실제 음성으로 바꾸지 않는다.

## 원문 규모·점검·미충족

통합 원장은168행(기존4 stream159 + 반례④ 보조9)이고, **고유 외부1차 저작은49개**로 보수적으로 계산했다. A 최초8, 제공 분야 규칙10, 후속 결정·반영15, 독립 반대·제약10, B 초기·별도 baseline·선행 구현6이다. 같은 저작은 한 범주에만 들어간다. 원 stream 합50에서 인접한 B02 코드13570과 시험13569를 같은 변경 작품으로 묶어49로 정정했다. 원래 값·정정 근거는 보존했다. CSS/GDAL 여러 판, LilyPond Essay의2.24/2.26, 동일 구현의 여러 파일을 따로 세지 않았다. `evidence/recount.json`, `sources.jsonl`, `streams/review-counts/report.json`이 이 수치의 재계산 근거다.

제공 분야 규칙10 중 명시적으로 연결된 선행 저작은2, 당시 관련 표준·간접 규범 계통은5, 후기 또는 실제 인용작과 다른 실무 비교는3이다. 따라서 원문 규모 충족을 실제 인과 donor10 확인으로 표현하지 않는다. NUMDAM은 정식 저널 원문 아카이브로 분류했다. 이 분류와 mutable NEWS를 더 엄격하게 제외하는 감도에서도46개(A8/규칙9/후속14/반대9/기타6)로 규모 조건을 충족한다. 이 감도는 직접 원전 접점의 미확인을 해결하지 않는다.

**미충족을 남긴다.** B04는 AMS403·Stanford503 뒤 발행자/기관 본문을 확보하지 못했다. B01의 핵심 hz 원문, B03의 정확한 악보 판·변경 전 글꼴도 미확인이다. A-C03의 완전 결말 비노출 조건은 충족하지 못했다. 네 반례 목표는 모두 조사했지만 다른 분야 원리 자체의 독립 발명과 특정 타 분야 전이의 공급자 제약 포기는 완전히 입증하지 못했다. 이 빈칸을 없애려고 표집 기간·순위·사건을 교체하지 않았다.

CSV 파싱·사건 결합·source ID 참조·범주별 고유 수는 재계산하고 Artifact Tool로 CSV를 별도 가져와 확인했다. 문헌 원장과 결과 형식 검사는 `evidence/acceptance-evidence.json`에 조건별 `met`·분자/분모·파일/행을 둔다. 역사적 프로그램 실행은 하지 않았고, B stream은 현재 GDAL3.10.3·pdfTeX1.40.26, Python2/LilyPond 부재·JP2KAK 미인식을 확인했다. 필요한 과거 버전·입력·명령은 HANDOFF에 남긴다. 원격 고정 SHA의 RESULT·수용 파일 재독과 session check 결과는 이 보고서 이후 마지막 HANDOFF 커밋에 기록한다.

## 같은 우선순위의 약점과 다음 조사
'''
weak_rows = [[w["weakness"], w["affected"], w["evidence"], w["next"], w["changes_if"]] for w in weaknesses]
last_table = table(["중요한 불일치·약점", "영향받는 결론", "근거 URL·행", "다음 최소 조사·첫 자료", "결과가 바뀌는 조건"], weak_rows)
result = "# AF-RES-037 · 다른 분야의 원리가 실제 소프트웨어 선택을 바꿨는가\n\n" + table(head1, rows1) + "\n\n" + table(head2, rows2) + "\n" + body + "\n" + last_table + "\n"
(ROOT / "RESULT.md").write_text(result)

cards = ["# AF-RES-037 · 선택 단위 반환 카드", "", "각 행은 특정 설계 선택·근거 절·가져오면 안 되는 조건과 최대2개 링크다. 새 원리 발견 여부와 사용 가능한 선례를 분리한다. 표집 사건12개를 한 번씩만 둔다.", ""]
for bucket in ["시점·용도 한정 선례", "유사 오답", "보류"]:
    cards.extend(["## " + bucket, ""])
    if bucket == "시점·용도 한정 선례":
        cards.extend(["엄격 역사적 양성 대조는 A0/B0, 조건부 회수율은 해당 없음이다. B02만 표준 포함·기존 코드 기준을 사전 선언한 별도 검사에서 좁은 준수 대조 후보가 될 수 있다. A-G03는 기존 선택 설명이며 신규 변화 양성으로 쓰지 않는다.", ""])
    rs = []
    for c in cases:
        if c["card_bucket"] != bucket:
            continue
        assert len(c["card_links"]) <= 2
        rs.append([c["case_id"], c["decision_unit"], c["card_use"], c["card_basis"], c["card_limit"], " · ".join(f"[근거{i}]({u})" for i,u in enumerate(c["card_links"],1)), c["strict_code"]])
    cards.extend([table(["사건", "독립 부분·범위", "도움이 되는 선택", "근거 절", "가져오면 안 되는 조건", "근거 링크", "판정"], rs), ""])
cards.extend(["## 사용 조건", "", "새로 찾은 대상은12개지만 저자가 당시 처음 알게 된 원리로 확정한 수는0이다. 미확인은 부재가 아니며, 이 카드는 검색 성능 측정 결과가 아니다. B04는 원 발행본 접근 실패와 미러 여부를 유지하고 양성 대조로 쓰지 않는다.", ""])
(ROOT / "cards.md").write_text("\n".join(cards))
print(json.dumps({"report_cases":len(rows1), "table2_rows":len(rows2), "last_weakness_rows":len(weak_rows), "cards":len(cases)}, ensure_ascii=False))
