#!/usr/bin/env python3
"""Run each sealed input twice against SQLite and Chromium and save receipts."""
from argparse import ArgumentParser
from datetime import datetime, timezone
from functools import partial
from hashlib import sha3_256
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
import json
from pathlib import Path
import re
import shutil
import subprocess
from threading import Thread
from time import perf_counter
from urllib.parse import urljoin

from select_passages import ROOT, digest, write_jsonl

PIN = "f1edffe3511493e684402fdfed42433e79374d55"
WPT = "https://raw.githubusercontent.com/web-platform-tests/wpt/" + PIN + "/"
RESOURCES = ("resources/testharness.js", "resources/testharnessreport.js",
             "resources/check-layout-th.js", "css/css-flexbox/support/flexbox.css",
             "fonts/ahem.css", "fonts/Ahem.ttf")
ORACLE = {"S1":1,"S2":1,"S3":2,"S4":2}
TIMEOUT = 12


def utc():
    return datetime.now(timezone.utc).isoformat()


def checked(path, sha):
    data = path.read_bytes()
    if digest(data) != sha:
        raise ValueError(f"Incorrect sealed SHA-256: {path}")
    return data


def preceding_select(data):
    text = data.decode().rstrip().rstrip(";")
    offset = text.rfind(";") + 1
    return text[:offset], text[offset:]


def json_result_arrays(output):
    values = []
    tail = output.lstrip()
    decoder = json.JSONDecoder()
    while tail:
        rows, end = decoder.raw_decode(tail)
        values.append([list(row.values()) for row in rows])
        tail = tail[end:].lstrip()
    return values


def run_sql(shell, case, item, repetition):
    data = checked(ROOT / item["path"], item["sha256"])
    original_setup, query = preceding_select(data)
    columns = [f"v{number}" for number in range(ORACLE[case["case"]])]
    labels = ",".join(columns)
    storage = ",".join(f"typeof({c}) as {c}_type" for c in columns)
    types_stmt = f"WITH q({labels}) AS MATERIALIZED ({query}) SELECT {labels},{storage} FROM q;"
    stdin = data.decode() + types_stmt + "\n"
    command = [str(shell), "-batch", "-bail", "-json", ":memory:"]
    info = {
        "case":case["case"],"input":item["form"],"repeat":repetition,
        "engine":"sqlite3 3.51.1", "started_utc":utc(), "argv":command,
        "input_sha256":item["sha256"],"stdin_sha256":digest(stdin),
        "typeof_statement":types_stmt, "timeout_seconds":TIMEOUT, "setup_codepoints":len(original_setup),
    }
    started = perf_counter()
    try:
        done = subprocess.run(command, input=stdin, text=True, capture_output=True, timeout=TIMEOUT)
        info.update(exit=done.returncode, timed_out=False, stdout=done.stdout, stderr=done.stderr)
        if done.returncode == 0:
            rows, typed = json_result_arrays(done.stdout)
            cuts = len(columns)
            info.update(rows=rows,types=[t[cuts:] for t in typed],
                        values_in_type_probe=[t[:cuts] for t in typed])
    except subprocess.TimeoutExpired:
        info.update(exit=None,timed_out=True,stderr="sqlite3 timeout")
    return dict(info,duration_seconds=perf_counter()-started,ended_utc=utc())


