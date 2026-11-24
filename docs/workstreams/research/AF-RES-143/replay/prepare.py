"""Create exact package locks, confirm published entry bytes and freeze static predictions."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from html.parser import HTMLParser
import json
import re
from pathlib import Path
from urllib.parse import unquote

from common import ROOT, Http, json_in, process, read_jsonl, sha, utc, write_csv, write_json, write_jsonl
from signals import (FUNCTIONS, after_edge, c_fingerprint, d_fingerprint, doc_path, e_fingerprint, entry,
                     matches, notice, release_assets)


class ReleaseBody(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "div" and (self.depth or dict(attrs).get("data-test-selector") == "body-content"):
            self.depth += 1

    def handle_endtag(self, tag):
        if tag == "div" and self.depth:
            self.depth -= 1

    def handle_data(self, data):
        if self.depth:
            self.parts.append(data)


def inventory(http, repo):
    cards, receipts = {}, []
    for n in range(1, 13):
        url = f"https://github.com/{repo}/releases?page={n}"
        raw, receipt = http.get(url)
        receipts.append(receipt)
        if raw is None:
            return cards, receipts, False
        if n == 1:
            _, api = http.get(f"https://api.github.com/repos/{repo}/releases?per_page=100&page=1")
            receipts.append(api | {"purpose": "API access diagnostic; browser HTML retained as evidence"})
        page = raw.decode()
        headings = list(re.finditer(r'<span [^>]*f1 text-bold[^>]*><a href="/' + re.escape(repo) +
                                    r'/releases/tag/([^"]+)"', page))
        for i, heading in enumerate(headings):
            limit = headings[i + 1].start() if i + 1 < len(headings) else len(page)
            html = page[heading.start():limit]
            stamp = re.search(r'<relative-time class="no-wrap" prefix="" datetime="([^"]+)"', html)
            tag = unquote(heading[1])
            body = ReleaseBody()
            body.feed(html)
            text = re.sub(r"\s+", " ", " ".join(body.parts)).strip()
            cards[tag] = dict(url=f"https://github.com/{repo}/releases/tag/{heading[1]}",
                              inventory_url=url, html_sha256=receipt["sha256"],
                              opened_utc=receipt["opened_utc"], displayed_publish=stamp[1] if stamp else None,
                              current_words=matches(text), body_bytes=len(text.encode()), body_sha256=sha(text.encode()),
                              has_body=bool(text))
        more = re.search(r'<a\b[^>]*class="next_page"[^>]*href=', page)
        terminal = re.search(r'<(?:span|em)\b[^>]*class="next_page disabled"', page)
        if not more:
            return cards, receipts, bool(terminal or not headings)
    return cards, receipts, False


def tags(repo):
    record = process(["git", "ls-remote", "--tags", f"https://github.com/{repo}.git"])
    if record["exit"] != 0:
        return {}, record
    parsed = {ref.removeprefix("refs/tags/"): commit for commit, ref in
              (line.split() for line in record["stdout"].splitlines())}
    record["stdout_sha256"] = sha(record.pop("stdout").encode())
    record["refs"] = len(parsed)
    return parsed, record


def find_tag(version, ref_map):
    marked = [name for name in (f"v{version}", version, f"simple-statistics@{version}") if name in ref_map]
    tag = next(iter(marked), "")
    return tag, ref_map.get(tag), ref_map.get(tag + "^{}", ref_map.get(tag))


def notice_status(version, published, cards, complete):
    card = next((cards[key] for key in ("v" + version, version, "simple-statistics@" + version) if key in cards), None)
    if card is None:
        return {"state": "absent-current-surfaces" if complete else "inventory-unavailable",
                "url": "", "limits": "삭제된 옛 공지는 확인 불가"}
    stamp = card["displayed_publish"]
    state = ("official-after-npm" if stamp and datetime.fromisoformat(stamp) > datetime.fromisoformat(published)
             else "time-unverified")
    return card | {"state": state, "last_edited_at": None, "limits": "현재 카드에서 마지막 편집 시각 확인 불가"}


def lock(package, version, dist, folder, cache):
    folder.mkdir(parents=True, exist_ok=True)
    project = {"name": "af-res-143-probe", "version": "1.0.0", "private": True, "dependencies": {package: version}}
    write_json(folder / "package.json", project)
    result = process(["npm", "install", "--package-lock-only", "--ignore-scripts", "--no-audit", "--no-fund",
                      "--cache", str(cache), "--registry", "https://registry.npmjs.org", "--fetch-retries", "1"], folder)
    if result["exit"] != 0:
        raise RuntimeError(result)
    tree = json_in(folder / "package-lock.json")
    locked = tree["packages"][f"node_modules/{package}"]
    if tree["lockfileVersion"] != 3 or locked["version"] != version or locked["resolved"] != dist["tarball"]:
        raise ValueError(f"lock did not pin {package}@{version}")
    if dist.get("integrity") and locked["integrity"] != dist["integrity"]:
        raise ValueError(f"lock SRI disagrees {package}@{version}")
    return {"project": project, "lock": tree}, result


def summarize_source(info, kind, ident, claim, locator, content, limits, counted=False):
    return dict(source_id=ident, work_id=ident.lower(), category="distribution", claim_ids=claim,
                publisher=info["package"], kind=kind, url=info["url"], edition_commit=info["edition"],
                publication_time=info.get("published"), opened_utc=info["at"], locator=locator, observed=content,
                access_limits=limits, evidence_level="직접 관측", counted=counted,
                count_reason="판별 데이터 또는 앞서 산입한 저작의 판 사본" if not counted else "독립 1차 저작")


def gather(package, repo, row, ref_map, cards, complete, scratch, static, cached):
    ver = row["version"]
    stem = f"{package}-{ver}"
    tmp = scratch / stem
    tmp.mkdir(exist_ok=True)
    http = Http()
    if cached:
        raw = (cached / f"{stem}.tgz").read_bytes()
        download = json_in(cached / f"{stem}.json")
    else:
        raw, download = http.get(row["dist"]["tarball"])
    if raw is None:
        # Preserve a registered release even when its archive could not be read.
        raise RuntimeError({"missing_archive": stem, "receipt": download})
    initial = row | {"package": package, "repo": repo}
    files, manifest, checks = release_assets(initial, raw)
    mode, public = entry(manifest)
    name, tag_object, commit = find_tag(ver, ref_map)
    pinned = row["git_head"] or commit
    tag_relation = ("same" if row["git_head"] == commit else "differ") if row["git_head"] and commit else (
        "tag-only identity" if commit else "npm gitHead only" if pinned else "identity unresolved")
    lock_data, lock_log = lock(package, ver, row["dist"], tmp / "lock", scratch / "npm-lock-cache")
    locations = lock_data["lock"]["packages"]
    direct = {}
    for field in ("dependencies", "optionalDependencies", "peerDependencies"):
        for dep, requirement in manifest.get(field, {}).items():
            where = next((x for x in (f"node_modules/{package}/node_modules/{dep}", f"node_modules/{dep}")
                          if x in locations), "")
            locked = locations.get(where, {})
            direct[dep] = {"field": field, "range": requirement, "version": locked.get("version"),
                           "integrity": locked.get("integrity")}
    release = initial | {"tag": name, "tag_oid": tag_object, "tag_commit": commit, "source_commit": pinned,
                         "tag_relation": tag_relation, "loader": mode, "entry": public,
                         "entry_sha256": sha(files[public]) if public in files else None,
                         "entry_bytes": len(files[public]) if public in files else None,
                         "tar_sha256": sha(raw), "tar_bytes": len(raw), "integrity_checks": checks,
                         "main": manifest.get("main"), "exports": manifest.get("exports"), "type": manifest.get("type"),
                         "direct": direct, "notice": notice_status(ver, row["published"], cards, complete),
                         "doc_urls": {}, "doc_sha256": {}}
    observations, c, d = [], {}, {}
    sources = [summarize_source(dict(package=package, url=download["url"], edition=ver,
                                    published=row["published"], at=download["opened_utc"]),
                                "npm 배포 아카이브", f"TAR-{stem}", ["Q1", "Q3", "Q4", "Q6"],
                                "package/package.json; 공개 entry, src, README, CHANGELOG 존재 여부",
                                f"검증 무결성 {checks}, {mode} {public}, entry {release['entry_sha256']}",
                                "배포 바이트와 manifest, 이 단계의 함수 출력 미열람.")]
    doc_checks = {}
    for fn in FUNCTIONS[package]:
        path = doc_path(package, fn)
        source = files.get(path)
        raw_url = f"https://raw.githubusercontent.com/{repo}/{pinned}/{path}" if pinned else ""
        if raw_url:
            fetched, event = http.get(raw_url)
            if raw_url not in doc_checks:
                doc_checks[raw_url] = event
                if fetched is not None:
                    sources.append(summarize_source(dict(package=package, url=raw_url, edition=pinned,
                                                         published=row["published"], at=event["opened_utc"]),
                                                    "고정 공식 기능 문서", f"DOC-{stem}-{fn}", ["Q1", "Q3"],
                                                    path + " 기능 절",
                                                    "배포본과 비교한 문서 원본, 바이트 동일 " + str(fetched == source),
                                                    "다른 판의 함수 계약 사본, 정책 판별에만 사용."))
            if fetched is not None and section_same(package, fn, fetched, source):
                release["doc_urls"][fn] = raw_url
                release["doc_sha256"][fn] = sha(fetched)
        if fn not in release["doc_urls"]:
            release["doc_urls"][fn] = row["dist"]["tarball"]
            release["doc_sha256"][fn] = sha(source) if source is not None else None
        c[fn] = c_fingerprint(package, fn, source)
        d[fn] = d_fingerprint(release, files, fn, c[fn])
    es, log, err = e_fingerprint(release, files, static, tmp / "tree", 2)
    if log:
        log["stdout_sha256"] = sha(log.pop("stdout").encode())
    info = {"package": package, "version": ver, "C": c, "D": d, "E": es.get("functions", {}),
            "E_error": err, "E_reads": es.get("reads", {}), "notice": notice(files, release)}
    return release, lock_data, info, sources, {"package": package, "version": ver, "tar": download,
                                              "docs": list(doc_checks.values()), "lock": lock_log, "static_parser": log}


def section_same(package, fn, remote, bundled):
    c_remote = c_fingerprint(package, fn, remote)
    c_bundled = c_fingerprint(package, fn, bundled)
    return c_remote["state"] == "resolved" and c_remote.get("sha256") == c_bundled.get("sha256")


def prediction_rows(cohorts, releases, static):
    for cohort in cohorts:
        package = cohort["package"]
        versions = [r["version"] for r in cohort["selected"]]
        for index, version in enumerate(versions):
            previous = versions[index - 1] if index else ""
            current = static[(package, version)]
            release = releases[(package, version)]
            for fn in FUNCTIONS[package]:
                row = dict(package=package, previous=previous, version=version,
                           publish_rank=index + 1, function=fn, cutoff_utc=release["published"],
                           doc_url=release["doc_urls"][fn], archive_url=release["dist"]["tarball"],
                           notice_url=release["notice"]["url"], notice_state=release["notice"]["state"],
                           current_notice_words=",".join(release["notice"].get("current_words", [])),
                           eligible_notice_words=",".join(current["notice"]["words"]))
                for policy in ("A", "C", "D", "E", "E2"):
                    decision, reason = ("initial", "first exact measurement") if not previous else after_edge(
                        policy, static[(package, previous)], current, fn)
                    row[policy] = decision
                    row[policy + "_reason"] = reason
                yield row


def releases_rows(releases):
    for r in releases:
        dist = r["dist"]
        yield {k: r.get(k) for k in ("package", "version", "cohort", "published", "publish_rank", "semver_rank",
                                     "repo", "tag", "tag_oid", "tag_commit", "git_head", "source_commit", "tag_relation",
                                     "tar_sha256", "tar_bytes", "loader", "entry", "entry_sha256", "entry_bytes",
                                     "main", "type", "deprecated_now")} | {
            "tarball": dist["tarball"], "integrity": dist["integrity"], "shasum": dist["shasum"],
            "exports": json.dumps(r["exports"], sort_keys=True, separators=(",", ":")),
            "direct": json.dumps(r["direct"], sort_keys=True, separators=(",", ":")),
            "lock_sha256": r["lock_sha256"], "notice": r["notice"]["state"],
        }


def parser_install(dest, cache):
    dest.mkdir(parents=True, exist_ok=True)
    pinned = json_in(ROOT / "replay/parser-lock.json")
    write_json(dest / "package.json", {"name": pinned["name"], "private": True,
                                       "dependencies": pinned["packages"][""]["dependencies"]})
    write_json(dest / "package-lock.json", pinned)
    receipt = process(["npm", "ci", "--ignore-scripts", "--no-audit", "--no-fund",
                       "--cache", str(cache), "--registry", "https://registry.npmjs.org"], dest)
    if receipt["exit"] != 0:
        raise RuntimeError(receipt)
    return receipt


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--scratch", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--cache-assets", type=Path)
    opt = p.parse_args()
    opt.scratch.mkdir(parents=True, exist_ok=True)
    opt.out.mkdir(parents=True, exist_ok=True)
    cohorts = json_in(ROOT / "evidence/roster.json")["cohorts"]
    parser = parser_install(opt.scratch / "parser", opt.scratch / "parser-cache")
    http = Http()
    jobs, provider_records = [], []
    for cohort in cohorts:
        package, repo = cohort["package"], cohort["repo"]
        ref_map, tag_log = tags(repo)
        cards, receipts, complete = inventory(http, repo)
        provider_records.append(dict(package=package, tag_log=tag_log, releases_inventory=receipts, complete=complete,
                                     tag_only_within_semver_window=tag_only(cohort, ref_map)))
        jobs.extend((package, repo, row, ref_map, cards, complete, opt.scratch, opt.scratch / "parser",
                     opt.cache_assets) for row in cohort["selected"])
    with ThreadPoolExecutor(max_workers=6) as pool:
        records = list(pool.map(lambda args: gather(*args), jobs))
    releases, locks, infos, sources, logs = map(list, zip(*records))
    keys = [(r["package"], r["version"]) for r in releases]
    for release, locked in zip(releases, locks):
        release["lock_sha256"] = sha((json.dumps(locked["lock"], ensure_ascii=False, indent=2) + "\n").encode())
    by_key = dict(zip(keys, releases))
    static = dict(zip(keys, infos))
    write_json(opt.out / "release-data.json", releases)
    write_json(opt.out / "locks.json", {"/".join(key): item for key, item in zip(keys, locks)})
    write_csv(opt.out / "releases.csv", list(releases_rows(releases)))
    write_csv(opt.out / "predictions.csv", list(prediction_rows(cohorts, by_key, static)))
    write_jsonl(opt.out / "static-components.jsonl", infos)
    write_jsonl(opt.out / "source-additions.jsonl", [source for group in sources for source in group])
    write_json(opt.out / "preparation.json", {"completed_utc": utc(), "archive_and_static": logs,
                                             "parser_install": parser, "providers": provider_records})


def tag_only(cohort, refs):
    def key(ver):
        return tuple(map(int, ver.split(".")))
    known = {row["version"] for row in cohort["selected"] + cohort["later_regular"]}
    bounds = [key(row["version"]) for row in cohort["selected"]]
    return [{"tag": name, "version": m[1], "commit": refs.get(name + "^{}", refs[name]),
             "state": "tag without currently recruited distribution"}
            for name in refs if (m := re.fullmatch(r"(?:v|simple-statistics@)?(\d+\.\d+\.\d+)", name))
            and min(bounds) <= key(m[1]) <= max(bounds) and m[1] not in known]


if __name__ == "__main__":
    main()
