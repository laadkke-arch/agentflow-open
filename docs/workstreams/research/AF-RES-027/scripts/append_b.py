"""Append B references and finish B frame rows, preserving every sealed A row."""
import copy,csv,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SEAL="1714a55a529c7da42596ac0779d398f3aacf97c3"
RELPATH="docs/workstreams/research/AF-RES-027/"
def main():
    refpath=ROOT/"references.jsonl"
    frozen=subprocess.check_output(["git","show",SEAL+":"+RELPATH+"references.jsonl"],text=True)
    a=[json.loads(x) for x in frozen.splitlines()]
    current_a=[json.loads(x) for x in refpath.read_text().splitlines() if json.loads(x).get("sample")=="A"]
    assert current_a==a
    amap={x["reference_id"]:x for x in a}
    bh=json.loads((ROOT/"collectors/homebrew-b/cases.json").read_text())
    bc=json.loads((ROOT/"collectors/conda-b/cases.json").read_text())
    refs=[]
    for bid,aid in [("B-H01","A-H02"),("B-H03","A-H06")]:
        r=copy.deepcopy(amap[aid]);r.update(reference_id=bid,sample="B",linked_A_reference=aid,
            sampling="predeclared upstream-first B attempt; same reference as A, no A increment",
            future_read_before_seal=None)
        refs.append(r)
    r={"reference_id":"B-H02","sample":"B","ecosystem":"Homebrew","consumer_project":"borgbackup/borg",
       "consumer_commit":"fc96fc4bfd22b72d01e603660bd475d57d6b1525","consumer_commit_date":"2019-12-23T17:19:44Z",
       "consumer_path":"docs/installation.rst","consumer_file_url":"https://github.com/borgbackup/borg/blob/fc96fc4bfd22b72d01e603660bd475d57d6b1525/docs/installation.rst",
       "package":"python","raw_reference":"brew install python3 openssl","selected_token":"python3","raw_citation_url":None,
       "normalized_catalog_url":"https://formulae.brew.sh/formula/python","catalog_url_provenance":"researcher normalization of name; not a literal consumer citation URL",
       "purpose":"Borg source/pip install; Python3 runtime+headers; create virtualenv and pip install current Borg",
       "version_requirement":">=3.5.0 in old instructions","purpose_intent":"current installation, not declared historical reproduction",
       "same_version_callsite_urls":["https://github.com/borgbackup/borg/blob/fc96fc4bfd22b72d01e603660bd475d57d6b1525/docs/installation.rst"],
       "same_version_callsite_location":"Dependencies L143–161, macOS L222–236, virtualenv/pip L294–309",
       "source_vs_release":"fixed source snapshot; consumer release version not established",
       "source_ids":["BH-S07"],"sampling":"predeclared upstream-first B attempt",
       "future_read_before_seal":None,"linked_A_reference":None}
    refs.append(r)
    for c in bc:
        o=c["consumer"];bid=c["case_id"]
        package={"B-C01":"matplotlib","B-C02":"mamba","B-C03":"qt"}[bid]
        path=o["old_url"].split("/blob/"+o["old_commit"]+"/",1)[1]
        r={"reference_id":bid,"sample":"B","ecosystem":"conda-forge","consumer_project":o["project"],
           "consumer_commit":o["old_commit"],"consumer_commit_date":o["old_date"],
           "consumer_path":path,"consumer_file_url":o["old_url"],"package":package,
           "raw_reference":o["reference"],"raw_citation_url":None,
           "normalized_catalog_url":"https://anaconda.org/conda-forge/"+package,
           "catalog_url_provenance":"researcher normalization; package/channel token in consumer original",
           "purpose":o["purpose"],"version_requirement":o["reference"],
           "purpose_intent":"as stated in fixed source; historical preservation not assumed",
           "same_version_callsite_urls":[o["old_url"]],"same_version_callsite_location":"See BC source record read_location and related_original_urls",
           "source_vs_release":"fixed source snapshot; release publication handled separately in chains",
           "source_ids":c["source_ids"],"sampling":"predeclared upstream-first B attempt",
           "future_read_before_seal":None,"linked_A_reference":None}
        if "auxiliary_repair" in c:
            r["auxiliary_reference_variant"]=c["auxiliary_repair"]
            r["auxiliary_reference_not_extra_attempt"]=True
        refs.append(r)
    refs.sort(key=lambda x:x["reference_id"])
    assert len(refs)==6 and len({x["reference_id"] for x in refs})==6
    refpath.write_text(frozen+"".join(json.dumps(x,ensure_ascii=False)+"\n" for x in refs))
    framepath=ROOT/"frame.csv"; old=list(csv.DictReader(framepath.open()))
    fields=list(old[0])
    old=[x for x in old if x["sample"]!="B_CANDIDATE"]
    bmap={x["reference_id"]:x for x in refs}
    shas={"B-H01":"48b5788c062ba492c34890e1b2a7cb26c8a1505f","B-H02":"56a265eb11a92c05efa050a565b5c9af1b97067c","B-H03":"562c37360f8133eda5870ab801d1a7710fe9abdc"}
    shas.update({x["case_id"]:x["upstream"]["after_commit"] for x in bc})
    descriptions={x["case_id"]:x["selected_event"] for x in bh+bc}
    for row in old:
        if row["sample"]!="B":continue
        rid=row["reference_id"];r=bmap[rid]
        row.update(consumer_project=r["consumer_project"],fixed_commit=shas[rid],
          selection_status="ATTEMPT_COMPLETED",duplicate_A_id=r.get("linked_A_reference") or "",
          reason=descriptions[rid]+"; upstream-first exploration, excluded from A rates")
    for c in bc:
        for i,alt in enumerate(c.get("secondary_attempts",[]),1):
            row={k:"" for k in fields}
            row.update(frame_id="F-"+c["case_id"]+"-ALT"+str(i),sample="B_CANDIDATE",ecosystem="conda-forge",
              consumer_project=alt["project"],reference_id=c["case_id"],selection_status="EXCLUDED_OR_UNRESOLVED",
              reason=alt["status"],outcome_used="True",ledger_url=c["upstream"]["proposal_url"])
            old.append(row)
    with framepath.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");w.writeheader();w.writerows(old)
    print(json.dumps({"A_references_preserved":len(a),"B_attempt_references":len(refs),"B_alternatives":sum(x["sample"]=="B_CANDIDATE" for x in old)}))
if __name__=="__main__":main()
