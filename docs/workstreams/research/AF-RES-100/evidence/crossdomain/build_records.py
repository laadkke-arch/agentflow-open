"""Rebuild the cross-domain source ledger from fixed acquisition receipts.

No upstream code is executed. All offsets refer to raw UTF-8 decoded without
newline conversion. Lines are one-based inclusive; chars/bytes are zero-based
half-open. This ledger concerns post-seal designated examples, never the 8-case
recruitment denominator or the frozen packet judgments.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
ANNOTATIONS = {
    "XG1": {
        "case_id": "XD-GDAL-VSHIFT", "group": "crossdomain_doc", "count": True,
        "ranges": [(181, 196, "vshift/novshift"), (623, 654, "Vertical transformation: eligibility, grids and units"), (790, 796, "EGM96-to-ellipsoidal documentation command")],
        "confirmed": ["Automatic vertical correction requires an explicit vertical CRS and a single-band raster; -vshift can force and -novshift disables it.", "The main manual itself states that geoid grids may need local installation or PROJ networking.", "Band unit takes priority over source-CRS vertical unit; target unit and MULT_FACTOR_VERTICAL_SHIFT affect values."],
        "supports": ["Main explanation suffices for the documented automatic-trigger and unit-priority rule.", "A command spelling alone does not establish that the geoid grid or the input DEM exists."],
        "limits": ["No supplied real in_dem.tif; the documentation command was not executed.", "The selected original fixtures are single-band, so they are not an executed multiband-negative control."]},
    "XG2": {
        "case_id": "XD-GDAL-VSHIFT", "group": "crossdomain_fixture", "count": True,
        "ranges": [(1865, 1920, "Original generated GTX and MEM fixtures"), (1923, 2000, "135/135a/b/c/d forward, reverse and two-grid assertions"), (2003, 2046, "135e/f/g no-grid, same-grid and VRT assertions"), (2049, 2088, "135h/i output units and VRT reopen"), (2117, 2191, "135m/n/o/p band-unit priority assertions"), (2222, 2249, "135s intended empty-grid test and literal filename anomaly")],
        "confirmed": ["Original upstream fixtures create 3x3 Float32 GTX grids filled with 20 and 5; original MEM source is one pixel of 100.", "Assertions expect forward 120, reverse 80, source20/target5 115, and identical source/target grids 100; these are upstream expectations, not observations from this study.", "135h expects 115/(1200/3937) in US survey feet; 135n/o return 120 after source-band feet conversion.", "135s constructs empty_grid_gtx, but srcSRS at line 2247 contains the literal {empty_grid_gtx} without f-string interpolation; only a generic exception is asserted for PROJ>=8."],
        "supports": ["The same tool boundary can add, subtract, or make no change depending on direction and both resource inputs.", "An upstream test name or passing generic-exception assertion does not establish that its intended grid payload was actually supplied."],
        "limits": ["No upstream tests executed; no real-world geoid accuracy or data coverage established.", "Synthetic constants are upstream-owned fixture inputs, not investigator substitutes for missing natural inputs.", "The 135s anomaly is established in source; the actual runtime exception cause remains unmeasured."]},
    "XG3": {
        "case_id": "XD-GDAL-VSHIFT", "group": "crossdomain_doc", "count": True,
        "ranges": [(1, 45, "vgridshift dimensions, grid names and file formats"), (102, 133, "Required grids and multiplier equation")],
        "confirmed": ["vgridshift consumes vertical corrections from named grids, with GTX/GeoTIFF support.", "The low-level relation is targetZ=sourceZ+multiplier*gridValue; the product must be metres and the default multiplier is -1."],
        "supports": ["Resource format, sign, units and direction are necessary details when operating the adjacent transformation directly.", "The GDAL forward fixture cannot be interpreted by simply adding the low-level default multiplier without preserving the wrapper's operation direction."],
        "limits": ["This is a PROJ operator manual, not proof of the exact internal GDAL-selected pipeline.", "The actual egm96_15.gtx dataset was not opened or downloaded.", "The optional-grid example was read but is not promoted as a new case because AF-RES-096 already used optional-grid reasoning."]},
    "XG4": {
        "case_id": "XD-GDAL-VSHIFT", "group": "crossdomain_doc", "count": True,
        "ranges": [(17, 82, "Resource lookup order and network enablement"), (126, 149, "Grid formats and proj-data distribution/installation")],
        "confirmed": ["Explicit filename location, file-finder callback and context search paths precede normal locations; callbacks/search paths can prevent later lookup stages.", "PROJ_DATA provides resource directories; runtime layout and a build option alter fallback order; networking may use CDN resources.", "The publisher identifies PROJ-data/PROJ CDN and installation through projsync or unpacking a package into PROJ_DATA."],
        "supports": ["For an actually missing geoid resource, the selected gdalwarp paragraph does not contain enough installation/lookup detail; this adjacent publisher section supplies the missing operational conditions."],
        "limits": ["No package archive, real geoid payload, network transaction or particular user's search path was verified.", "A known installation recipe is not proof that a named grid covers the user's coordinates or is currently installed."]},
    "XS1": {
        "case_id": "XD-SPHINX-INHERITANCE", "group": "crossdomain_doc", "count": True,
        "ranges": [(11, 40, "Extension, graphviz delegation and parts"), (51, 98, "top-classes and full-module known issue"), (144, 174, "Graph/node attributes and aliases")],
        "confirmed": ["The extension obtains Python inheritance and renders through sphinx.ext.graphviz.", "With full-module input, top-classes B/C may leave A as a standalone node; the document recommends listing the desired descendant classes instead.", "parts affects display names and inheritance_alias renames class labels."],
        "supports": ["Main-tool documentation can fully explain a boundary-looking diagram defect; adjacent renderer documentation does not change Python class seeding."],
        "limits": ["The documented known issue is not a natural recruited request or measured A/B outcome.", "No resulting image was rendered in this study."]},
    "XS2": {
        "case_id": "XD-SPHINX-INHERITANCE", "group": "crossdomain_fixture", "count": True,
        "ranges": [(18, 144, "Original top-class graph test and membership assertions"), (157, 205, "Original PNG inheritance builder assertions"), (206, 263, "Original SVG inheritance builder assertions"), (266, 319, "LaTeX and alias assertions")],
        "confirmed": ["test_inheritance_diagram builds testroot inheritance and captures InheritanceDiagram.run output.", "For explicit descendant input the allowed tuple list has five classes and omits A; for whole-module input it has six and includes A.", "These checks iterate actual class_info and assert membership, without an exact-set/cardinality assertion; they do not guarantee all listed classes are present.", "Build tests are gated by if_graphviz_found; the SVG case uses graphviz_output_format='svg' and reads emitted files/link targets."],
        "supports": ["Original fixture intent matches the main-doc top-classes distinction.", "A test gate and listed output assertions cannot prove execution or renderer availability on an untested environment."],
        "limits": ["No tests executed; no Graphviz version/plugins pinned by these tests.", "The membership-only test is weaker than full graph equality; source/fixture/doc inspection supplies context, not a measured repair.", "PNG/SVG linkage checks are supporting boundary evidence, not the new nominated case; AF-RES-096 already examined general graphviz format/path fixtures."]},
    "XS3": {
        "case_id": "XD-SPHINX-INHERITANCE", "group": "crossdomain_fixture", "count": False,
        "ranges": [(1, 18, "Original ext-inheritance_diagram index fixture")],
        "confirmed": ["The upstream fixture contains test.Foo, test.DocSubDir2 and external.other.Bob diagrams with local class targets and a caption."],
        "supports": ["Identifies actual inputs of the supporting inheritance rendering test; it is not the top-classes fixture."],
        "limits": ["Other Python modules/configuration are needed for a complete build; this file alone is not executable input."],
        "duplicate_reason": "Distinct file read for provenance, conservatively excluded from the minimum because the nominated case uses the separate test-inheritance fixtures."},
    "XS4": {
        "case_id": "XD-SPHINX-INHERITANCE", "group": "crossdomain_doc", "count": False,
        "ranges": [(100, 130, "import_classes module/class selection"), (143, 222, "Class seeding and traversal stop"), (411, 442, "HTML delegate to render_dot_html"), (479, 494, "graphviz extension setup")],
        "confirmed": ["Module inputs produce all classes defined by the module; _class_info seeds each supplied class and stops ancestor recursion at top_classes.", "HTML output creates DOT and delegates to render_dot_html; setup enables sphinx.ext.graphviz."],
        "supports": ["Explains why a root class already seeded by a module survives traversal stopping.", "Separates Python graph construction from the external image rendering boundary."],
        "limits": ["Static implementation review, not runtime trace.", "This file is implementation rather than the required official-document slot, so it is supplementary in the lower-bound count."],
        "duplicate_reason": "Unique implementation read, but not used to satisfy the official-document quota."},
    "XS5": {
        "case_id": "XD-SPHINX-INHERITANCE", "group": "crossdomain_fixture", "count": True,
        "ranges": [(1, 35, "Original A/B/C/D/E/F class fixture")],
        "confirmed": ["Original hierarchy defines B(A), C(A), D(B,C), E(B), F(C); there are six classes A-F."],
        "supports": ["The known-issue example uses an explicit, upstream-owned multiple-inheritance input instead of researcher-supplied stand-ins."],
        "limits": ["A tiny synthetic fixture is not evidence of real user frequency or independent replication."]},
    "XS6": {
        "case_id": "XD-SPHINX-INHERITANCE", "group": "crossdomain_fixture", "count": True,
        "ranges": [(1, 9, "Original explicit-descendants RST fixture")],
        "confirmed": ["Directive supplies dummy.test.F, dummy.test.D, dummy.test.E and top-classes dummy.test.B, dummy.test.C."],
        "supports": ["Fixes the exact upstream explicit-class input associated with the five-class expected membership list."],
        "limits": ["Shares author/test lineage and class fixture with XS7; two files do not create two independent cases."]},
    "XS7": {
        "case_id": "XD-SPHINX-INHERITANCE", "group": "crossdomain_fixture", "count": True,
        "ranges": [(1, 6, "Original whole-module RST fixture")],
        "confirmed": ["Directive supplies dummy.test and the same top-classes dummy.test.B, dummy.test.C."],
        "supports": ["Holds the top-class option fixed while changing module versus explicit-class input in the original test family."],
        "limits": ["Shares author/test lineage with XS6; not an independently recruited natural request."]},
    "XS8": {
        "case_id": "XD-SPHINX-INHERITANCE", "group": "crossdomain_doc", "count": False,
        "ranges": [(203, 229, "graphviz executable, arguments and HTML output-format configuration")],
        "confirmed": ["Sphinx itself explains graphviz_dot command/full-path selection and -D configuration.", "graphviz_dot_args passes additional arguments and HTML output format is png or svg."],
        "supports": ["Even the external executable boundary is partly explained by the main-tool manual; a second vendor link is not automatically needed for PATH/configuration questions."],
        "limits": ["Does not enumerate actual Graphviz build plugins or prove the local executable works.", "This source family was already used by AF-RES-096; only the configuration subsection supports the new inheritance case here."],
        "duplicate_reason": "Read as a counterexample to forced adjacent links; excluded conservatively from the new cross-domain minimum because it shares the AF-RES-096 graphviz-document lineage."},
    "XV1": {
        "case_id": "XD-SPHINX-INHERITANCE", "group": "crossdomain_doc", "count": True,
        "ranges": [(9, 23, "dot invocation/stdin"), (85, 107, "-T renderer/formatter and actual build availability")],
        "confirmed": ["The publisher describes dot -Tsvg and -Tformat[:renderer[:formatter]].", "Available renderer/formatter combinations depend on the Graphviz build; -Tformat: lists renderers and -v identifies the chosen combination."],
        "supports": ["If the required output depends on a particular renderer or build capability, publisher-level inspection is needed beyond Sphinx's selection of png/svg.", "Selecting an output format in Sphinx cannot prove the corresponding executable/plugin is available."],
        "limits": ["Documentation commit is fixed, but it is not a Graphviz executable release pin and includes newer features outside this analysis.", "No dot invocation or local plugin inventory was executed.", "The current rendered page was used to discover the source pin; only this fixed Markdown section supports the reported claims."]},
    "XV2": {
        "case_id": "XD-SPHINX-INHERITANCE", "group": "crossdomain_doc", "count": False,
        "ranges": [(821, 842, "Current SVG page usage and renderer note (raw HTML lines)")],
        "confirmed": ["Current official SVG page distinguishes svg, compressed svgz, and svg_inline since 10.0.1, and distinguishes Cairo from built-in SVG."],
        "supports": ["Exploratory countercheck: output labels and renderer choices are versioned; they cannot be transplanted into Sphinx 8.1.3 assumptions without checking its interface."],
        "limits": ["Unpinned current web page, so not used for any fixed-version completion judgment or the minimum.", "The example page's output is not a run by this investigator."],
        "duplicate_reason": "Exploratory mutable source; not counted among the fixed primary-source minimum."},
}


def line_span(text, start, end, name):
    lines = text.splitlines(keepends=True)
    assert 1 <= start <= end <= len(lines)
    a = sum(map(len, lines[:start-1])); b = a + sum(map(len, lines[start-1:end]))
    raw = text[a:b].encode("utf-8")
    return {"section": name, "lines_inclusive": [start, end],
            "char_start": a, "char_end": b,
            "byte_start": len(text[:a].encode("utf-8")),
            "byte_end": len(text[:b].encode("utf-8")),
            "span_sha256": hashlib.sha256(raw).hexdigest()}


def main():
    receipts = {r["source_id"]: r for r in map(json.loads, (ROOT/"acquisition-receipts.jsonl").read_text().splitlines())}
    ledger = ROOT/"sources.jsonl"
    previous = {r["source_id"]: r for r in map(json.loads, ledger.read_text().splitlines())} if ledger.exists() else {}
    rows = []
    retained_unpinned = []
    for sid, ann in ANNOTATIONS.items():
        rec = receipts[sid]
        cached = ROOT/rec["cached_body"]
        if not cached.exists() and rec["commit"] is None:
            # A mutable auxiliary page cannot be re-fetched as if it were the old
            # snapshot. Retain its committed historical record, excluded from
            # the count, and disclose that raw bytes were not reverified.
            old = previous[sid]
            assert not old["count_minimum"] and old["body_sha256"] == rec["body_sha256"]
            rows.append(old)
            retained_unpinned.append(sid)
            continue
        raw = cached.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == rec["body_sha256"], sid
        text = raw.decode("utf-8")
        if rec["repo"] == "OSGeo/gdal":
            publisher = "OSGeo GDAL upstream contributors"
            version = "GDAL 3.10.0 / "+rec["commit"]
        elif rec["repo"] == "OSGeo/PROJ":
            publisher = "OSGeo PROJ upstream contributors"
            version = "PROJ 9.5.1 / "+rec["commit"]
        elif rec["repo"] == "sphinx-doc/sphinx":
            publisher = "Sphinx upstream contributors"
            version = "Sphinx 8.1.3 / "+rec["commit"]
        else:
            publisher = "Graphviz project documentation contributors"
            version = "documentation snapshot / "+str(rec["commit"])
        lineage = ("Original upstream test/fixture in the same project tree; not a copied blog/example or an investigator-created replacement. "
                   if ann["group"] == "crossdomain_fixture" else
                   "Publisher-maintained original documentation/source. ")
        lineage += ("GDAL/PROJ vertical raster family; shared documentation/test lineage, no independent case count."
                    if ann["case_id"].startswith("XD-GDAL") else
                    "Sphinx inheritance/Graphviz rendering family; shared documentation/test lineage, no independent case count.")
        row = {
            "source_id": sid, "q_numbers": ["Q6", "Q7"], "case_id": ann["case_id"],
            "direct_url": rec["direct_url"], "fixed_url": rec["fixed_url"],
            "checked_utc": rec["checked_utc"], "author_publisher": publisher,
            "lineage": lineage, "version": version,
            "exact_section_payload": [line_span(text, lo, hi, section) for lo, hi, section in ann["ranges"]],
            "body_sha256": rec["body_sha256"], "git_blob_sha": rec.get("git_blob_sha"),
            "body_bytes": len(raw), "body_chars": len(text),
            "confirmed": ann["confirmed"], "supports": ann["supports"], "limits": ann["limits"],
            "count_minimum": ann["count"], "count_group": ann["group"],
            "duplicate_reason": ann.get("duplicate_reason", "Canonical repository path at one pin counted once; multiple spans and related tests are not additional sources."),
            "research_phase": "post_seal2_crossdomain_designated_examples",
            "seal2_commit": "5d81bcbeb5f1248fc1dd2ce2d825cf6467353673",
            "applies_to_frozen_judgments": False, "natural_recruitment_hits": 0,
            "upstream_executions": 0,
        }
        if sid == "XV1":
            rendered = ROOT/"_cache/graphviz_command_current.html"
            prior_render = previous.get(sid, {}).get("additional_read_locations", [{}])[0].get("cached_render_sha256")
            row["additional_read_locations"] = [{
                "url": "https://graphviz.org/doc/info/command.html",
                "role": "Current published rendering opened to find the fixed original-source link; not counted again and not assumed byte-identical.",
                "cached_render_sha256": hashlib.sha256(rendered.read_bytes()).hexdigest() if rendered.exists() else prior_render,
                "direct_browser_payload_id": "turn256746263view0",
            }]
        if sid == "XV2":
            row["direct_browser_payload_id"] = "turn256746263view1"
        rows.append(row)
    (ROOT/"sources.jsonl").write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in rows))
    summary = {"rows": len(rows), "unique_counted_fixed_files": sum(r["count_minimum"] for r in rows),
               "count_groups": {g: sum(r["count_minimum"] and r["count_group"]==g for r in rows)
                                for g in ("crossdomain_doc", "crossdomain_fixture")},
               "designated_case_families": 2, "natural_recruitment_hits": 0,
               "upstream_tests_executed": 0, "frozen_judgments_changed": 0,
               "retained_unpinned_records_without_raw_reverification": retained_unpinned,
               "offset_convention": "Unicode codepoints and UTF-8 bytes, zero-based half-open; raw line numbers one-based inclusive"}
    (ROOT/"counts.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(summary,ensure_ascii=False))


if __name__ == "__main__":
    main()
