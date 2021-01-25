from django.conf import settings

from main.loaders.common import Loader


class MovieLoader(Loader):
    """Загрузчик фильмов."""

    @property
    def channel(self) -> int:
        """Идентификатор канала загрузчика."""
        return int(settings.CHANNELS.MOVIE.value)
