"""AF-RES-039 single-packet, read-only public document GET consumer."""
import argparse
import hashlib
import ipaddress
import json
import re
import subprocess
import tarfile
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urldefrag, urljoin, urlsplit, urlunsplit, urlencode

VERSION = "1.0"
REDIRECTS = {301, 302, 303, 307, 308}
DEADLINE_SECONDS = 30
MAX_LOGICAL_GETS = 2
WINDOW_SIZE = 900
INPUT_NAME = "store.json"
C1 = "C1_B_presealed"
C2 = "C2_BH_with_provenance"
BASE_FIELDS = {"B", "B_sha256", "configuration", "ref_id"}
HISTORY_FIELDS = {
    "H", "H_sha256", "H_source_ids", "H_spans", "historical_retrieval_units",
    "acquisition_utc_is_not_event_date", "preserves_full_archive",
}


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def audit_url(url):
    """Avoid retaining credential-like redirect query values in a public log."""
    parts = urlsplit(url)
    sensitive = re.compile(r"(^_|signature|token|credential|^key$|^code$|x-amz|x-goog)", re.I)
    if not any(sensitive.search(key) for key, _ in parse_qsl(parts.query)):
        return url
    query = urlencode([
        (key, "[redacted]" if sensitive.search(key) else value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
    ])
    return urlunsplit(parts._replace(query=query))


def public_url(url):
    parts = urlsplit(url)
    if parts.scheme not in {"http", "https"} or not parts.hostname or parts.username or parts.password:
        return False
    if "." not in parts.hostname or parts.hostname.endswith((".local", ".internal", ".localhost")):
        return False
    try:
        return ipaddress.ip_address(parts.hostname).is_global
    except ValueError:
        return True


def read_packet(path):
    pre_read = sorted(item.name for item in Path.cwd().iterdir())
    data = path.read_bytes()
    packet = json.loads(data)
    config = packet["configuration"]
    if config not in {C1, C2}:
        raise ValueError("Unexpected storage configuration")
    expected = BASE_FIELDS | (HISTORY_FIELDS if config == C2 else set())
    if set(packet) != expected or sha(packet["B"].encode()) != packet["B_sha256"]:
        raise ValueError("Unexpected fields or B hash mismatch")
    if config == C2 and sha(packet["H"].encode()) != packet["H_sha256"]:
        raise ValueError("H hash mismatch")
    introduction, _, context = packet["B"].partition("\n\nOriginal context:\n")
    cite = dict(line.split(": ", 1) for line in introduction.splitlines()[1:])
    return packet, cite, context, {
        "input_sha256": sha(data), "input_bytes": len(data), "input_fields": sorted(packet),
        "cwd_before_read": pre_read, "B_sha256": packet["B_sha256"],
        "B_bytes": len(packet["B"].encode()),
    }


def parse_headers(data):
    blocks = []
    for block in re.split(r"\r?\n\r?\n", data):
        lines = block.splitlines()
        match = re.match(r"HTTP/\S+\s+(\d{3})\s*(.*)", lines[0]) if lines else None
        if match:
            fields = {}
            for line in lines[1:]:
                if ":" in line:
                    key, value = line.split(":", 1)
                    fields[key.lower()] = value.strip()
            blocks.append((int(match[1]), match[2], fields))
    return blocks


def exchange(url, prefix, remaining):
    body = prefix.with_suffix(".body")
    headers = prefix.with_suffix(".headers")
    args = [
        "curl", "--disable", "--silent", "--show-error", "--verbose", "--max-time", str(remaining),
        "--proto", "=http,https", "--request", "GET",
        "--header", "Accept-Encoding: identity", "--header", "Cache-Control: no-cache",
        "--output", str(body), "--dump-header", str(headers), "--write-out", "%{json}", "--",
        urldefrag(url)[0],
    ]
    started_at, started = utc(), time.monotonic()
    try:
        command = subprocess.run(args, capture_output=True, timeout=remaining, check=False)
        exit_code, stdout, stderr = command.returncode, command.stdout, command.stderr
    except subprocess.TimeoutExpired as error:
        exit_code, stdout, stderr = 28, error.stdout or b"", error.stderr or b""
    try:
        metrics = json.loads(stdout)
    except (ValueError, UnicodeDecodeError):
        metrics = {}
    chain = parse_headers(headers.read_text(encoding="iso-8859-1") if headers.exists() else "")
    connect_status = metrics.get("http_connect") or None
    status = metrics.get("response_code") or None
    sent_get = bool(re.search(rb"(?m)^> GET ", stderr))
    tls_connect_ok = bool(chain and chain[0][1].lower() == "connection established")
    if not status and sent_get and chain and not (len(chain) == 1 and tls_connect_ok):
        status = chain[-1][0]
    last_headers = chain[-1][2] if chain and (sent_get or status) else {}
    if exit_code == 28:
        error_code = "TIMEOUT"
    elif connect_status and connect_status != 200:
        error_code = "PROXY_CONNECT_DENIED"
    elif exit_code:
        error_code = "TRANSPORT_ERROR"
    elif status and status >= 400:
        error_code = "HTTP_ERROR"
    else:
        error_code = None
    body_data = body.read_bytes() if body.exists() else b""
    redir = last_headers.get("location")
    public_headers = {
        key: last_headers[key] for key in (
            "date", "age", "cache-control", "cache-status", "x-cache", "via", "etag",
            "last-modified", "content-length", "content-encoding", "content-type",
        ) if key in last_headers
    }
    safe_error = re.sub(r"https?://\S+", "[url]", metrics.get("errormsg") or "")
    return {
        "requested_url": audit_url(url),
        "started_utc": started_at, "finished_utc": utc(),
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "status": status, "status_blocks": [status for status, _, _ in chain],
        "proxy_connect_status": connect_status or (200 if tls_connect_ok else None),
        "proxy_connect_attempted": bool(re.search(rb"(?m)^> CONNECT ", stderr)) or bool(connect_status),
        "http_get_sent": sent_get,
        "http_exchange": bool(status and (sent_get or status != connect_status)),
        "curl_exit_code": exit_code, "error": error_code, "curl_error": safe_error[:160] or None,
        "response_headers": public_headers, "curl_version": metrics.get("curl_version"),
        "received_body_bytes": len(body_data), "curl_size_download": metrics.get("size_download"),
        "body_sha256": sha(body_data) if body.exists() else None,
        "body_file": str(body) if body.exists() else None,
        "location": audit_url(urljoin(url, redir)) if redir else None,
    }, redir


def get(url, logical_id, purpose):
    began, started = utc(), time.monotonic()
    request = {"logical": logical_id, "purpose": purpose, "initial_url": audit_url(url), "exchanges": []}
    seen = set()
    physical_id = 0
    error = None
    while True:
        remaining = DEADLINE_SECONDS - (time.monotonic() - started)
        if remaining <= 0:
            error = "TIMEOUT"
            break
        if not public_url(url):
            error = "NON_PUBLIC_LOCATOR"
            break
        transport_url = urldefrag(url)[0]
        if transport_url in seen:
            error = "REDIRECT_LOOP"
            break
        seen.add(transport_url)
        physical_id += 1
        prefix = Path("received") / f"{logical_id}-{physical_id}"
        result, location = exchange(url, prefix, remaining)
        request["exchanges"].append(result)
        if result["error"] or result["status"] not in REDIRECTS:
            error = result["error"]
            break
        if location is None:
            error = "REDIRECT_WITHOUT_LOCATION"
            break
        next_url = urljoin(url, location)
        if "#" not in location and urlsplit(url).fragment:
            next_url += "#" + urlsplit(url).fragment
        url = next_url
    last = request["exchanges"][-1] if request["exchanges"] else {}
    response_ok = not error and last.get("status") == 200
    if not error and not response_ok:
        error = "UNEXPECTED_STATUS"
    request.update(
        started_utc=began, finished_utc=utc(), elapsed_seconds=round(time.monotonic() - started, 6),
        error=error, final_url=audit_url(url),
        final_status=last.get("status"), accepted_body=last.get("body_file") if response_ok else None,
        http_exchanges=sum(item["http_exchange"] for item in request["exchanges"]),
    )
    return request, url


class Document(HTMLParser):
    """Visible text, named positions and links from any received HTML."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.positions = {}
        self.links = []
        self.hidden = 0
        self.active_link = None
        self.title = []
        self.in_title = False

    def handle_starttag(self, tag, attributes):
        fields = dict(attributes)
        if tag in {"script", "style", "template"}:
            self.hidden += 1
        if self.hidden:
            return
        if tag == "title":
            self.in_title = True
        for name in ("id", "name") if tag == "a" else ("id",):
            if fields.get(name):
                self.positions[fields[name]] = len(self.text)
        if tag == "a" and fields.get("href"):
            self.active_link = (fields["href"], len(self.text))

    def handle_endtag(self, tag):
        if tag in {"script", "style", "template"} and self.hidden:
            self.hidden -= 1
        if tag == "title":
            self.in_title = False
        if tag == "a" and self.active_link:
            href, start = self.active_link
            self.links.append((href, " ".join(self.text[start:])))
            self.active_link = None

    def handle_data(self, data):
        if self.hidden:
            return
        cleaned = " ".join(data.split())
        if cleaned:
            self.text.append(cleaned)
            if self.in_title:
                self.title.append(cleaned)


def html_document(data):
    result = Document()
    result.feed(data.decode("utf-8", errors="replace"))
    return result


def marker_terms(cite, context):
    purpose = cite["Presealed minimum purpose (collector paraphrase)"]
    markers = set(re.findall(r"(?<!\w)-[A-Z]\w*|[a-zA-Z][a-zA-Z0-9_-]{2,}", purpose))
    markers |= set(re.findall(r"\b(?:[a-z]+[A-Z]\w+|[A-Z]{2,})\b", context))
    return sorted(
        markers - {"GNU", "Bash", "GNU/Unix/Linux", "man", "page", "SEE", "ALSO", "Preface", "FAQ"},
        key=lambda term: (-len(term), term),
    )


def classify_document(doc, url, cite, context):
    fragment = unquote(urlsplit(url).fragment)
    text = " ".join(doc.text)
    terms = marker_terms(cite, context)
    purpose = cite["Presealed minimum purpose (collector paraphrase)"]
    explicit_standard_year = re.search(r"\b(19\d{2}|20\d{2})\s+POSIX", purpose)
    if fragment and fragment not in doc.positions:
        return {"qualified": False, "reason": "WRONG_OR_MISSING_ANCHOR", "locator": fragment}, terms
    if explicit_standard_year and explicit_standard_year[1] not in text:
        return {"qualified": False, "reason": "EDITION_UNCONFIRMED", "locator": fragment or None}, terms
    # Source editions and destination editions are different. A year is required
    # only if the citation purpose itself explicitly identifies the standard year.
    expected_release = re.search(r"/packages/(\d+\.\d+)(?:/|$)", cite["Original href"])
    delivered_release = re.search(r"/packages/(\d+\.\d+)(?:/|$)", url)
    if expected_release and (not delivered_release or delivered_release[1] != expected_release[1]):
        return {"qualified": False, "reason": "EDITION_UNCONFIRMED", "locator": fragment or None}, terms
    if fragment:
        index = doc.positions[fragment]
        relevant = " ".join(doc.text[index:max(index + 1, index + 120)])
    else:
        relevant = text
    matches = [term for term in terms if re.search(r"(?<![\w-])" + re.escape(term) + r"(?![\w-])",
                                                  relevant, re.I)]
    # A repository/archive index can be an intended endpoint. It must actually
    # list artifacts and contain the citation term, like a prose section must.
    distribution_index = any(
        re.search(r"[-_]\d+\.\d+.*\.(?:tar\.(?:gz|xz|bz2)|zip)(?:$|\?)", href)
        for href, _ in doc.links
    ) and bool(re.search(r"\b(?:source|release|newest)\b", purpose + " " + context, re.I))
    required_phrase = re.search(r"\b(?:Part|Volume) [A-Z0-9]+: ([A-Z][^,.\n]+)", context)
    if required_phrase and required_phrase[1].casefold() not in relevant.casefold():
        return {"qualified": False, "reason": "NEEDED_PART_UNCONFIRMED",
                "locator": fragment or None}, terms
    lower_text = relevant.casefold()
    positions = [lower_text.find(term.casefold()) for term in matches]
    start = max(0, min((position for position in positions if position >= 0), default=0) - 100)
    window = relevant[start:start + WINDOW_SIZE]
    qualified = (distribution_index and len(relevant) >= 100) or (
        len(relevant) >= 180 and len(matches) >= min(2, max(1, len(terms)))
        and (len(terms) > 1 or len(matches) == 1 and relevant.casefold().count(matches[0].casefold()) >= 3)
    )
    return {
        "qualified": qualified,
        "reason": None if qualified else "NEEDED_SECTION_UNCONFIRMED",
        "locator": fragment or "document text",
        "title": " ".join(doc.title)[:200], "marker_hits": matches,
        "visible_chars": len(relevant), "witness_sha256": sha(window.encode()),
    }, terms


def publisher_index(url):
    parts = urlsplit(url)
    stem = parts.path.rstrip("/")
    bio = re.fullmatch(r"/packages/(\d+\.\d+)/([A-Za-z][A-Za-z0-9.]*)", stem)
    if bio:
        index = f"/packages/{bio[1]}/bioc/src/contrib/Archive/{bio[2]}/"
    elif parts.hostname == "github.com" and stem.count("/") == 2:
        index = stem + "/tags"
    elif stem.endswith((".html", ".htm")):
        index = stem.rsplit("/", 1)[0] + "/"
    elif stem:
        index = stem + "/" if stem.count("/") <= 1 else stem.rsplit("/", 1)[0] + "/"
    else:
        return None
    return urlunsplit((parts.scheme, parts.netloc, index, "", ""))


def pick_link(doc, origin, cite, terms, history):
    if not doc:
        return None
    source = urlsplit(origin)
    link_text = cite["Link text"].casefold()
    keywords = {term.casefold() for term in terms if len(term) > 3}
    if not link_text.startswith(("https://", "http://")):
        keywords.add(link_text)
    ranked = []
    for ordinal, (href, label) in enumerate(doc.links):
        candidate = urljoin(origin, href)
        parts = urlsplit(candidate)
        # Preserve the original publication namespace, allowing publisher subhosts.
        home = source.hostname.removeprefix("www.")
        host = (parts.hostname or "").removeprefix("www.")
        if not public_url(candidate) or (host != home and not host.endswith("." + home)):
            continue
        if urldefrag(candidate)[0] == urldefrag(origin)[0]:
            continue
        target = unquote(parts.path + " " + label).casefold()
        if re.search(r"\b(?:login|subscribe|sign.in|privacy|license|issues|login)\b", target):
            continue
        score = sum(term in target for term in keywords)
        archive_hint = bool(re.search(r"(archive|older|release|\btags\b|previous|\.tar\.)", target))
        if history:
            score += 4 * archive_hint
            score -= 3 * ("latest" in target or "/main/" in target)
        else:
            score += 2 * bool(re.search(r"(reference.manual|documentation|user.guide|\.pdf|vignette)", target))
            score -= 2 * archive_hint
        if score >= 2:
            ranked.append((-score, ordinal, candidate))
    return min(ranked)[2] if ranked else None


def historical_sites(packet):
    if packet["configuration"] == C1:
        return []
    meta, separator, _ = packet["H"].partition("\n\nPublisher excerpt(s):")
    if not separator:
        raise ValueError("H has no publisher-excerpt delimiter")
    return json.loads(meta)["publisher_documents"]


def receipt_for_member(archive_body, history_site):
    member = history_site.get("member")
    if member is None and "GNU info" in history_site["edition_or_document"]:
        match = re.search(r"/(([a-z][a-z0-9_-]*)-[\d.]+)\.tar\.", history_site["url"])
        if match:
            member = f"{match[1]}/doc/{match[2]}.info"
    if member is None:
        return None, None
    try:
        with tarfile.open(archive_body) as archive:
            found = archive.getmember(member)
            if not found.isfile():
                return {"member": member, "error": "ARCHIVE_MEMBER_TYPE"}, None
            with archive.extractfile(found) as selected:
                body = selected.read()
    except KeyError:
        return {"member": member, "error": "ARCHIVE_MEMBER_MISSING"}, None
    except (tarfile.TarError, OSError, EOFError):
        return {"member": member, "error": "ARCHIVE_PARSE_ERROR"}, None
    return {"member": member, "member_sha256": sha(body), "member_bytes": len(body)}, body


def choose_second(task, first, final, doc, verdict, terms, cite, histories):
    origin = cite["Original href"]
    if first["error"] and urlsplit(origin).scheme == "http":
        return urlunsplit(urlsplit(origin)._replace(scheme="https")), "secure_original"
    if verdict.get("qualified"):
        if task == "current":
            return None, None
        if histories:
            return histories[0]["url"], "retained_historical_locator"
        return pick_link(doc, final, cite, terms, True) or publisher_index(final), "history_discovery"
    alternative = pick_link(doc, final, cite, terms, False)
    if alternative:
        return alternative, "published_candidate"
    release = re.search(r"/packages/(\d+\.\d+)(?:/|$)", origin)
    for site in histories:
        if release and f"/{release[1]}/" in site["url"] and cite["Link text"] in site["url"]:
            return site["url"], "same_edition_historical_locator"
    if task == "restore" and histories:
        return histories[0]["url"], "retained_historical_locator"
    return publisher_index(final), "publisher_index"


def as_document(data, file, member):
    if data.startswith(b"%PDF-") and not member:
        result = subprocess.run(["pdftotext", "-layout", str(file), "-"], capture_output=True, check=False)
        if result.returncode:
            return None, "PDF_TEXT_EXTRACTION_FAILED"
        data = result.stdout
    elif re.search(rb"<(?:!doctype|html|head|body|title|main|article)\b", data[:8192], re.I):
        return html_document(data), None
    elif b"\x00" in data[:8192]:
        return None, "NON_TEXT_BODY"
    doc = Document()
    doc.text = data.decode("utf-8", errors="replace").splitlines()
    return doc, None


def inspect_document(request, final, cite, context, history_site=None):
    if request["accepted_body"] is None:
        return None, {"qualified": False, "reason": request["error"]}, marker_terms(cite, context)
    file = Path(request["accepted_body"])
    member = None
    if history_site and ".tar." in urlsplit(final).path:
        receipt, data = receipt_for_member(file, history_site)
        if receipt is None:
            return None, {"qualified": False, "reason": "ARCHIVE_MEMBER_LOCATOR_MISSING"}, marker_terms(cite, context)
        request["archive_member"] = receipt
        member = receipt["member"]
        if receipt.get("error"):
            return None, {"qualified": False, "reason": receipt["error"], "locator": member}, marker_terms(cite, context)
    else:
        data = file.read_bytes()
    doc, error = as_document(data, file, member)
    if error:
        return None, {"qualified": False, "reason": error}, marker_terms(cite, context)
    verdict, terms = classify_document(doc, final, cite, context)
    if member:
        verdict["locator"] = member
    elif data.startswith(b"%PDF-"):
        verdict["locator"] = "PDF extracted text"
    return doc, verdict, terms


def run(task, path):
    started_utc, started = utc(), time.monotonic()
    packet, cite, context, boundary = read_packet(path)
    Path("received").mkdir()
    local_history = {
        "available_in_input": "H" in packet, "displayed": False, "read_bytes": 0,
        "H_bytes_validated_from_input": len(packet.get("H", "").encode()),
        "H_metadata_bytes_parsed": len(packet.get("H", "").partition("\n\nPublisher excerpt(s):")[0].encode()),
        "H_sha256": None, "integrity": None, "publisher_locator_used": False,
    }
    histories = historical_sites(packet)
    if task == "restore" and "H" in packet:
        text = packet["H"].encode()
        local_history.update(displayed=True, read_bytes=len(text), H_sha256=sha(text),
                             integrity="matches_packet")
        Path("received/local-H.txt").write_bytes(text)
    first, final = get(cite["Original href"], 1, "original")
    doc, verdict, terms = inspect_document(first, final, cite, context)
    first["section"] = verdict
    requests = [first]
    candidate, reason = choose_second(task, first, final, doc, verdict, terms, cite, histories)
    if candidate and public_url(candidate) and not any(
        urldefrag(candidate)[0] == urldefrag(url)[0] for url in (final, cite["Original href"])
    ):
        second, reached = get(candidate, 2, reason)
        history_site = next((site for site in histories if site["url"] == candidate), None)
        local_history["publisher_locator_used"] = history_site is not None
        _, second_verdict, _ = inspect_document(second, reached, cite, context, history_site)
        second["section"] = second_verdict
        requests.append(second)
    action = None
    if task == "current":
        action = "HOLD"
        if first["section"]["qualified"]:
            action = "KEEP"
        elif len(requests) == 2 and requests[1]["section"]["qualified"]:
            action = "KEEP" if reason == "secure_original" else "REPLACE"
    return {
        "runner_version": VERSION, "task": task, "ref_id": packet["ref_id"],
        "storage_configuration": packet["configuration"], **boundary,
        "started_utc": started_utc, "finished_utc": utc(),
        "wall_seconds": round(time.monotonic() - started, 6),
        "original_url": audit_url(cite["Original href"]), "requests": requests,
        "unrequested_second": "NO_DISTINCT_PUBLIC_CANDIDATE" if len(requests) == 1 and candidate else None,
        "logical_gets": len(requests), "http_exchanges": sum(item["http_exchanges"] for item in requests),
        "local_history": local_history, "provisional_action": action,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", choices=("current", "restore", "boundary"))
    parser.add_argument("--input", default=INPUT_NAME)
    args = parser.parse_args()
    input_file = Path(args.input)
    if args.task == "boundary":
        packet, cite, _, boundary = read_packet(input_file)
        output = {
            **boundary, "at_utc": utc(), "ref_id": packet["ref_id"],
            "storage_configuration": packet["configuration"], "original_href": cite["Original href"],
            "H_bytes": len(packet.get("H", "").encode()), "H_locators": len(historical_sites(packet)),
            "checked_fields": sorted(packet), "network_attempts": 0,
        }
    else:
        output = run(args.task, input_file)
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
