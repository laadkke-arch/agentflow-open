"""위치 앵커와 판 사이 위치 대응(07 R-1 임시안, 규칙 판 m1).

위치는 줄 범위와 함께 앵커를 갖는다.
- 인용 앵커: 인용 본문의 공백 정리 지문(관측의 quote_fp와 같다).
- 기호 앵커: Python 파일이면 ast로 얻은 기호 경로(예: "Queue", "Queue.shutdown")와, 줄 범위가 그 기호의 docstring 안인지.

새 판을 열 때 찾는 순서:
  (1) exact_quote: 인용 본문을 공백을 접은 채 새 판에서 정확히 찾는다.
  (2) symbol:      같은 기호를 새 판의 ast에서 찾아 그 기호의 줄 범위(앞 위치가 docstring이었으면 docstring 범위)를 쓴다.
  (3) unmapped:    둘 다 실패하면 추측하지 않는다.
어떤 방법으로 찾았는지(map_method)를 관측에 남긴다. 규칙을 바꾸면 MAP_RULES를 올린다(config.py).
"""
from __future__ import annotations

import ast
import hashlib
import re

from . import config

MAP_RULES = config.MAP_RULES


def fold_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def quote_fp(text: str) -> str:
    return hashlib.sha256(fold_ws(text).encode("utf-8")).hexdigest()


def lines_text(text: str, a: int, b: int) -> str:
    """1부터 세는 줄 a..b(양 끝 포함)의 본문. 줄 앞 들여쓰기는 남긴다."""
    return "\n".join(text.splitlines()[a - 1:b])


def _folded_with_lines(text: str) -> tuple[str, list[int]]:
    """공백을 접은 본문과, 접은 본문의 글자마다 원래 줄 번호."""
    out, line_of, line, pending_ws = [], [], 1, False
    for ch in text:
        if ch.isspace():
            if out:
                pending_ws = True
            if ch == "\n":
                line += 1
            continue
        if pending_ws:
            out.append(" ")
            line_of.append(line)
            pending_ws = False
        out.append(ch)
        line_of.append(line)
    return "".join(out), line_of


def find_quote(text: str, quote: str) -> tuple[int, int] | None:
    """인용을 공백을 접은 채 찾아 줄 범위를 돌려준다. 두 곳 이상이면 None(애매하면 추측하지 않는다)."""
    folded, line_of = _folded_with_lines(text)
    q = fold_ws(quote)
    if not q:
        return None
    i = folded.find(q)
    if i < 0 or folded.find(q, i + 1) >= 0:
        return None
    return line_of[i], line_of[i + len(q) - 1]


def find_phrase(text: str, phrase: str) -> tuple[int, int] | None:
    """한 구절이 든 줄 범위. 문장 단위 인용을 고를 때 쓴다(구절은 판독 계획이 준다)."""
    return find_quote(text, phrase)


def _defs(tree) -> list[tuple[str, ast.AST]]:
    out = []

    def walk(node, prefix):
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                q = f"{prefix}.{ch.name}" if prefix else ch.name
                out.append((q, ch))
                walk(ch, q)
    walk(tree, "")
    return out


def _doc_range(node) -> tuple[int, int] | None:
    if node.body and isinstance(node.body[0], ast.Expr) and isinstance(getattr(node.body[0], "value", None), ast.Constant) \
            and isinstance(node.body[0].value.value, str):
        d = node.body[0]
        return d.lineno, d.end_lineno
    return None


def symbols(text: str) -> dict[str, dict]:
    """기호 경로 → {'range': (첫 줄, 끝 줄), 'doc': docstring 줄 범위 또는 None}. 구문 오류면 빈 사전."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return {}
    return {q: {"range": (n.lineno, n.end_lineno), "doc": _doc_range(n)} for q, n in _defs(tree)}


def symbol_at(text: str, a: int, b: int) -> tuple[str | None, bool]:
    """줄 a..b를 감싸는 가장 안쪽 기호와, 그 범위가 기호의 docstring 안인지."""
    best, in_doc = None, False
    for q, s in symbols(text).items():
        lo, hi = s["range"]
        if lo <= a and b <= hi and (best is None or q.count(".") >= best.count(".")):
            best = q
            d = s["doc"]
            in_doc = bool(d and d[0] <= a and b <= d[1])
    return best, in_doc


def anchor(text: str, a: int, b: int, *, python: bool) -> dict:
    """위치의 앵커. 인용은 줄 a..b의 본문이다."""
    quote = lines_text(text, a, b)
    sym, in_doc = symbol_at(text, a, b) if python else (None, False)
    return {"lines": (a, b), "quote": quote, "quote_fp": quote_fp(quote), "symbol": sym, "in_doc": in_doc}


def map_position(old: dict, new_text: str, *, python: bool) -> dict:
    """앞 판의 앵커(old: quote, symbol, in_doc)를 새 판 본문에서 찾는다.
    돌려주는 사전: method(exact_quote|symbol|unmapped), lines, symbol_present(새 판에 같은 기호가 있나), rules."""
    out = {"rules": MAP_RULES, "lines": None, "method": "unmapped", "symbol_present": None}
    syms = symbols(new_text) if python else {}
    if old.get("symbol"):
        out["symbol_present"] = old["symbol"] in syms
    if old.get("quote"):
        r = find_quote(new_text, old["quote"])
        if r:
            out.update(method="exact_quote", lines=r)
            return out
    if python and old.get("symbol") in syms:
        s = syms[old["symbol"]]
        r = s["doc"] if old.get("in_doc") and s["doc"] else s["range"]
        out.update(method="symbol", lines=r)
    return out


def byte_span(text: str, a: int, b: int) -> tuple[int, int]:
    """줄 a..b의 UTF-8 바이트 범위(양 끝 포함, HTTP Range 형식). 고정판은 바이트가 바뀌지 않는다."""
    raw_lines = text.encode("utf-8").splitlines(keepends=True)
    start = sum(len(x) for x in raw_lines[:a - 1])
    end = start + sum(len(x) for x in raw_lines[a - 1:b]) - 1
    return start, end


def position(a: int, b: int) -> str:
    """장부의 줄 위치 표기. GitHub 조각과 같은 꼴(L36-L38). 설계 예제는 'L36–38'(엔대시)이었다(08 I3)."""
    return f"L{a}-L{b}" if b != a else f"L{a}"


def parse_position(pos: str) -> tuple[int, int] | None:
    m = re.fullmatch(r"L(\d+)(?:[-–]L?(\d+))?", pos or "")
    if not m:
        return None
    return int(m.group(1)), int(m.group(2) or m.group(1))
