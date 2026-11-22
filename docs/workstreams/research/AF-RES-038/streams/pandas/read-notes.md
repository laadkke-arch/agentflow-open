# pandas 원문 판독과 표집 메모

## 범위·순서와 관측 수준

이 stream은 P02 whole + P04 partial + P06 partial의 최초 formal PDEP, 동시대 해법 근거, 상세 기준과 후대 재검을 담당했다. selection-seal.json은 2026-11-22T18:36:03.612Z에 번호순 선정 근거를 기록했다. 원격 사전계약 7b977101c53730a5d6f5028a4ac540e045a6f84e 확인 뒤 조사했다. 현행 directory/status와 commit/PR 제목은 선정 전에 노출됐다. 상세 후대 test/decision은 봉인 뒤에 읽었다. 따라서 완전한 outcome-blind 표집이라고 부르지 않는다.

sources.jsonl의 count=true는 20개 고유 원문 그룹이다. 핵심 배분은 최초 formal proposal3, 동시대 대안 spec6, criterion3, later3 =15이며 supplement5가 추가된다. screening/전사범위 불완전 원문은 count=false로 남긴다. 같은 PDEP의 첫판과 개정판을 2개로 부풀리지 않는다. POC의 여러 파일, meson-python README+code도 각각 한 그룹으로 묶었다. 이 자료를 실제 실행한 것은 없으며 9개 제출은 AI 저자의 구성 예시다. human performance, 노동 시간, effect size, external human agreement는 미실시다.

## 최초판·작성일·공개일

|사건|문서 Created|commit author timestamp|검증한 formal PR 공개|한계|
|---|---|---|---|---|
|P02|2022-08-05|2022-08-06T02:29:39Z|2022-08-06T02:30:16Z, PR47988|최초 아이디어는 이전 POC에 있었음. first formal PDEP와 구별|
|P04|2022-09-18|2022-09-18T13:31:45Z|2022-09-18T13:36:32Z, PR48621|이전 이슈들이 동기이며 earliest immutable formal revision을 고정|
|P06|2022-12-23|2022-12-22T21:31:28Z|2022-12-23T21:57:17Z, PR50424|원 idea issue39584는 2021-02-03, fractional 처리 미결. formal PDEP가 그 결정을 구체화|

P06 첫판의 Discussion #50402는 실제 PR URL 404였다. 실제 formal PR50424 본문은 original discussion #39584 및 int→float 검토 목적을 명시한다. issue39584의 현행본문 원작성판은 immutable하지 않아 첫 내용 전체를 복구했다고 하지 않는다. 2021 원 아이디어부터 fractional reject가 합의됐다고 소급하지 않는다.

## 번호순 제외의 실질 이유

PDEP1은 절차/거버넌스다. PDEP3의 단일 Styler renderer 목적에서 기존 별도 HTMLFormatter를 두 번째 정답으로 두면 원 요구를 바꾸게 된다. PDEP5의 전역 opt-in no-row-index 모드에서 매번 reset_index를 하는 관행을 정답으로 두면 목적을 보존하지 못한다. 둘째 해법을 입증하지 못한 상태로 제외했으며 가능한 해법 자체가 없다고 증명한 것은 아니다.

PDEP7은 P02보다 뒤이고 2023 Git 문서가 2021 Google 초안의 이관이다. 2021 공개 메일과 2020 issue는 읽었지만 전체 첫 Google Doc 본문은 복구하지 못했다. eager-copy는 copy 회피 요구를 위반하므로 쉬운 대안으로 넣지 않았다. PDEP8~18은 할당 확보 뒤 제목/최초 PR metadata만 보았고 full eligibility를 판정하지 않았다. 19/20 검색 부재는 존재하지 않는다는 증명이 아니다. 전체 20행과 same-number 재사용은 frame.csv에 보존한다.

## P02: 이름으로 판정하면 틀리는 전체 설계

