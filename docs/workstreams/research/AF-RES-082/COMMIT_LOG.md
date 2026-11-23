# AF-RES-082 묶음 커밋 원장

아래 SHA는 GitHub `work/research-af-res-082`의 실제 원격 커밋이다. 각 묶음은 완성 직후 독립 커밋했다. 로컬과 원격의 작성자 메타데이터 차이로 SHA가 다른 경우 전체 git tree가 같음을 비교하고 원격을 기준으로 정렬했다. 세부 local/remote/tree/부모값은 `evidence/bundle-*-readback.json`에 있다.

| 요청 묶음 | 원격 SHA | 완료 내용 |
|---|---|---|
| ① 모집틀·보기·예산 | `476c341c9e863f8ad58b1254bdde3fd955f1f8f9` | 전체 조직 목록, SCOPE, 작업 manifest, 사전 방법 |
| ② 원요구·사전 링크 | `8ba1d686d4c7e50067f9d52bc753a4e02708cd42` | 여섯 자리 고정, 원요구·태그·A/B 최초 링크, 모집 포함/제외 |
| ③a 예산 판독 봉인 | `5f881c7094bf30be13069554b412a00c5b01f7c0` | 사후 배포 기록을 열기 전 2문서 예산 평가·실제HTTP/재사용 기록 |
| ③b 외부 분야 판 관계 | `6e83088ebfc21d285a58dabbe0e3d511b64ba7b9` | PLOS·Zenodo 쌍, 구판/정정PDF, tombstone·DOI alias·정책 한계 |
| ③c 독립 문서 게시 사건 | `3bacf25be32bd749844ae11898763ba478a4ca24` | prefix, alias, 태그권한, 관리형루트 사건·시도 원장 |
| ③d R 배포 계보 | `ae6fb65bc612120ca38337bd2b7f193b9c3664c1` | 선택 tag→생성 git HTML→현재 응답·지문·Pages 최종상태 공석 |
| ③e Python 배포 계보 | `97629ee228a59043162361674d5eeec77c5c8e21` | RTD exact-SHA 성공·실패 로그, named/alias 판별, native generator 계약 |
| ③f 현재 지원·정확한 딥링크 | `986d60e5bcbd9f327f142e2024bbd289f04778fe` | 현재 공식 서비스 범위/제한, P3 stable anchor·고정 README 위치 재확인 |
| ④ 표·카드·분모·자기검산 | `2e4ab7bc4ad4cf0ff35dc1d13fe97013670f430c` | RESULT표1–3, 6카드,201행/29계보, 검산27pass, PARTIAL·다음 조사 |

④의 수용 증거는 evidence/workbench-check.json·acceptance.json 및 bundle-4-readback.json이다. `2e4ab7bc…`의 전체 원격 tree를 비교했고 RESULT.md의 원격 blob도 재열람했다. 수용 증거 추가 커밋은 HANDOFF에서 식별한다. ⑤ HANDOFF는 그 검사 뒤 마지막 단독 커밋이다. 자기 파일 안에 자기 커밋 SHA를 만들어 넣지 않고 외부 커밋 이력과 최종 응답에서 식별한다.

이 기록은 중앙 `dot-control.json`이나 STATE를 변경하지 않는다. 배정자가 결과와 PARTIAL의 재개 입력을 검토해 색인/상태를 반영한다.
