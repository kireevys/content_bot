from django.test import TestCase

from main.views import MainMenu


class TestView(TestCase):
    """Проверка формирования стартового меню."""

    def test_main_menu_keyboard(self) -> None:
        """Проверка возврата главного меню на команду /start."""
        expected_description = "Hello"
        expected_media = "code_some_media"
        expected = MainMenu(expected_description, expected_media)

        result = MainMenu(expected_description, expected_media)

        self.assertEqual(expected, result)
