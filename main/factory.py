import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from main.components.keyborad import Keyboard
from main.components.view import View


class KeyboardFactory:
    """Фабрика клавиатуры."""

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
    """Рендер вьюхи."""

    def __init__(self, view: View) -> None:
        self.view = view

    def view_to_message(self) -> dict:
        """Создает сообщение на основе вьюхи."""
        return self.view.render()
