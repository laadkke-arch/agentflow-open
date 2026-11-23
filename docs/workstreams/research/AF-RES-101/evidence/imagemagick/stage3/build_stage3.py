"""Derive bounded Stage 3 evidence; never mutate Stage 1/2 sealed judgments."""
import datetime
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]
OUT = BASE / "evidence/imagemagick/stage3"
CACHE = BASE / ".cache/imagemagick/stage3"
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
PIN = "https://github.com/ImageMagick/ImageMagick/blob/eeb41d70c9baf418a3aa75c424fb305362a1b280/"


def read(path):
    return json.loads(path.read_text())


def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


official = {x["path"]: x for x in read(OUT / "official-acquisition.json")}
specs = [
    ("IM-O1", "www/command-line-options.html", ["IM-A1", "IM-A2", "IM-U1", "IM-U2"],
     "L766–790 brightness-contrast; L874–920 channel; L1961–1967 deskew; L2231–2243 Perspective; L2479–2496 distort canvas; L5381–5402 normalize; L6236–6239 separate; L6498–6508 size; L6870–6907 threshold",
     "brightness/contrast is a relative linear transformation, not a QR decoder. Perspective needs four coordinate pairs and preserves straight lines. -distort defaults to the input-size canvas; +distort fits the transformed image; viewport can override. threshold's raw quantum count differs from a percent. size is an input/canvas hint, not a resize of an already read image. normalize documentation identifies contrast-stretch 2%x1%.",
     "Supports different arguments/stages despite the same product; refutes interpreting every deskew/perspective operation as the same action. The normalize alias claim is contradicted by the same release's enhance.c implementation.",
     "7.0.10-61 is the stated version only for IM-A2. Other request versions are unspecified. Function documentation does not establish original QR decoding, automatic corners or wrapper API correctness. Multiple anchors count once.", True, "official_imagemagick"),
    ("IM-O2", "www/command-line-processing.html", ["IM-A1", "IM-A2"],
     "L561–581 Image Stack / parentheses",
     "Parentheses create a separate image stack; operators inside apply to that stack. Unix escaping belongs to shell token construction, while parentheses must be separate command arguments.",
     "Supports the significance of the grouped clone/mask pipeline and the need to compare actual arguments rather than program name or visually similar strings.",
     "Does not establish QuickMagick/RMagick translation correctness or repair a shell fragment. Root probe separately observes literal expansion and synthetic CLI behavior.", True, "official_imagemagick"),
    ("IM-O3", "MagickWand/operation.c", ["IM-U1", "IM-U2"],
     "L1900–1920 brightness-contrast; L2125–2147 contrast-stretch percent parsing; L2242–2278 distort / IsPlusOp; L2947–2949 normalize",
     "CLI dispatch parses brightness/contrast values and passes them to BrightnessContrastImage; contrast-stretch converts percentages to image-pixel counts and computes the white-side complement; the sign of distort is passed as bestfit; normalize dispatches to NormalizeImage.",
     "Connects documented option text with the implementation, distinguishing named aliases and effect-changing operator signs.",
     "Static implementation reading, not an execution of 7.0.10-61. Parsing existence does not prove source-image goal satisfaction.", True, "official_imagemagick"),
    ("IM-O4", "MagickCore/distort.c", ["IM-U2"],
     "L828+ Perspective mapping; L1678–1696 contract; L1818–1822 default canvas; L1882–1905 bestfit corners; L2018–2026 bounds; L2031–2038 viewport override",
     "Perspective uses a projective mapping. Default output canvas starts at input dimensions with zero offset; bestfit derives transformed bounds; an explicit viewport replaces the computed geometry.",
     "Supports a real +distort/-distort canvas difference and a countercase where explicit viewport makes those two spellings equivalent on a fixed input.",
     "No automatic source-corner detector or curved-surface dewarping is established. A source photograph's correct physical aspect ratio cannot be inferred solely from this mapping code.", True, "official_imagemagick"),
    ("IM-O5", "MagickCore/enhance.c", ["IM-U1"],
     "L222–251 BrightnessContrastImage; L1551+ ContrastStretchImage and L1660–1674 histogram limits; L4096–4105 NormalizeImage",
     "BrightnessContrastImage derives a linear slope from contrast. In fixed 7.0.10-61 NormalizeImage uses black=count*0.0015 and white=count*0.9995, corresponding through the CLI parser to 0.15% low and 0.05% high clipping. This differs from the same tag's 2%/1% documentation.",
     "Refutes an unqualified cross-version normalize=contrast-stretch 2%x1% alias. Supports separating source-confirmed old defaults from research-version results.",
     "Old release was not compiled or run. These are implementation values, not a historical user's runtime receipt or original QR decoder result.", True, "official_imagemagick"),
    ("IM-T1", "tests/cli-colorspace.tap", ["IM-A1"],
     "L28–38 rose: average input; L59–67 expected/reference pixels; L98–119 19 color-space checks",
     "Upstream test constructs the rose: average, expects 146,89,80 (with alternative gamma error colors 73,26,21 and 199,160,152), and checks color-space round trips. The unchanged fixed script was executed against research ImageMagick 7.1.1-43 and passed 19/19 TAP checks.",
     "Supports color-space conversion as an independently tested stage; provides an upstream input/expected-output bundle. Research receipt: probes/results.json upstream_script_execution.",
     "This test does not implement the HCL/G/15%-mask wrapper pipeline and does not validate the original grayscale-removal image. The script is from 7.0.10-61 but the executed binary is 7.1.1-43. The test's failure-message text says 145 while the expected comparison is 146; recorded values follow the comparison.", True, "upstream_test_bundle"),
    ("IM-T2", "tests/validate.h", ["IM-A1", "IM-A2", "IM-U1"],
     "L21–22 rose:/MIFF reference; L33–96 composite options incl CopyOpacity; L98–196 convert options incl crop/normalize; tests/validate.c L1333–1392; tests/validate-convert.tap L23",
     "Upstream convert options include crop, color-space operations and normalize; composite vectors include CopyOpacity. The harness builds a command with the reference image, runs ConvertImageCommand, and expects successful return status.",
     "Provides a second upstream command/input/expected-success test bundle for the original operators. The actual oracle was inspected rather than assuming that a passing option test proves pixel correctness.",
     "One bundle is counted across header, runner and TAP wrapper. The full C suite was not built/run. Its success-status oracle has no QR-decoder, alpha-mask goal, patch-geometry or requester-success assertion.", True, "upstream_test_bundle"),
    ("IM-T2-HARNESS", "tests/validate.c", ["IM-A1", "IM-A2", "IM-U1"],
     "L1333–1392 ValidateConvertCommand",
     "Read command construction and status-only pass/fail oracle; confirmed no output-pixel comparison in this function.",
     "Limits the strength of IM-T2; does not create a separate independent test bundle.",
     "Not executed; duplicate supporting component of IM-T2.", False, "test_bundle_component"),
    ("IM-T2-TAP", "tests/validate-convert.tap", ["IM-A1", "IM-A2", "IM-U1"],
     "L1–25; L23 invokes VALIDATE -validate convert",
     "Read wrapper entry point and the invocation of the convert validation group.",
     "Connects the header vectors and C harness to an upstream CLI test entry point.",
     "Not executed; duplicate supporting component of IM-T2.", False, "test_bundle_component"),
    ("IM-T1-ENV", "tests/common.shi", ["IM-A1"],
     "whole 10-line environment helper",
     "Read the upstream helper loading test environment defaults. Research execution generated a local environment with MAGICK pointing at the installed binary while preserving the original test script.",
     "Explains the execution boundary and environment used by IM-T1.",
     "Supporting helper, not an independent behavioral source or test bundle.", False, "test_bundle_component"),
    ("IM-TEST-UNUSED-PIPE", "tests/cli-pipe.tap", [],
     "whole script; pipe processing checks",
     "Read the pipe-focused script while checking available CLI tests; no selected candidate uses that stream pipeline.",
     "No selected candidate claim is established by this file; excluded from the minimum.",
     "Downloaded/read but not substantively matched to a candidate; not counted.", False, "unmatched_test"),
]
sources = []
for sid, path, cases, loc, observed, relation, limit, counted, category in specs:
    a = official[path]
    sources.append({
        "id": sid, "questions": ["Q5"], "case_ids": cases,
        "original_url": "https://github.com/ImageMagick/ImageMagick/blob/7.0.10-61/" + path,
        "directly_opened_url": a["url"], "pinned_url": a["pinned_url"],
        "confirmation_utc": a["utc"], "analyst_review_completed_utc": NOW,
        "author_publisher": "ImageMagick Studio LLC / ImageMagick upstream",
        "lineage": "ImageMagick upstream " + path,
        "version_section": "7.0.10-61; commit " + a["commit"] + "; " + loc,
        "fingerprint": {"sha256": a["sha256"], "git_blob_sha1": a["git_blob_sha1"]},
        "observed": observed, "claim_relation": relation, "limitations": limit,
        "counted": counted, "count_category": category,
        "duplicate_reason": None if counted else limit,
        "receipt": "evidence/imagemagick/stage3/official-acquisition.json",
    })
