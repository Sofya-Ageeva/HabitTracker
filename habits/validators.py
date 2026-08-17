from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_habit_time(value):
    """Проверка, что время выполнения не превышает 120 секунд"""
    if value > 120:
        raise ValidationError(
            'Время выполнения не должно превышать 120 секунд'
        )


def validate_periodicity(value):
    """Проверка, что периодичность от 1 до 7 дней"""
    if not (1 <= value <= 7):
        raise ValidationError(
            'Периодичность должна быть от 1 до 7 дней'
        )


def validate_pleasant_habit(data):
    """Валидация приятной привычки"""
    if data.get('is_pleasant'):
        if data.get('reward'):
            raise ValidationError(
                'Приятная привычка не может иметь вознаграждение'
            )
        if data.get('related_habit'):
            raise ValidationError(
                'Приятная привычка не может иметь связанную привычку'
            )


def validate_related_habit(data):
    """Проверка связанной привычки"""
    if data.get('related_habit'):
        if not data['related_habit'].is_pleasant:
            raise ValidationError(
                'Связанная привычка должна быть приятной'
            )


def validate_reward_and_related(data):
    """Проверка, что нельзя одновременно указывать reward и related_habit"""
    if data.get('reward') and data.get('related_habit'):
        raise ValidationError(
            'Нельзя одновременно указывать вознаграждение и связанную привычку'
        )
    