from django.db import models


class Meter(models.Model):

    name = models.CharField(max_length=255)
    work_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Branches(models.Model):

    name = models.CharField(max_length=100)
    small_name = models.CharField(max_length=10)
    description = models.TextField(blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Rating(models.Model):

    branch = models.ForeignKey(Branches, on_delete=models.CASCADE)
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    pools = models.IntegerField(default=0)
    percent = models.FloatField(default=0.0)
    pool_date = models.DateField()

    objects = models.Manager()

    @staticmethod
    def date_pools():
        date_ = Rating.objects.all().select_related('branch').values('pool_date').distinct().order_by('-pool_date')
        return date_

    # def __str__(self):
    #     return f'Дата опроса {self.pool_date}'
