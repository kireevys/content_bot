import re
from abc import ABC

from django.conf import settings
from telegram import Message


class Loader(ABC):
    """Загрузчик."""

    def __init__(self):
        self.channel: int


class Caption(ABC):
    """Парсер описания."""

    @classmethod
    def parse(cls, caption: str) -> "Caption":
        """Метод формирования Caption из raw данных."""

    @staticmethod
    def _strip_ok_emoji(caption: str) -> str:
        """Обрезает эмоджи-галку внчале, если она есть."""
        stripped = caption
        if caption.startswith(settings.EMOJI.get("ok")):
            stripped = caption.strip(settings.EMOJI.get("ok"))

        return stripped.strip()


class SeriesCaption(Caption):
    """Описание загружаемой серии."""

    def __init__(
        self, title_ru: str, title_eng: str, episode: int, season: int, lang: str
    ):
        self.title_ru = title_ru
        self.title_eng = title_eng
        self.episode = episode
        self.season = season
        self.lang = lang

    @classmethod
    def parse(cls, caption: str) -> "SeriesCaption":
        """Парсит описание.

        Examples:
            caption:
                Неортодоксальная / Unorthodox
                1 Сезон / 4 Серия
                SUB
        """
        caption = cls._strip_ok_emoji(caption)

        title, series, *lang = caption.split("\n")
        season, episode = re.findall(r"(\d+)", series)

        title_ru, title_eng = [i.strip() for i in title.split("/")]

        lang = lang[0].strip() if lang else "RUS"

        return cls(title_ru, title_eng, int(episode), int(season), lang)

    def __eq__(self, other: "SeriesCaption") -> bool:
        return all(
            (
                self.title_ru == other.title_ru,
                self.title_eng == other.title_eng,
                self.lang == other.lang,
                self.episode == other.episode,
                self.season == other.season,
            )
        )


class FileContent:
    """Объект файла для видео.

    Содержит информацию о хранении в Telegram.
    """

    def __init__(self, file_id: str, message_id: int):
        self.file_id = file_id
        self.message_id = message_id

    @classmethod
    def from_message(cls, message: Message) -> "FileContent":
        """Строитель из сообщения."""
        return cls(message.video.file_id, message.message_id)

    def __eq__(self, other: "FileContent") -> bool:
        return all((self.file_id == other.file_id, self.message_id == other.message_id))

    def __str__(self):
        return f"{self.file_id}-{self.message_id}"
