#!/usr/bin/env python3
"""Serialize the root's manual Q7 judgments; this does not infer judgments from labels."""
import copy, json
from pathlib import Path
from collections import Counter
BASE=Path(__file__).resolve().parents[1]
U={x['unit_id']:x for x in json.loads((BASE/'sample/units.json').read_text())['units']}
D={x['unit_id']:x for x in json.loads((BASE/'evidence/disagreements.json').read_text())['rows']}
SEL=json.loads((BASE/'evidence/impact-selection.json').read_text())['unit_ids']
ROWS=[]

def add(uid,H,T,decision,near,reason,challenge,next_check,extra=None):
    """H is a manually authored list of (condition, status, reason)."""
    common={'H':[dict(zip(('condition','status','reason'),v)) for v in H],
            'T':T,'overall_004_label':decision,'near_miss':near}
    ROWS.append({'unit_id':uid,'sample':U[uid]['sample'],'role_a':{k:D[uid]['a'][k] for k in ('S1','S2','S3')},
     'role_b':{k:D[uid]['b'][k] for k in ('S1','S2','S3')},
     'unit_fixed':'동결 packet의 problem/constraints/proposal/configuration/candidate_description. 빈 proposal이나 설정은 미제공 그대로 두며 전체 대체 주장을 새로 만들지 않는다.',
     'assessment_level':'H: 작업자의 사후 문서 기반 판단; 004-R03의 고정 EXPECTED와 제한된 toy 실행은 별도 표시',
     'judgment_a':copy.deepcopy(common),'judgment_b':copy.deepcopy(common),'label_only_changed':False,
     'reason':reason,'counterargument_examined':challenge,'minimum_next_check':next_check,
     'evidence_locations':['sample/units.json#'+uid,'evidence/disagreements.json#rows[unit_id='+uid+']',
       'AF-RES-004@2b798c7d2b7355b649691c18de196104ceabb0f0/PROTOCOL.md#판정 단위와 증거 경계; 네 판단축']+(extra or [])})

add('004-R03',[
 ('P01-H1','pass','주어진 로컬 JSON 변경 구성은 네트워크를 필요로 하지 않는다.'),
 ('P01-H2','unknown','patch log 보존 외에 초기 snapshot/replay 복구 경로가 제공되지 않았다.'),
 ('P01-H3','fail','동일 경로의 서로 다른 replace는 도착 역순에서 서로 다른 결과가 된다.')],
 'not_needed','SURFACE_OR_CONSTRAINT_MISMATCH','known',
 'standard/pattern 명명 어느 쪽도 공통 순서나 병합 알고리즘을 추가하지 않는다. 고정 004 기대판정과 같은 실패다.',
 '표준이라는 형태가 수렴 보증을 암시하는지 반박했다. RFC는 순차 적용을 정의할 뿐 임의 순서 수렴을 말하지 않는다.',
 '본문 복원 H2는 snapshot과 replay 입력을 추가해 확인; H3는 현재 구성의 실패를 유지한다.',
 ['I03 RFC 6902 §3, §4.3','evidence/toy-counterexamples.json#json_patch_order','004 EXPECTED.json R03'])
add('011-T010-002',[
 ('반응형 웹·DB·안전한 결제','unknown','프레임워크 이름과 학습 경로만으로 결제 안전성·연결 구성은 확인되지 않는다.')],
 'not_needed','INSUFFICIENT','not_established',
 'mixed/part와 framework/whole 모두 패킷의 안전한 결제 요구를 pass로 바꾸지 못한다.',
 'part라는 이유로 결제 요구를 지우는 해석을 배제했다. UI 층만 선택하려면 별도의 좁힌 사용 행이 필요하다.',
 '결제 경로·인증·DB 연결을 포함한 제안 구성 한 개를 명시한다.')
add('011-T011-005',[], 'not_needed',None,'not_established',
 '앱인지 실행 형태가 미상인지의 차이는 변경 감지 도구의 같은 제안을 바꾸지 않는다. 안정성은 prefer이며 검증되지 않았다.',
 'OpenBSD 사용 중이라는 사실을 모든 후보의 필수 OS 조건으로 자동 승격하지 않았다.',
 '실행 형태와 실제로 필요한 OS·알림 조건을 명시한다.')