r = read(OUT / "research-version-acquisition.json")
sources.append({
    "id": "IM-O5-V7143", "questions": ["Q5"], "case_ids": ["IM-U1"],
    "original_url": "https://github.com/ImageMagick/ImageMagick/blob/7.1.1-43/MagickCore/enhance.c",
    "directly_opened_url": r["url"], "pinned_url": r["pinned_url"],
    "confirmation_utc": r["utc"], "analyst_review_completed_utc": NOW,
    "author_publisher": "ImageMagick Studio LLC / ImageMagick upstream",
    "lineage": "ImageMagick upstream MagickCore/enhance.c; version comparison of IM-O5",
    "version_section": "7.1.1-43; a2d96f40e707ba54b57e7d98c3277d3ea6611ace; L4130–4139 NormalizeImage",
    "fingerprint": {"sha256": r["sha256"]},
    "observed": "NormalizeImage now uses black=count*0.02 and white=count*0.99. On the research 2000-pixel gradient normalize and contrast-stretch 2%x1% were identical; 0.15%x0.05% differed at 1992/2000 pixels.",
    "claim_relation": "Supports a release-dependent alias and prevents applying research-binary defaults to the old release.",
    "limitations": "Same upstream file across versions, not another unique source. The synthetic gradient is not the original QR input.",
    "counted": False, "count_category": "version_support", "duplicate_reason": "same source lineage as IM-O5",
    "receipt": "evidence/imagemagick/stage3/research-version-acquisition.json",
})
(OUT / "sources-official.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in sources))

events = read(CACHE / "followup/author-90day-projection.json")
inventory = read(OUT / "followup-inventory.json")
current = read(CACHE / "followup/current-question-projection.json")
initial = {x["case_id"]: x for x in read(BASE / "evidence/imagemagick/initial-part.json")}
acq = read(OUT / "followup-acquisition.json")
comments_receipt = next(x for x in acq if x["stem"] == "comments90")
rev_receipts = read(BASE / "evidence/imagemagick/acquisition-h1.json")

# Codes are conservative: an unobserved mental state is unknown, not false.
annotations = {
    "IM-U1-R2": (["formatting_only"], [], "Image link moved to its own paragraph; no new specific attempted operation.", "p1–p3", []),
    "IM-U1-C137059273": (["refinement_request", "thanks_only"], ["IM-U1-C1"], "Author asks whether the output can be black and white; no statement of running the command or successful decoding.", "whole comment", ["black and white"]),
    "IM-U1-C137066174": (["positive_evaluation", "thanks_only"], ["IM-U1-C1", "IM-U1-C2", "IM-U1-C3"], "Author calls both answers useful. This cannot attribute success or novelty to a particular operation or establish QR decoding.", "whole comment", ["useful answers"]),
    "IM-A1-R2": (["execution_report", "failure_reported", "candidate_modified"], ["IM-A1-C1"], "Author replaces the original attempt with the proposed QuickMagick pipeline but comments out alpha(off). Error reports a QuickMagick object plus arguments being treated as an image filename and no output image. Versions and source pixels are absent.", "p2/pre2 changed pipeline; p3/pre3 error", ["I tried by @8bithero"]),
    "IM-A1-C137114172": (["execution_report", "failure_reported"], ["IM-A1-C1"], "Author explicitly reports trying the code and adding the resulting error to the question. Read together with revision2 this concerns a modified candidate, not proven execution of the exact original snippet.", "whole comment linked to question revision2", ["after trying your code"]),
    "IM-U2-R2": (["goal_clarification_before_proposal"], [], "Author adds that the underlying object is rectangular but physical length/width are unknown a priori. This revision precedes the first candidate; it remains separate from the mandated earliest-revision baseline.", "p1–p4", []),
    "IM-U2-C137127563": (["goal_clarification"], ["IM-U2-C1"], "Author clarifies orthogonal photo angle as the target and de-emphasizes wrinkle removal. No execution of perspective mapping or new-awareness statement.", "whole comment", []),
    "IM-A2-C137150030": (["positive_evaluation_other_contexts", "thanks_only"], ["IM-A2-C1"], "Author says the approach may help in other situations. Neither a clear rejection nor a successful execution report.", "whole comment", ["in other situations"]),
    "IM-A2-C137150039": (["positive_intent_fit", "thanks_only"], ["IM-A2-C2"], "Author says the approach matches what was sought. This is intent-fit feedback, without a command, version, output or execution statement.", "whole comment", ["way I was looking for"]),
}
followup_rows = []
followup_sources = []
for e in events:
    suffix = "C" + str(e["comment_id"]) if e["kind"] == "author_comment" else "R" + str(e["revision_number"])
    key = e["case_id"] + "-" + suffix
    codes, candidates, observed, loc, quote = annotations[key]
    source_id = "FUP-" + key
    if e["kind"] == "author_comment":
        receipt = comments_receipt
    else:
        receipt = None
        for page, rr in enumerate(rev_receipts, 1):
            raw = read(BASE / f".cache/imagemagick/revisions-h1-{page}.json")
            if any(x.get("revision_guid") == e["revision_guid"] for x in raw["items"]):
                receipt = rr
                break
        assert receipt is not None
    observed_execution = "execution_report" in codes
    row = {
        "event_id": key, "source_id": source_id, "case_id": e["case_id"],
        "question_id": e["question_id"], "kind": e["kind"], "candidate_ids": candidates,
        "event_utc": datetime.datetime.fromtimestamp(e["time"], datetime.timezone.utc).isoformat(),
        "url": e["url"], "body_location": loc, "body_sha256": e["body_sha256"],
        "author": e.get("author"), "codes": codes, "observed": observed,
        "short_evidence": quote, "already_knew_before_proposal": "미확인",
        "explicit_new_awareness": "미확인",
        "execution_report": "지지" if observed_execution else "미확인",
        "input_version_output_linked_execution": "미확인",
        "rejection": "미확인", "old_method_retained": "미확인",
        "limits": "Deleted/private content is unobserved; comments have no public revision history. No acceptance/thanks-to-awareness inference. Modified-code execution is not exact-candidate execution.",
        "reviewed_utc": NOW, "after_stage2_seal": "4e7539906eb03abd46e6910643ed5317f97ddb45",
    }
    followup_rows.append(row)
    followup_sources.append({
        "id": source_id, "questions": ["Q6"], "case_id": e["case_id"],
        "original_url": e["url"], "directly_opened_url": receipt["url"],
        "pinned_url": e["url"] if e["kind"] != "author_comment" else None,
        "confirmation_utc": receipt["utc"], "analyst_review_utc": NOW,
        "author_publisher": e["author"]["display_name"] + " / Stack Overflow (Stack Exchange API)",
        "lineage": "Stack Overflow question " + str(e["question_id"]) + "; child of " + initial[e["case_id"]]["source_id"],
        "version_section": ("public revision " + str(e["revision_number"]) + "; GUID=" + e["revision_guid"] if e["kind"] != "author_comment" else "current public comment body; creation-time window only") + "; " + loc,
        "fingerprint": {"body_html_sha256": e["body_sha256"], "response_sha256": receipt["sha256"]},
        "observed": observed, "claim_relation": "Supports only the listed behavior codes; mental novelty and linked successful execution remain unknown.",
        "limitations": row["limits"], "counted": False, "count_category": "selected_request_child",
        "duplicate_reason": "Same independent request as " + initial[e["case_id"]]["source_id"],
    })
(OUT / "sources-followup.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in followup_sources))

changes = {
    "IM-A1": (True, False, "Revision2 replaces the first failed command with a modified C1 trial and detailed failure. Exact C1 identity still unproved because alpha(off) is commented out and input/version missing; no sealed filter is changed."),
    "IM-A2": (False, False, "Current public question body remains revision1."),
    "IM-U1": (False, False, "Revision2 only moves the input link; no identified actual product or operation is added."),
    "IM-U2": (False, True, "Revision2 adds rectangular-object/unknown-dimensions conditions before the first proposal; later comment narrows the target to orthogonal angle. Earliest-revision judgments are preserved."),
}
comparisons = []
for c in current:
    attempt_changed, target_changed, explanation = changes[c["case_id"]]
    comparisons.append({k: v for k, v in c.items() if k != "body"} | {
        "actual_attempt_history_changed": attempt_changed, "target_detail_changed": target_changed,
        "definitive_a_filter_change": False, "definitive_b_filter_change": False,
        "explanation": explanation, "reviewed_utc": NOW,
    })
write("followup-part.json", {
    "stage2_seal": "4e7539906eb03abd46e6910643ed5317f97ddb45", "review_completed_utc": NOW,
    "events": followup_rows, "case_inventory": inventory, "first_current_comparison": comparisons,
    "summary": {"request_count": 4, "events": 9, "author_comments": 6, "author_revisions": 3,
        "self_answers": 0, "explicit_new_awareness_supported_candidates": 0,
        "candidate_execution_report_supported": 1, "candidate_execution_report_detail": "IM-A1-C1 modified trial, two observations of one episode",
        "input_version_output_linked_execution_supported_candidates": 0,
        "current_body_changed_cases": 3, "actual_attempt_history_changed_cases": 1,
        "target_detail_changed_cases": 1, "definitive_a_filter_change_cases": 0, "definitive_b_filter_change_cases": 0,
        "external_result_patch_links_observed": 0},
    "completeness": "All 90-day API answer/comment pages exhausted (has_more=false); question revisions reused from complete Stage1 machine download and first analyst-read after Stage2 seal. No self-answer was present. Window is per-case t0 through t0+90*86400 seconds inclusive.",
    "exposure": "Current acceptance and all author records intentionally released only after Stage2 seal. Earlier indirect non-author quotations are separately recorded in proposals-exposure.json; not full blindness.",
    "limitations": "Public surviving records only; no historical comment versions, deleted content, private execution, or acceptance timestamps. Zero positive novelty evidence means unknown novelty, not proof of no learning.",
})
print(json.dumps({"official_unique": sum(s["counted"] for s in sources), "official_documents": sum(s["counted"] and s["count_category"] == "official_imagemagick" for s in sources), "upstream_bundles": sum(s["counted"] and s["count_category"] == "upstream_test_bundle" for s in sources), "followup_events": len(followup_rows)}, ensure_ascii=False))
