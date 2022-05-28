import json
import xlsxwriter
import pandas as pd
from itertools import zip_longest
from django.core.management import BaseCommand
from backend import settings
from meters.models import Rating
from backend.settings import JSON_DIR


class Command(BaseCommand):

    workbook = xlsxwriter.Workbook(f'{JSON_DIR}/demo.xlsx')
    worksheet = workbook.add_worksheet()
    current_date = '2022-03-16'

    @staticmethod
    def slice_lst(lst):
        i = iter(lst)
        return list(zip_longest(i, i, i))

    @staticmethod
    def load_json(file):
        with open(f'{JSON_DIR}/{file}.json', encoding='utf-8') as json_file:
            return json.load(json_file)

    def handle(self, *args, **options):
        result_json = []
        total_json = []

        # Excel заголовок
        self.worksheet.write(0, 0, "id")
        self.worksheet.write(0, 1, "branch")
        self.worksheet.write(0, 2, "meter")
        self.worksheet.write(0, 3, "total")
        self.worksheet.write(0, 4, "pools")
        self.worksheet.write(0, 5, "percent")
        self.worksheet.write(0, 6, "pool_date")

        cols = [i for i in range(1, 35)]

        branches = {'Филиал': 0, 'Адыгейские ЭС': 1, 'Армавирские ЭС': 2, 'Краснодарские ЭС': 3, 'Лабинские ЭС': 4,
                    'Ленинградские ЭС': 5, 'Славянские ЭС': 6, 'Сочинские ЭС': 7, 'Тимашевские ЭС': 8,
                    'Тихорецкие ЭС': 9, 'Усть-Лабинские ЭС': 10, 'Юго-Западные ЭС': 11, 'ВСЕГО': 12}

        try:
            xls = pd.read_excel(f'{settings.BASE_DIR}/xlsx/16.03.2022.xlsx',
                                sheet_name='Разбивка по филиалам',
                                skiprows=2,
                                nrows=13,
                                usecols=cols,
                                keep_default_na=False)

            demo = xls.to_dict('list')

            for val in demo.values():
                result_json.append(val)

            tmp = list(zip(*result_json))
            tmp.pop(0)

            for item in tmp:
                _item = list(item)
                branch = branches[_item.pop(0)]
                slice_lst = self.slice_lst(_item)

                for meter, val in enumerate(slice_lst, 1):
                    total = val[0]
                    pools = val[1]
                    percent = val[2] * 100

                    total_json.append(dict(
                        {"branch": branch, "meter": meter, "total": total, "pools": pools, "percent": percent,
                         "pool_date": self.current_date}))

                    self.worksheet.write(meter, 1, branch)
                    self.worksheet.write(meter, 2, meter)
                    self.worksheet.write(meter, 3, total)
                    self.worksheet.write(meter, 4, pools)
                    self.worksheet.write(meter, 5, percent)
                    self.worksheet.write(meter, 6, self.current_date)

            with open(f'{JSON_DIR}/rating.json', 'w', encoding='utf-8') as json_file:
                json_file.write(json.dumps(total_json))

            print('Create json file is Done.')
            self.workbook.close()

            """
            Запись в БД
            """
            ratings = self.load_json('rating')
            Rating.objects.all().delete()
            for rating in ratings:
                Rating.objects.create(
                    branch_id=rating.get('branch'),
                    meter_id=rating.get('meter'),
                    total=rating.get('total'),
                    pools=rating.get('pools'),
                    percent=rating.get('percent'),
                    pool_date=rating.get('pool_date')
                )

            print('Add data in DB is Done.')

        except FileNotFoundError as e:
            print('No such file.')
            return e.strerror
