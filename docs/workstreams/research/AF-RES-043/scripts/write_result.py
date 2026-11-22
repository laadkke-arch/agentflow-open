"""Render the required tables from frozen cards, observed reads, and explicit grades."""
import csv
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def jl(path):return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]
def cell(x):return str(x).replace('|','\\|').replace('\n','<br>')
def row(xs):return '| '+' | '.join(cell(x) for x in xs)+' |'
def table(headers,rows):return '\n'.join([row(headers),row(['---']*len(headers))]+[row(r) for r in rows])
def link(label,url):return f'[{label}]({url})' if str(url).startswith(('http:','https:')) else '**미확인**'
def configs(s):return s.replace('BLX','B+L+X').replace('BX','B+X').replace('BL','B+L')
def truth(x):return '일치' if x is True else '근거 미달' if x is False else '**미확인**'


def main():
    cards=jl(ROOT/'cards.jsonl');key={k['case_id']:k for k in jl(ROOT/'key.jsonl')}
    components={c['case_id']:c for c in jl(ROOT/'components.jsonl')}
    js=jl(ROOT/'evidence/scored-judgments.jsonl');by={(j['card_id'],j['task']):j for j in js}
    reads=list(csv.DictReader((ROOT/'reads.csv').open()))
    summary=json.loads((ROOT/'evidence/analysis-summary.json').read_text())
    short_purpose={
        'N-P-01':'Series.str 정규표현식 설명','N-P-02':'Series/ExtensionArray의 실제 ndarray 설명',
        'N-S-01':'월별요인 60개월 이동회귀; 시간 의도 미정','N-S-02':'다른 데이터의 Stata 회귀·영향 그림 비교',
        'T01':'최신 GDP 통계의 원 product 주소','T02':'같은날 Q2 최초추계의 추가설명',
        'J01':'원논문 코호트 인원 주장의 현재 재사용','J02':'mTERF22의 여러 유전자발현 역할'}
    bversion={'N-P-01':'Python3 family; minor/patch **미확인**','N-P-02':'NumPy 대상판 **미확인**','N-S-01':'자료판 **미확인**','N-S-02':'UCLA 대상판 **미확인**','T01':'2024-04-25 최초추계','T02':'2024-08-15 최초추계','J01':'2018 저작 DOI; 불변판 **미확인**','J02':'2018 저작 DOI; 불변판 **미확인**'}
    claim={'N-P-01':'정규표현식 연산 설명','N-P-02':'균질·고정크기 배열 정의','N-S-01':'192607 Mkt-RF=2.96','N-S-02':'당대 문구 **미확인**','T01':'2024Q1 1.6% 연율','T02':'2024Q2 0.6% 분기비','J01':'sepsis 분류3716명','J02':'여러 미토콘드리아 유전자발현'}
    cwhy={'N-P-01':'현행 기본정의','N-P-02':'현행 기본정의','N-S-01':'시간 의도 보류; B공통단서 한계','N-S-02':'관련 현행 설명/접근실패; 기준 **미확인**','T01':'최신발표를 제공하는 product 기능','T02':'지목한 같은날 발표의 상세','J01':'원3716→정정3806; 소비3806은 수정대상 아님','J02':'발현 역할과 정정의 위치주장 구분'}
    out=['# AF-RES-043 · 판 주소와 과거 인용의 개별 기여','']
    rows=[]
    for card in sorted(cards,key=lambda c:(c['case_index'],('B','BL','BX','BLX').index(c['config']))):
        k=key[card['case_id']];c=by[card['card_id'],'C'];h=by[card['card_id'],'H'];cid=card['case_id']
        routes=[]
        for task,j in [('C',c),('H',h)]:
            op=[r for r in reads if r['judgment_id']==j['judgment_id'] and r['mode']=='publisher_open']
            parts=[]
            for n,r in enumerate(op,1):
                url=r['resolved_url'] if r['resolved_url'].startswith(('http:','https:')) else r['requested_url']
                fail='실패 ' if 'fail' in r['outcome'] else ''
                parts.append(f"{fail}{link(str(n),url)} · {r['locator']}")
            routes.append(task+': '+' → '.join(parts))
        hist={'publisher_edition_match':'발행저작/판 해당절 대조','local_redisplay':'로컬 발췌 재표시만','unverified':'**미확인**','publisher_conflict':'지정판 충돌'}[h['historical_level']]
        if cid.startswith('N-') and h['historical_level']=='publisher_edition_match':hist+='(추가 재구성판; 실제 소비판 **미확인**)'
        if cid=='J02' and h['historical_level']=='publisher_edition_match':hist+='(현재 제공2018저작; S-I제외)'
        desc=configs(card['config'])+' · `'+card['card_id']+'`'
        if not k['X_available'] and 'X' in card['elements']:desc+='; X **미확인** 표시'
        if 'L' in card['elements'] and not k['L_version_pinned']:desc+='; L='+('이관위치' if cid=='N-S-02' else '직접저작·절 주소')
        agreement='C '+truth(c['supported_correct'])+' · '+link('기준',k['C_criterion_url'])+' '+k['C_criterion_locator']+'<br>H '+truth(h['supported_correct'])+' · '+link('기준',k['H_criterion_url'])+' '+k['H_criterion_locator']
        if not k['H_criterion_confirmed']:agreement+='; 재구성 도달 '+truth(h['H_reconstructed_attained'])
        hold='C '+c['hold_reason']+'; H '+h['hold_reason']
        rows.append([
            ('자연' if k['stratum']=='natural' else '정정우선')+' · '+link(cid,k['consumer_url'])+' · '+short_purpose[cid],
            desc,link('원 URL',k['original_href'])+' · '+bversion[cid],'<br>'.join(routes),
            c['action']+' · '+cwhy[cid]+' · '+truth(c['supported_correct']),
            claim[cid]+' · '+hist,agreement,
            f"발행 C{c['publisher_opens']}/H{h['publisher_opens']}; 유효X C{int(c['local_X_valid_redisplay'])}/H{int(h['local_X_valid_redisplay'])}; {hold}; 근거 `{c['judgment_id']}` / `{h['judgment_id']}`"
        ])
    out.append(table(['표집층·참조·실제 목적','B·L·X 구성','원래 URL·판','실제 연 URL·절(두 과업 구분)','현재 행동·근거','과거 문구·원판 대조 수준','기준 URL·절과 일치','열람수·보류 사유·미확인'],rows))
    out+=['','## 표 2 · 원규칙의 사례 내 짝 비교','']
    rows=[]
    for s in summary['pair_summary']:
        if s['sensitivity']!='original':continue
        st='자연' if s['stratum']=='natural' else '정정우선'
        loc='해당 없음 — 이 짝에서 판주소 단독의 추가 기여를 주장하지 않음'
        if s['task']=='H' and s['stratum']=='natural':loc='엄격 H는 **미확인**; 아래 재구성판 결과 별도'
        if s['task']=='H' and s['stratum']=='correction_first':
            if s['comparison']=='B↔BL':loc='X없이 T01·T02·J01·J02 대조. T02·J01은 B도 충분; J02는 직접HTML 접근효과 혼재'
            elif s['comparison']=='BL↔BLX':loc='왼쪽 B+L만으로4건 대조; X추가 발행대조 이득0'
            elif s['comparison']=='BX↔BLX':loc='T01·J02의 대조가 늘었으나 이 짝 자체는 X도 있음'
            else:loc='T02·J01은 B만으로도 대조'
        risk='관측된 단정 오류0; 기준 미확인 사례는 오류0으로 계산하지 않음'
        if s['task']=='C' and s['stratum']=='correction_first':risk='J01의 옛X는 현재 수치와 충돌. 실제 단정 오류0; J01/J02의 성과감소는 접근보류·순서와 함께 관측'
        attained=f"요구근거 도달 {s['left_attained']}→{s['right_attained']}/{s['criterion_confirmed_n']}" if s['criterion_confirmed_n'] else '요구근거 도달 비율 **해당 없음**'
        ev='; '.join('`'+x+'`' for x in s['pair_ids'])+'; '+attained
        rows.append([st+' · '+s['task']+' · '+configs(s['comparison']),f"전체{s['original_slots']} / 기준{s['criterion_confirmed_n']} / 쌍방판정{s['both_resolvable_n']}",f"{s['both_correct']} · {s['left_only']} · {s['right_only']} · {s['both_incorrect']}",f"보류/대조미확인{s['hold_or_unverified']} · 기준미확인{s['criterion_unknown']}",loc,risk,ev])
    out.append(table(['표집층·과업·비교하는 두 구성','전체·기준 확인 분모','둘 다 맞음·왼쪽만·오른쪽만·둘 다 틀림','보류·기준 미확인','판 주소만으로 충분한 사례','발췌가 판단을 그르친 사례','근거 ID'],rows))
    out+=['',"표1은32행이며 C/H 원관측64행은 [judgments.csv](judgments.csv), 실제 동작109행은 [reads.csv](reads.csv)에 있다. 표2의 네 정오 칸은 양쪽을 판정할 수 있을 때만 채운다. 접근보류·로컬재표시만 있는 쌍은 별도 칸이다. 따라서 한쪽만 맞음0을 ‘근거 도달의 증감0’으로 읽으면 안 된다. 오른쪽 근거ID 칸과 아래 표는 기준 있는 모든 쌍에서 요구근거를 얻었는지도 따로 보여 준다. 규범적 보류는 맞는 행동으로 포함한다.",'',
    '## 판단과 수용 상태','',
    '**L은 특정한 과거판의 절에 도달하도록 돕는 경우가 있었고, X는 저장한 말을 다시 보여 주는 데 충분했다. 두 성과는 서로 대체되지 않았다.** 현재 용도는 소비자의 시간 목적과 후속 정정의 해당 범위를 함께 봐야 했다. 이번 판독에서 X를 더해 잘못된 주장을 확언한 사건은 관측하지 못했다. 다만 J01의 옛 환자수는 과거 원문과 정확히 일치하면서 현재 재사용에는 정정이 필요한 실제 반례다. 이 결론은 아래의 관측 및 한계에 한정한다.',
    '',
    '8슬롯·32카드·64판독·64짝을 기록하고 계산했다. 직접 읽은 고유 발행자 1차 문서의 보수적 하한은 **28개**다. 그러나 요구한 분류별 최소는 **소비자7/8 + 대상8/8 + 별도 공지4/4 + 규칙4/4 =23/24**다. BMJ 소비 원문은 발행자에서 열리지 않아 PMC 전문으로 목적을 확인했으며, 미러 제외 규칙에 따라 최소수에 넣지 않았다. 다른 다섯 보조 원문을 소비자 부족분으로 대체하지 않았다. [28개 원문별 목록·위치](evidence/source-count-audit.json), [전체 출처 원장](sources.jsonl).',
    '',
    '**완전 표본 수용은 미충족이다.** UCLA의 당대판·X 부재, 자연층 실제 소비 대상판 미확인, 표집 추적 누락, N-S-01 카드의 연구자 해설 단서, literal href 추적 미완성이 남는다. 보고서와 원장은 이 실패를 포함한 검토 가능한 연구 결과다. [조건별 수용 기록](evidence/acceptance-evidence.json), [감사와 정정 이력](evidence/amendments.md).',
    '',
    '## Q1–Q2 · 먼저 관측된 소비 목적과 날짜','']
    rows=[]
    for cid,k in key.items():
        actual_l_url=re.search(r'https?://\S+',components[cid]['L']).group(0)
        old_version='**미확인**' if k['old_version']=='미확인' else k['old_version']
        expected='**미확인**' if k['C_expected']=='미확인' else k['C_expected']
        rows.append([link(cid,k['consumer_url'])+' · '+k['consumer_locator'],k['consumer_date'],k['purpose'],old_version+' · '+link('추가 L',actual_l_url),expected+' / '+('확인' if k['H_criterion_confirmed'] else '**미확인**')])
    out.append(table(['소비 문서·정확한 위치','소비 발행/갱신 시점','소비 목적','추가판·관계','C 기준 / 실제 소비판 H기준'],rows))
    out+=['',
    '자연층은 pandas1.5.3 user guide와 statsmodels0.14.0 examples의 본문 목차 첫25개에서 각2개를 선택했다. [frame.csv](frame.csv)는 두 원장50행과 통계25노출, 학술31원노출을 함께 보존한다. 학술은 동일저작 미러 중복을 빼면 첫25고유결과가 원노출26에서 끝난다. 뒤의 더 잘 열리는 사례로 바꾸지 않았다. 통계 첫 네 검색을 묶어 보낸 결과10개의 query별 순위와 J02 소비 검색의 일부 상세목록은 복원하지 못했다. 해당 원검색/탈락 기록은 collection/statistics 및 collection/journals에 남겼다. 사전규칙의 정확한 순서 준수는 **미확인**이며 완전 준수 수용은 하지 않는다.',
    '',
    'pandas의 2023-01-18은 소프트웨어 릴리스 날짜다. 외부 Python/NumPy 링크가 처음 삽입된 날짜나 실제 사용한 patch를 뜻하지 않는다. statsmodels 문서의 2023-05-05 갱신표시도 외부 자료 다운로드 시점과 동일하지 않다. 추가 Python3.11.1은2022-12-06 릴리스, NumPy1.24.0은2022-12-18 릴리스이며, 이 사실과 정확한 URL이 그때 존재했다는 증거를 분리했다. [Python 릴리스](https://www.python.org/downloads/release/python-3111/) 제목·날짜와 Online Documentation 링크, [NumPy 릴리스](https://numpy.org/doc/1.24/release/1.24.0-notes.html) 도입부; NAT-PY-RELEASE/NAT-NP-RELEASE.',
    '',
    '통계는 발표일·기준분기·개정일을 분리했다. T01 소비 분석은2024-04-25의2024Q1 최초추계를 사용하면서 최신 통계에는 product page를 지시한다([SCB May2024](https://apps.bea.gov/scb/issues/2024/05-may/0524-gdp-economy.htm) L25–31). 따라서 C는 최신 허브 유지, H는 Apr25의1.6% 확인이다. T02는2024-08-15 월간문서가 같은날 Q2 최초추계의 상세를 가리킨다([ONS 월간](https://www.ons.gov.uk/economy/grossdomesticproductgdp/bulletins/gdpmonthlyestimateuk/june2024) §2 L96–97). C도 이 특정판 참조를 유지한다. 두 목적을 최신값 대 과거값의 하나의 정답으로 합치지 않았다.',
    '',
    '학술은 원 논문 발행일(J01 2018-09-26; J02 2018-07-30), 소비 문서 발행일(2021-02-18;2021-02-02), 정정일(2024-03-21;2019-03-25)을 나눴다. J01 소비자가 이미3806명을 분석한 사실과 원논문의3716을 지금 재사용할지의 질문은 다르다. J02 소비 목적은 mTERF22의 유전자발현 역할이며 배타적 세포내 위치를 확언하는 과업으로 넓히지 않았다. [PMC 소비 본문](https://pmc.ncbi.nlm.nih.gov/articles/PMC7896572/) Methods·Results L254–280,298–299 및 ref16 L480; [MDPI 소비 본문](https://www.mdpi.com/1422-0067/22/3/1466) Introduction L181, ref26 L318.',
    '',
    '## Q3–Q4 · 카드가 실제로 제공한 정보와 허용 열람','',
    'B·L·X의 동일 문자열과 B→L→X 순서는 [components.jsonl](components.jsonl),32개 본문·해시·순서는 [cards.jsonl](cards.jsonl)에 봉인했다. 채점키는 [key.jsonl](key.jsonl)에 분리했다. X는 짧은 핵심 발췌이고 URL·판 단서가 확인된 X는0/7이다. French의192607은 관측 기준월이며 자료 발행판 단서로 세지 않았다. UCLA에는 원판 발췌를 만들지 않고 **미확인** 표시를 넣었다.',
    '',
    'L의 정보 증분은 균일하지 않다. Python은 정확한 release 경로, NumPy는1.24 계열 경로, French는2022년 자료 cut, BEA/ONS는 날짜 있는 발표다. J01/J02는 B의 DOI가 이미 저작을 식별하고 L은 직접 발행자 HTML과 절을 더한다. 이 두 L을 불변판 전용 URL이라고 부르지 않는다. UCLA L은 이관된 현행 위치다. 즉 판/발표 주소로 분류한 L은5/8, 직접 저작 locator2/8, 이관 locator1/8이며, X가 실제 있는 사례는7/8이다. 정확한 L URL의 소비 당시 존재나 과거 HTTP 응답은 **미확인**이다.',
    '',
    '현재·과거 과업마다 처음 보이는 URL에서 시작했고, 두 번째 이동은 첫 문서의 실제 href/링크ID로 제한했다. 55판독은1회,9판독은2회의 발행요청을 했다. 총73요청 중12실패를 포함한다. 같은문서 내 찾기4회와 로컬 X동작32회는 별도다. 그중 UCLA의 네 동작은 미확인 표시에 대한 표시였으므로 유효 발췌는28회(C14/H14)다. 네트워크 왕복·사람 시간·전송비를 측정한 수치는 아니다. [원관측 봉인](evidence/read-seal.json), [실행 규칙](READER_PROTOCOL.md).',
    '',
    '세 판독자는 새 문맥에서 배정 카드만 읽고 키 비노출을 기록했다. 주 작성자는 출처와 키를 이미 보았고 후속 채점도 비가림이다. 같은 사례 안에서는 앞 카드 노출을 지울 수 없었으며 공개 교차순서도 완전 균형/무작위 순서가 아니다. 특히 N-S-01 B의 시간 의도 부재 해석은 수집자의 설명이므로 보류 답 단서가 될 수 있다. 가림과 중립성을 혼동하지 않는다. [정적 감사](evidence/acceptance-audit-notes.md), [산술·근거 자체 감사](evidence/analysis-audit.md).',
    '',
    '둘째 요청9건의 실제 부모·링크 연결은 모두 남았으나 원HTML href 철자를 보존한 것은2/9다. 나머지7건은 **미확인**으로 유지했다. ③의 단순 검사1건을④의 접두사 검사7건으로 정정한 이력은 amendments.md에 있다. 일부 PLOS 응답의 summary-labeled 렌더링도 원문 바이트/철자의 완전 보존으로 과장하지 않는다. 주작성자의 별도 공개HTTP 본문 점검은 카드 예산과 성과에 더하지 않았다.',
    '',
    '## Q5 · 어느 요소가 어느 과업에 충분했는가','']
    cfg_rows=[]
    for st in ('natural','correction_first'):
        for task in ('C','H'):
            arr=[r for r in summary['config_summary'] if r['stratum']==st and r['task']==task]
            cfg_rows.append([('자연' if st=='natural' else '정정우선')+' · '+task,*[r['success_fraction'] if r['criterion_n'] else '**해당 없음** (기준0/4)' for r in arr], '자연 H의 실제 소비판 기준은 네 건 모두 **미확인**' if st=='natural' and task=='H' else '규범적 보류는 포함; 접근보류는 근거 미달'])
    out.append(table(['층·과업: 근거 충족 / 기준 확인','B','B+L','B+X','B+L+X','해석 범위'],cfg_rows))
    out+=['',
    '자연 C에서는 기준이 있는3건이 모든 구성에서 같은 근거 판정을 얻었다. 두 건은 선택된 기본 정의뿐이고, French는 규범적 보류다. UCLA는 B/BX에서 접근보류, BL/BLX에서 관련 설명 유지로 행동이 달랐으나 외부 기준이 없어 정오를 매기지 않았다. 자연 H의 실제 소비판 기준0을 재구성판 도달률로 대체하지 않았다. 별도로 추가한 판을 대조할 수 있었던3사례의 도달은 B0/3, BL2/3, BX0/3, BLX2/3이다. NumPy와French가 증가했고 Python은 과거판 요청이 실패했다. 이4/12는 실제 소비 이력을 복원한4건이라는 뜻이 아니다.',
    '',
    '정정우선 H에서는 T01과J02가 L을 더한 두 비교에서 각각 원판/저작 대조에 도달했다. T01은 동적허브→archive색인으로 두 번을 소진하던 것을 날짜 있는 발표로 직접 이동해 해결했다. J02는 DOI 실패와 직접HTML 성공의 차이가 섞여 있다. T02는 B가 이미 그 발표를 가리켜 L이 새 도착주소를 주지 않았다. J01은 B/BX에서도 초기방법으로 공개HTTP를 선택해 DOI의 원저작을 읽어 네 구성 모두 성공했다. 따라서 J01을 L의 역사검증 이득으로 세지 않았다. [T01 발표](https://www.bea.gov/news/2024/gross-domestic-product-first-quarter-2024-advance-estimate) L11–17; 원장 T01-H/J01-H/J02-H 행.',
    '',
    'X가 있는 유효 H14건은 모두 로컬 재표시를 했다. 그중8건은 같은 시행의 발행판 대조도 있었고6건은 재표시만 가능했다. X 추가의 두 비교에서 발행판 대조 수의 증가는0이었다. 이 수치는 X가 무용하다는 뜻이 아니다. 발행자에 못 도달해도 저장 문구를 다시 제시하는 용도는 실현했고, 그 성과를 ‘그때 발행된 판을 다시 검증했다’로 승격할 근거가 없다는 뜻이다. 전체 원 H32판독은 발행저작/판 대조16, 로컬만6, 미확인10이며 자연 재구성판4건과 본 기준12건을 분리했다.',
    '',
    '정정우선 C에서 B→BL 및 BX→BLX는 각1건의 요구근거 도달 증가가 있었다. B→BX 및 BL→BLX는 각1건 감소했다. 그러나 감소한 J01-BX-C는 첫 DOI 접근실패로 보류했고, J02-BLX-C는 정정 DOI가 실패한 뒤 나중 BL-C에서 다른 실제 View correction 링크를 선택했다. 잘못된 수치를 확언한 사건은0이다. 이 차이는 X의 인과적 오도나 네트워크 성능의 효과 크기가 아니다. 허용된 요청방법·순서에 따른 관측이다. 원규칙의64짝을 유지하고 [pairs.csv](pairs.csv)의 attainment_delta와 배타적 정오 칸을 함께 읽어야 한다.',
    '',
    '### 한 요소를 더한 실제 근거 도달 증감','']
    effect_rows=[]
    for s in summary['pair_summary']:
        if s['sensitivity']!='original':continue
        effect_rows.append([('자연' if s['stratum']=='natural' else '정정우선')+' · '+s['task'],configs(s['comparison']),s['criterion_confirmed_n'],s['left_attained'] if s['criterion_confirmed_n'] else '**미확인**',s['right_attained'] if s['criterion_confirmed_n'] else '**미확인**',', '.join(s['attainment_gain_cases']) or ('**해당 없음**' if not s['criterion_confirmed_n'] else '0'),', '.join(s['attainment_loss_cases']) or ('**해당 없음**' if not s['criterion_confirmed_n'] else '0')])
    out.append(table(['층·과업','비교','기준 분모','왼쪽 도달','오른쪽 도달','증가 사례','감소 사례'],effect_rows))
    out+=['',
    '## Q6 · 처음 결론을 뒤집는 반례와 분야별 비교','',
    '초기 가설 “발행자에 주소만 남기면 과거 인용도 충분하고, 과거 인용은 현재 정정과 늘 어긋난다”는 그대로 유지되지 않았다. 다음 경로를 실제로 읽었고 실패/미확인도 결과에 포함했다. 사례를 바꾸어 원하는 효과를 만들지 않았다. 반례는 [수집 노트](collection/statistics/evidence-notes.md), [학술 노트](collection/journals/evidence-notes.md), [최종 원문 재점검](evidence/final-source-checks.jsonl)과 연결된다.',
    '']
    counter=[
      ['옛 X가 맞아도 현재 주장은 틀림','J01 원저작에는3716;2024정정은3806/4989를 올바른 값으로 명시. 소비자는 이미3806. '+link('정정','https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0301218')+' L123–126','H는 옛 표현을 확인할 수 있고 C는 원논문 수치의 현재재사용을 교체해야 한다. 실제 X유발 단정오류는 관측0.'],
      ['주소만으로 충분하며 추가 L이 거의 중복','T02 소비자의 원href가 날짜 있는 최초추계. '+link('원 발표','https://www.ons.gov.uk/economy/grossdomesticproductgdp/bulletins/gdpfirstquarterlyestimateuk/apriltojune2024')+' §2 L103','B만으로 C/H충족. L은 같은주소와절위치를 더했으며 X없어도 본문대조가 됨.'],
      ['같은 값이 다른 판에서 재등장','T01 같은2024Q1: 최초1.6→셋째1.4→2024연례1.6→2026연례1.4. '+link('2026 SCB','https://apps.bea.gov/scb/issues/2026/09-september/0926-nea-annual-update.htm')+' L479–480. T02 최초0.6→Sep2024 0.5→'+link('현재IHYQ','https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/ihyq/pn2')+' L382의0.6','숫자 일치는 판 일치의 충분조건이 아니다. 발행시점·기준기간·빈티지가 필요. 중간 모든빈티지를수집했다는주장은안함.'],
      ['같은 발행문서의 절 의미가 정정됨','ONS Sep30 quarterly '+link('superseded v1','https://www.ons.gov.uk/economy/grossdomesticproductgdp/bulletins/quarterlynationalaccounts/apriltojune2024/previous/v1')+' §7 L516의Quarter1이 '+link('정정본문','https://www.ons.gov.uk/economy/grossdomesticproductgdp/bulletins/quarterlynationalaccounts/apriltojune2024')+' L523의Quarter2로 변경. correction banner L57–63.','발행자가 공개한 전후본문 차이. 두시점 동일URL200을 직접관측한 사례는 **미확인**. GDP0.5 자체는 불변.'],
      ['정정이 인용한 좁은 주장을 건드리지 않음','J02 '+link('정정','https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0214558')+' L111–117,130–134는 배타적위치·그림·자료공개 문제를 다룸. '+link('MDPI 소비문','https://www.mdpi.com/1422-0067/22/3/1466')+' L181은 유전자발현역할만 참조.','정정이 있다는 사실만으로 소비 목적의 모든주장을 버리는 판단도 부적절. 원자료가결과를지지한다는것은저자진술이며독립재현 아님.'],
      ['판주소가 있어도 접근/판관계가 부족','Python 과거판 두 요청 실패; UCLA는 현행 이관위치만 확보. '+link('Python release page','https://www.python.org/downloads/release/python-3111/')+' Online Documentation은/3.11/ patch별칭. '+link('ICMJE','https://www.icmje.org/recommendations/browse/publishing-and-editorial-issues/corrections-and-version-control.html')+' L61은 구판을요청시제공도허용.','L존재·발행기록·공개2회이내도달·실제소비판확인은각각다른조건. X는로컬복원에유효하나진본검증을대신하지않음.']
    ]
    out.append(table(['반례 탐색','직접 관측/발행자 진술과 위치','현재 판단에 주는 제한'],counter))
    out+=['',
    '공식통계에서 최초값을 보존하는 실제 보고서는 SCB May2024이며, 같은2024Q1의 수정1.4를 사용하는 오늘의 별도 분석은 SCB September2026이다. 발행자들은 각각 당대 또는 수정된 빈티지를 명시한다. “현재의 더 나은 추정”을 사용하는 분석과 “당시 공개된 정보를 재현”하는 분석은 모두 합당할 수 있다. 이 대조는 선택한 T01의 C를 같은분기 최신값으로 몰래 바꾼 재채점이 아니라 별도 문서 비교다. [SCB May2024](https://apps.bea.gov/scb/issues/2024/05-may/0524-gdp-economy.htm) L29–31; [SCB September2026](https://apps.bea.gov/scb/issues/2026/09-september/0926-nea-annual-update.htm) L25–30,479–480.',
    '',
    '발행자 관점에서도 revision과error는 같은 말이 아니다. [ONS 공식 규칙](https://www.ons.gov.uk/methodology/methodologytopicsandstatisticalconcepts/revisions/guidetostatisticalrevisions) §3–4 L68–95는 계획된 자료 보강과 오류정정을 구별한다. [BEA 설명](https://www.bea.gov/news/gdp-release-additional-information) vintages/updates L54–70는 발표 단계와 개정을 설명한다. 반대로 [Crossref](https://www.crossref.org/documentation/crossmark/participating-in-crossmark/) L146–165는 중요 변경의 관계를 등록하고 같은 DOI에서 본문이 교체될 수 있음을 설명한다. 지속 식별자 하나를 불변 문장 보증으로 간주할 수 없다.',
    '',
    '개발자는 현재 API/설명과 목적이 맞는지를 먼저 봐야 하고, 당시 분석을 재현하는 인용자는 데이터 cut·버전·절이 필요하다. 잘못을 고친 발행자는 최신 내용과 정정 범위를 연결해야 하며, 감사자는 저장문구가 어떤 판에서 대조됐는지와 개인의 실제 소비가 확인됐는지를 구별해야 한다. 이 네 관점을 한 개의 “추천 유지” 표시에 합치면 옛 인용의 가치를 잘못 평가한다.',
    '',
    '## Q7 · 감도와 보관 방식의 적용 조건','',
    '두 감도를 각각 원규칙과 비교했다. S-X는 X에 판/URL 단서가 없다고 확인된7사례만 남긴다. UCLA의 X는 없으므로 단서 없음으로 가정하지 않는다. S-I는 task별 별도 발행본 기준이 직접 확인된 경우만 남긴다. 독립 발행본은 독립 기관/판독자를 뜻하지 않는다. 둘의 교집합을 새로운 주 분모로 쓰지 않았다. [pairs.csv](pairs.csv)의 sx/si 열, [48개 집계](evidence/analysis-summary.json)의 pair_summary가 계산 근거다.',
    '']
    sensitivity_rows=[]
    for sen in ('original','S-X','S-I'):
        for st in ('natural','correction_first'):
            for task in ('C','H'):
                selected=[j for j in js if j['stratum']==st and j['task']==task and (sen=='original' or j['sx_eligible' if sen=='S-X' else 'si_eligible'])]
                vals=[]
                for cfg in ('B','BL','BX','BLX'):
                    a=[j for j in selected if j['config']==cfg and j['criterion_confirmed']]
                    vals.append(f"{sum(j['supported_correct'] is True for j in a)}/{len(a)}" if a else '**해당 없음**')
                sensitivity_rows.append([sen,('자연' if st=='natural' else '정정우선')+' · '+task,len(selected)//4,*vals])
    out.append(table(['감도','층·과업','선택사례 수','B','B+L','B+X','B+L+X'],sensitivity_rows))
    out+=['',
    'S-X에서 알려진 기준 분모와 성과는 변하지 않는다. S-I는 J02 H를 제외하므로 정정우선 H가 B2/3, BL3/3, BX2/3, BLX3/3으로 줄어든다. 이때에도 T01의 날짜 있는 주소 이득은 남고 X의 발행판 대조 이득은0이다. 모든 자연 H의 실제 소비판 기준은 계속0이다. 서로 다른 출력의 절/값 일치와 실제 같은판 확인을 혼합하지 않은 결과다.',
    '',
    '### 세 증거 수준을 분리하는 조건부 보관 제안','']
    storage=[
      ['지역 보관 X','짧은 인용문·출처저작ID·판표시·절/record·저장시각·본문해시','발행자를 못 열어도 저장한 표현을 다시 표시하는 감사/출처회상','이번유효H14/14 재표시. 해시는로컬동일성이고발행진본·당시소비의증명은아님. J01현재재사용에는정정 확인이 추가로필요.'],
      ['판/발표 주소 L','소비 원href를 유지하고 필요할때 판전용주소·절·판범위·당시존재근거를 추가','공개옛판이있고허용예산안에본문을열수있을때; B가이미같은발표주소면중복L은필수아님','T01·NumPy·French에서추가판도달. Python실패,UCLA이관주소,J02직접HTML경로의한계를그대로표시.'],
      ['발행판 해당절 대조','실제로 연 URL·관측판·정확한절·일치/충돌·확인시각·정정관계와현재사용판단','그판에그말이있었는지와지금쓸수있는지를함께설명해야할때','엄격H12/16;자연재구성4/12별도. 최신권고나독립내용검증까지자동보증하지않음.']
    ]
    out.append(table(['증거 수준','조건부 필드','충분할 수 있는 목적','이번 근거와 실패 조건'],storage))
    out+=['',
    '탐색기가 링크와 용도를 돌려줄 때에는 `현재 용도 판단`과 `과거 인용의 증거 수준`을 별도 값으로 반환하는 설계안을 제안한다. 목적이 최신 사용인지 지정판 재현인지 먼저 보존하고, 현재 추천에는 실제 확인한 현행/정정 관계를 붙인다. X는 저장 당시 문구로 명시해 최신 설명처럼 보이지 않게 한다. 원 B에 판과 절이 이미 있다면 동일 L을 또 저장해야 한다는 결론은 나오지 않는다. 두 주소가 같은 저작을 가리키지만 접근경로만 다른 경우도 판식별 증가와 구별한다.',
    '',
    '세 대안은 조건부다. 주소 중심 보관은 공개판 접근이 잘 되는 T02/T01 같은 조건에서 충분할 수 있다. 발췌 중심 보관은 로컬 재표시에 충분하지만 현재판/원판 검증을 주장할 수 없다. 주소·발췌·실제 대조기록의 결합은 정정 관계 설명에 유리하지만 잘못된 시간 목적이나 미확인 소비판을 해결해 주지는 않는다. 비용·사람시간·재방문 횟수의 우열은 이번 범위에서 **미확인**이다.',
    '',
    '## 검증과 재개 범위','',
    '036의 C1/C2와039의 실패·바이트 회계는 고정 입력으로만 사용했다. 새 자료를 그 실험의 재수집이나 비용모형에 합치지 않았다. 본 결과는 문서/모델 판독이며 사람의 행동 관측이 아니다. 통계적 일반화, 효과크기의 인과 추정, 실제 사용자의 재방문 비용을 주장하지 않는다.',
    '',
    '① 범위,② 키/카드,③ 원관측의 원격 SHA와④ 이후 확인은 [PROGRESS.md](PROGRESS.md), 최종 고정 결과 SHA·원격 재독·session check는 [HANDOFF.md](HANDOFF.md)에 남긴다. [SELF_CHECK.md](SELF_CHECK.md)는 Q1–Q7의 정확한 위치·반증·미확인·결론이 바뀔 조건을 연결한다. source-count-audit와 analysis-audit는 같은 모델 계열의 별도 문맥 감사다. 최종 판정은 아래 세 약점이 해소된 완전수용이 아니라 미충족을 명시한 결과 인계다.',
    '',
    '## 남은 중요한 불일치·약점 — 정확히 세 건','']
    weaknesses=json.loads((ROOT/'evidence/weaknesses.json').read_text())
    out.append(table(['중요한 불일치·약점','영향받는 판단과 근거 URL·행','다음 최소 조사·첫 자료','결과가 달라지는 조건'],[[w['weakness'],w['affected'],w['next'],w['flip']] for w in weaknesses]))
    (ROOT/'RESULT.md').write_text('\n'.join(out)+'\n')
    print('RESULT.md written',len((ROOT/'RESULT.md').read_text().splitlines()),'lines')


if __name__=='__main__':main()
