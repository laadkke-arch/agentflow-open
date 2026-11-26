"""07-review.md 6절 설계 결정 가운데 안이 갈리는 것을 시뮬레이션으로 비교한다.

  D2  활성 답: 어느 답에 알림을 보내나(all / latest / shown_latest)
  D3  중간 개정: 한 폴링 주기 안의 개정 여럿(합쳐 최신만 / 판마다 작업 / 합친 작업이 판마다 읽기)
  D4  기한 읽기 시각: T-24h·T에 무엇을 더하나(게시 시각이 다른 세계 다섯)
  D8  불변 판의 재확인: 168시간 직접 확인을 고정판에도 하나(그대로 / 면제 / 30일)
  D11 예산 배분: 한 묶음 예산인가 시계별 예산인가(폴링 우선 / 요청 우선 / 시계별, 폴링은 조건부 요청)

엔진은 ../db의 것을 그대로 쓰고, 안마다 엔진의 설정 값(DEADLINE_READS, ACTIVE_RULE, IMMUTABLE_KINDS 등)만 바꾼다.
세계 모형은 가정이다. 고른 안과 고른 규칙은 out/decide.json의 "chosen"과 "rule"에 있다.

실행: python3 -I decide_sim.py   (out/decide.json, 같은 엔진·같은 Python이면 바이트까지 같다)
"""
from __future__ import annotations

import json
import random
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ops_sim as base  # noqa: E402

base.load(base.DB)
eng, cases = base.eng, base.cases
plus, hours = base.plus, base.hours


def with_attrs(**kw):
    """엔진 클래스 설정을 잠시 바꾼다."""
    class Ctx:
        def __enter__(self):
            self.old = {k: getattr(eng.Ledger, k) for k in kw}
            for k, v in kw.items():
                setattr(eng.Ledger, k, v)

        def __exit__(self, *a):
            for k, v in self.old.items():
                setattr(eng.Ledger, k, v)
    return Ctx()


# ============================================================================ D4 기한 읽기 시각
D4_OPTIONS = {
    "A 기한 전날·기한(v1)": (("T-24h", -24), ("T", 0)),
    "B A+기한 6시간 뒤": (("T-24h", -24), ("T", 0), ("T+6h", 6)),
    "C A+기한 24시간 뒤": (("T-24h", -24), ("T", 0), ("T+24h", 24)),
    "D A+6시간 뒤+24시간 뒤": (("T-24h", -24), ("T", 0), ("T+6h", 6), ("T+24h", 24)),
    "E 기한·기한 24시간 뒤(전날 뺌)": (("T", 0), ("T+24h", 24)),
    "F 기한 시계 없음": None,
}
D4_WORLDS = {"30시간 일찍 게시": -30, "효력일 0시 게시(사례)": 0, "6시": 6, "14시": 14, "23시": 23}


def d4() -> dict:
    deadline_days = set(base.DEADLINE_OF.values())
    revs = [(ext, eff) for ext, eff, _r, _e in base.kb_revs()]
    dl_revs = [ext for ext, eff in revs if eff in deadline_days]       # 앞 판의 기한 날에 올라오는 개정
    phases = list(range(0, 72, 6))
    table = {}
    for name, reads in D4_OPTIONS.items():
        row = {}
        for wname, off in D4_WORLDS.items():
            base.PUB_OFF[0] = off
            runs = []
            for ph in phases:
                if reads is None:
                    runs.append(base.run_x1_clock(ph, deadlines=False))
                else:
                    with with_attrs(DEADLINE_READS=reads):
                        runs.append(base.run_x1_clock(ph, deadlines=True))
            base.PUB_OFF[0] = 0
            lags, never = [], 0
            for r in runs:
                for ext in dl_revs:
                    v = r["revisions"][ext]["lag_h"]
                    if v is None:
                        never += 1
                    else:
                        lags.append(round(v - off, 1))      # 게시 시각부터 잰 지연
            row[wname] = {"jobs_mean": round(sum(r["jobs_total"] for r in runs) / len(runs), 2),
                          "reads_mean": round(sum(r["reads"] for r in runs) / len(runs), 2),
                          "deadline_rev_never_observed": never,
                          "deadline_rev_lag_max_h": max(lags) if lags else None,
                          "deadline_rev_lag_mean_h": round(sum(lags) / len(lags), 1) if lags else None}
        table[name] = row

    def score(name):
        r = table[name].values()
        worst = max((x["deadline_rev_lag_max_h"] if x["deadline_rev_lag_max_h"] is not None else 1e9) for x in r)
        return (sum(x["deadline_rev_never_observed"] for x in r), 0 if worst <= 24 else 1,
                round(sum(x["reads_mean"] for x in r), 2), worst)
    ranking = sorted(table, key=score)
    return {"options": {k: [list(t) for t in v] if v else None for k, v in D4_OPTIONS.items()},
            "worlds_post_offset_h": D4_WORLDS, "deadline_day_revisions": dl_revs, "phases": len(phases),
            "table": table, "score(never, worst_lag_over_24h, reads, worst_lag)": {k: score(k) for k in table},
            "rule": "놓친 기한 개정이 가장 적고, 다섯 세계 모두에서 최대 지연이 24시간 이하인 안 가운데 읽기 수(세계 합)가 가장 적은 안",
            "chosen": ranking[0]}


