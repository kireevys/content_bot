from django.test import TestCase

from main import models
from main.static import Static


class TestStaticEnum(TestCase):
    """Проверка Enum-статики."""

    def setUp(self) -> None:
        """Подготовка стенда."""
        self.main = models.Static.objects.create(
            link="http://google.com", description="Test Main Static", slug="main"
        )

    def test_slug(self):
        """Проверка получения существующего ключа."""
        result = Static.MAIN

        self.assertEqual(self.main, result.model)
        self.assertEqual(self.main.link, result.link)
