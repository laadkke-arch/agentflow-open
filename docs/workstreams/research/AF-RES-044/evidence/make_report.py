"""Render required 12-row and 36-row tables, then paired interpretation."""
import json,csv
from urllib.parse import urldefrag
from build_study import ROOT,E,load,readcsv

def link(label,url):return '['+label+']('+url+')' if url else '**미확인**'
def clean(s):return str(s).replace('|','\\|').replace('\n',' ')
def table(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(clean(c) for c in r)+' |' for r in rows])
data=load('evidence/results-data.json');cases=load('evidence/cases.json');pool=readcsv('pool.csv');gold=load('evidence/pool-gold-summary.json');sources=load('evidence/source-count-audit.json')
views=data['views'];clicks=readcsv('clicks.csv');bytrial={r['trial_id']:r for r in clicks}
bycase={c['case_id']:c for c in cases};bypool={r['candidate_id']:r for r in pool}
def cl(id):return link(id,bypool[id]['url'])
complete={
'P1':'**미확인**. 원풀 미관측; 진단의 task_lists와 Lua filter 가능성을 완전 경로로 대입하지 않음.',
'P2':'**미확인**. 원풀 미관측; LaTeX writer 수정은 원요구 reader 방향의 증명이 아님.',
'P3':'**미확인**. 원풀 미관측; 일반 PDF 엔진 목록과 요청된 추가 엔진 지원을 구별.',
'P4':'**미확인**. 원풀 미관측; DITA 출력의 실제 구현 경로 미확인.',
'V1':'확인된 완전 대안0. View Configuration에는 원 v4 subtitle 색 계약의 완전 증거가 없음.',
'V2':'확인된 완전 대안0. identity/reflectY 일부 설명은 있으나 graticule·label 결합 및 원 spec 성공이 빠짐.',
'V3':'관측 풀의 완전 대안0. text mark의 문자열 출력은 word-cloud layout 증거가 아님. 원규칙 표본은 **미확인**.',
'V4':'확인된 완전 대안0. Transform/Aggregate는 tree/dendrogram 지원 증거가 아님.',
'C1':'HTTPX: '+cl('C1-1')+' 최초800 또는 '+cl('C1-2')+' Timeouts 또는 '+cl('C1-5')+' Request instances. Requests: '+cl('C1-4')+' Prepared Requests346 words. 독립 클라이언트2.',
'C2':'10개: '+cl('C2-1')+' Visualization h2 전체(pandas·Altair·Bokeh·pandas-bokeh·seaborn·plotnine·plotly·Lux·D-Tale·hvPlot). Matplotlib: '+cl('C2-3')+' h1 창 안 Plotting directly with Matplotlib, HTML1689–1721. 총11 frontend/library 대안이며 독립 렌더러11개라는 뜻은 아님.',
'C3':'CPython3.11 한 대안: '+cl('C3-3')+' 또는 '+cl('C3-4')+' Exception groups + '+cl('C3-5')+' except*. 다른 증거 조합을 다른 구현으로 중복 산입하지 않음.',
'C4':'확인된 완전 대안0, 예정 CPython 대안1은 **미확인**. '+cl('C4-2')+' + '+cl('C4-5')+'로 A1을 조합할 수 있으나 '+cl('C4-3')+'은 A2 전체 호출 절차를 직접 주지 않음.'}
near={
'P1':'일반 task list 출력만으로 사용자가 정한 checkbox 문자를 입증하지 못함. 원풀 내부 오답 판정은 **미확인**.',
'P2':link('writer 수정28e01fa','https://github.com/jgm/pandoc/commit/28e01fac74c88a777dc69c693f1296e46e1d738c')+'는 입력의 tagmcbegin/alt 보존을 입증하지 못함(풀 밖 진단).',
'P3':'pagedjs-cli 등 다른 추가 엔진의 지원을 Vivliostyle/PDFReactor/Antenna House 각각의 지원으로 확대하면 안 됨(풀 밖 진단).',
'P4':'DocBook·JATS·native XML 및 일반 custom writer는 DITA writer 구현과 같지 않음(풀 밖 진단).',
'V1':cl('V1-1')+'의 view config와 title/subtitle config 혼동. 원판 조건 부족.',
'V2':cl('V2-4')+'의 identity 타입과 일반 reflectY를 graticule/label 결합 성공으로 읽는 경우.',
'V3':cl('V3-1')+'의 Text mark를 word-cloud 배치 구현으로 읽는 경우.',
'V4':cl('V4-3')+'의 Aggregate를 Tree transform으로 읽는 경우.',
'C1':cl('C1-6')+'는 HTTP200이어도 client-instances fragment 없음. '+cl('C1-3')+' routing은 strict send 호출 직접증거가 조건부.',
'C2':cl('C2-4')+' Altair 첫 창 및 '+cl('C2-6')+' Bokeh 첫 창은 Python 이름 조건만 확인. 표 입력 조건 부족. ggplot2는 R.',
'C3':cl('C3-6')+' ordinary except는 except* subgroup 처리와 다름. 수동 subgroup/split도 자동 전파 명세와 다름.',
'C4':cl('C4-5')+' 기본 gather는 자식 실패 때 다른 awaitable을 취소하지 않음. gather 자체 취소는 별개 조건.'}
t1=[]
for c in cases:
    cid=c['case_id'];ps=[p for p in pool if p['case_id']==cid]
    slots='; '.join(str(i+1)+'='+ (cl(p['candidate_id']) if p['url'] else ('**미확인**' if p['empty_kind']=='unobserved' else '빈칸')) for i,p in enumerate(ps))
    hashes=sorted({p['html_sha256'] for p in ps if p['html_sha256']!='미확인'})
    slots+='<br>HTML SHA256: '+(' / '.join('`'+h+'`' for h in hashes) if hashes else '**미확인**')
    req=('이름 N' if c['stratum']=='N' else '계약 K' if c['stratum']=='K' else '보강 이름' if c['stratum']=='control_restore' else '보강 계약')+': '+'; '.join(a['id']+' '+a['text'] for a in c['required_atoms'])
    n=gold[cid]['eligible_count'];den='**미확인**(풀 결측)' if n is None else str(n)+'; '+('비율 **해당 없음**' if n==0 else '완전 대안 ID 분모')
    if cid=='C4':den+='; 의도한 완전성1 **미확인**'
    if cid=='C2':den+='; IPyvega/qtpandas는 원풀 Python 조건 **미확인**'
    if cid=='V3':den+='; 원규칙 대체분모 **미확인**'
    t1.append([c['layer']+'·'+cid+'·'+link('원요구',c['original_url']),req,slots,complete[cid],near[cid],den])

