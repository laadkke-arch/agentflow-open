#!/usr/bin/env python3
"""Verify frozen inputs, evidence joins, arithmetic, report structure and scope.

Only the owned evidence/validation.json is written. This is a research-data
check, not a historical package build, CI rerun or external factual review.
"""
from collections import Counter
from datetime import datetime
from hashlib import sha256
from pathlib import Path
import csv
import io
import json
import math
import re
import subprocess

P = Path(__file__).resolve().parents[1]
REPO = P.parents[3]
PREFIX = str(P.relative_to(REPO)) + "/"
SEAL = "1714a55a529c7da42596ac0779d398f3aacf97c3"
checks = []

def check(name, ok, detail):
    checks.append({"condition": name, "met": bool(ok), "evidence": detail})

def readj(name):
    return json.loads((P / name).read_text())

def readc(name):
    with (P / name).open(newline="") as f:
        return list(csv.DictReader(f))

def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO)

def dt(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))

def truth(value):
    return value is True or value == "true"

refs = [json.loads(line) for line in (P / "references.jsonl").read_text().splitlines()]
frame = readc("frame.csv")
up, chains, verdicts, intervals = [readc(n) for n in ("upstream.csv", "chains.csv", "verdicts.csv", "intervals.csv")]
sources = readj("sources.json")
counts = readj("evidence/counts.json")
seal = readj("evidence/a-seal.json")
A = [r for r in refs if r["sample"] == "A"]
B = [r for r in refs if r["sample"] == "B"]
ids = {r["reference_id"] for r in refs}
sids = {s["source_id"] for s in sources}

frozen_refs_bytes = git("show", SEAL + ":" + PREFIX + "references.jsonl")
frozen_refs = [json.loads(x) for x in frozen_refs_bytes.decode().splitlines()]
check("A sealed rows unchanged", A == frozen_refs, {"seal_commit": SEAL, "rows": len(A)})
check("A frozen source file hash matches receipt", sha256(frozen_refs_bytes).hexdigest() == seal["fixed_files_sha256"]["references.jsonl"], SEAL)
frozen_frame_bytes = git("show", SEAL + ":" + PREFIX + "frame.csv")
frozen_frame = list(csv.DictReader(io.StringIO(frozen_frame_bytes.decode())))
check("A frame decisions unchanged", [r for r in frame if r["sample"] == "A"] == [r for r in frozen_frame if r["sample"] == "A"], "frame.csv A rows versus sealed commit")
for name, expected in seal["fixed_files_sha256"].items():
    if name in ("references.jsonl", "frame.csv"):
        continue
    actual = sha256((P / name).read_bytes()).hexdigest()
    check("sealed input unchanged: " + name, actual == expected, actual)

check("A sample minimums", len(A) >= 12 and all(v >= 6 for v in Counter(r["ecosystem"] for r in A).values()) and len({r["consumer_project"] for r in A}) >= 8, {"references": len(A), "ecosystems": dict(Counter(r["ecosystem"] for r in A)), "projects": len({r["consumer_project"] for r in A})})
check("2019–2023 A anchors and project cap", all(2019 <= dt(r["consumer_commit_date"]).year <= 2023 for r in A) and max(Counter(r["consumer_project"] for r in A).values()) <= 2, "references.jsonl")
check("B six attempts, three per ecosystem", len(B) == 6 and dict(Counter(r["ecosystem"] for r in B)) == {"Homebrew": 3, "conda-forge": 3}, "B candidates are not attempt rows")
check("Reference identifiers unique", len(ids) == len(refs) == 18, sorted(ids))
for name, rows in (("upstream", up), ("chains", chains), ("verdicts", verdicts)):
    check(name + " exact reference join", len(rows) == len(ids) and {r["reference_id"] for r in rows} == ids, len(rows))
check("interval reference joins", all(r["reference_id"] in ids for r in intervals), len(intervals))
check("source IDs unique", len(sids) == len(sources), len(sources))
for name, rows, key in (("upstream", up, "source_ids"), ("verdicts", verdicts, "minimal_evidence_ids"), ("intervals", intervals, "source_ids")):
    used = set()
    for r in rows:
        if r.get(key):
            used.update(json.loads(r[key]))
    check(name + " source joins", not (used - sids), sorted(used - sids))

