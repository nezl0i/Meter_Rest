import json
from backend import settings
from django.core.management import BaseCommand

from meters.models import Branches


def load_from_json(file_name):
    with open(f'{settings.BASE_DIR}/json/{file_name}.json', encoding='utf-8') as json_file:
        return json.load(json_file)


class Command(BaseCommand):

    def handle(self, *args, **options):
        branches = load_from_json('branches')
        Branches.objects.all().delete()
        for branch in branches:
            Branches.objects.create(**branch)

        # rest_user = Branches.objects.create_superuser(
        #     username='admin',
        #     password='restapi',
        #     email='admin2@gb.local'
        # )
