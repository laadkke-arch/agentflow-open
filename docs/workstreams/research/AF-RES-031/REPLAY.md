# AF-RES-031 재현

실측은 Debian 13.6 x86-64, CPython 3.12.14, Temurin JDK 21.0.10+7, Maven 3.9.11, CMake 3.31.6, Rust 1.49.0 조합이다. Rust 의존 해석과 vendor에만 Cargo 1.85.1을 썼다. 잠금 파일은 evidence/locks, 원 배포 주소와 검증된 해시는 artifacts.csv에 있다. 빈 실행 디렉터리에서 고정 입력을 생성한다. 2 GiB 시험은 cgroup v2에서 관측 당시 여유 5 GiB 이상을 요구하고 Java allocator 상한은 3 GiB다.

## GitHub의 결과·입력 확인

```sh
git clone --single-branch --branch work/research-af-res-031 https://github.com/laadkke-arch/agentflow-open.git
cd agentflow-open
git fetch origin \
  refs/heads/chore/workspace-foundation:refs/remotes/origin/chore/workspace-foundation \
  refs/heads/work/research-af-res-025:refs/remotes/origin/work/research-af-res-025 \
  refs/heads/work/research-af-res-028:refs/remotes/origin/work/research-af-res-028
p="$PWD/docs/workstreams/research/AF-RES-031"
python -B "$p/verify.py"
python -B -m workbench.session check "$p/manifest.json" --fetch
```

재생용 입력을 GitHub 브랜치 SHA e969b2f9c33eeaf07a1fdb672bb88a22aba59c5b에서 새 clone으로 읽었다. 같은 하네스의 지시자는 후속 replay.sh로 저장했다. Python과 Java 스트림, Jupyter의 real sockets는 새 폴더에서 생성했다. JUnit 버전이 같은 standalone launcher로 원본 메서드를 새 작업 디렉터리에서 2개 실행했다. Rust는 최초에 사용한 정확한 libtest 실행 파일 3개를 빈 디렉터리에서 실행했다. 패키지, JDK/JNI, Java classpath, Rust 바이너리는 재사용했다. 차가운 캐시를 다시 다운로드·빌드하는 실행은 미실시다. 로컬 절대 경로, 시각, 수신 ID, RSS와 원 로그 해시는 실행별로 다를 수 있다.

## 캐시가 있는 재생

```sh
cache=/tmp/af31
fresh=$(mktemp -d)
bash "$p/replay.sh" "$cache" "$fresh/checked"
```

replay.sh의 주 출력은 raw stdout/stderr 및 실행 명령과 SHA를 가진 JSON이다. 새 실행을 보존된 영수증에 덮어쓰지 않는다. 최초·정규화 재생 비교는 evidence/replay-comparison.json과 comparison.csv에 있다. 위 스크립트가 찾는 레이아웃은 다음과 같다.

## 새 캐시 준비

### Python wheel·고정 소스

```sh
cache=$(mktemp -d)
mkdir -p "$cache"/{venv,source,setup,tools,cache}
for env in py20 py21 ipyk26 ipyk27; do
  wheelhouse="$cache/setup/$env"
  mkdir -p "$wheelhouse"
  python -m venv "$cache/venv/$env"
  vpy="$cache/venv/$env/bin/python"
  "$vpy" -m pip download --index-url https://pypi.org/simple --only-binary=:all: \
    --require-hashes -r "$p/evidence/locks/$env.txt" --dest "$wheelhouse"
  "$vpy" -m pip install --no-index --find-links "$wheelhouse" \
    --require-hashes -r "$p/evidence/locks/$env.txt"
done

fetch_source() {
  git init -q "$cache/source/$1"
  git -C "$cache/source/$1" fetch --no-tags --depth 1 "https://github.com/$2.git" "$3"
  git -C "$cache/source/$1" checkout --detach FETCH_HEAD
  test "$(git -C "$cache/source/$1" rev-parse HEAD)" = "$3"
}
fetch_source arrow-java apache/arrow-java 7a581880a85358315d05da08296cf570b3643924
fetch_source arrow-2021 apache/arrow 4b7cdcb9220b6d94b251aef32c21ef9b4097ecfa
```

PyArrow는 휠을 사용했고 source tag는 API와 라이브러리 판의 공급자 식별이다. Jupyter v6.27.0 휠은 명시 고정 시 설치 가능하며 %edit 문제로 yanked다. 잠금 조합은 조사 시점에 해결된 실제 의존 내역이다.

### Java 네이티브·JUnit

