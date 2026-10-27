# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Export an EPUB's spine with the shared portable document exporter."""
import io
import posixpath
import zipfile
from urllib.parse import unquote, urlsplit

from ..models import Artifact, OneKitError
from .portable_documents import convert
from .structured_data import xml_root


def local_path(base,href):
    uri = urlsplit(href)
    if uri.scheme or uri.netloc or '\\' in href:
        raise OneKitError('EPUB chapter paths must be local archive entries.')
    path = posixpath.normpath(posixpath.join(base,unquote(uri.path)))
    if path.startswith(('../','/')) or path == '..':
        raise OneKitError('EPUB chapter paths cannot leave the archive.')
    return path


def epub_html(file):
    with zipfile.ZipFile(io.BytesIO(file.data)) as archive:
        names = set(archive.namelist())
        if 'META-INF/encryption.xml' in names:
            raise OneKitError('Encrypted or DRM-protected EPUB files are not supported.')
        if archive.read('mimetype').strip() != b'application/epub+zip':
            raise OneKitError('Choose a valid EPUB book.')
        container = xml_root(archive.read('META-INF/container.xml'))
        rootfile = next((node.get('full-path') for node in container.iter() if node.tag.rsplit('}',1)[-1]=='rootfile'),None)
        if not rootfile:
            raise OneKitError('EPUB is missing its package document.')
        package_path = local_path('',rootfile)
        package = xml_root(archive.read(package_path))
        items = {node.get('id'):node for node in package.iter() if node.tag.rsplit('}',1)[-1]=='item'}
        spine = [node for node in package.iter() if node.tag.rsplit('}',1)[-1]=='itemref' and node.get('linear')!='no']
        if not spine or len(spine)>256:
            raise OneKitError('EPUB must contain between 1 and 256 reading-order chapters.')
        chapters = []
        chapter_bytes = 0
        for ref in spine:
            item = items.get(ref.get('idref'))
            if item is None or item.get('media-type') not in ('application/xhtml+xml','text/html'):
                raise OneKitError('EPUB spine contains an unsupported chapter format.')
            path = local_path(posixpath.dirname(package_path),item.get('href',''))
            data = archive.read(path)
            chapter_bytes += len(data)
            if chapter_bytes>8*1024*1024:
                raise OneKitError('EPUB chapter text exceeds 8 MiB; split the book.')
            chapters.append(data)
    html = '\n'.join(data.decode('utf-8-sig') for data in chapters)
    return html,len(chapters)


def run(tool, files, options):
    file = files[0]
    html,chapters = epub_html(file)
    result = convert(Artifact(file.stem+'.html',html.encode()),'html','pdf')
    result.warnings.append('Basic text layout in EPUB reading order. Original CSS, images, fonts, fixed layouts and interactive content are not reproduced.')
    result.details['chapters'] = chapters
    return result
