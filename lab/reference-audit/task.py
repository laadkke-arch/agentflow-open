"""Audit explicit [source:id] markers and root-repository identity references.

This checks evidence linkage, not the truth of a claim or availability of URLs.
"""
import json
from pathlib import Path
import re
import sys
from workbench.urls import RepositoryURL, repository_key


def audit(document, sources):
    if not isinstance(document, str) or not isinstance(sources, list):
        raise ValueError("expected document text and a source list")
    known = {}
    errors = []
    for source in sources:
        sid = source.get("id")
        if not isinstance(sid, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", sid):
            errors.append("invalid-source-id")
            continue
        if sid in known:
            errors.append("duplicate-source:" + sid)
            continue
        known[sid] = source
    used = set(re.findall(r"\[source:([a-z][a-z0-9-]*)\]", document))
    errors.extend("missing-source:" + sid for sid in sorted(used - known.keys()))
    roots = {}
    for sid, source in known.items():
        try:
            key = repository_key(source.get("url"))
            roots.setdefault(key, []).append(sid)
        except RepositoryURL:
            # A documentation subpage is not the same resource as its repo root.
            pass
    return {"ok": not errors, "errors": errors, "used": sorted(used),
            "unused": sorted(known.keys() - used),
            "duplicate_repository_sources": {k: v for k, v in roots.items() if len(v) > 1},
            "claim_truth_checked": False, "network_accessed": False}


if __name__ == "__main__":
    case = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = audit(case["document"], case["sources"])
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["ok"] else 1)
