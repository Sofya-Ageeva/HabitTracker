from rest_framework import generics, permissions
from .serializers import UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
