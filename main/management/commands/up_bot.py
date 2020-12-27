from django.conf import settings
from django.core.management.base import BaseCommand

from main.tg.run import run


class Command(BaseCommand):
    help = "Bot up"

    def check_env(self):
        if None in (settings.TOKEN,):
            raise EnvironmentError("Check your ENV")

    def handle(self, *args, **options):
        self.check_env()

        run()
