"""Join sealed judgments to replay results and regenerate the result tables."""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from capture import HERE, POLICIES, PREVIOUS, VIEWS, load_previous


TIERS = {
    "hash_identical": ("원문 해시 동일", 10),
    "current_reacquired": ("현행 재취득", 0),
    "access_failed": ("접근 실패", 0),
    "existing_control": ("기존 구성", 9),
    "new_control": ("새 대조", 12),
}
VERDICTS = ("직접", "일부", "명시충돌", "미확인")
LIMITS = {"investigation": 8, "display": 3}
P122 = f"https://github.com/laadkke-arch/agentflow-open/blob/{PREVIOUS}/docs/workstreams/research/AF-RES-122"


def read_labels(data, prior, prepare, tiers):
    old = [
        row for row in prepare.read_csv(prior / "truth.csv")
        if tiers.get(row["request_id"]) in ("hash_identical", "existing_control")
    ]
    rows = old + prepare.read_csv(data / "truth.csv")
    labels = {}
    for row in rows:
        key = row["request_id"], row["feature_id"]
        if key in labels or row["verdict"] not in VERDICTS or not row["api_url"]:
            raise ValueError(f"invalid or duplicated criterion {key}")
        labels[key] = row
    return labels


def label_counts(request, features, labels):
    counts = Counter(labels[request, fid]["verdict"] for fid in features)
    return {name: counts[name] for name in VERDICTS}


def sign_counts(request, csv_values, labels):
    return label_counts(request, (item.split(":")[0] for item in csv_values.split("|") if item), labels)


def read_queries(path, labels, expected_requests, prepare):
    groups = defaultdict(list)
    for row in prepare.read_csv(path / "ranks.csv"):
        key = row["request_id"], row["view"], row["policy"]
        groups[key].append(row)
    expected = {(request, view, policy) for request in expected_requests for view in VIEWS for policy in POLICIES}
    if set(groups) != expected:
        raise ValueError("ranks must cover every available request, both views and all four policies")

    inquiries = {}
    for (request, view, policy), rows in groups.items():
        ids = [row["feature_id"] for row in rows]
        if len(set(ids)) != 16 or len(ids) != 16 or any((request, fid) not in labels for fid in ids):
            raise ValueError(f"{request}: missing or duplicated ranking/criterion pairing")
        if sorted(rows, key=lambda row: (-int(row["score"]), row["feature_id"])) != rows:
            raise ValueError(f"{request}/{view}/{policy}: ranking order mismatch")
        positive = [row["feature_id"] for row in rows if int(row["score"]) > 0]
        inquiries[request, view, policy] = {
            stage: positive[:cap] for stage, cap in LIMITS.items()
        }

    slots = prepare.read_csv(path / "slots.csv")
    expected_slots = {
        (request, view, policy, stage, str(position)): picked[position - 1] if position <= len(picked) else ""
        for (request, view, policy), inquiry in inquiries.items()
        for stage, picked in inquiry.items()
        for position in range(1, LIMITS[stage] + 1)
    }
    actual_slots = {(r["request_id"], r["view"], r["policy"], r["stage"], r["slot"]): r["feature_id"] for r in slots}
    if expected_slots != actual_slots or len(actual_slots) != len(slots):
        raise ValueError("slot ledger and positive rank differ")
    return groups, inquiries


def verify_annotations(controls, annotations, groups, labels):
    by_request = defaultdict(list)
    match_positions = defaultdict(set)
    for row in annotations:
        key = row["request_id"], row["view"]
        by_request[key].append(row)
        for policy in POLICIES:
            if row["first_policy"] <= policy:
                match_positions[(*key, policy, row["feature_id"])].add(
                    f"{row['alias_id']}@{row['start']}:{row['end']}({row['first_policy']})"
                )
    for key, rows in groups.items():
        for row in rows:
            expected = match_positions[(*key, row["feature_id"])]
            if set(filter(None, row["alias_positions"].split("|"))) != expected:
                raise ValueError(f"{key}: replay alias spans and committed semantic annotations disagree")
    for control in controls:
        request = control["request_id"]
        direct = sorted(fid for (rid, fid), row in labels.items() if rid == request and row["verdict"] == "직접")
        if direct != control["expected_direct_ids"]:
            raise ValueError(f"{request}: direct eligibility differs from the registered expectation")
        for view in VIEWS:
            matches = [row for row in by_request[request, view] if row["alias_id"] == control["target_alias_id"]]
            observed = [policy for policy in POLICIES if any(match["first_policy"] <= policy for match in matches)]
            expected_referent = control["expected_referent"].split()[0]
            if observed != control["expected_policies"] or any(
                match["speech_role"] != control["expected_role"]
                or not match["referent_judgment"].startswith(expected_referent)
                for match in matches
            ):
                raise ValueError(f"{request}/{view}: alias boundary, referent, or role differs from the registered expectation")
    return by_request


