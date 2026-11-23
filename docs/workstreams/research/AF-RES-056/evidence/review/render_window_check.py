"""Deterministically measure the fixed README's rendered-text window.

Audit receipts under evidence/review; measured excerpts under evidence/transient.
Does not edit root judgments. Uses preinstalled pandoc GFM -> HTML text nodes.
"""
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime, timezone
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
TASK = HERE.parents[1]
PROVIDER = TASK / "evidence/transient/sc032-build"
PIN = "d5199551f758ba067612979ae32ec35693640ccf"
COMMAND = ["pandoc", "--from=gfm", "--to=html5", "--wrap=none", "--no-highlight"]
BLOCKS = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "pre", "div", "section", "ul", "ol", "li", "blockquote", "table", "tr", "td", "th"}


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.started = False
        self.parts = []
        self.links = []
        self.anchor = None
        self.hidden = 0

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "h1" and not self.started:
            self.started = True
        if not self.started:
            return
        if tag in {"script", "style"}:
            self.hidden += 1
        if self.hidden:
            return
        if tag in BLOCKS or tag == "br":
            self.parts.append("\n")
        if tag == "a":
            self.anchor = {"url": attrs.get("href", ""), "visible_words_before": len("".join(self.parts).split()), "parts": []}

    def handle_endtag(self, tag):
        if not self.started:
            return
        if tag in {"script", "style"}:
            self.hidden = max(0, self.hidden - 1)
            return
        if self.hidden:
            return
        if tag == "a" and self.anchor is not None:
            self.anchor["label"] = " ".join("".join(self.anchor.pop("parts")).split())
            self.links.append(self.anchor)
            self.anchor = None
        if tag in BLOCKS:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.started and not self.hidden:
            self.parts.append(data)
            if self.anchor is not None:
                self.anchor["parts"].append(data)


def render(source):
    result = subprocess.run(COMMAND, input=source, text=True, capture_output=True, check=True)
    parser = VisibleText()
    parser.feed(result.stdout)
    return "".join(parser.parts).strip(), parser.links


def sha256(value):
    return hashlib.sha256(value).hexdigest()


content = subprocess.check_output(["git", "show", PIN + ":README.md"], cwd=PROVIDER)
source = content.decode()
full_visible, links = render(source)
tokens = list(re.finditer(r"\S+", full_visible))
window = full_visible[:tokens[499].end()]
window_file = TASK / "evidence/transient/SC-032-rendered-window-v2.txt"
window_file.write_text(window + "\n")
license_bytes = subprocess.check_output(["git", "show", PIN + ":LICENSE"], cwd=PROVIDER)
(HERE / "SC-032-rendered-window-LICENSE.txt").write_bytes(license_bytes)

old_window = (TASK / "evidence/transient/SC-032-window.txt").read_text().rstrip("\n")
old_rendered, old_links = render(old_window)
source_lines = source.splitlines()
prefix_counts = {}
for line in [99, 105, 106]:
    prefix_visible, _ = render("\n".join(source_lines[:line]))
    prefix_counts[str(line)] = len(prefix_visible.split())

original_first_links = json.loads((TASK / "evidence/windows/first-window-links.json").read_text())
first_links = [link for link in links if link["visible_words_before"] < 500][:3]
condition_tokens = {word: {"old_rendered": word.casefold() in old_rendered.casefold(), "new_rendered": word.casefold() in window.casefold()} for word in ["pii", "column_datatype", "enum", "missing_column"]}
receipt = {
    "reviewer": "/root/authority_records; within-team audit",
    "checked_utc": datetime.now(timezone.utc).isoformat(),
    "provider_sha": PIN,
    "source_url": "https://github.com/pboettch/json-schema-validator/blob/" + PIN + "/README.md",
    "canonical_source_git_blob": subprocess.check_output(["git", "rev-parse", PIN + ":README.md"], cwd=PROVIDER, text=True).strip(),
    "canonical_source_sha256": sha256(content),
    "renderer_version": subprocess.check_output(["pandoc", "--version"], text=True).splitlines()[0],
    "renderer_command": COMMAND,
    "text_extraction": "HTML text nodes from first h1; block boundaries are whitespace; no HTML/Markdown syntax, href target bytes, CSS, or initial status badge counted; code text counted. Not a browser layout observation.",
    "v1_raw_markdown_words": len(old_window.split()),
    "v1_raw_window_sha256_without_terminal_LF": sha256(old_window.encode()),
    "v1_rendered_visible_words": len(old_rendered.split()),
    "v2_visible_words": len(window.split()),
    "v2_window_sha256_without_terminal_LF": sha256(window.encode()),
    "v2_window_file_sha256_with_terminal_LF": sha256(window_file.read_bytes()),
    "v2_source_line_start": 3,
    "v2_source_line_end": 106,
    "v2_last_visible_word": window.split()[-1],
    "prefix_rendered_word_counts_by_source_final_line": prefix_counts,
    "first_three_links_in_v2": first_links,
    "first_two_destination_urls_unchanged": [x["url"] for x in first_links[:2]] == [x["url"] for x in original_first_links[:2]],
    "conditions_token_search_not_semantic_proof": condition_tokens,
    "reviewed_added_content": "Only the static/shared-library default and CMake shared-library option, then the first word of the Windows linking paragraph, are added at the boundary. They do not establish JS-4 C1, C2, a Python environment, or an exact release version.",
    "C1_v1": "미확인",
    "C2_v1": "미확인",
    "C1_v2": "미확인",
    "C2_v2": "미확인",
    "combined_changed": False,
    "chronology": "Computed after provider diagnostic exposure. This corrects the raw-Markdown extraction against the already specified rendered-text rule; it is not an unexposed predeclared new observation. Preserve v1 and report both.",
    "license": {"source_url": "https://github.com/pboettch/json-schema-validator/blob/" + PIN + "/LICENSE", "name": "MIT", "copyright": "Copyright (c) 2016 Patrick Boettcher", "notice_file": "SC-032-rendered-window-LICENSE.txt", "license_sha256": sha256(license_bytes)},
}
assert receipt["v2_visible_words"] == 500
assert receipt["first_two_destination_urls_unchanged"]
assert prefix_counts["105"] < 500 <= prefix_counts["106"]
out = HERE / "SC-032-rendered-window-v2.json"
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"receipt": str(out), "window_file": str(window_file), "v1_raw_words": receipt["v1_raw_markdown_words"], "v1_visible_words": receipt["v1_rendered_visible_words"], "v2_visible_words": receipt["v2_visible_words"], "source_end_line": 106, "last_word": receipt["v2_last_visible_word"], "first_two_links_unchanged": receipt["first_two_destination_urls_unchanged"], "classification_changed": receipt["combined_changed"]}, ensure_ascii=False))

