"""확인 장부 구조 v1 운영 시뮬레이션.

완성된 시스템이 몇 달 운영된다고 두고, 설계서가 말한 규칙이 그대로 버티는지 엔진(db/ledger.py)을
직접 돌려 본다. 사례 재생(db/cases.py)은 사건마다 손으로 알맞은 시각에 폴링하고 알맞은 위치를 읽었다.
여기서는 그 손을 떼고 시계·작업자·예산·여러 프로젝트를 붙인다.

시나리오 ID와 묻는 것:
  M1  실제 시계로 EVAL-X1 재생(72시간 폴링, 매시 기한 시계, 매시 작업자, 위상 12개)
  M2  대량: 공용 장부·프로젝트 수가 늘 때 서랍 잡음, 사생활 검사, 전파의 비용
  M3  열람 예산 축소: 세는 법 셋의 모순, 출처가 늘 때 단일 예산의 붕괴(엔진에 시계별 예산이 있으면 그 격자도)
  M4  출처 이동·철회·잘못된 대체: 별칭 취소, 공급자 철회, 대체 되돌리기
  M5  동시 변경: 임차 만료 뒤 늦은 완료, 임차 중 새 원인, 판독 비결정성
  M6  다국어 신규 출처: 일본어 꼬리표, 한국어 필요 문장, 한국어 사생활 검사
  M7  판단 오염: 과다 꼬리표, 판독기 오류 회수, 공개 장부의 요청 수치, 쪽지 승계, 낡은 인용
  M8  S로 줄이는 규칙(C4)의 입력 지표가 쓸모를 재는가
  M9  시각 형식: 날짜만 있는 기한, 시간대 표기
  M10 보존과 삭제: 권리자 삭제 요청, 비공개 주소, 요청 시각 노출
  M11 알림 누적과 활성 답
  M12 채널 ID 체계 변경과 중복 ID

판정 값: "깨짐"(설계서가 말한 동작과 다르게 나온다), "빈칸"(설계서가 정하지 않아 구현자가 막힌다),
"모순"(설계서의 두 곳이 서로 다르다), "유지"(규칙이 버텼다).
판정은 관측값에서 계산한다. 같은 코드를 고친 엔진에 돌리면 판정이 바뀔 수 있다. 엔진에 07 6절 결정의 기능
(via_alias, visibility, redact, job_editions, fetched, notice.held)이 있으면 쓰고, 없으면 v1처럼 돈다.

실행:
  python3 -I ops_sim.py                         # 요약 출력, out/sim.json 쓰기
  python3 -I ops_sim.py --engine DIR --out F    # 다른 엔진 디렉터리(ledger.py, schema.sql, project_schema.sql)로
  ./pin_v1.sh                                   # PR #9 첫 커밋 f1698015의 엔진으로 돌려 out/sim_v1.json
측정 시간(초)은 out/perf.txt에만 남긴다. sim.json은 같은 엔진·같은 Python에서 바이트까지 같다.
"""
from __future__ import annotations

import argparse
import inspect
import json
import random
import re
import sqlite3
import sys
import time
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE.parent / "db"
FMT = "%Y-%m-%dT%H:%M:%SZ"
PERF: list[str] = []

eng = None     # ledger 모듈
cases = None   # 사례 자료(고정 문자열과 사례 함수)


def load(engine_dir: Path):
    global eng, cases
    sys.path.insert(0, str(engine_dir))
    import ledger as _ledger  # noqa: E402
    eng = _ledger
    sys.path.insert(1, str(DB))
    import cases as _cases  # noqa: E402  (ledger는 이미 올라와 있어 cases도 같은 엔진을 쓴다)
    cases = _cases


# ---------------------------------------------------------------------------- 시각
def P(s: str) -> datetime:
    return datetime.strptime(s, FMT).replace(tzinfo=timezone.utc)


def S(d: datetime) -> str:
    return d.strftime(FMT)


def hours(a: str, b: str) -> float:
    return (P(b) - P(a)).total_seconds() / 3600


def plus(s: str, h: float) -> str:
    return S(P(s) + timedelta(hours=h))


# ---------------------------------------------------------------------------- 엔진 호환(v1과 고친 판)
def has_param(fn, name) -> bool:
    return name in inspect.signature(fn).parameters


def reusable(L, url, ek, pos, project=None, at=None):
    if has_param(L.reusable, "at"):
        return L.reusable(url, ek, pos, project=project, at=at)
    return L.reusable(url, ek, pos, project=project)


def finish(L, job_id, result_obs, token=None, sup=None):
    """sup = (old_obs, effect, known_from, effective_from). 고친 엔진은 임차 표지가 맞을 때만 대체까지 한 거래로 쓴다.
    v1은 대체를 먼저 쓰고 완료를 따로 적는다(사례 재생과 같은 순서)."""
    if has_param(L.finish, "token"):
        kw = {"token": token}
        if sup:
            kw["supersede"] = sup
        return L.finish(job_id, result_obs, **kw)
    if sup:
        L.supersede(sup[0], result_obs, sup[1], known_from=sup[2], effective_from=sup[3])
    L.finish(job_id, result_obs)
    return None


def verdict(broken: bool, kind="깨짐") -> str:
    return kind if broken else "유지"


def table_cols(L, table, schema="main") -> list[str]:
    return [r[1] for r in L.db.execute(f"PRAGMA {schema}.table_info({table})")]


def quote_sql(L) -> tuple[str, str]:
    """인용 본문을 읽는 SELECT 식과 JOIN. 고친 엔진은 인용을 quote_text로 뗐고(07 D7), v1은 observation.quote에 둔다."""
    if L.db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='quote_text'").fetchone():
        return "q.text AS quote", " LEFT JOIN quote_text q ON q.quote_fp=o.quote_fp"
    return "o.quote", ""


# ============================================================================ M1 실제 시계
DEADLINE_OF = {"297191": "2025-07-08T00:00:00Z", "300072": "2025-10-08T00:00:00Z",
               "308355": "2025-11-06T00:00:00Z", "308427": "2025-11-12T00:00:00Z"}   # cases.case_b와 같은 값
T0_X1 = "2025-05-15T00:00:00Z"
POS_KB = "When is Pocket shutting down / dates"


def kb_revs():
    return [(ext, eff, reading, effect) for ext, _seen, _key, eff, _src, reading, effect in cases.POCKET_EVENTS]


PUB_OFF = [0]   # 개정이 효력일 0시에서 몇 시간 뒤 실제로 올라오나(가정). 0이면 사례 재생과 같은 세계


def kb_current(t: str):
    cur = None
    for ext, eff, reading, effect in kb_revs():
        if plus(eff, PUB_OFF[0]) <= t:
            cur = (ext, eff, reading, effect)
    return cur


def kb_history(t: str):
    return [{"id": ext, "title": f"future-of-pocket revision {ext}", "url": cases.KB, "edition": f"rev:{ext}"}
            for ext, eff, _r, _e in reversed(kb_revs()) if plus(eff, PUB_OFF[0]) <= t]


def moz_feed(t: str):
    if t >= plus("2025-05-22T00:00:00Z", PUB_OFF[0]):
        return [{"id": "building-whats-next", "title": "Building what's next",
                 "summary": "Pocket: 신규 다운로드 중단, 7월 8일 서비스 종료, 10월 8일 내보내기 예정", "url": cases.KB}]
    return []


def setup_x1(L):
    p = L.project("X")
    req = L.intake(p, request_key="X1", rev=1, at=T0_X1, text=cases.X1_TEXT, selected_part="저장 목록 계층",
                   requirements=[{"code": "R1", "kind": "must", "text": "공개 형식 내보내기"}],
                   prior={"known": []}, needs=cases.X1_NEEDS)
    L.search_fresh(p, req, T0_X1, {"direct": [{"url": cases.POCKET_HOME}],
                                   "domain_guess": [{"url": cases.OAI_URL}]})
    pocket0, _ = L.observe(url=cases.POCKET_HOME, edition_key="fetch:2025-05-15", edition_kind="fetch",
                           position="검색 결과 항목", at=T0_X1, method="intro_only",
                           statement="검색 결과에서 이름과 주소만 확인했다.", project=p)
    oai, _ = L.observe(url=cases.OAI_URL, edition_key="2.0 (doc 2015-01-08)", edition_kind="release",
                       position="§2.5.1", at=T0_X1, method="read_line", quote=cases.OAI_PERSISTENT, quote_lang="en",
                       statement="삭제 정보 보존 수준을 구분한다.", project=p)
    slots = [{"kind": "check", "first": pocket0, "ladder": "L0", "hold": "판독 전", "verb": "Pocket", "reason": "API 절"},
             {"kind": "principle", "first": oai, "contrast": [pocket0], "ladder": "L2", "verb": "증분 수확",
              "where": "§2.5.1", "borrow": "b", "recheck": "r", "break": "x", "hold": "h"}]
    run0 = L.compose(p, req, T0_X1, slots=slots, status="partial", next_action="API 문서를 연다")
    L.channel("mozilla", cases.MOZ_FEED, "feed", period_h=72)
    L.watch(pocket0, cases.MOZ_FEED, "Pocket", layer="supplier")
    L.poll(cases.MOZ_FEED, moz_feed(T0_X1), T0_X1)
    return p, req, run0, pocket0, oai


def worker_read_kb(L, job, ts, deadlines, state):
    """작업자 한 번. 채널 항목이 문서를 가리키면 그 문서를, 아니면 관측 위치를 읽는다(설계서가 정하지 않은 선택)."""
    cur = kb_current(ts)
    if cur is None:
        return None, None, None
    ext, eff, reading, effect = cur
    new, created = L.observe(url=cases.KB, edition_key=f"rev:{ext}", edition_kind="revision", position=POS_KB,
                             at=ts, method="read_line", quote=reading, quote_lang="ko-reading", published_at=eff[:10],
                             statement=reading, flip_position="기한과 가용 범위 문장", via="channel")
    sup = None
    if created:
        old = L.current(job["obs_id"], ts)
        if old != new:
            sup = (old, effect, ts, eff)
    return new, sup, ext


def run_x1_clock(phase_h: int, period_h=72, deadlines=True, end="2025-11-20T00:00:00Z") -> dict:
    L = eng.Ledger()
    p, req, run0, pocket0, oai = setup_x1(L)
    next_poll = {cases.MOZ_FEED: plus(T0_X1, phase_h)}
    t = T0_X1
    reads = 0
    while t <= end:
        # 1) 배경 시계: 주기가 된 채널만 폴링
        for ch in list(next_poll):
            if t >= next_poll[ch]:
                L.poll(ch, moz_feed(t) if ch == cases.MOZ_FEED else kb_history(t), t)
                next_poll[ch] = plus(next_poll[ch], period_h)
        # 2) 기한 시계
        if deadlines:
            L.due(t)
        # 3) 작업자
        L.release_expired(t)
        for j in L.jobs():
            tok = L.lease(j["job_id"], plus(t, 1))
            if not tok:
                continue
            reads += 1
            new, sup, ext = worker_read_kb(L, j, t, deadlines, None)
            if new is None:
                finish(L, j["job_id"], None, token=tok)
                continue
            if cases.KB_HISTORY not in next_poll:
                L.channel("mozilla", cases.KB_HISTORY, "revision_history", period_h=period_h)
                L.poll(cases.KB_HISTORY, kb_history(t), t)       # 기준선
                k = 0
                while plus(T0_X1, phase_h + k * period_h) <= t:
                    k += 1
                next_poll[cases.KB_HISTORY] = plus(T0_X1, phase_h + k * period_h)
            finish(L, j["job_id"], new, token=tok, sup=sup)
            L.watch(new, cases.KB_HISTORY, deadline=DEADLINE_OF.get(ext) if deadlines else None)
        # 4) 전파
        L.propagate(p, t)
        t = plus(t, 1)
    out = {"phase_h": phase_h}
    seen = {}
    for ext, eff, _r, _e in kb_revs():
        row = L.db.execute(
            "SELECT min(o.observed_at) FROM observation o JOIN edition e USING(edition_id) WHERE e.edition_key=?",
            (f"rev:{ext}",)).fetchone()[0]
        seen[ext] = {"observed_at": row, "lag_h": round(hours(eff, row), 1) if row else None}
    out["revisions"] = seen
    jobs = L.db.execute("SELECT cause, count(*) FROM recheck_job GROUP BY cause ORDER BY cause").fetchall()
    out["jobs"] = {r[0]: r[1] for r in jobs}
    out["jobs_total"] = sum(out["jobs"].values())
    out["reads"] = reads
    k = L.known_on(cases.KB, "2025-10-09T12:00:00Z")
    out["known_2025_10_09T12"] = next((ext for ext, _e, r, _x in kb_revs() if k and r == k["statement"]), None)
    notes = L.db.execute(f"SELECT slot_no, count(*) FROM {p}.notice GROUP BY slot_no").fetchall()
    out["notices"] = {str(r[0]): r[1] for r in notes}
    sup_watch = L.db.execute(
        "SELECT count(*) FROM watch w JOIN channel c USING(channel_id) WHERE c.url=? AND w.obs_id NOT IN"
        " (SELECT old_obs FROM supersession)", (cases.MOZ_FEED,)).fetchone()[0]
    out["supplier_layer_watch_alive_at_end"] = sup_watch
    L.db.close()
    return out


