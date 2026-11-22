# 자료 단위와 공개 시각의 근거

GitHub 공식 review 설명과 REST review/comment 명세를 직접 읽었다(M01–M03). Review는 comment들의 묶음이며 고유 review ID를 저작 단위로 센다. 한 review 안의 여러 inline comment와 파일 hunk는 자료 수를 늘리지 않는다. 일반 issue comment는 PR 저작에 보수 합산한다.

`original_commit_id`/원 hunk와 `submitted_at`은 검토된 판·공개된 review를 고정하는 데 쓴다. git author/committer 날짜를 review 게시일로 바꾸지 않는다. review 게시와 작성자의 실제 읽음·수정 이유·작업시간은 각각 다른 관측이다. PENDING review의 submitted_at 부재도 직접 노동시간 부재와 같지 않다.

이 명세는 현재 접근판이다. 2023년 UI/백엔드의 역사 전체를 재현했다는 근거로 쓰지 않는다. 이 방법 문헌3개는 과제의 최소26개 배당에 더하지 않는다.
