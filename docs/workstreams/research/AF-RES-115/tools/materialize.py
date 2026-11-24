"""Fetch the two inspected natural artifacts and build separate control copies."""
import argparse
import copy
import json
import re
from pathlib import Path

from frame import fetch, read_issue
from structure import compact, digest, drawing, emit, jsonl, native_score, score_xml

HERE = Path(__file__).resolve().parent.parent


def cache_blob(cache, value, expected=None):
    sha = digest(value)
    if expected is not None and sha != expected:
        raise ValueError(f"artifact changed, expected {expected}, got {sha}")
    (cache / f"{sha}.bin").write_bytes(value)
    return sha


def cached(cache, sha):
    value = (cache / f"{sha}.bin").read_bytes()
    if digest(value) != sha:
        raise ValueError(f"unexpected cache contents for {sha}")
    return value


def capture(case, cache):
    if case["format"] == "excalidraw":
        issue = read_issue(case["source_url"])
        body = issue["body"]
        if digest(body.encode()) != case["source_opening_sha256"]:
            raise ValueError("opening issue body differs from its frozen evidence")
        raw = re.search(r'\{"type":"excalidraw/clipboard".*\}', body)[0].encode()
    else:
        _, raw, _ = fetch(case["download_url"])
        source = case["fixed_attachment_url"].replace("https://github.com/", "https://raw.githubusercontent.com/").replace("/blob/", "/")
        _, updated, _ = fetch(source)
        cache_blob(cache, updated, case["fixed_blob_sha256"])
    cache_blob(cache, raw, case["blob_sha256"])


def from_control(control, raw, cache):
    return {**control, "blob_sha256": cache_blob(cache, raw), "bytes": len(raw), "status": "ready"}


def ex_control(control, raw, duplicate=False, repoint=False):
    scene = json.loads(raw)
    records = {item["id"]: item for item in scene["elements"]}
    label = records[control["mutation"]["seed"]]
    if duplicate:
        new_label = {**copy.deepcopy(label), "id": control["mutation"]["new_id"],
                     "x": label["x"] + 900, "boundElements": []}
        scene["elements"].append(new_label)
    if repoint:
        arrow = records[control["mutation"]["arrow"]]
        alternate = records[control["mutation"]["destination"]]
        arrow["endBinding"]["elementId"] = alternate["id"]
        label["boundElements"] = []
        alternate["boundElements"] = [{"id": arrow["id"], "type": "arrow"}]
    value = compact(scene).encode()
    shaped = drawing(value)
    by_id = {r["id"]: r for r in shaped}
    for r in shaped:
        for edge in r["refs"]:
            if edge["to"] not in by_id:
                raise ValueError(f'broken reference: {r["id"]} → {edge}')
    return value


def mx_control(control, raw, duplicate=False, repoint=False):
    if duplicate:
        needle = b'</measure>'
        added = (b'<measure number="2"><note id="m-copy"><pitch><step>D</step><octave>4</octave></pitch>'
                 b'<duration>4</duration><instrument id="IFl"/><type>whole</type></note></measure>')
        raw = raw.replace(needle, needle + added, 1)
    if repoint:
        raw = raw.replace(b'<instrument id="IFl"/>', b'<instrument id="IOb"/>', 1)
    normalized = score_xml(raw)
    definitions = {r["id"]: r["part"] for r in normalized if r["type"] == "score-instrument"}
    for note in (r for r in normalized if r["type"] == "note"):
        if any(definitions[edge["to"]] != note["part"] for edge in note["refs"]):
            raise ValueError("instrument reference points outside its part")
    return raw


def duplicate_frame(raw):
    match = re.search(rb"(?ms)^      <TBox>\r?\n.*?^[ \t]+</TBox>\r?\n", raw)
    if match is None or b"10,20,21,22,23" not in match[0]:
        raise ValueError("expected frame text was not found")
    offset = match.end()
    changed = raw[:offset] + match[0] + raw[offset:]
    hits = [r for r in native_score(changed) if r["type"] == "frame-text"
            and "10,20,21,22,23" in r["label"]]
    if len(hits) != 2:
        raise ValueError("duplicate artifact did not preserve both candidates")
    return changed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cache", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()
    args.cache.mkdir(parents=True, exist_ok=True)
    core = jsonl(HERE / "inputs.jsonl")
    controls = jsonl(HERE / "controls.jsonl")
    for case in core:
        if case["status"] == "ready" and args.fetch:
            capture(case, args.cache)
    repeat = next(case for case in core if case["id"] == "M60")
    raw = cached(args.cache, repeat["blob_sha256"])
    mutated = duplicate_frame(raw)
    extended = [*core, from_control({
        **repeat, "id": "M60-d", "tier": "linked-mutation", "parent": "M60",
        "target_summary": "같은 표시 내용의 독립 TBox 둘. 요청은 고를 수 있는 추가 주소를 주지 않음.",
        "selection_origin": "linked original text and synthetically duplicated TBox",
        "still_unknown": "두 TBox 중 선택. 원 작성자의 의도와 재편집 영향.",
    }, mutated, args.cache)]
    for base in controls:
        raw = (HERE / base["fixture_path"]).read_bytes()
        mutate = {"excalidraw": ex_control, "musicxml": mx_control}[base["format"]]
        extended.append(from_control(base, raw, args.cache))
        for suffix, action in (("d", "duplicate"), ("r", "repoint")):
            mutation_case = {**base, "id": f'{base["id"]}-{suffix}', "tier": "control-mutation",
                             "parent": base["id"], "mutation_type": action}
            if action == "duplicate":
                mutation_case["target_summary"] = "같은 표기인 시작 후보가 둘이다. 원 요청의 대상·보존 조건을 유지한다."
                mutation_case["still_unknown"] = "의도한 시작점과 이후 앱 상태."
            if action == "repoint":
                mutation_case["target_summary"] = "시작점은 유지하고 직접 관계 한 곳을 다른 대상에 둔다."
                mutation_case["still_unknown"] = "보고된 보존 조건과 바뀐 저장 관계의 양립 여부."
            extended.append(from_control(mutation_case, mutate(base, raw, **{action: True}), args.cache))
    emit(args.output, extended)


if __name__ == "__main__":
    main()
