from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
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

    def get_permissions(self):
        """Разные права для разных действий"""
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsOwner]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

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

    def perform_update(self, serializer):
        """При обновлении проверяем права"""
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied("Вы не можете редактировать эту привычку")
        serializer.save()

    def perform_destroy(self, instance):
        """При удалении проверяем права"""
        if instance.user != self.request.user:
            raise PermissionDenied("Вы не можете удалить эту привычку")
        instance.delete()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_habits(self, request):
        """Список привычек текущего пользователя"""
        habits = Habit.objects.filter(user=request.user)
        serializer = HabitListSerializer(habits, many=True)
        return Response(serializer.data)

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
        operation_description="Получение списка привычек (свои + публичные)",
        responses={200: HabitListSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получение деталей привычки",
        responses={200: HabitSerializer(), 404: "Не найдено"}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Полное обновление привычки",
        request_body=HabitSerializer,
        responses={200: HabitSerializer(), 400: "Ошибка валидации", 403: "Нет прав"}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частичное обновление привычки",
        request_body=HabitSerializer,
        responses={200: HabitSerializer(), 400: "Ошибка валидации", 403: "Нет прав"}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удаление привычки",
        responses={204: "Удалено", 403: "Нет прав", 404: "Не найдено"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)



