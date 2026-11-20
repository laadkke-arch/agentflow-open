"""Persist researcher summaries, screening decisions, and exact query strings."""
import json
from pathlib import Path
from datetime import datetime, timezone

P=Path(__file__).resolve().parent
NOW=datetime.now(timezone.utc).isoformat()
rows=[]
def src(sid,url,typ,title,version,sections,confirmed,limits,level='D1',used=None,count=False):
    rows.append(dict(id=sid,url=url,accessed_at_utc=NOW,source_type=typ,title=title,
                     version_or_date=version,sections_read=sections,confirmed=confirmed,
                     limits=limits,level=level,used_in=used or ['Q1','Q2','Q3','Q4'],
                     minimum_count_candidate=count,
                     access_note='accessed_at_utc는 직접 읽은 원문 묶음의 확인·기록 완료 UTC다. 개별 HTTP 최초 열람 시각은 보존하지 않아 정밀 시각으로 재구성하지 않았다.'))

src('PS-T-PEP1','https://peps.python.org/pep-0001/','template_procedure','PEP Purpose and Guidelines','live',
    ['PEP Maintenance','What belongs in a successful PEP?','Changing Existing PEPs'],
    'Motivation을 문제 설명으로, Rationale을 대안·관련 작업·다른 언어 선례의 기록으로 구분한다. Rejected Ideas는 토론에서 버린 안과 이유를 남기도록 한다. 최종 결정 뒤에는 대체로 역사적 문서로 유지하고 명세는 다른 문서에서 관리한다.',
    '절을 요구하는 절차가 모든 제안의 충실도나 정답 완전성을 보장하지 않는다. 현행 지침을 2000년 문서에 소급 강제하지 않는다.',count=True)
src('PS-T-PEP12','https://peps.python.org/pep-0012/','template_procedure','Sample reStructuredText PEP Template','live',
    ['How to Use This Template','Suggested Sections / Motivation, Rationale, Rejected Ideas, Open Issues','Change History'],
    '문제·명세·이유·기각안을 분리하는 실제 문서 골격이 제공된다. 현재판의 변경 기록에는 2026년 추가사항도 있으므로 초기 템플릿 역사는 Git 판으로 따로 확인했다.',
    '현행 템플릿이며 과거 제안이 그대로 따랐다는 증거가 아니다. python.org 최소수 상한 때문에 PEP1과 동시에 최소수에 넣을 필요가 없다.')
src('PS-T-PEP1-INITIAL','https://raw.githubusercontent.com/python/peps/41021a4bf9c3d410c7082cb514d8805e1eea2c8d/pep-0001.txt','template_historical','PEP1 first repository version','41021a4bf9c3d410c7082cb514d8805e1eea2c8d',
    ['초기 파일의 Rationale/alternative 문자열·절 존재 검사'],
    '최초 저장소 판에는 후속 확장판의 대안·다른 언어 선례 지침이 없음을 확인했다.',
    'Git 이관 전 사적 또는 외부 초안의 존재는 배제하지 않는다. 본문 근거 개수에는 별도 산입하지 않는다.','D3-fetch',['Q1'])
src('PS-T-PEP1-2000','https://raw.githubusercontent.com/python/peps/86fcb76ff6763002f89de3309de9de83cac21ba7/pep-0001.txt','template_historical','PEP1 expanded content guidelines','2000-07-25 / 86fcb76ff6763002f89de3309de9de83cac21ba7',
    ['What belongs in a successful PEP? / item 6 Rationale'],
    '관련 대안, 고려한 설계, 다른 언어의 같은 기능, 토론의 반대 의견을 Rationale에 기록하도록 한 지침이 이 판에 존재한다.',
    '별도의 Rejected Ideas 제목이 처음부터 있었다는 뜻은 아니다. 최초판과 두 번째 파일 변경 사이의 비교로 저장소 내 도입 시점을 판단했다.',used=['Q1'])
