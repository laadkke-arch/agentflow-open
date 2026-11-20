"""Researcher-authored extraction; external full texts are not stored.

Run only within this directory. Output is evidence/cases-ps/draft-cases.json and
sources.json; the root agent integrates these after committing all prefixes.
"""
import json
from pathlib import Path
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
HIST = json.loads((HERE / 'history-metadata-complete.json').read_text())
if (HERE/'history-P386.json').exists():
    HIST.update(json.loads((HERE/'history-P386.json').read_text()))
DATES = {r['sha']: r['date'] for rows in HIST.values() for r in rows}
NOW = datetime.now(timezone.utc).isoformat()
ROLE_DESIGN = '같은 분야의 다른 설계'
ROLE_PART = '재사용 부품'
ROLE_ECO = '다른 언어·생태계'
cases = []
sources = []

def source(sid, url, typ, title, ver, sections, confirmed, limits, level='D1', used=None):
    row = dict(id=sid, url=url, accessed_at_utc=NOW, source_type=typ,
               title=title, version_or_date=ver, sections_read=sections,
               confirmed=confirmed, limits=limits, level=level,
               used_in=used or ['Q1','Q2','Q3','Q4','Q7'], access_note='accessed_at_utc는 이 원문 열람 묶음의 확인·기록 완료 UTC다. 개별 HTTP 최초 열람 시각은 보존하지 않았으며 정밀 시각으로 재구성하지 않았다.')
    sources.append(row)
    return sid

def case(cid, title, prefix_sha, gold_sha, date, event, sections, problem, constraints,
         outcome='accepted', prefix_path=None, gold_path=None, superseded=None,
         date_url=None, gold_sections=None, date_note=None):
    ispy = cid.startswith('P')
    repo = 'python/peps' if ispy else 'swiftlang/swift-evolution'
    path = prefix_path or (f'pep-{int(cid[1:]):04d}.txt' if ispy else '')
    gold_path = gold_path or path
    pu = f'https://raw.githubusercontent.com/{repo}/{prefix_sha}/{path}'
    gu = f'https://raw.githubusercontent.com/{repo}/{gold_sha}/{gold_path}'
    url = f'https://github.com/{repo}/blob/{gold_sha}/{gold_path}'
    histkey = cid[0]+str(int(cid[1:]))
    histurl = f'https://api.github.com/repos/{repo}/commits?path={path}&per_page=100'
    sids = [source('PS-'+cid+'-prefix', pu, 'proposal_historical_draft',title,
                   prefix_sha, sections, problem,
                   '초기 문맥만 확인한다. 결정·대안의 완전성이나 실제 사용자 효용을 증명하지 않는다.'),
            source('PS-'+cid+'-gold', gu, 'proposal_pinned',title,
                   gold_sha, gold_sections or ['Alternatives / Prior Art / Rejected Ideas'],
                   '해당 고정 판에서 명시적으로 비교한 항목과 그 채택·기각·참고 이유를 하나씩 코딩했다. 골드 분절과 역할은 작업자의 판정이다.',
                   '저자·리뷰어가 문서에 남긴 유한 집합이다. 모든 유효 대안의 목록도, 역할 분류 신뢰도의 측정도 아니다.'),
            source('PS-H-'+histkey, histurl, 'repository_history_api', title+' commit history',
                   'live', ['sha, commit.committer.date, parent SHA; path history'],
                   '초기 문맥 판과 결정 상태를 기록한 판의 SHA·UTC 시각을 확인했다. 날짜의 의미는 case.date_evidence에 분리했다.',
                   'Git 반영 시각은 실제 회의·메일 결정 시각과 다를 수 있다. 별도의 공식 결정 기록이 있으면 그것을 우선했다.',
                   'D3-fetch',['Q1','Q2'])]
    row = dict(id=cid, canonical_id=cid, family='Python PEP' if ispy else 'Swift Evolution',
               title=title, url=url, pinned_version=gold_sha,
               decision_date=date, decision_event=event, decision_evidence_url=date_url or histurl,
               decision_outcome=outcome, superseded_by=superseded or [],
               prefix_sections=sections,
               prefix_version=dict(sha=prefix_sha, date=DATES.get(prefix_sha,'unconfirmed'), url=pu,
                                   selection='초기 공개 고정 판의 독립 문제·동기 문단; 해법·대안명·제안번호·링크 제거'),
               gold_version=dict(sha=gold_sha, date=DATES.get(gold_sha,'unconfirmed'), url=gu),
               gold_items=[], mandatory_constraints=constraints, source_ids=sids,
               extraction_performed_by='작업자: 내부 하위 에이전트; GPT-6 Astra Pro; ChatGPT 공유 Linux Cloud workspace',
               date_evidence=dict(decision_date=date, decision_event=event,
                                  official_url=date_url or histurl,
                                  repository_record_sha=gold_sha,
                                  repository_record_utc=DATES.get(gold_sha,'unconfirmed'),
                                  note=date_note or '이 날짜는 공식 저장소에서 상태·결정을 기록한 시점이다. 실제 회의 시각으로 확대 해석하지 않는다.'),
               extraction_exclusions=[], review_scope='본문과 명시한 리뷰만 열람; 전 토론을 전수 조사하지 않았다.')
    cases.append(row)
    return row

def gold(c, name, section, reason, role=ROLE_DESIGN, stance='rejected', url=None,
         review='unknown', boundary='', extra=None):
    item=dict(id=c['id']+'-G'+str(len(c['gold_items'])+1).zfill(2), name=name,
              url=url or c['url'], role=role, stance=stance, reason=reason,
              added_in_review=review, boundary_note=boundary,
              section_anchor=section, match_kind='external_entity' if url else 'structural_design',
              classification_by='작업자', source_ids=['PS-'+c['id']+'-gold'])
    if extra:item.update(extra)
    c['gold_items'].append(item)
    return item

p=case('P0201','Parallel Iteration','be3c33389e2cc8e83b76676eb06d8a403493c169',
       '8a03f9cff101e1e7c63c85a48cb2487e4839574d','2000-08-03',
       '공식 저장소에 BDFL 수락과 최종 API 선택을 기록한 커밋',
       ['Introduction: 대상 환경','Standard For-Loops: 기존 시퀀스 반복 문제','Parallel For-Loops: 목적·기존 관용구의 문제 문단만'],
       '여러 시퀀스의 같은 위치를 함께 순회하는 목적과 기존 관용구의 불명확함·길이 불일치 문제를 확인했다.',
       ['여러 시퀀스의 같은 위치 원소를 함께 처리','기존 시퀀스 반복 문맥에 적용','길이 불일치 동작을 명확히 설명'],
       gold_sections=['Lockstep For-Loops','BDFL Pronouncements'],
       superseded=[dict(type='partial_reversal_after_adoption',url='https://github.com/python/peps/blob/6e249d895555a5e330718a661678ef3827fa708a/pep-0201.txt',
                       pinned_version='6e249d895555a5e330718a661678ef3827fa708a',date='2003-08-02',
                       scope='Python 2.4에서 인수 없는 호출이 TypeError 대신 빈 목록을 반환하도록 변경. 가변 인수 펼침을 이용한 역변환·행열 전치의 빈 입력을 처리한다. 전체 zip 설계의 폐기는 아니다.')])
