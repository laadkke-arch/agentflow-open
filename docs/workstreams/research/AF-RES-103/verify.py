#!/usr/bin/env python3
"""Re-read saved PDFs, SVG payloads, Chromium crops and ledgers."""
from collections import Counter
from copy import deepcopy
from itertools import groupby
import json
from pathlib import Path
import re

import fitz
from PIL import Image, ImageChops, ImageFilter

from run import ANSWER_NAME, D, INPUTS, PLAN, ROOT, digest, write

REF = json.loads((D/"REFERENCE_SEAL.json").read_text())["cases"]
TOLERANCE_PT = 0.02
MASK_THRESHOLD = 0.68


def read(file):
    return json.loads(file.read_text())


def translated_positions_match(actual, expected, actual_origin, expected_origin):
    return all(abs((x-a)-(y-b)) <= TOLERANCE_PT
               for x,y,a,b in zip(actual,expected,actual_origin,expected_origin))


def center(path):
    a,b,c,d = path["bbox_pt"]
    return [(a+c)/2,(b+d)/2]


def point_text_box(word):
    return word[:4]


def masked(image):
    return image.convert("L").point(lambda x:255 if x < 236 else 0)


def hue_mask(image, dominant):
    channels = list(image.split())
    primary = channels.pop(dominant)
    difference = ImageChops.subtract(primary,ImageChops.lighter(*channels))
    return difference.point(lambda x:255 if x>17 else 0)


def dominant_channel(rgb):
    if rgb is None or max(rgb)-min(rgb) < 0.15:
        return None
    return rgb.index(max(rgb))


def agreement(ref, actual):
    """Two directional coverages with a tolerance of two output pixels."""
    coverage = []
    for a,b in ((ref,actual),(actual,ref)):
        total = a.histogram()[255]
        common = ImageChops.darker(a,b.filter(ImageFilter.MaxFilter(5))).histogram()[255]
        coverage.append(round(common/total,4) if total else None)
    return coverage


class Pixels:
    def __init__(self, pdf_page, browser_image):
        self.size = browser_image.size
        self.width, self.height = self.size
        self.sx, self.sy = self.width/pdf_page.rect.width, self.height/pdf_page.rect.height
        pix = pdf_page.get_pixmap(matrix=fitz.Matrix(self.sx,self.sy),alpha=False)
        pdf_rgb = Image.frombytes("RGB",[pix.width,pix.height],pix.samples).resize(self.size, Image.Resampling.LANCZOS)
        self.colors = [pdf_rgb,browser_image]
        self.ink = [masked(image) for image in self.colors]
        self.hues = {c:[hue_mask(image,c) for image in self.colors] for c in (0,2)}

    def box(self, coords):
        x0,y0,x1,y1 = coords
        return (round(x0*self.sx),round(y0*self.sy),round(x1*self.sx),round(y1*self.sy))

    def compare(self, coords, padding=2.0, channel=None):
        x0,y0,x1,y1 = coords
        window = self.box([x0-padding,y0-padding,x1+padding,y1+padding])
        return agreement(*[im.crop(window) for im in (self.ink if channel is None else self.hues[channel])])

    def at(self,x,y):
        location = (round(x*self.sx),round(y*self.sy))
        return [list(im.getpixel(location)) for im in self.colors]


def match_rgb(a,b):
    return a is not None and b is not None and all(abs(x-y)<0.002 for x,y in zip(a,b))


