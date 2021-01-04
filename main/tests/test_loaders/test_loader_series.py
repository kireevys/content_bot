from django.test import TestCase

from loaders.common import SeriesCaption, FileContent
from loaders.series import SeriesLoader
from main import models


class TestSeriesLoader(TestCase):
    """Проверка загрузчика сериалов."""

    def test_load_new_series(self):
        """Проверка загрузки сериала."""
        title_ru = "Тест"
        title_eng = "Test"
        caption = SeriesCaption(title_ru, title_eng, 1, 1, "RUS")
        file = FileContent("file_id", 123)
        SeriesLoader.upload(caption, file)

        result = models.Series.objects.get(title_ru=title_ru, title_eng=title_eng)

        episode = models.Episode.objects.get(series=result, season=1, episode=1)
        self.assertEqual(title_ru, result.title_ru)
        self.assertEqual(title_eng, result.title_eng)
        self.assertEqual(episode.series, result)
        self.assertEqual(FileContent(episode.file_id, episode.message_id), file)
