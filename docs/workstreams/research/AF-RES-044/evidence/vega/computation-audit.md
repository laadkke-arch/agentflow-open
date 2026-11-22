# 그룹·표시·후보 근거 계산 감사

검토 시각: 2026-11-22T20:44:04Z 이후. 기준 입력 커밋은 `8c22675a2e90134c386f362cdd2aabe7d14d252e`이며, 아래 생성물은 그 입력에서 만들어진 작업 파일이다. 검토자는 Vega 담당 보조 에이전트다. 같은 연구자의 자체 점검·내부 병렬 검토이며 사람의 독립 판정은 아니다. 원자료와 키를 수정하지 않았고 `build_study.py`를 실행해 산출물을 덮어쓰지 않았다. 별도 읽기 전용 Python 코드로 그룹과 카드 순서·근거 집합을 재계산했다.

## 1. 감사 결과

**그룹 계산과 세 자리 직렬화는 고정 입력에 일치한다. C는 이번 입력에서 A와 완전히 같은 분할을 만들었다.** 따라서 이후 C가 B보다 나은 결과를 내더라도, 그것을 정확한 중복 병합의 성과라고 해석할 수 없다. 미확인 singleton과 서로 다른 세부 키 때문에 실제 합침이 전혀 없는 조건이다.

확인한 생성물의 바이트 SHA256은 다음과 같다. 이후 파일이 달라지면 이 감사는 아래 버전에 대한 기록으로 남는다.

| 파일 | SHA256 |
| --- | --- |
| evidence/build_study.py | `c8f32f9ea7add402323e619be6bab247d41285df3f8fbc32290efa8567aa14f9` |
| groups.jsonl | `6063cac2a061bcece80e0182a6723ecf814147d1cde94a1eed0fd98898bb421d` |
| views.jsonl | `587b9ebc36ed14c3e3ddb239ae76be0bb5c1b4f3344711ecd0559684218ae4fe` |
| evidence/candidate-evidence.jsonl | `35dd5d19afbbe4e7dba90bf37c11915daeb923decdf3977d7240095944e75499` |

루트 `input-freeze.json`의 모든 SHA가 현재 파일과 일치한다. 앞선 감사의 CRLF/LF 결함은 원본 v1 보존과 canonical LF 정정으로 해소된 상태다. 현재 pool SHA는 `53ac7e9dbb95a029aae6c834e7222df3c009b1c4ad6e0993aea7b2ce62982b28`, metadata SHA는 `6bdbde48f81e2ed500edab6223f5ef237adba7badb3578c7906bae62253c12ac`이며 36개 view가 모두 이 둘을 참조한다.

## 2. 구조·first3·라벨 검증

| 검증 | 결과 |
| --- | --- |
| groups/view/candidate 행 수 | 36 / 36 / 72 |
| 같은 요구에 넣은 원순서 | A/B/C 모두 원래6 candidate ID를 같은 순서로 보존; 불일치0 |
| 그룹 키와 원멤버 | 독립 재계산과 36행 전부 일치; 그룹 내 최초 멤버가 대표 |
| 첫3 및 화면 밖 그룹 | 각 방식 최초3 그룹과 나머지 offscreen_groups가 일치; 불일치0 |
| 카드 슬롯 | 각 view 정확히3, 총108칸 |
| 비빈 카드 | 총55칸: A22, B11, C22 |
| 비빈 카드 고정 라벨 | 전부 `원문 보기` 5 Unicode code points, 설명0자 |
| 형제 목록 라벨 | 전부 `관련 링크` 5자; 원멤버 URL과 hidden_members 보존 |
| 후보 근거 원장 정합 | 72행의 case ID·candidate ID·URL이 pool과 일치; strict/full 지원 원자에 원요구 외 ID가 섞인 경우0 |

원풀에 있던41개 실제 URL은 이 표본에서 정확 URL이 각각 다르다. A는 fragment를 보존하므로 같은 HTML 문서를 가리키는 서로 다른 fragment를 합치지 않는다. 다음 표의 빈 대표는 관측된 반환 자리이며, P 행의 숫자0은 **관측 결측을 직렬화한 그룹0**일 뿐 원래 후보가 없었다는 판단이 아니다.

