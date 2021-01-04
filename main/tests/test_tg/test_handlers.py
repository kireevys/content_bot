from unittest.mock import MagicMock, patch

from django.conf import settings
from django.test import TestCase

from main import models
from tg.handlers.loader import SeriesUploadHandler
from main.loaders.series import SeriesLoader
from loaders.common import SeriesCaption


class TestLoaderSeries(TestCase):
    """Проверка загрузчика сериалов."""

    def test_parse(self):
        """Проверка преобразования Update в Caption."""
        caption = f"""{settings.EMOJI.get('ok')} Пацаны / The Boys
                2 season / 7 episode
                RUS"""
        message = MagicMock(caption=caption)

        expected = SeriesCaption("Пацаны", "The Boys", 7, 2, models.Langs.RUS.value)

        result = SeriesUploadHandler.parse(message)

        self.assertEqual(result, expected)

    def test_upload(self):
        """Проверка проксирования серии в объекты."""
        caption = f"""{settings.EMOJI.get('ok')} Пацаны / The Boys
                2 season / 7 episode
                RUS"""
        update = MagicMock(
            effective_message=MagicMock(
                caption=caption, message_id=1, video=MagicMock(file_id=10)
            )
        )
        with patch.object(SeriesLoader, "upload") as m:
            SeriesUploadHandler.upload(update, MagicMock())

        m.assert_called_once()
