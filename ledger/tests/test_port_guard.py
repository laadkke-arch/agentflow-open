"""옮긴 시험이 설계 예제와 같은 단언인지 지키는 시험. 설계 예제(docs/design/final/db)는 고치지 않고 기준으로 둔다."""
import ast
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = ROOT / "docs/design/final/db/test_ledger.py"


def methods(path, rename=None):
    src = path.read_text(encoding="utf-8")
    if rename:
        for a, b in rename.items():
            src = src.replace(a, b)
    out = {}
    for cls in ast.parse(src).body:
        if isinstance(cls, ast.ClassDef):
            for fn in cls.body:
                if isinstance(fn, ast.FunctionDef):
                    out[(cls.name, fn.name)] = ast.get_source_segment(src, fn)
    return out


class PortGuard(unittest.TestCase):
    def test_33_tests_are_ported_verbatim(self):
        design = methods(DESIGN, {"cases.KB": "KB"})
        ported = methods(HERE / "test_ported.py")
        tests = {k: v for k, v in ported.items() if k[1].startswith("test_")}
        counts = {}
        for (cls, _name) in tests:
            counts[cls] = counts.get(cls, 0) + 1
        self.assertEqual(counts, {"StorageContract": 13, "Rules": 2, "OperationalFixes": 14, "Decisions": 4})
        for k, body in ported.items():
            self.assertEqual(body, design[k], f"{k} differs from the design test")


if __name__ == "__main__":
    sys.exit(unittest.main())
