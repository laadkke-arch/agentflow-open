# 12자리 원 출력

각 ID는 새 실행 디렉터리에서 원본 또는 재정의 Qmd를 같은 명령으로 1회 렌더했다. Quarto가 한 렌더 안에서 xelatex를 2회 호출한 것은 바깥쪽 반복 수와 구별한다.

- 입력·명령·시각·종료값·세부 실패 플래그 및 입출력 SHA는 [runs.jsonl](../../runs.jsonl)에 있다.
- 각 ID의 `document.pdf`, `document.tex`, `document.tex-log.txt`, `document.fls`, `render.stderr.txt`, `process.txt`가 PDF와 생성 TeX, TeX 원 로그, 런타임 로더, Quarto 진단, 추적 선택행이다.
- `pandoc-defaults.yml`과 `pandoc-metadata.yml`에는 실제 임시 입력 바이트를 복사했다. `pandoc-stage.json`은 실제 임시 파일명과 해시를 적고, `reader.json`은 같은 staged Markdown을 번들 Qmd reader로 읽은 필터 전 독립 프로브다.
- `pdf-raw.json`은 실제 페이지의 워드·벡터와 래스터 단면을 보존한다. `target.json/png` 및 두 표 조건의 `control.json/png`가 표별 판정 프로그램 출력과 해당 벡터-래스터 비교에 사용한 이미지다. 좌표는 PDF 페이지 좌측 위부터 오른쪽·아래 방향 pt다.
