from .views import RegistrationAPIView, UsersView

app_name = 'users'

routeList = [
    ('users/register', RegistrationAPIView),
    ('users/update', UsersView),
]
