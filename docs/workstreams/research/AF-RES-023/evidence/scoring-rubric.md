# Q6 채점 규칙 — 정답 노출자의 자기 점검

최종 비교는 v3의 동일 입력16사건48행과 v4의 두 사건 재판독6행을 결합한다. 변경 경위는 protocol-errata에 있다. 사전 큰 범주는 SCOPE에 고정했고, 여기서는 판독 답안과 키를 대조할 세부 기준을 명시한다. 이는 기계 채점기·외부 독립 심사·실제 추천 시스템 평가가 아니다. 입력별 답안을 그대로 보존하고 root가 근거와 오류를 기록한다.

## 세 판단을 분리

1. **옛 대상 복원**: 의도한 대상의 종류·구분점, 당시 인용한 catalog ID, 그 ID가 다른 대상으로 잘못 쓰인 경우의 불일치를 사후 키의 확인 범위 안에서 복원했는가. 현재 올바른 목적지의 선택과는 별도다.
2. **기능·판·이유 복원**: 그 링크를 쓴 목적과 요구 판/버전/매체/조직 단위를 복원했는가. exact 판을 요구하지 않는 카드에 불필요한 exact 조건을 더하지 않는다. 당시 주장이 틀렸음을 지적하는 것도 복원이며 그 주장을 승인할 필요가 없다.
3. **목적지 결정**: 판독자가 SELECT/HOLD/CONDITIONAL 중 무엇을 택했고, 키의 확인된 관계·목적에 부합하는가. 적절한 HOLD는 오연결이 아니다. 현행 HTTP나 설치 실행 미확인만으로 과거 고정판의 모든 사실을 부정하지 않는다.

| 값 | 뜻 |
| --- | --- |
| PASS | 키가 확인한 범위의 필수 구분을 맞췄다. 외부 음원/법적 동일성·전수 복원을 추가 증명한 것은 아니다. |
| PARTIAL | 일부 대상/목적을 맞췄으나 판·역사 referent·서로 다른 실체의 구별 또는 필요한 ID가 남는다. |
| HOLD | 그 축에 답할 자료가 없어 명시적으로 판정을 보류했다. |
| WRONG | 키와 모순되는 특정 대상/판을 단정하거나 과거와 현재 관계를 잘못 연결했다. |
| UNVERIFIED | 키 자체에 필요한 정정판/관계가 없어서 그 축의 정오를 판정할 수 없다. |

PASS의 분모는 항상18이다. 미확인 사건을 분모에서 빼지 않으며, PASS·PARTIAL의 합을 전체 역사 복원 성공률로 보고하지 않는다. 이미 확인한 좁은 주장에는 PASS를 주더라도 `key_completeness_limit`에 source ID·원판·외부 소비자 범위의 미확인을 남긴다. `UNVERIFIED_ACCESS`·`EXTRACTION_NOT_RUN`·`RELATION_NOT_RECORDED`는 서로 다르고, 실제 소실이 입증되지 않으면 LOST로 쓰지 않는다.

## 필수 구분의 사례

| 사건군 | 대상/기능에서 채점할 핵심 | 별도 보류로 남기는 내용 |
| --- | --- | --- |
| MB01 | Europe 소장판과 US/Canada retained를 구별하고 새 Europe 후보를 조건부로 제시 | 소장 CD matrix, 원 source ID 직접매핑 |
| MB02·03 | Les Princes와 La Groupie, B4 비오케스트라와 retained 오케스트라를 구별; medium/길이 | 음원 독립 검증, source MBID 전수 |
| MB04·05 | 특정 CD를 요구하지 않은 recording 검색, 누락 데이터와 실제 다른 발매판의 구별 | source 외부ID provenance·독립 실물판 정답 |
| MB06 | 2024 소비자 MBID/지문 문맥과2026 target을 구별 | 2022즉시target·전체replica 완료 |
| ROR01·02 | 같은 COMTES 회사와 두 record, 본부와 소속division을 구별 | resolver 현재상태·전후전체dump |
| ROR05 | 역사적 ZFH 평가대상 유지와 네 후계 중 현재선택 보류 | 프로그램/학과 입력 없음 |
| ROR06–08 | 저장된 SLP/Spanish/Netrokona 주장과 잘못 사용된 원ID의 다른조직 정정을 구별 | 초기원판·법적공고·Spanish 정답ID |
| SW01·02 | 같은 배포물 또는 major3라는 좁은 탐색목적에서 불필요한 exact조건을 붙이지 않음 | archive bytes 및 설치실행 |
| SW03 | 같은 GNU readline6.2.4와 canonical 설치명 문제를 분리 | 최초rename 원문·실제keg재현 |
| SW05 | 2022배포물14.5와2024Rails 최신목적의@16을 구별 | 2026최신·DBmigration |
| SW06 | oldformula의 CLI generate/0.25.8과 현재library/CLI후계·소비자판요구를 구별 | 실제빌드재현 |
| WD01 | building의P910 category와institution을 구별; 별도consumerundo | category자체복원판·전수incominglink |

보기에 없던 관계를 맞히지 못한 것을 판독자의 능력 실패라고 해석하지 않는다. 원자료 풀의 누락은 세 표현 모두 동일하다. 한 표현당 한 판독자만 있으므로 변동성이나 통계 유의성을 계산하지 않는다. 관계와 사후 판단을 추가한③의 SELECT 수가 많아도 인과적 정확도 개선을 증명하지 않는다.
