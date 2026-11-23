"""Materialize scope-qualified research decisions, never mutate old records.

The first assessment remains evidence/first-assessment.json. Rows here are the
reconciled recommendation. Conditional split rows are not observed production
repairs. Run after assemble_ledgers.py.
"""
import csv
import json
from pathlib import Path

B = Path(__file__).resolve().parent
S = {x['source_id']: x for x in map(json.loads, (B/'sources.jsonl').read_text().splitlines())}
E = {}
for path in ('streams/gis/events.json','streams/oss/events.json','streams/root/controls.json'):
    E.update({x['event_id']:x for x in json.loads((B/path).read_text())})
ROWS = []


def locator(sid):
    s = S[sid]
    return s['fixed_location'] if isinstance(s['fixed_location'],str) else s['original_url']


def add(rid, old, new, kind, code, relation, versions, sources, observations,
        action, impact, resume, condition='evidence_supported_recommendation', direction='old -> new'):
    eid = rid.split('-')[0]
    e = E.get(eid,{})
    ROWS.append({
        'relation_id':rid, 'event_id':eid,
        'stratum':e.get('stratum','external_standard'),
        'old_id':old, 'new_id':new, 'namespace_and_kind':kind,
        'decision_code':code, 'relation':relation, 'direction':direction,
        'applicable_versions':versions,
        'publisher_lineage_declaration':e.get('declared_lineage',e.get('publisher_declaration',e.get('declaration','see external-records.json'))),
        'receiver_confirmation':e.get('receiver_confirmation','same-publisher fixed source/registration or linked receiving record; source IDs below'),
        'behavior_observation_ids':observations,
        'behavior_acceptance':'see observations.csv and later historical paired execution; lineage alone never implies compatibility',
        'source_ids':sources, 'new_evidence_link':locator(sources[-1]),
        'original_address_action':action,
        'preserve_old_id':True, 'preserve_old_citation':True,
        'past_citation_policy':'retain original URL, edition, section, acquired hash, old conclusion and its question; append dated relation and current locator; do not rewrite historical quoted behavior',
        'evidence_level':'publisher declaration + fixed original source/contract; execution only where an observation receipt explicitly says so',
        'status':condition,
        'difference_from_URL_only':'U cannot establish this typed/versioned relation; the corresponding current HTTP action is in evidence/url-policy-comparison.json',
        'error_impact':impact,
        'reversible':True,
        'reversal_method':'remove/deactivate the new relation row in a later revision; original ID, evidence and first-assessment remain recoverable',
        'resume_condition':resume,
    })

add('G01-R01','gdal-driver:RASDAMAN','gdal-driver:RASDAMAN','GDAL logical raster reader ID','1','preserve_retired_logical_driver',
    'core GDAL3.6.0; removed from core3.7.0; no verified restored binary',
    ['G-ras-doc3.6','G-ras-code3.6','G-ras-move-commit'],['G-O01','G-O02'],
    'append pinned3.6 documentation and receiving source; retain broken live URL as historical citation',
    'source archive presence must not be reported as installed reader/writer support',
    'build exact archived adapter with matching raslib/server; replay rgb checksum61774 and invalid queries; CRS/write requirements remain outside its declared role')
add('G01-R02','source-component:OSGeo/gdal/RASDAMAN@3.6.0','source-component:OSGeo/gdal-extra-drivers/RASDAMAN@ffe0c447','source distribution component, separate from driver ID and server product','4','moved_to_archived_source',
    'receiving commit2023-03-12; core removal3.7.0',
    ['G-NEWS-3.7.0','G-issue4808-comments','G-extra-readme','G-ras-move-commit'],['G-O01','G-O02'],
    'append explicit moved_to_source link; no supported distribution alias',
    'README generic3.5 heading is contradicted by edition-specific3.6 source and3.7 removal',
    'a receiver build/release declaring executable support, then exact API/server test')
add('G02-R01','gdal-driver:ARG','gdal-driver:ARG','GDAL raster driver ID','1','retain_with_retirement_interval',
    '3.7 available;3.8 default-disabled/deprecated with opt-in;3.9 removed',
    ['G-NEWS-3.8.0','G-NEWS-3.9.0','G-arg-code-3.8','G-arg-reg3.9'],['G-O03','G-O04','G-O05'],
    'append last versioned source and retirement notice; retain old URL',
    '404 alone cannot state the last valid environment or choose a conversion target',
    'run fixed ARG bytes under3.7 and3.8 default/opt-in; explicitly reconcile nodata sentinel')
add('G02-R02','gdal-driver:ARG','','GDAL driver replacement target unresolved','5','replacement_unassigned',
    'after3.9 removal; no named equivalent successor found',
    ['G-issue7920','G-arg-doc-3.8'],['G-O03','G-O04'],
    'do not point old ARG record to GTiff as identity alias; a conversion workflow would be a separate relation',
    'blind replacement may lose nodata, data type or georeferencing',
    'one named conversion/reader implementation with exact input and old-consumer roundtrip evidence',condition='hold')
