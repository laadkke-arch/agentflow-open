# pandas: 반례와 적용 한계

이 파일은 6개 고정 슬롯의 해석이다. 참고 PR51784,51166,52043,52053,52089는 선택 사건의 원대상/후속 자료이며 새 표본 사례가 아니다. MusicBrainz/OSM 분모 밖 대조는 root 통합 조사에서 별도로 작성한다.

## 처음 가정에 반대되는 관측

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

## 링크 내용의 읽음과 최초 발견

L-P1은 target의 _name 설계와 벤치마크 효과를 작성자가 직접 논의했으므로 target-specific engagement는 확인된다. L-P2 역시 API를 비교하고 기존 대체 PR을 연결한다. 하지만 두 경우 모두 자료를 읽었다는 명시 표현, 처음 알았다는 당사자 표현은 없다. 엄격한 명시 열람 수는 0/2이고 구체 내용 참여는 2/2이다. 읽지 않았다는 뜻이 아니라 직접 명시 진술의 부재다.

L-P2의 이전 저작은 사전 인지의 당사자 산출물 근거다. 이를 literal "이미 알았다" 진술로 바꾸지 않았다. natural 층에는 적격 reviewer 링크가 없으므로 링크를 조건으로 한 열람/최초발견 비율은 해당 없음이다.

## 실제 수정과 공표의 시간 경계

L-P2를 단순 실패로 처리하면 중요한 수정 증거를 놓친다. 후속 f95152e는 동일 작성자의 실제 공통 경로 코드이고, PR52089 개설은 원PR 종결 45초 전이다. 다만 git author/committer17:36:45를 public push 시간으로 간주하지 않았다. 17:37:25는 새 PR 공개 시각이고 바로 직전 생성된 surviving single commit의 정확 최초 공개 head는 별도 미확인이다. 원PR 작성자가 종결 때 이 후속PR을 직접 지목한다.

PR52089 merge 20:37:23은 원PR 첫 종결 17:38:10 뒤이므로 주 관측창의 병합으로 세지 않는다. target51166의4/5 병합도 후기다. 반면52053의3/20 17:17:55 병합은 창 안에 있으나 그 설계 코드는 링크 전에 이미 공개했다.

L-P1 target51784는3/4 13:23:42에 새로 공개되어 리뷰 링크보다3분50초 앞선다. 2/1 최초 설계 때는 제공할 수 없었던 선례다. target의 핵심 f516f4f5 코드도 링크 전 작성됐고, 링크 뒤 ce2bedb9는 다른 저자가 name 내부속성 처리를 보정한 코드다. 3/23 병합은 원PR 관측창 안이지만 원PR 저자가 자기 구현을 고친 증거가 되지는 않는다.

## 사람별 관점

| 관점 | L-P1 관측 | L-P2 관측 | 제품 적용 조건 |
|---|---|---|---|
| 선례 제공자 | reviewer는 자신이 막 공개한 대안을 비교 기준으로 제시하고 프로파일 측정 편향을 지적 | reviewer는 원 작성자가 이미 만들던 API의 일관성을 묻음 | 링크 추천은 신규 정보 제공, 비교 시험, 기존 지식 재상기, API 일관성 질문을 구분해야 함 |
| 실제 수정자 | 원 작성자는 재측정/설명 후 종결; 대안 코드는 reviewer가 작성 | 원 작성자가 이전에 시작한 여러 PR을 통해 같은 요구를 구현 | 변경의 실제 actor와 작업 branch/후속 PR 추적이 필요. 원PR commit 수만으로 완료 판정 금지 |
| 결과 소비자 | 프로그램 이용자는 나중에 main에 병합된 메타데이터 최적화를 사용할 수 있으나 사람 노동절감 증거 없음 | EA 구현자에게 통일된 dispatch 방향이 생기지만 모든 소비자의 실제 사용/품질검사는 미관측 | 제품 주장은 참고·비교·후속 구현 수준으로 제한하고 사용자 시간 절감은 별도 측정 |

## 같은 작성자와 타인 구현을 포함한 감도

주 분모는 추가층 2개이며 같은 작성자의 링크 뒤 같은 목적 실제 후속 패치는 1/2(L-P2), 엄격한 링크-기인 사슬은 확인 0/2다. L-P2는 이미 착수한 재설계를 이어간 사례로, 그 사건을 빼면 남은1개에서 same-author postlink patch는0/1이다.

