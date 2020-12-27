from django.test import TestCase

from main import models


class TestSeries(TestCase):
    """Проверка модели сериалов."""

    def test_new_series(self):
        """Проверка метода добавления Сериала."""
        models.Series.new(title_ru="Тест", title_eng="Test")

        result = models.Series.objects.first()

        self.assertEqual(result.title_eng, "Test")

    def test_add_series(self):
        """Проверка добавления сериала."""
        models.Series.objects.create(title_ru="Тест", title_eng="Test")

        result = models.Series.objects.first()

        self.assertEqual(result.title_eng, "Test")

    def test_add_episode(self):
        """Проверка добавления эпизода в сериал."""
        series = models.Series.objects.create(title_ru="Тест", title_eng="Test")
        episode = models.Episode(
            season=1,
            episode=1,
            lang=models.Langs.RUS.value,
            message_id=1,
            file_id="file",
        )

        series.add_episode(episode=episode)

        found_episode = models.Episode.objects.get(
            series=series, episode=1, lang=models.Langs.RUS.value
        )
        self.assertIsNotNone(found_episode)
