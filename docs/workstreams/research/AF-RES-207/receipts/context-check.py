"""Recompute the Rail and distinct-producer contrasts from the frozen observations."""
import argparse
import hashlib
import json
from pathlib import Path


def json_document(path):
    return json.loads(path.read_bytes())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cell(data, unit, geo):
    codes = dict(freq="A", unit=unit, tra_cov="INTL", geo=geo, time="2024")
    position = 0
    for dim, width in zip(data["id"], data["size"], strict=True):
        position = position * width + data["dimension"][dim]["category"]["index"][codes[dim]]
    index = str(position)
    present = index in data["value"] and data["value"][index] is not None
    return dict(dimension_key=[codes[dim] for dim in data["id"]], index=position,
                value=data["value"].get(index), value_present=present, status=data["status"].get(index))


def rail_contrast(capture, live=None):
    data = capture["published"]
    pkm = [cell(data, "MIO_PKM", country) for country in ("DK", "PT")]
    trips = [cell(data, "THS_PAS", country) for country in ("LT", "RO")]
    missing, zero = (cell(data, "MIO_PKM", geo) for geo in ("BE", "EE"))
    coverage = pkm + trips + [missing, zero]
    pkm_sum = sum(row["value"] for row in pkm)
    trip_sum = sum(row["value"] for row in trips)
    if not (pkm_sum == trip_sum == 404 and [row["value"] for row in pkm + trips] == [387, 17, 104, 300]):
        raise ValueError("specified four published observations differ")
    if missing["value_present"] or missing["status"] != "|C" or not zero["value_present"] or zero["value"] != 0:
        raise ValueError("absence and recorded zero did not reconcile")
    if live is not None:
        projected = [cell(live, row["dimension_key"][1], row["dimension_key"][3]) for row in coverage]
        if live["updated"] != data["updated"] or projected != coverage:
            raise ValueError("live release or cells have changed")
    return dict(source_id="E06", published_update=data["updated"], coverage="International, detailed, reporting geo, 2024 annual",
                pkm=dict(total=pkm_sum, unit="MIO_PKM", base_total=pkm_sum * 1_000_000, rows=pkm),
                trips=dict(total=trip_sum, unit="THS_PAS", base_total=trip_sum * 1_000, rows=trips),
                be_missing=missing, ee_zero=zero, missing_status_label=capture["status_labels"][missing["status"]])


def producer_contrast(core):
    observations = {row["case_id"]: row["result"]["observation"] for row in core
                    if row["scheme"] == "A" and row["case_id"] in ("M1", "M2")}
    left, right = (observations[case] for case in ("M1", "M2"))
    keys = left["rows"] + right["rows"]
    group = [key.split("/") for key in keys]
    participants = sorted({parts[1] for parts in group})
    common_source_units = sorted({parts[-1] for parts in group})
    if any(view["status"] != "confirmed" or view["unit"] != "ms" for view in (left, right)):
        raise ValueError("expected confirmed PET measurements for two groups")
    if len(participants) != 2 or len(common_source_units) != 5 or len(group) != 10:
        raise ValueError("the two condition denominators do not reconcile")
    return dict(source_ids=["D02","D03","D04"], unit="ms", left=left["value"], right=right["value"],
                difference=left["value"]-right["value"], across_condition_time_sum=left["value"]+right["value"],
                record_rows=len(group), language_doc_flores=common_source_units, participants=participants,
                condition_word_exposures=sum(view["denominator"]["source_words"] for view in (left, right)),
                shared_source_words=left["denominator"]["source_words"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rail", type=Path, required=True)
    parser.add_argument("--core", type=Path, required=True)
    parser.add_argument("--live-json", type=Path)
    args = parser.parse_args()
    core = [json.loads(line) for line in args.core.read_bytes().splitlines()]
    result = dict(rail=rail_contrast(json_document(args.rail), json_document(args.live_json) if args.live_json else None),
                  producer=producer_contrast(core), inputs_sha256={"rail":digest(args.rail),"core":digest(args.core)})
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
