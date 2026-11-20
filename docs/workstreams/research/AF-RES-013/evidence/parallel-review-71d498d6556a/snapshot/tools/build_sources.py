#!/usr/bin/env python3
"""Join recorded evidence, preserving exclusions and explicit minimum-count caps."""
import collections
import hashlib
import json
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["id", "url", "accessed_at_utc", "source_type", "title", "version_or_date", "sections_read", "confirmed", "limits", "level", "used_in"]
INPUTS = ["evidence/cases-kep/sources.json", "evidence/cases-rust/sources.json", "evidence/cases-ps/sources.json", "evidence/methods/sources.json", "evidence/methods/supplementary-sources.json"]
COUNTED = {f"M{i:02d}" for i in range(1, 17)} | {"M22", "M23", "M24", "M25", "M27", "PS-R-S25-DECISION", "R-TEMPLATE-PRIOR-MERGE", "PS-T-PEP12", "PS-T-SWIFT-INITIAL", "K-TEMPLATE-NOW"}


def site(url):
    host = (urlsplit(url).hostname or "unknown").lower()
    for domain in ["github.com", "githubusercontent.com", "python.org", "swift.org", "nist.gov", "nii.ac.jp", "uva.nl"]:
        if host == domain or host.endswith("." + domain):
            return "github.com" if domain in ("github.com", "githubusercontent.com") else domain
    return ".".join(host.split(".")[-2:])