class QuietHTTP(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


def ensure_path(cache, key):
    path = cache / key
    if not path.exists():
        path.parent.mkdir(parents=True,exist_ok=True)
        subprocess.run(["curl","-fLsS","--max-time","14",WPT+key,"-o",str(path)],check=True)
    return path


def render_files(cache, case):
    path = case["raw_path"]
    raw = checked(ensure_path(cache,path),case["raw_sha256"]).decode()
    left, right = case["edit"]
    starts = [m.start() for m in re.finditer(re.escape(left),raw)]
    at = starts[case["mutable_occurrence"]-1]
    new = raw[:at]+right+raw[at+len(left):]
    refs = re.findall(r'<link\s+rel=["\']match["\']\s+href=["\']([^"\']+)',raw,re.I)
    for index, href in enumerate(refs):
        resolved=urljoin(path,href)
        ref=ensure_path(cache,resolved)
        checked(ref,case["reference_hashes"][index]["sha256"])
    return raw, new, refs


def capture(page, path, store):
    image = page.screenshot(timeout=TIMEOUT*1000)
    if store:
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(image)
    return image


def native_assertions(probe, is_original):
    assertions = {}
    if probe is not None:
        expected = probe["data"]
        if "expected-height" in expected:
            v=float(expected["expected-height"])
            assertions["upstream_height"] = {"expected":v,"actual":probe["target"]["height"],
                "pass":v==probe["target"]["height"]}
        if "offset-y" in expected:
            v=float(expected["offset-y"])
            assertions["upstream_offset_y"]={"expected":v,"actual":probe["offsetTop"],
                "pass":v==probe["offsetTop"],"container_client_top":probe["parentClientTop"]}
    assertions["upstream_scope"]="original" if is_original else "original assertions on mutated input; diagnostic"
    return assertions


MEASURE = r"""([parentSpec, childSpec, axis]) => {
  const parent = document.querySelectorAll(parentSpec[0])[parentSpec[1]];
  const child = parent.querySelectorAll(childSpec[0])[childSpec[1]];
  const rect = e => e.getBoundingClientRect().toJSON();
  const p = rect(parent), t = rect(child);
  const cs = getComputedStyle(child), ps = getComputedStyle(parent);
  return {
    parent:p, target:t, relativePx:t[axis]-p[axis],
    siblings:[...parent.children].map(e => ({id:e.id,rect:rect(e),position:getComputedStyle(e).position})),
    parentClientTop:parent.clientTop, offsetTop:child.offsetTop,
    report:document.querySelector('#log')?.textContent ?? null,
    font:{family:cs.fontFamily,size:cs.fontSize,
      faces:[...document.fonts].map(f=>({family:f.family,status:f.status}))},
    computed:{alignItems:ps.alignItems,alignSelf:cs.alignSelf,alignContent:ps.alignContent,
      flexWrap:ps.flexWrap,flexDirection:ps.flexDirection,writingMode:ps.writingMode,
      margin:[cs.marginTop,cs.marginRight,cs.marginBottom,cs.marginLeft]},
    data:Object.fromEntries([...child.attributes].filter(a=>a.name.startsWith('data-'))
           .map(a=>[a.name.slice(5),a.value])),
    viewport:[innerWidth,innerHeight,devicePixelRatio]
  };
}"""

LISTENER = b"""\nadd_completion_callback((tests, status) => {
  window.af108Harness = {status:status.status, tests:tests.map(t=>({name:t.name,status:t.status,message:t.message}))};
});\n"""


def run_browser(browser, server, cache, case, item, rep):
    from PIL import Image, ImageChops
    from playwright.sync_api import TimeoutError
    kind=case["case"]
    fixture, edited, refs = render_files(cache,case)
    original=item["form"]==case["original_form"]
    payload=(fixture if original else edited).encode()
    digest_ok=digest(payload)==item["render_sha256"]
    if not digest_ok:
        raise ValueError(f"Incorrect render SHA-256 for {kind}/{item['form']}")
    info={"case":kind,"input":item["form"],"repeat":rep,"engine":f"Chromium {browser.version}",
          "started_utc":utc(),"timeout_seconds_per_browser_action":TIMEOUT,
          "document_sha256":digest(payload),"input_sha256":item["sha256"],
          "path":case["raw_path"],"original":original,"url":server+case["raw_path"]}
    title=f"{kind}-{item['form']}"
    start=perf_counter()
    with browser.new_context(viewport={"width":800,"height":600}, device_scale_factor=1) as ctx:
        def route_assets(route):
            addr=route.request.url
            if not addr.startswith(server):
                route.abort()
            elif addr==info["url"] and not original:
                route.fulfill(status=200,content_type="text/html; charset=utf-8",body=payload)
            elif addr.endswith("/resources/testharness.js"):
                route.fulfill(status=200,content_type="application/javascript",
                              body=(cache/"resources/testharness.js").read_bytes()+LISTENER)
            else:
                route.continue_()
        ctx.route("**/*",route_assets)
        page=ctx.new_page()
        errors=[]
        failed=[]
        page.on("pageerror",lambda e:errors.append(str(e)))
        page.on("requestfailed",lambda r:failed.append([r.url,r.failure]))
        page.set_default_timeout(TIMEOUT*1000)
        try:
            response=page.goto(info["url"],wait_until="load")
            page.evaluate("document.fonts.ready")
            if "/resources/testharness.js" in fixture:
                page.wait_for_function("window.af108Harness !== undefined")
                info["harness"]=page.evaluate("window.af108Harness")
            probe=page.evaluate(MEASURE,[case["container"],case["target"],case["axis"]])
            assert probe["viewport"]==[800,600,1]
            sample=ROOT/"evidence"/"renders"/(title+".png")
            img=capture(page,sample,rep==1)
            info.update(exit=0,timed_out=False,document_status=response.status,probe=probe,
                        screenshot_sha256=digest(img),screenshot=sample.relative_to(ROOT).as_posix() if rep==1 else None)
            checks=native_assertions(probe, original)
            if kind=="F1":
                checks["original_script_margins"]={"report":probe["report"]}
            if refs and original:
                reference=ctx.new_page()
                response=reference.goto(urljoin(info["url"],refs[0]),wait_until="load")
                reference.evaluate("document.fonts.ready")
                ref_file=ROOT/"evidence"/"renders"/f"{kind}-ref.png"
                refimg=capture(reference,ref_file,rep==1)
                result=Image.open(BytesIO(img)).convert("RGB")
                expected=Image.open(BytesIO(refimg)).convert("RGB")
                diff=ImageChops.difference(result,expected)
                checks["pixel_match"]={"equal":diff.getbbox() is None,"difference_box":diff.getbbox(),
                    "reference_http":response.status,"reference_url":urljoin(WPT+case["raw_path"],refs[0]),
                    "reference_screen":ref_file.relative_to(ROOT).as_posix() if rep==1 else None,
                    "reference_screenshot_sha256":digest(refimg)}
            info["native_assertions"]=checks
        except TimeoutError as err:
            info.update(exit=1,timed_out=True,error=str(err))
        except Exception as err:
            info.update(exit=1,timed_out=False,error=str(err))
        info.update(page_errors=errors,failed_requests=failed)
    return dict(info,duration_seconds=perf_counter()-start,ended_utc=utc())


def main():
    from playwright.sync_api import sync_playwright
    from importlib.metadata import version
    parser=ArgumentParser()
    parser.add_argument("cache",type=Path)
    parser.add_argument("--chromium",default="/usr/bin/chromium")
    args=parser.parse_args()
    cache=args.cache
    sqlite=cache/"upstream"/"sqlite"
    shell=sqlite/"sqlite3"
    wpt=cache/"upstream"/"wpt"
    items=json.loads((ROOT/"inputs"/"selection.json").read_text())
    first=utc()
    src=sqlite/"manifest"
    trailer = b"# Remove this line to create a well-formed Fossil manifest.\n"
    manifest_sha = sha3_256(src.read_bytes().removesuffix(trailer)).hexdigest()
    if (sqlite/"manifest.uuid").read_text().strip()!=manifest_sha:
        raise ValueError("SQLite release manifest check failed")
    manifest_entries={s.split()[1]:s.split()[2] for s in src.read_text().splitlines() if s.startswith("F ")}
    for case in items[:4]:
        name=case["raw_path"]
        raw=checked(sqlite/name,case["raw_sha256"])
        if sha3_256(raw).hexdigest()!=manifest_entries[name]:
            raise ValueError(f"Fixture not in verified source manifest: {name}")
    by_case={c["case"]:c for c in items}
    repo_hashes={s:digest(ensure_path(wpt,s).read_bytes()) for s in RESOURCES}
    metadata={
      "started_utc":first, "argv":[str(shell),"-batch","-bail","-json",":memory:"],
      "sqlite_shell_sha256":digest(shell.read_bytes()),"sqlite_c_sha3_256":sha3_256((sqlite/"sqlite3.c").read_bytes()).hexdigest(),
      "sqlite_release_manifest_sha3_256":manifest_sha,
      "sqlite_version":subprocess.check_output([str(shell),"-version"],text=True).strip(),
      "sqlite_compile_options":subprocess.check_output([str(shell),":memory:","PRAGMA compile_options;"],text=True).splitlines(),
      "playwright":version("playwright"),"viewport":[800,600,1],"chromium_executable":args.chromium,
      "fontconfig_sans":subprocess.run(["fc-match","sans-serif"],text=True,capture_output=True).stdout.strip(),
      "wpt_raw_assets_sha256":repo_hashes,"wpt_pin":PIN,
      "scope":"Local runs only; a fresh SQLite process and :memory: database or fresh browser context/document for each repetition.",
    }
    all_runs=[]
    for case in items[:4]:
        for item in case["inputs"]:
            for repetition in (1,2):
                all_runs.append(run_sql(shell,case,item,repetition))
    with ThreadingHTTPServer(("127.0.0.1",0),partial(QuietHTTP,directory=wpt)) as server:
        Thread(target=server.serve_forever,daemon=True).start()
        addr=f"http://127.0.0.1:{server.server_port}/"
        with sync_playwright() as play:
            with play.chromium.launch(executable_path=args.chromium,args=["--disable-dev-shm-usage"]) as browser:
                metadata["chromium_version"]=browser.version
                for cid in ("F1","F2","F3","F4"):
                    case=by_case[cid]
                    for item in case["inputs"]:
                        for repetition in (1,2):
                            all_runs.append(run_browser(browser,addr,wpt,case,item,repetition))
        server.shutdown()
    metadata["ended_utc"]=utc()
    write_jsonl(ROOT/"runs.jsonl",all_runs)
    (ROOT/"evidence"/"engines.json").write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+"\n")
    for r in all_runs:
        print(r["case"],r["input"],r["repeat"],r["exit"],r.get("rows",r.get("probe",{}).get("relativePx")),
            (r.get("native_assertions") or {}).get("pixel_match",{}).get("equal"),
            r.get("error",""))
    return 0 if all(r["exit"]==0 for r in all_runs) else 1


if __name__=="__main__":
    raise SystemExit(main())
