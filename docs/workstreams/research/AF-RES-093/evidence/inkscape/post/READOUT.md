# Inkscape Q5–Q6 · 사후 원자료 대조

사전 봉인: `3c50d0bd1d8f3659d86f8cf45fe233595c3d2592`. 이 디렉터리의 자료는 그 봉인 뒤에 열었다. 기존 모집·요청·후보·A/B 기록은 바꾸지 않았다.

## 엄격 채점 결과

| 사례 | 사전 A/B | 사후 원근거 | 엄격 정답·분모 | 사전 판정을 바꿀 최소 관측 |
|---|---|---|---|---|
| I1 #2225 | 분리 / 분리 | 원저자 WebM은 stamp 뒤 frame 변경이 여러 textbox에 영향을 주는 모습을 보여 준다. maintainer는 shape-inside 복사·재연결 차이를 설명하고 MR1275를 지목한다. | **미채점**. 같은 사용자1.0.2+r75+1·입력의 Duplicate 다음 resize 출력이 없다. 정확한tag1.0.2 code-path 설명에 한정하면 분리 advisory를 지지하지만 이를 두 GUI 결과의 독립 대조라 하지 않는다. | 같은 입력에서 stamp/Ctrl+D의 새 text ID·frame URI/ID·resize 전후 layout 쌍. |
| I2 #2231 | 유보 / 유보 | maintainer는 정확한1.0.2 e86c870879에서 문서에 없는 clipboard group ID를 연결하는 실패를 XML Editor로 재현했다. MR2570은 wrapper 안의 실제 child ID를 읽도록 수정한다. | **미채점**. 메뉴 후보의 같은 입력·다음 원본 편집 출력과 기존 target 보존 의도가 없다. | 기존 target ID 유지 필요 여부와 두 경로 targetID/linkeditem URI/원본 수정 후d의 대응쌍. |
| I3 #2283 | 유보 / 유보 | 저자가 clone 미삭제는 selection 제한의 정상 동작이라고 정정했다. crash 개선 주장도 저자와 maintainer 후속에서 재번복됐다. MR4079는 훗날 selection clear와 삭제 절차를 고친다. | **미채점**. 후보2 결원이고 후속판을 사용자1.0.2 대체쌍으로 채점하지 않는다. 이 행은 사전 description에서 사후 문장 노출도 있었다. | 같은 입력과 clone 유지 요구를 충족할 실제 후보2부터 확보; touched/selected/remaining IDs·crash·Undo 비교. |

신규 Inkscape strict 정답 자리: **0/3**. A의 채점 가능한 결정 분모0, B도0이므로 오병합률·불필요한 분리율·정확도는 **산출 불가**다. 유보는 A2/3, B2/3이고 사전 판단 변화는0/3이다. I3를 오염 민감도에서 제외해도 strict 정답은0/2다. 더 긴 기록의 바이트 증가만 관측했으며, 향상/악화를 추정하지 않는다.

## 후속 자료에서 실제로 바뀐 이해

- **I1:** ‘다른 객체에서는 stamp와 duplicate가 같을 것’이라는 maintainer의 첫 설명은 다음날 LPE 반례로 정정됐다. 같은 화면이 나오는 단순 입력에서 얻은 결론을 참조 shape·LPE로 일반화할 수 없다. 사전 A도 원문에서 독립 textbox 편집 요구를 알았기 때문에 B만의 성공이라고 볼 수 없다.
- **I2:** 버튼을 누른 뒤 Undo 항목이 생긴 것과 유효한 document object를 가리키는 링크가 생긴 것은 다르다. 2020-12-03 master의 수정일이 사용자1.0.2 release branch의 성공을 보증하지도 않는다.
- **I3:** 원문이 보고한 현상 중 clone 미삭제와 crash는 같은 원인이 아니었다. 사용자가 이미 선택한 originals를 남긴 채 eraser를 사용하면 hit된 clones가 selection에 없다는 조건이 중요했다. 뒤의 수정 주장만 읽었다면 실제 원저자의 반증을 놓쳤을 것이다.

후속 문장·MR·영상의 상세 출처는 followup_observations.jsonl과 sources.jsonl, Q6 네 유형은 COUNTEREXAMPLES.md 및 counterexamples.json, 실제 반환 링크와 한 질문은 CARDS.md에 있다.

## 자료·검사의 경계

추가로 직접 연 고유 원자료는 **11개**다: 세 이슈의 후속 thread3, MR1275/2570/4079의 본문+patch 각1로3, 원저자 WebM1, 공식 object-set-test1, SPUse 구현1, #2389 사건1, MR3180 본문+patch1. 여러 댓글·patch hunk·추출 frame으로 수를 늘리지 않았다. 기존 selection-chemistry.cpp를 다시 읽은 것은 산입0이다. 같은 사건의 영상/후속은 독립 사건 수를 늘리지 않는다. MR1275는 후보 duplicate 구현과 같은 저작 계보여서 독립 확인에서 제외한다. 나머지 독립성도 sources.jsonl에 publication과 runtime 검증을 나누어 표시했다.

GitLab REST notes API는 세 건 모두401이었다. 로그인이나 권한 확대 없이 공개 UI discussions.json에서 세 건 모두200으로 원문을 열었다. 실패 주소와 성공 재열람 주소를 함께 남겼다.

공식 testfiles/src/object-set-test.cpp의 assertions를 읽었으나 시험 바이너리나 GUI를 재실행하지 않았다. MR1275의 변경12파일, MR2570의 변경1파일, MR4079의 변경5파일에는 자동시험 파일 추가가 없었다. 이것은 기존 CI가 전혀 없거나 실행되지 않았다는 주장이 아니다. 원 시험을 직접 확인한 범위는 type·count·선택 type이며, pixel·exact ID·새 numeric edit의 짝 결과는 미확인이다.

원저자 영상의 원주소·SHA-256·18.798110초 길이·크기는 I1-video-access.json에 남겼다. fps=1/3 contact sheet를 시각적으로 읽었지만 각 이미지의 정확한 원 stream timestamp mapping을 별도로 저장하지 않았다. 따라서 이를 정량 frame-time 비교로 쓰지 않는다. 전체 영상·본문·patch 전문과 임시 contact sheet는 저장 산출물에서 제거했다.

## 다음 직접 확인 절차

실행을 맡는 후속 담당자는 먼저 `inkscape --version`을 기록하고 사용자 배포판1.0.2+r75+1 또는 그 차이를 확인한다. upstreamtag만 재빌드했으면 사용자 패키지 동일성은 계속 미확인으로 둔다.

1. I1: SVG2 자동흐름 textbox를 만든 뒤 동일 초기 SVG 사본 두 개에서 Space stamp와 Ctrl+D를 각각 수행한다. 첫 출력의 text/frame ID·href를 저장하고 같은 frame width 변경 뒤 다른 text의 layout을 비교한다. 원저자의 영상만으로 대조 입력 XML은 복원되지 않으므로 새 fixture는 연구자 재현으로 귀속한다.
2. I2: 기존 target ID를 유지할 필요를 먼저 확정한다. 두 경로에 같은 original shape를 주고 target ID/linkeditem URI와 original의d 변경 후 targetd를 보존한다. 새target을 만드는 메뉴와 기존target을 갱신하는 버튼이 같은 계약인지부터 확인한다.
3. I3: 후보2를 확보하기 전 두 대안 점수를 만들지 않는다. 현재 첫 후보의 selected-originals와 empty-selection을 나누고 clone hit 목록·남는 original/clone ID·crash·Undo를 기록한다. 최종 수정 MR의 다른 Cut/Clip 변화는 Delete 목표와 분리한다.
