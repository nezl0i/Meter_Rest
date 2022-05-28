from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from .models import Meter, Branches, Rating
from .serializers import MeterModelSerializer, BranchModelSerializer, RatingModelSerializer


class RatingModelPagination(PageNumberPagination):
    page_size = 10


class MeterModelViewSet(ModelViewSet):

    queryset = Meter.objects.all()
    serializer_class = MeterModelSerializer
    pagination_class = RatingModelPagination

    @classmethod
    def get_extra_actions(cls):
        return []


class BranchModelViewSet(ModelViewSet):

    queryset = Branches.objects.all()
    serializer_class = BranchModelSerializer
    pagination_class = RatingModelPagination

    @classmethod
    def get_extra_actions(cls):
        return []


class RatingModelViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingModelSerializer
    pagination_class = RatingModelPagination

    @classmethod
    def get_extra_actions(cls):
        return []