src('PS-T-PEP12-2002','https://raw.githubusercontent.com/python/peps/9ca8e6bba0d828c067d3c101fe204a74584e275e/pep-0012.txt','template_historical','PEP12 initial format template','2002-08-26 / 9ca8e6bba0d828c067d3c101fe204a74584e275e',
    ['Rationale','How to Use This Template'],
    '초기 PEP12는 reStructuredText 형식 안내에 집중하며 작성자는 Abstract·Rationale 등을 채우도록 되어 있었다. 후대의 완성된 Rejected Ideas 섹션 골격은 아직 없다.',
    '문서 형식 템플릿과 PEP1의 내용 지침은 서로 다른 역사다.',used=['Q1'])
src('PS-T-PEP12-BEFORE','https://raw.githubusercontent.com/python/peps/d69b083262d844a70735f6a9ef889acc0e2a8867/pep-0012.rst','template_historical','PEP12 before suggested-sections insertion','2019-03-06 / d69b083262d844a70735f6a9ef889acc0e2a8867',
    ['How to Use This Template','Rejected Ideas heading absence check'],
    'Rejected Ideas 제목이 없고 Abstract·Rationale 등의 작성 지침은 유지된다.',
    '과거 모든 외부 문서 관행을 배제하지 않는 저장소 판 비교다.',used=['Q1'])
src('PS-T-PEP12-2019','https://raw.githubusercontent.com/python/peps/8e7b03ab1da7c26ff75cf152e075bebe96f567a1/pep-0012.rst','template_historical','PEP12 suggested sections introduced','2019-03-08 / 8e7b03ab1da7c26ff75cf152e075bebe96f567a1',
    ['Suggested Sections / Motivation, Rationale, Rejected Ideas, Open Issues'],
    '직전 판에 없던 Suggested Sections 골격에 Rejected Ideas와 Open Issues가 포함된다. 기각안을 토론 결과와 함께 기록하는 구분이 템플릿 자체에 명시되었다.',
    'PEP1의 대안 기록 지침은 이미 2000년에 있었으므로 2019년을 대안 기록 관행 전체의 시작으로 해석하지 않는다.',used=['Q1'])
src('PS-T-SWIFT-INITIAL','https://raw.githubusercontent.com/swiftlang/swift-evolution/d444b1f8b827e759d6c18c9b0246cb882d8f16a1/0000-template.md','template_procedure','Swift Evolution initial proposal template','2015-11-03 / d444b1f8b827e759d6c18c9b0246cb882d8f16a1',
    ['Introduction','Motivation','Proposed solution','Detailed design','Alternatives considered'],
    '저장소의 root commit부터 문제 설명과 대안 비교 절이 분리되어 있다. Alternatives considered는 같은 문제의 다른 접근과 선택 이유를 기록하도록 요구한다.',
    '초기 공개된 몇 제안은 이미 Accepted여서 이 템플릿만으로 결정 전 입력을 복원할 수 없다.',used=['Q1','Q2'],count=True)

history_urls=[
 ('PS-H-T-P1','https://api.github.com/repos/python/peps/commits?path=pep-0001.txt&per_page=100'),
 ('PS-H-T-P1-2','https://api.github.com/repos/python/peps/commits?path=pep-0001.txt&per_page=100&page=2'),
 ('PS-H-T-P12','https://api.github.com/repos/python/peps/commits?path=pep-0012.txt&per_page=100'),
 ('PS-H-T-P12-RST','https://api.github.com/repos/python/peps/commits?path=pep-0012.rst&per_page=100'),
 ('PS-H-T-SWIFT','https://api.github.com/repos/swiftlang/swift-evolution/commits?path=0000-template.md&per_page=100'),
 ('PS-H-P554-NEW','https://api.github.com/repos/python/peps/commits?path=peps/pep-0554.rst&per_page=100'),
 ('PS-H-P649','https://api.github.com/repos/python/peps/commits?path=pep-0649.rst&per_page=100'),
 ('PS-H-P699','https://api.github.com/repos/python/peps/commits?path=pep-0699.rst&per_page=100'),
 ('PS-H-S169','https://api.github.com/repos/swiftlang/swift-evolution/commits?path=proposals/0169-improve-interaction-between-private-declarations-and-extensions.md&per_page=100'),
]
for sid,url in history_urls:
    src(sid,url,'repository_history_api','Template or successor path history','live',
        ['sha, commit.committer.date, parents; filtered history metadata'],
        '초기 템플릿·절 삽입 또는 후속 수락·대체 사건의 고정 SHA와 시각을 확인했다. 개인정보와 전체 commit 본문은 저장하지 않았다.',
        'API의 경로 이력은 파일 rename 전후를 따로 읽어야 한다. 메일 결정과 Git 반영은 동일 시각이라고 보지 않는다.','D3-fetch',['Q1','Q2'])

