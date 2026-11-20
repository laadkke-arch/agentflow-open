"""Look at additional known files at the selected pre-answer commits."""

import json
import re
from datetime import datetime
from urllib.parse import quote

from collect import ROOT, Reader, rows, verified_answer_dates


def main():
    dates = verified_answer_dates()
    reasons = {rec["reason_id"]: rec for rec in rows(ROOT / "REASONS.jsonl")}
    aliases = {r["repo"]: r["canonical_repo"] for r in rows(ROOT / "results/repo-now.jsonl")}
    history = {}
    for observed in rows(ROOT / "results/repo-then.jsonl"):
        anchor = observed.get("commit")
        if anchor:
            history[(aliases.get(observed["repo"]) or observed["repo"],
                     observed["answer_date"])] = observed
    reader = Reader(1.06)
    cache = {}
    path = ROOT / "results" / "pinned-files.jsonl"
    with path.open("w", encoding="utf-8", buffering=1) as stream:
        for line in (ROOT / "data/pinned-files.txt").read_text().splitlines():
            if not line or line.startswith("#"):
                continue
            ref, key, repo, explicit, filename, pattern, note = line.split("|", 6)
            reason = reasons[f"{ref}/{key}"]
            day = reason["answer_date"] or dates.get(ref, (None, None))[0]
            canonical = aliases.get(repo) or repo
            historic = history.get((canonical, day), {})
            commit = explicit or historic.get("commit")
            provenance = {"reason_id": reason["reason_id"], "at_answer": day,
                          "repo": canonical, "file": filename, "commit": commit}
            if commit:
                url = f"https://raw.githubusercontent.com/{canonical}/{commit}/{quote(filename, safe='/')}"
                if url not in cache:
                    cache[url] = reader.get(url)
                info, body = cache[url]
                match = re.search(pattern, body, re.IGNORECASE)
                provenance.update(checked_at=info["checked_at"], url=url,
                                  http=info["http"], committed_at=historic.get("committed_at"),
                                  request=info, line=1 + body.count("\n", 0, match.start())
                                  if match else None, confirmed=note if match else None)
                if explicit and not historic.get("committed_at"):
                    provenance["fixed_version"] = explicit
            stream.write(json.dumps(provenance, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
