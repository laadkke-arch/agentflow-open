"""주소 정규화.

한 주소에서 세 가지 키를 만든다. 원래 주소 문자열은 절대 고치지 않고 따로 둔다.

- url_norm : 같은 주소. 스킴·호스트 대소문자, www, 추적 인자, 조각(#), 끝 빗금을 접은 문자열.
- page     : 같은 문서. 판(태그·커밋·버전)을 떼어 낸 문서 키. 예: gh:owner/repo/src/a.py
- target   : 같은 대상. 프로젝트·작품 하나. 예: gh:owner/repo, pypi:requests, arxiv:2401.01234

떼어 낸 판은 edition, 조각·줄·경로는 position에 남긴다. 규칙은 이 파일 하나에만 둔다.
판 사이 위치 대응(같은 함수가 다른 줄 번호로 옮겨 감)은 하지 않는다. 그것은 자료를 읽은 뒤의 일이다.

표준 라이브러리만 쓴다(Python 3.9+).
"""
from __future__ import annotations

import html
import ipaddress
import re
import unicodedata
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit

RULES_VERSION = "n1"

# ---------------------------------------------------------------- 일반 규칙

TRACKING_EXACT = {
    "fbclid", "gclid", "dclid", "gbraid", "wbraid", "msclkid", "mc_cid", "mc_eid",
    "igshid", "yclid", "_ga", "_gl", "mkt_tok", "ref_src", "ref_url", "spm",
    "scm", "share_from", "sharesource", "from_source", "cmpid", "ito", "_hsenc",
    "_hsmi", "hsctatracking", "oly_anon_id", "oly_enc_id", "vero_id", "trk",
    "trkcampaign", "rdt", "srsltid", "si", "pk_campaign", "pk_kwd", "mtm_campaign",
}
TRACKING_PREFIX = ("utm_", "hsa_", "pk_", "mtm_")
# 'ref'는 많은 곳에서 추적용이지만 코드 호스팅에서는 브랜치를 뜻한다.
REF_IS_TRACKING_EXCEPT = {"github.com", "gitlab.com", "api.github.com", "codeberg.org", "gitee.com", "bitbucket.org"}
# 호스트별로 뜻 있는 인자만 남기는 곳
KEEP_ONLY = {
    "youtube.com": {"v", "list"},
    "news.ycombinator.com": {"id"},
    "news.hada.io": {"id"},
    "openreview.net": {"id"},
    "play.google.com": {"id"},
    "facebook.com": {"id", "story_fbid", "v"},
}
DROP_ALWAYS_ON = {
    "youtube.com": {"feature", "t", "ab_channel", "pp"},
    "twitter.com": {"s", "t", "ref_src"},
    "x.com": {"s", "t"},
}
INDEX_FILES = ("index.html", "index.htm", "index.php", "default.aspx", "default.htm", "index.shtml")
MOBILE_PREFIX_HOSTS = ("wikipedia.org", "wiktionary.org", "wikimedia.org", "youtube.com", "facebook.com", "twitter.com", "reddit.com")

# 남의 주소를 싸고 있는 주소. (호스트, 경로 정규식 또는 인자 이름)
CITATION_ARTIFACTS = re.compile(
    r"(\ue200.*?\ue201)|【[^】]*\u2020[^】]*】|citeturn\d+\w*?\d+|\u2020source"
    r"|\s*\(\[[^\]]{1,80}\]\(https?://[^)\s]*utm_source=chatgpt\.com[^)\s]*\)\)"
)


class NotASource(ValueError):
    """검색 결과 페이지, 대화 공유 주소처럼 원문이 아닌 주소."""


def clean_raw(url: str) -> str:
    """붙여넣기에서 흔히 붙는 군더더기를 걷는다. 주소 문자 자체는 바꾸지 않는다."""
    s = CITATION_ARTIFACTS.sub("", url or "").strip()
    if re.search(r"&(?:amp|quot|lt|gt|#\d+);", s):
        s = html.unescape(s)
    # 글에서 뽑을 때 따라 들어온 이스케이프(\\n 등)나 공백 뒤는 주소가 아니다
    s = re.split(r"\\[nrt\"']|\s", s, maxsplit=1)[0]
    s = s.rstrip("\\")
    # 마크다운 링크 [글](주소) 또는 <주소>
    m = re.match(r"^\[[^\]]*\]\((\S+?)\)$", s)
    if m:
        s = m.group(1)
    s = s.strip().strip("<>").strip()
    # 문장 끝 구두점, 짝 안 맞는 닫는 괄호
    while s and s[-1] in ".,;:!?'\"”’」』）】>":
        s = s[:-1]
    while s.endswith(")") and s.count(")") > s.count("("):
        s = s[:-1]
    while s.endswith("]") and s.count("]") > s.count("["):
        s = s[:-1]
    while s.endswith("}") and s.count("}") > s.count("{"):
        s = s[:-1]
    while s and s[-1] in ".,;:!?'\"”’」』）】>":
        s = s[:-1]
    # 웹챗이 붙이는 추적 인자. 조각(#) 뒤에 붙어 나오는 경우도 있다.
    s = re.sub(r"([?&])utm_source=chatgpt\.com(&|(?=#)|$)", lambda m: m.group(1) if m.group(2) == "&" else "", s)
    s = re.sub(r"(#[^?]*)\?(?:utm_[a-z]+|ref|source)=[^#]*$", r"\1", s)
    if s.startswith("//"):
        s = "https:" + s
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", s) and re.match(r"^[\w.-]+\.[a-z]{2,}(/|$)", s, re.I):
        s = "https://" + s
    return s


