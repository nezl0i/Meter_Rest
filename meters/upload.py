import xlsxwriter
import pandas as pd
import json
from django.contrib import messages
from django.shortcuts import render
from itertools import zip_longest
from backend.settings import JSON_DIR
from .resources import RatingResource
from tablib import Dataset
from .models import Rating
from django.contrib.auth.decorators import login_required


def slice_lst(lst):
    i = iter(lst)
    return list(zip_longest(i, i, i))


def load_json(file):
    with open(f'{JSON_DIR}/{file}.json', encoding='utf-8') as json_file:
        return json.load(json_file)


@login_required(login_url="/login/")
def simple_upload(request):

    if request.method == 'POST':
        rating_resource = RatingResource()
        dataset = Dataset()
        if not request.FILES:
            messages.error(request, 'Файл не выбран')
            return render(request, 'meters/upload.html')
        else:
            new_rating = request.FILES['myfile']

        if not new_rating.name.endswith('xlsx'):
            messages.error(request, 'Неверный формат файла')
            return render(request, 'meters/upload.html')

        tmp_date = new_rating.name.split('.')[:3]
        tmp_date.reverse()
        current_date = '-'.join(tmp_date)
        workbook = xlsxwriter.Workbook(f'{JSON_DIR}/{current_date}.xlsx')
        worksheet = workbook.add_worksheet()

        result_json = []
        total_json = []

        # Excel заголовок
        worksheet.write(0, 0, "id")
        worksheet.write(0, 1, "branch")
        worksheet.write(0, 2, "meter")
        worksheet.write(0, 3, "total")
        worksheet.write(0, 4, "pools")
        worksheet.write(0, 5, "percent")
        worksheet.write(0, 6, "pool_date")

        cols = [i for i in range(1, 35)]

        branches = {'Филиал': 0, 'Адыгейские ЭС': 1, 'Армавирские ЭС': 2, 'Краснодарские ЭС': 3, 'Лабинские ЭС': 4,
                    'Ленинградские ЭС': 5, 'Славянские ЭС': 6, 'Сочинские ЭС': 7, 'Тимашевские ЭС': 8,
                    'Тихорецкие ЭС': 9, 'Усть-Лабинские ЭС': 10, 'Юго-Западные ЭС': 11, 'ВСЕГО': 12}

        try:
            xls = pd.read_excel(new_rating,
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
            count = 1
            for item in tmp:
                _item = list(item)
                branch = branches[_item.pop(0)]
                slice_list = slice_lst(_item)

                for meter, val in enumerate(slice_list, 1):
                    total = val[0]
                    pools = val[1]
                    percent = val[2] * 100

                    total_json.append(dict(
                        {
                            "branch": branch,
                            "meter": meter,
                            "total": total,
                            "pools": pools,
                            "percent": percent,
                            "pool_date": current_date
                        }))

                    worksheet.write(count, 1, branch)
                    worksheet.write(count, 2, meter)
                    worksheet.write(count, 3, total)
                    worksheet.write(count, 4, pools)
                    worksheet.write(count, 5, percent)
                    worksheet.write(count, 6, current_date)

                    count += 1

            with open(f'{JSON_DIR}/rating.json', 'w', encoding='utf-8') as json_file:
                json_file.write(json.dumps(total_json))

            print('Create json file is Done.')
            workbook.close()

        except FileNotFoundError as e:
            print('No such file.')
            return e.strerror

        # imported_data = load_json('rating')
        # print(imported_data)
        # Rating.objects.all().delete()
        for data in total_json:
            Rating.objects.create(
                branch_id=data.get('branch'),
                meter_id=data.get('meter'),
                total=data.get('total'),
                pools=data.get('pools'),
                percent=data.get('percent'),
                pool_date=data.get('pool_date')
            )

        messages.info(request, 'Данные загружены успешно')
    return render(request, 'meters/upload.html')
