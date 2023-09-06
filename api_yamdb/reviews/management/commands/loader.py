import csv
from django.conf import settings
from api_yamdb import settings
from django.core.management.base import BaseCommand
from reviews.models import Genre, Category, Title, Review, Comment
from users.models import User


MODELS_DATA = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    Title.genre.through: 'genre_title.csv',
}


class Command (BaseCommand):

    def handle(self, *args, **options):
        for model, csv_file in MODELS_DATA.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{csv_file}', 'r',
                encoding="utf-8",
            ) as file:
                reader = csv.DictReader(file)
                records = []
                for row in reader:
                    records.append(model(**row))
            model.objects.bulk_create(records)
            self.stdout.write(self.style.SUCCESS(
                'Данные загружены.'
            ))
