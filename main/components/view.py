from abc import ABC, abstractmethod

from main.components.keyborad import Keyboard


class View(ABC):
    """Представление экрана."""

    caption: str
    media: str
    keyboard = None

    @abstractmethod
    def build_keyboard(self) -> Keyboard:
        """Создание клавиатуры представления."""

    def __eq__(self, other: "View") -> bool:
        if self.caption != other.caption:
            return False

        if self.media != other.media:
            return False

        if self.keyboard != other.keyboard:
            return False

        return True


class PhotoView(View):
    """Вьюха для картинок."""


class VideoView(View):
    """Вьюха для видосов."""
