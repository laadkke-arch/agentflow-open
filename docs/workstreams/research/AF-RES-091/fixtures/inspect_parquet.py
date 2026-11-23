"""Read the raw Parquet footer and geometry storage with PyArrow alone."""

import argparse
import hashlib
import io
import json
import os
import struct
import sys
from datetime import datetime, timezone
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq


def array_record(array):
    record = {
        "type": str(array.type),
        "valid": array.is_valid().to_pylist(),
        "length": len(array),
    }
    if pa.types.is_struct(array.type):
        record["fields"] = {
            field.name: {"nullable": field.nullable, **array_record(array.field(i))}
            for i, field in enumerate(array.type)
        }
    elif pa.types.is_list(array.type):
        record["offsets"] = array.offsets.to_pylist()
        record["values"] = {
            "field_name": array.type.value_field.name,
            "nullable": array.type.value_field.nullable,
            **array_record(array.values),
        }
    else:
        record["values"] = [storage_value(value) for value in array.to_pylist()]
    return record


def storage_value(value):
    if isinstance(value, bytes):
        order = "<" if value[0] == 1 else ">"
        return {"wkb_hex": value.hex(), "outer_type_code": struct.unpack_from(order + "I", value, 1)[0]}
    if isinstance(value, float) and (value != value or abs(value) == float("inf")):
        return str(value)
    return value


def inspect(path, expected):
    payload = path.read_bytes()
    sha256 = hashlib.sha256(payload).hexdigest()
    if sha256 != expected:
        raise ValueError("Parquet bytes differ from the writer receipt")
    file = pq.ParquetFile(io.BytesIO(payload))
    table = file.read()
    arrow_schema = file.schema_arrow
    metadata = file.metadata.metadata
    geo_raw = metadata[b"geo"]
    geo = json.loads(geo_raw)
    geometry = geo["primary_column"]
    return {
        "observed_utc": datetime.now(timezone.utc).isoformat(),
        "command": [sys.executable, *sys.orig_argv[1:]],
        "pid": os.getpid(),
        "geopandas_loaded": "geopandas" in sys.modules,
        "pyarrow": pa.__version__,
        "sha256": sha256,
        "bytes": len(payload),
        "geo_footer_sha256": hashlib.sha256(geo_raw).hexdigest(),
        "geo": geo,
        "geo_raw_utf8": geo_raw.decode(),
        "metadata_keys": sorted(k.decode() for k in metadata),
        "created_by": file.metadata.created_by,
        "format_version": file.metadata.format_version,
        "row_count": file.metadata.num_rows,
        "row_groups": file.metadata.num_row_groups,
        "arrow_fields": [{"name": field.name, "type": str(field.type), "nullable": field.nullable} for field in arrow_schema],
        "parquet_leaves": [
            {
                "path": column.path, "physical": column.physical_type,
                "definition": column.max_definition_level, "repetition": column.max_repetition_level,
                "compression": file.metadata.row_group(0).column(i).compression,
            }
            for i, column in enumerate(file.schema)
        ],
        "root_geometry": array_record(table[geometry].combine_chunks()),
        "row_ids": table["id"].to_pylist(),
        "scores": table["score"].to_pylist(),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("sha256")
    args = parser.parse_args()
    print(json.dumps(inspect(args.path, args.sha256), ensure_ascii=False, allow_nan=False, indent=2))
