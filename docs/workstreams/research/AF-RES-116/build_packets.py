"""Freeze unchanged blinded author's hints and expand the 18 prespecified packets."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
BASE=Path(__file__).resolve().parent
def main():
    authored=[json.loads(x) for x in (BASE/'authoring/draft-packets.jsonl').read_text().splitlines()]
    cases={x['case_id']:x for x in json.loads((BASE/'cases.json').read_text())['cases']}
    spans={'P1':[[6,37],[24,37],[6,22],[45,45],None], 'P2':[[1,1],[1,9],[1,1],[3,9],None], 'P3':[[21,23],[23,27],[27,27],None], 'I1':[[15,24],[15,15],[24,24],[15,24]], 'I2':[[15,23],[17,23],[15,17],[15,23]], 'I3':[[15,15],[15,39],[15,39],[39,39]]}
    packets=[];maps=[];checks=[]
    (BASE/'inputs').mkdir(exist_ok=True)
    for a in authored:
        cid=a['case_id'];c=cases[cid]
        assert a['common_request']==c['common_request']
        assert 50<=len(a['B_hint'])==len(a['C_hint'])<=100
        assert not any('http' in a[k] for k in ['B_hint','C_hint'])
        assert a['C_new_label'] not in c['common_request']
        assert a['C_new_label'] in a['C_hint']
        body=next(x for x in json.loads((BASE/c['original_body_snapshot_path']).read_text()) if x['number']==c['number'])['body'].splitlines()
        for i,m in enumerate(a['B_phrase_map']):
            sp=spans[cid][i]
            maps.append({'case_id':cid,**m,'original_url':c['original_url'],'original_lines':sp,'original_text':'\n'.join(body[sp[0]-1:sp[1]]) if sp else None,'basis':'original condition/structure restatement; confirmation wording is protocol wrapper' if sp else 'neutral confirmation/exception-check instruction; no additional substantive condition','mapper':'root before gold/manual semantic reading'})
        for condition in c['condition_order']:
            pid=f'r{len(packets)+1:02d}';hint=a[condition+'_hint']
            text=f"요청: {c['common_request']}\n문서 판: {a['doc_version']}\n시작 URL: {c['start_url']}\n"+(f'안내: {hint}\n' if hint else '')
            p={'packet_id':pid,'case_id':cid,'layer':'natural','condition':condition,'case_condition_order':c['condition_order'],'common_request':c['common_request'],'start_url':c['start_url'],'start_doc_id':a['start_doc_id'],'document_version':a['doc_version'],'version_explicit':a['doc_version_explicit_in_request'],'hint':hint,'hint_codepoints':len(hint),'hint_utf8_bytes':len(hint.encode()),'full_packet_text':text,'packet_codepoints':len(text),'packet_utf8_bytes':len(text.encode()),'request_codepoints':len(c['common_request']),'request_utf8_bytes':len(c['common_request'].encode()),'new_label':a['C_new_label'] if condition=='C' else None,'new_label_source':a['C_label_source'] if condition=='C' else None,'B_original_phrase_map_ids':[f'{cid}:{i+1}' for i in range(len(a['B_phrase_map']))] if condition=='B' else [],'author_selected_utc':a['selected_utc'],'author_draft_sha256':hashlib.sha256((BASE/'authoring/draft-packets.jsonl').read_bytes()).hexdigest(),'corp_sha256':'a2507268ef20cc0b9dc55b351b44e7973961e352f17f86dbb3b2b01dc3127b2d','fresh_reader_status':'not_started'}
            packets.append(p)
            recipient={k:p[k] for k in ['packet_id','common_request','start_url','start_doc_id','document_version','hint','full_packet_text']}
            (BASE/'inputs'/f'{pid}.json').write_text(json.dumps(recipient,ensure_ascii=False,indent=2)+'\n')
        checks.append({'case_id':cid,'B_codepoints':len(a['B_hint']),'C_codepoints':len(a['C_hint']),'B_utf8_bytes':len(a['B_hint'].encode()),'C_utf8_bytes':len(a['C_hint'].encode()),'C_label':a['C_new_label'],'duplicate_label_ambiguity_preserved':cid=='P2'})
    (BASE/'packets.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in packets))
    (BASE/'authoring/phrase-provenance.jsonl').write_text(''.join(json.dumps({'map_id':f"{x['case_id']}:{sum(1 for y in maps[:i+1] if y['case_id']==x['case_id'])}",**x},ensure_ascii=False)+'\n' for i,x in enumerate(maps)))
    (BASE/'authoring/packet-check.json').write_text(json.dumps({'checked_utc':datetime.now(timezone.utc).isoformat(),'checks':checks,'packets':len(packets),'planned_stage_slots':54,'source_line_mapping':'semantic original-span map plus separately identified neutral study wrapper; not exact English/Korean lexical equality','no_gold_or_witness_seen_by_author':True,'no_gold_or_witness_seen_by_mapper':True,'status':'passed'},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'packets':len(packets),'slots':54,'checks':checks},ensure_ascii=False))
if __name__=='__main__':main()