def check_sources(sources, annotations, opening_rows, domain_rows):
    known = {row["source_id"] for row in sources}
    if len(known) != len(sources):
        raise ValueError("source IDs must be unique")
    for ids in (
        [row["source_ids"].split("|") for row in annotations] +
        [[row["source_id"], *row["alternative_attempt_ids"]] for row in opening_rows] +
        [row["source_ids"].split("|") for row in domain_rows]
    ):
        if not set(ids) <= known:
            raise ValueError(f"unresolved source IDs {ids}")
    works = defaultdict(set)
    for source in sources:
        if source["counted"]:
            if source["access_status"] != "read":
                raise ValueError(f"unopened source cannot count: {source['source_id']}")
            works[source["category"]].add(source["work_id"])
    target = {"korean_author": 8, "language": 5, "pytorch_251": 5, "rail": 2, "library": 2}
    for category, required in target.items():
        if len(works[category]) < required:
            raise ValueError(f"{category}: primary source threshold not met")
    unique = set().union(*works.values())
    if len(unique) < 22:
        raise ValueError("fewer than 22 distinct directly read primary works")
    return {
        "attempt_rows": len(sources),
        "directly_read_rows": sum(row["counted"] for row in sources),
        "unique_works": len(unique),
        "unique_by_category": {key: len(value) for key, value in works.items()},
        "access_status_rows": dict(Counter(row["access_status"] for row in sources)),
    }


def stage_counts(requests, view, policy, inquiries, labels):
    metrics = {}
    for stage, width in LIMITS.items():
        combined = Counter()
        for request in requests:
            ids = inquiries[request, view, policy][stage]
            combined.update(label_counts(request, ids, labels))
            combined["공석"] += width - len(ids)
        metrics[stage] = {name: combined[name] for name in (*VERDICTS, "공석")}
        if sum(metrics[stage].values()) != len(requests) * width:
            raise ValueError(f"{view}/{policy}/{stage}: outcome and slot totals differ")
    return metrics


def aggregate(tiers, inquiries, costs, labels, annotations):
    result = []
    for tier, (title, planned) in TIERS.items():
        requests = sorted(key for key, value in tiers.items() if value == tier and value != "access_failed")
        available = {request: [label["verdict"] for (rid, _), label in labels.items() if rid == request] for request in requests}
        direct_requests = sum("직접" in statuses for statuses in available.values())
        partial_requests = sum("일부" in statuses for statuses in available.values())
        eligible_requests = sum(any(kind in statuses for kind in ("직접", "일부")) for statuses in available.values())
        direct_pairs = sum(statuses.count("직접") for statuses in available.values())
        partial_pairs = sum(statuses.count("일부") for statuses in available.values())
        for view in VIEWS:
            review_spans = sum(len(annotations[request, view]) for request in requests)
            for policy in POLICIES:
                queries = [costs[request, view, policy] for request in requests]
                cost = {key: sum(int(row[key]) for row in queries) for key in (
                    "candidate_comparisons", "symbol_checks", "english_token_checks", "alias_checks",
                    "candidate_windows_shared_bcd", "final_tokens_shared_bcd", "accepted_spans",
                )}
                result.append({
                    "tier": tier, "title": title, "view": view, "policy": policy,
                    "scheduled": planned, "measured_requests": len(requests),
                    "eligible_requests": eligible_requests, "direct_eligible_requests": direct_requests,
                    "partial_eligible_requests": partial_requests, "direct_pairs": direct_pairs,
                    "partial_pairs": partial_pairs, "criteria_pairs_reviewed_once": len(requests) * 16,
                    "all_annotated_spans_in_view": review_spans, "cost": cost,
                    **stage_counts(requests, view, policy, inquiries, labels),
                })
    return result


