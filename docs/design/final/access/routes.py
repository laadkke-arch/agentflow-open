"""catalog 대상을 원문 경로별로 나누고, 표본에서 인용이 실제로 원문(또는 원천)에 있는지 잰다.

읽기만 한다. 네트워크는 이 클라우드 환경에서 열린 곳(raw.githubusercontent.com, pypi.org, proxy.golang.org,
index.crates.io, static.crates.io, gitlab.com API)만 쓴다. 요청 사이 0.3초 쉰다.
"""
import gzip, io, json, re, sys, time, random, tarfile, zipfile, unicodedata, urllib.parse, urllib.request, urllib.error
from collections import Counter, defaultdict

SRC = sys.argv[1]
OUT = sys.argv[2]
PER_ROUTE = int(sys.argv[3]) if len(sys.argv) > 3 else 40
random.seed(20261127)

rows = [json.loads(l) for l in gzip.open(SRC, "rt")]


def host(u):
    return (urllib.parse.urlsplit(u).hostname or "?").lower()


# ---------- 경로 나누기 ----------
def classify(u):
    s = urllib.parse.urlsplit(u)
    h = (s.hostname or "").lower()
    p = [x for x in s.path.split("/") if x]
    if h == "raw.githubusercontent.com":
        return "A1-gh-raw", [u]
    if h == "github.com" and len(p) >= 2:
        o, r = p[0], p[1]
        if len(p) >= 5 and p[2] == "blob":
            return "A1-gh-blob", [f"https://raw.githubusercontent.com/{o}/{r}/{p[3]}/{'/'.join(p[4:])}"]
        if len(p) == 2:
            return "A1-gh-readme", [f"https://raw.githubusercontent.com/{o}/{r}/HEAD/{n}" for n in
                                    ("README.md", "README.rst", "README", "readme.md", "README.markdown")]
        if len(p) >= 3 and p[2] in ("issues", "pull", "discussions", "wiki", "releases", "commit"):
            return "A3-gh-api-only", []
        if len(p) >= 4 and p[2] == "tree":
            return "A1-gh-tree", [f"https://raw.githubusercontent.com/{o}/{r}/{p[3]}/{'/'.join(p[4:])}/README.md"]
        return "A3-gh-other", []
    if h == "gist.github.com":
        return "A3-gh-other", []
    if h == "pypi.org":
        name = None
        if len(p) >= 2 and p[0] == "project":
            name = p[1]
        elif len(p) >= 2 and p[0] == "pypi":
            name = p[1]
        if name:
            ver = p[2] if p[0] == "project" and len(p) >= 3 else (p[2] if p[0] == "pypi" and len(p) >= 4 else None)
            return "A2-pypi", [f"https://pypi.org/pypi/{name}/{ver}/json" if ver else f"https://pypi.org/pypi/{name}/json"]
        return "C-web", []
    if h == "pkg.go.dev" and p and "." in p[0]:
        return "A2-goproxy", ["/".join(p)]
    if h == "docs.rs" and p and p[0] not in ("about", "releases", "crate"):
        return "A2-crates", [p[0], p[1] if len(p) > 1 else "latest"]
    if h == "docs.python.org" and len(p) >= 2:
        ver = p[0]
        branch = "main" if ver in ("3", "dev") else ver
        if re.fullmatch(r"\d\.\d+", ver) or ver in ("3", "dev"):
            path = "/".join(p[1:])
            if path.endswith(".html"):
                path = path[:-5]
            return "B-docs-python", [f"https://raw.githubusercontent.com/python/cpython/{branch}/Doc/{path}.rst"]
        if len(p) >= 2 and re.fullmatch(r"[a-z]{2}(-[a-z]{2})?", ver):
            return "B-docs-python-xlang", []
    if h == "developer.mozilla.org" and len(p) >= 3 and p[1] == "docs":
        loc = p[0].lower()
        path = "/".join(p[2:]).lower().replace(":", "_colon_").replace("*", "_star_")
        repo = "mdn/content" if loc == "en-us" else "mdn/translated-content"
        return "B-mdn" if loc == "en-us" else "B-mdn-xlang", [f"https://raw.githubusercontent.com/{repo}/main/files/{loc}/{path}/index.md"]
    if h == "docs.github.com" and len(p) >= 2:
        path = "/".join(p[1:])
        c = [f"https://raw.githubusercontent.com/github/docs/main/content/{path}.md",
             f"https://raw.githubusercontent.com/github/docs/main/content/{path}/index.md"]
        return ("B-ghdocs" if p[0] == "en" else "B-ghdocs-xlang"), c
    if h == "kubernetes.io" and p:
        lang = "en"
        q = p
        if re.fullmatch(r"[a-z]{2}(-[a-z]{2})?", p[0]) and p[0] not in ("docs", "blog"):
            lang, q = p[0], p[1:]
        if q and q[0] == "docs":
            path = "/".join(q)
            c = [f"https://raw.githubusercontent.com/kubernetes/website/main/content/{lang}/{path}{s}" for s in
                 (".md", "/_index.md", "/index.md")]
            return "B-k8s", c
        return "B-k8s-blog", []
    if h == "learn.microsoft.com" and len(p) >= 3:
        loc = p[0]
        if p[1] == "azure":
            path = "/".join(p[2:])
            return ("B-mslearn-azure" if loc == "en-us" else "B-mslearn-azure-xlang"), [
                f"https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/main/articles/{path}.md",
                f"https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/main/articles/{path}/index.md"]
        if p[1] == "dotnet":
            path = "/".join(p[2:])
            return ("B-mslearn-dotnet" if loc == "en-us" else "B-mslearn-dotnet-xlang"), [
                f"https://raw.githubusercontent.com/dotnet/docs/main/docs/{path}.md",
                f"https://raw.githubusercontent.com/dotnet/docs/main/docs/{path}/index.md"]
        return "B-mslearn-other", []
    if h == "docs.gitlab.com" and p:
        path = "/".join(p)
        enc = lambda x: urllib.parse.quote(x, safe="")
        return "B-gitlab", [f"https://gitlab.com/api/v4/projects/278964/repository/files/{enc('doc/' + path + s)}/raw?ref=master"
                            for s in (".md", "/index.md", "/_index.md")]
    # 원천이 GitHub에 있다고 알려진 문서 사이트(이번에 재지 않음)
    if h in ("git-scm.com", "www.postgresql.org", "www.php.net", "www.w3.org", "docs.qgis.org", "www.mongodb.com",
             "www.elastic.co", "www.rfc-editor.org", "datatracker.ietf.org", "manpages.debian.org",
             "sources.debian.org", "chromium.googlesource.com", "apache.googlesource.com",
             "android.googlesource.com", "www.mediawiki.org", "docs.oracle.com"):
        return "B-unmeasured", []
    return "C-web", []


