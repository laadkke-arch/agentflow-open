# AF-RES-206 실행 영수증

- [기준 설정](../inputs.json)에는 발행 주소, 확인할 멤버명, 헤더, 원문 지문, 고정 분모가 있다. [publisher-attempt.txt](publisher-attempt.txt)는 실행 환경에서 받은 실제 거부와 원발행자 응답 미관측을 기록한다.
- [comparison.stdout.jsonl](comparison.stdout.jsonl)은 40점씩 두 X05 렌더링 표를 CSV로 옮긴 입력과 GitHub 고정 원문을 사용한 실행 원출력이다. X05 추출 SHA는 실제 HTML SHA와 다르다. 해시 대상은 `table,web_line,point_id,value1,value2,value3` 머리행, UTF-8 LF, 웹 행 번호 순서 92–131 및 136–175의 CSV 직렬화다.
- [x05-selected.csv](x05-selected.csv)는 지정 6점과 높이 보강 3점의 관측 값·위치다. [fresh-replay.stdout.jsonl](fresh-replay.stdout.jsonl)은 새 임시 디렉터리에서 고정 GitHub 바이트를 다시 받고 그 9점 발췌로 돌린 출력이다. 두 실행의 `points.csv`, `deltas.csv`는 바이트 단위로 동일했다. stdout에는 HEAD/동일 파일이 아닌 해시 고정 입력과 도구판이 있다. stderr 두 건은 각각 0바이트였다. 종료 2는 데이터를 비교하고 공식 판별이 보류된 경우다. 종료 1은 파싱 또는 검산 실패다.

## 재현

저장소 루트에서 Python 표준 라이브러리와 curl을 사용한다.

```sh
owned=docs/workstreams/research/AF-RES-206
run_dir=$(mktemp -d)
python "$owned/compare.py" --work "$run_dir" --fetch-comparators
```

full ZIP과 X05 HTML에 HTTPS GET할 수 있는 실행 환경에서는 같은 도구의 발행자 모드를 사용한다. 현재 결과의 `members.csv`에는 결과로 확인되지 않은 ZIP을 나타내는 결측 행만 있다.

```sh
python "$owned/compare.py" --work "$run_dir" --fetch-comparators --download-publisher --download-x05
```

공식 링크·필수 파일과 데이터 형상 검사를 통과하면 값과 ZIP inventory가 임시 디렉터리에 생성된다. 로그의 실제 URL/상태·바이트·SHA와 README·모형 가이드 판을 함께 확인한다. 발행자 ZIP이 자격을 갖추면 종료 0이 될 수 있으며, 점별 공차는 사람이 확인한 문서 범위에서 별도 기록한다. 임의로 제공된 local ZIP은 공식 배포의 확인된 SHA와 일치해야 공식 열에 쓰인다.
