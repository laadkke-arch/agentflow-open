# 사전 계획 이후 계측 보정

실행 예상과 판독 기준은 `d183ff516cc648f161acb0f9077666f42dcac914`의 [plan.json](../fixtures/plan.json)에서 고정했다. 첫 드라이버는 080의 설치 메타데이터 필드 `install`을 `installation`으로 읽다가 종료 1이었다. 이 실행은 자식 프로브를 시작하기 전에 멈췄다.

필드명 수정 뒤 Click 8.0.3 CliRunner의 양성은 일치했다. 같은 배포의 경계 시험은 입력을 소비한 다음 EOF에서 25초 동안 끝나지 않았다. 프로세스 로그가 관측값으로 반환되지 않았다. 공개 8.0.3의 CliRunner 대체 함수는 EOF에서 빈 문자열을 반환한다. 기본값 없는 prompt는 이를 다시 읽고, 실제 `input()`의 EOF 예외는 Abort로 이어진다. [첫 두 자리](first-attempts.jsonl) · [CliRunner 대체 함수](https://github.com/pallets/click/blob/41f5b7a7967bb65910e8837bd4e8542a18feec6c/src/click/testing.py#L277-L289) · [prompt 루프](https://github.com/pallets/click/blob/41f5b7a7967bb65910e8837bd4e8542a18feec6c/src/click/termui.py#L135-L180)

CN01의 양성·경계 모두 실제 CLI 자식 프로세스의 stdin 파이프로 옮겼다. 두 소비판에 같은 변경을 적용했고 입력 `foo bar\n`, 패키지/Python, 조건, 기대는 유지했다. 이후 CN01 네 관측의 실제 CLI 종료는 양성 0과 경계 1이다. 원 보고자가 사용한 TTY의 운영체제와 입력 장치는 미확인이다. [보정 fixture](../fixtures/probe.py) · [관측](../runs.jsonl)

080의 `first-seal`에 있는 `frames.csv` SHA-256은 CRLF로 계산됐다. Git에 저장된 raw LF SHA-256은 `e41493246c52ea7c88e6b4f6524bcea912c91c57468c751c99820b3decf40fea`다. 322개 줄끝을 CRLF로 바꾼 해시가 봉인 `5e96dae202bb3bad6c80784f892fde7c5280ca4be1f28fad23b060fd0bc32d08`와 정확히 일치했다. 나머지 다섯 봉인 파일은 raw로 일치했다. [080 봉인](https://github.com/laadkke-arch/agentflow-open/blob/152f5261ab9a35ab675ab003931ac4dc89966b55/docs/workstreams/research/AF-RES-080/evidence/first-seal.json) · [해당 Git 줄끝 설정](https://github.com/laadkke-arch/agentflow-open/blob/152f5261ab9a35ab675ab003931ac4dc89966b55/.gitattributes)
