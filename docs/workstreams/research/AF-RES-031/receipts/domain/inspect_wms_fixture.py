import hashlib
import json
from pathlib import Path
import re
import struct
import sys
from zipfile import ZipFile

fixture, xml = map(Path, sys.argv[1:])
with ZipFile(fixture) as archive:
    shp = archive.read("shapefile/Lakes.shp")
    projection = archive.read("shapefile/Lakes.prj").decode()
assert struct.unpack_from(">i", shp)[0] == 9994
assert 'UNIT["Degree"' in projection
assert 2 * struct.unpack_from(">i", shp, 24)[0] == len(shp)
x0, y0, x1, y1 = struct.unpack_from("<4d", shp, 36)
coordinates = (x0, y0, x1, y1)
swapped = (y0, x0, y1, x1)
assert x0 < x1 and y0 < y1 and all(-90 < n < 90 for n in coordinates)
assert swapped != coordinates
text = xml.read_text()
raw = re.search(r'<ctl:with-param name="preferred-bbox">([^<]+)</ctl:with-param>', text)[1]
symmetric = tuple(map(float, raw.split(",")))
assert symmetric == (symmetric[1], symmetric[0], symmetric[3], symmetric[2])
print(json.dumps({
    "observed_shp_header_x_y_degrees": coordinates,
    "crs84_if_header_x_is_longitude": coordinates,
    "epsg4326_if_header_x_is_longitude": swapped,
    "projection_from_fixture": projection,
    "both_fit_common_numeric_range_and_min_max": True,
    "symmetric_ctl_literal": raw,
    "swap_leaves_symmetric_literal_equal": True,
    "member_sha256": hashlib.sha256(shp).hexdigest(),
}, sort_keys=True))