gold(p,'map(None, ...)', 'Lockstep For-Loops','이미 가능한 같은 위치 결합이지만 특별한 None 인수와 짧은 입력의 None 패딩이 불명확하다.',ROLE_PART,'referenced','https://docs.python.org/2/library/functions.html#map')
gold(p,'for x in seq1, y in seq2 문법','Lockstep For-Loops','이미 다른 의미를 가진 문법이어서 의미를 바꾸면 기존 코드를 깨뜨린다.')
gold(p,'for x, y in seq1, seq2 문법','Lockstep For-Loops','기존 문법 의미와 충돌하고 다른 새 구문과 결합하기 어렵다.')
gold(p,'Haskell zip','BDFL Pronouncements / function name','더 나은 이름에 합의하지 못해 Haskell의 기존 이름을 따랐다.',ROLE_ECO,'referenced','http://www.haskell.org/onlinereport/standard-prelude.html#$vzip',boundary='다른 언어의 기능 및 명명 선례이며 먼 분야 원리는 아니다.',extra={'transfer_form':'term_and_operation','operational_influence':'이름 선택의 명시 근거; 이름만 맞으면 기능 적합을 보장하지 않음'})
gold(p,'선택적 pad 인수','BDFL Pronouncements / Optional padding','가장 짧은 입력에서 종료하는 단순 API를 택했다. 필요할 때 추가하기는 쉽지만 불필요한 인수를 나중에 삭제하기는 어렵다.')
gold(p,'__getitem__ 기반 지연 반환 객체','BDFL Pronouncements / Lazy evaluation','실제 리스트 반환을 택하고 지연 방식은 필요하면 별도 기능으로 추가하도록 미뤘다.')
gold(p,'내부·외부 컨테이너 타입을 호출자가 선택','BDFL Pronouncements / Inner and outer container control','API와 구현을 단순하게 유지하기 위해 제외했다.')
p['extraction_exclusions']=['최종판에서 삭제한 20개 이상의 이름 후보는 이 고정 판의 골드가 아니다.','채택된 무인수 TypeError 동작은 이 시점에 독립 대안과 비교되지 않아 골드 항목으로 소급 추가하지 않았다.']

p=case('P0202','List Comprehensions','8c3a432a609b36308f6d7d58b50ec277bed2ecf2',
       'ff898c8e8a69e31b05873ca8c5fdf88dd6ee9c2f','2000-07-27',
       'BDFL Pronouncements에 구문 수락과 반복 의미를 기록한 커밋',
       ['Rationale: 리스트 생성의 간결함을 요구하는 문제 문장; 비교 함수명은 제거'],
       '반복과 선택으로 새 리스트를 간결하게 만드는 목적을 확인했다. 문제 설명은 한 문장 수준으로 매우 얇다.',
       ['새 리스트 생성에 적용','반복에 따른 원소 생성과 조건 선택 지원'],
       gold_sections=['Rationale','BDFL Pronouncements','Open Issues / Syntax and Semantics'],
       date_note='Draft/Final 헤더 반영과 분리하여 구체적인 BDFL 구문·의미 결정이 추가된 시점을 쓴다.')
gold(p,'map()','Rationale','리스트 생성의 기존 수단으로 비교하며 더 간결한 표현을 제안한다.',ROLE_PART,'referenced','https://docs.python.org/2/library/functions.html#map')
gold(p,'filter()','Rationale','조건에 따라 리스트 원소를 고르는 기존 수단으로 비교한다.',ROLE_PART,'referenced','https://docs.python.org/2/library/functions.html#filter')
gold(p,'명시적 중첩 for 반복문','Rationale; Open Issues / Semantics','생성 결과의 반복 순서를 설명하는 기준이며 마지막 인덱스가 가장 빨리 변한다.',stance='referenced')
gold(p,'괄호 없는 다중 출력식 [x, y for ...]','BDFL Pronouncements','튜플 표현을 괄호로 묶도록 요구하여 파서 부담과 구문 혼동을 줄인다.')
gold(p,'세미콜론으로 절을 분리하는 구문','Open Issues / Syntax','각 절의 경계를 드러내자는 토론 대안이다. 이 고정 판의 Open Issues에는 대안이 남아 있어 별도 최종 기각 이유는 명시되지 않는다.',stance='referenced')
gold(p,'복수 for 절을 같은 위치끼리 병렬 결합하는 의미','Open Issues / Semantics','일부 독자가 예상한 의미와 실제 중첩 의미를 대조한다. 별도 결합 함수가 그 사용례를 담당한다.',stance='referenced')

p=case('P0204','Range Literals','6f232833deb031dd1deb88b4666341872a4aa14d',
       '2ec18ca954c8041761f3891c20c092f03471daa3','2000-11-01',
       '공식 원문에 Rejection 절과 기각 상태를 기록한 커밋',
       ['List ranges: 첫 문제 설명 및 clarity/efficiency 문단; 해결 문법·함수명은 제거'],
       '위치·간격으로 숫자열을 순회하는 필요와 호출 표현의 가독성, 이름 재정의에 따른 최적화 제약을 확인했다.',
       ['시작·끝·간격으로 숫자열 지정','위치 기반 또는 일정 간격 반복에 적용','가독성 및 내장 이름 재정의 영향 고려'],
       outcome='rejected',gold_sections=['List ranges','Slice Indices','Open issues','Rejection'])
gold(p,'range() 내장 함수','List ranges','호출과 추가 계산이 장황하고 이름을 재정의할 수 있어 컴파일러가 동작을 가정하기 어렵다.',ROLE_PART,'referenced','https://docs.python.org/2/library/functions.html#range')
gold(p,'확장 슬라이스의 시작:끝:간격 표기','Slice Indices','같은 세 인수에 기존 구문이 있다는 설계 선례로 제시한다. 숫자열과 슬라이스의 의미 혼동은 전체 기각 이유에도 등장한다.',stance='referenced')
gold(p,'xrange형 지연 생성기','Open issues / first bullet','작은 저장 공간을 사용하지만 실제 리스트가 아니어서 원소 대입과 append가 불가능하다.',ROLE_PART,'referenced','https://docs.python.org/2/library/functions.html#xrange')
gold(p,'튜플 범위 구문을 지연 생성기로 구현','Open issues / first bullet','불변 컨테이너라 지연 평가와 잘 맞지만 끝 인수의 선택 여부가 구문별로 달라지는 문제가 남는다.',stance='referenced')
gold(p,'일반 리스트 원소와 범위 리터럴을 한 목록에 혼합','Open issues / second bullet','단일 결과 리스트로 확장하는 구문을 검토했으나 결론은 열려 있다.',stance='referenced')
gold(p,'리스트 생성 구문 안의 범위를 평탄한 단일 리스트로 합침','Open issues / third bullet','반복마다 생성되는 범위를 하나로 합칠지 여부를 명시적으로 비교한다.',stance='referenced')
gold(p,'리스트 생성 구문 안의 범위를 리스트의 리스트로 보존','Open issues / third bullet','평탄화와 대조되는 중첩 결과를 제시하고 다른 제안의 의미 결정에 맡긴다.',stance='referenced')
gold(p,'범위 결과가 입력 값의 타입을 보존','Open issues / fourth bullet','일반 정수 외 타입을 만들 수 있지만 숨은 변환과 사용자 정의 생성자의 추가 인수 때문에 실패할 수 있다.',stance='referenced')
gold(p,'범위 생성 C 보조 함수를 비공개 구현으로 유지','Open issues / fifth bullet','공개 API로 노출할지 비공개로 둘지 명시적인 미결 설계 질문이다.',stance='referenced',boundary='검색할 외부 실체가 아니라 제안 내부의 API 경계 선택이다. 구조 일치만 가능하다.')

