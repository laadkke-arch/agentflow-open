"""Extract the preregistered chronological GitHub opening-body frame."""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
START, STOP = "2023-01-01T00:00:00Z", "2026-01-01T00:00:00Z"
FENCE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})([^\r\n]*)\r?$", re.M)
VEGA_KEY = re.compile(r'"(?:mark|encoding|layer|concat|hconcat|vconcat|repeat|facet)"\s*:')
MERMAID_HEAD = re.compile(
    r"(?im)^[ \t]*(?:flowchart|graph|sequenceDiagram|classDiagram(?:-v2)?|"
    r"stateDiagram(?:-v2)?|erDiagram|journey|gantt|pie|quadrantChart|"
    r"requirementDiagram|gitGraph|C4\w+|mindmap|timeline|sankey-beta|"
    r"xychart-beta|block-beta|packet-beta|kanban|architecture-beta|"
    r"radar-beta|treemap-beta|venn-beta)\b"
)


def digest(raw):
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def fences(body):
    """Return the exact content of general Markdown fences, with byte spans."""
    cursor = 0
    while match := FENCE.search(body, cursor):
        marker, info = match.groups()
        if marker[0] == "`" and "`" in info:
            cursor = match.end()
            continue
        end_line = body.find("\n", match.end())
        start = len(body) if end_line < 0 else end_line + 1
        pattern = rf"(?m)^[ \t]{{0,3}}{re.escape(marker[0])}{{{len(marker)},}}[ \t]*\r?$"
        close = re.compile(pattern).search(body, start)
        end = close.start() if close else len(body)
        raw = body[start:end]
        yield {
            "info": info.strip(),
            "start": len(body[:start].encode("utf-8")),
            "end": len(body[:end].encode("utf-8")),
            "sha256": digest(raw),
            "closed": close is not None,
            "raw": raw,
        }
        cursor = close.end() if close else len(body)


def mermaid_specs(block, label):
    raw = block["raw"]
    if label not in ("", "mermaid", "text", "txt", "markdown", "md", "html"):
        return
    quoted = re.fullmatch(r"\s*`([\s\S]+?)`\s*", raw)
    wrappers = list(re.finditer(
        r"""<pre\b[^>]*\bclass=["'][^"']*\bmermaid\b[^"']*["'][^>]*>([\s\S]*?)</pre\s*>""",
        raw, re.I,
    ))
    if wrappers:
        spans = [wrapper.span(1) for wrapper in wrappers if MERMAID_HEAD.search(wrapper.group(1))]
    elif quoted and MERMAID_HEAD.match(quoted.group(1)):
        spans = [quoted.span(1)]
    else:
        header = MERMAID_HEAD.search(raw)
        if header:
            prefix = raw[:header.start()].strip()
            lead = r"(?i)(?:https?://[^\s]+|mermaid|(?:ok|bad|nok|works|fails|working|broken):)"
            if all(re.fullmatch(lead, line.strip()) for line in prefix.splitlines() if line.strip()):
                spans = [(0 if not prefix else header.start(), len(raw))]
            elif prefix.startswith(("%%", "---")):
                spans = [(0, len(raw))]
            else:
                spans = []
        elif label == "mermaid" and re.search(
            r"(?m)^\s*(?:classDef\s+|style\s+|direction\s+|[\w.-]+\s*[-<][-.-]+>)", raw
        ):
            spans = [(0, len(raw))]
        else:
            spans = []
    for start, end in spans:
        yield {
            **block,
            "fence_start": block["start"],
            "fence_end": block["end"],
            "fence_sha256": block["sha256"],
            "start": block["start"] + len(raw[:start].encode("utf-8")),
            "end": block["start"] + len(raw[:end].encode("utf-8")),
            "sha256": digest(raw[start:end]),
            "raw": raw[start:end],
            "format": "mermaid",
        }


