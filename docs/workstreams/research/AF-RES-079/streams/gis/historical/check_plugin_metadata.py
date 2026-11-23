import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request

ROOT = Path(__file__).parent


def probe(version):
    url = "https://api.anaconda.org/release/conda-forge/libgdal-arrow-parquet/" + version
    row = {"version": version, "opened_url": url,
           "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(url, timeout=35) as response:
            data = response.read()
            row.update(status=response.status, arrived_url=response.url)
    except urllib.error.HTTPError as error:
        data = error.read()
        row.update(status=error.code, arrived_url=error.url)
    except Exception as error:
        row.update(error=str(error), status=None)
        return row
    (ROOT / "cache" / ("parquet-plugin-" + version + ".json")).write_bytes(data)
    row.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    content = json.loads(data)
    row["linux64_artifacts"] = [{key: dist.get(key) for key in
                                  ("basename", "download_url", "md5", "sha256", "attrs")}
                                 for dist in content.get("distributions", [])
                                 if dist.get("basename", "").startswith("linux-64/")]
    row["message"] = content.get("error")
    return row


with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    rows = list(pool.map(probe, ["3.7.0", "3.8.0", "3.9.0", "3.10.1"]))
record = {"actor": "gis_evidence tool agent", "scope":
          "Current official conda-forge release metadata, not historical availability.",
          "rows": rows, "additional_independent_works": 0}
(ROOT / "plugin-metadata.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))
