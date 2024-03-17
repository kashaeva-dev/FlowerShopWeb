from django.core.management.base import BaseCommand
from courier_bot.bot import run_courier_bot


class Command(BaseCommand):
    help = 'Запуск бота'

    def handle(self, *args, **options):
        run_courier_bot()