# ============================================================================ D3 중간 개정
def d3() -> dict:
    rnd = random.Random(33)
    docs = []
    for d in range(20):
        t = "2026-01-01T00:00:00Z"
        rv = [(f"d{d}r0", t)]
        while True:
            t = plus(t, max(1, round(rnd.expovariate(1 / 48))))   # 같은 시각의 두 개정은 순서를 정할 수 없어 1시간 이상 띄운다
            if t > "2026-03-31T00:00:00Z":
                break
            rv.append((f"d{d}r{len(rv)}", t))
        docs.append(rv)

    def run(option):
        class L2(eng.Ledger):
            def _enqueue(self, obs_id, cause, cause_ref, at):
                if option != "B 항목마다 작업" or cause != "channel":
                    return super()._enqueue(obs_id, cause, cause_ref, at)
                cur = self.db.execute("INSERT OR IGNORE INTO recheck_job(obs_id, cause, cause_ref, enqueued_at)"
                                      " VALUES (?,?,?,?)", (obs_id, cause, cause_ref, at))
                return cur.rowcount == 1
        L = L2()
        stats = Counter()
        chain_ok = 0
        total_edges = 0
        for di, rv in enumerate(docs):
            doc, hist = f"https://docs.example/d{di}", f"https://docs.example/d{di}/history"
            text = {rid: f"{rid} 내용" for rid, _ in rv}
            pub = dict(rv)
            o, _ = L.observe(url=doc, edition_key=f"rev:{rv[0][0]}", edition_kind="revision", position="§", at=rv[0][1],
                             method="read_line", quote=text[rv[0][0]], quote_lang="ko", statement=text[rv[0][0]],
                             published_at=rv[0][1])
            L.channel("ex", hist, "revision_history", period_h=72)
            L.poll(hist, [{"id": rv[0][0], "title": rv[0][0], "url": doc, "edition": f"rev:{rv[0][0]}"}], rv[0][1])
            L.watch(o, hist)
            phase = rnd.randrange(72)
            t = plus(rv[0][1], phase)
            while t <= "2026-04-03T00:00:00Z":
                listing = [{"id": rid, "title": rid, "url": doc, "edition": f"rev:{rid}"} for rid, p_ in rv if p_ <= t]
                L.poll(hist, list(reversed(listing)), t)
                jobs = L.jobs()
                if option == "B 항목마다 작업":     # 공정하게: 항목 작업을 발행 순으로 처리한다
                    jobs = sorted(jobs, key=lambda j: pub[j["cause_ref"].rsplit("#", 1)[1]])
                for j in jobs:
                    tok = L.lease(j["job_id"], plus(t, 1))
                    stats["jobs"] += 1
                    if option == "C 합친 작업이 판마다 읽기":
                        eds = sorted({e["edition_key"][4:] for e in L.job_editions(j["job_id"])}, key=lambda r: pub[r])
                    elif option == "B 항목마다 작업":
                        eds = [j["cause_ref"].rsplit("#", 1)[1]]
                    else:
                        eds = [[rid for rid, p_ in rv if p_ <= t][-1]]
                    new = None
                    for rid in eds:
                        stats["reads"] += 1
                        new, created = L.observe(url=doc, edition_key=f"rev:{rid}", edition_kind="revision", position="§",
                                                 at=t, method="read_line", quote=text[rid], quote_lang="ko",
                                                 statement=text[rid], published_at=pub[rid], via="channel")
                        cur = L.current(j["obs_id"], t)
                        if created and cur != new:
                            # 발행 시각이 현재 관측보다 늦을 때만 잇는다(늦게 온 옛 판은 사슬에 넣지 않는다)
                            if (L.obs(new)["published_at"] or "") > (L.obs(cur)["published_at"] or ""):
                                L.supersede(cur, new, "changes_value", t, pub[rid])
                    L.finish(j["job_id"], new, token=tok)
                t = plus(t, 72)
            seen = {r[0][4:] for r in L.db.execute(
                "SELECT e.edition_key FROM observation o JOIN edition e USING(edition_id) JOIN locator l"
                " USING(locator_id) WHERE l.url=?", (doc,))}
            stats["revisions"] += len(rv)
            stats["observed"] += len(seen)
            # 대체 사슬이 발행 순서를 지키나
            ids = {r[1][4:]: r[0] for r in L.db.execute(
                "SELECT o.obs_id, e.edition_key FROM observation o JOIN edition e USING(edition_id) JOIN locator l"
                " USING(locator_id) WHERE l.url=?", (doc,))}
            order = [rid for rid, _ in rv if rid in ids]
            for a, b in zip(order, order[1:]):
                total_edges += 1
                if L.db.execute("SELECT 1 FROM supersession WHERE old_obs=? AND new_obs=?", (ids[a], ids[b])).fetchone():
                    chain_ok += 1
        L.db.close()
        return {"revisions": stats["revisions"], "observed": stats["observed"],
                "observed_share": round(stats["observed"] / stats["revisions"], 3), "jobs": stats["jobs"],
                "reads": stats["reads"], "chain_in_publication_order": f"{chain_ok}/{total_edges}"}

    options = ["A 합쳐 최신만(v1)", "B 항목마다 작업", "C 합친 작업이 판마다 읽기"]
    table = {o: run(o) for o in options}
    ranking = sorted(options, key=lambda o: (-table[o]["observed_share"], table[o]["jobs"], table[o]["reads"]))
    return {"world": "문서 20개, 개정 간격 지수분포 평균 48시간, 2026-01~03, 72시간 폴링(문서마다 위상 무작위), 개정 이력에서 지난 판을 열 수 있음",
            "table": table, "rule": "관측한 개정 비율이 높고, 그다음 작업 수, 그다음 읽기 수가 적은 안",
            "chosen": ranking[0]}


