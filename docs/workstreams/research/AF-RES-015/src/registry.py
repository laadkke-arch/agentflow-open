"""Record the exact npm latest-version deprecation field from the public registry."""

import json
from urllib.parse import quote

from collect import ROOT, Reader


def main():
    reader = Reader(1.06)
    path = ROOT / "results" / "registry.jsonl"
    with path.open("w", encoding="utf-8", buffering=1) as stream:
        for line in (ROOT / "data" / "npm-packages.txt").read_text().splitlines():
            if not line or line.startswith("#"):
                continue
            name, predicates = line.split("|")
            info, body = reader.get(f"https://registry.npmjs.org/{quote(name, safe='@')}/latest")
            fields = json.loads(body) if body else None
            version = fields.get("version") if fields else None
            exact = bool(fields and fields.get("name") == name and version)
            observation = {"package": name, "predicates": predicates.split(","),
                           "version": version if exact else None, "matched": exact,
                           "deprecated": bool(fields.get("deprecated")) if exact else None,
                           "deprecation_message": " ".join(str(fields.get("deprecated", "")).split()[:25]) or None
                           if exact else None,
                           "license": fields.get("license") if exact else None, **info}
            stream.write(json.dumps(observation, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
