import logging
from typing import Union

from django.conf import settings

from main.loaders.common import FileContent, Loader, SeriesCaption  # noqa: I202
from main import models

logger = logging.getLogger("loader")


class SeriesLoader(Loader):
    """Загрузчик сериалов."""

    def __init__(self):
        super().__init__()
        self.channel = int(settings.CHANNELS.SERIES.value)

    @classmethod
    def upload(
        cls, caption: SeriesCaption, file_content: FileContent
    ) -> Union[models.Episode]:
        """Сохранение загруженной серии в Хранилище."""
        series, _ = models.Series.objects.get_or_create(
            title_ru=caption.title_ru, title_eng=caption.title_eng
        )
        episode = series.add_episode(
            models.Episode(
                episode=caption.episode,
                season=caption.season,
                lang=caption.lang,
                message_id=file_content.message_id,
                file_id=file_content.file_id,
            )
        )
        logger.info(
            "Load episode",
            extra={
                "series": series,
                "episode": episode,
            },
        )

        return episode
