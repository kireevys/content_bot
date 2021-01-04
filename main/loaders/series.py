from django.conf import settings
from main import models

from loaders.common import Loader, SeriesCaption, FileContent


class SeriesLoader(Loader):
    """Загрузчик сериалов."""

    channel = int(settings.CHANNELS.SERIES.value)

    @classmethod
    def upload(cls, caption: SeriesCaption, file: FileContent) -> None:
        """Сохранение загруженной серии в Хранилище."""
        series, _ = models.Series.objects.get_or_create(
            title_ru=caption.title_ru, title_eng=caption.title_eng
        )
        episode, _ = models.Episode.objects.get_or_create(
            series=series,
            message_id=file.message_id,
            file_id=file.file_id,
            episode=caption.episode,
            lang=caption.lang,
            season=caption.season,
        )
