# AF-RES-085 · 자가검산

| 질문·주장 | 원문 / 실행행 | 결론이 틀릴 사례를 찾은 경로와 발견 | 다음 최소 확인 |
| --- | --- | --- | --- |
| Q1 새 파트의 선택색과 목록이 원 요구였다. C4/E4 후속 편집은 연구 기준이다. | S06–S12, X1-U-1 probe 8·22, X4-U-1 probe 6·21과 04 화면 | 2019 PR 본문·댓글, 역사 데스크톱 도움말, 원 시험을 분리해 대조했다. Explode 원 시험의 두 이름은 본문에 행동이 없었고, 파트 파일 assertion은 새 선택 목록을 읽지 않는다. | 2019 보고에서 원문의 다음 UI 행동을 찾아 PR에 없는 기대가 있었는지 대조할 때만 추가한다. |
| Q2 같은 Tools 메뉴가 다른 함수에 진입한다. | S01–S05, X1-G-1 probe 13,14,19; X2-G-1 16,17,25; A-E05-L | 실제 붙임 경계와 마지막 범위 교체를 읽었다. E05는 source track과 대상 트랙, spanner 기본값, 원 트랙 제거, 마지막 RANGE 여부가 X1과 다르다. | 이미 차 있는 보표, 한 보표만 선택한 경우와 타이 분기에 clone/paste 횟수와 끝 staff를 추가로 읽는다. |
| Q3 숨김 중 child는 복제되며 L의 callback만 건너뛴다. | S05, X3-L-1 probe 10·16·18·19·34, X4-L-1 6·12·14·15, 숨김 화면 | 숨김 시 원 선택이 풀리는 경우와 raw Note child가 없는 경우를 각각 조사했다. 이 입력에서는 둘 다 0/6. 일반 보표에서 tag=2인 동일 child의 L callback 횟수가 0 대 1이다. tab 보표의 실제 복제 제외 분기는 소스에서 확인했다. | X3/X4를 tag=2 Symbol로 바꾸고 복제 전후·callback·피어를 8회 기록한다. |
| Q4 선택색과 다음 편집 대상을 동시 판독했다. | S08, S20–S23, 24개 next_edit_before/after, reselected_edit_after 및 reopen. verify.json 구간 색값 | 콤보 focus의 V 미도달이 예비 비교를 깨뜨렸다. 악보 클릭 없이 탭을 왕복해 같은 focus를 만든 뒤 실제 명령 진입을 읽었다. X3 G/L 화면 차이에도 V의 값은 동일했고 명시 클릭에서만 새 child를 편집했다. | 다른 입력에서 범위의 목록을 소비하는 명령과 단일 대상 소비자를 비교한다. |
| Q5 초기 차이, 메뉴 후 결과, 파일의 차이는 별개의 시점이다. | S03–S04, S08, S15–S18, S24, S41–S42. X1·X2 재선택, X3 L primary_saved 및 A-E06-G | X2에서 같은 XML 경로를 받는지, E06에서 mark 하나로 선택색이 나는지 확인했다. X3의 L은 저장 뒤 열린 창까지 색이 남았다. X1은 stderr rest 경고가 있었으나 native 파일의 겹침은 0/6. 4.0.2의 독립 신고에서는 겹친 rest가 관측됐다. | 별도 두 마디·타이 입력에서 복제·선택·길이 합·정상 command undo를 검사한다. |
| Q6 링크·선택·포커스·지속성은 작업마다 범위가 다르다. | S14·S19, S23·S25–S41, X3/X4 tabs 및 보조 API | Inkscape의 clone 손잡이 무변화와 Relink 실패, VS Code의 분할 강조 무변화, Blender와 Qt의 명시 공동 선택, GIMP의 XCF 저장, ProseMirror의 undo 복원을 직접 읽었다. 앱 간 상태 표현과 편집 경계가 다르다. | 실제 공동 선택을 원하는 파트 편집 작업을 특정하고 같은 모델에 원본/인스턴스 두 곳의 큰 선택을 부여하는 대조를 만든다. |
| Q7 X3의 화면 문제에는 G 링크를 건네고 다음 편집을 이유로 한 채택은 유보한다. | S09–S10, S16–S17, S33·S36. X3-G/L의 04-shown, next_edit_after, primary_saved, reopen | X4에서 L이 문제를 해결하고 X1에서는 차이가 너무 일찍 사라졌다. 범위 소비자나 판이 바뀌면 동등한 결과가 깨질 수 있다. 보고된 Paste 회귀는 다음 편집이 실제로 틀리는 설계 경계다. | 새 파트 한정인지 일반 복사도 재현되는지 한 번 확인한다. 후자이면 동일 입력 G/L 각각 두 회의 편집 ID를 수집한다. |

## 수치·파일 대응

- 동일 fixture SHA로 정식 GUI 24/24, 두 반복의 정규화 일치 12/12셀, U 기준 8/8세트. 비교 가능한 G/L 8/8짝에서 복제 직후 6/8 차이, 재표시·다음 키 경계 화면 2/8 차이, 실제 다음 편집 0/8 차이.
- 메뉴 직후 주 키의 문서 값 변경은 0/24. 별도 행위 -R에서 정확한 한 객체 변경과 undo 24/24. 주 키가 undo 항목을 만들지 않았으므로 명령 자체 undo를 주 키의 결과로 세지 않았다. 저장은 -R 전에 이루어졌고 양쪽 프로세스는 24/24 정상 종료했다.
- 정식 GUI에서 파일 해시, 기록된 시퀀스, 대상의 안정 키, peer 상호 참조, 다른 파트, 재열기, PNG 영역을 검산했다. X1 6회의 rest 경고를 원장에 남겼으며 같은 악보에서 최종 XML에 중복 rest는 없었다. X3/X4의 New All은 기존 Oboe를 보존하고 다른 Oboe 링크를 더했다.
- E05/E06 보조 API 6/6, 세 build smoke 3/3. 예비 GUI 37건 중 8건은 계획한 편집 경계에 이르지 못했다. 나머지 29건은 저장 순서가 다른 이전 절차였다. 기동 전 시도는 별도로 남겼다. [실행 원장](runs.jsonl) · [예비 기록](evidence/gui-attempts.jsonl) · [기동 자료](evidence/build/)
- 원독 42행에서 서로 겹치지 않는 독립 28개. 배정 9/5/4/4/6. 접근 실패와 선행 보고서 재사용은 분모에서 뺐다. 이 작업 참가자의 자기 검산이며 별도 연구자 재현은 0회다. [출처](sources.jsonl) · [실패·대체 경로](evidence/access-attempts.jsonl)

검산기는 ImageMagick으로 좌표 영역을 읽고, 원 노트·파트 구성과 XML을 Python으로 비교한다. 화면의 영역·픽셀과 모델의 object ID를 서로 연결한다. 출처 분모를 재계산하고 각 출처가 링크한 실행 파일을 확인한다. 외부 앱의 실측을 다시 실행하는 명령은 포함하지 않는다. [검산기](fixtures/verify.py) · [기록된 검산 결과](evidence/verify.json)

```bash
AF085_PACKET=docs/workstreams/research/AF-RES-085
python -B "$AF085_PACKET/fixtures/verify.py" --out /tmp/af085-verify-again.json
cmp /tmp/af085-verify-again.json "$AF085_PACKET/evidence/verify.json"
```
