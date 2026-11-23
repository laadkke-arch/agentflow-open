"""Run supplemental CSS and Calc scope probes with synthetic two-object inputs."""

import argparse
import io
import shutil
import subprocess
import zipfile
from pathlib import Path

import pymupdf
from PIL import Image, ImageChops

from experiment import HERE, digest, render_env, save_json
from measure import serialize

CSS_STYLES = {
    "baseline": "/* baseline */",
    "all-hidden": "table { border-block-style: hidden; }",
    "one-hidden": "table.suppress { border-block-style: hidden; }",
    "none-conflict": """
      table.suppress { border-block-style: none; }
      table.suppress tr:first-child td { border-top: 4px solid #0044cc; }
      table.suppress tr:last-child td { border-bottom: 4px solid #0044cc; }
    """,
    "hidden-conflict": """
      table.suppress { border-block-style: hidden; }
      table.suppress tr:first-child td { border-top: 4px solid #0044cc; }
      table.suppress tr:last-child td { border-bottom: 4px solid #0044cc; }
    """,
}
XML_NS = (
    'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
    'xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" '
    'xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" '
    'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '
    'xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"'
)
MIME = "application/vnd.oasis.opendocument.spreadsheet"
CALC_CONDITIONS = {
    "shared-on": (("Grid", "Grid"), False),
    "shared-off": (("Plain", "Plain"), False),
    "split": (("Grid", "Plain"), False),
    "one-explicit": (("Plain", "Plain"), True),
}
CELLS = [[("Alpha", 411), ("Beta", 522)], [("Delta", 633), ("Epsilon", 744)]]


def scan_blue(png, box):
    image = Image.open(io.BytesIO(png)).convert("RGB")
    x, y, width, height = (round(box[key]) for key in ("x", "y", "width", "height"))
    blue_rows = []
    for row_y in range(max(0, y - 3), min(image.height, y + height + 3)):
        samples = image.crop((x + 10, row_y, x + width - 10, row_y + 1))
        count = sum(red < 25 and 45 < green < 100 and blue > 170 for red, green, blue in samples.get_flattened_data())
        if count >= 0.9 * samples.width:
            blue_rows.append(row_y)
    bins = []
    for row in blue_rows:
        if bins and row == bins[-1][-1] + 1:
            bins[-1].append(row)
        else:
            bins.append([row])
    return [[group[0], group[-1] + 1] for group in bins]


def css_probe(output, sources):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path="/usr/bin/chromium", headless=True)
        page = browser.new_page(viewport={"width": 700, "height": 460}, device_scale_factor=1)
        fixtures = HERE / "fixtures/cross/scope.html"
        rows = {}
        for name, style in CSS_STYLES.items():
            page.set_content(fixtures.read_text(encoding="utf-8"))
            page.add_style_tag(content=style)
            screenshot = page.screenshot(path=output / (name + ".png"))
            tables = page.locator("table")
            data = []
            for table in tables.all():
                box = table.bounding_box()
                cells = [row.locator("td").all_inner_texts() for row in table.locator("tr").all()]
                data.append(dict(box_px=box, blue_bands_y_px=scan_blue(screenshot, box), rows=cells))
            rows[name] = dict(injected_style=style, tables=data)
        wpt_images = []
        wpt_sha = {}
        for name in ("wpt-html", "wpt-reference"):
            source = sources / name
            page.set_content(source.read_text(encoding="utf-8"))
            image_bytes = page.screenshot(path=output / (name + ".png"))
            wpt_images.append(Image.open(io.BytesIO(image_bytes)).convert("RGB"))
            wpt_sha[name] = digest(source)
        diff = ImageChops.difference(*wpt_images)
        result = dict(engine=browser.version, input_sha256=digest(fixtures), conditions=rows,
                      wpt=dict(source_sha256=wpt_sha, exact_raster_match=diff.getbbox() is None,
                               diff_bounds_px=diff.getbbox()))
        browser.close()
    save_json(output / "css.json", result)


