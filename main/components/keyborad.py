from abc import ABC
from typing import List

from main.components.button import Button


class Keyboard(ABC):
    """Клавиатура для вьюхи."""

    def __init__(self, *buttons: Button) -> None:
        self.buttons: List[Button] = sorted(buttons, reverse=True)

    def append(self, button: Button) -> None:
        """Добавляет кнопку к клавиатуре."""
        self.buttons.append(button)

    def __eq__(self, other: "Keyboard") -> bool:
        """Правила сравнения двух клавиатур."""
        if len(self.buttons) != len(other.buttons):
            return False

        return all(this == them for this, them in zip(self.buttons, other.buttons))

    def __repr__(self):
        return " | ".join(map(repr, self.buttons))
