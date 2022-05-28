import json
from backend import settings
from django.core.management import BaseCommand
from meters.models import Meter


def load_from_json(file_name):
    with open(f'{settings.BASE_DIR}/json/{file_name}.json', encoding='utf-8') as json_file:
        return json.load(json_file)


class Command(BaseCommand):

    def handle(self, *args, **options):
        meters = load_from_json('meters')
        Meter.objects.all().delete()
        for meter in meters:
            Meter.objects.create(**meter)
