# Rust resolver와 빌드 복구

- 고정 저장소에 Cargo.lock이 없다. Cargo 1.85.1의 동일 시험 신규 resolve는 모든 ahash 0.6.x가 yanked여서 Cargo exit 101, 입력 실행 0회였다.
- 공식 DataFusion 3.0.0 crate 내부 Cargo.lock의 ahash 0.6.3을 seed로 사용했다. 고정 checkout의 path dependencies를 현대 Cargo에서 다시 해결하고, vendor 디렉터리로 내려받았다. 첫 1.49.0은 vendor의 humantime 2.4.0 Rust 2021 edition manifest에서 중단했다.
- env_logger 0.8.2, structopt 0.3.21, termcolor 1.1.2, humantime 2.0.1로 고정하고 lock format을 4에서 3으로 바꿨다. 1.49.0로 source build가 Flight의 rustfmt 없는 단계까지 가서 다시 종료 101이었다. 고정 CI와 같은 rustfmt 컴포넌트 추가 후 컴파일을 마쳤다.
- 고정 ScalarValue·Cargo.toml에 변경이 없다. 외부 임시 checkout에서 공급자 build.rs가 dev-dependency의 생성된 Flight 파일 개행만 바꿨다. 차이와 실제 lock을 보존했다.
- 첫 테스트 실행은 025의 원본 시험 1개다. 추가 관측 2개는 같은 accessor의 배열→enum 양성·비지원 경계를 확인한다. 공급자 원 시험 2개는 그 반대인 enum→array다. 전체 workspace test가 실행된 것은 아니다. Rust의 Debug 표시와 정확한 enum PartialEq 비교를 구별한다.
