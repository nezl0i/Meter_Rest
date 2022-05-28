from rest_framework.serializers import ModelSerializer
from .models import Meter, Branches, Rating


class MeterModelSerializer(ModelSerializer):
    class Meta:
        model = Meter
        fields = ('id', 'url', 'name', 'work_name', 'description')


class BranchModelSerializer(ModelSerializer):
    class Meta:
        model = Branches
        fields = ('id', 'url', 'name', 'small_name', 'description')


class RatingModelSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'url', 'branch', 'meter', 'total', 'pools', 'percent', 'pool_date')