p=case('P0354','Enumerations in Python','98dd3dcbe42bfddacf825e81ba503249c677481d',
       'e31746e7fc5689491e7ea0d4a1b9c915358b18db','2007-05-18',
       '공식 저장소의 Rejected 상태 반영',
       ['Abstract: 자료형 목적','Motivation: 불변 상수 집합과 의미 없는 연산의 문제'],
       '이름 있는 관련 값의 불변 집합, 집합 안의 순서·비교, 외부 값과의 구별을 요구함을 확인했다.',
       ['관련 값 집합의 불변성','집합 외 값과 구별','의미 있는 순서·비교를 제공하고 무의미한 연산 제한'],
       outcome='rejected_then_replaced',gold_sections=['Rationale -- Other designs considered: four subsections'],
       superseded=[dict(type='rejected_proposal_replaced',url='https://github.com/python/peps/blob/4434e728a7db24540d581f52e96570ca1230356e/peps/pep-0435.rst',pinned_version='4434e728a7db24540d581f52e96570ca1230356e',date='2013-05-10',scope='기각된 열거형 제안을 PEP435로 대체. 2007년 제안이 먼저 채택되었다고 보지 않는다.')])
gold(p,'열거형과 값을 하나의 클래스·객체에 결합','All in one class','이점 없이 복잡성이 늘어난다는 이유로 컨테이너와 비교 가능한 값을 분리한다.')
gold(p,'메타클래스로 각각의 열거형 클래스를 생성','Metaclass for creating enumeration classes','서브클래싱은 가능하지만 값 집합의 클래스·인스턴스 의미가 혼동되고 Singleton 같은 추가 복잡성이 필요하다.')
gold(p,'열거 값을 정수·문자열 값에 강하게 연결','Values related to other types','열거형의 의미가 없는 문맥에 값을 사용하게 만들고 설계를 복잡하게 한다.')
gold(p,'열거 값의 문자열 키와 순서 인덱스를 숨김','Hiding attributes of enumerated values','실제 프로그램에서 타입·인덱스·키를 알아야 할 필요가 있으므로 그 속성을 노출하는 안을 택했다.')

p=case('P0433','Easier suppression of file descriptor inheritance','81f79a9a15c056e50d551fb6b4adb396c4de33be',
       '0efb6d7b3ec34a093a341551d7209aaf6e9dff2b','2013-08-28',
       'Draft를 Superseded로 바꾸고 대체 제안을 연결한 공식 커밋',
       ['Rationale: UNIX 기본 동작과 다른 프로세스 생성 경로의 유출 문제'],
       '특정 하위 프로세스 API 밖에서 디스크립터가 자식으로 전달되는 문제를 확인했다.',
       ['의도치 않은 부모→자식 디스크립터 전달을 다룸','여러 실행 경로와 외부 모듈 고려','표준 입출력과 추가 디스크립터 구분'],
       outcome='draft_superseded',gold_sections=['Alternatives: five functional alternatives','Links / Other languages'],
       superseded=[dict(type='draft_replaced',url='https://github.com/python/peps/blob/4434e728a7db24540d581f52e96570ca1230356e/peps/pep-0446.rst',pinned_version='4434e728a7db24540d581f52e96570ca1230356e',date='2013-08-28',scope='기본 상속을 유지하는 선택적 제안 대신 기본 비상속과 원자적 생성으로 바꾼 PEP446. 원 제안의 선행 채택은 없다.')])
gold(p,'상속 기본값 False 변경 없이 선택적 cloexec만 추가','Inheritance enabled by default, default no configurable','보수적인 API지만 모든 디스크립터 생성 위치를 수정해야 하므로 전체 유출 문제를 자체 해결하지 못한다.')
gold(p,'전역 기본값을 한 방향으로만 변경하는 설정','Inheritance enabled by default, default can only be set to True','한 번 비상속 쪽으로만 바꿀 수 있게 한 설계 변형이다. 독립 기각 이유는 명시되지 않는다.',stance='referenced')
gold(p,'비상속을 기본으로 하고 필요한 디스크립터만 상속','Disable inheritance by default','유출을 겪는 프로그램이 더 많다는 장점과 POSIX 기대·추가 시스템 호출·호환성 비용을 비교한다.',stance='referenced')
gold(p,'fork 직후 atfork 콜백으로 디스크립터 닫기','Close file descriptors after fork','Windows·exec 단독 경로·C에서 직접 fork하는 경로를 포괄하지 못하고 등록 해제 경합도 생긴다.',url='http://bugs.python.org/issue16500')
gold(p,'open 모드에 e 플래그 추가','open(): add e flag to mode','파일 open에만 적용되며 mode 인수가 없는 소켓과 파이프에는 적용할 수 없다.')
gold(p,'GNU libc fopen의 e 모드','open(): add e flag to mode','이미 제공되는 C 라이브러리의 비상속 파일 열기 선례다.',ROLE_ECO,'referenced',url='https://www.gnu.org/software/libc/manual/html_node/Opening-Streams.html',boundary='C 라이브러리에서 Python API로 옮기는 같은 문제의 생태계 선례. 별도 원문 링크는 이 실행에서 검증하지 않았다.')
gold(p,'Visual Studio fopen의 N 모드','open(): add e flag to mode','다른 C 런타임의 비상속 모드 선례로 함께 제시한다.',ROLE_ECO,'referenced',url='https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/fopen-wfopen',boundary='언어 런타임 간 선례이며 먼 분야 원리가 아니다. 현재 공식 문서 URL은 항목 식별용이며 이 실행에서 직접 열지 않았다.')
gold(p,'Perl SYSTEM_FD_MAX에 따른 상속 제한','Links / Other languages','일정 번호를 넘는 새 디스크립터의 close-on-exec 기본 동작을 선행 사례로 기록한다.',ROLE_ECO,'referenced','http://perldoc.perl.org/perlvar.html#%24SYSTEM_FD_MAX')
gold(p,'Ruby의 FD_CLOEXEC 기본 설정 및 일부 되돌림','Links / Other languages','Ruby의 전체 FD 기본 설정과 특정 open 플래그 변경의 되돌림을 함께 연결한다.',ROLE_ECO,'referenced','http://bugs.ruby-lang.org/issues/5041',extra={'additional_urls':['http://bugs.ruby-lang.org/issues/1291','http://bugs.ruby-lang.org/projects/ruby-trunk/repository/revisions/31643']})
gold(p,'OCaml Unix.set_close_on_exec 및 프로세스 상속 이슈','Links / Other languages','동일한 유출 문제와 명시적 설정 함수를 가진 다른 언어 사례다.',ROLE_ECO,'referenced','http://caml.inria.fr/mantis/view.php?id=5256')
p['extraction_exclusions']=['inherit/inherited/sensitive/sterile라는 순수 이름 후보는 독립 기능 대안이 아니므로 골드 분모에서 제외. sterile의 생물학적 어원은 장식적 용어 차용 기록으로만 남긴다.','Appendix의 모든 OS 플래그와 문제 사례 링크를 자동으로 prior art 골드에 추가하지 않았다.']

p=case('P0509','Add a private version to dict','534db9e409d047dc41b21575ad1b827ed0d0ffe3',
       'fd5c057e268dce0c88fc7fb921e61190b6c2d3bb','2016-09-08',
       '공식 저장소의 수락·Final 상태 반영',
       ['Rationale: 변경 가능한 이름 공간, 가드 비용, 전역 읽기 최적화 예시의 문제 문맥'],
       '동적인 이름 바인딩을 유지하면서 저비용으로 최적화 유효성을 확인해야 하는 문제를 확인했다.',
       ['실행 중 바인딩 변경 의미 보존','캐시 또는 최적화 무효화를 판별','확인 비용이 최적화 이익을 없애지 않는지 고려'],
       gold_sections=['Alternatives: three functional alternatives','Prior Art: five subsections'],
       superseded=[dict(type='adopted_specification_rescinded',url='https://github.com/python/peps/blob/ab15de6ab836f41e6be797b4de380a0233066ce8/pep-0699.rst',pinned_version='ab15de6ab836f41e6be797b4de380a0233066ce8',date='2023-01-18',scope='PEP699가 PEP509의 dict 버전 필드 사양을 철회하고 구현 세부로 재분류. 3.11 특수화는 다른 가드를 사용하며 후속 write watcher 등의 재사용을 허용한다.')])
