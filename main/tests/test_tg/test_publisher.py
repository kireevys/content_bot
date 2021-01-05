from unittest.mock import MagicMock, patch

from django.test import TestCase

from factory import ViewRender
from tg.publisher import Publisher
from views import MainMenu


class TestPublisher(TestCase):
    """Проверка класса публикации."""

    def test_publish_photo(self):
        """Проверка публикации фото."""
        bot = MagicMock()
        chat_id = 123
        message_id = 321
        view = MainMenu("Some Description", "media_link")
        rendered_view = ViewRender(view).view_to_message()

        with patch.object(bot, "edit_message_media") as m_bot:  # type: MagicMock
            Publisher(bot, chat_id).publish(view, message_id)

        m_bot.assert_called_once_with(
            chat_id=chat_id, message_id=message_id, **rendered_view
        )
