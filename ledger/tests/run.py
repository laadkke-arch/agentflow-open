"""ledger/tests의 시험을 모두 돈다. 네트워크를 쓰지 않는다(기록 재생). 실행: python3 -I ledger/tests/run.py"""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
suite = unittest.defaultTestLoader.discover(str(HERE), top_level_dir=str(HERE))
sys.exit(0 if unittest.TextTestRunner(verbosity=2 if "-v" in sys.argv else 1).run(suite).wasSuccessful() else 1)