def _host(netloc: str) -> tuple[str, str]:
    """(호스트, 포트 접은 netloc)"""
    hostport = netloc.rsplit("@", 1)[-1]
    if hostport.startswith("["):
        return hostport.lower(), hostport.lower()
    host, _, port = hostport.partition(":")
    host = host.strip(".").lower()
    try:
        host = host.encode("idna").decode("ascii") if any(ord(c) > 127 for c in host) else host
    except UnicodeError:
        pass
    if port in ("", "80", "443"):
        return host, host
    return host, f"{host}:{port}"


def bare_host(host: str) -> str:
    h = host
    if h.startswith("www."):
        h = h[4:]
    for suffix in MOBILE_PREFIX_HOSTS:
        if h.endswith(suffix):
            parts = h.split(".")
            if parts[0] in ("m", "mobile") or (len(parts) > 2 and parts[1] == "m"):
                parts = [p for i, p in enumerate(parts) if not (p in ("m", "mobile") and i < len(parts) - 2)]
                h = ".".join(parts)
    if h in ("old.reddit.com", "new.reddit.com", "np.reddit.com"):
        h = "reddit.com"
    if h in ("mobile.twitter.com",):
        h = "twitter.com"
    return h


_UNRESERVED = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~")


def _norm_path(path: str, keep_index: bool = False) -> str:
    """퍼센트 인코딩을 한 형태로 맞춘다.

    비예약 ASCII는 풀고, 예약 문자(/?#& 등)와 공백은 대문자 16진수로 둔다.
    UTF-8 바이트열은 읽을 수 있게 글자로 푼다(뜻이 바뀌지 않는다).
    """
    path = path.replace(" ", "%20")

    def fix_ascii(m: re.Match) -> str:
        b = int(m.group(1), 16)
        if b < 0x80:
            c = chr(b)
            return c if c in _UNRESERVED else "%" + m.group(1).upper()
        return "%" + m.group(1).upper()

    path = re.sub(r"%([0-9A-Fa-f]{2})", fix_ascii, path)

    def fix_utf8(m: re.Match) -> str:
        raw = bytes.fromhex(m.group(0).replace("%", ""))
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            return m.group(0)

    path = re.sub(r"(?:%[89A-F][0-9A-F])+", fix_utf8, path)
    path = unicodedata.normalize("NFC", path)
    segs = []
    for seg in path.split("/"):
        if seg == "..":
            if segs:
                segs.pop()
        elif seg not in (".", ""):
            segs.append(seg)
    out = "/" + "/".join(segs)
    for idx in ([] if keep_index else INDEX_FILES):
        if out.lower().endswith("/" + idx):
            out = out[: -len(idx)].rstrip("/") or "/"
    return out


def _norm_query(query: str, host: str) -> str:
    pairs = parse_qsl(query, keep_blank_values=True)
    keep_only = None
    drop = set()
    for h, keys in KEEP_ONLY.items():
        if host == h or host.endswith("." + h):
            keep_only = keys
    for h, keys in DROP_ALWAYS_ON.items():
        if host == h or host.endswith("." + h):
            drop = keys
    out = []
    for k, v in pairs:
        kl = k.lower()
        if keep_only is not None and k not in keep_only:
            continue
        if k in drop or kl in TRACKING_EXACT or kl.startswith(TRACKING_PREFIX):
            continue
        if kl in ("ref", "source", "via") and host not in REF_IS_TRACKING_EXCEPT:
            continue
        out.append((k, v))
    out.sort()
    return urlencode(out, doseq=True)


