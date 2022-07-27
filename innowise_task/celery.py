import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innowise_task.settings')

app = Celery('innowise_task')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(name="add")
def add(x, y):
 return x+y