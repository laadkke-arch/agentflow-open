"""Candidate-level Q5/Q6 assessments, separately from sealed A/B decisions."""
import datetime
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]
OUT = BASE / "evidence/imagemagick/stage3"
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
CANDIDATES = json.loads((BASE / "evidence/imagemagick/candidate-part.json").read_text())
FOLLOWUP = json.loads((OUT / "followup-part.json").read_text())
ROOT = json.loads((BASE / "evidence/root-supplement/assessment.json").read_text())
ROOT_BY_ID = {x["candidate_id"]: x for x in ROOT["candidates"]}
PIN = "https://github.com/ImageMagick/ImageMagick/blob/eeb41d70c9baf418a3aa75c424fb305362a1b280/"
OPT = PIN + "www/command-line-options.html"
PROC = PIN + "www/command-line-processing.html"

def official(sid, url, section):
    return {"source_id": sid, "url": url, "section": section, "link_origin": "researcher_added_after_stage2"}


spec = {
    "IM-A1-C1": {
        "required_output_status": "미확인", "hard_constraint_status": "미확인",
        "validity": "reference_version_counterevidence; historical full output unknown",
        "source_ids": ["IM-O1", "IM-O2", "IM-T1", "SUP-QUICK-IMAGE", "FUP-IM-A1-R2", "FUP-IM-A1-C137114172"],
        "official_evidence": [official("IM-O1", OPT, "L6870–6907 threshold raw quantum versus percentage"), official("IM-O2", PROC, "L561–581 stack isolation")],
        "required_output_reason": "Core stages exist, but the shown QuickMagick calls are not validated as a working wrapper pipeline. Fixed QuickMagick0.8.0 API and research raw15-versus15% control supply counterevidence. Author reports failure for a modified version with alpha(off) omitted; exact historical candidate success is not shown.",
        "hard_constraint_reason": "Ruby wrapper use is in scope. Original image bytes, library/engine versions, and the numeric definition of grey are absent; required visual preservation cannot be checked.",
        "literal_evidence_status": "반박(QuickMagick0.8.0 API boundary; 연구판 threshold counterexample)",
        "partial_support": "Threshold percentage and grouping can change output even within ImageMagick; this is a useful correction principle, not proof that the returned code works.",
        "execution_report": "지지(수정된 C1 시도)", "linked_execution": "미확인",
        "execution_limit": "Question revision2 comments out alpha(off); one failed episode is described by revision2 and comment137114172. It does not prove exact-snippet execution or input/version/output linkage.",
        "unknowns": ["original library and engine versions", "original pixels", "exact C1 execution", "new awareness", "successful output"],
    },
    "IM-A1-C2": {
        "required_output_status": "미확인", "hard_constraint_status": "미확인",
        "validity": "reference_version_counterevidence; historical version unknown",
        "source_ids": ["IM-O1", "IM-O2", "IM-T1", "SUP-RMAGICK-CHANGELOG", "SUP-RMAGICK-BINDING"],
        "official_evidence": [official("IM-O1", OPT, "L6870–6907 threshold percentage semantics"), official("IM-O2", PROC, "L561–581 stack semantics")],
        "required_output_reason": "QuantumRange*0.15 represents the intended 15% threshold, but RMagick removed matte= in version4.0.0 and the fixed5.3.0 binding does not provide it. An earlier library may differ. No author execution is specifically attributable to this second operation.",
        "hard_constraint_reason": "RMagick is an allowed Ruby option in the first body; compatibility, original pixels, and preservation of nongrey image content are unconfirmed.",
        "literal_evidence_status": "반박(RMagick5.3.0; matte= removed since4.0.0)",
        "partial_support": "The threshold argument is materially closer to the original percentage than C1's raw15, but one correct argument does not establish a valid complete pipeline.",
        "unknowns": ["original RMagick version", "whether author ran C2", "original image output", "new awareness"],
    },
    "IM-A1-C3": {
        "required_output_status": "미확인", "hard_constraint_status": "미확인",
        "validity": "conditional core CLI support; whole Ruby candidate unverified",
        "source_ids": ["IM-O1", "IM-O2", "IM-T1", "SUP-RUBY-OPEN3", "SUP-RUBY-SHELLWORDS", "SO-IM-77774582"],
        "official_evidence": [official("IM-O1", OPT, "L6870–6907 threshold; channel/separate"), official("IM-O2", PROC, "L561–581 parenthesized image stack")],
        "required_output_reason": "Root's synthetic grouped CLI maps grey and near-grey alpha to0 while preserving red/blue/green; ungrouped literal fails. This supports the core change. Ruby was unavailable, Shellwords loading is not shown in the snippet, and original pixels are unavailable.",
        "hard_constraint_reason": "Ruby can execute a subprocess, but the request's exact wrapper requirement and environment are not independently settled. No original-input result.",
        "literal_evidence_status": "지지(연구판 synthetic CLI 부분); 전체 Ruby 미확인",
        "partial_support": "This is a same-engine different-execution-path alternative; its grouped CLI was already quoted by the requester before the proposal.",
        "prior_known": "partial_core_only", "full_candidate_known": "미확인",
        "prior_known_evidence": "First revision pre1 contains the same grouped core command; pre2's actual attempted QuickMagick.exec3 omitted grouping. Open3/Shellwords familiarity is not stated.",
        "known_core_sensitivity": {"eligible": True, "a_excluded": True, "b_excluded": False, "a_returned": False, "b_returned": False, "unit": "core grouped CLI only, not whole candidate"},
        "unknowns": ["prior awareness of Open3/Shellwords", "complete Ruby execution", "original pixels/version", "historical success"],
    },
    "IM-A2-C1": {
        "required_output_status": "미확인", "hard_constraint_status": "미확인",
        "validity": "literal shell-argument counterevidence; corrected concept not scored",
        "source_ids": ["IM-O1", "IM-O2", "IM-T2", "FUP-IM-A2-C137150030"],
        "official_evidence": [official("IM-O2", PROC, "L561–581 separate shell parenthesis arguments"), official("IM-O1", OPT, "L6498–6508 size; geometry")],
        "required_output_reason": "Selecting a fragment before convert is conceptually different from inserting shell if into convert, but the exact proposal leaves eight backslash-parenthesis tokens and embedded quotes in argv in root's Bash5.2.37 probe. Only argv was captured; original Cygwin/ImageMagick7.0.10-61 execution and output were not performed.",
        "hard_constraint_reason": "The author wanted simplification and asked for an internal condition. Whether an external setup step violates a strict condition is ambiguous in the first body. Original image/coordinates are missing.",
        "literal_evidence_status": "반박(연구 셸 인수 전달); 원 실행 미확인",
        "partial_support": "Variable factoring can eliminate repeated pipelines, but repairing escaping or using arrays would be a new researcher operation.",
        "unknowns": ["Cygwin shell exact version", "original image/coords", "corrected fragment used by author", "new awareness", "execution"],
    },
    "IM-A2-C2": {
        "required_output_status": "반박", "hard_constraint_status": "미확인",
        "validity": "literal snippet syntax counterevidence; conceptual correction unscored",
        "source_ids": ["IM-O1", "IM-O2", "IM-T2", "FUP-IM-A2-C137150039"],
        "official_evidence": [official("IM-O1", OPT, "L6498–6508 size creates/hints input; not resize; geometry"), official("IM-O2", PROC, "L561–581 stack parsing")],
        "required_output_reason": "The fixed first proposal's complete final block fails bash -n at the residual fi (exit2). It also leaves the white patch fixed30x40 while moving dims to size before mpr:img, so the stated70x50-versus30x40 patch condition is not literally preserved. The later d typo correction does not establish full repair.",
        "hard_constraint_reason": "Factor scalar values before convert could fit the simplification goal, but an external condition may not meet a strict internal-condition requirement; that requirement's strength is unknown.",
        "literal_evidence_status": "반박(원 rev1 snippet의 Bash 문법; 원입력 실행 아님)",
        "partial_support": "Author explicitly liked the approach, but did not report execution. A corrected scalar-parameter version could be useful and must remain separate from the frozen proposal.",
        "unknowns": ["which corrected code if any author used", "actual execution and output", "strictness of inside-convert condition", "new awareness"],
    },
    "IM-U1-C1": {
        "required_output_status": "미확인", "hard_constraint_status": "미확인",
        "validity": "contrast effect supported; original QR decodability unknown",
        "source_ids": ["IM-O1", "IM-O3", "IM-O5", "FUP-IM-U1-C137059273", "FUP-IM-U1-C137066174"],
        "official_evidence": [official("IM-O1", OPT, "L766–790 brightness-contrast"), official("IM-O3", PIN + "MagickWand/operation.c", "L1900–1920 CLI dispatch"), official("IM-O5", PIN + "MagickCore/enhance.c", "L222–251 linear slope/intercept")],
        "required_output_reason": "Documentation/implementation establish increased contrast for0,90, and research gradient output differs from normalize. They do not reconstruct missing QR module interiors or prove common-reader decoding. Original input and answer output both returned403.",
        "hard_constraint_reason": "ImageMagick was allowed but actual prior use is unspecified. Reader, payload, usable input bytes and required black/white geometry are unavailable.",
        "literal_evidence_status": "지지(대비 조절 효과); QR 목표 미확인",
        "partial_support": "Author requested a black-and-white refinement, then called both answers useful. This cannot establish decoder success or new knowledge.",
        "unknowns": ["previous unspecified methods", "original input bytes", "reader/payload", "author execution", "new awareness"],
    },
    "IM-U1-C2": {
        "required_output_status": "미확인", "hard_constraint_status": "미확인",
        "validity": "algorithmic proposal with incomplete reconstruction/decoder evidence",
        "source_ids": ["SO-IM-77743451", "FUP-IM-U1-C137066174"],
        "official_evidence": [],
        "required_output_reason": "Scanning horizontal rows and toggling polarity addresses a different representation problem from a contrast stretch, but the frozen proposal gives no fully specified executable algorithm or decoding receipt. The diagnostic animation returned403.",
        "hard_constraint_reason": "The original QR reader requirement remains untested; handling low signal, noise, row consistency and cleanup is unspecified.",
        "literal_evidence_status": "미확인(원 알고리즘의 입력·예상 출력/실행 부재)",
        "partial_support": "Same answer URL contains a distinct operation; no official IM function is falsely assigned as the implementation of this custom method.",
        "unknowns": ["threshold/peak detector", "module-grid cleanup", "full implementation", "decoder success", "author execution/new awareness"],
    },
    "IM-U1-C3": {
        "required_output_status": "미확인", "hard_constraint_status": "미확인",
        "validity": "normalization preprocessing supported; release and QR output unknown",
        "source_ids": ["IM-O1", "IM-O3", "IM-O5", "IM-O5-V7143", "IM-T2", "FUP-IM-U1-C137066174"],
        "official_evidence": [official("IM-O1", OPT, "L5381–5402 normalize"), official("IM-O5", PIN + "MagickCore/enhance.c", "L4096–4105 old defaults"), official("IM-O3", PIN + "MagickWand/operation.c", "L2125–2147 percent conversion; L2947–2949 dispatch")],
        "required_output_reason": "The operation spreads the histogram and can prepare peaks/troughs. Same-tag docs and7.0.10-61 implementation disagree about clipping;7.1.1-43 implementation and synthetic runtime agree on2%/1%. This cannot establish the requester's unspecified version or readable QR output.",
        "hard_constraint_reason": "No original image/reader/payload or prior specific method is available. Original input/output image links returned403.",
        "literal_evidence_status": "지지(연구판 normalize 동작); 당시판 alias와 QR목표 미확인",
        "partial_support": "Different spellings normalize/contrast-stretch can be equivalent at fixed defaults, while normalize versus brightness-contrast0,90 differ on the same gradient. A/B both leave this third candidate outside the two returned positions.",
        "unknowns": ["requester's version", "previous methods", "original QR decoder result", "author awareness/execution"],
    },
    "IM-U2-C1": {
        "required_output_status": "미확인", "hard_constraint_status": "미확인",
        "validity": "conditional planar rectification component; automation unknown",
        "source_ids": ["IM-O1", "IM-O3", "IM-O4", "FUP-IM-U2-R2", "FUP-IM-U2-C137127563"],
        "official_evidence": [official("IM-O1", OPT, "L2231–2243 Perspective; L2479–2496 canvas/bestfit"), official("IM-O4", PIN + "MagickCore/distort.c", "L1818–1822 default canvas; L1882–1905 bestfit; L2031–2038 viewport")],
        "required_output_reason": "Four measured source corners mapped to a rectangle support planar projective correction. Candidate does not supply an automatic corner detector, destination aspect ratio, operator sign or output bounds. Bent-surface correction is not established.",
        "hard_constraint_reason": "The request asks for automation; the later preproposal revision states physical dimensions unknown. Supplying hand-picked corners in a research test does not satisfy that condition. Original photos returned503.",
        "literal_evidence_status": "지지(조건부 planar component); 자동보정 전체 미확인",
        "partial_support": "The original linked perspective page now404; fixed official docs are later researcher additions. Generic C1 cannot be proven identical to explicit +distort C2.",
        "unknowns": ["automatic corners", "destination dimensions/aspect", "operator sign/bounds", "curvature relevance", "author execution/awareness"],
    },
    "IM-U2-C2": {
        "required_output_status": "미확인", "hard_constraint_status": "미확인",
        "validity": "specified bestfit perspective component; automation/full goal unknown",
        "source_ids": ["IM-O1", "IM-O3", "IM-O4", "FUP-IM-U2-R2", "FUP-IM-U2-C137127563"],
        "official_evidence": [official("IM-O1", OPT, "L2231–2243 Perspective; L2479–2496 +distort"), official("IM-O3", PIN + "MagickWand/operation.c", "L2242–2278 IsPlusOp"), official("IM-O4", PIN + "MagickCore/distort.c", "L1882–1905 bestfit; L2031–2038 viewport")],
        "required_output_reason": "+distort explicitly requests bestfit. On the synthetic translation, -distort is80x60+0+0 and +distort82x62+9+9; with a fixed80x60+0+0 viewport both RGBA outputs match. Candidate does not state that viewport, automatic corner algorithm or a justified target aspect ratio.",
        "hard_constraint_reason": "A same-sized rectangle alone does not solve unknown original physical dimensions or automatic detection. No original input execution and no author reply after C2 are observed.",
        "literal_evidence_status": "지지(+distort bounds semantics); 원 자동화 목표 미확인",
        "partial_support": "This tests both sides of deduplication: signs can change a result, yet a missing state value can make two signs equivalent. Keep C1/C2 separate under the frozen missing-value rule; do not count them as independent request events.",
        "unknowns": ["how corners/target size are determined", "C1 sign unknown", "original photo bytes", "historical output", "author awareness/execution"],
    },
}

