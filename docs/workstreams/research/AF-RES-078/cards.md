# 부분 작업에 반환하는 두 링크

## 표 · SQL NULL과 빈 문자열이 모두 필요한 경우

SQLite의 `CSV mode`와 Python 3.13.5의 `csv.reader`를 연결한다. 빈 NULL 표기(`.nullvalue ""`), 헤더, UTF-8, `newline=""`, `quoting=csv.QUOTE_NOTNULL`, 고정 스키마를 조합한다. 출력은 새 임시품을 작성한 뒤 성공 경로에 게시한다. [SQLite 3.46.1 CSV 출력](https://github.com/sqlite/sqlite/blob/version-3.46.1/src/shell.c.in#L2036-L2059), [CPython 3.13.5 CSV](https://raw.githubusercontent.com/python/cpython/v3.13.5/Doc/library/csv.rst).

정상·봉인 8행과 동일 정상 입력 재시도에서 T01을 지지한다. 실제 SQL NULL, 빈 TEXT, 문자 그대로의 NULL을 각기 다른 키에 두고 같이 읽으며, 개행은 따옴표 안에 넣어 논리 행 수를 확인한다. 같은 이름의 3.12 reader, SQL TEXT 내부 NUL, 헤더가 생기지 않는 0행은 결과를 바꿀 수 있다. NUL이 필요한 작업에서 별도로 실행한 typed adapter는 `N`과 `T<hex>`를 사용한다. [시험 데이터](fixtures.jsonl), [판 차이와 복구](evidence/diagnostics.jsonl).

첫 재확인은 입력의 NUL 유무, `sqlite3 --version`, Python 버전과 3개 NULL 구분값을 같은 키 조회로 확인하는 것이다. 재생 명령은 아래 링크에서 정상·경계·재제출을 함께 실행한다. [재현](tools/replay.sh).

## 이미지 · 원래 상대경로와 실제 픽셀 방향이 모두 필요한 경우

Pillow에서 `ImageOps.exif_transpose` 뒤 RGB PNG로 저장하며 상대경로 트리를 유지한다. 그 staging 루트에서 member list를 `zip -X -q -@ -b <temp-dir> <new.zip>`에 넘긴다. [Pillow 13.0.0 ImageOps](https://github.com/python-pillow/Pillow/blob/13.0.0/src/PIL/ImageOps.py#L690-L747), [Info-ZIP 3.0 man 페이지](https://manpages.debian.org/trixie/zip/zip.1.en.html).

I00은 새 ZIP으로 정상과 봉인 입력을 두 번씩 통과했다. 각 입력은 두 폴더의 동명 PNG이고 봉인은 Unicode와 반사 태그를 포함한다. Python 기본 이름 조회로 각 파일의 원 상대경로를 열고 네 코너와 크기를 검증했다. `-j`와 변환 단계의 평탄화는 각각 원 이름을 없앤다. I00 재제출에서 기존 ZIP을 기본 add로 갱신하면 이전 멤버가 남는다. 별도 `-FS`와 새 ZIP 작성 후 게시 대조는 관측된 이전 멤버를 제거했다. [설정·재시도 원장](runs.jsonl), [복구와 태그 대조](evidence/diagnostics.jsonl).

첫 재확인은 새 파일과 기존 파일 두 상태에서 의도 목록의 정확한 이름·개수와 저장 후 원시 픽셀 방향을 함께 확인하는 것이다. 해제 프로그램이나 로캘이 바뀌면 Unicode 경로를 하나 이상 별도로 읽는다. [재현](tools/replay.sh).

## 비용을 읽는 방법

링크 두 개는 반환 항목 수다. 정상 후보는 로컬 조합 2단계를 쓰고 이름·타입·픽셀을 재판독한다. 재생의 실제 명령 수, 입력·중간·가시 끝 경로 바이트 및 이전 품목 추가 여부는 시도별 원장에서 확인할 수 있다. 외부 문서 전송량과 도입 시간은 실측으로 채우지 않았다. [실측 비용 원장](evidence/costs.csv).