add('011-T011-007',[], 'not_needed',None,'not_established',
 'app/service 차이는 같은 영역 감시·이력 후보의 역할 표시 차이다. 내부망 불가는 현재 명시된 must 위반이 아니다.',
 '내부망 사용 요구가 없는데 내부망 불가만으로 근접 오답이라고 판정하는 반례를 기각했다.',
 '감시 대상이 내부망인지와 안정성 비교 관측을 제공한다.')
add('011-T027-002',[
 ('별도 서버 예산 없음','unknown','DB 파일 또는 서비스의 클라이언트 배치·조회 방식이 없다.'),
 ('국가별 자동 판매 제한','unknown','IP 국가 데이터에서 실제 판매 제한까지의 연결은 제공되지 않는다.')],
 'not_needed','INSUFFICIENT','not_established',
 '국가 변환 범위를 whole로 볼지 데이터 층을 part로 볼지 달라도 제공되지 않은 연결을 pass로 채우지 않는다.',
 '원문 요약은 입력을 좌표로 한정하지 않는다. 좌표 대 IP의 실패를 확정하거나 part라서 판매 제한을 삭제하지 않았다.',
 '위치 입력형·클라이언트 조회·판매 제한 동작을 한 사용 시나리오로 명시한다.')
add('011-T036-005',[], 'not_needed',None,'not_claimed',
 '교체·관리 비용을 보는 동일 조언이 reference/comparison으로 갈린다. 비용 절감이 입증됐다는 주장은 없다.',
 '평가 기준이라는 라벨이 실제 비용 비교 실험을 대신할 수 있는지 검토하고 배제했다.',
 '실제 후보 두 개의 개발·교체·관리 비용 관측이 있어야 효과를 판정한다.')
add('011-T036-008',[], 'not_needed',None,'not_claimed',
 '변동성·신뢰 기준과 API 격리·통합 테스트는 함께 제시되어 있다. reference/mixed 어느 쪽도 실행 안의 보안 보증은 아니다.',
 'mixed를 선택했다고 후보 두 개에 대한 효과가 각각 검증된 것으로 읽지 않았다.',
 '평가 기준과 구현 조언의 주·보조 관계 및 적용 사례를 명시한다.')
add('011-T036-014',[], 'not_needed',None,'not_claimed',
 '기회비용·유지비 비교라는 동일 방법의 명명만 다르다. must 조건이나 수치 관측이 없는 데서 H pass를 만들지 않는다.',
 '비교 방법 제시와 비교 결과 입증을 구별했다.',
 '동일 프로젝트의 직접 구현·라이브러리 사용 두 비용 기록을 확보한다.')
add('011-T036-022',[], 'not_needed',None,'not_claimed',
 '약 한 시간 휴리스틱을 설계 참고나 비교 문턱으로 읽어도 그 문턱의 효과는 미검증이다.',
 '암호 라이브러리 선택에도 한 시간 기준이 충분하다는 확대 적용을 검토했으나 패킷에 뒷받침이 없다.',
 '보안 중요도와 유지 기간이 다른 실제 사례에서 문턱의 실패를 관측한다.')
add('011-T036-026',[], 'not_needed',None,'not_claimed',
 '기능·플랫폼·라이선스·가격을 고려하라는 같은 항목 목록이다. 구체 제품의 충족 판정은 어느 라벨에도 없다.',
 '평가 항목의 존재를 해당 항목에 합격한 후보의 존재로 읽는 것을 배제했다.',
 '특정 후보·버전·필수 조건을 연결한 평가 행을 만든다.')
add('011-T036-028',[], 'not_needed',None,'not_claimed',
 '도구 이름 묶음인지 경험에서 얻은 방법인지 달라도 추상화 수준을 바꾼 사례를 참고하는 범위는 같다.',
 'pdf.js 직접 조합 경험을 새 암호 문제의 적합성 증명으로 옮길 구체 관계는 없다.',
 '어떤 선택 문제의 어느 비용·제약에 경험을 옮기는지 연결을 명시한다.')
