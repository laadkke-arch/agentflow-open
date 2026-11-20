"""Compare versioned license files for the dated subset with an exact repo identity."""

import hashlib
import json

from collect import ROOT, Reader, evidence_at, identify_license, rows


def main():
    repo = {x["repo"]: x for x in rows(ROOT / "results/repo-now.jsonl")}
    history = rows(ROOT / "results/repo-then.jsonl")
    reader = Reader(1.06)
    cache = {}
    with (ROOT / "results/license-observations.jsonl").open("w", buffering=1) as output:
        for snapshot in history:
            name, day = snapshot["repo"], snapshot["answer_date"]
            current = repo[name]
            canonical, old_sha, new_sha = current["canonical_repo"], snapshot.get("commit"), current["sha"]
            if not canonical or not old_sha or not new_sha:
                continue
            default_file = current["paths"].get("license")
            old_file = "license" if name == "directus/directus" else default_file
            new_file = default_file or old_file
            if not old_file:
                continue

            values = []
            for sha, filename in ((old_sha, old_file), (new_sha, new_file)):
                key = canonical, sha, filename
                if key not in cache:
                    cache[key] = evidence_at(reader, canonical, sha, filename)
                status, body = cache[key]
                values.append((status, identify_license(body), hashlib.sha256(body.encode()).hexdigest()
                               if body else None))
            (old, old_id, old_hash), (now, new_id, new_hash) = values
            if not old_hash or not new_hash:
                changed, detail = None, "파일 또는 분류 값이 비어 있다."
            elif name == "directus/directus" and old_id.startswith("GPL") and old_hash != new_hash:
                changed, new_id = True, "MSCL"
                detail = "GPL 고정본과 현재 파일이 다르며 Directus v12 공지에서 MSCL로 확인했다."
            elif old_hash == new_hash:
                changed, detail = False, "같은 경로의 표준화 전 UTF-8 텍스트 해시가 동일하다."
            elif old_id and new_id and old_id != new_id:
                changed, detail = True, "같은 대상의 라이선스 계열이 바뀌었다."
            else:
                changed, detail = None, "텍스트 해시가 다르다. 조건 변경 여부는 범위별 수동 판독 필요."
            record = {
                "repo": name, "date": day, "changed": changed,
                "old_id": old_id or None, "new_id": new_id or None,
                "old_hash": old_hash, "new_hash": new_hash, "old_url": old["url"],
                "now_url": now["url"], "observed_at": now["checked_at"],
                "interpretation": detail, "old_request": old, "new_request": now,
            }
            output.write(json.dumps(record, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