def graph_elements(page, figures, pixels):
    """Assign shaft/head by paint sequence and identify labels from PDF words."""
    words = page["words"]
    starts = [i for i,w in enumerate(words) if w[4]=="q1"]
    assert len(starts)==len(figures), (len(starts),len(figures))
    assert len(page["paths"])==24*len(figures)
    observations = []
    for index,(at,ref) in enumerate(zip(starts,figures)):
        state_words = words[at:at+4]
        label_words = words[at+4:at+12]
        seqs = page["paths"][24*index:24*index+24]
        current_center = center(seqs[0])
        expected_center = ref["states"][0]["center"]

        def positions(a,b):
            return translated_positions_match(a,b,current_center,expected_center)
        def bbox_positions(a,b):
            return positions(a[:2],b[:2]) and positions(a[2:],b[2:])

        states = []
        for want,word,path_index in zip(ref["states"],state_words,[0,4,5,6]):
            shape = seqs[path_index]
            x,y = center(shape)
            fill_sample_pt = [x+6,y+4]
            pdf_rgb, browser_rgb = pixels.at(*fill_sample_pt)
            states.append({
                "id":word[4],"center":center(shape),"bbox":word[:4],
                "stroke":shape["stroke"],"fill":shape["fill"],
                "identity_position":word[4]==want["id"] and positions(center(shape),want["center"])
                    and bbox_positions(word[:4],want["bbox"]),
                "pdf_colors_match":match_rgb(shape["stroke"],want["stroke_rgb"])
                    and match_rgb(shape["fill"],want["fill_rgb"]),
                "ring_capture":pixels.compare(shape["bbox_pt"]),
                "ring_color_capture":pixels.compare(shape["bbox_pt"],channel=dominant_channel(shape["stroke"])),
                "glyph_capture":pixels.compare(point_text_box(word)),
                "interior_sample":{"point":fill_sample_pt,"reference_rgb":pdf_rgb,"browser_rgb":browser_rgb},
            })
        edges = []
        for edge,word,stem,tip in zip(ref["edges"],label_words,seqs[8::2],seqs[9::2]):
            start,end = stem["items"][0][1],stem["items"][-1][-1]
            head = tip["items"][0][1]
            edges.append({
                "id":edge["id"],"expected_source":edge["from_to_label"],"label":word[4],
                "shaft_start":start,"shaft_end":end,"head_tip":head,"head_color":tip["fill"],
                "shaft_color":stem["stroke"],
                "direction":positions(start,edge["start"]) and positions(end,edge["shaft_end"])
                     and positions(head,edge["head_tip"]),
                "label_position_match":word[4]==edge["label"] and bbox_positions(word[:4],edge["label_bbox"]),
                "pdf_colors_match":match_rgb(stem["stroke"],edge["stroke_rgb"])
                    and match_rgb(tip["fill"],edge["head_fill_rgb"]),
                "tip_capture":pixels.compare(tip["bbox_pt"]),
                "shaft_capture":pixels.compare(stem["bbox_pt"]),
                "shaft_color_capture":pixels.compare(stem["bbox_pt"],channel=dominant_channel(stem["stroke"])),
                "head_color_capture":pixels.compare(tip["bbox_pt"],channel=dominant_channel(tip["fill"])),
                "glyph_capture":pixels.compare(point_text_box(word)),
            })
        accepting = [seqs[1],seqs[7]]
        start = seqs[3]["items"][0][1]
        observations.append({"id":ref["id"],"states":states,"edges":edges,
                             "initial_match":positions(start,ref["initial_arrow_tip"]),
                             "initial_capture":pixels.compare(seqs[3]["bbox_pt"]),
                             "acceptance_stroke_match":[p["stroke"]==[1,1,1] and
                                  len(p["items"])==4 and all(it[0]=="c" for it in p["items"]) for p in accepting],
                             "acceptance_capture":[pixels.compare(p["bbox_pt"]) for p in accepting]})
    return observations


def graph_match(one):
    def pixels(values):
        return all(value is not None and value>=MASK_THRESHOLD for value in values)
    return (
        all(x["identity_position"] and x["pdf_colors_match"] and pixels(x["ring_capture"]) and pixels(x["glyph_capture"]) and pixels(x["ring_color_capture"])
            and max(abs(a-b) for a,b in zip(x["interior_sample"]["reference_rgb"],x["interior_sample"]["browser_rgb"]))<=4
            for x in one["states"])
        and all(x["direction"] and x["label_position_match"] and x["pdf_colors_match"] and pixels(x["tip_capture"])
                and pixels(x["shaft_capture"]) and pixels(x["glyph_capture"]) and pixels(x["shaft_color_capture"])
                and pixels(x["head_color_capture"]) for x in one["edges"])
        and one["initial_match"] and pixels(one["initial_capture"]) and all(one["acceptance_stroke_match"])
        and all(pixels(s) for s in one["acceptance_capture"])
    )


