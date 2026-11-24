# Public original contract: Syncthing #9313 / #9314

## Source and scope
Original asker KeyWeeUsr pinned revision 86a08eb87df2aa6cf1ab631120a0b918617a98b3 in https://github.com/syncthing/syncthing/issues/9313 (2024-01-01). This is a real original **public producer test fixture**, not the asker's private device identifier. Source files read directly through GitHub; the four Go files copied locally and verified against the Git blob hashes before execution. JS functions and HTML expression manually transcribed from directly read source, then patched according to the actual merged diff U1; not a full browser, network API, Syncthing build or user deployment. No original R3 PDF was attached in the visible question/answers; do not relabel generated OCR input as the user's original.

| source at pinned revision | Git blob SHA |
|---|---|
| [lib/protocol/deviceid.go](https://github.com/syncthing/syncthing/blob/86a08eb87df2aa6cf1ab631120a0b918617a98b3/lib/protocol/deviceid.go) | fee2f6d65e1c3c482db11228ef5ee7655e940708 |
| [lib/protocol/deviceid_test.go](https://github.com/syncthing/syncthing/blob/86a08eb87df2aa6cf1ab631120a0b918617a98b3/lib/protocol/deviceid_test.go) | 90fa3e000ec86ad852b519277e51f0bf1a1dfb05 |
| [lib/protocol/luhn.go](https://github.com/syncthing/syncthing/blob/86a08eb87df2aa6cf1ab631120a0b918617a98b3/lib/protocol/luhn.go) | 3402765410977c241c8c4d89959462a6434cb7a3 |
| [lib/protocol/luhn_test.go](https://github.com/syncthing/syncthing/blob/86a08eb87df2aa6cf1ab631120a0b918617a98b3/lib/protocol/luhn_test.go) | c53c6adacce22de70d8084aa1744cf2a4fa27274 |
| [gui/default/syncthing/core/syncthingController.js](https://github.com/syncthing/syncthing/blob/86a08eb87df2aa6cf1ab631120a0b918617a98b3/gui/default/syncthing/core/syncthingController.js#L1450-L1505) | 32fca420e26b85441b0112e9a7989a50c8b14f64 |
| [gui/default/index.html](https://github.com/syncthing/syncthing/blob/86a08eb87df2aa6cf1ab631120a0b918617a98b3/gui/default/index.html#L905-L920) | 729e50580b7ae221d9444eff1ff185346a291ef6 |

Original test fixture: P56IOI7-MZJNU2Y-IQGDREY-DM2MGTI-MGL3BXN-PQ6W5BM-TBBZ4TJ-XZWICQ2. Actual code constants: DeviceIDLength=32, ShortIDStringLength=7, ShortID.String() base32 prefix 7, EmptyDeviceID special-case. User asks consistency between API and presentation; prior JS uses 7 for lookup, 6 for display and 5 for introducedBy fallback.

## Actual execution, 2026-11-24 UTC, Linux amd64, Go 1.23.2, Node v22.16.0
Temporary work directory /tmp/af151-retry2/public-contract (not repository checkout). Original test file retained as deviceid_original_test.txt, verified blob before modification. Harness uses a local go.mod (module github.com/syncthing/syncthing, go 1.23), stdlib crypto/sha256 shim at lib/sha256/sha256.go (only external hash import; tested paths do not call NewDeviceID), removes TestNewDeviceIDMarshalling because its generated protobuf TestOldDeviceID and TestNewDeviceID types are unavailable. All other original tests left unchanged. Additional researcher fixture test checks id.Short().String()==canonical[:7]. Command: GOPROXY=off GOTOOLCHAIN=local go test -count=1 -v . ; exit0.
```
=== RUN   TestFormatDeviceID
--- PASS: TestFormatDeviceID (0.00s)
=== RUN   TestValidateDeviceID
--- PASS: TestValidateDeviceID (0.00s)
=== RUN   TestMarshallingDeviceID
--- PASS: TestMarshallingDeviceID (0.00s)
=== RUN   TestShortIDString
--- PASS: TestShortIDString (0.00s)
=== RUN   TestDeviceIDFromBytes
--- PASS: TestDeviceIDFromBytes (0.00s)
=== RUN   TestLuhn32
--- PASS: TestLuhn32 (0.00s)
=== RUN   TestAF151PublicFixture
    public_fixture_test.go:10: canonical=P56IOI7-MZJNU2Y-IQGDREY-DM2MGTI-MGL3BXN-PQ6W5BM-TBBZ4TJ-XZWICQ2 api_short=P56IOI7 len=7
--- PASS: TestAF151PublicFixture (0.00s)
PASS
ok github.com/syncthing/syncthing 0.002s
```
Six upstream tests passed, one upstream test explicitly excluded, one additional fixture passed. Benchmarks not run. Node command `node public-ui.js`, exit0 means reproduces inconsistency:
```json
{"api_prefix":"P56IOI7","friendlyNameFromID":"P56IOI","deviceShortID":"P56IOI","introducedBy":"P56IO","friendlyNameFromShort":"P56IOI"}
```
Patch exact original source behavior according to merge commit [2abfefc](https://github.com/syncthing/syncthing/commit/2abfefc18cb3020b68a113d7099950e98709b22b): shortIDStringLength=7, use it in both old 7 and old 6 substr, replace introducedBy substring(0,5) with deviceShortID. `node public-ui-fixed.js`, exit0:
```json
{"api_prefix":"P56IOI7","friendlyNameFromID":"P56IOI7","deviceShortID":"P56IOI7","introducedBy":"P56IOI7","friendlyNameFromShort":"P56IOI7"}
```
Five displayed/check strings including the protocol prefix: all 7 chars after patch, only one before. This validates the presentation contract on the producer fixture, not actual deployment, collision behavior of all IDs, or user's own device. The original user authored merged [PR #9314](https://github.com/syncthing/syncthing/pull/9314) (created 2024-01-02T03:11:17Z, merged 2024-01-02T16:31:58Z, 6 files +12/-6). The source fix is distinct from the previously compared Git and Kubernetes analogs, not a replacement member or a new strict reversal.

## Execution provenance
SHA256 of actual local input/derived files and logs (transcribed from shell output; this Markdown is not the raw log):
- deviceid.go e26c0cdd4bdbeb546b7cde088121692a743fb17243f5e5d3e27d1bd9f2113610
- deviceid_original_test.txt 668796342bf4d3c64f9645963bbf07b777b864a3d524cd49ca49a19d92b29286
- luhn.go 20b8b919866c2a01b68dba035b05bb9ebe8a59573519360852e71cfac6c3eaf0
- luhn_test.go 868821eda7097622f699db977b294b2da20094c13d71adb8f34e50a7684c21b0
- deviceid_test.go c8f67a1fe46f5c243410923a51cb0809cc0474aa5633c6f6317348a0993595d6
- public_fixture_test.go d1b9f27e93db084c3937cf58ddc1b4de68aff07cd83bbca48ea85bb054288f95
- public-ui.js c28d3f37a53e12d174483398a166e74e8e2e342a552c9cbb75dbec573906ce49
- public-ui-fixed.js 836e8c17e860ecbeb7549bc2b4bdd28d82c414312c111b0818bf471e483530f4
- go-test.log b08f296a1b1595d2de9ce4218012b322426e00a5219c416b3d93ed103d8264df
- node-test.log 2d8fd7e22754aa598694274b6c4bc396b0582690df5ae416e6b90e4f1bf4945c
- node-fixed.log 2acb82e6003e1085d7e0bc773bbc4a02f7b225050c31c6c177be7fa98ba3d6a3

For reproduction, fetch four pinned files, verify Git hashes, create the harness in a temporary directory; see contract-repro.sh (separate reconstructed script, not an assertion that the script itself was executed in the initial test).
