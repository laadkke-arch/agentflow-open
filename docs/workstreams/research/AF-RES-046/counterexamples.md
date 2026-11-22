# AF-RES-046 · 경쟁 설명과 분야 밖 대조

## R02 보완의 적용 범위

아래 stream 상세 대조는 묶음3 시점 기록을 바탕으로 한다. 이후12선정슬롯과자연탈락25272의최초opened head/base/body를공식공개미러+GitHub정확diff로복원했다. 당시미확인표시는이력으로남기며현재판정은initial-public-heads.csv와REVISIONS.md R02를우선한다. 모든중간push나후속증거PR의openinghead를이복원과동일시하지않는다. rawgzip403·원eventID미보존·raw독립대조0/12한계는유지한다.

## 첫 예상과 실제로 깨진 조건

첫 예상은 선례 URL을 받은 작성자가 뒤에 같은 목적의 코드를 바꾸면 채택 사슬이 보일 수 있다는 것이었다. 이 기록에서는 (1) 무링크 실패 지적만으로도 코드가 바뀌고, (2) 링크 뒤 같은 작성자의 변화가 있어도 같은 재설계가 링크 전에 이미 공개되며, (3) 실제 수정자가 링크를 받는 사람이 아닌 경우가 있다. 원문 위치·SHA·시험 입력은 아래 상세 원장과 `changes.csv`에 남긴다.

- **링크와 변경의 시간적 동반:** L-P2, L-S2에서 같은 작성자의 실제 후속 변경 확인. 원인을 특정하는 첫 링크 연결 발언과 사람 시간은 미확인.
- **선행 착수:** L-P2는 같은 작성자, L-P1은 다른 작성자의 대안 구현이 첫 링크보다 앞섰다. 두 종류를 합쳐 같은 작성자의 선행 수정으로 코딩하지 않는다.
- **무링크 비교:** N-P1은 실패 리뷰 뒤 실제 runtime 변경, N-S3은 타인 시험 등록 수정, N-P3/N-S4는 문구만 수정. 같은 품질·난이도의 시간 대조가 아니므로 절감 효과를 계산하지 않는다.
- **유지·축소·후기 회귀:** L-S2에서 뒤의 두 번째 링크에 따른 ndarray 유지와 새 URL 없는 설명에 따른 반환형 복원이 확인된다. 이를 첫 링크의 성공으로 바꿔 넣지 않는다. 병합 뒤 read-only 회귀는 후기이며 처음 완료 품질의 한계를 보여준다.
- **분야 대조:** OSM은 실제 필드 변경이 링크보다26초 앞섰다. MusicBrainz는 공개 포럼의 취소·대체 보고와 뒤늦은 규범 링크를 읽었지만 개별 편집 원장이403으로 막혀 실제 적용을 미확인으로 남겼다. 두 사건은12 PR 분모 밖이다.

엄격 사슬0은 효과0이라는 뜻이 아니다. 현재 공개 기록에서 첫 링크→작성자 연결 발언→동일인·동일목적 patch→해당 시험/반영의 고리를 모두 확인하지 못했다는 뜻이다. 직접 작업시간·자기보고·프로그램 시간·경과시간의 단위는 `labor.csv`와 아래 비용 시간선에서 분리한다.


## pandas 상세 대조

## pandas: 반례와 적용 한계

이 파일은 6개 고정 슬롯의 해석이다. 참고 PR51784,51166,52043,52053,52089는 선택 사건의 원대상/후속 자료이며 새 표본 사례가 아니다. MusicBrainz/OSM 분모 밖 대조는 root 통합 조사에서 별도로 작성한다.

### 처음 가정에 반대되는 관측

