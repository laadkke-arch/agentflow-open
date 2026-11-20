"""Read official registry records and GitHub project pages without retaining bodies."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html import unescape
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urlsplit
from urllib.request import Request, urlopen

from lxml import html

GITHUB_HOSTS = {"github.com", "raw.githubusercontent.com"}
REGISTRIES = {"pypi.org", "registry.npmjs.org"}


def short(line, words=23):
    line = re.sub(r"https?://\S+|[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}","",line)
    line = re.sub(r"(?<!\w)@[\w-]+", "", line)
    return " ".join(line.split()[:words]).strip()


def registry_url(requested):
    url = urlsplit(requested)
    if url.hostname == "pypi.org":
        name = url.path.strip("/").split("/")[1]
        return f"https://pypi.org/pypi/{quote(unquote(name))}/json"
    name = unquote(url.path.strip("/"))
    if name.endswith("/latest"):
        name = name[:-len("/latest")]
    return f"https://registry.npmjs.org/{quote(name, safe='@')}/latest"


def metadata(data, host):
    if host == "pypi.org":
        head = data["info"]
        return head["name"], head.get("summary"), head.get("version")
    return data["name"], data.get("description"), data.get("version")


def github_description(data):
    tree = html.fromstring(data)
    title = tree.xpath('string(//meta[@property="og:title"]/@content)').strip()
    tag_line = tree.xpath('string(//meta[@property="og:description"]/@content)').strip()
    if not title:
        title = tree.xpath('string(//title)').strip()
    if " · GitHub" in title:
        title = title.split(" · GitHub", 1)[0]
    if title.startswith("GitHub - "):
        title = title[len("GitHub - "):]
    match = re.search(r"GitHub - [^:]+:\s*(.+)", tag_line)
    if match:
        tag_line = match.group(1).split(" - GitHub", 1)[0].strip()
    if not tag_line or re.search(r"contribute to .* development by creating an account", tag_line, re.I):
        tag_line = title.partition(": ")[2]
    about = [short(a.text_content()) for a in tree.xpath(
        '//article[contains(@class,"markdown-body")]//p[not(ancestor::blockquote)]'
    )]
    about = [p for p in about if len(p.split()) >= 7 and not re.search(
        r"(?i)^(install|clone|see |join |download|visit |please |copyright|license|contribut|follow|thank|contact|website|build status|sponsor)",
        p,
    )]
    archive = "This repository has been archived by the owner" in data
    return title.split(": ", 1)[0], tag_line, (about[0] if about else None), archive


def capture(item):
    original = item["requested"]
    host = urlsplit(original).hostname
    target = registry_url(original) if host in REGISTRIES else original
    row = {"request": original, "observed_url": target, "observed_at_utc":
           datetime.now(timezone.utc).isoformat(timespec="seconds")}
    path = urlsplit(original).path
    if host in GITHUB_HOSTS and (len(path.strip("/").split("/")) < 2
                                 or re.search(r"/(issues|pull|discussions|users)(/|$)", path)):
        return row | {"error": "discussion/profile surface has no candidate documentation"}
    try:
        request = Request(target, headers={"User-Agent": "AF-RES-014 source research/1.0"})
        with urlopen(request, timeout=10) as response:
            data = response.read(3_000_000).decode("utf-8", "replace")
            row.update(status=response.status, observed_url=response.url)
    except HTTPError as exc:
        return row | {"status": exc.code, "error": "HTTP error"}
    except (URLError, TimeoutError, OSError) as exc:
        return row | {"error": type(exc).__name__}
    try:
        if host in REGISTRIES:
            title, excerpt, version = metadata(json.loads(data), host)
            notes, section, archive = None, "versioned registry summary/description", False
        elif host == "raw.githubusercontent.com":
            parts = [unescape(line).strip("# ") for line in data.splitlines()
                     if re.search(r"[a-zA-Z]", line) and not re.match(r"^(<|!|\[|\|)", line)]
            title, excerpt, version = parts[0], parts[1] if len(parts) > 1 else None, "live"
            notes, section, archive = None, "README/document heading and opening prose", False
        else:
            title, excerpt, notes, archive = github_description(data)
            version, section = "live", "repository About and README opening, when visible"
    except (ValueError, KeyError, IndexError) as exc:
        return row | {"error": f"unrecognized provider record ({type(exc).__name__})"}
    if not title or title in {"GitHub", "Page not found"}:
        return row | {"error": "candidate identity not identified"}
    short_description = short(excerpt or notes or "", 21)
    return row | {"title": short(title, 12), "excerpt": short_description, "version": version,
                  "section": section, "archived": archive}


def main():
    manifest, output = map(Path, sys.argv[1:3])
    inputs = list({x["requested"]: x for x in json.loads(manifest.read_text())}.values())
    with ThreadPoolExecutor(max_workers=8) as pool:
        rows = list(pool.map(capture, inputs))
    output.write_text(json.dumps(rows, ensure_ascii=False) + "\n")
    print(f"records={len(rows)} read={sum('error' not in row for row in rows)}")


if __name__ == "__main__":
    main()
