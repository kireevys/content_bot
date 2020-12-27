from abc import ABC

from django.conf import settings

from main import models


class Loader(ABC):
    """Загрузчик."""

    channel: int


class SeriesLoader(Loader):
    """Загрузчик сериалов."""

    channel = int(settings.CHANNELS.SERIES.value)

    @classmethod
    def upload(cls, series: models.Series) -> None:
        """Сохранение загруженной серии в БД."""


class MovieLoader(Loader):
    """Загрузчик фильмов."""

    channel = int(settings.CHANNELS.MOVIE.value)
