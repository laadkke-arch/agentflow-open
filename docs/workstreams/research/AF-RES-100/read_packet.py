"""Read registered AF-RES-100 packet intervals and log every displayed interval.

    python -B .../read_packet.py inspect PACKET_ID
    python -B .../read_packet.py read PACKET_ID SLOT [--start N --end N]
    python -B .../read_packet.py search PACKET_ID SLOT PATTERN [--limit N --context N]

Read offsets are absolute source Unicode code-point offsets, zero-based and
half-open. Full-file packets allow subsequent within-file navigation. Restricted
packets allow exactly one complete registered snippet read per slot and no search.
The first source access to each slot costs one, including vacant/failed slots.
The tool enforces its own interface, not operating-system isolation of readers.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import datetime
import fcntl
import hashlib
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent
CACHE_ROOT = (ROOT / "evidence" / "_cache").resolve()


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(s) for s in path.read_bytes().decode("utf-8").splitlines() if s.strip()]


def packet_for(packet_id: str) -> dict:
    if not re.fullmatch(r"[0-9a-f]{12}", packet_id):
        raise ValueError("invalid opaque packet ID")
    rows = [p for p in read_jsonl(ROOT / "packets.jsonl") if p["packet_id"] == packet_id]
    if len(rows) != 1:
        raise ValueError("packet ID is not uniquely registered")
    packet = rows[0]
    if digest((ROOT / "protocol.json").read_bytes()) != packet["protocol_sha256"]:
        raise ValueError("protocol changed after packet construction")
    if digest((ROOT / "corpus-files.jsonl").read_bytes()) != packet["corpus_manifest_sha256"]:
        raise ValueError("corpus manifest changed after packet construction")
    return packet


@contextmanager
def access_log(packet_id: str):
    path = ROOT / "evidence" / "packet-access" / f"{packet_id}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+", encoding="utf-8", newline="\n") as stream:
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        stream.seek(0)
        rows = [json.loads(line) for line in stream if line.strip()]
        try:
            yield stream, rows
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def append(stream, event: dict) -> None:
    stream.seek(0, 2)
    stream.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")
    stream.flush()


def safe_body(slot: dict) -> tuple[bytes, str]:
    path = (ROOT / slot["cached_body"]).resolve()
    if not path.is_relative_to(CACHE_ROOT):
        raise ValueError("registered source escaped evidence/_cache")
    raw = path.read_bytes()
    if digest(raw) != slot["sha256"]:
        raise ValueError("source SHA-256 mismatch")
    text = raw.decode("utf-8")
    if len(raw) != slot["source_bytes"] or len(text) != slot["source_chars"]:
        raise ValueError("source size mismatch")
    start, end = slot["char_start"], slot["char_end"]
    bstart, bend = len(text[:start].encode("utf-8")), len(text[:end].encode("utf-8"))
    if (bstart, bend) != (slot["byte_start"], slot["byte_end"]):
        raise ValueError("registered Unicode/UTF-8 boundary mismatch")
    if digest(raw[bstart:bend]) != slot["exposed_sha256"]:
        raise ValueError("exposure SHA-256 mismatch")
    return raw, text


def segment(text: str, start: int, end: int) -> dict:
    shown = text[start:end]
    return {
        "char_start": start, "char_end": end,
        "byte_start": len(text[:start].encode("utf-8")),
        "byte_end": len(text[:end].encode("utf-8")),
        "displayed_chars": len(shown), "displayed_utf8_bytes": len(shown.encode("utf-8")),
        "segment_sha256": digest(shown.encode("utf-8")),
        "line_start": text.count("\n", 0, start) + 1,
        "line_end": text.count("\n", 0, max(start, end - 1)) + 1,
    }


def merged_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    output: list[tuple[int, int]] = []
    for start, end in sorted(intervals):
        if output and start <= output[-1][1]:
            output[-1] = (output[-1][0], max(end, output[-1][1]))
        else:
            output.append((start, end))
    return output


def emit(event: dict, text: str | None = None) -> None:
    # The receipt contains no policy/mode labels. Mode becomes observable only
    # through source interval size or an attempted operation's permission rule.
    print(json.dumps(event, ensure_ascii=False, indent=2))
    if text is not None:
        for number, part in enumerate(event.get("displayed_segments", []), 1):
            print(f"\n--- source interval {number}: chars [{part['char_start']},{part['char_end']}); bytes [{part['byte_start']},{part['byte_end']}) ---")
            sys.stdout.write(text[part["char_start"]:part["char_end"]])
            sys.stdout.write("\n--- end source interval ---\n")


def act(args, packet: dict) -> int:
    slot = next((s for s in packet["slots"] if s["slot"] == args.slot), None)
    if slot is None:
        raise ValueError("slot must be one of the four registered positions")
    with access_log(packet["packet_id"]) as (stream, prior):
        slot_prior = [e for e in prior if e.get("slot") == args.slot and e.get("event") == "source_open"]
        charged = sum(e.get("charged_attempts", 0) for e in prior)
        event = {
            "packet_id": packet["packet_id"], "slot": args.slot, "file_id": slot["file_id"],
            "url": slot.get("url"), "command": args.command, "started_utc": now(),
            "event": "source_open" if not slot_prior else "section_navigation",
            "charged_attempts": 0, "prior_slot_accesses": len(slot_prior),
            "prior_display_events": sum(bool(e.get("displayed_segments")) for e in prior if e.get("slot") == args.slot),
            "exposed_char_start": slot["char_start"], "exposed_char_end": slot["char_end"],
            "exposed_byte_start": slot["byte_start"], "exposed_byte_end": slot["byte_end"],
            "source_sha256": slot.get("sha256"), "source_git_blob_sha": slot.get("git_blob_sha"),
            "displayed_segments": [], "displayed_chars": 0,
        }

        reason = None
        if packet["mode"] == "S" and args.command == "search":
            reason = "search is not permitted for this registered packet"
        elif packet["mode"] == "S" and (args.start is not None or args.end is not None):
            reason = "this registered snippet must be read in full without interval overrides"
        elif packet["mode"] == "S" and slot_prior:
            reason = "this slot has already used its single snippet access"
        elif slot_prior and slot_prior[0].get("status") != "success":
            reason = "failed or empty first access cannot be retried as free navigation"
        elif not slot_prior and charged >= 4:
            reason = "four charged access budget exhausted"
        if reason:
            event.update(event="denied_action", status="denied", reason=reason, finished_utc=now(), charged_total=charged)
            append(stream, event)
            emit(event)
            return 2

        if not slot_prior:
            event["charged_attempts"] = 1
        text = None
        try:
            if slot["empty"]:
                event.update(status="empty", reason=slot.get("empty_reason", "empty position"))
            else:
                raw, text = safe_body(slot)
                lo, hi = slot["char_start"], slot["char_end"]
                if not text:
                    raise ValueError("empty source file")
                if args.command == "read":
                    start = lo if args.start is None else args.start
                    end = (hi if packet["mode"] == "S" else min(hi, start + 1200)) if args.end is None else args.end
                    if not (lo <= start <= end <= hi):
                        raise ValueError("requested range lies outside the registered exposure")
                    intervals = [(start, end)]
                else:
                    if args.limit < 1 or args.limit > 100 or args.context < 0 or args.context > 5000:
                        raise ValueError("search limit must be 1..100 and context must be 0..5000")
                    regex = re.compile(args.pattern, re.I)
                    matches = []
                    for match in regex.finditer(text, lo, hi):
                        matches.append((match.start(), match.end()))
                        if len(matches) >= args.limit:
                            break
                    intervals = merged_intervals([(max(lo, a - args.context), min(hi, b + args.context)) for a, b in matches])
                    event.update(search_pattern=args.pattern, search_case_insensitive=True,
                                 search_limit=args.limit, search_context_chars=args.context,
                                 match_char_intervals=matches, search_scanned_chars=hi-lo,
                                 search_limit_reached=len(matches) == args.limit)
                parts = [segment(text, a, b) for a, b in intervals]
                event.update(status="success", displayed_segments=parts,
                             displayed_chars=sum(p["displayed_chars"] for p in parts),
                             displayed_utf8_bytes=sum(p["displayed_utf8_bytes"] for p in parts),
                             source_chars=len(text), source_bytes=len(raw))
        except Exception as exc:
            event.update(status="failed", error=f"{type(exc).__name__}: {exc}")
            text = None
        event.update(finished_utc=now(), charged_total=charged + event["charged_attempts"])
        append(stream, event)
        emit(event, text)
        return 0 if event["status"] in {"success", "empty"} else 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    p = subs.add_parser("inspect", help="Display the public descriptor; no source access is charged.")
    p.add_argument("packet_id")
    p = subs.add_parser("read", help="Display a registered interval; defaults to the first 1200 chars for a full-file packet, or the entire restricted snippet.")
    p.add_argument("packet_id")
    p.add_argument("slot", type=int)
    p.add_argument("--start", type=int)
    p.add_argument("--end", type=int)
    p = subs.add_parser("search", help="Search a registered full-file interval using a case-insensitive Python regular expression.")
    p.add_argument("packet_id")
    p.add_argument("slot", type=int)
    p.add_argument("pattern")
    p.add_argument("--limit", type=int, default=12)
    p.add_argument("--context", type=int, default=200)
    p.set_defaults(start=None, end=None)
    args = parser.parse_args()
    packet = packet_for(args.packet_id)
    if args.command == "inspect":
        descriptor = ROOT / "evidence" / "packet-descriptors" / f"{args.packet_id}.json"
        sys.stdout.write(descriptor.read_bytes().decode("utf-8"))
        return 0
    return act(args, packet)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, FileNotFoundError, KeyError) as exc:
        print(json.dumps({"status": "error", "error": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)
