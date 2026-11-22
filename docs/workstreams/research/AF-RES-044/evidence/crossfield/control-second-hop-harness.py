"""Read-only C1/C2 second-hop probe. Temporary reading windows are not deliverables."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urljoin, urldefrag, urlsplit
import datetime
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE.parent
spec = importlib.util.spec_from_file_location("af044_http_probe", EVIDENCE / "http_probe.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


def save(name, value):
    (HERE / ("control-second-hop-" + name)).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    )


def get_document(url):
    row = {"document_url": url, "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urlopen(url, timeout=25) as response:
            raw = response.read()
            row.update(http_status=response.status, final_document_url=response.geturl(),
                       content_type=response.headers.get("content-type", ""), byte_count=len(raw))
        row["sha256"] = hashlib.sha256(raw).hexdigest()
        row["connectivity_success"] = True
        if "html" not in row["content_type"]:
            row["parse_status"] = "non-HTML; no semantic body review claimed"
            return row, None
        dom = probe.DOM()
        dom.feed(raw.decode("utf-8", errors="replace"))
        dom.finish()
        row["parse_status"] = "HTML parsed"
        return row, dom
    except Exception as exc:
        row.update(http_status=getattr(exc, "code", "failed"), connectivity_success=False,
                   error_type=type(exc).__name__, error=str(exc))
        return row, None


def main():
    frozen = json.loads((EVIDENCE / "control/candidate-read-receipts.json").read_text())
    candidates = []
    for row in frozen:
        if row["candidate_id"].startswith("C1-"):
            candidates.append({"candidate_id": row["candidate_id"], "case_id": "C1",
                               "url": row["requested_url"], "source_html_sha256": row.get("sha256"),
                               "source_status": row["status"], "scope": row["scope"],
                               "window_text_sha256": row["window_text_sha256"],
                               "outgoing_inventory_status": "unknown: source access failed" if row["status"] != 200 else
                                   "empty: target fragment absent" if row["scope"].get("fragment_found") is False else "observed",
                               "source_receipt_file": "evidence/control/candidate-read-receipts.json"})
    browser_file = EVIDENCE / "browser-observations.json"
    if browser_file.exists():
        br = json.loads(browser_file.read_text()).get("requests")
        if br and br.get("loaded") and br.get("fragment_exists"):
            for candidate in candidates:
                if candidate["candidate_id"] == "C1-4":
                    candidate["raw_http_scope_preserved"] = candidate["scope"]
                    candidate["source_browser_observation"] = br
                    candidate["outgoing_inventory_status"] = "observed browser-rendered section; original raw HTTP failure preserved"
                    candidate["scope"] = {"fragment": "prepared-requests", "fragment_found": True,
                                          "scope_locator": br["locator"], "links": br["outgoing_hrefs"]}
    c2 = json.loads((HERE / "control-C2.json").read_text())
    source_urls = sorted(set(urldefrag(s["url"])[0] for s in c2["slots"]))
    source_docs = dict(zip(source_urls, ThreadPoolExecutor(max_workers=5).map(get_document, source_urls)))
    source_windows = []
    for s in c2["slots"]:
        url = s["url"]
        access, dom = source_docs[urldefrag(url)[0]]
        window = dom.window(url) if dom else {"text": "", "links": [], "fragment_found": False}
        cid = "C2-" + str(s["slot"])
        source_windows.append({"candidate_id": cid, "url": url, "access": access, "window": window})
        candidates.append({"candidate_id": cid, "case_id": "C2", "url": url,
                           "source_html_sha256": access.get("sha256"), "source_status": access["http_status"],
                           "source_hash_matches_frozen": access.get("sha256") == s["sha256"],
                           "scope": {k: v for k, v in window.items() if k != "text"},
                           "window_word_count": len(window.get("text", "").split()),
                           "window_text_sha256": hashlib.sha256(window.get("text", "").encode()).hexdigest(),
                           "outgoing_inventory_status": "observed" if dom else "unknown: source access failed"})
    save("source-windows.tmp.json", source_windows)
    save("source-receipts.json", candidates)

    targets, excluded = {}, []
    for c in candidates:
        for link in c["scope"].get("links", []):
            url = urljoin(c["url"], link["raw_href"])
            occurrence = {"case_id": c["case_id"], "candidate_id": c["candidate_id"],
                          "source_url": c["url"], **link}
            if urlsplit(url).scheme not in ("http", "https"):
                excluded.append({"url": url, "reason": "non-HTTP scheme", "source_occurrence": occurrence})
                continue
            targets.setdefault(url, {"url": url, "source_occurrences": []})["source_occurrences"].append(occurrence)
    ordered = [targets[u] for u in sorted(targets)]
    documents = sorted(set(urldefrag(t["url"])[0] for t in ordered))
    save("targets.json", {"strict_outgoing_occurrences": sum(len(t["source_occurrences"]) for t in ordered),
                          "unique_url_count": len(ordered), "unique_document_count": len(documents),
                          "targets": ordered, "excluded_non_http": excluded,
                          "incomplete_source_candidates": [c["candidate_id"] for c in candidates
                                                           if c["outgoing_inventory_status"].startswith("unknown")]})
    print(json.dumps({"phase": "targets", "urls": len(ordered), "documents": len(documents)}), flush=True)

    # A unique document is fetched once; every fragment gets its own independent logical arrival.
    cache = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        for url, result in zip(documents, executor.map(get_document, documents)):
            cache[url] = result
    save("access.json", [cache[u][0] for u in documents])
    arrivals, reading = [], []
    for target in ordered:
        url = target["url"]
        access, dom = cache[urldefrag(url)[0]]
        window = dom.window(url) if dom else {"text": "", "links": [], "fragment_found": None}
        frag = urldefrag(url)[1]
        arrival = {**target, "http_status": access["http_status"],
                   "connectivity_success": access["connectivity_success"],
                   "final_document_url": access.get("final_document_url"),
                   "document_sha256": access.get("sha256"), "content_type": access.get("content_type"),
                   "checked_utc": access["checked_utc"], "fragment_exists": window.get("fragment_found") if frag else "not applicable",
                   "destination_section_confirmed": bool(dom) and (not frag or window.get("fragment_found") is True),
                   "scope_locator": window.get("scope_locator", "no HTML window"),
                   "window_word_count": len(window.get("text", "").split()),
                   "window_text_sha256": hashlib.sha256(window.get("text", "").encode()).hexdigest(),
                   "actual_user_response": "미확인", "document_fetch_reused_for_fragments": True}
        arrivals.append(arrival)
        reading.append({**arrival, "text": window.get("text", ""), "links": window.get("links", [])})
    save("arrivals.json", arrivals)
    save("reading.tmp.json", reading)
    print(json.dumps({"phase": "arrivals", "urls": len(arrivals), "documents": len(documents),
                      "http_success_documents": sum(x[0]["connectivity_success"] for x in cache.values()),
                      "resolved_url_sections": sum(x["destination_section_confirmed"] for x in arrivals)}), flush=True)


if __name__ == "__main__":
    main()
