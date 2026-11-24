#!/usr/bin/env python3
"""Write the frame and sealed packet predictions from source-only observations."""
import argparse
import csv
import hashlib
import json
from pathlib import Path



ROOT = Path(__file__).resolve().parent.parent
PRODUCTS = {
    "G": ("GIMP", "3.0.6", "a77e8fd05d3d08a58650531a3700100f6a3216b7",
          "https://gitlab.gnome.org/GNOME/gimp/-/blob/"),
    "I": ("Inkscape", "1.4.3", "0d15f7504220b00925bc3cb3673fcf44610a17d5",
          "https://gitlab.com/inkscape/inkscape/-/blob/"),
}
PURPOSE = "선택된 UI 문구와 같은 조작·상태를 표시하는 기존 구현을 찾고 대상 언어의 발행 근거를 연결한다."
LANGUAGES = ("ko", "de")
VIEWS = ("A", "A+위치", "B", "C", "직접 키")


def encoded(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode()


def source_url(product, ref):
    _, _, commit, base = PRODUCTS[product]
    path, line = ref
    return f"{base}{commit}/{path}#L{line}"


def parse_ref(ref):
    path, number = ref.split(":")
    return path, int(number)


def proof(source, specification, fallback_path=None):
    if fallback_path is not None:
        line, snippet = specification.split(":", 1)
        path = fallback_path
    else:
        path, line, snippet = specification.split(":", 2)
    number = int(line)
    raw = (source / path).read_text(encoding="utf-8").split("\n")[number - 1]
    if snippet not in raw:
        raise ValueError(f"{path}:{number} does not contain {snippet!r}: {raw!r}")
    offset = len(raw[:raw.index(snippet)].encode())
    return {
        "path": path, "line": number, "utf8_start": offset,
        "utf8_end_exclusive": offset + len(snippet.encode()), "text": snippet,
        "line_sha256": hashlib.sha256(raw.encode()).hexdigest(),
        "line_text": raw.strip(),
    }


def dump_csv(path, records):
    with path.open("w", newline="", encoding="utf-8") as out:
        w = csv.DictWriter(out, fieldnames=list(records[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(records)


def dump_jsonl(path, records):
    path.write_bytes(b"".join(encoded(row) + b"\n" for row in records))


def catalog_candidates(product, entry, reviewed, context=None):
    keys = entry["keys"] if context is None else [
        one for one in entry["keys"] if one["context"] == context
    ]
    links = []
    for key in keys:
        matches = [row for row in reviewed if row["context"] == key["context"]]
        if matches and matches[0]["id"] == "I03b":
            # XML tooltip, action registry, and Undo wording are one implementation.
            links.append(matches[0]["return_url"])
            continue
        for ref in key["references"]:
            found = next((row for row in matches if row["anchor"] == ref), None)
            if found:
                links.append(found["return_url"])
                if found["alternate_url"]:
                    links.append(found["alternate_url"])
            else:
                links.append(source_url(product, ref))
    return list(dict.fromkeys(links))


def make_predictions(group, rows, timestamp):
    product = group["product"]
    name, release, _, _ = PRODUCTS[product]
    for lang in LANGUAGES:
        for target in rows:
            for view in VIEWS:
                base = {"selection": group["msgid"], "purpose": PURPOSE,
                        "product": name, "release": release, "language": lang}
                b, c = target["b"], target["c"]
                full = dict(base)
                source_span = None
                if view == "A+위치":
                    full["source"] = {"commit": PRODUCTS[product][2],
                                      "path": target["anchor"][0], "line": target["anchor"][1]}
                elif view == "B":
                    full["reference"] = b["text"]
                    source_span = b
                elif view == "C":
                    full["reference"] = c["text"]
                    source_span = c
                elif view == "직접 키":
                    full["msgctxt"] = target["context"]
                orig = catalog_candidates(product, group, rows)
                same_key = catalog_candidates(product, group, rows, target["context"])
                direct = [target["return_url"]]
                anchored = direct + ([target["alternate_url"]] if target["alternate_url"] else [])
                refs = {"A": orig, "A+위치": anchored, "B": direct, "C": orig,
                        "직접 키": same_key}[view]
                packet_id = f'{target["id"]}-{lang}-{VIEWS.index(view) + 1}'
                fingerprint = hashlib.sha256(encoded(full)).hexdigest()
                packet = dict(
                    packet_id=packet_id, call_id=target["id"], group=group["id"],
                    view=view, payload=full, scope="기능 링크와 별도 번역 근거",
                    source_span=source_span, payload_sha256=fingerprint,
                    selection_bytes=len(group["msgid"].encode()), payload_bytes=len(encoded(full)),
                    extra_bytes=len(encoded(full)) - len(encoded(base)),
                    reference_bytes=len(source_span["text"].encode()) if source_span else 0,
                )
                decision = "유일" if len(refs) == 1 else "여럿" if refs else "보류"
                if view in ("A", "C") and len(refs) != 1:
                    reason = "동일 목적과 표면에 출전 후보가 남음. C는 별개 제어이며 실제 동작 근거로 승인하지 않음."
                elif view == "직접 키" and len(refs) != 1:
                    reason = "카탈로그 키는 고정. 같은 키의 복수 소비자는 구분 불가."
                elif view == "A+위치" and len(refs) != 1:
                    reason = "공용 enum 원문 앵커에서 복수 콤보로 역참조됨."
                else:
                    reason = "원문 위치 또는 실제 역할·단일 후보에서 동작의 구현 위치까지 연결 가능."
                questions = {
                    "G01": "보간 함수 혼합 상태인가, 색 공간 혼합 상태인가?",
                    "G02": "캔버스 크기 조정의 레이어 선택인가, 버킷 선화 감지 입력인가?",
                    "G03": "보기의 색 관리와 바깥 패딩 중 어느 설정을 복원하는가?",
                    "G04": "불러오면서 색 프로필과 방향 메타데이터 중 무엇을 묻는가?",
                    "G05": "브러시 출력 종횡비인가, 선택 사각형의 고정 규칙인가?",
                    "G06": "측정 각도인가, 레이어 블렌드 공간·합성 공간·합성 모드 중 어느 조합인가?",
                    "I01": "상태 표시줄의 채우기·획인가, 도구 스타일 스와치인가?",
                    "I02": "글꼴 자형·너비인가, 창 크기인가, 다른 Default 입력인가?",
                    "I03": "이미 선택한 객체의 종류 표시인가, 선택을 묶는 명령인가?",
                    "I04": "복제에서 HSL 성분을 읽는가, Tweak으로 색상 성분을 바꾸는가?",
                    "I05": "어느 객체의 높이인가, 겹침 제거의 수평 간격인가?",
                    "I06": "복제 추적의 밝기 입력인가, Tweak의 밝기 편집인가?",
                }
                yield packet, dict(
                    packet_id=packet_id, group=group["id"], call_id=target["id"],
                    language=lang, view=view, sealed_utc=timestamp,
                    candidate_urls=json.dumps(refs, ensure_ascii=False),
                    decision=decision,
                    expected_function=target["role"] if decision == "유일" else "복수 후보의 목표를 보류",
                    proposed_url=refs[0] if decision == "유일" else "",
                    additional_question=questions.get(group["id"], "어느 UI 표면에서 보았는가?")
                    if decision != "유일" else "추가 질문 없음",
                    reason=reason, prior_exposure="고정 소스·POT. ko/de 결과 미열람",
                    payload_sha256=fingerprint,
                )


def seal(source_roots, frame_dir, output, timestamp):
    with (ROOT / "evidence/call-notes.tsv").open(encoding="utf-8") as file:
        notes = {row["id"]: row for row in csv.DictReader(file, delimiter="\t")}
    frame_rows, call_rows, packets, predictions = [], [], [], []
    for product, source in source_roots.items():
        raw = json.loads((frame_dir / f"{product}.json").read_text())
        cases = [
            (f"{product}{rank:02}", rank, entry) for rank, entry in enumerate(
                raw["explicit_multicontext_groups"][:12], 1)
        ]
        cases.extend((f"{product}C{rank}", rank, entry)
                     for rank, entry in enumerate(raw["single_controls"], 1))
        for group_id, rank, entry in cases:
            explicit = [key for key in entry["keys"] if key["context"]]
            is_control = group_id[1] == "C"
            selected = is_control or rank <= 6
            frame_rows.append(dict(
                id=group_id, product=PRODUCTS[product][0], release=PRODUCTS[product][1], rank=rank,
                layer="single_control" if is_control else "natural_candidate",
                msgid=entry["msgid"], utf8_hex=entry["msgid"].encode().hex(),
                explicit_contexts=json.dumps([key["context"] for key in explicit], ensure_ascii=False),
                all_refs=json.dumps(entry["keys"], ensure_ascii=False),
                chosen=json.dumps([key["context"] for key in explicit[:2]] if selected else [], ensure_ascii=False),
                status="sealed" if selected else "after_six",
                exclusion_or_limit=("선정 6개 이후. 원문 후보만 보관, 실제 호출 적격 별도 판독 대상"
                                    if not selected else "생산자 및 소비 위치는 calls.csv"),
            ))
            if not selected:
                continue
            seen = []
            for char, key in zip("ab", explicit[:2]):
                row = notes[group_id + char]
                anchor = key["references"][0]
                b = proof(source, row["b_ref"])
                c = proof(source, row["c_ref"], anchor[0])
                if len(c["text"].encode()) > len(b["text"].encode()):
                    raise ValueError(f'C is over B budget for {row["id"]}')
                if b["text"] in (entry["msgid"], key["context"]):
                    raise ValueError(f'B leaks the chosen bytes or msgctxt for {row["id"]}')
                for binding in row["binding_chain"].split(";"):
                    path, lines = binding.split(":")
                    count = len((source / path).read_bytes().splitlines())
                    first, last = map(int, lines.split("-"))
                    if not 1 <= first <= last <= count:
                        raise ValueError(f"invalid source binding {binding} ({count} lines)")
                alt = row["alternate_return"]
                generated = anchor[0].endswith("-enums.c")
                seen.append(dict(
                    id=row["id"], group=group_id, msgid=entry["msgid"], context=key["context"],
                    anchor=anchor, anchor_url=source_url(product, anchor),
                    role=row["role"], type_hint="generated-enum-bound" if generated else "direct",
                    binding_chain=row["binding_chain"], behavior_class=row["behavior_class"],
                    return_url=source_url(product, parse_ref(row["return_ref"])),
                    alternate_url=source_url(product, parse_ref(alt)) if alt != "-" else "",
                    b=b, c=c,
                ))
            for row in seen:
                packed = dict(row)
                for key in ("anchor", "b", "c"):
                    packed[key] = json.dumps(packed[key], ensure_ascii=False)
                call_rows.append(packed)
            group = {**entry, "id": group_id, "product": product}
            for packet, prediction in make_predictions(group, seen, timestamp):
                packets.append(packet)
                predictions.append(prediction)
    dump_csv(output / "frame.csv", frame_rows)
    dump_csv(output / "calls.csv", call_rows)
    dump_jsonl(output / "packets.jsonl", packets)
    dump_csv(output / "predictions.csv", predictions)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gimp", type=Path, required=True)
    parser.add_argument("--inkscape", type=Path, required=True)
    parser.add_argument("--frame", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--sealed-utc", required=True)
    args = parser.parse_args()
    seal({"G": args.gimp, "I": args.inkscape}, args.frame, args.output, args.sealed_utc)


if __name__ == "__main__":
    main()