add('G03-R01','gdal-driver:Parquet','gdal-driver:Parquet','GDAL vector driver registry ID','1','same_driver_location_repair',
    'GDAL3.7.0 ->3.8.0; format edition tracked separately',
    ['G-parquet-doc-3.7','G-parquet-doc-3.8'],['G-O06','G-O07'],
    'update current canonical driver URL; retain versioned beta/final citations separately',
    'driver URL repair is appropriate but cannot preserve an output-format version assertion alone',
    'same hashed fixture through both binaries plus old-consumer validation')
add('G03-R02','geoparquet-format:1.0.0-beta.1','geoparquet-format:1.0.0','GeoParquet format edition','4','succeeded_by_format_edition',
    'GDAL3.7 beta writer ->3.8 final1.0 writer',
    ['G-parquet-writer3.7','G-parquet-writer3.8','G-gp-spec1.0'],['G-O06','G-O07'],
    'append final1.0 source; keep beta output claim tied to3.7; mark3.8 manual stale',
    'same source path/test name has different fixture bytes; apparent paired evidence is insufficient',
    'freeze one old fixture SHA256; read/write under3.7 and3.8 and compare mandatory metadata')
add('G04-R01','gdal-option:Parquet.GEOARROW@3.8/interleaved','gdal-option:Parquet.GEOARROW_INTERLEAVED@3.9','versioned layer creation option for legacy encoding','2','scoped_rename_alias',
    'pre3.9 GEOARROW ->3.9 GEOARROW_INTERLEAVED; later releases not blanket-certified',
    ['G-parquet-doc-3.8','G-parquet-doc-3.9'],['G-O09','G-O10'],
    'append renamed legacy option with start version; retain old name and edition',
    'treating each new spelling as a new function duplicates legacy work; not an observed U false-split',
    'same point/null/EMPTY input in3.8 and3.9 legacy encoding, compared as Arrow type and geometry semantics')
add('G04-R02','gdal-option:Parquet.GEOARROW@3.8/interleaved','gdal-option:Parquet.GEOARROW@3.9/struct','two encoding implementations under reused display value','4','distinct_encoding_successor',
    'same option string changes meaning at3.9; strict1.0 reader is separate consumer',
    ['G-parquet-doc-3.9','G-parquet-test-3.9','G-gp-spec1.1'],['G-O08','G-O09','G-O10','G-O11'],
    'link encoding alternatives; forbid global same-name alias; qualify consumer edition',
    'fixed-size-list vs struct and null vs EMPTY may invalidate the consumer contract',
    'run3.8/3.9 same immutable input and old consumer; inspect schema and null bitmap')
add('G04-R03','record:unversioned-Parquet-GEOARROW','gdal-option:Parquet.GEOARROW@3.8/interleaved ; gdal-option:Parquet.GEOARROW@3.9/struct','hypothetical existing mixed recommendation record','3','conditional_record_split',
    'only if an actual record conflating the two versioned meanings is supplied',
    ['G-parquet-doc-3.8','G-parquet-doc-3.9','G-parquet-test-3.9'],['G-O09','G-O10'],
    'split typed target references while preserving the original record revision; no production record was supplied',
    'conditional repair proposal, excluded from observed completed-split/false-merge counts',
    'obtain the old recommendation record with its called option and consuming schema',condition='conditional_not_observed_production_repair')
add('O01-R01','python:scipy.stats.median_absolute_deviation','python:scipy.stats.median_abs_deviation','SciPy qualified public callable','4','deprecated_in_favour_of_with_scale_adapter',
    '1.4.1 old implementation ->1.5.0 new callable/old wrapper; no unrestricted later-edition promise',
    ['OS-REL-05','OS-PR-11431','OS-DOC-O01-new'],['O01-P1-NORMAL','O01-P2-DEFAULT','O01-BOUNDARY-EMPTY'],
    'append replacement URL and reciprocal-scale adapter; keep old expected value and shape contract',
    'blind rename changes1.4826 to1; adapter does not restore empty-array shape semantics',
    'validate the exact required shapes/NaN/warnings and choose whether legacy empty behavior must be emulated')
