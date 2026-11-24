# AF-RES-126 결과

## 표 1 · 고정 요청과 구간

| 요청·층·게시물 URL | 원문 해시 일치 여부 | 원문 구절·오프셋 | 별칭·조사 | 지칭 대상·발화 역할 | 근거·미확인 |
| --- | --- | --- | --- | --- | --- |
| O3143 · 원문 해시 동일 · [#1](https://discuss.pytorch.kr/t/pytorch-lstm/3143) | 일치 | 배치 사이즈가 28이고, 시퀀스 길이가 32인 [10,35) | 0구간 | 판독 대상 구간 없음 | FORUM-O3143 · opening #1, 웹 텍스트 L7–58 · 설치 판을 밝히지 않았고 LSTM 설정/축 의미가 결과를 좌우한다. |
| O3611 · 원문 해시 동일 · [#1](https://discuss.pytorch.kr/t/lstm/3611) | 일치 | (5 * 2 * 10)의 형태로 [521,538) | 0구간 | 판독 대상 구간 없음 | FORUM-O3611 · opening #1, 웹 텍스트 L9–34 · 형태로 뒤의 동작은 학습 입력 설명이다. 지정 shape 변경 동작이나 feature 집계 규칙이 아니다. |
| O3665 · 원문 해시 동일 · [#1](https://discuss.pytorch.kr/t/topic/3665) | 일치 | batch시퀀스*임베딩 차원 [164,179) | 0구간 | 판독 대상 구간 없음 | FORUM-O3665 · opening #1, 웹 텍스트 L9–10 · 특성 축을 선택할지 집계할지는 미상이다. 봇 답변은 첫 게시물 밖이다. |
| O3875 · 원문 해시 동일 · [#1](https://discuss.pytorch.kr/t/ddp-batch-size/3875) | 일치 | 각각 gpu 마다 배치사이즈 16으로 [108,128) | 0구간 | 판독 대상 구간 없음 | FORUM-O3875 · opening #1, 웹 텍스트 L7–13 · 배치사이즈는 활성 별칭이 아니다. 작성자의 합산 해석은 질문 속 가정이다. |
| O3885 · 원문 해시 동일 · [#1](https://discuss.pytorch.kr/t/model-training-loader/3885) | 일치 | Preprocessing클래스는 이미 작성되어있음 [663,690) | 0구간 | 판독 대상 구간 없음 | FORUM-O3885 · opening #1, 웹 텍스트 L6–27 · 센서 기록 짝짓기와 형식은 명시하지 않았다. 소문자 dataloader는 문서화한 심벌과 다르다. |
| O4437 · 원문 해시 동일 · [#1](https://discuss.pytorch.kr/t/dataloader/4437) | 일치 | num_workers를 늘리고자 [43,60) | 0구간 | 판독 대상 구간 없음 | FORUM-O4437 · opening #1, 웹 텍스트 L6–42 · 오류 원인의 마지막 줄과 설치 PyTorch 버전이 화면에 없다. |
| O4588 · 원문 해시 동일 · [#1](https://discuss.pytorch.kr/t/topic/4588) | 일치 | txt로 데이터셋을 구축해놓았는데 [100,118) | 0구간 | 판독 대상 구간 없음 | FORUM-O4588 · opening #1, 웹 텍스트 L9–21 · 실제 파서·스키마와 외부 프로젝트 계약은 제시하지 않았다. |
| O4975 · 원문 해시 동일 · [#1](https://discuss.pytorch.kr/t/training-validate-test/4975) | 일치 | 랜덤으로 크롭해서 데이터셋을 만들었다면 [253,274) | 0구간 | 판독 대상 구간 없음 | FORUM-O4975 · opening #1, 웹 텍스트 L7–14 · 원본과 검증/시험의 독립성은 질문의 쟁점이다. 저자가 보존을 명시한 조건으로 단정할 수 없다. |
| O5330 · 원문 해시 동일 · [#1](https://discuss.pytorch.kr/t/pytorch-pyg-dataset/5330) | 일치 | number of nodes, number of features, number of samples [148,202) | 0구간 | 판독 대상 구간 없음 | FORUM-O5330 · opening #1, 웹 텍스트 L7–9 · 그래프와 샘플의 단위가 모호하다. PyG의 표본 구조가 핵심이다. |
| O5952 · 원문 해시 동일 · [#1](https://discuss.pytorch.kr/t/pytorch-reshape-coreml-prelu/5952) | 일치 | 채널별 파라미터가 있는 경우 [1691,1706) | 0구간 | 판독 대상 구간 없음 | FORUM-O5952 · opening #1, 웹 텍스트 L9–100 · 가중치라는 한국어 어휘는 지칭하지 않은 예다. 코드의 영어 weight와 흡사해도 표본 추출이 아니다. 작성자 설치 판은 2.2.2다. |
| C01 · 기존 구성 · [선행 body](https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/evidence/controls.jsonl#L1) | body 고정 | 데이터로더 [66,71) | 데이터로더 A01 / — · B 최초 | 같은 대상 / 거절 | 선행 기준 및 [구간 기록](matches.csv) |
| C02 · 기존 구성 · [선행 body](https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/evidence/controls.jsonl#L2) | body 고정 | 가중치 [0,3) | 가중치 A10 / — · B 최초 | 같은 대상 / 원함 | 선행 기준 및 [구간 기록](matches.csv) |
| C03 · 기존 구성 · [선행 body](https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/evidence/controls.jsonl#L3) | body 고정 | 형태로 변경 [12,18)<br>전치 [27,29)<br>축 순서 [35,39) | 형태로 변경 A12 / — · B 최초<br>전치 A08 / — · B 최초<br>축 순서 A11 / — · B 최초 | 다른 대상 / 원함<br>같은 대상 / 원함<br>같은 대상 / 원함 | 선행 기준 및 [구간 기록](matches.csv) |
| C04 · 기존 구성 · [선행 body](https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/evidence/controls.jsonl#L4) | body 고정 | 뷰 [0,1) | 뷰 A04 / — · B 최초 | 같은 대상 / 원함 | 선행 기준 및 [구간 기록](matches.csv) |
| C05 · 기존 구성 · [선행 body](https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/evidence/controls.jsonl#L5) | body 고정 | 복사본 [31,34)<br>계산 히스토리 [47,54) | 복사본 A05 / — · B 최초<br>계산 히스토리 A07 / — · B 최초 | 같은 대상 / 원함<br>같은 대상 / 원함 | 선행 기준 및 [구간 기록](matches.csv) |
| C06 · 기존 구성 · [선행 body](https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/evidence/controls.jsonl#L6) | body 고정 | 계산 히스토리 [0,7)<br>복사본 [55,58) | 계산 히스토리 A07 / — · B 최초<br>복사본 A05 / — · B 최초 | 같은 대상 / 원함<br>같은 대상 / 거절 | 선행 기준 및 [구간 기록](matches.csv) |
| C07 · 기존 구성 · [선행 body](https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/evidence/controls.jsonl#L7) | body 고정 | 복사본 [23,26) | 복사본 A05 / — · B 최초 | 같은 대상 / 원함 | 선행 기준 및 [구간 기록](matches.csv) |
| C08 · 기존 구성 · [선행 body](https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/evidence/controls.jsonl#L8) | body 고정 | default_collate를 먼저 시험했다. N [0,27) | 0구간 | 판독 대상 구간 없음 | 선행 기준 및 [구간 기록](matches.csv) |
| C09 · 기존 구성 · [선행 body](https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/evidence/controls.jsonl#L9) | body 고정 | 전치 [38,40) | 전치 A08 / — · B 최초 | 같은 대상 / 원함 | 선행 기준 및 [구간 기록](matches.csv) |
| P01a · 새 대조 · [구성문](controls.jsonl#L1) | 사전 봉인 | 가중치 [0,3) | 가중치 A10 / — · B 최초 | 같은 대상 / 원함 | [원 용례](https://tiabet0929.tistory.com/35) · 직접 D08 |
| P01b · 새 대조 · [구성문](controls.jsonl#L2) | 사전 봉인 | 가중치가 [0,3) | 가중치 A10 / 가 · C 최초 | 같은 대상 / 원함 | [원 용례](https://tiabet0929.tistory.com/35) · 직접 D08 |
| P02a · 새 대조 · [구성문](controls.jsonl#L3) | 사전 봉인 | 축 순서 [0,4) | 축 순서 A11 / — · B 최초 | 같은 대상 / 원함 | [원 용례](https://sdesign416.tistory.com/110) · 직접 T03 |
| P02b · 새 대조 · [구성문](controls.jsonl#L4) | 사전 봉인 | 축 순서를 [0,4) | 축 순서 A11 / 를 · C 최초 | 같은 대상 / 원함 | [원 용례](https://sdesign416.tistory.com/110) · 직접 T03 |
| P03a · 새 대조 · [구성문](controls.jsonl#L5) | 사전 봉인 | 전치사 [8,10) | 전치 A08 / — · D 최초 | 다른 대상 / 원함 | [원 용례](https://statisticsplaybook.tistory.com/m/6) · 직접 0 |
| P03b · 새 대조 · [구성문](controls.jsonl#L6) | 사전 봉인 | 전치 [8,10) | 전치 A08 / — · B 최초 | 다른 대상 / 원함 | [원 용례](https://statisticsplaybook.tistory.com/m/6) · 직접 0 |
| P04a · 새 대조 · [구성문](controls.jsonl#L7) | 사전 봉인 | 뷰어 [8,9) | 뷰 A04 / — · D 최초 | 다른 대상 / 원함 | [원 용례](https://chickencat-jjanga.tistory.com/130) · 직접 0 |
| P04b · 새 대조 · [구성문](controls.jsonl#L8) | 사전 봉인 | 뷰 [11,12) | 뷰 A04 / — · B 최초 | 같은 대상 / 원함 | [원 용례](https://chickencat-jjanga.tistory.com/130) · 직접 T01, T02 |
| P05a · 새 대조 · [구성문](controls.jsonl#L9) | 사전 봉인 | 데이터로더 [40,45) | 데이터로더 A01 / — · B 최초 | 같은 대상 / 원함 | [원 용례](https://github.com/PyTorchKR/tutorials-kr/blob/2.3.1-latest/beginner_source/basics/quickstart_tutorial.py#L55-L65) · 직접 D01 |
| P05b · 새 대조 · [구성문](controls.jsonl#L10) | 사전 봉인 | 데이터로더 [40,45) | 데이터로더 A01 / — · B 최초 | 같은 대상 / 거절 | [원 용례](https://github.com/PyTorchKR/tutorials-kr/blob/2.3.1-latest/beginner_source/basics/quickstart_tutorial.py#L55-L65) · 직접 D07 |
| P06a · 새 대조 · [구성문](controls.jsonl#L11) | 사전 봉인 | 복사본을 [11,14) | 복사본 A05 / 을 · C 최초 | 같은 대상 / 원함 | [원 용례](https://github.com/PyTorchKR/tutorials-kr/blob/2.3.1-latest/beginner_source/introyt/tensors_deeper_tutorial.py#L549-L621) · 직접 T07 |
| P06b · 새 대조 · [구성문](controls.jsonl#L12) | 사전 봉인 | 복사본은 [28,31) | 복사본 A05 / 은 · C 최초 | 같은 대상 / 거절 | [원 용례](https://github.com/PyTorchKR/tutorials-kr/blob/2.3.1-latest/beginner_source/introyt/tensors_deeper_tutorial.py#L549-L621) · 직접 T08 |

## 표 2 · 요청, 정책 및 상한

조는 조사, 표는 표시다. 증감은 해당 뷰의 직전 정책 대비이며 가림 증감은 같은 정책의 원문 대비다. 순위 0은 양수 후보 밖이다. 판독 수의 순서는 직접/일부/명시충돌/미확인이다.

| 요청·원문 또는 가림 | 정책 | 조사 8·표시 3 | 직접·일부·충돌·미확인 | 유입·탈락 ID와 순위 | 반대 근거 URL |
| --- | --- | --- | --- | --- | --- |
| C01 · 원문 | A | 조 D01→D03→D06→D07→D08 (3공석) · 표 D01→D03→D06 (0공석) | 조 1/1/3/0 · 표 0/1/2/0 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| C01 · 원문 | B | 조 D01→D03→D06→D07→D08 (3공석) · 표 D01→D03→D06 (0공석) | 조 1/1/3/0 · 표 0/1/2/0 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| C01 · 원문 | C | 조 D01→D03→D06→D07→D08 (3공석) · 표 D01→D03→D06 (0공석) | 조 1/1/3/0 · 표 0/1/2/0 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| C01 · 원문 | D | 조 D01→D03→D06→D07→D08 (3공석) · 표 D01→D03→D06 (0공석) | 조 1/1/3/0 · 표 0/1/2/0 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| C01 · 가림 | A | 조 D03→D06→D07→D08 (4공석) · 표 D03→D06→D07 (0공석) | 조 1/1/2/0 · 표 1/1/1/0 | 가림 조 +— / −D01:1→0 / 이동 D03:2→1, D06:3→2, D07:4→3, D08:5→4<br>가림 표 +D07:4→3 / −D01:1→0 / 이동 D03:2→1, D06:3→2 | [D03 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataset.py#L193-L214) |
| C01 · 가림 | B | 조 D01→D03→D06→D07→D08 (3공석) · 표 D01→D03→D06 (0공석) | 조 1/1/3/0 · 표 0/1/2/0 | B 조 +D01:0→1 / −— / 이동 D03:1→2, D06:2→3, D07:3→4, D08:4→5<br>B 표 +D01:0→1 / −D07:3→4 / 이동 D03:1→2, D06:2→3 | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| C01 · 가림 | C | 조 D01→D03→D06→D07→D08 (3공석) · 표 D01→D03→D06 (0공석) | 조 1/1/3/0 · 표 0/1/2/0 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| C01 · 가림 | D | 조 D01→D03→D06→D07→D08 (3공석) · 표 D01→D03→D06 (0공석) | 조 1/1/3/0 · 표 0/1/2/0 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| C02 · 원문 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/evidence/controls.jsonl) |
| C02 · 원문 | B | 조 D08 (7공석) · 표 D08 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | B 조 +D08:0→1 / −— / 이동 —<br>B 표 +D08:0→1 / −— / 이동 — | [D08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L290) |
| C02 · 원문 | C | 조 D08 (7공석) · 표 D08 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [D08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L290) |
| C02 · 원문 | D | 조 D08 (7공석) · 표 D08 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [D08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L290) |
| C02 · 가림 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/evidence/controls.jsonl) |
| C02 · 가림 | B | 조 D08 (7공석) · 표 D08 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | B 조 +D08:0→1 / −— / 이동 —<br>B 표 +D08:0→1 / −— / 이동 — | [D08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L290) |
| C02 · 가림 | C | 조 D08 (7공석) · 표 D08 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [D08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L290) |
| C02 · 가림 | D | 조 D08 (7공석) · 표 D08 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [D08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L290) |
| C03 · 원문 | A | 조 T02 (7공석) · 표 T02 (2공석) | 조 0/0/1/0 · 표 0/0/1/0 | — | [T02 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L9257-L9294) |
| C03 · 원문 | B | 조 T02→T03→T04 (5공석) · 표 T02→T03→T04 (0공석) | 조 2/0/1/0 · 표 2/0/1/0 | B 조 +T03:0→2, T04:0→3 / −— / 이동 —<br>B 표 +T03:0→2, T04:0→3 / −— / 이동 — | [T02 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L9257-L9294) |
| C03 · 원문 | C | 조 T02→T03→T04 (5공석) · 표 T02→T03→T04 (0공석) | 조 2/0/1/0 · 표 2/0/1/0 | — | [T02 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L9257-L9294) |
| C03 · 원문 | D | 조 T02→T03→T04 (5공석) · 표 T02→T03→T04 (0공석) | 조 2/0/1/0 · 표 2/0/1/0 | — | [T02 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L9257-L9294) |
| C03 · 가림 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | 가림 조 +— / −T02:1→0 / 이동 —<br>가림 표 +— / −T02:1→0 / 이동 — | [T02 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L9257-L9294) |
| C03 · 가림 | B | 조 T02→T03→T04 (5공석) · 표 T02→T03→T04 (0공석) | 조 2/0/1/0 · 표 2/0/1/0 | B 조 +T02:0→1, T03:0→2, T04:0→3 / −— / 이동 —<br>B 표 +T02:0→1, T03:0→2, T04:0→3 / −— / 이동 — | [T02 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L9257-L9294) |
| C03 · 가림 | C | 조 T02→T03→T04 (5공석) · 표 T02→T03→T04 (0공석) | 조 2/0/1/0 · 표 2/0/1/0 | — | [T02 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L9257-L9294) |
| C03 · 가림 | D | 조 T02→T03→T04 (5공석) · 표 T02→T03→T04 (0공석) | 조 2/0/1/0 · 표 2/0/1/0 | — | [T02 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L9257-L9294) |
| C04 · 원문 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/evidence/controls.jsonl) |
| C04 · 원문 | B | 조 T01 (7공석) · 표 T01 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | B 조 +T01:0→1 / −— / 이동 —<br>B 표 +T01:0→1 / −— / 이동 — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| C04 · 원문 | C | 조 T01 (7공석) · 표 T01 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| C04 · 원문 | D | 조 T01 (7공석) · 표 T01 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| C04 · 가림 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/evidence/controls.jsonl) |
| C04 · 가림 | B | 조 T01 (7공석) · 표 T01 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | B 조 +T01:0→1 / −— / 이동 —<br>B 표 +T01:0→1 / −— / 이동 — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| C04 · 가림 | C | 조 T01 (7공석) · 표 T01 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| C04 · 가림 | D | 조 T01 (7공석) · 표 T01 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| C05 · 원문 | A | 조 T08→T07 (6공석) · 표 T08→T07 (1공석) | 조 1/0/1/0 · 표 1/0/1/0 | — | [T08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/aten/src/ATen/native/TensorShape.cpp#L3757-L3769) |
| C05 · 원문 | B | 조 T08→T07 (6공석) · 표 T08→T07 (1공석) | 조 1/0/1/0 · 표 1/0/1/0 | — | [T08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/aten/src/ATen/native/TensorShape.cpp#L3757-L3769) |
| C05 · 원문 | C | 조 T08→T07 (6공석) · 표 T08→T07 (1공석) | 조 1/0/1/0 · 표 1/0/1/0 | — | [T08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/aten/src/ATen/native/TensorShape.cpp#L3757-L3769) |
| C05 · 원문 | D | 조 T08→T07 (6공석) · 표 T08→T07 (1공석) | 조 1/0/1/0 · 표 1/0/1/0 | — | [T08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/aten/src/ATen/native/TensorShape.cpp#L3757-L3769) |
| C05 · 가림 | A | 조 T07→T08 (6공석) · 표 T07→T08 (1공석) | 조 1/0/1/0 · 표 1/0/1/0 | 가림 조 +— / −— / 이동 T07:2→1, T08:1→2<br>가림 표 +— / −— / 이동 T07:2→1, T08:1→2 | [T08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/aten/src/ATen/native/TensorShape.cpp#L3757-L3769) |
| C05 · 가림 | B | 조 T07→T08 (6공석) · 표 T07→T08 (1공석) | 조 1/0/1/0 · 표 1/0/1/0 | 가림 조 +— / −— / 이동 T07:2→1, T08:1→2<br>가림 표 +— / −— / 이동 T07:2→1, T08:1→2 | [T08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/aten/src/ATen/native/TensorShape.cpp#L3757-L3769) |
| C05 · 가림 | C | 조 T07→T08 (6공석) · 표 T07→T08 (1공석) | 조 1/0/1/0 · 표 1/0/1/0 | 가림 조 +— / −— / 이동 T07:2→1, T08:1→2<br>가림 표 +— / −— / 이동 T07:2→1, T08:1→2 | [T08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/aten/src/ATen/native/TensorShape.cpp#L3757-L3769) |
| C05 · 가림 | D | 조 T07→T08 (6공석) · 표 T07→T08 (1공석) | 조 1/0/1/0 · 표 1/0/1/0 | 가림 조 +— / −— / 이동 T07:2→1, T08:1→2<br>가림 표 +— / −— / 이동 T07:2→1, T08:1→2 | [T08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/aten/src/ATen/native/TensorShape.cpp#L3757-L3769) |
| C06 · 원문 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/evidence/controls.jsonl) |
| C06 · 원문 | B | 조 T07→T08 (6공석) · 표 T07→T08 (1공석) | 조 1/0/1/0 · 표 1/0/1/0 | B 조 +T07:0→1, T08:0→2 / −— / 이동 —<br>B 표 +T07:0→1, T08:0→2 / −— / 이동 — | [T07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L2716-L2736) |
| C06 · 원문 | C | 조 T07→T08 (6공석) · 표 T07→T08 (1공석) | 조 1/0/1/0 · 표 1/0/1/0 | — | [T07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L2716-L2736) |
| C06 · 원문 | D | 조 T07→T08 (6공석) · 표 T07→T08 (1공석) | 조 1/0/1/0 · 표 1/0/1/0 | — | [T07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L2716-L2736) |
| C06 · 가림 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/evidence/controls.jsonl) |
| C06 · 가림 | B | 조 T07→T08 (6공석) · 표 T07→T08 (1공석) | 조 1/0/1/0 · 표 1/0/1/0 | B 조 +T07:0→1, T08:0→2 / −— / 이동 —<br>B 표 +T07:0→1, T08:0→2 / −— / 이동 — | [T07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L2716-L2736) |
| C06 · 가림 | C | 조 T07→T08 (6공석) · 표 T07→T08 (1공석) | 조 1/0/1/0 · 표 1/0/1/0 | — | [T07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L2716-L2736) |
| C06 · 가림 | D | 조 T07→T08 (6공석) · 표 T07→T08 (1공석) | 조 1/0/1/0 · 표 1/0/1/0 | — | [T07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L2716-L2736) |
| C07 · 원문 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/evidence/controls.jsonl) |
| C07 · 원문 | B | 조 T07 (7공석) · 표 T07 (2공석) | 조 0/1/0/0 · 표 0/1/0/0 | B 조 +T07:0→1 / −— / 이동 —<br>B 표 +T07:0→1 / −— / 이동 — | [T07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L2716-L2736) |
| C07 · 원문 | C | 조 T07 (7공석) · 표 T07 (2공석) | 조 0/1/0/0 · 표 0/1/0/0 | — | [T07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L2716-L2736) |
| C07 · 원문 | D | 조 T07 (7공석) · 표 T07 (2공석) | 조 0/1/0/0 · 표 0/1/0/0 | — | [T07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L2716-L2736) |
| C07 · 가림 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/evidence/controls.jsonl) |
| C07 · 가림 | B | 조 T07 (7공석) · 표 T07 (2공석) | 조 0/1/0/0 · 표 0/1/0/0 | B 조 +T07:0→1 / −— / 이동 —<br>B 표 +T07:0→1 / −— / 이동 — | [T07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L2716-L2736) |
| C07 · 가림 | C | 조 T07 (7공석) · 표 T07 (2공석) | 조 0/1/0/0 · 표 0/1/0/0 | — | [T07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L2716-L2736) |
| C07 · 가림 | D | 조 T07 (7공석) · 표 T07 (2공석) | 조 0/1/0/0 · 표 0/1/0/0 | — | [T07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L2716-L2736) |
| C08 · 원문 | A | 조 D04→D01→D05→D02→D03→D06→D07→D08 (0공석) · 표 D04→D01→D05 (0공석) | 조 1/1/1/5 · 표 1/1/1/0 | — | [D04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/_utils/collate.py#L337-L398) |
| C08 · 원문 | B | 조 D04→D01→D05→D02→D03→D06→D07→D08 (0공석) · 표 D04→D01→D05 (0공석) | 조 1/1/1/5 · 표 1/1/1/0 | — | [D04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/_utils/collate.py#L337-L398) |
| C08 · 원문 | C | 조 D04→D01→D05→D02→D03→D06→D07→D08 (0공석) · 표 D04→D01→D05 (0공석) | 조 1/1/1/5 · 표 1/1/1/0 | — | [D04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/_utils/collate.py#L337-L398) |
| C08 · 원문 | D | 조 D04→D01→D05→D02→D03→D06→D07→D08 (0공석) · 표 D04→D01→D05 (0공석) | 조 1/1/1/5 · 표 1/1/1/0 | — | [D04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/_utils/collate.py#L337-L398) |
| C08 · 가림 | A | 조 D01→D04→D05→D02→D03→D06→D07→D08 (0공석) · 표 D01→D04→D05 (0공석) | 조 1/1/1/5 · 표 1/1/1/0 | 가림 조 +— / −— / 이동 D01:2→1, D04:1→2<br>가림 표 +— / −— / 이동 D01:2→1, D04:1→2 | [D04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/_utils/collate.py#L337-L398) |
| C08 · 가림 | B | 조 D01→D04→D05→D02→D03→D06→D07→D08 (0공석) · 표 D01→D04→D05 (0공석) | 조 1/1/1/5 · 표 1/1/1/0 | 가림 조 +— / −— / 이동 D01:2→1, D04:1→2<br>가림 표 +— / −— / 이동 D01:2→1, D04:1→2 | [D04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/_utils/collate.py#L337-L398) |
| C08 · 가림 | C | 조 D01→D04→D05→D02→D03→D06→D07→D08 (0공석) · 표 D01→D04→D05 (0공석) | 조 1/1/1/5 · 표 1/1/1/0 | 가림 조 +— / −— / 이동 D01:2→1, D04:1→2<br>가림 표 +— / −— / 이동 D01:2→1, D04:1→2 | [D04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/_utils/collate.py#L337-L398) |
| C08 · 가림 | D | 조 D01→D04→D05→D02→D03→D06→D07→D08 (0공석) · 표 D01→D04→D05 (0공석) | 조 1/1/1/5 · 표 1/1/1/0 | 가림 조 +— / −— / 이동 D01:2→1, D04:1→2<br>가림 표 +— / −— / 이동 D01:2→1, D04:1→2 | [D04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/_utils/collate.py#L337-L398) |
| C09 · 원문 | A | 조 T04 (7공석) · 표 T04 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [T04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L11226-L11274) |
| C09 · 원문 | B | 조 T04 (7공석) · 표 T04 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [T04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L11226-L11274) |
| C09 · 원문 | C | 조 T04 (7공석) · 표 T04 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [T04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L11226-L11274) |
| C09 · 원문 | D | 조 T04 (7공석) · 표 T04 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [T04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L11226-L11274) |
| C09 · 가림 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | 가림 조 +— / −T04:1→0 / 이동 —<br>가림 표 +— / −T04:1→0 / 이동 — | [T04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L11226-L11274) |
| C09 · 가림 | B | 조 T04 (7공석) · 표 T04 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | B 조 +T04:0→1 / −— / 이동 —<br>B 표 +T04:0→1 / −— / 이동 — | [T04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L11226-L11274) |
| C09 · 가림 | C | 조 T04 (7공석) · 표 T04 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [T04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L11226-L11274) |
| C09 · 가림 | D | 조 T04 (7공석) · 표 T04 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [T04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L11226-L11274) |
| O3143 · 원문 | A | 조 T01→T02→T05→D01→D02→D03→D06→T06 (0공석) · 표 T01→T02→T05 (0공석) | 조 0/0/2/6 · 표 0/0/2/1 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| O3143 · 원문 | B | 조 T01→T02→T05→D01→D02→D03→D06→T06 (0공석) · 표 T01→T02→T05 (0공석) | 조 0/0/2/6 · 표 0/0/2/1 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| O3143 · 원문 | C | 조 T01→T02→T05→D01→D02→D03→D06→T06 (0공석) · 표 T01→T02→T05 (0공석) | 조 0/0/2/6 · 표 0/0/2/1 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| O3143 · 원문 | D | 조 T01→T02→T05→D01→D02→D03→D06→T06 (0공석) · 표 T01→T02→T05 (0공석) | 조 0/0/2/6 · 표 0/0/2/1 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| O3143 · 가림 | A | 조 T01→T02→T05→D01→D02→D03→D06→T06 (0공석) · 표 T01→T02→T05 (0공석) | 조 0/0/2/6 · 표 0/0/2/1 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| O3143 · 가림 | B | 조 T01→T02→T05→D01→D02→D03→D06→T06 (0공석) · 표 T01→T02→T05 (0공석) | 조 0/0/2/6 · 표 0/0/2/1 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| O3143 · 가림 | C | 조 T01→T02→T05→D01→D02→D03→D06→T06 (0공석) · 표 T01→T02→T05 (0공석) | 조 0/0/2/6 · 표 0/0/2/1 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| O3143 · 가림 | D | 조 T01→T02→T05→D01→D02→D03→D06→T06 (0공석) · 표 T01→T02→T05 (0공석) | 조 0/0/2/6 · 표 0/0/2/1 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| O3611 · 원문 | A | 조 D04→T01→T05→T06→D01→D03→D07→T02 (0공석) · 표 D04→T01→T05 (0공석) | 조 0/4/2/2 · 표 0/1/1/1 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| O3611 · 원문 | B | 조 D04→T01→T05→T06→D01→D03→D07→T02 (0공석) · 표 D04→T01→T05 (0공석) | 조 0/4/2/2 · 표 0/1/1/1 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| O3611 · 원문 | C | 조 D04→T01→T05→T06→D01→D03→D07→T02 (0공석) · 표 D04→T01→T05 (0공석) | 조 0/4/2/2 · 표 0/1/1/1 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| O3611 · 원문 | D | 조 D04→T01→T05→T06→D01→D03→D07→T02 (0공석) · 표 D04→T01→T05 (0공석) | 조 0/4/2/2 · 표 0/1/1/1 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| O3611 · 가림 | A | 조 D04→T01→T05→T06→D01→D03→D07→T02 (0공석) · 표 D04→T01→T05 (0공석) | 조 0/4/2/2 · 표 0/1/1/1 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| O3611 · 가림 | B | 조 D04→T01→T05→T06→D01→D03→D07→T02 (0공석) · 표 D04→T01→T05 (0공석) | 조 0/4/2/2 · 표 0/1/1/1 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| O3611 · 가림 | C | 조 D04→T01→T05→T06→D01→D03→D07→T02 (0공석) · 표 D04→T01→T05 (0공석) | 조 0/4/2/2 · 표 0/1/1/1 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| O3611 · 가림 | D | 조 D04→T01→T05→T06→D01→D03→D07→T02 (0공석) · 표 D04→T01→T05 (0공석) | 조 0/4/2/2 · 표 0/1/1/1 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| O3665 · 원문 | A | 조 D01→D04→D07 (5공석) · 표 D01→D04→D07 (0공석) | 조 0/0/0/3 · 표 0/0/0/3 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| O3665 · 원문 | B | 조 D01→D04→D07 (5공석) · 표 D01→D04→D07 (0공석) | 조 0/0/0/3 · 표 0/0/0/3 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| O3665 · 원문 | C | 조 D01→D04→D07 (5공석) · 표 D01→D04→D07 (0공석) | 조 0/0/0/3 · 표 0/0/0/3 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| O3665 · 원문 | D | 조 D01→D04→D07 (5공석) · 표 D01→D04→D07 (0공석) | 조 0/0/0/3 · 표 0/0/0/3 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| O3665 · 가림 | A | 조 D01→D04→D07 (5공석) · 표 D01→D04→D07 (0공석) | 조 0/0/0/3 · 표 0/0/0/3 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| O3665 · 가림 | B | 조 D01→D04→D07 (5공석) · 표 D01→D04→D07 (0공석) | 조 0/0/0/3 · 표 0/0/0/3 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| O3665 · 가림 | C | 조 D01→D04→D07 (5공석) · 표 D01→D04→D07 (0공석) | 조 0/0/0/3 · 표 0/0/0/3 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| O3665 · 가림 | D | 조 D01→D04→D07 (5공석) · 표 D01→D04→D07 (0공석) | 조 0/0/0/3 · 표 0/0/0/3 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| O3875 · 원문 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/ddp-batch-size/3875) |
| O3875 · 원문 | B | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/ddp-batch-size/3875) |
| O3875 · 원문 | C | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/ddp-batch-size/3875) |
| O3875 · 원문 | D | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/ddp-batch-size/3875) |
| O3875 · 가림 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/ddp-batch-size/3875) |
| O3875 · 가림 | B | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/ddp-batch-size/3875) |
| O3875 · 가림 | C | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/ddp-batch-size/3875) |
| O3875 · 가림 | D | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/ddp-batch-size/3875) |
| O3885 · 원문 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/model-training-loader/3885) |
| O3885 · 원문 | B | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/model-training-loader/3885) |
| O3885 · 원문 | C | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/model-training-loader/3885) |
| O3885 · 원문 | D | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/model-training-loader/3885) |
| O3885 · 가림 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/model-training-loader/3885) |
| O3885 · 가림 | B | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/model-training-loader/3885) |
| O3885 · 가림 | C | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/model-training-loader/3885) |
| O3885 · 가림 | D | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/model-training-loader/3885) |
| O4437 · 원문 | A | 조 D01→T01→T02→D03→D07→T05→D02→D04 (0공석) · 표 D01→T01→T02 (0공석) | 조 0/1/0/7 · 표 0/1/0/2 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| O4437 · 원문 | B | 조 D01→T01→T02→D03→D07→T05→D02→D04 (0공석) · 표 D01→T01→T02 (0공석) | 조 0/1/0/7 · 표 0/1/0/2 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| O4437 · 원문 | C | 조 D01→T01→T02→D03→D07→T05→D02→D04 (0공석) · 표 D01→T01→T02 (0공석) | 조 0/1/0/7 · 표 0/1/0/2 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| O4437 · 원문 | D | 조 D01→T01→T02→D03→D07→T05→D02→D04 (0공석) · 표 D01→T01→T02 (0공석) | 조 0/1/0/7 · 표 0/1/0/2 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| O4437 · 가림 | A | 조 D01→T01→T02→D03→D07→T05→D02→D04 (0공석) · 표 D01→T01→T02 (0공석) | 조 0/1/0/7 · 표 0/1/0/2 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| O4437 · 가림 | B | 조 D01→T01→T02→D03→D07→T05→D02→D04 (0공석) · 표 D01→T01→T02 (0공석) | 조 0/1/0/7 · 표 0/1/0/2 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| O4437 · 가림 | C | 조 D01→T01→T02→D03→D07→T05→D02→D04 (0공석) · 표 D01→T01→T02 (0공석) | 조 0/1/0/7 · 표 0/1/0/2 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| O4437 · 가림 | D | 조 D01→T01→T02→D03→D07→T05→D02→D04 (0공석) · 표 D01→T01→T02 (0공석) | 조 0/1/0/7 · 표 0/1/0/2 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| O4588 · 원문 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/topic/4588) |
| O4588 · 원문 | B | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/topic/4588) |
| O4588 · 원문 | C | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/topic/4588) |
| O4588 · 원문 | D | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/topic/4588) |
| O4588 · 가림 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/topic/4588) |
| O4588 · 가림 | B | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/topic/4588) |
| O4588 · 가림 | C | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/topic/4588) |
| O4588 · 가림 | D | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/topic/4588) |
| O4975 · 원문 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/training-validate-test/4975) |
| O4975 · 원문 | B | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/training-validate-test/4975) |
| O4975 · 원문 | C | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/training-validate-test/4975) |
| O4975 · 원문 | D | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/training-validate-test/4975) |
| O4975 · 가림 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/training-validate-test/4975) |
| O4975 · 가림 | B | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/training-validate-test/4975) |
| O4975 · 가림 | C | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/training-validate-test/4975) |
| O4975 · 가림 | D | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://discuss.pytorch.kr/t/training-validate-test/4975) |
| O5330 · 원문 | A | 조 D01→D02→D03→D04→D05→D06→D08 (1공석) · 표 D01→D02→D03 (0공석) | 조 0/0/1/6 · 표 0/0/1/2 | — | [D03 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataset.py#L193-L214) |
| O5330 · 원문 | B | 조 D01→D02→D03→D04→D05→D06→D08 (1공석) · 표 D01→D02→D03 (0공석) | 조 0/0/1/6 · 표 0/0/1/2 | — | [D03 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataset.py#L193-L214) |
| O5330 · 원문 | C | 조 D01→D02→D03→D04→D05→D06→D08 (1공석) · 표 D01→D02→D03 (0공석) | 조 0/0/1/6 · 표 0/0/1/2 | — | [D03 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataset.py#L193-L214) |
| O5330 · 원문 | D | 조 D01→D02→D03→D04→D05→D06→D08 (1공석) · 표 D01→D02→D03 (0공석) | 조 0/0/1/6 · 표 0/0/1/2 | — | [D03 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataset.py#L193-L214) |
| O5330 · 가림 | A | 조 D01→D02→D03→D04→D05→D06→D08 (1공석) · 표 D01→D02→D03 (0공석) | 조 0/0/1/6 · 표 0/0/1/2 | — | [D03 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataset.py#L193-L214) |
| O5330 · 가림 | B | 조 D01→D02→D03→D04→D05→D06→D08 (1공석) · 표 D01→D02→D03 (0공석) | 조 0/0/1/6 · 표 0/0/1/2 | — | [D03 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataset.py#L193-L214) |
| O5330 · 가림 | C | 조 D01→D02→D03→D04→D05→D06→D08 (1공석) · 표 D01→D02→D03 (0공석) | 조 0/0/1/6 · 표 0/0/1/2 | — | [D03 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataset.py#L193-L214) |
| O5330 · 가림 | D | 조 D01→D02→D03→D04→D05→D06→D08 (1공석) · 표 D01→D02→D03 (0공석) | 조 0/0/1/6 · 표 0/0/1/2 | — | [D03 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataset.py#L193-L214) |
| O5952 · 원문 | A | 조 T02→T01→T07→T05→T03→D03→D04→T04 (0공석) · 표 T02→T01→T07 (0공석) | 조 0/3/3/2 · 표 0/3/0/0 | — | [T02 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L9257-L9294) |
| O5952 · 원문 | B | 조 T02→T01→T07→T05→T03→D03→D04→T04 (0공석) · 표 T02→T01→T07 (0공석) | 조 0/3/3/2 · 표 0/3/0/0 | — | [T02 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L9257-L9294) |
| O5952 · 원문 | C | 조 T02→T01→T07→T05→T03→D03→D04→T04 (0공석) · 표 T02→T01→T07 (0공석) | 조 0/3/3/2 · 표 0/3/0/0 | — | [T02 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L9257-L9294) |
| O5952 · 원문 | D | 조 T02→T01→T07→T05→T03→D03→D04→T04 (0공석) · 표 T02→T01→T07 (0공석) | 조 0/3/3/2 · 표 0/3/0/0 | — | [T02 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L9257-L9294) |
| O5952 · 가림 | A | 조 T05→D03→D04→T01→T02→T03→T04→T06 (0공석) · 표 T05→D03→D04 (0공석) | 조 0/2/4/2 · 표 0/0/1/2 | 가림 조 +T06:9→8 / −T07:3→10 / 이동 T05:4→1, D03:6→2, D04:7→3, T01:2→4, T02:1→5, T03:5→6, T04:8→7<br>가림 표 +T05:4→1, D03:6→2, D04:7→3 / −T02:1→5, T01:2→4, T07:3→10 / 이동 — | [T05 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6240-L6281) |
| O5952 · 가림 | B | 조 T05→D03→D04→T01→T02→T03→T04→T06 (0공석) · 표 T05→D03→D04 (0공석) | 조 0/2/4/2 · 표 0/0/1/2 | 가림 조 +T06:9→8 / −T07:3→10 / 이동 T05:4→1, D03:6→2, D04:7→3, T01:2→4, T02:1→5, T03:5→6, T04:8→7<br>가림 표 +T05:4→1, D03:6→2, D04:7→3 / −T02:1→5, T01:2→4, T07:3→10 / 이동 — | [T05 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6240-L6281) |
| O5952 · 가림 | C | 조 T05→D03→D04→T01→T02→T03→T04→T06 (0공석) · 표 T05→D03→D04 (0공석) | 조 0/2/4/2 · 표 0/0/1/2 | 가림 조 +T06:9→8 / −T07:3→10 / 이동 T05:4→1, D03:6→2, D04:7→3, T01:2→4, T02:1→5, T03:5→6, T04:8→7<br>가림 표 +T05:4→1, D03:6→2, D04:7→3 / −T02:1→5, T01:2→4, T07:3→10 / 이동 — | [T05 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6240-L6281) |
| O5952 · 가림 | D | 조 T05→D03→D04→T01→T02→T03→T04→T06 (0공석) · 표 T05→D03→D04 (0공석) | 조 0/2/4/2 · 표 0/0/1/2 | 가림 조 +T06:9→8 / −T07:3→10 / 이동 T05:4→1, D03:6→2, D04:7→3, T01:2→4, T02:1→5, T03:5→6, T04:8→7<br>가림 표 +T05:4→1, D03:6→2, D04:7→3 / −T02:1→5, T01:2→4, T07:3→10 / 이동 — | [T05 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6240-L6281) |
| P01a · 원문 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://tiabet0929.tistory.com/35) |
| P01a · 원문 | B | 조 D08 (7공석) · 표 D08 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | B 조 +D08:0→1 / −— / 이동 —<br>B 표 +D08:0→1 / −— / 이동 — | [D08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L290) |
| P01a · 원문 | C | 조 D08 (7공석) · 표 D08 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [D08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L290) |
| P01a · 원문 | D | 조 D08 (7공석) · 표 D08 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [D08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L290) |
| P01a · 가림 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://tiabet0929.tistory.com/35) |
| P01a · 가림 | B | 조 D08 (7공석) · 표 D08 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | B 조 +D08:0→1 / −— / 이동 —<br>B 표 +D08:0→1 / −— / 이동 — | [D08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L290) |
| P01a · 가림 | C | 조 D08 (7공석) · 표 D08 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [D08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L290) |
| P01a · 가림 | D | 조 D08 (7공석) · 표 D08 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [D08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L290) |
| P01b · 원문 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://tiabet0929.tistory.com/35) |
| P01b · 원문 | B | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://tiabet0929.tistory.com/35) |
| P01b · 원문 | C | 조 D08 (7공석) · 표 D08 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | C 조 +D08:0→1 / −— / 이동 —<br>C 표 +D08:0→1 / −— / 이동 — | [D08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L290) |
| P01b · 원문 | D | 조 D08 (7공석) · 표 D08 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [D08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L290) |
| P01b · 가림 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://tiabet0929.tistory.com/35) |
| P01b · 가림 | B | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://tiabet0929.tistory.com/35) |
| P01b · 가림 | C | 조 D08 (7공석) · 표 D08 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | C 조 +D08:0→1 / −— / 이동 —<br>C 표 +D08:0→1 / −— / 이동 — | [D08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L290) |
| P01b · 가림 | D | 조 D08 (7공석) · 표 D08 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [D08 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L290) |
| P02a · 원문 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://sdesign416.tistory.com/110) |
| P02a · 원문 | B | 조 T03 (7공석) · 표 T03 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | B 조 +T03:0→1 / −— / 이동 —<br>B 표 +T03:0→1 / −— / 이동 — | [T03 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L8325-L8346) |
| P02a · 원문 | C | 조 T03 (7공석) · 표 T03 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [T03 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L8325-L8346) |
| P02a · 원문 | D | 조 T03 (7공석) · 표 T03 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [T03 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L8325-L8346) |
| P02a · 가림 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://sdesign416.tistory.com/110) |
| P02a · 가림 | B | 조 T03 (7공석) · 표 T03 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | B 조 +T03:0→1 / −— / 이동 —<br>B 표 +T03:0→1 / −— / 이동 — | [T03 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L8325-L8346) |
| P02a · 가림 | C | 조 T03 (7공석) · 표 T03 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [T03 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L8325-L8346) |
| P02a · 가림 | D | 조 T03 (7공석) · 표 T03 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [T03 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L8325-L8346) |
| P02b · 원문 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://sdesign416.tistory.com/110) |
| P02b · 원문 | B | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://sdesign416.tistory.com/110) |
| P02b · 원문 | C | 조 T03 (7공석) · 표 T03 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | C 조 +T03:0→1 / −— / 이동 —<br>C 표 +T03:0→1 / −— / 이동 — | [T03 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L8325-L8346) |
| P02b · 원문 | D | 조 T03 (7공석) · 표 T03 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [T03 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L8325-L8346) |
| P02b · 가림 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://sdesign416.tistory.com/110) |
| P02b · 가림 | B | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://sdesign416.tistory.com/110) |
| P02b · 가림 | C | 조 T03 (7공석) · 표 T03 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | C 조 +T03:0→1 / −— / 이동 —<br>C 표 +T03:0→1 / −— / 이동 — | [T03 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L8325-L8346) |
| P02b · 가림 | D | 조 T03 (7공석) · 표 T03 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [T03 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L8325-L8346) |
| P03a · 원문 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://statisticsplaybook.tistory.com/m/6) |
| P03a · 원문 | B | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://statisticsplaybook.tistory.com/m/6) |
| P03a · 원문 | C | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://statisticsplaybook.tistory.com/m/6) |
| P03a · 원문 | D | 조 T04 (7공석) · 표 T04 (2공석) | 조 0/0/1/0 · 표 0/0/1/0 | D 조 +T04:0→1 / −— / 이동 —<br>D 표 +T04:0→1 / −— / 이동 — | [T04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L11226-L11274) |
| P03a · 가림 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://statisticsplaybook.tistory.com/m/6) |
| P03a · 가림 | B | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://statisticsplaybook.tistory.com/m/6) |
| P03a · 가림 | C | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://statisticsplaybook.tistory.com/m/6) |
| P03a · 가림 | D | 조 T04 (7공석) · 표 T04 (2공석) | 조 0/0/1/0 · 표 0/0/1/0 | D 조 +T04:0→1 / −— / 이동 —<br>D 표 +T04:0→1 / −— / 이동 — | [T04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L11226-L11274) |
| P03b · 원문 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://statisticsplaybook.tistory.com/m/6) |
| P03b · 원문 | B | 조 T04 (7공석) · 표 T04 (2공석) | 조 0/0/1/0 · 표 0/0/1/0 | B 조 +T04:0→1 / −— / 이동 —<br>B 표 +T04:0→1 / −— / 이동 — | [T04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L11226-L11274) |
| P03b · 원문 | C | 조 T04 (7공석) · 표 T04 (2공석) | 조 0/0/1/0 · 표 0/0/1/0 | — | [T04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L11226-L11274) |
| P03b · 원문 | D | 조 T04 (7공석) · 표 T04 (2공석) | 조 0/0/1/0 · 표 0/0/1/0 | — | [T04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L11226-L11274) |
| P03b · 가림 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://statisticsplaybook.tistory.com/m/6) |
| P03b · 가림 | B | 조 T04 (7공석) · 표 T04 (2공석) | 조 0/0/1/0 · 표 0/0/1/0 | B 조 +T04:0→1 / −— / 이동 —<br>B 표 +T04:0→1 / −— / 이동 — | [T04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L11226-L11274) |
| P03b · 가림 | C | 조 T04 (7공석) · 표 T04 (2공석) | 조 0/0/1/0 · 표 0/0/1/0 | — | [T04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L11226-L11274) |
| P03b · 가림 | D | 조 T04 (7공석) · 표 T04 (2공석) | 조 0/0/1/0 · 표 0/0/1/0 | — | [T04 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L11226-L11274) |
| P04a · 원문 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://chickencat-jjanga.tistory.com/130) |
| P04a · 원문 | B | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://chickencat-jjanga.tistory.com/130) |
| P04a · 원문 | C | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://chickencat-jjanga.tistory.com/130) |
| P04a · 원문 | D | 조 T01 (7공석) · 표 T01 (2공석) | 조 0/0/1/0 · 표 0/0/1/0 | D 조 +T01:0→1 / −— / 이동 —<br>D 표 +T01:0→1 / −— / 이동 — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| P04a · 가림 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://chickencat-jjanga.tistory.com/130) |
| P04a · 가림 | B | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://chickencat-jjanga.tistory.com/130) |
| P04a · 가림 | C | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://chickencat-jjanga.tistory.com/130) |
| P04a · 가림 | D | 조 T01 (7공석) · 표 T01 (2공석) | 조 0/0/1/0 · 표 0/0/1/0 | D 조 +T01:0→1 / −— / 이동 —<br>D 표 +T01:0→1 / −— / 이동 — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| P04b · 원문 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://chickencat-jjanga.tistory.com/130) |
| P04b · 원문 | B | 조 T01 (7공석) · 표 T01 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | B 조 +T01:0→1 / −— / 이동 —<br>B 표 +T01:0→1 / −— / 이동 — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| P04b · 원문 | C | 조 T01 (7공석) · 표 T01 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| P04b · 원문 | D | 조 T01 (7공석) · 표 T01 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| P04b · 가림 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://chickencat-jjanga.tistory.com/130) |
| P04b · 가림 | B | 조 T01 (7공석) · 표 T01 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | B 조 +T01:0→1 / −— / 이동 —<br>B 표 +T01:0→1 / −— / 이동 — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| P04b · 가림 | C | 조 T01 (7공석) · 표 T01 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| P04b · 가림 | D | 조 T01 (7공석) · 표 T01 (2공석) | 조 1/0/0/0 · 표 1/0/0/0 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| P05a · 원문 | A | 조 D07→D03→D06→D08 (4공석) · 표 D07→D03→D06 (0공석) | 조 0/2/2/0 · 표 0/2/1/0 | — | [D07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L293-L357) |
| P05a · 원문 | B | 조 D07→D01→D03→D06→D08 (3공석) · 표 D07→D01→D03 (0공석) | 조 1/2/2/0 · 표 1/1/1/0 | B 조 +D01:0→2 / −— / 이동 D03:2→3, D06:3→4, D08:4→5<br>B 표 +D01:0→2 / −D06:3→4 / 이동 D03:2→3 | [D07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L293-L357) |
| P05a · 원문 | C | 조 D07→D01→D03→D06→D08 (3공석) · 표 D07→D01→D03 (0공석) | 조 1/2/2/0 · 표 1/1/1/0 | — | [D07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L293-L357) |
| P05a · 원문 | D | 조 D07→D01→D03→D06→D08 (3공석) · 표 D07→D01→D03 (0공석) | 조 1/2/2/0 · 표 1/1/1/0 | — | [D07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L293-L357) |
| P05a · 가림 | A | 조 D03→D06→D07→D08 (4공석) · 표 D03→D06→D07 (0공석) | 조 0/2/2/0 · 표 0/2/1/0 | 가림 조 +— / −— / 이동 D03:2→1, D06:3→2, D07:1→3<br>가림 표 +— / −— / 이동 D03:2→1, D06:3→2, D07:1→3 | [D07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L293-L357) |
| P05a · 가림 | B | 조 D01→D03→D06→D07→D08 (3공석) · 표 D01→D03→D06 (0공석) | 조 1/2/2/0 · 표 1/2/0/0 | B 조 +D01:0→1 / −— / 이동 D03:1→2, D06:2→3, D07:3→4, D08:4→5<br>가림 조 +— / −— / 이동 D01:2→1, D03:3→2, D06:4→3, D07:1→4<br>B 표 +D01:0→1 / −D07:3→4 / 이동 D03:1→2, D06:2→3<br>가림 표 +D06:4→3 / −D07:1→4 / 이동 D01:2→1, D03:3→2 | [D07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L293-L357) |
| P05a · 가림 | C | 조 D01→D03→D06→D07→D08 (3공석) · 표 D01→D03→D06 (0공석) | 조 1/2/2/0 · 표 1/2/0/0 | 가림 조 +— / −— / 이동 D01:2→1, D03:3→2, D06:4→3, D07:1→4<br>가림 표 +D06:4→3 / −D07:1→4 / 이동 D01:2→1, D03:3→2 | [D07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L293-L357) |
| P05a · 가림 | D | 조 D01→D03→D06→D07→D08 (3공석) · 표 D01→D03→D06 (0공석) | 조 1/2/2/0 · 표 1/2/0/0 | 가림 조 +— / −— / 이동 D01:2→1, D03:3→2, D06:4→3, D07:1→4<br>가림 표 +D06:4→3 / −D07:1→4 / 이동 D01:2→1, D03:3→2 | [D07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L293-L357) |
| P05b · 원문 | A | 조 D07→D03→D06→D08 (4공석) · 표 D07→D03→D06 (0공석) | 조 1/1/1/1 · 표 1/1/0/1 | — | [D07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L293-L357) |
| P05b · 원문 | B | 조 D07→D01→D03→D06→D08 (3공석) · 표 D07→D01→D03 (0공석) | 조 1/1/2/1 · 표 1/0/1/1 | B 조 +D01:0→2 / −— / 이동 D03:2→3, D06:3→4, D08:4→5<br>B 표 +D01:0→2 / −D06:3→4 / 이동 D03:2→3 | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| P05b · 원문 | C | 조 D07→D01→D03→D06→D08 (3공석) · 표 D07→D01→D03 (0공석) | 조 1/1/2/1 · 표 1/0/1/1 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| P05b · 원문 | D | 조 D07→D01→D03→D06→D08 (3공석) · 표 D07→D01→D03 (0공석) | 조 1/1/2/1 · 표 1/0/1/1 | — | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| P05b · 가림 | A | 조 D03→D06→D07→D08 (4공석) · 표 D03→D06→D07 (0공석) | 조 1/1/1/1 · 표 1/1/0/1 | 가림 조 +— / −— / 이동 D03:2→1, D06:3→2, D07:1→3<br>가림 표 +— / −— / 이동 D03:2→1, D06:3→2, D07:1→3 | [D03 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataset.py#L193-L214) |
| P05b · 가림 | B | 조 D01→D03→D06→D07→D08 (3공석) · 표 D01→D03→D06 (0공석) | 조 1/1/2/1 · 표 0/1/1/1 | B 조 +D01:0→1 / −— / 이동 D03:1→2, D06:2→3, D07:3→4, D08:4→5<br>가림 조 +— / −— / 이동 D01:2→1, D03:3→2, D06:4→3, D07:1→4<br>B 표 +D01:0→1 / −D07:3→4 / 이동 D03:1→2, D06:2→3<br>가림 표 +D06:4→3 / −D07:1→4 / 이동 D01:2→1, D03:3→2 | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| P05b · 가림 | C | 조 D01→D03→D06→D07→D08 (3공석) · 표 D01→D03→D06 (0공석) | 조 1/1/2/1 · 표 0/1/1/1 | 가림 조 +— / −— / 이동 D01:2→1, D03:3→2, D06:4→3, D07:1→4<br>가림 표 +D06:4→3 / −D07:1→4 / 이동 D01:2→1, D03:3→2 | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| P05b · 가림 | D | 조 D01→D03→D06→D07→D08 (3공석) · 표 D01→D03→D06 (0공석) | 조 1/1/2/1 · 표 0/1/1/1 | 가림 조 +— / −— / 이동 D01:2→1, D03:3→2, D06:4→3, D07:1→4<br>가림 표 +D06:4→3 / −D07:1→4 / 이동 D01:2→1, D03:3→2 | [D01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) |
| P06a · 원문 | A | 조 T01→T05 (6공석) · 표 T01→T05 (1공석) | 조 0/0/2/0 · 표 0/0/2/0 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| P06a · 원문 | B | 조 T01→T05 (6공석) · 표 T01→T05 (1공석) | 조 0/0/2/0 · 표 0/0/2/0 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| P06a · 원문 | C | 조 T07→T01→T05 (5공석) · 표 T07→T01→T05 (0공석) | 조 1/0/2/0 · 표 1/0/2/0 | C 조 +T07:0→1 / −— / 이동 T01:1→2, T05:2→3<br>C 표 +T07:0→1 / −— / 이동 T01:1→2, T05:2→3 | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| P06a · 원문 | D | 조 T07→T01→T05 (5공석) · 표 T07→T01→T05 (0공석) | 조 1/0/2/0 · 표 1/0/2/0 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| P06a · 가림 | A | 조 T01→T05 (6공석) · 표 T01→T05 (1공석) | 조 0/0/2/0 · 표 0/0/2/0 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| P06a · 가림 | B | 조 T01→T05 (6공석) · 표 T01→T05 (1공석) | 조 0/0/2/0 · 표 0/0/2/0 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| P06a · 가림 | C | 조 T07→T01→T05 (5공석) · 표 T07→T01→T05 (0공석) | 조 1/0/2/0 · 표 1/0/2/0 | C 조 +T07:0→1 / −— / 이동 T01:1→2, T05:2→3<br>C 표 +T07:0→1 / −— / 이동 T01:1→2, T05:2→3 | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| P06a · 가림 | D | 조 T07→T01→T05 (5공석) · 표 T07→T01→T05 (0공석) | 조 1/0/2/0 · 표 1/0/2/0 | — | [T01 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) |
| P06b · 원문 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://github.com/PyTorchKR/tutorials-kr/blob/2.3.1-latest/beginner_source/introyt/tensors_deeper_tutorial.py#L549-L621) |
| P06b · 원문 | B | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://github.com/PyTorchKR/tutorials-kr/blob/2.3.1-latest/beginner_source/introyt/tensors_deeper_tutorial.py#L549-L621) |
| P06b · 원문 | C | 조 T07 (7공석) · 표 T07 (2공석) | 조 0/0/1/0 · 표 0/0/1/0 | C 조 +T07:0→1 / −— / 이동 —<br>C 표 +T07:0→1 / −— / 이동 — | [T07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L2716-L2736) |
| P06b · 원문 | D | 조 T07 (7공석) · 표 T07 (2공석) | 조 0/0/1/0 · 표 0/0/1/0 | — | [T07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L2716-L2736) |
| P06b · 가림 | A | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://github.com/PyTorchKR/tutorials-kr/blob/2.3.1-latest/beginner_source/introyt/tensors_deeper_tutorial.py#L549-L621) |
| P06b · 가림 | B | 조 — (8공석) · 표 — (3공석) | 조 0/0/0/0 · 표 0/0/0/0 | — | [요청 근거](https://github.com/PyTorchKR/tutorials-kr/blob/2.3.1-latest/beginner_source/introyt/tensors_deeper_tutorial.py#L549-L621) |
| P06b · 가림 | C | 조 T07 (7공석) · 표 T07 (2공석) | 조 0/0/1/0 · 표 0/0/1/0 | C 조 +T07:0→1 / −— / 이동 —<br>C 표 +T07:0→1 / −— / 이동 — | [T07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L2716-L2736) |
| P06b · 가림 | D | 조 T07 (7공석) · 표 T07 (2공석) | 조 0/0/1/0 · 표 0/0/1/0 | — | [T07 근거](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L2716-L2736) |

## 표 3 · 층별 분모, 표시 손익과 비용

적격 요청은 직접/일부/합집합, 쌍은 직접/일부 순이다. 동일·현행·실패는 공개 예정 10건을 분할한 조건부 층이다. 표의 두 뷰는 같은 요청을 반복한다. ‘창’은 B/C/D가 공유한 후보 창 수이며 행 사이에 더하지 않는다. 구간 판독과 후보 적격 기준은 정책별로 반복해 세지 않는다.

| 층·정책 | 예정·실측 요청 | 적격 요청·쌍 | 조사·표시 직접과 일부 | 충돌·미확인·공석 | 규칙 확인·원문 판독 비용 | 두 재생 일치 |
| --- | --- | --- | --- | --- | --- | --- |
| 원문 해시 동일 · 원문 · A | 10/10 | 0/8/8 · 0/17 | 조 0/8 · 표 0/5 · 직접률 산출 불가 | 조 8/26/38 · 표 4/9/12 | 후보/영문/별칭 160/1290/0 · 창 0 · 판독 구간 0 / 쌍 160 | 일치 |
| 원문 해시 동일 · 원문 · B | 10/10 | 0/8/8 · 0/17 | 조 0/8 · 표 0/5 · 직접률 산출 불가 | 조 8/26/38 · 표 4/9/12 | 후보/영문/별칭 160/1290/120 · 창 132 · 판독 구간 0 / 쌍 160 | 일치 |
| 원문 해시 동일 · 원문 · C | 10/10 | 0/8/8 · 0/17 | 조 0/8 · 표 0/5 · 직접률 산출 불가 | 조 8/26/38 · 표 4/9/12 | 후보/영문/별칭 160/1290/120 · 창 132 · 판독 구간 0 / 쌍 160 | 일치 |
| 원문 해시 동일 · 원문 · D | 10/10 | 0/8/8 · 0/17 | 조 0/8 · 표 0/5 · 직접률 산출 불가 | 조 8/26/38 · 표 4/9/12 | 후보/영문/별칭 160/1290/120 · 창 132 · 판독 구간 0 / 쌍 160 | 일치 |
| 원문 해시 동일 · 가림 · A | 10/10 | 0/8/8 · 0/17 | 조 0/7 · 표 0/2 · 직접률 산출 불가 | 조 9/26/38 · 표 5/11/12 | 후보/영문/별칭 160/1290/0 · 창 0 · 판독 구간 0 / 쌍 160 | 일치 |
| 원문 해시 동일 · 가림 · B | 10/10 | 0/8/8 · 0/17 | 조 0/7 · 표 0/2 · 직접률 산출 불가 | 조 9/26/38 · 표 5/11/12 | 후보/영문/별칭 160/1290/120 · 창 132 · 판독 구간 0 / 쌍 160 | 일치 |
| 원문 해시 동일 · 가림 · C | 10/10 | 0/8/8 · 0/17 | 조 0/7 · 표 0/2 · 직접률 산출 불가 | 조 9/26/38 · 표 5/11/12 | 후보/영문/별칭 160/1290/120 · 창 132 · 판독 구간 0 / 쌍 160 | 일치 |
| 원문 해시 동일 · 가림 · D | 10/10 | 0/8/8 · 0/17 | 조 0/7 · 표 0/2 · 직접률 산출 불가 | 조 9/26/38 · 표 5/11/12 | 후보/영문/별칭 160/1290/120 · 창 132 · 판독 구간 0 / 쌍 160 | 일치 |
| 현행 재취득 · 원문 · A | 0/0 | 0/0/0 · 0/0 | 미실행 · 직접률 산출 불가 | 해당 요청 0 | 미실행 | 해당 없음 |
| 현행 재취득 · 원문 · B | 0/0 | 0/0/0 · 0/0 | 미실행 · 직접률 산출 불가 | 해당 요청 0 | 미실행 | 해당 없음 |
| 현행 재취득 · 원문 · C | 0/0 | 0/0/0 · 0/0 | 미실행 · 직접률 산출 불가 | 해당 요청 0 | 미실행 | 해당 없음 |
| 현행 재취득 · 원문 · D | 0/0 | 0/0/0 · 0/0 | 미실행 · 직접률 산출 불가 | 해당 요청 0 | 미실행 | 해당 없음 |
| 현행 재취득 · 가림 · A | 0/0 | 0/0/0 · 0/0 | 미실행 · 직접률 산출 불가 | 해당 요청 0 | 미실행 | 해당 없음 |
| 현행 재취득 · 가림 · B | 0/0 | 0/0/0 · 0/0 | 미실행 · 직접률 산출 불가 | 해당 요청 0 | 미실행 | 해당 없음 |
| 현행 재취득 · 가림 · C | 0/0 | 0/0/0 · 0/0 | 미실행 · 직접률 산출 불가 | 해당 요청 0 | 미실행 | 해당 없음 |
| 현행 재취득 · 가림 · D | 0/0 | 0/0/0 · 0/0 | 미실행 · 직접률 산출 불가 | 해당 요청 0 | 미실행 | 해당 없음 |
| 접근 실패 · 원문 · A | 0/0 | 0/0/0 · 0/0 | 미실행 · 직접률 산출 불가 | 해당 요청 0 | 미실행 | 해당 없음 |
| 접근 실패 · 원문 · B | 0/0 | 0/0/0 · 0/0 | 미실행 · 직접률 산출 불가 | 해당 요청 0 | 미실행 | 해당 없음 |
| 접근 실패 · 원문 · C | 0/0 | 0/0/0 · 0/0 | 미실행 · 직접률 산출 불가 | 해당 요청 0 | 미실행 | 해당 없음 |
| 접근 실패 · 원문 · D | 0/0 | 0/0/0 · 0/0 | 미실행 · 직접률 산출 불가 | 해당 요청 0 | 미실행 | 해당 없음 |
| 접근 실패 · 가림 · A | 0/0 | 0/0/0 · 0/0 | 미실행 · 직접률 산출 불가 | 해당 요청 0 | 미실행 | 해당 없음 |
| 접근 실패 · 가림 · B | 0/0 | 0/0/0 · 0/0 | 미실행 · 직접률 산출 불가 | 해당 요청 0 | 미실행 | 해당 없음 |
| 접근 실패 · 가림 · C | 0/0 | 0/0/0 · 0/0 | 미실행 · 직접률 산출 불가 | 해당 요청 0 | 미실행 | 해당 없음 |
| 접근 실패 · 가림 · D | 0/0 | 0/0/0 · 0/0 | 미실행 · 직접률 산출 불가 | 해당 요청 0 | 미실행 | 해당 없음 |
| 기존 구성 · 원문 · A | 9/9 | 9/5/9 · 12/5 | 조 4/2 · 표 3/2 · 표시 직접률 3/12 | 조 6/5/55 · 표 5/0/17 | 후보/영문/별칭 144/1161/0 · 창 0 · 판독 구간 12 / 쌍 144 | 일치 |
| 기존 구성 · 원문 · B | 9/9 | 9/5/9 · 12/5 | 조 9/3 · 표 8/3 · 표시 직접률 8/12 | 조 7/5/48 · 표 6/0/10 | 후보/영문/별칭 144/1161/108 · 창 896 · 판독 구간 12 / 쌍 144 | 일치 |
| 기존 구성 · 원문 · C | 9/9 | 9/5/9 · 12/5 | 조 9/3 · 표 8/3 · 표시 직접률 8/12 | 조 7/5/48 · 표 6/0/10 | 후보/영문/별칭 144/1161/108 · 창 896 · 판독 구간 12 / 쌍 144 | 일치 |
| 기존 구성 · 원문 · D | 9/9 | 9/5/9 · 12/5 | 조 9/3 · 표 8/3 · 표시 직접률 8/12 | 조 7/5/48 · 표 6/0/10 | 후보/영문/별칭 144/1161/108 · 창 896 · 판독 구간 12 / 쌍 144 | 일치 |
| 기존 구성 · 가림 · A | 9/9 | 9/5/9 · 12/5 | 조 3/2 · 표 3/2 · 표시 직접률 3/12 | 조 4/5/58 · 표 3/0/19 | 후보/영문/별칭 144/1161/0 · 창 0 · 판독 구간 12 / 쌍 144 | 일치 |
| 기존 구성 · 가림 · B | 9/9 | 9/5/9 · 12/5 | 조 9/3 · 표 8/3 · 표시 직접률 8/12 | 조 7/5/48 · 표 6/0/10 | 후보/영문/별칭 144/1161/108 · 창 896 · 판독 구간 12 / 쌍 144 | 일치 |
| 기존 구성 · 가림 · C | 9/9 | 9/5/9 · 12/5 | 조 9/3 · 표 8/3 · 표시 직접률 8/12 | 조 7/5/48 · 표 6/0/10 | 후보/영문/별칭 144/1161/108 · 창 896 · 판독 구간 12 / 쌍 144 | 일치 |
| 기존 구성 · 가림 · D | 9/9 | 9/5/9 · 12/5 | 조 9/3 · 표 8/3 · 표시 직접률 8/12 | 조 7/5/48 · 표 6/0/10 | 후보/영문/별칭 144/1161/108 · 창 896 · 판독 구간 12 / 쌍 144 | 일치 |
| 새 대조 · 원문 · A | 12/12 | 9/5/9 · 10/7 | 조 1/3 · 표 1/3 · 표시 직접률 1/10 | 조 5/1/86 · 표 3/1/28 | 후보/영문/별칭 192/1548/0 · 창 0 · 판독 구간 12 / 쌍 192 | 일치 |
| 새 대조 · 원문 · B | 12/12 | 9/5/9 · 10/7 | 조 5/3 · 표 5/1 · 표시 직접률 5/10 | 조 7/1/80 · 표 5/1/24 | 후보/영문/별칭 192/1548/144 · 창 800 · 판독 구간 12 / 쌍 192 | 일치 |
| 새 대조 · 원문 · C | 12/12 | 9/5/9 · 10/7 | 조 8/3 · 표 8/1 · 표시 직접률 8/10 | 조 8/1/76 · 표 6/1/20 | 후보/영문/별칭 192/1548/144 · 창 800 · 판독 구간 12 / 쌍 192 | 일치 |
| 새 대조 · 원문 · D | 12/12 | 9/5/9 · 10/7 | 조 8/3 · 표 8/1 · 표시 직접률 8/10 | 조 10/1/74 · 표 8/1/18 | 후보/영문/별칭 192/1548/144 · 창 800 · 판독 구간 12 / 쌍 192 | 일치 |
| 새 대조 · 가림 · A | 12/12 | 9/5/9 · 10/7 | 조 1/3 · 표 1/3 · 표시 직접률 1/10 | 조 5/1/86 · 표 3/1/28 | 후보/영문/별칭 192/1548/0 · 창 0 · 판독 구간 12 / 쌍 192 | 일치 |
| 새 대조 · 가림 · B | 12/12 | 9/5/9 · 10/7 | 조 5/3 · 표 4/3 · 표시 직접률 4/10 | 조 7/1/80 · 표 4/1/24 | 후보/영문/별칭 192/1548/144 · 창 800 · 판독 구간 12 / 쌍 192 | 일치 |
| 새 대조 · 가림 · C | 12/12 | 9/5/9 · 10/7 | 조 8/3 · 표 7/3 · 표시 직접률 7/10 | 조 8/1/76 · 표 5/1/20 | 후보/영문/별칭 192/1548/144 · 창 800 · 판독 구간 12 / 쌍 192 | 일치 |
| 새 대조 · 가림 · D | 12/12 | 9/5/9 · 10/7 | 조 8/3 · 표 7/3 · 표시 직접률 7/10 | 조 10/1/74 · 표 7/1/18 | 후보/영문/별칭 192/1548/144 · 창 800 · 판독 구간 12 / 쌍 192 | 일치 |

## Q1 · 같은 발췌판에서 0건을 재검사했다

공개 첫 게시물 10건을 모두 다시 열었다. 원문 NFC SHA-256과 심벌 가림 SHA-256이 각각 10/10 일치했다. 해시가 달라 새로 판독한 현행판 0건, 공개 첫 게시물을 확보하지 못한 요청 0건이다. 공개 raw·JSON 대체 경로 20건은 웹 도구에서 실패했고, 셸의 JSON 표본 1건은 CONNECT 403이었다. 해시의 적용 범위는 웹 텍스트 발췌와 선행의 줄 번호다. 첫 게시 당시 편집 이력과 이미지 픽셀은 미확인이다. [원문 범위·해시](openings.jsonl) · [접근 시도](sources.jsonl)

O3611의 형태로는 끝 어절이 변경인 A12의 첫 어절만 충족한다. O3885의 loader와 O3875의 배치사이즈는 활성 별칭 12개에 해당하지 않는다. O5952의 영어 weight는 모델 파라미터를 뜻한다. D까지 검사해도 이 열 건에 B/C/D 구간은 각각 0건이었다. 이 표본에서는 어절 뒤 조사로 완전 일치 0건을 설명할 근거가 없다. 독립적으로 뽑은 무명 한국어 요청과 새로운 별칭으로 넓힌 효과는 미확인이다. [O3611](https://discuss.pytorch.kr/t/lstm/3611) · [O3885](https://discuss.pytorch.kr/t/model-training-loader/3885) · [O3875](https://discuss.pytorch.kr/t/ddp-batch-size/3875) · [O5952](https://discuss.pytorch.kr/t/pytorch-reshape-coreml-prelu/5952)

## Q2 · 점수와 경계를 고정하고 처음 맞은 정책을 기록했다

A는 별칭 없음, B는 NFC 완전 어절, C는 닫힌 12형 중 하나가 붙은 마지막 어절까지, D는 마지막 어절 내부까지 검사한다. 앞 어절의 내용·순서와 공백 경계를 보존했다. 심벌 12, 서로 다른 일치 문구당 4, 영어 집합 교집합, 동률 ID순 및 조사 8·표시 3은 선행과 같다. C/D를 재생하기 전에 공개 10건과 기존 구성 9건의 A/B 투영 38개 및 순위 1,216행의 선행 필드를 대조했다. [사전 범위](SCOPE.md) · [선행 순위 구현](https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/replay.py) · [영수증](evidence/replay-runs.json)

직접 검사한 경계는 NFC, 탭과 줄바꿈, 문장부호의 단절, 앞 어절 접두사의 거부, 끝 어절 안 접두사의 D 허용, 조사 겹침, 한 어절 안의 복합어, 조사 에서, 중복의 4점 제한 및 영어 심벌 가림이 공백 연결을 만드는 경우다. 마지막 현상은 별도 경계 입력으로 확인했고 실제 31요청의 별칭 구간 수에는 들어가지 않았다. 국립국어원은 로/으로의 받침 조건과 와의 여러 문장 역할을 구별한다. C는 닫힌 철자 규칙만 실험했다. [경계 확인](replay.py) · [국립국어원 받침](https://www.korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=&pageIndex=1&qna_seq=319928) · [국립국어원 문장 역할](https://www.korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=27&pageIndex=1&qna_seq=332869)

## Q3 · 새 구간의 대상과 역할이 갈렸다

원문 뷰 기준 별칭 구간 24개를 순위와 결합하기 전에 판독했다. 가림의 24개를 포함한 48행은 같은 요청의 짝이다. B→C 최초 구간은 뷰당 4개다. P01b에서는 ‘가중치가’로 표본 확률을 지정한다. P02b에서 목적격을 붙인 ‘축 순서를’로 세 축 순열을 지정한다. P06a는 ‘복사본을’ 원하고 P06b는 ‘복사본은’을 써서 독립 사본을 거절한다. C→D의 두 신규 구간은 전치사의 품사와 뷰어의 표시 도구다. 독립 전치도 P03b에서는 언어의 배치를 가리킨다. [오프셋·앞뒤 구절·역할](matches.csv) · [행렬 전치의 호출](https://statisticsplaybook.tistory.com/m/6) · [파일 표시](https://docs.github.com/ko/repositories/working-with-files/using-files/working-with-non-code-files#rendering-csv-and-tsv-data)

한국어 번역 원절에서 데이터로더는 준비한 Dataset의 특징과 레이블을 묶음으로 반환한다. 미니배치로는 표본을 전달하는 방식을 설명한다. 묶음으로는 C가 회수할 수 있는 실제 기술 표현이다. BatchSampler의 결과는 인덱스 목록이다. Tiabet의 가중치는 표본 확률을 가리키고, 텐서 소개의 학습 가중치는 모델 파라미터다. 번역의 계산 히스토리 문맥은 단절을 뜻하는 detach 예와 학습을 위한 추적 유지 예를 모두 포함한다. C05는 유지, C06은 단절을 요구한다. 공식 번역의 전치 주석은 tensor.T 호출을 가리키는 경우도 있다. [로더 원절](https://github.com/PyTorchKR/tutorials-kr/blob/2.3.1-latest/beginner_source/basics/quickstart_tutorial.py#L55-L65) · [미니배치 원절](https://github.com/PyTorchKR/tutorials-kr/blob/2.3.1-latest/beginner_source/basics/data_tutorial.py#L209-L232) · [샘플러 원절](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L357) · [확률 용례](https://tiabet0929.tistory.com/35) · [계산 이력 번역](https://github.com/PyTorchKR/tutorials-kr/blob/2.3.1-latest/beginner_source/introyt/tensors_deeper_tutorial.py#L549-L621) · [tensor.T 번역](https://tutorials.pytorch.kr/beginner/basics/tensorqs_tutorial.html#operation)

A11·A12가 공유하는 선행 개인 저작은 일반·모바일 두 경로에서 열리지 않았다. 선행 별칭을 유지했다. A11의 기능 대응은 고정판 permute의 [2,0,1] 예와 좌표·view 공식 테스트를 읽어 대조했다. A12의 형태 대응은 한국어 튜토리얼의 reshape 예를 사용했다. [실패·대체 원장](sources.jsonl) · [permute 정의](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L8325-L8343) · [reshape 번역](https://tutorials.pytorch.kr/beginner/introyt/tensors_deeper_tutorial.html)

## Q4 · 조사와 표시의 경계가 달랐다

공개층은 모든 정책에서 원문 표시 일부 5/17, 가림 표시 일부 2/17이었다. O5952에서 원문 표시 T02·T01·T07은 PReLU 구현 중 일부씩을 다룬다. 가림 뒤 T02는 1→5위, T01은 2→4위로 조사 안에 남고 T07은 3→10위로 조사 밖까지 내려갔다. 새 표시 T05·D03·D04의 판정은 충돌 1·미확인 2다. 원 저자의 PyTorch 2.2.2와 Core ML 변환 차이는 미확인이다. O4437의 DataLoader 가림은 원문 심벌 2구간을 제거했지만 후보 표시가 유지됐다. [상한 전이](evidence/transitions.csv) · [가림 범위](evidence/forum-audit.jsonl) · [O5952 첫 글](https://discuss.pytorch.kr/t/pytorch-reshape-coreml-prelu/5952)

C01 가림에서 A의 D07은 표시 3위였다. B부터 거절한 D01이 양수 밖→1위에 들어와 D07을 4위로 밀었다. C06은 두 뷰에서 T07 독립 복사가 충돌로 1위, T08 공유·미분 단절이 직접으로 2위다. C09 가림의 전치는 T04를 양수 밖에서 표시 1위로 회복했다. C08의 개별 표본 변환은 D05가 직접이다. 실행에서 NumPy 배열을 바꾸면서 정수 레이블과 배치 축 없는 형태를 보존했다. [등수 원장](ranks.csv) · [역할 판독](matches.csv) · [CPU 관측](evidence/cpu-probe.json)

## Q5 · 여섯 쌍의 기대와 반례를 확인했다

P01b의 D08, P02b의 T03은 B에서 양수 밖이었고 C에서 조사와 표시 모두 1위다. 조사 하나를 붙인 문장에서도 짝과 같은 기능 적격이 유지됐다. P03a 전치사와 P04a 뷰어는 D에서 각각 T04·T01을 양수 밖→1위로 표시했다. 두 행 모두 명시충돌이다. P03b의 독립 전치도 B에서 T04를 표시했다. P04b에서는 지정 연속 입력의 T01이 B에서 표시되고 해당 입력에서 직접인 T02도 별도로 판독됐다. 구성문 선행 기대와 실제 일치/직접 기준은 원문·가림 24개 사본에서 일치했다. [대조문과 기대](controls.jsonl) · [전수 기준](truth.csv) · [구간과 등수](evidence/policy-effects.csv)

P05a와 P05b는 같은 데이터로더 표면을 썼다. P05a는 표본 값 배치를 원하고 BatchSampler의 직접 호출을 거절한다. 가림은 거절한 이름 자체를 지웠으며 나머지 거절 동사는 남는다. P05b는 BatchSampler의 인덱스 목록을 원한다. B/C/D에서 D07은 원문 1위와 가림 4위로 갈렸다. P06a와 P06b도 복사본이라는 같은 명사를 썼다. C에서 각각 직접 T07과 충돌 T07이 1위에 들었다. P06b에서 원하는 T08은 여전히 양수 밖이다. [가림 전후](evidence/controls-audit.jsonl) · [전이](evidence/policy-effects.csv)

지정 CPU의 관측에서 P01 조건은 인덱스 [0,0,0]을 냈다. P02에서 같은 모양을 만들 때 좌표 (1,0,2)의 reshape 값은 8, permute 값은 9였다. 두 transpose를 합성한 경우 permute와 동일 좌표·저장소를 얻었다. P05는 마지막 인덱스 [9]와 마지막 표본 [109]를 구분했다. P06에서 clone의 조밀 비연속 stride [1,3]과 미분 경로가 보존됐고 detach 쪽 쓰기만 원본에 전파됐다. [CPU 관측](evidence/cpu-probe.json) · [view 공식 시험](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/test/test_view_ops.py#L775-L839) · [detach 공식 시험](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/test/test_autograd.py#L3783-L3838)

## Q6 · 손익의 분모와 확인 비용

31개 요청의 두 뷰에서 248회 조회와 3,968개 기능 점수, 496개 판정 쌍을 검산했다. 304쌍은 선행 입력 해시와 구성 원문을 확인해 연결했고 192쌍은 새 대조에 봉인했다. 공개 10건은 직접 적격 쌍 0으로 회수율 산출 불가다. 기존 구성 9건은 직접 12쌍 중 원문 표시가 A 3→B 8이고 가림도 3→8이다. B/C/D 사이에 기존 구성 표시 증감은 0이다. [집계](evidence/metrics.json) · [공석 원장](evidence/slots.csv)

새 대조 12건의 직접 기준은 9요청·10쌍이다. B→C에서 원문은 직접 표시 5→8, 가림은 4→7이다. 뷰마다 조사와 표시에서 직접 3·충돌 1이 유입됐으며 탈락은 0이다. 일부와 미확인에는 변화가 없다. C→D의 유입은 뷰마다 충돌 2이며 탈락과 직접·일부 증감은 0이다. 추가 충돌이 모두 빈 자리에 들어갔다. 기존 구성 C01의 A→B 직접 손실과 새 구성 P05b의 이름 가림에서 한 단계 더 생긴 표시 손실은 별도 전이다. [전이별 판정](evidence/policy-effects.csv) · [분모](evidence/metrics.json)

각 뷰의 정책당 전수 후보 확인은 496번, B/C/D의 별칭 문구 확인은 각각 372번이다. B/C/D 구현이 공유한 보존 후보 어절창은 뷰당 1,828개다. 원문 판독에는 10개 첫 게시물과 21개 구성문, 서로 다른 24개 별칭 구간이 들었다. 출처 원장은 68개 기록 중 직접 확인 행 39개와 계보를 합친 고유 1차 저작 38개를 담는다. 한국어 작성자 10, 기술 용례·문법 11, 고정판 정의·공식 시험 9, 철도 3, 도서관 5다. 실패한 대체 경로 28행과 메타데이터만 읽은 1행은 고유 자료 수에서 제외했다. 읽는 시간, 클릭과 이해는 미확인이다. [저작과 접근 원장](sources.jsonl) · [검사량](evidence/replay-costs.csv)

## Q7 · 철도·도서관과 적용 후보

부산교통공사의 1호선 원문에서 부산은 CODE 113, 부산대는 CODE 128이다. D가 부산대 안에서 부산을 찾으면 다른 역 링크가 된다. 같은 원장에는 113의 부산과 부산역을 함께 읽는 정차 안내도 있다. 부산역입니다의 D 적중은 같은 역이고 닫힌 C의 철자 조건 밖이다. 운영기관이 같은 ID에 연결한 호칭을 저장하면 이 경우를 따로 검토할 수 있다. 공항철도 공지의 서울역에서와 서울역에는 같은 표제에 출발·도착 역할을 각각 붙인다. C는 역 표제를 회수하고 방향은 안내문에서 별도 판독한다. 송파구의 실제 안내에서는 잠실나루역 3번과 잠실역 7·8번 출구가 갈린다. [부산 113](https://work.humetro.busan.kr/homepage/default/broadcast/list.do?CODE=113&SUB_CODE=1) · [부산대 128](https://work.humetro.busan.kr/homepage/default/broadcast/list.do?CODE=128&SUB_CODE=1) · [공항철도 원문](https://m.arex.or.kr/contentView.do?contentNo=CT202609160000000001&etcNo=&menuNo=MN202602270000000001) · [출구 안내](https://www.songpa.go.kr/www/contents.do?key=2657)

한국문학번역원의 토지 원작은 102781이며 작가 200092에 연결된다. 국토연구원 전자도서관의 토지이용계획론은 기록 5931117, ISBN 9788978397070이다. D의 내부 적중을 서명 동일성으로 쓰면 작품과 전문서를 혼동한다. 토지 이용 계획이 주제인 검색에서는 후자가 유의미하다. 박경리와 박금이는 A–D의 글자열 비교에서 연결되지 않는다. 국립중앙도서관의 전거 예와 한국문학번역원 작가 기록의 ISNI 0000000081196148이 인명의 연결 근거를 제공한다. 일곱 도메인 대조는 별도 분모다. [도메인 재생](evidence/domain-cases.csv) · [토지](https://library.ltikorea.or.kr/originalworks/102781) · [토지이용계획론](https://library.krihs.re.kr/%24/10110/contents/5931117) · [작가 기록](https://library.ltikorea.or.kr/writer/200092) · [국립중앙도서관 검색 안내](https://www.nl.go.kr/NL/contents/N71200000000.do)

| 사례 | 별칭은 조사까지 허용하고 A의 표시를 유지 | 별칭 점수로 표시까지 갱신 | 조합 조건 |
| --- | --- | --- | --- |
| P01b·P02b, 가림 | D08·T03을 각각 조사 목록에서 읽을 수 있다. 화면은 공석이다. | C에서 해당 직접 링크가 각각 1위다. | 확률·인덱스 또는 세 축·공유 조건을 카드에서 확인하면 표시 후보로 삼는다. |
| C01·P05b, 가림 | C 조사 안에서 A의 D07 3위를 표시한다. | C 화면 1위에 D01이 들어오고 D07이 4위로 밀린다. | 공개 iterator 출력과 요청의 인덱스 반환 조건이 다르면 로더 승격을 보류한다. |
| C06, 가림 | 두 링크를 조사하며 화면은 공석이다. | C가 충돌 T07을 1위, 직접 T08을 2위에 표시한다. | 저장소 공유와 미분의 단절을 별도 조건으로 기록한다. |
| P06a·P06b, 가림 | P06a의 기존 표시 T01·T05와 P06b의 공석이 유지된다. T07 두 건은 조사할 수 있다. | C가 두 요청 모두 T07을 1위로 올린다. P06a는 직접, P06b는 충돌이다. | 역할과 저장소 요구를 확인한 경우에 한해 표시한다. |
| P03a·P04a, 가림 | D 조사에 오탐 두 건이 들어오고 A 표시의 공석이 유지된다. | D가 텐서 기능을 각각 1위에 표시한다. | 요청 대상·입력형을 연결할 직접 근거를 찾기 전에는 관련 링크로만 검토한다. |

한국어 작성자에게는 조사 때문에 놓친 링크를 보여 주고 인덱스·저장소·거절 조건을 함께 표시할 가치가 있다. 번역 편집자에게는 부품명, 반환물, 호출 예와 예외의 관계를 기록하는 비용이 생긴다. 사전 유지자는 별칭 12개의 원절, 한 표면의 기능과 제약, 현행 주소 실패를 검토하고, 표시에서 밀리는 링크를 점검해야 한다. 표의 조사 전용 안은 조회 시뮬레이션이다. 독자가 검토한 시간과 최종 채택은 미측정이다. [조사 전용 전수 대조](evidence/investigation-only.csv) · [별칭 사전의 출전](https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/aliases.csv)

- **조건부 채택** · C를 조사 후보에 적용한다. P01b·P02b의 직접 링크를 회복한 경우와 P06b처럼 거절한 출력이 조사에 든 경우를 판독한다. 검토 비용은 조사에서 읽을 유입 후보 수로 기록한다.
- **조합** · 표시 단계는 원절의 발화 역할, 기능 입출력과 보존 조건, 조사·표시 경계에서 밀린 ID를 함께 본다. 확인을 기다리는 자리와 유효 링크의 보류를 기록한다.
- **보류** · D의 표시 승격은 현 증거에서 보류한다. 부산역 호칭이나 도서관 전거처럼 문서에 적힌 동일 ID 관계가 있는 경우에는 별도의 연결 근거로 비교한다.

| 불일치·약점 | 다음 조사 자료·행동 | 판정을 바꿀 관측 |
| --- | --- | --- |
| 공개 10건에서 별칭 경계 효과 0건이고 직접 적격이 있는 회복은 구성층에서 관측됐다. | 활성 별칭과 실제 직접 적격이 함께 있는 새 한국어 저자 #1 원문을 사전 정의한 표본으로 확보한다. | 동일 기능을 지칭하는 조사 결합이 실제 저자 문장에서 조사·표시의 직접 회복으로 반복된다. |
| 지칭 회복 뒤에도 C01·C06·P05b·P06b의 역할과 입출력 충돌이 남았다. | 독립 검토자가 순위 없이 구절·출력형을 판독하고, 같은 사례에서 조사 전용과 역할 확인 후 표시를 비교한다. | 원문의 직접 링크를 유지하면서 거절·반대 출력의 표시와 후속 판독 비용이 함께 줄어든다. |
| 가림에서 P05a의 거절 이름이 사라지고 O5952의 일부 링크 세 개가 표시에서 빠졌다. | 각 쌍의 원문·가림에서 사라진 이름과 보존된 역할을 독립 판독하고, 자연 원문에 이름이 없는 요청을 별도로 확보한다. | 역할 판독이 유지되는 가림에서도 같은 일부 손실이 반복되거나, 이름 없는 원문에서 다른 회수 경향이 관측된다. |
