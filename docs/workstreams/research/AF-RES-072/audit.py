"""Validate the archived corpus, path budgets, sealed joins and report tables."""

import argparse
import collections
import csv
import gzip
import json
import re
from pathlib import Path

from lxml import html

from capture import lines
from report import ARMS, LABELS, summarize
from search import CARD
from source_io import DISPLAY, MAX_BODY, MAX_OPENS, sha

ROOT = Path(__file__).resolve().parent


def csv_rows(name):
    with (ROOT/name).open(encoding="utf-8", newline="") as source:
        rows = list(csv.reader(source))
    columns, *body = rows
    assert len(columns) == len(set(columns)), name
    assert body and all(len(row) == len(columns) for row in body), name
    return [dict(zip(columns,row)) for row in body]


def indexed(rows, *keys):
    result = {tuple(r[k] for k in keys):r for r in rows}
    assert len(rows) == len(result), keys
    return result


def markdown_rows(markdown):
    rows = []
    section = None
    for line in markdown.splitlines():
        if line.startswith("## 표 "):
            section = []
            rows.append(section)
        elif section is not None and line.startswith("## "):
            section = None
        elif section is not None and line.startswith("|"):
            section.append(line.count("|")-1)
    return [len(table)-2 for table in rows if table and len(set(table))==1], rows


