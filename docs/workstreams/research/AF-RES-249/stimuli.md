# 두 과제의 자극·정답 키 v1 — 참가자용과 판정자용 분리

실행 전 CPython 3.12.0(고정 테스트 태그와 같음), UTF-8 환경. 공식 문서는 실제 열람 시 3.12.16 표시였으므로 자극 스냅샷 및 URL 해시를 배정 이전에 고정; patch 간 의미 동일 여부는 실행 담당 확인. 모든 예시는 수작업 정답. 연구자용 아래 후보/반전·정답은 baseline 전 참가자에게 제공 금지. 참가자에게는 중립 요구문·공개 예시만 보인다.

## A: 이벤트 로그 연속 구간 변환
참가자 문구: 함수 runs(events) 작성. events는 (문자열 key, 정수 payload) 쌍의 리스트. 입력 순서대로 연속해서 같은 key가 나타나는 최대 구간 하나씩 (key, 해당 payload 리스트)로 만들어 리스트 반환. 떨어진 같은 key는 새 구간. 빈 입력은 빈 리스트. 입력을 수정하지 않는다. 구현 방법 자유. 공개 예시 [('x',1),('x',2),('y',3)] → [('x',[1,2]),('y',[3])].
카드 A1: [Python itertools.groupby](https://docs.python.org/3.12/library/itertools.html#itertools.groupby), 연속 키 변경 시 새 그룹, 그룹 iterator는 원본과 공유되므로 즉시 materialize. 원문 정렬 예시를 그대로 복사하면 틀림.
카드 A2: [Python collections.Counter](https://docs.python.org/3.12/library/collections.html#collections.Counter), 키별 전체 등장 횟수. 같은 '묶기/집계' 역할이나 떨어진 같은 키 합침, payload 손실. 이것을 단독 직접 대체 후보로 쓰면 부적합; 보조 용도는 허용.
두 카드 동일 스타일(중립 제목+URL, 효과 주장하지 않음). 무작위 순서. 후보명을 participant 화면에 처음 노출한 시각과 페이지 구간 열람 시각 분리.

| 판정 벡터 | 입력 events | 손 계산 기대값 | 실패 탐지 |
|---|---|---|---|
| A0 | [] | [] | 빈 초기화 |
| A1 | [('a',1)] | [('a',[1])] | 마지막 flush |
| A2 | [('a',1),('a',2),('b',3),('a',4)] | [('a',[1,2]),('b',[3]),('a',[4])] | 전역 집계/정렬/비연속 병합 |
| A3 | [('a',2),('a',2),('a',0)] | [('a',[2,2,0])] | payload 중복/0 유지 |
| A4 | [('',0),('b',-1),('',2)] | [('',[0]),('b',[-1]),('',[2])] | falsy 키, 순서 |
| A5 | [('z',1),('a',2),('z',3),('a',4)] | [('z',[1]),('a',[2]),('z',[3]),('a',[4])] | 교대 키/정렬 |
| A6 | [('x',1),('x',2),('y',3)] | [('x',[1,2]),('y',[3])] | 공개 예시 |

허용 방식(예시, 미실행):
```python
def runs(events):
    out = []
    for k, v in events:
        if not out or out[-1][0] != k:
            out.append((k, [v]))
        else:
            out[-1][1].append(v)
    return out
```
```python
from itertools import groupby
def runs(events):
    return [(k, [v for _, v in g]) for k, g in groupby(events, key=lambda r: r[0])]
```
비적합 대안: sorted(events) 이후 groupby(실패 A2/A5); dict/Counter 키별 누적(실패 A2); group iterator만 보관 후 나중 소비(실패 A2); 이름만 바꾸는 wrapper는 방법 교체 아님. 출력 type tuple/list와 순서/내용, input unchanged 모두 비교. 특정 표준 API 호출은 별도 메타데이터, 통과 조건 아님.

## B: 정렬된 표의 동률 뒤 삽입 위치
참가자 문구: insertion_index(rows, x) 함수 작성. rows는 (정수 key, 문자열 tag) 쌍, key 비감소 순으로 정렬된 리스트; x는 새 행의 정수 key. rows를 바꾸지 말고 새 행을 삽입할 0부터 len(rows) 사이의 정수 위치를 반환. 같은 key 기존 행이 있으면 그 전부의 **뒤**, 기존 순서와 상대 위치 보존. 빈 입력 0. 공개 예시 [(1,'a'),(4,'b')], x=3 → 1. 입력 정렬은 전제, 정렬/복사할 필요 없음; 정렬되지 않은 입력·NaN·혼합 type은 적용 대상 밖. 성능 제한 없음(작은 테이블).
카드 B1: [bisect_right](https://docs.python.org/3.12/library/bisect.html#bisect.bisect_right), 기존 동률 뒤.
카드 B2: [bisect_left](https://docs.python.org/3.12/library/bisect.html#bisect.bisect_left), 동률 앞. 같은 역할이지만 현재 요구와 반대. 양쪽 anchor가 같은 문서라 우연히 다른 API도 볼 수 있음: 실제 section/visible text 기록; 후보별 독립 노출 가정 금지.

| 판정 벡터 | rows의 key 배열(각 tag는 고유) | x | 뒤(주 정답) | 앞(반전 비교, 채점 아님) |
|---|---|---:|---:|---:|
| B0 | [] | 2 | 0 | 0 |
| B1 | [1,4] | 3 | 1 | 1 |
| B2 | [1,2,2,4] | 2 | 3 | 1 |
| B3 | [2,2,2] | 2 | 3 | 0 |
| B4 | [2] | 1 | 0 | 0 |
| B5 | [2] | 3 | 1 | 1 |
| B6 | [1,1,4,4] | 4 | 4 | 2 |
| B7 | [-3,0,0,5] | 0 | 3 | 1 |

반전 문항(사후 이해 질문): 앞 요구로 바뀐다면 B2/B3/B6/B7의 위치는 각각 1/0/2/1. 이는 참가자 제출 사양을 바꾸거나 품질 정답에 추가하지 않는다.
허용 예:
```python
def insertion_index(rows, x):
    return sum(1 for k, _ in rows if k <= x)
```
```python
from bisect import bisect_right
def insertion_index(rows, x):
    return bisect_right(rows, x, key=lambda r: r[0])
```
수작업 upper-bound 이진 탐색도 허용. bisect_left와 index()로 최초 동률을 반환하면 B2/B3 실패. 정렬된 key 배열로 projection 후 right는 허용. x 자체에 key를 적용한다는 오해로 타입 예외가 발생하면 실패. boolean은 int subclass여도 type(result) is int 조건으로 거절. 동률 없는 B1만 성공은 부적합.

## 공통 채점/실행 인계
각 checkpoint hash를 고정하고 rubric version v1 + inputs(verify_vectors.py) hash + interpreter version + stdout/stderr + exit status + 테스트별 got/expected + 원본 불변 여부 + time + reviewer actor + verdict를 영수증으로 저장. 두 과제 모든 해당 벡터 통과, 원본 불변, 예외 없음, 요구 일치, 타인 개입 없는 해당 actor 제출을 별도 확인. 전부 맞아도 일반적 정확성을 보장하지 않음; 명세 외 판단은 보류. 합성 사건의 평가는 손 계산. 향후 실행 담당:
```sh
git checkout work/research-af-res-249
cd docs/workstreams/research/AF-RES-249
python3.12 -VV
sha256sum verify_vectors.py /absolute/path/to/submission.py
python3.12 verify_vectors.py A /absolute/path/to/submission.py
python3.12 verify_vectors.py B /absolute/path/to/submission.py
```
각 참가자의 해당 과제별로 실행; 위 두 명령은 각각 해당 함수를 가진 제출에만 적용. 신뢰되지 않는 제출 실행은 오프라인 제한된 격리 runner에서만, timeout/메모리 제한 포함. 실패 시 반례 벡터와 반환값·원예외 저장; stdout 비밀 없음 확인. API 이름을 알리는 답안/hidden 벡터는 참가자에게 비공개. 스크립트 미실행·환경 미확인.