src('PS-SU-P0201','https://raw.githubusercontent.com/python/peps/6e249d895555a5e330718a661678ef3827fa708a/pep-0201.txt','successor_design','Subsequent change to zip','2003-08-02 / 6e249d895555a5e330718a661678ef3827fa708a',
    ['Subsequent Change to zip()','Other Changes'],
    'Python2.4의 무인수 호출을 예외에서 빈 목록으로 바꾸기로 한 이유가 기록되어 있다. 가변 인수 펼침으로 행열을 바꾸는 작업에서 빈 데이터도 자연스럽게 처리한다. 별도 지연 함수도 Python2.3에서 추가되었다.',
    '전치 예시는 2000년 문서에도 일부 있었으므로 원리를 처음 발견한 사건이라고 해석하지 않는다. 초기 prefix에 빈 역변환 문제가 명시되지는 않았다.',used=['Q2','Q7','Q8'])
src('PS-SU-P0354','https://raw.githubusercontent.com/python/peps/4434e728a7db24540d581f52e96570ca1230356e/peps/pep-0435.rst','successor_design','PEP435 replacement enumeration design','4434e728a7db24540d581f52e96570ca1230356e',
    ['Abstract','Status of discussions','Motivation','Creating an Enum'],
    'PEP354를 대체하며 2013-05-10 수락을 명시한다. 정수 상수 호환을 위한 IntEnum과 일반 Enum을 나누고 멤버가 해당 열거 타입에 속하게 설계한다.',
    '회고 문단의 PEP354 기각 연도 2005는 2006년 첫 초안·2007년 거절 Git 기록과 어긋난다. 후속 회고의 연도를 무검증 기준일로 쓰지 않았다.',used=['Q2','Q7','Q8'])
src('PS-SU-P0433','https://raw.githubusercontent.com/python/peps/4434e728a7db24540d581f52e96570ca1230356e/peps/pep-0446.rst','successor_design','PEP446 non-inheritable descriptors','4434e728a7db24540d581f52e96570ca1230356e',
    ['Abstract','Rationale / inheritance on UNIX and Windows','Atomic creation'],
    'PEP433을 대체하고 Python이 만든 디스크립터를 기본 비상속으로 바꾸며 가능한 OS에서 원자적 플래그로 경합을 피한다.',
    '초기 PEP433은 채택 상태를 거친 것이 아니므로 채택 뒤 번복 수에 넣지 않는다. 이 자료가 모든 OS 동작을 직접 검증한 실행은 아니다.',used=['Q2','Q7','Q8'])
src('PS-SU-P0509','https://raw.githubusercontent.com/python/peps/ab15de6ab836f41e6be797b4de380a0233066ce8/pep-0699.rst','successor_design','PEP699 rescinding dict version specification','2023-01-18 / ab15de6ab836f41e6be797b4de380a0233066ce8',
    ['Abstract','Motivation','Status and Replaces headers'],
    'PEP509의 사적 버전 필드 사양을 철회한다. 3.11의 특수화가 다른 가드 방식을 쓰게 되어 필드를 다른 최적화 정보에 재사용하도록 한다.',
    '이는 원래 목적이 무가치했다는 실험이 아니라 구현 환경과 최적화 전략이 바뀐 사례다.',used=['Q2','Q7','Q8'])
