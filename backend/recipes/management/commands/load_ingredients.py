import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load ingredients data to DB'

    def handle(self, *args, **kwargs):
        with open('recipes/data/ingredients.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                name, unit = row
                Ingredient.objects.get_or_create(
                    name=name, measurement_unit=unit)