def m1() -> dict:
    phases = list(range(0, 72, 6))

    def sweep(pub_off, deadlines):
        PUB_OFF[0] = pub_off
        runs = [run_x1_clock(ph, deadlines=deadlines) for ph in phases]
        PUB_OFF[0] = 0
        lag = {}
        for ext in runs[0]["revisions"]:
            vals = [r["revisions"][ext]["lag_h"] for r in runs]
            seen_ = [v for v in vals if v is not None]
            lag[ext] = {"min": min(seen_) if seen_ else None, "max": max(seen_) if seen_ else None,
                        "never_observed_phases": sum(1 for v in vals if v is None)}
        return runs, {"jobs_total_min_max": [min(r["jobs_total"] for r in runs), max(r["jobs_total"] for r in runs)],
                      "known_2025_10_09T12_counts": dict(Counter(r["known_2025_10_09T12"] for r in runs)),
                      "lag_hours": lag,
                      "max_principle_slot_notices": max(r["notices"].get("2", 0) for r in runs),
                      "supplier_layer_watch_alive_at_end": max(r["supplier_layer_watch_alive_at_end"] for r in runs),
                      "supplier_layer_watch_alive_all_phases": all(r["supplier_layer_watch_alive_at_end"] for r in runs)}

    runs0, case_world = sweep(0, True)
    _, case_world_nodeadline = sweep(0, False)
    _, late_world = sweep(14, True)
    _, late_world_nodeadline = sweep(14, False)
    claim_jobs = [r["jobs_total"] for r in runs0]
    k1009 = Counter(r["known_2025_10_09T12"] for r in runs0)

    # M1b: 기한 없는 문서에서 72시간 안에 개정 두 개가 쌓이면 가운데 판을 읽지 못한다(규칙 (5) "각각 읽는다")
    L = eng.Ledger()
    doc, hist = "https://docs.example/pricing", "https://docs.example/pricing/history"
    revs = [("r1", "2026-01-01T00:00:00Z", "무료 등급 월 1,000회"), ("r2", "2026-01-11T00:00:00Z", "무료 등급 월 500회"),
            ("r3", "2026-01-12T00:00:00Z", "무료 등급 폐지")]   # 폴링은 1·4·7·10·13일 0시
    o, _ = L.observe(url=doc, edition_key="rev:r1", edition_kind="revision", position="요금표", at=revs[0][1],
                     method="read_line", quote=revs[0][2], quote_lang="ko", statement=revs[0][2])
    L.channel("ex", hist, "revision_history", period_h=72)
    L.poll(hist, [{"id": "r1", "title": "r1", "url": doc, "edition": "rev:r1"}], revs[0][1])
    L.watch(o, hist)
    t = revs[0][1]
    while t <= "2026-01-20T00:00:00Z":
        if hours(revs[0][1], t) % 72 == 0:
            L.poll(hist, [{"id": rid, "title": rid, "url": doc, "edition": f"rev:{rid}"} for rid, eff, _ in revs
                          if eff <= t], t)
        for j in L.jobs():
            tok = L.lease(j["job_id"], plus(t, 1))
            todo = [r for r in revs if r[1] <= t][-1:]
            if hasattr(L, "job_editions"):     # 고친 엔진(07 D3): 합친 작업이 든 판을 발행 순으로 모두 읽는다
                keys = {e["edition_key"] for e in L.job_editions(j["job_id"])}
                todo = [r for r in revs if r[1] <= t and f"rev:{r[0]}" in keys] or todo
            for k, (rid, eff, text) in enumerate(todo):
                new, created = L.observe(url=doc, edition_key=f"rev:{rid}", edition_kind="revision", position="요금표",
                                         at=t, method="read_line", quote=text, quote_lang="ko", statement=text)
                cur = L.current(j["obs_id"], t)
                if k < len(todo) - 1:
                    if created and cur != new:
                        L.supersede(cur, new, "changes_value", known_from=t, effective_from=eff)
                    continue
                finish(L, j["job_id"], new, token=tok,
                       sup=(cur, "changes_value", t, eff) if created and cur != new else None)
            L.watch(new, hist)
        t = plus(t, 1)
    observed = [r[0] for r in L.db.execute(
        "SELECT e.edition_key FROM observation o JOIN edition e USING(edition_id) ORDER BY o.obs_id")]
    merged = [r[0] for r in L.db.execute("SELECT merged_causes FROM recheck_job")]
    L.db.close()
    m1b_lost = "rev:r2" not in observed

    def unit2(world, off):
        """06 3.4 단위 2 완료 기준: 각 개정이 게시 뒤 폴링 주기(72) + 24시간 안에 관측, 공급자 층 감시 유지, 원리 자리 알림 0"""
        return (all(v["never_observed_phases"] == 0 and v["max"] - off <= 72 + 24 for v in world["lag_hours"].values())
                and world["supplier_layer_watch_alive_all_phases"] and world["max_principle_slot_notices"] == 0)
    v1_claim = min(claim_jobs) == 5 and max(claim_jobs) == 5 and len(k1009) == 1
    crit = {"case_world": unit2(case_world, 0), "late_world": unit2(late_world, 14)}
    broken = not all(crit.values()) or m1b_lost
    return {
        "id": "M1", "title": "실제 시계로 EVAL-X1 재생",
        "claim": "06 3.4 단위 2 완료 기준: 실제 폴링 시계에서 각 개정이 게시 뒤 폴링 주기 + 24시간 안에 관측되고, 대체 뒤에도 공급자 층 감시가 "
                 "살아 있고, 원리 자리 알림 0. 기한 없는 문서의 중간 개정도 관측한다(discovery_ops 6절 규칙 (5)). "
                 "v1 기준(사건마다 작업 1개, '10월 9일에 알던 기한' 11월 6일)은 v1_claim_holds에 따로 적는다",
        "setup": "72시간 폴링(위상 0~66시간, 6시간 간격 12개), 매시 기한 시계와 작업자, 2025-05-15~11-20. "
                 "세계 둘: 개정이 효력일 0시에 올라옴(사례 재생과 같음) / 14시에 올라옴[가정]. 기한 시계를 켜고 끈다",
        "observed": {
            "jobs_total_by_phase": dict(zip(map(str, phases), claim_jobs)),
            "case_world(개정이 효력일 0시에 올라옴)": case_world,
            "case_world_without_deadline_clock": case_world_nodeadline,
            "late_world(개정이 효력일 14시에 올라옴)": late_world,
            "late_world_without_deadline_clock": late_world_nodeadline,
            "m1b_observed_editions": observed, "m1b_merged_causes": merged, "m1b_middle_revision_lost": m1b_lost,
            "unit2_criterion_by_world": crit, "v1_claim_holds": v1_claim,
        },
        "verdict": verdict(broken),
        "missing": [
            "단위 2 완료 기준(작업 1개, 10월 9일 기한)은 사례 재생이 사건 시각에 맞춰 폴링해서 나온 값이다. "
            "실제 시계에서는 기한 작업이 제때 따로 돌아 작업 수가 늘고, '그날 알던 것'은 폴링 위상에 따라 달라진다.",
            "개정이 기한 0시에 올라오는 세계에서는 기한 시계가 지연을 0으로 만들고, 끄면 한 주기 안에 쌓인 개정을 놓친다(유지되는 부분). "
            "개정이 기한 당일 낮에 올라오면 기한 0시 읽기는 옛 판을 보고 지나가 효과가 사라진다. 기한 뒤 읽기(T+24h)가 없다.",
            "공급자 층 감시는 첫 대체 뒤 사라진다. 새 관측으로 감시를 넘기는 규칙이 엔진에 없다.",
            "기한 없는 문서에서 한 폴링 주기 안에 개정이 둘 쌓이면 작업이 하나로 합쳐지고 현재 판만 읽어 가운데 판을 잃는다"
            "(discovery_ops 6절 연결 규칙 (5)와 _enqueue 합치기가 부딪힌다).",
        ],
    }


# ============================================================================ M2 대량
def corpus_vocab() -> Counter:
    c = Counter()
    for line in (DB / "fixtures" / "af-res-012" / "entries.jsonl").read_text(encoding="utf-8").splitlines():
        e = json.loads(line)
        c.update(eng.content_tokens(e["D-b"]["en"]))
    for line in (DB / "fixtures" / "af-res-012" / "queries.jsonl").read_text(encoding="utf-8").splitlines():
        c.update(eng.content_tokens(json.loads(line)["en"]))
    return c


def bulk_commons(L, n: int, rnd: random.Random, vocab: Counter, at="2026-11-01T00:00:00Z"):
    words, weights = zip(*vocab.most_common())
    slots = ["input", "output", "user_without", "keeps", "breaks_when", "summary"]
    with L.db:
        for i in range(n):
            url = f"https://noise.example/{i}"
            L.db.execute("INSERT INTO locator(url, first_seen_at, first_seen_via) VALUES (?,?,?)", (url, at, "collection"))
            loc = L.db.execute("SELECT last_insert_rowid()").fetchone()[0]
            L.db.execute("INSERT INTO edition(locator_id, edition_key, kind, first_seen_at) VALUES (?,?,?,?)",
                         (loc, "v1", "release", at))
            ed = L.db.execute("SELECT last_insert_rowid()").fetchone()[0]
            L.db.execute("INSERT INTO observation(edition_id, position, observed_at, method, outcome, statement, idem_key)"
                         " VALUES (?,?,?,?,?,?,?)", (ed, "§1", at, "intro_only", "content", "noise", f"noise{i}"))
            oid = L.db.execute("SELECT last_insert_rowid()").fetchone()[0]
            for s in rnd.sample(slots, 3):
                text = " ".join(rnd.choices(words, weights=weights, k=rnd.randint(6, 14)))
                L.db.execute("INSERT INTO tag(obs_id, slot, height, lang, text, written_from) VALUES (?,?,?,?,?,?)",
                             (oid, s, "concrete", "en", text, "source_quote"))


