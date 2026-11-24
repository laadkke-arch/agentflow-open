#!/usr/bin/env bash
# Prepare pinned source and catalogs in an empty Debian 13 x86-64 workspace.
set -euo pipefail
root=${1:?pass an empty directory for source and gettext inputs}
mkdir -p "$root"
root=$(cd "$root" && pwd)
mkdir -p "$root/tools" "$root/inkscape" "$root/published-inkscape"
debian_gettext=https://deb.debian.org/debian/pool/main/g/gettext
debian_inkscape=https://deb.debian.org/debian/pool/main/i/inkscape

download() {
  local url=$1 name=$2 digest=$3
  curl -fLsS --retry 2 --max-time 150 "$url" -o "$root/$name"
  printf '%s  %s\n' "$digest" "$root/$name" | sha256sum --check -
}

download "$debian_gettext/gettext_0.23.1-2_amd64.deb" gettext.deb 25293e75989db79a1d4a6b942674b0e7243da54a0985f8d9df1b345d255d262b
download "$debian_gettext/gettext-base_0.23.1-2_amd64.deb" gettext-base.deb 1a3dfadd661520ff01d379fd89cd0d49972a5a775d490609f1712134ee3d62ca
dpkg-deb -x "$root/gettext.deb" "$root/tools"
dpkg-deb -x "$root/gettext-base.deb" "$root/tools"

git -c advice.detachedHead=false clone --no-tags --depth=1 --branch GIMP_3_0_6 \
  https://github.com/GNOME/gimp.git "$root/gimp"
test "$(git -C "$root/gimp" rev-parse HEAD)" = a77e8fd05d3d08a58650531a3700100f6a3216b7

download "$debian_inkscape/inkscape_1.4.3.orig.tar.xz" inkscape.tar.xz e83a2c3db570b6c5a1ff0fccfe7098837b3f6bd74b133567937c8a91710ed1d1
tar -xJf "$root/inkscape.tar.xz" -C "$root/inkscape" --strip-components=1
download "$debian_inkscape/inkscape_1.4.3-2+b2_amd64.deb" inkscape.deb 852e19c0aa502aead85436c8786955f43a7009b8e0025cc22fe4e22debd84fbf
dpkg-deb --fsys-tarfile "$root/inkscape.deb" |
  tar -x -C "$root/published-inkscape" \
    ./usr/share/locale/ko/LC_MESSAGES/inkscape.mo ./usr/share/locale/de/LC_MESSAGES/inkscape.mo

printf '%s\n' a77e8fd05d3d08a58650531a3700100f6a3216b7 0d15f7504220b00925bc3cb3673fcf44610a17d5
sha256sum "$root/gimp/po/ko.po" "$root/gimp/po/de.po" \
  "$root/inkscape/po/ko.po" "$root/inkscape/po/de.po" "$root/inkscape/po/inkscape.pot"
