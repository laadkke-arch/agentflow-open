# AF-RES-151#1 HANDOFF — PARTIAL (후속 실측·재판독 완료, 엄격 미충족 명시)

## 기준 및 결과
- 저장소 laadkke-arch/agentflow-open; 브랜치 work/research-af-res-151; 허용 경로 docs/workstreams/research/AF-RES-151/.
- 기준 인계 1b1ebb24347000f60acbe4ad2e9aa8c94ba416b9에서 재개. 이전 SCOPE/원장/비교/감사 파일 8개 그대로. 이전 인계는 해당 SHA에서 열람 가능.
- **후속 결과 SHA 659102892a691c5cfab1a27e80904fe94799724f**. [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/659102892a691c5cfab1a27e80904fe94799724f/docs/workstreams/research/AF-RES-151/RESULT.md), [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/659102892a691c5cfab1a27e80904fe94799724f/docs/workstreams/research/AF-RES-151/SELF_CHECK.md), [후속 검산](https://github.com/laadkke-arch/agentflow-open/blob/659102892a691c5cfab1a27e80904fe94799724f/docs/workstreams/research/AF-RES-151/followup/final-verification.json). 결과 blob 6fe3154c7f4f2b409c9c158722a1c7d5e1fcf82e, 자체 점검 blob 494f1c7b6eb73860fcc964760ccd60639bbc47bd; 고정 SHA에서 직접 읽어 확인. 기준 이후 24 변경 경로 모두 허용 범위; 기존 원장 변경 없음. 중앙 색인/공통 파일 변경 없음.
- 아래 인계는 결과 검증 후 단독 커밋. 자신의 SHA는 GitHub commit metadata로 확인.

| 단계 | 고정 커밋 |
| --- | --- |
| 자연 표본 사전등록 / N1 색인 / N1 판독 | 17f6990dd1094868a2166454efdadd5c9fbb1027 / 3ac89a8c350e8f58624f2b5b137619e424e0948b / c49dcba6463f22688df2f98f8019570562065bf4 |
| N2 사전등록 / 색인 / 선별 / 쌍 봉인 | 704252de135e00c0eefc283424fdbb00332dc1f3 / c218add3c55dbf38c8d750c145e86566c5910acf / a2159dfd53fe27160b2f91105d349be5d66706d3 / 36d91d4243bb928d47ac7a2a59d316ea5aab6ca4 |
| 가림 packet / 가림 자기 판독 / 공개·확장 공개 | 06353d7029175588ed595840745bc8bd90689af6 / 6592b0d1d22f959db84e919354d89c59c830c5fb / 979c483253d45eac447f19d40a740805eb0de4fb / e083e61045475a45359575bea259811280a85a10 |
| 후속 원문 / 추가 원문 / 인기도·운영 metadata | 9eb58503281f2f84b0261bd9f0f239eb3ae5ca01 / 127455fe3e33ed4defe2b44e156c672c7a45933b / cafa1d0a93d15af466b561a3e69939d22110eb25 |
| 자연 쌍 / 선별 / 중간 검산 / 고정 원장 재계산 | dca4e582060787bd47b3fe0497c149c6242dd3c0 / 4e2111266b1860a8a5a50d29b827271f94ba27ad / b49ed23567d1b7b8242161a22d27357e249fadc2 / d737cd5254b9db4959053318709266612663b621 |
| 실제 OCR 코드·receipt / Git·Go 코드·receipt | e816351c398f5421f0660418158e6d67022959af / 127e4f76d90cbe44fc944c5159abac51d9e893ad / eb3febb7bef38e23878473eddc7c72a1e8c257fe / c28e0c0b80e8995f3356e23b38f708aa16552fe5 |
| 결과 / 자체 점검 | d52c68cdf27c455b59f2c5f5a79d85caaeed83ca / 659102892a691c5cfab1a27e80904fe94799724f |

## 이번에 관측한 것
- 원 N0 Stack Exchange DNS/web 실패는 0/6 유지. 대체 자연 N1 7 반환 5 적격, N2 독립 사전등록 색인 30 반환·최초8 심사 6 적격(6 저자)/2 제외/22 quota. #9324 증상→과업 추론을 제외하는 민감도는 5/6. N2 후보 쌍 6 및 18 판단행 별도, 기존 12쌍 6대조 108행 및 기존 27 원자료 유지. 신규 후속 출처26행 counted20, N1/N2 사용자 적격 11건 별도; 합산 독립 원문 수는 단정하지 않음.
- 가림 자기 재판독 12/12 후 공개 12/12, 확장 별 비교 가능 6/12, 공개로 인한 변화0/12; 초기 대비 축약 근거에 따른 3셀 변경. 동일 연구자 사전 지식 선노출, 독립 판독 0. 작은 구현 D-Bus 기능·빌드 수정·사용자 장애/회복 원문, Vosk 예제 장애 및 조건별 사용자 보고 직접 확인. 저인지도=품질의 인과 주장 금지.
- 실제 Linux 합성 입력 3프로브: Tesseract PNG→TXT/PDF 성공 및 PDF 직접입력 실패, 정확 token4/7, 정확 영어 중심4/4 25px 이내, RO 3/3 diacritic 소실. Git collision 최소4→5자, Go generate 실패에도 asset 기존 시 build 성공, asset 제거 시 실패. 실제 역사 제품/사용자 원본 입력 아님.
- N2 확인합집합 11/18, 후보셀 S15/U20/X1; A 활성/보관9/11, B11/11, C 활성0/11 보관11/11. A 6 제외 슬롯 중 N2-01 및 N2-06 유일 atom 2개 손실. 동률 및 unknown 민감도 재계산; 자연 18행 수치 차이0·근거 ID 누락0·가림 코드 연결 차이0. 기존 보충 분모와 합산 금지. 
- CineLog upstream #76 비자유 plugin 문제와 수정 제안, source 공개 댓글, completed 및 F-Droid 복귀 확인. DAO 수정 diff 미확보. Awesome PR #3919/#3901 직접 확인 open/merged=false. F-Droid D10 추가 실제 대체 fork·복귀 확인.

## 미충족 및 재개
PARTIAL은 완료가 아니다. 대체 자연 6/6과 자기 가림 12/12, 실행 3개는 실제 달성; 원 N0 모집단·순서 접근 불가, 대체 #9324 엄격 민감도5/6, 독립 가림 판독자 부재, 사용자 실제 입력/완전 계약·엄격 반전0/6, 실제 채택/재취득 노동과 CineLog 수정 diff 미확인. 실제 shell Git DNS 실패로 checkout/manifest start/check/CI 미실시. 다음은 원 X1 승인 HTTP 환경, 무명 packet 독립 판독, 원 PDF/고정판 및 실제 OS/라우팅/사용 입력, operation diff와 비용 측정. `followup/ocr_probe.py` 및 `followup/natural_probe.py`와 receipts로 좁은 프로브 재현 가능(환경 차이 기록). 변경 범위 GitHub compare 검증은 session check 대체 아님. 정확한 이전 start/check 조건은 SCOPE와 SELF_CHECK의 기준판 명령 참조.
