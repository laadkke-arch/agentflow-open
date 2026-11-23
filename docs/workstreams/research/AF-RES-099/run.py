"""AF-RES-099. Run each stage in a new local evidence directory."""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import mimetypes
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
from urllib.parse import unquote, unquote_to_bytes, urlsplit
from xml.etree import ElementTree

HERE = Path(__file__).resolve().parent
INPUTS = json.loads((HERE / "inputs.json").read_text())
TEX = "example.tex"
C_PDF = INPUTS["answer"]["command"][-1]
BODY = ("The following is a TIKZ picture.", "The above is a TIKZ picture.")
VIEWPORT = {"width": 1100, "height": 1450}
MIME_SVG = "image/svg+xml"
SMALL_TEX = r"""\documentclass[border=3pt]{standalone}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{automata, positioning, arrows}
\begin{document}
\begin{tikzpicture}[>=stealth',->,node distance=21mm]
\node[state,initial,accepting,fill=blue!10] (a) {CAL};
\node[state,right=of a] (b) {OK};
\path (a) edge[above] node{yes} (b);
\end{tikzpicture}
\end{document}
"""
SMALL_CODE = r"""\begin{tikzpicture}
\draw[->,blue,very thick] (0,0) -- node[above]{OTHER} (2,0);
\end{tikzpicture}"""


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))


def metadata(path):
    return {"bytes": path.stat().st_size, "sha256": digest(path)}


def find_system(name):
    exe = shutil.which(name)
    if not exe:
        raise FileNotFoundError(name)
    return Path(exe).absolute()


def execute(args, cwd, env, name, log_limit=32000):
    args = [str(arg) for arg in args]
    start = utc()
    result = {"name": name, "argv": args, "cwd": str(cwd), "started_utc": start}
    try:
        proc = subprocess.run(args, cwd=cwd, env=env, capture_output=True, timeout=100)
        stdout, stderr = proc.stdout, proc.stderr
        result["exit_code"] = proc.returncode
    except (OSError, subprocess.TimeoutExpired) as exc:
        stdout, stderr = b"", str(exc).encode()
        result["exit_code"] = None
        result["launch_or_timeout_error"] = type(exc).__name__
    for kind, stream in (("stdout", stdout), ("stderr", stderr)):
        if stream:
            path = cwd / f"{name}.{kind}.txt"
            discarded = len(stream) > log_limit
            if discarded:
                part = log_limit // 2
                path.write_bytes(stream[:part] + b"\n[omitted middle]\n" + stream[-part:])
            else:
                path.write_bytes(stream)
            result[kind] = {
                "path": path.name,
                "original_sha256": hashlib.sha256(stream).hexdigest(),
                "original_bytes": len(stream),
                "excerpt": discarded,
            }
    result["finished_utc"] = utc()
    return result


def trace_child():
    """Transparent PATH interposer to preserve actual temporary compiler outputs."""
    name = Path(sys.argv[2]).name
    args = [json.loads(os.environ["AF099_TOOL_MAP"])[name], *sys.argv[3:]]
    cwd = Path.cwd()
    events = Path(os.environ["AF099_EVENTS"])
    record = {"tool": name, "argv": args, "cwd": str(cwd), "started_utc": utc()}
    result = subprocess.run(args)
    record["exit_code"] = result.returncode
    record["finished_utc"] = utc()
    index = len(list(events.glob("*.json")))
    if name in {"pdflatex", "xelatex"}:
        record["artifacts_copied_before_cleanup"] = {}
        for pattern in ("*.pdf", "*.log"):
            for source in cwd.glob(pattern):
                destination = events / f"{index}-{source.name}"
                shutil.copyfile(source, destination)
                record["artifacts_copied_before_cleanup"][destination.name] = metadata(destination)
        for source in cwd.glob("*.tex"):
            record["compiler_input"] = {"name": source.name, **metadata(source)}
    if name == "pdf2svg" and len(args) >= 3 and Path(args[2]).is_file():
        record["converter_output"] = {"name": Path(args[2]).name, **metadata(Path(args[2]))}
    write_json(events / f"{index:02d}-{name}.json", record)
    return result.returncode if result.returncode >= 0 else 128 - result.returncode


