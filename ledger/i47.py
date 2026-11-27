"""08 I47: m1을 실제로 사라진·이름이 바뀐 기호에서 잰다(CPython Lib/asyncio/unix_events.py v3.13.0 → v3.14.0, 기록 재생).

  python3 -I ledger/i47.py      out/i47_unix_events.json을 쓴다
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from afledger import locate  # noqa: E402
from afledger.adapters.http import Transport  # noqa: E402
from afledger.adapters.reader_github import raw_url  # noqa: E402

REPO, PATH, OLD, NEW = "python/cpython", "Lib/asyncio/unix_events.py", "v3.13.0", "v3.14.0"
GONE = ("AbstractChildWatcher", "BaseChildWatcher", "SafeChildWatcher", "FastChildWatcher", "MultiLoopChildWatcher")
RENAMED = {"PidfdChildWatcher": "_PidfdChildWatcher", "ThreadedChildWatcher": "_ThreadedChildWatcher"}


def texts():
    t = Transport("replay", HERE / "fixtures" / "http")
    return t.get(raw_url(REPO, OLD, PATH)).text(), t.get(raw_url(REPO, NEW, PATH)).text()


def run() -> dict:
    a, b = texts()
    sa, sb = locate.symbols(a), locate.symbols(b)
    rows = []
    for cls in GONE + tuple(RENAMED):
        s = sa[cls]
        for kind, rng, in_doc in (("docstring", s["doc"], True), ("class_range", s["range"], False)):
            if not rng:
                rows.append({"class": cls, "anchor": kind, "verdict": "no_anchor"})
                continue
            an = locate.anchor(a, *rng, python=True)
            m = locate.map_position({"quote": an["quote"], "symbol": an["symbol"], "in_doc": in_doc}, b, python=True)
            target = sb.get(RENAMED.get(cls, ""), {}).get("range")
            if cls in GONE:
                verdict = "correct" if not m["lines"] else "false_mapping"
            elif not m["lines"]:
                verdict = "miss"
            else:
                verdict = "correct" if target and target[0] <= m["lines"][0] and m["lines"][1] <= target[1] else "false_mapping"
            mapped_sym = locate.symbol_at(b, *m["lines"])[0] if m["lines"] else None
            rows.append({"class": cls, "anchor": kind, "old_lines": list(rng), "method": m["method"],
                         "new_lines": list(m["lines"]) if m["lines"] else None, "mapped_symbol": mapped_sym,
                         "symbol_present": m["symbol_present"], "expected": "unmapped" if cls in GONE else RENAMED[cls],
                         "verdict": verdict})
    from collections import Counter
    out = {"note": "기록 재생. 원문은 fixtures/http에 v3.13.0·v3.14.0 raw 1회씩 기록(08 I47). m1은 바꾸지 않았다.",
           "classes_old": [k for k in sa if "ChildWatcher" in k and "." not in k],
           "classes_new": [k for k in sb if "ChildWatcher" in k and "." not in k],
           "summary": dict(Counter(r["verdict"] for r in rows)), "rows": rows}
    (HERE / "out" / "i47_unix_events.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    r = run()
    print(r["summary"], r["classes_new"])
    for x in r["rows"]:
        print(x["class"], x["anchor"], x.get("method"), x.get("old_lines"), x.get("new_lines"), x.get("mapped_symbol"), x["verdict"])
