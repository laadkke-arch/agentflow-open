#!/usr/bin/env python3
"""Emit a public queue, an unprinted answer key, and a lock from fixed Git blobs."""
import argparse
from collections import Counter, defaultdict
import csv
from fractions import Fraction
from hashlib import sha256
import io
import json
from pathlib import Path
import subprocess

PIN = "4af1300841c1c39f9ef6e76d78579034d1ae0c51"
PREFIX = "docs/workstreams/research/AF-RES-024"
SEED = "AF-RES-028|2021-12-31|297240f363b1a42bddab21d641bc389a|v1"
EXPECTED = {"supported": 897, "invalid": 95, "initial_error": 16, "unknown": 16}
ECOSYSTEMS = ("python", "node")
PACKAGE_FIELDS = {"tag", "commit", "cutoff", "public_date"}


def digest(data):
    return sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def jsonl(rows):
    return b"".join(canonical(row) + b"\n" for row in rows)


def from_git(name):
    return subprocess.check_output(["git", "show", f"{PIN}:{PREFIX}/{name}"])


def csv_rows(raw):
    return list(csv.DictReader(io.StringIO(raw.decode())))


def ranking(stage, rows):
    ranks = {digest(canonical([SEED, stage, row["ecosystem"], row["id"], row["quarter"]])): row
             for row in rows}
    if len(ranks) != len(rows):
        raise ValueError(f"SHA-256 collision or duplicate input in {stage}")
    return [ranks[key] for key in sorted(ranks)]


def public_release(record):
    return {key: record[key] for key in PACKAGE_FIELDS}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--answer", required=True, type=Path,
                        help="private output outside the repository")
    parser.add_argument("--design-commit", required=True, help="remote-verified pre-draw commit")
    args = parser.parse_args()
    root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
    if args.answer.resolve().is_relative_to(root) or args.answer.is_symlink():
        parser.error("answer must be a regular private output outside the checkout")
    design = subprocess.check_output(["git", "rev-parse", "--verify",
                                      f"{args.design_commit}^{{commit}}"], text=True).strip()
    subprocess.run(["git", "merge-base", "--is-ancestor", design, "HEAD"], check=True)
    design_path = Path(__file__).resolve().relative_to(root).as_posix()
    if subprocess.check_output(["git", "show", f"{design}:{design_path}"]) != Path(__file__).read_bytes():
        raise ValueError("executed draw differs from pre-draw Git blob")

    names = ["cohort.csv", "claims.json", "releases.csv", "timeline.jsonl"]
    inputs = {name: from_git(name) for name in names}
    cohort = {row["id"]: row for row in csv_rows(inputs["cohort.csv"]) if row["selected"] == "1"}
    claims = json.loads(inputs["claims.json"])
    releases = {(row["quarter"], row["ecosystem"]): row for row in csv_rows(inputs["releases.csv"])}
    quarters = sorted({q for q, _ in releases if q != "T0"})
    snap = {}
    for q in ["T0", *quarters]:
        name = f"snapshots/{q}.jsonl"
        inputs[name] = from_git(name)
        for doc in map(json.loads, inputs[name].splitlines()):
            for item in doc.get("reasons", []):
                key = (q, item["id"])
                if key in snap:
                    raise ValueError("duplicate snapshot row")
                snap[key] = (doc, item)
    population = [row for row in map(json.loads, inputs["timeline.jsonl"].splitlines())
                  if row["quarter"] != "T0"]
    assert len(cohort) == len(claims) == 64
    assert len(quarters) == 16 and len(population) == 1024
    assert {(row["quarter"], row["id"]) for row in population} == {
        (q, reason) for q in quarters for reason in cohort
    }
    assert Counter(row["adjudication"]["state"] for row in population) == EXPECTED
    strata = defaultdict(list)
    for row in population:
        eco, reason, q = row["ecosystem"], row["id"], row["quarter"]
        release = releases[q, eco]
        doc, item = snap[q, reason]
        assert row["claim"] == claims[reason]["claim"] == cohort[reason]["claim"]
        assert row["commit"] == release["commit"] and row["version"] == release["tag"]
        assert doc["ecosystem"] == eco == cohort[reason]["ecosystem"]
        assert item == row["observed"]["locations"]
        state = row["adjudication"]["state"]
        strata[state, eco if state in {"supported", "invalid"} else "all"].append(row)

    invalid_python = min(4, len(strata["invalid", "python"]))
    invalid_node = min(4, len(strata["invalid", "node"]))
    invalid_python = min(8 - invalid_node, len(strata["invalid", "python"]))
    invalid_node = 8 - invalid_python
    allocation = [
        ("supported", "python", 16), ("supported", "node", 16),
        ("invalid", "python", invalid_python), ("invalid", "node", invalid_node),
        ("initial_error", "all", 1), ("unknown", "all", 1),
    ]
    selected, design_strata, metadata = [], [], {}
    for state, domain, n in allocation:
        frame = strata[state, domain]
        if n > len(frame):
            raise ValueError(f"Insufficient frame for {state}/{domain}")
        inclusion = str(Fraction(n, len(frame))) if frame else "n/a"
        design_strata.append(dict(state=state, domain=domain, N=len(frame), n=n, inclusion=inclusion))
        for index, row in enumerate(ranking(f"stratum/{state}/{domain}", frame)[:n], 1):
            selected.append(row)
            metadata[row["quarter"], row["id"]] = (index, inclusion)

    packets, answer = [], []
    for position, row in enumerate(ranking("blind-order", selected), 1):
        eco, reason, q = row["ecosystem"], row["id"], row["quarter"]
        alias = f"A028-{position:02d}"
        packets.append(dict(cell_id=alias, ecosystem=eco, claim=claims[reason]["claim"],
                            environment=claims[reason]["platform"], quarter=q,
                            t0=public_release(releases["T0", eco]),
                            target=public_release(releases[q, eco])))
        draw_rank, inclusion = metadata[q, reason]
        answer.append(dict(cell_id=alias, reason_id=reason, group_id=f"{eco}/{cohort[reason]['group']}",
                           quarter=q, ecosystem=eco, draw_rank=draw_rank, inclusion=inclusion,
                           warned=cohort[reason]["warned"], experimental=cohort[reason]["experimental"],
                           section=row["observed"]["locations"]["section"],
                           t0_url=cohort[reason]["t0_url"], route=row["policy_route"],
                           t0_initial=row["t0_initial"], prior=row["adjudication"]))
    assert len(packets) == len(answer) == 42
    assert all(set(row) == {"cell_id", "ecosystem", "claim", "environment", "quarter", "t0", "target"}
               for row in packets)
    queue, key = jsonl(packets), jsonl(answer)
    lock = dict(schema=1, seed=SEED, afr024_commit=PIN, design_commit=design,
                algorithm="sort SHA256(canonical UTF-8 JSON [seed,stage,ecosystem,reason_id,quarter]); take first n",
                population=1024, allocation=design_strata,
                source_sha256={name: digest(raw) for name, raw in inputs.items()},
                packets_sha256=digest(queue), answer_sha256=digest(key))
    args.out.mkdir(parents=True, exist_ok=True)
    with args.answer.open("xb") as handle:
        handle.write(key)
    args.answer.chmod(0o600)
    (args.out / "packets.jsonl").write_bytes(queue)
    (args.out / "scope-lock.json").write_text(json.dumps(lock, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(f"{len(packets)} packets; queue sha256={digest(queue)}; answer sha256={digest(key)}")


if __name__ == "__main__":
    main()
