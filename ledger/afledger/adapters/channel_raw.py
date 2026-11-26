"""같은 주소 층 채널: 원문 파일 하나를 조건부 요청으로 폴링한다(둘째 구현 단위, 07 D11·R-2).

- If-None-Match(앞 응답의 ETag)로 묻는다. 304는 not_modified로 적고 읽기 예산에 넣지 않는다(07 D1).
  다만 304도 요청 1회의 비용은 든다(opensource catalog F14 #2: "The cost is one upstream request for an If-Match read").
- 200이면 새 항목을 만든다. 항목 ID는 ETag(없으면 본문 sha256)다. 외부 ID 집합의 차분으로 poll에 넘긴다.
- 의미 검증: 200이어도 본문이 비었거나 기대한 표지(expect)가 없으면 fetch_error로 적고 기준선(앞 ETag·항목)을 옮기지 않는다
  (F09 #25: "失敗を記録しながら、比較対象そのものは進めない").
"""
from __future__ import annotations

import hashlib


class ConditionalFileChannel:
    def __init__(self, ledger, transport, url: str, *, expect: str | None = None):
        self.L, self.t, self.url, self.expect = ledger, transport, url, expect
        self.etag: str | None = None
        self.items: list[dict] = []
        self.log: list[dict] = []

    def listing(self, at: str) -> list[dict]:
        headers = {"If-None-Match": self.etag} if self.etag else {}
        r = self.t.get(self.url, headers, note=f"conditional poll {self.url}")
        if r.status == 304:
            self.L.fetched(self.url, None, at, "not_modified", 0, clock="background")
            self.log.append({"at": at, "status": 304, "bytes": 0})
            return list(self.items)
        body = r.body
        ok = r.status == 200 and body and (self.expect is None or self.expect.encode() in body)
        self.L.fetched(self.url, None, at, "ok" if ok else ("not_found" if r.status == 404 else "unreachable"),
                       len(body), clock="background")
        self.log.append({"at": at, "status": r.status, "bytes": len(body), "accepted": bool(ok)})
        if not ok:
            return list(self.items)          # 기준선을 옮기지 않는다
        etag = r.headers.get("etag") or hashlib.sha256(body).hexdigest()
        if etag != self.etag:
            self.etag = etag
            self.items.append({"id": etag, "title": f"content {etag[:12]}", "url": self.url,
                               "edition": "sha256:" + hashlib.sha256(body).hexdigest()[:16]})
        return list(self.items)
