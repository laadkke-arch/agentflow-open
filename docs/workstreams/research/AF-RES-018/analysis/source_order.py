#!/usr/bin/env python3
"""Compare A/P ordering across external records and separate blind judgments.

Common question sets are required. Entity denominators still differ by source;
ordering agreement is a sensitivity result, not agreement on adoption truth.
"""
import collections,csv,json
from common import ROOT,load,save
from metrics import groups
from bootstrap import paired_interval
def direction(value):
 if value is None:return 'unscorable'
 if abs(value)<1e-12:return 'tie'
 return 'P' if value>0 else 'A'
def relation(a,b):
 if 'unscorable' in [a,b]:return 'unscorable'
 if a==b:return 'same_order' if a!='tie' else 'both_tie'
 if 'tie' in [a,b]:return 'one_tie'
 return 'reversed'
def main():
 pairs=collections.defaultdict(dict)
 for r in load('analysis/per_question.json'):pairs[r['qid']][r['condition']]=r
 definitions=[('external_gold','gold_recall','primary','primary_pool_recall'),
              ('external_gold','gold_recall','secondary','secondary_pool_recall'),
              ('primary','primary_pool_recall','secondary','secondary_pool_recall')]
 results=[]
 for gid,label,qids in groups(pairs):
  for left,lf,right,rf in definitions:
   common=[q for q in qids if all(pairs[q][c].get(f) is not None for c in ['A','P'] for f in [lf,rf])]
   l=paired_interval([pairs[q] for q in common],'mean',field=lf)
   r=paired_interval([pairs[q] for q in common],'mean',field=rf)
   lo,ro=direction(l['difference']),direction(r['difference'])
   results.append({'group':gid,'group_label':label,'group_questions':len(qids),'common_questions':len(common),'common_qids':common,
                   'left_source':left,'right_source':right,'left_metric':lf,'right_metric':rf,'left_order':lo,'right_order':ro,
                   'status':relation(lo,ro),'left':l,'right':r,
                   'limits':'Same questions, distinct relevant-entity pools. Internal relevance does not independently establish adoption2. Ties and missingness are not forced into an ordering.'})
 save('analysis/judging-source-order.json',results)
 columns=['group','group_label','group_questions','common_questions','left_source','right_source','left_order','right_order','status','left_difference','right_difference']
 with (ROOT/'analysis/judging-source-order.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=columns,extrasaction='ignore');w.writeheader()
  for r in results:w.writerow({**r,'left_difference':r['left']['difference'],'right_difference':r['right']['difference']})
 print(json.dumps({'comparisons':len(results),'overall':[r for r in results if r['group']=='all']},ensure_ascii=False))
if __name__=='__main__':main()
