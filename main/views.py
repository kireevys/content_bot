from typing import Collection

from django.conf import settings
from django.db.models import QuerySet

from main import models
from main.components.button import Button
from main.components.keyborad import Keyboard
from main.components.view import PhotoView, VideoView
from main.components.view import View
from static import Static


class MainMenu(PhotoView):
    """Представление главного меню."""

    def __init__(self):
        self.media = Static(Static.MAIN).link
        self.caption = "Добро пожаловать"
        self.keyboard = self.build_keyboard()

    def build_keyboard(self) -> Keyboard:
        """Создание клавиатуры для главного меню."""
        return Keyboard(
            Button("Меню сериалов", {"type": "series"}), Button("Меню фильмов", {})
        )


class ErrorView(PhotoView):
    """Представление - ошибка."""

    def __init__(self):
        self.media = Static(Static.MAIN).link
        self.caption = "Этот раздел находится в разработке)))"

    def build_keyboard(self) -> Keyboard:
        """Формирование клавиатуры."""
        return Keyboard(Button("Главное меню", {"type": "main"}))


class EpisodeUploadView(VideoView):
    """Представление Эпизода в загрузчике."""

    def __init__(self, episode: models.Episode):
        self.episode = episode

    @property
    def caption(self) -> str:
        """Геттер для описания."""
        return self._get_upload_description(self.episode)

    @property
    def media(self) -> str:
        """Геттер для медиа."""
        return self.episode.file_id

    @staticmethod
    def _get_upload_description(episode: models.Episode) -> str:
        """Описание эпизода в загрузчике."""
        return (
            f"{settings.EMOJI.get('ok')}{episode.series.title_ru} / {episode.series.title_eng}\n"
            f"{episode.season} season / {episode.episode} episode\n"
            f"{episode.lang}"
        )

    def build_keyboard(self) -> Keyboard:
        """Создание клавиатуры эпизода."""
        return Keyboard(*[])


class SeriesMenu(PhotoView):
    """Главеное меню сериалов."""

    media = Static(Static.MAIN).link
    caption = "Главное меню сериалов"

    def build_keyboard(self) -> Keyboard:
        """Создание клавиатуры."""
        return Keyboard(
            Button("Все сериалы", {"type": "all"}),
            Button("Главное меню", {"type": "main"}),
        )


class AllSeries(PhotoView):
    """Все серии."""

    media = Static(Static.MAIN).link
    caption = "Все сериалы"

    def __init__(self, qs: QuerySet):
        self.qs: Collection[models.Series] = qs.all()

    def build_keyboard(self) -> Keyboard:
        """Формирование клавиатуры."""
        buttons = [
            Button(series.title, {"type": "series", "id": series.id})
            for series in self.qs
        ]
        buttons.append(Button("Главное меню", {"type": "main"}))
        return Keyboard(*buttons)
