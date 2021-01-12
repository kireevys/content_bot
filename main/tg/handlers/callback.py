import logging
import json
from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext

from main import models
from components.view import View
from static import Static
from main.tg.publisher import Publisher
from views import SeriesMenu, MainMenu, ErrorView, AllSeries

logger = logging.getLogger("main")


class Callback:
    """Объект колбека.

    Задача колбека - вернуть правильную вьюшку.
    """

    def __init__(self, callback_query: CallbackQuery):
        self.callback = json.loads(callback_query.data)

    def get_view(self) -> View:
        """Получение вьюхи для реакции."""
        if self.callback.get("type") == "series":
            if self.callback.get("id"):
                return SeasonMenu()
            else:
                return SeriesMenu()
        elif self.callback.get("type") == "main":
            return MainMenu()
        elif self.callback.get("type") == "all":
            return AllSeries(models.Series.objects.all())
        else:
            logger.error(f"Untyped callback {self.callback}")
            return ErrorView()

    def reaction(self):
        """Реакция на коллбек."""
        return self.get_view()


def callback(update: Update, context: CallbackContext):
    """Хендлер коллбеков."""
    publisher = Publisher(context.bot, update.effective_message.chat_id)

    callback_query = Callback(update.callback_query)
    publisher.publish(callback_query.get_view(), update.effective_message.message_id)

    update.callback_query.answer()
    logger.info("Callback answered")