gold(p,'Python 수준 read-only __version__ 속성','Expose the version at Python level as a read-only __version__ property','다른 mapping·구현체의 부담, Python 수준 조회 속도 이익 부족, overflow 비교 오해 때문에 공개하지 않는다.')
gold(p,'사전 엔트리별 버전 태그','Add a version to each dict entry','값의 강한 참조를 피할 수 있지만 64비트에서 엔트리마다 8바이트가 늘어난다는 메모리 비용이 있다.')
gold(p,'버전을 가진 새 dict 하위 타입 verdict','Add a new dict subtype','기존 exec/C API/정확한 dict 타입 검사와 호환되지 않으며 GC와 빠른 경로 문제도 있다.')
gold(p,'CPython method cache와 tp_version_tag','Method cache and type version tag','전역 버전과 타입 캐시 무효화의 기존 구현 선례다.',ROLE_PART,'referenced','https://bugs.python.org/issue1685986',extra={'additional_urls':['https://bugs.python.org/issue1700288']})
gold(p,'Globals / builtins cache issue10401','Globals / builtins cache','dict의 사적 버전 필드와 전역·내장 이름 캐시를 제안한 유사 패치다.',ROLE_DESIGN,'referenced','http://bugs.python.org/issue10401')
gold(p,'Cached globals+builtins lookup issue1616125','Cached globals+builtins lookup','dict 타임스탬프로 이름 검색을 캐시한 2006년 패치다.',ROLE_DESIGN,'referenced','https://bugs.python.org/issue1616125',extra={'additional_urls':['https://mail.python.org/pipermail/python-dev/2006-December/070348.html']})
gold(p,'사전 반복 중 변경 감지 issue19332','Guard against changing dict during iteration','dict가 변경될 때 증가하는 카운터를 반복 안전성에 이용한 선례다.',ROLE_DESIGN,'referenced','https://bugs.python.org/issue19332',boundary='목적은 반복 안전성으로 다르지만 같은 사전 구현 영역이라 먼 분야로 세지 않는다.')
gold(p,'PySizer의 dict 엔트리 시간 기록','PySizer','메모리 프로파일러가 프로세스 전체 카운터와 key/value 시간을 이용해 자식 객체의 등장 시점을 추적한다.',ROLE_PART,'referenced','http://pysizer.8325.org/',boundary='프로파일링에서 최적화 가드로 같은 dict 변경 메커니즘을 참고한다. 보수적 규칙상 동일 런타임 자료구조 영역이며 먼 분야가 아니다.')
p['extraction_exclusions']=['__cache_token__/__version_tag__/__timestamp__ 명칭과 abc.get_cache_token의 이름 유래는 독립 기능 대안이 아니므로 분모에서 제외.','메모리 비용의 배경인 다른 PEP 참조를 모두 골드로 올리지 않았다.']

p=case('P0554','Multiple Interpreters in the Stdlib','4df4ecf20951df6f34925cf90a124d5021a8e2dd',
       '6aeaba7f23a1ce373e099a2b35db9525dbb11f6d','2023-11-28',
       'Draft를 Superseded로 바꾸고 PEP734를 추가한 공식 커밋',
       ['Rationale: 같은 프로세스 안 격리와 기존 C API의 Python 접근 문제'],
       '기존 다중 인터프리터 기능을 Python 표준 라이브러리에서 접근하게 하는 목적을 확인했다.',
       ['같은 프로세스의 다중 인터프리터 범위','인터프리터 간 격리 존중','기존 기능을 Python 코드에서 접근'],
       outcome='draft_superseded',prefix_path='pep-0554.rst',gold_path='peps/pep-0554.rst',
       gold_sections=['Alternative Solutions','Rejected Ideas: explicit API and exception-handling alternatives'],
       superseded=[dict(type='draft_replaced',url='https://github.com/python/peps/blob/6aeaba7f23a1ce373e099a2b35db9525dbb11f6d/peps/pep-0734.rst',pinned_version='6aeaba7f23a1ce373e099a2b35db9525dbb11f6d',date='2023-11-28',scope='장기간 Draft였던 API를 더 작은 PEP734 제안으로 교체. PEP734의 최종 수락은 2025년이므로 이 사례의 결정 창 밖이며 선행 채택 후 번복으로 세지 않는다.')])
gold(p,'concurrent.futures에 인터프리터 지원 추가','Alternative Solutions','함수 실행 중심 API인데 인터프리터 간 함수 실행 방법이 준비되지 않았고 발견 가능성도 낮다.',ROLE_PART,'rejected','https://docs.python.org/3/library/concurrent.futures.html')
gold(p,'multiprocessing에 인터프리터 지원 추가','Alternative Solutions','기존 모듈의 실행 추상화에 바로 끼워 넣는 안에도 유사한 함수 실행·발견 가능성 문제가 적용된다.',ROLE_PART,'rejected','https://docs.python.org/3/library/multiprocessing.html')
gold(p,'채널을 명시적으로 연결·해제하는 메서드','Explicit channel association','보통 사용자가 관리할 필요가 없어 API 잡음만 늘린다고 판단했다.')
gold(p,'정확히 두 인터프리터 사이의 단방향 pipe API','Add an API based on pipes','많은 경우 충분하지만 many-to-many 채널로 확장하는 비용이 작고 pipe 이름 관리로 API가 더 복잡해진다.')
gold(p,'Queue 기반 API','Add an API based on queues','buffered channel과 유사하지만 채널은 인터프리터 문맥과 더 강하게 연관되며 기존 queue.Queue와의 혼동도 피한다.')
gold(p,'원래 예외 객체와 traceback을 그대로 전파','Alternate solutions to prevent leaking exceptions across interpreters / opening paragraphs','객체와 프레임이 격리 경계를 넘어 유출되어 향후 독립 메모리 관리와 충돌한다.')
gold(p,'원 예외와 traceback을 호출 인터프리터에 복제','Alternate solutions to prevent leaking exceptions across interpreters / rejected bullet 1','안전한 대리 예외를 사용하는 여러 대안 중 하나로 기각 목록에 있다. 개별 기각 이유는 추가로 명시하지 않는다.')
gold(p,'원 예외를 프록시하는 RunFailedError 하위 클래스','Alternate solutions to prevent leaking exceptions across interpreters / rejected bullet 2','경계 예외 처리의 대안으로 기각 목록에 있다. 개별 기각 이유는 명시되지 않는다.')
gold(p,'RunFailedError 대신 RuntimeError 발생','Alternate solutions to prevent leaking exceptions across interpreters / rejected bullet 3','별도 경계 실패 타입 대신 일반 런타임 오류를 사용하는 대안이며 개별 이유는 미기재다.')
gold(p,'CalledProcessError처럼 경계에서 예외 표현을 변환','Alternate solutions to prevent leaking exceptions across interpreters / rejected bullet 4','인터프리터 간에 통용되는 별도 표현이 필요하다.',boundary='프로세스 경계 오류를 인터프리터 경계로 옮긴 가까운 소프트웨어 영역 선례. 먼 분야 원리로 확대하지 않는다.')
gold(p,'Interpreter.excepthook으로 변환을 사용자 정의','Alternate solutions to prevent leaking exceptions across interpreters / rejected bullet 5','사용자 정의에도 인터프리터 간 예외 표현이 필요하다.')
gold(p,'경계의 프록시와 err.raise()로 원 traceback 전달','Alternate solutions to prevent leaking exceptions across interpreters / rejected bullet 6','대리 객체와 다시 발생시키는 프로토콜을 사용하는 기각 대안이다. 개별 이유는 미기재다.')
gold(p,'exec가 예외 또는 프록시를 반환','Alternate solutions to prevent leaking exceptions across interpreters / rejected bullet 7','오류를 발생시키는 대신 반환 값으로 표현하는 기각 대안이다. 개별 이유는 미기재다.')
gold(p,'subprocess형 실행 결과 객체 반환','Alternate solutions to prevent leaking exceptions across interpreters / rejected bullet 8','결과 객체 방식은 불필요한 복잡성일 수 있다고 기록한다.',boundary='같은 표준 라이브러리의 실행 API 패턴 차용으로 분류; 원거리 전이 아님.')
gold(p,'예외를 버리고 실행 스크립트가 채널로 처리','Alternate solutions to prevent leaking exceptions across interpreters / rejected bullet 9','스레드처럼 사용자 스크립트가 명시적으로 미처리 예외를 전달하도록 맡기는 기각 대안이다.')
gold(p,'새 인터프리터마다 전용 스레드를 자동 생성','Always associate each new interpreter with its own thread','C API와 달라 혼동을 주고 조기 스레드 생성 낭비·기존 스레드 사용 제한·구현 복잡성이 생긴다.')
gold(p,'채널을 실제 send/recv할 때만 연결','Only associate interpreters upon use','첫 사용 전에 자동으로 채널이 닫히는 경합과 혼동을 만들 수 있다.')
gold(p,'동시에 여러 Interpreter.exec 호출 허용','Allow multiple simultaneous calls to Interpreter.exec()','하나의 __main__을 공유하거나 별도 체계를 발명해야 하므로 단순성에 비해 비용이 크다.')
gold(p,'RunFailedError.reraise() 또는 __reraise__ 프로토콜','Add a reraise method to RunFailedError','기존 __cause__를 다시 발생시키는 방식으로 충분하므로 새 메서드는 불필요하다.')
p['extraction_exclusions']=['enumerate/list_all 명칭만의 선택은 독립 기능 대안이 아니어서 제외.','Deferred Functionality의 미래 기능을 모두 기각 대안으로 바꾸지 않았다.']
p['temporal_note']='접두부는 2017년 최초 초안이고 골드는 2023년 supersession 판이다. 6년 동안 늘어난 API 세부 대안을 초기 목적만으로 회수하는 어려움이 있다.'