required_source_fields = ["source_id", "related_questions", "case_ids", "original_url", "publication_or_revision_date", "fixed_version", "checked_utc", "directly_read_location", "verified_content", "limitations", "producer", "source_lineage", "count_toward_minimum", "count_reason"]
check("all source rows carry required fields", all(all(k in s for k in required_source_fields) for s in sources), required_source_fields)
credited = [s for s in sources if s["count_toward_minimum"]]
check("credited originals directly read and described", all(s["direct_read"] and s["original_url"].startswith("https://") and all(s[k] for k in ["directly_read_location", "verified_content", "limitations", "producer", "source_lineage"]) for s in credited), len(credited))
check("credited canonical works unique", len({s["canonical_work_key"] for s in credited}) == len(credited), len(credited))
cat = Counter(s["minimum_category"] for s in credited)
cats = {"A_historical": cat["historical"], "upstream": cat["upstream"], "consumer_followup": cat["followup"] + cat["consumer_followup"], "B_additional_historical": cat["b_consumer_original"] + cat["consumer_historical"], "cross_domain": cat["cross_domain_upstream"] + cat["cross_domain_consumer"]}
check("source category counts reconcile", cats == counts["source_minimum_categories"] and sum(cats.values()) == len(credited), cats)
check("original minima 32/12/8/8/4", len(credited) >= 32 and cats["A_historical"] >= 12 and cats["upstream"] >= 8 and cats["consumer_followup"] >= 8 and cats["cross_domain"] >= 4, cats)
check("source totals reconcile", len(sources) == counts["source_ledger_rows"] and len(credited) == counts["conservative_unique_originals"], {"rows": len(sources), "credited": len(credited)})
av = Counter(r["verdict"] for r in verdicts if r["sample"] == "A")
check("A verdict denominators reconcile", dict(av) == counts["A_verdicts"] and sum(av.values()) == len(A), dict(av))
au = {r["event_id"] for r in up if r["sample"] == "A" and r["event_id"]}
bu = {r["event_id"] for r in up if r["sample"] == "B" and r["event_id"]}
check("deduplicated selected event counts reconcile", len(au) == counts["A_selected_upstream_event_keys"] and len(bu) == counts["B_selected_upstream_event_keys"] and len(au | bu) == counts["A_B_deduplicated_selected_upstream_event_keys"], {"A": len(au), "B": len(bu), "union": len(au | bu)})
check("strict exposure/deployment not inferred", all(not truth(r["upstream_to_consumer_latency_eligible"]) and not truth(r["strict_five_point_complete"]) and not truth(r["Tr_exact_first_runtime_deployment"]) for r in chains), "all18 primary rows false; metadata/source intervals remain separate")
for r in intervals:
    if not r["lower_seconds"]:
        continue
    lower = (dt(r["end"]) - dt(r["start_upper"] or r["start"])).total_seconds()
    upper = (dt(r["end_upper"] or r["end"]) - dt(r["start"])).total_seconds()
    ok = all(math.isclose(a, b, abs_tol=1e-6) for a, b in [(lower, float(r["lower_seconds"])), (upper, float(r["upper_seconds"])), (lower / 86400, float(r["lower_days"])), (upper / 86400, float(r["upper_days"]))])
    check("interval arithmetic " + r["interval_id"], ok and lower <= upper, {"lower_seconds": lower, "upper_seconds": upper, "eligible": r["eligible"], "numeric_role": r["numeric_role"]})
    check("numeric interval has sources " + r["interval_id"], bool(json.loads(r["source_ids"])), r["source_ids"])
for r in chains:
    if r["window_start"] and r["window_end"]:
        gap = (dt(r["window_end"]) - dt(r["window_start"])).total_seconds()
        check("365-day artifact window " + r["reference_id"], gap == 365 * 86400, {"seconds": gap, "limit": r["window_anchor_limit"]})
for iid in ("A-H02-AssetMetadata", "A-C04-ConditionalMetadata"):
    x = next(r for r in intervals if r["interval_id"] == iid)
    check("noneligible metadata interval " + iid, x["eligible"] == "false", x["numeric_role"])
pub = [r for r in intervals if r["sample"] == "A" and r["eligible"] == "true" and r["numeric_role"] == "SOURCE_PUBLICATION"]
check("A source publication pairs versus references", len(pub) == 3 and len({r["reference_id"] for r in pub}) == 2, [r["interval_id"] for r in pub])

report = (P / "RESULT.md").read_text()
blocks = []
block = []
for line in report.splitlines() + [""]:
    if line.startswith("|"):
        block.append(line)
    elif block:
        blocks.append(block)
        block = []
