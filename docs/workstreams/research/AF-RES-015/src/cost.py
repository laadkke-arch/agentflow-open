"""Measure the network portion of the fixed triage and hybrid cost benchmark."""

import json
import time
from datetime import date
from urllib.parse import quote

from collect import ROOT, Reader, commit_list, payload, rows, utc_now
from extract import jsonl
from signals import link_observations, evaluate_link, site_key


def benchmark_inputs():
    for line in (ROOT / "data" / "cost-bench.txt").read_text().splitlines():
        if line and not line.startswith("#"):
            reason_id, repo, url, locator = line.split("|")
            yield reason_id, repo, url, locator


def scan(mode, reader, inputs, data, inherited):
    for reason_id, repo, manual_url, locator in inputs:
        reason = data[reason_id]
        begin, started = time.monotonic(), utc_now()
        old_link = inherited.get((reason["answer_ref"][:4], site_key(reason["url"])))
        prior_dead = evaluate_link(old_link)["http_dead"]["positive"]
        scoped = []
        intended_age, archived = None, None

        if repo:
            info, page = reader.get(f"https://github.com/{repo}")
            scoped.append(info)
            content = payload(page)
            about = content.get("codeViewLayoutRoute", {}).get("repo", {})
            archived = about.get("isArchived")
            ref = content.get("codeViewRepoRoute", {}).get("refInfo", {}).get("name")
            if ref:
                head_url = (info["final_url"] or "").rstrip("/") + "/commits/" + quote(ref, safe="/") + "/"
                info, page = reader.get(head_url)
                scoped.append(info)
                commit = next(iter(commit_list(payload(page))), {})
                when = commit.get("committedDate")
                if when:
                    intended_age = (date(2026, 11, 20) - date.fromisoformat(when[:10])).days

        age_flag = intended_age > 365 if intended_age is not None else None
        options = [archived, age_flag, prior_dead]
        alert = True if True in options else False if False in options else None
        yield {
            "reason_id": reason_id, "mode": mode, "input_url": reason["evidence_locator"]["source_url"],
            "official_url": manual_url, "official_locator": locator, "repo": repo or None,
            "started_at_utc": started, "finished_at_utc": utc_now(),
            "seconds": round(time.monotonic() - begin, 4),
            "requests": sum(x["requests"] for x in scoped),
            "metadata_pages": sum(x["http"] == 200 for x in scoped), "body_pages": 0,
            "input_011_404": prior_dead, "archived": archived,
            "last_commit_age_days": intended_age, "alert": alert, "calls": scoped,
        }


def main():
    inputs = list(benchmark_inputs())
    data = {r["reason_id"]: r for r in rows(ROOT / "REASONS.jsonl")}
    inherited = link_observations()
    reader = Reader(1.06)
    observations = []
    for mode in ("b", "c"):
        observations.extend(scan(mode, reader, inputs, data, inherited))
    jsonl(ROOT / "results" / "cost-network.jsonl", observations)


if __name__ == "__main__":
    main()