p=case('P0563','Postponed Evaluation of Annotations','454c88950bca978ddff30144c66f2e420f51f96e',
       'cfa69b62a19c959b70e806591b2c9dbe93fd6e0b','2017-12-04',
       '공식 수락 메일 2017-12-04T16:42:38Z',
       ['Rationale and Goals: forward reference와 import 비용','Non-goals: 동적 타입·임의 annotation 사용 유지'],
       '정의 시점의 annotation 평가가 앞선 이름 참조와 import 비용을 어렵게 만들며 임의 런타임 사용도 유지해야 함을 확인했다.',
       ['아직 정의되지 않은 이름 참조 처리','import 계산 비용 고려','타입 힌트를 의무화하지 않음','타입 검사 외 annotation 사용 보존'],
       prefix_path='pep-0563.rst',gold_sections=['Rejected Ideas: five functional alternatives'],
       date_url='https://mail.python.org/pipermail/python-dev/2017-December/151042.html',
       date_note='수락 메일은 Dec4 11:42:38 EST(16:42:38 UTC)이고 Git Accepted 반영은 Dec5이다. 접두부의 최초 동결에는 Git 날짜가 쓰였으므로 root가 실행 cutoff 정정을 별도 기록한다.',
       superseded=[dict(type='adopted_design_replaced',url='https://github.com/python/peps/blob/a111ec493be2d52356c1451f074e4a7c70d9ad82/pep-0649.rst',pinned_version='a111ec493be2d52356c1451f074e4a7c70d9ad82',date='2023-05-16',scope='PEP649의 Accepted 판은 문자열화가 런타임 사용자에게 준 문제를 지적하고 계산 함수+descriptor로 지연 평가한다. 2017년 lambda 대안의 잘못된 기각을 별도 절에서 재검토한다. 모든 이전 lambda 구현과 동일하다고 보지는 않는다.')])
gold(p,'annotation을 lambda로 보관하여 함수 지역 상태 유지','Keeping the ability to use function local state when defining annotations','프레임과 객체를 오래 살려두는 메모리 비용 및 클래스 스코프의 새 cell 형식 부담을 이유로 기각했다.')
gold(p,'클래스에서도 모듈 수준 이름만 사용','Disallowing local state usage for classes, too','일반적인 스코프 직관과 기존 타입 주석을 깨며 class decorator가 필요한 이름을 해석하지 못한다.')
gold(p,'__annotations_text__와 지연 __annotations__ 매핑을 병행','Introducing a new dictionary for the string literal form instead','함수 지역 상태 변화라는 호환성 문제를 해결하지 못하며 명시적 opt-in과 get_type_hints가 있으면 중복 단계가 된다.')
gold(p,'-O 실행 옵션으로 annotation 제거','Dropping annotations with -O','평가 비용은 줄이지만 앞선 이름 참조를 해결하지 못하고 런타임 annotation 사용을 모두 없앤다.')
gold(p,'문자열 리터럴 annotation의 내용만 그대로 저장','Passing string literals in annotations verbatim to __annotations__','문자열이 더 큰 annotation의 일부인 경우를 일관되게 처리하지 못하고 이중 감싸기를 완전히 피하지 못한다.')
p['extraction_exclusions']=['future import의 긴 이름 후보들은 기능 대안이 아닌 명명 변형이어서 골드 분모에서 제외.','Prior discussion의 단순 참고 링크를 모두 독립 대안으로 코딩하지 않았다.']

SWIFT_PATHS={16:'0016-initializers-for-converting-unsafe-pointers-to-ints.md',18:'0018-flexible-memberwise-initialization.md',19:'0019-package-manager-testing.md',20:'0020-if-swift-version.md',21:'0021-generalized-naming.md',22:'0022-objc-selectors.md',25:'0025-scoped-access-level.md',27:'0027-string-from-code-units.md'}
def swift(n,title,ps,gs,date,problem,constraints,**kw):
    return case(f'S{n:04d}',title,ps,gs,date,kw.pop('event','공식 저장소의 Accepted 상태 반영'),
                kw.pop('sections',['Introduction: 문제에 해당하는 문단','Motivation: 기존 상황·어려움; 해법과 대안 이름 제거']),
                problem,constraints,prefix_path='proposals/'+SWIFT_PATHS[n],gold_sections=kw.pop('gold_sections',['Alternatives considered']),**kw)

p=swift(16,'Initializers for converting unsafe pointers to integers','805dd31614b88590a4ef62a72804c1b7519b7df8','36dd2cc2f0306785af461271feeeab788ca3c430','2016-03-31',
        '포인터의 정렬·태그·비트 연산과 주소 크기 정수를 요구하는 C 함수 호출의 문제를 확인했다.',
        ['Swift에서 저수준 주소 조작','C 상호 운용에 적용','원래 불안전한 작업이라는 전제'],
        date_url='https://forums.swift.org/t/accepted-se-0016-adding-initializers-to-int-and-uint-to-convert-from-unsafepointer-and-unsafemutablepointer/2005/1',
        event='공식 review acceptance 2016-03-31T04:11:54Z',date_note='공식 수락 글 04:11:54Z, 저장소 반영 04:13:40Z를 별도로 확인했다.')