| 요구 | A/B/C 그룹 수 | A와 C의 첫3 candidate ID | B의 첫3 candidate ID |
| --- | --- | --- | --- |
| P1 | 0/0/0, 원풀 미확인 | 빈칸·빈칸·빈칸 | 빈칸·빈칸·빈칸 |
| P2 | 0/0/0, 원풀 미확인 | 빈칸·빈칸·빈칸 | 빈칸·빈칸·빈칸 |
| P3 | 0/0/0, 원풀 미확인 | 빈칸·빈칸·빈칸 | 빈칸·빈칸·빈칸 |
| P4 | 0/0/0, 원풀 미확인 | 빈칸·빈칸·빈칸 | 빈칸·빈칸·빈칸 |
| V1 | 1/1/1 | V1-1·빈칸·빈칸 | V1-1·빈칸·빈칸 |
| V2 | 5/1/5 | V2-1·V2-2·V2-3 | V2-1·빈칸·빈칸 |
| V3 | 5/1/5 | V3-1·V3-2·V3-3 | V3-1·빈칸·빈칸 |
| V4 | 6/1/6 | V4-1·V4-2·V4-3 | V4-1·빈칸·빈칸 |
| C1 | 6/2/6 | C1-1·C1-2·C1-3 | C1-1·C1-4·빈칸 |
| C2 | 6/3/6 | C2-1·C2-2·C2-3 | C2-1·C2-4·C2-6 |
| C3 | 6/1/6 | C3-1·C3-2·C3-3 | C3-1·빈칸·빈칸 |
| C4 | 6/1/6 | C4-1·C4-2·C4-3 | C4-1·빈칸·빈칸 |

V3에는 앞선 `input-audit.md`의 `text` 토큰 이탈이 계속 적용된다. 계산이 맞다는 사실로 표집 규칙 이탈이 사라지지 않는다. 또한 이 감사의 카드 수는 생성된 HTML/JSON 수다. 실제 사람의 화면 노출·클릭 수를 관측한 값은 아니다.

## 3. C 키의 특이도와 실제 합침

`build_study.py` 41–44행은 A에 정확 URL, B에 upstream, C에 `(upstream, component, purpose, version, sorted roles)`를 쓴다. C의 identity_key_complete=false는 candidate ID를 포함한 singleton이 된다. 코드가 완전 답안·후보 적격 등급을 읽어 key를 만드는 경로는 없다. `build_groups()`는 candidate-evidence를 읽지 않는다.

실제 C의41그룹은 singleton24개와 알려진 tuple17개다. 알려진 tuple17개도 모두 서로 달라 어느 원요구에서도 합침이 없다. 따라서 A/C의 그룹 원멤버·대표·화면 밖 멤버가 12요구 전부 동일하다. `evidence/views-U.jsonl` 역시 C와 카드 멤버·화면 밖 멤버가 모두 같다. 알려진 부분이 일치하는 unknown끼리만 합쳐도 이 입력에서는 같은 key가 생기지 않았다.

이를 C가 의미상 동일성을 잘 판별했다고 해석하면 과도하다. 예를 들어 C3-3과 C3-4는 같은 exceptions HTML의 같은 공유 설명을 읽지만 component를 ExceptionGroup/BaseExceptionGroup으로 나누어 따로 표시한다. 이 이름 구분은 원요구의 constructor 경계를 설명하는 데 의미가 있으나, 제공되는 문서 내용을 중복 제거한 것은 아니다. C2의 Styler와 DataFrame.plot도 서로 다른 용도·부품 key로 남는다. 역할/부품을 더 크게 묶었을 때의 결과는 이 감사에서 계산하지 않았으며 **미확인**이다. 관측 뒤 키를 바꾸어 C의 성과를 높여서는 안 된다.

## 4. 원풀 분모와 직링크 inventory 산술

후보별 `supports_by_alternative`를 **같은 대안 ID 안에서만** 합집합하여 원요구의 모든 atom이 포함되는지를 독립 확인했다. 아래는 현재 후보 의미 판정을 입력으로 사용한 산술이다. 새 의미 gold나 실제 클릭 시행을 승인한 표가 아니다. direct inventory는 세 대표가 제공하는 근거 범위이며 한 사람이 두 클릭으로 모두 읽었다는 뜻이 아니다.

