# AF-RES-053 단계 ① 방법 검토 — 동일 모델 보조 검토

검토 시점: 2026-11-23T01:43:05Z 이후. 기준판은 단계 ① 원격 봉인 SHA `a6b1624c899eacf118c0e01350f52cbd53e21dae`다. 이 문서는 그 판의 `SCOPE.md`, `operations.json`, `frame.csv`, `streams/vega/selection.md`, `streams/libass/selection.md`만 검토한다. 기준판 이후 카드·예측·후속 결과의 적절성을 확인한 문서가 아니다.

검토자는 도너 원전 수집을 맡았던 `/root/donor_sources`다. root와 같은 모델의 별도 작업자이며, 독립된 사람 평가나 다른 모델 검증이 아니다. 앞서 인쇄·지도 원전을 읽었고 그 개괄을 root에 전달한 이력이 있다. 이번 검토에서는 수신 이슈의 원문·댓글·PR·릴리스·시험·출력에 접근하지 않았다. 수신 요구는 위 선정 메모와 조작 정의의 요약으로만 알게 됐다. 따라서 선정 메모가 원문을 정확히 옮겼는지 독립 재검증하지 않았으며, 아래 내용은 **봉인 문서 사이의 일관성과 향후 과대계수 위험에 대한 검토 의견**이다.

초기 본문 미복원, L03 미충원, L02의 연구자 정상 대조, 도너 개괄 사전 노출은 이미 기록되어 있다. 이를 새로운 발견으로 다시 세지 않는다. 신규 검토 항목은 아래 다섯 개다. 후보 교체나 유리한 해결책 추가를 권하지 않는다.

## MR1. L01·L02의 B는 아직 측정 가능한 단일 조작보다 목표를 만족하는 조작군에 가깝다