def dump(path, value):
    (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    sources, excluded, ids = [], [], set()
    source_shards, shard_source_ids, shard_excluded_count = [], set(), 0
    optional = ["evidence/counterexamples/sources.json", "evidence/judgments/VERIFICATION.json", "evidence/baseline/sources.json", "evidence/reviewer-source-audit-sources.json"]
    optional += [str(p.relative_to(ROOT)) for p in sorted((ROOT/"evidence/judgments").glob("reviewer-*-sources.json"))]
    filenames = INPUTS + [x for x in optional if (ROOT/x).exists()]
    for filename in filenames:
        data = json.loads((ROOT / filename).read_text())
        for shard in data.get('source_shards',[]) if isinstance(data,dict) else []:
            assert hashlib.sha256((ROOT/shard['path']).read_bytes()).hexdigest()==shard['sha256']
            source_shards.append(shard)
            filenames.append(shard['path'])
        rows = data if isinstance(data, list) else data["sources"]
        excluded.extend([dict(x, recorded_in=filename) for x in (data.get("excluded", []) if isinstance(data, dict) else [])])
        for original in rows:
            row = dict(original)
            if row.get("status") in {"inaccessible_unknown", "blocked", "error", "failed", "not_opened", "snippet_only"}:
                excluded.append(dict(row, recorded_in=filename,
                    reason=row.get("limits",row.get("confirmed",row["status"])),
                    minimum_counted_noncase=False))
                continue
            assert not (set(REQUIRED) - set(row)), (filename, row.get("id"), set(REQUIRED) - set(row))
            assert row["id"] not in ids, row["id"]
            ids.add(row["id"])
            row["recorded_in"] = filename
            row["site_group"] = site(row["url"])
            row["minimum_counted_noncase"] = row["id"] in COUNTED
            row["counting_note"] = f"직접 본문을 읽은 비사례{len(COUNTED)}개 중 하나; 사이트당3개 상한" if row["id"] in COUNTED else "보조 원장; 비사례 최소수에 중복·추가 산입하지 않음"
            if filename.startswith("evidence/cases-ps/"):
                row["time_precision"] = "원문 열람 묶음의 기록 완료 시각 또는 별도 open-revalidation의 실제 요청 시각; 초단위 실행시간 비교에 쓰지 않음"
            sources.append(row)
            if filename.startswith('evidence/baseline/') and filename.endswith('.sources.json'):
                shard_source_ids.add(row['id'])
        if filename.startswith('evidence/baseline/') and filename.endswith('.sources.json'):
            shard_excluded_count += len(data.get('excluded',[]))
    ps_excluded = json.loads((ROOT / "evidence/cases-ps/excluded-source-readings.json").read_text())
    if isinstance(ps_excluded, dict):
        ps_excluded = ps_excluded.get("excluded", ps_excluded.get("records", []))
    excluded.extend(dict(x, recorded_in="evidence/cases-ps/excluded-source-readings.json") for x in ps_excluded)
    assert COUNTED <= ids, sorted(COUNTED - ids)
    counted = [s for s in sources if s["minimum_counted_noncase"]]
    assert all(s["level"] in ("D1", "D2") for s in counted)
    sites = collections.Counter(s["site_group"] for s in counted)
    assert max(sites.values()) <= 3
    old = subprocess.check_output(["git", "show", "7f627a81199f06da7f7b15f979e7fef25dd17602:docs/workstreams/research/AF-RES-009/sources.json"], text=True)
    novelty = {k: next(s["url"] for s in sources if s["id"] == k) not in old for k in ("M13", "M14")}
    assert all(novelty.values())
    cases = json.loads((ROOT / "cases/CASES.json").read_text())["cases"]
    audit = {"noncase_counted": len(counted), "counted_ids": sorted(COUNTED), "sites": dict(sorted(sites.items())), "single_site_max": max(sites.values()), "templates_or_procedures": ["R-TEMPLATE-PRIOR-MERGE", "PS-T-PEP12", "PS-T-SWIFT-INITIAL", "K-TEMPLATE-NOW"], "methodology_papers": ["M01", "M02", "M03", "M04", "M15", "M16"], "crossfield_overviews": {"patent": ["M05", "M07"], "law": ["M09"], "academic": ["M12"]}, "new_generative_citation_papers": novelty, "review_originals": ["M22", "M23", "M24", "M27", "PS-R-S25-DECISION"], "review_decision_announcements": ["M25"], "review_note": "토론·메일 원문5개와 별도 수락 공고M25를 구분한다. M27은 reviewer가 Pod 선례를 제시하고 제안자가 설계 차이를 비교한 원문이다. 추가 GitHub 리뷰는 읽었지만 사이트 상한 때문에 최소수에는 미산입.", "case_documents_counted_separately": len(cases), "case_families": dict(collections.Counter(c["family"] for c in cases)), "all_source_records_including_support": len(sources), "excluded_attempts": len(excluded), "limits": "사이트 상한은 비사례 최소수에 적용. GitHub에 호스팅된 사례는 독립 제안31개로 별도 보고하며 사이트 다양성으로 주장하지 않음."}
    core_sources = [s for s in sources if s['id'] not in shard_source_ids]
    core_excluded = [s for s in excluded if not (s.get('recorded_in','').startswith('evidence/baseline/') and s.get('recorded_in','').endswith('.sources.json'))]
    assert len(sources)==len(core_sources)+sum(x['source_count'] for x in source_shards)
    assert len(excluded)==len(core_excluded)+sum(x['excluded_count'] for x in source_shards)==len(core_excluded)+shard_excluded_count
    # Preserve all full records without sending one multi-megabyte JSON payload.
    # Every shard row has the same eleven required source fields; no evidence is
    # replaced with a URL-only entry, and all minima reside in the core ledger.
    ledger = {"schema_version":2,"counting":audit,"sources":core_sources,"excluded":core_excluded,
      "source_shards":source_shards,
      "format_note":"Complete ledger = sources + every source_shards file's sources; excluded is combined in the same way. All per-run rows retain all eleven required fields. Counts and SHA-256 are checked by validate_deliverables.py. Sharding changes serialization only, not readings, evidence levels, minimum counts or original run responses."}
    (ROOT/'sources.json').write_text(json.dumps(ledger,ensure_ascii=False,separators=(',',':'))+'\n')
    dump("evidence/SOURCE_COUNT.json", audit)
    print(json.dumps(audit, ensure_ascii=False))


if __name__ == "__main__":
    main()