# ============================================================================ D2 활성 답
def d2() -> dict:
    rnd = random.Random(22)
    plan = []
    for k in range(40):
        revs = rnd.choice([1, 1, 2, 2, 3])
        plan.append([(r, rnd.random() < 0.7) for r in range(1, revs + 1)])   # (요청판, 노출 여부)

    def run(rule):
        with with_attrs(ACTIVE_RULE=rule):
            L = eng.Ledger()
            o, _ = L.observe(url="https://example.org/doc", edition_key="v1", edition_kind="release", position="§1",
                             at="2026-11-01T00:00:00Z", method="read_line", quote="Export is supported.", quote_lang="en",
                             statement="내보내기를 지원한다.")
            projects = [L.project(f"P{i}") for i in range(4)]
            acted = {}      # (프로젝트, 요청 키) → 사용자가 따르는 답(가장 늦게 노출된 답)
            t0 = "2026-11-02T00:00:00Z"
            for k, revs in enumerate(plan):
                p = projects[k % 4]
                for rev, shown in revs:
                    at = plus(t0, k * 3 + rev)
                    req = L.intake(p, request_key=f"K{k}", rev=rev, at=at, text=f"요청 {k}판{rev}", selected_part="s",
                                   requirements=[], prior={"state": "none"})
                    run_id = L.compose(p, req, at, slots=[{"kind": "direct", "first": o, "ladder": "L2", "verb": "v",
                                                          "where": "§1", "reason": "r", "hold": "h"}])
                    if shown:
                        L.show(p, run_id, 1, at)
                        acted[(p, k)] = (p, run_id)     # run_id는 프로젝트 장부마다 따로 센다
            o2, _ = L.observe(url="https://example.org/doc", edition_key="v2", edition_kind="release", position="§1",
                              at="2026-12-01T00:00:00Z", method="read_line", quote="Export removed.", quote_lang="en",
                              statement="내보내기를 없앴다.")
            L.supersede(o, o2, "invalidates", "2026-12-01T00:00:00Z")
            delivered, held, hit, noise = 0, 0, 0, 0
            got = set()
            for p in projects:
                L.propagate(p, "2026-12-02T00:00:00Z")
                for n in L.db.execute(f"SELECT run_id, held FROM {p}.notice").fetchall():
                    if n["held"]:
                        held += 1
                        continue
                    delivered += 1
                    if (p, n["run_id"]) in acted.values():
                        hit += 1
                        got.add((p, n["run_id"]))
                    else:
                        noise += 1
            L.db.close()
        return {"notices": delivered + held, "delivered": delivered, "held": held,
                "delivered_to_followed_answer": hit, "delivered_to_unfollowed_answer": noise,
                "followed_answers_missed": len(set(acted.values()) - got), "followed_answers": len(acted)}

    rules = ["all", "latest", "shown_latest"]
    table = {r: run(r) for r in rules}
    ranking = sorted(rules, key=lambda r: (table[r]["followed_answers_missed"], table[r]["delivered_to_unfollowed_answer"]))
    return {"world": "요청 키 40개(요청판 1~3), 프로젝트 4개, 답마다 70% 확률로 노출. 사용자는 가장 늦게 노출된 답을 따른다[가정]. 인용 관측 하나가 무효가 된다",
            "table": table, "rule": "사용자가 따르는 답을 놓친 수가 가장 적고, 그다음 따르지 않는 답에 간 알림이 적은 안",
            "chosen": ranking[0]}


