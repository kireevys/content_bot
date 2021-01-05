from unittest.mock import MagicMock, patch

from django.conf import settings
from django.test import TestCase

from main import exceptions
from main import models
from main.loaders.common import SeriesCaption
from main.loaders.series import SeriesLoader
from main.tg.handlers.loader import SeriesUploadHandler


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

    def test_upload_new_series(self):
        """Проверка проксирования серии в объекты."""
        caption = f"""{settings.EMOJI.get('ok')} Пацаны / The Boys
                2 season / 7 episode
                RUS"""
        update = MagicMock(
            effective_message=MagicMock(
                caption=caption, message_id=1, video=MagicMock(file_id=10)
            )
        )
        with patch("main.tg.publisher.Publisher.publish") as p_mock:  # type: MagicMock
            with patch.object(SeriesLoader, "upload") as m:  # type: # MagicMock
                SeriesUploadHandler.upload(update, MagicMock())  # act

        m.assert_called_once()
        p_mock.assert_called_once()

    def test_upload_exists_series(self):
        """Проверка действий при загрузке существующей серии."""
        caption = f"""{settings.EMOJI.get('ok')} Пацаны / The Boys
                2 season / 7 episode
                RUS"""
        update = MagicMock(
            effective_message=MagicMock(
                caption=caption, message_id=1, video=MagicMock(file_id=10)
            )
        )
        with patch("main.tg.publisher.Publisher.delete") as p_mock:  # type: MagicMock
            with patch.object(
                SeriesLoader, "upload", side_effect=exceptions.EpisodeAlreadyExists()
            ) as m:  # type: MagicMock
                SeriesUploadHandler.upload(update, MagicMock())  # act

        m.assert_called_once()
        p_mock.assert_called_once()

    def test_upload_series_with_invalid_caption(self):
        """Проверка действий при загрузке существующей серии."""
        caption = f"""{settings.EMOJI.get('ok')} Пацаны / The Boys
                7 episode
                RUS"""
        update = MagicMock(
            effective_message=MagicMock(
                caption=caption, message_id=1, video=MagicMock(file_id=10)
            )
        )
        with patch("main.tg.publisher.Publisher.delete") as p_mock:  # type: MagicMock
            SeriesUploadHandler.upload(update, MagicMock())  # act

        p_mock.assert_called_once()
