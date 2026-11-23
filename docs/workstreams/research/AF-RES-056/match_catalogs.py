"""Reproduce frozen L/V membership and rank, without provider access."""
from pathlib import Path
import csv, json, re
P=Path(__file__).resolve().parent
def read(file): return list(csv.DictReader((P/file).open()))
def norm(s): return re.sub(r'\s+', ' ',s.casefold().replace('-',' ')).strip()
def run():
    cats=read('catalog.csv'); vocab=read('vocabulary.csv'); reqs=json.loads((P/'requirements.json').read_text())
    out=[]
    for req in reqs:
        pool=[r for r in cats if r['family']==req['domain']]
        for method in ('L','V'):
            terms=[]
            for v in vocab:
                if v['case_id']==req['case_id'] and (v['method']=='L,V' or (method=='V' and v['method']=='V')):
                    if norm(v['target_term']) not in [x['normalized'] for x in terms]:
                        terms.append({'mapping_id':v['mapping_id'],'term':v['target_term'],'normalized':norm(v['target_term'])})
            hits=[]; seen=set()
            for row in pool:
                matches=[]
                for term in terms:
                    for index,field in enumerate(json.loads(row['search_fields_json'])):
                        if re.search(r'(?<!\w)'+re.escape(term['normalized'])+r'(?!\w)',norm(field)):
                            matches.append({'mapping_id':term['mapping_id'],'term':term['term'],'field_index':index,'field_value':field})
                if matches and row['destination_url'] not in seen:
                    seen.add(row['destination_url'])
                    hits.append({'catalog_id':row['catalog_id'],'posted_rank':int(row['posted_rank']),'url':row['destination_url'],'hits':matches})
            out.append({'comparison_id':req['case_id']+'-'+method,'terms':terms,'hits':hits,'top3':[x['catalog_id'] for x in hits[:3]]})
    return out
if __name__=='__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2))