add('011-T039-009',[
 ('오픈소스','unknown','SQLite라는 이름 외에 제안한 큐 구현체와 배포 조건이 없다.'),
 ('ZooKeeper를 운영하지 않음','unknown','SQLite 테이블 구현 제안이지만 전체 큐 구성·의존성은 주어지지 않았다.')],
 'unknown','INSUFFICIENT','not_established',
 'library/whole과 pattern/reference는 실행 대상과 방법의 경계 차이다. 현재 입력은 어느 쪽에도 완성 큐나 claim/ack 설계를 제공하지 않는다.',
 'reference로 바꾸면서 OSS·운영 제약을 not_in_scope로 삭제하지 않았다. 구체 직접 사용인지 전이인지부터 불명확하다.',
 '실행할 큐 구현체 또는 메시지↔행·claim/ack·중단 후 재처리 설계를 제공한다.')
add('011-T041-005',[], 'not_needed',None,'not_established',
 '같은 탐색원을 document/data로 분류했다. 현행·풍부함은 prefer이며 링크 추천만으로 확인되지 않는다.',
 'component이므로 전체 탐색원 대체 후보에서 탈락시켜야 한다는 추론을 배제했다. S2 whole에는 양쪽이 동의한다.',
 '목록의 최근 갱신 시점과 필요한 주제의 항목 범위를 확인한다.')
add('011-T041-009',[], 'not_needed',None,'not_established',
 '뉴스레터와 목록을 document 또는 mixed로 묶어도 동일한 정보원을 탐색에 쓰는 제안이다.',
 '형태가 여러 개라는 이유로 최신성·풍부함이 더 높다고 평가하지 않았다.',
 '각 정보원의 최신성과 문제에 필요한 범위를 별도로 확인한다.')
add('011-T041-011',[], 'not_needed',None,'not_established',
 '기존 목록 위치 안내를 document/data 중 어디에 놓아도 안내되는 대상과 문제는 같다.',
 '서브레딧 위치 설명을 기능 구현이나 완전한 OSS 검색기로 확대하지 않았다.',
 '연결된 목록의 실제 범위와 갱신 시점을 확인한다.')
add('011-T047-005',[], 'not_needed',None,'not_claimed',
 'NATS 복잡도 전제에 대한 비판은 reference/comparison 양쪽에서 선택 정보다. 신뢰성 요구의 구체 값이 없어 구현 H는 아직 만들 수 없다.',
 '복잡성이 prefer이고 신뢰성 force가 unclear인 패킷을 004의 1시간 복구 조건으로 바꾸지 않았다.',
 '요구 전달 보장과 복잡성의 관측 기준을 명시한다.')
add('011-T047-018',[], 'unknown','INSUFFICIENT','not_established',
 '기존 Postgres가 있다는 전제도 실행 큐 확장도 구체적으로 주어지지 않는다. component/whole이나 principle/reference로 이름 붙여도 큐 보장을 확인할 수 없다.',
 'method를 완성 실행 부품으로 읽는 경우와 DB 관계를 옮기는 경우는 별도 가정이다. 원 패킷에 없는 구현을 추가하지 않았다.',
 '기존 Postgres 유무, 큐 구현체·설정, 필요한 전달 보장을 제시한다.')
add('011-T047-023',[], 'unknown',None,'not_claimed',
 '성장 단계별 후보 묶음과 선택 방법 중 무엇을 대상에 두는지 다르지만 현재 단계·부하·보장 값은 없다.',
 '여러 제품 이름이 나타났다고 현재 요구에 맞는 한 실행안이 검증되었다고 하지 않았다.',
 '현재 단계와 실제로 채택할 도구·설정을 선택해 별도 행으로 평가한다.')
add('011-T047-032',[], 'not_needed','INSUFFICIENT','not_established',
 'PostgreSQL의 pub/sub를 component/product로 달리 봐도 같은 service를 whole로 쓰는 해석은 일치한다. 신뢰성 요구·설정은 미제공이다.',
 'product라는 이유로 내구 메시지 보장을 자동 승인하거나 component라는 이유로 제외하지 않았다.',
 '필요한 전달 보장·중단 시나리오·구체 PostgreSQL 기능과 버전을 제시한다.')
