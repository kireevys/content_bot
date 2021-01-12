import json

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    InputMediaVideo,
)

from main.components.keyborad import Keyboard
from main.components.view import PhotoView, VideoView, View


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

    def for_send(self) -> dict:
        """Словарь для отправки."""
        if isinstance(self.view, VideoView):
            return {
                "video": self.view.media,
                "caption": self.view.caption,
                "reply_markup": KeyboardFactory(self.view.build_keyboard()).to_column(),
            }
        elif isinstance(self.view, PhotoView):
            return {
                "photo": self.view.media,
                "caption": self.view.caption,
                "reply_markup": KeyboardFactory(self.view.build_keyboard()).to_column(),
            }
        else:
            raise TypeError("Incorrect view")

    def for_edit(self) -> dict:
        """Словарь для редактирования."""

        if isinstance(self.view, VideoView):
            media_class = InputMediaVideo
        elif isinstance(self.view, PhotoView):
            media_class = InputMediaPhoto
        else:
            raise TypeError("Incorrect view")

        return {
            "media": media_class(media=self.view.media, caption=self.view.caption),
            "reply_markup": KeyboardFactory(self.view.build_keyboard()).to_column(),
        }
