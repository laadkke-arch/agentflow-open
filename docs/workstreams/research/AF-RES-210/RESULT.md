# AF-RES-210 — 카드 정렬 원전이 줄 diff 선택에 추가하는 판별력

| 입력쌍·출처 | 업무 목표 | 가까운 문서 예측 | 원리 추가 예측 | 기대 diff 위치 | 미확인 |
|---|---|---|---|---|---|
| R1 [C01 L9–19](https://github.com/git/git/blob/v2.43.0/t/t4033-diff-patience.sh#L9-L19) 3/3행 | 공백 무시와 실제 문자 수정 구분 | a,c 공통, b→bX | A01 Lemma1: 유일 pair (1,1),(3,3), LIS2; B02/B05 비교 등호 별도 | 공개 grep plus-X만. 소스 예측 -U0 @@ -2 +2 @@ | 전체 기대/실행 없음 |
| R2 [C03 L6–60,64–111](https://github.com/git/git/blob/v2.43.0/t/lib-diff-alternative.sh#L6-L111) 26/25행 | 함수 경계·코드 이동을 읽는 diff | patience/histogram 시도 가능, 앵커 불확정 | A01 Lemma1: B rank 1,12,13,15,16,18,9,22 → LIS7, return 1; (20,9) 제외. B02 L168–303 및 D02: 같은 root LIS | 공통 공개 expect @@ -1,26 +1,25 @@, +10/-11: B3–11 삽입, A9 및 A14–22 삭제, A25→B24. C01,C02 두 정책 | 정답 선노출; Myers 및 각 내부 추적/실행 없음 |
| R3 [C03 L180–225](https://github.com/git/git/blob/v2.43.0/t/lib-diff-alternative.sh#L180-L225) 6/6행 | 공통 없는 교체 | 전체 교체 | A01 LIS0; B02 L346–354 직접 all changed, fallback 아님 | 공개 공통 expect @@ -1,6 +1,6 @@ | 실행 미확인, 원전 추가 없음 |
| R4 [C04 L66–67](https://github.com/breezy-team/patiencediff/blob/v0.2.13/patiencediff/test_patiencediff.py#L59-L74) 5/5요소 | 중복 구분자 속 지역 일치 | b만 유일; a/c 선택 미정 | A01 LIS1: (3,3); D02/D03 head/tail, B02 gap/fallback 예측 (1,1),(3,3),(5,5) | 공개 0-based matches (0,0),(2,2),(4,4); unified hunk 없음 | Git LF 정규화 비교·histogram C(5,4) 후보·최종 출력 미실행 |
| C1 pairs.csv (합성) 4/4행 | 유일 행 없이 반복 이동 | 희소행 옵션 가능, patience 미정 | A01 LIS0, fallback 결정 못 함; B02→classic; D02→no match; B03→3행 후보 | 공개 없음. Breezy whole replace; Git 3 common lines 가능, histogram (2:1,3:2,4:3) 예측 | Git Myers tie, 출력 미실행 |
| C2 pairs.csv (합성) 2/2행 | 교차하는 유일 앵커 | 모두 unique, 두 행 동시 보존 불가 | A01/A02 LIS1 두 해. B02 A scan→B(2,1); D02/D03 B scan→A(1,2) | 공개 없음. Git A1 삭제, B2 삽입; Breezy B1 삽입, A2 삭제 후보 | 실제 hunk, Myers tie 미실행 |
| C3 pairs.csv (합성) 4/3행 | 한쪽만 중복인 줄 | A,C 후보, B 불확정 | A01 LIS2 on both-unique candidates; B02/D02 A,C 보존, B root 제외; B03 A frequency only | 공개 없음. B1 삽입, A2–3 삭제 후보 | histogram 최종 출력, 방향 반전 효과 미실행 |
| C4 pairs.csv (합성) 4/4행 | 순서 보존 단일 교체 | A,B,C 유지, old→new | A01 LIS3 단일해; B02/D02 동의 | 공개 없음. Git -U0 @@ -2 +2 @@ 후보 | 실행 미확인; 원전으로 새 선택 없음 |

| 구현·판 | 유일 기준·정렬 | 동률·fallback | 원소스 주소 | 어긋나는 입력 |
|---|---|---|---|---|
| Git patience v2.43.0 | 구간 양쪽 count=1; shared class ID; A 순회 B ranks LIS; 재귀에서 새 빈도 | 최소 tail 교체, predecessor 복원, explicit prefix anchor lock; 공통 없음 직접 changed; 공통 있으나 unique 없음 classic Myers | [B02 L87–244,246–372](https://github.com/git/git/blob/v2.43.0/xdiff/xpatience.c), [B05 L109–145,280–287](https://github.com/git/git/blob/v2.43.0/xdiff/xprepare.c), [B06 L405–434](https://github.com/git/git/blob/v2.43.0/xdiff/xutils.c) | C2 vs Breezy; C1 vs Breezy; CE6 anchored |
| Git histogram v2.43.0 | A-side frequency, B 순회, 연속 공통 영역 확장; 길이 또는 희소도 개선 | strict replacement condition; 처음 같은 length/count 유지; threshold 64, 적격 영역 없으나 공통이면 classic; scanA 오류와 fallback 구별 | [B03 L103–227,284–358](https://github.com/git/git/blob/v2.43.0/xdiff/xhistogram.c), [B09 port](https://github.com/git/git/commit/8c912eea94a2138e8bc608f7c390eb0b313effb0) | C1 repeated candidates, R4 B-side duplicate 가능; R2 same expect |
| Git Myers/default vs minimal v2.43.0 | 전체 편집 그래프·일치 snake, 유일성 전제 없음, pre-optimize | classic split; need_min flag 및 heuristic; exact equal-path tie 미추적 | [B04 L256–367](https://github.com/git/git/blob/v2.43.0/xdiff/xdiffi.c), [B01 diff-algorithm](https://git-scm.com/docs/git-diff/2.43.0) | CE7 전체 edit 최소와 unique-LIS 목표 다름 |
| Breezy Python v0.2.13 | 양쪽 구간 유일, B 순회 A ranks; hashable element | bisect tail, backpointer; recurse gaps; no unique면 prefix 또는 suffix만; recursion 제한 | [D02 unique_lcs_py/recurse_matches_py](https://github.com/breezy-team/patiencediff/blob/v0.2.13/patiencediff/_patiencediff_py.py), [C04 L76–84](https://github.com/breezy-team/patiencediff/blob/v0.2.13/patiencediff/test_patiencediff.py#L76-L84) | C2, C1, CE2 |
| Breezy C v0.2.13 | hash/equality class와 bounds, B 순회 A rank piles | backpointers; head/tail only no unique; maxrecursion stop; Python에서 유래 | [D03 L134–250,255–420,448–535](https://github.com/breezy-team/patiencediff/blob/v0.2.13/patiencediff/_patiencediff_c.c) | C2/C1; 동일 계보이며 독립 입증 아님 |
| Breezy unified_diff v0.2.13 | 기본 difflib.SequenceMatcher; 명시 matcher로 patience | grouped opcodes n=3; C import 우선·Python fallback | [D04 L25,31–98,129–142](https://github.com/breezy-team/patiencediff/blob/v0.2.13/patiencediff/__init__.py), [D05 L8–12](https://github.com/breezy-team/patiencediff/blob/v0.2.13/setup.py) | CE3 기본/명시 matcher 다른 공개 hunk |

| 목적 | 첫 원문 | 추가 원리가 가른 항목 | 같은 답을 낸 대안 | 관측 수준 |
|---|---|---|---|---|
| 설명: 왜 순서 보존 앵커인가 | [A01 pp413–415 Lemma1](https://www.stat.berkeley.edu/~aldous/Papers/me86.pdf) + [B02 L168–244](https://github.com/git/git/blob/v2.43.0/xdiff/xpatience.c#L168-L244) | 길이 최적/복원 차이, R2 제외 anchor 및 C2 2해를 유도; 구현 tie는 못 결정 | A02 pp2–4, A03 §2도 minimum-tail 불변조건 설명 | 수학적 규칙/연역; 독립 예측 효과 0건 입증 |
| Git 옵션 선택: 함수 이동 패치 읽기 | [B01 --diff-algorithm](https://git-scm.com/docs/git-diff/2.43.0) + [C03 L64–111](https://github.com/git/git/blob/v2.43.0/t/lib-diff-alternative.sh#L64-L111) | R2 원전이 root chain 길이를 설명하지만 이 옵션 사용에 필수 아님 | patience/histogram 같은 공개 expect, R3/C4 근접 설명으로 충분 | 규칙·공개 기대, 사용자 선호 미측정 |
| Git 옵션 선택: 표시 경계 | [C06 L91–197](https://github.com/git/git/blob/v2.43.0/t/t4061-diff-indent.sh#L91-L197), [C05 L51–80](https://github.com/git/git/blob/v2.43.0/t/t4032-diff-inter-hunk-context.sh#L51-L80) | LIS는 compaction/context를 가르지 않음 | indent/context만 조정해도 다른 hunk; spaces 3정책 같은 expect | 공개 기대 |
| 구현 재사용/포팅 | [B02 L87–372](https://github.com/git/git/blob/v2.43.0/xdiff/xpatience.c) 또는 [D02](https://github.com/breezy-team/patiencediff/blob/v0.2.13/patiencediff/_patiencediff_py.py), [D04 L72–87](https://github.com/breezy-team/patiencediff/blob/v0.2.13/patiencediff/__init__.py#L72-L87) | LIS 핵심은 이전 가능하나 equality, 지역성, tie, fallback, emission 불변 아님 | C04 공개 테스트·CE3; 같은 이름으로는 불충분 | 고정 소스/기대, 미실행 |
| 두 판 병합: 충돌/오병합 | [B10 L100–112](https://github.com/git/git/blob/v2.43.0/Documentation/merge-strategies.txt#L100-L112) | 카드 원리로 3-way 충돌 결정 불가 | ort histogram 기본/recursive diff.algorithm; 실제 3-way 필요 | 문서 규칙만 |

## Q1 — 목적을 섞지 않는다
[B08 도입 메시지](https://github.com/git/git/commit/92b7de93fb7801570ddc3195f03f30b9c201a3bd)는 +/- 줄 수를 먼저 최소화하기보다 고유 줄 보존을 우선하려는 당사자 의도를 말한다. [B11 Cohen 설명](https://bramcohen.livejournal.com/73318.html)은 코드 함수가 다른 위치로 가고 반복 brace가 혼선을 주는 예를 설명한다. [B01](https://git-scm.com/docs/git-diff/2.43.0)에서 default Myers, minimal의 추가 비용, patience와 histogram, --anchored, 표시 문맥은 별도 조작이다. B08은 선호 측정이 아니며 B11은 2010 설명이라 카드 놀이가 Git 채택의 역사적 원인이었다는 증거가 아니다. [E01](https://stackoverflow.com/questions/32365271/whats-the-difference-between-git-diff-patience-and-git-diff-histogram)과 [E02](https://stackoverflow.com/questions/19949526/examples-of-different-results-produced-by-the-standard-myers-minimal-patienc)는 차이를 보여줄 예를 요구한 독자 본문이다. 독자 원입력/사용자 성과 없음. [B10](https://github.com/git/git/blob/v2.43.0/Documentation/merge-strategies.txt#L100-L112) 3-way 전략은 결과가 충돌/병합이므로 2-way patch hunk와 별도. 개발자는 읽는 위치, 구현자는 비용·일치 규칙, 수학자는 순서 증인, 병합 사용자는 실제 병합 결과를 평가한다.

## Q2 — 수학 원전이 더하는 것과 하지 못하는 것
[A01 pp413–415 §1.1 Lemma 1](https://www.stat.berkeley.edu/~aldous/Papers/me86.pdf), [A02 pp2–4](https://www.stat.berkeley.edu/~aldous/Research/OP/patience.pdf)에서 순열의 값 x를 왼쪽부터 처리하고 top>x인 가장 왼쪽 pile에 놓거나 새 pile을 만든다. 길이 k의 증가 부분수열 중 최소 끝값 T(k)를 유지하는 불변조건으로 각 pile index가 길이 k의 증인을 가지며, 어떤 더 긴 증가 부분수열도 pile 수보다 길 수 없다. 새 카드의 이전 pile top을 pointer로 남기고 마지막 pile top에서 거꾸로 따라가야 원래 순서의 증가 수열을 복원한다. 최종 top 목록 그 자체는 시간순이 아닐 수 있다([2,3,1]→[1,3]). [A03 §2](https://par.cse.nsysu.edu.tw/resource/paper/2014/140127/On%20computing%20the%20length%20of%20longest%20increasing%20subsequences.pdf)는 minimum-tail 및 길이의 비교 복잡도 근거다. 전체 diff 복잡도와 다르다.
[2,1,3]은 길이2의 [2,3]과 [1,3]이 존재한다. C2의 [2,1]은 길이1 두 해. 수학적 결과는 cardinality를 좁혀도 어느 구현이 어느 해를 선택하는지 정하지 않는다. A01의 Ulam distance n−L(카드 한 장 이동의 metric)와 diff의 insert/delete cost는 같지 않다. CE7에서 유일 A 1개 보존과 전체 LCS x 3개 보존이 충돌한다. 동률·문자열 동일성·중복·지역 빈도·hunk는 카드 문제의 입력에 없다.

## Q3 — Git의 실제 구간 연산
B05 L109–145에서 hash와 실제 record 비교로 shared class를 부여하고, B06 L173–220에서 whitespace 옵션이 일치 조건을 바꾼다. B02 L87–161에서 A 구간 순으로 표를 만들고 B 구간에서 일치 위치를 연결, 어느 쪽 중복이라도 nonunique 처리한다. L168–244는 A 순회에서 B rank 최소 tail을 이진 검색하고 predecessor로 chain을 복원한다. --anchored의 prefix lock은 보통의 unconstrained LIS보다 별도 조건이 강하다(CE6). L246–303에서 anchor 앞쪽 일치 줄을 확장하고 left prefix를 소비, 나머지 gap을 재귀 처리하므로 global unique만으로 끝나지 않는다. L330–364에서 한쪽 빈 구간, 양쪽 공통 자체 없음, 공통 있으나 유일 없음의 세 경우를 구별한다. 마지막은 alg mask 제거 후 classic을 부분 파일에서 다시 실행(B06 L405–434). R4의 b root 하나만으로도 a,c가 복구되며 C1과 R3는 같은 LIS0이어도 처리 분기 다름.

## Q4 — 같은 이름, 다른 연산 및 계보
Git xhistogram(B03)은 A에 대한 occurrence 및 B 순회에서 연속 블록을 늘려 희소도·길이 개선을 선택한다. 한쪽만 중복인 경우도 허용 가능하고 hash-chain cap 64, 공통은 있으나 유효 후보가 없으면 classic; 오류 분기와 혼동 금지. B09는 JGit port를 명시하며 별개 원리/성능 검증으로 취급하지 않는다. Git classic(B04)은 unique filter가 아니라 편집 그래프와 need_min/heuristics를 사용한다. Breezy D02/D03는 B 순회 A rank, 구간 양쪽 유일, no-unique에서 같은 prefix/suffix만 복원; Git의 Myers fallback과 다르다. D03 C는 Python에 기반한 같은 계보이며 eq 부분 Mercurial bdiff 유래. D01의 Bazaar 추출 및 Cohen 설명 연결, B08 Git 도입은 별도 구현 출전이다. 카드 논문을 직접 인용해 채택했다는 역사적 자료는 확보 못 했다. D04에서는 패키지의 unified_diff를 matcher 미지정으로 부르면 기본 difflib이므로 CE3의 다른 hunk가 설명된다.

## Q5 — 증가분 판정 및 노출
기준판 매뉴얼을 먼저 열었으나 Git fixture와 expect가 같은 helper에 있어 R1–R3 기대를 먼저 보았다. R4 test와 소스도 같은 열람 묶음에 노출됐다. M-reconstructed를 먼저 커밋(5bbe48770fbff0de4c4bb5862e4094eb9f1e3be5), 원전과 소스를 열어 P/I/E를 보강했다. 원전 독립 노출 및 구현 후 수정 시점 분리는 실패했다. C1–4는 공개 정답 없는 합성 통제다. 8쌍×4단계=32행에서 원리의 독립적인 정확도 향상은 **입증 0건, 효과 자체는 미확인**. 오답률/정답률 계산 안 함. R2에서 원리만으로 가능한 순서의 길이와 제외 후보를 계산, C2에서 가능한 해를 두 개로 좁힌 것은 설명상 추가 정보다. 그러나 실제 앵커 동률 해결은 B02/D02, fallback 및 최종 hunk는 B04/B07/D04까지 요구한다. R1/R3/C4는 가까운 문서/입력만으로 같은 결과가 가능; C2 비동시 보존도 M 단계에서 이미 예측. 따라서 추가 원문을 모든 결과에 기계적으로 붙일 근거 없음.

## Q6 — 관측 수준과 반례
pairs.csv에 실제 4+통제4, root candidates, 정확한 줄 목록, 공개 expect 또는 결측을 넣었다. R1 grep만, R2/R3 full hunk expected, R4 match pairs only. C04 CE3는 동일 입력에서 기본 difflib vs 명시 patience 기대 헤더가 다르고, CE2는 nonunique middle 미매치 기대를 명시한다. C05 context로 동일 anchors의 hunk count가 달라짐; C06 compaction으로 알고리즘을 바꾸지 않고도 위치 변화, 3 알고리즘 같은 expect도 확인. 모두 기대/규칙이지 새로운 stdout 아니다. C2는 Git/Breezy의 동률 방향이 달라질 예측, C1은 fallback 정책 반례. R2와 C06에서 같은 hunk를 낸 서로 다른 정책의 공개 기대를 확인했다. Git 최종 hunk는 B04 L1054–1088의 compaction과 B07 L168–255의 context emission을 지나야 한다. 모든 세부 trace 및 실제 양쪽 구현 실행은 HANDOFF 검증 대상으로 둔다.

## Q7 — 제품 링크 선택과 비용
- 설명 카드: 원리를 요청할 때 A01의 Lemma1을 먼저, 매핑을 원할 때 B02/D02의 rank/pointer 구간을 함께 제시. 수학 원전은 읽을 비용이 더 크지만 원래 순서 보존 및 length/witness를 구분한다. 알고리즘 선택 하나만 물으면 B01 한 절로 충분한 사례부터 보여준다.
- 패치 검토: 목적이 이동한 함수 읽기라면 R2 expected와 실제 diff 옵션 문서, 필요시 C06 indent/함수 문맥을 먼저. exact output이 필요하면 동일 입력, version, options, stdout을 확보. 원전보다 구현 및 시험 링크가 먼저다.
- 재사용: 같은 명칭이 아니라 equality, uniqueness scope, scan direction, fallback, emit을 계약으로 묻는다. B02/D02/D04를 대조하고 코드를 재사용하기 전 API 기본 matcher/빌드 경로까지 확인. 서로 다른 선택은 비용·실패가 다르므로 무조건 patience 권장하지 않는다.
- 병합: 최소 edit, 읽기, 충돌 감소를 별도로 요청받고 B10과 3-way 테스트를 연결한다. 충돌/오병합 및 사람 성과의 검증이 없다면 우위 판단을 미확인으로 남긴다.

## 표집 및 품질
frame.csv는 Git 두 호출 스크립트와 공통 helper를 펼쳐 15 valid pair-related static diff calls(3 unique,12 repeats), Breezy nonempty explicit line-list/file 영역 12 static calls(5 unique,7 repeats), 합계 27 calls/8 unique, 앞 4 selected/4 capped/19 repeats. Git invalid source 2 및 apply 2, Breezy scalar/tuple/empty/error/inherited test 그룹을 별도 제외. 이 분모는 모든 SequenceMatcher 입력 호출 총수가 아니다. 행 텍스트 eligibility를 노출 후 좁힌 약점이 있으며, Unicode scalar까지 포함하는 모집이라면 R4 교체 필요. 통제 4 별도. sources.jsonl 산입 27 unique works/files A3 B11 C6 D5 E2; C05,C06 사후 시험 보강 제외 시 core C4/6, 총25. A01/A02 같은 author lineage, A03 facsimile 한 번; C04를 D에 중복 안 셈. 자료 수≠독립 실험 수. 독립 검토·실행 미수행. AF-RES-199 중앙 DONE과 실제 HANDOFF PARTIAL 차이를 유지. 210 PARTIAL.
 
| 불일치·약점 | 영향을 받는 결론 | 다음에 열 원자료·조사 | 판정을 바꿀 관측 |
|---|---|---|---|
| 기대값·소스 선노출 및 원리 단계 재구성, line-list eligibility 사후 명료화 | 원전의 실제 추가 판별 정확도·표집 대표성 | C01–C04에서 입력만 추출하여 별도 blind 세션, 예상 결과 차단; Unicode/문자 단위 범위 사전 확정 | 독립 M→P→I에서 원전이 추가로 맞힌 anchor/hunk 수와 틀린 사례; 0이면 설명 링크로 제한 |
| 두 구현 동일 입력 실제 stdout/anchor trace 없음; C02/C03 공통 기대만, 지정 파일 C4/6 | 동률/희소·fallback 예측의 실제 결과 및 종류별 기준 | v2.43.0 Git test harness, Breezy v0.2.13 C/Python unittest, pairs.csv 고정 입력; 실제 별도 fixture/expected 파일 탐색 | C1/C2/C3/R4의 정확한 hunk 및 내부 trace가 예측과 반대면 매핑/추천 수정; fixture 출전 2개 추가 또는 하한 명시 |
| 독자 원요구는 있지만 선호·병합 성과·역사적 인과 측정 없음 | 코드 이동을 더 읽기 쉽게 한다는 효용 및 링크 우선순위 | B08 당시 메일 원문, B10 3-way 사례, 사용자 비교 실험(과제 성공/시간/오류) | indent/context가 효과 대부분을 설명하면 C05/C06/B01 우선, unique-LIS가 별도 효과를 보이면 A01 부가 링크 강화 |
