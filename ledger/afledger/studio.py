"""Studio 입력 모형(06 3.1, 04 3.1). Studio 코드는 건드리지 않는다. Studio가 넘길 JSON의 모양만 정하고 검사한다.

{
  "request_key": "R1", "rev": 1, "received_at": "2026-11-26T01:00:00Z",
  "text": "요청 원문(사용자 언어 그대로)",
  "selected_part": {"label": "파이프라인: 작업 투입·완료 신호", "path": "pipeline/feed.py", "lines": [10, 42],
                    "commit": "abc123"},            # 문자열 하나도 받는다(label만)
  "environment": {"runtime": "CPython 3.13", "os": "linux", "deps": {"aiofiles": "23.2.1"}},  # 판·환경
  "context": {"workers_fixed": {"value": "yes", "provenance": "studio", "source": "..."}},
  "requirements": [{"code": "H1", "kind": "must", "text": "...", "provenance": "explicit"}],
  "prior": {"state": "given", "known": []},
  "needs": [{"slot": "keeps", "lang": "en", "text": "..."}]   # 없으면 접수(intake.py i1)가 쓴다
}
environment의 값은 provenance "studio"인 맥락 사실(runtime, os, dep:<이름>)로 들어간다.
선택 부분의 파일·줄·커밋은 사용자 저장소(비공개 원문)라 프로젝트 장부에만 쓴다(07 D6a).
"""
from __future__ import annotations

KINDS = {"must", "must_not", "prefer", "out_of_scope"}
PROVENANCE = {"explicit", "studio", "inferred", "later"}
SLOTS = {"input", "output", "user_without", "keeps", "breaks_when", "summary"}
PRIOR = {"given", "declined", "none"}


def parse(d: dict) -> dict:
    """Studio JSON을 검사해 Ledger.intake의 인자로 바꾼다. 잘못이면 ValueError(무엇이 틀렸나)."""
    errs = []
    for k in ("request_key", "rev", "received_at", "text"):
        if k not in d:
            errs.append(f"missing {k}")
    sp = d.get("selected_part", "")
    if isinstance(sp, dict):
        label = sp.get("label", "")
        where = sp.get("path")
        if where:
            if sp.get("lines"):
                a, b = sp["lines"]
                where += f":L{a}-L{b}"
            if sp.get("commit"):
                where += f"@{sp['commit']}"
            label = f"{label} ({where})" if label else where
    else:
        label = str(sp)
    reqs = []
    for r in d.get("requirements", []):
        if r.get("kind") not in KINDS:
            errs.append(f"requirement {r.get('code')}: kind {r.get('kind')!r}")
        if r.get("provenance", "explicit") not in PROVENANCE:
            errs.append(f"requirement {r.get('code')}: provenance")
        reqs.append({"code": r["code"], "kind": r["kind"], "text": r["text"],
                     "provenance": r.get("provenance", "explicit")})
    ctx = {}
    env = d.get("environment") or {}
    for k in ("runtime", "os"):
        if env.get(k):
            ctx[k] = {"value": str(env[k]), "provenance": "studio", "source": "Studio environment"}
    for name, ver in (env.get("deps") or {}).items():
        ctx[f"dep:{name}"] = {"value": str(ver), "provenance": "studio", "source": "Studio environment"}
    for k, v in (d.get("context") or {}).items():
        if not isinstance(v, dict) or "value" not in v or v.get("provenance") not in PROVENANCE:
            errs.append(f"context {k}: needs value and provenance")
            continue
        ctx[k] = v
    prior = d.get("prior")
    if prior is not None and prior.get("state", "given") not in PRIOR:
        errs.append("prior.state")
    needs = d.get("needs")
    for n in needs or []:
        if n.get("slot") not in SLOTS:
            errs.append(f"need slot {n.get('slot')!r}")
    if errs:
        raise ValueError("studio input: " + "; ".join(errs))
    return {"request_key": d["request_key"], "rev": int(d["rev"]), "at": d["received_at"], "text": d["text"],
            "selected_part": label, "requirements": reqs, "context": ctx, "prior": prior, "needs": needs}
