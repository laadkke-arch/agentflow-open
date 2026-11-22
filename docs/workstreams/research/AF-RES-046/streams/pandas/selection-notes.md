# pandas 선정 봉인 요청

고정 시각 2026-11-22T22:09:17.397Z. 자연층 N-P1 #50523(3순위), N-P2 #50530(9), N-P3 #50533(11), N-P4 #50539(14). 추가층 L-P1 #51109(6), L-P2 #51116(13). 40+40 원장 전체는 frame.csv. 후속 작성자 응답·diff·merge는 아직 의미 판독하지 않았으며 root 원격 SHA 뒤에 연다.

#50539 첫 surviving commit은 tests-only이지만 PR creation 이전 두 번째1b7de430의 frame.py/series.py 변경까지 읽어 구체 제안 코드를 확인했다. 모든 baseline SHA는 Git commit date와 PR creation을 비교한 후보이며 최초 공개 head를 입증하지 않는다.

## 탈락과 규칙 정정

자연층 #50529는 경고의 발생조건이나 데이터 변환이 아니라 경고 문구만 바꿔 제외. #50524는 성능만 개선, #50525는 기능 요구 없는 독립 random-print 파일, #50534 typing, #50536 tests-only로 제외. 결과로 선택을 바꾸지 않았다.

초기 SCOPE는 추가층에도 자연층의 사용자 I/O 변경 조건을 적용했다. root가 사용자 원문에 없는 과잉제한으로 정정하라고 지시했으며, 결과 판독 전에 같은40순위를 다시 적용해 성능 PR#51109를 추가층 첫 슬롯으로 선택했다. #51116은 두 번째. 원래 #51109 제외 및 이후 후보 심사를 frame.original_rule_status와 이 문서에 보존한다. 뒤 순위 PR을 더 읽은 사실을 미열람으로 바꾸지 않았다.

## 가림의 실제 한계

GitHub API는 현재 PR status·merge·head와 모든 댓글을 한 응답에 포함할 수 있다. 도구 내부 메모리에 수신하되 모델 출력은 created/title/body/author, earliest/precreation commit, reviewer URL 주변만 화이트리스트했다. PR body가 사후 편집되었는지는 별도 미확인이다. #51116 필터의 첫 버전은 reviewer URL이 있는 모든 발언을 출력하여 후속 reviewer의 bridge 표현도 노출했다. 작성자 응답·패치·종결은 열지 않았지만 완전 가림이라고 주장하지 않는다.

## 선행 링크 가용성

L-P1의51784와 L-P2의51166은 원 제안 뒤 출판되었을 가능성이 있어 target 생성시각/판을 다음 단계에서 확인한다. 링크 당시 읽을 수 있는 자료와 최초 설계 때 조기 제공 가능한 자료는 별도 판정한다.


## 봉인 전 교차일관성 추가 확인

정정 규칙 원격 SHA 54f09f68dd671678820fc5f8cca64ecf541e8824. #51110은 초기 ca9e262에서 copy_on_write 전역 옵션을 False로 복구하는 실행 코드가 있으므로 문서라는 이유로 제외하지 않고 reviewer URL을 확인했다. human 후보 URL0. #51114의 cf3d784/4632194는 blank line·줄바꿈만으로 실제 구현불변이다. 두 슬롯의 선정은 그대로다. #51110의 pre-open merge commit648119도 도구로 조회했지만 upstream 많은 파일이 섞여 잘린 응답이었으며 이들 unrelated patch는 자료수·초기 구현 판정에 쓰지 않는다.