def _unwrap(url: str, depth: int = 0) -> tuple[str, dict]:
    """감싼 주소(검색 이동, 웹 보관소, AMP, 하테나 북마크)를 벗긴다. 벗긴 사실은 extra에 남긴다."""
    extra: dict = {}
    if depth > 3:
        return url, extra
    p = urlsplit(url)
    host = bare_host(_host(p.netloc)[0])
    q = dict(parse_qsl(p.query))
    inner = None
    if host in ("google.com", "google.co.jp", "google.co.kr") and p.path == "/url":
        inner = q.get("q") or q.get("url")
    elif host == "l.facebook.com" and p.path == "/l.php":
        inner = q.get("u")
    elif host == "out.reddit.com":
        inner = q.get("url")
    elif host in ("duckduckgo.com",) and p.path.startswith("/l/"):
        inner = q.get("uddg")
    elif host == "href.li":
        inner = p.query or None
    elif host == "web.archive.org":
        m = re.match(r"^/web/(\d{1,14})(?:[a-z]{2}_)?/(.+)$", p.path + (("?" + p.query) if p.query else ""))
        if m:
            extra["archive"] = f"wayback:{m.group(1)}"
            inner = m.group(2)
            if not re.match(r"^[a-z]+:/", inner):
                inner = "http://" + inner
            inner = re.sub(r"^(https?):/([^/])", r"\1://\2", inner)
    elif host == "google.com" and p.path.startswith("/amp/s/"):
        inner = "https://" + p.path[len("/amp/s/"):]
    elif host.endswith(".cdn.ampproject.org") and re.match(r"^/[cv]/s/", p.path):
        inner = "https://" + re.sub(r"^/[cv]/s/", "", p.path)
    elif host == "b.hatena.ne.jp" and p.path.startswith("/entry/"):
        rest = p.path[len("/entry/"):]
        if rest.startswith("s/"):
            inner = "https://" + rest[2:]
        elif re.match(r"^\d+$", rest):
            inner = None
        else:
            inner = "http://" + rest
        if inner:
            extra["wrapper"] = "hatena-bookmark"
    if inner and inner != url:
        if "wrapper" not in extra and "archive" not in extra:
            extra["wrapper"] = host
        u2, e2 = _unwrap(inner, depth + 1)
        e2.update({k: v for k, v in extra.items() if k not in e2})
        return u2, e2
    return url, extra


NOT_SOURCE = [
    (re.compile(r"^(google\.[a-z.]+|bing\.com|duckduckgo\.com|search\.yahoo\.[a-z.]+|search\.naver\.com|yandex\.[a-z]+)$"), re.compile(r"^/(search|html|$)")),
    (re.compile(r"^(chatgpt\.com|chat\.openai\.com)$"), re.compile(r".*")),
    (re.compile(r"^github\.com$"), re.compile(r"^/search($|/)")),
]

# ---------------------------------------------------------------- 대상 규칙

GH_RESERVED = {
    "orgs", "settings", "marketplace", "topics", "sponsors", "features", "about", "collections",
    "trending", "search", "notifications", "apps", "login", "logout", "join", "site", "pricing", "enterprise",
    "explore", "issues", "pulls", "users", "new", "codespaces", "security", "customer-stories",
    "readme", "events", "team", "contact", "github", "solutions", "resources", "signup", "dashboard", "discussions",
    "organizations", "account", "stars", "watching", "copilot", "premium-support", "advisories",
}
REF_LIKE = re.compile(r"^(main|master|trunk|develop|dev|default|head|gh-pages|stable|latest|[0-9a-f]{7,40}|v?\d+(?:[._-]\d+)*(?:[-.+]?[A-Za-z0-9.]+)?)$", re.I)


def _split_ref(rest: list[str]) -> tuple[str | None, list[str]]:
    if not rest:
        return None, []
    return rest[0], rest[1:]


def _code_host(prefix: str, owner: str, repo: str, rest: list[str], lower: bool = True) -> dict:
    o, r = (owner.lower(), repo.lower()) if lower else (owner, repo)
    if r.endswith(".git"):
        r = r[:-4]
    target = f"{prefix}:{o}/{r}"
    edition = None
    position = None
    page = target
    if rest:
        kind = rest[0]
        if kind in ("blob", "tree", "raw", "blame", "src", "commits", "history", "edit"):
            sub = rest[1:]
            if kind == "src" and sub[:1] and sub[0] in ("branch", "tag", "commit"):
                sub = sub[1:]
            ref, path = _split_ref(sub)
            edition = ref
            hist = kind in ("commits", "history")
            if path:
                position = "/".join(path)
                page = f"{target}/commits/{position}" if hist else f"{target}/{position}"
            elif hist:
                page = f"{target}/commits"
        elif kind == "commit" and len(rest) >= 2:
            edition = rest[1]
            page = f"{target}/commit/{rest[1].lower()[:12]}"
        elif kind in ("issues", "pull", "pulls", "discussions", "merge_requests") and len(rest) >= 2 and rest[1].isdigit():
            page = f"{target}/{'pull' if kind in ('pull', 'pulls', 'merge_requests') else kind}/{rest[1]}"
        elif kind == "releases":
            if len(rest) >= 3 and rest[1] == "tag":
                edition = rest[2]
            page = f"{target}/releases"
        elif kind == "wiki" or kind == "wikis":
            page = f"{target}/wiki/{'/'.join(rest[1:])}".rstrip("/")
        elif kind == "archive" and len(rest) >= 2:
            edition = re.sub(r"\.(zip|tar\.gz|tgz)$", "", rest[-1])
            page = f"{target}/archive"
        else:
            page = f"{target}/{'/'.join(rest)}"
    return {"target": target, "page": page, "edition": edition, "position": position}


