"""Read the first 30 public issue bodies per repository from GitHub, without comments."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import unicodedata
from urllib.parse import urlencode
from urllib.request import Request, urlopen

REPOS = ("ocrmypdf/OCRmyPDF", "paperless-ngx/paperless-ngx")
QUERY = "is:issue is:public created:2024-01-01..2025-12-31 sort:created-asc"


class EmbeddedData(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.active = False
        self.data = []

    def handle_starttag(self, tag, attrs):
        if tag == "script" and dict(attrs).get("data-target") == "react-app.embeddedData":
            self.active = True

    def handle_endtag(self, tag):
        if tag == "script" and self.active:
            self.active = False

    def handle_data(self, data):
        if self.active:
            self.data.append(data)


def get_payload(url):
    request = Request(url, headers={"User-Agent": "AF-RES-146 research replay"})
    with urlopen(request, timeout=25) as response:
        raw = response.read()
        metadata = {
            "status": response.status, "final_url": response.url, "sha256": sha256(raw).hexdigest(),
            "checked_utc": datetime.now(UTC).isoformat(timespec="milliseconds"),
        }
    parser = EmbeddedData()
    parser.feed(raw.decode("utf-8"))
    return metadata, json.loads("".join(parser.data))["payload"]


def capture_issue(row):
    try:
        metadata, payload = get_payload(row["url"])
        issue = payload["issueViewerRoute"]["data"]["repository"]["issue"]
        if issue["number"] != row["number"] or issue["createdAt"] != row["created_utc"]:
            raise ValueError("issue identity or creation time changed")
        body = unicodedata.normalize("NFC", issue["body"].replace("\r\n", "\n").replace("\r", "\n"))
        actor = issue.get("author") or {}
    except Exception as err:
        return {**row, "access": "failed", "error": str(err), "checked_utc": datetime.now(UTC).isoformat()}
    return {**row, **metadata, "access": "opened", "title": issue["title"], "author": actor.get("login"),
            "author_type": actor.get("__typename"), "updated_utc": issue["updatedAt"],
            "body_version": issue.get("bodyVersion"), "body_sha256": sha256(body.encode()).hexdigest(),
            "body": body, "duplicate": bool(issue.get("duplicateOf"))}


def capture_repo(repo):
    metadata = []
    listing = []
    for page in (1, 2):
        url = f"https://github.com/{repo}/issues?{urlencode({'q': QUERY, 'page': page})}"
        receipt, payload = get_payload(url)
        route = payload["issuesIndexContentRoute"]
        metadata.append({**receipt, "query_url": url, "page_info": route["pageInfo"]})
        listing.extend(item["issue"] for item in route["results"])
    assert metadata[0]["page_info"]["totalCount"] == metadata[1]["page_info"]["totalCount"]
    assert len({row["number"] for row in listing}) == len(listing)
    order = sorted(listing, key=lambda item: (item["createdAt"], item["number"]))
    assert [item["createdAt"] for item in order] == [item["createdAt"] for item in listing]
    rows = [
        {"repo": repo, "slot": slot, "number": row["number"], "created_utc": row["createdAt"],
         "url": row["permalink"]}
        for slot, row in enumerate(order[:30], 1)
    ]
    with ThreadPoolExecutor(max_workers=6) as executor:
        issues = list(executor.map(capture_issue, rows))
    return {"repo": repo, "pages": metadata, "issues": issues}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Local scratch JSON, which contains public issue bodies")
    args = parser.parse_args()
    with ThreadPoolExecutor(max_workers=2) as executor:
        result = list(executor.map(capture_repo, REPOS))
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    for frame in result:
        print(frame["repo"], frame["pages"][0]["page_info"]["totalCount"], len(frame["issues"]),
              sum(issue["access"] == "opened" for issue in frame["issues"]))


if __name__ == "__main__":
    main()
