"""Read observations from fixed upstream files or disclosed local fault fixtures."""
from dataclasses import dataclass
from datetime import datetime
import hashlib
from io import BytesIO
import json
from pathlib import Path
import re
from xml.etree import ElementTree as ET
from zoneinfo import ZoneInfo

from events import ROOT, SELECTION


@dataclass(frozen=True)
class Observation:
    id: str | None
    url: str
    edition: str | None
    key: str | None
    scope: str | None
    location: str | None
    at: int | None
    kind: str
    value: dict | None
    delivery: str | None


class UnsupportedPath(ValueError):
    pass


class Provider:
    def __init__(self, prepared):
        self.prepared = Path(prepared)
        self.cells = {cell["id"]: cell for family in SELECTION["family_edition_order"]
                      for cell in SELECTION[family]}
        self.reads = []
        self.calls = []

    def read(self, path):
        content = path.read_bytes()
        name = (path.relative_to(self.prepared).as_posix() if path.is_relative_to(self.prepared)
                else "fixture/" + path.name)
        self.reads.append((name, len(content)))
        return content

    def acquire(self, event, edition, delivery):
        self.calls.append((event["id"], event["url"], edition, event["key"]))
        loc = None
        try:
            if event["family"] == "fixture":
                loc, value, kind = self.fixture(event, edition)
            elif event["family"] == "tzdb":
                loc, value = self.zone(self.cells[event["key"]], edition)
                kind = "value"
            else:
                loc, value = self.symbol(self.cells[event["key"]], edition)
                kind = "value" if value is not None else "key_absent"
        except (OSError, ValueError, ET.ParseError) as error:
            # The exact failed member/selector remains visible without inventing values.
            loc, value = (self.cells.get(event["key"], {}).get("member"), None)
            kind = "path_unresolved" if isinstance(error, (UnsupportedPath, ET.ParseError)) else "access_lost"
        obs_id = hashlib.sha256(delivery.encode()).hexdigest()[:24]
        return Observation(obs_id, event["url"], edition, event["key"], event.get("scope"),
                           loc, event["at"], kind, value, delivery)

    def zone(self, cell, edition):
        tzif = self.read(self.prepared / "tzdb" / edition / cell["zone"])
        zone = ZoneInfo.from_file(BytesIO(tzif), key=cell["zone"])
        instant = datetime.fromisoformat(cell["utc"]).astimezone(zone)
        location = f'{cell["member"]}#Zone {cell["zone"]}'
        return location, {"offset_seconds": int(instant.utcoffset().total_seconds()),
                          "abbreviation": instant.tzname()}

    def parents(self, root):
        data = self.read(root / "common/supplemental/supplementalData.xml")
        tree = ET.fromstring(data)
        return {name: entry.get("parent")
                for parents in tree.findall("parentLocales") if not parents.get("component")
                for entry in parents.findall("parentLocale")
                for name in entry.get("locales", "").split()}

    def symbol(self, cell, edition):
        root = self.prepared / "cldr" / edition
        locale = cell["locale"]
        system = cell["number_system"]
        role = cell["role"]
        seen = set()
        parents = None
        while locale:
            if (locale, system) in seen:
                raise UnsupportedPath(f"LDML cycle for {locale}/{system}")
            seen.add((locale, system))
            member = f"common/main/{locale}.xml"
            path = root / member
            if path.is_file():
                node = ET.fromstring(self.read(path))
                if node.find("alias") is not None or node.find("numbers/alias") is not None:
                    raise UnsupportedPath(f"whole-locale/numbers alias at {locale}")
                symbols = node.find(f"numbers/symbols[@numberSystem='{system}']")
                if symbols is not None:
                    alias = symbols.find("alias")
                    if alias is not None:
                        match = re.fullmatch(r"\.\./symbols\[@numberSystem='([A-Za-z0-9]+)'\]",
                                             alias.get("path", ""))
                        if alias.get("source") != "locale" or match is None:
                            raise UnsupportedPath(f"nonlocal symbols alias at {locale}/{system}")
                        system = match.group(1)
                        continue
                    literals = [x for x in symbols.findall(role) if not x.get("alt")]
                    if len(literals) > 1:
                        raise UnsupportedPath(f"nonunique symbols at {locale}/{system}/{role}")
                    value = literals[0].text if literals else None
                    location = f"{member}#/ldml/numbers/symbols[@numberSystem='{system}']/{role}"
                    if value == "∅∅∅":
                        return location, None
                    if value is not None and value != "↑↑↑":
                        return location, {"symbol": value, "role": role}
            if locale == "root":
                if not path.is_file():
                    raise FileNotFoundError(path)
                break
            if parents is None:
                parents = self.parents(root)
            locale = parents.get(locale, locale.rpartition("_")[0] or "root")
        return cell["member"] + "#" + cell["xpath"], None

    def fixture(self, event, edition):
        key, scope = event["key"], event.get("scope") or "general"
        loc = f"replay/fixture_source.json#/{edition}/{key}/{scope}"
        if key == "recovery" and event["at"] < 5:
            return loc, None, "temporary"
        if edition == "f3":
            return loc, None, "access_lost"
        raw = self.read(ROOT / "replay" / "fixture_source.json")
        value = json.loads(raw)[edition].get(key, {}).get(scope)
        if key == "entry" and edition == "f2":
            return loc, None, "entry_unavailable"
        return loc, value, "value" if value is not None else "key_absent"
