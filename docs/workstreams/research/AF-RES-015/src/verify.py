"""Reproduce committed study outputs and write a bounded verification receipt."""

import argparse
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
import subprocess
import sys
from urllib.parse import urlsplit

from collect import ROOT, rows

REPO = ROOT.parents[3]
OWNED = ROOT.relative_to(REPO).as_posix()
PIPELINE = ("extract", "restore", "signals", "signal_costs", "simulate", "cost_report", "sources", "report_tables")
GENERATED = ("REASONS.jsonl", "SIGNALS.csv", "sources.json", "results/answer-coverage.csv",
             "results/confusion.json", "results/signal-costs.json", "results/cadence.csv",
             "results/cadence.json", "results/cost.csv", "results/cost.json", "results/reason-types.json")
LOGS = ("repo-now", "repo-signals", "repo-then", "pinned-files", "fixed-evidence",
        "registry", "license-observations", "tag-date-observations", "cost-network")
MANIFEST = json.loads((ROOT / "manifest.json").read_text())


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO)


def run(argv):
    start = utc()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", GIT_TERMINAL_PROMPT="0")
    result = subprocess.run(argv, cwd=REPO, env=env, check=False, capture_output=True, text=True, timeout=120)
    entry = {"argv": argv, "started_at_utc": start, "completed_at_utc": utc(), "exit_code": result.returncode}
    if result.returncode:
        raise SystemExit(json.dumps({**entry, "stderr": result.stderr, "stdout": result.stdout}, ensure_ascii=False))
    return entry, result


def request_records(value):
    if isinstance(value, dict):
        if "requested_at" in value and isinstance(value.get("requests"), int) and value.get("url"):
            yield value
        for child in value.values():
            yield from request_records(child)
    elif isinstance(value, list):
        for child in value:
            yield from request_records(child)


def observations():
    responses = {}
    for filename in LOGS:
        for item in rows(ROOT / "results" / f"{filename}.jsonl"):
            for event in request_records(item):
                responses[(event["requested_at"], event["url"])] = event
    hosts, http = Counter(), Counter()
    for record in responses.values():
        hosts[urlsplit(record["url"]).netloc] += record["requests"]
        code = record.get("http")
        http[str(code) if code is not None else "no_http_status"] += 1
    web = {which: {"operations_logged": len(events), "viewable_flags": sum(x["viewable"] for x in events)}
           for which in ("web-current", "web-history", "web-methods")
           for events in [list(rows(ROOT / "results" / f"{which}.jsonl"))]}
    return {"collector_unique_attempts": len(responses), "collector_known_requests": sum(hosts.values()),
            "collector_requests_by_initial_host": hosts, "collector_terminal_statuses": http,
            "first_probe_attempts": 4, "first_probe_origin_responses": 0,
            "web_operation_log": web,
            "boundary": "하한 집계. 초기 4개와 브라우저 내부 HTTP는 수집기 합계 밖이다. 일부 출처 재열람과 Git 전송은 계측하지 않았다. 호스트 합계는 리다이렉트를 초기 호스트에 더한다.",
            "throttle": "수집기 인스턴스마다 초기 요청을 같은 호스트에 1.06초 이상 간격으로 시작. Retry-After 또는 429는 현재 실행에서 해당 호스트를 보류."}


def fixed_hashes():
    research = "docs/workstreams/research/"
    inputs = {"AF-RES-011": ("CASES.json", "evidence/aging-observations.json", "sources.json", "HANDOFF.md"),
              "AF-RES-009": ("FAILURES.md", "LANDSCAPE.md", "SYSTEMS.json", "HANDOFF.md")}
    checksums = {}
    for upstream in MANIFEST["dependencies"]:
        key = upstream["branch"].split("/research-")[1].upper()
        for source in inputs[key]:
            path = research + key + "/" + source
            sha = upstream["commit"]
            checksums[f"{sha}:{path}"] = sha256(git("show", sha + ":" + path)).hexdigest()
    return checksums


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true", help="verify the current integration contract on GitHub")
    choose = parser.parse_args()
    started, head = utc(), git("rev-parse", "HEAD").decode().strip()
    commands = []
    expected = {f: digest(ROOT / f) for f in GENERATED}
    for script in PIPELINE:
        result, _ = run([sys.executable, f"{OWNED}/src/{script}.py"])
        commands.append(result)
    rebuilt = {f: digest(ROOT / f) for f in GENERATED}
    if rebuilt != expected:
        changed = [f for f in expected if expected[f] != rebuilt[f]]
        raise ValueError(f"Generated artifacts changed in offline replay: {changed}")
    check, tests = run([sys.executable, "-m", "unittest", "discover", "-s", f"{OWNED}/tests", "-v"])
    commands.append({**check, "test_output": tests.stderr.strip().splitlines()})
    argv = [sys.executable, "-m", "workbench.session", "check", f"{OWNED}/manifest.json"]
    if choose.fetch:
        argv.append("--fetch")
    check, result = run(argv)
    contract = json.loads(result.stdout)
    commands.append({**check, "status": contract["status"], "freshness": contract["freshness"]})
    changed = set(git("diff", "--name-only", MANIFEST["base_commit"]).decode().splitlines())
    changed.update(git("ls-files", "--others", "--exclude-standard").decode().splitlines())
    outside = [f for f in changed if not f.startswith(OWNED + "/")]
    if outside or contract["status"] != "passed":
        raise ValueError(f"Contract or ownership check failed: {outside}")
    check, _ = run(["git", "diff", "--check", MANIFEST["base_commit"]])
    commands.append(check)
    inputs = fixed_hashes()
    measure = observations()
    method_totals = json.loads((ROOT / "sources.json").read_text())["summary"]
    api = json.loads((ROOT / "results/access.json").read_text())
    cloud_check = ROOT / "results/workbench-cloud-check.json"
    out = {"schema": 1, "task": "AF-RES-015", "checked_out_commit": head,
           "started_at_utc": started, "completed_at_utc": utc(), "python": sys.version.split()[0],
           "source_commit": MANIFEST["base_commit"],
           "fixed_inputs_sha256": inputs, "data_sha256": {
               path.relative_to(ROOT).as_posix(): digest(path)
               for path in sorted((ROOT / "data").glob("*.txt"))},
           "output_replay_sha256": rebuilt, "offline_outputs_identical": True,
           "checks": commands, "outside_paths": outside, "method_source_counts": method_totals,
           "api_probes": api, "anonymous_api_budget": {
               "api.github.com": {"published_per_hour_per_ip": 60, "remaining_observed": None, "source": "M-RATE"},
               "web.archive.org": {"origin_limit_observed": None, "definition": "M-WAYBACK"},
               "api.deps.dev": {"origin_limit_observed": None, "definition": "M-DEPS"},
               "archive.softwareheritage.org": {"origin_limit_observed": None, "definition": "M-SWHVIS"}},
           "requests": measure,
           "workbench_cloud_check": json.loads(cloud_check.read_text()) if cloud_check.exists() else None,
           "not_executed": ["사람 검토자 계측", "다른 새 모델의 독립 인계", "차단 호스트의 원격 응답", "실사용 제품 빌드·계정·배포"],
           "resumption": "PROGRESS.md 의 입력·명령과 HANDOFF.md 의 다음 첫 행동"}
    (ROOT / "VERIFICATION.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"head": head, "offline_identical": True, "owned_paths": len(changed),
                      "logged_requests": measure["collector_known_requests"],
                      "contract": contract["freshness"], "exact_outputs": len(rebuilt)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
