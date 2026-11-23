"""Render the three required tables from frozen records plus explicit summaries."""
from pathlib import Path
import csv
import json

P=Path(__file__).resolve().parent
initial=list(csv.DictReader((P/'initial.csv').open()))
candidates=list(csv.DictReader((P/'candidates.csv').open()))
sources={r['source_id']:r for r in map(json.loads,(P/'sources.jsonl').read_text().splitlines())}
assess={r['candidate_id']:r for r in json.loads((P/'evidence/assessment.json').read_text())}
follow=json.loads((P/'evidence/followup-cases.json').read_text())
refs={}
def ref(label,key,url=None):
    refs[key]=url or sources[key].get('fixed_url') or sources[key]['direct_open_url']
    return '['+label+']['+key+']'
def table(headers,rows):
    clean=lambda s:str(s).replace('|','\\|').replace('\n',' ')
    return '\n'.join('| '+' | '.join(map(clean,r))+' |' for r in [headers,['---']*len(headers),*rows])+'\n\n'

first={
'IM-A1':['회색 제거·유색 부분 보존, Ruby에서 실행','QuickMagick.exec3의 convert 문자열 실행·오류 보고. 첫 본문 p2/pre2; 괄호 빠짐','p1/pre1에 grouped CLI 이미 인용; threshold15%','판·원 픽셀·정확한 최초 오류·회색 범위'],
'IM-A2':['조건별 흰 패치·합성 결과를 유지하며 명령 단순화','바깥 if/else 실제 사용, convert 안 if 삽입 실패. 첫 pre 및 마지막 pre','7.0.10-61/Cygwin; val>300;70×50/+851 또는30×40/+840','원 이미지/coords; convert 내부 분기가 불변 조건인지'],
'IM-U1':['숨은 QR을 일반 판독기로 읽을 수 있게 변환','불특정 인터넷 방법 실패만; 첫 p1. OpenCV/ImageMagick는 언급','qr.png 주소와 QR 판독 목표','구체적 도구·호출·판·원 픽셀·디코더'],
'IM-U2':['사진 속 직사각형을 자동으로 정면 보정','deskew는 추측만, 실행 없음. 첫 p1–p4 및 예시 링크','카메라 각도·굽힘이 가능한 입력','꼭짓점 검출·실제 종횡비·평면성·기존 지식'],
'TY-A1':['격자 각 저자 항목의 테두리와 내용·배치 유지','page.background의 stroked block과 별도 authors.map grid 사용. 최초 code blocks','16.5×18cm; 최대2열/4행; gutter1cm; silver1pt dashed','사용판·원 첨부 렌더; 긴 내용 overflow'],
'TY-A2':['수학 모드에서 내용·색 두 인자로 원 수식 색칠','colMath helper 실제 사용; # 없이 red 전달 시 undefined. 최초 helper·호출 예','text(fill:color), x/color, s_2^-; helper 이미 앎','사용판·scope 전체; # 완전 금지가 필수인지'],
'TY-U1':['그림+caption만 있는 별도 페이지, 세로 중앙','LaTeX [p] 코드 예시는 있음; 실제 Typst 시도 미명시','figure-only page 개념과 image/caption','기존 실행·Typst 판; 자동 floating이 필수인지'],
'TY-U2':['파일 직접 컴파일 때만 test/debug 출력, 포함 때 숨김','include와 Python __main__ 언급; 구체적 guard 시도 없음','다중 파일과 직접/포함 차이','실행 명령·판·기존 해법·허용 추가 설정']}
rows=[]
for r in initial:
    c=r['case_id'];v=first[c]
    q=ref(c+' · '+r['question_id'],'Q-'+c,r['initial_revision_url'])
    hist=ref('원 위치/지문','H-'+c,r['source_record'])
    rows.append([q,('특정 시도' if r['stratum']=='attempt' else '특정 시도 미명시')+' '+r['stratum_rank']+'위; 태그 모집 '+r['frame_rank']+'위',v[0],v[1]+' '+hist,v[2],v[3]+' 미확인'])
text=table(['요청 ID·최초 revision 주소','층·선정 순위','원 목적·필수 출력','당시 실제 시도·원 위치','이미 알려진 값','미확인'],rows)

