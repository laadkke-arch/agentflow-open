# ROR 조사 묶음

## 핵심 인계

고정 저장소 판은 `ror-community/ror-updates@baffbf2b52cf09acd3dc29ef808d91c4a1aca278`이다. 이 SHA 아래 `rc-v1.*`, `rc-v2.16` 파일은 **공식 배포 준비 변경파일**이다. 사건 댓글이 해당 release에 반영되었다고 명시한 경우 그 발행자 진술을 추가했다. 전체 배포 dump나 현재 ROR API를 직접 확인한 것으로 쓰지 않는다.

`sources.json` 41행 중 보수적으로 최소 원문 수에 산입한 것은 15행이다(사건 대표 원문 8, 정책 2, 하위 소비자 5). 나머지 26행도 직접 열었지만 같은 사건의 전후파일·연결요청이므로 독립된 사건/저작처럼 추가 산입하지 않았다. 외부 자료가 41개라는 것은 41개의 독립적인 정답 출처라는 뜻이 아니다. 별도 `supplement-sources.json` 및 `SUPPLEMENT_REAL_MERGER.md`는 추가 보강이며 본 8사건과 합산하지 않는다.

| 사건 | 본표 추천 | 실제 관측 | 주요 범위 제한 |
|---|---|---|---|
| ROR01 COMTES | core | duplicate withdrawn + 한 successor; 원 회사는 옛 ID를 여전히 인용 | 법적 회사 합병 아님, live redirect 미확인 |
| ROR02 PTSD 본부/지부 | core | 연구 산출물의 지부 소속 근거 때문에 병합 제안 기각 | entity 전후 dump 없음; 요청에 인용된 논문 원문 미열람 |
| ROR03 Hamilton | supplement | 복구된 withdrawn record의 중복 GRID 제거, 다른 successor 잔존 | 원 삭제/복구 편집판 미확보; literal unmerge로 세지 않음 |
| ROR04 LLUR | supplement | inactive + 두 successor 및 상호 predecessor | before dump와 법령/기관 원문 미확보 |
| ROR05 ZFH | core | active/two child → inactive/four successor; EQAR도 역사 ID·후계 시점 보존 | 네 후계 중 특정 기능의 담당 기관은 선택 불가 |
| ROR06 Cuauhtémoc | core | 본교 ID를 지부로 덮어쓴 뒤 본교 복구·새 지부 ID | literal ID merge가 아닌 wrong-target update 정정 |
| ROR07 Biofisica/Biofisika | core | 이름·웹·부모는 복구했으나 v1.60 파일에 Spain/Leioa 위치 잔존 | 현재 상태·실제 소비자 피해 미확인 |
| ROR08 Gazipur/Netrokona | core | 다른 대학 ID에 적용한 이름변경을 취소하고 각각 올바른 ID로 갱신 | literal merge 아님; 별개 기관의 이름변경과 ID 정정 구별 |

기계적으로 `CORRECTED_IDENTITY`를 `CORRECTED_MERGE`로 바꾸지 말아야 한다. ROR06–08은 원문이 오류라고 판정한 실제 수정/복구 사건이지만, 두 ROR 레코드를 merge 명령으로 합친 뒤 되돌린 사건이 아니다. 본 작업의 “오병합·분리·정정”을 좁게 해석하여 literal merge만 허용한다면 이 셋은 정정군의 충분한 표본이라는 조건을 만족하지 않는다. 그 한계는 acceptance에서 숨기지 않아야 한다.

## 결과를 바꾸는 관측

복원 열의 `auto`는 **고정 구조화 파일에 이미 보존된 값을 해석 없이 추출할 수 있다는 연구자의 판정**이다. 실제 시스템 또는 소비자의 자동복원 실행을 관측했다는 뜻이 아니다. `manual`은 판/문맥 대조가 필요함, `unverified`는 필요한 원문 또는 실행 증거가 없음이다. 모든 사건의 `automatic_restoration_execution_verified`는 false로 둔다. 본표에서 실행 성공을 요구하는 조건에는 `auto`를 실행 완료로 집계하지 않는다.

정규화된 issue-comment 도구가 시간을 비워 반환한 항목은 별도 공개 GitHub comment 원문을 다시 열어 `created_at`/`updated_at`을 확인했다. 14개 댓글의 시각을 관련 source의 `comment_metadata`에 추가했다. PTSD 기각 판단은 2024-11-05T18:34:53Z이고 issue 종료는 2024-12-02로 서로 다르다.