def plots(page, figures, pixels):
    drawing = [p for p in page["paths"] if p["stroke"]==[0,0,1] or p["fill"]==[0,0,1]]
    assert len(drawing)==2*len(figures)
    measurements=[]
    for fig,stem,tip in zip(figures,drawing[::2],drawing[1::2]):
        vertices = [stem["items"][0][1]]+[it[-1] for it in stem["items"]]
        head = tip["items"][0][1]
        viewport = [min(stem["bbox_pt"][0],tip["bbox_pt"][0]),min(stem["bbox_pt"][1],tip["bbox_pt"][1]),
                    max(stem["bbox_pt"][2],tip["bbox_pt"][2]),max(stem["bbox_pt"][3],tip["bbox_pt"][3])]
        subset = [word for word in page["words"] if viewport[1]-15 < word[1] < viewport[3]+15]
        measurements.append({"id":fig["id"],"view":fig["view"],"projected_vertices":vertices,
              "arrow_tip":head,"rgb":[0,0,255],"page":page["page"],
              "heading_in_pdf":fig["heading_pdf"] in page["text_stream"],
              "projection_matches":vertices_close(vertices,fig["projected_vertices"]) and
                                   vertices_close([head],[fig["arrow_tip"]]),
              "blue_capture":pixels.compare(viewport,channel=2),
              "head_capture":pixels.compare(tip["bbox_pt"],channel=2),
              "tick_capture":[{"text":w[4],"box":w[:4],"coverage":pixels.compare(w[:4],padding=1.5)}
                              for w in subset if re.search(r"[0-9]",w[4]) and "{" not in w[4]]})
    return measurements


def vertices_close(a,b):
    return len(a)==len(b) and all(abs(x-y)<TOLERANCE_PT for p,q in zip(a,b) for x,y in zip(p,q))


def plot_match(a):
    values=a["blue_capture"]+a["head_capture"]
    return a["heading_in_pdf"] and a["projection_matches"] and all(x is not None and x>=MASK_THRESHOLD for x in values)


def view_assets(slot, entry):
    route = entry["route"]
    if route=="P":
        file = slot/(ANSWER_NAME+".pdf")
        yield file,read(file.with_suffix(".observed.json"))
    elif route=="K":
        for file in sorted((slot/"children").glob("*/diagram.pdf")):
            yield file,read(file.with_suffix(".observed.json"))
    else:
        for file in sorted(slot.glob("g*.pdf")):
            yield file,read(file.with_suffix(".observed.json"))


