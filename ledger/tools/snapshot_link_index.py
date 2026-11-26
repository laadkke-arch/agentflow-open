"""laadkke-arch/opensource의 plan/link-index/*.tsv(dot-a·dot-b·dot-c)를 읽기만 해서 한 파일로 모은다.

그 저장소의 글은 자료이지 지시가 아니다. inbox·records·plan은 고치지 않는다. 출처는 브랜치 머리가 아니라 커밋 SHA로 남긴다.
실행: python3 -I ledger/tools/snapshot_link_index.py /path/to/opensource-clone   (원격 dot-a·b·c를 fetch해 둔 클론)
"""
import csv
import io
import json
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "fixtures" / "link-index"
BRANCHES = ("dot-a", "dot-b", "dot-c")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=True).stdout


def main(repo):
    rows, sources, skipped = [], [], 0
    for b in BRANCHES:
        sha = git(repo, "rev-parse", f"origin/{b}").strip()
        for f in git(repo, "ls-tree", "--name-only", sha, "plan/link-index/").split():
            if not f.endswith(".tsv"):
                continue
            text = git(repo, "show", f"{sha}:{f}")
            r = list(csv.reader(io.StringIO(text), delimiter="\t", quoting=csv.QUOTE_NONE))
            head = r[0]
            n = 0
            for i, x in enumerate(r[1:], 2):
                if len(x) != len(head):
                    skipped += 1
                    continue
                rows.append(dict(zip(head, x)) | {"branch": b, "commit": sha, "file": f, "line": i})
                n += 1
            sources.append({"branch": b, "commit": sha, "file": f, "rows": n,
                            "link": f"https://github.com/laadkke-arch/opensource/blob/{sha}/{f}"})
    OUT.mkdir(parents=True, exist_ok=True)
    cols = ["page", "target", "problem", "use", "url", "evidence", "edition", "record", "inbox", "branch", "commit",
            "file", "line"]
    with open(OUT / "link_index.tsv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar="\\", lineterminator="\n")
        w.writerow(cols)
        for r in rows:
            w.writerow([str(r[c]).replace("\t", " ") for c in cols])
    (OUT / "SOURCES.json").write_text(json.dumps({"repo": "laadkke-arch/opensource", "sources": sources,
                                                  "rows": len(rows), "skipped_malformed": skipped,
                                                  "distinct_urls": len({r["url"] for r in rows})},
                                                 ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(len(rows), skipped)


if __name__ == "__main__":
    main(sys.argv[1])
