#!/usr/bin/env python3
"""Inspect the POSIX and SVG examples outside the 16-input performance ledger."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess

from select_passages import ROOT, choose, digest, extract_web, measure_segment

POSIX_ORIGINAL = "https://pubs.opengroup.org/onlinepubs/9699919799/functions/fnmatch.html"
SVG = "https://www.w3.org/TR/2018/CR-SVG2-20181004/painting.html#FillRuleProperty"
GNULIB = "https://github.com/coreutils/gnulib/blob/adbe61f5ee7462a6e479f21d75ce51be919b7550/tests/test-fnmatch.c"
SVG_FIXTURE = ("https://github.com/web-platform-tests/wpt/blob/"
               "f1edffe3511493e684402fdfed42433e79374d55/svg/import/painting-fill-03-t-manual.svg")


def source_selection(raw, label, query, patterns):
    doc = raw
    if label == "posix":
        # man7 wraps mandoc prose as HTML preformatted text. Remove its common
        # 11-character display indent. Code-looking prototype lines stay code.
        doc = "\n".join(re.sub(r"^ {1,11}(?![ ])", "", line) if not
                        re.search(r"^\s*(?:#include|int fnmatch\()", line)
                        else line for line in raw.split("\n"))
        # Remove manpage-only column indent while keeping the numbered line map.
        doc = "\n".join(line[11:] if line.startswith(" "*11) and not
                        re.search(r"^\s*(?:#include|int fnmatch\()", line)
                        else line for line in doc.split("\n"))
    source, blocks, origins = extract_web(doc,label)
    selected, details = choose(source,blocks,query)
    anchors={}
    for name, pattern in patterns.items():
        hits=[m.span() for m in re.finditer(pattern,source,re.I|re.S)]
        anchors[name]=[{
           "span":list(span),
           "shown":{arm:any(a<=span[0]<span[1]<=b for a,b in windows)
                            for arm,windows in selected.items()},
           "sha256":digest(source[slice(*span)]),
        } for span in hits]
    return {
       "raw_view_sha256":digest(raw),"normalized_sha256":digest(source),
       "normalization_extra":"strip man7 common line indentation" if label=="posix" else None,
       "query":query,"selector":{k:v for k,v in details.items() if k!="exceptions"},
       "critical_ranges":anchors,
       "arms":{arm:{
          "segments":[measure_segment(source,span,origins) for span in windows],
          "marker_sentences":[s for s in details["exceptions"] if any(a<=s[0]<s[1]<=b for a,b in windows)],
       } for arm,windows in selected.items()},
    }


def posix(cache):
    source = r"""
    #include <fnmatch.h>
    #include <stdio.h>

    int main(void) {
      printf("%d %d %d %d %d\n", fnmatch("?rc", ".rc", 0),
             fnmatch("?rc", ".rc", FNM_PERIOD),
             fnmatch("d/?rc", "d/.rc", FNM_PERIOD),
             fnmatch("d/?rc", "d/.rc", FNM_PERIOD | FNM_PATHNAME),
             FNM_NOMATCH);
      return 0;
    }
    """
    bin_path=cache/"fnmatch-example"
    compile_argv=["cc","-x","c","-o",str(bin_path),"-"]
    built=subprocess.run(compile_argv,input=source,text=True,capture_output=True,timeout=20,check=True)
    ran=subprocess.run([str(bin_path)],text=True,capture_output=True,timeout=10,check=True)
    upstream=cache/"upstream"/"gnulib-fnmatch"
    data=source_selection((cache/"docs"/"posix_view.view").read_text(),"posix",
       [["fnmatch","pattern","period","flags"],["leading","string","match","slash","pathname"]],
       {"leading_rule":r"If FNM_PERIOD is set in flags, then a leading <period>.*?value of FNM_PATHNAME:",
        "path_component":r"If FNM_PATHNAME is set, a <period> is .*?follows a\s*<slash>",
        "without_flag":r"If FNM_PERIOD is not set, then no special restrictions are placed\s+on matching a period"})
    return dict(data,normative_url=POSIX_ORIGINAL,
        capture_url="https://man7.org/linux/man-pages/man3/fnmatch.3p.html",
        canonical_open="403, 미확인",test_url=GNULIB,test_sha256=digest(upstream.read_bytes()),
        test_position="lines 388–450, ?rc/.rc; tests FNM_PERIOD with and without literal leading period",
        execution={"argv":compile_argv,"compile_exit":built.returncode,"run_exit":ran.returncode,
                   "stdout":ran.stdout.strip(),"stderr":ran.stderr,"c_source":source.strip(),
                   "libc":subprocess.check_output(["getconf","GNU_LIBC_VERSION"],text=True).strip()})


def svg(cache):
    from playwright.sync_api import sync_playwright
    path=cache/"upstream"/"painting-fill-03-t-manual.svg"
    data=source_selection((cache/"docs"/"svg_view.view").read_text(),"svg",
      [["fill","rule","nonzero","evenodd","crosses"],["path","count","point","inside","outside","overlap"]],
      {"parity":r"If this number is odd, the point is inside; if even, the point is outside\.",
       "winding_test":r"After counting the crossings, if the result is zero then the point is outside the path\. Otherwise, it is inside\.",
       "default":r"Initial:\s*\|\s*nonzero"})
    with sync_playwright() as pw:
        with pw.chromium.launch(executable_path="/usr/bin/chromium",args=["--disable-dev-shm-usage"]) as browser:
            with browser.new_context(viewport={"width":800,"height":600}) as ctx:
                url="http://127.0.0.1:9013/painting-fill-03-t.svg"
                ctx.route("**/*",lambda route:route.fulfill(
                    status=200,content_type="image/svg+xml",body=path.read_bytes())
                    if route.request.url==url else route.abort())
                page=ctx.new_page()
                page.goto(url,timeout=8000)
                result=page.evaluate("""() => [...document.querySelectorAll('path[fill-rule]')].map((p,i)=>({
                    rule:p.getAttribute('fill-rule'),xy:[110+255*i,155],center:p.isPointInFill(new DOMPoint(110+255*i,155))}))""")
                runtime={"browser":browser.version,"point_tests":result,
                         "method":"SVGGeometryElement.isPointInFill in fixture user coordinates","exit":0}
    return dict(data,normative_url=SVG,test_url=SVG_FIXTURE,test_sha256=digest(path.read_bytes()),
                test_position="painting-fill-03-t-manual.svg:14–29,47–50",execution=runtime)


def tie(cache):
    shell=cache/"upstream"/"sqlite"/"sqlite3"
    stmt="CREATE TABLE t5(a,b); INSERT INTO t5 VALUES(2,10),(2,9); SELECT * FROM t5 ORDER BY 1;"
    original=subprocess.run([str(shell),"-batch","-json",":memory:"],input=stmt,text=True,capture_output=True,check=True,timeout=10)
    alter=stmt.replace(" SELECT"," CREATE INDEX ix ON t5(a,b); EXPLAIN QUERY PLAN SELECT",1)+" SELECT * FROM t5 ORDER BY 1;"
    indexed=subprocess.run([str(shell),"-batch","-json",":memory:"],input=alter,text=True,capture_output=True,check=True,timeout=10)
    return {"baseline":{"stdin":stmt,"stdout":original.stdout,"exit":original.returncode},
            "counterexample":{"stdin":alter,"stdout":indexed.stdout,"exit":indexed.returncode},
            "scope":"Post-seal diagnostic; same tie input and ORDER BY, additional covering index. Excluded from main sample."}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("cache",type=Path)
    args=p.parse_args()
    result={"utc":datetime.now(timezone.utc).isoformat(),"main_sample":False,
            "posix":posix(args.cache),"svg":svg(args.cache),"s3_tie_index":tie(args.cache)}
    (ROOT/"evidence"/"calibration.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")


if __name__=="__main__":
    main()
