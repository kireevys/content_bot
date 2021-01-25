import json
import logging

from telegram import CallbackQuery, Update
from telegram.ext import CallbackContext

from components.view import View
from main import models
from main.tg.publisher import Publisher
from views import (
    AllSeries,
    EpisodeChanger,
    EpisodeView,
    ErrorView,
    LanguageMenu,
    MainMenu,
    SeasonMenu,
    SeriesMenu,
)

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
                if self.callback.get("season"):
                    if self.callback.get("lang"):
                        return EpisodeChanger(self.callback)
                    else:
                        return LanguageMenu(self.callback)
                else:
                    return SeasonMenu(self.callback)
            else:
                return SeriesMenu()
        elif self.callback.get("type") == "main":
            return MainMenu()
        elif self.callback.get("type") == "all":
            return AllSeries(models.Series.objects.all())
        elif self.callback.get("type") == "episode":
            return EpisodeView(self.callback)
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
