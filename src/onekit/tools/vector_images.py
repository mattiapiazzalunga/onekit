# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Vectorize TIFF and validate SVG before delegating raster rendering."""
import io
import re
from xml.etree import ElementTree as ET

from ..execution import current_context
from ..models import OneKitError, Result, output
from .structured_data import xml_root
from .video_edit import number


def svg_input(file, options):
    root = xml_root(file.data)
    if root.tag not in ('svg','{http://www.w3.org/2000/svg}svg'):
        raise OneKitError('Choose a valid SVG image.')
    for node in root.iter():
        tag = node.tag.rsplit('}',1)[-1].lower()
        if tag in ('script','foreignobject','animate','animatetransform','set','image','feimage'):
            raise OneKitError('Use a static, self-contained SVG without scripts, animation or embedded images.')
        for key,value in node.attrib.items():
            key = key.rsplit('}',1)[-1].lower()
            if key.startswith('on') or key in ('href','src') and not value.startswith('#'):
                raise OneKitError('SVG external resources and event handlers are not supported.')
        for value in [*node.attrib.values(),node.text or '']:
            if '@import' in value.lower() or re.search(r'url\(\s*[\'"]?(?!#)[^\s\'"]',value,re.IGNORECASE) or '\\' in value:
                raise OneKitError('SVG styles must not load external resources.')
    def dimension(value):
        match = re.fullmatch(r'\s*(\d+(?:\.\d+)?)\s*(px)?\s*',value or '')
        return float(match[1]) if match else None
    width,height = dimension(root.get('width')),dimension(root.get('height'))
    view = root.get('viewBox','').replace(',',' ').split()
    if (not width or not height) and len(view)==4:
        try:
            width,height = float(view[2]),float(view[3])
        except ValueError:
            pass
    if not width or not height or width<=0 or height<=0:
        raise OneKitError('SVG needs positive pixel dimensions or a viewBox.')
    if not root.get('viewBox'):
        root.set('viewBox',f'0 0 {width:g} {height:g}')
    scale = number(options,'scale',1,.1,4)
    width,height = round(width*scale),round(height*scale)
    if not 1<=width<=16384 or not 1<=height<=16384 or width*height>16000000:
        raise OneKitError('SVG output must contain at most 16 million pixels, up to 16384 pixels per side.')
    root.set('width',str(width));root.set('height',str(height))
    return {'svg':ET.tostring(root,encoding='unicode'),'width':width,'height':height}


def run(tool, files, options):
    file = files[0]
    if tool.id in ('tiff-to-svg','png-to-svg'):
        from .images import open_image
        from .photo_tools import vectorize
        image = open_image(file)
        colors = number(options,'colors',16,2,64,integer=True)
        resolution = number(options,'resolution',128,32,256,integer=True)
        data,shapes = vectorize(image,colors,resolution)
        return Result([output(file,'svg',data)],warnings=['Palette-based vector tiles approximate the first image frame. Fine detail and gradients may change; transparency is composited on white. No bitmap is embedded.'],details={'shapes':shapes})
    request = svg_input(file,options)
    renderer = current_context().svg_renderer
    if renderer:
        data = bytes(renderer(request))
    else:
        import resvg_py
        data = resvg_py.svg_to_bytes(svg_string=request['svg'],width=request['width'],height=request['height'])
    from PIL import Image
    with Image.open(io.BytesIO(data)) as image:
        if image.format != 'PNG' or image.size != (request['width'],request['height']):
            raise OneKitError('SVG renderer returned an invalid PNG image.')
        image.verify()
    return Result([output(file,'png',data)],details={'width':request['width'],'height':request['height']})
