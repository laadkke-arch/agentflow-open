"""Join the recorded pip outputs and verify results against the frozen predictions."""

import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit

from run import INPUTS, LOCAL_PROJECT, WHEEL_PREFIX, case_plan, digest, dump, read_fixtures, read_json

WARNING = "The candidate selected for download or install is a yanked version:"
REASON = "Reason for being yanked: "
IGNORED = "Ignored the following yanked versions:"
REJECTED = "No matching distribution found for "
NO_SELECTION = "해당 없음"
UNVERIFIED = "미확인"

FIELDS = [
    "group", "run_id", "request_id", "requirement", "index", "repeat", "target_attribute",
    "target_reason", "served_page_sha256", "outcome", "selected_version", "selected_filename",
    "selected_sha256", "report_url", "report_is_yanked", "selected_warning_stderr_count",
    "selected_warning_stdout_count", "warning_reason_stderr", "ignored_yanked_diagnostic_count",
    "pip_exit", "http_project_gets", "http_wheel_gets", "cause", "receipt",
]


def summarize_run(path, case, inputs, pages):
    group, request_id, requirement, variant, repeat = case
    run_id = f"{request_id}-{variant}-r{repeat}"
    target = next(item for item in inputs["wheels"] if item["version"] == inputs["target_version"])
    status = {"baseline": "문자열", "unmarked": "속성 없음", "empty": "빈 속성값", "missing": "링크 부재"}
    reason = {"baseline": target["version_json"]["yanked_reason"], "empty": '""'}
    row = dict.fromkeys(FIELDS, UNVERIFIED)
    row.update(group=group, run_id=run_id, request_id=request_id, requirement=requirement,
               index=variant, repeat=repeat, target_attribute=status[variant],
               target_reason=reason.get(variant, NO_SELECTION), receipt=f"{path.name}/{run_id}/")
    errors = []
    case_path = path / run_id

    def expect(condition, message):
        if not condition:
            errors.append(message)

    try:
        info = read_json(case_path / "run.json")
        expect(info["status"] == "observed", str(info.get("error", info["status"])))
        expect(info["requirement"] == requirement and info["variant"] == variant, "case mapping")
        expect(info["group"] == group and info["repeat"] == repeat, "group/repeat")
        row["served_page_sha256"] = info["index_sha256"]
        expect(row["served_page_sha256"] == digest(pages[variant]), "page hash")
        index = urlsplit(info["index_url"])
        expect(index.scheme == "http" and index.hostname == "127.0.0.1"
               and index.path == "/simple/" and index.port is not None, "loopback URL")
        r = info["resolver"]
        row["pip_exit"] = r["exit_code"]
        stdout = (case_path / "stdout.txt").read_bytes()
        stderr = (case_path / "stderr.txt").read_bytes()
        expect(r["stdout_sha256"] == digest(stdout) and r["stderr_sha256"] == digest(stderr), "stream SHA-256")
        stdout, stderr = stdout.decode("utf-8"), stderr.decode("utf-8")
        row["selected_warning_stderr_count"] = stderr.count(WARNING)
        row["selected_warning_stdout_count"] = stdout.count(WARNING)
        reasons = [line.split(REASON, 1)[1] for line in stderr.splitlines() if REASON in line]
        row["warning_reason_stderr"] = " / ".join(reasons) if reasons else NO_SELECTION
        row["ignored_yanked_diagnostic_count"] = stderr.count(IGNORED) + stdout.count(IGNORED)
        expect(len(reasons) == row["selected_warning_stderr_count"], "warning reason association")
        expect(not r["timed_out"] and not row["selected_warning_stdout_count"], "command timeout or warning in different channel")
        args = r["argv"]
        options = {"--dry-run", "--ignore-installed", "--no-deps", "--only-binary=:all:",
                   "--no-cache-dir", "--report", "--index-url", "--disable-pip-version-check"}
        expect(options <= set(args) and args[-1] == requirement
               and args[args.index("--index-url") + 1] == info["index_url"], "command options")
        expect(set(info["environment"]) & {"PIP_INDEX_URL", "PIP_EXTRA_INDEX_URL", "PIP_FIND_LINKS",
               "HTTP_PROXY", "HTTPS_PROXY", "PYTHONPATH"} == set(), "inherited setting")
        expect(info["environment"]["PIP_CONFIG_FILE"] in ("/dev/null", "nul"), "config is disabled")
        preflight = info["preflight"]
        before, after = (preflight[f"inventory_{when}"] for when in ("before", "after"))
        inventory = {"python":inputs["python_version"], "is_venv":True, "packages":{"pip":inputs["pip"]["version"]}}
        expect(json.loads(before["stdout"]) == json.loads(after["stdout"]) == inventory, "environment inventory")
        expect(all(k["exit_code"] == 0 for k in preflight.values()), "bootstrap exit")
        events = [json.loads(line) for line in (case_path / "http.jsonl").read_text(encoding="utf-8").splitlines()]
        projects = [event for event in events if event["path"] == LOCAL_PROJECT]
        wheels = [event for event in events if event["path"].startswith(WHEEL_PREFIX)]
        row["http_project_gets"] = sum(event["method"] == "GET" for event in projects)
        row["http_wheel_gets"] = sum(event["method"] == "GET" for event in wheels)
        expect(len(events) == len(projects) + len(wheels)
               and all(event["host"] == index.netloc and event["method"] == "GET" and event["status"] == 200
                       and event["body_bytes_sent"] == event["content_length"] for event in events), "unexpected HTTP access")
        expect(len(projects) == 1 and projects[0]["representation_sha256"] == row["served_page_sha256"],
               "served project content")
        report_path = case_path / "report.json"
        if report_path.is_file():
            report = read_json(report_path)
            expect(info["report_sha256"] == digest(report_path.read_bytes()), "report SHA-256")
            expect(report["version"] == "1" and report["pip_version"] == inputs["pip"]["version"]
                   and report["environment"]["python_full_version"] == inputs["python_version"]
                   and len(report["install"]) == 1, "report version/environment/cardinality")
            result = report["install"][0]
            version = result["metadata"]["version"]
            candidate = next((item for item in inputs["wheels"] if item["version"] == version), None)
            url = result["download_info"]["url"]
            download = urlsplit(url)
            sha = result["download_info"]["archive_info"]["hashes"]["sha256"]
            row.update(outcome="selected", selected_version=version, selected_filename=Path(download.path).name,
                       selected_sha256=sha, report_url=url, report_is_yanked=result["is_yanked"])
            expect(row["pip_exit"] == 0 and result["is_direct"] is False and result["requested"] is True
                   and result["metadata"]["name"].lower() == inputs["project"], "report flags/exit")
            expect(download.scheme == index.scheme and download.netloc == index.netloc
                   and not (download.query or download.fragment), "report URL origin")
            expect(candidate is not None and candidate["filename"] == row["selected_filename"]
                   and candidate["sha256"] == sha, "artifact identity")
            expect(len(wheels) == 1 and wheels[0]["path"] == download.path
                   and wheels[0]["representation_sha256"] == sha, "reported vs served wheel")
            expect(f'Would install pytest-{version}' in stdout, "would-install stdout")
            if row["selected_warning_stderr_count"]:
                expect(f"version {version} at {url}" in stderr, "warning identifies same file")
        elif row["pip_exit"] != 0 and REJECTED + requirement in stderr and not wheels:
            row.update(outcome="resolver_rejected", selected_version=NO_SELECTION, selected_filename=NO_SELECTION,
                       selected_sha256=NO_SELECTION, report_url=NO_SELECTION, report_is_yanked=NO_SELECTION)
        else:
            row["outcome"] = "unverified"
            errors.append("no report and no recognized resolver rejection")

        expected_version = {
            "pin-target": inputs["target_version"] if variant != "missing" else NO_SELECTION,
            "range-exclusive": "8.0.2" if variant == "baseline" else "8.1.0",
            "range-inclusive": "8.1.1", "pin-next": "8.1.1",
        }[request_id]
        marked_selected = request_id == "pin-target" and variant in ("baseline", "empty")
        expected_reason = {"baseline":reason["baseline"], "empty":"<none given>"}
        expect(row["selected_version"] == expected_version, "frozen prediction: selected version")
        expect(row["report_is_yanked"] == (NO_SELECTION if variant == "missing" else marked_selected),
               "frozen prediction: report is_yanked")
        expect(row["selected_warning_stderr_count"] == int(marked_selected)
               and row["warning_reason_stderr"] == (expected_reason[variant] if marked_selected else NO_SELECTION),
               "frozen prediction: stderr warning")
        expect(row["pip_exit"] == (1 if variant == "missing" else 0)
               and row["ignored_yanked_diagnostic_count"] == 0, "frozen prediction: exit or diagnostics")
        if not errors:
            if row["outcome"] == "resolver_rejected":
                why = "대상 링크가 빠져 정확판을 충족하는 후보 0"
            elif marked_selected:
                why = "정확 핀에서 유일한 적용 후보가 철회 상태로 남음"
            elif request_id == "range-exclusive" and variant == "baseline":
                why = "범위 내 철회 파일을 건너뛰고 비철회 8.0.2 선택"
            elif request_id == "range-exclusive":
                why = "속성 제거 후 범위 내 최대 호환 후보 선택"
            elif request_id == "range-inclusive":
                why = "범위 내 최대 비철회 후보 선택"
            else:
                why = "정확 버전을 만족하는 비철회 파일 선택"
            row["cause"] = why
    except (OSError, KeyError, ValueError, IndexError) as error:
        errors.append(f"{type(error).__name__}: {error}")
    return row, errors


