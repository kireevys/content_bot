from django.test import TestCase

from main.components.button import Button
from main.components.keyborad import Keyboard


class TestKeyboard(TestCase):
    """Проверка базового класса клавитуры."""

    def test_equals(self):
        """Проверка сравнения двух клавиатур."""
        for result, second, expected, ids in [
            (Keyboard(), Keyboard(), True, "both clear"),
            (
                Keyboard(Button("test_desc", {})),
                Keyboard(Button("test_desc", {})),
                True,
                "equals",
            ),
            (
                Keyboard(Button("first", {})),
                Keyboard(Button("second", {})),
                False,
                "different buttons",
            ),
            (
                Keyboard(Button("first", {}), Button("first", {})),
                Keyboard(Button("first", {})),
                False,
                "different buttons count",
            ),
        ]:
            with self.subTest(ids):
                self.assertEqual(result == second, expected)

    def test_order_buttons(self):
        """Проверка порядка кнопок."""
        buttons = [Button("b", {}), Button("a", {})]

        keyboard = Keyboard(*buttons)  # act

        self.assertEqual(keyboard.buttons[0], buttons[1])
        self.assertEqual(keyboard.buttons[1], buttons[0])