for suffix, old, new in [('01','integrate.simps','integrate.simpson'),('02','integrate.trapz','integrate.trapezoid'),('03','integrate.cumtrapz','integrate.cumulative_trapezoid'),('04','stats.trapz','stats.trapezoid')]:
    add('O02-R'+suffix,'python:scipy.'+old,'python:scipy.'+new,'SciPy fully qualified callable; one recruitment event with four separate targets','2','scoped_alias',
        'introduced1.6.0; integrate old names removed1.14.0; stats alias end not established here',
        ['OS-ISSUE-12924','OS-PR-12927','OS-PR-12934'],['O02-P1-INTEGRATE','O02-P2-INTEGRATE','O02-NAMESPACE-COUNTER'],
        'append new qualified name and validity interval; retain old citation; do not merge stats with integrate',
        'new-spelling-only identity creates duplicate tasks; namespace-erasing identity allows a distribution constructor where a number is required',
        'same pinned NumPy dependency, boundary matrix and exact callable; later simpson changes need separate edition evidence')
add('O03-R01','python:scipy.spatial.KDTree.query#k=None','python:scipy.spatial.KDTree.query_ball_point','method mode and related spatial-query method','4','feature_moved_with_adapter',
    '1.5.4 old mode ->1.6.0 deprecation wrapper; planned removal1.8.0, actual documented removal1.9.0',
    ['OS-REL-06','OS-PR-12382','OS-DOC-O03-new'],['O03-P1-NORMAL','O03-P2-RETURNS','O03-BOUNDARY-RADIUS'],
    'pin old mode documentation; add new method with distance/ordering/boundary conversion obligations',
    'new method lacks distances and nearest-first contract; same live query URL hides removed mode',
    'apply observed exact-radius and scalar-type differences to the actual caller contract; test a strict-boundary/distance-sort adapter')
add('O04-R01','python:scipy.ndimage.sum','python:scipy.ndimage.sum_labels','SciPy label-sum callable','2','scoped_alias',
    '1.5.4 old implementation ->1.6.0 alias; current1.17.0 supplemental check separate',
    ['OS-REL-06','OS-PR-12242','OS-DOC-O04-new'],['O04-P1-PROVIDER','O04-P2-PROVIDER','O04-HTTP-COUNTER'],
    'append preferred function URL; retain old name and versioned URL despite current doc404',
    '404 does not imply function deletion; treating preferred name as a new task duplicates the same label reduction',
    'extend current/provider fixture verification only to additional dtypes/errors actually required')
add('C01-R01','project:scikit-learn','project:scikit-learn','software project identity distinct from import namespace','1','same_project',
    '0.8 ->0.9 explicit package-name change',
    ['R002','R004'],['C01-P1','C01-P2'],
    'append surviving versioned release mirror; retain original locator and old spelling',
    'project continuity does not assert unchanged estimator defaults',
    '0.8/0.9 exact load_iris and selected estimator fixtures')
add('C01-R02','python-namespace:scikits.learn','python-namespace:sklearn','Python package namespace','2','version_bounded_namespace_alias',
    '0.9 alias retained; announced and later confirmed removal0.11',
    ['R002','R003','R005','R026'],['C01-P1','C01-P2'],
    'append scoped namespace alias; retain0.8 old import citation',
    'permanent/global alias would ignore later removal and fit/gamma changes',
    'execute historic imports and required fit/default behavior with versioned dependency pins')
add('C02-R01','distribution:PythonWare/Imaging@1.1.7','pypi:pillow','separate source distributions sharing PIL import namespace','4','forked_into',
    'PIL1.1.7 README2009-11-15; Pillow fork2010-07-31; inspectedPillow2.0 source; current13.0 probe separate',
    ['R031','R035','R036','R008'],['C02-P1','C02-P2'],
    'retain original PIL evidence; append fork and old-author response; mark current pythonware content as later authorship',
    'same PIL import string, version constant or domain cannot merge distributions',
    'independent original PIL source archive and same-image decoding/error test in a compatible historical runtime')
add('C02-R02','pypi-project-name:PIL','pypi-project-name:PIL','registry-name custody, separate from distribution version','1','registry_custody_changed',
    'PyPI administrator reports transfer completion2020-01-03; no release identity merge',
    ['R013','R014'],['C02-P1'],
    'append dated ownership metadata; keep old release provenance and fork relation separate',
    'ownership transfer of a name does not turn every PIL artifact into Pillow',
    'registry release artifact and owner history for the exact installed distribution')
add('C02-R03','record:unqualified-PIL','distribution:PythonWare/Imaging ; pypi:pillow ; pypi-project-name:PIL','hypothetical mixed distribution/import/registry record','3','conditional_record_split',
    'only for an actual mixed recommendation record',
    ['R014','R030','R031','R035'],['C02-P1','C02-P2'],
    'split references by namespace while preserving old record; no actual production record supplied',
    'excluded from observed error and completed split counts',
    'obtain installed artifact metadata and original recommendation record',condition='conditional_not_observed_production_repair')
