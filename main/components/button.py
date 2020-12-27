from abc import ABC


class Button(ABC):
    """Кнопка клавиатуры."""

    def __init__(self, description: str, callback: dict) -> None:
        self.description = description
        self.callback = callback

    def __eq__(self, other: "Button") -> bool:
        """Правила сравнения двух кнопок."""
        eq_description = self.description == other.description
        eq_callback = self.callback == other.callback

        return all((eq_callback, eq_description))

    def __repr__(self) -> str:  # pragma: no cover
        """Строковое представление кнопки."""
        return self.description