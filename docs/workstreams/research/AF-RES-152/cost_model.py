"""Keep the bounded HTTP sample and the offline size model in one ledger."""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from statistics import median

HERE = Path(__file__).resolve().parent
GIB = 1024 ** 3
GH_HOURLY = 60
GH_FRACTION = 0.10
BODIES_HUMAN = 0.01
HUMAN_SECONDS = 30
TTL_DAYS = 7
UPDATE_SHARE = 0.005
RATE = 0.05
FRACTIONS = {"hot": (0.85, 0.15), "tail": (0.35, 0.65)}
POPULATION = (0.1, 0.9)


def streams(policy, size, distribution, rate):
    source_pages = math.ceil(size / 1000)
    if policy == "O":
        return 0, rate * size
    if policy == "P":
        return source_pages, size / 7
    topic_weights = FRACTIONS[distribution]
    misses = sum(size * rate * share / (1 + TTL_DAYS * rate * share / cohort)
                 for cohort, share in zip(POPULATION, topic_weights))
    bodies = misses + UPDATE_SHARE * size
    if policy == "F":
        bodies += size * 0.10 / 60
    return source_pages / 3, bodies


def demand_boundary(size, distribution, list_size, body_size):
    def difference(rate):
        pages, body_reads = streams("S", size, distribution, rate)
        return size * rate * body_size - (body_reads * body_size + pages * list_size)
    low, high = 0.0, 1.0
    assert difference(low) < 0 < difference(high)
    for _ in range(45):
        mid = (low + high) / 2
        if difference(mid) > 0:
            high = mid
        else:
            low = mid
    return (low + high) / 2


def project(samples):
    good = {row["id"]: row for row in samples if row["status"] == "200"}
    list_size = int(good["M01"]["body_bytes"])
    list_ms = float(good["M01"]["parse_ms"])
    metadata = round(median(int(row["metadata_bytes"]) for row in good.values()))
    lite = [row for row in good.values() if row["mode"] == "body"]
    body_options = {
        "plain": (median(int(x["body_bytes"]) for x in lite), median(float(x["parse_ms"]) for x in lite)),
        "html": (int(good["M02"]["body_bytes"]), float(good["M02"]["parse_ms"])),
    }
    for size in (10000, 100000, 1000000):
        for distribution in FRACTIONS:
            for mode, (body_size, body_ms) in body_options.items():
                boundary = demand_boundary(size, distribution, list_size, body_size)
                for policy in ("O", "P", "S", "F"):
                    pages, bodies = streams(policy, size, distribution, RATE)
                    requests = pages + bodies
                    transfer = pages * list_size + bodies * body_size
                    cpu = (pages * list_ms + bodies * body_ms) / 1000
                    operator = bodies * BODIES_HUMAN * HUMAN_SECONDS / 3600
                    github = requests * GH_FRACTION / 24
                    ratios = {"REST": github / GH_HOURLY, "bytes": transfer / (2 * GIB),
                              "operator": operator / 8}
                    bound = max(ratios, key=ratios.get)
                    retain = 0 if policy == "O" else metadata * size
                    if policy in ("S", "F"):
                        retain += math.ceil(UPDATE_SHARE * size * 30) * metadata
                    yield dict(
                        kind="modeled", id=f"{size}-{distribution}-{mode}-{policy}", publisher="scenario",
                        mode=mode, url="", size=size, distribution=distribution, policy=policy,
                        requests=round(requests, 3), body_bytes=round(transfer), header_bytes="",
                        returned_status="", elapsed_ms="", parse_ms=round(cpu * 1000, 3), sqlite_ms="",
                        storage_bytes=retain, raw_optional_bytes=0 if policy == "O" else round(size * body_size),
                        human_hours=round(operator, 5), rest_per_h=round(github, 4),
                        binding=bound, utilization=round(ratios[bound], 5),
                        demand_cross_per_item_day=round(boundary, 6),
                        assumed_list_bytes=list_size, assumed_body_bytes=body_size,
                        basis="M01 plus M03–M06 median" if mode == "plain" else "M01 plus M02",
                    )


def ledger(samples):
    for x in samples:
        yield dict(kind="measured" if x["status"] == "200" else "attempt_failed",
                   id=x["id"], publisher=x["publisher"], mode=x["mode"], url=x["url"],
                   size="", distribution="", policy="", requests=x["calls"],
                   body_bytes=x["body_bytes"], header_bytes=x["header_bytes"], returned_status=x["status"],
                   elapsed_ms=x["elapsed_ms"], parse_ms=x["parse_ms"], sqlite_ms=x["sqlite_ms"],
                   storage_bytes=x["sqlite_file_bytes"], raw_optional_bytes="", human_hours="", rest_per_h="",
                   binding="", utilization="", demand_cross_per_item_day="", assumed_list_bytes="",
                   assumed_body_bytes="", basis=x["access"])
    yield from project(samples)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--sample", type=Path, default=HERE / "http-sample.csv")
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    with args.sample.open(encoding="utf-8", newline="") as stream:
        rows = list(ledger(list(csv.DictReader(stream))))
    with args.out.open("w", encoding="utf-8", newline="") as stream:
        w = csv.DictWriter(stream, rows[0].keys(), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