# ============================================================================ D8 불변 판의 재확인
def d8() -> dict:
    rnd = random.Random(8)
    weeks = 26
    start = "2026-06-01T00:00:00Z"
    end = plus(start, weeks * 168)
    n_pinned, n_mut = 30, 10
    reqs = sorted(round(rnd.uniform(0, weeks * 168)) for _ in range(10 * weeks))
    req_obs = [rnd.randrange(n_pinned + n_mut) for _ in reqs]
    yanks = {i: round(rnd.uniform(500, weeks * 168 - 200)) for i in rnd.sample(range(n_pinned), 3)}
    hidden = {}   # 바뀌는 판의 내용 변화(채널이 놓칠 수 있음)
    for i in range(n_pinned, n_pinned + n_mut):
        hidden[i] = sorted(round(rnd.uniform(0, weeks * 168)) for _ in range(rnd.randint(1, 3)))
    announced = {i: [rnd.random() < 0.8 for _ in hidden[i]] for i in hidden}   # 채널 재현율 0.8[가정]

    def run(kinds, recheck_h):
        with with_attrs(IMMUTABLE_KINDS=kinds, IMMUTABLE_RECHECK_H=recheck_h):
            L = eng.Ledger()
            ch = "https://example.org/changes"
            L.channel("ex", ch, "changelog", period_h=72)
            obs, version = [], {}
            for i in range(n_pinned + n_mut):
                kind = "release" if i < n_pinned else "revision"
                o, _ = L.observe(url=f"https://example.org/{i}", edition_key="v1", edition_kind=kind, position="§",
                                 at=start, method="read_line", quote=f"q{i}-0", quote_lang="en", statement=f"s{i}-0")
                L.watch(o, ch, f"[obj{i}]")
                obs.append(o)
                version[i] = 0
            L.poll(ch, [], start)
            items = []
            events = []   # (시각, 종류, i, k)
            for i, h in yanks.items():
                events.append((h, "yank", i, 0))
            for i, hs in hidden.items():
                for k, h in enumerate(hs):
                    events.append((h, "change", i, k))
            events.sort()
            truth_change = {i: [] for i in range(n_pinned + n_mut)}
            stats = Counter()
            ei = 0
            for h in range(0, weeks * 168 + 1):
                t = plus(start, h)
                while ei < len(events) and events[ei][0] <= h:
                    _h, kind_, i, k = events[ei]
                    truth_change[i].append(h)
                    if kind_ == "yank" or announced[i][k]:
                        items.append({"id": f"{kind_}-{i}-{k}", "title": f"[obj{i}] {kind_}"})
                    ei += 1
                if h % 72 == 0:
                    L.poll(ch, list(items), t)
                for j in L.jobs():
                    tok = L.lease(j["job_id"], plus(t, 1))
                    i = obs.index(L.ancestors(j["obs_id"])[-1]) if L.ancestors(j["obs_id"])[-1] in obs else None
                    if i is None:
                        L.finish(j["job_id"], None, token=tok)
                        continue
                    stats["follow_reads"] += 1
                    n_changes = len([x for x in truth_change[i] if x <= h])
                    if n_changes and n_changes > version[i]:
                        version[i] = n_changes
                        new, _ = L.observe(url=f"https://example.org/{i}", edition_key=f"v1+{n_changes}" if i >= n_pinned else "v1",
                                           edition_kind="release" if i < n_pinned else "revision", position="§", at=t,
                                           method="read_line", quote=f"q{i}-{n_changes}", quote_lang="en",
                                           statement=f"s{i}-{n_changes}" + (" 철회됨" if i < n_pinned else ""), via="channel")
                        L.finish(j["job_id"], new, token=tok,
                                 supersede=(L.current(j["obs_id"], t), "invalidates", t, None))
                    else:
                        L.finish(j["job_id"], None, token=tok)
                # 요청
                for idx in [x for x, rh in enumerate(reqs) if rh == h]:
                    i = req_obs[idx]
                    cur = L.current(obs[i], t)
                    g = L.reuse_gate(cur, t)
                    known_changes = version[i]
                    true_changes = len([x for x in truth_change[i] if x <= h])
                    if g["decision"] == "reuse":
                        stats["reuse"] += 1
                        if true_changes > known_changes:
                            stats["stale_answers"] += 1
                    else:
                        stats["request_rereads"] += 1
                        # 다시 읽으면 내용 변화는 보이지만, 고정판의 철회는 원문 내용에 나타나지 않는다
                        if i >= n_pinned and true_changes > known_changes:
                            version[i] = true_changes
                            new, _ = L.observe(url=f"https://example.org/{i}", edition_key=f"v1+{true_changes}",
                                               edition_kind="revision", position="§", at=t, method="read_line",
                                               quote=f"q{i}-{true_changes}", quote_lang="en", statement=f"s{i}-{true_changes}")
                            L.supersede(cur, new, "changes_value", t)
                        else:
                            L.observe(url=L.obs(cur)["url"], edition_key=L.obs(cur)["edition_key"],
                                      edition_kind=L.obs(cur)["edition_kind"], position="§", at=t, method="read_line",
                                      quote=L.obs(cur)["quote"], quote_lang="en", statement=L.obs(cur)["statement"])
                            if true_changes > known_changes:
                                stats["stale_answers"] += 1
            L.db.close()
        n = len(reqs)
        return {"requests": n, "request_rereads": stats["request_rereads"], "reuse": stats["reuse"],
                "follow_reads": stats["follow_reads"], "stale_answers": stats["stale_answers"],
                "stale_rate": round(stats["stale_answers"] / n, 3)}

    pinned = ("release", "commit", "tag", "doi")
    options = {"A 모든 판 168시간(v1)": ((), None), "B 고정판은 면제": (pinned, None), "C 고정판은 30일": (pinned, 720)}
    table = {k: run(*v) for k, v in options.items()}
    ranking = sorted(table, key=lambda k: (table[k]["stale_answers"], table[k]["request_rereads"]))
    return {"world": f"{weeks}주, 고정판 관측 {n_pinned}개(그중 3개 철회, 철회는 채널이 늘 알림), 바뀌는 판 관측 {n_mut}개"
                     "(내용 변화 1~3회, 채널 재현율 0.8[가정]), 주간 요청 10건, 72시간 폴링",
            "table": table, "rule": "낡은 답 수가 가장 적고, 그다음 요청 시계 재열람이 적은 안", "chosen": ranking[0]}


