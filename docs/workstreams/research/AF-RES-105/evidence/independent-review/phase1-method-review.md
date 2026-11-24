# 별도 판독 1차 — 분모·동일인·제안 지시 대상

검토자는 `/root/contract_prior_audit`라는 **별도 에이전트**다. 외부 인간 심사자나 맹검 판독자가 아니다. 이번 판독은 root의 제안된 결론을 알고 원 캐시를 다시 읽었다. QGIS 보조 2자리는 이 검토자가 앞서 직접 코딩했으므로 그 부분은 자기 재검토이며, 두 번째 독립 1차 코딩이라고 부르지 않는다. Blender 보조/후속과 root 통합 분모는 이번에 별도로 원문을 읽고 대조했다. 교차 분야 자료도 이 검토자가 작성했으므로 그 자료의 무결성 점검을 독립 내용 검증으로 내세우지 않는다.

검사 시점·입력 파일 SHA256·사건별 동일인/180일 재집계는 `phase1-denominators.json`에 있다. 원 질문 선택·사전·선정 제안은 바꾸지 않았다. RESULT/returns 최종 표와 공식 자료 최종 집계가 아직 생성 중인 시점의 1차 검토다.

## 확인된 분모

| 층 | 사건·후보 | 전체 제안 인지 판정 | 더 작은 변경 기능의 신규 인지 | 고정 제안 실행 |
|---|---|---|---|---|
| 시간순 | 서로 다른 질문8, 고정 제안 자리8. 타인 숫자ID가 확인된 제안7, QG-T1의 질문자ID 미확인1 | 판정 가능0, 미확인8 | 이 8건에서는 명시 판정0 | 같은 고정 제안의 작성자 실행 보고0, 실행 미확인8 |
| 진술 보조 | 서로 다른 질문4, 지시 대상 제안4, 시간순과 겹침0 | 판정 가능0, 미확인4 | BL-N1 Compare Direction과 QG-N1 GDAL with 지원의 새 인지2; 해당 단위 판정 가능2, 미확인2 | QG-K1 같은 0.5 치환의 실패 보고1. 나머지 실행 미확인3. 같은 제안 성공 보고0 |

BL-T1과 BL-T2의 작성자ID64184는 같다. 따라서 시간순8은 서로 다른 질문/에피소드8이며, 확인된 서로 다른 작성자ID는6개와 작성자 미확인 질문1개다. 보조4는 확인된 작성자ID4개이고 알려진 ID의 층간 겹침은 없다. 사건 수를 사람 수나 통계적 독립성으로 바꾸지 않는다.

SCOPE §2는 전체 제안의 명시 인지 또는 같은 전체 조작의 사전 수행 연결을 요구한다. 따라서 전체 제안 분모0과 더 좁은 기능의 명시 새 인지2를 동시에 보존하는 것이 맞다. **‘판정 가능0’만 적어 새 기능을 알았다는 두 진술까지 사라지게 하면 안 된다.** 반대로 기능명 수준의 두 진술을 전체 그래프/입력/판의 신규 인지로 확대해서도 안 된다.

위 표는 공개 증거의 보유 현황이다. ‘실행 보고0’을 ‘8명 모두 쓰지 않았다’로 바꿀 수 없다. 보조표본은 인지 문구로 모집했으므로 2/4 또는 2/2를 모집단 신규 인지율로 발표할 수 없다. 새 기능을 알았다는 두 사건의 실행은 둘 다 미확인이므로 ‘새로 배워 같은 조작을 실행’은 입증0이며 실제 발생0이라는 뜻이 아니다.

## 원문 지시 대상의 역추적

