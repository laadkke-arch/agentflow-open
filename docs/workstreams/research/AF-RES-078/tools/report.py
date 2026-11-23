"""Generate the three required tables, comparisons and explicit cost counts."""

from collections import Counter, defaultdict
import csv

from fixturegen import CASES_I, CASES_T, OWNED, digest, json_text, read_lines

OUTCOMES = ("true_support", "true_reject", "false_accept", "false_reject", "hold", "ineligible")
DISPLAY_SCENARIO = {"normal": "정상", "edge": "봉인 경계", "retry": "중단·재시도"}
DISPLAY_TRUTH = {True: "support", False: "reject", None: "unknown"}


def load_csv(name):
    with (OWNED / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(name, fields, rows):
    with (OWNED / name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def choose_runs(runs):
    result = defaultdict(list)
    for run in runs:
        if run["attempt"] != "stop":
            result[(run["domain"], run["cell"], run["scenario"])].append(run)
    return result


def truths(rows, condition):
    # An old product can be inspected but never satisfies the current execution.
    votes = [
        row["adoption"] if condition == "all"
        else row["phase_status"] == "complete" and row["final"]["conditions"][condition]
        for row in rows
    ]
    return votes[0] if len(set(votes)) == 1 else None


def compare(prediction, truth):
    if truth is None:
        return "ineligible"
    if prediction == "hold":
        return "hold"
    if prediction == "support":
        return "true_support" if truth else "false_accept"
    return "false_reject" if truth else "true_reject"


def compare_all(runs):
    chosen = choose_runs(runs)
    predictions = load_csv("predictions.csv") + load_csv("evidence/c-heldout-predictions.csv")
    details = {}
    for p in predictions:
        details[(p["view"], p["domain"], p["cell"], p["scenario"], p["condition"])] = p
    for (domain, cell, scenario), rows in sorted(chosen.items()):
        scope = "held_prediction" if scenario == "edge" else "primary"
        for cond in (*(CASES_T if domain == "T" else CASES_I), "all"):
            truth = truths(rows, cond)
            ids = " ".join(r["run"] for r in rows)
            for view in "ABC":
                if view == "C" and scope == "primary":
                    vote = "hold" if truth is None else DISPLAY_TRUTH[truth]
                    basis, reason = ids, "Same-run diagnostic readout, using observed output"
                    layer = "primary_diagnostic"
                else:
                    p = details[(view, domain, cell, scenario, cond)]
                    vote, basis, reason = p["prediction"], p["basis"], p["reason"]
                    layer = scope
                yield dict(view=view, layer=layer, domain=domain, cell=cell, scenario=scenario,
                           condition=cond, prediction=vote, truth=DISPLAY_TRUTH[truth],
                           judgment=compare(vote, truth), truth_runs=ids, basis=basis, reason=reason)


def aggregate(rows):
    result = defaultdict(Counter)
    for row in rows:
        match = row["view"], row["layer"]
        own, condition, vote = row["domain"], row["condition"], row["judgment"]
        result[(*match, own, condition)][vote] += 1
        if condition == "all":
            result[(*match, "both", condition)][vote] += 1
        else:
            for key in (own, "both"):
                result[(*match, key, "each_total")][vote] += 1
    ranked = []
    for (view, layer, domain, condition), values in sorted(result.items()):
        counts = {field: values[field] for field in OUTCOMES}
        ranked.append(dict(view=view, layer=layer, domain=domain, condition=condition,
                           total=sum(counts.values()), eligible=sum(counts.values()) - values["ineligible"], **counts))
    return ranked


def cost(run):
    status = run["phase_status"]
    return dict(run=run["run"], domain=run["domain"], scenario=run["scenario"], fixture=run["fixture"],
                processes=len(run["events"]), pipeline_steps=sum(e["stage"] in ("front", "back") for e in run["events"]),
                setup_steps=sum(e["stage"] == "prior" for e in run["events"]),
                verifier_steps=sum(e["stage"].startswith("oracle_") for e in run["events"]),
                original_bytes=run["bytes"]["original"], interchange_bytes=run["bytes"]["middle"],
                visible_final_bytes=run["bytes"]["final"],
                final_generation=("current" if status == "complete" else "previous")
                if run["bytes"]["final"] is not None else "absent",
                external_fetches=0)


def md_row(*cells):
    return "| " + " | ".join(str(value).replace("|", "\\|").replace("\n", " ") for value in cells) + " |\n"


def path_hash(snapshot, root, rel=None):
    if rel is not None:
        return snapshot.get(rel, {}).get("sha256")
    selected = {p: v["sha256"] for p, v in snapshot.items() if p.startswith(root + "/") and "sha256" in v}
    return digest(json_text(selected).encode("utf-8")) if selected else None


def run_hashes(row):
    states = row["snapshots"]
    start, middle, end = states["before_front"], states["after_front"], states["after_back"]
    if row["domain"] == "T":
        return path_hash(start, "", "source.db"), path_hash(middle, "", "exchange.csv"), path_hash(end, "", "final.jsonl")
    return path_hash(start, "source"), path_hash(middle, "stage"), path_hash(end, "", "artifact.zip")


def tables_one():
    c = load_csv("contracts.csv")
    output = "## 표 1. 단계와 계약\n\n"
    output += md_row("단계", "도구와 판", "두 계약의 해당 근거절", "입력 / 출력 역할", "사용자 필수조건", "깨지는 경계")
    output += md_row(*("---" for _ in range(6)))
    proofs = [
        "[T02 CLI §7.6](https://sqlite.org/cli.html#csv_export), [고정 output_csv](https://github.com/sqlite/sqlite/blob/version-3.46.1/src/shell.c.in#L2036-L2059)",
        "[T04 v3.13.5 reader/QUOTE_NOTNULL](https://raw.githubusercontent.com/python/cpython/v3.13.5/Doc/library/csv.rst), [T05 판 변화](https://github.com/python/cpython/issues/113732)",
        "[I01 exif_transpose](https://github.com/python-pillow/Pillow/blob/13.0.0/src/PIL/ImageOps.py#L690-L747), [스테이징](tools/convert.py)",
        "[I08 zip(1) -j/-@/add](https://manpages.debian.org/trixie/zip/zip.1.en.html), [I13 APPNOTE](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)",
    ]
    requirements = ["SQL 타입과 키, 인용 필드와 논리 행 수", "같은 키의 NULL/빈 텍스트/리터럴과 쉼표·따옴표·줄바꿈", "원래 상대 식별자, 표시 크기와 픽셀 코너", "원 이름별 1회 읽기, 전체 멤버 수와 코너 유지"]
    limits = ["NULL 표기 충돌, TEXT 내부 NUL", "기본 문자열 읽기, 3.12 reader 차이, 헤더 없는 빈 결과", "스테이징 이름 충돌, 태그와 원시 픽셀 불일치", "basename 충돌, 기존 아카이브에 남은 멤버, 파일명 디코딩"]
    for ix, row in enumerate(c):
        output += md_row(row["domain"] + " " + row["stage"], row["tool_version"], proofs[ix], row["input_role"] + " → " + row["output_role"], requirements[ix], limits[ix])
    return output


def tables_two(runs):
    loc = {run["run"]: ix for ix, run in enumerate(runs, 1)}
    output = "\n## 표 2. 실행별 근거와 첫 손실\n\n"
    output += "지문은 SHA-256 앞 12자리다. I의 입·중간 지문은 경로→개별 파일 SHA의 정렬 JSON 지문이다. 없음은 완성품 경로에 파일이 없음을, 이전은 현재 입력으로 게시된 파일이 아님을 뜻한다. 실행 링크에서 확정된 값·크기·모서리와 전체 지문을 읽을 수 있다.\n\n"
    output += md_row("분야", "셀", "시나리오", "run", "입력 / 중간 / 끝 지문", "독립 정답", "부품별 / 조합 판정", "첫 손실 지점")
    output += md_row(*("---" for _ in range(8)))
    order = {"normal": 0, "edge": 1, "retry": 2, "stop": 0, "resume": 1}
    arranged = sorted(runs, key=lambda run: (
        run["domain"] == "I", run["cell"], order[run["scenario"]],
        run["attempt"] if isinstance(run["attempt"], int) else order[run["attempt"]],
    ))
    for run in arranged:
        ident = run["run"]
        expected = run["expected"]
        ph = run["phase_status"]
        stamps = [s[:12] if s else "없음" for s in run_hashes(run)]
        if ph in ("interrupted", "back_failed") and stamps[-1] != "없음":
            stamps[-1] += " (이전)"
        if run["domain"] == "T":
            expected_info = f"{len(expected)}행·키별 타입/값({run['fixture']})"
        else:
            expected_info = ", ".join(f"`{p}` {r['size'][0]}×{r['size'][1]}" for p, r in expected.items()) + "·코너"
        labels = " ".join(f"{e['stage']}={e['exit']}" for e in run["events"] if e["stage"] in ("front", "back"))
        all_answer = "지지" if run["adoption"] else "배제"
        losses = defaultdict(list)
        for condition, step in run["first_loss"].items():
            losses[step].append(condition)
        fatal = " / ".join(f"{step} {','.join(conditions)}" for step, conditions in losses.items()) or "관측 없음"
        output += md_row(run["domain"], run["cell"], DISPLAY_SCENARIO[run["scenario"]], f"[{ident}](runs.jsonl#L{loc[ident]})",
                         " / ".join(stamps), expected_info, f"{labels} · {all_answer}", fatal)
    return output


def tables_three(aggregate_rows, costs, solo):
    output = "\n## 표 3. 보기별 적격 분모와 비용\n\n"
    output += "주 표본은 정상과 중단 후 재시도다. C의 주 진단은 같은 실행을 읽은 사후 결과다. 봉인 층의 C는 경계 입력 공개 전에 저장한 예측이다. 두 반복의 의미 판정이 다르면 해당 조건은 적격 분모에서 제외한다.\n\n"
    output += md_row("보기", "평가층", "적격 분모", "참지지 / 참배제 / 거짓채택 / 거짓배제 / 보류", "비용")
    output += md_row(*("---" for _ in range(5)))
    for row in aggregate_rows:
        if row["condition"] not in ("all", "each_total") or row["domain"] == "both":
            continue
        domain, view, layer = row["domain"], row["view"], row["layer"]
        if view in "AB":
            scoped = [s for s in solo if s["domain"] == domain]
            cost_label = f"단독 {len(scoped)}회 공유" + (" + 계약 2행" if view == "B" else "")
        elif layer == "primary_diagnostic":
            scope = [p for p in costs if p["domain"] == domain and p["scenario"] != "edge"]
            cost_label = f"주 {len(scope)}시도·{sum(p['pipeline_steps'] for p in scope)}단계 실측"
        else:
            cost_label = "정상 기록 8행 재사용·예측 시 새 실행 0"
        subject = "모두 충족" if row["condition"] == "all" else "요건 합산"
        phase = {"primary": "주 예측", "held_prediction": "봉인 예측", "primary_diagnostic": "주 사후 진단"}[layer]
        output += md_row(view, f"{domain} {phase} · {subject}", f"{row['eligible']}/{row['total']}",
                         " / ".join(str(row[c]) for c in OUTCOMES[:-1]), cost_label)
    output += "\n요건별 전체 행을 [evidence/counts.csv](evidence/counts.csv)에서, 개별 예측과 정답을 [comparisons.csv](comparisons.csv)에서 볼 수 있다.\n"
    return output


def main():
    runs = read_lines(OWNED / "runs.jsonl")
    solo = read_lines(OWNED / "evidence/solo.jsonl")
    comparisons = list(compare_all(runs))
    summary = aggregate(comparisons)
    costs = [cost(r) for r in runs]
    for name, rows in [("comparisons.csv", comparisons), ("evidence/counts.csv", summary), ("evidence/costs.csv", costs)]:
        write_csv(name, tuple(rows[0]), rows)
    text = "# AF-RES-078 조합 검증 결과\n\n" + tables_one() + tables_two(runs) + tables_three(summary, costs, solo)
    sections = (OWNED / "tools/result-sections.md").read_text(encoding="utf-8")
    (OWNED / "RESULT.md").write_text(text + "\n" + sections, encoding="utf-8")


if __name__ == "__main__":
    main()