1. ROR07은 “되돌림 완료” 댓글을 정답으로만 쓰면 놓치는 반례다. [v1.60 변경파일](https://github.com/ror-community/ror-updates/blob/baffbf2b52cf09acd3dc29ef808d91c4a1aca278/rc-v1.60/updates/041xzk838.json)의 이름·URL·CNR 부모와 locations를 독립적으로 읽어야 한다. Spain/Leioa 잔존은 역사 파일의 직접 관측이고 현재 ROR에도 남아 있다는 주장은 아니다.
2. ROR01의 [회사 공식 Contacts](https://www.comtesfht.com/contacts)는 withdrawn ID를 인용한다. 회사라는 목적상 대상이 같고 단일 successor가 있는 경우 역사관계가 짧게 충분할 수 있다. 현재 클릭 결과나 이용자 피해는 관측하지 않았다.
3. ROR05의 [EQAR](https://www.eqar.eu/qa-results/search/by-institution/institution/?id=205)는 옛 ROR와 2023 종료·네 후계를 함께 보존한다. 과거 QA 보고서의 기관은 비활성화했다고 오답이 되지 않는다.
4. ROR06의 같은 ROR URL은 SLP 지부판과 복구된 Puebla 본교판을 가리켰다. 당시 판이 없으면 과거 추천 이유의 캠퍼스가 바뀔 수 있다.
5. ROR08은 “모든 이름변경은 새 ID”도 틀림을 보여준다. 두 기관의 ID 혼동은 정정해야 하지만, 실제 Netrokona ID 안의 Sheikh Hasina라는 과거명은 alias로 유지한다.

## 하위 소비자 분모

직접 열린 5건은 COMTES Contacts, EQAR, CoLab, OpenAlex, science.eus다. 앞의 둘은 단순 기업 식별과 역사 기관 인용이라는 서로 다른 목적을 드러낸다. 뒤의 셋은 같은 ROR041xzk838을 쓰는 소비자 메타데이터의 서로 다른 해석을 드러낸다. **5/5의 최초 ID 삽입일과 소비자 정정일은 미확인**이다. 5건 모두 “실제 이용자 오추천 발생”의 증거로 세지 않는다.

CoLab/OpenAlex는 독립 운영자지만 같은 원천 ROR/GRID 자료를 수입했을 수 있다. 이들의 불일치는 독립적인 기관 정답 투표가 아니다. science.eus는 Zenodo 원자료를 새로 검증한 것으로 세지 않는다.

## 접근과 조회 순서

조사자는 issue 본문·토론·고정 JSON·정정 원문을 읽은 뒤 이 묶음을 작성했다. 따라서 이 조사자의 후속 복원 답은 눈가림 실험이 될 수 없다. parent가 별도 보기/정답키를 만들 때 이 열람 사실을 보존하고 같은 모델/연구자의 비교는 자기점검으로 보고해야 한다.

접근 실패와 관계 미보존은 다르다. `ror.org`/API 및 몇몇 기관 원문의 조회 실패는 “원문 접근 불가”이고, v1.60의 Spain/Leioa 잔존은 “직접 읽은 변경파일의 정합성 불완전”이다. 현재 HTTP 200/404를 측정했다고 선언하지 않았다.

## 네 관점 및 분야 전이

- 카탈로그 편집자: 중복 COMTES는 합칠 수 있지만 PTSD 지부의 연구출판 소속은 유지할 가치가 있다고 판단했다. 이름/웹사이트 일치만으로 두 경우를 통일할 수 없다.
- 원 ID 발급자: ROR 정책은 영속 ID와 역사적 상태/관계를 제공한다. 단일 successor가 항상 같은 법인이라는 보장이나 여러 successor 중 자동 선택 보장은 아니다. GRID/ISNI 원 발급자의 원판을 이번에 전부 읽지는 못했다.
- 옛 인용 독자: EQAR의 과거 보고서나 논문 소속은 당시 비활성 기관을 계속 인용하는 것이 맞을 수 있다. 현재 기관에 모두 옮기는 것 자체가 오류를 만들 수 있다.
- 특정 판에 추천 이유를 붙인 개발자: ROR07의 속성별 복구 결과와 ROR06의 캠퍼스 변경을 구분하려면 URL 외에 당시 판, 대상 단위, 근거 절이 필요하다. 후계/정정 이력도 실제 소비자의 오래된 인용을 자동 재분류하지 않는다.

음악의 work/recording/release와 비교할 때, 조직의 parent/child는 동일 작품의 구현판 관계가 아니다. PTSD 지부·Cuauhtémoc 캠퍼스의 연구소속 식별은 모조직에 흡수해도 되는 단순 label 차이와 다르다. 소프트웨어의 이름 alias와 비교할 때, COMTES 중복과 Netrokona 과거명은 같은 대상의 이름을 모을 수 있는 반면, ZFH의 네 후계는 같은 기능의 버전들이 아니므로 단일 최신판 규칙을 옮길 수 없다. 이것은 연구자의 교차 분야 해석이며 다른 분야의 원문 사건과 parent가 대조해야 한다.

## 다음 최소 확인

- ROR07: 전체 v1.37 dump의041xzk838 및 최신 전체 dump에서 names/locations/relationships를 대조하고 Spanish기관의 독립 정답 ROR를 확인한다.
- ROR06·08: 오류 노출 기간에 작성된 논문/소속 파일의 고정판과 실제 소비자 수정 commit을 찾는다.
- ROR05: 네 후계별 교육·연구기능 이관표를 찾아 역사기관 보존과 현재기능 추천을 별도 채점한다.
- ROR02·04: before dump를 확보하고 요청에서 인용한 논문/법령을 직접 열어 발행자 판단을 외부 근거와 대조한다.

