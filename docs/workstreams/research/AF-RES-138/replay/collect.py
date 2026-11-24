"""Recover the frozen GitHub Search windows and isolate first bodies."""

import argparse
import importlib.util
import json
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode


QUERIES = Path(__file__).resolve().with_name("queries.json")


def acquisition(path):
    spec = importlib.util.spec_from_file_location("af134_acquire", path / "acquire.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def utc_created(value):
    return datetime.fromisoformat(value).astimezone(timezone.utc)


def locator(result, page, number):
    repository = result["repo"]["repository"]
    owner_repo = repository["owner_login"] + "/" + repository["name"]
    issue_number = result["number"]
    return {
        "repository": owner_repo,
        "issue_number": issue_number,
        "issue_id": result["id"],
        "issue_url": f"https://github.com/{owner_repo}/issues/{issue_number}",
        "created_at": utc_created(result["created"]).isoformat(),
        "origin_page": page,
        "origin_position": number,
        "search_body_state": "search_highlight" if result.get("hl_text") else "no_search_highlight",
    }


def sort_key(row):
    return utc_created(row["created_at"]), row["repository"].casefold(), row["issue_number"]


def fetch_query(query, cap, acquire):
    rows, receipts = [], []
    page = 1
    state = "unresolved"
    while True:
        params = {"q": query["query"] + " sort:created-asc", "type": "issues"}
        if page > 1:
            params["p"] = page
        receipt, body = acquire.get("https://github.com/search?" + urlencode(params), "text/html")
        receipt.update(query_id=query["id"], query=query["query"], page=page,
                       returned=None, returned_body_state="no_origin_body")
        receipts.append(receipt)
        if body is None:
            break
        try:
            result = acquire.page_route(body, "blackbirdSearchRoute")
            returned = result["results"]
            receipt.update(returned=len(returned), result_count=result["result_count"],
                           page_count=result["page_count"], returned_page=result["page"],
                           result_type=result["type"], errors=result["errors"],
                           logged_in=result["logged_in"], limited=result["warn_limited_results"],
                           returned_body_state="search_hits_only")
            if result["page"] != page or result["type"] != "issues" or result["errors"] or result["warn_limited_results"]:
                raise ValueError("search payload page, type or completeness differs")
            offset = len(rows)
            for index, item in enumerate(returned, offset + 1):
                rows.append(locator(item, page, index))
            receipt["last_id"] = rows[-1]["issue_id"] if returned else None
            receipt["last_issue"] = rows[-1]["issue_url"] if returned else None
            receipt["last_created_utc"] = rows[-1]["created_at"] if returned else None
            dates = [utc_created(row["created_at"]) for row in rows]
            if dates != sorted(dates):
                raise ValueError("GitHub array does not preserve requested creation order")
            if len({row["issue_id"] for row in rows}) != len(rows):
                raise ValueError("GitHub result pages contain repeated issue IDs")
            if page >= result["page_count"] or not returned:
                if len(rows) != result["result_count"]:
                    raise ValueError("terminal page count disagrees with returned search rows")
                state = "complete"
                break
            if len(rows) > cap and dates[-1] > dates[cap - 1]:
                state = "complete"
                break
        except (KeyError, TypeError, ValueError, UnicodeError) as exc:
            receipt.update(access="wrong_search_payload", detail=str(exc))
            break
        page += 1
    frozen = sorted(rows, key=sort_key)[:cap]
    window = [{"query_id": query["id"], "layer": query["layer"], "position": index, **row}
              for index, row in enumerate(frozen, 1)]
    receipts.append({
        "query_id": query["id"], "kind": "window", "status": state, "cap": cap,
        "pages_fetched": page, "received_rows": len(rows), "frozen": len(window),
        "checking_boundary_rows": rows[cap:], "last": window[-1] if window else None,
        "frozen_at_utc": acquire.utc(),
    })
    return window, receipts


def collect_search(queries, cap, output, acquire):
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(lambda q: fetch_query(q, cap, acquire), queries))
    windows, pages = zip(*results, strict=True)
    order = {q["id"]: index for index, q in enumerate(queries)}
    window = sorted((r for batch in windows for r in batch),
                    key=lambda r: (r["position"], order[r["query_id"]]))
    acquire.save(output / "window.jsonl", window)
    acquire.save(output / "search.jsonl", [r for batch in pages for r in batch])


def collect_openings(window, output, acquire):
    grouped = defaultdict(list)
    for row in acquire.read(window):
        grouped[row["issue_id"]].append(row)
    with ThreadPoolExecutor(max_workers=3) as pool:
        openings = list(pool.map(lambda slots: acquire.issue_opening(slots[0]), grouped.values()))
    for row, slots in zip(openings, grouped.values(), strict=True):
        row["slots"] = [f"{s['query_id']}-{s['position']:02d}" for s in slots]
        if row["access"] == "opening":
            if str(row["database_id"]) != str(row["issue_id"]):
                row["access"] = "identity_mismatch"
            elif not isinstance(row["body"], str):
                row["access"] = "opening_body_absent"
            elif not row["body"].strip():
                row["access"] = "opening_body_empty"
    acquire.save(output / "openings.jsonl", openings)
    acquire.save(output / "opening-receipts.jsonl",
                 [{k: v for k, v in row.items() if k != "body"} for row in openings])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("search", "openings"))
    parser.add_argument("--af134", required=True, type=Path, help="directory containing pinned acquire.py")
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--window", type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    acquire = acquisition(args.af134)
    config = json.loads(QUERIES.read_text(encoding="utf-8"))
    if args.mode == "search":
        collect_search(config["query_order"], config["cap"], args.out, acquire)
    elif args.window:
        collect_openings(args.window, args.out, acquire)
    else:
        parser.error("openings requires --window")


if __name__ == "__main__":
    main()
