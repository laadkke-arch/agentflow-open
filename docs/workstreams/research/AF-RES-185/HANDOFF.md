# AF-RES-185 HANDOFF

## 판정 및 고정 결과

- worker 판정 **PARTIAL**, 독립 검토 미실시. 중앙 상태는 이 파일에서 갱신하지 않는다.
- 계획 기준 128f673685ec804c526a38e3f89d4d8a43fcd299; 작업 시작 foundation 6fa67328360b02bc7e7270d4ad3300bfe0f286bd. 선행 AF-RES-177 고정 인계 f3736d4dfaed02b5be20aac6601c0bc6c34af689. SCOPE에 차이와 조회 제약 기록.
- 작업 브랜치 work/research-af-res-185; 결과 고정 SHA **a6e7aff412155cf87305b53bc4fab71483db7d41**(자체점검 D03/D04 인용 보정까지 포함, 이 인계 커밋의 부모). RESULT 최초 완성 SHA b0c954c1fbdf430cada2d17fd88ecdc511080723. 이 파일 자체의 커밋 SHA는 GitHub branch HEAD에서 확인한다(자기 SHA를 자기 내용에 쓸 수 없음).
- 대표 파일: [RESULT.md](RESULT.md) → [SELF_CHECK.md](SELF_CHECK.md) → [sources.jsonl](sources.jsonl) → [graphs.csv](graphs.csv), [requirements.csv](requirements.csv), [answers.csv](answers.csv), [frame.csv](frame.csv), [SCOPE.md](SCOPE.md).
- 원장 59행 중 41 고유 원자료(11/8/9/4/9), 비산입 18. 4/4 manifest 자리; 태그 ref 2/4, 배포 원본 비교 2/4. 15 요청/18 그래프/12 답안. 자료 수의 하한은 충족하나 D의 CI·실제 산출 관측 및 핵심 공동 실행 기준 미충족. 구체 사건 family 9, 실제 하류 1 프로젝트 2 스냅샷, 같은 root+lock+patch 1건; 같은 target/command의 PNG+ZIP 입출력 직접 확인 0건(존재하지 않는다는 뜻 아님), 정확판 공동 거절 직접 확인 0건. 단독 실패/수정판 성공 보고를 공동 결과로 합치지 않음.
- 범위: PNG 0.17.10/0.18.0, ZIP 0.6.6/7.0.0 기능·선택부, 실제 Chromium 별도 두 판. 순수 Rust 구현은 unsafe-free 및 whole build native-free와 별개. default-features=false는 그 간선의 요청일 뿐; 같은 unit에서 다른 간선이 feature를 추가할 수 있다. zlib-rs는 C API wrapper를 거치는 Rust 구현, zlib-ng가 우선하는 판이 있음. 개별 라이브러리 링크 두 개를 합쳐 공동 성공을 주장할 수 없다.
- 미확인 핵심 3묶음(RESULT 마지막 표): (1) 동일 root target/명령/양쪽 산출물·사용자 AND, (2) 2023 배포 원본 2자리와 직접 태그 ref 2자리 및 고정 합성 검증, (3) 자연 gzip/PNG+ZIP 논리 및 두 분야 개별 승인+공동 반려 원사건. 미확인 수는 관측 단위별로 보고하며 중복 합산하지 않는다. 177의 공동 성공 공백 유지.
- 제약: GitHub connector로 큰 dot-control 원문 전체 읽기 및 Chromium 일부 GN 파일 접근 실패(429 포함). 최신 변경 patch의 task 행과 사용자 지정 선행 고정 SHA 확인, 원장 전체 독립 재확인 아님. 허용 경로 밖 미변경. 실제 Rust/GN 명령과 자체 빌드는 미실시.

## 첫 재개 행동 — 실제 하류의 target을 먼저 고정

G18의 동일 root SHA `d41c4d24cd81aef76cda21e4ea84ab2ddb2c71e6`에서 아래 자료를 다시 확인한다. 실제 하류가 Cargo가 아니라 GN으로 빌드할 수 있으므로 Cargo tree를 Chromium 실행 로그로 대체하지 않는다. 아래 명령은 Codex Cloud의 별도 scratch에서 실행하도록 전달하는 것(현재 작업에서 미실행).

