"""The cloud wrapper must retain failure evidence rather than manufacture a pass."""
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts import cloud_check


class CloudCheckEvidenceTests(unittest.TestCase):
    def exercise(self, steps):
        with tempfile.TemporaryDirectory(prefix="cloud-check-test-") as temp:
            root = Path(temp)
            with patch.object(cloud_check, "checks", return_value=steps), \
                 contextlib.redirect_stdout(io.StringIO()), \
                 contextlib.redirect_stderr(io.StringIO()):
                code = cloud_check.execute(root, "test-fixture")
            receipt = json.loads((root / ".workbench/cloud-check.json").read_text())
            logs = {step["name"]: {
                stream: (root / step[stream + "_log"]).read_text()
                for stream in ("stdout", "stderr")}
                for step in receipt["checks"]}
            return code, receipt, logs

    def test_nonzero_retains_output_and_stops_later_checks(self):
        code, receipt, logs = self.exercise([
            ("failure", [sys.executable, "-c", "print('failure marker'); raise SystemExit(7)"], 10),
            ("must-not-run", [sys.executable, "-c", "raise SystemExit(0)"], 10),
        ])
        self.assertEqual(code, 7)
        self.assertEqual(receipt["status"], "failed")
        self.assertIsNotNone(receipt["completed_at"])
        self.assertEqual([step["name"] for step in receipt["checks"]], ["failure"])
        self.assertIn("failure marker", logs["failure"]["stdout"])

    def test_timeout_is_nonzero_and_has_a_completed_receipt(self):
        code, receipt, logs = self.exercise([
            ("timeout", [sys.executable, "-c", "import time; time.sleep(10)"], 0.1),
        ])
        self.assertEqual(code, 124)
        self.assertEqual(receipt["status"], "failed")
        self.assertEqual(receipt["checks"][0]["status"], "timed_out")
        self.assertIn("timed out", logs["timeout"]["stderr"])

    def test_no_active_sessions_is_preserved_as_not_executed(self):
        result = {"status": "not-executed", "reason": "no_active_sessions", "count": 0}
        code, receipt, _ = self.exercise([
            ("sessions", [sys.executable, "-c", "print(" + repr(json.dumps(result)) + ")"], 10),
        ])
        self.assertEqual(code, 0)
        self.assertEqual(receipt["session_validation"], result)

    def test_github_context_keeps_shas_without_copying_secrets(self):
        with tempfile.TemporaryDirectory(prefix="cloud-event-test-") as temp:
            event = Path(temp) / "event.json"
            event.write_text(json.dumps({"token": "DO_NOT_COPY", "pull_request": {
                "head": {"sha": "a" * 40}, "base": {"sha": "b" * 40}}}))
            with patch.dict(os.environ, {"GITHUB_EVENT_PATH": str(event),
                            "GITHUB_SHA": "c" * 40, "SECRET": "DO_NOT_COPY"}, clear=True):
                result = cloud_check.github_context()
            self.assertEqual(result["pr_head_sha"], "a" * 40)
            self.assertEqual(result["pr_base_sha"], "b" * 40)
            self.assertEqual(result["event_sha"], "c" * 40)
            self.assertNotIn("DO_NOT_COPY", json.dumps(result))

    def test_clean_gate_rejects_tracked_child_mutation_and_dirty_restart(self):
        with tempfile.TemporaryDirectory(prefix="cloud-clean-test-") as temp:
            root = Path(temp)
            for args in (["init", "-q"], ["config", "core.autocrlf", "false"]):
                subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)
            (root / ".gitignore").write_text(".workbench/\n", encoding="utf-8")
            (root / "tracked.txt").write_text("committed content\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True, capture_output=True)
            subprocess.run(["git", "-c", "user.name=Fixture", "-c",
                            "user.email=fixture@example.invalid", "commit", "-qm", "baseline"],
                           cwd=root, check=True, capture_output=True)
            steps = [("change-tracked", [sys.executable, "-c",
                      "from pathlib import Path; Path('tracked.txt').write_text('changed')"], 10)]
            with patch.object(cloud_check, "checks", return_value=steps), \
                 contextlib.redirect_stdout(io.StringIO()), \
                 contextlib.redirect_stderr(io.StringIO()):
                code = cloud_check.execute(root, "test-fixture", require_clean=True)
            receipt = json.loads((root / ".workbench/cloud-check.json").read_text())
            self.assertEqual(code, 1)
            self.assertEqual(receipt["checks"][0]["exit_code"], 0)
            self.assertEqual(receipt["source_start"]["commit"], receipt["source_end"]["commit"])
            self.assertTrue(receipt["source_start"]["clean"])
            self.assertFalse(receipt["source_end"]["clean"])
            self.assertEqual(receipt["error"], "clean_checkout_required_at_end")
            with patch.object(cloud_check, "checks", return_value=steps), \
                 contextlib.redirect_stdout(io.StringIO()), \
                 contextlib.redirect_stderr(io.StringIO()):
                code = cloud_check.execute(root, "test-fixture", require_clean=True)
            receipt = json.loads((root / ".workbench/cloud-check.json").read_text())
            self.assertEqual(code, 1)
            self.assertEqual(receipt["checks"], [])
            self.assertEqual(receipt["error"], "clean_checkout_required_at_start")


if __name__ == "__main__":
    unittest.main()
