"""Render complete pair coverage; input is authored conditional relation-spec.json."""
import json,itertools,collections,subprocess,datetime,hashlib
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def read(name):return json.loads((P/name).read_text())
def write(name,obj):(P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
bundles={x['id']:x for x in read('bundles.json')['bundles']};claims={x['claim_id']:x for x in read('CLAIM_CHECK.json')};spec=read('evidence/relation-spec.json')
# Deliberately selected supporting claims. Edges themselves are H assembly judgments.
choice={
('B01','B02'):('C-B01-03','C-B02-01'),('B01','B06'):('C-B01-02','C-B06-01'),('B01','B07'):('C-B01-03','C-B07-01'),('B01','B23'):('C-B01-02','C-B23-01'),('B01','B24'):('C-B01-03','C-B24-03'),
('B02','B07'):('C-B02-02','C-B07-01'),('B02','B11'):('C-B02-03','C-B11-02'),('B02','B23'):('C-B02-01','C-B23-03'),('B02','B24'):('C-B02-02','C-B24-03'),
('B03','B08'):('C-B03-02','C-B08-02'),('B03','B09'):('C-B03-01','C-B09-02'),('B03','B12'):('C-B03-03','C-B12-01'),('B03','B13'):('C-B03-01','C-B13-01'),('B03','B15'):('C-B03-01','C-B15-02'),('B03','B18'):('C-B03-01','C-B18-01'),('B03','B23'):('C-B03-01','C-B23-02'),
('B04','B05'):('C-B04-01','C-B05-02'),('B04','B06'):('C-B04-02','C-B06-02'),('B04','B12'):('C-B04-01','C-B12-02'),('B04','B17'):('C-B04-01','C-B17-02'),('B04','B19'):('C-B04-02','C-B19-02'),('B04','B20'):('C-B04-01','C-B20-01'),
('B05','B06'):('C-B05-01','C-B06-01'),('B05','B12'):('C-B05-02','C-B12-02'),('B05','B13'):('C-B05-01','C-B13-03'),('B05','B16'):('C-B05-03','C-B16-01'),('B05','B17'):('C-B05-03','C-B17-02'),('B05','B20'):('C-B05-02','C-B20-01'),('B05','B24'):('C-B05-02','C-B24-01'),
('B06','B07'):('C-B06-01','C-B07-01'),('B06','B08'):('C-B06-02','C-B08-02'),('B06','B13'):('C-B06-01','C-B13-03'),('B06','B16'):('C-B06-03','C-B16-01'),('B06','B17'):('C-B06-03','C-B17-02'),('B06','B20'):('C-B06-01','C-B20-01'),('B06','B24'):('C-B06-01','C-B24-03'),
('B07','B08'):('C-B07-03','C-B08-02'),('B07','B11'):('C-B07-01','C-B11-02'),('B07','B12'):('C-B07-02','C-B12-02'),('B07','B14'):('C-B07-01','C-B14-03'),('B07','B15'):('C-B07-01','C-B15-03'),('B07','B17'):('C-B07-01','C-B17-02'),('B07','B18'):('C-B07-03','C-B18-01'),('B07','B20'):('C-B07-01','C-B20-03'),('B07','B24'):('C-B07-01','C-B24-03'),
('B08','B09'):('C-B08-01','C-B09-02'),('B08','B21'):('C-B08-03','C-B21-02'),('B08','B24'):('C-B08-02','C-B24-02'),
('B09','B10'):('C-B09-02','C-B10-01'),('B09','B13'):('C-B09-03','C-B13-02'),('B09','B15'):('C-B09-02','C-B15-02'),('B09','B20'):('C-B09-02','C-B20-02'),
('B10','B15'):('C-B10-01','C-B15-02'),('B10','B16'):('C-B10-02','C-B16-02'),('B10','B17'):('C-B10-02','C-B17-02'),('B10','B20'):('C-B10-02','C-B20-02'),('B10','B21'):('C-B10-01','C-B21-01'),
('B11','B12'):('C-B11-03','C-B12-01'),('B11','B14'):('C-B11-02','C-B14-02'),('B11','B15'):('C-B11-03','C-B15-01'),('B11','B17'):('C-B11-03','C-B17-02'),('B11','B21'):('C-B11-02','C-B21-01'),('B11','B23'):('C-B11-01','C-B23-01'),
('B12','B13'):('C-B12-01','C-B13-01'),('B12','B14'):('C-B12-01','C-B14-01'),('B12','B20'):('C-B12-02','C-B20-03'),('B12','B24'):('C-B12-03','C-B24-03'),
('B13','B14'):('C-B13-01','C-B14-01'),('B13','B18'):('C-B13-02','C-B18-02'),('B13','B23'):('C-B13-02','C-B23-02'),('B13','B24'):('C-B13-03','C-B24-01'),
('B14','B15'):('C-B14-03','C-B15-03'),('B14','B18'):('C-B14-01','C-B18-01'),('B14','B20'):('C-B14-02','C-B20-02'),('B15','B18'):('C-B15-02','C-B18-02'),('B15','B21'):('C-B15-01','C-B21-02'),
('B16','B17'):('C-B16-01','C-B17-02'),('B16','B18'):('C-B16-02','C-B18-02'),('B16','B20'):('C-B16-02','C-B20-02'),('B17','B18'):('C-B17-02','C-B18-01'),('B17','B20'):('C-B17-02','C-B20-03'),('B18','B22'):('C-B18-02','C-B22-02'),('B19','B20'):('C-B19-02','C-B20-01'),('B19','B22'):('C-B19-01','C-B22-01'),('B20','B21'):('C-B20-02','C-B21-01'),('B20','B22'):('C-B20-03','C-B22-03'),('B23','B24'):('C-B23-03','C-B24-03')}
by_pair=collections.defaultdict(list)
for i,r in enumerate(spec,1):
 key=tuple(sorted((r['a'],r['b'])));assert key in choice,key
 ids=choice[key];refs=[]
 for cid in ids:
  c=claims[cid];refs.append({'claim_id':cid,'task':c['source_task'],'sha':c['sha'],'path':c['path'],'locator':c['locator'],'url':c['source_url']})
 if key==('B07','B12') and r['type']=='충돌':
  sha='3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc';path='docs/workstreams/research/AF-RES-016/RESULT.md'
  refs.append({'task':'AF-RES-016','sha':sha,'path':path,'locator':'Q7 L174; 원 evidence/role-filter-counterexample.json $.rows','url':f'https://github.com/laadkke-arch/agentflow-open/blob/{sha}/{path}#L174'})
 rec={**r,'relation_id':f'R{i:03d}','basis_claim_ids':list(ids),'source_refs':refs,'judged_by':'GPT-6 Astra Pro 작업자; 조립 관계 H','evidence_level':'H — 고정 D1 원 결과 및 명시된 원 관측 기반'}
 if r['type']=='선행':
  rec['prerequisite_scope']='조건부 의미 계약 또는 평가 전제; 선행 묶음의 전체 구현·자료집을 의무 편입한다는 뜻이 아님'
 by_pair[key].append(rec)
pairs=[]
for a,b in itertools.combinations(sorted(bundles),2):
 rs=by_pair.get((a,b))
 if not rs:rs=[{'relation_id':f'U-{a}-{b}','a':a,'b':b,'type':'무관','from':None,'to':None,'condition':'이번 묶음의 채택 결정에 직접 관계를 특정하지 않았다. 다른 묶음을 통한 간접 관계·미래 상호작용 없음의 주장이 아니다.','source_refs':[],'basis_claim_ids':[],'evidence_level':'H — 현재 조립 범위의 미선정','judged_by':'GPT-6 Astra Pro 작업자','unknown':'미확인(둘을 실제 함께 쓰는 새 과제에서 직접 의존 발견 시 행 갱신)'}]
 pairs.append({'a':a,'b':b,'relations':rs})
assert len(pairs)==276
counts=collections.Counter(r['type'] for p in pairs for r in p['relations'])
obj={'schema_version':'1.0','task':'AF-RES-020','semantics':'각 무순서 쌍은 한 행; 조건이 다른 관계는 여러 개 허용. 선행은 from→to. 독립 채택 판단과 무의존 실행은 다름. 무관은 이 범위에서 직접 관계 미선정.','bundle_ids':sorted(bundles),'pair_count':len(pairs),'non_unrelated_pairs':len(by_pair),'relation_counts':dict(counts),'relations_are':'H 작업자 조립 판단; 원 연구의 공동 적용 효과로 승격하지 않음','method_sources':['X04','X05','X06','X08','X10','X22'],'pairs':pairs}
write('RELATIONS.json',obj)
def cell(x):return str(x).replace('|','\\|').replace('\n',' ')
def table(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(cell(x) for x in row)+' |' for row in rows])
text='''# AF-RES-020 관계 행렬

## 1. 읽는 법과 범위

24묶음의 276개 무순서 쌍을 빠짐없이 기록했다. 87쌍에는 조건 있는 비무관 관계 91개가 있고, 나머지 189쌍에는 `무관`을 명시했다. 한 쌍의 조건이 달라지면 대체와 병용이 동시에 가능하다. 이는 기계적인 모순이 아니라 조건의 분기다. 모든 관계는 **원 결과를 바탕으로 한 작업자의 H 조립 판단**이다. 실제 공동 적용·경제성 검증으로 읽지 않는다.

선행 A→B는 명시한 경로에서 A의 정의·관측 계약이 B에 필요하다는 뜻이다. A의 구현 전체나 사전 자료집을 도입하라는 뜻은 아니다. C0의 요청별 검토 기록으로 B06의 좁은 주장 의미를 충족할 수 있다. `무관`은 이번 결정 범위에서 직접 연결을 특정하지 않았다는 뜻이며, 간접 경로나 미발견 상호작용까지 없다는 주장이 아니다. 근거와 조건의 원장은 [RELATIONS.json](RELATIONS.json)이다.

방법 비교: Parnas(X04)는 바뀔 설계 결정을 경계로 감추는 원리, Baldwin·Clark와 Sullivan(X05·X06)는 공통 설계 규칙·테스트와 모듈 옵션의 전제, QOC·ADR(X08·X10)는 조건·선택·이유 기록, NASA(X22)는 정보가 결정을 바꾸는지와 일정 비용을 비교하는 원리를 제공한다. 이 원리에서 이번 묶음 관계를 도출한 부분은 H이며 각 문헌이 이 24묶음을 직접 검증한 것은 아니다. [CROSSFIELD](CROSSFIELD.md).

## 2. 전체 행렬

셀: `함` 함께 씀, `충` 충돌, `대` 대체, `→선` 행이 열의 전제, `←선` 열이 행의 전제, `무` 직접 관계 미선정, `—` 자기 자신. 여러 기호는 조건별 복수 관계이며 우열 점수는 아니다. 열을 여섯 개씩 나눠 같은 전체 행렬을 표시한다.
'''
lookup={(p['a'],p['b']):p['relations'] for p in pairs};ids=sorted(bundles)
for st in range(0,24,6):
 cols=ids[st:st+6];rows=[]
 for a in ids:
  row=[a]
  for b in cols:
   if a==b:row.append('—');continue
   rr=lookup[tuple(sorted((a,b)))];v=[]
   for r in rr:
    v.append(('→선' if r['from']==a else '←선') if r['type']=='선행' else {'함께 씀':'함','충돌':'충','대체':'대','무관':'무'}[r['type']])
   row.append(' / '.join(v))
  rows.append(row)
 text+=f'\n### 열 {cols[0]}–{cols[-1]}\n\n'+table(['행 / 열']+cols,rows)+'\n'