def short_ids(xs):return ', '.join(xs or []) or '0'
def witness_text(v):
    if not v['input_pool_observed']:return '**미확인**; 미관측 풀의 빈 fixture에서는 경로를 발명하지 않음.'
    n=len(v['reachable_original_pool_ids']);top='원풀 ID별 완결 경로 '+str(n)+'; 확인된 한 시행 최대 '+str(v['max_complete_original_pool_ids_in_one_trial'])
    if n:
        ids=list(v['witnesses'])
        if v['case_id']=='C2':ids=['C2-matplotlib']
        for a in ids:
            tid=v['witnesses'][a];r=bytrial[tid];acts=json.loads(r['actions']);path=' → '.join(link(s.get('action','open'),s['url']) if s.get('url') else '형제 목록' for s in acts)
            top+='<br>'+a+': '+tid+' ('+r['actual_cost']+'동작) '+path
    else:top+='<br>완전 경로0; 부분·실패 경로는 clicks.csv의 해당 요구 행.'
    if v['case_id']=='C2':
        trials=[r for r in clicks if v['case_id']+'-'+v['method'] in json.loads(r['applicable_views'])]
        best=max(trials,key=lambda r:len(json.loads(r['confirmed_original_pool_ids'])))
        acts=json.loads(best['actions']);path=' → '.join(link(s.get('action','open'),s['url']) if s.get('url') else '형제 목록' for s in acts)
        top+='<br>한 시행 원풀11: '+best['trial_id']+' ('+best['actual_cost']+'동작) '+path
    if v['additional_ids_outside_denominator']:
        top+='<br>분모 밖 추가확인: '+short_ids(v['additional_ids_outside_denominator'])+' (실제 공통 경로2시행, A/B/C별6회 복제 아님; 각 시행당 추가1)'
        for alt in v['additional_ids_outside_denominator']:
            tid=v['witnesses'][alt];r=bytrial[tid];acts=json.loads(r['actions'])
            top+='<br>'+tid+': '+' → '.join(link(s.get('action','open'),s['url']) if s.get('url') else '형제 목록' for s in acts)
    return top
t2=[]
for v in views:
    cid=v['case_id'];m=v['method'];ids=v['representatives'];rep=' / '.join(cl(i) if i else '빈칸' for i in ids)
    if not v['input_pool_observed']:rep='**미확인** / **미확인** / **미확인** (결측 fixture)'
    hidden=', '.join(v['hidden_members']) or ('**미확인**' if not v['input_pool_observed'] else '없음')
    if not v['input_pool_observed']:direct='완전·부분 모두 **미확인**'
    else:
        direct='완전 '+str(len(v['direct_complete_ids']))+': '+short_ids(v['direct_complete_ids'])
        if cid.startswith('V'):direct+='; '+('identity/reflectY 하위사실, 복합 atom 전체0' if cid=='V2' else '요구 전체의 입증 atom0')
        if cid=='C3':direct+='; '+('A1 constructor·3.11, A2 개요 일부' if m!='B' else '3.11·subgroup 개요 일부')
        if cid=='C4':direct+='; '+('TaskGroup 정책 하위조건 + awaitable 선언' if m!='B' else '도입·종료 대기 개요')
        if cid=='C2' and m=='B':direct+='; 새 Altair/Bokeh 카드가 이미 첫 문서에 있던 대안을 반복'
    effect='**미확인**' if not v['input_pool_observed'] else '직링크 미제공 ID: '+short_ids(v['missing_direct_ids'])+'; 두 클릭 미확인 ID: '+short_ids(v['missing_two_click_ids'])
    if cid=='C1' and m=='B':effect+='; A 대비 Requests1 되살림. HTTPX와 Requests의 다른 시행을 한 사용자 응답으로 합산하지 않음.'
    if cid=='C2' and m=='B':effect+='; Matplotlib 직링크 근거가 가려지나 원 생태계→chart href로 도달 가능.'
    if cid=='C3' and m=='B':effect+='; constructor와 except* 보완 조합이 기본 두 클릭에서 함께 안 읽힘.'
    n=v['eligible_count'];den='**미확인**' if n is None else str(n)+('; 비율 **해당 없음**' if n==0 else '')
    den+='; 본계획 관측 '+str(v['observed_trials'])+'/'+str(v['planned_trials'])+' 경로'
    if v['separate_browser_witnesses']:den+='; 별도 browser '+str(v['separate_browser_witnesses'])+'회'
    if v['shared_revalidated_witnesses']:den+='; 공통 독립 재검증 '+str(v['shared_revalidated_witnesses'])+'회'
    den+='; 사람 반응 **미확인**'
    t2.append([v['layer']+'·'+cid+'·'+m,rep,hidden,direct,witness_text(v),effect,den])

