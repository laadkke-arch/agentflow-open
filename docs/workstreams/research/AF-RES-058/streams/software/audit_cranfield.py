#!/usr/bin/env python3
"""Diagnostic corpus/source matching only; does not estimate participant effects."""
import argparse, collections, datetime, hashlib, json, re, tarfile
from pathlib import Path

def norm(s):
    return re.sub(r"\s+"," ",s).strip().casefold()

def audit(archive,root):
    with tarfile.open(archive,"r:gz") as t:
        raw={name:t.extractfile(name).read() for name in ("cran.all.1400","cran.qry","cranqrel","cranqrel.readme")}
    content=raw["cran.all.1400"].decode()
    index=collections.defaultdict(list)
    for block in re.split(r"(?m)^\.I ",content)[1:]:
        identifier=block.splitlines()[0].strip()
        title=re.search(r"(?s)\.T\s*\n(.*?)\n\.[A-Z]",block).group(1)
        index[norm(title)].append(identifier)
    query_blocks=re.split(r"(?m)^\.I ",raw["cran.qry"].decode())[1:]
    matches=[]
    prompt="What are the structural and aeroelastic problems associated with flight of high speed aircraft?"
    query_norm=lambda s:re.sub(r"[\s?.]+$", "", norm(s))
    for ordinal,block in enumerate(query_blocks,1):
        text=block.split(".W",1)[1]
        if query_norm(text)==query_norm(prompt):
            matches.append({"ordinal":ordinal,"source_I_identifier":block.splitlines()[0].strip()})
    qrels=raw["cranqrel"].decode().splitlines()
    query2=[(i,l.split()) for i,l in enumerate(qrels,1) if l.strip() and l.split()[0]=="2"]
    titles=set();occurrences=0
    for f in sorted((root/"client/data").glob("*/links.json")):
        for line in f.read_text().splitlines():
            if not line.strip():continue
            for pair in json.loads(line)["links"]:
                occurrences+=1;titles.add(pair[0])
    matching=collections.Counter("unique_exact_title" if len(index[norm(t)])==1 else
        ("ambiguous_exact_title" if len(index[norm(t)])>1 else "no_exact_title") for t in titles)
    return {"observed_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "source_id":"SW-S34","archive_url":"https://ir.dcs.gla.ac.uk/resources/test_collections/cran/cran.tar.gz",
      "archive_sha256":hashlib.sha256(archive.read_bytes()).hexdigest(),
      "files_sha256":{n:hashlib.sha256(v).hexdigest() for n,v in raw.items()},
      "query_match":matches,"query_match_rule":"case/whitespace normalization and terminal question mark/period ignored; word sequence preserved",
      "query_count":len(query_blocks),"document_count":sum(map(len,index.values())),"qrel_total_rows":sum(bool(l.strip()) for l in qrels),
      "qrel_query2_lines":[query2[0][0],query2[-1][0]],"qrel_query2_count":len(query2),
      "qrel_query2_code_histogram":dict(sorted(collections.Counter(r[2] for _,r in query2).items())),
      "readme_code_semantics":{"1":"complete answer","2":"high relevance","3":"useful background/method","4":"minimal interest","5":"no interest, stated omitted","-1":"not defined in supplied readme"},
      "bookmark_snapshot_occurrences":occurrences,"distinct_bookmark_title_values":len(titles),
      "title_match":dict(matching),"matching_rule":"case-fold and whitespace normalization only; no row-order merge or fuzzy matching",
      "duplicate_normalized_corpus_titles":sum(len(v)>1 for v in index.values()),
      "readme_version_note":"README names two legacy qrel sources differing in three lines; current archive contains cranqrel only, not CRAN.REL. The discrepant item IDs are not identified.",
      "limitations":["Title-level diagnostic matching does not establish deployed corpus version or article-body identity.",
       "One ambiguous bookmark title not assigned to either document.",
       "Unlisted qrels were not silently converted to incorrect advice.",
       "No threshold for graded relevance was specified by the selected human protocol.",
       "No full exposure/rank roster or T/TA/TAB mapping exists in the audited export; therefore no correct/wrong acceptance denominator is computed.",
       "Snapshot occurrences repeat across sessions and must not be treated as independent trials."]}
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--archive",type=Path,required=True);p.add_argument("--package-root",type=Path,required=True);p.add_argument("--output",type=Path,required=True)
    a=p.parse_args();d=audit(a.archive,a.package_root);a.output.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:d[k] for k in ("query_match","qrel_query2_count","qrel_query2_code_histogram","distinct_bookmark_title_values","title_match")}))