src('PS-SU-P0554','https://raw.githubusercontent.com/python/peps/6aeaba7f23a1ce373e099a2b35db9525dbb11f6d/peps/pep-0734.rst','successor_design','PEP734 initial replacement draft','2023-11-28 / 6aeaba7f23a1ce373e099a2b35db9525dbb11f6d',
    ['Status/Replaces headers','Abstract','Introduction / interpreters and threads'],
    'PEP554 대체 초안은 인터프리터 API와 Queue 및 InterpreterPoolExecutor를 함께 제안한다. 같은 커밋의 새 문서는 아직 Draft다.',
    '이 시점의 대체는 최종 제품 채택이 아니다. 후속 최종 수락은 원 표본의 2024년 관측 창 밖이다.',used=['Q2','Q7','Q8'])
src('PS-SU-P0554-LATE','https://raw.githubusercontent.com/python/peps/4434e728a7db24540d581f52e96570ca1230356e/peps/pep-0734.rst','successor_design','PEP734 later final status','4434e728a7db24540d581f52e96570ca1230356e',
    ['Status/Replaces/Resolution headers','Abstract','Motivation'],
    '현행 고정 판은 Final이고 Resolution 날짜는 2025-06-05로 기록되어 있다.',
    '표본 결정 창 밖의 후속 상태다. 초기2023 대체를 수락으로 바꾸는 근거로 쓰지 않는다.',used=['Q2'])
src('PS-SU-P0563','https://raw.githubusercontent.com/python/peps/a111ec493be2d52356c1451f074e4a7c70d9ad82/pep-0649.rst','successor_design','PEP649 accepted deferred annotations design','2023-05-16 / a111ec493be2d52356c1451f074e4a7c70d9ad82',
    ['Abstract','Overview','Comparison of Annotation Semantics','Mistaken Rejection Of This Approach In November 2017'],
    '문자열화 annotation이 런타임 사용자에게 준 문제를 지적하고 계산 함수와 descriptor로 대체한다. 2017년 implicit lambda 기각을 명시적으로 재검토하며 새 메커니즘은 클래스·지역·자유 변수 접근을 처리한다고 설명한다.',
    '그때 제안된 모든 lambda 설계와 후속 구현이 같다는 뜻은 아니다. 회수 적중이 실제 후속 설계를 완성했다는 효과 증거도 아니다.',used=['Q2','Q7','Q8'])
src('PS-SU-S0025','https://raw.githubusercontent.com/swiftlang/swift-evolution/17bc96ea9f23b1becfe91bfd72bd0c006390fd58/proposals/0169-improve-interaction-between-private-declarations-and-extensions.md','successor_design','SE0169 accepted access-control revision','2017-04-18 / 17bc96ea9f23b1becfe91bfd72bd0c006390fd58',
    ['Introduction','Motivation','Detailed Design','Source Compatibility','Alternatives Considered'],
    'SE0025의 좁은 scope가 같은 타입의 extension 사용을 불편하게 해 fileprivate가 예상보다 흔해졌다고 기록한다. 같은 파일의 동일 타입과 extensions를 공통 private scope로 보는 제한된 변경을 수락했다.',
    '완전한 접근 제어 폐기가 아니다. 다른 파일·다른 타입·subclass까지 같은 접근을 확장하지 않는다.',used=['Q2','Q7','Q8'])

src('PS-R-S21-LENS','https://forums.swift.org/t/proposal-expose-getter-setters-in-the-same-way-as-regular-methods/501/3.json','review_discussion','Review proposal of lenses for properties','2015-12-17T02:59:32Z',
    ['post3 본문: lens, recursive writeback, copy-on-write'],
    'getter와 setter를 따로 노출하는 것만으로는 값 타입의 부분 갱신과 copy-on-write 효율이 부족하다는 반론이 제시된다. 전체 속성 접근을 보존하는 lens를 제안하며 고정 SE0021이 이 토론을 연결한다.',
    '포럼 이관으로 updated_at은2018년이다. created_at의 원 메일 시각을 사용하며 공개 토론 전체를 전수 추적하지 않았다.',used=['Q3','Q4','Q7'])
