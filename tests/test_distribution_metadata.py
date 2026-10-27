from pathlib import Path
import tomllib

import pytest


@pytest.fixture
def validate_urls(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / 'scripts'))
    from check_distribution_licenses import validate_project_urls
    return validate_project_urls


def test_project_links_are_publishable_and_author_email_is_preserved(validate_urls):
    project = tomllib.loads((Path(__file__).resolve().parents[1] / 'pyproject.toml').read_text(encoding='utf-8'))['project']
    validate_urls([f'{label}, {url}' for label, url in project['urls'].items()])
    assert project['authors'][0]['email'] == 'hello@mattiapiazzalunga.com'


@pytest.mark.parametrize('entry', [
    'Author, mailto:hello@mattiapiazzalunga.com',
    'Repository, https:///missing-host',
    'Homepage, https://example.com/invalid path',
    'https://example.com',
])
def test_invalid_distribution_links_fail_before_upload(validate_urls, entry):
    with pytest.raises(ValueError, match='Project-URL'):
        validate_urls([entry])