**직접 문서 근거.** [operations.json L63–71](https://github.com/laadkke-arch/agentflow-open/blob/a6b1624c899eacf118c0e01350f52cbd53e21dae/docs/workstreams/research/AF-RES-053/operations.json#L63-L71)의 L01 B는 실제 block 높이를 고려해 중앙 배치용 여백을 정하지만, block의 의미·좌표계·큰 띠의 판별 경계는 미고정이다. [L80–88](https://github.com/laadkke-arch/agentflow-open/blob/a6b1624c899eacf118c0e01350f52cbd53e21dae/docs/workstreams/research/AF-RES-053/operations.json#L80-L88)의 L02 B는 동일 글꼴 출력에서 필요한 높이를 측정한 다음 흰 줄이 노란 block 위에 놓일 만큼 MarginV를 늘린다. 이는 [SCOPE.md §2](https://github.com/laadkke-arch/agentflow-open/blob/a6b1624c899eacf118c0e01350f52cbd53e21dae/docs/workstreams/research/AF-RES-053/SCOPE.md#L28-L35)의 동일 조작 및 결과 전 예측 규칙과 맞추어야 한다.

**위험.** 후속 출력의 겹침이 사라질 때까지 MarginV를 조정하거나, 실제 중앙에 온 결과를 보고 block 높이의 정의를 고르면 B 성공은 사전 예측을 가르는 증거가 되지 않는다. 반대로 출력 측정 자체가 언제나 금지인 것은 아니다. 결과를 보기 전에 정한 측정 절차와 식을 그대로 적용한다면 재현 가능한 조작이 된다. 현재 봉인은 그 둘을 아직 구별하지 못한다.

**최소 조치·엄격 감도.** 단계 ② 전에 API 근거가 허용하는 범위에서 측정 대상(예: layout box인지 ink box인지), 좌표 기준, 여백 산출 규칙, 측정 시점과 실패 조건을 고정한다. 숫자를 뒷받침할 자료가 없으면 수치를 만들어 넣지 말고 `B는 조건부 정책 후보; 실제 MarginV 미고정`으로 표시한다. 후속 자료가 임의로 조정한 값 한 개만 제시하면 그 결과는 원래 B와의 동일성이 미확인이다. **출력을 본 뒤 정한 여백만 존재하는 행을 제외한 분모**를 엄격 감도로 보고한다. 기존 A/B 문구를 구체화하면 그 시점의 읽은 문서와 변경 전후를 SCOPE에 추가하고 원 봉인 문구를 보존한다.

## MR2. 정상·경계라는 이름 아래 입력 쌍과 한 화면 내부의 부분집합이 섞여 있다

**직접 문서 근거.** [operations.json L46–54](https://github.com/laadkke-arch/agentflow-open/blob/a6b1624c899eacf118c0e01350f52cbd53e21dae/docs/workstreams/research/AF-RES-053/operations.json#L46-L54)는 V03의 정상 9개 record와 경계 zero record를 원문 10개 record의 부분집합으로 정의한다. V01·V02는 각각 외부 정상 예제와 변경 입력을 가리킨다([L12–20](https://github.com/laadkke-arch/agentflow-open/blob/a6b1624c899eacf118c0e01350f52cbd53e21dae/docs/workstreams/research/AF-RES-053/operations.json#L12-L20), [L29–37](https://github.com/laadkke-arch/agentflow-open/blob/a6b1624c899eacf118c0e01350f52cbd53e21dae/docs/workstreams/research/AF-RES-053/operations.json#L29-L37)). [Vega 선정 메모의 앞선 제외 표](https://github.com/laadkke-arch/agentflow-open/blob/a6b1624c899eacf118c0e01350f52cbd53e21dae/docs/workstreams/research/AF-RES-053/streams/vega/selection.md)는 여러 앞선 후보를 정상 비교입력 또는 입력 쌍 부재로 제외한다.

**위험.** V03에서 1 red/9 black을 판독하는 것은 유효한 범주 관측이지만, 그것을 독립적인 정상 입력 실행과 경계 입력 실행 두 번으로 세면 실측 분모가 늘어난다. 모집 규칙이 별개의 두 입력을 요구했는지, 한 입력의 구별 가능한 두 부분도 허용했는지 분명하지 않으면 앞선 제외 사례와 기준이 같다고 단정할 수도 없다. 이 검토만으로 앞선 후보가 실제 적격이었다고 판단하지는 않는다.

**최소 조치·엄격 감도.** 각 요구에 `관측 단위`를 붙여 V03은 `한 출력의 두 record 집합`, V01·V02는 `서로 다른 명시 입력 조건`, L01은 `띠 조건`, L02는 이미 기록된 연구자 대조로 구분한다. V03의 1 red와 9 black은 한 출력에서 함께 만족해야 하는 두 속성이다. 원문이 두 독립 입력을 준 사례만 남기는 엄격 감도에서는 V03을 제외하되, 다른 후보로 대체하지 않는다. 부분집합도 적격이라는 해석을 유지할 때는 앞선 제외 판단에 같은 정의를 적용했는지 확인할 최소 자료가 부족하다는 점을 남긴다. 이 해석을 사후 확장해 완전 충족으로 고쳐 쓰지 않는다.

## MR3. 첫 적격 절 규칙은 있으나 사례별 탐색의 결정 규칙은 봉인판에서 아직 재현되지 않는다

**직접 문서 근거.** [SCOPE.md L22–25](https://github.com/laadkke-arch/agentflow-open/blob/a6b1624c899eacf118c0e01350f52cbd53e21dae/docs/workstreams/research/AF-RES-053/SCOPE.md#L22-L25)는 원전군과 대략적 순서를 정하고 I의 `대응 단어`, D의 `제목/색인 용어`로 첫 적격 절을 택하도록 한다. 그러나 이 다섯 요구 각각에 대응할 정확한 검색어 순서, 파일·절의 동률 순서, 부적격 판정 요건은 이 봉인 파일들에 없다. 단어 수 상한의 동일성과 실제 길이 차이는 이미 구별했으므로 이 항목은 그 알려진 예산 차이를 다시 지적하는 것이 아니다.

**위험.** 서로 다른 제목 단어를 택하면 먼저 도달하는 I/D 절이 달라질 수 있다. 내용을 읽고 유리한 검색어·적격 의미를 정해도 `첫 적격`이라고 표현할 여지가 남는다. 원전 개수와 창 길이를 맞추는 것만으로 이 선택 재량은 제거되지 않는다.

**최소 조치·엄격 감도.** 실제 탐색 순서를 변경 없이 남긴다. 사례별 검색어·허용 원전 목록·정렬 규칙·각 후보의 탈락 이유·첫 본문 열람 시각·잘라 낸 시작/끝 위치가 필요하다. 이미 읽은 절에 대해 나중에 만든 순서를 최초의 사전 탐색 순서라고 쓰지 않는다. 아직 보지 않은 후보의 순서는 지금 고정할 수 있지만 그 시점과 이미 본 원전은 함께 기록한다. **사례별 순서가 내용 열람 전에 고정된 비교와, 읽은 뒤 적격성을 정리한 비교를 나눈 감도**가 적절하다. 후자의 새 정답은 특정 원전 창의 판별력 사례로 보고할 수 있으나, 동일 탐색 정책의 효과라고 확대하지 않는다. 이는 현재 시점 보충이 필요한 절차 구체화이며 후보 교체 사유가 아니다.

## MR4. 동시대 API에서 가능한 조작과 작성자가 실제 사용한 판의 동작을 별도 명제로 유지해야 한다

**직접 문서 근거.** `frame.csv`의 V01·V03은 schema major만, V02·L01은 실제 제품판 미명시, L02는 VLC 3.0.18만 기록한다. 해당 [frame 고정판](https://github.com/laadkke-arch/agentflow-open/blob/a6b1624c899eacf118c0e01350f52cbd53e21dae/docs/workstreams/research/AF-RES-053/frame.csv)에서 선정 행은 CSV 논리 행 5·11·13·46·52다. [operations.json](https://github.com/laadkke-arch/agentflow-open/blob/a6b1624c899eacf118c0e01350f52cbd53e21dae/docs/workstreams/research/AF-RES-053/operations.json)의 각 limits도 이를 명시하며, [SCOPE.md L32](https://github.com/laadkke-arch/agentflow-open/blob/a6b1624c899eacf118c0e01350f52cbd53e21dae/docs/workstreams/research/AF-RES-053/SCOPE.md#L32)는 판 일치를 요구한다.

**위험.** 이슈보다 앞선 배포 태그에서 API가 존재함을 확인해도 작성자 실행 엔진이 그 태그였다는 사실은 따라오지 않는다. schema URL이나 호스트 플레이어 버전을 renderer patch와 같다고 간주하면, Q2의 가용성 확인을 Q6의 같은 판 출력 확인으로 승격하게 된다. 이는 초기 본문 수정 이력의 복원 여부와 별개인 연결 고리다.

**최소 조치·엄격 감도.** `동시대 가용성 확인판`, `원 요청의 실제 실행판`, `후속 출력의 실행판`을 별도 열로 보존한다. A/B가 당시 어느 판에서 선택 가능했다는 결론은 낼 수 있지만, 원 요청 또는 후속 출력의 실행판이 미상이라면 `같은 판·입력·조작 실측` 분모에는 넣지 않는다. 엄격 감도는 **세 판의 필요한 대응이 입증된 행만** 남긴다. 원 요청판을 추측한 뒤 그 판으로 예측을 맞추는 사후 변경은 허용하지 않는다.

## MR5. 이미 본문에서 알려진 실패가 후속 검증이나 D의 새 판단으로 중복 계산될 수 있다

**직접 문서 근거.** [operations.json L21](https://github.com/laadkke-arch/agentflow-open/blob/a6b1624c899eacf118c0e01350f52cbd53e21dae/docs/workstreams/research/AF-RES-053/operations.json#L21)의 V01은 nested 입력 실패, [L38](https://github.com/laadkke-arch/agentflow-open/blob/a6b1624c899eacf118c0e01350f52cbd53e21dae/docs/workstreams/research/AF-RES-053/operations.json#L38)의 V02는 escaped 접근 성공과 title 누출, [L55](https://github.com/laadkke-arch/agentflow-open/blob/a6b1624c899eacf118c0e01350f52cbd53e21dae/docs/workstreams/research/AF-RES-053/operations.json#L55)의 V03은 B가 검정을 남김, [L89](https://github.com/laadkke-arch/agentflow-open/blob/a6b1624c899eacf118c0e01350f52cbd53e21dae/docs/workstreams/research/AF-RES-053/operations.json#L89)의 L02는 A의 경계 실패를 이미 노출된 내용으로 적었다. libass 선정 메모도 이 경계 현상의 후속 검증 중복 계산을 금한다.

**위험.** 후속 댓글이 알려진 실패를 되풀이하거나 패치 필요성만 확인할 때, 그 사실은 아직 관측되지 않은 경쟁 조작의 정상·경계 결과를 증명하지 않는다. 다섯 범주 중 `A만` 또는 `B만`은 승리 조작의 성공과 상대 조작의 미달을 함께 필요로 한다. 한쪽 실패를 이미 알았던 행에 대해 D가 그 실패를 재진술했다는 이유만으로 `I가 못한 신규 정답`을 세면 원문 밖 사전 지식과 후속 근거가 섞인다.

**최소 조치·엄격 감도.** 각 예측을 `봉인 전 알려진 사실`, `N/I/D 문구에서 추론한 미관측 결과`, `후속 자료가 새로 가른 부분`으로 나누어 적는다. 경쟁 조작 미관측, 조건 불일치, 또는 동일 실패 재진술뿐이면 우열은 미확인이다. **이미 알려진 실패만 재확인한 후속 자료를 모두 제거한 후에도 D와 I의 서로 다른 사전 예측이 갈리는지**를 감도로 확인한다. 본문 노출을 숨기거나 표본을 교체할 필요는 없으며, 채점 단위를 더 엄격히 유지하면 된다.

## 유지할 장치와 적용 순서

고정 모집틀은 59개 논리 데이터 행, 그중 실제 후보 58개와 빈 자리 1개다. 선정 요구는 5개이며 계획상 자리는 6개다. 이 수치와 N/I/D 카드 예정 18행은 실측 출력 수나 독립 시행 수가 아니다. 검색 substring 누락을 별도 metadata census로 보충하고, exact-word 감도를 새 모집으로 부르지 않은 점은 일관적이다. `operations.json`이 보조자의 잠정 A/B보다 우선한다는 SCOPE 선언도 있으므로, 과거 제안 차이를 미기록 사후 교체라고 오인하지 않는다.

단계 ② 전에는 MR1의 측정 규칙과 MR3의 실제 검색 이력을 가능한 범위에서 구체화하고, 구체화하지 못한 항목은 조건부·미확인으로 봉인하는 편이 적절하다. MR2·MR4·MR5는 원 표본과 원 예측을 유지한 채 관측 단위와 엄격 채점 분모를 나누면 된다. 이후에 필요한 변경은 시점·변경 전후·당시 노출을 남긴다. 이 검토는 후속 결과가 틀렸다거나 D가 열등하다는 관측을 제공하지 않는다.

## 검토 입력 식별

모든 해시는 위 고정 Git 객체의 원본 bytes에 대한 SHA256이다. 외부 이슈를 새로 열지 않고 `git show <SHA>:<path>`로 읽었다.

| 고정판 안의 파일 | SHA256 |
| --- | --- |
| SCOPE.md | `3f311e6a9fb7a8610be5981e873262a24e22475fd9d087f926d79a6ebb6abd1a` |
| operations.json | `10299df3f62d648cf772c0ee14d7e77bd9aed02c80a3c68042b177a7d9ef9c4a` |
| frame.csv | `6420e963435130dbda8355c800d3fe16cfb5bd8e9b879ef232da1745de0d88eb` |
| streams/vega/selection.md | `af80da82fc4e5cfc52872793f269469f699db6461c06853940aba6c6e6bc41a6` |
| streams/libass/selection.md | `a212d84d12aefd6003a06523de637e4a7e434156c0cb4e10fcd413b885f43197` |
