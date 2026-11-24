"""Render the three required tables from preserved AF-RES-106 ledgers."""
from pathlib import Path
import csv
import json
import importlib.util

ROOT = Path(__file__).resolve().parents[1]


def rows(name):
    with (ROOT / name).open(newline="") as f:
        return list(csv.DictReader(f))


def table(headers, data):
    def cell(v):
        return str(v).replace("|", "\\|").replace("\r", "").replace("\n", " ")
    return "\n".join(["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)] +
                     ["| " + " | ".join(cell(v) for v in r) + " |" for r in data])


def link(label, url):
    return f"[{label}]({url})" if str(url).startswith("http") else "미확인"


def pick(r, *keys, default="미확인"):
    return next((r[k] for k in keys if r.get(k)), default)


def short(value, n=170):
    return value if len(value) <= n else value[:n] + "…"


def arr(value):
    try:
        return json.loads(value) if isinstance(value, str) else value
    except (ValueError, TypeError):
        return []


def main():
    predictions, lineage, returns = rows("predictions.csv"), rows("lineage.csv"), rows("returns.csv")
    by_new = {r["case_id"]: r for r in lineage if r["edition"] == "new"}
    by_old = {r["case_id"]: r for r in lineage if r["edition"] == "old"}
    pred = {r["case_id"]: r for r in predictions}
    purposes = {
        "GG-M1": "diamonds의 carat/price를 cut별 점 모양으로 구별; geom_point(aes(shape=cut))",
        "GG-M2": "자동차 산점도의 같은 두 점을 직선·곡선으로 연결; geom_curve+geom_segment",
        "GG-G1": "cut별 boxplot에 clarity 그룹의 개별 carat 점 정렬; position_jitterdodge()",
        "GG-G2": "시간별 실업자수와 실업기간을 선 두께로 표현; geom_line(linewidth=uempmed)",
        "MP-A1": "좌심실 17분절 bullseye; polar pcolormesh/plot와 bullseye_plot",
        "MP-A2": "기본 회전 후 정렬 설명; Axes.text(rotation,ha,va,bbox), 기본 정렬 의미",
        "MP-G1": "밀도·온도·속도 3개 y축; twinx 두 번+오른쪽 spine offset",
        "MP-G2": "G1–G5 Men/Women 점수·수치라벨; ±width/2의 두 bar 호출+bar_label",
    }
    t1 = []
    for p in predictions:
        cid = p["case_id"]
        old = link("옛 고정 절", p["old_section_url"])
        temporary = pick(p, "provisional_return_url", "new_provisional_section_url")
        tree = pick(p, "new_tree_evidence_url", "tree_evidence_url")
        moment = pick(p, "prediction_utc", "prediction_recorded_utc")
        purpose = purposes.get(cid, "결원: 해당 층 후보 0; 목적/API 미확인")
        signal = short(pick(p, "signal", "vacancy_reason"), 145)
        t1.append([f'{p["project"]}·{p["stratum"]}·{cid}', old + " · " + purpose,
                   signal + " · " + link("완전 새 tree", tree), link("봉인 임시 주소", temporary) + (" · 실제 반환과 구별" if p["vacant"] == "NO" else ""),
                   p["prediction_U"] + " · " + moment + " UTC", "결원" if p["vacant"] == "YES" else "예측 시 새 본문 미열람; 이후 판독은 아래 표"])
    content = table(["프로젝트·층·자리", "옛판 절 URL·목적·API", "신호와 완전 트리 근거 URL", "원래 임시 반환 주소", "새판 사용 예측·판정 시각", "결원·미확인"], t1)

    t2 = []
    for r in lineage:
        cid = r["case_id"]
        source = pick(r, "github_read_url", "github_section_url", "section_url")
        if r["vacant"] == "YES":
            t2.append([cid + "·" + r["version"], "결원·고정 절/fragment 미확인", "자원·소스·지문 미확인", "P·도착 미확인", "목적·방법 미확인", "미확인", "후보0; 실제 음성 또는 예측 유보로 세지 않음"])
            continue
        exact = r.get("method_original_exact", r["method_inherited"])
        method = f'핵심 API {r.get("method_core_api", r["method_inherited"])} / 사전 구체 방법 {r["method_specific"]} / 원 구성 {exact}'
        source_cell = link("PNG", r["payload_url"]) + " SHA256 `" + r["payload_sha256"][:12] + "…`; " + link("예제 소스", r["source_url"]) + " `" + r["source_sha256"][:12] + "…`"
        obs = short(r["observation"], 210) + " · " + "브라우저 표시/예제 실행 미확인"
        t2.append([cid + "·" + r["version"], link("고정 HTML 위치", source) + " · `#" + r["actual_fragment"] + "`",
                   source_cell, f'P {r["P"]}; 옛 경로 P {r["legacy_path_P"]}; 옛 fragment {r["old_fragment_arrival"]}',
                   f'원 목적 {r["U_original_purpose"]} / 일반 역할 {r["U_visual_role"]}; ' + method, r["G"], obs])
    content += "\n\n### 2. 판별 표 — 24판 자리\n\n" + table(["쌍·판", "고정 절 URL·실제 fragment", "자원·소스 URL와 지문", "수록 P·옛 주소 도착", "시각 목적 U·구체적 방법", "당시 생성 G", "확인한 동작·반증·미확인"], t2)

    spec = importlib.util.spec_from_file_location("recalc", ROOT / "tools/recalculate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    metrics = {(x["project"], x["stratum"]): x for x in module.confusion(predictions, by_new, "U_original_purpose")}
    t3 = []
    for r in returns:
        cid = r["case_id"]
        p, n = pred[cid], by_new[cid]
        metric = metrics[(r["project"], r["stratum"])]
        denominator = f'층 실제 양성 {metric["actual_positive"]}/음성 {metric["actual_negative"]}/실측 미확인 {metric["observed_unknown"]}/예측 유보 {metric["prediction_abstentions"]}/결원 {metric["vacancies"]}'
        if r["vacant"] == "YES":
            result = "결원; 예측·실측 없음"
            recommended = "유보 · 추천할 실제 사례 없음"
        else:
            label = {("YES", "YES"): "TP", ("YES", "NO"): "FP", ("NO", "YES"): "FN", ("NO", "NO"): "TN"}.get((p["prediction_U"], n["U_original_purpose"]), "미확인")
            result = p["prediction_U"] + "→" + n["U_original_purpose"] + " " + label
            if n["U_original_purpose"] != n["U_visual_role"]:
                result += "; 일반 역할 YES→YES TP"
            old_url = pick(r, "old_github_read_url", "old_url")
            new_url = pick(r, "new_github_read_url", "new_url")
            recommended = r["decision"] + " · " + link("옛 고정 위치", old_url) + " / " + link("새 고정 위치", new_url) + " · 새 `#" + n["actual_fragment"] + "`"
            if r.get("new_rendered_url"):
                recommended += " · " + link("새판 렌더 문서", r["new_rendered_url"])
            recommended += f'; 추가 문서 {r["logical_document_visits"]}, HTTP {r["additional_content_http_reads"]}'
        support = arr(r.get("support_urls", "[]"))
        evidence = " / ".join(link("대체 근거" + str(i + 1), url) for i, url in enumerate(support[-2:])) or link("층 tree", pick(p, "new_tree_evidence_url", "tree_evidence_url"))
        t3.append([r["project"] + "·" + r["stratum"] + "·" + cid, result, denominator, recommended, evidence, short(r["change_condition"], 210) + " · 실제 browser arrival/G 미확인"])
    content += "\n\n### 3. 오류·반환 표\n\n" + table(["프로젝트·층·사례", "예측→실측 및 오류 종류", "실제 양성·음성·유보·결원 분모", "권할 링크·정확 위치", "대체를 지지하는 출처 URL", "결정을 바꿀 자료·미확인"], t3)

    content += """

### 보조 추적 — 주 표본과 분리

| 프로젝트·사전 경로 | 열람과 독립 사례 분모 | 목적·방법·오류 | 원자료·정확 반환 | 미확인·범위 |
|---|---|---|---|---|
| ggplot2 예제 소스 D/R | 관련 metadata4개 중 적격 사건2개 전부; 대표 예제2개만 의미 판독; 연결57페이지 중 주4와 합쳐 전체를 채점한 것은 아님 | register_theme_elements와 guide_axis 각각 목적/공개 방법 YES; 옛 자원 경로 유지; 보조 양성2/음성0, FP/FN0 | [Upkeep 변경](https://github.com/tidyverse/ggplot2/commit/04a5ef274e912bee76180154b25d8bca0206feb1), [guide rewrite](https://github.com/tidyverse/ggplot2/commit/b9f43f2a7d93548b0794bc527b0f18ff0f028681); [대표2판독](evidence/ggplot2/lineage-extra.json) | 예제와 연결되지 않은 helper 삭제2건은 공식 자료로만 산입; 독립 예제0. 미사용 잔류를 전체57에서 부정한 것이 아님 |
| Matplotlib 예제 소스 D/R | 적격6커밋 전부 → merge 중복 제외3사건; 주 A1/A2와 겹치는2사건 제외, 새 보조1쌍 | pyplot_mathtext→pyplot_text: 옛 경로 NO→수학식 텍스트 목적 YES, FN1; 양성1/음성0. 옛 구체 수학식 literal은 NO | [삭제·통합·redirect 공식 변경](https://github.com/matplotlib/matplotlib/commit/fca4a5f6f8df0f620f77536f5a8d747da414001f), [새 #text-and-mathtext-using-pyplot](https://matplotlib.org/3.7.0/gallery/pyplots/pyplot_text.html#text-and-mathtext-using-pyplot) | 옛 #pyplot-mathtext는 새 DOM에 없음. 주 FN2에 보조 FN1을 합쳐 주 오류율을 만들지 않음 |
| 자료 최소량 대조 | GG stat_unique/labs/ggtheme3개, MP custom_scale/polys3d/spines_dropped/keyword_plotting4개; 별도 source3개 | 주 표본 결원을 채우지 않음. 코드·목적·사용 자원을 확인하되 주 혼동표에 산입0 | [GG 판독](evidence/ggplot2/FINAL_AUDIT.md), [MP 판독](evidence/matplotlib/FINAL_AUDIT.md), [자료 계보 대사](evidence/crossdomain/source-count-review.json) | download-only GUI source는 실제 상호작용 실행 미실시 |

## 결론과 판정의 의미

**경로의 존재만으로 다음 판의 원 목적 사용을 결정하면 후계 두 건을 놓친다. 구체적인 설명 대상을 보존하려는 경우 같은 경로도 잘못된 반환이 될 수 있다.** 반면 일반적인 시각 역할을 묻는 독자에게 barchart의 새 펭귄 예제는 여전히 적합하다. 이 연구가 확보한 FP는 봉인된 Men/Women·G1–G5 점수 목적에 대한 조건부 FP이며, 일반 grouped-bar 기능의 실패가 아니다.

상태는 **RESEARCH_COMPLETE_WITH_LIMITATIONS**다. 12쌍 자리·24판 자리와 허용 결원, 필수 자료 하한과 사전 보조 추적을 마쳤다. 검사받은 결과 SHA와 실제 저장소 검사·고정 GitHub 재열람은 후속 [VALIDATION.md](VALIDATION.md)와 마지막 [HANDOFF.md](HANDOFF.md)의 실행 영수증으로 확인한다. 이 보고서의 본문 판독은 실제 R/Python 예제 실행이나 브라우저 표시를 포함하지 않는다.

세 표의 P는 해당 판에서 실제 따라간 자원의 수록이다. `legacy_path_P`는 옛 대표 자원 경로의 생존으로 별도 보존한다. 도착 YES/NO는 고정 HTML의 정적 DOM/redirect 판독 범위다. MP-A1의 실제 meta-refresh fragment 전달은 미확인이다. 고정 raw HTML은 text/plain 응답이므로 `#id`가 그 endpoint에서 렌더·스크롤된다는 약속이 아니다. 소스 읽기에는 고정 GitHub `#L` 위치를, 실물에는 고정 PNG/source URL을 함께 제공했다. 전체 지문·srcset의1x/2x·source-set·수신 영수증은 [lineage.csv](lineage.csv), [returns.csv](returns.csv)와 각 프로젝트 원문에 있다.

### Q1–Q3: 전수 모집 범위와 사전 판단

| 프로젝트 | 옛 전체 경로 | 잔여 적격 | 제외·중복 | 자원 종류 | 새 경로 층 A/M/G | 주 실제/결원 |
|---|---:|---:|---|---|---|---|
| ggplot2 | reference HTML195 | 68 | 기존40·교정2·선행 별칭3·잔여 내부 별칭4·Examples 없음57·연결 그림 없음21 =127 | 외부 그림68, 인라인 전용0 | 0/57/11 | 4/2 |
| Matplotlib | gallery HTML608 | 479 | 기존40·교정2·index/실행요약51·redirect36 =129 | 그림440, 실행 source download 전용39, 인라인 전용0 | 3/0/476 | 4/2 |

ggplot2는 한 번 받은 옛 archive의195 HTML을 자동 판독했다. Matplotlib는 선행42와 index51을 먼저 구분하고515 HTML=479후보+36redirect를 수신·자동 판독했다. 자동 스캔 숫자를 직접 깊이 읽은 고유 자료수로 세지 않았다. 선택한 원 HTML·첫 예제 경계는 별도 확인했다. 접근 실패로 빠진 후보와 규칙에 따른 제외를 구분하며, 적격 범위의 최종 접근 실패는0이다. ggplot2 저자 source-set 연결1개는 미확인이라 그 행의 제한을 유지한다. 완전 발행 tree와 렌더 입력 확인까지가 기계 분류의 범위다. [전체 원장](frame.csv), [모집 대사](evidence/stage2-frame-summary.json).

AF102의 적격40개씩과 교정 예제·논리 별칭은 제외했다. 잔여547개 경로 해시를 별도 검토자가 다시 계산했고 모두 일치했다. `SHA256(UTF8('AF106|' + project + '|' + old_section_path))`에서 `Matplotlib`의 대문자를 유지한다. 서로 배타적인 A→M→G 우선순위와 각 층 앞2개를 그대로 따랐다. 예측6 YES/2 NO/결원4와 임시 주소는 원격8054c222…에 고정됐다. [봉인 원장](predictions.csv), [독립 재검산](evidence/crossdomain/review-final.json).

다만 source-set 정의와 일반 시각 역할의 추가 해석은 새 경로/선택을 본 뒤, 새 본문·정답을 열기 전에 교정했다. 완전한 경로 노출 전 사전등록이라고 주장하지 않는다. 최초 man-only 계산에서는 GG A0/M0/G68, 실제2/결원4였다. 확인된 저자 R경로를 포함하자 A0/M57/G11로 바뀌었다. 최초 초안과 교정 이유를 [METHOD_AMENDMENT.md](METHOD_AMENDMENT.md), [민감도 원장](evidence/ggplot2/sensitivity-man-only/stage2-summary.json)에 남겼다. 일반 역할을 추가해도 원 구체 목적과 원 예측은 지우거나 고치지 않았다. [목적 판정 계약](EVALUATION_TARGETS.md).

### Q4–Q6: 후계와 반대 관측

**MP-A1**은 `leftventricle_bulleye`에서 `leftventricle_bullseye`로 옮겨간 실제 예제다. 공식88% rename, redirect-from, 17분절 함수와 polar pcolormesh, 새 절·새 PNG를 함께 확인했다. 그림이 비슷하다는 이유만으로 후계라 정하지 않았다. 17분절 핵심 방법은 YES지만 colorbar의 `fig.add_axes` 절대 위치 방식은 `inset_axes`로 바뀌었다. [공식 변경](https://github.com/matplotlib/matplotlib/commit/0d39834ce0c1d579703672e3890b42806eda2121).

**MP-A2**는 `text_rotation`이 `demo_text_rotation_mode`로 통합된 경우다. default의 회전 후 정렬 목적과 `Axes.text` 회전/ha/va 핵심 API는 이어진다. 그러나 사전 specific target에 포함된 default `bbox` 강조는 draw 후 `get_window_extent`와 `Rectangle`을 쓰도록 바뀌었다. 따라서 시각 목적 YES, 핵심 API YES, 해당 강조 방식 NO가 동시에 맞다. 새 combined 그림의 왼쪽 `rotation_mode='default'`를 정확히 안내하며, 원 방법이 필요하면 옛판도 병기한다. [공식 삭제·통합](https://github.com/matplotlib/matplotlib/commit/f21219be5f7411a38b1598382f16dd7b099ffa9e), [별도 원문·그림 검토](evidence/ggplot2/review-matplotlib.json).

**MP-G1**은 목적과 twinx/spine 방법이 같아도 fragment가 `multiple-yaxis-with-spines`에서 `multiple-y-axis-with-spines`로 바뀐다. 성공 HTTP와 남은 PNG 경로만으로 정확한 절 도착을 보장할 수 없다. **MP-G2**는 같은 페이지·fragment·PNG·download 경로를 유지하면서 데이터·설명·코드를 교체했다. 옛 PNG 경로를 새 절이 계속 참조하므로 이것은 ‘미사용 잔류 파일’ 사례가 아니다. 원 두 대칭 bar 호출은 loop로 바뀌지만 bar/bar_label 원리는 이어진다. [첫 공식 데이터 교체](https://github.com/matplotlib/matplotlib/commit/895626981706e301923cc23aa079b5c0a8774bf7), [펭귄·loop 교체](https://github.com/matplotlib/matplotlib/commit/e71012316e7271799a064ce09ea9285f3edb47a7).

G2의 원 목적 NO에는 고정 새 gallery522 Python source의 basename·Men/Women/gender·score·G1–G5·옛 값·호출 검색, 검색 후보5개와 의미상 대조5개 총10본문, 두 공식 변경을 사용했다. 다른 분야나 다른 판까지의 전역 부재가 아니다. `bar_unit_demo`는 Tea/Coffee·단위 변환, `barchart_demo`는 개인 체력시험 percentile, `demo_agg_filter`는 비슷한 수치라도 축을 숨기고 drop shadow를 보여 준다. 비슷한 막대·값·코드만으로 원 score comparison의 후계로 채택하지 않았다. 같은 고정 범위에서 정확한 원 목적 후계가 발견되면 NO를 바꾼다. [후보 원문](evidence/matplotlib/barchart-successor-candidates.json), [전수 코드 검색 범위](evidence/matplotlib/new-bundle-search.json), [보완 판독](evidence/matplotlib/FINAL_AUDIT.md).

ggplot2의 주4쌍은 모두 첫 코드·목적·공개 방법이 이어졌고, 새 PNG bytes는 모두 달랐다. source `.r→.R` 변경은 M 신호였지만 의미적 삭제는 아니었다. 두 source 사건의 예제 대표2개도 목적이 이어졌다. 경로 판독은68개 전수이지만 새 본문 의미 판독은 주4+대조3+보조대표2=9개다. 남은59개의 새 절 사용은 미확인이다. Matplotlib의 일반 G층은 주2+별도 대조4=6개 본문을 판독했으며, 나머지470개의 의미를 전수 확인한 것은 아니다. 엄격한 ‘옛 경로가 남지만 대응 새 절에서 미사용’은 이 상세 판독과 사전 D/R 추적 범위에서 찾지 못했다.

### 혼동표 — 층별 분모, 두 목적 축 분리
"""
    stats = []
    for field, label in [("U_original_purpose", "원 구체 목적"), ("U_visual_role", "일반 시각 역할")]:
        for m in module.confusion(predictions, by_new, field):
            stats.append([label, m["project"] + "·" + m["stratum"], f'{m["TP"]}/{m["FP"]}/{m["FN"]}/{m["TN"]}',
                          f'{m["actual_positive"]}/{m["actual_negative"]}', f'{m["prediction_abstentions"]}/{m["observed_unknown"]}/{m["vacancies"]}',
                          f'{m["FPR"]["numerator"]}/{m["FPR"]["denominator"]}' if m["actual_negative"] else "산출 불가"])
    content += "\n" + table(["목적 축", "프로젝트·층", "TP/FP/FN/TN", "실제 양성/음성", "예측유보/실측미확인/결원", "FPR"], stats)
    content += """

원 구체 목적의 실제 새판 양성은7개·음성은1개다. 일반 역할의 양성은8개·음성은0개다. 이 숫자는 자리 재고이며 서로 다른 층의 합산 성능 비율이 아니다. Matplotlib G의 원 목적 FPR1/1은 선택된 음성1개에 대한 값으로, 제품 전체의 거짓양성률 추정치가 아니다. 다른 음성0층에서는 FPR·특이도가 산출 불가다. 방법의 여러 축은 U와 다른 질문이므로 원 U 예측을 API 예측으로 사후 변경하지 않는다. [계산 원장](counts.json), [재계산 코드](tools/recalculate.py).

### Q7: 링크의 충분성이 깨지는 다른 분야

| 원리·실물 | 직접 확인한 관계 | 반환할 정확 위치 | 반례·미확인 |
|---|---|---|---|
| [IIIF Presentation3](https://iiif.io/api/presentation/3.0/)와 [Rijksmuseum Night Watch manifest](https://iiif.micr.io/PJEZO/manifest) | Canvas→AnnotationPage→painting Annotation→body를 읽음. thumbnail과 painting body는 서로 다른 역할 | 확인된 Canvas/Manifest 문맥과 painting body를 [Content State payload](evidence/crossdomain/iiif-return-payloads.json)로 보존 | 이미지 수록/thumbnail 존재만으로 선택 Canvas의 본문 사용을 보장하지 않음. 실제 viewer 실행은 미확인 |
| [Fitzwilliam 실물](https://miniatures-iiif.fitzmuseum.cam.ac.uk/AGOID.29376/manifest.json) | Choice17, comment Annotation32의 영역 좌표가 모두 null | 작품 전체/확인한 Canvas는 제공하되 특정 comment 영역 선택은 유보 | 실제 viewer의 default choice·좌표 fallback 미확인. 없는 좌표나 viewer URL을 만들어 넣지 않음 |
| [JATS1.3 fig](https://jats.nlm.nih.gov/publishing/tag-library/1.3/element/fig.html)·[xref](https://jats.nlm.nih.gov/publishing/tag-library/1.3/element/xref.html), [수학적 graph clustering PLOS XML](https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0319031&type=manuscript) | figure9, figure-xref20가 내부 id로 연결. Fig7의 본문 참조4회는 서로 다른3문단: Results2문단·Discussion1문단 | [Fig7](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031#pone-0319031-g007), [Results](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031#sec022), [Discussion](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031#sec025) | XML 점 구분 id가 HTML에서는 하이픈 id로 변환됨. 같은 그림도 결과·설명 목적이 다름 |
| 같은 PLOS의 Table3 | 내부 xref는 유효하지만 caption의 Ncut과 가리킨 Fig7의 Nassoc 의미가 어긋남 | [Table3 원문](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031#pone-0319031-t003)과 Fig7을 함께 표시하고 의미 충돌을 명시 | Fig8은 Ncut이지만 저자 의도·공식 수정은 미확인. 링크를 Fig8로 자동 교정하지 않음 |

이 비교는 ‘수록’, ‘정확한 부분에서의 참조’, ‘설명 목적’, ‘실제 도착’이 다른 질문임을 보여 준다. 14개 성공 URL을7저작으로 합쳤고, 재개 시 원URL8개를 다시 받아 모두 기존 bytes와 일치함을 확인했다. 재열람을 신규 저작으로 다시 세지 않았다. [Q7 최종 판독](evidence/crossdomain/CROSSDOMAIN_FINAL.md), [별도 판독 영수증](evidence/crossdomain/review-final.json).

## 직접 자료와 검토의 범위

| 자료 범주 | 요구 하한 | 최종 보수 산입 | 중복 제외 방식 |
|---|---:|---:|---|
| 서로 다른 발행 예제 본문 | 8 | 15 | GG6+MP9. 같은 예제 양판·다른 앵커는1저작 |
| 본문과 다른 계보의 실제 그림·예제 source | 6 | 6 | GG stat_unique/labs/ggtheme의 그림3 + MP tick_labels_from_values/demo_gridspec06/looking_glass의 source3. 이6개 본문은 별도 산입0 |
| 공식 변경·발행/redirect 기록 | 6 | 10 | GG5+MP5. 같은 사건 merge3개 및 같은 patch의API/로컬복사 제외 |
| IIIF 규격·실물 | 2 | 5 | Presentation, Content State, 박물관 별도 안내1, 실물2. 같은 소장품 하위 이미지/manifest 복사 중복 제외 |
| JATS 규격·실물 | 2 | 2 | fig/xref는 규격1저작; PLOS XML/HTML/그림은 논문1저작 |
| 합계 | 24 | **38** | 원장670행과 고유저작38개는 다른 수 |

모든 행은 원 URL, 불변 URL 또는 보존 위치, 직접 연 UTC, 판·절·지문, 관측·지지/반박, 제한과 산입 사유로 연결된다. [sources.jsonl](sources.jsonl)의 source ID allowlist는 [계보 대사](evidence/crossdomain/source-count-review.json)에 있다. AF102에서 이미 센 자료와 전수 스캔·실패·미열람 링크는 신규 최소량에 산입0이다. 특히 옛 stat_unique 본문을 그대로 더하면 그림3과 중복되므로 최종 집계에서 그림 범주에만1개를 배정했다. 옛 산입 기록은 `previous_countable`로 보존했다.

ggplot2·Matplotlib 담당자가 원문을 읽고, 다른 담당자가 A2/G2 및 Q7·선택·계보를 재검토했다. 이전 별도5사례 판독도 보존했지만 일부 결과 메시지가 첫 원문 읽기 뒤 노출되었다고 기록돼 있으므로 완전한 맹검으로 부르지 않는다. 모든 검토자는 같은 모델 계열의 AI이며 사람 검토는 없다. root의 PNG·source 재독은 결론을 안 상태의 대조다. [MP 별도 검토](evidence/ggplot2/review-matplotlib.json), [선택/Q7 별도 검토](evidence/crossdomain/review-final.json), [자체 Q1–Q7 점검](SELF_CHECK.md).

## 적용 선택지·비용·인계

운영자는 경로 신호를 추가 확인의 우선순위로 쓸 수 있지만 이것만으로 목적 보존을 확정해서는 안 된다. 역사 저자에게는 고정 옛판 절·payload·source를, 비교 대상 새판의 독자에게는 확인한 새 절·실제 id를, 방법/설명 대상이 바뀐 경우에는 차이를 적은 두 판을 반환하는 선택지가 있다. [PRODUCT_OPTIONS.md](PRODUCT_OPTIONS.md)는 이를 별도 채택·폐기 가능한 안으로 정리하며 제품 DB·상시 crawler·AgentFlow API를 확정하지 않는다.

반환 원장에는 경우별 추가 문서 열람과 성공 HTTP 영수증을 따로 둔다. 같은 공식 변경이 여러 사례의 비용에 들어가므로 합계를 고유 자료수로 해석하지 않는다. 이는 사용자 클릭 수·모델 호출 수·서비스 latency의 측정치가 아니다. Matplotlib A1-old/G2-new의 현 버전 사이트 PNG는 고정본과 bytes가 달랐지만 decoded pixels는 같고 Software/dpi metadata 차이로 확인됐다. 가변 사이트를 고정 원본과 바이트까지 같은 영구 인용으로 광고하지 않는다. [pixel/byte 대조](evidence/matplotlib/live-byte-vs-pixel-review.json).

모든 실제16판의 G는 미확인이다. 당시 build run·입력 환경·실행별 출력 manifest/digest→발행 연결을 확보하지 못했다. source·정적 참조·PNG 존재로 G=YES를 만들지 않았으며 AF102의 빈 과거 실행36조회는 반복하지 않았다. browser redirect/fragment scroll, IIIF viewer, R/Python 예제 실행은 미실시다. 완료한 결원 탐색과 이 미실시 동작을 구분했다.

시작 통합판32b6bb…와 재개 최신d678d6a…를 계획49f603…과 대조했을 때 관련 변경은 dot-control.json뿐이었다. 운영 의존102 끝은 c1c0c863… 그대로이고 연구 입력092f4c5…를 유지했다. 원 manifest를 재작성하지 않았다. 재개 중 미확인 동시 파일 작성이 관측되어 독립 사본으로 보존한 뒤 작업했다. 원격 갱신은 기대 head와 일치할 때만 수행했다. [재개 계약](evidence/resume-contract.json), [복사 지문](evidence/isolation-snapshot.json), [재현 절차](reproduce.md).

| 가장 중요한 불일치·약점 | 다음 조사 제안·직접 열 자료 또는 실행할 입력 | 어떤 관측이면 판단을 바꿀지 |
|---|---|---|
| 잔류 경로·새 절 미사용의 엄격한 반례는 미확보. G2는 같은 경로의 내용 교체이며 원 목적 FP/일반 역할 TP로 갈린다. | 같은 고정판 GG 미판독59개·MP G미판독470개를 새 규칙으로 사전등록하고 exact section/src/srcset/source를 검사한다. | 자원 경로가 남아도 대응 목적 절에서 미사용인 실제 예제, 또는 G2 원 점수 목적의 정확한 후계가 나오면 해당 방향·NO 판정을 바꾼다. |
| source-set와 일반 역할 정의가 경로/선택 노출 뒤 추가됐고, 원 목적 음성은1개다. | 보존된 man-only와 넓은 source-set을 다른 미노출 버전/프로젝트에서 고정해 비교하고 독자의 필수 목적을 먼저 기록한다. | 정의·표본 변화에 따라 FP/FN이 사라지거나 반전되면 신호의 효용과 목적 단위를 재평가한다. |
| 정적 참조와 실제 도착·역사 생성은 다르며 G16판과 browser/viewer 동작은 미확인이다. | 정확 반환 URL/fragment의 실제 브라우저 이동, 같은 과거 발행의 보존 run ID·환경 lock·output manifest/digest를 확보한다. | 실제 이동이 다른 절을 가리키면 반환을 수정하고, 실행별 출력과 발행 연결이 확인되면 해당 G를 YES/NO로 갱신한다. |
"""
    (ROOT / "RESULT.md").write_text(content.rstrip() + "\n")
    print(json.dumps({"table1": len(t1), "table2": len(t2), "table3": len(t3), "result_bytes": len(content.encode())}))


if __name__ == "__main__":
    main()
