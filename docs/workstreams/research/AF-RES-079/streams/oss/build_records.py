"""Assemble the OSS research ledger from explicitly reviewed evidence.

This does not infer runtime equivalence from HTTP success or execute old releases.
"""
import csv
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
SHAS = {"1.4.1":"adc4f4f7bab120ccfab9383aba272954a0a12fb0",
        "1.5.0":"4c0fd79391e3b2ec2738bf85bb5dab366dcd12e4",
        "1.5.4":"19acfed431060aafaa963f7e530c95e70cd4b85c",
        "1.6.0":"ab1c0907fe9255582397db04592d6066745018d3"}


def dump(name, value):
    (ROOT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def jsonlines(name, rows):
    (ROOT/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))


def blob(version, path, lines=None):
    u=f'https://github.com/scipy/scipy/blob/{SHAS[version]}/{path}'
    return u+(('#L'+lines) if lines else '')


http=[json.loads(l) for l in (ROOT/'http-observations.jsonl').read_text().splitlines()]
sources=[json.loads(l) for l in (ROOT/'pr-sources.jsonl').read_text().splitlines()]
release_rows=json.loads((ROOT/'release-screen.json').read_text())
for r in release_rows:
    v=r['version'];n=int(v.split('.')[1]);sid=f'OS-REL-{n:02}'
    sources.append({
        'source_id':sid,'work_id':'scipy-release-notes-series','original_url':r.get('url'),
        'actual_opened_url':r.get('url'),'arrived_url':r.get('arrived_url'),'http_status':r.get('status'),
        'checked_utc':r.get('checked_at_utc'),'publisher':'SciPy community','edition':'v'+v,
        'section':'release narrative; named migration loci in issue/PR list',
        'sha256':r.get('sha256'),'access_status':'directly_read' if n<=8 or n==14 else 'machine_screened_only',
        'finding':({'1.5.0':'L250 및 L296: MAD 새 함수와 구 함수 deprecation을 같은 사건으로 명시한다.',
                    '1.6.0':'L52–57/L245–246 rename 묶음, L270–271 KDTree mode 이관, L273–274 wminkowski 재공지, L490/L637 ndimage 이름 변경 순서.',
                    '1.7.0':'pinv2→pinv는 1.6 모집 충족 뒤의 다음 후보다.',
                    '1.8.0':'private/public namespace 정리와 NumericalInverseHermite 이관은 이번 첫4 모집 뒤의 사건이다.',
                    '1.14.0':'고정 RST L228–229 및 현재 렌더의 Expired deprecations: integrate.simps/trapz/cumtrapz 제거를 확인했다. 원래 1.6 alias의 적용 종료판 근거이며 신규 모집이 아니다.'}).get(v,'모집 상한 안 추가 판의 기계적 키워드 선별만 수행. 최초4 채택 판단이나 독립 저작 달성에는 산입하지 않는다.'),
        'limitations':'동일 release-note series의 판은 독립 원저작 수를 늘리지 않는다. 배포 시각과 코드 커밋은 별도 기록.',
        'counterevidence':'API 인자만 바뀌거나 이미 기간 전에 이관된 공지는 새 이전 사건이 아니다.',
        'counted_independent_work':v=='1.5.0','count_reason':'SciPy release-note series 전체를 보수적으로 1계보로 산입; 다른 판은0.',
        'claimed_events':['O01'] if v=='1.5.0' else ['O02','O03','O04'] if v=='1.6.0' else []})

