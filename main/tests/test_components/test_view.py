from django.test import TestCase

from main.views import MainMenu


class TestView(TestCase):
    """Проверка формирования стартового меню."""

    def test_eq(self) -> None:
        """Проверка метода сравнения для вьюх."""
        self.assertEqual(MainMenu(), MainMenu())  # act
