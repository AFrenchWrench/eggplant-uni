import os

from celery import Celery, shared_task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@shared_task
def add(x, y):
    return print(x + y)
