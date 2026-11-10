# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Install verified, separately replaceable DSS jars into the authoring guest."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path


def checksum(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def prepare(work, runtime, adapter, trust, certificate):
    root = work.resolve() / 'root'
    if not (work / '.onekit-dss-authoring').is_file():
        raise ValueError('build_directory_marker')
    manifest = json.loads((runtime / 'dependencies.json').read_text(encoding='utf-8'))
    locked = json.loads(Path(__file__).with_name('dependencies.lock.json').read_text(encoding='utf-8'))
    if manifest['components'] != locked['components'] or manifest['dssVersion'] != locked['dssVersion']:
        raise ValueError('dependency_lock_mismatch')
    engine = root / 'engine'
    (engine / 'lib').mkdir(parents=True, exist_ok=True)
    for row in manifest['components']:
        descriptor = row['binary']
        source = (runtime / descriptor['path']).resolve()
        if not source.is_relative_to(runtime.resolve()) or checksum(source) != descriptor['sha256']:
            raise ValueError('dependency_integrity')
        shutil.copyfile(source, engine / 'lib' / source.name)
    shutil.copyfile(adapter, engine / 'onekit.jar')
    shutil.copyfile(trust, engine / 'eu-trust.ser.gz')
    shutil.copyfile(certificate, engine / 'warmup-public.der')
    (engine / 'lotl-pins').mkdir(exist_ok=True)
    for pin in certificate.parent.glob('pin-*.der'):
        shutil.copyfile(pin, engine / 'lotl-pins' / pin.name)
    for path in ('jobs/boot', 'proc', 'sys', 'dev', 'tmp'):
        (root / path).mkdir(parents=True, exist_ok=True)
    digest = checksum(trust)
    script = f'''#!/bin/busybox sh
/bin/busybox mount -t proc proc /proc
/bin/busybox mount -t sysfs sysfs /sys
/bin/busybox mount -t devtmpfs devtmpfs /dev
exec </dev/ttyS0 >/dev/ttyS0 2>&1
/bin/busybox stty -F /dev/ttyS0 -echo
export LD_LIBRARY_PATH=/lib/i386-linux-gnu:/usr/lib/i386-linux-gnu
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-i386
export PATH=/bin:/usr/bin:/sbin:/usr/sbin
export LANG=C.UTF-8
/refresh-state /jobs/boot || exit 1
echo ONEKIT_BOOT
exec "$JAVA_HOME/bin/java" -Djava.awt.headless=true -Donekit.vmRefresh=true \\
  -Donekit.authoringWarmup=true -Donekit.authoringCompactSnapshot=true -Donekit.authoringCertificate=/engine/warmup-public.der \\
  -Xms32m -Xmx256m -XX:TieredStopAtLevel=1 -XX:ReservedCodeCacheSize=32m \\
  -XX:+UseSerialGC -XX:MinHeapFreeRatio=10 -XX:MaxHeapFreeRatio=20 -XX:-ShrinkHeapInSteps \\
  -cp '/engine/onekit.jar:/engine/lib/*' org.onekit.signatures.OfflineEngine \\
  /engine/eu-trust.ser.gz {digest} /jobs
'''
    (root / 'onekit-init').write_text(script, encoding='utf-8', newline='\n')
    (root / 'onekit-init').chmod(0o755)
    return digest


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', required=True, type=Path)
    parser.add_argument('--runtime', required=True, type=Path)
    parser.add_argument('--adapter', required=True, type=Path)
    parser.add_argument('--trust', required=True, type=Path)
    parser.add_argument('--certificate', required=True, type=Path)
    args = parser.parse_args()
    print(prepare(args.work, args.runtime, args.adapter, args.trust, args.certificate))
