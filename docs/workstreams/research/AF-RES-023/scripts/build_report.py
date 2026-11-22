"""Render required RESULT tables from ledgers and the v3/v4 composite self-check."""
from pathlib import Path
import json,csv,collections
P=Path(__file__).resolve().parents[1]
events=[json.loads(z) for z in (P/'events.jsonl').read_text().splitlines() if z.strip()]
events=[e for e in events if e['primary_sample']]
sources={s['id']:s for s in json.loads((P/'sources.json').read_text())}
rows=list(csv.DictReader((P/'reconstruction.csv').open()))
assert len(rows)==54
counts=json.loads((P/'evidence/counts.json').read_text())
spec={
'MB01':('private music 지역판','MB-S37','151147443 → 152536177/152539607/152589926; 2026-08-16→09-01','Europe 소장 CD; 지역·matrix','retained US/Canada + 새 Europe ID. 원 source 원상복구 아님','source f0a68a45 매핑은 이미지파일명 기반 추론; current route·matrix 대조 미확인'),
'MB02':('La Groupie/Les Princes','MB-S10','63656996(2019-09-04) → 115752742/115760023(2024-09-09)','CD3 track1 Les Princes 5:27','이름 복구와 medium 참조 분리를 각각 확인','ISRC/AcoustID 없음은 복구자 진술; 전수 외부 인용 미확인'),
'MB03':('07 오케스트라/비오케스트라','MB-S12','60587125(2019-04-16) → 63762772(09-16)/63972905(09-18)','Интервью B4 2:38 비오케스트라판','retained2:32와 새 recording2:38을 구별','원 source MBIDs·음원 비교·지문 전체 복원 미확인'),
'MB04':('Back Again 허용 병합','MB-S17','68967621; 2020-04-17 Applied,5yes0no','Reamonn Back Again7:34; CD edition 지정 안 함','recording 하나를 여러 release에서 공유','source MBID·원 ISRC별 provenance·사후 정정키 없음'),
'MB05':('Neththara 중복 보완','MB-S21','48434703(2017-10-14) → 48447069(10-21)','불완전한 앨범 정보 대신 보완된 같은 발매판','트랙3·8 보완 뒤 release/medium 병합','개별 status/old URL route·독립 실물 동일성 미확인'),
'MB06':('Tu es folle/AcoustID','MB-S22','92853437(2022-09-19) → 소비자2024-12-31/2025-02~06','지문과 녹음의 연결; live와replica 범위','catalog 적용 뒤에도 소비자 oldMBID/전파 결함 보고','2022즉시target·중간chain·모든replica 완결 미확인'),
'ROR01':('COMTES 중복','ROR-S03','#15331→15407; v1.56 수정2024-11-19/배포댓글11-20','회사 등록·연락 문맥','withdrawn tombstone + successor. 현실 회사합병 아님','resolver HTTP·소비자 처음작성/수정일·전체dump 미확인'),
'ROR02':('PTSD 본부/Division 기각','ROR-S09','#13495; 기각2024-11-05T18:34:53Z,종료12-02','Pacific Islands Division 소속 인용','소속 단위 때문에 병합 기각; 적용병합 아님','전후dump·인용논문 원문·현재HTTP 미확인'),
'ROR05':('ZFH 네 후계','ROR-S17','#20329; 현실종료2023/record v1.67 2025-06-24','옛 평가기록; 현재 문의 프로그램 미지정','inactive 역사기관 + 4 successor','특정 문의처 하나·EQAR 변경일·전체dump 미확인'),
'ROR06':('Cuauhtémoc 본교/SLP','ROR-S23','#19416→25805+25802; v1.66 2025-05-20→v1.72 10-06','San Luis Potosí 소속','원 ID Puebla 복구 + 새 SLP child. literal merge 아님','오류전 원판·외부 소비자 복구·전체dump 미확인'),
'ROR07':('Biofisica/Biofisika','ROR-S30','#6693→16454→17073; v1.38 2023-12-07→v1.60 2025-02-26/27','스페인기관 주장과 이탈리아 원ID의 구별','이름/사이트/부모 복구, changed JSON에 Spain/Leioa 잔존','Spanish 정답ID·오류전판·소비자 날짜·live API 미확인'),
'ROR08':('Gazipur/Netrokona','ROR-S38','#19286→21008+21009; v1.66 2025-05-20→v1.68 07-15','Netrokona 소속','wrong-ID 정정과 실제 Netrokona 정상rename을 구별','정부 개명공고·실소비자 수정·전체dump 미확인'),
'SW01':('TinyFugue 중복','SW-S01','7f379ed5…; 2011-10-28','tf-50b8 배포물; exact recipe 요구 안 함','중복 recipe 제거 + surviving formula alias','archive bytes·설치·독립 소비자 수정 미확인'),
'SW02':('libxml++3 정상rename','SW-S04','eb1463eb…; 2023-12-26','major3 탐색; exact recipe는 별도 목적','3.2.4 archive/SHA 유지; 현재old main404, fixed본문 확보','alias 설치실행 미실시; fixed URL HTTP503과 connector본문 구별'),
'SW03':('readline rename 취소','SW-S07','8c299821…; 2012-11-11','GNU readline6.2.4의 설치명/keg','canonical readline과 dependent 이름을 복구','최초rename 객체·설치실험 미확인; 실패는 편집자 진술'),
'SW05':('PostgreSQL 버전 승계','SW-S11','8060df91…; 2022-08-27 → Rails27cb8c61… 2024-05-23','Rails 당시 최신판; 이름/버전/데이터경로','canonical@14와 소비자 목적@16+libpq가 다름','DBmigration 실행·2026최신판 판단 안 함'),
'SW06':('tree-sitter library/CLI 분리','SW-S14','e5e819e6…; 2025-07-29 → 소비자 수정2026-05/11','generate CLI; historical0.25.8/consumer0.25.x','옛formula HTTP200이어도 library만. CLI successor 필요','실제빌드 재현 없음; latestCLI의 판 호환성 별도'),
'WD01':('category/institution 오병합 취소','WD-S05','1038289881(2019-10-24) → 1048159568/1048159950(11-08)','건물Q314104의 P910 main category','본체undo 뒤 별도consumer P910 undo1건','category 자체 복원판·전체incoming graph·사람 피해 미확인')
}
def esc(x):return str(x).replace('|','\\|').replace('\n',' ')
def link(label,url):return f'[{esc(label)}]({url})'
def table(headers,rs):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(esc(v) for v in r)+' |' for r in rs])+'\n'
def sl(sid):return link(sid,sources[sid]['url'])
def ids(e,phase):
    xs=e.get(phase,e.get(phase+'_ids',[]))
    out=[]
    for x in xs:
        if isinstance(x,str):out.append(x);continue
        ident=x.get('id')
        if ident is None:out.append('원 ID 미확인');continue
        name=link(ident,x['url']) if x.get('url') else ident
        extra=x.get('type','')
        if phase=='after':extra+='; '+x.get('relation','')
        if x.get('targets'):extra+=' → '+','.join(x['targets'])
        if x.get('target'):extra+=' → '+x['target']
        if x.get('status'):extra+='; '+x['status']
        if x.get('version'):extra+='; '+x['version']
        out.append(name+' ('+extra.strip('; ') +')')
    return '; '.join(out)