src('PS-R-S21-PARTIAL','https://forums.swift.org/t/proposal-draft-generalized-naming-for-any-function/787/6.json','review_discussion','Review proposal of placeholder partial application','2015-12-29T17:10:50Z',
    ['post6 본문: placeholder argument proposal; 인용된 기존 초안과 비교'],
    '자리표시자 인수로 일반 partial application을 만들고 모든 자리를 비우면 함수 이름 참조가 되는 대안이 토론에서 제시된다. 고정 SE0021은 이 글을 연결하고 일반성의 비용을 이유로 따르지 않는다.',
    '기여자의 이름과 메일 주소·본문 전문은 저장하지 않는다. 전체 토론에서 최초 발명자였다는 주장은 하지 않는다.',used=['Q3','Q7'])
src('PS-R-S22-ACCEPT','https://forums.swift.org/t/accepted-se-0022-referencing-the-objective-c-selector-of-a-method/1194.json','review_discussion','SE0022 review acceptance and alternatives','2016-01-26T22:16:32Z',
    ['post1 전체: accepted syntax and alternatives a,b,c'],
    '수락은 #selector 표기를 조건으로 한다. 암묵적 selector 변환, 특수 생성자, 함수의 특수 멤버라는 세 대안과 타입 시스템·미래 멤버 공간의 비용을 명시한다.',
    '암묵 변환과 특수 멤버 둘은 고정 제안 본문에 없으므로 review-only 확대 골드에만 넣는다.',used=['Q2','Q3','Q7'])
src('PS-R-S25-DECISION','https://forums.swift.org/t/se-0025-scoped-access-level-next-steps/1797/131.json','review_discussion','SE0025 final naming decision quoted in review','2016-04-04T14:54:20Z; quoted decision 2016-04-01',
    ['post131 확인 질문과 인용된 Apr1 core-team 결정'],
    'Apr4 확인 글에는 Apr1에 public/internal/fileprivate/private로 최종 결정했다는 공식 메일이 인용된다. 일반적인 private 기대와 기존 코드 변경량을 선택 이유로 기록한다.',
    'Apr1 원 메일의 독립 post ID는 확인하지 못했다. 원 기록은 같은 thread와 원 mailing-list 주간 archive에서 더 확인할 수 있다. Git 반영은Apr20이며 동일 날짜로 합치지 않았다.',used=['Q2','Q3','Q7'],count=True)
src('PS-R-S16-ACCEPT','https://forums.swift.org/t/accepted-se-0016-adding-initializers-to-int-and-uint-to-convert-from-unsafepointer-and-unsafemutablepointer/2005.json','review_discussion','SE0016 accepted unsafe-pointer conversions','2016-03-31T04:11:54Z',
    ['post1 전체'],
    '수락 글은 주소에서 정수로 되돌리는 빈틈을 메우고 기존 bitPattern 표기와 일관성을 유지하는 이유를 설명한다.',
    '추가 대안은 나오지 않는다. 현재 구현을 직접 실행한 관측이 아니다.',used=['Q2','Q3'])
src('PS-R-S169-ACCEPT','https://forums.swift.org/t/accepted-se-0169-improve-interaction-between-private-declarations-and-extensions/5692.json','review_discussion','SE0169 accepted after access-control experience','2017-04-18T00:25:21Z',
    ['post1 앞부분: review dates, acceptance, scope tradeoffs'],
    '2017-04-06~11 리뷰 뒤 수락했음을 명시한다. 기존 scoped access 사용을 보존하면서 extension 친화적 동작으로 바꾸려는 상충된 요구를 설명한다.',
    '댓글 전체가 같은 의견이라는 뜻은 아니다. 사용자가 실제로 더 나은 결과를 얻었는지 여기서 측정하지 않는다.',used=['Q2','Q3','Q7'])
