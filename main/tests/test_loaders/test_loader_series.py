from django.test import TestCase

from main import models
from main.exceptions import EpisodeAlreadyExists
from main.loaders.common import FileContent, SeriesCaption
from main.loaders.series import SeriesLoader


class TestSeriesLoader(TestCase):
    """Проверка загрузчика сериалов."""

    def test_load_new_series(self):
        """Проверка загрузки новго сериала и эпизода."""
        title_ru = "Тест"
        title_eng = "Test"
        caption = SeriesCaption(title_ru, title_eng, 1, 1, "RUS")
        file_content = FileContent("file_id", 123)
        SeriesLoader.upload(caption, file_content)

        result = models.Series.objects.get(title_ru=title_ru, title_eng=title_eng)

        episode = models.Episode.objects.get(series=result, season=1, episode=1)
        self.assertEqual(title_ru, result.title_ru)
        self.assertEqual(title_eng, result.title_eng)
        self.assertEqual(episode.series, result)
        self.assertEqual(FileContent(episode.file_id, episode.message_id), file_content)

    def test_load_exist_episode(self):
        """Проверка загрузки существующего эпизода."""
        title_ru = "Тест"
        title_eng = "Test"
        caption = SeriesCaption(title_ru, title_eng, 1, 1, "RUS")
        file_content = FileContent("file_id", 123)
        SeriesLoader.upload(caption, file_content)

        with self.assertRaises(EpisodeAlreadyExists):
            SeriesLoader.upload(caption, FileContent("another_file_id", 4321))

    def test_load_new_episode(self):
        """Загрузка нового эпизода в сериал."""
        title_ru = "Тест"
        title_eng = "Test"
        SeriesLoader.upload(
            SeriesCaption(title_ru, title_eng, 1, 1, "RUS"), FileContent("file_id", 123)
        )
        SeriesLoader.upload(
            SeriesCaption(title_ru, title_eng, 1, 2, "RUS"), FileContent("new", 4321)
        )

        result = models.Episode.objects.filter(series__title_ru=title_ru)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].season, 1)
        self.assertEqual(result[1].season, 2)
