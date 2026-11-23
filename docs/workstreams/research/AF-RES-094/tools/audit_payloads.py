"""Audit fixed sources, response/inline fingerprints, and published packages offline."""
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import sys
from tarfile import open as open_tar
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile

from lxml import etree, html
from PIL import Image

from inspect_response import embedded_blob, find_p1_minmal, tree

source_cache, main_cache, destination = map(Path, sys.argv[1:4])


def raw(key, work=source_cache):
    return (work / (key + ".body")).read_bytes()


def digest(body):
    return {"bytes": len(body), "sha256": sha256(body).hexdigest()}


def xml(body):
    return etree.fromstring(body, parser=etree.XMLParser(no_network=True, resolve_entities=False))


def compare(key, ref):
    body = raw(key, main_cache)
    blob, file, commit = embedded_blob(tree(body))
    restored = "\n".join(blob["rawLines"]).encode()
    original = raw(ref)
    return {"receipt_id": key, "fixed_file_id": ref, "commit": commit, "file": file, "wrapper": digest(body),
            "raw_lines": digest(restored), "raw_file": digest(original),
            "equal_after_removing_final_lfs_from_raw": original.rstrip(b"\n") == restored,
            "n_final_lfs_in_original": len(original) - len(original.rstrip(b"\n"))}


wrappers = [compare(case + "-" + card + "-" + client + "-1", ref)
            for case, ref in (("P1-next", "P1-CONFIG-RAW"), ("R1-next", "R1-DOC"))
            for card in "AB" for client in ("browser", "http")]
wrappers.extend(compare("R2-blob-primary-" + client + "-1", "R2-DOC") for client in ("browser", "http"))

minmal_file = raw("P1-CONFIG-RAW")
minmal = find_p1_minmal(tree(b"<html/>"), minmal_file).encode()
doc = raw("R2-DOC")
section = doc.split(b'id="using-svg-files"', 1)[1].split(b'<h2 id="showing-the-code"', 1)[0]
pres = re.findall(rb"<pre\b[^>]*>.*?</pre>", section, re.S)
fragment = tree(b"<section><h2 " + b'id="using-svg-files"' + section + b"</section>")
output_pres = [digest(el) for el in pres if el.startswith(b"<pre>\n##")]
assert output_pres[0]["sha256"] == "64eb0d80bae83cc4b40efc545937d1ea82807edffce84f750f781d0a470fd376"
section_hrefs = fragment.xpath(".//a/@href")
assert all(not (".cast" in href or ".svg" in href) for href in section_hrefs)


def svg_details(data):
    root = xml(data)
    text = root.xpath('//*[local-name()="text"]/text()')
    joined = " ".join(text)
    return {**digest(data), "root_tag": root.tag, "width": root.get("width"), "height": root.get("height"),
            "contains_title": "TITLE" in joined, "contains_example_expression": 'cli::rule(center = "TITLE"' in joined,
            "counts": {tag: len(root.xpath('//*[local-name()=$tag]', tag=tag))
                       for tag in ("animate", "animateTransform", "set", "script", "text")},
            "has_css_keyframes": b"@keyframes" in data, "has_animation_rule": bool(re.search(rb"animation(?:-name)?:", data))}


def cast_details(data):
    header, *events = map(json.loads, data.splitlines())
    return {**digest(data), "header_version": header["version"], "width": header["width"], "height": header["height"],
            "events": len(events), "type_set": sorted({row[1] for row in events}),
            "first_timestamp": events[0][0], "last_timestamp": events[-1][0]}


def tar_members(archive, files):
    mapped = {}
    with open_tar(fileobj=BytesIO(raw(archive)), mode="r:gz") as package:
        for member in package.getmembers():
            relative = member.name.split("/", 1)[-1]
            if relative in files and member.isfile():
                mapped[relative] = digest(package.extractfile(member).read())
    return mapped


figure_root = "articles/asciicast-demo_files/figure-html/"
candidates = {figure_root + f"unnamed-chunk-{n}.svg": svg_details(raw(f"R2-CANDIDATE-{n}")) for n in (6, 7)}
tar_files = tar_members("R2-GENERATED-TAR", {*candidates, "articles/asciicast-demo.html"})
for name, details in candidates.items():
    assert details["sha256"] == tar_files[name]["sha256"]
    details["in_frozen_html_href_src_or_data"] = name.split("/")[-1] in doc.decode("utf-8")
    assert not details["in_frozen_html_href_src_or_data"]

manifest_data = raw("IIIF-BOOK-RAW")
manifest = json.loads(manifest_data)
canvas = manifest["items"][1]
annotation = canvas["items"][0]["items"][0]
iiif = {"manifest": digest(manifest_data), "manifest_id": manifest["id"], "presentation_context": manifest["@context"],
        "canvas_count": len(manifest["items"]), "p2": {k: canvas[k] for k in ("id", "type", "label", "width", "height")},
        "motivation": annotation["motivation"], "target": annotation["target"], "painting_body": annotation["body"],
        "target_equals_embedded_canvas_id": annotation["target"] == canvas["id"],
        "canvas_description_additional_web_reads": 0, "painting_body_original_bytes": None}