# ============================================================================ D11 예산 배분
def d11() -> dict:
    policies = base.BUDGET_POLICIES
    run = base.budget_model
    grid = {pol: {f"C{C}_req{lam}": run(pol, C, lam) for C in (3, 10, 30) for lam in (5, 20)} for pol in policies}

    def bad(pol):
        g = grid[pol].values()
        return (sum(1 for x in g if x["deferred_rate"] > 0.05 or x["exhausted_rate"] > 0),
                sum(1 for x in g if x["follow_hours_deferred"] > 0),
                max(x["max_cursor_age_h"] for x in g))
    ranking = sorted(policies, key=bad)
    return {"world": "M3와 같은 출처·요청 모형, 12주. 출처 절반은 72시간·절반은 168시간 주기, 폴링마다 5% 확률로 변화(후속 읽기 1회). "
                     "한 묶음 예산은 168시간당 24회. 시계별은 요청당 4회, 후속 168시간당 3회, 배경 폴링은 조건부 요청이라 읽기 예산 밖[가정, 07 R-2]",
            "grid": grid, "rule": "보류율 5% 초과나 예산 소진이 난 설정 수가 가장 적고, 그다음 후속 읽기가 밀린 설정 수, 그다음 커서 최고령이 낮은 안",
            "bad_configs": {p: bad(p) for p in policies}, "chosen": ranking[0]}


SCENARIOS = [("D2", d2), ("D3", d3), ("D4", d4), ("D8", d8), ("D11", d11)]


def main():
    out = {"engine": "docs/design/final/db", "note": "세계 모형은 가정이다. 결과는 안 사이의 비교에만 쓴다. 07-review.md 6절",
           "results": {}}
    for key, fn in SCENARIOS:
        r = fn()
        out["results"][key] = r
        print(f"{key:4} 고른 안: {r['chosen']}")
    (HERE / "out").mkdir(exist_ok=True)
    (HERE / "out" / "decide.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
