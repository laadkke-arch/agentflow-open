"""Trace spine/media references with two ZIP and XML implementations."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import posixpath
import subprocess
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
import zipfile

from lxml import etree

OCF = "urn:oasis:names:tc:opendocument:xmlns:container"
OPF = "http://www.idpf.org/2007/opf"
XHTML = "http://www.w3.org/1999/xhtml"
MEDIA = {"video": "src", "audio": "src", "source": "src", "track": "src",
         "object": "data", "img": "src", "embed": "src", "iframe": "src"}


def collect_std(zip_path):
    with zipfile.ZipFile(zip_path) as z:
        assert z.testzip() is None
        root = ET.fromstring(z.read("META-INF/container.xml"))
        opf_path = root.find(f".//{{{OCF}}}rootfile").attrib["full-path"]
        package = ET.fromstring(z.read(opf_path))
        manifest = {item.attrib["id"]: item.attrib["href"]
                    for item in package.findall(f".//{{{OPF}}}manifest/{{{OPF}}}item")}
        spine = [item.attrib["idref"] for item in package.findall(f".//{{{OPF}}}spine/{{{OPF}}}itemref")]
        documents = {}
        for item_id in spine:
            path = posixpath.join(posixpath.dirname(opf_path), manifest[item_id])
            doc = ET.fromstring(z.read(path))
            parents = {child: node for node in doc.iter() for child in node}
            sources = []
            for node in doc.iter():
                if not node.tag.startswith(f"{{{XHTML}}}"):
                    continue
                kind = node.tag.split("}", 1)[1]
                attr = MEDIA.get(kind)
                if attr and attr in node.attrib:
                    parent = parents[node].tag.split("}", 1)[1]
                    sources.append((parent, kind, node.attrib[attr]))
            documents[item_id] = (path, sources)
        return summarize(opf_path, manifest, spine, documents, z.namelist(), z.read)


def collect_cli(zip_path):
    def unzip(*args):
        return subprocess.check_output(["unzip", *args])

    names = unzip("-Z1", str(zip_path)).decode().splitlines()

    def read(name):
        return unzip("-p", str(zip_path), name)

    def xml(name):
        return etree.fromstring(read(name), etree.XMLParser(resolve_entities=False, no_network=True))

    container = xml("META-INF/container.xml")
    opf_path = container.xpath("string(//ocf:rootfile/@full-path)", namespaces={"ocf": OCF})
    package = xml(opf_path)
    manifest = {entry.get("id"): entry.get("href") for entry in
                package.xpath("/opf:package/opf:manifest/opf:item", namespaces={"opf": OPF})}
    spine = package.xpath("/opf:package/opf:spine/opf:itemref/@idref", namespaces={"opf": OPF})
    media_expr = " | ".join(f"//x:{tag}[@{attr}]" for tag, attr in MEDIA.items())
    documents = {}
    for item_id in spine:
        path = posixpath.join(posixpath.dirname(opf_path), manifest[item_id])
        doc = xml(path)
        sources = []
        for element in doc.xpath(media_expr, namespaces={"x": XHTML}):
            tag = etree.QName(element).localname
            sources.append((etree.QName(element.getparent()).localname, tag, element.get(MEDIA[tag])))
        documents[item_id] = (path, sources)
    return summarize(opf_path, manifest, spine, documents, names, read)


def resolved_path(base, reference):
    uri = urlsplit(reference)
    if uri.scheme or uri.netloc:
        return reference
    return posixpath.normpath(posixpath.join(posixpath.dirname(base), unquote(uri.path)))


def summarize(opf, manifest, spine, docs, names, read):
    resolved = {resolved_path(opf, href): item for item, href in manifest.items()}
    references = []
    for item in spine:
        page, sources = docs[item]
        for parent, tag, src in sources:
            target = resolved_path(page, src)
            payload = read(target) if target in names else None
            references.append({"spineId": item, "xhtml": page, "element": f"{parent}/{tag}",
                               "src": src, "resolved": target, "manifestId": resolved.get(target),
                               "zipPresent": payload is not None, "bytes": len(payload) if payload is not None else None,
                               "sha256": hashlib.sha256(payload).hexdigest() if payload is not None else None,
                               "prefix16Hex": payload[:16].hex() if payload is not None else None})
    return {"opf": opf, "manifest": manifest, "spine": spine, "entries": sorted(names),
            "references": references,
            "manifestMediaWithoutSpineElement": sorted(
                path for path in resolved if path.endswith((".mp3", ".mp4", ".webm", ".vtt", ".xml"))
                and path not in {row["resolved"] for row in references})}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("root", type=Path)
    args = cli.parse_args()
    archive = args.root / "Shared-Culture-repacked.epub"
    test = subprocess.run(["unzip", "-t", archive], capture_output=True, check=True, text=True)
    a, b = collect_std(archive), collect_cli(archive)
    assert a == b
    result = {"finished_utc": datetime.now(timezone.utc).isoformat(),
              "methods": ["Python zipfile + ElementTree", "Info-ZIP unzip -Z1/-p + lxml XPath"],
              "archive_sha256": hashlib.file_digest(archive.open("rb"), "sha256").hexdigest(),
              "unzip_exit": test.returncode, "unzip_stdout": test.stdout, "unzip_stderr": test.stderr,
              "equal": True, "python": a, "infozip": b}
    (args.root / "epub-read.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(f"equal: OPF {a['opf']}; {len(a['entries'])} entries; {len(a['manifest'])} manifest items; "
          f"{len(a['spine'])} spine documents; {len(a['references'])} media edges")
    print(f"manifest media without spine element: {a['manifestMediaWithoutSpineElement']}")


if __name__ == "__main__":
    main()
