"""Build exposure and frozen-prediction tables from immutable reader outputs."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET_SEAL = '9518c3dccbd21cda72cec715afe47eebd4dba543'
SEALS = {'A':'7c1df93b11e06ca8b7f44ac5b7ff996879aebd09', 'B':'7bc2d1f84c04b47711d72e7c110b8f927d97f4ad'}
NORMALIZED = {'SC':'producer-scoped verified full-content provenance; legacy refusal',
              'MS':'local excerpt-boundary deselection; existing links and undo retained',
              'SG':'operation-local (original document,fragment) relocation plan; reject ambiguous same-document IDs'}

def write_csv(path, rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def json_text(x):
    return json.dumps(x,ensure_ascii=False,separators=(',',':'))

def main():
    rows=[]
    for brief in ('SC','MS','SG'):
        common=ROOT/f'packets/{brief}-common.json'
        for view in ('A','B'):
            packet=ROOT/f'packets/{brief}-{view}.json'
            p=json.loads(packet.read_text());rpath=ROOT/f'readers/{brief}-{view}.json';r=json.loads(rpath.read_text())
            rows.append(dict(brief_id=brief,view=view,source_work_id=p['work_id'],source_version=p['version'],
                             source_sections=json_text(p['sections']),source_urls=json_text(p['urls']),language=p['language'],
                             actual_excerpt_characters=len(p['excerpt']),character_ceiling=2000,
                             actual_packet_characters=len(packet.read_text()),common_characters=len(common.read_text()),
                             additional_reader_source_opens=len(r['extra_source_opens']),
                             source_access='compiler recovered offered excerpt; reader extra opens forbidden',
                             compiler_failures='see SOURCES.jsonl; not extra reader exposure',
                             packet_sha256=hashlib.sha256(packet.read_bytes()).hexdigest(),
                             common_sha256=hashlib.sha256(common.read_bytes()).hexdigest(),
                             reader_file=str(rpath.relative_to(ROOT)),reader_sha256=hashlib.sha256(rpath.read_bytes()).hexdigest(),
                             candidate_ids=json_text([c['id'] for c in r['candidates']]),
                             selected_id=r['chosen_candidate']['id'],normalized_selected_mechanism=NORMALIZED[brief],
                             selected_utc=r['completed_utc'],packet_seal_sha=PACKET_SEAL,choice_seal_sha=SEALS[view],
                             fresh_task_context=True,other_view_opened=False,target_outcome_opened=False,
                             pretraining_familiarity='unmeasurable',causal_effect_eligible=False,
                             independent_effect_denominator_contribution=0,
                             limitation='same model family; unequal actual character exposure; compiler pre-exposure; role prompts not proven byte-identical; technical comparison only'))
    write_csv(ROOT/'VIEWS.csv',rows)
    costs=[]
    for row in rows:
        costs.append(dict(id='READ-'+row['brief_id']+'-'+row['view'],actor='isolated_'+row['brief_id']+'_'+row['view'],
                          phase='sealed_first_pass',unit='local authorized file opens',count=2,count_status='reported by reader',
                          excerpt_characters=row['actual_excerpt_characters'],packet_characters=row['actual_packet_characters'],
                          common_characters=row['common_characters'],additional_work='proposal JSON; >=2 candidates; 3 predictions',
                          elapsed_seconds='',elapsed_status='not instrumented; completion UTC is not active work duration',
                          money='no paid API requested; tool billing unavailable',
                          receipt=row['reader_file'],limitation='No claim about developer minutes or effort saved.'))
    for id_,actor,n,receipt,note in [
        ('RECRUIT-SC','recruit_shotcut',29,'recruitment/shotcut/source_notes.json','16 connector calls +13 public GETs; overlapping request durations not wall time'),
        ('RECRUIT-MS','recruit_musescore',34,'recruitment/musescore/REPORT.md','includes failed query/type/version/tracker attempts'),
        ('RECRUIT-SG','recruit_sigil',33,'recruitment/sigil/report.md','includes2 failed exact-query calls; root exact replay separate'),
        ('SG-EXACT-REPLAY','root',2,'evidence/sigil-exact-query-replay.json','canonical untyped queries; do not count as new works'),
        ('ROOT-PRIMARY-DOCS','root',22,'reading/receipts.jsonl','22 successful HTTP retrievals,18 named works; fetched text is not whole-work reading; 3 added counterexample works are postseal compiler reads'),
        ('ROOT-GUIDE-PIN','root',2,'reading/sigil-guide-history.json;reading/sigil-guide-tree.json','retained history/tree receipts only; earlier repeated tree retrieval not fully cost-instrumented'),
        ('POST-SC','root',8,'postseal/shotcut/fetch-receipts.json;postseal/shotcut/source-receipts.json','3 metadata/comment endpoints +5 source files; same code/request lineages'),
    ]:
        costs.append(dict(id=id_,actor=actor,phase='retrieval',unit='external read requests',count=n,
                          count_status='recorded component; global total is a lower bound',excerpt_characters='',packet_characters='',common_characters='',
                          additional_work=note,elapsed_seconds='',elapsed_status='not comparable across actors; partly parallel',
                          money='no paid API requested; tool billing unavailable',receipt=receipt,
                          limitation='Discovery web calls and all compiler rereads were not exhaustively instrumented; do not infer total time or equal actual cost.'))
    costs.append(dict(id='ROOT-UNINSTRUMENTED',actor='root',phase='discovery_and_reread',unit='external/local reads',count='',count_status='UNKNOWN',
                      excerpt_characters='',packet_characters='',common_characters='',additional_work='search snippets, failed web routes, repeated local code reads, Git transport retries',
                      elapsed_seconds='',elapsed_status='UNKNOWN',money='no paid API requested; billing unavailable',receipt='evidence/EXPOSURE.md',
                      limitation='Known cost-register gap; protocol supports equal ceilings, not identical realized budget.'))
    write_csv(ROOT/'COSTS.csv',costs)
    print(json.dumps({'views':len(rows),'reader_file_opens':12,'extra_reader_opens':0,
                      'changed_core_choices':0,'comparison_denominator':3,'causal_effect_denominator':0,
                      'recorded_external_component_lower_bound':sum(int(x['count']) for x in costs if x['unit']=='external read requests')}))

if __name__=='__main__':main()
