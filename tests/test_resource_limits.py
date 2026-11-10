from dataclasses import FrozenInstanceError, replace
import io
import zipfile

import pytest

from onekit import Artifact, OneKitError, execute
from onekit.catalog import TOOLS, Tool
from onekit.execution import MAX_BYTES, ExecutionContext, ToolLimits
from onekit.limits import LIMITS, resource_limits
from onekit import validation


def test_limits_are_immutable_and_exported_as_an_independent_copy():
    with pytest.raises(FrozenInstanceError):
        LIMITS.max_bytes = 1
    exported = resource_limits()
    exported['max_bytes'] = 1
    assert resource_limits()['max_bytes'] == MAX_BYTES
    assert validation.MAX_FILES == LIMITS.max_files
    assert validation.MAX_PIXELS == LIMITS.max_image_pixels
    assert Tool.__dataclass_fields__['max_total_bytes'].default == LIMITS.max_bytes
    assert all(tool.max_file_bytes <= tool.max_total_bytes <= LIMITS.max_bytes for tool in TOOLS.values())


def test_consumers_can_tighten_but_not_raise_core_byte_ceilings():
    with pytest.raises(OneKitError):
        ToolLimits(LIMITS.max_bytes + 1, LIMITS.max_bytes + 1)
    context = ExecutionContext(tool_limits={'apk-to-xapk': ToolLimits(128, 128)})
    assert context.constrain(TOOLS['apk-to-xapk']).max_total_bytes == 128


def test_zip_validation_uses_the_configured_entry_ceiling(monkeypatch):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w') as archive:
        archive.writestr('a.txt', b'a')
        archive.writestr('b.txt', b'b')
    validation.validate_zip(stream.getvalue(), LIMITS.max_bytes)
    monkeypatch.setattr(validation, 'LIMITS', replace(LIMITS, max_archive_entries=1))
    with pytest.raises(OneKitError):
        validation.validate_zip(stream.getvalue(), LIMITS.max_bytes)


def test_android_and_face_guards_follow_the_shared_policy(monkeypatch):
    from test_android_packages import apk
    from test_face_blur import source
    from onekit.tools import android_packages, face_blur
    monkeypatch.setattr(android_packages, 'LIMITS', replace(LIMITS, max_android_manifest_bytes=8))
    with pytest.raises(OneKitError):
        execute('apk-to-xapk', [Artifact('app.apk', apk())])
    monkeypatch.setattr(face_blur, 'LIMITS', replace(LIMITS, max_face_pixels=1))
    with pytest.raises(OneKitError, match='single-frame'):
        execute('image-blur-faces', [source()])
