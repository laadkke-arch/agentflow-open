import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

from collect import CONTROLS, MATRIX, as_row


FIELDS = {
    "source_id", "work_id", "links", "type", "publisher", "url", "fixed_url", "version",
    "checked_utc", "locations", "confirmed", "limits", "evidence", "opened", "counted", "reason",
}
REQS = {"R-IN", "R-BYTE", "R-OCR", "R-LOG", "SIG", "TRUST", "PATH"}


def jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def sig_result(input_row, downloads):
    for result in downloads.values():
        if result["bytes_equal"]:
            assert result["signatures"] == input_row["signatures"]
            assert result["page_text"] == input_row["page_text"]


def describe(rows):
    return {
        "intakes": len(rows),
        "outcomes": dict(Counter(row["status"] for row in rows)),
        "downloads": sum(len(row["downloads"]) for row in rows),
        "wrapper": sum(row["wrapper_count"] for row in rows),
        "recognition": sum(row["tesseract_starts"]["recognition"] for row in rows),
    }


def verify_sources(task):
    sources = jsonl(task / "sources.jsonl")
    ids = {row["source_id"] for row in sources}
    assert len(ids) == len(sources)
    assert all(FIELDS <= row.keys() for row in sources)
    assert all(row["opened"] or not row["counted"] for row in sources)
    counted = [row for row in sources if row["counted"]]
    assert len({row["work_id"] for row in counted}) == len(counted) >= 20
    counts = Counter(row["type"] for row in counted)
    assert counts["사건"] >= 4 and counts["실행 계약"] >= 6
    assert sum(counts[key] for key in ("공개 시험", "검증 도구", "입력 생성 명세", "입력 검증 명세")) >= 6
    assert counts["기록보존 사례"] >= 2 and counts["연구데이터 사례"] >= 2
    return ids, {"rows": len(sources), "counted": len(counted), "types": dict(counts)}


def verify_artifacts(task):
    fixtures = {row["fixture_id"]: row for row in jsonl(task / "fixtures.jsonl")}
    source_ids, sources = verify_sources(task)
    for fixture in fixtures.values():
        data = (task / fixture["file"]).read_bytes()
        assert sha(data) == fixture["sha256"] and len(data) == fixture["bytes"]
        assert set(fixture["source_ids"]) <= source_ids
    for key in ("ST", "SI"):
        trust, = fixtures[key]["signatures"]["fixture_ca"]
        empty, = fixtures[key]["signatures"]["no_anchors"]
        assert trust["intact"] and trust["valid"] and trust["trusted"]
        assert empty["intact"] and empty["valid"] and not empty["trusted"]
        assert trust["coverage"] == "ENTIRE_FILE" == empty["coverage"]
    assert not fixtures["INVALID"]["signatures"]["fixture_ca"][0]["intact"]
    assert fixtures["INVALID"]["pdfsig"]["exit_code"] == 0
    certificate = (task / "replay/fixtures/qa-root.crt").read_bytes()
    assert b"BEGIN CERTIFICATE" in certificate and b"PRIVATE KEY" not in certificate

    rows = jsonl(task / "runs.jsonl")
    index = {row["run_id"]: row for row in rows}
    assert list(index) == [entry[0] for entry in MATRIX + CONTROLS]
    for row in rows:
        fixture = fixtures[row["fixture_id"]]
        assert row["queue_observed"]
        assert row["input"] == {"sha256": fixture["sha256"], "bytes": fixture["bytes"]}
        assert row["provider_after"] == row["input"]
        assert row["tesseract_starts"]["recognition"] == row["tesseract_exit_zero"]["recognition"]
        evidence = task / row["evidence"]
        receipt = json.loads(evidence.read_text())
        assert receipt["run_id"] == row["run_id"]
        assert len(receipt["celery_terminal_lines"]) == 1
        if row["status"] == "success":
            assert row["db_counts"][1] == row["db_counts"][0] + 1
            assert not row["consume_stays"]
            assert set(row["downloads"]) == {"original", "default"}
            assert row["stored_original"]["exists"]
            assert row["stored_original"]["sha256"] == fixture["sha256"]
            assert row["downloads"]["original"]["bytes_equal"]
            sig_result(fixture, row["downloads"])
            for key, response in row["downloads"].items():
                assert response["status"] == 200
                pdf = task / fixture["file"] if response["bytes_equal"] else evidence.parent / f"{key}.pdf"
                data = pdf.read_bytes()
                assert len(data) == response["bytes"] and sha(data) == response["sha256"]
        else:
            assert row["status"] == "failure" and row["db_counts"][1] == row["db_counts"][0]
            assert not row["downloads"] and row["download_missing_reason"]
            assert row["consume_stays"] and row["consume_after"]["sha256"] == fixture["sha256"]
    for n in (1, 2):
        for mode, fixture, status, wrapper, engine in (
            ("D", "UT", "success", 1, 0), ("D", "UI", "success", 1, 1),
            ("D", "ST", "failure", 2, 0), ("D", "SI", "failure", 2, 0),
            ("A", "UT", "success", 0, 0), ("A", "UI", "success", 1, 1),
            ("A", "ST", "success", 0, 0), ("A", "SI", "failure", 2, 0),
        ):
            row = index[f"R{n}-{mode}-{fixture}"]
            assert row["status"] == status and row["wrapper_count"] == wrapper
            assert row["tesseract_starts"]["recognition"] == engine
            if status == "failure":
                assert "DigitalSignatureError" in str(row["celery_result"])
            elif mode == "A":
                assert not row["stored_archive"] and row["downloads"]["default"]["bytes_equal"]
                if fixture == "UI":
                    assert row["pdfa_service_log"] and row["indexed_text"]
            else:
                assert row["stored_archive"] and not row["downloads"]["default"]["bytes_equal"]
        w, r, duplicate = [index[f"R{n}-A-{stage}"] for stage in ("W", "R", "DUP")]
        assert w["preflight"]["writable_test_exit"] == 1 and "Permission denied" in str(w["celery_result"])
        assert r["preflight"]["writable_test_exit"] == 0 and r["status"] == "success"
        assert duplicate["status"] == "failure" and "It is a duplicate" in str(duplicate["celery_result"])
        assert w["input"] == r["input"] == duplicate["input"]
    opt_in = index["S1-X-SI"]
    assert opt_in["status"] == "success" and opt_in["tesseract_starts"]["recognition"] == 1
    assert not opt_in["downloads"]["default"]["signatures"]["fixture_ca"]
    assert not opt_in["downloads"]["default"]["bytes_equal"]
    for group in {entry[1] for entry in MATRIX + CONTROLS}:
        path = task / "evidence/runtime" / group
        assert json.loads((path / "startup.json").read_text())["initial_db"] == {"docs": [], "tasks": []}
        assert all(row["exit_code"] == 0 for row in json.loads((path / "cleanup.json").read_text()))
    with (task / "decisions.csv").open(newline="") as f:
        decisions = list(csv.DictReader(f))
    assert {(d["run_id"], d["requirement"]) for d in decisions} == {
        (row["run_id"], req) for row in rows for req in REQS
    }
    assert len(decisions) == len(rows) * len(REQS)
    assert all(set(row["source_ids"].split()).issubset(source_ids) for row in decisions)
    bag = json.loads((task / "evidence/controls/bag-and-render.json").read_text())
    assert bag["render"]["reference"]["pixels"] == bag["render"]["altered"]["pixels"]
    assert bag["reference"]["sha256"] != bag["altered"]["sha256"]
    assert bag["bag"]["after_attributes_and_move"]["valid"]
    assert not bag["bag"]["after_companion_removed"]["valid"]
    assert bag["bag"]["smaller_bag_validation"]["valid"]
    return rows, sources


