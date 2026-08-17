from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Habit
from .serializers import HabitSerializer, HabitListSerializer
from .permissions import IsOwner, IsPublicHabit
from .pagination import HabitPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с привычками"""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_pleasant', 'is_public']
    search_fields = ['action', 'place']
    ordering_fields = ['time', 'periodicity']

    pagination_class = HabitPagination

    def get_queryset(self):
        """Фильтруем привычки по пользователю"""
        user = self.request.user

        if user.is_superuser:
            return Habit.objects.all()

        return Habit.objects.filter(
            models.Q(user=user) | models.Q(is_public=True)
        ).distinct()

    def get_serializer_class(self):
        """Разные сериализаторы для списка и деталей"""
        if self.action == 'list':
            return HabitListSerializer
        return HabitSerializer

    def perform_create(self, serializer):
        """При создании привязываем пользователя"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_habits(self, request):
        """Список привычек текущего пользователя"""
        habits = Habit.objects.filter(user=request.user)
        serializer = HabitListSerializer(habits, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def public(self, request):
        """Список публичных привычек"""
        habits = Habit.objects.filter(is_public=True)
        serializer = HabitListSerializer(habits, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Создание новой привычки",
        request_body=HabitSerializer,
        responses={
            201: HabitSerializer(),
            400: "Ошибка валидации",
            401: "Неавторизован",
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Список публичных привычек",
        responses={200: HabitListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def public(self, request):
        """Список публичных привычек"""
        habits = Habit.objects.filter(is_public=True)
        serializer = HabitListSerializer(habits, many=True)
        return Response(serializer.data)
