"""Generate auditable AF-RES-019 controls from frozen candidate order and Git facts."""
from argparse import ArgumentParser
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

from collect import STUDY, at_date, end_of_day, git_text, load_json, parse_day
from collect import prepare_repo, previous_months, save_json, snapshot_set

# Exploratory choices use category relevance before numerical distance. Specific negative
# calibration for SciPy keeps its otherwise eligible row outside the comparison.
SELECT = {
    "A01": 2, "A02": 1, "A03": 1, "A04": 1, "A05": 1, "A06": 1, "A07": 2, "A08": 2,
    "B01": 1, "B02": 1, "B03": 1, "B04": 1, "B05": 1, "B06": 1, "B07": 1, "B08": 1,
    "C01": 1, "C02": 1, "C03": 1, "C04": 2, "C05": 1, "C06": 2, "C07": 2, "C08": 1,
    "D01": 1, "D02": 3, "D03": 3, "D04": 1, "D05": 1, "D06": 1, "D07": 1, "D08": 1,
    "E01": 1, "E02": 2, "E03": 3, "E04": 1, "E05": 1, "E06": 1, "E07": 1, "E08": 1,
}
FEATURE_WITNESSES = {
    "K-C05-1": ("drivers/docker/driver.go",),
    "K-C06-2": ("packages/core/src/render3/component.ts", "packages/platform-browser/src/browser.ts"),
}
DOCS = {
    "B01": ("GeForce NOW 서비스와 기기별 클라우드 게임 안내", "NVIDIA 지역 페이지 전환. 가격제·카탈로그가 같은지는 미확인."),
    "B02": ("공식 공개 학술 검색과 API 제품", "기본 홈페이지 열람 오류. API 문서와 2021 운영 기록은 문헌 묶음에서 보강 대상."),
    "B03": ("파일 업로드, 링크 공유, 수신 기능", "현재 운영 문서는 2020년의 연속 운영을 자체적으로 입증하지 않는다."),
    "B04": ("현재 Flash 에뮬레이터와 브라우저 실행 목적", "공급자 Flash 지원이 아닌 독립 에뮬레이터의 조건이다."),
    "B05": ("현재 Dassault 제품 주소가 3DEXPERIENCE 데이터 서비스로 이동", "2012–2013 RSS 기능을 현재 주소만으로 검증할 수 없다."),
    "B06": ("무료 웹서비스와 데이터스토어 이용 문서", "현재 무료 제한 조건과 2022년 조건이 동일한지는 미확인."),
    "B07": ("바이너리 배포 기능과 Buildkite 인수 후 이름 변경", "2020–2021 당시 이용 범위의 끊김 없는 지원은 추가 확인 필요."),
    "B08": ("현재 무료 코딩 학습 안내", "모바일 다중언어 실행과 2025–2026 창은 현재 소개만으로 입증되지 않는다."),
}


def summarize_facts(v):
    return {key: v.get(key) for key in ("head", "first_commit_date", "first_commit_year",
                                       "authors_365d", "author_bin", "unknown")}


def compare(event, candidate, e_facts, c_facts):
    a, b = e_facts.get("first_commit_year"), c_facts.get("first_commit_year")
    diff = abs(a - b) if a is not None and b is not None else None
    bins = (e_facts.get("author_bin"), c_facts.get("author_bin"))
    return {"ecosystem": candidate["ecosystem"], "category": candidate["category"],
            "category_fit": candidate["category_fit"], "category_evidence": candidate["category_evidence"],
            "event_git": summarize_facts(e_facts), "control_git": summarize_facts(c_facts),
            "first_commit_year_distance": diff, "author_bin_equal": bins[0] == bins[1] if all(bins) else None}


