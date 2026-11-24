"""Regenerate the two synthetic one-bit PNG fixtures with Pillow and libraqm."""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, features

SIZE = (1200, 400)
TEXT = ("OFFLINE OCR CHECK", "اختبار القراءة")


def render(font_path: Path, output: Path) -> None:
    if not features.check_feature("raqm"):
        raise SystemExit("Pillow must have libraqm for Arabic shaping")
    output.mkdir(parents=True, exist_ok=True)
    blank = Image.new("L", SIZE, "white")
    page = blank.copy()
    draw = ImageDraw.Draw(page)
    font = ImageFont.truetype(str(font_path), 64, layout_engine=ImageFont.Layout.RAQM)
    draw.text((80, 62), TEXT[0], fill=0, font=font, anchor="lt", direction="ltr")
    draw.text((80, 210), TEXT[1], fill=0, font=font, anchor="lt", direction="rtl", language="ar")
    for name, image in (("page", page), ("blank", blank)):
        image.convert("1", dither=Image.Dither.NONE).save(output / f"{name}.png", dpi=(300, 300))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("font", type=Path)
    parser.add_argument("output", type=Path)
    options = parser.parse_args()
    render(options.font, options.output)
