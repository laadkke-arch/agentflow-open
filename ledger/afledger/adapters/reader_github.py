"""판독 어댑터: GitHub 고정판의 줄 범위를 읽는다(06 3.1).

내는 것: 인용(줄 본문), 인용 지문(공백 정리 sha256), 위치(L36-L38), 앵커(ast 기호), 바이트 범위, 가져오기 수, 판독기 ID.
- 원문은 raw.githubusercontent.com/{repo}/{tag}/{path}에서 받는다. 답의 링크는 github.com/{repo}/blob/{tag}/{path}#L..이다(D10).
- 한 요청판 안에서 같은 (page, 판)은 캐시한다. 줄 범위를 여러 개 읽어도 가져오기 1회다(07 D1, budget.py).
- 가져오기마다 Ledger.fetched(clock="request")로 적는다. 실패(404·접속 실패)도 1회다.
- recheck(관문 재열람)는 관측의 바이트 범위만 Range로 받는다. 파일 전체를 다시 읽지 않는다. 그래도 가져오기 1회다.
- 진술(원문 쪽 한 줄)은 이 어댑터가 쓰지 않는다. 단위 1에서는 판독 계획(사람)이 준다(08 I6).
"""
from __future__ import annotations

from .. import locate, normalize
from ..budget import RequestBudget

READER_ID = "gh-pinned-lines/1"


class SourceUnavailable(RuntimeError):
    def __init__(self, url, status, outcome):
        super().__init__(f"{outcome}: {url} ({status})")
        self.url, self.status, self.outcome = url, status, outcome


def raw_url(repo: str, tag: str, path: str) -> str:
    return f"https://raw.githubusercontent.com/{repo}/{tag}/{path}"


def _outcome(status: int) -> str:
    return "ok" if status in (200, 206) else ("not_found" if status == 404 else "unreachable")


class GitHubPinnedReader:
    def __init__(self, ledger, transport, p: str, req: int, *, reader_id: str = READER_ID):
        self.L, self.t, self.p, self.req, self.reader_id = ledger, transport, p, req, reader_id
        self.cache: dict[tuple[str, str], str] = {}
        self.budget = RequestBudget(ledger, p, req)

    # ------------------------------------------------------------- 원문 받기
    def source(self, repo: str, tag: str, path: str, at: str) -> str:
        page = normalize.keys(normalize.pinned_blob(repo, path, tag))["page"]
        if (page, tag) in self.cache:
            return self.cache[(page, tag)]
        self.budget.check_fetch()
        r = self.t.get(raw_url(repo, tag, path), note=f"source {repo}@{tag}:{path}")
        oc = _outcome(r.status)
        self.L.fetched(normalize.pinned_blob(repo, path, tag), tag, at, oc, len(r.body), p=self.p, req=self.req)
        if oc != "ok":
            raise SourceUnavailable(raw_url(repo, tag, path), r.status, oc)
        text = r.text()
        self.cache[(page, tag)] = text
        return text

    # ------------------------------------------------------------- 위치 찾기와 판독
    def locate(self, text: str, *, lines=None, phrase=None, symbol=None, doc=True, start=None, end=None
               ) -> tuple[int, int] | None:
        """판독 계획이 준 단서로 줄 범위를 찾는다. 순서: 줄 번호 > 시작·끝 구절(기호 범위 안) > 구절 > 기호."""
        if lines:
            return tuple(lines)
        if start and end:
            syms = locate.symbols(text)
            lo, hi = syms[symbol]["range"] if symbol in syms else (1, len(text.splitlines()))
            body = locate.lines_text(text, lo, hi)
            a, b = locate.find_phrase(body, start), locate.find_phrase(body, end)
            if a and b and a[0] <= b[1]:
                return a[0] + lo - 1, b[1] + lo - 1
            return None
        if phrase:
            r = locate.find_phrase(text, phrase)
            if r:
                return r
        if symbol:
            s = locate.symbols(text).get(symbol)
            if s:
                return s["doc"] if doc and s["doc"] else s["range"]
        return None

    def read(self, repo: str, tag: str, path: str, at: str, *, lines=None, phrase=None, symbol=None,
             doc=True, start=None, end=None) -> dict:
        text = self.source(repo, tag, path, at)
        rng = self.locate(text, lines=lines, phrase=phrase, symbol=symbol, doc=doc, start=start, end=end)
        python = path.endswith(".py")
        base = {"repo": repo, "tag": tag, "path": path, "url": normalize.pinned_blob(repo, path, tag),
                "reader": self.reader_id}
        if not rng:
            return base | {"found": False, "symbol_present": (symbol in locate.symbols(text)) if (python and symbol) else None}
        a = locate.anchor(text, rng[0], rng[1], python=python)
        bs = locate.byte_span(text, *rng)
        return base | {"found": True, "lines": rng, "position": locate.position(*rng), "quote": a["quote"],
                       "quote_fp": a["quote_fp"], "symbol": a["symbol"], "in_doc": a["in_doc"],
                       "byte_span": f"{bs[0]}-{bs[1]}", "link": normalize.pinned_blob(repo, path, tag, rng)}

    def map_to(self, old_obs: int, repo: str, tag: str, path: str, at: str) -> dict:
        """앞 판 관측의 위치를 새 판에서 찾는다(07 R-1 임시안 m1). 정확한 인용 → 같은 기호 → 대응 없음."""
        o = self.L.obs(old_obs)
        text = self.source(repo, tag, path, at)
        python = path.endswith(".py")
        m = locate.map_position({"quote": o["quote"], "symbol": o["anchor_symbol"], "in_doc": bool(o["anchor_in_doc"])},
                                text, python=python)
        out = {"repo": repo, "tag": tag, "path": path, "url": normalize.pinned_blob(repo, path, tag),
               "reader": self.reader_id, "map": m, "from_obs": old_obs, "from_position": o["position"],
               "symbol": o["anchor_symbol"]}
        if m["lines"]:
            a = locate.anchor(text, *m["lines"], python=python)
            bs = locate.byte_span(text, *m["lines"])
            out |= {"found": True, "lines": m["lines"], "position": locate.position(*m["lines"]), "quote": a["quote"],
                    "quote_fp": a["quote_fp"], "in_doc": a["in_doc"], "byte_span": f"{bs[0]}-{bs[1]}",
                    "link": normalize.pinned_blob(repo, path, tag, m["lines"])}
        else:
            out |= {"found": False}
        return out

    # ------------------------------------------------------------- 관문 재열람
    def recheck(self, obs_id: int, at: str) -> dict:
        """재사용 관문이 reopen일 때 뒤집을 위치(관측의 바이트 범위)만 받아 인용 지문을 대조한다. 가져오기 1회."""
        o = self.L.obs(obs_id)
        k = normalize.keys(o["url"])
        repo = "/".join(k["target"][3:].split("/")[:2])
        path = k["position"].split("#")[0]
        tag = o["edition_key"]
        self.budget.check_fetch()
        r = self.t.get(raw_url(repo, tag, path), {"Range": f"bytes={o['byte_span']}"},
                       note=f"recheck obs {obs_id} {o['position']}")
        oc = _outcome(r.status)
        self.L.fetched(o["url"], tag, at, oc, len(r.body), p=self.p, req=self.req)
        if oc != "ok":
            return {"ok": False, "outcome": oc, "status": r.status}
        same = locate.quote_fp(r.text()) == o["quote_fp"]
        return {"ok": True, "status": r.status, "bytes": len(r.body), "same": same, "quote": r.text()}