# ---------- 가져오기 ----------
LOG = []


def get(url, binary=False):
    time.sleep(0.3)
    req = urllib.request.Request(url, headers={"User-Agent": "afledger-route-probe/0"})
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            b = r.read()
            st = r.status
    except urllib.error.HTTPError as e:
        b, st = b"", e.code
    except Exception as e:  # noqa
        b, st = b"", 0
    LOG.append({"url": url, "status": st, "bytes": len(b), "ms": int((time.time() - t) * 1000)})
    return st, b


# ---------- 인용 대조 ----------
def norm_tokens(s):
    s = unicodedata.normalize("NFKC", s).lower()
    # rst 역할·마크다운 기호를 지운다
    s = re.sub(r":[a-z:]+:`~?", " ", s)
    s = re.sub(r"[`*_#>|\\\[\]{}()<>~=]", " ", s)
    return re.findall(r"[0-9a-zÀ-ɏͰ-ϿЀ-ӿ]+|[぀-ヿ㐀-鿿가-힯]", s)


def match(evidence, source_tokens_str, source_shingles):
    q = norm_tokens(evidence)
    if len(q) < 6:
        return None   # 대조하지 않음(짧음)
    qs = " ".join(q)
    if qs in source_tokens_str:
        return "exact"
    sh = [tuple(q[i:i + 4]) for i in range(len(q) - 3)]
    cov = sum(1 for x in sh if x in source_shingles) / len(sh)
    return "near" if cov >= 0.8 else "miss"


def evidences(r):
    out = []
    for c in r["claims"]:
        e = (c.get("evidence") or "").strip()
        if e:
            out.append((c.get("basis"), e))
    return out


