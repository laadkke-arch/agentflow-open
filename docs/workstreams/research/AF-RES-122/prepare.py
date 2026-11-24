"""Recreate the fixed lexical projection from reader-supplied opening text."""

import argparse
import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path


HERE = Path(__file__).resolve().parent
NAME_PART = r"[A-Za-z_][A-Za-z0-9_]*"
DOTTED_NAME = re.compile(rf"(?<![A-Za-z0-9_]){NAME_PART}(?:\.{NAME_PART})*")
ENGLISH = re.compile(r"[A-Za-z0-9_]+")
KOREAN_WORD = re.compile(r"[가-힣]+")
KOREAN_RUN = re.compile(r"[가-힣]+(?:\s+[가-힣]+)*")
URL_OR_PATH = re.compile(
    r"https?://[^\s\x60<>\"'】]+"
    r"|(?<![A-Za-z0-9_])(?:[A-Za-z]:\\|~/|\.\.?/|/)[^\s\x60<>\"'()\[\],:]+"
    r"|(?<![A-Za-z0-9_./])(?:[\w.-]+/)+[\w.-]+\.[A-Za-z0-9]+"
)
OTHER_RECEIVERS = {
    "numpy", "np", "pandas", "pd", "tf", "tensorflow", "jax", "jnp",
    "torchvision", "torchtext", "PIL", "cv2", "nn",
}
TENSOR_FUNCTIONS = {"reshape", "permute", "transpose", "clone"}
DATA_MODULES = {
    "torch.utils.data.dataloader": {"DataLoader", "default_collate", "default_convert"},
    "torch.utils.data.dataset": {"IterableDataset", "TensorDataset", "Subset"},
    "torch.utils.data.sampler": {"BatchSampler", "WeightedRandomSampler"},
    "torch.utils.data._utils.collate": {"default_collate", "default_convert"},
}


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def read_jsonl(path):
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def packed(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def names_for(cards):
    names = {}
    tensor_methods = {}
    for card in cards:
        feature = card["feature_id"]
        title = card["english_title"]
        names[card["symbol"]] = feature
        names[title] = feature
        if feature.startswith("T"):
            tensor_methods[title] = feature
            names[f"Tensor.{title}"] = feature
            if title in TENSOR_FUNCTIONS:
                names[f"torch.{title}"] = feature
        else:
            for module, exports in DATA_MODULES.items():
                if title in exports:
                    names[f"{module}.{title}"] = feature
    return names, tensor_methods


def find_spans(text, names, tensor_methods):
    excluded = [match.span() for match in URL_OR_PATH.finditer(text)]
    for match in DOTTED_NAME.finditer(text):
        start, end = match.span()
        if any(left < end and start < right for left, right in excluded):
            continue
        spelling = match.group()
        feature = names.get(spelling)
        if feature is None and "." in spelling:
            receiver, title = spelling.rsplit(".", 1)
            root = receiver.split(".", 1)[0]
            if root in OTHER_RECEIVERS or root == "torch":
                continue
            if not text[end:].lstrip().startswith("("):
                continue
            feature = tensor_methods.get(title)
            start = end - len(title)
        if feature:
            yield {
                "feature_id": feature,
                "start": start,
                "end": end,
                "before": text[start:end],
                "after": " " * (end - start),
            }


def projection(text, spans, english_vocab, korean_vocab):
    english_positions = {}
    for match in ENGLISH.finditer(text):
        word = match.group().lower()
        if word in english_vocab:
            english_positions.setdefault(word, []).append(match.start())

    korean_sequences = []
    for group in KOREAN_RUN.finditer(text):
        sequence = [
            [group.start() + match.start(), match.group()]
            if match.group() in korean_vocab else None
            for match in KOREAN_WORD.finditer(group.group())
        ]
        if any(item is not None for item in sequence):
            korean_sequences.append(sequence)

    return {
        "english_positions": english_positions,
        "korean_sequences": korean_sequences,
        "exact_ids": sorted({span["feature_id"] for span in spans}),
    }


def prepare(snapshots, cards, aliases):
    english_vocab = {
        word.lower() for card in cards for word in ENGLISH.findall(card["english_terms"])
    }
    korean_vocab = {
        word for alias in aliases if alias["status"] == "active"
        for word in KOREAN_WORD.findall(alias["surface"])
    }
    names, tensor_methods = names_for(cards)
    views = []
    audits = []
    for snapshot in snapshots:
        request = snapshot["request_id"]
        original = snapshot["body"]
        raw = unicodedata.normalize("NFC", original)
        spans = list(find_spans(raw, names, tensor_methods))
        masked_chars = list(raw)
        for span in spans:
            masked_chars[span["start"]:span["end"]] = span["after"]
        masked = "".join(masked_chars)
        masked_spans = list(find_spans(masked, names, tensor_methods))
        if len(masked) != len(raw) or masked_spans:
            raise ValueError(f"{request}: mask changed offsets or left an exact API match")
        for label, body, matches in [("raw", raw, spans), ("masked", masked, masked_spans)]:
            view = projection(body, matches, english_vocab, korean_vocab)
            views.append({
                "request_id": request,
                "view": label,
                "view_sha256": sha(body),
                "projection_sha256": sha(packed(view)),
                **view,
            })
        audits.append({
            "request_id": request,
            "original_sha256": sha(original),
            "raw_nfc_sha256": sha(raw),
            "masked_nfc_sha256": sha(masked),
            "same_without_symbol": not spans and raw == masked,
            "normalized_codepoints": len(raw),
            "mask": spans,
        })
    return views, audits


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(packed(row) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--views", required=True, type=Path)
    parser.add_argument("--audit", required=True, type=Path)
    args = parser.parse_args()
    views, audits = prepare(
        read_jsonl(args.input), read_csv(HERE / "catalog.csv"), read_csv(HERE / "aliases.csv")
    )
    write_jsonl(args.views, views)
    write_jsonl(args.audit, audits)


if __name__ == "__main__":
    main()
