from django.test import TestCase
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from main.controller import Controller
from main.factory import ViewRender
from main.views import MainMenu


class TestController(TestCase):
    """Проверки контроллера."""

    def test_entry(self) -> None:
        """Проверка точки входа."""
        result = Controller().entry()

        self.assertEqual(MainMenu("some", "media"), result)


class TestMessageFactory(TestCase):
    """Проверка фабрики сообщений."""

    def test_view_to_message(self) -> None:
        """Проверка преобразования вьюхи в сообщение."""
        text = "hello"
        media = "code_some_media"
        view = MainMenu(text, media)
        factory = ViewRender(view)
        expected = {
            "photo": media,
            "caption": text,
            "reply_markup": InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Меню сериалов", callback_data="{}")],
                    [InlineKeyboardButton("Меню фильмов", callback_data="{}")],
                ]
            ),
        }

        message = factory.view_to_message()  # act

        self.assertEqual(message.get("photo"), expected.get("photo"))
        self.assertEqual(message.get("caption"), expected.get("caption"))
        self.assertEqual(
            message.get("reply_markup").to_dict(),
            expected.get("reply_markup").to_dict(),
        )
