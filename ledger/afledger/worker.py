"""재확인 작업자(둘째 구현 단위, 04 3.8). 엔진의 저장 함수(lease, job_editions, observe, finish, supersede, watch)를 쓴다.

한 번의 작업:
  1. 후속 몫(follow_budget_left)이 0이면 잡지 않는다(작업은 대기로 남는다, 07 D11). config.DEADLINE_BUDGET="separate"면
     기한 원인만 가진 작업은 후속 몫을 쓰지 않고 clock="deadline"으로 센다(08 I22, 결정 전 선택지).
  2. lease로 임차 표지를 받는다. 0이면 다른 작업자가 잡았다.
  3. 읽을 판: job_editions(작업에 합쳐진 채널 항목의 판 키, 07 D3)가 있으면 발행 순으로 모두, 없으면 읽는 시각의 최신 판.
  4. 판마다 reader(관측, 판 키 또는 None, 시각)로 읽고 fetched(clock="follow")로 센다. 실패(None)도 1회다.
     observe(via="channel")로 남긴다. 같은 내용이면 다시 본 기록이 되고 대체는 없다.
  5. 새 관측이 생기면 judge(앞 관측, 읽은 것)로 효과(invalidates·changes_value·confirms)를 정한다. 발행이 현재 관측보다 늦은
     판만 대체 사슬에 잇는다. 마지막 대체는 finish(token=, supersede=)로 완료와 같은 거래에서, 그 앞의 대체는 임차를 다시 확인한 뒤 쓴다.
  6. 읽은 것이 감시(watch)를 말하면 새 관측에 단다(기한은 원문 내용이라 대체가 넘기지 않는다).
알림은 이 작업자가 보내지 않는다. 완료 뒤 propagate가 만든다(보내기 직전에 다시 확인, F09 #5 outbox 글과 같은 분리).
reader·judge는 바깥에서 준다. 단위 2의 첫 판은 기록된 개정 이력을 읽는 reader와 기록된 효과를 쓰는 judge(사람 판정)다.
"""
from __future__ import annotations

from . import config


class RecheckWorker:
    def __init__(self, ledger, reader, judge, *, lease_h: float = 1.0, name: str = "worker-1"):
        self.L, self.reader, self.judge, self.lease_h, self.name = ledger, reader, judge, lease_h, name
        self.log: list[dict] = []

    def _until(self, at: str) -> str:
        from .ledger import _shift
        return _shift(at, self.lease_h)

    def run_once(self, at: str) -> list[dict]:
        done = []
        for j in self.L.jobs("queued"):
            deadline_only = j["cause"] == "deadline" and not any(
                m.split(":", 1)[0] != "deadline" for m in j["merged_causes"].split(",") if m)
            separate = config.DEADLINE_BUDGET == "separate" and deadline_only
            if not separate and self.L.follow_budget_left(at) <= 0:
                self.log.append({"at": at, "job": j["job_id"], "skipped": "follow_budget"})
                break
            token = self.L.lease(j["job_id"], self._until(at))
            if not token:
                continue
            done.append(self._work(j, token, at, clock="deadline" if separate else "follow"))
        return done

    def _still_mine(self, job_id: int, token: int) -> bool:
        r = self.L.db.execute("SELECT state, attempts FROM recheck_job WHERE job_id=?", (job_id,)).fetchone()
        return r["state"] == "leased" and r["attempts"] == token

    def _work(self, j, token: int, at: str, clock: str = "follow") -> dict:
        L = self.L
        old = j["obs_id"]
        cur = L.current(old, at)
        editions = [e["edition_key"] for e in L.job_editions(j["job_id"])] or [None]
        readings = []
        for ek in editions:
            r = self.reader(L.obs(cur), ek, at)
            L.fetched((r or {}).get("url") or L.obs(cur)["url"], (r or {}).get("edition_key", ek), at,
                      "ok" if r else "unreachable", (r or {}).get("bytes"), clock=clock, job_id=j["job_id"])
            if r:
                readings.append(r)
        readings.sort(key=lambda r: r.get("published_at") or "")
        chain, new_obs = [], None
        for r in readings:
            oid, created = L.observe(url=r["url"], edition_key=r["edition_key"], edition_kind=r.get("edition_kind", "revision"),
                                     position=r["position"], at=at, method="read_line", quote=r["quote"],
                                     quote_lang=r.get("quote_lang"), statement=r["statement"], published_at=r.get("published_at"),
                                     flip_position=r.get("flip_position"), via="channel", reader=r.get("reader", self.name),
                                     evidence_ref=r.get("evidence_ref"))
            prev_pub = L.obs(cur)["published_at"] or ""
            if created and oid != cur and (r.get("published_at") or "") >= prev_pub:
                chain.append((cur, oid, self.judge(L.obs(cur), r), r))
                cur = oid
            new_obs = oid if created else new_obs
        if not chain:
            ok = L.finish(j["job_id"], new_obs or cur, token=token)
            rec = {"at": at, "job": j["job_id"], "obs": old, "result": "same", "accepted": ok}
            self.log.append(rec)
            return rec
        for a, b, effect, r in chain[:-1]:
            if not self._still_mine(j["job_id"], token):
                break
            L.supersede(a, b, effect, known_from=at, effective_from=r.get("effective_from"))
        a, b, effect, r = chain[-1]
        ok = L.finish(j["job_id"], b, token=token, supersede=(a, effect, at, r.get("effective_from")))
        if ok:
            for a_, b_, _e, r_ in chain:
                for w in r_.get("watch", []):
                    L.watch(b_, w["channel"], w.get("match_key", ""), layer=w.get("layer", "same_address"),
                            deadline=w.get("deadline"))
        rec = {"at": at, "job": j["job_id"], "obs": old, "result": "superseded", "chain": [(a_, b_, e_) for a_, b_, e_, _ in chain],
               "accepted": ok}
        self.log.append(rec)
        return rec


def follow_cap(ledger) -> int:
    n = ledger.db.execute("SELECT count(*) FROM channel").fetchone()[0]
    return config.FOLLOW_FETCHES_PER_10_SOURCES * max(1, -(-n // 10))
