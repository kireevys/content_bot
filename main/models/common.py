from functools import lru_cache

from django.db import models

__all__ = ("User", "Genre", "Static", "Langs")


class User(models.Model):
    """Модель Пользователя."""

    user_id = models.IntegerField(unique=True)
    user_name = models.TextField(null=True)
    first_name = models.TextField(null=True)
    authorize = models.BooleanField(default=True)
    add_date = models.DateTimeField(auto_now_add=True)


class Static(models.Model):
    """Модель статики."""

    link = models.URLField()
    description = models.CharField(max_length=128)
    slug = models.CharField(unique=True, max_length=10)
    add_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Текстовое представление модели."""
        return self.slug

    @classmethod
    @lru_cache(maxsize=8)
    def get_by_slug(cls, slug: str) -> "Static":
        """Получение модели по slug."""
        return cls.objects.get(slug=slug)


class Langs(models.TextChoices):
    """Доступные озвучки."""

    SUB = "SUB", "sub"
    RUS = "RUS", "russian"
    ENG = "ENG", "english"

    @classmethod
    def repr(cls, lang) -> str:
        """Представление языка."""
        _map = {
            Langs.RUS: "на русском",
            Langs.SUB: "с субтитрами",
            Langs.ENG: "на английском",
        }
        return _map.get(lang, "")


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(max_length=20, unique=True)

    class Meta:
        """Метаданные."""

        db_table = "genres"
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self) -> str:
        return self.name
