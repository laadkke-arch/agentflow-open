"""Proposed runner; not executed in AF-RES-249. Run untrusted submissions only in an isolated sandbox."""
import copy
import importlib.util
import json
import sys
import traceback

A = [
    ([], []),
    ([("a", 1)], [("a", [1])]),
    ([("a", 1), ("a", 2), ("b", 3), ("a", 4)], [("a", [1, 2]), ("b", [3]), ("a", [4])]),
    ([("a", 2), ("a", 2), ("a", 0)], [("a", [2, 2, 0])]),
    ([("", 0), ("b", -1), ("", 2)], [("", [0]), ("b", [-1]), ("", [2])]),
    ([("z", 1), ("a", 2), ("z", 3), ("a", 4)], [("z", [1]), ("a", [2]), ("z", [3]), ("a", [4])]),
    ([("x", 1), ("x", 2), ("y", 3)], [("x", [1, 2]), ("y", [3])]),
]
B = [([], 2, 0), ([1, 4], 3, 1), ([1, 2, 2, 4], 2, 3), ([2, 2, 2], 2, 3),
     ([2], 1, 0), ([2], 3, 1), ([1, 1, 4, 4], 4, 4), ([-3, 0, 0, 5], 0, 3)]

def main():
    task, path = sys.argv[1:]
    if task not in ("A", "B") or sys.version_info[:2] != (3, 12):
        raise SystemExit("task must be A or B and Python must be 3.12")
    spec = importlib.util.spec_from_file_location("submission", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cases = [(e, None, w) for e, w in A] if task == "A" else [
        ([(k, str(i)) for i, k in enumerate(keys)], x, w) for keys, x, w in B
    ]
    results = []
    for i, (rows, x, expected) in enumerate(cases):
        arg = copy.deepcopy(rows)
        try:
            got = mod.runs(arg) if task == "A" else mod.insertion_index(arg, x)
            type_ok = (type(got) is list and all(type(t) is tuple and len(t) == 2 and
                       type(t[0]) is str and type(t[1]) is list and
                       all(type(v) is int for v in t[1]) for t in got)) if task == "A" else type(got) is int
            ok = bool(type_ok and got == expected and arg == rows)
            row = {"id": f"{task}{i}", "input": repr(rows), "x": x, "expected": repr(expected),
                   "got": repr(got), "unchanged": arg == rows, "type_ok": type_ok, "pass": ok}
        except Exception:
            row = {"id": f"{task}{i}", "input": repr(rows), "x": x, "expected": repr(expected),
                   "exception": traceback.format_exc(), "pass": False}
        results.append(row)
        print(json.dumps(row, ensure_ascii=False))
    return 0 if all(r["pass"] for r in results) else 1

if __name__ == "__main__":
    raise SystemExit(main())
