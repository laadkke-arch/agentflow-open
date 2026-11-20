"""Build a source register from reviewed notes, answer positions, and observations."""

from collections import Counter, defaultdict
from urllib.parse import urlsplit
import json
import re

from adjudicate import web_findings
from collect import ROOT, rows
from extract import SHA, upstream

RESULTS = ROOT / "results"
DATE = "2026-11-20"
BASE = "https://github.com/laadkke-arch/agentflow-open/blob/"
FIXED = BASE + SHA + "/docs/workstreams/research/AF-RES-011/"


def source(key, url, at, kind, title, version, where, confirms, limits, level, uses):
    return {
        "id": key, "url": url, "accessed_at_utc": at, "source_type": kind,
        "title": title, "version_or_date": version, "sections_read": where,
        "confirmed": confirms, "limits": limits, "level": level, "used_in": uses,
    }


def site(url):
    host = urlsplit(url).hostname
    if host.endswith(("github.com", "githubusercontent.com", "github.io")):
        return "github.com"
    if host.endswith("thomsonreuters.com"):
        return "thomsonreuters.com"
    if host.endswith("lexisnexis.com"):
        return "lexisnexis.com"
    if host.endswith(("wikimedia.org", "wikipedia.org")):
        return "wikimedia.org / wikipedia.org"
    return host.removeprefix("www.")


def method_sources(web, fixed):
    noted, sites = {}, Counter()
    for line in (ROOT / "data" / "method-findings.txt").read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        key, kind, title, version, where, confirms, limits, uses, category = line.split("|")
        seen = web.get(key) or fixed[key]
        if not (seen.get("viewable") or seen.get("line")):
            raise ValueError(f"Source has no recorded body: {key}")
        host = site(seen["url"])
        counts = category != "companion" and sites[host] < 3
        if counts:
            sites[host] += 1
        level = "D3-fetch" if kind == "공식 원본 코드" else "D1"
        noted[key] = source(key, seen["url"], seen.get("checked_at_utc") or seen["checked_at"],
                           kind, title, version, where, confirms, limits, level, uses.split(","))
        noted[key].update(category=category, site_group=host, counts_toward_minimum=counts)
    return noted


def recommendation_sources(reasons):
    per_thread = defaultdict(list)
    for row in reasons:
        per_thread[row["answer_ref"].split(".")[0]].append(row)
    yield source("FIX-011-CASES", FIXED + "CASES.json", DATE, "고정 입력", "AF-RES-011 CASES",
                 SHA, "cases.answers, constraints, link_status_now", "61스레드와 635개 고정 답 위치를 제공한다.",
                 "답이 편집되거나 댓글만 있으면 문장과 시각을 다시 대조했다. 날짜 정밀도는 일 단위다.",
                 "D1", ["Q1", "Q4"])
    yield source("FIX-011-AGING", FIXED + "evidence/aging-observations.json", DATE,
                 "고정 관측", "AF-RES-011 원래 주소 관측", SHA, "HTTP, final URL, unavailable/blocked",
                 "281회 관측에서 명시적 404 URL 네 개를 남겼다.",
                 "단회 요청이므로 주소 상태의 반복 확인이나 추천 조건의 판정은 없었다.", "D3-fetch", ["Q4", "Q7"])
    nine = BASE + "7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/"
    for file, where, confirms in (
        ("HANDOFF.md", "결론, 남은 확인", "재검토 가설과 이미 확인한 중단 사례의 범위를 확인했다."),
        ("FAILURES.md", "중단·전환 7건", "서비스 유지 방식과 실제 중단 사례를 구분했다."),
        ("LANDSCAPE.md", "유지 방식 비교", "보존과 현행 근거 관리를 분리한 배경을 확인했다."),
        ("SYSTEMS.json", "maintenance fields", "체계별 과거 조사에서 갱신 방식을 어떻게 분류했는지를 확인했다."),
    ):
        yield source("FIX-009-" + file.split(".")[0], nine + file, DATE, "고정 선행 연구",
                     "AF-RES-009 " + file, "7f627a81199f06da7f7b15f979e7fef25dd17602", where,
                     confirms, "이번 실행의 모집단과 신호 성능을 측정하지 않았다.", "D1", ["Q6", "Q8"])
    for case in upstream("CASES.json")["cases"]:
        selected = per_thread[case["id"]]
        direct = [r for r in selected if r["evidence_locator"]["basis"] == "원문"]
        snippets = direct or selected
        examples = "; ".join(f'{r["candidate"]} — {r["reason_target"]}' for r in snippets[:2])
        locators = "; ".join(r["evidence_locator"]["position"] for r in direct[:4])
        finding = (f"{len(selected)}개 기록 중 원문으로 대조한 {len(direct)}개. {examples}" if selected
                   else "스레드와 고정 답 위치가 있다. 재현 가능한 귀속으로 이유를 추가하지 못했다.")
        yield source(case["id"], case["url"], DATE, "공개 원 스레드", f'{case["id"]} 추천 스레드',
                     case.get("date") or "live", locators or "스레드·고정 입력 답별 위치",
                     finding, "답별 재현 자료는 REASONS.jsonl. 정확한 UTC 시각은 답에 표시된 경우만 사용했다. 열람 시간은 날짜 정밀도.",
                     "D3-fetch" if direct else "D1", ["Q1", "Q3"])


