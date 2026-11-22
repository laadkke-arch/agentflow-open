"""Compare explicit and default Arrow types over the same Parquet input."""
import argparse
import hashlib
import json
from pathlib import Path
import struct

import pyarrow as pa
import pyarrow.parquet as pq


def offsets(array, width):
    return [value[0] for value in struct.iter_unpack({4: "<i", 8: "<q"}[width], array.buffers()[1])]


def sha256(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--version", required=True, choices=("20.0.0", "21.0.0"))
    args = parser.parse_args()
    assert pa.__version__ == args.version, pa.__version__
    fixture = json.loads(args.fixture.read_bytes())["parquet"]
    payload = [bytes.fromhex(value) if value is not None else None for value in fixture["payload_hex"]]
    table = pa.table(
        {
            "payload": pa.array(payload, type=pa.binary()),
            "items": pa.array(fixture["items"], type=pa.list_(pa.int32())),
        }
    )
    options = {"binary_type": pa.large_binary(), "list_type": pa.LargeListType}
    args.output.mkdir()
    for store_schema in fixture["stored_schema"]:
        label = "stored_schema" if store_schema else "no_stored_schema"
        path = args.output / f"{label}.parquet"
        pq.write_table(table, path, store_schema=store_schema)
        metadata = pq.read_metadata(path).metadata or {}
        assert (b"ARROW:schema" in metadata) == store_schema
        for explicit in (False, True):
            observation = {
                "stored_schema": store_schema,
                "options": "explicit" if explicit else "defaults",
                "version": pa.__version__,
                "fixture_sha256": sha256(path),
            }
            if explicit and args.version == "20.0.0":
                groups = {"both": options, **{name: {name: value} for name, value in options.items()}}
                errors = {}
                for name, selected in groups.items():
                    try:
                        pq.read_table(path, **selected)
                    except TypeError as error:
                        errors[name] = f"{type(error).__name__}: {error}"
                        assert "unexpected keyword argument" in str(error), errors
                        assert next(iter(selected)) in str(error), errors
                    else:
                        raise AssertionError(f"Expected rejection of {name}")
                observation["errors"] = errors
                print(json.dumps(observation, sort_keys=True))
                continue
            got = pq.read_table(path, **(options if explicit else {}))
            large = explicit and not store_schema
            width = 8 if large else 4
            binary, items = (got[name].combine_chunks() for name in ("payload", "items"))
            assert binary.type == (pa.large_binary() if large else pa.binary()), binary.type
            assert items.type == (pa.large_list(pa.int32()) if large else pa.list_(pa.int32())), items.type
            assert got.to_pydict() == table.to_pydict(), got.to_pydict()
            assert offsets(binary, width) == fixture["payload_offsets"]
            assert offsets(items, width) == fixture["items_offsets"]
            observation.update(
                {
                    "types": [str(binary.type), str(items.type)],
                    "offset_width_bytes": width,
                    "binary_offsets": offsets(binary, width),
                    "list_offsets": offsets(items, width),
                    "binary_null_count": binary.null_count,
                    "list_null_count": items.null_count,
                    "list_child_null_count": items.values.null_count,
                    "payload_hex": [value.hex() if value is not None else None for value in binary.to_pylist()],
                    "items": items.to_pylist(),
                }
            )
            if explicit:
                stream_path = args.output / f"{label}.arrow-stream"
                with pa.OSFile(str(stream_path), "wb") as sink, pa.ipc.new_stream(sink, got.schema) as writer:
                    writer.write_table(got)
                observation["ipc_sha256"] = sha256(stream_path)
            print(json.dumps(observation, sort_keys=True))


if __name__ == "__main__":
    main()
