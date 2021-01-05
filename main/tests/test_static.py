from django.test import TestCase

from main import models
from main.static import Static


class TestStaticEnum(TestCase):
    """Проверка Enum-статики."""

    def setUp(self) -> None:
        """Подготовка стенда."""
        self.main = models.Static.objects.create(
            link="http:://google.com", description="Test Main Static", slug="google"
        )

    def test_slug(self):
        """Проверка получения существующего ключа."""
        result = Static("google")

        self.assertEqual(self.main, result.model)
        self.assertEqual(self.main.link, result.link)
