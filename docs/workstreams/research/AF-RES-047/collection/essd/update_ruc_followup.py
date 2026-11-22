import pathlib,json,csv,datetime,shutil,re,collections
P=pathlib.Path(__file__).parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
for fn in ['cases.json','sources.jsonl','consumers.csv','editions.csv','runs.csv','readings.csv','collection-check.json']:
 dest=P/(fn.rsplit('.',1)[0]+'-before-RUC.'+fn.rsplit('.',1)[1])
 if not dest.exists():shutil.copy2(P/fn,dest)
# Preserve provenance receipts while retaining factual observations rather than source bodies.
for fn in ['ruc-focused-fetches.json','ruc-focused-rootpaths.json','ruc-focused-format-stations.json']:
 records=json.loads((P/fn).read_text())
 for r in records:
  r.pop('content_text',None);r['links']=[u for u in r.get('links',[]) if not u.startswith('mailto:')]
  u=r['url']
  if u.endswith('/intl/'):
   r['locator']='NOAA/ESRL Radiosonde Database; Recent Activities; sectionsI Input Dates,II Sounding Specific Information,III Select Stations/Data'
   r['observations']='June2020 IGRA/GSL2018–2019 merge notice; July2020 stationinventory update; choose UTCperiod,WMO/WBAN,levels,windunits. Links to General_Information.html andinventory_2000-2020.lis.'
  elif 'General_Information' in u:
   r['locator']='OVERVIEW: REAL-TIME ARCHIVE; STATION HISTORY; DATABASE ACCESS SOFTWARE; Disclaimer'
   r['observations']='2007 merge of IGRA global GTS with GSL/ESRL observations contains more observations than either source; stationhistory is required for soundingoutput; binaryarchive can export2ASCII,GTS,NetCDF; reports include mandatory/significant/PPBB levels.'
  elif 'fsl_format' in u:
   r['locator']='FSL Rawinsonde data format; LEGEND:SOURCE,WSUNITS,PRESSURE,TEMP,DEWPT'
   r['observations']='First4lines metadata, then datalines; missing32767(original) or99999(new); TEMP/DEWPT in0.1°C, PRESSURE wholemb(original) or0.1mb(new), wind output chosenknots/0.1m/s; SOURCE4 identifies NCDC+GTS mergeddata. No station/dateprofile values here.'
  elif 'netcdf_format' in u:
   r['locator']='variables wmoStat,synTime,relTime,tpMan,tdMan,wsMan; globalversion'
   r['observations']='Example schema wmoStat,launch/synoptic times; tpMan temperaturekelvin, tdMan dewpointdepressionkelvin, wsMan m/s; missing99999; globalversion Forecast Systems Lab1.3 is schema/example version, not a consumer input release.'
  if 'inventory' in u:
   r['locator']='Inventory header WMO_ID,BDATE,EDATE,TOTAL and12monthlycounts; response first1048576bytes'
   r['observations']='Header describes2000–2020 station/year/month counts. Readable response is exactly1MiB and contains no78954 in returned segment; completeness not established, so no station-absence claim.'
   r.pop('head',None)
  if 'international_sites' in u:
   r['locator']='international_sites.txt complete returned text search78954/grantley/barbad; pairedwith stat2000.txt perGeneralInformation'
   r['observations']='No78954 match in this file; provider requires both international and NorthAmerican history. This absence is not no-station evidence.'
   r.pop('head',None);r.pop('tail',None)
 (P/fn).write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
# Twelve source opens, with root-path recovery and snapshot redirect kept separate.
sets=[]
for fn in ['ruc-focused-fetches.json','ruc-focused-followups.json','ruc-focused-rootpaths.json','ruc-focused-format-stations.json']:
 sets+=json.loads((P/fn).read_text())
