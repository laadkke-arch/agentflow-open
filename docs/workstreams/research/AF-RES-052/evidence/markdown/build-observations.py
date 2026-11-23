"""Rebuild AF-RES-052 Markdown observation ledgers from already-read source receipts.

No network, code execution from suppliers, or edits to presealed input files.
Cache files are local read aids and deliberately excluded from the submission.
"""
from pathlib import Path
import csv
import hashlib
import json
import re
from html.parser import HTMLParser

HERE = Path(__file__).resolve().parent
CACHE = HERE / 'cache'
REMARK = '1146b3a274fc1f4607111e5d6607a3a769a0e89a'
UTILITY = '655f117443d99a08cb839765ff7489aa759f72d0'
MDAST = 'c034ec9ddb8ca2ab16de90d668433624bdd92179'
UNIST = '8b10b6113c1463113b879f423d605547e04efd0d'
IMPL = 'IM-M1-current-configured'
HISTORY = '미확인: requester react-stringify10.0.2 label unresolved; unified10.1.1 not tested'

def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()

def blob(text):
    b = text.encode()
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def jsonl(name, rows):
    (HERE / name).write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in rows))

def csvfile(name, rows, fields=None):
    with (HERE / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields or list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def real_headings(text):
    result = []
    fence = None
    for n, line in enumerate(text.splitlines(), 1):
        f = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if f:
            marker = f.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not f.group(2).strip():
                fence = None
            continue
        if fence:
            continue
        h = re.match(r'^(#{1,6})\s+(.+)$', line)
        if h:
            result.append((n, len(h.group(1)), h.group(2)))
    return result

def section(text, title):
    headings = real_headings(text)
    start = next(h for h in headings if h[2] == title)
    end = next((h[0]-1 for h in headings if h[0] > start[0] and h[1] <= start[1]), len(text.splitlines()))
    lines = text.splitlines()
    body = '\n'.join(lines[start[0]:end])
    tokens = list(re.finditer(r'\S+', body))
    if len(tokens) > 800:
        body = body[:tokens[799].end()]
        end = start[0] + body.count('\n') + 1
    return {'source_lines': f'L{start[0]}-L{end}', 'window_words': min(800, len(tokens)), 'window_sha256': sha(body), 'text': body}

class Visibility(HTMLParser):
    def __init__(self):
        super().__init__()
        self.details = []
        self.script = 0
        self.hits = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.script += 1
        if tag == 'details':
            self.details.append(dict(attrs))
    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.script = max(0, self.script-1)
        if tag == 'details' and self.details:
            self.details.pop()
    def handle_data(self, data):
        if not self.script and (data.strip() in ('fence', 'fences') or 'use fenced code always' in data):
            self.hits.append({'label_or_paraphrase': 'fence/fences option text', 'details_ancestor_count': len(self.details), 'closed_details_ancestor_count': sum('open' not in d for d in self.details)})

arrivals = [json.loads(x) for x in (HERE / 'arrivals.jsonl').read_text().splitlines()]
by_rank = {x['original_rank']: x for x in arrivals}
for a in arrivals:
    a['reading_projection'] = 'Fixed source-order window; not a measured rendered viewport, click session, or reader study.'
    a['collapsed_details_policy'] = 'Text inside collapsed details is source exposure only and supplies no 1-action positive atom.'
    a['positive_atoms'] = ['M-N1-C1'] if a['original_rank'] == 4 else []
    a['positive_atom_scope'] = 'current functional option; requester historical version unconfirmed' if a['original_rank'] == 4 else 'none'
    if a['original_rank'] == 4:
        a['visibility_check'] = 'Exact HTML fence/fences L160-L167 text has zero details ancestors; first two information hrefs precede any details.'
jsonl('arrivals.jsonl', arrivals)

anchors = [json.loads(x) for x in (HERE / 'anchor-arrivals.jsonl').read_text().splitlines()]
anchor_files = {'MA-R1-H1': ('remark-readme.md', 'Syntax'), 'MA-R1-H2': ('remark-readme.md', 'Syntax tree'), 'MA-R3-H2': ('vendor-parse.md', 'What is this?'), 'MA-R4-H2': ('vendor-stringify.md', 'What is this?'), 'MA-R5-H2': ('vendor-cli.md', 'What is this?')}
for a in anchors:
    file, title = anchor_files[a['arrival_id']]
    data = section((CACHE/file).read_text(), title)
    data.pop('text')
    a.update(data)
    a['boundary_method'] = 'ATX headings outside fenced code only; end before next equal/higher-level heading; max800 words'
    a['checked_utc'] = by_rank[int(a['arrival_id'][4])]['checked_utc']
    a['reading_projection'] = 'Verified source section and exact HTML anchor; no browser interaction executed.'
jsonl('anchor-arrivals.jsonl', anchors)

v = Visibility()
v.feed((CACHE/'exact-http-4.html').read_text())
assert v.hits and all(x['closed_details_ancestor_count'] == 0 for x in v.hits)
(HERE/'visibility-check.json').write_text(json.dumps({'arrival_id': 'MA-R4', 'source_lines': 'L160-L167', 'exact_html_sha256': by_rank[4]['exact_html_sha256'], 'checks': v.hits, 'result': 'C1 option text lies outside collapsed details', 'limits': 'HTML structure inspection only; not screenshot/viewport or user behavior validation. Other collapsed details supply no positive evidence.'}, ensure_ascii=False, indent=2)+'\n')

receipts = {x['id']: x for x in json.loads((HERE/'observation-read-receipts.json').read_text())}
outside = {x['name']: x for x in json.loads((CACHE/'outside-http-receipts.json').read_text())}
sources = []
def source(sid, publisher, work, kind, allocation, url, checked, version, locator, observed, limits, file=None, parent=None, duplicate=None, stance='supports_or_limits'):
    d = {'source_id': sid, 'question_ids': ['Q4','Q5','Q7'], 'requirement_ids': ['M-N1'], 'case_ids': ['D-M1'], 'publisher': publisher, 'work_id': work, 'source_type': kind, 'allotment': allocation, 'url': url, 'checked_utc': checked, 'version_sha': version, 'locator': locator, 'observed': observed, 'limitations': limits, 'stance': stance, 'duplicate_of': duplicate, 'evidence_parent': parent, 'direct_open': True, 'source_status': 'read'}
    if file:
        t = (CACHE/file).read_text()
        d['source_sha256'] = sha(t)
        d['blob_sha'] = blob(t)
    sources.append(d)
    return d

base = f'https://github.com/remarkjs/remark/blob/{REMARK}/'
source('M-VENDOR-ROOT', 'remarkjs', 'remark-readme', 'supplier_document', 'duplicate_existing_work', base+'readme.md', by_rank[1]['checked_utc'], REMARK, 'L154-L177; first800 words L2-L231; Syntax L398-L407; Syntax tree section', '첫 문서는 parser, serializer, 결합 패키지, CLI 네 패키지를 소개한다. 이름 네 개가 요구 완결 구현 네 개를 뜻하지 않으며 첫 두 정보 링크는 Syntax와 Syntax tree다.', '라우팅 시 전문과 창이 사전에 노출된 같은 저작. 접힌 예제는 사용자 1동작 근거에 포함하지 않는다. C1/C2 출력 보장은 창에서 확인되지 않는다.', 'remark-readme.md', duplicate='M-LIST-ROUTE')
source('M-VENDOR-SITE', 'remarkjs', 'remark-homepage', 'supplier_document', 'supplier_doc', 'https://remark.js.org', by_rank[2]['checked_utc'], 'live HTML SHA256:'+by_rank[2]['exact_html_sha256'], 'static homepage web L0-L16', '변환 생태계와 playground를 소개하며 첫 두 정보 목적지는 CommonMark 안내와 unified 홈페이지다.', '플레이그라운드는 실행하지 않았다. 제품판과 요구의 code-node 출력은 정적 본문에서 확인되지 않는다. 독립 구현 근거가 아니다.')
source('M-VENDOR-PARSE', 'remarkjs', 'remark-parse-readme', 'supplier_document', 'supplier_doc', base+'packages/remark-parse/readme.md', by_rank[3]['checked_utc'], REMARK, 'L8; L30-L52; first800 words L2-L284', 'Markdown을 syntax tree로 바꾸는 입력 parser이며 serializer를 함께 쓰는 조합을 소개한다. 첫 두 링크는 root README와 What is this 절이다.', '요구는 AST에서 Markdown으로 나가는 방향이다. 본문이 serializer 이름을 언급해도 C1/C2 출력 조건의 증명이 되지 않는다.', 'vendor-parse.md')
source('M-VENDOR-STRINGIFY', 'remarkjs', 'remark-stringify-readme', 'supplier_document', 'supplier_doc', base+'packages/remark-stringify/readme.md', by_rank[4]['checked_utc'], REMARK, 'L8; L28-L37; L160-L167; first800 words L2-L210', 'AST를 Markdown으로 출력하는 직렬화기다. fence의 기본 marker와 fences=true의 항상 fence 출력 규칙은 언어 없는 노드의 C1을 현재판에서 지지한다.', '같은800단어 창은 lang과 value를 유지하는 구체 출력을 명시하지 않아 C2는 미확인이다. 역사 요청의 react-stringify10.0.2와 동일하다고 고치지 않는다.', 'vendor-stringify.md')
source('M-VENDOR-CLI', 'remarkjs', 'remark-cli-readme', 'supplier_document', 'supplier_doc', base+'packages/remark-cli/readme.md', by_rank[5]['checked_utc'], REMARK, 'L26-L37; L101-L107; first800 words L2-L212', '파일을 검사·변환하는 CLI 및 설정/트리 입출력 옵션을 설명한다. 첫 두 정보 링크는 root와 자체 개요 절이다.', '같은 serializer 계열의 인터페이스이며 독립 대안으로 더하지 않는다. C1/C2 출력 또는 요청 역사판을 창에서 확인하지 못했다.', 'vendor-cli.md')
source('M-VENDOR-MDAST', 'syntax-tree', 'mdast-specification', 'supplier_feature_specification', 'supplier_doc', f'https://github.com/syntax-tree/mdast/blob/{MDAST}/readme.md', by_rank[6]['checked_utc'], MDAST, 'L7-L15; L205-L268; first800 words L2-L358', 'Code의 nullable lang 및 value 필드와 Markdown에서 만들어지는 노드 예시를 규정한다. B에서 rank6이 대표로 올라온다.', '명세 문서는 실행 가능한 serializer가 아니다. 예시는 Markdown→AST 방향이며 AST→Markdown fence 선택을 입증하지 않는다. 본문은 unreleased 변경 가능성을 고지한다.', 'vendor-mdast.md')
code_sources = [
 ('M-CODE-PACKAGE','remarkjs','remark-stringify-package-manifest','stringify-package.json',base+'packages/remark-stringify/package.json',REMARK,'L8-L12; L42-L51','현재 소스의 패키지는11.0.0이며 mdast-util-to-markdown ^2.0.0와 unified ^11.0.0을 선언한다.','범위는 허용 조합을 뜻한다. 실제 설치가 정확히2.0.0으로 해석됐다는 관측 또는 과거 버전 증거가 아니다.'),
 ('M-CODE-COMPILER','remarkjs','remark-stringify-compiler','stringify-compiler.js',base+'packages/remark-stringify/lib/index.js',REMARK,'L11; L23-L38','직렬화 compiler는 tree와 설정/옵션을 mdast-util-to-markdown의 toMarkdown에 전달한다.','실행하지 않았다. 플러그인/사용자 handler가 동작을 변경하는 설치까지 보장하지 않는다.'),
 ('M-CODE-HANDLER','syntax-tree','mdast-util-to-markdown-code-handler','code-handler.js',f'https://github.com/syntax-tree/mdast-util-to-markdown/blob/{UTILITY}/lib/handle/code.js',UTILITY,'L20-L47; L64-L72','code handler는 marker fence를 만들고 안전한 언어 라벨과 원래 value를 순서대로 출력한다. 일반 javascript 라벨과 제시 코드 내용은 조건을 만족하는 소스 경로다.','D2 코드 판독이며 실행 아님. 주목록의 새 독립 구현이 아니라 rank4 serializer의 구현 계보다.'),
 ('M-CODE-INDENT','syntax-tree','mdast-util-to-markdown-indentation-rule','code-indent.js',f'https://github.com/syntax-tree/mdast-util-to-markdown/blob/{UTILITY}/lib/util/format-code-as-indented.js',UTILITY,'L11-L20','fences=false와 언어 미지정 등이 함께 맞을 때 들여쓰기 코드로 출력하도록 분기한다.','설정 변화는 C1을 깨는 반례이며 모든 현재/과거판에 보편적으로 적용하지 않는다.'),
 ('M-CODE-FENCE','syntax-tree','mdast-util-to-markdown-fence-marker','code-fence.js',f'https://github.com/syntax-tree/mdast-util-to-markdown/blob/{UTILITY}/lib/util/check-fence.js',UTILITY,'L10-L21','기본 marker는 backtick이며 tilde도 허용한다.','tilde 선택은 유효한 Markdown이어도 사용자의 backtick 요구를 깨므로 완결에서 제외한다.')
]
for sid,pub,work,file,url,ver,loc,obs,limit in code_sources:
    source(sid,pub,work,'implementation_source','supplemental_code',url,receipts[sid]['checked_utc'],ver,loc,obs,limit,file,parent='M-VENDOR-STRINGIFY')
source('M-HOP-COMMONMARK','CommonMark','commonmark-help','official_reference','outside_pool_context','https://commonmark.org/help/',outside['commonmark-help']['checked_utc'],'live HTML SHA256:'+outside['commonmark-help']['sha256'],'Code blocks; web L51-L60','일반 Markdown 코드 블록 문법은 fence와 들여쓰기 두 표현을 허용한다.','해당 구현·판의 직렬화 정책이 아니며 들여쓰기 허용이 사용자 backtick 요구를 만족시킨다는 뜻도 아니다.',parent='M-VENDOR-SITE',stance='counterexample_to_semantic_equivalence')
source('M-HOP-UNIFIED','unified collective','unified-homepage','official_reference','outside_pool_context','https://unifiedjs.com',outside['unified-home']['checked_utc'],'live HTML SHA256:'+outside['unified-home']['sha256'],'homepage intro and first800-word source projection','구조화 텍스트 처리와 Markdown/HTML 도구의 생태계를 소개한다.','현재 요구의 code node fence 및 언어/내용 보존을 동일 serializer판에서 확인할 직접 근거는 없다.',parent='M-VENDOR-SITE')
source('M-HOP-UNIST','syntax-tree','unist-specification','official_reference','outside_pool_context',f'https://github.com/syntax-tree/unist/blob/{UNIST}/readme.md',receipts['M-HOP-UNIST']['checked_utc'],UNIST,'Syntax tree L41-L56; README top source projection','추상/구체 syntax tree의 차이와 일반 node 표현을 설명한다. mdast가 참조하는 상위 명세다.','root와 #syntax-tree는 한 저작이다. Markdown serializer 구현 또는 요구 출력의 증거가 아니다.','unist.md',parent='M-VENDOR-MDAST')
jsonl('observation-sources.jsonl',sources)

sources = []
release = json.loads((CACHE/'release15.json').read_text())
rbody = release['data']['body']
r = source('M-RELEASE-15','remarkjs','remark-release-15','release_note','release_test','https://github.com/remarkjs/remark/releases/tag/15.0.0',release['checked_utc'],'tag15.0.0; published2023-09-18T09:47:14Z; bodySHA256:'+sha(rbody),'Change section body L7-L12','발행자는 stringify 기본 fences가 true로 변경됐다고 기록한다. 2022 요청 뒤의 변경이므로 현재 기본동작을 역사판에 소급하면 안 된다.','같은 문장의 false에 관한 마이그레이션 설명은 현재 옵션 문서/소스/시험과 충돌한다. 기본변경과 문제의 설명을 분리하며 후자를 성공근거로 쓰지 않는다.',parent='M-VENDOR-STRINGIFY',stance='supports_version_change_and_contains_conflict')
r['published_at'] = release['data']['published_at']
source('M-TEST-UTILITY','syntax-tree','mdast-util-to-markdown-behavior-tests','behavior_test_source','release_test',f'https://github.com/syntax-tree/mdast-util-to-markdown/blob/{UTILITY}/test/index.js',receipts['M-TEST-UTILITY']['checked_utc'],UTILITY+' (tag2.0.0)','Code flow L794-L979; esp L810-L819,L929-L930','직접 읽은 assertion은 언어 없는 기본 fence 출력, false일 때 indent, lang과 value 동시 보존을 각각 검사한다.','D2 시험 원문 판독이다. 테스트 실행·패키지 설치·원요청의 전체 AST 재현은 하지 않았다. 생성과정은 rank4의 계보이며 새 독립 대안으로 세지 않는다.','to-markdown-tests.js',parent='M-CODE-HANDLER')
source('M-TEST-REMARK','remarkjs','remark-integration-tests','behavior_test_source','release_test',base+'test.js',receipts['M-TEST-REMARK']['checked_utc'],REMARK,'L187-L206; extension scenario L208 onward','unified와 remark-stringify를 연결한 문단 직렬화 assertion 및 extension 시나리오를 확인했다.','요구941의 code-node 쌍 자체를 검사하는 assertion은 이 인용 구간에 없다. wrapper 연결의 보조 근거이며 C1/C2를 대신하지 않고 실행도 하지 않았다.','remark-tests.js',parent='M-CODE-COMPILER')
jsonl('release-test-sources.jsonl',sources)

outside_arrivals = []
for rank, hop, name, url, section_name in [(2,1,'commonmark-help','https://commonmark.org/help/','CommonMark help including Code blocks'),(2,2,'unified-home','https://unifiedjs.com','Homepage intro')]:
    d=outside[name]
    outside_arrivals.append({'arrival_id':f'MA-R{rank}-H{hop}','requested_url':url,'final_url':d['final_url'],'http_status':d['status'],'checked_utc':d['checked_utc'],'html_sha256':d['sha256'],'actual_section':section_name,'original_pool_member':False,'supports_current_atoms':[],'complete_ids':[],'limitation':'Live static text; no rendered UI or interactive script execution; no same-version runtime requirement proof.'})
for hop,url,title in [(1,'https://github.com/syntax-tree/unist#syntax-tree','Syntax tree'),(2,'https://github.com/syntax-tree/unist','README top after H1')]:
    d={'arrival_id':f'MA-R6-H{hop}','requested_url':url,'source_commit':UNIST,'actual_section':title,'original_pool_member':False,'checked_utc':receipts['M-HOP-UNIST']['checked_utc'],'supports_current_atoms':[],'complete_ids':[],'limitation':'Exact requested GitHub URL opened by web reader; immutable source separately pins same work. Specification is not executable serializer.'}
    if hop==1:
        sd=section((CACHE/'unist.md').read_text(),'Syntax tree');sd.pop('text');d.update(sd)
    else:
        d['source_lines']='README first800-word source projection'
    outside_arrivals.append(d)
jsonl('outside-arrivals.jsonl',outside_arrivals)

evidence=[]
def ev(eid, rank, impl, atom, status, level, view, refs, locators, why, limit):
    evidence.append({'evidence_id':eid,'case_id':'D-M1','purpose_id':'M-N1','pool_rank':rank,'implementation_id':impl,'condition_id':atom,'condition_status':status,'evidence_level':level,'scope':view,'source_ids':refs,'locators':locators,'judgment':why,'limitations':limit,'historical_status':HISTORY})
for rank in range(1,7):
    for atom in ['M-N1-C1','M-N1-C2']:
        supported=rank==4 and atom=='M-N1-C1'
        reason={1:'Root names several packages but gives neither required code output guarantee.',2:'Homepage/playground introduction is not an executed code-node output.',3:'Parser direction differs; serializer name is mentioned without the required output evidence.',4:'fence/backtick and fences=true explicitly support C1; generic serializer definition does not prove lang/value retention for C2.',5:'CLI is another interface to the same lineage; no required code output in this window.',6:'mdast is a data specification in input direction; no executable serialization policy.'}[rank]
        ev(f'ME-R{rank}-{atom[-2:]}',rank,IMPL if rank==4 else '',atom,'supports_current_atom' if supported else '미확인','D1','exact-arrival first800 source projection',f'M-VENDOR-{["ROOT","SITE","PARSE","STRINGIFY","CLI","MDAST"][rank-1]}',f'MA-R{rank}; '+('L160-L167' if rank==4 else 'arrival window'),'현재 기능 부분조건 확인' if supported else reason,'No unsupported atom is treated as functional failure. Current source cannot establish requester historical tuple.')
for atom,refs,loc in [('M-N1-C1','M-CODE-PACKAGE;M-CODE-COMPILER;M-CODE-FENCE;M-CODE-INDENT;M-TEST-UTILITY','package L8-L12,L51; compiler L31-L38; fence L10-L21; indentation L11-L20; test L810-L819'),('M-N1-C2','M-CODE-PACKAGE;M-CODE-COMPILER;M-CODE-HANDLER;M-TEST-UTILITY','package L8-L12,L51; compiler L31-L38; handler L37-L47,L64-L72; test L929-L930')]:
    ev('ME-GOLD-'+atom[-2:],4,IMPL,atom,'supports_configured_current_possibility','D2','independent implementation/code/test reading; outside eligible two-action windows',refs,loc,'Declared compatible composition: remark-stringify11.0.0 at '+REMARK+' + mdast-util-to-markdown2.0.0 at '+UTILITY+'; unified^11; fences=true; fence=backtick; no overrides.','Source-supported conditional gold, not observed installed dependency or D3 execution. Utility is rank4 implementation lineage, not a new independent alternative.')
ev('ME-HISTORY',4,IMPL,'M-N1-C1;M-N1-C2','미확인','none','original requester environment','M-ISS-941;M-RELEASE-15','issue body L8-L10; release Change L7-L12','Original react-stringify label unresolved and 2022 tuple not reconstructed.','Current behavior cannot be backdated across a documented default change.')
csvfile('evidence.csv',evidence)

plans=json.loads((HERE.parent/'path-plan.json').read_text())['plans']
plans=[x for x in plans if x['case_id']=='D-M1']
assert len(plans)==34
for method,reps in [('A',[1,2,3]),('B',[1,6]),('C',[1,2,3])]:
    for rank in reps:
        for hop,href in enumerate(by_rank[rank]['first_two_information_hrefs'],1):
            plans.append({'plan_id':f'D-M1-{method}-H{rank}{hop}','case_id':'D-M1','method':method,'kind':'representative_next_href','purpose_id':'M-N1','actions':2,'steps':[{'action':'open_url','rank':rank,'url':by_rank[rank]['requested_url']},{'action':'open_information_href','from_rank':rank,'href_ordinal':hop,'url':href['resolved_url']}]})
assert len(plans)==50
paths=[]
for p in plans:
    ranks=[x['rank'] for x in p['steps'] if x['action']=='open_url']
    c1=4 in ranks
    ids=[]
    for x in p['steps']:
        if x['action']=='open_url':ids.append('MA-R'+str(x['rank']))
        elif x['action']=='open_information_href':
            if x['from_rank']==3 and x['href_ordinal']==1:ids.append('MA-R1')
            else:ids.append(f"MA-R{x['from_rank']}-H{x['href_ordinal']}")
    exact_pool_urls={a['requested_url'] for a in arrivals}
    outside_urls=[x['url'] for x in p['steps'] if x['action']=='open_information_href' and x['url'] not in exact_pool_urls]
    outside_work_urls=[x['url'] for x in p['steps'] if x['action']=='open_information_href' and x['from_rank'] in [2,6]]
    paths.append({'path_id':p['plan_id'],'case_id':'D-M1','purpose_id':'M-N1','method':p['method'],'path_kind':p['kind'],'actions':p['actions'],'steps_json':json.dumps(p['steps'],ensure_ascii=False,separators=(',',':')),'arrival_ids':';'.join(ids),'current_supported_atoms':'M-N1-C1' if c1 else '', 'current_unconfirmed_atoms':'M-N1-C2' if c1 else 'M-N1-C1;M-N1-C2','complete_current_ids':'','complete_current_count':0,'historical_status':HISTORY,'maximum_complete_this_trial':0,'outside_original_pool_urls':';'.join(outside_urls),'outside_original_pool_work_urls':';'.join(outside_work_urls),'outside_pool_complete_ids':'','positive_atom_source':'M-VENDOR-STRINGIFY:L160-L167' if c1 else '', 'judgment':'관측 0 full completion; C1 only' if c1 else '관측 0 full completion; both atoms unconfirmed within this trial','reading_limit':'Fixed source projection, not rendered viewport or user test; no union of partial atoms across different trials; code/tests excluded from this action budget'})
csvfile('paths.csv',paths)

sens=[]
for method,reps3,reps4 in [('A','1;2;3','1;2;3;4'),('B','1;6','1;6'),('C','1;2;3','1;2;3;4')]:
    sens.append({'sensitivity_id':'MS-SLOT4-'+method,'case_id':'D-M1','method':method,'change':'slots3_to4','baseline_representatives':reps3,'sensitivity_representatives':reps4,'first_changed_original_rank':4 if method!='B' else '', 'direct_current_complete_delta':0,'two_action_complete_delta':0,'direct_supported_atom_delta':'M-N1-C1@rank4' if method!='B' else '', 'interpretation':'serializer option becomes direct; C2 still absent from window' if method!='B' else 'two groups already exhausted; no representative change','status':'observed exact rank4 arrival reused under separately frozen array sensitivity'})
sens.append({'sensitivity_id':'MS-C-VERSION-SENTINEL','case_id':'D-M1','method':'C','change':'unknown_product_version_as_same_sentinel_only','baseline_representatives':'1;2;3','sensitivity_representatives':'1;2;3','first_changed_original_rank':'','direct_current_complete_delta':0,'two_action_complete_delta':0,'direct_supported_atom_delta':'','interpretation':'other fields still unknown or different; no five-field equality, C remains A','status':'computed from frozen metadata; no destination meaning used to fill key'})
csvfile('sensitivity-observations.csv',sens)

metrics={'case_id':'D-M1','primary_sample_member':False,'purpose_id':'M-N1','exact_urls':6,'all_section_urls':8,'section_exhausted_at_cap':False,'exact_http_success':6,'publisher_upstream_groups':2,'conditional_current_gold_ids':[IMPL],'strict_historical_gold':'미확인','original_pool_window_complete_ids':[],'original_pool_window_supported_atoms':['M-N1-C1'],'independent_new_runtime_alternatives_promoted':0,'unexecuted_supplier_tests':True,'source_projection_not_viewport':True,'methods':{}}
for m in 'ABC':
    rows=[p for p in paths if p['method']==m]
    metrics['methods'][m]={'paths':len(rows),'direct_complete_ids':[],'two_action_complete_id_union':[],'single_trial_maximum_complete':0,'direct_current_supported_atoms':[],'two_action_atom_union':['M-N1-C1'] if m=='B' else [],'positive_atom_path_ids':[p['path_id'] for p in rows if p['current_supported_atoms']],'history':'미확인','outside_pool_complete_ids':[]}
(HERE/'diagnostic-metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'paths':len(paths),'path_counts':{m:len([p for p in paths if p['method']==m]) for m in 'ABC'},'positive_atom_paths':[p['path_id'] for p in paths if p['current_supported_atoms']],'evidence_rows':len(evidence),'anchor_boundaries':{a['arrival_id']:a['source_lines'] for a in anchors}},ensure_ascii=False))
