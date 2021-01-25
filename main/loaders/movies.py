from django.conf import settings

from main.loaders.common import Loader


class MovieLoader(Loader):
    """Загрузчик фильмов."""

    def __init__(self):
        super().__init__()
        self.channel = int(settings.CHANNELS.MOVIE.value)
