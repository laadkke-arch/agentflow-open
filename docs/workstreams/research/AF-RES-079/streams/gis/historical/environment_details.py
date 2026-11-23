import datetime
import json
import sys
from osgeo import gdal, osr
import numpy
import pyarrow

record = {"checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "python": sys.version, "executable": sys.executable,
          "gdal_version": gdal.VersionInfo("RELEASE_NAME"),
          "gdal_build_info": gdal.VersionInfo("BUILD_INFO"),
          "numpy_version": numpy.__version__, "pyarrow_version": pyarrow.__version__,
          "proj_version": [osr.GetPROJVersionMajor(), osr.GetPROJVersionMinor(), osr.GetPROJVersionMicro()],
          "drivers": {name: gdal.GetDriverByName(name) is not None for name in
                      ["ARG", "Parquet", "Arrow", "RASDAMAN", "JP2Lura"]},
          "gdal_skip": gdal.GetConfigOption("GDAL_SKIP"),
          "gdal_driver_path": gdal.GetConfigOption("GDAL_DRIVER_PATH")}
print(json.dumps(record, indent=2))
