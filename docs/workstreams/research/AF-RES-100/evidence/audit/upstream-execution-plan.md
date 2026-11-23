# Pinned upstream execution plans

**Status: planning only; zero upstream tests executed.** These plans trace four counted original-test families to their pinned runners and build metadata. The supplemental source ledger contains 31 read records, all with `count_minimum=false`; they do not increase the study's minimum-source count.

The current runtime facts were supplied by the coordinating agent: jq 1.7, Pandoc 3.1.11.1, and no Rscript or cabal. No program-version probes, builds, dependency installs or tests were run for this plan. GNU sed 4.9 build/runtime parity was not established here.

## Preparation and fixed archive identities

Run the preparation commands from the AgentFlow repository root. Subsequent commands are prospective and must run in separate writable upstream trees.

```sh
AF100_REPO="$(git rev-parse --show-toplevel)"
AF100_CACHE="$AF100_REPO/docs/workstreams/research/AF-RES-100/evidence/_cache/corpora"
AF100_WORK="$(mktemp -d "$AF100_REPO/docs/workstreams/research/AF-RES-100/evidence/_cache/upstream-run.XXXXXX")"
```

- Before extraction, compare each archive's SHA-256 with the fixed values below. Archive recompression/hash drift is not silently accepted.
- Use complete archives or pinned checkouts in separate writable temporary trees; do not build or run tests in evidence/_cache/corpora.
- The registered-file cache alone omits build inputs and auxiliary fixtures; keep upstream directory layouts and original test bodies.
- External R/Haskell dependency resolution needs a recorded lock/plan before claiming repeatable runtime parity.

| Archive | SHA-256 |
|---|---|
| JQ | `3b0b7adbd7a7aa082716ba6dbeb23e11bf29fe8de58ed648402b86a30e79f664` |
| PD | `0c10acd68912abc5a2a6c985936c057f1e3886b0aa5d67699922fed77a9d09bf` |
| SED | `6e226b732e1cd739464ad6862bd1a1aba42d7982922da7a53519631d24975181` |
| KN | `9c0ea5945ed3252916b2b0c5e1e7d8329753783b5eb3e60db0f018c6d9d65859` |

The archive hashes identify the preserved original compressed bytes. The earlier offline verification is recorded in `cache-restore-check.json`; this planning task did not download or extract build trees. Complete source archives contain inputs omitted by the registered text-file cache.

## jq 1.7.1 — tests/jq.test

Registered fixture: `JQ-0080`; SHA-256 `35aade216e95e78e63e77011fb4588856a5d04d6ac7be572ad382a3430d8b4d5`. Pinned commit: `71c2ab509a8628dbbad4bc7b3f98a64aa90d3297`.

**Working directory:** Root of a separate full checkout at the pinned jq commit, with no spaces in the path because the original driver leaves some path variables unquoted.

### Acquire the complete pinned source

```sh
git clone https://github.com/jqlang/jq.git "$AF100_WORK/jq-1.7.1"
cd "$AF100_WORK/jq-1.7.1"
git checkout --detach 71c2ab509a8628dbbad4bc7b3f98a64aa90d3297
git submodule update --init
```

### Build

```sh
autoreconf -i
./configure --with-oniguruma=builtin
make -j2
```

### Run the original harness

```sh
NO_VALGRIND=1 JQ="$PWD/jq" sh ./tests/jqtest
```

The source also registers this Automake alternative:

```sh
make check TESTS=tests/jqtest NO_VALGRIND=1
```

### Inputs and dependency requirements

- Entire unchanged tests/jq.test (40,026 bytes): original jq programs, JSON inputs and expected results.
- tests/jqtest, tests/setup, complete tests/modules tree and the executable built from this checkout.
- Oniguruma at the submodule gitlink of the pinned checkout. tests/onig.supp and tests/local.supp are also used when Valgrind is enabled.

- C compiler/linker, POSIX shell, make, libtool, automake and autoconf.
- Git and the pinned Oniguruma submodule for the documented bundled-library build.
- Flex/Bison are relevant when regenerating lexer/parser sources; configure checks Bison >=3.0 in the applicable maintainer-mode path. The frozen archive already contains generated lexer/parser C.
- NO_VALGRIND=1 deliberately selects the upstream-supported mode without optional memory checking.