def execution_sources(reasons, fixed, web):
    yield from recommendation_sources(reasons)
    for line in (ROOT / "data" / "anchor-findings.txt").read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        key, version, title, where, confirms = line.split("|")
        record = web[key]
        yield source(key, record["url"], record["checked_at_utc"], "공식 버전 출시 공지",
                     title, version, where, confirms,
                     "배포판의 공개 시각을 보강한다. 개별 기능은 고정판 파일에서 확인했다.", "D1", ["Q3"])
    for record in rows(RESULTS / "tag-date-observations.jsonl"):
        if record.get("published_utc"):
            yield source("TAG-" + record["id"], record["url"], record["checked_at"], "공식 GitHub 릴리스·태그",
                         record["id"], record["checked_version"], "GitHub release relative-time and tag",
                         f'표시된 공개 시각은 {record["published_utc"]}.',
                         "태그 소스의 기능·조건은 같은 판을 따로 읽었다.", "D3-fetch", ["Q3"])
    for key in ("H-DJ-AUTH", "H-PTA-GIT2"):
        record = fixed[key]
        if record.get("line"):
            yield source(key, record["url"], record["checked_at"], "보강용 Git 고정판",
                         record["title"], record["url"].split("/")[5], f'L{record["line"]}',
                         record["confirmed"], "현재 동작이나 배포 범위는 별도다.", "D2", ["Q3"])
    for entry in web_findings():
        if entry["viewable"] and not re.search(r"(502|차단|미도달)", entry["sections_read"]):
            yield source(entry["id"], entry["url"], entry["checked_at"], "공식 웹 문서 또는 공지",
                         entry["title"], "live", entry["sections_read"], entry["confirmed"], entry["limits"],
                         "D1", ["Q2", "Q3"])
    for record in rows(RESULTS / "repo-now.jsonl"):
        if record.get("sha") and record.get("http") == 200:
            confirmed = "; ".join(hit["confirmed"] for hit in record["hits"][:3])
            fields = ", ".join(dict.fromkeys(hit["field"] for hit in record["hits"]))
            yield source("R-" + record["repo"], record["url"], record["checked_at"], "공식 저장소 본문·구조",
                         record["repo"], record["sha"], f"repo header, README and fields: {fields}",
                         f'archived={record["archived"]}. {confirmed or "기본 브랜치와 저장소 루트 경로를 관측했다."}',
                         "문서 및 저장소 표면에 한정된다. 부재를 무너짐으로 자동 판정하지 않는다.",
                         "D3-fetch", ["Q2", "Q4"])
    for r in reasons:
        for proof in (r.get("then_evidence") or {}, (r.get("then_evidence") or {}).get("supporting_git", {})):
            if proof.get("source_id"):
                pinned = fixed.get(proof["source_id"], {})
                version = proof.get("commit") or proof["historical_date"]
                if pinned.get("sha256_text"):
                    version += "#sha256=" + pinned["sha256_text"]
                yield source(proof["source_id"], proof["url"], proof["checked_at_utc"],
                             "이전 판 코드·문서" if proof["level"] == "D2" else "날짜 있는 출시·변경 기록",
                             f'{r["candidate"]} — {proof["source_id"]}', version, proof["location"], proof["finding"],
                             "특정 시점·파일 또는 제품 범위다. 릴리스와 커밋 날짜를 구분하고 배포·계정 동작은 별도로 확인한다.",
                             proof["level"], ["Q3", "Q4"])
    for r in rows(RESULTS / "registry.jsonl"):
        if r.get("http") == 200 and r.get("version"):
            yield source("N-" + r["package"], r["url"], r["checked_at"], "npm 공식 메타데이터", r["package"],
                         r["version"], "version, deprecated, license", f'deprecated={r["deprecated"]}, license={r["license"]}',
                         "패키지 단위 신호다. 같은 제품의 다른 아티팩트에는 적용하지 않았다.", "D3-fetch", ["Q4"])
    for r in rows(RESULTS / "repo-signals.jsonl"):
        for key in ("commit", "release"):
            obs = r.get(f"{key}_observation") or {}
            if obs.get("http") != 200:
                continue
            if key == "commit":
                value = (r.get("commit") or {}).get("committedDate")
            else:
                value = ", ".join(x["publishedAt"] for x in r.get("release_candidates", []) if x.get("publishedAt"))
            yield source(f'S-{key}-{r["repo"]}', obs["url"], obs["checked_at"], "GitHub 공식 이력",
                         f'{r["repo"]} {key}', "live", f"{key} entries", f'선택한 이력의 공개 시간 {value or "없음"}.',
                         "기본 브랜치와 표시된 릴리스만. 접근이 가능해도 날짜가 파싱되지 않으면 신호는 미확인이다.",
                         "D3-fetch", ["Q4"])
    for i, record in enumerate(rows(RESULTS / "license-observations.jsonl"), 1):
        for key, field in (("old", "old_request"), ("new", "new_request")):
            obs = record.get(field) or {}
            if obs.get("http") != 200:
                continue
            yield source(f"S-license-{i}-{key}", obs["url"], obs["checked_at"], "Git 고정 라이선스 파일 후보",
                         f'{record["repo"]} {key}', obs["url"].split("/")[5], "파일 전문의 해시와 헤더·단서",
                         record["interpretation"],
                         "파일 후보가 법적 적용 범위 전체를 대표하지 않는다. 라이선스 분류가 없으면 신호를 채우지 않았다.",
                         "D2", ["Q4"])


