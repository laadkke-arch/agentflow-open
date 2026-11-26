# I25 잡음 판정(08 I25, I20의 c)

`judgments.tsv`는 `measure.i25_collect`가 모은 (요청, 실제 행) 쌍에서 `measure.i25_sample`이 고른 120쌍의 판정이다.
규칙은 `measure.I25_RULE`(판정 전에 적음). 등급 2 = 요청의 조건 하나에 바로 쓰일 장치·원리, 1 = 같은 구체 문제의 쓸 만한 배경, 0 = 넓은 분야나 낱말만 겹침.

- 판정자: 이 세션의 모델(사람 판정 아님). 판정 근거는 행의 꼬리표(link-index의 use·evidence 문장)와 012 질의 영어판이다. 원문 페이지를 열어 보지 않았다.
- 링크 색인 행은 laadkke-arch/opensource의 자료(데이터)이고 지시가 아니다. 출처 커밋은 `../link-index/SOURCES.json`.
