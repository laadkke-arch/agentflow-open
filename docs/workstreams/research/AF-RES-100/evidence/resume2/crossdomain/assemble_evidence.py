#!/usr/bin/env python3
"""Assemble cross-domain evidence metadata from frozen, inspected bodies."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKSTREAM = HERE.parents[2]
REPO = HERE.parents[6]

# Source lines are 1-based inclusive. Character and byte intervals are zero-based,
# half-open over the unchanged UTF-8 response bodies.
SECTIONS = {
    "gdal-warp-doc": [
        (181, 196, "-vshift / -novshift", "The explicit switches force or disable vertical shifting; -novshift replaced the older option name.", "These options alone do not supply grid data."),
        (624, 652, "Vertical transformation", "Automatic vertical transformation requires a qualifying vertical/3D CRS and one raster band; geoid grids may be required; units can also affect values.", "This explains the automatic gate and flags the grid dependency, but does not give PROJ's resource search order or @ optional-grid contract."),
    ],
    "gdal-warp-lib-tests": [
        (1865, 1879, "gdalwarp_135_grid_gtx", "Upstream creates a 3-by-3 GTX grid in WGS84 filled with 20.", "Synthetic constant data, not a real geoid model."),
        (1899, 1906, "gdalwarp_135_src_ds", "Upstream creates a one-pixel, one-band MEM raster filled with 100 and specifies its geotransform.", "The fixture's default band is byte data; no multi-band fixture is asserted in this section."),
        (1923, 1935, "test_gdalwarp_lib_135", "With the fixture grid as a source geoid correction and EPSG:4979 as target, upstream asserts 120.", "A static upstream assertion, not evidence that this pinned test was executed here."),
        (2091, 2114, "test_gdalwarp_lib_135j / 135k", "Upstream accepts optional missing @i_dont_exist.tif in forward and inverse paths and asserts unchanged value 100.", "Optional absence is not a successful geoid correction; this does not assert mandatory-grid failure."),
    ],
    "gdal-warp-source": [
        (619, 667, "MustApplyVerticalShift", "The PROJ-based implementation checks one raster band or explicit bVShift plus vertical axes, and rejects identical CRSs.", "Implementation evidence is conditional on this compilation branch; the two-band local probe is an adaptation, not an upstream multi-band test."),
    ],
    "proj-vgridshift-doc": [
        (23, 45, "Vertical grid shift overview", "Loaded grids determine height offsets; @ makes a missing grid optional and list order sets precedence; GTX and GeoTIFF are supported.", "Does not establish that any particular installed grid exists or covers a real coordinate."),
        (102, 132, "+grids and +multiplier", "The required grids parameter accepts an optional @ prefix; the multiplier controls offset direction and units, with documented default -1.", "The GDAL source-CRS forward result must not be inferred by blindly applying the default vgridshift sign outside its coordinate-operation direction."),
    ],
    "proj-resource-doc": [
        (19, 82, "Where are PROJ resource files looked for?", "Explicit paths, callbacks, configured search paths, user directories, PROJ_DATA and installation/current directories participate in resource lookup; enabled networking can try remote grids.", "Build options and API overrides affect search order; this study kept networking off and supplied an explicit local fixture path."),
    ],
    "sphinx-inheritance-doc": [
        (11, 42, "inheritance-diagram directive", "The directive takes module/class names, traverses bases, delegates rendering to Graphviz, and supports parts, private-bases and caption.", "Directive semantics do not establish availability of the native renderer or support for a requested image format."),
    ],
    "sphinx-inheritance-tests": [
        (156, 203, "test_inheritance_diagram_png_html", "The Graphviz-gated HTML fixture expects a PNG img, the Test Foo! caption, and valid absolute/relative links.", "The inventory is constructed by the test; this is an expected assertion, not an observed local build."),
        (206, 262, "test_inheritance_diagram_svg_html", "The same fixture with graphviz_output_format=svg expects SVG object markup and verifies links in the generated SVG files.", "A found executable is a prerequisite; these assertions were not run locally because Sphinx/test dependencies are absent."),
    ],
    "sphinx-fixture-conf": [(1, 6, "Fixture configuration", "The fixture adds the current directory to Python import search and enables inheritance_diagram and intersphinx.", "Working-directory/import assumptions must be preserved when reconstructing the fixture.")],
    "sphinx-fixture-index": [(1, 18, "Fixture index", "The input contains test.Foo diagrams, the Test Foo! caption, local class targets, and an external.other.Bob diagram.", "The referenced classes and additional documents are separate fixture files, also frozen here.")],
    "sphinx-fixture-classes": [(1, 22, "Fixture class definitions", "Foo, DocHere, DocSubDir1 and DocSubDir2 form the inspected class chain; DocMainLevel and Alice are also defined.", "These Python classes are fixture inputs, not a standalone rendering implementation.")],
    "sphinx-testing-fixtures": [(224, 239, "if_graphviz_found", "The upstream gate invokes configured graphviz_dot with -V and skips on missing command/OSError.", "check=False means this gate alone does not require return code zero or prove a renderer can produce SVG/PNG.")],
    "sphinx-inheritance-source": [
        (414, 442, "HTML inheritance-diagram visitor", "The visitor generates DOT and delegates HTML rendering through render_dot_html.", "The generic Graphviz extension implementation was intentionally not read."),
        (480, 494, "setup", "Enabling inheritance_diagram loads the Graphviz extension and registers the directive and builders.", "Loading an extension does not itself establish installation of a native dot executable."),
    ],
    "graphviz-cli-pinned": [
        (9, 22, "Invocation and stdin", "Graphviz documents dot -Tsvg and reading DOT from standard input.", "The pinned website revision is a documentation revision, not a declared binary release pin."),
        (85, 116, "-T format and -V", "-T selects output format with build-dependent renderer choices; -V emits version information.", "The inspected page is newer than the Sphinx pin; only these displayed flags are used, and the local binary's identity is recorded separately."),
        (154, 166, "-o outfile", "-o writes to a named file and default output goes to stdout.", "This establishes executable I/O semantics, not Sphinx markup or link behavior."),
    ],
    "sphinx-fixture-example-__init__-py": [(1, 1, "Fixture package marker", "The example package marker is part of the complete upstream fixture tree.", "No behavioral assertion follows from this marker.")],
    "sphinx-fixture-example-sphinx-py": [(1, 5, "Fixture example module", "The example.sphinx fixture module defines DummyClass.", "Support input; not needed to infer native renderer availability.")],
    "sphinx-fixture-external-other-py": [(1, 5, "Fixture external class", "external.other.Bob derives from the local Alice class.", "The test supplies a separate synthetic intersphinx inventory.")],
    "sphinx-fixture-subdir-page1-rst": [(1, 9, "Fixture subdirectory page 1", "This page references DocMainLevel and DocSubDir2 diagrams and declares DocSubDir1.", "Only the upstream SVG/PNG tests establish expected hyperlink assertions.")],
    "sphinx-fixture-subdir-page2-rst": [(1, 5, "Fixture subdirectory page 2", "This page declares the DocSubDir2 target.", "Support input, not a runtime observation.")],
}


def main() -> None:
    manifest_rows = []
    for filename in ["fetch-manifest.json", "discovery.json", "fetch-manifest-extra.json", "fetch-manifest-final.json", "fetch-fixture-support.json"]:
        manifest_rows.extend(json.loads((HERE / filename).read_text()))
    by_id = {row["source_id"]: row for row in manifest_rows if row.get("status") == "fetched"}
    lineage = json.loads((HERE / "lineage.json").read_text())
    release_lineage = {row["repository"]: row for row in lineage["release_commits"]}
    path_lineage = {row["source_id"]: row for row in lineage["latest_path_commits"]}
    graphviz_commit = json.loads((WORKSTREAM / "evidence/_cache/resume2-crossdomain/graphviz-cli-commit.json").read_text())
    versions = {"OSGeo/gdal": "3.10.0", "OSGeo/PROJ": "9.5.1", "sphinx-doc/sphinx": "8.1.3", "graphviz/graphviz.gitlab.io": "website revision 51d048c4 (2025-10-29)"}
    docs = {"gdal-warp-doc", "sphinx-inheritance-doc", "proj-resource-doc", "proj-vgridshift-doc", "graphviz-cli-pinned"}
    tests = {"gdal-warp-lib-tests", "sphinx-inheritance-tests"}
    sources = []
    for source_id, definitions in SECTIONS.items():
        row = by_id[source_id].copy()
        if source_id == "gdal-warp-lib-tests":
            row.update(repository="OSGeo/gdal", pin="35a44cc570cdf4dbd55611e4bd61da76e56bc221", path="autotest/utilities/test_gdalwarp_lib.py")
        elif source_id == "sphinx-testing-fixtures":
            row.update(repository="sphinx-doc/sphinx", pin="a1510de4777eaa2e569435f95b05f6f3293d7035", path="sphinx/testing/fixtures.py")
        elif source_id == "graphviz-cli-pinned":
            row.update(repository="graphviz/graphviz.gitlab.io", pin="51d048c433e5a80ab51915876b695c971544fe54", path="content/en/docs/cli/_index.md")
        cache = REPO / row["local_cache"]
        body = cache.read_bytes()
        assert hashlib.sha256(body).hexdigest() == row["sha256"]
        text = body.decode("utf-8")
        lines = text.splitlines(keepends=True)
        sections = []
        for start, end, section, claim, limit in definitions:
            assert 1 <= start <= end <= len(lines)
            prefix = "".join(lines[: start - 1])
            excerpt = "".join(lines[start - 1 : end])
            sections.append({"section": section, "line_start": start, "line_end": end, "line_convention": "1-based inclusive", "char_start": len(prefix), "char_end": len(prefix) + len(excerpt), "byte_start": len(prefix.encode()), "byte_end": len(prefix.encode()) + len(excerpt.encode()), "excerpt_sha256": hashlib.sha256(excerpt.encode()).hexdigest(), "claim": claim, "limit": limit})
        if row["repository"] == "graphviz/graphviz.gitlab.io":
            canonical = f"https://gitlab.com/{row['repository']}/-/blob/{row['pin']}/{row['path']}"
            authors = {"project": "Official Graphviz documentation", "revision_author": graphviz_commit["author_name"], "revision_authored_utc": graphviz_commit["authored_date"], "revision_committer": graphviz_commit["committer_name"], "revision_message": graphviz_commit["message"], "revision_url": graphviz_commit["web_url"], "caveat": "Latest document revision author; not a claim of sole or original authorship."}
        else:
            canonical = f"https://github.com/{row['repository']}/blob/{row['pin']}/{row['path']}"
            authors = {"project": row["repository"], "release_commit": release_lineage[row["repository"]], "latest_path_commit": path_lineage.get(source_id), "caveat": "Release and latest-path lineage only; not sole/original authorship or independent replication."}
            if source_id == "gdal-warp-lib-tests":
                authors["file_header_credits"] = ["Faza Mahamood", "Even Rouault"]
        role = "official_documentation" if source_id in docs else "upstream_test_program" if source_id in tests else "upstream_fixture_input" if source_id.startswith("sphinx-fixture-") else "implementation_or_test_infrastructure"
        sources.append({"source_id": source_id, "role": role, "official_repository": row["repository"], "version": versions[row["repository"]], "pin": row["pin"], "path": row["path"], "url": canonical, "raw_url": row["url"], "fetched_utc": row["fetched_utc"], "sha256": row["sha256"], "bytes": len(body), "line_count": len(lines), "git_blob_sha1_computed_from_body": hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest(), "upstream_git_blob_sha": row.get("upstream_git_blob_sha"), "cached_body": str(cache.relative_to(WORKSTREAM)), "author_lineage": authors, "sections": sections, "runtime_evidence": False})
        source_record = sources[-1]
        scientific = row["repository"] in {"OSGeo/gdal", "OSGeo/PROJ"}
        count_minimum = source_id in docs or source_id in tests
        if source_id in docs:
            count_group = "crossdomain_official_docs"
            duplicate_reason = None
        elif source_id in tests:
            count_group = "crossdomain_fixtures"
            duplicate_reason = None
        elif source_id == "sphinx-testing-fixtures":
            count_group = "crossdomain_fixtures"
            duplicate_reason = "Common sphinx/testing/fixtures.py gate was also read in AF-RES-096, as disclosed by the coordinator. It is reused supporting infrastructure for the Sphinx inheritance-diagram family, not new minimum-count material or a new example."
        elif source_id.startswith("sphinx-fixture-"):
            count_group = "crossdomain_fixtures"
            duplicate_reason = "Supporting input or gate of the one Sphinx inheritance-diagram fixture family already counted by sphinx-inheritance-tests; not an additional minimum unit."
        else:
            count_group = "crossdomain_support"
            duplicate_reason = "Implementation support for the already counted family; neither a separate official documentation page nor a separate upstream fixture."
        source_record.update({
            "q_numbers": ["Q7"],
            "case_id": "CD-GDAL-WARP-VSHIFT" if scientific else "CD-SPHINX-INHERITANCE-DOT",
            "direct_url": "https://graphviz.org/doc/info/command.html" if source_id == "graphviz-cli-pinned" else canonical,
            "fixed_url": canonical,
            "checked_utc": row["fetched_utc"],
            "author_publisher": "Official " + row["repository"] + " project; named revision/file credits are preserved in lineage",
            "lineage": authors,
            "exact_section_payload": [
                {"section": section["section"], "line_start": section["line_start"], "line_end": section["line_end"], "char_start": section["char_start"], "char_end": section["char_end"], "byte_start": section["byte_start"], "byte_end": section["byte_end"], "excerpt_sha256": section["excerpt_sha256"], "fixed_url": canonical}
                for section in sections
            ],
            "body_sha256": row["sha256"],
            "confirmed": [section["claim"] for section in sections],
            "verified_body": True,
            "confirmation_scope": "Original source body and precise sections inspected; no implication of successful target execution.",
            "supports": [section["claim"] for section in sections],
            "limits": [section["limit"] for section in sections] + ["Shared project/author lineage is not statistical independence; this is Q7 context only."],
            "count_minimum": count_minimum,
            "count_group": count_group,
            "duplicate_reason": duplicate_reason,
            "research_phase": "resume2_crossdomain_context",
        })
        if source_id == "sphinx-testing-fixtures":
            source_record.update({
                "prior_use": {"workstream": "AF-RES-096", "path": "sphinx/testing/fixtures.py", "basis": "Coordinator disclosed prior use after this review; AF-RES-096 files were not reopened for this correction."},
                "novelty_status": "reused_common_test_gate",
                "new_material_minimum_counted": False,
                "new_example_counted": False,
            })
            source_record["limits"].append("This common gate was previously read in AF-RES-096; only the inheritance-diagram main document/fixture pair is presented as the different example.")
    (HERE / "sources.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in sources))

    fixture_inputs = [row["source_id"] for row in sources if row["role"] == "upstream_fixture_input"]
    fixtures = {
        "scope": "Q7 cross-domain context only; fixed named families, not recruited questions or reader wins",
        "counts_as_recruited8": False,
        "counts_as_primary_win": False,
        "selection": "Coordinator specified GDAL warp vertical-shift single-band/multi-band and Sphinx inheritance-diagram families before this inspection.",
        "evidence_counts": {"official_documentation_files": len(docs), "distinct_upstream_test_programs": len(tests), "named_crossdomain_families": 2},
        "families": [
            {
                "family_id": "CD-GDAL-WARP-VSHIFT",
                "domain": "Scientific geospatial raster transformation",
                "fixed_upstream_version": "GDAL 3.10.0 at 35a44cc570cdf4dbd55611e4bd61da76e56bc221",
                "adjacent_version": "PROJ 9.5.1 at 41f79ccfe107d3951dac6826f289b55d17cc3b81",
                "upstream_test_source": "gdal-warp-lib-tests",
                "upstream_fixture_names": ["gdalwarp_135_grid_gtx", "gdalwarp_135_src_ds"],
                "upstream_test_names": ["test_gdalwarp_lib_135", "test_gdalwarp_lib_135j", "test_gdalwarp_lib_135k"],
                "primary_document_sufficient_for": "Explaining when automatic vertical raster-value shifting applies, including the single-band requirement and -novshift override.",
                "boundary_condition": "Actually use a grid with specified location and absence semantics; distinguish a completed process from a completed height correction.",
                "adjacent_documentation_needed_for": "Exact PROJ resource lookup and @ optional-grid behavior. The primary GDAL page already flags the dependency, so this is narrow completion of the operational contract, not proof that neighboring documentation is universally indispensable.",
                "documented_or_source_expected": [
                    {"assertion": "one-band 100 with constant +20 fixture grid becomes 120", "basis": "upstream assertion", "source": "gdal-warp-lib-tests", "lines": [1923, 1935]},
                    {"assertion": "optional missing forward/inverse grid leaves 100 unchanged", "basis": "upstream assertions", "source": "gdal-warp-lib-tests", "lines": [2091, 2114]},
                    {"assertion": "automatic two-band case does not apply the height shift", "basis": "document/source implication, study adaptation", "sources": ["gdal-warp-doc", "gdal-warp-source"]},
                ],
                "actual_runtime": {"file": "gdal-runtime.json", "kind": "five-case local adaptation", "gdal": "3.10.3", "proj": "9.6.0", "network": "OFF", "pinned_upstream_suite_executed": False, "version_equivalence_claimed": False},
                "limitations": ["Synthetic uniform grid does not validate real geoid correctness, grid coverage, datum selection or scientific accuracy.", "Two-band, -novshift and mandatory-missing cases are study-authored variants, not claimed upstream tests.", "No dependency install, paid service, credentials, remote grid acquisition or full upstream test suite."],
                "reproduction_commands": ["/usr/bin/python3 -B docs/workstreams/research/AF-RES-100/evidence/resume2/crossdomain/run_gdal_fixture.py", "python -B docs/workstreams/research/AF-RES-100/evidence/resume2/crossdomain/reproduce_sources.py --source gdal-warp-lib-tests"],
                "optional_upstream_command_not_run": {"cwd_requirement": "An already prepared GDAL source tree at the specified pin with test dependencies", "command": "python -m pytest autotest/utilities/test_gdalwarp_lib.py::test_gdalwarp_lib_135 autotest/utilities/test_gdalwarp_lib.py::test_gdalwarp_lib_135j autotest/utilities/test_gdalwarp_lib.py::test_gdalwarp_lib_135k"},
            },
            {
                "family_id": "CD-SPHINX-INHERITANCE-DOT",
                "domain": "Document generation with a native external executable",
                "fixed_upstream_version": "Sphinx 8.1.3 at a1510de4777eaa2e569435f95b05f6f3293d7035",
                "adjacent_document_pin": "Official Graphviz CLI website revision 51d048c433e5a80ab51915876b695c971544fe54 (not a Graphviz binary pin)",
                "upstream_test_source": "sphinx-inheritance-tests",
                "upstream_test_names": ["test_inheritance_diagram_png_html", "test_inheritance_diagram_svg_html"],
                "fixture_root": "tests/roots/test-ext-inheritance_diagram",
                "fixture_input_source_ids": fixture_inputs,
                "primary_document_sufficient_for": "Specifying class inheritance traversal and the caption option on an inheritance-diagram directive.",
                "boundary_condition": "Produce the PNG/SVG image and corresponding HTML; a loadable Python extension alone does not establish native renderer availability.",
                "adjacent_documentation_needed_for": "Concrete executable/version and output-format probes such as dot -V and dot -Tsvg, while the exact integration is evidenced by Sphinx's inheritance source and fixture gate.",
                "documented_or_source_expected": [
                    {"assertion": "PNG img markup and Test Foo! caption, with links resolving", "basis": "upstream assertion", "source": "sphinx-inheritance-tests", "lines": [156, 203]},
                    {"assertion": "SVG object markup and generated SVG links resolving with graphviz_output_format=svg", "basis": "upstream assertion", "source": "sphinx-inheritance-tests", "lines": [206, 262]},
                    {"assertion": "tests skip when configured native dot cannot be started", "basis": "upstream test gate", "source": "sphinx-testing-fixtures", "lines": [224, 239]},
                ],
                "actual_runtime": {"file": "graphviz-runtime.json", "kind": "external-renderer-only probe", "dot": "2.42.4", "svg_returncode": 0, "sphinx_fixture_executed": False, "blocker": "Sphinx, docutils and pytest are absent in the inspected Python environments."},
                "limitations": ["dot -V uses check=False in the upstream gate and does not itself prove format support.", "The local SVG uses a manually supplied graph from the fixture class chain, not Sphinx-generated DOT; captions, HTML, inventory and hyperlinks remain unexecuted.", "The Graphviz documentation revision is later than the pinned Sphinx version; no complete cross-version equivalence is asserted."],
                "reproduction_commands": ["python -B docs/workstreams/research/AF-RES-100/evidence/resume2/crossdomain/run_graphviz_probe.py", "python -B docs/workstreams/research/AF-RES-100/evidence/resume2/crossdomain/reproduce_sources.py --source sphinx-inheritance-tests"],
                "optional_upstream_command_not_run": {"cwd_requirement": "An already prepared Sphinx source tree at the specified pin with test dependencies and a usable dot executable", "command": "python -m pytest tests/test_extensions/test_ext_inheritance_diagram.py::test_inheritance_diagram_png_html tests/test_extensions/test_ext_inheritance_diagram.py::test_inheritance_diagram_svg_html"},
            },
        ],
        "prior_use_disclosures": [{"source_id": "sphinx-testing-fixtures", "path": "sphinx/testing/fixtures.py", "prior_workstream": "AF-RES-096", "role": "reused common test gate", "counted_as_new_minimum_material": False, "counted_as_new_example": False, "basis": "Coordinator disclosure; no AF-RES-096 source reinspection was needed."}],
        "independence_limit": "Docs, source and tests share project and author lineage; these are traceable official examples, not independent replications or an estimate of effect size. The common Sphinx test gate was also used in AF-RES-096 and is not counted as new material or a new example.",
    }
    (HERE / "fixtures.json").write_text(json.dumps(fixtures, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"sources": len(sources), "official_docs": len(docs), "upstream_test_programs": len(tests), "fixture_input_files": len(fixture_inputs), "source_hashes_verified": True, "section_offsets_computed": True}))


if __name__ == "__main__":
    main()
