# AF-RES-096 밀려난 주 도구 12자리 독립 감사

**PASS · 오류 0건. 탐색 12/12, A만 완결 관찰 0/6쌍.**

분석 기준은 사전 봉인 `d03ca37daf0c43688c68bc39417d84a9b84803e9`다. 노출·접근·최종 판정은 수정하지 않았다. 여섯 경계 요청의 A 3·4위를 전수 추적했으며, 사후 답/댓글과 새 외부 본문은 열지 않았다. 공식 원문의 내용은 기존 절 메모·조건 판정에 귀속하고, 캐시 본문은 기록된 hash만 기계 검산했다.

|요청·A순위|밀려난 파일·기존 절|기록된 핵심 내용|A 사용/반환|필수조건 손실 검토|
|---|---|---|---|---|
|J2 · 3|[JQ-0080](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/tests/jq.test) `tests/jq.test` · 119-166, 424-446|누락 필드/범위 밖 접근의 null 및 변수 바인딩을 보여 주는 상류 기대출력.|예/예|A는 C3의 입력 누락 진단에 이 시험을 반환했다. B도 유지된 JQ-0001:408-435로 같은 null 진단을 했다. 시험이라는 별도 근거 형식은 없어졌지만 누락 offset의 출처나 필수조건 완결은 어느 경로도 확보하지 못했다.|
|J2 · 4|[JQ-0072](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/parser.c) `src/parser.c` · 3971-4002|객체 pair 문법을 컴파일하는 parser 구현.|아니오/아니오|A가 읽은 3971-4002는 객체 문법 확인이며 최종 조건 근거로 쓰지 않았다. C1은 유지된 매뉴얼로 지지되고 C2 매핑/C3 offset 누락은 그대로다.|
|J3 · 3|[JQ-0004](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/builtin.jq) `src/builtin.jq` · 147-165|range/3의 증가 조건을 구현한 jq 내장 함수.|아니오/아니오|A는 147-165를 확인했지만 사용하지 않았다. A/B 모두 유지된 manual의 range·인덱스·병합 절과 JQ-0080의 기대출력으로 C1/C2를 지지했다.|
|J3 · 4|[JQ-0002](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/builtin.c) `src/builtin.c` · 92-114|plus가 문자열·배열·객체에 따라 동작을 나누는 구현.|아니오/아니오|A는 92-114를 확인했지만 사용하지 않았다. 같은 타입별 의미가 두 경로의 manual/원시험 반환에 남아 있어 기록된 조건 지지는 감소하지 않았다.|
|J4 · 3|[JQ-0002](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/builtin.c) `src/builtin.c` · 841-876, 908-915, 1037-1050|match의 문자열 입력·global flag, Oniguruma 컴파일, Oniguruma 없는 build에서의 실패 분기.|예/예|A는 C1에 이 파일을 사용·반환했다. B는 유지된 manual의 match/foreach 계약으로 같은 조건을 지지하지만, A의 구체적인 Oniguruma 부재 경고는 B 반환에 없다. 이것은 설명의 반대조건 손실이며 사전 문서상 완결 또는 실제 runtime 성공의 관찰 손실과 같지 않다.|
|J4 · 4|[JQ-0055](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/jv_parse.c) `src/jv_parse.c` · 506-544|JSON 파서의 유효 literal 요구.|아니오/아니오|A는 506-544를 확인했지만 사용하지 않았다. raw-input으로 로그를 문자열로 다루어야 한다는 조건은 유지된 manual:124-148이 직접 설명한다.|
|P1 · 3|[PD-0007](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/doc/faqs.md) `doc/faqs.md` · 139-230|FAQ의 형식 변환·참조 스타일 설명.|아니오/아니오|A가 읽은 139-230은 최종 조건 근거가 아니며 simpara role→custom-style 복구를 닫지 못했다. 두 경로의 반박은 유지된 DocBook reader 및 manual로 설명된다.|
|P1 · 4|[PD-0016](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/doc/pandoc-server.md) `doc/pandoc-server.md` · 150-244, 348-409, 17-35, 296-308|server API의 reference-doc 옵션 및 filter/외부 HTTP 제한.|아니오/아니오|이 server API는 원 사용자의 CLI와 다르며 A의 최종 조건 근거가 아니다. 읽은 절에는 DocBook role 복구가 없다는 원 메모가 남아 있다. 이를 제거한 것이 CLI 복구의 실패 원인이라는 관찰은 없다.|
|P3 · 3|[PD-1324](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/test/mediawiki-reader.native) `test/mediawiki-reader.native` · 1-25, 120-185|빈 metadata와 MediaWiki RawInline/RawBlock 예제가 있는 native 기대출력 fixture.|아니오/아니오|원 요청은 YAML signature/template이다. 다른 reader이고 metadata가 비어 있어 A도 이 파일을 조건 근거로 사용하지 않았다. A/B의 최종 구성은 유지된 manual 하나에 근거한다.|
|P3 · 4|[PD-0022](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/src/Text/Pandoc/App/CommandLineOptions.hs) `src/Text/Pandoc/App/CommandLineOptions.hs` · 298-315, 357-375, 1214-1253|-V 문자열 변수와 metadata/template 변수 옵션을 구분하는 CLI parser.|아니오/아니오|초기 -V 후보를 이해하는 데는 쓰였지만 R chunk 값의 전달 시점은 입증하지 못했다. 사전 최종 판정은 원 생산 경로를 유지하는 raw HTML scalar 구성으로 바뀌었고 이 파일을 사용·반환하지 않았다.|
|P4 · 3|[PD-0007](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/doc/faqs.md) `doc/faqs.md` · 95-121|FAQ의 일반 변환 설명.|아니오/아니오|A가 읽은 95-121은 원 TikZ 그림의 AST→PDF→SVG 접합을 닫는 최종 근거가 아니다. 두 경로의 최종 반환은 유지된 Lua-filter 예제와 manual이다.|
|P4 · 4|[PD-0008](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/doc/filters.md) `doc/filters.md` · 1-65, 475-512|reader→AST→filter→writer의 일반 구조와 필터 예시.|아니오/아니오|일반 필터 구조는 확인했으나 정확한 TikZ preamble/그림 보존을 독립 지지하지 않는다. 원 기록은 반환한 PD-0012/PD-0001에 전체 문서상 구성을 귀속하며 이 파일을 사용하지 않는다.|