```sh
set -eu
mkdir -p /tmp/af185-chromium
cd /tmp/af185-chromium
curl -fSL 'https://chromium-review.googlesource.com/changes/6496030/detail?o=ALL_REVISIONS&o=MESSAGES' -o cl6496030.json
# Gerrit XSSI prefix 제거 뒤 revision / messages / 실제 job URL/ID 조사.
git clone --filter=blob:none --no-checkout https://chromium.googlesource.com/chromium/src.git src
sha=d41c4d24cd81aef76cda21e4ea84ab2ddb2c71e6
git -C src fetch origin "$sha"
git -C src show "$sha:third_party/rust/chromium_crates_io/Cargo.toml"
git -C src show "$sha:third_party/rust/chromium_crates_io/Cargo.lock"
git -C src ls-tree -r --name-only "$sha" third_party/rust |
  grep -E '/(png|zip|flate2)/.*(BUILD\.gn|README\.chromium)$'
git -C src show --stat "$sha"
```

실제 파일 목록에서 정확한 경로를 고르고 해당 SHA의 BUILD.gn/patch를 읽는다. CL tryjob 및 buildbucket ID는 실제 응답에서만 추출. 동일 revision/target/args, GN label, toolchain, rustc --cfg feature, 실제 두 library 활성, C compiler action, 실행 산출물 로그를 연결한다. GN 소스와 툴체인이 마련된 경우에만 `gn desc out/<실제-config> <실제-label> deps --all --tree`, `gn desc out/<실제-config> <실제-label> toolchain`, `ninja -C out/<실제-config> -t commands <실제-target>` 실행. iOS 도입 의도와 실제 iOS compile은 별개; macOS/Xcode/DEPS/도구 버전이 필요하며 Linux Cloud에서 불가하면 public CI 로그만 확보한다. 같은 SHA의 두 PNG/ZIP 입력과 출력 검증을 찾아야 공동 성공 승격. 없다면 HOLD를 유지하고 실패처럼 쓰지 않는다. 5270546e53b6cf52712ff2091c6a405e61dc0873는 별개 조회(그 lock의 1.1.5와 섞지 말 것).

2023 배포 원본 복구(네 자리 모두 같은 형식으로 대조 가능):

```sh
set -eu
mkdir -p /tmp/af185-crates
cd /tmp/af185-crates
for pair in png:0.17.10 png:0.18.0 zip:0.6.6 zip:7.0.0; do
  n=${pair%:*}; v=${pair#*:}
  curl -fSL "https://static.crates.io/crates/$n/$n-$v.crate" -o "$n-$v.crate"
  sha256sum "$n-$v.crate"
  tar -xzf "$n-$v.crate"
  cat "$n-$v/Cargo.toml.orig" "$n-$v/.cargo_vcs_info.json"
done
```

실패/파일 부재를 원장에 별도 기록. 발행 archive와 Git 원본 manifest의 직접/대상별 간선, default-features, optional, version, features, vcs SHA를 비교한다. SHA가 없거나 수정된 artifact라면 동일판으로 단정하지 않는다.

## Codex Cloud 검증 설계 — 실제 하류가 아닌 G11~G17 합성 시험

아래는 실행 가능한 lock을 **생성하고 고정하는 절차**이다. 이 세션에는 실행한 Cargo.lock이 없다. 생성 성공 뒤 그 파일과 checksum을 보존하고 이후 명령에는 --locked 사용; yanked/해석 실패/추가 버전/도구 버전 충돌 발생 시 실패 로그를 남기고 임의 버전으로 대체하지 않는다. 각 case와 target은 독립한다. toolchain 1.91.1 선택은 연구자 가정(2025말 당시 사용 가능한 stable 예시; 실제 Chromium toolchain과 동일하다는 뜻 아님). 환경 설치 권한/네트워크 및 대상용 linker/runner 준비 필요. WASI probe는 wasm32-unknown-unknown 브라우저와 다른 target으로 취급. 코드를 위한 scratch만 사용, 결과 커밋은 owned_path 내부만.

