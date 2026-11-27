"""재확인 작업자(둘째 구현 단위, 04 3.8). 엔진의 저장 함수(lease, job_editions, observe, finish, supersede, watch)를 쓴다.

한 번의 작업:
  1. 후속 몫(follow_budget_left)이 0이면 잡지 않는다(작업은 대기로 남는다, 07 D11). config.DEADLINE_BUDGET="separate"면
     기한 원인만 가진 작업은 후속 몫을 쓰지 않고 clock="deadline"으로 센다(08 I22, 결정 I23으로 기본).
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
            causes = [j["cause"]] + [m.split(":", 1)[0] for m in j["merged_causes"].split(",") if m]
            if all(c == "audit" for c in causes):
                continue   # 감사 작업은 운영자 몫이다(판독 충돌 I21, 위치 대응 없음 I36). 작업자가 원문을 다시 읽지 않는다
            if j["not_before"] and j["not_before"] > at:
                continue   # 다시 하기를 기다리는 작업(08 I41)
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
        cur = base = L.current(old, at)
        if L.retracted(cur, at) is not None:
            # 철회된 판독에 걸린 작업(취소 전에 임차된 것). 읽지 않고 원인을 되살아난 관측으로 옮긴다(08 I37 규칙 1)
            ok = L.finish(j["job_id"], None, token=token, base=(old, base, at))
            rec = {"at": at, "job": j["job_id"], "obs": old, "result": L.last_finish or "same", "accepted": ok}
            self.log.append(rec)
            return rec
        editions = [e["edition_key"] for e in L.job_editions(j["job_id"])] or [None]
        readings, unmapped, failed, fail_info = [], [], [], []
        for ek in editions:
            r = self.reader(L.obs(cur), ek, at)
            outcome = (r or {}).get("outcome", "content") if r else "unreachable"
            env = bool((r or {}).get("env_suspect")) and outcome != "content"
            L.fetched((r or {}).get("url") or L.obs(cur)["url"], (r or {}).get("edition_key", ek), at,
                      "ok" if outcome == "content" else outcome, (r or {}).get("bytes"), clock=clock, job_id=j["job_id"],
                      env_suspect=env)
            if outcome != "content":
                # 실패도 관측이다(04 6.2, 08 I38 규칙 1). 대체 사슬에는 잇지 않는다(규칙 2)
                o = L.obs(cur)
                fid, _ = L.observe(url=o["url"], edition_key=ek or f"attempt@{at}",
                                   edition_kind=o["edition_kind"] if ek else "fetch", position=o["position"], at=at,
                                   method="read_line", outcome=outcome, statement=f"원문 접근 실패({outcome})",
                                   via="channel", reader=(r or {}).get("reader", self.name))
                failed.append(fid)
                fail_info.append((outcome, (r or {}).get("retry_after_h") or 0, env))
            elif r.get("unmapped"):
                unmapped.append(r)     # 그 판에 같은 자리가 없다. 거짓 위치로 관측을 만들지 않는다(08 I36)
            elif r:
                readings.append(r)
        readings.sort(key=lambda r: r.get("published_at") or "")
        chain, new_obs, reread = [], None, []
        for r in readings:
            oid, created = L.observe(url=r["url"], edition_key=r["edition_key"], edition_kind=r.get("edition_kind", "revision"),
                                     position=r["position"], at=at, method="read_line", quote=r["quote"],
                                     quote_lang=r.get("quote_lang"), statement=r["statement"], published_at=r.get("published_at"),
                                     flip_position=r.get("flip_position"), via="channel", reader=r.get("reader", self.name),
                                     evidence_ref=r.get("evidence_ref"), anchor_symbol=r.get("anchor_symbol"),
                                     anchor_in_doc=r.get("anchor_in_doc"), map_method=r.get("map_method"),
                                     map_from=r.get("map_from"), byte_span=r.get("byte_span"))
            if not created and oid != cur and L.retracted(oid, at) is not None:
                reread.append(oid)     # 운영자가 철회한 판독을 다시 읽었다. 취소는 그대로 두고 감사로 넘긴다(I37 규칙 2)
                continue
            prev_pub = L.obs(cur)["published_at"] or ""
            linkable = created or oid not in L.earlier_obs(cur, at)    # 이미 있는 관측도 잇는다(I37 규칙 3)
            if oid != cur and linkable and (r.get("published_at") or "") >= prev_pub:
                chain.append((cur, oid, self.judge(L.obs(cur), r), r))
                cur = oid
            new_obs = oid if created else new_obs
        if not chain:
            all_failed = bool(failed) and not readings and not unmapped
            transient = all_failed and all(o_ in config.RETRY_OUTCOMES for o_, _, _ in fail_info)
            env_attempt = all_failed and all(e for _, _, e in fail_info)
            tries = L.job_attempts(j["job_id"])
            if transient and (tries["env"] <= config.ENV_RETRY_MAX if env_attempt else tries["real"] <= config.RETRY_MAX):
                # 일시 실패: 같은 작업을 기다렸다 다시 한다(08 I41). 처음 시도 + RETRY_MAX회.
                # 환경 고장 의심 시도는 따로 ENV_RETRY_MAX회까지 세고 RETRY_MAX를 쓰지 않는다(08 I46 규칙 4)
                from .ledger import _shift
                wait = max(config.RETRY_WAIT_H, max(h for _, h, _ in fail_info))
                L.last_finish = None
                ok = L.retry(j["job_id"], token, _shift(at, wait))
                result = "retry_scheduled"
            elif env_attempt:
                ok = L.finish(j["job_id"], None, ok=False, token=token, base=(old, base, at))
                result = L.last_finish or "env_failed"
            else:
                ok = L.finish(j["job_id"], new_obs or cur, ok=not all_failed, token=token, base=(old, base, at))
                result = L.last_finish or ("failed" if all_failed else "unmapped" if unmapped and not readings else
                                           "retracted_reread" if reread else "same")
            rec = {"at": at, "job": j["job_id"], "obs": old, "result": result, "accepted": ok}
        else:
            a, b, effect, r = chain[-1]
            ok = L.finish(j["job_id"], b, token=token, supersede=(a, effect, at, r.get("effective_from")),
                          chain_before=[(a_, b_, e_, at, r_.get("effective_from")) for a_, b_, e_, r_ in chain[:-1]],
                          base=(old, base, at))
            if ok:
                for a_, b_, _e, r_ in chain:
                    for w in r_.get("watch", []):
                        L.watch(b_, w["channel"], w.get("match_key", ""), layer=w.get("layer", "same_address"),
                                deadline=w.get("deadline"))
            rec = {"at": at, "job": j["job_id"], "obs": old, "result": L.last_finish or "superseded",
                   "chain": [(a_, b_, e_) for a_, b_, e_, _ in chain], "accepted": ok}
        if ok and failed:
            rec["source_failure"] = L.note_source_failure(base, failed[-1], at)
            if any(e for _, _, e in fail_info) and not any(a["kind"] == "env_suspect" and a.get("job") == j["job_id"]
                                                          for a in L.alerts):
                L.alerts.append({"kind": "env_suspect", "job": j["job_id"], "obs": base, "at": at})
        if ok and (readings or unmapped) and L.last_finish != "base_moved":
            rec["source_recovery"] = L.note_source_recovery(L.current(old, at), at)   # 원문을 다시 읽었다(08 I44)
        if ok and (unmapped or reread):
            with L.db:
                for r in unmapped:
                    L._enqueue(base, "audit", f"unmapped:{r['edition_key']}", at)
                    L.alerts.append({"kind": "position_unmapped", "obs": base, "edition": r["edition_key"],
                                     "at": at, "symbol_present": r["map"].get("symbol_present")})
                for oid in reread:
                    L._enqueue(base, "audit", f"reread_retracted:{oid}", at)
                    L.alerts.append({"kind": "retracted_reread", "obs": base, "retracted": oid, "at": at})
        self.log.append(rec)
        return rec


def follow_cap(ledger) -> int:
    n = ledger.db.execute("SELECT count(*) FROM channel").fetchone()[0]
    return config.FOLLOW_FETCHES_PER_10_SOURCES * max(1, -(-n // 10))
