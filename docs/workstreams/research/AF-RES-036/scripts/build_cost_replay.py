"""Conditional second-visit simulation from first-visit measured units, never a live benchmark."""
import collections,csv,hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def rows(name):return [json.loads(x) for x in (P/name).read_text().splitlines() if x.strip()]
def writej(name,v):(P/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def writecsv(name,rs):
    keys=list(dict.fromkeys(k for r in rs for k in r))
    with (P/name).open('w',newline='') as f:
        w=csv.DictWriter(f,keys,lineterminator='\n');w.writeheader();w.writerows(rs)
A={a['attempt_id']:a for a in rows('attempts.jsonl') if a.get('operation')=='GET'}
C={c['ref_id']:c for c in rows('components.jsonl')}
R={r['ref_id']:r for r in rows('references.jsonl')}
PK={(p['ref_id'],p['view']):p for p in rows('packets.jsonl')}
RET={r['ref_id']:r for r in json.loads((P/'evidence/retention-summary.json').read_text())['record_units']} if (P/'evidence/retention-summary.json').exists() else {}
# Original href is always tested. Navigation-only TOC and an uninformative exploratory
# S4Vectors PDF are omitted from an oracle replay; the real exploration remains in costs.csv.
N={'G01':['G-NGET001','G-NGET007','G-NGET009'],
   'G02':['G-NGET002'],'G03':['G-NGET003','G-NGET007','G-NGET009'],
   'G04':['G-NGET004'],'G05':['G-NGET005'],'G06':['G-NGET006'],
   'R01':['N-R01-ORIGINAL'],'R02':['N-R02-ORIGINAL'],
   'R03':['N-R03-ORIGINAL','N-R03-SOURCE'],
   'R04':['N-R04-ORIGINAL','N-R04-MANUAL'],
   'R05':['N-R05-ORIGINAL','N-R05-VIGNETTE'],'R06':['N-R06-ORIGINAL']}
H={'G01':['G-HGET001'],'G02':['G-HGET002','G-HGET005'],
   'G03':['G-HGET006'],'G04':['G-HGET006'],'G05':['G-HGET003'],
   'G06':['G-HGET011'],'R01':['H-R01-ARCHIVE'],'R02':['H-R02-ARCHIVE'],
   'R03':['R-EARLY-S4Vectors'],'R04':['R-EARLY-DESeq2'],
   'R05':['R-EARLY-SingleCellExperiment'],'R06':['R-EARLY-scater']}
def units(ids):
    aa=[A[k] for k in dict.fromkeys(ids)]
    return {'operations':len(aa),'http_exchanges':sum(1+len(a.get('redirect_chain',[])) for a in aa),
            'body_bytes':sum(a.get('received_body_bytes') or 0 for a in aa),
            'observed_failure_responses':sum(bool(a.get('error')) or (a.get('status') or 0)>=400 for a in aa),
            'first_visit_elapsed_proxy':round(sum(a.get('elapsed_seconds') or 0 for a in aa),6)}
out=[];case_units=[]
for rid in sorted(C):
    base=PK[(rid,'B')]['parts']['B']
    bbytes=len(base.encode()) if isinstance(base,str) else C[rid].get('B',{}).get('utf8_bytes')
    if bbytes is None: bbytes=PK[(rid,'B')]['part_utf8_bytes']['B']
    n,h=units(N[rid]),units(H[rid])
    case_units.append({'ref_id':rid,'base_acquisition_attempt_id':R[rid]['fetch_attempt_id'],
        'N_attempt_ids':N[rid],'H_attempt_ids':H[rid],'N_measured_units':n,'H_measured_units':h,
        'B_text_bytes':bbytes,'N_text_bytes':C[rid]['N']['utf8_bytes'],'H_text_bytes':C[rid]['H']['utf8_bytes'],
        'N_body_codepoints':C[rid]['N']['raw_codepoints'],'H_body_codepoints':C[rid]['H']['raw_codepoints']})
    for task in ['current_decision_N','reconstruct_evidence_body_NH']:
        for config in ['C1','C2']:
            ids=N[rid]+(H[rid] if task=='reconstruct_evidence_body_NH' and config=='C1' else [])
            u=units(ids)
            out.append({'cost_id':f'SIM-{rid}-{task}-{config}','ref_ids':rid,'collector':'root_simulation',
                'round':2,'configuration':config,'task':task,'actual_requests':0,
                'modeled_request_operations':u['operations'],'modeled_http_exchanges':u['http_exchanges'],
                'modeled_body_bytes':u['body_bytes'],'modeled_failures_if_status_unchanged':u['observed_failure_responses'],
                'received_body_bytes':'unmeasured_second_visit','temporary_stored_bytes':'unmeasured_second_visit',
                'durable_stored_bytes':RET.get(rid,{}).get('serialized',{}).get('C1_B_presealed' if config=='C1' else 'C2_BH_with_provenance',{}).get('bytes','not_yet_materialized'),
                'modeled_logical_retained_text_bytes':bbytes+(C[rid]['H']['utf8_bytes'] if config=='C2' else 0),
                'concrete_storage_example':'retention-options.jsonl; serialized B or B/H plus exact locator/hash provenance; service overhead unmeasured',
                'logical_text_bytes_scope':'one logical B text plus exact H text; excludes provenance outside the visible card and JSON containers',
                'durable_bytes_scope':'concrete serialized per-case retention record including locator/hash provenance; excludes database/storage-engine overhead and Git compression',
                'elapsed_seconds':'unmeasured_second_visit','first_visit_elapsed_proxy_seconds':u['first_visit_elapsed_proxy'],
                'request_operation_budget':2,'timeout_per_operation_seconds':30,
                'operation_count_within_budget':u['operations']<=2,
                'strict_exchange_count_within_budget':u['http_exchanges']<=2,
                'wall_time_budget_success':'unmeasured; count feasibility only',
                'not_a_minimum_task_cost':'reconstructs the sealed N evidence content; a narrower sufficient section could require fewer requests (not experimentally compared)',
                'unit_attempt_ids':'|'.join(dict.fromkeys(ids)),
                'local_H_reads':int(config=='C2' and task=='reconstruct_evidence_body_NH'),
                'local_H_read_bytes':C[rid]['H']['utf8_bytes'] if config=='C2' and task=='reconstruct_evidence_body_NH' else 0,
                'local_H_read_elapsed_seconds':'unmeasured',
                'original_packet_hash_restored':False,
                'measurement':'SIMULATION, first-observation body size and status held constant; second visit not executed',
                'assumptions':'oracle knows exact N/H source URLs and extraction positions; source bodies unchanged; no rediscovery cost; new current-query UTC differs from original packet',
                'unmeasured':'second-response status/bytes/time; locator rediscovery; human/model reading; service operation cost; C0 first discovery'})
writecsv('replay-costs.csv',out)
writej('evidence/replay-units.json',case_units)
summaries=[]
for task in ['current_decision_N','reconstruct_evidence_body_NH']:
    for config in ['C1','C2']:
        rs=[r for r in out if r['task']==task and r['configuration']==config]
        ids=[a for r in rs for a in r['unit_attempt_ids'].split('|')]
        physical=units(ids)
        summaries.append({'task':task,'configuration':config,'cases':len(rs),
            'logical_operations':sum(r['modeled_request_operations'] for r in rs),
            'logical_http_exchanges':sum(r['modeled_http_exchanges'] for r in rs),
            'logical_body_bytes':sum(r['modeled_body_bytes'] for r in rs),
            'shared_source_physical_lower_bound':physical,
            'operation_count_feasible_cases':sum(r['operation_count_within_budget'] for r in rs),
            'strict_exchange_count_feasible_cases':sum(r['strict_exchange_count_within_budget'] for r in rs),
            'operation_budget_fail_ids':[r['ref_ids'] for r in rs if not r['operation_count_within_budget']],
            'strict_exchange_budget_fail_ids':[r['ref_ids'] for r in rs if not r['strict_exchange_count_within_budget']],
            'logical_retained_text_bytes':sum(r['modeled_logical_retained_text_bytes'] for r in rs),
            'concrete_serialized_example_bytes':sum(r['durable_stored_bytes'] for r in rs) if all(isinstance(r['durable_stored_bytes'],int) for r in rs) else None,
            'local_H_reads':sum(r['local_H_reads'] for r in rs),'second_visit_executed':False})
writej('evidence/replay-summary.json',summaries)
print(json.dumps(summaries,ensure_ascii=False))