for r in http:
    eid,role=r['event_id'],r['role'];sid=f'OS-DOC-{eid}-{role}'
    sections={
        ('O01','old'):'signature / scale / nan_policy / Returns / Examples',
        ('O01','new'):'signature / scale / nan_policy / Returns / Examples',
        ('O02','old'):'signature / input axis / Returns / Examples',
        ('O02','new'):'signature / input axis / Returns / Examples',
        ('O03','old'):'Returns: k=None distance lists and nearest-first order',
        ('O03','new'):'return_sorted / return_length / Returns: index lists',
        ('O04','old'):'labels / index / Returns / Examples',
        ('O04','new'):'labels / index / Returns / Examples'}
    sources.append({'source_id':sid,'work_id':'scipy-api-reference-manual','original_url':r['requested_url'],
                    'actual_opened_url':r['requested_url'],'arrived_url':r.get('arrived_url'),'http_status':r.get('http_status'),
                    'redirect_chain':r.get('chain'),'checked_utc':r['checked_utc'],'publisher':'SciPy community',
                    'edition':r['version'],'section':sections.get((eid,role),'current unversioned address / availability'),
                    'sha256':r.get('sha256'),'access_status':'directly_read' if r.get('http_status')==200 else 'access_failed',
                    'finding':('구판·신판의 각 대상 문서가 200으로 독립 도착했다. 대상 문서의 함수·반환 계약은 관측 원장에 연결한다.' if role!='live_old' else '현재 주소 생존을 관측했다. 이것으로 과거 redirect나 설치 가능한 API 존재를 추정하지 않는다.'),
                    'limitations':'버전 문서와 현재 라이브 문서가 다르다. HTTP 200은 동작 검사가 아니다. 문서 계보는 보수적으로 추가 산입하지 않음.',
                    'counterevidence':'ndimage.sum의 현재 문서는404이나 설치된1.17.0 함수는 호출된다. query의 현재 문서는200이나 k=None은 거절된다.',
                    'counted_independent_work':False,'count_reason':'API 설명서는 원 PR/원 구현의 지원 자료로만 사용; 수량 부풀림 방지.',
                    'claimed_events':[eid]})

code_rows=json.loads((ROOT/'code-acquisition.json').read_text())
for i,r in enumerate(code_rows,1):
    good=r.get('http_status')==200
    sources.append({'source_id':f'OS-CODE-{i:02}','work_id':'scipy-source-tree',
        'original_url':r['url'],'actual_opened_url':r['url'],'arrived_url':r.get('arrived_url'),
        'http_status':r.get('http_status'),'checked_utc':r.get('checked_utc'),'publisher':'SciPy contributors',
        'edition':r['version']+'@'+r['commit'],'section':r['path']+' selected definitions named in observations.jsonl',
        'sha256':r.get('sha256'),'access_status':'directly_read' if good else 'access_failed',
        'finding':'고정 커밋에서 선언과 구현을 분리해 판독했다.' if good else r.get('error'),
        'limitations':'파일 취득/정적 판독이다. 해당 과거 wheel 실행 결과가 아니다.',
        'counterevidence':'MAD 기본 scale/빈 배열 형상, KDTree 거리 반환과 경계 조건을 별도 확인.',
        'counted_independent_work':False,'count_reason':'같은 저장소의 코드·판을 독립 저작으로 추가 계산하지 않음.',
        'claimed_events':['O01'] if 'stats/stats' in r['path'] else ['O02'] if 'integrate' in r['path'] else ['O03'] if 'kdtree' in r['path'] else ['O04']})

followup=ROOT/'followup-sources.jsonl'
if followup.exists():
    sources.extend(json.loads(line) for line in followup.read_text().splitlines())
for s in sources:
    s['source_url']=s['original_url']
    s['fixed_location']=s.get('edition','')+' / '+s.get('section','')
    s['reader']='oss_evidence tool agent; researcher and first assessor are same'
    if s['source_id'].startswith(('OS-PR-', 'OS-ISSUE-')):
        s['http_status_observation']='GitHub connector returned the source body/diff but did not expose raw response status or redirect chain; these remain unobserved.'
    if s['source_id']=='OS-DOC-O03-live_old':
        s['section']='Returns / Changed in version 1.9.0; manual banner v1.18.0 observed on 2026-11-23'
        s['finding']='현재 query 문서는200으로 살아 있지만 Returns 절이 k=None 제거판을1.9.0으로 명시한다. 원1.6.0 공지의 예정1.8.0과 실제 선언을 구분한다.'
        s['fixed_location']=s['original_url']+' / Returns, Changed in version1.9.0 / body sha256='+str(s.get('sha256'))
        s['followup_recorded_utc']=NOW
        s['followup_read_time_precision']='2026-11-23 UTC; exact web call timestamp not separately recorded; original HTTP observation UTC above remains exact'
