"""Parse only a requested source. Produce ordered, line-labelled reading windows."""

import re
from dataclasses import dataclass
from urllib.parse import urljoin

from lxml import etree, html

from source_io import WINDOW

BLOCKS = {"p", "li", "pre", "source", "dt", "dd", "td", "th", "blockquote"}
HEADS = {"h1", "h2", "h3", "h4", "h5", "h6"}
OMIT_TAGS = {"head", "nav", "script", "style", "figure"}
OMIT_IDS = {"toc", "respecHeader", "references"}


@dataclass(frozen=True)
class Block:
    line: int
    section: str
    words: tuple
    links: tuple


@dataclass(frozen=True)
class Window:
    start: int
    end: int
    section: str
    text: str
    links: tuple


def tag(element):
    return element.tag.split("}")[-1].lower() if isinstance(element.tag, str) else ""


def node_text(element):
    return " ".join("".join(element.itertext()).split())


def section_label(element):
    owners = [element, *element.iterancestors()]
    for ancestor in owners:
        if tag(ancestor) in {"section", "subsection"}:
            if ancestor.get("id"):
                return "#" + ancestor.get("id")
            if ancestor.get("name"):
                return ancestor.get("name")
    return "body"


def markup_blocks(raw, base):
    if raw.lstrip().lower().startswith(b"<!doctype html"):
        root = html.fromstring(raw)
    else:
        parser = etree.XMLParser(recover=True, resolve_entities=False, no_network=True)
        root = etree.fromstring(raw, parser)
    for element in root.iter():
        kind = tag(element)
        if kind not in BLOCKS | HEADS:
            continue
        if any(tag(parent) in OMIT_TAGS or parent.get("id") in OMIT_IDS for parent in element.iterancestors()):
            continue
        if kind in BLOCKS and any(tag(child) in BLOCKS for child in element.iterdescendants()):
            continue
        words = tuple(node_text(element).split())
        links = tuple(urljoin(base, child.get("href")) for child in element.iterdescendants()
                      if tag(child) == "a" and child.get("href"))
        if words:
            for offset in range(0, len(words), WINDOW):
                yield Block(element.sourceline or 1, section_label(element),
                            words[offset:offset + WINDOW], links)


def markdown_blocks(raw, base):
    section = "body"
    for number, line in enumerate(raw.decode("utf-8-sig").splitlines(), 1):
        if line.lstrip().startswith("#"):
            section = line.lstrip("# ").strip()
        if not line.strip() or not re.search(r"\w", line):
            continue
        source_links = re.findall(r'\]\(([^\s)]+)', line)
        links = tuple(urljoin(base, link) for link in source_links)
        line = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line)
        line = re.sub(r'<[^>]+>', ' ', line)
        words = tuple(line.lstrip("# ").split())
        for offset in range(0, len(words), WINDOW):
            yield Block(number, section, words[offset:offset + WINDOW], links)


def reading_windows(raw, url):
    parser = markdown_blocks if url.endswith(".md") else markup_blocks
    blocks = list(parser(raw, url))
    windows = []
    for start, first in enumerate(blocks):
        words = []
        links = []
        final = first
        for block in blocks[start:]:
            limit = WINDOW - len(words)
            if limit == 0 or block.section != first.section:
                break
            words.extend(block.words[:limit])
            if len(block.words) <= limit:
                links.extend(block.links)
            final = block
        if words:
            windows.append(Window(first.line, final.line, first.section, " ".join(words),
                                  tuple(dict.fromkeys(links))))
    return windows, sum(len(block.words) for block in blocks)
