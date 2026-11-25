"""Extract public release, asset, and checks fields from the captured GitHub pages."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from capture_http import public_headers, public_url


def verified_text(raw, key, recorded):
    path = raw / (key + ".body")
    blob = path.read_bytes()
    assert hashlib.sha256(blob).hexdigest() == recorded[key]["body_sha256"], path
    return blob.decode("utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw", type=Path, help="Directory with transient original *.body files")
    parser.add_argument("receipts", type=Path)
    args = parser.parse_args()
    recorded = {}
    for path in sorted(args.receipts.glob("*.transport.json")):
        data = json.loads(path.read_bytes())
        header_path = path.with_name(path.name.replace(".transport.json", ".headers.txt"))
        raw = header_path.read_bytes()
        safe = public_headers(raw)
        if safe != raw:
            header_path.write_bytes(safe)
            data.update(headers_sha256=hashlib.sha256(safe).hexdigest(),
                        raw_headers_sha256=hashlib.sha256(raw).hexdigest(),
                        header_storage="redacted session headers/redirect query")
        data["curl"]["url_effective"] = public_url(data["curl"]["url_effective"])
        recorded[path.name.removesuffix(".transport.json")] = data
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def read(key):
        return verified_text(args.raw, key, recorded)

    releases = {}
    for version in ("1.13.1", "1.14.0", "1.14.1"):
        slug = version.replace(".", "_")
        release = read(f"github-release-{slug}")
        date_matches = re.findall(r'released this\s*<relative-time [^>]* datetime="([^"]+)">', release)
        assert len(date_matches) == 1, version
        assert f"/scipy/scipy/releases/expanded_assets/v{version}" in release
        readme = read(f"readme-{slug}")
        checksums = {
            name: {"sha256": digest, "line": number}
            for number, line in enumerate(readme.splitlines(), start=1)
            if (match := re.fullmatch(r"([a-f0-9]{64})\s+(scipy-\S+)", line))
            for digest, name in [match.groups()]
        }
        assets = {}
        for row in read(f"assets-{slug}").split("</li>"):
            asset = re.search(r'href="(/scipy/scipy/releases/download/v[^/]+/scipy-[^"]+)"', row)
            if asset:
                utc, = re.findall(r'<relative-time datetime="([^"]+)"', row)
                assets[asset.group(1).split("/")[-1]] = {"link": asset.group(1), "datetime_utc": utc}
        checks = read(f"checks-{slug}")
        actions = read(f"github-actions-{slug}")
        assert "Workflow runs completed with no jobs" in checks
        assert "No results matched your search." in actions and f"branch:v{version}" in actions
        releases[version] = {
            "released_this_datetime_utc": date_matches[0],
            "release_mark_location": "release header after released this, relative-time/@datetime",
            "readme_checksums": checksums,
            "assets": assets,
            "check_tab_observation": "Workflow runs completed with no jobs",
            "tag_branch_actions_observation": "No results matched your search.",
        }
    other = {}
    for key, expected in (
        ("maintenance-wheels-1_14", "No results matched your search."),
        ("fork-debug-checks", "Workflow runs completed with no jobs"),
    ):
        assert expected in read(key)
        other[key] = expected
    print(json.dumps({"releases": releases, "other_checks": other}, indent=2))


if __name__ == "__main__":
    main()