| 사건 | 직접 다시 읽은 원문과 위치 | 유지해야 할 판정 | 피해야 할 확대 |
|---|---|---|---|
| BL-T2 | [첫 댓글534953](https://blender.stackexchange.com/questions/309047#comment534953_309047), 뒤의 shmuel 댓글534959, [작성자534974](https://blender.stackexchange.com/questions/309047#comment534974_309047) | 고정 첫 제안은 curve/누적 weight 방법이다. 작성자의 작동 보고는 뒤의 power/remap 제안과 inverse-square-root 변형에 연결된다. | 첫 제안의 성공이나 신규 인지로 옮기지 않는다. |
| QG-T2 | [작성자773398](https://gis.stackexchange.com/questions/473591#comment773398_473595), [773404](https://gis.stackexchange.com/questions/473591#comment773404_473595) | points가 실제 레이어가 아니라 스타일의 generated geometry라는 정정이다. 지시 대상은 뒤의 답473595다. | 고정 repeating-label 댓글773390의 실패 실행으로 세지 않는다. |
| QG-T3 | [작성자773400](https://gis.stackexchange.com/questions/473594#comment773400_473601) | 링크 예제가 자기 상황을 잘 보여 준다는 말이다. | 해당 식을 실행해 중복 라벨이 사라졌다는 결과로 세지 않는다. |
| QG-T4 | [작성자773450](https://gis.stackexchange.com/questions/473611#comment773450_473611) | 감사·도움 평가만 관측했다. | VRT를 실행해 속도가 좋아졌다는 성과로 확대하지 않는다. |
| BL-K1 | [작성자539174](https://blender.stackexchange.com/questions/311094#comment539174_311115) | 두 번째 Align Euler를 이미 안다고 말했지만 Pivot를 확인하지 않았다고만 말한다. 변경 핵심 Pivot 값의 인지와 실행은 미확인이다. | ‘Pivot를 몰랐다’ 또는 ‘직접 적용했다’로 보정하지 않는다. |
| BL-N1 | [작성자543409](https://blender.stackexchange.com/questions/313644#comment543409_313661) | Compare의 Direction 기능을 몰랐다는 대상은 분명하다. 예전 radius/arc-length 구성이 있었다는 말도 별도 유지한다. | 제안자 graph/GIF/연결 blend를 작성자의 실행으로 바꾸지 않는다. |
| QG-K1 | [제안783886](https://gis.stackexchange.com/questions/480481#comment783886_480481), [작성자784441](https://gis.stackexchange.com/questions/480481#comment784441_480481), [작성자784443](https://gis.stackexchange.com/questions/480481#comment784443_480523) | 0.5 치환의 제안 뒤 시도·실패1. 뒤의 성공 보고는 Bera 답480523에 $length/0.002 변형을 준 다른 방법이다. | ‘I tried that’를 사전 인지로 해석하거나 뒤 성공을 첫 제안에 귀속하지 않는다. |
| QG-N1 | [작성자779876](https://gis.stackexchange.com/questions/477944#comment779876_477957), [cleanup 링크779883](https://gis.stackexchange.com/questions/477944#comment779883_477957), [작성자780200](https://gis.stackexchange.com/questions/477944#comment780200_477957) | OpenEx 작동 보고와 Close 발견은 with 링크보다 먼저다. 새로 알았다는 단위는 with 지원이며 with 실행은 미확인이다. | OpenEx 성공을 with를 배운 뒤 실행했다고 연결하지 않는다. |

숫자ID와 생성시각을 전체 캐시에서 재집계한 결과는 기존 후속 투영과 일치했다. 시간순에서 작성자 이벤트는 BL-T2의2, QG-T2의2, QG-T3의1, QG-T4의1이다. QG-T1은 질문자ID 자체가 없으므로 ‘후속 없음’ 대신 동일인 확인 불가를 명시해야 한다. 자기 답을 포함한 답·댓글 코퍼스는 재집계했지만, 모든 공개 revision 원 응답을 이번 검토에서 다시 전수 판독하지는 않았다.

## 반례 표본에 관한 수정 권고

- [BL-C1의 먼저 알려진 Euler 순서](https://blender.stackexchange.com/questions/322945#comment563323_322945)와 [뒤 Rotate Euler 방법의 작동 보고](https://blender.stackexchange.com/questions/322945#comment563659_322995)는 같은 질문자187451이다. 이것은 ‘이미 알던 설명 이후 다른 방법의 작동을 보고’한 **D1 사례**로 적절하다. 독립 출력/성능 측정, 전체 새 방법 사전 인지, 원래 방법을 완전히 폐기했다는 주장은 미확인이다.
- [BL-C2의 작동 보고574773](https://blender.stackexchange.com/questions/328659#comment574773_328666)는 [후속 levels 새 지식574826](https://blender.stackexchange.com/questions/328659#comment574826_328688)보다 약15시간 앞선다. 학습 뒤 실행이라는 연결을 반박하는 데 적절하다. 두 답의 기술 설명 자체를 이 판독이 공식 검증한 것은 아니다.
- **스키마/표시 주의:** `auxiliary-counter/countercases.json`의 QG-C1 `followup` URL [790648](https://gis.stackexchange.com/questions/481552#comment790648_481556)은 질문자242921이 아니라 **다른 사용자221706**의 `{-y}` 제안이다. 최종 표에서 작성자 후속처럼 보이게 배치하면 안 된다. actor 또는 `later_other_comment` 표기를 두고 작성자 채택은 미확인으로 유지한다.
- 반례 3사건은 고정12자리의 분모에 추가하지 않는다. 같은 사건의 여러 댓글을 독립 사건/저작으로 세지 않는다.

## 원장 결합과 아직 남은 검토

1. 현재 initial.csv의12개 `source_refs`는 모두 root sources.jsonl에서 해소되며, case_id·candidate_id는 각각12개 고유다. 시간순/보조 질문의 교집합은0이다. QGIS 보조 참조 ID의 표현 수정은 선정 변경이 아니다.
2. source counting 키가 `counted_unique_primary_source`와 `counts_toward_24_primary_sources`로 다르다. 단순히 한 키만 합산하면 QGIS 초기4개가 누락된다. root가 원 필드를 보존하면서 정규화하기로 했으므로 최종 집계에서 다시 확인한다.
3. 보조 원글4개를 ‘필수 시간순 원글8개’ 하한에 섞으면 안 된다. 교차 분야22취득 기록도 필수4저작으로만 보수적으로 산입한다. Blender/QGIS 공식4+4와 상류2+2 최종 원장이 아직 합쳐지기 전이므로 전체24 달성은 이번 1차 검토가 인증하지 않는다.
4. `proposals.csv`의 `evidence_record`는 판독 파일로 이어지지만 명시 `source_refs` 열은 아직 없다. 최종 표의 원문 URL과 evidence_record가 유지되면 사람이 추적할 수 있다. 자동 결합을 하려면 canonical source_id를 추가하거나 별도 매핑을 제공해야 한다.
5. 선정 뒤/초기 판독 뒤의 정보를 읽었다는 사실을 노출 원장에 보존하고, 이 검토를 완전 맹검이나 외부 검증으로 표현하지 않는다. 최종 RESULT/returns/SELF_CHECK 생성 후 별도2차 일치 검토가 필요하다.