epub_data = raw("EPUB-BOOK")
with ZipFile(BytesIO(epub_data)) as package:
    files = {m.filename for m in package.infolist() if not m.is_dir()}
    container_name = "META-INF/container.xml"
    container = xml(package.read(container_name))
    opf_name = container.xpath('//*[local-name()="rootfile"]/@full-path')[0]
    opf = xml(package.read(opf_name))
    items = {el.get("id"): el for el in opf.xpath('//*[local-name()="manifest"]/*[local-name()="item"]')}
    spine = opf.xpath('//*[local-name()="spine"]/*[local-name()="itemref"]/@idref')
    external = {identifier: item.get("href") for identifier, item in items.items() if urlsplit(item.get("href")).scheme}
    flags = {identifier: item.get("properties") for identifier, item in items.items()
             if "remote-resources" in item.get("properties", "").split()}

    def relative(parent, target):
        return posixpath.normpath(posixpath.join(str(PurePosixPath(parent).parent), unquote(urlsplit(target).path)))

    matched = {identifier: relative(opf_name, item.get("href")) for identifier, item in items.items() if identifier not in external}
    cover_id, cover_item = next((identifier, item) for identifier, item in items.items()
                               if "cover-image" in item.get("properties", "").split())
    cover_doc_name = next(name for name in files if name.endswith("/cover.xhtml"))
    cover_doc = xml(package.read(cover_doc_name))
    cover_refs = cover_doc.xpath('//*[local-name()="image"]/@*[local-name()="href"] | //*[local-name()="img"]/@src')
    cover_path = matched[cover_id]
    cover = package.read(cover_path)
    with Image.open(BytesIO(cover)) as image:
        image.verify()
        cover_image = {"format": image.format, "size": image.size, **digest(cover)}
    links = []
    for name in sorted(files):
        if not name.endswith((".html", ".xhtml")):
            continue
        page = xml(package.read(name))
        links.extend({"path": name, "url": href} for href in page.xpath('//*[local-name()="a"]/@href')
                     if urlsplit(href).scheme in ("https", "http"))
    epub = {"package": digest(epub_data), "declared_epub_version": opf.get("version"),
            "entries_including_directories": len(package.namelist()), "file_count": len(files),
            "mime_entry": package.read("mimetype").decode(), "container": container_name, "opf": opf_name,
            "title": opf.xpath('//*[local-name()="title"]/text()')[0],
            "unique_identifier": opf.get("unique-identifier"), "modified": opf.xpath('//*[local-name()="meta" and @property="dcterms:modified"]/text()'),
            "manifest_items": len(items), "manifest_local_found": sum(name in files for name in matched.values()),
            "spine_count": len(spine), "spine_items_found": sum(idref in matched and matched[idref] in files for idref in spine),
            "manifest_remote_href": external, "manifest_remote_resource_flags": flags,
            "cover_id": cover_id, "declared_cover_mime": cover_item.get("media-type"),
            "cover_document": cover_doc_name, "cover_document_refs": cover_refs,
            "cover_ref_matches_image": any(relative(cover_doc_name, ref) == cover_path for ref in cover_refs),
            "cover_member": cover_path, "cover_image": cover_image, "xhtml_external_anchors": links,
            "web_resource_downloads_for_cover": 1, "zip_files_used_for_cover_path": [container_name, opf_name, cover_doc_name, cover_path]}
with ZipFile(BytesIO(raw("R1-ARCHIVE-DATA"))) as archive:
    archive_members = [m.filename for m in archive.infolist()]

evidence = {
    "wrappers": wrappers,
    "p1_first_minmal": {"without_trailing_lf": digest(minmal), "with_single_trailing_lf": digest(minmal + b"\n"),
                        "shown_master": "https://pypi.org", "preflight_plain_blob": digest(raw("CTRL-BLOB-RAW"))},
    "pypi_soft_failure": {"title": html.fromstring(raw("PYPI-SEARCH-RESPONSE")).xpath("string(//title)").strip(),
                          **digest(raw("PYPI-SEARCH-RESPONSE")), "source_receipt": "sources/http-supplement.json"},
    "archive_zip_members": archive_members,
    "r2_using_svg": {"chosen_static_pre": output_pres, "all_pre_count": len(pres), "hrefs": section_hrefs,
                     "src_or_data_attrs": fragment.xpath(".//@src | .//@data"),
                     "inline_svg_or_script_count": len(fragment.xpath(".//svg | .//script | .//asciinema-player")),
                     "fixed_svg_candidates": candidates, "tar_check": tar_files,
                     "different_svg_fixture": svg_details(raw("R2-SVG-EXAMPLE")),
                     "different_cast_fixture": cast_details(raw("R2-CAST-EXAMPLE"))},
    "iiif_0009": iiif, "epub_published_package": epub,
}
destination.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: evidence[k] for k in ("p1_first_minmal", "pypi_soft_failure", "r2_using_svg", "iiif_0009", "epub_published_package")},
                 ensure_ascii=False, indent=2))
