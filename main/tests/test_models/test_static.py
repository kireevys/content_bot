from django.test import TestCase

from main import models


class TestStatic(TestCase):
    """Проверка модели статики."""

    def setUp(self) -> None:
        """Подготовка стенда."""
        self.google = models.Static.objects.create(
            link="http:://google.com", description="TestStatic", slug="google"
        )
        self.yandex = models.Static.objects.create(
            link="http:://yandex.com", description="TestStatic", slug="yandex"
        )

    def test_get_by_slug(self):
        """Проверка получения статики по slug."""
        google = models.Static.get_by_slug("google")  # act

        self.assertEqual(self.google, google)

    def test_slug_not_found(self):
        """Проверка получения несущществующего slug."""
        with self.assertRaises(models.Static.DoesNotExist):
            models.Static.get_by_slug("not_exists")