# operation, official source IDs/section, difference, direct observation and limit
brief={
'IM-A1-C1':['QuickMagick 객체 pipeline','SUP-QUICK-IMAGE;IM-O1','객체 API·threshold','raw 문자열→객체 호출;15%→15','0.8.0 API/threshold 반대 근거. 수정형 OP 실패1건; 원판 전체 미확인'],
'IM-A1-C2':['RMagick·QuantumRange×.15','SUP-RMAGICK-CHANGELOG;SUP-RMAGICK-BINDING','4.0 제거·5.3 binding','다른 Ruby binding·mask 객체','matte=는4.0부터 제거. 5.3 literal 반박; 질문자판 미확인'],
'IM-A1-C3':['Open3 + grouped convert','IM-O2;SUP-RUBY-SHELLWORDS','image stack·shellescape','새 호출 경로; core CLI는 이미 인용','연구 CLI에서 회색 alpha0·색 보존. Ruby/원입력 미실행; Shellwords 로딩 조건'],
'IM-A2-C1':['조건별 명령 조각 문자열','IM-O2','Image Stack','convert 내부 if→바깥에서 fragment 선택','Bash argv에 역슬래시 괄호8개·인용부호 잔존. 원 Cygwin 전체 미실행'],
'IM-A2-C2':['dims/wd 변수로 치환','IM-O1','size·geometry','전체명령 분기→스칼라값 분기','원 rev1 bash -n exit2, 잔여fi·잘못 놓인-size·patch30×40 고정; 원문 반박'],
'IM-U1-C1':['-brightness-contrast 0,90','IM-O1;IM-O5','brightness-contrast','기존 구체적 조작 미확인','대비 효과 지지. 원 QR/출력403; 실제 decoding 미확인'],
'IM-U1-C2':['수평 peak 스캔·흑백 전환','SO-IM-77743451','원 제안의 알고리즘 설명','대비조절과 다른 처리 단계','완전한 구현·원 입력·예상 decode 결과 미확인; 공식 동작 근거 없음'],
'IM-U1-C3':['magick qr.png -normalize','IM-O1;IM-O5','normalize','히스토그램 조절; 기존 시도 미확인','7.0.10-61 문서2%/1%와 구현0.15%/0.05% 불일치. 연구판 결과 별도; QR 미확인'],
'IM-U2-C1':['네 꼭짓점→Perspective','IM-O1;IM-O4','Perspective·canvas','기존 시도 미확인; 부호/viewport 미명시','평면 성분만 조건부 지지; 자동검출·굽힘·종횡비 미해결'],
'IM-U2-C2':['+distort perspective','IM-O3;IM-O4','IsPlusOp·bestfit·viewport','+ 부호·출력 경계 구체화','± 기본 canvas는 다르고 viewport 고정 시 동일 RGBA. 원 자동보정은 미확인'],
'TY-A1-C1':['조건부 CSS border:2px 2px black','SUP-CSS-BORDERS','§3.2–3.4','CSS hook 가정; 기존 Typst 조작 아님','width 중복으로 literal CSS 반박. Typst hook 근거 없음'],
'TY-A1-C2':['각 authors.map 항목에 box(stroke)','TY-D01;TY-D05','box·page background','페이지 배경→각 항목 처리','v0.10.0 합성: stroke1→4, 내용12줄 보존. 원 사용자판 미확인'],
'TY-A1-C3':['box의 outset 옵션','TY-D01','outset','그리는 범위 변경; 값 미명시','2pt/2cm 연구 대조 중2cm 페이지 밖. 값·size 미확인'],
'TY-A2-C1':['외부 #let red=red + 같은 helper','TY-D02;TY-D03','math lookup·outer scope','helper 유지·호출 환경 변경','plain red 실패→binding 성공. red=blue이면 같은 helper도 파란 출력'],
'TY-A2-C2':['math 인수 #red','TY-D04;TY-D02','code expression·math call','색값을 code 모드에서 조회','원 수식 적용 성공·C1과 렌더 동일. 최초 짧은 예에는 위첨자− 생략'],
'TY-U1-C1':['pagebreak 전후 + align','TY-D05;TY-D06','pagebreak·horizon','실제 기존 Typst 시도 미확인','literal #pagebreak는1page; #pagebreak() 보정은3page. 자동 floating 미확인'],
'TY-U1-C2':['page container + 중앙 정렬','TY-D05;TY-D06','page·align','별도 수동 page container','합성 PNG+caption 중앙 독립page 지지. 자동 배치·기존 시도 미확인'],
'TY-U1-C3':['my-fig의 p 분기 helper','TY-D05;TY-D07','page·figure placement','새 이름 안에서 같은 수동 page 처리','C2와 가운데page 렌더 동일; 내장 figure에 p 직접 전달은 오류. B3위']}
rows=[]
for c in candidates:
    cid=c['candidate_id']
    if c['blank']=='True':
        rows.append([cid,'빈 자리: 30일 안 세 번째/해당 타인 조작 없음','해당 없음','판정 대상 없음','A 빈 자리 / B 빈 자리','미확인; 외부 검색으로 채우지 않음']);continue
    v=brief[cid];origin=ref('원 제안','O-'+cid,c['original_fixed_url'] or c['original_proposal_url'])
    links=json.loads(c['original_links']);attached=[]
    for i,l in enumerate(links):
        u=l if isinstance(l,str) else l['url'];kind='' if isinstance(l,str) else l.get('kind','')
        label='앞 댓글의 링크' if kind=='inherited_original_reference' else '원 첨부'
        attached.append(ref(label,'L-'+cid+'-'+str(i),u))
    original=origin+' '+v[0]+'; '+(', '.join(attached) if attached else '원 문서 링크 없음')
    official=' / '.join(ref(s,s) for s in v[1].split(';'))+' '+v[2]
    if cid=='IM-U1-C2': official='공식 절 미확인; '+ref('원 알고리즘','O-'+cid,c['original_fixed_url'])
    a=('제외: 실제 쓴 동일 제품' if c['A_decision']=='exclude' else (c['A_returned_position']+'위' if c['A_returned_position'] else '생존·2자리 밖'))
    b=c['B_returned_position']+'위' if c['B_returned_position'] else '생존·원3위, 2자리 밖'
    rec=assess[cid].get('execution_receipt') or assess[cid].get('observation_receipt') or 'evidence/assessment.json'
    rows.append([cid,original,official,v[3],'A '+a+' / B '+b+'; 조작 동일성 미확인',v[4]+' '+ref('판정/한계','ASSESS','evidence/assessment.json')+' '+ref('영수증','R-'+cid,rec)])
