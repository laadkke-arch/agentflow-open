# AF-RES-078 조합 검증 결과

## 표 1. 단계와 계약

| 단계 | 도구와 판 | 두 계약의 해당 근거절 | 입력 / 출력 역할 | 사용자 필수조건 | 깨지는 경계 |
| --- | --- | --- | --- | --- | --- |
| T front | SQLite CLI 3.46.1 Debian 3.46.1-7+deb13u2 | [T02 CLI §7.6](https://sqlite.org/cli.html#csv_export), [고정 output_csv](https://github.com/sqlite/sqlite/blob/version-3.46.1/src/shell.c.in#L2036-L2059) | read-only SQLite database → UTF-8 CSV with header | SQL 타입과 키, 인용 필드와 논리 행 수 | NULL 표기 충돌, TEXT 내부 NUL |
| T back | CPython csv 3.13.5 Debian 3.13.5-2+deb13u5 | [T04 v3.13.5 reader/QUOTE_NOTNULL](https://raw.githubusercontent.com/python/cpython/v3.13.5/Doc/library/csv.rst), [T05 판 변화](https://github.com/python/cpython/issues/113732) | UTF-8 CSV with exact keys → value-bearing rows recorded as JSONL | 같은 키의 NULL/빈 텍스트/리터럴과 쉼표·따옴표·줄바꿈 | 기본 문자열 읽기, 3.12 reader 차이, 헤더 없는 빈 결과 |
| I front | Pillow 13.0.0 on CPython 3.12.14 | [I01 exif_transpose](https://github.com/python-pillow/Pillow/blob/13.0.0/src/PIL/ImageOps.py#L690-L747), [스테이징](tools/convert.py) | source PNG under relative input tree → orientation-corrected RGB PNG under staging root | 원래 상대 식별자, 표시 크기와 픽셀 코너 | 스테이징 이름 충돌, 태그와 원시 픽셀 불일치 |
| I back | Info-ZIP Zip 3.0 Debian 3.0-15+deb13u1 | [I08 zip(1) -j/-@/add](https://manpages.debian.org/trixie/zip/zip.1.en.html), [I13 APPNOTE](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT) | relative staged PNG member list → ZIP central directory and payloads | 원 이름별 1회 읽기, 전체 멤버 수와 코너 유지 | basename 충돌, 기존 아카이브에 남은 멤버, 파일명 디코딩 |

## 표 2. 실행별 근거와 첫 손실

지문은 SHA-256 앞 12자리다. I의 입·중간 지문은 경로→개별 파일 SHA의 정렬 JSON 지문이다. 없음은 완성품 경로에 파일이 없음을, 이전은 현재 입력으로 게시된 파일이 아님을 뜻한다. 실행 링크에서 확정된 값·크기·모서리와 전체 지문을 읽을 수 있다.

| 분야 | 셀 | 시나리오 | run | 입력 / 중간 / 끝 지문 | 독립 정답 | 부품별 / 조합 판정 | 첫 손실 지점 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T | T00 | 정상 | [T00.normal.1](runs.jsonl#L27) | 5dabfdcb91b8 / a883a3255fd2 / b4f795bc540b | 8행·키별 타입/값(t-normal) | front=0 back=0 · 배제 | back/publication null |
| T | T00 | 정상 | [T00.normal.2](runs.jsonl#L28) | 5dabfdcb91b8 / a883a3255fd2 / b4f795bc540b | 8행·키별 타입/값(t-normal) | front=0 back=0 · 배제 | back/publication null |
| T | T00 | 봉인 경계 | [T00.edge.1](runs.jsonl#L25) | 83b200011722 / a0dce14b9a5e / b0cc423a623a | 8행·키별 타입/값(t-edge) | front=0 back=0 · 배제 | back/publication null |
| T | T00 | 봉인 경계 | [T00.edge.2](runs.jsonl#L26) | 83b200011722 / a0dce14b9a5e / b0cc423a623a | 8행·키별 타입/값(t-edge) | front=0 back=0 · 배제 | back/publication null |
| T | T00 | 중단·재시도 | [T00.retry.stop](runs.jsonl#L30) | 5dabfdcb91b8 / a883a3255fd2 / e8cefb7612b5 (이전) | 8행·키별 타입/값(t-normal) | front=0 back=-15 · 배제 | back/publication comma,empty,keys,literal,newline,null,quote,rows,text |
| T | T00 | 중단·재시도 | [T00.retry.resume](runs.jsonl#L29) | 5dabfdcb91b8 / a883a3255fd2 / b4f795bc540b | 8행·키별 타입/값(t-normal) | front=0 back=0 · 배제 | back/publication null |
| T | T01 | 정상 | [T01.normal.1](runs.jsonl#L33) | 5dabfdcb91b8 / a883a3255fd2 / 469a98220fd1 | 8행·키별 타입/값(t-normal) | front=0 back=0 · 지지 | 관측 없음 |
| T | T01 | 정상 | [T01.normal.2](runs.jsonl#L34) | 5dabfdcb91b8 / a883a3255fd2 / 469a98220fd1 | 8행·키별 타입/값(t-normal) | front=0 back=0 · 지지 | 관측 없음 |
| T | T01 | 봉인 경계 | [T01.edge.1](runs.jsonl#L31) | 83b200011722 / a0dce14b9a5e / 2b1b7138353a | 8행·키별 타입/값(t-edge) | front=0 back=0 · 지지 | 관측 없음 |
| T | T01 | 봉인 경계 | [T01.edge.2](runs.jsonl#L32) | 83b200011722 / a0dce14b9a5e / 2b1b7138353a | 8행·키별 타입/값(t-edge) | front=0 back=0 · 지지 | 관측 없음 |
| T | T01 | 중단·재시도 | [T01.retry.stop](runs.jsonl#L36) | 5dabfdcb91b8 / a883a3255fd2 / e8cefb7612b5 (이전) | 8행·키별 타입/값(t-normal) | front=0 back=-15 · 배제 | back/publication comma,empty,keys,literal,newline,null,quote,rows,text |
| T | T01 | 중단·재시도 | [T01.retry.resume](runs.jsonl#L35) | 5dabfdcb91b8 / a883a3255fd2 / 469a98220fd1 | 8행·키별 타입/값(t-normal) | front=0 back=0 · 지지 | 관측 없음 |
| T | T10 | 정상 | [T10.normal.1](runs.jsonl#L39) | 5dabfdcb91b8 / 2aa8396e5f0f / 34f52ed39152 | 8행·키별 타입/값(t-normal) | front=0 back=0 · 배제 | front null |
| T | T10 | 정상 | [T10.normal.2](runs.jsonl#L40) | 5dabfdcb91b8 / 2aa8396e5f0f / 34f52ed39152 | 8행·키별 타입/값(t-normal) | front=0 back=0 · 배제 | front null |
| T | T10 | 봉인 경계 | [T10.edge.1](runs.jsonl#L37) | 83b200011722 / b5f3e0298e38 / d01d8a9437f6 | 8행·키별 타입/값(t-edge) | front=0 back=0 · 배제 | front null |
| T | T10 | 봉인 경계 | [T10.edge.2](runs.jsonl#L38) | 83b200011722 / b5f3e0298e38 / d01d8a9437f6 | 8행·키별 타입/값(t-edge) | front=0 back=0 · 배제 | front null |
| T | T10 | 중단·재시도 | [T10.retry.stop](runs.jsonl#L42) | 5dabfdcb91b8 / 2aa8396e5f0f / e8cefb7612b5 (이전) | 8행·키별 타입/값(t-normal) | front=0 back=-15 · 배제 | back/publication comma,empty,keys,literal,newline,quote,rows,text / front null |
| T | T10 | 중단·재시도 | [T10.retry.resume](runs.jsonl#L41) | 5dabfdcb91b8 / 2aa8396e5f0f / 34f52ed39152 | 8행·키별 타입/값(t-normal) | front=0 back=0 · 배제 | front null |
| T | T11 | 정상 | [T11.normal.1](runs.jsonl#L45) | 5dabfdcb91b8 / 2aa8396e5f0f / 34f52ed39152 | 8행·키별 타입/값(t-normal) | front=0 back=0 · 배제 | front null |
| T | T11 | 정상 | [T11.normal.2](runs.jsonl#L46) | 5dabfdcb91b8 / 2aa8396e5f0f / 34f52ed39152 | 8행·키별 타입/값(t-normal) | front=0 back=0 · 배제 | front null |
| T | T11 | 봉인 경계 | [T11.edge.1](runs.jsonl#L43) | 83b200011722 / b5f3e0298e38 / d01d8a9437f6 | 8행·키별 타입/값(t-edge) | front=0 back=0 · 배제 | front null |
| T | T11 | 봉인 경계 | [T11.edge.2](runs.jsonl#L44) | 83b200011722 / b5f3e0298e38 / d01d8a9437f6 | 8행·키별 타입/값(t-edge) | front=0 back=0 · 배제 | front null |
| T | T11 | 중단·재시도 | [T11.retry.stop](runs.jsonl#L48) | 5dabfdcb91b8 / 2aa8396e5f0f / e8cefb7612b5 (이전) | 8행·키별 타입/값(t-normal) | front=0 back=-15 · 배제 | back/publication comma,empty,keys,literal,newline,quote,rows,text / front null |
| T | T11 | 중단·재시도 | [T11.retry.resume](runs.jsonl#L47) | 5dabfdcb91b8 / 2aa8396e5f0f / 34f52ed39152 | 8행·키별 타입/값(t-normal) | front=0 back=0 · 배제 | front null |
| I | I00 | 정상 | [I00.normal.1](runs.jsonl#L3) | f65ed941d4da / ca45197baa97 / a58995ee16bc | `a/photo.png` 7×5, `b/photo.png` 6×9·코너 | front=0 back=0 · 지지 | 관측 없음 |
| I | I00 | 정상 | [I00.normal.2](runs.jsonl#L4) | f65ed941d4da / ca45197baa97 / a58995ee16bc | `a/photo.png` 7×5, `b/photo.png` 6×9·코너 | front=0 back=0 · 지지 | 관측 없음 |
| I | I00 | 봉인 경계 | [I00.edge.1](runs.jsonl#L1) | 0d7fa0ca863e / 48af45c6ba6d / bc7cb44ab8eb | `a/é 541/photo.png` 7×5, `b/859/photo.png` 9×6·코너 | front=0 back=0 · 지지 | 관측 없음 |
| I | I00 | 봉인 경계 | [I00.edge.2](runs.jsonl#L2) | 0d7fa0ca863e / 48af45c6ba6d / bc7cb44ab8eb | `a/é 541/photo.png` 7×5, `b/859/photo.png` 9×6·코너 | front=0 back=0 · 지지 | 관측 없음 |
| I | I00 | 중단·재시도 | [I00.retry.stop](runs.jsonl#L6) | f65ed941d4da / ca45197baa97 / 2498ecd8a172 (이전) | `a/photo.png` 7×5, `b/photo.png` 6×9·코너 | front=0 back=9 · 배제 | back/publication extract,names,one_each,orientation,size |
| I | I00 | 중단·재시도 | [I00.retry.resume](runs.jsonl#L5) | f65ed941d4da / ca45197baa97 / a4b00fc475c9 | `a/photo.png` 7×5, `b/photo.png` 6×9·코너 | front=0 back=0 · 배제 | back/publication members,names |
| I | I01 | 정상 | [I01.normal.1](runs.jsonl#L9) | f65ed941d4da / ca45197baa97 / 없음 | `a/photo.png` 7×5, `b/photo.png` 6×9·코너 | front=0 back=16 · 배제 | back/publication extract,members,names,one_each,orientation,size |
| I | I01 | 정상 | [I01.normal.2](runs.jsonl#L10) | f65ed941d4da / ca45197baa97 / 없음 | `a/photo.png` 7×5, `b/photo.png` 6×9·코너 | front=0 back=16 · 배제 | back/publication extract,members,names,one_each,orientation,size |
| I | I01 | 봉인 경계 | [I01.edge.1](runs.jsonl#L7) | 0d7fa0ca863e / 48af45c6ba6d / 없음 | `a/é 541/photo.png` 7×5, `b/859/photo.png` 9×6·코너 | front=0 back=16 · 배제 | back/publication extract,members,names,one_each,orientation,size |
| I | I01 | 봉인 경계 | [I01.edge.2](runs.jsonl#L8) | 0d7fa0ca863e / 48af45c6ba6d / 없음 | `a/é 541/photo.png` 7×5, `b/859/photo.png` 9×6·코너 | front=0 back=16 · 배제 | back/publication extract,members,names,one_each,orientation,size |
| I | I01 | 중단·재시도 | [I01.retry.stop](runs.jsonl#L12) | f65ed941d4da / ca45197baa97 / 2498ecd8a172 (이전) | `a/photo.png` 7×5, `b/photo.png` 6×9·코너 | front=0 back=9 · 배제 | back/publication extract,names,one_each,orientation,size |
| I | I01 | 중단·재시도 | [I01.retry.resume](runs.jsonl#L11) | f65ed941d4da / ca45197baa97 / 2498ecd8a172 (이전) | `a/photo.png` 7×5, `b/photo.png` 6×9·코너 | front=0 back=16 · 배제 | back/publication extract,names,one_each,orientation,size |
| I | I10 | 정상 | [I10.normal.1](runs.jsonl#L15) | f65ed941d4da / 669e01bede73 / f841d79c6662 | `a/photo.png` 7×5, `b/photo.png` 6×9·코너 | front=0 back=0 · 배제 | front extract,members,names,one_each,orientation,size |
| I | I10 | 정상 | [I10.normal.2](runs.jsonl#L16) | f65ed941d4da / 669e01bede73 / f841d79c6662 | `a/photo.png` 7×5, `b/photo.png` 6×9·코너 | front=0 back=0 · 배제 | front extract,members,names,one_each,orientation,size |
| I | I10 | 봉인 경계 | [I10.edge.1](runs.jsonl#L13) | 0d7fa0ca863e / a145bfdff9e9 / 0930b3d01749 | `a/é 541/photo.png` 7×5, `b/859/photo.png` 9×6·코너 | front=0 back=0 · 배제 | front extract,members,names,one_each,orientation,size |
| I | I10 | 봉인 경계 | [I10.edge.2](runs.jsonl#L14) | 0d7fa0ca863e / a145bfdff9e9 / 0930b3d01749 | `a/é 541/photo.png` 7×5, `b/859/photo.png` 9×6·코너 | front=0 back=0 · 배제 | front extract,members,names,one_each,orientation,size |
| I | I10 | 중단·재시도 | [I10.retry.stop](runs.jsonl#L18) | f65ed941d4da / 669e01bede73 / 2498ecd8a172 (이전) | `a/photo.png` 7×5, `b/photo.png` 6×9·코너 | front=0 back=9 · 배제 | front extract,names,one_each,orientation,size |
| I | I10 | 중단·재시도 | [I10.retry.resume](runs.jsonl#L17) | f65ed941d4da / 669e01bede73 / a82f2936d669 | `a/photo.png` 7×5, `b/photo.png` 6×9·코너 | front=0 back=0 · 배제 | front extract,members,names,one_each,orientation,size |
| I | I11 | 정상 | [I11.normal.1](runs.jsonl#L21) | f65ed941d4da / 669e01bede73 / f841d79c6662 | `a/photo.png` 7×5, `b/photo.png` 6×9·코너 | front=0 back=0 · 배제 | front extract,members,names,one_each,orientation,size |
| I | I11 | 정상 | [I11.normal.2](runs.jsonl#L22) | f65ed941d4da / 669e01bede73 / f841d79c6662 | `a/photo.png` 7×5, `b/photo.png` 6×9·코너 | front=0 back=0 · 배제 | front extract,members,names,one_each,orientation,size |
| I | I11 | 봉인 경계 | [I11.edge.1](runs.jsonl#L19) | 0d7fa0ca863e / a145bfdff9e9 / 0930b3d01749 | `a/é 541/photo.png` 7×5, `b/859/photo.png` 9×6·코너 | front=0 back=0 · 배제 | front extract,members,names,one_each,orientation,size |
| I | I11 | 봉인 경계 | [I11.edge.2](runs.jsonl#L20) | 0d7fa0ca863e / a145bfdff9e9 / 0930b3d01749 | `a/é 541/photo.png` 7×5, `b/859/photo.png` 9×6·코너 | front=0 back=0 · 배제 | front extract,members,names,one_each,orientation,size |
| I | I11 | 중단·재시도 | [I11.retry.stop](runs.jsonl#L24) | f65ed941d4da / 669e01bede73 / 2498ecd8a172 (이전) | `a/photo.png` 7×5, `b/photo.png` 6×9·코너 | front=0 back=9 · 배제 | front extract,names,one_each,orientation,size |
| I | I11 | 중단·재시도 | [I11.retry.resume](runs.jsonl#L23) | f65ed941d4da / 669e01bede73 / a82f2936d669 | `a/photo.png` 7×5, `b/photo.png` 6×9·코너 | front=0 back=0 · 배제 | front extract,members,names,one_each,orientation,size |

## 표 3. 보기별 적격 분모와 비용

주 표본은 정상과 중단 후 재시도다. C의 주 진단은 같은 실행을 읽은 사후 결과다. 봉인 층의 C는 경계 입력 공개 전에 저장한 예측이다. 두 반복의 의미 판정이 다르면 해당 조건은 적격 분모에서 제외한다.

| 보기 | 평가층 | 적격 분모 | 참지지 / 참배제 / 거짓채택 / 거짓배제 / 보류 | 비용 |
| --- | --- | --- | --- | --- |
| A | I 봉인 예측 · 모두 충족 | 4/4 | 1 / 3 / 0 / 0 / 0 | 단독 4회 공유 |
| A | I 봉인 예측 · 요건 합산 | 24/24 | 6 / 9 / 9 / 0 / 0 | 단독 4회 공유 |
| A | T 봉인 예측 · 모두 충족 | 4/4 | 1 / 2 / 1 / 0 / 0 | 단독 4회 공유 |
| A | T 봉인 예측 · 요건 합산 | 36/36 | 33 / 2 / 1 / 0 / 0 | 단독 4회 공유 |
| A | I 주 예측 · 모두 충족 | 8/8 | 1 / 6 / 0 / 0 / 1 | 단독 4회 공유 |
| A | I 주 예측 · 요건 합산 | 48/48 | 6 / 18 / 9 / 0 / 15 | 단독 4회 공유 |
| A | T 주 예측 · 모두 충족 | 8/8 | 1 / 4 / 1 / 0 / 2 | 단독 4회 공유 |
| A | T 주 예측 · 요건 합산 | 72/72 | 33 / 4 / 1 / 0 / 34 | 단독 4회 공유 |
| B | I 봉인 예측 · 모두 충족 | 4/4 | 0 / 3 / 0 / 0 / 1 | 단독 4회 공유 + 계약 2행 |
| B | I 봉인 예측 · 요건 합산 | 24/24 | 3 / 18 / 0 / 0 / 3 | 단독 4회 공유 + 계약 2행 |
| B | T 봉인 예측 · 모두 충족 | 4/4 | 0 / 3 / 0 / 0 / 1 | 단독 4회 공유 + 계약 2행 |
| B | T 봉인 예측 · 요건 합산 | 36/36 | 29 / 3 / 0 / 0 / 4 | 단독 4회 공유 + 계약 2행 |
| B | I 주 예측 · 모두 충족 | 8/8 | 1 / 7 / 0 / 0 / 0 | 단독 4회 공유 + 계약 2행 |
| B | I 주 예측 · 요건 합산 | 48/48 | 10 / 38 / 0 / 0 / 0 | 단독 4회 공유 + 계약 2행 |
| B | T 주 예측 · 모두 충족 | 8/8 | 2 / 6 / 0 / 0 / 0 | 단독 4회 공유 + 계약 2행 |
| B | T 주 예측 · 요건 합산 | 72/72 | 66 / 6 / 0 / 0 / 0 | 단독 4회 공유 + 계약 2행 |
| C | I 봉인 예측 · 모두 충족 | 4/4 | 0 / 3 / 0 / 0 / 1 | 정상 기록 8행 재사용·예측 시 새 실행 0 |
| C | I 봉인 예측 · 요건 합산 | 24/24 | 3 / 18 / 0 / 0 / 3 | 정상 기록 8행 재사용·예측 시 새 실행 0 |
| C | T 봉인 예측 · 모두 충족 | 4/4 | 0 / 3 / 0 / 0 / 1 | 정상 기록 8행 재사용·예측 시 새 실행 0 |
| C | T 봉인 예측 · 요건 합산 | 36/36 | 29 / 3 / 0 / 0 / 4 | 정상 기록 8행 재사용·예측 시 새 실행 0 |
| C | I 주 사후 진단 · 모두 충족 | 8/8 | 1 / 7 / 0 / 0 / 0 | 주 16시도·32단계 실측 |
| C | I 주 사후 진단 · 요건 합산 | 48/48 | 10 / 38 / 0 / 0 / 0 | 주 16시도·32단계 실측 |
| C | T 주 사후 진단 · 모두 충족 | 8/8 | 2 / 6 / 0 / 0 / 0 | 주 16시도·32단계 실측 |
| C | T 주 사후 진단 · 요건 합산 | 72/72 | 66 / 6 / 0 / 0 / 0 | 주 16시도·32단계 실측 |

요건별 전체 행을 [evidence/counts.csv](evidence/counts.csv)에서, 개별 예측과 정답을 [comparisons.csv](comparisons.csv)에서 볼 수 있다.

## Q1. 사용자가 선택한 경계와 최소 반례

표의 작업은 이미 형식이 있는 SQLite의 행에서 시작한다. 범위의 끝은 정확한 키로 타입과 값을 다시 얻는 Python 행이다. JSONL은 그것을 검사하기 위한 기록이다. 이미지는 두 원본 PNG로 시작해 방향을 적용한 RGB 캐시를 만들고, 원래 상대 이름으로 하나씩 멤버를 풀어 읽는 데서 끝난다. RGBA→RGB와 두 파일의 마커는 통제 예시다. 각 원본에서 날짜·해시를 결론에 합치지 않고 디렉터리 전후 기록으로 원본 보존을 검사했다. [범위](SCOPE.md), [입력과 기대값](fixtures.jsonl), [실행](runs.jsonl).

| 최소 요구 | 가르는 가장 작은 입력 또는 변화 | 관측 범위 |
| --- | --- | --- |
| 행 키 | `001`을 숫자로 바꾸면 `1`과 구별할 수 없어진다. 개수는 하나여도 식별자가 변한다. | 설명용 반례. 본 입력의 키는 문자열로 직접 확인했다. |
| 행 수 | 한 데이터 행에서 줄바꿈이 든 인용 필드를 물리적 두 줄로 세면 행 수가 늘어난다. | r06 및 경계 개행 행을 논리 행 1개로 판독했다. |
| NULL / 빈 텍스트 / 리터럴 | 원본이 각각 SQL NULL, `""`, `NULL`인 세 키를 놓는다. 기본 reader는 앞의 두 값을 빈 문자열로 읽는다. `.nullvalue NULL`에서는 첫째와 셋째의 중간 필드가 모두 비인용 `NULL`이다. | T00·T10·T11 정상과 T01 대조. |
| 쉼표 / 큰따옴표 / 개행 | 한 값 `a,b`를 쉼표로만 자르면 열이 늘어났다. `a "quote"`에서 인용부호 하나를 버리면 값이 변한다. `a\r\nb`를 보편 개행 변환으로 읽으면 CR이 사라진다. | 부정 예시는 설명용이다. r04–r06과 별도 스캐너는 세 필드의 정확한 보존을 확인했다. |
| 그 밖의 텍스트 | `prefix\0suffix`는 SQL TEXT로 남지만 CLI CSV에는 `prefix`만 나온다. | T01.nul_text.1에서 양쪽 종료값 0, 텍스트만 불일치. |
| 원 상대 이름과 이름별 열기 | `a/photo.png`, `b/photo.png` 중 하나라도 디렉터리를 지우면 같은 입력 키로 다시 열 수 없다. | I01에서 ZIP 오류, I10/I11에서는 basename 하나만 게시. |
| 경로별 1개와 전체 멤버 수 | 이름이 맞는 두 멤버에 `old/previous.png`를 더하면 필수 두 경로를 하나씩 읽을 수 있어도 전체가 세 개다. 반대로 같은 이름을 두 번 쓰면 전체 수가 같아도 multiplicity가 달라진다. | I00.retry.resume의 잔존 멤버와 별도 이름별 검산. |
| 픽셀 크기 / 코너 방향 | 직사각형에 태그 6을 남긴 채 RGB 변환만 하면 크기 9×6과 원래 코너 배열이 유지된다. 180도나 좌우 반사는 크기에 변화 없이 배열만 바꿀 수 있다. | I00.raw_orientation_tag.1과 봉인 예시. |
| 원본 파일 | 결과를 원본 경로에 쓰면 이후 복구 입력이 손상된다. | 설명용 변경. 실제 실행은 읽기 전용 DB·별도 이미지 트리였으며 원본 지문 변화 0건이다. |

## Q2. 독립 시험과 연결 계약

각 설정에서 독립 표본 한 번씩, 총 8회를 실행했다. SQLite 두 출력에 같은 키의 SQL NULL과 빈 TEXT가 있었고 `.nullvalue NULL` 작성기 단독 시험에는 문자 그대로의 `NULL` 행을 넣지 않았다. Python의 손으로 쓴 CSV에는 비인용 빈 필드, 인용 빈 필드, 리터럴, 쉼표·인용·개행이 함께 있었다. 빈 필드 두 종류는 3.13.5의 QUOTE_NOTNULL에서만 다른 타입이었다. 작성기의 null 처리와 reader의 규칙을 대조할 때 이름이 같은 CSV만으로는 부족했다. 앞단은 현재 DB 유형이 있는 논리 행, 뒤는 UTF-8 CSV 레코드와 인용 상태가 단위다. [단독 실행](evidence/solo.jsonl), [T04 v3.13.5](https://raw.githubusercontent.com/python/cpython/v3.13.5/Doc/library/csv.rst), [SQLite 고정 3.46.1 구현](https://github.com/sqlite/sqlite/blob/version-3.46.1/src/shell.c.in#L2036-L2059).

Pillow 단독 두 설정은 9×6 태그 6의 PNG를 6×9로 바꾸었고, Zip 단독 두 설정은 수동 공급한 동일 이미지의 9×6 원시 픽셀과 태그 6을 건드리지 않았다. 한 파일만 있으므로 앞뒤 단독 성공에서는 이름 충돌을 볼 수 없었다. 변환 단위는 파일과 래스터이고 묶는 단위는 경로가 있는 멤버와 목록 전체다. 스테이징이 어느 디렉터리를 기준으로 목록을 건네는지, Zip이 어떤 이름과 기존 엔트리로 게시하는지 연결해야 한다. [실행판 API](https://github.com/python-pillow/Pillow/blob/13.0.0/src/PIL/ImageOps.py#L690-L747), [Zip 3.0 add와 -j](https://manpages.debian.org/trixie/zip/zip.1.en.html).

판 이름만으로 되돌림을 추론할 수 없었다. 수동 CSV 바이트를 같은 QUOTE_NOTNULL 이름의 3.12.14에서 실행하니 성공 종료하면서 비인용 빈 필드를 빈 문자열로 냈다. 3.13.5 단독 행은 None을 냈다. Pillow 7.1.0의 수동 회전 뒤 태그 잔존 보고와 8.2.0 exif_transpose의 원 객체 수정 보고는 각각 다른 실패다. 8.3.0의 TIFF KeyError와 수정을 별도로 읽었고 연관 계보의 수는 올리지 않았다. SQLite의 마지막 빈 필드 EOF 사건은 import 경로로 범위를 한정했다. [버전 대조](evidence/diagnostics.jsonl), [CPython #113732](https://github.com/python/cpython/issues/113732), [Pillow #4537](https://github.com/python-pillow/Pillow/issues/4537), [Pillow #5546](https://github.com/python-pillow/Pillow/issues/5546), [Pillow #5580](https://github.com/python-pillow/Pillow/issues/5580), [SQLite 수정](https://www.sqlite.org/src/info/6f7842f577a28df1).

## Q3. 설정 하나만 바꾼 짝

| 한 설정만 바꾼 짝 | 같은 입력 및 부작용 | 판정 |
| --- | --- | --- |
| T00→T01 reader만 | 정상·경계의 CSV 자체는 바이트 동일하다. 비인용 빈 필드의 타입 하나가 바뀌어 그 키의 SQL NULL을 복원한다. | 원 결합의 성공을 뒤집는 설정이다. |
| T10→T11 reader만 | 작성기가 SQL NULL과 리터럴을 같은 필드로 내보낸 뒤에는 둘 다 문자열 `NULL`이다. 정상에서 JSONL도 동일하다. | 이미 잃은 정보에 대한 무변화다. |
| T00→T10 null 표기만 | NULL 키의 값은 빈 문자열에서 문자열 `NULL`로 변했다. 어느 쪽도 SQL NULL 회복에는 부족했다. | 결과 바이트 변화와 목적 실패가 함께 있다. |
| T01→T11 null 표기만 | reader가 보는 비인용 빈 필드를 비인용 `NULL`로 바꾼다. 리터럴도 `NULL`이다. | reader의 복구 규칙을 앞단 변경이 무력화한다. |
| I00→I01 ZIP만 | 같은 경로·픽셀 중간품 2개에서 `-j`가 두 이름을 `photo.png`로 바꾼다. Zip은 16으로 실패한다. | 앞단은 멤버 2개를 보존했고 뒤에서 실패했다. |
| I00→I10 스테이징만 | 두 원본이 동일 staging 경로로 쓰이는 과정에서 첫 정체성이 사라지고 최종 멤버 하나만 남는다. | 실행 성공과 필수조건 실패가 공존한다. |
| I10→I11 ZIP만 | 이미 평탄화된 `photo.png` 하나에는 버릴 경로가 없었다. 정상과 경계에서 각각 ZIP 바이트도 동일했다. | 같은 필드에 두 조작을 해도 이미 작용한 단계 뒤에는 중복이다. |
| I01→I11 스테이징만 | 뒤의 이름 충돌 오류가 사라지지만 그 전에 이미지 하나가 덮였다. | 경고·실패의 상쇄는 사용자 목적을 회복시키지 않는다. |

I00의 `same_meaning_different_dates`는 ZIP 시간이 바뀌어 아카이브 해시가 다르지만, 같은 두 파일의 디코딩과 코너 판정은 그대로였다. T10/T11의 바이트 동일과 I10/I11의 동일은 공통 실패와도 양립한다. 경계의 이름은 분해형 e+결합 악센트와 공백을 갖는다. 설치판이 해당 엔트리에 UTF-8 bit 11을 세웠고 Python 조회와 UnZip 출력은 원 상대경로를 돌려줬다. 같은 입력에서 `-UN=n` 및 명시적 `metadata_encoding="utf-8"` 대조도 변화를 관측하지 못했다. [실행 짝](runs.jsonl), [추가 시험](evidence/diagnostics.jsonl), [APPNOTE §4.6.9](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT).

## Q4. 링크, 계약, 실제 연결의 판별력

주 표본은 분야별 **8개 셀×시나리오**이며 A·B의 판단은 합성 실행 전에 고정했다. 실제 전체 지지는 T 2/8, I 1/8이다. T에서 A는 T11을 하나 잘못 채택했고 두 번 보류했다. I의 전체 판정에서 A의 거짓 채택은 0/8이지만, 개별 요건에서 A는 멤버 수·크기·모서리를 9/48번 잘못 지지했다. B는 실제로 관측한 충돌과 기본 add의 잔존 상태를 구별해 주 표본 16개 전체 판정 및 120개 개별 요건에서 거짓 채택·거짓 배제·보류가 없었다. 해당 C열은 독립 기준으로 동일 실행을 판독한 진단이다. 미래 입력의 정확도로 환산할 수 없다. [사전 예측](predictions.csv), [요건별 분자·분모](evidence/counts.csv).

봉인 표본은 분야별 생성 픽스처 하나를 네 셀에 적용한 **4개 셀×시나리오씩**이다. T01과 I00만 지지됐다. T에서는 A가 T11을 1/4 거짓 채택했다. I에서는 A가 전체를 4/4 맞혔지만 개별 요건에선 9/24를 거짓 채택했다. B와 새 입력 C는 각각 T와 I에서 전체 양성 1개씩을 보류했고 거짓 채택·거짓 배제는 0이었다. 이번 T 경계 seed는 NUL 없는 “行:…”를 선택했고 I 경계의 UTF-8 플래그도 작동했다. 보류한 정답 2개를 성공 예측으로 올리지 않았다. B와 C의 봉인 숫자가 같은 상황은 정상 짝의 관측이 사전 계약을 확인했어도 새 문자열/이름 속성을 직접 확인하기 전에는 추가 결론이 없을 수 있음을 보여 준다. 판단을 억지로 채택 또는 배제로 채울 이유는 없다. [C의 별도 사전 답](evidence/c-heldout-predictions.csv), [시드 봉인](evidence/seed-seal.json), [시드 공개](evidence/seed-reveal.json), [A/B/C 원장](comparisons.csv).

적격 분모에는 독립 정답이 알려진 보류를 넣었다. 상태가 서로 다른 반복은 해당 요건에서 미적격이고 여기서는 0개다. 다른 실행의 긍정 요건을 서로 더하지 않았다. I01의 실패 후 이전 ZIP에 두 멤버가 있다는 관측은 현재 작업의 멤버 수 충족으로 득점하지 않았다. 이번 실제 요건 판정에서 근거가 상충한 실행은 0개다. 플랫폼·판이 달라지는 원문 사례와 실제 종료값과 의미 일치의 차이는 독립적으로 기록했다. 출처·환경·입력 미확인 시 추천 상태는 보류한다. [중단 로그](runs.jsonl), [타입과 바이트 오라클](tools/oracle.py).

## Q5. 중단, 빈 결과, 재제출

| 가지 | 실제 중단 직후 | 같은 요청 재제출 |
| --- | --- | --- |
| T00–T11 | 앞 CSV가 이미 기록돼 있다. reader의 첫 행 flush+fsync 지점에서 SIGTERM 후 Python 종료 -15. `final.part`는 남았고 49바이트의 이전 JSONL 지문은 4/4 동일했다. | 쓰기 모드로 기존 `.part`를 잘라 재작성하고 `os.replace`한다. 새 키 8개가 각 1개이며 이전 키는 없다. 별도로 T00/T10/T11의 NULL 문제는 반복됐다. |
| I00 | Info-ZIP PID의 `anon_pipe_read` 확인 뒤 EOF 전에 SIGTERM. native 종료 9. 중간 PNG 2개와 이전 ZIP을 보존했고 새 ZIP 임시 파일은 없었다. | 같은 키 `a/photo.png`의 이전 내용은 갱신됐다. 추가된 `b/photo.png`와 오래된 `old/previous.png`까지 3개가 되었다. 두 필수 키 각각은 읽힌다. |
| I01 | 같은 이전 ZIP과 중간 PNG 2개. native 종료 9, 임시 파일 없음. | `-j`가 충돌을 드러내 종료 16. 이전 ZIP 지문을 그대로 얻었으며 현재 목록을 게시하지 않았다. |
| I10/I11 | 이전 ZIP과 평탄화 뒤 PNG 하나가 남는다. native 종료 9, 임시 파일 없음. | 앞단의 덮어쓰기를 반복한다. ZIP은 기본 add로 이전 두 엔트리와 새 basename을 함께 보존한다. 현재 이미지 2개를 원래 이름으로 회복할 수 없다. |

ZIP에서 쓰기가 진행된 이후의 별도 보강은 원 격자의 `-@` 대기보다 늦은 지점이다. 실제 FIFO를 읽도록 한 native Zip이 65,536바이트의 임시 파일을 만든 뒤 같은 형태의 새 두 디렉터리에서 신호를 보냈다. SIGTERM은 종료 9 및 임시품 삭제, SIGKILL은 종료 -9 및 임시품 잔존을 보였고 이전 완성품은 두 경우 모두 바이트 동일했다. 실제 신호를 썼으며 FIFO는 중단 위치를 제어하는 테스트 입력이다. 서버 장애나 전원 장애를 재현하지 않았다. [추가 실행](evidence/diagnostics.jsonl), [Zip -b/-FI/종료값](https://manpages.debian.org/trixie/zip/zip.1.en.html), [Linux rename](https://man7.org/linux/man-pages/man2/rename.2.html#DESCRIPTION).

SQLite의 0행 조회는 종료 0이어도 CLI 교환 바이트가 0이었다. Python은 헤더 누락으로 종료 1이었고 완성품이 없었다. 존재하지 않는 열의 질의는 똑같이 0 교환 바이트를 냈지만 CLI 종료 1이고 reader 호출이 없었다. 명시적 13바이트 헤더를 준 `zero_framed`는 reader 종료 0, **실제 존재하는 0바이트 JSONL**, 독립 정답 0행이었다. 파일 묶음에서 단독 Zip은 입력 목록 0개로 종료 12 및 파일 부재를 보였다. 별도로 stdlib가 만든 22바이트 ZIP은 중앙 목록이 비어 있는 유효한 완료품이다. 0바이트, 파일 없음, 이전 산출물, 빈 중앙 목록을 서로 같은 상태로 취급할 수 없다. [진단 실행](evidence/diagnostics.jsonl).

## Q6. 가장 작은 복구와 별도 조합

- **설정 하나.** NUL이 없는 입력에서 T00→T01은 Python의 quoting만 바꿔 타입을 살렸다. T11→T01은 앞단 null 표기만 바꿔 같은 요구를 충족했다. I01→I00의 -j 제거는 새 ZIP에서 원 이름을 회복했다. I11→I10은 이미 덮인 앞단 때문에 무효였다. 기존 ZIP이 있는 I00 재시도에 -FS 한 옵션을 넣으면 별도 실행에서 2개가 남았고 과거 전용 키가 없어졌다. 이 시험은 대상 stage 목록이 완전하며 이전 전용 멤버를 삭제해도 되는 통제 목적이다. [설정 격자](runs.jsonl), [I00.sync_adapter.resume](evidence/diagnostics.jsonl), [Zip -FS](https://manpages.debian.org/trixie/zip/zip.1.en.html).
- **명시적 어댑터.** `prefix\0suffix`가 든 동일 DB를 SQL로 `N` 또는 `T`와 BLOB hex로 내보내고 Python에서 타입을 확인해 디코딩했다. T01의 실측 중간 126바이트·실패를 T00.typed_adapter.1의 188바이트·전체 지지로 바꿨다. 원래 T01의 점수는 유지한다. 파일은 의도 목록으로 새 ZIP을 만든 뒤 한 번 교체하는 별도 어댑터가 I00 재시도의 과거 전용 멤버를 제거했다. `-FS`와 새 ZIP 경로 모두 정상 ZIP과 같은 의미였다. [typed·fresh 실행](evidence/diagnostics.jsonl).
- **사용자 목적 변경.** NULL과 빈 문자열의 구별이 필요 없거나, 이름으로 되돌려 읽기 대신 basename 하나만을 고르거나, EXIF 우선 표시를 허용한다면 평가 계약 자체가 달라진다. 픽셀은 그대로이고 태그만 보존한 `raw_orientation_tag`는 이번 방향 요구를 실패했다. 강제로 태그 6을 다시 붙인 `stale_orientation_tag`는 이번 원시 코너 요구는 맞았으나 태그를 소비하는 별도 뷰어에서는 이중 정규화 가능성이 있다. 그 뷰어의 거동은 이 실행의 PNG 태그/픽셀 관측과 구별한다. [PNG eXIf](https://www.w3.org/TR/2025/REC-png-3-20250624/#eXIf), [방향 진단](evidence/diagnostics.jsonl).

## Q7. 링크 두 개와 첫 재확인

각 카드에는 앞뒤 구현으로 바로 가는 두 링크, 연결 옵션, 확인한 최소 입력, 실패 및 재시도 전제를 한꺼번에 담았다. 표는 T01에서 세 타입을 표기한 행과 인용 개행 한 행을 실제 데이터에서 먼저 확인한다. 파일은 fresh I00에서 상대경로별 하나를 열고 이름과 픽셀 코너를 본다. 기존 묶음에 갱신한다면 I00 재시도의 오래된 엔트리까지 함께 검사한다. [반환 카드](cards.md).

| 비용 항목 | 이 환경의 실측 | 그 값에서 추정할 수 있는 범위 |
| --- | --- | --- |
| 링크/요청 | 카드별 실행 대상 링크 2개. 원문 원장 39개 행 중 독립 산입 25개. 오프라인 격자 48개 시도의 외부 서비스 호출 0개. | 제품이 새 요청에서 링크를 열어 계약을 읽으면 카드당 최소 두 문서 열람이 필요할 수 있다. 실제 HTTP 리다이렉트·캐시·전송량, 사용자 왕복과 소요시간은 미측정이다. |
| 단계 | 기존 단독 8개 프로세스. 격자는 앞뒤 96개 프로세스, 과거 품목 설정 8개, 별도 UnZip 이름 검사 20개로 총 124개. 별도 진단 18개 행·44개 프로세스. | 깨끗한 조합 하나는 앞뒤 2단계와 최소 독립 검사 1회, 정상·경계를 두 번씩 보면 실행 4회라는 계획 비용을 계산할 수 있다. 중단 지점과 기존 산출물에서 검사 비용이 추가된다. |
| 바이트 | T01 정상은 DB 12,288→CSV 129→새 JSONL 284바이트. I00 정상은 원본 267→스테이징 260→ZIP 454바이트. T01 봉인 12,288→164→318, I00 봉인 267→248→467바이트였다. | 실사용 파일의 바이트 비용은 중간 표현·중복·압축률·DB 페이지 크기에 의존한다. 아래 수치는 같은 샘플의 반복을 포함한 합계다. |

전체 주·봉인·재시도 시도에서 T의 교환 파일 합 3,424바이트와 보인 완료 경로 합 6,158바이트, I의 중간 PNG 합 4,564바이트와 완료 경로 합 8,069바이트를 기록했다. 완료 경로 합계에는 중단/실패 후 남은 과거 출력(T 196, I 2,355바이트)이 포함된다. 새로 게시된 바이트만 보려면 각각 5,962 및 5,714바이트다. 인메모리 DB 생성·ZIP 해제와 독립 PNG 디코딩은 별도 프로세스 수로 세지 않았다. [시도별 비용](evidence/costs.csv), [런타임 판](evidence/runtime-versions.json).

## 다른 분야의 원자료와 교차 검토

PostgreSQL COPY는 표기 토큰에 맞는 실제 텍스트를 인용하는 계약을 제공한다. SQLite의 단순 nullValue 표기와 달리 그 표현에서 두 값이 구별된다. Arrow는 문자열 null 검출과 인용된 문자열 null을 별도 옵션으로 두며 W3C 모델은 원 셀 문자열과 해석값을 분리한다. 이 차이 때문에 두 CSV 관련 링크의 표현을 한 규칙으로 합치면 안 된다. [PostgreSQL COPY](https://www.postgresql.org/docs/17/sql-copy.html#SQL-COPY-NOTES), [Arrow ConvertOptions](https://arrow.apache.org/docs/python/generated/pyarrow.csv.ConvertOptions.html), [W3C Tabular Data Model](https://www.w3.org/TR/2015/REC-tabular-data-model-20151217/#cells).

Git 아카이브는 추적 경로에 prefix를 붙이는 방식과 외부 파일을 basename으로 추가하는 방식을 명시적으로 갈라준다. S3는 키 존재 또는 ETag를 게시 전제에 포함해 이전 성공물이 남아 있는 상태를 고객의 조건으로 노출한다. 미 의회도서관은 카메라 원형 파일에서 Exif를 발견했으나 세부 판을 모르는 실제 수장 상황을 기록한다. 세 경우 모두 파일 형식이 맞는지만으로 이름·게시·메타데이터 목적을 판정할 수 없다. 이 연구에서 세 외부 서비스를 재현하거나 운영 자원을 사용하지 않았다. [Git 2.46 git-archive](https://git-scm.com/docs/git-archive/2.46.0), [S3 게시 조건](https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html), [Library of Congress Exif 기록](https://www.loc.gov/preservation/digital/formats/fdd/fdd000146.shtml).

25개 독립 원문은 표 11, 이미지·ZIP 10, 교차 분야 4개다. 직접 확인한 독립 실패·판 변화 원사건은 5개이며 연결된 PR·공식 회귀·미러는 산입 수를 늘리지 않았다. 동일한 SQLite 간단 출력과 Pillow 정상 회전이 충분하다는 초기 가능성을 각각 NUL 무음 절단과 동명 경로·이전 아카이브 상태에서 다시 시험했다. 반대로 단독 근거가 항상 틀린다는 주장도 I 분야 A의 봉인 전체 판정과 정상 T01에서 반박된다. [출처 원장](sources.jsonl), [검색 실패와 회수](search-log.jsonl), [자체 점검](SELF_CHECK.md).

## 불일치와 약점 세 가지

| 약점 | 다음 조사와 판단이 바뀌는 관측 |
| --- | --- |
| 1. 통제 격자는 분야별 정상 1개와 봉인 1개를 재사용했다. 같은 작업자가 열람·예측·재판독했고 이번 T 봉인 입력에는 NUL이 없었다. | 서로 다른 원본 집합과 작성자가 눈가림 상태로 예측하도록 새로 봉인한다. 정해진 B/C 계약이 NUL 여부가 다른 새 픽스처에서도 보류·거짓 채택을 어떻게 바꾸는지 센다. |
| 2. 재시도는 Linux 같은 파일시스템에서 순차로 한 번만 보냈다. Zip의 -@ 대기와 FIFO 쓰기 중 신호는 각각 관측했지만 게시 시점의 동시 작성자 및 전원 장애는 미확인이다. | 같은 이전 ZIP·JSONL과 동일 새 입력 두 제출을 준비하고 게시 직전/직후를 제어한다. 내용 해시와 경로별 중복, 디렉터리 fsync 뒤의 내구성이 동시 정책별로 달라지면 재시도 계약을 수정한다. |
| 3. 픽셀 오라클은 RGB/RGBA PNG와 네 모서리에 한정하고 이름 판독은 지정 Linux 소비자에서 했다. 태그 6과 이미 회전한 픽셀을 함께 받은 실제 의도 뷰어 및 다른 ZIP 이름 해석기는 범위 밖이다. | 같은 봉인 PNG/ZIP으로 실사용 뷰어와 압축 해제기를 열어 경로 코드점·방향·이미지 크기를 확인한다. 태그 우선 뷰어의 결과나 ZIP 이름이 달라지면 카드의 입출력 조건과 필수 판정 규칙을 바꾼다. |