def check(replay_a=None, replay_b=None):
    source = lines(ROOT/"sources.jsonl")
    corpus = lines(ROOT/"corpus.jsonl")
    request = lines(ROOT/"requests.jsonl")
    urls = lines(ROOT/"urls.jsonl")
    cards = lines(ROOT/"cards.jsonl")
    purpose = lines(ROOT/"purpose.jsonl")
    source_by_id = indexed(source,"source_id")
    counted = [r for r in source if r["counts_toward_20"]]
    assert len(counted) == len(corpus) == len(cards) == len(urls) == len(purpose) == 20
    assert len({r["lineage"] for r in counted}) == 20
    assert len({r["opened_url"] for r in counted}) == 20
    assert all(r["authors"] and r["edition"] and r["checked_utc"] and r["sections"] and
               r["verified_claim"] and r["limits"] and r["counter_or_unknown"] for r in source)
    assert dict(collections.Counter(r["family"] for r in corpus)) == {"A":8,"W":6,"N":6}
    url_by_id = indexed(urls,"work_id")
    manifest = indexed(lines(ROOT/"frozen/manifest.jsonl"),"work_id")
    assert all(set(r)=={"work_id","url","owner","access"} for r in urls)
    assert {(r["work_id"],) for r in corpus} == set(url_by_id) == set(manifest)
    docs = {}
    frozen = {}
    for work in corpus:
        key = (work["work_id"],)
        docs[key[0]] = work
        raw_record = manifest[key]
        url = url_by_id[key]
        packed = (ROOT/work["path"]).read_bytes()
        raw = gzip.decompress(packed)
        frozen[key[0]] = raw
        assert source_by_id[("S-"+key[0],)]["lineage"] == work["lineage"]
        assert raw_record["url"] == url["url"] == work["retrieval_url"]
        assert raw_record["complete"] and raw_record["http_status"] == 200
        assert len(raw) == work["raw_bytes"] == raw_record["read_bytes"]
        assert sha(raw) == work["raw_sha256"] == raw_record["body_sha256"]
        assert len(packed) == raw_record["stored_bytes"] and sha(packed) == raw_record["stored_sha256"]
    cards_by_id = indexed(cards,"work_id")
    assert set(cards_by_id) == set(url_by_id)
    counts = [len(" ".join(r[key] for key in CARD).split()) for r in cards]
    assert max(counts) <= 80
    assert purpose == [{k:r[k] for k in ("work_id","name","purpose")} for r in cards]

    frames = {r["frame_id"]:r for r in csv_rows("issue-frame.csv")}
    cframe = [r for r in csv_rows("corpus-frame.csv") if r["state"]=="selected"]
    assert {(r["work_id"],r["source_commit"]) for r in cframe} == {(r["work_id"],r["pin"]) for r in corpus}
    ids = indexed(request,"request_id")
    assert len(ids)==8
    assert collections.Counter((r["group"],r["split"]) for r in request) == {
        ("Z","pilot"):1,("O","pilot"):1,("Z","holdout"):3,("O","holdout"):3,
    }
    assert all(re.fullmatch(r"[0-9a-f]{64}",r["body_sha256"]) and r["positive"] and r["boundary"] and
               r["environment"] and frames[r["frame_id"]]["observed_body_version"] == r["body_version"]
               for r in request)
    hold = {r["request_id"] for r in request if r["split"]=="holdout"}

    qrels = csv_rows("qrels.csv")
    judged = indexed(qrels,"request_id","work_id")
    assert set(judged) == {(case,work) for case in hold for work in docs}
    assert len({r["reader_alias"] for r in qrels}) == 120
    w3 = {key:html.fromstring(data) for key,data in frozen.items() if key.startswith("W")}
    for r in qrels:
        doc = docs[r["work_id"]]
        assert r["edition"]==doc["pin"]
        assert r["finding"] and r["source"] and r["section"]
        assert r["judgment"] in {"direct","partial","refute","unrelated","unverified"}
        assert r["distance"] in {"same","far"}
        transfer = tuple(r[key] for key in ("donor","recipient","transplant","break_condition"))
        if r["transfer_eligible"] == "True":
            assert r["judgment"] == "partial" and r["distance"]=="far" and all(transfer)
        else:
            assert not any(transfer)
        for where in r["section"].split(","):
            if doc["family"]=="W":
                assert w3[doc["work_id"]].get_element_by_id(where[1:],None) is not None
            else:
                start,stop = map(int,re.fullmatch(r"L(\d+)-L(\d+)",where).groups())
                assert 1 <= start <= stop <= len(frozen[doc["work_id"]].splitlines())

    rank = csv_rows("ranks.csv")
    alternate = csv_rows("evidence/alternate-ranks.csv")
    assert len(indexed(rank + alternate,"phase","rank_id"))==len(rank + alternate)
    assert len(rank)==72 and len(alternate)==300
    recurring = collections.defaultdict(list)
    for row in rank+alternate:
        recurring[row["phase"],row["path"],row["request_id"]].append(row)
        work = row["work_id"]
        assert (not work and not row["url"]) or row["url"] == url_by_id[(work,)]["url"]
        if row["phase"] == "offline":
            assert row["request_id"] in hold and row["path"] in ARMS
    for rows in recurring.values():
        assert [r["rank"] for r in rows]==["1","2","3"]
        returned = [r["work_id"] for r in rows if r["work_id"]]
        assert len(returned)==len(set(returned))

    fetch = lines(ROOT/"fetches.jsonl")
    assert len(indexed(fetch,"phase","path","request_id","attempt")) == 248
    assert len(indexed(fetch,"receipt_id")) == 248
    attempts = collections.defaultdict(list)
    for r in fetch:
        key = r["phase"],r["path"],r["request_id"]
        attempts[key].append(r)
        assert r["url"] == url_by_id[(r["work_id"],)]["url"]
        assert r["retries"] == 0
        assert r["remaining_before_bytes"] <= MAX_BODY
        if r["passage"] is not None:
            assert len(r["passage"].split())==r["display_words"]
            assert sha(r["passage"].encode()) == r["passage_sha256"]
        else:
            assert not r["display_words"] and r["error"]
        if r["body_sha256"]:
            assert (r["body_sha256"]==docs[r["work_id"]]["raw_sha256"])==r["exact_frozen_body"]

    costs = csv_rows("costs.csv")
    assert len(indexed(costs,"phase","path","request_id")) == len(costs)
    for cost in costs:
        if cost["stage"] != "request" or cost["phase"] == "offline_repeat":
            continue
        key = (cost["phase"],cost["path"],cost["request_id"])
        af = attempts[key]
        slots = recurring[key]
        assert [r["attempt"] for r in af] == list(range(1,len(af)+1))
        assert len(af)==int(cost["logical_opens"])<=MAX_OPENS
        assert len({r["work_id"] for r in af}) == len(af)
        assert sum(r["http_attempts"]+len(r["redirects"]) for r in af) == int(cost["http_requests"])
        assert sum(r["read_bytes"] for r in af) == int(cost["http_body_bytes"]) <= MAX_BODY
        assert sum(r["local_body_bytes"] for r in af) == int(cost["local_body_bytes"])
        shown = sum(r["display_words"] for r in af)+sum(int(r["displayed_card_words"]) for r in slots)
        assert shown == int(cost["displayed_words"]) <= DISPLAY
        assert int(cost["unused_display_words"]) == DISPLAY-shown
        assert int(cost["unused_opens"]) == MAX_OPENS-len(af)
        assert int(cost["unused_http_bytes"]) == MAX_BODY-int(cost["http_body_bytes"])
        assert sum(r["transport"]=="memory-hit" for r in af)==int(cost["cache_hits"])
        assert sum(bool(r["error"]) for r in af)==int(cost["failures"])
        if key[1] in {"I","P"}:
            assert not af and int(cost["scanned_card_rows"])==20
        elif key[1]=="L":
            assert int(cost["scanned_card_rows"])==0 and int(cost["scanned_url_rows"])==20
    capture = json.loads((ROOT/"frozen/timing.json").read_text())
    builds = {r["path"]:r for r in costs if r["stage"]=="build"}
    for arm,card_file in [("L",None),("I","cards.jsonl"),("H","cards.jsonl"),("P","purpose.jsonl")]:
        assert int(builds[arm]["persistent_bytes"])==(ROOT/"urls.jsonl").stat().st_size+(
            (ROOT/card_file).stat().st_size if card_file else 0)
        assert int(builds[arm]["http_body_bytes"])==(capture["body_bytes"] if card_file else 0)
        assert int(builds[arm]["http_requests"])==(capture["requests"] if card_file else 0)
    for card in ("qrel","rank"):
        seal=json.loads((ROOT/f"evidence/{card}-seal.json").read_text())
        if card=="qrel":
            assert all(sha((ROOT/f).read_bytes())==fingerprint for f,fingerprint in seal["hashes"].items())
        else:
            assert sha((ROOT/"ranks.csv").read_bytes())==seal["ranks_sha256"]
            assert all(sha((ROOT/f).read_bytes())==fingerprint
                       for f,fingerprint in seal["allowed_top_level_file_hashes"].items())
    modes = json.loads((ROOT/"evidence/replay-comparison.json").read_text())["run_hashes"]
    expected = modes["freeze-a"]
    assert expected["ranks.csv"] == modes["replay-b"]["ranks.csv"]
    assert expected["fetches.jsonl"] == modes["replay-b"]["fetches.jsonl"]
    if replay_a or replay_b:
        assert replay_a and replay_b
        for file in ("ranks.csv","fetches.jsonl"):
            assert sha((replay_a/file).read_bytes()) == expected[file] == sha((replay_b/file).read_bytes())

    actual, markdown = summarize()
    stored = json.loads((ROOT/"evidence/metrics.json").read_text())
    assert json.dumps(actual,sort_keys=True) == json.dumps(stored,sort_keys=True)
    report = (ROOT/"RESULT.md").read_text()
    assert markdown in report
    row_counts,widths = markdown_rows(report)
    assert row_counts == [24,144,8]
    assert all(width == 9 for table in widths for width in table)
    assert all(re.search(rf"^## Q{n}\.",report,re.MULTILINE) for n in range(1,9))
    assert "W1 ·" in report and "W2 ·" in report and "W3 ·" in report
    all_direct = sum(x["judgment"]=="direct" for x in qrels)
    assert all_direct == 0
    return dict(corpus=len(corpus),source_records=len(source),cards_max_words=max(counts),requests=len(request),
                holdout=len(hold),qrel_pairs=len(qrels),rank_rows=len(rank),alternate_rank_rows=len(alternate),
                fetch_rows=len(fetch),cost_rows=len(costs),result_tables=row_counts,
                qrel_strata=actual["qrel_cases"],live_body_fingerprints=actual["main_network"],
                replay_files_checked_in_this_run=bool(replay_a and replay_b))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay-a",type=Path)
    parser.add_argument("--replay-b",type=Path)
    args=parser.parse_args()
    print(json.dumps(check(args.replay_a,args.replay_b),ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
