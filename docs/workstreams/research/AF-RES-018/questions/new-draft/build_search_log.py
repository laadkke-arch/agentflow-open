#!/usr/bin/env python3
"""Write privacy-preserving discovery/read provenance; no response bodies."""
import datetime
import json
import pathlib
import urllib.parse

P = pathlib.Path(__file__).resolve().parent
def read(n): return json.loads((P/n).read_text())
def write(n,x): (P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
window = '2026-11-21T03:48:58Z/' + now
events = []
def query(engine,q,note='',at=None,recency=None):
    x={'operation':'search','engine':engine,'query':q,'query_string_precision':'exact as retained in session record',
       'accessed_at_utc':at or window,'timestamp_precision':'point' if at else 'bounded session interval',
       'result_level':'D0 until opened','count_as_read_source':False,'purpose':'sample discovery / probe construction, outside A/P experiment budgets','note':note}
    if recency is not None:x['recency_days']=recency
    events.append(x)

for q in [
 'site:softwarerecs.stackexchange.com/questions "2026" "Jun" software',
 'site:news.ycombinator.com/item "2026" "Ask HN" alternative',
 'site:reddit.com/r/selfhosted "2026" "recommend" "June"']:
    query('system2',q,'Initial date-window discovery; publication dates subsequently checked in direct sources.')
for q in [
 'site:softwarerecs.stackexchange.com/questions/ "Asked" "2026" "2 Answers"',
 'site:news.ycombinator.com "Ask HN:" "recommend" "2026"',
 'site:reddit.com/r/selfhosted "alternative" "2026" "November"',
 'site:github.com "discussions" "recommend" "Jul" "2026" alternative',
 'site:github.com "discussions" "looking for" "Sep" "2026" software',
 'site:github.com "discussions" "recommendations" "Jun" "2026" self-hosted']:
    query('system1',q,'Date words/recency are discovery filters, not direct date verification.',recency=173)
for term in ['recommend','alternative','looking','tool','software','library']:
    url='https://hn.algolia.com/api/v1/search?'+urllib.parse.urlencode({'query':term,'tags':'ask_hn','numericFilters':'created_at_i>1780272000,num_comments>1','hitsPerPage':100})
    events.append({'operation':'API search','canonical_replay_url':url,'url_precision':'parameters retained; exact parameter order/escaping not retained','query':term,'numeric_filter':'created_at_i>1780272000,num_comments>1',
                   'accessed_at_utc':window,'timestamp_precision':'bounded session interval','result_level':'D3-fetch','count_as_read_source':False,
                   'note':'Selected question bodies and reply trees opened separately through /api/v1/items/{id}; search results alone do not supply gold.'})
for term in ['alternative','recommend','looking for']:
    events.append({'operation':'API search','canonical_replay_url':'https://hn.algolia.com/api/v1/search_by_date?'+urllib.parse.urlencode({'query':term,'tags':'ask_hn','numericFilters':'created_at_i>1780272000,num_comments>1','hitsPerPage':60}),'url_precision':'parameters retained; exact parameter order/escaping not retained',
                   'query':term,'accessed_at_utc':window,'timestamp_precision':'bounded session interval','result_level':'D3-fetch','count_as_read_source':False,
                   'note':'Additional candidate discovery when Reddit absolute dates could not be directly confirmed.'})
events.append({'operation':'API search','canonical_replay_url':'https://api.stackexchange.com/2.3/questions?site=softwarerecs&fromdate=1780272000&sort=creation&order=desc&pagesize=100','url_precision':'known selection parameters only; exact original URL and optional filter not retained',
               'accessed_at_utc':window,'timestamp_precision':'bounded session interval','result_level':'D3-fetch','count_as_read_source':False,
               'note':'Question-list selection used creation date, answer count and accepted-answer evidence; later individual original revision and answer reads are recorded separately.'})

for q in [
 'site.backblaze.com computer backup Linux not supported',
 'site:proton.me/support custom domain free plan paid',
 'site:support.1password.com self hosted vault cloud 1Password',
 'site:sonarr.tv PVR usenet bittorrent',
 'site:ironfoxoss.org Play Store not available',
 'site:github.com/pbs-software PBS FAQ',
 'site:docs.mitmproxy.org javascript DOM response modify proxy',
 'site:github.com bash-parser javascript license MIT',
 'site:support.apple.com Safari only Apple devices Android',
 'site:anthropic.com "closed" "weights" Claude models',
 'site:docs.anthropic.com "open-weight" Claude']:
    query('system2',q,'Probe construction and attempts to disprove proposed hard-condition violations; only later body reads count as evidence.')
for q in ['site:swagger.io/tools/swagger-ui/ Swagger UI','WireDSL official wireframe DSL','site:builtwith.com technology lookup API','site:electrobun.dev Electrobun']:
    query('system2',q,'Auxiliary control entity verification. Precise second was not recorded for this search; following opens began 04:14:57 UTC.')
for q in ['site:pentaho.com data integration','"Qwen3.8-27B" official','site:bytemail.app email','site:anthropic.com Claude Sonnet 4']:
    query('system2',q,'Positive/auxiliary entity URL resolution; no product use or account creation.',at='2026-11-21T04:15:14Z')
query('system1','Pentaho data integration official site','Domain filter pentaho.com; primary source verification after system2 did not return the needed product page.',at='2026-11-21T04:15:24Z')

# Earlier query topics were not kept verbatim. Explicitly report this logging gap.
events.append({'operation':'search-history-gap','accessed_at_utc':window,'timestamp_precision':'bounded session interval',
               'query':None,'query_string_precision':'not retained; do not reconstruct as exact',
               'topics':['HN software alternatives after June 2026','Reddit self-hosted backup, offline tools, notes, RSS, PDF and password-manager requests',
                         'Flameshot active-window capture, Wispr offline mode, Pi-hole channel filtering, Borg S3, Swagger inputs, 1Password self-hosting'],
               'count_as_read_source':False,'note':'Directly opened URLs and conclusions are retained in sources-draft.json. Search logs cannot claim exact replay of these earlier query strings.'})

source_doc=read('sources-draft.json')
for s in source_doc['sources']:
    events.append({'operation':'body_read_evidence','source_id':s['id'],'url':s['url'],'accessed_at_utc':s['accessed_at_utc'],
                   'timestamp_precision':s.get('access_time_precision'),'level':s['level'],'sections_read':s['sections_read'],
                   'count_as_method_literature':False,'note':'Evidence-level record, not necessarily a distinct HTTP call; batch API reads and repeated source URLs must not be summed as worker budget.'})
for r in source_doc['excluded']:
    events.append({'operation':'excluded_or_failed_read',**r,'accessed_at_utc':r.get('accessed_at_utc',window),
                   'count_as_read_source':False})
for r in read('dedup-and-selection.json')['excluded_after_body_read']:
    events.append({'operation':'body_read_then_sample_exclusion','url':r['url'],'accessed_at_utc':window,'timestamp_precision':'bounded session interval',
                   'confirmed':r['reason'],'limits':'Not a selected experimental input; no body, author or profile retained.','level':'D1','count_as_selected_question':False})
for r in read('network.json'):
    events.append({'operation':'anonymous_network_check',**r,'level':'D3-fetch','count_as_read_source':False})

write('SEARCH_LOG.json',{'sampling_window':{'from':'2026-06-01','through':'2026-11-21'},'recorded_at_utc':now,'events':events,
      'limits':['Some earlier query strings and exact web-call times were not retained; this is stated explicitly rather than reconstructed as precise observations.',
                'API creation dates and initial revision metadata, not search snippets, determine final new-sample inclusion.',
                'This log belongs to preparation. A/P workers must keep independent exact queries/opened URLs and count their own budgets.']})

first={}
for s in source_doc['sources']:
    host=urllib.parse.urlparse(s['url']).hostname
    if host not in first:
        first[host]={'host':host,'first_recorded_body_url':s['url'],'accessed_at_utc':s['accessed_at_utc'],'anonymous':True,
                     'transport':'web search/open or public API; see exact network checks for API/HTML transports',
                     'observed_result':'document body read','http_status':None,
                     'http_status_note':'Web retrieval did not expose a numeric origin HTTP status. Do not infer 200 from body availability.'}
write('network-web.json',{'host_records':list(first.values()),'exact_http_checks_file':'network.json',
      'limits':'This records access confirmation with honestly unavailable status codes for the web tool; it is not a claim of the required numeric preflight status for every host.'})
print(json.dumps({'search_log_events':len(events),'web_host_records':len(first)}))