## 분자와 분모

- 경계쌍 6건 × 주 도구 두 자리 = **12자리**, 서로 다른 파일 **10개**. 반복 파일을 새 자료로 늘리지 않았다.
- A 실제 열람 **12/12**, A 최종 판정 사용 **2/12**, A 반환 **2/12**. B 노출·열람은 0/12다.
- 명시 조건 **10개**의 A/B 상태를 비교했고 차이는 **0개**다. 밀려난 파일만을 단독 근거로 적은 전체 조건은 **0개**다. 단독 인용 여부는 인과적 필요성과 같지 않다.
- A만 문서상 완결 **0/6쌍**. A만 완결 사례에서 밀려난 자리 **0/12**. 알려진 사례를 넣거나 사후 원문으로 이 분자를 채우지 않았다.
- ②봉인과 **43개 입력**의 bytes가 정확히 일치하고, 밀려난 파일의 기존 **22개 절** hash를 재계산했다. 새 body 접근은 **0회**다.

## 완결 손실과 설명 손실을 구별

관찰된 필수조건 완결 손실은 없었다. 그러나 모든 설명이 같아진 것은 아니다. J2-B의 반환은 J2-A가 붙인 누락키/null 상류 fixture의 별도 확인을 잃었다. J4-B는 J4-A가 반환한 Oniguruma 없는 build의 구체적인 실패 경고를 잃었다. 두 차이는 원 판정에 기록된 사실이며, 이 감사는 이를 반례 설명의 손실로 남긴다. 실제 사용자 build 실패나 문서상 완결 패배로 사후 승격하지 않는다.

## 사실·추론·설계 제안

**사실:** 노출 ID·원 순위·열람 절·사용/반환 ID와 A/B 판정은 고정 원장에서 재계산했다. 원문 내용 요약은 처음 읽은 연구자의 메모에 귀속한다.

**추론:** 현재 표본에서는 필요한 큰 manual/원시험이 상위 두 자리에 남아, 3·4위를 바꾸어도 최종 요구 충족 상태가 달라지지 않았다. 이것이 모든 요청에서 성립하거나 같은 연구자의 기억 영향을 배제한다는 결론은 아니다.

**설계 제안 / 다음 최소 확인:** 새 질문에서 필수 조건을 해결하는 주 도구 절이 실제 3/4위 파일에만 있고 1/2위에는 없다는 사전 판별을 봉인한 뒤, 독립 평가자가 두 노출 집합으로 같은 입력을 처리하도록 한다. 결과를 아는 현 8질문은 재모집하지 않는다.

## 적용 한계

- 관찰0은 봉인된 여섯 경계쌍의 문서상 완결 손실 0이다. 범위 확장의 실제 안전성이나 모든 가능한 요청에서 손실 없음이라는 명제가 아니다.
- 조건이 한 파일만 인용하는지와 파일 제거의 인과적 필요성은 다르다. 본 감사는 재실험 없이 기록된 조건·반환·판정의 관계를 추적했다.
- 새 원문 절을 열지 않아 기록되지 않은 절에 필수조건의 유일한 해법이 있는지는 미확인이다. 원 메모와 hash의 일치가 모든 해석의 참을 입증하지 않는다.
- 동일 연구자의 양 경로 기억 노출과 큰 manual이 상위 두 자리에 유지되는 구조가 손실 관찰을 줄일 수 있다. 독립 평가자/파일 분할은 새 실험이어야 한다.
- 실행 성공이나 사용자판 실패를 관찰한 분석이 아니다. 특히 J4 build 반대조건의 누락을 완결 패배로 사후 재분류하지 않았다.

## 감사 입력과 재실행

각 고정 judgment 링크·해시·원 절·전체 조건 비교는 displacement-audit.json에 있다. 루트 experiment.py/seal_routes.py나 사후 승패 요약을 호출하지 않았다.

```bash
python -B docs/workstreams/research/AF-RES-096/evidence/audit/audit_displacement.py
```

## 오류

없음.
