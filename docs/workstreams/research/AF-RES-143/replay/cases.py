"""Expand the frozen input families into exact query cache keys."""
import json

from common import ROOT, json_in, sha


def cases_for(package, calibration=False):
    definition = json_in(ROOT / "replay/inputs.json")["calibration" if calibration else package]
    for family in definition["families"]:
        values = family.get("values")
        source = {"values": values} if values is not None else {"range_desc": family["range_desc"]}
        for fn in family.get("functions", definition["functions"]):
            ps = [None] if fn == "median" else family["ps"]
            for index, p in enumerate(ps):
                for mode in family.get("modes", definition["modes"]):
                    case = {"id": f"{fn}/{family['id']}/p{index}/{mode}", "function": fn,
                            "family": family["id"], "mode": mode, "p": p, "input": source,
                            "representation": family.get("representation", "array"),
                            "accessor": family.get("accessor"), "source": family["source"]}
                    layer = family["layer"]
                    if package == "d3-array" and fn == "quantileSorted" and layer not in {"unsupported-vector", "defensive"}:
                        clean = list(map(number_from_json, values)) if values is not None else None
                        if layer in {"missing-values", "accessor-missing"} or case["representation"] != "array":
                            layer = "sorted-outside-contract"
                        elif mode == "direct" and (clean is None or any(a > b for a,b in zip(clean, clean[1:]))):
                            layer = "sorted-outside-contract"
                    case["layer"] = layer
                    case["input_sha256"] = sha(json.dumps(case, sort_keys=True, separators=(",", ":")).encode())
                    yield case


def number_from_json(v):
    if v == "-0":
        return -0.0
    if v == "max":
        return float.fromhex("0x1.fffffffffffffp+1023")
    return float("nan") if v in (None, "NaN", "undefined") else v


def observation(result):
    minimal = {k: v for k,v in result["result"].items() if k != "stack"}
    return [minimal, result["argument_before"], result["argument_after"], result["original_before"],
            result["original_after"], result["p_before"], result["p_after"]]