원판 [P-S01](https://github.com/pandas-dev/pandas/blob/aad11f695cacd7a07a35f4e31b8e0d1fc9a2767f/web/pandas/pdeps/0002-build-system-overhaul.md#L10-L32)이 CMake와 Meson을 이미 양립 가능한 후보로 제시한다. [CMake 당대 POC](https://github.com/pandas-dev/pandas/blob/d62f894c3ec08b721de0499cabe2c58a6e322496/build_support/build_backend.py)는 native compile을 외부 graph로 옮기고 wheel/metadata만 기존 packaging 라이브러리에 위임한다. 따라서 setuptools를 사용한다는 이유로 오탈락시키는 기준을 버렸다. 반대로 wheel을 잘 만들고 workerflag를 전달한다는 설명만으로 setup.py 컴파일 monolith를 유지하는 예시를 통과시키면 원 목표를 놓친다.

[Meson POC](https://github.com/lithomas1/pandas/blob/7e401dc31ca155fcc7b3128ee7a7b43989c71da3/meson.build)의 pyproject는 meson-python을 @main으로 지정했고 versioneer 관련 comment도 있다. 공개된 [0.7.0 backend](https://github.com/mesonbuild/meson-python/blob/2f9acf25e23de95b0ceead72770cad4acf19a449/README.md)는 실제 당시 원문이지만 그 버전으로 POC가 성공했다는 연결 증거는 없다. P02의 두 예시는 design/document consistency pass이며 실제 build pass가 아니다. 기본 platform 범위를 조용히 Linux만으로 줄이지 않는다. [PEP517](https://github.com/python/peps/blob/19f2582774070b86cc4f8866d5c751f8cb7c56ee/pep-0517.txt#L198-L284)의 read-only source 지원은 mandatory가 아니므로 그 한계로 정답을 탈락시키지 않는다.

후대 [PR49115](https://github.com/pandas-dev/pandas/pull/49115) body는 backend 전환을 미래로 적은 stale text인데 merged diff는 mesonpy를 실제 추가한다. 따라서 fixed merge 730439603919b9a38a54477f768b775f1aaf6412의 pyproject와 개발 문서를 기준으로 썼다. 후대 채택이 CMake의 원래 적합성을 지우지 않는다. import 자동 rebuild는 새 편의이므로 예방가능 재작업으로 세지 않는다.

## P04: 두 날짜의 성공을 강요하면 정당한 strict 실패를 오탈락

초안은 explicit DMY 경로만으로 작은 과제를 구성하려 했다. 별도 root 검토에서 최초 PDEP가 first-non-NaN inference도 허용한다는 반례를 적용했다. 고정 예시 두 개는 explicit DMY지만 다른 참가자가 first-row MDY를 고정하고 다음 13-01에서 raise하면 pass다. declared_mode / declared_format(or inference rule) / format_used / errors를 제출 필드로 둔다. 관측한 invariant는 batch 내 형식 변경 여부이며 Jan12/Jan13 출력의 강제가 아니다. 이 정정은 blind 예시 판독 전이며 사람 결과나 측정 분모의 변경은 없다.

[원판](https://github.com/pandas-dev/pandas/blob/e59b6ffd4881ecebb1d3739080d16e162660ae83/web/pandas/pdeps/0004-consistent-to-datetime-parsing.md)의 infer_datetime_format=True 반례는 Dec1→Jan13이라는 silent format switch다. [pandas1.4.4](https://github.com/pandas-dev/pandas/blob/ca60aab7340d9989d9428e11a51467658190bb6b/pandas/core/tools/datetimes.py) explicit format과 [CPython3.10.6](https://github.com/python/cpython/blob/9c7b4bd1646f2170247f88cf59936740d9c4c004/Doc/library/datetime.rst) 고정 strptime은 다른 구현/반환 타입으로 같은 literal 계약을 만족시킬 수 있다. 반복 파싱이 느릴 것이라는 추정으로 후자를 fail 처리하지 않는다. Python strptime의 zero-padding/범위와 pandas의 nanosecond/timezone 차이는 별도 범위로 남긴다. 별도 wrapper에서 first-non-NaN을 추론하는 완성 구현 자체는 이번 고정 예시로 검증하지 않았다.

후대 [PR50939](https://github.com/pandas-dev/pandas/pull/50939)의 mixed/ISO8601 named modes는 최초 strict invariant를 폐기한 증거가 아니라 opt-in 기능 확장이다. 두 t1 batch는 모든 참가자에게 공통 제공하고 정답 출력은 과제지에서 제거한다.

## P06: dtype 이름이 아니라 생성 계약과 손실을 함께 본다

native int64를 사후 nullable Int64로 바꾸고 dtype을 보존했다고 말할 수 없다. 이번 과제는 처음 만들 schema를 두 방식 중 고를 수 있게 한 부분과제이며 그 설정은 t0 공통 문구다. [P-S08](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/dtypes/cast.py#L1931-L2009)은 내부 lossless guard이고 그것을 소비자 setter 앞에 배치하는 구현은 저자의 구성적 추론이다. [P-S09](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/arrays/masked.py#L198-L235) nullable setter와 [P-S12](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/tests/arrays/masked/test_indexing.py#L9-L55)는 당대 직접 동작 근거다. 두 방식 모두 같은 literal 집합을 받는다.

1.5→1 truncation은 dtype을 유지해도 원판의 버그 예방 목적에 실패한다. bool/NA/overflow를 새로 채점 범위에 넣지 않는다. whole-valued float 2.0/3.0는 JSON 숫자 표현이 2/3으로 접힐 수 있어 value_literal과 value_type을 추가했다. 문자 그대로의 float/int 차이를 participant text와 실행 입력에 보존해야 한다.

[issue54660](https://github.com/pandas-dev/pandas/issues/54660)는 NaN 예외 논의를 보여준다. 이 후대 missing-value 입력을 원래 finite scalar 과제에 몰래 넣으면 두 schema의 지원 차이를 설명 추가 효과로 오인한다. stricter acceptance가 '공식 완성 consumer recipe 둘'이면 P06의 native wrapper는 해당 gate를 통과하지 못하므로 ready 분자에서 제외한다. 이번 선택은 문서·mechanism-level 조건부 준비도다.

## 출처와 기준의 독립성

P02는 외부 PEP 규격이 있으나 최초 제안이 그 규격을 이미 인용한다. P04/P06의 상세 tests는 card와 다른 파일이지만 같은 pandas maintainers가 썼다. 독립 human adjudication이나 외부 재현 결과가 아니다. 제안→카드→테스트가 같은 문서군에서 나온 만큼 wrong-card stress와 서로 다른 context 판독은 별도 근거로만 계산한다. 같은 model family의 두 판독을 사람 합의라 하지 않는다.

## 접근 실패·검색 범위·대체 경로

|시도한 주소/범위|관측|대체 경로|다음 확인|
|---|---|---|---|
|https://pandas.pydata.org/pdeps/|web open internal error|official GitHub web/pandas/pdeps directory + PDEP title PR search|필요시 공식 site를 다시 열고 목차와 git 이력 대조|
|https://pandas.pydata.org/pandas-docs/version/1.4/reference/api/pandas.to_datetime.html|404|v1.4.4 pinned official API docstring P-S06|정확한 historical HTML URL 확인; 의미 근거는 이미 고정 source에서 읽음|
|https://docs.google.com/document/d/1ZCQ9mx3LBMy-nhwRl33_jgcvWo9IWdEfxDNQ2thyTb0/edit|본문 접근 실패|2021-07 official mail + 2023 migration|P07를 다시 쓸 때 원 Google revision 복구; 못하면 first-public-unverified 유지|
|https://github.com/pandas-dev/pandas/pull/50402|GitHub 404|PR50424와 issue39584|첫파일의 링크 오탈자라는 점 보존|
|GitHub search issues PDEP 제목, 필터 없는 첫 query|422|is:pull-request/is:issue 추가 후 100개 한도 조회, PR53개 확인|20번호를 넘겨 후속 좋은 사례만 골라내지 않음|
|official GitHub contents endpoint for text|일부 응답 포맷 파싱 불가|github_fetch_file로 같은 ref/path 재요청|URL/source가 바뀐 것으로 세지 않음|

공식 NumPy can_cast HTML https://numpy.org/doc/1.23/reference/generated/numpy.can_cast.html 및 1.23.5 source는 선행 대안 탐색으로 읽었으나 scalar와 array 차이 때문에 P06 최종 구현근거로 삼지 않았다. Meson Commands.md의 generated include에는 jobs 문구가 보이지 않아 mcompile.py 실제 전달 코드를 열었다. integer/test_indexing.py에는 필요한 fractional assertion이 없어 masked/test_indexing.py로 이동했다. 2.1.0 whatsnew는 download/keyword만 확인해 최소수에서 제외했다. 현행 CPython3.10 HTML https://docs.python.org/3.10/library/datetime.html 은 현행3.10.22 표시여서 역사적 제공판으로 사용하지 않고 3.10.6 fixed source로 대체했다. 같은 content mirror/버전은 고유 원문 수를 늘리지 않는다.

## root 인계·재개 첫 행동

- 쓰기 파일: frame.csv, selection-seal.json, sources.jsonl, cases.json, packet-drafts.json, read-notes.md. git commit/push는 root만 수행한다.
- root는 실제 4과제20개 participant 파일과 rubric/12examples를 통합하고 B/C 실제 파일 URL·순서·판·문자수, private answer-link 경계를 다시 검사한다. draft JSON 검사만으로 이를 대체하지 않는다.
- pandas 실제 실행을 요구한다면 첫 행동은 P04/P06의 pinned-version 환경과 literal-type fixtures를 고정한 뒤 동일 계약을 검증하는 것이다. historical build POC는 별도 환경에서 dependency closure를 확정해야 하며 현재 @main을 그대로 실행하지 않는다. 구체 실행 명령/입력은 최종 HANDOFF의 재개 항목으로 남긴다.
- 모든 사람 trial/시간·품질 인과효과는 미실시다. 세 case design이 준비됐다는 판단과 실제 historical build/API 실행이 통과했다는 판단은 분리한다.

