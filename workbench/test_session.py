"""Real disposable Git repositories exercise stale handoffs and integration.

These are Git/worktree tests on the executing machine, not independent AI chats.
No remote service, model, Docker daemon, or user PC is contacted.
"""
import json
import contextlib
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from workbench import session


class SessionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="workbench-session-")
        self.addCleanup(self.tmp.cleanup)
        self.parent = Path(self.tmp.name)
        self.seed = self.parent / "seed"
        self.seed.mkdir()
        self.git(self.seed, "init", "-q", "-b", session.INTEGRATION)
        self.identity(self.seed)
        self.write(self.seed, ".gitignore", ".workbench/\n__pycache__/\n*.pyc\n")
        self.write(self.seed, ".gitattributes", "* text=auto eol=lf\n")
        files = ["docs/product/README.md", "docs/collaboration/README.md"]
        self.write(self.seed, session.CONTRACT, json.dumps({"schema": 1, "version": "1", "files": files}) + "\n")
        for name in files:
            self.write(self.seed, name, "Reviewed baseline.\n")
        self.write(self.seed, "docs/workstreams/shared/value.txt", "baseline\n")
        self.save(self.seed, "initial contract")
        self.remote = self.parent / "remote.git"
        self.git(self.parent, "clone", "-q", "--bare", str(self.seed), str(self.remote))
        self.git(self.seed, "remote", "add", "origin", str(self.remote))
        self.root = self.parent / "worker"
        self.git(self.parent, "clone", "-q", str(self.remote), str(self.root))
        self.identity(self.root)

    def git(self, root, *args, check=True):
        proc = subprocess.run(["git", *args], cwd=root, capture_output=True,
                              text=True, encoding="utf-8", timeout=30)
        if check:
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return proc

    def identity(self, root):
        self.git(root, "config", "user.name", "Workbench fixture")
        self.git(root, "config", "user.email", "fixture@example.invalid")
        self.git(root, "config", "core.autocrlf", "false")

    def write(self, root, relative, text):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def save(self, root, message):
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", message)
        return self.git(root, "rev-parse", "HEAD").stdout.strip()

    def task(self, root=None, task_id="example", allowed=None, **kwargs):
        root = root or self.root
        allowed = allowed or ["docs/workstreams/example/"]
        manifest = session.start_task(root, task_id, allowed, **kwargs)
        name = session.TASK_DIR + "/" + task_id + ".json"
        self.write(root, name, json.dumps(manifest, indent=2) + "\n")
        return name, manifest

    def test_empty_queue_is_not_a_collaboration_pass(self):
        result = session.check_all(self.root)
        self.assertEqual(result["status"], "not-executed")
        self.assertEqual(result["reason"], "no_active_sessions")
        self.assertEqual(result["freshness"], "not_checked")
        (self.root / "docs/product/README.md").unlink()
        with self.assertRaises(ValueError):
            session.check_all(self.root)

    def test_remote_contract_drift_without_version_bump_is_detected(self):
        name, task = self.task(fetch=True)
        self.assertEqual(task["freshness_at_start"], "remote_checked")
        self.write(self.seed, "docs/product/README.md", "A new required data field.\n")
        self.save(self.seed, "change shared contract without version bump")
        self.git(self.seed, "push", "-q", "origin", session.INTEGRATION)
        cached = session.check_task(self.root, name)
        self.assertEqual(cached["status"], "passed")
        self.assertEqual(cached["freshness"], "local_only")
        fresh = session.check_task(self.root, name, fetch=True)
        self.assertEqual(fresh["status"], "failed")
        self.assertEqual(fresh["freshness"], "remote_checked")
        self.assertTrue(any("integration contract changed" in item for item in fresh["errors"]))
        with self.assertRaisesRegex(ValueError, "working contract differs"):
            session.start_task(self.root, "stale-start", ["docs/workstreams/example/"], fetch=True)

    def test_committed_and_untracked_out_of_scope_changes_fail(self):
        name, _ = self.task()
        self.write(self.root, "docs/workstreams/example/answer.md", "allowed\n")
        self.write(self.root, "protected.txt", "outside ownership\n")
        self.save(self.root, "task changes")
        self.write(self.root, "another-task.txt", "untracked\n")
        result = session.check_task(self.root, name)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["outside_paths"], ["another-task.txt", "protected.txt"])
        self.assertNotIn(name, result["outside_paths"])

    def test_exact_dependency_pin_detects_a_new_remote_result(self):
        self.git(self.seed, "switch", "-qc", "work/dependency")
        self.write(self.seed, "dependency.txt", "result one\n")
        dependency = self.save(self.seed, "dependency one")
        self.git(self.seed, "push", "-q", "origin", "work/dependency")
        name, _ = self.task(dependencies=["work/dependency=" + dependency], fetch=True)
        self.write(self.seed, "dependency.txt", "result two\n")
        self.save(self.seed, "dependency two")
        self.git(self.seed, "push", "-q", "origin", "work/dependency")
        result = session.check_task(self.root, name, fetch=True)
        self.assertEqual(result["status"], "failed")
        self.assertIn("dependency changed: work/dependency", result["errors"])

    def test_ignored_run_outputs_do_not_become_task_changes(self):
        name, _ = self.task()
        self.write(self.root, ".workbench/runs/receipt.json", '{"status":"example"}\n')
        result = session.check_task(self.root, name)
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["changed_paths"], [])
        with self.assertRaises(ValueError):
            session.start_task(self.root, "escape", ["../other/"])

    def worktree(self, name):
        path = self.parent / name
        self.git(self.root, "worktree", "add", "-qb", name, str(path))
        self.addCleanup(lambda: self.git(self.root, "worktree", "remove", "--force", str(path), check=False))
        return path

    def test_independent_worktrees_merge_without_borrowing_ownership(self):
        a, b = self.worktree("task-a"), self.worktree("task-b")
        a_name, _ = self.task(a, "task-a", ["docs/workstreams/a/"])
        b_name, _ = self.task(b, "task-b", ["docs/workstreams/b/"])
        self.write(a, "docs/workstreams/a/result.md", "A result\n")
        self.write(b, "docs/workstreams/b/result.md", "B result\n")
        self.save(a, "A task")
        self.save(b, "B task")
        self.assertEqual(session.check_task(a, a_name)["status"], "passed")
        self.assertEqual(session.check_task(b, b_name)["status"], "passed")
        self.git(self.root, "merge", "--no-ff", "-qm", "integrate A", "task-a")
        self.git(self.root, "push", "-q", "origin", session.INTEGRATION)
        self.git(b, "merge", "--no-ff", "-qm", "refresh accepted A", session.INTEGRATION)
        # B sees A's accepted task but must only check its own unintegrated work.
        result = session.check_all(b, fetch=True)
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["integrated_tasks"], ["task-a"])
        self.git(self.root, "merge", "--no-ff", "-qm", "integrate B", "task-b")
        self.git(self.root, "push", "-q", "origin", session.INTEGRATION)
        self.assertTrue((self.root / "docs/workstreams/a/result.md").is_file())
        self.assertTrue((self.root / "docs/workstreams/b/result.md").is_file())
        result = session.check_all(self.root, fetch=True)
        self.assertEqual(result["status"], "not-executed")
        self.assertEqual(result["reason"], "already_integrated")

    def test_conflicting_worktree_merge_fails_and_can_be_aborted(self):
        a, b = self.worktree("conflict-a"), self.worktree("conflict-b")
        shared = "docs/workstreams/shared/value.txt"
        a_name, _ = self.task(a, "conflict-a", [shared])
        b_name, _ = self.task(b, "conflict-b", [shared])
        self.write(a, shared, "A changes the same line\n")
        self.write(b, shared, "B changes the same line\n")
        self.save(a, "A shared edit")
        self.save(b, "B shared edit")
        self.assertEqual(session.check_task(a, a_name)["status"], "passed")
        self.assertEqual(session.check_task(b, b_name)["status"], "passed")
        self.git(self.root, "merge", "--no-ff", "-qm", "accept A", "conflict-a")
        before = session.commit(self.root, "HEAD")
        failed = self.git(self.root, "merge", "--no-ff", "-m", "try B", "conflict-b", check=False)
        self.assertNotEqual(failed.returncode, 0)
        result = session.check_task(self.root, b_name)
        self.assertEqual(result["status"], "failed")
        self.assertIn(shared, result["unmerged_paths"])
        self.git(self.root, "merge", "--abort")
        self.assertEqual(session.commit(self.root, "HEAD"), before)
        self.assertFalse(self.git(self.root, "status", "--porcelain").stdout.strip())

    def test_reusing_an_integrated_task_for_new_changes_requires_a_new_pin(self):
        accepted = self.worktree("accepted-a")
        self.task(accepted, "accepted-a", ["docs/workstreams/a/"])
        self.write(accepted, "docs/workstreams/a/result.md", "accepted result\n")
        self.save(accepted, "A task")
        self.git(self.root, "merge", "--no-ff", "-qm", "integrate A", "accepted-a")
        self.git(self.root, "push", "-q", "origin", session.INTEGRATION)
        continued = self.worktree("continue-accepted-a")
        self.write(continued, "protected.txt", "new work outside the accepted task\n")
        self.save(continued, "reuse accepted manifest for unrelated work")
        # Exercise the actual CLI exit status in a fresh Python process, too.
        proc = subprocess.run([
            sys.executable, "-c",
            "import sys; from pathlib import Path; from workbench import session; "
            "session.ROOT = Path(sys.argv[1]); "
            "raise SystemExit(session.main(['check-all', '--fetch']))",
            str(continued)], cwd=Path(__file__).resolve().parents[1], capture_output=True,
            text=True, encoding="utf-8", timeout=30)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        result = json.loads(proc.stdout)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["reason"], "new_task_pin_required")
        self.assertEqual(result["count"], 0)
        self.assertEqual(result["integrated_tasks"], ["accepted-a"])
        self.assertEqual(result["changed_paths"], ["protected.txt"])

    def test_changed_task_cannot_use_itself_as_the_baseline(self):
        name, _ = self.task()
        self.write(self.root, "outside.txt", "must remain visible\n")
        self.save(self.root, "outside task ownership")
        with self.assertRaisesRegex(ValueError, "against itself"):
            session.check_task(self.root, name, integration_ref="HEAD")
        with self.assertRaisesRegex(ValueError, "against itself"):
            session.check_all(self.root, integration_ref="HEAD")
        # A precise older baseline remains a local-only reproducibility check.
        baseline = self.git(self.root, "rev-parse", "HEAD^").stdout.strip()
        result = session.check_task(self.root, name, integration_ref=baseline)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["freshness"], "local_only")

    def test_cli_creates_a_manifest_once_without_overwriting_it(self):
        args = ["start", "cli-example", "--allow", "docs/workstreams/example/",
                "--output", "docs/tasks/cli-example.json"]
        output = io.StringIO()
        with patch.object(session, "ROOT", self.root), contextlib.redirect_stdout(output):
            self.assertEqual(session.main(args), 0)
        manifest = self.root / "docs/tasks/cli-example.json"
        original = manifest.read_bytes()
        self.assertEqual(json.loads(output.getvalue())["freshness_at_start"], "local_only")
        output = io.StringIO()
        with patch.object(session, "ROOT", self.root), contextlib.redirect_stdout(output):
            self.assertEqual(session.main(args), 2)
        self.assertEqual(json.loads(output.getvalue())["status"], "invalid")
        self.assertEqual(manifest.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
