import telegram
from telegram import Bot, InputMediaVideo, InputMediaPhoto, Message

from components.view import View
from factory import ViewRender


class Publisher:
    """Вспомогательный класс для публикации сообщения."""

    def __init__(self, bot: Bot, chat_id: int) -> None:
        self.bot = bot
        self.chat_id = chat_id

    def _edit(self, view: View, previous_message_id: int) -> Message:
        """Редактирование сообщения.

        Args:
            view:
            previous_message_id:

        Raises:
            telegram.error.BadRequest
        """
        return self.bot.edit_message_media(
            chat_id=self.chat_id,
            message_id=previous_message_id,
            **ViewRender(view).view_to_message(),
        )

    def send_media(self, view: View) -> Message:
        """Отправляет медиа в заисимости от содержимого."""
        rendered = ViewRender(view).view_to_message()

        if rendered.get("video"):
            return self.bot.send_video(**rendered, chat_id=self.chat_id)
        elif rendered.get("photo"):
            return self.bot.send_photo(**rendered, chat_id=self.chat_id)
        else:
            raise ValueError("View has not media")

    def delete(self, message_id: int) -> None:
        """Удаление сообщения."""
        self.bot.delete_message(chat_id=self.chat_id, message_id=message_id)

    def _replace(self, view: View, previous_message_id: int) -> Message:
        """Замена сообщения удалением."""
        self.bot.delete_message(chat_id=self.chat_id, message_id=previous_message_id)
        return self.send_media(view)

    def publish(self, view: View, previous_message_id: int) -> Message:
        """
        Публикация сообщения.

        Этот метод заменяет предыдущее сообщение.

        Args:
            view:  View, которое будет отправлено
            previous_message_id: Идентификатор сообщения, которое надо заменить
        """
        try:
            return self._edit(view, previous_message_id)
        except (telegram.error.BadRequest, TypeError):
            return self._replace(view, previous_message_id)