text+=table(['요청·후보','원래 제안 URL·조작','공식 근거 URL·절','기존 조작과 다른 점','A·B 반환 위치 또는 제외 사유','실제로 확인한 내용·미확인'],rows)

returns={
'IM-A1':['이미 시도했는지 한 가지 되묻기','괄호로 묶은 convert를 Ruby 밖에서 같은 이미지에 실행해 보셨나요?','IM-O2','grouped CLI까지 이미 실행했다는 기록이면 core 재추천을 줄이고 wrapper 오류로 범위를 좁힘.','B만C1/C2 반환; 유효 다른 조작 분모0, 전체 사전인지 분모0','수정 C1 실패 실행1에피소드. core CLI는 최초판에 알려짐; Open3 전체 사전인지·신규 인지 미확인'],
'IM-A2':['같은 도구 안의 다른 절','셸에서 값만 고르는 방식이 허용되면 흰 패치의 -size와 -geometry 절을 보세요.','IM-O1','내부 분기가 불변조건이면 바깥 변수 대안은 목적 전체를 충족하지 못함.','B만C1/C2 반환; 유효 다른 조작 분모0','원하는 방향이라는 반응과 감사. 원문 실행·수정 코드·신규 인지 미확인'],
'IM-U1':['이미 시도했는지 한 가지 되묻기','대비 조정 뒤 실제 QR 판독기로 읽어 보셨나요?','IM-O1','같은 입력·옵션의 decode 실패가 제시되면 대비 제안 반복을 줄임.','A/B 모두C1/C2; 유효 다른 조작 분모0','흑백 출력 추가 요청·유용하다는 평가. QR decoding·신규 인지·실행 미확인'],
'IM-U2':['조건부 두 링크','평면의 네 꼭짓점이 확보되면 Perspective를, 출력 경계까지 같아야 하면 viewport 절을 보세요.','IM-O1;IM-O4','자동 꼭짓점 검출 또는 휜 면 복원이 필수이고 미제공이면 두 절만으로 부족.','A/B 모두C1/C2; 전체 자동보정 유효 분모0','직교 각도 보정으로 목적 설명. 실제 실행·신규 인지 미확인; 첫 제안 전 rev2에 치수 미지 추가'],
'TY-A1':['같은 도구 안의 다른 절','page background 대신 각 authors.map 결과에 box의 stroke를 적용하는 절을 보세요.','TY-D01','원판 또는 실제 긴 내용에서 테두리/배치가 깨지면 조건부로 낮춤.','B만C2: 연구판 다른 유효 조작1/1; A 손실1, B 손실0','OP 후속 없음. 채택 시점·실행·신규 인지 미확인'],
'TY-A2':['즉답','이미 쓰는 colMath를 유지하고 색 인수를 #red로 전달하세요; #는 code 모드 진입입니다.','TY-D04;TY-D03','# 완전 금지 또는 다른 scope/판에서 실패가 확인되면 외부 binding 경로로 제한.','B만C1/C2: 연구판 분모2; 엄격 literal 분모1; A 전부 손실, B0','scope 이유를 묻는 반응. helper는 이미 알고 있었음; 바뀐 호출의 사전인지·신규인지·실행 미확인'],
'TY-U1':['조건부 두 링크','수동 전용 페이지가 허용되면 page·align, 자동 배치가 필수라면 figure placement 지원 범위를 먼저 보세요.','TY-D05;TY-D07','본문을 끊지 않는 자동 floating이 불변조건이면 수동 page의 목적 전체 충족을 낮춤.','A/B 모두C1/C2; 수동 C2 출력 지지, 기존 시도 미상으로 다른 조작 분모0','수동임을 지적하며 감사. 명시 거절·실행·신규 인지 미확인'],
'TY-U2':['이미 시도했는지 한 가지 되묻기','자기 답의 #import 방식으로 직접 컴파일과 포함 양쪽을 실행해 보셨나요?','SELF-TYU2','판·입력·출력 연결 실행이 나오면 자기 답의 실제 해결 여부를 갱신; 타인 후보수는 그대로.','A/B 반환 없음; 후보3자리 모두 빈칸','동시 자기 답으로 import 접근 인지 지지. 최초 prose/import와 code/include 불일치; 125일 뒤 타인 수정은 창 밖']}
rows=[];decisions=[]
for f in follow:
    case=f['case_id'];cs=[c for c in candidates if c['case_id']==case and c['blank']=='False'];v=returns[case]
    props='; '.join(c['first_proposal_utc'].replace('2024-','').replace('+00:00','Z')+' '+ref(c['candidate_id'].split('-')[-1],'O-'+c['candidate_id'],c['original_fixed_url'] or c['original_proposal_url']) for c in cs) or '30일 타인 제안 없음'
    ev=[]
    for i,e in enumerate(f['author_events']):
        proof=e.get('evidence',{})
        if isinstance(proof,list): proof=next((item for item in proof if isinstance(item,dict) and item.get('url')), {})
        u=e.get('url') or proof.get('url');time=e.get('event_utc','')
        if u:ev.append(time.replace('2024-','').replace('+00:00','Z')+' '+ref('후속','F-'+case+'-'+str(i),u))
    detail=props+' / 90일: '+('; '.join(ev) or '공개 작성자 후속 없음')
    official=[]
    for sid in v[2].split(';'):
        u='https://stackoverflow.com/revisions/5337E644-F174-44B9-8BC0-A747D9660F16/view-source' if sid=='SELF-TYU2' else None
        official.append(ref('볼 절' if u is None else '동시 자기 답',sid,u))
    rows.append([case,detail,v[5]+' '+ref('시점·행동 원장','FUP','followup.csv'),v[4],v[0]+' — '+v[1]+' '+' / '.join(official),v[3]])
    decisions.append({'case_id':case,'mode':v[0],'one_line':v[1],'source_ids':v[2].split(';'),'counter_observation':v[3],'links_are_editorial_after_study':True,'does_not_replace_frozen_A_B_returns':True})