def _pep503(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def target_of(host: str, path: str, query: str) -> dict:
    """호스트별 규칙. 모르는 호스트는 target=None, page=None을 돌려 일반 규칙을 쓰게 한다."""
    segs = [s for s in path.split("/") if s]
    q = dict(parse_qsl(query))
    res: dict = {"target": None, "page": None, "edition": None, "position": None, "host_kind": "web"}

    def done(kind: str, **kw):
        res.update(kw)
        res["host_kind"] = kind
        if res.get("page") is None:
            res["page"] = res.get("target")
        return res

    # --- 코드 호스팅
    if host == "github.com":
        if len(segs) >= 2 and segs[0].lower() not in GH_RESERVED:
            return done("code", **_code_host("gh", segs[0], segs[1], segs[2:]))
        if len(segs) == 1 and segs[0].lower() not in GH_RESERVED:
            return done("code", target=f"gh:{segs[0].lower()}")
        return done("code")
    if host == "raw.githubusercontent.com" and len(segs) >= 3:
        d = _code_host("gh", segs[0], segs[1], ["blob"] + segs[2:])
        return done("code", **d)
    if host == "api.github.com":
        if len(segs) >= 3 and segs[0] == "repos":
            d = _code_host("gh", segs[1], segs[2], [])
            d["page"] = "ghapi:" + "/".join(segs[1:]).lower()
            return done("api", **d)
        return done("api")
    if host == "gist.github.com" and len(segs) >= 1:
        gid = segs[-1] if len(segs) >= 2 else segs[0]
        return done("code", target=f"gist:{gid.lower()}")
    if host.endswith(".github.io"):
        owner = host[: -len(".github.io")]
        repo = segs[0] if segs else f"{owner}.github.io"
        d = {"target": f"gh:{owner}/{repo.lower()}", "page": f"{host}{path}".rstrip("/")}
        return done("pages", **d)
    if host == "gitee.com" and len(segs) >= 2:
        return done("code", **_code_host("gitee", segs[0], segs[1], segs[2:]))
    if host in ("codeberg.org", "gitea.com", "git.disroot.org", "notabug.org") and len(segs) >= 2:
        pref = "cb" if host == "codeberg.org" else f"forgejo@{host}"
        return done("code", **_code_host(pref, segs[0], segs[1], segs[2:]))
    if host == "bitbucket.org" and len(segs) >= 2:
        return done("code", **_code_host("bb", segs[0], segs[1], segs[2:]))
    if host == "git.sr.ht" and len(segs) >= 2 and segs[0].startswith("~"):
        rest = segs[2:]
        if rest[:1] == ["tree"] and len(rest) >= 2:
            ref = rest[1]
            path = rest[3:] if rest[2:3] == ["item"] else rest[2:]
            rest = ["blob", ref] + path
        return done("code", **_code_host("srht", segs[0], segs[1], rest))
    if host == "sr.ht" or host.endswith(".sr.ht"):
        m = re.match(r"^(todo|lists|builds|man|hg)\.sr\.ht$", host)
        if m and len(segs) >= 2 and segs[0].startswith("~"):
            return done("code", target=f"srht:{segs[0].lower()}/{segs[1].lower()}")
    if host == "gitlab.com" or host in GITLAB_HOSTS:
        if "-" in segs:
            i = segs.index("-")
            proj, rest = segs[:i], segs[i + 1:]
        else:
            proj, rest = segs, []
            for i, s in enumerate(segs):
                if s in ("blob", "tree", "raw", "issues", "merge_requests", "commit", "commits", "wikis", "releases") and i >= 2:
                    proj, rest = segs[:i], segs[i:]
                    break
        if len(proj) >= 2 and proj[0] not in ("explore", "users", "help", "dashboard", "search"):
            pref = "gl" if host == "gitlab.com" else f"gl@{host}"
            d = _code_host(pref, "/".join(proj[:-1]), proj[-1], rest)
            return done("code", **d)
        return done("code")
    if host == "sourceforge.net" and len(segs) >= 2 and segs[0] in ("projects", "p"):
        return done("code", target=f"sf:{segs[1].lower()}")
    if host.endswith(".sourceforge.net") or host.endswith(".sourceforge.io"):
        return done("code", target=f"sf:{host.split('.')[0]}")
    if host == "launchpad.net" and segs:
        return done("code", target=f"lp:{segs[0].lower()}")
    if host == "savannah.gnu.org" and len(segs) >= 2 and segs[0] == "projects":
        return done("code", target=f"savannah:{segs[1].lower()}")

    # --- 패키지 등록소
    if host in ("pypi.org", "pypi.python.org") and len(segs) >= 2 and segs[0] in ("project", "pypi"):
        return done("registry", target=f"pypi:{_pep503(segs[1])}", edition=segs[2] if len(segs) > 2 and segs[2] != "#history" else None)
    if host in ("npmjs.com", "npmjs.org") and len(segs) >= 2 and segs[0] == "package":
        name = segs[1]
        rest = segs[2:]
        if name.startswith("@") and rest:
            name, rest = f"{name}/{rest[0]}", rest[1:]
        ed = rest[1] if rest[:1] == ["v"] and len(rest) > 1 else None
        return done("registry", target=f"npm:{name.lower()}", edition=ed)
    if host == "registry.npmjs.org" and segs:
        name = segs[0] if not segs[0].startswith("@") or len(segs) < 2 else f"{segs[0]}/{segs[1]}"
        return done("api", target=f"npm:{unquote(name).lower()}", page=f"npmapi:{'/'.join(segs).lower()}")
    if host == "crates.io" and len(segs) >= 2 and segs[0] == "crates":
        return done("registry", target=f"crates:{segs[1].lower().replace('_', '-')}", edition=segs[2] if len(segs) > 2 else None)
    if host == "docs.rs" and segs and segs[0] not in ("crate", "releases", "about"):
        name = segs[0]
        ed = segs[1] if len(segs) > 1 else None
        return done("docs", target=f"crates:{name.lower().replace('_', '-')}", page=f"docsrs:{name.lower()}/{'/'.join(segs[2:])}".rstrip("/"), edition=ed)
    if host == "pkg.go.dev" and segs:
        mod = "/".join(segs)
        ed = None
        if "@" in mod:
            mod, _, ed = mod.partition("@")
            ed = ed.split("/")[0]
        return done("registry", target=f"go:{mod.lower()}", edition=ed)
    if host == "rubygems.org" and len(segs) >= 2 and segs[0] == "gems":
        return done("registry", target=f"gem:{segs[1].lower()}", edition=segs[3] if len(segs) > 3 and segs[2] == "versions" else None)
    if host == "packagist.org" and len(segs) >= 3 and segs[0] == "packages":
        return done("registry", target=f"composer:{segs[1].lower()}/{segs[2].lower()}")
    if host == "nuget.org" and len(segs) >= 2 and segs[0] == "packages":
        return done("registry", target=f"nuget:{segs[1].lower()}", edition=segs[2] if len(segs) > 2 else None)
    if host in ("cran.r-project.org", "cloud.r-project.org"):
        name = None
        if len(segs) >= 3 and segs[:2] == ["web", "packages"]:
            name = segs[2]
        elif segs and segs[0].startswith("package="):
            name = segs[0].split("=", 1)[1]
        elif "package" in q:
            name = q["package"]
        if name:
            return done("registry", target=f"cran:{name}")
    if host == "bioconductor.org" and "packages" in segs and segs[-1] != "packages":
        name = re.sub(r"(_[\d.]+)?\.(html|tar\.gz|tgz|zip)$", "", segs[-1])
        return done("registry", target=f"bioc:{name}")
    if host == "hackage.haskell.org" and len(segs) >= 2 and segs[0] == "package":
        m = re.match(r"^(.*?)-(\d[\d.]*)$", segs[1])
        name, ed = (m.group(1), m.group(2)) if m else (segs[1], None)
        return done("registry", target=f"hackage:{name.lower()}", edition=ed)
    if host == "metacpan.org" and len(segs) >= 2 and segs[0] in ("pod", "dist", "release", "module"):
        return done("registry", target=f"cpan:{segs[-1] if segs[0] != 'release' else segs[-1]}")
    if host == "pub.dev" and len(segs) >= 2 and segs[0] == "packages":
        return done("registry", target=f"pub:{segs[1].lower()}")
    if host in ("mvnrepository.com",) and len(segs) >= 3 and segs[0] == "artifact":
        return done("registry", target=f"maven:{segs[1]}:{segs[2]}", edition=segs[3] if len(segs) > 3 else None)
    if host in ("central.sonatype.com", "search.maven.org") and len(segs) >= 3 and segs[0] == "artifact":
        return done("registry", target=f"maven:{segs[1]}:{segs[2]}", edition=segs[3] if len(segs) > 3 else None)
    if host == "hex.pm" and len(segs) >= 2 and segs[0] == "packages":
        return done("registry", target=f"hex:{segs[1].lower()}")
    if host == "anaconda.org" and len(segs) >= 2:
        return done("registry", target=f"conda:{segs[0].lower()}/{segs[1].lower()}")
    if host == "luarocks.org" and len(segs) >= 3 and segs[0] == "modules":
        return done("registry", target=f"luarocks:{segs[2].lower()}")
    if host == "opam.ocaml.org" and len(segs) >= 2 and segs[0] == "packages":
        return done("registry", target=f"opam:{segs[1].split('.')[0].lower()}")
    if (host == "juliahub.com" and "Packages" in "/".join(segs)) or host == "juliapackages.com":
        name = segs[-1] if segs else None
        if name:
            return done("registry", target=f"julia:{name.lower()}")
    if host == "marketplace.visualstudio.com" and "itemName" in q:
        return done("registry", target=f"vscode:{q['itemName'].lower()}")
    if host == "addons.mozilla.org" and "addon" in segs:
        i = segs.index("addon")
        if i + 1 < len(segs):
            return done("registry", target=f"amo:{segs[i + 1].lower()}")
    if host == "chromewebstore.google.com" and len(segs) >= 3 and segs[0] == "detail":
        return done("registry", target=f"cws:{segs[2]}")
    if host == "chrome.google.com" and "detail" in segs:
        return done("registry", target=f"cws:{segs[-1]}")
    if host == "apps.apple.com":
        m = re.search(r"id(\d+)", path)
        if m:
            return done("registry", target=f"appstore:{m.group(1)}")
    if host == "play.google.com" and "id" in q:
        return done("registry", target=f"gplay:{q['id']}")
    if host == "hub.docker.com":
        if len(segs) >= 2 and segs[0] == "_":
            return done("registry", target=f"docker:library/{segs[1].lower()}")
        if len(segs) >= 3 and segs[0] in ("r", "repository"):
            name = "/".join(segs[1:3]) if segs[0] == "r" else "/".join(segs[2:4])
            return done("registry", target=f"docker:{name.lower()}")

    # --- 논문·식별자
    if host in ("arxiv.org", "export.arxiv.org") and len(segs) >= 2 and segs[0] in ("abs", "pdf", "html", "format"):
        ident = "/".join(segs[1:])
        ident = re.sub(r"\.pdf$", "", ident)
        m = re.match(r"^((?:[a-z-]+(?:\.[A-Z]{2})?/)?\d{4,7}(?:\.\d{4,5})?)(v\d+)?$", ident)
        if m:
            return done("paper", target=f"arxiv:{m.group(1)}", edition=m.group(2))
    if host in ("doi.org", "dx.doi.org") and segs:
        return done("paper", target="doi:" + unquote("/".join(segs)).lower())
    m = re.match(r"^/(?:doi/(?:abs/|full/|pdf/|epdf/|book/)?|article/|chapter/)(10\.\d{4,9}/.+)$", path)
    if m and host in ("dl.acm.org", "link.springer.com", "onlinelibrary.wiley.com", "tandfonline.com",
                      "journals.sagepub.com", "pubs.acs.org", "science.org", "journals.plos.org", "academic.oup.com"):
        return done("paper", target="doi:" + unquote(m.group(1)).lower().rstrip("/"))
    if host == "ieeexplore.ieee.org" and len(segs) >= 2 and segs[0] in ("document", "abstract"):
        return done("paper", target=f"ieee:{segs[1]}")
    if host == "aclanthology.org" and segs:
        ident = re.sub(r"\.(pdf|bib)$", "", segs[0])
        return done("paper", target=f"acl:{ident.lower()}")
    if host == "openreview.net" and "id" in q:
        return done("paper", target=f"openreview:{q['id']}")
    if host == "zenodo.org" and len(segs) >= 2 and segs[0] in ("record", "records"):
        return done("dataset", target=f"zenodo:{segs[1]}")
    if host == "semanticscholar.org" and len(segs) >= 2 and segs[0] == "paper":
        return done("paper", target=f"s2:{segs[-1].lower()}")
    if host == "rfc-editor.org" or host == "datatracker.ietf.org" or host == "tools.ietf.org":
        m = re.search(r"rfc(\d+)", path, re.I)
        if m:
            return done("spec", target=f"rfc:{int(m.group(1))}")
        m = re.search(r"(draft-[a-z0-9-]+?)(?:-(\d\d))?(?:\.txt|\.html)?$", path)
        if m:
            return done("spec", target=f"ietf:{m.group(1)}", edition=m.group(2))
    if host == "peps.python.org" and segs:
        m = re.match(r"pep-(\d+)", segs[0])
        if m:
            return done("spec", target=f"pep:{int(m.group(1))}")
    if host == "w3.org" and len(segs) >= 2 and segs[0] == "TR":
        name = segs[1]
        m = re.match(r"^\d{4}/[A-Z]+-(.+?)-\d{8}$", "/".join(segs[1:3]))
        if m:
            name = m.group(1)
        return done("spec", target=f"w3c:{name.lower()}")

    # --- 백과·영상·토론
    if host.endswith("wikipedia.org"):
        lang = host.split(".")[0]
        title = None
        if len(segs) >= 2 and segs[0] == "wiki":
            title = "/".join(segs[1:])
        elif "title" in q:
            title = q["title"]
        if title:
            title = unquote(title).replace(" ", "_")
            title = title[:1].upper() + title[1:]
            return done("wiki", target=f"wp:{lang}:{title}", edition=q.get("oldid"))
    if host == "youtube.com":
        vid = q.get("v")
        if not vid and len(segs) >= 2 and segs[0] in ("shorts", "embed", "live", "v"):
            vid = segs[1]
        if vid:
            return done("video", target=f"yt:{vid}")
        if "list" in q:
            return done("video", target=f"ytlist:{q['list']}")
    if host == "youtu.be" and segs:
        return done("video", target=f"yt:{segs[0]}")
    if host == "vimeo.com" and segs and segs[0].isdigit():
        return done("video", target=f"vimeo:{segs[0]}")
    if host == "speakerdeck.com" and len(segs) >= 2:
        return done("slides", target=f"speakerdeck:{segs[0].lower()}/{segs[1].lower()}")
    if host == "slideshare.net" and len(segs) >= 2:
        return done("slides", target=f"slideshare:{'/'.join(segs[-2:]).lower()}")
    if host in SE_SITES or host.endswith(".stackexchange.com"):
        site = host.replace(".stackexchange.com", "").replace(".com", "")
        if len(segs) >= 2 and segs[0] in ("questions", "q") and segs[1].isdigit():
            return done("forum", target=f"se:{site}:q{segs[1]}")
        if len(segs) >= 2 and segs[0] == "a" and segs[1].isdigit():
            return done("forum", target=f"se:{site}:a{segs[1]}")
    if host == "news.ycombinator.com" and "id" in q:
        return done("forum", target=f"hn:{q['id']}")
    if host == "reddit.com" and len(segs) >= 4 and segs[0] == "r" and segs[2] == "comments":
        return done("forum", target=f"reddit:{segs[3].lower()}")
    if host == "redd.it" and segs:
        return done("forum", target=f"reddit:{segs[0].lower()}")
    if host == "lobste.rs" and len(segs) >= 2 and segs[0] == "s":
        return done("forum", target=f"lobsters:{segs[1]}")
    if host in ("twitter.com", "x.com") and len(segs) >= 3 and segs[1] == "status":
        return done("social", target=f"x:{segs[2]}")
    if host == "news.hada.io" and "id" in q:
        return done("forum", target=f"geeknews:{q['id']}")
    if host == "qiita.com" and len(segs) >= 3 and segs[1] == "items":
        return done("blog", target=f"qiita:{segs[2].lower()}")
    if host == "zenn.dev" and len(segs) >= 3 and segs[1] in ("articles", "books", "scraps"):
        return done("blog", target=f"zenn:{segs[0].lower()}/{segs[1]}/{segs[2].lower()}")
    if host == "note.com" and len(segs) >= 3 and segs[1] == "n":
        return done("blog", target=f"note:{segs[2].lower()}")
    if host == "velog.io" and len(segs) >= 2 and segs[0].startswith("@"):
        return done("blog", target=f"velog:{segs[0][1:].lower()}/{unquote(segs[1])}")
    if host == "habr.com":
        for s in segs:
            if s.isdigit():
                return done("blog", target=f"habr:{s}")
    if host == "medium.com" or host.endswith(".medium.com"):
        m = re.search(r"-([0-9a-f]{10,12})$", segs[-1]) if segs else None
        if m:
            return done("blog", target=f"medium:{m.group(1)}")
    if host == "dev.to" and len(segs) >= 2:
        return done("blog", target=f"devto:{segs[0].lower()}/{segs[1].lower()}")
    if host == "juejin.cn" and len(segs) >= 2 and segs[0] == "post":
        return done("blog", target=f"juejin:{segs[1]}")
    if host == "blog.csdn.net" and "details" in segs:
        return done("blog", target=f"csdn:{segs[-1]}")
    if host == "zhuanlan.zhihu.com" and len(segs) >= 2 and segs[0] == "p":
        return done("blog", target=f"zhihu:p{segs[1]}")
    if host == "v2ex.com" and len(segs) >= 2 and segs[0] == "t":
        return done("forum", target=f"v2ex:{segs[1]}")
    return res


CODE_FILE_HOSTS = {"github.com", "raw.githubusercontent.com", "gitlab.com", "codeberg.org", "gitee.com", "bitbucket.org", "git.sr.ht"}
GITLAB_HOSTS = {
    "gitlab.gnome.org", "salsa.debian.org", "invent.kde.org", "gitlab.freedesktop.org", "framagit.org",
    "gitlab.archlinux.org", "code.videolan.org", "gitlab.torproject.org", "gitlab.inria.fr", "git.gnome.org",
    "gitlab.haskell.org", "gitlab.alpinelinux.org", "foss.heptapod.net", "gitlab.xfce.org", "0xacab.org",
}
SE_SITES = {"stackoverflow.com", "superuser.com", "serverfault.com", "askubuntu.com", "mathoverflow.net", "ja.stackoverflow.com", "ru.stackoverflow.com", "pt.stackoverflow.com", "es.stackoverflow.com"}


def _is_local_or_placeholder(host: str) -> bool:
    h = host.strip("[]")
    if h in ("localhost", "example.com", "example.org", "example.net") or h.endswith((".localhost", ".local", ".internal", ".example", ".test", ".invalid", ".example.com")):
        return True
    try:
        ip = ipaddress.ip_address(h)
        return ip.is_private or ip.is_loopback or ip.is_unspecified or ip.is_link_local
    except ValueError:
        return "." not in h


GH_NAME = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")
GH_REPO = re.compile(r"^[A-Za-z0-9._-]{1,100}$")


def syntax_flags(n: dict) -> list:
    """접속하기 전에 볼 수 있는 의심 표시. 지어낸 주소에 흔한 모양을 잡는다."""
    flags = []
    raw = n.get("raw") or ""
    if re.search(r"\.\.\.|<[a-z_]+>|\{[a-z_]+\}|YOUR_|xxx|placeholder", raw, re.I):
        flags.append("placeholder")
    t = n.get("target") or ""
    if t.startswith("gh:"):
        parts = t[3:].split("/")
        if not GH_NAME.match(parts[0]) or (len(parts) > 1 and not GH_REPO.match(parts[1])):
            flags.append("gh_name_invalid")
    if t.startswith("arxiv:"):
        m = re.match(r"^arxiv:(\d{2})(\d{2})\.\d{4,5}$", t)
        if m and not (1 <= int(m.group(2)) <= 12):
            flags.append("arxiv_month_invalid")
    if t.startswith("doi:") and not re.match(r"^doi:10\.\d{4,9}/\S+$", t):
        flags.append("doi_invalid")
    if re.search(r"/blob/[^/]+$|/tree/[^/]+/?$", n.get("url_norm") or "") and t.startswith("gh:"):
        pass  # 브랜치 첫 화면. 의심은 아니다
    return flags


# ---------------------------------------------------------------- 입구

def normalize(url: str) -> dict:
    """주소 하나를 정규화한다.

    돌려주는 사전: raw, url_norm, page, target, edition, position, host, host_kind, notes, rules
    원문이 아닌 주소(검색 결과, 대화 공유)는 NotASource를 낸다. 주소가 아니면 ValueError.
    """
    raw = url
    s = clean_raw(url)
    notes = []
    if s != (url or "").strip():
        notes.append("cleaned")
    s, extra = _unwrap(s)
    if extra:
        notes.extend(f"{k}={v}" for k, v in sorted(extra.items()))
    p = urlsplit(s)
    scheme = p.scheme.lower()
    if scheme not in ("http", "https", "ftp"):
        raise ValueError(f"주소가 아님: {raw!r}")
    host, netloc = _host(p.netloc)
    if not host or "." not in host and not host.startswith("["):
        raise ValueError(f"호스트 없음: {raw!r}")
    bh = bare_host(host)
    netloc = netloc.replace(host, bh, 1)
    if _is_local_or_placeholder(bh):
        raise NotASource(f"로컬·예시 주소: {raw!r}")
    for hre, pre in NOT_SOURCE:
        if hre.match(bh) and pre.match(p.path or "/"):
            raise NotASource(f"원문이 아닌 주소: {raw!r}")
    path = _norm_path(p.path or "/", keep_index=bh in CODE_FILE_HOSTS)
    query = _norm_query(p.query, bh)
    frag = p.fragment
    keep_frag = frag.startswith("/") or frag.startswith("!")
    position = None if keep_frag else (unquote(frag) or None)
    if bh in ("github.com", "gitlab.com", "codeberg.org", "gitee.com"):
        # 저장소 경로는 대소문자를 가리지 않으므로 owner/repo만 소문자로
        segs = path.split("/")
        if len(segs) >= 3 and segs[1].lower() not in GH_RESERVED:
            segs[1], segs[2] = segs[1].lower(), segs[2].lower()
            if segs[2].endswith(".git"):
                segs[2] = segs[2][:-4]
            path = "/".join(segs)
    url_norm = f"{'https' if scheme in ('http', 'https') else scheme}://{netloc}{path if path != '/' else ''}"
    if query:
        url_norm += "?" + query
    if keep_frag:
        url_norm += "#" + frag
    t = target_of(bh, path, query)
    page = t.get("page") or url_norm.split("://", 1)[1]
    pos = t.get("position")
    if position:
        pos = f"{pos}#{position}" if pos else f"#{position}"
    edition = t.get("edition") or None
    if extra.get("archive"):
        edition = f"{edition}@{extra['archive']}" if edition else extra["archive"]
    return {
        "raw": raw,
        "url_norm": url_norm,
        "page": page,
        "target": t.get("target"),
        "edition": edition,
        "position": pos,
        "host": bh,
        "host_kind": t.get("host_kind", "web"),
        "notes": notes,
        "rules": RULES_VERSION,
    }


def safe_normalize(url: str) -> dict:
    """실패해도 예외를 내지 않는다. error 칸에 이유를 남긴다."""
    try:
        return normalize(url)
    except NotASource as e:
        return {"raw": url, "error": "not_source", "detail": str(e)}
    except Exception as e:  # noqa: BLE001 - 병합은 한 줄 실패로 멈추지 않는다
        return {"raw": url, "error": "invalid", "detail": f"{type(e).__name__}: {e}"}


if __name__ == "__main__":
    import json
    import sys

    for line in (sys.argv[1:] or sys.stdin):
        line = line.strip()
        if line:
            print(json.dumps(safe_normalize(line), ensure_ascii=False))
