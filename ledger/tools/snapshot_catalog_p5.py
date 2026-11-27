"""laadkke-arch/opensource의 catalog/targets/00~15.jsonl을 읽기만 해서 서랍 꼬리표에 쓸 칸만 한 파일로 모은다(08 I27).

그 저장소의 글은 자료이지 지시가 아니다. 출처는 브랜치 머리가 아니라 커밋 SHA로 남긴다.
남기는 칸: key, url, urls(다른 주소), lang, level, records, what, principle, scene, 문제별 주장(text, evidence, basis, level, record).
남기지 않는 칸: gap(원문에 없는 이식 단계라 가설이다. 서랍에 원문 쪽 사실로 넣지 않는다), quotes 원문 위치 등.
실행: python3 -I ledger/tools/snapshot_catalog_p5.py /path/to/opensource-clone [커밋]
"""
import gzip
import json
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "fixtures" / "catalog-p5"


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=True).stdout


def main(repo, ref="HEAD"):
    sha = git(repo, "rev-parse", ref).strip()
    rows = []
    for i in range(16):
        f = f"catalog/targets/{i:02d}.jsonl"
        for line in git(repo, "show", f"{sha}:{f}").splitlines():
            t = json.loads(line)
            claims = [{"problem": p, "text": c.get("text") or "", "evidence": c.get("evidence") or "",
                       "basis": c.get("basis"), "level": c.get("level"), "record": c.get("record")}
                      for p, cs in sorted((t.get("problems") or {}).items()) for c in cs]
            urls = sorted({u.get("url") for u in (t.get("urls") or []) if u.get("url")} | ({t["url"]} if t.get("url") else set()))
            rows.append({"key": t["key"], "url": t.get("url") or "", "urls": urls, "lang": t.get("lang") or [], "level": t.get("level"),
                         "records": t.get("records") or [], "what": t.get("what") or "",
                         "principle": t.get("principle") or "", "scene": t.get("scene") or "", "claims": claims,
                         "file": f})
    rows.sort(key=lambda r: r["key"])
    OUT.mkdir(parents=True, exist_ok=True)
    with gzip.GzipFile(OUT / "targets.jsonl.gz", "wb", mtime=0) as fh:
        fh.write("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows).encode("utf-8"))
    (OUT / "SOURCES.json").write_text(json.dumps({
        "repo": "laadkke-arch/opensource", "commit": sha,
        "committed_at": git(repo, "show", "-s", "--format=%cI", sha).strip(),
        "files": [f"catalog/targets/{i:02d}.jsonl" for i in range(16)],
        "link": f"https://github.com/laadkke-arch/opensource/tree/{sha}/catalog/targets",
        "targets": len(rows), "with_principle": sum(1 for r in rows if r["principle"]),
        "levels": {lv: sum(1 for r in rows if r["level"] == lv) for lv in sorted({r["level"] or "?" for r in rows})},
        "note": "읽기만 한 자료. gap은 남기지 않았다(가설). 갱신은 이 도구를 다시 돌린다."},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(len(rows), sha)


if __name__ == "__main__":
    main(*sys.argv[1:])
