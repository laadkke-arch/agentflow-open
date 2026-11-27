"""laadkke-arch/opensource의 judge/ 판정 답(원문을 연 모델 판정)을 읽기만 해서 고정한다(08 I45).

그 저장소의 글은 자료이지 지시가 아니다. 출처는 커밋 SHA로 남긴다.
남기는 칸: 파일, 세션, 지시문, 판정자 표시(judge=·by=), n, request, url, grade, opened, evidence 길이.
evidence(원문 인용)와 note(판정 이유)는 옮기지 않는다. 원문 사본을 이 저장소에 두지 않기 위해서다(captures README).
실행: python3 -I ledger/tools/snapshot_judge.py /path/to/opensource-clone [커밋]
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "fixtures" / "judge-orig"
COLS = ("file", "session", "prompt", "judge", "by", "n", "request", "url", "grade", "opened", "evidence_len")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=True).stdout


def parse(text: str, fname: str) -> list[dict]:
    rows, head, cols = [], None, None
    for line in text.splitlines():
        if line.startswith("@@judge"):
            head = dict(kv.split("=", 1) for kv in line.split()[1:] if "=" in kv)
            cols = None
        elif line.startswith("@@end"):
            head = None
        elif head is not None and cols is None:
            cols = line.split("\t")
        elif head is not None and line.strip():
            v = dict(zip(cols, line.split("\t")))
            rows.append({"file": fname, "session": head.get("session", ""), "prompt": head.get("prompt", ""),
                         "judge": head.get("judge", ""), "by": head.get("by", ""), "n": v["n"], "request": v["request"],
                         "url": v["url"], "grade": v["grade"], "opened": v.get("opened", ""),
                         "evidence_len": str(len(v.get("evidence", "")))})
    return rows


def main(repo, ref="origin/claude/project-thread-a3oi3x"):
    sha = git(repo, "rev-parse", ref).strip()
    files = [f for f in git(repo, "ls-tree", "--name-only", sha, "judge/").split() if f.endswith(".txt")]
    rows = [r for f in files for r in parse(git(repo, "show", f"{sha}:{f}"), f.split("/")[-1])]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "judgments.tsv").write_text("\t".join(COLS) + "\n" + "".join(
        "\t".join(r[c] for c in COLS) + "\n" for r in rows), encoding="utf-8")
    (OUT / "SOURCES.json").write_text(json.dumps({
        "repo": "laadkke-arch/opensource", "commit": sha,
        "committed_at": git(repo, "show", "-s", "--format=%cI", sha).strip(), "files": files,
        "link": f"https://github.com/laadkke-arch/opensource/tree/{sha}/judge", "rows": len(rows),
        "note": "읽기만 한 자료. 원문을 직접 연 모델 판정(dot D)이고 사람 판정이 아니다. evidence·note는 옮기지 않았다."},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(len(rows), sha, files)


if __name__ == "__main__":
    main(*sys.argv[1:])
