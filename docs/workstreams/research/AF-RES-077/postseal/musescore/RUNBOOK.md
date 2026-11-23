# MuseScore v3.0.1 test handoff — not executed

The files under `source/` are evidence copies, not a complete build checkout. No MuseScore build, installation, GUI operation, original regression suite, or frozen MS-N/MS-E/MS-X test was executed in this investigation.

## Environment observed here

`runtime-availability.json` records that `cmake`, `ctest`, `xvfb-run`, `mscore` and `musescore` were absent from the command path. `pkg-config --modversion Qt5Core Qt5Widgets Qt5Test` failed; the installed `qmake` launcher could not execute `/usr/lib/qt5/bin/qmake`. GNU make, g++ and diff were available. These are environment probes, not a failed MuseScore regression run. Nothing was installed.

## Source-supported requirements

At commit `06a66a2206fc5f3c2c33d7ee4123badf496bc4dd`:

- Root `CMakeLists.txt` declares CMake 3.0.0 and Qt minimum 5.8.0. The historical Travis job supplies CMake 3.10.1, GCC/G++ 4.9 and Qt 5.9.3. Compatibility with the current g++ 14 environment has not been tested.
- `build/FindQt5.cmake` searches for Core, Gui, Network, Test, Qml, Quick, QuickWidgets, Xml, XmlPatterns, Svg, Sql, Widgets, PrintSupport, Concurrent, OpenGL, LinguistTools and Help; its non-MinGW path also searches for WebEngine modules.
- The Linux CI package list includes audio, font and compression development dependencies: ALSA, PortAudio, PortMIDI, libsndfile, zlib, FreeType, Fontconfig, LAME, PulseAudio and Mesa/EGL. Root CMake additionally checks enabled optional Vorbis/Ogg and JACK features. Use the pinned CMake and CI files as the dependency authority for the chosen platform.
- `mtest/README.md` explicitly requires `diff` in PATH. The historical Linux runner uses `xvfb-run -a`, with `QT_QPA_PLATFORM=vnc` in the selected Travis job. Qt's VNC platform plugin and Xvfb must be available for that exact invocation.
- Root CMake adds `mtest` with `EXCLUDE_FROM_ALL` on Linux. Building the application alone does not build all tests; the separate make in `build.debug/mtest` matters.

## Original commands and bounded executable adaptation

The pinned `mtest/README.md` gives Linux commands `make debug`, `sudo make installdebug`, `cd build.debug/mtest`, `make`, then `ctest`. The selected CI job instead uses a private installation prefix, `CPUS=2`, and `xvfb-run -a ctest -j2 --output-on-failure`. The following is an **unexecuted handoff** using the existing Makefile targets with a private prefix and the five inspected suites. It does not reproduce the full CI job, which also generates visual artifacts, uploads files and performs cleanup.

Run this only in a separately provisioned build environment with the dependencies above:

```bash
MS_SOURCE="$PWD/musescore-v3.0.1-test"
git clone --branch v3.0.1 --depth 1 https://github.com/musescore/MuseScore.git "$MS_SOURCE"
cd "$MS_SOURCE"
test "$(git rev-parse HEAD)" = "06a66a2206fc5f3c2c33d7ee4123badf496bc4dd"

MS_PREFIX="$MS_SOURCE/local-install"
make revision
make debug CPUS=2 PREFIX="$MS_PREFIX" DOWNLOAD_SOUNDFONT=OFF
make installdebug CPUS=2 PREFIX="$MS_PREFIX" UPDATE_CACHE=FALSE DOWNLOAD_SOUNDFONT=OFF
make -C build.debug/mtest -j2

cd build.debug/mtest
QT_QPA_PLATFORM=vnc xvfb-run -a ctest -j2 --output-on-failure \
  -R '^(tst_parts|tst_links|tst_exchangevoices|tst_readwriteundoreset|tst_element)$'
```

The Makefile supports `PREFIX`, `DOWNLOAD_SOUNDFONT` and `UPDATE_CACHE`; turning off the soundfont download and system cache update is a handoff adaptation. The private-prefix install command above is supplied for a later operator and was not run here. No modern dependency package installation command is guessed.

To run only the original part suite from `build.debug/mtest`, use the same runner with `ctest --output-on-failure -R '^tst_parts$'`. `mtest/cmake.inc` registers each test executable with `-xunitxml -o result.xml`; capture those XML files, CTest output and the command exit code as execution receipts. Retain the exact source SHA, any applied changes and build configuration with the logs. A generated `result.xml` must be inspected before claiming a pass.

## Remaining work for the frozen cases

The three common cases are specifications. They are not existing test entry points, so the commands above do not execute MS-N, MS-E or MS-X. An implementation harness still needs concrete valid score fixtures, a mapping from `m1`/`u1` to real score objects, a proper pitch command with tonal-pitch-class handling, exact assertion checkpoints, and an explicit save/read cycle.

MS-E particularly needs its selected-flag/selection-list observation immediately after part creation. A final-only check after reopening can lose the transient state that distinguishes the reported defect. Existing XML reference comparisons are useful preservation checks but do not capture in-memory selection or object identity. No result for any of MS-N/MS-E/MS-X is available: **0 of 3 executed; pass and fail counts unknown**.
