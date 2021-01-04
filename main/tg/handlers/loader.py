from abc import abstractmethod
from typing import List

from telegram import Update, Message
from telegram.ext import CallbackContext, MessageHandler, Filters

from loaders.common import Caption, SeriesCaption, FileContent
from main.loaders.series import SeriesLoader
from loaders.movies import MovieLoader


class UploadHandler:
    loader = None
    base_filters = None

    @classmethod
    def upload(cls, update: Update, context: CallbackContext) -> None:
        """Загрузить видео."""
        message = update.effective_message
        caption = cls.parse(message)
        file = FileContent(message.message_id, message.video.file_id)
        cls.loader.upload(caption, file)

    @classmethod
    @abstractmethod
    def parse(cls, message: Message) -> Caption:
        """Распарсить сообщение."""
        pass

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

    @classmethod
    def parse(cls, message: Message) -> Caption:
        """Распарсить месседж сериала."""
        return SeriesCaption.parse(message.caption)


class MovieUploadHandler(UploadHandler):
    loader = MovieLoader
