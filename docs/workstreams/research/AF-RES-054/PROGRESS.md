# AF-RES-054 進行 기록

| 묶음 | 원격 SHA | 확인 범위 |
| --- | --- | --- |
| ① 모집·공동 종점·계산 규칙 | bea80dac12d7fe982319705b69b5744a8e7852c6 | SCOPE/manifest/session start, 결과 열람 전 규칙; 고정 SCOPE를 GitHub에서 재열람 |
| ①a 검색 문법 적응 | 1127a6f5a84f229f6cb417cd3fe111a6c3e8f8dc | native API/Boolean parser의 실제 한계를 발견한 뒤 새 연구 선정 전 동치 질의 분해를 명시 |

원격 Git 쓰기는 연결된 GitHub API로 수행한다. 셸의 공개 Git fetch는 가능하지만 git push는 인증 입력을 요구하여 실패했다. 토큰을 읽거나 인증 설정을 바꾸지 않았으며, base tree→commit→expected_sha 조건부 ref 갱신으로 같은 허용 경로를 커밋했다. 로컬 준비 커밋 ca8c86182c63b92453ce0f4680a0321738f56a00은 원격 결과 SHA가 아니며 원격 ①판으로 로컬 포인터만 정렬했다.

세 분담자는 기준+방법, software 모집, 교육/공학 모집을 서로 다른 streams 하위 경로에서 수행한다. 편집자는 root다. 분담 조사는 독립 외부 심사나 별도 사람 검토로 보고하지 않는다.

원논문 PDF/압축파일의 임시 캐시는 재배포하지 않는다. 인용 URL·판·위치·내용·한계·필요한 집계와 검증 절차를 커밋하며 캐시는 산출물 완료 수에 세지 않는다.