text='# AF-RES-044 · 세 자리 목록에서 사라지는 대안\n\n'
text+=table(['층·요구 ID·원요구 URL','이름·계약·필수조건','원풀 6자리·해시','완전 대안·필요한 URL과 절','근접 오답과 빠진 조건','적격 분모·미확인'],t1)+'\n\n'
text+=table(['층·요구·방식','첫 세 대표 URL','숨은 멤버','직링크로 제공된 완전·부분 근거','한 시행 두 클릭으로 확인된 경로·근거 URL','가려진 조건·되살아난 대안','원풀 분모·미확인'],t2)+'\n\n'
text+='## 필수 표 판독과 요구별 짝 차이\n\n'
text+='표1은 원풀의 의미 적격 분모이고, 표2 직링크 열은 세 대표가 제공하는 근거 inventory이다. 세 대표를 모두 읽었다는 두 클릭 사용자 시행이 아니다. 표2의 ID별 도달 수는 **각 ID마다 한 시행 안에서 완결되는 경로가 존재하는 수**이며, 관측된 한 시행에서 동시에 완결된 최대 수를 따로 썼다. 예를 들어 C1-B의1은 성공한 관측의 최대이며, 정상 브라우저에서 두 대표를 읽는 것이 불가능하다는 상한 주장이 아니다. 다른 시행의 부분 atom이나 서로 다른 구현의 조건을 합치지 않았다. 표1은 RESULT.md5–16행, 표2는20–55행에 있다. 각 링크 라벨의 요구/후보 ID는 분석 표용이며, 실제 카드 fixture의 비빈 라벨은 모두 `원문 보기`5자, 설명0자이다.\n\n'
pairs=[]
for cid in bycase:
    vs={r['method']:r for r in views if r['case_id']==cid}
    def cell(m,k):return '**미확인**' if vs[m][k] is None else str(len(vs[m][k]))
    pairs.append([cid,bycase[cid]['stratum'],str(gold[cid]['eligible_count']) if gold[cid]['eligible_count'] is not None else '**미확인**',' / '.join(cell(m,'direct_complete_ids') for m in 'ABC'),' / '.join(cell(m,'reachable_original_pool_ids') for m in 'ABC'),'자연 원풀 결측' if cid.startswith('P') else '보강 해법노출 표본' if cid.startswith('C') else ('V3 규칙 이탈 유지' if cid=='V3' else '관측 풀의 완전 근거 부재')])
text+=table(['요구','층','원풀 적격','직링크 A/B/C','두 클릭 ID별 A/B/C','해석 제한'],pairs)+'\n\n'
text+='### 층별 집계와 원문 반복 칸\n\n'
text+=table(['층','요구·관측 풀','원풀 적격 분모','직링크 A/B/C','두 클릭 원풀 ID A/B/C','조건부 회수·미확인'],[
['자연 이름 N','4요구; 관측2/4, 원규칙까지 통과1/4','관측2풀에서0; P3/P4 미확인','관측풀0/0/0','관측풀0/0/0','관측분모0: **해당 없음**. 전체 이름층: **미확인**. V3 원규칙 풀 별도 미확인.'],
['자연 계약 K','4요구; 관측2/4, 원규칙까지 통과2/4','관측2풀에서0; P1/P2 미확인','관측풀0/0/0','관측풀0/0/0','관측분모0: **해당 없음**. 전체 계약층: **미확인**.'],
['보강 이름 C1/C2','2요구; 관측2/2','13','12/12/12','12/13/12','A12/13, B13/13, C12/13. C2 외부2개는 원풀 분자·분모 제외.'],
['보강 계약 C3/C4','2요구; 관측2/2','확인1; C4 의도한 양성1 미확인','0/0/0','1/0/1','A1/1, B0/1, C1/1. C4 분모0은 **해당 없음**이며 양성 미충족.'],
['보강 전체','4요구; 관측4/4','확인14','12/12/12','13/13/13','각13/14. 해법 선정·C2의11개 비중 때문에 자연 성공률로 일반화 불가.']])+'\n\n'
repeat_rows=[]
for m in 'ABC':
    vs=[v for v in views if v['method']==m and v['input_pool_observed']]
    repeat_rows.append([m,str(sum(bool(u) for v in vs for u in v['representative_urls'])),str(sum(v['duplicate_original_document_card_slots'] for v in vs)),'요구별 첫 화면 안에서 fragment를 접은 동일 원문이 차지한 추가 칸; 요구 간 반복은 합치지 않음. P의 효과는 미확인.'])
