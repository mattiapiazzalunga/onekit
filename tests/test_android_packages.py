import io
import json
import struct
import zipfile

import pytest

from onekit import Artifact, OneKitError, execute


def apk(package='org.example.app', split='', version=7, required=False, utf8=True):
    values=['manifest','package',package,'versionCode','versionName','1.2','split',split,
            'http://schemas.android.com/apk/res/android','application','isSplitRequired']
    encoded=[]
    for value in values:
        data=value.encode('utf-8' if utf8 else 'utf-16-le')
        encoded.append(bytes([len(value),len(data)])+data+b'\0' if utf8 else struct.pack('<H',len(value))+data+b'\0\0')
    offsets=[];position=0
    for item in encoded:offsets.append(position);position+=len(item)
    payload=b''.join(encoded);payload+=b'\0'*(-len(payload)%4)
    start=28+len(values)*4
    pool=struct.pack('<HHIIIIII',1,28,start+len(payload),len(values),0,0x100 if utf8 else 0,start,0)+struct.pack('<'+'I'*len(offsets),*offsets)+payload
    def attribute(key,value,kind=3,ns=8):
        return struct.pack('<IIIHBBI',ns,key,0xffffffff,8,0,kind,value)
    attrs=attribute(1,2,ns=0xffffffff)+attribute(3,version,0x10)+attribute(4,5)
    if split:attrs+=attribute(6,7,ns=0xffffffff)
    def element(name,attrs):
        ext=struct.pack('<IIHHHHHH',0xffffffff,name,20,20,len(attrs)//20,0,0,0)+attrs
        return struct.pack('<HHIII',0x102,16,16+len(ext),0,0xffffffff)+ext
    body=pool+element(0,attrs)
    if required:body+=element(9,attribute(10,1,0x12))
    manifest=struct.pack('<HHI',3,8,8+len(body))+body
    output=io.BytesIO()
    with zipfile.ZipFile(output,'w') as target:
        target.writestr('AndroidManifest.xml',manifest)
        target.writestr('classes.dex',b'dex\n035\0'+bytes(range(128)))
    return output.getvalue()


def bundle(entries):
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w') as target:
        for name,data in entries:target.writestr(name,data)
    return Artifact('app.xapk',stream.getvalue())


@pytest.mark.parametrize('utf8',[True,False])
def test_apk_xapk_roundtrip_preserves_every_original_byte(utf8):
    data=apk(utf8=utf8)
    packed=execute('apk-to-xapk',[Artifact('app.apk',data)]).files[0]
    with zipfile.ZipFile(io.BytesIO(packed.data)) as source:
        manifest=json.loads(source.read('manifest.json'))
        assert manifest['package_name']=='org.example.app'
        assert manifest['version_code']=='7' and manifest['total_size']==len(data)
    result=execute('xapk-to-apk',[packed])
    assert len(result.files)==1 and result.files[0].data==data


def test_splits_and_expansion_data_remain_separate_and_complete():
    base,split=apk(required=True),apk(split='config.en')
    obb='Android/obb/org.example.app/main.7.org.example.app.obb'
    result=execute('xapk-to-apk',[bundle([('base.apk',base),('config.en.apk',split),(obb,b'game data')])])
    assert {file.name:file.data for file in result.files}=={'base.apk':base,'config.en.apk':split,obb:b'game data'}
    assert any('not a universal APK' in warning for warning in result.warnings)


@pytest.mark.parametrize('data',[apk(split='config.en'),apk(required=True)])
def test_incomplete_apks_are_not_presented_as_standalone_xapks(data):
    with pytest.raises(OneKitError,match='split or requires'):
        execute('apk-to-xapk',[Artifact('app.apk',data)])


@pytest.mark.parametrize('entries',[
    [('base.apk',apk()),('../outside.apk',apk())],
    [('base.apk',apk()),('BASE.APK',apk())],
    [('base.apk',apk()),('config.apk',apk(package='org.other.app',split='config.en'))],
    [('base.apk',apk()),('config.apk',apk(version=9,split='config.en'))],
    [('base.apk',apk(required=True))],
    [('split.apk',apk(split='config.en'))],
    [('base.apk',apk()),('Android/obb/org.other.app/game.obb',b'bad')],
    [('base.apk',apk()),('manifest.json',b'{"package_name":"org.other.app"}')],
    [('base.apk',apk()),('manifest.json',b'{"expansions":[{"file":"missing.obb"}]}')],
    [('base.apk',b'not an apk')],
])
def test_invalid_incomplete_or_unsafe_archives_fail_closed(entries):
    with pytest.raises(OneKitError):execute('xapk-to-apk',[bundle(entries)])


def test_manifest_bounds_and_archive_expansion_are_checked():
    damaged=io.BytesIO()
    with zipfile.ZipFile(damaged,'w') as target:target.writestr('AndroidManifest.xml',b'\x03\0\x08\0'+b'\xff'*16)
    with pytest.raises(OneKitError):execute('apk-to-xapk',[Artifact('bad.apk',damaged.getvalue())])
    bomb=io.BytesIO()
    with zipfile.ZipFile(bomb,'w',compression=zipfile.ZIP_DEFLATED) as target:target.writestr('base.apk',b'\0'*2_000_000)
    with pytest.raises(OneKitError,match='expansion'):execute('xapk-to-apk',[Artifact('bomb.xapk',bomb.getvalue())])


def test_corrupt_apk_payload_is_not_repackaged():
    data=bytearray(apk());offset=data.index(b'dex\n035\0')+8;data[offset]^=1
    with pytest.raises(OneKitError,match='Invalid Android'):
        execute('apk-to-xapk',[Artifact('corrupt.apk',bytes(data))])
