"""Measure page rules and cell text in the fixed P2 experiment."""

import math
import subprocess
from pathlib import Path

import pymupdf
from PIL import Image

DPI = 288
SCALE = DPI / 72
BLACK_THRESHOLD = 128
SPAN_FRACTION = 0.90
CENTER_ERROR_PT = 0.75
POPPLER = "/usr/bin/pdftoppm"


def rect(box):
    return [round(item, 5) for item in box]


def serialize(value):
    if isinstance(value, (pymupdf.Point, pymupdf.Rect, pymupdf.Quad)):
        return [serialize(item) for item in value]
    if isinstance(value, (tuple, list)):
        return [serialize(item) for item in value]
    if isinstance(value, dict):
        return {key: serialize(item) for key, item in value.items()}
    return value


def bounds(words):
    return [
        min(word[0] for word in words), min(word[1] for word in words),
        max(word[2] for word in words), max(word[3] for word in words),
    ]


def rows_by_y(words):
    rows = []
    for word in sorted(words, key=lambda w: ((w[1] + w[3]) / 2, w[0])):
        y = (word[1] + word[3]) / 2
        if not rows or abs(rows[-1][0] - y) > 1:
            rows.append((y, []))
        rows[-1][1].append(word)
    return [sorted(group, key=lambda w: w[0]) for _, group in rows]


def row_text(row):
    return " ".join(word[4] for word in row)


def recurring_columns(rows):
    clusters = []
    for x in sorted(w[0] for row in rows for w in row):
        if not clusters or abs(x - clusters[-1][0]) > 1:
            clusters.append([])
        clusters[-1].append(x)
    strongest = sorted(clusters, key=lambda group: (-len(group), group[0]))[:2]
    if len(strongest) < 2 or len(strongest[1]) < 2:
        return None
    left, right = sorted(sum(group) / len(group) for group in strongest)
    return (left, right) if right - left >= 10 else None


def horizontal_paths(drawings):
    """Keep individual dark horizontal strokes and thin filled rectangles."""
    spans = []
    for index, path in enumerate(drawings):
        stroke = path.get("color")
        fill = path.get("fill")
        if path.get("stroke_opacity") and stroke and max(stroke) <= 0.5:
            for item in path["items"]:
                if item[0] == "l" and abs(item[1].y - item[2].y) <= 0.05:
                    spans.append(dict(
                        path_index=index, shape="stroke", x=sorted([item[1].x, item[2].x]),
                        y=(item[1].y + item[2].y) / 2, thickness=path.get("width", 0),
                    ))
        if path.get("fill_opacity") and fill and max(fill) <= 0.5:
            for item in path["items"]:
                if item[0] == "re" and 0.25 <= item[1].height <= 3:
                    box = item[1]
                    spans.append(dict(path_index=index, shape="fill", x=[box.x0, box.x1],
                                      y=(box.y0 + box.y1) / 2, thickness=box.height))
    return spans


def raster_page(pdf, page_no, scratch):
    prefix = scratch / f"poppler-p{page_no}"
    args = [POPPLER, "-r", str(DPI), "-gray", "-singlefile", "-f", str(page_no),
            "-l", str(page_no), str(pdf), str(prefix)]
    receipt = subprocess.run(args, capture_output=True, text=True, check=True)
    with Image.open(prefix.with_suffix(".pgm")) as image:
        return image.copy(), dict(argv=args, exit_code=receipt.returncode, stderr=receipt.stderr)


def runs_of_true(flags):
    start = None
    for index, match in enumerate([*flags, False]):
        if match and start is None:
            start = index
        if not match and start is not None:
            yield start, index
            start = None


def raster_section(image, box):
    x0, y0, x1, y1 = box
    left = max(0, math.ceil((x0 + 1) * SCALE))
    right = min(image.width, math.floor((x1 - 1) * SCALE))
    top = max(0, math.floor(y0 * SCALE))
    bottom = min(image.height, math.ceil(y1 * SCALE))
    if right <= left or bottom <= top:
        raise ValueError(f"raster region outside page: {box}")
    width = right - left
    pixels = image.crop((left, top, right, bottom)).tobytes()
    min_span = math.ceil(width * SPAN_FRACTION)
    longest = []
    for offset in range(0, len(pixels), width):
        row = pixels[offset:offset + width]
        longest.append(max((end - start for start, end in runs_of_true(
            [pixel < BLACK_THRESHOLD for pixel in row])), default=0))
    stripes = [
        dict(y_px=[top + start, top + end], center_pt=(top + (start + end) / 2) / SCALE,
             thickness_px=end - start, longest_dark_run_px=max(longest[start:end]))
        for start, end in runs_of_true([span >= min_span for span in longest])
    ]
    return dict(window_px=[left, top, right, bottom], threshold=BLACK_THRESHOLD,
                min_span_px=min_span, longest_dark_each_y_px=longest, stripes=stripes)


