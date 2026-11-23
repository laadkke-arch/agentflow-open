"""Extract bounded evidence from a response without executing its scripts."""
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from lxml import etree, html


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def clip(value, size=300):
    return " ".join(value.split())[:size]


def tree(raw):
    return html.fromstring(raw, parser=html.HTMLParser(encoding="utf-8"))


def labelled_section(document, ident):
    matches = document.xpath('//*[@id=$ident]', ident=ident)
    if not matches:
        return []
    heading = matches[0]
    if heading.tag not in ("h1", "h2", "h3", "h4") or heading.xpath("./pre | ./table"):
        return [heading]
    blocks = [heading]
    for sibling in heading.itersiblings():
        if sibling.tag in ("h1", "h2", "h3", "h4") and sibling.tag <= heading.tag:
            break
        blocks.append(sibling)
    return blocks


def inside(blocks, xpath):
    return [node for block in blocks for node in block.xpath(xpath)]


def uri_entries(document, base):
    return [{"href": urljoin(base, href), "label": clip(anchor.text_content(), 75)}
            for anchor in document.xpath("//a[@href]")
            if (href := anchor.get("href"))]


def embedded_blob(document):
    for script in document.xpath('//script[@data-target="react-app.embeddedData"]'):
        try:
            payload = json.loads(script.text or "").get("payload", {})
        except (json.JSONDecodeError, AttributeError):
            continue
        blob = payload.get("blob", {})
        if blob:
            return blob, payload.get("path"), (payload.get("refInfo") or {}).get("currentOid")
        layout = payload.get("codeViewBlobLayoutRoute", {})
        if layout.get("blob"):
            styled = payload.get("codeViewBlobLayoutRoute.StyledBlob", {})
            view = payload.get("codeViewBlobRoute", {})
            blob = layout["blob"] | {"rawLines": styled.get("rawLines"), "richText": view.get("richText")}
            return blob, layout.get("path"), (layout.get("refInfo") or {}).get("currentOid")
    return {}, None, None


def find_p1_minmal(document, source):
    if source:
        markdown = source.decode("utf-8", errors="replace")
        match = re.search(r"(?ims)^#{2,6}\s+Minmal\s*$.*?^\x60{3}[^\r\n]*\r?\n(.*?)^\x60{3}", markdown)
        if match:
            return match.group(1).strip()
    blocks = labelled_section(document, "minmal") or labelled_section(document, "user-content-minmal")
    pre = inside(blocks, "self::pre | .//pre")
    if not pre and blocks:
        # GitHub can render a heading and its anchor inside a wrapper div.
        anchor = blocks[0]
        for sibling in anchor.getparent().itersiblings():
            if sibling.xpath("./h2 | ./h3 | ./h4 | self::h2 | self::h3 | self::h4"):
                break
            if block := sibling.xpath("self::pre | .//pre"):
                pre = block
                break
    return pre[0].text_content().strip() if pre else ""