| 시험한 주장 | 직접 확인한 반례 | 판정과 최소 뒤집기 자료 |
|---|---|---|
| 리뷰 링크가 나오고 설계가 바뀌면 링크가 새 대안을 알려준 것이다 | L-P2: [51166](https://github.com/pandas-dev/pandas/pull/51166)의 작성자는 원 PR51116의 jbrockmendel이며 2023-02-04 개설. [52043](https://github.com/pandas-dev/pandas/pull/52043)은 3/17 03:36:48, [52053](https://github.com/pandas-dev/pandas/pull/52053)은 16:00:14 공개. 첫 reviewer 링크는 [18:45:21](https://github.com/pandas-dev/pandas/pull/51116#issuecomment-1474263974) | 동일 목적 재설계는 링크 전에 이미 진행. 새로운 미인지 대안의 발견으로 코딩 불가. 링크 이후 추가로 바꾼 결정과 그 이유를 적은 작성자 기록이 있어야 링크의 별도 기여를 판정할 수 있음 |
| 선택 PR의 후속 commit이 0이면 동일 요구의 코드 수정도 0이다 | [작성자 응답1474292973](https://github.com/pandas-dev/pandas/pull/51116#issuecomment-1474292973)은 선행 후속 작업을 연결. [52089 patch f95152e](https://github.com/pandas-dev/pandas/commit/f95152e78c8baa2b1f4e07ecebb31496b3956c65)의 groupby.py/ops.py가 any/all을 공통 WrappedCythonOp로 실제 이동. PR52089 공개는 3/20 17:37:25, 원PR 종결은 17:38:10 | 원사건의 같은 작성자·같은 목적 후속 변경은 1건 있음. 표본PR를 추가하지 않고 L-P2에 연결. 링크 전 착수 사건을 빼는 감도에서는 이 건을 제거 |
| 작성자가 링크 내용에 반응하면 이를 구현한다 | L-P1 [1454857966](https://github.com/pandas-dev/pandas/pull/51109#issuecomment-1454857966)은 _name 패턴을 언급하지만 [1455017479](https://github.com/pandas-dev/pandas/pull/51109#issuecomment-1455017479)는 기존 fastpath=True로 충분할 수 있다고 반박. surviving selected PR commits는 모두 3/4 링크 전 | 열람을 시사하는 구체 반응과 실행은 다름. 삭제/force-push된 postlink 실제 패치가 공개 복원되면 구현 없음 판정을 재검토 |
| 링크 없는 PR은 비교에 쓸 정보가 없다 | N-P1 [실패 리뷰1233452129](https://github.com/pandas-dev/pandas/pull/50523#pullrequestreview-1233452129) 뒤 [cf06a273](https://github.com/pandas-dev/pandas/commit/cf06a2739af1fccfafaaa8e779e6cb03eb741d45), b6fa7aef,9a740a67,4989672f에서 작성자 수정. 끝내 [실패 재리뷰](https://github.com/pandas-dev/pandas/pull/50523#pullrequestreview-1234720872) 후 비병합 종결 | 실패 시험과 진단 권고만으로도 수정이 일어남. 무링크 사례는 요구·품질·시간이 맞지 않아 절감 비교군으로 계산하지 않음 |
| 모든 URL은 리뷰어가 새로 제시한 선례다 | N-P4 [author comment1084146158](https://github.com/pandas-dev/pandas/pull/50539#discussion_r1084146158)가 본인 [issue49523](https://github.com/pandas-dev/pandas/issues/49523)을 제시하여 리뷰어의 index.name 해석을 바로잡음. 이는 원 PR 전에 작성한 문제·대안 | 링크 제공자는 원 저자이고 지식은 선행. reviewer-선례 사건 수에 넣지 않음 |
| 코드에 있는 주석·reference 변경은 설계 변경이다 | N-P3 [7c60cfbe](https://github.com/pandas-dev/pandas/commit/7c60cfbe22e66146fb1adfdb3c61448e3d27d290)는 release note의 ??를 현재 PR50533으로 바꿈. N-P4 [c9ca480c](https://github.com/pandas-dev/pandas/commit/c9ca480c4c9c63b8f49666240dac0fbb6258e2cb)는 이유 주석/문구만 추가 | runtime 설계 유지와 설명 추가를 분리. N-P4의 후속 CoW test 기대값 보정도 별도 유형 |
| git 작성자 이름이 같으면 원 PR 작성자가 고친 것으로 엄격히 확정할 수 있다 | N-P2 [ea6a3087](https://github.com/pandas-dev/pandas/commit/ea6a308789e744db582b06cb084ed4f41502f1e0)는 Git name David Kleindienst, GitHub author XimesDK(254503752). PR 및 [분리 완료 답변](https://github.com/pandas-dev/pandas/pull/50530#discussion_r1061222269)은 DavidKleindienst(71123708). squash author는 원 PRauthor | 실제 동일인일 수 있지만 계정 ID가 다름. 엄격한 개별 패치 동일작성자는 미확인, 작성자 발언을 수용하는 넓은 attribution을 별도 감도로 둠 |
| 수치가 있는 시간은 작업 노동시간이다 | L-P1 PRbody의 %prun 31.655→20.328초, [3/4 응답](https://github.com/pandas-dev/pandas/pull/51109#issuecomment-1454857966)의 %timeit17.2→9.93초, [3/24](https://github.com/pandas-dev/pandas/pull/51109#issuecomment-1483371816)의13.5→10.3초 | 모두 프로그램 실행시간. 사람 능동 작업 시작/중지 또는 본인 소요시간 진술이 아니므로 labor나 savings로 산입하지 않음 |

### 링크 내용의 읽음과 최초 발견

L-P1은 target의 _name 설계와 벤치마크 효과를 작성자가 직접 논의했으므로 target-specific engagement는 확인된다. L-P2 역시 API를 비교하고 기존 대체 PR을 연결한다. 하지만 두 경우 모두 자료를 읽었다는 명시 표현, 처음 알았다는 당사자 표현은 없다. 엄격한 명시 열람 수는 0/2이고 구체 내용 참여는 2/2이다. 읽지 않았다는 뜻이 아니라 직접 명시 진술의 부재다.

L-P2의 이전 저작은 사전 인지의 당사자 산출물 근거다. 이를 literal "이미 알았다" 진술로 바꾸지 않았다. natural 층에는 적격 reviewer 링크가 없으므로 링크를 조건으로 한 열람/최초발견 비율은 해당 없음이다.

### 실제 수정과 공표의 시간 경계

L-P2를 단순 실패로 처리하면 중요한 수정 증거를 놓친다. 후속 f95152e는 동일 작성자의 실제 공통 경로 코드이고, PR52089 개설은 원PR 종결 45초 전이다. 다만 git author/committer17:36:45를 public push 시간으로 간주하지 않았다. 17:37:25는 새 PR 공개 시각이고 바로 직전 생성된 surviving single commit의 정확 최초 공개 head는 별도 미확인이다. 원PR 작성자가 종결 때 이 후속PR을 직접 지목한다.

PR52089 merge 20:37:23은 원PR 첫 종결 17:38:10 뒤이므로 주 관측창의 병합으로 세지 않는다. target51166의4/5 병합도 후기다. 반면52053의3/20 17:17:55 병합은 창 안에 있으나 그 설계 코드는 링크 전에 이미 공개했다.

L-P1 target51784는3/4 13:23:42에 새로 공개되어 리뷰 링크보다3분50초 앞선다. 2/1 최초 설계 때는 제공할 수 없었던 선례다. target의 핵심 f516f4f5 코드도 링크 전 작성됐고, 링크 뒤 ce2bedb9는 다른 저자가 name 내부속성 처리를 보정한 코드다. 3/23 병합은 원PR 관측창 안이지만 원PR 저자가 자기 구현을 고친 증거가 되지는 않는다.

### 사람별 관점

| 관점 | L-P1 관측 | L-P2 관측 | 제품 적용 조건 |
|---|---|---|---|
| 선례 제공자 | reviewer는 자신이 막 공개한 대안을 비교 기준으로 제시하고 프로파일 측정 편향을 지적 | reviewer는 원 작성자가 이미 만들던 API의 일관성을 묻음 | 링크 추천은 신규 정보 제공, 비교 시험, 기존 지식 재상기, API 일관성 질문을 구분해야 함 |
| 실제 수정자 | 원 작성자는 재측정/설명 후 종결; 대안 코드는 reviewer가 작성 | 원 작성자가 이전에 시작한 여러 PR을 통해 같은 요구를 구현 | 변경의 실제 actor와 작업 branch/후속 PR 추적이 필요. 원PR commit 수만으로 완료 판정 금지 |
| 결과 소비자 | 프로그램 이용자는 나중에 main에 병합된 메타데이터 최적화를 사용할 수 있으나 사람 노동절감 증거 없음 | EA 구현자에게 통일된 dispatch 방향이 생기지만 모든 소비자의 실제 사용/품질검사는 미관측 | 제품 주장은 참고·비교·후속 구현 수준으로 제한하고 사용자 시간 절감은 별도 측정 |

### 같은 작성자와 타인 구현을 포함한 감도

주 분모는 추가층 2개이며 같은 작성자의 링크 뒤 같은 목적 실제 후속 패치는 1/2(L-P2), 엄격한 링크-기인 사슬은 확인 0/2다. L-P2는 이미 착수한 재설계를 이어간 사례로, 그 사건을 빼면 남은1개에서 same-author postlink patch는0/1이다.

타인 구현까지 포함하면 L-P1에도 target ce2bedb9 후속보정과540db96b 병합이 있다. 넓은 '링크 뒤 관련 구현 공표'는 2/2로 커질 수 있으나 같은 저자·같은 설계 수정이라는 주 질문의 분자와 합치지 않는다. 그 target 핵심 구현 역시 링크 전에 시작되어 있었다. 이러한 확장은 엄격 사슬이나 미인지 발견을 새로 입증하지 않는다.

Natural4건은 모두 reviewer 선례URL0이며, 후속 runtime 수정이 직접 보이는 것은 N-P1(1/4)이다. N-P2는 테스트 구조, N-P3는 문서, N-P4는 주석 및 별도 테스트 기대값 변경이다. 자연층 전체에 인간 직접시간/자기보고시간/동등품질 시간쌍은 관측되지 않았다.

### 시간창 감도와 음성 사례의 보존

sensitivity.csv는 고정된6슬롯에30/60/90일 경계만 바꾼18행이다. 짧은 창에서 링크가 사라져도 표본을 다시 고르지 않았다.

| 고정 pandas 층 | 30일 | 60일 | 90일 |
|---|---|---|---|
| natural4 | reviewer 선례0/4, 선택PR 병합2/4 | 선례0/4, 병합3/4 | 선례0/4, 병합3/4 |
| link-priority2 | 첫링크0/2; 링크조건후속변경 해당 없음 | 링크2/2, 같은작성자후속변경1/2, strict0/2 | 링크2/2, 같은작성자후속변경1/2, strict0/2 |
| 인간시간 측정 가능 | 0/6; 값은 미확인 | 0/6; 값은 미확인 | 0/6; 값은 미확인 |

L-P1 링크가30일 경계보다하루늦고 L-P2 링크는44일째다. L-P1 종결은60일밖이지만90일안. N-P4 병합은30일밖이고60일안이다. 현재 타임라인에서 재오픈 사건은 없었다. N-P2 merge/closed의1초차를 늦은시각으로 잡아도 substantive 판정은 바뀌지 않는다.

### 비용 숫자가 있으나 노동은 아닌 시간선

L-P1:2/1 제안body의 profiler실행초 →3/4 reviewer 측정방법 교정+target링크 →6시간31분25초 후 author의 timeit 숫자/설계아이디어 →3/23 다른저자target병합 →3/24 author가잔여이득감소설명 →4/11종결. 6시간31분25초는 응답 경과시간이고 능동 작업시간이 아니다. 생성부터 종결까지5,951,295초도 동일하다.

L-P2:3/17 03:36 기존후속52043 공개 →16:00 기존후속52053 공개 →18:45 최초reviewer링크 →27분36초 후 author응답 →3/20 17:37 후속52089 공개 →45초 후원PR종결. 첫 링크부터후속PR공개255,124초는 경과시간이다. 선행작업,다른리뷰,테스트실패,CI대기,주말을 이 값에서 분리할 근거가 없다.

### 노동절감 판정을 가능하게 하는 최소 추가 기록

동일 요구와 회귀시험 통과 수준을 고정한 다음, 실제 사람의 설계 탐색·읽기·수정·시험작업을 actor와 시작/중지로 기록해야 한다. 중단·CI대기·다른 일·동료 수정은 별도 구간으로 구분한다. 기존 대안을 언제 알았는지 당사자가 당시 남긴 기록과, 링크가 없었던 동등 품질 대조 조건의 사람시간이 필요하다. 같은PR의 전후 runtime 수치나 선택창 elapsed를 대조 시간으로 쓰면 안 된다.

### 검토의 성격과 남은 취약점

이 문서와 원장은 같은 AI 조사자의 자체 재판독이다. root의 통합 점검도 AI 팀 내부 교차검토이며 외부 인간 독립 판독으로 부르지 않는다. 선택 시 #51116의 두번째 reviewer URL문장이 우발 노출된 점, 추가층 자격규칙 R01 정정, 최초head 미확인은 선정 원격 SHA와 REVISIONS.md에 보존된다. 결론을 지지하는 사례만 남기지 않았고 실패·무링크·설계유지·이미착수 사건을 모두 유지했다.


## scikit-learn 상세 대조

## scikit-learn 후속 판독과 반증

선정 원격 봉인은 994e21aaea7c5da0c4322db9d1ce2c4f52fa6a2f이다. 이 파일은 봉인 뒤 읽은 결과이며 frame.csv·selection.json의 당시 판정을 덮어쓰지 않는다. 선정 당시 N-S2의 초기 코드 미확인 표시는 보존한다. 이후 review1233732288의 원래 head d5a1cbaf23a471e0c87ddad123a22f85fd104932를 복구하여 구체적 구현이 있었다는 점을 확인했다. 묶음3 시점에는 최초 업로드 SHA를 별도 플랫폼 기록으로 고정하지 못했으나, R02에서공개opened이벤트미러와정확GitHubdiff로첫판을보완했다. 원PR종결전후속push손실은여전히미확인이다.

### 첫 링크가 곧 설계 변경의 원인이 되는가

자연층 4건에서는 적격 리뷰 선례 링크를 확인하지 못했다. 추가층 2건에서는 링크 뒤 같은 목적의 실제 패치가 발견되지만, 첫 링크를 원 작성자의 명시적 연결 발언과 완결된 시험·반영까지 잇는 엄격 사슬은 0건이다. 이는 링크가 효과가 없었다는 추정이 아니다. 공개 원문이 첫 링크의 독립적인 기여와 작업시간을 분리해 주지 않는다는 판정이다.

| 슬롯 | 링크 직전 선택과 이후 변경 | 첫 링크 연결을 약화시키는 원문 |
|---|---|---|
| N-S1 #25265 | validate_params를 처음부터 사용. 이후 유지보수자가 빈 줄만 삭제. | [초기 a5d94d](https://github.com/scikit-learn/scikit-learn/commit/a5d94d234de3bb73ad262ca707a43b4161b7fe3c), [564cdae](https://github.com/scikit-learn/scikit-learn/commit/564cdae490d1a123144052db0bd75fbddd1adcb5), [선행 이슈24862 Steps](https://github.com/scikit-learn/scikit-learn/issues/24862). 공통 부품은 리뷰 전 선택되어 있었다. |
| N-S2 #25268 | check_is_fitted와 whitelist 10개 제거를 원 리뷰 head에서 복구. 닫히기 전 후속 패치는 미복구. | [review1233732288](https://github.com/scikit-learn/scikit-learn/pull/25268#pullrequestreview-1233732288)는 changelog 요청. 현재 commits=[]는 무작업의 증거가 아니다. |
| N-S3 #25269 | 초기 입력검증 유지. 유지보수자가 공통 시험의 wrapper 매핑만 삭제. | [fa3c1cb](https://github.com/scikit-learn/scikit-learn/commit/fa3c1cb6ba3a1504c87d17cede4ec4a602e924c8). 작성자 교체와 시험 등록 수정을 설계자의 선례 채택으로 합치지 않는다. |
| N-S4 #25274 | 수치 DataFrame 허용·문자열 혼합 거절은 첫 패치에 완성되어 있다. 뒤 수정은 PR 번호/문구. | [초기 1e55ead](https://github.com/scikit-learn/scikit-learn/commit/1e55ead018c0230f6d1c10b471b6d73d47092bf6), [review1234551573](https://github.com/scikit-learn/scikit-learn/pull/25274#pullrequestreview-1234551573). [선행 이슈19905](https://github.com/scikit-learn/scikit-learn/issues/19905)의 문자열 지원 기대와 최종 거절 동작도 구별한다. |
| L-S1 #25535 | a897a34 testing helper는 미지원 입력 예외를 xfail 처리. 첫 링크는 외부 엔진 시험 워크플로. 이후 fcharras가 feaabb7e에서 예외/xfail 제거. | [첫 댓글1422865990](https://github.com/scikit-learn/scikit-learn/pull/25535#issuecomment-1422865990), [feaabb7e](https://github.com/scikit-learn/scikit-learn/commit/feaabb7e6f2ccecced7a6847a267ad54b026f8a3). 수정자는 원 PR 작성자 ogrisel이 아니며, [후속25605](https://github.com/scikit-learn/scikit-learn/pull/25605)는 미병합. 원 작성자 후기 패치는 강제 push 때문에 미확인이다. |
| L-S2 #25540 | const floating을 구체 DOUBLE_t로 변경한 eb6a658b가 같은 작성자에게서 확인되고 최종 병합에도 남는다. | [사전 실패1416766187](https://github.com/scikit-learn/scikit-learn/pull/25540#issuecomment-1416766187), [감사1416936430](https://github.com/scikit-learn/scikit-learn/pull/25540#issuecomment-1416936430), [작성자 caller 분석1418381186](https://github.com/scikit-learn/scikit-learn/pull/25540#issuecomment-1418381186), [eb6a658b](https://github.com/scikit-learn/scikit-learn/commit/eb6a658b0ada3464e0fa79da716f57af053141fe). 감사는 열람·최초 발견·수정 원인 진술과 같지 않다. |

#### 같은 PR 안에서 더 강한 사슬과 무링크 수정이 모두 보인다

L-S2의 두 번째 Cython 이슈 [5243](https://github.com/cython/cython/issues/5243)는 [review1285216537](https://github.com/scikit-learn/scikit-learn/pull/25540#pullrequestreview-1285216537)에서 n_classes 생성자에 ndarray를 유지하라는 이유로 제시됐다. 작성자는 [1097398366](https://github.com/scikit-learn/scikit-learn/pull/25540#discussion_r1097398366)에서 동의하고 [a1dbdc](https://github.com/scikit-learn/scikit-learn/commit/a1dbdc1d8aa1060f60bae2ddd8b7423e0288d33f)에서 실제로 되돌렸다. 이 더 명확한 사건을 첫 Cython5230 링크 대신 선택하면 성공 사례를 사후 선별하게 된다. 따라서 첫 사건의 엄격 분자는 늘리지 않는다.

그 뒤 thomasjpfan은 [review1289640474/1100444710](https://github.com/scikit-learn/scikit-learn/pull/25540#discussion_r1100444710)에서 PyArray API가 직접 ndarray를 다루도록 설계됐다고 설명했다. 이 설명에는 새로운 선례 URL이 없다. 작성자는 [e7e806](https://github.com/scikit-learn/scikit-learn/commit/e7e806bfe356d1ca62e26735b9136571efb318c4)에서 두 반환 함수의 ndarray를 복원하고 [1100471666](https://github.com/scikit-learn/scikit-learn/pull/25540#discussion_r1100471666)에서 컴파일 확인을 보고했다. 링크를 제공하는 기능과 정확한 맥락 설명을 제공하는 기능은 이 관측에서 분리되어야 한다.

첫 참고 이슈 [Cython5230](https://github.com/cython/cython/issues/5230)의 재현은 NumPy 사용자 정의 fused type과 const memoryview의 컴파일 실패다. 최초 TreeBuilder 댓글의 dispatch signature 실패와 구체적인 오류 경로가 동일하다고 증명되지 않았다. 함께 링크된 [HackMD 노트](https://hackmd.io/FR4Vp_OgR-WhlVEsVZzsIw/download)는 현재 본문을 읽었지만 2023-02-04 판이 없다. 현재 노트의 표현을 그때 이미 전달된 지식으로 소급하지 않는다.

### 사람 시간과 비용의 경계

| 기록 | 관측 단위 | 허용되는 해석 | 허용되지 않는 해석 |
|---|---|---|---|
| L-S2 첫 링크 2023-02-04 17:13:52 → 첫 관련 git committer date 2023-02-06 07:55:24 | 139,292초의 경과 | 토요일부터 월요일까지의 달력 간격. 원 작성자 리뷰로 공개 패치가 관측되는 상한 07:57:51까지는 139,439초. | 38시간 41분의 노동, 링크가 아낀 시간, CI 대기시간. |
| L-S2 17개 surviving commits 중 첫 링크 뒤 16개 | 커밋 16개: 일반 패치13+merge3; 실제 변경 파일3개 | 반복 수정 산출물이 존재. | 13회 사람 작업 세션 또는 고정 시간 환산. |
| L-S1 작성자 2023-02-03 시험 보고 | 6.31초의 기계 시험 실행, 15 failed/27 passed 등 | 첫 링크 이전에 실패와 수정 필요를 알고 있었다. | 사람의 직접 작업시간 6.31초. [댓글1416034432](https://github.com/scikit-learn/scikit-learn/pull/25535#issuecomment-1416034432). |
| N-S4 선행 소비자 2022-12-30 보고 | 비수치 자기보고 many hours | 실제 사용자가 DataFrame 실패를 디버깅하는 비용을 호소했다. | 원 PR 작성자의 수정시간, 첫 공개 이후 관측창 노동, 정확한 시간 수치. [issue25261 Describe the bug](https://github.com/scikit-learn/scikit-learn/issues/25261). |
| Cython5230 유지보수자의 weekend 계획 | 미래 작업 계획 | 수정 의향. | 실제 소요시간 또는 작업 완료. [1405427210](https://github.com/cython/cython/issues/5230#issuecomment-1405427210). |

직접 시작/중지 로그, 표본 작성자의 수치 소요시간 자기보고, 동일 품질의 무링크 시간 비교는 각각 0/6이다. 실제 사람 시간은 미확인이다. 비교 가능한 쌍을 분모로 하는 절감률은 0/0이므로 해당 없음이다. 절감량을 0으로 대체하지 않는다. 최소 추가 기록은 첫 실패/요구·직전 판, 첫 자료 노출 시각과 기존 인지 여부, 수정 구간별 실제 시작/중지와 중단 사유, 구현자 구분, 같은 회귀 입력/기대 출력의 전후 통과, 동일 난이도·동일 품질의 무링크 과제 시간을 한 묶음으로 남기는 것이다.

### 관측창·작성자·선행 수정 감도

자연 4건과 L-S2는 모두 5일 안에 종결되어 30/60/90일 절단 변경으로 표본 내 결과가 바뀌지 않는다. L-S1은 각각 2023-03-05/04-04/05-04 14:18:47Z에 끝난다. 첫 링크와 다른 작성자의 feaabb7e는 30일 안에 있어 확인된 링크2건, 같은 작성자 변경1건+미확인1건, 타인 포함 변경2건, 엄격 사슬0건은 세 창에서 동일하다. 이는 강제 push로 잃은 코드를 되찾았다는 뜻이 아니다.

N-S4는 PR API merged_at/closed_at가 2023-01-03 15:46:22Z이고 timeline closed가 15:46:23Z다. 1초를 바꿔도 사건 분류는 같다. reopen은 6개 공개 timeline에서 확인되지 않았다.

같은 작성자만 인정하면 추가층 변경은 확인1/2, 미확인1/2다. 다른 작성자까지 포함하면 확인2/2다. L-S1의 패치는 여전히 미병합 브랜치 수정이고 엄격 인과/노동 사슬은 0/2다. 이를 원 작성자가 자료를 읽고 고쳤다는 2/2로 바꾸면 안 된다.

첫 링크 전에 같은 구체적 후속 패치가 이미 올라왔다는 증거는 두 추가층 사건에서 확보하지 못했다. L-S2에는 첫 링크 전 사전 실패, L-S1에는 엔진 시험 관련 사전 수정·green 보고가 있다. 구체 패치 선행을 확인한 사례만 제외하는 좁은 감도에서는 제외0/2, 결과 동일이다. '이미 문제를 알고 넓은 수정 작업이 진행 중인 사건'까지 배제하는 넓은 감도에서는 두 사건이 모두 빠져 분모0, 조건부 비율은 해당 없음이다. 이 두 제외 규칙을 섞지 않는다.

#### 첫 종결 이후의 두 후기

N-S2 원 PR은 2023-01-04 22:30:46Z 닫혔다. 같은 작성자는 22:52:31Z에 [PR25294](https://github.com/scikit-learn/scikit-learn/pull/25294)를 만들고 [1371521054](https://github.com/scikit-learn/scikit-learn/pull/25294#issuecomment-1371521054)에서 이전 PR의 실수와 changelog 추가를 설명했다. [35b5ee](https://github.com/scikit-learn/scikit-learn/commit/35b5ee65770ee7fb7bf15d0acb2ee96d7d3bf1ab)는 같은 기능과 시험을 병합했다. 이는 닫힌 PR을 작업 포기로 단정하는 반례다. 원 관측창과 첫 선례 링크 분자는 바꾸지 않는다.

L-S2는 2023-02-09 병합 뒤 [25584](https://github.com/scikit-learn/scikit-learn/issues/25584)의 read-only 역직렬화 문제가 나왔다. [25585](https://github.com/scikit-learn/scikit-learn/pull/25585)의 실제 패치는 cnp.PyArray_DATA로 바뀌고 joblib mmap_mode='r' 회귀시험을 추가했다. 초안 본문의 const 계획과 최종 구현이 다르다. 첫 병합을 같은 품질의 완료 또는 절감의 증거로 삼기 어려운 후기이며, PR25540의 관측창을 임의로 늘려 본분자에 합치지 않는다.

### 세 관점과 적용 조건

링크 제공자는 발견한 제한과 재현 가능한 예제를 전달한다. Vincent의 두 Cython 링크는 서로 다른 실패를 다루며, fcharras의 워크플로는 외부 엔진이 공통 시험을 돌리는 실무 맥락을 제공한다. 수정자는 caller의 실제 타입, 기존 지원 범위, public ndarray 계약을 유지해야 한다. 따라서 예제에 나온 표면 형태를 그대로 적용하는 것이 목적이 아니다. 결과 소비자는 joblib read-only 버퍼, 수치 DataFrame, sparse/dense fit/predict 등 실제 입력 조합이 유지되는지에 영향을 받는다. [betatim1429734094](https://github.com/scikit-learn/scikit-learn/pull/25535#issuecomment-1429734094)는 일부 외부 엔진의 제약과 scikit-learn의 합리적인 기본 사용을 구별한다.

탐색기에게 이 자료가 지지하는 제품 표현은 '같은 목적의 선례와 적용 제약을 원문으로 찾게 돕는다'까지다. 일부 공개 리뷰 뒤 실제 수정이 있었다고 사례별로 말할 수 있지만, 첫 선례 링크가 원 작성자의 변경을 일으켰다거나 노동을 절감했다는 일반 수치는 이 표본에서 추정할 수 없다.

### 판독 오염·복구 제한과 재개 지점

선정 전 L-S1의 URL 필터가 90일 뒤인 9월 reviewer의 branch/force-push 상태를 노출했다. 선택 전 완전한 결과 가림은 충족되지 않는다. 자연 rank9 #25275의 9월 surviving patch와 rank7 #25272의 개설 다음 날 committer 판도 초기판으로 고정할 수 없다. 당시에는후자의최초공개diff동일성을입증하지못했다. R02에서opened head33ee1f59a66304eb16534be16f1a0287f13a95dc의실제testseed두줄교체를확인하여제외타당성을보완했다. 이 행은 screening-attempts.jsonl에서 명시했고 원 슬롯을 교체하지 않았다. 추가독립대조의첫자료는 #25272 원형GHArchivegzip의opened eventID다. 기존 review1234637508의 head be3bdde4만으로 1월2일 최초 head는 복구되지 않았다.

이 stream의 판독은 AI 연구자의 자체 판독이다. root의 L-S2 교차 재열람 역시 같은 실행 계열의 별도 AI 판독이며 외부 독립 인간 판독으로 표현하지 않는다. 별도 음악/지도 사례는 다른 담당 stream에서 결합된다.

## 음악 카탈로그와 지도 상세 대조

## AF-RES-046 · 음악 카탈로그·지도 편집 비교

두 사례는 **목적표집한 반례이며 PR 12슬롯의 분모 밖**이다. MusicBrainz는 공개 당사자 토론까지, OpenStreetMap은 실제 객체 전후판까지 읽었다. 두 분야 모두 사람의 작업 시작·중지 기록이나 동등 품질의 시간 비교는 없다. AI 분담 조사·자체 판독이며 외부 인간 독립 검토가 아니다.

### X-OS · 실제 변경이 링크보다 먼저였고 수정자도 달랐다

| 고리 | 관측과 정확한 출처 |
| --- | --- |
| 최초 선택 | Halil Şimşek(uid12586560)이 node11329057532 v3에 `opening_hours=MON to SUN, 08:00 to 16:00`을 넣었다. [객체 이력](https://api.openstreetmap.org/api/0.6/node/11329057532/history), node version3, timestamp2026-11-17T00:19:27Z, changeset192056303. |
| 실제 수정 | **다른 사람** BaguetteYeeter(uid22550176)가 v4를 01:03:05Z에 올려 `Mo-Su 08:00-16:00`으로 바꿨다. v3/v4 태그·좌표 대조에서 바뀐 필드는 opening_hours 하나다. [실제 패치](https://api.openstreetmap.org/api/0.6/changeset/192057263/download), modify/node11329057532 version4. |
| 링크 제시 | 그 수정자가 01:03:31Z에 원 changeset의 comment1691186으로 [opening_hours 규범](https://wiki.openstreetmap.org/wiki/Key:opening_hours)을 소개하고 자기 선행 수정을 가리켰다. [공개 토론](https://api.openstreetmap.org/api/0.6/changeset/192056303?include_discussion=true), discussion/comment1691186. |
| 작성자 응답 | 2026-11-22 조회에서 댓글1개이며 원 작성자의 응답은 관측되지 않았다. 읽음·이미 알았음·최초 발견은 미확인이다. |
| 시간·판정 | 수정은 링크보다 **26초 앞선다**. 최초 v3→v4의 **43분38초는 경과시간**이다. 후속 changeset 생성→종료1초도 작업시간이 아니다. 같은 작성자의 링크 후 수정 엄격사슬은 성립하지 않는다. |

역사적 판과 작성자 ID를 빼고 “규범 링크가 있는 토론 + 수정된 필드”만 조인하면 양성처럼 보인다. 여기서는 공개된 순서 자체가 그 해석을 뒤집는다. **타인 구현까지 허용해도 실제 수정이 링크 이전이므로 ‘그 링크 후의 수정’으로 바뀌지 않는다.** 사적 대화를 배제할 수는 없지만 공개 링크가 수정에 앞섰다는 주장도 할 수 없다.

원 작성자는 현장 지식을 데이터로 표현하려는 사람이고, reviewer는 형식을 고치는 수정자이자 자료 제공자였다. 소비자 관점에서는 같은 영업시간 주장을 규범 문법으로 읽을 수 있다는 이점이 예상되지만, 실제 파서 실행·지도 서비스 반영·현장 영업시간의 진실성은 확인하지 않았다. 이 예상 이점을 실제 소비자 성과나 절감량으로 기록하지 않는다. 규범의 `Wd`, `fixed_time`, `HH`, `mm` 절을 읽었으며 현재 페이지가 oldid3116008과 2026-11-16 수정일을 표시한다. oldid URL의 별도 재개방은 실패했으므로 reviewer의 실제 열람판까지 확정하지 않는다.

관측 끝은 node history를 획득한 2026-11-22T22:06:57Z다. v1–v4가 반환됐으며 미래 수정 부재를 뜻하지 않는다. map 사례에는 PR의 폐쇄→90일 규칙을 이식하지 않았다. 업로드 changeset은 댓글이 달리기 전에 닫히는 단위여서 그 규칙을 적용하면 공개 리뷰 자체를 놓친다.

### X-MB · 취소·타인 수정 보고는 보이지만 원장 적용은 미확인

초기 후보는 공식 스타일 규칙이 인용한 [edit6892422](https://musicbrainz.org/edit/6892422)였으나 공개 요청이403이었다. 다음 공개 검색에서 당사자들이 게시한 [Portuguese help needed for release](https://community.metabrainz.org/t/portuguese-help-needed-for-release/348556)를 찾았다. 포럼은 읽었지만 이를 비공개 edit notes의 복원이나 실제 적용 원장으로 취급하지 않는다.

| UTC · 고유 발행 ID | 직접 관측한 당사자 발언의 요지 |
| --- | --- |
| 2017-12-25 07:35:51.659 · post364166/#1 | thwaller는 이미 원자료에서 곡명을 가져와 제목 수정을 시도했고 언어 도움을 요청했다. |
| 12-25 15:54:31.855 · post364243/#2 | sibilant가 이미 문장형 대문자 표기로 고쳤다고 보고했다. |
| 12-26 20:46:54.892 · post364531/#4 | sibilant는 제목을 제안하고 [편집49854105](https://musicbrainz.org/edit/49854105)와 충돌한다고 설명했다. [레이블 소개 링크](http://juninhocds.com.br/home/sobre)는 공연 녹음·배포 설명에 붙었으며 제목 표기 규범과 같은 근거가 아니다. |
| 12-26 22:19:07.269 · post364548/#5 | thwaller는 다른 편집자가 제목을 고칠 수 있도록 해당 편집을 취소했다고 보고했다. |
| 12-26 22:48:07.319 · post364555/#6 | sibilant가 수정 제출을 보고했다. 실제 적용 여부는 이 발언만으로 알 수 없다. |
| 12-27 15:32:12.458 · post364689/#9 | 수정 보고 **다음 날** [포르투갈어 스타일 규칙](https://musicbrainz.org/doc/Style/Language/Portuguese)을 제시했다. |

각 발언의 UTC와 수정일은 [공개 JSON](https://community.metabrainz.org/t/348556.json)의 post ID로 확인했다. #4와 #9는 당일 수정됐고 #8은2023년에 수정됐다. 개별 노트의 원래 문구와 현재 표시 문구를 무조건 동일시하지 않는다. 정확 초기 제목·원 edit의 작성자·실제 취소 상태·후속 적용 필드는 원장에서 미확인이다. 이 사례는 **공개 수용 표현이 원 작성자의 실제 변경을 대신하지 못한다**는 부분 반례다.

공식 [편집 규칙](https://musicbrainz.org/doc/Edit)의 Applied/Cancelled/Failed prerequisite는 서로 다른 상태이고, [노트 작성법](https://musicbrainz.org/doc/How_to_Write_Edit_Notes)은 원 편집자의 취소 응답과 제3자의 검토를 허용한다. [공식 이력의2020-02-18 항목](https://musicbrainz.org/history)은 편집 이력 공개와 노트 비공개를 구분한다. 이번 원 edit와 [릴리스 편집 이력](https://musicbrainz.org/release/eaad4dfb-0766-44ea-9f8c-a5521c6f6da9/edits)은 일반 공개 HTTP에서도403이었다. 정책 설명이 그403의 구체 원인이라고 단정하지 않으며 로그인이나 다른 접근 경로로 제한을 우회하지 않았다.

레이블 링크→취소 보고의 약92분12초도 경과시간이고, 노동 투입이나 절감이 아니다. 자료 제공자는 해석·검토를, 원 편집자는 충돌 해소를, 다른 편집자는 수정 제출을 맡았다는 공개 보고가 있다. 소비자는 정리된 카탈로그를 볼 수 있으나 실제 적용·소비 결과는 이번 자료에서 관측되지 않는다.

### 반증 탐색과 전이 경계

OSM에서 처음 연 changeset180981580은 indoor mapping 규범 링크가 있으나 응답이 없었고, 검색의 인접 결과181032160은 다른 지역69객체 복원이다. 둘을 하나의 전후 사슬로 연결하지 않았다. 이후 opening_hours 사례는 실제 객체 버전과 작성자를 모두 조인할 수 있어 선택했다. 성공 여부를 가린 확률표본이 아니므로 두 분야의 발생률·양성 비율을 계산하지 않는다.

MusicBrainz에서는 규칙 링크의 원 사례를 읽으려는 시도와 별도 공개 포럼을 구분했다. 포럼만으로 누락된 편집 노트를 채우지 않는다. 스타일 자료는 적용되는 언어·필드가 중요하다. 레이블의 업무 설명을 제목 대문자 규칙의 근거로 잘못 연결하면 ‘같은 목적’ 판정부터 틀린다.

### 필요한 최소 후속 자료와 수용 상태

| 미확인 | 첫 재개 행동 | 판정이 바뀌는 조건 |
| --- | --- | --- |
| MusicBrainz 실제 전후·적용 | edit49854105와 같은 release의 후속 edit에 대해 발행자가 허용한 공개 원장/내보내기를 확보한다. 원 제안 필드·노트·수정자·created/applied/cancelled를 조인한다. | 공개 원장이 당사자 보고와 일치하면 실제 취소·타인 구현 단계까지 확장할 수 있다. 같은 작성자 수정으로 바꾸려면 그 작성자의 후속 edit가 따로 필요하다. |
| OSM 원 작성자 읽음·후속 수정 | comment1691186 이후 원 작성자의 새 답과 node history를 다시 읽는다. | 새로운 같은 목적·같은 작성자 변경이 관측되면 별도 후속 사건으로 기록한다. 이미 확인한 v4의26초 선행은 바뀌지 않는다. |
| 두 분야 노동·절감 | 동일 요구·품질 판정, 사람 활동 시작·중지, 대기, 무링크 비교를 연결하는 기록을 확보한다. | 비교 가능한 사람 시간 쌍이 생겨야 절감량을 계산한다. 현재는 미확인이다. |

출처 원장20행 중 고유 직접 판독1차 저작은14개다. 요구된 분야별 최소 배당은 **음악 운영규칙1 + 지도 편집 원장1 + 지도 객체 버전1 =3/4**만 보수 산입했다. **음악의 개별 원장 직접 열람은 미충족**이다. 공개 포럼·추가 규칙을 읽었다고 이 누락을 감추지 않았다. 같은 포럼의9개 발언, node의4개 버전, 같은 changeset의metadata와download는 저작 수를 늘리지 않는다.