jsonlines('sources.jsonl',sources)

rows=[
 ('R01','1.5.0',77,'linalg.eigh turbo/eigvals','subset_by_*','EXCLUDE_ARGUMENT_ONLY','','public callable identity unchanged'),
 ('R02','1.5.0',250,'stats.median_absolute_deviation','stats.median_abs_deviation','SELECT','O01','first eligible migration; L296 is same event'),
 ('R03','1.5.0',291,'special.bdtr family n','integral n','EXCLUDE_ARGUMENT_ONLY','','input-domain deprecation only'),
 ('R04','1.5.0',296,'stats.median_absolute_deviation','stats.median_abs_deviation','DUPLICATE','O01','same event as R02'),
 ('R05','1.5.0',300,'stats.iqr(scale=raw)','scale=1','EXCLUDE_ARGUMENT_ONLY','','no public function/name move'),
 ('R06','1.5.0',494,'approx_grad','_numdiff.approx_derivative','EXCLUDE_PRIVATE_TARGET','','issue title targets internal implementation; not public migration'),
 ('R07','1.5.0',735,'_lib._version','_lib._pep440','EXCLUDE_PRIVATE_TARGET','','internal modules'),
 ('R08','1.5.0',860,'xrange','range','EXCLUDE_INTERNAL_CLEANUP','','Python2 compatibility cleanup rather than SciPy public API migration'),
 ('R09','1.5.0',942,'tostring uses','tobytes uses','EXCLUDE_INTERNAL_CLEANUP','','internal use replacement, not a public SciPy callable being renamed'),
 ('R10','1.6.0',52,'integrate.simps/trapz/cumtrapz','integrate.simpson/trapezoid/cumulative_trapezoid','SELECT','O02','one naming decision #12924; PR12927 and12934 grouped'),
 ('R11','1.6.0',245,'stats.trapz','stats.trapezoid','DUPLICATE','O02','same PR12934 naming decision; distinct function IDs retained as subrows, not extra natural event'),
 ('R12','1.6.0',270,'KDTree.query(k=None)','KDTree.query_ball_point','SELECT','O03','public all-neighbors feature migrated to another public method; not merely a default-value change'),
 ('R13','1.6.0',273,'distance.wminkowski','distance.minkowski(w=...)','EXCLUDE_PRIOR_EVENT','','PR12374 says migration/soft-deprecation originated in SciPy1.0, outside window; 1.6 is warning enforcement'),
 ('R14','1.6.0',281,'scipy.fft callable alias','numpy.fft.fft / scipy.fft module','EXCLUDE_PRIOR_EVENT','','release explicitly says deprecated in1.4.0; no new migration counted'),
 ('R15','1.6.0',296,'signal.slepian','unspecified','EXCLUDE_NO_TARGET','','simple removal and prior1.1 deprecation'),
 ('R16','1.6.0',307,'stats.frechet_l/frechet_r','unspecified','EXCLUDE_PRIOR_EVENT','','prior1.0 deprecation; current notice supplies no target'),
 ('R17','1.6.0',490,'ndimage.sum','ndimage.sum_labels','SELECT','O04','issue10593 named in release; exact new public name at L637 PR12242'),
 ('R18','1.6.0',568,'integration naming proposal12924','three new names','DUPLICATE','O02','same R10 decision'),
 ('R19','1.6.0',637,'ndimage.sum','ndimage.sum_labels','DUPLICATE','O04','same R17 event; supplies target mapping'),
 ('R20','1.6.0',645,'LocalSearchWrapper bounds','internal bounds name','EXCLUDE_PRIVATE_TARGET','','optimizer implementation helper'),
 ('R21','1.6.0',686,'KDTree implementation','cKDTree wrapper','DUPLICATE','O03','same PR12382 underlying change'),
 ('R22','1.6.0',811,'cKDTree.query n_jobs','workers','EXCLUDE_ARGUMENT_ONLY','','public callable identity unchanged'),
 ('R23','1.6.0',844,'simps','simpson','DUPLICATE','O02','same naming decision'),
 ('R24','1.6.0',845,'trapz/cumtrapz','trapezoid/cumulative_trapezoid','DUPLICATE','O02','same naming decision'),
 ('R25','1.7.0',310,'linalg.pinv2','linalg.pinv','AFTER_QUOTA','','not substituted for any failed pair')]