### Source trace

- [UP-JQ-README](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/README.md), `README.md`, lines 20–46: Upstream build tools and commands.
- [UP-JQ-RUNNER](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/tests/jqtest), `tests/jqtest`, lines 1–5: Exact driver: setup, modules path and --run-tests.
- [UP-JQ-SETUP](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/tests/setup), `tests/setup`, lines 9–27: Binary selection and optional Valgrind.
- [UP-JQ-MAKE](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/Makefile.am), `Makefile.am`, lines 136–148: Official test registration and build-tree JQ environment.
- [UP-JQ-GITMODULES](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/.gitmodules), `.gitmodules`, lines 1–3: Submodule origin.

### Current gaps and required execution evidence

- Coordinator supplied installed jq 1.7; this is not pinned jq 1.7.1.
- No pinned build or original fixture execution occurred.
- Read-only archive member inspection found no top-level configure or modules/oniguruma/configure.ac. The cached GitHub archive alone is not the complete documented bundled-Oniguruma git build; use the checkout/submodule sequence.

- Record checkout and submodule SHAs, compiler/configuration, built jq version, original fixture hash, exact command, stdout/stderr and exit.
- Require successful completion of the unchanged complete fixture; retain failures. This does not verify the original user's incomplete JOIN inputs.

### Limits

- The command executes the full jq.test fixture; individual cases do not become new independent evidence sources.
- Optional Valgrind checks are disabled by the stated command.
- All commands are plans, not observed executions.

## GNU sed 4.9 — testsuite/bsd.sh

Registered fixture: `SED-0022`; SHA-256 `4633edc7078cc121aacb85dd4f9914f04bc174a52be78f55b289b408c7c1bb91`.

**Working directory:** Root of a separate full extraction of the preserved sed-4.9 release archive.

### Acquire the complete pinned source

```sh
mkdir "$AF100_WORK/sed-4.9"
tar -xJf "$AF100_CACHE/SED/source.tar" -C "$AF100_WORK/sed-4.9" --strip-components=1
cd "$AF100_WORK/sed-4.9"
```

### Build

```sh
./configure
make -j2
```

### Run the original harness

```sh
make check-TESTS TESTS=testsuite/bsd-wrapper.sh
```

### Inputs and dependency requirements

- Complete release source and generated build files, not just the selected text-cache subset.
- testsuite/bsd-wrapper.sh, bsd.sh, bsd.good, init.sh, envvar-check and project init.cfg when present.
- Built sed/sed, generated configuration and the check_PROGRAMS required by check-TESTS.
- bsd.sh generates lines1/lines2/etc. and sed.out. The expected-output oracle bsd.good has SHA-256 2c1028e0e605b9b9807517ac31c9f5fb12db38ae987a8e5b3c9ae2d8b6f17678.

- C compiler/linker, make, POSIX shell, and the ordinary build/harness command-line utilities.
- GNU tar with xz support for the extraction command. The release archive supplies configure; no git bootstrap is proposed.
- The local check-TESTS target builds its declared helper programs. The harness supplies LC_ALL=C, source/build directories and PATH containing the built sed.

### Source trace

