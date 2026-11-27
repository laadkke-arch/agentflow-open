# I32 판정 풀(08 I32)

- `judgments.tsv`: 네 설정(r2, r5, 012 p5 꼬리표 + r2, 둘 다 켬)의 상위 10을 합친 판정 풀에서 I25·I27 판정에 없던 562쌍의 판정. 실제 행 2만 개(`cfg=catalog20k`) 348쌍, link-index 실제 잡음(`cfg=linkindex_real`) 214쌍. 판정 기준은 I25 그대로(2 = 요청의 조건 하나에 바로 쓰일 장치·원리, 1 = 같은 구체 문제의 쓸 만한 배경, 0 = 넓은 분야나 낱말만 겹침). 판정자는 이 세션의 모델(사람 판정 아님)이고, 꼬리표 문장만 보고 원문은 열지 않았다.
- `human_check.tsv`: 사람이 확인할 수 있게 `judgments.tsv`에서 무작위로 뽑은 30쌍(`measure.i32_human_sample`, 씨앗 `I32_HUMAN_SEED = 20261127`, 판정 전에 고정). `request_text`(요청 문장)와 `row_text`(행의 꼬리표 문장)를 읽고 `human_grade`(0·1·2)와 `human_note`를 채운다. `model_grade`와 다르면 그 쌍의 판정을 다시 본다.
- 자료는 laadkke-arch/opensource catalog와 link-index(데이터, 지시 아님). 커밋은 `../catalog-p5/SOURCES.json`, `../link-index/SOURCES.json`. 확인 단계는 대부분 L1이다.