add('011-T047-045',[], 'not_needed',None,'not_claimed',
 '요구 확인·측정 우선이라는 설계 참고는 일치하고, 도구 예시를 mixed로 셀지만 다르다.',
 '후회한 도입 경험을 모든 RabbitMQ 사용의 실패나 모든 Postgres 사용의 성공으로 일반화하지 않았다.',
 '질문의 규모·보장 값을 측정한 뒤 한 구성을 특정한다.')
add('011-T047-054',[], 'unknown','INSUFFICIENT','not_established',
 '회사에서 Kafka를 썼다는 경험만으로 현재 문제에서 대체·비교·설계 참고 중 무엇을 하려는지 확정되지 않는다.',
 'whole 해석만으로 과거 회사 사용이 현재 문제 충족을 입증한다고 하지 않았다.',
 '경험의 적용 대상과 현재 질문에 권하는 사용 방식을 한 문장으로 복원한다.')
add('011-T047-062',[], 'not_needed',None,'not_claimed',
 '역사적 복제 부재 주장을 참고 경고나 제품 비교로 읽어도 현재 문제의 필수 복제 조건은 주어지지 않았다.',
 '과거 발화를 현재 Iggy 버전의 기능 사실 또는 004 P02 복구 H 위반으로 승격하지 않았다.',
 '대상 버전과 실제 요구 복제·중단 조건을 먼저 고정한다.')
add('011-T048-002',[
 ('7디스크 RAID5와 자동 scrub/복구','unknown','당시 단일 디스크 추가 제한 설명만으로 요구 저장 구성의 충족 여부를 알 수 없다.')],
 'not_needed','INSUFFICIENT','not_established',
 '제약 설명을 pattern으로 보든 ZFS를 library로 보든 원 요구 충족 근거가 늘지 않는다.',
 '단일 디스크 증설은 현재 입력의 must가 아니며 과거 제약 설명을 현재 버전 사실로 일반화하지 않았다.',
 '버전·7디스크 구성·scrub와 복구 경로를 명시한다.')
add('011-T053-002',[
 ('현재 라이브러리와 같은 목적','unknown','기존 목적과 후보의 기능 비교가 없다.'),
 ('활발한 유지보수','unknown','README 링크·사용 권유는 유지보수 관측이 아니다.')],
 'not_needed','INSUFFICIENT','not_established',
 'component/library와 unknown/unknown의 형태 차이는 두 필수 조건의 정보 부족을 해소하지 못한다.',
 '라이브러리 이름을 알아봤다는 것이 동일 목적·유지보수 검증이라는 해석을 배제했다.',
 '비교 기능 목록과 고정 관측 기간의 유지보수 기록을 제공한다.')
add('011-T054-003',[
 ('라벨 대신 회로 선 연결','unknown','사용 인상과 설정 조언에는 동일 과제의 확인 결과가 없다.'),
 ('PCB 배선 생성','unknown','정식 시험이 아니라는 요약이며 출력물 검증이 없다.')],
 'not_needed','INSUFFICIENT','not_established',
 '모델·설정 묶음을 mixed로 보든 모델 자료를 whole로 보든 KiCAD 과제 충족 근거는 같다.',
 '로컬 실행은 prefer이고 모델 사용 인상은 두 must에 대한 시험이 아니라는 구분을 유지했다.',
 '동일 입력 회로·도구 집합·설정에서 선 연결과 PCB 출력 결과를 검증한다.')
add('012-origami-solar',[
 ('재연결·반복 worker 중단 뒤 메시지 재처리','unknown','접기 시제품 설명에는 메시지 상태·재전달과의 대응이 없다.')],
 'unknown','INSUFFICIENT','not_established',
 'research/document 차이는 우연 연결된 메시지 질의와 후보 사이에 없는 사용 관계를 만들어 주지 않는다. 양쪽 모두 S2 none이다.',
 '접기 전이가 한 번 성공했다는 사례를 모든 분야 전이의 mapped 증거로 읽지 않았다. 단순 무관련과 알려진 근접 오답도 구별했다.',
 '관련성을 주장하려면 접기 구조와 메시지 복구 관계의 대응·실패 조건을 별도로 제시한다.')
