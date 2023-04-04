import csv

from django.conf import settings
from django.core.management import BaseCommand
from reviews.models import (Category, Genre, TitleGenre,
                            Title)

# пока импортировал готовые модели
MODELSDICT = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    TitleGenre: 'genre_title.csv',
}


class Command(BaseCommand):
    """Менеджмент команда для добавления записей в БД"""

    def handle(self, *args, **kwargs):
        try:
            for model, data in MODELSDICT.items():
                with open(
                    f'{settings.BASE_DIR}/static/data/{data}',
                    'r',
                    encoding='utf-8'
                ) as csv_file:
                    reader = csv.DictReader(csv_file)
                    model.objects.bulk_create(
                        model(**record) for record in reader)
            self.stdout.write(
                self.style.SUCCESS('Загрузка завершена!'))

        except Exception as ex:
            # на случай возможных ошибок
            self.stdout.write(
                self.style.ERROR(
                    f'Возникла ошибка при загрузке данных! {ex}'))
