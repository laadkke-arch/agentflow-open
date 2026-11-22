# AF-RES-044 원격 커밋 기록

| 묶음 | 원격 SHA | 범위 | 원격 확인 |
| --- | --- | --- | --- |
| ① | 0832f18bcb040871fa300db708a67d6f7f8866c7 | manifest, SCOPE v1, pilot-exposure | GitHub update_ref + git fetch |

로컬 git push는 HTTPS credential 부재로 실패했다. 인증된 GitHub 연결의 tree/commit/update_ref로 동일 파일을 저장했다. 로컬 선행 커밋 b3ed7b40d95df7a1b472e850371f5e71b996a221과 원격 커밋은 작성 metadata만 다르며 내용 tree가 같다. 이후 체크아웃을 원격 SHA에 soft align했다. 강제 push·권한 변경은 하지 않았다.

## ② 원요구·raw href·보강 풀·메타데이터 봉인

원격 `b36cc513ccbc1616168401ec9564866038e880a3`, tree `0dcddae3d9a803f73ab8420b9ec3feeada11f031`. 원격 ref를 조건부 전진한 뒤 fetch로 확인. 28개 파일; 80노출·72슬롯·원자·metadata. CSV 전송의 LF 정규화는 동일 행/순서이며 별도 봉인 정정으로 보존한다.

## ②b 원격 봉인 바이트·후기 브라우저 진단

원격 `8c22675a2e90134c386f362cdd2aabe7d14d252e`, tree `9a658b1203d7aebc92e39a358cc1dd95a168e295`. CSV LF 바이트 해시 정정과 v1 보존, Pandoc DOM 복구의 원 HTML 한계, Requests의 별도 browser 성공1회를 기록했다. 원풀·순서·요구를 바꾸지 않았다.

## ③ 후보 근거·36보기·실제 경로

원격 `ed63f44ff0586265d6640bedb82fc6c5c286f9b1`, tree `bf8cc9dfd7dafda2255fe64c80dcc1ccdd713f25`. 변경134파일의 Git blob SHA와 로컬 SHA256을 fetch 후 전부 대조했다. 고정 HTTP 계획/관측1,924개, 별도 Requests browser1개, C2 동일 출발카드의 새 exact-response 시행2개를 보존했다. 같은 관측을 방식별로 복제하지 않았다. sources632행/고유84원문, 원풀·후보별 근거·최소완전조합·36보기와 실제 도착 원장. 범위/해시 목록은 `evidence/publication-bundle3.json`.
