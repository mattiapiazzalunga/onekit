# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import pytest

from onekit.models import OneKitError
from onekit.tools.link_tools import download_target, source_links


def test_google_images_wrapper_preserves_original_query_and_skips_search_page():
    url='https://www.google.it/imgres?imgurl=https%3A%2F%2Fcdn.example%2Fphoto.png%3Fa%3D1%26b%3D2&imgrefurl=https%3A%2F%2Fexample.com'
    assert download_target(url,'image')['url']=='https://cdn.example/photo.png?a=1&b=2'
    fake='https://www.google.it.evil.example/imgres?imgurl=https%3A%2F%2Fother.example%2Fa.png'
    assert download_target(fake,'image')['url']==fake
    with pytest.raises(OneKitError):download_target('https://google.com/imgres?imgurl=javascript%3Aalert(1)','image')


@pytest.mark.parametrize('url',['https://youtu.be/test','https://www.youtube.com/watch?v=test','https://m.youtube.com/shorts/test','https://youtube-nocookie.com/embed/test'])
def test_youtube_classification_is_available_without_network(url):
    assert download_target(url,'video')['requires_extractor']
    assert not download_target(url,'image')['requires_extractor']
    assert not download_target('https://youtube.com.evil.example/video','video')['requires_extractor']


def test_image_metadata_is_prioritized_over_icons_and_lazy_responsive_sources_work():
    html=''.join(f'<img src="/icon{i}.png">' for i in range(12))+'<meta property="og:image" content="/main.jpg">'
    assert source_links(html,'https://example.com/page','image')[0]=='https://example.com/main.jpg'
    html='<base href="https://cdn.example/assets/"><picture><source srcset="small.jpg 320w, large.jpg 1600w"><img src="data:image/gif;base64,AA" data-src="lazy.jpg"></picture>'
    assert source_links(html,'https://example.com/page','image')[:3]==['https://cdn.example/assets/large.jpg','https://cdn.example/assets/small.jpg','https://cdn.example/assets/lazy.jpg']
