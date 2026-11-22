"""Normalize collector metadata without adding observations or decisions."""
import hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
refs={r['ref_id']:r for r in [json.loads(x) for x in (P/'references.jsonl').read_text().splitlines()]}
rows=[]
for collector in ('gnu','bioc'):
    source_file=P/'collectors'/collector/'evidence-components.jsonl'
    for line in source_file.read_text().splitlines():
        c=json.loads(line);rid=c.get('ref_id',c.get('reference_id'));r=refs[rid]
        row={'ref_id':rid,'collector':collector,'collector_component_path':str(source_file.relative_to(P)),'collector_row_sha256':sha(line)}
        for layer in ('N','H'):
            x=c[layer]
            if collector=='gnu':
                raw=x['text'];assert sha(raw)==x['text_sha256']
                if layer=='N':
                    request=x['original_request']
                    spans=x['excerpts']
                    meta={'observed_utc':request['started_utc'],'requested_url':request['url'],'HTTP_status_chain':[a['status'] for a in request['redirect_chain']]+[request['status']],'arrival_url':request['final_url'],'required_section_url':x['current_section_url'],'original_fragment':x['original_fragment'],'original_fragment_exists':x['original_fragment_exists'],'source_ids':x['source_ids']}
                    facts={'original_get_attempt_id':request['attempt_id'],'extra_fetch_attempt_ids':x.get('additional_request_ids',[]),'http_status':request['status'],'redirect_chain':request['redirect_chain'],'final_url':request['final_url'],'queried_utc':request['started_utc'],'current_section_url':x['current_section_url'],'source_contains_history':x.get('source_contains_history',False),'card_contains_history':x.get('text_history_overlap',False)}
                else:
                    spans=x['excerpts'];meta={'publisher_documents':x['historical_documents'],'source_ids':x['source_ids']}
                    facts={'source_contains_history':True,'contains_present_observation':x.get('contains_current_observation',False),'contains_collector_recommendation':x.get('contains_collector_recommendation',False),'contains_answer_key':x.get('contains_answer_key',False)}
                empty=bool(x.get('empty_reason'))
            else:
                assert sha(x['text'])==x['sha256']
                raw=x['raw_excerpt'];spans=x['spans']
                if layer=='N':
                    section_urls=list(dict.fromkeys(s['url'] for s in spans))
                    meta={'observed_utc':x['queried_utc'],'requested_url':r['original_href'],'HTTP_status_chain':[a['status'] for a in x['redirect_chain']]+[x['http_status']],'arrival_url':x['final_url'],'required_section_urls':section_urls,'observed_edition':x['edition'],'original_fragment':x.get('original_fragment'),'fragment_observation':x.get('fragment_check'),'source_ids':x['source_ids']}
                    direct_history=any(k in raw for k in ['up-to-date release','for Bioconductor 3.1'])
                    facts={'original_get_attempt_id':x['original_get_attempt_id'],'extra_fetch_attempt_ids':x.get('extra_fetch_attempt_ids',[]),'http_status':x['http_status'],'redirect_chain':x['redirect_chain'],'final_url':x['final_url'],'queried_utc':x['queried_utc'],'current_section_url':section_urls[-1] if section_urls else x['final_url'],'source_contains_history':x.get('overlap_history',False),'card_contains_history':direct_history}
                else:
                    meta={'publisher_documents':[{'url':x['archive_url'],'edition_or_document':x['edition'],'event_or_publication_time':x['publisher_event_date'],'member':x['member']}],'source_ids':x['source_ids']}
                    facts={'fetch_attempt_id':x.get('fetch_attempt_id'),'source_contains_history':True,'contains_present_observation':x.get('contains_present_observation',False),'contains_collector_recommendation':x.get('contains_collector_recommendation',False),'contains_answer_key':x.get('contains_answer_key',False),'shared_exact_excerpt_with_N':x.get('shared_exact_excerpt_with_N',False),'physical_fetch_reused_from_original_sampling':x.get('physical_fetch_reused_from_original_sampling',False)}
                empty=x.get('empty_evidence',False)
            assert len(raw)<=1600,(rid,layer,len(raw))
            text=json.dumps(meta,ensure_ascii=False,indent=2)+'\n\nPublisher excerpt(s):\n'+raw
            row[layer]={'metadata':meta,'text':text,'sha256':sha(text),'utf8_bytes':len(text.encode()),'codepoints':len(text),'raw_excerpt':raw,'raw_sha256':sha(raw),'raw_codepoints':len(raw),'raw_utf8_bytes':len(raw.encode()),'source_ids':x['source_ids'],'spans':spans,'empty_evidence':empty,**facts}
        rows.append(row)
(P/'components.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows))
print(json.dumps({'cases':len(rows),'components':len(rows)*2,'no_adjudication_fields_added':True}))