headers = ["| 참조 ID·A/B | 소비자 옛 판·목적·인용 URL | 상류 전후 판·시행 근거 | 소비자 확인·수정·배포 URL | 용도 충족·의도적 고정·미확인 |", "| 생태계·모집 방식 | 소비자·참조·독립 사건 수 | 전후 사슬 완성·부분·무사건 | 유지·오류·보류 | 날짜 쌍·검열 수 | 관측 지연 범위 |", "| 참조와 기대 기능 | 주소만으로 확인 | 판·용도로 추가 확인 | 이력·시점으로 추가 확인 | 최소 근거 URL | 대가·반례·남은 질문 |", "| Q 번호·주장·적용 범위 | 근거 원문 URL·정확한 절 또는 실행 영수증 | 확인한 내용·분자·분모 | 반례를 찾은 곳과 결과 | 미확인·판단을 바꿀 최소 자료 |"]
check("four required tables immediately below title", [b[0] for b in blocks[:4]] == headers and report.splitlines()[2] == headers[0] and all(line.startswith("|") or not line for line in report.splitlines()[2:report.splitlines().index(blocks[3][-1]) + 1]), "first four table headers and uninterrupted table region")
check("table1 includes all18 references", len(blocks[0]) == 20 and {line.split("|")[1].strip().split()[0] for line in blocks[0][2:]} == ids, len(blocks[0]) - 2)
check("last table exactly3 data rows and last content", len(blocks[-1]) == 5 and report.rstrip().endswith(blocks[-1][-1]) and blocks[-1][0].startswith("| 중요한 불일치·약점 |"), len(blocks[-1]) - 2)
for name in ("RESULT.md", "SELF_CHECK.md", "examples.md"):
    text = (P / name).read_text()
    mentioned = set(re.findall(r"\b(?:BH|BC|X|R|H|C)-(?:S|U|F|C|R)\d{2}\b", text))
    check(name + " source IDs resolve", mentioned <= sids, sorted(mentioned - sids))
    targets = re.findall(r"\]\(([^)]+)\)", text)
    relative = [t.split("#")[0] for t in targets if not re.match(r"[a-z]+:|#", t)]
    missing = sorted({t for t in relative if not (P / t).exists()})
    check(name + " relative links exist", not missing, missing)
check("Q1–Q8 self-check sections", all("## Q" + str(i) + "." in (P / "SELF_CHECK.md").read_text() for i in range(1, 9)), "SELF_CHECK.md")
acceptance = readj("evidence/acceptance-evidence.json")
check("acceptance required typed schema", isinstance(acceptance, list) and all(all(k in a for k in ("condition", "met", "evidence", "note")) and isinstance(a["met"], bool) for a in acceptance), len(acceptance))
check("unmet conditions include resumption input", all(a["note"] and a["evidence"] for a in acceptance if not a["met"]), [a["condition"] for a in acceptance if not a["met"]])
marc = P / "collectors/cross/harvard-2022-record.mrc"
check("fixed holdings record byte integrity", marc.stat().st_size == 2338 and sha256(marc.read_bytes()).hexdigest() == "6ce2142a32f7fe98f815cc62de767efdf6312571da20814c65a1fb6170d5e4e6", "2338 bytes; known independently checked SHA256")
manifest = readj("manifest.json")
paths = set(git("diff", "--name-only", manifest["base_commit"]).decode().splitlines()) | set(git("ls-files", "--others", "--exclude-standard").decode().splitlines())
check("only owned paths changed", all(p.startswith(PREFIX) for p in paths), sorted(p for p in paths if not p.startswith(PREFIX)))
white = subprocess.run(["git", "diff", "--check"], cwd=REPO, text=True, capture_output=True)
check("git diff whitespace", white.returncode == 0, white.stdout + white.stderr)
receipt = {"checked_utc": datetime.now().astimezone().isoformat(), "scope": "Research ledger, sealed-input, arithmetic, file-structure and ownership validation; not historical runtime verification", "head": git("rev-parse", "HEAD").decode().strip(), "checks": checks, "passed": sum(c["met"] for c in checks), "failed": sum(not c["met"] for c in checks)}
(P / "evidence/validation.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"passed": receipt["passed"], "failed": receipt["failed"], "failures": [c for c in checks if not c["met"]]}, ensure_ascii=False))
raise SystemExit(1 if receipt["failed"] else 0)
