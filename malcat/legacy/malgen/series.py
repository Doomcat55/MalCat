import os.path
import re


def _mal_sized_image_url(url, size):
    base, extension = os.path.splitext(url)
    return base + size + extension


def _mal_thumbnail_url(url):
    return _mal_sized_image_url(url, 't')


def _mal_poster_url(url):
    return _mal_sized_image_url(url, 'l')


class SeriesFormatter(object):

    _tags = {'ID', 'TYPE', 'TITLE', 'URL', 'SURL', 'LURL', 'IMG', 'SIMG', 'LIMG', 'SCORE', 'STATUS'}
    _pattern = re.compile('\\[(' + '|'.join(_tags) + ')\\]')

    def __init__(self, media_type):
        self._media_type = media_type
        self._id_key = 'series_{}db_id'.format(self._media_type.value)

    def _format_template(self, template, tags):
        def match_value(match):
            tag = match.group(1)
            return tags.get(tag, tag)

        return self._pattern.sub(match_value, template)

    def format_media(self, media, template):
        def lines():
            for medium in media:
                image_url = medium['series_image']
                thumbnail_url = _mal_thumbnail_url(image_url)
                poster_url = _mal_poster_url(image_url)

                tags = {
                    'ID': medium[self._id_key],
                    'TYPE': self._media_type.value,
                    'TITLE': medium['series_title'],
                    'URL': image_url,
                    'SURL': thumbnail_url,
                    'LURL': poster_url,
                    'IMG': image_url,
                    'SIMG': thumbnail_url,
                    'LIMG': thumbnail_url,
                    'SCORE': medium['my_score'],
                    'STATUS': medium['series_status']
                }

                yield self._format_template(template, tags)

        return '\n'.join(lines())
