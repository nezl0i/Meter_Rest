from django.urls import path, re_path
from home.views import index, pages, statistic, meters, tables_rating

urlpatterns = [
    path('', index, name='index'),

    path('meters/', tables_rating, name='meters'),
    path('meters_table/<str:date>/', meters, name='meters_table'),
    path('statistic/<str:date>/', statistic, name='statistic'),

    re_path(r'^.*\.*', pages, name='pages'),
]
