"""둘째 구현 단위 착수: EVAL-X1(Pocket)을 기록된 개정 이력과 폴링 시계로 재생한다(06 3.4 단위 2 완료 기준).

  python3 -I ledger/run_unit2.py      위상 12개로 돌려 ledger/out/unit2_x1.json을 쓴다(기록 재생, 네트워크 없음)

완료 기준(06 3.4): (1) 각 개정이 채널에 보인 뒤 폴링 주기 + 24시간 안에 관측된다, (2) 대체 뒤에도 공급자 층 감시가 살아 있다,
(3) Pocket 자리에만 알림, 원리 자리 알림 0. 개정 이력은 연구 원장 AF-RES-152의 기록이다(fixtures/unit2/x1_events.json).
실제 SUMO 페이지를 폴링하지 않았다(이 환경에서 막힘). 판정(효과)과 감시 기한은 원장 판독을 사람이 옮긴 값이다.
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from afledger import Ledger  # noqa: E402
from afledger.clock import PollingClock  # noqa: E402
from afledger.ledger import _shift  # noqa: E402
from afledger.worker import RecheckWorker  # noqa: E402

FIX = HERE / "fixtures" / "unit2"
START, END = "2025-05-15T00:00:00Z", "2025-11-20T00:00:00Z"
PERIOD = 72
POSITION = "When is Pocket shutting down / dates"


def load():
    return json.loads((FIX / "x1_events.json").read_text(encoding="utf-8"))


REASONS = ("감시 없음", "채널 커서가 늙음", "공지 기한", "처리 안 된 재확인 작업", "대체되었거나 철회된 관측", "마지막 직접 확인이")


def reason_key(why: str) -> str:
    return next((k for k in REASONS if why.startswith(k)), why)


def run_phase(phases: dict, d: dict | None = None, *, probe: bool = False, gate=None) -> dict:
    """probe=True면 매일 12:00Z 틱 시작에 재사용 관문을 묻는다(08 I39, 읽기만). gate(L, 관측, 시각)로 관문을 바꿔 시험할 수 있다."""
    d = d or load()
    revs = {r["id"]: r for r in d["revisions"]}
    L = Ledger()
    p = L.project("X")
    t0 = d["request"]["received_at"]
    req = L.intake(p, request_key="X1", rev=1, at=t0, text=d["request"]["text"], selected_part="저장 목록 계층",
                   requirements=[{"code": "R1", "kind": "must", "text": "내보내기"}, {"code": "R2", "kind": "must", "text": "사본"}],
                   prior={"state": "given", "known": []}, needs=d["request"]["needs"])
    L.search_fresh(p, req, t0, {"direct": [{"url": d["pocket_home"], "why": "read later"}],
                                "domain_guess": [{"url": d["oai"], "why": "incremental harvest"}]})
    pocket0, _ = L.observe(url=d["pocket_home"], edition_key="fetch:2025-05-15", edition_kind="fetch", position="검색 결과 항목",
                           at=t0, method="intro_only", statement="검색 결과에서 이름과 주소만 확인했다.", project=p)
    oai, _ = L.observe(url=d["oai"], edition_key="2.0 (doc 2015-01-08)", edition_kind="release", position="§2.5.1", at=t0,
                       method="read_line", quote=d["oai_quote"], quote_lang="en",
                       statement="저장소가 삭제 정보를 기한 없이 보존하는 수준과 보존하지 않는 수준을 구분한다.", project=p)
    slots = [{"kind": "check", "first": pocket0, "ladder": "L0", "hold": "원문 판독 전에는 지지로 내지 않습니다",
              "verb": "Pocket(직접 쓸 도구 후보, 검증 전)", "reason": "내보내기·API 문서를 먼저 확인합니다"},
             {"kind": "principle", "first": oai, "contrast": [pocket0], "ladder": "L2", "verb": "변경분 수확으로 사본을 맞춘다",
              "where": "OAI-PMH 2.0 §2.5.1", "borrow": "증분 수확", "recheck": "변경 이후 목록", "break": "종료 공지 뒤 API 닫힘",
              "hold": "삭제 정보가 없으면 주기적 전체 내보내기"}]
    run0 = L.compose(p, req, t0, slots=slots, status="partial", readback="'언제든 내보내기'를 읽기 API 가져오기로 읽었습니다.",
                     next_action="Pocket 읽기 API 문서를 연다")
    L.show(p, run0, 1, t0)
    L.channel("mozilla", d["supplier_feed"], "feed", period_h=PERIOD)
    L.channel("mozilla", d["kb_history"], "revision_history", period_h=PERIOD)
    L.watch(pocket0, d["supplier_feed"], "Pocket", layer="supplier")

    def supplier_listing(at):
        return [{"id": i["id"], "title": i["title"], "summary": i["summary"], "url": i["url"]}
                for i in d["supplier_items"] if i["first_seen_in_channel"] <= at]

    def kb_listing(at):
        return [{"id": r["id"], "title": f"future-of-pocket revision {r['id']}", "url": d["kb"], "edition": r["edition"]}
                for r in reversed(d["revisions"]) if r["first_seen_in_channel"] <= at]

    def reader(obs, edition_key, at):
        visible = [r for r in d["revisions"] if r["first_seen_in_channel"] <= at]
        r = next((x for x in visible if x["edition"] == edition_key), None) if edition_key else (visible[-1] if visible else None)
        if not r:
            return None
        return {"url": d["kb"], "edition_key": r["edition"], "position": POSITION, "quote": r["reading"], "quote_lang": "ko-reading",
                "statement": r["reading"], "published_at": r["first_seen_in_channel"], "effective_from": r["effective_from"],
                "flip_position": "기한과 가용 범위 문장", "reader": "replay:AF-RES-152", "rev": r["id"],
                "evidence_ref": f"AF-RES-152@ba038a0a {r['ledger_source']}",
                "watch": [{"channel": d["kb_history"], "deadline": r["deadline_stated"]}]}

    def judge(old_obs, r):
        return revs[r["rev"]]["effect"]

    w = RecheckWorker(L, reader, judge)
    probes = []
    gate = gate or (lambda L_, o, at: L_.reuse_gate(o, at))

    def probe_fn(at):
        if not at.endswith("T12:00:00Z"):
            return
        cur = L.current(pocket0, at)
        g = gate(L, cur, at)
        visible = [r for r in d["revisions"] if r["first_seen_in_channel"] <= at]
        behind = bool(visible) and L.obs(cur)["edition_key"] != visible[-1]["edition"]
        g2 = gate(L, oai, at)
        # 뒤처졌을 때 장부가 그 개정 항목을 이미 받았나(받았으면 관문의 구멍, 못 받았으면 폴링 주기 안의 지연)
        known = bool(visible) and bool(L.db.execute(
            "SELECT 1 FROM channel_item i JOIN channel c USING(channel_id) WHERE c.url=? AND i.external_id=?",
            (d["kb_history"], visible[-1]["id"])).fetchone())
        probes.append({"at": at, "obs": cur, "edition": L.obs(cur)["edition_key"], "decision": g["decision"],
                       "why": g["why"], "behind": behind, "item_known": known, "oai_decision": g2["decision"],
                       "oai_why": g2["why"]})

    clock = PollingClock(L, w, {
        d["supplier_feed"]: {"listing": supplier_listing, "period_h": PERIOD, "phase_h": phases["supplier"]},
        d["kb_history"]: {"listing": kb_listing, "period_h": PERIOD, "phase_h": phases["kb"]}}, projects=[p],
        before_tick=probe_fn if probe else None)
    clock.run(START, END)

    # (1) 개정마다 관측 지연
    delays = {}
    for r in d["revisions"]:
        row = L.db.execute("SELECT min(o.observed_at) FROM observation o JOIN edition e USING(edition_id)"
                           " WHERE e.edition_key=?", (r["edition"],)).fetchone()[0]
        delays[r["id"]] = None if row is None else round(
            (__import__("datetime").datetime.strptime(row, "%Y-%m-%dT%H:%M:%SZ")
             - __import__("datetime").datetime.strptime(r["first_seen_in_channel"], "%Y-%m-%dT%H:%M:%SZ")).total_seconds() / 3600, 1)
    # (2) 대체 사슬의 관측마다 공급자 층 감시
    chain = [pocket0]
    while True:
        nxt = L.db.execute("SELECT new_obs FROM supersession WHERE old_obs=?", (chain[-1],)).fetchone()
        if not nxt:
            break
        chain.append(nxt[0])
    supplier_alive = [bool(L.db.execute("SELECT 1 FROM watch w JOIN channel c USING(channel_id) WHERE w.obs_id=?"
                                        " AND w.layer='supplier'", (o,)).fetchone()) for o in chain]
    notices = L.replay(p, run0)["notices"]
    extra = {"probes": probes} if probe else {}
    return extra | {"phases": phases, "delays_h": delays, "max_delay_h": max(v for v in delays.values() if v is not None) if all(
        v is not None for v in delays.values()) else None, "missed": [k for k, v in delays.items() if v is None],
        "chain_editions": [L.obs(o)["edition_key"] for o in chain], "supplier_watch_alive": supplier_alive,
        "notices": [(n["slot"], n["effect"]) for n in notices],
        "notices_principle_slot": sum(1 for n in notices if n["slot"] == 2),
        "follow_fetches": L.fetch_count(clock="follow"), "background_polls": L.fetch_count(clock="background", include_not_modified=True),
        "background_counted": L.fetch_count(clock="background"),
        "follow_budget_skips": sum(1 for x in w.log if x.get("skipped")),
        "jobs": [{"at": x["at"], "result": x.get("result") or x.get("skipped")} for x in w.log],
        "known_on": {day: (L.known_on(d["kb"], day) or {"statement": None})["statement"]
                     for day in ("2025-10-09T12:00:00Z", "2025-10-10T12:00:00Z")}}


def run(n_phases: int = 12, seed: int = 7) -> dict:
    rng = random.Random(seed)
    d = load()
    runs = [run_phase({"supplier": rng.randrange(PERIOD), "kb": rng.randrange(PERIOD)}, d) for _ in range(n_phases)]
    limit = PERIOD + 24
    return {"note": "기록 재생(AF-RES-152 개정 이력), 실제 폴링 아님. 위상은 고정 씨앗 난수.", "period_h": PERIOD, "seed": seed,
            "criteria": {"1_all_observed_within_period_plus_24h": all(r["max_delay_h"] is not None and r["max_delay_h"] <= limit
                                                                     for r in runs),
                         "2_supplier_watch_alive_after_every_supersession": all(all(r["supplier_watch_alive"]) for r in runs),
                         "3_notices_only_pocket_slot": all(r["notices_principle_slot"] == 0 and r["notices"] and
                                                          all(s == 1 for s, _ in r["notices"]) for r in runs)},
            "worst_delay_h": max((r["max_delay_h"] or 9999) for r in runs), "runs": runs}


def summarize_probes(probes: list[dict]) -> dict:
    from collections import Counter
    n = len(probes)
    reuse = [x for x in probes if x["decision"] == "reuse"]
    fresh = [x for x in probes if not x["behind"]]
    why = Counter(reason_key(w) for x in probes if x["decision"] == "reopen" for w in x["why"])
    only5 = [x for x in fresh if x["decision"] == "reopen" and {reason_key(w) for w in x["why"]} == {"마지막 직접 확인이"}]
    stale = [{"at": x["at"], "edition": x["edition"], "item_known": x["item_known"]} for x in reuse if x["behind"]]
    return {"probes": n, "reuse": len(reuse), "reuse_share": round(len(reuse) / n, 3) if n else None,
            "behind": n - len(fresh), "fresh": len(fresh),
            "reuse_share_when_fresh": round(sum(1 for x in fresh if x["decision"] == "reuse") / len(fresh), 3) if fresh else None,
            "reopen_reasons": dict(why.most_common()), "reopen_only_recheck_h": len(only5), "stale_reuse": stale,
            "oai_reuse": sum(1 for x in probes if x["oai_decision"] == "reuse"),
            "oai_reopen_reasons": dict(Counter(reason_key(w) for x in probes for w in x["oai_why"]).most_common())}


def gate_without_recheck_h(L, o, at):
    """진단용(08 I39 판정 규칙 (b)의 제안 근거, 채택 아님): 조건 (5) '마지막 직접 확인이 RECHECK_H 안'을 뺀 관문."""
    g = L.reuse_gate(o, at)
    why = [w for w in g["why"] if reason_key(w) != "마지막 직접 확인이"]
    return {"decision": "reopen" if why else "reuse", "why": why}


def run_reuse(n_phases: int = 12, seed: int = 7, gate=None) -> dict:
    """재사용 관문을 EVAL-X1 기록 재생 도중에 잰다(08 I39). 위상은 run()과 같은 씨앗."""
    rng = random.Random(seed)
    d = load()
    per = []
    for _ in range(n_phases):
        ph = {"supplier": rng.randrange(PERIOD), "kb": rng.randrange(PERIOD)}
        r = run_phase(ph, d, probe=True, gate=gate)
        per.append({"phases": ph} | summarize_probes(r["probes"]) | {"timeline": [
            (x["at"][:10], "U" if x["decision"] == "reuse" else "O", int(x["behind"])) for x in r["probes"]]})
    allp = sum(x["probes"] for x in per)
    tot = {k: sum(x[k] for x in per) for k in ("probes", "reuse", "behind", "fresh", "reopen_only_recheck_h", "oai_reuse")}
    from collections import Counter
    reasons = Counter()
    for x in per:
        reasons.update(x["reopen_reasons"])
    return {"note": "기록 재생(AF-RES-152 개정 이력) 도중 매일 12:00Z 틱 시작에 묻는 요청 시계 탐침. 관문은 읽기만 한다.",
            "rules": "08 I39", "seed": seed, "recheck_h": __import__("afledger.config", fromlist=["x"]).RECHECK_H,
            "total": tot | {"reuse_share": round(tot["reuse"] / allp, 3),
                            "reuse_share_when_fresh": round(sum(x["fresh"] * (x["reuse_share_when_fresh"] or 0) for x in per)
                                                            / max(1, tot["fresh"]), 3),
                            "stale_reuse": sum(len(x["stale_reuse"]) for x in per),
                            "stale_reuse_item_known": sum(1 for x in per for y in x["stale_reuse"] if y["item_known"]),
                            "reopen_reasons": dict(reasons.most_common())},
            "per_phase": per}


def compare() -> dict:
    """D4(기한 읽기 셋)와 D11(후속 몫 168시간당 3회)의 충돌을 본다(08 I22). 세 경우를 같은 위상 12개로 돈다.
    deadline_separate가 결정된 기본(b2, 08 I23)이고 design_D4_in_follow는 b1이다."""
    from afledger import config
    saved = (config.DEADLINE_BUDGET, config.FOLLOW_FETCHES_PER_10_SOURCES, Ledger.FOLLOW_FETCHES_PER_10_SOURCES)
    out = {}
    for name, budget, cap in (("design_D4_in_follow", "follow", 3), ("deadline_separate", "separate", 3),
                              ("diagnostic_no_follow_cap", "follow", 1000)):
        config.DEADLINE_BUDGET, config.FOLLOW_FETCHES_PER_10_SOURCES, Ledger.FOLLOW_FETCHES_PER_10_SOURCES = budget, cap, cap
        r = run()
        out[name] = {"criteria": r["criteria"], "worst_delay_h": r["worst_delay_h"],
                     "max_delay_by_phase": [x["max_delay_h"] for x in r["runs"]],
                     "follow_fetches": [x["follow_fetches"] for x in r["runs"]],
                     "follow_budget_skips": [x["follow_budget_skips"] for x in r["runs"]],
                     "known_on_2025_10_10": sorted({x["known_on"]["2025-10-10T12:00:00Z"] for x in r["runs"]}),
                     "run0_phase": r["runs"][0]}
    config.DEADLINE_BUDGET, config.FOLLOW_FETCHES_PER_10_SOURCES, Ledger.FOLLOW_FETCHES_PER_10_SOURCES = saved
    return out


def conditional_poll(mode: str = "replay") -> dict:
    """같은 주소 층 조건부 폴링 한 주기(200 다음 304)를 실제로 한 번 기록한다(07 R-2의 이른 신호, 네트워크 2회).
    재생에서는 기록을 읽는다. 시간은 기록에 남은 받은 시각만 있고 지연은 재지 않는다(바이트와 요청 수만)."""
    from afledger.adapters.channel_raw import ConditionalFileChannel
    from afledger.adapters.http import Transport
    t = Transport("record" if mode == "live" else "replay", HERE / "fixtures" / "http_unit2")
    L = Ledger()
    ch = ConditionalFileChannel(L, t, "https://raw.githubusercontent.com/python/cpython/v3.13.18/Lib/asyncio/queues.py",
                                expect="class Queue")
    ch.listing("2026-11-26T00:00:00Z")
    ch.listing("2026-11-26T03:00:00Z")
    return {"log": ch.log, "requests": len(t.log), "counted_fetches": L.fetch_count(clock="background"),
            "recorded_fetches": L.fetch_count(clock="background", include_not_modified=True),
            "bytes_200": ch.log[0]["bytes"], "bytes_304": ch.log[1]["bytes"],
            "note": "304도 요청 1회다(F14 #2). 읽기 예산은 200만 센다(07 D1)."}


if __name__ == "__main__":
    out = run()
    out["budget_comparison"] = compare()
    out["conditional_poll"] = conditional_poll("live" if "--live" in sys.argv else "replay")
    (HERE / "out" / "unit2_x1.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out["criteria"]), "worst delay", out["worst_delay_h"])
    reuse = run_reuse()
    diag = run_reuse(gate=gate_without_recheck_h)
    reuse["diagnostic_without_condition_5"] = {"note": "진단(채택 아님): 조건 (5)를 뺀 관문", "total": diag["total"],
                                                "stale_reuse_by_phase": [x["stale_reuse"] for x in diag["per_phase"]]}
    (HERE / "out" / "unit2_reuse.json").write_text(json.dumps(reuse, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("reuse gate", json.dumps(reuse["total"], ensure_ascii=False))