def compare_placement(inquiries, labels):
    """Keep the A display order and show only its positive members of each investigation pool."""
    rows = []
    for (request, view, policy), pools in inquiries.items():
        if policy == "A":
            continue
        baseline = inquiries[request, view, "A"]["display"]
        filtered = [fid for fid in baseline if fid in pools["investigation"]]
        promoted = pools["display"]
        rows.append({
            "request_id": request, "view": view, "investigation_policy": policy,
            "investigation_ids": "|".join(pools["investigation"]),
            "a_display_from_pool": "|".join(filtered), "policy_display": "|".join(promoted),
            "a_display_verdicts": "|".join(labels[request, fid]["verdict"] for fid in filtered),
            "policy_display_verdicts": "|".join(labels[request, fid]["verdict"] for fid in promoted),
            "held_for_review": "|".join(fid for fid in pools["investigation"] if fid not in baseline),
            "baseline_display_excluded_by_investigation_limit": "|".join(fid for fid in baseline if fid not in pools["investigation"]),
        })
    return rows


def transition_metrics(rows, labels, tiers):
    output, totals = [], {}
    for row in rows:
        rid = row["request_id"]
        gains = sign_counts(rid, row["added"], labels)
        losses = sign_counts(rid, row["lost"], labels)
        key = (tiers[rid], row["view"], f"{row['before']}→{row['after']}", row["stage"])
        count = totals.setdefault(key, {"added": Counter(), "lost": Counter()})
        count["added"].update(gains)
        count["lost"].update(losses)
        output.append({
            "tier": tiers[rid], **row,
            **{f"added_{status}": v for status, v in gains.items()},
            **{f"lost_{status}": v for status, v in losses.items()},
        })
    summary = [
        {"tier": tier, "view": view, "transition": transition, "stage": stage, **counts}
        for (tier, view, transition, stage), counts in sorted(totals.items())
    ]
    return output, summary


