"""Render the three result tables, in order, from the committed ledgers."""
import json

from verify import CONDITIONS, KINDS, ROOT, csv_rows, inputs_and_runs, score

STATE = {"supported": "지지", "refuted": "반박", "unknown": "미확인", "conflicting": "상충"}
STATUS = {"excluded": "제외", "pending": "보류", "verified": "확정"}
VARIANT = {
    "original": "원문", "synonym": "동의", "order": "어순",
    "polarity": "극성", "scope": "범위", "omission": "누락",
}
CHANGE = {
    "original": "후보판과 변경·보존의 근거를 따로 표시",
    "synonym": "동일 효과의 근거 ID를 재사용할 조건을 확인",
    "order": "문장 전체의 순서와 절 위치를 분리",
    "polarity": "필수와 허용을 구분하고 새 조건으로 다시 판독",
    "scope": "이름과 원본·사용 발생의 ID를 함께 확인",
    "omission": "필수 정보가 비면 보류 사유와 필요 범위를 표시",
}
REASONS = {
    "literal_key_missing": "정확 문자열 누락", "unknown_or_different_edition": "판 불일치·미상",
    "action_or_target_unresolved": "동작·대상 미확인", "ambiguous_public_identity": "동명 발생",
    "different_action_or_target": "동작·대상 불일치", "different_range": "범위 불일치",
    "range_unresolved": "범위 미확인", "range_conflict": "범위 단서 상충", "required_span_missing": "필수 구간 누락",
    "observation_missing": "실제 관측 미확인", "identity_relation_unresolved": "동일 경로 관계 미확인",
    "permission_without_truth_obligation": "허용만 확인", "literal_keys": "문자열 대조", "compatible_slots": "슬롯 대조",
}


def clean(value):
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(header, rows):
    def line(values):
        return "| " + " | ".join(map(clean, values)) + " |"
    return "\n".join([line(header), line(["---"] * len(header)), *(line(row) for row in rows)])


def fmt_proof(values):
    return "/".join(", ".join(sorted(values[k])) or "∅" for k in CONDITIONS)


