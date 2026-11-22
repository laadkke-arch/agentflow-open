"""Recheck audit values, not an original R execution.

Run before raw-object disposal, or in an isolated owned-path replay
directory after retrieving the inputs at the URLs/hashes in the receipts.
Requires rdata1.1.0 and xarray2026.9.0 (or the recorded local wheels).
"""
import csv,datetime,hashlib,json,re,statistics,sys,warnings
from pathlib import Path
P=Path(__file__).resolve().parent

def iris_stats(rows):
    groups={r[4] for r in rows}
    mean=statistics.mean(float(r[2]) for r in rows)
    between=sum(sum(r[4]==g for r in rows)*(statistics.mean(float(r[2]) for r in rows if r[4]==g)-mean)**2 for g in groups)
    return dict(rows=len(rows),species_df=len(groups)-1,sum_sq=between)

iris=[]
for name in ['R-4.2.0-iris.R','R-4.2.1-iris.R']:
    path=P/'objects'/name
    if not path.exists():
        raise SystemExit('Raw objects were disposed. See RAW_DISPOSITION.md and replay downloads in an isolated owned-path directory.')
    text=path.read_text()
    columns={k:[float(x.strip()) for x in re.search(re.escape(k)+r' = c\((.*?)\)',text,re.S).group(1).split(',')] for k in ['Sepal.Length','Sepal.Width','Petal.Length','Petal.Width']}
    assert all(len(v)==150 for v in columns.values())
    assert 'Species = gl(3,50, label = c("setosa", "versicolor", "virginica"))' in text
    rows=[[*[columns[k][i] for k in columns],['setosa','versicolor','virginica'][i//50]] for i in range(150)]
    iris.append(dict(file=name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),**iris_stats(rows)))
for name in ['uci-iris.data','uci-bezdekIris.data']:
    rows=[r for r in csv.reader((P/'objects'/name).read_text().splitlines()) if r]
    iris.append(dict(file=name,**iris_stats(rows)))
assert all(x['species_df']==2 for x in iris)
assert iris[0]['sha256']==iris[1]['sha256']=='77af4424d5361afe1c46e7fb95bc4f95681f5515a586cb41c062b111c691dc5c'
assert [round(x['sum_sq'],1) for x in iris]==[437.1,437.1,436.6,437.1]

for wheel in (P/'objects').glob('*.whl'):
    sys.path.insert(0,str(wheel))
import rdata
constructors={**rdata.conversion.DEFAULT_CLASS_MAP,**{k:lambda obj,attrs:obj for k in ['data.frame','tbl_df','grouped_df','tbl']}}
with warnings.catch_warnings(record=True) as warning_records:
    meta=rdata.conversion.convert(rdata.parser.parse_file(P/'author/target_meta.RDS'),constructor_dict=constructors)
    features=rdata.conversion.convert(rdata.parser.parse_file(P/'author/data/syntax_feature_yr1998.RDS'),constructor_dict=constructors)
paths={str(p) for p,y in zip(meta['path'],meta['year']) if y==1998}
assert len(paths)==16 and paths==set(features['path'])
flags=[bool(flag) for pkg in features['function_feat'] if pkg['result'] is not None for flag in pkg['result']['fx_assign']]
assert len(flags)==386 and sum(flags)==0
receipt=json.loads((P/'cran_1998_publisher_receipts.json').read_text())
assert len(receipt)==16 and all(r['status']==200 for r in receipt)
assert {r['declared_local_path'] for r in receipt}==paths

cases=json.loads((P/'cases.json').read_text())
sources=[json.loads(x) for x in (P/'sources.jsonl').read_text().splitlines()]
source_ids={s['source_id'] for s in sources}
assert all(s in source_ids for c in cases for s in c['source_ids'])
readings=list(csv.DictReader((P/'readings.csv').open()))
assert len(cases)==3 and len(readings)==9
assert sum(c['publisher_exists'] for c in cases)==3
assert sum(c['specific_usage'] for c in cases)==1
assert all(not c['run_link'] and not c['value_checked'] and not c['strict_positive'] for c in cases)
result=dict(verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),audit_not_original_run=True,iris=iris,rstyle_declared1998=16,rstyle_publisher_objects_retrieved=16,author_record_true=0,author_record_functions=386,rds_warning_count=len(warning_records),warning_scope='Description text encoding plus unsupported POSIXct wrapper; ASCII paths, numeric years and Boolean values used. Identity constructors preserve vector/list data and do not execute R.',cases=3,readings=9,all_case_source_ids_resolve=True)
(P/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
