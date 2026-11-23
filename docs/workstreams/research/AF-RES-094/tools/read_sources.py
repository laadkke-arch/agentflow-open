"""Read the auxiliary sources using curl and retain bounded public receipts."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlsplit, urlunsplit

DIRECT = {
    "P3-GUIDE": "https://raw.githubusercontent.com/pypa/cibuildwheel/63fd63b352a9a8bdcc24791c9dbee952ee9a8abc/README.md",
    "P3-OPTIONS-SOURCE": "https://raw.githubusercontent.com/pypa/cibuildwheel/63fd63b352a9a8bdcc24791c9dbee952ee9a8abc/docs/options.md",
    "P3-RTD-CONFIG": "https://raw.githubusercontent.com/pypa/cibuildwheel/63fd63b352a9a8bdcc24791c9dbee952ee9a8abc/.readthedocs.yml",
    "P1-GUIDE": "https://raw.githubusercontent.com/pypa/bandersnatch/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/README.md",
    "P1-CONFIG-RAW": "https://raw.githubusercontent.com/pypa/bandersnatch/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/docs/mirror_configuration.md",
    "P1-DEFAULTS": "https://raw.githubusercontent.com/pypa/bandersnatch/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/src/bandersnatch/example.conf",
    "P1-FILTER": "https://raw.githubusercontent.com/pypa/bandersnatch/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/docs/filtering_configuration.md",
    "R1-DESC": "https://raw.githubusercontent.com/r-lib/archive/a4c6ec37fc8737a189ca7ec7095ec0161888f9e8/DESCRIPTION",
    "R1-DOC": "https://raw.githubusercontent.com/r-lib/archive/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html",
    "R1-BUILD-META": "https://raw.githubusercontent.com/r-lib/archive/45e0d9ebc168cf3632bc2d737c9db2318668a826/pkgdown.yml",
    "R1-ARCHIVE-DATA": "https://raw.githubusercontent.com/r-lib/archive/a4c6ec37fc8737a189ca7ec7095ec0161888f9e8/inst/extdata/data.zip",
    "R2-DESC": "https://raw.githubusercontent.com/r-lib/asciicast/f992b26f3cb30c799fbb95f6148852d8ae8a7f18/DESCRIPTION",
    "R2-DOC": "https://raw.githubusercontent.com/r-lib/asciicast/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html",
    "R2-RMD": "https://raw.githubusercontent.com/r-lib/asciicast/f992b26f3cb30c799fbb95f6148852d8ae8a7f18/vignettes/asciicast-demo.Rmd",
    "R2-RMD-HEAD": "https://raw.githubusercontent.com/r-lib/asciicast/HEAD/vignettes/asciicast-demo.Rmd",
    "R2-HELPER": "https://raw.githubusercontent.com/r-lib/asciicast/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/reference/init_knitr_engine.html",
    "R2-HELLO": "https://raw.githubusercontent.com/r-lib/asciicast/f992b26f3cb30c799fbb95f6148852d8ae8a7f18/inst/examples/hello.R",
    "R2-HELLO-GENERATED": "https://raw.githubusercontent.com/r-lib/asciicast/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/inst/examples/hello.R",
    "R2-RELEASE-SOURCE": "https://codeload.github.com/r-lib/asciicast/tar.gz/f992b26f3cb30c799fbb95f6148852d8ae8a7f18",
    "R2-CAST-EXAMPLE": "https://raw.githubusercontent.com/r-lib/asciicast/f992b26f3cb30c799fbb95f6148852d8ae8a7f18/inst/examples/hello.cast",
    "R2-SVG-EXAMPLE": "https://raw.githubusercontent.com/r-lib/asciicast/f992b26f3cb30c799fbb95f6148852d8ae8a7f18/tests/testthat/_snaps/svg/hello.svg",
    "R2-OLDER-DOC": "https://raw.githubusercontent.com/r-lib/asciicast/a79eac83fa8ef967ff3d4da9bea1d646291cccb6/articles/asciicast-demo.html",
    "R2-OLDER-DESC": "https://raw.githubusercontent.com/r-lib/asciicast/c4749fe2ce12658bf31373ecbb0c10d550f1ade7/DESCRIPTION",
    "R2-CANDIDATE-6": "https://raw.githubusercontent.com/r-lib/asciicast/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo_files/figure-html/unnamed-chunk-6.svg",
    "R2-CANDIDATE-7": "https://raw.githubusercontent.com/r-lib/asciicast/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo_files/figure-html/unnamed-chunk-7.svg",
    "R2-GENERATED-TAR": "https://codeload.github.com/r-lib/asciicast/tar.gz/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1",
    "R1-R-WORKFLOW": "https://raw.githubusercontent.com/r-lib/archive/a4c6ec37fc8737a189ca7ec7095ec0161888f9e8/.github/workflows/pkgdown.yaml",
    "PYPI-SEARCH-RESPONSE": "https://pypi.org/search/?q=bandersnatch",
    "IIIF-BOOK-RAW": "https://raw.githubusercontent.com/IIIF/cookbook-recipes/2bfdae80e148054a675c0c5a2cda9b4792b907bf/recipe/0009-book-1/manifest.json",
    "IIIF-BOOK-ORIGIN": "https://iiif.io/api/cookbook/recipe/0009-book-1/manifest.json",
    "IIIF-CANVAS": "https://iiif.io/api/cookbook/recipe/0009-book-1/canvas/p2",
    "IIIF-PAINTING": "https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f19/full/max/0/default.jpg",
    "IIIF-PAINTING-RAW": "https://raw.githubusercontent.com/IIIF/api/3fc309ca29ce933dff2751530d751ca1dff9ee40/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f19/full/max/0/default.jpg",
    "EPUB-BOOK": "https://github.com/IDPF/epub3-samples/releases/download/20230704/moby-dick.epub",
    "CTRL-BLOB-RAW": "https://raw.githubusercontent.com/octocat/Hello-World/7fd1a60b01f91b314f59955a4e4d4e80d8edf11d/README",
}

PUBLIC_HEADERS = {"content-type", "content-encoding", "content-length", "date", "last-modified", "location", "etag"}


def utc():
    return datetime.now(timezone.utc).isoformat()


def safe_location(uri):
    parsed = urlsplit(uri)
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "[query omitted]" if parsed.query else "", parsed.fragment))


def header_chain(file):
    if not file.exists():
        return []
    chain = []
    for block in file.read_text(errors="replace").replace("\r", "").split("\n\n"):
        status, _, rest = block.partition("\n")
        if not status.startswith("HTTP/"):
            continue
        headers = {}
        for line in rest.splitlines():
            key, _, value = line.partition(":")
            if key.lower() in PUBLIC_HEADERS:
                headers[key.lower()] = safe_location(value.strip()) if key.lower() == "location" else value.strip()
        chain.append({"status_line": status, "headers": headers})
    return chain


def fetch(entry, cache):
    identifier, url = entry
    raw_file = cache / (identifier + ".body")
    header_file = cache / (identifier + ".headers")
    started = utc()
    result = subprocess.run(["curl", "--disable", "--silent", "--show-error", "--location",
                             "--max-redirs", "8", "--max-time", "32", "--compressed",
                             "--dump-header", str(header_file), "--output", str(raw_file),
                             "--write-out", "%{json}", "--url", url],
                            capture_output=True, text=True, check=False)
    received = utc()
    transfer = json.loads(result.stdout) if result.stdout else {}
    raw = raw_file.read_bytes() if raw_file.exists() else None
    return {"id": identifier, "original_url": url, "requested_utc": started, "received_utc": received,
            "curl_exit": result.returncode, "status": transfer.get("http_code") or None,
            "proxy_connect_status": transfer.get("http_connect") or None,
            "mime": transfer.get("content_type"), "final_url": safe_location(transfer["url_effective"]) if transfer.get("url_effective") else None,
            "response_bytes": len(raw) if raw is not None else None, "response_sha256": sha256(raw).hexdigest() if raw is not None else None,
            "headers": header_chain(header_file), "error": result.stderr.strip()[:200] or None}


if __name__ == "__main__":
    cache, receipt = map(Path, sys.argv[1:3])
    selected = sys.argv[3:]
    reads = {identifier: DIRECT[identifier] for identifier in selected} if selected else DIRECT
    cache.mkdir(exist_ok=True)
    if receipt.exists():
        raise SystemExit("Use a new receipt path for each observation.")
    with ThreadPoolExecutor(max_workers=6) as workers:
        rows = list(workers.map(lambda entry: fetch(entry, cache), reads.items()))
    receipt.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    for row in rows:
        print(row["id"], row["status"], row["proxy_connect_status"], row["mime"], row["response_bytes"])