```sh
set -eu
rustup toolchain install 1.91.1 --profile minimal
rustup target add --toolchain 1.91.1 x86_64-unknown-linux-gnu wasm32-wasip1 wasm32-unknown-unknown
export RUSTUP_TOOLCHAIN=1.91.1
export CARGO_RESOLVER_INCOMPATIBLE_RUST_VERSIONS=fallback
mkdir -p /tmp/af185-probes
cd /tmp/af185-probes
rustc -Vv
cargo -V
uname -a
rustup show
command -v cc || true
command -v clang || true
command -v wasmtime || true
while read -r name pv zv zf fv old; do
  mkdir -p "$name/src"
  cat >"$name/Cargo.toml" <<EOF
[package]
name = "af185-probe"
version = "0.1.0"
edition = "2021"
rust-version = "1.91.1"
[workspace]
resolver = "2"
[features]
default = [$old]
old = []
[dependencies]
png = "=$pv"
zip = { version = "=$zv", default-features = false, features = ["$zf"] }
EOF
  # src/main.rs는 아래 고정 Rust 원문을 각 case에 복사한다.
  (
    cd "$name"
    cargo generate-lockfile
    cargo update -p flate2 --precise "$fv"
    case "$name" in 25-default-deflate|25-zlibrs)
      cargo update -p libz-rs-sys --precise 0.5.1
      cargo update -p zlib-rs --precise 0.5.1
      ;;
    esac
    sha256sum Cargo.lock
    cargo fetch --locked
  ) || echo "LOCK_FAILED $name" >&2
done <<'CASES'
23-miniz 0.17.10 0.6.6 deflate 1.0.28 "old"
23-zlib 0.17.10 0.6.6 deflate-zlib 1.0.28 "old"
25-neutral 0.18.0 7.0.0 deflate-flate2 1.1.5
25-default-deflate 0.18.0 7.0.0 deflate 1.1.5
25-zlib 0.18.0 7.0.0 deflate-flate2-zlib 1.1.5
25-zlibrs 0.18.0 7.0.0 deflate-flate2-zlib-rs 1.1.5
CASES
```

중요: Cargo는 lock 생성 전에 src/main.rs 존재를 요구한다. 위 루프를 실행하기 전에 아래 원문을 `/tmp/af185-probes/main.rs`로 저장하고, 루프의 주석 위치에 `cp /tmp/af185-probes/main.rs "$name/src/main.rs"`를 삽입한다. 각 old feature default는 ["old"], 신규는 []로 해석되어야 한다. 해당판 API가 다르면 exact artifact API를 확인한 뒤 수정 사유를 기록한다.

```rust
use std::io::{Cursor, Read, Write};

fn main() {
    let pixel = [1u8, 2, 3, 255];
    let mut png_bytes = Vec::new();
    {
        let mut enc = png::Encoder::new(&mut png_bytes, 1, 1);
        enc.set_color(png::ColorType::Rgba);
        enc.set_depth(png::BitDepth::Eight);
        #[cfg(feature = "old")]
        enc.set_compression(png::Compression::Best);
        #[cfg(not(feature = "old"))]
        enc.set_deflate_compression(png::DeflateCompression::Level(6));
        let mut writer = enc.write_header().unwrap();
        writer.write_image_data(&pixel).unwrap();
        writer.finish().unwrap();
    }
    let mut buffer = Cursor::new(Vec::new());
    {
        let mut zw = zip::ZipWriter::new(&mut buffer);
        #[cfg(feature = "old")]
        let options = zip::write::FileOptions::default()
            .compression_method(zip::CompressionMethod::Deflated)
            .compression_level(Some(6));
        #[cfg(not(feature = "old"))]
        let options = zip::write::SimpleFileOptions::default()
            .compression_method(zip::CompressionMethod::Deflated)
            .compression_level(Some(6));
        zw.start_file("pixel.png", options).unwrap();
        zw.write_all(&png_bytes).unwrap();
        zw.finish().unwrap();
    }
    let mut za = zip::ZipArchive::new(Cursor::new(buffer.into_inner())).unwrap();
    let mut entry = za.by_name("pixel.png").unwrap();
    assert_eq!(entry.compression(), zip::CompressionMethod::Deflated);
    let mut recovered = Vec::new();
    entry.read_to_end(&mut recovered).unwrap();
    assert_eq!(recovered, png_bytes);
    let decoder = png::Decoder::new(Cursor::new(recovered));
    let mut reader = decoder.read_info().unwrap();
    #[cfg(feature = "old")]
    let len = reader.output_buffer_size();
    #[cfg(not(feature = "old"))]
    let len = reader.output_buffer_size().unwrap();
    let mut output = vec![0u8; len];
    let info = reader.next_frame(&mut output).unwrap();
    assert_eq!((info.width, info.height), (1, 1));
    assert_eq!(&output[..info.buffer_size()], &pixel);
    println!("AF185_ROUNDTRIP_OK");
}
```