def cell(value):
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(header, rows):
    return "\n".join([
        "| " + " | ".join(header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
        *["| " + " | ".join(cell(field) for field in row) + " |" for row in rows],
    ])


def format_match(hits):
    if not hits:
        return "0구간", "판독 대상 구간 없음", ""
    aliases = [
        f"{row['phrase']} {row['alias_id']} / {row['particle'] or '—'} · {row['first_policy']} 최초"
        for row in hits
    ]
    roles = [f"{row['referent_judgment']} / {row['speech_role']}" for row in hits]
    spans = [f"{row['surface']} [{row['start']},{row['end']})" for row in hits]
    return "<br>".join(aliases), "<br>".join(roles), "<br>".join(spans)


def table_one(openings, previous_controls, controls, match_index):
    rows = []
    for item in openings:
        rid = item["request_id"]
        aliases, roles, spans = format_match(match_index[rid, "raw"])
        location = f"{item['excerpt']} [{item['excerpt_start']},{item['excerpt_end']})"
        status = {"hash_identical": "일치", "current_reacquired": "차이", "access_failed": "접근 실패"}[item["status"]]
        note = f"{item['source_id']} · {item['location']} · {item['limit']}"
        rows.append((
            f"{rid} · {TIERS[item['status']][0]} · [#1]({item['url']})",
            status, spans or location, aliases, roles, note,
        ))
    for i, item in enumerate(previous_controls, 1):
        rid = item["request_id"]
        aliases, roles, spans = format_match(match_index[rid, "raw"])
        rows.append((
            f"{rid} · 기존 구성 · [선행 body]({P122}/evidence/controls.jsonl#L{i})",
            "body 고정", spans or f"{item['body'][:27]} [0,27)", aliases, roles,
            "선행 기준 및 [구간 기록](matches.csv)",
        ))
    for i, item in enumerate(controls, 1):
        rid = item["request_id"]
        aliases, roles, spans = format_match(match_index[rid, "raw"])
        rows.append((
            f"{rid} · 새 대조 · [구성문](controls.jsonl#L{i})",
            "사전 봉인", spans, aliases, roles,
            f"[원 용례]({item['source_urls'][0]}) · 직접 {', '.join(item['expected_direct_ids']) or '0'}",
        ))
    return md_table(
        ("요청·층·게시물 URL", "원문 해시 일치 여부", "원문 구절·오프셋", "별칭·조사", "지칭 대상·발화 역할", "근거·미확인"),
        rows,
    )


def effects_text(rows):
    parts = []
    for label, row in rows:
        entered, lost, moved = [row[key].replace("|", ", ").replace(">", "→") for key in ("added", "lost", "moved")]
        if entered or lost or moved:
            parts.append(f"{label} +{entered or '—'} / −{lost or '—'} / 이동 {moved or '—'}")
    return "<br>".join(parts) or "—"


def table_two(inquiries, transitions, urls, labels):
    edges = {(r["request_id"], r["view"], r["after"], r["stage"]): r for r in transitions}
    rows = []
    for request, view, policy in sorted(inquiries, key=lambda row: (row[0], VIEWS.index(row[1]), row[2])):
        pools = inquiries[request, view, policy]
        counts = {stage: label_counts(request, ids, labels) for stage, ids in pools.items()}
        changes = []
        for stage, edge_label in (("investigation", "조"), ("display", "표")):
            if policy != "A":
                changes.append((f"{policy} {edge_label}", edges[request, view, policy, stage]))
            if view == "masked":
                changes.append((f"가림 {edge_label}", edges[request, "raw→masked", f"masked-{policy}", stage]))
        candidates = pools["display"]
        conflicts = [fid for fid in candidates if labels[request, fid]["verdict"] == "명시충돌"]
        lost = [piece.split(":")[0] for _, entry in changes for piece in entry["lost"].split("|") if piece]
        counter = (conflicts or lost or candidates or pools["investigation"])[:1]
        link = f"[{counter[0]} 근거]({labels[request, counter[0]]['api_url']})" if counter else f"[요청 근거]({urls[request]})"
        ranked = " · ".join(
            f"{label} {'→'.join(pools[stage]) or '—'} ({LIMITS[stage] - len(pools[stage])}공석)"
            for stage, label in (("investigation", "조"), ("display", "표"))
        )
        stages = " · ".join(
            f"{label} " + "/".join(str(counts[stage][verdict]) for verdict in VERDICTS)
            for stage, label in (("investigation", "조"), ("display", "표"))
        )
        rows.append((f"{request} · {'원문' if view == 'raw' else '가림'}", policy, ranked, stages, effects_text(changes), link))
    return md_table(
        ("요청·원문 또는 가림", "정책", "조사 8·표시 3", "직접·일부·충돌·미확인", "유입·탈락 ID와 순위", "반대 근거 URL"),
        rows,
    )


def table_three(metrics, replay_matches):
    def outcomes(row, names):
        return "/".join(str(row[name]) for name in names)

    rows = []
    for row in metrics:
        tier = row["tier"]
        view = "원문" if row["view"] == "raw" else "가림"
        label = f"{row['title']} · {view} · {row['policy']}"
        if row["measured_requests"] == 0:
            rows.append((label, f"{row['scheduled']}/0", "0/0/0 · 0/0", "미실행 · 직접률 산출 불가", "해당 요청 0", "미실행", "해당 없음"))
            continue
        outcomes_pair = " · ".join(
            f"{tag} " + outcomes(row[stage], ("직접", "일부"))
            for stage, tag in (("investigation", "조"), ("display", "표"))
        )
        outcomes_pair += f" · 표시 직접률 {row['display']['직접']}/{row['direct_pairs']}" if row["direct_pairs"] else " · 직접률 산출 불가"
        problems = " · ".join(
            f"{tag} " + outcomes(row[stage], ("명시충돌", "미확인", "공석"))
            for stage, tag in (("investigation", "조"), ("display", "표"))
        )
        cost = row["cost"]
        inspected = cost["candidate_windows_shared_bcd"] if row["policy"] != "A" else 0
        rows.append((
            label, f"{row['scheduled']}/{row['measured_requests']}",
            f"{row['direct_eligible_requests']}/{row['partial_eligible_requests']}/{row['eligible_requests']} · {row['direct_pairs']}/{row['partial_pairs']}",
            outcomes_pair, problems,
            f"후보/영문/별칭 {cost['candidate_comparisons']}/{cost['english_token_checks']}/{cost['alias_checks']} · 창 {inspected} · 판독 구간 {row['all_annotated_spans_in_view']} / 쌍 {row['criteria_pairs_reviewed_once']}",
            "일치" if replay_matches else "불일치",
        ))
    return md_table(
        ("층·정책", "예정·실측 요청", "적격 요청·쌍", "조사·표시 직접과 일부", "충돌·미확인·공석", "규칙 확인·원문 판독 비용", "두 재생 일치"),
        rows,
    )


def summarize(data, prior, replay, output):
    prepare, legacy = load_previous(prior)
    openings = prepare.read_jsonl(data / "openings.jsonl")
    existing = prepare.read_jsonl(prior / "evidence/controls.jsonl")
    controls = prepare.read_jsonl(data / "controls.jsonl")
    tiers = {row["request_id"]: row["status"] for row in openings}
    tiers.update({row["request_id"]: "existing_control" for row in existing})
    tiers.update({row["request_id"]: "new_control" for row in controls})
    measured = {request for request in tiers if tiers[request] != "access_failed"}
    labels = read_labels(data, prior, prepare, tiers)
    groups, inquiries = read_queries(replay, labels, measured, prepare)
    annotations = prepare.read_csv(data / "matches.csv")
    annotation_index = verify_annotations(controls, annotations, groups, labels)
    source_metrics = check_sources(
        prepare.read_jsonl(data / "sources.jsonl"), annotations, openings, prepare.read_csv(replay / "domain-cases.csv")
    )
    replay_costs = prepare.read_csv(replay / "replay-costs.csv")
    costs = {(row["request_id"], row["view"], row["policy"]): row for row in replay_costs}
    if set(costs) != set(inquiries) or len(costs) != len(replay_costs):
        raise ValueError("cost counts do not cover the replay")
    metric_rows = aggregate(tiers, inquiries, costs, labels, annotation_index)
    transitions = prepare.read_csv(replay / "transitions.csv")
    transition_rows, effect_metrics = transition_metrics(transitions, labels, tiers)
    receipt = json.loads((data / "evidence/replay-runs.json").read_text(encoding="utf-8"))
    replay_matches = len(receipt["runs"]) == 2 and not receipt["differences"] and all(
        legacy.file_sha(replay / name) == sha
        for name, sha in receipt["runs"][0]["output"]["output_sha256"].items()
    )

    urls = {row["request_id"]: row["url"] for row in openings}
    urls.update({row["request_id"]: f"{P122}/evidence/controls.jsonl" for row in existing})
    urls.update({row["request_id"]: row["source_urls"][0] for row in controls})
    table_blocks = [
        "# AF-RES-126 결과",
        "## 표 1 · 고정 요청과 구간",
        table_one(openings, existing, controls, annotation_index),
        "## 표 2 · 요청, 정책 및 상한",
        "조는 조사, 표는 표시다. 증감은 해당 뷰의 직전 정책 대비이며 가림 증감은 같은 정책의 원문 대비다. 순위 0은 양수 후보 밖이다. 판독 수의 순서는 직접/일부/명시충돌/미확인이다.",
        table_two(inquiries, transitions, urls, labels),
        "## 표 3 · 층별 분모, 표시 손익과 비용",
        "적격 요청은 직접/일부/합집합, 쌍은 직접/일부 순이다. 동일·현행·실패는 공개 예정 10건을 분할한 조건부 층이다. 표의 두 뷰는 같은 요청을 반복한다. ‘창’은 B/C/D가 공유한 후보 창 수이며 행 사이에 더하지 않는다. 구간 판독과 후보 적격 기준은 정책별로 반복해 세지 않는다.",
        table_three(metric_rows, replay_matches),
    ]
    output.mkdir(parents=True, exist_ok=True)
    (output / "tables.md").write_text("\n\n".join(table_blocks) + "\n", encoding="utf-8")
    legacy.write_csv(output / "policy-effects.csv", transition_rows)
    legacy.write_csv(output / "investigation-only.csv", compare_placement(inquiries, labels))
    metrics = {
        "tier_request_counts": dict(Counter(tiers.values())),
        "forum_requested": len(openings),
        "measured_requests": len(measured),
        "query_count": len(inquiries),
        "criteria_pairs": len(labels),
        "annotated_span_rows": len(annotations),
        "new_control_predicted_queries_checked": len(controls) * len(VIEWS),
        "sources": source_metrics,
        "replay_matches": replay_matches,
        "groups": metric_rows,
        "transitions": effect_metrics,
    }
    (output / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return {
        "output_sha256": {name: legacy.file_sha(output / name) for name in (
            "tables.md", "policy-effects.csv", "investigation-only.csv", "metrics.json",
        )},
        "measured_requests": len(measured), "criteria_pairs": len(labels),
        "unique_primary_sources": source_metrics["unique_works"], "same_rank_and_slots": replay_matches,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=HERE)
    parser.add_argument("--prior", type=Path, required=True)
    parser.add_argument("--ranks", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(summarize(args.data, args.prior, args.ranks, args.out), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
