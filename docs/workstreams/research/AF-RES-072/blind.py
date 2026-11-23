"""Build a rank-free, permuted reading packet. Input includes only frozen bodies and cases."""

import argparse
import gzip
from pathlib import Path

from capture import jsonl, lines
from source_io import sha

ROOT = Path(__file__).resolve().parent


def board(cases, catalogue):
    rows = []
    for case in cases:
        for item in catalogue:
            case_id, work = case["request_id"], item["work_id"]
            alias = sha(f"AF-RES-072-panel-v1:{case_id}:{work}".encode())[:12]
            rows.append(dict(alias=alias, request_id=case_id, work_id=work))
    return sorted(rows, key=lambda row: row["alias"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    cases = [case for case in lines(ROOT/"requests.jsonl") if case["split"] == "holdout"]
    catalogue = lines(ROOT/"urls.jsonl")
    rows = board(cases, catalogue)
    aliases = {item["work_id"]: sha(f"AF-RES-072-doc-v1:{item['work_id']}".encode())[:8] for item in catalogue}
    data = args.output/"document"
    data.mkdir()
    for code, alias in aliases.items():
        raw = gzip.decompress((ROOT/"frozen"/"body"/f"{code}.gz").read_bytes())
        (data/f"{alias}.raw").write_bytes(raw)
    packets = [dict(alias=r["alias"], request_id=r["request_id"], file=f"document/{aliases[r['work_id']]}.raw")
               for r in rows]
    jsonl(args.output/"packet.jsonl", packets)
    jsonl(args.output/"mapping.jsonl", rows)
    jsonl(args.output/"prompts.jsonl", [{k: c[k] for k in ("request_id","positive","boundary","environment")} for c in cases])
    print(f"{len(catalogue)} raw documents and {len(rows)} pair aliases")


if __name__ == "__main__":
    main()