def measure_region(spans, image, box, centers=None):
    x0, y0, x1, y1 = box
    rules = []
    rejected = []
    for span in spans:
        xa, xb = span["x"]
        y = span["y"]
        common_width = max(0, min(x1, xb) - max(x0, xa))
        if not y0 <= y <= y1:
            reason = "outside_y"
        elif common_width < (x1 - x0) * SPAN_FRACTION or abs(x0 - xa) > 4 or abs(x1 - xb) > 4:
            reason = "width_or_endpoints"
        elif not 0.25 <= span["thickness"] <= 3:
            reason = "thickness"
        else:
            label = None
            if centers is not None:
                first, last = centers
                label = "top" if y < first else "bottom" if y > last else "interior"
            rules.append(dict(**span, zone=label))
            continue
        rejected.append(dict(path_index=span["path_index"], reason=reason))
    rules.sort(key=lambda item: item["y"])
    raster = raster_section(image, box)
    stripes = raster["stripes"]
    agreement = len(rules) == len(stripes) and all(
        abs(rule["y"] - stripe["center_pt"]) <= CENTER_ERROR_PT
        for rule, stripe in zip(rules, stripes)
    )
    return dict(region_pt=rect(box), vector=rules, rejected_vector=rejected, raster=raster,
                vector_raster_agree=agreement)


def save_crop(image, box, path, margin=4):
    x0, y0, x1, y1 = box
    pixels = (max(0, math.floor((x0 - margin) * SCALE)),
              max(0, math.floor((y0 - margin) * SCALE)),
              min(image.width, math.ceil((x1 + margin) * SCALE)),
              min(image.height, math.ceil((y1 + margin) * SCALE)))
    image.crop(pixels).save(path)


def select_table_rows(rows, heading, headings):
    matches = [i for i, row in enumerate(rows) if row_text(row) == heading]
    if len(matches) != 1:
        return None, []
    index = matches[0]
    chosen = []
    previous = bounds(rows[index])[3]
    gap_limit = 45
    for row in rows[index + 1:]:
        box = bounds(row)
        if row_text(row) in headings or box[1] - previous > gap_limit:
            break
        chosen.append(row)
        previous = box[3]
        gap_limit = 25
    return rows[index], chosen


def read_table(rows, heading, headings, spans, image, output, name):
    heading_row, table_rows = select_table_rows(rows, heading, headings)
    if not table_rows:
        return dict(status="unreadable", error="missing/ambiguous heading or empty body")
    columns = recurring_columns(table_rows)
    if columns is None:
        return dict(status="unreadable", error="two recurring columns unresolved",
                    rows=[row_text(row) for row in table_rows])
    _, right = columns
    entries = []
    for row in table_rows:
        words = [[word for word in row if (word[0] >= right - 2) == bool(col)] for col in (0, 1)]
        entries.append(dict(bbox_pt=rect(bounds(row)), cells=[
            dict(text=row_text(cell), bbox_pt=rect(bounds(cell)) if cell else None)
            for cell in words
        ]))
    x0, y0, x1, y1 = bounds([word for row in table_rows for word in row])
    first = entries[0]["bbox_pt"]
    last = entries[-1]["bbox_pt"]
    roi = [x0, max(bounds(heading_row)[3], y0 - 9), x1, y1 + 9]
    centers = ((first[1] + first[3]) / 2, (last[1] + last[3]) / 2)
    result = measure_region(spans, image, roi, centers)
    crop_path = output / f"{name}.png"
    save_crop(image, roi, crop_path)
    return dict(**result, status="readable" if result["vector_raster_agree"] else "disagree",
                heading=heading, heading_bbox_pt=rect(bounds(heading_row)), columns_pt=columns,
                cell_rows=entries, rows=[[cell["text"] for cell in entry["cells"]] for entry in entries],
                rules_by_zone={zone: sum(rule["zone"] == zone for rule in result["vector"])
                               for zone in ("top", "interior", "bottom")},
                crop=crop_path.name)


def read_pdf(pdf, expected, output, scratch, calibration=False):
    with pymupdf.open(pdf) as doc:
        if len(doc) != 1 or doc[0].rotation != 0:
            raise ValueError("P2 detector expects one unrotated page")
        page = doc[0]
        words = page.get_text("words")
        drawings = page.get_drawings()
        spans = horizontal_paths(drawings)
        image, poppler = raster_page(pdf, 1, scratch)
        rows = rows_by_y(words)
        negatives = []
        for row in rows:
            value = row_text(row)
            if value in ("Test", "OutsideTitle 987") or (value == "1" and bounds(row)[1] > 600):
                x0, y0, x1, y1 = bounds(row)
                measured = measure_region(spans, image, [x0 - 6, y0 - 4, x1 + 6, y1 + 4])
                negatives.append(dict(text=value, **measured))
        if calibration:
            known_box = [72, 140, 144, 148]
            measured = measure_region(spans, image, known_box)
            save_crop(image, known_box, output / "known.png")
            negatives.append(dict(text="underline-length decoy",
                                  **measure_region(spans, image, [72, 177, 144, 187])))
            negatives.append(dict(text="page-edge decoy",
                                  **measure_region(spans, image, [72, 14, 144, 22])))
            # In the page-edge window raster alone sees a band, but vector endpoints disqualify it.
            tables = {"known_rule": measured}
        else:
            headings = {item["heading"] for item in expected.values()}
            tables = {name: read_table(rows, item["heading"], headings, spans, image, output, name)
                      for name, item in expected.items()}
        return dict(page_count=len(doc), page_pt=rect(page.rect), words=serialize(words),
                    drawings=serialize(drawings), horizontal_paths=spans, tables=tables,
                    negatives=negatives, rasterizer=poppler, dpi=DPI)