def write_csv(path, rows):
    with path.open("x", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_suite(path, inputs, pages):
    suite = read_json(path / "suite.json")
    group = suite["group"]
    checks = {
        "inputs_sha256": digest(INPUTS.read_bytes()),
        "runner_sha256": digest((INPUTS.parent / "run.py").read_bytes()),
        "pip_wheel_sha256": inputs["pip"]["sha256"],
        "project_page_sha256": {key:digest(value) for key, value in pages.items()},
        "wheel_sha256": {item["filename"]:item["sha256"] for item in inputs["wheels"]},
    }
    results = [summarize_run(path, case, inputs, pages) for case in case_plan(inputs, group)]
    rows = [row for row, _ in results]
    errors = {row["run_id"]: errors for row, errors in results if errors}
    if any(suite[key] != value for key, value in checks.items()):
        errors["suite_fingerprint"] = checks
    if suite["planned"] != len(rows) or suite["run_ids"] != [row["run_id"] for row in rows]:
        errors["coverage"] = "planned IDs differ from observed suite manifest"
    return group, rows, errors


def semantics(rows):
    skip = {"report_url", "receipt"}
    return {row["run_id"]: {key: value for key, value in row.items() if key not in skip} for row in rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", action="append", required=True, type=Path)
    parser.add_argument("--replay", type=Path)
    parser.add_argument("--main-csv", type=Path)
    parser.add_argument("--controls-csv", type=Path)
    parser.add_argument("--summary", required=True, type=Path)
    args = parser.parse_args()
    inputs = read_json(INPUTS)
    pages, _ = read_fixtures(inputs)
    groups = [read_suite(path, inputs, pages) for path in args.suite]
    rows = [row for _, group_rows, _ in groups for row in group_rows]
    errors = {group: issues for group, _, issues in groups if issues}
    if args.main_csv is not None:
        write_csv(args.main_csv, [row for row in rows if row["group"] == "main"])
    if args.controls_csv is not None:
        write_csv(args.controls_csv, [row for row in rows if row["group"] == "controls"])
    summary = {
        "argv": sys.argv, "status": "failed" if errors else "passed", "errors": errors,
        "observed_rows": len(rows), "by_group": dict(Counter(row["group"] for row in rows)),
        "by_outcome": dict(Counter(row["outcome"] for row in rows)),
        "warned_run_ids": [row["run_id"] for row in rows if row["selected_warning_stderr_count"] == 1],
        "http_wheel_gets": sum(row["http_wheel_gets"] for row in rows if isinstance(row["http_wheel_gets"], int)),
    }
    if args.replay is not None:
        _, replay, replay_errors = read_suite(args.replay, inputs, pages)
        first, second = semantics(rows), semantics(replay)
        mismatches = sorted(key for key in first.keys() | second.keys() if first.get(key) != second.get(key))
        summary["replay"] = {
            "observed_rows": len(replay), "matched_run_ids": sorted(first.keys() - set(mismatches)),
            "mismatched_run_ids": mismatches, "errors": replay_errors,
            "normalized": ["ephemeral loopback port", "receipt path", "timestamps and filesystem paths"],
        }
        if replay_errors or mismatches:
            summary["status"] = "failed"
    dump(args.summary, summary)
    print(f'{summary["status"]}: {summary["observed_rows"]} rows, {len(summary["warned_run_ids"])} selection warnings')
    return 0 if summary["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
