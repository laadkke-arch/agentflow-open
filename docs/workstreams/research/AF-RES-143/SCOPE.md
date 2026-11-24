# AF-RES-143 · 출력 전 고정 범위

계획 기준은 d950356cdfae3edf799870cdeb90b93b5bd4ffd3이다. 배정 checkout HEAD는 24d4766a70c3153dbe1ee4f14f202d1b12c94b25였고 직후 원격 통합판은 d35bf54869a828cd76a74cf3075be094f62e5a59였다. 로컬 work 참조와 작업 브랜치 이름이 충돌해 별도 GitHub clone을 열었다. 별도 clone에서 방금 fetch한 최신 통합판 c088f5af075c3b010102d002e66c84d9263fe5de에서 브랜치와 [계약](manifest.json)을 고정했다. 최신판의 AGENTS, STATE, START_HERE, DOT_AUTOMATION, RESEARCH_WORKFLOW, RESEARCH_BRIEF와 진행표의 AF-RES-143, AF-RES-139 행을 읽었다. 등록 선행은 AF-RES-139 하나다. 중앙 DONE과 고정 인계 PARTIAL을 구별한다. [통합 진행표](https://github.com/laadkke-arch/agentflow-open/blob/c088f5af075c3b010102d002e66c84d9263fe5de/docs/automation/dot-control.json) · [139 고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/c06598bada3039eae441a9ba49fd28837108873a/docs/workstreams/research/AF-RES-139/HANDOFF.md) · [139 고정 결과](https://github.com/laadkke-arch/agentflow-open/blob/1aabc75823d6f919ac74ca9e06cfc8d1b614f2ec/docs/workstreams/research/AF-RES-139/RESULT.md)

## 모집과 노출

- simple-statistics는 2023-01-15의 7.8.1을 발판으로 삼고 2026-01-01 UTC 전 나머지 정식판 7개를 사용한다. 7.8.1→7.8.8, 8판 7경계다. d3-array는 2020-01-01부터 2026-01-01 UTC 전 정식 공개 중 첫 16판인 2.5.0→3.0.3, 15경계를 사용한다. 판 모집은 현재 npm packument의 버전과 UTC time이 함께 존재해야 한다. 같은 밀리초는 숫자 semver로 정렬하며 순위 차이·사전판·time-only·태그만 있는 후보를 별도 기록한다. 이전 삭제·철회 흔적의 완전한 복원은 미확인이다. 태그와 배포의 gitHead가 다르면 양쪽을 보존한다. [모집과 지문](evidence/roster.json) · [SS-REG](https://registry.npmjs.org/simple-statistics) · [D3-REG](https://registry.npmjs.org/d3-array)
- 139의 SCOPE, signals, 사후 벡터, 비용 42행 및 replay 구현을 고정 인계 SHA에서 읽었다. 6.1.0→6.1.1의 #334와 기존 벡터 두 결과, 7.8.1의 고정 스칼라, 135의 d3-scale null 대조에 대한 139 설명이 선노출이다. d3-array의 2.4.0 README·구현·시험과 simple-statistics의 7.8.0 구현·시험만 새 창 바깥의 계약·입력 선정에 읽었다. 두 새 창의 명부와 배포 메타데이터 열람, 정적 코드와 공식 공지로부터의 추론, 공개 함수 실행 및 새 판의 결과 열람은 다른 사건이다. 새 창의 실행과 새 변경 이슈·시험 기대값 열람은 원격 predictions.csv와 그 해시를 확인한 뒤 시작한다. 두 옛 #334 입력은 교정층 AF139-CAL에 고정한다. [139 범위](https://github.com/laadkke-arch/agentflow-open/blob/c06598bada3039eae441a9ba49fd28837108873a/docs/workstreams/research/AF-RES-139/SCOPE.md) · [옛 벡터](https://github.com/laadkke-arch/agentflow-open/blob/c06598bada3039eae441a9ba49fd28837108873a/docs/workstreams/research/AF-RES-139/evidence/posthoc-array-p.json)

## 입력과 동일성

[고정 입력](replay/inputs.json)의 각 패키지에 명시 입력군 21개를 둔다. 정식 입력에는 홀짝, 동일 값의 순열, 중복, 경계 0/1, 부분 위치, signed zero, 길이 1을 넣는다. SS는 오름·내림·중복·길이 1의 p 벡터를 지원 계약으로 분리한다. 빈 표본, NaN과 범위 밖 p, 빈 p 벡터는 별도 층이다. SS의 큰 표본은 1000→0의 닫힌 정수열로 고정했다. 선행 quickselect 회귀와 같이 큰 구간을 타는 입력이다. 두 구판만 한 과정씩 실행해 배열 값과 예외 직렬화를 검산한다.

d3의 p는 역사 README의 [0,1] 안의 숫자다. 배열 p 두 가지는 지원 범위 밖 대조층이다. quantile과 median의 iterable·선택적 accessor 및 quantileSorted의 오름차순 배열·필요 인덱스 accessor를 별개로 기록한다. quantileSorted의 정렬되지 않은 직접 전달, 결측 포함, typed array는 방어 대조로 분리한다. median의 결측 무시는 README와 회귀 시험을 대조한다. quantile의 null 포함 입력은 역사 문서에서 보장 범위를 판독한 만큼만 해석한다. 빈 표본은 별도 층에 둔다. accessor는 value 필드를 반환하고 호출 인덱스와 세 번째 인수의 동일성만 기록한다. 호출 기록 차이는 반환값 또는 입력 변경과 구별하는 보조 관측이다. [d3 문서](https://github.com/d3/d3-array/blob/8153bcd3f2ea19d7a1d7e6edadf47ed8b673de05/README.md#L97-L123) · [SS 계약](https://github.com/simple-statistics/simple-statistics/blob/362641a695c3b27cba9a6ae721f7c6e8dba48f62/src/quantile.js#L4-L22)

direct는 새 원 배열을 직접 전달한다. sorted_copy는 별도 정렬 복제본을 전달한다. 정상 수는 수치 오름차순, null·undefined·NaN은 뒤에 두고 동률은 안정 정렬한다. 두 호출의 실제 전달 배열과 원 배열을 각각 전후 기록하고 p 벡터 순서도 남긴다. 길이 128 초과 배열은 전체 인코딩의 SHA-256, 길이, 양 끝 표본과 고정 생성 규칙을 사용한다. 숫자는 정밀 일치이며 NaN, −0, ±Infinity, undefined, null, hole을 각각 구별한다. 예외는 이름·코드·본문을 비교하고 스택과 절대 경로는 진단에만 쓴다. 반환/예외·인수(p 포함) 보존으로 비교 상태를 정하고 accessor 호출 궤적 차이는 별도 열에 둔다. API 유무가 양 실행에서 확인되면 가용성 차이로 보고하며 값 변화 분모에서 제외한다. 설치·로더·실행 실패 또는 두 경로의 불합의는 미확인이다. 함수·입력층과 판 경계의 한 셀 이상 변화 집계를 함께 보존한다. 발표순과 같은 semver 순서는 중복 계수하지 않는다.

## 사전 예측 정책

A는 정확판 첫 조회 직접 실행이다. C는 고정판의 기능 문서 본문만 비교한다. SS는 함수별 src JSDoc, d3는 README의 quantile·quantileSorted·median 항목이다. 댓글 경계, 줄 앞 별표, 공백을 정규화한다. 문서 본문·인수·예시·항목 순서를 보존한다. D는 C와 함께 공개 진입 파일, 대상 소스 및 정확한 직접 의존의 원바이트·경로 지문을 비교한다. E는 패키지 내부 공개 함수와 정적으로 해소한 직접 호출의 토큰 지문, 해당 판에 이용 가능하다고 확인한 공지의 고정 단어를 쓴다. E2는 E에 정적 호출 한 단계만 더 더한다. 사용자 accessor가 명시된 자리는 고정 입력으로 취급하고 기본 accessor가 정적 binding이면 추적한다. 함수의 기본 인수 표현식은 본문과 함께 지문화한다. 파서, 중복 이름, 래퍼, 배포-소스 판 대응의 실패와 공식 공지의 당시 시각 미확인은 강제 사유다. 동봉 CHANGELOG는 해당 판 절만 사용하고 현재 공식 릴리스 본문은 당시에 존재한 본문을 증명하는 시각/보관 근거가 있어야 사용한다. 당시 본문이 확정되지 않으면 현재 키워드와 당시 사용 여부를 분리한다. 목록을 끝까지 읽었고 표본판 release가 없고 동봉판 절도 없으면 ‘관측 표면에서 없음’이다. 과거 삭제 가능성은 별도 감도로 다룬다. 공지 단어는 139의 quantile/quantiles/quantileSorted/quantileRank/quantileRankSorted, percentile/percentiles/percentileRank, median/medians/medianSorted, quartile/quartiles/interquartile/interquartileRange/IQR, interpolation/interpolate/interpolated를 유지한다.

현대 Node의 require(ESM) 호환성에 의한 변화는 피한다. CJS main 또는 명시 require export가 있으면 bare require, ESM 전용 공개 export는 bare import를 사용한다. 배포 manifest, 공개 entry 해시와 Node가 실제 resolve한 경로를 비교한다. 태그 src는 해당 판의 배포 코드와 대응시키는 자료다. 현재 npm의 동일 v3 lock을 쓸 실행 두 개는 각자 빈 디렉터리·캐시에서 설치한다.

## 질의열과 실측 경계

모든 발표판 순차와 양 끝판을 시작판부터 여섯 번 교대하는 질의열을 각각 고정한다. 판별 배치에는 전 입력을 사용하고 개별 답의 키는 (패키지, 요청판, 함수, 입력 지문, 로더)다. 각 정책의 첫 발판은 직접 측정한다. C/D/E/E2는 마지막 실측판부터 타깃까지의 발표 경계를 판독하고 하나라도 경보·강제가 있으면 요청판을 실행한다. 중간판은 질의되지 않으면 실행하지 않는다. 고정판 캐시가 있으면 경계와 실행을 생략한다. 같은 요청의 답에 정확한 요청판 링크와 별개 실측판을 붙인다. 비용 채점은 그 요청판의 출력 전용 판정을 사용한다. 현재 삭제 가능성이 열린 공지 부재는 이월 추정의 별도 한계다.

각 (패키지, 질의열, 정책)에서 데이터·지문·답 캐시를 비운 실행과 직후 동일 질의열의 보존 실행을 한 쌍으로 한다. 세 반복에서 정책 순서의 시작 위치를 0→2→4로 순환한다. 모든 정책은 응답 링크 검산을 위해 새 요청판의 문서 원본을 공통 취득하고, C/D의 비교에는 중간판의 공식 절도 읽는다. E/E2는 그 경계에 필요한 tar와 공지 근거를 취득한다. 고정 모집·락·공지의 메타데이터 목록은 공통 준비 자산으로 분리한다. 실제 요청 중 공개 URL HTTP 본문, 로컬 URL/판정/답 캐시 히트, 논리 지문 바이트, 설치·실행·정적 파서 횟수, 처음 요청부터 마지막 비교까지의 실측 벽시계와 CPU를 분리한다. npm 설치가 외부에서 몰래 자료를 받지 않도록 계측된 tar를 로컬 캐시에 공급하고 잠금과 대조한다. 링크 취득 및 공급자 네트워크 공유 캐시 상태, TLS·헤더·재전송은 HTTP 본문과 구분한다. 현재 프로세스와 기다린 자식 CPU를 기록하며 이 시점과 머신의 비용으로 제한한다.

## 타 분야와 원전 하한

SWR의 같은 적용 기간 기본/임시표에서 동일 날짜·열·기점/방향을 맞추고 139의 Sway 및 New Milton은 교정에 남긴다. 같은 운영기관 표에서 새 열이나 새 정차 셀을 찾아 변경과 유지의 짝을 확인한다. ONS ASHE Table 1 2023 잠정·개정의 UK full-time 총연간소득 전체 중위수와 인접 통계 셀을 같은 원표에서 판독한다. 잠정·개정 둘 중 하나의 원표를 열 수 없다면 접근 결측 증거를 고정하고 Census Vintage 2023/2024 총인구 원표의 같은 주와 기준연도 셀을 사용한다. California의 2022-07-01 인구와 바로 인접한 참조연도 또는 주 행을 우선 대조한다. 원표 차이, 당사자 설명, 연구자 비교를 따로 기록한다. 기존 SWR 관측 두 개와 ONS 공표 표시값은 새 원표의 성과 분모에서 제외한다. 고유 원저작 기준은 함수·계약 6, 회귀·자연 예·변경 저작 6, 배포·방법 6, 교통 3, 통계 3이다.
