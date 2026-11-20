"""Apply traceable analyst adjudications to the fixed reason rows."""

import argparse
from pathlib import Path

from collect import rows
from extract import ROOT, jsonl

VERDICTS = {"S": "성립", "W": "약화", "B": "무너짐", "U": "판단 불가"}


def web_observations():
    return {x["id"]: x for x in rows(ROOT / "results" / "web-current.jsonl")}


def web_findings():
    observations = web_observations()
    for line in (ROOT / "data" / "current-findings.txt").read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        source, title, where, finding, limit, assignments = line.split("|")
        observation = observations[source]
        if assignments and not observation["viewable"] and any(
            not a.endswith("=U") for a in assignments.split(",")
        ):
            raise ValueError(f"{source}: definitive current judgment without viewable body")
        yield {"id": source, "title": title, "sections_read": where,
               "confirmed": finding, "limits": limit,
               "url": observation["url"], "checked_at": observation["checked_at_utc"],
               "verdicts": dict(a.split("=") for a in assignments.split(",") if a),
               "viewable": observation["viewable"]}


def current_ledger():
    skip = {k for k in (ROOT / "data" / "skip-github-keys.txt").read_text().splitlines()
            if k and not k.startswith("#")}
    evidence = {}
    for record in rows(ROOT / "results" / "repo-now.jsonl"):
        for hit in record["hits"]:
            key = hit["key"]
            if key in skip:
                continue
            pointer = {
                "source_id": "R-" + record["repo"], "url": record["final_url"],
                "checked_at": record["checked_at"], "version": record["sha"],
                "position": f'{hit["field"]}, 정규화 본문 offset {hit["start"]}',
                "finding": hit["confirmed"], "verdict": "성립", "level": "D3-fetch",
                "limits": "공개 문서·코드 제공 여부 확인. 배포, 설치, 성능, 계정 실험은 별도.",
            }
            evidence[key] = pointer
    for note in web_findings():
        for key, code in note["verdicts"].items():
            evidence[key] = {
                "source_id": note["id"], "url": note["url"], "checked_at": note["checked_at"],
                "position": note["sections_read"], "finding": note["confirmed"],
                "verdict": VERDICTS[code], "level": "D1" if note["viewable"] else "D3-fetch",
                "limits": note["limits"],
            }
    return evidence


def apply_now(reasons):
    evidence = current_ledger()
    for row in reasons:
        proof = evidence.get(row["predicate"])
        reasonless = row["reason_type"] == "이유 없음"
        if reasonless:
            row.update(now_verdict=None, now_evidence_url=None, now_checked_at_utc=None,
                       now_detail="해당 없음(답의 근거 속성 미제시)")
        elif proof is None:
            row.update(now_verdict="판단 불가", now_evidence_url=None, now_checked_at_utc=None,
                       now_detail="미확인(해당 이유의 동일 범위 1차 근거 또는 실행 검증 필요)")
        else:
            row.update(now_verdict=proof["verdict"], now_evidence_url=proof["url"],
                       now_checked_at_utc=proof["checked_at"], now_detail=proof)
        yield row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("now",))
    args = parser.parse_args()
    path = ROOT / "REASONS.jsonl"
    updated = list(apply_now(rows(path)))
    jsonl(path, updated)


if __name__ == "__main__":
    main()
