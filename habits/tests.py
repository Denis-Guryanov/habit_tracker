from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.exceptions import ValidationError
from .models import Habit
from .serializers import HabitSerializer
from users.models import User

class HabitModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass'
        )

    def test_habit_model_validation(self):
        """Тест базовой валидации модели привычки"""
        habit = Habit(
            user=self.user,
            place='Дом',
            time='12:00',
            action='Пить воду',
            is_pleasant=False,
            period=1,
            duration=60
        )
        habit.full_clean()  # Не должно быть ошибок

    def test_habit_duration_validation(self):
        """Тест валидации продолжительности привычки"""
        habit = Habit(
            user=self.user,
            place='Дом',
            time='12:00',
            action='Пить воду',
            is_pleasant=False,
            period=1,
            duration=121  # Больше 120 секунд
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_habit_period_validation(self):
        """Тест валидации периода привычки"""
        habit = Habit(
            user=self.user,
            place='Дом',
            time='12:00',
            action='Пить воду',
            is_pleasant=False,
            period=8,  # Больше 7 дней
            duration=60
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_pleasant_habit_validation(self):
        """Тест валидации приятной привычки"""
        habit = Habit(
            user=self.user,
            place='Дом',
            time='12:00',
            action='Смотреть сериал',
            is_pleasant=True,
            period=1,
            duration=60,
            reward='Шоколадка'  # У приятной привычки не может быть вознаграждения
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_related_habit_validation(self):
        """Тест валидации связанной привычки"""
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='12:00',
            action='Смотреть сериал',
            is_pleasant=True,
            period=1,
            duration=60
        )
        
        unpleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='12:00',
            action='Работать',
            is_pleasant=False,
            period=1,
            duration=60
        )

        habit = Habit(
            user=self.user,
            place='Дом',
            time='12:00',
            action='Учиться',
            is_pleasant=False,
            period=1,
            duration=60,
            related_habit=unpleasant_habit  # Связанная привычка должна быть приятной
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

        # Проверяем что можно привязать приятную привычку
        habit.related_habit = pleasant_habit
        habit.full_clean()  # Не должно быть ошибок

    def test_reward_and_related_habit_validation(self):
        """Тест валидации одновременного указания связанной привычки и вознаграждения"""
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='12:00',
            action='Смотреть сериал',
            is_pleasant=True,
            period=1,
            duration=60
        )

        habit = Habit(
            user=self.user,
            place='Дом',
            time='12:00',
            action='Учиться',
            is_pleasant=False,
            period=1,
            duration=60,
            related_habit=pleasant_habit,
            reward='Шоколадка'  # Нельзя указывать и связанную привычку, и вознаграждение
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

class HabitSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test2@example.com',
            password='testpass'
        )

    def test_habit_serializer_validation(self):
        """Тест валидации сериализатора привычки"""
        data = {
            'user': self.user.id,
            'place': 'Офис',
            'time': '09:00',
            'action': 'Встать',
            'is_pleasant': False,
            'period': 1,
            'duration': 60,
        }
        serializer = HabitSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_serializer_duration_validation(self):
        """Тест валидации продолжительности в сериализаторе"""
        data = {
            'user': self.user.id,
            'place': 'Офис',
            'time': '09:00',
            'action': 'Встать',
            'is_pleasant': False,
            'period': 1,
            'duration': 121,  # Больше 120 секунд
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('duration', serializer.errors)

class UserRegistrationTests(APITestCase):
    def test_register_user(self):
        """Тест регистрации пользователя"""
        data = {
            'email': 'newuser@example.com',
            'password': 'newpass123'
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

class HabitAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='apiuser@example.com',
            password='apipass'
        )
        self.client.force_authenticate(user=self.user)
        self.habit_data = {
            'place': 'Парк',
            'time': '08:00',
            'action': 'Бегать',
            'is_pleasant': False,
            'period': 1,
            'duration': 60
        }

    def test_create_habit(self):
        """Тест создания привычки"""
        self.habit_data['user'] = self.user.id
        response = self.client.post('/api/habits/', self.habit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)

    def test_read_habit(self):
        """Тест чтения привычки"""
        habit = Habit.objects.create(user=self.user, **self.habit_data)
        response = self.client.get(f'/api/habits/{habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], self.habit_data['place'])

    def test_update_habit(self):
        """Тест обновления привычки"""
        habit = Habit.objects.create(user=self.user, **self.habit_data)
        response = self.client.patch(f'/api/habits/{habit.id}/', {'place': 'Стадион'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.get(id=habit.id).place, 'Стадион')

    def test_delete_habit(self):
        """Тест удаления привычки"""
        habit = Habit.objects.create(user=self.user, **self.habit_data)
        response = self.client.delete(f'/api/habits/{habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_list_public_habits(self):
        """Тест получения списка публичных привычек"""
        # Создаем публичную привычку
        public_habit = Habit.objects.create(user=self.user, is_public=True, **self.habit_data)
        # Создаем приватную привычку
        private_habit = Habit.objects.create(user=self.user, is_public=False, **self.habit_data)
        
        response = self.client.get('/api/habits/?public=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Только публичная привычка
        self.assertEqual(response.data['results'][0]['id'], public_habit.id)
