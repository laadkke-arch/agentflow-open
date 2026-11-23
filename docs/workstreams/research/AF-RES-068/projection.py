"""Project pinned source to text and source offsets under the AF-RES-068 rules.

The Markdown/RST line projection follows the renderer at AF-RES-064
6341dce67a4dd4e38f68c2f16c9ae9f499b18f6f. Image and math omissions are counted.
"""
from dataclasses import dataclass, field
from html.parser import HTMLParser
import io
from pathlib import PurePosixPath
import re

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
    first: int
    last: int
    kind: str
    level: int = 0
    anchor: str = ""
    links: list[Link] = field(default_factory=list)
    images: int = 0
    math: int = 0


MARKDOWN = MarkdownIt("commonmark").enable(["table", "strikethrough"])
MATH = re.compile(r"(?<![\\$])(?:\$\$[\s\S]+?\$\$|\\\([\s\S]+?\\\)|\\\[[\s\S]+?\\\]|\$(?![\s$\d])[^$\n]+?(?<!\s)\$)(?!\w)")


class HtmlText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = ""
        self.images = 0
        self.math = 0
        self.links = []
        self.href = ""
        self.offset = 0
        self.hidden = None

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "img":
            self.images += 1
        if tag in {"script", "style", "math", "details"} and self.hidden is None:
            self.hidden = tag
            self.math += tag == "math"
        if tag == "a" and self.hidden is None:
            self.href = attrs.get("href", "")
            self.offset = len(self.text)
        if tag in {"p", "li", "br"} and self.text:
            self.text += "\n"

    def handle_endtag(self, tag):
        if tag == self.hidden:
            self.hidden = None
        elif tag == "a" and self.href:
            self.links.append(Link(self.text[self.offset:], self.href, len(self.text)))
            self.href = ""

    def handle_data(self, data):
        if self.hidden is None:
            self.text += data


def strip_math(text):
    return MATH.subn("", text)


def slug(label):
    return re.sub(r"[^\w -]", "", label.strip().lower()).replace(" ", "-")


def markdown_blocks(source):
    blocks = []
    heading_ids = set()
    level = 0
    for token in MARKDOWN.parse(source):
        if token.type == "heading_open":
            level = int(token.tag[1])
        elif token.type == "heading_close":
            level = 0
        if token.map is None:
            continue
        start, end = token.map
        if token.type in {"fence", "code_block"}:
            first = start + (2 if token.type == "fence" else 1)
            for no, line in enumerate(token.content.splitlines(), first):
                blocks.append(Block(line, no, no, "code"))
        elif token.type == "html_block":
            contents = HtmlText()
            contents.feed(token.content)
            blocks.append(Block(contents.text.strip("\n"), start + 1, end, "text",
                                links=contents.links, images=contents.images, math=contents.math))
        elif token.type == "inline":
            text = ""
            links = []
            images = math = 0
            href = ""
            link_start = 0
            for item in token.children or ():
                if item.type == "link_open":
                    href = item.attrGet("href")
                    link_start = len(text)
                elif item.type == "link_close":
                    if text[link_start:].strip():
                        links.append(Link(text[link_start:], href, len(text)))
                    href = ""
                elif item.type == "text":
                    line, omitted = strip_math(item.content)
                    text += line
                    math += omitted
                elif item.type == "code_inline":
                    text += item.content
                elif item.type in {"hardbreak", "softbreak"}:
                    text += "\n"
                elif item.type == "image":
                    images += 1
            anchor = ""
            if level and text.strip():
                anchor = base = slug(text)
                suffix = 1
                while anchor in heading_ids:
                    anchor = f"{base}-{suffix}"
                    suffix += 1
                heading_ids.add(anchor)
            if text.strip() or images or math:
                blocks.append(Block(text, start + 1, end, "heading" if level else "text",
                                    level, anchor, links, images, math))
    return blocks


def ancestors(node):
    while node.parent is not None:
        node = node.parent
        yield node


def rst_blocks(source):
    tree = publish_doctree(source, settings_overrides={
        "halt_level": 6, "warning_stream": io.StringIO(),
        "file_insertion_enabled": False, "raw_enabled": False,
        "syntax_highlight": "none",
    })
    blocks = []
    raw = source.splitlines()
    code_types = (nodes.literal_block, nodes.doctest_block)
    omissions = (nodes.image, nodes.math, nodes.math_block)
    for node in tree.findall():
        if not isinstance(node, (nodes.title, nodes.subtitle, nodes.paragraph, nodes.term,
                                 *code_types, *omissions)):
            continue
        parents = list(ancestors(node))
        if any(isinstance(p, (nodes.system_message, nodes.substitution_definition, nodes.footnote))
               for p in parents):
            continue
        line = node.line or next((p.line for p in parents if p.line), 1)
        if isinstance(node, omissions):
            if not isinstance(node.parent, nodes.paragraph):
                blocks.append(Block("", line, line, "text", images=isinstance(node, nodes.image),
                                    math=not isinstance(node, nodes.image)))
            continue
        text = node.astext()
        if isinstance(node, code_types):
            first = text.splitlines()[0].strip()
            candidates = [i for i, value in enumerate(raw, 1) if value.strip() == first]
            if candidates:
                line = min(candidates, key=lambda i: min(abs(i - line), abs(i + text.count("\n") + 1 - line)))
            for offset, code in enumerate(text.splitlines()):
                blocks.append(Block(code, line + offset, line + offset, "code"))
            continue
        images = math = 0
        for item in node.findall(lambda child: isinstance(child, omissions)):
            if item.astext():
                text = text.replace(item.astext(), "", 1)
            if isinstance(item, nodes.image):
                images += 1
            else:
                math += 1
        heading = isinstance(node, (nodes.title, nodes.subtitle))
        if heading:
            for i in range(max(0, line - 3), min(len(raw), line + 2)):
                if raw[i].strip() == text.strip():
                    line = i + 1
                    break
        links = []
        offset = 0
        for reference in node.findall(nodes.reference):
            label = reference.astext()
            pos = text.find(label, offset)
            uri = reference.get("refuri", "#" + reference["refid"] if reference.get("refid") else "")
            if uri and pos >= 0:
                offset = pos + len(label)
                links.append(Link(label, uri, offset))
        if text.strip() or images or math:
            level = 1 + sum(isinstance(p, nodes.section) for p in parents) if heading else 0
            ids = node.parent.get("ids", [])
            blocks.append(Block(text, line, line + text.count("\n"), "heading" if heading else "text",
                                level, ids[0] if heading and ids else "", links, images, math))
    return blocks


def source_blocks(path, source):
    suffix = PurePosixPath(path).suffix.lower()
    if suffix in {".md", ".markdown"}:
        return markdown_blocks(source)
    if suffix == ".rst":
        return rst_blocks(source)
    return [Block(line, no, no, "code") for no, line in enumerate(source.splitlines(), 1)]
