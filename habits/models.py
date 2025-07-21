from django.db import models
from users.models import User
from django.core.exceptions import ValidationError


class Habit(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    related_habit = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={"is_pleasant": True},
        verbose_name="Связанная привычка",
    )
    period = models.PositiveSmallIntegerField(
        default=1, verbose_name="Периодичность (в днях)"
    )
    reward = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Вознаграждение"
    )
    duration = models.PositiveSmallIntegerField(
        verbose_name="Время на выполнение (сек)"
    )
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")
    chat_id = models.CharField(
        max_length=32, blank=True, null=True, verbose_name="Telegram chat ID"
    )

    def clean(self):
        # Исключить одновременный выбор связанной привычки и указания вознаграждения
        if self.related_habit and self.reward:
            raise ValidationError(
                "Можно указать только одно: либо связанную привычку, "
                "либо вознаграждение."
            )
        # Время выполнения не больше 120 секунд
        if self.duration > 120:
            raise ValidationError("Время на выполнение не должно превышать 120 секунд.")
        # В связанные привычки могут попадать только приятные привычки
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError(
                "В связанные привычки можно выбирать только приятные привычки."
            )
        # У приятной привычки не может быть вознаграждения или связанной привычки
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения или "
                "связанной привычки."
            )
        # Нельзя выполнять привычку реже, чем 1 раз в 7 дней
        if self.period > 7:
            raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")
        if self.period < 1:
            raise ValidationError("Периодичность должна быть не менее 1 дня.")

    def __str__(self):
        return f"{self.action} в {self.time} в {self.place}"
