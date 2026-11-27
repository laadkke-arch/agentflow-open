"""포착 실행 단위의 환경 고장 의심 표시(08 I46 규칙 2).

포착 쪽(capture.py)은 한 실행에서 상태 0 실패가 80%(200건 이상)를 넘으면 멈추고 그 실행의 실패 줄에 env_suspect를 단다.
조금씩 끊긴 실행은 표시 없이 남을 수 있다. 장부로 옮기기 전에 실행마다 다시 센다. 실행은 줄을 더한 커밋으로 가른다.
"""
from __future__ import annotations

from collections import defaultdict

from . import config

STATUS0_FAIL = ("unreachable", "blocked_policy")


def mark_runs(lines: list[dict], run_key=lambda l: l["run"], share: float | None = None, min_lines: int | None = None) -> list[dict]:
    """줄을 실행별로 묶어, 상태 0 실패 몫이 share 이상(줄 min_lines 이상)인 실행의 상태 0 실패 줄에 env_suspect를 단 사본을 돌려준다.
    원래 표시는 그대로 둔다."""
    share = config.ENV_SUSPECT_SHARE if share is None else share
    min_lines = config.ENV_SUSPECT_MIN if min_lines is None else min_lines
    runs = defaultdict(list)
    for l in lines:
        runs[run_key(l)].append(l)
    suspect = set()
    for k, ls in runs.items():
        f0 = sum(1 for l in ls if l.get("status") == 0 and l.get("outcome") in STATUS0_FAIL)
        if len(ls) >= min_lines and f0 / len(ls) >= share:
            suspect.add(k)
    out = []
    for l in lines:
        m = dict(l)
        if run_key(l) in suspect and l.get("status") == 0 and l.get("outcome") in STATUS0_FAIL:
            m["env_suspect"] = True
        out.append(m)
    return out
