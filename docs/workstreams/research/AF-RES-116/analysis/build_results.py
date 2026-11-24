#!/usr/bin/env python3
"""Join immutable exposures, masked judgments and reference intervals.

This is descriptive accounting, not a treatment-effect estimator. It does not
edit any answer, judge output, packet, original request or reference definition.
"""
from pathlib import Path
from collections import Counter, defaultdict
import argparse, csv, hashlib, io, json, sys, re, posixpath

OWN=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(OWN/'analysis'))
from collect_trials import visible_unions

ORDER=['P1','P2','P3','I1','I2','I3']
FLAGS=['full_supported','justified_hold','partial_reconstruction','label_only','dangerous_certainty','counterexample_found']
GRADE_KO={'full_supported':'완전 근거','justified_hold':'정당한 보류','partial_reconstruction':'부분 재구성+보류','label_only':'라벨만 맞음','dangerous_certainty':'위험한 확정','unsupported_or_wrong':'근거 없는/틀린 답'}
def jl(name):return [json.loads(s) for s in (OWN/name).read_text().splitlines() if s.strip()]
def js(name):return json.loads((OWN/name).read_text())
def compact(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def csv_text(rows):
    s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader()
    for r in rows:w.writerow({k:compact(v) if isinstance(v,(dict,list)) else v for k,v in r.items()})
    return s.getvalue()
def cell(s):return str(s).replace('|','\\|').replace('\n','<br>')
def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(cell(c) for c in r)+' |' for r in rows])+'\n'
def covered(interval,unions):
    return any(a<=interval['start'] and interval['end']<=b for a,b in unions.get(interval['doc_id'],[]))
def mode_covered(mode,views):
    union=visible_unions(views)
    return any(alt and all(covered(x,union) for x in alt) for alt in mode['alternatives'])

