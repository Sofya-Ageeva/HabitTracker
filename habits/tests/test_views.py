from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from habits.models import Habit

User = get_user_model()


class HabitAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='test123456'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        data = {
            'place': 'Дом',
            'time': '09:00:00',
            'action': 'Зарядка',
            'duration': 60,
            'periodicity': 1,
        }
        response = self.client.post('/api/v1/habits/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_habit_with_reward_and_related(self):
        pleasant = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='10:00:00',
            action='Приятная привычка',
            duration=30,
            periodicity=1,
            is_pleasant=True,
        )

        data = {
            'place': 'Дом',
            'time': '09:00:00',
            'action': 'Полезная привычка',
            'duration': 60,
            'periodicity': 1,
            'reward': 'Шоколадка',
            'related_habit': pleasant.id,
        }
        response = self.client.post('/api/v1/habits/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_habits(self):
        Habit.objects.create(
            user=self.user,
            place='Дом',
            time='09:00:00',
            action='Привычка 1',
            duration=60,
            periodicity=1,
        )
        Habit.objects.create(
            user=self.user,
            place='Дом',
            time='10:00:00',
            action='Привычка 2',
            duration=60,
            periodicity=1,
        )
        response = self.client.get('/api/v1/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
