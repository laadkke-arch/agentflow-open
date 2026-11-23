#!/usr/bin/env python3
"""Extract frozen question snippets; never fetch, normalize, repair, or execute them."""
import argparse
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXECUTION = ROOT / "execution"
PRE = re.compile(r"<pre\b[^>]*>\s*<code\b[^>]*>(.*?)</code>\s*</pre>", re.S)
CASES = {
    "JN1": "78253195", "JN2": "78262117", "JE1": "78296361", "JE2": "78305924",
    "PN1": "78258237", "PN2": "78267487", "PE1": "78300525", "PE2": "78461996",
}
# Names describe evidence roles, not executable programs or verified solutions.
BLOCKS = {
    ("JN1", "R0"): [("input_fragment01.txt", "incomplete JSON and prose"), ("map_attempt_note.txt", "prose"), ("input_fragment02.txt", "incomplete JSON")],
    ("JN1", "R1"): [("attempted_query01.txt", "unexecuted original shell command"), ("input_fragment01.txt", "incomplete JSON"), ("attempted_query02.txt", "unexecuted original shell command"), ("input_fragment02.txt", "incomplete JSON"), ("weather.json", "complete JSON input")],
    ("JN2", "R0"): [("attempt_and_error.txt", "original shell command and reported diagnostic"), ("helm_chart.yaml", "complete shown YAML input")],
    ("JN2", "R1"): [("attempt_and_error.txt", "original shell command and reported diagnostic"), ("helm_chart.yaml", "complete shown YAML input")],
    ("JE1", "R0"): [("mixed_example.txt", "Python, JSON input, observed and desired Document representations; not executable Python")],
    ("JE1", "R1"): [("mixed_example.txt", "Python, JSON input, observed Document representations; not executable Python"), ("desired_documents.txt", "desired Document representations")],
    ("JE2", "R0"): [("input_with_ellipsis.json.txt", "incomplete JSON; literal .... retained"), ("desired_with_ellipsis.jsonl.txt", "desired JSON Lines with literal .... retained"), ("attempted_queries.txt", "unexecuted original shell commands")],
    ("JE2", "R1"): [("input_with_ellipsis.json.txt", "incomplete JSON; literal .... retained"), ("desired_with_ellipsis.jsonl.txt", "desired JSON Lines with literal .... retained"), ("attempted_queries.txt", "unexecuted original shell commands")],
    ("PN1", "R0"): [("table.md", "complete shown Markdown input; Unicode EM DASH preserved")],
    ("PN1", "R1"): [("table.md", "complete shown Markdown input; Unicode EM DASH preserved")],
    ("PN2", "R0"): [("formula.html", "complete shown HTML fragment input"), ("reported_output.adoc", "questioner reported output; not desired result")],
    ("PN2", "R1"): [("formula.html", "complete shown HTML fragment input"), ("reported_output.adoc", "questioner reported output; not desired result")],
    ("PE1", "R0"): [], ("PE1", "R1"): [],
    ("PE2", "R0"): [],
    ("PE2", "R1"): [("python_chunk.qmd", "shown Quarto input chunk; not realized Pandoc AST"), ("r_chunk.qmd", "shown Quarto input chunk; not realized Pandoc AST")],
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def products():
    outputs, entries, sources = {}, [], []
    for case, qid in CASES.items():
        for rev in ("R0", "R1"):
            source = ROOT / "evidence" / rev.lower() / (qid + ".html")
            raw_source = source.read_bytes()
            text = raw_source.decode("utf-8")
            relative_source = source.relative_to(ROOT).as_posix()
            sources.append({"case_id": case, "question_id": int(qid), "revision_label": rev,
                            "path": relative_source, "sha256": sha(raw_source)})
            matches = list(PRE.finditer(text))
            specs = BLOCKS[(case, rev)]
            if len(matches) != len(specs):
                raise ValueError(f"Unexpected code-block count: {case}/{rev}")

            def add(name, role, content, span, method, block=None, extra=None):
                destination = f"inputs/{case}/{rev}-{name}"
                encoded = content.encode("utf-8")
                outputs[destination] = encoded
                start, end = span
                row = {
                    "case_id": case, "question_id": int(qid), "revision_label": rev,
                    "path": destination, "sha256": sha(encoded), "bytes": len(encoded), "role": role,
                    "source_path": relative_source, "source_sha256": sha(raw_source),
                    "source_html_lines": [text.count("\n", 0, start) + 1,
                                          text.count("\n", 0, max(start, end - 1)) + 1],
                    "source_character_span_zero_based_half_open": [start, end],
                    "source_span_sha256": sha(text[start:end].encode("utf-8")),
                    "pre_code_block_ordinal_one_based": block, "extraction": method,
                    "source_is_frozen_rendered_html_not_original_markdown": True,
                }
                if extra:
                    row.update(extra)
                entries.append(row)

            for ordinal, (match, (name, role)) in enumerate(zip(matches, specs), 1):
                decoded = html.unescape(match.group(1))
                add(name, role, decoded, match.span(1),
                    "HTML entity decode exactly once; code content whitespace preserved", ordinal)

            if case == "JE1":
                decoded = html.unescape(matches[0].group(1))
                start = decoded.index("[", decoded.index("json_data ="))
                value, consumed = json.JSONDecoder().raw_decode(decoded[start:])
                if not isinstance(value, list) or len(value) != 2:
                    raise ValueError("JE1 exact JSON substring shape changed")
                content = decoded[start:start + consumed]
                add("web_data.json", "complete JSON input substring; no LangChain behavior claimed", content,
                    matches[0].span(1),
                    "HTML entity decode once; exact balanced JSON substring after json_data =; no whitespace normalization",
                    1, {"decoded_parent_character_span_zero_based_half_open": [start, start + consumed],
                        "parent_decoded_sha256": sha(decoded.encode("utf-8"))})

            if case == "PE1":
                inline = re.search(r"<code>(\{\.lang \.numberLines\})</code>", text)
                if inline is None:
                    raise ValueError("PE1 inline attribute missing")
                add("code_attribute.txt", "only code attributes; full code block, command, and engine are missing",
                    html.unescape(inline.group(1)), inline.span(1), "HTML entity decode once; inline content unchanged")

            if case == "PE2" and rev == "R0":
                paras = list(re.finditer(r"<p>(.*?)</p>", text, re.S))
                for lang, name in (("python", "python_chunk.qmd"), ("r", "r_chunk.qmd")):
                    first = next(i for i, m in enumerate(paras) if m.group(1) == "```{" + lang + "}")
                    last = next(i for i in range(first + 1, len(paras)) if paras[i].group(1) == "```")
                    members = paras[first:last + 1]
                    content = "\n".join(html.unescape(m.group(1)) for m in members) + "\n"
                    add(name, "Quarto chunk reconstructed from separate rendered paragraphs; original Markdown whitespace unknown",
                        content, (members[0].start(), members[-1].end()),
                        "HTML entity decode once per paragraph; join paragraph texts with one LF and terminal LF; rendering reconstruction, not original Markdown bytes",
                        extra={"paragraph_count": len(members)})

            if case == "JN1" and rev == "R0":
                for n, prefix in ((1, "drp="), (2, "apg=")):
                    match = re.search(re.escape(prefix) + r".*?(?=</p>)", text, re.S)
                    if match is None:
                        raise ValueError("JN1 paragraph query missing")
                    add(f"attempted_query0{n}.txt", "unexecuted original shell command extracted from paragraph",
                        html.unescape(match.group()), match.span(), "HTML entity decode once; paragraph command substring unchanged")

    index = {
        "schema": "AF-RES-088-extracted-inputs-v1",
        "method": "Deterministic extraction from frozen evidence/r0 and evidence/r1 only; no answers, current pages, downloads, repaired fixtures or synthetic code.",
        "source_files": sources,
        "entries": entries,
        "limitations": [
            "Hashes identify archived rendered HTML and extracted bytes, not initial posting bytes.",
            "R0 JN1 and both JE2 JSON inputs are incomplete; ellipses are not removed or filled.",
            "PE1 contains only attributes and images; no complete Markdown input is supplied.",
            "PE2 R0 paragraph joins recover visible code but not original Markdown byte layout.",
            "Reported outputs and attempted commands remain separately labeled and are not run.",
        ],
    }
    outputs["inputs/index.json"] = (json.dumps(index, ensure_ascii=False, indent=2) + "\n").encode()
    return outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="compare all expected extracted files without writing")
    args = parser.parse_args()
    expected = products()
    failures = []
    for relative, content in expected.items():
        path = EXECUTION / relative
        if args.check:
            if not path.exists() or path.read_bytes() != content:
                failures.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    if failures:
        print(json.dumps({"status": "mismatch", "paths": failures}, ensure_ascii=False))
        return 1
    print(json.dumps({"status": "verified" if args.check else "extracted", "file_count_including_index": len(expected)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
