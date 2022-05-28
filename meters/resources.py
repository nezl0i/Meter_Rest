from import_export import resources
from .models import Rating


class RatingResource(resources.ModelResource):
    class Meta:
        model = Rating