artifacts.csv의 java 도구 행에서 JDK tar, Maven tar, CMake wheel, JUnit standalone jar를 받고 해당 SHA-256을 확인한다. 저장 폴더는 cache/setup/java다. Maven의 upstream SHA-512와 JDK upstream SHA-256 사본은 receipts/acquisition에 있다. 공용 네트워크에서 직접 DNS가 가능하면 Maven 기본 설정을 쓴다. 관리형 프록시에서 최초 DNS 실패가 재현되면 상속 HTTPS_PROXY의 host와 port를 Maven Settings의 활성 http proxy에 쓰고 평소 신뢰하는 JVM CA 경로를 지정한다. JVM 프로세스용 user.home는 임시 쓰기 가능 경로로 지정한다.

```sh
mkdir -p "$cache/setup/java/maven-home" "$cache/tools/jdk"
tar -xzf "$cache/setup/java/OpenJDK21U-jdk_x64_linux_hotspot_21.0.10_7.tar.gz" \
  --strip-components=1 -C "$cache/tools/jdk"
tar -xzf "$cache/setup/java/apache-maven-3.9.11-bin.tar.gz" -C "$cache/tools"
python -m venv "$cache/venv/cmake"
"$cache/venv/cmake/bin/python" -m pip install \
  "$cache"/setup/java/cmake-3.31.6-*.whl
java_src="$cache/source/arrow-java"
cmake="$cache/venv/cmake/bin/cmake"
native="$cache/java-dist/lib/arrow_cdata_jni/x86_64"
export JAVA_HOME="$cache/tools/jdk"
export PATH="$JAVA_HOME/bin:$PATH"
export MAVEN_OPTS="-Duser.home=$cache/setup/java/maven-home"
"$cmake" -S "$java_src" -B "$cache/native" \
  -DARROW_JAVA_JNI_ENABLE_C=ON -DARROW_JAVA_JNI_ENABLE_DEFAULT=OFF \
  -DBUILD_TESTING=OFF -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$cache/java-dist"
"$cmake" --build "$cache/native" --target install --config Release --parallel 2
"$cache/tools/apache-maven-3.9.11/bin/mvn" -f "$java_src/pom.xml" \
  -B -ntp -Dmaven.repo.local="$cache/m2" -Parrow-c-data -pl c -am \
  -Darrow.c.jni.dist.dir="$cache/java-dist" -Darrow.cdata.library.path="$native" \
  -Dspotless.skip=true -Ddevelocity.enabled=false -Ddevelocity.buildScan.publish=NEVER \
  '-Dtest=RoundtripTest#testLargeVarBinaryVector+testLargeListVector' \
  -Dsurefire.failIfNoSpecifiedTests=false test
python -B - "$java_src/c/target/surefire-reports/TEST-org.apache.arrow.c.RoundtripTest.xml" \
  "$cache/setup/java/java.cp" <<'PY'
from pathlib import Path
from xml.etree import ElementTree as ET
import sys

root = ET.parse(sys.argv[1]).getroot()
assert (root.get("tests"), root.get("errors"), root.get("failures"), root.get("skipped")) == ("2", "0", "0", "0")
assert {r.get("name") for r in root.findall("testcase")} == {"testLargeListVector", "testLargeVarBinaryVector"}
props = {r.get("name"): r.get("value") for r in root.findall("properties/property")}
Path(sys.argv[2]).write_text((props.get("surefire.test.class.path") or props["java.class.path"]) + "\n")
PY
(cd "$cache/m2" && sha256sum -c "$p/evidence/locks/java-runtime-maven-sha256.txt")
```

첫 failure는 c profile 없는 reactor, extension의 쓰기 불가 홈, JNI 파일 검색 경로에서 각각 확인했다. 다시 원본 export 오류를 보려면 같은 라이브러리와 원 시험에서 arrow.cdata.library.path만 빼고 원래 CMake dist 리소스 구조를 유지한다. 실제 테스트 2개와 메시지는 java-upstream.failure.surefire.txt에 있다. C Data 교량은 재생 스크립트가 동일 PID를 확인하고 JNI 포인터를 전달한다. 목적으로 제한된 작은 IPC 전달은 Java 독립 프로세스다.

### Rust 잠금과 빌드

artifacts.csv의 rustup-init 해시를 확인한 설치자를 cache/setup/rust에 둔다. 공식 DataFusion 3.0.0 crate의 Cargo.lock은 복구 seed였고, 실제 실행 lock은 evidence의 파일이다. SHA를 고정한 Rust checkout을 컴파일러 1.49.0로 사용한다.

