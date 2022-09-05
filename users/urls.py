from .views import RegistrationAPIView, UsersView
from django.urls import path

app_name = 'users'

# urlpatterns = [
#     path("register/", RegistrationAPIView.as_view(), name='register'),
#     path("update/", UsersView.as_view(), name='update')
#
# ]
routeList = [
    ('register', RegistrationAPIView),
    ('update', UsersView),
]
