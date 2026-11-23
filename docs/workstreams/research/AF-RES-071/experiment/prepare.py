"""Emit the primary and supplemental paired-change frame before execution."""
import csv
from pathlib import Path
import sys

from model import ROOT, canonical, design, digest, load_json


PAIR_COLUMNS = ("pair_id", "layer", "object_id", "type", "treatment", "primary",
                "before_version", "after_version", "before_tag", "after_tag",
                "before_address", "after_address", "before_files", "after_files",
                "before_payload_sha256", "after_payload_sha256", "before_order", "after_order",
                "before_policy", "after_policy", "expected_answer_change",
                "expected_reason_change", "expected_link_change", "expected_load_order_change",
                "before_synthetic", "after_synthetic", "old_recipe_public")


def write_csv(path, columns, rows):
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(columns)
        writer.writerows(rows)


def payload_sha(edition):
    return digest(canonical({role: digest(raw) for role, raw in edition.files.items()}).encode())


def pair_row(pair):
    before, after = pair.before, pair.after
    return (pair.id, pair.spec["domain"], before.object_id, pair.type, pair.change, int(pair.main),
            before.id, after.id, before.tag, after.tag, before.address, after.address,
            canonical(before.fingerprints()), canonical(after.fingerprints()),
            payload_sha(before), payload_sha(after), " ".join(before.order), " ".join(after.order),
            before.policy, after.policy, *(int(value) for value in pair.expected),
            int(before.synthetic), int(after.synthetic), int(pair.old_recipe_public))


def main(out):
    (out / "inputs").mkdir(parents=True, exist_ok=True)
    specs = load_json(ROOT / "inputs" / "objects.json")
    pairs = list(design(specs))
    write_csv(out / "pairs.csv", PAIR_COLUMNS, (pair_row(pair) for pair in pairs))
    versions = {edition.id: edition for pair in pairs for edition in (pair.before, pair.after)}
    inventory = {}
    for episode, edition in sorted(versions.items()):
        inventory[episode] = {"tag": edition.tag, "source_copy": episode.endswith(".C0"),
                              "synthetic": edition.synthetic, "sha256_content_by_role": payload_sha(edition),
                              "files": {edition.paths[role]: {"sha256": digest(raw), "bytes": len(raw)}
                                        for role, raw in edition.files.items()}}
    raw_origins = {p.name: {"sha256": digest(p.read_bytes()), "bytes": p.stat().st_size}
                   for p in sorted((ROOT / "inputs").glob("*.txt"))}
    (out / "inputs" / "sha256.json").write_text(canonical({"local_versions": inventory,
                                                           "source_extracts": raw_origins}) + "\n")
    print(f"planned {sum(pair.main for pair in pairs)} primary, {sum(not pair.main for pair in pairs)} supplemental")


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT)
