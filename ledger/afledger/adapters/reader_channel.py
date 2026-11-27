"""작업자(후속 시계)용 고정판 코드 판독기(08 I36). 채널 항목이 준 새 판에서 앞 관측의 위치를 m1으로 찾는다.

m1(07 R-1 임시안, 08 I4): 정확한 인용 → 같은 기호(docstring이면 docstring, 아니면 정의 범위) → 대응 없음.
찾으면 새 판의 그 줄 범위를 판독으로 돌려준다. 못 찾으면 {"unmapped": True}를 돌려주고 작업자는 새 관측을 만들지 않는다.
원문 받기는 작업자가 후속 시계로 센다(이 판독기는 요청 예산을 쓰지 않는다). 원문은 Transport(실제·기록·재생)로 받는다.
"""
from __future__ import annotations

from .. import locate, normalize
from .reader_github import READER_ID, raw_url


class PinnedCodeChannelReader:
    def __init__(self, ledger, transport, *, reader_id: str = READER_ID):
        self.L, self.t, self.reader_id = ledger, transport, reader_id

    @staticmethod
    def _repo_path(url: str) -> tuple[str, str]:
        k = normalize.keys(url)
        return "/".join(k["target"][3:].split("/")[:2]), k["position"].split("#")[0]

    def __call__(self, obs, edition_key, at: str) -> dict | None:
        if not edition_key:            # 채널 항목이 판을 주지 않으면 무엇을 읽을지 모른다. 실패로 센다
            return None
        repo, path = self._repo_path(obs["url"])
        r = self.t.get(raw_url(repo, edition_key, path), note=f"follow {repo}@{edition_key}:{path}")
        if r.status != 200:
            return None
        text = r.text()
        python = path.endswith(".py")
        m = locate.map_position({"quote": obs["quote"], "symbol": obs["anchor_symbol"],
                                 "in_doc": bool(obs["anchor_in_doc"])}, text, python=python)
        url = normalize.pinned_blob(repo, path, edition_key)
        base = {"url": url, "edition_key": edition_key, "edition_kind": "release", "bytes": len(r.body),
                "reader": self.reader_id, "map": m}
        if not m["lines"]:
            return base | {"unmapped": True}
        a = locate.anchor(text, *m["lines"], python=python)
        bs = locate.byte_span(text, *m["lines"])
        return base | {"position": locate.position(*m["lines"]), "quote": a["quote"], "quote_lang": obs["quote_lang"],
                       "statement": obs["statement"], "map_method": m["method"], "map_from": obs["obs_id"],
                       "anchor_symbol": obs["anchor_symbol"], "anchor_in_doc": a["in_doc"],
                       "byte_span": f"{bs[0]}-{bs[1]}"}
