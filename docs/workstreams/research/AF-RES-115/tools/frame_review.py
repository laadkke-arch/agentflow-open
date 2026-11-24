"""Record the opening bodies in the frame and probe their public artifact URLs."""
import argparse
import concurrent.futures
import csv
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from frame import sha, utc

ORIGINAL_REQUESTS = {
    ("E", 4563), ("E", 4578), ("E", 4621),
    ("M", 10286), ("M", 10360), ("M", 10497),
}
PROBE_RE = re.compile(
    r"\.(?:excalidraw(?:lib)?|json|musicxml|mscx|mscz|mxl|zip|xml|gp)(?:\.txt)?(?:$|[?#])", re.I,
)
VISUAL_RE = re.compile(r"\.(?:png|jpe?g|gif|webp|svg|mp4|m4v|mov|webm)(?:$|[?#])", re.I)
XML_RE = re.compile(r"<(?:score-(?:partwise|timewise)|museScore)\b")


class Links(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.hrefs = []
        self.visual = False
        self.feed(markup)

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        url = attrs.get("href", "")
        if tag == "a" and url.startswith(("https://", "http://")):
            self.hrefs.append(url)
            self.visual |= bool(VISUAL_RE.search(url))
        if tag in {"img", "video"}:
            self.visual = True


def public_url(url):
    """Record the redirect origin/path, dropping transient signature parameters."""
    parts = urlsplit(url)
    return parts._replace(query="").geturl() if parts.hostname == "objects.githubusercontent.com" else url


class Redirects(HTTPRedirectHandler):
    def __init__(self):
        self.visits = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.visits.append({"status": code, "to": public_url(newurl)})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def alternate(url):
    parts = urlsplit(url)
    gh = re.fullmatch(r"/[^/]+/[^/]+/files/(\d+/[^/]+)", parts.path)
    if parts.hostname == "github.com" and gh:
        return f"https://github.com/user-attachments/files/{gh[1]}"
    if parts.hostname == "www.dropbox.com":
        query = dict(parse_qsl(parts.query))
        query["dl"] = "1"
        return urlunsplit(parts._replace(query=urlencode(query)))
    if parts.hostname == "excalidraw.com" and parts.fragment.startswith("json="):
        scene = parts.fragment[5:].split(",", 1)[0]
        return f"https://json.excalidraw.com/api/v2/{scene}"
    return None


def probe(url, cache):
    redirect = Redirects()
    opener = build_opener(redirect)
    result = {"url": url, "checked_utc": utc(), "redirects": redirect.visits}
    try:
        request = Request(url, headers={"User-Agent": "AF-RES-115 public artifact verification"})
        with opener.open(request, timeout=15) as response:
            data = response.read(10_000_001)
            result.update(landed=public_url(response.url), code=response.status,
                          bytes=len(data), content_type=response.headers.get_content_type(),
                          sha256=sha(data) if len(data) <= 10_000_000 else None)
        if len(data) > 10_000_000:
            result["status"] = "over_probe_limit"
        elif data[:4] == b"PK\x03\x04" or data.lstrip().startswith((b"{", b"<?xml", b"<museScore", b"<score-")):
            result["status"] = "bytes_need_parsing"
            (cache / result["sha256"]).write_bytes(data)
        else:
            result["status"] = "non_structured_response"
    except HTTPError as error:
        result.update(code=error.code, landed=public_url(error.url),
                      status="http_missing" if error.code in {404, 410} else "http_error")
    except OSError as error:
        result.update(landed=redirect.visits[-1]["to"] if redirect.visits else None,
                      status="proxy_denied" if "403 Forbidden" in str(error) else "fetch_error",
                      error=str(error))
    return result


def attachment_urls(issue):
    links = Links(issue["bodyHTML"])
    direct = [url for url in dict.fromkeys(links.hrefs)
              if PROBE_RE.search(url) or "#json=" in url]
    return links, direct


def scan_issues(scan, batch):
    raw = scan / "scan.csv"
    with raw.open(newline="", encoding="utf-8") as handle:
        scanned = list(csv.DictReader(handle))
    to_probe = {}
    for item in scanned:
        if not item["keyword_rank"] or item["error"]:
            continue
        project, number = item["project"], item["issue_number"]
        issue = json.loads((scan / project / f"{number}.json").read_text())
        links, direct = attachment_urls(issue)
        key = f'{project}{int(item["keyword_rank"]):02d}'
        batch.append((key, item, issue, links, direct))
        for url in direct:
            to_probe.setdefault(url, set()).add(key)
            if alt := alternate(url):
                to_probe.setdefault(alt, set()).add(key)
    return scanned, to_probe


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
                    encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cache", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--reuse-attempts", action="store_true")
    args = parser.parse_args()
    directory = args.destination
    output = directory / "evidence"
    output.mkdir(parents=True, exist_ok=True)
    files = args.cache / "attachments"
    files.mkdir(exist_ok=True)
    batch = []
    scanned, links = scan_issues(args.cache, batch)
    attempt_file = output / "attachment-attempts.jsonl"
    if args.reuse_attempts:
        attempts = [json.loads(line) for line in attempt_file.read_text().splitlines()]
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            attempts = list(pool.map(lambda u: {"frame_rows": sorted(links[u]), **probe(u, files)}, links))
        write_jsonl(attempt_file, attempts)
    lookup = {a["url"]: a for a in attempts}
    if set(lookup) != set(links):
        raise ValueError("attachment attempts do not cover this frame")
    for name in ("scan.csv", "scan-original.csv"):
        (output / ("frame-" + name)).write_bytes((args.cache / name).read_bytes())
    pages = [dict(attempt=attempt, **row) for attempt in ("initial", "partitioned")
             for project in ("E", "M") for row in json.loads((args.cache /
             f"{project}-lists{'-original' if attempt == 'initial' else ''}.json").read_text())]
    write_jsonl(output / "frame-pages.jsonl", pages)

    frame, sources = [], []
    for key, scan, issue, linkinfo, direct in batch:
        project, number = scan["project"], int(scan["issue_number"])
        body = issue["body"]
        author = (issue.get("author") or {}).get("login")
        if '"type":"excalidraw/clipboard"' in body:
            inline = "native_clipboard"
        elif XML_RE.search(body):
            inline = "native_score_xml_candidate"
        elif "<svg" in body:
            inline = "svg_expected_export"
        else:
            inline = ""
        direct_attempts = [lookup[u] for u in direct]
        if inline == "native_clipboard":
            state, disposition = "inline_native_read", "runnable_partial_structure"
        elif inline:
            state, disposition = "inline_output_or_schema_review", "review_only"
        elif direct_attempts:
            state = ";".join(sorted({a["status"] for a in direct_attempts}))
            disposition = "needs_artifact_or_semantic_review"
        elif linkinfo.visual:
            state, disposition = "visual_only", "excluded"
        else:
            state, disposition = "no_structured_opening_input", "excluded"
        duplicates = [
            edge["node"]["name"] for edge in issue["labels"].get("edges", [])
            if "duplicate" in edge["node"]["name"].casefold()
        ]
        duplicate_of = issue.get("duplicateOf") or {}
        frame.append({
            "row": key, **scan, "title": issue["title"], "author": author,
            "opening_body_version": issue["bodyVersion"], "attachment_state": state,
            "opening_attachment_urls": json.dumps(direct, ensure_ascii=False),
            "embedded_visual": str(linkinfo.visual).lower(), "opening_inline_structure": inline,
            "multiple_attachment_candidates": str(len(direct) > 1).lower(),
            "duplicate_flag": duplicate_of.get("url", ";".join(duplicates)),
            "disposition": disposition,
        })
        counted = (project, number) in ORIGINAL_REQUESTS
        sources.append({
            "source_id": key, "source_url": issue["url"], "landed_url": issue["landed"],
            "lineage": f'{scan["project"]}-issue-{number}', "author": author,
            "publication": issue["createdAt"], "edition": issue["bodyVersion"],
            "checked_utc": issue["opened"], "read_range": "opening Markdown and opening link attributes",
            "observed": f'{issue["title"]} | opening tokens {scan["keywords"]} | {state}',
            "limits": "최종 opening body 판에서 확인. 화면, 후속 파일과 실행은 원본 바이트 판정과 분리.",
            "questions": ["Q1"], "ledger_rows": [key],
            "allocation": "request" if counted else "frame",
            "unique_counted": counted, "origin_status": "opened",
            "opening_sha256": scan["body_sha256"],
        })
    output_keys = {"issue_number", "created_utc", "source_url", "landed", "opened_utc", "body_sha256"}
    for row in scanned:
        if row["keyword_rank"]:
            continue
        sources.append({
            "source_id": f'{row["project"]}-screen-{row["issue_number"]}',
            "source_url": row["source_url"], "landed_url": row["landed"] or None,
            "lineage": f'{row["project"]}-issue-{row["issue_number"]}',
            "author": None, "publication": row["created_utc"], "edition": None,
            "checked_utc": row["opened_utc"], "read_range": "automated opening body keyword screen",
            "observed": row["error"] or (row["keywords"] + " after cutoff" if row["keywords"] else "0 whole-token matches"),
            "limits": "생성순 검사용 자동 판독. 저작 배당과 수작업 해석에서 제외.",
            "questions": ["Q1"], "ledger_rows": [f'{row["project"]}:{row["scan_rank"]}'],
            "allocation": "screen", "unique_counted": False,
            "origin_status": "failed" if row["error"] else "screened",
            "opened_metadata": {key: row[key] for key in sorted(output_keys)},
        })
    for i, a in enumerate(attempts, 1):
        sources.append({
            "source_id": f"ATT{i:03d}", "source_url": a["url"], "landed_url": a.get("landed"),
            "lineage": a["frame_rows"], "author": "opening account or hosting service",
            "publication": None, "edition": a.get("sha256"), "checked_utc": a["checked_utc"],
            "read_range": "opening attachment URL and HTTP redirects",
            "observed": a["status"],
            "limits": "응답 상태 또는 파일 헤더 관측. 바이트를 받지 못한 경우 구조·만료 미확인.",
            "questions": ["Q1", "Q2"], "ledger_rows": a["frame_rows"], "allocation": "attachment_attempt",
            "unique_counted": False, "origin_status": a["status"],
        })
    for i, a in enumerate(pages, 1):
        sources.append({
            "source_id": f"LIST{i:03d}", "source_url": a["source_url"], "landed_url": a["landed"],
            "lineage": f'{a["project"]}-github-issue-index', "author": "GitHub",
            "publication": None, "edition": a["attempt"], "checked_utc": a["opened"],
            "read_range": f'page {a["page"]}, issue numbers {a["numbers"]}',
            "observed": f'{a["count_in_query"]} reported matches before body screen',
            "limits": "색인 페이지. 자료 하한에 산입하지 않음.",
            "questions": ["Q1"], "ledger_rows": [f'{a["project"]}:page-{a["page"]}'],
            "allocation": "index", "unique_counted": False, "origin_status": "index_only",
        })
    with (directory / "frame.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, list(frame[0]))
        writer.writeheader()
        writer.writerows(frame)
    write_jsonl(directory / "sources.jsonl", sources)
    for project in ("E", "M"):
        print(project, Counter(row["attachment_state"] for row in frame if row["project"] == project))
    print("attempts", Counter(a["status"] for a in attempts))
    print("read records", len(sources))


if __name__ == "__main__":
    main()
