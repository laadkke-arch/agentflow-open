from pathlib import Path
import json,csv,collections,hashlib
P=Path(__file__).resolve().parents[1]
cases=json.loads((P/'evidence/cases-normalized.json').read_text());rows=[];metrics=[]
for sample,folder,prefix in [('A','collectors/cross',''),('B','collectors/cran','B-')]:
 views={v:{r['rid']:r for r in json.loads((P/f'{folder}/{prefix}{v}-decisions.json').read_text())} for v in ['L1','L2','L3']}
 for c in cases:
  if c['sample']!=sample:continue
  rid=c['reference_id'];r={'reference_id':rid,'sample':sample,'purpose':c['purpose'],'source_adjudication':c['verdict'],'adjudication_actor':'full-context collector; independent internal reader given cards, not external ground truth','adjudication_eligible':rid!='B04','A_duplicate':rid=='B05','possible_prior_exposure':rid in ['A-D04','B03'],'later_correction_backdated':False,'all_clocks_exact':False,'missing_clock_count':sum(c['dates'].get(k) in [None,'미확인'] for k in ['consumer_merge','consumer_build','reader_report'])}
  for v,d in views.items():
   dec=d[rid];action=dec['decision'];cat='보류' if action=='보류' else ('평가불가' if rid=='B04' else ('정답' if action==c['verdict'] else ('오교체' if action=='교체' else '잘못유지')))
   r[v+'_decision']=action;r[v+'_comparison']=cat;r[v+'_rationale']=dec.get('rationale');r[v+'_remaining_unknown']=dec.get('remaining_unconfirmed',dec.get('remaining_uncertainty'));r[v+'_additional_external_pages']=dec.get('additional_pages',0);r[v+'_source_cards']=dec.get('source_cards_in_input',dec.get('source_cards_read',0));r[v+'_decision_file']=f'{folder}/{prefix}{v}-decisions.json'
  r['counterexplanation']=views['L3'][rid].get('minimum_information_or_next_source',c.get('verdict_reason'))
  r['history_does_not_establish']=c['unknowns'];rows.append(r)
 for v in views:
  subset=[r for r in rows if r['sample']==sample];ct=collections.Counter(r[v+'_comparison'] for r in subset)
  metrics.append({'sample':sample,'view':v,'attempt_denominator':len(subset),'correct_actions':ct['정답'],'wrong_replacement':ct['오교체'],'wrong_keep':ct['잘못유지'],'abstentions':ct['보류'],'nonevaluable_HTML_baseline':1 if sample=='B' else 0,'same_A_case_duplicates':1 if sample=='B' else 0,'extra_external_pages':sum(r[v+'_additional_external_pages'] for r in subset),'source_cards':sum(r[v+'_source_cards'] for r in subset),'note':'Abstention is not credited as correct, even when final adjudication also abstains. Match is conditional on collected evidence; not measured user performance.'})
with (P/'comparisons.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in r.items()} for r in rows)
(P/'evidence/comparison-counts.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2))
(P/'evidence/comparison-protocol-note.md').write_text('''# 비교 해석 한계\n\nA12와 B6은 각각 다른 내부판독자가 L1→L2→L3 입력을 순서대로 읽었고 결정파일을 봉인했다. 원문을 읽은 수집자의 기준판정과 나중 비교했다. 이는 실제 이용자 실험이나 외부 검토가 아니다. L3카드 자체에 수집자의 사실요약과일부해석이 포함되므로 독립 원문 검증으로 부르지 않는다.\n\nL1/L2는현재전달증거가 없어전원보류. L3에는현재응답·내용과배포이력을동시에추가하므로보류해소를이력만의효과로분리할수없다. 의미상유지판정만을위해서는A-D01/03/05,R01/02의목적과현재본문이면충분하다는사후분석이가능하지만,실제L1/L2에서판정을냈다고보고하지않는다. 최소정보만으로도보류가충분했던A-R04/B04는정답분자로올리지않는다.\n\n별도판독의추가외부웹조회는전단계0이다. 카드50(A)/23(B)는새로연페이지가아니다. 자료수집자의원문열람과archive의member상태관측은sources/editions/costs에별도단위로남긴다. A-D04사전B05노출과B03판독자의잠정curl배경노출을제외하는민감도는A11행(유지8/교체2/보류1),B5행(유지3/교체1/보류1)이다. B05중복도제외한독립B평가가능소비자는4개다.\n''')
print(json.dumps(metrics,ensure_ascii=False,indent=2))
