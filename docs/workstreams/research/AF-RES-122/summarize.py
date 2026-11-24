"""Join the sealed truth after replay and emit tables and denominators."""

import argparse
import csv
import io
import json
from collections import Counter, defaultdict
from pathlib import Path

from prepare import HERE, read_csv, read_jsonl, packed
from replay import CONDITIONS, LIMITS, write_csv


CLASSES = ("직접", "일부", "명시충돌", "미확인")
TIER_NAMES = {
    "forum-diagnostic": "공개 opening 진단",
    "constructed": "공식 시험 기반 구성",
}
GAP = {
    "O3143": ("PT-LSTM", "LSTM의 시간·배치 해석"),
    "O3611": ("PT-LSTM", "겹치는 시계열 창 및 레이블"),
    "O3665": ("PT-EMBED", "F 값과 축 집계"),
    "O3875": ("PT-DDP", "분산 입력과 gradient 합산·평균"),
    "O3885": ("PT-LOAD", "센서 레코드 짝짓기와 전처리"),
    "O4437": ("PT-FETCH", "원 CUDA worker 예외"),
    "O4588": ("PT-COLLATE", "파일별 파서와 구조 매핑"),
    "O4975": ("PT-TEST-DATA", "원본 이미지와 패치의 시험 독립성"),
    "O5330": ("PYG-DATA", "그래프·노드와 PyG 표본 구조"),
    "O5952": ("PT-TEST-VIEW", "Core ML 변환 및 2.2.2 실측"),
}


def by_key(rows, *columns):
    result = {tuple(row[key] for key in columns): row for row in rows}
    if len(result) != len(rows):
        raise ValueError(f"duplicate key {columns}")
    return result


def alias_costs(data, alias_rows, sources):
    at_url = {row["source_url"]: row for row in sources.values() if row["status"] == "read"}
    costs = []
    opened = set()
    for alias in alias_rows:
        if alias["status"] != "active":
            continue
        refs = {sources[(sid,)]["source_url"] for sid in alias["source_ids"].split("|")}
        refs.add(alias["companion_url"].split("#", 1)[0])
        if not refs <= at_url.keys():
            raise ValueError(f"{alias['alias_id']}: unresolved evidence {refs - at_url.keys()}")
        opened.update(refs)
        stream = io.StringIO(newline="")
        csv.writer(stream, lineterminator="\n").writerow(alias.values())
        costs.append({
            "alias_id": alias["alias_id"],
            "feature_id": alias["feature_id"],
            "surface": alias["surface"],
            "authority": alias["authority"],
            "direct_evidence_addresses": len(refs),
            "direct_evidence_source_ids": "|".join(sorted(at_url[url]["source_id"] for url in refs)),
            "row_utf8_bytes": len(stream.getvalue().encode("utf-8")),
        })
    return costs, {
        "active_rows": len(costs),
        "rejected_rows": len(alias_rows) - len(costs),
        "sum_evidence_refs": sum(row["direct_evidence_addresses"] for row in costs),
        "distinct_evidence_addresses": len(opened),
        "active_rows_utf8_bytes": sum(row["row_utf8_bytes"] for row in costs),
        "whole_csv_utf8_bytes": (data / "aliases.csv").stat().st_size,
    }


def rank_groups(data, requests, cards):
    ranks = read_csv(data / "ranks.csv")
    index = by_key(ranks, "request_id", "condition", "feature_id")
    expected = {(rq, condition, fid) for rq in requests for condition in CONDITIONS for fid, in cards}
    if expected != index.keys():
        raise ValueError("each request must have 16 scores in each of four conditions")
    group = defaultdict(list)
    for row in ranks:
        if int(row["score"]) != sum(int(row[key]) for key in ("symbol_points", "english_points", "alias_points")):
            raise ValueError(f"{row['request_id']} score mismatch")
        group[row["request_id"], row["condition"]].append(row)

    slots = by_key(read_csv(data / "evidence/slots.csv"), "request_id", "condition", "stage", "slot")
    lists = {}
    for key, rows in group.items():
        ordered = sorted(rows, key=lambda row: (-int(row["score"]), row["feature_id"]))
        if rows != ordered:
            raise ValueError(f"{key}: score order mismatch")
        positive = [row["feature_id"] for row in rows if int(row["score"]) > 0]
        for stage, limit in LIMITS.items():
            items = [row["feature_id"] for row in rows if row[stage + "_rank"]]
            expected_items = positive[:limit]
            if items != expected_items:
                raise ValueError(f"{key}: {stage} limit mismatch")
            for i in range(1, limit + 1):
                fid = items[i - 1] if i <= len(items) else ""
                if slots[(*key, stage, str(i))]["feature_id"] != fid:
                    raise ValueError(f"{key}: {stage} slot {i} mismatch")
            lists[(*key, stage)] = items
    if len(slots) != len(group) * sum(LIMITS.values()):
        raise ValueError("unexpected slot rows")
    return index, lists


