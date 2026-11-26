"""새 검색 어댑터(06 3.1): 직접 갈래만 실제 검색, 관계·분야 추정·언어 갈래는 빈 목록.

직접 갈래 = 사용자 런타임의 1차 소스에서 직접 도구를 찾는다. 규칙 판 s1:
  1. 범위: 맥락의 런타임이 CPython이면 저장소 python/cpython. 요청 원문·선택 부분에 나온 표준 라이브러리 이름
     (sys.stdlib_module_names)이 패키지면 path:Lib/<이름>, 모듈이면 path:Lib. 없으면 path:Lib.
  2. 낱말: 칸별 필요 문장의 영어 내용어(기능어·숫자 제외, 어간으로 묶음)를 "몇 칸에 나오나" 내림차순, 처음 나온 순서로
     줄 세워 앞에서 MAX_TERMS개. MAX_TERMS = 외부 시도 10 − 가져오기 4 = 6(예산에서 정한 값, 08 I7).
  3. 낱말마다 GitHub 코드 검색 1회(기존 코드 검색은 OR을 받지 않는다). 호출은 외부 시도로 센다.
  4. 파일 점수 = 맞은 낱말마다 log(N/df)의 합. df = 그 낱말의 결과 수, N = 결과 수의 최댓값 + 1.
     점수 내림차순, 경로순으로 앞에서 MAX_RESULTS개를 낸다. 맞은 낱말을 why에 남긴다.
GitHub 코드 검색은 기본 브랜치만 본다. 결과 주소의 판(커밋)은 사용자 판이 아니므로, 확인은 정규화한 page를
사용자 판(태그)으로 다시 연다. 이 검색은 Python 밖 요청에 일반화되지 않는다(08 I7).
"""
from __future__ import annotations

import importlib.util
import json
import math
import re
import sys
import urllib.parse

from .. import config

SEARCH_ID = f"gh-code-search/{config.SEARCH_RULES}"
MAX_TERMS = config.REQUEST_EXTERNAL_ATTEMPTS - config.REQUEST_FETCHES
MAX_RESULTS = 5
SLOT_ORDER = ("input", "output", "keeps", "breaks_when", "summary", "user_without")   # "처음 나온 순서"의 기준
API = "https://api.github.com/search/code"
GENERIC = {"this", "test", "code", "types", "string", "time", "token", "select", "signal", "random", "site", "abc",
           "io", "os", "sys", "copy", "queue", "array", "struct", "math", "glob", "html", "json"}


def _stem(t: str) -> str:
    for suf in ("ations", "ation", "ions", "ion", "ings", "ing", "edly", "ed", "es", "s"):
        if t.endswith(suf) and len(t) - len(suf) >= 3:
            return t[: -len(suf)]
    return t


def scope(context: dict, request_text: str, selected_part: str) -> dict | None:
    rt = (context.get("runtime") or "")
    if "cpython" not in rt.lower() and not rt.lower().startswith("python"):
        return None
    words = re.findall(r"[a-z_][a-z0-9_]*", (request_text + " " + selected_part).lower())
    mods = [w for w in dict.fromkeys(words) if w in sys.stdlib_module_names and w not in GENERIC]
    path, pkg = "Lib", None
    for m in mods:
        spec = importlib.util.find_spec(m)
        if spec and spec.submodule_search_locations:
            path, pkg = f"Lib/{m}", m
            break
    return {"repo": "python/cpython", "path": path, "package": pkg, "modules": mods}


def terms(needs: list[dict], content_tokens) -> list[dict]:
    seen: dict[str, dict] = {}
    order = 0
    for n in needs:
        for t in content_tokens(n["text"]):
            s = _stem(t)
            d = seen.setdefault(s, {"stem": s, "surface": {}, "slots": set(), "first": order})
            d["surface"][t] = d["surface"].get(t, 0) + 1
            d["slots"].add(n["slot"])
            order += 1
    ranked = sorted(seen.values(), key=lambda d: (-len(d["slots"]), d["first"]))
    out = []
    for d in ranked[:MAX_TERMS]:
        surface = sorted(d["surface"].items(), key=lambda kv: (-kv[1], len(kv[0])))[0][0]
        out.append({"term": surface, "stem": d["stem"], "slots": sorted(d["slots"])})
    return out


