"""Build AF-RES-100's frozen, file-identical A/B x F/S evidence packets.

No source bodies or snippets are written to tracked output. Cached upstream bytes
are indexed without printing them. Run only after requirements/corpus scope have
been fixed; the protocol's exact bytes are part of every opaque packet ID.

    python -B docs/workstreams/research/AF-RES-100/packet_builder.py
    python -B docs/workstreams/research/AF-RES-100/packet_builder.py --verify

Offsets are zero-based, half-open, in the unnormalised UTF-8 source. Unicode
offsets count Python Unicode code points, not encoded bytes or grapheme clusters.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import unicodedata


ROOT = Path(__file__).resolve().parent
CACHE_ROOT = ROOT / "evidence" / "_cache"


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def tokens(value: str) -> set[str]:
    """Exact AF-RES-096 experiment.py normalisation and membership rule."""
    return set(re.findall(r"[a-z0-9_]+", unicodedata.normalize("NFKC", value).casefold()))


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def jsonl_bytes(rows: list[dict]) -> bytes:
    return b"".join((json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8") for row in rows)


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_bytes().decode("utf-8").splitlines() if line.strip()]


def cached_path(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(CACHE_ROOT.resolve()):
        raise ValueError("cached_body must resolve inside evidence/_cache")
    return path


def query_text(value: str | list[str]) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return " ".join(value)
    raise ValueError("each query must be a string or an array of strings")


def anchor_position(text: str, matched: set[str]) -> tuple[int | None, bool]:
    if not matched:
        return None, True
    pattern = r"(?<![a-z0-9_])(?:" + "|".join(re.escape(t) for t in sorted(matched)) + r")(?![a-z0-9_])"
    match = re.search(pattern, text, flags=re.I)
    return (match.start(), False) if match is not None else (None, True)


def byte_offset(text: str, char_offset: int) -> int:
    return len(text[:char_offset].encode("utf-8"))


def ranking_rows(files: list[dict], index: dict[str, set[str]], query_sets: list[set[str]], which: int | None) -> list[dict]:
    merged = set().union(*query_sets)
    ranked_tokens = merged if which is None else query_sets[which]
    ordered = sorted(files, key=lambda row: (-len(ranked_tokens & index[row["file_id"]]), row["repo"] + "/" + row["path"]))
    return [
        {
            "rank": rank,
            "file_id": row["file_id"],
            "repo": row["repo"],
            "path": row["path"],
            "url": row["url"],
            "score": len(ranked_tokens & index[row["file_id"]]),
            "matched_tokens": sorted(ranked_tokens & index[row["file_id"]]),
            "per_query_scores": [len(q & index[row["file_id"]]) for q in query_sets],
            "per_query_matched_tokens": [sorted(q & index[row["file_id"]]) for q in query_sets],
            "eligible": bool(ranked_tokens & index[row["file_id"]]),
        }
        for rank, row in enumerate(ordered, 1)
    ]


def public_slot(slot: dict) -> dict:
    fields = (
        "slot", "file_id", "empty", "empty_reason", "url", "sha256",
        "git_blob_sha", "char_start", "char_end", "byte_start", "byte_end",
        "exposed_chars", "exposed_bytes", "exposed_sha256",
        "source_chars", "source_bytes",
    )
    return {key: slot[key] for key in fields if key in slot}


def build() -> tuple[dict[Path, bytes], dict]:
    protocol_raw = (ROOT / "protocol.json").read_bytes()
    protocol = json.loads(protocol_raw)
    protocol_sha = digest(protocol_raw)
    corpus_raw = (ROOT / "corpus-files.jsonl").read_bytes()
    inventory = read_jsonl(ROOT / "corpus-files.jsonl")
    cases = protocol["cases"]
    if len(cases) != 8:
        raise ValueError("protocol must preserve exactly eight case positions, including vacancies")
    if len({c["case_id"] for c in cases}) != 8:
        raise ValueError("case_id values must be unique")
    for case in cases:
        if not re.fullmatch(r"[A-Za-z0-9_-]+", case["case_id"]):
            raise ValueError("unsafe case_id")
        if case["stratum"] not in {"boundary", "control"}:
            raise ValueError("stratum must be boundary or control")
        if len(case.get("queries", [])) != 2:
            raise ValueError("every case must retain exactly two queries, even if both are empty")

    used_labels = {c.get(key) for c in cases for key in ("main_label", "adjacent_label") if c.get(key)}
    inventory = [row for row in inventory if row["label"] in used_labels]
    by_id = {row["file_id"]: row for row in inventory}
    if len(by_id) != len(inventory):
        raise ValueError("duplicate corpus file_id")
    bodies: dict[str, tuple[bytes, str]] = {}
    index: dict[str, set[str]] = {}
    for row in inventory:
        raw = cached_path(row["cached_body"]).read_bytes()
        if digest(raw) != row["sha256"]:
            raise ValueError("corpus SHA-256 mismatch: " + row["file_id"])
        text = raw.decode("utf-8")  # read_bytes avoids newline conversion
        bodies[row["file_id"]] = (raw, text)
        index[row["file_id"]] = tokens(text)

    outputs: dict[Path, bytes] = {}
    packets: list[dict] = []
    for case in cases:
        case_id = case["case_id"]
        query_sets = [tokens(query_text(q)) for q in case["queries"]]
        merged = set().union(*query_sets)
        available = case.get("question_id") is not None and not case.get("vacant", False)
        ranked_by_role: dict[str, list[dict]] = {}
        for role, label_key in (("main", "main_label"), ("adjacent", "adjacent_label")):
            label = case.get(label_key)
            files = [row for row in inventory if row["label"] == label] if available and label else []
            for which, suffix in ((0, "q1"), (1, "q2"), (None, "merged")):
                rows = ranking_rows(files, index, query_sets, which)
                outputs[ROOT / "evidence" / "ranking" / f"{case_id}-{role}-{suffix}.jsonl"] = jsonl_bytes(rows)
                if which is None:
                    ranked_by_role[role] = [r for r in rows if r["score"] > 0]

        def selected(role: str, count: int) -> list[tuple[str, dict | None]]:
            choices = ranked_by_role[role][:count]
            return [(role, choices[i] if i < len(choices) else None) for i in range(count)]

        a_choices = selected("main", 4)
        policies = {"A": a_choices, "B": a_choices if case["stratum"] == "control" else selected("main", 2) + selected("adjacent", 2)}
        for policy in ("A", "B"):
            for mode in ("F", "S"):
                identity = "\0".join((case_id, policy, mode, protocol_sha)).encode("utf-8")
                packet_id = digest(identity)[:12]
                slots = []
                for slot_number, (role, ranked) in enumerate(policies[policy], 1):
                    if ranked is None:
                        slots.append({
                            "slot": slot_number, "file_id": None, "empty": True,
                            "empty_reason": "vacant_request" if not available else "no_positive_ranked_file",
                            "role": role, "url": None, "sha256": None, "git_blob_sha": None,
                            "char_start": 0, "char_end": 0, "byte_start": 0, "byte_end": 0,
                            "exposed_chars": 0, "exposed_bytes": 0, "exposed_sha256": None,
                            "source_chars": 0, "source_bytes": 0,
                            "matched_tokens": [], "anchor_char": None, "anchor_fallback": True,
                            "queries": case["queries"], "charged_first_attempt": 1,
                        })
                        continue
                    row = by_id[ranked["file_id"]]
                    raw, text = bodies[row["file_id"]]
                    anchor, fallback = anchor_position(text, merged & index[row["file_id"]])
                    start = 0 if mode == "F" else max(0, (anchor if anchor is not None else 0) - 200)
                    end = len(text) if mode == "F" else min(len(text), start + 1200)
                    bstart, bend = byte_offset(text, start), byte_offset(text, end)
                    exposed_raw = raw[bstart:bend]
                    if exposed_raw != text[start:end].encode("utf-8"):
                        raise AssertionError("Unicode/UTF-8 interval mismatch")
                    slots.append({
                        "slot": slot_number, "file_id": row["file_id"], "empty": False,
                        "role": role, "repo": row["repo"], "path": row["path"],
                        "url": row["url"], "version": row.get("version"), "commit": row.get("commit"),
                        "sha256": row["sha256"], "git_blob_sha": git_blob_sha(raw),
                        "git_blob_sha_provenance": "calculated from exact cached upstream bytes",
                        "cached_body": row["cached_body"],
                        "within_role_rank": ranked["rank"], "score": ranked["score"],
                        "matched_tokens": ranked["matched_tokens"], "queries": case["queries"],
                        "anchor_char": anchor, "anchor_fallback": fallback,
                        "char_start": start, "char_end": end, "byte_start": bstart, "byte_end": bend,
                        "exposed_chars": end - start, "exposed_bytes": bend - bstart,
                        "exposed_sha256": digest(exposed_raw),
                        "source_chars": len(text), "source_bytes": len(raw), "charged_first_attempt": 1,
                    })
                packet = {
                    "schema": "af-res-100-packet-v1", "packet_id": packet_id,
                    "case_id": case_id, "question_id": case.get("question_id"),
                    "case_available": available, "stratum": case["stratum"],
                    "policy": policy, "mode": mode, "queries": case["queries"],
                    "query_tokens": [sorted(q) for q in query_sets],
                    "conditions": case.get("conditions", []),
                    "protocol_sha256": protocol_sha, "corpus_manifest_sha256": digest(corpus_raw),
                    "offset_convention": "zero-based half-open; original Unicode codepoints and UTF-8 bytes",
                    "slots": slots, "max_charged_attempts": 4,
                    "max_exposed_chars": 4800 if mode == "S" else None,
                    "total_exposed_chars": sum(slot["exposed_chars"] for slot in slots),
                }
                if mode == "S" and packet["total_exposed_chars"] > 4800:
                    raise AssertionError("short packet exceeds 4800 codepoints")
                packets.append(packet)
                descriptor = {
                    "schema": "af-res-100-reader-packet-v1", "packet_id": packet_id,
                    "question_id": case.get("question_id"), "request_available": available,
                    "conditions": case.get("conditions", []),
                    "original_revision_url": case.get("r0_url") or case.get("revision_url"),
                    "offset_convention": packet["offset_convention"],
                    "slots": [public_slot(slot) for slot in slots],
                    "reader_instruction": "Cite only the source intervals actually displayed through read_packet.py. URL identities are evidence provenance, not permission to open them externally. No supplied answer or other packet may be consulted.",
                }
                outputs[ROOT / "evidence" / "packet-descriptors" / f"{packet_id}.json"] = json_bytes(descriptor)

    if len(packets) != 32 or len({p["packet_id"] for p in packets}) != 32:
        raise AssertionError("expected 32 unique packet IDs")
    outputs[ROOT / "packets.jsonl"] = jsonl_bytes(packets)
    summary = {
        "protocol_sha256": protocol_sha, "corpus_manifest_sha256": digest(corpus_raw),
        "packets": len(packets), "file_positions": sum(len(p["slots"]) for p in packets),
        "empty_file_positions": sum(s["empty"] for p in packets for s in p["slots"]),
        "source_files_indexed": len(inventory), "outputs": len(outputs),
        "packet_ids": [p["packet_id"] for p in packets],
    }
    return outputs, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="Recompute every output and require byte-identical existing files; write nothing.")
    args = parser.parse_args()
    outputs, summary = build()
    mismatches = []
    for path, raw in outputs.items():
        if path.exists():
            if path.read_bytes() != raw:
                mismatches.append(str(path.relative_to(ROOT)))
        elif args.verify:
            mismatches.append(str(path.relative_to(ROOT)) + " (missing)")
    if mismatches:
        raise ValueError("Refusing to overwrite or validate changed output: " + "; ".join(mismatches))
    if not args.verify:
        for path, raw in outputs.items():
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open("xb") as stream:
                    stream.write(raw)
    print(json.dumps({"status": "verified" if args.verify else "built", **summary}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
