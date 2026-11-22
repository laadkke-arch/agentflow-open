# xarray 후속 판독 — 봉인 뒤 실제 질문·답·행동

T0 원격 봉인 `9de54923257d613359348c8ccee2ff8225c8a0d8` 이후에 읽었다. 판독자 `/root/xarray`의 같은 작업자 재검이며, 독립·블라인드 이중 코딩으로 부르지 않는다. root가 핵심 댓글을 별도 재독했다는 통지는 별도 검토다. 이 파일의 판단은 공개 대화에서 관측한 연결이며 전략의 반사실적 효과가 아니다.

## 부모 통합용 필수 수치

| 범위 | 사례 분모 | root30 실제 기존환경·목표·입력 질문 | 같은 변수의 기존값 엄격 직접답 | 명시적 같은지원자 권고변경 | 동일 입력의 새 한정동작 성공 | 동일 입력의 새 실패 | 원래 전체 목적 검증 성공 |
|---|---:|---:|---:|---:|---:|---:|---:|
| A | 8 | 3/8: X02(후발), X04, X07 | 1/8; 질문 있음 중1/3: X07 | 0/8; 엄격 직접답 중0/1 | 1/8: X04 직접 GeoTIFF 열기 | 0/8 | 0/8; X04 전체 메타데이터·intake 통합 미확인 |
| 선정 B | 5 | 4/5: XB03,XB08,XB13,XB14 | 4/5; root30 질문 있음 중4/4 | 0/5; 엄격 직접답 중0/4 | 0/5 | 1/5: XB13 원 파일 | 0/5 |
| B 전체 시도 | 27 | 발생률 집계에 사용하지 않음 | 선정 B와 합치지 않음 | 별도 감사 원장 | XB25는 질문 없는 실행의 보강 반례 | XB23·XB27 등 진단 실패 보존 | 별도 채택/시행 판단을 A/B8에 합치지 않음 |

root90에서 위 엄격 분자는 바뀌지 않는다. X05의 복사 의미 질문, X08의 설계 질문은 별도 design_semantics_request이다. B의 XB06은 root30과 root90 모두 실질 타인 댓글이 없지만, 최초 실제 질문이 16개월 뒤라는 이유로 B에서 삭제하지 않았다.

A 첫 실질 응답의 정보질문은 X04/X07의2/8이다. 후발 X02를 더하면 root30 전체 질문3/8이다. X04는 질문 문장에 이어 답했지만 안내된 호출을 새로 실행한 답으로 읽힌다. **기존값 회수**에 관한 엄격 직접답에서는 제외하고, 질문 내용에 대응한 새 실행까지 허용하는 확장 정의에서는 A 직접답2/3이다. 이 경계가 결과를 바꾸므로 `direct_answer_content=true`와 `category=post_advice_execution_answer`를 함께 남겼다.

선정 B의 직접답4건 가운데 XB03은 현재 root에 있던 핵심문제의 재진술에 새 array API 맥락이 덧붙은 것이다. 실제 첫판의 전체 문구는 복원하지 못했으므로 `core_value_present_in_current_root=true`와 `pre_first_version_proven=false`를 함께 둔다. XB08의 버전은 작성자가 첫 질문 뒤 위 본문에 추가했다고 확인했다. 따라서 버전 값이 처음부터 있었다고 세지 않는다.

## 단계별 사례 판정

