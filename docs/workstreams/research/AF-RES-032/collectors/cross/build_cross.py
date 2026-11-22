from pathlib import Path
import json, hashlib, datetime, csv, re, html
from html.parser import HTMLParser
P=Path(__file__).resolve().parent
C=P/'cache'; now=datetime.datetime.now(datetime.timezone.utc).isoformat()
(P/'.gitignore').write_text('cache/\n')
receipts=json.loads((C/'downloads.json').read_text())+json.loads((C/'data-downloads.json').read_text())
known={x['file']:x for x in receipts if 'sha256' in x}
archive_receipt=json.loads((C/'momabarr-receipt.json').read_text())
archive_receipt['file']='momabarr.html'
known['momabarr.html']=archive_receipt
receipts.append(archive_receipt)
urls={
'onsqna2023.html':'https://www.ons.gov.uk/economy/grossdomesticproductgdp/bulletins/quarterlynationalaccounts/januarytomarch2023',
'momaobject.html':'https://www.moma.org/collection/works/79269',
'momainstall.html':'https://www.moma.org/calendar/exhibitions/2748/installation_images/12499',
'momaart.jpg':'https://www.moma.org/media/W1siZiIsIjE1MTE2MyJdLFsicCIsImNvbnZlcnQiLCItcXVhbGl0eSA5MCAtcmVzaXplIDIwMDB4MjAwMFx1MDAzZSJdXQ.jpg?sha=4a6add15d32a7790'}
for f,u in urls.items():
 b=(C/f).read_bytes(); r={'file':f,'url':u,'final_url':u,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'observed_utc':now,'timestamp_note':'원 bytes를 이 시각 재독·해시 확인. 다운로드 시각 자체는 별도 receipt 없음; 파일 mtime을 역사 사건일로 사용하지 않음.'}; known[f]=r;receipts.append(r)