text+='''
## 3. 숨은 전제와 분해의 한계

| 겉으로 독립인 것 | 실제 필요한 정의·자료 | 좁은 충족 방법 | 누락하면 생기는 오류 |
| --- | --- | --- | --- |
| B07 판정 | B01 강제성, B02 사용 범위, B06 원문이 지지하는 좁은 주장 | 요청별 원문 위치·판·E/H·proposed_use·설정 기록 | component 역할을 사용 방식으로 대체해 잘못 승인 |
| B12 기여 | B11 질문의 선택 범위와 답/제안 단위, B07 제안한 사용 | 원 질문×답/제안×후보/사용 연결과 코드북 판 보존 | 동일 후보의 서로 다른 기여를 하나의 role로 덮음 |
| B13 역할별 검색 결과 | B12 역할 재현성, B14 판정원, B23 질의 변환 | 역할 층화를 쓸 때만 전제 활성화; 못 채우면 전체 지표로 제한 | 역할 분류 차이를 검색기 성능 차이로 오인 |
| B16 유지 신호 | B17 초기 오류/후발 변화/이유와 사건 단위, B04 대상 범위 | 기준 시점과 현재 상태, 이유→사건 연결 | 현재 14/195를 후발5/83과 동일 빈도로 읽음 |
| B24 제외 필터 | B01 금지/선호, B06 범위, B23 번역·요약 보존 | 확인된 hard constraint 위반만 제외, unknown은 유지 | ‘필요 없음’을 ‘포함하면 금지’로 바꿔 후보 제거 |
| B22 인수 상태 | B18의 실행·관측 범위, 원 HANDOFF와 수용 근거 | 원 상태와 정규화·진행 상태의 출처를 따로 기록 | DONE을 D4 효과 검증이나 무조건 채택으로 표시 |

**나눌 수 없는 최소 묶음:** B07의 특정 판정 행을 문제 조건·제안한 사용·설정·제공 근거에서 떼어내면 판정 자체가 정의되지 않는다. B12의 contribution도 선택 범위·제안 문맥 없는 후보 속성이 아니다. 이 의미 계약 내부는 더 작은 독립 채택 단위로 분해하지 않는다. B01/B06의 구현을 각기 보류할 수 있어도 그 정의를 대신 충족하는 입력은 필요하다. 독립 판단의 단위와 실행 자립성을 혼동하지 않는 반례다.

## 4. 조건에 따라 조합과 충돌이 바뀌는 쌍

B05/B06은 같은 레코드에서는 경량 메모와 독립 주장이라는 대체안이고, 정정이 잦은 일부 문장에만 구조를 더하면 병용된다. B13/B24도 한계 문장의 순위 투입과 별도 제외 검사라는 대체 경로를 가지며, 넓게 회수하고 확인된 위반만 제외하는 경로에서는 함께 쓴다. B07/B12는 형태·기여 표시로는 병용되나 product-only 적합성 필터에서는 DIRECT 7개 중3개를 잃는다(016 RESULT Q7 L174; 고정18판정 팩·2코더의 반사실 계산). B07/B24는 결정적 위반을 거르는 조건에서는 병용되고, 선호/불필요를 금지로 바꾸면 충돌한다.

## 한계

원 결과의 정의와 기록에 근거한 정적 조립이다. 간접 의존과 실제 운영의 비용·성능 상호작용을 전부 열거한 것이 아니다. 관계를 채택할 때 조건을 지우지 않는다. 새 반례가 생기면 기존 관계를 덮기보다 조건·근거 판과 변경 이유를 남긴다. 세 구성의 구체 충족 방법은 CONFIGS의 전제 연결표에 있다.
'''
(P/'RELATIONS.md').write_text(text)
print(json.dumps({'pairs':len(pairs),'non_unrelated_pairs':len(by_pair),'counts':dict(counts)},ensure_ascii=False))