text+=table(['방식','관측풀 비빈 대표칸','같은 원문 재표시 추가칸','계산 단위'],repeat_rows)+'\n\n'
text+='**세 자리의 중복 제거는 대안을 살리기도 하고 필수 근거를 가리기도 했다. 그러나 자연8건의 일반적 회수 효과를 추정할 수는 없었다.** 자연 표본의 Pandoc4풀은 원 HTML 획득 결측이고, Vega-Lite4풀에서는 완전 경로를 확인하지 못했다. 이 둘을 합쳐 “0/8 정답” 또는 “손실 없음”이라고 쓰지 않는다. 보강 C1에서 B는 HTTPX 문서 중복 뒤의 Requests를 첫 화면으로 올렸다. C2에서는 같은 B가 pandas chart 문서를 가려 Matplotlib의 직접 근거를 줄였으나 첫 생태계 문서의 실제 href로 두 클릭 안에 회복했다. C3에서는 B가 보완 근거 조합을 기본 두 클릭 밖으로 밀었다. 이는 같은 프로젝트라는 관계와 같은 요구를 완결한다는 관계가 다르다는 관측이다.\n\n'
text+='보강의 확인된 원풀 대안 ID 합계는14다(C1 2+C2 11+C3 1+C4 0). 직접 제공은 A/B/C가 각각12/14로 같아도 C1의 Requests 이득과 C2의 Matplotlib 손실이 상쇄된 값이다. 요구별 짝 차이를 먼저 읽어야 한다. C2가 분모의11개를 차지하며, 보강은 해법을 보고 선정했으므로 이 합계는 탐색기 품질·자연 성공률·사용자 채택률의 추정치가 아니다. C4의 미확인 양성을 성공 표본으로 고쳐 넣지 않았다.\n\n'
text+='## Q1 · 이름과 계약의 선행 구별\n\n'
text+='두 공개 원장은 `jgm/pandoc`, `vega/vega-lite`다.2020-01-01부터2025-12-31까지 `support in:body`를 생성일 오름차순으로 검색하고 각 최초40노출을 보존했다. 원장마다 최초 적격 N2/K2를 골랐으며 예비 matplotlib는 쓰지 않았다. N은 일반 기능의 지원 도구를 이름과 실제 지원 문장으로 답할 수 있는 경우, K는 원판·구체 보존·정확한 호출·오류 조건을 필수로 하는 경우다. DITA 같은 형식명이 있다는 사실만으로 모든 문법/직렬화 계약까지 임의 추가하지 않았고, 방향과 지원 기능은 N에도 필수로 남겼다. 분류가 애매한 P4는 요구 해석 한계에 포함했다.\n\n'
text+='처음 게시자가 작성한 현행 API body를 읽었지만, 그것이 게시 당시 편집 전 문장과 같은지는 미확인이다. 선정 전 댓글을 읽지 않았다는 뜻과 결말 정보에 전혀 노출되지 않았다는 뜻도 다르다. 최초 본문 속 실패·관련 링크, 후속 댓글의 실제 열람 시각은 frame과 comment receipts에 나누어 남겼다. V3와 V4가 같은 umbrella issue에 연결되어도 원 기능은 word cloud와 tree layout으로 다르다. 독립 사용 사건으로 유지하되 공통 유지보수 결정의 상관을 한계로 둔다. 근거: [frame.csv](frame.csv), [requirements.csv](requirements.csv), [P 해석 기록](evidence/pandoc/requirement-interpretation-note.json), [V 원요구](evidence/vega/requirements-V.json).\n\n'
text+='## Q2 · 후보 수집의 결손과 표시 손실\n\n'
docs=len({urldefrag(r['url'])[0] for r in pool if r['url']});urls=len({r['url'] for r in pool if r['url']})
text+=f'분모를 분리하면 자연48슬롯+보강24슬롯=72슬롯, 비빈41슬롯, 고유 exact URL{urls}개, fragment를 접은 독립 후보 문서{docs}개,12요구×3방식×3칸=108반환칸이다. 반환 비빈55칸(A22/B11/C22)과 후보41슬롯은 다른 단위다. Pandoc24슬롯은 미관측이고 Vega7슬롯은 실제 범주 소진이다. 같은 빈 문자열을 저장했어도 `empty_kind`가 다르다.\n\n'
text+='P 공식 매뉴얼의 shell 접근은403이었고 공식 게시 HTML fallback도 확보하지 못했다. 후기 cloud browser는 문서를 열었으나 렌더링 DOM200011자와 DOM SHA만 얻었다. 스크립트가 만든 anchor일 수 있는 DOM을 원 응답 HTML 바이트로 바꾸어 부르지 않았고, 원풀24칸을 성공 예시로 사후 채우지 않았다. 이 후기 진단은 `evidence/browser-observations.json`에 있다. 또 V3의 `text`는 최초 요청의 명사에서 나온 토큰이 아니었다. 후보 본문 전에 봉인했어도 SCOPE의 토큰 규칙 이탈이므로 원규칙 V3 결과는 미확인이다. 관측된 V3 수치는 그대로 보존하고 규칙 준수 분석에서는 제외해야 한다.\n\n'
text+='Python 현재 `/3/` 링크를3.11로 고치거나, C1의 존재하지 않는 `#client-instances`를 비슷한 절로 옮기거나, CPython 이슈의 잘못 도착한 숫자 링크를 의도했을 PR로 바꾸지 않았다. source index에서 만든 `#L` anchor나 인위적 후보 순서는 본 비교에 없다. 같은 source body에서 실제 href와 순서를 재구성하는 근거는 pool.csv의 raw_href·html_url·dom_index·hash와 각 freeze 파일이다.\n\n'
text+='## Q3–Q4 · 양성 대조, 반례, 동일 대상의 범위\n\n'
text+='C1은 실제 복원 양성이다. 공식 HTTPX 비교 문서의 앞3 자연 링크는 같은 HTTPX 상류이고 네 번째는 Requests다. B의 새 대표 Requests는 공식 Prepared Requests 절에서 Python Request 구성과 Session.send를 직접 입증한다. raw HTTP 실패와 별도 새 브라우저 성공은 서로 덮어쓰지 않았다. C1-3 Mounting transports는 Client 구성·routing만으로 strict “구성하고 전송”을 완전 입증하는지 내부 의견이 갈렸고, A2를 조건부로 낮췄다. 다른 HTTPX 후보가 따로 완전하므로 전체 분모2는 변하지 않았다. [비교 원문](https://www.python-httpx.org/compatibility/), [Requests 정확한 절](https://requests.readthedocs.io/en/stable/user/advanced/#prepared-requests).\n\n'
text+='C2는 반복된 프로젝트 링크 뒤에 별개 라이브러리의 자연 링크가 있지만, 그 별개 대안 열 개는 이미 첫 생태계 문서가 입증한다. B가 Altair/Bokeh 카드를 꺼냈다고 그 대안을 새로 발견했다고 세면 중복 성과다. 엄격 h1 창을 끝까지 다시 읽자 pandas chart 문서의 후반부에서 직접 Matplotlib에 Series/DataFrame을 넘기는 근거가 나왔다. 이 때문에 초기10 대안 판단을11로 정정했고 원 판단을 보존했다. B가 가린 것은 그11번째 직접 근거다. 첫 생태계→chart 링크의 두 클릭은 이를 복구한다. IPyvega/qtpandas는 이름은 원풀에 있었지만 Python 조건이 빠졌으며, 각각 다른 공식 저장소를 추가로 읽은 시행이 이를 채운다. 두 fresh response를 그 시행에서 즉시 읽어 기존 동적 HTML 해시 불일치를 보완했으며, 이전 실패를 지우지 않았다. 동일 출발카드를 공유하는 A/B/C에 적용 가능한 실제2시행을6회로 복제하지 않았다. 각 시행은 기존10개와 추가1개만 완결하며, 두 추가 대안과 Matplotlib를 한 시행에서 모두 읽은 것으로 합치지 않았다. 둘은 원풀 적격11의 회수 분자에 넣지 않는다. [생태계](https://pandas.pydata.org/pandas-docs/version/2.0/ecosystem.html#visualization), [같은 h1 창](https://pandas.pydata.org/pandas-docs/version/2.0/user_guide/visualization.html#visualization).\n\n'
text+='C3는 “항상 보완 문서 두 개가 필요하다”는 초기 직관의 반례도 준다. constructor와 except* 문서 조합 외에, PEP 첫800 단어 목차의 실제 Specification 링크를 두 번째로 열면 같은 원문이 두 역할을 제공한다. 첫 클릭의 Python-Version3.11과 둘째 절의 constructor·부분 매칭·미처리 전파를 한 시행에서 결합했다. B는 첫 release 소개만 남겨 기본 두 클릭에서 그 전체 조합을 갖추지 못했다. [PEP 입구](https://peps.python.org/pep-0654/), [Specification](https://peps.python.org/pep-0654/#specification), [except*](https://docs.python.org/3.11/reference/compound_stmts.html#except-star).\n\n'
text+='C4는 예정 양성이 실패한 사례로 남겼다. frozen A1에는 TaskGroup 정책과 gather 구별이 함께 있고, A2는 두 await와 예외 전달 절차를 요구한다. Data model 도착절은 awaitable 반환과 동기 프로토콜의 유사성을 설명하나, 완전 의사 코드는 별도의 compound statements에 있다. C4-3→async-with로 A2를 확인한 두 클릭에 다른 시행의 TaskGroup 근거를 더하지 않았다. TaskGroup 대안 자체가 불가능하다는 뜻이 아니라 봉인된 풀·범위에서 양성 완결성을 못 입증했다는 뜻이다. 완전 경로가 있는 보강은3/4이고, 새로운 별개 대안의 복원을 실제로 보여 준 보강은 목표2개 중 C1 하나다. [TaskGroup](https://docs.python.org/3.11/library/asyncio-task.html#asyncio.TaskGroup), [async context managers](https://docs.python.org/3.11/reference/datamodel.html#async-context-managers), [실제 async-with 절](https://docs.python.org/3.11/reference/compound_stmts.html#async-with).\n\n'
text+='같은 상류의 다른 호출은 TaskGroup과 gather, 다른 URL의 같은 기능 반복은 HTTPX, 한 문서의 복수 역할은 PEP654와 pandas ecosystem에서 관측했다. 방향을 뒤집는 추론의 반례는 Pandoc LaTeX writer 수정이 LaTeX reader의 alt 입력을 보장하지 않는 경우다. [Vega-Lite Overview](https://vega.github.io/vega-lite/docs/)가 명시한 컴파일 방향은 Vega-Lite→Vega이며, [Vega wordcloud](https://vega.github.io/vega/docs/transforms/wordcloud/)의 지원을 같은 이름의 Vega-Lite 호출 계약으로 역전할 근거는 아니다. 이는 선언된 방향과 역방향 보장 부재의 대조이며 모든 프로그램의 한 방향 대체 가능성을 실행으로 증명한 것은 아니다. 추가 D-RNG 진단에서는 NumPy 공식 정책이 같은 seed만으로 stream을 보장하지 않으며 scalar 호출5회와 size5 한 호출도 같은 stream을 보장하지 않는다고 명시한다. 같은 프로젝트·부품·용도·판·문서 역할의 키만으로 호출 순서·입자 크기의 계약을 모두 대신할 수 없다는 저자 진술이다. 이 진단을12요구에 추가하지 않았다. [방향별 수정](https://github.com/jgm/pandoc/commit/28e01fac74c88a777dc69c693f1296e46e1d738c), [NumPy 정책65–81행](https://numpy.org/doc/stable/reference/random/compatibility.html).\n\n'
text+='## Q5–Q6 · 실제 도착, 조건부 분모, 민감도\n\n'
text+=f'원장에는 통제된 HTTP/DOM 독립 시행{data["http_trials_observed"]}/{data["http_trials_planned"]}개와 Requests 새 브라우저1회, C2 동일 출발카드의 독립 재검증2회가 있다. 총 고유 시행은{data["total_unique_observed_trials"]}회이며 공통 경로를 방식별로 중복 산입하지 않는다. 매 시행은 빈 CookieJar와 새 opener로 시작한다. 같은 문서 fragment 전이는 그 시행의 이미 열린 DOM 안에서 이동하며, 형제 목록만 열면 원문 근거0이다. 실제 source href 존재, 원 응답 SHA, 최종 source 주소에서의 resolve, destination fragment를 구분했다. 원문0인 형제 목록 동작을 HTTP 접속 성공 횟수로 세지 않는다. 이 계측은 실제 사람의 클릭·선택·채택을 관측한 것이 아니다.\n\n'
text+='원풀 적격이 있는 C1–C3만 해당 ID를 조건부 분모에 넣는다. V의 확인된0과 C4의 확인된0은 비율을 **해당 없음**, P의 분모 결측은 **미확인**으로 둔다. 더 넓은 생태계에 답이 없다는 주장도 하지 않는다. C2-1의 설명을 다른 Bokeh/Altair first800 시행에 공짜로 붙이거나, C3의 별도 두 시행 A1/A2를 합쳐 완전으로 만들지 않았다. raw SHA가 달라 엄격한 출발 창을 재확인하지 못한 경우에는 두 번째 페이지가 열려도 봉인된 경로 증명에서 제외한다. 전송 실패와 의미상 적격의 차이는 clicks.csv의 접속·snapshot 일치·semantic_complete_ids·confirmed_complete_ids 열에 남겼다.\n\n'
text+='C의 raw frozen metadata에서 판 미확인24행은 처음부터 singleton이었다. 내부 감사로 출처 위치가 부족한 migration 역할·httpx.get 부품·test 역할 세 필드를 미확인으로 낮췄고, C4-6도 singleton으로 명시했다. v1 keys와 새 keys를 보존했으며36개 표시와 원멤버는 전혀 바뀌지 않았다. 관측한8풀에서는 결국 C와 A의 분할이 같다. P4풀의 빈 fixture 일치는 실제 효과0의 증거가 아니다.\n\n'
sens=[]
for cid in ['C1','C2','C3','C4']:
    for m in 'ABC':
        v=next(v for v in views if v['case_id']==cid and v['method']==m)
        if v['direct_complete_ids']!=v['W_direct_complete_ids'] or v['reachable_original_pool_ids']!=v['W_reachable_original_pool_ids']:
            sens.append([cid,m,str(len(v['direct_complete_ids']))+'→'+str(len(v['W_direct_complete_ids'])),str(len(v['reachable_original_pool_ids']))+'→'+str(len(v['W_reachable_original_pool_ids'])),'같은 도착 원문에서 추가로 확인한 절만 허용; keys·카드·strict 전이·비용 불변'])
