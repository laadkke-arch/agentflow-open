"""Independent read-only review of sealed selections and preserved Q7 originals."""
from pathlib import Path
import collections
import csv
import datetime
import hashlib
import io
import json
import subprocess

from lxml import etree, html

HERE = Path(__file__).resolve().parent
TASK = HERE.parent.parent
REPO = TASK.parents[3]
SEAL = "8054c2221d4023ba03c904d96f13928219d36c3d"
INPUT = "092f4c5c56451bceb53e632f4bddf33db6cda168"
PREFIX = "docs/workstreams/research/AF-RES-106/"


def git_bytes(revision, path):
    return subprocess.check_output(["git", "show", revision + ":" + path], cwd=REPO)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def rows(data):
    return list(csv.DictReader(io.StringIO(data.decode())))


def main():
    review = {"reviewed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "reviewer": "/root/crossdomain_review (same model family; distinct agent turn)",
              "sealed_commit": SEAL, "inherited_result_commit": INPUT,
              "scope": "Independent calculation of sealed selection and Q7 raw relationships. Not independent blind scoring of main U outcomes."}
    frame = rows(git_bytes(SEAL, PREFIX + "frame.csv"))
    predictions = rows(git_bytes(SEAL, PREFIX + "predictions.csv"))
    old_frame = rows(git_bytes(INPUT, "docs/workstreams/research/AF-RES-102/frame.csv"))
    old_sources = [json.loads(line) for line in git_bytes(INPUT, "docs/workstreams/research/AF-RES-102/sources.jsonl").splitlines() if line]
    review["sealed_files"] = {}
    for name in ["frame.csv", "predictions.csv", "SCOPE.md", "EVALUATION_TARGETS.md"]:
        original = git_bytes(SEAL, PREFIX + name)
        review["sealed_files"][name] = {"sha256": sha(original), "local_same_as_seal": original == (TASK/name).read_bytes()}
    selection = {"slots": len(predictions), "unique_case_ids": len({r["case_id"] for r in predictions}),
                 "filled": sum(r["vacant"] == "NO" for r in predictions),
                 "vacancies": sum(r["vacant"] == "YES" for r in predictions), "projects": []}
    for project in ["ggplot2", "Matplotlib"]:
        eligible = [r for r in frame if r["project"].lower() == project.lower() and r["eligible"] == "YES"]
        excludes = {r.get("page_path", "") for r in old_frame if r["project"].lower() == project.lower() and r.get("eligible") == "YES"}
        o = {"project": project, "eligible": len(eligible), "hash_mismatches": [], "prior_eligible_page_overlap": [], "strata": {}}
        for row in eligible:
            expected = sha(("AF106|" + project + "|" + row["old_section_path"]).encode())
            if expected != row["hash_sha256"]:
                o["hash_mismatches"].append(row["old_section_path"])
            if row["page_path"] in excludes:
                o["prior_eligible_page_overlap"].append(row["page_path"])
        for stratum in ["A", "M", "G"]:
            candidates = [r for r in eligible if (r["signal_stratum"] or r["stratum"]) == stratum]
            ordered = sorted(candidates, key=lambda r: (r["hash_sha256"], r["old_section_path"]))[:2]
            actual = [r for r in predictions if r["project"] == project and r["stratum"] == stratum and r["vacant"] == "NO"]
            o["strata"][stratum] = {"population": len(candidates), "expected": [r["old_section_path"] for r in ordered],
                                    "observed": [r["old_section_path"] for r in actual],
                                    "correct": [r["old_section_path"] for r in ordered] == [r["old_section_path"] for r in actual]}
        selection["projects"].append(o)
    review["selection"] = selection
    review["inherited_sources"] = {"rows": len(old_sources), "iiif_jats_matches": [o.get("source_id") for o in old_sources if any(x in json.dumps(o).lower() for x in ["iiif.io", "iiif.micr", "fitzmuseum", "jats.nlm", "pone.0319031"])]}
    review["reopened_originals"] = json.loads((HERE/"review-network-receipts.json").read_text())
    ledger = [json.loads(line) for line in (HERE/"sources-crossdomain.jsonl").read_text().splitlines() if line]
    review["first_ledger"] = {"rows": len(ledger), "countable_ids": [r["source_id"] for r in ledger if r["countable"]],
                              "countable_unique_lineages": len({r["lineage"] for r in ledger if r["countable"]}),
                              "review_reopen_added_count": 0,
                              "payload_digest_mismatches": [r["source_id"] for r in ledger if sha((TASK/r["preservation"]).read_bytes()) != r["sha256"]]}
    rijks = json.loads((HERE/"review-raw/rijksmuseum-manifest.json").read_text())
    canvas = rijks["items"][0]
    annotation = canvas["items"][0]["items"][0]
    review["rijks"] = {"canvas": canvas["id"], "canvas_count": len(rijks["items"]), "annotation_page": canvas["items"][0]["id"],
                       "annotation": annotation["id"], "motivation": annotation["motivation"], "target": annotation["target"],
                       "painting_body": annotation["body"]["id"], "thumbnail": rijks["thumbnail"][0]["id"],
                       "same_body_and_thumbnail_url": annotation["body"]["id"] == rijks["thumbnail"][0]["id"]}
    fitz = json.loads((HERE/"review-raw/fitzwilliam-manifest.json").read_text())
    canvas = fitz["items"][0]
    choices = canvas["items"][0]["items"][0]["body"]
    annotations = canvas["annotations"][0]["items"]
    review["fitz"] = {"canvas": canvas["id"], "painting_body_type": choices["type"], "choice_count": len(choices["items"]),
                      "choice_labels": [x["label"] for x in choices["items"]], "commentary_count": len(annotations),
                      "targets": dict(collections.Counter(x["target"] for x in annotations)), "viewer_display": "미확인"}
    xml = etree.fromstring((HERE/"review-raw/plos-spark.xml").read_bytes())
    html_doc = html.fromstring((HERE/"review-raw/plos-spark.html").read_bytes())
    figures = xml.xpath("//fig")
    xrefs = xml.xpath('//xref[@ref-type="fig"]')
    fig7x = xml.xpath('//xref[@ref-type="fig"][@rid="pone.0319031.g007"]')
    bodyx = [e for e in fig7x if e.getparent().tag == "p"]
    refs = []
    for e in fig7x:
        section = e.xpath("ancestor::sec[1]")[0]
        refs.append({"line": e.sourceline, "parent": e.getparent().tag, "parent_line": e.getparent().sourceline,
                     "section": section.get("id"), "in_table_caption": bool(e.xpath("ancestor::table-wrap"))})
    figures_mapping = []
    for e in figures:
        ident = e.get("id")
        figures_mapping.append({"xml_id": ident, "xml_line": e.sourceline,
                                "literal_html_id_count": len(html_doc.xpath('//*[@id=$value]', value=ident)),
                                "actual_html_id": ident.replace(".", "-"),
                                "actual_html_id_count": len(html_doc.xpath('//*[@id=$value]', value=ident.replace(".", "-")))})
    captions = {}
    for ident in ["pone.0319031.g007", "pone.0319031.g008", "pone.0319031.t003"]:
        e = xml.xpath('//*[@id=$value]', value=ident)[0]
        caption = e.xpath("./caption")[0]
        captions[ident] = {"line": e.sourceline, "caption_text": " ".join("".join(caption.itertext()).split()),
                          "figure_xref_targets": caption.xpath('.//xref[@ref-type="fig"]/@rid')}
    review["plos"] = {"dtd_version": xml.get("dtd-version"), "figure_count": len(figures), "figure_xref_count": len(xrefs),
                      "all_figure_xrefs_resolve": all(len(xml.xpath('//*[@id=$value]', value=e.get("rid"))) == 1 for e in xrefs),
                      "figure_mapping": figures_mapping, "fig7_xref_count": len(fig7x), "fig7_prose_xref_count": len(bodyx),
                      "fig7_distinct_prose_paragraphs": len({e.getparent() for e in bodyx}), "fig7_refs": refs,
                      "captions": captions, "viewer_scroll": "미확인", "table3_author_intent": "미확인"}
    review["limitations"] = ["The source-set amendment occurred after path exposure but before outcome reading; existing disclosure retained.",
                              "The generalized Matplotlib visual-role target was appended after selection; original purpose must remain separately scored.",
                              "Q7 snapshots are current public documents, not time-series evidence of migration or historical generation.",
                              "Four Fig7 prose xrefs occur in three distinct paragraphs, not four paragraphs.",
                              "Independent selection audit recomputes sealed frame hashes and ranks, not all raw old-page eligibility boundaries."]
    (HERE/"review-final.json").write_text(json.dumps(review, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({"selection": selection, "inherited_sources": review["inherited_sources"], "ledger": review["first_ledger"],
                      "network": {"success": sum(r.get("http_status") == 200 for r in review["reopened_originals"]),
                                  "same_bytes": sum(r.get("same_bytes_as_first_snapshot", False) for r in review["reopened_originals"])},
                      "plos": {k: review["plos"][k] for k in ["figure_count", "figure_xref_count", "fig7_xref_count", "fig7_prose_xref_count", "fig7_distinct_prose_paragraphs"]}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
