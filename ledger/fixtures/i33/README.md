# I33 판정(08 I33)

`judgments.tsv`는 여섯 설정(r2, r5, r6, 각각 012 p5 꼬리표 끔·켬)의 상위 10 합집합에서 I25·I27·I32에 없던 396쌍의 판정이다(실제 행 2만 개 278, link-index 118).
규칙은 `measure.I33_JUDGE_RULE`(판정 전에 적음). 등급은 I25와 같다. 판정자는 이 세션의 모델이다(사람 판정 아님).

- `level`: catalog 대상의 확인 단계(L1 병합만, L2 주소 살아 있음, L3 인용이 원문에 있음, L4 교차 확인). 대상이 없는 link-index 행은 L1로 적었다.
- `original`: opensource `captures` 가지에서 그 주소의 원문을 봤는지. 판정 때 가지(커밋 `618e8ce`)에는 원문 본문(`http/`)이 아직 없어 모두 `none`이다. 원문 전체 사본은 opensource 밖에 두지 않으므로 이 저장소에는 복사하지 않는다(`measure.capture_text`는 로컬 클론에서만 읽는다).
