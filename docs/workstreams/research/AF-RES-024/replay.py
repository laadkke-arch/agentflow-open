"""Independently score policy visits against the dated adjudication and aggregate costs."""

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import replace
from datetime import date
from pathlib import Path
from statistics import median

from acquire import HERE, read_jsonl, write_jsonl
from policy import Config, Inputs, replay, write_csv

FIELDS = ("http_attempts", "http_body_bytes", "git_pack_bytes", "new_objects",
          "local_reads", "local_bytes", "retries", "elapsed_s")
FAVORED = ("N-20-t2-cold-charged-once-both", "D-20-t2-cold-charged-once-both",
           "S-20-t2-cold-charged-once-both", "O-known-address")


def configurations():
    yield Config("N")
    for name in ("D", "S"):
        cfg = Config(name)
        for budget in (10, 20, 40):
            yield replace(cfg, budget=budget)
        for cache in ("reuse1", "reuse2"):
            yield replace(cfg, cache=cache)
        for failure in ("stress_charged", "stress_free_review"):
            yield replace(cfg, failure=failure)
        yield replace(cfg, shared="per_reason")
        for eco in ("python", "node"):
            yield replace(cfg, ecosystem=eco)
    for threshold in (1, 3):
        yield Config("S", threshold=threshold)


def build_timeline(inp, key):
    events = {reason: e for e in key["events"] for reason in e["reason_ids"]}
    assert sum(len(e["reason_ids"]) for e in key["events"]) == len(events)
    timeline = []
    seen = set()
    for q in ["T0", *inp.quarters]:
        view = inp.views[q] if q != "T0" else read_jsonl(inp.folder / "snapshots" / "T0.jsonl")
        for doc in view:
            for item in doc.get("reasons", []):
                id = item["id"]
                eco = doc["ecosystem"]
                r, release = inp.cohort[id], inp.releases[q, eco]
                until = release["cutoff"]
                assert release["public_date"] <= until
                assert (q, id) not in seen
                seen.add((q, id))
                e = events.get(id)
                if id in key["initial_errors"]:
                    state, why = "initial_error", key["initial_errors"][id]
                elif id in key["uncertain"]:
                    state, why = "unknown", key["uncertain"][id]["basis"]
                elif e and e["effective_date"] <= until and (not e.get("restored_date") or
                                                             e["restored_date"] > until):
                    state, why = "invalid", e["change"]
                elif doc["status"] != "ok" or item["section"] != "present":
                    state, why = "unknown", "태그 스냅샷에 대응 절을 찾지 못했다."
                else:
                    state, why = "supported", "해당 용례를 뒷받침하는 절이 확인됐다. 실행과 날짜 사이 변화는 별도다."
                findings = [p for p in inp.findings[q, doc["ecosystem"], "manual", doc["path"]] if p["id"] == id]
                timeline.append(dict(
                    id=id, ecosystem=eco, stratum=r["stratum"], quarter=q, cutoff=until,
                    version=release["tag"], published_date=release["public_date"], commit=release["commit"],
                    t0_initial=r["initial"], claim=r["claim"], policy_route=doc["url"],
                    observed=dict(path=doc["path"], http=doc["raw_status"], status=doc["status"],
                                  blob=doc["blob"], locations=item,
                                  manual_readings=[{k: p[k] for k in ("status", "location", "url")}
                                                   for p in findings]),
                    adjudication=dict(state=state, basis=why,
                                      sources=key["uncertain"].get(id, {}).get("sources", []),
                                      event_group=e["event_group"] if e else "",
                                      notice=e["notice_date"] if e else "", enact=e["effective_date"] if e else "",
                                      release_source=e["release_source"] if e else "",
                                      implementation_sources=e["implementation_sources"] if e else []),
                ))
    assert len(seen) == (len(inp.quarters) + 1) * len(inp.cohort)
    return timeline


def load_oracle_receipts(folder):
    out = {}
    for name in ("truth-acquisition", "truth-supplemental", "netrc-bracket"):
        for row in read_jsonl(folder / "evidence" / f"{name}.jsonl"):
            out[row["url"]] = row
    return out


