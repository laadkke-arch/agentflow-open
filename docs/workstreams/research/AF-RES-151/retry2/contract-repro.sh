#!/usr/bin/env bash
# Reconstructed portable harness of the recorded execution. Requires network for pinned downloads
# (or AF151_SOURCE_DIR containing deviceid.go, deviceid_test.go, luhn.go, luhn_test.go).
# Original execution copied verified bytes through connector, not curl.
set -euo pipefail
rev=86a08eb87df2aa6cf1ab631120a0b918617a98b3
tmp=$(mktemp -d)
echo "workdir=$tmp"
srcdir=${AF151_SOURCE_DIR:-}
cd "$tmp"
fetch() {
    if [ -n "$srcdir" ]; then
        cp "$srcdir/$1" "$1"
    else
        curl -fsSL "https://raw.githubusercontent.com/syncthing/syncthing/$rev/lib/protocol/$1" -o "$1"
    fi
    test "$(git hash-object "$1")" = "$2"
}
fetch deviceid.go fee2f6d65e1c3c482db11228ef5ee7655e940708
fetch deviceid_test.go 90fa3e000ec86ad852b519277e51f0bf1a1dfb05
fetch luhn.go 3402765410977c241c8c4d89959462a6434cb7a3
fetch luhn_test.go c53c6adacce22de70d8084aa1744cf2a4fa27274
cp deviceid_test.go deviceid_original_test.txt
python - <<'PY'
from pathlib import Path
p=Path("deviceid_test.go")
s=p.read_text()
start=s.index("func TestNewDeviceIDMarshalling(")
end=s.index("\nvar resStr string", start)
p.write_text(s[:start]+s[end+1:])
PY
mkdir -p lib/sha256
cat >go.mod <<'EOF'
module github.com/syncthing/syncthing

go 1.23
EOF
cat >lib/sha256/sha256.go <<'EOF'
// Local harness only: replace external accelerated hash dependency with stdlib.
package sha256

import "crypto/sha256"

var Sum256 = sha256.Sum256
EOF
cat >public_fixture_test.go <<'EOF'
package protocol

import "testing"

func TestAF151PublicFixture(t *testing.T) {
    id, err := DeviceIDFromString(formatted)
    if err != nil { t.Fatal(err) }
    canonical := id.String()
    short := id.Short().String()
    t.Logf("canonical=%s api_short=%s len=%d", canonical, short, len(short))
    if len(short) != 7 || short != canonical[:7] { t.Fatal("short ID contract violated") }
}
EOF
GOPROXY=off GOTOOLCHAIN=local go test -count=1 -v . | tee go-test.log
# Transcribed pinned source functions and original index.html introducedBy expression.
cat >public-ui.js <<'EOF'
const $scope={devices:{}};
$scope.friendlyNameFromShort = function (shortID) {
    var matches = Object.keys($scope.devices).filter(function (id) {
        return id.substr(0, 7) === shortID;
    });
    if (matches.length !== 1) {
        return shortID;
    }
    return $scope.friendlyNameFromID(matches[0]);
};
$scope.friendlyNameFromID = function (deviceID) {
    var match = $scope.devices[deviceID];
    if (match) {
        return $scope.deviceName(match);
    }
    return deviceID.substr(0, 6);
};
$scope.deviceName = function (deviceCfg) {
    if (typeof deviceCfg === 'undefined') {
        return "";
    }
    if (deviceCfg.name) {
        return deviceCfg.name;
    }
    return $scope.deviceShortID(deviceCfg.deviceID);
};
$scope.deviceShortID = function (deviceID) {
    if (typeof deviceID === 'undefined') {
        return "";
    }
    return deviceID.substr(0, 6);
};
const id='P56IOI7-MZJNU2Y-IQGDREY-DM2MGTI-MGL3BXN-PQ6W5BM-TBBZ4TJ-XZWICQ2';
// Expression copied from index.html; scope functions invoked in Node, not browser.
const deviceCfg={introducedBy:id};
const devices=$scope.devices;
const deviceName=$scope.deviceName;
const introducedBy=deviceName(devices[deviceCfg.introducedBy]) || deviceCfg.introducedBy.substring(0, 5);
const output={api_prefix:id.substring(0,7),friendlyNameFromID:$scope.friendlyNameFromID(id),deviceShortID:$scope.deviceShortID(id),introducedBy};
$scope.devices[id]={deviceID:id,name:''};output.friendlyNameFromShort=$scope.friendlyNameFromShort(id.substring(0,7));
console.log(JSON.stringify(output));
if(output.api_prefix.length!==7||output.friendlyNameFromID.length!==6||output.deviceShortID.length!==6||output.introducedBy.length!==5||output.friendlyNameFromShort.length!==6)process.exit(1);
EOF
node public-ui.js | tee node-test.log
# Apply semantic changes from merged 2abfefc18cb3020b68a113d7099950e98709b22b.
python - <<'PY'
from pathlib import Path
s=Path('public-ui.js').read_text().replace('const $scope={devices:{}};','const shortIDStringLength=7;\nconst $scope={devices:{}};').replace('.substr(0, 7)', '.substr(0, shortIDStringLength)').replace('.substr(0, 6)', '.substr(0, shortIDStringLength)').replace('const deviceName=$scope.deviceName;', 'const deviceName=$scope.deviceName;\nconst deviceShortID=$scope.deviceShortID;').replace('deviceCfg.introducedBy.substring(0, 5)', 'deviceShortID(deviceCfg.introducedBy)').replace('.length!==6', '.length!==7').replace('.length!==5', '.length!==7')
Path('public-ui-fixed.js').write_text(s)
PY
node public-ui-fixed.js | tee node-fixed.log
sha256sum deviceid.go deviceid_original_test.txt luhn.go luhn_test.go deviceid_test.go public_fixture_test.go public-ui.js public-ui-fixed.js go-test.log node-test.log node-fixed.log