gold(p,'포인터의 intValue 변환 메서드','Alternatives considered / first alternative','가능한 타입 변환은 initializer로 표현하는 언어 관례를 따른다.')
gold(p,'포인터 타입에 모든 산술·비트 연산 API 추가','Alternatives considered / next alternative','모든 사용례를 예측하기 어렵고 signed/unsigned 분리와 불필요한 왕복 변환이 늘어난다.')
gold(p,'복잡한 포인터 조작을 C 코드로 작성','Alternatives considered / last alternative','Swift를 시스템 프로그래밍 언어로 쓰는 가치를 떨어뜨린다고 판단했다.',ROLE_ECO,'rejected',url='https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf',boundary='제안의 외부 링크가 아니라 C 언어 대안의 공식 표준 식별 URL이다. 해당 표준의 세부 적합성은 이 항목 코딩에서 판정하지 않았다.')

p=swift(18,'Flexible Memberwise Initialization','40c4211d165070abeb4d0bf2f85885303263ae4a','7778003344f926a503edbc14f95e2153dad6f7d9','2016-01-13',
        '초기화 반복 코드가 속성 수×초기화 경로 수로 늘고 불변성과 부분 자동화를 해친다는 문제를 확인했다.',
        ['초기화 반복 코드 감소','불변 속성 사용을 방해하지 않음','일부 멤버 자동화와 사적 구현 상태의 수동 초기화를 병행'],
        outcome='rejected_for_current_cycle_then_returned_for_revision',event='공식 원문에 Rejected 상태와 review rationale를 기록한 시점',
        date_url='https://forums.swift.org/t/review-se-0018-flexible-memberwise-initialization/939/22',
        date_note='Jan12 review 완료·보류 기록과 Jan13 Rejected 기록이 인접한다. 여기서는 Jan13 원문 고정 판의 거절 기록을 decision event로 사용한다. 2022년 Returned for revision은 후속 상태이며 초기 입력에 넣지 않는다.')
gold(p,'속성별 memberwise 명시 opt-in','Require properties to opt-in to memberwise initialization','명시성은 좋지만 기본 자동 모델을 함께 제공할 수 없고 일반적 사용에 표기가 더 필요하다.',stance='referenced')
gold(p,'모든 initializer가 자동 참여','Allow all initializers to participate in memberwise initialization','기존 코드를 바꾸고 선언만 보고 합성 인수·속성 초기화를 알기 어렵다.')
gold(p,'initializer가 명시적으로 opt-out','Require initializers to opt-out of memberwise initialization','모든 initializer 자동 참여와 동일한 호환성·명시성 문제가 있다.')
gold(p,'initializer보다 덜 공개된 속성의 인수도 합성','Allow parameters to be synthesized for properties with a lower access level than the initializer','사적 상태가 예상 밖으로 공개되며 일반적으로 안전한 기본값이 아니다. 필요한 경우 직접 작성할 수 있다.')
gold(p,'인수는 모두 선언하고 속성 대입만 합성','Require initializers to explicitly specify memberwise initialization parameters','인수 선언은 여전히 M×N으로 증가하고 convenience/delegating initializer 전달 문제를 해결하지 못한다.',url='https://forums.swift.org/t/helpers-for-initializing-properties-of-the-same-name-as-parameters/129/3')
gold(p,'Kotlin의 타입 선언 매개변수·속성 문법','Adopt type parameter list syntax like Kotlin and Scala','간결하지만 여러 초기화 경로·부분 초기화·속성 배치의 유연성을 충분히 제공하지 못한다.',ROLE_ECO,'rejected',url='https://kotlinlang.org/docs/classes.html',review=True,boundary='한 절에서 Scala와 함께 비교하지만 서로 다른 언어 실체이므로 별도 항목. 코어 구조가 같아도 언어명만으로 중복 적중을 주지 않는다.',extra={'review_evidence':'원문은 메일링리스트 제안이라고 명시하며 Jan5 commit a4ae11742164d8f581f0628bcc4d2b0129a94a57에서 해당 비교가 추가됨. 토론 전수 출현 시점은 미확인.'})
gold(p,'Scala의 타입 선언 매개변수·속성 문법','Adopt type parameter list syntax like Kotlin and Scala','부분 자동화와 여러 initializer 지원 및 속성 배치에 같은 제약이 있다고 대조한다.',ROLE_ECO,'rejected',url='https://docs.scala-lang.org/tour/classes.html',review=True,boundary='다른 언어·생태계이며 먼 분야 원리가 아니다.',extra={'review_evidence':'원문은 메일링리스트 제안이라고 명시하며 Jan5 commit a4ae11742164d8f581f0628bcc4d2b0129a94a57에서 해당 비교가 추가됨.'})

p=swift(19,'Swift Package Manager Testing','6d38d54e7176f88fba666c9d0b3567211f44b333','2fdf30579c233ddb26a36a3e1a77bca9d9cef30a','2016-01-21',
        '패키지 생태계의 안정성과 신뢰성을 위해 테스트 통합이 필요하다는 짧은 Introduction을 확인했다.',
        ['Swift 패키지 관리 작업과 테스트 통합','안정성과 신뢰성 개선 목적'],sections=['Introduction: 테스트의 필요와 패키지 관리 통합 목적'])
gold(p,'Xcode형 Sources 옆 FooTests 디렉터리 배치','Alternatives Considered / first block','기존 프로젝트는 많지만 패키지의 단순한 디렉터리 규칙과 일관되지 않아 오동작 진단을 어렵게 한다.',stance='rejected',boundary='실제 Xcode 관행을 참고한 같은 Swift 개발 생태계의 배치 설계다.')
gold(p,'테스트와 SwiftPM을 완전히 분리','Alternatives Considered / second block','테스트도 빌드와 의존성 관리가 필요하므로 완전한 분리는 불가능하다.')
gold(p,'기본 XCTest 지원 없이 테스트 프로토콜만 제공','Alternatives Considered / third block','테스트 지원을 빨리 갖추고 시스템이 기본 프레임워크를 보장하는 장점 때문에 미뤘다.')

p=swift(20,'Build configuration by Swift language version','eff6f9c4e1cd09ccb9f190ee4134b7ca037cfb68','b3c511881a9813105032b10fe6dac4351c6bd078','2016-01-21',
        '하나의 배포 소스를 여러 언어 버전에서 빌드하고 별도 릴리스 브랜치를 줄이려는 목적을 확인했다.',
        ['언어 버전에 따른 문법 차이 처리','별도 소스 트리 증가를 줄임','소스 배포 패키지의 여러 버전 빌드 지원'],sections=['Motivation: 두 문단'])
gold(p,'문자열 리터럴로 버전 지정','Alternatives considered / String literals','성분 수를 자유롭게 늘릴 수 있지만 미세 버전에서 문법 변경은 드물며 필요하면 파서를 확장할 수 있다.')
gold(p,'비교 연산자 없는 버전 숫자','Alternatives considered / Just plain','기본 비교가 이상인지 동등인지 독자가 오해할 수 있다.')
gold(p,'쉼표로 분리한 버전 인수 목록','Alternatives considered / Argument lists','버전의 각 성분이 아니라 서로 다른 의미의 인수처럼 보일 수 있다.')

p=swift(21,'Generalized Naming','040da0949b409ec7e66d72612bf1828acd2f395b','05ef3a9d51d81be80208a4d8d554a7eef2f8e3b5','2016-01-20',
        '동일한 기본 이름과 타입을 가진 오버로드를 함수 값으로 참조할 때 불명확하고 장황해지는 문제를 확인했다.',
        ['의도한 오버로드를 함수 값으로 참조','동일 타입·다른 레이블의 경우 처리','반복 코드와 불필요한 타입 표기 감소'])
