from pathlib import Path
import json,datetime
p=Path(__file__).parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
entries=[
('B-R01','DIG36','https://www.sciencedirect.com/science/article/pii/S0360131519302647','publisher original open','403; only indexed abstract/intro visible','Author DIG list→publisher; OpenAlex DOI OA metadata closed/no accessible full location'),
('B-R02','DIG35','https://www.tandfonline.com/doi/full/10.1080/15391523.2020.1795956','publisher original open','403/full methods unavailable','https://www.trails.umd.edu/byrne author list→DOI only; OpenAlex closed'),
('B-R03','DIG32','https://www.sciencedirect.com/science/article/pii/S0742051X21002377','publisher original open','403; full methods unavailable','Author DIG/TRAILS list, institutional metadata and OpenAlex closed'),
('B-R04','SEARCH11','https://ila.onlinelibrary.wiley.com/doi/full/10.1002/jaal.1225','publisher original open','redirect to abstract; fulltext sign-in wall','Author/DOI listing plus OpenAlex: no full primary methods recovered'),
('B-R05','DIG31','https://www.sciencedirect.com/science/article/pii/S0360131522000902','publisher original open','403; abstract only','https://www.trails.umd.edu/byrne gives publisher link; OpenAlex closed'),
('B-R06','SEARCH7','https://www.sciencedirect.com/science/article/abs/pii/S0360131523001094','publisher original open','403; methods not read','https://cris.technion.ac.il/en/publications/misinformation-is-contagious-middle-school-students-learn-how-to-/ institution author abstract; OpenAlex closed'),
('B-R07','DIG22','https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID4104750_code2785140.pdf?abstractid=3936112','author manuscript archive download','403','Publisher supplementary task appendix and Stanford2019 precursor report recovered; sample difference unresolved'),
('B-R08','SEARCH6','https://epub.ub.uni-muenchen.de/108405/','institution author archive','Record explicitly says no fulltext; main paper unavailable','OSFhr5js independent author questionnaire fully read; all arms access sources'),
('B-R09','DIG33','https://www.tandfonline.com/doi/full/10.1080/07370008.2021.1908288','publisher original open/indexed notes','fullbody403; Notes1–2 visible as publisher text in search','Explicit same2019 participant cohort;not counted as directlyread complete report'),
('B-R10','DIG21','https://www.sciencedirect.com/science/article/pii/S2352250X23001823','publisher original open','403; review status available in publisher/PubMed metadata','No new primary human method claimed; no minimum count'),
('B-R11','B-DIAG-VRAGA','http://www.snopes.com/zika-virus-gmo-mosquitoes/','exact source URL from AppendixA','402; no article body','Canonical https://www.snopes.com/fact-check/zika-virus-gmo-mosquitoes/ also unavailable; 2016 WaybackCDX attempted'),
('B-R12','B-DIAG-VRAGA','http://www.cdc.gov/zika/disease-qa.html','exact source URL from AppendixA','404','Historical2016 WaybackCDX query attempted; WHO2016 independent original recovered instead,not a landing-page substitute'),
('B-R13','B-DIAG-VRAGA','https://web.archive.org/cdx/search/cdx?url=cdc.gov/zika/disease-qa.html&output=json&filter=statuscode:200&filter=timestamp:2016&collapse=digest','archive index query','tool inaccessible; returned count 미확인','Exact2016 original snapshot needed'),
('B-R14','B-DIAG-VRAGA','https://web.archive.org/cdx/search/cdx?url=snopes.com/zika-virus-gmo-mosquitoes/&output=json&filter=statuscode:200&filter=timestamp:2016&collapse=digest','archive index query','tool inaccessible; returned count 미확인','Exact2016 original snapshot needed'),
('B-R15','B-DIAG-VRAGA','http://www.who.int/emergencies/zika-virus/articles/rumours/en/','author truth original','404','2016WHO text mirrored at https://app.mhpss.net/?get=285/Dispelling-Rumours.pdf directlyread p2'),
('B-R16','B-DIAG-DISTRICT','https://www.givewell.org/charities/amf/November-2018-Version','author historical truth original','web fulltext succeeded; urllib200 was212byte challenge','Direct2018 Summary/Reviewprocess sections; current2023page checked separately,not substituted forhistory'),
('B-R17','DIG29','https://www.samwineburg.com/writing/paged-4/2/','author bibliography page2','success; preprint lineage explicit','https://stacks.stanford.edu/file/druid:mf412bt5333/Educating_for_Misunderstanding.pdf fullmethodsread; /writing/page2 route does not selectcorrect bibliography pagination'),
('B-R18','DIG22','https://purl.stanford.edu/xr124mv4805/iiif/manifest','author archive manifest','200','Manifest resolved originalCOR CurriculumEvaluationPDF; methodsfullread'),
('B-R19','DIG42','https://www.scribd.com/document/788438647/Can-Students-Evaluate-Online-Sources-Learning-From-Assessments-of-Civic-Online-Reasoning','full primary work mirror','fullMethodsread; uploader provenance unverified','PublisherDOI/title match; source counted as primary text with mirror caveat'),
('B-R20','DIG23','https://www.academia.edu/94127083/Improving_university_students_web_savvy_An_intervention_study','full primary work mirror','fullMethodsread; publisher abstract corroboratesidentity','Mirror provenance caveat; author-controlled archival copy not obtained'),
('B-R21','SEARCH10','https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/bjdp.12559','publisher original','fullMethodsread','Entered correctedfirst25 aftercohort merges; metadata was frozenbeforeoutcome reading'),
]
with (p/'search-log-addendum.jsonl').open('w') as f:
 for i,k,u,q,status,route in entries:
  d=dict(search_id=i,candidate_or_case=k,query_url=u,query=q,retrieved_utc_before=now,timestamp_semantics='post-read upper bound recorded after retrieval; initial tool timestamps not exported. HTTP receipts in retrieval-log have exact request UTC.',sort='해당 없음 for direct document; archiveCDX supplied filter, native order unavailable',filters='2018–2025 final publication for screen; historical truth targets allowed earlier; archiveyear2016 where URLspecifies',returned_count='1 target attempted; substantive/fulltext success described in status',total_results='해당 없음 for direct target; archiveindex total 미확인',status=status,recovery_route=route,minimum_read_count='Only full primary methods/sections count in sources.jsonl; no abstract/failure count',phase='post-freeze targeted method/source recovery')
  f.write(json.dumps(d,ensure_ascii=False)+'\n')
print('recovery rows',len(entries))
