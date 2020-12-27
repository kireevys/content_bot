from main.components.view import View
from main.components.keyborad import Keyboard
from main.components.button import Button


class MainMenu(View):
    """Представление главного меню."""

    def __init__(self, description: str, media: str) -> None:
        super().__init__(description, media)

    def build_keyboard(self) -> Keyboard:
        """Создание клавиатуры для главного меню."""
        return Keyboard(Button("Меню сериалов", {}), Button("Меню фильмов", {}))
