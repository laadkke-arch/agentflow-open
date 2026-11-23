"""Summarize frozen ranks, independent qrels and cost receipts into reproducible tables."""

import argparse
import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

from capture import lines

ROOT = Path(__file__).resolve().parent
BASE = "https://github.com/laadkke-arch/agentflow-open/blob"
RANK_SEAL = "b74de450e7f0f0ffff150b8662cb840388a17aea"
QREL_SEAL = "41b73e199f9529bc5ce3165532b87d88eb4d62d0"
REPLAY_SEAL = "168d8da351873873fa121932a6dc514386d524cb"
PREFIX = "docs/workstreams/research/AF-RES-072"
PHASES = ("offline", "cold", "repeat", "translated", "failure")
ARMS = ("L", "I", "H", "P")
LABELS = ("direct", "partial", "far")


def table(path):
    with (ROOT/path).open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def stratum(row):
    if row["transfer_eligible"] == "True":
        return "far"
    if row["judgment"] in LABELS:
        return row["judgment"]
    return None


def pinned(revision, file, number, label):
    return f"[{label}]({BASE}/{revision}/{PREFIX}/{file}#L{number})"


def mdrow(values):
    return "| " + " | ".join(str(x).replace("|", "&#124;").replace("\n", " ") for x in values) + " |"


def mdtable(headers, rows):
    return "\n".join([mdrow(headers), mdrow(["---"]*len(headers)), *(mdrow(r) for r in rows)])



