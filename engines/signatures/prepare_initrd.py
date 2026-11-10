# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Assemble a minimal initrd from the exact kernel and BusyBox Debian packages."""
import argparse
import gzip
import shutil
import subprocess
from pathlib import Path


def prepare(work, output):
    work, output = work.resolve(), output.resolve()
    root = work / 'root'
    kernels = list((root / 'boot').glob('vmlinuz-*'))
    if len(kernels) != 1:
        raise ValueError('kernel_selection')
    kernel = kernels[0].name.removeprefix('vmlinuz-')
    subprocess.run(['depmod', '-b', str(root), kernel], check=True)
    initrd = work / 'initrd'
    for directory in ('bin', 'dev', 'proc', 'rootfs'):
        (initrd / directory).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(root / 'bin/busybox', initrd / 'bin/busybox')
    (initrd / 'bin/busybox').chmod(0o755)
    for module in ('virtio_pci', '9pnet_virtio', '9p'):
        result = subprocess.run(['modprobe', '-d', str(root), '-S', kernel, '--show-depends', module],
                                check=True, capture_output=True, text=True)
        for row in result.stdout.splitlines():
            if not row.startswith('insmod '):
                continue
            path = Path(row.removeprefix('insmod ').strip()).resolve()
            target = initrd / path.relative_to(root)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
    for metadata in (root / 'lib/modules' / kernel).glob('modules.*'):
        if metadata.is_file():
            shutil.copyfile(metadata, initrd / metadata.relative_to(root))
    script = '''#!/bin/busybox sh
/bin/busybox mount -t devtmpfs devtmpfs /dev
/bin/busybox mount -t proc proc /proc
/bin/busybox modprobe virtio_pci || exit 1
/bin/busybox modprobe 9pnet_virtio || exit 1
/bin/busybox modprobe 9p || exit 1
/bin/busybox mount -t 9p -o trans=virtio,version=9p2000.L,cache=loose host9p /rootfs || exit 1
exec /bin/busybox switch_root /rootfs /onekit-init
'''
    (initrd / 'init').write_text(script, encoding='utf-8', newline='\n')
    (initrd / 'init').chmod(0o755)
    paths = ['.'] + [str(path.relative_to(initrd)) for path in sorted(initrd.rglob('*'))]
    packed = subprocess.run(['cpio', '--null', '-o', '--format=newc', '--owner=0:0'],
                            input=('\0'.join(paths) + '\0').encode(), capture_output=True, cwd=initrd, check=True)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'initrd.cpio.gz').write_bytes(gzip.compress(packed.stdout, mtime=0))
    shutil.copyfile(kernels[0], output / 'kernel.bin')
    shutil.copyfile(root / 'usr/share/seabios/bios.bin', output / 'seabios.bin')
    shutil.copyfile(root / 'usr/share/seabios/vgabios-stdvga.bin', output / 'vgabios.bin')
    print(kernel)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    prepare(args.work, args.output)
