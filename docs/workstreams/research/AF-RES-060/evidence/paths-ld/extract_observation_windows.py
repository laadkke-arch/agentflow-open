"""Extract bounded reading windows from the frozen plan and acquired responses."""
from pathlib import Path
import datetime
import hashlib
import importlib.util
import json
import re
import sys
from urllib.parse import urlsplit

sys.dont_write_bytecode = True
HERE = Path(__file__).parent.resolve()
spec = importlib.util.spec_from_file_location("prepared_paths", HERE / "prepare_paths.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
PLAN = json.loads((HERE / "prepared-plan.json").read_text())
SECOND_DIR = HERE / "second-windows"
SECOND_DIR.mkdir(exist_ok=True)


def digest(payload):
    return hashlib.sha256(payload).hexdigest()


def save_window(key, window):
    target = SECOND_DIR / (key + ".txt")
    target.write_text(window["text"] + "\n")
    return str(target.relative_to(HERE)), digest(window["text"].encode())


def main():
    records = []
    for row in PLAN["rows"]:
        first = row["paths"][0]["documents"][0]
        records.append({
            "id": row["catalog_id"].replace("-", "") + "-D1",
            "source_id": "P-" + row["catalog_id"] + "-D1",
            "catalog_id": row["catalog_id"],
            "original_url": row["original_url"],
            "fixed_url": first["fixed_response_url"],
            "implementation_sha": first["implementation_sha"],
            "implementation_version": first["implementation_version"],
            "window_file": first["window_file"],
            "words": first["window"]["words"],
            "hash": first["raw_sha256"],
            "window_hash": first["window"]["window_sha256"],
            "status": "bounded_window_prepared_for_direct_read",
            "role": "provider_readme",
            "acquisition": "same_response_as_stage2",
            "physical_body_requests": 0,
            "implementation_linkage": "fixed_provider_commit",
        })
    web = json.loads((HERE / "web-seconds.json").read_text())
    github = json.loads((HERE / "github-seconds.json").read_text())
    for row in github:
        path = HERE / row["raw_file"]
        payload = path.read_bytes()
        for trim in range(4):
            candidate = payload if trim == 0 else payload[:-trim]
            if hashlib.sha1(("blob " + str(len(candidate)) + "\0").encode() + candidate).hexdigest() == row["blob"]:
                assert trim == 0 or payload[-trim:] == b"\n" * trim
                payload = candidate
                path.write_bytes(payload)
                break
        else:
            raise ValueError("Git blob mismatch " + row["id"])
        row["sha256"] = digest(payload)
    for row in web + github:
        key = row["id"]
        catalog_id = key[:2] + "-" + key[2:5]
        document = {
            "id": key,
            "source_id": "P-" + catalog_id + "-" + key.split("-")[1],
            "catalog_id": catalog_id,
            "original_url": row["original_url"],
            "fixed_url": row.get("fixed_url"),
            "implementation_sha": row.get("sha"),
            "implementation_version": None,
            "window_file": None,
            "words": 0,
            "hash": row.get("sha256"),
            "window_hash": None,
            "status": "access_failed",
            "role": "linked_document; no direct provider-version linkage assumed",
            "acquired_utc": row.get("acquired_utc"),
            "physical_body_requests": len(row.get("attempts", [1])),
            "metadata_requests": row.get("metadata_requests", 0),
            "implementation_linkage": "not_established",
        }
        if row.get("raw_file"):
            path = HERE / row["raw_file"]
            raw = path.read_bytes().decode(row.get("charset", "utf-8"), errors="replace")
            fragment = urlsplit(row["original_url"]).fragment
            window = module.first_window(raw, path.suffix, fragment)
            window_file, window_hash = save_window(key, window)
            document.update({
                "window_file": window_file,
                "window_hash": window_hash,
                "words": window["words"],
                "heading": window.get("heading"),
                "status": "bounded_window_prepared_for_direct_read" if window["words"] else "no_readable_body_at_selected_destination",
                "window_status": window["status"],
            })
        if key == "SC036-D3":
            # The selected tools.ietf URL redirected to datatracker in the web
            # reader. HTTP acquisition remained 403. Keep the direct-reader
            # response and its bounded document text; do not invent an HTML hash.
            response = (HERE / "raw/SC036-D3.web.txt").read_text()
            numbered = re.findall(r"^L(\d+): ?(.*)$", response, flags=re.M)
            body = []
            for number, value in numbered:
                if int(number) >= 27:
                    value = re.sub(r"【\d+†([^】]+)】", r"\1", value)
                    value = re.sub(r"^\s*#\s+", "", value)
                    body.append(value)
            full = "\n".join(body)
            words = list(re.finditer(r"\S+", full))
            clipped = full[:words[499].end()].strip() if len(words) >= 500 else full.strip()
            window_file, window_hash = save_window(key, {"text": clipped})
            document.update({
                "fixed_url": "https://datatracker.ietf.org/doc/html/draft-zyp-json-schema-04",
                "window_file": window_file,
                "window_hash": window_hash,
                "words": len(clipped.split()),
                "status": "bounded_web_reader_primary_document_excerpt",
                "hash": digest(response.encode()),
                "hash_kind": "web_reader_response_text; original HTTP body unavailable",
                "source_ref": "turn507786142view1",
                "heading": "JSON Schema: core definitions and terminology",
                "edition": "draft-zyp-json-schema-04, 31 January 2013",
                "physical_body_requests": 4,
                "acquisition_note": "Original HTTP, HTTPS retry and observed redirect HTTP all403; exact original URL web reader returned same draft, first500 document words retained.",
            })
        elif key == "SC036-D2":
            document["physical_body_requests"] += 1
            document["acquisition_note"] = "Original URL403 plus exact original URL web reader unavailable; no mirror substituted."
        records.append(document)
    by_id = {row["catalog_id"]: row for row in PLAN["rows"]}
    for key, fragment in [("SC039-D3", "draft-support"), ("SC040-D3", "")]:
        catalog_id = key[:2] + "-" + key[2:5]
        source = module.acquisitions()[catalog_id]
        path = Path(source["raw_file"])
        if not path.is_absolute():
            path = module.OWNED.parents[3] / path
        payload = path.read_bytes()
        window = module.first_window(payload.decode(), path.suffix, fragment)
        if key == "SC040-D3":
            window_file = by_id[catalog_id]["paths"][0]["documents"][0]["window_file"]
            window_hash = window["window_sha256"]
        else:
            window_file, window_hash = save_window(key, window)
        records.append({
            "id": key,
            "source_id": "P-" + catalog_id + "-D3",
            "catalog_id": catalog_id,
            "original_url": by_id[catalog_id]["paths"][2]["documents"][1]["requested_url"],
            "fixed_url": source["fixed_url"] + ("#" + fragment if fragment else ""),
            "implementation_sha": source.get("sha"),
            "implementation_version": source.get("version"),
            "window_file": window_file,
            "words": window["words"],
            "hash": digest(payload),
            "window_hash": window_hash,
            "status": "bounded_window_prepared_for_direct_read",
            "role": "same_provider_readme_fragment" if fragment else "self_link_same_readme_return",
            "physical_body_requests": 0,
            "implementation_linkage": "same_fixed_provider_commit",
        })
    (HERE / "document-records.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
    for record in records:
        print(record["id"], record["status"], record["words"], record.get("heading", ""))


if __name__ == "__main__":
    main()
