"""Recalculate the AF-RES-100 matrix and verify all byte/reading boundaries.

No network calls and no external programs. Add --initial to audit reader outputs
before assembling the final judgments.jsonl. This verifies record integrity,
not the truth of semantic judgments or original-user execution.
"""
from pathlib import Path
from collections import Counter, defaultdict
import argparse
import hashlib
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parent

def jl(p):
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]

def merge(xs):
    out = []
    for a, b in sorted(xs):
        if out and a <= out[-1][1]: out[-1][1] = max(out[-1][1], b)
        else: out.append([a,b])
    return out

def covered(a,b,xs):
    return any(x <= a <= b <= y for x,y in merge(xs))

def run(initial=False):
    errors=[]; warnings=[]; packets=jl(ROOT/'packets.jsonl')
    proto=json.loads((ROOT/'protocol.json').read_text()); byid={x['packet_id']:x for x in packets}
    expected={(c['case_id'],p,m) for c in proto['cases'] for p in ['A','B'] for m in ['F','S']}
    actual={(p['case_id'],p['policy'],p['mode']) for p in packets}
    if actual!=expected or len(packets)!=32 or len(byid)!=32: errors.append('matrix positions mismatch')
    if any(len(p['slots'])!=4 for p in packets): errors.append('packet lacks four file positions')
    protocol_sha=hashlib.sha256((ROOT/'protocol.json').read_bytes()).hexdigest()
    manifest_sha=hashlib.sha256((ROOT/'corpus-files.jsonl').read_bytes()).hexdigest()
    allocation=defaultdict(list)
    for f in sorted((ROOT/'evidence/assignments').glob('*.json')):
        d=json.loads(f.read_text()); seen=[]
        for r in d['packets']:
            allocation[r['packet_id']].append(d['reader_id']); seen.append(r['question_id'])
        if len(seen)!=8 or len(set(seen))!=8: errors.append('reader allocation repeats/misses question: '+f.name)
    bodies={}; access={}; costs={}; unique_chars={}
    for p in packets:
        pid=p['packet_id']
        if p['protocol_sha256']!=protocol_sha or p['corpus_manifest_sha256']!=manifest_sha: errors.append(pid+' frozen input hash mismatch')
        if len(allocation[pid])!=1: errors.append(pid+' allocation not unique')
        if p['mode']=='S' and p['total_exposed_chars']>4800: errors.append(pid+' short budget exceeds4800')
        log=ROOT/'evidence/packet-access'/f'{pid}.jsonl'; ev=jl(log) if log.exists() else []
        access[pid]=ev; charged=sum(e.get('charged_attempts',0) for e in ev)
        costs[pid]={'charged':charged,'section_moves':sum(e.get('event')=='section_navigation' and e.get('status')=='success' for e in ev),
                    'displayed_chars':sum(e.get('displayed_chars',0) for e in ev),
                    'denied_actions':sum(e.get('event')=='denied_action' for e in ev)}
        if charged!=4: errors.append(f'{pid} charged attempts {charged}, expected4')
        running_charge=0
        for slot_no in range(1,5):
            opened=[e for e in ev if e['slot']==slot_no and e.get('event')=='source_open']
            if len(opened)!=1 or sum(e.get('charged_attempts',0) for e in opened)!=1:
                errors.append(f'{pid} slot{slot_no} must have one charged initial access')
        for e in ev:
            running_charge+=e.get('charged_attempts',0)
            if e.get('charged_total')!=running_charge: errors.append(pid+' cumulative charge mismatch')
        uniques=defaultdict(list)
        for s in p['slots']:
            if s['empty']: continue
            raw=(ROOT/s['cached_body']).read_bytes(); text=raw.decode('utf-8'); bodies[(pid,s['slot'])]=(raw,text)
            a,b=s['char_start'],s['char_end']; ba,bb=s['byte_start'],s['byte_end']
            if hashlib.sha256(raw).hexdigest()!=s['sha256']:errors.append(pid+' source hash mismatch')
            if hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!=s['git_blob_sha']:
                errors.append(pid+' source git blob mismatch')
            if p['mode']=='S' and b-a>1200:errors.append(pid+' short slot exceeds1200')
            if (len(text[:a].encode()),len(text[:b].encode()))!=(ba,bb):errors.append(pid+' exposure char/byte mismatch')
            if raw[ba:bb]!=text[a:b].encode():errors.append(pid+' exposure bytes mismatch')
            if hashlib.sha256(raw[ba:bb]).hexdigest()!=s['exposed_sha256']:errors.append(pid+' exposed hash mismatch')
        for e in ev:
            slot=next(s for s in p['slots'] if s['slot']==e['slot'])
            for r in e.get('displayed_segments',[]):
                if slot['empty']: errors.append(pid+' displayed empty slot');continue
                raw,text=bodies[(pid,e['slot'])]; a,b=r['char_start'],r['char_end'];ba,bb=r['byte_start'],r['byte_end']
                if not (slot['char_start']<=a<=b<=slot['char_end']):errors.append(pid+' displayed outside packet')
                if (len(text[:a].encode()),len(text[:b].encode()))!=(ba,bb):errors.append(pid+' read char/byte mismatch')
                if hashlib.sha256(raw[ba:bb]).hexdigest()!=r['segment_sha256']:errors.append(pid+' read segment hash mismatch')
                if r.get('displayed_chars')!=b-a or r.get('displayed_utf8_bytes')!=bb-ba:
                    errors.append(pid+' displayed length arithmetic mismatch')
                uniques[e['file_id']].append([a,b])
            if e.get('displayed_chars',0)!=sum(r['char_end']-r['char_start'] for r in e.get('displayed_segments',[])):
                errors.append(pid+' event displayed chars mismatch')
        unique_chars[pid]=sum(b-a for rs in uniques.values() for a,b in merge(rs))
        if p['mode']=='S':
            for n in range(1,5):
                displayed=[e for e in ev if e['slot']==n and e.get('displayed_segments')]
                if len(displayed)>1:errors.append(pid+' repeated restricted snippet')
            if costs[pid]['displayed_chars']>4800:errors.append(pid+' total S displayed exceeds4800')
    for c in proto['cases']:
        for policy in ['A','B']:
            f=next(p for p in packets if (p['case_id'],p['policy'],p['mode'])==(c['case_id'],policy,'F'))
            s=next(p for p in packets if (p['case_id'],p['policy'],p['mode'])==(c['case_id'],policy,'S'))
            if [x['file_id'] for x in f['slots']]!=[x['file_id'] for x in s['slots']]:errors.append(c['case_id']+' F/S candidates differ')
        if c['stratum']=='control':
            for mode in ['F','S']:
                a=next(p for p in packets if (p['case_id'],p['policy'],p['mode'])==(c['case_id'],'A',mode))
                b=next(p for p in packets if (p['case_id'],p['policy'],p['mode'])==(c['case_id'],'B',mode))
                if [(s['file_id'],s['char_start'],s['char_end']) for s in a['slots']]!=[(s['file_id'],s['char_start'],s['char_end']) for s in b['slots']]:errors.append(c['case_id']+' control A/B differs')
    judgments=[]
    if initial:
        for f in sorted((ROOT/'evidence/readers').glob('R*/judgments.jsonl')): judgments+=jl(f)
    elif (ROOT/'judgments.jsonl').exists():judgments=jl(ROOT/'judgments.jsonl')
    if len(judgments)!=32:errors.append(f'judgments {len(judgments)}, expected32')
    if len({j['packet_id'] for j in judgments})!=len(judgments):errors.append('duplicate judgment packet')
    for j in judgments:
        pid=j['packet_id'];p=byid[pid]
        if j['reader_id'] not in allocation[pid]:errors.append(pid+' reader allocation mismatch')
        required={c['id'] for c in p['conditions']}
        if {c['id'] for c in j['conditions']}!=required:errors.append(pid+' condition set mismatch')
        if j.get('same_question_previous_exposure'):errors.append(pid+' same-question crossover')
        if j.get('contamination'):warnings.append(pid+' declared contamination '+str(j['contamination']))
        if j.get('tool_output_truncations'):warnings.append(pid+' declared output truncation '+str(j['tool_output_truncations']))
        all_supported=all(c['status']=='supported' for c in j['conditions'])
        if j['complete'] and not all_supported:errors.append(pid+' complete but unsupported condition')
        for c in j['conditions']:
            if c['status'] not in ['supported','refuted','partial','unknown']:errors.append(pid+' unknown status')
            if c['status']=='supported' and not c.get('citations'):errors.append(pid+' supported condition without citation')
            for cite in c.get('citations',[]):
                s=next((s for s in p['slots'] if s['slot']==cite['slot']),None)
                if not s or s['empty'] or cite['file_id']!=s['file_id'] or cite['url']!=s['url']:errors.append(pid+' citation source mismatch');continue
                raw,text=bodies[(pid,s['slot'])];a,b=cite['char_start'],cite['char_end'];ba,bb=cite['byte_start'],cite['byte_end']
                if not (s['char_start']<=a<b<=s['char_end']):errors.append(pid+' citation outside packet')
                if (len(text[:a].encode()),len(text[:b].encode()))!=(ba,bb):errors.append(pid+' citation char/byte mismatch')
                initial_cutoff=datetime.fromisoformat(j.get('initial_judgment_recorded_utc',j['recorded_utc']))
                shown=[(v['char_start'],v['char_end']) for e in access[pid]
                       if e['slot']==s['slot'] and e.get('status')=='success'
                       and datetime.fromisoformat(e['finished_utc'])<=initial_cutoff
                       for v in e.get('displayed_segments',[])]
                audited=cite.get('audit_added',False)
                if not covered(a,b,shown) and not audited:errors.append(pid+' citation not displayed to reader')
                if audited:
                    if initial: errors.append(pid+' initial citation marked audit-added')
                    else:
                        audit=ROOT/'evidence/audit/availability-access.jsonl';aa=jl(audit) if audit.exists() else []
                        audit_cutoff=datetime.fromisoformat(j.get('evidence_availability',{}).get('recorded_utc',j['recorded_utc']))
                        shown_a=[(v['char_start'],v['char_end']) for e in aa if e['packet_id']==pid and e['slot']==s['slot']
                                 and datetime.fromisoformat(e['recorded_utc'])<=audit_cutoff for v in e.get('segments',[])]
                        if not covered(a,b,shown_a):errors.append(pid+' audit citation not displayed to auditor')
    byj={j['packet_id']:j for j in judgments};summary={}
    for mode in ['F','S']:
        for stratum in ['all','boundary','control']:
            counts=Counter(); positions=0
            for c in proto['cases']:
                if stratum!='all' and c['stratum']!=stratum:continue
                positions+=1
                pa=next(p for p in packets if (p['case_id'],p['policy'],p['mode'])==(c['case_id'],'A',mode));pb=next(p for p in packets if (p['case_id'],p['policy'],p['mode'])==(c['case_id'],'B',mode))
                if not c.get('stable_adjacent_resolved',True):counts['incomparable']+=1;continue
                if pa['packet_id'] not in byj or pb['packet_id'] not in byj:counts['pending']+=1;continue
                a,b=byj[pa['packet_id']]['complete'],byj[pb['packet_id']]['complete']
                counts['both' if a and b else 'A_only' if a else 'B_only' if b else 'neither']+=1
            summary[f'{mode}/{stratum}']={'positions':positions,**{k:counts[k] for k in ['A_only','B_only','both','neither','incomparable','pending']},'comparable':sum(counts[k] for k in ['A_only','B_only','both','neither'])}
    return {'status':'PASS' if not errors else 'FAIL','stage':'initial' if initial else 'audited','errors':errors,'warnings':warnings,'packets':len(packets),'file_positions':sum(len(p['slots']) for p in packets),'empty_positions':sum(s['empty'] for p in packets for s in p['slots']),'judgments':len(judgments),'comparison_counts':summary,'costs':{p:{**v,'unique_displayed_chars':unique_chars[p]} for p,v in costs.items()},'limits':'Record/boundary consistency only; semantic validity, reader training memory and original-user execution are not proven.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--initial',action='store_true');ap.add_argument('--output');a=ap.parse_args();result=run(a.initial)
    text=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if a.output:
        dest=(ROOT/a.output).resolve();assert dest.is_relative_to(ROOT.resolve());dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text)
    print(text);raise SystemExit(0 if result['status']=='PASS' else 1)