def render():
    requests, cases, aliases, blind, gold, runs = inputs_and_runs(ROOT)
    metrics = score(requests, gold, runs)
    sources = {f["evidence_id"]: f["source"] for case in cases.values() for f in case["evidence"]}
    edges = {}
    for edge in csv_rows(ROOT / "links.csv"):
        key = (aliases[edge["id"]], edge["method"])
        edges.setdefault(key, []).append(edge)
    history = csv_rows(ROOT / "lifecycle.csv")
    costs = json.loads((ROOT / "evidence" / "replays.json").read_text())[0]["db_costs"]
    first, second, third = [], [], []
    for rid, request in requests.items():
        case = cases[request["case_id"]]
        g = gold[rid]["raw"]
        raw_spans = blind[g["read_id"]]["parts"]
        parts_label = " · ".join(f"{k} [{s[0]},{s[1]})" if s else f"{k} 누락" for k, s in raw_spans.items())
        witness = []
        for k in CONDITIONS:
            for proof in sorted(gold[rid]["proof"][k]):
                src = sources[proof]
                witness.append(f'[{proof} · {src["selector"]}]({src["url"]})')
        witness.append(f'[원 요청]({case["raw_event"]["url"]})')
        if g["unresolved"]:
            witness.append(g["unresolved"])
        target = "<br>".join(
            " / ".join(g[f"{k}_{x}"] or "미확인" for x in ("target", "action", "polarity", "scope")) for k in CONDITIONS
        )
        first.append((rid, request["text"] + " · " + parts_label, target,
                      " / ".join(STATE[g[f"{k}_state"]] for k in CONDITIONS) + " · " + g["edition"], " · ".join(witness)))
        for method in ("A", "B"):
            run = runs[rid, method]
            stats = " / ".join(f'{STATE[g[k+"_state"]]}→{STATE[run["states"][k]]}' for k in CONDITIONS)
            signals = metrics[request["variant"]][method]["by_request"][rid]
            comparison = ", ".join(
                name + " " + "/".join(signals[internal]) for internal, name in
                (("wrong_inheritance","잘못 승계"), ("false_support","오지지"), ("missed","누락 근거"), ("justified_hold","정당 보류"))
                if internal in signals
            )
            row_edges = edges[rid, method]
            wrong = set(signals.get("wrong_inheritance", []) + signals.get("false_support", []))
            missing = set(signals.get("missed", []))
            focus = next((e for e in row_edges if e["criterion"] in wrong and e["used"] == "True"), None)
            if focus is None:
                focus = next((e for e in row_edges if e["criterion"] in missing and e["used"] == "False"), None)
            if focus is None:
                focus = next((e for e in row_edges if e["used"] == "True"), row_edges[0])
            reason = REASONS.get(focus["reason"], focus["reason"])
            if focus["criterion"] in wrong and focus["slots"]:
                slots = json.loads(focus["slots"])
                cues = ", ".join(dict.fromkeys(m["quote"] for m in slots["polarity_mentions"]))
                if cues:
                    reason += f" · 극성 단서 {cues}"
            second.append((f'{method} · {rid} · run {run["run_id"]} · `{run["id"]}`',
                           f'{run["candidate"]} @ {run["version"]} · {fmt_proof(run["evidence"])}',
                           stats, f'{STATUS[run["status"]]} · {comparison or "해당 없음"}',
                           f'{reason} · [{focus["evidence_id"]}]({focus["source_url"]})'))

    for variant in KINDS:
        rids = [r["id"] for r in requests.values() if r["variant"] == variant]
        d = metrics[variant]["distribution"]
        matches = []
        for method in ("A", "B"):
            if variant == "original":
                x = f"A·B 입력 SHA {len(rids)}/{len(rids)} 일치"
                matches = [x]
                break
            kept = sum(
                runs[rid, method]["decision_output_sha256"] ==
                runs[requests[rid]["case_id"]+"-original", method]["decision_output_sha256"] for rid in rids
            )
            matches.append(f"{method} 원문과 판정 출력 SHA 일치 {kept}/{len(rids)}")
        third.append((f'{VARIANT[variant]} · {len(rids)}',
                      "/".join(str(d[k]) for k in ("A_only","B_only","both","neither")),
                      " · ".join(matches),
                      f'A/B 각 {len(rids)} 판정 · 2조건/판정', CHANGE[variant]))
    for event in history:
        old, new = event["past_sha256"], event["new_sha256"]
        before, after = json.loads(event["before"]), json.loads(event["after"])
        delta = sum(after.values()) - sum(before.values())
        third.append((f'수명주기 {event["event"]} · 합성 1',
                      "원형 고정 엔진", f'`{old[:12]}` → '+(f'`{new[:12]}`' if new else "거절"),
                      f'SQLite 순증 {delta}행', "이전 판 보존 · " + (event["error"] or "새 판과 원 답의 출처 지문 대조")))
    third.append(("두 번 새 DB · 6사건", "replay 2/2",
                  "[지문 원장](evidence/replays.json)",
                  " · ".join(f'{m} {costs[m]["database_bytes"]:,}바이트, {costs[m]["table_counts"]["claim"]} claim' for m in ("A", "B")),
                  "원 인용과 판정 분포를 별도 검산"))
    return "\n\n".join((
        table(["사건·변형ID", "원문·구간", "대상·조작·극성·범위", "독립 정답·판", "근거 URL·절·미확인"], first),
        table(["방식·요청판", "후보·근거 ID (조작/보존)", "조건별 기대→실측 (조작/보존)", "잘못 승계·보류", "최소 반례"], second),
        table(["변형층·고유사건 수", "A만·B만·양쪽 정합·미확인/비정합",
               "과거·새 답 지문", "저장·검사 비용", "바꿀 결정"], third),
    ))


if __name__ == "__main__":
    print(render())
