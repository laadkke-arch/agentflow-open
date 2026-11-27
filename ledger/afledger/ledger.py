"""확인 장부 엔진(제품 단위 1). 설계 예제 docs/design/final/db/ledger.py에서 옮겼다.

아래는 옮겨 온 설계 예제의 머리말이다. 제품에서 달라진 점은 docs/design/final/08-implementation.md에 있다.

확인 장부 구조 v1 프로토타입 엔진.

이 코드는 저장 구조와 규칙(재사용, 묻기, 원리 관문, 우연 적중, 철회 전파, 과거 답 재생)을
고정 입력으로 확인하기 위한 것이다. 원문 판독과 꼬리표 작성은 사례 자료가 준다.
즉 이 코드가 보증하는 것은 "판독 결과가 주어졌을 때 기록과 전파가 맞게 일어나는가"이고,
판독 자체의 품질은 보증하지 않는다.

운영 시뮬레이션(../sim/ops_sim.py)에서 드러난 규칙 위반을 고친 판이다(../07-review.md 5절).
재사용·인용·승계는 대체를 보고, 작업 완료는 임차 표지를 확인하며, 대체는 감시를 새 관측으로 넘기고, 잘못된 대체는 취소 행으로 되돌린다.

features로 핵심 구성요소를 끄면 구성요소 삭제 시험을 같은 코드로 돌릴 수 있다.
  drawer : 공용 장부를 프로젝트 사이·시점 사이에 재사용한다(끄면 프로젝트마다 따로 기억).
  usage  : 답 자리 → 관측 사용 쪽지로 철회를 전파한다(끄면 프로젝트의 모든 답 자리에 알림).
  split  : 판단을 비공개 쪽지로 둔다(끄면 판단이 공용 관측에 붙어 다른 프로젝트로 흐른다).
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sqlite3
from pathlib import Path

import hmac
import secrets

from . import config, locate, normalize, privacy
from . import tokenize as ko_tok

SQL_DIR = Path(__file__).resolve().parent / "sql"

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


ISO = "%Y-%m-%dT%H:%M:%SZ"


def _parse_iso(s: str):
    """'YYYY-MM-DD', 'YYYY-MM-DDTHH:MM:SSZ', '+09:00' 같은 시간대 표기를 모두 UTC로 읽는다."""
    from datetime import datetime, timezone
    s = s.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    t = datetime.fromisoformat(s[:-1] + "+00:00" if s.endswith("Z") else s)
    return (t if t.tzinfo else t.replace(tzinfo=timezone.utc)).astimezone(timezone.utc)


def utc(s: str | None, *, date_only_ok=False) -> str | None:
    """저장 전에 시각을 UTC 'Z' 형식으로 맞춘다. 문자열 비교가 시간대 표기에 흔들리지 않게 한다.
    date_only_ok이면 날짜·연월만 있는 발행 표기('2015-01-08', '2018-10')는 그대로 둔다."""
    if s is None:
        return None
    if date_only_ok and re.fullmatch(r"\d{4}(-\d{2}){0,2}", s.strip()):
        return s.strip()
    return _parse_iso(s).strftime(ISO)


def _shift(iso: str, hours: float) -> str:
    """시각 문자열을 hours만큼 옮긴다. 날짜만 있거나 시간대 표기가 있어도 UTC로 읽는다."""
    from datetime import timedelta
    return (_parse_iso(iso) + timedelta(hours=hours)).strftime(ISO)


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
        self.rank_rules = config.RANK_RULES     # 서랍 순위 규칙 판(r0 설계 bm25 합, r1 IDF, r2 IDF+길이 정규화, 07 R-6)
        self.elig_idf_min = None                # 진단용 자격 IDF 문턱(08 I20). None이면 설계 자격 그대로
        self.elig_rules = config.ELIG_RULES     # 서랍 자격 규칙 판(e1 설계: min_slots 칸, e2: min(min_slots, 요청 칸 수) 칸, 08 I24)
        self.token_rules = config.TOKEN_RULES   # 서랍 토큰화 규칙 판(t1 영어만, t2 다국어). 측정에서 비교하려고 인스턴스마다 바꿀 수 있다
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.executescript((SQL_DIR / "commons.sql").read_text(encoding="utf-8"))
        self.projects: list[str] = []
        self.origin: dict[int, str] = {}   # drawer=False일 때만 쓰는 관측의 출처 프로젝트
        self.opens: dict[str, int] = {}    # 원문을 새로 연 횟수(요청 시계 비용). 새 관측만 센다
        self.rereads: dict[str, int] = {}  # 다시 읽었지만 내용이 같아 다시 본 기록만 남은 횟수. 이것도 실제 가져오기다
        self.alerts: list[dict] = []       # 운영자 경보(채널 ID 체계 변경 의심 등)
        self.last_finish: str | None = None
        self.clock_errors: list[dict] = [] # 기한 시계가 읽지 못한 행(형식 오류). 다른 행의 작업은 계속 만든다
        if not self.features["split"]:
            self.db.execute("""CREATE TABLE IF NOT EXISTS shared_judgment (
                obs_id INTEGER, project TEXT, code TEXT, verdict TEXT, role TEXT, reason TEXT, at TEXT)""")

    # ------------------------------------------------------------------ 대체 상태
    # 감시를 멈출 관측: 취소되지 않은 대체의 앞 관측(효과와 무관, 감시는 새 관측으로 넘어간다) + 철회된 판독.
    RETIRED_SQL = ("SELECT s.old_obs FROM supersession s WHERE s.known_from<=:at AND NOT EXISTS"
                   " (SELECT 1 FROM supersession_cancel c WHERE c.old_obs=s.old_obs AND c.new_obs=s.new_obs"
                   "  AND c.cancelled_at<=:at)"
                   " UNION SELECT c.new_obs FROM supersession_cancel c WHERE c.cancelled_at<=:at")
    # 근거로 쓰면 안 되는 관측: 취소되지 않은 invalidates·changes_value 대체의 앞 관측 + 철회된 판독.
    STALE_SQL = ("SELECT s.old_obs FROM supersession s WHERE s.known_from<=:at AND s.effect<>'confirms' AND NOT EXISTS"
                 " (SELECT 1 FROM supersession_cancel c WHERE c.old_obs=s.old_obs AND c.new_obs=s.new_obs"
                 "  AND c.cancelled_at<=:at)"
                 " UNION SELECT c.new_obs FROM supersession_cancel c WHERE c.cancelled_at<=:at")
    FAR_FUTURE = "9999-12-31T23:59:59Z"
    # 상수는 config.py 한 곳에 둔다(값을 바꾸면 규칙 판을 올린다)
    RULE_VERSION = config.RULE_VERSION
    DEADLINE_READS = config.DEADLINE_READS
    ACTIVE_RULE = config.ACTIVE_RULE
    IMMUTABLE_KINDS: tuple = config.IMMUTABLE_KINDS
    IMMUTABLE_RECHECK_H: int | None = config.IMMUTABLE_RECHECK_H
    REQUEST_FETCHES = config.REQUEST_FETCHES
    FOLLOW_FETCHES_PER_10_SOURCES = config.FOLLOW_FETCHES_PER_10_SOURCES

    def stale(self, obs_id: int, at: str | None = None) -> bool:
        """at 시각에 이 관측을 근거로 인용하면 안 되는가(무효·값 바뀜으로 대체됐거나 철회된 판독)."""
        return bool(self.db.execute(f"SELECT 1 FROM ({self.STALE_SQL}) x WHERE x.old_obs=:o",
                                    {"at": at or self.FAR_FUTURE, "o": obs_id}).fetchone())

    def retired(self, obs_id: int, at: str | None = None) -> bool:
        """at 시각에 이 관측의 감시를 멈추는가(대체돼 감시가 새 관측으로 넘어갔거나 철회된 판독)."""
        return bool(self.db.execute(f"SELECT 1 FROM ({self.RETIRED_SQL}) x WHERE x.old_obs=:o",
                                    {"at": at or self.FAR_FUTURE, "o": obs_id}).fetchone())

    # ------------------------------------------------------------------ 프로젝트
    def project(self, name: str) -> str:
        alias = "p_" + re.sub(r"[^0-9a-zA-Z_]", "_", name)
        if alias not in self.projects:
            self.db.execute(f"ATTACH DATABASE ':memory:' AS {alias}")
            ddl = (SQL_DIR / "project.sql").read_text(encoding="utf-8").replace("{p}", alias)
            self.db.executescript(ddl)
            # 공용 장부에 두는 영수증·대비 지문의 열쇠(07 D6c). 프로젝트 밖으로 나가지 않는다
            self.db.execute(f"INSERT OR IGNORE INTO {alias}.secret(one, k) VALUES (1, ?)", (secrets.token_hex(32),))
            self.projects.append(alias)
        return alias

    # ------------------------------------------------------------------ 공용 장부 쓰기
    def _locator(self, url: str, at: str, via: str) -> int:
        if via == "request":
            # 요청이 처음 연 주소의 첫 관측 시각은 날짜까지만 둔다. 누가 언제 무엇을 찾았는지 짐작하지 못하게(07 D6)
            at = utc(at)[:10] + "T00:00:00Z"
        k = normalize.keys(url)   # 정규화 키(07 R-1, n1). 원래 문자열은 그대로 둔다
        self.db.execute(
            "INSERT OR IGNORE INTO locator(url, first_seen_at, first_seen_via, url_norm, page, target, norm_rules)"
            " VALUES (?,?,?,?,?,?,?)", (url, at, via, k["url_norm"], k["page"], k["target"], k["rules"]))
        return self.db.execute("SELECT locator_id FROM locator WHERE url=?", (url,)).fetchone()[0]

    def _edition(self, locator_id: int, key: str, kind: str, published_at, at: str) -> int:
        published_at = utc(published_at, date_only_ok=True)
        self.db.execute(
            "INSERT OR IGNORE INTO edition(locator_id, edition_key, kind, published_at, first_seen_at)"
            " VALUES (?,?,?,?,?)", (locator_id, key, kind, published_at, at))
        return self.db.execute(
            "SELECT edition_id FROM edition WHERE locator_id=? AND edition_key=?",
            (locator_id, key)).fetchone()[0]

    def project_fp(self, p: str, body) -> str:
        """프로젝트 열쇠로 만든 지문(HMAC-SHA256). 공용에 두는 영수증·대비 지문이다(07 D6c)."""
        k = self.db.execute(f"SELECT k FROM {p}.secret WHERE one=1").fetchone()[0]
        text = body if isinstance(body, str) else json.dumps(body, ensure_ascii=False, sort_keys=True)
        return hmac.new(bytes.fromhex(k), text.encode("utf-8"), "sha256").hexdigest()

    def receipt(self, runtime: str, program_sha256: str, inp: dict, out, ran_at: str, *, p: str | None = None) -> int:
        """실행 영수증(07 D6c). 입력·출력 본문은 요청 프로젝트 장부에, 공용에는 런타임·프로그램 지문·입출력 지문만 둔다.
        요청 수치가 든 영수증이 공용으로 가지 않게 p 없이는 쓰지 않는다."""
        if p is None:
            raise PrivacyError("실행 영수증의 입력·출력은 요청 프로젝트 장부에 둔다(07 D6c): p를 준다")
        in_fp, out_fp = self.project_fp(p, inp), self.project_fp(p, out)
        key = sha256("|".join([runtime, program_sha256, in_fp, out_fp]))
        with self.db:
            self.db.execute(
                "INSERT OR IGNORE INTO receipt(runtime, program_sha256, input_fp, output_fp, ran_on, idem_key)"
                " VALUES (?,?,?,?,?,?)", (runtime, program_sha256, in_fp, out_fp, utc(ran_at)[:10], key))
            rid = self.db.execute("SELECT receipt_id FROM receipt WHERE idem_key=?", (key,)).fetchone()[0]
            self.db.execute(f"INSERT OR IGNORE INTO {p}.receipt_body(receipt_id, input_json, output_json, ran_at)"
                            " VALUES (?,?,?,?)", (rid, json.dumps(inp, ensure_ascii=False, sort_keys=True),
                                                  json.dumps(out, ensure_ascii=False, sort_keys=True), utc(ran_at)))
        return rid

    def receipt_body(self, p: str, receipt_id: int) -> dict | None:
        r = self.db.execute(f"SELECT * FROM {p}.receipt_body WHERE receipt_id=?", (receipt_id,)).fetchone()
        return None if r is None else {"input": json.loads(r["input_json"]), "output": json.loads(r["output_json"]),
                                       "ran_at": r["ran_at"]}

    def observe_run(self, p: str, *, url, edition_key, edition_kind, position, at, receipt_id, statement,
                    reader=None, published_at=None) -> tuple[int, bool]:
        """실행 관측(07 D6c). 공용 관측 문장은 영수증이 있다는 것만 말하고, 값 문장은 프로젝트 장부 exec_note에 둔다."""
        r = self.db.execute("SELECT runtime, program_sha256 FROM receipt WHERE receipt_id=?", (receipt_id,)).fetchone()
        public = f"실행 영수증: 프로그램 {r['program_sha256'][:12]}을 {r['runtime']}에서 실행했다(입력·출력·값은 요청 프로젝트 장부)"
        oid, created = self.observe(url=url, edition_key=edition_key, edition_kind=edition_kind, position=position, at=at,
                                    method="executed", receipt_id=receipt_id, statement=public, reader=reader,
                                    published_at=published_at, project=p)
        with self.db:
            self.db.execute(f"INSERT OR IGNORE INTO {p}.exec_note(obs_id, statement) VALUES (?,?)", (oid, statement))
        return oid, created

    def exec_note(self, p: str, obs_id: int) -> str | None:
        r = self.db.execute(f"SELECT statement FROM {p}.exec_note WHERE obs_id=?", (obs_id,)).fetchone()
        return r[0] if r else None

    def observe(self, *, url, edition_key, edition_kind, position, at, method, outcome="content",
                quote=None, quote_lang=None, statement, flip_position=None, receipt_id=None,
                published_at=None, via="request", evidence_ref=None, project=None, reader=None,
                via_alias=None, visibility="public", anchor_symbol=None, anchor_in_doc=None, map_method=None,
                map_from=None, byte_span=None) -> tuple[int, bool]:
        """관측을 남긴다. 같은 (판, 위치, 결과, 인용 지문, 방법, 영수증)이면 새 행 대신 sighting을 더한다.
        reader는 판독한 주체(모델 ID·프롬프트 판, 사람)다. via_alias는 이 관측을 연 별칭이다. 둘 다 멱등 키에는 넣지 않는다.
        visibility는 판독 어댑터가 정한다. 공개가 아닌 원문(사용자 저장소, 사내 문서)은 공용 장부에 쓰지 않는다(07 D6)."""
        if visibility != "public":
            raise PrivacyError("비공개 원문은 공용 장부에 쓰지 않는다. 사용자 자신의 원문은 프로젝트 장부의 맥락 사실로 둔다")
        with self.db:
            loc = self._locator(url, at, via)
            ed = self._edition(loc, edition_key, edition_kind, published_at, at)
            fp = sha256(fold_ws(quote)) if quote else None
            if fp:
                # 본문은 지문 키로 따로 둔다. 지운(묘비) 문장을 다시 읽어도 본문을 다시 쓰지 않는다(07 D7)
                self.db.execute("INSERT OR IGNORE INTO quote_text(quote_fp, text, stored_at) VALUES (?,?,?)",
                                (fp, quote, at))
            parts = [ed, position, outcome, fp, method, receipt_id]
            if not self.features["drawer"] and project:
                parts.append(project)   # 서랍을 끄면 프로젝트마다 따로 기억한다
            key = sha256("|".join(map(str, parts)))
            row = self.db.execute("SELECT obs_id FROM observation WHERE idem_key=?", (key,)).fetchone()
            if row:
                self.db.execute("INSERT OR IGNORE INTO sighting(obs_id, seen_at, via, reader) VALUES (?,?,?,?)",
                                (row[0], at, via if via != "operator" else "request", reader))
                if project and method in ("read_line", "executed"):
                    self.rereads[project] = self.rereads.get(project, 0) + 1
                return row[0], False
            cur = self.db.execute(
                "INSERT INTO observation(edition_id, position, observed_at, method, outcome, quote_lang,"
                " quote_fp, statement, evidence_ref, flip_position, receipt_id, reader, via_alias,"
                " anchor_symbol, anchor_in_doc, map_method, map_from, map_rules, byte_span, idem_key)"
                " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (ed, position, at, method, outcome, quote_lang, fp, statement, evidence_ref,
                 flip_position, receipt_id, reader, via_alias, anchor_symbol,
                 None if anchor_in_doc is None else int(anchor_in_doc), map_method, map_from,
                 locate.MAP_RULES if map_method else None, byte_span, key))
            obs_id = cur.lastrowid
            if outcome == "content" and method == "read_line" and fp:
                # 판독 충돌(07 R-3, 08 I21): 같은 판·같은 위치를 같은 방법으로 읽었는데 인용이 다르고 대체로 이어지지 않았다.
                # 두 관측을 모두 남기고, 앞 관측에 감사 작업(conflict:새 관측)을 만들고 운영자에게 알린다. 어느 쪽도 고르지 않는다
                for (old,) in self.db.execute(
                        "SELECT obs_id FROM observation WHERE edition_id=? AND position=? AND method='read_line'"
                        " AND outcome='content' AND quote_fp<>? AND obs_id<>?", (ed, position, fp, obs_id)).fetchall():
                    if config.CANCEL_RELINK and self.retracted(old) is not None:
                        continue   # 철회된 판독과는 견주지 않는다(08 I42 규칙 2)
                    linked = self.db.execute("SELECT 1 FROM supersession WHERE (old_obs=? AND new_obs=?) OR"
                                             " (old_obs=? AND new_obs=?)", (old, obs_id, obs_id, old)).fetchone()
                    if not linked:
                        self._enqueue(old, "audit", f"conflict:{obs_id}", at)
                        self.alerts.append({"kind": "reading_conflict", "obs": old, "other": obs_id, "at": at,
                                            "position": position})
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
            cur = self.db.execute(
                "INSERT OR IGNORE INTO tag(obs_id, slot, height, lang, text, audience, written_from)"
                " VALUES (?,?,?,?,?,?,?)", (obs_id, slot, height, lang, text, audience, written_from))
            if cur.rowcount == 1:
                words, gs = ko_tok.index_text(text)
                if words:
                    self.db.execute("INSERT INTO tag_fts_ko(rowid, words, grams) VALUES (?,?,?)", (cur.lastrowid, words, gs))
        return self.db.execute(
            "SELECT tag_id FROM tag WHERE obs_id=? AND slot=? AND height=? AND lang=? AND text=?",
            (obs_id, slot, height, lang, text)).fetchone()[0]

    def _privacy_lint(self, obs_id: int, text: str):
        """규칙은 privacy.py(p1·p2, config.PRIVACY_RULES). 모든 프로젝트의 요청 원문과 대조한다."""
        obs = self.db.execute("SELECT q.text AS quote, o.statement FROM observation o"
                              " LEFT JOIN quote_text q USING(quote_fp) WHERE o.obs_id=?", (obs_id,)).fetchone()
        source_side = (obs["quote"] or "") + " " + obs["statement"]
        # 요청 원문과 함께 비공개 칸별 필요 문장도 대조한다(설계 예제는 요청 원문만 봤다, 08 I8)
        requests = [r["text"] for p in self.projects for r in self.db.execute(
            f"SELECT text FROM {p}.request_rev UNION ALL SELECT text FROM {p}.need")]
        privacy.check(text, source_side, requests)

    def contrast(self, left_obs, right_obs, condition, left_value, right_value, receipt_id=None, *, p: str | None = None):
        """대비(07 D6c). 조건과 값은 요청 수치를 담으므로 프로젝트 장부에 두고, 공용에는 두 관측과 본문 지문만 둔다."""
        if p is None:
            raise PrivacyError("대비 본문은 요청 프로젝트 장부에 둔다(07 D6c): p를 준다")
        fp = self.project_fp(p, [condition, left_value, right_value])
        with self.db:
            self.db.execute("INSERT OR IGNORE INTO contrast(left_obs, right_obs, body_fp, receipt_id) VALUES (?,?,?,?)",
                            (left_obs, right_obs, fp, receipt_id))
            self.db.execute(f"INSERT OR IGNORE INTO {p}.contrast(left_obs, right_obs, condition, left_value, right_value,"
                            " receipt_id, body_fp) VALUES (?,?,?,?,?,?,?)",
                            (left_obs, right_obs, condition, left_value, right_value, receipt_id, fp))

    def supersede(self, old_obs, new_obs, effect, known_from, effective_from=None) -> None:
        """대체를 쓰고, 앞 관측의 감시(채널·키·층)를 새 관측으로 넘긴다. 기한은 원문 내용이라 넘기지 않는다.
        넘기지 않으면 첫 대체 뒤 공급자 층 감시가 사라진다(운영 시뮬레이션 M1)."""
        with self.db:
            self._supersede(old_obs, new_obs, effect, known_from, effective_from)

    def _supersede(self, old_obs, new_obs, effect, known_from, effective_from=None) -> None:
        self.db.execute(
            "INSERT OR IGNORE INTO supersession(old_obs, new_obs, effect, effective_from, known_from)"
            " VALUES (?,?,?,?,?)", (old_obs, new_obs, effect, utc(effective_from, date_only_ok=True), utc(known_from)))
        self.db.execute(
            "INSERT OR IGNORE INTO watch(obs_id, channel_id, match_key, layer, deadline)"
            " SELECT ?, channel_id, match_key, layer, NULL FROM watch WHERE obs_id=?", (new_obs, old_obs))

    def cancel_supersession(self, old_obs: int, new_obs: int, at: str, reason: str) -> None:
        """잘못 쓴 대체를 취소한다. 앞 관측은 다시 유효해지고 감시가 돌아오며, new_obs는 철회된 판독이 된다.
        바른 판독은 앞 관측과 내용이 같아 새 관측이 생기지 않으므로 confirms 대체로는 되돌릴 수 없다(순환)."""
        with self.db:
            self.db.execute("INSERT INTO supersession_cancel(old_obs, new_obs, cancelled_at, reason) VALUES (?,?,?,?)",
                            (old_obs, new_obs, utc(at), reason))
            # 잘못 대체된 동안 철회된 판독 쪽으로 들어온 재확인 원인은 앞 관측이 이어받는다(그 사이 채널 항목을 놓치지 않게).
            # 옮긴 작업은 철회된 쪽에서 닫는다. 남겨 두면 작업자가 철회된 판독에서 출발해 다시 대체를 쓴다(08 I37 규칙 1)
            for j in self.db.execute("SELECT job_id, cause, cause_ref, merged_causes FROM recheck_job WHERE obs_id=? AND"
                                     " state='queued' AND cause<>'audit'", (new_obs,)).fetchall():
                self._move_causes(j, old_obs, utc(at))
                self.db.execute("UPDATE recheck_job SET state='done', result_obs=NULL WHERE job_id=?", (j["job_id"],))
            # 하류 다시 잇기(I37 규칙 4, I43): new의 하류 관측을 결과로 낸 작업의 채널 원인을 old에 다시 넣는다.
            # 작업자가 X의 판을 old 기준으로 읽고 이미 있는 관측 X로 잇는다(규칙 3). 효과는 old와 견준 것이 된다
            # 하류 닫힘(08 I43): new에서 취소되지 않은 대체를 따라 닿는 관측 전부. 작업 하나가 X→Y를 쓰면 result_obs는 Y다
            relink = [x for (x,) in self.db.execute(
                "WITH RECURSIVE dn(o) AS (SELECT s.new_obs FROM supersession s WHERE s.old_obs=? AND NOT EXISTS"
                " (SELECT 1 FROM supersession_cancel c WHERE c.old_obs=s.old_obs AND c.new_obs=s.new_obs)"
                " UNION SELECT s.new_obs FROM supersession s JOIN dn ON s.old_obs=dn.o WHERE NOT EXISTS"
                " (SELECT 1 FROM supersession_cancel c WHERE c.old_obs=s.old_obs AND c.new_obs=s.new_obs))"
                " SELECT o FROM dn", (new_obs,)).fetchall() if x != new_obs]
            if config.CANCEL_RELINK:
                relink.append(new_obs)   # 취소된 판 자체의 원인도 되살린다(08 I42 규칙 1): 바른 판독이 그 판을 다시 읽게
            for x in relink:
                for j in self.db.execute("SELECT job_id, cause, cause_ref, merged_causes FROM recheck_job"
                                         " WHERE result_obs=? AND state='done'", (x,)).fetchall():
                    self._move_causes(j, old_obs, utc(at), only=("channel",))

    def _move_causes(self, j, target: int, at: str, only: tuple = ("channel", "deadline", "request")) -> None:
        for c, ref in [(j["cause"], j["cause_ref"])] + [tuple(m.split(":", 1)) for m in j["merged_causes"].split(",") if m]:
            if c in only:
                self._enqueue(target, c, ref, at)

    def retracted(self, obs_id: int, at: str | None = None) -> int | None:
        """철회된 판독이면 되살아난 앞 관측 번호를, 아니면 None을 돌려준다(취소된 대체의 새 관측)."""
        r = self.db.execute("SELECT old_obs FROM supersession_cancel WHERE new_obs=? AND (? IS NULL OR cancelled_at<=?)"
                            " ORDER BY cancelled_at DESC LIMIT 1", (obs_id, at, at)).fetchone()
        return r[0] if r else None

    def fail_streak(self, base: int, at: str) -> tuple[int, str | None]:
        """감시 계보(기준 관측과 앞선 관측들)에 걸린 재확인 작업의 가져오기를 최근 것부터 보아, 맨 뒤에서 이어진 같은 실패의
        수와 그 outcome을 돌려준다. ok·not_modified가 나오거나 outcome이 바뀌면 멈춘다(08 I38 규칙 4)."""
        lineage = sorted({base} | self.earlier_obs(base, at))
        marks = ",".join("?" * len(lineage))
        n, kind = 0, None
        for (o, env) in self.db.execute(
                f"SELECT f.outcome, f.env_suspect FROM fetch_log f JOIN recheck_job j ON j.job_id=f.job_id WHERE j.obs_id IN ({marks})"
                " AND f.at<=? ORDER BY f.fetch_id DESC", (*lineage, at)):
            if env and o not in ("ok", "not_modified"):
                continue   # 환경 고장 의심 실패는 세지도 끊지도 않는다(08 I46 규칙 3)
            if o in ("ok", "not_modified") or (kind is not None and o != kind):
                break
            kind, n = o, n + 1
        return n, kind

    def note_source_failure(self, base: int, fail_obs: int, at: str) -> bool:
        """연속이 문턱에 처음 닿은 순간이면 source_failure 행을 남기고 True를 돌려준다."""
        n, kind = self.fail_streak(base, at)
        if n != config.SOURCE_FAIL_STREAK:
            return False
        with self.db:
            self.db.execute("INSERT OR IGNORE INTO source_failure(base_obs, fail_obs, outcome, at, streak)"
                            " VALUES (?,?,?,?,?)", (base, fail_obs, kind, utc(at), n))
        self.alerts.append({"kind": "source_failure", "obs": base, "outcome": kind, "streak": n, "at": at})
        return True

    def note_source_recovery(self, base: int, at: str) -> int:
        """계보(base와 앞선 관측들)에 회복 기록이 없는 source_failure가 있으면 회복을 남긴다(08 I44). 남긴 수를 돌려준다."""
        lineage = sorted({base} | self.earlier_obs(base, at))
        marks = ",".join("?" * len(lineage))
        rows = self.db.execute(
            f"SELECT f.failure_id FROM source_failure f WHERE f.base_obs IN ({marks}) AND f.at<? AND NOT EXISTS"
            " (SELECT 1 FROM source_recovery r WHERE r.failure_id=f.failure_id)", (*lineage, utc(at))).fetchall()
        with self.db:
            for (fid,) in rows:
                self.db.execute("INSERT OR IGNORE INTO source_recovery(failure_id, at, obs_id) VALUES (?,?,?)",
                                (fid, utc(at), base))
        return len(rows)

    def earlier_obs(self, obs_id: int, at: str) -> set[int]:
        """취소되지 않은 대체를 거꾸로 따라 닿는 앞선 관측들."""
        rows = self.db.execute(
            "WITH RECURSIVE up(o) AS (SELECT ? UNION SELECT s.old_obs FROM supersession s JOIN up ON s.new_obs=up.o"
            " WHERE s.known_from<=? AND NOT EXISTS (SELECT 1 FROM supersession_cancel c WHERE c.old_obs=s.old_obs"
            " AND c.new_obs=s.new_obs AND c.cancelled_at<=?)) SELECT o FROM up", (obs_id, at, at)).fetchall()
        return {r[0] for r in rows} - {obs_id}

    def alias(self, from_url: str, to_url: str, kind: str, at: str, evidence_obs=None) -> int:
        with self.db:
            a = self._locator(from_url, at, "operator")
            b = self._locator(to_url, at, "operator")
            return self.db.execute(
                "INSERT INTO locator_alias(from_id, to_id, kind, asserted_at, evidence_obs) VALUES (?,?,?,?,?)",
                (a, b, kind, at, evidence_obs)).lastrowid

    def cancel_alias(self, alias_id: int, at: str, reason: str) -> None:
        """별칭을 취소한다. 그 별칭을 따라 연 관측마다 원 주소에서 다시 확인하는 감사 작업을 만들고,
        그 관측을 인용한 답 자리에는 전파가 알린다(07 D5)."""
        with self.db:
            self.db.execute("INSERT INTO locator_alias_cancel(alias_id, cancelled_at, reason) VALUES (?,?,?)",
                            (alias_id, at, reason))
            for (oid,) in self.db.execute("SELECT obs_id FROM observation WHERE via_alias=? ORDER BY obs_id",
                                          (alias_id,)).fetchall():
                self._enqueue(oid, "audit", f"alias:{alias_id}", utc(at))

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
    def channel(self, supplier: str, url: str, kind: str, period_h: int = 72, *, windowed: bool = False) -> int:
        with self.db:
            self.db.execute("INSERT OR IGNORE INTO channel(supplier, url, kind, period_h, windowed) VALUES (?,?,?,?,?)",
                            (supplier, url, kind, period_h, int(windowed)))
        return self.db.execute("SELECT channel_id FROM channel WHERE url=?", (url,)).fetchone()[0]

    def watch(self, obs_id: int, channel_url: str, match_key: str = "", *, layer="same_address",
              deadline: str | None = None) -> None:
        ch = self.db.execute("SELECT channel_id FROM channel WHERE url=?", (channel_url,)).fetchone()[0]
        deadline = utc(deadline)   # 날짜만 적은 기한은 그날 0시 UTC로. 형식이 틀리면 여기서 거절한다
        with self.db:
            # 대체가 넘겨준 감시 행이 이미 있으면 기한만 채운다
            self.db.execute("INSERT INTO watch(obs_id, channel_id, match_key, layer, deadline) VALUES (?,?,?,?,?)"
                            " ON CONFLICT(obs_id, channel_id, match_key) DO UPDATE SET"
                            " deadline=COALESCE(excluded.deadline, watch.deadline)",
                            (obs_id, ch, match_key, layer, deadline))

    def _enqueue(self, obs_id: int, cause: str, cause_ref: str, at: str) -> bool:
        """같은 관측에 대기 중인 작업이 있으면 새 원인을 거기에 합친다(기한 작업과 채널 항목이 같은 날 오면 하나).
        임차 중인 작업에는 합치지 않는다. 작업자가 이미 받아 온 판으로 끝내면 새 원인이 읽히지 않고 끝나기 때문이다(M5b)."""
        open_job = self.db.execute(
            "SELECT job_id, merged_causes FROM recheck_job WHERE obs_id=? AND state='queued'",
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
        """DEADLINE_READS(기한 24시간 전, 기한, 24시간 뒤)마다 직접 읽는 작업을 만든다. 기한 경과만으로 관측을 무효로 하지 않는다."""
        n = 0
        with self.db:
            rows = self.db.execute(
                f"SELECT obs_id, deadline FROM watch WHERE deadline IS NOT NULL AND obs_id NOT IN ({self.RETIRED_SQL})",
                {"at": at}).fetchall()
            for w in rows:
                try:
                    plan = tuple((ref, _shift(w["deadline"], h)) for ref, h in self.DEADLINE_READS)
                except ValueError as e:
                    # 한 행의 형식 오류가 다른 관측의 기한 작업까지 막지 않게 한다(M9)
                    self.clock_errors.append({"obs_id": w["obs_id"], "deadline": w["deadline"], "error": str(e)})
                    continue
                for ref, when in plan:
                    if when <= at and self._enqueue(w["obs_id"], "deadline", f"{w['deadline']}#{ref}", at):
                        n += 1
        return n

    def reuse_gate(self, obs_id: int, at: str) -> dict:
        """요청 시계에서 재사용 관측을 다시 열지 않아도 되는가. 조건이 모두 참이면 다시 열지 않는다.
        보증(08 I40): 장부가 받은 변화 뒤에는 재사용하지 않는다. 받기 전의 지연은 감시 채널 주기(확인 커서 2배 한도)로 묶인다.
        (4') 바뀌는 판은 같은 주소 층 감시가 있어야 한다(감시 범위, I40).
        (1) 감시 채널 커서가 주기의 2배 안에서 성공 (2) 열린 재확인 작업 없음 (3) 공지 기한이 24시간 안에 오지 않음
        (4) 감시가 주장과 같은 층(감시를 달 때 확인 단계가 보증) (5) 마지막 직접 확인이 168시간 안."""
        why = []
        ws = self.db.execute(
            "SELECT w.*, c.last_polled_at, c.confirmed_at, c.period_h, c.url AS ch_url FROM watch w"
            " JOIN channel c USING(channel_id) WHERE w.obs_id=?", (obs_id,)).fetchall()
        last = self.db.execute(
            "SELECT max(t) FROM (SELECT observed_at AS t FROM observation WHERE obs_id=?"
            " UNION ALL SELECT seen_at FROM sighting WHERE obs_id=?)", (obs_id, obs_id)).fetchone()[0]
        if not ws:
            why.append("감시 없음")
        last_read = max(h for _r, h in self.DEADLINE_READS)
        for w in ws:
            # 확인 커서(마지막 ok 폴링)로 본다. 시도 시각은 원문에 닿지 못한 폴링도 새것으로 만든다(08 I35)
            if not w["confirmed_at"] or w["confirmed_at"] < _shift(at, -2 * w["period_h"]):
                why.append(f"채널 커서가 늙음({w['ch_url']})")
            # 기한 읽기 창(T-24h ~ 마지막 기한 읽기) 안이거나, 기한이 지났는데 그 뒤 직접 확인이 없을 때만 다시 연다.
            # v1은 기한이 지나면 대체될 때까지 영원히 다시 열었다
            if w["deadline"] and (_shift(w["deadline"], -24) <= at <= _shift(w["deadline"], max(0, last_read))
                                  or (w["deadline"] <= at and last < w["deadline"])):
                why.append(f"공지 기한 {w['deadline']} 임박 또는 경과")
        if self.db.execute("SELECT 1 FROM recheck_job WHERE obs_id=? AND state IN ('queued','leased')",
                           (obs_id,)).fetchone():
            why.append("처리 안 된 재확인 작업")
        if self.stale(obs_id, at):
            why.append(f"대체되었거나 철회된 관측(현재 관측 {self.current(obs_id, at)})")
        kind = self.db.execute("SELECT e.kind FROM observation o JOIN edition e USING(edition_id) WHERE o.obs_id=?",
                               (obs_id,)).fetchone()[0]
        # (4') 감시 범위(08 I40): 바뀌는 판은 그 주소의 변화를 받는 같은 주소 층 감시가 있어야 한다. 공급자 층은 지위 공지만 받는다.
        # 고정판은 내용이 바뀌지 않으므로 어느 층이든 감시 하나로 충분하다
        if ws and kind not in self.IMMUTABLE_KINDS and not any(w["layer"] == "same_address" for w in ws):
            why.append("감시 범위 부족(같은 주소 층 감시 없음)")
        # 주장이 판에 고정된 종류(태그·커밋·DOI)는 원문이 바뀌지 않는다. 바뀌는 것은 판의 지위(철회·이동)이고 채널이 잡는다
        limit = self.IMMUTABLE_RECHECK_H if kind in self.IMMUTABLE_KINDS else config.RECHECK_H
        if limit is not None and last < _shift(at, -limit):
            why.append(f"마지막 직접 확인이 {limit}시간보다 오래됨")
        polled = [w["confirmed_at"] for w in ws if w["confirmed_at"]]
        return {"decision": "reopen" if why else "reuse", "why": why,
                "basis": None if why else f"채널 확인 시각 {max(polled)}"}

    def poll(self, channel_url: str, listing: list[dict], at: str, *, outcome: str = "ok",
             full_listing: bool | None = None) -> list[dict]:
        """채널 목록 전체를 받아 외부 ID 집합의 차분만 새 항목으로 넣고, 닿는 관측의 재확인 작업을 만든다.
        확인 커서(08 I35): outcome="ok"이고 결번이 없을 때만 confirmed_at·cursor를 옮긴다. "error"(원문에 닿지 못함)는
        목록을 처리하지 않고 시도 시각만 남긴다. 창 채널에서 직전 최신 ID가 목록에 없으면 결번(gap)으로 보고 새 ID는 넣되
        확인 커서를 멈추고 전체 목록 1회를 요청한다(needs_full_listing). full_listing=True인 목록은 결번 검사를 하지 않는다."""
        chrow = self.db.execute("SELECT * FROM channel WHERE url=?", (channel_url,)).fetchone()
        ch = chrow["channel_id"]
        self.last_poll_outcome = outcome
        if outcome == "error":
            with self.db:
                self.db.execute("UPDATE channel SET last_polled_at=? WHERE channel_id=?", (at, ch))
            return []
        known_rows = self.db.execute(
            "SELECT external_id FROM channel_item WHERE channel_id=? ORDER BY item_id", (ch,)).fetchall()
        known = {r[0] for r in known_rows}
        full = (not chrow["windowed"]) if full_listing is None else full_listing
        gap = False
        if chrow["windowed"] and not full and known:
            newest_known = known_rows[-1][0]
            gap = newest_known not in {it["id"] for it in listing}
        if gap:
            self.last_poll_outcome = "gap"
            self.alerts.append({"kind": "channel_gap_suspected", "channel": channel_url, "at": at,
                                "missing": newest_known})
        new, ids = [], set()
        for it in listing:                 # 목록 안의 중복 ID는 첫 항목만 쓴다(중복이면 거래 전체가 실패했다, M12)
            if it["id"] not in known and it["id"] not in ids:
                new.append(it)
                ids.add(it["id"])
        reset = bool(known) and len(new) >= self.RESET_MIN_NEW and len(new) >= self.RESET_SHARE * len(listing)
        if reset:
            # ID 체계가 바뀐 것으로 보고 기준선만 다시 잡는다. 재확인 작업은 만들지 않고 운영자에게 알린다 [가정: 문턱]
            self.alerts.append({"kind": "channel_id_reset_suspected", "channel": channel_url, "at": at,
                                "new_ids": len(new), "listing": len(listing)})
        with self.db:
            for it in new:
                self.db.execute(
                    "INSERT INTO channel_item(channel_id, external_id, first_seen_at, title, summary, locator_url,"
                    " edition_key) VALUES (?,?,?,?,?,?,?)",
                    (ch, it["id"], at, it["title"], it.get("summary"), it.get("url"), it.get("edition")))
                if reset:
                    continue
                active = self.db.execute(
                    f"SELECT obs_id, match_key FROM watch WHERE channel_id=:ch AND obs_id NOT IN ({self.RETIRED_SQL})",
                    {"ch": ch, "at": at}).fetchall()
                for w in active:
                    hay = (it["title"] + " " + (it.get("summary") or "")).lower()
                    if w["match_key"] and w["match_key"].lower() not in hay:
                        continue
                    self._enqueue(w["obs_id"], "channel", f"{channel_url}#{it['id']}", at)
            self.db.execute("UPDATE channel SET last_polled_at=?, last_item_count=? WHERE channel_id=?",
                            (at, len(listing), ch))
            if gap:
                self.db.execute("UPDATE channel SET needs_full_listing=1 WHERE channel_id=?", (ch,))
            else:
                ids_all = sorted(known | {it["id"] for it in new})
                cur = hashlib.sha256("\n".join(ids_all).encode("utf-8")).hexdigest()[:16]
                self.db.execute("UPDATE channel SET confirmed_at=?, cursor=?, needs_full_listing=0 WHERE channel_id=?",
                                (at, cur, ch))
        return new

    RESET_MIN_NEW = config.RESET_MIN_NEW   # [가정] 기준선이 있는 채널에서 한 번에 새 ID가 이만큼 이상이고
    RESET_SHARE = config.RESET_SHARE       # [가정] 목록의 이 비율 이상이면 ID 체계 변경으로 의심한다

    def jobs(self, state="queued") -> list[sqlite3.Row]:
        return self.db.execute("SELECT * FROM recheck_job WHERE state=? ORDER BY job_id", (state,)).fetchall()

    def lease(self, job_id: int, until: str) -> int:
        """작업자 둘이 같은 작업을 잡지 않게 한다. 잡으면 임차 표지(이번 시도 번호, 1 이상)를, 이미 잡혔으면 0을 돌려준다."""
        with self.db:
            cur = self.db.execute(
                "UPDATE recheck_job SET state='leased', lease_until=?, attempts=attempts+1"
                " WHERE job_id=? AND state='queued'", (until, job_id))
        if cur.rowcount != 1:
            return 0
        return self.db.execute("SELECT attempts FROM recheck_job WHERE job_id=?", (job_id,)).fetchone()[0]

    def job_attempts(self, job_id: int) -> dict:
        """작업의 시도를 가른다(08 I46): 실패한 시도 가운데 모든 실패가 환경 고장 의심이면 env, 아니면 real."""
        rows = self.db.execute("SELECT at, min(env_suspect) AS all_env FROM fetch_log WHERE job_id=? AND outcome IN"
                               " ('unreachable','truncated','not_found','unsupported') GROUP BY at", (job_id,)).fetchall()
        return {"env": sum(1 for r in rows if r["all_env"]), "real": sum(1 for r in rows if not r["all_env"])}

    def retry(self, job_id: int, token: int, not_before: str) -> bool:
        """임차한 작업을 대기로 되돌리고 not_before 전에는 잡히지 않게 한다(08 I41). 임차가 이미 풀렸으면 False."""
        with self.db:
            cur = self.db.execute("UPDATE recheck_job SET state='queued', lease_until=NULL, not_before=?"
                                  " WHERE job_id=? AND state='leased' AND attempts=?", (utc(not_before), job_id, token))
        return cur.rowcount == 1

    def finish(self, job_id: int, result_obs: int | None, ok=True, token: int | None = None,
               supersede: tuple | None = None, chain_before: list | None = None, base: tuple | None = None) -> bool:
        """작업을 끝낸다. token을 주면 지금도 그 임차가 유효할 때만 받는다(임차가 풀려 다른 작업자가 잡았으면 거절).
        supersede=(앞 관측, 효과, 알게 된 시각, 효력 시각)을 주면 대체를 같은 거래 안에서 쓴다. 늦게 돌아온 작업자가
        대체를 먼저 써 버려 대체가 두 갈래로 생기는 일을 막는다(M5a). token 없이 부르면 예전처럼 무조건 받는다.
        chain_before=[(앞, 뒤, 효과, 알게 된 시각, 효력 시각), …]은 마지막 대체 앞의 고리로, 같은 거래에서 먼저 쓴다.
        base=(작업 관측, 기준 관측, 시각)을 주면 기준 관측이 아직 작업 관측의 현재 관측이고 철회되지 않았을 때만 대체를 쓴다.
        아니면 대체 없이 작업을 닫고 원인을 되살아난 관측으로 옮긴 뒤 False를 돌려준다(08 I37 규칙 1, last_finish="base_moved")."""
        self.last_finish = None
        with self.db:
            if base is not None:
                job_obs, b0, at_ = base
                back = self.retracted(b0)
                if back is not None or self.current(job_obs, at_) != b0:
                    if token is not None:
                        cur = self.db.execute("UPDATE recheck_job SET state='done', result_obs=NULL WHERE job_id=?"
                                              " AND state='leased' AND attempts=?", (job_id, token))
                        if cur.rowcount != 1:
                            return False
                    j = self.db.execute("SELECT job_id, cause, cause_ref, merged_causes FROM recheck_job WHERE job_id=?",
                                        (job_id,)).fetchone()
                    target = self.current(back if back is not None else job_obs, at_)
                    self._move_causes(j, target, utc(at_))
                    self.last_finish = "base_moved"
                    return False
            if token is not None:
                cur = self.db.execute(
                    "UPDATE recheck_job SET state=?, result_obs=? WHERE job_id=? AND state='leased' AND attempts=?",
                    ("done" if ok else "failed", result_obs, job_id, token))
                if cur.rowcount != 1:
                    return False
            else:
                self.db.execute("UPDATE recheck_job SET state=?, result_obs=? WHERE job_id=?",
                                ("done" if ok else "failed", result_obs, job_id))
            for a, b, effect, known_from, effective_from in chain_before or []:
                self._supersede(a, b, effect, known_from, effective_from)
            if supersede and result_obs is not None:
                old, effect, known_from, effective_from = supersede
                self._supersede(old, result_obs, effect, known_from, effective_from)
        return True

    def job_editions(self, job_id: int) -> list[dict]:
        """이 작업에 합쳐진 채널 항목이 가리키는 판들(07 D3). 판 키가 있는 항목마다 작업자가 그 판을 읽고,
        읽은 판을 발행 시각 순으로 대체 사슬에 잇는다. 한 폴링 주기 안에 개정이 둘 와도 가운데 판을 잃지 않는다.
        판 키가 있는 항목이 없으면 빈 목록이다(읽는 시각의 최신 판을 읽는다)."""
        j = self.db.execute("SELECT cause, cause_ref, merged_causes FROM recheck_job WHERE job_id=?",
                            (job_id,)).fetchone()
        refs = [(j["cause"], j["cause_ref"])] + [tuple(m.split(":", 1)) for m in j["merged_causes"].split(",") if m]
        out, seen = [], set()
        for cause, ref in refs:
            if cause != "channel" or "#" not in ref:
                continue
            ch_url, ext = ref.rsplit("#", 1)
            row = self.db.execute(
                "SELECT i.edition_key, i.locator_url, i.first_seen_at FROM channel_item i JOIN channel c USING(channel_id)"
                " WHERE c.url=? AND i.external_id=?", (ch_url, ext)).fetchone()
            if row and row["edition_key"] and row["edition_key"] not in seen:
                seen.add(row["edition_key"])
                out.append({"edition_key": row["edition_key"], "url": row["locator_url"], "item": ext,
                            "first_seen_at": row["first_seen_at"]})
        return out

    def redact(self, *, at: str, reason: str, quote_fp: str | None = None, obs_id: int | None = None) -> int:
        """권리자 요청으로 인용 본문을 지운다. 관측·지문·진술은 남고, 본문 자리에 지운 시각과 이유(묘비)가 남는다(07 D7).
        같은 문장을 인용한 다른 판의 관측도 함께 지워진다(같은 지문)."""
        if obs_id is not None:
            quote_fp = self.obs(obs_id)["quote_fp"]
        if not quote_fp:
            return 0
        with self.db:
            cur = self.db.execute("UPDATE quote_text SET text=NULL, erased_at=?, erase_reason=?"
                                  " WHERE quote_fp=? AND text IS NOT NULL", (utc(at), reason, quote_fp))
        return cur.rowcount

    # ------------------------------------------------------------------ 예산(07 D1)
    def fetched(self, url: str, edition_key: str | None, at: str, outcome: str = "ok", nbytes: int | None = None, *,
                p: str | None = None, req: int | None = None, clock: str = "request", job_id: int | None = None,
                env_suspect: bool = False) -> None:
        """원문을 한 번 가져왔다고 적는다. 예산은 이 기록으로 센다. 실패·재시도도 한 번이다. 실행은 영수증으로 따로 센다.
        요청 시계의 기록은 프로젝트 장부에, 후속·배경 시계의 기록은 공용 장부에 둔다. not_modified(조건부 요청 304)는 따로 센다."""
        with self.db:
            if clock == "request":
                if p is None or req is None:
                    raise ValueError("요청 시계의 가져오기는 프로젝트와 요청판을 적는다")
                self.db.execute(f"INSERT INTO {p}.fetch_log(req_id, url, edition_key, at, outcome, bytes)"
                                " VALUES (?,?,?,?,?,?)", (req, url, edition_key, utc(at), outcome, nbytes))
            else:
                self.db.execute("INSERT INTO fetch_log(clock, url, edition_key, at, outcome, bytes, job_id, env_suspect)"
                                " VALUES (?,?,?,?,?,?,?,?)", (clock, url, edition_key, utc(at), outcome, nbytes, job_id,
                                                              int(bool(env_suspect))))

    def called(self, p: str, req: int, kind: str, query: str, at: str, outcome: str, total: int | None = None) -> None:
        """검색 호출을 적는다. 가져오기가 아니라 외부 시도로 센다(budget.py)."""
        with self.db:
            self.db.execute(f"INSERT INTO {p}.call_log(req_id, kind, query, at, outcome, total) VALUES (?,?,?,?,?,?)",
                            (req, kind, query, utc(at), outcome, total))

    def executed(self, p: str, req: int, *, runtime_wanted: str, runtime_ran: str | None, program_sha256: str, at: str,
                 ok: bool, receipt_id: int | None = None, note: str | None = None) -> None:
        """실행을 적는다. 가져오기와 따로 센다(07 D1). 원한 판과 실제로 돈 판을 둘 다 남긴다."""
        with self.db:
            self.db.execute(f"INSERT INTO {p}.exec_log(req_id, runtime_wanted, runtime_ran, program_sha256, at, ok,"
                            " receipt_id, note) VALUES (?,?,?,?,?,?,?,?)",
                            (req, runtime_wanted, runtime_ran, program_sha256, utc(at), int(ok), receipt_id, note))

    def request_budget_left(self, p: str, req: int) -> int:
        """이 요청판이 더 가져올 수 있는 원문 수(07 D11). 0이면 budget_exhausted로 답한다."""
        return self.REQUEST_FETCHES - self.fetch_count(p=p, req=req)

    def follow_budget_left(self, at: str) -> int:
        """후속 시계가 지금부터 더 가져올 수 있는 원문 수. 168시간 창, 감시 출처(채널) 10개당 FOLLOW_FETCHES_PER_10_SOURCES."""
        n = self.db.execute("SELECT count(*) FROM channel").fetchone()[0]
        cap = self.FOLLOW_FETCHES_PER_10_SOURCES * max(1, -(-n // 10))
        used = self.fetch_count(clock="follow", since=_shift(at, -168))
        # 환경 고장 의심 시도는 출처에 닿지 못했으므로 후속 몫에서 뺀다(08 I49). ENV_RETRY_MAX가 따로 묶는다
        used -= self.db.execute("SELECT count(*) FROM fetch_log WHERE clock='follow' AND env_suspect=1 AND at>=?"
                                " AND outcome<>'not_modified'", (_shift(at, -168),)).fetchone()[0]
        return cap - used

    def fetch_count(self, *, p: str | None = None, req: int | None = None, clock: str = "request",
                    since: str | None = None, include_not_modified: bool = False) -> int:
        nm = "" if include_not_modified else " AND outcome<>'not_modified'"
        if clock == "request":
            q = f"SELECT count(*) FROM {p}.fetch_log WHERE (? IS NULL OR req_id=?) AND (? IS NULL OR at>=?){nm}"
            return self.db.execute(q, (req, req, since, since)).fetchone()[0]
        q = f"SELECT count(*) FROM fetch_log WHERE clock=? AND (? IS NULL OR at>=?){nm}"
        return self.db.execute(q, (clock, since, since)).fetchone()[0]

    def recall_reader(self, reader: str, at: str) -> int:
        """판독기 하나의 관측을 모두 다시 확인한다(그 판독기의 오류가 드러났을 때). 만든 작업 수를 돌려준다."""
        n = 0
        with self.db:
            for (oid,) in self.db.execute("SELECT obs_id FROM observation WHERE reader=? ORDER BY obs_id",
                                          (reader,)).fetchall():
                if self._enqueue(oid, "audit", f"reader:{reader}", at):
                    n += 1
        return n

    def release_expired(self, now: str) -> int:
        with self.db:
            cur = self.db.execute(
                "UPDATE recheck_job SET state='queued' WHERE state='leased' AND lease_until < ?", (now,))
        return cur.rowcount

    # ------------------------------------------------------------------ 공용 장부 읽기
    def obs(self, obs_id: int) -> sqlite3.Row:
        return self.db.execute(
            "SELECT o.*, q.text AS quote, e.edition_key, e.kind AS edition_kind, e.published_at, l.url,"
            " l.url_norm, l.page, l.target, l.norm_rules"
            " FROM observation o JOIN edition e USING(edition_id) JOIN locator l USING(locator_id)"
            " LEFT JOIN quote_text q ON q.quote_fp = o.quote_fp WHERE o.obs_id=?",
            (obs_id,)).fetchone()

    def link(self, obs_id: int) -> str:
        """답에 쓰는 링크. GitHub 소스는 판을 넣은 고정판 줄 링크로 만든다(D10)."""
        o = self.obs(obs_id)
        if o["method"] == "executed":
            r = self.db.execute("SELECT runtime, program_sha256 FROM receipt WHERE receipt_id=?",
                                (o["receipt_id"],)).fetchone()
            return f"실행 영수증 {r['program_sha256'][:12]} ({r['runtime']}, {o['position'].split()[-1]})"
        url = o["url"]
        if "/blob/main/" in url:
            url = url.replace("/blob/main/", f"/blob/{o['edition_key']}/")
        r = locate.parse_position(o["position"])
        if r and "github.com" in url and "#" not in url:
            url += f"#L{r[0]}" + (f"-L{r[1]}" if r[1] != r[0] else "")
        return url

    def reusable(self, url: str, edition_key: str, position: str, project: str | None = None, at: str | None = None):
        """같은 판·같은 위치의 관측이 있으면 돌려준다. 판이 다르면 None(그 판을 다시 열어야 한다).
        일시 실패(unreachable·truncated)는 재사용하지 않는다. not_found는 '그 판에 없다'는 사실이라 재사용한다.
        at 시각까지 무효·값 바뀜으로 대체됐거나 철회된 판독이면 None이다(현재 관측으로 다시 확인해야 한다, M7e)."""
        # 재사용 키는 (page, 판, 위치)다(07 R-1 임시안 n1). 같은 문서의 다른 주소 꼴(blob/main, blob/태그, raw)이 만난다.
        # target으로는 묶지 않는다(전역 병합 금지)
        page = normalize.keys(url)["page"]
        row = self.db.execute(
            "SELECT o.obs_id FROM observation o JOIN edition e USING(edition_id) JOIN locator l USING(locator_id)"
            " WHERE l.page=? AND e.edition_key=? AND o.position=? AND o.outcome NOT IN ('unreachable','truncated')"
            " ORDER BY o.observed_at DESC, o.obs_id DESC LIMIT 1",
            (page, edition_key, position)).fetchone()
        if not row or self.stale(row[0], at):
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
                "SELECT s.new_obs FROM supersession s WHERE s.old_obs=? AND s.known_from<=? AND NOT EXISTS"
                " (SELECT 1 FROM supersession_cancel c WHERE c.old_obs=s.old_obs AND c.new_obs=s.new_obs"
                "  AND c.cancelled_at<=?) ORDER BY s.known_from DESC LIMIT 1", (cur, at, at)).fetchone()
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
        """해석 결정을 남긴다. 덮어쓰지 않는다(예전에는 INSERT OR REPLACE라 한 번 묻기의 질문·답 기록이 지워질 수 있었다).
        같은 결정의 재전송은 무시하고, 한 번 묻기에 나중에 온 답만 빈 answer 칸에 채운다. 그 밖의 변경은 새 요청판으로."""
        with self.db:
            row = self.db.execute(f"SELECT chosen, other, decision, question, answer FROM {p}.interpretation"
                                  " WHERE req_id=? AND code=?", (req, code)).fetchone()
            if row is None:
                self.db.execute(
                    f"INSERT INTO {p}.interpretation(req_id, code, chosen, other, decision, question, answer, decided_at)"
                    " VALUES (?,?,?,?,?,?,?,?)", (req, code, chosen, other, decision, question, answer, at))
                return
            same = (row["chosen"], row["other"], row["decision"], row["question"]) == (chosen, other, decision, question)
            if same and row["answer"] == answer:
                return
            if same and row["answer"] is None and answer is not None:
                self.db.execute(f"UPDATE {p}.interpretation SET answer=? WHERE req_id=? AND code=?", (answer, req, code))
                return
            raise ValueError("해석 결정은 고치지 않는다. 바뀐 해석은 새 요청판으로 받는다")

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
                                                     "matched": [], "func": set()})
                d["score"] += r["score"]
                d["slots"].add(n["slot"] if n["slot"] != "summary" else r["slot"])
                d["matched"] += [m for m in matched if m not in d["matched"]]
                d.setdefault("rk", {}).setdefault((n["slot"], "en"), set()).update(matched)   # r4: 검색기 = (필요 칸, 언어)
                d.setdefault("tg", {}).setdefault(r["tag_id"], set()).update(matched)        # r6: 꼬리표 한 줄마다 맞은 단위
                d["func"] |= {m for m in matched if m in FUNCTION_WORDS or m.isdigit()}
        if self.token_rules == "t2":
            self._drawer_ko(needs, at, per_obs, include_function_words)
        hits = []
        # e2(08 I24): 요청이 칸 하나만 쓰면 그 칸에서 서로 다른 내용어 둘로 자격을 준다. 자격 칸 수 = min(min_slots, 요청 칸 수)
        need_slots = len({n["slot"] for n in needs if (n["text"] or "").strip()})
        slots_needed = min(min_slots, max(1, need_slots)) if self.elig_rules == "e2" else min_slots
        for d in per_obs.values():
            d.setdefault("func", set())
            d["lexical_accident"] = all(m in d["func"] for m in d["matched"])
            content_slots = len(d["slots"]) if not d["lexical_accident"] else 0
            distinct = {stem(m) if "~" not in m else m.split("~")[0] for m in d["matched"] if m not in d["func"]}
            d["eligible"] = (content_slots >= slots_needed and len(distinct) >= 2) or \
                            (min_slots <= 1 and content_slots >= 1)
            hits.append(d)
        if self.rank_rules != "r0":
            self._rescore(per_obs, hits, at)
        hits.sort(key=lambda d: (not d["eligible"], d["lexical_accident"], d["score"]))
        hits = hits[:k]
        for d in hits:
            d.pop("func", None)
            d.pop("rk", None)
            d.pop("tg", None)
            # 서랍은 옛 관측의 꼬리표로도 적중한다. 인용 전에 현재 관측을 확인하라고 같이 돌려준다(M7e)
            d["current"] = self.current(d["obs_id"], at)
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

    def _drawer_stats(self, at: str) -> dict:
        """서랍 순위용 통계(07 R-6). 문서 = 관측(그 관측의 꼬리표를 합친 것). at 이전에 관측된 것만 센다.
        df: 영어 어간·한국어 줄기·한국어 2-gram마다 그것을 가진 관측 수. length: 관측의 서로 다른 내용 단위 수."""
        units: dict[int, set] = {}
        tag_len: dict[int, int] = {}
        for r in self.db.execute(
                "SELECT t.tag_id, t.obs_id, t.text, k.words, k.grams FROM tag t JOIN observation o ON o.obs_id = t.obs_id"
                " LEFT JOIN tag_fts_ko k ON k.rowid = t.tag_id WHERE o.observed_at <= ?", (at,)):
            u = units.setdefault(r["obs_id"], set())
            tu = {("en", stem(x)) for x in tokens(r["text"]) if x not in FUNCTION_WORDS and not x.isdigit()}
            if r["words"]:
                tu |= {("kw", w) for w in r["words"].split()}
                u |= {("kg", g) for g in r["grams"].split()}
            u |= tu
            tag_len[r["tag_id"]] = len(tu)   # r6(08 I33): 꼬리표 한 줄의 서로 다른 내용 단위 수
        df: dict[tuple, int] = {}
        for u in units.values():
            for k in u:
                df[k] = df.get(k, 0) + 1
        lengths = {o: sum(1 for k in u if k[0] != "kg") for o, u in units.items()}
        n = len(units) or 1
        # r3(08 I26): 언어 칸별 길이. en = 영어 어간, ko = 한국어 줄기. 평균은 그 칸이 있는 관측만으로
        field_len = {o: {"en": sum(1 for k in u if k[0] == "en"), "ko": sum(1 for k in u if k[0] == "kw")}
                     for o, u in units.items()}
        field_avg = {}
        for f in ("en", "ko"):
            xs = [v[f] for v in field_len.values() if v[f]]
            field_avg[f] = (sum(xs) / len(xs)) if xs else 1.0
        return {"n": n, "df": df, "length": lengths, "avg_len": (sum(lengths.values()) / n) if lengths else 1.0,
                "field_len": field_len, "field_avg": field_avg, "tag_len": tag_len,
                "avg_tag_len": (sum(tag_len.values()) / len(tag_len)) if tag_len else 1.0}

    def _rescore(self, per_obs: dict, hits: list, at: str) -> None:
        """규칙 판 r1: 맞은 내용 단위(질의 낱말 하나 = 한 번)마다 IDF를 더한다. 설계(r0)는 칸·꼬리표 행마다 bm25를 더해
        긴 summary 꼬리표가 모든 칸에서 거듭 점수를 받았다(08 I17). r2: r1을 꼬리표 길이로 정규화한다(BM25의 b).
        점수는 작을수록 앞이다(설계와 같은 방향)."""
        st = self._drawer_stats(at)
        b = config.RANK_LENGTH_B if self.rank_rules in ("r2", "r3") else 0.0
        if self.rank_rules in ("r4", "r5"):
            self._rrf(hits, st, length_b=config.RANK_LENGTH_B if self.rank_rules == "r5" else 0.0)
            return
        if self.rank_rules == "r6":
            self._max_tag(hits, st)
            return
        for d in hits:
            best: dict[str, float] = {}
            field: dict[str, str] = {}
            for m in d["matched"]:
                if m in d.get("func", ()):
                    continue
                if "~" in m:
                    unit, key = m.split("~")[0], ("kg", m.split("~")[1])
                elif re.search(r"[가-힣]", m):
                    unit, key = m, ("kw", m)
                else:
                    unit, key = "en:" + stem(m), ("en", stem(m))
                df = st["df"].get(key, 0)
                idf = math.log(1 + (st["n"] - df + 0.5) / (df + 0.5))
                best[unit] = max(best.get(unit, 0.0), idf)
                field[unit] = "en" if key[0] == "en" else "ko"
            if self.rank_rules == "r3":
                # BM25F처럼 칸마다 그 칸의 길이로 정규화한 뒤 더한다(F30 C5: europeana bm25f-3~5, Elastic combined_fields)
                fl = st["field_len"].get(d["obs_id"], {})
                total = 0.0
                for f in ("en", "ko"):
                    sf = sum(v for u, v in best.items() if field[u] == f)
                    if sf:
                        total += sf / (1 - b + b * (fl.get(f) or st["field_avg"][f]) / st["field_avg"][f])
                d["score"] = -total
            else:
                score = sum(best.values())
                norm = 1 - b + b * st["length"].get(d["obs_id"], st["avg_len"]) / st["avg_len"]
                d["score"] = -score / norm
            if self.elig_idf_min is not None and d["eligible"]:
                # 진단용(08 I20, 채택 안 함): 자격의 "서로 다른 내용어 둘"을 IDF 문턱 이상인 단위로만 센다
                d["eligible"] = sum(1 for v in best.values() if v >= self.elig_idf_min) >= 2

    def _unit_idf(self, m: str, st: dict) -> tuple[str, float]:
        if "~" in m:
            unit, key = m.split("~")[0], ("kg", m.split("~")[1])
        elif re.search(r"[가-힣]", m):
            unit, key = m, ("kw", m)
        else:
            unit, key = "en:" + stem(m), ("en", stem(m))
        df = st["df"].get(key, 0)
        return unit, math.log(1 + (st["n"] - df + 0.5) / (df + 0.5))

    def _max_tag(self, hits: list, st: dict) -> None:
        """규칙 판 r6(08 I33): 꼬리표 한 줄당 최대 점수. 꼬리표마다 그 줄에서 맞은 내용 단위의 IDF 합(단위는 한 번)을 그 줄의 길이로
        보정하고(1 - b + b·줄 길이/평균 줄 길이, b = RANK_LENGTH_B), 관측 점수는 그 가운데 최댓값이다. 꼬리표가 늘어도 관측이
        깎이지 않고, 긴 줄 하나가 여러 낱말을 모아 이기지도 않는다. 근거(opensource catalog/by-problem/F30.md @ 423aebf, L1):
        Vespa의 다값 칸 maxWeight(맞은 원소 가운데 최댓값, C5-S02-b1-r08). 점수는 작을수록 앞이다."""
        b = config.RANK_LENGTH_B
        avg = st["avg_tag_len"]
        for d in hits:
            best_tag = 0.0
            for tag_id, ms in d.get("tg", {}).items():
                best: dict[str, float] = {}
                for m in ms:
                    if m in d.get("func", ()):
                        continue
                    unit, idf = self._unit_idf(m, st)
                    best[unit] = max(best.get(unit, 0.0), idf)
                if best:
                    norm = 1 - b + b * st["tag_len"].get(tag_id, avg) / avg
                    best_tag = max(best_tag, sum(best.values()) / norm)
            d["score"] = -best_tag

    def _rrf(self, hits: list, st: dict, length_b: float = 0.0) -> None:
        """규칙 판 r4(08 I28): 검색기 = (필요 칸, 언어). 검색기마다 맞은 단위의 IDF 합(r1, 길이 정규화 없음)으로 순위를 내고
        RRF로 합친다: 점수 = 검색기마다 1/(RRF_K + 순위)의 합. 한 검색기에만 나온 관측도 남긴다(외부 조인). 결과 창은 자르지 않는다.
        근거(opensource catalog/claims/F30.tsv @ 286d9d55, 모두 L1): Elastic RRF retriever(C5-S03-b1-r12, rank_constant 기본 60),
        pyterrier fusion 외부 조인(C5-S03-b3-r09). 점수는 작을수록 앞이다.
        r5(08 I31): 검색기 안의 점수를 r2처럼 관측 전체 길이로 보정한다(IDF 합 / (1 - b + b·길이/평균)). 합치는 것은 그대로 순위만."""
        per_ranker: dict = {}
        for d in hits:
            for rk, ms in d.get("rk", {}).items():
                best: dict[str, float] = {}
                for m in ms:
                    if m in d.get("func", ()):
                        continue
                    unit, idf = self._unit_idf(m, st)
                    best[unit] = max(best.get(unit, 0.0), idf)
                if best:
                    norm = 1 - length_b + length_b * st["length"].get(d["obs_id"], st["avg_len"]) / st["avg_len"]
                    per_ranker.setdefault(rk, []).append((sum(best.values()) / norm, d["obs_id"]))
        fused: dict[int, float] = {}
        for rk, xs in per_ranker.items():
            xs.sort(key=lambda t: (-t[0], t[1]))
            for i, (_sc, oid) in enumerate(xs, 1):
                fused[oid] = fused.get(oid, 0.0) + 1.0 / (config.RRF_K + i)
        for d in hits:
            d["score"] = -fused.get(d["obs_id"], 0.0)

    def _drawer_ko(self, needs, at, per_obs: dict, include_function_words: bool) -> None:
        """한국어 두 층(어절 줄기·음절 2-gram)으로 같은 칸 꼬리표를 맞춘다(07 R-5, t2). 결과는 per_obs에 더한다."""
        for n in needs:
            units = ko_tok.ko_units(n["text"], include_function=include_function_words)
            if not units:
                continue
            terms = [f'words : "{u["word"]}"' for u in units] + \
                    [f'grams : "{g}"' for g in dict.fromkeys(g for u in units for g in u["grams"])]
            slot_filter = "" if n["slot"] == "summary" else "AND (t.slot=? OR t.slot='summary')"
            args = [" OR ".join(terms), at] + ([] if n["slot"] == "summary" else [n["slot"]])
            rows = self.db.execute(
                "SELECT t.tag_id, t.obs_id, t.slot, k.words, k.grams, bm25(tag_fts_ko) AS score FROM tag_fts_ko k"
                " JOIN tag t ON t.tag_id = k.rowid JOIN observation o ON o.obs_id = t.obs_id"
                f" WHERE tag_fts_ko MATCH ? AND o.observed_at <= ? {slot_filter}", args).fetchall()
            for r in rows:
                matched = ko_tok.match_units(units, set(r["words"].split()), set(r["grams"].split()))
                if not matched:
                    continue
                d = per_obs.setdefault(r["obs_id"], {"obs_id": r["obs_id"], "score": 0.0, "slots": set(),
                                                     "matched": [], "func": set()})
                d["score"] += r["score"]
                d["slots"].add(n["slot"] if n["slot"] != "summary" else r["slot"])
                d["matched"] += [m for m, _f in matched if m not in d["matched"]]
                d.setdefault("rk", {}).setdefault((n["slot"], "ko"), set()).update(m for m, _f in matched)
                d.setdefault("tg", {}).setdefault(r["tag_id"], set()).update(m for m, _f in matched)
                d["func"] |= {m for m, f in matched if f}

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

    def drawer_contribution(self, p: str, req: int) -> dict:
        """S로 줄이는 규칙(04 7절)의 입력. 서랍만 찾은 적격 후보 가운데 이 요청의 답 자리(대조 인용 제외)나
        접힌 근접 대안에 실제로 오른 것만 센다. 적격 적중 수는 쓸모와 무관하게 거의 늘 1 이상이다(M8)."""
        only = set(self.path_log(p, req)["drawer_only"])
        used = set()
        for (run,) in self.db.execute(f"SELECT run_id FROM {p}.answer_run WHERE req_id=?", (req,)).fetchall():
            used |= {self.obs(o)["url"] for (o,) in self.db.execute(
                f"SELECT obs_id FROM {p}.usage WHERE run_id=? AND part<>'contrast'", (run,))}
            used |= {u for (u,) in self.db.execute(f"SELECT url FROM {p}.folded WHERE run_id=?", (run,))}
        return {"drawer_only_eligible": len(only), "drawer_only_used": sorted(only & used)}

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
            if self.stale(s["obs_id"], at):
                # 무효가 된 관측이나 철회된 판독에 기댄 쪽지는 옮기지 않는다(M4c, M7d)
                dropped.append({"slip": s["slip_id"], "code": s["code"], "obs": s["obs_id"],
                                "premise_mismatch": [k for k, v in prem.items() if ctx.get(k) != v],
                                "edition_mismatch": not ed_ok, "superseded": True})
                continue
            if ok and ed_ok:
                kept.append(self.judge(p, new_req, s["code"], s["obs_id"], s["verdict"], s["role"], s["ladder"],
                                       s["reason"], at, premises=prem, cause="request", supersedes=s["slip_id"]))
            else:
                dropped.append({"slip": s["slip_id"], "code": s["code"], "obs": s["obs_id"],
                                "premise_mismatch": [k for k, v in prem.items() if ctx.get(k) != v],
                                "edition_mismatch": not ed_ok})
        return {"kept": kept, "dropped": dropped}

    @staticmethod
    def edition_matches(context_version: str, edition_key: str) -> bool:
        """맥락의 판과 관측 판이 맞는가(07 D9). 맥락이 작은 판까지만 말하면('CPython 3.13') 같은 작은 판의
        어느 수정 판('v3.13.18')이든 맞고, 수정 판까지 말하면('3.13.18') 그 판만 맞는다. 답 문장에는 관측 판을 적는다."""
        ver = context_version.split()[-1] if context_version else ""
        ek = edition_key.lstrip("v")
        return bool(ver) and (ek == ver or ek.startswith(ver + "."))

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
        for i, s in enumerate(slots, 1):
            if s.get("kind") == "check":
                addr = self.obs(s["first"])["url"] if s.get("first") else s.get("url")
                # first 없이 url만 준 확인할 후보도 같은 검사를 받는다(예전에는 이 길로 검사를 건너뛰었다)
                if not addr or addr not in searched:
                    raise ValueError("확인할 후보도 탐색 기록에 있는 이름만 낸다(모델 기억에서만 나온 이름 금지)")
            if s.get("kind") == "principle" and s.get("ladder") not in ("L0", "L1", "L2"):
                raise ValueError("원리 자리의 근거 수준은 L2를 넘지 않는다(04 3.5 규칙 4)")
            for part in ("first", "support", "flip"):
                ids = [s.get(part)] if part == "first" else s.get(part, [])
                for oid in ids:
                    if oid and self.stale(oid, at):
                        raise ValueError(f"대체되었거나 철회된 관측 {oid}를 근거로 인용할 수 없다. "
                                         f"현재 관측 {self.current(oid, at)}을 확인해 인용한다(대조 인용은 허용)")
        if status == "complete":
            first = slots[0] if slots else {}
            if first.get("kind") not in ("direct", "transplant") or first.get("ladder") not in ("L2", "L3", "L4"):
                raise ValueError("complete는 1번 자리가 직접·이식 자리이고 L2 이상일 때만 쓴다(04 3.2, 3.5 규칙 2)")
        with self.db:
            run = self.db.execute(
                f"INSERT INTO {p}.answer_run(req_id, produced_at, status, budget_json, next_action, rule_version, idem_key)"
                " VALUES (?,?,?,?,?,?,?)",
                (req, at, status, json.dumps(budget or {}, ensure_ascii=False), next_action, self.RULE_VERSION,
                 key)).lastrowid
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
        seal = self.db.execute(f"SELECT sealed_at FROM {p}.prior_seal WHERE req_id=?", (req,)).fetchone()
        if not seal or seal[0] > at:
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
            todo += [r[0] for r in self.db.execute(
                "SELECT s.old_obs FROM supersession s WHERE s.new_obs=? AND NOT EXISTS (SELECT 1 FROM supersession_cancel c"
                " WHERE c.old_obs=s.old_obs AND c.new_obs=s.new_obs)", (o,))]
        return out

    def propagate(self, p: str, at: str) -> list[dict]:
        """at까지 알려진 대체 가운데 이 프로젝트 답 자리에 닿는 것만 알림으로 만든다.
        usage=False이면 어느 자리가 무엇을 인용했는지 모르므로 프로젝트의 모든 답 자리에 알린다."""
        out = []
        # at까지 취소된 대체는 알리지 않는다(알리기 전에 취소됐으면 알림도 복원도 없다)
        sups = self.db.execute(
            "SELECT * FROM supersession s WHERE s.known_from<=? AND NOT EXISTS (SELECT 1 FROM supersession_cancel c"
            " WHERE c.old_obs=s.old_obs AND c.new_obs=s.new_obs AND c.cancelled_at<=?) ORDER BY s.known_from",
            (at, at)).fetchall()
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
                        f"INSERT OR IGNORE INTO {p}.notice(run_id, slot_no, old_obs, new_obs, effect, created_at, text, held)"
                        " VALUES (?,?,?,?,?,?,?,?)",
                        (t["run_id"], t["slot_no"], s["old_obs"], s["new_obs"], s["effect"], s["known_from"], text,
                         0 if self.is_active(p, t["run_id"], s["known_from"]) else 1))
                    if cur.rowcount:
                        out.append({"run": t["run_id"], "slot": t["slot_no"], "effect": s["effect"], "text": text})
            # 대체 취소: 그 대체로 알림을 받은 자리에 '다시 유효'를, 철회된 판독을 인용한 자리에 '근거 무효'를 붙인다
            cancels = self.db.execute(
                "SELECT c.*, s.known_from FROM supersession_cancel c JOIN supersession s USING(old_obs, new_obs)"
                " WHERE c.cancelled_at<=? ORDER BY c.cancelled_at", (at,)).fetchall()
            for c in cancels:
                groups = (
                    ("restored", f"다시 유효: 대체 취소({c['reason']}) (취소 시각 {c['cancelled_at']})",
                     f"SELECT DISTINCT run_id, slot_no FROM {p}.notice WHERE old_obs=? AND new_obs=?",
                     (c["old_obs"], c["new_obs"])),
                    ("invalidates", f"근거 무효: 철회된 판독({c['reason']}) (취소 시각 {c['cancelled_at']})",
                     f"SELECT DISTINCT u.run_id, u.slot_no FROM {p}.usage u JOIN {p}.answer_run r USING(run_id)"
                     f" WHERE u.obs_id=? AND u.part<>'contrast' AND r.produced_at<=?", (c["new_obs"], c["cancelled_at"])),
                )
                for effect, text, sql, args in groups:
                    for t in self.db.execute(sql, args).fetchall():
                        cur = self.db.execute(
                            f"INSERT OR IGNORE INTO {p}.notice(run_id, slot_no, old_obs, new_obs, effect, created_at, text, held)"
                            " VALUES (?,?,?,?,?,?,?,?)",
                            (t["run_id"], t["slot_no"], c["new_obs"], c["old_obs"], effect, c["cancelled_at"], text,
                             0 if self.is_active(p, t["run_id"], c["cancelled_at"]) else 1))
                        if cur.rowcount:
                            out.append({"run": t["run_id"], "slot": t["slot_no"], "effect": effect, "text": text})
            # 원문 접근 실패(04 6.2, 08 I38): 같은 실패가 문턱만큼 이어진 기준 관측의 계보를 인용한 자리에 알린다.
            # 실패는 대체가 아니다. 앞 관측은 그대로 두고 표시만 붙인다
            for f in self.db.execute("SELECT * FROM source_failure WHERE at<=? ORDER BY at", (at,)).fetchall():
                chain = self.ancestors(f["base_obs"])
                marks = ",".join("?" * len(chain))
                text = f"원문 접근 실패: {f['outcome']} {f['streak']}회 연속 (마지막 시각 {f['at']})"
                for t in self.db.execute(
                        f"SELECT DISTINCT u.run_id, u.slot_no FROM {p}.usage u JOIN {p}.answer_run r USING(run_id)"
                        f" WHERE u.obs_id IN ({marks}) AND u.part<>'contrast' AND r.produced_at<=?",
                        (*chain, f["at"])).fetchall():
                    cur = self.db.execute(
                        f"INSERT OR IGNORE INTO {p}.notice(run_id, slot_no, old_obs, new_obs, effect, created_at, text, held)"
                        " VALUES (?,?,?,?,?,?,?,?)",
                        (t["run_id"], t["slot_no"], f["base_obs"], f["fail_obs"], "source_unreachable", f["at"], text,
                         0 if self.is_active(p, t["run_id"], f["at"]) else 1))
                    if cur.rowcount:
                        out.append({"run": t["run_id"], "slot": t["slot_no"], "effect": "source_unreachable", "text": text})
            # 원문 다시 읽힘(08 I44): 그 실패로 '원문 접근 실패' 알림을 받은 자리에만 붙인다. 내용 변화는 대체 알림이 따로 한다
            for r in self.db.execute(
                    "SELECT r.at, r.obs_id, f.base_obs, f.fail_obs FROM source_recovery r JOIN source_failure f USING(failure_id)"
                    " WHERE r.at<=? ORDER BY r.at", (at,)).fetchall():
                text = f"원문 다시 읽힘: {r['at']}에 원문을 다시 읽었다"
                for t in self.db.execute(
                        f"SELECT DISTINCT run_id, slot_no FROM {p}.notice WHERE effect='source_unreachable' AND old_obs=?"
                        " AND new_obs=?", (r["base_obs"], r["fail_obs"])).fetchall():
                    cur = self.db.execute(
                        f"INSERT OR IGNORE INTO {p}.notice(run_id, slot_no, old_obs, new_obs, effect, created_at, text, held)"
                        " VALUES (?,?,?,?,?,?,?,?)",
                        (t["run_id"], t["slot_no"], r["fail_obs"], r["obs_id"], "source_recovered", r["at"], text,
                         0 if self.is_active(p, t["run_id"], r["at"]) else 1))
                    if cur.rowcount:
                        out.append({"run": t["run_id"], "slot": t["slot_no"], "effect": "source_recovered", "text": text})
            # 별칭 취소: 그 별칭을 따라 연 관측을 인용한 자리에 알린다(07 D5). 관측 자체는 그 주소에 대해 여전히 참이다
            for a in self.db.execute(
                    "SELECT c.alias_id, c.cancelled_at, c.reason FROM locator_alias_cancel c WHERE c.cancelled_at<=?"
                    " ORDER BY c.cancelled_at", (at,)).fetchall():
                text = (f"주소 별칭 취소: 이 근거는 별칭을 따라 연 다른 대상일 수 있다({a['reason']}). "
                        f"원 주소에서 다시 확인한다 (취소 시각 {a['cancelled_at']})")
                for t in self.db.execute(
                        f"SELECT DISTINCT u.run_id, u.slot_no, u.obs_id FROM {p}.usage u JOIN {p}.answer_run r USING(run_id)"
                        " JOIN observation o ON o.obs_id=u.obs_id WHERE o.via_alias=? AND u.part<>'contrast'"
                        " AND r.produced_at<=?", (a["alias_id"], a["cancelled_at"])).fetchall():
                    cur = self.db.execute(
                        f"INSERT OR IGNORE INTO {p}.notice(run_id, slot_no, old_obs, new_obs, effect, created_at, text, held)"
                        " VALUES (?,?,?,?,?,?,?,?)",
                        (t["run_id"], t["slot_no"], t["obs_id"], t["obs_id"], "alias_cancelled", a["cancelled_at"], text,
                         0 if self.is_active(p, t["run_id"], a["cancelled_at"]) else 1))
                    if cur.rowcount:
                        out.append({"run": t["run_id"], "slot": t["slot_no"], "effect": "alias_cancelled", "text": text})
        return out

    def is_active(self, p: str, run_id: int, at: str) -> bool:
        """at 시각에 이 실행이 활성 답인가(07 D2, ACTIVE_RULE). 활성이 아닌 답의 알림은 쌓되(held) 알리지 않고 재생 때 붙인다."""
        if self.ACTIVE_RULE == "all":
            return True
        key = self.db.execute(f"SELECT r.request_key FROM {p}.answer_run a JOIN {p}.request_rev r USING(req_id)"
                              " WHERE a.run_id=?", (run_id,)).fetchone()[0]
        runs = self.db.execute(
            f"SELECT a.run_id, EXISTS(SELECT 1 FROM {p}.exposure x WHERE x.run_id=a.run_id AND x.event='shown'"
            f" AND x.at<=?) AS shown FROM {p}.answer_run a JOIN {p}.request_rev r USING(req_id)"
            " WHERE r.request_key=? AND a.produced_at<=? ORDER BY a.produced_at, a.run_id", (at, key, at)).fetchall()
        if not runs:
            return True
        pool = [r for r in runs if r["shown"]] if self.ACTIVE_RULE == "shown_latest" else []
        return (pool or runs)[-1]["run_id"] == run_id

    def inbox(self, p: str, at: str) -> list[sqlite3.Row]:
        """사용자에게 알릴 알림(활성 답의 알림만). 재생(replay)은 held 알림도 붙인다."""
        return self.db.execute(f"SELECT * FROM {p}.notice WHERE held=0 AND created_at<=? ORDER BY created_at, notice_id",
                               (at,)).fetchall()

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
