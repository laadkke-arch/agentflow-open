"""Verify the sealed, replayed ledgers and reconstruct the first three report tables."""
import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from compare import stamp
from replay import runner_envelope
from structure import digest, jsonl

HERE = Path(__file__).resolve().parent.parent


def csv_rows(name):
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def open_json(name):
    return json.loads((HERE / name).read_text())


def frame_check():
    frame = csv_rows("frame.csv")
    scan = csv_rows("evidence/frame-scan.csv")
    attempts = jsonl(HERE / "evidence/attachment-attempts.jsonl")
    outcome = {}
    for project in "EM":
        pool = [r for r in scan if r["project"] == project]
        chosen = [r for r in frame if r["project"] == project]
        screened = [r for r in pool if r["keywords"]]
        assert not any(r["error"] for r in pool)
        assert len(chosen) == 60
        assert [r["issue_id"] for r in chosen] == [r["issue_id"] for r in screened[:60]]
        key = lambda row: (row["created_utc"], int(row["issue_id"]))
        assert pool == sorted(pool, key=key)
        assert chosen == sorted(chosen, key=key)
        assert pool[-1]["created_utc"] > chosen[-1]["created_utc"]
        assert [int(r["keyword_rank"]) for r in chosen] == list(range(1, 61))
        outcome[project] = {
            "opened_for_frame": len(pool), "ranked": len(chosen), "edge_issue": chosen[-1]["issue_number"],
            "body_errors": 0, "attachment_state": dict(Counter(r["attachment_state"] for r in chosen)),
            "duplicate_flag": [r["row"] for r in chosen if r["duplicate_flag"]],
            "multi_url": [r["row"] for r in chosen if r["multiple_attachment_candidates"] == "true"],
            "timestamp_ties_before_cutoff": sum(
                a["created_utc"] == b["created_utc"] and key(b) <= key(chosen[-1])
                for a, b in zip(pool, pool[1:])
            ),
        }
    return outcome, dict(Counter(a["status"] for a in attempts))


def views_check(views):
    checked = 0
    per_case = defaultdict(dict)
    for v in views:
        text = v["text"]
        assert len(text) == v["chars"] <= v["budget"] <= 1600
        assert v["open_view_sha256"] == digest(text.encode())
        assert len(v["fragments"]) <= 4
        prev = v["request_chars"]
        for section in v["fragments"]:
            start, end = section["shown"]
            assert start == prev + 1 and text[prev] == "\n" and end <= len(text)
            if section["complete"]:
                record = json.loads(text[start:end])
                assert (record["id"], record["path"]) == (section["id"], section["path"])
            else:
                assert len(text[start:end]) < section["record_chars"]
            prev = end
            checked += 1
        assert prev == len(text)
        per_case[v["input_id"]][v["length_layer"], v["view"]] = v
    pairs = {}
    for key, items in per_case.items():
        limit = min(items["budget", m]["chars"] for m in "BC")
        assert all(items["matched", m]["budget"] == limit for m in "BC")
        assert items["budget", "A"]["text"] == items["budget", "B"]["text"][:items["budget", "A"]["chars"]]
        result = {}
        for layer in ("budget", "matched"):
            b, c = (items[layer, m] for m in "BC")
            sets = [{s["id"] for s in v["fragments"] if s["complete"]} for v in (b, c)]
            result[layer] = {"chars": [b["chars"], c["chars"]], "common": sorted(sets[0] & sets[1]),
                             "b_only": sorted(sets[0] - sets[1]), "c_only": sorted(sets[1] - sets[0]),
                             "cut": [b["truncated"], c["truncated"]],
                             "partial_records": [sum(not s["complete"] for s in v["fragments"]) for v in (b, c)],
                             "omitted_records": [b["omitted_records"], c["omitted_records"]]}
        pairs[key] = result
    return checked, pairs


def verdict(run, gold):
    if run["winner"] is None:
        return "hold"
    if run["winner"] != gold["expected_candidate"] or not gold["confirmed_selection"]:
        return "wrong"
    return "exact" if run["selected"] == json.loads(gold["confirmed_selection"]) else "wrong"