sets.append(json.loads((P/'ruc-focused-north-america.json').read_text()))
assert len(sets)==12
sources=[json.loads(s) for s in (P/'sources.jsonl').read_text().splitlines() if int(json.loads(s)['source_id'].split('E')[1])<59]
for idx,r in enumerate(sets,59):
 url=r['url'];fin=r.get('final_url');ok=r.get('status')==200
 original=re.sub(r'^https://web.archive.org/web/[^/]+/','',url)
 cap=re.search(r'/web/(\d{14})',fin or '')
 count=idx==60
 loc=r.get('locator','HTTP access result')
 confirmed=r.get('observations',r.get('error','Response read'))
 limitations='Archive capture date is distinct from provider publication/update and target observation time. No1994–2016 consumer trainingexport, originalrun or LWPvalue identified.'
 if idx==59:limitations+=' Requested2022-01-19 redirected to2023-01-04; do not treat as2022snapshot.'
 if idx==66:limitations+=' Inventory returned exactly1MiB; no inference from missing78954 in returned portion.'
 if idx==70:
  loc='stat2000.txt physical lines90–91, WMO78954; raw field values, datehistory'
  confirmed='WMO78954/SEAWELL APT: fields13.07,59.50,56 for19650730–19711026; fields13.07,59.50,47 for19711027–99999999. File requested2021-12-05, actualcapture2022-07-06.'
  limitations+=' Historicalstationmetadata differs from consumerTableA1; coordinateencoding/sign convention and inputexport choice unresolved. Not an LWP mismatch.'
 s={'source_id':'S-E%03d'%idx,'work_id':'NOAA-RUC-ESRL-GSL-radiosonde-archive','edition_id':('webcapture:'+cap.group(1)) if cap else None,'source_url':original,'final_url':fin or url,'archive_request_url':url if 'web.archive.org' in url else None,'capture_timestamp_utc':cap.group(1) if cap else None,'publisher':'NOAA ESRL/GSL; Internet Archive preserves original provider content','kind':'publisher_archive_original' if ok else 'access_failure','published_date':None,'modified_date':None,'checked_utc':r['utc'],'first_opened_utc':r['utc'],'locator':loc,'confirmed':confirmed,'limitations':limitations,'questions':['Q3','Q4','Q5','Q7'],'case_ids':['N-E02'],'duplicate_of':None if count else 'S-E060','count_toward_minimum':count,'quota_category':'publisher_edition_file_correction' if count else None,'status':'opened' if ok else 'access_failed','sha256':r.get('sha256'),'byte_count':r.get('bytes'),'time_note':'Archivecapture,providercontentupdate,targetobservationperiod,and researchercheckUTC are separate axes.'}
 sources.append(s)
# Retrieval indices are evidence of discovery/access, not extra publisher originals.
metadata=[
('https://archive.org/wayback/available?url=ruc.noaa.gov%2Fraobs%2Fintl%2F&timestamp=20211223','2026-11-22T22:35:31.330258+00:00','Wayback available API reportsclosest20220119054955; actualfetchredirected2023; indexalone isnotcontent'),
('https://web.archive.org/cdx/search/cdx?url=ruc.noaa.gov%2Fraobs%2Fintl%2F&output=json&filter=statuscode%3A200&collapse=timestamp%3A4&fl=timestamp,original,statuscode,mimetype&from=2020&to=2022','2026-11-22T22:35:31.301483+00:00','CDX lists20201218094634 and20220119054955 HTTP200 HTML captures; actualcontent fetched separately'),
('https://archive.org/wayback/available?url=ruc.noaa.gov%2Fraobs%2FGeneral_Information.html&timestamp=20211223','2026-11-22T22:37:29.367967+00:00','API finds20211205084551; actualGeneralInformationbody read atsamecapture'),
('https://web.archive.org/cdx/search/cdx?url=ruc.noaa.gov%2Fraobs%2Fintl%2FGeneral_Information.html&output=json&filter=statuscode%3A200&collapse=timestamp%3A4&fl=timestamp,original,statuscode,mimetype','2026-11-22T22:37:29.819854+00:00','EmptyCDX result forwrong/intl/relativepath; rootpath subsequentlyfound'),
('https://web.archive.org/cdx/search/cdx?url=ruc.noaa.gov%2Fraobs%2Fintl%2Finventory_2000-2020.lis&output=json&filter=statuscode%3A200&collapse=timestamp%3A4&fl=timestamp,original,statuscode,mimetype','2026-11-22T22:37:29.777571+00:00','EmptyCDX result forwrong/intl/relativepath; rootpath subsequentlyfound')]
for idx,(u,t,what) in enumerate(metadata,71):
 sources.append({'source_id':'S-E%03d'%idx,'work_id':'InternetArchive-retrieval-index','edition_id':None,'source_url':u,'final_url':u,'publisher':'InternetArchive','kind':'archive_retrieval_metadata','published_date':None,'modified_date':None,'checked_utc':t,'first_opened_utc':t,'locator':'JSONAPIresponse','confirmed':what,'limitations':'Metadata only, not original content or actualdataset bytes. No minimum count.','questions':['Q3','Q4'],'case_ids':['N-E02'],'duplicate_of':None,'count_toward_minimum':False,'quota_category':None,'status':'opened'})
for idx,(u,ref) in enumerate([('https://web.archive.org/web/20220119054955/https://ruc.noaa.gov/raobs/intl/','turn651189980view0'),('https://web.archive.org/web/20201218094634/https://ruc.noaa.gov/raobs/intl/','turn651189980view1')],76):
 sources.append({'source_id':'S-E%03d'%idx,'work_id':'NOAA-RUC-ESRL-GSL-radiosonde-archive','edition_id':None,'source_url':u,'final_url':u,'publisher':'InternetArchive/NOAA','kind':'tool_fetch_failure','published_date':None,'modified_date':None,'checked_utc':now,'first_opened_utc':None,'locator':'webopen tool failed','confirmed':'Search retrieval tool couldnotaccess thisarchive URL; independenturllibfetchsucceeded','limitations':'Toolfailure notsourceabsence; seeS-E059/060. Exactwebcalltime notcaptured separately.','questions':['Q3'],'case_ids':['N-E02'],'duplicate_of':'S-E060','count_toward_minimum':False,'quota_category':None,'status':'tool_fetch_failed','web_ref':ref})
