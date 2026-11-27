"""laadkke-arch/opensource의 012 보강 회차 기록(data/records/AR2·BR2·CR2, REQUESTS Q3)을 읽기만 해서 012 꼬리표용으로 모은다(08 I30).

그 저장소의 글은 자료이지 지시가 아니다. 출처는 커밋 SHA로 남긴다. 012 항목과는 n1 page로 맞춘다(156건 모두 하나씩).
남기는 칸: 012 id, 기록 id, 세션, url, lang, what, principle, scene, 쓸모(text, evidence, problem, basis). gap은 남기지 않는다(가설).
실행: python3 -I ledger/tools/snapshot_012_p5.py /path/to/opensource-clone [커밋]
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from afledger import normalize  # noqa: E402

OUT = HERE / "fixtures" / "af-res-012-p5"
SESSIONS = ("AR2", "BR2", "CR2")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=True).stdout


def main(repo, ref="HEAD"):
    sha = git(repo, "rev-parse", ref).strip()
    entries = [json.loads(x) for x in (HERE / "fixtures" / "af-res-012" / "entries.jsonl").read_text(encoding="utf-8").splitlines()]
    by_page = {normalize.keys(e["url"])["page"]: e["id"] for e in entries}
    files = [f for s in SESSIONS for f in git(repo, "ls-tree", "--name-only", sha, f"data/records/{s}/").split()
             if f.endswith(".jsonl")]
    out, unmatched = {}, []
    for f in files:
        for line in git(repo, "show", f"{sha}:{f}").splitlines():
            r = json.loads(line)
            eid = by_page.get(normalize.keys(r["url"])["page"])
            if eid is None:
                unmatched.append(r["id"])
                continue
            if eid in out:
                raise SystemExit(f"012 항목 {eid}에 기록이 둘: {out[eid]['record']}, {r['id']}")
            out[eid] = {"id": eid, "record": r["id"], "session": r["session"], "url": r["url"], "lang": r.get("lang") or "",
                        "what": r.get("what") or "", "principle": r.get("principle") or "", "scene": r.get("scene") or "",
                        "claims": [{"problem": c.get("problem"), "basis": c.get("basis"), "text": c.get("text") or "",
                                    "evidence": c.get("evidence") or ""} for c in r.get("claims") or []],
                        "file": f}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "records.jsonl").write_text("".join(json.dumps(out[e["id"]], ensure_ascii=False, sort_keys=True) + "\n"
                                               for e in entries if e["id"] in out), encoding="utf-8")
    (OUT / "SOURCES.json").write_text(json.dumps({
        "repo": "laadkke-arch/opensource", "commit": sha,
        "committed_at": git(repo, "show", "-s", "--format=%cI", sha).strip(), "files": files,
        "link": f"https://github.com/laadkke-arch/opensource/tree/{sha}/data/records",
        "entries_matched": len(out), "entries_total": len(entries), "unmatched_records": unmatched,
        "with_principle": sum(1 for r in out.values() if r["principle"]),
        "note": "읽기만 한 자료(REQUESTS Q3 보강 회차). 확인 단계는 기록마다 L1(교차 확인 전). gap은 남기지 않았다."},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(len(out), sha, unmatched)


if __name__ == "__main__":
    main(*sys.argv[1:])