def replay_check(views, runs, truth):
    gold = {(r["input_id"], r["candidate"]): r for r in truth}
    first, second = ([{k: v for k, v in row.items() if k != "replay"} for row in runs if row["replay"] == key]
                     for key in ("one", "two"))
    assert first == second and len(views) == len(first)
    receipts = open_json("evidence/replays.json")
    assert receipts["all_equal"]
    for receipt in receipts["runs"]:
        assert [(a["file"], a["mode"]) for a in receipt["accesses"]] == [
            ("visible.jsonl", "r"), ("candidates.json", "r"), ("runs.jsonl", "w"), ("audit.json", "w")]
        assert receipt["view_rows"] == len(views)
        assert receipt["candidate_sha256"] == digest((HERE / "candidate-conditions.json").read_bytes())
        assert receipt["program_sha256"] == digest((HERE / "tools/compare.py").read_bytes())
    all_gold = {}
    details = []
    directions = Counter()
    groups = open_json("candidate-conditions.json")
    for v, run in zip(views, first, strict=True):
        key = run["input_id"]
        assert (key, run["method"], run["length_layer"]) == (v["input_id"], v["view"], v["length_layer"])
        assert run["view_input_sha256"] == stamp(runner_envelope(v))
        assert run["candidate_input_sha256"] == stamp(groups[v["candidate_set"]])
        assert run["result_sha256"] == stamp({k: val for k, val in run.items() if k != "result_sha256"})
        assert run["application_effect"] == "unknown"
        for result in run["candidates"]:
            row = gold[key, result["candidate"]]
            all_gold[key] = row
            if result["status"] == "support":
                assert result["proof"] and result["preserve"]
                for proof in result["proof"]:
                    start, end = proof["view_chars"]
                    actual = json.loads(v["text"][start:end])
                    assert (actual["id"], actual["path"]) == (proof["record"], proof["origin"])
            directions[result["status"], row["expected_direction"]] += 1
        row = all_gold[key]
        details.append({**run, "grade": verdict(run, row), "known": bool(row["expected_candidate"]),
                        "gold_effect": row["effect_state"], "gold_target": row["target_candidates"],
                        "gold_runtime": row["runtime_effect"], "gold_stored": row["stored_changed_set"]})
    return details, {"pairs":len(views), "executions":len(runs),
                     "candidate_directions":{f"{a}/{b}":c for (a,b),c in sorted(directions.items())}}


GROUPS = [
    ("E", "본 자연", {"natural-primary", "primary-unfilled"}),
    ("M", "본 자연", {"natural-primary", "primary-unfilled"}),
    ("E", "본 구성", {"primary-mutation"}),
    ("M", "본 구성", {"primary-mutation"}),
    ("M", "링크 자연 보조", {"natural-linked"}),
    ("M", "링크 구성 보조", {"linked-mutation"}),
    ("E", "대조 기본", {"control"}),
    ("M", "대조 기본", {"control"}),
    ("E", "대조 변형", {"control-mutation"}),
    ("M", "대조 변형", {"control-mutation"}),
]


def aggregate(cases, details):
    output = []
    for project, title, tiers in GROUPS:
        scheduled = [r for r in cases if r["project"] == project and r["tier"] in tiers]
        aids = {r["input_id"] for r in scheduled}
        selected = [r for r in details if r["input_id"] in aids]
        initial = [r for r in selected if r["length_layer"] == "budget"]
        matched = [r for r in selected if r["length_layer"] == "matched"]
        tallies = {}
        for name, layer in (("budget", initial), ("matched", matched)):
            tallies[name] = {kind: dict(Counter(row["grade"] for row in layer if row["method"] == kind))
                             for kind in ("ABC" if name == "budget" else "BC")}
        output.append({"project": project, "layer": title,
                       "scheduled": len(scheduled) * 3, "executed": len(initial),
                       "known": sum(row["known"] for row in initial),
                       "unfilled": len(scheduled) * 3 - len(initial),
                       "runtime_unknown": len(initial), "matched_done": len(matched),
                       "scores": tallies})
    return output


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def table(head, rows):
    return "\n".join(["| " + " | ".join(head) + " |",
                      "| " + " | ".join("---" for _ in head) + " |",
                      *("| " + " | ".join(cell(value) for value in row) + " |" for row in rows)])


def link(text, url):
    if not url:
        return "미확인"
    return f"[{text}]({url})"


def triples(item):
    return "/".join(str(item.get(key, 0)) for key in ("exact", "wrong", "hold")) if item else "—"


