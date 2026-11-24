"""Change one declared catalog input and preserve all other records."""

import argparse
import json
from pathlib import Path

from replay import PROFILES, read_jsonl


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--feature", required=True)
    change = parser.add_mutually_exclusive_group(required=True)
    change.add_argument("--drop-alias", choices=tuple(PROFILES))
    change.add_argument("--omit-role", nargs=2, metavar=("CONCEPT", "ROLE"))
    args = parser.parse_args()
    cards = read_jsonl(args.input)
    card, = [item for item in cards if item["feature_id"] == args.feature]
    if args.drop_alias:
        card[PROFILES[args.drop_alias]] = []
    else:
        concept, role = args.omit_role
        before = card["roles"]
        card["roles"] = [entry for entry in before if (entry["concept"], entry["role"]) != (concept, role)]
        if len(before) - len(card["roles"]) != 1:
            raise ValueError("the intervention must omit exactly one recorded role")
    with args.output.open("x", encoding="utf-8") as stream:
        for card in cards:
            stream.write(json.dumps(card, ensure_ascii=False, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
