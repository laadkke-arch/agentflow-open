"""R1 한 요청을 실제 검색·실제 원문·실제 실행으로 끝까지 돌린다(06 3절 첫 구현 단위, 완료 기준 2~5).

  python3 -I ledger/run_r1.py --live     네트워크·해석기로 돌리고 응답을 fixtures에 기록, ledger/out/r1_live.json을 쓴다
  python3 -I ledger/run_r1.py            기록 재생(네트워크 없음). 시험이 이 길을 쓴다

판정·관문·자리 문장은 사람이 쓴 계획(fixtures/r1/plan.json)이다. 숫자는 실제 실행 영수증에서, 줄 범위·인용은
실제 원문에서, 후보 파일은 실제 검색에서 온다. 계획이 읽으라는 파일이 탐색 기록에 없으면 읽지 않는다.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from afledger import Ledger, PrivacyError, config, locate  # noqa: E402
from afledger.adapters.http import Transport  # noqa: E402
from afledger.adapters.reader_github import GitHubPinnedReader, SourceUnavailable  # noqa: E402
from afledger.adapters.runner import ReceiptRunner, record_receipt  # noqa: E402
from afledger.adapters.search_github import direct_branch, log_fresh, resolve_drawer_symbols  # noqa: E402
from afledger.budget import REASON as BUDGET_REASON, BudgetExhausted, RequestBudget  # noqa: E402
from afledger.intake import intake  # noqa: E402
from afledger.ledger import content_tokens  # noqa: E402
from drawer_load import preload_catalog, preload_noise  # noqa: E402

FIX = HERE / "fixtures"
REPO = "python/cpython"
PY_CHANGELOG = "https://docs.python.org/3/whatsnew/changelog.html"
# cases.py의 손 대응(3.13.18 → 3.12.3). 설계 예제 위치 표기(엔대시)를 그대로 둔다
HAND_MAP = {"q1": ("L36–38", "L24–26"), "q2": ("L252–258", "not_found"), "s1": ("L355–358", "L333–336")}


def load(name):
    return json.loads((FIX / "r1" / name).read_text(encoding="utf-8"))


class Fmt:
    """계획 문장의 {A.max_waiting}, {in.maxsize}, {tag}, {q1.position}, {gate.failed} 자리를 채운다."""
    def __init__(self):
        self.v: dict[str, object] = {}

    def __call__(self, s):
        if not isinstance(s, str):
            return s
        return re.sub(r"\{([A-Za-z0-9_]+)(?:\.([A-Za-z0-9_]+))?\}",
                      lambda m: str(self.v[m.group(1)] if m.group(2) is None else self.v[m.group(1)][m.group(2)]), s)


def run(mode: str = "replay", needs: str = "studio", noise: bool = True) -> dict:
    """needs="i1"이면 Studio의 칸별 필요 문장을 빼고 접수 규칙 i1이 쓰게 한다(A4).
    noise=False면 서랍에 F01 잡음을 넣지 않는다(설계 사례의 서랍: 012 자료집 156항목만)."""
    plan = load("plan.json")
    t = Transport(mode if mode != "live" else "record", FIX / "http")
    runner = ReceiptRunner(mode if mode != "live" else "record", FIX / "exec")
    L = Ledger()
    catalog = preload_catalog(L)
    noise = preload_noise(L, "F01") if noise else {}
    inv = {v: k for k, v in catalog.items()}
    out: dict = {"mode": "live" if mode == "live" else "replay",
                 "rules": {k: getattr(config, k) for k in dir(config) if k.endswith("_RULES") or k == "RULE_VERSION"},
                 "drawer_size": {"catalog": len(catalog), "noise_F01": len(noise)}}

    # =========================================================== 요청판 1 (CPython 3.13)
    p = L.project("A")
    s1 = load("studio_rev1.json")
    if needs == "i1":
        s1.pop("needs")
    t0 = s1["received_at"]
    req1, info = intake(L, p, s1)
    it = plan["interpretation"]
    d = L.decide(it["first_a"], it["first_b"])
    L.interpret(p, req1, it["code"], it["chosen"], it["other"], d, t0)
    f = Fmt()
    f.v["in"] = plan["program"]["input"]

    drawer = L.search_drawer(p, req1, t0, k=12)
    audit = L.search_drawer(p, req1, t0, k=600, min_slots=1, include_function_words=True, log=False)

    # 확인 1: 실행(사용자 판을 정한다. 이 러너가 돌린 판의 태그를 읽는다)
    rec = runner.run(HERE / plan["program"]["path"], plan["program"]["input"], "3.13")
    rid = record_receipt(L, p, req1, rec, t0)
    tag = "v" + rec["runtime_ran"].split()[-1]
    f.v["tag"] = tag
    res = {r["pattern"].split()[0]: r for r in rec["output"]["results"]}
    f.v.update(res)

    # 찾기: 새 검색 직접 갈래(실제), 나머지 세 갈래는 빈 목록
    budget1 = RequestBudget(L, p, req1)
    direct = direct_branch(L, t, p, req1, t0, context=L.context(p, req1), request_text=s1["text"],
                           selected_part=s1["selected_part"]["label"], content_tokens=content_tokens, budget=budget1)
    log_fresh(L, p, req1, t0, direct)
    symbols = resolve_drawer_symbols(L, t, p, req1, t0, scope=direct["scope"], drawer_hits=drawer, budget=budget1)
    searched_paths = {r["path"] for r in direct["results"]} | {x["path"] for s_ in symbols for x in s_["results"]}

    # 확인 2: 사용자 판의 원문 줄
    reader = GitHubPinnedReader(L, t, p, req1)
    obs, readings, unread = {}, {}, []
    for rd in plan["readings"]:
        if rd["path"] not in searched_paths:
            unread.append({"id": rd["id"], "path": rd["path"], "reason": "탐색 기록에 없음"})
            continue
        try:
            r = reader.read(REPO, tag, rd["path"], t0, symbol=rd["symbol"], start=rd["start"], end=rd["end"])
        except BudgetExhausted:
            unread.append({"id": rd["id"], "path": rd["path"], "reason": BUDGET_REASON})
            continue
        except SourceUnavailable as e:
            unread.append({"id": rd["id"], "path": rd["path"], "reason": e.outcome})
            continue
        if not r["found"]:
            unread.append({"id": rd["id"], "path": rd["path"], "reason": "계획한 구절을 이 판에서 찾지 못함"})
            continue
        oid, _ = L.observe(url=r["url"], edition_key=tag, edition_kind="release", position=r["position"], at=t0,
                           method="read_line", quote=r["quote"], quote_lang="en", statement=rd["statement"],
                           flip_position=f"{r['position']} {rd.get('flip', '')}".strip(), reader=r["reader"],
                           project=p, anchor_symbol=r["symbol"], anchor_in_doc=r["in_doc"], map_method="direct",
                           byte_span=r["byte_span"])
        obs[rd["id"]] = oid
        readings[rd["id"]] = r
        f.v[rd["id"]] = {"position": r["position"], "link": r["link"]}

    # 실행 관측(값 문장은 프로젝트 장부, 07 D6c)
    for rr in plan["runs"]:
        url = f"https://github.com/{REPO}/blob/{tag}/{rr['path']}"
        oid, _ = L.observe_run(p, url=url, edition_key=tag, edition_kind="release",
                               position=f"run:r1_queue.py {rr['pattern']}", at=t0, receipt_id=rid,
                               statement=f(rr["statement"]), reader=rec["runner"])
        obs[rr["id"]] = oid
    for a, b, cond, lv, rv in plan["contrasts"]:
        L.contrast(obs[a], obs[b], cond, f(lv), f(rv), rid, p=p)
    for oid_ref, slot, height, lang, text in plan["tags"]:
        if oid_ref in obs:
            L.tag(obs[oid_ref], slot, height, lang, text)

    gp = plan["gate"]
    g = L.gate(role_map=[tuple(x) for x in gp["role_map"]], invariant_quote=gp["invariant_quote"],
               break_input=gp["break_input"], baseline_prediction=gp["baseline_prediction"],
               principle_prediction=gp["principle_prediction"], target_doc_states_it=gp["target_doc_states_it"])
    f.v["gate"] = {"failed": "; ".join(g["failed"])}

    def ref(x):
        return catalog[x[4:]] if x.startswith("cat:") else obs.get(x)

    prem = plan["premises"]
    for code, o, v, role, lad, reason, pr in plan["judgments_rev1"]:
        if ref(o):
            L.judge(p, req1, code, ref(o), v, role, lad, f(reason), t0, premises=prem.get(pr, pr) if isinstance(pr, str) else pr)

    searched_urls = {r[0] for r in L.db.execute(
        f"SELECT h.url FROM {p}.search_hit h JOIN {p}.search_run r USING(search_id) WHERE r.req_id=?", (req1,))}

    def folded_list(obs_map, fmt, unread_now, tag_now):
        fl, skipped = [], []
        for it_ in plan["folded"]:
            o = obs_map.get(it_["ref"]) if not it_["ref"].startswith("cat:") else catalog[it_["ref"][4:]]
            if o is None:
                skipped.append({"ref": it_["ref"], "why": "관측 없음(읽지 못함)"})
                continue
            if it_["ref"].startswith("cat:") and L.obs(o)["url"] not in searched_urls:
                skipped.append({"ref": it_["ref"], "why": "이 요청의 탐색 기록에 없음(단위 1은 관계·분야·언어 갈래가 비어 있다)"})
                continue
            url = L.link(o) if not it_["ref"].startswith("cat:") else L.obs(o)["url"]
            fl.append({"url": url, "obs": o, "condition": it_["condition"], "reason": fmt(it_["reason"])})
        for u in unread_now:
            fl.append({"url": f"https://github.com/{REPO}/blob/{tag_now}/{u['path']}", "obs": None,
                       "condition": f"읽지 않은 후보 {u['id']}", "reason": u["reason"]})
        return fl, skipped

    folded1, skipped1 = folded_list(obs, f, unread, tag)
    sp = plan["slot_rev1"]
    slot = {k: (f(v) if isinstance(v, str) else v) for k, v in sp.items()}
    slot.update(first=obs.get(sp["first"]), support=[obs[x] for x in sp["support"] if x in obs],
                flip=[obs[x] for x in sp["flip"] if x in obs])
    b1 = budget1.summary() | {"exhausted": any(u["reason"] == BUDGET_REASON for u in unread)}
    status = "complete" if slot["first"] else ("budget_exhausted" if b1["exhausted"] else "none_verified")
    run1 = L.compose(p, req1, t0, slots=[slot] if slot["first"] else [], folded=folded1, readback=plan["readback"],
                     status=status, budget=b1,
                     next_action=None if slot["first"] else "첫 확인 항목: 대기열 절(H1·H2)")
    L.channel("python", PY_CHANGELOG, "changelog")
    for k in ("q1", "q2"):
        if k in obs:
            L.watch(obs[k], PY_CHANGELOG, "asyncio")
    L.show(p, run1, 1, t0)

    out["rev1"] = {
        "received_at": t0, "needs_by": info["needs_by"], "clarify": d, "runtime_tag": tag,
        "execution": {"runtime_wanted": rec["runtime_wanted"], "runtime_ran": rec["runtime_ran"],
                      "note": rec["note"], "program_sha256": rec["program_sha256"]},
        "drawer": [{"rank": h["rank"], "id": inv.get(h["obs_id"]) or f"F01:{noise[h['obs_id']]['record']}"
                    if (h["obs_id"] in inv or h["obs_id"] in noise) else h["obs_id"],
                    "url": L.obs(h["obs_id"])["url"], "slots": h["slots"], "matched": h["matched"],
                    "eligible": h["eligible"], "lexical_accident": h["lexical_accident"]} for h in drawer],
        "drawer_audit_accidents": [{"id": inv.get(h["obs_id"]) or h["obs_id"], "rank": h["rank"], "matched": h["matched"],
                                    "eligible_under_rule": False} for h in audit if h["lexical_accident"]][:20],
        "fresh_direct": {"scope": direct["scope"], "terms": direct["terms"], "calls": direct["calls"],
                         "results": [{k: r[k] for k in ("url", "path", "score", "why")} for r in direct["results"]],
                         "branches_empty": ["relation", "domain_guess", "language"],
                         "drawer_symbols_resolved": symbols},
        "readings": {k: {x: v[x] for x in ("link", "position", "symbol", "in_doc", "quote_fp", "byte_span")}
                     for k, v in readings.items()},
        "unread": unread, "folded_plan_items_skipped": skipped1,
        "gate": g, "budget": b1, "fetch_log": [dict(r) for r in L.db.execute(
            f"SELECT url, edition_key, outcome, bytes FROM {p}.fetch_log WHERE req_id=?", (req1,))],
        "answer": L.replay(p, run1), "path_log": L.path_log(p, req1),
        "exec_notes": {k: L.exec_note(p, obs[k]) for k in ("eA", "eB", "eC", "eD")},
    }

    # =========================================================== 요청판 2 (CPython 3.12)
    s2 = load("studio_rev2.json")
    t1 = s2["received_at"]
    req2, _ = intake(L, p, s2)
    carried = L.carry_slips(p, req1, req2, t1, lambda o, ctx: "python/cpython" not in (o["url"] or "") or
                            Ledger.edition_matches(ctx.get("runtime", ""), o["edition_key"]))
    rec2 = runner.run(HERE / plan["program"]["path"], plan["program"]["input"], "3.12")
    rid2 = record_receipt(L, p, req2, rec2, t1)
    tag2 = "v" + rec2["runtime_ran"].split()[-1]
    f2 = Fmt()
    f2.v.update(f.v)
    f2.v["tag"] = tag2
    f2.v.update({r["pattern"].split()[0]: r for r in rec2["output"]["results"]})
    reader2 = GitHubPinnedReader(L, t, p, req2)
    cited = {u for (u,) in L.db.execute(f"SELECT DISTINCT obs_id FROM {p}.usage WHERE run_id=?", (run1,))} | \
        {o for (o,) in L.db.execute(f"SELECT obs_id FROM {p}.folded WHERE run_id=? AND obs_id IS NOT NULL", (run1,))}
    obs2, maps = dict(obs), {}
    reuse_313_for_312 = L.reusable(readings["q1"]["url"], tag2, readings["q1"]["position"]) if "q1" in readings else None
    for k, o in obs.items():
        if k not in readings or o not in cited:
            continue
        rd = next(x for x in plan["readings"] if x["id"] == k)
        try:
            m = reader2.map_to(o, REPO, tag2, rd["path"], t1)
        except BudgetExhausted:
            maps[k] = {"method": "not_read", "reason": BUDGET_REASON}
            continue
        maps[k] = {"from": readings[k]["position"], "method": m["map"]["method"], "to": m.get("position"),
                   "symbol": m["symbol"], "symbol_present": m["map"]["symbol_present"]}
        if m["found"]:
            oid, _ = L.observe(url=m["url"], edition_key=tag2, edition_kind="release", position=m["position"], at=t1,
                               method="read_line", quote=m["quote"], quote_lang="en", statement=rd["statement"],
                               flip_position=f"{m['position']} {rd.get('flip', '')}".strip(), reader=m["reader"],
                               project=p, anchor_symbol=m["symbol"], anchor_in_doc=m["in_doc"],
                               map_method=m["map"]["method"], map_from=o, byte_span=m["byte_span"])
            f2.v[k] = {"position": m["position"], "link": m["link"]}
        elif m["map"]["symbol_present"] is False:
            # 기호가 새 판의 ast에 없다는 것을 확인했다: 그 판에 없다는 관측(추측이 아니라 ast 확인)
            oid, _ = L.observe(url=m["url"], edition_key=tag2, edition_kind="release", position=m["symbol"], at=t1,
                               method="read_line", outcome="not_found", statement=rd["missing_statement"],
                               reader=m["reader"], project=p, anchor_symbol=m["symbol"], map_method="unmapped",
                               map_from=o)
            f2.v[k] = {"position": m["symbol"], "link": m["url"]}
        else:
            continue
        obs2[k] = oid
    for rr in plan["runs"]:
        url = f"https://github.com/{REPO}/blob/{tag2}/{rr['path']}"
        oid, _ = L.observe_run(p, url=url, edition_key=tag2, edition_kind="release",
                               position=f"run:r1_queue.py {rr['pattern']}", at=t1, receipt_id=rid2,
                               statement=f2(rr["statement"]), reader=rec2["runner"])
        obs2[rr["id"]] = oid
    for code, o, v, role, lad, reason, pr in plan["judgments_rev2"]:
        if o in obs2:
            L.judge(p, req2, code, obs2[o], v, role, lad, f2(reason), t1,
                    premises=prem.get(pr, pr) if isinstance(pr, str) else pr)
    folded2, _ = folded_list(obs2, f2, [], tag2)
    sp2 = dict(plan["slot_rev1"], **plan["slot_rev2"])
    slot2 = {k: (f2(v) if isinstance(v, str) else v) for k, v in sp2.items()}
    slot2.update(first=obs2["q1"], support=[obs2["q2"], obs2["eA"]], flip=[obs2["q1"]])
    b2 = RequestBudget(L, p, req2).summary() | {"exhausted": False}
    run2 = L.compose(p, req2, t1, slots=[slot2], folded=folded2, readback=plan["readback"], budget=b2)
    L.note(p, run1, 1, obs["q2"], obs2["q2"], "changes_value", t1, plan["note_rev2"])
    hand_cmp = []
    for k, (h_from, h_to) in HAND_MAP.items():
        got_from = readings[k]["position"] if k in readings else None
        got_to = maps.get(k, {}).get("to") if maps.get(k, {}).get("method") != "unmapped" else "not_found"
        norm = lambda s: s and s.replace("–", "-L") if s and s.startswith("L") else s  # noqa: E731
        hand_cmp.append({"id": k, "hand_from": h_from, "got_from": got_from, "hand_to": h_to, "got_to": got_to,
                         "method": maps.get(k, {}).get("method"),
                         "from_agrees": norm(h_from) == got_from, "to_agrees": norm(h_to) == got_to})
    out["rev2"] = {
        "received_at": t1, "runtime_tag": tag2,
        "execution": {"runtime_wanted": rec2["runtime_wanted"], "runtime_ran": rec2["runtime_ran"], "note": rec2["note"]},
        "carry": {"kept": len(carried["kept"]), "dropped": len(carried["dropped"]),
                  "dropped_for_edition": sum(1 for x in carried["dropped"] if x.get("edition_mismatch"))},
        "reuse_313_for_312": reuse_313_for_312,
        "position_map": maps, "hand_map_comparison": hand_cmp,
        # 대응 규칙의 어긋남(새 판 위치)과, 첫 판에서 고른 줄 범위의 차이(대응과 무관)를 따로 센다
        "hand_map_mismatches": sum(1 for x in hand_cmp if not x["to_agrees"]),
        "rev1_position_choice_differences": sum(1 for x in hand_cmp if not x["from_agrees"]),
        "budget": b2, "fetch_log": [dict(r) for r in L.db.execute(
            f"SELECT url, edition_key, outcome, bytes FROM {p}.fetch_log WHERE req_id=?", (req2,))],
        "answer": L.replay(p, run2),
        "run1_after": L.replay(p, run1),
        "run1_slots_unchanged": L.replay(p, run1)["slots"] == out["rev1"]["answer"]["slots"],
    }

    # =========================================================== 다른 프로젝트 C (같은 판 3.13)
    pc = L.project("C")
    sc = load("studio_c.json")
    t2 = sc["received_at"]
    reqc, _ = intake(L, pc, sc)
    hc = L.search_drawer(pc, reqc, t2, k=5)
    obs_before = L.counts()["observations"]
    reuse = L.reusable(readings["q1"]["url"], tag, readings["q1"]["position"], project=pc, at=t2)
    gate_c = L.reuse_gate(reuse, t2) if reuse else None
    readerc = GitHubPinnedReader(L, t, pc, reqc)
    recheck = None
    if reuse and gate_c["decision"] == "reopen":
        recheck = readerc.recheck(reuse, t2)
        if recheck.get("same"):
            o = L.obs(reuse)
            L.observe(url=o["url"], edition_key=tag, edition_kind="release", position=o["position"], at=t2,
                      method="read_line", quote=o["quote"], quote_lang="en", statement=o["statement"],
                      flip_position=o["flip_position"], reader=readerc.reader_id, project=pc)
    file_bytes = next((r["bytes"] for r in out["rev1"]["fetch_log"] if r["url"].endswith("queues.py")), None)
    out["project_c"] = {
        "drawer_eligible": [{"url": L.obs(h["obs_id"])["url"], "matched": h["matched"]} for h in hc if h["eligible"]],
        "reused_obs": reuse, "same_as_A_q1": reuse == obs.get("q1"), "gate": gate_c,
        "recheck": {k: v for k, v in (recheck or {}).items() if k != "quote"},
        "new_observations": L.counts()["observations"] - obs_before,
        "fetches": L.fetch_count(p=pc, req=reqc),
        "recheck_bytes": (recheck or {}).get("bytes"), "full_file_bytes": file_bytes,
        "sees_A_slips": L.db.execute(f"SELECT count(*) FROM {pc}.slip").fetchone()[0] + len(L.inherited(pc, reuse or 0)),
    }

    # =========================================================== 공개 꼬리표에 요청 문장 쓰기
    attempts = []
    for a in plan["privacy_attempts"]:
        try:
            L.tag(obs["q1"], "summary", "one_up", a["lang"], a["text"])
            attempts.append({"why": a["why"], "rejected": False})
        except PrivacyError as e:
            attempts.append({"why": a["why"], "rejected": True, "error": str(e)})
    legit = "await put() will block when the queue reaches maxsize"   # 원문 쪽 낱말만
    try:
        L.tag(obs["q1"], "summary", "one_up", "en", legit)
        legit_ok = True
    except PrivacyError:
        legit_ok = False
    out["privacy"] = {"rules": config.PRIVACY_RULES, "attempts": attempts, "source_side_tag_accepted": legit_ok}

    # =========================================================== D6c: 공용 장부에 요청 수치가 없나
    commons_receipts = [dict(r) for r in L.db.execute("SELECT * FROM receipt")]
    commons_contrast = [dict(r) for r in L.db.execute("SELECT * FROM contrast")]
    exec_statements = [r[0] for r in L.db.execute("SELECT statement FROM observation WHERE method='executed'")]
    out["d6c"] = {"commons_receipt_columns": sorted(commons_receipts[0].keys()) if commons_receipts else [],
                  "commons_contrast_columns": sorted(commons_contrast[0].keys()) if commons_contrast else [],
                  "commons_exec_statement_example": exec_statements[0] if exec_statements else None,
                  "project_exec_note_example": out["rev1"]["exec_notes"]["eA"]}
    out["transport"] = {"requests": len(t.log), "replayed": sum(1 for x in t.log if x["replayed"]),
                        "first_fetched_at": min((x["fetched_at"] for x in t.log), default=None),
                        "last_fetched_at": max((x["fetched_at"] for x in t.log), default=None)}
    out["_ledger"] = L
    return out


def main():
    live = "--live" in sys.argv
    r = run("live" if live else "replay")
    r.pop("_ledger")
    r["executed_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    text = json.dumps(r, ensure_ascii=False, indent=1)
    if live:
        (HERE / "out" / "r1_live.json").write_text(text + "\n", encoding="utf-8")
        print("wrote ledger/out/r1_live.json")
    else:
        print(text)


if __name__ == "__main__":
    main()
