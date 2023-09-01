import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_settings.settings")

app = Celery("project_settings")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "parse-every-10-min": {
        "task": "products.tasks.parse_feedbacks",
        "schedule": crontab(minute="*/10"),
    },
}
