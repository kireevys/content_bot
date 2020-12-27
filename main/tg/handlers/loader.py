from typing import List

from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters

from main.loaders.series import SeriesLoader, MovieLoader


class UploadHandler:
    loader = None
    base_filters = None

    # @classmethod
    # def add_description(cls, update: Update, context: CallbackContext):
    #     """Добавление описания."""
    #     cls.uploader(update, context).add_description(update.effective_message.text)
    #
    # @classmethod
    # def add_poster(cls, update: Update, context: CallbackContext):
    #     """"""
    #     cls.uploader(update, context).add_poster(update.channel_post.photo[-1].file_id)

    @classmethod
    def upload(cls, update: Update, context: CallbackContext):
        cls.loader(update, context).upload()

    @classmethod
    def get_handlers(cls) -> List[MessageHandler]:
        """Возвращает хендлеры загрузчика."""
        filters = (~Filters.command) & (Filters.chat(cls.loader.channel))

        return [
            MessageHandler(
                Filters.video & filters,
                cls.upload,
            )
        ]


class SeriesUploadHandler(UploadHandler):
    loader = SeriesLoader


class MovieUploadHandler(UploadHandler):
    loader = MovieLoader
