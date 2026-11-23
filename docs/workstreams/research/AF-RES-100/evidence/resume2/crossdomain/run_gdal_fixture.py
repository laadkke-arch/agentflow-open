#!/usr/bin/env python3
"""Supplemental local adaptation of pinned GDAL vertical-shift fixtures.

Upstream: OSGeo/gdal 35a44cc570cdf4dbd55611e4bd61da76e56bc221,
autotest/utilities/test_gdalwarp_lib.py, lines 1865-1935 and 2091-2114.
Upstream test authorship header credits Faza Mahamood and Even Rouault (MIT).
The two-band, -novshift and mandatory-missing variants are this study's
adaptations. This script does not run or claim to reproduce the upstream suite.
No dependency installation or network grid acquisition is performed.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
from pathlib import Path
import struct
import sys

os.environ["PROJ_NETWORK"] = "OFF"
from osgeo import gdal, osr  # noqa: E402


def main() -> None:
    output_dir = Path(__file__).resolve().parent
    cache_dir = output_dir.parents[1] / "_cache" / "resume2-crossdomain" / "runtime-gdal"
    cache_dir.mkdir(parents=True, exist_ok=True)
    gdal.UseExceptions()
    osr.SetPROJEnableNetwork(False)

    grid_path = cache_dir / "constant-20.gtx"
    missing_path = cache_dir / "never-created-grid.gtx"
    if missing_path.exists():
        raise RuntimeError("The mandatory-missing control path unexpectedly exists")

    reference = osr.SpatialReference()
    reference.SetFromUserInput("WGS84")
    grid = gdal.GetDriverByName("GTX").Create(str(grid_path), 3, 3, 1, gdal.GDT_Float32)
    grid.SetProjection(reference.ExportToWkt())
    grid.SetGeoTransform([-270, 180, 0, 135, 0, -90])
    grid.GetRasterBand(1).Fill(20)
    grid = None

    cases = [
        {"id": "single_existing_grid", "bands": 1, "grid": str(grid_path), "expected": [120], "basis": "upstream test_gdalwarp_lib_135"},
        {"id": "two_band_existing_grid", "bands": 2, "grid": str(grid_path), "expected": [100, 100], "basis": "study adaptation; pinned gdalwarp vertical-transformation automatic single-band rule"},
        {"id": "single_novshift", "bands": 1, "grid": str(grid_path), "options": ["-novshift"], "expected": [100], "basis": "study adaptation; pinned gdalwarp -novshift option"},
        {"id": "single_optional_missing_grid", "bands": 1, "grid": "@" + str(missing_path), "expected": [100], "basis": "upstream test_gdalwarp_lib_135j, adapted missing path"},
        {"id": "single_mandatory_missing_grid", "bands": 1, "grid": str(missing_path), "expected_failure": True, "basis": "study adaptation; compare required grid with optional @ control"},
    ]
    records = []
    for case in cases:
        source = gdal.GetDriverByName("MEM").Create("", 1, 1, case["bands"], gdal.GDT_Byte)
        source.SetGeoTransform([500000, 1, 0, 4000000, 0, -1])
        for band in range(1, case["bands"] + 1):
            source.GetRasterBand(band).Fill(100)
        errors = []
        gdal.PushErrorHandler(lambda kind, number, message: errors.append({"class": kind, "number": number, "message": message}))
        actual = None
        exception = None
        try:
            dataset = gdal.Warp(
                "", source, format="MEM",
                srcSRS=f"+proj=utm +zone=31 +datum=WGS84 +units=m +geoidgrids={case['grid']} +vunits=m +no_defs",
                dstSRS="EPSG:4979", options=case.get("options", []),
            )
            if dataset is not None:
                actual = [struct.unpack("d", dataset.GetRasterBand(band).ReadRaster(0, 0, 1, 1, buf_type=gdal.GDT_Float64))[0] for band in range(1, dataset.RasterCount + 1)]
        except RuntimeError as exc:
            exception = str(exc)
        finally:
            gdal.PopErrorHandler()
        expected_failure = case.get("expected_failure", False)
        passed = (actual is None and exception is not None) if expected_failure else actual == case["expected"]
        records.append({**case, "actual_values": actual, "exception": exception, "errors": errors, "expectation_met": passed})

    report = {
        "kind": "supplemental_local_runtime_not_pinned_upstream_suite",
        "executed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python": sys.executable,
        "gdal_version": gdal.VersionInfo("RELEASE_NAME"),
        "proj_version": [osr.GetPROJVersionMajor(), osr.GetPROJVersionMinor(), osr.GetPROJVersionMicro()],
        "pinned_documentation_versions": {"GDAL": "3.10.0", "PROJ": "9.5.1"},
        "version_equivalence_claimed": False,
        "network_enabled": osr.GetPROJEnableNetwork(),
        "grid_sha256": hashlib.sha256(grid_path.read_bytes()).hexdigest(),
        "grid_file": str(grid_path),
        "cases": records,
    }
    (output_dir / "gdal-runtime.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