rows = []
for c in CANDIDATES:
    cid = c["candidate_id"]
    if c["blank"]:
        rows.append({"candidate_id": cid, "case_id": c["case_id"], "blank": True,
                     "required_output_status": "미확인", "hard_constraint_status": "미확인", "validity": "empty_slot",
                     "source_ids": [], "prior_known": "미확인", "explicit_new_awareness": "미확인", "execution_report": "미확인", "linked_execution": "미확인",
                     "unknowns": ["no third concrete operation in the30-day public window"], "judged_utc": NOW})
        continue
    a = spec[cid]
    a.update({
        "candidate_id": cid, "case_id": c["case_id"], "blank": False,
        "original_rank": c["original_rank"], "original_operation": c["operation"],
        "origin_urls": c["origin_urls"], "original_links": c["original_links"],
        "sealed_a": c["a"], "sealed_b": c["b"], "seal": "4e7539906eb03abd46e6910643ed5317f97ddb45",
        "judged_utc": NOW, "awareness_scope": "whole candidate; partial core familiarity separately coded",
        "explicit_new_awareness": "미확인", "input_version_output_linked_execution": "미확인",
        "eligible_rerecommendation_denominator": False, "eligible_valid_alternative_denominator": False,
        "eligible_known_returned_denominator": False,
        "denominator_reason": "Whole-candidate preproposal knowledge and full required-output/immutable-condition satisfaction are not independently established. Research correction and conceptual plausibility do not qualify.",
        "followup_event_ids": [e["event_id"] for e in FOLLOWUP["events"] if cid in e["candidate_ids"]],
        "historical_version": "7.0.10-61/Cygwin" if c["case_id"] == "IM-A2" else "미확인",
        "reference_version": "ImageMagick7.0.10-61 source/docs; root wrapper fixed references where linked",
        "research_runtime": "ImageMagick7.1.1-43 Q16; original7.0.10-61 not executed",
    })
    a.setdefault("prior_known", "미확인")
    a.setdefault("full_candidate_known", "미확인")
    a.setdefault("execution_report", "미확인")
    a.setdefault("linked_execution", "미확인")
    after = [e for e in FOLLOWUP["events"] if cid in e["candidate_ids"] and e["event_utc"] >= c["first_proposal_utc"]]
    a["no_observed_response"] = not bool(after)
    a["response_scope"] = "Public surviving author records after this candidate; answer-level thanks may not identify an individual operation. Current acceptance is not a dated response."
    a["rejection"] = "미확인"
    a["old_method_retained"] = "미확인"
    if a["required_output_status"] == "반박":
        a["denominator_reason"] = "Frozen literal candidate has independent counterevidence, so it is not a valid-alternative denominator member. Prior whole-candidate awareness remains unknown."
    if cid in ROOT_BY_ID:
        a["root_supplement_assessment"] = ROOT_BY_ID[cid]
        a["execution_receipt"] = "evidence/root-supplement/probe-receipt.json"
    elif c["case_id"] in ["IM-U1", "IM-U2"]:
        a["execution_receipt"] = "evidence/imagemagick/stage3/probes/results.json" if cid != "IM-U1-C2" else None
    rows.append(a)

