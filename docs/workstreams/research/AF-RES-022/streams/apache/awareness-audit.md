# A 24건 인지 주체·표적 해법 독립 감사

**엄격한 해법 미인지→발견→인과적 선택 변경→실행의 관측 하한은 0/24다.** 초기 공개 선택에서 지정한 작성자가 지정 해법을 알았는지 미확인인 행은 A06·A07·A09이고, 최종 필요 기능이 후발인 A06을 분리하면 당시 소개 가능한 인지 기록완성 후보는 **A07·A09, 2건**이다. 이 두 행을 모두 음성 또는 모두 양성으로 완성한 **0/24~2/24(0~8.33%)는 인지 기록만의 조건부 시나리오**다. 엄격 인과효과의 상한, 모집단 발생률, 신뢰구간으로 읽을 수 없다.

입력은 streams/{adr,apache,rust}/decisions.jsonl의 24행과 각 sources.json이다. 원 unknown 플래그를 수정하지 않았다. 행별 정확한 주소·근거 ID·원판정·입력 SHA-256·감사 UTC는 awareness-audit.json에 있다. 첫 공개 제안의 기지 여부, 공개 선택 구간에서의 늦은 인지 사건, 생애 최초 인지일을 분리했다. **생애 최초 인지일과 사적인 최초 필요일은 각각 24/24 미확인**이며, 이를 공개 선택의 24건 미인지로 세지 않는다.

## 행별 감사

표의 기지는 baseline_known, 늦은 사건은 decision_actor_late_event_observed, 제공은 availability_before_initial_choice, 인과는 causal_change, 실행은 actual_execution이다. `?`는 미확인이다. 늦은 사건 `있음*`과 인과 `예*`는 **알려진 해법의 제약 교정**이며 엄격한 해법 최초 발견이 아니다. `없음`은 읽은 공개 구간에서 사건을 입증하지 못했다는 뜻이다. 실행 `예`는 각 행의 observed_implementation_scope 범위에 한한다.

