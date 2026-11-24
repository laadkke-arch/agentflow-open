# AF-RES-185 자체 점검

- 판정: **PARTIAL**. 자기 검토이며 독립 검토는 미실시. 원자료 읽기/정적 판독 및 저장된 원장의 구조 검증만 수행; Rust/GN 실행·빌드·링크·런타임 실측은 하지 않았다.
- 검사 대상 결과 커밋: `b0c954c1fbdf430cada2d17fd88ecdc511080723`. 아래 표는 해당 SHA의 RESULT 및 원장에 대한 점검이다.

| 질문 | 답·근거 ID/URL | 반증 탐색과 결과 | 미충족 |
|---|---|---|---|
| Q1 | R01~R15, C01 [WASM pure Rust](https://github.com/zip-rs/zip-old/issues/60), C02 [헤더 실패](https://github.com/zip-rs/zip-old/issues/113), C04 [Chromium importer](https://github.com/zip-rs/zip2/issues/344), C09 [PNG 토론](https://github.com/image-rs/image-png/issues/611). 순수 Rust·C 툴체인·안전 코드·성능 선호·한 compressor 택일은 서로 다른 조건. | C03 [native 허용 성능 요청](https://github.com/zip-rs/zip-old/issues/88); C02 clang 존재, stdlib.h 실패를 C compiler 부재로 승격하지 않음. C04의 avoid both는 PNG+ZIP AND가 아님. R10~14 합성 요청으로 구별. | PNG+ZIP 동시 필수 자연 발화, gzip 택일 자연 발화와 같은 build 연결 미확보. |
| Q2 | B01 [png 0.17.10](https://github.com/image-rs/image-png/blob/v0.17.10/Cargo.toml), B02 [png 0.18.0](https://github.com/image-rs/image-png/blob/7d4c1b0866089f2eefdae5e9b44c521d52e5d348/Cargo.toml), B03 [zip 0.6.6](https://github.com/zip-rs/zip-old/blob/21a20584bc9e05dfa4f3c5b0bc420a1389fae2c3/Cargo.toml), B04 [zip 7](https://github.com/zip-rs/zip2/blob/v7.0.0/Cargo.toml). 네 manifest 모두 flate2 선언; PNG 기본 활성, ZIP 선택적. | G17: ZIP stored-only/7 zopfli-only에서 활성 간선 없어질 수 있음. B05~08 실제 encode/decode 경로 및 버전별 옵션 확인. X03~05, X16~17 배포 비교/접근 실패 구별. | 네 자리 중 직접 태그 ref 2, 고정 출시/배포 SHA 대체 2; 배포 orig 관련 조항 비교 2/4, 2023 두 원본 미확인. 완전 블라인드 모집 아님. |
| Q3 | A01 [Cargo features](https://doc.rust-lang.org/cargo/reference/features.html), A02 [resolver](https://doc.rust-lang.org/cargo/reference/resolver.html), D04 [동일 root manifest](https://chromium.googlesource.com/chromium/src/+/d41c4d24cd81aef76cda21e4ea84ab2ddb2c71e6/third_party/rust/chromium_crates_io/Cargo.toml), D03 [lock](https://chromium.googlesource.com/chromium/src/+/d41c4d24cd81aef76cda21e4ea84ab2ddb2c71e6/third_party/rust/chromium_crates_io/Cargo.lock). G18 실제 한 root의 png 0.18.0-rc + zip 2.6.1 → flate2 1.1.1 registry 동일 package ID; D01은 다른 SHA/버전. | resolver2 host/build/dev/inactive target 분리; 동일 lock만으로 unit 활성 추정 금지. D02 GN의 ZIP 설정과 D01을 같은 SHA로 합치지 않음. | 실제 GN target+명령+unit별 cfg/host 분리 로그 미확인. |
| Q4 | A03~A06/A08~A10 [flate2 1.1.5 선택부](https://github.com/rust-lang/flate2-rs/blob/1.1.5/src/ffi/c.rs#L455-L483), A11~12 [libz-rs-sys source](https://github.com/trifectatechfoundation/zlib-rs/blob/v0.5.1/libz-rs-sys/src/lib.rs), B05~08. any_zlib/C 경로와 Rust 구현 zlib-rs 분리, 여러 feature 존재와 선택/호출 분리. | zlib-ng가 zlib-rs보다 우선; 비선택 C 의존도 build 가능. rust-allocator+c-allocator 동시 요청 compile_error(합성 반례), unsafe Rust는 순수 Rust 구현과 다른 술어. PNG fdeflate/miniz 경로가 별도로 있음. | 실효 cfg·링크·호출/전체 native 부재 미실측. |
| Q5 | C04~06 [zip 단독 기능 실패](https://github.com/zip-rs/zip2/issues/344), [수정 commit](https://github.com/zip-rs/zip2/commit/6242a005f3c9abd60dda3bf9e5f929e26d93b2de); D02~04 G18 실제 [Chromium import commit](https://chromium.googlesource.com/chromium/src/+/d41c4d24cd81aef76cda21e4ea84ab2ddb2c71e6). 단독 실패/수정판 compile 보고와 root+lock은 확인됨. | C02 WASM 실패/회피책은 다른 작성자·다른 조건. [CL6496030](https://chromium-review.googlesource.com/c/chromium/src/+/6496030) 실제 job 로그 접근 불가, GN 파일 조회 실패/429. G11~17 정적 예측을 실제 공동 관측으로 산입하지 않음. | 동일 target/명령의 공동 성공 1건 및 실제 정확판 공동 실패/거절 1건 요건 미달. compile/run/native 증거 각각 미확인. |
| Q6 | E01 [NARA format tables](https://www.archives.gov/records-mgmt/policy/transfer-guidance-tables.html), E02 [metadata](https://www.archives.gov/records-mgmt/bulletins/2015/2015-04.html), E03/E08/E09 [AAD 실제 사례](https://www.archives.gov/publications/prologue/2006/spring/aad-ww2.html). E04 [철도 split](https://www.nationalrail.co.uk/tickets-railcards-and-offers/buying-a-ticket/split-train-tickets/), E05 [Ombudsman minutes](https://media.railombudsman.org/Passenger_Advisory_Panel_July2024_Minutes_compressed_cc02058aa2.pdf) p4, E06~07. 각각 허용된 포맷/표가 결합 시 공통 metadata·relation 또는 동일 여정·정차/시간 조건 필요. | AAD 처리 실제 사례≠두 지정 포맷 공동 반려; wrong-train 중재 실제 사례≠두 개별 유효 승차권 공동 거부 확정; E06 split 대안 가정; E07 개별 사건 수 미확인. | 개별 승인+공동 거절을 동일 사건에서 모두 입증하는 원자료 미확보. |
| Q7 | N01~N12, R01~R15, G01~G18 및 위 출처. 택일 단독·동시 조건부 조합·금지 보류/거절·선호 trade-off. | 개별 ZIP 단독 성공을 PNG+ZIP 성공으로 합산하지 않음; Z25 deflate-flate2는 backend 중립; zlib-rs도 무조건 safe/native-free가 아님. 질문에 target·scope·검사 필요. | 자연 AND 요청+같은 정확판 성공을 연결할 증거 부족. 답변 규칙은 가설/조건부, 최종 제품 선택 아님. |

## 분모 및 증거 성격

| 유형 | 최소 | 산입 | 자가 판독 결론 |
|---|---:|---:|---|
| A Cargo/flate2 규칙·선택 구현 | 4 | 11 | 기능 합산 규칙·고정 구현 판독; 동일 blob A09 제외 |
| B 소비자 manifest/선언/원 코드 | 6 | 8 | 네 판 manifest와 호출/옵션 원 코드 |
| C 원 요청·수정/출시 논의 | 4 | 9 | 요구의 actor·논리와 한계 확인 |
| D 실제 하류 그래프·CI·산출 | 4 | 4 | 숫자만 충족: Chromium 두 SHA의 root/lock/patch 문서. 실제 CI/산출물 관측 부족으로 실질 기준 미달 |
| E 보존·철도 규정 및 사례 | 4 | 9 | 규정과 사용/분쟁의 실제 보고 분리. 엄격한 개별 승인/공동 반려 미확인 |
| 합계 | 22 | 41 | PARTIAL |

- 59행(41 산입+18 제외/보조); 산입 URL 41 고유, source_id 59 고유, lineage 30, event_id 25(규칙/릴리스 등 포함; 실제 사건 수와 다름). 구체적 case family 9: wasm-2018, wasm-2019, chromium-import, zopfli-only, feature-fail, chromium-lock, split-case, fare-case, archive-aad. 각 family는 독립 실험 횟수가 아니다. E07 집계된 개별 사건 수 미확인. 실제 하류 동일 package ID 관측은 Chromium 두 SHA(한 프로젝트/계보); 동일 root manifest+lock+patch 관측 G18 1건. 동일 target의 양쪽 실행 성공 직접 확인 0건(현실에 존재하지 않는다는 뜻 아님). 독립 재현 관측 0건(미실행); 원 제보/후속 제보는 재현과 별도.
- frame 21행(4 예정판 모두 설명, 2 직접 태그 ref+2 출시/배포 SHA 대체; 날짜/안정판 기준). 하류 후보 3개 중 Chromium만 고정 원 graph 판독; 나머지 repro/fork는 고정 근거 부족. 검색으로 나온 이름을 합성해 하류 모집하지 않음. 2023 prerelease 제외 행은 안정판 선정에만 사용; 모든 prerelease 태그 전수 확인 아님.
- requirements 15행, graphs 18행, answers 12행. RESULT 앞 3표 데이터 행 8/11/10, 마지막 약점 표 정확히 3행. 4자리·공동 보류·반례·조건부 응답 포함.

## 저장본 구조 검증

GitHub connector로 b0c954c1 SHA의 7개 파일을 다시 읽고 JS로 JSONL 59행 전체 parse 및 필수 값 비어 있음 0, source_id 중복 0, 산입 URL 중복 0, CSV 열 수 각각 7/9/14/12 일정, source_id 참조 누락 0, answers의 requirement_id/graph_id 참조 누락 0을 확인했다(문자열에 명시된 ID 검사이며 의미·구간 범위 독립 검토가 아님). RESULT 첫 3표 헤더와 마지막 약점 표 확인. base 6fa673283 대비 14 commits ahead, 0 behind, 바뀐 7개 파일은 모두 owned_path 내부; dot-control.json 변경 없음. scope에 기록된 control 원장 전체 읽기 제한/patch 대체 확인은 남아 있다. 외부 실행은 미실시. HANDOFF의 재현 설계는 실행 성공 보증이 아니다.

보정: Q3의 D03/D04 인용 표기를 원장과 대조하여 수정(D03 lock, D04 manifest); 판단은 동일하다.
