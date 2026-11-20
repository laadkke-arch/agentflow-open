"""Combine distinct public signals with fixed prior link observations."""

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from collect import ROOT, read_rules, rows
from extract import jsonl, upstream

SIGNALS = {
    "http_dead": "HTTP 404/410", "domain_redirect": "리다이렉트 외부 도메인",
    "github_archived": "GitHub archived", "repo_moved": "저장소 이동",
    "commit_age": "마지막 커밋 365일 초과", "release_age": "마지막 릴리스 365일 초과",
    "license_change": "라이선스 조건 변경", "npm_deprecated": "npm 버전 deprecated",
    "maintained": "Scorecard Maintained < 5", "registration_change": "등록 주체 변경",
}
TWO_LEVEL_SUFFIXES = {"co.uk", "org.uk", "ac.uk", "com.au", "co.jp", "co.kr",
                      "ac.kr", "co.nz", "com.br", "com.tr", "gov.uk"}
DETERMINATE = {"성립", "약화", "무너짐"}
POLARITY = {"성립": False, "약화": False, "무너짐": True}


def site_key(url):
    if not url:
        return None
    parts = urlsplit(url)
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(),
                       parts.path.rstrip("/"), parts.query, ""))


def registrable_host(url):
    host = urlsplit(url or "").hostname
    if not host:
        return None
    parts = host.casefold().rstrip(".").split(".")
    suffix = ".".join(parts[-2:])
    return ".".join(parts[-3:]) if suffix in TWO_LEVEL_SUFFIXES else suffix


def observed(value, url=None, checked_at=None, raw=None, note=None):
    return {"positive": value, "url": url, "checked_at_utc": checked_at,
            "raw": raw, "note": note}


def link_observations():
    baseline = upstream("CASES.json")
    aging = upstream("evidence/aging-observations.json")
    results = {}
    for case in baseline["cases"]:
        for item in case["link_status_now"]:
            if item.get("url"):
                results[(case["id"], site_key(item["url"]))] = item
    for item in aging["current_link_observations"]:
        if item.get("url"):
            key = item["case_id"], site_key(item["url"])
            results[key] = {
                "url": item["url"], "status": item["original_status"],
                "final_url": item.get("final_url"), "observed_at_utc": item.get("observed_at_utc"),
                "explicit": item.get("http_status_explicit"),
                "class": item.get("audit_class"), "level": "AF-RES-011",
            }
    return results


def evaluate_link(item):
    if not item:
        none = observed(None, note="미확인(고정 링크 원장에 정확히 대응하는 주소 없음)")
        return {"http_dead": none, "domain_redirect": none}
    status = item["status"]
    explicit = item.get("explicit")
    reachable = status in {"accessible", "redirected", "archived"}
    dead = True if explicit in {404, 410} else False if reachable else None
    original, last = item["url"], item.get("final_url")
    domain_move = (registrable_host(original) != registrable_host(last)
                   if reachable and registrable_host(last) else None)
    original_fields = {k: item.get(k) for k in ("status", "final_url", "explicit", "class")}
    stamp = item.get("observed_at_utc")
    msg = "011의 고정 단회 관측. 수집 시 HTTP 호출 없음. 과부하/차단의 대체 주소는 제외."
    return {"http_dead": observed(dead, original, stamp, original_fields, msg),
            "domain_redirect": observed(domain_move, original, stamp, original_fields, msg)}


def age_signal(when, info, raw, at, label):
    days = (at - date.fromisoformat(when[:10])).days if when else None
    return observed(days > 365 if days is not None else None, info.get("url"),
                    info.get("checked_at"), {"days": days, **raw}, label)


def repo_signals(repo, timed, at):
    if not repo:
        none = observed(None, note="미확인(공식 GitHub 원격 매핑 부재)")
        return {name: none for name in ("github_archived", "repo_moved", "commit_age", "release_age")}
    checked, url = repo["checked_at"], repo["url"]
    current = repo["canonical_repo"]
    moved = repo["repo"].casefold() != current.casefold() if current else None
    vals = {
        "github_archived": observed(repo["archived"], url, checked,
                                    {"archived": repo["archived"], "repo": current}),
        "repo_moved": observed(moved, url, checked, {"from": repo["repo"], "to": current},
                               "관찰한 공식 GitHub 원격에서 도착한 정규 ID 비교"),
    }
    if not timed:
        none = observed(None, note="미확인(공식 커밋·릴리스의 최신 날짜 재수집)")
        vals.update(commit_age=none, release_age=none)
        return vals
    commit = timed["commit"]
    release = max((item for item in timed["release_candidates"] if not item["isPrerelease"]),
                  key=lambda item: item["publishedAt"], default={})
    vals["commit_age"] = age_signal(commit.get("committedDate"), timed["commit_observation"],
                                    commit, at, "기본 브랜치의 관측된 첫 커미터 시각")
    vals["release_age"] = age_signal(release.get("publishedAt"), timed["release_observation"],
                                     release, at, "릴리스 목록 첫 페이지에 보이는 일반 릴리스")
    return vals


