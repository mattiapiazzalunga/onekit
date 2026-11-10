# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Inspect and repackage Android archives without executing or rewriting APKs."""
import io
import json
import re
import stat
import struct
import zipfile

from ..models import Artifact, OneKitError, Result, parse_json
from ..limits import LIMITS

INVALID = 'Invalid Android package or manifest.'
UNSAFE = 'Android archive contains unsafe, duplicate, encrypted or oversized entries.'


def archive(data, limit, *, portable=True):
    try:
        from ..validation import validate_zip
        validate_zip(data, limit)
        result = zipfile.ZipFile(io.BytesIO(data))
        entries = result.infolist()
        seen = set()
        if not entries or len(entries) > LIMITS.max_archive_entries or sum(entry.file_size for entry in entries) > limit:
            raise OneKitError(UNSAFE)
        for entry in entries:
            name = entry.filename
            if portable:
                Artifact(name.rstrip('/'), b'')
            key = name.casefold() if portable else name
            if key in seen or '\\' in name or entry.flag_bits & 1 or stat.S_ISLNK(entry.external_attr >> 16):
                raise OneKitError(UNSAFE)
            if entry.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
                raise OneKitError(UNSAFE)
            seen.add(key)
        return result
    except (zipfile.BadZipFile, ValueError, OverflowError) as error:
        if isinstance(error, OneKitError):
            raise
        raise OneKitError(INVALID) from error


def binary_manifest(data):
    """Read bounded Android ResXMLTree attributes, including UTF-8/UTF-16 pools."""
    def u16(offset):
        return struct.unpack_from('<H', data, offset)[0]

    def u32(offset):
        return struct.unpack_from('<I', data, offset)[0]

    def length(offset, wide, end):
        unit = 2 if wide else 1
        if offset + unit > end:
            raise ValueError()
        value = u16(offset) if wide else data[offset]
        offset += unit
        flag = 0x8000 if wide else 0x80
        if value & flag:
            if offset + unit > end:
                raise ValueError()
            value = ((value & (flag - 1)) << (16 if wide else 8)) | (u16(offset) if wide else data[offset])
            offset += unit
        return value, offset

    if len(data) < 8 or len(data) > LIMITS.max_android_manifest_bytes or u16(0) != 3 or u32(4) != len(data):
        raise ValueError()
    offset = u16(2)
    strings, elements = [], []
    if offset < 8:
        raise ValueError()
    while offset < len(data):
        if offset + 8 > len(data):
            raise ValueError()
        kind, header, size = u16(offset), u16(offset + 2), u32(offset + 4)
        end = offset + size
        if header < 8 or size < header or end > len(data):
            raise ValueError()
        if kind == 1:
            if header < 28:
                raise ValueError()
            count, flags, start = u32(offset + 8), u32(offset + 16), u32(offset + 20)
            styles = u32(offset + 24)
            if count > LIMITS.max_android_strings or header + count * 4 > start or start >= size:
                raise ValueError()
            string_end = offset + (styles or size)
            for index in range(count):
                pos = offset + start + u32(offset + header + index * 4)
                if pos >= string_end:
                    raise ValueError()
                utf8 = bool(flags & 0x100)
                if utf8:
                    _, pos = length(pos, False, string_end)
                count_chars, pos = length(pos, not utf8, string_end)
                byte_count = count_chars * (1 if utf8 else 2)
                terminator = 1 if utf8 else 2
                if pos + byte_count + terminator > string_end or any(data[pos + byte_count:pos + byte_count + terminator]):
                    raise ValueError()
                strings.append(data[pos:pos + byte_count].decode('utf-8' if utf8 else 'utf-16-le'))
        elif kind == 0x102:
            if header < 16 or header + 20 > size:
                raise ValueError()
            ext = offset + header
            name = strings[u32(ext + 4)]
            attr_start, attr_size, count = u16(ext + 8), u16(ext + 10), u16(ext + 12)
            if attr_start < 20 or attr_size < 20 or ext + attr_start + attr_size * count > end:
                raise ValueError()
            attrs = {}
            for index in range(count):
                pos = ext + attr_start + index * attr_size
                namespace, key, raw = u32(pos), strings[u32(pos + 4)], u32(pos + 8)
                ns = '' if namespace == 0xffffffff else strings[namespace]
                if ns not in ('', 'http://schemas.android.com/apk/res/android') or key in attrs:
                    raise ValueError()
                value_type, value = data[pos + 15], u32(pos + 16)
                if value_type == 3:
                    value = strings[value]
                elif value_type == 0x12:
                    value = bool(value)
                elif value_type not in (0x10, 0x11):
                    value = strings[raw] if raw != 0xffffffff else None
                attrs[key] = value
            elements.append((name, attrs))
        offset = end
    if not elements or elements[0][0] != 'manifest' or sum(name == 'manifest' for name, _ in elements) != 1:
        raise ValueError()
    return elements


