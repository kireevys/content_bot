import logging
from abc import abstractmethod
from typing import List, Union

from telegram import Message, Update
from telegram.ext import CallbackContext, Filters, MessageHandler

from main import models
from main.exceptions import (
    EpisodeAlreadyExists,
    MovieAlreadyExists,
    MovieParseError,
    SeriesParseError,
)
from main.loaders.common import Caption, FileContent, SeriesCaption
from main.loaders.movies import MovieLoader
from main.loaders.series import SeriesLoader
from main.tg.publisher import Publisher
from main.views import EpisodeUploadView

logger = logging.getLogger("loader")


class UploadHandler:
    """Базовый класс загрузчика."""

    loader = None
    base_filters = None

    @classmethod
    def upload(cls, update: Update, context: CallbackContext) -> Message:
        """Загрузить видео."""
        publisher = Publisher(context.bot, update.effective_message.chat_id)

        try:
            content: Union[models.Episode] = cls.loader.upload(
                cls.parse(update.effective_message),
                FileContent.from_message(update.effective_message),
            )

        except (EpisodeAlreadyExists, MovieAlreadyExists) as e:
            logger.info("Content already exists", extra={"exc": str(e)})
            publisher.delete(update.effective_message.message_id)

        except (SeriesParseError, MovieParseError):
            logger.info("Incorrect caption")
            publisher.delete(update.effective_message.message_id)

        else:
            message = publisher.publish(
                EpisodeUploadView("desc", "media", content),
                update.effective_message.message_id,
            )
            logger.info("Republish content", extra={"content": content})

            content.update_content(FileContent.from_message(message))

            return message

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
    """Загрузчик сериалов."""

    loader = SeriesLoader

    @classmethod
    def parse(cls, message: Message) -> Caption:
        """Распарсить месседж сериала."""
        try:
            return SeriesCaption.parse(message.caption)
        except Exception as e:
            raise SeriesParseError(str(e))


class MovieUploadHandler(UploadHandler):
    """Загрузчик фильмов."""

    loader = MovieLoader

    @classmethod
    def parse(cls, message: Message) -> Caption:
        """Парсер для описания фильмов."""
        pass
