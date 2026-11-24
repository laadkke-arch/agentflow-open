"""Join the two raw name-probe receipts to the sealed study directions."""

import csv
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
PYTHON = "CPython 3.13.0"
ICU = "ICU4C 76.1"
CHOICES = ("U_UNICODE_CHAR_NAME", "U_CHAR_NAME_ALIAS", "U_EXTENDED_CHAR_NAME")
SHORT_CHOICE = dict(zip(CHOICES, ("UNICODE", "ALIAS", "EXTENDED"), strict=True))
ICU_FAILURE = (65535, 12, "U_ILLEGAL_CHAR_FOUND")
ICU_SUCCESS = (0, "U_ZERO_ERROR")


def csv_rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def receipt_rows(directory, consumer, repeat):
    if consumer == PYTHON:
        lines = (directory / f"python-{repeat}.stdout").read_text().splitlines()
        metadata, *body = [json.loads(line) for line in lines]
        assert metadata["kind"] == "metadata" and metadata["ucd"] == "15.1.0"
        assert all(row["kind"] == "call" and row["repeat"] == repeat for row in body)
        return body, 2
    lines = (directory / f"icu-{repeat}.stdout").read_text().splitlines()
    rows = [line for line in lines if not line.startswith("#")]
    assert "# u_getUnicodeVersion=16.0 (16,0,0,0)" in lines
    body = list(csv.DictReader(rows, delimiter="\t"))
    assert all(None not in row and row["repeat"] == str(repeat) for row in body)
    return body, len(lines) - len(rows) + 2


def observations(directory, consumer):
    runs = []
    for repeat in (1, 2):
        rows, start = receipt_rows(directory, consumer, repeat)
        indexed = {}
        for line, raw in enumerate(rows, start):
            key = raw["input_id"], raw["choice"]
            assert key not in indexed, key
            row = {k: v for k, v in raw.items() if k not in ("kind", "repeat")}
            indexed[key] = row, line
        runs.append(indexed)
    first, second = runs
    assert first.keys() == second.keys()
    return [(row, second[key][0], line, second[key][1])
            for key, (row, line) in first.items()]


def outcome(consumer, raw):
    """Preserve each value needed to decide whether the probe matched."""
    if consumer == PYTHON:
        if "exception" in raw:
            return (raw["exception"],)
        if raw["operation"] == "lookup":
            return tuple(raw["code_points"])
        return (raw["value"],)
    status = int(raw["status"]), raw["status_name"]
    if raw["operation"] == "lookup":
        return int(raw["return"]), *status
    return int(raw["return"]), raw["buffer_text"], *status


def expand_prediction(consumer, direction, row, inputs):
    """Expand AF-RES-222 and the choice rules sealed in SCOPE.md."""
    code = int(row["code_point"], 16)
    choice = row["choice"]
    old_name = next((x["literal"] for x in inputs if x["role"] == "old"), "")
    correction = next((x["literal"] for x in inputs if x["alias_type"] == "correction"), "")
    if consumer == PYTHON:
        if direction != "code→Name":
            return (code,)
        if old_name:
            return (old_name,)
        return ("ValueError",) if choice == "name" else (None,)

    if direction == "old→code":
        return (code, *ICU_SUCCESS) if choice != CHOICES[1] else ICU_FAILURE
    if direction == "alias→code":
        if choice == CHOICES[1] and row["input"] == correction:
            return code, *ICU_SUCCESS
        return ICU_FAILURE
    names = (old_name, correction, old_name or "<control-000A>")
    name = names[CHOICES.index(choice)]
    return len(name), name, *ICU_SUCCESS


def json_compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def call_links(phase, consumer, n1, n2):
    stem = "python" if consumer == PYTHON else "icu"
    return f"receipts/{phase}/{stem}-1.stdout#L{n1}", f"receipts/{phase}/{stem}-2.stdout#L{n2}"


def main_calls(inputs, predicted):
    slot_by_key = {(r["consumer"], r["code_point"], r["direction"]): r for r in predicted}
    role = {r["input_id"]: r["role"] for r in inputs}
    rows = []
    for consumer, expected_count in ((PYTHON, 30), (ICU, 72)):
        observed = observations(HERE / "receipts/main", consumer)
        assert len(observed) == expected_count
        for first, second, n1, n2 in observed:
            cp, input_id = first["code_point"], first["input_id"]
            categories = {"old": "old→code", "alias": "alias→code"}
            direction = categories[role[input_id]] if input_id in role else "code→Name"
            slot = slot_by_key[consumer, cp, direction]
            prev = expand_prediction(consumer, direction, first, [x for x in inputs if x["code_point"] == cp])
            observed_1, observed_2 = outcome(consumer, first), outcome(consumer, second)
            raw_1, raw_2 = call_links("main", consumer, n1, n2)
            header_differs = (consumer == ICU and first["operation"] == "lookup"
                              and observed_1 == ICU_FAILURE)
            expected_header = "10 U_INVALID_CHAR_FOUND" if header_differs else ""
            argument = first["input"] if first["operation"] == "lookup" else "U+" + cp
            rows.append({
                "call_id": f"C{len(rows)+1:03}", "direction_id": slot["direction_id"],
                "code_point": cp, "input_id": input_id, "consumer": consumer,
                "operation": first["operation"], "choice": first["choice"],
                "argument": argument, "input_ascii_hex": first["input_ascii_hex"],
                "expected": json_compact(prev), "observed_1": json_compact(observed_1),
                "observed_2": json_compact(observed_2),
                "same_raw_values": int(first == second),
                "matches_expanded_prediction": int(observed_1 == observed_2 == prev),
                "header_prediction_conflict": expected_header,
                "receipt_1": raw_1, "receipt_2": raw_2,
            })
    return rows


