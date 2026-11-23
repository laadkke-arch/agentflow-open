import urllib.request,urllib.parse,json,concurrent.futures,datetime
from pathlib import Path
p=Path(__file__).parent
names=[
('DIG21','Teaching lateral reading: Interventions to help people read like fact checkers'),
('DIG22','Lateral reading on the open Internet: A district-wide field study in high school government classes'),
('DIG23','Improving university students web savvy: An intervention study'),
('DIG24','Lateral reading: College students learn to critically evaluate internet sources in an online course'),
('DIG25','Measuring what matters: Investigating what new types of assessments reveal about students online source evaluations'),
('DIG26','Students civic online reasoning: A national portrait'),
('DIG27','Civic Online Reasoning Across the Curriculum: Developing and Testing the Efficacy of Digital Literacy Lessons'),
('DIG28','Critical ignoring as a core competence for digital citizens'),
('DIG29','Civic preparation for the digital age: How college students evaluate online sources about social and political issues'),
('DIG30','Preparing college students for a digital age: A survey of instructional approaches to spotting misinformation'),
('DIG31','Conversations after lateral reading: Supporting teachers to focus on process, not content'),
('DIG32','Challenging approaches: Sharing and responding to weak digital heuristics in class discussions'),
('DIG33','Internet or archive? Expertise in searching for digital sources on a contentious historical question'),
('DIG34','Educating for misunderstanding'),
('DIG35','Who is behind this? Preparing high school students to evaluate online content'),
('DIG36','Learning to evaluate: An intervention in civic online reasoning'),
('DIG37','Civic online reasoning: Curriculum evaluation'),
('DIG40','Lateral reading and the nature of expertise: Reading less and learning more when evaluating digital information'),
('DIG42','Can students evaluate online sources? Learning from assessments of civic online reasoning'),
('SEARCH1','Online searches to evaluate misinformation can increase its perceived veracity'),
('SEARCH2','I do not believe you: how providing a source corrects health misperceptions across social media platforms'),
('SEARCH3','Using expert sources to correct health misinformation in social media'),
('SEARCH4','Improving college students fact-checking strategies through lateral reading instruction in a general education civics course'),
('SEARCH5','Lateral reading and monetary incentives to spot disinformation about science'),
('SEARCH6','Sourcing against misinformation: Effects of a scalable lateral reading training based on cognitive apprenticeship'),
('SEARCH7','Misinformation is contagious: Middle school students learn how to evaluate and share information responsibly through a digital game'),
('SEARCH8','I Don’t Think That’s True, Bro! Social Corrections of Misinformation in India'),
('SEARCH9','The advantage of videos over text to boost adolescents lateral reading in a digital workshop'),
('SEARCH10','Trust issues: Adolescents epistemic vigilance towards online sources'),
('SEARCH11','Guiding their thinking: A formative study of digital source evaluation'),
('SEARCH12','See something, say something: Correction of global health misinformation on social media'),
('SEARCH13','Boosting media literacy using lateral reading and online search interventions'),
('SEARCH14','Debriefings in misinformation research should include fact-checks to correct misperceptions and increase perceived learning')
]
def one(pair):
 key,title=pair
 url='https://api.crossref.org/works?'+urllib.parse.urlencode({'query.title':title,'rows':3})
 ts=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(url,timeout=25) as r:j=json.load(r)
  items=[]
  for a in j['message']['items']:
   items.append({k:a.get(k) for k in ['DOI','title','published','published-online','published-print','type','URL','container-title']})
  return {'discovery_key':key,'query':title,'url':url,'accessed_utc':ts,'result_count_returned':len(items),'total_results':j['message'].get('total-results'),'sort':'relevance default; first3 metadata matches only','items':items}
 except Exception as e:return {'discovery_key':key,'query':title,'url':url,'accessed_utc':ts,'error':repr(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as e:
 out=list(e.map(one,names))
(p/'crossref-metadata.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
for r in out:
 print(r['discovery_key'],r['query'])
 for x in r.get('items',[])[:1]:print(json.dumps(x,ensure_ascii=False))
 if 'error' in r:print(r['error'])