def table1_data(data, requests, verdicts):
    rows = []
    for row in read_csv(data / "frame.csv"):
        if row["kind"] == "scheduled":
            rows.append({
                "request_id": row["slot"], "tier": "natural-planned", "opening": "", "version": "미확인",
                "goal": "공석. " + row["reason"], "constraints": "", "author_api": "미확인",
                "direct_partial_conflict_unknown": "미평가", "basis": "", "limit": "모집 순서와 기간 경계 미검증",
            })
    for rid, request in requests.items():
        tally = Counter(row["verdict"] for (q, _), row in verdicts.items() if q == rid)
        basis, gap = GAP.get(rid, (request["source_id"], request["location"]))
        rows.append({
            "request_id": rid,
            "tier": request["tier"],
            "opening": request["url"],
            "version": request["author_version"],
            "goal": request["goal"],
            "constraints": request["constraints"],
            "author_api": request["author_api_role"],
            "direct_partial_conflict_unknown": "/".join(str(tally[value]) for value in CLASSES),
            "basis": basis,
            "limit": gap,
        })
    return rows


def difference(left, right):
    return "|".join(item for item in right if item not in left)


def table2_data(requests, indices, lists, verdicts, cards, aliases):
    rows = []
    effects = []
    for rid in requests:
        base_in = lists[rid, "raw-off", "investigation"]
        base_show = lists[rid, "raw-off", "display"]
        for condition in CONDITIONS:
            key = rid, condition
            investigated = lists[*key, "investigation"]
            shown = lists[*key, "display"]
            links = sorted({
                aid for fid in investigated
                for aid in indices[*key, fid]["alias_hits"].split("|") if aid
            })
            outcomes = Counter(verdicts[rid, fid]["verdict"] for fid in shown)
            rows.append({
                "request_id": rid, "condition": condition,
                "investigation": "|".join(investigated), "display": "|".join(shown),
                "display_empties": LIMITS["display"] - len(shown),
                "investigation_empties": LIMITS["investigation"] - len(investigated),
                "added_investigation": difference(base_in, investigated),
                "lost_investigation": difference(investigated, base_in),
                "added_display": difference(base_show, shown),
                "lost_display": difference(shown, base_show),
                "checked_operation_and_remaining": " / ".join(
                    f"{fid} · {verdicts[rid,fid]['finding']} · {verdicts[rid,fid]['remaining_conditions']}" for fid in shown
                ),
                "alias_ids": "|".join(links),
                "alias_urls": "|".join(aliases[aid,]["korean_url"] for aid in links),
                "investigation_api_urls": "|".join(cards[fid,]["api_url"] for fid in investigated),
                "display_conflict": outcomes["명시충돌"],
                "display_unknown": outcomes["미확인"],
            })

            for fid in shown:
                rank = indices[*key, fid]
                verdict = verdicts[rid, fid]["verdict"]
                if rank["alias_hits"] and verdict in ("직접", "일부") and rank["symbol_points"] == rank["english_points"] == "0":
                    effects.append({"request_id": rid, "condition": condition, "feature": fid,
                                    "effect": "한국어 어절만으로 표시", "verdict": verdict,
                                    "trigger": rank["alias_hits"]})
                if condition.startswith("raw") and rank["symbol_points"] == "12":
                    opposite = condition.replace("raw", "masked")
                    if fid not in lists[rid, opposite, "display"]:
                        effects.append({"request_id": rid, "condition": condition, "feature": fid,
                                        "effect": "원문 심벌이 있을 때만 표시", "verdict": verdict,
                                        "trigger": "same alias state, masked to raw"})
            if condition.endswith("-on"):
                old_shown = lists[rid, condition.replace("-on", "-off"), "display"]
                for fid in old_shown:
                    if fid not in shown and verdicts[rid, fid]["verdict"] == "직접":
                        effects.append({"request_id": rid, "condition": condition, "feature": fid,
                                        "effect": "별칭 추가 뒤 직접 표시 소실", "verdict": "직접",
                                        "trigger": "조사 유지" if fid in investigated else "조사에서도 빠짐"})
                for fid in shown:
                    rank = indices[*key, fid]
                    if fid not in old_shown and rank["alias_hits"] and verdicts[rid, fid]["verdict"] == "명시충돌":
                        effects.append({"request_id": rid, "condition": condition, "feature": fid,
                                        "effect": "별칭으로 명시충돌 유입", "verdict": "명시충돌",
                                        "trigger": rank["alias_hits"]})
    return rows, effects


