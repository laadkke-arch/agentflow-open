"""Offline condition evaluator. Run python demo.py; its input is cases.json."""

import json
from pathlib import Path
from urllib.parse import urlsplit


CONTEXT_FIELDS = ("subject", "version", "scope", "configuration")
STATE_KO = {
    "supported": "지지", "refuted": "반증", "unknown": "미확인", "conflicting": "상충"
}
STATUS_KO = {"verified": "검증됨", "excluded": "배제", "pending": "보류"}
UNSPECIFIED = {"", "?", "*", "unknown", "미확인"}


def usable_locator(locator):
    """Only accept a bounded location. This offline check never fetches a source."""
    if not isinstance(locator, str) or any(ch.isspace() for ch in locator):
        return False
    try:
        parsed = urlsplit(locator)
        if parsed.scheme == "https" and parsed.hostname and parsed.path and parsed.fragment:
            return True
    except ValueError:
        return False
    return locator.startswith("cases.json#/records/") and bool(locator.split("/")[-1])


def rejection(claim, target):
    if claim.get("kind") != "direct":
        return "제안·비유 또는 직접 근거로 분류되지 않은 기록"
    if claim.get("direction") not in ("support", "refute"):
        return "근거 방향 미확인"
    if not usable_locator(claim.get("locator")):
        return "근거의 판독 위치 미확인"
    observed = claim.get("context") or {}
    for field in CONTEXT_FIELDS:
        expected, actual = target.get(field), observed.get(field)
        if not all(isinstance(val, str) and val.strip().casefold() not in UNSPECIFIED
                   for val in (expected, actual)):
            return f"{field} 미확인"
        if expected != actual:
            return f"{field} 불일치 ({actual} ≠ {expected})"
    return None


def evaluate(candidate, criteria, claims):
    """Judge a single configuration. Supported clauses do not prove a joint run."""
    outcomes = {}
    required = []
    for criterion in criteria:
        key = criterion["id"]
        if key in outcomes or not isinstance(criterion["required"], bool):
            raise ValueError("조건 ID는 고유해야 하며 required는 참 또는 거짓이어야 합니다.")
        relevant = [c for c in claims if c["candidate"] == candidate["id"]
                    and c["criterion"] == key]
        used, ignored, directions = [], {}, set()
        for claim in sorted(relevant, key=lambda c: c["id"]):
            reason = rejection(claim, candidate.get("context") or {})
            if reason:
                ignored[claim["id"]] = reason
            else:
                used.append(claim["id"])
                directions.add(claim["direction"])
        if len(directions) == 2:
            state, explanation = "conflicting", "같은 맥락의 직접 근거가 서로 반대입니다."
        elif "refute" in directions:
            state, explanation = "refuted", "같은 맥락에서 조건을 위반하는 근거가 있습니다."
        elif "support" in directions:
            state, explanation = "supported", "같은 맥락에서 조건을 지지하는 근거가 있습니다."
        else:
            state, explanation = "unknown", "이 맥락에 적용할 직접 근거가 없습니다."
        outcomes[key] = dict(state=state, explanation=explanation, used=used, ignored=ignored)
        if criterion["required"]:
            required.append(state)

    if "refuted" in required:
        status, reason = "excluded", "반증된 필수조건이 있습니다."
    elif required and all(state == "supported" for state in required):
        status, reason = "verified", "같은 맥락에서 각 필수조건을 지지하는 근거가 있습니다."
    else:
        status, reason = "pending", "필수조건이 비어 있거나 미확인·상충 조건이 남았습니다."
    return dict(status=status, explanation=reason, criteria=outcomes)


def next_check(criteria, results):
    """Pick one pending requirement: disagreement first, refutation next, then input order."""
    candidates = []
    for criterion in criteria:
        key = criterion["id"]
        if not criterion["required"]:
            continue
        states = {r["criteria"][key]["state"] for r in results.values()}
        pending = [cid for cid, r in results.items() if r["status"] == "pending"
                   and r["criteria"][key]["state"] in {"unknown", "conflicting"}]
        if pending:
            candidates.append(((len(states), "refuted" in states), key, pending))
    if not candidates:
        return None
    _, key, pending = max(candidates, key=lambda row: row[0])
    return {"criterion": key, "candidates": pending}


def load_fixture(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    for row in data["candidates"] + data["claims"]:
        row["context"] = data["contexts"][row["context"]]
    for claim in data["claims"]:
        local = "cases.json#/records/"
        if claim.get("locator", "").startswith(local):
            if claim["locator"][len(local):] not in data["records"]:
                raise ValueError(f"예제 근거 위치 없음: {claim['id']}")
    return data


def main():
    data = load_fixture(Path(__file__).with_name("cases.json"))
    results = {}
    for candidate in data["candidates"]:
        result = evaluate(candidate, data["criteria"], data["claims"])
        results[candidate["id"]] = result
        print(f"{candidate['label']} → {STATUS_KO[result['status']]} · {result['explanation']}")
        for spec in data["criteria"]:
            row = result["criteria"][spec["id"]]
            kind = "필수" if spec["required"] else "선호"
            print(f"  {kind} {spec['label']}: {STATE_KO[row['state']]} · {row['explanation']}")
            print("    채택", ", ".join(row["used"]) or "없음")
            for claim_id, reason in row["ignored"].items():
                print(f"    제외 {claim_id}: {reason}")
    alternatives = {key: results[key] for key in data["compare"]}
    choice = next_check(data["criteria"], alternatives)
    if choice:
        criterion = next(c for c in data["criteria"] if c["id"] == choice["criterion"])
        print(f"다음 확인 ({', '.join(choice['candidates'])}): {criterion['check']}")


if __name__ == "__main__":
    main()