def directions(predicted, calls):
    output = []
    for pred in predicted:
        did, consumer, cp, name_direction = (pred[key] for key in
                                           ("direction_id", "consumer", "code_point", "direction"))
        selected = [r for r in calls if r["direction_id"] == did]
        applicable = cp != "000A" or name_direction != "old→code"
        assert bool(selected) == applicable
        count = len(selected)
        header_diff = sum(bool(r["header_prediction_conflict"]) for r in selected)
        mismatched = sum(not r["matches_expanded_prediction"] for r in selected)
        comparison = ("N/A: 공식 Name 없음" if not applicable else
                      "확장 예측 %d/%d 일치" % (count-mismatched, count))
        if applicable and consumer == ICU and name_direction == "old→code":
            comparison += " / 선행표 choice 미기재"
        if header_diff:
            comparison += f" / I02 헤더 오류 상수 {header_diff}키 불일치"
        output.append({
            "direction_id": did, "code_point": cp, "consumer": consumer,
            "direction": name_direction, "applicability": "적용" if applicable else "N/A",
            "input_set": " / ".join(dict.fromkeys(r["argument"] for r in selected)) if selected else "",
            "call_ids": " ".join(r["call_id"] for r in selected),
            "planned_calls": count * 2, "observed_calls": count * 2, "missing_calls": 0,
            "repeat_different_keys": sum(not r["same_raw_values"] for r in selected),
            "baseline_expected": pred["expected"], "prediction_comparison": comparison,
            "missing_or_na_reason": "" if applicable else "UnicodeData field 1의 <control>은 공식 Name 부재",
        })
    return output


def error_rows(calls):
    output = []
    for row in calls:
        observed = json.loads(row["observed_1"])
        if row["consumer"] == PYTHON:
            if row["input_id"] != "000A-name":
                continue
            issue = "python_missing_name"
            header, impl = "P02 L38–42: ValueError/default", "P03 L1509–1516: ValueError 또는 default"
        elif row["operation"] == "lookup" and observed[1] != 0:
            issue = "lookup_miss_sentinel"
            header = "I02 L3806–3819: U_INVALID_CHAR_FOUND=10, undefined code"
            impl = "I03 L1530, L1624–1631: U_ILLEGAL_CHAR_FOUND=12, 0xFFFF"
        elif row["operation"] == "name" and observed[0] == 0:
            issue = "empty_name_with_success"
            header = "I02 L3758–3769: length 0, empty string"
            impl = "I03 L1487–1500: length 0 → NUL, U_ZERO_ERROR"
        else:
            continue
        output.append(error_entry(row, "main", issue, header, impl))
    return output


def error_entry(row, phase, issue, header, impl):
    return {
        "phase": phase, "case": row["input_id"], "code_point": row["code_point"],
        "consumer": row["consumer"], "operation": row["operation"], "choice": row["choice"],
        "input": row["argument"], "type": issue, "header_or_docs_expected": header,
        "implementation_or_generator_expected": impl,
        "raw_value_repeat_1": row["observed_1"], "raw_value_repeat_2": row["observed_2"],
        "repeat_match": row["same_raw_values"],
        "buffer_repeat_1": row.get("buffer_repeat_1", ""),
        "buffer_repeat_2": row.get("buffer_repeat_2", ""),
        "receipt_1": row["receipt_1"], "receipt_2": row["receipt_2"],
    }


def control_contract(consumer, first):
    if consumer == PYTHON:
        if first["operation"] == "name":
            return ("python_no_name", "P02 L38–42", "P03 L1509–1516: exception/default")
        return ("python_lookup_accept" if "code_points" in first else "python_lookup_miss",
                "P02 L29–35: KeyError on miss",
                "P03 L1055–1071, L1394–1443: exact algorithmic path vs ASCII folded table")
    error = int(first["status"])
    if first["operation"] == "lookup":
        if error:
            return ("lookup_miss_sentinel", "I02 L3806–3819: U_INVALID_CHAR_FOUND=10",
                    "I03 L1530–1631: return 0xFFFF / U_ILLEGAL_CHAR_FOUND=12")
        if first["return_hex"] == "FFFF":
            return ("valid_noncharacter", "I02 L3806–3819: code point on success",
                    "I03 L1562–1601: validated EXTENDED type and hexadecimal")
        return ("icu_lookup_accept", "I02 L3806–3813: complete name matching",
                "I03 L1545–1627: folds ASCII then branches on choice")
    if error:
        return ("buffer_warning" if error < 0 else "buffer_overflow",
                "I02 L3758–3769: complete length; header describes NUL",
                "I09 L1437–1458: warning on exact capacity, overflow if shorter")
    return ("empty_name_with_success" if first["return"] == "0" else "synthetic_reverse",
            "I02 L2060, L3758–3769: standard or synthetic plus full length",
            "I03 L1487–1500: choice, fallback label, then NUL")


