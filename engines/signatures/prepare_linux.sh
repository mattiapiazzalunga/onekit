#!/bin/sh
# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
# Linux authoring only. Packages are downloaded and extracted, never installed
# on the authoring host; no guest package post-install scripts are executed.
set -eu
test "$#" -eq 1 || { echo build_directory_argument >&2; exit 1; }
TASK=$(realpath -m "$1")
case "$TASK" in /|/home|/usr|/var|/tmp) echo unsafe_build_directory >&2; exit 1;; esac
if [ -d "$TASK" ] && [ ! -f "$TASK/.onekit-dss-authoring" ]; then
    test -z "$(ls -A "$TASK")" || { echo build_directory_not_empty >&2; exit 1; }
fi
mkdir -p "$TASK/debs/partial" "$TASK/apt-lists/partial" "$TASK/root" "$TASK/sources"
touch "$TASK/.onekit-dss-authoring" "$TASK/status"
cat > "$TASK/debian.list" <<'SOURCES'
deb [arch=i386 signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://deb.debian.org/debian bookworm main
deb [arch=i386 signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://security.debian.org/debian-security bookworm-security main
deb-src [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://deb.debian.org/debian bookworm main
deb-src [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://security.debian.org/debian-security bookworm-security main
SOURCES
cat > "$TASK/apt.conf" <<CONFIG
APT::Architecture "i386";
APT::Architectures { "i386"; };
Dir::State::status "$TASK/status";
Dir::State::extended_states "$TASK/extended_states";
Dir::Etc::sourcelist "$TASK/debian.list";
Dir::Etc::sourceparts "-";
Dir::Etc::parts "-";
Dir::Etc::main "-";
Dir::State::lists "$TASK/apt-lists";
Dir::Cache::archives "$TASK/debs";
Dir::Cache::pkgcache "$TASK/cache.bin";
Dir::Cache::srcpkgcache "$TASK/src-cache.bin";
Acquire::Languages "none";
CONFIG
export APT_CONFIG="$TASK/apt.conf"
apt-get update -qq
apt-get install --download-only -y --no-install-recommends openjdk-17-jre-headless fontconfig fonts-dejavu-core
cd "$TASK/debs"
apt-get download busybox-static seabios linux-image-686-pae
KERNEL=$(apt-cache depends linux-image-686-pae | awk '/Depends: linux-image-[0-9]/{print $2; exit}')
test -n "$KERNEL" || { echo kernel_package_unresolved >&2; exit 1; }
apt-get download "$KERNEL"
for pkg in "$TASK"/debs/*.deb; do dpkg-deb -x "$pkg" "$TASK/root"; done
mkdir -p "$TASK/root/bin" "$TASK/root/dev" "$TASK/root/proc" "$TASK/root/sys" "$TASK/root/tmp" "$TASK/root/jobs"
test -x "$TASK/root/bin/busybox" || { echo busybox_missing >&2; exit 1; }
test -x "$TASK/root/usr/lib/jvm/java-17-openjdk-i386/bin/java" || { echo java_missing >&2; exit 1; }
printf '%s\n' "$KERNEL" > "$TASK/kernel-package.txt"
printf 'ONEKIT_LINUX_PACKAGES=%s\n' "$(find "$TASK/debs" -maxdepth 1 -name '*.deb' | wc -l)"
