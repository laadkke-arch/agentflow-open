# 예측 봉인 전 시간·Audacity 행 재판독

검토 시각: 2026-11-22T22:15:55Z. 검토자: `temporal_donors`, 같은 모델의 별도 문맥이며 원문 제공 조사에도 참여했다. 외부 독립 판독 또는 결말에 눈가림된 인간 검토가 아니다. `requests.csv`, `predictions.csv`, `sources.jsonl`의 AUD/TD/TC 행을 읽었으며 후속 결정·PR·시험·종료 사건은 열지 않았다. 공유 원장에는 쓰지 않았다.

## 검토 입력 바이트

| 파일 | SHA256 |
| --- | --- |
| requests.csv | `dff09ef318efcdacc5ac16e0658061de163edb6ff911caa7e2648f314cd3a8a8` |
| predictions.csv | `5db89173ec6f102d9d909832dea0e87c26df12297a698784455a8500945aad2f` |
| sources.jsonl | `7dfbae077f5b22e356e7471d9599dc819210ba73a44b338a52b61916cf9aa429` |

이후 편집본을 검토한 것으로 소급하지 않는다.

## 통과한 구분

- **AUD01 same:** 두 경계 조회 API가 같은 수치 출력으로 설계되므로 정상·커서 입력 둘 다 같다는 분류는 타당하다. 영상 IN 프레임 포함을 오디오 초 값에 더하지 않았고, 조회 API의 이름은 제공 원리로 결정하지 않았다. [Avid p82](https://resources.avid.com/SupportFiles/attach/MCGS.PDF), [Adobe PDFp43·289](https://help.adobe.com/archive/en/premiere-pro/cs6/premiere_pro_reference.pdf).
- **AUD01 W3C 예외:** `a=b`를 빈 재생 성공으로 적지 않았다. [고정2012판 §6.2.2](https://www.w3.org/TR/2012/REC-media-frags-20120925/)에서 오류 구간을 무시하도록 **권고(SHOULD)**한다는 수준을 유지해야 한다. 규범 예외는 현재 행에 보존돼 있다.
- **AUD02 underdetermined:** 선택 테두리는 waveform 대비를 자동 해결하지 않는다. 두 후보가 제약을 달리 보며 자동 색 보정이 원래 사용자 색 보존과 충돌할 수 있다는 제한을 남긴 분류는 정직하다. 세 번째 설계(A+border)가 원 A/B 판별을 대신하지 않는다.
- **출판판·분야:** TD03 Netflix 현행2025편집판과 TD04 Apple 현행/날짜미상판을 현대 진단으로 표시했다. TC02는 수신측 인접 DSP 비교로 배당했다. 영화 편집·오디오 편집의 인접성도 표시했다.
- **단일 산입:** TD04b와 TC02b/c/d를 별도 저작으로 세지 않았다. 시간 경계 자체의 제공 규칙은 TD01·TD02·TD03의3개이며, TD04의 색 마스크를 추가 시간 경계 저작으로 표현할 필요는 없다.

## 봉인 전에 고칠 항목

### R1. AUD03-B 수치 예측을 고정하거나 조건부 판별의 한계를 유지

현재 `outer feather2bins`는 연산자·가중치·경계 처리·음수 dB의 적용 공간을 특정하지 않는다. 두 bin 밖으로 범위를 늘린다는 성질만으로 모든 입력에서 bin86의 엄격한 변화량이 정해지는 것은 아니다. 현행 `different_conditional`은 조건을 붙인 모델 분류로는 가능하지만 완결된 동일 입력 수치 예측 분모에 넣을 수 없다.

봉인 전에 둘 중 하나를 택한다.

1. 함수 미지정 상태를 유지하고 `조건부 차이; 수치 판별은 미확인`으로 표시하며, 명확한 수신측 동일 연산자·시험이 없으면 엄격 판별 분모에서 제외한다.
2. 아래처럼 **연구자 합성 연산자**를 추가로 고정한다. 이 연산자는 Apple·Netflix 규칙이나 실제 Audacity 알고리즘이라고 주장하지 않는다.

`g=10^(-6/20)`, `G_A(k)=g` for `42<=k<86`, otherwise `1`. `G_B(k)=(product(G_A(k+j), j=-2..2))^(1/5)`라는 중심5bin 동일가중 기하평균을 택하면, bin64는 두 방식 모두−6dB이며 bin86은 A=0dB, B=−2.4dB로 고정된다. 이 추가 모델과 같은 조작·입력을 가진 공개 후속 시험만 그 수치 예측을 지지할 수 있다. 범위 밖을 마지막에 다시1로 덮는 처리나 inside-only feather는 다른 연산자다.

### R2. AUD02의 대비 수치 표현

`requests.csv`의 `waveform 대비0`은 시각적 차이0라는 설명으로는 이해되지만 `predictions.csv`가 쓰는 대비율과 혼동된다. `동일 휘도, 대비율1:1`로 통일하는 것이 정확하다. 흑백 입력의 WCAG 대비율21:1과도 같은 척도로 비교할 수 있다. 자동 보정 외 다른 표시를 허용하면 B 정의도 그에 맞게 한정해야 한다.

### R3. 제공 규칙과 연구자 선택을 집계에서 다시 구분

AUD03-P1의 hard mask 선호는 Premiere의 표본 정밀도나 Smith의 sidelobe 설명에서 직접 도출되지 않는다. 연구자가 `only selected area`에 적용한 outside-bin 보존 조건이 그 선호를 만든다. 현재 `receiver_mapping`·`authorship`에 이 사실이 있지만, 최종 표에서 `외부 원리가 새로 A를 제안했다`로 축약하지 말아야 한다. AUD03-P2의 두-bin 평활화도 연구자 대응이며 Netflix는 특히 근접 오답의 성격이다.

### R4. 기계 판독용 중복 열의 빈 값

AUD 행의 `purpose`, `observable`, `known_names_at_request`, `baseline_api`, `body_revision`, `checked_utc`, `new_choice_relative_request`는 비어 있으나 같은 의미의 상세 열 일부에는 값이 있다. 봉인 전 정규 열을 상세 열에서 명시적으로 채우거나 정규화 규칙을 남길 필요가 있다. `author_stated_purpose`, `normal_observable`/`boundary_observable`, `known_name_at_request`, `choice_feasibility`, `first_body_status`, `opened_at`를 잘못 결측으로 세지 않아야 한다. 새로운 선택 여부는 별도 판독을 유지하고 자동으로 참으로 채우지 않는다.

## 산술 재검산

검산은 입력 상수에 대한 Python 산술만 수행했다. Audacity·영상 편집기·필터 프로그램을 실행한 시험이 아니다.

| 값 | 결과 |
| --- | --- |
| Fs/N | 48000/2048 = 23.4375Hz |
| floor(1000/df) | 42 |
| ceil(2000/df), exclusive upper | 86 |
| normal bin64 | 1500Hz |
| last included bin85 | 1992.1875Hz |
| first excluded bin86 | 2015.625Hz |
| stipulated −6dB amplitude gain | 0.5011872336272722 |
| optional centered5bin geometric-mean model at86 | 0.7585775750291838 = −2.4dB |

원 요청의 연속 주파수 `[1000,2000]Hz`와 반올림된 bin 집합 `[42,86)`는 같지 않다. bin42는984.375Hz다. 이번 입력은 후자를 명시한 합성 fixture이므로 그 차이를 숨기지 않으면 사용할 수 있다. 반올림을 바꾸는 감도는 원 봉인판과 별도다.

## 재판독 결론

AUD01은 같은 예측, AUD02는 판별불가/제약 의존으로 유지할 수 있다. AUD03은 조건부로 갈리지만 함수·허용오차가 없는 상태에서는 강한 수치 판별 성공을 주장할 수 없다. 위 R1–R4를 봉인 전에 반영하거나 미충족으로 고정한 뒤 후속 근거를 열면 된다. 이 검토는 현재 파일의 의미·산술 점검이며 제공 원리의 역사적 채택 또는 제품 추천 성능을 확인한 것이 아니다.
