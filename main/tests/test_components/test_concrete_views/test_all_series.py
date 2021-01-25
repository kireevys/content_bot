from django.test import TestCase

from components.button import Button
from components.keyborad import Keyboard
from main import models
from views import AllSeries


class TestAllSeries(TestCase):
    """Проверка вьюхи Все Серии."""

    def test_keyboard(self):
        """Проверка создания клавиатуры."""
        objs_series = [
            (models.Series(title_ru=f"Тест_{num}", title_eng=f"Test_{num}"))
            for num, i in enumerate(range(10))
        ]
        models.Series.objects.bulk_create(objs_series)
        qs = models.Series.objects.all().order_by("pk")
        expected = Keyboard(
            *(
                Button(
                    s.title,
                    {"type": "series", "id": s.id},
                )
                for s in qs
            )
        )
        expected.append(Button("Главное меню", {"type": "main"}))
        view = AllSeries(qs)

        result = view.build_keyboard()

        self.assertEqual(len(result.buttons), len(objs_series) + 1)
        self.assertEqual(result, expected)
