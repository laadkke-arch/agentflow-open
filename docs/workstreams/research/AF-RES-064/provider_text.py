"""Project pinned public source into ordered text blocks and link/heading metadata."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import time
from urllib.parse import quote
from urllib.request import Request, urlopen

from docutils import nodes
from docutils.core import publish_doctree
from markdown_it import MarkdownIt


@dataclass
class Link:
    label: str
    href: str
    end: int


@dataclass
class Block:
    text: str
    start: int
    end: int
    kind: str
    level: int = 0
    anchor: str = ""
    links: list[Link] = field(default_factory=list)


def urls(doc):
    stem = f"{doc['repo']}/{doc['ref']}/{quote(doc['path'], safe='/')}"
    return (
        f"https://github.com/{doc['repo']}/blob/{doc['ref']}/{quote(doc['path'], safe='/')}",
        f"https://raw.githubusercontent.com/{stem}",
    )


def document_bytes(doc, cache):
    _, url = urls(doc)
    key = hashlib.sha256(url.encode()).hexdigest()
    file = cache / key
    receipt = cache / (key + ".json")
    cache.mkdir(parents=True, exist_ok=True)
    if file.exists():
        data = file.read_bytes()
        result = json.loads(receipt.read_bytes())
        if hashlib.sha256(data).hexdigest() != result["raw_sha256"]:
            raise ValueError(f"Damaged local cache: {url}")
        return data, result
    attempts = []
    for delay in (0, 1, 2):
        time.sleep(delay)
        stamp = datetime.now(timezone.utc).isoformat()
        try:
            with urlopen(Request(url, headers={"User-Agent": "AF-RES-064 pinned text replay"}), timeout=20) as response:
                data = response.read()
                attempts.append({"utc": stamp, "status": response.status, "url": response.geturl()})
            break
        except OSError as error:
            attempts.append({"utc": stamp, "error": str(error), "url": url})
    else:
        receipt.write_text(json.dumps(attempts, ensure_ascii=False) + "\n", encoding="utf-8")
        raise OSError(f"Document request failed: {url}: {attempts}")
    result = {
        "raw_url": url, "raw_sha256": hashlib.sha256(data).hexdigest(),
        "raw_bytes": len(data), "attempts": attempts,
    }
    file.write_bytes(data)
    receipt.write_text(json.dumps(result, ensure_ascii=False) + "\n", encoding="utf-8")
    return data, result


class RawHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = ""
        self.links = []
        self.href = ""
        self.begin = 0
        self.level = 0
        self.anchor = ""

    def handle_starttag(self, tag, attribute_pairs):
        attrs = dict(attribute_pairs)
        if tag in {"p", "li", "br"}:
            self.text += "\n"
        if tag == "a":
            self.href = attrs.get("href", "")
            self.begin = len(self.text)
        if re.fullmatch(r"h[1-6]", tag):
            self.level = int(tag[1:])
            self.anchor = attrs.get("id", "")

    def handle_endtag(self, tag):
        if tag == "a" and self.href:
            self.links.append(Link(self.text[self.begin:], self.href, len(self.text)))
            self.href = ""

    def handle_data(self, text):
        self.text += text


def slug(label):
    return re.sub(r"[^\w\s-]", "", label.lower()).replace(" ", "-")


def markdown_blocks(source):
    parser = MarkdownIt("commonmark").enable(["table", "strikethrough"])
    blocks = []
    heading_ids = set()
    level = 0
    for token in parser.parse(source):
        if token.type == "heading_open":
            level = int(token.tag[1:])
            continue
        if token.type == "heading_close":
            level = 0
            continue
        if not token.map:
            continue
        start, end = token.map
        if token.type in {"fence", "code_block"}:
            line = start + 2 if token.type == "fence" else start + 1
            for item in token.content.splitlines():
                blocks.append(Block(item, line, line, "code"))
                line += 1
        elif token.type == "html_block":
            html = RawHTML()
            html.feed(token.content)
            if html.text.strip():
                blocks.append(Block(html.text, start + 1, end, "heading" if html.level else "text",
                                    html.level, html.anchor, html.links))
        elif token.type == "inline":
            text = ""
            links = []
            href = ""
            link_start = 0
            for item in token.children or ():
                if item.type == "link_open":
                    href = item.attrGet("href")
                    link_start = len(text)
                elif item.type == "link_close":
                    links.append(Link(text[link_start:], href, len(text)))
                    href = ""
                elif item.type in {"text", "code_inline"}:
                    text += item.content
                elif item.type in {"hardbreak", "softbreak"}:
                    text += "\n"
                elif item.type == "html_inline":
                    html = RawHTML()
                    html.feed(item.content)
                    text += html.text
                # Image pixels and badge alt text are outside the text projection.
            if not text.strip():
                continue
            level_here = level
            anchor = ""
            if level_here:
                base = slug(text)
                anchor = base
                suffix = 1
                while anchor in heading_ids:
                    anchor = f"{base}-{suffix}"
                    suffix += 1
                heading_ids.add(anchor)
            blocks.append(Block(text, start + 1, end, "heading" if level_here else "text", level_here, anchor, links))
    return blocks


def rst_blocks(source):
    import io

    tree = publish_doctree(source, settings_overrides={"halt_level": 6, "warning_stream": io.StringIO(),
                                                       "file_insertion_enabled": False, "raw_enabled": False})
    visited = []
    kinds = (nodes.title, nodes.subtitle, nodes.paragraph, nodes.literal_block, nodes.term)
    for node in tree.findall():
        if not isinstance(node, kinds) or isinstance(node.parent, (nodes.system_message, nodes.footnote)):
            continue
        if any(isinstance(parent, (nodes.system_message, nodes.substitution_definition))
               for parent in ancestors(node)):
            continue
        text = node.astext()
        if not text.strip():
            continue
        parents = list(ancestors(node))
        reference_links = []
        offset = 0
        for ref in node.findall(nodes.reference):
            label = ref.astext()
            pos = text.find(label, offset)
            path = ref.get("refuri") or ("#" + ref["refid"] if ref.get("refid") else "")
            if path and pos >= 0:
                offset = pos + len(label)
                reference_links.append(Link(label, path, offset))
        line = node.line or next((parent.line for parent in parents if parent.line), 1)
        heading = isinstance(node, (nodes.title, nodes.subtitle))
        level = 1 + sum(isinstance(parent, nodes.section) for parent in parents) if heading else 0
        kind = "heading" if heading else "code" if isinstance(node, nodes.literal_block) else "text"
        if heading:
            lines = source.splitlines()
            for candidate in range(max(0, line - 3), min(len(lines), line + 2)):
                if lines[candidate].strip() == text.strip():
                    line = candidate + 1
                    break
        if kind == "code":
            lines = source.splitlines()
            first = text.splitlines()[0].strip()
            for candidate in range(max(0, line - 4), min(len(lines), line + 3)):
                if lines[candidate].strip() == first:
                    line = candidate + 1
                    break
        ids = node.parent.get("ids", [])
        visited.append(Block(text, line, line + text.count("\n"), kind, level,
                             ids[0] if level and ids else "", reference_links))
    return visited


def ancestors(node):
    while node.parent is not None:
        node = node.parent
        yield node


def read_blocks(doc, cache):
    data, receipt = document_bytes(doc, cache)
    source = data.decode("utf-8-sig")
    suffix = Path(doc["path"]).suffix.lower()
    if suffix in {".md", ".markdown"}:
        blocks = markdown_blocks(source)
    elif suffix == ".rst":
        blocks = rst_blocks(source)
    else:
        blocks = [Block(line, i, i, "code") for i, line in enumerate(source.splitlines(), 1)]
    if not blocks:
        raise ValueError(f"No readable blocks for {doc}")
    return blocks, receipt