AFTER_TIME={'MB01':'Europe2026-08-31/retained지역2026-09-01','MB02':'2024-09-09','MB03':'2019-09-16','MB04':'2020-04-17','MB05':'2017-10-21','MB06':'2024보고/2026관측;2022즉시target미확인','ROR01':'v1.56;2024-11-19수정/20배포댓글','ROR02':'2024-11-05기각결정;dump미검증','ROR05':'2023현실종료;v1.67 2025-06-24','ROR06':'v1.72 2025-10-06','ROR07':'v1.60 2025-02-26수정/27댓글','ROR08':'v1.68 2025-07-15','SW01':'2011-10-28','SW02':'2023-12-26','SW03':'2012-11-11','SW05':'2022-08-27;소비자2024-05-23','SW06':'2025-07-29;현재HTTP2026-11-22','WD01':'2019-11-08T10:36/10:37Z'}
CORRECTION_SOURCE={'MB01':'MB-S06','MB02':'MB-S10','MB03':'MB-S13','MB04':'MB-S17','MB05':'MB-S21','MB06':'MB-S23','ROR01':'ROR-S06','ROR02':'ROR-S09','ROR05':'ROR-S19','ROR06':'ROR-S24','ROR07':'ROR-S31','ROR08':'ROR-S41','SW01':'SW-S01','SW02':'SW-S04','SW03':'SW-S07','SW05':'SW-S20','SW06':'SW-S14','WD01':'WD-S09'}

text=['# AF-RES-023 — 실제 병합·분리 뒤 옛 링크와 추천 이유의 복원','', '## 표 1 · 사건의 전후와 관측 범위','']
rs=[]
for e in events:
    eid=e['event_id'];title,sid,editdate,need,result,unknown=spec[eid]
    cr=CORRECTION_SOURCE[eid]
    refs=sl(sid)+((' · '+sl(cr)) if cr!=sid else '')
    rs.append([eid+' · '+e['system']+' · '+title,ids(e,'before'),refs+' · '+editdate,ids(e,'after')+'; '+AFTER_TIME[eid],need,result,unknown])