| 요구 | 원풀에서 입증된 완전 대안 수 | A direct | B direct | C direct | 판단 범위 |
| --- | --- | --- | --- | --- | --- |
| P1 | **미확인** | **미확인** | **미확인** | **미확인** | 발행 HTML을 수집하지 못한24슬롯 중6개 |
| P2 | **미확인** | **미확인** | **미확인** | **미확인** | 동일 |
| P3 | **미확인** | **미확인** | **미확인** | **미확인** | 동일 |
| P4 | **미확인** | **미확인** | **미확인** | **미확인** | 동일 |
| V1 | 0 | 0 | 0 | 0 | 현행 링크가 과거 v4 해결을 입증하지 않음 |
| V2 | 0 | 0 | 0 | 0 | projection 하위사실을 복합 atom 전체로 올리지 않음 |
| V3 | 0 | 0 | 0 | 0 | 봉인된 Text 풀에서의 값; 토큰 이탈 때문에 원규칙 표본 값은 미확인 |
| V4 | 0 | 0 | 0 | 0 | generic transform/aggregate를 tree 지원으로 올리지 않음 |
| C1 | 2 | 1 | 2 | 1 | HTTPX/Requests, 문서상 일반 능력; C1-3 판독 불일치는 다음 절 |
| C2 | 11 | 11 | 10 | 11 | 첫 절10개와 C2-3의 별도 Matplotlib 직접 사용1개 |
| C3 | 1 | 0 | 0 | 0 | 원풀의 A1+A2 보완 조합은 한 CPython 계약 대안 |
| C4 | 0, A2 미입증 | 0 | 0 | 0 | 예정 양성의 성공을 뜻하지 않음 |

0 분모의 회수 비율은 **해당 없음**이다. P의 결측 분모를 여기에 넣으면 안 된다. C1에서 B는 Requests라는 원풀 대안이 직링크에 들어오고, C2에서는 Matplotlib 직접 사용의 근거가 직링크에서 빠진다. 보강 direct 개수를 한 덩어리로만 합하면 이 반대 방향 변화가 가려진다. C3의 문서 조합 두 가지를 두 구현 대안으로 늘리지 않았다.

