from abc import ABC
from typing import List

from main.components.button import Button


class Keyboard(ABC):
    """Клавиатура для вьюхи."""

    def __init__(self, *buttons: Button) -> None:
        self.buttons: List[Button] = self._order_buttons(*buttons)

    def _order_buttons(self, *buttons: Button) -> list:
        """Сортировка кнопок по алфавиту."""
        return sorted(buttons, key=lambda b: b.description)

    def __eq__(self, other: "Keyboard") -> bool:
        """Правила сравнения двух клавиатур."""
        if len(self.buttons) != len(other.buttons):
            return False

        for this, them in zip(self.buttons, other.buttons):
            if this != them:
                return False

        return True
