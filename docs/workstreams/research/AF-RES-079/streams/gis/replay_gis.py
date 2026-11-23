"""AF-RES-079 follow-up probes; execution results are JSON, not assertions of success.

Use a Python interpreter linked to the exact GDAL edition being compared.
No network calls or automatic installation. Outputs are created only when requested.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import struct
import sys


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-version", required=True)
    parser.add_argument("--arg-opt-in", action="store_true")
    modes = parser.add_subparsers(dest="mode", required=True)
    modes.add_parser("env")
    for mode in ("inspect-raster", "inspect-vector"):
        sub = modes.add_parser(mode)
        sub.add_argument("--input", required=True)
        sub.add_argument("--driver")
    sub = modes.add_parser("write-vector")
    sub.add_argument("--fixture", required=True)
    sub.add_argument("--output", required=True)
    sub.add_argument("--encoding", default="WKB")
    sub.add_argument("--compression", default="NONE")
    sub.add_argument("--point-m", action="store_true")
    sub = modes.add_parser("write-raster")
    sub.add_argument("--output", required=True)
    sub.add_argument("--bands", type=int, default=1)
    args = parser.parse_args()
    record = {
        "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "argv": sys.argv[1:], "actor": "executor invoking this supplied probe",
        "location": sys.executable, "result": "unobserved",
    }
    try:
        from osgeo import gdal, ogr, osr
        gdal.UseExceptions()
        ogr.UseExceptions()
        actual = gdal.VersionInfo("RELEASE_NAME")
        record["gdal_version"] = actual
        if actual != args.expected_version:
            raise RuntimeError("Wrong GDAL edition: expected %s; found %s" %
                               (args.expected_version, actual))
        os.environ.pop("GDAL_ENABLE_DEPRECATED_DRIVER_ARG", None)
        gdal.SetConfigOption("GDAL_ENABLE_DEPRECATED_DRIVER_ARG",
                             "YES" if args.arg_opt_in else None)
        record["arg_opt_in"] = args.arg_opt_in
        record["drivers"] = {name: gdal.GetDriverByName(name) is not None
                             for name in ("ARG", "RASDAMAN", "Parquet")}
        if args.mode == "env":
            record["result"] = "observed_environment"
        elif args.mode.startswith("inspect-"):
            source = args.input
            if Path(source).is_file():
                record["input_sha256"] = digest(source)
            kwargs = {"allowed_drivers": [args.driver]} if args.driver else {}
            flags = gdal.OF_RASTER if args.mode == "inspect-raster" else gdal.OF_VECTOR
            dataset = gdal.OpenEx(source, flags, **kwargs)
            if dataset is None:
                raise RuntimeError("OpenEx returned None")
            record["opened_driver"] = dataset.GetDriver().ShortName
            if args.mode == "inspect-raster":
                record["shape"] = [dataset.RasterYSize, dataset.RasterXSize,
                                   dataset.RasterCount]
                record["geotransform"] = dataset.GetGeoTransform()
                record["srs_wkt"] = dataset.GetProjectionRef()
                band = dataset.GetRasterBand(1)
                record["dtype"] = gdal.GetDataTypeName(band.DataType)
                record["nodata"] = band.GetNoDataValue()
                record["checksum"] = band.Checksum()
                if dataset.RasterXSize * dataset.RasterYSize <= 64:
                    raw = band.ReadRaster(buf_type=gdal.GDT_Float64)
                    record["ordered_values"] = list(struct.unpack("=" + "d" *
                        (len(raw) // 8), raw))
            else:
                layer = dataset.GetLayer(0)
                definition = layer.GetLayerDefn()
                record["fields"] = [
                    {"name": definition.GetFieldDefn(i).GetName(),
                     "type": definition.GetFieldDefn(i).GetTypeName()}
                    for i in range(definition.GetFieldCount())]
                srs = layer.GetSpatialRef()
                record["srs_wkt"] = srs.ExportToWkt() if srs else None
                record["geo_metadata"] = layer.GetMetadataItem("geo", "_PARQUET_METADATA_")
                record["ordered_rows"] = []
                for feature in layer:
                    geometry = feature.GetGeometryRef()
                    record["ordered_rows"].append({
                        "values": [feature.GetField(i) for i in
                                   range(definition.GetFieldCount())],
                        "geometry": geometry.ExportToWkt() if geometry else None,
                        "is_empty": bool(geometry.IsEmpty()) if geometry else None})
                try:
                    import pyarrow.parquet as pq
                    record["arrow_schema"] = str(pq.read_schema(source))
                except ImportError:
                    record["arrow_schema"] = "UNOBSERVED: pyarrow unavailable"
            record["result"] = "observed_read"
        elif args.mode == "write-vector":
            fixture = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
            record["input_sha256"] = digest(args.fixture)
            output = Path(args.output)
            if output.exists():
                raise RuntimeError("Output already exists; preserve prior evidence")
            output.parent.mkdir(parents=True, exist_ok=True)
            driver = ogr.GetDriverByName("Parquet")
            if driver is None:
                raise RuntimeError("Parquet driver unavailable")
            dataset = driver.CreateDataSource(str(output))
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(4326)
            srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
            geometry_type = ogr.wkbPointM if args.point_m else ogr.wkbPoint
            layer = dataset.CreateLayer("af079", srs=srs, geom_type=geometry_type,
                options=["GEOMETRY_ENCODING=" + args.encoding,
                         "COMPRESSION=" + args.compression])
            if layer is None:
                raise RuntimeError("CreateLayer returned None")
            layer.CreateField(ogr.FieldDefn("id", ogr.OFTInteger))
            layer.CreateField(ogr.FieldDefn("label", ogr.OFTString))
            for row in fixture["rows"]:
                feature = ogr.Feature(layer.GetLayerDefn())
                feature["id"] = row["id"]
                feature["label"] = row["label"]
                if row["wkt"] is not None:
                    feature.SetGeometry(ogr.CreateGeometryFromWkt(row["wkt"]))
                code = layer.CreateFeature(feature)
                if code != 0:
                    raise RuntimeError("CreateFeature returned " + str(code))
            dataset = None
            record["output_sha256"] = digest(output)
            record["result"] = "observed_write"
        elif args.mode == "write-raster":
            output = Path(args.output)
            if output.exists():
                raise RuntimeError("Output already exists; preserve prior evidence")
            output.parent.mkdir(parents=True, exist_ok=True)
            source = gdal.GetDriverByName("MEM").Create("", 2, 2, args.bands, gdal.GDT_Int16)
            source.SetGeoTransform((0, 1, 0, 2, 0, -1))
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(4326)
            source.SetProjection(srs.ExportToWkt())
            for i in range(1, args.bands + 1):
                source.GetRasterBand(i).SetNoDataValue(-9999)
                source.GetRasterBand(i).WriteRaster(0, 0, 2, 2,
                    struct.pack("=4h", 1, 2, 3, -9999), buf_type=gdal.GDT_Int16)
            driver = gdal.GetDriverByName("ARG")
            if driver is None:
                raise RuntimeError("ARG driver unavailable")
            result = driver.CreateCopy(str(output), source)
            if result is None:
                raise RuntimeError("CreateCopy returned None")
            result = None
            record["output_sha256"] = digest(output)
            record["result"] = "observed_write"
        record["exit_code"] = 0
    except Exception as exc:
        record["result"] = "observed_failure"
        record["exception_type"] = type(exc).__name__
        record["error"] = str(exc)
        record["exit_code"] = 3
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return record["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