C2-3의 후보 근거는 `C2-pandas`와 `C2-matplotlib`를 구별한다. 원문의 [Chart visualization #visualization](https://pandas.pydata.org/pandas-docs/version/2.0/user_guide/visualization.html#visualization)은 h1 창 전체를 허용하므로 뒤의 **Plotting directly with Matplotlib** 절도 범위 안이다. `control-C2.json`의 source_coverage_revisions에 남은 최초10→11 정정과 일치하며, 단순히 pandas가 Matplotlib을 내부 사용한다는 사실을 중복 계산한 것이 아니다.

## 5. C1-3 의미 판독 불일치

`build_study.py` 101행은 C1-1/2/3/5를 일괄적으로 두 atom 완전 지원으로 넣는다. [Mounting transports](https://www.python-httpx.org/advanced/transports/#mounting-transports) 원문을 다시 열고 307–458행 및 저장된811어절 strict창을 대조했다. 창에는 Python의 `import httpx`, Client/transport 구성과 HTTP 요청을 scheme/domain/port에 따라 라우팅한다는 설명이 있다. 그러나 그 창 안에는 Request를 구성하거나 get/send를 호출하는 예가 없으며, 실제 송신을 설명하는 상단 Transport 도입·HTTP Transport 예제는 도착 창 밖이다.

따라서 두 가지 독해가 갈린다. 이름층의 일반 능력이라는 넓은 독해에서는 ‘HTTP 요청을 라우팅하는 Client’를 구성한다는 설명으로 송신 능력을 추론할 수 있다. 반면 봉인 request의 **construct and send**를 창 안의 직접 증거로 요구하면 A2는 **조건부/미확인**이다. 현행 원장처럼 무조건 ‘예’라고 표시한 것은 이 추론 단계를 생략한다. `C1.A2` 문구 자체는 constructing/sending으로 되어 있어 request의 and와도 해석 강도가 다르다. 이 감사는 원자를 바꾸지 않고 불일치를 보존한다.

이 한 후보의 등급을 엄격하게 낮춰도 현재 C1 원풀·직링크 대안 ID 집합은 달라지지 않는다. C1-1의 유지보수자 `httpx.get` 설명, C1-2의 timeout GET 예, C1-5의 요청 인스턴스 설명이 별도로 있기 때문이다. 다만 C1-3만 읽는 독립 시행의 완전성은 영향을 받는다. 전체 대안 수가 같다는 이유로 후보 수준의 근거 차이를 지워서는 안 된다.

C1-4는 이전 raw HTTP 실패 뒤 `evidence/browser-observations.json`의 `BROWSER-C1-B-DIRECT-REQUESTS`에서 별도 정상 도착이 기록되었다. fragment 존재·346어절·Request/Session 구성 및 Session.send를 확인한 기록이 있으므로 앞선 입력 감사의 도착 미확인은 그 **새 시행에 한해** 해소된다. 생성 원장의 source_record가 실패한 candidate receipt만 가리키므로 최종 경로 원장에서는 browser-observations의 trial ID도 직접 연결해야 한다. 실패한 과거 HTTP 시행을 성공으로 덮어쓰면 안 된다.

## 6. C4 부분 원자와 C3 시행 합산 금지

C4의 원 atom은 그대로 유지된다. C4-2는 `C4.A1.taskgroup`, C4-5는 `C4.A1.gather`라는 부분 증거 ID를 따로 갖고 strict `supports_by_alternative`에는 A1 전체를 넣지 않았다. 이는 constructor/호출 계약을 느슨하게 바꾸지 않는 보존 방식이다. 두 부분 ID는 새로운 필수조건 분모 두 개가 아니다. 추후 평가기는 **같은 시행·같은 대안 안에서 두 부분이 함께 확인되었을 때만** 원래 A1 하나를 완성할 수 있다. A2는 별도 전체 조건으로 계속 필요하다.

표시 코드북에는 작은 불일치가 남는다. V2.A1의 일부만 입증한 행은 verdict=`조건부`, counts_as_proven=false지만 C4-2/5의 같은 종류 부분 증거는 자동 생성 분기 때문에 verdict=`미확인`이다. 완전성 산술은 둘 다 거짓이어서 같지만, 동일 코드북의 의미 설명을 맞추거나 차이를 명시해야 한다. 원 요구·키 변경은 필요하지 않다.

C3의 B는 첫 대표가 release 한 장이다. `release → ExceptionGroup` 시행에서 얻는 A1과 `release → except*`의 다른 시행에서 얻는 A2를 합쳐 한 사람의 완전 답으로 만들 수 없다. 형제 목록을 열고 멤버 하나를 읽은 경우에도 그 한 원문만 읽었다. 반대로 A/C의 PEP 대표에서 실제 목차 Specification으로 가는 경로는 같은 시행에서 두 조건을 얻을 수 있는 별도 검사 대상이다. 이 감사 시점에는 `gold-paths.csv`, `clicks.csv`, `changes.csv`가 아직 없으므로 이런 독립 시행 분리와 실제 도착을 **검증 완료로 승인하지 않았다**.

C2도 같은 원칙이다. 형제 목록→C2-3만 읽은 시행에 아직 열지 않은 C2-1의10개 대안을 자동으로 더할 수 없다. C2-1을 먼저 열고 그 절의 실제 Chart visualization 링크를 여는 경로는 다른 합법적 후보 시행이며, 도착/창을 실제 확인한 뒤 판정해야 한다.

## 7. W와 남은 검증 경계

C1-6은 fragment_confirmed=false이며 strict 지원이 없다. 동시에 `full_document_supports_by_alternative`에는 HTTPX 완전 지원이 들어 있다. 이는 같은 clients 문서 전체에는 근거가 있다는 의미 자료일 수 있지만, SCOPE의 누락 fragment를 성공 클릭으로 바꾸지 않는 규칙을 무효화하지 않는다. W 평가기가 이 필드를 보고 도착 실패를 자동 성공 처리하지 않는지 최종 경로 감사가 필요하다. W는 판독 범위의 한 요소만 완화하는 것이지 URL 수선이나 추가 클릭 면제가 아니다.

C4-2/4/5의 W에서 A1이 지원되는 것은 같은 asyncio-task 문서에 TaskGroup과 gather 설명이 함께 있기 때문이다. 그것만으로 별도 compound 문서의 A2까지 공짜로 가져오면 안 된다. C3에서도 W의 PEP 전체와 strict PEP 첫800 단어를 섞지 않아야 한다.

현재 승인 범위는 **고정 입력 해시, 그룹 산출, 첫 세 대표, 라벨 길이, 후보별 현재 지원 집합의 산술**이다. C 키 의미의 일반적 우수성, C1-3의 엄격 직접 증거, 실제 두 클릭 경로 완전성, 전체문서 민감도의 도착 gate, 실제 사람의 채택은 이 감사만으로 승인되지 않는다.