| 사례 | 관측한 답과 선택 | 행동 및 한계 | 핵심 원문 |
|---|---|---|---|
| X01 | 명시 encoding 대체를 설명하고 기존 dict 직접 수정 안내. 질문 없음 | 작성자 후속 실행 없음. root의 Edit와 우연히 본 미래 close 문구 노출은 T0에 보존 | [첫 답](https://github.com/pydata/xarray/issues/7406#issuecomment-1383184222) |
| X02 | 초기 mode=w/tmp_path 제안 뒤 **묻지 않은** S3+moto 사실 공개. 지원자가 이해를 수정해 오류 자료 요청 | 작성자는 다른 버그로 막혀 제공하겠다고만 답. 요청한 오류·traceback 값 없음 | [자발 공개](https://github.com/pydata/xarray/issues/7408#issuecomment-1369880263), [요청](https://github.com/pydata/xarray/issues/7408#issuecomment-1369974685), [중단](https://github.com/pydata/xarray/issues/7408#issuecomment-1370139670) |
| X03 | Dataset 임시 변환 제안에 이해했다는 답. Series 선호는 root에도 있었음 | 실제 호출/반환 결과 없음. 제3자 구현 제안은 별도 | [작성자 답](https://github.com/pydata/xarray/issues/7409#issuecomment-1398072586) |
| X04 | 호출을 묻는 문장과 동시에 rasterio 조건부 실행을 제시. 작성자는 그 호출로 동작했다고 보고 | 직접 GeoTIFF 열기 성공. 성공 뒤 entrypoint/list_engines 설명이 추가되므로 Q→권고변경→실행이라는 순서가 아님. 전체 geospatial 보존/intake 통합 미확인 | [실행 답](https://github.com/pydata/xarray/issues/7411#issuecomment-1372480571), [뒤의 설명](https://github.com/pydata/xarray/issues/7411#issuecomment-1375736147) |
| X05 | 공급자가 두 설계안에 동의하고 PR을 언급. 30일 뒤 제3자의 복사 의미 질문에 원 작성자가 답 | 새 기능 개발과 사용자 시행을 구분. 작성자 실행 없음 | [PR 보고](https://github.com/pydata/xarray/issues/9196#issuecomment-2218045878), [의미 답](https://github.com/pydata/xarray/issues/9196#issuecomment-2261578914) |
| X06 | root90 인간 실질 응답 없음 | fork commit 참조를 새 실행으로 인정하지 않음 | [root](https://github.com/pydata/xarray/issues/9197) |
| X07 | 신규 기여자가 원 작성자/유지관리자에게 pure-xarray의 뜻을 물음. 원 작성자가 목적을 직접 설명 | 질문한 newcomer의 후속 선택 없음. 이후 제3자 재현은 원 작성자 실행 아님. 유지관리자 겸 요청자 제외 감도에서 이 엄격 직접답은 빠짐 | [답](https://github.com/pydata/xarray/issues/9201#issuecomment-2206433913), [제3자 재현](https://github.com/pydata/xarray/issues/9201#issuecomment-2292210004) |
| X08 | 처음 목적은 shoyer의 다른 토론 발화를 TomNicholas가 옮긴 것. 뒤의 설계 질문에는 61일 뒤 되묻기 | 설계 선택/실행은 미확인. 질문→답처럼 보여도 의미 재확인이며 직접 설계값 답 아님 | [root](https://github.com/pydata/xarray/issues/9203), [되묻기](https://github.com/pydata/xarray/issues/9203#issuecomment-2338399208) |
| XB03 | 핵심 문제 재진술 뒤 응답자의 해석이 넓어지고 선호를 다시 물음 | 첫 질문 전 기술제안이 없어서 no_prior_proposal. special case 제거 선호의 형성 시점은 미확인 | [첫 답](https://github.com/pydata/xarray/issues/7721#issuecomment-1510169910), [선호 답](https://github.com/pydata/xarray/issues/7721#issuecomment-1516251985) |
| XB06 | 16개월 뒤 질문에 xarray 고유인지 모른다고 답. 당시부터 쓰던 retry 우회 회고 | root30/90 양성 없음. late question30에는 새 로그 실패가 있지만 xarray 판이 바뀜. 원인 판별값은 여전히 미확인 | [미확인 답](https://github.com/pydata/xarray/issues/7726#issuecomment-2318466786), [새 로그](https://github.com/pydata/xarray/issues/7726#issuecomment-2331409793) |
| XB08 | 첫 질문 뒤 버전 표 추가. 지원자가 이후 진단·engine=flox 벤치마크 | root90 안 작성자는 감사만. **2023-09-06T21:08:04Z** 작성자 성능 개선 보고는 root+153일 밖 late_history에 보존 | [버전 추가](https://github.com/pydata/xarray/issues/7730#issuecomment-1499263329), [늦은 실행](https://github.com/pydata/xarray/issues/7730#issuecomment-1709120441) |
| XB13 | local 여부와 filename 두 변수를 한 답에 제공. 뒤의 engine 지정 trial 여부는 답하지 않음 | 원 파일의 새 독립 open은 실패. 다른 파일+다른 Python에서 성공은 원 입력 성공으로 합산하지 않음 | [직접 답·실패](https://github.com/pydata/xarray/issues/7754#issuecomment-1509390748), [다른 대상 성공](https://github.com/pydata/xarray/issues/7754#issuecomment-1510522371) |
| XB14 | backend는 바로 답했으나 server/filesystem 용어는 모름. mounted NFS라는 설명 뒤 두 번째 변수 답 | 같은 지원자는 질문 의미를 고쳤고 기술 설명은 다른 지원자가 제공. 새 작성자 실행 없음 | [부분 답](https://github.com/pydata/xarray/issues/7758#issuecomment-1509633511), [최종 변수 답](https://github.com/pydata/xarray/issues/7758#issuecomment-1509899467), [다른 지원자 코드](https://github.com/pydata/xarray/issues/7758#issuecomment-1516738260) |

## 대기·왕복 단위

`answers[].roundtrip_key`는 사례·실제 질문 댓글·답 댓글의 조합이다. 두 변수에 같은 답을 한 XB13은 한 왕복이다. XB14는 용어 설명 뒤 다시 답하여 두 왕복이며, 두 번째 답의 **직전 재표현→답** 대기는0.0247시간, **처음 질문→그 변수 최종 답**은11.7547시간이다. `episode_elapsed_hours`로 후자를 복원할 수 있다. `question_utterances`와 `question_episodes`도 분리했다.

엄격 직접답 왕복은 A1, 선정B5이다. A 직접답 대기는2.42시간, B 최초 질문 episode에서 직접값에 이르는 대기는2.7572–11.7547시간이다. A의 post-advice 실행 답 X04는26.1786시간, X02의 값 없는 중단 답은2.8403시간이다. XB06의 늦은 첫 답은22.6306시간이지만 필요한 원인변수를 모른다는 답이다. no-answer의 question30 상한은720시간이며, 실제 클릭·읽기시간·대체 노동은 미확인이다. 중첩 대기는 합산하지 않는다.

## 반증 경로와 감도

1. **답이 왔다고 정보가 늘어난 것은 아니다.** XB03의 핵심문제는 현재 root에도 있다. 다만 원판이 U이므로 완전한 재질문 확정 사례로 과장하지 않는다. 답이 만든 추가 맥락과 원래 있던 핵심을 나눈다.
2. **후속 이해 수정이 실제 질문의 효과일 필요는 없다.** X02의 조언 수정은 질문 없이 자발 공개된 사실에 반응했다. 뒤의 실제 오류 질문은 값 답변을 얻지 못했다.
3. **질문과 즉시 행동을 함께 주어도 실행이 권고변경보다 앞설 수 있다.** X04는 질문이 필요한 후보변경을 일으킨 사례가 아니라, 함께 주어진 조건부 안내의 실제 적용을 관측한 사례다.
4. **질문 없는 안내로 실행할 수 있다.** B 시도 XB25의 [첫 제안](https://github.com/pydata/xarray/issues/7782#issuecomment-1520277594) 뒤 [부분 결과](https://github.com/pydata/xarray/issues/7782#issuecomment-1520341470), 같은 지원자의 [대안](https://github.com/pydata/xarray/issues/7782#issuecomment-1520363622), 작성자의 [작동 보고](https://github.com/pydata/xarray/issues/7782#issuecomment-1520409398)가 이어졌다. A/B선정 분모에 편입하지 않는다. 한 링크 뒤 모호한 완료만 있는 [XB11](https://github.com/pydata/xarray/issues/7742#issuecomment-1501076957)은 구체 실행으로 승격하지 않는다.
5. **실행으로 답해도 물은 기존값의 답은 아닐 수 있다.** B 시도 XB22의 후발 버전질문에 작성자는 [main에서 재현되지 않음](https://github.com/pydata/xarray/issues/7772#issuecomment-1519897098)을 보고했다. 원래 버전값 직접답과 다르다.
6. **목표/선호 형성은 시간정보 없이는 구별 불가하다.** XB03의 special case 선호, XB14의 대기 허용도는 뒤에서 표현되지만 질문 전부터 있었는지 새로 골랐는지 확인하지 못했다.

X01 T0 미래노출과 XB08 사후 확인된 버전표 노출을 미노출 감도에서 제외한다. X07의 역할 반전과 X05/X08의 유지관리자 요청은 일반 사용자 지원으로 일반화하지 않는다. X04를 확장 직접답에 포함해도 엄격 연결된 권고변경과 전체 chain_success는0이다. 미확인 실행을 모두 성공으로 가정하면 실행비율은 크게 바뀔 수 있으나, 실제 문장에 없는 전 제안·같은 지원자 명시 연결을 만들어0을 양성으로 바꾸지는 않는다. 그 경우는 별도 미확인 상한 가정으로 표시해야 한다.

## 원판·관측 완전성·제공자 근거

`initial-field-audit.jsonl`13행은 목표/이미 시도/판·설정·입력/원하는 출력/선호·필수·금지를 T0 캐시 hash와 줄 위치에 매핑한다. 모든 hash가 봉인된 initial과 일치했다. **후속 열람 뒤 위치 보강**이며 최초판 복원이나 사전 판정 추가로 주장하지 않는다. 원판 등급은 T0대로 유지했다.

A8+전체 B27의 comments page2가 모두 빈 배열임을 원격 확인했다. 선정13개의 timeline page2도 모두 빈 배열이다. 따라서 현재 공개되는 댓글 창을 읽은 의미에서 public_visible_complete이며, 삭제됐던 과거 본문까지 완전하다는 주장은 아니다. B 비선정22건은 모든 root90 인간 댓글의 prose를 읽되 긴 fenced code는 screening에서 생략했다. 그 생략된 출력으로 새 기술적 성공을 주장하지 않는다. 선택13건은 실제 판정에 사용한 코드와 출력도 읽었다.

`providers.jsonl`은 당시 tag/commit의 공식 근거11개를 담고, 같은 파일의 판 보강 XD06과 보조 반례 XD10은 최소수 산입을 껐다. XD06은 X01의 실제2022.03판에서 encoding 대체를 확인한다. XD09b는2022-12-19 배포된 rioxarray0.13.3의 rasterio entrypoint를 확인한다. XD07/XD08의 remote retry는 전체 open_dataset timeout 보장이 아니며 XB14의 요구를 충족한다고 결론내리지 않는다. XD11은 mixed array libraries가 표준 범위 밖이라는 당시 결정의 직접 근거다. 각 자료의 범위와 한계는 원장에 있다.

## 파일·검사·남은 첫 자료

`chains.jsonl`13행이 주 후속 원장, `later-questions.csv`8행이 후발 질문, `screening-followups.jsonl`27행이 모든 B 시도 창 감사, `reading-updates.jsonl`35행이 동일 thread 재열람 기록이다. `corrections.jsonl`4행은 봉인 원장을 수정하지 않고 이후 드러난 편집/시점을 기록한다. `critical-reread-receipts.json`의6개 핵심 댓글은 원격으로 다시 열었고 캐시 body hash와 일치했다.

이 stream에서는 제품 코드·사례의 실행 환경을 실행하지 않았다. 실행 성공은 공개 작성자 보고이며 재현 실행을 했다고 말하지 않는다. 모든 원시 원문은 ignored retrieved/에 두고 공개 파일에는 URL, 시각, hash, 필요한 짧은 인용·한국어 요약만 남겼다. 부모가 commit/check를 담당한다.

| 가장 중요한 불일치 또는 약점 | 근거 URL | 영향을 받는 판단 | 다음 조사 제안·첫 자료 |
|---|---|---|---|
| 현재 root를 첫판으로 읽으면 XB08 버전이 질문 전에 있었던 것으로 뒤집힘 | https://github.com/pydata/xarray/issues/7730#issuecomment-1499263329 | 이미 있던 값·미래정보 미노출 감도 | 해당 issue 본문 edit diff의 버전 표 추가 시점 |
| X04 직접 실행 성공은 원래 호출값 회수·권고변경 뒤 실행과 순서가 다름 | https://github.com/pydata/xarray/issues/7411#issuecomment-1372480571 | 직접답 분자와 chain_success | 질문 전 실제 호출 및 동일 GeoTIFF의 metadata 비교 출력 |
| XB13 성공의 파일·Python판이 원 실패와 다름 | https://github.com/pydata/xarray/issues/7754#issuecomment-1510522371 | 같은 입력 실행 성공 및 원목표 전체 해결 | 원 파일의 공개 형식 정보와 명시 engine 시험 결과 |