def behavior(row):
    stable_fields = (
        "status", "input", "queue_observed", "wrapper_count", "wrapper_early_return",
        "tesseract_starts", "tesseract_exit_zero", "db_counts", "consume_stays",
    )
    return {
        **{field: row[field] for field in stable_fields},
        "archive_stored": bool(row["stored_archive"]),
        "downloads": {
            key: {field: response[field] for field in ("status", "bytes_equal", "page_text", "signatures")}
            for key, response in row["downloads"].items()
        },
    }


def verify_replay(task, stored, replay_dir):
    import tempfile

    with tempfile.TemporaryDirectory(prefix="af154-compare-") as directory:
        observed = [as_row(entry, replay_dir, Path(directory)) for entry in MATRIX + CONTROLS]
    mismatches = [r1["run_id"] for r1, r2 in zip(stored, observed, strict=True)
                  if r2["status"] == "unobserved" or behavior(r1) != behavior(r2)]
    outputs = {
        "different_archive_sha256": [
            r1["run_id"] for r1, r2 in zip(stored, observed, strict=True)
            if r2["status"] != "unobserved" and r1["stored_archive"] and r2["stored_archive"]
            and r1["stored_archive"]["sha256"] != r2["stored_archive"]["sha256"]
        ],
        "behavior_mismatches": mismatches,
        "matched_ids": len(stored) - len(mismatches),
    }
    print(json.dumps(outputs, ensure_ascii=False))
    assert not mismatches


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--replay-dir", type=Path, default=None)
    args = parser.parse_args()
    rows, sources = verify_artifacts(args.task.resolve())
    print(json.dumps({
        "sources": sources,
        "matrix": describe([r for r in rows if r["planned"]]),
        "controls": describe([r for r in rows if not r["planned"]]),
    }, ensure_ascii=False))
    if args.replay_dir is not None:
        verify_replay(args.task, rows, args.replay_dir.resolve())


if __name__ == "__main__":
    main()
