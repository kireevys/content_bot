from django.conf import settings

from main.loaders.common import Loader


class MovieLoader(Loader):
    """Загрузчик фильмов."""

    channel = int(settings.CHANNELS.MOVIE.value)
