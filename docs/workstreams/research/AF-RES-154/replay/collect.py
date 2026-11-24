import argparse
import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path


MATRIX = [
    (f"R{repeat}-{setting}-{fixture}", f"R{repeat}-{setting}", repeat, setting, fixture)
    for repeat in (1, 2) for setting in ("D", "A") for fixture in ("UT", "UI", "ST", "SI")
]
CONTROLS = [
    (f"R{repeat}-A-{label}", f"R{repeat}-A", repeat, "A", "WT")
    for repeat in (1, 2) for label in ("W", "R", "DUP")
] + [("S1-X-SI", "S1-X", 1, "X", "SI")]


def load(path):
    return json.loads(path.read_text())


def docker_events(group, receipt):
    start = datetime.fromisoformat(receipt["moved_utc"])
    end = start + timedelta(seconds=receipt["process_seconds_to_task_terminal_including_poll"] + 0.3)
    output = []
    for descriptor in ("stdout", "stderr"):
        fn = group / f"container.{descriptor}"
        if not fn.exists():
            continue
        for i, line in enumerate(fn.read_text().splitlines(), 1):
            try:
                stamp = datetime.fromisoformat(line.split()[0])
            except (IndexError, ValueError):
                continue
            if start <= stamp <= end and (
                "Output file is a PDF/A" in line or "digital signatures will be invalidated" in line
            ):
                output.append({"fd": descriptor, "line": i, "message": line})
    return output


def as_row(entry, raw, task):
    run_id, group, repeat, setting, fixture = entry
    run_source = raw / group / run_id
    evidence = task / "evidence" / "runtime" / group / run_id
    base = {
        "run_id": run_id, "repeat": repeat, "setting": setting, "fixture_id": fixture,
        "paperless": "2.2.1", "input_route": "inotify consume folder → Celery", "planned": entry in MATRIX,
    }
    if not (run_source / "receipt.json").is_file():
        errors = raw / "harness-errors.json"
        messages = [e["error"] for e in load(errors) if e["group"] == group] if errors.is_file() else []
        return {**base, "status": "unobserved", "missing_reason": "; ".join(messages) or "No complete receipt"}
    evidence.mkdir(parents=True, exist_ok=True)
    for name in ("receipt.json", "paperless.log", "celery.log", "tesseract.tsv"):
        shutil.copyfile(run_source / name, evidence / name)
    receipt = load(run_source / "receipt.json")
    downloads = {}
    for name, response in receipt["downloads"].items():
        downloads[name] = {key: response[key] for key in (
            "route", "sha256", "bytes", "bytes_equal", "page_text", "signatures",
            "download_seconds", "verify_seconds", "status",
        )}
        if not response["bytes_equal"]:
            shutil.copyfile(run_source / f"{name}.pdf", evidence / f"{name}.pdf")
    return {
        **base,
        "status": receipt["status"],
        "queue_observed": receipt["queued_log"],
        "celery_status": receipt["task"]["status"],
        "celery_result": json.loads(receipt["task"]["result"]),
        "input": receipt["input"],
        "wrapper_count": receipt["wrapper"]["count"],
        "wrapper_early_return": receipt["wrapper"]["early_return_log"],
        "tesseract_starts": receipt["engine"]["process_starts"],
        "tesseract_exit_zero": receipt["engine"]["process_exit_zero"],
        "db_counts": [receipt["db_count_before"], receipt["db_count_after"]],
        "consume_stays": receipt["consume_path_after"]["exists"],
        "consume_after": receipt["consume_path_after"],
        "provider_after": receipt["provider_path_after"],
        "stored_original": receipt["stored"]["original"] if receipt["stored"] else None,
        "stored_archive": receipt["stored"]["archive"] if receipt["stored"] else None,
        "indexed_text": receipt["stored"]["api_indexed_text"] if receipt["stored"] else None,
        "process_seconds": receipt["process_seconds_to_task_terminal_including_poll"],
        "stage_seconds": receipt["stage_seconds"],
        "preflight": receipt["preflight"],
        "pdfa_service_log": docker_events(raw / group, receipt),
        "downloads": downloads,
        "download_missing_reason": None if downloads else "No document from failed intake",
        "evidence": str((evidence / "receipt.json").relative_to(task)),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--task", type=Path, required=True)
    parser.add_argument("--phase", choices=("matrix", "full"), required=True)
    args = parser.parse_args()
    raw = args.raw.resolve()
    task = args.task.resolve()
    entries = MATRIX if args.phase == "matrix" else MATRIX + CONTROLS
    groups = dict.fromkeys(entry[1] for entry in entries)
    for group in groups:
        source = raw / group
        target = task / "evidence" / "runtime" / group
        target.mkdir(parents=True, exist_ok=True)
        names = ["startup.json", "cleanup.json", "container.stdout", "container.stderr",
                 "versions.stdout", "versions.stderr"]
        if args.phase == "full":
            names.append("write-retry.json")
        for name in names:
            if (source / name).is_file():
                shutil.copyfile(source / name, target / name)
    shutil.copyfile(raw / "platform.json", task / "evidence" / "runtime" / "platform.json")
    rows = [as_row(entry, raw, task) for entry in entries]
    (task / "runs.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
    print(f"{sum(r['status'] != 'unobserved' for r in rows)}/{len(rows)} evidence rows")


if __name__ == "__main__":
    main()