def license_signals():
    path = ROOT / "results" / "license-observations.jsonl"
    sources = rows(path) if path.exists() else []
    return {(x["repo"], x["date"]): observed(
        x["changed"], x.get("now_url"), x.get("observed_at"),
        {k: x.get(k) for k in ("old_id", "new_id", "old_hash", "new_hash", "old_url")},
        x["interpretation"]) for x in sources}


def attach(records):
    now = {x["repo"]: x for x in rows(ROOT / "results/repo-now.jsonl")}
    timed = {x["repo"]: x for x in rows(ROOT / "results/repo-signals.jsonl")}
    pkg = {key: r for r in rows(ROOT / "results/registry.jsonl") for key in r["predicates"]}
    by_key = {rule["key"]: repo for repo, rules in read_rules().items() for rule in rules
              if repo in now and now[repo]["http"] == 200}
    extra = ROOT / "data" / "signal-repo-map.txt"
    if extra.exists():
        for line in extra.read_text().splitlines():
            if line and not line.startswith("#"):
                pred, repo = line.split("|")
                by_key[pred] = repo
    links, licenses = link_observations(), license_signals()
    at = date(2026, 11, 20)

    for row in records:
        pred = row["predicate"]
        repo = by_key.get(pred)
        values = evaluate_link(links.get((row["answer_ref"][:4], site_key(row["url"]))))
        values.update(repo_signals(now.get(repo), timed.get(repo), at))
        values["license_change"] = licenses.get((repo, row["answer_date"])) or observed(
            None, note="미확인(같은 대상의 앞뒤 라이선스 파일 조합 없음)")
        package = pkg.get(pred)
        values["npm_deprecated"] = (
            observed(package["deprecated"], package["url"], package["checked_at"],
                     {k: package[k] for k in ("package", "version", "deprecation_message")},
                     "npm 최신 공개 메타데이터. 답의 구판 설치 가능성과 구별")
            if package else observed(None, note="미확인(동일 아티팩트 버전 미매핑)")
        )
        values["maintained"] = observed(None, note="미확인(점수와 분석 SHA 필요)")
        values["registration_change"] = observed(None, note="미확인(과거·현재 등록인 공개 자료 필요)")
        row["signals"] = values
        yield row


def select_matrix(records, key, include_weak=False, verified_then=False, unique=False):
    usable = []
    seen = set()
    for row in records:
        verdict = row["now_verdict"]
        if verdict not in DETERMINATE or row["then_verdict"] == "처음부터 틀림":
            continue
        if verified_then and row["then_verdict"] != "성립":
            continue
        if key in {"github_archived", "commit_age", "release_age"} and row["reason_type"] == "관리 상태":
            continue
        # The same legal state forms part of the answer key for these rows.
        if key == "license_change" and row["reason_type"] == "라이선스":
            continue
        signal = row["signals"][key]["positive"]
        if signal is None:
            continue
        label = POLARITY[verdict] or (include_weak and verdict == "약화")
        signature = (row["candidate"].casefold(), label, signal)
        if unique and signature in seen:
            continue
        seen.add(signature)
        category = ("TP" if signal else "FN") if label else ("FP" if signal else "TN")
        usable.append((category, row))

    tally = Counter(category for category, _ in usable)
    precision_n = tally["TP"] + tally["FP"]
    recall_n = tally["TP"] + tally["FN"]
    examples = {}
    for tag in ("FN", "FP", "TP"):
        names = set()
        examples[tag] = []
        for category, row in usable:
            if category != tag or row["candidate"] in names:
                continue
            names.add(row["candidate"])
            if len(examples[tag]) < 8:
                examples[tag].append({
                    "reason_id": row["reason_id"], "candidate": row["candidate"],
                    "reason": row["reason_target"], "evidence": row["now_evidence_url"],
                    "signal_evidence": row["signals"][key]["url"],
                })
    return {"n": len(usable), **{k: tally[k] for k in ("TP", "FN", "FP", "TN")},
            "precision": tally["TP"] / precision_n if precision_n else None,
            "recall": tally["TP"] / recall_n if recall_n else None, "examples": examples}


def export(records):
    with (ROOT / "SIGNALS.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(("reason_id", "answer_ref", "candidate", "signal", "flag",
                         "collected_at_utc", "url", "raw", "limit"))
        for row in records:
            for key, values in row["signals"].items():
                flag = values["positive"]
                writer.writerow((row["reason_id"], row["answer_ref"], row["candidate"], key,
                                 "unknown" if flag is None else int(flag), values["checked_at_utc"],
                                 values["url"], json.dumps(values["raw"], ensure_ascii=False),
                                 values["note"]))
    result = {
        key: {"name": name, "strict": select_matrix(records, key),
              "weak_positive": select_matrix(records, key, include_weak=True),
              "verified_then": select_matrix(records, key, verified_then=True),
              "deduplicated": select_matrix(records, key, unique=True)}
        for key, name in SIGNALS.items()
    }
    (ROOT / "results" / "confusion.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    )


def main():
    path = ROOT / "REASONS.jsonl"
    records = list(attach(rows(path)))
    jsonl(path, records)
    export(records)


if __name__ == "__main__":
    main()