def grouped_metrics(requests, verdicts, lists, costs):
    rows = []
    misses = []
    for tier in ("natural-planned", "forum-diagnostic", "constructed"):
        for named in ((None,) if tier == "natural-planned" else (False, True)):
            subset = [rid for rid, request in requests.items() if request["tier"] == tier and bool(request["mask"]) == named]
            eligible = {
                rid: {fid for (q, fid), row in verdicts.items() if q == rid and row["verdict"] == "직접"} for rid in subset
            }
            for condition in CONDITIONS:
                counts = Counter()
                for rid in subset:
                    seen = lists[rid, condition, "investigation"]
                    shown = lists[rid, condition, "display"]
                    counts["investigated_direct"] += len(eligible[rid].intersection(seen))
                    counts["shown_direct"] += len(eligible[rid].intersection(shown))
                    counts["questions_with_investigated_direct"] += bool(eligible[rid].intersection(seen))
                    counts["questions_with_shown_direct"] += bool(eligible[rid].intersection(shown))
                    counts["display_vacancies"] += LIMITS["display"] - len(shown)
                    for fid in shown:
                        counts[verdicts[rid, fid]["verdict"]] += 1
                    for fid in sorted(eligible[rid] - set(shown)):
                        reason = "조사 내 미표시" if fid in seen else "조사 밖"
                        misses.append({"request_id": rid, "condition": condition, "feature": fid, "reason": reason})
                rows.append({
                    "tier": tier, "raw_has_exact_symbol": {None: "미확인", True: "있음", False: "없음"}[named],
                    "condition": condition, "questions": len(subset),
                    "eligible_questions": sum(bool(ids) for ids in eligible.values()) if subset else "",
                    "eligible_pairs": sum(map(len, eligible.values())) if subset else "",
                    "investigated_direct": counts["investigated_direct"] if subset else "",
                    "shown_direct": counts["shown_direct"] if subset else "",
                    "questions_with_investigated_direct": counts["questions_with_investigated_direct"] if subset else "",
                    "questions_with_shown_direct": counts["questions_with_shown_direct"] if subset else "",
                    "shown_partial": counts["일부"] if subset else "",
                    "shown_conflict": counts["명시충돌"] if subset else "",
                    "shown_unknown": counts["미확인"] if subset else "",
                    "display_vacancies": counts["display_vacancies"] if subset else "",
                    "candidate_checks": sum(int(costs[rid, condition]["candidate_comparisons"]) for rid in subset),
                    "symbol_checks": sum(int(costs[rid, condition]["symbol_checks"]) for rid in subset),
                    "english_checks": sum(int(costs[rid, condition]["english_token_checks"]) for rid in subset),
                    "alias_checks": sum(int(costs[rid, condition]["alias_checks"]) for rid in subset),
                    "shown_links": sum(int(costs[rid, condition]["display_links"]) for rid in subset),
                    "two_runs": "일치" if subset else "비교 불가",
                })
    return rows, misses


def md_table(headers, rows):
    def safe(text):
        return str(text).replace("|", " / ").replace("\n", " ")
    return "\n".join([
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
        *["| " + " | ".join(map(safe, row)) + " |" for row in rows],
    ])


def link(label, url):
    return f"[{label}]({url})" if url else label


def md_first(table, sources):
    for row in table:
        basis = [
            link(sid, sources[sid,]["source_url"]) for sid in row["basis"].split("|") if sid
        ]
        yield (
            f"{link(row['request_id'],row['opening'])} · {row['version']}",
            " / ".join(dict.fromkeys(filter(None, (row["goal"], row["constraints"])))),
            row["author_api"],
            row["direct_partial_conflict_unknown"],
            " · ".join([*basis, row["limit"]]),
        )