def direct_branch(L, transport, p: str, req: int, at: str, *, context: dict, request_text: str, selected_part: str,
                  content_tokens, budget=None) -> dict:
    """직접 갈래를 돌린다. 돌려주는 사전: scope, terms, calls, results([{url, why, score, matched}])."""
    sc = scope(context, request_text, selected_part)
    order = {s: i for i, s in enumerate(SLOT_ORDER)}
    needs = sorted((dict(r) for r in L.db.execute(f"SELECT slot, lang, text FROM {p}.need WHERE req_id=?", (req,))),
                   key=lambda n: order.get(n["slot"], 99))
    out = {"search_id": SEARCH_ID, "scope": sc, "terms": [], "calls": [], "results": []}
    if not sc:
        return out
    ts = terms(needs, content_tokens)
    out["terms"] = ts
    per_file: dict[str, dict] = {}
    df = {}
    for t in ts:
        if budget is not None:
            budget.check_external()
        q = f"{t['term']} repo:{sc['repo']} path:{sc['path']} language:Python"
        url = API + "?" + urllib.parse.urlencode({"q": q, "per_page": 100})
        r = transport.get(url, {"Accept": "application/vnd.github.text-match+json"}, note=f"search direct {q}")
        ok = r.status == 200
        items = r.json().get("items", []) if ok else []
        total = r.json().get("total_count", 0) if ok else None
        L.called(p, req, "search:direct", q, at, "ok" if ok else f"http_{r.status}", total)
        out["calls"].append({"q": q, "status": r.status, "total": total, "fetched_at": r.fetched_at})
        df[t["term"]] = max(1, len(items))
        for it in items:
            d = per_file.setdefault(it["path"], {"path": it["path"], "html_url": it["html_url"], "matched": []})
            frag = " ".join(m.get("fragment", "") for m in it.get("text_matches", []))[:300]
            d["matched"].append({"term": t["term"], "fragment": frag})
    n = max(df.values(), default=1) + 1
    for d in per_file.values():
        d["score"] = round(sum(math.log(n / df[m["term"]]) for m in d["matched"]), 4)
    ranked = sorted(per_file.values(), key=lambda d: (-d["score"], d["path"]))[:MAX_RESULTS]
    out["results"] = [{"url": d["html_url"], "path": d["path"], "score": d["score"],
                       "why": "matched: " + ", ".join(m["term"] for m in d["matched"]),
                       "matched": d["matched"]} for d in ranked]
    return out


def log_fresh(L, p: str, req: int, at: str, direct: dict) -> list[dict]:
    """탐색 기록에 네 갈래를 남긴다. 직접 갈래만 실제 결과, 나머지 셋은 빈 목록(단위 1)."""
    return L.search_fresh(p, req, at, {
        "direct": [{"url": r["url"], "why": r["why"]} for r in direct["results"]],
        "relation": [], "domain_guess": [], "language": [],
    })


def dumps(d) -> str:
    return json.dumps(d, ensure_ascii=False, sort_keys=True)


def resolve_drawer_symbols(L, transport, p: str, req: int, at: str, *, scope: dict, drawer_hits: list[dict],
                           budget=None) -> list[dict]:
    """서랍 적중 가운데 사용자 런타임의 기호(자료집 이름이 '<패키지>.<클래스>')를 사용자 판의 소스 파일로 찾는다.
    서랍은 문서 주소(docs.python.org)를 들고 있어 고정판 소스 줄(D10)로 열려면 파일을 알아야 한다.
    기호마다 코드 검색 1회(외부 시도). 결과는 탐색 기록에 새 검색 직접 갈래로 남긴다(질의에 서랍 출처를 적는다)."""
    if not scope or not scope.get("package"):
        return []
    out = []
    for h in drawer_hits:
        if not h.get("eligible") or h.get("lexical_accident"):
            continue
        o = L.obs(h["obs_id"])
        name = (o["quote"] or "").split(" — ")[0].strip()
        m = re.fullmatch(re.escape(scope["package"]) + r"\.([A-Z][A-Za-z0-9_]*)", name)
        if not m:
            continue
        if budget is not None:
            budget.check_external()
        q = f'"class {m.group(1)}" repo:{scope["repo"]} path:{scope["path"]} language:Python'
        url = API + "?" + urllib.parse.urlencode({"q": q, "per_page": 10})
        r = transport.get(url, {"Accept": "application/vnd.github.text-match+json"}, note=f"search symbol {q}")
        ok = r.status == 200
        items = r.json().get("items", []) if ok else []
        L.called(p, req, "search:direct_symbol", q, at, "ok" if ok else f"http_{r.status}",
                 r.json().get("total_count") if ok else None)
        hits = [it for it in items if f"class {m.group(1)}" in
                " ".join(x.get("fragment", "") for x in it.get("text_matches", []))] or items
        res = [{"url": it["html_url"], "path": it["path"],
                "why": f"class {m.group(1)} (서랍 적중 {name}에서, 순위 {h['rank']})"} for it in hits[:1]]
        L.search_fresh(p, req, at, {f"direct:symbol {name}": [{"url": x["url"], "why": x["why"]} for x in res]})
        out.append({"name": name, "drawer_rank": h["rank"], "q": q, "status": r.status, "results": res})
    return out
