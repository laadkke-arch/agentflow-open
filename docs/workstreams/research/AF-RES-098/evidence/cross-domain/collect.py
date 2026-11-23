"""Read public EPUB/data version evidence; no example builds or authenticated writes.

Usage: python -B docs/workstreams/research/AF-RES-098/evidence/cross-domain/collect.py
Original payloads are cached in a temporary directory; only receipts and
selected factual metadata are written beside this script.
"""
import concurrent.futures
import datetime as dt
import hashlib
import io
import json
import posixpath
import re
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

OUT = Path(__file__).resolve().parent
CACHE = Path(tempfile.gettempdir()) / "af098-cross-domain-cache"
CACHE.mkdir(exist_ok=True)


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def fingerprint(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def safe_url(url):
    p = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((p.scheme, p.netloc, p.path,
                                   "[temporary-signed-query-omitted]" if "Signature=" in p.query or "sig=" in p.query else p.query, ""))


class Redirects(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        self.chain = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.chain.append({"status": code, "from": safe_url(req.full_url), "to": safe_url(newurl)})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(entry):
    key, url = entry
    redirect = Redirects()
    receipt = {"id": key, "url": url, "utc": utc(), "method": "GET"}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AF-RES-098 public evidence audit"})
        with urllib.request.build_opener(redirect).open(req, timeout=45) as response:
            data = response.read()
            receipt.update(status=response.status, mime=response.headers.get("Content-Type"),
                           final_url=safe_url(response.url), redirects=redirect.chain, **fingerprint(data))
            (CACHE / key).write_bytes(data)
    except Exception as exc:
        receipt.update(status=getattr(exc, "code", None), error=str(exc), redirects=redirect.chain)
    return receipt


URLS = {
    "epub-release": "https://api.github.com/repos/IDPF/epub3-samples/releases/tags/20230704",
    "epub-tag": "https://api.github.com/repos/IDPF/epub3-samples/git/ref/tags/20230704",
    "epub-package": "https://github.com/IDPF/epub3-samples/releases/download/20230704/cole-voyage-of-life.epub",
    "epub-previous-package": "https://github.com/IDPF/epub3-samples/releases/download/20170606/cole-voyage-of-life.epub",
    "epub-rule": "https://www.w3.org/TR/2026/REC-epub-33-20260113/",
    "data-v10": "https://zenodo.org/api/records/11196859",
    "data-v11": "https://zenodo.org/api/records/11216814",
    "datacite-v10": "https://api.datacite.org/dois/10.5281/zenodo.11196859",
    "datacite-v11": "https://api.datacite.org/dois/10.5281/zenodo.11216814",
    "datacite-concept": "https://api.datacite.org/dois/10.5281/zenodo.11196858",
    "datacite-rule": "https://datacite-metadata-schema.readthedocs.io/en/4.5/appendices/appendix-1/relationType/",
    "zenodo-version-rule": "https://help.zenodo.org/docs/deposit/manage-versions/",
    "epub-pack-script": "https://raw.githubusercontent.com/IDPF/epub3-samples/46d7e07e1b39b2d0a0245ececaf896edcd9de4b2/pack-single.sh",
    "epub-source-opf": "https://raw.githubusercontent.com/IDPF/epub3-samples/46d7e07e1b39b2d0a0245ececaf896edcd9de4b2/30/cole-voyage-of-life/EPUB/cole.opf",
    "epub-source-body": "https://raw.githubusercontent.com/IDPF/epub3-samples/46d7e07e1b39b2d0a0245ececaf896edcd9de4b2/30/cole-voyage-of-life/EPUB/xhtml/1b-childhood-painting.xhtml",
    "epub-source-image": "https://raw.githubusercontent.com/IDPF/epub3-samples/46d7e07e1b39b2d0a0245ececaf896edcd9de4b2/30/cole-voyage-of-life/EPUB/images/1-childhood-1024.jpg",
    "concept-doi-resolver": "https://doi.org/10.5281/zenodo.11196858",
    "version-doi-resolver": "https://doi.org/10.5281/zenodo.11216814",
    "zenodo-doi-rule": "https://zenodo.org/help/versioning",
}


def epub_audit(key):
    data = (CACHE / key).read_bytes()
    z = zipfile.ZipFile(io.BytesIO(data))
    names = z.namelist()
    c = ET.fromstring(z.read("META-INF/container.xml"))
    opf_path = c.find("{*}rootfiles/{*}rootfile").get("full-path")
    opf = ET.fromstring(z.read(opf_path))
    root = posixpath.dirname(opf_path)
    items = []
    for item in opf.findall("{*}manifest/{*}item"):
        a = dict(item.attrib)
        a["resolved_member"] = posixpath.normpath(posixpath.join(root, urllib.parse.unquote(a["href"])))
        a["present"] = a["resolved_member"] in names
        if a["present"]:
            a.update(fingerprint(z.read(a["resolved_member"])))
        items.append(a)
    images = []
    external = []
    data_uris = []
    docs = []
    for item in items:
        if item.get("media-type") not in ["application/xhtml+xml", "image/svg+xml"] or not item["present"]:
            continue
        member = item["resolved_member"]
        doc = ET.fromstring(z.read(member))
        docs.append({"member": member, "title": " ".join(t.text or "" for t in doc.findall(".//{*}title")), **fingerprint(z.read(member))})
        for node in doc.iter():
            tag = node.tag.split("}")[-1]
            for attr, ref in node.attrib.items():
                short_attr = attr.split("}")[-1]
                if short_attr not in ["src", "href", "data"]:
                    continue
                if ref.startswith("data:"):
                    data_uris.append({"member": member, "tag": tag, "attribute": attr, "prefix": ref[:80]})
                elif urllib.parse.urlsplit(ref).scheme in ["http", "https"]:
                    external.append({"member": member, "tag": tag, "attribute": attr, "uri": ref})
                elif tag in ["img", "image"]:
                    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(member), urllib.parse.unquote(urllib.parse.urlsplit(ref).path)))
                    row = {"body_member": member, "tag": tag, "attribute": attr, "literal_uri": ref,
                           "resolution_base": member, "resolved_member": resolved, "present": resolved in names,
                           "manifest_item": next((i for i in items if i["resolved_member"] == resolved), None)}
                    if row["present"]:
                        b = z.read(resolved)
                        row.update(fingerprint(b))
                        row["signature"] = b[:16].hex()
                    images.append(row)
    return {"package": fingerprint(data), "zip_entries": len(names), "files": sum(not n.endswith("/") for n in names),
            "mimetype": z.read("mimetype").decode(), "container": "META-INF/container.xml", "opf": opf_path,
            "declared_epub_version": opf.get("version"), "unique_identifier": opf.get("unique-identifier"),
            "title": [e.text for e in opf.findall("{*}metadata/{*}title")],
            "identifier": [e.text for e in opf.findall("{*}metadata/{*}identifier")],
            "modified": [e.text for e in opf.findall("{*}metadata/{*}meta") if e.get("property") == "dcterms:modified"],
            "opf_metadata_external_links": [e.get("href") for e in opf.findall("{*}metadata/{*}link")],
            "manifest_count": len(items), "manifest_present": sum(i["present"] for i in items),
            "spine_count": len(opf.findall("{*}spine/{*}itemref")), "manifest": items,
            "content_documents": docs, "image_references": images, "external_references": external, "data_uris": data_uris}


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        receipts = list(ex.map(fetch, URLS.items()))
    successful = {r["id"] for r in receipts if r.get("status") == 200}
    (OUT / "receipts.json").write_text(json.dumps(receipts, ensure_ascii=False, indent=2) + "\n")
    audit = {"collected_utc": utc(), "scope": "Q6 supplementary; excluded from six main cases", "epub": {}, "data": {}, "datacite": {}}
    for key in ["epub-package", "epub-previous-package"]:
        if key in successful:
            audit["epub"][key] = epub_audit(key)
    for key in ["data-v10", "data-v11"]:
        if key in successful:
            d = json.loads((CACHE / key).read_bytes())
            audit["data"][key] = {k: d.get(k) for k in ["id", "doi", "conceptdoi", "conceptrecid", "created", "updated", "files"]}
            audit["data"][key]["metadata"] = {k:d["metadata"].get(k) for k in ["title", "version", "publication_date", "resource_type", "creators", "related_identifiers", "relations"]}
            audit["data"][key]["claim_in_description"] = {"citation_records": 10006058, "v11_no_citations_added_removed": "No citations have been added" in d["metadata"].get("description", "")}
            audit["data"][key]["file_bytes_retrieved"] = False
            audit["data"][key]["limitation"] = "Publisher-declared MD5/length, not independently recomputed for 1.4/1.83 GB ZIP."
    for key in ["datacite-v10", "datacite-v11", "datacite-concept"]:
        if key in successful:
            a = json.loads((CACHE / key).read_bytes())["data"]["attributes"]
            audit["datacite"][key] = {k:a.get(k) for k in ["doi", "url", "version", "relatedIdentifiers", "titles", "types"]}
    if all(k in audit["epub"] for k in ["epub-package", "epub-previous-package"]):
        old = audit["epub"]["epub-previous-package"]
        new = audit["epub"]["epub-package"]
        om = {x["resolved_member"]:x for x in old["manifest"]}
        matches = []
        for i in new["manifest"]:
            if i["resolved_member"] in om and i.get("media-type", "").startswith("image/"):
                o = om[i["resolved_member"]]
                matches.append({"member": i["resolved_member"], "old_sha256":o.get("sha256"), "new_sha256":i.get("sha256"), "same_bytes":o.get("sha256")==i.get("sha256"),
                                "currently_referenced": any(r["resolved_member"]==i["resolved_member"] for r in new["image_references"])})
        audit["epub"]["cross_release_images"] = matches
        old_docs = {x["member"]:x for x in old["content_documents"]}
        audit["epub"]["changed_content_documents"] = [x["member"] for x in new["content_documents"]
                                                       if x["member"] in old_docs and x["sha256"] != old_docs[x["member"]]["sha256"]]
    audit["epub"]["source_commit"] = "46d7e07e1b39b2d0a0245ececaf896edcd9de4b2"
    if "epub-tag" in successful:
        audit["epub"]["tag_observation"] = json.loads((CACHE / "epub-tag").read_bytes())
    if "epub-package" in successful:
        z = zipfile.ZipFile(CACHE / "epub-package")
        comparisons = []
        for key, member in [("epub-source-opf", "EPUB/cole.opf"),
                            ("epub-source-body", "EPUB/xhtml/1b-childhood-painting.xhtml"),
                            ("epub-source-image", "EPUB/images/1-childhood-1024.jpg")]:
            if key not in successful:
                continue
            x, y = (CACHE / key).read_bytes(), z.read(member)
            comparisons.append({"source_receipt_id": key, "package_member": member,
                                "source_bytes": len(x), "source_sha256": hashlib.sha256(x).hexdigest(),
                                "package_bytes": len(y), "package_sha256": hashlib.sha256(y).hexdigest(),
                                "exact_equal": x == y,
                                "equal_after_CRLF_normalization": x.replace(b"\r\n", b"\n") == y.replace(b"\r\n", b"\n")})
        audit["epub"]["source_package_comparisons"] = comparisons
    if "epub-release" in successful:
        release = json.loads((CACHE / "epub-release").read_bytes())
        audit["epub"]["release"] = {k:release.get(k) for k in ["id", "tag_name", "published_at", "target_commitish"]}
        audit["epub"]["release"]["asset"] = [{k:x.get(k) for k in ["id", "name", "size", "created_at", "updated_at", "digest", "browser_download_url"]}
                                               for x in release["assets"] if x["name"] == "cole-voyage-of-life.epub"][0]
    audit["data"]["doi_resolution"] = [{k:r.get(k) for k in ["id", "url", "final_url", "utc", "status", "redirects"]}
                                         for r in receipts if r["id"] in ["concept-doi-resolver", "version-doi-resolver"]]
    (OUT / "audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"receipts":[{k:r.get(k) for k in ["id","status","bytes","error"]} for r in receipts],
                      "epub_audit_keys":list(audit["epub"]),"data_versions":list(audit["data"])}, ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
