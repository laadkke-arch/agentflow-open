"""Write RGB PNGs from the explicit list of input images."""

import argparse
import json
import os
from pathlib import Path

from PIL import Image, ImageOps


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("policy", choices=("keep", "flat"))
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--direction", choices=("normalize", "raw", "stale"), default="normalize")
    parser.add_argument("--mtime", type=int, default=1650000000)
    args = parser.parse_args()
    for rel in sorted(args.paths):
        relative = Path(rel)
        out = args.target / (relative if args.policy == "keep" else relative.name)
        out.parent.mkdir(parents=True, exist_ok=True)
        old = out.exists()
        with Image.open(args.source / relative) as im:
            old_exif = im.getexif().tobytes()
            converted = im if args.direction == "raw" else ImageOps.exif_transpose(im)
            exif = old_exif if args.direction == "stale" else converted.getexif().tobytes()
            converted.convert("RGB").save(out, exif=exif)
        os.utime(out, (args.mtime, args.mtime))
        print(json.dumps({"src": rel, "dest": out.relative_to(args.target).as_posix(), "replaced_stage_file": old}, ensure_ascii=False))


if __name__ == "__main__":
    main()