def source_text_for(route, cands):
    """경로마다 원문(또는 원천) 텍스트를 돌려준다. (상태, 텍스트, 실제 주소)"""
    if route.startswith("A2-pypi"):
        st, b = get(cands[0])
        if st != 200:
            return st, "", cands[0]
        d = json.loads(b)
        info = d.get("info", {})
        return 200, (info.get("summary") or "") + "\n" + (info.get("description") or ""), cands[0]
    if route == "A2-goproxy":
        parts = cands[0].split("/")
        ver = None
        for i, x in enumerate(parts):
            if "@" in x:
                parts[i], ver = x.split("@", 1)
        for n in range(len(parts), 0, -1):
            mod = "/".join(parts[:n])
            esc = re.sub(r"[A-Z]", lambda m: "!" + m.group(0).lower(), mod)
            st, b = get(f"https://proxy.golang.org/{esc}/@{'v/' + ver + '.info' if ver else 'latest'}")
            if st == 200:
                info = json.loads(b)
                v = info["Version"]
                st2, z = get(f"https://proxy.golang.org/{esc}/@v/{v}.zip")
                if st2 != 200:
                    return st2, "", mod
                sub = "/".join(parts[n:])
                zf = zipfile.ZipFile(io.BytesIO(z))
                txt = []
                for name in zf.namelist():
                    rel = name.split("@", 1)[1].split("/", 1)[1] if "@" in name else name
                    d = rel.rsplit("/", 1)[0] if "/" in rel else ""
                    if (d == sub) and (name.endswith(".go") or name.endswith(".md")):
                        txt.append(zf.read(name).decode("utf-8", "replace"))
                if not txt:
                    for name in zf.namelist():
                        if name.endswith(".md") or name.endswith("doc.go"):
                            txt.append(zf.read(name).decode("utf-8", "replace"))
                return 200, "\n".join(txt), f"{mod}@{v} ({info.get('Origin', {}).get('Hash', '')[:12]})"
        return 404, "", cands[0]
    if route == "A2-crates":
        crate, ver = cands
        c = crate.lower()
        pre = (f"1/{c}" if len(c) == 1 else f"2/{c}" if len(c) == 2 else f"3/{c[0]}/{c}" if len(c) == 3
               else f"{c[:2]}/{c[2:4]}/{c}")
        st, b = get(f"https://index.crates.io/{pre}")
        if st != 200:
            return st, "", crate
        vers = [json.loads(l) for l in b.decode().splitlines() if l.strip()]
        vs = [v["vers"] for v in vers if not v.get("yanked")]
        if not vs:
            return 404, "", crate
        v = ver if ver in vs else vs[-1]
        st, b = get(f"https://static.crates.io/crates/{c}/{c}-{v}.crate")
        if st != 200:
            return st, "", crate
        txt = []
        with tarfile.open(fileobj=io.BytesIO(b), mode="r:gz") as tf:
            for m in tf.getmembers():
                if m.isfile() and (m.name.endswith(".rs") or m.name.endswith(".md")) and m.size < 2_000_000:
                    txt.append(tf.extractfile(m).read().decode("utf-8", "replace"))
        return 200, "\n".join(txt), f"{c}-{v}.crate"
    last = None
    for u in cands:
        st, b = get(u)
        last = (st, u)
        if st == 200:
            return 200, b.decode("utf-8", "replace"), u
    return (last[0] if last else 0), "", (last[1] if last else "")


by_route = defaultdict(list)
for r in rows:
    route, c = classify(r["url"])
    by_route[route].append((r, c))

summary = {"targets": len(rows), "routes": {k: len(v) for k, v in sorted(by_route.items())},
           "levels_by_route": {k: dict(Counter(r["level"] for r, _ in v)) for k, v in sorted(by_route.items())}}

measure = {}
for route, items in sorted(by_route.items()):
    if route.startswith("C-") or route in ("A3-gh-api-only", "A3-gh-other", "B-unmeasured", "B-k8s-blog",
                                            "B-mslearn-other", "B-docs-python-xlang"):
        continue
    # 대조할 수 있는 인용이 있는 대상만 뽑는다
    pool = [(r, c) for r, c in items if any(len(norm_tokens(e)) >= 6 for _, e in evidences(r))]
    sample = random.sample(pool, min(PER_ROUTE, len(pool)))
    res = Counter()
    ex = []
    for r, c in sample:
        st, txt, where = source_text_for(route, c)
        if st != 200 or not txt:
            res[f"fetch_{st}"] += 1
            ex.append({"key": r["key"], "status": st, "where": where})
            continue
        toks = norm_tokens(txt)
        tstr = " ".join(toks)
        sh = set(tuple(toks[i:i + 4]) for i in range(len(toks) - 3))
        best = None
        for basis, e in evidences(r):
            m = match(e, tstr, sh)
            if m == "exact" or (m == "near" and best != "exact") or (m == "miss" and best is None):
                best = m
        res[best or "short"] += 1
        ex.append({"key": r["key"], "status": st, "where": where, "result": best, "level_before": r["level"]})
    measure[route] = {"population": len(items), "with_quotable_evidence": len(pool), "sample": len(sample),
                      "result": dict(res), "examples": ex}
    print(route, len(items), len(pool), len(sample), dict(res), flush=True)

summary["measure"] = measure
summary["requests"] = {"count": len(LOG), "by_status": dict(Counter(x["status"] for x in LOG)),
                       "bytes": sum(x["bytes"] for x in LOG)}
summary["log"] = LOG
json.dump(summary, open(OUT, "w"), ensure_ascii=False, indent=1)
