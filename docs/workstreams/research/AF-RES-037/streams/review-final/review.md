# AF-RES-037 최종 독립 QA

## 현재 판정

주요 결론인 **고정 원안 기준 A 0/8·B 0/4**, 별도 **표준 포함·기존 코드 기준 B02 준수 사슬 1/4**는 표와 원장에서 구분돼 있다. B02 부분을 새 사건으로 더하지 않았으며, 회고·유추를 허용한 수를 엄격 완결 사슬로 바꾸지 않았다. 문헌 읽기 규모를 인과 donor 수로 바꾸지도 않았다.

필수 표1은 제목 바로 다음에 정확한12사건(A8/B4), 필수 표2는 바로 다음에5조건이다. 마지막 약점 표는 정확히3데이터행으로 끝난다. cards12개는 사건별1개이며 각 링크2개다. sources168행/고유 counted group49개, frame219행, chains12행, judgments25행을 재파싱했고 source ID 누락이나 counted group 중복은 발견하지 않았다.

## 제기한 문제와 해결 확인

| ID | 문제 | 최소 수정 | 결론 영향 |
| --- | --- | --- | --- |
| FQA-01 | judgments의 B02/B03/B04 `decision_authority`가 미확인으로 출력되지만 chains의 `object_authority_json.authority`에는 직접 확인한 권한 대응이 있다. 생성기가 `decision_actor`/`actor`만 읽는다. | rebuild.py의 권한 매핑에 `authority`를 추가하고 재생성한다. | 수치는 바뀌지 않지만 Q4 근거가 소실되는 오류를 복원한다. |
| FQA-02 | rebuild.py는 일반 사건의 `complete_chain=False`, 감도분모4, 출력 strict A/B0을 상수로 둔다. 현재 판정과 맞지만 RESULT의 플래그 기반 재집계라는 설명보다 약하다. | 사건 판정 코드·필수 접점에서 완결 여부를 도출하고, 실제 층별 사건에서 분모와 요약을 도출한다. | 예상 최종 수치는 그대로0/8·0/4·감도1/4. 독자가 값을 바꿔 재계산할 수 있게 한다. |
| FQA-03 | 표2 strict B의 명시 변경1은 B03의1998 발표문 진술이다. 이 초기 진술은 강한 근거지만, 변경 전0.1이나 최초 설계안은 복원되지 않았다. B02의 고정 RFC안 전후와 같은 접점으로 읽힐 수 있다. | 해당 셀을 `명시 변경 진술1; 고정 원안 전후 미확인`으로 한정하고 독립 접점의 뜻을 설명한다. 또는 relaxed의 변경 진술로만 센다. | 엄격 완결0은 유지된다. 변경 진술과 확인된 원안 변화의 혼합을 막는다. |

## B03 업데이트와 원문 범위

1998년1.0.1 소스의 ANNOUNCEMENT·fonts.doc·악보를 명명한 Feta 주석이 RESULT와 cards, chains에 반영돼 있다. 현대 Essay 회고만 남은 설명이 아니며, 날짜를 archive mtime 경계로 표시하고 최초 공개일·정확한 원전 판·0.1 글꼴을 미확인으로 보존했다. 초기 글꼴 교체를 현대 optical spacing이나 모든 크기 조정과 한 사건으로 합치지 않았다. MPA1993/MOLA2017은 실제 본보기 원문 대신 세지 않았다.

CSS-C04는 선행 Servo 구현과2020 명세 반영을 구분하고, CSS-C03는 명세 이름 변경만 확인했다고 적었다. B02는 EPSG4xxx/GEOGCS 조건과 override, 실제 시험13569와 구현13570을 구분했다. GML 규범이 없었다는 잠정 반론은 ROOT-P10을 통해 정정됐으며, 표준 기여자라는 사실을 저자 첫 인지나 새 학습으로 확대하지 않았다. URL·시점의 중요한 범위 표기는 원장과 일치했다.

## 검토 범위

RESULT, cards, case-decisions, sources, frame, chains, judgments, recount, rebuild를 읽고 서로 대조했다. 새 표집·원문 연구·외부 실행은 하지 않았다. SELF_CHECK와 acceptance는 이 스냅샷에 없어서 아직 검토하지 않았으며, 최종 파일이 제공되면 같은 두 review 파일만 갱신한다. 다른 산출물이나 Git을 변경하지 않았다.

## 수정 재검증

세 문제 모두 수정됐다. authority fallback이 B02/B03/B04의 권한을 보존하고, 완결 사슬은 독립 접점 플래그에서 도출되며 분모·표시 요약도 실제 행에서 계산한다. RESULT 표2의 B03는 `1 진술 (B03; 고정 원안 전후 미확인)`으로 한정됐고, 바로 뒤 설명과 judgments의 별도 동일 기준선 필드가 그 뜻을 고정한다. `python -B docs/workstreams/research/AF-RES-037/evidence/rebuild.py --check`를 읽기 전용으로 실행해 종료0, sources168/고유49/사건12/strict A0 B0/감도1/4를 재확인했다. Q6④의 추가9개 기록은 고유 저작을 늘리지 않았다. 내용 검토의 열린 발견은0이며 SELF_CHECK/acceptance 최종 검토만 남았다.

## SELF_CHECK·수용 파일 최종 검토

SELF_CHECK와 acceptance-evidence.json을 추가로 읽었다. Q1–Q7마다 판단, 직접 근거, 반대 근거, 미확인이 있고, JSON의 source evidence/counterevidence 참조140개는 source ID·sources.jsonl 행·원 주소·locator와 모두 일치했다. 파일 위치와 marker도 모두 맞고 acceptance에 저장한9개 산출물 해시는 실제 파일과 일치했다. CSV 독립 파싱 영수증의 파일 해시도 새 원장에 맞는다.

24조건 가운데 미충족은 정확히 AC03(완전 비노출7/8), AC05(B 원 발행자 수신본3/4), AC06(핵심 제공 원전1/4), AC18(원리 자체 독립 발명0/1), AC19(확정 타 분야 채택의 공급자 제약에 따른 반영 전 포기0/1)다. 각 부족 이유가 원장과 일치하며, 고유1차 저작49개라는 총량으로 이 다섯 공백을 충족 처리하지 않았다. Q6 탐색4/4와 엄격 반례 확정 실패도 분리했다. strict 양성0을 실패 조건으로 만들거나 미확인을 실제 부재로 바꾸지 않았다.

커밋 뒤 RESULT/acceptance 고정 SHA 재독, session check --fetch, HANDOFF 마지막 별도 커밋은 정확히 pending으로 기록돼 있다. 이 검토가 그것을 실행했다는 뜻은 아니다. root가 작성 중인 validate.py는 검토 말미에 존재했지만 validation.json 실행 영수증은 아직 없었다. SELF_CHECK의 실제 수행 목록에 들어간 검증이므로, root는 예정대로 실행하고 영수증을 생성한 뒤 커밋해야 한다. 이 실행 조건 외에 추가 내용 수정이나 새 연구 요구는 없다.

**최종 내용 검토와 reviewer 수정은 종료했다.** 기존 발견3개는 모두 해결됐고 열린 내용상 발견은0이다. review-final의 이 두 파일 외에는 쓰지 않았으며 Git도 변경하지 않았다.