gold(p,'프로퍼티 전체 접근 인터페이스를 보존하는 lens','Alternatives considered / first bullet','단순 getter/setter 함수보다 값 타입의 재귀 쓰기와 copy-on-write 효율을 보존한다.',ROLE_DESIGN,'referenced','https://forums.swift.org/t/proposal-expose-getter-setters-in-the-same-way-as-regular-methods/501/3',review=True,boundary='함수형 프로그래밍과 속성 인터페이스의 같은 언어 설계 영역. 먼 분야로 세지 않는다.',extra={'review_evidence':'PS-R-S21-LENS: 2015-12-17 공개 토론이 해당 인터페이스를 제안하며 최종 원문이 직접 연결한다.'})
gold(p,'_ 자리표시자를 이용한 일반 partial application','Alternatives considered / second bullet','일반 partial application까지 추가할 필요가 작고 기존 closure가 거의 같은 간결함과 더 분명한 인수 대응을 제공한다.',url='https://forums.swift.org/t/proposal-draft-generalized-naming-for-any-function/787/6',review=True,extra={'review_evidence':'PS-R-S21-PARTIAL: 2015-12-29 초안 토론의 새 제안. 최종 원문이 이 글을 직접 연결한다.'})
gold(p,'함수 이름에서 비어 있는 인수 레이블의 underscore 생략','Alternatives considered / third bullet','레이블 유무를 시각적으로 구분하기 어렵고 다른 도구의 이름 표기와 일관되지 않다.')

p=swift(22,'Referencing Objective-C selectors','040da0949b409ec7e66d72612bf1828acd2f395b','bf1c86212314ed90e6b615ddf8db8c15eb00e201','2016-01-26',
        '문자열로 메서드 식별 값을 만들면 대상 검증이 없고 언어 간 이름 대응도 불분명해진다는 문제를 확인했다.',
        ['의도한 Objective-C 메서드 식별 값 생성','오타와 대상 혼동 감소','서로 다른 표면 이름 대응 부담 고려'],
        event='공식 공개 리뷰 수락 2016-01-26T22:16:32Z',
        date_url='https://forums.swift.org/t/accepted-se-0022-referencing-the-objective-c-selector-of-a-method/1194/1',
        date_note='Jan26 수락 글이 문법 변경과 기각 대안들을 명시했다. Jan28 고정 골드는 그 결정을 문서에 반영한 판으로, 2일의 반영 지연을 숨기지 않는다.',
        gold_sections=['Alternatives considered','공식 acceptance discussion: 추가된 두 대안'])
gold(p,'type-safe selector 호출 규약','Alternatives considered / primary alternative','타입 정보는 안전하지만 Swift와 Clang의 큰 변경 및 많은 ObjC API 채택이 필요하며 closure 대안이 이미 선호된다.',url='https://forums.swift.org/t/type-safe-selectors/108')
gold(p,'Objective-C형 @selector 표기','Alternatives considered / syntax','Swift에서 @는 attribute를 뜻하므로 기존 언어의 표기 의미와 맞지 않는다.')
gold(p,'특수한 Selector initializer','Alternatives considered / original version','일반 생성자처럼 보이지만 실제 initializer로 표현할 수 없는 컴파일러 특수 기능이라 리뷰에서 다른 sigil로 바뀌었다.',review=True,extra={'review_evidence':'PS-R-S22-ACCEPT: Jan26 공식 수락 글이 magic constructor를 기각했다고 명시한다.'})
gold(p,'메서드 참조를 Selector로 암묵 변환','Official acceptance discussion / alternative a','드문 ObjC 상호 운용 때문에 타입 시스템을 복잡하게 하지 않기로 했다.',url='https://forums.swift.org/t/accepted-se-0022-referencing-the-objective-c-selector-of-a-method/1194/1',review=True,extra={'gold_origin':'review_addition','source_ids':['PS-R-S22-ACCEPT'],'match_kind':'structural_design'})
gold(p,'함수 선언의 magic .selector 멤버','Official acceptance discussion / alternative c','향후 함수 타입에 실제 멤버를 제공할 때 사용할 이름 공간을 미리 점유한다.',url='https://forums.swift.org/t/accepted-se-0022-referencing-the-objective-c-selector-of-a-method/1194/1',review=True,extra={'gold_origin':'review_addition','source_ids':['PS-R-S22-ACCEPT'],'match_kind':'structural_design'})

p=swift(25,'Scoped Access Level','13dfdd7796a6331fa39a3f4b4dbfa4f196311f6a','70116480493c158afc1d815057885ab0615fbebf','2016-04-01',
        '파일 배치와 독립적으로 클래스·확장의 구현 세부를 숨기고 컴파일러가 강제하기를 바라는 문제를 확인했다.',
        ['클래스·확장 구현 세부의 바깥 사용 제한','관련 타입의 파일 분리를 강제하지 않음','컴파일러가 숨김 의도를 강제'],
        event='공식 Discussion에 인용된 core-team 최종 접근 수준 결정 2016-04-01',
        date_url='https://forums.swift.org/t/se-0025-scoped-access-level-next-steps/1797/131',
        date_note='Apr4 확인 글이 Apr1 최종 결정 메일을 인용한다. 원 메일의 독립 post 식별은 미확인(해당 주 mailing-list archive에서 Apr1 원 메시지 재확인). Git Accepted 상태는 Apr20 반영되어 19일 늦다.',
        superseded=[dict(type='partial_reversal_after_adoption',url='https://github.com/swiftlang/swift-evolution/blob/17bc96ea9f23b1becfe91bfd72bd0c006390fd58/proposals/0169-improve-interaction-between-private-declarations-and-extensions.md',pinned_version='17bc96ea9f23b1becfe91bfd72bd0c006390fd58',date='2017-04-18',decision_url='https://forums.swift.org/t/accepted-se-0169-improve-interaction-between-private-declarations-and-extensions/5692/1',scope='동일 파일 안 동일 타입의 extensions를 하나의 private 접근 scope로 본다. lexical scope만 허용하던 SE0025 경계를 부분적으로 넓힌다. 다른 파일·다른 타입의 모든 접근을 허용하는 전면 폐기는 아니다.')])
gold(p,'기존 이름 관례·파일 분리와 파일 수준 private 유지','Alternatives considered / item 1','컴파일러 강제와 의도 표현이 약하거나 파일 구성 방식을 강제한다.')
gold(p,'파일 일부를 감싸는 scoped namespace','Alternatives considered / item 2','그룹·중첩을 추가하고 논리적 관련성 대신 접근 수준별로 코드를 묶게 한다.')
gold(p,'기존 private 명칭을 유지하고 새 modifier 추가','Alternatives considered / item 3','소스 호환성은 좋지만 다른 언어의 private 기대에 맞추려는 결정으로 새 이름 체계를 택했다.',review=True,extra={'review_evidence':'PS-R-S25-DECISION: Apr1 core-team 결정이 인용되고 Apr20 원문이 반영됨.'})

p=swift(27,'String from Code Units','6aa016b50df07ccbff764e9159f971be594bf177','83bdc871121565084645b8fe792874594ae18fed','2016-02-23',
        '버퍼에서 효율적이고 안전한 문자열을 만들 때 널 종료·인코딩 제한, 재복사, 길이 재계산 문제가 있음을 확인했다.',
        ['버퍼→문자열 성능과 Unicode 안전성 고려','길이가 알려진 버퍼와 내부 널 문자 지원 문맥','불필요한 전체 복사·느린 원소별 처리 회피'],
        outcome='rejected',event='공식 저장소의 Rejected 상태 반영',
        sections=['Introduction: 직렬화·파일·통신 사용 문맥','Motivation: 마지막 두 문제 문단; 고속 API 이름과 Proposed solution은 제거'])
