import io
from pathlib import Path

import pytest
from PIL import Image

from onekit import Artifact, OneKitError, execute
from onekit.execution import ExecutionContext


def source():
    image=Image.new('RGB',(120,100),'white')
    for x in range(120):
        for y in range(100):image.putpixel((x,y),(255*(x%2),255*(y%2),128))
    exif=Image.Exif();exif[270]='Private source metadata'
    output=io.BytesIO();image.save(output,format='PNG',exif=exif)
    return Artifact('private.png',output.getvalue())


def test_blur_changes_face_pixels_preserves_other_pixels_and_strips_metadata():
    file=source()
    context=ExecutionContext(face_reader=lambda _: [{'x':40,'y':35,'width':20,'height':20}])
    result=execute('image-blur-faces',[file],context=context)
    with Image.open(io.BytesIO(result.files[0].data)) as output,Image.open(io.BytesIO(file.data)) as original:
        assert output.size==original.size
        assert output.getpixel((45,45))[:3]!=original.getpixel((45,45))
        assert output.getpixel((0,0))[:3]==original.getpixel((0,0))
        assert not output.getexif() and 'exif' not in output.info
    assert result.details=={'faces':1}


@pytest.mark.parametrize('faces',[[],[{'x':float('nan'),'y':0,'width':10,'height':10}],[{'x':0,'y':0,'width':-1,'height':10}]])
def test_no_detection_or_invalid_boxes_do_not_export_an_unredacted_image(faces):
    with pytest.raises(OneKitError):execute('image-blur-faces',[source()],context=ExecutionContext(face_reader=lambda _: faces))


def test_real_yunet_model_detects_and_blurs_a_public_domain_face():
    pytest.importorskip('onnxruntime')
    from onekit.tools.face_blur import detect
    file=Artifact('astronaut.png',(Path(__file__).parent/'fixtures/face-astronaut.png').read_bytes())
    boxes=detect(file)
    assert len(boxes)>=1 and boxes[0]['score']>.8
    result=execute('image-blur-faces',[file])
    with Image.open(io.BytesIO(result.files[0].data)) as output,Image.open(io.BytesIO(file.data)) as original:
        assert output.getpixel((140,70))[:3]!=original.getpixel((140,70))
        assert output.getpixel((0,0))[:3]==original.getpixel((0,0))


def test_bundled_model_and_license_are_pinned():
    import hashlib
    from importlib.resources import files
    from onekit.tools.face_blur import MODEL
    data=files('onekit').joinpath('data')
    assert hashlib.sha256(data.joinpath('yunet.onnx').read_bytes()).hexdigest()==MODEL['sha256']
    assert 'MIT License' in data.joinpath('yunet-LICENSE.txt').read_text()


def test_real_detector_finds_multiple_faces():
    pytest.importorskip('onnxruntime')
    from onekit.tools.face_blur import detect
    with Image.open(Path(__file__).parent/'fixtures/face-astronaut.png') as photo:
        image=Image.new('RGB',(photo.width*2,photo.height));image.paste(photo,(0,0));image.paste(photo,(photo.width,0))
        stream=io.BytesIO();image.save(stream,format='PNG')
    boxes=detect(Artifact('group.png',stream.getvalue()))
    assert len(boxes)==2
    assert min(box['x'] for box in boxes)<320 and max(box['x'] for box in boxes)>320
