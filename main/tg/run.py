import logging
import traceback
from enum import Enum

from django.conf import settings
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Dispatcher, Updater

from main import models
from main.factory import ViewRender
from main.tg.handlers.loader import SeriesUploadHandler
from main.views import MainMenu
from static import Static

logger = logging.getLogger("telegram")

def error_callback(update, context):
    """Колбек исключений телеги."""
    try:
        raise context.error
    except Exception:
        logger.error(traceback.format_exc())


def start(update: Update, context: CallbackContext):
    """Отклик на команду /start."""
    view = MainMenu("test", Static(Static.MAIN).link)

    context.bot.send_photo(
        chat_id=update.effective_chat.id, **ViewRender(view).view_to_message()
    )


class Commands(Enum):
    """Команды."""

    START = ("start", start)

    def __init__(self, command: str, fn):
        self.command = command
        self.fn = fn


def run() -> Dispatcher:
    """Инициализация хендлеров и запуск бота."""
    updater = Updater(token=settings.TOKEN, use_context=True)
    dispatcher: Dispatcher = updater.dispatcher

    dispatcher.add_error_handler(error_callback)

    start_handler = CommandHandler(Commands.START.command, Commands.START.fn)
    dispatcher.add_handler(start_handler)

    [dispatcher.add_handler(handler) for handler in SeriesUploadHandler.get_handlers()]

    updater.start_polling(poll_interval=0.2)

    return dispatcher
