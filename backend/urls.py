from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from meters.upload import simple_upload
from meters.views import MeterModelViewSet, BranchModelViewSet, RatingModelViewSet
from users import urls as user_url

routeLists = [user_url.routeList]

router = DefaultRouter()
router.register('branches', BranchModelViewSet)
router.register('meters', MeterModelViewSet)
router.register('rating', RatingModelViewSet)

for routeList in routeLists:
    # print(routeList)
    for route in routeList:
        router.register(route[0], route[1], basename=route[0])


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('upload/', simple_upload),
    # path('api/users/', include('users.urls', namespace='users')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
