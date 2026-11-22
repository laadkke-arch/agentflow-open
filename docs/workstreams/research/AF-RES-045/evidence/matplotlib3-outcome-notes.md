# M03 봉인 후 판독

봉인 `0d998cb3503e8a7f0faf2bf2f8e62dd046a662b1` 뒤 2026-11-22T22:20:09.248Z에 댓글을 처음 열었다. `requests.csv`와 `predictions.csv`는 그대로 둔다.

원작성자의 [수락](https://github.com/matplotlib/matplotlib/issues/13600#issuecomment-470159527)은 A인 `transAxes` 조작을 정성적으로 뒷받침한다. 그러나 두 봉인 factor의 좌표 로그는 없다. 같은 이슈의 [PR13603](https://github.com/matplotlib/matplotlib/pull/13603)은 별도 `None` 접근 버그를 고쳤다. [고정 시험 L313–327](https://github.com/matplotlib/matplotlib/blob/f9d8cd7e0c9a4e94962fc925c57fb678ba252f87/lib/matplotlib/tests/test_tightlayout.py#L313-L327)은 colorbar가 없는 큰 annotation과 rect 입력이다. 시험 정의와 공개 통과 보고를 색상막대 위치의 실행 근거로 재사용하지 않는다.

3.0.2와2.2.2의 고정 colorbar.py를 비교해 좌표 단위가 달라지는 조건을 확인했다. 이는 정적 판독이며 실행 출력이 아니다. 봉인 후보P2는 값 .5의 보존이 목표인 다른 문제에서는 맞지만, 원래 중앙 배치 조건에는 맞지 않는다. P2가 예상한 실패 자체가 맞는 경우도 있으므로 '틀린 원리'와 '목적에 맞지 않는 조작'을 구별한다.

원작성자는 최초 생성시 제목만 제출한 뒤 본문을 완성했다고 밝혔다. 현재 첫 게시물이 생성순간의 불변 판이라는 가정은 성립하지 않는다. 완료본문은 해결 조언보다 앞서 있었지만 정확한 그 판은 복원하지 못했다.
