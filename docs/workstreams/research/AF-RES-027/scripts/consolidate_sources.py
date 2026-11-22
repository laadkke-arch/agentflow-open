"""Normalize collector ledgers without changing the sealed historical inputs."""
import collections
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = [
    "collectors/homebrew/sources.json",
    "collectors/conda/sources.json",
    "collectors/homebrew/future-sources.json",
    "collectors/conda/future-sources.json",
    "collectors/homebrew-b/sources.json",
    "collectors/conda-b/sources.json",
    "collectors/cross/sources.json",
    "evidence/review-sources.json",
]
# One edit viewed as a diff, PR, alias file, or bottle commit gets one credit.
EVENT_ALIASES = {
    "48b5788c062ba492c34890e1b2a7cb26c8a1505f": "homebrew-core:PR194885",
    "2ddcf80b77a6db2485c4e9ecaa33c519b9e68164": "homebrew-core:PR194885",
    "2fb756508be49f99faeaa4af9915629fb2a90232": "homebrew-core:PR194885",
    "0c357945611d988fe65e46aeb092cbb6ca7492bd": "homebrew-core:PR194885",
    "562c37360f8133eda5870ab801d1a7710fe9abdc": "homebrew-core:PR68241",
    "ab9d906d072fb2c5ba6ca30b23cb3136e42de6c1": "homebrew-core:qt6-transition",
    "67e7aa02813056543f2d31dcd643e7418eb329cb": "homebrew-core:qt6-transition",
    "7ed0b0b9765d948cc6ebf62772c1073f1e17fe86": "homebrew-core:PR262253",
    "ad4806814e498656ca06816d4d65341a139169a9": "homebrew-core:PR285604",
}
PR_GROUPS = {"194885":"homebrew-core:PR194885","68241":"homebrew-core:PR68241",
             "262253":"homebrew-core:PR262253","285604":"homebrew-core:PR285604"}
FIXED_NON_GIT = {
    "X-S01":"PLOS ONE correction DOI10.1371/journal.pone.0165166, published2016-10-21",
    "X-S03":"PeerJ final article DOI10.7717/peerj.4375, published2018-02-13; author-hosted PDF copy",
    "X-S04":"Library of Congress Cataloging Service Bulletin60, Spring1993, pp2–4",
    "X-S05":"Harvard20220215_017.bib.mrc bytes295257330–295259667; recordSHA2566ce2142a32f7fe98f815cc62de767efdf6312571da20814c65a1fb6170d5e4e6",
}

def inferred_version(row, url):
    sid = row["source_id"]
    if sid in FIXED_NON_GIT: return FIXED_NON_GIT[sid]
    m = re.search(r"(?:blob|commit|commits)/([0-9a-f]{40})", url)
    if m: return m.group(1)
    if "api.anaconda.org/release/" in url:
        return url.split("/release/")[1] + "; mutable release metadata checked " + row.get("checked_utc", "미확인")
    if "/releases/tag/" in url:
        return url.split("/releases/tag/")[1] + "; release metadata as retrieved, see dated source observation"
    return "edition/date as stated: " + str(first(row, "publication_or_revision_date", "published_or_revised", "publication_date", default="미확인"))

def first(row, *names, default=None):
    for name in names:
        value = row.get(name)
        if value is not None and value != "":
            return value
    return default

def array(value):
    if value is None: return []
    return value if isinstance(value, list) else [value]

def git_revision(url):
    for pattern in [r"github.com/([^/]+/[^/]+)/(?:blob|commit)/([0-9a-f]{40})",
                    r"raw.githubusercontent.com/([^/]+/[^/]+)/([0-9a-f]{40})",
                    r"api.github.com/repos/([^/]+/[^/]+)/commits/([0-9a-f]{40})"]:
        match = re.search(pattern, url)
        if match: return match.groups()
    return None

def get_key(row, url, fixed):
    match = git_revision(url)
    if match:
        repo, sha = match
        return EVENT_ALIASES.get(sha, repo.lower() + "@" + sha)
    for sha, group in EVENT_ALIASES.items():
        if sha in str(fixed): return group
    pm = re.search(r"github.com/Homebrew/homebrew-core/pull/(\d+)", url)
    if pm and pm.group(1) in PR_GROUPS: return PR_GROUPS[pm.group(1)]
    return first(row, "canonical_work_key", "unique_original_group",
                 default=url.split("#")[0])

