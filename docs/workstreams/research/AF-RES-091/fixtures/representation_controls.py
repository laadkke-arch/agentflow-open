"""Use fixed tabular rows and indexed pixels to compare visible and exact contracts."""

import argparse
import io
from pathlib import Path

import pandas as pd
import pyarrow as pa
from PIL import Image, __version__ as pillow_version

from build import dump, utc
from model import digest, score_value


def record_frame(frame):
    score = frame["score"]
    return {
        "dtype": str(score.dtype),
        "normalized_numeric_values": [score_value(value) for value in score],
        "missing_mask": score.isna().tolist(),
        "integer_columns": list(frame.select_dtypes(include="integer").columns),
        "duplicated_value_row_ids": frame.loc[score.notna() & score.duplicated(keep=False), "id"].tolist(),
    }


def tabular_case(values):
    input_frame = pd.DataFrame({"id": ["A", "B", "N"], "score": pd.array(values, dtype="Int64")})
    with_metadata = pa.table(input_frame)
    without_metadata = with_metadata.replace_schema_metadata(None)
    mapped = without_metadata.to_pandas(types_mapper={pa.int64(): pd.Int64Dtype()}.get)
    return {
        "arrow_values": without_metadata.to_pylist(),
        "arrow_column_type": str(without_metadata.schema.field("score").type),
        "arrow_mask": without_metadata["score"].is_null().to_pylist(),
        "input": record_frame(input_frame),
        "plain": record_frame(without_metadata.to_pandas()),
        "mapped": record_frame(mapped),
        "metadata_roundtrip": record_frame(with_metadata.to_pandas()),
        "data_equals_after_metadata_removal": with_metadata.equals(without_metadata, check_metadata=False),
        "metadata_roundtrip_equal": with_metadata.to_pandas().equals(input_frame),
        "mapped_roundtrip_equal": mapped.equals(input_frame),
    }


def observe_png(image):
    target = io.BytesIO()
    image.save(target, format="PNG")
    payload = target.getvalue()
    with Image.open(io.BytesIO(payload)) as opened:
        indices = list(opened.getdata())
        return {
            "sha256": digest(payload), "bytes_hex": payload.hex(), "mode": opened.mode,
            "indices": indices, "palette": opened.getpalette()[:6],
            "transparent_index": opened.info.get("transparency"),
            "rgba": list(opened.convert("RGBA").getdata()),
            "index_1_positions": [(x, 0) for x, value in enumerate(indices) if value == 1],
        }


def palette_case():
    image = Image.new("P", (2, 1))
    image.putpalette([0, 0, 0, 255, 0, 0])
    image.putdata([0, 1])
    image.info["transparency"] = 0
    original = observe_png(image)
    swapped = observe_png(image.remap_palette([1, 0]))
    identity = observe_png(image.remap_palette([0, 1]))
    return {
        "original": original, "remap_swap": swapped, "remap_identity": identity,
        "swap_rgba_equal": swapped["rgba"] == original["rgba"],
        "swap_index_selection_equal": swapped["index_1_positions"] == original["index_1_positions"],
        "identity_rgba_equal": identity["rgba"] == original["rgba"],
        "identity_index_selection_equal": identity["index_1_positions"] == original["index_1_positions"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    dump(args.out, {
        "observed_utc": utc(),
        "pandas": pd.__version__, "pyarrow": pa.__version__, "Pillow": pillow_version,
        "small_integers": tabular_case([1, 2, None]),
        "consecutive_large_ids": tabular_case([2**53, 2**53 + 1, None]),
        "palette": palette_case(),
    })