(OUT / "assessment-part.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
summary = {
    "observed_unit": "candidate, clustered within4 request events", "slots": len(rows),
    "actual_candidates": sum(not x["blank"] for x in rows), "blank_slots": sum(x["blank"] for x in rows),
    "a_returned": sum(bool(x.get("sealed_a", {}).get("returned_rank")) for x in rows),
    "b_returned": sum(bool(x.get("sealed_b", {}).get("returned_rank")) for x in rows),
    "rerecommendation": {"denominator": 0, "a_removed": 0, "b_removed": 0, "missing": 10, "rate": "산출 불가"},
    "valid_alternative_loss": {"denominator": 0, "a_removed": 0, "b_removed": 0, "missing": 9, "noneligible_literal_refuted": 1, "rate": "산출 불가"},
    "known_method_returned": {"denominator": 0, "a_returned": 0, "b_returned": 0, "missing": 10, "rate": "산출 불가"},
    "partial_core_sensitivity": {"candidate_id": "IM-A1-C3", "denominator": 1, "a_removed": 1, "b_removed": 0, "a_returned": 0, "b_returned": 0, "outside_primary_denominator": True},
    "notice": "A filters out5 same-engine candidates; B returns4 additional candidates. None is a confirmed whole-goal valid alternative under the strict evidence rule. This does not prove A superior or B useless; failures and missing data are explicit.",
    "judged_utc": NOW,
}
(OUT / "denominators-part.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(summary, ensure_ascii=False))