def extract_specs(project, block):
    raw = block["raw"].strip()
    info = block["info"].lower().split()
    label = info[0].strip("{}.") if info else ""
    if not raw:
        return
    if project == "M":
        yield from mermaid_specs(block, label)
        return
    if not raw.startswith("{") or re.search(r"/schema/vega/v\d", raw):
        return None
    if label not in ("", "json", "jsonc", "text", "txt", "javascript", "js", "yaml", "vega-lite"):
        return None
    if "/schema/vega-lite/" not in raw and not VEGA_KEY.search(raw):
        return None
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        yield dict(block, format="vega-lite-partial")
        return
    if isinstance(parsed, dict):
        yield dict(block, format="vega-lite")


def read_pages(directory, project):
    rows = {}
    paths = sorted(directory.glob(f"{project}-*.jsonl"))
    for path in paths:
        for line in path.read_text().splitlines():
            row = json.loads(line)
            if row["number"] in rows:
                raise ValueError(f"duplicate issue in page snapshots: {project} {row['number']}")
            rows[row["number"]] = row
    return sorted(rows.values(), key=lambda row: (row["created"], row["number"]))


def make_frame(directory, project):
    result, rank = [], 0
    for row in read_pages(directory, project):
        if not START <= row["created"] < STOP:
            continue
        body = row.get("body")
        blocks = list(fences(body or "")) if not row["pr"] else []
        eligible = [spec for block in blocks for spec in extract_specs(project, block)]
        if row["pr"]:
            state = "pull-request"
        elif body is None:
            state = "null-body"
        elif not eligible:
            state = "no-qualifying-fence"
        else:
            rank += 1
            state = "boundary-41" if rank == 41 else "within-first-40"
        result.append((row, state, rank if eligible else None, eligible, len(blocks)))
        if rank == 41:
            break
    return result


def frame_entry(project, item, decisions):
    row, state, rank, blocks, total = item
    decision = decisions.get(f"{project}{row['number']}", {})
    return {
        "project": project,
        "number": row["number"],
        "created_utc": row["created"],
        "updated_utc": row["updated"],
        "rank": rank,
        "state": state,
        "selection": decision.get("selection", "cutoff" if rank == 41 else "뒤 순번·먼저 세 건 충족" if rank else state),
        "eligibility_evidence": decision.get("evidence", ""),
        "original_state": decision.get("history", "API opening field; first revision unverified" if rank else ""),
        "title": row["title"],
        "issue_url": row["html"],
        "api_url": row["api"],
        "page_url": row["page_url"],
        "retrieved_utc": row["retrieved_utc"],
        "body_bytes": len(row["body"].encode("utf-8")) if row["body"] is not None else None,
        "body_sha256": digest(row["body"]) if row["body"] is not None else None,
        "fence_count": total,
        "specs": json.dumps(
            [{key: val for key, val in block.items() if key != "raw"} for block in blocks],
            ensure_ascii=False, separators=(",", ":"),
        ),
    }


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("pages", type=Path, help="local JSONL opening-body page snapshots")
    parser.add_argument("--write", action="store_true", help="write frame.csv with reviewed selection")
    args = parser.parse_args()
    frames = {project: make_frame(args.pages, project) for project in ("V", "M")}
    for project, frame in frames.items():
        print(project, len(frame), sum(rank is not None for _, _, rank, _, _ in frame))
        for row, _, rank, blocks, _ in frame:
            if rank is not None:
                print(f"{project}{row['number']} rank={rank} {row['title']!r}",
                      [(b['format'], b['end'] - b['start'], b['raw'].splitlines()[0][:100]) for b in blocks])
    if args.write:
        decisions = json.loads((ROOT / "selection.json").read_text())
        rows = [frame_entry(project, item, decisions) for project, items in frames.items() for item in items]
        with (ROOT / "frame.csv").open("w", encoding="utf-8", newline="") as output:
            writer = csv.DictWriter(output, rows[0])
            writer.writeheader()
            writer.writerows(rows)


if __name__ == "__main__":
    main()