def md_second(table, cards, aliases, verdicts):
    groups = {}
    for row in table:
        group_key = tuple(value for field, value in row.items() if field != "condition")
        groups.setdefault(group_key, []).append(row)
    for group in groups.values():
        row = group[0]
        shown = row["display"].split("|") if row["display"] else []
        details = [(fid, verdicts[row["request_id"], fid]) for fid in shown]
        changes = []
        for stage in ("investigation", "display"):
            plus, minus = row["added_"+stage], row["lost_"+stage]
            if plus or minus:
                label = "조사" if stage == "investigation" else "표시"
                changes.append(f"{label} +{plus or '—'} −{minus or '—'}")
        desc = " · ".join(f"{fid} {item['verdict']}" for fid, item in details)
        links = [link(fid, cards[fid,]["api_url"]) for fid in shown]
        links += [
            link(aid, aliases[aid,]["korean_url"]) for aid in row["alias_ids"].split("|") if aid
        ]
        yield (
            row["request_id"] + " · " + " / ".join(item["condition"] for item in group),
            f"조사 {(row['investigation'] or '—').replace('|', ' → ')} · 표시 {(row['display'] or '—').replace('|', ' → ')} · 공석 {row['investigation_empties']}/{row['display_empties']}",
            " · ".join(changes) or "—",
            desc + (" · " if desc else "") + (
                (
                    details[0][1]["finding"] + (
                        " 남은 조건 · " + details[0][1]["remaining_conditions"]
                        if details[0][1]["remaining_conditions"] else ""
                    )
                ) if details else "양점 후보 없음"
            ),
            " · ".join(links) or "—",
            f"{row['display_conflict']}/{row['display_unknown']}",
        )


def md_third(table, preparation):
    yield ("정규 예정 · 유무 미확인 · 네 조건", "0/8 · 미평가", "미평가", "미평가 · 모집 공석 8", "실행 0", "비교 불가")
    for row in table:
        if not row["questions"]:
            continue
        readiness = f"별칭 {preparation['active_rows']}행" if row["condition"].endswith("-on") else "별칭 조회 0"
        yield (
            f"{TIER_NAMES[row['tier']]} · {row['raw_has_exact_symbol']} · {row['condition']}",
            f"{row['questions']} / {row['eligible_questions']} / {row['eligible_pairs']}",
            f"{row['investigated_direct']} / {row['shown_direct']}",
            f"{row['shown_partial']} / {row['shown_conflict']} / {row['shown_unknown']} / {row['display_vacancies']}",
            f"{readiness} · {row['candidate_checks']} 비교 / {row['alias_checks']} 별칭 / {row['shown_links']} 링크",
            row["two_runs"],
        )