def excluded_sources(web, fixed, included):
    for record in {**web, **fixed}.values():
        key = record["id"]
        if key in included:
            continue
        no_content = not (record.get("viewable") or record.get("line"))
        if key in {"M-SCORE", "S-SCORE", "S-RDAP"} or no_content:
            detail = "호스트 차단·응답 실패 또는 본문 단서 미확보"
        else:
            detail = "검색·초록·중복 후보 또는 최종 판정에 쓰지 않은 관측. 최소 문헌 수에서 제외."
        yield source(key, record["url"], record.get("checked_at_utc") or record.get("checked_at"),
                     "열람·검토 후보", record.get("title") or key, "live",
                     ", ".join(record.get("lines_read", [])) or "정확한 행 위치 없음",
                     "판정·문헌 수에 미산입", detail, "D0" if key.startswith("M-") else "D3-fetch", [])
    for record in json.loads((RESULTS / "access.json").read_text())["requests"]:
        key = "PROBE-" + record["host"]
        yield source(key, record["url"], record["checked_at_utc"], "초기 익명 접근 시험",
                     record["host"], "live", "HTTPS GET", record["outcome"],
                     "원격 한도·수치·스냅샷은 관측되지 않았다.", "D3-run", ["Q3", "Q4"])


def main():
    web = {}
    for name in ("web-methods", "web-current", "web-history"):
        web.update({x["id"]: x for x in rows(RESULTS / f"{name}.jsonl")})
    fixed = {x["id"]: x for x in rows(RESULTS / "fixed-evidence.jsonl")}
    reasons = list(rows(ROOT / "REASONS.jsonl"))
    methods = method_sources(web, fixed)
    execution = {entry["id"]: entry for entry in execution_sources(reasons, fixed, web)}
    excluded = list(excluded_sources(web, fixed, set(methods) | set(execution)))
    categories = Counter(r["category"] for r in methods.values() if r["counts_toward_minimum"])
    out = {"summary": {"methods_reviewed": len(methods), "methods_counted": sum(categories.values()),
                       "counted_by_category": categories, "execution_distinct_source_ids": len(execution),
                       "execution_distinct_urls": len({r["url"] for r in execution.values()}),
                       "excluded": len(excluded), "site_cap": 3,
                       "day_precision": "공개 스레드 및 고정 입력 열람 시각은 UTC 날짜 정밀도."},
           "methods": list(methods.values()), "execution": list(execution.values()), "excluded": excluded}
    (ROOT / "sources.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
