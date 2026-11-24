"""Scope-specific persistence and response rules for the three SQLite hypotheses."""
from dataclasses import asdict
from datetime import datetime, timedelta
import hashlib
import json
import sqlite3

from events import ROOT, SELECTION, encoded
from provider import Observation

MASKS = ("edition", "location", "input_key", "requested_edition",
         "observed_at", "kind", "observation_id")
FIXED_NEGATIVES = {"key_absent", "entry_unavailable", "path_unresolved"}
TTL = SELECTION["virtual_ttl_ticks"]


def answer(mode, outcome, reason, value=None, obs=None):
    return {"mode": mode, "outcome": outcome, "reason": reason, "value": value,
            "basis": asdict(obs) if obs else None}


def decide(req, obs, mode="current"):
    if req["mode"] == "unknown":
        return answer(mode, "hold", "preference_unknown", obs=obs)
    if obs.kind != "value":
        return answer(mode, "hold", obs.kind, obs=obs)
    fact = obs.value
    if req["role"] and fact.get("role") != req["role"]:
        return answer(mode, "reject", "role_mismatch", fact, obs)
    if req["mode"] == "instant":
        if "offset_seconds" not in fact:
            return answer(mode, "hold", "role_unresolved", obs=obs)
        moment = datetime.fromisoformat(req["utc"])
        delta = timedelta(seconds=fact["offset_seconds"])
        wall_time = (moment + delta).replace(tzinfo=None).isoformat(timespec="seconds")
        return answer(mode, "approve", "instant_preserved",
                      {"local": wall_time, "offset_seconds": fact["offset_seconds"], "utc": req["utc"]},
                      obs)
    if req["mode"] == "literal":
        token = fact.get("symbol") if req["role"] else fact.get("abbreviation")
        value = {"literal": token, "role": req["role"] or "abbreviation"}
        match = token == req["literal"]
        return answer(mode, "approve" if match else "reject",
                      "literal_preserved" if match else "literal_changed", value, obs)
    if req["mode"] == "magnitude":
        sep = fact["symbol"]
        if not sep or any(ch.isdecimal() for ch in sep):
            return answer(mode, "hold", "role_unresolved", obs=obs)
        n = req["number"]
        if req["role"] == "decimal":
            rendered = n.replace(".", sep)
        else:
            rendered = n[:-3] + sep + n[-3:]
        rendered = rendered.translate(str.maketrans("0123456789", req["digits"]))
        return answer(mode, "approve", "number_preserved",
                      {"number": n, "display": rendered, "role": req["role"]}, obs)
    raise ValueError(req["mode"])


def present_observation(row):
    if row is None:
        return None
    loc = json.loads(row["location"]) if row["location"] else {}
    value = json.loads(row["value"]) if row["value"] else None
    return Observation(row["id"], row["url"], row["edition"], row["target_key"],
                       loc.get("scope"), loc.get("location"), row["observed_at"],
                       row["kind"] or ("value" if value is not None else "untyped_hold"),
                       value, row["provider_delivery_id"])


