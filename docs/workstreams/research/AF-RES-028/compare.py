#!/usr/bin/env python3
"""Join only the verified revealed answer with the sealed checks and fixed policy runs."""
import argparse
from collections import Counter, defaultdict
import csv
from hashlib import sha256
import io
import json
from pathlib import Path
import subprocess

from draw import from_git, canonical

HERE = Path(__file__).resolve().parent
LABELS = ("supported", "invalid", "initial_error", "unknown")
SCENARIOS = {f"{p}-20-t2-cold-charged-once-both": p for p in ("D", "S")}
KNOWN = {"doesNotReject", "triggerAsyncId", "createHook", "child_process.exec", "--heap-prof",
         "isConnected", "console.debug", "channel.unsubscribe", "resolve4", "domain.intercept",
         "ERR_CRYPTO_INVALID_KEYLEN", "events.listenerCount"}


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def digest(data):
    return sha256(data).hexdigest()


def old_policy(keys):
    policy = {}
    actions = defaultdict(list)
    open_status = {}
    for r in csv.DictReader(io.StringIO(from_git("visits.csv").decode())):
        if r["scenario"] not in SCENARIOS:
            continue
        p = SCENARIOS[r["scenario"]]
        if r["entry_type"] == "reason":
            key = (r["quarter"], r["id"], p)
            if key[:2] in keys:
                policy[key] = r
        elif r["kind"] == "manual":
            action_key = (r["quarter"], r["ecosystem"], r["path"], p)
            if r["status"] not in {"shared", "budget"}:
                open_status[action_key] = r["status"]
            key = (r["quarter"], r["reason_id"], p)
            if key[:2] in keys:
                actions[key].append(r)
    return policy, actions, open_status


def prediction(state, alert):
    if state == "supported":
        return "FP" if alert else "TN"
    if state == "invalid":
        return "TP" if alert else "FN"
    return "censored"


def counts(values):
    data = Counter(values)
    return {name: data[name] for name in ("TP", "FP", "FN", "TN", "censored")}


