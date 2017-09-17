import os

import lxml.etree
import pytest

from myanimelist.api import _Parser


_resources_directory = 'tests/resources/'


def _read_media(file_name):
    path = os.path.join(_resources_directory, file_name)
    media_type = 'anime' if 'anime' in file_name else 'manga'
    nodes = (node for _, node in lxml.etree.iterparse(path, tag=media_type))
    media = []
    for node in nodes:
        media.append({element.tag: element.text for element in node})
        node.clear()
    return media


class _DummyResponse(object):

    def __init__(self, content):
        self.content = content


def _read_profile(file_name):
    path = os.path.join(_resources_directory, file_name)
    with open(path) as f:
        data = f.read()
    response = _DummyResponse(data)
    parser = _Parser()
    return parser.parse_profile(response)


@pytest.fixture(scope='session')
def empty_media_list():
    return _read_media('empty list.xml')


@pytest.fixture(scope='session')
def regular_anime_list():
    return _read_media('regular anime list.xml')


@pytest.fixture(scope='session')
def regular_manga_list():
    return _read_media('regular manga list.xml')


@pytest.fixture(scope='session')
def huge_anime_list():
    return _read_media('huge anime list.xml')


@pytest.fixture(scope='session')
def huge_manga_list():
    return _read_media('huge manga list.xml')


@pytest.fixture(scope='session')
def profile():
    return _read_profile('profile.html')