(P/'download-receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
def s(i,f,kind,pub,ver,date,loc,verified,limits,case,count=True,group=None,url=None):
 r=known.get(f,{})
 return {'source_id':i,'source_type':kind,'publisher':pub,'original_url':url or r.get('url'),'version':ver,'publication_date':date,'publication_date_proof':'발행자 본문/판면에서 읽은 날짜; 처음 웹 게시된 정확 시각은 미확인','observed_utc':r.get('observed_utc',now),'read_location':loc,'verified':verified,'limitations':limits,'questions':['Q7','Q8'],'case_ids':[case],'duplicate_group':group or i,'count_minimum':count,'category':'cross_field','directly_read':True,'artifact_sha256':r.get('sha256'),'artifact_bytes':r.get('bytes'),'capture_file':('cache/'+f) if f else None,'cache_is_not_committed':True}
S=[
s('X-S01','ons2022.html','official annual statistical chapter','ONS','Blue Book 2022','2022-10-31','Introduction; §2 Figure1; Cite this chapter','명시2022판의 2021 실질 연간GDP성장률7.5%. 2020값-11.0%.','현재 보존된 연도페이지는2023-01-23 notice를 포함한다. 2022당일 원 bytes 불변성·최초공개UTC 미확인.','X-STAT01'),
s('X-S02','onsqna2023.html','official quarterly statistical table','ONS','QNA January–March2023','2023-06-30','§2 Table1 row2021, column Chained volume measures GDP','2021 연간 값7.6. 같은 표에서 실질·명목·인구당 칸을 분리한다.','2022연차판과 같은 data vintage가 아니다. 표 조회시각을 데이터시행일로 사용하지 않음.','X-STAT01'),
s('X-S03','onsnotice.html','official revision announcement','ONS / Niamh McAuley','Impact of Blue Book2023','2023-09-01','§2 bullets; §4 paragraph on latest QNA; §5 Figure3','2021 실질성장8.7%, 직전추정7.6%대비+1.1pp; Q4수준 회복판정 변경.','2022연차판7.5와 이 공표의직전7.6을 같은 판으로 합치면 안 된다. 사전 indicative 공표와 완전연차판출판은 별개.','X-STAT01'),
s('X-S04','ons2023.html','official annual statistical chapter','ONS','Blue Book2023','2023-10-31','Overview; §2 Figure1','2021성장8.7%,2020 -10.4%; 앞으로도 개정될 수 있음을 명시.','2026현재 최신값이라는 주장이 아님. 단순파일명만 다른 동일본문이 아니라 수치가 다른 별도판이다.','X-STAT01'),
s('X-S05','boe2023.html','external official citing report','Bank of England MPC','Monetary Policy Report November2023','2023-11-02','Box C: How has Blue Book2023 changed past estimates; raw HTML anchor Blue Book2023','연례개정이 과거GDP 판단을 어떻게 바꿨는지 설명하며 X-S03의 날짜고정URI를 실제 href로 인용한다.','같은 소비자가 옛URL에서 새URL로 수정한 이력·실제독자클릭은 미확인. 보고서자체의2023맥락을2026현재조언으로 바꾸지 않음.','X-STAT01'),
s('X-S06','moma1936.pdf','original exhibition catalogue scan','MoMA / Alfred H. Barr Jr.','Cubism and Abstract Art,1936','1936','PDF1-based14(preface printp9);126(Fig114);127(printp124);218(printp215,no152)','Fig114와목록152의 작품은1914표기. 전시서문이역사적서술임을 명시한다.','259PDF페이지와258웹목록은 스캔래퍼 차이일 수 있으나 원인미확인. 현재스캔게시일·개체재연대시점 미확인.','X-MUS01'),
s('X-S07','momaobject.html','current museum object record','MoMA','Object248.1935; collection/works/79269',None,'heading; medium/dimensions/objectnumber; provenance; gallery label','현재표제 Suprematist Composition: Airplane Flying,1915(뒷면1914기재). 이미지와크기·소장처를원목록152와대조했다.','정확한재연대결정일·웹수정일 미확인. 현재기록의역사전시연도/소유이력은출판시각이 아님.','X-MUS01'),
s('X-S08','lowry.pdf','public scholarly catalogue essay citing original','MoMA / Glenn D. Lowry','Abstraction in1936: Barr’s Diagrams; Inventing Abstraction1910–1925','2012','PDFp1–3=printedpp358–363; plate452;1941letterdiscussion and note3','1936카탈로그표지와초안의논증을역사적으로비교;1941수정지시도별도단계로서술한다.','현재개체인명·연대정정문이 아니며1936책을최신작품record로치환할근거가 아님.1941편지원본은직접열지않음.','X-MUS01'),
s('X-S09','momaexhibit.html','official exhibition publication locator','MoMA','Exhibition2748',None,'Publications; rendered catalogue listing; supplemental-links pdfs attribute','1936전시와카탈로그PDF를연결. 원HTML은href대신custom-element pdfs필드에주소를둔다.','카탈로그의독립내용으로중복산입하지않음. currentpage의최초게시일미확인.','X-MUS01',False,'X-S06'),
s('X-S10','momainstall.html','current metadata for archival installation photograph','MoMA; photograph Beaumont Newhall','IN46.35B;installation_images/12499',None,'photograph caption; Works identified link to79269','사진메타데이터가1936전시를가리키고현재작품79269로연결한다.','2018–19기계식별사업/후속직원식별의개별날짜 미확인. 사진촬영시점이현재웹메타데이터출판일은아님.','X-MUS01',False,'X-S07'),
s('X-S11','momabarr.html','current archival finding aid','MoMA Archives / Elena Cordova','Alfred H.Barr Jr.Papers;reprocessed2016','2016','Arrangement; Subseries VII.B description; entries VII.B.4 and VII.B.5','2016 재처리와 원질서 보존 원칙을 명시한다. VII.B.5는 1936년 원 책 표지이고, 별도 VII.B.4는 1937년 교정판의 dummy로 기술된다.','폴더 내용 원본은 열지 않았다. 1937년 dummy의 존재는 정정판 공개 출판을 증명하지 않는다. 현재 finding aid는 보조 기록으로 최소수 미산입.','X-MUS01',False,'X-S11',url='https://www.moma.org/research/archives/finding-aids/Barrb.html'),
s('X-S12',None,'official publication metadata','MoMA','Malevich artist record3710',None,'Publications, Inventing Abstraction entry','Lowry발췌의모책은2012년출판376쪽전시카탈로그로등재.','모책전체나발췌PDF의최초업로드일을확인한것은아님.메타데이터보강용으로최소수미산입.','X-MUS01',False,'X-S08',url='https://www.moma.org/artists/3710-kazimir-malevich'),
s('X-S13','ons2022.csv','official CSV serialization of Figure1','ONS','Blue Book2022 Figure1',None,'CSV rows2020/2021','다운로드CSV에서도2021값7.5를읽음.','같은도표의다른직렬화이므로X-S01와중복;별도원문수아님.','X-STAT01',False,'X-S01'),
s('X-S14','ons2023.csv','official CSV serialization of Figure1','ONS','Blue Book2023 Figure1',None,'CSV rows2020/2021/2022','다운로드CSV에서도2021값8.7을읽음.','같은도표의다른직렬화이므로X-S04와중복;별도원문수아님.','X-STAT01',False,'X-S04')]
(P/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in S))
class Anchors(HTMLParser):
 def __init__(self):super().__init__();self.current=None;self.out=[]
 def handle_starttag(self,t,a):
  if t=='a':self.current={'raw_tag':self.get_starttag_text(),'attributes':dict(a),'link_text':''}
 def handle_data(self,d):
  if self.current:self.current['link_text']+=d
 def handle_endtag(self,t):
  if t=='a' and self.current:self.out.append(self.current);self.current=None
