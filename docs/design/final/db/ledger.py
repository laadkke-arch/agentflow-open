"""확인 장부 구조 v1 프로토타입 엔진.

이 코드는 저장 구조와 규칙(재사용, 묻기, 원리 관문, 우연 적중, 철회 전파, 과거 답 재생)을
고정 입력으로 확인하기 위한 것이다. 원문 판독과 꼬리표 작성은 사례 자료가 준다.
즉 이 코드가 보증하는 것은 "판독 결과가 주어졌을 때 기록과 전파가 맞게 일어나는가"이고,
판독 자체의 품질은 보증하지 않는다.

features로 핵심 구성요소를 끄면 구성요소 삭제 시험을 같은 코드로 돌릴 수 있다.
  drawer : 공용 장부를 프로젝트 사이·시점 사이에 재사용한다(끄면 프로젝트마다 따로 기억).
  usage  : 답 자리 → 관측 사용 쪽지로 철회를 전파한다(끄면 프로젝트의 모든 답 자리에 알림).
  split  : 판단을 비공개 쪽지로 둔다(끄면 판단이 공용 관측에 붙어 다른 프로젝트로 흐른다).
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent

# 결과를 보기 전에 고정한 영어 닫힌 기능어. 숫자만으로 된 토큰도 기능어처럼 다룬다.
FUNCTION_WORDS = frozenset("""
a an the and or but nor if then else so than too very just also as about above after again
against all any both each few more most other some such only own same up down out off once
until while during before between through because per via vs of in on at to for from by with
without into onto over under within upon is are was were be been being am do does did done
can could may might must shall should will would it its this that these those there here
which who whom whose what when where why how not no yes we you they he she i me my our your
their them us his her one ones lets let get gets got has have had having make makes made
""".split())

LADDER_TEXT = {
    "L0": "목록에 있다는 것만 확인했다",
    "L1": "소개 글이나 언급만 보았다",
    "L2": "이 판의 원문 줄에서 방법을 확인했다",
    "L3": "공개 산출물에서 그 값을 확인했다",
    "L4": "이 판에서 실행해 값을 확인했다",
    "L5": "사용자 맥락에서 확인해야 한다",
}


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fold_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def tokens(text: str) -> list[str]:
    return [t for t in re.split(r"[^0-9a-z]+", text.lower()) if len(t) >= 2]


def content_tokens(text: str) -> list[str]:
    out = []
    for t in tokens(text):
        if t in FUNCTION_WORDS or t.isdigit():
            continue
        if t not in out:
            out.append(t)
    return out


def _shift(iso: str, hours: float) -> str:
    """ISO 시각 문자열을 hours만큼 옮긴다(같은 'YYYY-MM-DDTHH:MM:SSZ' 형식)."""
    from datetime import datetime, timedelta, timezone
    t = datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc) + timedelta(hours=hours)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def stem(t: str) -> str:
    """FTS5 porter와 같은 방향의 아주 거친 어간. 일치 토큰을 보여 줄 때만 쓴다."""
    for suf in ("ations", "ation", "ions", "ion", "ings", "ing", "edly", "ed", "es", "s"):
        if t.endswith(suf) and len(t) - len(suf) >= 3:
            return t[: -len(suf)]
    return t


class PrivacyError(ValueError):
    pass


class Ledger:
    def __init__(self, path: str = ":memory:", features: dict | None = None):
        self.features = {"drawer": True, "usage": True, "split": True}
        self.features.update(features or {})
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.executescript((HERE / "schema.sql").read_text(encoding="utf-8"))
        self.projects: list[str] = []
        self.origin: dict[int, str] = {}   # drawer=False일 때만 쓰는 관측의 출처 프로젝트
        self.opens: dict[str, int] = {}    # 원문을 새로 연 횟수(요청 시계 비용)
        if not self.features["split"]:
            self.db.execute("""CREATE TABLE IF NOT EXISTS shared_judgment (
                obs_id INTEGER, project TEXT, code TEXT, verdict TEXT, role TEXT, reason TEXT, at TEXT)""")

    # ------------------------------------------------------------------ 프로젝트
    def project(self, name: str) -> str:
        alias = "p_" + re.sub(r"[^0-9a-zA-Z_]", "_", name)
        if alias not in self.projects:
            self.db.execute(f"ATTACH DATABASE ':memory:' AS {alias}")
            ddl = (HERE / "project_schema.sql").read_text(encoding="utf-8").replace("{p}", alias)
            self.db.executescript(ddl)
            self.projects.append(alias)
        return alias

    # ------------------------------------------------------------------ 공용 장부 쓰기
    def _locator(self, url: str, at: str, via: str) -> int:
        self.db.execute(
            "INSERT OR IGNORE INTO locator(url, first_seen_at, first_seen_via) VALUES (?,?,?)",
            (url, at, via))
        return self.db.execute("SELECT locator_id FROM locator WHERE url=?", (url,)).fetchone()[0]

    def _edition(self, locator_id: int, key: str, kind: str, published_at, at: str) -> int:
        self.db.execute(
            "INSERT OR IGNORE INTO edition(locator_id, edition_key, kind, published_at, first_seen_at)"
            " VALUES (?,?,?,?,?)", (locator_id, key, kind, published_at, at))
        return self.db.execute(
            "SELECT edition_id FROM edition WHERE locator_id=? AND edition_key=?",
            (locator_id, key)).fetchone()[0]

    def receipt(self, runtime: str, program_sha256: str, inp: dict, out: dict, ran_at: str) -> int:
        body = json.dumps(out, ensure_ascii=False, sort_keys=True)
        key = sha256("|".join([runtime, program_sha256, json.dumps(inp, sort_keys=True), body]))
        self.db.execute(
            "INSERT OR IGNORE INTO receipt(runtime, program_sha256, input_json, output_json, ran_at, idem_key)"
            " VALUES (?,?,?,?,?,?)",
            (runtime, program_sha256, json.dumps(inp, sort_keys=True), body, ran_at, key))
        return self.db.execute("SELECT receipt_id FROM receipt WHERE idem_key=?", (key,)).fetchone()[0]

    def observe(self, *, url, edition_key, edition_kind, position, at, method, outcome="content",
                quote=None, quote_lang=None, statement, flip_position=None, receipt_id=None,
                published_at=None, via="request", evidence_ref=None, project=None) -> tuple[int, bool]:
        """관측을 남긴다. 같은 (판, 위치, 결과, 인용 지문, 방법, 영수증)이면 새 행 대신 sighting을 더한다."""
        with self.db:
            loc = self._locator(url, at, via)
            ed = self._edition(loc, edition_key, edition_kind, published_at, at)
            fp = sha256(fold_ws(quote)) if quote else None
            parts = [ed, position, outcome, fp, method, receipt_id]
            if not self.features["drawer"] and project:
                parts.append(project)   # 서랍을 끄면 프로젝트마다 따로 기억한다
            key = sha256("|".join(map(str, parts)))
            row = self.db.execute("SELECT obs_id FROM observation WHERE idem_key=?", (key,)).fetchone()
            if row:
                self.db.execute("INSERT OR IGNORE INTO sighting(obs_id, seen_at, via) VALUES (?,?,?)",
                                (row[0], at, via if via != "operator" else "request"))
                return row[0], False
            cur = self.db.execute(
                "INSERT INTO observation(edition_id, position, observed_at, method, outcome, quote, quote_lang,"
                " quote_fp, statement, evidence_ref, flip_position, receipt_id, idem_key)"
                " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (ed, position, at, method, outcome, quote, quote_lang, fp, statement, evidence_ref,
                 flip_position, receipt_id, key))
            obs_id = cur.lastrowid
            if project:
                self.origin[obs_id] = project
                if method in ("read_line", "executed"):
                    self.opens[project] = self.opens.get(project, 0) + 1
            return obs_id, True

    def tag(self, obs_id: int, slot: str, height: str, lang: str, text: str, *,
            audience=None, written_from="source_quote") -> int:
        """꼬리표를 붙인다. 어느 프로젝트 요청 원문에만 있고 원문 쪽에는 없는 내용어가 들어 있으면 거절한다."""
        self._privacy_lint(obs_id, text)
        with self.db:
            self.db.execute(
                "INSERT OR IGNORE INTO tag(obs_id, slot, height, lang, text, audience, written_from)"
                " VALUES (?,?,?,?,?,?,?)", (obs_id, slot, height, lang, text, audience, written_from))
        return self.db.execute(
            "SELECT tag_id FROM tag WHERE obs_id=? AND slot=? AND height=? AND lang=? AND text=?",
            (obs_id, slot, height, lang, text)).fetchone()[0]

    def _privacy_lint(self, obs_id: int, text: str):
        obs = self.db.execute("SELECT quote, statement FROM observation WHERE obs_id=?", (obs_id,)).fetchone()
        source_side = set(content_tokens((obs["quote"] or "") + " " + obs["statement"]))
        for p in self.projects:
            for r in self.db.execute(f"SELECT text FROM {p}.request_rev"):
                private = set(content_tokens(r["text"])) - source_side
                leaked = [t for t in content_tokens(text) if t in private and len(t) >= 5]
                # 요청에만 있는 긴 내용어가 둘 이상 들어가면 요청 문장을 옮겨 적은 것으로 본다.
                if len(leaked) >= 2:
                    raise PrivacyError(f"tag repeats request-only words {leaked} from {p}")

    def contrast(self, left_obs, right_obs, condition, left_value, right_value, receipt_id=None) -> None:
        with self.db:
            self.db.execute(
                "INSERT OR IGNORE INTO contrast(left_obs, right_obs, condition, left_value, right_value, receipt_id)"
                " VALUES (?,?,?,?,?,?)", (left_obs, right_obs, condition, left_value, right_value, receipt_id))

    def supersede(self, old_obs, new_obs, effect, known_from, effective_from=None) -> None:
        with self.db:
            self.db.execute(
                "INSERT OR IGNORE INTO supersession(old_obs, new_obs, effect, effective_from, known_from)"
                " VALUES (?,?,?,?,?)", (old_obs, new_obs, effect, effective_from, known_from))

    def alias(self, from_url: str, to_url: str, kind: str, at: str, evidence_obs=None) -> int:
        with self.db:
            a = self._locator(from_url, at, "operator")
            b = self._locator(to_url, at, "operator")
            return self.db.execute(
                "INSERT INTO locator_alias(from_id, to_id, kind, asserted_at, evidence_obs) VALUES (?,?,?,?,?)",
                (a, b, kind, at, evidence_obs)).lastrowid

    def cancel_alias(self, alias_id: int, at: str, reason: str) -> None:
        with self.db:
            self.db.execute("INSERT INTO locator_alias_cancel(alias_id, cancelled_at, reason) VALUES (?,?,?)",
                            (alias_id, at, reason))

    def resolve(self, url: str, at: str) -> str:
        """취소되지 않은 별칭을 따라 지금 열 주소를 돌려준다. 과거 인용은 원 주소 그대로 둔다."""
        seen = {url}
        while True:
            row = self.db.execute(
                "SELECT l2.url FROM locator l1 JOIN locator_alias a ON a.from_id=l1.locator_id"
                " JOIN locator l2 ON l2.locator_id=a.to_id"
                " WHERE l1.url=? AND a.asserted_at<=? AND a.alias_id NOT IN"
                " (SELECT alias_id FROM locator_alias_cancel WHERE cancelled_at<=?)"
                " ORDER BY a.asserted_at DESC LIMIT 1", (url, at, at)).fetchone()
            if not row or row[0] in seen:
                return url
            url = row[0]
            seen.add(url)

    def latest_edition(self, url: str, at: str) -> str | None:
        """쓴 순서가 아니라 발행 시각(모르면 처음 본 시각) 순으로 최신 판을 고른다."""
        row = self.db.execute(
            "SELECT e.edition_key FROM edition e JOIN locator l USING(locator_id) WHERE l.url=? AND e.first_seen_at<=?"
            " ORDER BY COALESCE(e.published_at, e.first_seen_at) DESC, e.edition_id DESC LIMIT 1",
            (url, at)).fetchone()
        return row[0] if row else None

    # ------------------------------------------------------------------ 변경 채널
    def channel(self, supplier: str, url: str, kind: str, period_h: int = 72) -> int:
        with self.db:
            self.db.execute("INSERT OR IGNORE INTO channel(supplier, url, kind, period_h) VALUES (?,?,?,?)",
                            (supplier, url, kind, period_h))
        return self.db.execute("SELECT channel_id FROM channel WHERE url=?", (url,)).fetchone()[0]

    def watch(self, obs_id: int, channel_url: str, match_key: str = "", *, layer="same_address",
              deadline: str | None = None) -> None:
        ch = self.db.execute("SELECT channel_id FROM channel WHERE url=?", (channel_url,)).fetchone()[0]
        with self.db:
            self.db.execute("INSERT OR IGNORE INTO watch(obs_id, channel_id, match_key, layer, deadline)"
                            " VALUES (?,?,?,?,?)", (obs_id, ch, match_key, layer, deadline))

    def _enqueue(self, obs_id: int, cause: str, cause_ref: str, at: str) -> bool:
        """같은 관측에 열린 작업이 있으면 새 원인을 거기에 합친다(기한 작업과 채널 항목이 같은 날 오면 하나)."""
        open_job = self.db.execute(
            "SELECT job_id, merged_causes FROM recheck_job WHERE obs_id=? AND state IN ('queued','leased')",
            (obs_id,)).fetchone()
        if open_job:
            ref = f"{cause}:{cause_ref}"
            merged = [m for m in open_job["merged_causes"].split(",") if m]
            if ref not in merged:
                self.db.execute("UPDATE recheck_job SET merged_causes=? WHERE job_id=?",
                                (",".join(merged + [ref]), open_job["job_id"]))
            return False
        cur = self.db.execute(
            "INSERT OR IGNORE INTO recheck_job(obs_id, cause, cause_ref, enqueued_at) VALUES (?,?,?,?)",
            (obs_id, cause, cause_ref, at))
        return cur.rowcount == 1   # 새 작업을 만들었을 때만 True

    def due(self, at: str) -> int:
        """공지 기한 24시간 전과 기한 시각에 직접 읽는 작업을 만든다. 기한 경과만으로 관측을 무효로 하지 않는다."""
        n = 0
        with self.db:
            rows = self.db.execute(
                "SELECT obs_id, deadline FROM watch WHERE deadline IS NOT NULL AND obs_id NOT IN"
                " (SELECT old_obs FROM supersession WHERE known_from<=?)", (at,)).fetchall()
            for w in rows:
                for ref, when in (("T-24h", _shift(w["deadline"], -24)), ("T", w["deadline"])):
                    if when <= at and self._enqueue(w["obs_id"], "deadline", f"{w['deadline']}#{ref}", at):
                        n += 1
        return n

    def reuse_gate(self, obs_id: int, at: str) -> dict:
        """요청 시계에서 재사용 관측을 다시 열지 않아도 되는가. 다섯 조건이 모두 참이면 다시 열지 않는다.
        (1) 감시 채널 커서가 주기의 2배 안에서 성공 (2) 열린 재확인 작업 없음 (3) 공지 기한이 24시간 안에 오지 않음
        (4) 감시가 주장과 같은 층(감시를 달 때 확인 단계가 보증) (5) 마지막 직접 확인이 168시간 안."""
        why = []
        ws = self.db.execute(
            "SELECT w.*, c.last_polled_at, c.period_h, c.url AS ch_url FROM watch w JOIN channel c USING(channel_id)"
            " WHERE w.obs_id=?", (obs_id,)).fetchall()
        if not ws:
            why.append("감시 없음")
        for w in ws:
            if not w["last_polled_at"] or w["last_polled_at"] < _shift(at, -2 * w["period_h"]):
                why.append(f"채널 커서가 늙음({w['ch_url']})")
            if w["deadline"] and _shift(w["deadline"], -24) <= at:
                why.append(f"공지 기한 {w['deadline']} 임박 또는 경과")
        if self.db.execute("SELECT 1 FROM recheck_job WHERE obs_id=? AND state IN ('queued','leased')",
                           (obs_id,)).fetchone():
            why.append("처리 안 된 재확인 작업")
        last = self.db.execute(
            "SELECT max(t) FROM (SELECT observed_at AS t FROM observation WHERE obs_id=?"
            " UNION ALL SELECT seen_at FROM sighting WHERE obs_id=?)", (obs_id, obs_id)).fetchone()[0]
        if last < _shift(at, -168):
            why.append("마지막 직접 확인이 168시간보다 오래됨")
        polled = [w["last_polled_at"] for w in ws if w["last_polled_at"]]
        return {"decision": "reopen" if why else "reuse", "why": why,
                "basis": None if why else f"채널 확인 시각 {max(polled)}"}

    def poll(self, channel_url: str, listing: list[dict], at: str) -> list[dict]:
        """채널 목록 전체를 받아 외부 ID 집합의 차분만 새 항목으로 넣고, 닿는 관측의 재확인 작업을 만든다."""
        ch = self.db.execute("SELECT channel_id FROM channel WHERE url=?", (channel_url,)).fetchone()[0]
        known = {r[0] for r in self.db.execute(
            "SELECT external_id FROM channel_item WHERE channel_id=?", (ch,))}
        new = [it for it in listing if it["id"] not in known]
        with self.db:
            for it in new:
                self.db.execute(
                    "INSERT INTO channel_item(channel_id, external_id, first_seen_at, title, summary, locator_url,"
                    " edition_key) VALUES (?,?,?,?,?,?,?)",
                    (ch, it["id"], at, it["title"], it.get("summary"), it.get("url"), it.get("edition")))
                active = self.db.execute(
                    "SELECT obs_id, match_key FROM watch WHERE channel_id=? AND obs_id NOT IN"
                    " (SELECT old_obs FROM supersession WHERE known_from<=?)", (ch, at)).fetchall()
                for w in active:
                    hay = (it["title"] + " " + (it.get("summary") or "")).lower()
                    if w["match_key"] and w["match_key"].lower() not in hay:
                        continue
                    self._enqueue(w["obs_id"], "channel", f"{channel_url}#{it['id']}", at)
            self.db.execute("UPDATE channel SET last_polled_at=?, last_item_count=? WHERE channel_id=?",
                            (at, len(listing), ch))
        return new

    def jobs(self, state="queued") -> list[sqlite3.Row]:
        return self.db.execute("SELECT * FROM recheck_job WHERE state=? ORDER BY job_id", (state,)).fetchall()

    def lease(self, job_id: int, until: str) -> bool:
        """작업자 둘이 같은 작업을 잡지 않게 한다. 이미 잡혔으면 False."""
        with self.db:
            cur = self.db.execute(
                "UPDATE recheck_job SET state='leased', lease_until=?, attempts=attempts+1"
                " WHERE job_id=? AND state='queued'", (until, job_id))
        return cur.rowcount == 1

    def finish(self, job_id: int, result_obs: int | None, ok=True) -> None:
        with self.db:
            self.db.execute("UPDATE recheck_job SET state=?, result_obs=? WHERE job_id=?",
                            ("done" if ok else "failed", result_obs, job_id))

    def release_expired(self, now: str) -> int:
        with self.db:
            cur = self.db.execute(
                "UPDATE recheck_job SET state='queued' WHERE state='leased' AND lease_until < ?", (now,))
        return cur.rowcount

    # ------------------------------------------------------------------ 공용 장부 읽기
    def obs(self, obs_id: int) -> sqlite3.Row:
        return self.db.execute(
            "SELECT o.*, e.edition_key, e.published_at, l.url FROM observation o"
            " JOIN edition e USING(edition_id) JOIN locator l USING(locator_id) WHERE o.obs_id=?",
            (obs_id,)).fetchone()

    def link(self, obs_id: int) -> str:
        o = self.obs(obs_id)
        if o["method"] == "executed":
            r = self.db.execute("SELECT runtime FROM receipt WHERE receipt_id=?", (o["receipt_id"],)).fetchone()
            return f"실행 영수증 receipts/r1_queue.py ({r['runtime']}, {o['position'].split()[-1]})"
        url = o["url"]
        if "/blob/main/" in url:
            url = url.replace("/blob/main/", f"/blob/{o['edition_key']}/")
        m = re.search(r"L(\d+)(?:[–-](\d+))?", o["position"])
        if m and "github.com" in url:
            url += f"#L{m.group(1)}" + (f"-L{m.group(2)}" if m.group(2) else "")
        return url

    def reusable(self, url: str, edition_key: str, position: str, project: str | None = None):
        """같은 판·같은 위치의 관측이 있으면 돌려준다. 판이 다르면 None(그 판을 다시 열어야 한다)."""
        row = self.db.execute(
            "SELECT o.obs_id FROM observation o JOIN edition e USING(edition_id) JOIN locator l USING(locator_id)"
            " WHERE l.url=? AND e.edition_key=? AND o.position=? ORDER BY o.obs_id DESC LIMIT 1",
            (url, edition_key, position)).fetchone()
        if not row:
            return None
        if not self.features["drawer"] and project and self.origin.get(row[0]) != project:
            return None
        return row[0]

    def current(self, obs_id: int, at: str) -> int:
        """at 시각까지 알려진 대체를 따라가 그때의 최신 관측을 돌려준다(그날 알 수 있던 것)."""
        seen = {obs_id}
        cur = obs_id
        while True:
            nxt = self.db.execute(
                "SELECT new_obs FROM supersession WHERE old_obs=? AND known_from<=? ORDER BY known_from DESC LIMIT 1",
                (cur, at)).fetchone()
            if not nxt or nxt[0] in seen:
                return cur
            cur = nxt[0]
            seen.add(cur)

    def known_on(self, url: str, at: str) -> sqlite3.Row | None:
        """그 주소에 대해 at 시각까지 우리가 본 가장 늦은 관측."""
        return self.db.execute(
            "SELECT o.*, e.edition_key FROM observation o JOIN edition e USING(edition_id)"
            " JOIN locator l USING(locator_id) WHERE l.url=? AND o.observed_at<=?"
            " ORDER BY o.observed_at DESC, o.obs_id DESC LIMIT 1", (url, at)).fetchone()

    # ------------------------------------------------------------------ 접수
    def intake(self, p: str, *, request_key, rev, at, text, selected_part, requirements,
               context=None, prior=None, needs=None) -> int:
        """요청판을 한 번에 쓴다. 같은 내용 재전송은 같은 req_id, 같은 판의 다른 내용은 거절."""
        body = json.dumps([text, selected_part, requirements, context, needs], ensure_ascii=False, sort_keys=True)
        key = sha256(f"{request_key}|{rev}|{body}")
        row = self.db.execute(f"SELECT req_id, idem_key FROM {p}.request_rev WHERE request_key=? AND rev=?",
                              (request_key, rev)).fetchone()
        if row:
            if row["idem_key"] != key:
                raise ValueError("same request revision with different content; make a new revision")
            return row["req_id"]
        with self.db:
            cur = self.db.execute(
                f"INSERT INTO {p}.request_rev(request_key, rev, received_at, text, selected_part, idem_key)"
                " VALUES (?,?,?,?,?,?)", (request_key, rev, at, text, selected_part, key))
            req = cur.lastrowid
            for r in requirements:
                self.db.execute(
                    f"INSERT INTO {p}.requirement(req_id, code, kind, text, provenance, stamped_at) VALUES (?,?,?,?,?,?)",
                    (req, r["code"], r["kind"], r["text"], r.get("provenance", "explicit"), at))
            for k, v in (context or {}).items():
                self.db.execute(
                    f"INSERT INTO {p}.context_fact(req_id, key, value, provenance, source_ref, stamped_at)"
                    " VALUES (?,?,?,?,?,?)", (req, k, v["value"], v["provenance"], v.get("source"), at))
            if prior is not None:
                state = prior.get("state", "given") if isinstance(prior, dict) else "given"
                items = json.dumps(prior, ensure_ascii=False, sort_keys=True)
                self.db.execute(
                    f"INSERT INTO {p}.prior_seal(req_id, sealed_at, state, items_json, sha256) VALUES (?,?,?,?,?)",
                    (req, at, state, items, sha256(items)))
            for n in needs or []:
                self.db.execute(f"INSERT INTO {p}.need(req_id, slot, lang, text) VALUES (?,?,?,?)",
                                (req, n["slot"], n["lang"], n["text"]))
        return req

    def context(self, p: str, req: int) -> dict:
        return {r["key"]: r["value"] for r in self.db.execute(
            f"SELECT key, value FROM {p}.context_fact WHERE req_id=?", (req,))}

    @staticmethod
    def decide(first_section_a: str, first_section_b: str, *, fields_settle=False, common_action=False,
               studio_can_fetch=False, execution_can_settle=False, irreversible=False) -> str:
        """묻기 규칙. 두 해석의 첫 절이 같으면 진행. 다르면
        0단계 요청판 재독(다른 명시 칸이 해석을 정하면 고르고 답 첫 줄에 밝힘) →
        1단계 공통 행동(두 해석을 함께 채우고 범위 밖을 어기지 않는 행동) →
        Studio 회수 → 실행 확인 → 되돌릴 수 없을 때만 한 번 묻기 → 조건부 두 링크."""
        if first_section_a == first_section_b:
            return "proceed"
        if fields_settle:
            return "reread"
        if common_action:
            return "common"
        if studio_can_fetch:
            return "fetch"
        if execution_can_settle:
            return "verify"
        if irreversible:
            return "ask_once"
        return "conditional"

    def interpret(self, p, req, code, chosen, other, decision, at, question=None, answer=None):
        with self.db:
            self.db.execute(
                f"INSERT OR REPLACE INTO {p}.interpretation(req_id, code, chosen, other, decision, question, answer, decided_at)"
                " VALUES (?,?,?,?,?,?,?,?)", (req, code, chosen, other, decision, question, answer, at))

    # ------------------------------------------------------------------ 찾기
    def search_drawer(self, p: str, req: int, at: str, *, k=10, min_slots=2,
                      include_function_words=False, log=True) -> list[dict]:
        """서랍 검색. 필요 문장과 꼬리표를 같은 칸끼리 맞춘다. at 이전에 관측된 것만 본다.
        min_slots 칸 이상 내용어가 맞아야 후보로 올리고, 맞은 토큰이 기능어뿐이면 우연 적중으로 표시한다."""
        if not self.features["drawer"]:
            return []
        needs = self.db.execute(f"SELECT slot, lang, text FROM {p}.need WHERE req_id=?", (req,)).fetchall()
        per_obs: dict[int, dict] = {}
        for n in needs:
            toks = tokens(n["text"]) if include_function_words else content_tokens(n["text"])
            toks = [t for t in dict.fromkeys(toks) if not t.isdigit() or include_function_words]
            if not toks:
                continue
            q = " OR ".join(f'"{t}"' for t in toks)
            slot_filter = "" if n["slot"] == "summary" else "AND (t.slot=? OR t.slot='summary')"
            args = [q, at] + ([] if n["slot"] == "summary" else [n["slot"]])
            rows = self.db.execute(
                "SELECT t.tag_id, t.obs_id, t.slot, t.text, bm25(tag_fts) AS score FROM tag_fts"
                " JOIN tag t ON t.tag_id = tag_fts.rowid JOIN observation o ON o.obs_id = t.obs_id"
                f" WHERE tag_fts MATCH ? AND o.observed_at <= ? {slot_filter}", args).fetchall()
            for r in rows:
                tag_stems = {stem(x) for x in tokens(r["text"])}
                matched = [t for t in toks if stem(t) in tag_stems]
                if not matched:
                    continue
                d = per_obs.setdefault(r["obs_id"], {"obs_id": r["obs_id"], "score": 0.0, "slots": set(),
                                                     "matched": []})
                d["score"] += r["score"]
                d["slots"].add(n["slot"] if n["slot"] != "summary" else r["slot"])
                d["matched"] += [m for m in matched if m not in d["matched"]]
        hits = []
        for d in per_obs.values():
            d["lexical_accident"] = all(m in FUNCTION_WORDS or m.isdigit() for m in d["matched"])
            content_slots = len(d["slots"]) if not d["lexical_accident"] else 0
            distinct = {stem(m) for m in d["matched"] if m not in FUNCTION_WORDS}
            d["eligible"] = (content_slots >= min_slots and len(distinct) >= 2) or \
                            (min_slots <= 1 and content_slots >= 1)
            hits.append(d)
        hits.sort(key=lambda d: (not d["eligible"], d["lexical_accident"], d["score"]))
        hits = hits[:k]
        if not log:   # 진단용 검색(기능어 포함 감사 등)은 탐색 기록에 남기지 않는다
            for i, d in enumerate(hits, 1):
                d["rank"] = i
                d["slots"] = sorted(d["slots"])
            return hits
        with self.db:
            sid = self.db.execute(
                f"INSERT INTO {p}.search_run(req_id, path, query, ran_at) VALUES (?,?,?,?)",
                (req, "drawer", json.dumps([dict(n) for n in needs], ensure_ascii=False), at)).lastrowid
            for i, d in enumerate(hits, 1):
                self.db.execute(
                    f"INSERT INTO {p}.search_hit(search_id, rank, url, obs_id, matched_tokens, lexical_accident,"
                    " eligible) VALUES (?,?,?,?,?,?,?)",
                    (sid, i, self.obs(d["obs_id"])["url"], d["obs_id"], ",".join(d["matched"]),
                     int(d["lexical_accident"]), int(d["eligible"])))
                d["rank"] = i
                d["slots"] = sorted(d["slots"])
        return hits

    def search_fresh(self, p: str, req: int, at: str, branch_results: dict[str, list[dict]]) -> list[dict]:
        """새 검색. 실제 검색은 바깥 도구가 하고, 여기서는 갈래별 결과를 기록한다(고정 자료)."""
        out = []
        with self.db:
            for branch, results in branch_results.items():
                sid = self.db.execute(
                    f"INSERT INTO {p}.search_run(req_id, path, query, ran_at) VALUES (?,?,?,?)",
                    (req, "fresh", branch, at)).lastrowid
                for i, r in enumerate(results, 1):
                    self.db.execute(
                        f"INSERT INTO {p}.search_hit(search_id, rank, url, obs_id, matched_tokens, lexical_accident)"
                        " VALUES (?,?,?,?,?,?)", (sid, i, r["url"], None, r.get("why", ""), 0))
                    out.append({"branch": branch, "rank": i, **r})
        return out

    def path_log(self, p: str, req: int) -> dict:
        """서랍만 찾은 것, 새 검색만 찾은 것, 둘 다 찾은 것(주소 기준)."""
        rows = self.db.execute(
            f"SELECT r.path, h.url, h.lexical_accident, h.eligible FROM {p}.search_hit h"
            f" JOIN {p}.search_run r USING(search_id) WHERE r.req_id=?", (req,)).fetchall()
        drawer = {r["url"] for r in rows if r["path"] == "drawer" and r["eligible"] and not r["lexical_accident"]}
        fresh = {r["url"] for r in rows if r["path"] == "fresh"}
        return {"drawer_only": sorted(drawer - fresh), "fresh_only": sorted(fresh - drawer),
                "both": sorted(drawer & fresh)}

    # ------------------------------------------------------------------ 판정
    def judge(self, p: str, req: int, code: str, obs_id: int, verdict: str, role: str, ladder: str,
              reason: str, at: str, *, premises=None, cause="initial", supersedes=None) -> int:
        with self.db:
            sid = self.db.execute(
                f"INSERT INTO {p}.slip(req_id, code, obs_id, verdict, role, ladder, reason, premises, written_at,"
                " cause, supersedes) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (req, code, obs_id, verdict, role, ladder, reason,
                 json.dumps(premises or {}, ensure_ascii=False, sort_keys=True), at, cause, supersedes)).lastrowid
            if not self.features["split"]:
                self.db.execute("INSERT INTO shared_judgment VALUES (?,?,?,?,?,?,?)",
                                (obs_id, p, code, verdict, role, reason, at))
        return sid

    def inherited(self, p: str, obs_id: int) -> list[sqlite3.Row]:
        """split=False일 때 다른 프로젝트의 판단이 이 프로젝트로 흘러드는 것을 보여 준다."""
        if self.features["split"]:
            return []
        return self.db.execute("SELECT * FROM shared_judgment WHERE obs_id=? AND project<>?",
                               (obs_id, p)).fetchall()

    def carry_slips(self, p: str, old_req: int, new_req: int, at: str, edition_of) -> dict:
        """같은 요청의 새 판에서 지난 쪽지를 옮긴다. 요건 사실이 모두 같고 관측 판이 지금 판과 맞을 때만."""
        ctx = self.context(p, new_req)
        kept, dropped = [], []
        for s in self.db.execute(f"SELECT * FROM {p}.slip WHERE req_id=? ORDER BY slip_id", (old_req,)).fetchall():
            prem = json.loads(s["premises"])
            ok = all(ctx.get(k) == v for k, v in prem.items())
            ed_ok = edition_of(self.obs(s["obs_id"]), ctx)
            if ok and ed_ok:
                kept.append(self.judge(p, new_req, s["code"], s["obs_id"], s["verdict"], s["role"], s["ladder"],
                                       s["reason"], at, premises=prem, cause="request", supersedes=s["slip_id"]))
            else:
                dropped.append({"slip": s["slip_id"], "code": s["code"], "obs": s["obs_id"],
                                "premise_mismatch": [k for k, v in prem.items() if ctx.get(k) != v],
                                "edition_mismatch": not ed_ok})
        return {"kept": kept, "dropped": dropped}

    @staticmethod
    def gate(*, role_map: list[tuple[str, str]], invariant_quote: str | None, break_input: str | None,
             baseline_prediction: str | None, principle_prediction: str | None,
             target_doc_states_it: bool) -> dict:
        """원리 관문. ① 역할 대응 ② 원문 절로 인용한 유지 성질 ③ 동종 기준선과 예측이 다른 깨지는 입력.
        대상 1차 문서가 이미 같은 관계를 말하면 ③은 성립하지 않는다(258 LOD API, 257 API 절)."""
        failed = []
        if not role_map:
            failed.append("역할 대응 없음")
        if not invariant_quote:
            failed.append("유지 성질을 원문 절로 인용하지 못함")
        if not break_input:
            failed.append("깨지는 입력 없음")
        elif target_doc_states_it or baseline_prediction == principle_prediction:
            failed.append("동종 기준선과 예측이 같음")
        if not failed:
            return {"decision": "open", "failed": []}
        if break_input and not role_map:
            return {"decision": "explain", "failed": failed}
        return {"decision": "fold_test" if break_input else "explain", "failed": failed}

    # ------------------------------------------------------------------ 조합
    def compose(self, p: str, req: int, at: str, *, slots: list[dict], folded=(), status="complete",
                next_action=None, budget=None, readback=None) -> int:
        """답 실행·자리·문장·사용 쪽지를 한 거래로 쓴다. 같은 내용 재전송은 같은 run_id."""
        body = json.dumps([slots, list(folded), status, next_action, readback], ensure_ascii=False, sort_keys=True)
        key = sha256(f"{req}|{body}")
        row = self.db.execute(f"SELECT run_id FROM {p}.answer_run WHERE idem_key=?", (key,)).fetchone()
        if row:
            return row[0]
        searched = {r[0] for r in self.db.execute(
            f"SELECT h.url FROM {p}.search_hit h JOIN {p}.search_run r USING(search_id) WHERE r.req_id=?", (req,))}
        for s in slots:
            if s.get("kind") == "check" and s.get("first") and self.obs(s["first"])["url"] not in searched:
                raise ValueError("확인할 후보도 탐색 기록에 있는 이름만 낸다(모델 기억에서만 나온 이름 금지)")
        with self.db:
            run = self.db.execute(
                f"INSERT INTO {p}.answer_run(req_id, produced_at, status, budget_json, next_action, idem_key)"
                " VALUES (?,?,?,?,?,?)",
                (req, at, status, json.dumps(budget or {}, ensure_ascii=False), next_action, key)).lastrowid
            if readback:
                self.db.execute(
                    f"INSERT INTO {p}.answer_slot(run_id, slot_no, kind, sentence, ladder, hold) VALUES (?,?,?,?,?,?)",
                    (run, 0, "check", "해석: " + readback, "L5", "해석이 다르면 알려 주세요"))
            for i, s in enumerate(slots, 1):
                self.db.execute(
                    f"INSERT INTO {p}.answer_slot(run_id, slot_no, kind, sentence, ladder, hold) VALUES (?,?,?,?,?,?)",
                    (run, i, s["kind"], self.sentence(s), s["ladder"], s["hold"]))
                for part, ids in (("first_link", [s.get("first")]), ("support", s.get("support", [])),
                                  ("flip", s.get("flip", [])), ("contrast", s.get("contrast", []))):
                    for oid in ids:
                        if oid:
                            self.db.execute(
                                f"INSERT OR IGNORE INTO {p}.usage(run_id, slot_no, obs_id, part) VALUES (?,?,?,?)",
                                (run, i, oid, part))
            for f in folded:
                self.db.execute(
                    f"INSERT OR IGNORE INTO {p}.folded(run_id, url, obs_id, condition, reason) VALUES (?,?,?,?,?)",
                    (run, f["url"], f.get("obs"), f["condition"], f["reason"]))
        return run

    def show(self, p: str, run_id: int, slot_no: int, at: str) -> None:
        """노출 기록. 봉인 행(given/declined/none)이 먼저 있어야 한다. 그래야 '새로 알았나'를 셀 수 있다."""
        req = self.db.execute(f"SELECT req_id FROM {p}.answer_run WHERE run_id=?", (run_id,)).fetchone()[0]
        if not self.db.execute(f"SELECT 1 FROM {p}.prior_seal WHERE req_id=?", (req,)).fetchone():
            raise ValueError("봉인 전에는 노출하지 않는다")
        with self.db:
            self.db.execute(f"INSERT OR IGNORE INTO {p}.exposure(run_id, slot_no, event, at) VALUES (?,?,?,?)",
                            (run_id, slot_no, "shown", at))

    def sentence(self, s: dict) -> str:
        link = self.link(s["first"]) if s.get("first") else s.get("url", "주소 미확인")
        lad = LADDER_TEXT[s["ladder"]]
        if s["kind"] == "direct":
            withs = f" 함께 필요한 것: {s['with']}." if s.get("with") else ""
            return (f"{s['verb']}. 첫 원문: {link} ({s['where']}). 이유: {s['reason']}. "
                    f"근거 수준: {lad}.{withs} 철회 조건: {s['hold']}.")
        if s["kind"] == "transplant":
            return (f"이식할 부분: {s['verb']}. 첫 원문: {link} ({s['where']}). 맞는 칸: {s['reason']}. "
                    f"함께 필요한 것: {s.get('with', '없음')}. 근거 수준: {lad}. 철회 조건: {s['hold']}.")
        if s["kind"] == "principle":
            return (f"시험할 원리: {s['verb']}. 첫 원문: {link} ({s['where']}). 빌릴 것: {s['borrow']}. "
                    f"대상에서 다시 확인할 것: {s['recheck']}. 깨지는 입력: {s['break']}. 근거 수준: {lad}. "
                    f"철회 조건: {s['hold']}.")
        if s["kind"] == "test":
            return f"실패 시험 하나(접음): {s['verb']}. 원문: {link}. 이유: {s['reason']}."
        if s["kind"] == "reference":
            return f"같은 모양의 선례(참고): {s['verb']}. 원문: {link}. 맞는 것과 맞지 않는 것: {s['reason']}."
        if s["kind"] == "check":
            withs = f" 함께 필요한 것: {s['with']}." if s.get("with") else ""
            hold = f" 보류: {s['hold']}." if s.get("hold") else ""
            return (f"확인할 후보: {s['verb']}. 먼저 열 원문: {link}. 확인할 한 가지: {s['reason']}. "
                    f"근거 수준: {lad}.{withs}{hold}")
        raise ValueError(s["kind"])

    # ------------------------------------------------------------------ 전파와 재생
    def ancestors(self, obs_id: int) -> list[int]:
        """대체 사슬을 거슬러 올라간 관측들(자기 자신 포함). 답 자리는 사슬의 어느 고리를 인용했어도 영향을 받는다."""
        out, todo = [], [obs_id]
        while todo:
            o = todo.pop()
            if o in out:
                continue
            out.append(o)
            todo += [r[0] for r in self.db.execute("SELECT old_obs FROM supersession WHERE new_obs=?", (o,))]
        return out

    def propagate(self, p: str, at: str) -> list[dict]:
        """at까지 알려진 대체 가운데 이 프로젝트 답 자리에 닿는 것만 알림으로 만든다.
        usage=False이면 어느 자리가 무엇을 인용했는지 모르므로 프로젝트의 모든 답 자리에 알린다."""
        out = []
        sups = self.db.execute("SELECT * FROM supersession WHERE known_from<=? ORDER BY known_from",
                               (at,)).fetchall()
        with self.db:
            for s in sups:
                if self.features["usage"]:
                    chain = self.ancestors(s["old_obs"])
                    marks = ",".join("?" * len(chain))
                    targets = self.db.execute(
                        f"SELECT DISTINCT u.run_id, u.slot_no FROM {p}.usage u JOIN {p}.answer_run r USING(run_id)"
                        f" WHERE u.obs_id IN ({marks}) AND u.part<>'contrast' AND r.produced_at<=?",
                        (*chain, s["known_from"])).fetchall()
                else:
                    targets = self.db.execute(
                        f"SELECT a.run_id, a.slot_no FROM {p}.answer_slot a JOIN {p}.answer_run r USING(run_id)"
                        " WHERE a.slot_no>0 AND r.produced_at<=?", (s["known_from"],)).fetchall()
                for t in targets:
                    new = self.obs(s["new_obs"])
                    label = {"invalidates": "근거 무효", "changes_value": "값 바뀜", "confirms": "다시 확인됨"}[s["effect"]]
                    text = f"{label}: {new['statement']} (알게 된 시각 {s['known_from']})"
                    cur = self.db.execute(
                        f"INSERT OR IGNORE INTO {p}.notice(run_id, slot_no, old_obs, new_obs, effect, created_at, text)"
                        " VALUES (?,?,?,?,?,?,?)",
                        (t["run_id"], t["slot_no"], s["old_obs"], s["new_obs"], s["effect"], s["known_from"], text))
                    if cur.rowcount:
                        out.append({"run": t["run_id"], "slot": t["slot_no"], "effect": s["effect"], "text": text})
        return out

    def note(self, p: str, run_id: int, slot_no: int, old_obs: int, new_obs: int, effect: str, at: str,
             text: str) -> None:
        """요청판이 바뀌어(사용자 쪽 사실 변화) 지난 답 자리가 대체될 때 남기는 알림."""
        with self.db:
            self.db.execute(
                f"INSERT OR IGNORE INTO {p}.notice(run_id, slot_no, old_obs, new_obs, effect, created_at, text)"
                " VALUES (?,?,?,?,?,?,?)", (run_id, slot_no, old_obs, new_obs, effect, at, text))

    def replay(self, p: str, run_id: int, at: str | None = None) -> dict:
        """지난 답을 당시 문장과 인용 관측 그대로 연다. 이후 알림은 따로 붙인다."""
        run = self.db.execute(f"SELECT * FROM {p}.answer_run WHERE run_id=?", (run_id,)).fetchone()
        slots = self.db.execute(f"SELECT * FROM {p}.answer_slot WHERE run_id=? ORDER BY slot_no",
                                (run_id,)).fetchall()
        notices = self.db.execute(
            f"SELECT * FROM {p}.notice WHERE run_id=? AND (? IS NULL OR created_at<=?) ORDER BY created_at, notice_id",
            (run_id, at, at)).fetchall()
        return {
            "produced_at": run["produced_at"], "status": run["status"], "next_action": run["next_action"],
            "slots": [{"no": s["slot_no"], "kind": s["kind"], "sentence": s["sentence"],
                       "cites": [u["obs_id"] for u in self.db.execute(
                           f"SELECT DISTINCT obs_id FROM {p}.usage WHERE run_id=? AND slot_no=? ORDER BY obs_id",
                           (run_id, s["slot_no"]))]} for s in slots],
            "notices": [{"slot": n["slot_no"], "effect": n["effect"], "text": n["text"]} for n in notices],
            "folded": [{"url": f["url"], "condition": f["condition"], "reason": f["reason"]} for f in
                       self.db.execute(f"SELECT * FROM {p}.folded WHERE run_id=? ORDER BY rowid", (run_id,))],
            "contrast": [(u["slot_no"], u["obs_id"]) for u in self.db.execute(
                f"SELECT slot_no, obs_id FROM {p}.usage WHERE run_id=? AND part='contrast' ORDER BY slot_no, obs_id",
                (run_id,))],
        }

    def counts(self) -> dict:
        q = lambda sql: self.db.execute(sql).fetchone()[0]
        return {"observations": q("SELECT count(*) FROM observation"),
                "sightings": q("SELECT count(*) FROM sighting"),
                "recheck_jobs": q("SELECT count(*) FROM recheck_job"),
                "opens": dict(self.opens)}
