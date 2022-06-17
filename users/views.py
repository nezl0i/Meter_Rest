from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response

from users.serializers import UserViewSerializer, RegistrationSerializer
from users.models import User


class UsersModelPagination(PageNumberPagination):
    page_size = 5


class UsersView(viewsets.ModelViewSet):
    """
    Просмотр и редактирование пользователей
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserViewSerializer
    pagination_class = UsersModelPagination
    permission_classes = (IsAdminUser,)


class RegistrationAPIView(viewsets.ModelViewSet):
    """
    Регистрация пользователя
    """
    queryset = User.objects.filter(is_active=True).order_by('id')
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    pagination_class = UsersModelPagination
    # renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})

        # Паттерн создания сериализатора, валидации и сохранения - довольно
        # стандартный, и его можно часто увидеть в реальных проектах.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
