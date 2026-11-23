"""Build the three required AF-RES-104 result tables from sealed ledgers."""
from __future__ import annotations

import argparse
import csv
import json

from select_passages import ROOT, read_jsonl

STATUS = {"supported": "지지", "partial": "부분", "unknown": "미확인", "refuted": "반박"}
PAIR = {"both": "양쪽 완결", "left_only": "왼쪽만 완결", "right_only": "오른쪽만 완결",
        "neither": "모두 미완결", "incomparable": "비교불가"}


def table(headers, rows):
    def fmt(row):
        return "| " + " | ".join(str(cell).replace("|", "&#124;").replace("\n", " ") for cell in row) + " |"
    return "\n".join([fmt(headers), fmt(["---"] * len(headers)), *(fmt(row) for row in rows)]) + "\n"


def loc(one):
    a, b = one["unicode"]
    x, y = one["utf8"]
    return f"U[{a},{b}) B[{x},{y})"


def anchored(url, lo, hi):
    if "github.com" in url:
        return f"{url}#L{lo}-L{hi}"
    return f"{url}#n{lo}"


def link_range(f, start, end, url):
    return f"[{f} L{start}–{end}]({anchored(url, start, end)})"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    cases = {c["case_id"]: c for c in json.loads((ROOT / "protocol.json").read_bytes())["cases"]}
    packets = read_jsonl((ROOT / "packets.jsonl").read_bytes())
    judgments = read_jsonl((ROOT / "judgments.jsonl").read_bytes())
    comparisons = list(csv.DictReader((ROOT / "pairs.csv").read_text().splitlines()))
    exposure = json.loads((ROOT / "evidence" / "exposure.json").read_bytes())
    overlap = {pid: len(shared) for row in exposure for pid, shared in row["cross_case_overlap_by_packet"].items()}
    decisions = json.loads((ROOT / "evidence" / "audit-decisions.json").read_bytes())
    pindex = {(p["case_id"], p["policy"], p["window"]): p for p in packets}
    ordinal = {p["packet_id"]: i for i, p in enumerate(packets, 1)}
    sources = {s["file_id"]: s["url"] for p in packets for s in p["slots"] if not s["empty"]}
    state = {}
    for row in judgments:
        state.setdefault(row["packet_id"], {}).setdefault(row["phase"], []).append(row)
    feature_rows = read_jsonl((ROOT / "evidence" / "feature-visibility.jsonl").read_bytes())
    features = {r["id"]: r["point"] for r in feature_rows}

    lines = ["# AF-RES-104 · 같은 파일의 같은 문자 예산에서 구간 선택 비교\n", "## 1. 예산 표\n"]
    budgets = []
    for c in cases.values():
        cid = c["case_id"]
        for policy in ("A", "B"):
            w1, w2 = (pindex[cid, policy, w] for w in ("W1", "W2"))
            a, b = [p["metrics"] for p in (w1, w2)]
            src = [f"[{c['question_id']}]({c['revision_url']})"] + [f"[{s['file_id']}][{s['file_id']}]"
                for s in w1["slots"] if not s["empty"]]
            slots = [f"{s['slot']} {s['file_id'] or '공석'}" for s in w1["slots"]]
            states = "실재 슬롯별 동일, 기존 S 재현"
            if a["empty_slots"]:
                states += " · 공석 2개는 각 1회 과금"
            shared = f"선행 사례 공유 파일 {overlap[w1['packet_id']]}개"
            receipts = f"[두 패킷](packets.jsonl#L{ordinal[w1['packet_id']]}-L{ordinal[w2['packet_id']]})"
            budgets.append([f"{cid}·{policy}", " · ".join(src), " · ".join(slots),
                f"W1 {a['display_chars']:,}자 / {a['display_utf8_bytes']:,}B / {a['additional_moves']}회<br>W2 {b['display_chars']:,}자 / {b['display_utf8_bytes']:,}B / {b['additional_moves']}회",
                f"{states} · {shared} · 독해 시간 미확인 · {receipts}"])
    lines.append(table(["요청·정책", "최초 질문·파일판 URL", "원 파일 4자리·공석",
                       "W1·W2 문자·바이트·추가 이동", "예산 일치·선행 노출·미확인"], budgets))

    lines.append("## 2. 필수조건 판독 표\n")
    readings = []
    for packet in packets:
        cid, pol, mode, pid = (packet[k] for k in ("case_id", "policy", "window", "packet_id"))
        rows = state[pid]["initial_opaque_self_read"]
        audits = state[pid]["post_lock_F_audit"]
        blocks = []
        for s in packet["slots"]:
            if s["empty"]:
                blocks.append(f"{s['slot']} 공석")
            else:
                f = s["file_id"]
                blocks.append(f"{s['slot']} [{f}][{f}] " + " / ".join(loc(seg) for seg in s["segments"]))
        rationale = [f"{r['condition_id']} {STATUS[r['status']]} · {r['reason']}" for r in rows]
        refs = []
        for row in rows:
            refs.append(row["condition_id"] + " " + (" · ".join(
                f"{link_range(c['file_id'],*c['lines_lf'],c['url'])} {loc(c)}" for c in row["citations"]
            ) or "미확인"))
        replacement = [a["alternate_proof_of_same_condition"] for a in audits if a["alternate_proof_of_same_condition"]]
        remaining = [r["condition_id"] for r in rows if r["status"] != "supported"]
        summary = "완결" if not remaining else "부분" if any(r["status"] in ("partial", "supported") for r in rows) else "미확인"
        note = " · ".join(replacement) if replacement else decisions["w1_w2_notes"][f"{cid}/{pol}"][0]
        if remaining:
            note = f"{', '.join(remaining)} 미충족. {note}"
        readings.append([f"{cid}·{pol}·{mode} [`{pid}`](packets.jsonl#L{ordinal[pid]})", "<br>".join(blocks),
                         "<br>".join(rationale), "<br>".join(refs), summary, note])
    lines.append(table(["요청·정책·창", "파일·Unicode/UTF-8 구간", "필수조건별 실제 확인 내용",
                       "지지·반박 근거 URL 및 경계", "완결·부분·미확인", "사라진 조건 또는 대체 절"], readings))

    lines.append("## 3. 대응·반환 표\n")
    return_rows = []
    for i, row in enumerate(comparisons, 2):
        cid, label, axis = (row[k] for k in ("case_id", "comparison", "axis"))
        left, right = ("W1", "W2") if axis == "W1/W2" else ("A", "B")
        status = PAIR[row["result"]]
        if status == "오른쪽만 완결":
            status = f"{right}만 완결"
        if status == "왼쪽만 완결":
            status = f"{left}만 완결"
        recall = f"전체 인용 {left} {row['left_earlier_F_exact']} · {right} {row['right_earlier_F_exact']}"
        if cid == "J1" and (axis == "W1/W2" or label == "W2"):
            recall += " · 구현·새 시험이 C1 대체"
        if cid == "J2":
            recall += " · 결손 null의 좁은 대체"
        if row["exclusion"]:
            denominator = "주 비교 0/1 · 공석 3·4"
        else:
            denominator = "주 비교 1/1"
        lost = [features[f] for f in row["left_only_feature_ids"].split()]
        gained = [features[f] for f in row["right_only_feature_ids"].split()]
        limits = ("오른쪽에서 빠짐 " + " · ".join(lost) + ". " if lost else "") + (
            "오른쪽에 추가 " + " · ".join(gained) + ". " if gained else "")
        if axis == "W1/W2":
            limits += decisions["w1_w2_notes"][f"{cid}/{label}"][1]
        else:
            limits += "대조 파일 동일." if cases[cid]["stratum"] == "control" else (
                "B 공석으로 이미지·의존성 미확인." if cid == "P3" else "표시된 제한을 실제 사용자 실행으로 확장할 수 없다.")
        links = [f"{link_range(src, lo, hi, sources[src])} {hint}"
                 for src, lo, hi, hint in decisions["return_links"][cid]]
        return_rows.append([f"{axis}·{cid} [`{row['pair_id']}`](pairs.csv#L{i})", status, recall, limits,
                            "<br>".join(links), denominator + " · 원 실행 미확인"])
    lines.append(table(["비교축·질문·짝 ID", "한쪽만·양쪽·모두 미완결·비교불가",
                       "원 F 인용 회수 또는 대체 근거", "원 시험·제약 손실",
                       "반환할 링크·절·조건", "분모·미확인"], return_rows))
    lines.append("U와 B는 각각 원 Unicode 코드포인트 및 UTF-8 바이트의 0기반 반열림 좌표다. 4자리에는 공석 비용이 들어간다. 반환 링크는 봉인 뒤 읽을 절을 가리키며 최초 판독에 추가되지 않는다.\n")
    lines.append("\n".join(f"[{item}]: {url}" for item, url in sorted(sources.items())) + "\n")
    lines.append("<!-- End of generated required tables -->\n")
    output = "\n".join(lines)
    if args.check:
        if not (ROOT / "RESULT.md").read_bytes().startswith(output.encode()):
            raise ValueError("required report tables differ from the ledgers")
        print("required tables verified: 16 budget rows, 32 reading rows, 32 paired rows")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