위 코드는 양쪽 roundtrip 검증용이며 실제 backend 호출 추적을 대신하지 않는다. ZIP deflate writer 선택(Zopfli 가능)은 별도 cfg/호출 관측; 25-zlibrs는 zopfli를 요청하지 않는 대조. 두 라이브러리 단독 대조는 동일 case에서 각각 반대 dependency 및 관련 코드를 제거한 별도 root로 생성하고 lock을 새로 pin한다. PNG 단독은 동일 1x1 encode/decode; ZIP 단독은 고정 4바이트 entry write/read. 25-neutral의 ZIP 단독에는 backend를 공급하는 간선이 없는 것이 시험 조건이며 임의 flate2 직접 의존 추가 금지. stored-only와 zopfli-only는 ZIP read/write DEFLATE 공동 요구가 아닌 별도 대조. allocator 충돌 시험은 25-zlibrs 복사본에서 libz-rs-sys=0.5.1 default-features=false features=["c-allocator"] 직접 간선을 추가하고 lock 생성 후 compile_error 관측; 실제 두 소비자만으로 생긴 오류로 표기 금지.

각 성공 lock case에서:

```sh
# case 디렉터리 안에서, target마다 별도 log 및 target dir.
for t in x86_64-unknown-linux-gnu wasm32-wasip1 wasm32-unknown-unknown; do
  mkdir -p "logs/$t"
  cargo tree --locked --target "$t" -e features >"logs/$t/tree.txt" 2>&1
  cargo tree --locked --target "$t" -d >"logs/$t/duplicates.txt" 2>&1
  cargo metadata --locked --format-version 1 --filter-platform "$t" >"logs/$t/metadata.json"
  CARGO_TARGET_DIR="$PWD/check-$t" cargo check --locked --target "$t" -vv >"logs/$t/check.log" 2>&1
  echo "$?" >"logs/$t/check.exit"
  CARGO_TARGET_DIR="$PWD/build-$t" cargo build --locked --target "$t" -vv >"logs/$t/build.log" 2>&1
  echo "$?" >"logs/$t/build.exit"
done
# shell의 set -e를 해제한 별도 실행에서 각 종료코드를 저장(실패 후 다음 case 계속).
./build-x86_64-unknown-linux-gnu/x86_64-unknown-linux-gnu/debug/af185-probe
wasmtime run ./build-wasm32-wasip1/wasm32-wasip1/debug/af185-probe.wasm
```

각 check/build/run 종료코드 별도, stdout/stderr, Cargo.lock SHA256, manifest/main.rs SHA256, toolchain host/target, package ID/source와 rustc feature cfg를 보존. 위 예시는 x86_64 Linux와 WASI runner가 있을 때만 실행; bare wasm은 적합한 host runner 없이 run 승격 금지. Native source compiler 부재 검사: lock fetch 후 offline fresh target dir, 실제 환경의 compiler/linker/runner 목록 고정, `CC`, `CXX`, `HOST_CC`, `TARGET_CC`, `CC_wasm32_wasip1`, `CXX_wasm32_wasip1`, `PKG_CONFIG`를 호출을 로그에 기록하고 exit 97하는 wrapper로 설정. 가능한 경우 compiler 없는 감사된 이미지 및 execve trace(`strace -f -e execve -o exec.log cargo build --locked --offline --target wasm32-wasip1 -vv`); host build script도 포함한다. x86 native 실행은 시스템 링커를 필요로 할 수 있어 C source compilation과 linker 호출을 구별한다. dynamic `readelf -d`, static symbol/링크 map 및 build script output 조사; ldd 단독은 static C 부재를 보증 못 한다. 증명 범위는 이 case, target, 모드, compiler 관측 한정.

기대(모두 미실측 가설): 23-miniz와 25-neutral miniz, 23-zlib/25-zlib C zlib 가능→native strict 거절, 25-default-deflate/25-zlibrs zlib-rs Rust 구현 선택 가능. 다른 feature 추가/host 분리/target 불가/실제 dependency resolution 변화가 있으면 가설 수정. allocator 동시 사용은 명시적 compile_error 예상. 특정 zlib-rs 구현이 Rust여도 별도 native graph 및 unsafe-free 조건은 미확정. 성공 문자열 AF185_ROUNDTRIP_OK 및 두 assert가 성립해야 run 확인. 실제 Chromium 관측은 독립 열 유지.

## 색인 제안

AF-RES-185 — PARTIAL: Cargo feature-unification의 동일 package/unit 판별, 4개 고정 release manifest와 Chromium 동일 root+lock+patch, 41 원자료, 같은 target의 공동 성공/거절·배포 orig/자연 요구 미확인; 후속 target/action 및 고정 roundtrip 검사 필요. RESULT/graphs/SELF_CHECK/HANDOFF 링크, 제품 DB·검색 형식 확정 금지.
