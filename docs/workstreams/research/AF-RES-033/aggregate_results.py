"""Reconstruct 144 pairs and question-level denominators from frozen ledgers.

This program never changes queries, scores, the corpus, or primary judgments.
Document correspondence and evidence in the original returned window are distinct.
Use --check to compare generated products byte for byte without writing them.
"""
import argparse
import csv
import io
import json
import unicodedata
from collections import Counter
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
FIELDS = ('library', 'transport', 'statistics')
LABELS = ('support', 'conflict', 'partial', 'unverified')


def readjl(name):
    return [json.loads(x) for x in (ROOT/name).read_text().splitlines() if x.strip()]


def js(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


WINDOW_NOTES = {
 'R01-S': [
  '자원이 안정·증가할 때 기존과 비슷한 연결·빈도·시간을 지향하지만 지역 우선에 따른 예외를 허용한다. 동일 의미의 개명·옛 호출 전달·호출 시 경고는 없다.',
  '사전 공지와 대체 운송수단의 우선순위가 있다. 동일 동작의 별칭 전달이나 향후 의미 변경을 호출자에게 경고하는 규칙은 없다. 문서의 추가 예외를 이 창으로 소급하지 않는다.',
  '낮은 수요에서 철도를 버스로 대체하고 운행 수준을 줄이는 조건을 말한다. 같은 실행 효과를 보존하는 이름 변경이 아니다.'],
 'R01-R': [
  '정류장 앞문 접근과 20피트 공간을 단계적으로 확보하는 제안이다. 옛 이름·전달·경고의 대응 근거가 없다.',
  '노선 직선성·우회·연결의 물리적 설계다. route/consistent가 등장해도 식별자 전달과 동일 의미 보존은 입증되지 않는다.',
  '경미·주요 운행 변경과 승인 권한을 구분한다. 개명 후 옛 호출을 동일 구현에 전달하는 동작이 없다.'],
 'R02-S': [
  '수요·재원에 따라 노선 자원을 재배분한다. 상하위 항목의 암묵 유입과 명시적 접근을 구분하는 선택 규칙은 없다.',
  '대출 상태·수령점 변경 마감·기간의 절이다. 제공 문서의 로컬 소장본 요청 금지 근거는 이 창에 없으며 한정 상위 접근 보존도 없다.',
  '정정 배너와 출력 변경 공지는 있으나 이름이 같은 상하위 항목의 충돌 해소와 명시적 양쪽 접근은 없다.'],
 'R02-R': [
  '비상·실험 변경에서 180일 분석 유예를 정한다. 암묵 상속·명시 import의 진리표에 대응하지 않는다.',
  '시계열의 전 구간 재기준화와 과거 수정이 허용된다. 명시적 구 항목을 선택해 동일 동작을 유지하는 규칙은 없다.',
  '기존 교통수단 우선과 셔틀 대안을 말한다. 일반적 우선순위를 namespace 해소 규칙으로 대체할 수 없다.'],
 'R03-S': [
  '이용자 계정 등록과 대출 신청이다. register는 CPU 레지스터가 아니며 입력 소비 전 출력 덮어쓰기 금지가 없다.',
  '대출 카드 등록과 검색·신청 절차다. 레지스터 수명·출력 할당의 대응은 미확인이다.',
  '비상 운행 변경 권한과 혼잡 개선 우선순위다. 자원의 소비 완료 후 재사용을 보장하지 않는다.'],
 'R03-R': [
  '노선 우회와 고정·가변 경로를 비교한다. 읽기 완료 전 덮어쓰기 금지나 lateout 재사용 조건은 없다.',
  '현장 피드백과 12개월 시범 운행 뒤 평가다. 컴파일러 입출력 수명 경계와 같은 것으로 볼 근거가 없다.',
  '신청 시스템 계정 등록·통합이다. 입력값 소비 후에만 출력 공간을 재사용한다는 동작은 없다.'],
 'R04-S': [
  '노선 개편 전후 서비스를 설명해 이해관계자에게 알린다. 종료 집단 보관·인프라 동결·재개 승인까지 제공하지 않는다.',
  '빌릴 수 없는 기록물과 도착 지연 대응을 다룬다. archival이라는 단어는 프로젝트 종료 후의 기록 보관 절차가 아니다.',
  '참여 자료·요약을 남기고 의견을 받는다. 집단의 종료·비공개 피드백 제외·권한 있는 재개 규칙은 없다.'],
 'R04-R': [
  '기록물 대출 제외와 지연 대체본 요청이다. 프로젝트 보관/재개에 필요한 상태 전이와 책임자를 반환하지 않는다.',
  '개편 전후 설명은 공개 설명의 부분 단서다. 중단 집단 보관과 담당자·상위팀 합의로 재개하는 동작은 없다.',
  '서로 분리된 대출 계정과 카드 교체 시 통합이다. 조직 보관·인프라 동결·재개 합의는 없다.'],
 'R05-S': [
  '서비스 지침 구성과 승객 혼잡도 도입부다. 혼합 요청의 접수와 공급자 실현 결정을 나누는 절은 없다.',
  '비상시 운행 변경 권한과 투자 우선순위다. 한 혼합 객체를 API에서 허용한다는 구조는 없다.',
  '운행 변경의 비교·비용·수요 조정을 다룬다. 이종 포트를 한 객체에 접수하는 경계는 없다.'],
 'R05-R': [
  '혼잡도·차량 용량·시설 책임의 다단 본문 조각이다. 서로 다른 단을 합쳐 혼합 요청 중개 원리로 읽지 않는다.',
  '예외적 운행 변경 권한을 준다. 혼합 객체 접수 후 기존 공급자에 전달한다는 두 조건은 없다.',
  '확장 운행의 재원 제약과 팬데믹 축소를 설명한다. 이종 정의 접수와 공급 가능성의 역할 분리는 입증되지 않는다.'],
 'R06-S': [
  '노선별 서비스 종류·수준과 지역 특성을 나눈다. 별도 Kind·파일·flag 우선·공유 갱신 비침범은 없다.',
  '통행시간 구성요소의 가중치를 합산한다. 구성요소를 나열하는 것만으로 instance 설정의 별도 저장 경계는 생기지 않는다.',
  '예산 시나리오에서 일부 수치를 고정한 가정이다. 실제 노드별 설정을 동적 공유 갱신에서 보호하는 절이 아니다.'],
 'R06-R': [
  '교통수단별 혼잡 한도와 특수 서비스 예외를 둔다. 저장 Kind/파일 분리·legacy flag 우선·공유 갱신 방지는 없다.',
  '이동 요소별 가중치를 계산한다. 두 설정 표현의 독립성과 우선순위는 반환하지 않는다.',
  '혼잡·신뢰성·성장의 투자 순서와 비상권한이다. legacy flag와 파일 값의 충돌 해결 규칙이 아니다.'],
 'R07-S': [
  '민감 통계의 사전 접근과 보안 책임이다. 구/신 표현 생성 진리표나 새 필드 불변성은 없다.',
  '대체교통 접근성 예외와 승인이다. 두 표현 일치 검증·불변성·구 표현 갱신 무시에 대응하지 않는다.',
  '노선 유형별 성과 비교·주기 갱신과 비용이다. 정적인 객체 값의 권위·불변성을 규정하지 않는다.'],
 'R07-R': [
  '더 나은 자료로 이전 추정치를 수정하는 신뢰성 개념이다. 같은 객체의 새 필드를 불변으로 두는 매핑과 방향이 다르다.',
  '감축 우선순위 표와 노선 재편 정의다. 버전별 표현 권위와 backfill 진리표는 없다.',
  '재원 회복 시나리오의 가정이다. old/new 표현의 동일값 검증·권위·불변 동작은 없다.'],
 'R08-S': [
  '노선 수 등을 시나리오에서 고정했으나 시간·운행량은 달라진다. 기능 동일성 보존을 입증하는 기본값 활성화 절이 아니다.',
  '불균형 영향·부담의 분석 기준이다. 기존 기능을 그대로 기본 활성화하는 상태 변화는 없다.',
  '대출 상태·수령점·기간 규칙이다. 기능을 바꾸지 않는 기본값 전환과의 대응은 없다.'],
 'R08-R': [
  '노선 복구·확장에 동일 정책 목표를 적용한다. 목표가 같다는 사실은 작동/기능이 같다는 증거가 아니다.',
  '다른 기관 서비스가 기존 노선을 대신하고 자원을 재배치한다. 같은 기능의 기본값만 켜는 변화와 다르다.',
  '대출 수령점 변경 마감과 기간이다. 기존 기능의 기본 활성화 원리는 반환하지 않는다.']
}


def evidence_ranges(judgment):
    return judgment['provider_evidence_line_ranges']


def generate():
    inputs = {x['recipient_id']:x for x in readjl('inputs.jsonl')}
    corpus = {x['candidate_id']:x for x in readjl('corpus.jsonl')}
    primary=[]
    for field in FIELDS:
        rows=readjl(f'judgments/{field}.jsonl')
        assert len(rows)==48, (field,len(rows))
        primary += [(row,f'judgments/{field}.jsonl:{i}') for i,row in enumerate(rows,1)]
    judgments = {x['pair_id']:(x,origin) for x,origin in primary}
    assert len(judgments)==144
    expected={f'{r}-{c}' for r in inputs for c in corpus}
    assert set(judgments)==expected
    ranks=list(csv.DictReader((ROOT/'rankings.csv').open()))
    assert len(ranks)==288
    rank_index={(r['recipient_id'],r['route'],r['candidate_id']):r for r in ranks}
    returns=readjl('returns.jsonl')
    assert len(returns)==16
    window_rows=[]
    for run in returns:
        key=run['recipient_id']+'-'+run['route']
        for d,note in zip(run['returned_documents'],WINDOW_NOTES[key],strict=True):
            rid=run['recipient_id'];cid=d['candidate_id'];j,_=judgments[rid+'-'+cid]
            w=d['window'];body=unicodedata.normalize('NFC',(REPO/corpus[cid]['cache_text_path']).read_text()).lower()
            start=w['lowercase_normalized_char_start_0based'];end=w['lowercase_normalized_char_end_exclusive']
            snippet=body[start:end]
            assert sha256(snippet.encode()).hexdigest()==w['normalized_window_sha256']
            lines=body.splitlines(keepends=True);offsets=[0]
            for line in lines:offsets.append(offsets[-1]+len(line))
            covered=[];missing=[]
            for a,b in evidence_ranges(j):
                # Whole cited lines are conservative evidence units; mere line
                # overlap is never evidence that a cut sentence was returned.
                lo=offsets[a-1];hi=offsets[b]
                while lo<hi and body[lo].isspace():lo+=1
                while hi>lo and body[hi-1].isspace():hi-=1
                (covered if start<=lo and hi<=end else missing).append([a,b])
            strict=j['judgment']=='support' and not missing
            window_rows.append({'return_id':f'{rid}-{run["route"]}-{d["rank"]}',
                'pair_id':rid+'-'+cid,'recipient_id':rid,'route':run['route'],'rank':d['rank'],
                'candidate_id':cid,'provider_url':d['url'],'window_id':w['window_id'],
                'window_sha256':w['normalized_window_sha256'],'line_start':w['text_line_start_1based'],
                'line_end':w['text_line_end_1based'],'char_start':start,'char_end_exclusive':end,
                'document_judgment':j['judgment'],'strict_citation_complete':strict,
                'fully_contained_provider_evidence_ranges':covered,'not_fully_contained_provider_evidence_ranges':missing,
                'read_observation':note,'checked_scope':'Original exact window, root direct read; no document expansion counted.',
                'whole_document_may_have_other_evidence':True})
    assert len(window_rows)==48
    windex={(r['recipient_id'],r['route'],r['candidate_id']):r for r in window_rows}
    maps=[]
    for pair in sorted(judgments):
        j,origin=judgments[pair];rid=j['recipient_id'];cid=j['candidate_id'];inp=inputs[rid];doc=corpus[cid]
        mids=inp['frozen_partial_target']['mandatory_predicate_ids']
        assert {m['predicate_id'] for m in j['mandatory_evidence']}==set(mids),(pair,mids)
        assert j['judgment'] in LABELS
        if j['judgment']=='support':
            assert all(m['status']=='match' for m in j['mandatory_evidence'])
            assert not j['new_core_required']
        date=doc.get('publication_or_version_date')
        temporal='unverified' if not date else ('available' if date<inp['created_at'][:len(date)] else 'later_fixed_edition')
        r={'pair_id':pair,'recipient_id':rid,'recipient_source_id':inp['initial_source_id'],
            'candidate_id':cid,'provider_source_id':doc['source_id'],'provider_field':doc['field'],
            'judgment':j['judgment'],'whole_design_judgment':j['whole_design_judgment'],
            'judgment_origin':origin,'recipient_url':inp['immutable_source_url'],'provider_url':doc['url'],
            'frozen_partial_objective':inp['frozen_partial_target']['objective'],
            'mandatory_predicate_ids':js(mids),'mandatory_evidence':js(j['mandatory_evidence']),
            'recipient_locations':js(j['recipient_locations']),'provider_locations':js(j['provider_locations']),
            'provider_evidence_line_ranges':js(j['provider_evidence_line_ranges']),
            'input_map':js(j['input_map']),'state_change_map':js(j['state_change_map']),
            'output_map':js(j['output_map']),'role_map':js(j['role_map']),
            'preconditions_exceptions':js(j['preconditions_exceptions']),
            'remaining_glue':js(j['remaining_glue']),'new_core_required':js(j['new_core_required']),
            'break_condition':j['break_condition'],'historical_fixed_edition_status':temporal,
            'provider_fixed_version_date':date or '', 'novelty':js(j['novelty']),
            'unverified_and_next_evidence':js(j['unverified_and_next_evidence'])}
        for route in ('S','R'):
            rr=rank_index[rid,route,cid];ww=windex.get((rid,route,cid))
            for col in ('rank','score','returned_top1','returned_top3','best_window_id','window_line_start','window_line_end','window_sha256'):
                r[route+'_'+col]=rr[col]
            r[route+'_strict_citation_complete']=bool(ww and ww['strict_citation_complete'])
            r[route+'_window_read_observation']=ww['read_observation'] if ww else 'Not in the original top 3; no returned-window claim.'
        maps.append(r)
    stats=[]
    for rid in sorted(inputs):
        m=[x for x in maps if x['recipient_id']==rid]
        count={label:sum(x['judgment']==label for x in m) for label in LABELS}
        assert sum(count.values())==18
        stat={'recipient_id':rid,'candidate_counts':count,'strict_eligible_candidates':[x['candidate_id'] for x in m if x['judgment']=='support'],
            'historical_strict_eligible_candidates':[x['candidate_id'] for x in m if x['judgment']=='support' and x['historical_fixed_edition_status']=='available'],
            'broad_eligible_candidates':[x['candidate_id'] for x in m if x['judgment'] in ('support','partial')],
            'searches':2,'scored_documents':36,'returned_slots':6,'full_list_comparisons':18,
            'unique_returned_candidates':len({r['candidate_id'] for r in window_rows if r['recipient_id']==rid})}
        for route in ('S','R'):
            stat[route]={}
            for k in (1,3):
                strict=[x['candidate_id'] for x in m if int(x[route+'_rank'])<=k and x[route+'_strict_citation_complete']]
                docstrict=[x['candidate_id'] for x in m if int(x[route+'_rank'])<=k and x['judgment']=='support']
                broad=[x['candidate_id'] for x in m if int(x[route+'_rank'])<=k and x['judgment'] in ('support','partial')]
                stat[route][f'top{k}']={'strict_citation_ids':strict,'strict_document_ids':docstrict,'broad_document_ids':broad}
        stats.append(stat)
    variants=[]
    for name,exclude in [('all',None),('exclude_R01','R01'),('exclude_R03','R03'),('exclude_R04','R04'),('exclude_R08','R08'),('exclude_query_author_exposure',None),('opening_verified_only',None)]:
        selected=[s for s in stats if s['recipient_id']!=exclude]
        variants.append({'variant':name,'recipient_denominator':len(selected),
            'strict_top1_S':sum(bool(s['S']['top1']['strict_citation_ids']) for s in selected),
            'strict_top1_R':sum(bool(s['R']['top1']['strict_citation_ids']) for s in selected),
            'strict_top3_S':sum(bool(s['S']['top3']['strict_citation_ids']) for s in selected),
            'strict_top3_R':sum(bool(s['R']['top3']['strict_citation_ids']) for s in selected),
            'broad_top1_S':sum(bool(s['S']['top1']['broad_document_ids']) for s in selected),
            'broad_top1_R':sum(bool(s['R']['top1']['broad_document_ids']) for s in selected),
            'broad_top3_S':sum(bool(s['S']['top3']['broad_document_ids']) for s in selected),
            'broad_top3_R':sum(bool(s['R']['top3']['broad_document_ids']) for s in selected),
            'strict_full_list_eligible_questions':sum(bool(s['strict_eligible_candidates']) for s in selected)})
    counts={l:sum(m['judgment']==l for m in maps) for l in LABELS}
    summary={'method':'Frozen queries and BM25 rankings; original primary semantic readings; exact-window evidence separate.',
        'input_sha256':digest(ROOT/'inputs.jsonl'),'corpus_sha256':digest(ROOT/'corpus.jsonl'),
        'rankings_sha256':digest(ROOT/'rankings.csv'),
        'judgment_sha256':{f:digest(ROOT/f'judgments/{f}.jsonl') for f in FIELDS},
        'recipients':8,'candidate_documents':18,'original_searches':16,'scored_document_rows':288,
        'returned_slots':48,'empty_searches':sum(r['empty_result'] for r in returns),
        'unique_candidate_window_pairs':len({(r['candidate_id'],r['window_id']) for r in window_rows}),
        'pair_count':144,'mandatory_evidence_count':sum(len(j['mandatory_evidence']) for j,_ in judgments.values()),
        'counts':counts,'whole_design_support':sum(m['whole_design_judgment']=='support' for m in maps),
        'per_recipient':stats,'sensitivities':variants,
        'historical_candidate_counts':dict(Counter(m['historical_fixed_edition_status'] for m in maps)),
        'historical_candidate_ids':sorted({m['candidate_id'] for m in maps if m['historical_fixed_edition_status']=='available'}),
        'strict_all_list_support_pairs':[m['pair_id'] for m in maps if m['judgment']=='support'],
        'strict_both_missed_pairs':[m['pair_id'] for m in maps if m['judgment']=='support' and m['S_returned_top3']=='False' and m['R_returned_top3']=='False'],
        'strict_citation_complete_slots':sum(x['strict_citation_complete'] for x in window_rows),
        'no_user_adoption_or_open_web_performance_inference':True}
    stream=io.StringIO(newline='');writer=csv.DictWriter(stream,fieldnames=list(maps[0]),lineterminator='\n');writer.writeheader();writer.writerows(maps)
    return {'maps.csv':stream.getvalue(),
        'evidence/returned-window-audit.jsonl':''.join(js(x)+'\n' for x in window_rows),
        'evidence/recount.json':json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True)+'\n'}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    products=generate()
    for name,content in products.items():
        if args.check:
            assert (ROOT/name).read_bytes()==content.encode(),f'Regenerated product differs: {name}'
        else:
            (ROOT/name).write_text(content)
    summary=json.loads(products['evidence/recount.json'])
    print(js({'mode':'check' if args.check else 'write','counts':summary['counts'],
        'pairs':summary['pair_count'],'mandatory':summary['mandatory_evidence_count'],
        'strict_citation_slots':summary['strict_citation_complete_slots'],
        'products':list(products)}))
