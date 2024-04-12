import os

from celery import Celery, shared_task


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
#os.environ.setdefault('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/')
#os.environ.setdefault('CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379/')



app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
