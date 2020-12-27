from abc import ABC, abstractmethod

from main.components.keyborad import Keyboard


class View(ABC):
    """Представление экрана."""

    def __init__(self, description: str, media: str) -> None:
        self.keyboard: Keyboard = self.build_keyboard()
        self.description: str = description
        self.media: str = media

    @abstractmethod
    def build_keyboard(self) -> Keyboard:
        """Создание клавиатуры представления."""

    def __eq__(self, other: "View") -> bool:
        if self.description != other.description:
            return False

        if self.media != other.media:
            return False

        if self.keyboard != other.keyboard:
            return False

        return True