text.append(table(['사건 ID·시스템','변경 전 ID·종류·원 주소','편집·정정 주소·일시','변경 후 ID·관계·시점','당시 참조가 요구한 기능·판','관측된 결과','미확인'],rs))
text+=['## 표 2 · 같은 사건의 세 저장 표현','']
rs=[]
labels={'1':'① URL+짧은 이유','2':'② ①+당시 ID·판·근거 절','3':'③ ②+변경 관계·유효시점'}
for r in rows:
    eid=r['event_id'];rep=r['representation'];sid=CORRECTION_SOURCE[eid]
    rs.append([eid,labels[rep],r['target_verdict']+' · '+r['target_assessment'],r['function_version_verdict']+' · '+r['function_assessment'],r['destination_decision']+' · '+r['destination_assessment'],r['needed_evidence'][:110]+('…' if len(r['needed_evidence'])>110 else '')+' '+sl(sid)])
text.append(table(['사건 ID','저장한 정보 ①·②·③','옛 대상 복원','기능·버전·이유 복원','오연결 또는 보류','필요한 추가 자료·근거 주소'],rs))
text+=['## 표 3 · 선택지의 전제와 반례','']
text.append(table(['선택지','합쳐도 되는 조건','분리해야 하는 반례','이력 유지·이관 비용의 관측 단위','적용되지 않는 분야','근거·미확인'],[
 ['엄격 병합','같은 catalog 층위의 실제 중복; 목적·판 차이와 누락 데이터를 구별','MB01 지역release, MB03 recording, WD01 category/institution','MB05 선행 보완1+병합1; WD01 본체undo1+consumer undo1','같은 work→같은 recording, 같은 조직브랜드→같은campus라는 일반화 불가',sl('MB-S21')+'; '+sl('WD-S06')+'; 음원/실물 독립정답 미확인'],
 ['가역 별칭·옛 ID 보존','같은 배포물/주체를 찾는 좁은 목적; 관계시점과 과거판 유지','SW03 canonicalkeg, SW05 최신판 목적, ROR05 복수후계','SW02 rename map+전후blob; SW01 삭제recipe+alias+survivor','formula명에 MBID/ROR와 같은 영속·기능 보장을 자동 이전하지 않음',sl('SW-S04')+'; '+sl('SW-S07')+'; 설치·live resolver 미실행'],
 ['관련 후보 병렬 표시','분기·포크·조직단위가 다르며 사용 목적이 추가로 필요','SW01·MB05처럼 다른표기가 실제 중복인 경우 영구분리도 오류','ROR05 과거기관1+후계4; SW06 library/CLI recipe2 및 consumer별판','물리release의matrix를조직/소프트웨어에그대로이전불가',sl('ROR-S19')+'; '+sl('SW-S14')+'; 사용목적 없는 후계하나 선택 보류']
]))
text+=['## 표 4 · Q별 판정과 근거·반증','']
qrows=[
 ['Q1','실제수정/기각18; 완전전후이력18은미달',sl('MB-S37')+' Status; '+sl('SW-S14')+' changed recipes; '+sl('ROR-S09')+' rejection comment','MB6+ROR6+SW5+WD1; 시스템당최대6; 5:9:4','허용5와기각1을포함; aliasrollback/eigen3는이유불명으로보충','sourceID·전체dump부족. 원편집행/고정dump가판정을바꿈'],
 ['Q2','URL·record·실체·판·목적을18행 독립열로구분',sl('MB-S10')+'115752742/115760023; '+sl('ROR-S23')+'request; '+sl('SW-S01')+'recipe deletion','identity-layers.csv18행; 외부ID발급자전수원문0검증','같은DiscID다른release와다른표기같은tf-50b8을둘다확인','실체음원/법적조직동일성은일부저자진술. 발급자고정record필요'],
 ['Q3','현재HTTP와역사적target/기능을별도판정',sl('SW-S25')+'formula current; '+sl('SW-S05')+'3.2.4 recipe; '+sl('MB-S23')+'2024 report','직접요구반례200기능변화1,404+고정본문1; HTTP기록15회','deadURL만찾지않고aliveURL의기능범위와2022/2024/2026target을비교','MB/ROR현재HTTP·중간chain미확인; 실제응답/판별원행필요'],
 ['Q4','90개필드점검; 자동전수복원성공주장없음',sl('WD-S06')+'undo diff; '+sl('WD-S09')+'P910; '+sl('ROR-S31')+'names/links/relationships/locations','18×5행; 자동복원실행0/18; WDconsumer별도복구1','ROR07location잔존,MB01새ID재생성,AcoustIDreplica후속문제','미열람과실제소실구별. 원source와consumer전수diff필요'],
 ['Q5','소비자원문충족과날짜있는역사체인부족을구별',sl('SW-S20')+'Brewfile; '+sl('SW-S21')+'tools.tsv; '+sl('ROR-S20')+'institution history','원장13행; 최소수8/외부독립7; 날짜후속4/외부3; 불변전후diff3','COMTES좁은회사lookup/DEQAR역사인용유지와Rails목적변경을대조','사람오추천18/18미확인; ROR최초인용/수정고정판필요'],
 ['Q6','v3/v4 제한읽기54행; root사후자기점검',link('v4 manifest','evidence/frozen-manifest-v4.json')+'; '+link('key','reconstruction/key/answer-key.json')+'; '+sl('ROR-S19'),'18×3;16사건×3+2사건재판독×3;사건·표현당1답;미확인제외0','단순링크MB04,다중후계ROR05,중복미병합SW01/MB05; 입력결함발견후보강','실제추천문18건/인간독립시험아님. 독립판독및완전정정키필요'],
 ['Q7','실제경계가다른2쌍·4관점; 최종DB결정없음',sl('SW-FS03')+'README19,119–129; '+sl('ROR-X03')+'Recherche136–147; '+sl('WD-S06'),'2쌍,각4관점; 실제기관합병/포크보강은18분모제외','같은주소=같다와모든차이=분리를실제편집에서모두반증','작업시간·전체오병합률미측정; 관측단위편집/관계/consumer파일만사용']
]
text.append(table(['Q 번호','주장·판정 범위','근거 자료 주소·정확한 위치','확인한 내용·분자와 분모','반례를 찾은 경로·결과','미확인·결정을 바꿀 자료'],qrows))

