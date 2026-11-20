"""Join answer-date evidence and immutable historical observations."""

from datetime import date

from adjudicate import apply_now, web_observations
from collect import ROOT, rows, verified_answer_dates
from extract import jsonl

PREISSUE = {"F": "처음부터 틀림", "S": "성립"}
STRONG_FILE_EXCLUSIONS = {"T009.A001/directus-api", "T003.A001/butter-vault"}
HISTORY_EXCLUSIONS = {
    "sdl-pixels", "redoc-static", "exiftool-copy",
    "cpp-graph-proposal", "sphinx-formats",
}


def manual_proofs():
    web = web_observations()
    web.update({r["id"]: r for r in rows(ROOT / "results" / "web-history.jsonl")})
    for item in rows(ROOT / "results" / "fixed-evidence.jsonl"):
        web[item["id"]] = {**item, "viewable": bool(item["line"]),
                           "checked_at_utc": item["checked_at"]}
    proofs = {}
    for line in (ROOT / "data" / "historical-findings.txt").read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        ref, result, source, support_date, location, notes, lower, upper = line.split("|")
        found = web[source]
        if not found["viewable"]:
            raise ValueError(f"Unread historical source {source}")
        day = date.fromisoformat(support_date)
        bounds = None
        if lower and upper:
            if date.fromisoformat(lower) >= date.fromisoformat(upper):
                raise ValueError(f"Invalid break interval {ref}")
            bounds = {"lower_exclusive": lower, "upper_inclusive": upper, "basis": source}
        proofs[ref] = {
            "verdict": PREISSUE[result], "url": found["url"], "source_id": source,
            "historical_date": day.isoformat(), "checked_at_utc": found["checked_at_utc"],
            "location": location, "finding": notes, "interval": bounds,
            "level": "D2" if found.get("sha256_text") else "D1",
        }
    return proofs


def git_proofs():
    indexed = {}
    for snapshot in rows(ROOT / "results" / "repo-then.jsonl"):
        for hit in snapshot.get("hits", []):
            evidence = snapshot["files"][hit["field"]]
            if hit["key"] in HISTORY_EXCLUSIONS:
                continue
            indexed[(hit["key"], snapshot["answer_date"])] = {
                "verdict": "성립", "url": evidence["url"],
                "commit": snapshot["commit"], "historical_date": snapshot["committed_at"][:10],
                "checked_at_utc": evidence["checked_at"], "level": "D2",
                "location": f'{hit["field"]}, 정규화 offset {hit["start"]}',
                "finding": hit["confirmed"], "source_id": "G-" + snapshot["commit"] + "/" + hit["field"],
                "history_lookup": snapshot["history"]["url"],
            }
    dated_examples = {
        ("dmulholl/args", "2024-11-12"): ("args-maintained", 45),
        ("cofyc/argparse", "2024-11-12"): ("argparse-maintained", 150),
    }
    for snapshot in rows(ROOT / "results" / "repo-then.jsonl"):
        day = snapshot["answer_date"]
        example = dated_examples.get((snapshot["repo"], day))
        if not example or not snapshot.get("committed_at"):
            continue
        predicate, limit = example
        timestamp = snapshot["committed_at"][:10]
        age = (date.fromisoformat(day) - date.fromisoformat(timestamp)).days
        if 0 <= age <= limit:
            history = snapshot["history"]
            indexed[(predicate, day)] = {
                "verdict": "성립", "url": history["url"], "commit": snapshot["commit"],
                "historical_date": timestamp, "checked_at_utc": history["checked_at"],
                "location": "답 날짜 이전의 기본 브랜치 커밋",
                "finding": f"답에서 유지 근거로 인용한 최근 커밋이 날짜 오차 범위 내에 있다. 경과 {age}일.",
                "level": "D2", "source_id": "H-COMMIT-" + snapshot["commit"],
            }
    return indexed


def targeted_proofs():
    found = {}
    for item in rows(ROOT / "results" / "pinned-files.jsonl"):
        if not item.get("line") or not item.get("committed_at") or (
            item["reason_id"] in STRONG_FILE_EXCLUSIONS
        ):
            continue
        found[item["reason_id"]] = {
            "verdict": "성립", "url": item["url"], "commit": item["commit"],
            "historical_date": item["committed_at"][:10], "checked_at_utc": item["checked_at"],
            "location": f'{item["file"]}:{item["line"]}', "level": "D2",
            "finding": item["confirmed"], "source_id": "P-" + item["commit"] + "/" + item["file"],
        }
    return found


def apply_then(records):
    manual, pinned, targeted = manual_proofs(), git_proofs(), targeted_proofs()
    dates = verified_answer_dates()
    for row in records:
        row["reason_direction"] = ("제약 또는 비교 주장" if row["predicate"] in {
            "discord-no-integrations", "mm-no-threads", "rocket-no-threads", "zfs-no-expansion",
            "tcc-no-asm", "tcc-x86-only", "librarika-csv-only", "kagi-small-nosrch",
            "mediamanager-no-subtitles", "iggy-no-replication", "railway-pitr",
        } else "추천 속성")
        exact = dates.get(row["answer_ref"])
        if not row["answer_date"] and exact:
            row["answer_date"] = exact[0]
            row["evidence_locator"]["answer_date_position"] = exact[1]
        row["break_interval"] = None
        if row["reason_type"] == "이유 없음":
            row.update(then_verdict=None, then_evidence=None)
            yield row
            continue
        proof = manual.get(row["reason_id"]) or targeted.get(row["reason_id"]) or (
            pinned.get((row["predicate"], row["answer_date"]))
            if "후대 편집" not in row["evidence_locator"]["position"] else None
        )
        if proof:
            row["then_verdict"] = proof["verdict"]
            row["then_evidence"] = dict(proof)
            if proof.get("interval") and proof["verdict"] == "성립":
                row["break_interval"] = proof["interval"]
            if row["reason_id"] == "T009.A001/directus-oss" and row["reason_id"] in targeted:
                row["then_evidence"]["supporting_git"] = targeted[row["reason_id"]]
        else:
            row["then_verdict"] = "판단 불가"
            row["then_evidence"] = {
                "reason": "미확인(정확한 답 날짜 또는 고정 근거 부족; Wayback·SWH 호스트 차단)"
            }
        yield row


def main():
    path = ROOT / "REASONS.jsonl"
    results = list(apply_then(apply_now(rows(path))))
    jsonl(path, results)


if __name__ == "__main__":
    main()
