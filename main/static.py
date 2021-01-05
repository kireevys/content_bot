from main import models


class Static:
    """Прокси для часто используемой статики."""

    MAIN = "main"

    def __init__(self, slug: str):
        self.slug = slug

    @property
    def link(self) -> str:
        """Геттер для ссылки модели."""
        return self.model.link

    @property
    def model(self) -> models.Static:
        """Инициализация модели.

        Это необходимо, чтобы во время инициализации
        приложение не пыталось получить доступ к БД.
        """
        return models.Static.get_by_slug(self.slug)