def inspect_candidate(row, event, scratch):
    eid, t = event["id"], event["effective_date"]
    if row["category_fit"] == "서비스":
        seen, limitation = DOCS[eid]
        return {"check": "service_analogue", "source": row["review_url"], "confirmed": seen, "limits": limitation}
    if not row["repo_url"] or not t:
        return {"check": "undated", "source": row["review_url"], "limits": "정확한 T가 없어 같은 창을 정할 수 없다."}
    if row["id"] == "K-C04-1":
        return {"check": "excluded_same_type_event",
                "source": "https://docs.scipy.org/doc/scipy/release/1.13.0-notes.html",
                "confirmed": "2024년 1.13에서 scipy.linalg의 tri/triu/tril이 제거됐다는 릴리스 기록을 별도 확인했다.",
                "limits": "연도·작성자 구간이 맞아도 같은 사건 유형이면 제외."}
    repo, receipt = prepare_repo(row["repo_url"], scratch / "repos")
    if receipt["exit_code"]:
        return {"check": "git_failed", "source": row["review_url"], "limits": "복제 실패"}
    dates = (previous_months(date.fromisoformat(t), 12).toordinal(), parse_day(t) - 1)
    followup = min(parse_day(t) + 365, parse_day("2026-11-20"))
    refs = {}
    for day in (*dates, followup):
        sha = git_text(repo, ["log", "-1", "--first-parent", "--before=" + end_of_day(day),
                              "--format=%H", receipt["head"]]).strip()
        refs[day] = sha or None
    traffic = []
    snapshots = snapshot_set(repo, refs, row.get("package"), row["project"], traffic)
    witness_files = FEATURE_WITNESSES.get(row["id"], ())
    proof = {}
    for day, snap in snapshots.items():
        found = []
        if witness_files:
            out = git_text(repo, ["ls-tree", "-r", "--name-only", snap["sha"], "--", *witness_files])
            found = out.splitlines()
        files = [p for p in (snap["paths"][0], snap["paths"][2], *found) if p]
        proof[at_date(day)] = {"sha": snap["sha"], "readme_checked": snap["readme_exists"],
                              "license_family": snap["license"], "project_notice_words": snap["notices"],
                              "feature_paths": found, "files": files,
                              "urls": [row["review_url"] + "/blob/" + snap["sha"] + "/" + path for path in files]}
    observed = [snapshots.get(d, {}) for d in dates]
    licenses = [v.get("license") for v in observed]
    license_ok = all(lic in {"Apache", "MIT", "BSD", "MPL", "GPL", "AGPL"} for lic in licenses)
    license_ok = license_ok and len(set(licenses)) == 1
    readme_ok = all(v.get("readme_exists") and not v["notices"] for v in observed)
    features_ok = bool(witness_files) and all(proof.get(at_date(d), {}).get("feature_paths") for d in dates)
    pkg = row.get("package")
    registry = {}
    if pkg:
        from collect import cache_name
        receipt_path = scratch / "registry" / (cache_name(pkg) + ".json")
        if receipt_path.exists():
            cached = load_json(receipt_path)
            registry = {"http_code": cached.get("http_code"),
                        "latest": cached.get("latest_version"),
                        "live_inactive": cached.get("current_latest_inactive"),
                        "release_count_window": sum(dates[0] <= d <= dates[1] for d, _ in cached.get("dated_versions", []))}
    checks = {"license": license_ok, "feature": features_ok, "abandon": readme_ok,
              "deprecated": readme_ok and registry.get("live_inactive") is False
                            and registry.get("release_count_window", 0) >= 1}
    return {"check": "scoped_history_supported" if checks.get(event["type"]) else "historical_scope_incomplete",
            "source": row["review_url"], "window": [at_date(d) for d in dates], "snapshots": proof,
            "registry": registry,
            "limits": "작업자 판정. 선택한 경로·README·라이선스 계열 및 기간 내 판을 확인했다. "
                      "리버트된 내부 결정, 모든 릴리스 내용, 레지스트리 과거 표시 로그는 가시 범위 밖이다.",
            "http_requests": sum(x["requests"] for x in traffic)}


def build(events, candidates, facts, scratch, jobs):
    output, rejected = [], []
    by_id = {c["id"]: c for c in candidates}
    tasks = [(event, by_id[f"K-{event['id']}-{SELECT[event['id']]}"]) for event in events]
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        outcomes = list(pool.map(lambda pair: inspect_candidate(pair[1], pair[0], scratch), tasks))
    for (event, candidate), witness in zip(tasks, outcomes):
        eid, cid = event["id"], candidate["id"]
        fields = compare(event, candidate, facts[eid], facts[cid])
        numeric = fields["first_commit_year_distance"] is not None and fields["first_commit_year_distance"] <= 2
        eligible = numeric and fields["author_bin_equal"] and fields["category_fit"] == "정확"
        state = "strict" if eligible and witness["check"] == "scoped_history_supported" else "exploratory"
        if candidate["category_fit"] == "서비스":
            state = "service_analogue"
        elif not event["effective_date"]:
            state = "undated"
        output.append({"id": "C-" + eid, "candidate_id": cid, "matched_event": eid,
                       "project": candidate["project"], "repo_url": candidate["repo_url"], "package": candidate["package"],
                       "category": event["category"], "ecosystem": event["ecosystem"],
                       "matching_fields": fields, "status": state, "no_event_check": witness})
        for alternative in (r for r in candidates if r["matched_event"] == eid and r["id"] != cid):
            alt = alternative["id"]
            comparison = compare(event, alternative, facts[eid], facts[alt])
            status = "same_type_event" if alt == "K-C04-1" else "unselected"
            rejected.append({"candidate_id": alt, "matched_event": eid, "project": alternative["project"],
                             "matching_fields": comparison, "status": status})
    return output, rejected


def main():
    parser = ArgumentParser()
    parser.add_argument("--scratch", required=True, type=Path)
    parser.add_argument("--jobs", type=int, default=5)
    args = parser.parse_args()
    records = load_json(STUDY / "events/EVENTS.json")
    candidates = load_json(STUDY / "controls/CANDIDATES.json")
    facts = {r["id"]: r for r in load_json(args.scratch / "matching.json")}
    controls, rejected = build(records, candidates, facts, args.scratch, args.jobs)
    save_json(STUDY / "controls/CONTROLS.json", controls)
    save_json(STUDY / "controls/UNSELECTED.json", rejected)
    print(Counter(r["status"] for r in controls))
    for r in controls:
        print(r["id"], r["status"], r["project"], r["no_event_check"]["check"])


if __name__ == "__main__":
    main()
