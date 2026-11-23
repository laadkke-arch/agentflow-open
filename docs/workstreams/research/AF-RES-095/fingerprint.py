"""Record versions, runtime template files, and XeTeX/PDF reader fingerprints."""

import argparse
import json
import platform
import re
import subprocess
from pathlib import Path

import PIL
import pymupdf
from pymupdf import _mupdf

from experiment import TEMPLATE_FILES, digest, render_env, save_json, utc

RELEASE = "https://github.com/quarto-dev/quarto-cli/releases/tag/v1.4.553"
CHECKSUMS = "https://github.com/quarto-dev/quarto-cli/releases/download/v1.4.553/quarto-1.4.553-checksums.txt"
EXPECTED_ARCHIVE = "22b7541b1e1be9746657a447383796ba420e6f0cbc5e7b31c8229ddebc258c90"


def identify(path):
    path = Path(path)
    return dict(path=str(path), resolved=str(path.resolve()), bytes=path.stat().st_size, sha256=digest(path))


def capture(args, env):
    proc = subprocess.run([str(part) for part in args], env=env, capture_output=True, text=True, check=False)
    return dict(argv=[str(part) for part in args], exit_code=proc.returncode,
                stdout=proc.stdout.rstrip(), stderr=proc.stderr.rstrip())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quarto", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--checksums", type=Path, required=True)
    parser.add_argument("--calibration", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    env = render_env(args.work.resolve(), args.work.resolve() / "shared")
    quarto = args.quarto.resolve()
    share = quarto.parent.parent / "share"
    tool = quarto.parent / "tools/x86_64"
    calibration = args.calibration.resolve() / "CAL-ORIGINAL"
    package = identify(args.archive.resolve())
    assert package["sha256"] == EXPECTED_ARCHIVE
    published = dict(line.split(maxsplit=1)[::-1] for line in args.checksums.read_text().splitlines())
    assert published[args.archive.name] == EXPECTED_ARCHIVE
    versions = {
        "quarto": capture([quarto, "--version"], env),
        "quarto_pandoc": capture([quarto, "pandoc", "--version"], env),
        "bundled_pandoc": capture([tool / "pandoc", "--version"], env),
        "xelatex": capture(["/usr/bin/xelatex", "--version"], env),
        "xdvipdfmx": capture(["/usr/bin/xdvipdfmx", "--version"], env),
        "tlmgr": capture(["/usr/bin/tlmgr", "--version"], env),
        "poppler": capture(["/usr/bin/pdftoppm", "-v"], env),
        "strace": capture(["/usr/bin/strace", "-V"], env),
    }
    assert all(version["exit_code"] == 0 for version in versions.values())
    assert versions["quarto"]["stdout"] == "1.4.553"
    assert versions["bundled_pandoc"]["stdout"].startswith("pandoc 3.1.11\n")
    queries = {}
    for name in ("booktabs.sty", "longtable.sty", "article.cls", "latex.ltx", "xelatex.fmt"):
        flags = ["--engine=xetex", "--format=fmt"] if name == "xelatex.fmt" else ["--progname=xelatex"]
        queries[name] = capture(["/usr/bin/kpsewhich", *flags, name], env)
    recorder = (calibration / "document.fls").read_text().splitlines()
    loaded_tex = {}
    for name, query in queries.items():
        info = identify(query["stdout"])
        positions = [n for n, line in enumerate(recorder, 1) if line == "INPUT " + info["path"]]
        loaded_tex[name] = dict(locator=query, file=info, recorder_lines=positions,
                                role="compiled kernel source reference" if name == "latex.ltx" else "runtime input")
    assert all(item["recorder_lines"] for name, item in loaded_tex.items() if name != "latex.ltx")
    debug = (calibration / "render.stderr.txt").read_text()
    stage = json.loads((calibration / "pandoc-stage.json").read_text())
    template = {}
    for name in TEMPLATE_FILES:
        staged = stage[name]
        package_name = "template.tex" if name == "template.patched" else name
        shipped = share / "formats/pdf/pandoc" / package_name
        runtime = re.search(r"\[INFO\] Loaded (\S+/" + re.escape(name) + r") from", debug)
        assert runtime, name
        template[name] = dict(
            shipped=identify(shipped), runtime_path=runtime[1],
            staged_sha256=staged["sha256"], staged_bytes=staged["bytes"],
            equal=digest(shipped) == staged["sha256"],
            calibration_evidence="evidence/calibration/CAL-ORIGINAL/pandoc-stage.json",
        )
    packages = capture(["/usr/bin/dpkg-query", "-W", "-f=${Package}\t${Version}\n",
                        "texlive-base", "texlive-binaries", "texlive-latex-base", "texlive-latex-extra",
                        "texlive-latex-recommended", "texlive-xetex", "texlive-fonts-recommended",
                        "poppler-utils", "libpoppler147", "strace"], env)
    poppler_lib_line = next(line for line in capture(
        ["/usr/bin/ldd", "/usr/bin/pdftoppm"], env)["stdout"].splitlines() if "libpoppler.so." in line)
    data = {
        "captured_utc": utc(),
        "os": {"release": Path("/etc/os-release").read_text(), "arch": platform.machine(),
               "kernel": platform.release(), "python": platform.python_version()},
        "distribution": {
            "release_url": RELEASE, "source_commit": "466d959674507930685b2c977e878495932152ba",
            "asset_url": RELEASE.replace("/tag/", "/download/") + "/" + args.archive.name,
            "checksums_url": CHECKSUMS, "checksums_file": identify(args.checksums),
            "published_sha256": published[args.archive.name], "archive": package,
            "bundle_listing": "evidence/calibration/bundle-members.txt",
        },
        "versions": versions,
        "binaries": {name: identify(path) for name, path in {
            "quarto": quarto, "quarto_js": quarto.parent / "quarto.js",
            "bundled_pandoc": tool / "pandoc", "deno": tool / "deno",
            "xelatex": "/usr/bin/xelatex", "xdvipdfmx": "/usr/bin/xdvipdfmx",
            "pdftoppm": "/usr/bin/pdftoppm", "strace": "/usr/bin/strace",
            "libpoppler": poppler_lib_line.split("=>")[1].strip().split()[0],
            "pymupdf_extension": _mupdf.__file__, "pillow_init": PIL.__file__,
        }.items()},
        "quarto_reader_and_filter": {name: identify(share / name) for name in (
            "filters/qmd-reader.lua", "pandoc/datadir/readqmd.lua", "filters/main.lua"
        )},
        "reference_pandoc": {"version": "3.1.11", "source_commit": "c3038dcd54152c4e18e49db31676b79ee7cc29b2",
                             "relation": "092 standalone comparison source, not separately executed in this matrix"},
        "tex_locator_observations": loaded_tex,
        "templates": template,
        "debian_packages": packages,
        "reader": {"pymupdf_binding": pymupdf.__version__, "mupdf": pymupdf.mupdf_version,
                   "pillow": PIL.__version__, "raster_renderer": "/usr/bin/pdftoppm", "dpi": 288},
        "matrix_common_env": {"PATH": env["PATH"], "TZ": env["TZ"], "LC_ALL": env["LC_ALL"],
                              "per_run": "TMPDIR", "shared_writable": "XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, TEXMFVAR, TEXMFCONFIG",
                              "unset": ["QUARTO_PANDOC", "QUARTO_BIN_PATH", "QUARTO_SHARE_PATH", "QUARTO_TINYTEX", "TEXINPUTS"]},
        "auto_install": False,
    }
    save_json(args.output, data)


if __name__ == "__main__":
    main()
