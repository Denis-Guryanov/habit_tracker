from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import User

from .models import Habit


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"], password=validated_data["password"]
        )
        return user


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, data):
        # Исключить одновременный выбор связанной привычки и указания вознаграждения
        if data.get("related_habit") and data.get("reward"):
            raise serializers.ValidationError(
                "Можно указать только одно: либо связанную привычку, либо вознаграждение."
            )
        # Время выполнения не больше 120 секунд
        if data.get("duration", 0) > 120:
            raise serializers.ValidationError(
                "Время на выполнение не должно превышать 120 секунд."
            )
        # В связанные привычки могут попадать только приятные привычки
        if data.get("related_habit") and not data["related_habit"].is_pleasant:
            raise serializers.ValidationError(
                "В связанные привычки можно выбирать только приятные привычки."
            )
        # У приятной привычки не может быть вознаграждения или связанной привычки
        if data.get("is_pleasant") and (
            data.get("reward") or data.get("related_habit")
        ):
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )
        # Нельзя выполнять привычку реже, чем 1 раз в 7 дней
        if data.get("period", 1) > 7:
            raise serializers.ValidationError(
                "Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
            )
        if data.get("period", 1) < 1:
            raise serializers.ValidationError(
                "Периодичность должна быть не менее 1 дня."
            )
        return data

    def validate_duration(self, value):
        """Валидация длительности привычки"""
        if value > 120:
            raise serializers.ValidationError(
                "Время на выполнение не должно превышать 120 секунд."
            )
        return value
