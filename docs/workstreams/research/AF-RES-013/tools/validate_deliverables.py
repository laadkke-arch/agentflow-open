"""Validate research artifacts and expose, rather than waive, acceptance limits."""
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit
import argparse
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
OWNED = "docs/workstreams/research/AF-RES-013/"
RUN_COMMIT = "caa2a814727dd485ed0eb9bb8530d6b16fab9584"
GOLD_COMMIT = "f6f59a85949a001792b80260dd454c3fcc714a70"
HEADERS = [
    ["사례 ID", "계열", "원문 주소(고정 판)", "결정일", "정답 항목 수(완성품·부품·같은 분야 설계·다른 생태계·다른 분야·표준논문)", "기준선 A 적중", "기준선 B 적중", "놓친 정답 항목", "정답원 밖 유용 후보", "근접 오답", "깨진·가짜 링크", "누설·사후 자료", "미확인"],
    ["역할", "정답 항목 수(분모)", "기준선 A 적중(비율)", "기준선 B 적중(비율)", "대표 놓침 사례 ID", "미확인"],
    ["주장", "근거 자료 주소", "확인한 내용", "반증 시도", "미확인"],
]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO)


def read(path):
    return json.loads((ROOT / path).read_text())


def parse_table(block):
    lines = [x for x in block.splitlines() if x.startswith("|")]
    return [[x.strip() for x in re.split(r"(?<!\\)\|", line)[1:-1]] for line in lines]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["report", "self-check"], default="report")
    args = parser.parse_args()
    cases = read("cases/CASES.json")["cases"]
    prefixes = read("cases/PREFIX_MANIFEST.json")["prefixes"]
    prefix_map = {p["id"]: p for p in prefixes}
    assert len(cases) == len(prefixes) == 31
    family = Counter(c["family"] for c in cases)
    assert len(family) >= 4 and max(family.values()) <= len(cases) / 2
    assert min(len(c["gold_items"]) for c in cases) >= 3
    assert sum(len(c["gold_items"]) for c in cases) == 176
    old_gold = json.loads(git("show", GOLD_COMMIT + ":" + OWNED + "cases/CASES.json"))["cases"]
    old_identity = {(c["id"], g["id"]): (g["name"], g["url"], g["stance"]) for c in old_gold for g in c["gold_items"]}
    assert old_identity == {(c["id"], g["id"]): (g["name"], g["url"], g["stance"]) for c in cases for g in c["gold_items"]}
    prefix_audit = []
    for c in cases:
        assert re.fullmatch(r"[0-9a-f]{40}", c["pinned_version"])
        assert c["pinned_version"] in c["url"]
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", c["decision_date"])
        path = c["prefix_file"]
        digest = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        assert digest == c["prefix_sha256"] == prefix_map[c["id"]]["sha256"]
        last = git("log", "-1", "--format=%H", "--", OWNED + path).decode().strip()
        subprocess.run(["git", "merge-base", "--is-ancestor", last, GOLD_COMMIT], cwd=REPO, check=True)
        assert last != GOLD_COMMIT
        prefix_audit.append({"id": c["id"], "sha256": digest, "last_prefix_commit": last, "precedes_gold": True})
    run_files = []
    for b in "AB":
        for c in cases:
            path = f"runs/{b}/{c['id']}.json"
            content = (ROOT / path).read_bytes()
            assert content == git("show", RUN_COMMIT + ":" + OWNED + path)
            run_files.append({"path": path, "sha256": hashlib.sha256(content).hexdigest(), "unchanged_from_preserved_run_commit": True})
    judgments = read("JUDGMENTS.json")["judgments"]
    assert len(judgments) == 342
    assert len({(j["case_id"], j["baseline"], j["rank"]) for j in judgments}) == 342
    aggregates = read("evidence/AGGREGATES.json")
    for name, digest in aggregates["input_hashes"].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest
    report = (ROOT / "RESULT.md").read_text()
    first_sections = re.findall(r"^## §(\d) ", report, re.M)
    assert first_sections == ["1", "2", "3", "4", "5"]
    tables = []
    for i, header in enumerate(HEADERS, 1):
        marker = f"### 표 {i} —"
        block = report.split(marker, 1)[1].split("\n### ", 1)[0]
        parsed = parse_table(block)
        assert parsed[0] == header, (i, parsed[0])
        rows = parsed[2:]
        assert all(len(row) == len(header) and all(cell for cell in row) for row in rows)
        assert all("미확인(" in row[-1] for row in rows)
        if i == 1:
            assert len(rows) == 31 and {r[0] for r in rows} == {c["id"] for c in cases}
            for row in rows:
                m = next(m for m in aggregates["cases"] if m["id"] == row[0])
                assert row[5].startswith(str(m["A"]["strict_historical_hits"]) + "/")
                assert row[6].startswith(str(m["B"]["strict_historical_hits"]) + "/")
        if i == 2:
            assert len(rows) == 6 and sum(int(r[1]) for r in rows) == 176
        tables.append({"number": i, "rows": len(rows), "columns": len(header), "headers_exact": True})
    assert re.findall(r"^### Q(\d)\.", report, re.M) == list("12345678")
    weaknesses = report.split("## §4", 1)[1].split("## §5", 1)[0]
    assert len(re.findall(r"^### [123]\. ", weaknesses, re.M)) == 3
    for phrase in ["무엇이 어긋나거나 약한가", "근거 위치", "이것이 틀리면 바뀌는 결론", "다음 조사 제안"]:
        assert weaknesses.count("**" + phrase + ":**") == 3
    local_links = []
    for target in re.findall(r"\]\(([^)]+)\)", report):
        if not target.startswith(("https://", "http://", "#")):
            path = target.split("#", 1)[0]
            assert (ROOT / path).is_file(), target
            local_links.append(path)
    sources = read("sources.json")
    required = {"id", "url", "accessed_at_utc", "source_type", "title", "version_or_date", "sections_read", "confirmed", "limits", "level", "used_in"}
    assert len({s["id"] for s in sources["sources"]}) == len(sources["sources"])
    assert all(required <= set(s) for s in sources["sources"])
    counted = [s for s in sources["sources"] if s.get("minimum_counted_noncase")]
    assert len(counted) == 25 and all(s["level"] in {"D1", "D2"} for s in counted)
    assert max(Counter(s["site_group"] for s in counted).values()) == 3
    assert set(s["id"] for s in counted) == set(sources["counting"]["counted_ids"])
    def site(url):
        host = urlsplit(url).hostname
        return "github.com" if host == "github.com" or host.endswith(".github.com") or host == "githubusercontent.com" or host.endswith(".githubusercontent.com") else host
    case_hosts = Counter(site(c["url"]) for c in cases)
    literal_case_count = sum(min(3, n) for n in case_hosts.values())
    assert literal_case_count == 3
    changed = git("diff", "--name-only", "a18d8d2e1575d9b679442134fd0f6f8e17423bfe", "HEAD").decode().splitlines()
    changed += git("diff", "--name-only", "HEAD").decode().splitlines()
    changed += git("ls-files", "--others", "--exclude-standard").decode().splitlines()
    outside = sorted({p for p in changed if not p.startswith(OWNED)})
    assert not outside, outside
    if args.phase == "self-check":
        self_check = (ROOT / "SELF_CHECK.md").read_text()
        assert "세부 질문 | 답 한 줄 | 붙은 출처 ID(종류 수) | 반증 시도(쓴 질의·자료와 결과) | 남은 불확실성" in self_check
        assert "차단" in self_check and "아니오" in self_check
        assert all(f"| Q{i} |" in self_check for i in range(1, 9))
    output = {
        "schema_version": 1,
        "phase": args.phase,
        "artifact_integrity": "passed",
        "strict_acceptance": "blocked",
        "blockers": [{"id": "SITE_CAP_CASES", "condition": "사이트당 최대3개를 사례 최소수에도 문자적으로 적용", "observed_case_host_counts": dict(case_hosts), "count_toward_literal_minimum": literal_case_count, "required_minimum": 30, "reason": "최초 SAMPLING의 비사례 한정 해석은 사용자 승인된 예외가 아님", "minimum_next_action": "진행 담당이 요청문과 최초 SAMPLING의 충돌을 인수 조건으로 해소하거나, 별도 사전 고정 절차로 최소10사이트의 적격 사례30개와 그 실행을 확보해야 함"}],
        "cases": len(cases), "families": dict(family), "gold": 176,
        "prefixes": prefix_audit, "original_gold_identity_unchanged": True,
        "run_files": run_files, "judgments": len(judgments), "tables": tables,
        "q_sections": 8, "section4_weaknesses": 3, "local_report_links_resolve": len(local_links),
        "minimum_noncase": 25, "noncase_sites": len(Counter(s["site_group"] for s in counted)), "noncase_site_max": 3,
        "outside_owned_path": outside,
        "file_hashes": {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ["RESULT.md", "JUDGMENTS.json", "cases/CASES.json", "sources.json", "SEARCH_LOG.json"]},
        "limits": "구조·원장·조상·불변성 검증이며 원문 전수 재열람, 실제 사용자 효용, 모든 링크의 미래 생존을 증명하지 않는다. 차단을 성공으로 바꾸지 않는다."
    }
    (ROOT / "evidence/FINAL_VALIDATION.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: output[k] for k in ["artifact_integrity", "strict_acceptance", "cases", "gold", "judgments", "tables", "minimum_noncase", "noncase_sites", "outside_owned_path"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