def oracle(data, key, adjudication):
    """The direct known address is permitted here after a confirmed effect date."""
    by_reason = {r: e for e in key["events"] for r in e["reason_ids"]}
    seen, found = set(), set()
    rows, actions = [], []
    receipts = load_oracle_receipts(data.folder)
    for r in adjudication:
        if r["quarter"] == "T0":
            continue
        id, q, eco = r["id"], r["quarter"], r["ecosystem"]
        truth = r["adjudication"]["state"]
        is_new = id not in found and truth == "invalid"
        row = dict(scenario=FAVORED[3], id=id, quarter=q, ecosystem=eco, stratum=r["stratum"],
                   predicted_invalid=truth == "invalid" and (id in found or is_new), score=0, signal=False,
                   new_signal=False, warning_prior=False, new_report=is_new,
                   outcome="oracle_invalid" if is_new else "oracle_no_visit", proof="", proof_kind="")
        if is_new:
            e = by_reason[id]
            url = e["oracle_url"]
            proof = receipts[url]
            assert proof["status"] == "ok", f"Missing independently opened oracle source {url}"
            row["proof"] = url
            row["proof_kind"] = "given_event_url"
            found.add(id)
            shared = (q, url) in seen
            seen.add((q, url))
            actions.append(dict(
                scenario=FAVORED[3], id=id, quarter=q, ecosystem=eco, kind="given_event_url",
                url=url, path=proof["path"], status="shared" if shared else "ok",
                opened_original=not shared, review_units=int(not shared),
                **{k: 0 if shared else proof[k] for k in FIELDS},
            ))
        rows.append(row)
    return rows, actions


def fraction(a, b):
    return round(a / b, 6) if b else None


def distribution(values):
    values = sorted(values)
    if not values:
        return dict(n=0, min=None, median=None, max=None, values=[])
    return dict(n=len(values), min=values[0], median=median(values), max=values[-1], values=values)


def delay(start, end):
    return (date.fromisoformat(end) - date.fromisoformat(start)).days


def first_findings(rows, event_map, truth):
    found = {}
    for row in rows:
        id, q = row["id"], row["quarter"]
        if id not in event_map or id in found or row["outcome"].split("_")[-1] != "invalid":
            continue
        if truth[q, id]["adjudication"]["state"] != "invalid":
            continue
        found[id] = row
    return found