def main():
    out, seen_ids, credited, missing = [], set(), {}, []
    for relative in INPUTS:
        path = ROOT / relative
        if not path.exists():
            missing.append(relative); continue
        data = json.loads(path.read_text())
        if isinstance(data, dict):
            data = data.get("sources", data.get("records", []))
        for raw in data:
            sid = raw["source_id"]
            if sid in seen_ids: raise ValueError("duplicate source ID: " + sid)
            seen_ids.add(sid)
            url = first(raw, "original_url", "url", default="미확인")
            fixed = first(raw, "fixed_version", "fixed_revision", default=inferred_version(raw, url))
            cat = first(raw, "count_category", "category", default="supplement")
            wanted = bool(first(raw, "counted_original", "count_toward_minimum", default=False))
            read = first(raw, "direct_read", "directly_read", default=None)
            if read is None:
                # Historical Homebrew supplementary search/path logs are not inferred as original reads.
                read = wanted or cat in ("historical", "upstream", "consumer_followup", "followup")
            read = bool(read)
            group = get_key(raw, url, fixed)
            reason = first(raw, "count_reason", default=(
                "직접 읽은 원문; 중복 계보 검사 적용" if wanted else "보조/탐색 자료; 원문 최소수에서 제외"))
            count = wanted and read and url.startswith("https://")
            duplicate_of = None
            if count and group in credited:
                duplicate_of = credited[group]
                count = False
                reason = "동일 편집/판의 다른 렌더링·호출 파일/재열람: " + duplicate_of
            elif count:
                credited[group] = sid
            row = {
                "source_id": sid,
                "related_questions": array(first(raw, "related_questions", "related_q", "questions")),
                "case_ids": array(raw.get("case_ids")),
                "title": first(raw, "title", default=sid),
                "original_url": url,
                "read_url": first(raw, "read_url", "retrieved_url", default=url),
                "related_original_urls": raw.get("related_original_urls", []),
                "publication_or_revision_date": first(raw, "publication_or_revision_date",
                    "published_or_revised", "publication_date", default="미확인"),
                "fixed_version": fixed,
                "checked_utc": first(raw, "checked_utc", default="미확인"),
                "check_timestamp_semantics": first(raw, "check_timestamp_semantics", "checked_utc_note",
                    default="직접 판독 후 기록/재검토 시각; 원문 발행일과 구별"),
                "directly_read_location": first(raw, "directly_read_location", "read_location",
                    default="미확인; 원 수집 원장 참조"),
                "verified_content": first(raw, "verified_content", "confirmed_content", "observed",
                    default="미확인; 탐색/접근 기록"),
                "limitations": first(raw, "limitations", "limits", default="미확인; 추가 검토 필요"),
                "producer": first(raw, "producer", default="미확인"),
                "source_lineage": first(raw, "source_lineage", "lineage", default="미확인"),
                "claim_kind": first(raw, "claim_kind", "evidence_type", default="source_observation"),
                "direct_read": read,
                "count_toward_minimum": count,
                "minimum_category": cat,
                "count_reason": reason,
                "canonical_work_key": group,
                "duplicate_of": duplicate_of,
                "collector_file": relative,
            }
            out.append(row)
    (ROOT / "sources.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    counts = collections.Counter(r["minimum_category"] for r in out if r["count_toward_minimum"])
    urls = sorted({u.split("#")[0] for r in out if r["direct_read"]
                   for u in [r["original_url"]]+r["related_original_urls"]})
    revisions = set()
    for r in out:
        if not r["direct_read"]: continue
        for u in [r["original_url"]]+r["related_original_urls"]:
            m = git_revision(u)
            if m: revisions.add(m[0].lower()+"@"+m[1])
    rechecks = json.loads((ROOT/"evidence/root-rechecks.json").read_text())
    metrics = {
        "method":"원장에 남은 직접 판독 URL/고정 Git SHA의 고유값을 센 보수적 기록량. 요청횟수·사람해석시간·서로다른독립실험횟수가 아니다.",
        "source_rows":len(out), "minimum_credit_unique_originals":sum(counts.values()),
        "minimum_credit_by_raw_category":dict(counts),
        "documented_unique_direct_read_urls":len(urls),
        "documented_distinct_fixed_git_revisions":len(revisions),
        "root_reopen_receipts":len(rechecks),
        "human_reading_seconds":None, "operating_storage_cost":None,
        "missing_collector_inputs":missing,
        "direct_read_urls":urls, "fixed_git_revisions":sorted(revisions),
    }
    by_case = {}
    for case in sorted({c for r in out for c in r["case_ids"] if c.startswith("A-")}):
        case_urls = {u.split("#")[0] for r in out if r["direct_read"] and case in r["case_ids"]
                     for u in [r["original_url"]]+r["related_original_urls"]}
        editions = {p[0].lower()+"@"+p[1] for u in case_urls if (p := git_revision(u))}
        by_case[case] = {"documented_unique_direct_read_urls":len(case_urls),
                         "documented_distinct_fixed_git_revisions":len(editions)}
    metrics["by_A_reference"] = by_case
    (ROOT/"evidence/retrieval-metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({k:v for k,v in metrics.items() if k not in ("direct_read_urls","fixed_git_revisions")}, ensure_ascii=False))

if __name__ == "__main__": main()
