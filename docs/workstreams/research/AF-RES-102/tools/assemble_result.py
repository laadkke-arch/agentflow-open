#!/usr/bin/env python3
"""Produce the three required tables from frozen predictions and adjudicated rows."""
import collections
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRATA = ["general", "old_asset_absent", "asset_retained_source_changed"]
LABEL = {"general": "일반", "old_asset_absent": "옛 경로 부재", "asset_retained_source_changed": "경로 유지·소스 변경"}
PRED = list(csv.DictReader((ROOT / "predictions.csv").open()))
LINEAGE = list(csv.DictReader((ROOT / "lineage.csv").open()))
PAIR = {(r["case_id"], r["edition"]): r for r in LINEAGE}
EVIDENCE_COMMIT = "be9c4cfa09a59da937d40f71cdf7c675fb42c0fa"


def jread(name):
    return json.loads((ROOT / name).read_text())


def jwrite(name, data):
    (ROOT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def link(label, url):
    return f"[{label}]({url})" if url else "미확인"


def blob(raw, line=None):
    url = raw.split("#")[0].replace("https://raw.githubusercontent.com/", "https://github.com/", 1)
    pieces = url.split("/")
    if "raw.githubusercontent.com" in raw:
        pieces.insert(5, "blob")
    return "/".join(pieces) + (f"#L{line}" if line else "")


def start_line(row):
    match = re.search(r"L(\d+)", row.get("section_locator", ""))
    return int(match.group(1)) if match else None


def table(headers, rows):
    def cell(x):
        return str(x).replace("|", r"\|").replace("\n", " ")
    return "\n".join(["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"] + ["| " + " | ".join(cell(x) for x in row) + " |" for row in rows]) + "\n"


def rate(n, d):
    return {"numerator": n, "denominator": d, "value": n / d if d else None, "display": f"{n}/{d}" if d else "산출 불가", "reason": "" if d else "해당 실제 분모가 0"}


def main():
    strata = []
    classifications = {}
    for project in ["ggplot2", "Matplotlib"]:
        for stratum in STRATA:
            ps = [p for p in PRED if p["project"] == project and p["stratum"] == stratum]
            c = {k: 0 for k in ["TP", "FP", "FN", "TN", "abstention", "vacancy", "actual_positive", "actual_negative"]}
            for p in ps:
                actual = PAIR[p["case_id"], "new"]["U"]
                if p["vacant"] == "True":
                    k = "vacancy"
                elif actual not in ["YES", "NO"] or p["prediction_U"] not in ["YES", "NO"]:
                    k = "abstention"
                else:
                    k = {("YES", "YES"): "TP", ("YES", "NO"): "FP", ("NO", "YES"): "FN", ("NO", "NO"): "TN"}[(p["prediction_U"], actual)]
                c[k] += 1
                if p["vacant"] != "True":
                    c["actual_positive"] += actual == "YES"
                    c["actual_negative"] += actual == "NO"
                classifications[p["case_id"]] = k
            strata.append({"project": project, "stratum": stratum, "slots": len(ps), **c,
                           "sensitivity": rate(c["TP"], c["actual_positive"]),
                           "false_negative_rate": rate(c["FN"], c["actual_positive"]),
                           "false_positive_rate": rate(c["FP"], c["actual_negative"]),
                           "specificity": rate(c["TN"], c["actual_negative"]),
                           "case_ids": [p["case_id"] for p in ps]})
    sources = jread("evidence/source-reconciliation.json")
    counts = {
        "unit": "One old logical example / two selected publication editions; confusion matrix joins prediction to NEW-edition U only.",
        "main": {"pair_slots": 12, "filled_pairs": 8, "vacant_pairs": 4, "edition_positions": 24, "actual_edition_positions": 16, "vacant_edition_positions": 8,
                 "filled_predictions": {"YES": 8, "NO": 0, "abstention": 0}, "new_U": {"YES": 8, "NO": 0, "unknown_actual": 0},
                 "actual_position_P": {"YES": 16, "NO": 0, "unknown": 0}, "actual_position_U": {"YES": 16, "NO": 0, "unknown": 0}, "actual_position_G": {"YES": 0, "NO": 0, "미확인": 16},
                 "main_pairs_different_primary_PNG_bytes_same_purpose": 8, "provisional_fragment_corrections": ["MP-C1"]},
        "strata": strata,
        "no_pooled_rate": "Selection conditions differ; only descriptive counts above are combined. No overall error-rate, specificity or rename-detection performance claim.",
        "supplemental": {"ggplot2": {"pairs": 20, "type1_found": 0, "type1_checked": 20, "type2_eligible_absent_paths": 0, "type3_found": 0, "type3_same_byte_pairs": 1, "type4_found": 19, "type4_checked": 20},
                         "Matplotlib": {"pairs": 20, "external": 17, "inline": 3, "type1_found": 0, "type1_external_checked": 17, "type2_eligible_absent_paths": 0, "type3_found": 0, "type3_same_byte_pairs": 0, "type4_found": 20, "type4_checked": 20},
                         "scope": "First20 remaining examples by frozen hash order within each first40 frame, not the whole site; never promoted to main."},
        "source_minimum": sources,
        "generation_queries": {"ggplot2": 14, "Matplotlib": 22, "result": "All HTTP200 with zero visible records; no observed historical job/output binding; not evidence of G=NO."},
    }
    jwrite("counts.json", counts)
    jwrite("evidence/counts.json", counts)

    author_returns = {}
    for group in ["ggplot2", "matplotlib"]:
        for x in jread(f"evidence/{group}/returns.json"):
            author_returns[x["case_id"]] = x
    returns = []
    t1, t2, t3 = [], [], []
    for p in PRED:
        cid, vacant = p["case_id"], p["vacant"] == "True"
        old, new = PAIR[cid, "old"], PAIR[cid, "new"]
        prj = "GG" if p["project"] == "ggplot2" else "MP"
        if vacant:
            pub_repo = "tidyverse/ggplot2" if prj == "GG" else "matplotlib/matplotlib.github.com"
            edition_links = f'{link(p["old_version"] + " " + p["old_publication_sha"][:8], "https://github.com/" + pub_repo + "/tree/" + p["old_publication_sha"])} → {link(p["new_version"] + " " + p["new_publication_sha"][:8], "https://github.com/" + pub_repo + "/tree/" + p["new_publication_sha"])}'
            t1.append([f'{cid} · {p["project"]} · {LABEL[p["stratum"]]} · {p["slot"]}', "결원; 이전 예제·절·목적 미확인", edition_links, "완전한 새 트리의 해당 후보 0", "미확인(결원); " + p["prediction_recorded_utc"], "고정 첫40에서 부족; 다음 본문·그림·CI 선행 열람0; 사후 충원 금지"])
            ret = {"case_id": cid, "decision": "유보", "vacant": True, "reason": p["vacancy_reason"], "history_url": None, "current_url": None, "reproduction_url": None,
                   "restart_input": "New preregistered cohort outside the first40, same official old/new publication trees; cannot fill this already sealed vacancy post hoc."}
            returns.append(ret)
            t3.append([f'{cid} · {p["project"]} · {LABEL[p["stratum"]]}', "미확인 → 미확인", "결원", "당시·현재·재현 URL 미확인; 새 모집을 먼저 봉인", "음성0 / 양성0 (해당 층)", link("완전 트리·선정 근거", p["project_exposure"]) + "; 새 범위의 경로 부재 후보를 확보해야 재개"])
        else:
            edition_links = f'{link(p["old_version"] + " " + p["old_publication_sha"][:8], blob(old["body_url"], start_line(old)))} → {link(p["new_version"] + " " + p["new_publication_sha"][:8], blob(new["body_url"], start_line(new)))}; source {p["old_source_sha"][:8]}→{p["new_source_sha"][:8]}'
            name = p["old_section_path"].split("/")[-1]
            signal = "옛 자원 경로 있음; 본문 경로 있음; 대응 소스 blob " + ("변경" if p["source_blob_changed"] == "True" else "같음")
            t1.append([f'{cid} · {p["project"]} · {LABEL[p["stratum"]]} · {p["slot"]}', f'{name}; {p["purpose"]}', edition_links, signal, "YES; " + p["prediction_recorded_utc"], "release/tag/pub SHA 등은 선행 노출; 새 본문·그림·개별CI0; 원격봉인22:07:47.803Z"])
            ar = author_returns[cid]
            historical = blob(old["body_url"], start_line(old))
            current = blob(new["body_url"], start_line(new)) if prj == "GG" else ar["current_selected_version_url"]
            reproduction = blob(new["source_url"]) if prj == "GG" else ar["reproduction_source_url"]
            ret = {"case_id": cid, "project": p["project"], "stratum": p["stratum"], "vacant": False,
                   "decision": "두 판 병기" if cid != "MP-C1" else "두 판 병기·새 fragment로 교체",
                   "history_url": historical, "history_location": old["section_locator"], "history_payload_url": old["payload_url"],
                   "current_url": current, "current_location": new["section_url"].split("#")[-1] + " / " + new["section_locator"],
                   "current_fixed_body": blob(new["body_url"], start_line(new)), "current_payload_url": new["payload_url"],
                   "reproduction_url": reproduction, "reproduction_publication_url": new["publication_url"],
                   "G": "미확인", "missing_generation_link": "actual historical invocation/environment/input and per-output digest -> selected publication payload",
                   "cheaper_sufficient_check": "설명 독자는 정확판·정확절을 확인한다. 이미지 재사용이면 절이 참조한 최종 payload까지 확인한다. 생성 귀속·동일 빌드 재현을 요구할 때 실제 job·출력 digest를 추가한다.",
                   "warning": "선택한 발행판의 설명·그림 사용은 확인했지만 최신판 호환성과 당시 생성 빌드의 재현은 미확인입니다.",
                   "source_record": "evidence/ggplot2/returns.json" if prj == "GG" else "evidence/matplotlib/returns.json"}
            returns.append(ret)
            correction = "원 절·그림 역할을 잇는 캡션/코드가 반박되면 U 재판정; G 실행증거 없음."
            if cid == "MP-C1":
                correction = "옛 제목 fragment는 새 DOM에 없음; HBox 첫 그림으로 교정. VBox 추가는 원 HBox 목적의 삭제가 아님."
            t3.append([f'{cid} · {p["project"]} · {LABEL[p["stratum"]]}', "YES → YES", "참양성(TP)", f'{ret["decision"]}: 당시 {link("고정 절", historical)}; 현재 {link("선택 새판 절", current)}; 재현 {link("고정 소스", reproduction)}. 각 첫 그림·직전 코드; G 미확인', "음성0 / 양성2 (해당 층)", link("판독·반대 근거", new["evidence"]) + "; " + correction])
        for row in [old, new]:
            if vacant:
                t2.append([f'{cid} · {row["version"]} · {row["edition"]}', "미확인 — 해당 층 후보 없음", "미확인 — 요청할 예제·자원 미선정", "미확인 / 미확인 / 미확인", link("선정·결원 근거", p["project_exposure"]), "고정 첫40에서 부재층 후보0; 새 범위를 사전 등록한 뒤 재개"])
            else:
                first_receipt = row["receipt"].split(";")[0]
                ref = row["literal_reference"]
                if prj == "MP":
                    ref += "; srcset 동일1x + _2_0x.png 2x"
                t2.append([f'{cid} · {row["version"]} · {row["edition"]}',
                           f'{link(row["section_locator"], blob(row["body_url"], start_line(row)))}; {ref}',
                           f'{link("최종 PNG", row["payload_url"])}; {row["payload_bytes"]} B; SHA-256 {row["payload_sha256"]}',
                           f'{row["P"]} / {row["U"]} / {row["G"]}',
                           f'{link("관측", row["evidence"])} · {link("수신 영수증", first_receipt)} · {link("논리 소스", blob(row["source_url"]))}',
                           "실제 생성 job→이 payload의 출력 digest 연결 없음; 바이트 변경만으로 G 판정 안 함"])
    jwrite("evidence/returns.json", returns)
    weakness = [
        ["주8쌍이 모두 양성이고 부재층4쌍은 결원이다. 보조 탐색도 첫40 내부의 남은20개씩으로 한정된다.",
         "같은 고정 두 판의 첫40 밖 목록에서 부재·잔류 후보를 새로 사전 등록하고, exact section과 모든 대체 참조를 연다.",
         "옛 경로가 남지만 U=NO인 FP, 또는 옛 경로가 없는데 후계 표현 U=YES인 FN을 직접 확인하면 조건별 판단을 수정한다."],
        ["실제16판 자리의 G는 모두 미확인이다. 빈 Actions/check/status 조회는 과거 생성 부재를 입증하지 않는다.",
         "14개 GG·22개 MP 조회의 정확 SHA/날짜 창에 해당하는 보존 job, 입력·환경 lock, 단계별 출력 manifest/digest와 복사 기록을 확보한다.",
         "실제 실행이 선택 PNG를 새로 만들었다는 입력→실행→출력 digest→발행 연결이 생기면 G=YES; 복사만 했음이 입증되면 해당 실행의 G=NO로 바꾼다."],
        ["같은 설명 목적과 같은 방법·주소는 다르다. HBox fragment 변경, coord_flip의 동일 새 PNG 두 방법, 가변 live HTML이 확인됐다.",
         "독자가 시각적 목적과 구체적 API 방법 중 무엇을 보존하려는지 명시하고, MP C1 실제 fragment와 GG coord_flip 두 코드 블록을 다시 대조한다.",
         "고정한 구체적 방법의 후계가 없거나 반환 절·참조 PNG가 바뀐다는 관측이면 U의 목적 단위와 현재 링크 결정을 재검토한다."],
    ]
    jwrite("evidence/final-weaknesses.json", {"headers": ["가장 중요한 불일치·약점", "다음에 열 자료 또는 실행할 입력", "어떤 관측이면 결론을 바꿀지"], "rows": weakness})
    report = "## 1. 모집·예측 표 — 12쌍 자리\n\n" + table(
        ["프로젝트·층·순번", "이전 예제·절·목적", "두 발행판 주소·SHA", "목록에서만 본 신호", "봉인 U 예측 및 시각", "제외·선행 노출·미확인"], t1)
    report += "\n## 2. 판별 표 — 24판 자리\n\n" + table(
        ["예제·판", "해당 절 주소·실제 참조 표현", "요청·패키지 내 최종 위치·지문", "배포 P·사용 U·생성 G", "직접 확인한 내용·반대 근거 주소", "미확인 사유"], t2)
    report += "\n## 3. 오류·반환 표 — 12쌍 자리\n\n" + table(
        ["프로젝트·층·예제", "사전 예측과 관측 U", "참·오귀속·놓침·유보", "당시 인용·현재 이용·재현 목적별 반환 URL과 볼 절", "실제 음성·양성 분모", "판단을 뒤집을 근거·미확인"], t3)
    report += """

# AF-RES-102 — 경로가 남는 것, 절이 쓰는 것, 빌드가 만드는 것

**지정 범위의 조사·판독 완료, 인계 전 저장소 검사 대상.** 12쌍 자리 중 실제 적격 표본은8쌍이고4쌍은 사전 규칙이 허용한 결원이다. 실제16판 자리의 P·U는 모두YES, G는 모두미확인이다. 새판U를 예측한8개YES는 모두 맞았지만 실제 음성이0개여서, 이 결과로 일반 링크 오류율이나 이름 변경 탐지 성능을 주장하지 않는다. 필수 자료 최소량은 검토 후 보수적으로 **111개**이며, 요구된5범주 최소량을 모두 충족한다.

첫 세 표의 단위는 논리 예제 한 개와 두 발행판이다. 결원은 NO나 실제 유보 예측이 아니다. P는 해당 판의 본문에서 끝까지 추적한 payload의 발행 포함이며, 옛 경로 존속은 별도 legacy_path_P다. U는 봉인한 목적을 해당 절이 계속 설명하는지다. G는 바로 그 역사적 실행이 해당 바이트를 새로 생성했는지다. PNG를 새로 내려받았거나 해시가 달라졌다는 사실은 G의 증거가 아니다.

표의 SHA 표시를 줄인 곳은 전체40자리와 원주소가 [predictions.csv](predictions.csv)에 있다. 모든 payload의 전체64자리 SHA-256·위치·영수증은 [lineage.csv](lineage.csv)에 보존했다. raw GitHub HTML은 과거 발행 파일의 소스이며 렌더된 역사적 사이트로 표시하지 않는다. 표의 GitHub blob 행 링크는 그 소스의 정확한 읽기 위치다. “현재 이용”은 조사한 다음 판3.5.0/3.7.0을 뜻하며2026년 최신판이라는 뜻이 아니다.

## Q1. 두 판의 발행 근거와 계약

시작한 통합판은 ac7abc85e12b3a5b5f87b694d00e9511332fe272다. 계획판 ace1a06a13ea435f5cb6a3e340ad24f03f68ecae와의 변경 파일은 중앙 dot-control.json뿐이며 연구 브리프·운영 규칙은 같은 blob이었다. 운영 의존 끝5022d581d8d7a4a359250797d55c79f6b67d219c은 배정 후 이동하지 않았다. 실제 연구 입력은 고정846aa7b644bda67ef2551c3f4fb1ec6f5de9484d이며, 등록 인계판까지 변한 것은 HANDOFF뿐이었다. 인수한 predictions·lineage·counts·RESULT 네 파일은 두 끝에서 같은 blob이다. [계약 대조 및 원주소](evidence/input-contract.json), [실제 session start 영수증](evidence/session-start.json), [manifest](manifest.json).

| 프로젝트·판 | 정식 source tag SHA | 실제 문서 source revision | 고정 발행 commit / 범위 |
|---|---|---|---|
| ggplot2 3.4.0 | 63125db184b6e7d5516007574b5d15acbfd8f470 | 같은 tag | [57852124c86f770dd443fcf5064d30ea320a4731](https://github.com/tidyverse/ggplot2/commit/57852124c86f770dd443fcf5064d30ea320a4731), gh-pages reference/ |
| ggplot2 3.5.0 | a6f1a7c845bfe056ef952b839d2fd65b888ab5cd | 같은 tag | [392175bbb00b04025aa5d17a0c18b3896adeb40f](https://github.com/tidyverse/ggplot2/commit/392175bbb00b04025aa5d17a0c18b3896adeb40f), gh-pages reference/ |
| Matplotlib 3.6.3 | c23ccdde6f0f8c071b09a88770e24452f2859e99 | 655f616e86e2c0f7724d7c88717d4ac4eb438c57 | [f3ac5407f8ffc861cae1ea87eddd06c63b222e4b](https://github.com/matplotlib/matplotlib.github.com/commit/f3ac5407f8ffc861cae1ea87eddd06c63b222e4b), 3.6.3/ |
| Matplotlib 3.7.0 | d6dd1b79142e4e2483244c25ff1e3ddb664722d3 | 235131a6bc2527aee7eea370fd5f94564a48c20d | [410d8388303fab638bbedbd1d2eace0e5efb0de9](https://github.com/matplotlib/matplotlib.github.com/commit/410d8388303fab638bbedbd1d2eace0e5efb0de9), 3.7.0/ |

ggplot2는 tag를 명시한 최초 발행을 골랐고, Matplotlib은 정식3.6.3 추가·3.7.0 final 발행 커밋을 골랐다. Matplotlib HTML의 실제 버전은 각각 v3.6.3-3-g655f616e86과 v3.7.0-3-g235131a6bc다. source tag와 문서 revision을 같다고 가정하지 않았다. 요청된 matplotlib.github.io 저장소 API는404였고, 실제 공식 발행 저장소 matplotlib.github.com을 직접 확인했다. 실패 응답은 [실패 색인](evidence/failure-index.json)에 보존했다.

ggplot2의 CRAN3.4.0/3.5.0 소스 묶음은 각각888/966멤버였다. 선택한 DESCRIPTION·주4개 Rd를 직접 읽고8/8 tag 소스 일치를 확인했다. 그 소스 묶음에는 생성 reference HTML/선택PNG가 없다. Matplotlib의 공식 gallery_python.zip은521/522멤버의 Python 예제 소스 묶음이고 전체HTML 보관본은 아니다. 실제 docs revision, Download Python, ZIP 멤버는 주8판에서8/8 SHA가 일치했다. 웹 발행 포함 P는 별도의 완전한 발행 트리와 수신 payload로 확인했다. [GG 배포 감사](evidence/ggplot2/distribution-audit.json), [MP 배포·소스 연결](evidence/matplotlib/source-distribution-links.json).

## Q2–Q3. 결과 전 선정과 경로만의 예측

옛 페이지 경로를 정렬하여 ggplot2 reference195개 중 앞68경로를 검사해40적격, Matplotlib gallery608개 중 앞47경로를 검사해40적격을 얻었다. [frame.csv](frame.csv)는115개 검사행과 각 제외 이유를 남긴다. AF-RES-098의6개 주 논리 예제는 제외했고, 자동 스캔만 한 페이지는 새 고유 자료로 세지 않았다. Matplotlib의 원래 inline animation12개는 외부 경로 삭제로 취급하지 않았다.

일반층은 프로젝트 이름의 대소문자까지 고정한 SHA-256(AF-RES-102|프로젝트|옛 절 경로)의 앞2개다. ① 원격 커밋 뒤에만 새 트리와 대응 소스 blob을 열었다. ggplot2는40개 옛 자원 경로가 모두 남고40개 Rd blob이 달랐다. 일반2개를 빼면 변경층 후보38개다. Matplotlib은 외부 자원28개 경로가 모두 남고, 변경층 적격은6개였다. 각각 같은 hash 순서로2개를 고르고 두 부재층은2개씩 공석으로 두었다. [GG 선정 노출 일지](evidence/ggplot2/stage2.json), [MP 선정 노출 일지](evidence/matplotlib/stage2.json).

예측 규칙은 정확한 옛 상대 경로가 남으면YES, 완전한 트리에서 없으면NO, 불완전·모호하면유보다. 실제8개는 모두YES였다. 이 규칙은 별칭, 새 이름, data URL, 삭제된 본문이 남긴 파일, 바뀐 목적을 의도적으로 읽지 않는다. 새 본문 경로 존재와 source blob 변화는 층 선정 신호이며 U 판정의 대체물이 아니다.

| 봉인·열람 사건 | UTC | 증거 |
|---|---|---|
| ① 이전 모집·일반층 원격 확인 | 2026-11-23T22:03:18.088Z | [5f664a87df16f453151ec985e9ad37913e3bda90](https://github.com/laadkke-arch/agentflow-open/commit/5f664a87df16f453151ec985e9ad37913e3bda90) |
| 새 경로 목록 첫 노출 | 2026-11-23T22:03:53.099Z | 단계2 노출 영수증; 아직 본문·그림·개별CI0 |
| GG / MP 예측 파일 기록 | 22:04:03.902910 / 22:04:24.934583Z | [predictions.csv](predictions.csv) |
| ② 예측 원격 봉인 확인 | 2026-11-23T22:07:47.803Z | [f1c5d6ff927fd5fbe108565598810ca7e94c5753](https://github.com/laadkke-arch/agentflow-open/commit/f1c5d6ff927fd5fbe108565598810ca7e94c5753) |
| 첫 새 본문 요청 시작 | GG 22:08:32.363481Z; MP 22:08:40.563576Z | [별도 검토](evidence/cross-domain/review-stage3.json); 모두 원격 봉인 뒤 |
| ③ 사후 근거 원격 확인 | 2026-11-23T22:24:55.653Z | [be9c4cfa09a59da937d40f71cdf7c675fb42c0fa](https://github.com/laadkke-arch/agentflow-open/commit/be9c4cfa09a59da937d40f71cdf7c675fb42c0fa) |

GG audit의 첫 새 본문22:08:38.727319Z는 관측 응답 시점이며, 위 요청 시작과 구별한다. release/tag/publication SHA·메타데이터·이전 작업에서 알려진 새판 발행 계보는 미리 보았다. 이 노출을 숨긴 완전 맹검이라고 주장하지 않는다. 봉인 전에 새 본문·그림·개별 job을 읽지 않았다는 더 좁은 순서를 확인했다. [stage1 지문](evidence/stage1-seal.json), [예측 지문](evidence/prediction-seal.json), [단계별 원격SHA·변경 파일](evidence/checkpoints.json).

## Q4. 실제 절, 참조, 그림과 목적

ggplot2는 정확 ref-examples 경계, Matplotlib은 동급 section 닫힘까지 읽었다. img/srcset/picture/source/base, inline SVG·data URI·script·object 등의 대체 표현을 조사했고 선택 주8예제의16판에서는 실제 img와 MP의2x srcset이 사용됐다. 최종 PNG와 source를 직접 열고 형식·크기·지문·Git blob을 확인했다. 주 PNG의 역할도 그림으로 대조했다. 별도 검토자가16절의 경계를 다시 계산하고24payload(GG8, MP1x/2x16)의 지문과 PNG·발행 tree를 재검산했다. [GG 판독](evidence/ggplot2/audit.json), [MP 판독](evidence/matplotlib/audit.json), [별도 검토](evidence/cross-domain/review-stage3.md).

모든 주8쌍은 PNG 바이트가 달라졌지만 봉인한 설명 목적은 이어졌다. ggplot2 주4개의 Rd 예제 블록은 모두 같았다. GG-G1·C1의 Rd blob 변경은 원본 파일명 .r→.R 한 줄이며, G2·C2도 주변 설명 변경과 실제 예제 변경을 구분했다. 특히 geom_count의 단위는 뒤의 count-size 그림이 아니라 첫 일반 geom_point 기준 산점도다.

Matplotlib G1·G2·C2는 첫 그림 픽셀이 같고 C1은 픽셀도 달라졌다. C1은 옛 HBoxDivider 같은 높이 목적을 새 첫 그림에서 유지하면서 VBoxDivider 같은 너비 예제를 두 번째로 추가했다. [저자 변경8ecd60dc](https://github.com/matplotlib/matplotlib/commit/8ecd60dc48e8767282656c8633415fda1be8beeb), 실제 배포 소스, 캡션과 그림을 함께 대조했다. 옛 #hboxdivider-demo는 새 DOM에 없으므로 #hboxdivider-and-vboxdivider-demo로 교정했다. 공통 생성소스 앵커 #sphx-glr-gallery-axes-grid1-demo-axes-hbox-divider-py도 두 판에서 확인했다. U=YES가 옛 fragment의 유효성까지 보장하지 않는다.

현재 matplotlib.org/3.7.0의 네 반환 페이지는 HTTP200이지만 완전 HTML 바이트는 최초 고정 발행본과4/4 달랐다. 이 엄격한 비교는 종료1의 실패 관측으로 보존했다. 같은 수신 자료에서 정확 절의 정규화 본문·모든 img 속성은4/4 같았고, 실제1x/2xPNG8개를 다시 요청하니8/8 고정 SHA와 같았다. 따라서 관측시각의 독자용 절 링크를 줄 수 있지만 완전 HTML의 불변성을 약속하지 않는다. [전체 비교 실패](evidence/return-url-checks.json), [절 비교](evidence/return-url-scope-comparison.json), [PNG 성공 비교](evidence/live-payload-checks.json).

## Q5. P와 U가 확인되어도 G를 비워 둔 이유

공식 발행 tree·payload 수신은 P를, exact section의 실제 참조와 논리 소스는 U를 확인한다. tag/release 기록은 판을 식별한다. 빌드 규칙은 가능한 절차를 보여주지만 실제 실행·출력과의 연결을 대신하지 않는다.

ggplot2 workflow는 사이트 생성과 docs→gh-pages 배포를 나눈다. pkgdown의 로컬 목적지 정리와 배포 action의 clean:false는 서로 다른 단계다. 후자는 목적지 잔류를 허용하지만 이번 그림이 실제 잔류라는 증거는 아니다. Matplotlib release guide는 release 태그 설치와 ver-doc 문서 소스, 빌드 후 발행 저장소로 rsync를 구분한다. CircleCI deploy-docs.sh는 devdocs 경로이며 선택 정식판 발행의 실행 증거로 쓰지 않았다. html-noplot 경로의 존재도 이번 실행이 이를 탔다는 뜻은 아니다.

GG는 tag2·발행2 SHA 각각의 Actions/check/status12조회와 날짜 창2조회, MP는 tag/docs/pub6 SHA의18조회와 날짜 창4조회다. 총수는14/22이며 모두HTTP200, 보이는 항목0이다. 검색 범위·URL·시각·빈 응답을 남겼다. 보존 정책 때문에 사라졌는지, 다른 시스템에서 실행했는지도 미확인이다. combined status의 빈 pending을 실제 실행 중 job으로 읽지 않았다. [GG 검색](evidence/ggplot2/build-search.json), [MP 검색](evidence/matplotlib/generation-search.json).

G를 바꿀 최소 증거는 실제 실행 ID와 입력 source/environment, 해당 출력 manifest/digest, 발행 파일까지의 복사 연결이다. 새로 로컬 재빌드에 성공해도 그 성공은 당시 생성 기록이 되지 않는다. R·Python 예제 실행, 브라우저/JS 실행, 역사적 빌드 재현은 미실시이며 P/U의 정적 근거와 혼동하지 않았다.

## Q6. 층별 혼동표와 반례 탐색

"""
    report += table(["프로젝트", "층", "TP", "FP", "FN", "TN", "유보", "결원", "실제 양성/음성", "FNR", "FPR·특이도"], [
        [s["project"], LABEL[s["stratum"]], s["TP"], s["FP"], s["FN"], s["TN"], s["abstention"], s["vacancy"],
         f'{s["actual_positive"]}/{s["actual_negative"]}', s["false_negative_rate"]["display"], "산출 불가(음성0)"] for s in strata])
    report += """

일반층과 변경층의 FNR=FN/(TP+FN)은 각각0/2로 계산할 수 있다. FPR와 특이도의 실제 음성 분모는0이므로 산출 불가다. 부재층의 양성·음성 분모는 모두0이다. 같은 이유로 이름이 사라진 조건의 후계 탐지 성능도 계산할 수 없다. 세 층을 합친 비율은 내지 않았다. [기계 판독 집계](counts.json).

주 표본에서 못 찾은 반례는 봉인한 첫40 후보의 남은36개 가운데 hash순 앞20개씩만 보조 조사했다. 이 상한은 결과를 보기 전 SCOPE에 정했다. 전체 사이트의 남은 모든 예제를 조사했다고 쓰지 않는다. MP 보조3개 inline animation은 실제 dataPNG 첫 프레임을 디코딩했지만 애니메이션을 실행하지 않았다. 098의 보조 animate_decay·bayes_update는 고정 탐색 순서에서는 보존하고 신규 자료 수에서 제외했다.

| 요구한 반례 | ggplot2 보조20 | Matplotlib 보조20 | 해석 |
|---|---|---|---|
| ① 경로 있음 / 절이 안 씀 | 발견0/20 | 외부 경로17개에서0/17; 원래 내장3개 별도 | 이 범위에서 못 찾음. 전체 잔류 오류가 없다는 결론 아님 |
| ② 옛 경로 없음 / 새 이름·내장으로 지속 | 부재 조건 분모0 | 부재 조건 분모0 | 두 부재층4쌍 결원을 유지 |
| ③ 같은 이름·해시 / 목적 변경 | 동일 첫 PNG 양판1쌍(fortify.lm), 목적 유지; 발견0/1 | 동일 바이트 조건0쌍 | 분모 없는 유형의 오류율0을 만들지 않음 |
| ④ 다른 바이트 / 같은 절 목적 | 19/20 | 20/20 | 목적 identity와 payload identity는 다름; 일반 오류율 아님 |

보조 GG-S13 coord_flip는 반대 해석을 검토하는 핵심 사례다. 고정 목적은 수평 가격 boxplot이다. 옛 첫 코드는 coord_flip(), 새 첫 코드는 x/y aesthetics를 교환한다. 새 두 번째 블록에 원래 coord_flip 방법이 계속 있고 저자가 두 방법을 연결한다. [새 NEWS L49–51](https://github.com/tidyverse/ggplot2/blob/a6f1a7c845bfe056ef952b839d2fd65b888ab5cd/NEWS.md#L49), [새 두 코드 블록](https://github.com/tidyverse/ggplot2/blob/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/coord_flip.html#L140).

새 coord_flip-1.png와 coord_flip-2.png는38,884B, SHA-256 5b83ffa8756ebf4b4fc3cad479388874578dc018d6dc72915b90660d4020d563으로 동일하다. 시각적 목적은YES지만 구체적 coord_flip 방법을 찾는 독자에게는 새 두 번째 블록을 줘야 한다. 옛 경로는 남고 옛 바이트는 달랐으므로 이를 정확한 유형②·③ 적중으로 세지 않았다. 동일 바이트가 곧 동일 방법이라는 초기 단순 결론은 이 사례가 반박한다. [보조 상세](evidence/ggplot2/supplemental-audit.json).

## Q7. EPUB·wheel에서 검토한 수록과 실제 참조

| 분야·새 실물 | 직접 읽은 규격과 실물 | 관측한 관계 | 만들지 않은 주장 |
|---|---|---|---|
| IDPF Trees EPUB20230704 | container→EPUB/package.opf; ZIP12, manifest9, spine3; titlepage body#titlepage L28–41; [실물](https://github.com/IDPF/epub3-samples/releases/download/20230704/trees.epub), [규격](https://www.w3.org/TR/2024/REC-epub-rs-33-20241017/#sec-scripted-content) | cover.jpg는 수록YES이지만 선택 titlepage 본문이 정적으로 참조하지 않음. 실제 본문은 canvas와4JS, tree.js/Snake에 연결 | reader의 책장·별도 표지 표시 NO, JS 실제 실행, 당시 생성G는 주장하지 않음 |
| build1.2.2.post1 wheel | ZIP19=RECORD19, 비어 있지 않은 hash/size18/18 일치; entry_points 두 이름→build.__main__:entrypoint; [실물](https://files.pythonhosted.org/packages/84/c2/80633736cd183ee4a62107413def345f7e6e3c01563dbca1417363cf957e/build-1.2.2.post1-py3-none-any.whl), [wheel규격](https://packaging.python.org/en/latest/specifications/binary-distribution-format/), [entry-point규격](https://packaging.python.org/en/latest/specifications/entry-points/) | RECORD는 수록과 지문, entry_points는 호출 대상 선언. 함수는L444–445, main guard는L448–449. ZIP에 설치 wrapper 없음 | 설치·wrapper 생성·실제 entrypoint 호출·역사적 빌드G는 미확인 |

Trees cover JPEG는400×393·32,681B이며 SHA-256 85e2083c66d98ac55253c438e387111a0b2cc6a67f1b16920275979c56b1ff75다. 본문3개·CSS·JS4개를 읽어 선택 본문의 이미지 참조를 찾았고 manifest의 cover-image 메타데이터와 별도 관계로 남겼다. 이는 “패키지에 있음→그 페이지가 그림을 보여줌”의 구체적 반례다. 패키지를 수록 위치로 주는 링크와 실제 표시 문맥을 주는 링크는 구별해야 한다.

wheel은22,950B, SHA-256 1d61c0887fa860c01971625baae8bdd338e517b836a2f70dd1f7aa3a6b2fc5b5다. RECORD 자기 행의 hash/size가 빈 것은 규격상 허용되며 나머지18개를 직접 검산했다. console_scripts의 pyproject-build와 pipx.run의 build가 같은 함수를 선언하지만 실행 관측은 없다. “선언→실행”이라는 추론을 뒷받침할 증거가 없음을 확인한 사례이며 실제로 한 번도 실행되지 않았다는 NO 관측은 아니다. [교차 분야 분석](evidence/cross-domain/cross-domain.md), [실물 감사](evidence/cross-domain/audit.json), [다른 작성자의 정적 재검산](evidence/ggplot2/review-cross-domain.md).

실제 패키지·규격 주소와 고정 소스 SHA는 [교차 분야 원장](evidence/cross-domain/sources.jsonl)에 있다. Cole/Moby-Dick은 새 사례로 쓰지 않았다. 추가 Children’s Literature 탐색은 원하는 비spine 반례를 만들지 못한 결과도 보존했고 최소량에는 넣지 않았다.

## 후속 설계자가 선택할 링크 반환 방식

이 묶음은 제품 DB나 최종 구현을 확정하지 않는다. 독자 목적에 따라 다음 대안을 채택하거나 버릴 수 있다.

| 반환 대안 | 충분한 확인 | 얻는 것·대가 | 실패 조건과 한 줄 경고 |
|---|---|---|---|
| 옛판 유지 | 고정 발행 SHA·정확 절·연결 payload | 당시 논거 보존; raw HTML은 소스 읽기 필요 | “당시 설명이며 현재 API 호환성은 확인하지 않았습니다.” |
| 새 위치로 교체 | 원 목적을 잇는 본문·소스·저자 연결과 실제 새 참조 | 지금 조사한 판에서 이용 가능; 옛 모습은 달라질 수 있음 | “목적은 이어지지만 이름·방법·모양은 달라질 수 있습니다.” |
| 두 판 병기 | 위 두 확인을 연결 | 역사 인용과 다음 판 이용을 함께 지원; 선택 부담 증가 | “판별 목적은 같아도 같은 바이트나 같은 빌드를 뜻하지 않습니다.” |
| 본문 절만 제공 | 질문이 설명 독해이며 파일 재사용·생성 귀속을 요구하지 않음 | 가장 싼 확인으로 충분; payload 독립 검증은 생략 가능 | “그림 파일을 재사용할 때에는 이 절의 실제 참조를 더 확인하세요.” |
| 유보 | 불완전 tree, 불명확한 후계, 필요한 실행 연결 미확보 | 오귀속 방지; 즉시 usable asset을 주지 못함 | “수록·사용·생성 중 필요한 연결이 아직 확인되지 않았습니다.” |

주 사례는 목적별 두 판 병기를 기본으로 하고 MP-C1의 새 fragment를 교정했다. 설명을 읽는 독자에게는 절만으로 충분하며, 파일 재사용에는 그 절이 실제 연결한 payload와 지문을 추가한다. 당시 빌드 재현에는 source와 발행 SHA만으로 부족하다. [사례별 반환·비용조건·경고](evidence/returns.json).

## 자료 수, 수정, 검토와 재현

최종 sources.jsonl은477행이며 신규 고유 자료111개다. 같은 저작의 양판·미러·동일 바이트, 패키지 멤버와 본체, 자동 모집만 한 자료, 실패 요청, 빈 job조회,098 계승 자료는 중복 계산하지 않는다. release·발행·소스·규칙의 공통 계보도 표시했다. 이 숫자는111개의 독립 실험을 뜻하지 않는다.

"""
    report += table(["최소량 범주", "요구", "확인·산입"], [
        ["실제 판별 예제 본문", 8, 46], ["서로 다른 payload/예제 소스", 8, 45],
        ["발행·변경·릴리스·빌드 근거", 8, 15], ["EPUB 규격·새 패키지", 2, 2], ["wheel 규격·새 패키지", 2, 3], ["합계", 28, 111]])
    report += """

별도 검토는 원본 작성과 분리한 AI 작업자가 수행했으며 사람 검토는 없다. 모집·예측 검토는21개+18개 봉인 지문,80개 후보 hash와12자리 선정을 확인했다. 사후 검토에서 ggplot2 빌드규칙5개가098과 같은 저작(그중2개 동일 SHA)임을 찾아, 단계3의 잠정116에서 최종111로 수정했다. 원천 GG ledger의57은 당시 작성자 집계로 남고, 최종 root ledger는52+54+5로 계산한다. [검토 반영 집계](evidence/source-reconciliation.json).

그 밖에 CSV 줄끝 정규화, MP의 section 경계 줄수, 세미콜론 없는 inline-frame 파서, 실제 SHA가 없는 비교값을 같다고 처리하지 않기, 불완전 트리 조기 중단, 교차 분야 재현 스크립트가 파일을 다시 쓴다는 문구를 교정했다. 수정된 재현 코드가 과거 봉인 파일을 덮어쓰지 않도록 별도 사본에서 실행하도록 안내했다. 자료 오류와 실제 관측 실패는 각각 [실패 색인](evidence/failure-index.json), [MP 자체 수정](evidence/matplotlib/self-corrections.json), [교차 검토](evidence/ggplot2/review-cross-domain.md)에 보존했다.

[SELF_CHECK.md](SELF_CHECK.md)는 Q1–Q7의 답·반대 근거·판단을 바꿀 최소 확인을 남긴다. [reproduce.md](reproduce.md)는 예측만 먼저 읽는 절차와 사후 공개 순서, 실제 검증 명령을 분리한다. 이 결과를 커밋한 정확한 SHA에서 session check와 cloud_check를 실행한다. 실행 후 추가되는 검증 영수증 및 마지막 HANDOFF는 검사한 SHA·UTC·종료값·실제 자동 세션 수·미실시를 구별한다. 그 후의 영수증/인계 문서를 앞 검사에 포함됐다고 표시하지 않는다.

## 남기는 세 가지 약점

"""
    report += table(["가장 중요한 불일치·약점", "다음에 열 자료 또는 실행할 입력", "어떤 관측이면 결론을 바꿀지"], weakness)
    (ROOT / "RESULT.md").write_text(report)
    print(json.dumps({"required_table_rows": [len(t1), len(t2), len(t3)], "strata": len(strata), "new_primary_sources": sources["countable"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
