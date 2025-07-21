from celery import shared_task
from django.utils import timezone

from .models import Habit
from .telegram import send_telegram_message


@shared_task
def send_habit_reminders_for_today():
    today = timezone.now().date()
    now_time = timezone.now().time()
    habits = Habit.objects.filter(chat_id__isnull=False)
    for habit in habits:
        # Проверяем, нужно ли напоминать сегодня (по периодичности)
        if habit.period and habit.user.date_joined:
            days_since = (today - habit.user.date_joined.date()).days
            if days_since % habit.period != 0:
                continue
        # Время напоминания: если время привычки близко к текущему (±5 минут)
        if (abs((timezone.datetime.combine(today, habit.time) - timezone.now()).total_seconds()) <= 300):
            send_telegram_message(
                habit.chat_id,
                f"Напоминание: {habit.action} в {habit.time} в {habit.place}",
            )


@shared_task
def send_habit_reminder(habit_id, chat_id):
    from .models import Habit

    try:
        habit = Habit.objects.get(id=habit_id)
        send_telegram_message(
            chat_id, f"Напоминание: {habit.action} в {habit.time} в {habit.place}"
        )
    except Habit.DoesNotExist:
        pass
