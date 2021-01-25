from abc import ABC


class Button(ABC):
    """Кнопка клавиатуры."""

    def __init__(
        self, description: str, callback: dict, is_active: bool = False
    ) -> None:
        self._description = description
        self.callback = callback
        self.is_active = is_active

    @property
    def description(self) -> str:
        """Описание."""
        return f"[{self._description}]" if self.is_active else str(self._description)

    def __eq__(self, other: "Button") -> bool:
        """Правила сравнения двух кнопок."""
        eq_description = self._description == other._description
        eq_callback = self.callback == other.callback

        return all((eq_callback, eq_description))

    def __lt__(self, other: "Button"):
        return self._description > other._description

    def __repr__(self) -> str:  # pragma: no cover
        """Строковое представление кнопки."""
        return str(self._description)