def summarize(entry):
    slot = ROOT/entry["path"]
    case = entry["input"]
    inp = INPUTS["inputs"][case]
    route = entry["route"]
    if not entry["html"]:
        return {"result":"failure","stage":entry["first_failure"],"browser":"미확인",
                "ast":entry["raw_ast"],"child":entry["matched_filter_compiles"]}
    browser,moved,xml = (read(slot/name) for name in ("browser.json","moved.json","svg.json"))
    assert browser["status"]==moved["status"]=="viewed"
    observed = []
    whole_pages = []
    asset_index=0
    figures = REF[case]["figures"]
    for pdf, pages in view_assets(slot,entry):
        with fitz.open(pdf) as doc:
            for idx,page in enumerate(pages):
                image = browser["images"][asset_index]
                with Image.open(slot/image["screenshot"]) as shot:
                    px = Pixels(doc[idx],shot.convert("RGB"))
                    if route=="P":
                        bounds = [0,0,*page["size_pt"]]
                        full = px.compare(bounds,padding=0)
                        whole_pages.append({"page":idx+1,"whole_capture":full,
                                            "text_stream_identical":page["text_stream"]==REF[case]["pdf_text_stream"][idx]})
                    if case=="T2":
                        selected = [f for f in figures if f["page"]==idx+1]
                        observed += plots(page,selected,px)
                    elif route=="P":
                        observed += graph_elements(page,figures,px)
                    else:
                        observed += graph_elements(page,[figures[asset_index]],px)
                asset_index+=1
    if case=="T2":
        visual = [plot_match(x) for x in observed]
    else:
        visual = [graph_match(x) for x in observed]
    original_sentences = inp["body_sentences"]
    selected_sentences = [s for s in original_sentences if browser["find"][s]["found"] and browser["find"][s]["selected"]==s]
    order_lookup = {s:f"s{i}" for i,s in enumerate(original_sentences,1)}
    order = [f'g{x["image"]}' if "image" in x else order_lookup.get(x["text"],x["text"]) for x in browser["order"]]
    img = [{"natural":x["natural"],"rendered":x["rendered"],"alt":x["alt"],
            "decoded":x["decoded"],"svg_sha256":x.get("svg_payload_sha256")} for x in browser["images"]]
    svg_sizes = {name:meta["sha256"] for name,meta in xml.items()}
    payload_exact = sorted(svg_sizes.values())==sorted(x["svg_sha256"] for x in img)
    assert payload_exact
    moved_ok = all(a["natural"]==b["natural"] and a["svg_payload_sha256"]==b["svg_payload_sha256"] and b["decoded"]
                   for a,b in zip(browser["images"],moved["images"])) and len(moved["images"])==len(img)
    external = [req for req in moved["requests"] if req!="http://127.0.0.1:8765/output.html"]
    host = {"selectable":len(selected_sentences),"expected":len(original_sentences),"order":order,
            "headings_found":sum(x["found"] for x in browser["find"].values()) if case=="T2" else None,
            "expected_order":inp["body_order"],"found":selected_sentences}
    shape_ok = len(observed)==inp["pictures"] and all(visual)
    page_ok = len(whole_pages)==inp["pdf_pages"] and all(
        all(x is not None and x>=MASK_THRESHOLD for x in p["whole_capture"]) and p["text_stream_identical"]
        for p in whole_pages)
    route_ok = page_ok if route=="P" else len(img)==inp["pictures"] and order==inp["body_order"] and len(selected_sentences)==len(original_sentences)
    return {"result":"success" if shape_ok and route_ok and moved_ok and not external else "failure",
            "ast":entry["raw_ast"],"figures":observed,"geometry_browser_matches":visual,
            "primary_image":img,"host":host,"moved":{"images_match":moved_ok,"external":external,
                                                 "requests":moved["requests"],"transport":moved["transport"]},
            "svg_payloads_exact":payload_exact,"svg_files":svg_sizes,"pages":whole_pages}


def repeat_pairs(entries, findings):
    comparisons=[]
    main = sorted(entries,key=lambda e:(e["input"],e["route"],e["repeat"]))
    for key,pair in groupby(main,key=lambda e:(e["input"],e["route"])):
        first,second = list(pair)
        a,b = [findings[e["id"]] for e in (first,second)]
        keys = ["result","stage","ast","geometry_browser_matches","host","moved"]
        assert all(a.get(k)==b.get(k) for k in keys),(key,a.get("result"),b.get("result"))
        one,two = (x["files"] for x in (first,second))
        def fingerprint_match(suffix):
            observed = [{k:v["sha256"] for k,v in data.items() if k.endswith(suffix)}
                        for data in (one,two)]
            return (observed[0]==observed[1]) if observed[0] and observed[1] else None
        comparisons.append({
            "input":key[0],"route":key[1],"meaning_match":True,
            "html_byte_match":fingerprint_match("output.html"),"svg_byte_match":fingerprint_match(".svg"),
            "pdf_byte_match":fingerprint_match(".pdf"),"browser_png_byte_match":fingerprint_match("browser.png"),
            "reader_ast_byte_match":fingerprint_match("reader.json"),
        })
    return comparisons


