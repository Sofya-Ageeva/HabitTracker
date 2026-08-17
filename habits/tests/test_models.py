from django.test import TestCase
from django.contrib.auth import get_user_model
from habits.models import Habit
from django.core.exceptions import ValidationError

User = get_user_model()


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='test123456'
        )

    def test_create_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='09:00:00',
            action='Утренняя зарядка',
            duration=60,
            periodicity=1,
        )
        self.assertEqual(habit.action, 'Утренняя зарядка')
        self.assertEqual(habit.user, self.user)

    def test_habit_duration_validation(self):
        with self.assertRaises(ValidationError):
            habit = Habit(
                user=self.user,
                place='Дом',
                time='09:00:00',
                action='Долгая привычка',
                duration=150,  # Больше 120 секунд
                periodicity=1,
            )
            habit.full_clean()

    def test_periodicity_validation(self):
        with self.assertRaises(ValidationError):
            habit = Habit(
                user=self.user,
                place='Дом',
                time='09:00:00',
                action='Редкая привычка',
                duration=60,
                periodicity=14,
            )
            habit.full_clean()
