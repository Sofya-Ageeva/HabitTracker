from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Habit(models.Model):
    """Модель привычки"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь'
    )

    place = models.CharField(
        max_length=200,
        verbose_name='Место выполнения'
    )

    time = models.TimeField(
        verbose_name='Время выполнения'
    )

    action = models.CharField(
        max_length=255,
        verbose_name='Действие'
    )

    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки'
    )

    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='related_to',
        verbose_name='Связанная привычка',
        help_text='Может быть только приятной привычкой'
    )

    periodicity = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        verbose_name='Периодичность (дни)',
        help_text='От 1 до 7 дней'
    )

    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Вознаграждение'
    )

    duration = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(120)],
        verbose_name='Время на выполнение (сек)',
        help_text='Не более 120 секунд'
    )

    is_public = models.BooleanField(
        default=False,
        verbose_name='Публичная привычка'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.action} в {self.time}"

    def clean(self):
        """Валидация модели"""
        from django.core.exceptions import ValidationError

        if self.reward and self.related_habit:
            raise ValidationError(
                'Нельзя одновременно указывать вознаграждение и связанную привычку'
            )

        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError(
                'Связанная привычка должна быть приятной'
            )

        if self.is_pleasant:
            if self.reward:
                raise ValidationError(
                    'Приятная привычка не может иметь вознаграждение'
                )
            if self.related_habit:
                raise ValidationError(
                    'Приятная привычка не может иметь связанную привычку'
                )

        if self.duration > 120:
            raise ValidationError(
                'Время выполнения не должно превышать 120 секунд'
            )

        if not (1 <= self.periodicity <= 7):
            raise ValidationError(
                'Периодичность должна быть от 1 до 7 дней'
            )