links=[]
for f,source,match in [('boe2023.html','X-S05','impactofbluebook2023'),('ons2022.html','X-S01','52fea6e6&format=csv'),('ons2023.html','X-S04','40820add&format=csv'),('momainstall.html','X-S10','/collection/works/79269')]:
 a=Anchors();a.feed((C/f).read_text())
 for x in a.out:
  if match in x['attributes'].get('href',''):
   x.update(source_id=source,base_url=known[f]['url'],raw_href=x['attributes']['href'],context_status='아래 purposes의 한국어는판독요약이며원문인용아님');links.append(x)
(P/'citations.json').write_text(json.dumps({'read_utc':now,'links':links,'museum_print_citation':{'source_id':'X-S08','raw_citation_url':None,'citation_role':'plate452 references1936exhibitioncatalogue;printcitation,notliteralURL','researcher_locator':known['moma1936.pdf']['url'],'purpose':'1936전시카탈로그표지의도식·초안·후속수정을역사적으로비교'}},ensure_ascii=False,indent=2)+'\n')
cases=[{'case_id':'X-STAT01','domain':'public_statistics','software_denominator':False,'sources':['X-S01','X-S02','X-S03','X-S04','X-S05'],'observed_reference':'BankofEngland2023-11-02 BoxC→ONS2023-09-01 actualHTMLhref','purpose_from_public_text':'과거GDP측정이2023개정에따라어떻게달라졌는지해석','keep_evidence':'그시점의판단/보고서재현에는해당날짜판과이전추정판을함께보존','replace_evidence':'현재최선추정값을묻는별도사용에는기준연도뿐아니라새vintage와현개정표를확인해야함','unresolved':'이BoE본문의실제href수정이력·독자열람·오인피해·2026최신값','counterexample':'2022연차판의7.5와2023개정공표가비교하는직전7.6이달라,연도/BlueBook이름만으로개정량을계산하면틀림','not_latency':'2023-09-01→2023-11-02는공표와날짜있는인용의간격일뿐같은참조의정정전파지연은아님','next_material':'BoE직전출판판BoxC/해당문단의불변HTML또는PDF와변경이력1쌍'},
{'case_id':'X-MUS01','domain':'museum_archive','software_denominator':False,'sources':['X-S06','X-S07','X-S08','X-S09','X-S10','X-S11','X-S12'],'observed_reference':'Lowry2012plate452→1936cataloguehistoricalobject;MoMAcurrentinstallationrecord→currentartwork79269','purpose_from_public_text':'Lowry는1936표지의기원·초안·후속변형을비교한다.1936카탈로그서문은역사적조사임을명시한다.','keep_evidence':'당시전시주장과카탈로그표기복원은원판을보존하고현재개체를병기','replace_evidence':'현재박물관분류를묻는경우현object248.1935의1915및뒷면1914기재를사용','unresolved':'재연대시행일·카탈로그원스캔최초공개일·독자실패보고·Lowry가작품152연대를의식해판을유지했는지','counterexample':'원판figure114/catalogue152는1914,현개체는1915(verso1914).대상이같아도문서의역할/시점이다름','identity_method':'Fig114를현재이미지와시각대조:검정기하형·대각노랑형/가로띠배치일치.원크기23x19in와현재22⅞x19in의근접·MoMA소장표기·1936사진작품식별로교차확인.1936목록에현재objectnumber는없음.','not_latency':'1914/1915는작품연대,1936은전시/카탈로그연도,1999는소장권확인,2026은관측;이를수정지연쌍으로사용하지않음','next_material':'MoMA작품248.1935재연대결정의날짜있는원장/카탈로그raisonné근거1건'}]
(P/'cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
# Numeric source snippets are facts, not whole-page copies.
(P/'edition-values.csv').write_text('source_id,reference_year,publication_date,metric,value,units\nX-S01,2021,2022-10-31,real_annual_GDP_growth,7.5,percent\nX-S02,2021,2023-06-30,real_annual_GDP_growth,7.6,percent\nX-S03,2021,2023-09-01,real_annual_GDP_growth_indicative,8.7,percent\nX-S04,2021,2023-10-31,real_annual_GDP_growth,8.7,percent\nX-S06,artwork_152,1936,represented_artwork_year,1914,year\nX-S07,artwork_248.1935,,current_artwork_year,1915,year\n')
A=[{'attempt_id':'X-T01','query':'site.ons.gov.uk GDP Blue Book 2023 2021 0.6% below 8.7 revision','result':'ONSoriginalnoticefound','count_minimum':False},
{'attempt_id':'X-T02','query':'site.obr.uk 2023 GDP revisions 2021 forecast 2020 ONS vintage','result':'OBRfoundbutwebopen403;replacedbyaccessibleBoEreport','count_minimum':False},
{'attempt_id':'X-T03','url':'https://obr.uk/efo/economic-and-fiscal-outlook-november-2023/','method':'webopenandplainurllib','result':'403;notcounted','count_minimum':False},
{'attempt_id':'X-T04','url':known['moma1936.pdf']['url'],'method':'webopen','result':'contentlength49582898too_large;plainurllib403;ordinarybrowserUserAgentpublicGET200thenPDFread','count_minimum':False},
{'attempt_id':'X-T05','url':'https://www.moma.org/documents/moma_catalogue_2024_300061829.pdf','method':'webopen','result':'contentlength20367519too_large;notreadnotcounted','count_minimum':False},
{'attempt_id':'X-T06','query':'site.metmuseum.org art collection Rembrandt 1920 Gorget','result':'nousefulprimarycandidateinreturnedresults;notpursued','count_minimum':False},
{'attempt_id':'X-T07','query':'site.moma.org calendar exhibitions Cubism and Abstract Art 1936 catalogue','result':'1936officialarchivefound','count_minimum':False},
{'attempt_id':'X-T08','query':'site.ons.gov.uk National accounts at a glance 2022 7.5','result':'2022editionfoundandread','count_minimum':False},
{'attempt_id':'X-T09','query':'site.moma.org Cubism and Abstract Art 1911 The Portuguese','result':'nochosenartwork;subsequentinstallationviewused','count_minimum':False},
{'attempt_id':'X-T10','query':'site.moma.org/documents/moma_catalogue European 1930;site.moma.org New Photography 2010 publication','result':'alternativesfound;1930PDFoversize,2010notneededafter1936retrieval','count_minimum':False},
{'attempt_id':'X-T11','query':'site.moma.org/collection/works Barr Cubism and Abstract Art;site.moma.org Alfred H. Barr diagram collection','result':'officialLowryessayandfindingaidfound;currentartworkvia1936installationrecord','count_minimum':False},
{'attempt_id':'X-T12','query':'site.moma.org Inventing Abstraction 1910–1925 2012 catalogue Lowry;site.moma.org Inventing Abstraction 359 2012','result':'officialpublicationmetadatafoundandopened','count_minimum':False},
{'attempt_id':'X-T13','method':'webclickONSCSV2022/2023','result':'unsupportedapplication/octet-stream;ordinarypublicGETsucceededandrowsread','count_minimum':False}]
for x in A:x.update(recorded_utc=now,precision_note='사후시도원장작성UTC;개별검색의정확실행초미기록')
(P/'attempts.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in A))
(P/'QA.json').write_text(json.dumps({'checked_utc':now,'collector':'/root/cross_fields','same_worker_recheck':True,'external_independent_review':False,'sources_recorded':len(S),'unique_minimum_counted':sum(x['count_minimum'] for x in S),'cases':2,'software_denominator_added':0,'raw_html_link_verified':'BoEBoxC→ONSnotice','pdf_visual_check':['moma1936.pdfp126figure114','moma1936.pdfp218catalogue152','lowry.pdfp1plate452','currentmomaart.jpg'],'pdf_sha256':known['moma1936.pdf']['sha256'],'deliberate_historical_intent_scope':'Lowry1936chartanalysisexplicit;artwork152datepreservationintentinthatessayunconfirmed','proper_date_separation':True,'no_latency_estimate':True,'source_duplicates_excluded':['X-S09','X-S10','X-S11','X-S12','X-S13','X-S14']},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'sources':len(S),'counted':sum(x['count_minimum'] for x in S),'cases':len(cases),'files':[x.name for x in P.iterdir() if x.name!='cache']},ensure_ascii=False))
