import argparse
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

import bagit
from PIL import Image
from pyhanko.keys import load_cert_from_pemder

from fixtures import NAMES, checked, fingerprint, inspect_pdf


def draw_receipt(pdf, target):
    checked("pdftoppm", "-r", "96", "-singlefile", "-png", pdf, target, cwd=target.parent)
    png = target.with_suffix(".png")
    with Image.open(png) as image:
        return {
            "png": fingerprint(png.read_bytes()),
            "pixels": fingerprint(image.tobytes()),
            "size": image.size,
            "mode": image.mode,
            "title": next(line for line in checked("pdfinfo", pdf, cwd=target.parent).splitlines() if line.startswith("Title:")),
        }


def bag_validation(path):
    bag = bagit.Bag(str(path))
    try:
        bag.validate()
        return {"valid": True, "error": None}
    except bagit.BagValidationError as error:
        return {"valid": False, "error": str(error)}


def state(path):
    status = path.stat()
    return {**fingerprint(path.read_bytes()), "mode": oct(status.st_mode & 0o777),
            "mtime_epoch": int(status.st_mtime)}


def bag_control(signed, work):
    origin = work / "source"
    origin.mkdir()
    shutil.copyfile(signed, origin / "input.pdf")
    (origin / "README.txt").write_text("Synthetic receipt companion for AF-RES-154.\n")
    bagit.make_bag(origin, checksums=["sha256"])
    manifest = (origin / "manifest-sha256.txt").read_text()
    before = bag_validation(origin)
    payload = origin / "data/input.pdf"
    before_attrs = state(payload)
    payload.chmod(0o640)
    os.utime(payload, (1700000000, 1700000000))
    after_attrs = state(payload)
    relocated = work / "receiver"
    origin.rename(relocated)
    after_move = bag_validation(relocated)
    (relocated / "data/README.txt").unlink()
    incomplete = bag_validation(relocated)
    still_pdf = state(relocated / "data/input.pdf")
    subset = work / "valid-subset"
    subset.mkdir()
    shutil.copyfile(signed, subset / "input.pdf")
    bagit.make_bag(subset, checksums=["sha256"])
    smaller = bag_validation(subset)
    if not (before["valid"] and after_move["valid"] and not incomplete["valid"] and smaller["valid"]):
        raise RuntimeError("Bag validation controls did not show the expected outcomes")
    return {
        "tool": "bagit 1.8.1",
        "source_before": "source/data/input.pdf",
        "recipient_after": "receiver/data/input.pdf",
        "before": before, "after_attributes_and_move": after_move,
        "payload_before": before_attrs, "payload_after_attributes": after_attrs,
        "whole_bag_manifest": manifest, "after_companion_removed": incomplete,
        "payload_after_missing_companion": still_pdf,
        "smaller_bag_manifest": (subset / "manifest-sha256.txt").read_text(),
        "smaller_bag_validation": smaller,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, default=Path(__file__).with_name("fixtures"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    folder = args.fixtures.resolve()
    root = load_cert_from_pemder(str(folder / "qa-root.crt"))
    date = datetime.fromisoformat((folder / "validation-time.txt").read_text().strip())
    signed, altered = folder / NAMES["ST"], folder / "invalid-metadata-control.pdf"
    with TemporaryDirectory(prefix="af154-controls-") as temp:
        work = Path(temp)
        reference_render = draw_receipt(signed, work / "reference")
        altered_render = draw_receipt(altered, work / "altered")
        if reference_render["pixels"] != altered_render["pixels"]:
            raise RuntimeError("Tamper control changed rendered page pixels")
        report = {
            "render": {"tool": "Poppler pdftoppm -r 96",
                       "reference": reference_render, "altered": altered_render},
            "reference": inspect_pdf(signed, root, date),
            "altered": inspect_pdf(altered, root, date),
            "bag": bag_control(signed, work),
        }
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
