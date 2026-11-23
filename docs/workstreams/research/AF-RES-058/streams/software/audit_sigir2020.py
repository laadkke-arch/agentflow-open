#!/usr/bin/env python3
"""Read-only aggregate audit of the author SIGIR2020 package; emits no participant rows."""
import argparse, collections, datetime, hashlib, json, re
from pathlib import Path

def read_jsonl(path):
    return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]

def session_key(row):
    value = row.get("session")
    # App.js serializes an integer; verify.html posts an HTML string. Only exact
    # nonnegative integral strings/ints are treated as the same documented session.
    if isinstance(value, int) or (isinstance(value, str) and re.fullmatch(r"[0-9]+", value)):
        return (row.get("id"), str(int(value)))
    return (row.get("id"), type(value).__name__ + ":" + repr(value))

def audit(root):
    results = []
    all_rows = collections.defaultdict(list)
    schema = []
    keys = set()
    for batch in range(1,6):
        per = {}
        rows = {}
        for name in ("links","responses","verify"):
            path = root / f"client/data/batch_{batch}/{name}.json"
            data = read_jsonl(path)
            rows[name] = data
            all_rows[name].extend(data)
            fields = sorted(set().union(*(r.keys() for r in data)))
            keys.update(fields)
            ids = [r.get("id") for r in data]
            per[name] = {"rows":len(data), "unique_id":len(set(ids)),
                         "id_missing":sum(x is None for x in ids)}
            schema.append({"file":str(path.relative_to(root)), "format":"JSON Lines despite .json suffix",
                           "sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                           "data_rows":len(data),"line_range":[1,len(data)],"fields":fields})
            if name != "responses":
                counts = collections.Counter(map(session_key,data))
                per[name]["unique_id_session"] = len(counts)
                per[name]["duplicate_id_session_keys"] = sum(n>1 for n in counts.values())
                per[name]["surplus_rows_on_duplicate_keys"] = sum(n-1 for n in counts.values())
            if name == "links":
                per[name]["fields_missing_rows"] = {k:sum(k not in r for r in data) for k in ("queries","views","time")}
                per[name]["empty_bookmark_snapshot_rows"] = sum(not r.get("links") for r in data)
            if name == "verify":
                per[name]["stored_numCorrect"] = dict(sorted(collections.Counter(str(r.get("numCorrect","missing")) for r in data).items()))
                stored = [r for r in data if "numCorrect" in r]
                answer_keys = ("answer-1","answer-4","answer-2","answer-2")
                per[name]["stored_score_vs_HEAD_key_mismatches"] = sum(r["numCorrect"] != sum(r.get(f"Question {i} goes here")==k for i,k in enumerate(answer_keys,1)) for r in stored)
                per[name]["stored_score_rows_checked"] = len(stored)
        id_sets={k:{r["id"] for r in v} for k,v in rows.items()}
        lkeys=collections.Counter(map(session_key,rows["links"]))
        vkeys=collections.Counter(map(session_key,rows["verify"]))
        matched=set(lkeys)&set(vkeys)
        joined={"all_three_id":len(set.intersection(*id_sets.values())),
                "responses_without_links_id":len(id_sets["responses"]-id_sets["links"]),
                "responses_without_verify_id":len(id_sets["responses"]-id_sets["verify"]),
                "links_and_verify_id_session_keys":len(matched),
                "one_to_one_links_verify_keys":sum(lkeys[k]==1 and vkeys[k]==1 for k in matched),
                "ambiguous_links_verify_keys":sum(lkeys[k]!=1 or vkeys[k]!=1 for k in matched)}
        results.append({"batch":batch, "tables":per,"joins":joined})
    totals={k:{"rows":len(v),"unique_id":len({r["id"] for r in v})} for k,v in all_rows.items()}
    ids={k:{r["id"] for r in v} for k,v in all_rows.items()}
    totals["all_three_id"] = len(set.intersection(*ids.values()))
    totals["export_id_gaps_not_participant_attrition"] = {
        "links_without_verify":len(ids["links"]-ids["verify"]),
        "verify_without_links":len(ids["verify"]-ids["links"]),
        "verify_without_responses":len(ids["verify"]-ids["responses"]),
        "links_without_responses":len(ids["links"]-ids["responses"])}
    scores=[r["numCorrect"] for r in all_rows["verify"] if "numCorrect" in r]
    totals["stored_score_only_diagnostic"]={"attempts":len(scores),"question_opportunities":4*len(scores),
        "correct_answers":sum(scores),"pass_attempts_ge3":sum(x>=3 for x in scores),
        "score_histogram":dict(sorted(collections.Counter(map(str,scores)).items())),
        "unit":"repeated quiz attempts; not recommendation acceptance, not independent people, not randomized conditions"}
    return {"actor":"software_ir assistant read-only local Python","observed_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "upstream_commit":"4a308f735066b2741d2931cd0e5dc0d372f06429","schema":schema,"batches":results,"totals":totals,
       "condition_fields_found":[k for k in sorted(keys) if any(t in k.lower() for t in ("condition","treatment","variant","arm","group","bars"))],
       "unresolved":["No author mapping from batches/ids to T/TA/TAB; public exports cannot be identified as the paper's 150-person analysis cohort.",
                     "No per-impression complete candidate/rank roster, article relevance label key, or attention-to-explanation log.",
                     "No pre-advice own answer; bookmarks are final snapshots without all add/remove events.",
                     "No join by sorted row order was made; duplicate id/session keys are reported, not arbitrarily collapsed.",
                     "HEAD code and instruction variants may differ from deployed experiment; no external app was run."]}
if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--package-root",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    a=parser.parse_args()
    data=audit(a.package_root)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"output":str(a.output),"totals":data["totals"],"condition_fields_found":data["condition_fields_found"]},ensure_ascii=False))

