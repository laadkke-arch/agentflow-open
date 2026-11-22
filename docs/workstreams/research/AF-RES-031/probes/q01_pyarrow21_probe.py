"""Not executed in AF-RES-025. Small functional input, not a >2GiB test."""
import argparse
import json
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq

parser = argparse.ArgumentParser()
parser.add_argument('--output-dir', required=True)
args = parser.parse_args()
out = Path(args.output_dir)
out.mkdir(parents=True, exist_ok=True)
assert pa.__version__ == '21.0.0', pa.__version__
input_table = pa.table({
    'payload': pa.array([b'ab', None, b'xyz'], type=pa.binary()),
    'items': pa.array([[1, None, 2], None, []], type=pa.list_(pa.int32())),
})
observed = {}
for store_schema in (False, True):
    label = 'stored_schema' if store_schema else 'no_stored_schema'
    path = out / (label + '.parquet')
    pq.write_table(input_table, path, store_schema=store_schema)
    got = pq.read_table(path, binary_type=pa.large_binary(), list_type=pa.LargeListType)
    expect_binary = pa.binary() if store_schema else pa.large_binary()
    expect_list = pa.list_(pa.int32()) if store_schema else pa.large_list(pa.int32())
    assert got.schema.field('payload').type == expect_binary, got.schema
    assert got.schema.field('items').type == expect_list, got.schema
    assert got.to_pydict() == input_table.to_pydict()
    observed[label] = str(got.schema)
    if not store_schema:
        with pa.OSFile(str(out / 'large-types.arrow-stream'), 'wb') as sink:
            with pa.ipc.new_stream(sink, got.schema) as writer:
                writer.write_table(got)
print(json.dumps({'pyarrow': pa.__version__, 'schemas': observed,
                  'row_count': input_table.num_rows,
                  'large_buffer_threshold_tested': False,
                  'java_import_tested': False}, indent=2))
