"""Extract the same fields from both AF-RES-243 EPUB records with ElementTree."""
import argparse
import hashlib
import json
import posixpath
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile

from receipt import digest, invoke, write_json

PINS = json.loads(Path(__file__).with_name("epub.json").read_text())
OPF = "{http://www.idpf.org/2007/opf}"
HTML = "{http://www.w3.org/1999/xhtml}"
EPUB_TYPE = "{http://www.idpf.org/2007/ops}type"
DC = "{http://purl.org/dc/elements/1.1/}"


def git_blob(content):
    return hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()


def joined_path(base, href):
    return posixpath.normpath(posixpath.join(posixpath.dirname(base), unquote(href)))


def clean_text(element):
    return " ".join("".join(element.itertext()).split())


def parse(book, opf_bytes, nav_bytes):
    opf, nav = ET.fromstring(opf_bytes), ET.fromstring(nav_bytes)
    metadata = opf.find(OPF + "metadata")
    manifest = {item.attrib["id"]: item.attrib
                for item in opf.findall(f"{OPF}manifest/{OPF}item")}
    nav_id, nav_member = [(item_id, item) for item_id, item in manifest.items()
                          if "nav" in item.get("properties", "").split()][0]
    nav_path = joined_path(book["opf"], nav_member["href"])
    if nav_path != book["nav"]:
        raise ValueError("OPF manifest resolves to a different navigation member")
    by_href = {joined_path(book["opf"], item["href"]): item_id for item_id, item in manifest.items()}
    spine = opf.find(OPF + "spine")
    sequence = [{"position": index, "idref": ref.attrib["idref"], "properties": ref.get("properties"),
                 "linear_raw": ref.get("linear"), "linear_effective": ref.get("linear", "yes"),
                 "href": manifest[ref.attrib["idref"]]["href"]}
                for index, ref in enumerate(spine.findall(OPF + "itemref"), 1)]
    spine_ids = {item["idref"] for item in sequence}

    def headings(node):
        return [{"level": int(elem.tag[-1]), "text": clean_text(elem)}
                for elem in node.iter() if elem.tag in {HTML + "h" + str(i) for i in range(1, 7)}]

    def link(elem):
        href = elem.attrib["href"]
        url = urlsplit(href)
        path = None if url.scheme or url.netloc else joined_path(nav_path, url.path) if url.path else nav_path
        item = by_href.get(path)
        match = None
        if path == nav_path and url.fragment:
            match = any(node.get("id") == unquote(url.fragment) for node in nav.iter())
        return {"text": clean_text(elem), "href": href, "resolved_member": path,
                "fragment": url.fragment or None, "same_document_fragment_exists": match,
                "manifest_item_id": item, "in_spine": item in spine_ids,
                "epub_type": elem.get(EPUB_TYPE)}

    sections = []
    for node in nav.iter(HTML + "nav"):
        sections.append({"type": node.get(EPUB_TYPE), "id": node.get("id"),
                         "heading_inside_nav": headings(node),
                         "links": [link(elem) for elem in node.iter(HTML + "a")]})
    return {
        "package_version": opf.attrib["version"], "book_title": metadata.findtext(DC + "title"),
        "publisher_as_declared": metadata.findtext(DC + "publisher"), "date_as_declared": metadata.findtext(DC + "date"),
        "nav_manifest_id": nav_id, "nav_resolved_member": nav_path, "nav_in_spine": nav_id in spine_ids,
        "spine_attributes": spine.attrib, "spine_sequence": sequence,
        "xhtml_title": nav.findtext(f"{HTML}head/{HTML}title"),
        "all_body_headings": headings(nav.find(HTML + "body")), "nav_sections": sections,
        "xml_parser": "xml.etree.ElementTree",
    }


def record(out, work, book):
    slug = book["slug"]
    folder = out / slug
    folder.mkdir()
    base = f"https://raw.githubusercontent.com/IDPF/epub3-samples/{PINS['repository_commit']}/30/{slug}/"
    sources = {}
    for kind in ("opf", "nav"):
        member = book[kind]
        filename = work / (slug + "." + kind)
        url = base + member
        step = invoke(folder, kind, ["curl", "-fLsS", "--max-time", "45", "-o", filename,
                                     "-w", "%{http_code} %{size_download}\n", url], cwd=work)
        if step["exit"]:
            raise ValueError("Pinned source XML not received")
        source = filename.read_bytes()
        if git_blob(source) != book[kind + "_git_blob"]:
            raise ValueError("Source XML differs from AF-RES-243's pinned blob")
        sources[kind] = (source, url, digest(filename))

    epub_url = "https://github.com/IDPF/epub3-samples/releases/download/" + PINS["release"] + "/" + slug + ".epub"
    filename = work / (slug + ".epub")
    step = invoke(folder, "epub-release", ["curl", "-fLsS", "--max-time", "60", "-o", filename,
                                           "-w", "%{http_code} %{size_download}\n", epub_url], cwd=work)
    if step["exit"]:
        raise ValueError("Public EPUB package not received")
    if (filename.stat().st_size, digest(filename)) != (book["archive_bytes"], book["archive_sha256"]):
        raise ValueError("Public EPUB package fingerprint changed")
    with ZipFile(filename) as package:
        container = package.read("META-INF/container.xml")
        (folder / "container.xml").write_bytes(container)
        rootfiles = ET.fromstring(container).findall(".//{*}rootfile")
        paths = [rootfile.attrib["full-path"] for rootfile in rootfiles]
        if paths != [book["opf"]]:
            raise ValueError("Container package-document path differs from pin")
        public = {kind: package.read(book[kind]) for kind in ("opf", "nav")}
        matches = {kind: git_blob(data) == book[kind + "_git_blob"] for kind, data in public.items()}
        published_view = parse(book, public["opf"], public["nav"])
    frozen_view = parse(book, sources["opf"][0], sources["nav"][0])
    result = {"case": slug, "xml_sources": {kind: {"url": url, "sha256": sha, "git_blob": git_blob(data)}
                                           for kind, (data, url, sha) in sources.items()},
              "epub": {"url": epub_url, "sha256": digest(filename), "bytes": filename.stat().st_size,
                       "package_paths": paths, "member_matches_pinned_git_blob": matches},
              "views_equal": frozen_view == published_view, "frozen": frozen_view,
              "shipped": published_view}
    write_json(folder / "result.json", result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True)
    failed = False
    for book in PINS["books"]:
        try:
            with tempfile.TemporaryDirectory(prefix="af264-epub-") as temp:
                result = record(out, Path(temp), book)
            print(result["case"], result["views_equal"], result["epub"]["member_matches_pinned_git_blob"])
        except (ValueError, KeyError, OSError, ET.ParseError) as exc:
            write_json(out / book["slug"] / "error.json", {"status": "failed", "error": str(exc)})
            print(book["slug"], str(exc), file=sys.stderr)
            failed = True
    sys.exit(failed)
