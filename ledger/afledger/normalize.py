"""주소 정규화(07 R-1 임시안). 규칙은 opensource의 n1을 바이트 그대로 가져와 쓴다(vendor/README.md).

장부가 쓰는 것:
- 관측의 원래 주소 문자열은 그대로 둔다(locator.url). 정규화 키는 열로 더한다(url_norm, page, target, norm_rules).
- 재사용 조회 키는 (page, edition, position)이다. target은 묶어 보여 주는 데만 쓰고 재사용 키로 쓰지 않는다
  (전역 병합 금지, 04 6.3).
- 정규화가 실패한 주소(예시·로컬 주소, 원문이 아닌 주소)는 원래 문자열을 page로 쓰고 rules에 실패 이유를 적는다.
  그래서 실패해도 재사용은 "같은 문자열"로 좁혀질 뿐 넓어지지 않는다.

알려진 빈칸(08 I3): docs.python.org/3.13/... 같은 문서 경로의 판을 n1은 뽑지 않는다(edition=None, page에 '3.13'이 남음).
판이 page 안에 남으므로 다른 판끼리 잘못 묶이지는 않는다. 단위 1은 첫 링크를 고정판 소스 줄로 내므로(D10) 고치지 않았다.
"""
from __future__ import annotations

from .vendor import rcore_normalize as _n1

RULES = _n1.RULES_VERSION   # "n1"
SOURCE = {
    "repo": "laadkke-arch/opensource",
    "path": "tools/rcore/normalize.py",
    "commit": "7c8f9860a6f1f39951ef6c2f2a4cfc4d8a5881bf",
    "blob": "1132b02225f8757e5a1e82b628c16b21bf584f82",
}


def keys(url: str) -> dict:
    """주소 하나의 정규화 키. 실패해도 예외를 내지 않는다."""
    r = _n1.safe_normalize(url)
    if r.get("error"):
        return {"raw": url, "url_norm": url, "page": url, "target": None, "edition": None, "position": None,
                "rules": f"{RULES}:{r['error']}"}
    return {k: r.get(k) for k in ("raw", "url_norm", "page", "target", "edition", "position")} | {"rules": RULES}


def pinned_blob(repo: str, path: str, edition: str, lines: tuple[int, int] | None = None) -> str:
    """고정판 소스 줄 링크(D10). 예: https://github.com/python/cpython/blob/v3.13.18/Lib/asyncio/queues.py#L36-L38"""
    url = f"https://github.com/{repo}/blob/{edition}/{path}"
    if lines:
        url += f"#L{lines[0]}" + (f"-L{lines[1]}" if lines[1] != lines[0] else "")
    return url