add('C03-R01','cpython-api:imp.find_module','cpython-api:imp.find_module','retired function and its versioned documentation section','1','retain_retired_function',
    '3.11 last documented available edition; removed3.12',
    ['R016','R017','R019','R032'],['C03-P1'],
    'point historical citation to3.11 anchor; retain live URL as observed removed stub',
    '200 without old section silently loses the old recommendation evidence',
    'exact old caller and required return/error fields; no need to assume current URL is historical content')
add('C03-R02','cpython-api:imp.find_module','cpython-api:importlib.util.find_spec','distinct Python import APIs','4','replacement_guidance_with_contract_conversion',
    '3.11 ->3.12 migration guidance; current3.12.14 observed',
    ['R016','R019','R033'],['C03-P2'],
    'append method-level migration guidance; never alias whole imp to importlib',
    'tuple/ImportError vs ModuleSpec/None breaks a drop-in consumer',
    'test explicit result conversion and absent-module exception policy; separate reload behavior if needed')
add('EXT01-R01','iana-language:mo','iana-language:ro','IANA BCP47 language subtag registry','2','deprecated_preferred_value',
    'Deprecated2008-11-22; original standard change2008-11-03; request2008-11-25',
    ['STD-S01','STD-S02','STD-S07'],[],
    'append scoped preferred-value relation; preserve raw historical tag and source edition',
    'the earlier mo.txt description update is not the November deprecation source; do not substitute ISO639-3 IDs',
    'original ISO change row if upstream approval date is itself part of the claim')
add('EXT02-R01','iana-language:bhk','iana-language:{fbl,lbl,rbl,ubl}','IANA BCP47 language subtag registry','4','split_into_multiple_successors',
    'source split2010-01-20; IANA Deprecated/receiver Added2010-03-11',
    ['STD-S01','STD-S02','STD-S06'],[],
    'preserve bhk; append all four directional relations; no single preferred alias',
    'choosing the first target discards other possible meanings of legacy content',
    'one distinguishing language/region/content observation for the specific old record')
add('EXT02-R02','iana-language:bhk','','single-target mapping for an unspecified legacy text','5','single_successor_unresolved',
    'after2010 split until content is identified',
    ['STD-S01','STD-S06'],[],
    'hold automatic single-target replacement',
    'a one-to-many split is not a set of freely interchangeable aliases',
    'content evidence identifying one of the four successor languages',condition='hold')

# Append completed evidence without changing the locked first assessment.
hp = B/'streams/oss/historical/paired-observations.jsonl'
if hp.exists():
    pairs = [json.loads(line) for line in hp.read_text().splitlines()]
    for r in ROWS:
        selected = [p for p in pairs if p['event_id'] == r['event_id']]
        if r['event_id'] == 'O02':
            if r['relation_id'] == 'O02-R02':
                selected = [p for p in selected if p['case'] != 'distribution_alias']
            elif r['relation_id'] == 'O02-R04':
                selected = [p for p in selected if p['case'] == 'distribution_alias']
            else:
                selected = []
                r['behavior_acceptance'] = 'alias declaration/source structure read; this individual simps/cumtrapz mapping was not executed by the historical probe'
        if selected:
            r['behavior_observation_ids'] += ['H-'+p['pair_id'] for p in selected]
            r['evidence_level'] += '; historical native same-host Python3.8.20/NumPy1.19.5 comparison in the cited exact inputs'
            r['behavior_acceptance'] = {
                'O01':'P1 normal scalar value/type preserved with warning; empty2D shape differs. P2 default changes value; reciprocal scale repairs normal fixture only.',
                'O02':'tested trapz/trapezoid or stats distribution inputs preserve values/representation/errors; no all-input or later-version equivalence claim.',
                'O03':'P1 exact-radius membership and scalar index type differ. P2 lacks distance outputs. Adapter not implemented or certified.',
                'O04':'tested provider/float32/empty values and complex/shape error contracts match; scoped alias supported.',
            }[r['event_id']]
if 'PA001' in S:
    for r in ROWS:
        if r['event_id'] == 'C02':
            r['source_ids'] += ['PA001','PA002','PA004','PA006']
            r['behavior_observation_ids'] += ['PA-O01','PA-O02','PA-O03','PA-O04']
            r['evidence_level'] += '; original PIL1.1.7 archive obtained from official Debian preservation and checked against descriptor; original runtime still unexecuted'
        if r['relation_id'] == 'C02-R01':
            r['new_evidence_link'] = locator('PA001')
            r['resume_condition'] = 'source gap closed; next run identical PNG load (not just lazy open), invalid/truncated bytes and stage-sensitive exceptions under original PIL1.1.7 and pinned Pillow; verify signer only if stronger provenance is required'

with (B/'relations.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(ROWS[0]))
    w.writeheader()
    for r in ROWS:
        w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()})
print(json.dumps({'relations':len(ROWS),'conditional_splits':sum(x['decision_code']=='3' for x in ROWS),'old_records_overwritten':0}))
