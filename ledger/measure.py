"""단위 1의 첫 측정(06 3.3)과 P0 조사의 이른 신호.

  python3 -I ledger/measure.py           기록 재생(네트워크 없음)
  python3 -I ledger/measure.py --live    A4의 자동 접수 문장으로 새 검색을 실제로 돌려 기록한다

쓰는 파일(ledger/out/):
  measure_a4.json        A4: 자동 접수(i1)가 쓴 칸별 필요 문장 대 cases.py 손 문장(서랍 상위 6개·자격, 새 검색 결과)
  measure_b1.json        B1: 한국어 원문을 그대로 서랍에 넣었을 때 우연 적중 비율
  measure_r4.json        R-4: 사생활 검사 p1·p2의 누출 시도 통과율과 정당한 꼬리표 거절률(link-index use 문장)
  measure_normalize.json R-1: link-index 전체 주소로 n1 회귀(깨짐, 묶임, 색인 자체 키와의 일치)
  measure_f01.json       M2·R-6 이른 신호: F01 잡음을 넣은 R1 서랍
  measure_r1_map.json    R-1: queues.py·locks.py의 docstring 위치를 3.13.18 → 3.12.3으로 대응(m1) 대 ast 정답
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from afledger import Ledger, intake as intake_mod, locate, normalize, privacy  # noqa: E402
from afledger.adapters.http import Transport  # noqa: E402
from afledger.adapters.reader_github import raw_url  # noqa: E402
from afledger.adapters.search_github import direct_branch  # noqa: E402
from afledger.ledger import FUNCTION_WORDS, content_tokens  # noqa: E402
from drawer_load import link_index_rows, preload_catalog, preload_noise  # noqa: E402

FIX = HERE / "fixtures"
OUT = HERE / "out"
T0 = "2026-11-26T01:00:00Z"


def write(name, d):
    (OUT / name).write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def studio(name):
    return json.loads((FIX / "r1" / name).read_text(encoding="utf-8"))


def p03():
    for line in (FIX / "af-res-012" / "queries.jsonl").read_text(encoding="utf-8").splitlines():
        q = json.loads(line)
        if q["id"] == "P03.w":
            return q


def drawer_ids(L, catalog, noise, hits):
    inv = {v: k for k, v in catalog.items()}
    return [inv.get(h["obs_id"]) or (f"F01:{noise[h['obs_id']]['record']}" if h["obs_id"] in noise else h["obs_id"])
            for h in hits]


# ------------------------------------------------------------------------------------------- A4
def a4(mode):
    s = studio("studio_rev1.json")
    hand = s["needs"]
    q = p03()
    reqs_en = [  # P03 영어판의 조건 줄(같은 코드). 영어판은 012 자료집의 번역본이다
        {"code": "H1", "kind": "must", "text": "The waiting queue must hold at most eight items, and at most four jobs may run at a time."},
        {"code": "H2", "kind": "must_not", "text": "The producer must wait when the sink slows. It may not create tasks for all inputs ahead of time or move them into another unbounded buffer."},
        {"code": "H3", "kind": "must", "text": "Admission must resume based on completion or recovery of capacity. Time passing alone must not allow the concurrency bound to be exceeded."},
        {"code": "X", "kind": "out_of_scope", "text": "A total RAM byte bound"}]
    variants = {
        "hand": hand,
        "i1_ko": intake_mod.write_needs(s["text"], s["requirements"]),
        "i1_en": intake_mod.write_needs(q["en"], reqs_en),
    }
    t = Transport("record" if mode == "live" else "replay", FIX / "http")
    out = {"rule": "크게 어긋남 = 자동 문장의 서랍 상위 6개에 asyncio-queue가 없거나, 손 문장 상위 6개와 겹침이 3개 미만이거나, "
                   "asyncio-queue가 자격을 잃거나, 새 검색 직접 갈래 1위가 queues.py가 아님(돌리기 전에 정함)",
           "variants": {}}
    out["token_rules_compared"] = ["t1", "t2"]
    for tok in ("t1", "t2"):
      for name, needs in variants.items():
        for with_noise in (False, True):
            L = Ledger()
            L.token_rules = tok
            catalog = preload_catalog(L)
            noise = preload_noise(L) if with_noise else {}
            p = L.project("A")
            kw = dict(request_key="R1", rev=1, at=T0, text=s["text"], selected_part="파이프라인: 작업 투입·완료 신호",
                      requirements=s["requirements"], context={"runtime": {"value": "CPython 3.13", "provenance": "studio"}},
                      needs=needs)
            req = L.intake(p, **kw)
            hits = L.search_drawer(p, req, T0, k=12)
            ids = drawer_ids(L, catalog, noise, hits)
            deep = L.search_drawer(p, req, T0, k=5000, log=False)
            deep_ids = drawer_ids(L, catalog, noise, deep)
            row = {"top6": ids[:6], "eligible_top6": [h["eligible"] for h in hits[:6]],
                   "asyncio_queue_rank": ids.index("asyncio-queue") + 1 if "asyncio-queue" in ids else None,
                   "asyncio_queue_eligible": next((h["eligible"] for h, i in zip(hits, ids) if i == "asyncio-queue"), False),
                   "eligible_count": sum(h["eligible"] for h in hits),
                   "asyncio_semaphore_rank": ids.index("asyncio-semaphore") + 1 if "asyncio-semaphore" in ids else None,
                   "eligible_total": sum(h["eligible"] for h in deep),
                   "deep_rank": {n: (deep_ids.index(n) + 1 if n in deep_ids else None,
                                     next((h["eligible"] for h, i in zip(deep, deep_ids) if i == n), False))
                                 for n in ("asyncio-queue", "asyncio-semaphore")}}
            if not with_noise and tok == "t2":
                row["needs"] = needs
                try:
                    d = direct_branch(L, t, p, req, T0, context=L.context(p, req), request_text=s["text"],
                                      selected_part="파이프라인: 작업 투입·완료 신호", content_tokens=content_tokens)
                    row["fresh_terms"] = [x["term"] for x in d["terms"]]
                    row["fresh_top"] = [x["path"] for x in d["results"]]
                except Exception as e:  # noqa: BLE001 - 기록이 없으면 측정에서 뺀다
                    row["fresh_error"] = f"{type(e).__name__}: {e}"
            out["variants"].setdefault(f"{name}@{tok}", {})["with_F01_noise" if with_noise else "catalog_only"] = row
    for tok in ("t1", "t2"):
      hand6 = out["variants"][f"hand@{tok}"]["catalog_only"]["top6"]
      for name in ("i1_ko", "i1_en"):
        v = out["variants"][f"{name}@{tok}"]["catalog_only"]
        overlap = len(set(v["top6"]) & set(hand6))
        big = (v["asyncio_queue_rank"] is None or v["asyncio_queue_rank"] > 6 or overlap < 3 or not v["asyncio_queue_eligible"]
               or (v.get("fresh_top") or [None])[0] != "Lib/asyncio/queues.py")
        v["overlap_with_hand_top6"] = overlap
        v["big_deviation"] = big
        # 돌린 뒤 드러난 이차 신호(규칙에는 없다): 적격 후보 수와 근접 대안(세마포어)이 서랍에 남는가
        v["secondary"] = {"eligible_count": v["eligible_count"],
                          "eligible_count_hand": out["variants"][f"hand@{tok}"]["catalog_only"]["eligible_count"],
                          "asyncio_semaphore_rank": v["asyncio_semaphore_rank"],
                          "asyncio_semaphore_rank_hand": out["variants"][f"hand@{tok}"]["catalog_only"]["asyncio_semaphore_rank"]}
    # 자동 접수(i1, 한국어 원문)로 R1 흐름 전체를 돌리면 완료 기준 2가 어떻게 되나(서랍 토큰화 t1·t2 × F01 잡음 유무)
    import run_r1
    from afledger import config as cfg
    out["r1_flow_with_i1_ko"] = {}
    saved = cfg.TOKEN_RULES
    for tok in ("t1", "t2"):
        for noise in (False, True):
            cfg.TOKEN_RULES = tok
            key = f"{tok}_{'with_F01' if noise else 'catalog_only'}"
            try:
                r = run_r1.run(mode if mode == "live" else "replay", needs="i1", noise=noise)
                r.pop("_ledger")
                folded = {f["condition"]: f["reason"] for f in r["rev1"]["answer"]["folded"]}
                slot1 = next((s_["sentence"] for s_ in r["rev1"]["answer"]["slots"] if s_["kind"] == "direct"), "")
                c2 = {"first_slot_queue_313_L4": "/blob/v3.13." in slot1 and "queues.py#L" in slot1
                      and "이 판에서 실행해 값을 확인했다" in slot1,
                      "must_four_workers": "[필수] 일꾼 작업을 정확히 4개" in slot1,
                      "semaphore_folded_H1U": "H1 U" in folded.get("대기 8을 대기열 길이로 지키는가", ""),
                      "create_all_folded_H2": "H2 위반" in folded.get("입력마다 작업 객체를 미리 만드는가", ""),
                      "search_record": bool(r["rev1"]["drawer"]) and bool(r["rev1"]["fresh_direct"]["calls"])}
                out["r1_flow_with_i1_ko"][key] = {"criterion2_pass": all(c2.values()), "parts": c2,
                    "status": r["rev1"]["answer"]["status"], "unread": r["rev1"]["unread"],
                    "drawer_top3": [h["id"] for h in r["rev1"]["drawer"][:3]],
                    "drawer_symbols": [x["name"] for x in r["rev1"]["fresh_direct"]["drawer_symbols_resolved"]],
                    "budget": r["rev1"]["budget"]}
            except Exception as e:  # noqa: BLE001
                out["r1_flow_with_i1_ko"][key] = {"error": f"{type(e).__name__}: {e}"}
    cfg.TOKEN_RULES = saved
    write("measure_a4.json", out)
    return out


# ------------------------------------------------------------------------------------------- B1
def ko_eojeol(text):
    return list(dict.fromkeys(re.findall(r"[가-힣]+", text)))


def b1():
    """한국어 문장을 칸 하나(summary)의 필요 문장으로 그대로 넣는다(질의 101개, 서랍 = 자료집 156 + F01).
    t1 = 설계 예제 토큰화(영어만), t2 = R-5 결정(영어 + 한국어 어절 줄기·음절 2-gram, 기능 어절 제외).
    naive = 한글 어절을 그대로 토큰으로 세는 경우(형태 분석·기능 어절 목록 없음, FTS5 unicode61과 같음).
    도달 = 적중이 하나 이상인 질의. 내용 도달 = 우연이 아닌 적중이 하나 이상인 질의.
    우연 적중 = 맞은 토큰이 모두 기능어(영어 닫힌 목록, 숫자, tokenize.KO_FUNC_EOJEOL·조사 덩어리)인 적중."""
    from afledger import tokenize as kt
    rows = link_index_rows()
    sample = [r for i, r in enumerate(rows) if i % 40 == 0 and re.search(r"[가-힣]", r["use"])][:100]
    s = studio("studio_rev1.json")
    queries = [{"src": "R1 P03.w 한국어 원문", "text": s["text"]}] + \
              [{"src": f"link-index {r['record']}", "text": r["use"]} for r in sample]
    out = {"queries": len(queries), "sample_rule": "link-index 40행마다 1행(한글 use), 최대 100 + R1 원문", "modes": {}}
    for mode in ("t1", "t2"):
        L = Ledger()
        L.token_rules = mode
        preload_catalog(L)
        preload_noise(L)
        p = L.project("B1")
        c = Counter()
        for i, qd in enumerate(queries):
            req = L.intake(p, request_key=f"B{i}", rev=1, at=T0, text=qd["text"], selected_part="s", requirements=[],
                           needs=[{"slot": "summary", "lang": "ko", "text": qd["text"]}])
            hits = L.search_drawer(p, req, T0, k=10, min_slots=1, include_function_words=True, log=False)
            c["hits"] += len(hits)
            c["accidents"] += sum(h["lexical_accident"] for h in hits)
            c["reached"] += bool(hits)
            c["content_reached"] += any(not h["lexical_accident"] for h in hits)
        out["modes"][mode] = dict(c) | {"accident_ratio": round(c["accidents"] / c["hits"], 4) if c["hits"] else None}
    # naive: 한글 어절 그대로(기능 어절도 내용어로)
    L = Ledger()
    preload_catalog(L)
    preload_noise(L)
    tags = [(t["obs_id"], t["text"]) for t in L.db.execute("SELECT obs_id, text FROM tag")]
    c = Counter()
    examples = []
    for qd in queries:
        qt = set(ko_eojeol(qd["text"]))
        scored = sorted(((len(qt & set(ko_eojeol(t))), o, sorted(qt & set(ko_eojeol(t)))) for o, t in tags
                         if qt & set(ko_eojeol(t))), key=lambda x: (-x[0], x[1]))[:10]
        acc = [x for x in scored if all(kt.KO_FUNC_EOJEOL.match(w) or w in kt.KO_ENDINGS_SET for w in x[2])]
        c["hits"] += len(scored)
        c["accidents"] += len(acc)
        c["reached"] += bool(scored)
        c["eligible_if_counted_as_content"] += sum(1 for x in acc if x[0] >= 2)
        if acc and len(examples) < 6:
            examples.append({"query": qd["src"], "matched_only_function_eojeols": acc[0][2]})
    out["modes"]["naive_eojeol"] = dict(c) | {"accident_ratio": round(c["accidents"] / c["hits"], 4) if c["hits"] else None}
    out["examples_naive"] = examples
    write("measure_b1.json", out)
    return out


# ------------------------------------------------------------------------------------------- R-4
def r4():
    rows = [r for r in link_index_rows() if re.search(r"[가-힣]", r["use"])]
    by_p: dict[str, list] = {}
    for r in rows:
        by_p.setdefault(r["problem"], []).append(r)
    legit, leaks = [], []
    for prob, rs in sorted(by_p.items()):
        if len(rs) < 10:
            continue
        for i, r in enumerate(rs[::7][:12]):
            others = [x["use"] for x in rs if x is not r][:20]   # 같은 분야의 다른 요청 20개
            legit.append((r["use"], r["evidence"], others))
        for r in rs[3::25][:4]:
            u = r["use"]
            half = u[: max(10, len(u) // 2)]
            leaks.append((u, "", [u]))                           # 요청 문장을 그대로 꼬리표로
            leaks.append((half, "", [u]))                        # 앞 절반만
    variants = {"p1": {}, "p2": {"KO_MIN_COUNT": 3, "VERBATIM_CHARS": 16},
                "p2_k2": {"KO_MIN_COUNT": 2, "VERBATIM_CHARS": 16}, "p2_k4": {"KO_MIN_COUNT": 4, "VERBATIM_CHARS": 16},
                "p2_v12": {"KO_MIN_COUNT": 3, "VERBATIM_CHARS": 12}, "p2_v24": {"KO_MIN_COUNT": 3, "VERBATIM_CHARS": 24},
                "p2_verbatim_v12": {"KO_TOKEN_RULE": False, "VERBATIM_CHARS": 12},
                "p2_verbatim_v16": {"KO_TOKEN_RULE": False, "VERBATIM_CHARS": 16},
                "p2_verbatim_v24": {"KO_TOKEN_RULE": False, "VERBATIM_CHARS": 24}}
    saved = (privacy.KO_MIN_COUNT, privacy.VERBATIM_CHARS, privacy.KO_TOKEN_RULE)
    out = {"legit_tags": len(legit), "leak_attempts": len(leaks),
           "rule": "누출 시도 통과 0이면서 정당한 꼬리표 거절 5% 미만인 안 가운데 거절이 가장 적은 안(07 R-4 끝나는 조건, 돌리기 전에 정함)",
           "sample": "link-index 문제별(10행 이상) 7행마다 최대 12행을 정당한 꼬리표(원문 쪽 = evidence), 같은 문제의 다른 use 20개를 다른 프로젝트 요청으로. "
                     "누출 시도는 문제별 4행의 use 전체와 앞 절반",
           "variants": {}}
    for name, cfg in variants.items():
        privacy.KO_MIN_COUNT = cfg.get("KO_MIN_COUNT", saved[0])
        privacy.VERBATIM_CHARS = cfg.get("VERBATIM_CHARS", saved[1])
        privacy.KO_TOKEN_RULE = cfg.get("KO_TOKEN_RULE", True)
        rules = "p1" if name == "p1" else "p2"
        rej = sum(1 for tag, src, reqs in legit if any(privacy.leak(tag, src, q, rules) for q in reqs))
        passed = sum(1 for tag, src, reqs in leaks if not any(privacy.leak(tag, src, q, rules) for q in reqs))
        out["variants"][name] = {"legit_rejected": rej, "legit_reject_rate": round(rej / len(legit), 4),
                                 "leak_passed": passed, "leak_pass_rate": round(passed / len(leaks), 4)} | cfg
    privacy.KO_MIN_COUNT, privacy.VERBATIM_CHARS, privacy.KO_TOKEN_RULE = saved
    ok = {k: v for k, v in out["variants"].items() if v["leak_passed"] == 0 and v["legit_reject_rate"] < 0.05}
    out["chosen"] = min(ok, key=lambda k: out["variants"][k]["legit_reject_rate"]) if ok else None
    write("measure_r4.json", out)
    return out


# ------------------------------------------------------------------------------------------- 정규화 회귀
def norm_regression():
    rows = link_index_rows()
    urls = sorted({r["url"] for r in rows})
    keys = {u: normalize.keys(u) for u in urls}
    errs = Counter(k["rules"] for k in keys.values() if k["rules"] != "n1")
    ok = [k for k in keys.values() if k["rules"] == "n1"]
    idem = sum(1 for k in ok if normalize.keys(k["url_norm"])["page"] == k["page"])
    page_groups = Counter(k["page"] for k in ok)
    target_groups = Counter(k["target"] or k["page"] for k in ok)
    agree_page = agree_target = comparable = 0
    for r in rows:
        k = keys[r["url"]]
        if k["rules"] != "n1":
            continue
        comparable += 1
        agree_page += (r["page"].strip() == k["page"])
        agree_target += (r["target"].strip() == (k["target"] or ""))
    multi = [(p, n) for p, n in page_groups.most_common(8) if n > 1]
    out = {"rows": len(rows), "distinct_raw_urls": len(urls), "errors": dict(errors := errs),
           "distinct_url_norm": len({k["url_norm"] for k in ok}), "distinct_page": len(page_groups),
           "distinct_target_or_page": len(target_groups),
           "idempotent_page_on_url_norm": f"{idem}/{len(ok)}",
           "pages_with_several_raw_urls": sum(1 for n in page_groups.values() if n > 1), "largest_page_groups": multi,
           "largest_target_groups": target_groups.most_common(8),
           "agreement_with_index_columns": {"rows_compared": comparable, "page_equal": agree_page, "target_equal": agree_target,
                                            "note": "link-index의 page·target 열은 dot 세션이 손으로 쓴 키다(README: 확정하기 어려우면 원문 주소)."},
           "exact_duplicate_rows": len(rows) - len({tuple((r[c] for c in ("page", "target", "problem", "use", "url", "evidence", "edition", "record"))) for r in rows})}
    _ = errors
    write("measure_normalize.json", out)
    return out


# ------------------------------------------------------------------------------------------- F01 잡음
def f01():
    s = studio("studio_rev1.json")
    out = {}
    for name, with_noise in (("catalog_only", False), ("with_F01", True)):
        L = Ledger()
        catalog = preload_catalog(L)
        noise = preload_noise(L) if with_noise else {}
        p = L.project("A")
        req = L.intake(p, request_key="R1", rev=1, at=T0, text=s["text"], selected_part="s",
                       requirements=s["requirements"], needs=s["needs"])
        hits = L.search_drawer(p, req, T0, k=10)
        audit = L.search_drawer(p, req, T0, k=1000, min_slots=1, include_function_words=True, log=False)
        content = {h["obs_id"]: h for h in L.search_drawer(p, req, T0, k=1000, log=False)}
        acc = [h for h in audit if h["lexical_accident"]]
        ids = drawer_ids(L, catalog, noise, hits)
        out[name] = {"top10": ids, "noise_in_top10": sum(1 for i in ids if str(i).startswith("F01:")),
                     "asyncio_queue_rank": ids.index("asyncio-queue") + 1 if "asyncio-queue" in ids else None,
                     "function_word_only_hits_in_audit": len(acc),
                     "of_which_noise": sum(1 for h in acc if h["obs_id"] in noise),
                     "function_word_only_hits_that_are_eligible_under_rule": sum(
                         1 for h in acc if content.get(h["obs_id"], {}).get("eligible")),
                     "eligible_noise_total": sum(1 for o, h in content.items() if o in noise and h["eligible"]),
                     "drawer_size": len(catalog) + len(noise)}
    out["reading"] = ("서랍 자격은 내용어로만 매기므로 기능어·숫자만 맞은 적중은 자격이 0이다. "
                      "자격을 얻은 잡음은 내용어(queue, worker, jobs 등)가 맞은 같은 분야 글이다(M2·R-6의 문제는 이쪽).")
    write("measure_f01.json", out)
    return out


# ------------------------------------------------------------------------------------------- R-1 docstring 대응
def r1_map():
    t = Transport("replay", FIX / "http")
    out = {"rule": "3.13.18의 모든 class·def docstring 위치를 m1로 3.12.3에 대응한다. 정답 = 같은 기호 경로가 3.12.3 ast에 있으면 그 docstring 범위, "
                   "없으면 '없음'. exact_quote는 docstring 문장이 그대로 남은 경우, symbol은 문장이 바뀐 경우다.", "files": {}}
    tot = Counter()
    for path in ("Lib/asyncio/queues.py", "Lib/asyncio/locks.py"):
        new = t.get(raw_url("python/cpython", "v3.12.3", path)).text()
        old = t.get(raw_url("python/cpython", "v3.13.18", path)).text()
        so, sn = locate.symbols(old), locate.symbols(new)
        c = Counter()
        wrong = []
        for q, s in so.items():
            if not s["doc"]:
                continue
            a = locate.anchor(old, *s["doc"], python=True)
            m = locate.map_position(a, new, python=True)
            truth = sn[q]["doc"] if q in sn and sn[q]["doc"] else (sn[q]["range"] if q in sn else None)
            got = m["lines"]
            c["positions"] += 1
            c[m["method"]] += 1
            okk = (got == truth) if truth else (got is None)
            c["agree"] += okk
            if not okk:
                wrong.append({"symbol": q, "method": m["method"], "got": got, "truth": truth})
        out["files"][path] = dict(c) | {"disagreements": wrong}
        tot.update(c)
    out["total"] = dict(tot)
    write("measure_r1_map.json", out)
    return out


# ------------------------------------------------------------------------------------------- A4 한국어 20건
def a4_20():
    """A4를 한국어 요청 20건으로 넓힌다(08 I19). 고르는 규칙(돌리기 전에 정함): 012 질의 가운데 등급 2 판정이 하나 이상 있고
    P03 묶음(R1)이 아닌 것, 파일 순서로 앞의 20건. 조건은 원문의 'Pxx-Hn:' 줄에서 읽고(requirements_from_text), 칸별 필요 문장은
    접수 규칙(config.INTAKE_RULES)이 쓴다. 비교 팔은 같은 규칙을 012의 영어판에 쓴 것(번역 접수의 대용). 서랍은 012 자료집 156항목
    (+F01 잡음). 판정은 012 qrels(등급 1·2).
    확인 범위 예산(I18): 런타임이 CPython이라고 둘 때 사용자 판 확인으로 넘길 서랍 후보(적격, 자료집 이름이 '<표준 라이브러리>.<클래스>')
    수를 top_k(상위 12)와 eligible(적격 전부)로 세고, 외부 시도 = 직접 갈래 낱말 6 + 확인 검색 + 가져오기 2로 한도 10과 비교한다."""
    import csv
    import sys as _sys
    from afledger.adapters.search_github import MAX_TERMS
    qs = [json.loads(line) for line in (FIX / "af-res-012" / "queries.jsonl").read_text(encoding="utf-8").splitlines()]
    qrels: dict[str, dict] = {}
    for r in csv.DictReader(open(FIX / "af-res-012" / "qrels.tsv", encoding="utf-8"), delimiter="\t"):
        if r["grade"].isdigit():   # N은 판정 보류(근접 오답 표시 등)라 빼고 센다
            qrels.setdefault(r["query_id"], {})[r["entry_id"]] = int(r["grade"])
    chosen = [q for q in qs if any(g == 2 for g in qrels.get(q["id"], {}).values())
              and not q["id"].startswith("P03")][:20]
    rows, agg = [], {}
    for noise in (False, True):
        L = Ledger()
        cat = preload_catalog(L)
        nz = preload_noise(L) if noise else {}
        inv = {v: k for k, v in cat.items()}
        p = L.project("A20")
        for q in chosen:
            row = {"id": q["id"], "noise": noise}
            for lang in ("ko", "en"):
                text = q[lang]
                reqs = intake_mod.requirements_from_text(text)
                needs = intake_mod.write_needs(text, reqs)
                req = L.intake(p, request_key=f"{q['id']}.{lang}", rev=1, at=T0, text=text, selected_part="s",
                               requirements=reqs, needs=needs)
                hits = L.search_drawer(p, req, T0, k=5000, log=False)
                ids = [inv.get(h["obs_id"]) for h in hits]
                rel = {e: g for e, g in qrels[q["id"]].items() if g >= 1}
                top = ids[:12]
                g2 = [e for e, g in rel.items() if g == 2]
                best2 = min((ids.index(e) + 1 for e in g2 if e in ids), default=None)
                sym = [h for h in hits if h["eligible"] and re.fullmatch(
                    r"([a-z_]+)\.[A-Z]\w*", (L.obs(h["obs_id"])["quote"] or "").split(" — ")[0])
                    and (L.obs(h["obs_id"])["quote"] or "").split(".")[0] in _sys.stdlib_module_names]
                row[lang] = {"needs_slots": sorted(n["slot"] for n in needs),
                             "eligible": sum(h["eligible"] for h in hits),
                             "recall12": round(sum(1 for e in rel if e in top) / len(rel), 3) if rel else None,
                             "grade2_best_rank": best2, "grade2_in_top12": bool(best2 and best2 <= 12),
                             "symbol_confirm_top_k": sum(1 for h in sym if hits.index(h) < 12),
                             "symbol_confirm_eligible": len(sym)}
                for scope in ("top_k", "eligible"):
                    row[lang][f"projected_external_{scope}"] = MAX_TERMS + row[lang][f"symbol_confirm_{scope}"] + 2
            rows.append(row)
        key = "with_F01" if noise else "catalog_only"
        rs = [r for r in rows if r["noise"] == noise]
        agg[key] = {lang: {"mean_recall12": round(sum(r[lang]["recall12"] or 0 for r in rs) / len(rs), 3),
                           "grade2_in_top12": sum(r[lang]["grade2_in_top12"] for r in rs),
                           "zero_eligible": sum(1 for r in rs if r[lang]["eligible"] == 0),
                           "max_symbol_confirm_eligible": max(r[lang]["symbol_confirm_eligible"] for r in rs),
                           "over_budget_eligible": sum(1 for r in rs if r[lang]["projected_external_eligible"] > 10)}
                    for lang in ("ko", "en")}
        agg[key]["ko_misses_grade2_en_finds"] = [r["id"] for r in rs if r["en"]["grade2_in_top12"]
                                                 and not r["ko"]["grade2_in_top12"]]
        agg[key]["ko_recall_below_en_by_0.25"] = [r["id"] for r in rs if (r["ko"]["recall12"] or 0)
                                                  < (r["en"]["recall12"] or 0) - 0.25]
    out = {"rule": a4_20.__doc__.split("\n")[1:3], "queries": [q["id"] for q in chosen],
           "intake_rules": __import__("afledger").config.INTAKE_RULES, "summary": agg, "rows": rows}
    write("measure_a4_20.json", out)
    return out


# ------------------------------------------------------------------------------------------- R-3 판독 재현성
def r3(mode):
    """07 R-3: 같은 위치를 다시 읽었을 때 결과 차이(08 I21). 판독기는 gh-pinned-lines/1(결정적 코드).
    위치: queues.py·locks.py의 v3.13.18·v3.12.3에서 docstring이 있는 모든 class·def(기호 경로로 찾음).
    읽기 셋: (A) R1 실행 때 기록한 raw 원문, (B) 같은 주소를 나중에 다시 받은 원문(fixtures/http_r3, --live에서만 네트워크 4회),
    (C) 이 컨테이너에 설치된 같은 판의 표준 라이브러리(다른 배포 경로, fixtures/local_stdlib).
    더해 R1 위치 4개를 바이트 범위(Range)로 다시 받아(네트워크 4회) 전체 원문의 같은 범위와 대조한다.
    잰다: 파일 바이트 일치, 위치별 줄 범위 일치, 인용 지문 일치, 같은 장부에 세 번 쓸 때 새 관측·다시 본 기록·충돌 수."""
    from afledger.adapters.reader_github import raw_url
    ta = Transport("replay", FIX / "http")
    tb = Transport("record" if mode == "live" else "replay", FIX / "http_r3")
    files = [("v3.13.18", "Lib/asyncio/queues.py"), ("v3.13.18", "Lib/asyncio/locks.py"),
             ("v3.12.3", "Lib/asyncio/queues.py"), ("v3.12.3", "Lib/asyncio/locks.py")]
    out = {"rule": r3.__doc__.split("\n")[1:5], "files": {}, "positions": 0, "by_pair": {}, "range": []}
    L = Ledger()
    pairs = {"A_vs_B": Counter(), "A_vs_C": Counter()}
    for tag, path in files:
        url = raw_url("python/cpython", tag, path)
        ra, rb = ta.get(url), tb.get(url, note=f"r3 reread {tag}:{path}")
        texts = {"A": ra.text(), "B": rb.text() if rb.status == 200 else None,
                 "C": (FIX / "local_stdlib" / tag.lstrip("v") / "asyncio" / path.split("/")[-1]).read_text(encoding="utf-8")}
        sha = {k: (hashlib.sha256(v.encode()).hexdigest()[:16] if v is not None else None) for k, v in texts.items()}
        out["files"][f"{tag}:{path}"] = {"sha256_16": sha, "B_status": rb.status, "B_fetched_at": rb.fetched_at,
                                         "A_fetched_at": ra.fetched_at, "etag_A": ra.headers.get("etag"),
                                         "etag_B": rb.headers.get("etag")}
        syms = {k: locate.symbols(v) for k, v in texts.items() if v is not None}
        for q, sa in syms["A"].items():
            if not sa["doc"]:
                continue
            out["positions"] += 1
            qa = locate.lines_text(texts["A"], *sa["doc"])
            for read in ("A", "B", "C"):
                if read not in syms:
                    continue
                sx = syms[read].get(q)
                quote = locate.lines_text(texts[read], *sx["doc"]) if sx and sx["doc"] else None
                L.observe(url=f"https://github.com/python/cpython/blob/{tag}/{path}", edition_key=tag, edition_kind="release",
                          position=f"{q}.__doc__", at=f"2026-11-26T0{'ABC'.index(read) + 1}:00:00Z", method="read_line",
                          quote=quote or "(없음)", quote_lang="en", statement="docstring", reader=f"gh-pinned-lines/1:{read}")
                if read != "A":
                    c = pairs[f"A_vs_{read}"]
                    c["compared"] += 1
                    c["same_lines"] += bool(sx and sx["doc"] == sa["doc"])
                    c["same_quote_fp"] += bool(quote and locate.quote_fp(quote) == locate.quote_fp(qa))
    out["by_pair"] = {k: dict(v) for k, v in pairs.items()}
    out["ledger"] = {"observations": L.counts()["observations"], "sightings": L.counts()["sightings"],
                     "conflicts_flagged": sum(1 for a in L.alerts if a["kind"] == "reading_conflict"),
                     "audit_jobs": len(L.jobs())}
    # R1 위치 4개를 바이트 범위로 다시 받는다(관문 재열람과 같은 길)
    live = json.loads((OUT / "r1_live.json").read_text(encoding="utf-8"))
    for k, r in live["rev1"]["readings"].items():
        tag, path = "v3.13.18", r["link"].split("/blob/")[1].split("#")[0].split("/", 1)[1]
        url = raw_url("python/cpython", tag, path)
        full = ta.get(url).body
        a_, b_ = map(int, r["byte_span"].split("-"))
        rr = tb.get(url, {"Range": f"bytes={r['byte_span']}"}, note=f"r3 range {k}")
        out["range"].append({"id": k, "position": r["position"], "status": rr.status,
                             "same_bytes_as_full_slice": rr.body == full[a_:b_ + 1],
                             "same_quote_fp": locate.quote_fp(rr.text()) == r["quote_fp"]})
    write("measure_r3.json", out)
    return out


# ------------------------------------------------------------------------------------------- R-6 규모
NOISE_TOTAL = 20000


def r6_scale():
    """07 R-6의 끝나는 조건: 잡음 2만 개에서 상위 10 중 잡음 2개 이하, 사례 결과는 그대로(08 I20).
    잡음 = 012 자료집 밖의 모든 관측. 실제 잡음은 link-index 전체(4,390행, 관측 2,480개), 나머지는 합성
    (drawer_load.preload_synthetic, link-index 문장 반쪽을 고정 씨앗으로 섞음)으로 2만 개를 채운다.
    잰다: R1(손 문장·자동 한국어)과 A4 20건(한국어·영어판)의 상위 10 잡음 수, 순위 규칙 r0·r2 비교, R1 흐름의 완료 기준 2."""
    import csv
    import time
    import run_r1
    from drawer_load import preload_all_link_index, preload_synthetic

    def noise_loader(L):
        real = preload_all_link_index(L)
        return list(real) + preload_synthetic(L, NOISE_TOTAL - len(real))

    s = studio("studio_rev1.json")
    qs = [json.loads(line) for line in (FIX / "af-res-012" / "queries.jsonl").read_text(encoding="utf-8").splitlines()]
    qrels: dict[str, dict] = {}
    for r in csv.DictReader(open(FIX / "af-res-012" / "qrels.tsv", encoding="utf-8"), delimiter="\t"):
        if r["grade"].isdigit():
            qrels.setdefault(r["query_id"], {})[r["entry_id"]] = int(r["grade"])
    a20 = json.loads((OUT / "measure_a4_20.json").read_text(encoding="utf-8"))["queries"]
    out = {"rule": r6_scale.__doc__.split("\n")[1:4], "noise_total": NOISE_TOTAL, "rank_rules": {},
           "rank_rules_current": __import__("afledger").config.RANK_RULES}
    configs = (("r0", noise_loader), ("r2", noise_loader), ("r2_real_only", lambda L: list(preload_all_link_index(L))))
    for rank, loader in configs:
        t0 = time.time()
        L = Ledger()
        # "r2" 열쇠는 "지금 순위 규칙" 자리다(I20 이후 이름을 지킨다). 실제 규칙은 rank_rules_current에 남긴다
        L.rank_rules = "r0" if rank == "r0" else __import__("afledger").config.RANK_RULES
        cat = preload_catalog(L)
        catset = set(cat.values())
        inv = {v: k for k, v in cat.items()}
        n_noise = len(loader(L))
        p = L.project("S")
        res = {"noise_observations": n_noise, "r1": {}, "a4_20": {}}
        cases = {"hand": s["needs"], "i2_ko": intake_mod.write_needs(s["text"], s["requirements"])}
        for name, nd in cases.items():
            req = L.intake(p, request_key=f"R1.{name}", rev=1, at=T0, text=s["text"], selected_part="s",
                           requirements=s["requirements"], needs=nd)
            hits = L.search_drawer(p, req, T0, k=5000, log=False)
            ids = [inv.get(h["obs_id"], "noise") for h in hits]
            top_noise = [L.obs(h["obs_id"])["url"] for h in hits[:10] if h["obs_id"] not in catset]
            res["r1"][name] = {"noise_in_top10": len(top_noise),
                               "noise_top10_synthetic": sum(1 for u in top_noise if "synthetic.invalid" in u),
                               "noise_top10_real_link_index": sum(1 for u in top_noise if "synthetic.invalid" not in u),
                               "asyncio_queue": ids.index("asyncio-queue") + 1 if "asyncio-queue" in ids else None,
                               "asyncio_semaphore": ids.index("asyncio-semaphore") + 1 if "asyncio-semaphore" in ids else None,
                               "eligible": sum(h["eligible"] for h in hits)}
        for lang in ("ko", "en"):
            nz10, rec, g2 = [], [], 0
            for q in (x for x in qs if x["id"] in a20):
                reqs = intake_mod.requirements_from_text(q[lang])
                req = L.intake(p, request_key=f"{q['id']}.{lang}", rev=1, at=T0, text=q[lang], selected_part="s",
                               requirements=reqs, needs=intake_mod.write_needs(q[lang], reqs))
                hits = L.search_drawer(p, req, T0, k=12, log=False)
                ids = [inv.get(h["obs_id"]) for h in hits]
                rel = {e for e, g in qrels[q["id"]].items() if g >= 1}
                nz10.append(sum(1 for h in hits[:10] if h["obs_id"] not in catset))
                rec.append(sum(1 for e in rel if e in ids) / len(rel))
                g2 += any(qrels[q["id"]].get(e) == 2 for e in ids)
            res["a4_20"][lang] = {"mean_noise_in_top10": round(sum(nz10) / len(nz10), 2),
                                  "requests_with_noise_le_2": sum(1 for x in nz10 if x <= 2),
                                  "mean_recall12": round(sum(rec) / len(rec), 3), "grade2_in_top12": g2}
        res["seconds"] = round(time.time() - t0, 1)
        out["rank_rules"][rank] = res
    flow = {}
    for nn in ("studio", "i1"):
        r = run_r1.run("replay", needs=nn, noise=False, noise_loader=noise_loader)
        r.pop("_ledger")
        folded = {f["condition"]: f["reason"] for f in r["rev1"]["answer"]["folded"]}
        slot1 = next((x["sentence"] for x in r["rev1"]["answer"]["slots"] if x["kind"] == "direct"), "")
        flow["hand" if nn == "studio" else "i2_ko"] = {
            "first_slot_queue_313_L4": "/blob/v3.13." in slot1 and "queues.py#L" in slot1,
            "semaphore_folded_H1U": "H1 U" in folded.get("대기 8을 대기열 길이로 지키는가", ""),
            "create_all_folded_H2": "H2 위반" in folded.get("입력마다 작업 객체를 미리 만드는가", ""),
            "drawer_symbols": [(x["name"], x.get("drawer_rank"), x.get("skipped")) for x in
                               r["rev1"]["fresh_direct"]["drawer_symbols_resolved"]],
            "external_attempts": r["rev1"]["budget"]["external_attempts"]}
    out["r1_flow_r2"] = flow
    out["diagnostic_eligibility_idf_floor"] = {
        "note": "채택하지 않은 진단(08 I20). 자격의 서로 다른 내용어 둘을 df가 N의 f 이하인 단위로만 센다. r2, 잡음 2만 개. "
                "값: (손 문장 상위 10 잡음, 자동 한국어 상위 10 잡음, 자동 한국어 적격 수)",
        "none": [4, 9, 5000], "f=0.05": [4, 9, 1404], "f=0.02": [4, 9, 377], "f=0.01": [4, 9, 68], "f=0.005": [6, 9, 26]}
    r2 = out["rank_rules"]["r2"]
    out["end_condition_met"] = {"r1_hand": r2["r1"]["hand"]["noise_in_top10"] <= 2,
                                "r1_i2_ko": r2["r1"]["i2_ko"]["noise_in_top10"] <= 2,
                                "a4_20_ko_all": r2["a4_20"]["ko"]["requests_with_noise_le_2"] == len(a20),
                                "a4_20_en_all": r2["a4_20"]["en"]["requests_with_noise_le_2"] == len(a20),
                                "r1_case_unchanged": all(v["first_slot_queue_313_L4"] and v["semaphore_folded_H1U"]
                                                         and v["create_all_folded_H2"] for v in flow.values())}
    write("measure_r6_scale.json", out)
    return out


# ------------------------------------------------------------------------------------------- I24 한 칸 요청의 자격
def i24():
    """08 I24: 서랍 자격 e1(설계, 맞은 칸 2 이상) 대 e2(자격 칸 수 = min(2, 요청 칸 수)). A4 20건과 잡음 2만 개(R-6 끝나는 조건)를
    같은 규칙으로 두 번 잰다. 되돌리는 규칙(돌리기 전에 정함, 사용자 결정): e2에서 상위 10 잡음이 e1보다 늘면 e1로 되돌린다.
    비교하는 잡음 수: R1 손 문장·자동 한국어의 상위 10 잡음, A4 20건 한국어·영어판의 평균 상위 10 잡음(r2, 2만 개)."""
    from afledger import config
    saved = config.ELIG_RULES
    res = {}
    try:
        for rule in sorted(("e1", "e2"), key=lambda r: r == saved):   # 기본 규칙을 마지막에 돌려 공용 출력 파일을 기본으로 남긴다
            config.ELIG_RULES = rule
            a, r = a4_20(), r6_scale()
            res[rule] = {"a4_20": a["summary"], "r6_scale_r2": {k: r["rank_rules"]["r2"][k] for k in ("r1", "a4_20")},
                         "r6_scale_real_only": {k: r["rank_rules"]["r2_real_only"][k] for k in ("r1", "a4_20")},
                         "end_condition_met": r["end_condition_met"], "r1_flow": r["r1_flow_r2"]}
    finally:
        config.ELIG_RULES = saved

    def noise(rule):
        x = res[rule]["r6_scale_r2"]
        return {"r1_hand": x["r1"]["hand"]["noise_in_top10"], "r1_i2_ko": x["r1"]["i2_ko"]["noise_in_top10"],
                "a4_20_ko_mean": x["a4_20"]["ko"]["mean_noise_in_top10"], "a4_20_en_mean": x["a4_20"]["en"]["mean_noise_in_top10"]}
    n1, n2 = noise("e1"), noise("e2")
    worse = [k for k in n1 if n2[k] > n1[k]]
    out = {"rule": i24.__doc__.split("\n")[1:4], "noise_top10": {"e1": n1, "e2": n2}, "worse_under_e2": worse,
           "revert_to_e1": bool(worse), "results": res}
    write("measure_i24.json", out)
    return out


# ------------------------------------------------------------------------------------------- I25 잡음 판정(I20 c)
def _r6_requests(L, p, s, qs, a20):
    """R-6 끝나는 조건의 요청들: R1 손 문장·자동 한국어, A4 20건 한국어·영어판. (이름, 요청 번호) 목록."""
    out = []
    for name, nd in (("R1.hand", s["needs"]), ("R1.i2_ko", intake_mod.write_needs(s["text"], s["requirements"]))):
        out.append((name, L.intake(p, request_key=name, rev=1, at=T0, text=s["text"], selected_part="s",
                                   requirements=s["requirements"], needs=nd)))
    for lang in ("ko", "en"):
        for q in (x for x in qs if x["id"] in a20):
            reqs = intake_mod.requirements_from_text(q[lang])
            out.append((f"{q['id']}.{lang}", L.intake(p, request_key=f"{q['id']}.{lang}", rev=1, at=T0, text=q[lang],
                                                      selected_part="s", requirements=reqs,
                                                      needs=intake_mod.write_needs(q[lang], reqs))))
    return out


def i25_collect(out_name="i25_pairs.json"):
    """08 I25 (I20의 c): 상위 10에 든 012 밖 실제 행(link-index)을 모은다. 판정할 목록을 out/i25_pairs.json에 쓴다.
    설정: r2, 현재 자격 규칙, 잡음 2만 개와 실제 잡음만. 같은 (요청, 관측) 쌍은 한 번만."""
    from drawer_load import preload_all_link_index, preload_synthetic
    s = studio("studio_rev1.json")
    qs = [json.loads(line) for line in (FIX / "af-res-012" / "queries.jsonl").read_text(encoding="utf-8").splitlines()]
    qtext = {q["id"]: q for q in qs}
    a20 = json.loads((OUT / "measure_a4_20.json").read_text(encoding="utf-8"))["queries"]
    import drawer_load
    pairs: dict = {}
    top10: dict = {}
    for cfg in ("noise_20k", "real_only"):
        L = Ledger()
        cat = preload_catalog(L)
        catset = set(cat.values())
        real = preload_all_link_index(L)
        if cfg == "noise_20k":
            preload_synthetic(L, NOISE_TOTAL - len(real))
        p = L.project("S")
        for name, req in _r6_requests(L, p, s, qs, a20):
            hits = L.search_drawer(p, req, T0, k=10, log=False)
            top10.setdefault(cfg, {})[name] = [
                {"kind": "catalog" if h["obs_id"] in catset else "real" if h["obs_id"] in real else "synthetic",
                 "url": L.obs(h["obs_id"])["url"]} for h in hits]
            for rank, h in enumerate(hits, 1):
                if h["obs_id"] in catset or h["obs_id"] not in real:
                    continue
                o = L.obs(h["obs_id"])
                key = f"{name}|{o['url']}"
                e = pairs.setdefault(key, {"request": name, "url": o["url"], "seen_in": {},
                                           "tags": [t["text"] for t in L.db.execute(
                                               "SELECT text FROM tag WHERE obs_id=? ORDER BY tag_id", (h["obs_id"],))],
                                           "problems": sorted({r["problem"] for r in link_index_rows() if r["url"] == o["url"]})})
                e["seen_in"][cfg] = rank
    reqtext = {"R1.hand": s["text"], "R1.i2_ko": s["text"]}
    for k, q in qtext.items():
        reqtext[f"{k}.ko"], reqtext[f"{k}.en"] = q["ko"], q["en"]
    out = {"rule": i25_collect.__doc__.split("\n")[1:3], "elig_rules": __import__("afledger").config.ELIG_RULES,
           "catalog_ko_slots": drawer_load.CATALOG_KO_SLOTS, "top10": top10,
           "requests": {n: reqtext[n] for n in sorted({e["request"] for e in pairs.values()})},
           "pairs": sorted(pairs.values(), key=lambda e: (e["request"], e["url"]))}
    write(out_name, out)
    return out


I25_RULE = [
    "판정 대상: i25_collect가 모은 (요청, 실제 행) 쌍 전부. 120쌍을 넘으면 요청마다 상위 순위부터 고르게 120쌍(고정 순서)만 판정하고 나머지는 잡음으로 둔다.",
    "등급(012 qrels와 같은 눈금): 2 = 요청의 조건 하나에 바로 쓰일 장치·원리, 1 = 같은 구체 문제의 쓸 만한 배경, 0 = 넓은 분야나 낱말만 겹침.",
    "잡음 = 등급 0과 판정하지 않은 실제 행, 그리고 합성 잡음 전부(합성은 따로 보고). 판정자: 이 세션의 모델(사람 판정 아님), 판정 근거 한 줄을 남긴다.",
]


def i25_sample(pairs_file="i25_pairs.json", cap=120) -> list[dict]:
    """I25_RULE 첫 줄의 표본: 요청 이름순으로 돌아가며 요청마다 가장 좋은 순위부터 한 쌍씩, cap쌍까지."""
    pairs = json.loads((OUT / pairs_file).read_text(encoding="utf-8"))["pairs"]
    by: dict = {}
    for x in pairs:
        by.setdefault(x["request"], []).append(x)
    for k in by:
        by[k].sort(key=lambda x: (min(x["seen_in"].values()), x["url"]))
    out, i = [], 0
    while len(out) < cap and any(i < len(v) for v in by.values()):
        for k in sorted(by):
            if i < len(by[k]) and len(out) < cap:
                out.append(by[k][i])
        i += 1
    return out


def i25_score(pairs_file="i25_pairs.json", judgments=FIX / "i25" / "judgments.tsv", out_name="measure_i25.json"):
    """08 I25: 판정으로 고친 잡음 수. 상위 10의 실제 행 가운데 등급 1·2는 잡음에서 뺀다. R1과 A4 20건 요청마다 다시 센다.
    잡음 2만 개(합성 포함)와 실제 잡음만 두 설정, 합성 잡음은 따로 센다."""
    import csv
    pairs = json.loads((OUT / pairs_file).read_text(encoding="utf-8"))
    grade = {}
    for r in csv.DictReader(open(judgments, encoding="utf-8"), delimiter="\t"):
        grade[(r["request"], r["url"])] = int(r["grade"])
    per = {}
    for cfg in ("noise_20k", "real_only"):
        tops = pairs["top10"][cfg]
        rows = {}
        for req, items in tops.items():
            synth = sum(1 for x in items if x["kind"] == "synthetic")
            real = [x for x in items if x["kind"] == "real"]
            judged_rel = sum(1 for x in real if grade.get((req, x["url"]), 0) >= 1)
            unjudged = sum(1 for x in real if (req, x["url"]) not in grade)
            rows[req] = {"noise_before": synth + len(real), "synthetic": synth, "real": len(real),
                         "real_judged_relevant": judged_rel, "real_unjudged": unjudged,
                         "noise_after": synth + len(real) - judged_rel, "real_noise_after": len(real) - judged_rel}
        a4 = {lang: [v for k, v in rows.items() if k.endswith("." + lang) and not k.startswith("R1.")] for lang in ("ko", "en")}
        per[cfg] = {"r1": {k: v for k, v in rows.items() if k.startswith("R1.")},
                    "a4_20": {lang: {"mean_noise_before": round(sum(x["noise_before"] for x in xs) / len(xs), 2),
                                     "mean_noise_after": round(sum(x["noise_after"] for x in xs) / len(xs), 2),
                                     "mean_real_noise_after": round(sum(x["real_noise_after"] for x in xs) / len(xs), 2),
                                     "le2_before": sum(1 for x in xs if x["noise_before"] <= 2),
                                     "le2_after": sum(1 for x in xs if x["noise_after"] <= 2),
                                     "le2_after_real_only_count": sum(1 for x in xs if x["real_noise_after"] <= 2)}
                              for lang, xs in a4.items()},
                    "rows": rows}
    dist = {}
    for g in grade.values():
        dist[g] = dist.get(g, 0) + 1
    out = {"rule": I25_RULE, "judged_pairs": len(grade), "grade_counts": dict(sorted(dist.items())),
           "elig_rules": pairs["elig_rules"], "catalog_ko_slots": pairs.get("catalog_ko_slots"), "by_config": per}
    write(out_name, out)
    return out



# ------------------------------------------------------------------------------------------- I26 012 한국어 칸별 꼬리표
def i26():
    """08 I26 (I20의 a): 012 자료집에 한국어 breaks_when 꼬리표(D-c 둘째 문장)를 더하기 전과 뒤. 채택 규칙(돌리기 전에 정함):
    실제 잡음만에서 A4 한국어의 판정 잡음 평균이 줄고, R1 손 문장·자동 한국어와 A4 영어판의 판정 잡음이 두 설정 어디서도 늘지 않고,
    R1 흐름의 완료 기준 2가 그대로면 기본으로 켠다. 판정은 I25의 120쌍을 그대로 쓰고 새로 든 실제 행은 판정 안 함(잡음)으로 센다."""
    import drawer_load
    saved = drawer_load.CATALOG_KO_SLOTS
    res = {}
    try:
        for flag in sorted((False, True), key=lambda f: f == saved):
            drawer_load.CATALOG_KO_SLOTS = flag
            key = "ko_slots" if flag else "before"
            a, r = a4_20(), r6_scale()
            i25_collect(out_name=f"i26_pairs_{key}.json")
            sc = i25_score(pairs_file=f"i26_pairs_{key}.json", out_name=f"measure_i26_{key}.json")
            res[key] = {"a4_20": a["summary"], "r6_scale_r2": {k: r["rank_rules"]["r2"][k] for k in ("r1", "a4_20")},
                        "r6_scale_real_only": {k: r["rank_rules"]["r2_real_only"][k] for k in ("r1", "a4_20")},
                        "r1_flow": r["r1_flow_r2"], "end_condition_met_unjudged": r["end_condition_met"],
                        "judged": {c: {"r1": {k: v["noise_after"] for k, v in x["r1"].items()}, "a4_20": x["a4_20"]}
                                   for c, x in sc["by_config"].items()}}
    finally:
        drawer_load.CATALOG_KO_SLOTS = saved

    def j(key, cfg):
        x = res[key]["judged"][cfg]
        return {"r1_hand": x["r1"]["R1.hand"], "r1_i2_ko": x["r1"]["R1.i2_ko"],
                "a4_ko": x["a4_20"]["ko"]["mean_noise_after"], "a4_en": x["a4_20"]["en"]["mean_noise_after"]}
    cmp = {cfg: {"before": j("before", cfg), "ko_slots": j("ko_slots", cfg)} for cfg in ("real_only", "noise_20k")}
    flow_ok = all(v["first_slot_queue_313_L4"] and v["semaphore_folded_H1U"] and v["create_all_folded_H2"]
                  for v in res["ko_slots"]["r1_flow"].values())
    worse = [f"{cfg}.{k}" for cfg in cmp for k in ("r1_hand", "r1_i2_ko", "a4_en")
             if cmp[cfg]["ko_slots"][k] > cmp[cfg]["before"][k]]
    adopt = cmp["real_only"]["ko_slots"]["a4_ko"] < cmp["real_only"]["before"]["a4_ko"] and not worse and flow_ok
    out = {"rule": i26.__doc__.split("\n")[1:4], "judged_noise": cmp, "worse": worse, "r1_flow_ok": flow_ok,
           "adopt": adopt, "results": res}
    write("measure_i26.json", out)
    return out


def i26_rank():
    """08 I26 둘째: 순위 r2(관측 전체 길이로 정규화) 대 r3(언어 칸별 길이로 정규화, BM25F식). 012 꼬리표는 I26 첫째에서 정한 대로.
    채택 규칙(돌리기 전에 정함): 실제 잡음만에서 A4 한국어 판정 잡음 평균이 줄고, R1 손 문장·자동 한국어와 A4 영어판의 판정 잡음이
    두 설정 어디서도 늘지 않고, A4 자료집만 회수율(한국어·영어판)이 줄지 않고, R1 흐름의 완료 기준 2가 그대로면 r3를 기본으로 한다."""
    from afledger import config
    saved = config.RANK_RULES
    res = {}
    try:
        for rank in sorted(("r2", "r3"), key=lambda r: r == saved):
            config.RANK_RULES = rank
            a, r = a4_20(), r6_scale()
            i25_collect(out_name=f"i26_pairs_{rank}.json")
            sc = i25_score(pairs_file=f"i26_pairs_{rank}.json", out_name=f"measure_i26_{rank}.json")
            res[rank] = {"a4_20": a["summary"], "r6_scale_cur": {k: r["rank_rules"]["r2"][k] for k in ("r1", "a4_20")},
                         "r6_scale_real_only": {k: r["rank_rules"]["r2_real_only"][k] for k in ("r1", "a4_20")},
                         "r1_flow": r["r1_flow_r2"],
                         "judged": {c: {"r1": {k: v["noise_after"] for k, v in x["r1"].items()}, "a4_20": x["a4_20"]}
                                    for c, x in sc["by_config"].items()}}
    finally:
        config.RANK_RULES = saved

    def j(rank, cfg):
        x = res[rank]["judged"][cfg]
        return {"r1_hand": x["r1"]["R1.hand"], "r1_i2_ko": x["r1"]["R1.i2_ko"],
                "a4_ko": x["a4_20"]["ko"]["mean_noise_after"], "a4_en": x["a4_20"]["en"]["mean_noise_after"]}
    cmp = {cfg: {r: j(r, cfg) for r in ("r2", "r3")} for cfg in ("real_only", "noise_20k")}
    rec = {r: {lang: res[r]["a4_20"]["catalog_only"][lang]["mean_recall12"] for lang in ("ko", "en")} for r in ("r2", "r3")}
    flow_ok = all(v["first_slot_queue_313_L4"] and v["semaphore_folded_H1U"] and v["create_all_folded_H2"]
                  for v in res["r3"]["r1_flow"].values())
    worse = [f"{cfg}.{k}" for cfg in cmp for k in ("r1_hand", "r1_i2_ko", "a4_en") if cmp[cfg]["r3"][k] > cmp[cfg]["r2"][k]]
    worse += [f"recall.{lang}" for lang in ("ko", "en") if rec["r3"][lang] < rec["r2"][lang]]
    adopt = cmp["real_only"]["r3"]["a4_ko"] < cmp["real_only"]["r2"]["a4_ko"] and not worse and flow_ok
    out = {"rule": i26_rank.__doc__.split("\n")[1:4], "judged_noise": cmp, "catalog_only_recall12": rec, "worse": worse,
           "r1_flow_ok": flow_ok, "adopt_r3": adopt, "results": res}
    write("measure_i26_rank.json", out)
    return out


def i26_combo():
    """08 I26 셋째(첫째·둘째 결과를 본 뒤, 돌리기 전에 정함): 012 한국어 꼬리표 + r3 대 지금(꼬리표 없음 + r2).
    첫째에서 한국어 꼬리표가 한국어는 낫게, 영어·R1 손 문장은 나쁘게 한 까닭이 관측 전체 길이 정규화(r2)라는 가설을 시험한다.
    채택 규칙: 첫째 규칙(실제 잡음만 A4 한국어 판정 잡음 감소, R1 둘·A4 영어판 판정 잡음이 두 설정 어디서도 늘지 않음, R1 흐름 그대로)
    + A4 자료집만 회수율(한국어·영어판)이 줄지 않으면 둘을 함께 기본으로 한다."""
    import drawer_load
    from afledger import config
    base = json.loads((OUT / "measure_i26.json").read_text(encoding="utf-8"))["results"]["before"]
    saved = (drawer_load.CATALOG_KO_SLOTS, config.RANK_RULES)
    try:
        drawer_load.CATALOG_KO_SLOTS, config.RANK_RULES = True, "r3"
        a, r = a4_20(), r6_scale()
        i25_collect(out_name="i26_pairs_ko_slots_r3.json")
        sc = i25_score(pairs_file="i26_pairs_ko_slots_r3.json", out_name="measure_i26_ko_slots_r3.json")
        new = {"a4_20": a["summary"], "r6_scale_cur": {k: r["rank_rules"]["r2"][k] for k in ("r1", "a4_20")},
               "r6_scale_real_only": {k: r["rank_rules"]["r2_real_only"][k] for k in ("r1", "a4_20")},
               "r1_flow": r["r1_flow_r2"],
               "judged": {c: {"r1": {k: v["noise_after"] for k, v in x["r1"].items()}, "a4_20": x["a4_20"]}
                          for c, x in sc["by_config"].items()}}
    finally:
        drawer_load.CATALOG_KO_SLOTS, config.RANK_RULES = saved
        a4_20(), r6_scale()          # 공용 출력 파일을 기본 설정으로 되돌린다

    def j(x, cfg):
        y = x["judged"][cfg]
        return {"r1_hand": y["r1"]["R1.hand"], "r1_i2_ko": y["r1"]["R1.i2_ko"],
                "a4_ko": y["a4_20"]["ko"]["mean_noise_after"], "a4_en": y["a4_20"]["en"]["mean_noise_after"]}
    cmp = {cfg: {"now": j(base, cfg), "ko_slots_r3": j(new, cfg)} for cfg in ("real_only", "noise_20k")}
    rec = {k: {lang: x["a4_20"]["catalog_only"][lang]["mean_recall12"] for lang in ("ko", "en")}
           for k, x in (("now", base), ("ko_slots_r3", new))}
    flow_ok = all(v["first_slot_queue_313_L4"] and v["semaphore_folded_H1U"] and v["create_all_folded_H2"]
                  for v in new["r1_flow"].values())
    worse = [f"{cfg}.{k}" for cfg in cmp for k in ("r1_hand", "r1_i2_ko", "a4_en")
             if cmp[cfg]["ko_slots_r3"][k] > cmp[cfg]["now"][k]]
    worse += [f"recall.{lang}" for lang in ("ko", "en") if rec["ko_slots_r3"][lang] < rec["now"][lang]]
    adopt = cmp["real_only"]["ko_slots_r3"]["a4_ko"] < cmp["real_only"]["now"]["a4_ko"] and not worse and flow_ok
    out = {"rule": i26_combo.__doc__.split("\n")[1:5], "judged_noise": cmp, "catalog_only_recall12": rec, "worse": worse,
           "r1_flow_ok": flow_ok, "adopt": adopt, "result": new}
    write("measure_i26_combo.json", out)
    return out


# ------------------------------------------------------------------------------------------- I27 실제 행 2만 개
def i27(rank=None, out_name="measure_i27.json"):
    """08 I27: R-6 잡음 2만 개를 opensource catalog p5 대상(012 주소·012 보강 회차 기록을 뺀 것, 키 SHA-1 순 앞 2만 개)으로 채운다.
    정한 것(돌리기 전): 이 설정을 R-6 잡음 2만 개의 기본 설정으로 쓰고 합성 잡음은 비교로만 둔다. 칸 대응은 drawer_load.P5_SLOT_MAP.
    012 쪽 꼬리표는 지금 기본(D-b 영어·한국어 summary) 그대로다. 잡음은 셋으로 센다: 그대로(012 밖 전부), I25 판정을 같은 (요청, 주소)에
    이어 씀(판정 안 한 것은 잡음), 판정 안 한 것에 I25 관련 비율을 적용한 추정. 사례 결과는 R1 흐름 완료 기준 2."""
    import csv
    import run_r1
    from afledger import config
    from drawer_load import preload_catalog_p5
    rank = rank or config.RANK_RULES
    s = studio("studio_rev1.json")
    qs = [json.loads(line) for line in (FIX / "af-res-012" / "queries.jsonl").read_text(encoding="utf-8").splitlines()]
    qrels: dict[str, dict] = {}
    for r in csv.DictReader(open(FIX / "af-res-012" / "qrels.tsv", encoding="utf-8"), delimiter="\t"):
        if r["grade"].isdigit():
            qrels.setdefault(r["query_id"], {})[r["entry_id"]] = int(r["grade"])
    a20 = json.loads((OUT / "measure_a4_20.json").read_text(encoding="utf-8"))["queries"]
    grade = {(r["request"], r["url"]): int(r["grade"]) for r in
             csv.DictReader(open(FIX / "i25" / "judgments.tsv", encoding="utf-8"), delimiter="\t")}
    rate = sum(1 for g in grade.values() if g >= 1) / len(grade)
    L = Ledger()
    L.rank_rules = rank
    cat = preload_catalog(L)
    catset = set(cat.values())
    inv = {v: k for k, v in cat.items()}
    noise = preload_catalog_p5(L)
    p = L.project("S")
    per, top10 = {}, {}
    for name, req in _r6_requests(L, p, s, qs, a20):
        hits = L.search_drawer(p, req, T0, k=5000 if name.startswith("R1") else 12, log=False)
        ids = [inv.get(h["obs_id"]) for h in hits]
        top = [h for h in hits[:10]]
        nz = [L.obs(h["obs_id"])["url"] for h in top if h["obs_id"] not in catset]
        rel_judged = sum(1 for u in nz if grade.get((name, u), 0) >= 1)
        unj = sum(1 for u in nz if (name, u) not in grade)
        top10[name] = [{"kind": "catalog" if h["obs_id"] in catset else "p5", "url": L.obs(h["obs_id"])["url"],
                        "key": noise[h["obs_id"]]["key"] if h["obs_id"] in noise else inv.get(h["obs_id"])} for h in top]
        row = {"noise_raw": len(nz), "noise_judged": len(nz) - rel_judged, "unjudged": unj,
               "noise_estimate": round(len(nz) - rel_judged - unj * rate, 2)}
        if name.startswith("R1"):
            row |= {"asyncio_queue": ids.index("asyncio-queue") + 1 if "asyncio-queue" in ids else None,
                    "asyncio_semaphore": ids.index("asyncio-semaphore") + 1 if "asyncio-semaphore" in ids else None,
                    "eligible": sum(h["eligible"] for h in hits)}
        else:
            q = name.rsplit(".", 1)[0]
            rel = {e for e, g in qrels[q].items() if g >= 1}
            row |= {"recall12": round(sum(1 for e in rel if e in ids[:12]) / len(rel), 3),
                    "grade2_in_top12": any(qrels[q].get(e) == 2 for e in ids[:12])}
        per[name] = row
    a4 = {}
    for lang in ("ko", "en"):
        xs = [v for k, v in per.items() if k.endswith("." + lang) and not k.startswith("R1")]
        a4[lang] = {m: round(sum(x[m] for x in xs) / len(xs), 2) for m in ("noise_raw", "noise_judged", "noise_estimate", "recall12")}
        a4[lang] |= {f"le2_{m}": sum(1 for x in xs if x[m] <= 2) for m in ("noise_raw", "noise_judged", "noise_estimate")}
        a4[lang]["grade2_in_top12"] = sum(x["grade2_in_top12"] for x in xs)
    flow = {}
    for nn in ("studio", "i1"):
        r = run_r1.run("replay", needs=nn, noise=False, noise_loader=lambda L_: list(preload_catalog_p5(L_)))
        r.pop("_ledger")
        folded = {f["condition"]: f["reason"] for f in r["rev1"]["answer"]["folded"]}
        slot1 = next((x["sentence"] for x in r["rev1"]["answer"]["slots"] if x["kind"] == "direct"), "")
        flow["hand" if nn == "studio" else "i2_ko"] = {
            "first_slot_queue_313_L4": "/blob/v3.13." in slot1 and "queues.py#L" in slot1,
            "semaphore_folded_H1U": "H1 U" in folded.get("대기 8을 대기열 길이로 지키는가", ""),
            "create_all_folded_H2": "H2 위반" in folded.get("입력마다 작업 객체를 미리 만드는가", ""),
            "drawer_symbols": [(x["name"], x.get("drawer_rank"), x.get("skipped")) for x in
                               r["rev1"]["fresh_direct"]["drawer_symbols_resolved"]],
            "external_attempts": r["rev1"]["budget"]["external_attempts"]}
    commit = json.loads((FIX / "catalog-p5" / "SOURCES.json").read_text(encoding="utf-8"))["commit"]
    out = {"rule": i27.__doc__.split("\n")[1:5], "catalog_commit": commit, "rank_rules": rank,
           "noise_observations": len(noise), "i25_relevant_rate": round(rate, 3),
           "r1": {k: v for k, v in per.items() if k.startswith("R1")}, "a4_20": a4, "r1_flow": flow,
           "end_condition_met": {m: {"r1_hand": per["R1.hand"][m] <= 2, "r1_i2_ko": per["R1.i2_ko"][m] <= 2,
                                     "a4_ko_all": a4["ko"][f"le2_{m}"] == len(a20), "a4_en_all": a4["en"][f"le2_{m}"] == len(a20)}
                                 for m in ("noise_raw", "noise_judged", "noise_estimate")},
           "per_request": per, "top10": top10}
    write(out_name, out)
    return out



I27_JUDGE_RULE = [
    "판정 대상(판정 전에 정함): measure_i27.json 상위 10의 catalog 행 가운데 I25에서 판정하지 않은 (요청, 주소) 쌍.",
    "R1 두 요청의 쌍은 전부, A4 요청은 이름순으로 돌아가며 요청마다 가장 좋은 순위부터 한 쌍씩, 합쳐 80쌍까지.",
    "등급과 판정자는 I25_RULE과 같다(이 세션의 모델, 꼬리표만 보고, 원문은 열지 않음). 근거는 대상의 what·principle·scene·쓸모 문장.",
]


def i27_sample(cap=80) -> list[dict]:
    import csv
    o = json.loads((OUT / "measure_i27.json").read_text(encoding="utf-8"))
    judged = {(r["request"], r["url"]) for r in csv.DictReader(open(FIX / "i25" / "judgments.tsv", encoding="utf-8"), delimiter="\t")}
    by: dict = {}
    for req, items in o["top10"].items():
        for rank, x in enumerate(items, 1):
            if x["kind"] == "p5" and (req, x["url"]) not in judged:
                by.setdefault(req, []).append({"request": req, "url": x["url"], "key": x["key"], "rank": rank})
    out = [x for k in sorted(by) if k.startswith("R1.") for x in by[k]]
    a4 = sorted(k for k in by if not k.startswith("R1."))
    i = 0
    while len(out) < cap and any(i < len(by[k]) for k in a4):
        for k in a4:
            if i < len(by[k]) and len(out) < cap:
                out.append(by[k][i])
        i += 1
    return out


def i27_score(src="measure_i27.json", out_name="measure_i27_judged.json"):
    """08 I27 판정 뒤: 실제 행 2만 개 상위 10을 I25·I27 판정을 합쳐 다시 센다. 판정 안 한 행은 잡음, 추정은 두 판정의 관련 비율로."""
    import csv
    o = json.loads((OUT / src).read_text(encoding="utf-8"))
    grade = {}
    for f in (FIX / "i25" / "judgments.tsv", FIX / "i27" / "judgments.tsv"):
        for r in csv.DictReader(open(f, encoding="utf-8"), delimiter="\t"):
            grade[(r["request"], r["url"])] = int(r["grade"])
    rate = sum(1 for g in grade.values() if g >= 1) / len(grade)
    per = {}
    for req, items in o["top10"].items():
        nz = [x["url"] for x in items if x["kind"] != "catalog"]
        rel = sum(1 for u in nz if grade.get((req, u), 0) >= 1)
        unj = sum(1 for u in nz if (req, u) not in grade)
        per[req] = {"noise_raw": len(nz), "noise_judged": len(nz) - rel, "unjudged": unj,
                    "noise_estimate": round(len(nz) - rel - unj * rate, 2)}
    a4 = {}
    for lang in ("ko", "en"):
        xs = [v for k, v in per.items() if k.endswith("." + lang) and not k.startswith("R1")]
        a4[lang] = {m: round(sum(x[m] for x in xs) / len(xs), 2) for m in ("noise_raw", "noise_judged", "unjudged", "noise_estimate")}
        a4[lang] |= {f"le2_{m}": sum(1 for x in xs if x[m] <= 2) for m in ("noise_raw", "noise_judged", "noise_estimate")}
    out = {"src": src, "judged_pairs": len(grade), "relevant_rate": round(rate, 3),
           "r1": {k: v for k, v in per.items() if k.startswith("R1")}, "a4_20": a4, "per_request": per}
    write(out_name, out)
    return out

# ------------------------------------------------------------------------------------------- I28 RRF
def i28():
    """08 I28: 서랍 순위 r4(검색기 = (필요 칸, 언어), 검색기 안은 IDF 합, RRF k=60으로 결합) 대 r2.
    채택 규칙(돌리기 전에 정함): 실제 행 2만 개(I27)에서 A4 한국어 판정 잡음(I25 판정 이어 씀, 판정 안 한 것은 잡음) 평균이 줄고,
    R1 손 문장·자동 한국어·A4 영어판의 판정 잡음이 실제 행 2만 개와 link-index 실제 잡음만(I25) 어디서도 늘지 않고,
    A4 자료집만 회수율(한국어·영어판)이 줄지 않고, 실제 행 2만 개에서 R1 흐름의 완료 기준 2가 그대로면 r4를 기본으로 한다."""
    from afledger import config
    saved = config.RANK_RULES
    res = {}
    try:
        for rank in sorted(("r2", "r4"), key=lambda r: r == saved):
            config.RANK_RULES = rank
            a = a4_20()
            c = i27(rank, out_name=f"measure_i28_catalog_{rank}.json")
            i25_collect(out_name=f"i28_pairs_{rank}.json")
            sc = i25_score(pairs_file=f"i28_pairs_{rank}.json", out_name=f"measure_i28_linkindex_{rank}.json")
            li = sc["by_config"]["real_only"]
            res[rank] = {"recall12_catalog_only": {lang: a["summary"]["catalog_only"][lang]["mean_recall12"] for lang in ("ko", "en")},
                         "catalog20k": {"r1_hand": c["r1"]["R1.hand"]["noise_judged"], "r1_i2_ko": c["r1"]["R1.i2_ko"]["noise_judged"],
                                        "a4_ko": c["a4_20"]["ko"]["noise_judged"], "a4_en": c["a4_20"]["en"]["noise_judged"],
                                        "a4_ko_estimate": c["a4_20"]["ko"]["noise_estimate"],
                                        "a4_en_estimate": c["a4_20"]["en"]["noise_estimate"],
                                        "le2_judged": {l: c["a4_20"][l]["le2_noise_judged"] for l in ("ko", "en")}},
                         "linkindex_real": {"r1_hand": li["r1"]["R1.hand"]["noise_after"], "r1_i2_ko": li["r1"]["R1.i2_ko"]["noise_after"],
                                            "a4_ko": li["a4_20"]["ko"]["mean_noise_after"], "a4_en": li["a4_20"]["en"]["mean_noise_after"]},
                         "r1_flow": c["r1_flow"],
                         "r1_ranks": {k: (v["asyncio_queue"], v["asyncio_semaphore"]) for k, v in c["r1"].items()}}
    finally:
        config.RANK_RULES = saved
    a, b = res["r2"], res["r4"]
    flow_ok = all(v["first_slot_queue_313_L4"] and v["semaphore_folded_H1U"] and v["create_all_folded_H2"]
                  for v in b["r1_flow"].values())
    worse = [f"{cfg}.{k}" for cfg in ("catalog20k", "linkindex_real") for k in ("r1_hand", "r1_i2_ko", "a4_en")
             if b[cfg][k] > a[cfg][k]]
    worse += [f"recall.{l}" for l in ("ko", "en") if b["recall12_catalog_only"][l] < a["recall12_catalog_only"][l]]
    adopt = b["catalog20k"]["a4_ko"] < a["catalog20k"]["a4_ko"] and not worse and flow_ok
    out = {"rule": i28.__doc__.split("\n")[1:5], "results": res, "worse": worse, "r1_flow_ok": flow_ok, "adopt_r4": adopt}
    write("measure_i28.json", out)
    return out


# ------------------------------------------------------------------------------------------- I29 한 문장 요청 되묻기
def i29():
    """08 I29: 한 문장 요청(012의 부분 질의)에 한 번 되묻기(intake.reask_questions: 받는 것, 깨지면 안 되는 것) 대 그대로.
    대리 답(돌리기 전에 정함): 같은 문제의 전체 질의(.w)를 접수 규칙으로 나눈 칸에서 input은 "받는 것" 답, keeps·breaks_when은
    "깨지면 안 되는 것" 답이다. 부분 질의 문장과 같은 문장은 답에서 뺀다(복사 금지). 전체 질의 그대로는 위쪽 한계로 같이 잰다.
    대상: A4 20건 가운데 부분 질의(.1·.2) 16건, 한국어·영어판. 잡음은 실제 행 2만 개(I27), 순위는 지금 기본.
    권하는 규칙: 한국어·영어판 모두 적격 0 요청이 줄고, 자료집만 회수율 평균과 등급 2 상위 12 수가 줄지 않고, 실제 행 2만 개의 판정 잡음
    평균이 늘지 않으면 접수 설계에 되묻기를 권한다. 새 검색 맡기기(c)는 직접 갈래가 CPython 소스 검색뿐이라 012 질의에는 잴 수 없다."""
    import csv
    from drawer_load import preload_catalog_p5
    qs = {json.loads(x)["id"]: json.loads(x) for x in (FIX / "af-res-012" / "queries.jsonl").read_text(encoding="utf-8").splitlines()}
    qrels: dict[str, dict] = {}
    for r in csv.DictReader(open(FIX / "af-res-012" / "qrels.tsv", encoding="utf-8"), delimiter="\t"):
        if r["grade"].isdigit():
            qrels.setdefault(r["query_id"], {})[r["entry_id"]] = int(r["grade"])
    a20 = json.loads((OUT / "measure_a4_20.json").read_text(encoding="utf-8"))["queries"]
    parts = [q for q in a20 if not q.endswith(".w")]
    grade = {(r["request"], r["url"]): int(r["grade"]) for r in
             csv.DictReader(open(FIX / "i25" / "judgments.tsv", encoding="utf-8"), delimiter="\t")}

    def needs_for(qid, lang, arm):
        text = qs[qid][lang]
        nd = intake_mod.write_needs(text, intake_mod.requirements_from_text(text))
        if arm == "part":
            return nd, []
        whole = qs[qid.split(".")[0] + ".w"][lang]
        wn = intake_mod.write_needs(whole, intake_mod.requirements_from_text(whole))
        if arm == "whole":
            return wn, []
        asked = intake_mod.reask_questions(nd, lang)
        mine = {s_.strip() for n in nd for s_ in intake_mod._sentences(n["text"])}
        ans = {}
        for a in asked:
            src = ("input",) if a["slot"] == "input" else ("keeps", "breaks_when")
            ans[a["slot"]] = " ".join(s_ for n in wn if n["slot"] in src for s_ in intake_mod._sentences(n["text"])
                                      if s_.strip() not in mine)
        return intake_mod.apply_reask(nd, ans), asked

    out = {"rule": i29.__doc__.split("\n")[1:7], "parts": parts, "arms": {}}
    for noise in ("catalog_only", "catalog20k"):
        L = Ledger()
        cat = preload_catalog(L)
        catset = set(cat.values())
        inv = {v: k for k, v in cat.items()}
        if noise == "catalog20k":
            preload_catalog_p5(L)
        p = L.project("Q")
        for arm in ("part", "reask", "whole"):
            for lang in ("ko", "en"):
                rows = []
                for qid in parts:
                    nd, asked = needs_for(qid, lang, arm)
                    req = L.intake(p, request_key=f"{qid}.{lang}.{arm}", rev=1, at=T0, text=qs[qid][lang], selected_part="s",
                                   requirements=[], needs=nd)
                    hits = L.search_drawer(p, req, T0, k=12, log=False)
                    ids = [inv.get(h["obs_id"]) for h in hits]
                    rel = {e for e, g in qrels[qid].items() if g >= 1}
                    nz = [L.obs(h["obs_id"])["url"] for h in hits[:10] if h["obs_id"] not in catset]
                    rows.append({"id": qid, "slots": sorted({n["slot"] for n in nd}), "asked": len(asked),
                                 "eligible": sum(h["eligible"] for h in hits),
                                 "recall12": sum(1 for e in rel if e in ids) / len(rel),
                                 "grade2": any(qrels[qid].get(e) == 2 for e in ids),
                                 "noise_judged": len(nz) - sum(1 for u in nz if grade.get((f"{qid}.{lang}", u), 0) >= 1)})
                out["arms"].setdefault(noise, {}).setdefault(arm, {})[lang] = {
                    "zero_eligible_in_top12": sum(1 for r in rows if r["eligible"] == 0),
                    "mean_recall12": round(sum(r["recall12"] for r in rows) / len(rows), 3),
                    "grade2_in_top12": sum(r["grade2"] for r in rows),
                    "mean_noise_judged": round(sum(r["noise_judged"] for r in rows) / len(rows), 2),
                    "asked_requests": sum(1 for r in rows if r["asked"]), "rows": rows}
    A = out["arms"]
    ok = {}
    for lang in ("ko", "en"):
        c0, c1 = A["catalog_only"]["part"][lang], A["catalog_only"]["reask"][lang]
        n0, n1 = A["catalog20k"]["part"][lang], A["catalog20k"]["reask"][lang]
        ok[lang] = (n1["zero_eligible_in_top12"] < n0["zero_eligible_in_top12"] and c1["mean_recall12"] >= c0["mean_recall12"]
                    and c1["grade2_in_top12"] >= c0["grade2_in_top12"] and n1["mean_noise_judged"] <= n0["mean_noise_judged"])
    out["recommend_reask"] = all(ok.values())
    out["by_lang"] = ok
    write("measure_i29.json", out)
    return out


# ------------------------------------------------------------------------------------------- I30·I31 공용
def _judgments() -> dict:
    import csv
    g = {}
    for f in (FIX / "i25" / "judgments.tsv", FIX / "i27" / "judgments.tsv", FIX / "i32" / "judgments.tsv",
              FIX / "i33" / "judgments.tsv"):
        if not f.exists():
            continue
        for r in csv.DictReader(open(f, encoding="utf-8"), delimiter="\t"):
            g[(r["request"], r["url"])] = int(r["grade"])
    return g


def _judge_top10(top10: dict) -> dict:
    """상위 10 잡음을 두 값으로 센다(08 I30 사용자 결정 3): judged = 판정 안 한 실제 행을 잡음으로 셈, judged_only = 판정 안 한
    실제 행을 빼고 셈(판정 0인 실제 행 + 합성). 판정은 I25·I27을 합친 것. 요청별 값과 R1·A4 요약을 돌려준다."""
    g = _judgments()
    per = {}
    for req, items in top10.items():
        nz = [x for x in items if x["kind"] != "catalog"]
        syn = sum(1 for x in nz if x["kind"] == "synthetic")
        real = [x["url"] for x in nz if x["kind"] != "synthetic"]
        rel = sum(1 for u in real if g.get((req, u), 0) >= 1)
        unj = sum(1 for u in real if (req, u) not in g)
        per[req] = {"raw": len(nz), "synthetic": syn, "unjudged": unj, "judged": len(nz) - rel, "judged_only": len(nz) - rel - unj}
    a4 = {}
    for lang in ("ko", "en"):
        xs = [v for k, v in per.items() if k.endswith("." + lang) and not k.startswith("R1")]
        a4[lang] = {m: round(sum(x[m] for x in xs) / len(xs), 2) for m in ("raw", "unjudged", "judged", "judged_only")}
        a4[lang] |= {f"le2_{m}": sum(1 for x in xs if x[m] <= 2) for m in ("raw", "judged", "judged_only")}
    return {"r1": {k: v for k, v in per.items() if k.startswith("R1")}, "a4_20": a4, "per_request": per}


def _setting_eval(tag: str) -> dict:
    """지금 설정(012 꼬리표, 순위 규칙)으로 A4 자료집만 회수율, 실제 행 2만 개(R1 흐름 포함), link-index 실제 잡음만을 잰다."""
    a = a4_20()
    c = i27(out_name=f"measure_{tag}_catalog.json")
    li = i25_collect(out_name=f"{tag}_linkindex_pairs.json")
    return {"recall12_catalog_only": {l: a["summary"]["catalog_only"][l]["mean_recall12"] for l in ("ko", "en")},
            "grade2_catalog_only": {l: a["summary"]["catalog_only"][l]["grade2_in_top12"] for l in ("ko", "en")},
            "zero_eligible_catalog_only": {l: a["summary"]["catalog_only"][l]["zero_eligible"] for l in ("ko", "en")},
            "catalog20k": _judge_top10(c["top10"]), "linkindex_real": _judge_top10(li["top10"]["real_only"]),
            "r1_flow": c["r1_flow"], "r1_ranks": {k: (v["asyncio_queue"], v["asyncio_semaphore"]) for k, v in c["r1"].items()}}


def _adopt(base: dict, new: dict) -> tuple[bool, list, dict]:
    """I30·I31 채택 규칙(돌리기 전에 정함): 실제 행 2만 개에서 A4 한국어 judged 평균이 줄고, R1 손 문장·자동 한국어·A4 영어판의
    judged가 실제 행 2만 개와 link-index 실제 잡음 어디서도 늘지 않고, A4 자료집만 회수율(한국어·영어판)이 줄지 않고, 실제 행
    2만 개에서 R1 흐름 완료 기준 2가 그대로면 채택한다. judged_only는 보고만 한다."""
    def j(x, cfg):
        y = x[cfg]
        return {"r1_hand": y["r1"]["R1.hand"]["judged"], "r1_i2_ko": y["r1"]["R1.i2_ko"]["judged"],
                "a4_ko": y["a4_20"]["ko"]["judged"], "a4_en": y["a4_20"]["en"]["judged"]}
    cmp = {cfg: {"base": j(base, cfg), "new": j(new, cfg)} for cfg in ("catalog20k", "linkindex_real")}
    worse = [f"{cfg}.{k}" for cfg in cmp for k in ("r1_hand", "r1_i2_ko", "a4_en") if cmp[cfg]["new"][k] > cmp[cfg]["base"][k]]
    worse += [f"recall.{l}" for l in ("ko", "en") if new["recall12_catalog_only"][l] < base["recall12_catalog_only"][l]]
    flow_ok = all(v["first_slot_queue_313_L4"] and v["semaphore_folded_H1U"] and v["create_all_folded_H2"]
                  for v in new["r1_flow"].values())
    ok = cmp["catalog20k"]["new"]["a4_ko"] < cmp["catalog20k"]["base"]["a4_ko"] and not worse and flow_ok
    return ok, worse, cmp


def i30():
    """08 I30: 012 꼬리표를 opensource Q3 보강 회차 p5 기록(AR2·BR2·CR2, fixtures/af-res-012-p5)으로 켬 대 끔(D-b만), 순위 r2.
    켬 = D-b 영어·한국어 summary + p5 기록을 잡음 쪽과 같은 칸 대응(P5_SLOT_MAP)으로. 잡음은 실제 행 2만 개(I27, catalog 55c51d4)와
    link-index 실제 잡음만. 채택 규칙은 _adopt(돌리기 전에 정함). 켜면 drawer_load.CATALOG_P5_TAGS를 기본으로 바꾼다."""
    import drawer_load
    saved = drawer_load.CATALOG_P5_TAGS
    res = {}
    try:
        for flag in sorted((False, True), key=lambda f: f == saved):
            drawer_load.CATALOG_P5_TAGS = flag
            res["p5" if flag else "db_only"] = _setting_eval("i30_p5" if flag else "i30_db_only")
    finally:
        drawer_load.CATALOG_P5_TAGS = saved
    ok, worse, cmp = _adopt(res["db_only"], res["p5"])
    out = {"rule": [i30.__doc__.split("\n")[1:4], _adopt.__doc__.split("\n")[0:4]], "judged": cmp, "worse": worse,
           "adopt_p5": ok, "results": res}
    write("measure_i30.json", out)
    return out


def i31():
    """08 I31: 순위 r5(검색기 = (필요 칸, 언어), 검색기 안은 r2처럼 IDF 합을 관측 길이로 보정, RRF k=60) 대 r2.
    012 꼬리표는 I30에서 정한 기본. 잡음과 채택 규칙은 I30과 같다(_adopt). 채택하면 RANK_RULES를 r5로 바꾼다."""
    from afledger import config
    saved = config.RANK_RULES
    res = {}
    try:
        for rank in sorted(("r2", "r5"), key=lambda r: r == saved):
            config.RANK_RULES = rank
            res[rank] = _setting_eval(f"i31_{rank}")
    finally:
        config.RANK_RULES = saved
    ok, worse, cmp = _adopt(res["r2"], res["r5"])
    import drawer_load
    out = {"rule": [i31.__doc__.split("\n")[1:3], _adopt.__doc__.split("\n")[0:4]], "catalog_p5_tags": drawer_load.CATALOG_P5_TAGS,
           "judged": cmp, "worse": worse, "adopt_r5": ok, "results": res}
    write("measure_i31.json", out)
    return out


# ------------------------------------------------------------------------------------------- I32 판정 풀과 B 조건
I32_SETTINGS = {   # 이름: (012 p5 꼬리표, 순위 규칙, 상위 10 파일 접두)
    "r2": (False, "r2", "i31_r2"),
    "r5": (False, "r5", "i31_r5"),
    "p5_r2": (True, "r2", "i30_p5"),
    "p5_r5": (True, "r5", "i32_p5_r5"),
}


def i32_run_both():
    """08 I32: 네 번째 설정(012 p5 꼬리표 켬 + r5)의 상위 10을 만든다. 나머지 셋은 I30·I31의 출력을 쓴다."""
    import drawer_load
    from afledger import config
    saved = (drawer_load.CATALOG_P5_TAGS, config.RANK_RULES)
    try:
        drawer_load.CATALOG_P5_TAGS, config.RANK_RULES = True, "r5"
        r = _setting_eval("i32_p5_r5")
    finally:
        drawer_load.CATALOG_P5_TAGS, config.RANK_RULES = saved
        a4_20()                      # 공용 출력 파일을 기본 설정으로 되돌린다
    write("measure_i32_p5_r5.json", r)
    return r


def _i32_top10(name: str, cfg: str) -> dict:
    tag = (I33_SETTINGS if name in globals().get("I33_SETTINGS", {}) else I32_SETTINGS)[name][2]
    if cfg == "catalog20k":
        return json.loads((OUT / f"measure_{tag}_catalog.json").read_text(encoding="utf-8"))["top10"]
    return json.loads((OUT / f"{tag}_linkindex_pairs.json").read_text(encoding="utf-8"))["top10"]["real_only"]


def i32_pool(cfgs=("catalog20k",), names=None) -> list[dict]:
    """판정 풀: 네 설정 상위 10의 합집합 가운데 아직 판정하지 않은 실제 행 (요청, 주소) 쌍. 요청·주소 순으로 고정."""
    g = _judgments()
    names = names or [n for n in I32_SETTINGS if (OUT / (f"measure_{I32_SETTINGS[n][2]}_catalog.json")).exists()]
    pool = {}
    for cfg in cfgs:
        for n in names:
            for req, items in _i32_top10(n, cfg).items():
                for x in items:
                    if x["kind"] in ("p5", "real") and (req, x["url"]) not in g:
                        pool.setdefault((req, x["url"]), {"request": req, "url": x["url"], "key": x.get("key"), "cfg": cfg})
    return [pool[k] for k in sorted(pool)]


def i32_decide():
    """08 I32 B 조건 비교(돌리기 전에 정함, 사용자 결정 2026-11-27 셋째).
    요청마다 B 조건: 상위 10의 판정한 잡음(등급 0인 실제 행 + 합성) 2개 이하이고 판정 안 한 실제 행 0개.
    요청은 R1 손 문장·자동 한국어와 A4 20건 한국어·영어판(42개), 잡음 설정은 실제 행 2만 개(주)와 link-index 실제 잡음(보조).
    기본값 고르기: (1) 실제 행 2만 개에서 R1 흐름 완료 기준 2가 성립하지 않는 설정은 뺀다. (2) 실제 행 2만 개에서 B를 만족한 요청 수가
    가장 많은 설정. (3) 같으면 link-index에서 B를 만족한 요청 수. (4) 같으면 A4 자료집만 회수율(한국어+영어판) 합. (5) 같으면 바꾸는 것이
    적은 쪽(r2 < r5, 꼬리표 끔 < 켬). 판정 안 한 행이 남은 설정·요청은 B를 만족하지 않은 것으로 센다."""
    res = {}
    for n in I32_SETTINGS:
        tag = I32_SETTINGS[n][2]
        ev = json.loads((OUT / (f"measure_i32_p5_r5.json" if n == "p5_r5" else
                                ("measure_i31.json" if n in ("r2", "r5") else "measure_i30.json"))).read_text(encoding="utf-8"))
        ev = ev if n == "p5_r5" else ev["results"]["p5" if n == "p5_r2" else n]
        row = {"recall12_catalog_only": ev["recall12_catalog_only"], "grade2_catalog_only": ev["grade2_catalog_only"],
               "r1_flow_ok": all(v["first_slot_queue_313_L4"] and v["semaphore_folded_H1U"] and v["create_all_folded_H2"]
                                 for v in ev["r1_flow"].values()), "r1_ranks": ev["r1_ranks"]}
        for cfg in ("catalog20k", "linkindex_real"):
            j = _judge_top10(_i32_top10(n, cfg))
            per = j["per_request"]
            b = {k: v["judged_only"] <= 2 and v["unjudged"] == 0 for k, v in per.items()}
            row[cfg] = {"B_met": sum(b.values()), "requests": len(b), "unjudged_total": sum(v["unjudged"] for v in per.values()),
                        "B_by_request": b, "r1": j["r1"], "a4_20": j["a4_20"],
                        "B_a4": {l: sum(1 for k, v in b.items() if v and k.endswith("." + l) and not k.startswith("R1"))
                                 for l in ("ko", "en")}}
        res[n] = row
    order = ["r2", "r5", "p5_r2", "p5_r5"]   # (5)의 단순한 순서
    cand = [n for n in order if res[n]["r1_flow_ok"]]
    best = sorted(cand, key=lambda n: (-res[n]["catalog20k"]["B_met"], -res[n]["linkindex_real"]["B_met"],
                                       -sum(res[n]["recall12_catalog_only"].values()), order.index(n)))
    out = {"rule": i32_decide.__doc__.split("\n")[1:7], "judged_pairs": len(_judgments()), "results": res,
           "ranking": best, "chosen": best[0] if best else None}
    write("measure_i32.json", out)
    return out


I32_HUMAN_SEED = 20261127   # 사람 확인 표본의 씨앗(판정 전에 정함)


def i32_human_sample(n=30):
    """08 I32: 사람이 확인할 수 있게 I32 판정에서 무작위 n쌍을 뽑아 fixtures/i32/human_check.tsv로 남긴다.
    씨앗은 I32_HUMAN_SEED. 칸: 번호, 요청, 요청 문장(영어판·R1 요약), 주소, 행의 꼬리표 문장, 모델 등급·근거, 사람 등급·메모(빈칸)."""
    import csv
    import gzip
    import random
    rows = list(csv.DictReader(open(FIX / "i32" / "judgments.tsv", encoding="utf-8"), delimiter="\t"))
    pick = sorted(random.Random(I32_HUMAN_SEED).sample(range(len(rows)), n))
    qs = {json.loads(x)["id"]: json.loads(x) for x in (FIX / "af-res-012" / "queries.jsonl").read_text(encoding="utf-8").splitlines()}
    cat = {}
    with gzip.open(FIX / "catalog-p5" / "targets.jsonl.gz", "rt", encoding="utf-8") as fh:
        for line in fh:
            t = json.loads(line)
            cat[t["key"]] = t
    li = {}
    for f in sorted(OUT.glob("*linkindex_pairs.json")) + [OUT / "i25_pairs.json"]:
        for x in json.loads(f.read_text(encoding="utf-8"))["pairs"]:
            li.setdefault(x["url"], x["tags"])
    r1 = ("R1: asyncio 이미지 변환·저장. 대기 큐 최대 8, 처리 중 최대 4, sink가 느리면 producer가 기다림, 모든 입력의 task를 미리 "
          "만들거나 무제한 buffer로 옮기기 금지, 완료·용량 회복이 재개 근거, 항목 버리기 금지")
    out = []
    for i in pick:
        r = rows[i]
        req = r["request"]
        qtext = r1 if req.startswith("R1") else qs[req.rsplit(".", 1)[0]]["en"].replace("\n", " / ")
        if r["key"] and r["key"] in cat:
            t = cat[r["key"]]
            text = " || ".join(x for x in [t["what"], t["principle"], t["scene"]] + [c["text"] for c in t["claims"][:2]] if x)
        else:
            text = " || ".join(li.get(r["url"], []))
        out.append({"n": r["n"], "request": req, "request_text": qtext, "url": r["url"], "row_text": text,
                    "model_grade": r["grade"], "model_reason": r["reason"], "human_grade": "", "human_note": ""})
    with open(FIX / "i32" / "human_check.tsv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    return out


# ------------------------------------------------------------------------------------------- I33 꼬리표 한 줄당 최대 점수
I33_SETTINGS = dict(I32_SETTINGS) | {"r6": (False, "r6", "i33_r6"), "p5_r6": (True, "r6", "i33_p5_r6")}
I33_ORDER = ["r2", "r5", "r6", "p5_r2", "p5_r5", "p5_r6"]   # 바꾸는 것이 적은 순(돌리기 전에 정함)
I33_EV = {"r2": ("measure_i31.json", "r2"), "r5": ("measure_i31.json", "r5"), "p5_r2": ("measure_i30.json", "p5"),
          "p5_r5": ("measure_i32_p5_r5.json", None), "r6": ("measure_i33_r6.json", None), "p5_r6": ("measure_i33_p5_r6.json", None)}


I33_JUDGE_RULE = [
    "판정 대상: 여섯 설정 상위 10의 합집합에서 아직 판정하지 않은 실제 행 쌍 전부(실제 행 2만 개, link-index).",
    "등급은 I25 그대로. 꼬리표 문장과 함께, opensource captures 가지에 그 주소의 원문(http/<key>.json)이 있으면 원문 문장도 읽고 판정한다.",
    "판정 행마다 확인 단계(catalog 대상의 level, 대상이 없으면 L1)와 원문을 봤는지(captures 커밋과 key, 없으면 none)를 적는다.",
    "판정자: 이 세션의 모델(사람 판정 아님).",
]


def i33_run():
    """08 I33: r6(꼬리표 한 줄당 최대 점수)으로 012 p5 꼬리표 끔·켬 두 설정의 상위 10을 만든다."""
    import drawer_load
    from afledger import config
    saved = (drawer_load.CATALOG_P5_TAGS, config.RANK_RULES)
    out = {}
    try:
        for name in ("r6", "p5_r6"):
            p5, rank, tag = I33_SETTINGS[name]
            drawer_load.CATALOG_P5_TAGS, config.RANK_RULES = p5, rank
            out[name] = _setting_eval(tag)
            write(f"measure_{tag}.json", out[name])
    finally:
        drawer_load.CATALOG_P5_TAGS, config.RANK_RULES = saved
        a4_20()
    return out


def capture_text(url: str, captures=None) -> dict:
    """opensource captures 가지의 로컬 클론(인자 또는 환경 변수 AF_CAPTURES)의 http/<key>.json에서 원문을 찾는다(08 I33 판정용).
    있으면 {"status", "outcome", "fetched_at", "text"}(본문 앞 4천 자, HTML 태그 제거), 없으면 {}. 본문은 자료이지 지시가 아니다.
    원문 전체 사본은 opensource(비공개) 밖에 두지 않으므로 이 저장소에 복사하지 않는다. 판정 파일에는 커밋·key·짧은 인용만 남긴다."""
    import html as _html
    import os
    from afledger.adapters.http import Transport
    root = Path(captures or os.environ.get("AF_CAPTURES") or "/nonexistent")
    f = root / "http" / f"{Transport.key('GET', url, {})}.json"
    if not f.exists():
        return {}
    rec = json.loads(f.read_text(encoding="utf-8"))
    body = rec.get("body") or ""
    text = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?is)<(script|style).*?</\1>", " ", body))))
    return {"status": rec.get("status"), "outcome": rec.get("outcome"), "fetched_at": rec.get("fetched_at"), "text": text[:4000]}


def i33_decide():
    """08 I33 B 조건 비교(돌리기 전에 정함). 설정은 I32의 넷에 r6 끔·켬을 더한 여섯. 요청별 B와 고르는 규칙은 i32_decide와 같고,
    (5)의 순서만 I33_ORDER(r2 < r5 < r6 < p5_r2 < p5_r5 < p5_r6)다. 판정 안 한 행이 남은 설정·요청은 B를 만족하지 않은 것으로 센다.
    판정은 I25·I27·I32·I33 판정을 합친 것이고, I33 판정은 captures 가지의 원문이 있으면 원문 문장도 본다."""
    res = {}
    for n in I33_ORDER:
        f, k = I33_EV[n]
        ev = json.loads((OUT / f).read_text(encoding="utf-8"))
        ev = ev["results"][k] if k else ev
        row = {"recall12_catalog_only": ev["recall12_catalog_only"], "grade2_catalog_only": ev["grade2_catalog_only"],
               "r1_flow_ok": all(v["first_slot_queue_313_L4"] and v["semaphore_folded_H1U"] and v["create_all_folded_H2"]
                                 for v in ev["r1_flow"].values()), "r1_ranks": ev["r1_ranks"]}
        for cfg in ("catalog20k", "linkindex_real"):
            tag = I33_SETTINGS[n][2]
            top = (json.loads((OUT / f"measure_{tag}_catalog.json").read_text(encoding="utf-8"))["top10"] if cfg == "catalog20k"
                   else json.loads((OUT / f"{tag}_linkindex_pairs.json").read_text(encoding="utf-8"))["top10"]["real_only"])
            j = _judge_top10(top)
            per = j["per_request"]
            b = {k2: v["judged_only"] <= 2 and v["unjudged"] == 0 for k2, v in per.items()}
            row[cfg] = {"B_met": sum(b.values()), "requests": len(b), "unjudged_total": sum(v["unjudged"] for v in per.values()),
                        "B_by_request": b, "r1": j["r1"], "a4_20": j["a4_20"],
                        "B_a4": {l: sum(1 for k2, v in b.items() if v and k2.endswith("." + l) and not k2.startswith("R1"))
                                 for l in ("ko", "en")}}
        res[n] = row
    cand = [n for n in I33_ORDER if res[n]["r1_flow_ok"]]
    best = sorted(cand, key=lambda n: (-res[n]["catalog20k"]["B_met"], -res[n]["linkindex_real"]["B_met"],
                                       -sum(res[n]["recall12_catalog_only"].values()), I33_ORDER.index(n)))
    out = {"rule": i33_decide.__doc__.split("\n")[1:5], "judged_pairs": len(_judgments()), "results": res,
           "ranking": best, "chosen": best[0] if best else None}
    write("measure_i33.json", out)
    return out

# ------------------------------------------------------------------------------------------- R-6
R6_VARIANTS = [("r0", 0.75, "top_k"), ("r1", 0.75, "top_k"), ("r2", 0.5, "top_k"), ("r2", 0.75, "top_k"),
               ("r2", 1.0, "top_k"), ("r2", 0.75, "eligible")]


def r6(mode):
    """07 R-6: 서랍 순위. I17의 목표 셋 — (T1) 자동 한국어 R1에서 세마포어가 자료집만·F01 포함 모두 상위 12 안,
    (T2) F01 포함에서 asyncio-queue가 1~2위, (T3) 손 문장 결과는 그대로(1번 자리·접힘·asyncio-queue 1위).
    고르는 순서(사용자 지시, 2026-11-26): 흔한 분야 낱말의 가중치를 낮추는 방식(IDF, 꼬리표 길이 정규화)을 먼저,
    서랍 상위 12와 자격 규칙은 마지막 수단. T1은 서랍 순위로, 그리고 R1 흐름 전체의 세마포어 접힘으로 본다."""
    import run_r1
    from afledger import config as cfg
    s = studio("studio_rev1.json")
    needs = {"hand": s["needs"], "i1_ko": intake_mod.write_needs(s["text"], s["requirements"])}
    saved = (cfg.RANK_RULES, cfg.RANK_LENGTH_B, cfg.DRAWER_SYMBOL_SCOPE)
    out = {"targets": r6.__doc__.split("\n")[1:3], "variants": {}}
    base_top = {}
    for rank, b, scope in R6_VARIANTS:
        cfg.RANK_RULES, cfg.RANK_LENGTH_B, cfg.DRAWER_SYMBOL_SCOPE = rank, b, scope
        name = f"{rank}" + (f"_b{b}" if rank == "r2" else "") + (f"+{scope}" if scope != "top_k" else "")
        row = {"rank_rules": rank, "length_b": b if rank == "r2" else None, "symbol_scope": scope, "drawer": {}, "flow": {}}
        for noise in (False, True):
            L = Ledger()
            cat = preload_catalog(L)
            nz = preload_noise(L) if noise else {}
            p = L.project("A")
            for nn, nd in needs.items():
                req = L.intake(p, request_key=nn, rev=1, at=T0, text=s["text"], selected_part="s",
                               requirements=s["requirements"], needs=nd)
                hits = L.search_drawer(p, req, T0, k=5000, log=False)
                ids = drawer_ids(L, cat, nz, hits)
                key = f"{nn}_{'with_F01' if noise else 'catalog_only'}"
                top = ids[:12]
                base_top.setdefault(key, top)
                row["drawer"][key] = {"asyncio_queue": ids.index("asyncio-queue") + 1 if "asyncio-queue" in ids else None,
                                      "asyncio_semaphore": ids.index("asyncio-semaphore") + 1 if "asyncio-semaphore" in ids else None,
                                      "noise_in_top12": sum(1 for i in top if str(i).startswith("F01:")),
                                      "top12_same_as_r0": top == base_top[key]}
                # 순위 비교는 기록된 응답만 재생한다(변형 6개 × 흐름 4개를 실제로 돌리면 검색 한도를 넘는다)
                r = run_r1.run("replay", needs="studio" if nn == "hand" else "i1", noise=noise)
                r.pop("_ledger")
                folded = {f["condition"]: f["reason"] for f in r["rev1"]["answer"]["folded"]}
                slot1 = next((x["sentence"] for x in r["rev1"]["answer"]["slots"] if x["kind"] == "direct"), "")
                row["flow"][key] = {"first_slot_queue_313_L4": "/blob/v3.13." in slot1 and "queues.py#L" in slot1
                                    and "이 판에서 실행해 값을 확인했다" in slot1,
                                    "semaphore_folded_H1U": "H1 U" in folded.get("대기 8을 대기열 길이로 지키는가", ""),
                                    "create_all_folded_H2": "H2 위반" in folded.get("입력마다 작업 객체를 미리 만드는가", ""),
                                    "external_attempts": r["rev1"]["budget"]["external_attempts"]}
        d = row["drawer"]
        row["T1_drawer"] = all((d[k]["asyncio_semaphore"] or 999) <= 12 for k in ("i1_ko_catalog_only", "i1_ko_with_F01"))
        row["T1_flow"] = all(row["flow"][k]["semaphore_folded_H1U"] for k in ("i1_ko_catalog_only", "i1_ko_with_F01"))
        row["T2"] = (d["i1_ko_with_F01"]["asyncio_queue"] or 999) <= 2
        row["T3"] = all(d[k]["asyncio_queue"] == 1 and row["flow"][k]["first_slot_queue_313_L4"]
                        and row["flow"][k]["semaphore_folded_H1U"] and row["flow"][k]["create_all_folded_H2"]
                        for k in ("hand_catalog_only", "hand_with_F01"))
        out["variants"][name] = row
    cfg.RANK_RULES, cfg.RANK_LENGTH_B, cfg.DRAWER_SYMBOL_SCOPE = saved
    reweight = {k: v for k, v in out["variants"].items() if v["symbol_scope"] == "top_k"}
    score = lambda v: (v["T1_flow"] + v["T2"] + v["T3"], v["T1_drawer"])  # noqa: E731
    out["best_reweighting_only"] = max(reweight, key=lambda k: score(reweight[k]))
    out["chosen"] = next((k for k, v in out["variants"].items()
                          if v["symbol_scope"] == "top_k" and v["T1_flow"] and v["T2"] and v["T3"]), None) or \
        next((k for k, v in out["variants"].items() if v["T1_flow"] and v["T2"] and v["T3"]), None)
    write("measure_r6.json", out)
    return out


# ------------------------------------------------------------------------------------------- I45 원문 판정(J1)과 B 다시 세기
def _judgments_orig() -> dict:
    """원문을 연 판정(J_orig: opensource judge/, dot D 모델). 꼬리표 판정 _judgments()와 섞지 않는다(08 I45 규칙 1)."""
    import csv
    f = FIX / "judge-orig" / "judgments.tsv"
    if not f.exists():
        return {}
    return {(r["request"], r["url"]): int(r["grade"]) for r in csv.DictReader(open(f, encoding="utf-8"), delimiter="\t")
            if r["grade"] != "?"}    # 열지 못한 쌍은 판정 안 함(08 I48 규칙 2)


def _b_count(g: dict, top10: dict, unjudged_as: str, exclude: frozenset = frozenset()) -> dict:
    """판정 사전 g 하나로만 B를 센다. unjudged_as: 'noise'(아래 끝) 또는 'relevant'(위 끝).
    exclude: 원문을 열 수 없어 풀에서 뺀 (요청, 주소). 상위 10에서 지우고 11위로 채우지 않는다(08 I51 규칙 2)."""
    met, unj_total = {}, 0
    for req, items in top10.items():
        nz = [x for x in items if x["kind"] != "catalog" and (req, x["url"]) not in exclude]
        syn = sum(1 for x in nz if x["kind"] == "synthetic")
        real = [x["url"] for x in nz if x["kind"] != "synthetic"]
        unj = sum(1 for u in real if (req, u) not in g)
        noise0 = sum(1 for u in real if (req, u) in g and g[(req, u)] == 0)
        noise = syn + noise0 + (unj if unjudged_as == "noise" else 0)
        unj_total += unj
        met[req] = noise <= 2
    return {"B_met": sum(met.values()), "requests": len(met), "unjudged_pairs_in_top10": unj_total}


def i45(jo: dict | None = None, write_out: bool = True):
    """08 I45·I48: J1·J2 견주기와 B를 J_orig로 다시 세기(두 끝). 판정자를 섞지 않는다.
    jo를 주면 그 판정을 J_orig 자리에 쓴다(시험용). write_out=False면 파일을 쓰지 않는다."""
    import csv
    import io
    from collections import Counter
    jt, jo = _judgments(), (_judgments_orig() if jo is None else jo)
    hc = list(csv.DictReader(open(FIX / "i32" / "human_check.tsv", encoding="utf-8"), delimiter="\t"))
    rows = list(csv.DictReader(open(FIX / "judge-orig" / "judgments.tsv", encoding="utf-8"), delimiter="\t"))
    j1 = {r["n"]: r for r in rows if r["session"] == "J1-D"}
    conf = Counter((h["model_grade"], j1[h["n"]]["grade"]) for h in hc if h["n"] in j1)
    diff = [h for h in hc if h["n"] in j1 and h["model_grade"] != j1[h["n"]]["grade"]]
    stats = {"pairs": sum(conf.values()), "exact_agree": sum(v for (a, b), v in conf.items() if a == b),
             "binary_agree": sum(v for (a, b), v in conf.items() if (a == "0") == (b == "0")),
             "orig_higher": sum(v for (a, b), v in conf.items() if b > a), "orig_lower": sum(v for (a, b), v in conf.items() if b < a),
             "confusion_tag_to_orig": {f"{a}->{b}": v for (a, b), v in sorted(conf.items())},
             "diverging_n": sorted(int(h["n"]) for h in diff)}
    with (open(FIX / "judge-orig" / "human_check_14.tsv", "w", encoding="utf-8", newline="") if write_out else io.StringIO()) as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["n", "request", "request_text", "url", "row_text", "tag_grade", "orig_grade", "human_grade", "human_note"])
        for h in sorted(diff, key=lambda h: int(h["n"])):
            w.writerow([h["n"], h["request"], h["request_text"], h["url"], h["row_text"], h["model_grade"],
                        j1[h["n"]]["grade"], "", ""])
    # 08 I51 규칙 2: J4 뒤에도 ?인 쌍은 "열 수 없음"으로 풀에서 뺀다(J4가 들어온 뒤에만)
    j4 = [r for r in rows if r["prompt"] == "j4"]
    excluded = frozenset((r["request"], r["url"]) for r in j4 if r["grade"] == "?")
    pool, res = set(), {}
    for n in I32_SETTINGS:
        top = _i32_top10(n, "catalog20k")
        for req, items in top.items():
            pool |= {(req, x["url"]) for x in items if x["kind"] in ("p5", "real") and (req, x["url"]) not in excluded}
        res[n] = {"tag_judge": _b_count(jt, top, "noise"),
                  "orig_judge_lower": _b_count(jo, top, "noise", excluded),
                  "orig_judge_upper": _b_count(jo, top, "relevant", excluded)}
    src = {}
    for name in ("i25", "i27", "i32", "i33"):
        for r in csv.DictReader(open(FIX / name / "judgments.tsv", encoding="utf-8"), delimiter="\t"):
            src.setdefault((r["request"], r["url"]), name + (":" + r["cfg"] if r.get("cfg") else ""))
    missing = sorted(k for k in pool if k not in jo)
    unopened = {(r["request"], r["url"]) for r in rows if r["grade"] == "?"}
    # missing_for_b.tsv는 J3 의뢰의 기준(@027eeb04)이라 그대로 두고, 지금 남은 쌍은 missing_now.tsv에 쓴다(08 I48 규칙 2)
    with (open(FIX / "judge-orig" / "missing_now.tsv", "w", encoding="utf-8", newline="") if write_out else io.StringIO()) as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["request", "url", "tag_judgment_from", "reason"])
        for req, url in missing:
            s_ = src.get((req, url), "")
            w.writerow([req, url, s_, "unopened" if (req, url) in unopened else
                        "j3_requested" if s_ != "i32:catalog20k" else "not_judged"])
    cov = Counter("unopened" if k in unopened else "j3_requested" if src.get(k) != "i32:catalog20k" else "not_judged"
                  for k in missing)
    i32 = {r["n"]: r for r in csv.DictReader(open(FIX / "i32" / "judgments.tsv", encoding="utf-8"), delimiter="\t")}
    sessions = {}
    for sess in sorted({r["session"].split("-")[0] for r in rows}):
        rs = [r for r in rows if r["session"].split("-")[0] == sess and r["prompt"] in ("j1", "j2")]
        if not rs:
            continue
        c = Counter((i32[r["n"]]["grade"], r["grade"]) for r in rs)
        opened = {k: v for k, v in c.items() if k[1] != "?"}
        sessions[sess] = {"pairs": len(rs), "unopened": sum(v for k, v in c.items() if k[1] == "?"),
                          "exact_agree": sum(v for (a, b), v in opened.items() if a == b),
                          "binary_agree": sum(v for (a, b), v in opened.items() if (a == "0") == (b == "0")),
                          "orig_higher": sum(v for (a, b), v in opened.items() if b > a),
                          "orig_lower": sum(v for (a, b), v in opened.items() if b < a),
                          "confusion_tag_to_orig": {f"{a}->{b}": v for (a, b), v in sorted(c.items())}}
    for sess in sorted({r["session"].split("-")[0] for r in rows if r["prompt"] == "j3"}):
        rs = [r for r in rows if r["session"].split("-")[0] == sess]
        c = Counter((str(jt.get((r["request"], r["url"]), "-")), r["grade"]) for r in rs)
        opened = {k: v for k, v in c.items() if k[1] != "?" and k[0] != "-"}
        sessions[sess] = {"pairs": len(rs), "unopened": sum(v for k, v in c.items() if k[1] == "?"),
                          "orig_grades": dict(Counter(r["grade"] for r in rs)),
                          "exact_agree": sum(v for (a, b), v in opened.items() if a == b),
                          "binary_agree": sum(v for (a, b), v in opened.items() if (a == "0") == (b == "0")),
                          "orig_higher": sum(v for (a, b), v in opened.items() if b > a),
                          "orig_lower": sum(v for (a, b), v in opened.items() if b < a),
                          "confusion_tag_to_orig": {f"{a}->{b}": v for (a, b), v in sorted(c.items())}}
    # 08 I48 규칙 3: I32 고르기 규칙을 J_orig로. link-index 동률 깨기(3)는 건너뛴다(J_orig 없음, 판정자를 섞지 않음).
    # 08 I50(고친 규칙 4): 두 끝(남은 행을 모두 잡음 / 모두 관련)에서 같은 설정을 고르면 정한다
    prev = json.loads((OUT / "measure_i32.json").read_text(encoding="utf-8"))["results"]
    order = ["r2", "r5", "p5_r2", "p5_r5"]
    cand = [n for n in order if prev[n]["r1_flow_ok"]]

    def ranked(bound):
        return sorted(cand, key=lambda n: (-res[n][bound]["B_met"], -sum(prev[n]["recall12_catalog_only"].values()),
                                           order.index(n)))
    lo, hi = ranked("orig_judge_lower"), ranked("orig_judge_upper")
    same = bool(lo) and lo[0] == hi[0]
    pick = {"ranking_lower": lo, "ranking_upper": hi, "chosen_lower": lo[0] if lo else None,
            "chosen_upper": hi[0] if hi else None, "decided": not missing or same,
            "chosen": (lo[0] if (not missing or same) else None),
            "B_orig_lower": {n: res[n]["orig_judge_lower"]["B_met"] for n in order},
            "B_orig_upper": {n: res[n]["orig_judge_upper"]["B_met"] for n in order}}
    out = {"rules": "08 I45", "judges": {"tag": "이 세션의 모델, 꼬리표 문장만(I25·I27·I32·I33)",
                                         "orig": "opensource judge/ dot D 모델, 원문을 엶(사람 아님)"},
           "orig_pairs": len(jo), "j1": stats, "b_pool_pairs": len(pool), "b_pool_with_orig": len(pool) - len(missing),
           "missing": dict(cov), "by_session": sessions,
           "excluded_unopenable": {"count": len(excluded), "pairs": sorted(list(p_) for p_ in excluded)},
           "decision": ("J_orig로 고름(풀을 다 덮음)" if not missing else
                        "두 끝이 같은 설정을 골라 정함(I50 규칙 4a)" if same else
                        "두 끝이 달라 J4를 기다림(I50 규칙 4b)"),
           "pick_orig": pick, "B_catalog20k": res}
    if write_out:
        write("measure_i45.json", out)
    return out


def main():
    if sys.argv[1:2] == ["i45"]:
        print(json.dumps(i45(), ensure_ascii=False, indent=1))
        return
    mode = "live" if "--live" in sys.argv else "replay"
    OUT.mkdir(exist_ok=True)
    res = {"a4": a4(mode), "b1": b1(), "r4": r4(), "norm": norm_regression(), "f01": f01(), "r1_map": r1_map(),
           "r6": r6(mode), "a4_20": a4_20(), "r6_scale": r6_scale(), "r3": r3(mode), "i24": i24(), "i25_pairs": i25_collect(), "i25": i25_score(),
           "i26": i26(), "i26_rank": i26_rank(), "i26_combo": i26_combo(),
           "i27": i27(), "i27_judged": i27_score(), "i28": i28(), "i29": i29(),
           "i30": i30(), "i31": i31(), "i32_run": i32_run_both(), "i32": i32_decide(), "i32_human": i32_human_sample(),
           "i33_run": i33_run(), "i33": i33_decide(), "i45": i45()}
    a = res["a4"]["variants"]
    print("A4", {k: (v["catalog_only"]["asyncio_queue_rank"], v["catalog_only"].get("overlap_with_hand_top6"),
                     v["catalog_only"]["eligible_count"], v["catalog_only"]["deep_rank"])
                 for k, v in a.items()})
    print("A4 flow", {k: (v.get("criterion2_pass"), v.get("parts")) for k, v in res["a4"]["r1_flow_with_i1_ko"].items()})
    print("B1", res["b1"]["modes"])
    print("R4", res["r4"]["variants"], "chosen", res["r4"]["chosen"])
    print("NORM", {k: res["norm"][k] for k in ("rows", "distinct_raw_urls", "distinct_url_norm", "distinct_page",
                                                "distinct_target_or_page", "errors", "idempotent_page_on_url_norm")})
    print("F01", {k: {x: v[x] for x in ("noise_in_top10", "asyncio_queue_rank", "function_word_only_hits_that_are_eligible_under_rule", "eligible_noise_total")} for k, v in res["f01"].items() if isinstance(v, dict)})
    print("R1MAP", res["r1_map"]["total"])
    for k, v in res["r6"]["variants"].items():
        print("R6", k, "T1d", v["T1_drawer"], "T1f", v["T1_flow"], "T2", v["T2"], "T3", v["T3"],
              {kk: (vv["asyncio_queue"], vv["asyncio_semaphore"], vv["noise_in_top12"]) for kk, vv in v["drawer"].items()})
    print("R3", json.dumps(res["r3"]["by_pair"]), json.dumps(res["r3"]["ledger"]), [x["same_quote_fp"] for x in res["r3"]["range"]])
    print("A4-20", json.dumps(res["a4_20"]["summary"], ensure_ascii=False))
    print("R6-SCALE", json.dumps(res["r6_scale"]["end_condition_met"]), json.dumps(res["r6_scale"]["rank_rules"]["r2"]["r1"]))
    print("I24", json.dumps(res["i24"]["noise_top10"]), "revert", res["i24"]["revert_to_e1"])
    print("I25", res["i25"]["grade_counts"], json.dumps({c: v["a4_20"] for c, v in res["i25"]["by_config"].items()}))
    print("I26", res["i26"]["adopt"], res["i26_rank"]["adopt_r3"], res["i26_combo"]["adopt"], json.dumps(res["i26_combo"]["judged_noise"]))
    print("I27", json.dumps(res["i27_judged"]["r1"]), json.dumps(res["i27_judged"]["a4_20"]))
    print("I28", res["i28"]["adopt_r4"], res["i28"]["worse"], "I29", res["i29"]["recommend_reask"])
    print("I30", res["i30"]["adopt_p5"], res["i30"]["worse"], "I31", res["i31"]["adopt_r5"], res["i31"]["worse"])
    print("I32", res["i32"]["ranking"], {n: r["catalog20k"]["B_met"] for n, r in res["i32"]["results"].items()})
    print("I33", res["i33"]["ranking"], {n: r["catalog20k"]["B_met"] for n, r in res["i33"]["results"].items()})
    print("R6 best reweighting", res["r6"]["best_reweighting_only"], "chosen", res["r6"]["chosen"])


if __name__ == "__main__":
    main()