def summarize(data, output):
    receipt = json.loads((data / "evidence/replay-receipt.json").read_text(encoding="utf-8"))
    if receipt["mismatches"] or not all(receipt["run_to_run"].values()):
        raise ValueError("the two replay outputs must match the stored ledgers")
    source_rows = read_jsonl(data / "sources.jsonl")
    sources = by_key(source_rows, "source_id")
    cards = by_key(read_csv(data / "catalog.csv"), "feature_id")
    alias_rows = read_csv(data / "aliases.csv")
    aliases = by_key(alias_rows, "alias_id")
    request_rows = read_jsonl(data / "requests.jsonl") + read_jsonl(data / "evidence/controls.jsonl")
    requests = {row["request_id"]: row for row in request_rows}
    verdicts = by_key(read_csv(data / "truth.csv"), "request_id", "feature_id")
    assert set(verdicts) == {(rid, fid) for rid in requests for fid, in cards}
    assert all(row["verdict"] in CLASSES for row in verdicts.values())
    assert all((sid,) in sources for row in verdicts.values() for sid in row["source_ids"].split("|"))
    views = by_key(
        read_jsonl(data / "evidence/query-inputs.jsonl") + read_jsonl(data / "evidence/controls-query-inputs.jsonl"),
        "request_id", "view"
    )
    for rid, row in requests.items():
        raw, masked = views[rid, "raw"], views[rid, "masked"]
        assert raw["view_sha256"] == row["raw_nfc_sha256"] and masked["view_sha256"] == row["masked_nfc_sha256"]
        if not row["mask"]:
            assert raw["view_sha256"] == masked["view_sha256"] and raw["projection_sha256"] == masked["projection_sha256"]
        else:
            assert not masked["exact_ids"] and raw["view_sha256"] != masked["view_sha256"]
        for span in row["mask"]:
            assert span["after"] == " " * (span["end"] - span["start"]) and len(span["before"]) == len(span["after"])

    indices, lists = rank_groups(data, requests, cards)
    costs = by_key(read_csv(data / "evidence/replay-costs.csv"), "request_id", "condition")
    alias_rows_cost, preparation = alias_costs(data, alias_rows, sources)
    one = table1_data(data, requests, verdicts)
    two, effects = table2_data(requests, indices, lists, verdicts, cards, aliases)
    three, misses = grouped_metrics(requests, verdicts, lists, costs)
    frame = read_csv(data / "frame.csv")
    metrics = {
        "source_rows": len(sources),
        "source_candidate_addresses": len({row["source_url"] for row in source_rows}),
        "source_read_addresses": len({row["source_url"] for row in source_rows if row["status"] == "read"}),
        "source_primary_lineages": len({
            row["lineage_id"] for row in source_rows if row["status"] == "read" and row["count_primary"]
        }),
        "source_failed_addresses": len({row["source_url"] for row in source_rows if row["status"] == "failed"}),
        "source_failed_rows": sum(row["status"] == "failed" for row in source_rows),
        "source_counts": dict(Counter(row["status"] for row in source_rows)),
        "planned": sum(row["kind"] == "scheduled" for row in frame),
        "planned_available": sum(row["kind"] == "scheduled" and row["decision"] != "공석" for row in frame),
        "forum_openings_read": sum(row["kind"] == "opening" for row in frame),
        "truth_by_tier": {
            tier: dict(Counter(row["verdict"] for row in verdicts.values() if row["tier"] == tier)) for tier in TIER_NAMES
        },
        "request_counts": dict(Counter(row["tier"] for row in requests.values())),
        "same_views_without_symbol": dict(Counter(row["tier"] for row in requests.values() if not row["mask"])),
        "number_of_mask_spans": {
            rid: len(request["mask"]) for rid, request in requests.items() if request["mask"]
        },
        "n_rank_rows": len(indices),
        "n_queries": len(costs),
        "alias_preparation": preparation,
        "relevant_alias_effects": dict(Counter(
            f"{requests[row['request_id']]['tier']}::{row['condition']}::{row['effect']}::{row['verdict']}"
            for row in effects
        )),
        "direct_misses": dict(Counter(row["reason"] for row in misses)),
    }
    output.mkdir(parents=True, exist_ok=True)
    for name, rows in (
        ("table1.csv", one), ("table2.csv", two), ("table3.csv", three),
        ("alias-costs.csv", alias_rows_cost), ("effects.csv", effects), ("direct-misses.csv", misses),
    ):
        write_csv(output / name, rows)
    (output / "metrics.json").write_text(packed(metrics) + "\n", encoding="utf-8")
    tables = [
        "## 표 1 · 요청과 고정판 판독",
        md_table(("질문·원문·작성자 판", "조작·대상·보존", "원저자 심벌·역할", "직접/일부/충돌/미확인", "기준 원절·미확인"), md_first(one, sources)),
        "## 표 2 · 네 조회의 순위",
        md_table(("질문·조건", "조사순 / 표시순 · 공석", "원문 OFF 대비 추가·소실", "표시 판독과 대표 동작·조건", "기능·별칭 원문", "충돌/미확인"), md_second(two, cards, aliases, verdicts)),
        "## 표 3 · 분모와 비교 비용",
        md_table(("표본층·원문 심벌·조건", "질문/적격 질문/적격 쌍", "조사 직접/표시 직접", "표시 일부/충돌/미확인/공석", "근거 준비·후보 비교/별칭 확인/링크", "두 재생"), md_third(three, preparation)),
    ]
    (output / "tables.md").write_text("\n\n".join(tables) + "\n", encoding="utf-8")
    return metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=HERE, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    print(packed(summarize(args.data, args.out)))


if __name__ == "__main__":
    main()