add('012-otel-wal',[
 ('새 별도 broker를 운영하지 않음','pass','제공 설명은 Collector 로컬 file_storage 구성이며 별도 broker 없는 사용을 명시한다.')],
 'not_needed','INSUFFICIENT','not_established',
 '금지 조건 하나의 문서상 pass는 양쪽에서 같다. whole/unknown 차이가 있어도 이루려는 양의 목표가 없으므로 전체 적합성은 확정할 수 없다.',
 'broker 금지라는 음의 조건에서 손실 없는 재전송 목표와 무제한 queue를 임의 복원하지 않았다.',
 '상위 질문의 목표·10분 중단 여부·queue/retry/디스크 조건을 복원한다.')
add('012-pg-wal',[
 ('이전 파일 판을 선택해 복원','unknown','DB 전용 WAL의 설명만 있고 파일 백업 대상의 baseline·보존·redo 연결은 없다.')],
 'analogy_only','INSUFFICIENT','not_established',
 'service/library 차이에도 reference 기여는 같다. 선기록·복구의 일반 관계에서 파일 백업 설계로 가는 대응이 미완성이다.',
 'WAL이라는 이름이 임의 파일의 이전 판 복원 도구임을 뜻하지 않는다. 원문에 없는 bridge를 mapped로 채우지 않았다.',
 '파일 baseline·변경 이력·보존 정책·복원 알고리즘의 대응과 실패 조건을 제시한다.')
add('012-pypi-aiolimiter',[
 ('대기 최대 8 / 처리 중 최대 4','unknown','실제 사용 제안과 큐·완료 기반 동시 제한 설정이 없다. 처리율 인터페이스만으로 보장할 근거는 없다.')],
 'not_needed','INSUFFICIENT','not_established',
 'part/none 차이는 투입률을 어느 정도 기여로 인정할지다. 비어 있는 proposal을 단독 전체 보장 주장으로 바꾸지 않았다.',
 '단독 limiter가 상한을 보장한다는 별도 가정은 I02와 toy에서 반례가 생긴다. 그러나 그 가정을 원 후보 추천의 실제 주장으로 소급하지 않는다.',
 'limiter의 단독/보조 사용 여부와 완료 기반 permit·유한 queue 구성을 명시한다.',
 ['I02 Typical use/Bursting/API','evidence/toy-counterexamples.json#rate_not_concurrency'])
add('012-pypi-opentelemetry-exporter-otlp',[
 ('Collector 외부 전송의 10분 장애·재시작 손실 감소','unknown','Python exporter의 이름·요약은 Collector queue와 재시작 저장 구성을 입증하지 않는다.'),
 ('새 별도 broker 금지','unknown','실제 도입 구성 자체가 제공되지 않았다.')],
 'not_needed','INSUFFICIENT','not_established',
 'part/none을 어느 쪽으로 정해도 선택 구간은 Collector 이후이고 내구 전송 설정은 없다. I01은 SDK→OTLP endpoint와 Collector 후단 설정의 구분을 확인한다.',
 '제목의 Collector용이라는 말만으로 Collector 내부 exporter라고 확정하지 않았다. 단독 전체 대체로 읽을 경우의 범위 위반은 새 주장에 대한 판정이다.',
 '송신자·수신자·실행 위치와 Collector queue/storage 설정을 명시한다.',
 ['I01 OTLP Collector Setup/Dependencies/Usage'])

assert [r['unit_id'] for r in ROWS]==SEL
assert all(r['unit_id'] in D for r in ROWS)
assert len({r['unit_id'] for r in ROWS})==30
# The following contrasts are explicitly new hypothetical units, not recoded observed cases.
variants=[]
for uid in ('011-T039-009','011-T047-018'):
 variants.append({'original_unit_id':uid,'level':'H','included_in_main_change_rate':False,
  'role_interpretation_a':'이미 실행 가능한 큐 부품과 인터페이스를 제공하며 직접 사용한다는 추가 가정',
  'role_interpretation_b':'DB 테이블 관계를 새 큐 설계로 옮기자는 참고이고 메시지↔행, claim/ack, 중단 후 재처리 대응이 없는 추가 가정',
  'a_T':'not_needed','b_T':'analogy_only','conditional_T_change':True,
  'H_rule':'원래 필수 조건은 양쪽에 보존. 가정만으로 H pass나 DIRECT_DOCUMENTED를 부여하지 않는다.',
  'causal_limit':'추가 가정이 proposed_use/제공 근거를 바꾸므로 역할명만의 효과가 아니다. 원 packet의 T unknown을 소급 교정하지 않는다.',
  'next_check':'실제 제안자가 실행 큐를 지시했는지 설계 원리를 지시했는지 원 응답의 사용 문장을 확인한다.'})