def m2() -> dict:
    vocab = corpus_vocab()
    rnd = random.Random(20261126)
    sizes = [0, 1000, 5000, 20000]
    elig, rows = {}, {}
    for n in sizes:
        L = eng.Ledger()
        cases.preload_catalog(L)
        bulk_commons(L, n, rnd, vocab)
        p = L.project("A")
        req = L.intake(p, request_key="R1", rev=1, at="2026-11-26T01:00:00Z", text="r1", selected_part="s",
                       requirements=[], needs=cases.R1_NEEDS)
        t1 = time.perf_counter()
        hits = L.search_drawer(p, req, "2026-11-26T01:00:00Z", k=10 ** 9, log=False)
        dt = time.perf_counter() - t1
        e = [h for h in hits if h["eligible"]]
        noise = [h for h in e if L.obs(h["obs_id"])["url"].startswith("https://noise.example/")]
        top10_noise = sum(1 for h in hits[:10] if L.obs(h["obs_id"])["url"].startswith("https://noise.example/"))
        q_rank = next((i for i, h in enumerate(hits, 1) if "asyncio-queue" in L.obs(h["obs_id"])["url"]), None)
        elig[str(n)] = {"eligible": len(e), "eligible_noise": len(noise), "noise_in_top10": top10_noise,
                        "asyncio_queue_rank": q_rank}
        # 서랍이 훑은 꼬리표 행 수(칸별 MATCH 결과의 합)
        scanned = 0
        for nd in cases.R1_NEEDS:
            toks = eng.content_tokens(nd["text"])
            q = " OR ".join(f'"{t}"' for t in toks)
            scanned += L.db.execute("SELECT count(*) FROM tag_fts WHERE tag_fts MATCH ?", (q,)).fetchone()[0]
        rows[str(n)] = scanned
        PERF.append(f"M2 search_drawer commons+{n}: {dt:.3f}s, scanned tag rows {scanned}")
        L.db.close()

    # 사생활 검사: 꼬리표 하나를 쓸 때 읽는 비공개 요청판 행 수와 시간.
    # 실행 예제는 프로젝트 장부를 ATTACH로 붙이므로 SQLite 기본 한도(붙인 DB 10개)를 넘으면 프로젝트를 더 열 수 없다.
    qs = [json.loads(l) for l in (DB / "fixtures" / "af-res-012" / "queries.jsonl").read_text(encoding="utf-8").splitlines()]
    lint = {}
    attach_limit = None
    L, o = small_ledger()
    for i in range(12):
        try:
            L.project(f"p{i}")
        except sqlite3.OperationalError:
            attach_limit = i
            break
    L.db.close()
    for revs in (2, 20, 200):
        L, o = small_ledger()
        for i in range(9):
            pp = L.project(f"p{i}")
            for r in range(1, revs + 1):
                L.intake(pp, request_key="K", rev=r, at="2026-11-26T00:00:00Z", text=qs[(i + r) % len(qs)]["ko"] + f" #{r}",
                         selected_part="s", requirements=[])
        t1 = time.perf_counter()
        L.tag(o, "summary", "one_up", "en", "export is supported")
        PERF.append(f"M2 privacy lint with 9 projects x {revs} revisions: {time.perf_counter() - t1:.4f}s per tag")
        lint[f"9x{revs}"] = {"request_rows_read_per_tag": 9 * revs}
        L.db.close()

    # 전파: 호출마다 지금까지의 대체 전부를 다시 훑는다
    prop = {}
    for nsup in (100, 1000, 5000):
        L, o = small_ledger()
        p = L.project("A")
        req = L.intake(p, request_key="R", rev=1, at="2026-11-26T00:00:00Z", text="t", selected_part="s", requirements=[])
        L.compose(p, req, "2026-11-26T00:00:00Z", slots=[{"kind": "direct", "first": o, "ladder": "L2", "verb": "v",
                                                          "where": "§1", "reason": "r", "hold": "h"}])
        with L.db:
            for i in range(nsup):
                a, _ = L.observe(url=f"https://x.example/{i}", edition_key="v1", edition_kind="release", position="§",
                                 at="2026-11-26T00:00:00Z", method="read_line", quote=f"a{i}", statement="a")
                b, _ = L.observe(url=f"https://x.example/{i}", edition_key="v2", edition_kind="release", position="§",
                                 at="2026-11-27T00:00:00Z", method="read_line", quote=f"b{i}", statement="b")
                L.supersede(a, b, "changes_value", "2026-11-27T00:00:00Z")
        t1 = time.perf_counter()
        L.propagate(p, "2026-12-01T00:00:00Z")
        L.propagate(p, "2026-12-02T00:00:00Z")
        PERF.append(f"M2 propagate with {nsup} supersessions: {(time.perf_counter() - t1) / 2:.3f}s per call")
        prop[str(nsup)] = {"supersessions_rescanned_per_call": nsup}
        L.db.close()

    grows = elig[str(sizes[-1])]["eligible_noise"] > 0 and elig[str(sizes[-1])]["noise_in_top10"] > 0
    return {
        "id": "M2", "title": "대량: 장부와 프로젝트가 늘 때",
        "claim": "04 4절 서랍 자격(두 칸·서로 다른 내용어 둘)이 우연을 막는다. 2.1 규칙 3 사생활 검사. 6절 전파",
        "setup": "012 자료집 156항목에 같은 분야 어휘로 만든 무관한 관측 0/1k/5k/20k개(꼬리표 셋씩)를 더하고 R1 필요 문장으로 서랍을 돌린다",
        "observed": {"drawer_by_commons_size": elig, "drawer_tag_rows_scanned": rows,
                     "privacy_lint": lint, "projects_attachable_in_one_connection": attach_limit,
                     "propagate": prop},
        "verdict": verdict(grows),
        "missing": [
            "자격 규칙은 장부 크기와 무관한 고정 문턱이라, 같은 분야의 무관한 관측이 늘면 자격 있는 잡음도 선형으로 는다. "
            "상위 10에 잡음이 들어오고 정답 관측의 순위가 밀린다. 꼬리표 길이·희귀도로 정규화하는 규칙이 없다.",
            "사생활 검사는 꼬리표 하나를 쓸 때마다 모든 프로젝트 장부의 모든 요청판을 읽는다. "
            "공용 쓰기 경로가 모든 비공개 장부를 읽어야 해 '그 프로젝트만 읽는다'(2.1)와 C9 권한 경계에 어긋난다.",
            "전파는 호출마다 대체 전체를 다시 훑는다. 커서(마지막으로 전파한 대체)가 없다.",
            "서랍 질의에 상한(LIMIT)이 없어 흔한 낱말 하나가 장부 전체를 끌어온다.",
            "실행 예제는 프로젝트 장부를 한 연결에 ATTACH로 붙여 SQLite 기본 한도 때문에 프로젝트 10개를 넘기지 못한다. "
            "공용 꼬리표 쓰기가 모든 프로젝트 요청판을 읽는 구조와 함께 제품 저장소에서 다시 정해야 한다.",
        ],
    }


def small_ledger():
    L = eng.Ledger()
    o, _ = L.observe(url="https://example.org/doc", edition_key="v1", edition_kind="release", position="§1",
                     at="2026-11-26T00:00:00Z", method="read_line", quote="Export is supported.", quote_lang="en",
                     statement="내보내기를 지원한다.")
    return L, o


def m2b() -> dict:
    """사례가 실제로 쓴 꼬리표가, 같은 분야 프로젝트가 늘수록 사생활 검사에 걸리기 시작하는가."""
    L = eng.Ledger()
    catalog = cases.preload_catalog(L)
    cases.case_a(L, catalog)
    cases.case_b(L)
    cases.case_r2(L)
    qe, qj = quote_sql(L)
    authored = L.db.execute(
        f"SELECT t.obs_id, t.slot, t.text, {qe}, o.statement FROM tag t JOIN observation o USING(obs_id){qj}"
        " WHERE t.written_from <> 'catalog_description' AND t.lang='en' ORDER BY t.tag_id").fetchall()
    authored = [dict(r) for r in authored]
    L.db.close()
    qs = [json.loads(l) for l in (DB / "fixtures" / "af-res-012" / "queries.jsonl").read_text(encoding="utf-8").splitlines()]
    curve = {}
    for P_ in (0, 6, 12, 24, 36):
        L2 = eng.Ledger()
        ids = []
        for i, a in enumerate(authored):
            o, _ = L2.observe(url=f"https://src.example/{i}", edition_key="v1", edition_kind="release", position="§",
                              at="2026-11-26T00:00:00Z", method="read_line" if a["quote"] else "intro_only",
                              quote=a["quote"], quote_lang="en", statement=a["statement"])
            ids.append(o)
        pp = L2.project("others")    # 검사는 어느 장부든 모든 요청판을 같은 방식으로 읽으므로 한 장부에 모은다(ATTACH 한도)
        for i in range(P_):
            L2.intake(pp, request_key=f"Q{i}", rev=1, at="2026-11-26T00:00:00Z", text=qs[i]["en"], selected_part="s",
                      requirements=[])
        rejected = []
        for o, a in zip(ids, authored):
            try:
                L2._privacy_lint(o, a["text"])
            except eng.PrivacyError:
                rejected.append(a["text"])
        curve[str(P_)] = {"rejected": len(rejected), "of": len(authored), "examples": rejected[:3]}
        L2.db.close()
    # 한국어로 요청 문장을 그대로 옮긴 공개 꼬리표, 오류 문장이 다른 프로젝트 말을 드러내는가
    L3, o = small_ledger()
    pa = L3.project("A")
    r1ko = cases.p03w()["ko"]
    L3.intake(pa, request_key="R1", rev=1, at="2026-11-26T00:00:00Z", text=r1ko, selected_part="s", requirements=[])
    ko_copy = r1ko.split("\n")[0][:80]
    try:
        L3.tag(o, "summary", "one_up", "ko", ko_copy)
        ko_passed = True
    except eng.PrivacyError:
        ko_passed = False
    L3.intake(pa, request_key="R9", rev=1, at="2026-11-26T00:00:00Z",
              text="auditor handover of confidential conversation transcripts", selected_part="s", requirements=[])
    try:
        L3.tag(o, "summary", "one_up", "en", "export confidential conversation transcripts")
        msg = ""
    except eng.PrivacyError as e:
        msg = str(e)
    L3.db.close()
    leak_in_msg = ("confidential" in msg) or ("p_A" in msg)
    fp = curve["36"]["rejected"] > curve["0"]["rejected"]
    return {
        "id": "M2b", "title": "사생활 검사의 오탐과 누락",
        "claim": "04 2.1 규칙 3: 요청에만 있는 다섯 글자 이상 내용어가 둘 이상이면 공개 꼬리표 쓰기를 거절한다",
        "setup": "사례 셋이 원문 쪽 말로 쓴 영어 꼬리표 전부를 같은 원문 인용과 함께 다시 쓰면서, 012의 같은 분야 질의 36개를 프로젝트 요청으로 하나씩 늘린다",
        "observed": {"authored_tags_rejected_by_projects": curve, "korean_copy_of_request_passed": ko_passed,
                     "error_message": msg, "error_reveals_other_project": leak_in_msg},
        "verdict": verdict(fp or ko_passed or leak_in_msg),
        "missing": [
            "검사가 영문 낱말만 본다(tokens가 [0-9a-z]만 남긴다). 한국어·일본어로 요청을 옮겨 적은 꼬리표는 통과한다.",
            "다른 프로젝트 요청에 같은 분야 낱말이 있으면 원문 쪽 꼬리표도 거절된다. 프로젝트가 늘수록 오탐이 는다.",
            "꼬리표만 검사한다. 관측 문장, 대비 조건과 값, 영수증 입력은 검사하지 않는다(M7c).",
            "거절 문장이 다른 프로젝트의 별칭과 낱말을 그대로 담아, 거절 자체가 비공개 내용을 다른 쓰기 경로에 흘린다.",
        ],
    }


# ============================================================================ 예산 모형(M3, decide_sim D11이 같이 쓴다)
BUDGET_POLICIES = ["A 한 묶음, 폴링 먼저(v1 해석)", "B 한 묶음, 요청 먼저", "C 시계별(폴링은 조건부 요청)",
                   "D 시계별 + 후속 몫을 출처 10개당 168시간 3회"]


