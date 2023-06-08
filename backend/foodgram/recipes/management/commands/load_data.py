import os
import json

from django.conf import settings

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError

from recipes.models import Ingredient

base_dir = settings.BASE_DIR


class Command(BaseCommand):
    help = 'Импорт ингридиентов с json файла'

    def handle(self, *args, **options):
        ingredients = []
        try:
            with open(
                 (os.path.join(
                  base_dir, 'data/ingredients.json')),
                    encoding='utf-8') as file_ingredients:
                data = json.load(file_ingredients)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Файл не найден'))

        for ingredient in data:
            ingredients.append(
                Ingredient(
                    name=ingredient['name'],
                    measurement_unit=ingredient['measurement_unit']
                )
            )
        try:
            Ingredient.objects.bulk_create(ingredients)
            self.stdout.write(self.style.SUCCESS("Ингридиенты загружены"))
        except ValidationError as error:
            self.style.ERROR(
                'Ошибка загрузки файла с ингридами, ошибка {}'.format(
                    str(error)))