gold(p,'현재 API를 유지','Alternatives considered / Do nothing','필요한 생성자가 없어 순수 Swift 구현의 성능이 제한된다.')
gold(p,'mutable String.UTF8View와 UTF16View의 상각 O(1) append','Alternatives considered / views solution','고급 사용과 장기 API 유지에 더 나을 수도 있으나 당장의 제안은 영향이 작다고 비교한다.',stance='referenced')
gold(p,'SequenceType의 프로토콜 중심 decode API','Alternatives considered / protocol-oriented API','문자열과의 관계가 덜 명백하고 아직 없는 원소 타입 제약이 필요하다.')
gold(p,'NSString bridge 성능 개선','Alternatives considered / bridge faster','브리지 내부가 왜 느린지 명확하지 않아 버그 가능성을 열어 둔 대안이다.',ROLE_PART,'referenced','https://gist.github.com/zwaldowski/5f1a1011ea368e1c833e#file-nsstring-swift',boundary='현재 Swift 문자열 경로 안의 ObjC 재사용 부품이므로 다른 생태계 전체 제품으로 세지 않는다.')
gold(p,'String.append 성장 전략과 reserveCapacity 성능 개선','Alternatives considered / append faster','관측 성능이 문서상 상각 비용과 맞지 않으며 사전 토론에서 reserveCapacity 효과가 없다는 보고가 있었다.',ROLE_PART,'referenced','https://gist.github.com/zwaldowski/5f1a1011ea368e1c833e#file-unicodescalar-swift')

p=case('P0386','Changing the version comparison module in Distutils',
       '526ad628ce51892e4e7bd38402c74b59f8b626bd','b1c944fbd2c125a63c22a9b94f32d776e0cddc75',
       '2010-03-21','공식 저장소에 Accepted 상태를 기록한 커밋',
       ['Motivation: 의존성의 호환 버전 범위','Proposal: 자유로운 버전 문자열과 OS 재패키징 문제 문단만'],
       '버전 범위로 의존성을 제한하려면 신뢰할 비교가 필요하며 독자적 표기가 OS 재패키징을 어렵게 한다는 문제를 확인했다.',
       ['의존성 호환 범위를 위한 버전 비교','서로 다른 기존 표기와 OS 패키징 환경 고려','실제 버전 순서 판별'],
       gold_sections=['Requisites and current status / Distutils','Setuptools','Caveats of existing systems'],
       superseded=[dict(type='adopted_specification_replaced',url='https://github.com/python/peps/blob/df28da700d4b378bb6dd6f8d8cd67e54c6816c68/pep-0440.txt',pinned_version='df28da700d4b378bb6dd6f8d8cd67e54c6816c68',date='2014-08-22',scope='PEP440 수락과 함께 PEP386이 Superseded로 변경. 개발 버전 정렬 순서, 날짜 버전·version epoch·local identifier·호환 릴리스 범위를 확장하여 기존 표기의 이전 문제를 다룬다.')])
gold(p,'Distutils LooseVersion','Requisites and current status / Distutils','거의 모든 문자열과 여러 성분을 허용하지만 사전·사후·개발 릴리스에 필요한 의미를 표현하지 못한다.',ROLE_PART,'referenced','http://docs.python.org/distutils')
gold(p,'Distutils StrictVersion','Requisites and current status / Distutils','제한된 숫자 성분과 alpha/beta 선행 버전은 지원하지만 개발·사후 릴리스가 부족하다.',ROLE_PART,'referenced','http://docs.python.org/distutils')
gold(p,'Setuptools pkg_resources.parse_version','Requisites and current status / Setuptools','다양한 관행을 정렬 키로 바꾸지만 정책이 느슨하고 의미가 복잡하여 사람이 직접 순서를 예측하기 어렵다.',ROLE_PART,'referenced','http://peak.telecommunity.com/DevCenter/setuptools#specifying-your-project-s-version')
gold(p,'RPM의 날짜 버전에서 일반 숫자 버전으로의 전환','Caveats of existing systems','큰 날짜 숫자를 major로 사용한 뒤 일반 major.minor로 바꾸면 새 버전이 더 오래된 것으로 정렬되는 배포판 호환성 사례다.',ROLE_ECO,'referenced',boundary='OS 패키징과 Python 패키징의 다른 생태계 사례이며 먼 분야 원리로 세지 않는다.')
gold(p,'Debian/Ubuntu 패키징의 하이픈 취급','Caveats of existing systems','Setuptools의 하이픈 의미와 배포판 패키징의 규칙이 다르다는 상호 운용 비교다.',ROLE_ECO,'referenced',boundary='하나의 공통 규칙으로 함께 비교된 Debian/Ubuntu를 두 중복 항목으로 늘리지 않는다.')
p['sampling_correction']='최초 선별에서 Distutils를 한 도구로 뭉쳐 2개라고 판단한 오류를 발견했다. 원문이 StrictVersion과 LooseVersion을 각각 상세 비교하므로 규칙상 3개 이상이다. 기존 30개 접두부를 폐기하지 않고 C31을 gold 이전 별도 선행 커밋으로 추가한다.'
p['extraction_exclusions']=['easy_install/pip/zc.buildout는 사용 확산의 예시일 뿐 독립 비교 대상으로 설명되지 않아 제외.','Twisted의 사후 릴리스 표기는 선택된 비교 절 밖의 명세 설명 예시이므로 별도 골드에 더하지 않는다.']

UNLINKED_TARGETS={
    'P0201-G01','P0202-G01','P0202-G02','P0204-G01','P0204-G03',
    'P0433-G06','P0433-G07','P0554-G01','P0554-G02','S0016-G03',
    'S0018-G06','S0018-G07',
}
for c in cases:
    for item in c['gold_items']:
        if item['id'] in UNLINKED_TARGETS:
            item['url']=c['url']
            item['match_kind']='external_entity'
            item['url_note']='고정 원문은 비교 대상 이름만 제시하고 독립 외부 주소를 제공하지 않는다. 따라서 실제 읽은 고정 원문의 해당 section_anchor를 항목 출처로 사용한다.'
            if item['id']=='S0016-G03': item['boundary_note']='제안 원문이 C 코드로 문제를 처리하는 대안을 명시한다. 별도 C 표준의 기술적 적합성은 이 코딩에서 판정하지 않았다.'
            if item['id'] in ['P0433-G06','P0433-G07']: item['boundary_note']='C 라이브러리에서 Python API로 옮기는 동일 목적의 생태계 선례이며 먼 분야 원리가 아니다. 항목 주소는 해당 선례를 실제로 기록한 고정 제안 원문이다.'
    if c['id']=='S0022':
        c['review_gold_items']=[i for i in c['gold_items'] if i.get('gold_origin')=='review_addition']
        c['gold_items']=[i for i in c['gold_items'] if i.get('gold_origin')!='review_addition']
        c['review_gold_note']='고정 제안 본문의 primary 분모와 수락 토론에만 있는 확대 분모를 분리한다.'
    else:
        c['review_gold_items']=[]
    assert len(c['gold_items']) >= 3, c['id']
    assert c['prefix_version']['date'] != 'unconfirmed', c['id']
    assert c['gold_version']['date'] != 'unconfirmed', c['id']
    c['gold_item_count'] = len(c['gold_items'])
    c['gold_source_status'] = '독립 설계 원문·리뷰에서 추출; 분절·역할은 작업자 코딩'
    c['distant_principle_items'] = [i['id'] for i in c['gold_items'] if i['role']=='다른 분야 원리']
    c['review_gold_item_count'] = len(c['review_gold_items'])

if (HERE/'additional-sources.json').exists():
    sources += json.loads((HERE/'additional-sources.json').read_text())

(HERE/'draft-cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
(HERE/'sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'cases':len(cases),'gold_items':sum(len(c['gold_items']) for c in cases),'sources':len(sources),'by_case':{c['id']:len(c['gold_items']) for c in cases}},ensure_ascii=False))
