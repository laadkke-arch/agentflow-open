# ④ 발견 봉인 후 대조·반증·비용
- 발견/초안수정 봉인 227a522a2e6339345681fabc9e493827b1ee3916, 2026-11-24T14:50:25.664Z. 이후에만 아래 C01–C07을 열었다. C08은 소프트웨어 재열람. **사후 대조 0건을 자발적 발견 분자에 추가했다는 뜻이 아니라, 사후 대조는 전부 자발적 발견에서 제외했다.** 비교 가능한 A/B 0/8.
- 검색 경로: `site:archives.gov transfer permanent records electronic records transfer acceptance retain copy records agency confirmation`; `site:nationalarchives.gov.uk transfer digital records transfer preparation verification checksums acceptance`; `site:osha.gov 1910.147 energy control verification isolation release lockout tagout`; `site:ecfr.gov 21 CFR 211.192 production record review approval before release batch`; 별도 재질의 `NARA transfer permanent records electronic records transfer agency retain records until legal custody acceptance confirmation site:archives.gov`, `UK National Archives transfer digital records transfer preparation validation checksum transfer site:nationalarchives.gov.uk`. C06/C07 403 → PDF 독립 원전으로 대체, p2/3 실제 스크린샷 확인. 결과 목록만으로 산입 금지.
| 원전·분야 | 원 입력→작동→보존값 | 대상의 대응 | 깨지는 조건 / 제안 시험 |
|---|---|---|---|
| C01 기록관리 | 영구기록과 일정→승인된 이전·수탁 상태→보존 책임 명시 | J-W1 저장 성공/공유 선택/수신 확인을 별개 상태로 | JEX 내보내기는 법적 수탁이 아니다; 공유 성공 후 원본을 자동 삭제하지 말 것. 수신 불명에서도 로컬 복원 가능해야 함 |
| C02 기록관리 | 목록·체크섬→복사·검증·서면 확인→기록 무결성 및 책임 | 파일 경로/크기/체크섬·readback 확인 후 저장 성공; share cancellation 별도 | 무결성은 복원 완전성 아님: 첨부가 빠진 정상 체크섬 파일은 복원 실패. 불완전 manifest fixture; 정책상 자동삭제 반려 |
| C03 제조 설비 유지보수 | 에너지 경로→격리·잔류 제거·검증→위험 접근 방지 | J-W2 선언된 포트 없음과 실제 외부 접근 실패 별개; 구성 변경 후 재검증 | 공정 작업자 잠금과 DB ACL 동일 아님; 운영 연결도 끊는 모든 격리안은 앱 연결 보존값 위반. 재시작 후 다른 컨테이너 접근 시험 |
| C04 의약 제조 | 생산기록→품질 검토/승인→배치 릴리스, 불일치 조사 | J-W1 export 완료 후 검증 gate; J-P2 심각한 오류는 배너 숨김과 상태 해결 분리 | 인간 QC를 그대로 강제할 이유 없음; 정상 저위험 배너 dismiss 금지하면 작업성 해침. 손상 export 후 share disabled 확인 |
| C05 기록관리 예외 | 물리 수탁→기한·통지→법적 수탁, 기존 일정만 | 저장 위치/사용자 통제는 분리할 수 있음 | 새 일정에 적용 불가. 신규 Joplin 흐름에 법적 절차를 그대로 이식하지 않음 |

## 반례 및 분리 판정
- 같은 단어/다른 역할: S07 GDAL 'layer'는 단일 OGR entities layer + 속성이고 F-W1의 물리 document-tree node 아님. S08 Ventus는 실제 tree지만 2026.2 후기 자료. 가까운 산업의 기능도 요구한 dimension 의미 보존은 확인 못 함.
- 재포장·중복: S05/S06 ezdxf 동일 1.4.5 manual, S01/S02 Google Sheets API, S09/S10 Inventor manual, S19/S20 Compose 문서. 미열람 mirror/검색 결과는 전부 제외. S13 이해문서와 S14 별도 failure test는 S14만 최소량 산입. C08=S12. S21 Docker Engine 추가 문서는 보수적으로 하한 제외, S22 독립 재현 이슈 산입. C05 추가 NARA 운영 예외 보수적으로 제외.
- 반증: S05 explode가 source INSERT를 파괴, virtual_entities는 XCLIP/MINSERT/scale 한계, S07 dimension fallback 비선형→선형, S10 식 제한, S14 sticky footer 역효과, S15 고심각도 배너 상시 dismiss 금지, S16 cloud URI/앱 uninstall, S18 AtomicFile lock 없음, S21/S22 구버전 및 라우팅 모드. 모두 문서/보고, 자체 실행 없음.
- 일반 검색만 찾은 적격 사례인지: A/B 다른 사건 단일 노출이라 A-only/B-only 판정은 불가능. J-W2 A는 이미 원문의 가까운 해결책 확인 사례이며 B를 필요로 했다고 주장하지 않음. F-W2 B 역시 같은 CAD 제품 문서라 cross-field 탐색이 필수였다고 말할 수 없음. 산업 이름/후보 미주입 의도와 달리 F-P2 B 쿼리의 ezdxf, J-W1 B 쿼리의 SAF 명칭이 사전지식 반영; 배정은 순서 기준이지만 세션 분리와 진정한 masking 없음.
- 표본 선행 노출: 80개 first body 모집하며 인접 사례 #9669를 알게 됐고 S04 후기 이슈가 A 검색에 노출됨. S04는 원저자/다른 이슈 당사자 보고로 분리, pilot packet에 넣지 않았으나 동일 문맥 오염을 제거할 수 없음. 현재판 문서들(특히 Ventus, Chrome 등)은 2024년 당시 가용성 증거 아님.
- 비용: 별도 `costs.json`. 같은 문맥 단계 wall-clock는 실제 UTC 차이; 일별·사건별 측정, 모델 토큰·가격·사람 실제 분·원저자 재작업시간은 미확인. 비용 차이/절감률 산출 불가. 검색/개봉은 URL 문서 단위, follow/find 반복은 새 작품 아님.
- 원장 정정(봉인 후, 원본 변경하지 않음): F-W1 S08 Ventus의 combined visible rerun order는 discovery의 전체 나열 기준 13번째이고 S08.route의 "rank 11"은 불일치. 실제 검색기관별 순위는 원본 웹 결과가 배치로 병합되어 복원 불가; 13번째 표시 순서만 사용. C08의 S12 최종 수정일 2026-11-06을 확인, 후기 문서. F-P1 S04 시기별 의견은 후기 관측이며 실제 해결 코드 확인하지 않음.
