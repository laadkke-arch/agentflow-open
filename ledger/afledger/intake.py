"""접수(04 2절 ①): Studio 입력을 요청판 한 거래로 쓴다. 칸별 필요 문장이 없으면 규칙 i1로 쓴다(06 A4).

i1은 번역도 모델도 쓰지 않는 규칙이다. 요청 원문의 줄과 조건을 단서 낱말로 칸에 나눈다.
  - 목표/Goal 줄 → summary
  - 전제/Given 줄의 문장 → 입력 단서(입력, iterator, producer, 받, input, iterator, receive)면 input, 나머지는 summary
  - 조건 must: 상한 단서(최대, 상한, 이하, 넘지, at most, maximum, bound, limit)면 keeps, 아니면 output
  - 조건 must_not → breaks_when
  - out_of_scope, 대상 부분/Target part 줄 → 쓰지 않는다
칸마다 문장을 이어 한 줄로 쓰고, 언어는 원문 그대로 둔다(한글이 있으면 ko). 이 규칙의 쓸모는 A4가 잰다(ledger/out/measure_a4.json).
"""
from __future__ import annotations

import re

from . import config, studio

RULES = config.INTAKE_RULES
INPUT_CUES = ("입력", "iterator", "producer", "받는", "input", "receive", "lazy")
BOUND_CUES = ("최대", "상한", "이하", "넘지", "at most", "maximum", "bound", "limit", "no more than")
SKIP_PREFIX = ("대상 부분", "target part", "범위 밖", "out of scope")


def _lang(text: str) -> str:
    return "ko" if re.search(r"[가-힣]", text) else "en"


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?。])\s+|(?<=다\.)\s*", text) if s.strip()]


def write_needs(text: str, requirements: list[dict]) -> list[dict]:
    slots: dict[str, list[str]] = {}
    req_texts = {r["text"].strip() for r in requirements}
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        low = line.lower()
        head, _, body = line.partition(":")
        h = head.strip().lower()
        if low.startswith(SKIP_PREFIX):
            continue
        if h in ("목표", "goal"):
            slots.setdefault("summary", []).append(body.strip())
        elif h in ("전제", "given"):
            for s in _sentences(body):
                slot = "input" if any(c in s.lower() for c in INPUT_CUES) else "summary"
                slots.setdefault(slot, []).append(s)
        elif any(body.strip() == t for t in req_texts):
            continue   # 조건 줄은 아래에서 조건 종류로 나눈다
    for r in requirements:
        t = r["text"].strip()
        if r["kind"] == "out_of_scope":
            continue
        if r["kind"] == "must_not":
            slot = "breaks_when"
        elif r["kind"] == "must":
            slot = "keeps" if any(c in t.lower() for c in BOUND_CUES) else "output"
        else:
            continue
        slots.setdefault(slot, []).append(t)
    order = ["input", "output", "keeps", "breaks_when", "summary"]
    return [{"slot": s, "lang": _lang(" ".join(slots[s])), "text": " ".join(slots[s])} for s in order if s in slots]


def intake(L, p: str, studio_json: dict) -> tuple[int, dict]:
    """요청판을 쓴다. 돌려주는 값: (req_id, {'needs_by': 'studio'|'i1', 'needs': [...]})."""
    kw = studio.parse(studio_json)
    by = "studio"
    if not kw["needs"]:
        kw["needs"] = write_needs(kw["text"], kw["requirements"])
        by = RULES
    req = L.intake(p, **kw)
    return req, {"needs_by": by, "needs": kw["needs"]}
