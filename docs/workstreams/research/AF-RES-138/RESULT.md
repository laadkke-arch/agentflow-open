| 모집층·정확한 질의·순서 | 예정·원서버 반환·열람한 첫 글 | 고유 저자·중복·기존 글 | 표면형 확인·역할·제외·미확인 | 실제 비교 분모 |
| --- | --- | --- | --- | --- |
| 목적 P1 · `"pytorch" "가중치를" is:issue is:public in:body created:2019-01-01..2025-12-31 sort:created-asc` | 20 · 원서버 전체 24 / 받아서 확인한 24 / 창 20 · 첫 글 20 · p1–3 [SEARCH-P1-p1](sources.jsonl#L42) | 15명 · 중복 슬롯 2 · 선행 1 | 질의형 20 · 인용/설명 14 · 시도 4 · 로그 2 · 새 제외 16 · 접근 미확인 0 | 1건·1저자 · 16쌍 |
| 목적 P2 · `"pytorch" "복사본을" is:issue is:public in:body created:2019-01-01..2025-12-31 sort:created-asc` | 20 · 원서버 전체 2 / 받아서 확인한 2 / 창 2 · 첫 글 2 · p1–1 [SEARCH-P2-p1](sources.jsonl#L45) | 2명 · 중복 슬롯 0 · 선행 0 | 질의형 2 · 인용/설명 2 · 시도 0 · 로그 0 · 새 제외 2 · 접근 미확인 0 | 0건·0저자 · 0쌍 |
| 목적 P3 · `"pytorch" "전치를" is:issue is:public in:body created:2019-01-01..2025-12-31 sort:created-asc` | 20 · 원서버 전체 0 / 받아서 확인한 0 / 창 0 · 첫 글 0 · p1–1 [SEARCH-P3-p1](sources.jsonl#L46) | 0명 · 중복 슬롯 0 · 선행 0 | 질의형 0 · 역할 해당 없음 · 새 제외 0 · 접근 미확인 0 | 0건·0저자 · 0쌍 |
| 목적 P4 · `"pytorch" "데이터로더를" is:issue is:public in:body created:2019-01-01..2025-12-31 sort:created-asc` | 20 · 원서버 전체 0 / 받아서 확인한 0 / 창 0 · 첫 글 0 · p1–1 [SEARCH-P4-p1](sources.jsonl#L47) | 0명 · 중복 슬롯 0 · 선행 0 | 질의형 0 · 역할 해당 없음 · 새 제외 0 · 접근 미확인 0 | 0건·0저자 · 0쌍 |
| 중립 N1 · `"pytorch" "궁금합니다" is:issue is:public in:body created:2019-01-01..2025-12-31 sort:created-asc` | 20 · 원서버 전체 41 / 받아서 확인한 30 / 창 20 · 첫 글 20 · p1–3 [SEARCH-N1-p1](sources.jsonl#L48) | 19명 · 중복 슬롯 0 · 선행 8 | 질의형 20 · 지정 4형 0 · 새 제외 9 · 접근 미확인 0 | 3건·3저자 · 48쌍 |
| 중립 N2 · `"pytorch" "도와주세요" is:issue is:public in:body created:2019-01-01..2025-12-31 sort:created-asc` | 20 · 원서버 전체 1 / 받아서 확인한 1 / 창 1 · 첫 글 1 · p1–1 [SEARCH-N2-p1](sources.jsonl#L51) | 1명 · 중복 슬롯 0 · 선행 0 | 질의형 1 · 지정 4형 0 · 새 제외 0 · 접근 미확인 0 | 1건·1저자 · 16쌍 |
| 목적 합계 | 80 · 창 22 · 첫 글 20개 · 배열 끝 칸 58 | 15명 · 동일 이슈 중복 슬롯 2 · 기존 1 · 기열람 포함 본문 계보 3 | 지정 4형 고유 글 20 · 새 제외 18 · 접근 미확인 0 · 저자 ID 미확인 1 | 1건·1저자 · 16쌍 |
| 중립 합계 | 40 · 창 21 · 첫 글 21개 · 배열 끝 칸 19 | 20명 · 동일 이슈 중복 슬롯 0 · 기존 8 · 기열람 포함 본문 계보 1 | 지정 4형 고유 글 0 · 새 제외 9 · 접근 미확인 0 · 저자 ID 미확인 0 | 4건·4저자 · 64쌍 |

| 원저자 요청 URL·원문 구절·역할 | 카드·원절 URL·반환값 | 보존·거절·모르는 조건 | 전수 기준과 반대 해석 | B·C·Gate·조건부안의 조사8위·표시3위 | 유입·밀림·공석 |
| --- | --- | --- | --- | --- | --- |
| [N2-01 L3](https://github.com/openspeech-team/openspeech/issues/202) ‘aihub_labels.csv를 찾을 수 없다는 에러가 발생합니다.’ · 목표 [ISS-N2-01](sources.jsonl#L4) | [D01](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L158) 데이터셋과 옵션 → 배치 또는 개별 샘플 반복자 [PT-LOAD](sources.jsonl#L52) | 라벨 CSV를 먼저 공급 · 경로/생성 미확인 | 미확인 · vocab_path에 넣을 파일을 읽기 전 실패다. Dataset 반복자는 원 데이터 파일이나 문자-ID 맵을 제공하지 않는다. | 1/1 · 1/1 · 1/보류 · 1/보류 | 동일 순위 · Gate에서 표시 1 보류 |
| [N2-01 L3](https://github.com/openspeech-team/openspeech/issues/202) `N2-01-G`와 동일 · 목표 [ISS-N2-01](sources.jsonl#L4) | [D05](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/_utils/collate.py#L23-L70) 단일 샘플 → 단일 변환 샘플 [PT-COLLATE](sources.jsonl#L54) | 문자 ID 매핑 필수 · 개별 NumPy 변환과 다른 단계 | 미확인 · 문자열을 받더라도 개별 NumPy 변환은 그 문자열을 어휘 CSV로 읽지 않는다. | 6/— · 6/— · 6/보류 · 6/보류 | 조사 6 유지 · 표시 예산 밖→보류 |
| [N1-03 L4](https://github.com/sooftware/kospeech/issues/12) ‘0에폭 16000step의 weight를 불러 와볼려고 합니다.’ · 목표 [ISS-N1-03](sources.jsonl#L9) | [D01](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L158) 데이터셋과 옵션 → 배치 또는 개별 샘플 반복자 [PT-LOAD](sources.jsonl#L52) | 첫 작업은 checkpoint 키·값 적재 · batch_size는 로그와 다음 질문 | 미확인 · 첫 요청에서 실패한 동작은 모델 매개변수 적재다. L28의 batch_size와 L56의 OOM은 별개이며 해결 조건도 더 필요하다. | 1/1 · 1/1 · 1/보류 · 1/보류 | 조사/표시 순위 유지 · Gate 표시 보류 |
| [N1-03 L4](https://github.com/sooftware/kospeech/issues/12) `N1-03-G`와 동일 · 목표 [ISS-N1-03](sources.jsonl#L9) | [D08](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L244) 표본별 1D 가중치·횟수·복원 여부 → int 반복자 [PT-SAMPLER](sources.jsonl#L56) | 전체 키 보존 또는 호환 키만 초기화 · 표본별 확률은 명시되지 않음 | 충돌 · 이름별 checkpoint weight를 표본 선택 가중치로 대체하면 입력 의미와 결과가 달라진다. 반환되는 int는 현재 모듈을 갱신하지 않는다. | 0점/— · 0점/— · 0점/— · 0점/— | 전 정책 0점 · 충돌 판정은 표시 노출 0 |
| [N1-05 L6](https://github.com/gyunggyung/KoGPT2-FineTuning/issues/6) ‘dataset은 제가 구축해야 하는 부분인가요??’ · 목표 [ISS-N1-05](sources.jsonl#L13) | [D01](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L158) 데이터셋과 옵션 → 배치 또는 개별 샘플 반복자 [PT-LOAD](sources.jsonl#L52) | 텍스트 코퍼스 제공처와 레코드 포맷 미확인 | 미확인 · 이미 구축한 Dataset 순회라면 쓸 수 있다. 묻는 corpus 제공·준비 여부에는 반환 근거가 없다. | 1/1 · 1/1 · 1/보류 · 1/보류 | Gate에서 표시 1 보류 |
| [P1-07 L3](https://github.com/Beomi/KcELECTRA/issues/5) ‘다른 리뷰 데이터를 넣어서 predict값을 뽑아주고 싶은데’ · 목표 [ISS-P1-07](sources.jsonl#L16) | [D01](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L130-L158) 데이터셋과 옵션 → 배치 또는 개별 샘플 반복자 [PT-LOAD](sources.jsonl#L52) | 저장 모델과 리뷰 추론 · 배치 재사용 및 새 입력 label 미확인 | 일부 · 직접 forward 해석 미확인 · 작성자가 코드에서 사용하는 Dataset 순회는 다중 리뷰 텐서를 공급하는 한 단계다. 모델 입력 인자와 forward가 여전히 필요하다. | 1/1 · 1/1 · 1/보류 · 1/보류 | B/C의 표시 1 유지 · Gate에서 보류 |
| [P1-07 L3](https://github.com/Beomi/KcELECTRA/issues/5) `P1-07-G`와 동일 · 목표 [ISS-P1-07](sources.jsonl#L16) | [D03](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataset.py#L193-L214) 동일 dim0 길이의 여러 텐서 → 인덱스에 대응하는 텐서 튜플 [PT-DATASET](sources.jsonl#L53) | 기존 document·label 텐서 쌍 · 새 입력에 label 미확인 | 일부 · 직접 forward 해석 미확인 · 작성자 코드가 이미 document·label 텐서를 래핑한다. 그 튜플은 배치용 입력 한 단계이며 예측은 산출하지 않는다. | 2/2 · 2/2 · 2/보류 · 2/보류 | B/C의 표시 2 유지 · Gate에서 보류 |
| [P1-07 L3](https://github.com/Beomi/KcELECTRA/issues/5) `P1-07-G`와 동일 · 목표 [ISS-P1-07](sources.jsonl#L16) | [T08](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/aten/src/ATen/native/TensorShape.cpp#L3757-L3769) Tensor → grad와 단절된 공유 Tensor [PT-SHAPE](sources.jsonl#L59) | detach는 기존 손실 코드 · 저장소/이력 단절 요구 미확인 | 미확인 · 지정된 첫 요청에서 이 카드의 계산 이력에서 떼기를 필요한 하위 동작으로 연결할 입력 또는 반환 원절이 없다. | 3/3 · 3/3 · 3/보류 · 3/보류 | B/C 표시 3 유지 · Gate에서 보류 |
| [P1-07 L4](https://github.com/Beomi/KcELECTRA/issues/5) ‘가중치를 `best.ckpt`로 저장한 상태입니다.’ · 시도 [ISS-P1-07](sources.jsonl#L16) | [D08](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L244) 표본별 1D 가중치·횟수·복원 여부 → int 반복자 [PT-SAMPLER](sources.jsonl#L56) | 저장 가중치 사용 · 확률 표집 요구나 인덱스 출력 미확인 | 충돌 · best.ckpt의 훈련 가중치는 유지해 추론하려는 것이다. 인덱스 확률 추출로 대체하면 객체와 원하는 출력이 다르다. | 0점/— · 4/— · 4/보류 · 4/보류 | C 0→4점, 조사 신규 4 · 표시 예산 밖 |
| [P1-07 L3](https://github.com/Beomi/KcELECTRA/issues/5) `P1-07-G`와 동일 · 목표 [ISS-P1-07](sources.jsonl#L16) | [D04](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/_utils/collate.py#L337-L361) 샘플 시퀀스 → 선두 배치 축 또는 구조별 결과 [PT-COLLATE](sources.jsonl#L54) | 인코딩·패딩과 배치 입력 조건 미확인 | 일부 · 직접 forward 해석 미확인 · 기존 배치 경로에서는 패딩된 review token tensor 쌓기가 입력의 한 단계다. 생문자열을 토큰화하거나 분류하지 않는다. | 4/— · 5/— · 5/보류 · 5/보류 | 조사 4→5 · 일부 기능이 한 자리 하락 |
| [P1-07 L3](https://github.com/Beomi/KcELECTRA/issues/5) `P1-07-G`와 동일 · 목표 [ISS-P1-07](sources.jsonl#L16) | [D05](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/_utils/collate.py#L23-L70) 단일 샘플 → 단일 변환 샘플 [PT-COLLATE](sources.jsonl#L54) | 텍스트 인코딩 필요 · NumPy 변환 입력 미확인 | 미확인 · 개별 NumPy 변환 대신 작성자는 tokenizer로 Python 입력을 인코딩하고 torch.tensor로 만들었다. 필요한 NumPy 입력은 없다. | 5/— · 6/— · 6/보류 · 6/보류 | 조사 5→6 |
| [P1-07 L3](https://github.com/Beomi/KcELECTRA/issues/5) `P1-07-G`와 동일 · 목표 [ISS-P1-07](sources.jsonl#L16) | [D07](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L293-L355) 인덱스 반복자 → list[int] 반복자 [PT-SAMPLER](sources.jsonl#L56) | 인덱스 묶음과 학습에서 쓴 샘플 공급 계약 구별 | 충돌 · 직접 forward 해석 미확인 · 기존 데이터 공급 역할을 이 반환으로 대체하면 입력 텐서 대신 int 목록을 건넨다. 별도 순회 계획으로 쓰는 경우에는 의도가 미확인이다. | 6/— · 7/— · 7/보류 · 7/보류 | 조사 6→7 |
| [P1-07 L3](https://github.com/Beomi/KcELECTRA/issues/5) `P1-07-G`와 동일 · 목표 [ISS-P1-07](sources.jsonl#L16) | [T01](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_tensor_docs.py#L6083-L6126) Tensor+shape 또는 dtype → 같은 저장소의 Tensor [PT-TMETHOD](sources.jsonl#L58) | 리뷰의 어말 뷰는 A04 토큰 경계를 통과하지 못함 | 미확인 · 지정된 첫 요청에서 해당 view가 반환하는 shape·dtype 재해석은 새 리뷰 추론에서 요청한 하위 조작으로 확인되지 않았다. | 7/— · 8/— · 8/보류 · 8/보류 | 조사 7→8 |
| [P1-07 L3](https://github.com/Beomi/KcELECTRA/issues/5) `P1-07-G`와 동일 · 목표 [ISS-P1-07](sources.jsonl#L16) | [D02](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataset.py#L77-L94) __iter__ 구현 → 샘플 반복자 [PT-DATASET](sources.jsonl#L53) | 직접 쓸 스트림 구현 및 요구 미확인 | 미확인 · 지정된 첫 요청에서 저자는 기존 map-style 입력을 사용했다. 별도 스트림에서 샘플을 읽어야 한다는 요구는 확인되지 않았다. | 8/— · 예산밖/— · 예산밖/— · 예산밖/— | 조사 8→9, 조사 예산 밖 |
| [N1-10 L25](https://github.com/cleinc/bts/issues/98) ‘아님 output channels를 다르게 해주어야 할까요?’ · 목표 [ISS-N1-10](sources.jsonl#L23) | [T04](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/_torch_docs.py#L11226-L11253) Tensor+두 축 → 순서를 교환한 Tensor [PT-TFUNC](sources.jsonl#L57) | 실제 stage별 채널이 필요 · axis 교환이나 새 저장소 요구 미확인 | 미확인 · 두 축이 역순이면 전치가 가능하다. 질문은 채널 수 설정이며 차원 순서·저장소 조건이 없다. | 0점/— · 0점/— · 0점/— · 0점/— | 모두 0점 · 조사 8, 표시 3 공석 |

| 모집층·정책쌍 | 요청·저자·질문×카드 수 | 새 직접·빠진 직접·새 충돌·막은 충돌 | 확정 표시·조건부 표시·빈자리 | 추가 판독 원절·미확인 |
| --- | --- | --- | --- | --- |
| 목적 · B→C | 1 / 1 / 16 | 조사 0/0/1/0 · 표시 0/0/0/0 | 확정 3→3 · 조건 0→0 · 공석 0→0 | 0개 · 표시 미확인 1→1 |
| 목적 · C→Gate | 1 / 1 / 16 | 조사 0/0/0/0 · 표시 0/0/0/0 | 확정 3→0 · 조건 0→0 · 공석 0→3 | 11개 · 표시 미확인 1→0 |
| 목적 · Gate→조건부안 | 1 / 1 / 16 | 조사 0/0/0/0 · 표시 0/0/0/0 | 확정 0→0 · 조건 0→0 · 공석 3→3 | 0개 · 표시 미확인 0→0 · 조건 판독 8쌍 |
| 중립 · B→C | 4 / 4 / 64 | 조사 0/0/0/0 · 표시 0/0/0/0 | 확정 8→8 · 조건 0→0 · 공석 4→4 | 0개 · 표시 미확인 8→8 |
| 중립 · C→Gate | 4 / 4 / 64 | 조사 0/0/0/0 · 표시 0/0/0/0 | 확정 8→0 · 조건 0→0 · 공석 4→12 | 22개 · 표시 미확인 8→0 |
| 중립 · Gate→조건부안 | 4 / 4 / 64 | 조사 0/0/0/0 · 표시 0/0/0/0 | 확정 0→0 · 조건 0→0 · 공석 12→12 | 0개 · 표시 미확인 0→0 · 조건 판독 15쌍 |
| 합계 · B→C | 5 / 5 / 80 | 조사 0/0/1/0 · 표시 0/0/0/0 | 확정 11→11 · 조건 0→0 · 공석 4→4 | 0개 · 표시 미확인 9→9 |
| 합계 · C→Gate | 5 / 5 / 80 | 조사 0/0/0/0 · 표시 0/0/0/0 | 확정 11→0 · 조건 0→0 · 공석 4→15 | 33개 · 표시 미확인 9→0 |
| 합계 · Gate→조건부안 | 5 / 5 / 80 | 조사 0/0/0/0 · 표시 0/0/0/0 | 확정 0→0 · 조건 0→0 · 공석 15→15 | 0개 · 표시 미확인 0→0 · 조건 판독 23쌍 |

## 관측 범위

**PARTIAL.** 목적층 1명, 중립층 4명으로 5명의 첫 요청을 비교했다. 유일한 말끝 조사 적중은 이미 저장한 모델 가중치를 가리켰다. 새 조사 후보는 표본 인덱스를 반환하는 D08이었으며, 화면에 새로 표시된 링크는 0장이다. 조건부 표시도 관측 0장이다. 목적층과 전체 하한에 각각 3명이 부족하다. [판독 원장](requests.jsonl) · [별칭 검산](evidence/alias-audit.csv)

표 1의 원서버 전체 수는 결과 개수 필드, 받아서 확인한 수는 경계 확인을 포함해 실제 받은 배열, 창은 첫 20으로 자른 위치다. 표 2의 각 쌍은 B, C, Gate, 조건부 순서의 조사/표시 위치다. 값 0점은 양점 후보가 되지 않은 경우이며, 예산 밖과 보류는 각각 조사 한도와 판독 이탈이다. 표 3의 각 네 수는 표시된 열 순서이며, 확정 표시는 B/C가 즉시 보여 준 링크와 Gate 통과 링크를 합계 규칙상 뜻한다. 실제 직접 등급은 이와 별도로 센다. [80 표시 판독](display.csv) · [80 전수 기준](truth.csv) · [320 순위](ranks.csv) · [480 전이](transitions.csv)

## Q1 모집기의 반환과 원문 창

여섯 질의의 사이트 개수 필드 합은 68슬롯이다. 응답 10페이지에서 57슬롯을 받았고 경계 밖 행 14개를 제외해 창 43슬롯을 고정했다. P1의 마지막은 kimaram/chip #3, ID 3559707532, N1은 MISOChallenge-taekwondo #2, ID 1040406859다. 두 경계 다음 생성시각은 각 경계 시각보다 늦었다. P2와 N2의 마지막 ID는 각각 3552241503과 1813749635다. P3·P4의 HTTP 200 배열은 빈 배열이었다. 120개 예정 칸 중 77개는 관측한 배열 끝 뒤의 칸이다. [검색 URL·UTC·페이지·마지막 ID](evidence/search.jsonl) · [120슬롯](frame.csv)

목적층 22슬롯은 20개 이슈로 합쳐졌다. P2 두 이슈는 P1에도 있었고 순환 순서의 먼저 나온 P2에 귀속했다. 중립 단독 이슈는 21개이고 층간 겹침 0, 겹침 제외 후 목적층 이슈 20개다. 41개의 고유 첫 본문을 모두 열었고 9개가 134에서 열었던 이슈였다. 목적층의 기존 #27은 첫 본문과 일치했으며 작성자 ID를 회수하지 못했다. 배열과 본문 배달이 성공한 경우에도 요청의 적격성은 별도 판정이다. [공개 첫 글과 지문](evidence/opening-receipts.jsonl) · [기존 및 본문 계보](frame.csv)

## Q2 조사 결합과 첫 저자 요청

목적층 고유 글 20개에 지정형이 들어 있었으나 적격 1건에서 해당 형태는 저자의 **시도** 구절이었다. 중립 21개 가운데 지정 네 형태가 나온 첫 본문은 0개다. 적격 4건은 라벨 CSV, checkpoint 매개변수 적재, corpus 입력, encoder feature 채널이었다. 예제 코드의 추적 설명과 Normalize의 이유를 물은 N1-06·N1-14는 저자가 수행할 텐서 조작·보존을 첫 글에서 확정하기 어려워 제외했다. P1-06의 실제 표본 확률 사례는 복습 글이고 P2에는 면접 FAQ와 번역이 들어왔다. 검색기가 회수한 표면형을 모두 확인하고 본문 계보·학습기록·기존 기사·설치/환경 자료를 각각 표기했다. [표면형의 코드포인트 위치](evidence/surface-audit.jsonl) · [첫 요청의 역할과 지문](requests.jsonl)

국립국어원 자료는 앞말에 붙이는 규정과 조사 연속, 인용 끝의 조사, 부사/조사의 동형을 보여 준다. 한 개의 허용 접사만 일치시키는 C의 계약은 규정으로 포괄되는 모든 용법을 처리하지 않는다. 목표와 같은 말이 명시 인용에 있다면 현재 화자의 요청인지 다시 보아야 한다. [KO-NIKL-41](sources.jsonl#L81) · [KO-NIKL-RO](sources.jsonl#L82) · [KO-NIKL-BODA](sources.jsonl#L83)

## Q3 같은 단어와 다른 출력

- P1-07 L4의 weight는 기존 모델이 사용한 checkpoint의 값이다. D08은 샘플별 1D 확률 가중치를 입력으로 받아 int 인덱스를 낸다. N1-03 L44–51에도 모델 키의 불일치가 실제 로그로 들어 있다. 모델 weight를 적재하는 고정판 API는 `Module.load_state_dict`이며 16카드 밖에 있다. strict=False의 공식 시험은 누락이나 예상 밖의 키를 보고하고 모든 값을 보존할 수 있는지의 판단은 남긴다. [P1-07 L4](https://github.com/Beomi/KcELECTRA/issues/5) · [N1-03 L44–51](https://github.com/sooftware/kospeech/issues/12) · [PT-SAMPLER](sources.jsonl#L56) · [PT-MODULE](sources.jsonl#L65)
- 독립 복사 T07은 autograd를 유지하며 T08은 저장소를 공유할 수 있다. strided T04는 축을 교환하면서 저장소를 공유하고 sparse 경로는 그 공유가 없다. T03의 전체 축 순열을 두 축 교환과 구별했다. 공식 회귀에는 reshape의 view와 비-view 사례가 모두 있다. 복사/저장소/이력 조건을 요청한 적격 첫 글은 이번 창에서 확인하지 못했다. [PT-TFUNC](sources.jsonl#L57) · [PT-SHAPE](sources.jsonl#L59) · [복사·전치 반례](evidence/counterexamples.md)
- D01은 샘플 또는 배치의 반복자, D07은 인덱스 목록의 반복자, D04는 받은 샘플 묶음의 결합, D05는 개별 NumPy 입력 변환이다. N2-01의 도움 요청 앞에는 tokenizer가 읽을 라벨 파일이 없다. 해당 로그의 영어 dataset/batch가 카드 점수에 들어갔으나, 로더의 출력은 어휘 CSV를 마련하지 않는다. P1-07의 T08 정확 심벌은 손실을 처리하는 코드에 있다. [N2-01 첫 글 및 L198–213](https://github.com/openspeech-team/openspeech/issues/202) · [PT-LOAD](sources.jsonl#L52) · [점수에 들어간 심벌·영문 위치](evidence/symbol-roles.csv)
- P1-07에 쓰인 **리뷰**에는 `뷰`가 부분 문자열로 두 번 있다. 출발점 앞에 다른 한글이 붙어 B와 C에서 둘 다 점수를 받지 않았다. `전치를`, `데이터로더를`이 0이어도 동작의 다른 표기나 영문 심벌 존재 여부는 별개다. 이번 모집창에서 그 표기들에 대한 모델 성능은 산출할 수 없다. [한글 어절 감사](evidence/alias-audit.csv)

## Q4 선행 두 판독과 후속 해석

같은 작업자가 표시 80쌍을 먼저 봉인하고 순위·기준 없이 각 카드 반환을 읽었다. 다음 커밋의 별도 기준 양식에서 직접 0, 일부 3, 충돌 3, 미확인 74를 기록했다. 그 뒤 다섯 스레드의 댓글 13개를 열었다. P1-07의 답변은 tokenizer의 반환을 model forward에 직접 넘기는 예를 주었다. 그 해석에서는 D01·D03·D04의 일부 등급을 미확인으로, D07의 충돌은 로더의 대체 후보일 때로 좁힌다. 새 리뷰의 라벨 유무만으로 기존 DataLoader가 예측을 반환하게 되지 않는다. N1-03의 답변은 코드 세대의 키 변경을 지목했고 N2-01의 답변은 전처리 생성과 작성자의 해결 보고를 남겼다. 기준과 표시 판정의 봉인은 보존했다. [P1-07 후속 호출](https://github.com/Beomi/KcELECTRA/issues/5#issuecomment-977563439) · [댓글과 변동 표](evidence/post-seal-comments.csv) · [기준](truth.csv)

## Q5 실제 이동과 예산

B와 C는 모두 조사 40자리 중 23장, 표시 15자리 중 11장을 채웠다. P1-07에서 D08이 0→4점으로 조사 4위에 들었고 D02가 조사 8위에서 전체 9위로 밀렸다. D04·D05·D07·T01은 조사에서 한 자리씩 내려갔다. 표시 D01·D03·T08은 같은 순위였다. 중립 네 질문은 조사와 표시가 그대로였다. [실제 전이](transitions.csv) · [반례 산식](evidence/counterfactual.json)

B의 전수 80쌍에는 0점 49, 조사 예산 밖 8, 조사 안 표시 예산 밖 12, 표시 11이 있었다. C는 각각 48, 9, 12, 11이다. Gate와 조건부안은 0점 48, 조사 예산 밖 9, 조사 안 보류 23이다. 표시 공석은 B와 C 4, Gate와 조건부안 15다. 다섯 요청 모두에 Gate 통과가 없었고, 공석에 한 장을 추가하기에 적격인 비교쌍도 없었다. [순위 사유](ranks.csv) · [자리 보존](evidence/slots.csv)

## Q6 사용자·개발자·편집자의 손익

사용자에게 C는 이 창에서 새로운 직접 링크를 제공하지 않았다. 잘못된 입력 객체 하나를 내부 조사에 들이는 효과가 있었다. Gate는 일부 2개와 미확인 9개를 화면에서 거둬들였다. 원래 표시된 충돌은 0개라 표시 충돌 제거 관측도 0이다. 열람 비용을 낮추는 공석과, 일부라도 이어서 탐색할 경로를 잃는 공석을 구분할 필요가 있다. 개발자가 모델 파라미터를 유지하려는 경우 샘플 인덱스 선택 API로 방향을 바꾸면 원하는 연산이 달라진다. [P1-07 입력과 출력](requests.jsonl) · [전이](transitions.csv)

편집자의 정책상 추가 원절은 C→Gate에서 저자 구절 10개와 카드 반환 위치 23개로 총 33개였다. 조건부안은 해당 원절을 재사용해 23쌍의 유일 조건 여부를 더 판독했다. 같은 구절이나 위치는 한 요청에서 한 번 세므로 신규 원절 차이는 0개다. 실험상 새 조건부 자리 0개여서 조건 참과 거짓 각각의 직접·충돌 추가 건수는 모두 0이다. 조건부 클릭과 성공률의 분모는 없다. P1-07의 두 해석에서는 B/C 표시 일부가 각각 0–2개, 표시 충돌은 0개다. 조사의 충돌은 B에서 0–1개, C에서 1–2개로 변한다. [편집 비용](evidence/editor-cost.csv) · [반대 해석](truth.csv)

N1-03은 양점 두 후보 모두가 B/C 조사와 표시에 남는 관측이다. P1-07에서 일부 기능인 D04는 조사에서 실제 하락했고 D02는 예산 밖으로 갔다. D02의 실제 유용성은 미확인이다. 별도 민감도 대조에서는 기존 손실 코드의 T08 점수를 0으로 두면 같은 3자리에서 D04가 D08에 밀린다. 이 계산은 기본 정책의 실제 이동으로 합산하지 않았다. 독립 사용자 표본이 없어 목적 질의의 적중을 일반 질문 발생률로 바꾸지 않는다. [반례와 보존 조건](evidence/counterexamples.md)

## Q7 식별자·역할·남은 조건

MBTA의 운영 설정과 GTFS 규격에서 Park Street 상위 역 `place-pktrm`의 Red child `70075`와 `70076`를 대조했다. 남행의 표기는 Ashmont/Braintree, 북행의 표기는 Alewife다. Green child의 ID도 같은 상위 역으로 묶이며 상위 이름만으로 개별 승차 위치를 고를 수 없다. 운영 자료의 `Park`, `PARK STREET [R]`, `Park Street`는 같은 역으로 연결된다. 같은 `70075`에서 Red 남행까지 알아도 JFK/UMass 이후 Ashmont/Braintree 중 어느 종점을 선택하느냐가 남는다. 이 사례는 날짜별 실시간 운행을 확인한 것이 아니며, 배정된 /developers와 공개 실시간/zip 경로는 프록시에서 열지 못했다. [MBTA-ORBIT](sources.jsonl#L89) · [MBTA-SCREENS](sources.jsonl#L91) · [교통 ID와 역할](domains.csv)

LOC 개별 목록 2018560366은 Schubert의 작곡과 Liszt의 독주 피아노 편곡을 구분한다. 동일한 Liszt 표목을 작곡가로 표시하는 `Mazurka brillante` 2018560490과 작곡·편곡을 함께 표시하는 2018570800은 원서버/브라우저에서 열리지 않아 검색 관측으로 남겼다. LOC의 공식 MARC 사례에는 동일 Hindemith 표목, 작품명과 soprano/piano 편성에서 1923과 1948이 갈리는 개별 기술이 있다. 연도를 알면 해당 두 편을 구분할 수 있다. LOC 큐레이터 또한 Grofé의 작곡과 다른 작품 편성 작업을 구별한다. 이 자료의 악보 책임표시 이미지와 두 번째 개별 목록을 직접 대조하는 작업은 남아 있다. [LOC 개별 목록](https://www.loc.gov/item/2018560366/) · [LOC MARC 예시 p.138](https://www.loc.gov/aba/publications/FreeCSB/CSB_108.pdf#page=138) · [접근 기록](sources.jsonl#L112)

운영 노선의 분기·서지의 판정은 식별자와 역할을 먼저 연결해도 추가 값이 필요한 사례다. 기능 링크의 가망과 노선·서지의 실제 판단율을 같은 분모로 계산할 근거는 없다. [타 분야 원장](domains.csv)

## 자료와 검산

하한 집계에 넣은 외부 고유 원전은 37편이다. 신규 23, 재열람 14다. 유형별로 적격 자연 질문 5, PyTorch API·구현·독립 회귀 17, 한국어 규정 인용·공식 용례·기술 원절 6, 운영기관 자료 7, LOC 개별 목록 1 및 공식 서지 원장 예시 1이다. 41개 GitHub 첫 글 전체와 13개 후속 댓글 기록을 보존했고, 적격이 아닌 글과 댓글·검색 응답·실패를 하한에 중복 산입하지 않았다. 두 프로세스의 네 정책 CSV 다섯 파일은 일치했다. 한 사람이 수행한 두 판독이며, 공식 PyTorch 회귀는 코드로 판독했다. [출처 원장](sources.jsonl) · [두 재생](evidence/replays.json) · [독립 재집계](evidence/recount.json) · [자가검사](SELF_CHECK.md)

| 중요한 불일치·약점 | 다음 조사·자료 또는 실험 | 결론을 바꿀 관측 |
| --- | --- | --- |
| 목적 1/4·전체 5/8저자이며 이번 창의 적격 복사·전치·데이터로더 지정형이 0건이다. | 새로운 별도 창과 순서를 먼저 고정하고 원저자 목표에 실제 들어간 조사 결합형을 찾는다. | 동일 카드·예산에서 직접 회복 또는 기존 직접 후보의 이탈이 나온다. |
| 유일한 활성 조사 적중은 모델 가중치 시도였다. 새 조건부 표시는 0이다. | 요청과 반환이 이미 일치하고 하나의 값만 빠진 실제 요청에서 같은 자리 규칙을 적용한다. | 조건 참에서 직접 링크가 추가되며 거짓·명시 금지에서는 공석이 유지된다. |
| LOC 개별 편곡 목록은 확인했으며 작곡 대조 목록과 표지 원책임표시는 배달 오류다. | 2018560490와 2018560366의 목록과 표지 또는 MARC 원문을 공개 접속에서 연다. | 같은 표목과 작품별 역할이 원책임표시에서도 확인되거나 목록의 역할과 다르다. |
