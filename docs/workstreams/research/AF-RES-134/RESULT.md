# AF-RES-134 · PARTIAL

## 표 1 · 모집층과 원저자 열람

| 모집층·창 | 예정·실제 응답·원저자 첫 글 열람 | 제외·중복·미확인 | 적격 채택·저자 | 판·시각·출처 |
| --- | --- | --- | --- | --- |
| A · PyTorchKR ID 6001–6064 | 64 ID 예정, JSON origin 응답 0/64, 공개 HTML #1 열람 1/64 | 홍보 제외 1, 63 ID의 원문·존재 미확인, 중복 판독 0건 | 관측 0건/0명, 상한 8건 | 2026-11-24 11:19–11:21 UTC. [HTTP](evidence/forum-http.jsonl) · [HTML](evidence/forum-html.jsonl) |
| B · 사이트 자체 가중치·복사본·전치·데이터로더 | 4질의×8슬롯 예정, 검색 JSON 응답 0/4, 원저자 첫 글 열람 0건 | 질의 배열과 32 예정 슬롯 미관측, 제외·중복 미확인 | 채택 0건/0명 관측, 실제 적격 미확인, 상한 질의당 2건 | 2026-11-24 11:19–11:21 UTC. [검색 시도](evidence/forum-http.jsonl) · [모집 원장](frame.csv) |
| G1 · deeplearningzerotoall/PyTorch | 최대 40슬롯, 공식 1페이지 22 ID 반환·22/22 열람, 나머지 18은 목록 끝 | 제외 18, 중복 0, 첨부 의존 판독 유보 2 | 2건/2명, 목표 8건 | 2026-11-24 11:21:03.779 UTC 고정, 마지막 #48. [검색](evidence/g1-search.jsonl) · [창](evidence/g1-window.jsonl) |
| G2 · pytorch 어떻게 | 최대 24슬롯, 공식 3페이지 30 후보 응답 중 첫 24/24 고정·열람 | 제외 21, 중복 0, 본문 결측 0 | 3건/3명 | 2026-11-24 11:21:48.697 UTC, 24번 HwangToeMat/VDSR_Pytorch_HTM#1. [검색](evidence/g2-how-search.jsonl) · [창](evidence/g2-how-window.jsonl) |
| G2 · pytorch 싶습니다 | 최대 24슬롯, 공식 3페이지 22 ID·22/22 열람, 나머지 2는 목록 끝 | 제외 16, 중복 5, 본문 결측 0 | 1건/1명 | 2026-11-24 11:21:48.371 UTC, 22번 LISTatSNU/FastMRI_challenge#246. [검색](evidence/g2-want-search.jsonl) · [창](evidence/g2-want-window.jsonl) |

G1·G2는 68열람 슬롯, 66개 고유 첫 글 URL, 동일 첫 글 2회와 동일 FAQ 재게시 3회를 통합한 63개 원문 계보에서 6건·6명의 비교 가능 요청을 확보했다. A/B와 미접근 포럼의 교차 중복 여부는 미확인이다. 전체 고정 판독 대상은 관측된 6건이다. [원장 재집계](evidence/recount.json) · [판독 기준](SCOPE.md)

## 표 2 · 요청 역할, 카드 원절과 조사·표시

위치는 `조사8 / 표시3`로 적었다. ∅는 그 카드가 해당 단계에 들지 않은 자리다. 모두 0점인 질문은 실제 공석을 표시했다. C 조사 범위에 있던 카드와 충돌 기준의 0점 카드 D05를 실었다. 나머지 쌍은 6×16×3 전수 원장에서 확인할 수 있다. [전수 기준](truth.csv) · [순위](ranks.csv) · [공석](evidence/slots.csv)

