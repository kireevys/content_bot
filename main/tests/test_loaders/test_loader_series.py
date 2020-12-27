from django.test import TestCase

from loaders.series import SeriesLoader
from main import models


class TestSeriesLoader(TestCase):
    """Проверка загрузчика сериалов."""

    def test_load_new_series(self):
        """Проверка загрузки сериала."""
        title_ru = "Тест"
        title_eng = "Test"
        SeriesLoader.upload(models.Series.new(title_ru, title_eng))

        result = models.Series.objects.get(title_ru=title_ru, title_eng=title_eng)

        episode = models.Episode.objects.get(series=result, season=1, episode=1)
        self.assertEqual(title_ru, result.title_ru)
        self.assertEqual(title_eng, result.title_eng)
        self.assertEqual(episode.series, result)
