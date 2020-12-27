from main.views import MainMenu


class Controller:
    """Модуль, отвечающий за анализ запроса и вызов нужной модели."""
    def entry(self):
        """Точка входа в приложение."""
        return MainMenu('some', 'media')
