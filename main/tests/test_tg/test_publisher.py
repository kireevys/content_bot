from unittest.mock import MagicMock, patch

from django.test import TestCase

from main.factory import ViewRender
from main.tg.publisher import Publisher
from main.views import MainMenu


class TestPublisher(TestCase):
    """Проверка класса публикации."""

    def test_publish_photo(self):
        """Проверка публикации фото."""
        bot = MagicMock()
        chat_id = 123
        message_id = 321
        view = MainMenu()
        rendered_view = ViewRender(view).for_edit()
        with patch.object(bot, "edit_message_media") as m_bot:  # type: MagicMock

            Publisher(bot, chat_id).publish(view, message_id)  # act

        m_bot.assert_called_once_with(
            chat_id=chat_id, message_id=message_id, **rendered_view
        )

    def test_send_media_photo(self):
        """Проверка отправки медиа вьюшек."""
        view = MainMenu()
        bot = MagicMock()
        chat_id = 123

        result = Publisher(bot, chat_id).send_media(view)

        self.assertTrue(result)
