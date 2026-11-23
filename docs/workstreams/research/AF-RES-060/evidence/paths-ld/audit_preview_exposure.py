"""Recount the exact web-reader preview actually displayed to the investigator."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).parent
receipt = json.loads((HERE / "ietf-retry-receipt.json").read_text())
preview = receipt["exposed_excerpts"][0]
numbered = re.findall(r"^L(\d+): ?(.*)$", preview, flags=re.M)
lines = []
for number, text in numbered:
    if int(number) >= 27:
        text = re.sub(r"【\d+†([^】]+)】", r"\1", text)
        text = re.sub(r"^\s*#\s+", "", text)
        lines.append(text)
body = "\n".join(lines)
words = list(re.finditer(r"\S+", body))
extra = body[words[500].start():] if len(words) > 500 else ""
audit = {
    "source_id": "P-SC-036-D3",
    "original_url": "http://tools.ietf.org/html/draft-zyp-json-schema-04",
    "observed_redirect_url": "https://datatracker.ietf.org/doc/html/draft-zyp-json-schema-04",
    "source_ref": "turn507786142view1",
    "preview_receipt_file": "ietf-retry-receipt.json",
    "preview_json_pointer": "/exposed_excerpts/0",
    "preview_sha256_utf8": hashlib.sha256(preview.encode()).hexdigest(),
    "preview_characters": len(preview),
    "preview_whitespace_tokens_including_tool_wrapper": len(preview.split()),
    "body_display_words": len(words),
    "allowed_body_words": 500,
    "excess_body_words": max(0, len(words) - 500),
    "count_rule": "Take actually displayed L27..L98; remove reader line labels, heading markup, and link-reference wrappers; whitespace split exactly as registered.",
    "body_start": "document title JSON Schema: core definitions and terminology",
    "body_end": "partial source line98, Table of Contents 5.General...",
    "overflow_text": extra,
    "overflow_characterization": "Table-of-contents lines only; no implementation or instance-validation evidence",
    "affected_paths": [
        {"case_id": "JS-4", "catalog_id": "SC-036", "path_id": "P3"},
        {"case_id": "JS-6", "catalog_id": "SC-036", "path_id": "P3"},
    ],
    "budget_status": "overexposed_611_of_500",
    "retained_judgment": "unconfirmed",
    "judgment_scope": "Conditions use only the separately stored first500; cutting that stored window does not restore actual protocol compliance.",
    "additional_unique_documents": 0,
    "extra_display_cost": "611 body words were displayed as an additional preview; 111 extend beyond the registered source window. Repeated presentation cost and unique over-window exposure are different units.",
}
(HERE / "preview-exposure.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: audit[k] for k in ["source_id", "preview_sha256_utf8", "body_display_words", "excess_body_words", "budget_status"]}))