class Store:
    def __init__(self, database, design, policy, provider, mask=None):
        self.design = design
        self.versioned = design in {"B", "C"}
        self.policy = policy
        self.provider = provider
        self.mask = mask
        self.latest = {}
        self.sql_lookups = 0
        self.inserts = 0
        self.last_fetch = None
        self.transition = ""
        self.tables = ["links"]
        self.db = sqlite3.connect(database)
        self.db.row_factory = sqlite3.Row
        for pragma in ("page_size=4096", "journal_mode=DELETE", "synchronous=FULL",
                       "foreign_keys=ON"):
            self.db.execute("PRAGMA " + pragma)
        common, hypotheses = (ROOT / "schemas.sql").read_text(encoding="utf-8").split("-- A\n")
        a, hypotheses = hypotheses.split("-- B\n")
        b, c = hypotheses.split("-- C\n")
        self.db.executescript("CREATE TABLE IF NOT EXISTS " + common.split("CREATE TABLE ", 1)[1])
        self.db.executescript(self.idempotent(b if self.versioned else a))
        self.tables.append("observations" if self.versioned else "last_observation")
        if design == "C":
            self.db.executescript(self.idempotent(c))
            self.tables.append("decisions")

    @staticmethod
    def idempotent(sql):
        return sql.replace("CREATE TABLE ", "CREATE TABLE IF NOT EXISTS ").replace(
            "CREATE INDEX ", "CREATE INDEX IF NOT EXISTS ")

    def select(self, query, args):
        self.sql_lookups += 1
        return self.db.execute(query, args).fetchone()

    def remember(self, obs):
        self.last_fetch = asdict(obs)
        if obs.kind in {"value", "key_absent"}:
            title = {
                SELECTION["registrations"]["tzdb"]: "Time Zones",
                SELECTION["registrations"]["cldr"]: "CLDR Releases/Downloads",
            }.get(obs.url, "Controlled number record")
            self.db.execute("UPDATE links SET title=? WHERE url=? AND title IS NULL", (title, obs.url))
        value = encoded(obs.value) if obs.value is not None else None
        if not self.versioned:
            self.db.execute(
                """INSERT INTO last_observation VALUES (?, ?, ?)
                   ON CONFLICT(url) DO UPDATE SET value=excluded.value, status=excluded.status""",
                (obs.url, value, obs.kind))
            self.transition = "last-written"
            return obs
        location = encoded({"scope": obs.scope, "location": obs.location})
        inserted = self.db.execute("INSERT OR IGNORE INTO observations VALUES (?,?,?,?,?,?,?,?,?)",
                                   (obs.id, obs.url, None if self.mask == "edition" else obs.edition,
                                    obs.key, None if self.mask == "location" else location,
                                    None if self.mask == "observed_at" else obs.at,
                                    None if self.mask == "kind" else obs.kind, value, obs.delivery))
        self.inserts += inserted.rowcount
        self.transition = "observation-inserted" if inserted.rowcount else "delivery-deduplicated"
        return obs

    def observation(self, url, edition, key, scope, cutoff):
        conditions = ["url=?", "target_key=?"]
        args = [url, key]
        if self.mask != "edition":
            conditions.append("edition=?")
            args.append(edition)
        if self.mask != "location" and scope is not None:
            conditions.append("json_extract(location, '$.scope')=?")
            args.append(scope)
        if self.mask != "observed_at":
            conditions.append("observed_at<=?")
            args.append(cutoff)
        where = " AND ".join(conditions)
        return present_observation(self.select(
            f"SELECT * FROM observations WHERE {where} ORDER BY observed_at DESC,rowid DESC LIMIT 1", args))

    def reusable(self, obs, at):
        if not obs:
            return False
        if obs.kind == "value" or obs.kind in FIXED_NEGATIVES:
            return True
        return (self.policy == "ttl" and obs.kind in {"temporary", "untyped_hold"} and
                obs.at is not None and 0 <= at - obs.at < TTL)

    @staticmethod
    def input_key(event):
        return hashlib.sha256(encoded([event["input"], event["scope"]]).encode()).hexdigest()

    def existing_decision(self, event, edition):
        conditions = ["url=?", "project=?", "target_key=?", "request_selector=?",
                      "delivered_at<=?", "outcome IN ('approve','reject')", "observation_id IS NOT NULL"]
        args = [event["url"], event["project"], event["key"], event["selector"], event["at"]]
        if self.mask != "requested_edition":
            conditions.append("requested_edition=?")
            args.append(edition)
        if self.mask != "input_key":
            conditions.append("input_key=?")
            args.append(self.input_key(event))
        return self.select("SELECT * FROM decisions WHERE " + " AND ".join(conditions) +
                           " ORDER BY delivered_at DESC,rowid DESC LIMIT 1", args)

    def persist_decision(self, event, edition, result):
        proof = result["basis"]
        value = result["value"]
        req = event["input"]
        self.db.execute(
            "INSERT OR IGNORE INTO decisions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (event["id"], event["url"], event["project"], event["key"],
             None if self.mask == "requested_edition" else edition, event["selector"],
             None if self.mask == "input_key" else self.input_key(event),
             encoded(req),
             encoded({"mode": req["mode"], "literal": req["literal"], "role": req["role"]}),
             event["at"], proof["id"] if proof and self.mask != "observation_id" else None,
             result["outcome"], encoded(value) if value is not None else None,
             result["reason"], event["prior"]))

    def delivered(self, row, mode):
        obs = (present_observation(self.select("SELECT * FROM observations WHERE id=?",
                                              (row["observation_id"],)))
               if row["observation_id"] else None)
        value = json.loads(row["delivered_value"]) if row["delivered_value"] else None
        return answer(mode, row["outcome"], row["reason"], value, obs)

    def current(self, event, edition):
        if self.policy != "off":
            if self.design == "C":
                saved = self.existing_decision(event, edition)
                if saved:
                    self.transition = "decision-hit"
                    return self.delivered(saved, "current")
            if self.versioned:
                obs = self.observation(event["url"], edition, event["key"], event["scope"], event["at"])
                if self.reusable(obs, event["at"]):
                    self.transition = "observation-hit"
                    return decide(event["input"], obs)
            elif self.design == "A-url":
                last = self.select("SELECT * FROM last_observation WHERE url=?", (event["url"],))
                if last:
                    self.transition = "last-url-hit"
                    value = json.loads(last["value"]) if last["value"] else None
                    return decide(event["input"], Observation(None, event["url"], None, None,
                                                              None, None, None, last["status"], value, None))
        obs = self.remember(self.provider.acquire(event, edition, "request:" + event["id"]))
        return decide(event["input"], obs)

    def ingest(self, event):
        token = event["delivery_id"]
        if self.versioned and self.select("SELECT id FROM observations WHERE provider_delivery_id=?",
                                          (token,)):
            self.transition = "delivery-deduplicated"
            return
        self.remember(self.provider.acquire(event, event["edition"], token))

    def historical(self, event):
        if self.design == "C":
            row = self.select("SELECT * FROM decisions WHERE id=? AND url=?",
                              (event["target"], event["url"]))
            if row:
                return self.delivered(row, "recorded")
        if event["action"] == "reconstruct" and self.versioned:
            obs = self.observation(event["url"], event["edition"], event["key"],
                                   event.get("scope"), event["cutoff"])
            if obs and obs.kind == "value":
                return decide(event["input"], obs, "reconstructed")
        return answer("not_recorded", "hold", "delivery_unproven")

    def step(self, event):
        self.transition = ""
        self.last_fetch = None
        verb = event["action"]
        url = event["url"]
        if verb == "register":
            self.db.execute("INSERT OR IGNORE INTO links(url) VALUES (?)", (url,))
            return None
        if verb == "publish":
            self.latest[url] = event["edition"]
            return None
        if verb == "bookmark":
            link = self.select("SELECT url FROM links WHERE url=?", (url,))
            return answer("bookmark", "link", "address", link[0])
        if verb == "catalog":
            table = "observations" if self.versioned else "last_observation"
            known = self.select(f"SELECT 1 FROM {table} WHERE url=? LIMIT 1", (url,))
            return (answer("catalog", "link", "tracked_link", url) if known else
                    answer("catalog", "hold", "unobserved", url))
        if verb == "ingest":
            self.ingest(event)
            return None
        if verb in {"history", "reconstruct"}:
            return self.historical(event)
        if verb == "asof":
            obs = (self.observation(url, event["edition"], event["key"], event["scope"], event["cutoff"])
                   if self.versioned else None)
            if obs and obs.kind == "value":
                return answer("knowledge", "known", "observed_before_cutoff", obs.value, obs)
            return answer("knowledge", "unknown", "no_qualified_observation")
        if verb != "current":
            raise ValueError(verb)
        edition = self.latest[url] if event["selector"] == "latest" else event["selector"]
        result = self.current(event, edition)
        if self.design == "C":
            self.persist_decision(event, edition, result)
        return result

    def summary(self):
        logical = {}
        for name in self.tables:
            rows = self.db.execute(f"SELECT * FROM {name} ORDER BY rowid").fetchall()
            logical[name] = {"rows": len(rows), "bytes": sum(len(encoded(tuple(row)).encode()) for row in rows)}
        return {"tables": logical, "page_size": self.db.execute("PRAGMA page_size").fetchone()[0],
                "pages": self.db.execute("PRAGMA page_count").fetchone()[0]}