def group_summary(group, name):
    sources = Counter((r["prior_state"], r["runtime_state"]) for r in group)
    enabled = {"supported", "invalid"}
    both = [r for r in group if r["prior_state"] in enabled and r["runtime_state"] in enabled]
    policy = {}
    for p in ("D", "S"):
        paired = Counter((r[f"{p}_old"], r[f"{p}_new"]) for r in both)
        invalidity_miss = [r for r in group if r[f"{p}_new"] == "FN"]
        policy[p] = dict(old=counts(r[f"{p}_old"] for r in group), revised=counts(r[f"{p}_new"] for r in group),
                         paired_old=counts(r[f"{p}_old"] for r in both),
                         paired_new=counts(r[f"{p}_new"] for r in both),
                         transitions={f"{a}->{b}": n for (a, b), n in sorted(paired.items())},
                         manual_attempt=sum(r[f"{p}_manual_tried"] for r in group),
                         manual_read=sum(r[f"{p}_manual_read"] for r in group),
                         nonvisit_fn=sum(not r[f"{p}_manual_tried"] for r in invalidity_miss),
                         unread_after_attempt_fn=sum(r[f"{p}_manual_tried"] and not r[f"{p}_manual_read"] for r in invalidity_miss),
                         read_fn=sum(r[f"{p}_manual_read"] for r in invalidity_miss),
                         new_reports=sum(r[f"{p}_new_report"] for r in group),
                         prior_alerts=sum(r[f"{p}_predicted_invalid"] for r in group))
    return dict(layer=name, n=len(group), independent_reasons=len({r['reason_id'] for r in group}),
                groups=len({r['group_id'] for r in group}),
                release_count=len({(r['ecosystem'],r['target_version']) for r in group}),
                reason_release=len({(r['reason_id'],r['target_version']) for r in group}),
                source_states={f"{a}/{b}": n for (a, b), n in sorted(sources.items())},
                verdicts={s:sum(r["runtime_state"] == s for r in group) for s in LABELS},
                direct_pairs=sum(r["direct_pair"] for r in group),
                disagreements=sum(r["prior_state"] != r["runtime_state"] for r in group),
                unknown=sum(r["runtime_state"] == "unknown" for r in group),
                rows=[r["cell_id"] for r in group], policy=policy)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--answer", type=Path, required=True)
    parser.add_argument("--sealed-commit", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    owned = HERE.relative_to(Path(subprocess.check_output(["git","rev-parse","--show-toplevel"],text=True).strip()))
    get_seal = ["git", "show", f"{args.sealed_commit}:{owned}/observation-seal.json"]
    sealed = json.loads(subprocess.check_output(get_seal))
    for name, expected in sealed["blinded"].items():
        if digest((HERE / name).read_bytes()) != expected:
            raise ValueError(f"Working evidence differs from sealed Git evidence: {name}")
    lock = json.loads((HERE / "scope-lock.json").read_text())
    raw = args.answer.read_bytes()
    if digest(raw) != lock["answer_sha256"]:
        raise ValueError("Reveal key does not match committed hash")
    keys = [json.loads(line) for line in raw.splitlines()]
    obs = {r["cell_id"]: r for r in rows(HERE / "observations.jsonl")}
    source_read = {r["cell_id"]: r for r in rows(HERE / "blind-review.jsonl")}
    packets = {r["cell_id"]: r for r in rows(HERE / "packets.jsonl")}
    asked = {(r["quarter"],r["reason_id"]) for r in keys}
    policy, actions, open_status = old_policy(asked)
    assert len(policy) == 84 and len(asked) == len(keys) == 42
    disclosed = []
    for answer in keys:
        c = answer["cell_id"]
        q, rid, eco = answer["quarter"], answer["reason_id"], answer["ecosystem"]
        o, source, packet = obs[c], source_read[c], packets[c]
        assert o["quarter"] == q and o["ecosystem"] == eco
        old, new = answer["prior"], o["verdict"]
        name = dict(supported="유지", invalid="무효", initial_error="최초 오류", unknown="보류")
        row = dict(cell_id=c, ecosystem=eco, quarter=q, reason_id=rid, group_id=answer["group_id"],
                   t0_version=packet["t0"]["tag"], target_version=packet["target"]["tag"],
                   inclusion=answer["inclusion"], sample_rank=answer["draw_rank"], baseline_warned=answer["warned"]=="1",
                   experimental=answer["experimental"]=="1", section=answer["section"],
                   prior_state=old["state"], prior_basis=old["basis"], prior_evidence=old["release_source"],
                   prior_event=old["event_group"], prior_notice=old["notice"],
                   prior_notice_by_cutoff=bool(old["notice"] and old["notice"]<=packet["target"]["cutoff"]),
                   prior_route=answer["route"], prior_t0_url=answer["t0_url"], prior_t0_state=answer["t0_initial"],
                   direct_pair=o["direct_pair"], runtime_state=new, primary_runtime_reason=o["reason"],
                   runtime_v1=o["run_verdict_v1"], runtime_alternative=o["alternative_verdict"],
                   runtime_alternative_scope=o.get("alternative_scope",""),
                   initial_claim_exposure=eco=="node" and any(rid.endswith("/"+symbol) or rid.endswith("."+symbol)
                                                            for symbol in KNOWN),
                   agreement="일치" if old["state"]==new else f"{name[old['state']]}→{name[new]}",
                   t0_receipt=o["t0"], target_receipt=o["target"],
                   t0_doc=source["t0_source"], target_doc=source["target_source"],
                   contemporary_doc=source["target_document"], static_ids=" ".join(source["static_sources"]),
                   pydoc_literal_post_reveal="initial_error on literal executable name; ambiguous across packaging" if o["contract"]=="pydoc" else "")
        for p in ("D","S"):
            k = (q,rid,p)
            v = policy[k]
            direct_actions = actions[k]
            status = [a["status"] for a in direct_actions]
            acquired = open_status.get((q,eco,v["path"],p))
            attempted = any(s != "budget" for s in status)
            readable = ("ok" in status) or ("shared" in status and acquired=="ok")
            predicted_invalid = v["predicted_invalid"]=="True"
            row.update({f"{p}_predicted_invalid":predicted_invalid, f"{p}_new_report":v["new_report"]=="True",
                        f"{p}_manual_status":"|".join(status), f"{p}_manual_tried":attempted,
                        f"{p}_manual_read":readable, f"{p}_outcome":v["outcome"],
                        f"{p}_proof_kind":v["proof_kind"], f"{p}_proof_url":v["proof"],
                        f"{p}_warning_prior":v["warning_prior"]=="True",f"{p}_signal":v["signal"]=="True",
                        f"{p}_old":prediction(old["state"],predicted_invalid), f"{p}_new":prediction(new,predicted_invalid)})
        disclosed.append(row)
    groups = {"all":disclosed}
    for label in LABELS:
        group = [r for r in disclosed if r["prior_state"]==label]
        groups[label]=group
        for eco in ("python","node"):
            groups[label+"/"+eco]=[r for r in group if r["ecosystem"]==eco]
    main = groups["supported"]
    for field in ("baseline_warned","prior_notice_by_cutoff","S_signal","S_warning_prior","section"):
        for key in sorted({str(r[field]) for r in disclosed}):
            groups[f"all/{field}={key}"]=[r for r in disclosed if str(r[field])==key]
            groups[f"supported/{field}={key}"]=[r for r in main if str(r[field])==key]
    groups["controls"] = [r for r in disclosed if r["prior_state"]!="supported"]
    for id in [r["cell_id"] for r in disclosed if r["runtime_alternative"]]:
        altered = [dict(r) for r in disclosed]
        case = next(r for r in altered if r["cell_id"]==id)
        case["runtime_state"] = case["runtime_alternative"]
        for p in ("D","S"):
            case[f"{p}_new"] = prediction(case["runtime_state"],case[f"{p}_predicted_invalid"])
        groups[f"all alternative {id}"] = altered
    strict_entry = [dict(r) for r in disclosed]
    literal_cli = next(r for r in strict_entry if r["cell_id"] == "A028-20")
    literal_cli["runtime_state"] = "initial_error"
    for p in ("D", "S"):
        literal_cli[f"{p}_new"] = prediction("initial_error", literal_cli[f"{p}_predicted_invalid"])
    groups["all strict pydoc executable"] = strict_entry
    args.out.mkdir(parents=True,exist_ok=True)
    with (args.out/"comparison.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(disclosed[0]),lineterminator="\n")
        w.writeheader()
        w.writerows(disclosed)
    tab = {name:group_summary(group,name) for name,group in groups.items()}
    tab["strata_lock"] = lock["allocation"]
    tab["reveal"] = dict(prior_commit=lock["afr024_commit"], sealed_commit=args.sealed_commit,
                          answer_sha256=lock["answer_sha256"],
                          policy_input_sha256=digest(from_git("visits.csv")),
                          policy_scenarios=SCENARIOS, exposed_sample=[r["cell_id"] for r in disclosed if r["initial_claim_exposure"]],
                          supported_untested=897-len(main),
                          primary_hidden_invalid=sum(r["runtime_state"]=="invalid" for r in main),
                          primary_unconfirmed=sum(r["runtime_state"]=="unknown" for r in main))
    (args.out/"tabulations.json").write_bytes(canonical(tab)+b"\n")
    print([(name,r["n"],r["source_states"]) for name,r in tab.items() if name in LABELS])


if __name__ == "__main__":
    main()