src('PS-R-P563-LAMBDA','https://mail.python.org/pipermail/python-dev/2017-November/150109.html','review_discussion','PEP563 implicit-lambda objection','2017-11-03T14:40:48Z',
    ['메일 본문과 앞선 제안의 인용: implicit lambda, class-level names'],
    'implicit lambda 방식의 설명 가능성을 주장한 토론에 대해 클래스 수준 정의를 메서드 annotation에서 참조할 수 없다는 이유로 부정적 판단을 내린다. 후속 PEP649가 이 메시지를 잘못된 기각의 근거로 직접 연결한다.',
    '한 메시지는 모든 lambda 구현의 불가능성이나 토론 전체 합의를 입증하지 않는다. 본문에서 제시한 제약과 후속 구현을 구분한다.',used=['Q3','Q7','Q8'],count=True)
src('PS-R-P563-ACCEPT','https://mail.python.org/pipermail/python-dev/2017-December/151042.html','review_discussion','PEP563 official acceptance','2017-12-04T16:42:38Z',
    ['수락 선언과 editorial-note 문단','인용된 Draft3의 Rationale/Non-goals 일부'],
    '2017-12-04 수락을 명시하며 남은 편집 의견은 수락을 바꾸지 않는다고 한다. Draft3의 런타임 annotation 호환성 취급이 최초 초안보다 좁아졌음도 확인된다.',
    '메일 인용에 긴 초안이 붙어 있으나 전문을 저장하지 않았다. 접두부 동결의 Git 날짜12/5를 실제 결정12/4와 구분한다.',used=['Q2','Q3','Q7'],count=True)

src('PS-SU-P0386','https://raw.githubusercontent.com/python/peps/df28da700d4b378bb6dd6f8d8cd67e54c6816c68/pep-0440.txt','successor_design','PEP440 accepted replacement version scheme','2014-08-22 / df28da700d4b378bb6dd6f8d8cd67e54c6816c68',
    ['Abstract','Summary of differences from PEP386','Changing the version scheme','Support for date based version identifiers','Adding version epochs','Adding local version identifiers'],
    'PEP386을 대체하며 개발 버전의 정렬을 기존 pkg_resources 동작과 맞춘다. 날짜 기반 버전·버전 epoch·로컬 빌드 식별자를 지원하여 기존 프로젝트와 OS 배포판의 이전 및 패치 빌드 문제를 다룬다.',
    '2010년 초안의 넓은 목적에는 버전 비교가 있지만 후속의 모든 구체 제약이 명시된 것은 아니다. 후속 문서를 원래 골드에 소급 편입하지 않는다.',used=['Q2','Q7','Q8'])
(P/'additional-sources.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')

selection=[]
def screen(cid,family,stratum,outcome,reason,url,sha,detail,method='manual_comparison_section_read'):
    selection.append(dict(canonical_id=cid,family=family,stratum=stratum,screen_order=len(selection)+1,
                          outcome=outcome,reason=reason,url=url,pinned_version=sha,
                          opened_at_utc=NOW,detail=detail,screening_method=method))
