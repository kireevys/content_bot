from django.test import TestCase

from main.components.button import Button


class TestButton(TestCase):
    """Проверки базового класса кнопок."""

    def test_equals(self):
        """Проверка равенства."""
        for first, second, expected, ids in [
            (Button("test_desc", {}), Button("test_desc", {}), True, "equals"),
            (Button("first", {}), Button("second", {}), False, "different description"),
            (
                Button("test", {"1": "1"}),
                Button("test", {"1": "2"}),
                False,
                "different callback",
            ),
        ]:
            with self.subTest(ids):
                result = (first == second)  # act

                self.assertEqual(result, expected)