def budget_model(policy, C, lam, weeks=12, seed=11, budget=24, p_change=0.05, request_cap=4, follow_per_10=3,
                 deadline_every_h=None, deadline_mode="follow") -> dict:
    """출처 C개, 주간 요청 lam건을 weeks주 돌린다. 출처 절반은 72시간·절반은 168시간 주기로 폴링하고, 폴링마다
    p_change 확률로 바뀐 것을 봐 후속 읽기 1회를 만든다. 요청은 새 원문 2회와 관문이 닫히면 재열람 1회를 쓴다.
    한 묶음(A·B)은 168시간당 budget회를 모두가 나눠 쓰고, 시계별(C·D)은 요청당 request_cap회, 후속은 168시간당
    follow_per_10회(D는 출처 10개마다 그만큼), 배경 폴링은 조건부 요청이라 읽기 예산 밖이다[가정, 07 R-2].
    deadline_every_h가 있으면 출처마다 평균 그 간격으로 기한이 오고(D4), 기한마다 T-24h·T·T+24h에 직접 읽는다.
    deadline_mode="follow"는 기한 읽기가 후속 몫(한 묶음이면 그 묶음)을 함께 쓰고, "separate"는 기한마다 3회를
    따로 센다(08 I22). 후속 읽기와 기한 읽기는 예정 시각 순으로 몫을 받는다. 없으면 결과는 예전과 바이트까지 같다."""
    rnd = random.Random(seed + C * 7 + lam)
    per_clock = policy[0] in "CD"
    H = weeks * 168
    period = [72 if i % 2 == 0 else 168 for i in range(C)]
    next_due = [rnd.randrange(period[i]) for i in range(C)]
    last_poll, last_direct = [None] * C, [None] * C
    spent: list[int] = []
    follow = []           # 바뀐 것을 본 출처(후속 읽기 대기)
    follow_spent: list[int] = []
    pending = []
    arrivals = sorted((int(rnd.uniform(0, H)), rnd.randrange(C)) for _ in range(int(lam * weeks)))
    dl_reads = []         # (예정 시각, 출처) 기한 읽기. 따로 쓰는 난수라 기한이 없을 때의 흐름을 바꾸지 않는다
    if deadline_every_h:
        rd = random.Random(seed * 31 + C * 7 + lam + 1)
        for i in range(C):
            t = rd.expovariate(1 / deadline_every_h)
            while t < H:
                dl_reads.extend((int(t) + off, i) for off in (-24, 0, 24) if 0 <= int(t) + off < H)
                t += rd.expovariate(1 / deadline_every_h)
        dl_reads.sort()
    di = 0
    dl_queue: list = []
    dl_delay: list[int] = []
    follow_lag: list[int] = []
    ai = 0
    st = Counter()
    cursor_age = []
    for h in range(H):
        spent = [x for x in spent if x > h - 168]
        follow_spent = [x for x in follow_spent if x > h - 168]
        while ai < len(arrivals) and arrivals[ai][0] <= h:
            pending.append(arrivals[ai])
            ai += 1

        def do_requests():
            keep = []
            for (t0, src) in pending:
                fresh = last_poll[src] is not None and h - last_poll[src] <= 2 * period[src]
                direct = last_direct[src] is not None and h - last_direct[src] <= 168
                need = 2 + (0 if (fresh and direct) else 1)
                room = (budget - len(spent)) if not per_clock else request_cap
                if room >= need:
                    if not per_clock:
                        spent.extend([h] * need)
                    st["request_reads"] += need
                    st["done"] += 1
                    st["reopen"] += 0 if (fresh and direct) else 1
                    last_direct[src] = h
                    if h > t0:
                        st["deferred"] += 1
                elif h - t0 >= 72:
                    st["exhausted"] += 1
                else:
                    keep.append((t0, src))
            pending[:] = keep

        if policy == BUDGET_POLICIES[1]:
            do_requests()
        for i in range(C):
            if h >= next_due[i]:
                if per_clock or len(spent) < budget:
                    if not per_clock:
                        spent.append(h)
                    st["polls"] += 1
                    last_poll[i] = h
                    next_due[i] = h + period[i]
                    if rnd.random() < p_change:
                        follow.append((h, i))
                else:
                    st["poll_hours_deferred"] += 1
        if policy != BUDGET_POLICIES[1]:
            do_requests()
        while di < len(dl_reads) and dl_reads[di][0] <= h:
            dl_queue.append(dl_reads[di])
            di += 1
        keep_f, keep_d = [], []
        for kind, (due, i) in sorted([("f", x) for x in follow] + [("d", x) for x in dl_queue], key=lambda e: e[1][0]):
            if kind == "d" and deadline_mode == "separate":
                ok = True
            elif per_clock:
                cap = follow_per_10 if policy[0] == "C" else follow_per_10 * max(1, -(-C // 10))
                ok = len(follow_spent) < cap
                if ok:
                    follow_spent.append(h)
            else:
                ok = len(spent) < budget
                if ok:
                    spent.append(h)
            if ok:
                last_direct[i] = h
                if kind == "f":
                    st["follow_reads"] += 1
                    follow_lag.append(h - due)
                else:
                    st["deadline_reads"] += 1
                    dl_delay.append(h - due)
            elif kind == "f":
                keep_f.append((due, i))
                st["follow_hours_deferred"] += 1
            else:
                keep_d.append((due, i))
        follow, dl_queue = keep_f, keep_d
        if h % 24 == 0:
            cursor_age.append(max((h - lp) if lp is not None else h for lp in last_poll))
    n = max(1, st["done"] + st["exhausted"])
    return {"deferred_rate": round(st["deferred"] / n, 3), "exhausted_rate": round(st["exhausted"] / n, 3),
            "gate_reopen_rate": round(st["reopen"] / max(1, st["done"]), 3), "max_cursor_age_h": max(cursor_age),
            "source_reads_per_week": round((st["request_reads"] + st["follow_reads"]) / weeks, 1),
            "polls_per_week": round(st["polls"] / weeks, 1), "follow_hours_deferred": st["follow_hours_deferred"],
            **({} if not deadline_every_h else {
                "follow_lag_max_h": max(follow_lag, default=0), "deadline_reads_per_week": round(st["deadline_reads"] / weeks, 1),
                "deadline_read_delay_max_h": max(dl_delay, default=0),
                "deadline_reads_late": sum(1 for x in dl_delay if x > 0) + len(dl_queue),
                "all_reads_per_week": round((st["request_reads"] + st["follow_reads"] + st["deadline_reads"]) / weeks, 1)})}


# ============================================================================ M3 예산
def m3() -> dict:
    # (a) 세는 법 셋. 사례 A 첫 요청이 실제로 한 일에서 센다.
    L = eng.Ledger()
    catalog = cases.preload_catalog(L)
    a = cases.case_a(L, catalog)
    pA = "p_A"
    files = L.db.execute(
        "SELECT count(DISTINCT l.url) FROM observation o JOIN edition e USING(edition_id) JOIN locator l USING(locator_id)"
        " WHERE o.method='read_line' AND o.observed_at='2026-11-26T01:00:00Z'").fetchone()[0]
    execs = L.db.execute("SELECT count(DISTINCT receipt_id) FROM observation WHERE method='executed'"
                         " AND observed_at='2026-11-26T01:00:00Z'").fetchone()[0]
    engine_opens = a["opens_t0"]
    rules = {"04_5절(파일 수, 실행 따로)": files, "request_utility_6절(실패·재열람·실행 포함)": files + execs,
             "엔진 L.opens(새 관측 수)": engine_opens}
    k_fetch = "엔진 fetch_count(07 D1, 판독 어댑터가 적은 가져오기)"
    if hasattr(L, "fetched"):
        # 고친 엔진: 판독 어댑터가 하듯 T0에 받은 (주소, 판)마다 가져오기를 적고 엔진이 센다. 위치 수와 무관하다
        req1 = L.db.execute(f"SELECT min(req_id) FROM {pA}.request_rev").fetchone()[0]
        for url, ek in L.db.execute(
                "SELECT DISTINCT l.url, e.edition_key FROM observation o JOIN edition e USING(edition_id)"
                " JOIN locator l USING(locator_id) WHERE o.method='read_line' AND o.observed_at='2026-11-26T01:00:00Z'"
                " ORDER BY l.url").fetchall():
            L.fetched(url, ek, "2026-11-26T01:00:00Z", p=pA, req=req1)
        rules[k_fetch] = L.fetch_count(p=pA, req=req1)
        rules_checked = ["04_5절(파일 수, 실행 따로)", k_fetch]     # 07 D1 확정 뒤 예산이 세는 것은 이 둘이다
    else:
        rules_checked = list(rules)
    table = {}
    for b in (4, 3, 2, 1):
        table[str(b)] = {k: ("complete" if v <= b else "budget_exhausted") for k, v in rules.items()}
    c_gate = a["project_c_gate"]["decision"]
    c_counted = a["project_c_full_opens"]
    L.db.close()

    # (b) 출처가 늘 때 단일 예산(152 HIGH: 168시간당 24회)
    def budget_run(C, lam_week, weeks=12, seed=7):
        rnd = random.Random(seed + C * 101 + lam_week)
        H = weeks * 168
        period = [72 if i % 2 == 0 else 168 for i in range(C)]      # 절반은 인용된 출처(72), 절반은 무인용(168)
        next_due = [rnd.randrange(period[i]) for i in range(C)]
        last_poll = [None] * C
        last_direct = [None] * C
        spent: list[int] = []    # 예산을 쓴 시각(시)
        pending = []             # (도착 시각, 출처)
        arrivals = sorted(rnd.uniform(0, H) for _ in range(int(lam_week * weeks)))
        arrivals = [(int(x), rnd.randrange(C)) for x in arrivals]
        ai = 0
        stats = Counter()
        cursor_age = []
        for h in range(H):
            spent = [s_ for s_ in spent if s_ > h - 168]
            # 배경 폴링을 먼저 쓴다(discovery_ops 4절: 채널 차분은 지킨다). 예산이 없으면 다음 시각으로 미룬다.
            for i in range(C):
                if h >= next_due[i]:
                    if len(spent) < 24:
                        spent.append(h)
                        last_poll[i] = h
                        next_due[i] = h + period[i]
                        stats["polls"] += 1
                    else:
                        stats["poll_hours_deferred"] += 1
            while ai < len(arrivals) and arrivals[ai][0] <= h:
                pending.append(arrivals[ai])
                ai += 1
            keep = []
            for (t0, src) in pending:
                fresh = last_poll[src] is not None and h - last_poll[src] <= 2 * period[src]
                direct = last_direct[src] is not None and h - last_direct[src] <= 168
                need = 2 + (0 if (fresh and direct) else 1)       # 새 원문 2 + 재사용 관문이 닫히면 재열람 1
                if 24 - len(spent) >= need:
                    spent += [h] * need
                    stats["request_fetches"] += need
                    stats["requests_done"] += 1
                    stats["gate_reopen"] += 0 if (fresh and direct) else 1
                    last_direct[src] = h
                    if h > t0:
                        stats["requests_deferred"] += 1
                elif h - t0 >= 72:
                    stats["budget_exhausted"] += 1
                else:
                    keep.append((t0, src))
            pending = keep
            if h % 24 == 0:
                cursor_age.append(max((h - lp) if lp is not None else h for lp in last_poll))
        n = max(1, stats["requests_done"] + stats["budget_exhausted"])
        return {"requests": n, "deferred_rate": round(stats["requests_deferred"] / n, 3),
                "exhausted_rate": round(stats["budget_exhausted"] / n, 3),
                "gate_reopen_rate": round(stats["gate_reopen"] / max(1, stats["requests_done"]), 3),
                "background_share": round(stats["polls"] / max(1, stats["polls"] + stats["request_fetches"]), 3),
                "poll_hours_deferred": stats["poll_hours_deferred"], "max_cursor_age_h": max(cursor_age)}

    grid = {f"C{C}_req{lam}": budget_run(C, lam) for C in (3, 7, 10, 15, 30) for lam in (5, 20)}
    per_clock = None
    if hasattr(eng.Ledger, "REQUEST_FETCHES"):
        # 고친 엔진: 시계별 예산(07 D11). 엔진의 설정 값으로 같은 출처·요청 격자를 돌린다
        per_clock = {f"C{C}_req{lam}": budget_model(BUDGET_POLICIES[3], C, lam,
                                                     request_cap=eng.Ledger.REQUEST_FETCHES,
                                                     follow_per_10=eng.Ledger.FOLLOW_FETCHES_PER_10_SOURCES)
                     for C in (3, 7, 10, 15, 30) for lam in (5, 20)}
        collapse = [k for k, v in per_clock.items() if v["deferred_rate"] > 0.05 or v["exhausted_rate"] > 0]
    else:
        collapse = [k for k, v in grid.items() if v["deferred_rate"] > 0.05]
    contradiction = len(set(table["4"][k] for k in rules_checked)) > 1
    return {
        "id": "M3", "title": "열람 예산 축소",
        "claim": "04 5절·C1: 요청 하나에 원문 4회. 배경은 출처당 72시간마다 1회. 예산 단위는 152 HIGH(168시간당 24회). 보류율 5% 초과면 후속·배경 몫을 줄인다",
        "setup": "(a) 사례 A 첫 요청을 세 문서의 세는 법으로 센다. (b) 출처 C개·주간 요청 λ건을 12주 돌린다. 배경 폴링을 먼저 쓰고(채널 차분 보호), 요청은 새 원문 2회와 관문이 닫히면 재열람 1회를 쓴다",
        "observed": {"counting_rules_r1": rules, "status_by_budget_and_rule": table,
                     "rules_checked": rules_checked,
                     "project_c_gate": c_gate, "project_c_counted_opens": c_counted, "shared_budget_grid": grid,
                     **({"engine_per_clock_grid": per_clock} if per_clock is not None else {}),
                     "configs_over_5pct_deferral": collapse},
        "verdict": "모순" if contradiction else verdict(bool(collapse)),
        "missing": [
            "같은 R1이 세는 법에 따라 원문 2·3·8회다. 예산 4에서 complete인지 budget_exhausted인지가 문서마다 다르다.",
            "프로젝트 C는 재사용 관문이 reopen인데 엔진은 열람 0회로 센다. 다시 본 기록(sighting)을 열람으로 세지 않기 때문이다.",
            "배경 몫이 출처 수에 비례하는데 예산 단위는 고정이다. 출처가 약 7~10개를 넘으면 배경만으로 예산을 다 쓰고, "
            "요청이 밀리며, 커서가 늙어 재사용 관문이 닫히고, 다시 열람이 는다(되먹임).",
            "예산이 시스템 전체인지, 프로젝트·테넌트별인지, 출처별인지 정하지 않았다. 여러 프로젝트 사이 배분 규칙이 없다.",
            "엔진에 예산을 세고 멈추는 코드가 없다. 읽는 순서(retrieval_judgment 4절)도 엔진에 없다.",
        ],
    }


# ============================================================================ M4 이동·철회·잘못된 대체
def m4() -> dict:
    out = {}
    # (a) 별칭을 따라 만든 관측과 답: 별칭을 취소하면 닿는 자리를 찾을 수 있나
    L = eng.Ledger()
    p = L.project("A")
    t = "2026-11-26T00:00:00Z"
    old, new = "https://formulae.example/tree-sitter", "https://formulae.example/tree-sitter-cli"
    aid = L.alias(old, new, "moved", t)
    target = L.resolve(old, t)
    kw = {"via_alias": aid} if has_param(L.observe, "via_alias") else {}     # 07 D5: 따라 연 별칭을 남긴다
    o, _ = L.observe(url=target, edition_key="0.25.0", edition_kind="release", position="install", at=t,
                     method="read_line", quote="brew install tree-sitter-cli", quote_lang="en", statement="CLI 설치", **kw)
    req = L.intake(p, request_key="R", rev=1, at=t, text="t", selected_part="s", requirements=[], prior={"state": "none"})
    L.search_fresh(p, req, t, {"direct": [{"url": old}]})
    L.compose(p, req, t, slots=[{"kind": "direct", "first": o, "ladder": "L2", "verb": "설치", "where": "install",
                                 "reason": "r", "hold": "h"}])
    L.cancel_alias(aid, "2026-11-27T00:00:00Z", "이름은 같지만 다른 대상(023)")
    n = L.propagate(p, "2026-11-28T00:00:00Z")
    link_cols = [c for c in table_cols(L, "observation") + table_cols(L, "usage", "p_A") if "alias" in c]
    out["a_alias_cancel_notices"] = len(n)
    out["a_columns_linking_alias_to_obs"] = link_cols
    L.db.close()

    # (b) 공급자 철회(yank): 핀 형태에 따라 현재 추천이 갈리는가
    L = eng.Ledger()
    url = "https://pypi.org/pypi/pytest/8.1.0/json"
    o, _ = L.observe(url=url, edition_key="8.1.0", edition_kind="release", position="files", at=t, method="read_line",
                     quote="pytest-8.1.0-py3-none-any.whl", quote_lang="en", statement="8.1.0 배포 파일")
    L.channel("pypi", "https://pypi.org/rss/project/pytest/releases.xml", "yank_flag")
    L.watch(o, "https://pypi.org/rss/project/pytest/releases.xml", "8.1.0")
    runs = {}
    for name, pin in (("P_eq", "==8.1.0"), ("P_lt", "<8.1.1")):
        pp = L.project(name)
        rq = L.intake(pp, request_key="R", rev=1, at=t, text="t", selected_part="s", requirements=[],
                      context={"pin": {"value": pin, "provenance": "studio"}}, prior={"state": "none"})
        runs[name] = L.compose(pp, rq, t, slots=[{"kind": "direct", "first": o, "ladder": "L2", "verb": "v",
                                                   "where": "files", "reason": "r", "hold": "h"}])
    L.poll("https://pypi.org/rss/project/pytest/releases.xml", [{"id": "yank-8.1.0", "title": "8.1.0 yanked"}],
           "2026-11-27T00:00:00Z")
    j = L.jobs()[0]
    tok = L.lease(j["job_id"], "2026-11-27T01:00:00Z")
    y, _ = L.observe(url=url, edition_key="8.1.0", edition_kind="release", position="files", at="2026-11-27T00:00:00Z",
                     method="read_line", quote="yanked: true", quote_lang="en", statement="8.1.0 철회(yanked)")
    finish(L, j["job_id"], y, token=tok, sup=(o, "invalidates", "2026-11-27T00:00:00Z", None))
    texts = {name: [x["text"] for x in L.propagate(f"p_{name}", "2026-11-28T00:00:00Z")] for name in runs}
    schema_sql = (Path(eng.__file__).parent / "schema.sql").read_text(encoding="utf-8")
    obs_table = schema_sql[schema_sql.index("CREATE TABLE IF NOT EXISTS observation"):]
    outcome_enum = re.search(r"outcome\s+TEXT NOT NULL CHECK \(outcome IN \(([^)]*)\)", obs_table).group(1)
    out["b_notices_by_pin"] = texts
    out["b_same_notice_for_both_pins"] = texts["P_eq"] == texts["P_lt"]
    out["b_outcome_values"] = outcome_enum
    L.db.close()

    # (c) 잘못된 대체와 되돌리기(04 6.3: "반대 방향의 새 관측과 confirms 대체로 되돌린다")
    L = eng.Ledger()
    p = L.project("A")
    doc = "https://docs.example/export"
    A, _ = L.observe(url=doc, edition_key="rev:10", edition_kind="revision", position="Export", at=t, method="read_line",
                     quote="Export to JSON is available on all plans.", quote_lang="en", statement="모든 요금제에서 JSON 내보내기")
    L.channel("ex", doc + "/history", "revision_history")
    L.watch(A, doc + "/history")
    req = L.intake(p, request_key="R", rev=1, at=t, text="t", selected_part="s", requirements=[], prior={"state": "none"})
    L.compose(p, req, t, slots=[{"kind": "direct", "first": A, "ladder": "L2", "verb": "v", "where": "Export",
                                 "reason": "r", "hold": "h"}])
    # 판독 오류: 같은 판을 잘못 읽어 "내보내기 없음"이라 쓴다
    B, _ = L.observe(url=doc, edition_key="rev:10", edition_kind="revision", position="Export", at="2026-11-27T00:00:00Z",
                     method="read_line", quote="Export to JSON is unavailable.", quote_lang="en", statement="JSON 내보내기 없음")
    L.supersede(A, B, "invalidates", "2026-11-27T00:00:00Z")
    L.judge(p, req, "H1", B, "N", "direct", "L2", "잘못된 판독", "2026-11-27T00:00:00Z", cause="channel")
    # 그사이 채널에 진짜 변경이 올라온다
    L.poll(doc + "/history", [{"id": "11", "title": "rev 11"}], "2026-11-28T00:00:00Z")
    jobs_between = len(L.jobs())
    # 되돌리기: 바른 판독을 다시 쓰면 내용이 A와 같아 새 관측이 생기지 않는다
    C, created = L.observe(url=doc, edition_key="rev:10", edition_kind="revision", position="Export",
                           at="2026-11-29T00:00:00Z", method="read_line",
                           quote="Export to JSON is available on all plans.", quote_lang="en", statement="모든 요금제에서 JSON 내보내기")
    restored_by = None
    if hasattr(L, "cancel_supersession"):
        L.cancel_supersession(A, B, "2026-11-29T00:00:00Z", "판독 오류")
        restored_by = "cancel_supersession"
    else:
        try:
            L.supersede(B, C, "confirms", "2026-11-29T00:00:00Z")
            restored_by = "confirms(B→C)"
        except sqlite3.IntegrityError as e:
            restored_by = f"실패: {e}"
    cur = L.current(A, "2026-11-30T00:00:00Z")
    L.poll(doc + "/history", [{"id": "11", "title": "rev 11"}, {"id": "12", "title": "rev 12"}], "2026-11-30T00:00:00Z")
    jobs_after = [dict(r) for r in L.db.execute("SELECT obs_id, cause_ref FROM recheck_job ORDER BY job_id")]
    notes = [x["effect"] for x in L.propagate(p, "2026-11-30T00:00:00Z")]
    req2 = L.intake(p, request_key="R", rev=2, at="2026-11-30T00:00:00Z", text="t", selected_part="s", requirements=[])
    carried = L.carry_slips(p, req, req2, "2026-11-30T00:00:00Z", lambda o_, c_: True)
    wrong_slip_carried = any(L.db.execute(f"SELECT verdict FROM {p}.slip WHERE slip_id=?", (k,)).fetchone()[0] == "N"
                             for k in carried["kept"])
    out["c_corrected_obs_is_A_again"] = (C == A and not created)
    out["c_restore_method"] = restored_by
    out["c_current_of_A_after_restore"] = "A" if cur == A else ("B(잘못된 판독)" if cur == B else str(cur))
    out["c_jobs_created_while_wrongly_superseded"] = jobs_between
    out["c_jobs_after_restore"] = jobs_after
    out["c_notice_effects"] = notes
    out["c_wrong_slip_carried_to_next_revision"] = wrong_slip_carried
    L.db.close()

    broken = (out["a_alias_cancel_notices"] == 0) or out["c_current_of_A_after_restore"] != "A" or wrong_slip_carried
    return {
        "id": "M4", "title": "출처 이동·철회·잘못된 대체",
        "claim": "04 6.3: 별칭을 따라 만든 답 자리는 사용 쪽지로 찾아 알린다. 잘못된 대체는 반대 방향의 새 관측과 confirms로 되돌린다. "
                 "discovery_ops 3절: 공급자 철회는 핀 형태로 현재 추천이 갈린다",
        "setup": "(a) 별칭을 따라 연 관측으로 답한 뒤 별칭 취소 (b) 같은 판을 두 프로젝트가 ==8.1.0과 <8.1.1로 쓰다 철회 "
                 "(c) 같은 판을 잘못 읽어 invalidates를 쓰고 나중에 바로잡기",
        "observed": out,
        "verdict": verdict(broken),
        "missing": [
            "별칭과 관측·사용 쪽지를 잇는 열이 없다. 별칭을 취소해도 그 별칭을 따라 만든 자리를 찾을 길이 없다.",
            "공급자 철회를 나타낼 결과 값이 없고(outcome에 withdrawn 없음), 핀 형태를 담을 칸이 없어 두 프로젝트가 같은 '근거 무효'를 받는다.",
            "같은 판을 바로 읽으면 멱등 키가 원래 관측과 같아 '반대 방향의 새 관측'이 생기지 않는다. B→A confirms는 순환을 만들고 "
            "current(A)가 잘못된 판독 B에 머문다. 그동안 A의 감시는 꺼져 진짜 변경을 놓친다.",
            "잘못된 판독으로 쓴 쪽지(N)를 되돌리는 규칙이 없어 다음 요청판으로 그대로 옮겨진다.",
        ],
    }


# ============================================================================ M5 동시 변경
def m5() -> dict:
    out = {}
    t = "2026-11-26T00:00:00Z"
    # (a) 임차가 끝난 뒤 늦게 돌아온 작업자
    L, o = small_ledger()
    ch = "https://example.org/changes"
    L.channel("ex", ch, "changelog")
    L.watch(o, ch)
    L.poll(ch, [{"id": "1", "title": "v2"}], t)
    job = L.jobs()[0]["job_id"]
    tokA = L.lease(job, plus(t, 1))
    L.release_expired(plus(t, 2))
    tokB = L.lease(job, plus(t, 3))
    X, _ = L.observe(url="https://example.org/doc", edition_key="v2", edition_kind="release", position="§1",
                     at=plus(t, 2.5), method="read_line", quote="Export is read-only.", quote_lang="en", statement="읽기 전용")
    finish(L, job, X, token=tokB, sup=(o, "invalidates", plus(t, 2.5), None))
    Y, _ = L.observe(url="https://example.org/doc", edition_key="v1.9-cache", edition_kind="release", position="§1",
                     at=plus(t, 4), method="read_line", quote="Export is supported (cached).", quote_lang="en",
                     statement="캐시본")
    late = finish(L, job, Y, token=tokA, sup=(o, "changes_value", plus(t, 4), None))
    res = L.db.execute("SELECT result_obs FROM recheck_job WHERE job_id=?", (job,)).fetchone()[0]
    forks = L.db.execute("SELECT count(*) FROM supersession WHERE old_obs=?", (o,)).fetchone()[0]
    out["a_result_obs_after_late_finish"] = "X(새 작업자)" if res == X else ("Y(늦은 작업자)" if res == Y else str(res))
    out["a_supersession_forks"] = forks
    out["a_current"] = "X" if L.current(o, plus(t, 5)) == X else "Y"
    out["a_late_finish_return"] = late
    L.db.close()

    # (b) 임차 중 들어온 새 원인
    L, o = small_ledger()
    L.channel("ex", ch, "changelog", period_h=72)
    L.watch(o, ch)
    world = [("v1", t, "Export is supported."), ("v2", plus(t, 0.5), "Export is read-only."),
             ("v3", plus(t, 1.5), "Export is removed.")]

    def page(at_):
        return [w for w in world if w[1] <= at_][-1]

    L.poll(ch, [{"id": "v2", "title": "v2"}], plus(t, 1))
    j = L.jobs()[0]
    tok = L.lease(j["job_id"], plus(t, 4))
    ver, _eff, text = page(plus(t, 1))           # 작업자가 v2를 받아 왔다
    L.poll(ch, [{"id": "v2", "title": "v2"}, {"id": "v3", "title": "v3"}], plus(t, 2))   # 그사이 v3 항목
    n_open = L.db.execute("SELECT count(*) FROM recheck_job WHERE state IN ('queued','leased')").fetchone()[0]
    o2, _ = L.observe(url="https://example.org/doc", edition_key=ver, edition_kind="release", position="§1",
                      at=plus(t, 2.5), method="read_line", quote=text, quote_lang="en", statement=text)
    finish(L, j["job_id"], o2, token=tok, sup=(o, "invalidates", plus(t, 2.5), None))
    L.watch(o2, ch)
    first_v3 = None
    h = plus(t, 3)
    while h <= plus(t, 24 * 30):
        if hours(t, h) % 72 == 1:
            L.poll(ch, [{"id": "v2", "title": "v2"}, {"id": "v3", "title": "v3"}], h)
        for jj in L.jobs():
            tk = L.lease(jj["job_id"], plus(h, 1))
            vv, _e, tx = page(h)
            on, cr = L.observe(url="https://example.org/doc", edition_key=vv, edition_kind="release", position="§1",
                               at=h, method="read_line", quote=tx, quote_lang="en", statement=tx)
            finish(L, jj["job_id"], on, token=tk, sup=(L.current(jj["obs_id"], h), "invalidates", h, None) if cr else None)
            if vv == "v3" and first_v3 is None:
                first_v3 = h
        h = plus(h, 1)
    out["b_open_jobs_after_v3_item"] = n_open
    out["b_v3_first_observed_hours_after_item"] = round(hours(plus(t, 2), first_v3), 1) if first_v3 else None
    L.db.close()

    # (c) 판독 비결정성: 같은 판·같은 줄을 두 번 읽어 인용이 한 글자 다르다
    L = eng.Ledger()
    a1, _ = L.observe(url="https://docs.example/q", edition_key="v1", edition_kind="release", position="L10-12", at=t,
                      method="read_line", quote="put() blocks when the queue is full.", quote_lang="en", statement="가득 차면 기다린다")
    a2, _ = L.observe(url="https://docs.example/q", edition_key="v1", edition_kind="release", position="L10-12",
                      at=plus(t, 5), method="read_line", quote="put() blocks when the queue is full", quote_lang="en",
                      statement="가득 차면 기다린다")
    out["c_observations_same_edition_position"] = L.db.execute(
        "SELECT count(*) FROM observation o JOIN edition e USING(edition_id) WHERE e.edition_key='v1'").fetchone()[0]
    out["c_supersessions"] = L.db.execute("SELECT count(*) FROM supersession").fetchone()[0]
    out["c_reusable_returns"] = "두 번째" if reusable(L, "https://docs.example/q", "v1", "L10-12") == a2 else "첫 번째"
    L.db.close()

    broken = (out["a_supersession_forks"] > 1 or out["a_result_obs_after_late_finish"] != "X(새 작업자)"
              or out["b_v3_first_observed_hours_after_item"] is None)
    return {
        "id": "M5", "title": "동시 변경",
        "claim": "04 6.1: 임차로 두 작업자가 같은 재확인을 하지 않는다. 같은 관측의 새 원인은 열린 작업에 합친다",
        "setup": "(a) 작업자 A가 임차한 채 멈추고, 임차가 풀려 B가 끝낸 뒤 A가 돌아온다 (b) 작업자가 v2를 받아 온 뒤 끝내기 전에 v3 항목이 온다 "
                 "(c) 같은 판·같은 줄을 두 번 읽어 인용의 마침표 하나가 다르다",
        "observed": out,
        "verdict": verdict(broken),
        "missing": [
            "완료가 임차 표지를 확인하지 않는다. 늦은 작업자가 결과를 덮어쓰고, 같은 관측에서 대체가 두 갈래로 생겨 current가 늦은 쪽을 따른다.",
            "임차 중인 작업에 새 원인을 합치면, 작업자는 이미 받아 온 판으로 끝내고 새 원인은 읽히지 않은 채 끝난 것으로 남는다. "
            "다음 항목이나 기한이 올 때까지 v3를 모른다.",
            "같은 판·같은 위치에 서로 다른 관측이 둘 생겨도 충돌로 표시하지 않는다. 재사용은 나중 것을 고르고 앞 답은 앞 것을 인용한다. "
            "판독기 출력의 정규화와 충돌 규칙이 없다.",
        ],
    }


# ============================================================================ M6 다국어
def m6() -> dict:
    out = {}
    # (a) 일본어 꼬리표만 있는 ii-svn-log, (b) 한국어 필요 문장
    def r2_world(tags_lang: str):
        L = eng.Ledger()
        ii, _ = L.observe(url=cases.II_SVN, edition_key="fetch:2026-11-25", edition_kind="fetch", position="post",
                          at="2026-11-26T03:00:00Z", method="intro_only", statement=cases.II_SVN_READING, via="collection")
        if tags_lang == "en":
            L.tag(ii, "input", "concrete", "en", "a Subversion repository URL and its commit history", written_from="maker_statement")
            L.tag(ii, "output", "concrete", "en", "the commit history exported to one Excel file", written_from="maker_statement")
            L.tag(ii, "user_without", "concrete", "en", "people on a PC without Subversion can view and share the history",
                  written_from="maker_statement")
        else:
            L.tag(ii, "input", "concrete", "ja", "SVNリポジトリのURLとコミット履歴", written_from="maker_statement")
            L.tag(ii, "output", "concrete", "ja", "コミット履歴をExcelファイルに出力", written_from="maker_statement")
            L.tag(ii, "user_without", "concrete", "ja", "SVNのないPCで閲覧・共有できる", written_from="maker_statement")
        return L, ii

    en_needs = [{"slot": "input", "lang": "en", "text": "work records produced by our tool"},
                {"slot": "output", "lang": "en", "text": "the records exported as one standalone file the receiver can open"},
                {"slot": "user_without", "lang": "en", "text": "an auditor on a PC without our tool and without internet access"}]
    ko_needs = [{"slot": "input", "lang": "ko", "text": "우리 도구가 만든 작업 기록"},
                {"slot": "output", "lang": "ko", "text": "받는 사람이 열 수 있는 독립 파일 하나로 내보낸 기록"},
                {"slot": "user_without", "lang": "ko", "text": "우리 도구도 인터넷도 없는 PC의 감리자"}]
    for tl in ("en", "ja"):
        for nl, needs in (("en", en_needs), ("ko", ko_needs)):
            L, ii = r2_world(tl)
            p = L.project("B")
            req = L.intake(p, request_key="R2", rev=1, at="2027-03-02T00:00:00Z", text="r2", selected_part="s",
                           requirements=[], needs=needs)
            hits = L.search_drawer(p, req, "2027-03-02T00:00:00Z", k=5)
            out[f"tags_{tl}_needs_{nl}_found"] = any(h["obs_id"] == ii and h["eligible"] for h in hits)
            L.db.close()
    # (c) 자료집의 한국어 꼬리표 156개가 서랍에서 쓰일 수 있나
    L = eng.Ledger()
    cases.preload_catalog(L)
    ko_tags = [r[0] for r in L.db.execute("SELECT text FROM tag WHERE lang='ko'")]
    out["c_ko_catalog_tags"] = len(ko_tags)
    out["c_hangul_words_in_ko_tags"] = sum(len(re.findall(r"[가-힣]+", t)) for t in ko_tags)
    out["c_hangul_words_visible_to_drawer"] = sum(1 for t in ko_tags for w in eng.content_tokens(t)
                                                  if re.search(r"[가-힣]", w))
    out["c_ko_tags_with_any_drawer_token"] = sum(1 for t in ko_tags if eng.content_tokens(t))
    # (d) FTS5 unicode61이 일본어를 어떻게 자르나
    L.db.execute("CREATE VIRTUAL TABLE j USING fts5(text, tokenize='porter unicode61')")
    L.db.execute("INSERT INTO j(text) VALUES ('SVNのないPCで閲覧・共有できる')")
    out["d_fts_match_SVN"] = L.db.execute("SELECT count(*) FROM j WHERE j MATCH '\"SVN\"'").fetchone()[0]
    out["d_fts_match_閲覧"] = L.db.execute("SELECT count(*) FROM j WHERE j MATCH '\"閲覧\"'").fetchone()[0]
    L.db.close()
    broken = (not out["tags_en_needs_ko_found"]) or (not out["tags_ja_needs_en_found"])
    return {
        "id": "M6", "title": "다국어 신규 출처",
        "claim": "1.3 장면 2: 꼬리표는 원문 언어와 영어로 쓰고, 서랍이 칸으로 다른 언어 원문에 닿는다. retrieval_judgment 4절 (마) 규칙 ④",
        "setup": "ii-svn-log 꼬리표를 영어/일본어로, R2 필요 문장을 영어/한국어로 바꿔 네 조합으로 서랍을 돌린다",
        "observed": out,
        "verdict": verdict(broken),
        "missing": [
            "서랍과 사생활 검사가 쓰는 낱말 나누기(tokens)는 [0-9a-z]만 남긴다. 한국어·일본어 필요 문장과 꼬리표는 서랍에서 보이지 않는다. "
            "장면 2는 영어 꼬리표와 영어 필요 문장이 둘 다 있을 때만 성립한다.",
            "자료집 한국어 꼬리표는 들어 있는 영문 고유명사로만 맞는다. 한글 낱말은 하나도 서랍에 닿지 않는다.",
            "FTS5 unicode61은 일본어 문장을 띄어쓰기 없는 한 덩어리로 잘라 '閲覧' 같은 낱말로 찾을 수 없다.",
            "영어 필요 문장과 영어 꼬리표를 누가 어떻게 쓰는지(A4·B4)가 장면 2 전체의 전제다. 번역 품질을 재지 않았다.",
        ],
    }


# ============================================================================ M7 판단 오염
def m7() -> dict:
    out = {}
    # (a) 과다 꼬리표 하나가 서랍을 차지하는가
    vocab = corpus_vocab()
    top = [w for w, _ in vocab.most_common(60)]
    requests = {
        "R1": cases.R1_NEEDS, "X1": cases.X1_NEEDS,
        "W1": [{"slot": "summary", "lang": "en",
                "text": "keep our own copy of bookmarks held by an outside service so the copy remains if the service closes"},
               {"slot": "output", "lang": "en", "text": "a copy of every bookmark kept on our own server"}],
        "R2": [{"slot": "input", "lang": "en", "text": "work records produced by our tool"},
               {"slot": "output", "lang": "en", "text": "the records exported as one standalone file the receiver can open"},
               {"slot": "user_without", "lang": "en", "text": "an auditor on a PC without our tool and without internet access"},
               {"slot": "keeps", "lang": "en", "text": "the handed over files stay unchanged or the receiver can verify any change"}],
    }
    ranks = {}
    for name, needs in requests.items():
        L = eng.Ledger()
        cases.preload_catalog(L)
        spam, _ = L.observe(url="https://seo.example/best-tools", edition_key="fetch:1", edition_kind="fetch", position="page",
                            at="2026-11-01T00:00:00Z", method="intro_only", statement="도구 목록 페이지", via="collection")
        for s in ("input", "output", "user_without", "keeps", "breaks_when", "summary"):
            L.tag(spam, s, "one_up", "en", " ".join(top), written_from="catalog_description")
        p = L.project("Z")
        req = L.intake(p, request_key=name, rev=1, at="2027-01-01T00:00:00Z", text="z", selected_part="s",
                       requirements=[], needs=needs)
        hits = L.search_drawer(p, req, "2027-01-01T00:00:00Z", k=10)
        ranks[name] = next((h["rank"] for h in hits if h["obs_id"] == spam and h["eligible"]), None)
        L.db.close()
    out["a_keyword_stuffed_rank"] = ranks

    # (b) 판독기 오류 회수: 어느 관측이 문제 판독기의 것인가
    rnd = random.Random(3)
    L = eng.Ledger()
    truth = {}
    for d in range(90):
        for k in range(8):
            reader = rnd.choice(["reader-a@1", "reader-b@1", "reader-a@2" if 30 <= d < 38 else "reader-a@1"])
            bad = reader == "reader-a@2" and rnd.random() < 0.4
            at = S(P("2026-09-01T00:00:00Z") + timedelta(days=d, hours=k))
            kw = {"reader": reader} if has_param(L.observe, "reader") else {}
            o, _ = L.observe(url=f"https://r.example/{d}/{k}", edition_key="v1", edition_kind="release", position="§",
                             at=at, method="read_line", quote=f"q{d}-{k}", statement="s", **kw)
            truth[o] = (reader, bad)
    bad_ids = {o for o, (_r, b) in truth.items() if b}
    window = {r[0] for r in L.db.execute("SELECT obs_id FROM observation WHERE observed_at>=? AND observed_at<?",
                                         ("2026-10-01T00:00:00Z", "2026-10-09T00:00:00Z"))}
    if "reader" in table_cols(L, "observation"):
        by_reader = {r[0] for r in L.db.execute("SELECT obs_id FROM observation WHERE reader='reader-a@2'")}
    else:
        by_reader = None
    out["b_bad_observations"] = len(bad_ids)
    out["b_time_window_selected"] = len(window)
    out["b_time_window_precision"] = round(len(bad_ids & window) / max(1, len(window)), 3)
    out["b_reader_column"] = "reader" in table_cols(L, "observation")
    out["b_by_reader_selected"] = len(by_reader) if by_reader is not None else None
    out["b_by_reader_precision"] = round(len(bad_ids & by_reader) / max(1, len(by_reader)), 3) if by_reader else None
    L.db.close()

    # (c) 공개 장부에 남은 요청 수치(1.8: 조건 수치 R1의 8과 4는 비공개)
    L = eng.Ledger()
    catalog = cases.preload_catalog(L)
    cases.case_a(L, catalog)
    rec = [json.loads(r[0]) for r in L.db.execute("SELECT input_json FROM receipt")]
    contrast = [dict(r) for r in L.db.execute("SELECT condition, left_value, right_value FROM contrast")]
    stmt = [r[0] for r in L.db.execute("SELECT statement FROM observation WHERE method='executed'")]
    out["c_public_receipt_inputs"] = rec
    out["c_public_contrast_rows"] = contrast
    out["c_public_exec_statements_with_8_and_4"] = sum(1 for s in stmt if re.search(r"\b8\b", s) and re.search(r"\b4\b", s))
    L.db.close()

    # (d) 대체된 관측을 인용한 쪽지가 다음 요청판으로 옮겨지는가
    L, o = small_ledger()
    p = L.project("A")
    t = "2026-11-26T00:00:00Z"
    r1 = L.intake(p, request_key="R", rev=1, at=t, text="t", selected_part="s", requirements=[])
    L.judge(p, r1, "H1", o, "Y", "direct", "L2", "내보내기 지원", t)
    o2, _ = L.observe(url="https://example.org/doc", edition_key="v1", edition_kind="release", position="§1",
                      at="2026-11-27T00:00:00Z", method="read_line", quote="Export was removed.", quote_lang="en",
                      statement="내보내기 제거")
    L.supersede(o, o2, "invalidates", "2026-11-27T00:00:00Z")
    r2 = L.intake(p, request_key="R", rev=2, at="2026-11-28T00:00:00Z", text="t2", selected_part="s", requirements=[])
    kept = L.carry_slips(p, r1, r2, "2026-11-28T00:00:00Z", lambda ob, c: True)["kept"]
    out["d_slip_on_invalidated_obs_carried"] = len(kept) > 0
    L.db.close()

    # (e) 낡은 관측을 재사용해 답하면 철회 알림이 오지 않는다
    L = eng.Ledger()
    p, req, run0, pocket0, oai = setup_x1(L)
    kb1, _ = L.observe(url=cases.KB, edition_key="rev:300072", edition_kind="revision", position=POS_KB,
                       at="2025-07-09T00:00:00Z", method="read_line", quote="저장 종료", quote_lang="ko", statement="저장 종료")
    L.supersede(pocket0, kb1, "invalidates", "2025-07-09T00:00:00Z")
    w = L.project("W2")
    t2 = "2025-08-01T00:00:00Z"
    rq = L.intake(w, request_key="W", rev=1, at=t2, text="읽어 둘 링크 서비스", selected_part="s", requirements=[],
                  prior={"state": "none"})
    L.search_fresh(w, rq, t2, {"direct": [{"url": cases.POCKET_HOME}]})
    reused = reusable(L, cases.POCKET_HOME, "fetch:2025-05-15", "검색 결과 항목", at=t2)
    composed = None
    if reused:
        try:
            run = L.compose(w, rq, t2, slots=[{"kind": "check", "first": reused, "ladder": "L0", "verb": "Pocket",
                                               "reason": "API 절", "hold": "판독 전"}], status="partial")
            composed = "답함(낡은 관측 인용)"
        except ValueError as e:
            composed = f"거절: {e}"
    else:
        composed = "재사용 안 함(현재 관측으로 다시 확인)"
    notes = L.propagate(w, "2025-08-02T00:00:00Z")
    out["e_reused_superseded_obs"] = reused == pocket0
    out["e_compose"] = composed
    out["e_notices_to_new_answer"] = len(notes)
    L.db.close()

    stuffed_top = sum(1 for v in ranks.values() if v is not None and v <= 3)
    broken = (stuffed_top >= 2 or out["d_slip_on_invalidated_obs_carried"]
              or (out["e_reused_superseded_obs"] and composed.startswith("답함")))
    return {
        "id": "M7", "title": "판단 오염",
        "claim": "1.8 공개·비공개 경계, 04 2.1 규칙 3, 6.4 사실이 바뀔 때, 4절 재사용 조회",
        "setup": "(a) 낱말을 몰아 넣은 꼬리표 하나 (b) 8일 동안 오류율 40%인 판독기 판 (c) 사례 A의 공개 행 "
                 "(d) 무효가 된 관측의 쪽지 승계 (e) 대체된 Pocket 관측을 다른 프로젝트가 재사용",
        "observed": out,
        "verdict": verdict(broken),
        "missing": [
            "꼬리표의 품질·작성자·신뢰를 따지지 않는다. 흔한 내용어를 몰아 넣은 꼬리표 하나가 여러 요청의 서랍 상위를 차지한다.",
            "관측에 판독기(모델·프롬프트 판·사람) 칸이 없어, 잘못된 판독기의 관측을 골라 다시 확인할 수 없다. 시간 창으로 고르면 정밀도가 낮다.",
            "1.8은 조건 수치(8과 4)를 비공개로 두는데, 공개 영수증 입력·대비 값·실행 관측 문장에 그 수치가 그대로 있다. "
            "요청이 만든 실행과 대비를 공개로 둘지 비공개로 둘지 규칙이 없다.",
            "무효가 된 관측의 쪽지가 다음 요청판으로 옮겨진다(carry_slips가 대체를 보지 않는다).",
            "재사용 조회가 대체를 보지 않아, 대체된 관측으로 새 답을 만들 수 있다. 그 답은 대체를 안 뒤에 만들어져 전파에서도 빠진다(조용한 낡은 답).",
        ],
    }


# ============================================================================ M8 S로 줄이는 규칙
def m8() -> dict:
    L = eng.Ledger()
    catalog = cases.preload_catalog(L)
    cases.case_a(L, catalog)
    cases.case_b(L)
    cases.case_r2(L)
    rows = {}
    for p in L.projects:
        for (req, key) in L.db.execute(f"SELECT req_id, request_key FROM {p}.request_rev WHERE rev=1").fetchall():
            pl = L.path_log(p, req)
            runs = [r[0] for r in L.db.execute(f"SELECT run_id FROM {p}.answer_run WHERE req_id=?", (req,))]
            if not runs:
                continue
            used = set()
            for r in runs:
                used |= {L.obs(u[0])["url"] for u in L.db.execute(
                    f"SELECT obs_id FROM {p}.usage WHERE run_id=? AND part<>'contrast'", (r,))}
                used |= {f[0] for f in L.db.execute(f"SELECT url FROM {p}.folded WHERE run_id=?", (r,))}
            useful = [u for u in pl["drawer_only"] if u in used]
            rows[f"{p}:{key}"] = {"drawer_only_eligible": len(pl["drawer_only"]), "drawer_only_used_in_answer": len(useful),
                                  "fresh_only": len(pl["fresh_only"]), "both": len(pl["both"])}
            if hasattr(L, "drawer_contribution"):   # 고친 엔진: 04 7절의 새 지표를 엔진이 직접 낸다. 시뮬레이션 계산과 같아야 한다
                rows[f"{p}:{key}"]["engine_drawer_only_used"] = len(L.drawer_contribution(p, req)["drawer_only_used"])
    # 같은 대상이 두 주소로 남는가(같음 관계 없이 '같은 대상 중복 자리'를 셀 수 있나)
    q_locs = [r[0] for r in L.db.execute("SELECT url FROM locator WHERE url LIKE '%asyncio%queue%'")]
    L.db.close()
    noisy = [k for k, v in rows.items() if v["drawer_only_eligible"] > 0 and v["drawer_only_used_in_answer"] == 0]
    return {
        "id": "M8", "title": "S로 줄이는 규칙(C4)의 입력 지표",
        "claim": "04 7절: 서랍만 찾은 적격 후보 수가 두 분기 연속 0이면 꼬리표·대비 작성을 멈추고 S로 줄인다",
        "setup": "사례 셋의 요청마다 path_log의 서랍만 찾은 적격 후보와, 그중 답 자리나 접힌 목록에 실제로 오른 것을 센다",
        "observed": {"per_request": rows, "requests_with_eligible_but_unused_drawer_only": noisy,
                     "locators_for_asyncio_queue": q_locs},
        "verdict": verdict(bool(noisy)),
        "missing": [
            "적격 후보는 쓸모와 무관하게 거의 늘 1개 이상 나온다(R1은 10개 모두 답에 쓰이지 않았다). 이 지표로는 규칙이 사실상 걸리지 않는다. "
            "'서랍만 찾았고 답 자리·접힌 근접 대안에 오른 후보'로 바꿔야 서랍의 몫을 잰다.",
            "경로 비교를 주소 문자열로 해서, 같은 대상을 서랍은 저장소 주소로, 새 검색은 문서 사이트 주소로 찾으면 둘 다 '한쪽만'으로 센다.",
            "asyncio Queue 하나가 주소 둘(문서 사이트, 저장소)로 따로 있는데 둘을 잇는 관계가 없다. "
            "6.3의 재도입 조건 '같은 대상 중복 자리'는 같음 관계 없이는 셀 수 없다.",
        ],
    }


# ============================================================================ M9 시각 형식
def m9() -> dict:
    out = {}
    L, o = small_ledger()
    o2, _ = L.observe(url="https://example.org/other", edition_key="v1", edition_kind="release", position="§1",
                      at="2026-11-26T00:00:00Z", method="read_line", quote="Shutdown notice.", quote_lang="en", statement="종료 공지")
    L.channel("ex", "https://example.org/changes", "changelog")
    L.watch(o, "https://example.org/changes", "a", deadline="2026-12-01")            # 공지문에 흔한 날짜만 쓴 기한
    L.watch(o2, "https://example.org/changes", "b", deadline="2026-12-01T00:00:00Z")
    try:
        n = L.due("2026-12-01T00:00:00Z")
        out["a_due_result"] = n
        out["a_due_error"] = None
    except Exception as e:  # noqa: BLE001
        out["a_due_result"] = None
        out["a_due_error"] = type(e).__name__
    out["a_jobs_created"] = len(L.jobs())
    L.db.close()
    # 시간대 표기가 섞인 발행 시각
    L = eng.Ledger()
    for key, pub in (("fetch:a", "2025-11-11T21:54:00+09:00"), ("fetch:b", "2025-11-11T13:00:00Z")):
        L.observe(url=cases.II_SVN, edition_key=key, edition_kind="fetch", position="post", at="2026-11-26T00:00:00Z",
                  method="intro_only", statement=key, published_at=pub)
    out["b_latest_edition"] = L.latest_edition(cases.II_SVN, "2026-11-27T00:00:00Z")
    out["b_expected"] = "fetch:b"   # 21:54+09:00 = 12:54Z < 13:00Z
    L.db.close()
    broken = out["a_due_error"] is not None or out["a_jobs_created"] < 2 or out["b_latest_edition"] != out["b_expected"]
    return {
        "id": "M9", "title": "시각 형식",
        "claim": "04 3.3·discovery_ops 6절: 공지 기한 24시간 전과 기한(고친 엔진은 24시간 뒤도)에 직접 읽는다. 최신 판은 발행 시각으로 고른다",
        "setup": "(a) 날짜만 적은 기한 하나와 정상 기한 하나 (b) +09:00 표기 발행 시각과 Z 표기 발행 시각",
        "observed": out,
        "verdict": verdict(broken),
        "missing": [
            "기한 하나의 형식이 틀리면 due() 전체가 예외로 멈춰 다른 관측의 기한 작업도 만들어지지 않는다(시계 하나가 통째로 선다).",
            "시각을 문자열 그대로 비교한다. 시간대 표기가 섞이면 최신 판을 잘못 고른다. 저장 전에 UTC로 바꾸는 규칙이 없다.",
            "공지문에서 기한을 누가 어떤 정밀도(날짜, 현지 시각)로 뽑는지 정하지 않았다. 사례의 기한은 손으로 넣었다.",
        ],
    }


# ============================================================================ M10 보존과 삭제
def m10() -> dict:
    out = {}
    L, o = small_ledger()
    out["a_redaction_api"] = hasattr(L, "redact")
    if out["a_redaction_api"]:       # 고친 엔진(07 D7): 인용 본문만 지우고 지문·진술은 남긴다
        L.redact(obs_id=o, at="2026-11-27T00:00:00Z", reason="권리자 요청")
        row = L.obs(o)
        out["a_quote_erasable"] = row["quote"] is None and row["quote_fp"] is not None
    else:
        try:
            L.db.execute("UPDATE observation SET quote=NULL WHERE obs_id=?", (o,))
            out["a_quote_erasable"] = True
        except sqlite3.DatabaseError:
            out["a_quote_erasable"] = False
    p = L.project("A")
    priv = "https://github.com/acme-corp/internal-billing/blob/main/README.md"
    out["b_visibility_guard"] = has_param(L.observe, "visibility")   # 07 D6a: 요청 흐름이 공개 여부를 넘긴다
    kw = {"visibility": "private"} if out["b_visibility_guard"] else {}
    try:
        L.observe(url=priv, edition_key="main@abc123", edition_kind="commit", position="L1-20", at="2026-11-26T00:00:00Z",
                  method="read_line", quote="Internal billing service.", quote_lang="en", statement="내부 과금 서비스",
                  project=p, **kw)
        out["b_private_rejected"] = False
    except eng.PrivacyError:
        out["b_private_rejected"] = True
    out["b_private_url_in_commons"] = L.db.execute("SELECT count(*) FROM locator WHERE url=?", (priv,)).fetchone()[0] == 1
    L.db.close()
    L = eng.Ledger()
    catalog = cases.preload_catalog(L)
    cases.case_a(L, catalog)
    cases.case_b(L)
    cases.case_r2(L)
    out["c_request_originated_locators"] = L.db.execute(
        "SELECT count(*) FROM locator WHERE first_seen_via='request'").fetchone()[0]
    out["c_request_originated_with_time_of_day"] = L.db.execute(
        "SELECT count(*) FROM locator l WHERE first_seen_via='request' AND first_seen_at NOT LIKE '%T00:00:00Z'").fetchone()[0]
    L.db.close()
    broken = (not out["a_quote_erasable"] and not out["a_redaction_api"]) or out["b_private_url_in_commons"]
    return {
        "id": "M10", "title": "보존과 삭제",
        "claim": "discovery_ops 2절: 권리자가 요청하면 지운다, 묘비를 남긴다. 1.8: 요청 때 새로 읽은 공개 원문도 관측은 공개, 누가 왜 읽었는지는 남기지 않는다",
        "setup": "(a) 관측의 인용을 지우려 한다 (b) 요청 흐름이 사용자의 비공개 저장소 주소를 연다 (c) 사례 셋에서 요청이 처음 연 주소",
        "observed": out,
        "verdict": verdict(broken),
        "missing": [
            "관측은 트리거로 수정·삭제가 막혀 인용을 지울 길이 없다. 덧붙이기 원칙과 권리자 삭제·묘비가 부딪힌다. 인용 본문을 지울 수 있는 별도 저장으로 빼야 한다.",
            "'공개 원문'을 가리는 규칙이 없다. 요청 흐름이 연 비공개 주소(사용자의 저장소, 사내 문서)도 공용 장부에 들어간다.",
            "요청이 처음 연 주소의 첫 관측 시각이 초 단위로 공용에 남는다. 드문 주소라면 '누가 언제 무엇을 찾았나'를 거꾸로 짐작할 수 있다.",
        ],
    }


# ============================================================================ M11 알림 누적
def m11() -> dict:
    L, o = small_ledger()
    t = "2026-11-26T00:00:00Z"
    runs = 0
    latest = set()
    for i in range(8):
        p = L.project(f"P{i}")
        for rev in (1, 2, 3):
            rq = L.intake(p, request_key="R", rev=rev, at=plus(t, rev), text=f"t{rev}", selected_part="s", requirements=[])
            r = L.compose(p, rq, plus(t, rev), slots=[{"kind": "direct", "first": o, "ladder": "L2", "verb": f"v{rev}",
                                                       "where": "§1", "reason": "r", "hold": "h"}])
            runs += 1
            if rev == 3:
                latest.add((p, r))
    o2, _ = L.observe(url="https://example.org/doc", edition_key="v1", edition_kind="release", position="§1",
                      at=plus(t, 24), method="read_line", quote="Export is supported!", quote_lang="en", statement="같은 내용")
    L.supersede(o, o2, "confirms", plus(t, 24))
    total, on_old = 0, 0
    for p in L.projects:
        for n in L.propagate(p, plus(t, 25)):
            total += 1
            if (p, n["run"]) not in latest:
                on_old += 1
    cols = table_cols(L, "answer_run", "p_P0")
    held, delivered_old = 0, on_old
    if "held" in table_cols(L, "notice", "p_P0"):     # 고친 엔진(07 D2): 활성 답이 아닌 답의 알림은 쌓되 알리지 않는다
        delivered_old = 0
        for p in L.projects:
            for r in L.db.execute(f"SELECT run_id, held FROM {p}.notice").fetchall():
                if r["held"]:
                    held += 1
                elif (p, r["run_id"]) not in latest:
                    delivered_old += 1
    L.db.close()
    return {
        "id": "M11", "title": "알림 누적과 활성 답",
        "claim": "04 7절 '활성 답 항목'(재확인 큐 최고령), 3.3 알림",
        "setup": "프로젝트 8개가 같은 관측을 요청판 1·2·3에서 인용한 뒤, 그 관측에 '다시 확인됨' 대체가 하나 생긴다",
        "observed": {"answer_runs": runs, "notices": total, "notices_on_non_latest_revisions": on_old,
                     "held": held, "delivered_to_non_latest": delivered_old, "answer_run_columns": cols},
        "verdict": "빈칸" if delivered_old > 0 else "유지",
        "missing": [
            "'활성 답'의 정의와 칸이 없다. 새 요청판이 나온 옛 답에도 알림이 가고, 바뀐 것이 없는 '다시 확인됨'도 알림이 된다.",
            "알림의 읽음·묶음·우선순위가 없다. 인기 관측 하나가 바뀌면 모든 프로젝트의 모든 옛 답에 알림이 쌓인다.",
        ],
    }


# ============================================================================ M12 채널 ID 체계 변경
def m12() -> dict:
    out = {}
    L = eng.Ledger()
    ch = "https://feeds.example/releases"
    L.channel("ex", ch, "release_notes")
    obs = []
    for i in range(20):
        o, _ = L.observe(url=f"https://docs.example/p{i}", edition_key="v1", edition_kind="release", position="§",
                         at="2026-11-26T00:00:00Z", method="read_line", quote=f"q{i}", statement="s")
        L.watch(o, ch)
        obs.append(o)
    L.poll(ch, [{"id": f"a{i}", "title": f"release {i}"} for i in range(200)], "2026-11-26T00:00:00Z")
    for j in L.jobs():
        tk = L.lease(j["job_id"], "2026-11-26T01:00:00Z")
        finish(L, j["job_id"], j["obs_id"], token=tk)
    new = L.poll(ch, [{"id": f"b{i}", "title": f"release {i}"} for i in range(200)], "2026-11-29T00:00:00Z")
    out["a_new_items_after_id_scheme_change"] = len(new)
    out["a_jobs_created"] = len(L.jobs())
    out["a_merged_causes_per_job"] = max(len([c for c in j["merged_causes"].split(",") if c]) for j in L.jobs()) + 1 \
        if L.jobs() else 0
    out["a_operator_alert"] = bool(getattr(L, "alerts", None))
    L.db.close()
    L = eng.Ledger()
    L.channel("ex", ch, "release_notes")
    o, _ = L.observe(url="https://docs.example/p", edition_key="v1", edition_kind="release", position="§",
                     at="2026-11-26T00:00:00Z", method="read_line", quote="q", statement="s")
    L.watch(o, ch)
    try:
        L.poll(ch, [{"id": "x", "title": "x"}, {"id": "x", "title": "x (dup)"}], "2026-11-26T00:00:00Z")
        out["b_duplicate_id_poll"] = "ok"
    except sqlite3.IntegrityError:
        out["b_duplicate_id_poll"] = "IntegrityError"
    out["b_cursor_advanced"] = L.db.execute("SELECT last_polled_at FROM channel WHERE url=?", (ch,)).fetchone()[0] is not None
    L.db.close()
    broken = out["b_duplicate_id_poll"] != "ok" or (out["a_jobs_created"] > 0 and not out["a_operator_alert"])
    return {
        "id": "M12", "title": "채널 ID 체계 변경과 중복 ID",
        "claim": "discovery_ops 6절: 새 ID는 지금 집합에서 본 집합을 뺀 것. 표시일로 거르지 않는다",
        "setup": "(a) 감시 관측 20개가 걸린 채널이 항목 200개의 ID를 한꺼번에 바꾼다 (b) 목록에 같은 ID가 두 번 나온다",
        "observed": out,
        "verdict": verdict(broken),
        "missing": [
            "ID 체계가 바뀌면 모든 항목이 새것으로 보여, 감시 키가 빈 문자열인 관측 전부에 재확인 작업이 생긴다. 리셋을 알아채고 기준선만 다시 잡는 규칙이 없다.",
            "목록에 같은 ID가 두 번 나오면 폴링 거래 전체가 실패하고 커서가 앞으로 가지 않는다. 공급자가 고치지 않으면 그 채널은 계속 늙는다.",
        ],
    }


# ============================================================================ 실행
SCENARIOS = [m1, m2, m2b, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", default=str(DB))
    ap.add_argument("--out", default=str(HERE / "out" / "sim.json"))
    ap.add_argument("--perf", default=str(HERE / "out" / "perf.txt"))
    args = ap.parse_args()
    load(Path(args.engine).resolve())
    results = []
    for fn in SCENARIOS:
        t1 = time.perf_counter()
        r = fn()
        PERF.append(f"{r['id']} total {time.perf_counter() - t1:.2f}s")
        results.append(r)
        print(f"{r['id']:4} {r['verdict']:3}  {r['title']}")
    eng_dir = Path(args.engine).resolve()
    doc = {"engine": "docs/design/final/db" if eng_dir == DB.resolve() else "PR #9 첫 커밋 f1698015 고정판",
           "python": sys.version.split()[0],
           "note": "missing은 v1 고정판에서 찾은 빈칸을 적은 고정 문장이다. 고친 엔진에서 사라진 항목과 남은 항목은 "
                   "../07-review.md 3절 전후 표에 있다. verdict와 observed는 실행한 엔진의 값이다.",
           "results": results}
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(doc, ensure_ascii=False, indent=1, sort_keys=False) + "\n", encoding="utf-8")
    Path(args.perf).write_text("\n".join(PERF) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