def build():
    packets=jl('packets.jsonl');pkt={p['packet_id']:p for p in packets}
    trails=jl('trails.jsonl');trials=js('analysis/trial-summary.json')
    mapping={r['masked_id']:r for r in js('evaluation/masking-map.json')}
    jud={};judge_inputs=[]
    for family in ['pandoc','imagemagick']:
        path=f'evaluation/judgments-{family}.jsonl';judge_inputs.append(path)
        for r in jl(path):
            m=mapping[r['masked_id']];key=(m['packet_id'],r['step'])
            assert key not in jud and r['case_id']==m['case_id']
            assert all(type(r[f]) is bool for f in FLAGS)
            jud[key]=(r,path)
    assert len(trails)==len(jud)==54
    requirements={r['case_id']:r for r in js('gold-intervals.json')['cases']}
    reach={(r['case_id'],r['mode']):r for r in jl('reachability.jsonl')}
    cases={r['case_id']:r for r in js('cases.json')['cases']}
    gold={r['case_id']:r for r in csv.DictReader((OWN/'gold.csv').open())}
    notes=js('analysis/report-case-notes.json')
    sessions={r['session']:r for r in trials['sessions']}
    answers=[];seen=defaultdict(list);by_packet=defaultdict(list)
    for line,t in enumerate(trails,1):
        key=(t['packet_id'],t['step']);g,gpath=jud[key];p=pkt[key[0]]
        seen[key[0]].append(t['view'])
        modes={n:mode_covered(m,seen[key[0]]) for n,m in requirements[t['case_id']]['modes'].items()}
        target_alts=requirements[t['case_id']]['modes']['target']['alternatives']
        union=visible_unions(seen[key[0]])
        target_overlap=max(sum(max(0,min(hi,x['end'])-max(lo,x['start'])) for x in alt for lo,hi in union.get(x['doc_id'],[])) for alt in target_alts)
        same_anchor=any(v['doc_id']==x['doc_id'] and v.get('fragment')==x.get('anchor') for alt in target_alts for x in alt for v in seen[key[0]])
        target_required=min(sum(x['end']-x['start'] for x in alt) for alt in target_alts)
        r={'row_id':f"{t['packet_id']}-s{t['step']}",'case_id':t['case_id'],'layer':'natural','condition':t['condition'],
          'packet_id':t['packet_id'],'step':t['step'],'trails_line':line,'masked_id':g['masked_id'],
          'method':'fresh_AI_context_bounded_offline_document_viewer','source_log':t['source_log'],
          'exposure_at_utc':t['exposure_at_utc'],'answer_at_utc':t['answer_at_utc'],
          'action':t['choice']['action'],'selection_reason':t['choice_reason'],
          'hint':t['hint'],'common_request':p['common_request'],'doc_id':t['doc_id'],
          'document_version':t['document_version'],'arrival_url':t['arrival_url'],
          'arrival_url_kind':t['arrival_url_kind'],'fragment':t['fragment'],
          'offset_start':t['offset_start'],'offset_end':t['offset_end'],'display_sha256':t['display_sha256'],
          'answer_original':t['answer_original'],'recipient_disposition':t['answer_original']['disposition'],
          'citations_original':t['answer_original'].get('citations',[]),
          'citation_exact_count':sum(bool(q['strict_supported']) for q in t['citation_checks']),
          'citation_unmatched_count':sum(not q['strict_supported'] for q in t['citation_checks']),
          'primary_exact_interval_arrived':modes['target'],
          'primary_same_anchor_scope_seen_posthoc':same_anchor,
          'primary_target_overlap_codepoints_posthoc':target_overlap,
          'primary_target_required_codepoints':target_required,
          'full_required_intervals_exposed':modes['full'],
          'covered_reference_modes':[n for n,b in modes.items() if b],
          'judge_source':gpath,'grade':g['grade'],**{f:g[f] for f in FLAGS},
          'counterexample_detail':g['counterexample_detail'],'judge_evidence':g['evidence_used'],
          'missing_required_evidence':g['missing_required_evidence'],'claim_errors':g['errors'],
          'rationale_ko':g['rationale_ko'],**t['cost'],**t['duration'],
          'hint_codepoints_once_per_packet':p['hint_codepoints'],
          'hint_utf8_bytes_once_per_packet':p['hint_utf8_bytes'],
          'unobserved':'human response/time/adoption; historical binary execution; OS isolation not provided'}
        answers.append(r);by_packet[key[0]].append(r)
    packet_outcomes=[]
    for p in packets:
        rr=by_packet[p['packet_id']];last=rr[-1];ss=sessions[p['packet_id']]
        packet_outcomes.append({'packet_id':p['packet_id'],'case_id':p['case_id'],'condition':p['condition'],
          'opens':len(rr),'final_grade':last['grade'],
          **{f:last[f] for f in FLAGS},
          'counterexample_ever':any(r['counterexample_found'] for r in rr),
          'primary_exact_interval_arrived':last['primary_exact_interval_arrived'],
          'primary_same_anchor_scope_seen_posthoc':last['primary_same_anchor_scope_seen_posthoc'],
          'primary_target_overlap_codepoints_posthoc':last['primary_target_overlap_codepoints_posthoc'],
          'primary_target_required_codepoints':last['primary_target_required_codepoints'],
          'full_required_intervals_exposed':last['full_required_intervals_exposed'],
          'final_covered_reference_modes':last['covered_reference_modes'],
          'actions':[r['action'] for r in rr],
          'display_hashes':[r['display_sha256'] for r in rr],
          'locations':[{'doc_id':r['doc_id'],'version':r['document_version'],'url':r['arrival_url'],'fragment':r['fragment'],'interval':[r['offset_start'],r['offset_end']]} for r in rr],
          'display_codepoints':sum(r['display_codepoints'] for r in rr),
          'display_utf8_bytes':sum(r['display_utf8_bytes'] for r in rr),
          'content_codepoints':sum(r['content_codepoints'] for r in rr),
          'navigation_codepoints':sum(r['total_navigation_codepoints'] for r in rr),
          'measured_session_wall_seconds':ss['measured_session_wall_seconds'],
          'hint_codepoints':p['hint_codepoints'],'hint_utf8_bytes':p['hint_utf8_bytes'],
          'full_packet_codepoints':p['packet_codepoints'],'full_packet_utf8_bytes':p['packet_utf8_bytes']})
    po={(p['case_id'],p['condition']):p for p in packet_outcomes};pairs=[]
    for cid in ORDER:
        for left,right in [('A','B'),('B','C'),('A','C')]:
            l=po[cid,left];r=po[cid,right]
            different=next((i for i,(x,y) in enumerate(zip(l['display_hashes'],r['display_hashes']),1) if x!=y),None)
            pairs.append({'pair_id':f'{cid}-{left}-{right}','case_id':cid,'layer':'natural','comparison':left+'↔'+right,
              'primary_path_availability':reach[cid,'target']['semantic_reachability'],
              'full_answer_path_availability':reach[cid,'full']['semantic_reachability'],
              'reachable_opportunity_denominator':int(reach[cid,'full']['semantic_reachability']=='reachable_in_fixed_viewer'),
              'natural_case_recruited':True,'left_packet':l['packet_id'],'right_packet':r['packet_id'],
              'left_actions':l['actions'],'right_actions':r['actions'],'same_action_sequence':l['actions']==r['actions'],
              'same_display_sequence':l['display_hashes']==r['display_hashes'],'first_different_exposure_stage':different,
              'left_locations':l['locations'],'right_locations':r['locations'],
              'left_primary_exact_arrival':l['primary_exact_interval_arrived'],'right_primary_exact_arrival':r['primary_exact_interval_arrived'],
              'left_same_anchor_scope_seen_posthoc':l['primary_same_anchor_scope_seen_posthoc'],'right_same_anchor_scope_seen_posthoc':r['primary_same_anchor_scope_seen_posthoc'],
              'left_target_overlap_codepoints_posthoc':l['primary_target_overlap_codepoints_posthoc'],'right_target_overlap_codepoints_posthoc':r['primary_target_overlap_codepoints_posthoc'],
              'left_full_supported':l['full_supported'],'right_full_supported':r['full_supported'],
              'left_partial_reconstruction':l['partial_reconstruction'],'right_partial_reconstruction':r['partial_reconstruction'],
              'left_counterexample':l['counterexample_ever'],'right_counterexample':r['counterexample_ever'],
              'left_dangerous_certainty':l['dangerous_certainty'],'right_dangerous_certainty':r['dangerous_certainty'],
              'left_nearby_modes':[m for m in l['final_covered_reference_modes'] if 'nearby' in m],
              'right_nearby_modes':[m for m in r['final_covered_reference_modes'] if 'nearby' in m],
              'left_opens':l['opens'],'right_opens':r['opens'],'delta_opens_right_minus_left':r['opens']-l['opens'],
              'left_display_codepoints':l['display_codepoints'],'right_display_codepoints':r['display_codepoints'],
              'delta_display_codepoints':r['display_codepoints']-l['display_codepoints'],
              'left_display_utf8_bytes':l['display_utf8_bytes'],'right_display_utf8_bytes':r['display_utf8_bytes'],
              'delta_display_utf8_bytes':r['display_utf8_bytes']-l['display_utf8_bytes'],
              'left_wall_seconds':l['measured_session_wall_seconds'],'right_wall_seconds':r['measured_session_wall_seconds'],
              'delta_wall_seconds':round(r['measured_session_wall_seconds']-l['measured_session_wall_seconds'],6),
              'wall_time_interpretation':'AI session wall interval including scheduling/tool latency; no human or causal savings inference',
              'left_hint_codepoints':l['hint_codepoints'],'right_hint_codepoints':r['hint_codepoints'],
              'left_hint_utf8_bytes':l['hint_utf8_bytes'],'right_hint_utf8_bytes':r['hint_utf8_bytes'],
              'authoring_cost_allocation':'shared pool: 5 file reads, known12860cp/15169B plus unknown truncated exposure; 560.956346 wall s; per-case time unavailable',
              'next_check':notes[cid]['next_check']})
    costs={}
    for condition in 'ABC':
        ss=[p for p in packet_outcomes if p['condition']==condition]
        costs[condition]={k:round(sum(p[k] for p in ss),6) for k in ['opens','display_codepoints','display_utf8_bytes','content_codepoints','navigation_codepoints','measured_session_wall_seconds','hint_codepoints','hint_utf8_bytes','full_packet_codepoints','full_packet_utf8_bytes']}
    bycond={c:{'packets':6,'stages':18,
          'primary_exact_arrival_packets':sum(p['primary_exact_interval_arrived'] for p in packet_outcomes if p['condition']==c),
          'full_supported_packets':sum(p['full_supported'] for p in packet_outcomes if p['condition']==c),
          'final_partial_packets':sum(p['partial_reconstruction'] for p in packet_outcomes if p['condition']==c),
          'partial_stages':sum(r['partial_reconstruction'] for r in answers if r['condition']==c),
          'counterexample_stages':sum(r['counterexample_found'] for r in answers if r['condition']==c),
          'dangerous_certainty_stages':sum(r['dangerous_certainty'] for r in answers if r['condition']==c)} for c in 'ABC'}
    source_counts=js('analysis/source-counts.json')
    full_status=Counter(reach[c,'full']['semantic_reachability'] for c in ORDER)
    target_status=Counter(reach[c,'target']['semantic_reachability'] for c in ORDER)
    metrics={'schema':1,'task_id':'AF-RES-116','status':'PARTIAL',
      'status_reasons':['P3 exact original rendering invocation/engine/template/package environment unresolved','I3 exact original JP2 bytes and tile band semantics unavailable','Original pre-read remote update timing not independently re-proven from a retained provider receipt'],
      'completed_scope':['frozen100-row frame and6 natural requests','18 fresh-AI packets and54 observed stages','bounded navigation enumeration','masked semantic evaluation54 stages','source quotas and cross-domain comparisons','separate2 preregistered document calibrations and1 post-reference start-only diagnostic'],
      'natural':{'cases_planned':6,'cases_recruited':6,'missing_cases':0,'packets_planned':18,'packets_observed':18,'stages_planned':54,'stages_observed':54,'early_stop_stages':0,'unobserved_stages':0,
        'full_supported_packets':sum(p['full_supported'] for p in packet_outcomes),'full_supported_stages':sum(r['full_supported'] for r in answers),
        'partial_reconstruction_stages':sum(r['partial_reconstruction'] for r in answers),
        'justified_hold_flag_stages':sum(r['justified_hold'] for r in answers),
        'counterexample_flag_stages':sum(r['counterexample_found'] for r in answers),
        'dangerous_certainty_stages':sum(r['dangerous_certainty'] for r in answers),
        'grade_counts':dict(Counter(r['grade'] for r in answers)),
        'primary_exact_arrival_packets':sum(p['primary_exact_interval_arrived'] for p in packet_outcomes),
        'full_reachable_cases':full_status['reachable_in_fixed_viewer'],'full_unreachable_cases':full_status['unreachable_in_fixed_viewer'],'full_unknown_cases':full_status['unknown'],
        'primary_reachable_cases':target_status['reachable_in_fixed_viewer'],'primary_unreachable_cases':target_status['unreachable_in_fixed_viewer'],
        'reachable_opportunity_success_rate':None,'rate_limit':'No reachable natural full-answer opportunity; 0/18 is a descriptive observed count, not a causal effect estimate.',
        'counterexample_scope':'Exposed document exceptions: I2 Set/off-to-opaque in all3 conditions and P3 RTF figure exception in C. No natural failure reproduced.'},
      'by_condition':bycond,'costs_by_condition':costs,
      'paired_same_display_counts':{comp:sum(r['same_display_sequence'] for r in pairs if r['comparison']==comp) for comp in ['A↔B','B↔C','A↔C']},
      'paired_denominators':{'descriptive_pairs':18,'cases_per_comparison':6,'reachable_full_answer_opportunity_per_comparison':0},
      'total_reader_openings':len(trails),'total_reader_display_codepoints':sum(c['display_codepoints'] for c in costs.values()),
      'total_reader_display_utf8_bytes':sum(c['display_utf8_bytes'] for c in costs.values()),
      'citation_counts':trials['citation_counts'],
      'claim_error_stages':sum(bool(r['claim_errors']) for r in answers),
      'posthoc_location_diagnostics':{'same_declared_anchor_scope_seen_packets':sum(p['primary_same_anchor_scope_seen_posthoc'] for p in packet_outcomes),'any_target_body_overlap_packets':sum(p['primary_target_overlap_codepoints_posthoc']>0 for p in packet_outcomes),'definition':'Added after audit to distinguish same fragment scope, partial text overlap, and predeclared whole-target coverage; not a replacement success endpoint. I2 readers saw106/166 declared target codepoints, missing60.'},
      'bounded_graph':{'complete_graphs':6,'nodes_with_path_prefixes':sum(reach[c,'target']['graph_nodes'] for c in ORDER),'distinct_case_local_views':sum(reach[c,'target']['graph_distinct_views'] for c in ORDER),'interval_modes':len(reach),'unrestricted_web_reachability':'not_evaluated'},
      'source_counts':source_counts,
      'preparation':{'shared_author_pool_id':'AF-RES-116-blinded-author-pool-1','file_read_events':5,'known_visible_codepoints':12860,'known_visible_utf8_bytes':15169,'additional_truncated_visible_size':None,'wall_seconds':560.956346,'per_case_active_seconds':None,'unit_warning':'File inspections and recipient document opens are different units; do not sum.'},
      'calibration':{'prespecified_cases':2,'deterministic_replays':3,'witnesses_supported':2,'near_wrong_supported':0,'new_reader_choices':False,'natural_denominator_inclusion':False,'receipt':'calibration/replay-check.json'},
      'start_only_diagnostic':{'id':'D0','opens':1,'display_codepoints':1434,'display_utf8_bytes':1468,'new_reader_choices':False,'post_reference':True,'natural_denominator_inclusion':False},
      'roles':{'recipients':'18 fresh no-fork AI contexts, procedural file restrictions, shared filesystem; not human/OS isolation','evaluators':'2 new contexts with sole masked family input; residual prose may disclose presence of guidance','integrator':'reference+all outcomes visible; no blind claim','source_auditor':'separate AI audit actor; context isolation not independently certified; no recipient/hint content read'},
      'environment_limits':['local fixed text viewer, not observed browser HTTP arrivals','historical Pandoc MANUAL source rendered using installed Pandoc3.1.11.1','no historical natural binary executions','model API revision/seed and independent human time unavailable'],
      'packet_outcomes':packet_outcomes,
      'inputs_sha256':{n:digest(OWN/n) for n in ['cases.json','packets.jsonl','trails.jsonl','gold.csv','gold-intervals.json','reachability.jsonl','analysis/source-counts.json','analysis/report-case-notes.json','evaluation/masking-map.json',*judge_inputs]}}

    # Required report tables are reconstructed from these ledgers, not hand-copied.
    rows1=[]
    for cid in ORDER:
        c=cases[cid];g=gold[cid];n=notes[cid]
        version=g['fixed_document_version']+(' (원판 미지정)' if not c['specified_version'] else '')
        rows1.append([cid+' / 자연',f"[원 요청 #{c['number']}]({c['original_url']}) · {version}<br>[시작]({c['start_url']})<br>고정 source `{g['upstream_commit']}`",n['two_conditions_and_counter'],n['witness_and_sections'],n['unknown']])
    for r in notes['supplemental_table1']:rows1.append(r)
    rows2=[]
    for r in answers:
        quote='; '.join(q.get('quote','') for q in r['citations_original']) or '인용 없음'
        exp='예외 발견: '+r['counterexample_detail'] if r['counterexample_found'] else '요청 관련 반례 미발견'
        error=' / 전사 오류 1' if r['citation_unmatched_count'] else ''
        rows2.append([f"{r['case_id']} · {r['condition']} · {r['step']} ({r['packet_id']})",r['hint'] or '추가 한 줄 없음 — 공통 요청+시작 URL',
          f"`{r['action']}`; 이유: {r['selection_reason']}<br>[도착 표시 주소]({r['arrival_url']}) `{r['doc_id']}[{r['offset_start']}:{r['offset_end']}]` · {r['document_version']}",
          f"{GRADE_KO[r['grade']]}{error}. {r['rationale_ko']}<br>인용: {quote}<br>{exp}",
          f"1회 · {r['display_codepoints']}자/{r['display_utf8_bytes']}B; 내용{r['content_codepoints']}자·내비{r['total_navigation_codepoints']}자; 노출→답 {r['exposure_to_answer_seconds']:.6f}s<br>인간 시간·실제 역사 실행 미관측; trails #{r['trails_line']}"])
    rows3=[]
    for r in pairs:
        cid=r['case_id'];p=r['comparison'];l=po[cid,p[0]];rr=po[cid,p[-1]]
        same='동일 노출' if r['same_display_sequence'] else f"{r['first_different_exposure_stage']}단계부터 다른 노출"
        rows3.append([cid+(' / 완전 경로 불가' if r['full_answer_path_availability']=='unreachable_in_fixed_viewer' else ' / 완전 경로 미확인')+'; 도달 가능 분모0',
          p+'; '+same,
          f"선언 target 전구간 {int(l['primary_exact_interval_arrived'])}↔{int(rr['primary_exact_interval_arrived'])} (같은 fragment 범위 {int(l['primary_same_anchor_scope_seen_posthoc'])}↔{int(rr['primary_same_anchor_scope_seen_posthoc'])}; target 겹침 {l['primary_target_overlap_codepoints_posthoc']}↔{rr['primary_target_overlap_codepoints_posthoc']}자); 충분한 답 {int(l['full_supported'])}↔{int(rr['full_supported'])}; 위험 확정 {int(l['dangerous_certainty'])}↔{int(rr['dangerous_certainty'])}<br>최종 부분 {int(l['partial_reconstruction'])}↔{int(rr['partial_reconstruction'])}; 문서 예외 {int(l['counterexample_ever'])}↔{int(rr['counterexample_ever'])}",
          f"수신 {l['opens']}↔{rr['opens']}회; {l['display_codepoints']}↔{rr['display_codepoints']}자; {l['display_utf8_bytes']}↔{rr['display_utf8_bytes']}B; 벽시계 {l['measured_session_wall_seconds']:.6f}↔{rr['measured_session_wall_seconds']:.6f}s<br>한 줄 {l['hint_codepoints']}↔{rr['hint_codepoints']}자/{l['hint_utf8_bytes']}↔{rr['hint_utf8_bytes']}B; 제작 공유풀5파일·560.956346s, 사건별 배분 불가",r['next_check']])
    tables='## 표 1. 사건·표본층과 기준 도달성\n\n'+table(['사건·표본층','원 요청·판·시작 URL','확인할 두 조건·반례','3회 이내 증인 경로·원절','미확인'],rows1)
    tables+='\n## 표 2. 실제 수신 54단계\n\n'+table(['사건·보기·단계','독자에게 보인 한 줄','실제 선택·도착 URL·구간','답·반례·근거 충분성','비용·미관측'],rows2)
    tables+='\n## 표 3. 사건별 세 쌍의 비교\n\n'+table(['사건·도달 가능 분모','A↔B·B↔C·A↔C','정확한 절·충분한 답·위험한 확정','제작·수신 비용','다음 확인'],rows3)
    tables+='\n표의 주소는 고정 오프라인 문서의 원 URL·fragment를 복원한 위치 표지다. 해당 시점의 HTTP 도착 또는 현재 라이브 문서의 동일 본문을 뜻하지 않는다. `[...]`는 corpus의 Unicode 반열림 구간이며 본문/내비 지문은 `trails.jsonl`에 있다. 각 단계 판정은 그때까지 누적 노출된 구간만 사용한다. 제작 비용은 6건 공유풀이므로 표 3의 반복 표기를 합산하지 않는다.\n'
    interpretation=(OWN/'analysis/interpretation.md').read_text().rstrip()
    def relocate(m):
        target=m.group(1)
        if '://' in target or target.startswith(('#','/')):return m.group(0)
        return ']('+posixpath.normpath('analysis/'+target)+')'
    interpretation=re.sub(r'\]\(([^)]+)\)',relocate,interpretation)
    report=tables+'\n'+interpretation+'\n'
    return {'answers.csv':csv_text(answers),'pairs.csv':csv_text(pairs),'metrics.json':json.dumps(metrics,ensure_ascii=False,indent=2)+'\n','RESULT.md':report,'analysis/report-tables.md':tables}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args();outputs=build();bad=[]
    for n,t in outputs.items():
        if a.check:
            if not (OWN/n).exists() or (OWN/n).read_bytes()!=t.encode():bad.append(n)
        else:(OWN/n).write_bytes(t.encode())
    print(json.dumps({'check':a.check,'outputs':list(outputs),'mismatches':bad}));raise SystemExit(bool(bad))
if __name__=='__main__':main()
