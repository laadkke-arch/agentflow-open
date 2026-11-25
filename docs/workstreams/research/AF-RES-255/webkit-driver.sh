#!/bin/sh
# Resolve the Debian build's compiled libexec path within this process tree.
set -eu
: "${AF255_WEBKIT_ROOT:?set to the extracted Debian package root}"
: "${AF255_WEBKIT_SHIM:?set to the compiled libexec relocation library}"
library_dir="$AF255_WEBKIT_ROOT/usr/lib/x86_64-linux-gnu"
export LD_LIBRARY_PATH="$library_dir${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export AF255_WEBKIT_LIBEXEC="$library_dir/webkit2gtk-4.1"
export LD_PRELOAD="$AF255_WEBKIT_SHIM"
export WEBKIT_DISABLE_DMABUF_RENDERER=1
export WEBKIT_DISABLE_SANDBOX_THIS_IS_DANGEROUS=1
exec "$AF255_WEBKIT_ROOT/usr/bin/WebKitWebDriver" "$@"
