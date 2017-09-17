import string

from myanimelist.models import MediaStatus


class StatusFormatter(object):

    def format_statuses(self, statuses, template, headers):
        template = string.Template(template)

        def lines():
            n_rows = 2
            for status in MediaStatus:
                n_media = statuses[status]

                if n_media > 0:
                    header = headers[status]
                    yield template.safe_substitute(index=n_rows, content=header)
                    n_rows += n_media

        return '\n'.join(lines())