(P/'sources.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in sources))
cases=json.loads((P/'cases.json').read_text())
for c in cases:
 if c['case_id']!='N-E02':continue
 c['publisher_object_exists']=True
 c['publisher_first_attempted_utc']='2026-11-22T22:09:34Z'
 c['publisher_first_opened_utc']='2026-11-22T22:36:01.356013+00:00'
 c['publisher_time_note']='Initial currentendpoint attempt failed; actual originalproviderbody firstread through2020archive at22:36:01UTC.'
 c['publisher_locator']='CurrentRUC unavailable; originalNOAA index archive2020-12-18, GeneralInformation2021-12-05, FSL/NetCDF formats andstat2000 actualcapture2022-07-06; no trainingprofilefile'
 c['publisher_edition']='미확인: publisher archive/format/history content recovered; capture IDs and formatversionFSL1.3 are not actual1994–2016 trainingexport edition'
 c['publisher_value']='Primary LWP input-to-output value 미확인. Auxiliary originalNOAA stationhistory78954 fields differ fromTableA1, with capture/validtime/encoding limits.'
 c['missing_reason']='Originalprovider documents and stationhistory recovered via archived original URLs, but actual RUC trainingexport, selectedfileformat, samplemembership/seed/weights and runID remainmissing; own235output nottrainingedition.'
 c['source_ids']=list(dict.fromkeys(c['source_ids']+['S-E%03d'%i for i in range(59,78)]))
 extras=[sources[i-1]['final_url'] for i in [60,65,68,69,70]]
 for conf in ['B','C']:c[conf]['visible_urls']=list(dict.fromkeys(c[conf]['visible_urls']+extras))
 c['B']['evidence']='CurrentRUCfails, but originalNOAA indexcapture2020-12-18 andGeneralInformation2021-12-05 read; originalprovider explainsIGRA+GSLmergedarchive andstationhistory dependency. 2022formatcaptures distinguishASCII0.1°C fromNetCDFkelvin, old/newmissingcodes; noactualtrainingprofiles.'
 c['B']['new_fact']='B−A (revised after focusedarchivefollowup): publisher originaldocumentation and sourcefamily recovered; format/level/units/history choices affect export. Capturedate or FSL1.3schema doesnot identify consumedinputedition.'
 c['B']['judgment']='발행자 원문 열람 회복. 실제 훈련판·소비자 판 명시·실행·원 입력값은 미확인; 단순 IGRA 대체 불가.'
 c['C']['judgment']='당대 코드와 발행자 형식/이력은 읽었으나 실제 훈련 export와 실행 연결은 보류; codehash, schema version, archivecapture를 input/run 증거로 승격하지 않음.'
(P/'cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
# Apply changed case fields to existing tables without altering original/sensitivity selection.
for name in ['consumers.csv','editions.csv']:
 with (P/name).open() as f:reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
 byid={c['case_id']:c for c in cases}
 for row in rows:
  for k in fields:
   if k in byid[row['case_id']]:row[k]=byid[row['case_id']][k]
 with (P/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
with (P/'readings.csv').open() as f:reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
for row in rows:
 c=next(c for c in cases if c['case_id']==row['case_id']);x=c[row['configuration']]
 row.update(visible_urls=' ; '.join(x['visible_urls']),evidence=x['evidence'],judgment=x['judgment'],new_fact=x['new_fact'])
with (P/'readings.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
with (P/'runs.csv').open() as f:reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
for row in rows:
 if row['case_id']=='N-E02':row['resume_first_action']='Obtainauthor RUC1994–2016 trainingexport with WMO/launch/samplekeys, selectedFSLorNetCDFformat/units/levels/missingcode and filehash; then connect originalrandomsplit/weights/runmanifest. Archivedproviderdocs are nowavailable; do not repeat broadservice search.'
with (P/'runs.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
check=json.loads((P/'collection-check.json').read_text());counted=[s for s in sources if s['count_toward_minimum']]
assert len(sources)==77 and len(counted)==8 and len({s['work_id'] for s in counted})==8
check.update(checked_utc=now,source_records=len(sources),counted_unique_works=len(counted),quota=dict(collections.Counter(s['quota_category'] for s in counted)))
check['checks'].append('RUC originalwork recovered through archive; all relatedpages/captures countonce; P/U/R/V unchanged')
(P/'collection-check.json').write_text(json.dumps(check,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'sources':len(sources),'quota':check['quota'],'strict_flags':check['main_flags'],'RUCoriginalcounted':'S-E060','newdirectopens':'S-E059–070','retrievalrecords':'S-E071–077'},ensure_ascii=False,indent=2))
