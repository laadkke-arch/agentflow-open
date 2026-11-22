#!/usr/bin/env python3
"""Emit donor-only source metadata from the frozen, locally captured bodies."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[4]
CACHE = BASE / "cache"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(REPO))


def write_jsonl(name: str, rows: list[dict]) -> None:
    (BASE / name).write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8", newline="\n")


FACTS = [
    ("L01", "LIB-01", "library", "Seattle Public Library", "Washington, United States", "Interlibrary Loan", None,
     "Current undated official service page, captured on 2026-11-22.",
     "Explains who may request material, request limits, excluded formats, and ways to submit or check requests.",
     "Standalone public interlibrary-loan procedure; complete substantive body before related-link navigation.",
     ["No publication or revision date is stated; historical availability before capture is unverified.", "The embedded request form itself is not included in the textual policy body."],
     "library_directory_manifest.jsonl", 1),
    ("L02", "LIB-02", "library", "Denver Public Library", "Colorado, United States", "Interlibrary Loan & Purchase Suggestions", None,
     "Current undated official service page, captured on 2026-11-22.",
     "Describes registration, requests, borrowing conditions, renewals, charges, and handling of lost or damaged items.",
     "Standalone public procedure; complete substantive body including the associated purchase-request instructions and contact block.",
     ["No publication or revision date is stated; the HTTP Last-Modified header tracks the response and is not treated as a publication date.", "The combined interlibrary-loan and purchase-request page is counted as one work."],
     "libraries_1_candidate_manifest.jsonl", 1),
    ("L03", "LIB-03", "library", "Multnomah County Library", "Oregon, United States", "Interlibrary loan", None,
     "Current undated official service page, captured on 2026-11-22.",
     "Provides account and borrowing instructions, request status information, charges, renewal conditions, and reasons requests may remain unfilled.",
     "Standalone public procedure; entire account-instructions and FAQ body, stopping before the related-pages navigation.",
     ["No publication or revision date is stated; historical availability before capture is unverified.", "The body includes the publisher's copyright-use restrictions as part of its operating instructions."],
     "libraries_1_candidate_manifest.jsonl", 1),
    ("L04", "LIB-04", "library", "Toronto Public Library", "Ontario, Canada", "Interlibrary Loan Information for Other Libraries", None,
     "Current undated official lending page, read through the official-source web reader on 2026-11-22.",
     "Specifies lending periods, charges, material restrictions, institutional identifiers, and contact information for requesting libraries.",
     "Standalone procedure for institutional borrowers; full web-reader body lines 191–239, with page title and footer excluded.",
     ["Direct HTTP retrieval returned a 202 challenge with an empty policy body; the substantive source is the full official-page web-reader transcript.", "Original policy HTML bytes could not be retained; the reader transcript and its exact derived body are hashed separately.", "No policy publication or revision date is stated; the website software's update date is not used as the policy date."],
     "libraries_1_candidate_manifest.jsonl", 1),
    ("L05", "LIB-05", "library", "Hennepin County Library", "Minnesota, United States", "Interlibrary loan", None,
     "Current undated official MNLINK instructions page, captured on 2026-11-22.",
     "Explains account access, searching and requesting material, handling absent catalogue records, and checking request information.",
     "Standalone patron instructions at the mnlink-instructions URL; complete main body.",
     ["The search returned two pages with the same title; the frozen URL tie-break placed these MNLINK instructions first.", "No publication or revision date is stated; historical availability before capture is unverified."],
     "libraries_2_stats_1_candidate_manifest.jsonl", 2),
    ("L06", "LIB-06", "library", "Vancouver Public Library", "British Columbia, Canada", "Interlibrary Loans for VPL Cardholders", None,
     "Current undated official service page, captured on 2026-11-22; an older fee-change date inside the body is not treated as its revision date.",
     "Sets out requests, material eligibility, costs, pickup arrangements, borrowing periods, and cancellation conditions.",
     "Standalone patron procedure; complete operational FAQ before the separate requesting-libraries navigation card; accordion controls excluded.",
     ["No page publication or revision date is stated; historical availability before capture is unverified.", "The page separately gives an approval estimate and a total-process estimate; both are retained without harmonising them.", "Email text appears obfuscated in the served HTML; the captured source display is retained."],
     "libraries_2_stats_1_candidate_manifest.jsonl", 2),
    ("S01", "STAT-01", "statistics", "Office for National Statistics", "United Kingdom", "Release practice policy", "2026-04-16",
     "The page visibly states that it was last updated on 16 April 2026; the URL remains mutable.",
     "Governs statistical publication timing, presentation, corrections, user-requested data, and exceptional access before publication.",
     "Standalone policy; complete numbered operating sections 1–6, excluding the title, date metadata, and related-link navigation.",
     ["The URL does not pin a historical revision; the captured bytes and body hash identify the observed version."],
     "libraries_2_stats_1_candidate_manifest.jsonl", 1),
    ("S02", "STAT-02", "statistics", "Statistics Canada", "Canada", "A closer look at the Policy on Official Release", "2025-12-23",
     "The page visibly states Date modified: 2025-12-23; it is the first eligible title-ordered official guidance page.",
     "Describes the controls, limited access, acknowledgements, and responsibilities required when information is shared before official publication.",
     "Standalone official procedural guidance; complete substantive body, excluding title, navigation, footer, and date-modified metadata.",
     ["This is the agency's public procedural explanation, not the separately linked formal policy document.", "The URL is mutable and the stated modified date does not supply a historical revision archive."],
     "libraries_2_stats_1_candidate_manifest.jsonl", 1),
    ("S03", "STAT-03", "statistics", "Australian Bureau of Statistics", "Australia", "Australian System of National Accounts: Concepts, Sources and Methods, Edition 8", "2026-01-20",
     "Edition 8 is marked as the latest release and dated 20 January 2026 on the section page; the edition directory also contains a 23 October 2026 release entry without a section-specific change history.",
     "Explains the national-accounts compilation cycle, routine and historical revisions, and the publication of revision information.",
     "One technical manual is counted once. Retrieval uses the complete Revisions section in chapter 24, numbered paragraphs 24.107–24.131, in original order.",
     ["The initial search found the 2020–21 edition. Its official latest-edition link led to Edition 8; this is a version update of the same work.", "The section is not counted as an additional standalone document.", "An initial request to the current chapter returned HTTP 503; a retry, the official chapter-print representation, and the current section subsequently succeeded."],
     "statistics_2_candidate_manifest.jsonl", 4),
    ("S04", "STAT-04", "statistics", "Bureau of Labor Statistics", "United States", "BLS Error Correction Policy", "2026-08-28",
     "The page visibly states Last modified date: August 28, 2026; the URL is mutable.",
     "Describes the agency's process for reporting discovered errors, recording correction status, and occasionally leaving small errors uncorrected.",
     "Standalone policy; complete substantive main body, excluding the title, modified-date metadata, and adjacent navigation.",
     ["Program-specific details are linked elsewhere and are not included in this central policy's body."],
     "statistics_2_candidate_manifest.jsonl", 1),
    ("S05", "STAT-05", "statistics", "Bureau of Economic Analysis", "United States", "Correction Policy", None,
     "Current undated official policy page, captured on 2026-11-22.",
     "Sets out factors used to choose a correction notice or scheduled revision, notification arrangements, and treatment of small table errors.",
     "Standalone policy; complete three-paragraph operating body after the breadcrumb navigation.",
     ["No policy publication or revision date is stated; a server Last-Modified value is not treated as a policy date.", "The observed URL is mutable; historical availability before capture is unverified."],
     "statistics_2_candidate_manifest.jsonl", 1),
    ("S06", "STAT-06", "statistics", "Stats NZ", "New Zealand", "Release practices policy", "2026-03-31",
     "The body states an effective date of 31 March 2026 and next review in March 2028. Embedded page metadata separately retains PageDate 2021-06-10.",
     "Assigns responsibility for statistical releases and specifies principles governing access, timing, integrity, and applicable institutional obligations.",
     "Standalone policy; complete rendered content from FeaturedText and ordered PageBlocks in the official page's embedded JSON.",
     ["The initial visible-DOM extraction was empty because content is embedded for client rendering; the original HTML contains the complete text.", "The effective date governs version reporting; the older CMS PageDate is preserved as a separate observation.", "Linked detailed embargo and access procedures are separate works and are not added to this body."],
     "statistics_2_candidate_manifest.jsonl", 2),
]


def selected_rows() -> list[dict]:
    rows = []
    for cid, local, field, issuer, jurisdiction, title, date, version, summary, scope, limitations, manifest, rank in FACTS:
        capture = json.loads((CACHE / f"{local}.capture.json").read_text())
        text_path = CACHE / f"{local}.txt"
        data = text_path.read_bytes()
        assert data and b"\r" not in data and len(data.split()) > 30
        raw_path = CACHE / f"{local}.html"
        raw_kind = "official_http_html"
        if local == "LIB-04":
            raw_path = CACHE / "LIB-04.web.json"
            raw_kind = "official_url_web_reader_transcript"
        initial_path = CACHE / f"{local}.initial_extracted.txt"
        row = {
            "candidate_id": cid,
            "source_id": cid,
            "field": field,
            "issuer": issuer,
            "jurisdiction": jurisdiction,
            "title": title,
            "url": capture["requested_url"],
            "url_fixity": "versioned_edition_path_mutable_content" if cid == "S03" else "current_mutable_url",
            "publication_or_version_date": date,
            "version_note": version,
            "retrieved_at": "2026-11-22" if cid == "L04" else capture["retrieved_at"],
            "language": "English",
            "language_observation": "Official publisher's English page; no translation or third-party rendering of the language was used.",
            "document_unit": scope,
            "neutral_procedural_summary": summary,
            "read_location": f"Selected plain-text body lines 1–{len(data.decode('utf-8').splitlines())}; {scope}",
            "substantive_read": True,
            "counted_minimum": True,
            "selection_status": "selected",
            "discovery_manifest": relative(BASE / manifest),
            "initial_or_directory_candidate_rank": rank,
            "cache_text_path": relative(text_path),
            "body_sha256": digest(text_path),
            "text_sha256": digest(text_path),
            "body_bytes": len(data),
            "body_lines": len(data.decode('utf-8').splitlines()),
            "body_whitespace_words": len(data.split()),
            "cache_raw_path": relative(raw_path),
            "raw_sha256": digest(raw_path),
            "raw_representation": raw_kind,
            "full_extracted_text_sha256": digest(initial_path) if initial_path.exists() else digest(text_path),
            "extraction": capture["extraction"],
            "limitations": limitations,
            "license_status": "No open-reproduction permission is asserted in this collection; original full text is retained only in ignored local cache.",
            "public_verbatim_body_excerpt": "",
            "protocol_commit": "cf10073b65a84002a889d37a2436a19b8f43d412",
        }
        if cid == "S03":
            row["work_url"] = "https://www.abs.gov.au/statistics/detailed-methodology-information/concepts-sources-methods/australian-system-national-accounts-concepts-sources-and-methods/edition-8"
            old = CACHE / "STAT-03-C4.txt"
            row["observed_prior_editions"] = [{"edition": "2020–21", "publication_date": "2021-07-09", "url": json.loads((CACHE / "STAT-03-C4.capture.json").read_text())["requested_url"], "cache_text_path": relative(old), "body_sha256": digest(old), "substantive_read": True, "counted_as_separate_document": False}]
        rows.append(row)
    return rows


def excluded_rows() -> list[dict]:
    facts = [
        ("LX01", "LIB-01-C3", "library", "Seattle Public Library", "Due Dates", None, "General checkout/overdue rules contain only an incidental statement about variable interlibrary-loan periods, not an interlibrary-loan or recall procedure."),
        ("LX02", "LIB-05-C1", "library", "Hennepin County Library", "Collection Development and Management Policy", "2024-11-13", "Collection policy describes resource sharing but does not prescribe an interlibrary-loan or recall procedure."),
        ("LX03", "LIB-06-C1", "library", "Vancouver Public Library", "Digitization and Lending of Print Books", "2022-09-28", "Operates digitization and lending of locally held works; interlibrary loan appears as a definition rather than the governed procedure."),
        ("SX01", "STAT-03-C3", "statistics", "Australian Bureau of Statistics", "Australian System of Government Finance Statistics: Concepts, Sources and Methods, 2015", "2015-12-23", "The complete data-quality-framework section gives assessment dimensions, not an operational release/revision/correction procedure. The manual is counted as one excluded work, not the section as an additional work."),
    ]
    rows = []
    for sid, local, field, issuer, title, date, reason in facts:
        cap = json.loads((CACHE / f"{local}.capture.json").read_text())
        text = CACHE / f"{local}.txt"
        raw = CACHE / f"{local}.html"
        rows.append({
            "source_id": sid, "candidate_id": None, "field": field, "issuer": issuer, "title": title,
            "url": cap["requested_url"], "publication_or_version_date": date,
            "retrieved_at": cap["retrieved_at"], "selection_status": "excluded_after_substantive_read",
            "exclusion_reason": reason, "substantive_read": True, "counted_minimum": False,
            "read_location": f"Entire cached main body, {len(text.read_text().splitlines())} lines; page title omitted by extractor.",
            "cache_text_path": relative(text), "body_sha256": digest(text),
            "cache_raw_path": relative(raw), "raw_sha256": digest(raw),
            "license_status": "No open-reproduction permission asserted; full original body retained only in ignored local cache.",
            "public_verbatim_body_excerpt": "",
        })
    return rows


if __name__ == "__main__":
    rows = selected_rows()
    sources = rows + excluded_rows()
    write_jsonl("library_statistics_corpus_draft.jsonl", rows)
    write_jsonl("library_statistics_sources.jsonl", sources)
    print(json.dumps({"selected": len(rows), "substantively_read_excluded_works": len(sources) - len(rows), "by_field": {field: sum(row['field'] == field for row in rows) for field in ['library', 'statistics']}, "candidate_ids": [row['candidate_id'] for row in rows]}, indent=2))
