"""Check the result tables, denominators, receipt links and recorded payloads."""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess

EXPECTED_GROUPS = {"asset": 7, "norm": 4, "implementation": 6, "consumer": 4}
EVIDENCE_COMMIT = "7c002297b6f2fa7ebeaf74b7e623be757463872c"


def get_json(path):
    return json.loads(path.read_text())


def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tables(markdown):
    matches = re.findall(r"(?m)^\|.*(?:\n\|.*)+", markdown)
    return [block.splitlines() for block in matches]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("owned", type=Path)
    root = parser.parse_args().owned
    receipt = root / "receipts"
    manifest = get_json(receipt / "input-manifest.json")
    assert len(manifest["files"]) == 60
    assert all(r["tree_blob"] == r["git_blob"] and r["http"] == 200 for r in manifest["files"])
    static = get_json(receipt / "python-static.json")["entries"]
    assert len(static) == 7
    for left, right in zip(static, get_json(receipt / "node-static.json")["entries"], strict=True):
        assert all(left[k] == right[k] for k in ("path", "bytes", "sha256", "glb", "geometry"))
    glbs = [entry for entry in static if entry["glb"]]
    assert len(glbs) == 3 and all(not entry["uris"] for entry in glbs)
    with (root / "chunks.csv").open(newline="") as f:
        chunks = list(csv.DictReader(f))
    assert len(chunks) == 13
    assert {row["sha256"] for row in chunks} == {entry["sha256"] for entry in static}
    assert sum(len(entry["geometry"]) for entry in static) == len(chunks)
    print("7 serializations, 13 primitive rows, 3 exact GLBs and 2 independent parsers")

    ledger = [json.loads(line) for line in (root / "sources.jsonl").read_text().splitlines()]
    assert len(ledger) == len({row["source_id"] for row in ledger})
    for row in ledger:
        for key in ("source_id", "work_id", "lineage_id", "q", "case", "url", "publisher", "edition",
                    "edition_date", "opened_utc", "location", "observed", "evidence_type",
                    "limitations", "access", "counted", "count_reason"):
            assert key in row, (row["source_id"], key)
    works = [row for row in ledger if row["counted"]]
    assert len({r["work_id"] for r in works}) == len(works) >= 21
    assert all(r["access"] == "success" for r in works)
    groups = Counter(row["category"] for row in works)
    assert all(groups[k] >= v for k, v in EXPECTED_GROUPS.items())
    print(f"{len(ledger)} source rows, {len(works)} counted originals, "
          f"{len({r['lineage_id'] for r in works})} lineages; {dict(groups)}")

    with (root / "runs.csv").open(newline="") as f:
        runs = list(csv.DictReader(f))
    cases = get_json(receipt / "cases.json")
    assert {(r["case"], int(r["round"])) for r in runs} == {
        (c["id"], round_id) for c in cases for round_id in (1, 2)
    }
    assert len(runs) == 2 * len(cases) == 48
    primary = [r for r in runs if r["purpose"] != "control"]
    assert Counter(r["purpose"] for r in primary) == {"geometry": 6, "material": 6, "offline": 6}
    case_pins = {c["id"]: c for c in cases}
    for row in runs:
        path = root / row["receipt"]
        outcome = get_json(path)
        entry = case_pins[row["case"]]
        assert row["entry_sha256"] == outcome["sha256"] == entry["sha256"]
        served = [e for e in outcome["serverHttp"] if e["category"] == "model"]
        assert json.loads(row["model_http"]) == [{"url": x["url"], "status": x["status"]} for x in served]
        assert not any(outcome.get(x) for x in ("outstandingRequests", "pageErrors", "executionError"))
        f = outcome["outcome"].get("frame")
        if f:
            assert fingerprint(path.parent / f["png"]["path"]) == f["png"]["sha256"] == row["frame_png_sha256"]
            assert f["pixelsSha256"] == row["rgba256"]
        if row["purpose"] != "control":
            assert outcome["outcome"]["load"] == "resolved" and row["geometry_match_glb"] == "True"
            assert all(e["status"] == 200 for e in served)
            if row["purpose"] == "offline":
                assert len(served) == 1 and len(entry["paths"]) == 1 and not outcome["blocked"]
            assert bool(f) == (row["purpose"] != "geometry")
            if f:
                assert f["foreground"] > 0 and outcome["outcome"]["draw"]["glError"] == 0
    control = Counter(r["observation"] for r in runs if r["purpose"]=="control")
    assert control == {"정상관측": 20, "저하관측": 6, "실패관측": 4}
    assert sum(len(json.loads(r["model_http"])) for r in primary) == 34
    assert sum(bool(r["rgba256"]) for r in primary) == 12
    assert get_json(receipt / "epub-read.json")["equal"]
    print("18 primary rows (34 model HTTP 200, 18 loads, 12 draws), 30 controlled observations, EPUB equality")

    prose = (root / "RESULT.md").read_text()
    groups = tables(prose)
    assert prose.startswith("| 모델·판·목적·회차 | 원파일 지문·요청 | 실제 기하·재질·픽셀 | 추가 자원·오류 | 원영수증 URL | 미확인 |")
    assert groups[1][0] == "| 단일 변경 | 기대한 접근 | 실제 요청·선택·표시 | 추천 조합 변화 | 재생 결과 |"
    assert groups[-1][0] == "| 가장 중요한 불일치·약점 | 영향받는 판단 | 다음 조사의 첫 원자료·행동 | 결론이 바뀌는 관측 |"
    for group, size, cols in ((groups[0], 18, 6), (groups[1], 13, 5), (groups[-1], 3, 4)):
        assert len(group)-2 == size and all(line.count("|")-1 == cols for line in group)
    assert prose.rstrip().endswith(groups[-1][-1])
    assert re.findall(r"(?m)^## (Q[1-7])\.", prose) == [f"Q{i}" for i in range(1,8)]
    linked = re.findall(r"https://github.com/laadkke-arch/agentflow-open/blob/" + EVIDENCE_COMMIT +
                        r"/docs/workstreams/research/AF-RES-265/(receipts/round-[12]/[^)]+)", "\n".join(groups[0]))
    assert sorted(linked) == sorted(row["receipt"] for row in primary)
    for path in linked:
        git_path = f"docs/workstreams/research/AF-RES-265/{path}"
        stored = subprocess.check_output(["git", "show", f"{EVIDENCE_COMMIT}:{git_path}"])
        assert stored == (root / path).read_bytes()
    for file in ("RESULT.md", "SELF_CHECK.md", "SCOPE.md", "replay.md", "COUNTEREXAMPLES.md"):
        text = (root / file).read_text()
        for link in re.findall(r"\]\(([^)]+)\)", text):
            if not link.startswith(("https://", "#")):
                assert (root / link.split("#")[0]).is_file(), (file, link)
    print("mandatory tables 18×6, 13×5, 3×4, Q1–Q7, 18 immutable receipt links and local file links verified")


if __name__ == "__main__":
    main()
