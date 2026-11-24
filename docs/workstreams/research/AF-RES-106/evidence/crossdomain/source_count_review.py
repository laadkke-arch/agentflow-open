"""Canonical source allowlist: count a logical work/event once across representations."""
from pathlib import Path
import collections
import datetime
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
TASK = HERE.parent.parent
REPO = TASK.parents[3]
SEAL = "8054c2221d4023ba03c904d96f13928219d36c3d"
INPUT = "092f4c5c56451bceb53e632f4bddf33db6cda168"


def parse(data):
    return [json.loads(line) for line in data.splitlines() if line]


def sid(row):
    return row.get("source_id") or row.get("id")


def canonical(row):
    lineage = row.get("work_lineage") or row.get("lineage") or ""
    if "reference/" in lineage:
        return "ggplot2:" + re.search(r"reference/[^\s]+\.html", lineage).group(0)
    if "gallery/" in lineage:
        return "matplotlib:" + re.search(r"gallery/[^\s]+\.html", lineage).group(0)
    url = row.get("original_url", "")
    match = re.search(r"github.com/([^/]+/[^/]+)/commit/([a-f0-9]{40})", url)
    if match:
        return "event:" + match.group(1) + ":" + match.group(2)
    return lineage


def main():
    sealed = parse(subprocess.check_output(["git", "show", SEAL + ":docs/workstreams/research/AF-RES-106/sources.jsonl"], cwd=REPO, text=True))
    inherited_text = subprocess.check_output(["git", "show", INPUT + ":docs/workstreams/research/AF-RES-102/sources.jsonl"], cwd=REPO, text=True)
    inherited = parse(inherited_text)
    files = {"gg": TASK/"evidence/ggplot2/sources-stage3.jsonl", "mp": TASK/"evidence/matplotlib/sources-stage3.jsonl", "cd": HERE/"sources-crossdomain.jsonl"}
    rows = {key: parse(path.read_text()) for key, path in files.items()}
    proof = []

    def include(row, category, source_ledger):
        proof.append({"source_id": sid(row), "canonical_work": canonical(row), "category": category,
                      "source_ledger": source_ledger, "original_url": row["original_url"],
                      "preserved_path": row.get("preserved_location") or row.get("preserved_path") or row.get("preservation"),
                      "source_digest": row.get("sha256") or row.get("fingerprint") or row.get("fingerprints"),
                      "reason": "One logical work/event; editions, payloads, section aliases and merge duplicates add zero."})

    for row in rows["gg"]:
        if row.get("countable"):
            include(row, {"body": "body", "figure_or_source": "figure_or_source", "publication_record": "official_record"}[row["category"]], "evidence/ggplot2/sources-stage3.jsonl")
    sealed_counted = {canonical(row): row for row in sealed if row.get("countable")}
    retained_sealed_ids = []
    for row in rows["mp"]:
        if row.get("category") == "example_body":
            key = canonical(row)
            if key in sealed_counted:
                include(sealed_counted[key], "body", "sealed " + SEAL + ":sources.jsonl")
                retained_sealed_ids.append(sid(sealed_counted[key]))
            else:
                include(row, "body", "evidence/matplotlib/sources-stage3.jsonl")
        elif row.get("countable"):
            include(row, {"independent_source_or_payload": "figure_or_source", "official_change_record": "official_record"}[row["category"]], "evidence/matplotlib/sources-stage3.jsonl")
    for row in rows["cd"]:
        if row.get("countable"):
            include(row, "crossdomain", "evidence/crossdomain/sources-crossdomain.jsonl")
    duplicate_work_keys = [key for key, count in collections.Counter(r["canonical_work"] for r in proof).items() if count > 1]
    duplicate_ids = [key for key, count in collections.Counter(r["source_id"] for r in proof).items() if count > 1]
    inherited_exact_hits = []
    for row in proof:
        key = row["canonical_work"]
        if key.startswith(("ggplot2:", "matplotlib:")):
            path = key.split(":", 1)[1]
            hits = [sid(old) for old in inherited if path in old.get("original_url", "")]
        elif key.startswith("event:"):
            commit = key.rsplit(":", 1)[1]
            hits = [sid(old) for old in inherited if commit in json.dumps(old)]
        else:
            hits = [sid(old) for old in inherited if row["original_url"] == old.get("original_url")]
        if hits:
            inherited_exact_hits.append({"source_id": row["source_id"], "inherited_ids": hits})
    mpdir = TASK/"evidence/matplotlib/diffs"
    merges = []
    for primary, merge in [
        ("f21219be5f7411a38b1598382f16dd7b099ffa9e", "dbe0ee669262350aaae877bf7c83c9e9909cd8c4"),
        ("0d39834ce0c1d579703672e3890b42806eda2121", "7ffc3e4a6a057d6117529163187592816830e9cf"),
        ("fca4a5f6f8df0f620f77536f5a8d747da414001f", "ebba21ad5e0403e3c4df15ca5e7f631428fd5e4d")]:
        a = (mpdir/(primary+".patch")).read_text()
        b = (mpdir/(merge+".first-parent.patch")).read_text()
        a = a[a.index("diff --git "):]
        b = b[b.index("diff --git "):]
        merges.append({"counted_primary_commit": primary, "excluded_merge_commit": merge,
                       "example_diff_bytes_equal": a == b, "diff_sha256": hashlib.sha256(a.encode()).hexdigest()})
    source_proof = [r for r in proof if r["category"] == "figure_or_source"]
    for row in source_proof:
        file = TASK / row["preserved_path"]
        row["reviewed_preserved_bytes_sha256"] = hashlib.sha256(file.read_bytes()).hexdigest()
        row["review_mode"] = "GG PNG decoded and viewed; MP Python source read in full; no source execution."
    result = {"reviewed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "reviewer": "/root/crossdomain_review",
              "seal": SEAL, "inherited_input": INPUT,
              "ledger_sha256": {str(path.relative_to(TASK)): hashlib.sha256(path.read_bytes()).hexdigest() for path in files.values()},
              "counted_ids": [r["source_id"] for r in proof], "canonical_works": proof,
              "counts": dict(collections.Counter(r["category"] for r in proof)), "total": len(proof),
              "retained_sealed_mp_body_ids": retained_sealed_ids,
              "duplicate_work_keys": duplicate_work_keys, "duplicate_ids": duplicate_ids, "inherited_exact_hits": inherited_exact_hits,
              "matplotlib_same_event_merge_exclusions": merges,
              "matplotlib_bar_event_distinction": [
                  {"commit": "895626981706e301923cc23aa079b5c0a8774bf7", "pr": 23590, "utc": "2022-08-27T07:10:29Z", "change": "Men/Women to Tea/Coffee"},
                  {"commit": "e71012316e7271799a064ce09ea9285f3edb47a7", "pr": 24498, "utc": "2022-12-11T21:11:31Z", "change": "Tea/Coffee paired bars to penguin categories and loop"}],
              "count_reallocations": [
                  {"sealed_id": "GG106-OLD-BODY-stat_unique", "final_counted_id": "GG106-S3-GG-X1-new-payload", "action": "same work counted once in figure_or_source; old body explicitly count0 in final global ledger"},
                  {"ids": ["MP106-old-gallery_misc_hyperlinks_sgskip", "MP106-old-gallery_shapes_and_collections_ellipse_demo"], "action": "old-only direct readings outside this conservative 38-work proof set; may remain logged but count0 here"},
                  {"action": "GG old/new bodies and MP stage3 reread bodies matching retained sealed IDs must be duplicates, not additional counts"}],
              "scope_limits": ["Canonical count and evidence trace review, not independent reclassification of all old eligible pages or all main U outcomes.",
                               "IIIF/JATS7 works are cross-domain evidence, not primary error-rate cases.",
                               "Six figure/source works have distinct purposes and canonical examples from the selected15 body works; same logical body/source versions are not doubled.",
                               "Published Git source branch and merge for the same event count1; historical build G remains 미확인."]}
    assert len(proof) == 38 and not duplicate_work_keys and not duplicate_ids and not inherited_exact_hits
    assert result["counts"] == {"body": 15, "figure_or_source": 6, "official_record": 10, "crossdomain": 7}
    assert all(x["example_diff_bytes_equal"] for x in merges)
    (HERE/"source-count-review.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({key: result[key] for key in ["counts", "total", "retained_sealed_mp_body_ids", "duplicate_work_keys", "inherited_exact_hits"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
