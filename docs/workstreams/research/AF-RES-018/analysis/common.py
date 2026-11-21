"""Shared analysis utilities. Read recorded observations; do not infer executions."""
from pathlib import Path
import datetime,hashlib,json,math,statistics,urllib.parse
ROOT=Path(__file__).resolve().parents[1]
def load(path,default=None):
    f=ROOT/path
    return json.loads(f.read_text()) if f.exists() else default
def save(path,obj):
    f=ROOT/path;f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def parse_time(s):
    if not s:return None
    if s.endswith(' UTC'):
        return datetime.datetime.strptime(s,'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=datetime.timezone.utc)
    return datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
def elapsed(a,b):
    a,b=parse_time(a),parse_time(b)
    return (b-a).total_seconds() if a and b else None
def document_counts(docs):
    seen=set();opened=0;failed=0;revisits=0;finds=0
    for d in docs:
        url=str(d.get('url',''));parts=urllib.parse.urlsplit(url)
        key=urllib.parse.urlunsplit((parts.scheme,parts.netloc,parts.path,parts.query,''))
        op=str(d.get('operation','')).lower()
        if op=='find':finds+=1;revisits+=1;continue
        if d.get('status')=='opened':
            if key in seen:revisits+=1
            else:seen.add(key);opened+=1
        else:failed+=1
    return {'logged_document_events':len(docs),'unique_successfully_opened_urls':opened,
            'failed_open_attempts':failed,'revisits_or_finds':revisits,'explicit_find_events':finds,
            'normalized_document_budget':opened+failed,
            'definition':'Successful exact URLs excluding fragments counted once; failed opens count each attempt; explicit find operations are rereads.'}
def quantile(values,p):
    if not values:return None
    s=sorted(values);x=(len(s)-1)*p;lo=math.floor(x);hi=math.ceil(x)
    return s[lo]+(s[hi]-s[lo])*(x-lo)
def avg(values):
    values=[x for x in values if x is not None]
    return statistics.mean(values) if values else None
def ratio(n,d):return n/d if d else None
def check_decision(c):return c.get('decision',c.get('verdict'))
def temporal_category(record):
    if record.get('post_decision') is True:return 'post_decision'
    if record.get('date_status')=='pre_decision':return 'pre_decision'
    return 'unknown'
def run_costs(run,receipt):
    documents=document_counts(run['opened_documents']);firstdocs=run['opened_documents'][:receipt['document_prefix_count']]
    return {'queries':len(run['queries']),'declared_open_budget':run['budget']['opened_pages'],
            **documents,'stage1_queries':receipt['query_prefix_count'],
            'stage1_document_budget':document_counts(firstdocs)['normalized_document_budget'],
            'raw_response_words':len(run['raw_response'].split()),
            'total_wall_seconds':elapsed(run.get('started_at_utc'),run.get('ended_at_utc')),
            'stage1_wall_seconds':elapsed(run.get('started_at_utc'),run.get('stage1_frozen_at_utc')),
            'checks_wall_seconds':elapsed(run.get('checks_started_at_utc'),run.get('checks_ended_at_utc')),
            'exposure_count':len(run.get('exposures',[])),
            'post_question_document_count':sum(temporal_category(d)=='post_decision' for d in run['opened_documents']),
            'unknown_date_document_count':sum(temporal_category(d)=='unknown' for d in run['opened_documents'])}
