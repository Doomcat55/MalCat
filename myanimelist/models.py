import collections
import enum


class User(collections.namedtuple('User', ('name',))):

    @property
    def _normalized(self):
        return self._replace(name=self.name.lower())

    def __hash__(self):
        return tuple.__hash__(self._normalized)

    def __eq__(self, other):
        try:
            return tuple.__eq__(self._normalized, other._normalized)
        except AttributeError:
            return False


class UserStatistics(collections.namedtuple('UserStatistics', ('media_status_breakdown',))):

    def n_media_with_status(self, media_type, media_status):
        return self.media_status_breakdown[media_type][media_status]


UserProfile = collections.namedtuple('UserProfile', ('statistics',))


class MediaType(enum.Enum):

    ANIME = 'anime'
    MANGA = 'manga'


class MediaStatus(enum.Enum):

    CURRENT = 1
    COMPLETED = 2
    ON_HOLD = 3
    DROPPED = 4
    PLANNED = 5
