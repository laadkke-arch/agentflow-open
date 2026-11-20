"""Read allowed public surfaces. Save timestamps, pointers and bounded match locations."""

import argparse
import hashlib
import itertools
import json
import re
import time
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit, urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener

from extract import ROOT, jsonl

ALLOWED = {"github.com", "raw.githubusercontent.com", "registry.npmjs.org", "pypi.org"}
USER_AGENT = "AF-RES-015-public-recommendation-research/1.0"
MAX_BYTES = 6_000_000
EMBEDDED = re.compile(
    r'<script type="application/json" data-target="react-app.embeddedData">(.*?)</script>',
    re.DOTALL,
)


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


class TextOnly(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def plain(html):
    parser = TextOnly()
    parser.feed(html)
    return re.sub(r"\s+", " ", " ".join(parser.parts))


class Reader:
    def __init__(self, interval):
        self.interval = interval
        self.after = {}
        self.paused = set()
        self.calls = []

    def reserve(self, url):
        host = urlsplit(url).hostname
        if host not in ALLOWED:
            raise URLError("outside allowed hosts")
        if host in self.paused:
            raise URLError("host paused on rate-limit or access response")
        wait = self.after.get(host, 0) - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        self.after[host] = time.monotonic() + self.interval

    def get(self, url):
        redirects = []
        reader = self

        class RoutedRedirect(HTTPRedirectHandler):
            def redirect_request(self, request, stream, code, msg, headers, new_url):
                reader.reserve(new_url)
                redirects.append({"http": code, "url": new_url})
                return super().redirect_request(request, stream, code, msg, headers, new_url)

        issued = utc_now()
        start = time.monotonic()
        reserved = False
        try:
            self.reserve(url)
            reserved = True
            opened = utc_now()
            request = Request(url, headers={"User-Agent": USER_AGENT})
            try:
                response = build_opener(RoutedRedirect()).open(request, timeout=13)
            except HTTPError as error:
                response = error
            with response:
                status = response.status
                final = response.geturl()
                fields = {key.lower(): value for key, value in response.headers.items()
                          if key.lower() in {"retry-after", "x-ratelimit-limit", "x-ratelimit-remaining"}}
                body = response.read(MAX_BYTES + 1).decode("utf-8", errors="replace")
            failure = "response exceeds bounded read" if len(body) > MAX_BYTES else None
            if status == 429 or (status == 403 and "retry-after" in fields):
                self.paused.add(urlsplit(url).hostname)
        except (URLError, TimeoutError, OSError) as error:
            status, final, fields, body, failure = None, None, {}, "", str(error)[:250]
            opened = locals().get("opened")

        info = {"url": url, "final_url": final, "http": status, "headers": fields,
                "requested_at": opened, "queued_at": issued, "checked_at": utc_now(),
                "seconds": round(time.monotonic() - start, 4), "redirects": redirects,
                "requests": int(reserved) + len(redirects), "failure": failure}
        self.calls.append(info)
        return info, body if status == 200 and not failure else ""


def payload(body):
    match = EMBEDDED.search(body)
    return json.loads(match.group(1)).get("payload", {}) if match else {}


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def read_rules():
    rules = {}
    for line in (ROOT / "data" / "github-rules.txt").read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        repo, field, key, pattern, claim = line.split("|", 4)
        rules.setdefault(repo, []).append(
            {"field": field, "key": key, "regex": re.compile(pattern, re.IGNORECASE),
             "confirmed": claim})
    return rules


def match_rules(patterns, fields, print_hits=False):
    hits = []
    for rule in patterns:
        value = fields.get(rule["field"], "")
        match = rule["regex"].search(value)
        if match:
            line = value.count("\n", 0, match.start()) + 1
            stamp = {"key": rule["key"], "field": rule["field"], "line": line,
                     "start": match.start(), "confirmed": rule["confirmed"]}
            hits.append(stamp)
            if print_hits:
                # Inspect a narrow region during execution. Raw bodies and snippets are never written.
                vicinity = value[max(0, match.start() - 35):match.end() + 55]
                print(f'  {rule["key"]}: ' + re.sub(r"\s+", " ", vicinity)[:155], flush=True)
    return hits


def repo_current(reader, rules, verbose):
    for repo, patterns in rules.items():
        info, body = reader.get(f"https://github.com/{repo}")
        data = payload(body)
        code = data.get("codeViewRepoRoute", {})
        layout = data.get("codeViewLayoutRoute", {}).get("repo", {})
        about = data.get("sidebarAbout", {})
        paths, values = {}, {}
        for entry in code.get("overview", {}).get("overviewFiles", []):
            path = entry.get("path")
            if not path:
                continue
            family = "readme" if path.lower().split("/")[-1].startswith("readme") else "license"
            paths[family] = path
            values[family] = plain(entry.get("richText") or "")
        license_value = (about.get("repo", {}).get("license") or {}).get("spdxId", "")
        if license_value:
            values["spdx"] = license_value
        values["desc"] = about.get("description") or ""
        ref = code.get("refInfo", {})
        print(repo, info["http"], ref.get("currentOid", "")[:12], flush=True)
        hits = match_rules(patterns, values, verbose)
        yield {"repo": repo, "canonical_repo": "/".join((layout["ownerLogin"], layout["name"]))
               if layout.get("name") and layout.get("ownerLogin") else None,
               "branch": ref.get("name"), "sha": ref.get("currentOid"),
               "archived": layout.get("isArchived"), "created_at": layout.get("createdAt"),
               "paths": paths, "spdx": license_value or None,
               "release_count": (about.get("sections", {}).get("releases") or {}).get("releaseCount"),
               "hits": hits, **info}


def commit_list(data):
    return list(itertools.chain.from_iterable(
        group.get("commits", [])
        for group in data.get("commitsRefRoute", {}).get("commitGroups", [])))


def release_rows(body):
    cards = re.finditer(r'<section[^>]*data-release-anchor="([^"]+)"[^>]*>(.*?)</section>',
                        body, re.DOTALL)
    for card in cards:
        label, html = card.groups()
        issued = re.search(r'released this\s*<relative-time[^>]*datetime="([^"]+)"', html)
        if issued:
            yield {
                "tag": label.removeprefix("release-"),
                "publishedAt": issued.group(1),
                "isPrerelease": bool(re.search(r"<span[^>]+>\s*Pre-release\s*</span>", html)),
            }


def evidence_at(reader, repo, commit, file_path):
    address = f"https://raw.githubusercontent.com/{repo}/{commit}/{quote(file_path, safe='/')}"
    return reader.get(address)


def primary_rows():
    return rows(ROOT / "REASONS.jsonl")


def verified_answer_dates():
    dates = {}
    for line in (ROOT / "data" / "answer-dates.txt").read_text().splitlines():
        if line and not line.startswith("#"):
            ref, day, location = line.split("|")
            dates[ref] = (day, location)
    return dates


def history(reader, rules, verbose, visited):
    verified = verified_answer_dates()
    current = rows(ROOT / "results" / "repo-now.jsonl")
    by_key = {rule["key"]: repo for repo, specs in rules.items() for rule in specs}
    dates = {}
    for reason in primary_rows():
        repo = by_key.get(reason["predicate"])
        answer_date = reason["answer_date"] or verified.get(reason["answer_ref"], (None, None))[0]
        if repo and answer_date and "후대 편집" not in reason["evidence_locator"]["position"]:
            dates.setdefault((repo, answer_date), set()).add(reason["predicate"])
    for item in current:
        repo, name = item["repo"], item["canonical_repo"]
        if not name or not item["branch"]:
            continue
        for (candidate, day), keys in sorted(dates.items()):
            if candidate != repo or (repo, day) in visited:
                continue
            until = (date.fromisoformat(day) + timedelta(days=1)).isoformat()
            path = f"https://github.com/{name}/commits/{quote(item['branch'], safe='/')}/"
            info, body = reader.get(path + "?" + urlencode({"until": until}))
            commits = commit_list(payload(body))
            # Only use a state already public before the answer's date. Same-day ordering is unknown.
            commit = next((c for c in commits if c.get("committedDate", "")[:10] < day
                           and c.get("committedDate") and c.get("oid")), None)
            if not commit:
                yield {"repo": repo, "answer_date": day, "keys": sorted(keys), "history": info,
                       "reason": "no dated preceding commit surfaced"}
                continue
            patterns = [rule for rule in rules[repo] if rule["key"] in keys]
            sha = commit["oid"]
            file_fields, file_observations = {}, {}
            for field in {rule["field"] for rule in patterns}:
                family = "license" if field == "spdx" else field
                file_path = item["paths"].get(family)
                if not file_path:
                    continue
                observation, contents = evidence_at(reader, name, sha, file_path)
                file_observations[field] = observation
                file_fields[field] = (identify_license(contents) if field == "spdx"
                                      else re.sub(r"\s+", " ", contents))
                if contents:
                    observation["sha256"] = hashlib.sha256(contents.encode()).hexdigest()
            print(repo, day, sha[:12], flush=True)
            yield {"repo": repo, "answer_date": day, "keys": sorted(keys), "history": info,
                   "commit": sha, "committed_at": commit["committedDate"], "files": file_observations,
                   "hits": match_rules(patterns, file_fields, verbose)}


def identify_license(text):
    low = text.casefold()
    if "business source license" in low:
        return "BUSL-1.1"
    if "zero clause bsd" in low or (
        "permission to use, copy, modify, and/or distribute this software for any purpose"
        in " ".join(low.split()) and "provided that" not in low
    ):
        return "0BSD"
    if "mozilla public license" in low or "mozilla.org/mpl/2.0" in low:
        return "MPL-2.0"
    if "apache license" in low and "version 2.0" in low:
        return "Apache-2.0"
    if "general public license" in low or "general public licence" in low:
        family = "AGPL" if "affero" in low else "LGPL" if "lesser" in low else "GPL"
        version = re.search(r"version\s+([23])", low)
        return f"{family}-{version.group(1)}.0" if version else family
    if "permission is hereby granted, free of charge" in " ".join(low.split()):
        return "MIT"
    if ("redistribution and use in source and binary forms" in " ".join(low.split())):
        return "BSD"
    if "cecill" in low:
        return "CeCILL"
    return ""


def repo_signals(reader, exclude=frozenset()):
    for item in rows(ROOT / "results" / "repo-now.jsonl"):
        if not item["canonical_repo"] or item["repo"] in exclude:
            continue
        url = f"https://github.com/{item['canonical_repo']}"
        query = quote(item["branch"], safe="/")
        commit_obs, commit_body = reader.get(f"{url}/commits/{query}/")
        first = next(iter(commit_list(payload(commit_body))), {})
        release_obs, release_body = reader.get(f"{url}/releases")
        releases = list(release_rows(release_body))
        yield {"repo": item["repo"], "commit_observation": commit_obs,
               "commit": {k: first.get(k) for k in ("oid", "committedDate", "url")},
               "release_observation": release_obs, "release_candidates": releases}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("now", "then", "signals"))
    parser.add_argument("--interval", type=float, default=1.06)
    parser.add_argument("--show-hits", action="store_true")
    parser.add_argument("--resume", action="store_true", help="only collect new dated repo pairs")
    args = parser.parse_args()
    if args.interval < 1:
        parser.error("per-host interval must be at least one second for this study")
    reader = Reader(args.interval)
    study = read_rules()
    path = ROOT / "results" / f"repo-{args.stage}.jsonl"
    append = args.stage == "then" and args.resume and path.exists()
    visited = {(x["repo"], x["answer_date"]) for x in rows(path)} if append else set()
    if args.stage == "now":
        evidence = repo_current(reader, study, args.show_hits)
    elif args.stage == "then":
        evidence = history(reader, study, args.show_hits, visited)
    else:
        evidence = repo_signals(reader)
    with path.open("a" if append else "w", encoding="utf-8", buffering=1) as stream:
        for observation in evidence:
            stream.write(json.dumps(observation, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
