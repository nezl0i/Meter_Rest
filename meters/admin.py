from django.contrib import admin
from .models import Meter, Branches, Rating
from import_export.admin import ImportExportModelAdmin


class ApiMeter(admin.ModelAdmin):
    list_display = ['name', 'work_name', 'description']


class ApiBranches(admin.ModelAdmin):
    list_display = ['name', 'small_name', 'description']


class RatingAdmin(ImportExportModelAdmin):

    list_display = ['branch', 'meter', 'total', 'pools', 'percent', 'pool_date']
    list_filter = ('branch', 'meter', 'pool_date')
    list_per_page = 20
    search_fields = ('branch', 'meter', 'pool_date')
    ordering = ('branch',)


admin.site.register(Meter, ApiMeter)
admin.site.register(Branches, ApiBranches)
admin.site.register(Rating, RatingAdmin)