def summarize():
    requests = {r["request_id"]:r for r in lines(ROOT/"requests.jsonl") if r["split"]=="holdout"}
    work = {r["work_id"]: r for r in lines(ROOT/"corpus.jsonl")}
    judging = table("qrels.csv")
    qrels = {(q["request_id"],q["work_id"]):q for q in judging}
    qpositions = {q["qrel_id"]:n for n,q in enumerate(judging,2)}
    totals = {case: Counter(stratum(q) for q in judging if q["request_id"]==case)
              for case in requests}
    main_ranks = table("ranks.csv")
    positions = {r["rank_id"]:n for n,r in enumerate(main_ranks,2)}
    route_rows = defaultdict(list)
    for row in main_ranks + table("evidence/alternate-ranks.csv"):
        if row["request_id"] in requests:
            route_rows[row["phase"],row["path"],row["request_id"]].append(row)
    fetch = lines(ROOT/"fetches.jsonl")
    execution = table("costs.csv")
    cost = {(r["phase"],r["path"],r["request_id"]):r for r in execution}
    evidence = {}
    recovered = {}
    for phase in PHASES:
        for arm in ARMS:
            metrics = {}
            for case in requests:
                rows = route_rows[phase,arm,case]
                hits = {label: [] for label in LABELS}
                near = []
                unknown = []
                for r in rows:
                    if not r["work_id"]:
                        continue
                    judgment = qrels[case,r["work_id"]]
                    category = stratum(judgment)
                    if category:
                        hits[category].append(int(r["rank"]))
                    if judgment["judgment"]=="refute":
                        near.append(r["work_id"])
                    if judgment["judgment"]=="unverified":
                        unknown.append(r["work_id"])
                metrics[case] = dict(
                    rank_ids=[r["rank_id"] for r in rows],
                    top3=[r["work_id"] or None for r in rows],
                    denominator={label:totals[case][label] for label in LABELS},
                    recovered={label:len(hits[label]) for label in LABELS},
                    first_in_top3={label:min(hits[label]) if hits[label] else None for label in LABELS},
                    near_misses=near,
                    unverified=unknown,
                )
            recovered[phase,arm] = metrics
            evidence[f"{phase}:{arm}"] = dict(
                cases=metrics,
                numerator={label:sum(r["recovered"][label] for r in metrics.values()) for label in LABELS},
                denominator={label:sum(r["denominator"][label] for r in metrics.values()) for label in LABELS},
                near_miss_slots=sum(len(r["near_misses"]) for r in metrics.values()),
            )
    reading = json.loads((ROOT/"evidence/route-reading.json").read_text())
    observations = {r["fetch_id"]:r for r in reading["observations"]}
    displayed_judgments = []
    for arm in ("L","I","H"):
        for case in requests:
            for r in route_rows["offline",arm,case]:
                trace = next((a["fetch_id"] for a in fetch if a["phase"]=="offline"
                              and a["path"]==arm and a["request_id"]==case and a["work_id"]==r["work_id"]
                              and a["complete"]), None)
                observed = observations.get(trace, {}).get("adjudication")
                action = "rejected" if observed == "reject-as-direct" else "abstained"
                displayed_judgments.append(dict(
                    rank_id=r["rank_id"],request_id=case,path=arm,work_id=r["work_id"],fetch_id=trace,
                    joint_adjudication=action,conditional_piece=observed=="conditional-piece",
                    wrong_adoption=False,
                ))
    figures = dict(
        qrel_categories=dict(Counter(q["judgment"] for q in judging)),
        qrel_cases={r:{label:totals[r][label] for label in LABELS} for r in requests},
        by_method_and_phase=evidence,
        primary_displayed_judgments=displayed_judgments,
        main_network=dict(
            complete=sum(r["transport"]=="http" and r["complete"] for r in fetch),
            exact=sum(r["transport"]=="http" and r["exact_frozen_body"] is True for r in fetch),
            changed=sum(r["transport"]=="http" and r["exact_frozen_body"] is False for r in fetch),
            redirects=sum(len(r["redirects"]) for r in fetch),
        ),
    )
    tables = []
    first_rows = []
    for case,c in requests.items():
        requirement = f"{c['positive']} · 경계 {c['boundary']} · 환경 {c['environment']}"
        for arm in ARMS:
            row = recovered["offline",arm][case]
            rank_id = row["rank_ids"][0]
            slots = []
            for w in row["top3"]:
                if w is None:
                    slots.append("빈칸")
                else:
                    q = qrels[case,w]
                    slots.append(pinned(QREL_SEAL,"qrels.csv",qpositions[q["qrel_id"]],w))
            ratios = []
            for label in LABELS:
                d, n = row["denominator"][label],row["recovered"][label]
                first = row["first_in_top3"][label]
                ratios.append("해당 없음" if d == 0 else f"{n}/{d} ({first}위)" if n else f"0/{d} (3위 밖)")
            near = ", ".join(row["near_misses"]) or "0"
            reject = sum(j["request_id"]==case and j["path"]==arm and j["joint_adjudication"]=="rejected"
                         for j in displayed_judgments)
            path_link = pinned(RANK_SEAL,"ranks.csv",positions[rank_id],f"{arm} · {rank_id}~3")
            joint = f"충족 0 · 반박 {reject} · 기권 {3-reject}" if arm!="P" else "보조 순위만"
            adopt = f"오채택 0 · 근접 {near}" if arm!="P" else f"채택 미적용 · 근접 {near}"
            first_rows.append([case,c["language"],requirement,path_link," / ".join(slots),
                               " / ".join(str(row["denominator"][l]) for l in LABELS),
                               " / ".join(ratios),joint,adopt])
    tables.append("## 표 1. 고정판 상위 3과 공동근거\n\n"
                  +mdtable(["요구ID","언어","필수조건과 환경","경로·원행","상위 3 작품",
                            "D/P/R 분모","D/P/R 회수와 첫 순위","공동근거","오채택과 근접 오답"],first_rows))
    second_rows = []
    how = {"offline":"고정 1","cold":"라이브 빈 캐시","repeat":"라이브 반복"}
    for number,row in enumerate(fetch,1):
        if row["phase"] not in how:
            continue
        # The original publisher's GitHub blob is reachable at this exact pin.
        pos = row["origin_lines"]
        suffix = f"?plain=1#L{pos[0]}" if pos else ""
        src = work[row["work_id"]]["source_url"]+suffix
        edition = work[row["work_id"]]["pin"][:9]
        reason = row["selection_reason"]
        status = str(row["http_status"]) if row["http_status"] is not None else "—"
        if row["error"]:
            status += " · " + row["error"]
        changed = " → ".join("/".join(row[key]) for key in ("top3_before","top3_after"))
        if row["top3_before"] == row["top3_after"]:
            changed = "변동 0"
        second_rows.append([row["request_id"],row["path"],
                            pinned(REPLAY_SEAL,"fetches.jsonl",number,f"{row['attempt']} · {row['fetch_id']}"),
                            reason,f"[{row['work_id']}@{edition}]({src})",status,
                            how[row["phase"]]+" · "+row["transport"],
                            f"{row['section'] or '—'} · {row['display_words']}단어",changed])
    tables.append("## 표 2. 본문 시도와 순위 변화\n\n"
                  +mdtable(["요구ID","경로","시도·원행","선정 이유","URL/판","HTTP/오류",
                            "관측층·운반","표시 절","바뀐 판단"],second_rows))
    third_rows=[]
    profiles={}
    for arm in ARMS:
        build = cost["setup",arm,""]
        first = [cost["cold",arm,c] for c in requests]
        repeat = [cost["repeat",arm,c] for c in requests]
        build_no=next(i for i,r in enumerate(execution,2) if r is build)
        for phase,rows in [("cold",first),("repeat",repeat)]:
            fields=("http_requests","http_body_bytes","displayed_words")
            means={k:statistics.mean(int(r[k]) for r in rows) for k in fields}
            cold_means={k:statistics.mean(int(r[k]) for r in first) for k in fields}
            builds={k:int(build[k] or 0) for k in fields}
            # Build display unmeasured. Show request-only display sums instead.
            series={}
            for n in (1,10,100):
                series[n] = {k:builds[k]+n*means[k] if phase=="cold" else
                             builds[k]+cold_means[k]+(n-1)*means[k] for k in fields}
            times=[int(r["elapsed_ns"])/1e6 for r in rows]
            outcomes=dict(http_requests=sum(int(r["http_requests"]) for r in rows),
                          logical_opens=sum(int(r["logical_opens"]) for r in rows),
                          failures=sum(int(r["failures"]) for r in rows),
                          retries=sum(int(r["retries"]) for r in rows),
                          cache_hits=sum(int(r["cache_hits"]) for r in rows),
                          shown_words=sum(int(r["displayed_words"]) for r in rows),
                          local_bytes=sum(int(r["local_body_bytes"]) for r in rows),
                          machine_card_rows=sum(int(r["scanned_card_rows"]) for r in rows),
                          machine_body_words=sum(int(r["scanned_body_words"]) for r in rows))
            profiles[f"{phase}:{arm}"] = dict(per_request_mean=means, totals_for_6=outcomes, extrapolation=series,
                                             elapsed_ms=dict(min=min(times),median=statistics.median(times),max=max(times)))
            s = [f"{series[n]['http_requests']:,.2f} / {series[n]['http_body_bytes']:,.0f} / {series[n]['displayed_words']:,.0f}"
                 for n in (1,10,100)]
            setup = f"{build['http_requests']} GET · {int(build['http_body_bytes']):,} B · 캡처벽시계 {int(build['acquisition_wall_ns'])/1e9:.3f}s"
            human = build["card_interval_seconds"]
            if human:
                setup += f" · 카드 집중 구간 {human}s"
            local = int(build["elapsed_ns"])/1e6
            setup += f" · 색인 적재 {local:.2f}ms"
            body = (f"{means['http_requests']:.2f} GET · {means['http_body_bytes']:,.0f} B · "
                    f"{means['displayed_words']:,.1f} 단어 · "
                    f"중앙 {statistics.median(times):.2f}ms ({min(times):.2f}–{max(times):.2f})")
            build_source=pinned(REPLAY_SEAL,"costs.csv",build_no,f"{arm} {phase} · setup:{arm}")
            sample_no=next(i for i,r in enumerate(execution,2) if r is rows[0])
            build_source += " · " + pinned(REPLAY_SEAL,"costs.csv",sample_no,f"{phase}:{arm}:{rows[0]['request_id']}")
            third_rows.append([build_source,setup,body,f"{int(build['persistent_bytes']):,} B",*s,
                               "같은 6건 평균" if phase=="cold" else "첫 cold + 나머지 repeat 평균",
                               "활동시간 · 인프라 바이트 · 구축 표시량"])
    figures["cost_profiles"] = profiles
    tables.append("## 표 3. 운영 상태별 실측과 N회 요청 비용\n\n"
                  +mdtable(["경로·구축 원행","구축비","요청비 평균·시간 범위","저장량",
                            "N=1 GET/B/표시 단어","N=10 GET/B/표시 단어","N=100 GET/B/표시 단어",
                            "가정","미측정"],third_rows))
    return figures, "\n\n".join(tables)+"\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tables", type=Path)
    parser.add_argument("metrics", type=Path)
    args = parser.parse_args()
    metrics, markdown = summarize()
    args.tables.write_text(markdown)
    args.metrics.write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+"\n")


if __name__ == "__main__":
    main()