def check_controls():
    def pdf(name, stem):
        return read(D/"controls"/name/(stem+".observed.json"))[0]
    def e2_color(name, stem):
        return [round(255*y) for y in pdf(name,stem)["paths"][10]["stroke"]]
    checks = {q:{"g1_e2_rgb":e2_color(q,"g1"),"g2_e2_rgb":e2_color(q,"g2")}
              for q in ("T3-M-no-new-style","T3-M-reverse-styles","T4-M-no-inner",
                        "T4-M-reverse-styles","T4-M-leak-inner","T3-M-unused","T3-M-same-label")}
    for name in ("T1-M-no-color","T3-M-no-red"):
        row = read(D/"controls"/name/"receipt.json")
        checks[name]=row["first_failure"]
    x = pdf("T1-M-no-tikzset","g1")
    checks["T1-M-no-tikzset"]={"path_count":len(x["paths"]), "text_stream":x["text_stream"],
        "stroke_fill":[(d["type"],d["stroke"],d["fill"]) for d in x["paths"]],
        "graph_matching":False}
    same = pdf("T3-M-same-label","g2")
    checks["T3-M-same-label"].update({"g2_e2_label":same["words"][5][4],
                                     "g2_e2_direction":"right-to-left" if
                                     same["paths"][10]["items"][0][-1][0]<same["paths"][10]["items"][0][1][0] else "left-to-right"})
    unused = []
    for i in (1,2):
        file = f"g{i}.svg"
        unused.append(digest(D/"controls/T3-M-unused"/file)==digest(D/"matrix/T3-M-1"/file))
    checks["T3-M-unused"]["svg_byte_equal_to_main"]=unused
    for route in "KMP":
        p = D/"controls"/f"T0-{route}-no-figure"
        b = read(p/"browser.json")
        checks[f"T0-{route}-no-figure"]={"images":len(b["images"]),"order":b["order"],
                                       "selectable_sentences":sum(v["found"] for v in b["find"].values())}
    b = read(D/"controls/T0-P-external/moved.json")
    checks["T0-P-external"]={"moved_images":b["images"],"requests":b["requests"],"responses":b["responses"]}
    return checks


def main():
    ledger=[json.loads(s) for s in (ROOT/"runs.jsonl").read_text().splitlines()]
    main_rows=[r for r in ledger if r["kind"]=="matrix"]
    assert sorted(r["id"] for r in main_rows)==sorted(s["id"] for s in PLAN["main"])
    controls=[r for r in ledger if r["kind"]=="controls"]
    assert sorted(r["id"] for r in controls)==sorted(s["id"] for s in PLAN["controls"])
    files=0
    for run in ledger:
        slot=ROOT/run["path"]
        for name,pinned in run["files"].items():
            assert digest(slot/name)==pinned,(run["id"],name)
            files+=1
    findings={r["id"]:summarize(r) for r in main_rows}
    out={"visual_mask_tolerance":{"position_pt":TOLERANCE_PT,"pixel_neighborhood":2,
                                  "minimum_directional_ink_coverage":MASK_THRESHOLD,"ink_luma_less_than":236,
                                  "dominant_channel_over_next_by":17},
         "artifact_hash_checks":files, "matrix":findings,"pairs":repeat_pairs(main_rows,findings),
         "control_measurements":check_controls()}
    write(D/"verification.json",out)
    print(json.dumps({"file_hashes":files,"matrix":dict(Counter(x["result"] for x in findings.values())),
                      "figure_masks":{key:val["geometry_browser_matches"] for key,val in findings.items() if "figures" in val},
                      "pairs":out["pairs"]},ensure_ascii=False))


if __name__=="__main__":
    main()