def summarize(rows, network, key, verdicts, scope, stratum, config):
    rows = [r for r in rows if (scope == "all" or r["ecosystem"] == scope) and
            (stratum == "all" or r["stratum"] == stratum)]
    events = {id: e for e in key["events"] for id in e["reason_ids"]}
    ids = {r["id"] for r in rows}
    ev_set = {id: e for id, e in events.items() if id in ids}
    found = first_findings(rows, ev_set, verdicts)
    event_groups = {e["event_group"] for e in ev_set.values()}
    found_groups = {ev_set[id]["event_group"] for id in found}
    counts = Counter()
    warning = Counter()
    previous_cutoffs = {}
    for row in rows:
        verdict = verdicts[row["quarter"], row["id"]]
        before = previous_cutoffs.get(row["id"], verdicts["T0", row["id"]]["cutoff"])
        previous_cutoffs[row["id"]] = verdict["cutoff"]
        state = verdict["adjudication"]["state"]
        predicted = row["predicted_invalid"]
        if state == "initial_error":
            counts["initial_error"] += 1
            continue
        if state == "unknown":
            counts["unknown_pos" if predicted else "unknown_neg"] += 1
        else:
            counts[("TP" if predicted else "FN") if state == "invalid" else
                   ("FP" if predicted else "TN")] += 1
        if row["new_report"]:
            counts[f"report_{state}"] += 1
        if row["signal"]:
            warning["signal_count"] += 1
            warning[f"signal_{state}"] += 1
            if row["new_signal"]:
                warning["signal_new"] += 1
            else:
                warning["signal_carry"] += 1
            if row["quarter"] == "2022Q1" and row["warning_prior"]:
                warning["t0_warning_active_q1"] += 1
            event = ev_set.get(row["id"])
            if event:
                if verdict["cutoff"] < event["notice_date"]:
                    warning["signal_before_notice"] += 1
                    warning["new_before_notice"] += int(row["new_signal"])
                plan = event.get("removal_plan_date")
                if plan and verdict["cutoff"] < plan:
                    warning["signal_before_removal_plan"] += 1
            if event and state == "invalid":
                warning["signal_at_onset"] += int(before < event["effective_date"] <= verdict["cutoff"])
    times_effect = []
    times_notice = []
    discoveries = []
    for id, e in ev_set.items():
        hit = found.get(id)
        when = verdicts[(hit["quarter"], id)]["cutoff"] if hit else None
        nlag = delay(e["notice_date"], when) if when else None
        elag = delay(e["effective_date"], when) if when else None
        if hit:
            times_effect.append(elag)
            times_notice.append(nlag)
        discoveries.append(dict(scenario=config, id=id, event_group=e["event_group"],
                                notice_date=e["notice_date"], notice_basis=e["notice_basis"],
                                effective_date=e["effective_date"], discovery_date=when,
                                notice_delay_days=nlag, effective_delay_days=elag,
                                effective_delay_max_days=delay(e.get("effective_earliest", e["effective_date"]), when)
                                if when else None,
                                proof=hit["proof"] if hit else "", missed=not hit))
    tp, fp, fn, tn = (counts[name] for name in ("TP", "FP", "FN", "TN"))
    unknown_pos, unknown_neg = counts["unknown_pos"], counts["unknown_neg"]
    net = [a for a in network if scope == "all" or a["ecosystem"] == scope]
    opened = sum(a.get("opened_original", False) for a in net)
    numq = len({r["quarter"] for r in rows})
    report_count = sum(counts["report_" + key] for key in ("invalid", "supported", "unknown"))
    monitored = len(rows) - counts["initial_error"]
    out = dict(
        scenario=config, ecosystem=scope, stratum=stratum, reasons=len(ids), quarters=numq,
        reason_quarters=len(rows), scored=tp+fp+fn+tn, event_groups=len(event_groups),
        event_reasons=len(ev_set), groups_seen=len(found_groups), reasons_seen=len(found),
        missed_groups=len(event_groups-found_groups), missed_reasons=len(ev_set)-len(found),
        initial_error=counts["initial_error"], unknown=unknown_pos + unknown_neg,
        TP=tp, FP=fp, FN=fn, TN=tn,
        precision=fraction(tp,tp+fp), recall=fraction(tp,tp+fn),
        precision_unknown_negative=fraction(tp,tp+fp+unknown_pos),
        recall_unknown_negative=fraction(tp,tp+fn),
        precision_unknown_positive=fraction(tp+unknown_pos,tp+fp+unknown_pos),
        recall_unknown_positive=fraction(tp+unknown_pos,tp+fn+unknown_pos+unknown_neg),
        new_reports=report_count, report_TP=counts["report_invalid"], report_FP=counts["report_supported"],
        report_unknown=counts["report_unknown"],
        report_precision=fraction(counts["report_invalid"],counts["report_invalid"]+counts["report_supported"]),
        monitored_reason_quarters=monitored,
        reports_per_100_reason_quarters=fraction(100*report_count,monitored),
        event_recall=fraction(len(found),len(ev_set)),
        observed_gaps=sum(r["outcome"] in {"evidence_gap","manual_uncertain","failed"} for r in rows),
        not_visited=sum(r["outcome"] in {"no_visit","below_threshold","budget","oracle_no_visit"} for r in rows),
        evidence_public_delay_min=distribution(times_notice)["min"],
        evidence_public_delay_median=distribution(times_notice)["median"],
        evidence_public_delay_max=distribution(times_notice)["max"],
        effect_delay_min=distribution(times_effect)["min"],
        effect_delay_median=distribution(times_effect)["median"],
        effect_delay_max=distribution(times_effect)["max"],
        screens=warning["signal_count"], screens_new=warning["signal_new"], screens_carry=warning["signal_carry"],
        screens_at_onset=warning["signal_at_onset"], screens_seeded_at_q1=warning["t0_warning_active_q1"],
        screens_before_notice=warning["signal_before_notice"], new_screens_before_notice=warning["new_before_notice"],
        screens_before_explicit_removal_plan=warning["signal_before_removal_plan"],
        screen_TP=warning["signal_invalid"], screen_FP=warning["signal_supported"],
        screen_FN=tp+fn-warning["signal_invalid"], screen_TN=fp+tn-warning["signal_supported"],
        screen_unknown=warning["signal_unknown"],
        screen_precision=fraction(warning["signal_invalid"],warning["signal_invalid"]+warning["signal_supported"]),
        screens_per_100_reason_quarters=fraction(100*warning["signal_count"],monitored),
        opened_originals=opened if stratum == "all" else None,
        case_http_attempts=sum(a.get("http_attempts",0) for a in net) if stratum == "all" else None,
        case_http_bytes=sum(a.get("http_body_bytes",0) for a in net) if stratum == "all" else None,
    )
    assert out["scored"] + out["unknown"] + out["initial_error"] == out["reason_quarters"]
    return out, discoveries


