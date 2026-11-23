"""Verify the published research bundle without importing a GeoPandas reader."""
import csv
import itertools
import json
from collections import Counter

from generate import HERE, digest

checks = {}


def load(path):
    return json.loads((HERE / path).read_bytes())


def line_objects(path):
    return [json.loads(line) for line in (HERE / path).read_text().splitlines()]


def require(name, condition):
    checks[name] = bool(condition)


def main():
    manifest = load("manifest.json")
    plan = manifest["research"]
    require("scope seal", digest((HERE / plan["scope_file"]).read_bytes()) == plan["scope_sha256"])
    require("common input seal", digest((HERE / plan["common_input"]).read_bytes()) == plan["common_input_sha256"])
    require("scope and sole dependency", manifest["allowed_paths"] == ["docs/workstreams/research/AF-RES-087/"]
            and manifest["dependencies"] == [{"branch": "work/research-af-res-083",
                        "commit": "f9be0dacdb51603c72f30abd452ce9d349d0ca3b"}])

    with (HERE / "files.csv").open(newline="") as table:
        files = {row["file_id"]: row for row in csv.DictReader(table)}
    require("four intended files", set(files) == set(plan["files"]))
    for ident, row in files.items():
        footer = load(row["footer"])
        output = load(row["writer_log"])
        data = (HERE / row["file"]).read_bytes()
        size = int.from_bytes(data[-8:-4], "little")
        require(f"{ident} same file and footer SHA", digest(data) == row["file_sha256"] == footer["file_sha256"]
                == output["file_sha256"] and digest(data[-8-size:-8]) == row["footer_sha256"]
                == footer["footer_sha256"])
        require(f"{ident} recipe and actual format", row["status"] == "generated"
                and (row["writer_exit"], row["footer_exit"]) == ("0", "0")
                and output["input_sha256"] == plan["common_input_sha256"]
                and output["writer"]["commit"] == plan["geopandas_commits"][row["writer"]]
                and row["schema_version"] == footer["geo"]["version"] == plan["files"][ident]["schema_version"]
                and row["actual_encoding"] == ("polygon/point" if ident == "F4" else "WKB/WKB")
                and footer["geo"]["primary_column"] == "geometry"
                and "bbox" not in [field["name"] for field in footer["arrow_fields"]]
                and all("covering" not in c and "bbox" in c for c in footer["geo"]["columns"].values()))
    pair_diffs = load("evidence/build/footer-differences.json")
    require("three inspected pair differences", set(pair_diffs) == {"F1/F2", "F2/F3", "F3/F4"})
    require("metadata version isolation", {d["path"] for d in pair_diffs["F2/F3"]} ==
            {"/geo/version", "/schema_metadata_sha256/geo", "/schema_metadata_sha256/ARROW:schema"})
    sections = load("evidence/build/data-sections.json")
    require("equal WKB data sections", len({sections[ident]["data_section_sha256"]
                                           for ident in ("F1", "F2", "F3")}) == 1)

    envs = load("environments.json")
    versions = ["python", "platform", "pandas", "numpy", "pyarrow", "shapely",
                "GEOS", "pyproj", "PROJ", "fiona_GDAL", "pyogrio_GDAL"]
    for role, env in envs.items():
        require(f"{role} exact runtime source", env["exit"] == 0 and env["commit"] == plan["geopandas_commits"][role]
                and env["geopandas_version"] == env["distribution_version"]
                and env["tracked_source_clean"] and env["import_path"].startswith(env["checkout"] + "/"))
    require("matched runtime dependencies", all(envs["O"][key] == envs["N"][key] for key in versions)
            and [row for row in envs["O"]["installed"] if row[0] != "geopandas"] ==
                [row for row in envs["N"]["installed"] if row[0] != "geopandas"])

    runs = line_objects("runs.jsonl")
    combos = set(itertools.product(plan["files"], plan["readers"], range(1, 3)))
    require("original 16 requested slots", len(runs) == 16 and
            {(r["file_id"], r["role"], r["repeat"]) for r in runs} == combos)
    require("16 distinct processes", len({r["pid"] for r in runs}) == 16)
    require("reader actual bytes equal writer output in every slot", all(
        r["source_bytes_sha256"] == files[r["file_id"]]["file_sha256"] == r["expected_file_sha256"]
        and r["reader"]["commit"] == plan["geopandas_commits"][r["role"]]
        and r["reader"]["import_path"] == envs[r["role"]]["import_path"]
        and r["reader"]["arrow_source_sha256"] == envs[r["role"]]["arrow_source_sha256"]
        for r in runs
    ))
    outcome = Counter(r["outcome"] for r in runs)
    require("14 preserved, two explicit rejections", outcome == {"preserved": 14, "explicit_rejection": 2})
    require("explicit rejects only on O F4", all(
        (r["file_id"], r["role"], r["process_exit"], r["exception"]) ==
        ("F4", "O", 20, {"type": "ValueError", "message": "Only WKB geometry encoding is supported"})
        and r["semantic_spatial"] is None and r["strict_attribute_schema"] is None
        for r in runs if r["outcome"] == "explicit_rejection"
    ))
    fixed = load("fixtures/input.json")
    successes = [r for r in runs if r["process_exit"] == 0]
    require("all successes satisfy both", len(successes) == 14 and all(
        r["semantic_spatial"] and r["strict_attribute_schema"] and r["both_contracts"]
        and r["columns"] == fixed["columns"] and r["active_geometry"] == fixed["active_geometry"]
        and r["feature_ids"] == [row["feature_id"] for row in fixed["rows"]]
        and all(all(check.values()) for check in r["attribute_checks"].values())
        and all(g["crs"]["equals"] and g["crs"]["same_xy"] and
                all(h["same_type_dimension"] and h["same_normalized_xy"] for h in g["rows"])
                for g in r["geometry"].values()) for r in successes
    ))
    comparable = ("outcome", "process_exit", "exception", "geometry", "attributes", "columns",
                  "input_physical_schema", "warnings", "semantic_spatial", "strict_attribute_schema")
    require("both repeats agree for each cell", all(
        len([r for r in runs if r["file_id"] == f and r["role"] == role]) == 2 and
        len({json.dumps([r.get(key) for key in comparable], sort_keys=True)
             for r in runs if r["file_id"] == f and r["role"] == role}) == 1
        for f in plan["files"] for role in plan["readers"]
    ))

    upstream = load("evidence/upstream/receipts.json")
    require("48 original selected pytest passes", sum(x["selected"] for x in upstream.values()) == 48
            and all(x["exit"] == 0 and all(t["outcome"] == "passed" for t in x["cases"])
                    for x in upstream.values()))
    original_fixtures = load("evidence/upstream/fixture-fingerprints.json")["fixtures"]
    require("12 official fixture byte matches", sum(f["spec_tag_source_same_bytes"] is True
                                                    for f in original_fixtures) == 12)

    def aux(name):
        return load(f"evidence/auxiliary/{name}.json")

    require("plain table reads the actual F4 bytes", aux("A-pyarrow")["exit"] == 0
            and aux("A-pyarrow")["stdout"]["source_bytes_sha256"] == files["F4"]["file_sha256"]
            and not aux("A-pyarrow")["stdout"]["semantic_spatial"])
    require("one changed cell detected by both", all(
        r["semantic_spatial"] and not r["strict_attribute_schema"]
        and not r["strict_except_additional_attributes"]
        and r["attributes"]["score"]["values"] == [8, None] for r in aux("B-cell")
    ))
    require("null and EMPTY are independent", all(
        r["stdout"]["arrow_validity"] == [True, False, True]
        and r["stdout"]["state_and_coordinates_equal"] for r in aux("C-WKB") + aux("C-native")[1:]
    ) and aux("C-native")[0]["exit"] == 20)
    require("missing and null CRS give different results", all(
        r["semantic_spatial"] and not r["geometry"]["probe"]["crs"]["equals"]
        and r["geometry"]["probe"]["crs"]["equals_ignore_axis"] for r in aux("D-missing-crs")
    ) and all(not r["semantic_spatial"] and r["geometry"]["probe"]["crs"]["observed"] is None
              for r in aux("D-null-crs")))
    require("one new column accepted only under relaxed policy", all(
        r["semantic_spatial"] and not r["strict_attribute_schema"]
        and r["strict_except_additional_attributes"] for r in aux("E-added")
    ))
    require("removed pandas metadata loses dtype without geometry loss", all(
        r["process_exit"] == 0 and r["semantic_spatial"] and not r["strict_attribute_schema"]
        and r["attributes"]["score"]["pandas"] == "float64" and r["attributes"]["score"]["arrow"] == "int16"
        for r in aux("F-no-pandas-meta")
    ))
    require("mixed native geometry type differs despite equal topology", all(
        r["types_equal"] for r in aux("G-WKB")
    ) and aux("G-native")[0]["exit"] == 20 and not aux("G-native")[1]["types_equal"]
        and aux("G-native")[1]["topology_equal"] == [True, True])
    for name, rec in (aux("build")["stdout"] | aux("G-write")["files"]).items():
        require(f"auxiliary SHA {name}", digest((HERE / "fixtures/auxiliary" / f"{name}.parquet").read_bytes())
                == rec["sha256"])

    ledger = line_objects("sources.jsonl")
    counted = [row for row in ledger if row["counted"]]
    groups = {row["independent_id"] for row in counted}
    urls = {row["url"].split("#")[0] for row in counted}
    tag_minima = {"external_gis_consumer": 6, "gis_counterevidence": 4,
                  "image_actual_case": 2, "pdf_actual_case": 2}
    thematic_counts = {tag: len({row["independent_id"] for row in counted if tag in row["qualifiers"]})
                       for tag in tag_minima}
    required = ["id", "independent_id", "kind", "url", "version_or_locator", "read_at_utc",
                "questions", "case_id", "observed_by", "confirmed", "effect", "limit"]
    require("complete source notes and unique IDs", len({row["id"] for row in ledger}) == len(ledger)
            and all(all(row.get(k) for k in required) for row in ledger))
    require("source minima and dedup", len(urls) >= 24 and len(groups) >= 20
            and all(thematic_counts[k] >= minimum for k, minimum in tag_minima.items()))
    pdf = load("evidence/other/pdf-tag-order.json")["cases"]
    require("PDF same version, distinct logical order", [c["layout_tag_order_match"] for c in pdf] == [True, False]
            and pdf[0]["document_properties"] == pdf[1]["document_properties"])
    report = (HERE / "RESULT.md").read_text()
    require("ordered mandatory tables and 3 closing limitations", report.startswith("## 표 1")
            and report.index("## 표 2") < report.index("## 표 3") < report.index("### 분모")
            and len([ln for ln in report.split("## 주요 약점과 판단을 바꿀 조사 3건")[1].splitlines()
                     if ln[:3] in ("1. ", "2. ", "3. ")]) == 3)

    print(json.dumps({
        "checks": len(checks), "failed": [k for k, ok in checks.items() if not ok],
        "files": len(files), "matrix_runs": len(runs), "outcomes": outcome,
        "upstream": sum(t["selected"] for t in upstream.values()),
        "source_rows": len(ledger), "direct_rows": len(counted), "source_urls": len(urls),
        "independent_units": len(groups), "qualifiers": thematic_counts,
    }, ensure_ascii=False, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
