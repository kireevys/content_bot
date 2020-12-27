from enum import Enum

from django.conf import settings
from telegram import Update
from telegram.ext import Dispatcher, Updater, CommandHandler, CallbackContext

from main.factory import ViewRender
from main.views import MainMenu


def start(update: Update, context: CallbackContext):
    """Отклик на команду /start."""
    view = MainMenu(
        "test",
        "https://occ-0-2794-2219.1.nflxso.net/dnm/api/v6/LmEnxtiAuzezXBjYXPuDgfZ4zZQ/AAAABSPrjQDeZC5a1YVfbODFnaUQ8sejisIEI62mvKcW-dJCV5IuoFDBgDa8MWFM5ZI5Gyc0HDdYUeaDzFF-cySZ64SfOwWptrY8c3EI.png?r=df2",
    )

    context.bot.send_photo(
        chat_id=update.effective_chat.id, **ViewRender(view).view_to_message()
    )


class Commands(Enum):
    START = ("start", start)

    def __init__(self, command: str, fn):
        self.command = command
        self.fn = fn


def run() -> Dispatcher:
    """Инициализация хендлеров и запуск бота."""
    updater = Updater(token=settings.TOKEN, use_context=True)
    dispatcher: Dispatcher = updater.dispatcher

    start_handler = CommandHandler(Commands.START.command, Commands.START.fn)
    dispatcher.add_handler(start_handler)

    updater.start_polling(poll_interval=0.2)

    return dispatcher
