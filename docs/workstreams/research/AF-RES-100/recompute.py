"""Reconstruct all required report tables and denominators from committed ledgers.

Run --write while authoring, or --check for a read-only deterministic comparison.
No network, answer retrieval, subject-program execution, or new model judgment.
"""
from pathlib import Path
import argparse, collections, csv, hashlib, json

ROOT=Path(__file__).resolve().parent
def jl(name): return [json.loads(x) for x in (ROOT/name).read_text().splitlines() if x.strip()]
def truth(v): return v is True or v=='True'
def esc(v): return str(v).replace('|','&#124;').replace('\n',' ')
def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','|'+'|'.join(['---']*len(headers))+'|']+
      ['| '+' | '.join(esc(v) for v in row)+' |' for row in rows])+'\n'
def union_size(spans):
    end=-1;size=0
    for a,b in sorted(spans):
        size+=max(0,b-max(a,end));end=max(end,b)
    return size
def link(fid,label=None):return '['+(label or fid)+']['+fid+']'
def pair_counts(rows):
    c=collections.Counter(r['result'] for r in rows)
    return {'positions':len(rows),'comparable':sum(truth(r['comparable']) for r in rows),
            **{k:c[k] for k in ['A_only','B_only','both','neither','incomparable']}}
def write_or_check(path,text,check):
    p=ROOT/path
    if check:assert p.read_bytes()==text.encode(),'report differs from ledgers: '+path
    else:p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
