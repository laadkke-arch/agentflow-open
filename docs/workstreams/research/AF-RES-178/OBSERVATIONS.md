# 관측 단계 ③

- S43은 커널 실제 문자열 비교 보고, S44는 ScanCode의 입력 정책 요구다. 둘은 지명 소비자와 별개. ② 이후 추가한 근거로 sources/frame 보정.
- 세 소비자 중 scikit-learn-extra는 #141 미병합 제안→#167 병합. 정확 전후 627f97b011cb267828e89cdf9257e35f59b328e7→0f95d8dda4c69f9de4fb002366041adcb1302f3b; conftest와 CommonNN 세 분기. 2023-03-27 v0.3.0은 먼저 배포되었고 구형 코드. post-merge 첫 태그 미확인.
- Yellowbrick은 #1323(2025) 제안만; 앞선 #1319(2024) 정확 부모 f7a8e950bd31452ea2f5d402a1c5d519cd163fd5→5e493f212aca0efc845c63dadc4736c0bfcfa96f를 별도 대조로 확인. 둘을 연결된 수정으로 합치지 않는다. 태그 v1.5는 구형.
- Elpy 2021은 JSON 경고 억제, 2024는 distutils 모듈 부재를 setuptools 의존성으로 해결하는 병합. 두 수정은 동일하지 않음. fork S17은 정확 same-call 교체, S18은 import fallback만. upstream 채택/배포 미확인.
- values 28자리: MNE 1.0.dev0 비교 보고는 #514/#10404 같은 관측 1건; Manjaro 보고 1건 별도. 12 fixture는 실행값이 아니라 기대. Yellowbrick 3.4.1/1.5.0 및 scikit CI 문자열은 원자료 값에 규칙 적용한 추론, 실행 미확인. Elpy latest null은 비교 실패값으로 해석하지 않는다.
- 실제 병합된 지명 same-call 전환 1/3, proposal/fork exact 전후는 3/3. named post-merge same-call 교체 첫 tag 0/3 확인(나머지 미확인/미병합), named 동일 환경·값 runtime pair 0건 확인, 실제 부재라는 뜻 아님.
