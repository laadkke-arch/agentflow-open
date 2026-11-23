"""Read one already frozen Parquet file's CRS, nullability, and metadata contract."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import sys
from osgeo import gdal
import pyarrow
import pyarrow.parquet as pq

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--expected-version", required=True)
args = parser.parse_args()
gdal.UseExceptions()
record = {"checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "input": args.input, "input_sha256": hashlib.sha256(Path(args.input).read_bytes()).hexdigest(),
          "python": sys.version, "gdal": gdal.VersionInfo("RELEASE_NAME"),
          "pyarrow": pyarrow.__version__}
try:
    if record["gdal"] != args.expected_version:
        raise RuntimeError("Wrong GDAL edition")
    dataset = gdal.OpenEx(args.input, gdal.OF_VECTOR, allowed_drivers=["Parquet"])
    layer = dataset.GetLayer(0)
    srs = layer.GetSpatialRef()
    record["srs"] = None if srs is None else {
        "authority_name": srs.GetAuthorityName(None),
        "authority_code": srs.GetAuthorityCode(None),
        "data_axis_to_srs_axis_mapping": srs.GetDataAxisToSRSAxisMapping(),
        "axis_names": [srs.GetAxisName(None, i) for i in range(srs.GetAxesCount())],
        "wkt": srs.ExportToWkt()}
    definition = layer.GetLayerDefn()
    record["ogr_geometry_fields"] = definition.GetGeomFieldCount()
    record["ogr_fields"] = [{"name": definition.GetFieldDefn(i).GetName(),
                             "type": definition.GetFieldDefn(i).GetTypeName(),
                             "nullable": bool(definition.GetFieldDefn(i).IsNullable())}
                            for i in range(definition.GetFieldCount())]
    metadata = layer.GetMetadataItem("geo", "_PARQUET_METADATA_")
    record["ogr_geo_metadata"] = json.loads(metadata) if metadata else None
    parquet = pq.ParquetFile(args.input)
    record["parquet_created_by"] = parquet.metadata.created_by
    record["arrow_fields"] = [{"name": field.name, "type": str(field.type),
                               "nullable": field.nullable,
                               "metadata": {k.decode(): v.decode(errors="replace")
                                            for k, v in (field.metadata or {}).items()}}
                              for field in parquet.schema_arrow]
    table = parquet.read()
    record["arrow_null_counts"] = {name: table[name].null_count for name in table.column_names}
    record["scope_limit"] = "Schema and reader CRS state observed; no coordinate transformation test. Normal two-point fixture has no null values and diagonal coordinates, so it alone cannot expose axis reversal or prove all null cases."
    record["exit_code"] = 0
except Exception as error:
    record["error"] = str(error)
    record["exception_type"] = type(error).__name__
    record["exit_code"] = 3
print(json.dumps(record, ensure_ascii=False, indent=2))
raise SystemExit(record["exit_code"])
