"""Serialize already-observed common-start receipts; performs no network calls."""
from pathlib import Path
import json, re, importlib.util
from datetime import datetime, timezone

P=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('protocol',P/'protocol.py'); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
Q={x['id']:x for x in map(json.loads,(P/'questions.jsonl').read_text().splitlines())}
selected={'Q01':[1,2],'Q03':[1,2],'Q05':[1,6],'Q07':[1,2],'Q09':[1,3],'Q11':[1,2]}
providers={
 'Q01':[{'id':'php','prefixes':['https://www.php.net/manual/']},{'id':'mozilla-javascript','prefixes':['https://developer.mozilla.org/en-US/docs/Web/JavaScript/','https://github.com/mdn/content/']}],
 'Q03':[{'id':'go-runtime','prefixes':['https://go.dev/','https://go.googlesource.com/go/','https://github.com/golang/go/','https://golang.google.cn/']}],
 'Q05':[{'id':'cpython-stdlib','prefixes':['https://docs.python.org/','https://github.com/python/cpython/']}],
 'Q07':[{'id':'cpython-stdlib','prefixes':['https://docs.python.org/','https://github.com/python/cpython/']}],
 'Q09':[{'id':'numpy','prefixes':['https://numpy.org/doc/','https://numpy.org/devdocs/','https://github.com/numpy/numpy/']}],
 'Q11':[{'id':'numpy','prefixes':['https://numpy.org/doc/','https://numpy.org/devdocs/','https://github.com/numpy/numpy/']}],
}
notes={
 'Q01':[
 ('PHP array destructuring','Array destructuring L472–555; array-key behavior L377–382','PHP 7.1+ syntax, PHP 8 warning distinction; mutable manual','Assign fixed array positions to separate variables; absent entries give null and warning.','Different language; Go bindings and type integration are not supplied.','php-arrays',True),
 ('JavaScript destructuring','Description and defaults L241–373; Array destructuring L376–400, L437–566','MDN current page; no immutable edition','Positional binding and default expressions; exhausted input produces undefined without explicit default.','JavaScript undefined is not implicit null; Go implementation is absent.','mdn-destructuring',True)],
 'Q03':[
 ('Go runtime error handling','Error handling and reporting L40–46','Go commit 917b60b4944c4a7c764d64f3973d2588ed36f8e8','Runtime distinguishes panic, throw and fatal; racing map writes use fatal.','Does not implement a recoverable map detector; observing guideline is not testing current runtime.','go-runtime-hacking',True),
 ('Go runtime error handling, current mirror','Error handling and reporting L145–151','Current official Go China source mirror; exact tag unreported','Same fatal/racing-map rule appears in this edition.','Same document family; not a second independent supplier original.','go-runtime-hacking',False)],
 'Q05':[
 ('CPython frame inspection','Types and members L9–50, especially f_locals L46','Tool title Python 3.15.2, mutable /3/ alias','Frames expose a local-namespace member.','Visible returned excerpt does not specify write-through or locals() semantics; title version is observed, not independently release-verified.','python-inspect',True),
 ('CPython frame inspection, 3.11','Types and members L9–45, especially f_locals L44','Tool title Python 3.11.18','Older manual also names frame local namespace.','No write-through evidence in read excerpt; same document family counted once.','python-inspect',False)],
 'Q07':[
 ('CPython typing overview','Module overview and callable annotation L1–145; retrieved excerpt ends L543','Tool title Python 3.15.2','The opened excerpt describes typing machinery and annotations.','Annotated/DocInfo sections were not delivered in this open; page-wide existence cannot be inferred from total_lines.','python-typing',True),
 ('CPython typing source page','GitHub file chrome/line-number preview through tool L1382','main; exact source commit unreported','The response identifies the typing.rst repository path.','Substantive source text was not returned; excluded from directly-read-original count and from baseline citations.','python-typing',False)],
 'Q09':[
 ('NumPy scalar promotion','Detailed behavior of Python scalars L71–107; numerical promotion L108–119; builtin classes L139–150; prior behavior L191','Tool title NumPy v2.5, stable alias','Python scalar precision is ignored; result_type example and distinction from old scalar/0-D rules are documented.','No execution; dtype result and arithmetic overflow behavior must be scored separately.','numpy-promotion',True),
 ('NumPy scalar promotion, development','Python scalars L71–107; cast safety L108–132; builtin classes L164–175; prior behavior L216','Tool title NumPy v2.6.dev0','Development page preserves weak-scalar rules and adds cast-safety detail.','Same manual document family; development text is not evidence of historical availability.','numpy-promotion',False)],
 'Q11':[
 ('NumPy variable-width string arrays','Variable-width strings L73–89; Missing data L90–135; coercion L140–150','Tool title NumPy v2.6.dev0; feature says added 2.0','StringDType stores variable UTF-8 strings in ndarray; coerce=False rejects nonstrings; missing sentinel behavior is documented.','N-D indexing/scalar guarantees and entire serialization subsystem are not established by this section alone.','numpy-strings',True),
 ('NumPy ndarray user guide','PDF printed pp3–11 / tool pages6–15: ndarray shape/dtype L109–138, creation L188–211, indexing L397–414','PDF Release 2.5.0','General ndarray construction, dimensions and indexing are visible.','Only first returned PDF excerpt read; StringDType chapter was not delivered; aggregate guide is not an independent strings-document count.','numpy-userguide',True)]
}
for q, ranks in selected.items():
 d=P/'common'/q
 search=json.loads((d/'search.json').read_text())
 text='\n'.join(x.get('text','') for x in search['response'].get('content',[]) if x.get('type')=='text')
 hits=[{'rank':i+1,'title':v[0],'url':v[1],'ref':v[2]} for i,v in enumerate(re.findall(r'^(.+?) \((https?://[^\n]+)\)\n【([^】]+)】',text,re.M))]
 opens=[]; sources=[]; candidates=[]
 for i,rank in enumerate(ranks,1):
  rec=json.loads((d/f'open-{i}.json').read_text()); h=hits[rank-1]; name,section,version,verified,limit,dup,count=notes[q][i-1]
  body='\n'.join(x.get('text','') for x in rec['response'].get('content',[]) if x.get('type')=='text')
  source_id=f'{q}-C-S{i}'
  readable=not(q=='Q07' and i==2)
  opens.append({'provided_rank':rank,'url':h['url'],'receipt':f'common/{q}/open-{i}.json','source_id':source_id,'body_open_number':i,'status':'readable_excerpt' if readable else 'metadata_only','read_sections':[section],'version':version,'duplicate_group':dup,'limitation':limit})
  sources.append({'source_id':source_id,'kind':'supplier_manual' if readable else 'attempt_metadata_only','publisher':providers[q][min(i-1,len(providers[q])-1)]['id'],'original_url':h['url'],'version':version,'checked_utc':rec['ended_utc'],'read_sections':[section],'verified':verified,'limitations':limit,'linked_questions':[q],'stage':'common_start','receipt':f'common/{q}/open-{i}.json','duplicate_group':dup,'counted_minimum':bool(count and readable),'direct_original_read':readable,'body_excerpt_utf8_bytes':len(body.encode()),'server_bytes':'미계측'})
  if readable:
   candidates.append({'rank':len(candidates)+1,'name':name,'proposed_use':Q[q]['independent_partial_purpose'],'citations':[{'url':h['url'],'section':section,'source_id':source_id}],'opened_evidence':[f'common/{q}/open-{i}.json'],'limitations':limit})
 for h in hits[:10]:
  u=h['url'];r=h['rank']
  if r in ranks: reason='selected_first_eligible_original'; eligible=True
  elif any(x in u for x in ['nep-00','pep-0','peps.python','/python/peps/','bugs.python']):reason='proposal_process_or_followup_excluded';eligible=False
  elif ('highlight=' in u or q=='Q01' and 'github.com/mdn/content' in u): reason='visible_alias_or_mirror';eligible=False
  elif any(u.startswith(z) for p in providers[q] for z in p['prefixes']):reason='eligible_but_two_open_cap_reached';eligible=True
  elif q=='Q09' and 'docs.jax.dev' in u:reason='eligible_other_provider_but_two_open_cap_reached';eligible=True
  else:reason='third_party_explanation_or_unverified_original_provider';eligible=False
  h.update(eligible=eligible,selection_reason=reason,selected=r in ranks)
 exposures=[{'question_id':q,'stage':'common_search','observer':'root','exposure':'All provided response text retained; selection restricted to first ten. Root displayed beyond-ten response text for Q01/Q03/Q05 before noticing tool returns more than ten.' if q in ['Q01','Q03','Q05'] else 'Only first-ten search rows displayed to selector; full response retained for auditing.','beyond_ten_selected':False,'followup_snippets_visible':q in ['Q03','Q05','Q07','Q09','Q11'],'treatment':'Record exposure; do not count snippets as evidence or import later conclusions into frozen predicates.'}]
 (d/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
 (d/'exposures.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in exposures))
 start={'question_id':q,'stage':'common_start','neutral_query':Q[q]['neutral_query'],'query_receipt':f'common/{q}/search.json','top_ten':hits[:10],'provided_result_count':len(hits),'rank_definition':'provided appearance order; not global SERP rank or numeric source-ref suffix','opened':opens,'allowed_providers':providers[q],'budget':{'navigation':1,'body_opens':2,'body_successes':sum(x['status']=='readable_excerpt' for x in opens),'body_failures':sum(x['status']!='readable_excerpt' for x in opens)},'server_bytes':'미계측','selection_rule':'first two eligible provider originals; exact aliases skipped, ambiguous editions retained','frozen_input_commit':'3475576d56b4307bd75964b9a27dc2a60093efbf'}
 (d/'start.json').write_text(json.dumps(start,ensure_ascii=False,indent=2)+'\n')
 m.write_return(d/'baseline-return.json',{'question_id':q,'route':'C','candidates':candidates,'budget':start['budget'],'selector':'root cached-receipt reader','assessment':'No success labels assigned at generation; exact returned section coverage judged later.'})
print('Serialized six odd common packets without network requests.')
