"""요청 시계 예산(07 D1·D11 그대로, 규칙 판 b1).

- 가져오기 = (주소, 판)의 원문을 네트워크에서 받은 횟수. 실패·재시도·관문 재열람(뒤집을 위치만 대조)도 1회다.
- 304(not_modified)는 기록만 하고 세지 않는다.
- 한 요청판 안에서 같은 (주소, 판)은 판독 어댑터가 캐시하므로 줄 범위를 여러 개 읽어도 1회다(캐시는 어댑터의 몫,
  셈은 fetch_log 행 수).
- 실행은 따로 센다(exec_log). 검색 호출은 가져오기가 아니라 외부 시도로 센다(call_log).
- 요청판마다 가져오기 REQUEST_FETCHES, 받은 바이트 REQUEST_BYTES, 외부 시도(가져오기+검색) REQUEST_EXTERNAL_ATTEMPTS.
  상수는 config.py에 있다.
- 예산이 바닥나면 남은 후보는 이유 "예산"과 함께 접힌 목록으로 보내고 답의 budget_json에 exhausted를 적는다.
"""
from __future__ import annotations

from . import config

RULES = config.BUDGET_RULES
REASON = "예산"


class BudgetExhausted(RuntimeError):
    def __init__(self, what: str, used: int, cap: int):
        super().__init__(f"request budget exhausted: {what} {used}/{cap}")
        self.what, self.used, self.cap = what, used, cap


class RequestBudget:
    def __init__(self, ledger, p: str, req: int):
        self.L, self.p, self.req = ledger, p, req

    def fetches(self) -> int:
        return self.L.fetch_count(p=self.p, req=self.req)

    def bytes(self) -> int:
        return self.L.db.execute(f"SELECT COALESCE(sum(bytes),0) FROM {self.p}.fetch_log WHERE req_id=?"
                                 " AND outcome<>'not_modified'", (self.req,)).fetchone()[0]

    def calls(self) -> int:
        return self.L.db.execute(f"SELECT count(*) FROM {self.p}.call_log WHERE req_id=?", (self.req,)).fetchone()[0]

    def external(self) -> int:
        return self.fetches() + self.calls()

    def check_fetch(self) -> None:
        if self.fetches() >= config.REQUEST_FETCHES:
            raise BudgetExhausted("fetches", self.fetches(), config.REQUEST_FETCHES)
        if self.bytes() >= config.REQUEST_BYTES:
            raise BudgetExhausted("bytes", self.bytes(), config.REQUEST_BYTES)
        self.check_external()

    def check_external(self) -> None:
        if self.external() >= config.REQUEST_EXTERNAL_ATTEMPTS:
            raise BudgetExhausted("external_attempts", self.external(), config.REQUEST_EXTERNAL_ATTEMPTS)

    def summary(self) -> dict:
        execs = self.L.db.execute(f"SELECT count(*) FROM {self.p}.exec_log WHERE req_id=?", (self.req,)).fetchone()[0]
        return {"rules": RULES, "fetches": self.fetches(), "fetch_cap": config.REQUEST_FETCHES,
                "bytes": self.bytes(), "byte_cap": config.REQUEST_BYTES,
                "search_calls": self.calls(), "external_attempts": self.external(),
                "external_cap": config.REQUEST_EXTERNAL_ATTEMPTS, "executions": execs}