summary=[]
for rep in ['1','2','3']:
    subset=[r for r in rows if r['representation']==rep]
    dc=collections.Counter(r['destination_decision'] for r in subset)
    tc=collections.Counter(r['target_verdict'] for r in subset)
    fc=collections.Counter(r['function_version_verdict'] for r in subset)
    summary.append([labels[rep],'18',f"SELECT {dc['SELECT']} / CONDITIONAL {dc['CONDITIONAL']} / HOLD {dc['HOLD']}",'; '.join(f'{k} {v}' for k,v in sorted(tc.items())),'; '.join(f'{k} {v}' for k,v in sorted(fc.items()))])
body=(P/'evidence/analysis-body.md').read_text()
body=body.replace('{{RECONSTRUCTION_SUMMARY}}',table(['표현','전체 분모','판독자의 목적지 결정','옛 대상 — 자기점검 범위','기능·판·이유 — 자기점검 범위'],summary))
text.append(body)
text+=['## 중요한 불일치·약점 — 다음 조사에서 바뀔 판단','']
text.append(table(['중요한 불일치·약점','근거 ID·주소','이 약점이 바꿀 판단','다음 조사 질문·자료·최소 확인'],[
 ['18사건은 확보했으나 완전한 원source/정정 chain18은 아니다. MB source누락·성공병합의 사후정정키부족, ROR changedJSON만확인.',sl('MB-S12')+'; '+sl('MB-S17')+'; '+sl('MB-S22')+'; '+sl('ROR-S31'),'③으로 충분히 복원된다는 일반결론을 보류. 승인·새ID생성과 원상복구를 구별.','공식snapshot의edit60587125/68967621/92853437/151147443 원행과ROR해당전체release를추출·대조.'],
 ['외부 소비자7원문 중 ROR4곳의 최초인용/수정일이 없다. dated 후속chain은외부3+내부1뿐.',sl('ROR-S08')+'; '+sl('ROR-S20')+'; '+sl('ROR-S33')+'; '+sl('ROR-S34'),'현재 설명불일치를 실제 사람의오추천·정정지연기간으로 해석하지 않음.','각소비자의사전고정파일과사후변경commit/배포일을한쌍씩확보; 먼저CoLab/OpenAlex의041xzk838 이력요청/공개판탐색.'],
 ['5:9:4 목적표집, 통제된가상추천이유, 사건·표현당1답. 입력보강뒤v3/v4결합판독이며실행재현없음.',link('protocol-errata','evidence/protocol-errata.md')+'; '+link('v4 hash','evidence/frozen-manifest-v4.json')+'; '+sl('SW-S22'),'전체오병합률·저장방식인과효과·자동복구성공률을 제시하지 않음.','완전한정정키를갖춘6/6/6추가표본과독립판독자,실제옛추천문·소비자실행을최소1사건씩검증.']
]))
(P/'RESULT.md').write_text('\n'.join(text).rstrip()+'\n')
print('RESULT.md written; first four tables and final three weakness rows rendered')
