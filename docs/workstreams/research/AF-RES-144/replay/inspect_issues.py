"""Project only the public issue and comment date fields and byte fingerprints."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess

from fixtures import ISSUES, blob


def issue_payload(contents):
    for match in re.finditer(rb'<script[^>]*application/json[^>]*>(.*?)</script>', contents, re.S):
        payload = json.loads(match[1])
        route = payload.get("payload", {}).get("issueViewerRoute")
        if route:
            return route["data"]["repository"]["issue"]
    raise ValueError("GitHub issue payload unavailable")


def timestamp():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def curl(url):
    started = timestamp()
    job = subprocess.run(["curl", "-sSL", "-m", "25", "-w", "\n%{http_code}", url], capture_output=True)
    data, _, status = job.stdout.rpartition(b"\n")
    return data, {"url": url, "observed_utc": started, "http": status.decode(), "exit": job.returncode, "stderr": job.stderr.decode()}


def comment_snapshot(repo, item):
    comment_id = item["databaseId"]
    url = f"https://api.github.com/repos/{repo}/issues/comments/{comment_id}"
    data, receipt = curl(url)
    fields = {}
    if receipt["http"] == "200":
        raw = json.loads(data)
        fields = {name: raw.get(name) for name in ("created_at", "updated_at", "html_url", "author_association")}
        fields["body_sha256"] = blob(raw["body"].encode())["sha256"]
        assert fields["html_url"] == item["url"]
    return receipt, fields


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("timeline", type=Path)
    parser.add_argument("evidence", type=Path)
    opts = parser.parse_args()
    rows = []
    evidence = []
    with ThreadPoolExecutor(max_workers=6) as workers:
        pages = workers.map(curl, ISSUES.values())
        for (case, url), (raw, html_receipt) in zip(ISSUES.items(), pages):
            issue = issue_payload(raw)
            repo = "/".join(url.split("/")[3:5])
            author = issue["author"]["login"]
            nodes = issue["timelineItems"]["edges"] + issue["backTimelineItems"]["edges"]
            comments = {edge["node"]["databaseId"]: edge["node"] for edge in nodes
                        if edge.get("node", {}).get("__typename") == "IssueComment"}
            assert len(comments) == issue["totalCommentsCount"]
            by_date = sorted(comments.values(), key=lambda comment: comment["createdAt"])
            rest = list(workers.map(lambda item: comment_snapshot(repo, item), by_date))
            initial_hour = f'{issue["createdAt"][:10]}-{int(issue["createdAt"][11:13])}'
            # Hold the archive separate from the current HTML and its timestamps.
            archive_url = f"https://data.gharchive.org/{initial_hour}.json.gz"
            archive_job = subprocess.run(
                ["curl", "-sSLI", "-m", "15", "-o", "/dev/null", "-w", "%{http_code}", archive_url], capture_output=True
            )
            history_access = {
                "archive_head": {"url": archive_url, "observed_utc": timestamp(), "exit": archive_job.returncode,
                                 "http": archive_job.stdout.decode(), "stderr": archive_job.stderr.decode()},
                "html_sha256": blob(raw)["sha256"],
            }
            issue_row = dict(case=case, layer="current-issue", id=issue["databaseId"], author=author, role="original author",
                             url=url, created_html=issue["createdAt"], issue_updated_at=issue["updatedAt"],
                             rest_created_at=None, rest_updated_at=None, last_edited_html=None,
                             body_sha256=blob(issue["body"].encode())["sha256"], body_version=issue["bodyVersion"],
                             first_edition="unproven", observed_utc=html_receipt["observed_utc"],
                             note="Issue HTML metadata; current body. No opening event or first revision read.")
            rows.append(issue_row)
            evidence.append(dict(case=case, source_id=f"I-{case}", html=html_receipt, issue_node=issue["id"],
                                 timeline_event_types=list(dict.fromkeys(edge["node"]["__typename"] for edge in nodes)),
                                 **history_access))
            owner = issue["repository"]["owner"]["login"]
            for item, (receipt, fields) in zip(by_date, rest):
                speaker = item["author"]["login"]
                association = item["authorAssociation"]
                role = "original author" if speaker == author else (
                    "project owner/member" if speaker == owner or association in {"OWNER", "MEMBER"} else "third party")
                suff = "-min" if item["databaseId"] == 1372294143 else f'-{item["databaseId"]}'
                rows.append(dict(case=case, layer="followup-comment", id=item["databaseId"], author=speaker, role=role, url=item["url"],
                                 created_html=item["createdAt"], issue_updated_at=None, rest_created_at=fields.get("created_at"),
                                 rest_updated_at=fields.get("updated_at"), last_edited_html=item["lastEditedAt"],
                                 body_sha256=blob(item["body"].encode())["sha256"], body_version=item["bodyVersion"],
                                 first_edition=None, observed_utc=html_receipt["observed_utc"],
                                 note=f'Anchor in public HTML. REST HTTP={receipt["http"]}; public edit diff unavailable.'))
                evidence.append(dict(case=case, source_id=f"I-{case}{suff}", comment_node=item["id"], url=item["url"],
                                     association=association, last_edit=item["lastUserContentEdit"], rest=receipt, rest_fields=fields))
    with opts.timeline.open("w", newline="", encoding="utf8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    opts.evidence.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf8")


if __name__ == "__main__":
    main()