타인 구현까지 포함하면 L-P1에도 target ce2bedb9 후속보정과540db96b 병합이 있다. 넓은 '링크 뒤 관련 구현 공표'는 2/2로 커질 수 있으나 같은 저자·같은 설계 수정이라는 주 질문의 분자와 합치지 않는다. 그 target 핵심 구현 역시 링크 전에 시작되어 있었다. 이러한 확장은 엄격 사슬이나 미인지 발견을 새로 입증하지 않는다.

Natural4건은 모두 reviewer 선례URL0이며, 후속 runtime 수정이 직접 보이는 것은 N-P1(1/4)이다. N-P2는 테스트 구조, N-P3는 문서, N-P4는 주석 및 별도 테스트 기대값 변경이다. 자연층 전체에 인간 직접시간/자기보고시간/동등품질 시간쌍은 관측되지 않았다.

## 시간창 감도와 음성 사례의 보존

sensitivity.csv는 고정된6슬롯에30/60/90일 경계만 바꾼18행이다. 짧은 창에서 링크가 사라져도 표본을 다시 고르지 않았다.

| 고정 pandas 층 | 30일 | 60일 | 90일 |
|---|---|---|---|
| natural4 | reviewer 선례0/4, 선택PR 병합2/4 | 선례0/4, 병합3/4 | 선례0/4, 병합3/4 |
| link-priority2 | 첫링크0/2; 링크조건후속변경 해당 없음 | 링크2/2, 같은작성자후속변경1/2, strict0/2 | 링크2/2, 같은작성자후속변경1/2, strict0/2 |
| 인간시간 측정 가능 | 0/6; 값은 미확인 | 0/6; 값은 미확인 | 0/6; 값은 미확인 |

L-P1 링크가30일 경계보다하루늦고 L-P2 링크는44일째다. L-P1 종결은60일밖이지만90일안. N-P4 병합은30일밖이고60일안이다. 현재 타임라인에서 재오픈 사건은 없었다. N-P2 merge/closed의1초차를 늦은시각으로 잡아도 substantive 판정은 바뀌지 않는다.

## 비용 숫자가 있으나 노동은 아닌 시간선

L-P1:2/1 제안body의 profiler실행초 →3/4 reviewer 측정방법 교정+target링크 →6시간31분25초 후 author의 timeit 숫자/설계아이디어 →3/23 다른저자target병합 →3/24 author가잔여이득감소설명 →4/11종결. 6시간31분25초는 응답 경과시간이고 능동 작업시간이 아니다. 생성부터 종결까지5,951,295초도 동일하다.

L-P2:3/17 03:36 기존후속52043 공개 →16:00 기존후속52053 공개 →18:45 최초reviewer링크 →27분36초 후 author응답 →3/20 17:37 후속52089 공개 →45초 후원PR종결. 첫 링크부터후속PR공개255,124초는 경과시간이다. 선행작업,다른리뷰,테스트실패,CI대기,주말을 이 값에서 분리할 근거가 없다.

## 노동절감 판정을 가능하게 하는 최소 추가 기록

동일 요구와 회귀시험 통과 수준을 고정한 다음, 실제 사람의 설계 탐색·읽기·수정·시험작업을 actor와 시작/중지로 기록해야 한다. 중단·CI대기·다른 일·동료 수정은 별도 구간으로 구분한다. 기존 대안을 언제 알았는지 당사자가 당시 남긴 기록과, 링크가 없었던 동등 품질 대조 조건의 사람시간이 필요하다. 같은PR의 전후 runtime 수치나 선택창 elapsed를 대조 시간으로 쓰면 안 된다.

## 검토의 성격과 남은 취약점

이 문서와 원장은 같은 AI 조사자의 자체 재판독이다. root의 통합 점검도 AI 팀 내부 교차검토이며 외부 인간 독립 판독으로 부르지 않는다. 선택 시 #51116의 두번째 reviewer URL문장이 우발 노출된 점, 추가층 자격규칙 R01 정정, 최초head 미확인은 선정 원격 SHA와 REVISIONS.md에 보존된다. 결론을 지지하는 사례만 남기지 않았고 실패·무링크·설계유지·이미착수 사건을 모두 유지했다.

