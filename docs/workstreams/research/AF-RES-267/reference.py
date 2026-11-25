"""AF-RES-249 stimuli v1, transcribed and checked independently of its runner."""
import argparse
import json
from pathlib import Path
import sys
import traceback

# The manual answers and inputs are from stimuli.md, lines 6-19 and 40-55.
# The tag labels for B follow the original runner's decimal index encoding.
A = [
    ([], [], "No runs."),
    ([("a", 1)], [("a", [1])], "One final run."),
    ([("a", 1), ("a", 2), ("b", 3), ("a", 4)],
     [("a", [1, 2]), ("b", [3]), ("a", [4])], "Cut at a/b and b/a."),
    ([("a", 2), ("a", 2), ("a", 0)], [("a", [2, 2, 0])], "Keep both 2s and 0."),
    ([("", 0), ("b", -1), ("", 2)], [("", [0]), ("b", [-1]), ("", [2])],
     "The two empty-string runs are separated."),
    ([("z", 1), ("a", 2), ("z", 3), ("a", 4)],
     [("z", [1]), ("a", [2]), ("z", [3]), ("a", [4])], "Every adjacent key changes."),
    ([("x", 1), ("x", 2), ("y", 3)], [("x", [1, 2]), ("y", [3])],
     "Public example. One cut at x/y."),
]
B = [
    ([], 2, 0, "No preceding keys."),
    ([1, 4], 3, 1, "Only 1 precedes 3."),
    ([1, 2, 2, 4], 2, 3, "1 and both 2s precede insertion."),
    ([2, 2, 2], 2, 3, "All three ties precede insertion."),
    ([2], 1, 0, "Before the first key."),
    ([2], 3, 1, "After the only key."),
    ([1, 1, 4, 4], 4, 4, "Both 1s and both 4s precede insertion."),
    ([-3, 0, 0, 5], 0, 3, "-3 and both 0s precede insertion."),
]
A_TYPE = "list[tuple[str,list[int]]]"
B_TYPE = "int"


def consecutive_runs(rows):
    if not rows:
        return []
    boundaries = [0]
    for i in range(1, len(rows)):
        if rows[i - 1][0] != rows[i][0]:
            boundaries.append(i)
    boundaries.append(len(rows))
    return [(rows[start][0], [payload for _, payload in rows[start:end]])
            for start, end in zip(boundaries, boundaries[1:])]


def first_greater(rows, probe):
    return next((i for i, (key, _) in enumerate(rows) if key > probe), len(rows))


def vectors(task):
    if task == "A":
        for i, (rows, manual, reason) in enumerate(A):
            yield f"A{i}", rows, None, manual, consecutive_runs(rows), A_TYPE, reason
    else:
        for i, (keys, probe, manual, reason) in enumerate(B):
            rows = [(key, str(j)) for j, key in enumerate(keys)]
            yield f"B{i}", rows, probe, manual, first_greater(rows, probe), B_TYPE, reason


def exact_shape(task, value):
    if task == "B":
        return type(value) is int
    if type(value) is not list:
        return False
    for pair in value:
        if type(pair) is not tuple or len(pair) != 2:
            return False
        key, payloads = pair
        if type(key) is not str or type(payloads) is not list:
            return False
        if any(type(item) is not int for item in payloads):
            return False
    return True


def line_observer(function, arg, changes):
    previous = tuple(arg)

    def check(frame, event, detail):
        nonlocal previous
        current = tuple(arg)
        if current != previous:
            changes.append({"event": event, "line": frame.f_lineno,
                            "before": repr(list(previous)), "after": repr(list(current))})
            previous = current
        return check

    def select(frame, event, detail):
        if event == "call" and frame.f_code is function.__code__:
            return check
        return None

    return select


def run(task, path, observe_lines=False):
    path = path.resolve()
    namespace = {"__name__": "af267_fixture", "__file__": str(path)}
    exec(compile(path.read_bytes(), str(path), "exec"), namespace)
    function = namespace["runs" if task == "A" else "insertion_index"]
    for vector_id, rows, probe, manual, expected, expected_type, reason in vectors(task):
        if manual != expected or not exact_shape(task, manual):
            raise ValueError(f"{vector_id}: written answer and reference disagree")
        # Every input row contains only an immutable tuple and builtin scalars.
        arg = list(rows)
        changes = []
        record = {"id": vector_id, "input": repr(rows), "x": probe,
                  "manual_expected": repr(manual), "expected": repr(expected),
                  "expected_type": expected_type, "manual_reason": reason}
        try:
            if observe_lines:
                sys.settrace(line_observer(function, arg, changes))
            try:
                got = function(arg) if task == "A" else function(arg, probe)
            finally:
                if observe_lines:
                    sys.settrace(None)
        except Exception as exc:
            record.update(exception=f"{type(exc).__name__}: {exc}",
                          traceback=traceback.format_exc(), endpoint_pass=False)
        else:
            record.update(got=repr(got), got_type=type(got).__name__,
                          value_equal=(got == expected), type_ok=exact_shape(task, got))
            record["endpoint_pass"] = record["value_equal"] and record["type_ok"] and arg == rows
        record["unchanged"] = arg == rows
        if observe_lines:
            record["line_observations"] = changes
        print(json.dumps(record, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", choices=("A", "B"))
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--observe-lines", action="store_true")
    args = parser.parse_args()
    run(args.task, args.fixture, args.observe_lines)


if __name__ == "__main__":
    main()
