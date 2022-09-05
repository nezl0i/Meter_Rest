import debug_toolbar
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from meters.upload import simple_upload
from meters.views import MeterModelViewSet, BranchModelViewSet, RatingModelViewSet
from users import urls as user_url

router = DefaultRouter()
router.register('branches', BranchModelViewSet)
router.register('meters', MeterModelViewSet)
router.register('rating', RatingModelViewSet)


routeLists = [user_url.routeList]

for routeList in routeLists:
    for route in routeList:
        router.register(f'users/{route[0]}', route[1], basename=route[0])


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('upload/', simple_upload),
    # path('api/users/', include('users.urls', namespace='users')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include("authentication.urls")),
    path('', include("home.urls")),
    # path('users/', include("users.urls"))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
