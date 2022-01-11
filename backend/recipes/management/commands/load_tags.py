import csv

from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = "Load tags from csv file."

    def handle(self, *args, **kwargs):
        with open('recipes/data/tags.csv', encoding='utf-8') as tags:
            for row in csv.reader(tags):
                name, color, slug = row
                Tag.objects.get_or_create(
                    name=name, color=color, slug=slug
                )
