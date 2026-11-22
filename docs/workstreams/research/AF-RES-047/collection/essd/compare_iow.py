import urllib.request,zipfile,hashlib,io,xml.etree.ElementTree as E,datetime,json,pathlib,concurrent.futures
P=pathlib.Path(__file__).parent
urls=['https://doi.iow.de/doi/2021/data-2021-0002/data-2021-0002.zip','https://doi.iow.de/doi/2021/data-2021-0002-01/data-2021-0002-01.zip']
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def fetch(u):
 f=urllib.request.urlopen(u,timeout=60);b=f.read();return {'source_url':u,'final_url':f.url,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'http_status':f.status,'content_type':f.headers.get('Content-Type'),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'valid_zip':zipfile.is_zipfile(io.BytesIO(b))},b
results=list(concurrent.futures.ThreadPoolExecutor(max_workers=2).map(fetch,urls));books=[];receipts=[]
for r,b in results:
 z=zipfile.ZipFile(io.BytesIO(b));r['members']=z.namelist();r['files']=[];book={}
 for name in z.namelist():
  if not name.endswith(('.xlsx','.docx')):continue
  data=z.read(name); zz=zipfile.ZipFile(io.BytesIO(data)); f={'name':name,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
  if name.endswith('.docx'):
   pp=[''.join(p.itertext()) for p in E.fromstring(zz.read('word/document.xml')).findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p')]
   print('DOCX',name)
   for i,s in enumerate(pp,1):
    if any(x in s for x in ['Data release','2021.','Group –','Taxa –']): print(i,s)
   f['paragraph_locator_notes']='Read release/date and Group/Taxa descriptors; exact locators printed during inspection and summarized below.'
  else:
   strings=[''.join(c.itertext()) for c in E.fromstring(zz.read('xl/sharedStrings.xml'))]
   wr=E.fromstring(zz.read('xl/workbook.xml'));rels=E.fromstring(zz.read('xl/_rels/workbook.xml.rels'));rm={x.get('Id'):x.get('Target') for x in rels}
   f['sheets']=[]
   for sheet in wr.findall('m:sheets/m:sheet',ns):
    target=rm[sheet.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')];sn='xl/'+target if not target.startswith('/') else target.lstrip('/')
    rt=E.fromstring(zz.read(sn)); cells={};formulas={}
    for c in rt.findall('m:sheetData/m:row/m:c',ns):
     v=c.find('m:v',ns); val=v.text if v is not None else ''
     if c.get('t')=='s':val=strings[int(val)]
     elif c.get('t')=='inlineStr':val=''.join(c.find('m:is',ns).itertext())
     if val!='':cells[c.get('r')]=val
     formula=c.find('m:f',ns)
     if formula is not None:formulas[c.get('r')]=formula.text
    book[sheet.get('name')]={'cells':cells,'formulas':formulas}
    f['sheets'].append({'name':sheet.get('name'),'nonempty_cells':len(cells),'formula_count':len(formulas),'selected_cells':{k:cells.get(k) for k in ['A2','I2','F4','G4','A5','B5','F5','G5']}})
  r['files'].append(f)
 receipts.append(r);books.append(book)
comparison={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'role':'auxiliary author-output editions, NOT WoRMS input editions','archive_receipts':receipts,'sheet_comparisons':[],'interpretation_limit':'Cell/formula comparisons ignore presentation and other XML metadata. Unchanged values cannot prove which edition consumer read; no original run observed.'}
for name in sorted(set(books[0])|set(books[1])):
 a=books[0].get(name,{});b=books[1].get(name,{}); row={'sheet':name,'present_v1':bool(a),'present_v2':bool(b)}
 if a and b:
  diffs=[]
  for key in sorted(set(a['cells'])|set(b['cells'])):
   if a['cells'].get(key)!=b['cells'].get(key):diffs.append({'cell':key,'v1':a['cells'].get(key),'v2':b['cells'].get(key)})
  fkeys=set(a['formulas'])|set(b['formulas']); fd=[key for key in fkeys if a['formulas'].get(key)!=b['formulas'].get(key)]
  row.update(different_cell_values=len(diffs),different_formulas=len(fd),first_cell_differences=diffs[:15],first_formula_difference_cells=fd[:15])
 if a and b and name!='Raw_Single_Measurments_Factors':
  def keyed(cells):
   out={}
   for key,value in cells.items():
    if key.startswith('A') and key[1:].isdigit() and int(key[1:])>=3:
     n=key[1:];out[value]={'row':int(n),'count':cells.get('B'+n),'WW_to_DW':cells.get('C'+n),'WW_to_AFDW':cells.get('D'+n)}
   return out
  ka,kb=keyed(a['cells']),keyed(b['cells'])
  changes=[]
  for taxon in sorted(set(ka)|set(kb)):
   av,bv=ka.get(taxon),kb.get(taxon)
   if av is None or bv is None or any(av.get(k)!=bv.get(k) for k in ['count','WW_to_DW','WW_to_AFDW']):changes.append({'taxon':taxon,'v1':av,'v2':bv})
  row['taxon_keyed_changes']=changes
  collisions=[]
  for k in a['cells']:
   if k.startswith(('B','C','D')) and k[1:].isdigit() and int(k[1:])>=3 and a['cells'][k]==b['cells'].get(k):
    taxona,taxonb=a['cells'].get('A'+k[1:]),b['cells'].get('A'+k[1:])
    if taxona and taxonb and taxona!=taxonb:collisions.append({'cell':k,'value_both':a['cells'][k],'taxon_v1':taxona,'taxon_v2':taxonb})
  row['same_numeric_cell_different_taxon_examples']=collisions[:3]
 if a and b and name=='Raw_Single_Measurments_Factors':
  row['changed_region_records']=[{'row':n,'v1':{col:a['cells'].get(col+str(n)) for col in ['A','B','F','G','N','Q','R','S']},'v2':{col:b['cells'].get(col+str(n)) for col in ['A','B','F','G','N','Q','R','S']}} for n in [7319,13310]]
 comparison['sheet_comparisons'].append(row)
print(json.dumps(comparison,ensure_ascii=False,indent=2))
(P/'iow-edition-comparison.json').write_text(json.dumps(comparison,ensure_ascii=False,indent=2)+'\n')
r=receipts[0];r['inspection_correction']='Earlier BadZipFile came from mistakenly attempting to parse an empty directory member as ZIP; source outer archive was valid. That diagnostic did not indicate HTML or publisher failure.'
(P/'iow-release1-receipt.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
