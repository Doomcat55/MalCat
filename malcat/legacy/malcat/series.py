import string


class SeriesFormatter(object):

    def __init__(self, media_type):
        self._media_type = media_type
        self._id_key = 'series_{}db_id'.format(media_type.value)

    def format_media(self, media, template):
        template = string.Template(template)

        def lines():
            for index, medium in enumerate(media):
                substitutions = dict(medium)
                substitutions['index'] = index
                substitutions['list'] = self._media_type.value
                try:
                    substitutions['id'] = medium[self._id_key]
                except KeyError:
                    pass

                yield template.safe_substitute(**substitutions)

        return '\n'.join(lines())
