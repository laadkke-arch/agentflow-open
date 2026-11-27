"""배경·기한·후속 시계를 한 시간 단위로 돌리는 구동기(둘째 구현 단위, 04 1절·5절).

채널마다 주기(기본 72시간)와 위상(시작 뒤 첫 폴링까지의 시간)을 갖는다. 위상은 고정 씨앗의 난수로 정한다(06 3.4: 위상 무작위).
틱마다: 폴링할 채널은 목록을 받아 poll(외부 ID 차분)하고 배경 가져오기를 적는다(목록이 그대로면 not_modified, 예산 밖) →
due(기한 T-24h·T·T+24h) → 작업자 한 번 → 프로젝트마다 propagate. 목록 공급자(listing)는 바깥에서 준다(기록 재생 또는 실제 채널).
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

ISO = "%Y-%m-%dT%H:%M:%SZ"


def _t(s: str) -> datetime:
    return datetime.strptime(s, ISO).replace(tzinfo=timezone.utc)


class PollingClock:
    def __init__(self, ledger, worker, channels: dict, *, projects=(), step_h: int = 1):
        """channels: {채널 주소: {"listing": fn(at) -> list[dict], "period_h": 72, "phase_h": 0..period}}"""
        self.L, self.worker, self.channels, self.projects, self.step_h = ledger, worker, channels, list(projects), step_h
        self.polls: list[dict] = []
        self.notices: list[dict] = []
        self._last_ids: dict[str, tuple] = {}

    def due_poll(self, url: str, t: datetime, start: datetime) -> bool:
        c = self.channels[url]
        h = int((t - start).total_seconds() // 3600)
        return h >= c["phase_h"] and (h - c["phase_h"]) % c["period_h"] == 0

    def run(self, start: str, end: str) -> None:
        t0, t, t1 = _t(start), _t(start), _t(end)
        while t <= t1:
            at = t.strftime(ISO)
            for url, c in self.channels.items():
                if self.due_poll(url, t, t0):
                    listing = c["listing"](at)
                    ids = tuple(sorted(i["id"] for i in listing))
                    outcome = "not_modified" if self._last_ids.get(url) == ids else "ok"
                    self._last_ids[url] = ids
                    if not c.get("self_logging"):   # 조건부 채널 어댑터는 스스로 가져오기를 적는다
                        self.L.fetched(url, None, at, outcome, None, clock="background")
                    src = getattr(c["listing"], "__self__", None)   # 어댑터가 오류를 알리면 확인 커서를 옮기지 않는다(08 I35)
                    poll_outcome = c.get("outcome", lambda _at: getattr(src, "last_outcome", "ok"))(at)
                    new = self.L.poll(url, listing, at, outcome=poll_outcome)
                    self.polls.append({"at": at, "channel": url, "new": [i["id"] for i in new], "outcome": outcome,
                                       "poll_outcome": self.L.last_poll_outcome})
            self.L.due(at)
            self.worker.run_once(at)
            for p in self.projects:
                for n in self.L.propagate(p, at):
                    self.notices.append(n | {"project": p, "at": at})
            t += timedelta(hours=self.step_h)