def apk_info(data, limit):
    try:
        with archive(data, limit, portable=False) as source:
            entry = source.getinfo('AndroidManifest.xml')
            if entry.file_size > LIMITS.max_android_manifest_bytes:
                raise ValueError()
            elements = binary_manifest(source.read(entry))
            if source.testzip() is not None:
                raise ValueError()
        attrs = elements[0][1]
        package = attrs.get('package', '')
        version = attrs.get('versionCode')
        if not isinstance(package, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*', package):
            raise ValueError()
        major = attrs.get('versionCodeMajor', 0)
        if type(version) is not int or not 0 <= version <= 0xffffffff or type(major) is not int or not 0 <= major <= 0x7fffffff:
            raise ValueError()
        version |= major << 32
        split = attrs.get('split', '')
        if not isinstance(split, str):
            raise ValueError()
        required = any(name == 'uses-split' or name == 'application' and values.get('isSplitRequired') is True
                       or name == 'meta-data' and values.get('name') == 'com.android.vending.splits.required' and values.get('value') is True
                       for name, values in elements)
        sdk = next((values for name, values in elements if name == 'uses-sdk'), {})
        return {'package_name': package, 'version_code': str(version), 'version_name': str(attrs.get('versionName') or version),
                'min_sdk_version': str(sdk.get('minSdkVersion') or 1),
                'target_sdk_version': str(sdk.get('targetSdkVersion') or sdk.get('minSdkVersion') or 1),
                'split': split, 'required': required,
                'uses': [values['name'] for name, values in elements if name == 'uses-split' and isinstance(values.get('name'), str)],
                'permissions': sorted({values['name'] for name, values in elements if name == 'uses-permission' and isinstance(values.get('name'), str)})}
    except (ValueError, KeyError, IndexError, struct.error, UnicodeError, zipfile.BadZipFile) as error:
        if isinstance(error, OneKitError):
            raise
        raise OneKitError(INVALID) from error


def run(tool, files, options):
    file = files[0]
    limit = options['_max_expanded_bytes']
    if tool.id == 'apk-to-xapk':
        info = apk_info(file.data, limit)
        if info['split'] or info['required']:
            raise OneKitError('This APK is a split or requires other APKs. Supply a complete standalone APK.')
        manifest = {key: value for key, value in info.items() if key not in ('split', 'required', 'uses')}
        manifest.update(xapk_version=1, name=info['package_name'], total_size=len(file.data), expansions=[])
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_STORED) as target:
            target.writestr(info['package_name'] + '.apk', file.data)
            target.writestr('manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8'))
        return Result([Artifact(file.stem + '.xapk', stream.getvalue())])
    outputs, records = [], []
    with archive(file.data, limit) as source:
        entries = source.infolist()
        if sum(not entry.is_dir() and entry.filename.lower().endswith(('.apk', '.obb')) for entry in entries) > LIMITS.max_files:
            raise OneKitError(UNSAFE)
        manifest = None
        if 'manifest.json' in source.namelist():
            if source.getinfo('manifest.json').file_size > LIMITS.max_xapk_manifest_bytes:
                raise OneKitError(INVALID)
            manifest = parse_json(source.read('manifest.json').decode('utf-8-sig'))
            if not isinstance(manifest, dict):
                raise OneKitError(INVALID)
        for entry in entries:
            if entry.is_dir():
                continue
            if entry.filename.lower().endswith('.apk'):
                data = source.read(entry)
                records.append(apk_info(data, limit))
                outputs.append(Artifact(entry.filename, data))
        if not records or sum(not record['split'] for record in records) != 1:
            raise OneKitError('The XAPK must contain one base APK and all required split APKs.')
        base = next(record for record in records if not record['split'])
        if any((record['package_name'], record['version_code']) != (base['package_name'], base['version_code']) for record in records):
            raise OneKitError('The APKs belong to different Android packages or versions.')
        if len({record['split'] for record in records}) != len(records) or len(records) == 1 and base['required']:
            raise OneKitError('The XAPK must contain one base APK and all required split APKs.')
        if any(dependency not in {record['split'] for record in records} for record in records for dependency in record['uses']):
            raise OneKitError('The XAPK must contain one base APK and all required split APKs.')
        if manifest and manifest.get('package_name', base['package_name']) != base['package_name']:
            raise OneKitError('The XAPK manifest does not match its APK files.')
        if manifest:
            for key in ('expansions', 'split_apks'):
                declared = manifest.get(key, [])
                suffix = '.obb' if key == 'expansions' else '.apk'
                if not isinstance(declared, list) or any(not isinstance(item, dict) or not isinstance(item.get('file'), str) or not item['file'].lower().endswith(suffix) or item['file'] not in source.namelist() for item in declared):
                    raise OneKitError('The XAPK manifest does not match its APK files.')
        for entry in entries:
            if entry.filename.lower().endswith('.obb'):
                expected = 'Android/obb/' + base['package_name'] + '/'
                if not entry.filename.startswith(expected) or '/' in entry.filename[len(expected):]:
                    raise OneKitError('OBB files must be inside the matching Android/obb package directory.')
                outputs.append(Artifact(entry.filename, source.read(entry)))
    warnings = []
    if len(records) > 1:
        warnings.append('Split APKs were preserved separately. Install the base and matching splits together; they are not a universal APK.')
    if len(outputs) > len(records):
        warnings.append('OBB data was preserved. Copy it to the matching Android/obb directory after installing the APKs.')
    return Result(outputs, warnings)
