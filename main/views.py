from typing import Collection

from django.conf import settings
from django.db.models import QuerySet

from main import models
from main.components.button import Button
from main.components.keyborad import Keyboard
from main.components.view import PhotoView, VideoView
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
            f"{settings.EMOJI.get('ok')}{episode.series.title_ru} "
            f"/ {episode.series.title_eng}\n"
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
    """Все сериалы."""

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
        keyboard = Keyboard(*buttons)
        keyboard.append(Button("Главное меню", {"type": "main"}))
        return keyboard


class SeasonMenu(PhotoView):
    """Меню выбора сезона."""

    def __init__(self, callback: dict):
        self.series = models.Series.objects.get(pk=callback.get("id"))
        self.media = self.series.poster or Static(Static.MAIN).link
        self.caption = self.series.desc or self.series.title_ru

    def build_keyboard(self) -> Keyboard:
        """Формирование клавиатуры."""
        seasons: set = {
            season.season
            for season in models.Episode.objects.filter(series=self.series)
        }
        buttons = [
            Button(
                f"Сезон {season}",
                {"type": "series", "id": self.series.id, "season": season},
            )
            for season in seasons
        ]
        keyboard = Keyboard(*buttons)
        keyboard.append(Button("Список сериалов", {"type": "all"}))
        keyboard.append(Button("Главное меню", {"type": "main"}))

        return keyboard


class LanguageMenu(PhotoView):
    """Вьюха эпизода."""

    def __init__(self, callback: dict):
        self.series = models.Series.objects.get(pk=callback.get("id"))
        self.media = self.series.poster or Static(Static.MAIN).link
        self.caption = "Выбери язык"
        self.season = callback.get("season")

    def build_keyboard(self) -> Keyboard:
        """Формирование клавиатуры."""
        langs = {
            episode.lang
            for episode in models.Episode.objects.filter(
                series=self.series, season=self.season
            )
        }
        buttons = [
            Button(
                models.Langs.repr(
                    lang,
                ),
                {
                    "type": "series",
                    "id": self.series.id,
                    "season": self.season,
                    "lang": lang,
                },
            )
            for lang in langs
        ]
        keyboard = Keyboard(*buttons)
        keyboard.append(
            Button(
                "К выбору сезона",
                {"type": "series", "id": self.series.id},
            )
        )
        keyboard.append(Button("Главное меню", {"type": "main"}))

        return keyboard


class EpisodeChanger(PhotoView):
    """Вьюха Выбора эпизода."""

    def __init__(self, callback: dict):
        self.series = models.Series.objects.get(pk=callback.get("id"))
        self.lang = callback.get("lang")
        self.season = callback.get("season")

        self.media = self.series.poster or Static(Static.MAIN).link

    @property
    def caption(self) -> str:
        """Описание."""
        caption = self.series.title

        if self.series.desc:
            caption += f"\n{self.series.desc}"

        return caption

    def build_keyboard(self) -> Keyboard:
        """Формирование клавиатуры."""
        episodes = models.Episode.objects.filter(
            series=self.series, lang=self.lang, season=self.season
        )

        buttons = [
            Button(
                episode.episode,
                {
                    "type": "episode",
                    "id": episode.pk,
                },
            )
            for episode in episodes
        ]
        keyboard = Keyboard(*buttons)
        keyboard.append(
            Button(
                "К выбору языка",
                {"type": "series", "id": self.series.id, "season": self.season},
            )
        )
        keyboard.append(Button("Главное меню", {"type": "main"}))
        return keyboard


class EpisodeView(VideoView):
    """Вьюха эпизода."""

    def __init__(self, callback: dict):
        self.episode = models.Episode.objects.get(pk=callback.get("id"))
        self.media = self.episode.file_id

    @property
    def caption(self) -> str:
        """Описание."""
        caption = self.episode.series.title

        if self.episode.series.desc:
            caption += f"\n{self.episode.series.desc}"

        caption += f"\n\nСезон {self.episode.season} / Эпизод {self.episode.episode}"

        return caption

    def build_keyboard(self) -> Keyboard:
        """Формирование клавиатуры."""
        episodes = models.Episode.objects.filter(
            series=self.episode.series,
            lang=self.episode.lang,
            season=self.episode.season,
        )

        buttons = [
            Button(
                episode.episode,
                {
                    "type": "episode",
                    "id": episode.pk,
                },
                is_active=episode == self.episode,
            )
            for episode in episodes
        ]
        keyboard = Keyboard(*buttons)
        keyboard.append(
            Button(
                "К описанию",
                {
                    "type": "series",
                    "id": self.episode.series.id,
                    "season": self.episode.season,
                    "lang": self.episode.lang,
                },
            )
        )
        keyboard.append(Button("Главное меню", {"type": "main"}))
        return keyboard