def costs_for(folder, actions, metrics):
    costs = []
    for cache in ("cold","reuse1","reuse2"):
        rows = read_jsonl(folder / "evidence" / "runs" / f"{cache}.jsonl")
        receipts = [r for q in rows for r in read_jsonl(folder / "evidence" / "receipts" / cache /
                                                       f"{q['quarter']}.jsonl")]
        costs.append(dict(
            scope="full_fixture_measured", scenario="all_sources", cache=cache,
            successful=sum(r["status"]=="ok" for r in receipts),
            missing=sum(r["status"]=="missing" for r in receipts),
            failed=sum(r["status"] not in {"ok","missing"} for r in receipts),
            opened_originals=sum(r["kind"]!="git_tree" and r["status"]=="ok" for r in receipts),
            duplicate_attempts=sum(max(0,r["http_attempts"]-1) for r in receipts if r["kind"]!="git_tree"),
            http_304=sum(r["http_status"]==304 for r in receipts),
            wall_s=round(sum(q["wall_s"] for q in rows),6),
            **{k: round(sum(r[k] for r in receipts),6) for k in FIELDS},
        ))
    prep = load_oracle_receipts(folder)
    prep_rows = list(prep.values())
    costs.append(dict(scope="truth_source_preparation_measured", scenario="direct_inputs", cache="mixed",
                      successful=sum(r["status"] == "ok" for r in prep_rows),
                      missing=sum(r["http_status"] == 404 for r in prep_rows),
                      failed=sum(r["status"] != "ok" and r["http_status"] != 404 for r in prep_rows),
                      opened_originals=sum(r["status"] == "ok" for r in prep_rows),
                      duplicate_attempts=sum(max(0,r["http_attempts"]-1) for r in prep_rows),
                      http_304=sum(r["http_status"] == 304 for r in prep_rows),
                      **{k: round(sum(r[k] for r in prep_rows), 6) for k in FIELDS}))
    for m in metrics:
        if m["stratum"] != "all" or m["ecosystem"] != "all":
            continue
        sc = m["scenario"]
        a = [a for a in actions if a["scenario"] == sc and a["status"] not in
             {"budget","shared","semantic_share"}]
        total = {k: round(sum(r.get(k,0) for r in a),6) for k in FIELDS}
        costs.append(dict(
            scope="policy_replay_receipt_projection", scenario=sc,
            cache=sc.split("-")[3] if sc != FAVORED[3] else "given_address",
            opened_originals=m["opened_originals"], successful=sum(r["status"]=="ok" for r in a),
            missing=sum(r["status"]=="missing" for r in a), failed=sum(r["status"]=="failure" for r in a),
            reasons_seen=m["reasons_seen"], groups_seen=m["groups_seen"], missed_reasons=m["missed_reasons"],
            extra_opens_per_reason_vs_N=fraction(m["opened_originals"],m["reasons_seen"]),
            extra_opens_per_group_vs_N=fraction(m["opened_originals"],m["groups_seen"]),
            bytes_per_reduced_miss_vs_N=fraction(total["http_body_bytes"],m["reasons_seen"]),
            requests_per_reduced_miss_vs_N=fraction(total["http_attempts"],m["reasons_seen"]),
            **total,
        ))
    return costs