PY_SHA='4434e728a7db24540d581f52e96570ca1230356e'
sup=[(215,'excluded','fewer_than_3_items','Discussion의 구체 대안은 연산자형 구현 등으로3개 미만. 다른 언어를 포괄적으로 언급하지만 독립 이름·구조를3개 제시하지 않는다.'),
     (241,'excluded','no_comparison_section','패키지 메타데이터 사양 중심으로 독립 비교 항목3개를 확인하지 못함.'),
     (314,'excluded','no_comparison_section','메타데이터 갱신 사양이며 비교 항목3개를 확인하지 못함.'),
     (344,'excluded','no_explicit_supersession','PEP3134로 번호를 바꾼 대체를 결정 변경으로 세지 않음.'),
     (345,'excluded','no_comparison_section','메타데이터 필드 사양이며 독립 대안3개를 확인하지 못함.'),
     (354,'included','eligible','기각된 제안의 실제 대체; 비교 설계4개.'),
     (367,'excluded','no_explicit_supersession','PEP3135로의 재번호화 자체를 의미 변경으로 세지 않음.'),
     (386,'included_correction','eligible','초기 도구 단위 묶음은 오류. StrictVersion/LooseVersion/parse_version은 각각 실질 비교 대상이므로 추가 C31로 복구.'),
     (431,'excluded','fewer_than_3_items','withdrawn→새 제안은 확인되지만 해당 비교절에서 독립 항목3개를 확보하지 못함.'),
     (433,'included','eligible','Draft supersession; 비상속 전략과 다른 언어 선례.'),
     (509,'included','eligible','채택 후 사양 철회; 기능 대안3개와 prior art5개.'),
     (554,'included','eligible','Draft supersession; API·예외 처리 대안19개.'),
     (563,'included_retained_after_correction','eligible','초기 동결에 포함했던 적격 사례를 유지. 채택 후 PEP649로 실질 대체.'),
     (622,'not_selected','eligible_beyond_quota','현재 본문 비교절이 풍부함을 확인했지만 대체층 선행 적격 수를 채운 뒤여서 신규 선정하지 않음.'),
     (631,'not_selected','eligible_beyond_quota','선행 대체층 수 충족 뒤 미선정; 짧은 메타데이터 문서.'),
     (3153,'not_selected','eligible_beyond_quota','선행 대체층 수 충족 뒤 미선정; 비동기 I/O 구조 비교가 존재함.')]
for n,outcome,reason,detail in sup:
    screen(f'P{n:04d}','Python PEP','superseded',outcome,reason,f'https://raw.githubusercontent.com/python/peps/{PY_SHA}/peps/pep-{n:04d}.rst',PY_SHA,detail)
for n,outcome,reason,detail in [
    (100,'excluded','no_comparison_section','헤더와 전체 절 목록에서 독립 비교절을 찾지 못함. 초기 공통 root commit의 pep-0100.txt는404. 이 실패만으로 역사 전체의 초안 부재를 주장하지 않음.'),
    (201,'included','eligible','초기 문제 문맥과 수락판의 비교 항목7개 확보. 추가로 후속 부분 변경도 확인.'),
    (202,'included','eligible','얇지만 독립된 Rationale 목적 문장과 비교항목6개 확보.'),
    (203,'excluded','fewer_than_3_items','기존 이항 연산과 제자리 갱신의 의미 비교를 독립 선행 항목3개로 분절하지 않음.'),
    (204,'included','eligible','range/slice와 Open issues의 독립 설계 대안을 확보.')]:
    screen(f'P{n:04d}','Python PEP','general',outcome,reason,f'https://raw.githubusercontent.com/python/peps/{PY_SHA}/peps/pep-{n:04d}.rst',PY_SHA,detail)

