from django.test import TestCase
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

from main.components.button import Button
from main.components.keyborad import Keyboard
from main.components.view import View, VideoView
from main.factory import ViewRender
from main.views import MainMenu


class SomeView(VideoView):
    """Тестовая вьюха."""

    def __init__(self):
        self.media = "media"
        self.caption = "some caption"
        self.keyboard = self.build_keyboard()

    def build_keyboard(self) -> "Keyboard":
        return Keyboard(
            Button("First", {}),
            Button("Second", {}),
        )


class TestMessageFactory(TestCase):
    """Проверка фабрики сообщений."""

    def test_view_render_for_edit(self) -> None:
        """Проверка преобразования вьюхи в сообщение."""

        factory = ViewRender(SomeView())
        expected = {
            "media": InputMediaPhoto("media", caption="some caption"),
            "reply_markup": InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("First", callback_data="{}")],
                    [InlineKeyboardButton("Second", callback_data="{}")],
                ]
            ),
        }

        message = factory.for_edit()  # act

        self.assertEqual(message.get("media").media, expected.get("media").media)
        self.assertEqual(message.get("caption"), expected.get("caption"))
        self.assertEqual(
            message.get("reply_markup").to_dict(),
            expected.get("reply_markup").to_dict(),
        )
