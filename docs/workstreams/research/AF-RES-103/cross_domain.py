"""Reproduce the WPT reftest and scoped Graphviz fixtures."""
import argparse
from base64 import b64encode
import json
from pathlib import Path
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET

from PIL import Image, ImageChops

from browser_probe import Browser
from run import ROOT, digest, utc, write

FIXTURES = ROOT / "evidence/cross-fixtures"
SVG = "{http://www.w3.org/2000/svg}"


def pixels(file):
    im = Image.open(file).convert("RGB")
    hues = {"green":(0,128,0), "red":(255,0,0), "black":(0,0,0)}
    return {name:dict(zip(("count","first","last"), color_pixels(im,rgb))) for name,rgb in hues.items()}


def color_pixels(im, rgb):
    count, first, last = 0, None, None
    pix = im.load()
    for y in range(im.height):
        for x in range(im.width):
            if pix[x,y] == rgb:
                count += 1
                if first is None:
                    first = [x,y]
                last = [x,y]
    return count, first, last


def wpt(browser, root):
    shutil.copyfile(FIXTURES/"wpt-test.html",root/"wpt-test.html")
    shutil.copyfile(FIXTURES/"wpt-expected.xht",root/"wpt-expected.xht")
    original = (root/"wpt-test.html").read_bytes()
    payload = re.search(rb"<svg\b.*?</svg>",original,re.S).group()
    (root/"payload.svg").write_bytes(payload)
    clone = (b'<!doctype html><meta charset="utf-8"><style>body{margin:0} div{color:green;'
             b'float:left;width:300px;height:150px;} img{display:block;width:300px;height:150px}</style>'
             b'<div id="inline">' + payload + b'</div><div id="external"><img src="payload.svg"></div>')
    (root/"host.html").write_bytes(clone)
    # Identical payload with an explicit presentation attribute tests whether img can display the color.
    literal_green = payload.replace(b"currentColor",b"green")
    (root/"explicit-green.svg").write_bytes(literal_green)
    (root/"literal.html").write_bytes(clone.replace(b'src="payload.svg"',b'src="explicit-green.svg"'))
    start = utc()
    test = browser.probe(root/"wpt-test.html",root,"wpt",
                         extra=("#container rect",),per_image=False)
    expected = browser.probe(root/"wpt-expected.xht",root,"wpt-expected",per_image=False)
    host = browser.probe(root/"host.html",root,"host",
                         extra=("#inline rect","#external img"),per_image=False)
    literal = browser.probe(root/"literal.html",root,"literal",
                            extra=("#inline rect","#external img"),per_image=False)
    png = Image.open(root/"host.png").convert("RGB")
    literal_png = Image.open(root/"literal.png").convert("RGB")
    return {"started_utc":start, "ended_utc":utc(), "source":digest(root/"wpt-test.html"),
            "expected_input":digest(root/"wpt-expected.xht"), "same_payload":digest(root/"payload.svg"),
            "original_wpt":test, "reference":expected, "host":host, "literal_control":literal,
            "expected":{"original_wpt":"green 100x100, no red",
                        "same_payload_inline":"green","same_payload_external":"black",
                        "literal_external":"green"},
            "actual":{
                "wpt_color_counts":pixels(root/"wpt.png"),
                "expected_color_counts":pixels(root/"wpt-expected.png"),
                "wpt_full_raster_equal":ImageChops.difference(Image.open(root/"wpt.png").convert("RGB"),
                    Image.open(root/"wpt-expected.png").convert("RGB")).getbbox() is None,
                "inline_center":png.getpixel((50,50)),
                "external_center":png.getpixel((350,50)),
                "literal_external_center":literal_png.getpixel((350,50)),
            }}


def graph_symbols(path):
    svg = ET.parse(path).getroot()
    groups = {}
    for g in svg.findall(".//"+SVG+"g"):
        key = g.attrib.get("class")
        title = g.findtext(SVG+"title")
        if key not in ("node","edge","cluster") or not title:
            continue
        groups[title] = {"class":key,"paints":[{"shape":e.tag.removeprefix(SVG), "fill":e.get("fill"),
            "stroke":e.get("stroke"),"points":e.get("points"),"d":e.get("d")} for e in g
            if e.tag.removeprefix(SVG) in ("path","polygon","ellipse","polyline")],
            "label":[x.text for x in g.findall(SVG+"text")]}
    return groups


def graphviz(browser, root):
    result = {}
    for name in ("clusters","scope","flattened","swapped"):
        path = root/(name+".gv")
        if name == "swapped":
            source = (FIXTURES/"scope.gv").read_text()
            a = source.index("  subgraph alpha")
            b = source.index("  subgraph beta")
            c = source.index("  outside")
            path.write_text(source[:a]+source[b:c]+source[a:b]+source[c:])
        else:
            shutil.copyfile(FIXTURES/(name+".gv"),path)
        svg = root/(name+".svg")
        cmd = [shutil.which("dot"),"-Tsvg",path.name,"-o",svg.name]
        start = utc()
        p = subprocess.run(cmd,cwd=root,capture_output=True,check=False)
        (root/(name+".stdout")).write_bytes(p.stdout)
        (root/(name+".stderr")).write_bytes(p.stderr)
        res = {"argv":cmd,"exit":p.returncode,"started_utc":start,"ended_utc":utc(),
               "input":digest(path)}
        if not p.returncode:
            res["svg"] = digest(svg)
            res["symbols"] = graph_symbols(svg)
            html = root/(name+".html")
            markup = '<!doctype html><meta charset="utf-8"><img src="data:image/svg+xml;base64,'
            html.write_text(markup+b64encode(svg.read_bytes()).decode()+'">\n')
            res["browser"] = browser.probe(html,root,name,per_image=False)
        result[name] = res
    result["expectations"] = {
        "clusters":"a0–a3 white fill, b0–b3 lightgrey fill, directed arrows",
        "scope":"shared and a0 red, b0 blue, outside black; edges to a0, b0, outside red vee, blue dot, black normal",
        "flattened":"all nodes & arrows blue; dot on all arrows",
        "swapped":"shared now blue; subgraph-specific and outside edge arrow types as before",
    }
    result["upstream_expected"] = {
        **digest(FIXTURES/"clusters-expected.ps"),
        "excerpt":"tests/nshare/clusters_dot.ps a0 ~L220 white nodecolor, b0 ~L435 lightgrey 0.82745 nodecolor",
    }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True,exist_ok=False)
    with Browser(shutil.which("chromium")) as browser:
        write(out/"wpt.json",wpt(browser,out))
        write(out/"graphviz.json",graphviz(browser,out))
    print(json.dumps({"wpt":str(out/"wpt.json"),"graphviz":str(out/"graphviz.json")}))


if __name__ == "__main__":
    main()