text+=table(['요청','30일 제안·90일 후속 URL와 시점','이미 알았음·신규 인지·실행·결과의 근거','A만·B만 남긴 유효 대안·비교 가능 분모','권할 링크·볼 절 또는 질문 한 가지','오판 가능성·미확인'],rows)
(P/'evidence/return-decisions.json').write_text(json.dumps(decisions,ensure_ascii=False,indent=2)+'\n')

text+='''# AF-RES-101 — 제품명 일치, 조작 일치, 실제 인지의 분리

**연구 결론:** 같은 제품을 이미 썼다는 이유만으로 후보를 숨기면, 기존 시도와 다른 유효 조작도 사라진다. 이번 표본에서 그 근거는 두 Typst 요청의 세 후보다. 동시에 조작 동일성을 입증하지 못했다고 남겨 둔 후보 중에는 원문 오류와 미충족 조건이 있었다. 따라서 B의 더 많은 반환을 더 많은 유효 대안이나 새로운 지식으로 해석할 수 없다. 이는 후속 설계자가 선택·폐기할 근거 묶음이며 제품 정책의 일반 성능률을 추정한 실험이 아니다. [후보별 동작/한계](evidence/assessment.json), [분담 비판 검토](evidence/denominator-review.md)

표의 A는 최초에 실제 사용한 같은 제품 후보를 제외하고, B는 입력 상태·효과를 바꾸는 인자·처리 단계까지 기존 실제 조작과 같다고 입증된 후보만 제외한다. 두 필터는 같은 원순서에서 첫 두 생존 후보를 반환한다. **생존하지만 2자리 밖인 후보는 반환도 제외도 아니다.** 빈칸을 외부 검색으로 채우지 않았다. 공식 절은 연구자가 나중에 연결한 근거이며 원 제안에 붙었던 링크와 구별했다. [사전 규칙](SCOPE.md), [봉인 후보](candidates.csv)

## 분자·분모와 결측

| 관측 단위/지표 | 비교 가능한 분모 | A | B | 미확인·제외된 범위 |
| --- | --- | --- | --- | --- |
| 후보 자리 | 24=실재18+빈6 | 9 제외, 7 반환, 생존2개는 반환 밖 | 0 제외, 14 반환, 생존4개는 반환 밖 | 빈6은 평가 분모 아님 |
| 연구판에서 목적 지지 + 기존 실제 시도와 다른 조작 | 3: TY-A1-C2, TY-A2-C1/C2 | 다른 유효 조작 손실3/3 | 손실0/3 | 나머지15는 원문 반박·조건부·원목표/이전시도 미확인 등을 후보별 분리 |
| 위 지표의 원문 엄격 민감도 | 2: TY-A2-C2의 짧은 예에 빠진 위첨자−를 허용하지 않음 | 2/2 | 0/2 | 조작을 원 수식에 적용한 연구 입력과 원 예문 literal을 구별 |
| 전체 후보를 이미 알았거나 시도했다는 독립 증거에 따른 재추천 제거 | 0 | 산출 불가 | 산출 불가 | 전체 후보 사전인지18개 미확인; 일부 helper/core 지식은 별도 |
| 이미 아는 전체 후보를 새 후보로 실제 반환 | 0 | 산출 불가 | 산출 불가 | 같은 이유로18개 미확인; 생존과 반환을 혼동하지 않음 |
| 신규 인지의 명시 증언 | 조사 대상18에서 양성 관측0 | 인지율 산출 불가 | 인지율 산출 불가 | 신규 여부18개 모두 미확인. 0%라고 하지 않음 |
| 작성자 실행 보고 | 수정 C1의 실패1에피소드; revision+댓글2관측 | 해당 후보를 제외 | 해당 후보를 반환 | 봉인 원문 그대로의 실행0확인·18미확인; 입력/판/출력 완전 연결도0 |
| 원 사용자판과 원 입력을 함께 확인한 전체 목적 재현(추가 검증층) | 0 | 산출 불가 | 산출 불가 | 18개 미확인. 이를 사후에 주 분모의 새 조건으로 바꾸지 않음 |

정확한 후보 ID 배열·누락 이유·반환 재계산은 [reconciliation.json](evidence/reconciliation.json), 실행 코드는 [recalculate.py](recalculate.py)에 있다. 세 유효 조작은 **두 요청에 속한 세 후보**이며 독립 요청 세 개가 아니다. B만 반환한7개 중 연구판 목적 지지는3개이고 나머지4개에는 wrapper·셸 관련 반대 근거가 있다. A만 반환한 후보는0개다. 각 후보의 목적 적합성, 사전 지식, 신규 인지, 실제 실행을 서로의 대리값으로 사용하지 않았다.

## 모집·최초판·변경판

Stack Exchange API의 2024-01-01~06-30 UTC 현재 태그 모집틀을 생성시각→숫자 ID 순으로 읽었다. ImageMagick60개, Typst27개, 합계87개다. 각 태그에서 적격인 특정 실제 시도2개·특정 시도 미명시2개를 골라8자리를 채웠으므로 H2 연장은 하지 않았다. 현재 태그/제목 모집과 최초 공개 revision의 차이를 [frame.csv](frame.csv)에 보존했다. 답 수·채택 표시는 선정 판단에서 가렸고, API에 원래 포함된 필드의 기계 수신과 모델 실제 노출을 구별했다. [최초 봉인](evidence/seals/initial.json), [초기 시도](initial.csv)

경계 탈락 IM77772356은 PNG→CR2 실패를 명시했지만 최종 요청이 이미지 결과 조작이 아니라 지원 형식 목록/API였으므로 제외했다. '시도 없음'으로 분류한 것이 아니다. TY77831146은 최초 본문만으로 원하는 정렬이 특정되지 않고 첨부 이미지 접근이 막혀 부적격으로 두었다. 현재 제목을 소급하여 목표를 채우지 않았다. 이 두 경계가 바뀌면 모집 결과도 달라진다. [경계 별도 대조](evidence/initial-boundary-review.md)

현재 질문 본문이 최초판과 다른 경우는3/8, 실제 시도 이력이 달라진 경우는 IM-A1 한 건이다. IM-U2는 첫 제안 전에 추가된 치수 미지 조건도 별도로 보존했다. 엄격한 동일성 기준에서 확정되는 A/B 반환 변화는0/8이지만, 이것이 시도 이력·목표 조건이 같다는 뜻은 아니다. TY-U2의 동시 자기 답은 최초 prose의 import와 code의 include가 달랐고, 약125일 뒤 타인이 code를 수정했다. 그 수정은90일 창 밖이며 당시 성공을 입증하지 않는다. [최초/현재 대조](evidence/original-current-comparison.json)

## 반대 근거까지 확인한 동작 차이

**같은 도구의 다른 처리 위치:** TY-A1은 page background에 선을 그리는 상태에서 각 map 결과에 box를 씌우는 조작으로 바뀐다. v0.10.0 합성 입력에서 선1개가4개가 되고12줄 내용이 보존됐다. 하지만 outset이 같은 함수에 있다는 이유로 모든 값이 유효하지는 않았다. 연구자2cm 대조에서는 선이 페이지 밖으로 나갔다. 원 제안의 미지정 값을 유리한 값으로 채워 유효성 분모에 넣지 않았다. [고정 container 구현](https://github.com/typst/typst/blob/70ca0d257bb4ba927f63260e20443f244e0bb58c/crates/typst/src/layout/container.rs), [측정](evidence/typst-official/metrics.json)

**이미 아는 helper와 바뀐 입력 환경:** TY-A2는 helper 자체가 이미 본문에 있었다. 외부 red binding 유무에 따라 같은 math 호출이 실패하거나 성공했고 red를 blue로 바인딩하면 출력 색도 달라졌다. #red 경로를 원 수식에 적용한 렌더는 C1과 같았다. 이는 해당 상태의 효과 동등성이지 질문자가 새 helper를 배웠다는 증거가 아니다. 후대 답의 markup mode라는 명칭도 공식 syntax의 code expression과 구분했다. [고정 scope](https://github.com/typst/typst/blob/70ca0d257bb4ba927f63260e20443f244e0bb58c/crates/typst/src/foundations/scope.rs), [원 입력/출력 영수증](evidence/typst-official/run-receipt.json)

**실행 성공과 목적 충족:** Typst의 literal #pagebreak는 컴파일 종료값0이어도 함수 이름을 출력하고1페이지에 남았다. 호출 괄호를 보충한 것은3페이지가 되지만 원 표기를 보정한 별도 대조다. page container와 my-fig helper는 동일한 수동 페이지를 만들었으며 자동 floating 동등성은 입증하지 못했다. ImageMagick A2의 첫 제안은 셸 구문 검사를 통과해도 확장된 argv에 역슬래시와 인용부호가 남았고, 두 번째 원 제안은 잔여fi로 구문 검사 exit2였다. 감사·현재 채택을 이 오류의 해결 증거로 읽지 않았다. [Typst 대조](evidence/typst-official/RESULT.md), [셸/그룹/threshold 영수증](evidence/root-supplement/probe-receipt.json)

**공식 문서도 판과 구현을 대조해야 한다:** ImageMagick7.0.10-61의 normalize 문서는2%/1% clipping 동등식을 설명하지만 같은 SHA의 enhance.c는0.15%/0.05%에 해당하는 값을 사용한다. 실제 실행한 연구판7.1.1-43에서는 normalize와 문서 별칭이2000/2000픽셀 일치하고 옛 구현 값의 별칭과는1992픽셀이 달랐다. 옛 바이너리를 실행한 결과로 쓰지 않았다. [고정 문서](https://github.com/ImageMagick/ImageMagick/blob/eeb41d70c9baf418a3aa75c424fb305362a1b280/www/command-line-options.html), [동판 구현](https://github.com/ImageMagick/ImageMagick/blob/eeb41d70c9baf418a3aa75c424fb305362a1b280/MagickCore/enhance.c), [실행](evidence/imagemagick/stage3/probes/results.json)

**B의 중복 생존 반례 탐색:** IM-A1-C3의 grouped CLI는 최초판에 이미 있었지만 Open3/Shellwords까지 아는지는 미확인이다. core만 단위로 바꾼 민감도에서는 A가 알려진1개를 제외하고 B는 생존시키지만 원3위라 실제 반환하지 않는다. TY-U1 새 helper도 수동 page의 기존 원리를 감싼다. 완전 후보 사전인지 분모와 이런 부분 지식을 섞지 않았다. 'B가 중복을 실제 반환하지 않는다'는 일반 결론도 자료가 지지하지 않는다. [후보별 해석](evidence/assessment.json), [별도 분모 검토](evidence/denominator-review.md)

## 다른 분야에서의 교정과 보여줄 한 줄

| 실제 명령 대조 | 입력·관측 | 링크 편집에 주는 교정 |
| --- | --- | --- |
| git restore --worktree / --staged | HEAD=base,index=index,worktree=worktree에서 각각 index/index와 base/worktree | 같은 프로그램·같은 매뉴얼이어도 대상과 기본 원천이 다름 |
| git restore --source=HEAD --staged --worktree / -s@ -SW | 둘 다 base/base | 다른 표기만으로 새 조작이라고 하면 중복을 남김 |
| ffmpeg -i source.mkv -c copy / -map 0 -c copy | 영상1·음성2 입력에서 출력2streams/45packets와3streams/89packets | stream selection과 copy를 구별해야 모든 음성을 보존 |
| -map 0 -c copy / -map 0 -codec copy | 같은89개 packet hash 배열 | URL·이름·옵션 철자가 달라도 같은 조작일 수 있음 |
| -map 0 -c:v copy -c:a flac |3streams 유지, codec ffv1/flac/flac,21packets | 선택집합이 같아도 처리 단계가 다름 |

Git v2.45.2 매뉴얼·t2070, FFmpeg n7.0.1 문서·FATE 파일을 직접 읽었다. 실제 합성 실행은 Git2.56.1/FFmpeg7.1.5이며 의미 대조7/7이다. 입력이 이미 동일하거나 음성이 하나뿐이면 겉으로 같은 출력이 날 수 있는 반례도 남겼다. [4개 고정 원자료 및 명령별 결과](evidence/cross-domain/RESULT.md), [전체 실행 영수증](evidence/cross-domain/commands.jsonl)

사용자에게는 바뀌는 입력·출력과 남는 제약을, 답변자에게는 기존 시도와 다른 인자·단계를, 편집자에게는 같은 문서의 다른 절과 다른 표기의 같은 호출을 보여주는 것이 이 자료에 맞는다. 표3의 한 줄은 이 세 관점을 목적별로 합친 후속 편집안이다. 원 A/B 순서를 재채점하거나 새 후보를 원래 받은 링크로 넣은 결과가 아니다. [8개 결정·반대 관측](evidence/return-decisions.json)

## 자료 수·범위·검토

| 고유 1차 자료 범주 | 수 | 산입 방식 |
| --- | --- | --- |
| 선정 공개 요청 |8|한 사건의 댓글·수정·자기 답을 별도 사건으로 늘리지 않음|
| ImageMagick 고정 문서/구현 |5|같은 문서의 여러 anchor는1개|
| Typst 고정 문서/구현 |7|동일 source의 live reference 중복 제외|
| ImageMagick 상류 시험/입출력 묶음 |2|원파일 직접 읽기와 연구판 실행을 구별|
| Typst 상류 입력/예상 출력 묶음 |3|input와 expected PNG를 한 묶음으로 산입|
| Git·FFmpeg 정식 문서/상류 시험 |4|각 도구2개; 주8사건 분모에는 제외|
| QuickMagick·RMagick·Ruby·W3C 보조 1차 자료 |6|배포 gem의 동일 파일·metadata 중복 제외|
| 합계 |35|필수 범주29, 요구 하한24 충족|

비선정79요청의 최초판도 개별 원장에 남겼지만 하한에 산입하지 않았다. 검색 미리보기·미러·읽지 않은 링크·실패 응답도 고유 수에 넣지 않았다. 이미지403/503, 옛 Perspective 링크404, 잘못된 upstream 경로404는 [ImageMagick 취득 기록](evidence/imagemagick/stage3/image-acquisition.json)과 [보조 실패](evidence/root-supplement/failures.jsonl) 등에 보존했다. [sources.jsonl](sources.jsonl), [범주 검산](evidence/source-counts.json)

전체 맹검이라고 주장하지 않는다. 기계가 수신한 현재 상태와 모델이 읽은 projection을 구별했고, 두 번째 봉인 전 답변자 글에 인용된 OP 오류 등 간접 노출을 기록했다. Typst 공식 평가는 OP 후속을 읽지 않은 분담자가 완료했고 이후 다른 분담자가 분모를 실제 대조했다. 분담 교차검토는 사람의 검토가 아니며 Typst 최초 코딩을 맡은 사람의 해당 부분 재검토는 자기검토다. [노출 범위](evidence/seals/behavior-exposure.json), [실제 교차검토](evidence/independent-review.md), [Q1~Q7 자기점검](SELF_CHECK.md)

민감도: IM-U2 두 제안을 같은 제안의 구체화로 합치면 실재17·A반환6·B반환13이 되어 차이7은 유지된다. ImageMagick engine 대신 wrapper 단위로 A를 한정하여 IM-A1-C2만 달리 처리하면 A반환8/B14가 된다. 이런 단위를 본문/후속을 본 뒤 유리하게 선택하지 않도록 주 표는 사전 봉인을 유지했다.

## 계약·커밋·재현

시작 통합판은 ac7abc85e12b3a5b5f87b694d00e9511332fe272. 계획판 ace1a06a13ea435f5cb6a3e340ad24f03f68ecae와 달라진 것은 dot-control.json뿐이며 브리프/연구규칙 blob은 동일했다. 운영 의존 tip은 등록판 a4b5471c08dc369367645a9e78249b44f8143f05와 같았고 연구 자료는 f475e1a55c5be68cd6d9bcca1a7c7b4f9893e24c에 고정했다. 097은 지정 표·인계·reconciliation만 교정용으로 읽고 이전 실행을 반복하지 않았다. [시작 계약](manifest.json), [원 blob 대조](evidence/start/contract-read.json)

| 묶음 | 원격 커밋 | 봉인 UTC·변경파일 영수증 |
| --- | --- | --- |
|① 모집·최초 이력|9d646592613ba2fd9c52bc9bbf3dbc28bac68693|2026-11-23T22:00:31.806896Z; evidence/seals/initial.json|
|② 원 제안·A/B·후속 전 봉인|4e7539906eb03abd46e6910643ed5317f97ddb45|2026-11-23T22:07:03.624061Z; evidence/seals/candidates.json|
|③ 동작·후속·반례|c68b40e646dffcc41261ea21974c2bbfeab53348|2026-11-23T22:22:41.461916Z; evidence/seals/behavior-followup.json|
|④ 분모·반환표·자가검토·재현|이 RESULT를 담은 고정 결과 커밋|정확한 결과 SHA·검사·GitHub 재열람은 마지막 HANDOFF에 기록|

최초/후보 CSV의 로컬 CRLF와 원격 LF 차이는 [전송 정규화 영수증](evidence/seals/transport-normalization.json)에 양쪽 SHA를 남겼다. 파싱한8/87/24행은 같고 봉인 판단은 변경하지 않았다. 직접 git push는 인증 입력 수단 부재로 실패했으며 허용된 GitHub 연결의 tree/commit/ref 갱신으로 각 묶음을 원격에 반영했다. [원격 기록](evidence/seals/commits.jsonl)

연구자의 실행: Typst v0.10.0 합성17개(종료0 15개·의도 오류2개), ImageMagick 연구판에서 상류 colorspace19/19와 작은 동작 대조, Git/FFmpeg 의미 대조7/7. 원 사용자판/원 입력 재현, Ruby 전체 snippet, Git t2070·FFmpeg FATE·Typst 상류 전체 스위트 실행은 미실시다. 이 미실시를 통과로 쓰지 않았다. 정확한 공개 읽기·재계산·재현 명령과 필요한 입력은 [reproduce.md](reproduce.md)에 있다. 사용자의 즉시 마감 지시에 따라 추가 탐색은 중단하고 확보된 결과와 한계를 확정한다.

'''
weaknesses=[
['원 사용자판·원 입력 부재와 normalize 문서/구현 불일치','7.0.10-61/Cygwin 및 실제 Ruby gem 판에서 원 이미지·좌표로 재생; QR은 원 픽셀과 판독기 결과 필요','동일 원판/입력에서 다른 출력 또는 목표 실패가 확인되면 연구판 지지 범위를 낮추고, 일치하면 해당 범위만 확장'],
['신규 인지·완전 후보 사전 지식 미확인; 원문 예시와 적용 조작 차이','제안 전 실제 호출 기록/명시 회고·입력/판/출력 연결 실행; TY-A2 #red의 원 수식 포함 호출','전체 후보를 이미 알았다는 독립 증거가 나오면 중복 분모를 열고, 원문 그대로 출력 충족이 확인되면 literal 민감도 갱신'],
['모집 경계와 후보 단위·노출의 민감도','TY77831146 최초 첨부, IM77772356 최종 목표, IM-U2 첫 proposal의 부호/viewport/좌표 확인','적격 목표가 복구되면 모집 대체, 두 제안이 완전 동일하면17/6/13으로 병합; 기존 주 봉인과 차이는 별도 유지']]
(P/'evidence/weaknesses.json').write_text(json.dumps(weaknesses,ensure_ascii=False,indent=2)+'\n')
text+='\n'.join('['+k+']: '+v for k,v in refs.items())+'\n\n'
text+=table(['가장 중요한 불일치·약점','다음에 열 자료 또는 실행할 입력','어떤 관측이면 결론을 바꿀지'],weaknesses)
(P/'RESULT.md').write_text(text)
print(json.dumps({'result_bytes':len(text.encode()),'required_table_rows':[8,24,8],'references':len(refs)},ensure_ascii=False))