# The root supplied the complete text of the same previously read live response.
# Homepage text remains transient: permanent evidence records measurements only.
homepage_input = TASK / "evidence/transient/home-parsed-full.json"
if homepage_input.exists():
    home_source_bytes = homepage_input.read_bytes()
    home_source = json.loads(home_source_bytes)
    home_lines = home_source["lines"]
    home_markdown = "\n".join(row["text"] for row in home_lines)
    home_visible, _ = render(home_markdown)
    home_tokens = list(re.finditer(r"\S+", home_visible))
    home_window = home_visible[:home_tokens[499].end()]
    home_original = (TASK / "evidence/transient/SC-032-home-window.txt").read_text().rstrip("\n")
    old_home_visible, _ = render(home_original)
    raw_home_tokens = list(re.finditer(r"\S+", home_markdown))
    recovered_original = home_markdown[:raw_home_tokens[499].end()]
    assert recovered_original == home_original, "Supplied page snapshot differs from the original raw 500-word extraction."

    low, high = 1, len(home_lines)
    while low < high:
        middle = (low + high) // 2
        text, _ = render("\n".join(row["text"] for row in home_lines[:middle]))
        if len(text.split()) >= 500:
            high = middle
        else:
            low = middle + 1
    end_index = low
    preceding, _ = render("\n".join(row["text"] for row in home_lines[:end_index - 1]))
    through_end, _ = render("\n".join(row["text"] for row in home_lines[:end_index]))
    end_line = home_lines[end_index - 1]["line"]
    home_out = TASK / "evidence/transient/SC-032-home-rendered-window-v2.txt"
    home_out.write_text(home_window + "\n")
    home_receipt = {
        "reviewer": "/root/authority_records; within-team audit",
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "original_url": home_source["original_url"],
        "final_url": "https://json-schema.org/",
        "web_ref": home_source["web_ref"],
        "source_snapshot": "Original web response supplied by root, lines6-185; no new live page substituted.",
        "source_snapshot_json_sha256": sha256(home_source_bytes),
        "source_plain_markdown_sha256_without_terminal_LF": sha256(home_markdown.encode()),
        "source_raw_words": len(home_markdown.split()),
        "v1_raw_window_recovered_exactly": recovered_original == home_original,
        "v1_raw_window_sha256_without_terminal_LF": sha256(home_original.encode()),
        "v1_raw_words": len(home_original.split()),
        "v1_rendered_visible_words": len(old_home_visible.split()),
        "v2_visible_words": len(home_window.split()),
        "v2_window_sha256_without_terminal_LF": sha256(home_window.encode()),
        "v2_window_file_sha256_with_terminal_LF": sha256(home_out.read_bytes()),
        "v2_source_start_line": 6,
        "v2_source_end_line": end_line,
        "v2_last_visible_word": home_window.split()[-1],
        "preceding_source_line_word_count": {"line": home_lines[end_index - 2]["line"], "words": len(preceding.split())},
        "through_last_source_line_word_count": {"line": end_line, "words": len(through_end.split())},
        "renderer_version": receipt["renderer_version"],
        "renderer_command": COMMAND,
        "text_extraction": receipt["text_extraction"],
        "input_limit": "Source is tool-parsed page text with original link wrappers already removed by root, not a recovered browser DOM or layout. Only Markdown control syntax is removed here.",
        "C1_v1": "미확인", "C2_v1": "미확인", "C1_v2": "미확인", "C2_v2": "미확인",
        "combined_changed": False,
        "implementation_specific_evidence": False,
        "reviewed_added_content": "The boundary adds upcoming community office-hours entries for December29,2026 and January5,2027. It contains no SC-032 implementation version, dynamic pii relation, or column_datatype enumeration.",
        "chronology": "Post-observation mechanical correction of the specified rendered-text boundary. Preserve original raw-Markdown window and both measurements; no third user action or new live response.",
        "copyright_retention": "Full text and 500-word extract remain evidence/transient only. Permanent audit contains hashes, counts, positions, own summary, and one boundary word.",
    }
    assert len(home_window.split()) == 500
    assert len(preceding.split()) < 500 <= len(through_end.split())
    home_receipt_path = HERE / "SC-032-home-rendered-window-v2.json"
    home_receipt_path.write_text(json.dumps(home_receipt, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"receipt": str(home_receipt_path), "v1_raw_words": len(home_original.split()), "v1_visible_words": len(old_home_visible.split()), "v2_words": 500, "source_end_line": end_line, "last_word": home_window.split()[-1], "added_boundary_words_for_reviewer": home_window.split()[len(old_home_visible.split()):], "classification_changed": False}, ensure_ascii=False))
