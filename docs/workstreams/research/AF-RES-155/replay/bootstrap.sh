#!/usr/bin/env bash
set -euo pipefail

replay_dir=$(cd -- "$(dirname -- "$0")" && pwd)
tool_dir=$(mkdir -p -- "${1:?usage: bootstrap.sh TOOL_DIR}" && cd -- "$1" && pwd)
archive=pandoc-3.1.11-linux-amd64.tar.gz
install_dir="$tool_dir/node"

if [[ $(uname -s)/$(uname -m) != Linux/x86_64 ]]; then
    echo 'This bootstrap pins the upstream Linux x86_64 Pandoc archive.' >&2
    exit 1
fi

curl --fail --silent --show-error --location --retry 2 \
    "https://github.com/jgm/pandoc/releases/download/3.1.11/$archive" -o "$tool_dir/$archive"
(
    cd "$tool_dir"
    echo "c573fc25bc0880879bfff9a929a2a9c6834a6c5e4d7d1669fb23eddeaef37937  $archive" | sha256sum -c -
    tar -xzf "$archive" --no-same-owner pandoc-3.1.11/bin/pandoc
)
mkdir -p "$install_dir"
cp -- "$replay_dir/package.json" "$replay_dir/package-lock.json" "$install_dir/"
npm --prefix "$install_dir" --cache "$tool_dir/npm-cache" ci --ignore-scripts --no-audit --no-fund
"$tool_dir/pandoc-3.1.11/bin/pandoc" --version | sed -n '1,3p'
node --version
