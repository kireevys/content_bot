import django
from django.db import models

from main.exceptions import EpisodeAlreadyExists
from main.loaders.common import FileContent
from .common import Langs

__all__ = ("Series", "Episode")


class Series(models.Model):
    """Модель сериала."""

    title_ru = models.TextField(unique=True, null=True)
    title_eng = models.TextField(unique=True)
    poster = models.TextField(unique=False, null=True, blank=True)
    genre = models.ManyToManyField("Genre", blank=True)
    desc = models.TextField(null=True, blank=True)

    class Meta:
        """Метаданные."""

        db_table = "series"
        verbose_name = "Сериалы"
        verbose_name_plural = "Сериалы"

    @classmethod
    def new(cls, title_ru: str, title_eng: str) -> "Series":
        """Конструктор сериала."""
        return cls.objects.get_or_create(title_ru=title_ru, title_eng=title_eng)

    def add_episode(self, episode: "Episode") -> "Episode":
        """Добавление эпизода.

        Raises:
            EpisodeAlreadyExists
        """
        episode.series = self
        try:
            episode.save()
        except django.db.utils.IntegrityError:
            raise EpisodeAlreadyExists(f"Episode {episode} already exists")

        return episode

    @property
    def title(self) -> str:
        """Геттер заголовка."""
        return f"{self.title_ru} / {self.title_eng}"

    def __str__(self) -> str:
        return self.title


class Episode(models.Model):
    """Модель эпизода."""

    series = models.ForeignKey("Series", on_delete=models.CASCADE)

    file_id = models.TextField(unique=False)
    message_id = models.IntegerField(unique=True)

    episode = models.IntegerField()
    season = models.IntegerField()
    lang = models.CharField(max_length=3, choices=Langs.choices, default=Langs.RUS)

    class Meta:
        """Метаданные."""

        unique_together = ["series", "episode", "season", "lang"]
        db_table = "episodes"

        verbose_name = "Эпизоды"
        verbose_name_plural = "Эпизоды"

    def update_content(self, file_content: FileContent) -> None:
        """Обновляет данные контента."""
        self.file_id = file_content.file_id
        self.message_id = file_content.message_id

        self.save()

    def __str__(self) -> str:
        """Текстовое представление эпизода."""
        return f"{self.series.title} {self.season}/{self.episode} {self.lang}"