| 요청·역할 | 카드·원절 URL | 보존·반대 조건 | 기준 등급 | B 조사/표시 | C 조사/표시 | Gate 조사/표시 | 진입·탈락·공석 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [G1-39](https://github.com/deeplearningzerotoall/PyTorch/issues/39#issue-717173320) · 수식과 일치하는 reduction | 고정 16카드 양점 없음 | scalar loss 가설, 첨부 수식과 차원 미확인; mean vs sum은 배치 크기 1에서도 우연히 같을 수 있다. | 미확인 16쌍 | 8/3 공석 | 8/3 공석 | 8/3 공석 | 양점 후보 없음 |
| [G1-40](https://github.com/deeplearningzerotoall/PyTorch/issues/40#issue-717595288) · bias 축 평균/결과 동일성 | 고정 16카드 양점 없음 | 배치 축/shape·브로드캐스트가 본문에서 확정되지 않는다. diff 미분 질문은 별도 목표다. | 미확인 16쌍 | 8/3 공석 | 8/3 공석 | 8/3 공석 | 양점 후보 없음 |
| [G2-how-19](https://github.com/kakao/khaiii/issues/94#issue-694826524) · 말뭉치 평가 라벨 ID | [D01](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) | 태그 사전 조회 실패, OOV 처리 미확인 | 미확인 | 1/1 | 1/1 | 1/∅ | C→Gate 표시 탈락·보류 |
| G2-how-19 | [D02](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataset.py#L77-L164) | 태그 사전 조회 실패, OOV 처리 미확인 | 미확인 | 2/2 | 2/2 | 2/∅ | C→Gate 표시 탈락·보류 |
| G2-how-19 | [D03](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataset.py#L193-L214) | 태그 사전 조회 실패, OOV 처리 미확인 | 미확인 | 3/3 | 3/3 | 3/∅ | C→Gate 표시 탈락·보류 |
| G2-how-19 | [D06](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataset.py#L393-L422) | 태그 사전 조회 실패, OOV 처리 미확인 | 미확인 | 4/∅ | 4/∅ | 4/∅ | Gate 후보 검토·보류 |
| G2-how-19 | [D07](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L293-L357) | 태그 사전 조회 실패, OOV 처리 미확인 | 미확인 | 5/∅ | 5/∅ | 5/∅ | Gate 후보 검토·보류 |
| [G2-how-20](https://github.com/Beomi/KcBERT/issues/3#issue-695999584) · TSV 5레이블 적재·모델 계약 | [T01](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6176) | 동일 TSV 열과 5클래스 보존, logits·target 호환 확인 필요 | 미확인 | 1/1 | 1/1 | 1/∅ | C→Gate 표시 탈락·보류 |
| G2-how-20 | [T02](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L9257-L9294) | 동일 TSV 열과 5클래스 보존, logits·target 호환 확인 필요 | 미확인 | 2/2 | 2/2 | 2/∅ | C→Gate 표시 탈락·보류 |
| G2-how-20 | [T05](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6240-L6281) | 동일 TSV 열과 5클래스 보존, logits·target 호환 확인 필요 | 미확인 | 3/3 | 3/3 | 3/∅ | C→Gate 표시 탈락·보류 |
| G2-how-20 | [D04](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/_utils/collate.py#L337-L398) | 동일 TSV 열과 5클래스 보존, logits·target 호환 확인 필요 | 미확인 | 4/∅ | 4/∅ | 4/∅ | Gate 후보 검토·보류 |
| G2-how-20 | [T03](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L8325-L8346) | 동일 TSV 열과 5클래스 보존, logits·target 호환 확인 필요 | 미확인 | 5/∅ | 5/∅ | 5/∅ | Gate 후보 검토·보류 |
| G2-how-20 | [T06](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L4154-L4183) | 동일 TSV 열과 5클래스 보존, logits·target 호환 확인 필요 | 미확인 | 6/∅ | 6/∅ | 6/∅ | Gate 후보 검토·보류 |
| G2-how-20 | [T07](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L2716-L2736) | 동일 TSV 열과 5클래스 보존, logits·target 호환 확인 필요 | 미확인 | 7/∅ | 7/∅ | 7/∅ | Gate 후보 검토·보류 |
| G2-how-20 | [D01](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L201) | 동일 TSV 열과 5클래스 보존, logits·target 호환 확인 필요 | 미확인 | 8/∅ | 8/∅ | 8/∅ | Gate 후보 검토·보류 |
| [G2-how-24](https://github.com/HwangToeMat/VDSR_Pytorch_HTM/issues/1#issue-714769321) · HDF5 표본 배치 | [D01](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L410-L415) | 단일 프로세스 허용과 HDF5 dataset 접근 필요 | 직접 | 1/1 | 1/1 | 1/∅ | C→Gate 표시 탈락·보류 |
| G2-how-24 | [D04](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/_utils/collate.py#L337-L398) | 표본 결합만, worker 직렬화가 먼저 실패 | 일부 | 2/2 | 2/2 | 2/∅ | C→Gate 표시 탈락·보류 |
| G2-how-24 | [D07](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L293-L357) | list[int]를 표본 배치로 읽으면 충돌 | 충돌 | 3/3 | 3/3 | 3/∅ | C→Gate 표시 탈락·보류 |
| G2-how-24 | [D08](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L290) | 확률적 int 인덱스를 표본 배치로 읽으면 충돌 | 충돌 | 4/∅ | 4/∅ | 4/∅ | Gate 후보 검토·보류 |
| G2-how-24 | [T07](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L2716-L2736) | 표본 배치와 Windows worker 직렬화, 병렬성 미확인 | 미확인 | 5/∅ | 5/∅ | 5/∅ | Gate 후보 검토·보류 |
| G2-how-24 | [D05](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/_utils/collate.py#L23-L107) | 단일 샘플 출력으로 배치 계약 위반 | 충돌 | ∅/∅ | ∅/∅ | ∅/∅ | 세 안 0점 |
| [G2-want-18](https://github.com/deep-learning-with-projects/deep-learning-with-projects/issues/18#issue-1173645126) · 중복 log softmax 제거 | 고정 16카드 양점 없음 | raw logits→cross entropy 또는 log probs→NLL. 본문 요구는 모델이 써야 하는 loss 계약이다. | 미확인 16쌍 | 8/3 공석 | 8/3 공석 | 8/3 공석 | 양점 후보 없음 |

## 표 3 · 층별 정책 분모와 짝지은 변화

조사8과 표시3의 튜플 순서는 `직접·일부·충돌·미확인·공석`이며 단위는 자리다. 정책 변화는 같은 요청·카드의 `얻은 직접·잃은 직접·추가 충돌·해소 충돌` 순서다. 비교는 C에서 B로 되짚고 Gate에서 C로 되짚었다. B는 기준이다. [재현 집계](evidence/metrics.csv) · [짝지은 이동](evidence/transitions.csv) · [편집 원절 수](evidence/editor-cost.csv)

| 층·정책 | 비교 요청 / 전수 쌍 | 직접 있는 요청 / 직접 쌍 | 조사8 등급·공석 / 예정 자리 | 표시3 등급·공석 / 예정 자리 | 조사8 / 표시3 변화 쌍 | 추가 원절 수·미확인 |
| --- | --- | --- | --- | --- | --- | --- |
| 포럼 A · B | 0건 / 0쌍 | 미확인 | 산출 불가 | 산출 불가 | 산출 불가 | 미실시 · 63 ID 미확인 |
| 포럼 A · C | 0건 / 0쌍 | 미확인 | 산출 불가 | 산출 불가 | 산출 불가 | 미실시 · 63 ID 미확인 |
| 포럼 A · Gate | 0건 / 0쌍 | 미확인 | 산출 불가 | 산출 불가 | 산출 불가 | 미실시 · 63 ID 미확인 |
| 포럼 B · B | 0건 / 0쌍 | 미확인 | 산출 불가 | 산출 불가 | 산출 불가 | 미실시 · 4질의 응답 미확인 |
| 포럼 B · C | 0건 / 0쌍 | 미확인 | 산출 불가 | 산출 불가 | 산출 불가 | 미실시 · 4질의 응답 미확인 |
| 포럼 B · Gate | 0건 / 0쌍 | 미확인 | 산출 불가 | 산출 불가 | 산출 불가 | 미실시 · 4질의 응답 미확인 |
| G1 · B | 2건 / 32쌍 | 0건 / 0쌍 | 0·0·0·0·16 / 16자리 | 0·0·0·0·6 / 6자리 | 기준 | 0개 · 실제 사용자 확인 미실시 |
| G1 · C | 2건 / 32쌍 | 0건 / 0쌍 | 0·0·0·0·16 / 16자리 | 0·0·0·0·6 / 6자리 | 0·0·0·0 / 0·0·0·0 | 0개 · 실제 사용자 확인 미실시 |
| G1 · Gate | 2건 / 32쌍 | 0건 / 0쌍 | 0·0·0·0·16 / 16자리 | 0·0·0·0·6 / 6자리 | 0·0·0·0 / 0·0·0·0 | 0개 · 실제 사용자 확인 미실시 |
| G2 · B | 4건 / 64쌍 | 1건 / 1쌍 | 1·1·2·14·14 / 32자리 | 1·1·1·6·3 / 12자리 | 기준 | 0개 · 실제 사용자 확인 미실시 |
| G2 · C | 4건 / 64쌍 | 1건 / 1쌍 | 1·1·2·14·14 / 32자리 | 1·1·1·6·3 / 12자리 | 0·0·0·0 / 0·0·0·0 | 0개 · 실제 사용자 확인 미실시 |
| G2 · Gate | 4건 / 64쌍 | 1건 / 1쌍 | 1·1·2·14·14 / 32자리 | 0·0·0·0·12 / 12자리 | 0·0·0·0 / 0·1·0·1 | 28개 · 실제 사용자 확인 미실시 |
| 관측 G1·G2 · B | 6건 / 96쌍 | 1건 / 1쌍 | 1·1·2·14·30 / 48자리 | 1·1·1·6·9 / 18자리 | 기준 | 0개 · 실제 사용자 확인 미실시 |
| 관측 G1·G2 · C | 6건 / 96쌍 | 1건 / 1쌍 | 1·1·2·14·30 / 48자리 | 1·1·1·6·9 / 18자리 | 0·0·0·0 / 0·0·0·0 | 0개 · 실제 사용자 확인 미실시 |
| 관측 G1·G2 · Gate | 6건 / 96쌍 | 1건 / 1쌍 | 1·1·2·14·30 / 48자리 | 0·0·0·0·18 / 18자리 | 0·0·0·0 / 0·1·0·1 | 28개 · 실제 사용자 확인 미실시 |

## Q1–Q2 · 모집과 접근

포럼 A와 B는 **PARTIAL**이다. 지정한 두 probe에서 원본 HTTP 상태와 콘텐츠 타입을 관측하지 못했다. CONNECT 403은 프록시 실패였고, DNS 실패·HTTP 삭제·서버 오류 판정으로 옮기지 않았다. 6027의 공개 HTML 1번은 출시 홍보였으며 같은 topic JSON과의 post ID 일치는 미확인이다. 자체 검색 배열과 마지막 ID는 네 질의 모두 미확인이다. [회수 영수증](evidence/intake.md)

G1·G2의 관측 창 고정과 채택 6건에 대한 재생은 **DONE**, 비교 가능한 한국어 질문 8저자 목표는 **PARTIAL**이다. 상태 필터 없이 읽었다. G1에서 미확인인 #30과 #43은 첨부 그림 없이는 조작 객체나 출력을 구체화하기 어려웠다. G2에는 번역, 운영 FAQ, 기능계획 양식, 제3자 인용과 로그 키워드가 섞였다. 어떻게 검색 페이지가 세 번째까지 30개를 노출했으며 24번째까지만 모집했다. 두 G2 질의는 사이트가 취득 시각에 돌려준 순위이고 B층을 대신하지 않는다. [모집과 제외](frame.csv) · [공개 첫 본문 해시](evidence/github-openings.jsonl)

## Q3–Q4 · 이름, 요청 출력과 표시 근거

| 확인한 구별 | 실제 판독과 적용 조건 | 한계 |
| --- | --- | --- |
| 표본별 가중치와 모델 가중치 | 제외 원문 G2-how-5에서 `가중치를`의 대상은 모델 체크포인트다. 실제 NFC 어절에서 C는 A10을 잡는다. D08의 출력은 정수 인덱스다. [원문](https://github.com/sooftware/kospeech/issues/27) · [고정 sampler](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L290) | 적격 효과 분모 밖. 공식 D08은 가중 순위 정렬이나 모델 parameter를 다루지 않는다. |
| 텐서 사본, 공유 view와 장치 전송 | 포럼 3155는 데이터량을 유지한 장치 복사 속도를 원한다. 51995는 원소별 확대 비교에 메모리 복사를 피하려 한다. view의 stride/원소수 조건, 일부 reshape의 복사, clone의 grad 연결, detach의 공유를 각각 읽었다. [전송 #1](https://discuss.pytorch.kr/t/host-cpu-gpu-memory-copy-speedup/3155) · [무복사 #1](https://discuss.pytorch.org/t/view-tensor-as-larger-tensor-without-copying-memory/51995) · [회귀](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/test/test_view_ops.py#L775-L834) | 사례는 모집 창 밖이다. 51995의 무복사는 가능한 경우라는 선호다. 런타임·성능·사용자 반응은 미실시. |
| 인덱스 묶음과 실제 표본 배치 | D07의 list[int], fetch의 실제 자료 조회, D04의 결합, D05의 단일 샘플 변환을 따로 읽었다. 일반 tuple 안의 결과가 list인 예와 문자열 유지·가변 길이 오류 시험도 확인했다. [fetch](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/_utils/fetch.py#L46-L55) · [collate](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/_utils/collate.py#L337-L380) · [loader 회귀](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/test/test_dataloader.py#L2314-L2337) | G2-how-24에서 병렬성이 필수면 D01 단독은 일부다. 단일 작업자 조건은 실측한 원문 머신이 아닌 핀의 코드 판독이다. |
| 구절의 화자와 영어 심벌 | 원문의 주석·변수·오류 로그를 보존하되 목표 구절과 다르게 표시했다. 자연 심벌이나 이름은 고정 16카드 바깥에도 있었다. 원저자 설명에 공개 API 이름이 직접 나타난 요청은 G1-39·G1-40·G2-want-18의 3건/6건이다. 나머지 3건에는 공개 API 이름이 목표 문구에 없었다. 카드 정확 심벌이 있는 요청 1건/6건은 G2-how-20의 trace `.view`, 나머지 5건/6건은 고정 심벌 가점이 없었다. [요청 NFC 구절](requests.jsonl) · [심벌과 역할](evidence/role-boundaries.jsonl) | 심벌 가점 없음은 영문 API를 전혀 언급하지 않았다는 뜻과 다르다. bodyVersion, createdAt, updatedAt을 보존했으나 본문 공개 편집 시각이 별도 필드로 확인되지 않았다. |
| 조사·출력 근거 | 국립국어원은 한 개뿐 아니라 연속 조사도 앞말에 붙인다. 직접 인용 종결 구두점의 경우에는 따옴표 뒤 조사를 안내한다. 한국어 실제 사용의 `뷰`, `전치`, `가중치를`와 로그 앱 `뷰어`는 역할별로 읽었다. [§41 답변](https://www.korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&pageIndex=1&qna_seq=321432&searchCondition=&searchKeyword=) · [자료 원장](sources.jsonl) | C는 12개 단일 끝조사와 고정 경계만 허용한다. 인용·합성어·의미 역할은 이 규칙의 성능 보장 범위 밖이다. |

6×16=96쌍의 표시 판독은 기준과 점수 전에 고정했다. 별도 전수 기준에서 직접 1, 일부 1, 충돌 3, 미확인 91쌍이었다. 같은 판독자가 두 기록을 작성했다. G2-how-24의 기준은 단일 프로세스가 허용되는 경우 D01을 직접으로 판정한다. Gate는 배치가 저자 목표 문구보다 traceback에 드러나고 작업자·배치 보존이 명시되지 않아 보류했다. 단일 프로세스를 허용하는 경우 원저자는 유용한 링크 한 건을 잃는다. 병렬성이 필수인 경우 단일 프로세스 링크는 진단용 일부로 내려가며 직접 링크 손실 주장은 적용되지 않는다. [표시 판독](display-review.csv) · [전수 기준](truth.csv)

## Q5–Q6 · 정책 차이와 운영 비용

B와 C는 채택 여섯 본문에서 활성 별칭 적중 0건이어서 양점 순서·조사·표시가 모두 일치했다. 그래서 조사 하나의 회수나 밀림을 실제 적격 요청에서 관측할 기회가 없었다. 제외 원문의 A10 적중과 `뷰어`의 넓은 부분 문자열 반례는 경계의 설명이며 이 여섯 건의 정책 효과에 산입하지 않았다. [적중 장부](evidence/alias-audit.csv) · [경계 반례](evidence/counterexamples.md)

C→Gate는 G2 조사 18 양점 자리와 14공석을 유지했다. 표시에서는 G2-how-24의 D01 직접 1, D04 일부 1, D07 충돌 1과 두 요청의 미확인 6쌍을 보류했다. 유입은 0쌍이었다. 표시 9자리의 추가 공석이 생겨 GitHub 관측 전체 18자리 전부가 공석이었다. G2-how-24의 D08 충돌은 조사 4위에 남았고 D05 충돌은 0점이었다. [짝지은 이동](evidence/transitions.csv) · [전수 순위](ranks.csv)

관측 6건에서 데이터 역할 3건·48쌍만 직접 후보 1건을 포함했다. 텐서 계산 역할 3건·48쌍은 고정 카드의 직접 근거 0이었다. 카드 정확 심벌이 있는 1건·16쌍에서 표시 미확인 3개를 보류했다. 정확 심벌이 없는 5건·80쌍에서 표시 직접 1과 충돌 1을 함께 보류했다. 19개 G1 저자 키와 35개 G2 저자 키가 반환 창에 있었고 G2의 미식별 저자는 1슬롯이다. G1의 교육 이슈와 G2의 반복 작성자·설치·템플릿이 모집에 영향을 준다. 분모가 서로 다른 포럼 층 및 사이트 검색 노출은 채택 가능성을 일반화할 수 없다. [모집 원장](frame.csv) · [역할·심벌 하위층](evidence/metrics.csv)

| 읽는 사람 | 이 표본에서 바꿔 줄 링크와 조건 | 비용과 보류 |
| --- | --- | --- |
| 요청 작성자 | HDF5 작업자 예외에는 단일 프로세스가 허용될 때 loader의 작업자 분기와 Windows spawn 원절을 먼저 읽을 수 있다. 5레이블 오류는 분류 출력 차원/target 계약을 확인할 근거가 우선한다. [작업자 분기](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L410-L415) · [Windows 원절](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/docs/source/data.rst#L329-L351) | 원저자의 클릭·이해·채택·해결은 미실시. 16카드에 대응 원절이 없는 질문에는 추가 맥락이 필요하다. |
| 카드 관리자 | 12개 활성 별칭의 이름·입력·출력을 유지한다. 가중치 역할을 모델 파라미터 및 표본 확률로, 묶음을 인덱스와 표본으로 확인할 필요가 있다. [고정 별칭](https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/aliases.csv) | 사전 전수 검토는 이번 정책의 실제 신규 유지비로 계측하지 않았다. |
| 편집자 | 조사 목록에서 요청 구절과 출력 API를 같이 확인한다. 클릭 전제로 옮기지 않고 후보 18개와 요청 구절 10개, 합계 28원절을 편집 검토량으로 계산했다. 96쌍 사전 판독은 별도 작업량이다. [원절비용](evidence/editor-cost.csv) | 순수 Gate는 직접·충돌을 둘 다 숨길 수 있다. `단일 프로세스 허용`처럼 보존 조건을 한 가지 확인해 표시할 수 있을지는 새 검증 가설이다. |

## Q7 · 철도와 도서관의 식별자 및 역할

| 원문 비교 | 문자열 판정 | 식별자와 역할을 읽은 뒤 | 추가 확인 뒤 남은 조건 |
| --- | --- | --- | --- |
| MTA 23 St 네 역 | R/W, C/E, F/M, 1 표제가 같아 한 시설로 합쳐진다. | 정류장 ID는 R19, A30, D18, 130이며 단지 ID도 다르다. R/W의 같은 Broadway 역은 R19 한 개다. [MTA 역 자료](https://data.ny.gov/resource/39hk-dx4f.json) · [R 지도](https://www.mta.info/maps/subway-line-maps/r-line) · [W 지도](https://www.mta.info/maps/subway-line-maps/w-line) · [1 지도](https://www.mta.info/maps/subway-line-maps/1-line) | `23 St, Downtown`만으로는 노선이 다른 같은 이름 후보가 남는다. 실제 가까운 교차로와 승차 노선이 필요하다. |
| MTA 6의 23 St 표기와 방향 | `23 St`와 `23 St-Baruch College`는 다르게 잡힌다. | Park Avenue South 6호선의 GTFS 정류장 634, 역/단지 MRN 405에 대응한다. 같은 이름 안에서 Downtown 승강장 엘리베이터는 23rd St 북서, Uptown은 북동 모서리다. [6 지도](https://www.mta.info/maps/subway-line-maps/6-line) · [방향 안내](https://www.mta.info/accessibility/stations) · [역 ID](https://data.ny.gov/resource/39hk-dx4f.json) | 공식 정규 GTFS ZIP은 접근하지 못해 승강장 자식 stop ID를 별도로 대조하지 않았다. 안내판과 이 표의 시각은 고정 관측이다. |
| MTA Times Square 이름 이형 | 숫자·약어가 다른 두 이름을 다르게 잡는다. | 작품 자료의 Times Sq-42 St 표제와 Times Square-42nd Street Station 캡션은 단지 611에서 같은 대상을 가리킨다. 127·R16·725·902는 그 안에서 다른 노선 정류장이다. [작품 원문](https://www.mta.info/agency/arts-design/collection/return-of-spring) · [역 자료](https://data.ny.gov/resource/39hk-dx4f.json) | 이름·단지 ID는 접근 시설을 좁히지만 승강장/방향에는 노선 및 개별 stop ID가 필요하다. |
| BnF Baudelaire 세 역할과 이형 | 세 레코드에서 표목을 찾으면 모두 저자라고 오인한다. Charles Pierre 변형은 누락한다. | Les fleurs du mal cb37367035f는 저자, Histoires extraordinaires cb474837353은 번역자, cb41169554h 안의 La statue de Baudelaire는 주제다. 세 역할 링크가 모두 인물 전거 cb118905823으로 간다. Charles Pierre와 Dufaÿs는 해당 전거의 이형이다. [저자](https://catalogue.bnf.fr/ark:/12148/cb37367035f) · [번역자](https://catalogue.bnf.fr/ark:/12148/cb474837353) · [주제](https://catalogue.bnf.fr/ark:/12148/cb41169554h) · [전거](https://catalogue.bnf.fr/ark:/12148/cb118905823) | 올바른 사람 ID라도 역할을 빼면 번역서를 저작으로 분류한다. 서지 판·부분 자료는 각각 역할을 확인해야 한다. |
| BnF Alexandre Dumas 부자 | 이름과 저자 역할만 남은 입력은 둘 다 매치한다. | cb119010630(1802–1870)과 cb11901062n(1824–1895)은 별개 전거다. 작품과 이형이 다르다. 후자의 폐기 ISNI도 직접 확인했다. [아버지 전거](https://catalogue.bnf.fr/ark:/12148/cb119010630.public) · [아들 전거](https://catalogue.bnf.fr/ark:/12148/cb11901062n) | 입력에 날짜·작품·전거가 없으면 두 저자 후보가 남는다. 역할을 추가하는 것만으로 판정을 마칠 수 없는 반례다. |

두 분야에서는 이름이나 검색어로 후보를 조사하고, 링크를 내보낼 때는 올바른 엔터티와 현재 역할을 같이 근거로 삼는다. 기능 카드에서도 어떤 객체를 받아 어떤 결과를 반환하는지 함께 주는 제안으로 옮길 수 있다. [식별자 검산표](evidence/domain-identities.csv)

## 자료와 검사

고유 외부 원전 **38편**을 직접 판독했다. 유형별로 자연 한국어 채택 질문 6/목표 8저자, PyTorch 고정 구현·공식 가이드·회귀 13/최소 6편(선행 7편 재열람, 신규 6편), 한국어 문법·용례 6/4편, 공식 철도 7/3편, 서지·전거 6/3편이다. 양적 하한 24편을 넘겼으며 자연 질문 유형 목표가 남았다. 첫 글 제외/중복, 회수 실패, 검색 응답, 보조 사례는 별도의 원장 행이다. [출처 원장](sources.jsonl) · [재집계](evidence/recount.json)

분리한 두 프로세스에서 같은 고정 입력을 읽어 결과 6개 CSV의 지문이 일치했다. 공개 첫 본문을 매번 여섯 건 다시 열고 NFC·구절과 투영을 재검사했다. 같은 판독자의 검산이다. PyTorch 공식 회귀 코드를 읽었고 런타임 시험과 별도 세션 판독은 미실시다. [재생 영수증](evidence/replay-validation.json) · [자가검사](SELF_CHECK.md)

| 중요한 불일치·약점 | 다음 조사·원문 또는 실험 | 판단을 바꿀 관측 |
| --- | --- | --- |
| 포럼 원본 JSON 0/64 및 검색 0/4, 자연 질문 6/8저자 | 공개 접속 가능한 환경에서 같은 A ID 및 B 네 질의와 #1을 먼저 복구한다. G1 첨부 두 건을 재확인한다. | 앞선 미접근 원문을 포함한 최초 적격 채택과 실제 조사 결합 별칭이 확인된다. |
| B/C 동률은 활성 별칭 0건의 여섯 원문에서만 관측됐다. | 동일 카드판에서 조사 결합을 실제 쓴 자연 원문의 거절·보존을 먼저 봉인하고 두 정책을 짝비교한다. | C의 신규 직접, 밀려난 직접, 추가 충돌 중 하나가 같은 요청·카드에서 나타난다. |
| Gate가 충돌 1과 직접 1을 동시에 걷어냈으며 직접 판정은 단일 프로세스 허용에 의존한다. | HDF5 첫 본문의 두 해석을 별도로 평가하고 작업자 보존이 명시된 경우와 유보 조건을 독립 판독한다. | 단일 프로세스가 금지됐거나 필요한 출력 구절을 근거 비용 안에서 보완해 직접 링크를 유지할 수 있다. |