def tables(cases, original, controls, details, summary):
    descriptions = {a["id"]: a for a in original + controls}
    rows1 = []
    for r in cases:
        value = descriptions.get(r["input_id"]) or descriptions.get(r["parent"], {})
        exhibit = link("원 요청·정의", value.get("source_url"))
        artifact = link("입력", r["source"]) if r["source"] else "미확인"
        if value.get("id") == "M03":
            artifact += " · " + link("3.6 예제", "https://musescore.org/sites/musescore.org/files/2022-01/MMTest36.mscz")
        if r["variant"] in {"duplicate", "repoint"}:
            summary_text = r["change"] or "변형 공석"
        else:
            summary_text = value.get("target_summary", "")
        rows1.append([f'{r["input_id"]} · {r["tier"]}', f'{exhibit} · {artifact} · {value.get("edition","미확인")}',
                      summary_text, value.get("selection_origin", "미확인"), r["exception"]])
    rows2 = []
    for run in details:
        if run["length_layer"] != "budget":
            continue
        record_spec = []
        for row in run["opened_records"]:
            edges = ", ".join(f'{e["field"]}→{e["to"]}' for e in row["refs"])
            record_spec.append(row["id"] + (f" ({edges})" if edges else ""))
        chosen = next((c for c in run["candidates"] if c["candidate"] == run["winner"]), None)
        selected = ",".join(run["selected"] or []) or "미확인"
        kept = ", ".join(run["preserved_links"]) or "미확인"
        stored = ",".join(json.loads(run["gold_stored"])) if run["gold_stored"] else "미확인"
        effect = {"predicted":"예상", "observed-upstream-diff":"상류 diff", "unknown":"미확인"}[run["gold_effect"]]
        state = {"exact":"저장 범위 정확", "wrong":"오확정", "hold":"보류"}[run["grade"]]
        status = state + " · " + ", ".join(c["status"] + "/" + c["reason"] for c in run["candidates"])
        rows2.append([f'{run["input_id"]}/{run["method"]}', " · ".join(record_spec) or "원문",
                      link(chosen["candidate"], chosen["url"]) if chosen else
                      "보류 · " + " · ".join(link(c["candidate"],c["url"]) for c in run["candidates"]),
                      f"선택 {selected} · 보존 {kept} · 기준 저장 {stored} ({effect}) · 앱 미확인", status, str(run["chars"])])
    for r in cases:
        if r["state"] != "ready":
            rows2.append([f'{r["input_id"]}/A·B·C', "공석", "—", "—", r["exception"], "—"])
    rows3 = [
        [f'{s["project"]} · {s["layer"]}', f'{s["scheduled"]} · 실행 {s["executed"]} · 기준 확정 {s["known"]}',
         " · ".join(f'{k} {triples(s["scores"]["budget"][k])}' for k in "ABC"),
         " · ".join(f'{k} {triples(s["scores"]["matched"][k])}' for k in "BC"),
         f'{s["executed"]}/{s["executed"]} 반복 일치 · 공석 {s["unfilled"]} · 실측 미확인 {s["runtime_unknown"]}']
        for s in summary
    ]
    return [
        ("표 1 · 모집 사건과 시험 사본",
         table(["사건·자연/구성", "원 요청·첨부 URL·판", "목표 부분·보존 조건", "작성자 선택 근거", "전체 파일로도 미확인"], rows1)),
        ("표 2 · 보기별 판정",
         table(["사건·보기", "실제로 받은 객체·참조", "연결 절 URL과 보류 후보", "선택·영향 집합", "확인·오확정·보류", "열람량(문자)"], rows2)),
        ("표 3 · 분모와 재생",
         table(["프로젝트·표본층", "예정·판정 가능 분모", "A·B·C 정확/오확정/보류",
                "길이 일치 B·C 정확/오확정/보류", "반복 일치·미확인"], rows3)),
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=Path, default=HERE / "runs.jsonl")
    parser.add_argument("--tables", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    options = parser.parse_args()
    frames, attempts = frame_check()
    seal = open_json("evidence/gold-seal.json")
    for name, expected in seal["files"].items():
        assert digest((HERE / name).read_bytes()) == expected, name
    views = jsonl(HERE / "views.jsonl")
    seen, pairs = views_check(views)
    cases, truth = csv_rows("cases.csv"), csv_rows("truth.csv")
    rows, run_stats = replay_check(views, jsonl(options.runs), truth)
    counts = aggregate(cases, rows)
    sources = jsonl(HERE / "sources.jsonl")
    counted = [x for x in sources if x["unique_counted"]]
    assert len({x["source_id"] for x in sources}) == len(sources)
    assert len({x["lineage"] for x in counted}) == len(counted)
    outcome = {
        "frame":frames, "attachment_probes":attempts, "view_record_fragments":seen,
        "groups":counts, "pairs":pairs, "runs":run_stats, "planned_case_rows":len(cases),
        "truth_rows":len(truth), "source_rows":len(sources),
        "unique_opened_works":dict(Counter(x["allocation"] for x in counted)),
        "source_unique_urls": len({x["source_url"] for x in sources}),
        "source_attempt_status": dict(Counter(x["origin_status"] for x in sources)),
        "primary_read_available_cases":[x["input_id"] for x in cases if x["tier"]=="natural-primary"],
        "matched_benefits":[r["input_id"] for r in rows if r["length_layer"]=="matched" and r["method"]=="C"
                            and r["grade"]=="exact" and not any(b["input_id"]==r["input_id"] and
                            b["length_layer"]=="matched" and b["method"]=="B" and b["grade"]=="exact" for b in rows)],
    }
    options.evidence.write_text(json.dumps(outcome,ensure_ascii=False,indent=2)+"\n")
    display = tables(cases, jsonl(HERE / "inputs.jsonl"), jsonl(HERE / "controls.jsonl"), rows, counts)
    options.tables.write_text("".join(f"## {title}\n\n{body}\n\n" for title, body in display))
    print(f'{len(views)} views / {run_stats["executions"]} executions; {len(counted)} primary source works; all file and ledger checks passed.')


if __name__ == "__main__":
    main()
