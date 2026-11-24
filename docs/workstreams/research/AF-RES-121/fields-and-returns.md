# 타 분야와 반환 역할

## 교통계획: 같은 정렬, 다른 선택, 남는 제약
T1 FTA ROD pp1,6–7 및 MMRP TST-2: 3A/3B는 Fourth/Stockton 정렬 공통. 3A는 station locations/platform size/tunnel length, surface station 여부에서 다르다. 3B LPA 2008-02-19, 8-19 adoption. ROD 3A 기각 근거는 예측 건설비뿐 아니라 Chinatown 핵심 접근성, 814–828 Stockton 역사자원, 상점 이전 10 vs 8, 공원 영향. T2 July11 공개된 AB-2는 공통 Powell 환승 접근 및 BART 별도 egress 요구와 2004/2008 용량 분석, 모델 가정 검증·비용 분담 계획을 기록. FTA TST-2의 pedestrian LOS D 이상 유지 및 책임 SFMTA/BART/공사 후 monitor 조건을 연결. 3A를 버려도 승객 안전/용량은 사라지지 않는다. 2008-05/06 분석은 2월 선택보다 늦음. July response/ROD도 앞선 선택의 회고/승인 근거이지 정확히 최초 변경을 일으킨 특정 문서로 소급하지 않는다. $172m 예측 차이는 실제 절약/노동시간 아님. F14 당시 회의 transcript timeout; T2 스크린샷은 크기 제한(F15), 텍스트만. 실제 첫 회의의 시각과 독립 연구 원문/실행 관측은 미확인.

## 미술 보존: 사전 승인과 사후 결과를 분리
T3 NG 2006 conservation policy: 대형 treatment 전후 Board 승인, dossier에 전후 사진·서면 보고서. T5 AIC §25–28도 examination/date/examiner→alternatives/risks→dated treatment→보존을 분리(비교 기준일 뿐 NG의 규정으로 전제하지 않음). T6 NG194 Board minutes 2023-03-30 item1.2: examination reports를 받고 제안 treatment 승인. **선행 117의 사전 승인 공백 일부 해소**. T7 2024-05-23 item1.1 Board 재전시 승인. T4 2024-06-18 기관 결과 보고: Rubens 원래 구성으로 회귀 vs 후대 변경 유지, 1940s 처리 수준 유지, retouch 및 cradle 조정(전체 교체 대신 더 유연한 battens), panel provenance/condition 판단. 사전 보고서 내용 자체는 미공개/미확인, 1940s 수준의 선택 및 cradle 상세 결정을 누가 언제 명시 승인했는지는 모름. 회의록은 treatment approval이고 개별 보존 대안 선택의 근거가 아님. 14개월 전체 경과를 절약 시간/실제 노동시간으로 변환 금지. 별도 dossier 요청 또는 공개 board annex 확인이 다음 첫 행동.

## 같은 사건, 역할별 반환
|사건|제안자 (선택·조건)|리뷰어 (반례)|승인자 (권한·결정)|후속 구현자 (입력·실행)|
|---|---|---|---|---|
|R1|E1+E1a: datagram mux는 Linux 및 태그 필요; EOF 없음|A5+A6: 주장 한정, A3 두 Vec 및 종료/drain 조건|A4+D1a: 이미 폐기 유보; 승인/merge 별도 조회|E1 example, child writes both streams and explicit done/exit then drain; non-Linux error path; test 제안, 미실행|
|R3|E2/E3: unsafe Pod / enum dispatch 제한; 자동 도입 금지|A8/A9/A10/A12: wrapper, unsafe, generic proc macro type info|A13/A14/A15: TODO ≠ 승인, 철회 이유 복합|I2 example, StepBy<Enum> vs concrete wrappers; all bit patterns/padding 조건; playground/bench 실행 미확인|
|P4|T8/A19/A20: use-case 좁히기, 혼합 read-only keys 보존|E6/A18/I8: final/narrowing과 update unsound 구별|I3/T9: TC 권고+SC 승인; 외부 mypy 직접 귀속 아님|I5 tests and I6 release, qualifier combinations/inheritance, check actual test receipt; Child2 assertions audit|
|R2|E4: bail early Err, panic 아닌 비유|A23/A24: 이미 결정된 위치와 후행 링크 분리|A25: 범주 보류, root compat 유지|D2 only commit; re-export 테스트 별도, 없음 확인 아님|
|R4|E5: GHC error vs ignorable hints|A26/A27: terminology only|A28/A29: design meeting policy; governance record|I7 UI fixtures unsupported options/warnings/accepted attribute; run receipt absent|
|교통|T1 rejected reasons + common alignment|T2 BART request/capacity study|T1 3B approval and MMRP|TST-2 monitoring, actual LOS and safety results missing|
|보존|T3 plan + T6 proposed authorization|T4 material alternatives and condition|T6 and T7 separately dated approvals|T4 process, request actual dossier and decision note; no person-hours|

반환 계약 제안: 역할별 1–3 핵심 링크와 같은 claim_id에 비교/대조 링크를 병기, 주소+fixed version+passage/hunk+당시 유효 범위+반례+권한+관측 유형+미확인 이유+검증 입력. 인과는 D3의 3 gates를 통과할 때만 말함. 추천(적용 가능), 보존(조건), 기각(이유), 시험(입력/expected/receipt 분리) 네 종류를 독립 반환. 설계자가 묶음에서 각 링크를 독립 채택·보류·조합할 수 있게 하고, 실행 성능/노동시간을 추정해 채우지 않는다.