def sheet_xml(index, explicit_border):
    rows = []
    for offset, (label, number) in enumerate(CELLS[index]):
        attr = ' table:style-name="EdgeTop"' if offset == 0 else ' table:style-name="EdgeBottom"'
        attr = attr if explicit_border and index == 0 else ""
        rows.append(
            f'<table:table-row><table:table-cell{attr} office:value-type="string"><text:p>{label}</text:p>'
            f'</table:table-cell><table:table-cell{attr} office:value-type="float" office:value="{number}">'
            f'<text:p>{number}</text:p></table:table-cell></table:table-row>'
        )
    sheet = f"Sheet{index + 1}"
    return (f'<table:table table:name="{sheet}" table:style-name="Tab{index}" '
            f'table:print-ranges="{sheet}.A1:{sheet}.B2"><table:table-column table:number-columns-repeated="2"/>'
            f'{"".join(rows)}</table:table>')


def ods(path, style_pair, explicit_border):
    layout = '''
    <style:page-layout style:name="PL{name}">
      <style:page-layout-properties fo:page-width="8.5in" fo:page-height="11in"
        fo:margin="1in" style:print-orientation="portrait" style:print="{flag}"/>
    </style:page-layout>
    '''
    master = '<style:master-page style:name="{0}" style:page-layout-name="PL{0}"/>'
    styles = (f'<office:document-styles {XML_NS} office:version="1.3"><office:styles/>'
              f'<office:automatic-styles>{layout.format(name="Grid", flag="grid")}'
              f'{layout.format(name="Plain", flag="")}</office:automatic-styles>'
              f'<office:master-styles>{master.format("Grid")}{master.format("Plain")}'
              f'</office:master-styles></office:document-styles>')
    table_styles = "".join(f'<style:style style:name="Tab{index}" style:family="table" style:master-page-name="{style}"/>'
                           for index, style in enumerate(style_pair))
    cell_styles = "".join(
        f'<style:style style:name="Edge{edge.title()}" style:family="table-cell"><style:table-cell-properties '
        f'fo:border-{edge}="0.035cm solid #cc0000"/></style:style>' for edge in ("top", "bottom")
    )
    content = (f'<office:document-content {XML_NS} office:version="1.3">'
               f'<office:automatic-styles>{table_styles}{cell_styles}</office:automatic-styles>'
               f'<office:body><office:spreadsheet>{sheet_xml(0, explicit_border)}{sheet_xml(1, explicit_border)}'
               '</office:spreadsheet></office:body></office:document-content>')
    manifest = f'''
    <manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.3">
      <manifest:file-entry manifest:full-path="/" manifest:media-type="{MIME}"/>
      <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
      <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
    </manifest:manifest>
    '''
    with zipfile.ZipFile(path, mode="x") as archive:
        for name, data in {"mimetype": MIME, "content.xml": content, "styles.xml": styles,
                           "META-INF/manifest.xml": manifest}.items():
            item = zipfile.ZipInfo(name)
            archive.writestr(item, data)


def calc_probe(output, work):
    libreoffice = shutil.which("soffice")
    if libreoffice is None:
        raise SystemExit("soffice is required for the separate Calc experiment")
    version = subprocess.check_output([libreoffice, "--version"], text=True).strip()
    outcomes = {}
    for name, (styles, borders) in CALC_CONDITIONS.items():
        original = output / (name + ".ods")
        ods(original, styles, borders)
        isolated = work / name
        env = render_env(isolated, work / "shared")
        args = [libreoffice, "-env:UserInstallation=" + (isolated / "profile").as_uri(),
                "--headless", "--convert-to", "pdf", "--outdir", str(output), str(original)]
        invocation = subprocess.run(args, capture_output=True, text=True, env=env, timeout=60, check=False)
        pdf = original.with_suffix(".pdf")
        receipt = dict(args=args, exit_code=invocation.returncode, stdout=invocation.stdout, stderr=invocation.stderr,
                       ods_sha256=digest(original), applied_page_styles=styles, explicit_cell_borders=borders)
        if pdf.exists():
            with pymupdf.open(pdf) as pdf_doc:
                receipt["pdf_sha256"] = digest(pdf)
                receipt["pages"] = [dict(text=page.get_text(), drawings=serialize(page.get_drawings()))
                                    for page in pdf_doc]
        outcomes[name] = receipt
    save_json(output / "calc.json", dict(engine=version, results=outcomes))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", type=Path, required=True, help="folder with wpt-html and wpt-reference")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    args = parser.parse_args()
    output, work = args.output.resolve(), args.work.resolve()
    output.mkdir(parents=True)
    work.mkdir(parents=True)
    css_probe(output, args.sources.resolve())
    calc_probe(output, work)


if __name__ == "__main__":
    main()
