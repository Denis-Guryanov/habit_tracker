import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    "send-habit-reminders-every-5-minutes": {
        "task": "habits.tasks.send_habit_reminders_for_today",
        "schedule": crontab(minute="*/5"),
    },
}