text+=table(['변경 요구','방식','직링크 strict→W','두 클릭 strict→W','바꾼 한 요소'],sens or [['**미확인**','실행 진행','**미확인**','**미확인**','완료후 생성']])+'\n\n'
text+='U는 미확인 필드를 함께 두어도 나머지 알려진 키가 맞아야 병합한다. 관측8풀에서는 실제 합침0·변화0이고, P4풀은 미확인이다. W는 strict 사실을 유지하고 같은 열린 원문에서 확인한 추가 절만 합친다. 전이 그래프까지 새 링크로 넓힌 다른 실험은 아니다. C3의 B 결론이 달라지는 직접 반례는 release→PEP를 두 클릭으로 연 뒤 PEP 전체를 읽게 하는 것이다. 존재하지 않는 fragment나 실패한 도착을 W로 정상화하지 않았다.\n\n'
text+='## Q7 · 박물관·운수기관의 같은 이름과 다른 단위\n\n'
text+='Met의 Great Wave 레코드 JP10(36491), JP2972(56353), JP1847(45434)는 같은 작품 이름으로 연결되지만 소장품 번호·크기·취득 기록이 다르다. 이름만 찾는 사람에게 대표1개는 작품 식별의 충분한 출발점일 수 있다. 특정 인상의 크기·소장 기록을 검증하는 사람에게는 다른 레코드의 값이 대체 증거가 아니다. Met API가 objectID를 고유 식별자로 쓰며 accessionNumber는 항상 유일하지 않다고 설명하는 운영 문서까지 대조했다. 관리자는 작품 묶음과 소장 객체 ID를 함께 보존해야 다시 풀 수 있다. [JP10](https://www.metmuseum.org/art/collection/search/36491), [JP2972](https://www.metmuseum.org/art/collection/search/56353), [JP1847](https://www.metmuseum.org/art/collection/search/45434), [Met API](https://metmuseum.github.io/).\n\n'
text+='MTA A 노선은 이름만 찾을 때 공식 노선 대표가 유용하지만, 행선지와 특정 역 정차를 확인하려면 방향·branch·시각을 남겨야 한다. 실제 PDF 유효일은2025-11-02이며 검색 요약의 이전 날짜를 쓰지 않았다. p8의 평일 Inwood06:58→Far Rockaway08:33과07:05→Lefferts08:20은 같은 A 이름의 다른 운행이다. p1은 시간표가 모든 정차역을 열거하지 않는다고 명시하고, Aqueduct 공식 map은 북행 방향 조건을 더한다. 특정 역이 시간표에서 생략됐다는 사실을 무정차로 읽으면 안 된다. 한 PDF가 양방향/branches를 담고 있어 대표1개가 무조건 손실을 만든다는 주장에도 반례다. CF-T-SCOPE 진단은 p2만 허용하면 미확인, 같은 PDF p8까지 허용하면 해당 branch 구별 가능으로 바뀌었다. 이27페이지 PDF는 원문1개로 셌다. [A 시간표](https://www.mta.info/schedules/subway/a-train), [Aqueduct map](https://www.mta.info/document/1091).\n\n'
text+='박물관 이용자의 단위는 작품/물리 객체, 교통 이용자의 단위는 노선/방향별 운행, 관리자의 단위는 묶었다가 되돌릴 수 있는 record다. 프로젝트만으로 묶는 B도 같은 종류의 선택이다. 이름층에서는 대표 문서가 여러 구성원을 실제로 설명할 수 있고, 특정 구성품·입출력 방향·정차 조건에서는 대표가 그 사실을 담는지 별도로 확인해야 한다. 분야 사례는 사용자의 실제 행동 실험이 아니라 발행자 원문의 단위 비교다. 상세 위치와 반증은 [분야 비교](evidence/crossfield/NOTES.md)와 [comparisons.csv](evidence/crossfield/comparisons.csv)에 있다.\n\n'
text+='## 보관 대안과 적용 조건\n\n'
text+=table(['표시/보관 선택','적용할 수 있는 조건','실패 사례·대가'],[
['A URL 동일만 합침','같은 exact URL 반복을 제거하며 fragment 차이를 보존하려는 기준선','동일 원문 fragment들이 첫3자리를 반복 점유할 수 있음. C1 Requests가 뒤로 남음.'],
['B 상류 프로젝트 대표','대표 자체가 요청 기능을 입증하거나 실제 두 클릭에서 필요한 구성원을 읽을 수 있음','C3의 보완 문서 조합이 예산 밖으로 밀림. C2 첫 대표가 이미10대안을 담아 새 카드의 효용을 중복 집계할 위험.'],
['C 부품·용도·판·역할','표시시점 metadata가 독립적으로 확인되고 미확인은 개별 유지','본 관측8풀은 A와 같아 효과를 시험하지 못함. D-RNG처럼 호출 인자/순서 계약까지 키가 표현하지 못할 수 있음.'],
['원멤버·근거 역할을 보관하고 대표를 표시','URL 원순서·publisher/subject 구별·판·필수조건 지지 행렬을 보존할 때','형제 목록 열기1+원문1이면 하나만 읽으므로 두 보완 문서가 필요한 C3를 자동 구제하지 못함.'],
['같은 문서 전체 읽기 W','실제로 도착한 원문에 보완 절이 있으며 범위를 명시할 때','C3 결론을 바꿀 수 있음. 누락 fragment, 다른 문서의 미열람 명세, 판 불일치까지 해결하지는 않음.']])+'\n\n'
text+='제품용 색인 제안은 구현·부품뿐 아니라 **요구 atom→근거 절→판/방향→원멤버** 연결을 저장하고, 카드 수·원풀의 완전 대안 수·한 시행의 확인량을 따로 내보내는 것이다. 이 연구에서는 gold를 C key로 쓰지 않았다. 실제 제품이 나중에 요구별 support matrix를 써서 선택할지는 별도 실험이며, 본 결과로 검증됐다고 주장하지 않는다.\n\n'
text+='## 수용 상태와 검산 이력\n\n'
text+=f'활성 sources.jsonl은{sources["active_ledger_rows"]}관측행, 고유 산입 원문{sources["unique_counted_originals"]}개다. 이 중 경로 추가 조사 없이도 핵심 원문{sources["core_unique_originals_without_second_hop"]}개이며, 추가 Vega 경로의31개를 별도 계산했다. 같은 HTML의 fragment·반복 열람·실패는 원문 수를 늘리지 않는다. Python/C1/C2의 후속 경로 원장도 보충 관측으로 산입을 억제했다. 원요구8, 공식 비교/결정4, 공급자8 이상, 발행/호환/시험4 이상, 박물관·운수기관 각2 이상은 출처 원장에 연결된다.\n\n'
text+='수용 전체는 **미충족**이다. 자연48슬롯의 원순서 재구성은 P24 결측 때문에24/48만 확인했고, 자연 요구별 원규칙·원풀 관측의 결합 통과는3/8이다(P4 결측+V3 이탈). 보강24슬롯 순서는 확인했지만 완전 양성은3/4, 새로운 대안 복원 양성은1/2이다. 표36행·동일 입력·고정 라벨·두 동작 한도·ID별 손익 검산을 이 결손의 대체 증거로 쓰지 않는다. 내부 별도 에이전트 검토는 사람의 독립판독이 아니며, 같은 모델 계열의 자체 점검이다.\n\n'
text+='관측 뒤 정정은 숨기지 않았다: CSV CRLF→LF 해시 정정, C2 h1 전 범위 재독에 따른 Matplotlib 추가, first800 창 밖 href 제거, dt/section과 각주/댓글 범위 정정, 문서전체 요약의 fragment 과대 서술 정정, C1-3 조건부화, display metadata3필드 미확인화, W 단조성·판 대응·source SHA/resolve gate 정정을 원 버전·이유·영향과 함께 남겼다. 원풀/요구/원래 그룹 기준의 숫자는 보존했다. 고정 커밋과 실행 명령은 [COMMIT_LOG.md](COMMIT_LOG.md), [SELF_CHECK.md](SELF_CHECK.md), [acceptance-evidence.json](evidence/acceptance-evidence.json), 최종 [HANDOFF.md](HANDOFF.md)를 따른다.\n\n'
weak=[
['자연 표본의 획득 결측과 사전규칙 이탈','P1–P4 raw HTML·원순서 및 V3 토큰; [MANUAL](https://pandoc.org/MANUAL.html), [V3 원요구](https://github.com/vega/vega-lite/issues/6135); pool.csv2–25행, source-scope/input audit','같은 MANUAL 원응답 byte를 승인된 수집에서 확보해 SHA/href를 먼저 봉인. V3는 최초요구 명사만으로 새 amendment를 사전 고정; 기존 수치 유지.','새 자연 풀에 실제 완전 경로가 생기거나 원규칙 V3 fallback이 다른 근거를 포함하면 이름/계약층의 회수·손실 판단이 달라짐.'],
['보강 양성의 부족과 해법 선정 편중','C4 A2 및 C2 복원 양성의 해석; [Data model](https://docs.python.org/3.11/reference/datamodel.html#async-context-managers), [async-with](https://docs.python.org/3.11/reference/compound_stmts.html#async-with), [ecosystem](https://pandas.pydata.org/pandas-docs/version/2.0/ecosystem.html#visualization); requirements.csv C4행·gold-paths.csv','새 독립 유지보수/이관 사례의 요구·자연6순서·근접오답을 그룹 계산 전에 봉인. C4를 사후 완화해 채우지 말고 완전 경로와 첫대표에 없는 별개 대안을 실제 확인.','두 번째 복원 양성과 두 번째 보완 양성이 확보되거나, C4의 의미상 참조를 허용하는 별도 기준이 사전에 채택되면 대조 범위가 확대됨.'],
['키의 구별력과 통제 클릭의 외적 한계','C=A인 관측8풀·U무변화·Requests HTTP/브라우저 차이; [Requests](https://requests.readthedocs.io/en/stable/user/advanced/#prepared-requests), [PEP](https://peps.python.org/pep-0654/#specification), [NumPy](https://numpy.org/doc/stable/reference/random/compatibility.html); groups.jsonl·clicks.csv','표시 metadata가 실제 같은 C key로 합쳐지는 독립 풀 하나부터 봉인하고 같은3카드로 사람의 과업별 클릭/확신/채택을 별도로 관측. 첫 자료는 현재 views fixture와 원멤버/절 지도.','C가 실제 병합하면서 다른 구현을 살리거나 필수조건을 가리거나, 실제 독자가 긴 문서·형제 목록을 다르게 이용하면 표시·행동 결론이 달라짐.']]
(E/'weaknesses.json').write_text(json.dumps(weak,ensure_ascii=False,indent=2)+'\n')
text+=table(['중요한 불일치·약점','영향받는 판단과 근거 URL·행','다음 최소 조사·첫 자료','결과가 달라지는 조건'],weak)+'\n'
target=E/'RESULT_DRAFT.md' if data['provisional'] else ROOT/'RESULT.md'
target.write_text(text)
print(str(target),len(text),'characters',len(t1),len(t2),'table rows')
