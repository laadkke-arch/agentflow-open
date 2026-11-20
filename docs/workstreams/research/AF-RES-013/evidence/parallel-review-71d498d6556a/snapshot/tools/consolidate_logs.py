"""Index exact recorded searches and convert actual run reads to source-ledger rows."""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]

def main():
    searches=[]
    for f in sorted((ROOT/'evidence').rglob('*SEARCH_LOG.json')):
        if f.parent.name=='baseline': continue
        data=json.loads(f.read_text())
        # Preserve each input verbatim rather than silently flattening different author schemas.
        searches.append({'recorded_in':str(f.relative_to(ROOT)),'records':data})
    sources,excluded,run_indexes,shards=[],[],[],[]
    (ROOT/'evidence/baseline').mkdir(exist_ok=True)
    for f in sorted((ROOT/'runs').glob('*/*.json')):
        run=json.loads(f.read_text()); tag=f"RUN-{run['baseline']}-{run['case_id']}"
        source_start, excluded_start = len(sources), len(excluded)
        run_indexes.append({'case_id':run['case_id'],'baseline':run['baseline'],'path':str(f.relative_to(ROOT)),'queries':run['queries'],'started_at_utc':run['started_at_utc'],'ended_at_utc':run['ended_at_utc']})
        for i,o in enumerate(run['opened_documents'],1):
            sid=f'{tag}-D{i:02d}'; url=o['url']
            if o.get('status')!='opened':
                excluded.append({'id':sid,'url':url,'accessed_at_utc':o.get('at_utc',run['ended_at_utc']),'reason':o.get('confirmed',o.get('status')),'recorded_in':str(f.relative_to(ROOT)),'counts_toward_minimum':False}); continue
            # A successful HTTP/tool response is not always a document-body read.
            # Preserve metadata-only and relocation observations in exclusions.
            body_note=(o.get('confirmed','')+' '+o.get('sections_read','')).lower()
            metadata_only=o.get('verification_incomplete',False) or any(t in body_note for t in (
                'readme body did not load','content was not rendered',
                'not expose usable catalogue entries','actual release-note body was not retrieved',
                'redirect wrapper','redirect stub','omitted the substantive body','omitted substantive body','before returning useful content','before returning content',
                'did not expose its substantive body','not expose its substantive body'))
            if metadata_only:
                excluded.append({'id':sid,'url':url,'accessed_at_utc':o.get('at_utc',run['ended_at_utc']),
                  'reason':'Opened response but substantive body not verified: '+o.get('confirmed',''),
                  'recorded_in':str(f.relative_to(ROOT)),'observation_level':'D3-fetch','counts_toward_minimum':False})
                continue
            candidate=next((c for c in run['candidates'] if c['url']==url),None)
            is_code=bool(re.search(r'\.(?:go|rs|java|c|h|cpp|hpp|scm|py|swift|cs)(?:$|\?)',url))
            # A missing branch name is not evidence of an immutable revision.
            # Live code endpoints such as go.dev/src/... remain D3-fetch.
            pinned=is_code and bool(re.search(r'/(?:[0-9a-f]{40}|(?:v|go|release[-_])?\d+\.\d+(?:\.\d+)?(?:[-_][A-Za-z0-9.]+)?)/',url))
            api=('api.github.com/' in url or 'grep.app/api/' in url or 'github.com/search' in url)
            level='D3-fetch' if api or (is_code and not pinned) else 'D2' if pinned else 'D1'
            confirmed=o.get('confirmed','Actual opened response recorded in the immutable run.')
            if any(t in confirmed.lower() for t in ['before returning useful content','before returning content','did not expose its substantive body','not expose its substantive body']): level='D3-fetch'
            sources.append({'id':sid,'url':url,'accessed_at_utc':o.get('at_utc',run['ended_at_utc']),
              'source_type':'code_search_response' if api else 'public_code' if is_code else 'baseline_opened_document',
              'title':candidate['name'] if candidate else urlsplit(url).path.rsplit('/',1)[-1] or urlsplit(url).hostname,
              'version_or_date':o.get('published_or_version') or 'live','sections_read':o.get('sections_read','See original run read log'),
              'confirmed':confirmed,'limits':(candidate.get('constraints_or_caveat','')+' ' if candidate else '')+'This is the recorded read scope, not a full-document or deployment validation. Evidence time class: '+o.get('date_status','unknown')+'. Original read and any failures remain in '+str(f.relative_to(ROOT))+'.',
              'level':level,'used_in':['Q5' if run['baseline']=='A' else 'Q6','Q7'],'count_toward_minimum':False})
        path=ROOT/'evidence/baseline'/(run['baseline']+'-'+run['case_id']+'.sources.json')
        rows, failures=sources[source_start:],excluded[excluded_start:]
        path.write_text(json.dumps({'schema_version':1,'case_id':run['case_id'],'baseline':run['baseline'],'sources':rows,'excluded':failures},ensure_ascii=False,indent=2)+'\n')
        shards.append({'path':str(path.relative_to(ROOT)),'source_count':len(rows),'excluded_count':len(failures),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    (ROOT/'evidence/baseline/sources.json').write_text(json.dumps({'schema_version':2,'sources':[],'excluded':[],'source_shards':shards,'source_count':len(sources),'excluded_count':len(excluded),'format_note':'All complete source rows and excluded attempts are preserved in the hash-checked per-run source_shards. The root sources.json carries the same manifest; counts are read records, not independent documents.'},ensure_ascii=False,indent=2)+'\n')
    (ROOT/'SEARCH_LOG.json').write_text(json.dumps({'schema_version':1,'selection_methodology_counterexample_logs':searches,'baseline_runs':run_indexes,'limits':'Exact recorded queries are preserved. Embedded source logs have heterogeneous schemas; a query string is not proof that a source body was read. Counterexample outcome coding is in COUNTEREXAMPLES.md.'},ensure_ascii=False,separators=(',',':'))+'\n')
    print(json.dumps({'source_read_records':len(sources),'excluded_attempts':len(excluded),'baseline_runs':len(run_indexes),'source_logs':len(searches)}))

if __name__=='__main__':main()
