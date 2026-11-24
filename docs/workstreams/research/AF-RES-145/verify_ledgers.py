"""Replay ledger integrity only; not a target product test or independent reader."""
import csv, json, pathlib, collections
p=pathlib.Path(__file__).parent
def jl(n):
    return [json.loads(x) for x in (p/n).read_text(encoding="utf-8").splitlines() if x.strip()]
def cs(n):
    with (p/n).open(encoding="utf-8", newline="") as f: return list(csv.DictReader(f))
def fnv16(obj):
    raw=json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-16-le", errors="surrogatepass")
    h=2166136261
    for i in range(0,len(raw),2):
        h=((h^(raw[i]|(raw[i+1]<<8)))*16777619)&0xffffffff
    return f"{h:08x}"
frame,sources,drafts,packets,discovery,readings,judge=(cs("frame.csv"),jl("sources.jsonl"),jl("drafts.jsonl"),jl("packets.jsonl"),jl("discovery.jsonl"),jl("readings.jsonl"),cs("adjudication.csv"))
assert len(frame)==80
assert collections.Counter(r["repo"] for r in frame)=={"FreeCAD/FreeCAD":40,"laurent22/joplin":40}
selected=[r for r in frame if r["event_id"]]
assert len(selected)==8
for repo in ("FreeCAD/FreeCAD","laurent22/joplin"):
    for kind in ("W","P"):
        group=sorted([r for r in frame if r["repo"]==repo and r["classification"]==kind],key=lambda r:int(r["rank"]))
        assert len(group)>=2 and all(r["event_id"] for r in group[:2])
        assert sum(bool(r["event_id"]) for r in group)==2
ids={r["event_id"] for r in selected}
base=[r for r in packets if r["packet_type"]=="baseline_input"]
assert len(base)==8 and all(r["body_match_search"] for r in base)
for d in drafts:
    x={k:v for k,v in d.items() if k not in ("fingerprint_fnv1a_utf16","line")}
    assert fnv16(x)==d["fingerprint_fnv1a_utf16"],d["event_id"]
for group in (base,drafts,discovery,readings,judge):
    assert len(group)==8 and {r["event_id"] for r in group}==ids
sids={r["source_id"] for r in sources}
assert len(sources)==len(sids)==38
counted=[r for r in sources if r["counts"]]
assert len(counted)==len({r["work_id"] for r in counted})==25
assert collections.Counter(r["type"] for r in counted)=={"original request":8,"supplier":8,"supplier-extra":1,"boundary":4,"nonsoftware-control":4}
assert all(r["type"]!="failed" for r in counted)
assert sum(r["type"]=="failed" for r in sources)==3
assert all(set(r["source_ids"]+r["packet_source_ids"]+r["failed"])<=sids for r in discovery)
assert all(set(r["source_ids"]+r["counter_sources"])<=sids for r in readings)
assert all(set(r["source_ids"].split(";"))<=sids for r in judge)
assert all(r["query_count"]<=4 and r["direct_attempts"]<=6 and len(r["packet_source_ids"])<=3 for r in discovery)
assert sum(r["query_count"] for r in discovery)==22
assert sum(r["direct_attempts"] for r in discovery)==22
assert sum(r["direct_successes"] for r in discovery)==21
assert len({q for r in discovery for q in r["queries"]})==18
assert all(not r["condition_valid"] and not any(s.startswith("C") for s in r["source_ids"]) for r in discovery)
assert all(not r["blind"] and not r["independent"] and not r["actual_test_run"] for r in readings)
assert all(r["pair_class"]=="비교불가" for r in judge)
print("Ledger structure PASS: selected=8; counted distinct=25; valid paired comparisons=0/8; target tests=0; effect rate undefined")
