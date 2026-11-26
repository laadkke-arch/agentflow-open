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


def main():
    mode = "live" if "--live" in sys.argv else "replay"
    OUT.mkdir(exist_ok=True)
    res = {"a4": a4(mode), "b1": b1(), "r4": r4(), "norm": norm_regression(), "f01": f01(), "r1_map": r1_map(),
           "r6": r6(mode), "a4_20": a4_20(), "r6_scale": r6_scale(), "r3": r3(mode), "i24": i24(), "i25_pairs": i25_collect(), "i25": i25_score()}
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
    print("R6 best reweighting", res["r6"]["best_reweighting_only"], "chosen", res["r6"]["chosen"])


if __name__ == "__main__":
    main()
