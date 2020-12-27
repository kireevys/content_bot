import enum

import main.models.common
from main import models


class Static(enum.Enum):
    """Прокси для часто используемой статики."""

    MAIN = "main"

    def __init__(self, slug: str):
        self.slug = slug

    @property
    def link(self) -> str:
        """Геттер для ссылки модели."""
        return self.model.link

    @property
    def model(self) -> main.models.common.Static:
        """Инициализация модели.

        Это необходимо, чтобы во время инициализации
        приложение не пыталось получить доступ к БД.
        """
        return main.models.common.Static.get_by_slug(self.slug)
