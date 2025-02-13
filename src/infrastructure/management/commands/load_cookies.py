from django.core.management.base import BaseCommand
from infrastructure.models import CookieFileORM

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.save_cookie_file_to_db('C:/Users/heppy/Desktop/NEWER-PY-main/ads.tiktok.com.cookies.json', 'ads.tiktok.com.cookies.json')

    def save_cookie_file_to_db(self, file_path, name):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        cookie_file = CookieFileORM(name=name, content=content)
        cookie_file.save()

        print(f"Файл с куки успешно загружен: {cookie_file.name}")
