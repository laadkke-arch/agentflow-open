#!/usr/bin/env python3
"""AF-RES-103, independent reference, K/M/P matrix and context controls."""
import argparse
from base64 import b64encode
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
from tempfile import TemporaryDirectory

import fitz

from browser_probe import Browser, inspect_svg

ROOT = Path(__file__).resolve().parent
D = ROOT / "evidence"
INPUTS = json.loads((ROOT / "inputs.json").read_text())
DEFINITIONS = json.loads((D / "definitions.json").read_text())
PLAN = json.loads((D / "plan.json").read_text())
PICTURE = re.compile(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", re.S)
ANSWER_NAME = "aff2748b-266e-48f5-b2f7-7547936bb6aa"
PDFFLAGS = ["-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", "-recorder"]
READER = ["--from=latex+raw_tex"]
WRITER = ["--standalone", "-N", "--to=html5", "--embed-resources"]
M_HEADER = r"""\documentclass{standalone}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{automata, positioning, arrows}
"""
M_CONTENT = "\\begin{document}\n\\nopagecolor\n"
COLORS = re.compile(r"\\definecolor\{[A-Za-z][A-Za-z0-9]*\}\{(RGB|rgb)\}\{([0-9., ]+)\}")
STYLE = re.compile(r"\\tikzset\{([A-Za-z0-9 .,!={}\-<>$'/]+)\}")
MACRO = re.compile(r"\\newcommand\{\\[A-Za-z]+\}\{[A-Za-z0-9 .,!+\-]*\}")
DYNAMIC = re.compile(r"\\(?:[egx]?def|foreach|csname|let|if[a-z]*)\b|(?<!\\)#[1-9]")


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return {"sha256": sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size}


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def get_ast_blocks(obj):
    if isinstance(obj, dict):
        if obj.get("t") in ("RawBlock", "RawInline", "CodeBlock"):
            yield obj
        for value in obj.values():
            yield from get_ast_blocks(value)
    if isinstance(obj, list):
        for value in obj:
            yield from get_ast_blocks(value)


def pdf_page_data(file, screenshots=False):
    """Store geometry, paint, fonts and both content-stream and spatial order."""
    pages = []
    with fitz.open(file) as pdf:
        for i, page in enumerate(pdf, 1):
            paths = page.get_drawings()
            pages.append({
                "page": i, "size_pt": [page.rect.width,page.rect.height],
                "text_stream": page.get_text(), "text_spatial": page.get_text(sort=True),
                "words": page.get_text("words"),
                "fonts": [list(x[1:]) for x in page.get_fonts()],
                "paths": [
                    {"seq": p["seqno"], "type":p["type"], "bbox_pt":list(p["rect"]),
                     "stroke":p["color"], "fill":p["fill"], "width":p["width"],
                     "items":[[item[0],*[list(x) if isinstance(x,(fitz.Point,fitz.Rect)) else x
                                         for x in item[1:]]] for item in p["items"]]}
                    for p in paths
                ],
            })
            if screenshots:
                page.get_pixmap(matrix=fitz.Matrix(4/3,4/3), alpha=False).save(file.parent/f"pdf-page-{i:02d}.png")
    return pages


class Tools:
    def __init__(self, path):
        self.root = path
        self.pandoc = path / "pandoc-3.6/bin/pandoc"
        self.pdf2svg = path / "debian/usr/bin/pdf2svg"
        self.mutool = path / "debian/usr/bin/mutool"
        self.pdflatex = Path(shutil.which("pdflatex") or "/usr/bin/pdflatex")
        self.chromium = shutil.which("chromium")
        for app, expected in (
            (self.pandoc, "7f1ac56064cdc02cdf8bd913f9ea45ba07fbb74419e755328c4571e4470769b2"),
            (self.pdf2svg, "c29b1ff1ac46d9341605c97e4dbd1c9feeb47ad139abe472322b81d60b540d51"),
            (self.mutool, "b9588916750d90219b1511cf329776439c68e9a1ae1e6f92dc6532e21dd96df7"),
        ):
            if digest(app)["sha256"] != expected:
                raise ValueError(f"Tool fingerprint differs from the selected executable: {app}")
        if not self.chromium:
            raise ValueError("chromium is missing")

    def environment(self):
        env = os.environ.copy()
        lib = self.root / "debian/usr/lib/x86_64-linux-gnu"
        env["LD_LIBRARY_PATH"] = os.pathsep.join(filter(None,(str(lib),env.get("LD_LIBRARY_PATH"))))
        env.update({"LC_ALL": "C.UTF-8", "TZ": "UTC"})
        return env

    def report(self, previous):
        def command(*argv):
            p = subprocess.run(argv, env=self.environment(), text=True, capture_output=True, check=False)
            return {"argv":list(map(str,argv)),"exit":p.returncode,"stdout":p.stdout,"stderr":p.stderr}
        def fingerprint(arg, counterpart):
            filename = Path(arg)
            spec = {"path":str(filename),"resolved":str(filename.resolve()),**digest(filename)}
            old = counterpart.get("sha256")
            spec.update({"af099_sha256":old,"af099_match":spec["sha256"]==old if old else None})
            return spec

        binaries = {}
        for name, file, args in (
            ("pandoc", self.pandoc, ["--version"]), ("pdflatex",self.pdflatex,["--version"]),
            ("pdf2svg",self.pdf2svg,[]), ("mutool",self.mutool,["-v"]),
            ("chromium",self.chromium,["--version"]),("dot",shutil.which("dot"),["-V"]),
        ):
            binaries[name] = {**fingerprint(file,previous.get("binaries",{}).get(name,{})),
                              "probe":command(file,*args)}
        binaries["pdf2svg"]["version_via_package"] = "0.2.4-1"
        binaries["chromium"]["browser_binary"] = fingerprint("/usr/lib/chromium/chromium",{})
        tex_files = {}
        filenames = (
            "pdflatex.fmt", "article.cls", "report.cls", "standalone.cls","xcolor.sty","tikz.sty",
            "tikzlibraryautomata.code.tex","tikzlibrarypositioning.code.tex","tikzlibraryarrows.code.tex",
            "pgf.revision.tex","pgfplots.sty","pgfplots.revision.tex",
            "cmr10.pfb","cmmi10.pfb","cmr7.pfb","cmbx10.pfb","cmr12.pfb","cmmi7.pfb",
        )
        for filename in filenames:
            flags = ["-engine=pdftex","-format=fmt"] if filename.endswith(".fmt") else []
            lookup = command("kpsewhich",*flags,filename)
            path = lookup["stdout"].strip()
            tex_files[filename] = {"lookup":lookup}
            if path:
                tex_files[filename].update(fingerprint(path,previous.get("tex_files",{}).get(filename,{})))
        packages = command("dpkg-query","-W","texlive-base","texlive-binaries","texlive-latex-base",
                           "texlive-latex-extra","texlive-latex-recommended","texlive-pictures",
                           "libpoppler-glib8t64","libcairo2","graphviz","chromium")
        apt = []
        for deb in sorted((self.root/"debs").glob("*.deb")):
            apt.append({"archive":deb.name,**digest(deb),"control":command("dpkg-deb","-f",deb,"Package","Version","Architecture")})
        return {
            "checked_utc":utc(),"platform":platform.platform(),"python":platform.python_version(),
            "os_release":platform.freedesktop_os_release(),
            "python_packages":{name:importlib.metadata.version(name) for name in ("PyMuPDF","Pillow","playwright")},
            "binaries":binaries, "tex_files":tex_files, "packages":packages,
            "af099_packages":previous.get("installed_package_versions"),"apt_debs":apt,
            "fontconfig":[command("fc-match","-f","%{family}\t%{file}\n",x) for x in ("serif","sans-serif","system-ui")],
            "ldd":[command("ldd",filename) for filename in (self.pdf2svg,self.mutool)],
            "execution_notes":{"K":"pdflatex arguments from sealed Lua; restricted write18 as in 099, tmp per slot",
                               "M_P_reference":"pdflatex -no-shell-escape -recorder; system format",
                               "offline":"fresh Chromium contexts, offline, local disk byte route if file URLs blocked"},
        }


class Slot:
    def __init__(self, tools, output, spec):
        self.tools = tools
        self.spec = spec
        self.root = output / spec["id"]
        self.root.mkdir()
        self.env = tools.environment()
        self.started = utc()
        self.processes = []
        self.phase = "created"
        self.first_failure = None
        self.matches = None
        self.wrapper_calls = []
        self.output_name = None
        self.page_count = None
        tmp = self.root / "tmp"
        tmp.mkdir()
        self.env.update({"TMPDIR":str(tmp), "XDG_CACHE_HOME":str(tmp/"cache"), "TEXMFVAR":str(tmp/"texmf-var"),
                         "MKTEXFMT":"0"})
        self.tmp = tmp

    def run(self, name, argv, env=None):
        argv = list(map(str,argv))
        started = utc()
        try:
            p = subprocess.run(argv, cwd=self.root, env=env or self.env, capture_output=True, timeout=120)
            code, stdout, stderr = p.returncode, p.stdout, p.stderr
        except (OSError,subprocess.TimeoutExpired) as exc:
            code, stdout, stderr = 125, b"", str(exc).encode()
        for ext, data in (("stdout",stdout),("stderr",stderr)):
            (self.root / f"{name}.{ext}").write_bytes(data)
        self.processes.append({
            "step":name,"argv":argv,"cwd":str(self.root),"started_utc":started,"ended_utc":utc(),
            "exit":code,"stdout":f"{name}.stdout","stderr":f"{name}.stderr",
        })
        return code

    def set_input(self, text):
        (self.root/"input.tex").write_text(text, encoding="utf-8")

    def read_ast(self):
        cmd = [self.tools.pandoc,*READER,"--to=json","input.tex","--output=reader.json"]
        if self.run("reader",cmd):
            return None
        ast = json.loads((self.root/"reader.json").read_text())
        raw = list(get_ast_blocks(ast["blocks"]))
        self.matches = {kind:sum(node["t"]==kind for node in raw)
                        for kind in ("RawBlock","RawInline","CodeBlock")}
        pictures = [node for node in raw if node["t"]=="RawBlock" and node["c"][0] in ("latex","tex")
                    and PICTURE.search(node["c"][1])]
        self.matches["picture_matching_raw_blocks"] = len(pictures)
        self.matches["all_literal_tikz_starts_in_raw"] = sum(
            node["c"][1].count(r"\begin{tikzpicture}") for node in raw if node["t"] in ("RawBlock","RawInline")
        )
        return ast, pictures

    def k(self):
        frozen = D/"inputs/p4-raw-tikz.lua"
        if digest(frozen)["sha256"] != INPUTS["lua"]["sha256"]:
            raise ValueError("Frozen Lua hash changed")
        env = self.env.copy()
        env["AF103_CHILD_DIR"] = str(self.root/"children")
        env["AF103_REAL_PDFLATEX"] = str(self.tools.pdflatex)
        env["AF103_REAL_PDF2SVG"] = str(self.tools.pdf2svg)
        (self.root/"children").mkdir()
        with TemporaryDirectory(prefix="af103-shim-") as shims:
            for name in ("pdflatex","pdf2svg"):
                (Path(shims)/name).symlink_to(ROOT/"capture-child.py")
            env["PATH"] = shims + os.pathsep + env["PATH"]
            code = self.run("pandoc-k",[
                self.tools.pandoc,*READER,*WRITER,"--lua-filter="+str(frozen),"input.tex","--output=output.html"
            ],env)
        self.wrapper_calls = [json.loads(p.read_text()) | {"receipt":str(p.relative_to(self.root))}
                              for p in sorted((self.root/"children").glob("*/call.json"))]
        if code:
            failed = next((c for c in self.wrapper_calls if c["exit"]),None)
            self.first_failure = {"step":failed["tool"] if failed else "pandoc-k",
                                  "exit":failed["exit"] if failed else code}
        else:
            self.output_name = "output.html"

    def m(self, text, selection, spans, ast):
        dynamic = [{"line":i,"tokens":DYNAMIC.findall(line.split("%",1)[0])}
                   for i,line in enumerate(text.splitlines(),1) if DYNAMIC.search(line.split("%",1)[0])]
        if dynamic:
            reasons = DEFINITIONS["t2_blocker"] if self.spec["input"] == "T2" else {
                "phase":"M.admission","reason":"source has a parameterized, generated or conditional expression",
            }
            write(self.root/"admission.json",{**reasons,"detected_tokens":dynamic})
            self.first_failure = {"step":reasons["phase"],"exit":None,"reason":reasons["reason"]}
            return
        if ast is None:
            self.first_failure = {"step":"reader","exit":self.processes[-1]["exit"]}
            return
        document, pictures = ast
        lines = text.splitlines()
        declarations = {}
        write(self.root/"selected-lines.json",{
            "authority":"manual declaration list",
            "source_rows":selection,"picture_spans":spans,
            "active_group_spans":DEFINITIONS["scope_spans"] if self.spec["input"]=="T4" else {},
            "actual_declarations":{key:[{"line":i,"raw":lines[i-1]} for i in numbers]
                                   for key,numbers in selection.items()},
        })
        expected = ["\n".join(lines[a-1:b]) for a,b in spans.values()]
        received = [PICTURE.search(node["c"][1]).group() for node in pictures]
        if expected != received or list(spans) != list(selection):
            self.first_failure = {"step":"M.picture-mapping","exit":None,"reason":"source and AST span mismatch"}
            return
        for gid, raw in zip(spans,received):
            preamble, body = [], []
            for number in selection[gid]:
                line = lines[number-1].strip()
                if not supported(line):
                    self.first_failure = {"step":"M.declaration","exit":None,"source_line":number}
                    return
                phase = preamble if number <= lines.index(r"\begin{document}") else body
                phase.append(line)
            declarations[gid] = {
                "preamble_cmds":preamble,"body_cmds":body,
                "tex":M_HEADER+block(preamble)+M_CONTENT+block(body)+raw+"\n\\end{document}\n",
            }
        for gid, node in zip(spans,pictures):
            source = self.root/(gid+".tex")
            source.write_text(declarations[gid]["tex"])
            if (rc := self.run(gid+"-pdflatex",[self.tools.pdflatex,*PDFFLAGS,source.name])):
                self.first_failure = {"step":gid+"-pdflatex","exit":rc}
                return
            if (rc := self.run(gid+"-pdf2svg",[self.tools.pdf2svg,gid+".pdf",gid+".svg"])):
                self.first_failure = {"step":gid+"-pdf2svg","exit":rc}
                return
            node["t"] = "Para"
            node["c"] = [{"t":"Image","c":[[gid,[],[]],[],[gid+".svg",""]]}]
        write(self.root/"writer-input.json",document)
        if (rc := self.run("pandoc-m-writer",[self.tools.pandoc,"--from=json",*WRITER,"writer-input.json","--output=output.html"])):
            self.first_failure = {"step":"pandoc-m-writer","exit":rc}
        else:
            self.output_name = "output.html"

    def p(self, external=False):
        if (rc := self.run("pdflatex-p",[self.tools.pdflatex,*PDFFLAGS,"-jobname="+ANSWER_NAME,"input.tex"])):
            self.first_failure = {"step":"pdflatex-p","exit":rc}
            return
        if (rc := self.run("mutool",[self.tools.mutool,"draw","-oout.svg",ANSWER_NAME+".pdf"])):
            self.first_failure = {"step":"mutool","exit":rc}
            return
        svgs = sorted(self.root.glob("out*.svg"),key=lambda p:int(p.stem.removeprefix("out") or 1))
        with fitz.open(self.root/(ANSWER_NAME+".pdf")) as doc:
            self.page_count = len(doc)
        if self.page_count != len(svgs):
            self.first_failure = {"step":"P.page-count","exit":None,"pages":self.page_count,"svgs":len(svgs)}
            return
        make_preview(self.root/"output.html", svgs, "page", external)
        self.output_name = "output.html"

    def inspect(self, browser, queries=(), try_file=False):
        reports = {}
        for svg in sorted(self.root.glob("*.svg")):
            reports[svg.name] = {**digest(svg), **inspect_svg(svg)}
        write(self.root/"svg.json",reports)
        for pdf in sorted(self.root.glob("*.pdf")):
            write(pdf.with_suffix(".observed.json"), pdf_page_data(pdf, self.spec["route"]=="reference"))
        for child in sorted((self.root/"children").glob("*/*.pdf")):
            write(child.with_suffix(".observed.json"), pdf_page_data(child))
        if self.output_name:
            file = self.root/self.output_name
            write(self.root/"browser.json",browser.probe(file,self.root,"browser",queries,try_file=try_file))
            moved = self.tmp/"moved-only-html"
            moved.mkdir()
            moved_file = moved/self.output_name
            shutil.copyfile(file,moved_file)
            write(self.root/"moved.json",browser.probe(moved_file,self.root,"moved",queries,per_image=False))
        elif reports:
            make_preview(self.root/"partial.html",[self.root/x for x in reports],"fragment")
            write(self.root/"partial-browser.json",browser.probe(self.root/"partial.html",self.root,"partial",queries))

    def finish(self):
        shutil.rmtree(self.tmp)
        files = {str(path.relative_to(self.root)):digest(path) for path in sorted(self.root.rglob("*"))
                 if path.is_file()}
        rel = str(self.root.relative_to(ROOT)) if self.root.is_relative_to(ROOT) else str(self.root)
        executed_tools = sorted({c["tool"] for c in self.wrapper_calls}
                                | {Path(p["argv"][0]).name for p in self.processes})
        receipt = {
            **self.spec, "started_utc":self.started,"ended_utc":utc(),"path":rel,
            "execution":"attempted","first_failure":self.first_failure,
            "processes":self.processes,"child_processes":self.wrapper_calls,
            "actual_tools":executed_tools, "raw_ast":self.matches,
            "matched_filter_compiles":sum(c["tool"]=="pdflatex" for c in self.wrapper_calls),
            "html":self.output_name,"page_count":self.page_count,"files":files,
            "source_sha256":files["input.tex"]["sha256"],"environment":"environment.json",
        }
        write(self.root/"receipt.json",receipt)
        return receipt


def block(lines):
    return "".join(line + "\n" for line in lines)


def supported(line):
    color = COLORS.fullmatch(line)
    if color:
        bits = [x.strip() for x in color[2].split(",")]
        regex, limit = (r"[0-9]{1,3}",255) if color[1]=="RGB" else (r"(?:0|1)?(?:\.[0-9]+)?",1)
        return len(bits)==3 and all(x and re.fullmatch(regex,x) and 0<=float(x)<=limit for x in bits)
    if STYLE.fullmatch(line):
        level = 0
        for char in line:
            level += (char=="{") - (char=="}")
            if level < 0:
                return False
        return level==0 and all(x not in line for x in ("/.code","/.add","/.append","/.expanded","/.evaluated"))
    return MACRO.fullmatch(line) is not None


def make_preview(file, svgs, role, external=False):
    items = []
    for i, svg in enumerate(svgs,1):
        src = svg.name if external else "data:image/svg+xml;base64,"+b64encode(svg.read_bytes()).decode()
        items.append(f'<img alt="{role.capitalize()} {i}" src="{src}">')
    file.write_text(
        '<!doctype html>\n<html lang="en"><meta charset="utf-8">\n'
        '<title>AF-RES-103 visual comparison</title>\n'
        '<style>img{display:block;max-width:100%;height:auto}</style>\n<body>\n'
        + "\n".join(items) + "\n</body></html>\n", encoding="utf-8"
    )


def perturb(spec, text, declarations, spans):
    key = spec["id"]
    if key in ("T1-M-no-color","T1-M-no-tikzset"):
        declarations["g1"].remove(4 if key.endswith("color") else 6)
    elif key in ("T3-M-no-new-style","T3-M-no-red"):
        declarations["g2"].remove(28 if key.endswith("style") else 5)
    elif key in ("T3-M-reverse-styles","T4-M-reverse-styles"):
        gid = "g2" if spec["input"]=="T3" else "g1"
        declarations[gid][-2:] = reversed(declarations[gid][-2:])
    elif key == "T4-M-no-inner":
        declarations["g1"].remove(12)
    elif key == "T4-M-leak-inner":
        declarations["g2"] = [4,5,7,8,12]
    elif key == "T3-M-unused":
        lines = text.splitlines()
        lines.insert(5,r"\definecolor{AFUnused}{RGB}{115,40,85}")
        text = block(lines)
        declarations = {gid:sorted([n+(n>=6) for n in rs]+[6]) for gid,rs in declarations.items()}
        spans = {gid:[start+1,end+1] for gid,(start,end) in spans.items()}
    elif key == "T3-M-same-label":
        text = text.replace("AFTrack] node{r}", "AFTrack] node{b}")
    elif key.endswith("-no-figure"):
        text = PICTURE.sub("",text)
        declarations, spans = {}, {}
    return text, declarations, spans


def run_slot(tools, browser, output, spec):
    case = spec["input"]
    source = ROOT/INPUTS["inputs"][case]["path"]
    if digest(source)["sha256"] != INPUTS["inputs"][case]["sha256"]:
        raise ValueError(f"Source changed: {source}")
    text = source.read_text()
    decl = deepcopy(DEFINITIONS["rows"][case])
    spans = deepcopy(DEFINITIONS["source_spans"][case])
    text, decl, spans = perturb(spec,text,decl,spans)
    slot = Slot(tools,output,spec)
    slot.set_input(text)
    route = spec["route"]
    queries = INPUTS["inputs"][case]["body_sentences"]
    if case=="T2":
        queries = INPUTS["inputs"][case]["t2_heading_groups"] + [
            "Special case view=0,0","Special case view=90,0","Special case view=-90,0",
            "Special case view=0,90","Special case view=0,-90","Special case view=90,90",
        ]
    if route in ("K","M"):
        ast = slot.read_ast()
        if route == "K":
            slot.k()
        else:
            slot.m(text,decl,spans,ast)
    elif route == "P":
        slot.p(external=spec["id"]=="T0-P-external")
    elif (rc := slot.run("reference",[tools.pdflatex,*PDFFLAGS,"input.tex"])):
        slot.first_failure = {"step":"reference","exit":rc}
    slot.inspect(browser,queries,try_file=spec["id"]=="CAL-T0-K")
    return slot.finish()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=["environment","reference","calibration","matrix","controls"])
    parser.add_argument("--tools",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--af099-environment",type=Path)
    args = parser.parse_args()
    tools = Tools(args.tools.resolve())
    output = args.output.resolve()
    if args.action == "environment":
        previous = json.loads(args.af099_environment.read_text()) if args.af099_environment else {}
        write(output,tools.report(previous))
        return
    output.mkdir(parents=True,exist_ok=False)
    specs = {
        "reference":[{"id":x,"input":x,"route":"reference"} for x in INPUTS["inputs"]],
        "calibration":[{"id":f"CAL-{case}-{route}","input":case,"route":route}
                       for case,route in [("T0","K"),("T1","K"),("T4","M"),("T0","P")]],
        "matrix":PLAN["main"],"controls":PLAN["controls"],
    }[args.action]
    with Browser(tools.chromium) as browser, (output/"runs.jsonl").open("w",encoding="utf-8") as ledger:
        for spec in specs:
            entry = run_slot(tools,browser,output,{"kind":args.action,**spec})
            ledger.write(json.dumps(entry,ensure_ascii=False)+"\n")
            ledger.flush()
            print(entry["id"], entry["first_failure"] or entry["html"] or "reference",flush=True)


if __name__ == "__main__":
    main()
