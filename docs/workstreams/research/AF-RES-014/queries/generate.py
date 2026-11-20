"""Regenerate the in-memory query texts and reproducibility metadata."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import Request, urlopen

PRIOR = "478c301b693896e2c6d777f46ac441f071bfdfe8"
FIXED = "docs/workstreams/research/AF-RES-011/"
HERE = Path(__file__).resolve().parent
USER_AGENT = "AF-RES-014 public-question-research/1.0"
TOKEN = re.compile(r"[^\W_]+")
OMIT_TAGS = {"pre", "code", "script", "style", "blockquote", "svg", "samp"}


def stamp():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def prior(filename):
    return json.loads(subprocess.check_output(
        ["git", "show", f"{PRIOR}:{FIXED}{filename}"], cwd=HERE,
    ))


class Prose(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in OMIT_TAGS or (tag == "a" and (
            attrs.get("href", "").startswith("/users/") or "user-mention" in attrs.get("class", "")
        )):
            self.skip.append(tag)
        elif not self.skip and tag in {"br", "p", "li", "div", "hr", "tr", "h2", "h3"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if self.skip and tag == self.skip[-1]:
            self.skip.pop()
        elif not self.skip and tag in {"p", "li", "div", "tr"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def sanitize(body, *, html=False):
    if html:
        parser = Prose()
        parser.feed(body)
        body = "".join(parser.parts)
    else:
        body = re.sub(r"(?ms)^ *(```+|~~~+).*?^ *\1[^\n]*", "\n", body)
        body = re.sub(r"(?m)^(?: {4}|\t|>).*$", "", body)
        body = re.sub(r"`+[^`\n]+`+", " ", body)
        body = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", body)
        body = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", body)
        body = unescape(body)
    body = re.sub(r"(?im)^\s*(?:--+\s*$|best(?: regards)?[,!]?\s*$|cheers[,!]?\s*$|thanks(?: in advance)?[,.!]?\s*$)[\s\S]*\Z", "", body)
    body = re.sub(r"https?://[^\s>\])]+", " ", body)
    body = re.sub(r"(?<!\w)@[-\w]+|(?<!\w)[^\s@]+@[^\s@]+\.[^\s@]+", " ", body)
    return " ".join(unicodedata.normalize("NFKC", body).split())


class PublicAPI:
    def __init__(self):
        self.attempts = []
        self.policy_block = {}

    def read(self, url, query_id, *, want_html=False):
        host = urlsplit(url).hostname
        if host in self.policy_block:
            return None, f"host_policy:{self.policy_block[host]}"
        row = {"id": f"QAPI-{len(self.attempts) + 1:03}", "query_id": query_id, "url": url,
               "accessed_at_utc": stamp(), "method": "GET", "http_status": None, "connect_status": None}
        self.attempts.append(row)
        try:
            request = Request(url, headers={"User-Agent": USER_AGENT,
                                           "Accept": "text/html" if want_html else "application/json"})
            with urlopen(request, timeout=10) as response:
                row.update(final_url=response.url, http_status=response.status)
                data = response.read(2_000_000)
            row["outcome"] = "response"
            return (data.decode("utf-8") if want_html else json.loads(data)), row["id"]
        except HTTPError as exc:
            row.update(http_status=exc.code, outcome="http_error")
        except (URLError, TimeoutError, OSError, ValueError) as exc:
            reason = str(getattr(exc, "reason", exc))
            connect = re.search(r"Tunnel connection failed:\s*(\d{3})", reason)
            row["outcome"] = "proxy_connect_error" if connect else type(exc).__name__
            if connect:
                row["connect_status"] = int(connect.group(1))
                if row["connect_status"] == 403:
                    self.policy_block[host] = row["id"]
        return None, row["id"]


def stack_exchange(case, api):
    question = re.search(r"/questions/(\d+)", case["url"]).group(1)
    base = "https://api.stackexchange.com/2.3"
    query = urlencode({"site": "softwarerecs", "filter": "withbody", "pagesize": 100})
    current, body_ref = api.read(f"{base}/questions/{question}?{query}", case["id"])
    revisions, rev_ref = api.read(f"{base}/posts/{question}/revisions?{query}", case["id"])
    refs = [body_ref, rev_ref]
    if current and revisions:
        for revision in revisions.get("items", []):
            if revision.get("revision_number") == 1 and revision.get("body"):
                return sanitize(revision["body"], html=True), "se_revisions_v1", revision.get("revision_guid"), refs
    if current and current.get("items"):
        item = current["items"][0]
        if item.get("body") and item.get("last_activity_date") == item.get("creation_date"):
            return sanitize(item["body"], html=True), "se_body_unchanged", item["creation_date"], refs
    return "", "summary", None, refs


def hacker_news(case, api):
    item_id = parse_qs(urlsplit(case["url"]).query)["id"][0]
    firebase, first = api.read(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json", case["id"])
    algolia, second = api.read(f"https://hn.algolia.com/api/v1/items/{item_id}", case["id"])
    # The public item snapshots expose no recoverable body revision identifier.
    refs = [first, second]
    if firebase or algolia:
        refs.append("initial_revision_not_exposed")
    return "", "summary", None, refs


def reddit(case, api):
    path = urlsplit(case["url"]).path.rstrip("/")
    payload, ref = api.read(f"https://www.reddit.com{path}.json?raw_json=1&limit=1", case["id"])
    if isinstance(payload, list) and payload:
        children = payload[0].get("data", {}).get("children", [])
        if children:
            post = children[0]["data"]
            body = post.get("selftext", "")
            if body and body not in {"[deleted]", "[removed]"} and post.get("edited") is False:
                return sanitize(body), "reddit_unedited", str(post.get("created_utc")), [ref]
    return "", "summary", None, [ref]


def github_issue(case, api):
    if "/issues/" not in case["url"]:
        return "", "summary", None, ["discussion_has_no_issue_rest_endpoint"]
    endpoint = f"https://api.github.com/repos{urlsplit(case['url']).path}"
    issue, ref = api.read(endpoint, case["id"])
    if issue and issue.get("body") and issue.get("updated_at") == issue.get("created_at"):
        return sanitize(issue["body"]), "github_rest_unchanged", issue["created_at"], [ref]
    return "", "summary", None, [ref]


HANDLERS = {
    "softwarerecs": stack_exchange,
    "hackernews": hacker_news,
    "reddit": reddit,
    "github": github_issue,
}


def fingerprint(text):
    return {"sha256": sha256(text.encode("utf-8")).hexdigest(), "word_count": len(TOKEN.findall(text))}


def build():
    cases = prior("CASES.json")["cases"]
    api = PublicAPI()
    records = []
    for case in cases:
        handler = HANDLERS.get(case["platform"])
        if handler:
            body, mode, version, refs = handler(case, api)
        else:
            body, mode, version, refs = "", "summary", None, ["initial_revision_api_not_identified"]
        if not body:
            body, mode, version = sanitize(case["question_summary"]), "summary", PRIOR
        records.append({
            "id": case["id"], "url": case["url"], "date": case["date"], "platform": case["platform"],
            "source": "summary" if mode == "summary" else "original", "mode": mode,
            "version": version, "api_attempts": refs,
            "whole_or_part": case["whole_or_part"], "I5": case.get("info_codes", {}).get("I5"),
            "must": [{"target": row["target"], "polarity": row["polarity"]}
                     for row in case.get("constraints", []) if row.get("force") == "must"],
            **fingerprint(body),
        })
    return records, api.attempts


def load_inputs():
    """Read locked modes. A missing or changed original fails closed."""
    cases = {case["id"]: case for case in prior("CASES.json")["cases"]}
    api = PublicAPI()
    for row in json.loads((HERE / "metadata.json").read_text()):
        case = cases[row["id"]]
        if row["source"] == "summary":
            body = sanitize(case["question_summary"])
        else:
            body, mode, version, _ = HANDLERS[case["platform"]](case, api)
            if (mode, version) != (row["mode"], row["version"]):
                raise ValueError(f"Original revision unavailable or changed for {row['id']}")
        if any(row[field] != value for field, value in fingerprint(body).items()):
            raise ValueError(f"Query fingerprint mismatch for {row['id']}")
        yield row, body


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-metadata", action="store_true")
    args = parser.parse_args()
    if args.write_metadata:
        records, attempts = build()
        for filename, value in [("metadata.json", records), ("api-attempts.json", attempts)]:
            (HERE / filename).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
        print(f"questions={len(records)} original={sum(row['source'] == 'original' for row in records)}")
    else:
        print(f"verified={sum(1 for _ in load_inputs())}")


if __name__ == "__main__":
    main()