swift=json.loads((P/'swift-screening-first65.json').read_text())
SWIFT_INCLUDE={16,18,19,20,21,22,25,27}
SWIFT_REASON={1:'기존 문법과 개별 escaping의2개 수준',2:'최초 공개판이 이미Accepted; 결정 전 입력 복원 불가',3:'변경 재검토 설명은 있으나 독립 항목3개 미만',4:'최초 공개판이 이미Accepted; 결정 전 입력 복원 불가',5:'비교절 없음',6:'비교절 없음',7:'현상 유지 한 가지',8:'비교절 없음',9:'명시적 self의 제한 대안 한 가지',10:'통합 기능으로 미루는 대안 등3개 미만',11:'비교절 없음',12:'API notes 한 가지의 여러 단점;3개 대안으로 세지 않음',13:'상속 타입 표현 대안3개 미만',14:'비교절 없음',15:'variadic generics로 미루는 한 가지',17:'기존 Unmanaged 구조 유지 등3개 미만',23:'비교절 없음',24:'대입 표기 한 가지',26:'프로토콜·attribute 대안2개'}
for r in swift:
    n=int(r['canonical_id'])
    if n>27:
        screen(f'S{n:04d}','Swift Evolution','prefetch_after_quota','not_used','eligible_beyond_quota',r['url'],r['pinned_version'],
               '일괄 선별용 응답을 메모리에서 가져와 비교절 길이만 계산했다. 포함 판정이나 D1 본문 개수로 세지 않는다.','automated_section_length_screen_only')
        continue
    if n in SWIFT_INCLUDE:
        screen(f'S{n:04d}','Swift Evolution','general','included','eligible',r['url'],r['pinned_version'],'초기 고정 문맥·결정 증거·3개 이상 비교 항목을 개별적으로 확인.')
    else:
        reason='prefix_not_historically_recoverable' if n in [2,4] else ('no_comparison_section' if r['alt_chars']==0 else 'fewer_than_3_items')
        screen(f'S{n:04d}','Swift Evolution','general','excluded',reason,r['url'],r['pinned_version'],SWIFT_REASON.get(n,'독립 비교 대상3개 미만'))
(P/'selection.json').write_text(json.dumps(selection,ensure_ascii=False,indent=2)+'\n')

logs=[]
def log(kind,q,purpose,result):
    logs.append(dict(id='PS-Q'+str(len(logs)+1).zfill(3),kind=kind,query_string=q,
                     timestamp_utc=NOW,purpose=purpose,result=result,
                     timestamp_note='질의 문자열은 실제 실행 그대로이며 이 시각은 해당 원문 열람 묶음의 기록 완료 UTC다. 개별 최초 요청 시각은 보존하지 않았다.'))
log('official_index_open','https://peps.python.org/pep-0000/','대체층 공식 목록','Superseded 목록16개를 번호순으로 선별; 사용자명·본문 전문 저장 안 함.')
for c in json.loads((P/'draft-cases.json').read_text()):
    log('github_history_api',c['decision_evidence_url'] if c['decision_evidence_url'].startswith('https://api.github.com/') else f"https://api.github.com/repos/{'python/peps' if c['id'].startswith('P') else 'swiftlang/swift-evolution'}/commits?path={c['prefix_version']['url'].split('/',6)[-1]}&per_page=100",'초기판·결정판 이력','history-metadata-complete.json 또는 history-P386.json에 SHA/date/parents만 저장')
    log('direct_open',c['prefix_version']['url'],'누설 없는 초기 문제 문맥 추출','읽은 절은 사례 prefix_sections')
    log('direct_open',c['gold_version']['url'],'고정 판의 골드 추출','항목과 분절 제외는 draft-cases.json')
for sid,url in history_urls:log('github_history_api',url,'템플릿 도입 또는 후속 결정의 이력','관련 추가 source '+sid)
for r in rows:
    if r['source_type']!='repository_history_api':log('direct_open',r['url'],'템플릿·리뷰·대체 원문 직접 읽기',r['id'])
for r in selection:log('direct_open',r['url'],'번호순 표본 스크리닝',r['canonical_id']+': '+r['reason'])
log('system2_search_query','site:forums.swift.org "SE-0025" "accepted" "Apr" 2016','Apr1 원 수락 메시지의 독립 주소 탐색','후속 SE0169와 회고 토론이 검색됨; Apr1 원 메시지 위치를 추가 확보하지 못함. snippet은 본문 근거로 세지 않음.')
log('system2_search_query','site:forums.swift.org "core team met" "fileprivate" "April 1"','최종 명칭 결정 메시지 탐색','정확 원글 주소를 얻지 못함. 이미 연 공식 thread의 인용 증거와 Git 반영을 분리 유지.')
log('system1_search_query','site:forums.swift.org "settled on the list above" "private"','검색엔진 교차 확인','부적합 결과; 새 근거로 쓰지 않음.')
(P/'SEARCH_LOG.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'additional_sources':len(rows),'selection_records':len(selection),'search_log_records':len(logs)}))