def scenario_decisions(metrics):
    lookup = {r["scenario"]: r for r in metrics if r["ecosystem"] == r["stratum"] == "all"}
    setups = (
        ("low_budget", 10, "cold", 30, 0.01, 1.0, 1.0, 0.0),
        ("scarce_reading_time", 20, "cold", 30, 0.01, 1.0, 1.0, 0.0),
        ("costly_miss", 20, "cold", 100, 0.01, 1.0, 1.0, 0.1),
        ("preloaded_documents", 20, "reuse2", 100, 0.01, 1.0, 1.0, 0.1),
        ("high_budget", 40, "cold", 100, 0.01, 1.0, 1.0, 0.1),
    )
    for name, budget, cache, miss, fp, open_cost, mib, late in setups:
        chosen = []
        for policy in ("N", "D", "S"):
            config = Config(policy, budget=budget, cache=cache)
            row = lookup[FAVORED[0] if policy == "N" else config.label]
            loss = (miss * row["missed_reasons"] + fp * row["screen_FP"] +
                    open_cost * row["opened_originals"] + mib * row["case_http_bytes"] / 2**20 +
                    late * row["FN"])
            chosen.append(dict(
                environment=name, scenario=policy, cache=cache, budget=budget, miss_penalty=miss,
                false_screen_penalty=fp, document_open_penalty=open_cost, per_MiB_penalty=mib,
                invalid_quarter_penalty=late, missed=row["missed_reasons"], late_quarters=row["FN"],
                open_originals=row["opened_originals"], false_screens=row["screen_FP"],
                body_bytes=row["case_http_bytes"], total_loss=round(loss, 6),
            ))
        least = min(r["total_loss"] for r in chosen)
        yield from (r | {"minimum_for_environment": r["total_loss"] == least} for r in chosen)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=HERE)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    inp = Inputs(args.inputs)
    truth = json.loads((args.inputs / "truth.json").read_text(encoding="utf-8"))
    timeline = build_timeline(inp, truth)
    verdicts = {(r["quarter"],r["id"]):r for r in timeline}
    visits, actions, metrics, found = [], [], [], []
    runs = [(c.label,*replay(inp,c)) for c in configurations()]
    runs.append((FAVORED[3],*oracle(inp,truth,timeline)))
    for label, rows, paths in runs:
        visits.extend({"entry_type":"reason"} | r for r in rows)
        actions.extend(paths)
        ecosystems = sorted({r["ecosystem"] for r in rows})
        for eco in ("all",*ecosystems):
            for stratum in ("all","ordinary","warned"):
                summary, discoveries = summarize(rows,paths,truth,verdicts,eco,stratum,label)
                metrics.append(summary)
                if eco == stratum == "all":
                    found.extend(discoveries)
    visits.extend({"entry_type":"document_attempt"} | r for r in actions)
    write_jsonl(args.out / "timeline.jsonl", timeline)
    for filename, rows in (("visits.csv",visits),("metrics.csv",metrics),("discoveries.csv",found),
                           ("costs.csv",costs_for(args.inputs,actions,metrics)),
                           ("decisions.csv",list(scenario_decisions(metrics)))):
        write_csv(args.out / filename, rows)
    for row in metrics:
        if row["scenario"] in FAVORED and row["ecosystem"] == row["stratum"] == "all":
            print(json.dumps(row, ensure_ascii=False))


if __name__ == "__main__":
    main()
