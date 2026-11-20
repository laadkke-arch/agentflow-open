"""Summarize observed public-request costs per signal surface."""

import json
import statistics

from collect import ROOT, rows


def stats(items):
    if not items:
        return None
    return {"n": len(items), "requests_mean": statistics.mean(x["requests"] for x in items),
            "seconds_mean": statistics.mean(x["seconds"] for x in items),
            "seconds_median": statistics.median(x["seconds"] for x in items)}


def main():
    git = rows(ROOT / "results/repo-signals.jsonl")
    metadata = rows(ROOT / "results/repo-now.jsonl")
    licence = rows(ROOT / "results/license-observations.jsonl")
    keys = {
        "github_archived": stats(metadata), "repo_moved": stats(metadata),
        "commit_age": stats([x["commit_observation"] for x in git]),
        "release_age": stats([x["release_observation"] for x in git]),
        "npm_deprecated": stats(rows(ROOT / "results/registry.jsonl")),
        "license_change": stats([
            {"requests": x["old_request"]["requests"] + x["new_request"]["requests"],
             "seconds": x["old_request"]["seconds"] + x["new_request"]["seconds"]} for x in licence
        ]),
    }
    keys["license_change"]["note"] = "캐시를 무시한 두 면의 관측 비용 합산. 고정 SHA 탐색 비용 별도."
    for signal in ("http_dead", "domain_redirect"):
        keys[signal] = {"n": 0, "requests_mean": 0, "seconds_mean": None,
                        "note": "011의 관측 재사용. 순수 오프라인 조인 시간 미계측."}
    keys.update(maintained=None, registration_change=None)
    (ROOT / "results/signal-costs.json").write_text(
        json.dumps(keys, ensure_ascii=False, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