with (ROOT/'recruitment.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['candidate_id','release','source_line','old_target','new_target','screen_decision','event_id','reason'])
    w.writerows(rows)

events=[
 {'event_id':'O01','recruitment_original_rank':'R02; release1.5.0 L250 (repeat L296)','eligible_event_order':1,
  'old_id':'python:scipy.stats.median_absolute_deviation','new_id':'python:scipy.stats.median_abs_deviation',
  'old_version':'1.4.1','new_version':'1.5.0','namespace':'Python public qualified function name; distribution PyPI:scipy',
  'target_kind':'function','original_behavior':'scaled median absolute deviation: old numeric scale multiplies raw MAD; default1.4826',
  'publisher_declaration':'SciPy1.5.0 deprecates old function in favour of new API; old wrapper explicitly reciprocates scale.',
  'receiver_confirmation':'same SciPy publisher; new function and preserved old wrapper coexist in fixed1.5.0 source.',
  'behavior_evidence':'old source return scale*mad versus new source return mad/scale; provider examples 2.9652 versus2.0 for axis=None; old wrapper adapts scale.',
  'decision_codes':['4'],'relationship':'deprecated_function -> replacement_function, with reciprocal-scale adapter; not unconditional same-behavior alias',
  'direction':'old -> new','applicable_versions':'new API since1.5.0; adapter claim checked at1.5.0; later removal requires separate record',
  'repair':'preserve1.4.1 old URL and citation; append1.5.0 replacement URL and required parameter adapter; never overwrite historical expected values',
  'past_evidence_retained':True,'reversible':True,
  'counterexample':'same name-change declaration with defaults changes y=[1,3,2] expectation1.4826 to1; empty2D shape also changes across old/new release.',
  'resume_condition':'run probe.py in Python3.8 + NumPy1.19.5 + SciPy1.4.1 and1.5.0; inspect normal/empty2D/nan/axis/dtype rows before accepting adapter broadly',
  'sources':['OS-REL-05','OS-PR-11431','OS-ISSUE-11090','OS-DOC-O01-old','OS-DOC-O01-new'],
  'runtime_pair_observed':False},
 {'event_id':'O02','recruitment_original_rank':'R10; release1.6.0 L52–57 plus L245–246 folded as one decision','eligible_event_order':2,
  'old_id':'python:scipy.integrate.{simps,trapz,cumtrapz};python:scipy.stats.trapz',
  'new_id':'python:scipy.integrate.{simpson,trapezoid,cumulative_trapezoid};python:scipy.stats.trapezoid',
  'old_version':'1.5.4','new_version':'1.6.0','namespace':'Python module-qualified API names; never erase integrate/stats namespace',
  'target_kind':'function family naming migration, one recruitment event with four mappings',
  'original_behavior':'three integration operations and one probability distribution; independent function identities under one naming decision',
  'publisher_declaration':'old names retained for compatibility in1.6.0; issue12924 and PR12927/12934 form one rename decision.',
  'receiver_confirmation':'same publisher source exposes old/new names together and wrappers pass arguments unchanged; stats alias has its own class lineage.',
  'behavior_evidence':'integrate.trapz delegates to trapezoid and both versions bind NumPy trapz; supplier stats alias test compares its pdf to uniform distribution.',
  'decision_codes':['2'],'relationship':'scoped old-name -> new-name alias per qualified function; integration and distribution are separate targets',
  'direction':'old name -> preferred new name; callable compatibility at1.6.0',
  'applicable_versions':'alias checked1.6.0; integration old names removed in1.14.0 per later release; no undated forever-alias claim',
  'repair':'add per-module aliases, retain old1.5.4 citation and new1.6.0 locator; record1.14.0 end for integration old names',
  'past_evidence_retained':True,'reversible':True,
  'counterexample':'integrate.trapezoid(y,x) returns a number while stats.trapezoid(c,d) creates a frozen distribution; same short name must not merge target IDs.',
  'resume_condition':'run both releases with the same NumPy1.19.5; test reverse/empty/axis/dtype and distribution alias separately',
  'target_mappings':[
    {'old':'scipy.integrate.simps','new':'scipy.integrate.simpson'},
    {'old':'scipy.integrate.trapz','new':'scipy.integrate.trapezoid'},
    {'old':'scipy.integrate.cumtrapz','new':'scipy.integrate.cumulative_trapezoid'},
    {'old':'scipy.stats.trapz','new':'scipy.stats.trapezoid'}],
  'sources':['OS-REL-06','OS-ISSUE-12924','OS-PR-12927','OS-PR-12934','OS-DOC-O02-old','OS-DOC-O02-new'],
  'runtime_pair_observed':False},
 {'event_id':'O03','recruitment_original_rank':'R12; release1.6.0 L270–271','eligible_event_order':3,
  'old_id':'python:scipy.spatial.KDTree.query#k=None','new_id':'python:scipy.spatial.KDTree.query_ball_point',
  'old_version':'1.5.4','new_version':'1.6.0','namespace':'method plus mode; KDTree class/product ID is a different scope',
  'target_kind':'function mode -> related method','original_behavior':'all neighbours under bound, distances and indices sorted by distance',
  'publisher_declaration':'SciPy1.6.0 deprecates query(k=None), directs callers to query_ball_point; same publisher.',
  'receiver_confirmation':'1.6.0 query_ball_point exists; original query compatibility wrapper reconstructs distances and sorts hits.',
  'behavior_evidence':'new method returns index lists only; original wrapper performs extra distance computation/sorting. 1.5.4 query uses strict < bound; new wrapper delegates to radius search.',
  'decision_codes':['4'],'relationship':'old mode -> suggested replacement method; output adapter needed; no behavioral identity asserted',
  'direction':'query(k=None) -> query_ball_point plus explicit distance/sort adapter',
  'applicable_versions':'deprecation starts1.6.0; original1.6.0 note planned removal1.8.0; current docs report actual removal1.9.0 (must distinguish plan from actual)',
  'repair':'retain old1.5.4 query citation including mode; link new method and adapter requirements; do not infer all-neighbour mode from a surviving query page',
  'past_evidence_retained':True,'reversible':True,
  'counterexample':'query_ball_point does not supply distances or nearest-distance order. Exact radius equality can distinguish the prior strict bound from a ball search.',
  'resume_condition':'paired native run of points[[0],[1],[2]], query[0], radii1.1/1.0, complex query and shape mismatch; bind output-order/distance contract',
  'sources':['OS-REL-06','OS-PR-12382','OS-DOC-O03-old','OS-DOC-O03-new'],
  'runtime_pair_observed':False},
 {'event_id':'O04','recruitment_original_rank':'R17; release1.6.0 issue list L490, exact mapping PR list L637','eligible_event_order':4,
  'old_id':'python:scipy.ndimage.sum','new_id':'python:scipy.ndimage.sum_labels',
  'old_version':'1.5.4','new_version':'1.6.0','namespace':'Python scipy.ndimage; distinguish builtins.sum',
  'target_kind':'function alias','original_behavior':'sum values by labels/index, output order follows index, absent index returns0',
  'publisher_declaration':'PR12242 renames function to avoid collision with builtins.sum; old name stays alias.',
  'receiver_confirmation':'1.6.0 sum wrapper delegates unchanged arguments to sum_labels; _stats implementation matches1.5.4 byte-for-byte at function-text scope.',
  'behavior_evidence':'supplier test_sum_labels uses input[[1,2],[3,4]],labels[[1,2],[2,4]],index[4,8,2] and expected[4,0,5]; old/new outputs asserted equal.',
  'decision_codes':['2'],'relationship':'old public name -> preferred public name for same labelled-sum feature',
  'direction':'sum -> sum_labels; scoped alias','applicable_versions':'alias introduced1.6.0; additionally observed working in installed1.17.0, future unknown',
  'repair':'add sum_labels locator and alias; retain old source/version; current404 old documentation does not delete historical ID or prove runtime removal',
  'past_evidence_retained':True,'reversible':True,
  'counterexample':'treating the two aliases as different implementations duplicates work. Merging builtins.sum with ndimage.sum loses label/index semantics.',
  'resume_condition':'paired native1.5.4/1.6.0 probe for dtype/shape/complex errors; verify current docs at actual installed release when URL404 needs repair',
  'sources':['OS-REL-06','OS-PR-12242','OS-DOC-O04-old','OS-DOC-O04-new'],
  'runtime_pair_observed':False}
]
for e in events:
    e.update({'stratum':'natural','domain':'OSS','frame':'SCIPY_RELEASES_1.5_1.14',
              'old_commit':SHAS[e['old_version']],'new_commit':SHAS[e['new_version']],
              'publisher':'SciPy community','observed_http':[r for r in http if r['event_id']==e['event_id']],
              'first_assessor':'oss_evidence tool agent','independent_review':'not in this stream; source-only packet supplied to root',
              'evidence_level':'official release + fixed implementation + provider tests read; historical native execution unobserved',
              'pair_available':True})
dump('events.json',events)

obs=[]
def add(eid,oid,q,inp,expected,old_result,new_result,kind,source_ids,loc,disagreement,verdict,limit):
    obs.append({'observation_id':oid,'event_id':eid,'question':q,'input_environment':inp,
                'expected':expected,'old_observation_or_prediction':old_result,
                'new_observation_or_prediction':new_result,'observation_kind':kind,
                'evidence_source_ids':source_ids,'evidence_locations':loc,
                'norm_behavior_disagreement':disagreement,'verdict':verdict,
                'limit':limit,'checked_utc':NOW,'observer':'oss_evidence tool agent'})

add('O01','O01-P1-NORMAL','P1',{'input':[1.,3.,2.],'old_call':'stats.median_absolute_deviation(x)','releases':['1.4.1','1.5.0']},
    'old public call and default value1.4826 retained','source predicts1.4826','source wrapper predicts1.4826 plus deprecation warning',
    'fixed_implementation_static_prediction_not_native_pair',['OS-PR-11431','OS-DOC-O01-old'],
    [blob('1.4.1','scipy/stats/stats.py','2767-L2882'),blob('1.5.0','scipy/stats/stats.py','3031-L3149')],
    'normal numeric contract retained; warning policy changes','CONDITIONALLY_SUPPORTED_NORMAL_ONLY','native past release pair unexecuted; multidimensional empty input differs')
add('O01','O01-P2-DEFAULT','P2',{'input':[1.,3.,2.],'new_call':'stats.median_abs_deviation(x)','releases':['1.4.1','1.5.0']},
    'replace name while preserving old expected1.4826','source predicts1.4826','new default source predicts1.0; scale=1/1.4826 adapter is required',
    'fixed_implementation_static_prediction_not_native_pair',['OS-PR-11431','OS-DOC-O01-new'],
    [blob('1.4.1','scipy/stats/stats.py','2882'),blob('1.5.0','scipy/stats/stats.py','2878-L3028')],
    'official replacement guidance does not assert unchanged default semantics','REJECT_UNADAPTED_SUBSTITUTION','a reciprocal-scale adapter can repair normal values; it does not prove all boundary behavior')
add('O01','O01-BOUNDARY-EMPTY','P1/P2',{'input_shape':[3,0],'axis':1},
    'preserve prior output shape','1.4.1 implementation returns scalar NaN for any empty input','1.5.0 returns NaN array shape[3]',
    'fixed_implementation_static_prediction_not_native_pair',['OS-PR-11431'],
    [blob('1.4.1','scipy/stats/stats.py','2860-L2862'),blob('1.5.0','scipy/stats/stats.py','3001-L3009')],
    'legacy wrapper also delegates to changed shape handling','REJECT_FULL_BOUNDARY_EQUIVALENCE','predicted from explicit branches; run old/new wheel for runtime confirmation')
add('O02','O02-P1-INTEGRATE','P1',{'y':[1.,3.,2.],'x':[0.,1.,2.],'call':'integrate.trapz(y,x)','numpy_pin_for_future_run':'1.19.5'},
    '4.5 and old name retained','1.5.4 copies NumPy trapz','1.6.0 old wrapper passes to copied NumPy trapz named trapezoid',
    'fixed_implementation_and_provider_examples_not_native_pair',['OS-PR-12934','OS-DOC-O02-old','OS-DOC-O02-new'],
    [blob('1.5.4','scipy/integrate/_quadrature.py','7-L29'),blob('1.6.0','scipy/integrate/_quadrature.py','7-L43')],
    'no mismatch for alias forwarding with same NumPy dependency','SUPPORTED_ALIAS_STRUCTURE','same NumPy must be fixed; not a measurement of two installed historical releases')
add('O02','O02-P2-INTEGRATE','P2',{'cases':'normal/reverse/empty/singleton/2D/float32/complex/axis9/mismatched x','replacement':'integrate.trapezoid'},
    'same numeric array/exception contract as old integration function','provider examples 4.0/8.0 and axis output arrays','same provider examples and forwarded parameters in1.6.0; full boundary matrix not executed',
    'provider_examples_and_static_wrapper',['OS-PR-12934','OS-DOC-O02-old','OS-DOC-O02-new'],
    [blob('1.6.0','scipy/integrate/_quadrature.py','7-L43')],
    'no proved mismatch in scoped alias; boundary/runtime proof incomplete','HOLD_FULL_RUNTIME_ACCEPTANCE','current1.17.0 probe is separate and must not fill historical pair cells')
add('O02','O02-NAMESPACE-COUNTER','P2',{'arguments':[[1.,3.,2.],[0.,1.,2.]],'wrong_replacement':'stats.trapezoid instead of integrate.trapezoid'},
    'numeric integration result','integrate function has y,x contract','stats callable is distribution constructor with c,d, not numerical quadrature',
    'distinct_official_API_roles_plus_current_negative_probe',['OS-PR-12934','OS-DOC-O02-new'],
    ['https://github.com/scipy/scipy/pull/12934','current-native.jsonl#O02-RUN-wrong_namespace-stats.trapezoid'],
    'same shortened label would conflate different public namespaces','REJECT_CROSS_NAMESPACE_MERGE','negative probe is researcher-defined and contributes no extra natural event')
add('O03','O03-P1-NORMAL','P1',{'points':[[0.],[1.],[2.]],'query':[0.],'k':None,'distance_upper_bound':1.1},
    'distance list[0,1] and index list[0,1], ordered nearest-first','source predicts both lists','1.6.0 compatibility branch explicitly reconstructs and sorts distances; warns',
    'fixed_implementation_static_prediction_not_native_pair',['OS-PR-12382','OS-DOC-O03-old'],
    [blob('1.5.4','scipy/spatial/kdtree.py','326-L406'),blob('1.6.0','scipy/spatial/kdtree.py','445-L470')],
    'normal output maintained by extra adapter code','CONDITIONALLY_SUPPORTED_NORMAL_ONLY','exact-boundary and OS integer-type behavior require separate checks')
add('O03','O03-P2-RETURNS','P2',{'same_points':[[0.],[1.],[2.]],'query':[0.],'r':1.1,'replacement':'query_ball_point'},
    'distances plus indices in nearest-distance order','old query Returns promises both outputs','new method Returns promises indices only; index sorting is not distance sorting',
    'two_edition_publisher_contracts_and_fixed_implementation',['OS-PR-12382','OS-DOC-O03-old','OS-DOC-O03-new'],
    [blob('1.6.0','scipy/spatial/kdtree.py','452-L470'),'https://docs.scipy.org/doc/scipy-1.6.0/reference/generated/scipy.spatial.KDTree.query_ball_point.html#returns'],
    'replacement suggestion is weaker than old return contract','REJECT_UNADAPTED_SUBSTITUTION','distance computation/sorting adapter may restore contract but must be tested')
add('O03','O03-BOUNDARY-RADIUS','P1/P2',{'points':[[0.],[1.],[2.]],'query':[0.],'radius':1.0},
    'preserve exact boundary convention','1.5.4 strict comparison ds < bound excludes point at1.0','1.6.0 wrapper delegates to ball query; possible inclusive-boundary difference',
    'static_discriminator_prediction_not_both_native_releases',['OS-PR-12382'],
    [blob('1.5.4','scipy/spatial/kdtree.py','363-L370'),blob('1.6.0','scipy/spatial/kdtree.py','459-L468')],
    'boundary equivalence not established','HOLD_BOUNDARY_EQUIVALENCE','old/new native execution of exact-radius input is the minimum discriminator')
add('O04','O04-P1-PROVIDER','P1',{'input':[[1,2],[3,4]],'labels':[[1,2],[2,4]],'index':[4,8,2],'call':'ndimage.sum'},
    '[4,0,5] preserving requested index order and absent-label0','old provider test_sum12 expected[4,0,5]','new provider test_sum_labels asserts old alias==new name==[4,0,5]',
    'provider_test_diff_read_not_historical_native_execution',['OS-PR-12242'],
    ['https://github.com/scipy/scipy/pull/12242',blob('1.5.4','scipy/ndimage/measurements.py','574-L616'),blob('1.6.0','scipy/ndimage/measurements.py','576-L632')],
    'no observed source-level alias mismatch','SUPPORTED_PROVIDER_TEST_SCOPE','past runtime not executed; current1.17.0 same input observed separately')
add('O04','O04-P2-PROVIDER','P2',{'same_provider_input':True,'replacement':'ndimage.sum_labels','boundary':'missing label8; unsupported complex dtype; mismatched labels'},
    'same output and required errors','shared _stats implementation and old function body','1.6.0 same _stats body plus wrapper; current1.17.0 both names give same normal/complex/shape outcomes',
    'fixed_implementation_and_current_native_supplement',['OS-PR-12242'],
    [blob('1.5.4','scipy/ndimage/measurements.py','467-L616'),blob('1.6.0','scipy/ndimage/measurements.py','469-L632'),'current-native.jsonl#O04-RUN-provider-sum_labels'],
    'no split of feature needed solely because preferred name changes','SUPPORTED_ALIAS_STRUCTURE_HOLD_PAST_RUNTIME','current1.17.0 supports observations only at that release')
add('O04','O04-HTTP-COUNTER','Q1/Q4',{'old_live_url':'https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.sum.html','installed_scipy':'1.17.0'},
    'URL state and function availability tracked independently','current old live document404','installed sum and sum_labels both return[4,0,5]',
    'current_http_plus_current_installed_native_observation',['OS-DOC-O04-live_old','OS-PR-12242'],
    ['http-observations.jsonl','current-native.jsonl#O04-RUN-provider-sum'],
    '404 cannot by itself prove function retirement','URL_ONLY_HOLD_NOT_FALSE_SPLIT','unversioned docs were serving a different current manual; no past redirect inferred')
jsonlines('observations.jsonl',obs)

dump('stream-summary.json',{'natural_slots':4,'natural_pairs_with_two_source_editions':4,
     'historical_native_pairs_executed':0,'source_derived_question_rows':len(obs),
     'independent_original_works_counted':len({s['work_id'] for s in sources if s['counted_independent_work']}),
     'independent_review_in_this_stream':False,'first_four_final':['O01','O02','O03','O04'],
     'excluded_repeat':'wminkowski1.6 warning enforcement of1.0 migration',
     'source_only_masked_packet':'evidence-packet.json','updated_utc':NOW})
print(json.dumps({'events':len(events),'source_rows':len(sources),'observation_rows':len(obs),'counted_original_works':len({s['work_id'] for s in sources if s['counted_independent_work']})}))