- [UP-SED-INSTALL](https://ftp.gnu.org/gnu/sed/sed-4.9.tar.xz), `INSTALL`, lines 50–61: Release configure/make workflow.
- [UP-SED-GENERATED-MAKE](https://ftp.gnu.org/gnu/sed/sed-4.9.tar.xz), `Makefile.in`, lines 5456–5460: Verified local check-TESTS target and check_PROGRAMS prerequisite.
- [UP-SED-GENERATED-MAKE](https://ftp.gnu.org/gnu/sed/sed-4.9.tar.xz), `Makefile.in`, lines 5704–5708: Local versus recursive check.
- [UP-SED-LOCAL](https://ftp.gnu.org/gnu/sed/sed-4.9.tar.xz), `testsuite/local.mk`, lines 99–119: Registered wrapper entrypoint.
- [UP-SED-LOCAL](https://ftp.gnu.org/gnu/sed/sed-4.9.tar.xz), `testsuite/local.mk`, lines 123–177: Helpers and test environment.
- [UP-SED-WRAPPER](https://ftp.gnu.org/gnu/sed/sed-4.9.tar.xz), `testsuite/bsd-wrapper.sh`, lines 19–31: Execute bsd.sh, normalize CRs, compare bsd.good and propagate failure.
- [UP-SED-BSD](https://ftp.gnu.org/gnu/sed/sed-4.9.tar.xz), `testsuite/bsd.sh`, lines 49–69: Generated inputs and executable/output paths.

### Current gaps and required execution evidence

- This task has no recorded matching built sed 4.9 tree or wrapper result; the coordinator supplied no sed-version observation.
- Running an arbitrary host sed or bsd.sh alone would not establish the official wrapper's golden comparison. No original test was executed.

- Record archive hash, compiler/platform/configure settings, built sed version, bsd.sh and bsd.good hashes, and the exact harness command.
- Preserve testsuite/bsd-wrapper.log/.trs, test-suite.log and exit status. Distinguish PASS/FAIL/ERROR/SKIP; skip is not pass.

### Limits

- check-TESTS is verified in the pinned generated Makefile.in; selecting this local target avoids recursively propagating the test path into other subdirectories.
- A standalone bsd.sh zero exit without bsd.good comparison is insufficient.
- This fixture does not reproduce the user's raw evtx/XML/yq pipeline.

## knitr 1.50 — tests/testit/test-plot.R

Registered fixture: `KN-0133`; SHA-256 `3694e39bb3cb4b89240d3996d9bd053ef679da2aca9bac7e13f118587224159a`. Pinned commit: `01bf7eff974903d1498e76e92a3e4b3bf9273cf5`.

**Working directory:** Root of a separate complete knitr 1.50 extraction; its parent must be writable for the source tarball and R check directory.

### Acquire the complete pinned source

```sh
mkdir "$AF100_WORK/knitr-1.50"
tar -xzf "$AF100_CACHE/KN/source.tar" -C "$AF100_WORK/knitr-1.50" --strip-components=1
cd "$AF100_WORK/knitr-1.50"
```

### Run the original harness

```sh
make travis
```

The `make travis` target expands to the following build/check sequence in the extraction's parent directory:

```sh
R CMD build --no-manual knitr-1.50
R CMD check knitr_1.50.tar.gz --no-manual
```

The original R entrypoint `tests/run-all.R` is:

```r
library(testit)
test_pkg("knitr")
```

**Selection limit:** The pinned source establishes a package-level testit runner, not a single-file selector. The exact existing make target therefore includes other package checks. No guessed testit filter argument or bare source() substitute is proposed.

### Inputs and dependency requirements

- Complete pinned package source, DESCRIPTION/NAMESPACE/R implementation, tests/run-all.R, all tests/testit inputs and vignette inputs used by R CMD build.
- Unchanged test-plot.R, which refers to internal knitr helpers and is not established as standalone in an arbitrary R session.
- Optional tests/testit/knit-tikzDevice.Rnw, SHA-256 d6022af5c3d9cbebfbcaa0fa94d45c3bf6df3ae1cebf90b5e89bd84aedfabac7.
- myfigure.pdf, img/test.png and ~/test.png are used with error=FALSE in the displayed include_graphics path tests; these tests do not prove those files exist.

- R >=3.6.0 and Rscript.
- Imports: evaluate >=0.15, highr >=0.11, xfun >=0.51, yaml >=2.1.19, methods and tools. testit is required by tests/run-all.R.
- The full package build/check also needs its applicable Suggests and litedown/knitr vignette builders. The pinned metadata specifies bounds/categories, not a full immutable dependency lock.
- Unconditional PDF/grid graphics support. A working PNG device enables PNG checks; ragg enables its guarded checks. tikzDevice, pdflatex and the stated platform/environment condition enable the TikZ fixture.
- Record actual R/dependency versions and device capabilities. Optional branches not entered must not be reported as passed.

### Source trace

- [UP-KN-RUNNER](https://github.com/yihui/knitr/blob/01bf7eff974903d1498e76e92a3e4b3bf9273cf5/tests/run-all.R), `tests/run-all.R`, lines 1–2: Exact package runner.
- [UP-KN-MAKE](https://github.com/yihui/knitr/blob/01bf7eff974903d1498e76e92a3e4b3bf9273cf5/Makefile), `Makefile`, lines 15–33: Existing build and travis check targets.
- [UP-KN-DESCRIPTION](https://github.com/yihui/knitr/blob/01bf7eff974903d1498e76e92a3e4b3bf9273cf5/DESCRIPTION), `DESCRIPTION`, lines 116–162: R, package and system requirements.
- [UP-KN-PLOTTEST](https://github.com/yihui/knitr/blob/01bf7eff974903d1498e76e92a3e4b3bf9273cf5/tests/testit/test-plot.R), `tests/testit/test-plot.R`, lines 1–86: Graphics behavior and device gates.
- [UP-KN-PLOTTEST](https://github.com/yihui/knitr/blob/01bf7eff974903d1498e76e92a3e4b3bf9273cf5/tests/testit/test-plot.R), `tests/testit/test-plot.R`, lines 132–146: Conditional TikZ input and path checks.
- [UP-KN-CI](https://github.com/yihui/knitr/blob/01bf7eff974903d1498e76e92a3e4b3bf9273cf5/.github/workflows/R-CMD-check.yaml), `.github/workflows/R-CMD-check.yaml`, lines 53–81: Upstream dependency provisioning and Suggests policy.

### Current gaps and required execution evidence

- Coordinator reports Rscript absent.
- No R version, knitr 1.50/testit installation or graphics-device capability was established or executed here.

- Record source hash, R version, sessionInfo()/dependency versions, exact build/check commands, R CMD check result and logs.
- Confirm tests/run-all.R actually ran, and distinguish conditional blocks entered from skipped branches.
- Preserve original test bodies; generic plot/path checks do not establish an SVG/EMF default-selection option.

### Limits

- The verified upstream package runner is broader than test-plot.R. A precise isolated-file command remains unverified from the available pinned knitr sources.
- Dependency versions and CI's R release aliases are not fully pinned.
- No original runtime success is claimed.

## Pandoc 3.6 — test/command/yaml-metadata-blocks.md

Registered fixture: `PD-1175`; SHA-256 `132e2020401710093aadefac1a01c781ce8d67cae9014f27ca9e874b3e3b7287`. Pinned commit: `8a72b8449ddccd84fcdffc1a09ae18c4baaca32a`.

**Working directory:** Root of a separate complete Pandoc 3.6 source extraction, preserving cabal.project and its local packages.

### Acquire the complete pinned source

```sh
mkdir "$AF100_WORK/pandoc-3.6"
tar -xzf "$AF100_CACHE/PD/source.tar" -C "$AF100_WORK/pandoc-3.6" --strip-components=1
cd "$AF100_WORK/pandoc-3.6"
```

### Build

```sh
cabal update
cabal build test-pandoc
```

### Run the original harness

```sh
cabal test test-pandoc --test-options='-p yaml-metadata-blocks.md'
```

**Component confirmation:** pandoc.cabal 780–784 explicitly declares test-suite test-pandoc, main-is test-pandoc.hs and hs-source-dirs test. INSTALL 353–356 documents -p name-pattern selection.

### Inputs and dependency requirements

- Complete source, cabal.project, pandoc.cabal, local project package metadata, src/data/test trees.
- test/test-pandoc.hs, test/Tests/Command.hs and test/Tests/Helpers.hs from this exact revision.
- All five original fenced commands, stdin blocks and native-AST expected outputs in yaml-metadata-blocks.md.
- test/command/yaml-metadata.yaml for cases 4–5, SHA-256 6ee9c4ff818ce0a3c96a6b0b73150a4a10448ec8f4223f72eba1b5110ca69e16.

- GHC and Cabal supporting cabal-version 2.4 syntax. The package lists tested GHC 8.10.7, 9.0.2, 9.2.5, 9.4.4 and 9.6.3; record the selected versions.
- The core dependency closure in pandoc.cabal 435–551 and test dependencies in 785–804, under cabal.project constraints.
- Test dependencies include tasty >=0.11 && <1.6, tasty-golden >=2.3 && <2.4, tasty-hunit >=0.9 && <0.11, tasty-quickcheck >=0.8 && <0.12 and pandoc-types >=1.23.1 && <1.24.
- cabal.project enables tests/embedded data and names pandoc-lua-engine, pandoc-server and pandoc-cli; preserve the complete local project layout.
- Shell/process support. These selected cases output native AST and do not invoke TeX, mermaid-filter or pandoc-eqnos.

The selected Markdown file contains exactly five original cases. Each command below is rewritten by the upstream command-test runner to use `test-pandoc --emulate`; input and expected output remain in the original fixture.

| Case | Embedded command | Input lines | Expected-output lines |
|---|---|---|---|
| 1 | `pandoc -s -t native` | 3–7 | 9–12 |
| 2 | `pandoc -s -t native` | 16–35 | 37–62 |
| 3 | `pandoc -s -t native` | 66–70 | 72–85 |
| 4 | `pandoc -s -t native --metadata-file command/yaml-metadata.yaml` | 89–91 | 93–104 |
| 5 | `pandoc -s -t native --metadata-file command/yaml-metadata.yaml -M title=cmdline` | empty stdin | 109–120 |

### Source trace

- [UP-PD-CABAL](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/pandoc.cabal), `pandoc.cabal`, lines 780–804: Verified suite name and bounds.
- [UP-PD-INSTALL](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/INSTALL.md), `INSTALL.md`, lines 347–368: Documented test command and selector.
- [UP-PD-PROJECT](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/cabal.project), `cabal.project`, lines 1–11: Local packages/flags/constraints.
- [UP-PD-RUNNER](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/test/test-pandoc.hs), `test/test-pandoc.hs`, lines 107–123: Run from test/ and emulate with built code.
- [UP-PD-COMMAND](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/test/Tests/Command.hs), `test/Tests/Command.hs`, lines 60–87: Command rewriting/discovery.
- [UP-PD-COMMAND](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/test/Tests/Command.hs), `test/Tests/Command.hs`, lines 101–141: Golden comparison and file-name group.
- [UP-PD-YAML](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/test/command/yaml-metadata-blocks.md), `test/command/yaml-metadata-blocks.md`, lines 1–121: Five unchanged original cases.
- [UP-PD-HELPERS](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/test/Tests/Helpers.hs), `test/Tests/Helpers.hs`, lines 86–105: Built test-binary PATH and data environment.

### Current gaps and required execution evidence

- Coordinator reports installed Pandoc 3.1.11.1, rather than pinned 3.6.
- cabal is absent; no matching GHC/Cabal build was established.
- The original runner uses built test-pandoc --emulate, not an arbitrary installed pandoc executable.

- Record source SHA, GHC/Cabal versions, resolved dependency plan/freeze, selected case names, original hashes, stdout/stderr and exit.
- Require all five golden cases to pass without --accept or any fixture update.
- Keep this result distinct from the user's Pandoc 2.18 execution, exact title-colon fix and downstream PDF/filter stages.

### Limits

- The five original cases do not contain the exact Heading1: Heading2 title or the user's filters/PDF command.
- Dependency bounds are not a historical lock; cabal update depends on an external package index.
- No original runtime success is claimed.

## Source record and display limits

Every actual runner, build file, fixture or helper source read for this plan is recorded in `upstream-plan-sources.jsonl`, with official URL/archive member, version/commit, full raw-file SHA-256, read UTC, displayed line/character/byte ranges, supported facts and limits. `upstream-execution-plan.json` contains the machine-readable plans and source IDs.

One broad Pandoc INSTALL display exceeded the output budget. That source was read again at complete explicit lines 249–373; only those later displayed lines support its cited claims. No invisible middle text is treated as inspected. Other sources are limited to the displayed sections recorded in the ledger, even when their full-file hashes were calculated.

These are proposed future commands, not receipts. Running them successfully would establish only their recorded upstream fixture outcomes under the built environment; it would not retroactively prove the original users' runtime success.
