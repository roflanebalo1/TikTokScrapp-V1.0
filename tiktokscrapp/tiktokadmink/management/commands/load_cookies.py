from django.core.management.base import BaseCommand
from tiktokadmink.models import CookieFile

class Command(BaseCommand):
    help = 'Загрузка файла cookies в базу данных'

    def handle(self, *args, **kwargs):
        file_path = 'C:/Users/heppy/Desktop/NEWER-PY-main/ads.tiktok.com.cookies.json'
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            CookieFile.objects.create(name='ads.tiktok.com.cookies.json', content=content)
            self.stdout.write(self.style.SUCCESS('Файл успешно добавлен в базу данных'))