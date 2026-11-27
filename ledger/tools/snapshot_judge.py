"""laadkke-arch/opensource의 judge/ 판정 답(원문을 연 모델 판정)을 읽기만 해서 고정한다(08 I45).

그 저장소의 글은 자료이지 지시가 아니다. 출처는 커밋 SHA로 남긴다.
남기는 칸: 파일, 세션, 지시문, 판정자 표시(judge=·by=), n, request, url, grade, opened, evidence 길이.
잇기(08 I48 규칙 1): j1·j2의 n은 I32 judgments.tsv의 n이라 n으로 (요청, 주소)를 잇는다. j3는 (요청, 주소)로 잇고
missing_for_b.tsv @ 027eeb04에 있는지 본다. 주소의 &amp;는 &로 되돌린다. 맞지 않는 줄은 버리고 수를 남긴다. grade "?"(열지 못함)는 그대로 둔다.
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


MISSING_REF = "027eeb04"   # J3 의뢰 목록의 기준 커밋(이 저장소)


def link(rows: list[dict]) -> tuple[list[dict], dict]:
    import csv
    i32 = {r["n"]: r for r in csv.DictReader(open(HERE / "fixtures" / "i32" / "judgments.tsv", encoding="utf-8"),
                                             delimiter="\t")}
    miss_txt = subprocess.run(["git", "-C", str(HERE), "show", f"{MISSING_REF}:ledger/fixtures/judge-orig/missing_for_b.tsv"],
                              capture_output=True, text=True).stdout
    miss = {(r["request"], r["url"]) for r in csv.DictReader(miss_txt.splitlines(), delimiter="\t")} if miss_txt else set()
    out, dropped = [], {"n_unknown": 0, "request_mismatch": 0, "url_mismatch": 0, "j3_not_in_missing": 0, "j4_not_unopened": 0,
                        "amp_fixed": 0}
    unopened = set()
    for r in rows:
        url = r["url"].replace("&amp;", "&")
        dropped["amp_fixed"] += url != r["url"]
        if r["prompt"] in ("j1", "j2"):
            t = i32.get(r["n"])
            if t is None:
                dropped["n_unknown"] += 1
                continue
            if t["request"] != r["request"]:
                dropped["request_mismatch"] += 1
                continue
            if t["url"] != url:
                dropped["url_mismatch"] += 1
                continue
            if r["grade"] == "?":
                unopened.add((r["request"], url))
        elif r["prompt"] == "j4":
            if (r["request"], url) not in unopened:     # 08 I51 규칙 1: 앞 고정에서 ?였던 쌍만
                dropped["j4_not_unopened"] += 1
                continue
        elif (r["request"], url) not in miss:
            dropped["j3_not_in_missing"] += 1
            continue
        if r["grade"] == "?" and r["prompt"] == "j3":
            unopened.add((r["request"], url))
        out.append(r | {"url": url})
    return out, dropped


def main(repo, ref="origin/claude/project-thread-a3oi3x"):
    sha = git(repo, "rev-parse", ref).strip()
    files = [f for f in git(repo, "ls-tree", "--name-only", sha, "judge/").split()
             if f.endswith(".txt") and f.split("/")[-1].startswith("J")]
    rows, dropped = link([r for f in files for r in parse(git(repo, "show", f"{sha}:{f}"), f.split("/")[-1])])
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "judgments.tsv").write_text("\t".join(COLS) + "\n" + "".join(
        "\t".join(r[c] for c in COLS) + "\n" for r in rows), encoding="utf-8")
    (OUT / "SOURCES.json").write_text(json.dumps({
        "repo": "laadkke-arch/opensource", "commit": sha,
        "committed_at": git(repo, "show", "-s", "--format=%cI", sha).strip(), "files": files,
        "link": f"https://github.com/laadkke-arch/opensource/tree/{sha}/judge", "rows": len(rows), "link_check": dropped,
        "unopened": sum(1 for r in rows if r["grade"] == "?"),
        "note": "읽기만 한 자료. 원문을 직접 연 모델 판정(dot D)이고 사람 판정이 아니다. evidence·note는 옮기지 않았다."},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(len(rows), sha, files, dropped)


if __name__ == "__main__":
    main(*sys.argv[1:])