obj={'study':'AF-RES-016','author':'작업자 GPT-6 Astra Pro','human':False,
 'serialization_note':'사례별로 두 역할의 의미와 요구·근거를 대조한 뒤 공통 수기 판단을 양쪽 표시값에 복사한다. 두 H/T를 독립적으로 재코딩한 실험이 아니며 0/30은 이 판정 불변성 감사의 값이다.',
 'method':'동결 후 59개 불일치 ID를 정렬해 30개를 균등 간격으로 선택. 각 입력·A/B 이유를 직접 읽고 동일 사용·근거 아래 H/T 및 근접 오답을 수기로 검토. 이 파일의 A/B 판단은 원 코더에게 재질문한 답이 아니라 작업자가 작성한 조건부 판정이다.',
 'source_role':'011/012는 고정 연구자의 요약을 사용하며 원 추천의 사실 진위를 다시 코딩한 것이 아니다. Q7 후속 I01–I03은 양쪽에 동일 제공한 문서 확인이며 원 S1/S2/S3에 반영하지 않았다.',
 'H_empty_rule':'H=[]는 must가 제공되지 않았거나 force=unclear라서 004 H 조건을 새로 만들지 않았다는 뜻이다. 모든 H 통과 또는 유용성 승인이라는 뜻이 아니다.',
 'overall_null_rule':'overall_004_label=null은 전체 판정 라벨 미부여다. 15개 중 조언/비교 10개와 필수 판정 기준이 부족한 실제 대안 제안 5개(T011-005/007,T041-005/009/011)를 구별한다. 제안 없음 또는 모든 H 통과를 뜻하지 않으며 새 판정 어휘도 아니다.',
 'near_miss_rule':{'known':'명시 사용의 알려진 결정적 위반','not_established':'근접 오답이라는 증거 미충족; 적합 판정 아님','not_claimed':'구체 전체 충족 주장이 없는 조언; 역할만으로 N을 만들지 않음'},
 'summary':{'reviewed_unique_disagreements':len(ROWS),'label_only_judgment_changes':sum(r['label_only_changed'] for r in ROWS),
  'known_mismatch_cases':sum(r['judgment_a']['near_miss']=='known' for r in ROWS),
  'insufficient_cases':sum(r['judgment_a']['overall_004_label']=='INSUFFICIENT' for r in ROWS),
  'overall_label_not_assigned_cases':sum(r['judgment_a']['overall_004_label'] is None for r in ROWS),
  'unassigned_advice_or_comparison_cases':10,'unassigned_alternative_missing_must_criteria_cases':5,
  'conditional_new_use_T_contrasts':len(variants),'conditional_contrasts_counted_as_observed_changes':0},
 'limits':['0/30은 통제된 문서 재판정의 라벨 불변성이다. 실제 사람의 화면 표시 효과 또는 전체 59개의 무영향 확률이 아니다.',
 '많은 행은 근거·필수 판정 기준이 부족하거나 비교 조언이다. 그대로 유지된 unknown을 충분한 정보가 있는 부정 결과와 합쳐 역할 불일치가 항상 무해하다고 할 수 없다.',
 'T 대비 두 개는 연구자가 추가한 사용 해석의 가정이며 실제 제안 의도를 확인한 판정 변화가 아니다.',
 '후속 내부 별도 검토는 오판 위험 검토일 뿐 인간 또는 타 모델 독립 재판정이 아니다.'],
 'rows':ROWS,'new_use_hypotheses':variants}
(BASE/'evidence/impact.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(obj['summary'],ensure_ascii=False))