```sh
rust_src="$cache/source/arrow-2021"
mkdir -p "$rust_src/rust/.cargo"
export RUSTUP_HOME="$cache/tools/rustup" CARGO_HOME="$cache/tools/cargo"
export CARGO_TARGET_DIR="$cache/cache/rust149" CARGO_BUILD_JOBS=2
chmod +x "$cache/setup/rust/rustup-init"
"$cache/setup/rust/rustup-init" -y --no-modify-path --profile minimal --default-toolchain 1.49.0
export PATH="$CARGO_HOME/bin:$PATH"
rustup toolchain install 1.85.1 --profile minimal
rustup component add rustfmt --toolchain 1.49.0
cp "$p/evidence/locks/rust-4b7cdcb-Cargo.lock" "$rust_src/rust/Cargo.lock"
cp "$p/probes/af_res025_scalar_probe.rs" "$p/probes/scalar_boundaries.rs" "$rust_src/rust/datafusion/tests/"
(
  cd "$rust_src/rust"
  cargo +1.85.1 vendor --versioned-dirs --locked "$cache/vendor149" > .cargo/config.toml
  cargo +1.49.0 test --locked --offline -p datafusion --test af_res025_scalar_probe \
    common_accessor_boolean_utf8_list -- --exact --nocapture
  cargo +1.49.0 test --locked --offline -p datafusion --test scalar_boundaries -- --nocapture --test-threads=1
  cargo +1.49.0 test --locked --offline -p datafusion --lib \
    scalar::tests::scalar_list_ -- --nocapture --test-threads=1
)
```

최초 실패를 재현하려면 동일 source SHA의 별도 checkout에 025 시험 파일만 복사한 후 1.85.1로 cargo test -p datafusion --test af_res025_scalar_probe common_accessor_boolean_utf8_list -- --exact --nocapture를 실행한다. lock 없는 조회는 ahash ^0.6 선택 단계의 101을 확인했다. 라이브 레지스트리는 이후 달라질 수 있다. 필수 source 파일의 hash와 generated Flight diff는 receipts/rust-setup에 있다.

## 보조 판·미확인 항목 재개

- **6.27.1 보조 재생**은 ipyk271 wheel lock을 위 환경 생성과 동일하게 설치한 뒤, jupyter_wire.py의 문자열 6.27.0을 6.27.1로 치환한 임시 복사본에 --version 6.27.1 --fixture "$p/probes/inputs.json"을 전달한다. 각 실행의 별도 cwd, IPYTHONDIR 및 JUPYTER_RUNTIME_DIR를 사용한다. 원판의 잘못된 v1 판정은 847df80713786ad260789c46e5474a6002ddb41c의 probe를 git show로 꺼내 6.26.0과 같은 입력으로 실행하면 검산할 수 있다.
- **2021 Arrow 원문 직접 재독**은 Apache mailing archive HTTP 접근이 가능한 곳에서 025의 restore_inputs.py Q01 Q02와 이 작업의 source-attempts.jsonl을 연다. 처음 두 raw Message-ID의 본문 SHA-256 일치, 제안과 수락 메일의 각각 독립 Message-ID 확인이 첫 행동이다. tracker의 재현은 최초 메일을 대신하지 않는다.
- **대형 Parquet 또는 IPC**는 작은 두 스트림과 C Data 고주소의 범위 밖이다. 같은 PyArrow와 Java에서 길이 2,147,487,744의 채워진 Binary payload와 4바이트 tail을 가진 단일 논리 청크를 고정하고, 예산을 잰 뒤 생성·Parquet read·IPC write·Java tail read를 별도 영수증으로 닫는다. 파일 쓰기량·row group·압축 및 Arrow chunk 분리를 먼저 기록한다.
- **WMS 의미부터 화면까지**는 Blue Lake ZIP과 CRS:84/EPSG:4326을 모두 지원하는 로컬 서비스에서 Lakes 범위를 두 순서와 고의 바꾼 순서로 요청하고 동일한 위치의 픽셀을 확인한다. 이번 측정은 ZIP의 헤더와 CTL fixture 판독이다.

## Java 원본 논리행 반례의 별도 재생

```sh
holder_run=$(mktemp -d)
mkdir "$holder_run/classes"
java_cp=$(cat "$cache/setup/java/java.cp")
"$cache/tools/jdk/bin/javac" -cp "$java_cp" -d "$holder_run/classes" "$p/probes/JavaHolderControl.java"
(
  cd "$holder_run"
  "$cache/tools/jdk/bin/java" --add-opens=java.base/java.nio=ALL-UNNAMED \
    -Darrow.cdata.library.path="$cache/java-dist/lib/arrow_cdata_jni/x86_64" \
    -cp "$holder_run/classes:$java_cp" JavaHolderControl
)
```

두 입력은 같은 holder에 hello world와 null을 설정한다. 원 방식은 producer/ABI/consumer가 0/0/0이며 setValueCount(2)만 추가한 대조는 2/2/2다. 원본 JUnit은 별도 그대로 실행했다.