def inspect(raw, url, purpose, mime):
    result = {"kind": "empty_or_unavailable", "title": "", "candidates": []}
    if not raw:
        return result
    try:
        document = tree(raw)
    except (etree.ParserError, ValueError):
        return result | {"kind": "non_html", "sample": clip(raw[:600].decode("utf-8", "replace"))}
    title = clip(" ".join(document.xpath("//title/text()")))
    result |= {"kind": "rendered_document", "title": title,
               "headings": [clip(node.text_content(), 90) for node in document.xpath("//h1 | //h2")][:12]}
    if "html" not in mime.lower():
        result |= {"kind": "plain_or_non_html", "sample": clip(raw[:600].decode("utf-8", "replace"))}
    errors = re.compile(r"page not found|site not found|service unavailable|unicorn!|access denied|request forbidden|bad gateway|not allowed|blocked by|couldn.t find the file", re.I)
    prominent = title + " " + " ".join(result["headings"][:5])
    if errors.search(prominent):
        result["kind"] = "error_document"
    result["quoted_sample"] = clip(" ".join(document.xpath("//h1//text() | //h2//text() | //body/p//text()")), 170)
    blob, file, ref = embedded_blob(document) if urlsplit(url).hostname == "github.com" else ({}, None, None)
    source = None
    if blob:
        lines = blob.get("rawLines")
        if isinstance(lines, list) and all(isinstance(value, str) for value in lines):
            source = "\n".join(lines).encode()
        rich_text = blob.get("richText")
        if isinstance(rich_text, str) and "<" in rich_text:
            result["rich_text_sha256"] = sha256(rich_text.encode())
            rich = tree(rich_text.encode())
        else:
            rich = document
        result |= {
            "kind": "github_markdown_wrapper" if str(file or urlsplit(url).path).endswith(".md") else "github_source_wrapper",
            "file": file, "commit": ref, "blob_truncated": blob.get("truncated"), "blob_line_count": len(lines) if isinstance(lines, list) else None,
            "wrapper_kept": True, "restored_sha256": sha256(source) if source else None,
            "restored_plus_lf_sha256": sha256(source + b"\n") if source and not source.endswith(b"\n") else None,
            "restored_bytes": len(source) if source else None,
        }
    else:
        rich = document

    if purpose == "P1-next" and "bandersnatch" in url:
        code = find_p1_minmal(rich, source)
        master = re.search(r"(?m)^master\s*=\s*(https?://\S+)\s*$", code)
        result |= {"minmal_sha256": sha256(code.encode()) if code else None, "minmal_bytes": len(code.encode()),
                   "minmal_settings": dict(re.findall(r"(?m)^(master|workers|timeout|global-timeout|directory)\s*=\s*([^\r\n]+)", code))}
        if master:
            uri = master.group(1)
            active = any(lnk["href"].rstrip("/") == uri.rstrip("/") for lnk in uri_entries(rich, url))
            result["candidates"] = [{"href": uri, "label": "Minmal · master", "type": "href" if active else "literal"}]
    elif purpose == "P1-next" and urlsplit(url).hostname in ("pypi.org", "www.pypi.org"):
        result["service_markers"] = [s for s in ("Python Package Index", "PyPI", "Search projects") if s.lower() in clip(document.text_content(), 8000).lower()]

    if purpose.startswith("R1") and "archive" in url:
        content = tree(source) if source and result["kind"] == "github_source_wrapper" else document
        usage = labelled_section(content, "ref-usage")
        examples = labelled_section(content, "ref-examples")
        text = " ".join(el.text_content() for el in examples)
        link = "https://rdrr.io/r/base/system.file.html"
        hrefs = inside(examples, ".//a/@href")
        result |= {"usage_has_archive_read": any("archive_read" in el.text_content() for el in usage),
                   "examples_has_system_file": "system.file" in text, "examples_href": hrefs[:12],
                   "archive_version_marker": ("1.1.12" if "1.1.12" in content.text_content() else None)}
        if link in hrefs:
            result["candidates"] = [{"href": link, "label": "Examples · system.file",
                                    "type": "literal" if content is not document else "href"}]
    elif purpose.startswith("R1") and urlsplit(url).hostname == "rdrr.io":
        result["system_file_markers"] = [s for s in ("system.file", "Find Names of R System Files", "package") if s.lower() in clip(document.text_content(), 21000).lower()]

    if purpose.startswith("P3") and "cibuildwheel" in url:
        enable = labelled_section(document, "enable")
        legacy = labelled_section(document, "what-does-it-do")
        current_text = " ".join(el.text_content() for el in enable)
        table = inside(legacy, "self::table | .//table")
        result |= {"enable_excerpt": clip(current_text, 185), "enable_markers": [s for s in
                    ("cpython-freethreading", "3.13", "3.14") if s in current_text],
                   "legacy_tables": [clip(el.text_content(), 240) for el in table],
                   "legacy_identifier_markers": [s for s in ("cp27", "pp27") if s in document.text_content()]}
        for link in uri_entries(document, url):
            if urlsplit(link["href"]).hostname == "cibuildwheel.pypa.io" and "/en/1.x/" in link["href"]:
                link["type"] = "href"
                result["candidates"].append(link)

    if purpose.startswith("R2") and "asciicast" in url:
        content = tree(source) if source and result["kind"] == "github_source_wrapper" else document
        blocks = labelled_section(content, "using-svg-files")
        pres = inside(blocks, "self::pre | .//pre")
        rendered = [obj.text_content().strip("\n") for obj in pres]
        hrefs = inside(blocks, ".//a/@href")[:18]
        attrs = inside(blocks, ".//@src | .//@data")
        inline_body = [el.tag for el in inside(blocks, ".//svg | .//asciinema-player | .//script")]
        result |= {"asciicast_version_marker": ("2.3.1" if "2.3.1" in content.text_content() else None),
                   "selected_section_seen": bool(blocks), "section_hrefs": hrefs, "section_src_or_data": attrs,
                   "section_svg_player_script_elements": inline_body,
                   "pre_fingerprints": [{"bytes": len(s.encode()), "sha256": sha256(s.encode()),
                                          "kind": "option_code" if "asciicast_knitr_output" in s else "preformatted"} for s in rendered]}
        result["candidates"] = [{"href": urljoin(url, link), "label": "Using SVG files · payload", "type": "href"}
                                for link in hrefs + attrs if re.search(r"\.(svg|cast)(?:[?#]|$)", link, re.I)]

    if purpose.startswith("control"):
        text = clip(document.text_content(), 2500)
        result["control_markers"] = [s for s in ("Hello World!", "The Python Package Index", "pip install", "Page not found", "Example Domains", "Forbidden") if s.lower() in text.lower()]
    return result


if __name__ == "__main__":
    mode, path, url, purpose, mime = sys.argv[1:]
    result = inspect(Path(path).read_bytes(), url, purpose, mime)
    print(json.dumps(result, ensure_ascii=False))
