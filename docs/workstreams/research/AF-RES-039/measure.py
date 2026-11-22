"""Read observations, preserve raw measures and check the execution envelope."""
import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from batch import read_manifest
from prepare import ROOT, sha


def load_lines(path, phase=None):
    records = [json.loads(line) for line in path.read_text().splitlines()]
    return [record for record in records if phase is None or record.get("phase") == phase]


def file_path(capture, event, exchange):
    name = exchange.get("body_file")
    return capture / event["run_id"] / Path(name).name if name else None


def physicals(event):
    return [exchange for request in event["requests"] for exchange in request["exchanges"]]


def measure(event):
    requests = event["requests"]
    shots = physicals(event)
    successful = [exchange for exchange in shots if exchange["status"] == 200 and not exchange["error"]]
    return {
        "order": event["order"], "run_id": event["run_id"], "ref_id": event["ref_id"],
        "task": event["task"], "configuration": event["configuration"], "input_sha256": event["input_sha256"],
        "serialized_input_bytes": event["input_bytes"], "started_utc": event["started_utc"],
        "finished_utc": event["finished_utc"], "provisional_action": event["provisional_action"],
        "logical_gets": len(requests), "http_exchanges": sum(shot["http_exchange"] for shot in shots),
        "application_gets_sent": sum(shot["http_get_sent"] for shot in shots),
        "transfer_invocations": len(shots),
        "proxy_connects": sum(shot["proxy_connect_attempted"] for shot in shots),
        "successful_body_bytes": sum(shot["received_body_bytes"] for shot in successful),
        "total_body_bytes": sum(shot["received_body_bytes"] for shot in shots),
        "displayed_local_H_bytes": event["local_history"]["read_bytes"],
        "validated_local_H_bytes": event["local_history"]["H_bytes_validated_from_input"],
        "H_metadata_read_bytes": event["local_history"]["H_metadata_bytes_parsed"],
        "worker_wall_seconds": event["wall_seconds"],
        "request_seconds_sum": round(sum(req["elapsed_seconds"] for req in requests), 6),
        "tool_wall_seconds": event["supervisor_elapsed_seconds"],
        "tool_exit_code": event["tool_exit_code"],
        "requests_with_errors": sum(bool(req["error"]) for req in requests),
        "failures": ";".join(req["error"] for req in requests if req["error"]),
        "request_urls": ";".join(req["initial_url"] for req in requests),
        "final_urls": ";".join(req["final_url"] for req in requests),
        "sections": ";".join(req["section"].get("locator") or req["section"].get("reason") or ""
                              for req in requests),
        "response_sha256s": ";".join(shot["body_sha256"] or "" for shot in shots),
    }


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def checks(events, captures):
    frozen = {row["run_id"]: row for row in read_manifest()}
    plan = [row["run_id"] for row in frozen.values()]
    assert [row["run_id"] for row in events] == plan
    seen = Counter()
    over_logical = []
    over_deadline = []
    over_strict = []
    for event in events:
        run_id = event["run_id"]
        expected = frozen[run_id]
        assert event["order"] == expected["order"] and event["input_bytes"] == expected["input_bytes"]
        assert event["input_sha256"] == expected["input_sha256"] == event["input_expected_sha256"]
        assert event["B_sha256"] == expected["B_sha256"]
        assert event["initial_directory"] == event["cwd_before_read"] == ["replay.py", "store.json"]
        assert not event["file_access"]["unexpected_workspace_or_tmp_open_paths"]
        assert event["tool_exit_code"] == 0
        assert event["logical_gets"] == len(event["requests"])
        if event["logical_gets"] > 2:
            over_logical.append(run_id)
        if event["http_exchanges"] > 2:
            over_strict.append(run_id)
        for request in event["requests"]:
            if request["elapsed_seconds"] > 30:
                over_deadline.append((run_id, request["logical"], request["elapsed_seconds"]))
            for exchange in request["exchanges"]:
                path = file_path(captures, event, exchange)
                if path:
                    data = path.read_bytes()
                    assert len(data) == exchange["received_body_bytes"]
                    assert sha(data) == exchange["body_sha256"]
                    seen["response_body_files_verified"] += 1
                if exchange.get("curl_size_download") is not None:
                    assert exchange["curl_size_download"] == exchange["received_body_bytes"]
                    seen["curl_byte_counter_matches"] += 1
                seen[exchange["error"] or f"status_{exchange['status']}"] += 1
        if event["local_history"]["displayed"]:
            data = (captures / run_id / "local-H.txt").read_bytes()
            assert event["local_history"]["read_bytes"] == len(data) == expected["H_bytes"]
            assert expected["H_sha256"] == sha(data) == event["local_history"]["H_sha256"]
            seen["displayed_H_files_verified"] += 1
    pair_gaps = [
        (datetime.fromisoformat(b["supervisor_started_utc"]) - datetime.fromisoformat(a["supervisor_finished_utc"])).total_seconds()
        for a, b in zip(events[::2], events[1::2])
    ]
    return {
        "runs": len(events), "pairs": len(pair_gaps), "body_checks": dict(seen),
        "over_two_logical_gets": over_logical, "elapsed_over_30s": over_deadline,
        "over_two_document_http_exchanges": over_strict, "max_within_pair_idle_seconds": max(pair_gaps),
        "run_exit_codes": dict(Counter(row["tool_exit_code"] for row in events)),
        "observed_window_utc": [events[0]["supervisor_started_utc"], events[-1]["supervisor_finished_utc"]],
        "batch_elapsed_seconds": (
            datetime.fromisoformat(events[-1]["supervisor_finished_utc"])
            - datetime.fromisoformat(events[0]["supervisor_started_utc"])
        ).total_seconds(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture_dir", type=Path)
    args = parser.parse_args()
    source = ROOT / "attempts.jsonl"
    events = load_lines(source, "main")
    raw = [measure(row) for row in events]
    write_csv(ROOT / "runs.csv", raw)
    receipt = {
        "phase": "main queries, before grader and simulation",
        "commands": [
            "python -B batch.py main --capture-dir /tmp/af039-main-2982044 --journal attempts.jsonl",
            "python -B measure.py /tmp/af039-main-2982044",
        ],
        "observed_runner_commit": "2982044f4fb1cb7de4b7f239c193f7f95bcf7d40",
        "attempts_prefix_sha256": sha(b"".join(source.read_bytes().splitlines(keepends=True)[:48])),
        "raw_runs_csv_sha256": sha((ROOT / "runs.csv").read_bytes()),
        **checks(events, args.capture_dir),
    }
    (ROOT / "evidence/raw-observations.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
