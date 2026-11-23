# 삽입 위치와 토큰 경계 보조 실험

모든 Quarto 프로브는 행렬과 동일한 바이너리·옵션으로 새 경로에서 한 번 실행했다. 원시 [probes.jsonl](probes.jsonl)에 명령, 지문, 종료값과 PDF 판독을 연결했다. 직접 TeX 프로브도 같은 XeTeX·booktabs를 썼다.

| ID | 다른 입력 | 실측 및 판정을 바꾼 근거 |
| --- | --- | --- |
| P-LOCAL-Z, P-LOCAL-T | 본문 재정의와 첫 longtable을 하나의 `\begingroup … \endgroup`로 감싼 두 문서 | 첫 표 상·내·하 0/0/0, 둘째 1/1/1, 모든 값 보존. 그룹 종료는 두 번째 제목 전에 출력됐다. [Z 생성 tex](P-LOCAL-Z/document.tex#L143) · [T 생성 tex](P-LOCAL-T/document.tex#L143) · [대조 표](P-LOCAL-T/control.json) |
| P-HEADER-T, P-INCLUDE-T | 최상위 `header-includes` 블록, PDF 설정의 `include-in-header: {text: …}` | 둘 다 booktabs L55 뒤, 문서 시작 L142 앞의 L79–80에 정의가 놓였다. 두 표 모두 겉 두 선이 없어지고 둘째의 내부 1선과 셀은 남았다. [header-includes](P-HEADER-T/document.tex#L79) · [include-in-header](P-INCLUDE-T/document.tex#L79) |
| P-TRACE-T | 두 인수의 detokenized 문자열을 `\noalign` 안에서 로그로 쓴 별도 정의 | 두 표의 top·bottom에서 4회 모두 `A=[\noalign ] B=[]`가 기록됐다. [TeX 로그](P-TRACE-T/document.tex-log.txt#L813) · [계측 정의](../../fixtures/probes/trace-T.qmd) |
| P-TABULAR-O/Z/T | booktabs 원 규칙 호출 뒤에 빈 그룹 없는 셀, 선택 폭 또는 비어 있지 않은 noalign을 둔 원/무인수/두 인수 | O의 `Stable`은 Z에서 유지, T에서 `able`로 바뀌었다. 폭 표기 행은 O `Widths`, Z `[1.6pt] Widths`, T `.6pt] Widths`다. Before/After y 간격은 O 23.543, Z 19.955, T 11.955pt다. Z는 `\vskip 8bp`를 남기고 T는 그룹째 없앴다. 세 종료값 0. [O 원값](P-TABULAR-O/pdf-raw.json) · [Z 원값](P-TABULAR-Z/pdf-raw.json) · [T 원값](P-TABULAR-T/pdf-raw.json) |
| P-BARE-BOTTOM-O/Z/T | 맨 아래 `\bottomrule` 바로 다음에 `\end{tabular}` | O·Z는 종료 0과 PDF. T는 `\end`와 그룹을 소비하는 이 호출에서 `\begin{tabular} … ended by \end{document}` 오류, 종료 1, PDF 없음. [입력](../../fixtures/probes/bare-bottom.tex) · [오류 로그](P-BARE-BOTTOM-T/document.tex-log.txt) |

주 렌더의 `document.tex-log.txt`는 XeTeX 2차 패스가 기록한 로그다. 1차 패스 원로그는 그 렌더에서 덮였다. 6조건의 첫 반복에서 커밋된 TeX 그대로를 새 경로로 옮겨 같은 XeTeX 명령을 두 번 재생했다. 1차 6/6에 hyperref PageLabels, longtable 너비 변경 2줄, 교차 참조 경고가 있었고 2차 6/6에서 모두 사라졌다. 모든 종료값 0이다. [실제 재생 발췌](engine-replay.jsonl)
