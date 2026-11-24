#!/usr/bin/env bash
set -euo pipefail
cd /tmp/af-res-240-evidence
sha=6903dde39ed637adaafc352c4b6993739253f058
cat tzbuild/ref.stdout
sha256sum sources/T05-archive
tar -xf sources/T05-archive
cd "tz-$sha"
sed -n '3p' NEWS
cmp backward ../sources/T01-archive
zic --version
zic -b fat -d ../tzbuild/with-backward africa antarctica asia australasia europe northamerica southamerica etcetera backward
zic -b fat -d ../tzbuild/no-backward africa antarctica asia australasia europe northamerica southamerica etcetera
cd ../tzbuild
stat -c '%i %h %n' with-backward/US/Eastern with-backward/America/New_York \
    with-backward/Asia/Calcutta with-backward/Asia/Kolkata
sha256sum with-backward/US/Eastern with-backward/America/New_York \
    with-backward/Asia/Calcutta with-backward/Asia/Kolkata
test ! -e no-backward/US/Eastern && test ! -e no-backward/Asia/Calcutta
printf '%s\n' 'Both Link names are absent in the no-backward output tree.'
