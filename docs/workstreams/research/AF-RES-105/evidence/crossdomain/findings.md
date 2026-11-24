# Q7 다른 분야 대조 — Calc와 Audacity

검토자: `/root/contract_prior_audit`. 단계② 원격 봉인 `4a4aae107be25f71318dbb0c7b7cfa73506c5030` 뒤에 연 자료다. 이 비교는 시간순·진술 모집의 사건이나 사용자 인지/채택 분자에 더하지 않는다. 직접 취득·판독한 기록 22개 중 필수 하한에는 **서로 다른 저작 4개**만 보수적으로 산입한다. 같은 매뉴얼의 다른 페이지, 같은 버그의 이미지, 탐색용 트리, 관련 없는 시험은 따로 남겼다.

## 1. 이름이 같아도 적용 범위가 다른 경우

| 대조 | 직접 확인한 입력·조작·출력 | 이름만으로 묶을 때 생기는 오류 | 정확한 절과 근거 | 한계 |
|---|---|---|---|---|
| Calc의 같은 ‘절대 참조’: 수식 복사와 참조 대상의 이동 | 24.2 설명은 복사 때 `$` 축을 유지하지만 참조 대상이 이동하면 상대·절대 참조 모두 갱신한다고 구분한다. 독립 상류 시험에서 A1=2, C3=`=A1`, C4=`=$A$1`에 맨 앞 두 행을 삽입하면 C5=`=A3`, C6=`=$A$3`가 된다. | ‘절대’라는 이름을 주소가 어떤 편집에서도 변하지 않는다는 의미로 확대하면 틀린다. | [공식 설명 L51–66](https://github.com/LibreOffice/help/blob/6409921048d4098f63109eeca0f0d2a4d7d7c8ae/source/text/scalc/guide/relativ_absolut_ref.xhp#L51-L66), 특히 `When to Use Relative and Absolute References`; [상류 시험 L1508–1606](https://github.com/LibreOffice/core/blob/da48488a73ddd66ea24cf16bbc4f7b9c08e9bea1/sc/qa/unit/ucalc_formula.cxx#L1508-L1606). | 이 연구에서 LibreOffice를 실행한 결과가 아니다. 상류 시험의 입력과 예상 단언을 직접 읽었다. 복사 동작은 이 시험 구간이 아니라 매뉴얼 근거다. |
| Audacity의 같은 ‘음량’: 클립의 시간별 envelope, 트랙 Gain, 선택 구간 Amplify | 3.6.4 설명에서 트랙 Gain은 그 트랙의 모든 클립에 작용한다. `SetEnvelope` 구현은 지정 시각을 포함하는 클립의 envelope에 점을 추가한다. Amplify는 선택한 샘플에 적용된다. | 한 클립의 일부를 바꾸려는 목적에 전체 트랙 Gain을 주면 다른 클립도 변한다. 세 기능을 같은 제품/음량 기능이라고 전부 제외하거나 전부 새 조작으로 세면 범위 차이가 사라진다. | [Audio Clips L39–49](https://github.com/audacity/audacity-manual/blob/991d4bc7a2be98840ca0e91c6e8c12a5763ea3b0/manual/man/audacity_tracks_and_clips.html#L39-L49), [SetEnvelope L72–102](https://github.com/audacity/audacity/blob/b17f97803c8cb7e1dcd3bbea1225c9b226bfd91c/src/commands/SetEnvelopeCommand.cpp#L72-L102), [Amplify L37–63](https://github.com/audacity/audacity-manual/blob/991d4bc7a2be98840ca0e91c6e8c12a5763ea3b0/manual/man/amplify.html#L37-L63). | 클립별 envelope와 최근 버전의 별도 clip-gain UI를 혼동하지 않았다. 여기서 고정한 UI/구현은 3.6.4다. |

## 2. 이름·UI가 달라도 효과가 겹치는 경우와 그 경계

| 대조 | 같은 입력에서 겹치는 효과 | 동등하다고 해서는 안 되는 부분 | 원자료 |
|---|---|---|---|
| Calc 상대·절대 수식 | B2=1, B3=2, C2=3, C3=4에 상대 SUM과 절대 SUM의 시험 예상값은 모두 10이다. B1:B2만 밀어 데이터 범위 일부가 달라지면 모두 7, 되돌리면 모두 10이다. | 같은 현재 값은 다음 복사에서 같은 참조를 보장하지 않는다. 두 방식 모두 참조 대상을 삭제하면 NoRef가 된다. | [상류 시험 L1613–1710](https://github.com/LibreOffice/core/blob/da48488a73ddd66ea24cf16bbc4f7b9c08e9bea1/sc/qa/unit/ucalc_formula.cxx#L1613-L1710). 여러 입력은 한 시험 저작이지 독립 사용자 사건이 아니다. |
| Calc 직접 `$` 입력과 F4 전환 | 같은 수식 토큰과 커서 위치라면 F4 한 번으로 A1을 `$A$1`로 바꾸는 경로와 직접 그 토큰을 입력하는 경로가 겹친다. | F4 반복은 행만/열만 고정하는 중간 상태를 거친다. 키 이름을 아는 것과 어느 축을 고정했는지는 별개다. 이 경로 쌍을 실제 앱에서 실행하지 않았다. | [Absolute Addressing, L54–58](https://github.com/LibreOffice/help/blob/6409921048d4098f63109eeca0f0d2a4d7d7c8ae/source/text/scalc/guide/relativ_absolut_ref.xhp#L54-L58). |
| Audacity Gain의 슬라이더·키보드 대화상자 | 공식 설명은 슬라이더, 정밀 수치 입력, Shift+G를 같은 트랙 Gain에 접근하는 경로로 제시한다. | envelope나 Amplify로 바뀐 것은 아니다. 같은 값이라도 조작 대상이 다른 트랙이면 동등하지 않다. | [Gain and panning, L132–141](https://github.com/audacity/audacity-manual/blob/991d4bc7a2be98840ca0e91c6e8c12a5763ea3b0/manual/man/mixing.html#L132-L141). |
| Audacity 편집 가능한 envelope와 Mix and Render | 공식 설명은 단일 트랙의 envelope를 렌더한 뒤에도 같은 소리를 의도하며, 제어점은 제거된다고 구분한다. | 같은 청각 결과가 같은 편집 상태를 뜻하지 않는다. 다른 트랙까지 선택하면 혼합 입력도 달라진다. 실제 오디오 수치 비교는 미실시다. | [Rendering envelope changes, L117–119](https://github.com/audacity/audacity-manual/blob/991d4bc7a2be98840ca0e91c6e8c12a5763ea3b0/manual/man/envelope_tool.html#L117-L119). |
| Audacity 일정 Gain과 Amplify | Amplify의 3.6.4 구현은 입력 샘플에 `mRatio`를 곱한다. 같은 샘플·같은 상수·다른 처리 없음이라는 제한 아래 선형 진폭 결과의 겹침을 추론할 수 있다. | **추론이지 실행 결과가 아니다.** Gain은 실시간 효과 스택 뒤에 적용된다. Amplify로 샘플을 먼저 바꾸면 비선형 효과의 입력이 달라질 수 있고, 선택·클립 분할·시간 늘이기 렌더 여부도 다르다. | [Amplify ProcessBlock L151–159](https://github.com/audacity/audacity/blob/b17f97803c8cb7e1dcd3bbea1225c9b226bfd91c/src/effects/Amplify.cpp#L151-L159), [Mixing L136](https://github.com/audacity/audacity-manual/blob/991d4bc7a2be98840ca0e91c6e8c12a5763ea3b0/manual/man/mixing.html#L136), [Amplify L55–56](https://github.com/audacity/audacity-manual/blob/991d4bc7a2be98840ca0e91c6e8c12a5763ea3b0/manual/man/amplify.html#L55-L56). |

## 3. 첫 결론을 뒤집는 원 예제

### ‘조용하게 들리면 같은 결과’의 반례

[Audacity 원 예제 #2371](https://github.com/audacity/audacity/issues/2371)는 3.1.3을 명시한다. 작성자는 30초 tone의 10–20초를 envelope로 거의 0처럼 보이게 한 뒤 +50 dB를 세 번 적용한 경로와, 같은 구간에 Ctrl+L을 추가해 무음으로 만든 경로를 비교했다. 직접 연 세 그림에서 첫 경로의 중간 구간은 다시 커지지만, 두 번째 경로는 10–20초가 평평하다. 음량이 작다는 목적과 이후 무음 탐지에 필요한 정확한 0은 다르다. 3.6.4의 [Control Points L78–84](https://github.com/audacity/audacity-manual/blob/991d4bc7a2be98840ca0e91c6e8c12a5763ea3b0/manual/man/envelope_tool.html#L78-L84)도 exponential envelope가 일반적으로 정확한 0에 도달하지 않음을 설명한다.

그림은 실행 순서나 잔여 진폭의 정확한 수치를 인증하지 않는다. 원 오디오·프로젝트 파일이 없으므로 여기서 수치 측정은 미확인이다. 이 2022 예제는 2018 Bugzilla 사례를 언급하지만 그 과거 사례를 별도로 읽은 것으로 세지 않는다. 세 그림도 한 사건이다.

### ‘나중에 효과를 붙여도 기존 곡선은 남는다’의 반례

[원 예제 #5099](https://github.com/audacity/audacity/issues/5099)의 작성자는 3.3.3 Windows에서 envelope를 둔 stereo clip에 Clip Fix를 적용하자 점들이 시작점으로 몰린다고 보고했다. 직접 본 전·후 그림은 기울어진 envelope와 여러 위치의 손잡이가 평평한 경계·왼쪽 손잡이로 바뀐 모습을 보여 준다. 3.6.4 매뉴얼의 같은 버그 경고는 이 이슈에 연결된다. 따라서 설명과 이슈는 이 버그의 독립 복제 두 건이 아니다. 이 예제는 추가 반례로 쓰되 필수 네 자료 수에는 추가하지 않았다. 현재 버전 재현이나 모든 효과의 같은 동작은 미확인이다.

## 4. 제품 반환에 옮길 규칙 — 새 지식 여부와 별도로 필요한 정확한 절

| 상황 | 작성자에게 줄 한 줄과 링크 | 작성자·답변자·문서 편집자의 관점 차이 | 판단을 바꿀 관측 |
|---|---|---|---|
| Calc에서 `$`를 이미 썼지만 목적 조작이 불명 | **“고정하려는 상황이 수식을 복사할 때인가요, 참조 셀에 행·열을 삽입할 때인가요?”** 확인 뒤 [When to Use Relative and Absolute References](https://github.com/LibreOffice/help/blob/6409921048d4098f63109eeca0f0d2a4d7d7c8ae/source/text/scalc/guide/relativ_absolut_ref.xhp#L62-L66)를 표시한다. | 작성자가 `$`를 아는 것은 유지한다. 답변자는 바꾸려는 축/작업을 특정해야 한다. 편집자는 F4 소개 대신 복사와 이동을 가르는 절을 고른다. | 이미 복사 방향·고정 축이 명시되면 질문을 생략하고 그 축의 절로 바로 보낸다. |
| Calc에서 같은 값이 나온다는 이유로 다른 참조 방식을 버리려 함 | **“현재 합계는 같아도 복사 뒤 참조는 달라집니다. 기존 수식을 표시하고 복사 규칙 절을 보세요.”** [Relative Addressing](https://github.com/LibreOffice/help/blob/6409921048d4098f63109eeca0f0d2a4d7d7c8ae/source/text/scalc/guide/relativ_absolut_ref.xhp#L51-L58). | 답변자가 같은 값을 재현해도 작성자가 원하는 후속 편집까지 확인한 것은 아니다. 문서 절은 결과값보다 작업 맥락을 분리한다. | 이후 복사/삽입을 전혀 하지 않는 일회 계산이면 이 차이의 실용 중요도가 낮아진다. |
| Audacity에서 한 클립의 구간만 바꾸려는데 Gain을 이미 앎 | **“기존 Gain 설정은 두고, 이 클립의 구간별 제어점을 확인하세요.”** [Control Points / Editing Control Points](https://github.com/audacity/audacity-manual/blob/991d4bc7a2be98840ca0e91c6e8c12a5763ea3b0/manual/man/envelope_tool.html#L78-L98). | 작성자의 기존 트랙 Gain 지식을 무시하지 않는다. 답변자가 바꾸는 것은 시간 범위·객체다. 편집자는 제품 홈이 아니라 해당 제어점 절을 지정한다. | 전체 트랙 모든 클립의 동일 증감이 목적이라면 Gain 절이 더 맞다. |
| Audacity에서 목표가 ‘무음’이라고만 적힘 | **“작게 들리면 되나요, 후속 처리에 필요한 정확한 0이어야 하나요?”** [Control Points의 0 제한](https://github.com/audacity/audacity-manual/blob/991d4bc7a2be98840ca0e91c6e8c12a5763ea3b0/manual/man/envelope_tool.html#L78-L84)과 [원 대조 예제](https://github.com/audacity/audacity/issues/2371)를 제시한다. | 새 기능을 배웠는지와 무관하게 관측 결과의 기준이 필요하다. 같은 파형 표시를 정확한 수치로 과해석하지 않는다. | 원 프로젝트의 해당 샘플이 실제로 모두 0인 측정이 생기면 envelope 경로의 그 결과는 따로 인정한다. |
| Audacity에서 현재 소리는 유지하고 다음 효과를 적용하려 함 | **“현재 곡선을 먼저 렌더할지, 계속 편집할지 정한 뒤 해당 절을 확인하세요.”** [Rendering envelope changes](https://github.com/audacity/audacity-manual/blob/991d4bc7a2be98840ca0e91c6e8c12a5763ea3b0/manual/man/envelope_tool.html#L117-L127). | 답변자는 새 도구 이름을 추가할 필요 없이 순서와 보존 상태를 바꿀 수 있다. 편집자는 버전 경고와 렌더 절을 같이 표시한다. | 지정 버전·효과·동일 프로젝트에서 제어점 유지가 확인되면 버그 회피를 이유로 한 선행 렌더 권고를 철회한다. |

## 5. 판·산입·재현 범위

- Calc 설명은 help commit `6409921048d4098f63109eeca0f0d2a4d7d7c8ae`, 독립 시험은 core commit `da48488a73ddd66ea24cf16bbc4f7b9c08e9bea1`이며 둘 다 `libreoffice-24.2.0.3`에서 확인했다.
- Audacity 설명은 manual tag `v3.6.4` → `991d4bc7a2be98840ca0e91c6e8c12a5763ea3b0`, 페이지 생성일 2024-09-03이다. 구현은 3.6.4 commit `b17f97803c8cb7e1dcd3bbea1225c9b226bfd91c`이다. 현재 사이트도 먼저 읽었지만 별도 버전/저작 수로 세지 않았다.
- 필수 산입은 Calc 설명 1 + Calc 원 시험 1 + Audacity 설명 1 + Audacity 원 예제 1 = **4**다. 22 취득 기록과 4 필수 저작을 혼동하지 않는다. 상세 제외 사유는 `sources-part.jsonl`과 `counting.json`에 있다.
- `original-examples.json`에 입력·예상/보고 출력·직접 본 이미지·입출력 SHA256을 보존했다. `acquisition.jsonl`은 실제 UTC·응답·바이트 SHA256을 남긴다. 숫자 측정/상류 시험 통과를 이 연구가 실행한 것으로 쓰지 않는다.
- 셸 조회·파싱 중 `bs4`가 없어 첫 HTML 본문 파싱이 종료값 1이었다. 표준 라이브러리 `html`/정규식으로 다시 읽어 성공했다. 이것은 출처 취득 실패가 아니며, 별도 자료로 산입하지 않는다.