def main():
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--write',action='store_true');g.add_argument('--check',action='store_true');a=ap.parse_args()
    protocol=json.loads((ROOT/'protocol.json').read_text());cases=protocol['cases']
    notes=json.loads((ROOT/'case-notes.json').read_text())
    packets=jl('packets.jsonl');judgments=jl('judgments.jsonl');initial=jl('evidence/initial-judgments.jsonl')
    jd={r['packet_id']:r for r in judgments};idj={r['packet_id']:r for r in initial}
    ps={(r['case_id'],r['policy'],r['mode']):r for r in packets}
    pairs=list(csv.DictReader((ROOT/'pairs.csv').open()));outcomes=list(csv.DictReader((ROOT/'outcomes.csv').open()))
    od={r['case_id']:r for r in outcomes};sources=jl('sources.jsonl');disp=list(csv.DictReader((ROOT/'displacement.csv').open()))
    corpus={r['file_id']:r for r in jl('corpus-files.jsonl')}
    assert len(cases)==8 and len(packets)==len(judgments)==len(initial)==32
    assert len(pairs)==16 and len(outcomes)==8 and len(disp)==24
    assert len(set(jd))==32 and all((c['case_id'],p,m) in ps for c in cases for p in 'AB' for m in 'FS')
    case_map={c['case_id']:c for c in cases}
    for j in judgments:
        assert j['complete']==all(c['status']=='supported' for c in j['conditions'])
    for r in pairs:
        ja,jb=jd[r['A_packet']],jd[r['B_packet']]
        assert ja['complete']==truth(r['A_complete']) and jb['complete']==truth(r['B_complete'])
        comparable=case_map[r['case_id']]['stable_adjacent_resolved']
        assert comparable==truth(r['comparable'])
        expected=('incomparable' if not comparable else 'both' if ja['complete'] and jb['complete'] else 'A_only' if ja['complete'] else 'B_only' if jb['complete'] else 'neither')
        assert r['result']==expected, 'pair classification is inconsistent with judgments: '+r['case_id']+'/'+r['mode']
    counted=[s for s in sources if s['count_minimum']]
    identities=[s['fixed_url'] for s in counted];assert len(identities)==len(set(identities))
    source_groups=collections.Counter(s['count_group'] for s in counted)
    minima={'new_initial_questions':8,'main_official':5,'adjacent_official':5,'upstream_tests':4,'crossdomain_official_docs':2,'crossdomain_fixtures':2}
    assert all(source_groups[k]>=v for k,v in minima.items())
    packet_files={s['file_id'] for p in packets for s in p['slots'] if not s.get('empty')}
    assert packet_files <= {s['source_id'][4:] for s in sources if s['source_id'].startswith('AUD-')}
    stats={};events=[];citations=[]
    for p in packets:
        ev=jl('evidence/packet-access/'+p['packet_id']+'.jsonl');events.extend(ev)
        byfile=collections.defaultdict(list)
        for e in ev:
            for s in e.get('displayed_segments',[]):byfile[e['file_id']].append((s['char_start'],s['char_end']))
        st={'charged':sum(e.get('charged_attempts',0) for e in ev),
            'navigation':sum(e['event']=='section_navigation' for e in ev),
            'displayed_chars':sum(e.get('displayed_chars',0) for e in ev),
            'unique_displayed_chars':sum(union_size(x) for x in byfile.values()),
            'available_chars':p['total_exposed_chars']}
        assert st['charged']==4
        if p['mode']=='S':assert st['navigation']==0 and st['available_chars']<=4800
        stats[p['packet_id']]=st
        for cond in jd[p['packet_id']]['conditions']:
            for cite in cond['citations']:
                slot=p['slots'][cite['slot']-1]
                assert slot['url']==cite['url'] and slot['char_start']<=cite['char_start']<cite['char_end']<=slot['char_end']
                assert slot['byte_start']<=cite['byte_start']<cite['byte_end']<=slot['byte_end']
                raw=(ROOT/slot['cached_body']).read_bytes();txt=raw.decode()
                assert hashlib.sha256(raw).hexdigest()==slot['sha256']
                assert len(txt[:cite['char_start']].encode())==cite['byte_start']
                assert len(txt[:cite['char_end']].encode())==cite['byte_end']
                covered=[]
                for e in ev:
                    if e.get('status')=='success' and e.get('finished_utc','')<=jd[p['packet_id']]['initial_judgment_recorded_utc']:
                        covered += [(max(cite['char_start'],s['char_start']),min(cite['char_end'],s['char_end'])) for s in e.get('displayed_segments',[]) if e.get('file_id')==cite['file_id'] and max(cite['char_start'],s['char_start'])<min(cite['char_end'],s['char_end'])]
                assert union_size(covered)==cite['char_end']-cite['char_start']
                citations.append(cite)
    aggregates={}
    for mode in 'FS':
      for stratum in ['all','boundary','control']:
        selected=[r for r in pairs if r['mode']==mode and (stratum=='all' or r['stratum']==stratum)]
        aggregates[mode+'/'+stratum]=pair_counts(selected)
    transitions=[]
    for c in cases:
      for policy in 'AB':
        f,s=ps[(c['case_id'],policy,'F')],ps[(c['case_id'],policy,'S')]
        transitions.append({'case_id':c['case_id'],'policy':policy,'F_complete':jd[f['packet_id']]['complete'],'S_complete':jd[s['packet_id']]['complete'],
          'comparable':c['stable_adjacent_resolved'],'lost_when_snippeted':jd[f['packet_id']]['complete'] and not jd[s['packet_id']]['complete']})
    budgets={m:{k:sum(stats[p['packet_id']][k] for p in packets if p['mode']==m) for k in ['charged','navigation','displayed_chars','unique_displayed_chars','available_chars']} for m in 'FS'}
    condition_counts={m:dict(collections.Counter(c['status'] for p in packets if p['mode']==m for c in jd[p['packet_id']]['conditions'])) for m in 'FS'}
    changed=[r['packet_id'] for r in judgments if r['complete']!=idj[r['packet_id']]['complete']]
    metrics={'schema':'af-res-100-derived-v1','primary_metric':protocol['evaluation']['primary_metric'],
      'cases':8,'packets':32,'comparisons':16,'comparable_comparisons':sum(truth(r['comparable']) for r in pairs),
      'aggregates':aggregates,'budgets':budgets,'condition_counts':condition_counts,'transitions':transitions,
      'F_to_S_complete_losses':sum(r['lost_when_snippeted'] for r in transitions),
      'source_rows':len(sources),'counted_unique_sources':len(counted),'source_groups':dict(source_groups),'source_group_minima':minima,
      'packet_unique_files':len(packet_files),'charged_slots':128,'vacant_slots':sum(s.get('empty',False) for p in packets for s in p['slots']),
      'citations_checked':len(citations),'initial_to_preoutcome_changes':changed,
      'same_question_prior_exposure':sum(bool(r['same_question_previous_exposure']) for r in judgments),
      'prior_shared_file_packets':sum(bool(r['prior_same_source_files']) for r in judgments),
      'observed_contaminated_packets':[r['packet_id'] for r in judgments if r['contamination']],
      'outcomes':{'cases':len(outcomes),'answers':sum(int(r['answers_current_count']) for r in outcomes),'comments_30days':sum(int(r['comments_within_30_days']) for r in outcomes),
         'accepted':sum(bool(r['current_accepted_answer_id']) for r in outcomes),'same_version_input_output_verified':sum(truth(r['same_version_input_output_execution_verified']) for r in outcomes)},
      'sensitivities':{},'inputs_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ['protocol.json','packets.jsonl','judgments.jsonl','pairs.csv','outcomes.csv','displacement.csv','sources.jsonl','case-notes.json']}}
    for scenario,remove,demote in [('helper_builtin_only',set(),{'P1'}),('exclude_retagged_P1',{'P1'},set()),('require_J1_final_join',set(),{'J1'}),('J2_heterogeneous_original_pipeline',set(),{'J2'}),('require_P4_end_to_end_PDF',set(),{'P4'})]:
      m={}
      for mode in 'FS':
        rr=[]
        for r in pairs:
          if r['mode']!=mode or r['case_id'] in remove:continue
          q=dict(r)
          if r['case_id'] in demote and truth(r['comparable']):q['result']='neither';q['A_complete']='False';q['B_complete']='False'
          rr.append(q)
        m[mode]=pair_counts(rr)
      metrics['sensitivities'][scenario]=m
    # Required table 1: recruitment and intended requirement.
    t1=[]
    for c in cases:
      n=notes[c['case_id']];rv='jq1.7.1' if c['tag']=='jq' else 'Pandoc3.6'
      if c.get('adjacent_label'):
        versions=sorted({s['version'] for p in packets if p['case_id']==c['case_id'] for s in p['slots'] if not s.get('empty') and s['role']=='adjacent'})
        rv+='; '+('/'.join(versions) or '인접 고정판 공석')
      origin='; '.join(x['id']+' U'+','.join(f'[{u},{v})' for u,v in x['origin_ranges']) for x in c['conditions'])
      t1.append([f"{c['case_id']} [{c['question_id']}]({c['r0_url']}) · {c['stratum']} · 태그순위 {c['original_rank']}",n['request']+'<br>'+n['means_boundary'],
        '; '.join(k+'='+str(v) for k,v in c['user_versions'].items())+'<br>연구: '+rv,n['missing'],n['criterion']+'<br>R0 HTML '+origin])
    tables='# AF-RES-100 결과 — 파일 전체와 제한 발췌의 문서 근거 가용성\n\n## 1. 모집·의도 표\n\n'+table(['사례·질문 ID / 최초 revision','원 필수 결과·수단 / 인접 경계','사용자판 / 연구판','누락·제외·재게시','사전 판정 기준·원문 구간'],t1)
    # Required table 2: all 32 packets, all four source boundaries and citations.
    t2=[];status={'supported':'지지','partial':'부분','unknown':'유보','refuted':'반박'}
    for p in packets:
      j=jd[p['packet_id']];st=stats[p['packet_id']];slotparts=[]
      for s in p['slots']:
        if s.get('empty'):slotparts.append(str(s['slot'])+' 공석(1접근 과금)');continue
        slotparts.append(str(s['slot'])+' '+link(s['file_id'])+f" U[{s['char_start']},{s['char_end']}) B[{s['byte_start']},{s['byte_end']})")
      cj=[]
      for c in j['conditions']:
        refs=[]
        for z in c['citations']:
          refs.append(link(z['file_id'])+' §'+z.get('section','')+f" U[{z['char_start']},{z['char_end']}) B[{z['byte_start']},{z['byte_end']})")
        cj.append(c['id']+' '+status[c['status']]+': '+('; '.join(refs) or '패킷 안 충분한 인용 없음'))
      missing=','.join(c['id'] for c in j['conditions'] if c['status']!='supported') or '필수 조건 없음; 실행 미확인은 표1'
      result=('완결' if j['complete'] else '미완결') if p['case_id']!='P3' else '비교불가(문서 미완결)'
      t2.append([p['case_id']+'/'+p['policy']+'/'+p['mode']+' / `'+p['packet_id']+'`','<br>'.join(slotparts),
        f"{st['charged']} / {st['navigation']} / {st['displayed_chars']:,} / {st['unique_displayed_chars']:,}<br>[각 구간 로그](evidence/packet-access/{p['packet_id']}.jsonl)",
        '<br>'.join(cj),result+'; 부족 '+missing+'<br>관측 오염 '+str(len(j['contamination']))+'; 선행 공유파일 '+str(len(j['prior_same_source_files']))+'<br>'+j['reader_id']+' '+j['initial_judgment_recorded_utc']])
    tables+='\n## 2. 32자리 근거 표\n\nU는 원 파일 Unicode 문자, B는 UTF-8 바이트의 0기반 반열린 구간이다. 파일 ID 링크는 아래 고정 원문 주소로 연결된다. 접근/이동/표시/고유는 과금 접근 수, 무료 절 이동 수, 반복 포함 표시 문자 수, 패킷 안 중복을 제거한 표시 문자 수이다. 전체 파일에 접근할 수 있다는 사실을 전체를 읽었다고 세지 않았다. 판정은 필수 조건의 문서 충분성이며 원 사용자 실행 성공이 아니다.\n\n'+table(['질문·정책·읽기 / 패킷 ID','순위 1–4 / 노출 U·B 범위','접근 / 절 이동 / 표시 / 고유 문자','조건별 판정·근거 URL/절/정확한 구간','완결·누락·오염·첫 판정 UTC'],t2)
    # Required table 3: paired result plus up to two post-seal return links.
    t3=[];pairmap={(r['case_id'],r['mode']):r for r in pairs}
    for c in cases:
      cid=c['case_id'];n=notes[cid];rout=[]
      for ln in n['links']:
        rout.append((link(ln['file_id']) if 'file_id' in ln else '[Docker 고정 README]('+ln['url']+')')+' — '+ln['section'])
      def label(mode):
        r=pairmap[(cid,mode)]
        if not truth(r['comparable']):return 'A 미완결 / B 공석 → 비교불가'
        return 'A '+('완결' if truth(r['A_complete']) else '미완결')+' / B '+('완결' if truth(r['B_complete']) else '미완결')
      outurl=od[cid]['principal_followup_url'] or od[cid]['question_url']
      t3.append([cid,label('F'),label('S'),n['effect'],'<br>'.join(rout)+'<br>실패 조건: '+n['failure'],n['post']+'<br>[공개 후속]('+outurl+')'])
    tables+='\n## 3. 비교·반환 표\n\n반환은 봉인 후 만든 편집안이며 질문별 최대 두 링크이다. 서로 다른 패킷 또는 사후 자료를 조합한 반환 링크는 주32판정의 근거를 추가하지 않는다. 특히 P1의 둘째 writer 링크는 A에 있던 출력 단서이고 P3 Docker README는 사후에만 연 오래된 고정판이다. 두 링크가 모든 조건을 덮지 못하면 실패 조건에 명시했다.\n\n'+table(['질문','F의 A·B','S의 A·B','밀림·추가 근거','줄 링크·볼 절·한계','사후 질문자 행동·미확인'],t3)
    defs='\n'.join('['+fid+']: '+corpus[fid]['url'] for fid in sorted(packet_files|{ln['file_id'] for n in notes.values() for ln in n['links'] if 'file_id' in ln}))
    tables+='\n'+defs+'\n'
    nums='## 4. 예산·층별 분모와 민감도\n\n'
    nr=[]
    for k,d in aggregates.items():nr.append([k,d['positions'],d['comparable'],d['A_only'],d['B_only'],d['both'],d['neither'],d['incomparable']])
    nums+=table(['읽기/층','배정 쌍','비교 가능','A만','B만','양쪽','모두 미완결','비교불가'],nr)
    nums+='\n'+table(['읽기','배정 자리','과금 접근','절 이동','접근 가능한 문자','실제 표시 문자(반복 포함)','패킷별 고유 표시 문자 합'],[[m,16,budgets[m]['charged'],budgets[m]['navigation'],budgets[m]['available_chars'],budgets[m]['displayed_chars'],budgets[m]['unique_displayed_chars']] for m in 'FS'])
    nums+='\n'+table(['자료 종류','최소 요구','고유 산입'],[[k,minima[k],source_groups[k]] for k in minima])
    sr=[]
    labels={'helper_builtin_only':'P1 내장 옵션·기존 호출 불변만 허용','exclude_retagged_P1':'최초 태그·본문에 Pandoc 없는 P1 제외','require_J1_final_join':'J1 최종 JOIN 성공까지 필수','J2_heterogeneous_original_pipeline':'사후 J2 이질 EventData/UserData 전체 실행 필수','require_P4_end_to_end_PDF':'P4 최종 PDF 전체 성공까지 필수'}
    for k,m in metrics['sensitivities'].items():
      for mode,d in m.items():sr.append([labels[k],mode,d['positions'],d['comparable'],d['A_only'],d['B_only'],d['both'],d['neither'],d['incomparable']])
    nums+='\n### 해석 민감도 — 각각 하나씩 적용한 문서 충분성 재분류\n\n'+table(['조건','읽기','배정','비교 가능','A만','B만','양쪽','모두 미완결','비교불가'],sr)
    nums+='\n민감도는 주 판정을 고치지 않는다. P1/J1/P4 해석 분기는 공개 전 protocol에 있었다. J2의 이질 EventData/UserData 전체 실행은 사후 새로 알려진 조건을 적용한 별도 엄격 분석이다. P1 제외는 모집 민감도다. 이 행들을 합산하거나 동일 관측처럼 취급하지 않는다.\n'
    perspectives='## 7. 독자·유지관리자·검색 결과 편집자의 후속 판단\n\n'+table(['질문','독자','유지관리자','검색 결과 편집자'],[[cid,n['reader'],n['maintainer'],n['editor']] for cid,n in notes.items()])
    narrative=(ROOT/'REPORT_NOTES.md').read_text()
    assert '<!-- PERSPECTIVES -->' in narrative
    narrative=narrative.replace('<!-- PERSPECTIVES -->',perspectives)
    narrative=narrative.replace('{{SOURCE_ROWS}}',str(len(sources)))
    checks_path=ROOT/'evidence/result-checks.json'
    check_text='실제결과판check/cloud_check는결과를커밋한뒤수행한다. 아직실행을주장하지않는다.'
    if checks_path.exists():
      cr=json.loads(checks_path.read_text())
      check_text='### 실제 결과판 검사\n\n'+table(['검사','실제 대상SHA','종료값','범위·건너뜀'],[[r['label'],r['target_sha'],r['exit_code'],r['scope']] for r in cr['commands']])
      check_text+='\n[실제명령·UTC·stdout/stderr영수증](evidence/result-checks.json). 이표는실제검사한SHA를명시하며,영수증추가후속커밋을소급해검사했다고하지않는다. 최종GitHub재열람과마지막검사대상은HANDOFF에기록한다.'
    narrative=narrative.replace('<!-- RESULT_CHECKS -->',check_text)
    result=tables+'\n'+nums+'\n'+narrative
    write_or_check('evidence/derived/metrics.json',json.dumps(metrics,ensure_ascii=False,indent=2)+'\n',a.check)
    write_or_check('evidence/derived/required-tables.md',tables,a.check)
    write_or_check('RESULT.md',result,a.check)
    print(json.dumps({'check':a.check,'packets':32,'pairs':16,'comparable':metrics['comparable_comparisons'],'sources_counted':len(counted),'citations_checked':len(citations),'F_to_S_losses':metrics['F_to_S_complete_losses'],'primary_changes':changed},ensure_ascii=False))

if __name__=='__main__':main()