def control_error_rows():
    output = []
    for consumer, count in ((PYTHON, 22), (ICU, 69)):
        rows = observations(HERE / "receipts/controls", consumer)
        assert len(rows) == count
        for first, second, n1, n2 in rows:
            issue, header, impl = control_contract(consumer, first)
            raw_1, raw_2 = call_links("controls", consumer, n1, n2)
            row = dict(first, consumer=consumer,
                       argument=first["input"] if first["operation"] == "lookup" else "U+" + first["code_point"],
                       observed_1=json_compact(outcome(consumer, first)),
                       observed_2=json_compact(outcome(consumer, second)),
                       same_raw_values=int(first == second), receipt_1=raw_1, receipt_2=raw_2)
            if consumer == ICU and first["operation"] != "lookup":
                for repeat, raw in ((1, first), (2, second)):
                    row[f"buffer_repeat_{repeat}"] = json_compact({
                        key: raw[key] for key in ("buffer_capacity", "nul_index", "buffer_hex")})
            output.append(error_entry(row, "controls", issue, header, impl))
    return output


def show_outcome(row):
    result = json.loads(row["observed_1"])
    if row["consumer"] == PYTHON:
        value = result[0]
        if row["operation"] == "lookup":
            return f"U+{value:04X}"
        return "None" if value is None else "ValueError" if value == "ValueError" else f'`{value}`'
    if row["operation"] == "lookup":
        value, error, name = result
        return f"{value} (U+{value:04X}) / {error} {name}" if error == 0 else f"{value} (0xFFFF) / {error} {name}"
    length, value, error, name = result
    return f'{length} / {error} {name} / ' + (f'`{value}`' if value else "빈 문자열")


def table_one(slots, calls):
    lines = ["## 표 1", "",
             "한 행은 코드 포인트 × 소비자 × 조회 방향 1자리다. 하위 호출은 각 입력×choice를 2회씩 실행했다. UNICODE/ALIAS/EXTENDED는 각각 `U_UNICODE_CHAR_NAME`/`U_CHAR_NAME_ALIAS`/`U_EXTENDED_CHAR_NAME`이며 번호는 0/3/2다. 이름 반환값은 길이 / 상태 / 텍스트 순이다.", "",
             "| 코드 포인트·입력 | 소비자·판·choice | 방향·반복 | 실제 값·예외·오류 상수 | 원영수증·예측 차이 | 미확인 |",
             "| --- | --- | --- | --- | --- | --- |"]
    for slot in slots:
        selected = [r for r in calls if r["direction_id"] == slot["direction_id"]]
        name_direction = slot["direction"]
        keys = list(dict.fromkeys(r["choice"] for r in selected))
        choice = "/".join(SHORT_CHOICE.get(k, k) for k in keys)
        literal = slot["input_set"] if name_direction != "code→Name" else ""
        code_input = f'U+{slot["code_point"]}' + (f' · {literal}' if literal else "")
        if not selected:
            lines.append(f'| {code_input} · 공식 Name 없음 | {slot["consumer"]} | {name_direction} · N/A | N/A | AF-RES-222의 N/A 유지 | 해당 없음 |')
            continue

        displayed = []
        for key in keys:
            bucket = [r for r in selected if r["choice"] == key]
            values = list(dict.fromkeys(show_outcome(r) for r in bucket))
            count = f" ({len(bucket)}키)" if len(bucket) > 1 else ""
            label = f"{SHORT_CHOICE.get(key, key)} " if len(keys) > 1 else ""
            displayed.append(f"{label}{' / '.join(values)}{count}")
        groups = " / ".join(f"[{which}]({selected[0][f'receipt_{which}']})" for which in (1, 2))
        call_ids = selected[0]["call_id"]
        if len(selected) > 1:
            call_ids += f'–{selected[-1]["call_id"]}'
        comparison = slot["prediction_comparison"]
        lines.append(f'| {code_input} | {slot["consumer"]} · {choice} | {name_direction} · 1=2 | '
                     f'{"<br>".join(displayed)} | {groups} · {call_ids} · {comparison} | 없음 |')
    return "\n".join(lines) + "\n"


def generate_main():
    inputs = csv_rows(HERE / "inputs.csv")
    predicted = csv_rows(HERE / "predictions.csv")
    assert len(predicted) == 36
    for index, row in enumerate(predicted, 1):
        row["direction_id"] = f"D{index:02}"
    calls = main_calls(inputs, predicted)
    slots = directions(predicted, calls)
    write_csv(HERE / "calls.csv", calls)
    write_csv(HERE / "directions.csv", slots)
    write_csv(HERE / "errors.csv", error_rows(calls) + control_error_rows())
    sys.stdout.write(table_one(slots, calls))


if __name__ == "__main__":
    generate_main()
