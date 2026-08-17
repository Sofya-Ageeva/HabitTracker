from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Habit"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = [
            'id', 'user', 'place', 'time', 'action',
            'is_pleasant', 'related_habit', 'periodicity',
            'reward', 'duration', 'is_public',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        """Валидация при создании/обновлении"""
        if data.get('related_habit'):
            if not data['related_habit'].is_pleasant:
                raise serializers.ValidationError({
                    'related_habit': 'Связанная привычка должна быть приятной'
                })

        if data.get('is_pleasant'):
            if data.get('reward'):
                raise serializers.ValidationError({
                    'reward': 'Приятная привычка не может иметь вознаграждение'
                })
            if data.get('related_habit'):
                raise serializers.ValidationError({
                    'related_habit': 'Приятная привычка не может иметь связанную привычку'
                })

        if data.get('reward') and data.get('related_habit'):
            raise serializers.ValidationError({
                'reward': 'Нельзя одновременно указывать вознаграждение и связанную привычку'
            })

        return data


class HabitListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка привычек (краткая версия)"""

    class Meta:
        model = Habit
        fields = ['id', 'action', 'time', 'place', 'periodicity', 'is_public']
