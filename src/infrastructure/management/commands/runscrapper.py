from django.core.management.base import BaseCommand
from src.adapters.project_pars import TiktokScrapper

class Command(BaseCommand):
    help = 'Запускает парсер для TikTok'

    def handle(self, *args, **kwargs):
        TiktokScrapper().create_driver()
