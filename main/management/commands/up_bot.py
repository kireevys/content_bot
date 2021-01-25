from django.conf import settings
from django.core.management.base import BaseCommand

from main.tg.run import run


class Command(BaseCommand):
    """Команда поднятия бота."""

    help = "Bot up"  # noqa: VNE003

    def check_env(self):
        """Проверка окружения."""
        if None in (settings.TOKEN,):
            raise EnvironmentError("Check your ENV")

    def handle(self, *args, **options):
        """Исполняемый метод."""
        self.check_env()

        run()
