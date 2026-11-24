"""Validate report structure and independently re-read the selected raw PET keys."""

import argparse
import ast
import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from pathlib import Path


def read(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_xml(work, upstream):
    assignments = read(work / "assignments.csv")
    segments = read(work / "segments.csv")
    by_id = {r["unit_id"]: r for r in segments}
    assert len(by_id) == 96
    for language in ("ita", "tur"):
        with zipfile.ZipFile(upstream / f"data/raw/{language}.zip") as archive:
            for a in [r for r in assignments if r["language"] == language]:
                _, per = a["raw_entries"].split(":", 1)
                _, pej = a["planned_entries"].split(":", 1)
                raw = archive.read(per)
                plan = archive.read(pej)
                assert hashlib.sha256(raw).hexdigest() == a["raw_file_sha256"]
                assert hashlib.sha256(plan).hexdigest() == a["planned_file_sha256"]
                out, draft = ET.fromstring(raw), ET.fromstring(plan)
                ins = {x.get("id"): x for x in draft.findall("task")}
                assert out.get("status") == "FINISHED" and out.get("id") == draft.get("id")
                assert len(ins) == int(a["completed_units"])
                for u in out.findall("unit"):
                    r = by_id[f"{out.get('id')}-{u.get('id')}"]
                    src = u.findtext("S")
                    assert src == ins[u.get("id")].findtext("S")
                    assert u.findtext("MT") == ins[u.get("id")].findtext("MT")
                    assert u.get("orig_id") == ins[u.get("id")].get("orig_id") == r["flores_id"]
                    visits = u.findall("annotations/annotation")
                    target = visits[-1].find("HT" if a["condition"] == "ht" else "PE")
                    assert hashlib.sha256(target.text.encode()).hexdigest() == r["target_sha256"]
                    assert r["subject_id"] == f"{language}_{target.get('producer').split('.')[0]}"
                    event_times = [list(v.find("events")) for v in visits]
                    last_t = [int(row[-1].get("t")) if row else 0 for row in event_times]
                    assert sum(last_t) == int(r["event_time_ms"]) == int(r["author_event_ms"])
                    assert len(src.split()) == int(r["src_words"]) == int(r["author_src_words"])
    return assignments, segments


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--upstream", type=Path, required=True)
    a = parser.parse_args()
    p = a.work
    assignments, segments = test_xml(p, a.upstream)
    frame = read(p / "frame.csv")
    assert len([r for r in frame if r["row_kind"] == "planned_slot"]) == 24
    assert {r["slot_id"] for r in frame if r["row_kind"] == "planned_slot"} == {r["slot_id"] for r in assignments}
    assert len({(r["language"], r["doc_id"]) for r in assignments}) == 8
    assert all(r["raw_comparison_eligible"] == "True" for r in segments)
    assert all(r["author_all_metrics_match"] == "True" and r["author_fingerprint_match"] == "True" for r in segments)
    assert all(r["hf_state"] == "pinned_tsv_unavailable" and not r["hf_event_ms"] for r in segments)
    assert len({r["source_sha256"] for r in segments}) == 16
    assert sum(int(r["events"]) for r in segments) == 39194
    assert sum(int(r["visits"]) for r in segments) == 140
    e = [r for r in segments if r["prior_row_id"]]
    assert len(e) == 5 and all(r["prior_values_match"] == "True" for r in e)
    assert sum(int(r["event_time_ms"]) for r in e) == 2061853
    assert sum(int(r["src_words"]) for r in e) == 111
    viewer = read(p / "receipts/03-viewer-five.csv")
    assert {(r["unit_id"], r["event_ms"], r["src_words"]) for r in viewer} == {
        (r["unit_id"], r["event_time_ms"], r["src_words"]) for r in e
    }

    source_rows = [json.loads(line) for line in (p / "sources.jsonl").read_text().splitlines()]
    ids = {s["source_id"] for s in source_rows}
    assert len(source_rows) == len(ids) == 70
    expected = {
        "source_id", "work_id", "lineage_id", "question_id", "case_id", "url", "publisher",
        "version", "checked_utc", "read_location", "observation", "original_value_units",
        "evidence_type", "limits", "access_status", "inclusion_reason",
    }
    assert all(expected <= set(s) and s["url"].startswith("https://") for s in source_rows)
    counted = Counter(s["category"] for s in source_rows if s["count_toward_minimum"])
    assert counted == {"raw_per": 24, "code": 5, "design_schema_processed": 4, "prior_contrast": 7}
    assert all(s["access_status"] == "direct" for s in source_rows if s["count_toward_minimum"])
    assert len({s["sha256"] for s in source_rows if s["category"] == "raw_per"}) == 24
    assert all(set(r["evidence_ids"].split(";")) <= ids for r in assignments)
    assert {q for s in source_rows for q in s["question_id"]} == {f"Q{i}" for i in range(1, 8)}

    result = (p / "RESULT.md").read_text()
    first = result.split("\n\n")[:3]
    assert [chunk.splitlines()[0] for chunk in first] == [
        "| 언어·문서·배정키 | HT/PE 조건·상태 | 원파일 해시·URL/entry | 출력 식별자 | 결측 사유 |",
        "| 분절·비교 단위 | 원 이벤트 ms | 처리판 ms·단어 | 차이·조사 원인 | 증거 파일/행 | 미확인 |",
        "| 같은 원문 대조 | 비교 가능한 번역 노동창 | 품질·검수 연결 여부 | 허용할 수치·단위 | 비교 불가 조건 |",
    ]
    assert [len(block.splitlines()) - 2 for block in first] == [24, 13, 8]
    last = result.rstrip().split("\n\n")[-1].splitlines()
    assert last[0] == "| 불일치·약점 | 영향을 받는 주장 | 다음 조사와 원자료 | 판단을 뒤집을 관측 |"
    assert len(last) == 5
    assert re.findall(r"^## (Q\d)", result, re.MULTILINE) == [f"Q{i}" for i in range(1, 8)]
    for filename in ("RESULT.md", "SELF_CHECK.md", "SCOPE.md"):
        for target in re.findall(r"\]\(([^):]+)\)", (p / filename).read_text()):
            assert (p / target.split("#")[0]).is_file(), target
    for name in ("extract.py", "receipts/04-contrast.py", "receipts/05-verify.py"):
        ast.parse((p / name).read_text(), filename=name)
    print("verified 24 PEJ/PER keys, 96 segments plus 5 prior/viewer rows, 70 ledger records, 7 Q answers, 24/13/8 initial rows and exactly 3 final limitations")


if __name__ == "__main__":
    main()