class Study:
    def __init__(self, tools, output):
        self.tools = tools.resolve()
        self.output = output.resolve()
        self.pandoc = self.tools / "pandoc-3.6/bin/pandoc"
        self.diagram = self.tools / "diagram"
        self.diagram_lua = self.diagram / INPUTS["diagram"]["entry_target"]
        self.tex = self.tools / TEX
        self.lua = self.tools / "p4-raw-tikz.lua"
        self.formats = self.tools / "formats/web2c"
        self.debian = self.tools / "debian/usr"
        self.pdflatex = find_system("pdflatex")
        self.xelatex = find_system("xelatex")
        self.chromium = find_system("chromium")
        self.pdf2svg = self.debian / "bin/pdf2svg"
        self.inkscape = find_system("inkscape")
        self.mutool = self.debian / "bin/mutool"
        for path, expected in (
            (self.tex, INPUTS["question"]["tex_sha256"]),
            (self.lua, INPUTS["b"]["lua_sha256"]),
            (self.pandoc, INPUTS["pandoc"]["binary_sha256"]),
        ):
            if digest(path) != expected:
                raise ValueError(f"unexpected input bytes: {path}")
        fixed = INPUTS["diagram"]["commit"]
        head = subprocess.check_output(["git", "-C", self.diagram, "rev-parse", "HEAD"], text=True)
        sealed = subprocess.check_output(
            ["git", "-C", self.diagram, "show", f"{fixed}:{INPUTS['diagram']['entry_target']}"]
        )
        if head.strip() != fixed or sealed != self.diagram_lua.read_bytes():
            raise ValueError("unexpected diagram checkout or filter bytes")
        # A writes in an empty working directory, with the same symlink layout as upstream.
        self.output.mkdir(parents=True, exist_ok=False)
        self.rows = []

    def slot(self, name, formats=True, observe=False):
        cwd = self.output / name
        cwd.mkdir()
        env = os.environ.copy()
        for var, name in (
            ("TMPDIR", "tmp"), ("TEXMFVAR", "texmf-var"), ("TEXMFCONFIG", "texmf-config"),
            ("TEXMFHOME", "texmf-home"), ("XDG_CACHE_HOME", "cache"), ("XDG_DATA_HOME", "data"),
            ("XDG_CONFIG_HOME", "config"),
        ):
            path = cwd / name
            path.mkdir()
            env[var] = str(path)
        library = self.debian / "lib/x86_64-linux-gnu"
        env["LD_LIBRARY_PATH"] = os.pathsep.join(
            value for value in (str(library), env.get("LD_LIBRARY_PATH")) if value
        )
        env["PATH"] = os.pathsep.join((str(self.debian / "bin"), env["PATH"]))
        formats_path = self.formats if formats else cwd / "texmf-var"
        env["TEXFORMATS"] = f"{formats_path}//"
        env["MKTEXFMT"] = "0"
        if observe:
            events = cwd / "events"
            events.mkdir()
            bin_dir = cwd / "trace-bin"
            bin_dir.mkdir()
            tools = (self.pdflatex, self.xelatex, self.pdf2svg, self.inkscape)
            env["AF099_TOOL_MAP"] = json.dumps({tool.name: str(tool) for tool in tools})
            env["AF099_EVENTS"] = str(events)
            for tool in tools:
                # Shell wrapper supplies the invoked name while retaining stdin and stdout.
                path = bin_dir / tool.name
                source = shlex.join([sys.executable, str(Path(__file__).resolve()), "_trace"])
                path.write_text(f'#!/bin/sh\nexec {source} "$0" "$@"\n')
                path.chmod(0o755)
            env["PATH"] = os.pathsep.join((str(bin_dir), env["PATH"]))
        return cwd, env

    def row(self, cwd, kind, steps, input_sha=None, **extra):
        artifacts = {}
        for entry in sorted(cwd.iterdir()):
            if entry.is_file() and entry.suffix not in {".lua", ".tex", ".md", ".yaml", ".aux"}:
                artifacts[entry.name] = metadata(entry)
        media_dir = cwd / "media"
        if media_dir.exists():
            artifacts.update({str(p.relative_to(cwd)): metadata(p)
                              for p in media_dir.rglob("*") if p.is_file()})
        events_dir = cwd / "events"
        if events_dir.exists():
            artifacts.update({str(p.relative_to(cwd)): metadata(p) for p in events_dir.iterdir()})
        record = {
            "id": cwd.name, "kind": kind, "path": cwd.name,
            "input_sha256": input_sha, "processes": steps, "artifacts": artifacts, **extra,
        }
        if events_dir.exists():
            record["child_processes"] = [
                json.loads(p.read_text()) for p in sorted(events_dir.glob("*.json"))
            ]
        self.rows.append(record)

    def frozen(self, cwd, env, name="pandoc"):
        return execute(
            [self.pandoc, "--standalone", "-N", "--from=latex+raw_tex", "--to=html5",
             f"--lua-filter={self.lua}", "--embed-resources", TEX, "--output=example.html"],
            cwd, env, name,
        )

    def build_formats(self):
        cwd, env = self.slot("FORMAT-BUILD")
        env.pop("TEXFORMATS")
        env.pop("MKTEXFMT")
        env["TEXMFVAR"] = str(self.tools / "formats")
        (self.tools / "formats").mkdir(exist_ok=False)
        steps = [
            execute([find_system("fmtutil-user"), "--byfmt", name], cwd, env, name, 10060)
            for name in ("pdflatex", "xelatex")
        ]
        self.row(cwd, "format-preparation", steps)
        return all(s["exit_code"] == 0 for s in steps)

    def calibration(self):
        cwd, env = self.slot("Q2-POS")
        tex = cwd / "calibration.tex"
        tex.write_text(SMALL_TEX)
        steps = [
            execute(["kpsewhich", "-engine=pdftex", "-format=fmt", "pdflatex.fmt"], cwd, env, "found-format"),
            execute(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex.name], cwd, env, "compile"),
            execute(["pdf2svg", "calibration.pdf", "calibration.svg"], cwd, env, "pdf2svg"),
            execute(["mutool", "draw", "-ocalibration-page%d.svg", "calibration.pdf"], cwd, env, "mutool"),
        ]
        html = cwd / "calibration.html"
        html.write_text(wrap_svg("calibration.svg"))
        png = cwd / "calibration-browser.png"
        browser = browser_probe(self.chromium, html, png)
        write_json(cwd / "browser.json", browser)
        write_json(cwd / "svg.json", svg_probe(cwd / "calibration.svg"))
        self.row(cwd, "positive-control", steps, digest(tex))

        cwd, env = self.slot("Q2-NOFMT", formats=False, observe=True)
        shutil.copyfile(self.tex, cwd / TEX)
        steps = [execute(["kpsewhich", "-engine=pdftex", "-format=fmt", "pdflatex.fmt"],
                         cwd, env, "missing-format"), self.frozen(cwd, env)]
        self.row(cwd, "negative-format-control", steps, digest(self.tex))
        self.codeblock_controls()

    def diagram_convert(self, cwd, env, filename, output, lua="diagram.lua", extra=()):
        return execute(
            [self.pandoc, "--standalone", "-N", f"--lua-filter={lua}", "-f", "latex",
             "-t", "html", filename, "-o", output, *extra],
            cwd, env, Path(output).stem,
        )

    def observe_diagram(self, cwd):
        source = self.diagram_lua.read_text()
        needle = "  return function (block)\n"
        hit_log = """    io.stderr:write("AF099 CodeBlock first_class=", block.classes[1] or "-", "\\n")\n"""
        doc_needle = "      local conf = configure(doc.meta, FORMAT)\n"
        doc_log = """      io.stderr:write("AF099 document callback loaded\\n")\n"""
        if source.count(needle) != 1 or source.count(doc_needle) != 1:
            raise ValueError("diagram instrumentation locations changed")
        path = cwd / "observed-diagram.lua"
        path.write_text(source.replace(needle, needle + hit_log).replace(doc_needle, doc_log + doc_needle))
        return path.name

    def codeblock_controls(self):
        cwd, env = self.slot("Q3-OTHER", observe=True)
        path = cwd / "other.md"
        path.write_text("Other before.\n\n```{.tikz filename=other}\n" + SMALL_CODE + "\n```\n\nOther after.\n")
        observed = self.observe_diagram(cwd)
        steps = [
            execute([self.pandoc, "-f", "markdown", "-t", "json", path.name, "-o", "reader.json"],
                    cwd, env, "reader"),
            execute([self.pandoc, "--standalone", "-f", "markdown", "-t", "html", "--embed-resources",
                     f"--lua-filter={self.diagram_lua}", path.name, "-o", "other.html"],
                    cwd, env, "pandoc"),
            execute([self.pandoc, "--standalone", "-f", "markdown", "-t", "html", "--embed-resources",
                     f"--lua-filter={observed}", path.name, "-o", "observed.html"],
                    cwd, env, "observed"),
        ]
        write_json(cwd / "browser.json", browser_probe(self.chromium, cwd / "other.html", cwd / "browser.png"))
        self.row(cwd, "positive-codeblock-and-wrong-picture-control", steps, digest(path),
                 observed_lua_sha256=digest(cwd / observed))

        cwd, env = self.slot("Q3-UPSTREAM", observe=True)
        upstream = self.diagram / "test/input-tikz.md"
        steps = [execute(
            [self.pandoc, "-f", "markdown", "-t", "html", f"--lua-filter={self.diagram_lua}",
             upstream, "-o", "actual.html", "--extract-media=media"], cwd, env, "upstream",
        )]
        write_json(cwd / "browser.json", browser_probe(self.chromium, cwd / "actual.html", cwd / "browser.png"))
        self.row(cwd, "upstream-input-media-extraction", steps, digest(upstream))

    def route_a(self, index):
        cwd, env = self.slot(f"A{index}", observe=True)
        shutil.copyfile(self.tex, cwd / TEX)
        (cwd / "diagram.lua").symlink_to(self.diagram_lua)
        steps = [
            self.diagram_convert(cwd, env, TEX, "example.html"),
            execute([self.pandoc, "-f", "latex", "-t", "json", TEX, "-o", "reader.json"], cwd, env, "reader"),
        ]
        write_json(cwd / "browser.json", browser_probe(self.chromium, cwd / "example.html", cwd / "browser.png"))
        self.row(cwd, "primary", steps, digest(self.tex), route="A", repetition=index)

    def route_b(self, index):
        cwd, env = self.slot(f"B{index}", observe=True)
        shutil.copyfile(self.tex, cwd / TEX)
        steps = [
            self.frozen(cwd, env),
            execute([self.pandoc, "-f", "latex+raw_tex", "-t", "json", TEX, "-o", "reader.json"],
                    cwd, env, "reader"),
        ]
        html = cwd / "example.html"
        if html.exists():
            browser = browser_probe(self.chromium, html, cwd / "browser.png")
            write_json(cwd / "browser.json", browser)
            images = browser.get("images", [])
            img = images[0] if len(images) == 1 else {}
            payload = img.get("source", "")
            if payload.startswith("data:image/svg+xml"):
                decoded = cwd / "decoded.svg"
                decoded.write_bytes(decode_data(payload))
                write_json(cwd / "svg.json", svg_probe(decoded))
        self.row(cwd, "primary", steps, digest(self.tex), route="B", repetition=index)

    def route_c(self, index):
        cwd, env = self.slot(f"C{index}")
        shutil.copyfile(self.tex, cwd / TEX)
        steps = [
            execute(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                     f"-jobname={Path(C_PDF).stem}", TEX], cwd, env, "compile"),
            execute(INPUTS["answer"]["command"], cwd, env, "mutool"),
        ]
        pages = sorted(cwd.glob("out*.svg"))
        if len(pages) == 1:
            svg = pages[0]
            write_json(cwd / "svg.json", svg_probe(svg))
            write_json(cwd / "browser.json", browser_probe(self.chromium, svg, cwd / "browser.png"))
            pdf_browser_reference(self.chromium, cwd, C_PDF)
        self.row(cwd, "primary", steps, digest(self.tex), route="C", repetition=index,
                 svg_pages=[page.name for page in pages])

    def route_c_plus(self, index, embedded=False, missing=False):
        suffix = "EMBED" if embedded else "MISSING" if missing else "EXTERNAL"
        cwd, _ = self.slot(f"CPLUS-{suffix}-{index}")
        pages = sorted((self.output / f"C{index}").glob("out*.svg"))
        if len(pages) != 1:
            self.row(cwd, "researcher-html-wrapper", [], note=f"expected one C SVG, found {len(pages)}")
            return
        svg = pages[0]
        src = f"data:{MIME_SVG};base64," + base64.b64encode(svg.read_bytes()).decode() if embedded else svg.name
        if not (embedded or missing):
            shutil.copyfile(svg, cwd / svg.name)
        html = cwd / "page.html"
        html.write_text(wrap_svg(src))
        write_json(cwd / "browser.json", browser_probe(self.chromium, html, cwd / "browser.png"))
        self.row(cwd, "researcher-html-wrapper", [], digest(svg), source_c=f"C{index}/{svg.name}",
                 resource=suffix)

    def auxiliary(self):
        cwd, env = self.slot("A-OBSERVED", observe=True)
        shutil.copyfile(self.tex, cwd / TEX)
        observed = self.observe_diagram(cwd)
        steps = [
            self.diagram_convert(cwd, env, TEX, "observed.html", observed),
            execute([self.pandoc, "-f", "latex+raw_tex", "-t", "json", TEX, "-o", "raw-reader.json"],
                    cwd, env, "raw-reader"),
            execute([self.pandoc, "-f", "latex", "-t", "json", "--list-extensions=latex"],
                    cwd, env, "latex-extensions"),
            self.diagram_convert(cwd, env, TEX, "raw-with-diagram.html", observed,
                                 ("--from=latex+raw_tex",)),
        ]
        self.row(cwd, "separate-filter-observation", steps, digest(self.tex),
                 observed_lua_sha256=digest(cwd / observed))

        cwd, env = self.slot("B-NOPIC", observe=True)
        text = self.tex.read_text()
        altered, changed = re.subn(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", "", text, flags=re.S)
        if changed != 1:
            raise ValueError("no-picture control needs exactly one picture")
        (cwd / TEX).write_text(altered)
        steps = [self.frozen(cwd, env)]
        write_json(cwd / "browser.json", browser_probe(self.chromium, cwd / "example.html", cwd / "browser.png"))
        self.row(cwd, "no-picture-input-control", steps, digest(cwd / TEX))

        cwd, _ = self.slot("B-ONLY-HTML")
        html = cwd / "example.html"
        shutil.copyfile(self.output / "B1/example.html", html)
        write_json(cwd / "browser.json", browser_probe(self.chromium, html, cwd / "browser.png"))
        self.row(cwd, "moved-html-alone-offline-control", [], digest(html), source="B1/example.html")

        for index in (1, 2):
            self.route_c_plus(index)
            self.route_c_plus(index, embedded=True)
        self.route_c_plus(1, missing=True)

    def preamble_control(self):
        cwd, env = self.slot("B-CUSTOM-PREAMBLE", observe=True)
        original = self.tex.read_text()
        before = r"\begin{document}"
        original = original.replace(before, r"\definecolor{AFControl}{RGB}{0,94,179}" + "\n" + before, 1)
        original = original.replace("fill=gray!10", "fill=AFControl!10", 1)
        # Color must occur inside the transferred block, not only in the document's tikzset.
        original = original.replace(r"\node[state, initial, accepting]",
                                    r"\node[state, initial, accepting, draw=AFControl]", 1)
        path = cwd / TEX
        path.write_text(original)
        steps = [
            execute([self.pdflatex, "-interaction=nonstopmode", "-halt-on-error",
                     "-jobname=original-custom", TEX], cwd, env, "reference-compile"),
            self.frozen(cwd, env),
        ]
        self.row(cwd, "preamble-dependency-counterexample", steps, digest(path),
                 derivation="One preamble definecolor and one node draw option depend on AFControl.")

    def run(self, stage):
        try:
            if stage == "formats":
                return 0 if self.build_formats() else 1
            if stage == "calibrate":
                self.calibration()
            if stage == "counterexample":
                self.preamble_control()
            if stage == "matrix":
                for index in (1, 2):
                    self.route_a(index)
                    self.route_b(index)
                    self.route_c(index)
                self.auxiliary()
            return 0
        finally:
            write_jsonl(self.output / "runs.jsonl", self.rows)


def wrap_svg(source):
    return ('<!doctype html>\n<html lang="en"><meta charset="utf-8">\n'
            '<title>SVG viewer</title>\n'
            f'<body><img src="{source}" alt=""></body></html>\n')


def decode_data(source):
    header, encoded = source.split(",", 1)
    if header.endswith(";base64"):
        return base64.b64decode(encoded, validate=True)
    return unquote_to_bytes(encoded)


def svg_probe(path):
    root = ElementTree.parse(path).getroot()
    counts = {}
    tags = []
    for item in root.iter():
        tag = item.tag.rsplit("}", 1)[-1]
        counts[tag] = counts.get(tag, 0) + 1
        if tag == "text":
            tags.append("".join(item.itertext()))
    links = [
        item.attrib.get("href") or item.attrib.get("{http://www.w3.org/1999/xlink}href")
        for item in root.iter() if item.tag.rsplit("}", 1)[-1] == "use"
    ]
    ids = {f"#{node.attrib['id']}" for node in root.iter() if "id" in node.attrib}
    return {
        "file": metadata(path), "dimensions": dict(root.attrib), "element_counts": counts,
        "text_elements": tags, "use_targets": links,
        "all_use_targets_local": all(x and x.startswith("#") for x in links),
        "data_text_count": sum("data-text" in x.attrib for x in root.iter()),
        "local_use_targets_resolved": all(link in ids for link in links),
    }


def browser_probe(binary, path, screenshot):
    from playwright.sync_api import Error

    if not path.is_file():
        return {"opened": False, "error": "output file absent", "viewport": VIEWPORT}
    failures = []
    outbound = []
    try:
        return open_in_browser(binary, path, screenshot, failures, outbound)
    except Error as exc:
        return {"opened": False, "error": str(exc), "viewport": VIEWPORT}


def open_in_browser(binary, path, screenshot, failures, outbound):
    from playwright.sync_api import sync_playwright

    directory = path.resolve().parent
    origin = "http://127.0.0.1:8765"
    served = []

    def handle(route):
        parsed = urlsplit(route.request.url)
        if f"{parsed.scheme}://{parsed.netloc}" != origin:
            route.abort()
            return
        requested = (directory / unquote(parsed.path).lstrip("/")).resolve()
        if not requested.is_relative_to(directory) or not requested.is_file():
            served.append({"path": parsed.path, "status": 404})
            route.fulfill(status=404, body="File absent in this evidence directory.")
            return
        served.append({"path": parsed.path, "status": 200, **metadata(requested)})
        content_type = mimetypes.guess_type(requested.name)[0] or "application/octet-stream"
        route.fulfill(status=200, path=requested, content_type=content_type)

    with sync_playwright() as play:
        browser = play.chromium.launch(executable_path=binary, args=["--disable-dev-shm-usage"])
        context = browser.new_context(viewport=VIEWPORT, offline=True, device_scale_factor=1)
        context.route("**/*", handle)
        page = context.new_page()
        page.on("requestfailed", lambda req: failures.append({"url": req.url, "error": req.failure}))
        page.on("request", lambda req: outbound.append(req.url)
                if req.url.startswith(("http://", "https://")) else None)
        page.goto(f"{origin}/{path.name}", wait_until="load", timeout=12000)
        result = page.evaluate(
            """() => ({
                root: document.documentElement.localName,
                navigatorOnline: navigator.onLine,
                bodyText: document.body?.innerText ?? '',
                paragraphs: Array.from(document.querySelectorAll('p'), p => p.innerText),
                sequence: Array.from(document.querySelectorAll('p,img')).map(
                    el => el.localName === 'img' ? '<img>' : el.innerText),
                svgText: Array.from(document.querySelectorAll('svg text'), e => e.textContent),
                svgLinks: Array.from(document.querySelectorAll('svg a'), el =>
                    el.getAttribute('href') || el.getAttributeNS('http://www.w3.org/1999/xlink', 'href')),
                images: Array.from(document.images ?? []).map(el => ({
                    source: el.getAttribute('src'), alt: el.getAttribute('alt'),
                    width: el.naturalWidth, height: el.naturalHeight, complete: el.complete,
                    rect: el.getBoundingClientRect().toJSON()
                }))
            })"""
        )
        page.screenshot(path=screenshot)
        result.update(opened=True, viewport=VIEWPORT, offline=True, browser_version=browser.version,
                      failed_requests=failures, outbound_requests=outbound,
                      served=served, transport="Playwright fulfills local files at loopback origin; no HTTP listener")
    result["before_after_searchable"] = [phrase in result["bodyText"] for phrase in BODY]
    for img in result["images"]:
        source = img["source"] or ""
        if source.startswith("data:"):
            img["decoded_sha256"] = hashlib.sha256(decode_data(source)).hexdigest()
    return result


def pdf_browser_reference(chromium, cwd, filename):
    import fitz

    with fitz.open(cwd / filename) as pdf:
        page = pdf[0]
        page.get_pixmap(matrix=fitz.Matrix(4 / 3, 4 / 3), alpha=False).save(cwd / "pdf-page.png")
        facts = {
            "pages": len(pdf), "page_pt": [page.rect.width, page.rect.height],
            "text": page.get_text(), "words": page.get_text("words"),
            "drawings": page.get_drawings(),
        }
        (cwd / "pdf.json").write_text(json.dumps(facts, default=list, indent=2) + "\n")
    (cwd / "pdf-view.html").write_text(wrap_svg("pdf-page.png"))
    write_json(cwd / "pdf-browser.json",
               browser_probe(chromium, cwd / "pdf-view.html", cwd / "pdf-browser.png"))


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "_trace":
        sys.exit(trace_child())
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["formats", "calibrate", "matrix", "counterexample"])
    parser.add_argument("--tools", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    sys.exit(Study(args.tools, args.output).run(args.stage))


if __name__ == "__main__":
    main()
