"""routes40.json 후처리: 놓친 것을 원인별로 나누고, 경로별 L3 상한을 모집단에 곱해 추정한다."""
import gzip, json, sys, re
from collections import Counter

targets = {}
for l in gzip.open(sys.argv[1], "rt"):
    d = json.loads(l)
    targets[d["key"]] = d
m = json.load(open(sys.argv[2]))


def latin_share(s):
    letters = [c for c in s if c.isalpha()]
    if not letters:
        return 0.0
    return sum(1 for c in letters if c < "ɐ") / len(letters)


out = {}
for route, v in m["measure"].items():
    res = Counter()
    for ex in v["examples"]:
        r = ex.get("result")
        if r is None:
            res["fetch_fail"] += 1
            continue
        if r in ("exact", "near"):
            res["match"] += 1
            continue
        t = targets[ex["key"]]
        evs = [c.get("evidence") or "" for c in t["claims"]]
        best = max((latin_share(e) for e in evs), default=0)
        xlang_route = route.endswith("xlang")
        if not xlang_route and best < 0.5:
            res["miss_translated_evidence"] += 1
        else:
            res["miss_other"] += 1
    n = v["sample"]
    fetched = n - res["fetch_fail"]
    out[route] = {"population": v["population"], "sample": n, **res,
                  "match_rate_of_sample": round(res["match"] / n, 3) if n else None,
                  "match_rate_of_fetched": round(res["match"] / fetched, 3) if fetched else None,
                  "est_L3_population": round(res["match"] / n * v["population"]) if n else 0}
    print(route, json.dumps(out[route], ensure_ascii=False))
tot = sum(x["est_L3_population"] for x in out.values())
print("estimated L3 across measured routes:", tot)
json.dump(out, open(sys.argv[3], "w"), ensure_ascii=False, indent=1)
