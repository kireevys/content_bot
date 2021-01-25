from django.conf import settings
from django.test import TestCase

from main import models
from main.loaders.common import SeriesCaption


class TestSeriesCaption(TestCase):
    """Проверка Парсера описания Сериала."""

    def test_parse(self):
        """Проверка парсинга."""
        caption = f"""{settings.EMOJI.get('ok')} Пацаны / The Boys
2 season / 7 episode
RUS"""
        expected = SeriesCaption("Пацаны", "The Boys", 7, 2, models.Langs.RUS.value)

        result = SeriesCaption.parse(caption)

        self.assertEqual(result, expected)

    def test_strip_ok_emoji(self):  # noqa: AAA01
        """Проверка обрезки эмоджи."""
        for i, expected in [
            (f"{settings.EMOJI.get('ok')}aa", "aa"),
            (f"{settings.EMOJI.get('ok')} aa", "aa"),
            (f"{settings.EMOJI.get('ok')}aa ", "aa"),
            (f"{settings.EMOJI.get('ok')}  aa  ", "aa"),
            (f"{settings.EMOJI.get('ok')}  aa  ", "aa"),
            ("aa", "aa"),
            ("   aa    ", "aa"),
        ]:
            with self.subTest(f"{i} = {expected}"):

                result = SeriesCaption._strip_ok_emoji(i)  # act

                self.assertEqual(result, expected)
