"""접수(04 2절 ①): Studio 입력을 요청판 한 거래로 쓴다. 칸별 필요 문장이 없으면 규칙 i1로 쓴다(06 A4).

i1은 번역도 모델도 쓰지 않는 규칙이다. 요청 원문의 줄과 조건을 단서 낱말로 칸에 나눈다.
  - 목표/Goal 줄 → summary
  - 전제/Given 줄의 문장 → 입력 단서(입력, iterator, producer, 받, input, iterator, receive)면 input, 나머지는 summary
  - 조건 must: 상한 단서(최대, 상한, 이하, 넘지, at most, maximum, bound, limit)면 keeps, 아니면 output
  - 조건 must_not → breaks_when
  - out_of_scope, 대상 부분/Target part 줄 → 쓰지 않는다
칸마다 문장을 이어 한 줄로 쓰고, 언어는 원문 그대로 둔다(한글이 있으면 ko). 이 규칙의 쓸모는 A4가 잰다(ledger/out/measure_a4.json).

i2(08 I19) = i1 + 이름표 없는 줄. 012의 K·P1·P2 요청처럼 '목표/전제' 이름표 없이 산문으로 쓴 줄은 i1이 버렸다.
i2는 그런 줄의 문장마다 단서로 칸을 정한다: 금지 단서(안 된다, 않아야, 금지, 허용하지 않, must not, may not) → breaks_when,
상한 단서 → keeps, 입력 단서 → input, 그 밖 → summary. 이름표가 있는 줄(R1)은 i1과 같게 다룬다.
requirements_from_text는 Studio가 조건을 따로 주지 않았을 때 원문의 'P02-H1:' 같은 줄을 조건으로 읽는다(측정용).
"""
from __future__ import annotations

import re

from . import config, studio

RULES = config.INTAKE_RULES
INPUT_CUES = ("입력", "iterator", "producer", "받는", "input", "receive", "lazy")
BOUND_CUES = ("최대", "상한", "이하", "넘지", "at most", "maximum", "bound", "limit", "no more than")
PROHIBIT_CUES = ("안 된다", "안 되", "않아야", "금지", "허용하지 않", "허용되지 않", "must not", "may not", "prohibit",
                 "not allowed", "should not")
REQ_HEAD = re.compile(r"^[A-Z]+\d*-H\d+$")
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
        elif any(body.strip() == t for t in req_texts) or REQ_HEAD.match(head.strip()):
            continue   # 조건 줄은 아래에서 조건 종류로 나눈다
        elif RULES != "i1" and line.strip() not in req_texts:
            for s_ in _sentences(line):          # i2: 이름표 없는 산문 줄
                lo = s_.lower()
                if any(c in lo for c in PROHIBIT_CUES):
                    slot = "breaks_when"
                elif any(c in lo for c in BOUND_CUES):
                    slot = "keeps"
                elif any(c in lo for c in INPUT_CUES):
                    slot = "input"
                else:
                    slot = "summary"
                slots.setdefault(slot, []).append(s_)
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


def requirements_from_text(text: str) -> list[dict]:
    """원문의 'P02-H1: …'·'범위 밖: …' 줄을 조건으로 읽는다. Studio가 조건을 주지 않은 측정용 요청에 쓴다."""
    out = []
    for line in text.splitlines():
        head, sep, body = line.partition(":")
        h, body = head.strip(), body.strip()
        if not sep or not body:
            continue
        if REQ_HEAD.match(h):
            kind = "must_not" if any(c in body.lower() for c in PROHIBIT_CUES) else "must"
            out.append({"code": h.split("-")[-1], "kind": kind, "text": body})
        elif h.lower() in ("범위 밖", "out of scope"):
            out.append({"code": "X", "kind": "out_of_scope", "text": body})
    return out


def intake(L, p: str, studio_json: dict) -> tuple[int, dict]:
    """요청판을 쓴다. 돌려주는 값: (req_id, {'needs_by': 'studio'|'i1', 'needs': [...]})."""
    kw = studio.parse(studio_json)
    by = "studio"
    if not kw["needs"]:
        kw["needs"] = write_needs(kw["text"], kw["requirements"])
        by = RULES
    req = L.intake(p, **kw)
    return req, {"needs_by": by, "needs": kw["needs"]}


# ---- 08 I29: 한 문장 요청에 한 번 되묻기(I19의 b를 복사 대신 질문으로)
REASK = (("input", {"ko": "무엇을 받아 처리하나요?", "en": "What does it take in?"}),
         ("breaks_when", {"ko": "무엇이 깨지면 안 되나요?", "en": "What must not break?"}))


def reask_questions(needs: list[dict], lang: str = "ko") -> list[dict]:
    """필요 문장이 칸 하나뿐이면 비어 있는 칸(받는 것, 깨지면 안 되는 것)마다 질문 하나를 돌려준다. 한 번만 묻는다.
    칸이 둘 이상이면 묻지 않는다. 같은 문장을 다른 칸에 복사하지 않는다(I24)."""
    filled = {n["slot"] for n in needs if (n["text"] or "").strip()}
    if len(filled) >= 2:
        return []
    return [{"slot": slot, "question": q[lang]} for slot, q in REASK if slot not in filled and
            not (slot == "breaks_when" and "keeps" in filled)]


def apply_reask(needs: list[dict], answers: dict[str, str]) -> list[dict]:
    """되묻기 답을 칸으로 넣는다. "깨지면 안 되는 것" 답은 상한 단서가 있으면 keeps, 아니면 breaks_when. 이미 있는 문장은 넣지 않는다."""
    have = {(n["text"] or "").strip() for n in needs}
    out = [dict(n) for n in needs]
    for slot, text in answers.items():
        text = (text or "").strip()
        if not text or text in have:
            continue
        if slot == "breaks_when" and any(c in text.lower() for c in BOUND_CUES) and \
                not any(c in text.lower() for c in PROHIBIT_CUES):
            slot = "keeps"
        out.append({"slot": slot, "lang": _lang(text), "text": text})
    return out
