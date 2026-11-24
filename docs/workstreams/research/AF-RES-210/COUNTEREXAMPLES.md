# 반례·정정 (AF-RES-210)

표기: (A행,B행)은 1-based; Breezy 공개 기대값은 원래 0-based인 경우 명시. 이 문서의 새 입력은 보강이며 고정 8쌍 분모에 넣지 않는다. 공개 시험의 expected와 실제 stdout은 다르다. 아래 구현 결과는 코드 추적 예측, 실행하지 않았다.

| ID | 입력/조건 | 반증하는 주장 | 원자료 / 근거 | 판정 |
|---|---|---|---|---|
| CE1 | 순열 2,3,1; 마지막 pile tops 1,3 | pile tops가 바로 원래 순서의 LIS | A01 pp413–415 Lemma1, A02 pp2–4; 1은 3 뒤에 나타남. 마지막 pile 3의 이전 pointer는 2 | 길이는 2, 실제 복원 2,3; 길이와 증인 구분 |
| C2 | A=[A,B], B=[B,A]; both unique | 같은 LIS 길이면 같은 앵커 | B02 L168–244; D02 unique_lcs_py; D03 L347–420 | Git A 순회 B rank 2→1: B를 유지; Breezy B 순회 A rank 2→1: A를 유지. 둘 다 길이 1. -U0 편집 후보 Git A1 삭제/B2 삽입, Breezy B1 삽입/A2 삭제. 최종 헤더는 각각 emit 구현에 따름 |
| C1 | A=[X,Y,X,Y], B=[Y,X,Y,X] | 유일 앵커가 없으면 동일 처리 | B02 L346–364, B03 L156–227; D02/D03 L448–535 | Git patience fallback; histogram 첫 B=Y에서 A2–4/B1–3 길이3 후보; Breezy no unique, 양끝 불일치로 전체 replace. Git classic tie 실제 미확인 |
| CE2 | C04 L84,132,218: aBccDe / abccde (문자열=문자 단위, 행으로 바꾸면 별도 실험) | 동일 이름 patience는 모든 중복 내부를 같은 방식으로 구제 | [C04](https://github.com/breezy-team/patiencediff/blob/v0.2.13/patiencediff/test_patiencediff.py#L76-L84) expected (0,0),(5,5); B02/B06 fallback | Breezy 실제 시험 기대상 c,c 미매치; Git 한 문자 한 행으로 정규화하면 가운데 공통 c,c에 Myers fallback 예측, stdout 미확인 |
| CE3 | C04 L355–387, A=a..p, B=abcdefxydefghijklmnop 각 문자 LF 행 | patiencediff.unified_diff 이름이면 patience | [C04](https://github.com/breezy-team/patiencediff/blob/v0.2.13/patiencediff/test_patiencediff.py#L355-L388), [D04](https://github.com/breezy-team/patiencediff/blob/v0.2.13/patiencediff/__init__.py#L72-L87) | 기본 difflib expected @@ -1,6 +1,11 @@; 명시 matcher expected @@ -4,6 +4,11 @@; 같은 입력·다른 정책, 다른 기대 hunk |
| CE4 | A,1,B→X,1,Y, -U0 vs --inter-hunk-context=1 | 같은 앵커면 같은 hunk 수 | [C05](https://github.com/git/git/blob/v2.43.0/t/t4032-diff-inter-hunk-context.sh#L51-L80) | 공개 기대 2개 @@ -1 +1 @@/@@ -3 +3 @@ vs 1개 @@ -1,3 +1,3 @@ |
| CE5 | spaces.txt / functions.c, indent on/off | 원리 하나가 brace/blank 위치를 결정 | [C06](https://github.com/git/git/blob/v2.43.0/t/t4061-diff-indent.sh#L91-L197), B04 L1054–1088 | spaces compacted expect @@ -2,6 +2,9 @@ (patience/histogram/default 동일); no-indent @@ -3,5 +3,8 @@. functions compacted @@ -1,5 +1,10 @@ vs @@ -1,6 +1,11 @@. 기대값만 |
| CE6 | A=[A,B,C], B=[B,C,A], --anchored=A | explicit anchor도 무조건 최대 길이 LIS | B01 anchored; B02 L168–244의 anchor_i lock | plain B ranks 3,1,2에서 길이2(B,C); A가 첫 prefix anchor면 lock으로 길이1 A를 유지하는 코드 후보. 실행 필요 |
| CE7 | A=[A,x,x,x], B=[x,x,x,A] | patience가 전체 최소 편집 수를 보장 | A01 Lemma1, B02 unique filter, B08 commit, B04 classic | A만 유일 → 1 match, 6 indel; 전체 LCS x,x,x 유지하면 2 indel(최소, A 이동). 모델 예측; stdout/선호 미측정 |
| R3 | 모든 행이 다름 | LIS 길이0이면 무조건 Myers fallback | B02 L346–354, C03 L200–225 | 공통 없음은 직접 all-changed. C1과 구분; 공개 hunk 동일 |
| R2 | frobnitz fixture | 서로 다른 알고리즘이면 hunk가 반드시 다름 | [C03](https://github.com/git/git/blob/v2.43.0/t/lib-diff-alternative.sh#L64-L111), C01/C02 | 두 전략에 동일 expect/diffstat, 10 삽입 11 삭제. 실제 통과/사람 선호와 무관 |

## 정정 기록
- 첫 M 행의 R4 "first explicit nonempty line-list"는 문자 단위/빈 배열을 제외한 후의 첫 행 목록이다. C04 L36–57의 Unicode/문자열 입력이 그보다 앞선다. 입력 범위를 행 텍스트에 맞춰 좁힌 판단은 원문 노출 후 명료화됐으므로 엄밀한 사전 표집으로 표현하지 않는다.
- M 단계 R2의 함수 경계 보존 가능성 및 R3의 전체 교체는 이미 공개 기대값을 열람한 상태였다. 첫 M 파일 커밋 5bbe48770fbff0de4c4bb5862e4094eb9f1e3be5의 원값을 유지하고 P/I/E 행을 뒤에 추가했다. 이전 값은 정답률에 산입하지 않는다. C2의 M은 이미 비교차 조건을 예상했으므로 P의 길이 1은 증명·명료화이지 새 관측 성공으로 가산하지 않는다.
- A01 1999 원문과 A02 1993 기술보고는 저자·계보 동일, 별도 기록이지만 독립 입증으로 세지 않는다. A03 Fredman은 다른 저술의 본문 facsimile만 1회 산입. C05,C06은 시험파일 유형 보강, 사전 표본/지정 파일 하한을 채운 것으로 숨기지 않는다.
- C1 Git fallback을 전체 교체로 간주하지 않는다. R3에서는 공통 자체 없음, C1에서는 반복 공통 존재. R4의 histogram C(5,4) 후보는 compaction 전 예측; 최종 hunk로 확정하지 않는다.

## 경쟁 설명
1. "readability" 이득은 LIS가 아니라 희소 행 선택·출력 경계 조정의 산물일 수 있다. CE4/5는 LIS 없이도 표시 위치 변화. 같은 입력에 -U와 indent만 조절해 사람 과제/오류율을 비교해야 한다. 이 설명이 지지되면 첫 링크를 B01 context/indent 절 또는 B07로 바꾸고 카드 원전을 부가 자료로 내린다.
2. "최소 편집"과 "함수 보존"은 비용 함수가 다르다(CE7). 사용자의 과제가 저장량/전송량이면 minimal 및 edit graph를 먼저, 읽는 과제라면 R2와 C06의 기대 위치를 먼저. 사람 선호 측정 없음.
3. "merge 품질"은 base/ours/theirs와 충돌·오병합의 결과로만 평가. B10의 설명은 설계 근거이지 R2 diff의 성공으로 merge를 추론할 수 없다. 충돌 감소/잘못된 자동 병합이 관측되면 merge 전략 링크 순서를 재판정한다.
