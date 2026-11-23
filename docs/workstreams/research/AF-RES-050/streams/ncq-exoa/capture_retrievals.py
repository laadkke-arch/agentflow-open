"""Preserve retrieval receipts only; do not redistribute papers or participant records."""
import concurrent.futures
import datetime
import hashlib
import json
import urllib.request

URLS = {
    "NA-001": "https://brittany-reid.github.io/publication/reid-2023-ncq/reid-2023-ncq.pdf",
    "NA-002": "https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf",
    "NA-003": "https://raw.githubusercontent.com/Brittany-Reid/node_code_query/ce14f193f7014c120f04619826cb251818d99b0e/README.md",
    "NA-003-INSTRUCTIONS": "https://raw.githubusercontent.com/Brittany-Reid/node_code_query/ce14f193f7014c120f04619826cb251818d99b0e/docs/instructions.md",
    "NA-003-LOGGER": "https://raw.githubusercontent.com/Brittany-Reid/node_code_query/ce14f193f7014c120f04619826cb251818d99b0e/src/core/logger.js",
    "NA-003-LINT": "https://raw.githubusercontent.com/Brittany-Reid/node_code_query/ce14f193f7014c120f04619826cb251818d99b0e/data/scripts/user-study-snippets.js",
    "NA-004": "https://brittany-reid.github.io/publication/reid-2022-software/reid-2022-software.pdf",
    "NA-005": "https://raw.githubusercontent.com/Brittany-Reid/SE-Prolific-User-Study-Recruitment/f76a155fdb07ec4290b7e4bd8f5f0128fea1e2aa/Screening%20Survey%20(Part%201).pdf",
    "NA-005-CONSENT": "https://raw.githubusercontent.com/Brittany-Reid/SE-Prolific-User-Study-Recruitment/f76a155fdb07ec4290b7e4bd8f5f0128fea1e2aa/Video%20Call%20Consent%20Form%20(Part%202).pdf",
    "NA-006": "https://zenodo.org/api/records/5094598",
    "NA-007": "https://brittany-reid.github.io/publication/reid-2023-ncq/",
    "NA-008": "https://api.crossref.org/works/10.1145/2414782.2414783",
    "NA-009": "https://people.csail.mit.edu/hunkim/",
    "NA-FAIL-EXOA-HTTP": "http://exoa.postech.ac.kr/",
    "NA-FAIL-EXOA-HTTPS": "https://exoa.postech.ac.kr/",
    "NA-FAIL-ACM": "https://dl.acm.org/doi/10.1145/2414782.2414783",
    "NA-SEARCH-GITHUB": "https://api.github.com/search/repositories?q=eXoaDocs",
    "NA-SEARCH-ZENODO": "https://zenodo.org/api/records?q=exoadocs&size=25",
    "NA-SEARCH-OSF": "https://api.osf.io/v2/nodes/?filter%5Btitle%5D=eXoaDocs",
}


def fetch(item):
    key, url = item
    result = {"source_id": key, "url": url,
              "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            body = response.read()
            result.update(status="opened", http_status=response.status,
                          bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                          content_type=response.headers.get("Content-Type"))
            if key.startswith("NA-SEARCH"):
                data = json.loads(body)
                result["result_count"] = (data.get("total_count") if "github" in url
                                          else data.get("hits", {}).get("total") if "zenodo" in url
                                          else len(data.get("data", [])))
            if key == "NA-008":
                result["relation"] = json.loads(body)["message"].get("relation")
            if key == "NA-006":
                data = json.loads(body)
                result["record_title"] = data["metadata"]["title"]
                result["record_version"] = data["metadata"].get("version")
                result["files"] = [{"name": x["key"], "size": x["size"], "checksum": x["checksum"]}
                                   for x in data["files"]]
    except Exception as error:
        result.update(status="access_failed", error_type=type(error).__name__, error=str(error))
    result["finished_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return result


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        records = list(pool.map(fetch, URLS.items()))
    print(json.dumps({"purpose": "source recheck receipts after direct reading; not full source copies",
                      "records": records}, ensure_ascii=False, indent=2))