| ID / 지정 주체·해법 | 초기 기지 | 늦은 사건 | 당시 제공 | 인과 | 실행 | 판정 근거 |
|---|---|---|---|---|---|---|
| A01 / freben · Kubernetes 형식 | 예 | 있음* | 예 | 예* | 예 | 기지 형식의 annotation 제약 교정. [ADR-D01](https://github.com/backstage/backstage/blob/86bb6cc6a8d3424a7f75393a05ebe225f9f68d55/docs/architecture-decisions/adr002-default-catalog-file-format.md) · [ADR-T01](https://github.com/backstage/backstage/pull/894) |
| A02 / freben · named export/React.lazy | 예 | 없음 | 예 | 아니오 | 예 | 첫 초안부터 함께 비교. [ADR-D02](https://github.com/backstage/backstage/blob/7fac93feea279d4a42b49a3a1f17c9ceebc597f4/docs/architecture-decisions/adr003-avoid-default-exports.md) · [ADR-F02](https://github.com/backstage/backstage/pull/1385) |
| A03 / Rugvip · index 공개 구조 | 예 | 없음 | 예 | 아니오 | 예 | 기존 재수출 구조를 알고 재설계. [ADR-D03](https://github.com/backstage/backstage/blob/582f63677678205956dbb6b69f563dc2934cfd65/docs/architecture-decisions/adr004-module-export-structure.md) · [ADR-F02](https://github.com/backstage/backstage/pull/1385) |
| A04 / mbruggmann · GCP Config Connector | 예 | 없음 | 예 | 아니오 | ? | 첫 초안 L62에 이름 명시. [ADR-D04](https://github.com/backstage/backstage/blob/1312d34147af604355117ee85ed913e7a9460092/docs/architecture-decisions/adr005-catalog-core-entities.md) · [ADR-T04](https://github.com/backstage/backstage/pull/1072) |
| A05 / epixa · lifecycle 대안 | 예 | 없음 | 예 | 아니오 | 예 | 기존 start/stop 및 분리안 비교. [ADR-D05](https://github.com/elastic/kibana/blob/57917dc50fd935b9511a4932f4540d61d86b70f6/rfcs/text/0001_lifecycle_init.md) · [ADR-T05](https://github.com/elastic/kibana/pull/32507) |
| A06 / njd5475 · node-crypto의 AAD | ? | 없음 | 아니오 | 아니오 | 예 | 최종 조건의 기능이 초기 제안 뒤 추가. [ADR-D06](https://github.com/elastic/kibana/blob/941ba313b102ae6d15d615bd452fcee045a2816f/rfcs/text/0002_encrypted_attributes.md) · [ADR-V04](https://github.com/elastic/node-crypto/pull/3) |
| A07 / joshdover · react-router-dom | ? | ? | 예 | ? | 예 | 초기판에 없고 후속판에 거절 문단. [ADR-D07](https://github.com/elastic/kibana/blob/5ec0bcf18041d2e6bb6046642ee0ce654121ba09/rfcs/text/0003_application_service_mounting.md) · [ADR-R07](https://github.com/elastic/kibana/blob/b8423952c036ae302c059afe2a606bc77dceee62/rfcs/text/0004_application_service_mounting.md) |
| A08 / epixa · handler/context 규약 | 예 | 없음 | 예 | 아니오 | 예 | 기존 패턴 공통화라는 직접 설명. [ADR-D08](https://github.com/elastic/kibana/blob/2b95f6179aa858a19f4069962cac47de6e9ebbbe/rfcs/text/0003_handler_interface.md) · [ADR-T08](https://github.com/elastic/kibana/pull/36509) |
| A09 / Bowen Li · RocksDB DBWithTTL | ? | ? | 예 | 아니오 | 예 | 2월 인지 미상, 5월 기지 거절. [AP-M25-ORIG](https://lists.apache.org/thread/47qqn7x9pb72wjv3c668jjt9jzhfxr50) · [AP-D25](https://cwiki.apache.org/confluence/rest/api/content/80452561?expand=body.storage,history,version&status=historical&version=6) |
| A10 / Eron Wright · YARN proxy/filter | 예 | 없음 | 예 | 아니오 | 예 | Servlet/Netty 제약을 알고 검토. [AP-D26](https://cwiki.apache.org/confluence/rest/api/content/80453255?expand=body.storage,history,version&status=historical&version=1) · [AP-J26](https://issues.apache.org/jira/browse/FLINK-9312) |
| A11 / Aljoscha Krettek · SourceFunction | 예 | 없음 | 예 | 아니오 | 예 | 구 API의 책임과 한계를 알고 비교. [AP-M27-ORIG](https://lists.apache.org/thread/334co89dbhc8qpr9nvmz8t1gp4sz2c8y) · [AP-F111](https://flink.apache.org/2020/07/06/apache-flink-1.11.0-release-announcement/) |
| A12 / Timo Walther · Scala/Java 모듈 | 예 | 없음 | 예 | 아니오 | 예 | 기지 선택; 후속 Blink 공급이 변경. [AP-M28-ORIG](https://lists.apache.org/thread/b8dvfrqr9xkr282f7mc9hkk04x7c2r9z) · [AP-M32-ORIG](https://lists.apache.org/thread/mqw9hhkq18673hoyct8ccov0t5m1wptz) |
| A13 / Jincheng Sun · SQL/DataStream 우회 | 예 | 없음 | 예 | 아니오 | 예 | 원 메일부터 우회 비용·제약 비교. [AP-M29-ORIG](https://lists.apache.org/thread/h1rhsoztg5onhgc07c7v4ppx06z2rzqf) · [AP-F19](https://flink.apache.org/2019/08/22/apache-flink-1.9.0-release-announcement/) |
| A14 / Xuefu Zhang · Hive/catalog | 예 | 없음 | 예 | 아니오 | 예 | 상위 필요와 구체 초안 모두 기지 대안. [AP-M30-ORIG](https://lists.apache.org/thread/r8xolxo9x0sxgl6obnt26d74pw3b60xz) · [AP-D30](https://cwiki.apache.org/confluence/rest/api/content/100827366?expand=body.storage,history,version&status=historical&version=2) |
| A15 / Zhijiang Wang · Netty 구성요소 | 예 | 없음 | 예 | 아니오 | 예 | 원 구조 인지와 재사용 설명. [AP-M31-ORIG](https://lists.apache.org/thread/wkogrk9tt2bznhnj6p0slltr09dhyho5) · [AP-M31-REPLY](https://lists.apache.org/thread/y28w05mogwh2s55kp2199djh7s7vqhtk) |
| A16 / Becket Qin · histogram/gauge | 예 | 없음 | 예 | 아니오 | 예 | 초안과 자체 benchmark에서 기지 선택. [AP-D33](https://cwiki.apache.org/confluence/rest/api/content/103089919?expand=body.storage,history,version&status=historical&version=1) · [AP-M33-REPLY](https://lists.apache.org/thread/pwzyp9bc46wbotcrnbxyrv84yo5c3nc6) |
| A17 / porky11 · struct/macro | 예 | 없음 | 예 | 아니오 | ? | 대안 기지; 거절 뒤 사용자 배포 미상. [RUST-D01](https://raw.githubusercontent.com/rust-lang/rfcs/ddfb37006552b7f973c429d1f981f2a251aaf444/text/0000-function-structs.md) · [RUST-F01](https://github.com/rust-lang/rfcs/pull/2276) |
| A18 / Manishearth · Cargo profile | 예 | 없음 | 예 | 아니오 | 예 | 기존 profile와 상위 빌드 제어 비교. [RUST-D02](https://raw.githubusercontent.com/rust-lang/rfcs/ffb1862b3f0d22b3665b16a1cd3ff12dfb373792/text/0000-custom-cargo-profiles.md) · [RUST-I2282](https://github.com/rust-lang/cargo/pull/5384) |
| A19 / Manishearth · CommonMark | 예 | 있음* | 예 | 예* | 예 | 구현 중 기지 명세의 제약 교정. [RUST-F03](https://github.com/rust-lang/rfcs/pull/2285) · [RUST-I2285](https://github.com/rust-lang/rust/pull/47046) |
| A20 / Manishearth · Criterion | 예 | 없음 | 예 | 아니오 | 예 | 추천 직후 이미 검토했다고 답함. [RUST-F04](https://github.com/rust-lang/rfcs/pull/2287) · [RUST-I2287](https://github.com/rust-lang/rust/pull/53410) |
| A21 / Centril · 기존 type bound | 예 | 없음 | 예 | 아니오 | 예 | 미인지 당사자는 별도 리뷰어. [RUST-D05](https://raw.githubusercontent.com/rust-lang/rfcs/e91e24dc42093cc2ab5b29fe0c4471645719d641/text/0000-associated-type-bounds.md) · [RUST-F05](https://github.com/rust-lang/rfcs/pull/2289) |
| A22 / nvzqz · stable write_bytes | 예 | 없음 | 예 | 아니오 | ? | 안정 Rust에서 가능하다고 인정. [RUST-D06](https://raw.githubusercontent.com/rust-lang/rfcs/202a265e8b7a37f2ca1cae5a9c05f2cf5b3f43fd/text/0000-mem-zero.md) · [RUST-F06](https://github.com/rust-lang/rfcs/pull/2291) |
| A23 / strake · if let/match 조합 | 예 | 없음 | 예 | 아니오 | 예 | 첫 초안에 기존 조합 명시. [RUST-D07](https://raw.githubusercontent.com/rust-lang/rfcs/8e4a6c97d71c53b91eac6933edb675d4c94c3695/text/0000-if-let-guard.md) · [RUST-I2294](https://github.com/rust-lang/rust/pull/79051) |
| A24 / kennytm · WTF-8/Pattern | 예 | 없음 | 예 | 아니오 | ? | 이전 설계 기지; 구현·안정화 미상. [RUST-D08](https://raw.githubusercontent.com/rust-lang/rfcs/ee0def25e14e125137648dbac7651d892fd99f62/text/0000-os-str-pattern.md) · [RUST-T49802](https://github.com/rust-lang/rust/issues/49802) |

## 불확실성 후보와 제외 이유

| 구분 | ID | 남은 연결·최소 확인 |
|---|---|---|
| 초기 인지 미확인, 최종 기능 후발 | A06 | 2019-03-22 초안은 node-crypto/AAD를 말하지 않는다. 필요한 AAD 인수는 04-12 추가되므로 완성된 해법을 초기 선택에 소개할 수 있었다고 세지 않는다. 라이브러리 자체의 선행 인지는 여전히 미확인이다. [ADR-D06](https://github.com/elastic/kibana/blob/941ba313b102ae6d15d615bd452fcee045a2816f/rfcs/text/0002_encrypted_attributes.md) · [ADR-V04](https://github.com/elastic/node-crypto/pull/3) |
| 당시 소개 가능한 인지 후보 U | A07 | 05-10 초안에는 react-router 제품명/해당 거절 문단이 없고 05-28 판에 들어간다. 최종 06-18 package 의존은 joshdover의 05-10 선행 인지를 증명하지 않는다. 최초 제안 이전 검토 기록 또는 그 뒤 처음 알았다는 작성자 답글이 필요하다. [ADR-D07](https://github.com/elastic/kibana/blob/5ec0bcf18041d2e6bb6046642ee0ce654121ba09/rfcs/text/0003_application_service_mounting.md) · [ADR-R07](https://github.com/elastic/kibana/blob/b8423952c036ae302c059afe2a606bc77dceee62/rfcs/text/0004_application_service_mounting.md) · [ADR-AUX11](https://github.com/elastic/kibana/blob/b8423952c036ae302c059afe2a606bc77dceee62/package.json) |
| 당시 소개 가능한 인지 후보 U | A09 | 02-06 제안 당시 RocksDB 내장 TTL 인지는 미확인이고 05-02 초안에서는 알고 거절한다. 그 사이 최초 소개·답글이 필요하다. 06월의 직접 새 정보는 compliance 요구이며 외부 TTL 채택으로 바뀌지 않았다. [AP-M25-ORIG](https://lists.apache.org/thread/47qqn7x9pb72wjv3c668jjt9jzhfxr50) · [AP-D25](https://cwiki.apache.org/confluence/rest/api/content/80452561?expand=body.storage,history,version&status=historical&version=6) · [AP-M25-NEWNEED](https://lists.apache.org/thread/0pdkltmm3noygb8lprxxk2gpp7tt049y) |

이 U는 해법·주체·첫 공개 선택 구간을 고정한 후보 목록이다. 다른 미지 대안을 새로 상정해 U를 늘리지 않는다. A07의 발견과 설계 변화 사이 인과는 미확인이고, A09는 기존 외부 대안을 거절한 채 자체 TTL을 수정했다. 따라서 U 두 행의 인지만 완성해도 엄격 인과 양성 두 건이 되지 않는다.

## 합산하면 달라지는 판단

- **A01·A19의 2/24는 기지 해법의 제약 교정과 실행이다.** Kubernetes annotation의 타입 조건과 CommonMark 문법 제약을 늦게 이해한 뒤 실제 변경했다. 개입 가능한 정보의 예지만, 해법의 존재 자체를 몰랐다는 수와 합치지 않는다. [ADR-T01](https://github.com/backstage/backstage/pull/894) · [RUST-F03](https://github.com/rust-lang/rfcs/pull/2285) · [RUST-I2285](https://github.com/rust-lang/rust/pull/47046)
- **A04는 U에서 제외한다.** 고정 최초 초안 L62가 GCP Config Connector를 이미 명시한다. 리뷰어의 구체 스키마 추천이나 다른 유지보수자의 재평가를 원 제안자의 최초 발견으로 옮길 수 없다. [ADR-D04](https://github.com/backstage/backstage/blob/1312d34147af604355117ee85ed913e7a9460092/docs/architecture-decisions/adr005-catalog-core-entities.md) · [ADR-T04](https://github.com/backstage/backstage/pull/1072)
- **A20은 의사결정 사슬과 발견 사슬을 분리한다.** Manishearth는 Criterion 추천에 이미 검토했다고 답했다. 후속 custom framework 실행은 연결되지만 새 지식 사건 또는 Criterion 채택은 입증하지 않는다. 현재 원장의 connected_chain=false와 이 감사가 일치한다. [RUST-F04](https://github.com/rust-lang/rfcs/pull/2287) · [RUST-I2287](https://github.com/rust-lang/rust/pull/53410)
- **A21의 직접 미인지 진술은 리뷰어 LukasKalbertodt의 것이다.** 이를 제안자 Centril 또는 최종 언어팀에게 전이하지 않는다. 기존 표현을 아는 초기 초안과 나란히 남긴다. [RUST-D05](https://raw.githubusercontent.com/rust-lang/rfcs/e91e24dc42093cc2ab5b29fe0c4471645719d641/text/0000-associated-type-bounds.md) · [RUST-F05](https://github.com/rust-lang/rfcs/pull/2289)
- 실행은 20/24에서 범위를 한정해 관측했다. A04는 표적 KCC 통합, A17·A22는 미채택 뒤 실제 사용자 구현 유지, A24는 최종 구현·안정화가 미확인이다. 표준/제안 거절만으로 실제 후속 배포가 없었다고 판정하지 않는다.

## 검사와 재현

24개 고유 ID, 필수 필드, 3개 원장의 자료 ID 참조, U 목록, 분모를 기계 대조했다. 감사 실행 중 원 decisions.jsonl에 쓰기 작업을 하지 않았고 해시를 보존했다. 다른 담당자의 이후 수정은 별도 스냅샷이므로 통합 시 input_sha256과 현재 원장을 다시 비교한다. 핵심 불일치는 기존 고정 원문 3개(ADR-D04·D06·D07)를 재열람했다. 그 읽기 UTC·본문 해시는 awareness-audit-read-log.json에 있으며 새 독립 원문 수로 재산입하지 않는다.
