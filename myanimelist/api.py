import functools

import lxml.etree
import lxml.html
import requests
import six
from six.moves.urllib import parse as urllib_parse

from myanimelist.models import MediaStatus, MediaType, UserProfile, UserStatistics


def _set_parameters(url, parameters):
    query_string = urllib_parse.urlencode(parameters)
    return urllib_parse.urlparse(url)._replace(query=query_string).geturl()


class NetworkError(Exception):
    pass


class _Downloader(object):

    _SCHEME = 'https'
    _DOMAIN = 'myanimelist.net'
    _ROOT_URL = urllib_parse.urlunparse((_SCHEME, _DOMAIN, '/', None, None, None))
    _API_URL = urllib_parse.urljoin(_ROOT_URL, 'malappinfo.php')
    _PROFILE_ROOT_URL = urllib_parse.urljoin(_ROOT_URL, 'profile/')

    def __init__(self):
        self._session = requests.Session()

    @classmethod
    def _media_api_parameters(cls, user, media_type):
        return {'u': user.name, 'media_type': media_type.value, 'status': 'all'}

    @classmethod
    def _profile_url(cls, user):
        return urllib_parse.urljoin(cls._PROFILE_ROOT_URL, user.name)

    def _get(self, *args, **kwargs):
        try:
            response = self._session.get(*args, **kwargs)
            response.raise_for_status()
        except requests.RequestException as e:
            six.raise_from(NetworkError, e)
        return response

    def user_media(self, user, media_type):
        parameters = self._media_api_parameters(user, media_type)
        return self._get(self._API_URL, params=parameters, stream=True)

    def user_profile(self, user):
        url = self._profile_url(user)
        return self._get(url)


class _Parser(object):

    _MEDIA_STATUSES_SELECTOR = '.stats.{type} .stats-status li a + span'

    @classmethod
    def _media_statuses_selector(cls, media_type):
        return cls._MEDIA_STATUSES_SELECTOR.format(type=media_type.value)

    def parse_media(self, response, media_type):
        # Don't bother validating XML etc. - invalid XML will just result in an empty list
        xml = response.raw
        xml.read = functools.partial(xml.read, decode_content=True)
        nodes = (node for _, node in lxml.etree.iterparse(xml, tag=media_type.value))
        media = []
        for node in nodes:
            media.append({element.tag: element.text for element in node})
            node.clear()
        return media

    def _parse_media_status_breakdown(self, document, media_type):
        selector = self._media_statuses_selector(media_type)
        values = (int(element.text.replace(',', '')) for element in document.cssselect(selector))
        return dict(zip(MediaStatus, values))

    def parse_profile(self, response):
        html = response.content
        document = lxml.html.fromstring(html)
        media_status_breakdown = {
            media_type: self._parse_media_status_breakdown(document, media_type)
            for media_type in MediaType
        }
        statistics = UserStatistics(media_status_breakdown)
        profile = UserProfile(statistics)
        return profile


class Myanimelist(object):

    def __init__(self):
        self._downloader = _Downloader()
        self._parser = _Parser()

    def user_media(self, user, media_type):
        response = self._downloader.user_media(user, media_type)
        media = self._parser.parse_media(response, media_type)
        return media

    def user_profile(self, user):
        response = self._downloader.user_profile(user)
        profile = self._parser.parse_profile(response)
        return profile
