"""Acquire the declared public windows and isolate each GitHub opening body."""

import argparse
import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


FORUM = "https://discuss.pytorch.kr"
FORUM_SEARCH = ("가중치", "복사본", "전치", "데이터로더")
REPO = "https://github.com/deeplearningzerotoall/PyTorch"
QUERIES = {
    "G1": "is:issue created:<=2024-12-31 sort:created-asc",
    "G2-how": 'is:issue is:public in:title,body created:2019-01-01..2024-12-31 "pytorch" "어떻게" sort:created-asc',
    "G2-want": 'is:issue is:public in:title,body created:2019-01-01..2024-12-31 "pytorch" "싶습니다" sort:created-asc',
}
CAPS = {"G1": 40, "G2-how": 24, "G2-want": 24}
EMBEDDED = re.compile(
    r'<script type="application/json" data-target="react-app.embeddedData">(.*?)</script>', re.S
)


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def save(path, rows):
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def read(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def get(url, accept):
    receipt = {"url": url, "observed_at_utc": utc(), "origin_http": None, "content_type": None}
    try:
        with urlopen(Request(url, headers={"Accept": accept, "User-Agent": "AF-RES-134 public research"}), timeout=20) as r:
            body = r.read()
            receipt.update(
                origin_http=r.status, content_type=r.headers.get("Content-Type"),
                response_date=r.headers.get("Date"), final_url=r.url, bytes=len(body),
                response_sha256=sha256(body), access="response"
            )
            return receipt, body
    except HTTPError as exc:
        state = "service_limit" if exc.code == 429 else "http_error"
        receipt.update(origin_http=exc.code, content_type=exc.headers.get("Content-Type"), access=state)
    except (TimeoutError, URLError) as exc:
        reason = str(exc)
        proxy = re.search(r"Tunnel connection failed: (\d+)", reason)
        if proxy:
            receipt.update(access="proxy_connect_error", proxy_http=int(proxy.group(1)), detail=reason)
        else:
            dns = any(marker in reason for marker in ("Name or service not known", "Temporary failure in name resolution", "nodename"))
            receipt.update(access="dns_error" if dns else "network_error", detail=reason)
    return receipt, None


def page_route(body, name):
    for script in EMBEDDED.findall(body.decode("utf-8")):
        payload = json.loads(script).get("payload", {})
        if name in payload:
            return payload[name]
    raise ValueError(f"no official payload route {name}")


def forum_snapshot(destination, bodies):
    jobs = [("A", str(number), f"{FORUM}/t/{number}.json") for number in range(6001, 6065)]
    jobs.extend(("B", q, f"{FORUM}/search.json?" + urlencode({"q": q})) for q in FORUM_SEARCH)
    with ThreadPoolExecutor(max_workers=3) as pool:
        responses = list(pool.map(lambda job: get(job[2], "application/json"), jobs))

    receipts, openings = [], []
    for (layer, selector, _), (receipt, body) in zip(jobs, responses, strict=True):
        receipt.update(layer=layer, selector=selector)
        if body is not None:
            try:
                data = json.loads(body)
            except (ValueError, UnicodeError):
                receipt.update(access="html_or_nonjson_error")
            else:
                if layer == "A":
                    first = next((p for p in data.get("post_stream", {}).get("posts", [])
                                  if p.get("post_number") == 1), None)
                    receipt.update(topic_id=data.get("id"), post_number=first and first.get("post_number"),
                                   post_id=first and first.get("id"))
                    if first and str(data.get("id")) == selector:
                        # Discourse JSON supplies cooked HTML. Preserve it transiently for
                        # the reviewer to choose and document a rendered or raw projection.
                        openings.append({"topic_id": data["id"], "first_post": first})
                else:
                    topics = data.get("topics")
                    posts = data.get("posts")
                    receipt.update(
                        arrays={name: len(values) if isinstance(values, list) else None
                                for name, values in data.items() if name in ("topics", "posts", "users", "categories", "tags")},
                        first_topic_ids=[row["id"] for row in topics[:8]] if isinstance(topics, list) else None,
                        first_post_topic_ids=[row.get("topic_id") for row in posts[:8]] if isinstance(posts, list) else None,
                        search_term=data.get("grouped_search_result", {}).get("term"),
                    )
        receipts.append(receipt)
    save(destination, receipts)
    save(bodies, openings)


def issue_window(layer, destination, receipt_path):
    rows, pages = [], []
    number = 1
    while len(rows) < CAPS[layer]:
        params = {"q": QUERIES[layer]}
        if layer != "G1":
            params["type"] = "issues"
        if number > 1:
            params["p" if layer != "G1" else "page"] = number
        base = REPO + "/issues" if layer == "G1" else "https://github.com/search"
        receipt, body = get(base + "?" + urlencode(params), "text/html")
        receipt.update(query=QUERIES[layer], page=number, filter="all issue states")
        pages.append(receipt)
        if body is None:
            break
        if layer == "G1":
            page = page_route(body, "issuesIndexContentRoute")
            results = page["results"]
            available = page["pageInfo"]
            receipt.update(result_count=available["totalCount"], page_count=available["totalPages"],
                           result_type=page["issueSearchType"], returned=len(results))
            for row in results:
                issue = row.get("issue", {})
                rows.append({"issue_number": issue["number"], "created_at": issue["createdAt"],
                             "repository": "deeplearningzerotoall/PyTorch", "kind": row["itemType"]})
        else:
            page = page_route(body, "blackbirdSearchRoute")
            results = page["results"]
            receipt.update(result_count=page["result_count"], page_count=page["page_count"],
                           result_type=page["type"], returned=len(results), logged_in=page["logged_in"],
                           returned_page=page["page"], errors=page["errors"],
                           warn_limited_results=page["warn_limited_results"])
            if receipt["returned_page"] != number:
                raise ValueError("returned page disagrees with requested page")
            for row in results:
                repo = row["repo"]["repository"]
                rows.append({"issue_number": row["number"], "created_at": row["created"],
                             "repository": repo["owner_login"] + "/" + repo["name"], "kind": "issue_search_hit"})
        if number >= receipt["page_count"] or not results:
            break
        number += 1
    if layer == "G1":
        rows.sort(key=lambda row: (row["created_at"], row["issue_number"]))
    else:
        dates = [datetime.fromisoformat(r["created_at"]) for r in rows]
        if dates != sorted(dates):
            raise ValueError("global search does not match declared creation order")
    chosen = [{"position": i, **row} for i, row in enumerate(rows[:CAPS[layer]], 1)]
    save(destination, chosen)
    pages.append({"layer": layer, "cap": CAPS[layer], "frozen_rows": len(chosen),
                  "window_sha256": sha256(destination.read_bytes()), "frozen_at_utc": utc(),
                  "last": chosen[-1] if chosen else None})
    save(receipt_path, pages)


def issue_opening(row):
    locator = f'https://github.com/{row["repository"]}/issues/{row["issue_number"]}'
    receipt, body = get(locator, "text/html")
    out = {**row, **receipt}
    if body is None:
        return out
    if "/pull/" in receipt["final_url"]:
        return {**out, "access": "pull_request_redirect"}
    try:
        route = page_route(body, "issueViewerRoute")
        node = route["data"]["repository"]["issue"]
    except (ValueError, KeyError):
        return {**out, "access": "wrong_html_payload"}
    if node["number"] != row["issue_number"] or datetime.fromisoformat(node["createdAt"]) != datetime.fromisoformat(row["created_at"]):
        return {**out, "access": "identity_mismatch"}
    author = node.get("author") or {}
    # No title, comment, timeline, scores or replies are returned to the reader.
    return {
        **out, "access": "opening", "canonical_url": node["url"], "node_id": node["id"],
        "database_id": node["databaseId"], "updated_at": node["updatedAt"],
        "body_version": node.get("bodyVersion"), "last_edited_at": node.get("lastEditedAt"),
        "first_body_edit_field_present": "lastEditedAt" in node,
        "author_id": author.get("id"), "author": author.get("login"), "author_type": author.get("__typename"),
        "body": node.get("body"),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("forum", "window", "openings"))
    parser.add_argument("--layer", choices=tuple(QUERIES))
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--window", type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    if args.mode == "forum" and args.receipt:
        forum_snapshot(args.receipt, args.out)
    elif args.mode == "window" and args.layer and args.receipt:
        issue_window(args.layer, args.out, args.receipt)
    elif args.mode == "openings" and args.window:
        with ThreadPoolExecutor(max_workers=3) as pool:
            save(args.out, pool.map(issue_opening, read(args.window)))
    else:
        parser.error("forum requires --receipt, window requires --layer and --receipt, openings requires --window")


if __name__ == "__main__":
    main()
