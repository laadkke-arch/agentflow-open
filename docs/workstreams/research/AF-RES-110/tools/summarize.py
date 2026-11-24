"""Recompute the natural experiment's denominators and three RESULT tables."""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path
from urllib.parse import urldefrag

ROOT = Path(__file__).resolve().parents[1]
METHODS = ("A", "B", "C")
AREAS = {"publication": "문서 출판", "archive": "파일·미디어 보관", "conversion": "표·지리 변환"}
LANGUAGES = ("en", "ko")
VERDICTS = {"direct": "직접", "partial": "일부", "old_only": "옛판만", "conflict": "충돌",
            "unknown": "미확인", "vacancy": "공석"}
TIERS = ("current", "old")


def csv_rows(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def json_rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def filled(rows):
    return [row for row in rows if row["occupied"] == "True"]


def md_table(headers, rows):
    def render(cells):
        return "| " + " | ".join(str(cell).replace("|", "·").replace("\n", " ") for cell in cells) + " |"
    return "\n".join([render(headers), render(["---"] * len(headers)), *(render(row) for row in rows)]) + "\n"


def fmt_counts(counter):
    return " / ".join(str(counter.get(key, 0)) for key in ("current", "old"))


def disposition(row, truth):
    return truth[(row["query_id"], row["feature_id"])][row["tier"] + "_verdict"]


def sets_for(rows, truth):
    direct = [row for row in filled(rows) if disposition(row, truth) == "direct"]
    return {row["feature_id"] for row in direct}, {row["page_url"] for row in direct}


def load(snapshot, evidence):
    frames = csv_rows(ROOT / "frame.csv")
    issue_frame = csv_rows(ROOT / "issue-frame.csv")
    cards = {card["card_id"]: card for card in json_rows(ROOT / "catalog.jsonl")}
    queries = json_rows(ROOT / "queries.jsonl")
    truth = {(row["query_id"], row["feature_id"]): row for row in csv_rows(ROOT / "truth.csv")}
    ranks = csv_rows(snapshot / "ranks.csv")
    runs = json_rows(snapshot / "runs.jsonl")
    replay = json.loads((evidence / "replay.json").read_text())
    sources = json_rows(ROOT / "sources.jsonl")
    return frames, issue_frame, cards, queries, truth, ranks, runs, replay, sources


def compute(snapshot, evidence):
    frames, issue_frame, cards, queries, truth, ranks, runs, replay, sources = load(snapshot, evidence)
    row_groups = {(q["query_id"], lang, method): [] for q in queries for lang in LANGUAGES for method in METHODS}
    for r in ranks:
        if r["build"] == "1":
            row_groups[(r["query_id"], r["language"], r["method"])].append(r)
    run_groups = {(r["query_id"], r["language"], r["method"]): r for r in runs if r["build"] == 1}

    approved = {}
    table1 = []
    for q in queries:
        qid = q["query_id"]
        cards_for = [c for c in cards.values() if (qid, c["feature_id"]) in truth]
        by_tier = {}
        for tier in TIERS:
            page_keys = {urldefrag(c["url"]).url for c in cards_for if c["tier"] == tier}
            labels = Counter(row[tier + "_verdict"] for (key, _), row in truth.items() if key == qid)
            eligible = [c for c in cards_for if c["tier"] == tier and truth[(qid, c["feature_id"])][tier + "_verdict"] == "direct"]
            by_tier[tier] = {"grades": dict(labels), "features": sorted(c["feature_id"] for c in eligible),
                             "pages": sorted({urldefrag(c["url"]).url for c in eligible}), "pages_total": len(page_keys)}
        approved[qid] = by_tier
        d1, d2 = by_tier["current"], by_tier["old"]
        n = len(frames)
        denom = (f"현행 {len(d1['features'])}/{n}, 미확인 {d1['grades'].get('unknown', 0)} · "
                 f"직전 {len(d2['features'])}/{n}, 미확인 {d2['grades'].get('unknown', 0)} · "
                 f"직접 페이지 {len(d1['pages'])}/{d1['pages_total']} · {len(d2['pages'])}/{d2['pages_total']}")
        old_current = next(c["edition"] for c in cards.values() if c["project"] == q["project"] and c["tier"] == "current")
        previous = next(c["edition"] for c in cards.values() if c["project"] == q["project"] and c["tier"] == "old")
        table1.append((f"{qid} · en/ko", f"{old_current} · {previous} · {q['required_operation']} / {q['required_constraint']}",
                       denom, f"[작성자 본문]({q['issue_url']}) · {q['body_location'].split(' raw body ', 1)[-1]}"))

    by_variant = {}
    variants_summary = {}
    table2 = []
    for q in queries:
        qid = q["query_id"]
        for lang in LANGUAGES:
            variant = f"{qid}/{lang}"
            methods = {m: filled(row_groups[qid, lang, m]) for m in METHODS}
            displays = {m: [r for r in rs if r["display_slot"]] for m, rs in methods.items()}
            displayed = {m: {r["card_id"] for r in rs} for m, rs in displays.items()}
            by_variant[variant] = {
                m: {
                    "display_cards": [r["card_id"] for r in ds],
                    "display_grades": dict(Counter(disposition(r, truth) for r in ds)),
                    "display_vacancies": run_groups[qid, lang, m]["display_vacant"],
                    "candidate_vacancies": run_groups[qid, lang, m]["investigation_vacant"],
                    "exclusive_cards": sorted(displayed[m].difference(*(displayed[o] for o in METHODS if o != m))),
                    "eligible_features": sorted(sets_for(ds, truth)[0]),
                    "eligible_pages": sorted(sets_for(ds, truth)[1]),
                    "eligible_within_12": sorted(sets_for(methods[m], truth)[0]),
                    "edition_unknown": sum(r["edition_compatibility"] == "unknown" for r in ds),
                } for m, ds in displays.items()
            }
            eligible_features = set(approved[qid]["current"]["features"]) | set(approved[qid]["old"]["features"])
            eligible_pages = set(approved[qid]["current"]["pages"]) | set(approved[qid]["old"]["pages"])
            for m in METHODS:
                row = by_variant[variant][m]
                row["direct_feature_denominator"] = len(eligible_features)
                row["direct_page_denominator"] = len(eligible_pages)
                row["eligible_feature_only_in_method"] = sorted(set(row["eligible_features"]).difference(
                    *(set(by_variant[variant][other]["eligible_features"]) for other in METHODS if other != m)
                ))
            variants_summary[variant] = {
                "feature_denominator": len(eligible_features), "page_denominator": len(eligible_pages),
                "area": q["area"],
            }
            lookup = {m: {r["card_id"]: r for r in rs} for m, rs in methods.items()}
            seen = {}
            for m in METHODS:
                for row in displays[m]:
                    seen.setdefault(row["card_id"], row)
            for id, row in seen.items():
                def rank_at(method):
                    match = lookup[method].get(id)
                    if not match:
                        return "—"
                    return ("**" + match["candidate_rank"] + "**") if match["display_slot"] else match["candidate_rank"]
                raw_terms = lookup["B"].get(id, {}).get("note_only", "")
                fields = lookup["C"].get(id, {}).get("conflicts", "")
                verdict = disposition(row, truth)
                detail = cards[id]["output"] if verdict == "conflict" else {
                    "direct": "동작+조건", "partial": "일부 조건 지원",
                    "old_only": "현행 불일치", "unknown": "근거 부족",
                }[verdict]
                table2.append((f"{variant} · {id}", " / ".join(rank_at(m) for m in METHODS),
                               f"{raw_terms or '—'} · {fields or '—'}", f"{VERDICTS[verdict]} · {detail}",
                               f"[{row['return_location']}]({row['url']})"))
            if not seen:
                table2.append((variant, "— / — / —", "—", "표시 공석 각 3", "—"))

    area_summary = {}
    score_by_language = {}
    table3 = []
    for lang in LANGUAGES:
        score_by_language[lang] = {}
        for method in METHODS:
            score_by_language[lang][method] = Counter()
            agg = score_by_language[lang][method]
            for area, label in AREAS.items():
                qs = [q for q in queries if q["area"] == area]
                keys = [(q["query_id"], lang, method) for q in qs]
                primary = [r for k in keys for r in filled(row_groups[k]) if r["display_slot"]]
                direct = Counter(r["tier"] for r in primary if disposition(r, truth) == "direct")
                conflict = Counter(r["tier"] for r in primary if disposition(r, truth) in ("conflict", "old_only"))
                other = Counter(disposition(r, truth) for r in primary)
                runs_for_area = [run_groups[k] for k in keys]
                gap = sum(run["display_vacant"] for run in runs_for_area)
                cgap = sum(run["investigation_vacant"] for run in runs_for_area)
                variants = [by_variant[f"{k[0]}/{lang}"][method] for k in keys]
                denom_features = sum(row["direct_feature_denominator"] for row in variants)
                denom_pages = sum(row["direct_page_denominator"] for row in variants)
                got_features = sum(len(row["eligible_features"]) for row in variants)
                got_pages = sum(len(row["eligible_pages"]) for row in variants)
                total_ns = sum(r["end_to_end_ns"] for r in runs_for_area)
                extra_sql = sum(r["sql_statements"] for r in runs_for_area)
                db = replay["builds"][0]["A" if method == "A" else "B"]
                row = {
                    "query_variants": len(qs), "feature_recovered": got_features, "feature_denominator": denom_features,
                    "page_recovered": got_pages, "page_denominator": denom_pages, "slot_vacancies": gap,
                    "candidate_vacancies": cgap, "independently_unknown": other["unknown"], "partly_useful": other["partial"],
                    "confirmed_bad": dict(conflict), "direct": dict(direct), "query_end_to_end_ns": total_ns,
                    "catalog_calls": sum(r["catalog_calls"] for r in runs_for_area), "additional_sql": extra_sql,
                    "edition_applicability_unknown": sum(row["edition_unknown"] for row in variants),
                }
                area_summary[f"{lang}/{method}/{area}"] = row
                agg.update({
                    "direct_cards": sum(direct.values()), "confirmed_bad": sum(conflict.values()),
                    "unknown_cards": other["unknown"], "partial": other["partial"],
                    "vacancies": gap, "candidate_vacancies": cgap,
                    "feature_recovered": got_features, "feature_denominator": denom_features,
                    "page_recovered": got_pages, "page_denominator": denom_pages,
                    "catalog_calls": row["catalog_calls"], "sql_statements": extra_sql,
                    "query_end_to_end_ns": total_ns,
                })
                call_count = str(row["catalog_calls"]) if method != "C" else "공유 " + str(len(qs)) + ", 추가 0"
                cost = f"{db['database_bytes']:,}/{db['term_table_and_indexes_bytes']:,} B · {call_count}회 · {total_ns / 1e6:.3f} ms"
                table3.append((f"{lang} · {method} · {label} · 현행/직전",
                               f"직접 {fmt_counts(direct)} · 오추천 {fmt_counts(conflict)} · 일부 {other['partial']} · 미확인 {other['unknown']}",
                               f"누락 기능 {denom_features - got_features} / 페이지 {denom_pages - got_pages} · 표시 {gap}/6 · 조사 {cgap}/24",
                               cost, ("일치" if replay["replay_identical"] else "불일치")))
    ties = Counter()
    for key, modes in replay["builds"][0]["tie_runs"].items():
        qid, lang = key.split("/")
        for method, row in modes.items():
            ties[f"{method}_cutoff_3"] += row["tie_across_3"]
            ties[f"{method}_cutoff_12"] += row["tie_across_12"]
            for owner, displays in row["methods"].items():
                first, alternate = displays["display_original"], displays["display_reverse_id"]
                ties[f"{owner}_order_changed"] += first != alternate
                ties[f"{owner}_set_changed"] += set(first) != set(alternate)
                ftr = lambda cards_ids: {cards[id]["feature_id"] for id in cards_ids
                                         if truth[(qid, cards[id]["feature_id"])][cards[id]["tier"] + "_verdict"] == "direct"}
                ties[f"{owner}_direct_feature_changed"] += ftr(first) != ftr(alternate)
    counted = [s for s in sources if s["counted"]]
    source_counts = Counter(s["category"] for s in counted)
    assert len({s["work_key"] for s in counted}) == len(counted)
    total = {
        "frame_slots": len(frames), "frame_vacancies": sum(row["status"] == "vacancy" for row in frames),
        "query_slots": len(queries), "issue_starter_posts": sum(int(r["ordinal"]) <= 30 for r in issue_frame),
        "first_query_original_verified": sum(q["creation_revision"] == "verified" for q in queries),
        "counts_by_feature_verdict": dict(Counter(row["verdict"] for row in truth.values())),
        "direct_requests": sorted(qid for qid, by_tier in approved.items() if any(v["features"] for v in by_tier.values())),
        "truth_rows": len(truth), "catalog_cards": len(cards),
        "pages_in_catalog": len({urldefrag(c["url"]).url for c in cards.values()}),
        "direct_first_party_work_counts": dict(source_counts),
        "total_sources": len(sources),
        "non_natural": {"translations": sum(s["category"] == "translation" for s in sources),
                        "posthoc": sum(s["category"] == "posthoc" for s in sources),
                        "prototype_calibrations": 2, "replacement_query_variants": 2},
        "main_replay_fingerprint": replay["builds"][0]["fingerprint"],
        "main_catalog_calls": sum(r["catalog_calls"] for r in runs),
        "phase_sql": sum(r["sql_statements"] for r in runs),
        "tie_catalog_calls": sum(len(modes) for entry in replay["builds"] for modes in entry["tie_runs"].values()),
        "edition_labels": approved, "variants": by_variant, "areas": area_summary,
        "metrics": {lang: {method: dict(row) for method, row in by_mode.items()}
                    for lang, by_mode in score_by_language.items()},
        "ties": dict(ties),
    }
    tables = "\n".join((
        "## 표 1. 요구 원문과 적격 분모\n\n" + md_table(
            ["요구ID·언어", "현행·직전 대상 판과 원조작·조건", "직접 적격·미확인, 기능·페이지", "원근거 URL·절"], table1),
        "## 표 2. 표시 후보의 순위와 실제 반환 위치\n\n"
        "굵은 숫자는 표시, 나머지 숫자는 12개 조사 후보 안의 순위다. 메모 칸은 B가 더한 토큰과 C 충돌 판별이다.\n\n" + md_table(
            ["요구·후보", "A / B / C", "메모 토큰·판/목적 충돌", "순위 공개 전 판정·대상", "실제 반환 위치"], table2),
        "## 표 3. 방식·영역별 상위3과 비용\n\n"
        "각 행은 요구 2×표시 3=6, 조사 2×12=24다. 순서는 현행/직전이다. "
        "비용은 DB/단어표·색인 바이트와 1회차 두 요청의 조회횟수·경과 시간이다. C의 경과는 B 조회와 재정렬의 합이다.\n\n" + md_table(
            ["언어·방식·영역·판", "표시 직접 적격·오추천·일부·미확인",
             "빠진 적격과 빈 자리", "준비·조회 비용", "두 번 재생"], table3),
    ))
    return total, tables


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, default=ROOT)
    parser.add_argument("--evidence", type=Path, default=ROOT / "evidence")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    statistics, tables = compute(args.snapshot, args.evidence)
    (args.output / "summary.json").write_text(json.dumps(statistics, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    (args.output / "tables.md").write_text(tables)
