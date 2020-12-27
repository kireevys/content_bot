import json

from main.components.view import View
from main.components.keyborad import Keyboard
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


class KeyboardFactory:
    """Фабрика клавиатуры"""

    def __init__(self, keyboard: Keyboard) -> None:
        self.keyboard = keyboard

    def to_column(self) -> InlineKeyboardMarkup:
        """Клавиатура в InlineKeyboardMarkup."""
        row = [
            InlineKeyboardButton(
                button.description, callback_data=json.dumps(button.callback)
            )
            for button in self.keyboard.buttons
        ]
        return InlineKeyboardMarkup.from_column(row)


class ViewRender:
    """Рендер вьюхи"""

    def __init__(self, view: View) -> None:
        self.view = view

    def view_to_message(self):
        """Создает сообщение на основе вьюхи."""
        return {
            "photo": self.view.media,
            "caption": self.view.description,
            "reply_markup": KeyboardFactory(self.view.keyboard).to_column(),
        }
