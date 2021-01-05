from django.conf import settings
from telegram import InputMediaVideo

from factory import KeyboardFactory
from main import models
from main.components.button import Button
from main.components.keyborad import Keyboard
from main.components.view import View


class MainMenu(View):
    """Представление главного меню."""

    def __init__(self, description: str, media: str) -> None:
        super().__init__(description, media)

    def render(self) -> dict:
        """Рендерит менюху."""
        return {
            "photo": self.media,
            "caption": self.description,
            "reply_markup": KeyboardFactory(self.keyboard).to_column(),
        }

    def build_keyboard(self) -> Keyboard:
        """Создание клавиатуры для главного меню."""
        return Keyboard(Button("Меню сериалов", {}), Button("Меню фильмов", {}))


class EpisodeUploadView(View):
    """Представление Эпизода в загрузчике."""

    def __init__(self, description: str, media: str, episode: models.Episode):
        super().__init__(self._get_upload_description(episode), episode.file_id)

    @staticmethod
    def _get_upload_description(episode: models.Episode) -> str:
        """Описание эпизода в загрузчике."""
        return (
            f"{settings.EMOJI.get('ok')}{episode.series.title_ru} / {episode.series.title_eng}\n"
            f"{episode.season} season / {episode.episode} episode\n"
            f"{episode.lang}"
        )

    def render(self) -> dict:
        """Рендерит ответ на загрузку эпизода."""
        return {
            "video": self.media,
            "caption": self.description,
            "reply_markup": KeyboardFactory(self.keyboard).to_column(),
        }

    def build_keyboard(self) -> Keyboard:
        """Создание клавиатуры эпизода."""
        return Keyboard(*[])
